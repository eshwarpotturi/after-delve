import pickle, collections
P=pickle.load(open("pass2.pkl","rb")); words=P["words"]; docs=P["docs"]
def grp(pc):
    a=pc.split('.')[0]
    return 'tech' if a in('cs','eess') else 'other'
cnt=collections.defaultdict(lambda: collections.Counter()); tot=collections.Counter()
for ym,pc,ws in docs:
    k=(grp(pc),int(ym[:2])); tot[k]+=1
    c=cnt[k]
    for w in ws: c[w]+=1
def rate(g,ys,w): return 1e4*sum(cnt[(g,y)][w] for y in ys)/sum(tot[(g,y)] for y in ys)
rows=[]
for i,w in enumerate(words):
    bt=rate('tech',(19,20,21,22),i); bo=rate('other',(19,20,21,22),i)
    pt=max((rate('tech',(y,),i),y) for y in (24,25,26)); po=max((rate('other',(y,),i),y) for y in (24,25,26))
    rows.append((w,bt,pt[0],pt[1],pt[0]/(bt+0.3),bo,po[0],po[1],po[0]/(bo+0.3),rate('tech',(26,),i),rate('other',(26,),i)))
keep=[r for r in rows if r[4]>=3 and r[8]>=3 and r[6]>=3]
keep.sort(key=lambda r:-r[4])
print("kept",len(keep))
for r in keep: print(f"{r[0]:16s} tech {r[1]:6.1f}->{r[2]:6.1f} ('{r[3]}) x{r[4]:5.1f} now {r[9]:6.1f} | other {r[5]:6.1f}->{r[6]:6.1f} ('{r[7]}) x{r[8]:5.1f} now {r[10]:6.1f}")
pickle.dump(rows,open("rows.pkl","wb"))
