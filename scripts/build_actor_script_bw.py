#!/usr/bin/env python3
"""Build a PRINT-FRIENDLY, BLACK-AND-WHITE Actor Rehearsal Script PDF.

Same content as the actor script (built by build_actor_script.build_actor_html),
but rendered for a laser printer instead of the screen/cream edition:
  - white paper, black ink (no cream full-bleed background to soak up toner)
  - normal page margins (not edge-to-edge)
  - the maroon accents flattened to black; all fills removed
  - speaker names stay bold, stage directions stay italic, so the page still
    reads clearly with no colour at all.

A4 portrait. Run: python scripts/build_actor_script_bw.py
"""
import os
from pathlib import Path

import build_actor_script  # reuse the exact same trimming/strip logic

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", ROOT / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

# Black-and-white, print-friendly overrides. Injected last so it wins.
BW_CSS = """
<style id="bw-print-overrides">
  @page { size: A4; margin: 18mm; }

  /* White paper, black ink — kill every fill and the cream theme variables. */
  html, body { background: #ffffff !important; color: #000000 !important; }
  body {
    --bg: #ffffff; --ink: #000000; --ink-soft: #333333;
    --accent: #000000; --rule: #999999; --suggest: #000000;
    font-size: 11.5pt; line-height: 1.5;
  }
  body * { background-color: transparent !important; background-image: none !important;
           box-shadow: none !important; text-shadow: none !important; color: #000000 !important; }
  * { border-color: #999999 !important; }

  /* Keep the page's structure legible in mono. */
  .speaker { color: #000000 !important; font-weight: 700; }
  .action  { color: #333333 !important; font-style: italic; }
  a { color: #000000 !important; text-decoration: none; }

  /* Hide the on-screen reader controls (also print-hidden, but be safe). */
  .r-controls, .r-progress, .r-act-pin { display: none !important; }

  /* Sensible print breaks. */
  main { max-width: 100% !important; padding: 0 !important; }
  .cover { page-break-after: always; }
  .act-header { page-break-before: always; }
  .speech { orphans: 2; widows: 2; }
</style>
"""


def build():
    html = build_actor_script.build_actor_html()
    if "</head>" in html:
        html = html.replace("</head>", BW_CSS + "\n</head>", 1)
    else:
        html = BW_CSS + html

    out_html = OUT_DIR / "actor_script_print_bw.html"
    out_html.write_text(html)
    out_pdf = OUT_DIR / "actor_script_print_bw.pdf"

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**launch_kwargs)
        pg = b.new_page()
        pg.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(800)
        pg.pdf(
            path=str(out_pdf),
            format="A4",
            margin={"top": "18mm", "right": "18mm", "bottom": "18mm", "left": "18mm"},
            print_background=False,   # never paint backgrounds — pure white paper
            prefer_css_page_size=True,
        )
        b.close()
    out_html.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
