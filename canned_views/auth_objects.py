from django.apps import apps as django_apps

CANNED_VIEW = "CANNED"
CANNED_SUPER = "CANNED_SUPER"
CANNED_EXPORT = "CANNED_EXPORT"
CANNED_ROLE = "CANNED_ROLE"
CANNED_SUPER_ROLE = "CANNED_SUPER_ROLE"
canned_view_codenames = ["edc_navbar.nav_canned_views_section"]
for app_config in django_apps.get_app_configs():
    if app_config.name in [
        "canned_views",
    ]:
        for model_cls in app_config.get_models():
            for prefix in ["view"]:
                canned_view_codenames.append(
                    f"{app_config.name}.{prefix}_{model_cls._meta.model_name}"
                )

canned_super_codenames = ["edc_navbar.nav_canned_views_section"]
for app_config in django_apps.get_app_configs():
    if app_config.name in [
        "canned_views",
    ]:
        for model_cls in app_config.get_models():
            for prefix in ["add", "change", "view", "delete"]:
                canned_super_codenames.append(
                    f"{app_config.name}.{prefix}_{model_cls._meta.model_name}"
                )
