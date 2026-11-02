#!/usr/bin/env python3
"""Build a compact, verified in-game equipment catalog from WFCD/warframe-items.

This script runs in GitHub Actions. No account credentials or visitor data are used.
"""
from __future__ import annotations
import datetime as dt
import json
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGET = ROOT / 'data' / 'loadouts.json'
BASE = 'https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/'
SOURCE_FILES = {
    'warframe': ('Warframes.json',),
    'primary': ('Primary.json',),
    'secondary': ('Secondary.json',),
    'melee': ('Melee.json',),
    'companion': ('Pets.json', 'Sentinels.json'),
    'archgun': ('Arch-Gun.json',),
}
MINIMUM_COUNTS = dict(warframe=50, primary=75, secondary=65, melee=90, companion=12, archgun=10)
EXCLUDE_WORDS = re.compile(r'\b(blueprint|component|chassis|neuroptics|systems|receiver|barrel|stock|link|harness|carapace|research|skin|statue|decoration|glyph|sigil|nog)\b', re.I)



VARIANT_PREFIX = re.compile(r'^(?:MK1[-\s]*|Kuva |Tenet |Coda |Prisma |Telos |Synoid |Rakta |Vaykor |Secura |Sancti |Dex |Carmine |Mara |Mutalist |Proboscis )', re.I)
VARIANT_SUFFIX = re.compile(r'(?: Prime| Vandal| Wraith| Umbra)$', re.I)


def family_name(raw: str, category: str) -> str:
    value = raw.strip()
    if category == 'warframe' and re.fullmatch(r'(?:sirius\s*(?:&|and)\s*orion|orion\s*(?:&|and)\s*sirius|sirius|orion)', value, re.I):
        return 'Sirius & Orion'
    if category == 'warframe' and value.casefold() == 'excalibur umbra':
        return 'Excalibur'
    for _ in range(4):
        earlier = value
        value = VARIANT_SUFFIX.sub('', VARIANT_PREFIX.sub('', value)).strip()
        if earlier == value:
            break
    if category == 'archgun' and value.casefold() == 'dual decurions':
        return 'Dual Decurion'
    return value or raw.strip()


def group_families(rows: list[dict], category: str) -> list[dict]:
    families: dict[str, dict] = {}
    for row in rows:
        name = row['name'].strip()
        root = family_name(name, category)
        key = root.casefold()
        record = families.setdefault(key, {'root': root, 'originals': set(), 'names': set(), 'base': False})
        record['originals'].add(name)
        record['names'].add(name)
        record['names'].update(a for a in row.get('aliases', []) if isinstance(a, str))
        if name.casefold() == key:
            record['base'] = True
    result = []
    for fam in families.values():
        names = fam['names']
        # An otherwise-unrepresented special weapon (such as Kuva Bramma)
        # keeps its real in-game name; variants with a base share that family.
        single = next(iter(fam['originals']))
        special_only = single.startswith(('Kuva ', 'Tenet ', 'Coda '))
        standalone_prime = single.casefold() in {'gotva prime', 'dakra prime', 'reaper prime'}
        label = fam['root'] if fam['base'] or len(names) > 1 or not (special_only or standalone_prime) else single
        result.append({'id': f"family:{category}:{fam['root'].casefold()}",
                       'name': label, 'aliases': sorted((n for n in names if n != label), key=str.casefold)})
    return sorted(result, key=lambda x: x['name'].casefold())


VARIANT_PREFIX = re.compile(r'^(?:MK1[-\s]*|Kuva |Tenet |Coda |Prisma |Telos |Synoid |Rakta |Vaykor |Secura |Sancti |Dex |Carmine |Mara |Mutalist |Proboscis )', re.I)
VARIANT_SUFFIX = re.compile(r'(?: Prime| Vandal| Wraith| Umbra)$', re.I)


def family_name(raw: str, category: str) -> str:
    value = raw.strip()
    if category == 'warframe' and re.fullmatch(r'(?:sirius\s*(?:&|and)\s*orion|orion\s*(?:&|and)\s*sirius|sirius|orion)', value, re.I):
        return 'Sirius & Orion'
    if category == 'warframe' and value.casefold() == 'excalibur umbra':
        return 'Excalibur'
    for _ in range(4):
        earlier = value
        value = VARIANT_SUFFIX.sub('', VARIANT_PREFIX.sub('', value)).strip()
        if earlier == value:
            break
    if category == 'archgun' and value.casefold() == 'dual decurions':
        return 'Dual Decurion'
    return value or raw.strip()


