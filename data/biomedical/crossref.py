import json,urllib.request,time,os
js=json.load(open("journals_top.json"))
out=json.load(open("publishers.json")) if os.path.exists("publishers.json") else {}
for j in js:
    i=j["issn"]
    if i in out: continue
    for k in range(3):
        try:
            req=urllib.request.Request(f"https://api.crossref.org/journals/{i}",headers={"User-Agent":"delve-epidemic-research/0.1"})
            with urllib.request.urlopen(req,timeout=40) as r:
                m=json.load(r)["message"]; out[i]={"publisher":m.get("publisher"),"title":m.get("title")}
            break
        except urllib.error.HTTPError as e:
            if e.code==404: out[i]={"publisher":None,"title":None}; break
            time.sleep(3)
        except Exception as e: time.sleep(3)
    time.sleep(0.15)
json.dump(out,open("publishers.json","w"))
import collections
print(len(out)); print(collections.Counter(v["publisher"] for v in out.values()).most_common(40))
