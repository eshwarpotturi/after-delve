import json, re, collections
D=json.load(open("data.json"))
mo=D["months"]; T=D["m_total"]
CTRL=["however","therefore","significant","patients"]
style=[w for w in D["WORDS"] if w not in CTRL]
def rate(w): return [1e4*a/t for a,t in zip(D["m_words"][w],T)]
bi=[i for i,m in enumerate(mo) if m<="2022-12"]
def base(w): return sum(D["m_words"][w][i] for i in bi)/sum(T[i] for i in bi)*1e4
def smooth(r,k=3): return [sum(r[max(0,i-k+1):i+1])/len(r[max(0,i-k+1):i+1]) for i in range(len(r))]
words={}
for w in style+CTRL:
    r=rate(w); s=smooth(r); b=base(w)
    pk=max(range(len(s)),key=lambda i:s[i])
    last=sum(D["m_words"][w][-6:])/sum(T[-6:])*1e4
    words[w]={"r":[round(x,2) for x in s],"b":round(b,2),"peak":mo[pk],"peakv":round(s[pk],1),"last":round(last,1),"ctrl":w in CTRL,
              "faded": last<0.6*s[pk]}
anyshare=[round(100*a/t,3) for a,t in zip(D["m_any"],T)]
out={"months":mo,"any":anyshare,"words":words,"mark":D["MARK"],"total":sum(T)}
pct=lambda a,b:round(100*a/b,2)
out["countries"]=sorted([{"n":k,"s22":pct(*v["2022"]),"s24":pct(*v["2024"]),"s25":pct(*v["2025"]),"p25":v["2025"][1]} for k,v in D["countries"].items()],key=lambda r:-r["s25"])
agg=collections.defaultdict(lambda:[0,0,0,0,0])
for j in D["journals"]:
    a=agg[j["pub"]]; a[0]+=j["2022"][0];a[1]+=j["2022"][1];a[2]+=j["2025"][0];a[3]+=j["2025"][1];a[4]+=1
out["publishers"]=sorted([{"n":k,"s22":pct(a[0],a[1]),"s25":pct(a[2],a[3]),"p25":a[3],"j":a[4]} for k,a in agg.items() if k!="Other" and a[3]>=15000],key=lambda r:-r["s25"])
def clean(n):
    n=re.sub(r"\s*\(.*?\)","",n); n=re.sub(r"\s*:.*$","",n).strip()
    return n[0].upper()+n[1:]
out["journals"]=sorted([{"n":clean(j["name"]),"p":j["pub"],"s22":pct(*j["2022"]),"s25":pct(*j["2025"]),"p25":j["2025"][1]} for j in D["journals"] if j["2025"][1]>=1500 and j["2022"][1]>=300],key=lambda r:-r["s25"])
json.dump(out,open("page_data.json","w"),separators=(",",":"))
import os; print("bytes",os.path.getsize("page_data.json"))
print("total abstracts",out["total"], "journals",len(out["journals"]), "papers25 in journals", sum(j["p25"] for j in out["journals"]))
a=anyshare; pk=max(range(len(a)),key=lambda i:a[i]); print("any peak",mo[pk],a[pk],"2022 mean",sum(D["m_any"][i] for i,m in enumerate(mo) if m[:4]=="2022")/sum(T[i] for i,m in enumerate(mo) if m[:4]=="2022")*100,"last",mo[-1],a[-1])
yi=D["years"].index(2025); print("2025 any count",D["y_any"][yi],D["y_total"][yi])
for w in ["delves","intricate","realm","showcasing","unveiled","underscoring","synthesizes","integrates","underexplored","outperforming","however"]:
    x=words[w]; print(w,"base",x["b"],"peak",x["peak"],x["peakv"],"last6",x["last"],"faded",x["faded"], "raw peak", max(rate(w)), "sep26", round(rate(w)[-1],1))
print("faded:",[w for w in style if words[w]["faded"]])
print("rising/steady:",[w for w in style if not words[w]["faded"]])
# race check
for m in ["2023-06","2024-04","2025-06","2026-09"]:
    i=mo.index(m); rk=sorted([(words[w]["r"][i]/words[w]["b"],w) for w in style if words[w]["b"]>=0.5],reverse=True)[:8]
    print(m,[(w,round(x,1)) for x,w in rk])
print(out["publishers"])
