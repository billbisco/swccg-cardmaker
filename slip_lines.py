"""Take the slip's own line breaks from the Remaster PDF's text layer and store them in each card JSON as
"game_text_lines" (the game text with \\n at the slip's line ends). The renderer then breaks the text exactly where
the slip does (Bill, 2026-10-12: "Trash Compactor" must stay on one line as on the slip) and only shrinks the
font if a line would not fit.

    python3 slip_lines.py 2            # all cards of set 2
    python3 slip_lines.py 2 10 12      # some
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHEET_PDF = {3: "VirtualCards3-legacy.pdf"}   # the Dec 2006 Remaster sheet of VS3 is the "-legacy" file here
TOKEN = re.compile(r"\{[\w-]+(?::[^}]*)?\}")


def norm(w: str) -> str:
    w = w.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-")
    return re.sub(r"[^a-z0-9<>+=\-()•▲▼.,;:!?'\"/]", "", w.lower())


def pdf_lines(pdf: Path) -> list[tuple[int, float, float, list[str]]]:
    """(page, xMin, yMin, words) for every text line, in PDF points."""
    html = subprocess.run(["pdftotext", "-bbox-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    out = []
    for pg, pm in enumerate(re.finditer(r"<page [^>]*>(.*?)</page>", html, re.S), 1):
        for m in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)"[^>]*>(.*?)</line>', pm.group(1), re.S):
            words = re.findall(r">([^<]*)</word>", m.group(3))
            words = [w.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'") for w in words]
            if words:
                out.append((pg, float(m.group(1)), float(m.group(2)), words))
    return out


def slip_boxes(vs: int, dpi: int = 300):
    """Slip boxes (page, x, y, w, h) in PDF points, detected on the rendered pages like the crops were."""
    from PIL import Image
    import numpy as np
    from scipy import ndimage
    boxes = []
    for png in sorted((ROOT / f"src/slips/vs{vs}").glob("p300-*.png")):
        pg = int(png.stem.split("-")[1])
        a = np.array(Image.open(png).convert("RGB"))
        dark = a.max(axis=2) < 60
        lab, _ = ndimage.label(ndimage.binary_closing(dark, iterations=3))
        bb = []
        for o in ndimage.find_objects(lab):
            h = o[0].stop - o[0].start; w = o[1].stop - o[1].start
            if 700 < w < 800 and 300 < h < 420:   # a slip (the covers have other big dark boxes)
                bb.append((o[1].start, o[0].start, w, h))
        bb.sort(key=lambda b: (round(b[1] / 100), b[0]))
        boxes += [(pg, x * 72 / dpi, y * 72 / dpi, w * 72 / dpi, h * 72 / dpi) for x, y, w, h in bb]
    return boxes


def visible(unit: str) -> str:
    """What a game-text unit (whitespace-separated) looks like in the PDF text layer."""
    u = re.sub(r"\{pilot:(\d+)\}", r"\1", unit)       # pilot-power icon + number → the number
    u = TOKEN.sub("", u)                              # other icons have no text (the key letter is a separate word)
    return norm(u.replace("_", "").replace("*", ""))


def align(units: list[str], lines: list[list[str]]):
    """Find the run of PDF lines holding this text; return the line index of every unit (None if unmatched)."""
    stream = [(li, norm(w)) for li, ws in enumerate(lines) for w in ws]
    if not stream:
        return 0, [None] * len(units)
    vis = [visible(u) for u in units]
    firsts = [i for i, v in enumerate(vis) if v][:3]
    best = None
    for s in range(len(stream)):
        # try to align from stream position s
        pos, hits, idx = s, 0, []
        for v in vis:
            if not v:
                idx.append(None); continue
            # look ahead a little for the word (skips icon letters like "A" in the layer)
            found = None
            for k in range(pos, min(pos + 4, len(stream))):
                for j in (1, 2, 3):   # the layer splits a word at a font change (italic ship names): join up to 3 words
                    if "".join(w for _, w in stream[k:k + j]) == v:
                        found = (k, j); break
                if found:
                    break
            if found is None:
                idx.append(None)
            else:
                idx.append(stream[found[0]][0]); pos = found[0] + found[1]; hits += 1
        if best is None or hits > best[0]:
            best = (hits, idx)
        if hits == len([v for v in vis if v]):
            break
    return best


def main():
    vs = int(sys.argv[1])
    nums = [f"{int(n):02d}" for n in sys.argv[2:]] or sorted(p.stem for p in (ROOT / f"cards/vs{vs}").glob("[0-9][0-9].json"))
    all_lines = pdf_lines(ROOT / "src/slips" / SHEET_PDF.get(vs, f"VirtualCards{vs}.pdf"))
    boxes = slip_boxes(vs)
    for n in nums:
        p = ROOT / f"cards/vs{vs}/{n}.json"
        c = json.loads(p.read_text(encoding="utf-8"))
        pg, bx, by, bw, bh = boxes[int(n) - 1]
        inside = [l for l in all_lines if l[0] == pg and bx - 2 <= l[1] <= bx + bw and by - 2 <= l[2] <= by + bh]
        inside.sort(key=lambda l: (round(l[2]), l[1]))
        lines = [l[3] for l in inside]
        paras = c["game_text"].split("\n")
        out_paras, report = [], []
        for para in paras:
            units = para.split(" ")
            hits, idx = align(units, lines)
            nvis = len([u for u in units if visible(u)])
            # rebuild with breaks where the line index changes
            res, cur = [], None
            for u, li in zip(units, idx):
                if li is not None and cur is not None and li != cur:
                    res.append("\n")
                res.append(u)
                if li is not None:
                    cur = li
            text = " ".join(res).replace(" \n ", "\n")
            out_paras.append(text)
            report.append(f"{hits}/{nvis}")
        c["game_text_lines"] = "\n".join(out_paras)
        p.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
        print(n, " ".join(report), "|", c["game_text_lines"].replace("\n", " / ")[:110])


if __name__ == "__main__":
    main()
