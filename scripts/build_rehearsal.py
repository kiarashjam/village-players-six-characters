#!/usr/bin/env python3
"""Build the deepen-and-memorise rehearsal sheet (the "fourth evening" and
beyond) — WHOLE PLAY, not one act.

The company has already read the play flat and full-emotion; this sheet turns
that understanding into memory and a better outcome. One PDF, house style:
  1. how we learn lines (the method, grounded in how memory actually works);
  2. the evening step by step (deepen + drill cues + go off-book + speed-run);
  3. how to learn your lines at home + an off-book timeline;
  4. the questions the director asks, across all three acts (from the plan);
  5. what each person should do.

Questions are read from data/table_work_plan.json so this stays in sync.
Run: python scripts/build_rehearsal_act_one.py
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


METHOD = [
    ("Learn by what you want, not by rote", "A motivated line is half-learned. When you know what your character is <em>doing</em> to the other person in a line — I warn you, I beg you, I corner you — the words come because the intention comes. Lines learned as sound alone fall out under pressure; lines learned as actions hold."),
    ("Learn your cue, not just your line", "The hardest thing to remember is the <em>other</em> person's last few words — that is what tells you to speak. Learn the cue and the line together, always. Half of &ldquo;knowing the play&rdquo; is knowing exactly when you come in."),
    ("Test yourself — don't re-read", "Reading the scene over and over feels like learning and isn't. Read it a few times, then <strong>close the book</strong> and say it from memory; open only when you stick. Testing (active recall) builds far stronger memory than repetition."),
    ("Little and often — space it out", "A scene that feels solid after one long session shows holes after a weekend. Ten minutes a day for a week beats an hour the night before. Space the same material across days and it sets."),
    ("The first-three-words rule", "When you dry in a run, whoever is on book gives you only the <strong>first three words</strong> of the line — never the whole thing. You retrieve the rest yourself. Being handed the line teaches nothing; retrieving it is the memory forming."),
]

AGENDA = [
    ("18:00", "Welcome &amp; the frame", "Seated. Say it plainly: <em>we know the play — tonight we make it stick and start getting it up. We turn understanding into memory: by intention, by cue, and by testing ourselves.</em>"),
    ("18:10", "Warm-up", "Short seated voice and breath warm-up."),
    ("18:15", "The method (5 minutes, then we use it)", "Walk the five rules opposite — learn by objective, learn the cue, test don't re-read, space it, first-three-words. Everyone will practise them tonight and take them home."),
    ("18:20", "Units &amp; actioning — the memory-maker", "On tonight's act, name the units and put one verb per thought (<em>I&nbsp;___&nbsp;you</em>), pencilled in. This is not separate from learning lines — chunked, motivated text is exactly what memory holds. Cover the whole play across these evenings, one act at a time."),
    ("19:00", "The prompted cue-run", "Run the act script-in-hand but focused only on <strong>cue pick-up</strong>: the instant the cue lands, you are in — no gaps. On a dry, the prompter gives the first three words. This drills the joins, which is where runs fall apart."),
    ("19:20", "Break", "Fifteen minutes. Rest the voice."),
    ("19:35", "Off-book attempt — books down", "Put the scripts <strong>down</strong> for the section the company has learned furthest (Act One first). Run it; prompt with first-three-words only. This is the real test — and the fastest way to find the gaps while there is still time to close them."),
    ("20:00", "The Father's arc / the act's spine", "Quick close-up on the evening's hardest thread — for Act One, the Father's <strong>control &rarr; injury &rarr; attack &rarr; horror</strong>. Knowing the shape makes the lines recall themselves in order."),
    ("20:20", "The Italian speed-run", "The whole act, script in hand if needed, <em>as fast as humanly possible</em> — no emotion, no pauses, cues snapped up instantly. It welds the cues and the shape into the body and shows the act's true speed."),
    ("20:40", "Set the plan &amp; close", "Confirm who runs lines with whom this week, and the off-book date for this act. One sentence each: <em>&ldquo;I am trying to&nbsp;______.&rdquo;</em>"),
]

HOME = [
    "Photocopy your scene. Read it aloud three times, thinking only about what you <em>want</em> in each line.",
    "Cover your lines with a card. Read the cue, say your line from memory, then slide the card down to check. Repeat the scene until you get through it clean once.",
    "Do it again the next day, and the next — ten minutes each. Spacing is what makes it stick.",
    "Learn the <strong>cue</strong> with every line: whoever runs lines with you reads only the cues; you supply the lines.",
    "Record the other parts (leave gaps for yours) on your phone and run it walking to work. Motion helps memory.",
    "When you dry, get only the first three words — then retrieve the rest. Never read the whole line back.",
]

# Off-book timeline (staging block opens 20 Aug)
TIMELINE = [
    ("Act One", "off book for the first staging call — it opens the August block"),
    ("Act Two", "off book two weeks after Act One"),
    ("Act Three", "off book two weeks after Act Two — the shortest, learned last"),
    ("Whole play", "secure and running well before the first full run"),
]

DUTIES = [
    ("You — the Director", "Rehearse by unit name (&ldquo;again, from The Veil&rdquo;) — it trains the company's memory as much as yours. Read first, talk second. Enforce the first-three-words rule so no one gets handed a line. Keep the Father off the lecture and on the fight."),
    ("Assistant Director", "Keep the master notes: units named, verbs chosen. Track who is off-book where, so the director knows which scenes can lose the books next week. Flag energy or tone drifting."),
    ("Stage Manager / on book", "Hold the prompt book and give <strong>only the first three words</strong> on a dry — never the whole line. Note the units into the book. Time the segments; run the stopwatch on the Italian run."),
    ("The Father", "The biggest load in the play — start now. Learn by your four stages (control, injury, attack, horror): the shape is your memory-map. Action every thought so the Defence plays as panic, not a lecture. Aim to be off-book on Act One first."),
    ("The Step-Daughter", "The engine and the second-biggest part. Action your cuts cold — evidence, not screaming. Learn your cues off the Father especially; your speed of attack depends on snapping in on his last words. &ldquo;Valentine&rdquo; is a wound, not a number."),
    ("The Mother", "Fewer lines, but each is load-bearing and easy to throw away — learn them by what they cost you, not by rote. &ldquo;But you drove me away&rdquo; is the sentence he can never talk you out of. Scored around the object and the veil; say less than you want to."),
    ("The Son", "Stillness is a presence, not a passivity — every line a door closing. Learn the cues that drag you in against your will. Save the one crack — &ldquo;somebody must be guilty who did nothing.&rdquo;"),
    ("The Manager", "The most lines and the most cues in the play — you drive the tempo, so your cue pick-up sets everyone's. Play a director first. Earn the move from &ldquo;throw them out&rdquo; to &ldquo;God help me, it tempts me.&rdquo; You also hold the comedy timing."),
    ("Madame Pace", "Only in Act Two, but a full arc in one scene — comic on arrival, chilling by the exit. Learn the broken English exactly as written; the rhythm is the character, and a half-learned accent reads as a mistake, not a choice."),
    ("The Players (1 / 2 / 3)", "You carry many small cues that keep the machine moving — learn them tight, because a missed Player cue leaves a hole in front of the family's scene. Nervous, not punch-line; be the first to feel the joke die."),
]


def build_html(plan):
    agenda = "".join(
        f'<tr><td class="t">{esc(t)}</td><td class="a"><strong>{a}</strong><br>'
        f'<span class="d">{d}</span></td></tr>' for t, a, d in AGENDA)
    method = "".join(
        f'<div class="m"><div class="m-h">{esc(n)}</div><p>{d}</p></div>' for n, d in METHOD)
    home = "".join(f"<li>{h}</li>" for h in HOME)
    timeline = "".join(
        f'<tr><td class="tl-w">{esc(w)}</td><td>{esc(d)}</td></tr>' for w, d in TIMELINE)
    duties = "".join(
        f'<div class="duty"><div class="duty-who">{esc(w)}</div><p>{d}</p></div>' for w, d in DUTIES)

    # questions across all three acts
    acts = []
    for i, act_label in [(0, "Act One"), (1, "Act Two"), (2, "Act Three")]:
        s = plan["sessions"][i]
        qparts = []
        for pt in s.get("parts", []):
            groups = []
            for q in pt["questions"]:
                asks = q.get("asks") or [q.get("ask")]
                items = "".join(f"<li>{esc(a)}</li>" for a in asks)
                groups.append(f'<div class="qgrp"><span class="q-to">{esc(q["to"])}</span><ul>{items}</ul></div>')
            qparts.append(
                f'<div class="qpart"><div class="qp-head">{esc(pt["name"])}'
                f'<span class="qp-in">In it: {esc(pt.get("present",""))}</span></div>'
                + "".join(groups) + "</div>")
        acts.append(f'<h3 class="qact">{esc(act_label)}</h3>' + "".join(qparts))
    questions = "".join(acts)

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Rehearsal — Deepen &amp; Memorise</title>
<style>
@page {{ size:A4; margin:15mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:11pt; line-height:1.5; }}
.eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:11pt;
  letter-spacing:0.22em; text-transform:uppercase; color:#8b3a3a; margin:0 0 2mm; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:32pt;
  color:#8b3a3a; margin:0 0 1mm; line-height:1.05; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 5mm; font-size:12pt; line-height:1.4; }}
.lede {{ background:#f4eeda; border:1px solid rgba(139,58,58,0.3); border-radius:4px;
  padding:3mm 4mm; margin:0 0 6mm; line-height:1.5; }}
h2 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:20pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:7mm 0 3mm; padding-bottom:1mm; break-after:avoid; }}
h3.qact {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:12pt; letter-spacing:0.1em;
  text-transform:uppercase; color:#8b3a3a; margin:4mm 0 2mm; break-after:avoid; }}
.m {{ break-inside:avoid; margin:0 0 2.4mm; padding-left:3mm; border-left:2px solid rgba(139,58,58,0.4); }}
.m-h {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:12.5pt; }}
.m p {{ margin:0.3mm 0 0; line-height:1.45; }}
table.agenda {{ width:100%; border-collapse:collapse; }}
table.agenda td {{ vertical-align:top; padding:1.7mm 0; border-top:1px dotted rgba(42,32,26,0.28); }}
table.agenda td.t {{ width:20mm; font-family:Arial; font-weight:700; font-size:9pt; color:#8b3a3a; white-space:nowrap; }}
table.agenda td.a .d {{ color:#4a4035; font-size:10.5pt; }}
.home {{ background:#f4eeda; border:1px solid rgba(42,32,26,0.2); border-radius:4px; padding:2mm 5mm 2mm 8mm; }}
.home li {{ margin-bottom:1.4mm; line-height:1.45; }}
table.tl {{ width:100%; border-collapse:collapse; margin-top:2mm; }}
table.tl td {{ padding:1.4mm 0; border-top:1px dotted rgba(42,32,26,0.25); vertical-align:top; line-height:1.4; }}
table.tl .tl-w {{ width:34mm; font-weight:700; color:#8b3a3a; }}
.qnote {{ font-style:italic; color:#5d513f; margin:0 0 2mm; }}
.qpart {{ break-inside:avoid; margin:0 0 2.4mm; }}
.qp-head {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:12.5pt; color:#2a201a;
  border-bottom:1px solid rgba(42,32,26,0.22); padding-bottom:0.5mm; margin:0 0 1.2mm; }}
.qp-in {{ float:right; font-style:italic; font-weight:400; font-size:8.6pt; color:#6b5b48; }}
.qgrp {{ break-inside:avoid; margin:0 0 1.2mm; }}
.q-to {{ font-weight:700; color:#8b3a3a; }}
.qgrp ul {{ margin:0.2mm 0 0; padding-left:6mm; }}
.qgrp li {{ font-style:italic; margin-bottom:0.4mm; line-height:1.35; font-size:10pt; }}
.duty {{ break-inside:avoid; margin:0 0 2.4mm; padding-left:3mm; border-left:2px solid rgba(139,58,58,0.4); }}
.duty-who {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:12.5pt; }}
.duty p {{ margin:0.3mm 0 0; line-height:1.45; }}
.foot {{ margin-top:7mm; padding-top:3mm; border-top:1px solid rgba(42,32,26,0.2);
  font-style:italic; color:#6b5b48; line-height:1.45; }}
</style></head><body>

<div class="eyebrow">Rehearsal &middot; deepen &amp; memorise</div>
<h1 class="title">Making It Stick</h1>
<p class="sub">The whole play, act by act &middot; Six Characters in Search of an Author &middot; Village Players, Lausanne &middot; dir. Kiarash Jamshidi<br>
Everyone seated &middot; scripts and pencils &middot; no staging yet</p>

<div class="lede">We have read the play twice — flat, then far too big. <strong>Now we make it stick.</strong>
This is how we turn understanding into memory and get lines into heads the way that actually holds:
by what the character wants, by the cue, and by testing ourselves — not by staring at the page. We
work one act at a time across these evenings; the method is the same for all three.</div>

<h2>How we learn lines — five rules</h2>
{method}

<h2>The evening, step by step</h2>
<table class="agenda"><tbody>{agenda}</tbody></table>

<h2>How to learn your lines at home</h2>
<ol class="home">{home}</ol>

<h2>Off-book timeline</h2>
<table class="tl"><tbody>{timeline}</tbody></table>

<h2>The questions you ask</h2>
<p class="qnote">After the flat read of each part, put these to the characters who appear in it —
one sentence each, in character. Answering them is also how the line gets learned: a line you
know the reason for is a line you can recall.</p>
{questions}

<h2>What each person should do</h2>
{duties}

<p class="foot">Two rules over all of it: test yourself instead of re-reading, and never take the
whole line on a dry — the first three words, then retrieve the rest. Understanding first, then
memory, then the floor in August. Nothing tonight is fixed; it is being learned.</p>

</body></html>"""


def build():
    plan = json.loads(DATA.read_text())
    doc = _fullbleed.apply(build_html(plan), top="14mm", side="14mm")
    out_html = OUT_DIR / "rehearsal_making_it_stick.html"
    out_html.write_text(doc)
    out_pdf = OUT_DIR / "rehearsal_making_it_stick.pdf"
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
