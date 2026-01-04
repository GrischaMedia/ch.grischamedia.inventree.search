from django.utils.translation import gettext_lazy as _

from plugin import InvenTreePlugin
from plugin.mixins import NavigationMixin, SettingsMixin, UrlsMixin


class SearchPlugin(UrlsMixin, NavigationMixin, SettingsMixin, InvenTreePlugin):
    """Enhanced search functionality for InvenTree."""

    NAME = "Suche"
    SLUG = "search"
    TITLE = _("Suche")
    DESCRIPTION = _("Erweiterte Suchfunktionen für InvenTree")
    AUTHOR = "GrischaMedia.ch"
    PUBLISHED_DATE = "2025-01-01"
    VERSION = "0.0.1"
    WEBSITE = "https://github.com/grischamedia/ch.grischamedia.inventree.search"
    LICENSE = "MIT"
    PUBLIC = True

    MIN_VERSION = "1.1.18"

    SETTINGS = {
        "ENABLE_ADVANCED_SEARCH": {
            "name": "Erweiterte Suche aktivieren",
            "description": "Wenn aktiviert, sind erweiterte Suchfunktionen verfügbar",
            "validator": bool,
            "default": True,
        },
    }

    NAVIGATION = [
        {
            "name": _("Suche"),
            "link": "plugin:search:index",
            "icon": "fa-search",
            "roles": ["topbar", "sidebar"],
        }
    ]

    def setup_urls(self):
        from . import urls

        return urls.urlpatterns