def group_families(rows: list[dict], category: str) -> list[dict]:
    families: dict[str, dict] = {}
    for row in rows:
        name = row['name'].strip()
        root = family_name(name, category)
        key = root.casefold()
        record = families.setdefault(key, {'root': root, 'originals': set(), 'names': set(), 'base': False})
        record['originals'].add(name)
        record['names'].add(name)
        record['names'].update(a for a in row.get('aliases', []) if isinstance(a, str))
        if name.casefold() == key:
            record['base'] = True
    result = []
    for fam in families.values():
        names = fam['names']
        # An otherwise-unrepresented special weapon (such as Kuva Bramma)
        # keeps its real in-game name; variants with a base share that family.
        single = next(iter(fam['originals']))
        special_only = single.startswith(('Kuva ', 'Tenet ', 'Coda '))
        standalone_prime = single.casefold() in {'gotva prime', 'dakra prime', 'reaper prime'}
        label = fam['root'] if fam['base'] or len(names) > 1 or not (special_only or standalone_prime) else single
        result.append({'id': f"family:{category}:{fam['root'].casefold()}",
                       'name': label, 'aliases': sorted((n for n in names if n != label), key=str.casefold)})
    return sorted(result, key=lambda x: x['name'].casefold())

def download_category(filename: str):
    url = BASE + filename
    request = urllib.request.Request(url, headers={'User-Agent': 'Codex-Calcs-Loadout-Catalog/1.0', 'Accept': 'application/json'})
    with urllib.request.urlopen(request, timeout=45) as response:
        if response.status != 200:
            raise RuntimeError(f'{filename}: HTTP {response.status}')
        data = json.load(response)
    if not isinstance(data, list) or not data:
        raise RuntimeError(f'{filename}: missing or invalid JSON list')
    return data


def clean(items: list, key: str, now: dt.date) -> list:
    output = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        name = item.get('name')
        unique_name = item.get('uniqueName')
        if not isinstance(name, str) or not (2 <= len(name) <= 90):
            continue
        if not isinstance(unique_name, str) or not unique_name.startswith('/Lotus/'):
            continue
        if item.get('masterable') is False:
            continue
        if item.get('codexSecret') is True and not item.get('wikiAvailable'):
            continue
        if EXCLUDE_WORDS.search(name):
            continue
        if name.lower() in {'none', 'unknown', 'unarmed', 'fists', 'placeholder'}:
            continue
        if key == 'warframe' and item.get('type') != 'Warframe':
            continue
        # Only already-introduced equipment, not entries from a future release.
        introduced = item.get('introduced') or {}
        release = item.get('releaseDate') or (introduced.get('date') if isinstance(introduced, dict) else None)
        if isinstance(release, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', release):
            try:
                if dt.date.fromisoformat(release) > now:
                    continue
            except ValueError:
                pass
        if key in ('primary', 'secondary', 'melee', 'archgun') and item.get('type') in {'Exalted Weapon', 'Kitgun Component'}:
            continue
        # Exclude blueprint and other non-playable crafting nodes if present in the feed.
        if item.get('category') in {'Resources', 'Skins', 'Components', 'Mods'}:
            continue
        output[unique_name] = {
            'id': unique_name,
            'name': name,
            'prime': bool(item.get('isPrime') or name.endswith(' Prime')),
            'variant': ('Kuva' if name.startswith('Kuva ') else 'Tenet' if name.startswith('Tenet ') else 'Coda' if name.startswith('Coda ') else ''),
        }
    return sorted(output.values(), key=lambda x: (x['name'].casefold(), x['id']))


def main():
    now = dt.datetime.now(dt.timezone.utc)
    all_categories = {}
    for key, files in SOURCE_FILES.items():
        raw = []
        for filename in files:
            fetched = download_category(filename)
            raw.extend(fetched)
        items = group_families(clean(raw, key, now.date()), key)
        if len(items) < MINIMUM_COUNTS[key]:
            raise RuntimeError(f'{key}: suspiciously small result ({len(items)})—refusing to publish')
        all_categories[key] = items
        print(f'{key}: {len(items)}')
    result = {
        'schema': 2,
        'source': 'WFCD/warframe-items',
        'updated_at': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'categories': all_categories,
    }
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n'
    temporary = TARGET.with_suffix('.json.tmp')
    temporary.write_text(text, encoding='utf-8')
    temporary.replace(TARGET)
    print(f'Published {sum(map(len, all_categories.values()))} entries')


if __name__ == '__main__':
    main()
