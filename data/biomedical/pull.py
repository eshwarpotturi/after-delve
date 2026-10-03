import json, time, urllib.request, urllib.parse, os, calendar, threading, sys
from concurrent.futures import ThreadPoolExecutor
BASE="https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CACHE="cache.json"
cache=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
lock=threading.Lock()
def count(q):
    if q in cache: return cache[q]
    url=BASE+"?"+urllib.parse.urlencode({"query":q,"format":"json","pageSize":1,"resultType":"idlist"})
    for i in range(6):
        try:
            with urllib.request.urlopen(url,timeout=60) as r:
                v=json.load(r)["hitCount"]
            with lock: cache[q]=v
            return v
        except Exception as e:
            time.sleep(2*(i+1))
    return None
def save():
    with lock: json.dump(cache,open(CACHE,"w"))
WORDS=["delves","delve","showcasing","intricate","realm","meticulous","garnered","unveiled","pivotal","tapestry","underscores","underscore","underscoring","synthesizes","aligns","aligning","underexplored","leverages","leveraging","transformative","integrates","necessitating","emphasizing","surpassing","outperforming","encompassing","elucidates","fostering","foundational","safeguarding","offering","highlighting","nuanced","multifaceted","notably","crucial","however","therefore","significant","patients"]
MARK=["delves","delve","showcasing","underscores","underscoring","underscore","intricate","realm","synthesizes","aligns","aligning","underexplored","surpassing","leverages","transformative","necessitating","encompassing","elucidates","garnered","meticulous"]
M="("+" OR ".join(f'ABSTRACT:"{w}"' for w in MARK)+")"
B="HAS_ABSTRACT:y AND SRC:MED"
months=[(y,m) for y in range(2019,2027) for m in range(1,13) if (y,m)<=(2026,9)]
def mr(y,m): return f"FIRST_PDATE:[{y}-{m:02d}-01 TO {y}-{m:02d}-{calendar.monthrange(y,m)[1]:02d}]"
COUNTRIES={"China":'AFF:"China"',"United States":'(AFF:"USA" OR AFF:"United States")',"India":'AFF:"India"',"Japan":'AFF:"Japan"',"Germany":'AFF:"Germany"',"United Kingdom":'(AFF:"UK" OR AFF:"United Kingdom")',"Italy":'AFF:"Italy"',"South Korea":'AFF:"Korea"',"Iran":'AFF:"Iran"',"Brazil":'AFF:"Brazil"',"Spain":'AFF:"Spain"',"France":'AFF:"France"',"Canada":'AFF:"Canada"',"Australia":'AFF:"Australia"',"Turkey":'(AFF:"Turkey" OR AFF:"Türkiye" OR AFF:"Turkiye")',"Saudi Arabia":'AFF:"Saudi Arabia"',"Egypt":'AFF:"Egypt"',"Pakistan":'AFF:"Pakistan"',"Netherlands":'AFF:"Netherlands"',"Poland":'AFF:"Poland"',"Taiwan":'AFF:"Taiwan"',"Switzerland":'AFF:"Switzerland"',"Sweden":'AFF:"Sweden"',"Nigeria":'AFF:"Nigeria"',"Ethiopia":'AFF:"Ethiopia"',"Indonesia":'AFF:"Indonesia"',"Malaysia":'AFF:"Malaysia"',"Iraq":'AFF:"Iraq"',"Mexico":'AFF:"Mexico"',"Russia":'AFF:"Russia"'}
CY=[2021,2022,2023,2024,2025,2026]
journals=json.load(open("journals_top.json"))
JY=[2022,2024,2025]
qs=[]
for y,m in months:
    qs.append(f"{B} AND {mr(y,m)}"); qs.append(f"{M} AND {B} AND {mr(y,m)}")
    for w in WORDS: qs.append(f'ABSTRACT:"{w}" AND {B} AND {mr(y,m)}')
for y in range(2015,2027):
    qs.append(f"{B} AND PUB_YEAR:{y}"); qs.append(f"{M} AND {B} AND PUB_YEAR:{y}")
    for w in WORDS: qs.append(f'ABSTRACT:"{w}" AND {B} AND PUB_YEAR:{y}')
for c,f in COUNTRIES.items():
    for y in CY:
        qs.append(f"{f} AND {B} AND PUB_YEAR:{y}"); qs.append(f"{M} AND {f} AND {B} AND PUB_YEAR:{y}")
for j in journals:
    for y in JY:
        qs.append(f'ISSN:"{j["issn"]}" AND {B} AND PUB_YEAR:{y}'); qs.append(f'{M} AND ISSN:"{j["issn"]}" AND {B} AND PUB_YEAR:{y}')
todo=[q for q in qs if q not in cache]
print("queries",len(qs),"todo",len(todo),flush=True)
done=0
with ThreadPoolExecutor(6) as ex:
    for i,_ in enumerate(ex.map(count,todo)):
        if i%300==0: save(); print(i,flush=True)
save(); print("DONE",len(cache),"missing",sum(1 for q in qs if cache.get(q) is None),flush=True)
json.dump({"WORDS":WORDS,"MARK":MARK,"M":M,"B":B,"COUNTRIES":COUNTRIES,"CY":CY,"JY":JY},open("config.json","w"))
