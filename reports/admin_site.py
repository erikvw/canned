from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

reports_admin = EdcAdminSite(name="reports_admin", app_label=AppConfig.name)
