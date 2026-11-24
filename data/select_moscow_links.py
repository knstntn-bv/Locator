import json
from pathlib import Path
p=Path('data/moscow-events.json');d=json.loads(p.read_text(encoding='utf-8'))
links={
2:'https://afisha.timepad.ru/moscow/events/knizhnyy-klub-13-plus-v-poiskah-prikliucheniy-4026774',
3:'https://afisha.timepad.ru/moscow/events/knizhnyy-klub-13-plus-v-poiskah-prikliucheniy-4026774',
5:'https://moscowcss.timepad.ru/event/4291445/',9:'https://t.me/littleproduct/1390',12:'https://moscowjs.timepad.ru/event/4296651/',
17:'https://findquiz.ru/event/60-sek/358458-biznes-liga-bitva-brendov',
18:'https://findquiz.ru/event/60-sek/358459-otkrytaya-liga-dlya-novichkov',
19:'https://moscow.quizplease.ru/game/01a1bf92-c756-73da-a20f-fe42f3aa91fe',
20:'https://iwenty.ru/moskva/event/kviz-pliz-100-hitov-P12c2thc',
21:'https://www.mozgva.com/calendar',
22:'https://msk.quizwhois.ru/games/vselennaya-garri-pottera',
23:'https://squiz.ru/game/msk-tsena-voprosa-9-261203',
24:'https://rudagames.com/moskva/schedule',
25:'https://squiz.ru/game/msk-skviz-miks-12-1',
26:'https://squiz.ru/game/msk-liga-novichkov-237-2',
27:'https://bingo-fm.ru/',
28:'https://msk.quizwhois.ru/games/zakrytie-osennego-sezona-klassika-millenialy',
29:'https://squiz.ru/game/msk-1030-2-261201',
30:'https://squiz.ru/game/msk-puteshestviya-13',
31:'https://msk.quizwhois.ru/games/kinchik-i-muzonchik-2',
32:'https://squiz.ru/game/msk-ugaday-melodiyu-17-1-261203',
33:'https://squiz.ru/game/msk-garri-potter-27-1-261205',
34:'https://rudagames.com/moskva/schedule',35:'https://rudagames.com/moskva/schedule',36:'https://rudagames.com/moskva/schedule',
37:'https://spontanno.space/moscow/games/otkrytye-igry-sotsionicheskoy-mafii--r3jxbhzt',
38:'https://spontanno.space/moscow/games/nastolnye-igry-na-privoze--4brn0c4j',
39:'https://spontanno.space/moscow/games/gorodskaya-mafiya-s-razborami--nfk8c6kd',
40:'https://spontanno.space/moscow/workshops/masterskaya-solenaya-snezhinka--xc7mx70x',
41:'https://svetlovka.timepad.ru/event/4305832/',
42:'https://iwenty.ru/moskva/event/nastolnye-igry-na-angliyskom-ulv8zCUj',
43:'https://spontanno.space/moscow/games/klub-nastolnykh-igr-na-begovoy--psck0n3c',
44:'https://spontanno.space/moscow/games/kviz-kinomuzigra--f5z7f6qf',
45:'https://spontanno.space/moscow/games/igroteka-lev-v-igre--xsnhvcav',
46:'https://spontanno.space/moscow/games/bolshaya-igroteka-igraem-s-nami--qt2psd63',
48:'https://spontanno.space/moscow/games/novogodniy-kinomuzykalnyy-kviz-tayna-poteryannogo-goda--kg7yfes7',
49:'https://morepost.ru/moscow/event/literaturnyi-kviz-156058',
50:'https://extra.hse.ru/announcements/1217575735.html',
51:'https://spontanno.space/moscow/food/art-branch--p1ygfdd1',
52:'https://www.ticketland.ru/doma-kultury/kulturnyy-centr-strogino/master-klass-multfilm/',
53:'https://spontanno.space/moscow/cinema/kinoprosmotr-curovoe-ispytanie-2011--9w8z3f55',
54:'https://spontanno.space/moscow/cinema/kino-bez-barerov-pokaz-samykh-vdokhnovlyayushchikh-korotkometrazhnykh-filmov-o--m9ygjneg',
55:'https://spontanno.space/moscow/cinema/kinoklub-na-angliyskom-yazyke--pjma0hsn',
56:'https://spontanno.space/moscow/workshops/master-klass-yaponskaya-illyustratsiya--amh9p132',
57:'https://spontanno.space/moscow/lectures/lektsiya-iz-tsikla-zhivopis-v-kino-sorrentino--gdj60nea',
58:'https://spontanno.space/moscow/cinema/novye-tikhie-kak-kinoyazyk-opisyvaet-realnost-nulevykh-v-rossii--0bvt7t67',
59:'https://www.ticketland.ru/doma-kultury/kc-brateevo/master-klass-lepka-elochnykh-igrushek/',
60:'https://spontanno.space/moscow/workshops/master-klass-zhivopis-po-motivam-matissa--642f2cpm',
61:'https://spontanno.space/moscow/cinema/kinopokaz-s-obsuzhdeniem-ernst-lyubich-kukla--hy6xsaaz',
62:'https://votkuda.ru/event/masterskaya-novogodnyaya-igrushka-39694/',
63:'https://spontanno.space/moscow/concerts/novogodniy-muzykalnyy-vecher-mne-nuzhno-pet--dk0xdeyq',
64:'https://expoafisha.ru/events/gurman-fest/'
}
audit=[]
for e in d['events']:
 if e.get('latitude') is None:continue
 n=int(e['key'].split('-')[2])
 url=links[n] if n!=1 else 'https://afisha.timepad.ru/moscow/events/yaponskiy-madzhong-dlya-novichkov-i-prodvinutyh-po-sredam-3925662'
 e['sources']=[url]
 kind='schedule' if n in (21,24,27,34,35,36) else 'series' if n in (1,2,3,59) else 'event'
 e['source_selection']={'kind':kind,'searched_on':'2026-11-23','method':'web_search_and_page_links'}
 if n==57:e['source_selection']['note']='Совпадают название и адрес; страница показывает 18.11 вместо даты 09.12 в каталоге. Дату тестовой записи не меняли.'
 if n==1:e['source_selection']['note']='Общая страница серии; даты отдельных сред рассчитаны по указанию пользователя.'
 audit.append({'key':e['key'],'title':e['title'],'url':url,**e['source_selection']})
assert len(audit)==58
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
Path('data/moscow-event-links.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path('data/build_moscow_migration.py');s=p.read_text(encoding='utf-8-sig');s=s.replace("        if sources:\n            details.append('Ссылки из исходной подборки (могут быть общими для нескольких событий):\\n' + '\\n'.join(sources))", "        assert len(sources) == 1, e['key']\n        details.append('Подробнее: ' + sources[0])")
s=s.replace('ODbL. https://www.openstreetmap.org/copyright','ODbL.')
p.write_text(s,encoding='utf-8')
print('Selected one link for each of 58 events')
