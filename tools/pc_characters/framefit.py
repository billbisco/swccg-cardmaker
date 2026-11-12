"""Fit scale+offset of build frame onto PC frame (745 space), masking element boxes and art window."""
import json, sys, numpy as np, cv2
from pathlib import Path
def load(d):
    r = json.load(open(d/"report.json"))
    B = cv2.imread(str(d/"build.png")).astype(np.float32)
    P = cv2.imread(str(d/"pc.png")).astype(np.float32)
    m = np.ones(B.shape[:2], np.uint8)
    for k, e in r["elements"].items():
        if e.get("box"):
            x, y, w, h = e["box"]; m[max(0,y-6):y+h+6, max(0,x-6):x+w+6] = 0
    m[:, :40] = 0; m[:, -40:] = 0; m[:40] = 0; m[-40:] = 0   # rounded corners / border
    return B, P, m
def cost(B, P, m, s, tx, ty, cx=372.5, cy=519.5):
    M = np.float32([[s, 0, cx - s*cx + tx], [0, s, cy - s*cy + ty]])
    W = cv2.warpAffine(B, M, (B.shape[1], B.shape[0]), flags=cv2.INTER_CUBIC)
    return np.abs(W - P).mean(2)[m > 0].mean()
def fit(dirs):
    data = [load(Path(d)) for d in dirs]
    f = lambda s, tx, ty: np.mean([cost(B, P, m, s, tx, ty) for B, P, m in data])
    best = (f(1, 0, 0), 1, 0, 0); base = best[0]
    for step_s, step_t, n in ((0.002, 1.0, 3), (0.001, 0.5, 2), (0.0005, 0.25, 2)):
        _, s0, x0, y0 = best
        for s in s0 + step_s*np.arange(-n, n+1):
            for tx in x0 + step_t*np.arange(-n, n+1):
                for ty in y0 + step_t*np.arange(-n, n+1):
                    c = f(s, tx, ty)
                    if c < best[0]: best = (c, s, tx, ty)
    return base, best
if __name__ == "__main__":
    base, (c, s, tx, ty) = fit(sys.argv[1:])
    print(f"MAD {base:.2f} -> {c:.2f}  scale {s:.4f}  tx {tx:+.2f} ty {ty:+.2f} (745 px)")
