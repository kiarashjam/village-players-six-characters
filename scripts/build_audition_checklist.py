#!/usr/bin/env python3
"""Build the Audition Checklist PDF.

A working checklist the director carries through auditions. For each
of the eight cast tracks, one page with checkboxes covering the
reading, the signature beats, the voice/body work, and a notes
section. Plus a cover, an auditioner-info form, and a general
assessment page.

The director ticks boxes during the audition. Each page has the
auditioner's name field at the top so pages don't get mixed up
across multiple auditioners.
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
CHROMIUM = os.environ.get("CHROMIUM_PATH")


# ---------------------------------------------------------------------------
# Per-role checklists
# ---------------------------------------------------------------------------

CHARACTERS = [
    {
        "role": "The Father",
        "tag": "the brain of the family",
        "summary": "A well-educated middle-class man whose intellectual elegance is his shield against shame. The philosophy is autobiographical, disguised as metaphysics. Fighting for his existence, not lecturing.",
        "sections": [
            ("Reading", [
                "Plays him as a man fighting for his existence, not lecturing",
                "Intellectual elegance reads as shield against shame",
                "The philosophy lands as autobiographical, not abstract",
                "Mellifluous when controlling the rhythm; violent when it breaks",
                "Believes every paradox in real time",
            ]),
            ("Signature & arc", [
                "The handkerchief appears at moments of greatest shame",
                "Handkerchief out at <em>hundred francs</em>",
                "Handkerchief gripped at <em>proof that I am a man</em>",
                "Four-stage arc visible: control → injury → attack → horror",
                "<em>Can you tell me who you are?</em> — turns out to the house",
                "<em>Because I suffer, sir</em> — the cry breaks through philosophy",
                "<em>Our reality cannot change</em> — closing stillness is paralysis, not composure",
            ]),
            ("Voice & body", [
                "Voice carries the long speeches without strain",
                "Listens to the Step-Daughter as she cuts him",
                "Does not anticipate the Step-Daughter's attacks",
                "Comfortable with stillness",
                "Comfortable with the Step-Daughter's proximity inside the intimacy protocol",
            ]),
        ],
    },
    {
        "role": "The Mother",
        "tag": "silence that finally screams",
        "summary": "Silence is her language. The body does her acting — hands, veil, the bundle, the chair-and-coat. The keystone line <em>It's taking place now</em> must land like a stone learning to speak.",
        "sections": [
            ("Reading", [
                "Heavy under the veil — the veil does her listening for her",
                "Not crushed in the sentimental way; pressed down for so long it has lost the muscle for its own posture",
                "Three silences distinguishable (Act 1 / Act 2 / Act 3)",
                "Holds both children at once in Act 3 — the bundle and the chair-and-coat",
            ]),
            ("Signature & arc", [
                "Hands score the part: grip tightens at <em>illusion</em>, at <em>reality</em>, at <em>he always knew exactly where to find me</em>",
                "The veil — lifted once by the Father against her will; lifted once on her own at the fountain",
                "Eyes mostly on the floor",
                "<em>It's taking place now. It happens all the time</em> — lands like a stone learning to speak",
                "<em>My son! My son!</em> — the voice has been waiting an entire production to use itself",
            ]),
            ("Voice & body", [
                "Available for long stillness without restlessness",
                "Cry (the eruption at Madame Pace, the cry at the fountain) carries without being pushed",
                "Body is specific, not generic",
                "Does not perform sympathy",
            ]),
        ],
    },
    {
        "role": "The Step-Daughter",
        "tag": "the one who refuses to let it be made beautiful",
        "summary": "The moral centre of the play. Sharp, in control, never coquettish. The seduction is exposure, not flirtation. Cuts the Father three times across the philosophy stretch — level, flat, never screamed.",
        "sections": [
            ("Reading", [
                "Sharp, in control, never apologetic, never coquettish",
                "The wit is real; the wit is rage",
                "Refuses to let the Father become the hero of the scene",
                "Tenderness for the Child (bundle) is unbearably real",
                "Contempt for the Boy (chair-and-coat) reads as the same wound, pointed the other way",
            ]),
            ("Signature & arc", [
                "Three cuts against the Father, each colder than the philosophy:",
                "&nbsp;&nbsp;1. <em>His <strong>reality</strong>. He always knew exactly where to find me.</em>",
                "&nbsp;&nbsp;2. <em>He was real that afternoon. With his hundred francs. He was very real.</em>",
                "&nbsp;&nbsp;3. <em>His doesn't change. Mine doesn't either. He should know.</em>",
                "<em>Worse? Listen.</em> — early exposure lands cold, not theatrical",
                "<em>I am dying to live that scene</em> — disgust and revenge in the same beat",
                "<em>Cry out, mother. Cry out as you did then.</em> — physical contact is choreographed and bounded",
            ]),
            ("Voice & body", [
                "Voice level, never raised in the cuts",
                "Holds the bundle as if its stillness depends on her",
                "Available for the intimacy protocol (knows it, has read it)",
                "Comfortable refusing to soften her own line",
            ]),
        ],
    },
    {
        "role": "The Son",
        "tag": "the one who will not act",
        "summary": "The production's most modern figure. The adult child who has been told to show up for a parent's narrative and has decided no. Hands in pockets. Eyes on the floor. The mirror speech surprises him.",
        "sections": [
            ("Reading", [
                "Quiet, cold, with the energy of someone who would leave if he could",
                "Every line is a door closing",
                "Agrees with the author who abandoned them — <em>Exactly what it was, sir; exactly that</em>",
                "Refusal is aesthetic and ethical, not stubbornness",
                "Becomes more himself the more he is held in place",
            ]),
            ("Signature & arc", [
                "Hands in his pockets the entire part",
                "Never looks at the chair-and-coat or the bundle",
                "Looks at the floor, the wall, the wings — not at the Manager unless he has to",
                "The one moment of looking up: <em>Exactly what it was, sir. Exactly that.</em>",
                "<em>Delighted! Delighted!</em> — tries to leave",
                "<em>I act nothing</em> — the body finally still, a kind of dignity arrives",
                "Mirror speech: surprises him on the word <em>horrible</em>, not before",
                "Fountain narration: breaks out of him because he cannot keep it inside any longer",
            ]),
            ("Voice & body", [
                "Stillness reads as presence, not passivity",
                "Voice carries the mirror speech without melodrama",
                "Fountain narration delivered in broken beats",
                "Available for being physically restrained by the Father",
            ]),
        ],
    },
    {
        "role": "The Manager",
        "tag": "the symbol of the audience itself",
        "summary": "The Manager is the audience, concretely. Everything he does is what the audience does in their seats. The clipboard is their program. His verbal tics are their thoughts. He delivers, in the closing line, what they were going to say themselves.",
        "sections": [
            ("Reading", [
                "Plays him as the audience itself, not a director-on-deadline cliché",
                "Cynicism is technique; compassion is real",
                "Almost understands what he is watching; never quite admits it",
                "Not a buffoon",
            ]),
            ("Signature & arc", [
                "The clipboard signature — under the arm, on the table, in the hand",
                "Clipboard goes down on <em>By Jove, it tempts me</em>",
                "Picks it back up when the action becomes unbearable",
                "Audience-like verbal tics: <em>I don't understand at all / Let's hear them out / Damned good / Effect certain</em>",
                "The pivot: stands, picks up the chair-and-coat himself, walks it to the fountain",
                "The closing line played straight — no commentary, no irony",
                "Walks off the stage the way a man leaves a theatre",
            ]),
            ("Voice & body", [
                "Practical, working-director voice — not theatrical",
                "Sits at the table forward, slightly bored, half-engaged — the audience's posture",
                "Almost says <em>Pirandello</em> in Act 3 Part II and stops himself",
                "Available for the long Act 3 stretch without losing energy",
            ]),
        ],
    },
    {
        "role": "Player 1",
        "tag": "one character in five hats — the faded Leading Man",
        "summary": "A once-promising Anglo actor who came to Lausanne thinking it was a stepping stone to Paris. Paris did not happen. Vanity is now a defense mechanism. He plays five roles but always as himself.",
        "sections": [
            ("Reading", [
                "Plays five roles, but always as himself",
                "Anglo English (he thinks of it as classical; audience reads as English)",
                "Vanity is defence; affection underneath",
                "He does not know he is funny",
            ]),
            ("Signature & arc", [
                "The comb signature — small, in the breast pocket",
                "Comb out at <em>I have a reputation in this canton</em>",
                "Comb out as the Door-keeper (out of habit)",
                "Comb out at <em>By me, if you've no objection</em>",
                "Comb pressed to chest like a small cross when Madame Pace materialises",
                "<em>Neither am I. I am through with this scene</em> — two steps toward exit, calculation crosses face, he stops",
                "Plays the Father in the shop scene with practised gallantry",
            ]),
            ("Voice & body", [
                "Carries five distinct hats without losing the spine",
                "Comfortable with comic exposure",
                "Pretentious in his Stanislavski-talk without naming Stanislavski",
                "Available for the shop-scene playing within the intimacy protocol",
            ]),
        ],
    },
    {
        "role": "Player 2",
        "tag": "the diva and the props",
        "summary": "The veteran character actress who actually is what Player 1 pretends to be. Has done leads at every Lausanne house. Knows the audience by name. Also does the props because the budget is small.",
        "sections": [
            ("Reading", [
                "Senior actor in the company — does not need to say so",
                "Diva is real, earned, tired",
                "Property Man is the same woman with the chain raised",
                "Both registers, one body",
            ]),
            ("Signature & arc", [
                "Reading glasses on a long silver chain",
                "Glasses down to inspect a prop, read a cue, give an appraising look",
                "Glasses up when she is being looked at",
                "<em>I insist on being treated with respect — and reasonable lighting — otherwise I go</em>",
                "The wound: the Step-Daughter laughs at her attempt to play the Step-Daughter",
                "<em>I have been made a fool of — believe me — by considerably better</em> — the glasses come off",
                "Act 3: would like to be at home with the cat",
            ]),
            ("Voice & body", [
                "Comfortable flipping between Leading Lady and Property Man inside a single scene",
                "Wounded pride lands without histrionics",
                "Available for the shop-scene playing within the intimacy protocol",
                "Practical, no-nonsense Property Man bearing",
            ]),
        ],
    },
    {
        "role": "Player 3",
        "tag": "the youngest, and Madame Pace",
        "summary": "The earnest one. Carries the Juvenile Lead, the Prompter, and the production's most theatrically demanding moment — Madame Pace, who arrives comic and exits chilling.",
        "sections": [
            ("Reading", [
                "Earnest, genuinely curious about the Characters",
                "Juvenile Lead — the most theatrically open of the three Players",
                "Prompter — meticulous, slightly older, in the box",
                "Madame Pace — comic on arrival, chilling on exit",
            ]),
            ("Signature & arc", [
                "Player 3 transformation is the production's most demanding moment",
                "<em>Buongiorno, buongiorno, signor</em> — comic entry, full theatricality",
                "<em>He clean. He polite. He pay cash</em> — the bookkeeping of shame",
                "Smile never drops; only what she is saying changes",
                "<em>Sì sì, certo. I go. I go.</em> — exit not furious, unhurried",
                "<em>Don't you forget the name. La Pace.</em> — parting threat",
            ]),
            ("Voice & body", [
                "Half-Italian, half-French dialect carried without losing meaning",
                "Audience must laugh on her first line, regret laughing by her last",
                "Available for the wig, the heels, the powder — full physical transformation",
                "Available for the touching protocol with the Step-Daughter (hand under chin, briefly)",
            ]),
        ],
    },
]


# ---------------------------------------------------------------------------
# HTML composition
# ---------------------------------------------------------------------------

CSS = """
@page { size: A4; margin: 18mm 20mm 18mm 20mm; }
*,*::before,*::after { box-sizing: border-box; }
html, body { background: #efe6cf; color: #2a201a; font-family: 'EB Garamond','Georgia','Times New Roman',serif; font-size: 11pt; line-height: 1.55; margin: 0; padding: 0; }
:root { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }
main { max-width: 170mm; margin: 0 auto; }

.cover { padding-top: 22mm; text-align: center; page-break-after: always; }
.cover .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.28em; text-transform:uppercase; color:var(--accent); margin: 0 0 16mm 0; }
.cover h1 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size:34pt; line-height:1.05; margin: 0 0 4mm 0; }
.cover .italian { font-style: italic; color: var(--ink-soft); font-size: 13pt; margin: 0 0 10mm 0; }
.cover .credit { font-size: 11pt; margin: 4mm 0; }
.cover .company { margin-top: 16mm; font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.22em; text-transform:uppercase; }
.cover .instructions { margin-top: 24mm; max-width: 130mm; margin-left: auto; margin-right: auto; text-align: left; }
.cover .instructions h3 { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.18em; text-transform:uppercase; color:var(--accent); margin: 0 0 4mm 0; text-align: center; }
.cover .instructions p { font-size: 10.5pt; line-height: 1.65; margin: 0 0 3mm 0; }

