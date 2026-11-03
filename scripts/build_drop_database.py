#!/usr/bin/env python3
"""Build the full Codex Calcs drop catalog from Digital Extremes' own PC tables.

Every source is retained, along with BOTH the chance to enter an enemy's
loot table and the conditional chance of that item inside the table.
The browser computes overall odds; mission/relic/bounty chances remain per roll.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

URL = 'https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html'
OUTPUT = Path(__file__).resolve().parents[1] / 'data' / 'drops.json'
DATE = re.compile(r'Last\s+Update\s*:\s*(\d{1,2}\s+\w+\s*,?\s*\d{4})', re.I)
RATE = re.compile(r'^\s*(Very Common|Common|Uncommon|Rare|Very Rare|Ultra Rare|Legendary)\s*\(\s*([\d,.]+)\s*%\s*\)\s*$', re.I)
TABLE = re.compile(r'\b(Mod|Blueprint/Item|Blueprint|Item|Resource|Sigil|Additional Item|Relic)\s+Drop\s+Chance\s*:\s*([\d,.]+)\s*%', re.I)
PERCENT = re.compile(r'^\s*([\d,.]+)\s*%\s*$')
ROTATION = re.compile(r'^Rotation\s+[A-Z0-9]+$', re.I)
SKIP_SOURCE = {'', 'source', 'enemy', 'item', 'chance', 'drop chance', 'n/a'}


def clean(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip()


def as_chance(value):
    try:
        chance = float(str(value).replace(',', ''))
        if 0 < chance <= 100:
            return chance
    except (ValueError, TypeError):
        pass
    return None


def group_for(title):
    t = clean(title).lower().rstrip(':')
    if t in ('missions', 'mission rewards'):
        return 'Missions'
    if t in ('relics', 'relic rewards'):
        return 'Relics'
    if t in ('keys', 'key rewards'):
        return 'Keys'
    if t.startswith('dynamic location reward'):
        return 'Dynamic Rewards'
    if t.startswith('sortie'):
        return 'Sorties'
    if 'bounty reward' in t:
        return 'Bounties'
    if 'drops by source' in t or 'drops by mod' in t or 'drops by item' in t:
        return 'Enemy Drops'
    if t.startswith(('blueprint/part drops', 'additional item drops')):
        return 'Enemy Drops'
    return None


def item_kind(title):
    t = title.lower()
    for token, label in (
        ('resource', 'Resource'), ('blueprint', 'Blueprint/Item'),
        ('sigil', 'Sigil'), ('additional item', 'Additional Item'),
        ('relic drops', 'Relic'), ('mod drops', 'Mod'),
    ):
        if token in t:
            return label
    return 'Item'


def parse_table(group, title, table, subheading=''):
    """Parse source-first, rotation, and nested stage tables.

    Row schema:
      [category, exact source name, rotation/stage, reward, conditional%,
       rarity, table-roll% | null, table kind | '']
    """
    rows = []
    source = ''
    rotation = ''
    stage = ''
    table_roll = None
    kind = item_kind(title) if group == 'Enemy Drops' else ''
    inverted = bool(re.search(r'\bby (?:mod|item)\b', title, re.I))

    for tr in table.find_all('tr'):
        cells = tr.find_all(['th', 'td'], recursive=False)
        if not cells:
            continue
        vals = [clean(c.get_text(' ', strip=True)) for c in cells]
        if not any(vals):
            continue
        first = vals[0]
        last = vals[-1]
        rarity_match = RATE.fullmatch(last)

        if rarity_match:
            chance = as_chance(rarity_match.group(2))
            if chance is None:
                continue
            if inverted:
                # Inverted item-first tables repeat data also in source-first
                # tables; source-first is preferred, so these are ignored by
                # default in convert(). They remain supported for fixtures.
                item, node = source, first
                m = PERCENT.fullmatch(vals[1]) if len(vals) >= 3 else None
                roll = as_chance(m.group(1)) if m else None
            else:
                item = vals[-2] if len(vals) >= 3 else first
                node = source or (subheading if group == 'Dynamic Rewards' else title)
                roll = table_roll if group == 'Enemy Drops' else None
                # Some official sections repeat the source in the reward row.
                if group == 'Enemy Drops' and len(vals) >= 3 and first:
                    node = first
            node, item = clean(node), clean(item)
            if not node or not item or node.lower() in SKIP_SOURCE or item.lower() in SKIP_SOURCE:
                continue
            if group == 'Enemy Drops' and node.lower().startswith(('mod drops', 'resource drops', 'blueprint/part drops')):
                continue
            context = ' · '.join(x for x in (rotation, stage) if x)
            rows.append([group, node, context, item, chance, rarity_match.group(1).title(), roll, kind])
            continue

        joined = ' '.join(vals)
        # The 2-column enemy header looks like:
        # Scyto Raknoid | Resource Drop Chance: 20.00%
        drop_match = TABLE.search(joined)
        if group == 'Enemy Drops' and drop_match and first and first.lower() not in SKIP_SOURCE:
            source = first
            table_roll = as_chance(drop_match.group(2))
            kind = drop_match.group(1).title()
            rotation = stage = ''
            continue
        if not first and len(vals) >= 2 and vals[1].lower().startswith(('stage ', 'final stage')):
            stage = vals[1]
            continue
        if first.lower().startswith(('stage ', 'final stage')):
            stage = first
            continue
        if ROTATION.fullmatch(first):
            rotation = first
            stage = ''
            continue
        # Column headings and separators do not carry source information.
        if first.lower() in ('source', 'item', 'chance', 'drop chance', 'rotation', 'reward'):
            continue
        if first.startswith('---'):
            continue
        if first and (cells[0].name == 'th' or len(vals) == 1 or all(not v for v in vals[1:])):
            source = first
            rotation = stage = ''
            table_roll = None

    return rows


def convert(html):
    if len(html) < 250000 or 'missionRewards' not in html or 'relicRewards' not in html:
        raise ValueError('DE page is unexpectedly small or missing mission/relic sections')
    soup = BeautifulSoup(html, 'html.parser')
    records = []
    groups = set()
    active = None
    section_title = ''

    for heading in soup.find_all(['h2', 'h3', 'h4', 'h5']):
        title = clean(heading.get_text(' ', strip=True)).rstrip(':')
        group = group_for(title)
        if group:
            active, section_title = group, title
        elif heading.name in ('h2', 'h3'):
            # Unknown top-level sections must not inherit a prior category.
            active, section_title = None, ''
        if not active:
            continue
        # There can be many subsections of Dynamic Rewards. A table is owned
        # by the closest heading, not an earlier heading several blocks away.
        following = heading.find_next(['h2', 'h3', 'h4', 'h5', 'table'])
        if not following or following.name != 'table':
            continue
        if active == 'Enemy Drops' and re.search(r'\bby (?:mod|item)\b', section_title, re.I):
            # The inverted tables duplicate the same enemy/item combinations.
            continue
        kind_title = section_title if active == 'Enemy Drops' else title
        section_records = parse_table(active, kind_title, following, title if active == 'Dynamic Rewards' else '')
        if section_records:
            groups.add(active)
            records.extend(section_records)

    # No generically named enemy may be introduced by the parser. Duplicate
    # official rows are retained: they can be distinct slots in a loot table.
    counts = {g: sum(row[0] == g for row in records) for g in groups}
    if len(records) < 10000 or not {'Missions', 'Relics', 'Enemy Drops', 'Bounties'}.issubset(groups):
        raise ValueError(f'Official parser coverage incomplete: {len(records)} rows; {counts}')
    if any(row[1].lower() in SKIP_SOURCE for row in records):
        raise ValueError('Unnamed/generic sources found in extracted records')
    stamp = DATE.search(soup.get_text(' ', strip=True)[:1400])
    return {
        'schema': 2,
        'source': 'Digital Extremes official Warframe PC drop tables',
        'source_url': URL,
        'source_date': stamp.group(1) if stamp else '',
        'source_hash': hashlib.sha256(html.encode()).hexdigest(),
        'coverage': counts,
        'rows': records,
    }


def main():
    with urlopen(Request(URL, headers={'User-Agent': 'CodexCalcsOfficialDropDB/1.1'}), timeout=60) as response:
        html = response.read(40000000).decode('utf-8', 'replace')
    current = convert(html)
    old = json.loads(OUTPUT.read_text(encoding='utf-8')) if OUTPUT.exists() else {}
    if old.get('schema') == current['schema'] and old.get('source_hash') == current['source_hash']:
        print(f'Official tables unchanged ({len(current["rows"])} entries).')
        return
    current['checked_at'] = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    temp = OUTPUT.with_suffix('.tmp')
    temp.write_text(json.dumps(current, ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf-8')
    temp.replace(OUTPUT)
    print(f'Updated {len(current["rows"]):,} detailed records, coverage={current["coverage"]}; DE source: {current["source_date"]}')

if __name__ == '__main__':
    main()
