#!/usr/bin/env python3
"""Render six_characters.html to PDF using Playwright/Chromium.

Adds a small print-only override stylesheet to:
- Force the light/cream Day theme
- Hide interactive UI (controls, progress strip, act pin)
- Set page margins and page breaks
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("PDF_SRC", HERE / "six_characters_village_players.html"))
OUT = Path(os.environ.get("PDF_OUT", HERE / "outputs" / "six_characters.pdf"))
CHROMIUM = os.environ.get("CHROMIUM_PATH")  # optional override

PRINT_CSS = """
<style id="print-overrides">
  @page { size: A4; margin: 22mm 18mm 22mm 18mm; }

  html, body { background: #efe6cf !important; color: #2a201a !important; }
  body {
    --bg: #efe6cf;
    --ink: #2a201a;
    --ink-soft: #6b5b48;
    --accent: #8b3a3a;
    --rule: rgba(42, 32, 26, 0.18);
    --suggest: #2d6373;
  }

  /* Hide interactive UI */
  .r-controls, .r-progress, .r-act-pin { display: none !important; }

  /* Page breaks at major boundaries */
  .cover { page-break-after: always; }
  .act-header { page-break-before: always; }
  .part-note { page-break-before: always; page-break-inside: avoid; }
  .portrait, .casting-note { page-break-inside: avoid; }
  .speech { orphans: 2; widows: 2; }

  main { max-width: 100% !important; padding: 0 !important; }
  body { font-size: 11pt; line-height: 1.55; }

  .stats-list li { page-break-inside: avoid; }
</style>
"""

html = SRC.read_text()
if "</head>" in html:
    html_with_overrides = html.replace("</head>", PRINT_CSS + "\n</head>", 1)
else:
    html_with_overrides = PRINT_CSS + html

TMP = SRC.parent / "_pdf_tmp.html"
TMP.write_text(html_with_overrides)

print(f"Rendering {SRC.name} → PDF via Chromium…")

with sync_playwright() as p:
    launch_kwargs = {}
    if CHROMIUM:
        launch_kwargs["executable_path"] = CHROMIUM
    browser = p.chromium.launch(**launch_kwargs)
    page = browser.new_page()
    page.goto(f"file://{TMP.resolve()}", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(1200)
    page.pdf(
        path=str(OUT),
        format="A4",
        margin={"top": "22mm", "right": "18mm", "bottom": "22mm", "left": "18mm"},
        print_background=True,
        prefer_css_page_size=True,
    )
    browser.close()

TMP.unlink(missing_ok=True)
print(f"\nDone: {OUT} ({OUT.stat().st_size:,} bytes)")
