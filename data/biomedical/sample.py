import json, time, urllib.request, urllib.parse, gzip, os, sys
from concurrent.futures import ThreadPoolExecutor
BASE="https://www.ebi.ac.uk/europepmc/webservices/rest/search"
def fetch(q, cursor="*", size=1000):
    url=BASE+"?"+urllib.parse.urlencode({"query":q,"format":"json","pageSize":size,"resultType":"core","cursorMark":cursor})
    for i in range(5):
        try:
            with urllib.request.urlopen(url,timeout=120) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(3*(i+1))
    return None
def job(args):
    y,m,d=args
    date=f"{y}-{m:02d}-{d:02d}"
    out=[]; cur="*"
    for page in range(2):
        j=fetch(f"HAS_ABSTRACT:y AND SRC:MED AND FIRST_PDATE:{date}",cur)
        if not j: break
        for r in j.get("resultList",{}).get("result",[]):
            ji=r.get("journalInfo",{}).get("journal",{})
            out.append({"id":r.get("id"),"y":y,"m":m,"a":r.get("abstractText",""),"j":ji.get("title"),"issn":ji.get("issn") or ji.get("essn"),
                        "lang":r.get("language")})
        nc=j.get("nextCursorMark")
        if not nc or nc==cur: break
        cur=nc
    return date,out
jobs=[(y,m,d) for y in (2021,2022,2024,2025) for m in range(1,13) for d in (14,) if not os.path.exists(f"sample/{y}-{m:02d}-{d:02d}.json.gz")]
os.makedirs("sample",exist_ok=True)
with ThreadPoolExecutor(4) as ex:
    for date,out in ex.map(job,jobs):
        with gzip.open(f"sample/{date}.json.gz","wt") as f: json.dump(out,f)
        print(date,len(out),flush=True)