.auditioner-form { padding-top: 6mm; page-break-after: always; }
.auditioner-form h2 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size:22pt; margin: 0 0 6mm 0; }
.auditioner-form h3 { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.18em; text-transform:uppercase; color:var(--accent); margin: 10mm 0 3mm 0; border-bottom: 1px solid var(--rule); padding-bottom: 2mm; }
.field { display: flex; align-items: baseline; gap: 4mm; margin-bottom: 5mm; font-size: 11pt; }
.field .label { font-weight: 600; min-width: 38mm; }
.field .line { flex: 1; border-bottom: 1px solid var(--ink); height: 8mm; }
.field-half { width: 48%; display: inline-flex; align-items: baseline; gap: 4mm; margin-bottom: 5mm; font-size: 11pt; }
.field-half .label { font-weight: 600; }
.field-half .line { flex: 1; border-bottom: 1px solid var(--ink); height: 8mm; }
.fields-row { display: flex; gap: 4%; }

.role-page { page-break-before: always; padding-top: 2mm; }
.role-header { padding-bottom: 4mm; margin-bottom: 5mm; border-bottom: 1px solid var(--rule); }
.role-header .top-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 2mm; font-size: 9.5pt; color: var(--ink-soft); font-family: 'Cormorant Unicase', serif; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; }
.role-header .auditioner-row { display: flex; gap: 5mm; align-items: baseline; margin-bottom: 4mm; font-size: 10pt; }
.role-header .auditioner-row .label { font-weight: 600; min-width: 24mm; }
.role-header .auditioner-row .line { flex: 1; border-bottom: 1px solid var(--ink); height: 5mm; }
.role-header h2 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size: 24pt; margin: 0 0 1mm 0; }
.role-header .tag { font-style: italic; color: var(--ink-soft); font-size: 11pt; margin: 0 0 3mm 0; }
.role-header .summary { font-size: 10pt; line-height: 1.55; margin: 0; color: var(--ink); }

