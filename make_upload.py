"""Build a wiki upload folder for an Original Virtual Set: full-card remasters (745 px webp, q90) named as
wiki_vs.py links them, the re-cropped slips under the names the stubs already use, and the set symbol.

    python3 make_upload.py 8 out/vs8-upload            # everything
    python3 make_upload.py 3 out/rr-upload --changed    # only remasters whose pixels differ from the last upload
"""
from __future__ import annotations
import io, json, re, shutil, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "out"


def remaster_name(vs: int, n: str, c: dict) -> str:
    safe = re.sub(r"[^A-Za-z0-9]+", "_", c["title"].replace("•", "")).strip("_")
    return f"OVS{vs}-{int(n):02d}-{safe}-remaster.webp"


def last_uploaded() -> dict[str, Path]:
    """Newest copy of every OVS*-remaster.webp under out/ (what the wiki holds now)."""
    best: dict[str, Path] = {}
    for p in OUT_DIR.rglob("OVS*-remaster.webp"):
        if "rr-upload" in p.parts[-2]:
            continue
        if p.name not in best or p.stat().st_mtime > best[p.name].stat().st_mtime:
            best[p.name] = p
    return best


def webp_bytes(png: Path) -> bytes:
    b = io.BytesIO()
    Image.open(png).save(b, "WEBP", quality=90, method=6)
    return b.getvalue()


def differs(new: bytes, old: Path) -> float:
    a = np.asarray(Image.open(io.BytesIO(new)).convert("RGBA")).astype(int)
    b = np.asarray(Image.open(old).convert("RGBA")).astype(int)
    if a.shape != b.shape:
        return 999.0
    return float(np.abs(a - b).max(axis=2).__gt__(40).mean() * 100)   # % of pixels changed noticeably


def main():
    vs, dest = int(sys.argv[1]), Path(sys.argv[2])
    changed_only = "--changed" in sys.argv
    dest.mkdir(parents=True, exist_ok=True)
    prev = last_uploaded() if changed_only else {}
    nums = sorted(p.stem for p in (ROOT / f"cards/vs{vs}").glob("[0-9][0-9].json"))
    report = []
    for n in nums:
        c = json.load(open(ROOT / f"cards/vs{vs}/{n}.json", encoding="utf-8"))
        name = remaster_name(vs, n, c)
        png = OUT_DIR / f"vs{vs}-{n}_745.png"
        data = webp_bytes(png)
        if changed_only:
            old = prev.get(name)
            d = differs(data, old) if old else 999.0
            if d < 0.05:
                continue
            report.append(f"{vs}-{n} {d:.2f}% {name}")
        (dest / name).write_bytes(data)
        if c.get("game_text_back"):   # objective back
            back = OUT_DIR / f"vs{vs}-{n}b_745.png"
            if back.exists():
                safe_b = re.sub(r"[^A-Za-z0-9]+", "_", (c.get("title_back") or "").replace("•", "")).strip("_")
                (dest / f"OVS{vs}-{int(n):02d}b-{safe_b}-remaster.webp").write_bytes(webp_bytes(back))
    if not changed_only:
        stubs = {int(v["image"][5:7]): v["image"] for v in json.load(open(ROOT / "gempdata/original-vs-stubs.json", encoding="utf-8")).values()
                 if v["set"] == f"Virtual Set {vs} (Original)"}
        for p in sorted((ROOT / f"src/slips/vs{vs}").glob("[0-9][0-9]-*.png")):
            shutil.copy(p, dest / stubs[int(p.name[:2])])
        shutil.copy(ROOT / f"assets/icons/ovs-set-{vs}.png", dest / f"VS{vs}O-set-symbol.png")
    print("\n".join(report))
    print(len(list(dest.iterdir())), "files in", dest)


if __name__ == "__main__":
    main()
