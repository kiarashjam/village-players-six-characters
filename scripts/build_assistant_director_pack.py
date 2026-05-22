#!/usr/bin/env python3
"""Build the Assistant Director Pack PDF.

A standalone brief for the person taking the Assistant Director role:
what they do, what they do not do, how they work with the Stage Manager,
and the full production timeline (audition block, table-work block,
staging block).
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Assistant Director Pack — Six Characters in Search of an Author</title>
<style>
  :root { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }
  @page { size: A4; margin: 22mm 22mm 22mm 22mm; }
  *,*::before,*::after { box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif;
    font-size: 11pt; line-height: 1.65; margin: 0; padding: 0; }

  main { max-width: 162mm; margin: 0 auto; }

  /* Masthead */
  .masthead { text-align: center; margin-bottom: 8mm; padding-bottom: 6mm;
              border-bottom: 1px solid var(--rule); }
  .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600;
             font-size: 9pt; letter-spacing: 0.28em;
             text-transform: uppercase; color: var(--accent);
             margin: 0 0 4mm 0; }
  h1 { font-family:'Cormorant Garamond',serif; font-weight: 500;
       font-size: 22pt; line-height: 1.15; margin: 0 0 2mm 0; }
  .play { font-style: italic; font-size: 11pt; color: var(--ink-soft);
          margin: 0 0 4mm 0; }
  .credit { font-size: 10.5pt; color: var(--ink); margin: 0; letter-spacing: 0.04em; }

  /* Section headers */
  h2 { font-family:'Cormorant Unicase',serif; font-weight: 600;
       font-size: 11pt; letter-spacing: 0.22em;
       text-transform: uppercase; color: var(--accent);
       margin: 8mm 0 3mm 0; }
  h3 { font-family:'Cormorant Garamond',serif; font-weight: 600;
       font-size: 13pt; color: var(--ink);
       margin: 5mm 0 2mm 0; }

  p { margin: 0 0 3mm 0; }
  ul { margin: 0 0 4mm 0; padding-left: 6mm; }
  li { margin-bottom: 3mm; line-height: 1.6; }
  strong { color: var(--ink); }
  em { color: var(--ink); }

  /* At-a-glance box */
  .at-a-glance { border: 1px solid var(--rule);
                 padding: 5mm 6mm; margin: 4mm 0 6mm 0;
                 background: rgba(255,255,255,0.25); }
  .at-a-glance h2 { margin-top: 0; }
  .at-a-glance dl { margin: 0; display: grid;
                    grid-template-columns: 42mm 1fr;
                    gap: 2mm 5mm; }
  .at-a-glance dt { font-weight: 600; color: var(--accent);
                    font-size: 10pt; letter-spacing: 0.04em; }
  .at-a-glance dd { margin: 0; font-size: 10.5pt; }

  /* Callout */
  .callout { border-left: 3px solid var(--accent);
             padding: 3mm 5mm; margin: 4mm 0 5mm 0;
             background: rgba(255,255,255,0.25); }
  .callout p:last-child { margin-bottom: 0; }

  /* Page break helpers */
  .page-break { page-break-before: always; }
  section { page-break-inside: avoid; }

  /* Footer */
  footer.foot { margin-top: 10mm; padding-top: 4mm;
                border-top: 1px solid var(--rule);
                font-size: 9.5pt; color: var(--ink-soft);
                font-style: italic; text-align: center; line-height: 1.6; }
  footer.foot strong { font-style: normal; color: var(--ink); }
</style>
</head><body>

<main>

  <div class="masthead">
    <p class="eyebrow">Assistant Director Pack</p>
    <h1>Six Characters<br>in Search of an Author</h1>
    <p class="play">Sei personaggi in cerca d'autore &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
    <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne &nbsp;·&nbsp; late autumn 2026</p>
    <p class="credit" style="margin-top:6px;">Rewritten and directed by <strong>Kiarash Jamshidi</strong></p>
  </div>

  <section class="at-a-glance">
    <h2>At a glance</h2>
    <dl>
      <dt>Company</dt><dd>Village Players, Lausanne — English-language amateur company at SSA Lausanne.</dd>
      <dt>The play</dt><dd>Pirandello's 1921 metatheatrical masterpiece; three acts, three parts per act.</dd>
      <dt>Cast</dt><dd>Eight live performers. Two stage objects in place of the two youngest characters (the chair-and-coat for the Boy; the wrapped bundle for the Child). Three brief projections on the rear wall.</dd>
      <dt>Settings</dt><dd>Three stripped settings — the rehearsal room (Act I), the dressmaker's shop (Act II), the garden with fountain (Act III).</dd>
      <dt>Audition block</dt><dd>Three sessions at SSA Lausanne, 18:00 – 21:00: Tue 2 June, Fri 5 June, Wed 10 June 2026.</dd>
      <dt>Table-work block</dt><dd>Seven Thursdays at SSA Lausanne, 18:00 – 21:00 each evening, 18 June – 30 July 2026.</dd>
      <dt>Staging block</dt><dd>Thirteen weeks of weekly rehearsals, 5 August – 1 November 2026.</dd>
      <dt>Opening</dt><dd>Late autumn 2026. A short run of three or four performances.</dd>
    </dl>
  </section>

  <section>
    <h2>The role</h2>
    <p>The Assistant Director is the director's second pair of eyes and the director's voice when the director is not in the room. In an amateur company this is most often a colleague from the Village Players, or a friend with directing experience who has been brought in to support the production. You do not direct; you assist directing. Where you are present, the director can focus on the moment in front of them while the rest of the production continues to move forward.</p>
    <p>Your work falls into five areas. The list below is complete; nothing here is optional once the role has been accepted.</p>
  </section>

  <section>
    <h2>1. In rehearsal, with the director</h2>
    <p>You take notes throughout each session. You hold the script. You track blocking changes as they are made. You watch for moments the director may have missed because the director was working with a different actor at the same time. You watch for tonal drift, energy drops, scenes running long, off-message comedy. You quietly flag the director when something is slipping. At the end of each session you debrief with the director: what worked, what did not, what to come back to next week. You keep a running list of unresolved questions so nothing gets quietly dropped.</p>
  </section>

  <section>
    <h2>2. With the cast, between scenes and between sessions</h2>
    <p>You run sub-rehearsals when the director is occupied elsewhere — a Player working on the Madame Pace dialect, say, while the director works the Step-Daughter and Mother on the <em>It's taking place now</em> beat. You brief actors who missed the previous session: what was decided, what was tried, what changed. You hold line readings when the director is not in the room. You are available between rehearsals for actor questions the director does not need to answer personally.</p>
  </section>

  <section>
    <h2>3. In technical and dress rehearsals</h2>
    <p>A second pair of eyes from the house — watching the play as the audience will see it, with the light and sound cues running. You flag anything that does not read: a stage direction that is not landing, a cue arriving too early or too late, a sightline blocked, an actor not lit, the pianist's tempo off, the shower-light missing its mark. The director cannot direct and watch the play at the same time; the Assistant Director makes the second pair of eyes possible.</p>
  </section>

  <section>
    <h2>4. During the run of performances</h2>
    <p>You watch each performance from the house. You take notes — what landed, what is drifting, what each actor needs to know before the next show. You feed the notes to the director the next morning. You handle the day-to-day communication with the cast so the director can think about the play.</p>
  </section>

  <section>
    <h2>5. Between rehearsals — communication</h2>
    <p>You are the director's voice when the director is not on call. Email and message follow-up with cast. Coordination with the Stage Manager on scheduling, room changes, missing material. Distribution of any revised pages. Reading the room for energy and morale across the production; flagging anything significant to the director directly.</p>
  </section>

  <section>
    <h2>What the Assistant Director does <em>not</em> do</h2>
    <ul>
      <li>Cast the production — the director casts.</li>
      <li>Block the show — the director blocks.</li>
      <li>Give acting notes directly to actors during a director's session — notes go through the director.</li>
    </ul>
  </section>

  <section class="page-break">
    <h2>Working with the Stage Manager</h2>
    <p>The Assistant Director and the Stage Manager are different roles with overlapping territory. In a small company they often work as a pair. Communication between you is daily during the rehearsal block: who is in the room, what changed, what props are still missing, what each actor needs before next session. The director should not be the message router between you; you speak directly to one another, and you tell the director the outcome — not the other way around.</p>
    <p>Where your responsibilities overlap — cast scheduling communication, calendar logistics, the prompt book, room access — you decide between yourselves who handles what for each given week, and you tell the director. The principle: the director should have to think about the play. Everything else flows through these two roles.</p>
  </section>

  <section>
    <h2>The audition block — 2 / 5 / 10 June 2026</h2>
    <p>Three audition sessions at SSA Lausanne, 18:00 – 21:00.</p>
    <ul>
      <li><strong>Tuesday 2 June 2026 — Open auditions, session 1.</strong> You sit beside the director. You greet auditioners. You hold the audition checklist for the director when needed. You note auditioner reactions to the room, energy, follow-up worth scheduling.</li>
      <li><strong>Friday 5 June 2026 — Open auditions, session 2.</strong> Additional slot for auditioners who could not attend the Tuesday.</li>
      <li><strong>Wednesday 10 June 2026 — Callbacks &amp; final casting.</strong> Callbacks for borderline decisions. The confirmed cast is announced at end of evening.</li>
    </ul>
  </section>

  <section>
    <h2>The seven Thursdays — table-work block, 18 June – 30 July 2026</h2>
    <p>All sessions at SSA Lausanne, 18:00 – 21:00.</p>
    <ul>
      <li><strong>Thursday 18 June 2026 — First table reading.</strong> You help with logistics: signing in arrivals, distributing the Director's Copy and the Actor Rehearsal Script. You take attendance for the production's first formal record. The director runs the reading; you watch the company as a whole — who is reading freely, who is struggling, who is reading <em>at</em> the others vs. <em>with</em> them.</li>
      <li><strong>Thursday 25 June 2026 — Production walk-through.</strong> The chair-and-coat and the bundle are introduced as physical conventions. You make sure the Mother and the Step-Daughter have the objects with them at the table. Notes on how the company is receiving the conventions.</li>
      <li><strong>Thursday 2 July 2026 — Act One table work.</strong> Note-taking, prompt-book annotation, watching for off-message comedy in the Players' Lausanne register. The Step-Daughter / Mother dynamic needs particular protection at this stage — flag any drift toward coquettishness or sentimentality.</li>
      <li><strong>Thursday 9 July 2026 — Act Two table work.</strong> Player 3's transformation work begins. The voice-recording schedule for the Step-Daughter's projected monologue is set; you book the recording session in the production calendar.</li>
      <li><strong>Thursday 16 July 2026 — Act Three table work.</strong> The hardest material in the play. Watch how the actors land the Father's philosophical stretch — there is a tendency for it to drift toward lecture. Note the moments where the Son's silence is doing real work vs. where it has gone empty.</li>
      <li><strong>Thursday 23 July 2026 — Light &amp; Sound walk-through, difficult scenes.</strong> The full cue list walked through with the stage manager. Hard scenes returned to. You take notes on cue placement and pace.</li>
      <li><strong>Thursday 30 July 2026 — Full read-through with cues.</strong> End-to-end read with the Stage Manager calling cues aloud. You take detailed notes in real time: every cue that landed, every cue that did not, every actor who needs a specific thing before August. Your notes go to the director that same night.</li>
    </ul>
  </section>

  <section>
    <h2>The staging block — 5 August – 1 November 2026</h2>
    <p>Thirteen weeks. Primary sessions Thursdays 18:00 – 21:00 at SSA Lausanne, with additional weekend sessions where the room requires it.</p>
    <ul>
      <li><strong>Wed 5 Aug – Thu 20 Aug.</strong> Act One blocking. You carry the prompt book during blocking sessions, recording every position, every movement, every staged beat. You and the Stage Manager confirm who carries the prompt book on which day. You run sub-rehearsals when the director is working on a parallel scene.</li>
      <li><strong>Thu 27 Aug – Thu 3 Sep.</strong> Act Two: Madame Pace's aria and the doubled scene. The Step-Daughter / Mother / Father / Player 1 / Player 2 / Player 3 work block. Detailed prompt-book entries on every staged beat.</li>
      <li><strong>Thu 10 Sep – Thu 24 Sep.</strong> Act Three: the argument over reality, the Son's refusal, the fountain. The hardest material on its feet for the first time.</li>
      <li><strong>Thu 1 Oct – Thu 15 Oct.</strong> Run-throughs begin. You watch from the house with notes. You are the production's first audience. Costumes integrated for the principals.</li>
      <li><strong>Thu 22 Oct — Technical rehearsal.</strong> You are the house-eyes — every sightline, every cue, every actor's lighting. Your notes feed directly into the production's last-mile adjustments.</li>
      <li><strong>Thu 29 Oct — Dress rehearsal.</strong> Full costume, full cues, played as if for an audience. Notes for the next day are minimal.</li>
      <li><strong>Sun 1 Nov — Final dress / preview.</strong> Closing session of the staging block. Whatever the production needs before opening.</li>
      <li><strong>Performance run (3–4 nights, late autumn).</strong> One performance, one set of notes, delivered to the director the next morning. The director needs to keep the show shaped across the run; you give them the data to do that.</li>
    </ul>
  </section>

  <section>
    <h2>One closing reminder</h2>
    <div class="callout">
      <p>The director casts, blocks, and decides. The Stage Manager runs the production's spine. You are the connective tissue: between the director and the cast, between the director and the Stage Manager, between this rehearsal and the next. If you are doing your job well, the director can spend their attention on the play and nobody else has to chase information.</p>
    </div>
  </section>

  <footer class="foot">
    <p><strong>Village Players · Lausanne</strong> &nbsp;·&nbsp; Director: Kiarash Jamshidi</p>
    <p>This document is one of a set: Director's Copy, Actor Rehearsal Script, Audition Pack, Audition Checklist, Production Summary, Assistant Director Pack, Stage Manager Pack.</p>
  </footer>

</main>

</body></html>
"""

HTML_PATH = OUT_DIR / "assistant_director_pack.html"
HTML_PATH.write_text(HTML)

OUT = OUT_DIR / "assistant_director_pack.pdf"
with sync_playwright() as p:
    launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
    browser = p.chromium.launch(**launch_kwargs)
    page = browser.new_page()
    page.goto(f"file://{HTML_PATH.resolve()}", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(600)
    page.pdf(path=str(OUT), format="A4",
             margin={"top":"22mm","right":"22mm","bottom":"22mm","left":"22mm"},
             print_background=True, prefer_css_page_size=True)
    browser.close()

try:
    from pypdf import PdfReader
    r = PdfReader(str(OUT))
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes) · {len(r.pages)} pages")
except BaseException:
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes)")
