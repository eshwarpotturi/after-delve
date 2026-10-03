import duckdb, re, collections, pickle, time, json
t0=time.time()
P=pickle.load(open("pass1.pkl","rb")); df=P["df"]; n=P["n"]
N=lambda y: n[('cs',y)]+n[('eess',y)]
pre=df[('tech',21)]+df[('tech',22)]; npre=N(21)+N(22)
cand=set()
for y in (24,25,26):
    post=df[('tech',y)]; npost=N(y); rows=[]
    for w,c in post.items():
        if c/npost<0.0015 or not re.fullmatch(r"[a-z]{4,}",w): continue
        rows.append(((c/npost)/((pre.get(w,0)+0.5)/npre),w))
    rows.sort(reverse=True); cand|={w for r,w in rows[:400] if r>=2.5}
BIO=["delves","delve","showcasing","underscores","underscoring","underscore","intricate","realm","synthesizes","aligns","aligning","underexplored","surpassing","leverages","transformative","necessitating","encompassing","elucidates","garnered","meticulous"]
CTRL=["however","therefore","significant","propose","show","results"]
words=sorted(cand|set(BIO)|set(CTRL)); wid={w:i for i,w in enumerate(words)}
print("candidates",len(words))
tok=re.compile(r"[a-z][a-z\-']{2,}")
c=duckdb.connect()
q="""SELECT id, split_part(categories,' ',1) AS pc, abstract FROM 'pq/*.parquet'
     WHERE regexp_matches(id,'^[0-9]{4}\\.[0-9]{4,5}$') AND substr(id,1,2) BETWEEN '19' AND '26'"""
docs=[]
for b in c.execute(q).to_arrow_reader(50000):
    for i,pc,a in zip(b.column(0).to_pylist(),b.column(1).to_pylist(),b.column(2).to_pylist()):
        s=set(tok.findall((a or "").lower()))
        docs.append((i[:4],pc,tuple(sorted(wid[w] for w in s if w in wid))))
pickle.dump({"words":words,"docs":docs,"BIO":BIO,"CTRL":CTRL},open("pass2.pkl","wb"))
print("docs",len(docs),"secs",round(time.time()-t0))
