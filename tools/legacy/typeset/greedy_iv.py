"""For each card: the range of frame widths w (pt) for which a greedy line breaker with the PDF's own word widths
reproduces the PC's line breaks (kp_items.json from kp_test.py) -> greedy_iv.json (read by typeset_final.py).
Greedy (first fit) reproduces 841 of 999 master-list cards; a Knuth-Plass composer reproduced fewer (717)."""
import json
I = json.load(open('kp_items.json')); U = json.load(open('pdf/akz_uni.json'))['AkzidenzGroteskBE-Cn']
def prep(it):
    sp = (U[' '] + it['track']) * it['size'] / 1000
    bi = {b: k for k, b in enumerate([0] + it['brk'][:-1])}
    W, G, S = [], [], []
    for i, (w, g) in enumerate(it['seq']):
        off = it['starts'][bi[i]] if i in bi else 0
        W.append(w); G.append(g if g is not None else sp + off); S.append(off)
    return W, G, S
def greedy(W, G, S, Wm):
    br = []; x = None
    for i, w in enumerate(W):
        if x is None: x = S[i] + w
        elif x + G[i] + w <= Wm + 1e-6: x += G[i] + w
        else: br.append(i); x = S[i] + w
    return br + [len(W)]
out = {}
for g, it in I.items():
    W, G, S = prep(it)
    good = [d / 100 for d in range(0, 1500) if greedy(W, G, S, it['lo'] + d / 100) == it['brk']]
    out[g] = (it['lo'] + good[0], it['lo'] + good[-1]) if good else None
json.dump(out, open('greedy_iv.json', 'w'))
print(sum(1 for v in out.values() if v), 'of', len(out), 'cards reproducible by greedy breaking')
