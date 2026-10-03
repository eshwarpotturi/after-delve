import duckdb, re, collections, pickle
tok=re.compile(r"[a-z][a-z\-']{2,}")
c=duckdb.connect()
q="""SELECT id, split_part(categories,' ',1) AS pc, abstract FROM 'pq/*.parquet'
     WHERE regexp_matches(id,'^[0-9]{4}\\.[0-9]{4,5}$') AND substr(id,1,2) IN ('19','22','25')"""
df=collections.defaultdict(collections.Counter); n=collections.Counter()
for b in c.execute(q).to_arrow_reader(50000):
    for i,pc,a in zip(b.column(0).to_pylist(),b.column(1).to_pylist(),b.column(2).to_pylist()):
        g='tech' if pc.split('.')[0] in('cs','eess') else 'other'; k=(g,i[:2]); n[k]+=1
        df[k].update(set(tok.findall((a or '').lower())))
def test(a,b):
    out=[]
    for w,cnt in df[('tech',b)].items():
        if not re.fullmatch(r"[a-z]{4,}",w): continue
        rt=1e4*cnt/n[('tech',b)]
        if rt<15: continue
        bt=1e4*df[('tech',a)][w]/n[('tech',a)]; ro=1e4*df[('other',b)][w]/n[('other',b)]; bo=1e4*df[('other',a)][w]/n[('other',a)]
        if rt/(bt+0.3)>=3 and ro>=3 and ro/(bo+0.3)>=3: out.append((round(rt/(bt+0.3),1),w))
    return sorted(out,reverse=True)
p=test('19','22'); r=test('22','25')
print("2019->2022 words passing:",len(p),p[:40])
print("2022->2025 words passing:",len(r),[w for _,w in r[:60]])
pickle.dump({"p":p,"r":r},open("placebo.pkl","wb"))
