# Plugin URLs

Das Search-Plugin registriert folgende URLs in InvenTree:

## Haupt-URLs

Basierend auf dem Plugin-SLUG `"gm-search"` werden die URLs unter `/plugin/gm-search/` registriert:

1. **Hauptseite (Suchoberfläche):**
   - **URL:** `/plugin/gm-search/`
   - **URL-Name:** `plugin:gm-search:index`
   - **View:** `SearchView` (Template-View)
   - **Zugriff:** Benutzer muss eingeloggt sein und `part.view_part` Berechtigung haben

2. **API-Endpunkt (Suchfunktion):**
   - **URL:** `/plugin/gm-search/api/search/`
   - **URL-Name:** `plugin:gm-search:api-search`
   - **View:** `search` (Funktions-View)
   - **Methode:** GET
   - **Parameter:** `q` (Query-String für die Suche)
   - **Zugriff:** Benutzer muss eingeloggt sein und `part.view_part` Berechtigung haben

## Beispiel-URLs

Wenn Ihr InvenTree unter `http://localhost:8000` läuft:

- Hauptseite: `http://localhost:8000/plugin/gm-search/`
- API-Suche: `http://localhost:8000/plugin/gm-search/api/search/?q=Beispiel`

## Navigation

Das Plugin fügt einen Navigationspunkt hinzu:
- **Name:** "Suche"
- **Icon:** `fa-search`
- **Link:** `plugin:gm-search:index` (zeigt auf die Hauptseite)
- **Position:** Topbar und Sidebar

