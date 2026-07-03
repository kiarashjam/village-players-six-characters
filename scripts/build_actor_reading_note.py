#!/usr/bin/env python3
"""Build the actor-facing handout: "Table Readings — The Plan".

A short, warm one/two-page note to share with the whole company, so everyone
knows what the five table-reading evenings are and how they work. Deliberately
simpler than the director's table-work plan: no method jargon, no agendas.
Dates are read from data/table_work_plan.json so the two documents stay in sync.

A4 portrait, cream full-bleed. Run: python scripts/build_actor_reading_note.py
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


def short_date(d):
    # "Thursday 2 July 2026" -> "Thu 2 July"
    d = d.replace("Thursday", "Thu").replace(" 2026", "")
    return d.strip()


# Friendly one-line label for each of the five evenings, by order.
EVENING_LABELS = [
    "Act One — and we settle in: how we work, and the world of the play.",
    "Act Two.",
    "Act Three.",
    "The whole play, joined up — how it all connects.",
    "A full read with the cues — then we are ready for the floor in August.",
]


def build_html(plan):
    dates = [short_date(s["date"]) for s in plan["sessions"]]
    evenings = "".join(
        f'<div class="ev"><span class="ev-date">{esc(d)}</span>'
        f'<span class="ev-what">{esc(lab)}</span></div>'
        for d, lab in zip(dates, EVENING_LABELS))

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Table Readings — The Plan — for the company</title>
<style>
@page {{ size: A4; margin: 16mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:11.5pt; line-height:1.55; }}
.eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:11pt;
  letter-spacing:0.22em; text-transform:uppercase; color:#8b3a3a; margin:0 0 2mm; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:34pt;
  color:#8b3a3a; margin:0 0 1mm; line-height:1.05; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 6mm; font-size:12pt; line-height:1.4; }}
p {{ margin:0 0 3mm; }}
h2 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:17pt; color:#8b3a3a;
  margin:6mm 0 2mm; break-after:avoid; }}
ul {{ margin:0 0 3mm; padding-left:6mm; }}
li {{ margin-bottom:1.6mm; line-height:1.5; }}
.when {{ background:#f4eeda; border:1px solid rgba(42,32,26,0.18); border-radius:4px;
  padding:3mm 4mm; margin:0 0 5mm; line-height:1.5; }}
.ev {{ display:flex; gap:4mm; padding:2mm 0; border-top:1px dotted rgba(42,32,26,0.28); break-inside:avoid; }}
.ev:first-child {{ border-top:none; }}
.ev-date {{ flex:0 0 26mm; font-family:Arial; font-weight:700; font-size:9.5pt; color:#8b3a3a;
  white-space:nowrap; padding-top:0.6mm; }}
.ev-what {{ line-height:1.45; }}
.hold {{ background:#efe2d0; border:1px solid rgba(139,58,58,0.45); border-radius:4px;
  padding:3mm 4mm; margin:5mm 0 0; line-height:1.5; }}
.hold strong {{ color:#8b3a3a; }}
.foot {{ margin-top:7mm; padding-top:3mm; border-top:1px solid rgba(42,32,26,0.2);
  font-style:italic; color:#6b5b48; line-height:1.45; }}
</style></head><body>

<div class="eyebrow">For the company</div>
<h1 class="title">Table Readings — The Plan</h1>
<p class="sub">Six Characters in Search of an Author · Village Players, Lausanne · dir. Kiarash Jamshidi</p>

<p>Before we get on our feet in August, we spend five Thursday evenings sitting round a table,
reading the play together. This is where we get to know the play — and each other — with
no pressure at all to &ldquo;perform.&rdquo; Come as you are.</p>

<h2>When &amp; where</h2>
<div class="when"><strong>Five Thursdays — {esc(dates[0])} · {esc(dates[1])} · {esc(dates[2])} · {esc(dates[3])} · {esc(dates[4])}</strong><br>
18:00–21:00 at SSA Lausanne. There is a proper break each evening.</div>

<h2>How each evening works</h2>
<ul>
  <li><strong>We read an act, then talk about it.</strong> No staging, no moving — we stay at the table.</li>
  <li><strong>Two reads of the main scenes.</strong> First completely <em>flat</em> — no acting, just the words. Then deliberately <em>over-the-top</em> — far too big. Both are meant to be freeing (and a little silly); the honest version comes later, on the floor.</li>
  <li><strong>A few quick questions.</strong> After each part I&rsquo;ll ask the characters in it a short question or two — &ldquo;What do you want here?&rdquo;, &ldquo;What are you hiding?&rdquo; Answer in a sentence, in character. There are no wrong answers.</li>
  <li><strong>We read to discover, not to perform.</strong> Nothing you try is locked in. Play, guess, change your mind.</li>
</ul>

<h2>The five evenings</h2>
{evenings}

<h2>What to bring</h2>
<ul>
  <li><strong>Your own script</strong> — please bring your own copy every week.</li>
  <li><strong>A pencil</strong> — for notes you can rub out as things change.</li>
  <li><strong>A bit of energy</strong> after your day. That&rsquo;s all you need.</li>
</ul>

<div class="hold">This play goes to some dark places, and we look after each other.
If anything is ever too much, just say <strong>&ldquo;hold&rdquo;</strong> — we stop at once, no questions asked and no reason needed.</div>

<p class="foot">See you at the table. Any questions before we start, just ask.</p>

</body></html>"""


def build():
    plan = json.loads(DATA.read_text())
    doc = _fullbleed.apply(build_html(plan), top="15mm", side="15mm")
    out_html = OUT_DIR / "table_reading_for_actors.html"
    out_html.write_text(doc)
    out_pdf = OUT_DIR / "table_reading_for_actors.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**launch_kwargs)
        pg = b.new_page()
        pg.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(600)
        pg.pdf(path=str(out_pdf), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    out_html.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
