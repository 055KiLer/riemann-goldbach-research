import json, numpy as np
rows=json.load(open('cache/final_data.json'))
rows=[r for r in rows if r.get('n',0)]
qs=sorted(set(r['q'] for r in rows))
def C(x): return complex(x[0],x[1])
print("# per-q variant table")
print("| q | prim | counts | std_Xab rel mean/med/max | |E-M|/sqrt(q) mean/max | std_X1m rel | swap_Xab rel | swap_X1m rel |")
print("|---|---|---|---|---|---|---|---|")
for q in qs:
    sel=[r for r in rows if r['q']==q]
    relX=[r['std_Xab']['rel'] for r in sel]
    sc=[r['std_Xab']['abs']/np.sqrt(q) for r in sel]
    rel1=[r['std_X1m']['rel'] for r in sel]
    relS=[r['swap_Xab']['rel'] for r in sel]
    relS2=[r['swap_X1m']['rel'] for r in sel]
    print(f"| {q} | {sel[0]['n']} | {tuple(sel[0]['counts'])} | {np.mean(relX):.3f}/{np.median(relX):.3f}/{np.max(relX):.2f} | {np.mean(sc):.2f}/{np.max(sc):.2f} | {np.mean(rel1):.2f} | {np.mean(relS):.2f} | {np.mean(relS2):.2f} |")
print()
print("# parity table")
print("| q | even vs M_e | odd vs M_e | even vs swapped | odd vs swapped |")
print("|---|---|---|---|---|")
for q in qs:
    sel=[r for r in rows if r['q']==q]
    ev=[];od=[];evs=[];ods=[]
    for r in sel:
        Ee=[C(r['Ee'][0]),C(r['Ee'][1])]; P=[C(r['pieces'][0]),C(r['pieces'][1])]
        ev.append(abs(Ee[0]-P[0])/max(1e-12,abs(P[0])))
        od.append(abs(Ee[1]-P[1])/max(1e-12,abs(P[1])))
        evs.append(abs(Ee[0]-P[1])/max(1e-12,abs(P[1])))
        ods.append(abs(Ee[1]-P[0])/max(1e-12,abs(P[0])))
    print(f"| {q} | {np.mean(ev):.3f} | {np.mean(od):.3f} | {np.mean(evs):.3f} | {np.mean(ods):.3f} |")
print()
print("# scaling |E-M|/sqrt(q), std_Xab, mean over shifts")
for q in qs:
    sel=[r for r in rows if r['q']==q]
    sc=np.mean([r['std_Xab']['abs']/np.sqrt(q) for r in sel])
    print(f"q={q}: {sc:.2f}")
