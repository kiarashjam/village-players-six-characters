#!/usr/bin/env python3
"""Build the Two Deaths Note PDF.

A short production note explaining how the production conveys the two
deaths — the Child drowned in the fountain and the Boy shooting himself
— using only objects, sound, dialogue, and light, with no performer
asked to die on stage. For the cast and crew at the production
walk-through, so everyone has the same vocabulary for how the deaths
are "performed" by objects.
"""
import os
from pathlib import Path
import _fullbleed
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Two Deaths, No Performers — Six Characters in Search of an Author</title>
<style>
  :root { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }
  @page { size: A4; margin: 12mm; }
  *,*::before,*::after { box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif;
    font-size: 8pt; line-height: 1.3; margin: 0; padding: 0; }
  main { max-width: none; margin: 0; }

  .masthead { text-align: center; margin-bottom: 2.5mm; padding-bottom: 2mm;
              border-bottom: 1px solid var(--rule); }
  .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600;
             font-size: 7.5pt; letter-spacing: 0.26em;
             text-transform: uppercase; color: var(--accent);
             margin: 0 0 1.5mm 0; }
  h1 { font-family:'Cormorant Garamond',serif; font-weight: 500;
       font-size: 14pt; line-height: 1.1; margin: 0 0 1mm 0; }
  .play { font-style: italic; font-size: 8.5pt; color: var(--ink-soft); margin: 0 0 1mm 0; }
  .credit { font-size: 8pt; color: var(--ink); margin: 0; letter-spacing: 0.04em; }

  h2 { font-family:'Cormorant Unicase',serif; font-weight: 600;
       font-size: 8pt; letter-spacing: 0.18em;
       text-transform: uppercase; color: var(--accent);
       margin: 2.5mm 0 1mm 0; }

  p { margin: 0 0 1.5mm 0; line-height: 1.35; }
  strong { color: var(--ink); }
  em { color: var(--ink); }

  /* Two-column main body */
  .deaths { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin: 2mm 0 0 0; }
  .death { padding: 2mm 3mm; border: 1px solid var(--rule);
           background: rgba(255,255,255,0.22); page-break-inside: avoid; }
  .death h3 { font-family:'Cormorant Garamond',serif; font-weight: 600;
              font-size: 10pt; color: var(--accent);
              margin: 0 0 0.5mm 0; padding-bottom: 0.5mm;
              border-bottom: 1px solid var(--rule); }
  .death h3 .sub { font-family:'EB Garamond',serif; font-style: italic;
                   font-weight: 400; font-size: 8.5pt; color: var(--ink-soft);
                   display: block; margin-top: 0.5mm; }
  .death h4 { font-family:'Cormorant Unicase',serif; font-weight: 600;
              font-size: 7pt; letter-spacing: 0.14em;
              text-transform: uppercase; color: var(--accent);
              margin: 1.5mm 0 0.5mm 0; }
  .death p { margin: 0 0 1mm 0; font-size: 8pt; line-height: 1.3; }

  .setup { border-left: 2px solid var(--accent); padding: 1.5mm 3mm;
           background: rgba(255,255,255,0.22); margin: 1mm 0 2mm 0; }
  .setup h2 { margin-top: 0; }
  .setup ul { margin: 0; padding-left: 4mm; }
  .setup li { margin-bottom: 0.5mm; font-size: 8pt; line-height: 1.3; }

  .close { border-top: 1px solid var(--rule); margin-top: 2.5mm; padding-top: 1.5mm; }
  .close p { font-style: italic; color: var(--ink); margin: 0 0 1mm 0;
             font-size: 8.5pt; line-height: 1.4; }
  .close p.last { font-style: normal; font-size: 8pt; color: var(--ink-soft); margin-bottom: 0; }

  footer.foot { margin-top: 2mm; padding-top: 1.5mm;
                border-top: 1px solid var(--rule);
                font-size: 7.5pt; color: var(--ink-soft);
                font-style: italic; text-align: center; line-height: 1.3; }
  footer.foot strong { font-style: normal; color: var(--ink); }
</style>
</head><body>