.checklist-section { margin-bottom: 5mm; }
.checklist-section h3 { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9.5pt; letter-spacing:0.18em; text-transform:uppercase; color:var(--accent); margin: 0 0 2mm 0; }
.checklist-section ul { list-style: none; padding: 0; margin: 0; }
.checklist-section li { display: flex; align-items: flex-start; gap: 3mm; margin: 0 0 1.6mm 0; font-size: 10pt; line-height: 1.45; page-break-inside: avoid; }
.checklist-section li .box { display: inline-block; flex-shrink: 0; width: 4mm; height: 4mm; border: 1.2px solid var(--ink); border-radius: 0.5mm; margin-top: 1mm; }

.notes { margin-top: 6mm; }
.notes h3 { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9.5pt; letter-spacing:0.18em; text-transform:uppercase; color:var(--accent); margin: 0 0 2mm 0; }
.notes .lines { background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 5.5mm, var(--rule) 5.5mm, var(--rule) 5.6mm); height: 38mm; }

.verdict { margin-top: 6mm; padding-top: 4mm; border-top: 1px solid var(--rule); display: flex; align-items: center; justify-content: space-between; font-size: 10pt; }
.verdict .label { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9.5pt; letter-spacing:0.18em; text-transform:uppercase; color:var(--accent); }
.verdict .options { display: flex; gap: 6mm; }
.verdict .option { display: flex; align-items: center; gap: 2mm; }
.verdict .option .box { display: inline-block; width: 4.5mm; height: 4.5mm; border: 1.5px solid var(--ink); border-radius: 0.5mm; }

