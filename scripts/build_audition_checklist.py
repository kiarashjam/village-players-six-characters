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
        "summary": "A well-educated middle-class man whose intellectual elegance is his shield against shame. The philosophy is autobiographical, disguised as metaphysics. The role lives or dies on the actor's ability to fight for his own existence in real time.",
        "sections": [
            ("Voice & breath", [
                "Vocal range and stamina to carry the long Act One and Act Three speeches without strain",
                "Breath control under intellectual pressure — does not run out at the end of a clause",
                "Can move from mellifluous to violent without losing register",
                "Voice breaks honestly at the right moments (does not pre-load the break)",
                "Earned pauses, not filler",
                "Specificity of word choice — discovers each key word as he says it",
            ]),
            ("Character & text", [
                "Plays the speeches as defence and survival, not as lecture",
                "Believes every paradox he speaks, in real time",
                "Holds the contradiction between his elegance and his shame",
                "Audience can hear the philosophy as autobiographical",
                "Available for a four-stage arc: composure → injury → attack → exposure",
                "Listens to the Step-Daughter as she cuts him; does not anticipate her",
                "Holds the silence after each of her cuts — does not rescue himself too fast",
            ]),
            ("Body & presence", [
                "Comfortable with shame as a visible physiological event",
                "Holds stillness when he is losing the argument",
                "Movement is specific, not generalised",
                "Available for the Step-Daughter's close-proximity blocking on stage",
            ]),
            ("Direction-taking & range", [
                "Takes an adjustment between takes and holds it",
                "Available for the line read in three different registers (light, urgent, broken)",
                "Asks specific questions about the text rather than general questions about the play",
            ]),
        ],
    },
    {
        "role": "The Mother",
        "tag": "silence that finally screams",
        "summary": "Silence is her language. The body does her acting. Most of the part is not text. The role needs an actor who is alive when she is not speaking, and who can deliver the keystone line without performing it.",
        "sections": [
            ("Voice & breath", [
                "Voice carries the cry at Madame Pace and at the fountain without being pushed",
                "Keystone line — <em>It's taking place now. It happens all the time</em> — lands without ornament",
                "Speech is humble, peasant-class register; uncomplicated rhythm",
                "Available for long stretches of silence without filling them with sound",
            ]),
            ("Character & text", [
                "Does not perform sympathy or grief; plays the suffering itself",
                "Three different silences distinguishable (Act 1 — does not yet believe she will be heard / Act 2 — being made to watch / Act 3 — holding both children at once)",
                "Available to be looked at without flinching",
                "Listens to everyone on stage — including those she is not facing",
            ]),
            ("Body & presence", [
                "Stillness reads as presence, not passivity",
                "Body is specific — the actor has decided what the Mother's hands are doing at every moment",
                "Comfortable holding the bundle for long stretches",
                "Comfortable with the chair-and-coat as the second child",
                "Available for the staged moment where the Father raises her veil",
                "Eyes can stay on the floor for extended periods without dropping focus",
            ]),
            ("Direction-taking & range", [
                "Available for delicate adjustment without breaking the stillness",
                "Resists the temptation to make the role bigger",
                "Trusts the script to do the work",
            ]),
        ],
    },
    {
        "role": "The Step-Daughter",
        "tag": "the one who refuses to let it be made beautiful",
        "summary": "The moral centre of the play. The role lives or dies on whether the actor can be sharp without being shrill, funny because furious, and direct without ornament. Refuses to be made delicate.",
        "sections": [
            ("Voice & breath", [
                "Voice level and unforced in the surgical cuts against the Father",
                "Can land a long speech (the Madame Pace recall, the bundle monologue) without becoming theatrical",
                "Has range from cold flat delivery to the bundle-tenderness in the same scene",
                "Earned pauses; does not pad the lines",
            ]),
            ("Character & text", [
                "Sharp without being shrill",
                "Comedy and pain in the same beat — the wit is real, the wit is rage",
                "Refuses to be played as delicate or victimised",
                "Refuses to soften her own line",
                "Tenderness for the bundle is unbearably real, not sentimental",
                "Holds the cuts against the Father as moral intervention, not as taunt",
            ]),
            ("Body & presence", [
                "Reads young — the audience must see the age difference with the Father",
                "Knows how to use a room without flirting",
                "Comfortable with the bundle as her sister",
                "Available for the staged close-proximity work with the Father actor",
            ]),
            ("Direction-taking & range", [
                "Available for the line read in two registers (open, attacking)",
                "Takes a note about coldness specifically — can dial intensity down without losing the line",
                "Trusts the audience to read her without help",
            ]),
        ],
    },
    {
        "role": "The Son",
        "tag": "the one who will not act",
        "summary": "The production's most modern figure. The adult child who refuses to participate in a parent's narrative. The role lives or dies on the actor's ability to hold stillness as presence and to let two moments — the mirror speech, the fountain narration — break out of him.",
        "sections": [
            ("Voice & breath", [
                "Quiet voice that carries",
                "Mirror speech earns its own cry mid-sentence (does not pre-load)",
                "Fountain narration available in broken beats, not flowing prose",
                "Comfortable with monosyllables",
            ]),
            ("Character & text", [
                "Refusal is an aesthetic and ethical position — not stubbornness or sulk",
                "Cold without disengagement; cares without showing it",
                "Reads ~22 (or convincingly so) — modern, recognisable",
                "Available for stretches of stage time without speaking",
                "Two moments where the wound breaks out (the mirror speech, the fountain narration) — earns both",
            ]),
            ("Body & presence", [
                "Stillness reads as presence, not blankness",
                "Has chosen what the body is doing during long silences and committed to it",
                "Comfortable being held by the shoulders by the Father in the Act Three confrontation",
                "Available to be looked at by other characters without performing a reaction",
            ]),
            ("Direction-taking & range", [
                "Available to dial up and down — refusal can be quieter or louder without losing meaning",
                "Takes adjustment without becoming defensive about the character's coldness",
                "Trusts that not doing is doing",
            ]),
        ],
    },
    {
        "role": "The Manager",
        "tag": "the symbol of the audience itself",
        "summary": "He is the audience, concretely. Everything he does is what the audience does in their seats. The role lives or dies on the actor's ability to be practical, warm, and recognisable — not theatrical, not directorial in cliché.",
        "sections": [
            ("Voice & breath", [
                "Working-director voice — practical, not declamatory",
                "Carries the rhythm of a real rehearsal room",
                "Comic timing without commenting on the joke",
                "Closing line played straight, with no irony — the most demanding single line in the part",
            ]),
            ("Character & text", [
                "Plays him as the audience proxy throughout",
                "Cynicism is technique; compassion is real — both visible in the same scene",
                "Almost understands what he is watching; never quite admits it",
                "Curiosity wins out over the schedule by Act Two",
                "Almost names Pirandello in Act Three Part Two and stops himself",
                "Pivot moment (setting the chair-and-coat behind the fountain) carries the weight of accessory, not just stage business",
            ]),
            ("Body & presence", [
                "Sits the way the audience sits — forward, half-engaged",
                "Comfortable being looked at across long Act 3 stretches",
                "Movement is functional, not theatrical",
                "Available for long Act 3 stretches without losing energy or focus",
            ]),
            ("Direction-taking & range", [
                "Takes adjustment on temperature (warmer / cooler) without losing the role",
                "Available for the line read with three different relationships to the audience",
                "Generous with scene partners — does not pull focus when the Father or Step-Daughter are speaking",
            ]),
        ],
    },
    {
        "role": "Player 1",
        "tag": "one character in five hats — the Leading Man underneath",
        "summary": "The role asks an actor to play five different functions (Leading Man, L'Ingénue, Door-keeper, Machinist, Third Actor) as the same vain Anglo Leading Man underneath, without losing the spine. Vanity as defence, with affection beneath it. He does not know he is funny.",
        "sections": [
            ("Voice & breath", [
                "Anglo-classical diction that the production can read as English-in-Lausanne",
                "Comic timing without anticipating the laugh",
                "Vocal flexibility across the five roles without losing the spine",
                "Earned theatricality in the shop-scene playing — the gallantry must sound rehearsed, not improvised",
            ]),
            ("Character & text", [
                "Plays five roles as the same man underneath — the audience reads one character, five hats",
                "Vanity is defence; affection is real",
                "Does not know he is funny",
                "Self-correction at <em>I am through with this scene</em> reads as economic, not punchline",
                "Available to play the Leading Man playing the Father in the shop scene without losing his own ego under the role",
            ]),
            ("Body & presence", [
                "Physical specificity across the costume changes",
                "Comfortable with comic exposure — being laughed at without becoming sour",
                "Available for the shop-scene playing on the upper platform",
            ]),
            ("Direction-taking & range", [
                "Takes notes about smaller — can dial vanity down without losing comedy",
                "Available to read each of the five hats in audition (one or two short beats apiece)",
                "Generous in scene with Player 2 in the shop-scene replay",
            ]),
        ],
    },
    {
        "role": "Player 2",
        "tag": "the diva and the props",
        "summary": "The veteran character actress who actually is what Player 1 pretends to be. The role asks for two registers in one body — the Leading Lady's wounded vanity and the Property Man's practical irritation — without losing the same woman in both.",
        "sections": [
            ("Voice & breath", [
                "Range from the diva's wounded indignation to the Property Man's quick functional dispatch",
                "Earned vanity in the voice (not defensive vanity)",
                "Comic timing that lands and then steps aside",
                "Available for a Step-Daughter line read inside the shop-scene replay without parodying",
            ]),
            ("Character & text", [
                "Two registers, one woman — audience reads the same person across both",
                "Vanity is earned, not Player 1's defensive vanity",
                "The wound when the Step-Daughter laughs at her attempt lands as real, not as schtick",
                "<em>I have been made a fool of — believe me — by considerably better</em> — said meaning it",
                "Practical, no-nonsense Property Man bearing",
            ]),
            ("Body & presence", [
                "Comfortable flipping between Leading Lady and Property Man within a single scene",
                "Physical authority — reads as the senior actor in the company",
                "Available for the shop-scene playing on the upper platform",
                "Comfortable with stage objects (hats, screen, table, pegs)",
            ]),
            ("Direction-taking & range", [
                "Takes adjustment on the wound — can play the Step-Daughter's laugh at her as private hurt or public offence",
                "Available to read across both registers in audition",
                "Generous in scene with Player 1",
            ]),
        ],
    },
    {
        "role": "Player 3",
        "tag": "the youngest, and Madame Pace",
        "summary": "The earnest one. Carries the Juvenile Lead and the Prompter, plus the production's most theatrically demanding moment — Madame Pace, who arrives comic and exits chilling. The role lives or dies on the actor's willingness to fully transform, and on whether the dialect can hold meaning.",
        "sections": [
            ("Voice & breath", [
                "Earnest, open Juvenile Lead voice",
                "Quiet, meticulous Prompter voice (slightly older, in the box)",
                "Half-Italian, half-French dialect for Madame Pace that carries meaning, not just sound",
                "The Madame Pace arc — vocal warmth on entry, cold by exit, smile never dropped",
            ]),
            ("Character & text", [
                "Three distinct people, recognisably the same actor",
                "Earnest, genuinely curious in the Juvenile Lead beats",
                "Madame Pace: audience must laugh on the first line, regret laughing by the last",
                "The bookkeeping aria — <em>he clean, he polite, he pay cash</em> — lands as a transactional list, not theatrical menace",
                "Threat at the exit (<em>Don't you forget the name</em>) carried by stillness, not raised voice",
            ]),
            ("Body & presence", [
                "Available for full physical transformation — wig, heels, powder",
                "Body inhabits Madame Pace fully; the audience reads a different person from the Juvenile Lead",
                "Available for the staged hand-under-chin moment with the Step-Daughter (brief, dressmaker-to-customer framing)",
                "Comfortable with the prompter's box for extended periods",
            ]),
            ("Direction-taking & range", [
                "Available for adjustment on dialect — clearer or thicker",
                "Takes notes about the chill — can sharpen the cold register without losing the comedy",
                "Available to read short beats from each of the three roles in audition",
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
  <p class="credit"><strong>Director: Kiarash Jamshidi</strong></p>
  <p class="company">Director's working pages</p>

  <div class="instructions">
    <h3>How to use these pages</h3>
    <p>One page per role, plus an auditioner-info form at the front and a general assessment page at the back. Tick the boxes during the audition. Write the auditioner's name and date at the top of each role page so the pages don't get mixed up across the morning.</p>
    <p>Each role page assesses an actor's <strong>capacity</strong> for the role across four standard categories: <strong>Voice &amp; breath</strong>, <strong>Character &amp; text</strong>, <strong>Body &amp; presence</strong>, and <strong>Direction-taking &amp; range</strong>. The items are role-specific (the Father has long philosophical speeches; the Mother holds long silences; the Step-Daughter needs to be sharp without being shrill) but the categories are the same throughout. They are the questions any audition is trying to answer.</p>
    <p>The general assessment page at the back covers the fundamentals across all roles — voice &amp; speech, body &amp; presence, text work, acting fundamentals, direction-taking, ensemble &amp; practical, and the bigger questions for this production specifically.</p>
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
  <div class="field"><span class="label">Audition: Tue 2 / Fri 5 / Wed 10 June 2026, 18:00 – 21:00, SSA Lausanne</span><span class="line"></span></div>
  <div class="field"><span class="label">Table-work: Thursdays 18 June – 30 July 2026, 18:00 – 21:00, SSA Lausanne</span><span class="line"></span></div>
  <div class="field"><span class="label">Staging: 20 August – 1 November 2026 (5 &amp; 13 Aug summer break; weekly Thursdays + some weekends)</span><span class="line"></span></div>
  <div class="field"><span class="label">Late autumn 2026 (performance run)</span><span class="line"></span></div>
  <div class="field"><span class="label">Known conflicts (specific dates)</span><span class="line"></span></div>

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
    <p class="tag">After the role-specific pages — the actor's fundamentals across voice, body, text, ensemble, and direction-taking.</p>
  </div>

  <div class="two-col">
    <div>
      <div class="checklist-section">
        <h3>Voice &amp; speech</h3>
        <ul>
          <li><span class="box"></span><span>Audible projection to the back of the room</span></li>
          <li><span class="box"></span><span>Clear diction</span></li>
          <li><span class="box"></span><span>Vocal range and colour</span></li>
          <li><span class="box"></span><span>Breath control on long lines</span></li>
          <li><span class="box"></span><span>Tempo &amp; pitch variation (not one-note)</span></li>
          <li><span class="box"></span><span>Earned pauses, not filler</span></li>
          <li><span class="box"></span><span>English diction comfortable</span></li>
          <li><span class="box"></span><span>French diction / accent comfort (for Players' Lausanne texture)</span></li>
        </ul>
      </div>

      <div class="checklist-section">
        <h3>Body &amp; presence</h3>
        <ul>
          <li><span class="box"></span><span>Centred posture; comfortable on stage</span></li>
          <li><span class="box"></span><span>Listens with the body</span></li>
          <li><span class="box"></span><span>Comfortable with stillness</span></li>
          <li><span class="box"></span><span>Specific gesture (not generalised)</span></li>
          <li><span class="box"></span><span>Spatial awareness of scene partners</span></li>
          <li><span class="box"></span><span>Comfortable with the chair-and-coat / bundle conventions</span></li>
          <li><span class="box"></span><span>Available for all scheduled rehearsal dates</span></li>
        </ul>
      </div>

      <div class="checklist-section">
        <h3>Text work</h3>
        <ul>
          <li><span class="box"></span><span>Comprehends what they're saying</span></li>
          <li><span class="box"></span><span>Discovers the word as they say it (not pre-loaded)</span></li>
          <li><span class="box"></span><span>Makes images, not just sounds</span></li>
          <li><span class="box"></span><span>Specific operative words</span></li>
          <li><span class="box"></span><span>Available for verse / broken-beat rhythms</span></li>
        </ul>
      </div>
    </div>

    <div>
      <div class="checklist-section">
        <h3>Acting fundamentals</h3>
        <ul>
          <li><span class="box"></span><span>Listens to scene partner; reacts in real time</span></li>
          <li><span class="box"></span><span>Specific choices, not generalised emotion</span></li>
          <li><span class="box"></span><span>Believes the words as they speak them</span></li>
          <li><span class="box"></span><span>Range — can shift register within a scene</span></li>
          <li><span class="box"></span><span>Risk-taking / vulnerability available</span></li>
          <li><span class="box"></span><span>Comedy timing without commenting on the joke</span></li>
          <li><span class="box"></span><span>Emotional honesty</span></li>
          <li><span class="box"></span><span>Stakes are felt, not announced</span></li>
        </ul>
      </div>

      <div class="checklist-section">
        <h3>Direction-taking</h3>
        <ul>
          <li><span class="box"></span><span>Open to adjustment; willing to try the line again</span></li>
          <li><span class="box"></span><span>Holds an adjustment to the second take</span></li>
          <li><span class="box"></span><span>Range of changes available</span></li>
          <li><span class="box"></span><span>Asks specific questions, not vague ones</span></li>
          <li><span class="box"></span><span>Resilient under correction; does not become defensive</span></li>
        </ul>
      </div>

      <div class="checklist-section">
        <h3>Ensemble &amp; practical</h3>
        <ul>
          <li><span class="box"></span><span>Generous in scene; does not pull focus</span></li>
          <li><span class="box"></span><span>Easy to work with in the room</span></li>
          <li><span class="box"></span><span>Punctual / prepared</span></li>
          <li><span class="box"></span><span>Headshot / résumé received</span></li>
          <li><span class="box"></span><span>Available for full rehearsal arc</span></li>
          <li><span class="box"></span><span>Available for callbacks</span></li>
        </ul>
      </div>

      <div class="checklist-section">
        <h3>Bigger questions for this production</h3>
        <ul>
          <li><span class="box"></span><span>Can hold the Characters' register (timeless, serious, ghost-like)</span></li>
          <li><span class="box"></span><span>Can hold the Players' register (local, modern, amateur in the best sense)</span></li>
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
      <span class="option"><span class="box"></span><span>Yes — cast</span></span>
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
