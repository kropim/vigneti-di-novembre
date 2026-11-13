# GPX-Routing-Prüfbericht

Automatisch berechnet mit Valhalla, Profil `bicycle / Road`, asphaltfreundliche Gewichtung.
**Nicht automatisch freigegeben:** Asphalt, Verkehr, landschaftliche Qualität und Höhenmeter sind vor dem Merge zu prüfen.

| Tour | Vorgabe km | Track km | Abweichung | Höhenmeter | Prüfung |
|---|---:|---:|---:|---|---|
| 01 Nordrunde über Riegel | 69 | 88.6 | +28.5% | Vorgabe 170, **nicht verifiziert** | ⚠️ Länge prüfen |
| 02 Tuniberg-Finale | 70 | 83.4 | +19.1% | Vorgabe 330, **nicht verifiziert** | ⚠️ Länge prüfen |
| 03 Kaiserstuhl-Höhen | 66 | 86.6 | +31.2% | Vorgabe 520, **nicht verifiziert** | ⚠️ Länge prüfen |
| 04 Auggen-Runde | 62 | 62.8 | +1.4% | Vorgabe 450, **nicht verifiziert** | ⚠️ Belag/Hm prüfen |
| 05 Tuniberg und Pfaffenweiler | 61 | 66.4 | +8.8% | Vorgabe 380, **nicht verifiziert** | ⚠️ Belag/Hm prüfen |
| 06 Große Weinstraßen-Runde | 68 | 66.4 | -2.4% | Vorgabe 420, **nicht verifiziert** | ⚠️ Belag/Hm prüfen |
| 07 Route des Vins ab Guebwiller | 52 | 58.4 | +12.4% | Vorgabe 480, **nicht verifiziert** | ⚠️ Länge prüfen |
| 08 Cernay, Thann und Vallée Noble | 58 | 64.0 | +10.3% | Vorgabe 540, **nicht verifiziert** | ⚠️ Länge prüfen |
| 09 Tuniberg und südliche Weinberge | 84 | 88.0 | +4.7% | Vorgabe 480, **nicht verifiziert** | ⚠️ Belag/Hm prüfen |
| 10 Tuniberg, Schwarzwaldrand und Weinstraße | 73 | 79.9 | +9.5% | Vorgabe 450, **nicht verifiziert** | ⚠️ Belag/Hm prüfen |
| 11 Kreuzweg, Sirnitz und Schwärze | 73 | 77.2 | +5.7% | Vorgabe 1050, **nicht verifiziert** | ⚠️ Belag/Hm prüfen |
| 12 Schauinsland über Geiersnest | 62 | 68.3 | +10.2% | Vorgabe 1250, **nicht verifiziert** | ⚠️ Länge prüfen |
| 13 Direkt zum Kaiserstuhl | 67 | 81.5 | +21.6% | Vorgabe 190, **nicht verifiziert** | ⚠️ Länge prüfen |

## Freigabe-Checkliste

- [ ] GPX-Tracks in Komoot/BRouter visuell prüfen; keine ungeeigneten Wege oder Schotter
- [ ] Tatsächliche Höhenmeter mit einem Höhenprofil ermitteln und mit den Vorgaben vergleichen
- [ ] Kilometerabweichungen prüfen und nötigenfalls Zwischenpunkte anpassen
- [ ] Schöne, möglichst getrennte Radwege und verkehrsarme Strassen bevorzugen
- [ ] Erst nach Prüfung Pull Request in `main` übernehmen
