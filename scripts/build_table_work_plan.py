#!/usr/bin/env python3
"""Build the Table-Work Plan PDF — "The Round of Readings".

A researched, bespoke plan for the five table-read evenings (Thu 2/9/16/23/30
July 2026, 18:00–21:00, SSA Lausanne) before the staging block. Content is
data-driven from data/table_work_plan.json (produced by the research
workflow); this script only renders it in the house style.

A4 portrait, cream full-bleed. Run: python scripts/build_table_work_plan.py
"""
import os, json, html as _html
from pathlib import Path
import _fullbleed

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", ROOT / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
DATA = Path(os.environ.get("PLAN_JSON", ROOT / "data" / "table_work_plan.json"))
CHROMIUM = os.environ.get("CHROMIUM_PATH")


def esc(s):
    return _html.escape(str(s), quote=False)


def paras(text):
    """Split a text blob on blank lines into <p> paragraphs."""
    blocks = [b.strip() for b in str(text).split("\n\n") if b.strip()]
    if not blocks:
        blocks = [str(text).strip()]
    return "".join(f"<p>{esc(b)}</p>" for b in blocks)


def ul(items, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f"<ul{c}>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def build_html(plan):
    sessions = plan["sessions"]

    # --- at-a-glance map of the five evenings
    glance = "".join(
        f'<div class="glance-card"><div class="g-date">{esc(s["date"])}</div>'
        f'<div class="g-title">{esc(s["title"])}</div>'
        f'<div class="g-focus">{esc(s["focus"])}</div></div>'
        for s in sessions)

    # --- principles
    principles = "".join(
        f'<div class="prin"><h3>{esc(p["name"])}</h3>'
        f'<p class="what">{esc(p["what"])}</p>'
        f'<p class="why"><span class="lbl">WHY</span> {esc(p["why"])}</p></div>'
        for p in plan["principles"])

    # --- sessions
    sec = []
    for n, s in enumerate(sessions, 1):
        agenda = "".join(
            f'<tr><td class="t">{esc(a["time"])}</td>'
            f'<td class="a"><strong>{esc(a["activity"])}</strong><br>'
            f'<span class="d">{esc(a["detail"])}</span></td></tr>'
            for a in s["agenda"])
        exercises = "".join(
            f'<div class="ex"><div class="ex-name">{esc(e["name"])}</div>'
            f'<p class="ex-how">{esc(e["how"])}</p>'
            f'<p class="ex-purpose"><span class="lbl">YIELDS</span> {esc(e["purpose"])}</p></div>'
            for e in s["exercises"])
        prompts = ul(s["discussion_prompts"], "prompts")
        parts = s.get("parts")
        if parts:
            cards = "".join(
                f'<div class="part"><div class="part-h">'
                f'<span class="part-when">{esc(pt["when"])}</span>'
                f'<span class="part-name">{esc(pt["name"])}</span></div>'
                f'<div class="part-present">In it: {esc(pt["present"])}</div>'
                '<ul class="qs">'
                + "".join(f'<li><span class="q-to">{esc(q["to"])}</span> — {esc(q["ask"])}</li>'
                          for q in pt["questions"])
                + "</ul></div>"
                for pt in parts)
            parts_html = (
                '<h4>Part by part — read it flat, then ask</h4>'
                '<p class="parts-note">After the flat read of each part, put these questions to the '
                'characters who appear in it. One sentence each, in role — then move on.</p>'
                f'<div class="parts">{cards}</div>')
        else:
            parts_html = ""
        sec.append(f"""
<section class="session">
  <div class="s-head">
    <span class="s-num">Session {n}</span>
    <span class="s-date">{esc(s['date'])}</span>
  </div>
  <h2>{esc(s['title'])}</h2>
  <p class="s-focus">{esc(s['focus'])}</p>

  <h4>Goals for the evening</h4>
  {ul(s['goals'])}

  <h4>The evening, hour by hour</h4>
  <table class="agenda"><tbody>{agenda}</tbody></table>

  {parts_html}

  <h4>Exercises at the table</h4>
  {exercises}

  <h4>Questions to put to the room</h4>
  {prompts}

  <div class="hw"><span class="lbl">HOMEWORK</span> {esc(s['homework'])}</div>
  <div class="outcome"><span class="lbl">BY THE END</span> {esc(s['outcome'])}</div>
</section>""")
    sessions_html = "".join(sec)

    sources = "".join(
        f'<li><strong>{esc(x["title"])}</strong>'
        + (f' — {esc(x["author"])}' if x.get("author") else "")
        + (f'. <span class="src-note">{esc(x["note"])}</span>' if x.get("note") else "")
        + "</li>"
        for x in plan["sources"])

    hr = plan["how_to_run"]

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>The Round of Readings — Table-Work Plan — Six Characters</title>
<style>
@page {{ size: A4; margin: 14mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:11pt; line-height:1.5; }}
.eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:11pt;
  letter-spacing:0.22em; text-transform:uppercase; color:#8b3a3a; margin:0 0 2mm; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:34pt;
  color:#8b3a3a; margin:0 0 1mm; line-height:1.04; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 5mm; font-size:12pt; line-height:1.4; }}
.lede {{ margin:0 0 6mm; }}
.lede p {{ margin:0 0 2.6mm; line-height:1.5; }}
h2 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:21pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:2mm 0 2mm; padding-bottom:1mm; break-after:avoid; }}
h3 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:13.5pt; color:#2a201a;
  margin:3mm 0 1mm; break-after:avoid; }}
