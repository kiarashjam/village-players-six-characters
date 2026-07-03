#!/usr/bin/env python3
"""Build ONE black-and-white, print-friendly bundle for the director.

Stitches the Director's Copy (the whole annotated play) together with the key
companion documents — the Table-Work Plan, the Sound & Music Score, the
Blocking Storyboard, and all nine Part Books — into a single PDF, rendered for
a laser printer: white paper, black ink, normal margins, no cream full-bleed.

How it works without any PDF-merge tool on the box: every standalone builder
funnels its HTML through _fullbleed.apply() just before rendering, so we swap
that for a black-and-white stylesheet, point the builders at a temp folder
(the colour outputs are left untouched), render the play the same way, then
concatenate the pages with pdfrw (pure Python).

Output: outputs/director_bundle_print_bw.pdf
Run: python scripts/build_director_bundle_bw.py
"""
import os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_DIR = ROOT / "outputs"
TMP = ROOT / "outputs" / "_bundle_bw_tmp"
TMP.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

# Send every standalone builder's output into the temp folder, not outputs/.
os.environ["OUT_DIR"] = str(TMP)
sys.path.insert(0, str(HERE))

# --- Black-and-white print stylesheet (replaces the cream full-bleed wrap) ---
BW = (
    "<style id='bw-bundle'>"
    "@page{size:A4;margin:16mm;}"
    "html,body{background:#ffffff !important;color:#000000 !important;}"
    "body *{background-color:transparent !important;background-image:none !important;"
    "box-shadow:none !important;text-shadow:none !important;color:#000000 !important;}"
    "*{border-color:#999999 !important;}"
    ".action{color:#333333 !important;}"
    ".speaker{font-weight:700 !important;}"
    "a{color:#000000 !important;text-decoration:none;}"
    ".r-controls,.r-progress,.r-act-pin{display:none !important;}"
    ".chip,.lbl{color:#000000 !important;background:transparent !important;"
    "border:1px solid #000000 !important;}"
    "main{max-width:100% !important;padding:0 !important;}"
    ".cover{page-break-after:always;}"
    ".act-header{page-break-before:always;}"
    ".speech{orphans:2;widows:2;}"
    "</style>"
)

import _fullbleed  # noqa: E402


def bw_apply(html, top=None, side=None):
    if "</head>" in html:
        return html.replace("</head>", BW + "</head>", 1)
    return BW + html


_fullbleed.apply = bw_apply  # patch: every builder now renders B&W, no full-bleed


def render_html_to_pdf(html, out_pdf):
    tmp_html = TMP / (out_pdf.stem + ".src.html")
    tmp_html.write_text(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        kw = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**kw)
        pg = b.new_page()
        pg.goto(f"file://{tmp_html.resolve()}", wait_until="networkidle", timeout=90000)
        pg.wait_for_timeout(700)
        pg.pdf(path=str(out_pdf), format="A4",
               margin={"top": "16mm", "right": "16mm", "bottom": "16mm", "left": "16mm"},
               print_background=False, prefer_css_page_size=True)
        b.close()
    tmp_html.unlink(missing_ok=True)


def build():
    order = []  # (label, pdf_path) in bundle order

    # 1) Director's Copy — the whole annotated play, in B&W
    print("· Director's Copy (play) …")
    play = (ROOT / "six_characters_village_players.html").read_text()
    play_pdf = TMP / "00_directors_copy.pdf"
    render_html_to_pdf(bw_apply(play), play_pdf)
    order.append(("Director's Copy", play_pdf))

    # 2) Companion builders (they render B&W into TMP via the patched _fullbleed)
    import build_table_work_plan; print("· Table-Work Plan …"); build_table_work_plan.build()
    order.append(("Table-Work Plan", TMP / "table_work_plan.pdf"))
    import build_sound_score; print("· Sound & Music Score …"); build_sound_score.build()
    order.append(("Sound & Music Score", TMP / "sound_score.pdf"))
    import build_blocking_storyboard; print("· Blocking Storyboard …"); build_blocking_storyboard.build()
    order.append(("Blocking Storyboard", TMP / "blocking_storyboard.pdf"))
    import build_part_books; print("· Part Books (×9) …"); build_part_books.main()
    for slug in ["father", "mother", "step_daughter", "son", "manager",
                 "madame_pace", "player1", "player2", "player3"]:
        pb = TMP / f"{slug}_part_book.pdf"
        if pb.exists():
            order.append((f"Part book: {slug}", pb))

    # 3) Concatenate everything with pdfrw
    from pdfrw import PdfReader, PdfWriter
    w = PdfWriter()
    total = 0
    for label, pdf in order:
        if not pdf.exists():
            print(f"  ! missing, skipped: {label}")
            continue
        pages = PdfReader(str(pdf)).pages
        w.addpages(pages)
        total += len(pages)
        print(f"  + {label}: {len(pages)} pp")
    out = OUT_DIR / "director_bundle_print_bw.pdf"
    w.write(str(out))
    print(f"\nDone: {out} ({out.stat().st_size:,} bytes, {total} pages)")


if __name__ == "__main__":
    build()
