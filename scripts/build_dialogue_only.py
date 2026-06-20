#!/usr/bin/env python3
"""Build a PDF of ONLY the spoken dialogue — no speaker names, no stage
directions, no headings. Just the lines, in order."""
import os, re, html
from pathlib import Path
import _fullbleed

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("OUT_DIR", HERE.parent / "outputs")); OUT.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")
SRC = HERE.parent / "six_characters_village_players.html"

src = SRC.read_text(encoding="utf-8")
lines = []
for m in re.finditer(r'<p class="speech">(.*?)</p>', src, re.S):
    t = m.group(1)
    t = re.sub(r'<span class="speaker">.*?</span>', '', t, flags=re.S)   # drop WHO
    t = re.sub(r'<span class="action">.*?</span>', '', t, flags=re.S)    # drop stage actions
    t = re.sub(r'</?(?!em\b)[a-zA-Z][^>]*>', '', t)                      # drop tags except <em>
    t = re.sub(r'^\s*[.:;,]?\s*', '', t)                                 # leading speaker-tag punctuation
    t = re.sub(r'\s+', ' ', t).strip()
    if re.sub(r'<[^>]+>', '', t).strip():                               # skip lines with no spoken words
        lines.append(t)
print("dialogue lines:", len(lines))

body = "".join(f'<p>{t}</p>' for t in lines)
doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<style>
@page {{ size: A4; margin: 16mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:12pt; }}
p {{ margin:0 0 3.2mm; line-height:1.5; }}
</style></head><body>{body}</body></html>"""
doc = _fullbleed.apply(doc, top="16mm", side="16mm")
hp = OUT / "dialogue_only.html"; hp.write_text(doc)
pp = OUT / "dialogue_only.pdf"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    kw = {"executable_path": CHROMIUM} if CHROMIUM else {}
    b = p.chromium.launch(**kw); pg = b.new_page()
    pg.goto(f"file://{hp.resolve()}", wait_until="networkidle", timeout=60000); pg.wait_for_timeout(500)
    pg.pdf(path=str(pp), format="A4", print_background=True, prefer_css_page_size=True); b.close()
hp.unlink(missing_ok=True)
print(f"Done: {pp} ({pp.stat().st_size:,} bytes)")
