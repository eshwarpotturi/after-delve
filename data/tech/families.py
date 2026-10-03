import pickle, json
P=pickle.load(open("pass2.pkl","rb")); words=P["words"]; docs=P["docs"]; wid={w:i for i,w in enumerate(words)}
A=json.load(open("agg.json")); mo=A["months"]; mi={m:i for i,m in enumerate(mo)}
FAM={"delve":["delve","delves"],"showcase":["showcasing","showcases"],"underscore":["underscore","underscores","underscoring"],"overlook":["overlook","overlooking"]}
ids={f:set(wid[w] for w in L) for f,L in FAM.items()}
cnt={f:[0]*len(mo) for f in FAM}
for ym,pc,ws in docs:
    if ym in mi and pc.split('.')[0] in('cs','eess'):
        s=set(ws)
        for f,I in ids.items():
            if s&I: cnt[f][mi[ym]]+=1
json.dump({"FAM":FAM,"cnt":cnt},open("families.json","w")); print({f:sum(v) for f,v in cnt.items()})
