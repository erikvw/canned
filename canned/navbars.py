from django.conf import settings
from edc_navbar import Navbar, site_navbars

# from meta_dashboard.navbars import navbar as meta_dashboard_navbar

navbar = Navbar(name=settings.APP_NAME)

# navbar.append_item(
#     [item for item in canned_dashboard_navbar.items if item.name == "screened_subject"][
#         0
#     ]
# )

site_navbars.register(navbar)
