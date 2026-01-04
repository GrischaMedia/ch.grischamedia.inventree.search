from django.utils.translation import gettext_lazy as _

from plugin import InvenTreePlugin
from plugin.mixins import NavigationMixin, SettingsMixin, UrlsMixin


class SearchPlugin(UrlsMixin, NavigationMixin, SettingsMixin, InvenTreePlugin):
    """Enhanced search functionality for InvenTree."""

    NAME = "Suche"
    SLUG = "gm-search"
    TITLE = _("Suche")
    DESCRIPTION = _("Erweiterte Suchfunktionen für InvenTree")
    AUTHOR = "GrischaMedia.ch"
    PUBLISHED_DATE = "2025-01-01"
    VERSION = "1.0.0"
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
        "HEADER_TITLE": {
            "name": "Header Titel",
            "description": "Titel der in der Kopfzeile der Suchseite angezeigt wird (ohne 'InvenTree')",
            "validator": str,
            "default": "Suche",
        },
        "CARD_TITLE": {
            "name": "Karten Titel",
            "description": "Titel der in der Karte (Box) über dem Suchfeld angezeigt wird",
            "validator": str,
            "default": "Suche",
        },
        "CARD_SUBTITLE": {
            "name": "Karten Untertitel",
            "description": "Untertitel der in der Karte (Box) unter dem Titel angezeigt wird",
            "validator": str,
            "default": "Artikel, Stückzahl & Standortsuche",
        },
    }

    NAVIGATION = [
        {
            "name": _("Suche"),
            "link": "plugin:gm-search:index",
            "icon": "fa-search",
            "roles": ["topbar", "sidebar"],
        }
    ]

    def setup_urls(self):
        from . import urls

        return urls.urlpatterns

