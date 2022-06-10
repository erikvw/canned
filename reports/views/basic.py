from django.db import OperationalError, connection, models
from django.views.generic import ListView


class CannedViewNameError(Exception):
    pass


class Dialect:
    def __init__(self, field_attr, type_attr):
        self.field = field_attr
        self.type = type_attr


Dialects = dict(mysql=Dialect("Field", "Type"), sqlite=Dialect("name", "type"))


class BasicView(ListView):
    queryset = None
    paginate_by = 100
    template_name = "canned_report.html"

    def get(self, request, *args, sql_view_name=None, **kwargs):
        self.model = self.get_dynamic_model_cls(sql_view_name)
        self.queryset = self.model.objects.raw(f"select * from {sql_view_name}")
        return super().get(request, *args, **kwargs)

    def get_dynamic_model_cls(self, sql_view_name):
        attrs = {}
        mysql_command = None
        sqlite_command = None
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"describe {sql_view_name}")
            except OperationalError:
                cursor.execute(f"select * from pragma_table_info('{sql_view_name}')")
                sqlite_command = f"select * from pragma_table_info('{sql_view_name}')"
            else:
                mysql_command = f"describe {sql_view_name}"
            columns = [col[0] for col in cursor.description]

        with connection.cursor() as cursor:
            if mysql_command:
                dialect = Dialects.get("mysql")
            elif sqlite_command:
                dialect = Dialects.get("sqlite")
            cursor.execute(mysql_command or sqlite_command)
            rows = cursor.fetchall()
            for row in rows:
                rowdict = dict(zip(columns, row))
                attrs.update(
                    {
                        rowdict.get(dialect.field): self.get_dynamic_field_cls(
                            rowdict.get(dialect.type)
                        ),
                    }
                )
            attrs.update({"__module__": "reports.models"})
        model_name = f"TemporaryView{sql_view_name.replace('_', '').lower().title()}"
        model_cls = type(model_name, (models.Model,), attrs)
        return model_cls

    @staticmethod
    def get_dynamic_field_cls(field_type):
        field_type = field_type.lower()
        if field_type.startswith("varchar"):
            max_length = int(field_type.replace("varchar(", "").split(")")[0])
            field_cls = models.CharField(max_length=max_length, null=True)
        elif field_type.startswith("char"):
            max_length = int(field_type.replace("char(", "").split(")")[0])
            field_cls = models.CharField(max_length=max_length, null=True)
        elif field_type.startswith("text"):
            field_cls = models.TextField(null=True)
        elif field_type.startswith("longtext"):
            field_cls = models.TextField(null=True)
        elif field_type.startswith("integer"):
            field_cls = models.IntegerField(null=True)
        elif field_type.startswith("int"):
            field_cls = models.IntegerField(null=True)
        elif field_type.startswith("datetime"):
            field_cls = models.DateTimeField(null=True)
        elif field_type.startswith("date"):
            field_cls = models.DateField(null=True)
        else:
            raise CannedViewNameError(f"Unknown field type. Got {field_type}.")
        return field_cls
