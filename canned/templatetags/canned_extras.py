from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=False)
def write_table(object_list):
    table = [
        '<table id="table_id" class="table table-condensed table-hover table-responsive">\n'
    ]
    columns = None
    for obj in object_list:
        if not columns:
            columns = [k for k in obj.__dict__ if not k.startswith("_") and k != "id"]
            row = ["<thead>\n  <tr>\n"]
            for col in columns:
                row.append(f"    <th>{col}</th>\n")
            row.append("  </tr>\n</thead>\n")
            table.append("".join(row))
        row = ["<tbody>\n  <tr>\n"]
        for col in columns:
            value = getattr(obj, col)
            row.append(f"    <td>{value}</td>\n")
        row.append("  </tr>\n</tbody>\n")
        table.append("".join(row))
    table.append("</table>")
    return format_html("".join(table))
