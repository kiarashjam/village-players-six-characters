#!/usr/bin/env python3
"""Build a one-page publication summary PDF for the production.
Suitable for press releases, programme notes, festival listings, or
the company's own announcements."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Production Summary — Six Characters in Search of an Author</title>
<style>
  :root { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }
  @page { size: A4; margin: 22mm 22mm 22mm 22mm; }
  *,*::before,*::after { box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif;
    font-size: 11pt; line-height: 1.6; margin: 0; padding: 0; }

  main { max-width: 162mm; margin: 0 auto; }

  /* Masthead */
  .masthead { text-align: center; margin-bottom: 6mm; }
  .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600;
             font-size: 9pt; letter-spacing: 0.28em;
             text-transform: uppercase; color: var(--accent);
             margin: 0 0 4mm 0; }
  h1 { font-family:'Cormorant Garamond',serif; font-weight: 500;
       font-size: 26pt; line-height: 1.1; margin: 0 0 1mm 0; }
  .italian { font-style: italic; font-size: 11.5pt; color: var(--ink-soft);
             margin: 0 0 4mm 0; }
  .credit { font-size: 10.5pt; color: var(--ink); margin: 0; letter-spacing: 0.04em; }

  /* Tagline */
  .tagline { text-align: center; font-family:'Cormorant Garamond',serif;
             font-style: italic; font-size: 15pt; line-height: 1.4;
             color: var(--ink); margin: 6mm 0 7mm 0; }

  /* Rule */
  .rule { width: 50mm; height: 1px; background: var(--rule); margin: 0 auto 7mm; }

  /* Sections */
  section.note { margin-bottom: 5mm; }
  section.note h2 { font-family:'Cormorant Unicase',serif; font-weight: 600;
                    font-size: 8.5pt; letter-spacing: 0.20em;
                    text-transform: uppercase; color: var(--accent);
                    margin: 0 0 2mm 0; }
  section.note p { margin: 0; line-height: 1.65; }

  /* Footer */
  footer.foot { margin-top: 7mm; padding-top: 4mm;
                border-top: 1px solid var(--rule);
                font-size: 9.5pt; color: var(--ink-soft);
                font-style: italic; text-align: center; line-height: 1.6; }
  footer.foot strong { font-style: normal; color: var(--ink); }

  /* Timeline section */
  section.timeline { margin-top: 8mm; padding-top: 5mm;
                     border-top: 1px solid var(--rule);
                     page-break-inside: avoid; }
  .timeline-heading { font-family:'Cormorant Unicase',serif; font-weight: 600;
                      font-size: 10pt; letter-spacing: 0.22em;
                      text-transform: uppercase; color: var(--accent);
                      margin: 0 0 4mm 0; text-align: center; }
  dl.tl-list { margin: 0; display: grid;
               grid-template-columns: 50mm 1fr;
               gap: 3mm 6mm;
               border-left: 1px solid var(--rule);
               padding-left: 6mm; }
  dl.tl-list dt { font-family:'Cormorant Garamond',serif; font-weight: 600;
                  font-size: 11pt; color: var(--accent);
                  letter-spacing: 0.02em;
                  position: relative; }
  dl.tl-list dt::before {
    content: ""; display: block;
    width: 3mm; height: 3mm;
    background: var(--accent); border-radius: 50%;
    position: absolute; left: -7.5mm; top: 1.5mm;
  }
  dl.tl-list dd { margin: 0; font-size: 10.5pt; line-height: 1.55; color: var(--ink); }
</style>
</head><body>

<main>

  <div class="masthead">
    <p class="eyebrow">Production Summary</p>
    <h1>Six Characters<br>in Search of an Author</h1>
    <p class="italian">Sei personaggi in cerca d'autore</p>
    <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne</p>
    <p class="credit" style="margin-top:6px;">Rewritten and directed by <strong>Kiarash Jamshidi</strong></p>
  </div>

  <p class="tagline">A rehearsal is interrupted by six people no one invited.</p>

  <div class="rule"></div>

  <section class="note">
    <h2>The play</h2>
    <p>Pirandello's 1921 masterpiece begins on what looks like a working rehearsal morning. A theatre company is in the middle of a play it does not particularly like, when six figures in mourning walk on and ask, very politely, to be staged. What follows is one of the most disquieting pieces of theatre written in the last hundred years — a slow argument between the company that wants to finish its morning and the strangers who insist that the tragedy they have walked in carrying has nowhere else to go.</p>
  </section>

  <section class="note">
    <h2>The story, act by act</h2>
    <p><strong>Act One.</strong> A working theatre company at SSA Lausanne, mid-morning, mid-rehearsal of a play it does not particularly like. The door at the back of the stage opens. The Door-keeper enters, carrying a wooden chair, and sets it at the edge of the stage with a black coat folded over the back. Behind him, four figures in mourning walk on; a young woman is already carrying a small wrapped bundle of white cloth. The chair is the silent fourteen-year-old Boy. The bundle is the small four-year-old Child. The Father, lit a tenuous amber, lays out the philosophy he has been rehearsing privately for years: a character is fixed forever in what he is; an actor can go home at night and become someone else. The Step-Daughter, who has heard the philosophy before, breaks it open in one sentence — there was a hundred francs, a pale blue envelope, a back room of a dressmaker's shop. The lights have crept, almost without anyone noticing, to a low blood-coloured wash. The Manager has agreed to try to stage what happened.</p>
    <p><strong>Act Two.</strong> The set is built on two levels. The Step-Daughter speaks her opening monologue alone in a tight column of light, with the wrapped bundle in her arms and the chair-and-coat at her side, a pianist playing Satie's <em>Gymnopédie</em> underneath. Mid-speech, she pulls a revolver from the coat's pocket. Then the shop has to be summoned. A door opens upstage and Madame Pace is simply there — conjured by the very arrangement of the stage, carried by her own performer: a wig, a black silk dress, a long silver chain ending in a pair of scissors. The audience laughs at her first line and regrets it by her last — somewhere inside her bookkeeping aria, the laughter turns. The Mother, who has been silent for an act and a half, finally breaks her silence at Madame Pace and confesses, surprising herself, that she had half-known what was happening in the back room of the shop while she sat in the kitchen and drank the tea. The scene of the atelier is then played again by the company's own actors, with the Mother forced to watch her daughter's worst hour staged in front of her twice — and her broken voice returns, larger this time, as the keystone of the production: <em>"It's taking place now. It happens all the time."</em> The piano dies on her cry.</p>
    <p><strong>Act Three.</strong> Almost all the light is gone. A low fountain basin sits at the centre of the stage, lit pale-blue from inside; a bare bulb hangs above the Manager's table, swinging slightly; a low cello drone underneath that the audience never quite hears. The Father argues philosophy across the act, and the Step-Daughter cuts him three times. The Son, who has not spoken in two acts, tells the room at last what he saw in the garden of his father's house — that he was a single step from the water when the Boy's face froze him, and he did not move. As he speaks, the Step-Daughter lowers the wrapped bundle into the basin; the basin's walls do the hiding. The stage lights drop until only the fountain's pale-blue glow and the silhouette of the chair-and-coat behind it remain. Ten seconds. Then full blackout. Then, out of the dark, the gunshot. The Manager looks once at the empty chair-and-coat, says <em>To hell with it all,</em> and walks out — the audience's own exit, taken first, before they have the chance to take it themselves.</p>
  </section>

  <section class="note">
    <h2>Our staging</h2>
    <p>Nine live performers; three acts; one defining visual per act — a circle of chairs in Act One, a two-level set (rehearsal stage above, watching floor below) in Act Two, a single short fountain basin alone on stage in Act Three. The Boy and the Child, the two youngest of the Six, are not played by performers; they are objects on the stage — a coat-and-chair and a wrapped bundle of white cloth — carried, handled, and spoken to throughout the play. There is no projection, no video, no screen: the audience reads each object as a child because the family does.</p>
    <p>A mostly black-box, minimalist staging. Lighting does much of the storytelling — every shift in tone marked by a change in the temperature of the room. The music score carries the scenes where text alone cannot reach, and pulls the audience through the long emotional arc from the opening comedy to whatever it is the last quarter of an hour becomes.</p>
  </section>

  <section class="note">
    <h2>How it plays</h2>
    <p>The first ten minutes are committed comedy. The last quarter of an hour is not. The production runs in three acts with a <strong>single interval, after Act One</strong> — the audience walks out for a drink while the chairs come down, then returns to a second half (Acts Two and Three) that plays unbroken, building without release to the fountain. Comedy gives way to argument; argument gives way to the family's revealed wound; the final scene at the fountain belongs to no one in the audience who set out to be amused. The discomfort the audience leaves with, by design, is the play.</p>
  </section>

  <section class="timeline">
    <h2 class="timeline-heading">Production timeline</h2>
    <dl class="tl-list">
      <dt>Tue 2 June 2026 · 18:00–21:00 · SSA Lausanne</dt>
      <dd>Open auditions, session 1. Nine tracks to fill: Father, Mother, Step-Daughter, Son, Manager, Players 1 / 2 / 3, and Madame Pace.</dd>

      <dt>Fri 5 June 2026 · 18:00–21:00 · SSA Lausanne</dt>
      <dd>Open auditions, session 2. Additional slot for auditioners who could not attend the Tuesday.</dd>

      <dt>Wed 10 June 2026 · 18:00–21:00 · SSA Lausanne</dt>
      <dd>Callbacks and final casting. Confirmed cast announced at end of evening.</dd>

      <dt>Thu 18 June 2026 · 18:00–21:00 · SSA Lausanne</dt>
      <dd>First table reading. Full company gathers for the first time; round-table introductions; full play read aloud around a table. No staging, no music — just hearing the play together for the first time.</dd>

      <dt>Thu 25 June 2026 · 18:00–21:00 · SSA Lausanne</dt>
      <dd>Production walk-through. Nine performers, two stage objects, three stripped settings (no projection, no screen); chair-and-coat and bundle introduced as conventions.</dd>

      <dt>Thu 2 July 2026 · 18:00–21:00 · SSA Lausanne</dt>
      <dd>Act One table work. Per-part discussion; Light &amp; Sound for Act One walked through (white → amber → red, the radio in the wings).</dd>

      <dt>Thu 9 July 2026 · 18:00–21:00 · SSA Lausanne</dt>
      <dd>Act Two table work. The Step-Daughter's solo opening monologue staged live in the shower light; pianist confirmed; the Madame Pace bookkeeping aria introduced.</dd>

      <dt>Thu 16 July 2026 · 18:00–21:00 · SSA Lausanne</dt>
      <dd>Act Three table work. The Father's philosophical debate, the Son's refusal, the fountain. Light &amp; Sound for Act Three: dark stage, fountain, hanging bulb, cello drone, Pärt at the curtain.</dd>

      <dt>Thu 23 July 2026 · 18:00–21:00 · SSA Lausanne</dt>
      <dd>Light &amp; Sound walk-through, difficult scenes. Full cue list walked through with the stage manager and the company; hardest scenes returned to.</dd>

      <dt>Thu 30 July 2026 · 18:00–21:00 · SSA Lausanne</dt>
      <dd>Full read-through with cues — end-to-end read with the stage manager calling light and sound cues aloud. Notes session afterwards; confirmation of the staging-block calendar.</dd>

      <dt>20 August – 1 November 2026 · SSA Lausanne</dt>
      <dd>Staging block — blocking, run-throughs, technical and dress rehearsals, building toward opening. (5 &amp; 13 August are the company's summer break — no rehearsal.) Primary sessions Thursdays 18:00–21:00, with weekend sessions where needed.</dd>

      <dt>Opening</dt>
      <dd>Late autumn 2026. A short run of three or four performances. Dates and venue to be announced.</dd>
    </dl>
  </section>

  <footer class="foot">
    <p><strong>Village Players · Lausanne</strong> &nbsp;·&nbsp; Dates and venue to be announced</p>
  </footer>

</main>

</body></html>
"""

HTML_PATH = OUT_DIR / "production_summary.html"
HTML_PATH.write_text(HTML)

OUT = OUT_DIR / "production_summary.pdf"
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