<main>

  <div class="masthead">
    <p class="eyebrow">Production Note &nbsp;·&nbsp; Two Deaths, No Performers</p>
    <h1>How the production stages the deaths of the Boy and the Child</h1>
    <p class="play">Six Characters in Search of an Author &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
    <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne &nbsp;·&nbsp; Director: <strong>Kiarash Jamshidi</strong></p>
  </div>

  <section class="setup">
    <h2>What the audience knows by Act Three</h2>
    <p>Before either death lands, the audience has had nearly two hours to learn the convention. By the time the Step-Daughter walks toward the fountain, the room knows three things — and the production will use all three:</p>
    <ul>
      <li><strong>The chair is the Boy.</strong> The wooden chair at the edge of the stage, with the black coat over the back, the schoolboy's cap on the seat, and the satchel by the leg, is the silent fourteen-year-old. The family speaks <em>to</em> it. The Step-Daughter handles it. Nobody is ever seen to play him.</li>
      <li><strong>The bundle is the Child.</strong> The Step-Daughter has carried her in her arms since the moment the Six walked on. The cloth has been kissed, set down, lifted again. The audience reads her as a four-year-old because the family does.</li>
      <li><strong>The Boy has a revolver in his coat pocket.</strong> The Step-Daughter found it in Act Two — pulled it from the pocket inside the column of light, held it briefly, said <em>"If I'd been in your place, instead of killing myself I'd have shot one of those two — or both"</em>, and put it back. The room knows what is in that coat, and it knows what he plans to do with it.</li>
    </ul>
    <p style="margin-top:2mm;">That is the whole instruction the production needs. From here, objects, sound, dialogue, and light do the rest. No performer is ever asked to die in front of an audience.</p>
  </section>

  <div class="deaths">

    <!-- THE CHILD ============================== -->
    <div class="death">
      <h3>The Child<span class="sub">drowned in the fountain, in plain sight, in an unseeable space</span></h3>

      <h4>Object</h4>
      <p>The Step-Daughter lifts the wrapped bundle from the Mother's lap and carries it to the basin. She bends over the water with the bundle in her arms. She lowers it into the basin.</p>

      <h4>Staging — the basin does the hiding</h4>
      <p><strong>The basin's walls are too high for anyone, audience or live actors, to see inside.</strong> This is the production's single most important physical decision. The drowning happens in plain sight, in an unseeable space. The cloth becomes wet, becomes heavy, and the walls hide everything else. The Step-Daughter sobs once.</p>

      <h4>Light</h4>
      <p>As the Son begins his narration, the stage lights drop slowly — breath by breath — until only the fountain's pale-blue interior glow and the bare bulb above the Manager's table remain. The Step-Daughter is silhouetted, bent forward, over the basin.</p>

      <h4>Sound</h4>
      <p>The fountain water has been audible since the top of the part — soft and continuous, slightly louder as she approaches the basin. No splash. Nothing dramatic. The water is the only thing in the room with the strength to keep going.</p>

      <h4>Dialogue</h4>
      <p>The Son tells the room what happened, in past tense, as it happens in present tense on the stage:</p>
      <p><em>"I ran over to her. I was jumping in — to drag her out — when I saw something that stopped me where I stood. The boy. Standing stock still. With a look on his face I will never forget. Watching his little sister, there in the water."</em></p>

      <h4>What lands</h4>
      <p>Past-tense narration over present-tense action. The Son's testimony confirms what the Step-Daughter's silhouette is doing. The Child is dead. The audience never saw it. They know.</p>
    </div>

    <!-- THE BOY ================================ -->
    <div class="death">
      <h3>The Boy<span class="sub">shoots himself out of the dark, from where the chair-and-coat is</span></h3>

      <h4>Object — placed earlier, by the Manager</h4>
      <p>Earlier in Act Three, <strong>the Manager sets the chair-and-coat behind the fountain basin himself.</strong> This is the production's hinge moment — he stops being audience and becomes accessory. The Boy is now standing where Pirandello's text always said he was: by the basin, watching his little sister in the water. He has not moved on his own. He has been put there.</p>

      <h4>Light — the ten-second silhouette</h4>
      <p>After the Step-Daughter lowers the bundle into the water, the fountain light holds for <strong>ten seconds</strong> on the silhouette of the chair-and-coat behind the basin. The audience sees, in low water-light, the Boy watching his little sister in the water. The image is held just long enough to land — and then long enough to become unbearable.</p>

      <h4>Then — full blackout</h4>
      <p>Even the fountain light cuts. Total dark. The audience cannot see anything.</p>

      <h4>Sound</h4>
      <p>Out of that dark, from exactly where the chair-and-coat is, <strong>a single sharp revolver shot.</strong> The water sound briefly stops with it. Then resumes. Then everything stops.</p>

      <h4>Dialogue — the Mother first, then the room</h4>
      <p>The lights snap back. The Mother runs over toward the sound, the veil still down over her face — she never lifts it herself, not even now: <em>"My son! My son!"</em> The Manager: <em>"Is he really wounded?"</em> Players 1 and 2: <em>"He's dead! dead!"</em> Player 3: <em>"No, no, it's only make believe, it's only pretence!"</em> The Father, the only time he raises his voice in the whole play: <em>"Pretence? Reality, sir, reality!"</em></p>

      <h4>What lands</h4>
      <p>The actors lift what they think is the Boy's body — which is the chair-and-coat — and carry it off as a body: heavy, careful, terrible. <strong>The chair has become a body.</strong> The audience reads it as a body. The shot came from where they last saw the silhouette. The revolver was in that coat. They have known, since Act Two, that he was going to use it.</p>
    </div>

  </div>

  <section class="close">
    <p>The principle, in one line: <strong>the most terrible thing on a stage is the thing the audience does not see.</strong> Pirandello already wrote this into the script — drowning hidden by the basin, gunshot heard, not seen. The production extends it: the children are not played by performers, because no performer should be asked to die in front of an audience every night, and because the audience's own imagination will always supply something more frightening than anything a stage can literally show. <strong>Object</strong> gives the audience a body to read; <strong>sound</strong> gives them the event to put inside it; <strong>dialogue</strong> tells them what happened, in a voice too late to stop it; <strong>light</strong> withdraws so they do the last of the work themselves.</p>
    <p class="last">By the time the chair-and-coat is being carried off the stage as a body, the audience has been calling it a body for two hours. That complicity is the play — what the Manager's last act, the look at the empty chair and <em>"To hell with it all"</em> as he walks out, is asking them to admit on the way home.</p>
  </section>

  <footer class="foot">
    <p><strong>Village Players · Lausanne</strong> &nbsp;·&nbsp; Director: Kiarash Jamshidi &nbsp;·&nbsp; Companion to the Director's Copy, the Stage Manager Pack, and the Intimacy Protocol.</p>
  </footer>

</main>

</body></html>
"""

HTML_PATH = OUT_DIR / "two_deaths_note.html"
HTML_PATH.write_text(_fullbleed.apply(HTML))

OUT = OUT_DIR / "two_deaths_note.pdf"
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
