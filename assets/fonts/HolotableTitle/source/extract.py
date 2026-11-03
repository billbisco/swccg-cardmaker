"""#118: glyph instances straight from the PC titles, no reference font involved.
Each title's ink is split into letter clusters (connected components merged where they overlap horizontally:
i, j, !, ?, :, ;). A title is used only when its cluster count equals its letter count, so every cluster IS that
letter. Instances are scaled by the title's measured cap height, aligned on the baseline, registered to each other
at sub-pixel precision and averaged at S x super-resolution.
Out: glyphs/<cp>.png (ink white on black, canonical px), glyphs/meta.json (per letter: n, baseline row, and the
measured spacing: left/right gap to neighbours), pairs.json (measured gaps per letter pair)."""
import json, os, re, math, collections
import numpy as np, cv2
from PIL import Image

S = 8
rows = [r for r in json.load(open('cards.json')) if r['type'] != 'Location']
CAPS = set('ABCDEFGHIJKLMNOPRSTUVWXYZbdfhklt0123456789')   # letters whose top is the cap/ascender line
FLAT = set('ABDEFHIKLMNPRTUVWXYZ0123456789abdehiklmnrtuvwxz')  # letters that sit flat on the baseline (no descender, no overshoot)


def clean(t):
    t = re.sub(r"\s*\((V|AI|ALT|Holo AI|Premium)\)", "", t or "")
    return t.replace("'", "’").replace("<>", "")


def title_mask(path, dark):
    a = np.asarray(Image.open(path).convert('L')).astype(np.float32)
    band = a[40:125, 95:612]
    v = band.astype(np.uint8)
    t, _ = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if dark:   # white ink
        hi = np.percentile(band, 99.5); t = max(t, (np.median(band) + hi) / 2)
        ink = np.clip((band - t + 30) / 60, 0, 1)
    else:      # black ink on silver
        lo = np.percentile(band, 0.5); t = min(t, (np.median(band) + lo) / 2)
        ink = np.clip((t + 30 - band) / 60, 0, 1)
    return ink


