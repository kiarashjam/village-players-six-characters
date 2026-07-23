#!/usr/bin/env python3
"""Build the map for TODAY's table reading — Act One only.

The director's own flow: warm up, then go part by part through Act One; for
each part read it the Italian way (fast, flat, cues snapped up), then action
it line by line (subject-verb-object: "I ___ you"); ask the part's questions;
and finish with a bit of practice. Questions read from
data/table_work_plan.json (Session 1) so it stays in sync.

Run: python scripts/build_today_map.py  ->  outputs/today_act_one_map.pdf
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


# per-part: (when, one-line note, worked example: speaker / real line / action)
PART_EXTRA = {
    "Part I — The Rehearsal":  ("18:15", "The Manager cracks the whip; the Players drag their feet.",
        ("Player 1", "We were drawing perfectly well. …Adequately.", "I save face.")),
    "Part II — The Arrival":   ("18:30", "The Father talks his way in; the Step-Daughter throws &ldquo;Valentine&rdquo; like a stone.",
        ("The Step-Daughter", "We may be your fortune, sir — if you have the nerve for us.", "I dare you.")),
    "Part III — The Veil":     ("18:52", "He lifts the veil against her will; she names what he did.",
        ("The Mother", "But you drove me away.", "I correct you.")),
    "Part IV — The Defence":   ("19:25", "The big one — the Father's defence must be a fight, not a lecture.",
        ("The Father", "Words are the whole trouble. Each of us carries a whole world inside him…", "I reason you round.")),
    "Part V — The Hinge":      ("20:00", "The Son shuts every door.",
        ("The Son", "Don't look at me. I don't come into this.", "I shut you out.")),
    "Part VI — The Bargain":   ("20:15", "He sells the tragedy; the Manager buys.",
        ("The Father", "You must be the author. You need not invent us — only give us form.", "I recruit you.")),
}

# The notions we work with tonight (name, what it is / how to do it)
NOTIONS = [
    ("Read to discover, not to perform", "Nothing tonight is a performance — the acting comes in August. We read to <em>find out what is there</em>. Try things, guess, be wrong out loud."),
    ("The Italian way (<em>l'italiana</em>)", "Say the lines as fast as humanly possible — flat, no emotion, no pauses, cues snapped up the instant they land. No acting allowed. It drills the cues (the hardest thing to learn is the <em>other</em> person's last words) and lets us feel the true shape and speed of a scene."),
    ("The action — subject &middot; verb &middot; object", "For each line I call, name what you are doing to the other person as <strong>&ldquo;I&nbsp;___&nbsp;you.&rdquo;</strong> It must fit that frame, so it is always something you <em>do</em> to someone — <em>I warn you, I coax you, I shame you</em> — never a mood (<em>not</em> &ldquo;I am sad&rdquo;) and never an adverb. Feeling comes out of doing."),
    ("One action per thought — not per line", "A long speech turns three or four times. Mark where the verb changes: the Father goes <em>I explain &rarr; I plead &rarr; I attack</em> inside one speech. The turns are the map of the scene."),
    ("Learn the cue with the line", "The Italian way trains this: you come in on the other person's last words, so learn them together. Half of &ldquo;knowing the play&rdquo; is knowing exactly when you speak."),
    ("Let the laugh curdle", "Act One is funny — and then suddenly not. Notice where the room laughs and where the laugh must die (the veil; &ldquo;He calls it pity&rdquo;). Never kill the comedy; let it <em>turn</em>."),
    ("Play each one true", "The Father is panic hidden under intelligence, never a lecture. The Step-Daughter lays down evidence, cold, never screams. The Mother is scored around the object and the silence, not the tears. The Son shuts doors. The Manager is a director first."),
]


def build_html(plan):
    parts = plan["sessions"][0].get("parts", [])
    cards = []
    for pt in parts:
        when, note, ex = PART_EXTRA.get(pt["name"], ("", "", None))
        qs = []
        for q in pt["questions"]:
            asks = q.get("asks") or [q.get("ask")]
            qs.append(f'<span class="q-to">{esc(q["to"])}</span> ' + " / ".join(esc(a) for a in asks))
        qlist = "".join(f"<li>{x}</li>" for x in qs)
        exhtml = ""
        if ex:
            spk, line, act = ex
            exhtml = (f'<div class="ex"><span class="ex-h">Worked example</span> '
                      f'<span class="ex-who">{esc(spk)}:</span> &ldquo;{esc(line)}&rdquo; '
                      f'&nbsp;&rarr;&nbsp; <strong>{esc(act)}</strong></div>')
        cards.append(f"""
<div class="part">
  <div class="p-head"><span class="p-when">{esc(when)}</span><span class="p-name">{esc(pt["name"])}</span></div>
  <div class="p-in">In it: {esc(pt.get("present",""))} &middot; <em>{note}</em></div>
  <div class="step"><span class="n">1</span><strong>Read it the Italian way.</strong> The whole part, script in hand, as fast as you can — flat, no emotion, no pauses, cues snapped up the instant they land.</div>
  <div class="step"><span class="n">2</span><strong>Action it — line by line.</strong> For each line I point to, say what you are doing to the other person as <em>subject &ndash; verb &ndash; object</em>: <strong>&ldquo;I&nbsp;___&nbsp;you.&rdquo;</strong> One strong verb per thought, pencilled in.</div>
  {exhtml}
  <div class="ask"><span class="ask-h">Ask (one sentence, in character):</span><ul>{qlist}</ul></div>
