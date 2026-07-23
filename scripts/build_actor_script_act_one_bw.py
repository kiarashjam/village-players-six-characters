#!/usr/bin/env python3
"""Build the ACT ONE-only Actor Rehearsal Script in print-friendly BLACK &
WHITE — white paper, black ink, normal margins, no colour.

Reuses build_actor_script.build_actor_html() (same trims/strips/part
headings), drops Acts Two and Three, and applies the same black-and-white
stylesheet as build_actor_script_bw. Output:
outputs/actor_script_act_one_print_bw.pdf

Run: python scripts/build_actor_script_act_one_bw.py
"""
import os
from pathlib import Path
from bs4 import BeautifulSoup

import build_actor_script
import build_actor_script_bw as BW

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", ROOT / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")


def build():
    soup = BeautifulSoup(build_actor_script.build_actor_html(), "html.parser")
    for sel in ("#act-2", "#act-3"):
        el = soup.select_one(sel)
        if el:
            el.decompose()
    t = soup.find("title")
    if t:
        t.string = "Six Characters — Actor Rehearsal Script — ACT ONE (print B&W)"
    cover = soup.select_one("section.cover")
    if cover is not None:
        p = soup.new_tag("p")
        p.string = "ACT ONE ONLY"
        p["style"] = ("font-family:'Cormorant Unicase',serif;letter-spacing:0.2em;"
                      "color:#8b3a3a;margin-top:8px;")
        cover.append(p)
    html = soup.decode()
    html = html.replace("</head>", BW.BW_CSS + "\n</head>", 1) if "</head>" in html else BW.BW_CSS + html

    out_html = OUT_DIR / "actor_script_act_one_print_bw.html"
    out_html.write_text(html)
    out_pdf = OUT_DIR / "actor_script_act_one_print_bw.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        kw = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**kw)
        pg = b.new_page()
        pg.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=90000)
        pg.wait_for_timeout(700)
        pg.pdf(path=str(out_pdf), format="A4",
               margin={"top": "18mm", "right": "18mm", "bottom": "18mm", "left": "18mm"},
               print_background=False, prefer_css_page_size=True)
        b.close()
    out_html.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
