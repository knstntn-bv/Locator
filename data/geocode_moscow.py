import json, urllib.request, urllib.parse, time
from pathlib import Path
p=Path('data/moscow-events.json'); data=json.loads(p.read_text(encoding='utf-8'))
cache_path=Path('data/moscow-geocoding-results.json')
cache=json.loads(cache_path.read_text(encoding='utf-8')) if cache_path.exists() else {}
aliases={'Новорогожская, 5. Бесплатно. Клуб «Фурин»':'Новорогожская улица, 5','Карманицкий пер., 3Ас4. 2 000 ₽':'Карманицкий переулок, 3А строение 4','Там же. 2 000 ₽':'Карманицкий переулок, 3А строение 4','Школа 21, Вятская, 27с42. Бесплатно':'Вятская улица, 27 строение 42','МТС Банк, пр-т Андропова, 18к1. Бесплатно':'проспект Андропова, 18 корпус 1','Поклонная, 3. Бесплатно':'Поклонная улица, 3'}
aliases.update({'Карманицкий пер., 3Ас4. 2 000 ₽':'Карманицкий переулок, 3Ас4','Там же. 2 000 ₽':'Карманицкий переулок, 3Ас4','Школа 21, Вятская, 27с42. Бесплатно':'Вятская улица, 27с42','МТС Банк, пр-т Андропова, 18к1. Бесплатно':'проспект Андропова, 18к1','Coffeeshop, Новослободская, 23':'Новослободская улица, 23','ВДНХ, павильон №61':'ВДНХ Центросоюз','Библиотека №21, Клары Цеткин, 11к2':'улица Клары Цеткин, 11к2','Пивотека 465, Новоданиловская наб., 4А':'Новоданиловская набережная, 4А','КЦ «Строгино»':'Культурный центр Строгино','КЦ «ЗИЛ»':'Культурный центр ЗИЛ','Фудмолл «ПРИВОЗ», Жулебино':'Привоз Жулебино'})
selected=[e for e in data['events'] if e.get('reported_location') and not e['reported_location'].startswith('Москва') and e['reported_location']!='Место уточняется']
assert len(selected)==58
for e in selected:
 loc=e['reported_location']; query=aliases.get(loc,loc)+' , Москва'
 if query not in cache:
  params=urllib.parse.urlencode(dict(q=query,format='jsonv2',limit=3,addressdetails=1,countrycodes='ru',viewbox='37.0,56.1,38.2,55.1',bounded=1))
  url='https://nominatim.openstreetmap.org/search?'+params
  req=urllib.request.Request(url,headers={'User-Agent':'Locator-test-data-geocoder/1.0','Accept-Language':'ru'})
  try:
   result=json.load(urllib.request.urlopen(req,timeout=25))
  except Exception as exc:
   cache[query]={'url':url,'error':str(exc),'results':[]}; cache_path.write_text(json.dumps(cache,ensure_ascii=False,indent=2),encoding='utf-8'); raise
  cache[query]={'url':url,'results':result}
  cache_path.write_text(json.dumps(cache,ensure_ascii=False,indent=2),encoding='utf-8')
  print(query, '=>',len(result),flush=True); time.sleep(1.1)
 results=cache[query]['results']
 original_results=results
 # Ignore roads, transit stops and unrelated services when selecting a venue.
 if not any(ch.isdigit() for ch in query):
  venues=[r for r in results if r.get('type') in ('restaurant','bar','pub','nightclub','community_centre','arts_centre','theatre')]
  if len(venues)==1: results=venues
 if len(results)>1:
  houses={r.get('address',{}).get('house_number') for r in results}
  latspread=max(float(r['lat']) for r in results)-min(float(r['lat']) for r in results)
  lonspread=max(float(r['lon']) for r in results)-min(float(r['lon']) for r in results)
  if len(houses)==1 and None not in houses and latspread<0.001 and lonspread<0.0015:
   results=[results[0]]
 if len(results)==1 and results[0].get('class') in ('highway','railway','boundary'):
  results=[]
 e['latitude']=None; e['longitude']=None
 e['geocoding']={'provider':'OpenStreetMap Nominatim','query':query,'request_url':cache[query]['url'],'status':'matched' if len(results)==1 else 'ambiguous' if results else 'not_found','attribution':'© OpenStreetMap contributors, ODbL','candidate_count':len(original_results),'selection_method':'single_venue_or_same_address_cluster'}
 if len(results)==1:
  r=results[0]; e['latitude']=float(r['lat']);e['longitude']=float(r['lon']);e['geocoding'].update(display_name=r['display_name'],osm_type=r.get('osm_type'),osm_id=r.get('osm_id'),match_type=r.get('type'))
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
from collections import Counter
print(Counter(e['geocoding']['status'] for e in selected))