def clusters(ink):
    m = (ink > 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    comps = [dict(x0=st[i, 0], y0=st[i, 1], x1=st[i, 0] + st[i, 2] - 1, y1=st[i, 1] + st[i, 3] - 1, a=st[i, 4], i=i) for i in range(1, n) if st[i, 4] >= 3]
    comps.sort(key=lambda c: c['x0'])
    # discs / destiny ring: very tall blobs; drop them and everything left of the last disc before the title
    tall = [c for c in comps if c['y1'] - c['y0'] > 52]
    if tall:
        left_discs = [c for c in tall if c['x1'] < 300]
        if left_discs:
            cut = max(c['x1'] for c in left_discs)
            comps = [c for c in comps if c['x0'] > cut]
        right = [c for c in tall if c['x0'] > 400]
        if right:
            cut = min(c['x0'] for c in right)
            comps = [c for c in comps if c['x1'] < cut]
        comps = [c for c in comps if c['y1'] - c['y0'] <= 52]
    cl = []
    for c in comps:   # merge components overlapping horizontally (dots of i/j, ! ? : ;)
        if cl and c['x0'] <= cl[-1]['x1'] - 1 and (min(c['x1'], cl[-1]['x1']) - max(c['x0'], cl[-1]['x0'])) >= 0.5 * min(c['x1'] - c['x0'] + 1, cl[-1]['x1'] - cl[-1]['x0'] + 1):
            p = cl[-1]; p['x0'] = min(p['x0'], c['x0']); p['x1'] = max(p['x1'], c['x1']); p['y0'] = min(p['y0'], c['y0']); p['y1'] = max(p['y1'], c['y1']); p['ids'].append(c['i'])
        else:
            cl.append(dict(c, ids=[c['i']]))
    return cl, lab


inst = collections.defaultdict(list); gaps = collections.defaultdict(list); cap_heights = []
used = tried = dp_used = 0
titles = []
for r in rows:
    p = f"crops/{r['key']}.png"
    if not os.path.exists(p):
        continue
    text = clean(r['title'])
    letters = [c for c in text if c != ' ']
    if not letters:
        continue
    tried += 1
    try:
        ink = title_mask(p, r['side'] == 'Dark')
    except Exception:
        continue
    cl, lab = clusters(ink)
    cl = [c for c in cl if c['x0'] > 1 and c['x1'] < ink.shape[1] - 2]          # nothing cut by the band edge
    if text.startswith('•'):      # everything left of the first bullet is a disc or icon
        bl = [k for k, c in enumerate(cl) if (c['x1'] - c['x0']) < 16 and (c['y1'] - c['y0']) < 16 and abs((c['x1'] - c['x0']) - (c['y1'] - c['y0'])) <= 4]
        if bl:
            cl = cl[bl[0]:]
    # specks to the right of the title (frame texture by the destiny ring)
    while len(cl) > 1 and (cl[-1]['x0'] - cl[-2]['x1']) > 25:
        cl = cl[:-1]
    if cl:
        titles.append((r, text, letters, ink, cl, lab))


def metrics(cl):
    base = float(np.median([c['y1'] for c in cl])) + 1
    top = float(np.percentile([c['y0'] for c in cl], 10))
    return base, base - top


def take(text, letters, ink, cl, lab, assign, base, capH):
    """assign: list of letter index (or None) per cluster; records single-letter instances and spacing."""
    global used
    by_letter = {li: c for c, li in zip(cl, assign) if li is not None}
    cap_heights.append(capH)
    k = -1; prev = None; sp = False
    for ch in text:
        if ch == ' ':
            sp = True; continue
        k += 1
        c = by_letter.get(k)
        if c is not None and prev is not None and prev[0] == k - 1:
            gaps[(prev[1], ' ' if sp else '', ch)].append((c['x0'] - prev[2]['x1'] - 1) / capH)
        prev = (k, ch, c) if c is not None else None; sp = False
    for li, c in by_letter.items():
        mask = np.isin(lab, c['ids']).astype(np.float32)
        m2 = cv2.dilate(mask, np.ones((3, 3), np.uint8))
        inst[letters[li]].append((ink * m2, c, base, capH))


# pass 1: titles whose cluster count equals the letter count
widths = collections.defaultdict(list); rest = []
for r, text, letters, ink, cl, lab in titles:
    if len(cl) == len(letters):
        base, capH = metrics(cl)
        if 22 < capH < 40:
            used += 1
            take(text, letters, ink, cl, lab, list(range(len(cl))), base, capH)
            for ch, c in zip(letters, cl):
                widths[ch].append((c['x1'] - c['x0'] + 1) / capH)
            continue
    rest.append((r, text, letters, ink, cl, lab))
W_ = {ch: float(np.median(v)) for ch, v in widths.items() if len(v) >= 3}
GAP = 0.06
def wexp(ch):
    return W_.get(ch, W_.get(ch.lower(), W_.get(ch.upper(), 0.45)))

# pass 2: align clusters to letters (a cluster is 1 letter, 2-3 touching letters, or a speck) by dynamic programming
for r, text, letters, ink, cl, lab in rest:
    base, capH = metrics(cl)
    if not (22 < capH < 40):
        continue
    m, n = len(cl), len(letters)
    INF = 1e9
    D = np.full((m + 1, n + 1), INF); B = {}
    D[0, 0] = 0
    for i in range(m):
        w = (cl[i]['x1'] - cl[i]['x0'] + 1) / capH
        small = (cl[i]['y1'] - cl[i]['y0']) < 0.25 * capH and w < 0.15
        for j in range(n + 1):
            if D[i, j] >= INF:
                continue
            if small and D[i, j] + 0.05 < D[i + 1, j]:           # speck: skip
                D[i + 1, j] = D[i, j] + 0.05; B[(i + 1, j)] = (i, j, 0)
            for k in (1, 2, 3):
                if j + k > n:
                    break
                e = sum(wexp(ch) for ch in letters[j:j + k]) + GAP * (k - 1)
                cost = abs(w - e) / max(e, 0.2) + (0.15 * (k - 1))
                if D[i, j] + cost < D[i + 1, j + k]:
                    D[i + 1, j + k] = D[i, j] + cost; B[(i + 1, j + k)] = (i, j, k)
    if D[m, n] >= INF or D[m, n] / max(1, m) > 0.25:
        continue
    assign = [None] * m; i, j = m, n
    ok = True
    while (i, j) != (0, 0):
        pi, pj, k = B[(i, j)]
        if k == 1:
            w = (cl[pi]['x1'] - cl[pi]['x0'] + 1) / capH; e = wexp(letters[pj])
            assign[pi] = pj if abs(w - e) / max(e, 0.2) < 0.18 else None
        i, j = pi, pj
    dp_used += 1
    take(text, letters, ink, cl, lab, assign, base, capH)
print('pass 2 titles used', dp_used)
print('titles tried', tried, 'exact', used, 'dp', dp_used, 'median cap height', np.median(cap_heights))
CAP = float(np.median(cap_heights))
json.dump({'cap_px': CAP, 'S': S}, open('scale.json', 'w'))

os.makedirs('glyphs', exist_ok=True)
meta = {}
for ch, L in sorted(inst.items(), key=lambda kv: -len(kv[1])):
    P = []
    for ink, c, base, capH in L:
        sc = S * CAP / capH                     # normalise every title to the median cap height
        pad = 4
        x0, x1 = c['x0'] - pad, c['x1'] + pad
        w = int(round((x1 - x0) * sc)); h = 85 * S     # canonical window: baseline at row 60*S
        M = np.float32([[1 / sc, 0, x0], [0, 1 / sc, base - 60 * S / sc]])
        P.append(cv2.warpAffine(ink, M, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_CUBIC, borderValue=0))
    W = int(np.median([q.shape[1] for q in P])) + 6 * S; H = P[0].shape[0]
    Q = []
    for q in P:   # centre horizontally in a common canvas
        z = np.zeros((H, W), np.float32); off = (W - q.shape[1]) // 2
        if off >= 0:
            z[:, off:off + q.shape[1]] = q[:H, :]
        else:
            z[:, :] = q[:H, -off:-off + W]
        Q.append(z)
    mean = np.median(np.stack(Q), 0)
    keep_n = len(Q)
    for it in range(5):
        R, sc_ = [], []
        for q in Q:
            (dx, dy), _ = cv2.phaseCorrelate(mean.astype(np.float32), q.astype(np.float32))
            dy = 0.0 if abs(dy) > 1.5 * S else dy   # baseline is already known; allow only small vertical refinement
            rq = cv2.warpAffine(q, np.float32([[1, 0, -dx], [0, 1, -dy]]), (W, H), flags=cv2.INTER_LINEAR)
            R.append(rq); sc_.append(float(np.corrcoef(rq.ravel(), mean.ravel())[0, 1]))
        sc_ = np.array(sc_)
        # outliers: a different glyph (miscounted title), a neighbour in the window, or a bad cut
        good = sc_ >= max(0.6, np.median(sc_) - 2.5 * (np.median(np.abs(sc_ - np.median(sc_))) + 1e-3)) if len(R) >= 4 else np.ones(len(R), bool)
        keep_n = int(good.sum())
        mean = np.mean(np.stack([r for r, g in zip(R, good) if g]), 0)
    cv2.imwrite(f'glyphs/{ord(ch):04x}.png', (np.clip(mean, 0, 1) * 255).astype(np.uint8))
    meta[ch] = {'n': len(L), 'kept': keep_n, 'W': W, 'H': H, 'baseline_row': int(60 * S)}
print({k: v['n'] for k, v in meta.items()})
json.dump(meta, open('glyphs/meta.json', 'w'), ensure_ascii=False, indent=0)
json.dump({'|'.join(k): v for k, v in gaps.items()}, open('pairs.json', 'w'), ensure_ascii=False)
