#!/usr/bin/env python3
"""Build the Reading Edition PDF.

The complete play, in order, where EVERY spoken line is preceded by a short
interpretive note — what the line means and the intent / subtext beneath it.
The notes live in data/reading_glosses.json (one per speech, in document
order); this script harvests the script from the Director's Copy, pairs each
speech with its note, and lays the two together.

A4 portrait, cream full-bleed. Run: python scripts/build_reading_edition.py
"""
import os
import re
import sys
import json
import html as _html
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _fullbleed

ROOT = HERE.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", ROOT / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")
SRC = ROOT / "six_characters_village_players.html"
GLOSS = ROOT / "data" / "reading_glosses.json"

ACT_TITLE = {"Act One": "Act One — The Family",
             "Act Two": "Act Two — The Theatre",
             "Act Three": "Act Three — The Question"}


def harvest():
    """Ordered parts with their elements; speeches carry a global index that
    matches the order the glosses were written in."""
    src = SRC.read_text(encoding="utf-8")
    token = re.compile(
        r'<div class="part-eyebrow"[^>]*>(?P<eye>.*?)</div>'
        r'|<h3 class="part-title"[^>]*>(?P<part>.*?)</h3>'
        r'|<p class="speech">(?P<sp>.*?)</p>'
        r'|<p class="stage"[^>]*>(?P<st>.*?)</p>', re.S)

    def txt(s):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

    seq = []
    act = no = None
    gi = 0
    for m in token.finditer(src):
        if m.group("eye") is not None:
            e = txt(m.group("eye"))
            mm = re.match(r"(Part [IVX]+) of (Act \w+)", e)
            if mm:
                no, act = mm.group(1), ACT_TITLE.get(mm.group(2), mm.group(2))
        elif m.group("part") is not None:
            seq.append({"act": act or "", "part": f"{no} — {txt(m.group('part'))}", "els": []})
        elif not seq:
            continue
        elif m.group("sp") is not None:
            h = (m.group("sp").replace('<span class="speaker">', '<span class="who">')
                              .replace('<span class="action">', '<span class="sd">'))
            seq[-1]["els"].append(("speech", h, gi)); gi += 1
        elif m.group("st") is not None:
            seq[-1]["els"].append(("stage", m.group("st"), None))
    return seq, gi


def build():
    seq, nspeech = harvest()
    glosses = json.loads(GLOSS.read_text(encoding="utf-8"))
    missing = [i for i in range(nspeech) if str(i) not in glosses]
    if missing:
        print(f"WARNING: {len(missing)} speeches without a note: {missing[:15]}")
    else:
        print(f"All {nspeech} speeches have a note.")

    blocks = []
    last_act = None
    for p in seq:
        if p["act"] != last_act:
            blocks.append(f'<h1 class="act">{p["act"]}</h1>')
            last_act = p["act"]
        blocks.append(f'<h2 class="part">{p["part"]}</h2>')
        for kind, htm, gi in p["els"]:
            if kind == "stage":
                blocks.append(f'<p class="stagedir">{htm}</p>')
            else:
                note = glosses.get(str(gi), "")
                blocks.append(
                    f'<div class="unit"><p class="note">{_html.escape(note)}</p>'
                    f'<p class="sp">{htm}</p></div>')
    body = "".join(blocks)

    intro = '''
    <section class="intro">
      <h1 class="title">Reading Edition</h1>
      <p class="sub">The whole play, line by line — and before each line, what it means and what is moving underneath it. Six Characters in Search of an Author · Village Players, Lausanne · dir. Kiarash Jamshidi</p>
      <h3>How to use it</h3>
      <ul>
        <li><strong>Every spoken line carries a note</strong> — the short italic line set just above it, marked by a gold rule. It says what the line is really doing: the intent, the subtext, the move beneath the words.</li>
        <li><strong>The line itself follows, in full.</strong> Stage directions are set in italic between the speeches, as in the script.</li>
        <li><strong>Read it straight through</strong> to follow the play with its undertow exposed, or dip into any part — the notes are written to stand on their own.</li>
        <li>The notes read the play through this production's lens: the Father who turns guilt into philosophy, the Step-Daughter who uses truth as a weapon, the Mother as the silent centre of pain, the Son who refuses to be staged, the Manager who becomes the audience's complicity, and the company who stop laughing.</li>
      </ul>
    </section>'''

    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Reading Edition — Six Characters</title>
<style>
@page {{ size: A4; margin: 13mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:10.5pt; }}
.intro {{ page-break-after: always; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:32pt; color:#8b3a3a; margin:0 0 2mm; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 7mm; font-size:11.5pt; line-height:1.4; }}
.intro h3 {{ font-family:'Cormorant Unicase',serif; font-size:12pt; letter-spacing:0.18em; text-transform:uppercase; color:#8b3a3a; margin:5mm 0 3mm; }}
.intro ul {{ padding-left:6mm; margin:0; }} .intro li {{ margin-bottom:3mm; line-height:1.5; }}
h1.act {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:22pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:4mm 0 3mm; padding-bottom:1mm; page-break-before:always; }}
h2.part {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:11pt; letter-spacing:0.12em;
  text-transform:uppercase; color:#2a201a; margin:5mm 0 3mm; break-after:avoid; }}
.unit {{ break-inside:avoid; page-break-inside:avoid; margin:0 0 3.4mm; }}
.note {{ font-style:italic; font-size:8.7pt; color:#7c6a4f; border-left:2.2px solid #c39a52;
  padding-left:3mm; margin:0 0 1.1mm; line-height:1.38; }}
.sp {{ margin:0; line-height:1.5; }}
.who {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.07em;
  text-transform:uppercase; color:#8b3a3a; }}
.sd {{ font-style:italic; color:#6b5b48; }}
.stagedir {{ font-style:italic; color:#5d513f; margin:3mm 7mm; line-height:1.42; }}
</style></head><body>
{intro}
{body}
</body></html>"""

    doc = _fullbleed.apply(doc, top="13mm", side="13mm")
    out_html = OUT_DIR / "reading_edition.html"
    out_html.write_text(doc)
    out_pdf = OUT_DIR / "reading_edition.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**launch_kwargs)
        pg = b.new_page()
        pg.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=90000)
        pg.wait_for_timeout(800)
        pg.pdf(path=str(out_pdf), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    out_html.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
