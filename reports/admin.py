from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse

from canned.auth_objects import CANNED_SUPER_ROLE

from .admin_site import reports_admin
from .models import Reports
from .report_form import ReportsForm


@admin.register(Reports, site=reports_admin)
class ReportAdmin(admin.ModelAdmin):

    form = ReportsForm

    fieldsets = (
        (
            None,
            (
                {
                    "fields": (
                        "report_name",
                        "report_description",
                        "report_datetime",
                        "sql_view_name",
                    )
                }
            ),
        ),
    )

    list_display = ["report_name", "report_description", "sql_view_name", "list_view"]

    search_fields = ("report_name",)

    readonly_fields = ["sql_view_name"]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj) or []
        if "sql_view_name" in readonly_fields and CANNED_SUPER_ROLE in [
            role.name for role in request.user.userprofile.roles.all()
        ]:
            readonly_fields.remove("sql_view_name")
        return readonly_fields

    def list_view(self, obj=None, label=None):
        url = reverse(
            "reports:basic_report_url",
            kwargs=dict(sql_view_name=obj.sql_view_name),
        )
        context = dict(title="Go to report", url=url, label=label)
        return render_to_string("canned/report_button.html", context=context)
