from django.urls.conf import path
from django.views.generic import RedirectView

from .views import BasicView

app_name = "reports"

urlpatterns = [
    path("report_view/<sql_view_name>/", BasicView.as_view(), name="basic_report_url"),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
