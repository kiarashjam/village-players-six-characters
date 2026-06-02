#!/usr/bin/env python3
"""Build the Synopsis PDF — the whole story, beginning to end.

Plain narrative voice. Not the Director's Copy (which carries the full
dialogue and the directorial commentary). Not the press blurb (which
markets the show). This document tells the story from the backstory
through the curtain, in language a friend would use on the way to the
theatre.

For cast, company, production crew, and anyone reading the production
documents who has not read Pirandello.
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
<title>The Story — Six Characters in Search of an Author</title>
<style>
  :root { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }
  @page { size: A4; margin: 22mm 24mm 22mm 24mm; }
  *,*::before,*::after { box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif;
    font-size: 11.5pt; line-height: 1.7; margin: 0; padding: 0; }
  main { max-width: 162mm; margin: 0 auto; }

  /* Masthead */
  .masthead { text-align: center; margin-bottom: 9mm; padding-bottom: 6mm;
              border-bottom: 1px solid var(--rule); }
  .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600;
             font-size: 9pt; letter-spacing: 0.26em;
             text-transform: uppercase; color: var(--accent);
             margin: 0 0 4mm 0; }
  h1 { font-family:'Cormorant Garamond',serif; font-weight: 500;
       font-size: 22pt; line-height: 1.15; margin: 0 0 2mm 0; }
  .play { font-style: italic; font-size: 11pt; color: var(--ink-soft);
          margin: 0 0 3mm 0; }
  .credit { font-size: 10.5pt; color: var(--ink); margin: 0; letter-spacing: 0.04em; }

  /* "What this is" intro block */
  .intro p { margin: 0 0 3mm 0; }
  .intro h2 { font-family:'Cormorant Unicase',serif; font-weight: 600;
              font-size: 11pt; letter-spacing: 0.20em;
              text-transform: uppercase; color: var(--accent);
              margin: 7mm 0 3mm 0; }

  /* Section headers — one per act */
  h2.section { font-family:'Cormorant Garamond',serif; font-weight: 500;
               font-size: 20pt; color: var(--accent);
               margin: 12mm 0 1mm 0;
               padding-bottom: 1mm;
               border-bottom: 1px solid var(--rule); }
  h2.section .roman { font-size: 13pt; font-family:'Cormorant Unicase',serif;
                      font-weight: 600; letter-spacing: 0.16em; color: var(--ink-soft);
                      margin-right: 5mm; }
  p.subheading { font-style: italic; color: var(--ink-soft);
                 margin: 0 0 5mm 0; font-size: 11pt; }

  p { margin: 0 0 3.5mm 0; }

  /* The opening "before the play" section */
  .backstory { page-break-after: always; }

  /* Closing block */
  .closing { margin-top: 8mm; padding-top: 5mm; border-top: 1px solid var(--rule); }
  .closing p:last-of-type { margin-bottom: 0; }

  /* Pull-quote, used once at the end */
  .pull-quote { font-family:'Cormorant Garamond',serif; font-style: italic;
                font-size: 13pt; line-height: 1.5;
                padding: 5mm 8mm; margin: 6mm 0 6mm 0;
                color: var(--ink); text-align: center;
                border-top: 1px solid var(--rule);
                border-bottom: 1px solid var(--rule); }

  section { page-break-inside: avoid; }
  .act { page-break-before: always; }

  footer.foot { margin-top: 10mm; padding-top: 5mm;
                border-top: 1px solid var(--rule);
                font-size: 9.5pt; color: var(--ink-soft);
                font-style: italic; text-align: center; line-height: 1.55; }
  footer.foot strong { font-style: normal; color: var(--ink); }
</style>
</head><body>

<main>

  <div class="masthead">
    <p class="eyebrow">The Story &nbsp;·&nbsp; Beginning to End</p>
    <h1>Six Characters<br>in Search of an Author</h1>
    <p class="play">Sei personaggi in cerca d'autore &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
    <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne &nbsp;·&nbsp; late autumn 2026</p>
    <p class="credit" style="margin-top:6px;">Director: <strong>Kiarash Jamshidi</strong></p>
  </div>

  <section class="intro">
    <h2>What this is</h2>
    <p>The whole story of the play, told briefly and straight through — from the events that happened years before the curtain rises to the closing line. Plain narrative voice; no directorial commentary, no staging notes, no technical anything. Read it before you read the script; read it again when you have finished the script; hand it to a friend who is coming to see the show and wants to know what they are walking into.</p>
    <p>The play has two stories inside it. There is a <strong>family tragedy</strong> — a marriage, a separation, a man, his wife, her secretary, four children, a poor little dressmaker's shop, a hundred francs, a fountain. And there is a <strong>theatrical present</strong> in which six figures from that family tragedy walk onto a working company's stage one morning and demand that their story be staged. The two stories meet, argue, fail, and end in the same room. The family one is told only in pieces, because the family itself can only ever tell it in pieces. The theatrical one is what the audience watches, in real time, for two hours.</p>
    <p>What follows tells the family story first — what happened, in the order it happened — and then walks through what the audience sees on the stage, act by act.</p>
  </section>

  <section class="backstory">
    <h2 class="section"><span class="roman">Before</span>What happened before the play begins</h2>
    <p class="subheading">The family story, in the order it happened</p>

    <p>Years before the play opens — in a town that, in this production, is Lausanne — a man and a woman were married. They had one son. The husband was a man of restless intelligence and unhappy temper; the wife was simple, gentle, and almost silent. Watching her grow attached to his secretary — a quiet man who shared her temperament more than the husband did — the husband decided, with what he believed at the time to be a kind of generosity, to give her to the secretary. He sent the two of them away together. The small son was left behind in the country, raised by a wet-nurse, and saw nothing of either of his parents for the rest of his childhood.</p>

    <p>The wife and the secretary had three more children together: a daughter, a boy, and a small girl. They lived in modest comfort for many years. The husband, from a distance, watched them grow — he kept an eye, in the quiet way men do when they cannot allow themselves to look directly. Once, in particular, he stood at the gate of the eldest daughter's school, and saw her come out among the other children; he came back, more than once, with little parcels of gifts for her — a fine straw hat, a bouquet of flowers — that she received with a child's polite confusion, not knowing who he was. He told himself, then and afterwards, that what he felt was a father's affection. The wife and her new family never knew he had been there.</p>

    <p>Then the secretary died. The wife and her three children fell out of comfort, then out of security, and then out of dignity. They moved to a smaller town, took rooms above a shop, and the wife began to do piecework sewing for a dressmaker called Madame Pace, whose atelier sat off the rue de Bourg in a courtyard near Saint-François. Madame Pace's dressmaking was the public side of her trade. The back rooms of the atelier did other business — quiet business, polite business, transacted in cash by gentlemen who paid for half an hour and left without leaving names — that the town agreed, by long habit, not to look at too closely.</p>

    <p>The mother's sewing was poor. She ruined silk; the costs mounted on Madame Pace's book; the book had to balance. Madame Pace, smiling, suggested one afternoon that the eldest daughter — eighteen years old, two months an orphan, still in full mourning for her father — might help to settle the debt by spending some afternoons in the back room. The daughter agreed because the alternative was the family going hungry. She had been working at the atelier for some weeks when a particular customer came in: a middle-aged man in a good coat, polite, soft-voiced, who placed a hundred francs in a pale blue envelope on a little mahogany table beside the bed and asked the new girl, very gently, to take her little black dress off.</p>

    <p>He was her stepfather. He did not recognise her; he had only seen her once, briefly, outside the gate of her school, and she had grown. She did not recognise him; she had been too small the last time he was in her mother's house to remember his face. They were minutes from a transaction neither of them would ever live down when the mother — at the shop that afternoon herself — walked through the door, recognised her husband, and the whole room shattered into a place from which no character inside it would ever recover.</p>

    <p>What happened after the shop is also part of the story, although the family will not tell it in order. The mother and her four children moved into the husband's house — there was nowhere else for them to go. The young son, who had been raised alone in the country, was brought back, and found himself sharing the house with a mother he did not know, three half-siblings he had never met, and a stepfather he despised. He withdrew, and refused to speak to any of them. The small Child wandered in the garden of the house, untended. The fourteen-year-old Boy walked behind her in silence. One afternoon, the small Child fell into the fountain in the garden and drowned. The Boy stood by the side of the basin and watched her drown. The young Son ran toward her, was about to jump in, and was frozen at the threshold by the sight of the Boy's face. The Child died. Soon afterwards, the Boy, with a revolver he had been carrying in the pocket of his school coat, shot himself.</p>

    <p>This is the story the play is about. The play itself begins long afterwards, somewhere else entirely.</p>
  </section>

  <section class="act">
    <h2 class="section"><span class="roman">Act One</span>The Six arrive at a rehearsal</h2>
    <p class="subheading">The theatre company is interrupted</p>

    <p>The curtain rises on a working theatre company at SSA Lausanne, preparing for an evening's rehearsal. The Manager sits at his table with a script he does not particularly like — Pirandello's <em>Mixing It Up</em>, of all things. His three Players, all working actors, are getting into position. The Leading Man complains about being asked to wear a cook's cap in the opening scene. The Leading Lady, who is also doing the props this season because the company cannot afford a Property Man, is building a folding screen out of two old flats and a hinge she bought yesterday. The youngest member of the company, who is also serving as Prompter, is taking dictation about the set. The Manager is arguing with everyone, and behind on the morning.</p>

    <p>Into this rehearsal, the Door-keeper enters with six strangers — and behind him, a wooden chair he carries to the edge of the stage, with a black coat folded over its back, a schoolboy's cap on the seat, and a small leather satchel by the leg.</p>

    <p>The strangers are four figures in mourning — a man of about fifty, a woman heavily veiled, a young woman in elegant black, and a tall young man with the bearing of someone who has come on stage against his will. The young woman is carrying a small wrapped bundle of white cloth with a black silk sash. The chair is the silent fourteen-year-old <strong>Boy</strong>. The bundle is the four-year-old <strong>Child</strong>. The audience reads them as children within the first minute, because the family does.</p>

    <p>The Six explain: they were once written, by an author who then abandoned them. They have been carrying their unfinished drama ever since, looking for someone who will at last stage it. They have come to this company, on this morning, because they have nowhere else to go.</p>

    <p>The Manager is, by turns, sceptical, dismissive, fascinated, and finally — against his own better judgement — interested. The <strong>Father</strong> explains the philosophy that he will return to all morning: a character is fixed forever in what he is; an actor goes home at night and becomes someone else, while a character has no other room to live in, and no other hour to live in. The <strong>Step-Daughter</strong>, impatient with her stepfather's philosophy, taunts him and exposes him: there was a hundred francs in a back room of a dressmaker's shop, and a girl in mourning, and a small dress she was asked to take off. The <strong>Mother</strong>, hearing this said in a room full of strangers, nearly faints. The Father, in his agitation, lifts her veil against her will. The young <strong>Son</strong> says nothing.</p>

    <p>By the end of the act the comedy of the morning has burned off entirely. The family is standing inside its own argument, in a deep blood-coloured light, with the working company watching them in silence. The Manager has agreed to try to stage what happened — partly because he believes there may be a play in it, and partly because he has lost a morning already and does not yet know how to recover it.</p>
  </section>

  <section class="act">
    <h2 class="section"><span class="roman">Act Two</span>The staging attempt, and the doubled scene</h2>
    <p class="subheading">The dressmaker's shop, played twice</p>

    <p>The stage has been transformed onto two levels. The upper platform is where the family's drama will be played; the lower floor is where the working company stays, watching.</p>

    <p>The Step-Daughter erupts onto the upper platform with the wrapped bundle in her arms and the chair-and-coat dragged behind her. She has just lost an argument with the Manager that we did not see. Alone in a tight column of light, with a pianist playing Satie's <em>Gymnopédie</em> underneath, she speaks to her two silent siblings — tender to the bundle as if it were a real four-year-old, contemptuous to the chair-and-coat as if it were her brother. Mid-speech, she reaches for the coat hanging on the chair, takes it by the sleeve, and pulls a revolver from its pocket. She holds it briefly in the column of light, then puts it back. The audience watches a young woman speak with great love to a piece of cloth and with great contempt to a piece of furniture, and decides — quietly, without being asked — to believe both.</p>

    <p>The Manager then sets the company to work. The Property Man wheels the folding screen into position. The little mahogany table is placed on the upper platform. A row of pegs is set up for hats. The folding screen separates a small space for the dressmaker's atelier; the Father takes a position outside it; the Step-Daughter takes a position inside.</p>

    <p>And then, in the production's strangest single moment, <strong>Madame Pace</strong> arrives. She is not in the cast list; nobody has invited her; the production's youngest performer, who has been playing the Prompter all morning, transforms before the audience's eyes into a fat, bleach-blonde, rouged Italian-Swiss woman in black silk, with a long silver chain at her waist ending in a pair of scissors. She speaks half in Italian, half in French — a foreigner's broken speech, ridiculous and grotesque. The audience laughs at her first line. By her last line they regret laughing. She is a businesswoman of shame: elegant, practical, smiling, and morally rotten. The cruelty is in the bookkeeping. She does not shout.</p>

    <p>Madame Pace and the Step-Daughter play the scene of the atelier the way it happened — the silk debt, the conversation, the dress, the hundred francs, the entrance of the polite gentleman in the good coat who turns out to be her stepfather. The audience watches it. Then, when it has happened once, the Manager has it played again: the company's own Leading Lady and Leading Man climb onto the upper platform and perform the same scene as <em>theatre</em>, with the bundle and the chair-and-coat watching from below. The Step-Daughter laughs at them — the laugh is the wound; the Leading Lady, who has played leads at every house in this canton, has been made a fool of by better, and she means it.</p>

    <p>The Mother is forced to watch her daughter's worst hour staged twice in front of her. The column of light falls on her — only on her — and in it, after an act and a half of silence, she finds her voice. <em>"It's taking place now. It happens all the time."</em> The pianist's music dies on her cry. By accident, a stagehand drops the curtain. Interval.</p>
  </section>

  <section class="act">
    <h2 class="section"><span class="roman">Act Three</span>The argument, the refusal, the fountain</h2>
    <p class="subheading">The garden, in the dark</p>

    <p>Almost all the light is gone. The stage is dark; a single low fountain basin sits at the centre of it, lit pale-blue from inside, the colour of water in a public garden at night. A single bare bulb hangs above the Manager's table, swinging very slightly, the working light of a director who has stopped trying to make this beautiful. The chair-and-coat is at the side of the stage; nobody has decided yet what to do with it.</p>

    <p>The Father, by now, has come to believe there is a real play in what his family has carried in. He launches into the philosophical argument he has been preparing all morning: that a character is more real than the actors who would play him, because the actors change and the character cannot. The Step-Daughter cuts him three times across the part — surgically, precisely, each cut a step further than the one before. <em>"His reality. He always knew exactly where to find me."</em> She has stopped letting him explain.</p>

    <p>The Manager turns, finally, to the Son, who has refused to speak for two acts. He is asked to play the scene at the fountain. He refuses. The Father, in frustration, grabs his arm at <em>"You can force him, sir"</em> — and a single sharp note from the piano, like a slap, sounds in the dark. The Son does not give him the scene. But — because he has, after all these years, decided to say one true sentence — he does at last tell the room what he saw on that afternoon in the garden of his father's house: he was running toward the fountain to save the Child, and when he was a single step from the water the sight of the Boy's face froze him. He stopped. He did not jump in. The Child drowned in the time it took him to stop.</p>

    <p>As he speaks, the Step-Daughter takes the wrapped bundle to the basin. She bends over the water and lowers the bundle into it. The basin's walls hide the drowning from view; nobody can see inside. The stage lights drop slowly, breath by breath, as the Son's narration unfolds, until only the fountain's pale-blue interior and the bare hanging bulb remain. The chair-and-coat is silhouetted behind the basin for ten seconds — the Boy watching his drowned sister. Then full blackout.</p>

    <p>Out of the dark, from where the chair-and-coat is, a single revolver shot rings out. The Mother cries out. The lights snap back up. The actors lift what they think is the Boy's body — which is the chair-and-coat now being carried as a body, heavy, with care. Some say he is dead. Others say it was only pretence. The Father, with a terrible cry: <em>"Pretence? Reality, sir, reality!"</em> The Manager has had enough.</p>

    <div class="pull-quote">
      "Pretence? Reality? To hell with it all! I've lost a whole day over these people. A whole day."
    </div>

    <p>The Manager walks out. The lights go down. The first phrase of Arvo Pärt's <em>Spiegel im Spiegel</em> opens, plays for ten seconds, and stops. Curtain.</p>
  </section>

  <section class="closing">
    <h2 class="section"><span class="roman">After</span>What the audience leaves with</h2>

    <p>The play does not resolve. The family is not put right. The Child is dead; the Boy has shot himself, or has only seemed to, depending on which character you believe. The Step-Daughter has run from the stage. The Father is still arguing. The Mother is still grieving. The Son has, after all these years, said his one true sentence. The Manager has walked out admitting nothing.</p>

    <p>The audience walks out into the Lausanne autumn carrying it. Some are angry. Some are silent. Some do not yet know what they think. The play has been working out exactly that effect, on exactly that audience, in exactly that night air, for one hundred and five years — and it will work it out again tonight, on whoever has come.</p>

    <p>The discomfort the audience leaves with is the play. If they leave comforted, something has gone wrong.</p>
  </section>

  <footer class="foot">
    <p><strong>Village Players · Lausanne</strong> &nbsp;·&nbsp; Director: Kiarash Jamshidi</p>
    <p>For the full text, see the Director's Copy and the Actor Rehearsal Script. The base translation is Edward Storer's 1922 English version of Pirandello's <em>Sei personaggi in cerca d'autore</em> (1921), in the public domain via Project Gutenberg Australia.</p>
  </footer>

</main>

</body></html>
"""

HTML_PATH = OUT_DIR / "synopsis.html"
HTML_PATH.write_text(HTML)

OUT = OUT_DIR / "synopsis.pdf"
with sync_playwright() as p:
    launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
    browser = p.chromium.launch(**launch_kwargs)
    page = browser.new_page()
    page.goto(f"file://{HTML_PATH.resolve()}", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(600)
    page.pdf(path=str(OUT), format="A4",
             margin={"top": "22mm", "right": "24mm", "bottom": "22mm", "left": "24mm"},
             print_background=True, prefer_css_page_size=True)
    browser.close()

try:
    from pypdf import PdfReader
    r = PdfReader(str(OUT))
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes) · {len(r.pages)} pages")
except BaseException:
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes)")
