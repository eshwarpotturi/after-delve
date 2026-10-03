import pickle, collections, json
P=pickle.load(open("pass2.pkl","rb")); words=P["words"]; docs=P["docs"]; wid={w:i for i,w in enumerate(words)}
W1=["delves","delve","showcasing","showcases","meticulously","intricate","intricacies","pivotal","garnered","excels","fostering","groundbreaking","comprehending","advancements","innovative","necessitating","underscores"]
W2=["underscoring","underscore","underexplored","overlooking","overlook","transformative","advancing","nuanced","foundational","paving","groundwork","surpassing","adaptability"]
W3=["reframes","survives","reshapes","collapses","sustains","reformulates","genuinely","obscures","persists","sharply","restores","structurally","exposes","decouples","isolates","reverses","amplifies","weakens","narrows","strengthens","markedly","underpins"]
miss=[w for w in W1+W2+W3 if w not in wid]; print("missing",miss)
S=[set(wid[w] for w in L) for L in (W1,W2,W3)]; U=S[0]|S[1]|S[2]
track=W1+W2+W3+["however"]
tix=[wid[w] for w in track]
def grp(pc):
    a=pc.split('.')[0]
    return {'cs':'cs','eess':'eess','math':'math','stat':'stat','q-bio':'qbio','q-fin':'econ','econ':'econ'}.get(a,'phys')
months=sorted({d[0] for d in docs}); months=[m for m in months if '1901'<=m<='2609']; mi={m:i for i,m in enumerate(months)}
NM=len(months)
tot=[0]*NM; wave=[[0]*NM for _ in range(4)]; wc={w:[0]*NM for w in tix}
fy=collections.defaultdict(lambda:[0,0,0,0,0])   # (field,year)-> n, w1,w2,w3,any
cy=collections.defaultdict(lambda:[0,0,0,0,0])   # (pc,year)
for ym,pc,ws in docs:
    if ym not in mi: continue
    g=grp(pc); y=int(ym[:2]); s=set(ws)
    h=[bool(s&S[0]),bool(s&S[1]),bool(s&S[2])]; a=any(h)
    r=fy[(g,y)]; r[0]+=1; r[1]+=h[0]; r[2]+=h[1]; r[3]+=h[2]; r[4]+=a
    if g in('cs','eess'):
        r=cy[(pc,y)]; r[0]+=1; r[1]+=h[0]; r[2]+=h[1]; r[3]+=h[2]; r[4]+=a
        i=mi[ym]; tot[i]+=1
        for k in range(3): wave[k][i]+=h[k]
        wave[3][i]+=a
        for w in s:
            if w in wc: wc[w][i]+=1
out={"months":months,"tot":tot,"wave":wave,"wc":{words[w]:v for w,v in wc.items()},"fy":{f"{k[0]}|{k[1]}":v for k,v in fy.items()},"cy":{f"{k[0]}|{k[1]}":v for k,v in cy.items()},"W":[W1,W2,W3]}
json.dump(out,open("agg.json","w"))
pct=lambda a,b:100*a/b if b else 0
print("tech abstracts",sum(tot))
print("monthly waves % (tech):")
for i,m in enumerate(months):
    if m>='2206' and (int(m[2:])%2==0 or m>='2601'): print(m,tot[i],*[f"{pct(wave[k][i],tot[i]):5.1f}" for k in range(4)])
print("\nyearly by field: any%  (w1,w2,w3)")
for f in ('cs','eess','stat','econ','qbio','phys','math'):
    print(f, " ".join(f"'{y}:{pct(fy[(f,y)][4],fy[(f,y)][0]):4.1f}({pct(fy[(f,y)][1],fy[(f,y)][0]):.1f},{pct(fy[(f,y)][2],fy[(f,y)][0]):.1f},{pct(fy[(f,y)][3],fy[(f,y)][0]):.1f})" for y in (22,23,24,25,26)))
print("\ncs/eess subfields 2026 (n>=1500): any% 2022 -> 2026, w3 2026")
rows=[(pct(v[4],v[0]),k[0],pct(cy[(k[0],22)][4],cy[(k[0],22)][0]),pct(v[3],v[0]),v[0]) for k,v in cy.items() if k[1]==26 and v[0]>=1500]
for r in sorted(rows,reverse=True): print(f"{r[1]:10s} {r[2]:5.1f} -> {r[0]:5.1f}  w3 {r[3]:5.1f}  n {r[4]}")
