#!/usr/bin/env python3
"""Generate reviewable, road-following GPX tracks from Valhalla; never invent geometry."""
import argparse
import json
import math
import os
from pathlib import Path
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get('VALHALLA_URL', 'https://valhalla1.openstreetmap.de').rstrip('/')


def decode_polyline(encoded, precision=6):
    result = []
    lat = lon = i = 0
    while i < len(encoded):
        nums = []
        for _ in range(2):
            value = shift = 0
            while True:
                if i >= len(encoded):
                    raise ValueError('Ungültige Polyline')
                b = ord(encoded[i]) - 63
                i += 1
                value |= (b & 31) << shift
                shift += 5
                if b < 32:
                    break
            nums.append((value >> 1) ^ (-(value & 1)))
        lat += nums[0]
        lon += nums[1]
        result.append((lat / (10 ** precision), lon / (10 ** precision)))
    return result


def distance_km(points):
    total = 0.0
    for (a, b), (c, d) in zip(points, points[1:]):
        r1, r2 = math.radians(a), math.radians(c)
        x = math.sin((r2-r1)/2)**2 + math.cos(r1)*math.cos(r2)*math.sin(math.radians(d-b)/2)**2
        total += 6371.0088 * 2 * math.asin(min(1, math.sqrt(x)))
    return total


def fetch_segment(start, end, attempts=3):
    req = {'locations': [{'lat': start[0], 'lon': start[1]}, {'lat': end[0], 'lon': end[1]}],
           'costing': 'bicycle',
           'costing_options': {'bicycle': {'bicycle_type': 'Road', 'use_roads': 0.15,
                                           'use_hills': 0.45, 'avoid_bad_surfaces': 1}},
           'directions_options': {'units': 'kilometers'}}
    url = BASE + '/route?json=' + urllib.parse.quote(json.dumps(req, separators=(',', ':')))
    last = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'VignetiRoadCycling/1.0'}), timeout=50) as response:
                data = json.load(response)
            legs = data.get('trip', {}).get('legs', [])
            if not legs or not legs[0].get('shape'):
                raise ValueError('Routingantwort ohne Strassenverlauf: ' + str(data.get('error', '')))
            pts = decode_polyline(legs[0]['shape'])
            if len(pts) < 2:
                raise ValueError('Unvollständiger Routenabschnitt')
            return pts
        except Exception as exc:
            last = exc
            if attempt < attempts-1:
                time.sleep(2 * (attempt+1))
    raise RuntimeError(str(last))


def gpx_xml(tour, places, points):
    ns = 'http://www.topografix.com/GPX/1/1'
    ET.register_namespace('', ns)
    gpx = ET.Element(f'{{{ns}}}gpx', {'version': '1.1', 'creator': 'Vigneti di novembre – Valhalla Rennrad-Routing'})
    metadata = ET.SubElement(gpx, f'{{{ns}}}metadata')
    ET.SubElement(metadata, f'{{{ns}}}name').text = tour['name']
    for place_key in tour['via']:
        lat, lon, name = places[place_key]
        ET.SubElement(ET.SubElement(gpx, f'{{{ns}}}wpt', {'lat': str(lat), 'lon': str(lon)}), f'{{{ns}}}name').text = name
    trk = ET.SubElement(gpx, f'{{{ns}}}trk')
    ET.SubElement(trk, f'{{{ns}}}name').text = tour['name']
    seg = ET.SubElement(trk, f'{{{ns}}}trkseg')
    for lat, lon in points:
        ET.SubElement(seg, f'{{{ns}}}trkpt', {'lat': f'{lat:.6f}', 'lon': f'{lon:.6f}'})
    return ET.tostring(gpx, encoding='utf-8', xml_declaration=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tour', type=int, default=0, help='0 = alle 13')
    parser.add_argument('--max-deviation-pct', type=float, default=10)
    args = parser.parse_args()
    db = json.loads((ROOT/'touren.json').read_text(encoding='utf-8'))
    tours = [t for t in db['tours'] if not args.tour or t['id'] == args.tour]
    if not tours:
        raise SystemExit('Unbekannte Tour')
    (ROOT/'gpx').mkdir(exist_ok=True)
    report = ['# GPX-Routing-Prüfbericht', '',
              'Automatisch berechnet mit Valhalla, Profil `bicycle / Road`, asphaltfreundliche Gewichtung.',
              '**Nicht automatisch freigegeben:** Asphalt, Verkehr, landschaftliche Qualität und Höhenmeter sind vor dem Merge zu prüfen.', '',
              '| Tour | Vorgabe km | Track km | Abweichung | Höhenmeter | Prüfung |',
              '|---|---:|---:|---:|---|---|']
    failures = []
    for t in tours:
        print(f"Tour {t['id']:02}: {t['name']}", flush=True)
        pts = []
        try:
            via = [db['places'][k] for k in t['via']]
            for idx, (a, b) in enumerate(zip(via, via[1:]), 1):
                segment = fetch_segment(a, b)
                if pts:
                    segment = segment[1:]
                pts.extend(segment)
                print(f'  Abschnitt {idx}/{len(via)-1}: {len(segment)} Punkte', flush=True)
                time.sleep(0.35)
            if len(pts) < 20:
                raise ValueError('Zu wenige Trackpunkte')
            km = distance_km(pts)
            deviation = (km / t['km'] - 1) * 100
            status = '⚠️ Länge prüfen' if abs(deviation) > args.max_deviation_pct else '⚠️ Belag/Hm prüfen'
            path = ROOT/'gpx'/f"tour-{t['id']:02}.gpx"
            path.write_bytes(gpx_xml(t, db['places'], pts))
            report.append(f"| {t['id']:02} {t['name']} | {t['km']} | {km:.1f} | {deviation:+.1f}% | Vorgabe {t['hm']}, **nicht verifiziert** | {status} |")
            print(f'  {km:.1f} km / Ziel {t["km"]} km, {deviation:+.1f}%', flush=True)
        except Exception as exc:
            failures.append(t['id'])
            report.append(f"| {t['id']:02} {t['name']} | {t['km']} | — | — | — | ❌ Routingfehler: {str(exc).replace('|', '/')} |")
            print(f'  FEHLER: {exc}', flush=True)
    report += ['', '## Freigabe-Checkliste', '',
               '- [ ] GPX-Tracks in Komoot/BRouter visuell prüfen; keine ungeeigneten Wege oder Schotter',
               '- [ ] Tatsächliche Höhenmeter mit einem Höhenprofil ermitteln und mit den Vorgaben vergleichen',
               '- [ ] Kilometerabweichungen prüfen und nötigenfalls Zwischenpunkte anpassen',
               '- [ ] Schöne, möglichst getrennte Radwege und verkehrsarme Strassen bevorzugen',
               '- [ ] Erst nach Prüfung Pull Request in `main` übernehmen', '']
    (ROOT/'ROUTENPRUEFUNG.md').write_text('\n'.join(report), encoding='utf-8')
    if failures:
        print('Nicht berechnete Touren: ' + ', '.join(map(str, failures)), flush=True)
        # Keep the report and any successful GPX files; workflow creates a PR for review.

if __name__ == '__main__':
    main()
