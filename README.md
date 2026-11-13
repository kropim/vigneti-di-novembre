# Vigneti di novembre – Rennrad-Webseite

13 Rennradtouren mit OpenStreetMap, mobilfreundlicher Kartenansicht und GPX-Downloads. **Sobald GPX-Dateien im Repository liegen, werden sie für alle Besucher automatisch geladen.** Browser-Cache ist nur eine optionale Zwischenlösung.

## Einmalige Berechnung direkt auf GitHub (empfohlen)

1. Den **Inhalt dieses Pakets inklusive `.github/workflows/routen-berechnen.yml`** ins Root des GitHub-Repositories hochladen. Versteckte Ordner müssen mit hochgeladen werden.
2. Unter **Settings → Pages** die Veröffentlichung von Branch `main` / `/(root)` aktivieren.
3. Unter **Actions** den Workflow **„Rennradrouten berechnen und zur Freigabe vorlegen“** öffnen → **Run workflow** → `tour: 0` → starten.
4. Nach dem Lauf unter **Pull requests** den automatisch erstellten Pull Request öffnen. Die Datei `ROUTENPRUEFUNG.md` zeigt Kilometerabweichungen und offene Prüfungen. Die GPX-Dateien können auch als ZIP-ähnliches Workflow-Artefakt unter **Actions → Lauf → Artifacts** heruntergeladen werden.
5. **Erst nach Prüfung** (Asphalt, Streckenlänge, Höhenmeter, schöne Radwege) den Pull Request **Merge**n. Danach liegen die GPX-Dateien unter `gpx/tour-01.gpx` bis `gpx/tour-13.gpx` auf `main`. Alle Besucher sehen und laden sie direkt, ohne Routing.

### Einmalige GitHub-Einstellung

Falls das automatische Anlegen des Pull Requests mit `GitHub Actions is not permitted to create or approve pull requests` fehlschlägt: Unter **Settings → Actions → General → Workflow permissions** die Berechtigung **Read and write permissions** und **Allow GitHub Actions to create and approve pull requests** aktivieren (sofern die Repository-Einstellungen das erlauben), danach Workflow erneut starten.

## Qualitätsgrenzen

- Routing nutzt den öffentlichen Valhalla-Dienst mit Rennrad-Profil (`bicycle_type: Road`) und Präferenz gegen schlechte Oberflächen und stark befahrene Strassen. Ein externer öffentlicher Dienst kann ausfallen, begrenzt sein oder andere Strecken wählen.
- **Keine automatische Garantie für 100 % Asphalt.** OSM-Daten können fehlen. Jeder Track muss überprüft werden.
- **Höhenmeter werden derzeit nicht automatisch ermittelt.** Die ursprünglichen Soll-Höhenmeter werden im Prüfbericht angegeben, nicht als gemessene Werte ausgegeben.
- Längenabweichungen werden berechnet und im Prüfbericht ausgewiesen, aber nicht automatisch durch ungeprüfte Umwege „korrigiert“.
- Die einmalige Routing-Aktion ist ein **manueller Workflow**. Die Webseite enthält bewusst **keine GitHub-Zugriffstokens** und benötigt für Besucher keinerlei GitHub-Berechtigungen.
- Wenn einzelne Touren fehlschlagen, sind die erfolgreichen GPX-Dateien und der Fehlerbericht im Pull Request zu sehen; die fehlenden Touren können später separat neu gestartet werden.

## Dateien

- `index.html` – Webseite
- `touren.json` – Tourvorgaben und Zwischenorte
- `scripts/generate_routes.py` – Rennrad-Routing und GPX-Erzeugung
- `.github/workflows/routen-berechnen.yml` – GitHub Actions, Berechnung und Pull Request
- `gpx/` – veröffentlichte Tracks nach Freigabe
- `ROUTENPRUEFUNG.md` – wird beim ersten Workflow-Lauf erzeugt
