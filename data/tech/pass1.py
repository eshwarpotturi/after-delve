import duckdb, re, collections, pickle, time
t0=time.time()
c=duckdb.connect()
q="""SELECT id, split_part(categories,' ',1) AS pc, abstract FROM 'pq/*.parquet'
     WHERE regexp_matches(id,'^[0-9]{4}\\.[0-9]{4,5}$') AND substr(id,1,2) BETWEEN '19' AND '26'"""
tok=re.compile(r"[a-z][a-z\-']{2,}")
def grp(pc):
    a=pc.split('.')[0]
    if a=='cs': return 'cs'
    if a=='eess': return 'eess'
    if a=='math' : return 'math'
    if a=='stat': return 'stat'
    if a in('q-bio',): return 'qbio'
    if a in('q-fin','econ'): return 'econ'
    return 'phys'
df={}  # (group, year) -> Counter
n=collections.Counter(); nm=collections.Counter(); cats=collections.Counter()
rdr=c.execute(q).fetch_record_batch(50000)
for b in rdr:
    ids=b.column(0).to_pylist(); pcs=b.column(1).to_pylist(); abss=b.column(2).to_pylist()
    for i,pc,a in zip(ids,pcs,abss):
        y=int(i[:2]); g=grp(pc); tech=g in('cs','eess')
        n[(g,y)]+=1; nm[(g,i[:4])]+=1; cats[(pc,y)]+=1
        if tech and y in(21,22,24,25,26) and a:
            k=('tech',y)
            if k not in df: df[k]=collections.Counter()
            df[k].update(set(tok.findall(a.lower())))
pickle.dump({"df":df,"n":n,"nm":nm,"cats":cats},open("pass1.pkl","wb"))
print("secs",round(time.time()-t0))
for y in range(19,27): print(y,{g:n[(g,y)] for g in('cs','eess','stat','math','phys','qbio','econ')})
