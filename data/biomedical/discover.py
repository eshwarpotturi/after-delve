import gzip,json,glob,re,collections,math,sys
tok=re.compile(r"[a-z][a-z\-']{2,}")
def load(years):
    df=collections.Counter(); n=0
    for f in sorted(glob.glob("sample/*.gz")):
        y=int(f.split("/")[1][:4])
        if y not in years: continue
        for r in json.load(gzip.open(f)):
            a=r.get("a") or ""
            if len(a)<200: continue
            n+=1
            for w in set(tok.findall(a.lower())): df[w]+=1
    return df,n
pre,npre=load({2021,2022}); 
for post_years in ({2024},{2025}):
    post,npost=load(post_years)
    if npost==0: continue
    print("PRE n",npre,"POST",post_years,"n",npost)
    rows=[]
    for w,c in post.items():
        if c<40: continue
        p1=(pre.get(w,0)+0.5)/npre; p2=c/npost
        rows.append((p2/p1,w,pre.get(w,0)/npre*1e4,p2*1e4,(p2-p1)*1e4))
    rows.sort(reverse=True)
    for r in rows[:70]: print(f"{r[1]:18s} x{r[0]:6.1f}  pre {r[2]:7.1f}  post {r[3]:7.1f}  gap {r[4]:7.1f}")
