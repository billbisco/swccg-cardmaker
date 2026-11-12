import sys, json, numpy as np, cv2
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); from framefit import load, cost
for d in sys.argv[1:]:
    B, P, m = load(Path(d))
    g = lambda a: cv2.GaussianBlur(cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32), (5,5), 0)
    W = np.eye(2, 3, dtype=np.float32)
    try:
        _, W = cv2.findTransformECC(g(P), g(B), W, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), m, 5)
    except cv2.error as e: print(d, "fail", e); continue
    # W maps PC coords -> build coords; invert to get build->PC
    A = cv2.invertAffineTransform(W)
    sx, sy = A[0,0], A[1,1]; cx, cy = 372.5, 519.5
    tx = A[0,0]*cx + A[0,1]*cy + A[0,2] - cx; ty = A[1,0]*cx + A[1,1]*cy + A[1,2] - cy
    M = A
    Wb = cv2.warpAffine(B, M, (745,1039), flags=cv2.INTER_CUBIC)
    print(f"{d}: sx {sx:.4f} sy {sy:.4f} shear {A[0,1]:+.4f}/{A[1,0]:+.4f} centre shift {tx:+.2f},{ty:+.2f}  MAD {np.abs(B-P).mean(2)[m>0].mean():.2f} -> {np.abs(Wb-P).mean(2)[m>0].mean():.2f}")
