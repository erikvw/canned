from django.conf import settings
from edc_navbar import Navbar, NavbarItem, site_navbars

no_url_namespace = True if settings.APP_NAME == "canned_views" else False

navbar_item = NavbarItem(
    name="canned_views_home",
    title="Monitoring Reports",
    label="MR",
    codename="edc_navbar.canned_views_section",
    url_name="canned_views:home_url",
    no_url_namespace=no_url_namespace,
)

canned_views_navbar = Navbar(name="canned_views")
canned_views_navbar.append_item(navbar_item)

site_navbars.register(canned_views_navbar)