.general h2 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size: 22pt; margin: 0 0 5mm 0; }
.general .two-col { display: flex; gap: 8mm; }
.general .two-col > div { flex: 1; }
"""

COVER = """
<section class="cover">
  <p class="eyebrow">Audition Checklist</p>
  <h1>Six Characters<br>in Search of an Author</h1>
  <p class="italian">Sei personaggi in cerca d'autore</p>
  <p class="credit">Luigi Pirandello &nbsp;·&nbsp; trans. Edward Storer (1922)</p>
  <p class="credit">Village Players · Lausanne</p>
  <p class="company">Director's working pages</p>

  <div class="instructions">
    <h3>How to use these pages</h3>
    <p>One page per role, plus an auditioner-info form at the front and a general assessment page at the back. Tick the boxes during the audition. Write the auditioner's name and date at the top of each role page so the pages don't get mixed up across the morning.</p>
    <p>Each role's checklist is divided into <strong>Reading</strong> (does the actor understand who this is?), <strong>Signature &amp; arc</strong> (did they handle the specific moves the production scores?), and <strong>Voice &amp; body</strong> (the technical performance).</p>
    <p>The final box on each page — <em>Yes / Maybe / No</em> — is your snap impression. Use the lined notes area for anything more specific.</p>
  </div>
