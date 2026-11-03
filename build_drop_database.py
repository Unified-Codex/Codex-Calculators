#!/usr/bin/env python3
"""Parse Digital Extremes' official published Warframe drop tables into site JSON."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup

URL='https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html'
OUTPUT=Path(__file__).resolve().parents[1]/'data'/'drops.json'
RATE=re.compile(r'([\w -]+)\s*\(\s*([\d,.]+)\s*%\s*\)',re.I)
DATE=re.compile(r'Last\s+Update\s*:\s*(\d{1,2}\s+\w+\s*,?\s*\d{4})',re.I)
TABLE=re.compile(r'(?:Mod|Item|Blueprint/Item|Resource|Sigil|Relic|Additional Item)\s+Drop\s+Chance\s*:\s*([\d,.]+)\s*%',re.I)

def clean(s):return re.sub(r'\s+',' ',s or '').strip()
def section(t):
 t=t.lower()
 if t.startswith('mission'):return 'Missions'
 if t.startswith('relic') and 'drop' not in t:return 'Relics'
 if t.startswith('key'):return 'Keys'
 if t.startswith('dynamic'):return 'Dynamic Rewards'
 if 'sortie' in t:return 'Sorties'
 if 'bounty' in t:return 'Bounties'
 if any(s in t for s in ['mod drops','blueprint','resource drops','sigil drops','additional item','relic drops']):return 'Enemy Drops'
 return t.title()[:48]

def parse_table(category,title,table):
 rows=[];source='';rotation='';stage='';roll=None
 inverted=bool(re.search(r'\b(by mod|by blueprint/item|by blueprint|by resource)\b',title,re.I))
 for tr in table.find_all('tr'):
  cs=tr.find_all(['th','td'],recursive=False)
  if not cs:continue
  vals=[clean(c.get_text(' ',strip=True)) for c in cs]
  if not any(vals):continue
  m=RATE.search(vals[-1]);rarity=clean(m.group(1)) if m else ''
  if not m or rarity.lower() not in ['very common','common','uncommon','rare','very rare','ultra rare','legendary']:
   header=TABLE.search(' '.join(vals))
   if header and vals[0]:
    source=vals[0];roll=float(header.group(1).replace(',',''));rotation=stage='';continue
   first=vals[0]
   if first.lower() in ['source','item','chance','drop chance'] or first.startswith('---'):continue
   if re.fullmatch('Rotation\\s+\\w+',first,re.I):rotation=first;stage='';continue
   if len(vals)>1 and not first and vals[1].lower().startswith(('stage ','final stage')):stage=vals[1];continue
   if first.lower().startswith(('stage ','final stage')):stage=first;continue
   if (cs[0].name=='th' or len(vals)==1) and first:
    source=first;rotation=stage='';roll=None
   continue
  chance=float(m.group(2).replace(',',''))
  if not (0<chance<=100):continue
  if inverted:
   item=source;node=vals[0]
   other=re.search(r'([\d,.]+)\s*%',vals[1]) if len(vals)>=3 else None
   tableChance=float(other.group(1).replace(',','')) if other else None
  else:
   item=vals[-2] if len(vals)>=3 else vals[0]
   node=source or title;tableChance=roll
  if not node or not item or item.lower() in ['source','item','rotation']:continue
  rows.append([category,node,' · '.join(p for p in [rotation,stage] if p),item,chance,rarity.title(),tableChance])
 return rows

def convert(html):
 if len(html)<250000 or 'missionRewards' not in html or 'relicRewards' not in html:raise ValueError('Official HTML unexpectedly small or missing key sections')
 soup=BeautifulSoup(html,'html.parser');rows=[];groups=set()
 for h in soup.find_all(['h2','h3']):
  identifier=h.get('id') or ''
  if not identifier or not ('rewards' in identifier.lower() or any(x in identifier.lower() for x in ['avatar','drops','location','relic','mod'])):continue
  table=h.find_next_sibling('table')
  if table is None:continue
  title=clean(h.get_text(' ',strip=True)).rstrip(':');group=section(title)
  got=parse_table(group,title,table)
  if got:rows.extend(got);groups.add(group)
 seen=set();out=[]
 for row in rows:
  identity=json.dumps(row,ensure_ascii=False,separators=(',',':'))
  if identity not in seen:seen.add(identity);out.append(row)
 if len(out)<10000 or not {'Missions','Relics','Enemy Drops'}.issubset(groups):raise ValueError(f'Parser validation failed: {len(out)} rows; sections={sorted(groups)}')
 stamp=DATE.search(soup.get_text(' ',strip=True)[:1100]);return {'schema':1,'source':'Digital Extremes official Warframe PC drop tables','source_url':URL,'source_date':stamp.group(1) if stamp else '','source_hash':hashlib.sha256(html.encode()).hexdigest(),'rows':out}

def main():
 with urlopen(Request(URL,headers={'User-Agent':'CodexCalcsOfficialDropDB/1.0'}),timeout=60) as response:html=response.read(40000000).decode('utf-8','replace')
 current=convert(html)
 old=json.loads(OUTPUT.read_text(encoding='utf-8')) if OUTPUT.exists() else {}
 if old.get('source_hash')==current['source_hash']:
  print(f'No changes to DE official tables ({len(current["rows"])} entries).');return
 current['checked_at']=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
 tmp=OUTPUT.with_suffix('.tmp');tmp.write_text(json.dumps(current,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8');tmp.replace(OUTPUT)
 print(f'Updated {len(current["rows"]):,} official drop records — DE update: {current["source_date"]}')
if __name__=='__main__':main()
