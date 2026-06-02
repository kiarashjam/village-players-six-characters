#!/usr/bin/env python3
"""Build the Audition Briefing PDF.

A director's briefing for the audition room — one page per role for four
anchor characters (Father, Manager, Player 1, Player 3). Each page gives
the look, the behaviour, the tone of speaking, what to coach against,
plus a three-sentence solo monologue the auditioner can read alone, and
a "what to listen for" note for the director's ear.

For Player 3, includes a short Madame Pace transformation test on the
same page.
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
<title>Audition Briefing — Six Characters in Search of an Author</title>
<style>
  :root { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }
  @page { size: A4; margin: 20mm 22mm 20mm 22mm; }
  *,*::before,*::after { box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif;
    font-size: 11pt; line-height: 1.6; margin: 0; padding: 0; }
  main { max-width: 168mm; margin: 0 auto; }

  /* Masthead */
  .masthead { text-align: center; margin-bottom: 7mm; padding-bottom: 5mm;
              border-bottom: 1px solid var(--rule); }
  .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600;
             font-size: 9pt; letter-spacing: 0.26em;
             text-transform: uppercase; color: var(--accent);
             margin: 0 0 4mm 0; }
  h1 { font-family:'Cormorant Garamond',serif; font-weight: 500;
       font-size: 21pt; line-height: 1.15; margin: 0 0 2mm 0; }
  .play { font-style: italic; font-size: 11pt; color: var(--ink-soft);
          margin: 0 0 3mm 0; }
  .credit { font-size: 10.5pt; color: var(--ink); margin: 0; letter-spacing: 0.04em; }

  /* Intro */
  .intro h2 { font-family:'Cormorant Unicase',serif; font-weight: 600;
              font-size: 11pt; letter-spacing: 0.20em;
              text-transform: uppercase; color: var(--accent);
              margin: 7mm 0 3mm 0; }
  .intro p { margin: 0 0 3mm 0; }
  .intro ul { margin: 0 0 3mm 0; padding-left: 6mm; }
  .intro li { margin-bottom: 2mm; line-height: 1.55; }

  /* Role pages */
  .role { page-break-before: always; }
  .role-head { border-bottom: 2px solid var(--accent);
               margin-bottom: 5mm; padding-bottom: 2mm; }
  .role-head h2 { font-family:'Cormorant Garamond',serif; font-weight: 500;
                  font-size: 23pt; color: var(--accent); margin: 0; }
  .role-tag { font-style: italic; color: var(--ink-soft);
              margin: 1mm 0 0 0; font-size: 11pt; }

  h3 { font-family:'Cormorant Unicase',serif; font-weight: 600;
       font-size: 10pt; letter-spacing: 0.18em;
       text-transform: uppercase; color: var(--accent);
       margin: 5mm 0 2mm 0; }

  p { margin: 0 0 2.5mm 0; }
  ul { margin: 0 0 3mm 0; padding-left: 6mm; }
  li { margin-bottom: 2mm; line-height: 1.55; }
  strong { color: var(--ink); }

  /* The solo callout */
  .solo { border-left: 3px solid var(--accent);
          padding: 5mm 7mm 4mm 7mm;
          margin: 5mm 0 3mm 0;
          background: rgba(255,255,255,0.30);
          page-break-inside: avoid; }
  .solo .solo-label { font-family:'Cormorant Unicase',serif; font-weight: 600;
                      font-size: 9pt; letter-spacing: 0.20em;
                      text-transform: uppercase; color: var(--accent);
                      margin: 0 0 3mm 0; }
  .solo .solo-text { font-family:'EB Garamond',serif; font-size: 11.5pt;
                     line-height: 1.65; margin: 0; color: var(--ink); }

  /* "What to listen for" — a softer secondary callout */
  .listen { border: 1px solid var(--rule);
            padding: 3mm 5mm; margin: 0 0 4mm 0;
            background: rgba(255,255,255,0.22);
            page-break-inside: avoid; }
  .listen .listen-label { font-family:'Cormorant Unicase',serif; font-weight: 600;
                          font-size: 9pt; letter-spacing: 0.18em;
                          text-transform: uppercase; color: var(--accent);
                          margin: 0 0 2mm 0; }
  .listen p { margin: 0; font-size: 10.5pt; line-height: 1.6; }

  /* Madame Pace mini-card on Player 3's page */
  .pace-card { border-top: 1px dashed var(--rule);
               margin-top: 5mm; padding-top: 4mm;
               page-break-inside: avoid; }
  .pace-card .pace-label { font-family:'Cormorant Unicase',serif; font-weight: 600;
                           font-size: 9pt; letter-spacing: 0.20em;
                           text-transform: uppercase; color: var(--accent);
                           margin: 0 0 2mm 0; }

  footer.foot { margin-top: 9mm; padding-top: 4mm;
                border-top: 1px solid var(--rule);
                font-size: 9.5pt; color: var(--ink-soft);
                font-style: italic; text-align: center; line-height: 1.55; }
  footer.foot strong { font-style: normal; color: var(--ink); }
</style>
</head><body>

<main>

  <div class="masthead">
    <p class="eyebrow">Audition Briefing &nbsp;·&nbsp; Four Anchor Roles</p>
    <h1>Six Characters<br>in Search of an Author</h1>
    <p class="play">Sei personaggi in cerca d'autore &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
    <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne &nbsp;·&nbsp; late autumn 2026</p>
    <p class="credit" style="margin-top:6px;">Director: <strong>Kiarash Jamshidi</strong></p>
  </div>

  <section class="intro">
    <h2>What this is</h2>
    <p>A director's briefing for the audition room, covering four of the eight speaking roles: <strong>the Father, the Manager, Player 1, and Player 3</strong>. For each role, one page: what the character should look like, how they should behave, the tone of speaking, what to coach against — and a <strong>three-sentence solo monologue</strong> the auditioner can read alone, cold or prepared. Each solo is written to show the character's whole personality in a minute or less.</p>

    <h2>How to use it in the room</h2>
    <ul>
      <li><strong>Prepared first.</strong> Let the auditioner read the solo once as they have prepared it. Do not interrupt.</li>
      <li><strong>One adjustment, then read it again.</strong> A single redirection — "play it quieter"; "play the third sentence as if you were telling it to your closest friend"; "start it as if you have just walked in" — tells you more about their range than the first read does.</li>
      <li><strong>Watch the body, not just the voice.</strong> Where does the chin go on a vain line? Where does the breath shorten on a shameful one? Does the auditioner stay still during a silence, or fill it?</li>
      <li><strong>For Player 3, optionally</strong>, the page also includes a short Madame Pace transformation test. Run it only if the auditioner is in contention for the role — that one tells you whether the transformation is in them.</li>
    </ul>

    <p>These solos are not from the play itself. They are short audition pieces composed for this audition only, in each character's voice as written in the Director's Copy. They will not be performed in the production.</p>
  </section>

  <!-- ============================================================ -->
  <!-- THE FATHER                                                   -->
  <!-- ============================================================ -->

  <section class="role">
    <div class="role-head">
      <h2>The Father</h2>
      <p class="role-tag">the brain of the family — philosophy as confession</p>
    </div>

    <h3>Look</h3>
    <p><strong>Around 50.</strong> Hair reddish, thinning at the temples but not bald. Thick moustaches over a still-fresh mouth. Fattish, pale, with a wide forehead. <strong>Blue oval-shaped eyes — clear and piercing,</strong> which go sharper the moment he is interrupted. Costume: mourning. Dark morning coat, dark trousers, white shirt, dark tie. The look of an educated middle-class man at his neighbourhood lawyer's office. <strong>Body:</strong> heavy but contained — the body of a man who has thought a great deal more than he has moved. He should look capable of dignity.</p>

    <h3>Behaviour</h3>
    <p>A man who arrives carrying the worst hour of his life and wants to be allowed to be <em>more than that hour</em>. <strong>Mellifluous when he is in control of his argument</strong> — almost charming, the cadence of a man who has rehearsed his case many times privately. The instant his argument is broken, the body shifts: heat at the brow, breath shortening, the small adjustments of a man who would prefer to be elsewhere. <strong>He sweats. Not as a prop — physiologically.</strong> The body confesses what the mouth refuses to admit. He recovers his composure when he is winning the argument; he loses it when he is not.</p>

    <h3>Tone of speaking</h3>
    <p><strong>Long, circling, philosophical sentences.</strong> He talks himself in spirals because the spiral is the only thing keeping the shame from arriving in a straight line. Educated, articulate, sometimes elegant — the vocabulary of a man who has read his Schopenhauer. Vocal range from warm-priestly (Act One, the metaphysics) to broken and uneven (Act Three, after the Step-Daughter's three cuts). <strong>He never shouts.</strong> Even his rage is articulate.</p>

    <h3>Coach against</h3>
    <ul>
      <li><strong>Self-pity.</strong> He would love to be pitiable. He is not.</li>
      <li><strong>Becoming a villain.</strong> A villain is grand — and being grand would let him off. Play him ordinary, certain he was being kind.</li>
      <li><strong>Demonstrating shame.</strong> The shame is in the body's involuntary responses. The mouth keeps trying to escape it.</li>
    </ul>

    <div class="solo">
      <p class="solo-label">Three-sentence solo &nbsp;·&nbsp; read alone</p>
      <p class="solo-text">"You think me ridiculous, I can see it from here — a man of fifty, in a borrowed black coat, asking strangers to please believe my philosophy at half past ten in the morning. But the philosophy, sir, is not a flourish; it is the precise instrument I have built across the worst years of my life to keep one half-hour in a back room from being the whole of me — and if you take the instrument away from me, there is nothing left for me to stand in front of you with except the man who once paid a hundred francs in that room. That, gentlemen, is not a play; it is the end of the world, said quietly, in a shop."</p>
    </div>

    <div class="listen">
      <p class="listen-label">What to listen for</p>
      <p>The long circling sentences, the articulate self-awareness, the philosophy as cover, the shame arriving in the last clause. Can the auditioner hold the breath across the dashes? Does the body go small on <em>"the man who once paid a hundred francs"</em>? The closing image — <em>"the end of the world, said quietly, in a shop"</em> — should land flat, not dramatic. Quiet is the role.</p>
    </div>
  </section>

  <!-- ============================================================ -->
  <!-- THE MANAGER                                                  -->
  <!-- ============================================================ -->

  <section class="role">
    <div class="role-head">
      <h2>The Manager</h2>
      <p class="role-tag">the audience's body on stage — pragmatic, tired</p>
    </div>

    <h3>Look</h3>
    <p><strong>Late 50s.</strong> Looks like a man who runs a theatre. The kind of figure the audience would not look twice at in a Lausanne café. Costume: working-rehearsal clothes — comfortable mid-day clothes, slightly rumpled, the warm slightly-tired look of an experienced amateur director at his Thursday rehearsal. No glamour. <strong>He should look more like a member of the audience than like a character.</strong> This is critical: he <em>is</em> the audience's body on stage.</p>

    <h3>Behaviour</h3>
    <p>Arrives furious that the morning is being wasted. Gets ready to throw the Six out. Then he starts to listen — and the audience does the same thing. Sits at his table the way the audience sits in their seats: forward, slightly bored, half-engaged. When the play becomes uncomfortable, <strong>he looks down</strong> — the way the audience does when something on stage is more than they want to look at. The production's hinge: in Act Three he picks up the chair-and-coat himself and sets it behind the fountain. <strong>That gesture is the moment he stops being audience and becomes accessory.</strong> Then he walks out, says the line, curtain.</p>

    <h3>Tone of speaking</h3>
    <p>Pragmatic, conversational, often impatient. The voice of a man behind on his day's work. <strong>Short sentences. Direct questions.</strong> Practical vocabulary. Verbal tics to score — these are the audience's own thoughts, said out loud: <em>"I don't understand this at all." "Yes, yes, I know this." "Where does all this take us?" "Let's hear them out."</em> <strong>Cynicism is technique; compassion is real.</strong> He has learned to talk over his feelings, but the feelings are under there.</p>

    <h3>Coach against</h3>
    <ul>
      <li><strong>Becoming a buffoon.</strong> He almost understands what he is watching. Do not let him become a clown.</li>
      <li><strong>Becoming a hero.</strong> He is the man who walks out without quite admitting what he just saw.</li>
      <li><strong>Modern director-clichés.</strong> He runs an amateur company in Lausanne. He is not Stanislavski.</li>
    </ul>

    <div class="solo">
      <p class="solo-label">Three-sentence solo &nbsp;·&nbsp; read alone</p>
      <p class="solo-text">"I came in this morning to rehearse Pirandello — which my Leading Man already considers a personal affront — and now six strangers in mourning have walked onto my stage to ask, very politely, whether I will put their family on at the weekend. I keep looking at my watch, and the watch insists we are still in the same minute we were in twenty minutes ago, which is, in my professional view, the technical definition of a bad day for a working director. I have a wife expecting me home at a reasonable hour, an electrician I have not paid since the summer, and a Leading Man currently arguing with me about a cook's cap — and yet, against every instinct I have learned in thirty years of this trade, I find I have not thrown them out."</p>
    </div>

    <div class="listen">
      <p class="listen-label">What to listen for</p>
      <p>Pragmatic, conversational, <em>tired</em>. The cynicism is technique; the compassion is real. The button — <em>"I find I have not thrown them out"</em> — should land flat, not with a wink. He is admitting something he did not want to admit, in the voice of a man counting the minutes. If the auditioner plays the line for irony, redirect: "say it as if you've just surprised yourself."</p>
    </div>
  </section>

  <!-- ============================================================ -->
  <!-- PLAYER 1                                                     -->
  <!-- ============================================================ -->

  <section class="role">
    <div class="role-head">
      <h2>Player 1 — the Leading Man</h2>
      <p class="role-tag">vain, faded, defensive, and entirely sincere</p>
    </div>

    <h3>Look</h3>
    <p><strong>Mid-50s.</strong> Looks like a Leading Man who has been a Leading Man for too long. There is a smartness to him that is half real and half rehearsed. Costume: working clothes of a working actor, but slightly more groomed than the others — collar a bit crisper, hair a bit more arranged. The vanity shows. For the functions he doubles into (the cook's cap, the Door-keeper's cap, L'Ingénue), <strong>the change of hat is the only costume change.</strong> The body remains him.</p>

    <h3>Behaviour</h3>
    <p>Vain, faded, defensive, and entirely English in a city that has not given him the career he was promised. He came to Lausanne fifteen years ago believing it was a stepping stone to Paris. Paris did not happen. London does not call. Name-drops productions from years ago that nobody remembers, and one production he was <em>nearly</em> cast in, which was almost the West End. <strong>Believes he is the senior actor in the company. He is wrong</strong> — Player 2 is. He performs seniority; she has it. Plays five functions, all of them as himself in different hats: the Door-keeper still has his self-importance; the Machinist still has his opinions; L'Ingénue is the joke he doesn't quite get is on him.</p>

    <h3>Tone of speaking</h3>
    <p>An Anglo English he thinks of as classical and the audience hears as just <em>English</em>. He speaks the way he imagines a Leading Man speaks. The lines stretch — he gives weight to every clause, and believes any sentence he speaks improves on contact with his voice. <em>"I'd sooner resign"</em> — said every season around the first read-through, never delivered. <strong>Play the bluff.</strong> The voice goes higher and slightly faster when he is offended. The chin goes up.</p>

    <h3>Coach against</h3>
    <ul>
      <li><strong>Camp.</strong> He is vain, but not camp. The comedy is in the <em>sincerity</em>.</li>
      <li><strong>Lovability.</strong> He is irritating, and very faintly endearing because he is sincere. Resist softening him too early.</li>
      <li><strong>Modern-actor jokes.</strong> No theatre-school jargon, no "devised work," no agent jokes. The comedy is character, not cleverness.</li>
    </ul>

    <div class="solo">
      <p class="solo-label">Three-sentence solo &nbsp;·&nbsp; read alone</p>
      <p class="solo-text">"I have given fifteen years of my best work to this company — fifteen, and one might fairly count the year I was very nearly seen for the Almeida as a sixteenth — and on every one of those mornings I have come into this building, in good shoes, prepared to do my work, only to be informed that the part I have been given is to be performed under a cook's cap. Now I am the very last man in this canton to make a fuss, as anyone who knows my reputation will tell you, but there is a great deal of difference, sir, between a hat that flatters the actor and a hat that flatters the soup — and I should like to think that, after all this time, I can be relied upon to know which is which. I ought to have gone to Paris when I was a young man, that is the long and the short of it; one mistakes a stepping stone for a destination at one's peril, and I have been paying the bill for that particular mistake on the first of every month for more than thirty years."</p>
    </div>

    <div class="listen">
      <p class="listen-label">What to listen for</p>
      <p>The chin goes up before the sentence begins. The lines stretch — he gives weight to every clause. The comedy is in the <strong>sincerity</strong>: he genuinely believes he is the centre of every room. The wound — <em>"I ought to have gone to Paris when I was a young man"</em> — is real, not a joke. If the auditioner plays it for camp, redirect: "play it as a man telling a truth, in confidence, to a sympathetic stranger."</p>
    </div>
  </section>

  <!-- ============================================================ -->
  <!-- PLAYER 3                                                     -->
  <!-- ============================================================ -->

  <section class="role">
    <div class="role-head">
      <h2>Player 3 — the youngest, and Madame Pace</h2>
      <p class="role-tag">curious, leaning in — and the transformation</p>
    </div>

    <h3>Look as Player 3</h3>
    <p><strong>Early 20s.</strong> The youngest in the company by a decade. Should read as such from the back row. First proper season at the Village Players, after a few small parts last year and a drama school in Geneva she still mentions when she is nervous. Costume: working-rehearsal clothes, but more put-together than the others — she has dressed <em>carefully</em> for her first big season. Body: younger, sharper, listening. The eyes track the senior actors to learn what one does.</p>

    <h3>Behaviour</h3>
    <p><strong>Curious is her dominant register.</strong> Where Player 1 has opinions and Player 2 has shoulders, Player 3 has questions. Leans forward when the Six are speaking. Nods. Catches herself nodding and tries to stop. The other two notice; she colours. She is the first to take the strangers seriously — not because she believes the Father's philosophy, but because she has never seen a rehearsal interrupted in this way and she wants to know what happens. Writes everything down. <strong>Arc:</strong> enthralled in Act One, stops nodding in Act Two when the shop scene plays, and by Act Three she is the audience's mirror at every horror — the only one in the room still asking whether someone should stop it.</p>

    <h3>Tone of speaking</h3>
    <p>A young voice, clear, <strong>slightly uncertain at the end of sentences</strong> — the rising intonation of someone who has not yet decided what she thinks but wants you to consider it. Phrases that land for her: <em>"Perhaps there is a play." "Is anyone else following this?" "Should we — should someone — stop this?"</em></p>

    <h3>Coach against</h3>
    <ul>
      <li><strong>Becoming a generic ingenue.</strong> She is curious, not naive. There is a difference.</li>
      <li><strong>Cuteness.</strong> She is earnest. Earnestness reads as serious when it is not performed.</li>
      <li><strong>Treating the Madame Pace transformation as a costume change only.</strong> The youngest body in the room becomes the most frightening one in it. That is the role's range.</li>
    </ul>

    <div class="solo">
      <p class="solo-label">Three-sentence solo &nbsp;·&nbsp; read alone</p>
      <p class="solo-text">"This is my first proper season — I keep saying that, I know, but it is true, and I keep saying it because I want you to know that whatever I get wrong this morning I will write down, and learn, and not get wrong again next time. I have spent every evening for two weeks reading the Pirandello on the tram on the way home from work, and the strangest thing is that the more I read it the less it stops being strange — there is a family in it that I think I almost know, and a young woman in it who is trying so hard to be heard that I find I am sitting up straighter on the tram every time she speaks. I do not yet know whether I am an actress or a person who is currently acting, but I would very much like, if you will let me, to spend the next six months finding out — and I promise you I will not be the easiest person in the room, but I will be the most awake."</p>
    </div>

    <div class="listen">
      <p class="listen-label">What to listen for</p>
      <p>Young, clear, slightly rising at the end of clauses — the voice of someone who has not decided yet, but wants you to consider it. Resist the urge (theirs or yours) to make her a generic ingenue: she is <strong>curious</strong>, not naive. The audition value is in the last line: can the auditioner <em>promise</em> without becoming cute?</p>
    </div>

    <div class="pace-card">
      <p class="pace-label">Optional &nbsp;·&nbsp; Madame Pace transformation test</p>
      <p>Run this only if the auditioner is in contention for the role. Ask them to read the following lines aloud — <strong>twice</strong>: first in the half-Italian, half-French broken speech of a foreigner running a shop in Lausanne (a foreigner who has lived here too long to speak the language properly, and not long enough to forget her first); then a second time, in the same voice, but <strong>calmly, smiling, as if reading a column of figures in a ledger.</strong></p>
      <div class="solo" style="margin-top:3mm;">
        <p class="solo-text">"Cara — you come back to me. I knew you come back. The young ones, they always come back to Madame Pace, sooner or later, one way or another way. He clean. He polite. He pay cash. The book, you understand, it must balance. Francs do not lie. People — people lie all day long."</p>
      </div>
      <p style="margin-top:3mm; font-size: 10.5pt;"><strong>What to listen for:</strong> the accent is the gateway, not the role. The first reading tests whether they can carry the dialect without flinching. The second reading tests whether they can be <em>cold</em> inside the comedy — the bookkeeping smile that makes the audience regret having laughed at her first line. If the second reading frightens you a little, you have your Madame Pace.</p>
    </div>
  </section>

  <footer class="foot">
    <p><strong>Village Players · Lausanne</strong> &nbsp;·&nbsp; Director: Kiarash Jamshidi</p>
    <p>Companion to the Audition Pack, the Audition Two-Hander Pack, and the Audition Checklist. The character readings follow the Director's Copy.</p>
  </footer>

</main>

</body></html>
"""

HTML_PATH = OUT_DIR / "audition_briefing.html"
HTML_PATH.write_text(HTML)

OUT = OUT_DIR / "audition_briefing.pdf"
with sync_playwright() as p:
    launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
    browser = p.chromium.launch(**launch_kwargs)
    page = browser.new_page()
    page.goto(f"file://{HTML_PATH.resolve()}", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(600)
    page.pdf(path=str(OUT), format="A4",
             margin={"top": "20mm", "right": "22mm", "bottom": "20mm", "left": "22mm"},
             print_background=True, prefer_css_page_size=True)
    browser.close()

try:
    from pypdf import PdfReader
    r = PdfReader(str(OUT))
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes) · {len(r.pages)} pages")
except BaseException:
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes)")
