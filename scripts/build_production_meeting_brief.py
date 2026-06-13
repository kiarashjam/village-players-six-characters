#!/usr/bin/env python3
"""Build the Production Meeting Brief PDF.

A single document the director carries into the meeting with the
Production Manager: the production at a glance, what the production
needs from the PM, area-by-area questions to ask, a stage-by-stage
walk-through of the whole process, and a decisions checklist.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Production Meeting Brief — Six Characters in Search of an Author</title>
<style>
  :root { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }
  @page { size: A4; margin: 12mm; }
  *,*::before,*::after { box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif;
    font-size: 11pt; line-height: 1.6; margin: 0; padding: 0; }

  main { max-width: none; margin: 0; }

  .masthead { text-align: center; margin-bottom: 7mm; padding-bottom: 5mm;
              border-bottom: 1px solid var(--rule); }
  .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600;
             font-size: 9pt; letter-spacing: 0.26em;
             text-transform: uppercase; color: var(--accent);
             margin: 0 0 4mm 0; }
  h1 { font-family:'Cormorant Garamond',serif; font-weight: 500;
       font-size: 21pt; line-height: 1.15; margin: 0 0 2mm 0; }
  .play { font-style: italic; font-size: 11pt; color: var(--ink-soft); margin: 0 0 3mm 0; }
  .credit { font-size: 10.5pt; color: var(--ink); margin: 0; letter-spacing: 0.04em; }

  h2 { font-family:'Cormorant Unicase',serif; font-weight: 600;
       font-size: 11pt; letter-spacing: 0.20em;
       text-transform: uppercase; color: var(--accent);
       margin: 8mm 0 3mm 0; }
  h3 { font-family:'Cormorant Garamond',serif; font-weight: 600;
       font-size: 12.5pt; color: var(--ink); margin: 5mm 0 1mm 0; }

  p { margin: 0 0 2.5mm 0; }
  ul, ol { margin: 0 0 3mm 0; padding-left: 6mm; }
  li { margin-bottom: 2mm; line-height: 1.55; }
  strong { color: var(--ink); }

  /* "Ask" lists — questions to put to the PM */
  ul.ask { list-style: none; padding-left: 0; }
  ul.ask li { position: relative; padding-left: 8mm; margin-bottom: 2.5mm; }
  ul.ask li::before { content: "?"; position: absolute; left: 0; top: 0;
                      font-family:'Cormorant Garamond',serif; font-weight: 700;
                      font-size: 12pt; color: var(--accent); }

  /* "Need" lists */
  ul.need { list-style: none; padding-left: 0; }
  ul.need li { position: relative; padding-left: 8mm; margin-bottom: 2mm; }
  ul.need li::before { content: "\2192"; position: absolute; left: 0; top: 0;
                       color: var(--accent); font-weight: 700; }

  /* Checkbox lists */
  ul.check { list-style: none; padding-left: 0; }
  ul.check li { position: relative; padding-left: 8mm; margin-bottom: 2.5mm; }
  ul.check li::before { content: "\2610"; position: absolute; left: 0; top: -0.5mm;
                        font-size: 13pt; color: var(--ink-soft); }

  .at-a-glance { border: 1px solid var(--rule); padding: 5mm 6mm; margin: 4mm 0 6mm 0;
                 background: rgba(255,255,255,0.25); }
  .at-a-glance h2 { margin-top: 0; }
  .at-a-glance dl { margin: 0; display: grid; grid-template-columns: 40mm 1fr; gap: 2mm 5mm; }
  .at-a-glance dt { font-weight: 600; color: var(--accent); font-size: 10pt; letter-spacing: 0.04em; }
  .at-a-glance dd { margin: 0; font-size: 10.5pt; }

  .callout { border-left: 3px solid var(--accent); padding: 3mm 5mm; margin: 4mm 0 5mm 0;
             background: rgba(255,255,255,0.25); }
  .callout p:last-child { margin-bottom: 0; }

  .flag { border: 1px solid var(--accent); padding: 3mm 5mm; margin: 3mm 0 4mm 0;
          background: rgba(139,58,58,0.05); }
  .flag .flag-label { font-family:'Cormorant Unicase',serif; font-weight: 600;
                      font-size: 9pt; letter-spacing: 0.16em; text-transform: uppercase;
                      color: var(--accent); margin: 0 0 1.5mm 0; }
  .flag p:last-child { margin-bottom: 0; }

  nav.toc { margin: 6mm 0 9mm; padding: 5mm 6mm; border: 1px solid var(--rule);
            background: rgba(255,255,255,0.25); }
  nav.toc h2 { margin: 0 0 3mm 0; text-align: center; }
  nav.toc ol { margin: 0; padding-left: 5mm; font-size: 10pt; columns: 2; column-gap: 8mm; }
  nav.toc li { margin-bottom: 1.5mm; }

  .page-break { page-break-before: always; }
  section { page-break-inside: avoid; }

  footer.foot { margin-top: 9mm; padding-top: 4mm; border-top: 1px solid var(--rule);
                font-size: 9.5pt; color: var(--ink-soft); font-style: italic;
                text-align: center; line-height: 1.55; }
  footer.foot strong { font-style: normal; color: var(--ink); }
</style>
</head><body>

<main>

  <div class="masthead">
    <p class="eyebrow">Production Meeting Brief &nbsp;·&nbsp; for the meeting with the Production Manager</p>
    <h1>Six Characters<br>in Search of an Author</h1>
    <p class="play">Sei personaggi in cerca d'autore &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
    <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne &nbsp;·&nbsp; late autumn 2026</p>
    <p class="credit" style="margin-top:6px;">Director: <strong>Kiarash Jamshidi</strong></p>
  </div>

  <section>
    <h2>How to use this in the meeting</h2>
    <p>This is the director's working brief for the production meeting. It has four jobs: (1) give the Production Manager the full picture of the show in one read; (2) list what the production needs from them; (3) supply the questions to put to them, area by area; (4) walk the whole process stage by stage so nothing is left until it is too late to source.</p>
    <p>The "?" bullets are questions to ask. The "&rarr;" bullets are things the production needs delivered. The "&#9744;" bullets are decisions to walk out of the meeting having made. The red boxes are the items most likely to cost money, time, or safety if they are not solved early — raise these first.</p>
    <p>The roles, briefly: the <strong>Production Manager</strong> owns the budget, the schedule of resources, the technical departments, the venue logistics, and delivery. The <strong>Stage Manager</strong> runs the rehearsal room and calls the show. The <strong>director</strong> owns the play. This meeting is where the director hands the PM everything the play will demand of the production.</p>
  </section>

  <nav class="toc">
    <h2>Contents</h2>
    <ol>
      <li>The production at a glance</li>
      <li>The five items to solve first</li>
      <li>Budget &amp; finance</li>
      <li>Venues &amp; dates — SSA + performance venue (with all SSA booking times)</li>
      <li>Schedule &amp; calendar</li>
      <li>Set &amp; staging</li>
      <li>The fountain (water on stage)</li>
      <li>Lighting</li>
      <li>Sound</li>
      <li>The two stage objects (chair-and-coat, bundle)</li>
      <li>The gunshot &amp; the prop revolver</li>
      <li>Props</li>
      <li>Costume &amp; the Madame Pace transformation</li>
      <li>The pianist &amp; the piano</li>
      <li>Crew &amp; personnel</li>
      <li>Health &amp; safety / risk</li>
      <li>The intimacy protocol — logistics</li>
      <li>Rights &amp; licensing</li>
      <li>Insurance</li>
      <li>Marketing, box office, front of house</li>
      <li>Get-in, get-out, strike</li>
      <li>Stage by stage — the whole process</li>
      <li>The meeting agenda</li>
      <li>Decisions to leave with today</li>
    </ol>
  </nav>

  <section class="at-a-glance">
    <h2>1. The production at a glance</h2>
    <dl>
      <dt>The play</dt><dd>Pirandello's 1921 metatheatrical drama. Three acts, three parts per act. Runs roughly two hours, with a single interval after Act One — the second half (Acts Two and Three) plays unbroken, building in one sweep to the fountain.</dd>
      <dt>The concept</dt><dd>A working theatre company is interrupted by six characters demanding to be staged. Comedy in the first half-hour; shame and tragedy by the end. Minimalist, near-black-box; light and music carry the weather.</dd>
      <dt>On stage</dt><dd>Nine live performers (Father, Mother, Step-Daughter, Son, Manager, Players 1 / 2 / 3, and Madame Pace) plus a credited pianist for Act Two.</dd>
      <dt>Stage objects</dt><dd>The Boy is a wooden chair with a coat; the Child is a wrapped bundle of cloth. Two of the six "characters" are objects, not performers.</dd>
      <dt>Settings</dt><dd>Three stripped settings — the rehearsal room (Act I), the dressmaker's shop with a two-level set (Act II), the garden with a fountain (Act III).</dd>
      <dt>Special elements</dt><dd>A tight "shower" light special; a water fountain lit from inside; a single bare hanging bulb that swings; a gunshot; an on-stage upright piano. No projection, no screen.</dd>
      <dt>Calendar</dt><dd>Auditions Tue 2 / Fri 5 / Wed 10 June 2026. Table-work Thursdays 18 June – 30 July 2026. Staging block 20 August – 1 November 2026 (5 &amp; 13 August are the summer break — no rehearsal). Opening late autumn 2026, a short run of 3–4 performances. All audition, table-work, and staging-rehearsal sessions are 18:00 – 21:00.</dd>
      <dt>Rehearsal home</dt><dd>SSA Lausanne — auditions, table-work, and staging rehearsals (see Section 4 for the full booking list and times).</dd>
      <dt>Performance venue</dt><dd>To be announced — hosts get-in, tech, dress, and the run.</dd>
      <dt>Company</dt><dd>Village Players, Lausanne — English-language amateur company.</dd>
    </dl>
  </section>

  <section>
    <h2>2. The five items to solve first</h2>
    <p>Everything in this brief matters, but five items will cost the most money, time, or safety if they are left late. Open the meeting with these.</p>
    <div class="flag">
      <p class="flag-label">Flag 1 — Water on stage (the Act Three fountain)</p>
      <p>A fountain basin, lit from inside, ideally with live water. Water plus stage electrics is the production's single biggest safety and logistics question. We need to decide: live water or convincing substitute? If live: containment, drainage, refilling, electrical isolation, slip protection. This drives the Act Three set design and a chunk of the budget.</p>
    </div>
    <div class="flag">
      <p class="flag-label">Flag 2 — The gunshot</p>
      <p>A real-sounding gunshot in total silence. Almost certainly recorded / electronic rather than a blank-firing weapon (licensing, safety, cost). But a prop revolver is <em>seen</em> being pulled from the coat. We need to decide the sound method and the weapon-prop handling, and check what the venue and canton require.</p>
    </div>
    <div class="flag">
      <p class="flag-label">Flag 3 — The two-level set (Act Two)</p>
      <p>An upper platform (the rehearsal stage) above a lower floor (the watching company). Working at height: structural load, access, edge protection, sightlines. This is the largest build in the show.</p>
    </div>
    <div class="flag">
      <p class="flag-label">Flag 4 — The two stage objects (chair-and-coat, bundle)</p>
      <p>Two of the six "characters" are not played by performers. The Boy is a wooden chair with a black coat over its back, a schoolboy's cap on the seat, and a small leather satchel by the leg. The Child is a small wrapped bundle of white cloth with a black silk sash. Both must be built (or sourced) early — the Step-Daughter rehearses with both from the August staging block onward, and both must be sturdy enough to be carried, dragged, lowered into the fountain, and lifted as a body in the final scene.</p>
    </div>
    <div class="flag">
      <p class="flag-label">Flag 5 — The performance venue is not yet named</p>
      <p>The rehearsal home is settled — SSA Lausanne, with all dates and times known (Section 4). But the <em>performance</em> venue is still "to be announced." Almost every other decision (set size, rig, get-in time, water feasibility, performance dates) depends on that room. Locking the performance venue is the meeting's highest-value outcome.</p>
    </div>
  </section>

  <section class="page-break">
    <h2>3. Budget &amp; finance</h2>
    <h3>What I need</h3>
    <ul class="need">
      <li>A top-line production budget and the spending authority within it.</li>
      <li>A breakdown by department: set, lighting, sound, props (including the two stage objects), costume, piano, crew, venue, marketing, contingency.</li>
      <li>Clarity on what is hired vs. built vs. borrowed.</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>What is the total budget, and what is already committed?</li>
      <li>What is the contingency line, and who authorises drawing on it?</li>
      <li>Which departments are we hiring out, and which are we doing in-house?</li>
      <li>Are there company assets we already own — flats, a piano, lighting stock?</li>
      <li>What does the SSA / venue provide as standard, and what do we bring?</li>
      <li>Is there a grant, sponsor, or cantonal arts support in play, and does it carry obligations (credits, dates, reporting)?</li>
      <li>What is the deadline for committing the big-ticket items (set build, piano, the fountain build)?</li>
    </ul>
  </section>

  <section>
    <h2>4. Venues &amp; dates — two rooms, not one</h2>
    <p>The production uses <strong>two</strong> venues. Be precise with the PM about which is which, because they have different booking owners, costs, and deadlines.</p>
    <ul>
      <li><strong>SSA Lausanne — the rehearsal home.</strong> Auditions, table-work, and the staging rehearsals all happen here. We know the exact dates and times (below). These bookings can be confirmed now.</li>
      <li><strong>The performance venue — to be announced.</strong> Get-in, the technical rehearsal, the dress, and the run happen here. Not yet named or booked. Confirming it is the meeting's highest-value outcome.</li>
    </ul>

    <h3>SSA Lausanne — the exact room bookings we need</h3>
    <p>Every session is <strong>18:00 – 21:00</strong>. We need the room booked for:</p>
    <ul class="need">
      <li><strong>Audition block — 3 evenings.</strong> Tue 2 June, Fri 5 June, Wed 10 June 2026.</li>
      <li><strong>Table-work block — 7 Thursdays.</strong> 18 June, 25 June, 2 July, 9 July, 16 July, 23 July, 30 July 2026.</li>
      <li><strong>Staging block — 9 weekly Thursdays.</strong> 20 Aug, 27 Aug, 3 Sep, 10 Sep, 17 Sep, 24 Sep, 1 Oct, 8 Oct, 15 Oct 2026. (<strong>5 &amp; 13 August are the summer break — no rehearsal, no booking.</strong>)</li>
      <li><strong>Staging block — weekend sessions as needed</strong> across late August–October for intensive blocking, dedicated intimacy rehearsals, and extra run-throughs. Estimate and book these early so the dates are held.</li>
    </ul>
    <p>That is a minimum of <strong>19 evening sessions (18:00 – 21:00) at SSA Lausanne</strong>, plus the weekend sessions. After 15 October the company moves to the performance venue.</p>

    <h3>Performance venue (TBA) — what we need it for</h3>
    <ul class="need">
      <li><strong>Get-in</strong> — set, rig, fountain install, around the week of 19 October 2026.</li>
      <li><strong>Technical rehearsal</strong> — Thu 22 October 2026, in the venue, full cue call with the operators.</li>
      <li><strong>Dress rehearsal</strong> — Thu 29 October 2026.</li>
      <li><strong>Final dress / preview</strong> — Sun 1 November 2026.</li>
      <li><strong>The run</strong> — 3–4 performances, late autumn 2026, dates to be confirmed.</li>
      <li><strong>Get-out / strike</strong> — immediately after the closing performance.</li>
    </ul>

    <h3>What to ask</h3>
    <ul class="ask">
      <li>Can SSA Lausanne confirm all 19 evening sessions plus the weekend holds now?</li>
      <li>Which performance venue, and is it confirmed? If not, what is the shortlist and the decision date?</li>
      <li>What are the exact performance dates (3–4 shows, late autumn 2026)?</li>
      <li>How many days do we get in the performance venue before tech — when is the get-in?</li>
      <li>Performance-venue stage dimensions, height to the grid, available rig and dimmers, power supply, wing space, get-in access?</li>
      <li>Can the performance venue take a water feature (drainage, floor protection)?</li>
      <li>House capacity and sightlines — any seats from which the two-level set, the fountain, or the chair-and-coat at the edge of the stage will not read?</li>
      <li>What does each venue require of us — insurance, technical staff, licences, noise limits?</li>
    </ul>
  </section>

  <section>
    <h2>5. Schedule &amp; calendar</h2>
    <h3>What I need</h3>
    <ul class="need">
      <li>The production schedule aligned to the rehearsal calendar already set.</li>
      <li>Department deadlines back-planned from opening.</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Does the venue availability fit our staging block (20 Aug – 1 Nov) and opening?</li>
      <li>When is the get-in? When is the technical rehearsal? When is the dress?</li>
      <li>What are the order deadlines for set, piano, costume, the chair-and-coat and bundle, and the fountain build?</li>
      <li>When does each crew member need to be confirmed and contracted?</li>
    </ul>
    <div class="callout">
      <p>The fixed dates the PM is planning around: auditions 2 / 5 / 10 June; table-work Thursdays 18 June – 30 July; staging block 20 August – 1 November (5 &amp; 13 Aug are the summer break); opening late autumn. <strong>All audition, table-work, and staging-rehearsal sessions run 18:00 – 21:00 at SSA Lausanne</strong> — the complete list of SSA booking dates is in Section 4. Tech, dress, and the run are in the performance venue. The full per-session breakdown is in the Director's Copy and the Stage Manager Pack.</p>
    </div>
  </section>

  <section>
    <h2>6. Set &amp; staging</h2>
    <h3>What I need</h3>
    <ul class="need">
      <li>Three settings, near-black-box, minimalist: rehearsal room (I), the two-level shop set (II), the garden with fountain (III).</li>
      <li>A build that changes from the chair-circle to the two-level set during the one interval (after Act One), and from the two-level set to the fountain in a fast covered change between Acts Two and Three (no interval).</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Who is designing the set, and when do we lock the design?</li>
      <li>Is the two-level platform a build or a hire? What is the load rating and the access?</li>
      <li>Can we strike the chair-circle and build the two-level set inside the one interval — and strike the two-level set for the fountain in a fast covered change (no interval) between Acts Two and Three?</li>
      <li>What is stored where between performances, and who resets?</li>
      <li>Do we need the Manager's mahogany table, the folding screen, the hat-rack as set or as props (see the Stage Manager Pack prop list)?</li>
    </ul>
  </section>

  <section>
    <h2>7. The fountain (water on stage)</h2>
    <div class="flag">
      <p class="flag-label">High priority — safety + budget</p>
      <p>Act Three centres on a low fountain basin, lit pale-blue from inside, ideally with live, faintly rippling water. The Step-Daughter bends over the bundle inside the basin; the drowning is hidden. This is the production's hardest technical object.</p>
    </div>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Live water or a convincing substitute (light, haze, sound)? What does each cost?</li>
      <li>If live: how is it contained, drained, and refilled between shows?</li>
      <li>How do we isolate the water from the stage electrics and the interior light fixture?</li>
      <li>What is the slip protection around the basin for the performers?</li>
      <li>Who maintains and resets the fountain each performance?</li>
      <li>Does the venue permit water on its stage at all?</li>
    </ul>
  </section>

  <section>
    <h2>8. Lighting</h2>
    <h3>What I need</h3>
    <ul class="need">
      <li>Act One: white working lights → amber → deep red across the three parts.</li>
      <li>A tight overhead "shower" — a narrow vertical column for one performer, used three times in Act Two.</li>
      <li>Act Three: near-dark; the fountain lit from inside; a single bare hanging bulb that swings.</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Who is the lighting designer / operator, and is the venue rig enough or do we hire?</li>
      <li>Can we achieve the narrow "shower" special with the available fixtures and focus?</li>
      <li>How do we rig and safely run the swinging bare bulb over the Manager's table?</li>
      <li>Can the rig hold the slow amber-to-red drift smoothly over a whole act?</li>
      <li>Is there enough dimmer and circuit capacity for all of the above plus the fountain interior light?</li>
    </ul>
  </section>

  <section>
    <h2>9. Sound</h2>
    <h3>What I need</h3>
    <ul class="need">
      <li>A wings radio (French chanson, pre-show into Act One; cuts mid-bar).</li>
      <li>The pianist amplified or balanced as needed (live, Act Two).</li>
      <li>A low cello drone (Act Three Part I); a single offstage piano note (Part II); fountain water sound; the gunshot; Arvo Pärt's <em>Spiegel im Spiegel</em> at the close.</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Who is the sound designer / operator? What is the venue's PA and playback setup?</li>
      <li>Do we need the recorded cues (chanson, cello drone, fountain water, Pärt, gunshot, the offstage piano "slap" note in Act Three) produced and assembled in advance — by whom, by when?</li>
      <li>Does the live piano need reinforcement, or does the room carry it?</li>
      <li>How do we trigger the gunshot cleanly in total silence?</li>
    </ul>
  </section>

  <section>
    <h2>10. The two stage objects (chair-and-coat, bundle)</h2>
    <div class="flag">
      <p class="flag-label">Built early — these are the children of the play</p>
      <p>The Boy and the Child are not played by performers. They are physical objects on the stage from the moment the Six walk on. The audience reads each as a child because the company treats each as a child — so both objects have to be in the rehearsal room from the very first staging session.</p>
    </div>
    <h3>What I need</h3>
    <ul class="need">
      <li><strong>The chair-and-coat (the Boy).</strong> A plain wooden chair, sturdy enough to be carried as a body in the final scene. A folded black coat over the back, a schoolboy's cap on the seat, and a small leather satchel by the leg. The coat must have a pocket deep enough to hold the prop revolver and concealed enough that the audience does not see it until the Step-Daughter pulls it out in Act Two.</li>
      <li><strong>The bundle (the Child).</strong> A small wrapped bundle of white cloth, the shape and weight of a swaddled four-year-old, with a black silk sash tied around it at the waist. Must hold its form when held, when kissed, when set down, when lifted as if it were a body, and when lowered into the fountain basin in Act Three (so: water-resistant outer wrap, or a duplicate kept dry).</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Who builds / sources the chair-and-coat, the coat, the cap, the satchel?</li>
      <li>Who makes the bundle, and how is it constructed so that it survives being lowered into water and lifted back out at every performance?</li>
      <li>Can both objects be in the room from the first staging session on Thu 20 August? (Director's Copy asks for placeholder versions even earlier, in the table-work block.)</li>
      <li>How are both stored between performances and reset before each show?</li>
    </ul>
  </section>

  <section>
    <h2>11. The gunshot &amp; the prop revolver</h2>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Recorded / electronic gunshot, or a blank-firing prop? What is safest and cheapest?</li>
      <li>What do the venue and the canton require for any stage weapon — licence, storage, a named handler?</li>
      <li>The revolver is <em>seen</em> being pulled from the coat: do we need a realistic non-firing replica, and who controls it backstage?</li>
      <li>Who handles, stores, and signs the weapon prop in and out at each performance?</li>
    </ul>
  </section>

  <section>
    <h2>12. Props</h2>
    <h3>What I need</h3>
    <ul class="need">
      <li>The full master prop list — see the Stage Manager Pack. Headline items: the chair-and-coat (the Boy), the white bundle (the Child), the prop revolver, the pale-blue envelope, the mahogany table, the folding screen, the hat-rack, assorted hats, the cook's cap and apron, Madame Pace's silver chain and scissors, the fountain basin, the bare bulb, the upright piano, the Players' scripts.</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Who sources and builds props, and against what deadline?</li>
      <li>The chair-and-coat and the bundle are effectively characters — who makes them and when, so they can be in the rehearsal room from August?</li>
      <li>What is bought, built, borrowed, or hired?</li>
      <li>Who runs the props table during the run and resets it between shows?</li>
    </ul>
  </section>

  <section>
    <h2>13. Costume &amp; Madame Pace</h2>
    <h3>What I need</h3>
    <ul class="need">
      <li>Mourning costume for the four Characters; the Mother's heavy widow's veil; the Players' working-rehearsal clothes; Madame Pace's wig, black silk, and silver chain.</li>
      <li>Madame Pace is a Character carried by her own performer — no longer doubled by a Player, and no on-stage quick change. She enters through the upstage door already in costume, conjured by the magic of the stage.</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Who designs and sources costume, and against what deadline?</li>
      <li>Where does Madame Pace dress and wait for her Act Two entrance, and who cues her through the upstage door?</li>
      <li>Do we need a dresser for the run?</li>
      <li>Who launders and maintains costume across the run?</li>
    </ul>
  </section>

  <section>
    <h2>14. The pianist &amp; the piano</h2>
    <h3>What I need</h3>
    <ul class="need">
      <li>A credited pianist (the fourth Player), confirmed by 16 July 2026, rehearsing with the company from August.</li>
      <li>An upright piano on stage, visible throughout Act Two, in tune.</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Are we hiring the pianist, and on what terms? Who approaches them?</li>
      <li>Do we own a usable upright, or hire one? Who tunes it, and how often across the run?</li>
      <li>How does the piano get into the venue and onto the stage?</li>
    </ul>
  </section>

  <section>
    <h2>15. Crew &amp; personnel</h2>
    <h3>What I need</h3>
    <ul class="need">
      <li>Lighting operator, sound operator, stage crew for changes, a dresser if needed — plus the Stage Manager and Assistant Director already in place.</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Who is on the crew, and which roles are still open?</li>
      <li>Are crew volunteers, paid, or a mix? When are they confirmed?</li>
      <li>Who calls the show — confirm it is the Stage Manager — and who operates each department on the night?</li>
      <li>Do we have enough hands for the one interval change (Act One → Two) and, critically, the fast covered change from the two-level set to the fountain between Acts Two and Three?</li>
    </ul>
  </section>

  <section>
    <h2>16. Health &amp; safety / risk</h2>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Who owns the production risk assessment, and when is it done?</li>
      <li>Water on stage, the gunshot, working at height on the platform, the swinging bulb, the haze/light — each needs a named control. Who signs them off?</li>
      <li>What does the venue require for fire, electrical, and water safety?</li>
      <li>First aid, evacuation, and incident procedure for the run — who is responsible?</li>
    </ul>
  </section>

  <section>
    <h2>17. The intimacy protocol — logistics</h2>
    <h3>What I need</h3>
    <ul class="need">
      <li>A third party present at every intimacy rehearsal (the AD or SM, per the protocol). If budget allows, a professional intimacy coordinator.</li>
      <li>Dedicated intimacy-rehearsal sessions scheduled in the staging block.</li>
    </ul>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Is there budget for a professional intimacy coordinator, or do we use the AD / SM as the third party?</li>
      <li>Can the schedule carry dedicated, separate intimacy-rehearsal sessions?</li>
    </ul>
    <div class="callout">
      <p>The full protocol is a standalone signed document (<code>intimacy_protocol.pdf</code>). The PM's part is purely logistical: budget for a coordinator if possible, and protect the schedule for the dedicated sessions.</p>
    </div>
  </section>

  <section>
    <h2>18. Rights &amp; licensing</h2>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>The base text is the public-domain Storer 1922 translation — confirm we are clear on performance rights for our adapted edition.</li>
      <li>Music: the Satie is public domain; Weill, Mistinguett, Aznavour/Piaf recordings, and the Arvo Pärt are likely <em>not</em>. What performance/sync licences do we need, and who clears them?</li>
      <li>Any rights / clearance needed for recorded audio cues we produce ourselves (e.g. the cello drone, the gunshot effect)?</li>
    </ul>
    <div class="flag">
      <p class="flag-label">Watch — music licensing</p>
      <p>The Pärt and the Weimar/chanson recordings are the most likely rights cost in the whole show. Raise music clearance early; it can take time and money.</p>
    </div>
  </section>

  <section>
    <h2>19. Insurance</h2>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>What insurance does the production and the company carry — public liability, employer's liability, equipment?</li>
      <li>Does water on stage, a weapon prop, or work at height affect cover?</li>
      <li>What does the venue require us to hold?</li>
    </ul>
  </section>

  <section>
    <h2>20. Marketing, box office, front of house</h2>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>Who owns marketing, and what is the budget and timeline?</li>
      <li>The <code>production_summary.pdf</code> is ready as a press / programme blurb — who uses it and when?</li>
      <li>How does box office work — pricing, capacity, ticketing platform?</li>
      <li>Who runs front of house, and do we need a House Manager separate from the Stage Manager?</li>
      <li>Do we want a content note for audiences (the play handles exploitation and a death) — who words it?</li>
    </ul>
  </section>

  <section>
    <h2>21. Get-in, get-out, strike</h2>
    <h3>What to ask</h3>
    <ul class="ask">
      <li>When is the get-in to the performance venue, and how long do we have before tech?</li>
      <li>What is the get-out / strike plan — who, when, returning what to whom?</li>
      <li>How do hired items (piano, lighting, the fountain build) get returned, and by when?</li>
      <li>Who is responsible for leaving both the performance venue and SSA Lausanne as found?</li>
    </ul>
  </section>

  <section class="page-break">
    <h2>22. Stage by stage — the whole process</h2>
    <p>What happens at each stage, and what the Production Manager must have delivered by the end of it.</p>

    <h3>Stage 0 — Pre-production (now → end May 2026)</h3>
    <ul class="need">
      <li>All SSA Lausanne sessions booked (19 evenings, 18:00 – 21:00, plus weekend holds — see Section 4).</li>
      <li>Performance venue named and booked; performance dates locked.</li>
      <li>Budget agreed and departments allocated.</li>
      <li>Set designer, lighting designer, sound designer engaged.</li>
      <li>Big-ticket order deadlines identified (set, piano, fountain).</li>
      <li>Music-licensing process started.</li>
    </ul>

    <h3>Stage 1 — Audition block (Tue 2 / Fri 5 / Wed 10 June 2026, SSA Lausanne, 18:00 – 21:00)</h3>
    <ul class="need">
      <li>Audition room booked at SSA Lausanne for the three evenings.</li>
      <li>Nothing technical yet — but the PM confirms the pianist approach is moving and the chair-and-coat and bundle prototypes are in build.</li>
    </ul>

    <h3>Stage 2 — Table-work block (7 Thursdays, 18 June – 30 July 2026, SSA Lausanne, 18:00 – 21:00)</h3>
    <ul class="need">
      <li>Pianist confirmed by 16 July; piano sourcing under way.</li>
      <li>Placeholder chair-and-coat and bundle in the room from the production walk-through (25 June); final versions in build for August.</li>
      <li>Set design locked; build scheduled. Fountain solution decided.</li>
      <li>Costume design under way; Madame Pace transformation planned.</li>
    </ul>

    <h3>Stage 3 — Staging block at SSA Lausanne (Thu 20 Aug – Thu 15 Oct 2026, 18:00 – 21:00 + weekends; 5 &amp; 13 Aug are the summer break)</h3>
    <ul class="need">
      <li>Real props in the room as they are built — the chair-and-coat, the bundle (in its final water-tolerant form), the revolver replica.</li>
      <li>A rehearsal-room mock-up of the two-level platform for blocking (the real set goes into the performance venue at get-in).</li>
      <li>Pianist rehearsing with the company.</li>
      <li>Costumes ready for the run-throughs in October.</li>
      <li>Crew confirmed and contracted. Risk assessment complete.</li>
    </ul>

    <h3>Stage 4 — Get-in &amp; technical rehearsal (performance venue, week of 19 Oct; tech Thu 22 Oct 2026)</h3>
    <ul class="need">
      <li>Set into the performance venue; rig focused; the shower special set; the fountain installed and water-tested; the swinging bulb rigged.</li>
      <li>All cues built into the prompt book and walked with the operators.</li>
      <li>The shower special and the fountain interior light checked under the real light states.</li>
      <li>Gunshot and water-isolation safety signed off.</li>
    </ul>

    <h3>Stage 5 — Dress rehearsal (around 29 October – 1 November)</h3>
    <ul class="need">
      <li>Full costume, full cues, full props, played as a performance.</li>
      <li>Front of house and box office ready.</li>
      <li>Final risk and safety walk-through.</li>
    </ul>

    <h3>Stage 6 — Performance run (late autumn 2026)</h3>
    <ul class="need">
      <li>Show called by the Stage Manager; departments operated by confirmed crew.</li>
      <li>Props and fountain reset between performances; piano re-tuned as needed.</li>
      <li>Front of house, box office, and any content note in place.</li>
    </ul>

    <h3>Stage 7 — Get-out, strike &amp; wrap</h3>
    <ul class="need">
      <li>Venue struck and returned as found; hires returned.</li>
      <li>Final accounts reconciled against budget.</li>
      <li>Post-mortem with the director and Stage Manager.</li>
    </ul>
  </section>

  <section class="page-break">
    <h2>23. The meeting agenda</h2>
    <p>A running order for the meeting itself — roughly an hour.</p>
    <ol>
      <li><strong>The show in five minutes.</strong> Walk the PM through Section 1 so they have the full picture.</li>
      <li><strong>The five items to solve first</strong> (Section 2): performance venue, water, gunshot, two-level set, the two stage objects.</li>
      <li><strong>Budget &amp; venue</strong> (Sections 3–4) — the decisions everything else hangs on.</li>
      <li><strong>Department by department</strong> (Sections 6–14): set, fountain, light, sound, the two stage objects, props, costume, piano.</li>
      <li><strong>People &amp; safety</strong> (Sections 15–17): crew, risk, intimacy logistics.</li>
      <li><strong>Rights, insurance, marketing, get-out</strong> (Sections 18–21).</li>
      <li><strong>Confirm the stage-by-stage deadlines</strong> (Section 22).</li>
      <li><strong>Lock today's decisions</strong> (Section 24) and agree who owns each open action.</li>
    </ol>
  </section>

  <section>
    <h2>24. Decisions to leave with today</h2>
    <p>Walk out of the meeting with these settled, or with a named owner and a date for each.</p>
    <ul class="check">
      <li>SSA Lausanne booked — all 19 evening sessions (18:00 – 21:00) plus weekend holds.</li>
      <li>Performance venue confirmed (or shortlist + decision date).</li>
      <li>Performance dates locked.</li>
      <li>Top-line budget agreed; contingency and authority clear.</li>
      <li>Fountain: live water or substitute — decided.</li>
      <li>Gunshot: recorded or blank — decided; weapon-prop handling named.</li>
      <li>Two-level set: build or hire — decided; designer engaged.</li>
      <li>Chair-and-coat and bundle: who builds them, in what materials, by when.</li>
      <li>Pianist: who approaches, on what terms; piano sourced.</li>
      <li>Lighting and sound operators identified.</li>
      <li>Music licensing: process started, owner named.</li>
      <li>Risk assessment owner and date set.</li>
      <li>Intimacy: coordinator budgeted or AD/SM confirmed as third party.</li>
      <li>Marketing and box office owner named.</li>
      <li>Department order deadlines back-planned from opening.</li>
      <li>Next production meeting scheduled.</li>
    </ul>
  </section>

  <footer class="foot">
    <p><strong>Village Players · Lausanne</strong> &nbsp;·&nbsp; Director: Kiarash Jamshidi</p>
    <p>Companion documents: Director's Copy, Stage Manager Pack (full prop &amp; cue lists), Assistant Director Pack, Intimacy Protocol, Production Summary.</p>
  </footer>

</main>

</body></html>
"""

HTML_PATH = OUT_DIR / "production_meeting_brief.html"
HTML_PATH.write_text(HTML)

OUT = OUT_DIR / "production_meeting_brief.pdf"
with sync_playwright() as p:
    launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
    browser = p.chromium.launch(**launch_kwargs)
    page = browser.new_page()
    page.goto(f"file://{HTML_PATH.resolve()}", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(600)
    page.pdf(path=str(OUT), format="A4",
             margin={"top": "12mm", "right": "12mm", "bottom": "12mm", "left": "12mm"},
             print_background=True, prefer_css_page_size=True)
    browser.close()

try:
    from pypdf import PdfReader
    r = PdfReader(str(OUT))
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes) · {len(r.pages)} pages")
except BaseException:
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes)")
