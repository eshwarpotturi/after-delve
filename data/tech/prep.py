import json
A=json.load(open("agg.json")); mo=A["months"]; T=A["tot"]; N=len(mo)
months=["20"+m[:2]+"-"+m[2:] for m in mo]
W=A["W"]; wave_of={w:k for k,L in enumerate(W) for w in L}
def sm(r,k=3): return [sum(r[max(0,i-k+1):i+1])/len(r[max(0,i-k+1):i+1]) for i in range(len(r))]
words={}
for w,k in wave_of.items():
    r=[1e4*a/t for a,t in zip(A["wc"][w],T)]; b=1e4*sum(A["wc"][w][:48])/sum(T[:48]); s=sm(r)
    words[w]={"r":[round(x,2) for x in s],"b":round(b,2),"w":k}
out={"months":months,"waves":[[round(100*a/t,2) for a,t in zip(A["wave"][k],T)] for k in range(4)],"words":words,"W":W,"total":sum(T)}
FN={"cs":"Computer science","eess":"Electrical engineering","stat":"Statistics","econ":"Economics and finance","qbio":"Quantitative biology","phys":"Physics","math":"Mathematics"}
pct=lambda v:round(100*v[4]/v[0],3)
out["fields"]=sorted([{"n":FN[f],"s22":pct(A["fy"][f+"|22"]),"s25":pct(A["fy"][f+"|25"]),"p25":A["fy"][f+"|25"][0]} for f in FN],key=lambda r:-r["s25"])
SN={"cs.AI":"Artificial intelligence","cs.IR":"Information retrieval","cs.CY":"Computers and society","cs.CV":"Computer vision","cs.CL":"Language processing","cs.SE":"Software engineering","cs.SD":"Sound and audio","cs.CR":"Security","cs.HC":"Human-computer interaction","eess.IV":"Image and video processing","cs.RO":"Robotics","cs.NI":"Networking","cs.LG":"Machine learning","cs.DC":"Distributed computing","eess.SP":"Signal processing","eess.SY":"Systems and control","cs.IT":"Information theory","cs.DS":"Algorithms and data structures"}
subs=[]
for k,v in A["cy"].items():
    pc,y=k.split("|")
    if y=="25" and v[0]>=1500: subs.append({"n":SN[pc],"c":pc,"s22":pct(A["cy"][pc+"|22"]),"s25":pct(v),"p25":v[0]})
out["subs"]=sorted(subs,key=lambda r:-r["s25"])
json.dump(out,open("page_data.json","w"),separators=(",",":"))
import os; print("bytes",os.path.getsize("page_data.json"),"N",N,months[0],months[-1],"idx 2024-04",months.index("2024-04"))
wv=out["waves"]
for k,nm in enumerate(["w1","w2","w3","any"]):
    p=max(range(N),key=lambda i:wv[k][i]); y22=100*sum(A["wave"][k][36:48])/sum(T[36:48])
    print(nm,"2022 %.2f"%y22,"peak",months[p],wv[k][p],"last",wv[k][-1], "apr23",wv[k][months.index("2023-04")], "dec22", wv[k][months.index("2022-12")])
for w in ["delves","intricate","structurally","collapses","survives","reframes","underscoring","underexplored"]:
    x=words[w]; pk=max(range(N),key=lambda i:x["r"][i]); print(w,"base",x["b"],"peak3m",months[pk],x["r"][pk],"x",round(x["r"][pk]/x["b"],1),"last3m",x["r"][-1],"x",round(x["r"][-1]/x["b"],1))
for m in ["2023-06","2024-04","2025-06","2026-09"]:
    i=months.index(m); rk=sorted([(words[w]["r"][i]/words[w]["b"],w) for w in words if words[w]["b"]>=0.3],reverse=True)[:8]
    print(m,[(w,round(x,1)) for x,w in rk])
print([ (w,words[w]["b"]) for w in words if words[w]["b"]<0.3])
print(out["fields"]); 
