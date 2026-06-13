#!/usr/bin/env python3
"""Build the Stage Manager Pack PDF.

A standalone brief for the person taking the Stage Manager role:
what they do, what they do not do, working with the Assistant Director,
the master prop list, the master costume list, the Light & Sound
cue list called from the prompt book, and the production timeline.
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
<title>Stage Manager Pack — Six Characters in Search of an Author</title>
<style>
  :root { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }
  @page { size: A4; margin: 22mm 22mm 22mm 22mm; }
  *,*::before,*::after { box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif;
    font-size: 11pt; line-height: 1.65; margin: 0; padding: 0; }

  main { max-width: 162mm; margin: 0 auto; }

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

  .callout { border-left: 3px solid var(--accent);
             padding: 3mm 5mm; margin: 4mm 0 5mm 0;
             background: rgba(255,255,255,0.25); }
  .callout p:last-child { margin-bottom: 0; }

  /* Cue table */
  table.cues { width: 100%; border-collapse: collapse; margin: 3mm 0 5mm 0;
               font-size: 10pt; }
  table.cues th, table.cues td { text-align: left; vertical-align: top;
                                  padding: 2.5mm 3mm; border-bottom: 1px solid var(--rule); }
  table.cues th { font-family:'Cormorant Unicase',serif; font-weight: 600;
                  font-size: 9pt; letter-spacing: 0.12em;
                  text-transform: uppercase; color: var(--accent);
                  background: rgba(255,255,255,0.25); }
  table.cues td.cue-id { font-weight: 600; color: var(--accent);
                         white-space: nowrap; width: 18mm; }
  table.cues td.cue-when { width: 52mm; }
  .act-row td { background: rgba(139,58,58,0.07);
                font-family:'Cormorant Unicase',serif; font-weight: 600;
                font-size: 9.5pt; letter-spacing: 0.16em;
                text-transform: uppercase; color: var(--accent); }

  /* Props / costumes tables */
  table.inv { width: 100%; border-collapse: collapse; margin: 3mm 0 5mm 0;
              font-size: 10pt; }
  table.inv th, table.inv td { text-align: left; vertical-align: top;
                                padding: 2.5mm 3mm; border-bottom: 1px solid var(--rule); }
  table.inv th { font-family:'Cormorant Unicase',serif; font-weight: 600;
                 font-size: 9pt; letter-spacing: 0.12em;
                 text-transform: uppercase; color: var(--accent);
                 background: rgba(255,255,255,0.25); }
  table.inv td.item { width: 60mm; font-weight: 600; }
  table.inv td.checkbox { width: 12mm; text-align: center; font-size: 14pt;
                          color: var(--ink-soft); }

  .page-break { page-break-before: always; }
  section { page-break-inside: avoid; }

  footer.foot { margin-top: 10mm; padding-top: 4mm;
                border-top: 1px solid var(--rule);
                font-size: 9.5pt; color: var(--ink-soft);
                font-style: italic; text-align: center; line-height: 1.6; }
  footer.foot strong { font-style: normal; color: var(--ink); }
</style>
</head><body>

<main>

  <div class="masthead">
    <p class="eyebrow">Stage Manager Pack</p>
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
      <dt>Cast on stage</dt><dd>Nine live performers (Father, Mother, Step-Daughter, Son, Manager, Players 1 / 2 / 3, and Madame Pace) plus a credited pianist for Act II.</dd>
      <dt>Stage objects</dt><dd>The Boy is a wooden chair with a black coat folded over the back, schoolboy's cap on seat, leather satchel at the leg. The Child is a small wrapped bundle of white cloth with a black silk sash.</dd>
      <dt>No projection</dt><dd>There is no rear-wall video and no screen anywhere in the production. The Boy and the Child are objects on the stage from the moment the Six walk on — the chair-and-coat and the wrapped bundle do all the work, live, throughout.</dd>
      <dt>Audition block</dt><dd>Three sessions at SSA Lausanne, 18:00 – 21:00: Tue 2 June, Fri 5 June, Wed 10 June 2026.</dd>
      <dt>Table-work block</dt><dd>Seven Thursdays at SSA Lausanne, 18:00 – 21:00 each evening, 18 June – 30 July 2026.</dd>
      <dt>Staging block</dt><dd>20 August – 1 November 2026 (5 &amp; 13 August are the summer break — no rehearsal).</dd>
      <dt>Opening</dt><dd>Late autumn 2026. A short run of three or four performances.</dd>
    </dl>
  </section>

  <section>
    <h2>The role</h2>
    <p>The Stage Manager is the production's spine. Where the Director shapes the play and the Assistant Director extends the director's reach, the Stage Manager makes the production run. Without an effective Stage Manager an amateur company cannot reliably open a show; with one, every other role on the production gets to focus on the work in front of them.</p>
    <p>Your work runs from before the first rehearsal until the strike. Six areas. The list below is complete.</p>
  </section>

  <section>
    <h2>1. Before the first rehearsal</h2>
    <p>Room bookings at SSA Lausanne for the three audition sessions (Tue 2 / Fri 5 / Wed 10 June 2026, 18:00 – 21:00), the seven Thursday table-work evenings (18 June – 30 July 2026, 18:00 – 21:00), and the staging block (20 August – 1 November 2026; 5 &amp; 13 August are the summer break — no booking). The full rehearsal calendar communicated to the cast — email, calendar invite, and a shared document everyone can see. Distribution: every cast member receives the Director's Copy, the Actor Rehearsal Script, and the calendar before the first read-through. Logistics: keys, room access, working lights, water, any administrative paperwork the company needs. Initial contact with the pianist and (where applicable) the light and sound operators.</p>
  </section>

  <section>
    <h2>2. During the seven-Thursday block</h2>
    <p>Attendance: tracking who is in, who is out, who is late, who is missing entirely. The rehearsal log: a written record of every session — what was worked, what changed, what needs revisiting next week. Prompt book maintenance from day one: every blocking note (when blocking starts), every line change, every cue placement goes into the master script. Continuity: any cast member who missed last week is briefed by you on what was decided so the director does not have to spend the next session catching them up. Communication: the director and the cast both go through you for scheduling and logistical questions.</p>
  </section>

  <section>
    <h2>3. During the August–November weekly rehearsals</h2>
    <p>Floor markings: blocking marks taped on the rehearsal-room floor as staging is set, so actors can find their positions reliably. Props inventory tracked from this point on (see master list below). Costume continuity tracked (see master list below). Cue building: as the light and sound score is rehearsed into the room, every cue is written into the prompt book, walked through with the operators, and timed.</p>
  </section>

  <section>
    <h2>4. Technical and dress rehearsals</h2>
    <p>Cue calling: you call every cue in the play — light, sound, curtain, the pianist's entrances and exits, the shower-light beats, the fountain water, the gunshot, the Pärt at the closing. The prompt book is now the master document for the show. Technical coordination: with the lighting operator, the sound operator, the pianist. Dress: full run with costumes, props, cues; notes taken in real time; problems triaged before opening night.</p>
  </section>

  <section>
    <h2>5. During the performance run</h2>
    <p>Calling the show from the prompt book — every cue, every scene change, every intermission, every curtain. Backstage management: actor entrances and exits, handling any onstage problem in real time (a missed entrance, a prop misplaced, a cue that did not fire, an actor who is unwell), holding the show only if absolutely necessary. Health and safety on stage throughout. Liaison with front-of-house if there is no separate House Manager. Locking the venue at the end of each night.</p>
  </section>

  <section>
    <h2>6. After the run</h2>
    <p>Strike: returning the venue to its starting condition, returning hired equipment, returning costumes, returning the keys. Archive: filing the final prompt book, the rehearsal log, the cue list, the props list. Post-mortem with the director: what worked technically, what would be done differently on the next production, what the company learned about its own room.</p>
  </section>

  <section>
    <h2>What the Stage Manager does <em>not</em> do</h2>
    <ul>
      <li>Direct — the director directs.</li>
      <li>Give acting notes — those go through the director or the Assistant Director.</li>
      <li>Change the script — changes go through the director and are entered into the prompt book only after the director has signed off.</li>
      <li>Negotiate scheduling with individual cast members without coordinating first with the Assistant Director.</li>
    </ul>
  </section>

  <section>
    <h2>Working with the Assistant Director</h2>
    <p>The Stage Manager and the Assistant Director are different roles with overlapping territory. In a small company you often work as a pair. Communication between you is daily during the rehearsal block. Where your responsibilities overlap — cast scheduling communication, calendar logistics, the prompt book, room access — you decide between yourselves who handles what for each given week, and you tell the director. The principle: the director should have to think about the play. Everything else flows through these two roles.</p>
  </section>

  <section class="page-break">
    <h2>The audition block — 2 / 5 / 10 June 2026</h2>
    <p>Three audition sessions at SSA Lausanne, 18:00 – 21:00.</p>
    <ul>
      <li><strong>Tuesday 2 June 2026 — Open auditions, session 1.</strong> Your job: greet, sign in, distribute sides, keep the schedule moving, log timing per audition, take environmental notes (energy, what was tried, who came back).</li>
      <li><strong>Friday 5 June 2026 — Open auditions, session 2.</strong> Additional slot for auditioners who could not attend the Tuesday. Same setup, same job.</li>
      <li><strong>Wednesday 10 June 2026 — Callbacks &amp; final casting.</strong> Callbacks for borderline decisions. The confirmed cast announced at end of evening. Your job: log the final cast, open the production roster, schedule the next session.</li>
    </ul>
  </section>

  <section>
    <h2>The table-work block — seven Thursdays, 18 June – 30 July 2026</h2>
    <p>All sessions at SSA Lausanne, 18:00 – 21:00.</p>
    <ul>
      <li><strong>Thursday 18 June 2026 — First table reading.</strong> The full confirmed company gathers for the first time. Round-table introductions, distribution of the Director's Copy and the Actor Rehearsal Script. The full play read out loud by the company in order, around a table. No staging, no music. Just hearing the play together for the first time. Your job: distribute the documents, open the prompt book, open the rehearsal log, take attendance for the production's first formal record, log timing per act, manage table layout, ensure water and breaks.</li>
      <li><strong>Thursday 25 June 2026 — Production walk-through.</strong> Walk-through of the production concept (nine performers, two stage objects, three stripped settings — no projection, no screen). The chair-and-coat (Boy) and the bundle (Child) introduced as physical conventions. Your job: source or confirm a placeholder chair-and-coat and a placeholder bundle for the table-work block; log the company's questions on the conventions.</li>
      <li><strong>Thursday 2 July 2026 — Act One table work.</strong> Per-part discussion using the Act One part-notes. Light &amp; Sound concept for Act One walked through with you: white → amber → red across the three parts, the radio in the wings. Your job: log every directorial decision into the prompt book; begin the Act One cue list.</li>
      <li><strong>Thursday 9 July 2026 — Act Two table work.</strong> The Step-Daughter's solo monologue — staged live, alone in the shower light, with the bundle in her arms and the chair-and-coat beside her. Madame Pace's work begins with her own performer. The pianist score introduced (Satie's <em>Gymnopédie No. 1</em>, Weill's <em>Bilbao Song</em>, Mistinguett's <em>Mon Homme</em>); the pianist is confirmed for the production. Your job: log Act Two cues into the prompt book; confirm the pianist's availability across August–November.</li>
      <li><strong>Thursday 16 July 2026 — Act Three table work.</strong> The Father's philosophical stretch, the Son's refusal, the fountain. Light &amp; Sound for Act Three walked through with you: dark stage, fountain lit from inside, single hanging bulb above the Manager's table, the cello drone, the silence, the gunshot in real silence, the Arvo Pärt at the closing. Your job: log Act Three cues; source or confirm the fountain basin and the bare hanging bulb; confirm the prop revolver and the gunshot effect; locate or commission the cello drone recording and the Pärt clip.</li>
      <li><strong>Thursday 23 July 2026 — Light &amp; Sound walk-through, difficult scenes.</strong> The full cue list walked through with you and the company — every light, every sound, every piano cue. The hardest scenes returned to: the Madame Pace aria, the shop-scene replay, the fountain. Your job: bring the full cue list in working draft to the room; revise live during the session; close the session with the working cue list distributed to the operators and the pianist.</li>
      <li><strong>Thursday 30 July 2026 — Full read-through with cues.</strong> End-to-end read of the play with light and sound cues called aloud by you from the prompt book. Notes session afterwards: what landed, what didn't, what each actor still needs to find before August. Confirmation of the staging-block calendar (20 August – 1 November 2026; 5 &amp; 13 August are the summer break). Your job: deliver the first end-to-end cue call; distribute the staging calendar to every member of the company before they leave the room.</li>
    </ul>
  </section>

  <section>
    <h2>The staging block — 20 August – 1 November 2026</h2>
    <p>The first two weeks of August are the company's summer break — <strong>no rehearsal on 5 or 13 August.</strong> Staging begins 20 August. Primary sessions Thursdays 18:00 – 21:00 at SSA Lausanne. Additional weekend sessions where the room requires them — booked ahead and communicated to the cast at least two weeks in advance.</p>
    <ul>
      <li><strong>5 &amp; 13 Aug — Summer break.</strong> No rehearsal, no booking. The company returns on 20 August.</li>
      <li><strong>Thu 20 Aug — Re-orientation, Act One blocking.</strong> The company returns from the break. Floor markings begin (you tape them). Act One blocked across all three parts — the rehearsal, the family's arrival, the bargain.</li>
      <li><strong>Thu 27 Aug — Act One run; Act Two Parts I &amp; II.</strong> First end-to-end run of Act One. Act Two Part I (the Step-Daughter's live monologue in the shower light, the pianist's first entrance) and Part II, Madame Pace's aria: her performer brought to performance level, the Weimar vamp, the shower light called in.</li>
      <li><strong>Thu 3 Sep — Act Two Part III: the doubled scene and the Mother's cry.</strong> The shop-scene replay between Leading Lady and Leading Man. The Mother's keystone line and the shower falling on her.</li>
      <li><strong>Thu 10 Sep — Act Three Part I: the argument over reality.</strong> The Father's four-stage arc on his feet. The Step-Daughter's three cuts. The cello drone underneath.</li>
      <li><strong>Thu 17 Sep — Act Three Part II: the Son's refusal.</strong> Mirror speech, closing exchange, the silence that does the work.</li>
      <li><strong>Thu 24 Sep — Act Three Part III: the fountain.</strong> The basin lit from inside, the gunshot in real silence, the Pärt at the curtain.</li>
      <li><strong>Thu 1 Oct — First full run-through.</strong> End-to-end run of the play. No stopping for notes inside the run; full notes session afterwards.</li>
      <li><strong>Thu 8 Oct — Second full run-through.</strong> Tighten what the first run revealed.</li>
      <li><strong>Thu 15 Oct — Third run-through, costume integration.</strong> Costumes introduced for the principals. Last session at SSA before the move to the performance venue.</li>
      <li><strong>Thu 22 Oct — Technical rehearsal.</strong> Full cue call with the operators, in the performance venue. Light operator, sound operator, pianist all in their positions for the first time. <em>Your night.</em></li>
      <li><strong>Thu 29 Oct — Dress rehearsal.</strong> Full costume, full cues, played as if for an audience.</li>
      <li><strong>Sun 1 Nov — Final dress / preview.</strong> The last session of the staging block.</li>
    </ul>
  </section>

  <section class="page-break">
    <h2>Master prop list</h2>
    <p>Tracked from August onward. Every item sourced, labelled, stored, and accounted for at every rehearsal. Check box at every session.</p>
    <table class="inv">
      <thead><tr><th>Item</th><th>Description / notes</th><th class="checkbox">✓</th></tr></thead>
      <tbody>
        <tr><td class="item">The Boy (chair + coat)</td><td>Wooden chair, black coat folded over back, schoolboy's cap on seat, small leather satchel at chair leg. Side of stage Acts I &amp; II; behind fountain basin in Act III.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">The Child (bundle)</td><td>Small wrapped bundle of white cloth, like swaddling, black silk sash tied around it. Carried, kissed, set down, lifted again. Always moved by another performer.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Prop revolver</td><td>Hidden in the chair-coat pocket Acts I &amp; II; pulled from the coat by the Step-Daughter; gunshot heard, not seen.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Pale-blue envelope</td><td>The Father's letter handed to the Step-Daughter early in Act One.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Mahogany table (Manager's)</td><td>Manager's working table, stage-left. In Act Three: the single bare bulb hangs above it, swinging slightly throughout the act.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Folding screen</td><td>Used in the shop-scene replay (Act Two) for the dressmaker's atelier interior.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Hat-rack</td><td>Receives the hats given by the actresses to the Father in Act One.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Hats (assorted)</td><td>Given by the actresses to the Father across Act One.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Cook's cap &amp; apron</td><td>Costume props from the company's rehearsal of <em>Mixing It Up</em> (the play within the play).</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Madame Pace's silver chain &amp; scissors</td><td>Long silver chain worn at the waist with scissors hanging — Pirandello's original detail. Madame Pace's signature object.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Fountain basin (Act III)</td><td>Short low basin centre-stage. Lit from inside (pale-blue). Live water if possible, recorded if necessary. The Step-Daughter bends over the bundle inside the basin; the drowning is not seen.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Bare hanging bulb (Act III)</td><td>Single practical bulb above the Manager's table. Swings very slightly throughout the act.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Upright piano (Act II)</td><td>Small upright stage-right on the lower floor, visible to the audience throughout Act Two. Played live by the credited pianist.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Scripts / notebooks</td><td>The Players' rehearsal scripts and notebooks — visible from Act One onward, the working tools of the company they play.</td><td class="checkbox">☐</td></tr>
      </tbody>
    </table>
  </section>

  <section>
    <h2>Master costume list</h2>
    <table class="inv">
      <thead><tr><th>Role</th><th>Costume notes</th><th class="checkbox">✓</th></tr></thead>
      <tbody>
        <tr><td class="item">Father</td><td>Dark morning coat. Mourning suit. The bearing of a man who has lost a son.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Mother</td><td>Heavy widow's veil — covers most of the face. Full mourning. The veil is half the costume.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Step-Daughter</td><td>Black mourning dress; harder line, younger cut. Not a girl in a black dress — a woman in full black.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Son</td><td>Dark suit, mourning, withdrawn. Closed posture.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Madame Pace</td><td>Wig — bleach-blonde puff. Black silk. The long silver chain with scissors at the waist. Her own performer; she enters through the upstage door, already in costume.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Manager</td><td>Working-rehearsal clothes; the comfortable mid-day clothes of a Lausanne director at a morning rehearsal. Could be in costume by Act III — or could not. Director's call.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Players 1, 2, 3</td><td>Working-rehearsal clothes — the Lausanne register. Local, modern, amateur in the best sense. Could be anything they would wear to a Tuesday-night rehearsal.</td><td class="checkbox">☐</td></tr>
        <tr><td class="item">Pianist</td><td>Dark, formal — black trousers / black skirt, white or muted top. Visible throughout Act II; reads as a performer, not as a stagehand.</td><td class="checkbox">☐</td></tr>
      </tbody>
    </table>
  </section>

  <section class="page-break">
    <h2>Light &amp; Sound cue list — called from the prompt book</h2>
    <p>The Stage Manager calls every cue. Below: the full cue list across the three acts. The numbering is the prompt-book numbering; written here in the order it lands in performance.</p>

    <h3>Act One — three colours, one radio</h3>
    <table class="cues">
      <thead><tr><th class="cue-id">Cue</th><th class="cue-when">When</th><th>What</th></tr></thead>
      <tbody>
        <tr class="act-row"><td colspan="3">Part I — The Rehearsal</td></tr>
        <tr><td class="cue-id">L01</td><td class="cue-when">Pre-show / curtain up</td><td><em>White working lights up.</em> Cold-white, fluorescent, unflattering — the light of an actual morning rehearsal.</td></tr>
        <tr><td class="cue-id">S01</td><td class="cue-when">Pre-show / curtain up</td><td>Radio in the wings — old French chanson at low volume (Aznavour's <em>La Bohème</em>, or a scratchy Piaf: <em>La Vie en rose</em>, <em>Sous le ciel de Paris</em>). Should feel like the company forgot to turn it off.</td></tr>
        <tr class="act-row"><td colspan="3">Part II — The Family Arrives</td></tr>
        <tr><td class="cue-id">L02</td><td class="cue-when">Door-keeper steps onto the stage with the chair-and-coat</td><td><em>White softens to amber / honey gold.</em> The "tenuous light" Pirandello specifies for the Six. The four live Characters walk on inside the warmth; the Step-Daughter is already carrying the wrapped bundle.</td></tr>
        <tr><td class="cue-id">S02</td><td class="cue-when">Door-keeper's first line</td><td>Radio cuts off, mid-bar.</td></tr>
        <tr><td class="cue-id">M01 (live)</td><td class="cue-when">Mid-part</td><td>Step-Daughter sings <em>Prenez garde à Tchou-Tchin-Tchou</em>. Live, unaccompanied. Not a music cue, but recorded in the prompt book.</td></tr>
        <tr class="act-row"><td colspan="3">Part III — The Bargain</td></tr>
        <tr><td class="cue-id">L03</td><td class="cue-when">Step-Daughter's line <em>hundred francs</em></td><td>Amber begins drifting slowly to deep red. Almost imperceptible.</td></tr>
        <tr><td class="cue-id">L04</td><td class="cue-when">End of act</td><td>Final state: low, blood-coloured wash. No music. The silence under the red is the texture.</td></tr>
        <tr><td class="cue-id">L05</td><td class="cue-when">Act-end blackout</td><td>Cue for interval.</td></tr>
      </tbody>
    </table>

    <h3>Act Two — the pianist and the shower</h3>
    <p>The pianist is in position from house open. The <em>shower</em> is a tight vertical column of light from a single overhead source, narrow enough for one performer.</p>
    <table class="cues">
      <thead><tr><th class="cue-id">Cue</th><th class="cue-when">When</th><th>What</th></tr></thead>
      <tbody>
        <tr class="act-row"><td colspan="3">Part I — The Step-Daughter Alone</td></tr>
        <tr><td class="cue-id">L06</td><td class="cue-when">Top of Part I — Step-Daughter kneels with the bundle</td><td><em>Shower</em> falls on the Step-Daughter only. The rest of the stage drops to dark.</td></tr>
        <tr><td class="cue-id">M02 (live)</td><td class="cue-when">As L06 settles</td><td>Pianist plays Satie's <em>Gymnopédie No. 1</em> — slow, simple, once through, beneath the monologue.</td></tr>
        <tr><td class="cue-id">M02-out</td><td class="cue-when">Step-Daughter's last line</td><td>Piano dies on the word. Shower holds one breath, then releases.</td></tr>
        <tr><td class="cue-id">L06-out</td><td class="cue-when">After M02-out</td><td>Working lights up. Property Man, Machinist, and Manager begin the white-parlour set-up on the upper platform.</td></tr>
        <tr class="act-row"><td colspan="3">Part II — Madame Pace's Aria</td></tr>
        <tr><td class="cue-id">L07</td><td class="cue-when">Madame Pace materialises on the upper platform</td><td><em>Shower</em> falls on Madame Pace as she steps into it.</td></tr>
        <tr><td class="cue-id">M03 (live)</td><td class="cue-when">As Madame Pace enters the shower</td><td>Pianist begins slow Weimar-shop vamp: Weill's <em>Bilbao Song</em> at half tempo, or a vamp on Mistinguett's <em>Mon Homme</em>. Sleazy, comic-cabaret tune. Plays continuously through the aria.</td></tr>
        <tr><td class="cue-id">M03-out</td><td class="cue-when">Mother's line <em>You old devil. You murderess.</em></td><td>Piano dies on that line, mid-bar. The silence is the wound.</td></tr>
        <tr class="act-row"><td colspan="3">Part III — The Doubled Scene and the Mother's Cry</td></tr>
        <tr><td class="cue-id">M04 (live)</td><td class="cue-when">Leading Lady &amp; Leading Man take the platform</td><td>Pianist re-enters cautiously — fragments of the Madame Pace vamp, in tatters, as if rehearsing the tune badly.</td></tr>
        <tr><td class="cue-id">L08</td><td class="cue-when">Mother's line <em>It's taking place now. It happens all the time.</em></td><td><em>Shower</em> falls on the Mother — the only light in the room is the column she stands in.</td></tr>
        <tr><td class="cue-id">M04-out</td><td class="cue-when">Mother's cry begins</td><td>Piano cuts out. Does not return.</td></tr>
        <tr><td class="cue-id">M05 (live)</td><td class="cue-when">Accidental curtain falls</td><td>Single piano chord, held. Lights go.</td></tr>
        <tr><td class="cue-id">L09</td><td class="cue-when">After M05</td><td>Blackout behind the fallen curtain. Fast covered change to the fountain — <strong>no interval</strong>; Act Three follows at once.</td></tr>
      </tbody>
    </table>

    <h3>Act Three — dark, the fountain lit, one hanging bulb</h3>
    <table class="cues">
      <thead><tr><th class="cue-id">Cue</th><th class="cue-when">When</th><th>What</th></tr></thead>
      <tbody>
        <tr><td class="cue-id">L10</td><td class="cue-when">Pre-show / curtain up</td><td>Stage is dark. Fountain basin lit from inside — pale blue, faintly rippling. Single bare bulb above the Manager's table, swinging slightly throughout. Performers are in silhouette around the fountain.</td></tr>
        <tr class="act-row"><td colspan="3">Part I — The Argument over Reality</td></tr>
        <tr><td class="cue-id">S03</td><td class="cue-when">Top of Part I</td><td>Sustained cello drone — very low, one note, varying barely. Suggested: a sustained C in the cello's lowest register, or a low organ pedal-tone. The audience should feel a pulse in the room, not hear a note.</td></tr>
        <tr><td class="cue-id">S03-out</td><td class="cue-when">Step-Daughter's line <em>His reality. He always knew exactly where to find me.</em></td><td>Drone dies.</td></tr>
        <tr class="act-row"><td colspan="3">Part II — The Refusal</td></tr>
        <tr><td class="cue-id">—</td><td class="cue-when">Entire part</td><td>Silence. No drone, no piano, no underscoring. Only footsteps and breath.</td></tr>
        <tr><td class="cue-id">S04</td><td class="cue-when">Father's line <em>You can force him, sir</em> (as he grabs the Son's arm)</td><td>Single sharp note from the piano — offstage or recorded — like a slap. Then silence again.</td></tr>
        <tr class="act-row"><td colspan="3">Part III — The Fountain</td></tr>
        <tr><td class="cue-id">S05</td><td class="cue-when">Top of Part III</td><td>Sound of water — fountain live if possible, recorded if necessary — fades in. Stays under the part. Slightly louder as the Step-Daughter approaches the basin.</td></tr>
        <tr><td class="cue-id">L10-dim</td><td class="cue-when">Beneath the Son's narration</td><td>Stage lights drop slowly, breath by breath. End state: only the fountain's pale-blue interior and the bare bulb above the Manager's table remain. The chair-and-coat is silhouetted behind the basin. Hold the silhouette for ten seconds.</td></tr>
        <tr><td class="cue-id">L10-out</td><td class="cue-when">After the ten-second hold</td><td>Full blackout. Even the fountain light cuts. Total dark.</td></tr>
        <tr><td class="cue-id">S06</td><td class="cue-when">Out of the dark — on cue</td><td>Real gunshot effect in real silence. Water sound briefly stops with it, then resumes. The gunshot comes from where the chair-and-coat is, behind the basin.</td></tr>
        <tr><td class="cue-id">L10-back</td><td class="cue-when">On the Mother's cry</td><td>Lights snap back up to the Act Three low state — fountain, bulb, basic stage wash. The Boy is never seen.</td></tr>
        <tr><td class="cue-id">S05-out</td><td class="cue-when">Manager's closing line <em>To hell with it all.</em></td><td>Water sound fades.</td></tr>
        <tr><td class="cue-id">M06</td><td class="cue-when">Immediately after the closing line</td><td>First phrase of Arvo Pärt's <em>Spiegel im Spiegel</em> — about ten seconds. Then lights go.</td></tr>
        <tr><td class="cue-id">L11</td><td class="cue-when">End of M06</td><td>Blackout. End of play.</td></tr>
      </tbody>
    </table>

    <div class="callout">
      <p>The light and sound design should be felt, not heard. The audience does not need to know they are being scored. Call the cues clean; the rest is taste.</p>
    </div>
  </section>

  <section class="page-break">
    <h2>Performance day — running order</h2>
    <ul>
      <li><strong>3 hours before curtain.</strong> Venue access. Working lights up. Pre-set props checked against the master list — every item in its starting position. Costume rail checked. Pianist's instrument tuned / confirmed. Front-of-house briefed on house open and intermission.</li>
      <li><strong>90 minutes before.</strong> Cast call. Half-hour call follows the standard cycle. Light and sound operators in position. Final prop check.</li>
      <li><strong>House open.</strong> Pre-show state up — Act One pre-set (white working lights, French chanson radio at low volume in the wings). House management hands over to you at the time printed in the programme.</li>
      <li><strong>The show.</strong> You call every cue from the prompt book. <strong>One interval, after Act One</strong> (chairs struck, two-level set built); the Act Two → Three change is a fast covered change behind the fallen curtain, not an interval. Pre-set check before Act Two (during the interval) and before Act Three (during the covered change).</li>
      <li><strong>Curtain.</strong> Blackout held. Bows on a separate light state (warm general wash, no shower, no fountain). Cast clear.</li>
      <li><strong>Strike between performances.</strong> Light strike — props back to start positions; bundles returned to the green room; coats and caps reset on the chair. The bulb does not need to be reset; let it swing.</li>
      <li><strong>End of run.</strong> Full strike per Section 6 above.</li>
    </ul>
  </section>

  <section>
    <h2>One closing reminder</h2>
    <div class="callout">
      <p>The director shapes the play. The Assistant Director extends the director's reach. You run the production. If you are doing your job well, the lights come up on time, the props are where they should be, the pianist arrives on cue, the gunshot fires when it should fire — and the audience never thinks about any of it. They watch the play.</p>
    </div>
  </section>

  <footer class="foot">
    <p><strong>Village Players · Lausanne</strong> &nbsp;·&nbsp; Director: Kiarash Jamshidi</p>
    <p>This document is one of a set: Director's Copy, Actor Rehearsal Script, Audition Pack, Audition Checklist, Production Summary, Assistant Director Pack, Stage Manager Pack.</p>
  </footer>

</main>

</body></html>
"""

HTML_PATH = OUT_DIR / "stage_manager_pack.html"
HTML_PATH.write_text(HTML)

OUT = OUT_DIR / "stage_manager_pack.pdf"
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
