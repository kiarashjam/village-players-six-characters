#!/usr/bin/env python3
"""Build an ACT ONE-ONLY Actor Rehearsal Script.

Reuses build_actor_script.build_actor_html() (same trimming/stripping and part
headings as the full actor script), drops the Act Two and Act Three articles,
and renders through the same cream print pipeline as the full script
(make_pdf.py). Output: outputs/actor_script_act_one.pdf

Run: python scripts/build_actor_script_act_one.py
"""
import os, sys, subprocess
from pathlib import Path
from bs4 import BeautifulSoup

import build_actor_script

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", ROOT / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)


def build():
    soup = BeautifulSoup(build_actor_script.build_actor_html(), "html.parser")
    for sel in ("#act-2", "#act-3"):
        el = soup.select_one(sel)
        if el:
            el.decompose()
    t = soup.find("title")
    if t:
        t.string = "Six Characters — Actor Rehearsal Script — ACT ONE"
    cover = soup.select_one("section.cover")
    if cover is not None:
        tag = soup.new_tag("p")
        tag.string = "ACT ONE ONLY"
        tag["style"] = ("font-family:'Cormorant Unicase',serif;letter-spacing:0.2em;"
                        "color:#8b3a3a;margin-top:8px;")
        cover.append(tag)

    tmp = ROOT / "_act1_tmp.html"
    tmp.write_text(soup.decode())
    out_pdf = OUT_DIR / "actor_script_act_one.pdf"
    env = dict(os.environ, PDF_SRC=str(tmp), PDF_OUT=str(out_pdf))
    subprocess.run([sys.executable, str(HERE / "make_pdf.py")], env=env, check=True)
    tmp.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
