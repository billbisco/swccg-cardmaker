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
            if 700 < w < 800 and 300 < h < 460:   # a slip (the covers have other big dark boxes)
                bb.append((o[1].start, o[0].start, w, h))
        bb.sort(key=lambda b: (round(b[1] / 100), b[0]))
        boxes += [(pg, x * 72 / dpi, y * 72 / dpi, w * 72 / dpi, h * 72 / dpi) for x, y, w, h in bb]
    return boxes


def visible(unit: str) -> str:
    """What a game-text unit (whitespace-separated) looks like in the PDF text layer."""
    u = re.sub(r"\{pilot:(\d+)\}", r"\1", unit)       # pilot-power icon + number → the number
    u = TOKEN.sub("", u)                              # other icons have no text (the key letter is a separate word)
    return norm(u.replace("_", "").replace("*", ""))


def merge_runs(inside):
    """Text runs on one printed line (split by an inline icon or a glyph in another font) share a y within 7 pt:
    merge them, keeping the first run's y. Lone 1–2 digit numbers (deploy/forfeit/slip number) are not text."""
    inside = [l for l in inside if not (len(l[3]) == 1 and re.fullmatch(r"\d{1,2}", l[3][0]))]
    # stat boxes and type banners are all-caps lines (POWER 1, FORCE-SENSITIVE, LOST INTERRUPT): not game text
    inside = [l for l in inside if any(w != w.upper() for w in l[3] if re.search(r"[A-Za-z]", w))]
    inside.sort(key=lambda l: (l[2], l[1]))
    merged = []
    for l in inside:
        if merged and abs(merged[-1][2] - l[2]) < 4 and l[1] >= merged[-1][1]:
            merged[-1] = (l[0], merged[-1][1], merged[-1][2], merged[-1][3] + l[3])
        else:
            merged.append(l)
    return merged


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
    from sheet import slip_boxes as keyed_boxes, sheet_pdf
    all_lines = pdf_lines(sheet_pdf(vs))
    keyed = keyed_boxes(vs)
    for n in nums:
        p = ROOT / f"cards/vs{vs}/{n}.json"
        c = json.loads(p.read_text(encoding="utf-8"))
        pg, bx, by, bw, bh = keyed[n]
        bx, by, bw, bh = [v * 72 / 300 for v in (bx, by, bw, bh)]
        inside = [l for l in all_lines if l[0] == pg and bx - 2 <= l[1] <= bx + bw and by - 2 <= l[2] <= by + bh]
        inside.sort(key=lambda l: (round(l[2]), l[1]))
        # an inline icon splits one printed line into two text runs at the same y: merge runs whose yMin is within 3 pt
        merged = merge_runs(inside)
        lines = [l[3] for l in merged]
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
        if c.get("game_text_back") and n + "b" in keyed:
            pg, bx, by, bw, bh = keyed[n + "b"]
            bx, by, bw, bh = [v * 72 / 300 for v in (bx, by, bw, bh)]
            inside = [l for l in all_lines if l[0] == pg and bx - 2 <= l[1] <= bx + bw and by - 2 <= l[2] <= by + bh]
            inside.sort(key=lambda l: (round(l[2]), l[1]))
            merged = merge_runs(inside)
            blines = [l[3] for l in merged]
            units = c["game_text_back"].split(" ")
            hits, idx = align(units, blines)
            res, cur = [], None
            for u, li in zip(units, idx):
                if li is not None and cur is not None and li != cur:
                    res.append("\n")
                res.append(u)
                if li is not None:
                    cur = li
            c["game_text_back_lines"] = " ".join(res).replace(" \n ", "\n")
            report.append(f"back {hits}/{len([u for u in units if visible(u)])}")
        p.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
        print(n, " ".join(report), "|", c["game_text_lines"].replace("\n", " / ")[:110])


if __name__ == "__main__":
    main()
