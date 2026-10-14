"""Slip boxes of a Remaster sheet, keyed by the slip's printed number.

    boxes = slip_boxes(4)   # {"01": (page, x, y, w, h), …, "11b": …}   (pixels at 300 DPI)

A slip is a dark component 500–800 px wide and 120–460 px tall on src/slips/vsN/p300-*.png (Objectives are taller,
site slips are shorter and narrower); components inside another one are dropped. The number is the two-digit word
printed in the slip's caption strip (from the PDF text layer); the second slip with the same number (an Objective's
back) gets a "b" suffix."""
from __future__ import annotations
import re, subprocess
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent
SHEET_PDF = {3: "VirtualCards3-legacy.pdf"}   # the Dec 2006 Remaster sheet of VS3 is the "-legacy" file here
DPI = 300


def sheet_pdf(vs: int) -> Path:
    return ROOT / "src/slips" / SHEET_PDF.get(vs, f"VirtualCards{vs}.pdf")


def pdf_words(vs: int):
    html = subprocess.run(["pdftotext", "-bbox-layout", str(sheet_pdf(vs)), "-"], capture_output=True, text=True).stdout
    out = []
    for pg, pm in enumerate(re.finditer(r"<page [^>]*>(.*?)</page>", html, re.S), 1):
        for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', pm.group(1)):
            out.append((pg, float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(5)))
    return out


DARK_THR = {10: 100}   # VS10's white-framed slips have a grey (not black) outline


MAX_H = {12: 530, 13: 1100, 14: 1100, 15: 1100, 16: 1100}     # VS12's Epic Event and two-title Effect slips are taller


def raw_boxes(png: Path, thr: int = 60, max_h: int = 460):
    a = np.array(Image.open(png).convert("RGB"))
    dark = a.max(axis=2) < thr
    lab, _ = ndimage.label(ndimage.binary_closing(dark, iterations=3))
    bb = []
    for o in ndimage.find_objects(lab):
        h = o[0].stop - o[0].start; w = o[1].stop - o[1].start
        if 500 < w < 1100 and 120 < h < max_h:      # site slips are 1052 wide, Objectives 432 tall
            bb.append((o[1].start, o[0].start, w, h))
    # drop boxes contained in another box
    keep = []
    for b in bb:
        x, y, w, h = b
        if not any(o != b and o[0] <= x and o[1] <= y and o[0] + o[2] >= x + w and o[1] + o[3] >= y + h for o in bb):
            keep.append(b)
    return keep


def slip_boxes(vs: int) -> dict[str, tuple[int, int, int, int, int]]:
    words = pdf_words(vs)
    found: dict[str, tuple] = {}
    for png in sorted((ROOT / f"src/slips/vs{vs}").glob("p300-*.png")):
        pg = int(png.stem.split("-")[1])
        for x, y, w, h in sorted(raw_boxes(png, DARK_THR.get(vs, 60), MAX_H.get(vs, 460)), key=lambda b: (b[1], b[0])):
            X, Y, W, H = [v * 72 / DPI for v in (x, y, w, h)]
            nums = [t for p, x0, y0, x1, y1, t in words if p == pg and X <= x0 <= X + W and Y + H - 20 <= y0 <= Y + H and re.fullmatch(r"\d\d", t)]
            if not nums:
                continue
            real = [n for n in nums if n != "00"]   # VS14's sheet hides a stray "00" under some numbers
            if not real:
                continue                            # cover / rule-card boxes
            key = real[-1]
            if key in found:
                key += "b"
            found[key] = (pg, x, y, w, h)
    return found


if __name__ == "__main__":
    import sys
    b = slip_boxes(int(sys.argv[1]))
    print(len(b), sorted(b))
