import json, calendar, collections
c=json.load(open("cache.json")); cfg=json.load(open("config.json"))
W=cfg["WORDS"]; M=cfg["M"]; B=cfg["B"]
def mr(y,m): return f"FIRST_PDATE:[{y}-{m:02d}-01 TO {y}-{m:02d}-{calendar.monthrange(y,m)[1]:02d}]"
months=[(y,m) for y in range(2019,2027) for m in range(1,13) if (y,m)<=(2026,9)]
D={"months":[f"{y}-{m:02d}" for y,m in months]}
D["m_total"]=[c[f"{B} AND {mr(y,m)}"] for y,m in months]
D["m_any"]=[c[f"{M} AND {B} AND {mr(y,m)}"] for y,m in months]
D["m_words"]={w:[c[f'ABSTRACT:"{w}" AND {B} AND {mr(y,m)}'] for y,m in months] for w in W}
yrs=list(range(2015,2027)); D["years"]=yrs
D["y_total"]=[c[f"{B} AND PUB_YEAR:{y}"] for y in yrs]
D["y_any"]=[c[f"{M} AND {B} AND PUB_YEAR:{y}"] for y in yrs]
D["y_words"]={w:[c[f'ABSTRACT:"{w}" AND {B} AND PUB_YEAR:{y}'] for y in yrs] for w in W}
D["countries"]={}
for k,f in cfg["COUNTRIES"].items():
    D["countries"][k]={str(y):[c[f"{M} AND {f} AND {B} AND PUB_YEAR:{y}"],c[f"{f} AND {B} AND PUB_YEAR:{y}"]] for y in cfg["CY"]}
pubs=json.load(open("publishers.json"))
def norm(p):
    if not p: return "Other"
    for k,v in [("Elsevier","Elsevier"),("MDPI","MDPI"),("Biomed Central","Springer Nature"),("Springer","Springer Nature"),("Frontiers","Frontiers"),("Wiley","Wiley"),("American Chemical Society","American Chemical Society"),("Royal Society of Chemistry","Royal Society of Chemistry"),("Wolters Kluwer","Wolters Kluwer"),("Dove","Taylor & Francis"),("Taylor & Francis","Taylor & Francis"),("Public Library of Science","PLOS"),("Oxford University Press","Oxford University Press"),("BMJ","BMJ"),("SAGE","SAGE"),("Cureus","Springer Nature")]:
        if k in p: return v
    return "Other"
D["journals"]=[]
for j in json.load(open("journals_top.json")):
    i=j["issn"]; r={"issn":i,"name":j["name"],"pub_raw":pubs.get(i,{}).get("publisher"),"pub":norm(pubs.get(i,{}).get("publisher"))}
    for y in cfg["JY"]:
        r[str(y)]=[c[f'{M} AND ISSN:"{i}" AND {B} AND PUB_YEAR:{y}'],c[f'ISSN:"{i}" AND {B} AND PUB_YEAR:{y}']]
    D["journals"].append(r)
D["MARK"]=cfg["MARK"]; D["WORDS"]=W
json.dump(D,open("data.json","w"))
pct=lambda a,b: 100*a/b if b else float('nan')
print("YEARLY any-marker share %:"); 
for y,a,t in zip(yrs,D["y_any"],D["y_total"]): print(y,t,f"{pct(a,t):.2f}")
print("\nper-word per 10k: 2022, 2023, 2024, 2025, 2026")
for w in W:
    r=[D["y_words"][w][yrs.index(y)]/D["y_total"][yrs.index(y)]*1e4 for y in (2022,2023,2024,2025,2026)]
    print(f"{w:16s}"+" ".join(f"{x:8.1f}" for x in r)+f"   x{r[3]/r[0]:.1f} (25/22)  peak {'2024' if r[2]>r[3] else '2025+'}")
print("\nCOUNTRIES share% 2022 -> 2025 (n 2025)")
rows=[]
for k,v in D["countries"].items():
    rows.append((pct(*v["2025"]),k,pct(*v["2022"]),pct(*v["2024"]),pct(*v["2026"]),v["2025"][1]))
for r in sorted(rows,reverse=True): print(f"{r[1]:16s} 2022 {r[2]:5.2f}  2024 {r[3]:5.2f}  2025 {r[0]:5.2f}  2026 {r[4]:5.2f}  n25 {r[5]}")
print("\nPUBLISHERS (journals in set)")
agg=collections.defaultdict(lambda:[0,0,0,0,0,0,0])
for j in D["journals"]:
    a=agg[j["pub"]]; a[0]+=j["2022"][0];a[1]+=j["2022"][1];a[2]+=j["2025"][0];a[3]+=j["2025"][1];a[4]+=1;a[5]+=j["2024"][0];a[6]+=j["2024"][1]
for k,a in sorted(agg.items(),key=lambda kv:-pct(kv[1][2],kv[1][3])): print(f"{k:28s} journals {a[4]:3d}  2022 {pct(a[0],a[1]):5.2f}  2024 {pct(a[5],a[6]):5.2f}  2025 {pct(a[2],a[3]):5.2f}  n25 {a[3]}")
print("\nTOP JOURNALS 2025 (n>=1500)")
js=[j for j in D["journals"] if j["2025"][1]>=1500 and j["2022"][1]>=300]
print(len(js))
for j in sorted(js,key=lambda j:-pct(*j["2025"]))[:25]: print(f'{pct(*j["2025"]):5.1f}  (2022 {pct(*j["2022"]):4.1f})  n {j["2025"][1]:6d}  {j["pub"]:16s} {j["name"][:50]}')
print("...lowest")
for j in sorted(js,key=lambda j:pct(*j["2025"]))[:12]: print(f'{pct(*j["2025"]):5.1f}  (2022 {pct(*j["2022"]):4.1f})  n {j["2025"][1]:6d}  {j["pub"]:16s} {j["name"][:50]}')