</div>""")
    cards_html = "".join(cards)
    notions = "".join(
        f'<div class="notion"><div class="notion-h">{n}</div><p>{d}</p></div>' for n, d in NOTIONS)

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Today — Act One Table Reading</title>
<style>
@page {{ size:A4; margin:15mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:11pt; line-height:1.5; }}
.eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:11pt;
  letter-spacing:0.22em; text-transform:uppercase; color:#8b3a3a; margin:0 0 2mm; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:33pt;
  color:#8b3a3a; margin:0 0 1mm; line-height:1.04; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 5mm; font-size:12pt; line-height:1.4; }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:3mm 6mm; margin:0 0 6mm; }}
.box {{ background:#f4eeda; border:1px solid rgba(139,58,58,0.3); border-radius:4px; padding:3mm 4mm; line-height:1.46; }}
.box h4 {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.12em;
  text-transform:uppercase; color:#8b3a3a; margin:0 0 1.5mm; }}
h2 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:19pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:6mm 0 3mm; padding-bottom:1mm; break-after:avoid; }}
.plain {{ margin:0 0 4mm; }}
.notion {{ break-inside:avoid; margin:0 0 2.4mm; padding-left:3mm; border-left:2px solid rgba(139,58,58,0.4); }}
.notion-h {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:12.5pt; }}
.notion p {{ margin:0.3mm 0 0; line-height:1.45; }}
.ex {{ margin:0 0 1.4mm 8mm; padding:1.6mm 3mm; background:#f4eeda; border:1px solid rgba(42,32,26,0.2);
  border-radius:3px; line-height:1.44; font-size:10pt; }}
.ex-h {{ font-family:Arial; font-weight:700; font-size:7.4pt; letter-spacing:0.4px; color:#fff; background:#8b3a3a;
  border-radius:2px; padding:0.5mm 1.6mm; margin-right:1.5mm; }}
.ex-who {{ font-weight:700; color:#8b3a3a; }}
.part {{ break-inside:avoid; margin:0 0 4mm; padding:0 0 2mm; border-bottom:1px dotted rgba(42,32,26,0.3); }}
.p-head {{ display:flex; align-items:baseline; gap:4mm; }}
.p-when {{ font-family:Arial; font-weight:700; font-size:9pt; color:#8b3a3a; white-space:nowrap; }}
.p-name {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:16pt; }}
.p-in {{ font-style:italic; color:#5d513f; font-size:9.5pt; margin:0 0 1.6mm; }}
.step {{ margin:0 0 1.4mm; padding-left:8mm; text-indent:-8mm; line-height:1.46; }}
.step .n {{ display:inline-block; width:5mm; height:5mm; line-height:5mm; text-align:center; margin-right:2mm;
  background:#8b3a3a; color:#fff; border-radius:50%; font-family:Arial; font-weight:700; font-size:8pt; text-indent:0; }}
.ask {{ margin:1mm 0 0 8mm; }}
.ask-h {{ font-family:Arial; font-weight:700; font-size:7.6pt; letter-spacing:0.4px; color:#fff; background:#9a8f78;
  border-radius:2px; padding:0.5mm 1.8mm; }}
.ask ul {{ margin:1.4mm 0 0; padding-left:5mm; }}
.ask li {{ margin-bottom:0.6mm; line-height:1.4; font-size:10pt; }}
.q-to {{ font-weight:700; color:#8b3a3a; }}
.foot {{ margin-top:5mm; padding-top:3mm; border-top:1px solid rgba(42,32,26,0.2); font-style:italic; color:#6b5b48; line-height:1.45; }}
</style></head><body>

<div class="eyebrow">Today &middot; table reading &middot; Act One</div>
<h1 class="title">The Map for Tonight</h1>
<p class="sub">Act One only &middot; everyone seated &middot; scripts and pencils &middot; Six Characters &middot; Village Players &middot; dir. Kiarash Jamshidi</p>

<div class="two">
  <div class="box"><h4>The two moves, each part</h4>
    <strong>1 &middot; The Italian way.</strong> Fast, flat, no emotion, no stopping — it drills the cues and lets us hear the shape.<br>
    <strong>2 &middot; The action.</strong> For each line I call, say <strong>&ldquo;I&nbsp;___&nbsp;you&rdquo;</strong> — subject, verb, object. One verb per thought. Feeling comes out of doing.</div>
  <div class="box"><h4>Order of the evening</h4>
    Warm up &rarr; then the six parts in order, each read the Italian way then actioned &rarr; a short break after The Veil &rarr; finish with a bit of practice.</div>
</div>

<h2>The notions we are working with</h2>
{notions}

<h2>Warm-up &nbsp;·&nbsp; 18:00</h2>
<p class="plain">Ten to fifteen minutes, seated: voice and breath. Loosen the tongue for the fast reading to come. Then we begin, part by part.</p>

<h2>Part by part</h2>
{cards_html}

<h2>A bit of practice &nbsp;·&nbsp; 20:35</h2>
<p class="plain">To finish: pick one or two parts and run them once more — still seated — this time <em>playing the actions</em> we found, at a normal pace, cues tight. Not a performance; just a taste of the scene standing on its own feet, so everyone leaves with the act in the body. Then a go-round: one sentence each — <em>&ldquo;In Act One, I am trying to&nbsp;______.&rdquo;</em></p>

<p class="foot">Break after The Veil (about 19:10). We are reading to discover, not to perform — nothing is fixed tonight. The staging comes in August; tonight is the words, the cues, and the actions under them.</p>

</body></html>"""


def build():
    plan = json.loads(DATA.read_text())
    doc = _fullbleed.apply(build_html(plan), top="14mm", side="14mm")
    out_html = OUT_DIR / "today_act_one_map.html"
    out_html.write_text(doc)
    out_pdf = OUT_DIR / "today_act_one_map.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        kw = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**kw)
        pg = b.new_page()
        pg.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(700)
        pg.pdf(path=str(out_pdf), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    out_html.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
