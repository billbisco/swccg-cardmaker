"""Render an SVG in assets/vector to a transparent PNG in assets/icons (same basename + -vector)."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
for f in sys.argv[1:]:
    p = Path(f); svg = p.read_text()
    html = f"<html><body style='margin:0;background:transparent'><div id=i style='width:300px;height:300px'>{svg.replace('<svg ', '<svg width=300 height=300 ')}</div></body></html>"
    tmp = p.with_suffix('.html'); tmp.write_text(html)
    out = Path('assets/icons') / (p.stem + '-vector.png')
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 300, 'height': 300}); pg.goto(tmp.as_uri())
        pg.locator('#i').screenshot(path=str(out), omit_background=True); b.close()
    tmp.unlink(); print(out)