h4 {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.12em;
  text-transform:uppercase; color:#8b3a3a; margin:4mm 0 1.5mm; break-after:avoid; }}
.section-title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:21pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:7mm 0 3mm; padding-bottom:1mm; break-after:avoid; }}
ul {{ margin:0 0 3mm; padding-left:6mm; }}
li {{ margin-bottom:1.6mm; line-height:1.46; }}
.lbl {{ font-family:Arial; font-weight:700; font-size:6.8pt; letter-spacing:0.6px; color:#fff;
  background:#9a8f78; border-radius:2px; padding:0.6mm 1.8mm; vertical-align:1.5px; margin-right:1.5mm; }}

/* how-we-run grid */
.run {{ display:grid; grid-template-columns:1fr 1fr; gap:3mm 6mm; margin:0 0 4mm; }}
.run .box {{ break-inside:avoid; }}
.run .cadence {{ grid-column:1 / -1; background:#f4eeda; border:1px solid rgba(139,58,58,0.3);
  border-radius:3px; padding:3mm 3.5mm; line-height:1.46; }}

/* at-a-glance */
.glance {{ display:grid; grid-template-columns:repeat(5,1fr); gap:2.5mm; margin:0 0 5mm; }}
.glance-card {{ background:#f4eeda; border:1px solid rgba(42,32,26,0.18); border-radius:4px;
  padding:2.6mm 2.4mm; break-inside:avoid; }}
.g-date {{ font-family:Arial; font-weight:700; font-size:7.2pt; letter-spacing:0.4px; color:#8b3a3a;
  text-transform:uppercase; margin-bottom:1mm; }}
.g-title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:12pt; line-height:1.1;
  margin-bottom:1.4mm; }}
