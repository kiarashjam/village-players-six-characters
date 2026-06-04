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
    <p>The whole story of the play, told straight through — from the years before the curtain rises to the moment after it falls. Plain narrative voice, no directorial commentary, no staging notes — but written in the register the production lives in: a daylight surface with a much older shadow underneath.</p>
    <p>The play has two stories inside it. There is a <strong>family tragedy</strong> — a marriage that did not survive its own silence, a secretary who took the place a husband had emptied, four children by two men, a small shop above a courtyard off the rue de Bourg, a hundred francs in a pale blue envelope, a fountain in a garden no one was watching. And there is a <strong>theatrical present</strong> in which six figures from that family tragedy walk onto a working company's stage, one morning, and ask, very politely, to be staged.</p>
    <p>The family story is told only in pieces, because the family itself can only ever tell it in pieces. The theatrical story is what the audience watches happen.</p>
    <p>What follows tells the family story first — in the order it happened, as far as the play lets us see it — and then walks the audience's view of the play, act by act.</p>
  </section>

  <section class="backstory">
    <h2 class="section"><span class="roman">Before</span>What happened before the play begins</h2>
    <p class="subheading">The family story, in the order it happened</p>

    <p>Years before the play opens — in a town that, in this production, is Lausanne — a man and a woman were married.</p>

    <p>He was a man of restless intelligence and unhappy temper; she was simple, gentle, and almost silent. They had one son. The marriage did not survive the silence between them. He could not bear her tenderness, or his own coldness toward it; she could not bear how clearly that coldness was directed at her. They did not separate cleanly. They erased each other slowly, across years, in small daily ways, until what was left between them was a shape without weather inside it.</p>

    <p>He kept a clerk in his service — a secretary, quiet, faithful, of a temperament close to his wife's. He watched the two of them, across months, find each other in small silent ways: a glance over a teacup, a hand near a door, the slight softening that two gentle people make in the presence of a third who is not. He told himself — afterwards, at any rate — that what he did next he did for both of them. He sent his secretary away. Then, because he could no longer bear watching his wife wander the empty rooms of his house, as he himself, much later, would put it, <em>like an animal one has taken in out of pity</em>, he sent her away too, after the secretary, to live with him in another town. The small son was left behind in the country, raised by a wet-nurse — a peasant woman with rough hands and no soft words — and saw nothing of either of his parents for the rest of his childhood.</p>

    <p>He told himself, then and afterwards, that what he had done was a kind of generosity. He had been generous, perhaps. Generosity is one of the names a man gives to a thing he does not wish to look at directly.</p>

    <p>Years passed. The wife and the secretary built a quiet life. They had three more children together — a daughter first, then a boy, then a small girl. They lived in modest comfort. The husband, from a distance, kept watch. He never made himself known to them. He went, more than once, to the gate of the eldest daughter's school, in the afternoon when the children came out among the trees, and waited there with little parcels — a fine straw hat one day, a bouquet of flowers another. He gave them to the child, gently, and walked away. She received them with the polite confusion of a young girl who has been told to be kind to strangers. He never told her his name. The wife and her new family never knew he had been there. <em>He came, sir,</em> as the Step-Daughter will say much later, very flatly, in front of strangers, <em>to see how I was growing up.</em></p>

    <p>He told himself, then and afterwards, that what he felt was a father's affection. It is the sort of thing a man can tell himself, in the dark, for a very long time, before he is forced to hear it said back to him by somebody else.</p>

    <p>Then the secretary died.</p>

    <p>The wife and her three children fell out of comfort, then out of security, then out of dignity. They moved to a smaller town — in the production's relocation, to Lausanne — and took rooms above a shop in a poor street. The eldest daughter put on the mourning her mother could not afford to lay off. The wife began to do piecework sewing for a small dressmaker called Madame Pace, whose atelier sat off the rue de Bourg in a courtyard near Saint-François.</p>

    <p>Madame Pace's dressmaking was the public side of her trade. The back rooms of her atelier did other business — quiet business, polite business, transacted in cash by gentlemen who paid for half an hour and left without leaving names — that the town, by a long habit nobody quite remembered the start of, had agreed not to look at too closely. Madame Pace herself was elegant, practical, smiling, fluent in three half-languages, and morally rotten in a way nobody who walked into her shop in good shoes ever wanted to name. She kept a book. The book, she would say later, had to balance.</p>

    <p>The mother's sewing was poor. Her hands had begun to shake at the end of long days; the silk she was given was the most expensive cloth in the shop. She ruined it, and the costs mounted on Madame Pace's book, and Madame Pace, smiling, over tea, suggested one afternoon — in the soft voice a kind landlady uses to suggest a thing — that the eldest daughter, eighteen years old, two months an orphan, still in full mourning for her father, might be persuaded to help to settle the debt by spending one or two afternoons in the back room. The daughter agreed because the children at home were thin and the alternative was the family going hungry. She had been working at the atelier for some weeks when a particular customer came in: a middle-aged man in a good coat, polite, soft-voiced, with the small grooming gestures of a man who has rehearsed kindness across his whole life. He laid a hundred francs, in a pale blue envelope, on a little mahogany table beside the bed. He asked the new girl, very gently — <em>in the voice men use for children</em>, the Step-Daughter will say later — to take her little black dress off.</p>

    <p>He was her stepfather.</p>

    <p>He did not recognise her; he had only seen her once, briefly, outside the gate of her school, and she had grown. She did not recognise him; she had been too small the last time he had been in her mother's house to remember his face. They were one or two minutes from a transaction neither of them would ever live down when the mother — at the shop that afternoon herself — walked through the door, and saw what was about to happen, and recognised her husband, and the whole room shattered into a place from which no character inside it would ever afterwards recover. The Father will say, much later, in front of strangers, that the mother arrived <em>in time</em>. The Step-Daughter, who was inside the room, will reply only: <em>Almost.</em></p>

    <p>The Father took them all home with him — there was nowhere else for them to go. The young Son, raised alone in the country, was brought back, and found himself sharing a house with a mother he did not know, three half-siblings he had never met, and a stepfather he had decided to despise before he understood why. He withdrew into a corner of a room that was no longer anyone's, and stopped speaking. He has been keeping the same silence ever since.</p>

    <p>What happened after that, the family will not tell in order. They will let it slip across the rest of the play, in fragments, as if it were a thing they could not afterwards look at directly even at the distance of a stage.</p>

    <p>There was a garden behind the house. At the middle of the garden there was a low stone fountain with grey walls and a little still water in the basin that nobody had remembered to change. The small Child wandered there in the afternoons, untended, because there was no longer anyone in the house with the strength to watch a four-year-old at play. The fourteen-year-old Boy walked behind her in silence, his hands in the pockets of his school coat. In one of those pockets — for how long nobody in the family could afterwards say — he had been carrying a revolver.</p>

    <p>One afternoon, when nobody was looking, the small Child fell into the fountain. The Boy did not move. He stood at the side of the basin, his hands still in his pockets, and watched her drown.</p>

    <p>The young Son, hearing the splash from somewhere in the house, ran across the garden — was a single step from the water — was about to jump in — and was frozen at the threshold by the sight of the Boy's face. He stopped. He did not move. The Child died in the few seconds it took him to stop. Soon afterwards, the Boy used what was in his pocket.</p>

    <p>This is the story the play is about. The play itself begins long afterwards, somewhere else entirely, on a stage where none of these people are expected.</p>
  </section>

  <section class="act">
    <h2 class="section"><span class="roman">Act One</span>The Six arrive at a rehearsal</h2>
    <p class="subheading">The theatre company is interrupted</p>

    <p>The curtain rises on a working theatre company at SSA Lausanne, preparing for an evening's rehearsal. The Manager sits at his table with a script he does not particularly like — Pirandello's <em>Mixing It Up</em>, of all things. His three Players, all working actors, are getting into position. The Leading Man is complaining about being asked to wear a cook's cap in the opening scene. The Leading Lady, who is also doing the props this season because the company can no longer afford a Property Man, is building a folding screen out of two old flats and a hinge she bought yesterday. The youngest in the company, serving as Prompter, is taking dictation about the set in a shorthand she is privately a little proud of. The Manager is arguing with everyone, and behind on the morning.</p>

    <p>For the first ten minutes, this is comedy.</p>

    <p>Then the door at the back of the stage opens. The Door-keeper comes in, carrying a wooden chair. He sets the chair at the edge of the stage. He lays a folded black coat over the back of it, places a schoolboy's cap on the seat, and sets a small leather satchel on the floor by the leg. He has not yet spoken. The Manager has not yet looked up.</p>

    <p>Behind him, four figures walk onto the stage in mourning. A man of about fifty. A heavily veiled woman beside him, her eyes downcast. A young woman in elegant black, carrying a small wrapped bundle of white cloth with a black silk sash against her shoulder. A tall young man at the back, who looks — as Pirandello specifies — as if he had come on stage against his will. The chair is the silent fourteen-year-old <strong>Boy</strong>. The bundle is the small four-year-old <strong>Child</strong>. Both are children of this family. Neither will be played by a performer. The audience reads them as the children, within the first minute, because the family does.</p>

    <p>What follows is not, exactly, a play yet. It is a family standing on a working stage and asking, in front of strangers, to be staged.</p>

    <p>The Manager refuses, by turns, then demurs, and at last — against his own better judgement — listens. The <strong>Father</strong>, lit in a tenuous amber, lays out the philosophy he will return to all morning: a character is fixed forever in what he is; an actor goes home at night and becomes someone else, but a character has no other room to live in, and no other hour. He speaks like a man who has rehearsed the argument privately, for a long time, in a quiet room.</p>

    <p>The <strong>Step-Daughter</strong> has heard the philosophy before. She does not wait for him to finish. With one or two sentences — short, precise, surgical — she breaks it open. There was a hundred francs, she says, in a pale blue envelope, on a little mahogany table, in the back room of a dressmaker's shop. <em>You know Madame Pace, sir.</em> She is two months an orphan. She is in mourning. The man in the good coat — and the room understands it half a beat before her sentence ends — was her own stepfather. Her own mother walked through the door.</p>

    <p>The Father reaches for the philosophy again, as if it might still cover him. The <strong>Mother</strong>, hearing all this said aloud in a room of strangers, very nearly faints. The Father, in his agitation, lifts her veil against her will — the way a man lifts a thing he does not wish to look at directly because he wants other people to see it. The young <strong>Son</strong> says nothing. He has been deciding, for a long time, not to.</p>

    <p>By the end of the act the comedy of the morning has burned off entirely. The amber light has crept, almost without anyone noticing, to a low blood-coloured wash. The working company has fallen silent around the family standing inside its own argument. The Manager has agreed — partly because he believes there may be a play in this, partly because he no longer has a morning to recover — to try to stage what happened.</p>

    <p>The first interval is twenty minutes long. The audience walks out into the lobby for a drink. They do not yet quite know what they have just agreed to listen to.</p>
  </section>

  <section class="act">
    <h2 class="section"><span class="roman">Act Two</span>The staging attempt, and the doubled scene</h2>
    <p class="subheading">The dressmaker's shop, played twice</p>

    <p>When the audience comes back, the stage has been transformed onto two levels. The upper platform is where the family's drama will be played. The lower floor is where the working company stays, watching.</p>

    <p>The Step-Daughter erupts onto the upper platform with the wrapped bundle in her arms and the chair-and-coat dragged behind her. She has just lost an argument with the Manager backstage that the audience did not see, and losing it has not made her gentler. The rest of the stage drops to dark. A single tight column of light falls on her, and on her only.</p>

    <p>Alone in that column, with a pianist playing Satie's slow <em>Gymnopédie</em> underneath, she speaks to her two silent siblings. The bundle in her arms she addresses as a frightened four-year-old in a strange room. The chair-and-coat, mid-speech, she turns to and addresses as her brother. She takes the coat by the sleeve as if she were taking him by the arm. She slides her hand into the coat pocket and pulls out a revolver. She holds it, briefly, in the column of light. Then she returns it, gently, to the pocket where she found it.</p>

    <p>The audience watches a young woman speak with great love to a piece of cloth and with great contempt to a piece of furniture, and decides — quietly, without being asked — to believe both.</p>

    <p>The shop has to be summoned. The Property Man wheels the folding screen into position. The little mahogany table is placed on the upper platform. A row of pegs is set up for hats. A small sign appears against the back wall: <em>robes et manteaux</em>. The Father takes a position outside the screen; the Step-Daughter takes a position inside.</p>

    <p>And then, in the production's strangest single moment, something the audience does not understand for the next five seconds begins to happen.</p>

    <p>The youngest in the company — who has been keeping shorthand all evening from her box on the lower floor — steps out of the box. She walks up to the platform without looking at anyone. She enters a wig. She enters a corset. She enters a heavy black silk dress and a long silver chain at her waist ending in a pair of scissors. She is no longer the youngest in the company. She is <strong>Madame Pace</strong>, who has been keeping a small dressmaker's shop in Lausanne for forty years, and the front door has rung, and a new customer is here.</p>

    <p>She speaks half in Italian, half in French — the broken speech of a foreigner who has lived in this town too long to speak the language properly, and not long enough to forget her first. The audience laughs at her first line. <em>Cara. You come back to me. I knew you come back.</em> The laughter sounds, in the room, like a small accident the audience cannot afterwards explain.</p>

    <p>She and the Step-Daughter play the scene of the atelier the way it happened. Madame Pace recites her bookkeeping — the man who rinses his hands at the basin first and then again after, the blue envelope on the little mahogany table, the names that belong to him for half an hour, the customers like the bells of Saint-François, three times a week. The audience laughs at her first line and stops laughing somewhere in the middle of the second.</p>

    <p>And then, surprising even herself, the Mother breaks her silence for the first time in the play. She has been quiet for an act and a half. She erupts upward, from the lower floor: <em>"You old devil! You murderess!"</em> — and the voice does not stop where it usually would. She names the kitchen, the tea, the Wednesdays and Fridays and sometimes the Sundays, the silk her hands had ruined; she confesses that she half-knew, and let herself not know, because if she had known the children at home would not have eaten. She spends what she has, and the Step-Daughter calms her, and Madame Pace exits — unhurried, smiling, mentioning the girl who comes after, on Tuesday afternoons, who looks a little like her — and the Mother is restored to her silence.</p>

    <p>The company's own Leading Lady and Leading Man then climb onto the upper platform and play the same scene over again as <em>theatre</em>, with the bundle and the chair-and-coat watching from below. The Step-Daughter, on the lower floor now, laughs at the working actors trying to be her. The laugh is the wound. The Leading Lady, who has played leads at every house in this canton, has been made a fool of by better, and she means it.</p>

    <p>The Mother is forced to watch her daughter's worst hour staged in front of her, twice. The column of light falls on her — only on her — and the voice she found earlier with Madame Pace comes back, larger this time, the keystone of the production:</p>

    <p><em>"It's taking place now. It happens all the time."</em></p>

    <p>The pianist's music dies on her cry. By accident, a stagehand drops the curtain. Lights up, slowly, on a house that is no longer thirsty.</p>
  </section>

  <section class="act">
    <h2 class="section"><span class="roman">Act Three</span>The argument, the refusal, the fountain</h2>
    <p class="subheading">The garden, in the dark</p>

    <p>Almost all the light is gone.</p>

    <p>The stage is dark. A single low fountain basin sits at the middle of it, lit pale-blue from inside — the colour of public-garden water at the hour when nobody is watching. Above the Manager's table, a single bare bulb hangs and swings, very slightly, as if a door had closed somewhere offstage and no one had heard. The chair-and-coat is at the side of the stage. Nobody has decided yet what to do with it.</p>

    <p>A low sustained note plays underneath the whole of what follows. The audience never quite hears it. They feel that the room has a pulse.</p>

    <p>The Father, by now, has come to believe there is a real play in what his family has carried in. He launches into the philosophical argument he has been preparing all morning: that a character is more real than the actors who would play him, because the actors change and the character cannot. He speaks beautifully. He speaks at length. He has, in this voice, talked his way out of a great many rooms.</p>

    <p>The Step-Daughter cuts him three times across the part.</p>

    <p>She does not raise her voice. She does not move much. She cuts him with one short sentence, then another, then a third, each one sharper and a little further than the one before. <em>"His reality. He always knew exactly where to find me."</em> The drone dies on her third cut. The Father, by the end of it, has stopped trying to win.</p>

    <p>The Manager turns, finally, to the Son. The Son has not spoken in two acts. He has been sitting in a chair the audience has almost forgotten about. The Manager asks him to play the scene at the fountain. The Son refuses. The Father, in his frustration, grabs his arm at <em>"You can force him, sir"</em> — and a single sharp note from the piano, like a slap, sounds in the dark. The Son does not give him the scene.</p>

    <p>But — because he has, after all these years, decided to say one true sentence — he does at last tell the room what he saw on that afternoon in the garden of his father's house.</p>

    <p>He saw the small Child by the fountain. He saw the Boy beside her, watching. He ran. He was a single step from the water. He was about to jump in. The sight of the Boy's face froze him. He stopped. He did not move. He has not, in some sense, moved since.</p>

    <p>As he speaks, the Step-Daughter takes the wrapped bundle to the basin. She bends over the water and lowers the bundle into it. The basin's walls are too high for anyone — neither the audience nor the live actors — to see inside. The drowning happens in plain sight, in an unseeable space.</p>

    <p>The stage lights drop, breath by breath, beneath the Son's narration, until only the fountain's pale-blue glow and the bare hanging bulb remain. The chair-and-coat is silhouetted behind the basin. For ten seconds, in that low water-light, the audience sees the Boy watching his drowned sister.</p>

    <p>Then full blackout.</p>

    <p>Then, out of the dark, from where the chair-and-coat is, a single revolver shot.</p>

    <p>The Mother cries out. The lights snap back. The actors lift what they think is the Boy's body — which is the chair-and-coat now being carried as a body, heavy, careful, terrible.</p>

    <p>Some say he is dead. Others say it was only pretence.</p>

    <p>The Father, with a terrible cry, the only time in the play he raises his voice — <em>"Pretence? Reality, sir, reality!"</em></p>

    <p>The Manager has had enough.</p>

    <div class="pull-quote">
      "Pretence? Reality? To hell with it all. I've lost a whole day over these people. A whole day."
    </div>

    <p>He walks out. The lights drop again. Out of the dark, the first phrase of Arvo Pärt's <em>Spiegel im Spiegel</em> opens, plays for ten seconds, and stops. Curtain.</p>
  </section>

  <section class="closing">
    <h2 class="section"><span class="roman">After</span>What the audience leaves with</h2>

    <p>The play does not resolve. The family is not put right. The Child is dead. The Boy has shot himself, or has only seemed to, depending on which of the actors on stage you decide to believe. The Step-Daughter has run from the stage, and from the play. The Father is still arguing. The Mother is still grieving. The Son has, after all these years, said his one true sentence and gone quiet again. The Manager has walked out without quite admitting what he has just watched.</p>

    <p>He is the closest thing on the stage to the audience itself. His exhaustion at the end is the audience's exhaustion, said aloud, by their proxy, before they have had the chance to say it for themselves. He has done them the small kindness of saying it for them — and the larger, less kind thing, which is the production: he has condemned them with it in the same breath.</p>

    <p>The audience walks out into the Lausanne autumn carrying that. Some are angry. Some are silent. Some do not yet know what they think. The play has been working out exactly that effect, on exactly that audience, in exactly that night air, for one hundred and five years — and it will work it out again tonight, on whoever has come.</p>

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
