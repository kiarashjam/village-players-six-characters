#!/usr/bin/env python3
"""Build the one-page-per-section rehearsal sheet for the Act One deep-dive
evening (the "fourth time" — after the company has already read the whole play
flat and full-emotion).

Three things in one PDF: what we do tonight (step by step), the questions the
director asks (by the six parts of Act One), and what each person should do.
Questions are read from data/table_work_plan.json (Session 1 parts) so this
stays in sync with the plan. A4 cream full-bleed, house style.

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


# ---- The evening, step by step -------------------------------------------
AGENDA = [
    ("18:00", "Welcome &amp; the frame", "Everyone seated. Say it plainly: <em>we have read the whole play twice — flat and over-the-top. Tonight we do not read it again. We take Act One apart: what each line is doing, where the laughs live and die, and how fast it really goes.</em>"),
    ("18:10", "Warm-up", "A short seated voice and breath warm-up."),
    ("18:15", "Name the units", "Go through Act One's six parts. Whenever the room feels <em>something new starts here</em>, stop and agree a short title for that beat — &ldquo;The knock,&rdquo; &ldquo;We want to live,&rdquo; &ldquo;The veil,&rdquo; &ldquo;The hundred francs.&rdquo; Everyone pencils the titles into their script. An actor can't play &ldquo;Act One&rdquo; — they can play &ldquo;The Veil.&rdquo;"),
    ("18:45", "Action the spine", "Teach it in three minutes: for every thought, one strong verb aimed at the other person — <em>I&nbsp;___&nbsp;you</em> (I charm you, I corner you, I warn you, I beg you). Then action four stretches only: the family's arrival (<em>We want to live</em>), the faint and the veil, the Father's Defence (where <em>I&nbsp;explain</em> becomes <em>I&nbsp;plead</em> becomes <em>I&nbsp;attack</em>), and the bargain. Write the verbs in pencil."),
    ("19:25", "Break", "Fifteen minutes. Rest the voice."),
    ("19:40", "The Father's arc, close-up", "Map his four stages — <strong>control &rarr; injury &rarr; attack &rarr; horror</strong> — onto exact lines. Where does control first crack? Where does attack begin? Where does horror flicker? The others say what they see from outside at each stage."),
    ("20:00", "The laugh map", "As a room, mark every script: <strong>&check; laugh here</strong> (the Players, the Manager's dryness); <strong>&#10007; the laugh dies here</strong> (the veil; &ldquo;He calls it pity&rdquo;); <strong>&#9888; danger</strong> (&ldquo;Valentine&rdquo; must land as a wound, not a number). Comedy is timing nine people share — decide it together."),
    ("20:20", "Italian speed-run of Act One", "The whole act, script in hand, <em>as fast as humanly possible</em> — no emotion, no pauses, cues picked up instantly (about 15&ndash;18 minutes). No acting, no stopping, laugh and keep going. It welds the shape into the body, forces everyone to <em>listen</em> for their cue, and shows the act's true speed."),
    ("20:45", "Close", "Go-round: each actor, one sentence — <em>&ldquo;In Act One, I am trying to&nbsp;______.&rdquo;</em> Homework: start getting Act One lines into your head — August opens with Act One. Confirm next: the whole play, one cued read."),
]

# ---- What each person does tonight ---------------------------------------
DUTIES = [
    ("You — the Director", "Run the room; frame each segment. Read first, talk second: ask what they found before giving your reading. Keep the Father off the lecture and on the fight. Protect the laugh map. Do not over-talk — when talk stops earning its keep, move to the speed-run."),
    ("Assistant Director", "Keep the master notes: every unit title agreed, every verb chosen, every &ldquo;who is more real&rdquo; decision. Watch for the tone drifting or energy dropping and flag it. Brief anyone who missed a night."),
    ("Stage Manager", "Time the segments and keep the evening moving. Note the unit titles into the prompt book (pencil). Run the stopwatch on the Italian run and read stage directions aloud where needed."),
    ("The Father", "<strong>This is your evening.</strong> The Defence is the act's centre. Action every thought — panic hidden under intelligence, never a lecture; the argument must escalate, not repeat. Find your four stages: control, injury, attack, horror. End like a man who has just proved the walls of his own cell — not like a man who has won."),
    ("The Step-Daughter", "You are the engine and the moral centre. Action your cuts cold — evidence laid down, not anger screamed. Find the one or two moments the cleverness drops and the hurt shows. &ldquo;Valentine&rdquo; is a wound thrown as a provocation, never a number."),
    ("The Mother", "You are scored around the object and the silence, not around tears. Keep the Child-bundle and the veil doing your listening for you. Your few lines are load-bearing — &ldquo;But you drove me away&rdquo; is the one sentence he can never talk you out of. Say less than you want to."),
    ("The Son", "Your stillness is a presence, not a passivity. You refuse to be in the scene, and every line is a door closing. Save the one crack — &ldquo;somebody must be guilty who did nothing&rdquo; — so it costs something when it comes."),
    ("The Manager", "Play a director first, not a device. You move from &ldquo;throw them out&rdquo; to &ldquo;there may be a play here&rdquo; — earn each step. You also hold the comedy: your dryness sets the laughs, and your patience running out sets the danger. The turn is &ldquo;God help me, it tempts me.&rdquo;"),
    ("The Players (1 / 2 / 3)", "You begin as bored professionals and recede to the wings as an audience — keep reacting, dry and delighted, so the comedy never leaves the room. Nervous, not punch-line. The joke dies the instant the Mother's grief lands; be the first to feel it."),
]


def build_html(plan):
    s1 = plan["sessions"][0]
    parts = s1.get("parts", [])

    agenda = "".join(
        f'<tr><td class="t">{esc(t)}</td><td class="a"><strong>{a}</strong><br>'
        f'<span class="d">{d}</span></td></tr>'
        for t, a, d in AGENDA)

    # questions grouped by part, each character then their questions
    qparts = []
    for pt in parts:
        groups = []
        for q in pt["questions"]:
            asks = q.get("asks") or [q.get("ask")]
            items = "".join(f"<li>{esc(a)}</li>" for a in asks)
            groups.append(f'<div class="qgrp"><span class="q-to">{esc(q["to"])}</span><ul>{items}</ul></div>')
        qparts.append(
            f'<div class="qpart"><div class="qp-head">{esc(pt["name"])}'
            f'<span class="qp-in">In it: {esc(pt.get("present",""))}</span></div>'
            + "".join(groups) + "</div>")
    questions = "".join(qparts)

    duties = "".join(
        f'<div class="duty"><div class="duty-who">{esc(who)}</div><p>{what}</p></div>'
        for who, what in DUTIES)

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Rehearsal — Act One, In Depth</title>
<style>
@page {{ size:A4; margin:15mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:11pt; line-height:1.5; }}
.eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:11pt;
  letter-spacing:0.22em; text-transform:uppercase; color:#8b3a3a; margin:0 0 2mm; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:33pt;
  color:#8b3a3a; margin:0 0 1mm; line-height:1.05; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 5mm; font-size:12pt; line-height:1.4; }}
.lede {{ background:#f4eeda; border:1px solid rgba(139,58,58,0.3); border-radius:4px;
  padding:3mm 4mm; margin:0 0 6mm; line-height:1.5; }}
h2 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:20pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:7mm 0 3mm; padding-bottom:1mm; break-after:avoid; }}
table.agenda {{ width:100%; border-collapse:collapse; }}
table.agenda td {{ vertical-align:top; padding:1.8mm 0; border-top:1px dotted rgba(42,32,26,0.28); }}
table.agenda td.t {{ width:20mm; font-family:Arial; font-weight:700; font-size:9pt; color:#8b3a3a; white-space:nowrap; }}
table.agenda td.a {{ line-height:1.45; }}
table.agenda td.a .d {{ color:#4a4035; font-size:10.5pt; }}
.qnote {{ font-style:italic; color:#5d513f; margin:0 0 3mm; }}
.qpart {{ break-inside:avoid; margin:0 0 3mm; }}
.qp-head {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:13.5pt; color:#2a201a;
  border-bottom:1px solid rgba(42,32,26,0.22); padding-bottom:0.6mm; margin:0 0 1.4mm; }}
.qp-in {{ float:right; font-family:'EB Garamond',serif; font-style:italic; font-weight:400;
  font-size:9pt; color:#6b5b48; }}
.qgrp {{ break-inside:avoid; margin:0 0 1.4mm; }}
.q-to {{ font-weight:700; color:#8b3a3a; }}
.qgrp ul {{ margin:0.3mm 0 0; padding-left:6mm; }}
.qgrp li {{ font-style:italic; margin-bottom:0.5mm; line-height:1.38; font-size:10.5pt; }}
.duty {{ break-inside:avoid; margin:0 0 2.6mm; padding-left:3mm; border-left:2px solid rgba(139,58,58,0.4); }}
.duty-who {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:13pt; }}
.duty p {{ margin:0.4mm 0 0; line-height:1.46; }}
.foot {{ margin-top:7mm; padding-top:3mm; border-top:1px solid rgba(42,32,26,0.2);
  font-style:italic; color:#6b5b48; line-height:1.45; }}
</style></head><body>

<div class="eyebrow">Rehearsal &middot; the fourth evening</div>
<h1 class="title">Act One, In Depth</h1>
<p class="sub">Six Characters in Search of an Author &middot; Village Players, Lausanne &middot; dir. Kiarash Jamshidi<br>
Everyone seated &middot; scripts and pencils &middot; no staging tonight</p>

<div class="lede">We have already read the whole play twice — once completely flat, once far too big.
<strong>Tonight we do not read it again.</strong> We take Act One apart: what every line is
<em>doing</em>, where the laughs live and die, and how fast the act really goes — so August's
staging has a spine to build on.</div>

<h2>The evening, step by step</h2>
<table class="agenda"><tbody>{agenda}</tbody></table>

<h2>The questions you ask</h2>
<p class="qnote">After the flat read of each part, put these to the characters who appear in it.
Answers in one sentence, in character — then move on. No wrong answers; they are for the actor to
discover, not to perform.</p>
{questions}

<h2>What each person should do tonight</h2>
{duties}

<p class="foot">One rule over all of it: read to discover, not to perform. Nothing anyone tries
tonight is fixed — the performances are found later, on the floor, in August. When the talking
stops helping, stop talking and run it.</p>

</body></html>"""


def build():
    plan = json.loads(DATA.read_text())
    doc = _fullbleed.apply(build_html(plan), top="14mm", side="14mm")
    out_html = OUT_DIR / "rehearsal_act_one.html"
    out_html.write_text(doc)
    out_pdf = OUT_DIR / "rehearsal_act_one.pdf"
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