</section>
"""

AUDITIONER_FORM = """
<section class="auditioner-form">
  <h2>Auditioner</h2>

  <h3>Identity</h3>
  <div class="field"><span class="label">Full name</span><span class="line"></span></div>
  <div class="field"><span class="label">Date of audition</span><span class="line"></span></div>
  <div class="fields-row">
    <div class="field-half"><span class="label">Phone</span><span class="line"></span></div>
    <div class="field-half"><span class="label">Email</span><span class="line"></span></div>
  </div>

  <h3>Languages</h3>
  <div class="fields-row">
    <div class="field-half"><span class="label">English</span><span class="line"></span></div>
    <div class="field-half"><span class="label">French</span><span class="line"></span></div>
  </div>
  <div class="fields-row">
    <div class="field-half"><span class="label">Other</span><span class="line"></span></div>
    <div class="field-half"><span class="label">Native</span><span class="line"></span></div>
  </div>

  <h3>Roles auditioning for</h3>
  <div class="field"><span class="label">Primary</span><span class="line"></span></div>
  <div class="field"><span class="label">Open to</span><span class="line"></span></div>

  <h3>Availability</h3>
  <div class="field"><span class="label">June 2026 (auditions / line reads)</span><span class="line"></span></div>
  <div class="field"><span class="label">August–November 2026 (weekly rehearsals)</span><span class="line"></span></div>
  <div class="field"><span class="label">Late autumn 2026 (performance run)</span><span class="line"></span></div>
  <div class="field"><span class="label">Known conflicts</span><span class="line"></span></div>

  <h3>Practical</h3>
  <div class="fields-row">
    <div class="field-half"><span class="label">Headshot/résumé received</span><span class="line"></span></div>
    <div class="field-half"><span class="label">Available for callbacks</span><span class="line"></span></div>
  </div>
