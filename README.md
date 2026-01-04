# ch.grischamedia.inventree.search

InvenTree Plugin für **erweiterte Suchfunktionen** in InvenTree.

## Funktion

Das Plugin stellt eine erweiterte Suchseite bereit unter: **`/plugin/search/`** (Trailing Slash wichtig)

Auf dieser Seite können Sie nach Teilen (Parts) suchen:

* **Name** - Suche im Teilnamen
* **Beschreibung** - Suche in der Beschreibung
* **IPN** - Suche nach IPN (Internal Part Number)

### Features

* Echtzeit-Suche mit automatischer Aktualisierung (300ms Debounce)
* Suche in mehreren Feldern gleichzeitig (Name, Beschreibung, IPN)
* Anzeige von Kategorie und IPN in den Suchergebnissen
* Direkte Links zu den gefundenen Teilen
* Moderne, benutzerfreundliche Oberfläche

## Plugin Settings

* **ENABLE_ADVANCED_SEARCH**: Aktiviert erweiterte Suchfunktionen (Standard: aktiviert)

## Installation (Development)

Im gleichen Python-Environment wie dein InvenTree-Server:

```bash
pip install -e .
```

Danach InvenTree neu starten und im Admin unter **Plugin Settings** aktivieren.

## Installation (Production / Docker / Portainer)

Voraussetzung:

* In InvenTree ist **Plugin Support** aktiv
* In der Server-Konfiguration ist **ENABLE_PLUGINS_URL** aktiv, damit `/plugin/...` erreichbar ist

### Variante A: Installation über InvenTree UI

* In InvenTree als Admin: **Settings → Plugin Settings**
* Plugin installieren (z.B. via Git URL oder Paketname)
* **Server & Worker neu starten**

### Variante B: Installation per `plugins.txt`

InvenTree kann Plugins beim Start automatisch installieren, wenn **Check Plugins on Startup** aktiv ist.

1. In deinem InvenTree Config-Verzeichnis eine `plugins.txt` anlegen/erweitern (Pfad abhängig von deiner Installation)
2. Eintrag hinzufügen (Beispiele):  
   * VCS-Install (latest): `git+https://github.com/grischamedia/ch.grischamedia.inventree.search.git@master`  
   * Pin auf Tag/Commit: `git+https://github.com/grischamedia/ch.grischamedia.inventree.search.git@<tag-oder-commit>`
3. Container neu starten

### Portainer (Stack)

Allgemeines Vorgehen (abhängig von deinem InvenTree Stack):

1. **plugins.txt persistieren** (Volume/Bind-Mount), damit sie Container-Neustarts überlebt
2. In Portainer: Stack → **Editor** → bei `inventree-server` und `inventree-worker` sicherstellen:  
   * gleiches Plugin-Install-Verhalten (beide brauchen Plugin verfügbar)  
   * nach Änderung: **Re-deploy**
3. In InvenTree UI: **Check Plugins on Startup** aktivieren
4. Danach Plugin in **Plugin Settings** aktivieren und beide Services neu starten

#### Beispiel für Portainer Stack (docker-compose.yml)

```yaml
services:
  inventree-server:
    volumes:
      - ./plugins.txt:/data/plugins.txt
    environment:
      - INVENTREE_PLUGINS_ENABLED=true
      - INVENTREE_PLUGINS_FILE=/data/plugins.txt

  inventree-worker:
    volumes:
      - ./plugins.txt:/data/plugins.txt
    environment:
      - INVENTREE_PLUGINS_ENABLED=true
      - INVENTREE_PLUGINS_FILE=/data/plugins.txt
```

In der `plugins.txt`:

```
git+https://github.com/grischamedia/ch.grischamedia.inventree.search.git@master
```

## Nutzung

Öffne die Seite:

* `https://<dein-host>/plugin/search/`

**Verwendung:**

* Geben Sie einen Suchbegriff in das Suchfeld ein
* Die Suche startet automatisch nach 300ms Pause
* Oder drücken Sie Enter für eine sofortige Suche
* Klicken Sie auf ein Ergebnis, um zum entsprechenden Teil zu gelangen

## API-Endpunkt

Das Plugin stellt auch einen API-Endpunkt bereit:

* **URL:** `/plugin/search/api/search/`
* **Methode:** GET
* **Parameter:** `q` (Suchbegriff)
* **Rückgabe:** JSON mit Suchergebnissen

**Beispiel:**
```
GET /plugin/search/api/search/?q=Beispiel
```

**Antwort:**
```json
{
  "results": [
    {
      "type": "part",
      "id": 123,
      "name": "Beispiel Teil",
      "description": "Beschreibung...",
      "ipn": "IPN123",
      "url": "/part/123/",
      "category": "Kategorie Name"
    }
  ]
}
```

## Beispiel: pip install direkt von GitHub (master)

```bash
pip install --no-cache-dir git+https://github.com/grischamedia/ch.grischamedia.inventree.search.git@master
```

## Autor

GrischaMedia.ch

## Lizenz

MIT