.g-focus {{ font-size:8.6pt; color:#5d513f; line-height:1.34; }}

/* principles */
.prin {{ break-inside:avoid; margin:0 0 2.6mm; padding-bottom:2mm; border-bottom:1px dotted rgba(42,32,26,0.25); }}
.prin h3 {{ margin:0 0 0.8mm; }}
.prin .what {{ margin:0 0 1mm; line-height:1.46; }}
.prin .why {{ margin:0; color:#4a4035; font-size:10.5pt; line-height:1.44; }}

/* sessions */
.session {{ break-before:page; padding-top:1mm; }}
.session:first-of-type {{ break-before:auto; }}
.s-head {{ display:flex; align-items:baseline; gap:4mm; margin-bottom:0.5mm; }}
.s-num {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10.5pt; letter-spacing:0.16em;
  text-transform:uppercase; color:#8b3a3a; }}
.s-date {{ font-family:Arial; font-weight:700; font-size:8.4pt; letter-spacing:0.4px; color:#6b5b48; }}
.session h2 {{ margin-top:0; }}
.s-focus {{ font-style:italic; color:#5d513f; margin:0 0 1mm; line-height:1.44; }}
table.agenda {{ width:100%; border-collapse:collapse; margin:0 0 2mm; }}
table.agenda td {{ vertical-align:top; padding:1.5mm 0; border-top:1px dotted rgba(42,32,26,0.25); }}
table.agenda td.t {{ width:26mm; font-family:Arial; font-weight:700; font-size:8.6pt; color:#8b3a3a;
  white-space:nowrap; padding-right:3mm; }}
table.agenda td.a {{ line-height:1.42; }}
table.agenda td.a .d {{ color:#5d513f; font-size:10pt; }}
.ex {{ break-inside:avoid; margin:0 0 2.2mm; padding-left:3mm; border-left:2px solid rgba(139,58,58,0.4); }}
.ex-name {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:12pt; }}
.ex-how {{ margin:0.4mm 0 0.8mm; line-height:1.44; }}
.ex-purpose {{ margin:0; color:#4a4035; font-size:10pt; line-height:1.4; }}
.prompts li {{ font-style:italic; }}
.hw, .outcome {{ break-inside:avoid; border-radius:3px; padding:2.4mm 3mm; margin:2.5mm 0 0; line-height:1.46; }}
.hw {{ background:#f4eeda; border:1px solid rgba(42,32,26,0.2); }}
.outcome {{ background:#efe2d0; border:1px solid rgba(139,58,58,0.4); }}

.sources li {{ line-height:1.42; }}
.src-note {{ font-style:italic; color:#5d513f; }}
.parts-note {{ font-style:italic; color:#5d513f; margin:0 0 2mm; font-size:10pt; line-height:1.4; }}
.parts {{ margin:0 0 2mm; }}
.part {{ break-inside:avoid; margin:0 0 2.6mm; padding:2mm 0 0; border-top:1px dotted rgba(42,32,26,0.28); }}
.part-h {{ display:flex; align-items:baseline; gap:3mm; flex-wrap:wrap; }}
.part-when {{ font-family:Arial; font-weight:700; font-size:8pt; letter-spacing:0.3px; color:#8b3a3a; white-space:nowrap; }}
.part-name {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:12.5pt; }}
.part-present {{ font-size:9.4pt; color:#5d513f; margin:0.3mm 0 1mm; }}
.qs {{ margin:0; padding-left:5mm; }}
.qs li {{ margin-bottom:1mm; line-height:1.4; font-size:10.5pt; }}
.q-to {{ font-weight:700; color:#2a201a; }}
.foot {{ margin-top:7mm; padding-top:3mm; border-top:1px solid rgba(42,32,26,0.2);
  font-style:italic; color:#6b5b48; line-height:1.45; }}
</style></head><body>

<div class="eyebrow">The Round of Readings · Table-Work Plan</div>
<h1 class="title">Five Evenings at the Table</h1>
<p class="sub">Before we stand up: reading, given circumstances, character and scene work for
<em>Six Characters in Search of an Author</em> · Village Players, Lausanne · dir. Kiarash Jamshidi<br>
Thursdays 2 · 9 · 16 · 23 · 30 July 2026 · 18:00–21:00 · SSA Lausanne</p>

<div class="lede">{paras(plan['method_overview'])}</div>

<h2>The five evenings at a glance</h2>
<div class="glance">{glance}</div>

<h2>How we run the room</h2>
<div class="run">
  <div class="box"><h4>Ground rules</h4>{ul(hr['room_norms'])}</div>
  <div class="box"><h4>Who does what</h4>{ul(hr['roles'])}</div>
  <div class="box"><h4>Bring to every session</h4>{ul(hr['materials'])}</div>
  <div class="box"><h4>Shape of an evening</h4><p style="margin:0;line-height:1.46;">{esc(hr['cadence'])}</p></div>
  <div class="cadence"><span class="lbl">REMEMBER</span> Table work serves the floor — we read to discover, not to perform, and we get up the moment talk stops earning its keep.</div>
</div>

<h2>The methods we use</h2>
{principles}

<h1 class="section-title">The Sessions</h1>
{sessions_html}

<h2>Traps to avoid</h2>
{ul(plan['pitfalls'])}

<h2>Where this comes from — further reading</h2>
<ul class="sources">{sources}</ul>

<p class="foot">This plan is a researched scaffold, not a script for the evenings. Sessions may run
longer or shorter inside the 18:00–21:00 window depending on the room; the architecture is what
matters — each Thursday lays one course of the wall the August staging block will build on.</p>

</body></html>"""


def build():
    plan = json.loads(DATA.read_text())
    doc = _fullbleed.apply(build_html(plan), top="14mm", side="14mm")
    out_html = OUT_DIR / "table_work_plan.html"
    out_html.write_text(doc)
    out_pdf = OUT_DIR / "table_work_plan.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**launch_kwargs)
        pg = b.new_page()
        pg.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(700)
        pg.pdf(path=str(out_pdf), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    out_html.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
