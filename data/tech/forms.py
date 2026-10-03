import duckdb, re, collections
fam={"delve":["delve","delves","delved","delving"],"showcase":["showcase","showcases","showcased","showcasing"],
"underscore":["underscore","underscores","underscored","underscoring"],"advance":["advance","advances","advanced","advancing"],
"persist":["persist","persists","persisted","persisting"],"collapse":["collapse","collapses","collapsed","collapsing"],
"overlook":["overlook","overlooks","overlooked","overlooking"],"reframe":["reframe","reframes","reframed","reframing"]}
allw={w for L in fam.values() for w in L}
tok=re.compile(r"[a-z][a-z\-']{2,}")
c=duckdb.connect()
q="""SELECT id, abstract FROM 'pq/*.parquet' WHERE regexp_matches(id,'^[0-9]{4}\\.[0-9]{4,5}$') AND substr(id,1,2) BETWEEN '19' AND '26'
     AND split_part(split_part(categories,' ',1),'.',1) IN ('cs','eess')"""
n=collections.Counter(); cnt=collections.defaultdict(collections.Counter); famc=collections.defaultdict(collections.Counter)
def per(y): return 'base' if y<=22 else str(y)
for b in c.execute(q).to_arrow_reader(50000):
    for i,a in zip(b.column(0).to_pylist(),b.column(1).to_pylist()):
        p=per(int(i[:2])); n[p]+=1
        s=set(tok.findall((a or '').lower()))&allw
        for w in s: cnt[w][p]+=1
        for f,L in fam.items():
            if s&set(L): famc[f][p]+=1
P=['base','23','24','25','26']
r=lambda d,p: 1e4*d[p]/n[p]
print("per 10,000 tech abstracts:            base   2023   2024   2025   2026   peak/base")
for f,L in fam.items():
    for w in L:
        v=[r(cnt[w],p) for p in P]; print(f"  {w:14s}"+"".join(f"{x:7.1f}" for x in v)+f"   x{max(v[1:])/(v[0]+0.3):5.1f}")
    v=[r(famc[f],p) for p in P]; print(f"= {f.upper()+' family':14s}"+"".join(f"{x:7.1f}" for x in v)+f"   x{max(v[1:])/(v[0]+0.3):5.1f}\n")