</section>
"""

GENERAL_ASSESSMENT = """
<section class="general role-page">
  <div class="role-header">
    <div class="top-row"><span>General assessment</span><span>Across all roles</span></div>
    <div class="auditioner-row">
      <span class="label">Auditioner</span><span class="line"></span>
      <span class="label">Date</span><span class="line" style="max-width:30mm;"></span>
    </div>
    <h2>Overall impression</h2>
    <p class="tag">After the role-specific pages — a summary of voice, body, working temperament, and the bigger questions.</p>
  </div>

  <div class="two-col">
    <div>
      <div class="checklist-section">
        <h3>Voice</h3>
        <ul>
          <li><span class="box"></span><span>Clear projection</span></li>
          <li><span class="box"></span><span>Range and colour</span></li>
          <li><span class="box"></span><span>Available for verse rhythms / broken-beat work</span></li>
          <li><span class="box"></span><span>English diction</span></li>
          <li><span class="box"></span><span>French diction / accent comfort</span></li>
          <li><span class="box"></span><span>Listens with the voice</span></li>
        </ul>
      </div>

      <div class="checklist-section">
        <h3>Body</h3>
        <ul>
          <li><span class="box"></span><span>Stage presence</span></li>
          <li><span class="box"></span><span>Listens with the body</span></li>
          <li><span class="box"></span><span>Comfortable with stillness</span></li>
          <li><span class="box"></span><span>Comfortable with the chair-and-coat / bundle conventions</span></li>
          <li><span class="box"></span><span>Available for intimacy protocol</span></li>
        </ul>
      </div>
    </div>

    <div>
      <div class="checklist-section">
        <h3>Working together</h3>
        <ul>
          <li><span class="box"></span><span>Takes direction</span></li>
          <li><span class="box"></span><span>Generous in scene</span></li>
          <li><span class="box"></span><span>Asks specific questions</span></li>
          <li><span class="box"></span><span>Available for full rehearsal arc</span></li>
        </ul>
      </div>

      <div class="checklist-section">
        <h3>Bigger questions</h3>
        <ul>
          <li><span class="box"></span><span>Can hold the Characters' register (timeless, serious, ghost-like)</span></li>
          <li><span class="box"></span><span>Can hold the Players' register (local, modern, amateur in the best sense)</span></li>
          <li><span class="box"></span><span>Has read the intimacy protocol</span></li>
          <li><span class="box"></span><span>Has read the Light &amp; Sound score</span></li>
          <li><span class="box"></span><span>Brings something we did not know we needed</span></li>
        </ul>
      </div>
    </div>
  </div>

  <div class="notes">
    <h3>Director's final impression</h3>
    <div class="lines"></div>
  </div>

  <div class="verdict">
    <span class="label">Overall</span>
    <div class="options">
      <span class="option"><span class="box"></span><span>Yes</span></span>
      <span class="option"><span class="box"></span><span>Maybe — call back</span></span>
      <span class="option"><span class="box"></span><span>No</span></span>
      <span class="option"><span class="box"></span><span>Open for another role</span></span>
    </div>
  </div>
</section>
"""


def render_role_page(c):
    sections_html = []
    for title, items in c["sections"]:
        items_html = "".join(
            f'<li><span class="box"></span><span>{item}</span></li>'
            for item in items
        )
        sections_html.append(f'''
  <div class="checklist-section">
    <h3>{title}</h3>
    <ul>{items_html}</ul>
  </div>''')

    return f"""
<section class="role-page">
  <div class="role-header">
    <div class="top-row"><span>Audition checklist</span><span>{c['role']}</span></div>
    <div class="auditioner-row">
      <span class="label">Auditioner</span><span class="line"></span>
      <span class="label">Date</span><span class="line" style="max-width:30mm;"></span>
    </div>
    <h2>{c['role']}</h2>
    <p class="tag">{c['tag']}</p>
    <p class="summary">{c['summary']}</p>
  </div>

  {"".join(sections_html)}

  <div class="notes">
    <h3>Notes</h3>
    <div class="lines"></div>
  </div>

  <div class="verdict">
    <span class="label">Verdict</span>
    <div class="options">
      <span class="option"><span class="box"></span><span>Yes</span></span>
      <span class="option"><span class="box"></span><span>Maybe</span></span>
      <span class="option"><span class="box"></span><span>No</span></span>
    </div>
  </div>
</section>
"""


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    role_pages = "".join(render_role_page(c) for c in CHARACTERS)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Audition Checklist — Six Characters · Village Players Lausanne</title>
<style>{CSS}</style>
</head>
<body>
<main>
{COVER}
{AUDITIONER_FORM}
{role_pages}
{GENERAL_ASSESSMENT}
</main>
</body>
</html>
"""

    out_html = OUT_DIR / "audition_checklist.html"
    out_html.write_text(html)
    print(f"Wrote {out_html.name} ({out_html.stat().st_size // 1024} KB)")

    out_pdf = OUT_DIR / "audition_checklist.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page()
        page.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(600)
        page.pdf(
            path=str(out_pdf), format="A4",
            margin={"top": "18mm", "right": "20mm", "bottom": "18mm", "left": "20mm"},
            print_background=True, prefer_css_page_size=True,
        )
        browser.close()
    print(f"Wrote {out_pdf.name} ({out_pdf.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build()
