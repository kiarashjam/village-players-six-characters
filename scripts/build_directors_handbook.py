#!/usr/bin/env python3
"""Build the Director's Handbook PDF.

A comprehensive field manual for the director: directing technique,
Pirandello in particular, the production's specific demands, working
with actors, working with the company, and the production's compass.

Structured in seven parts, multiple sections per part, with subsections
and sub-sub-sections where the material asks for them.
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
<title>Director's Handbook — Six Characters in Search of an Author</title>
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

  /* Part headings (h1 below masthead) */
  h1.part { font-family:'Cormorant Garamond',serif; font-weight: 500;
            font-size: 20pt; line-height: 1.15;
            text-align: center; margin: 14mm 0 4mm 0;
            padding-bottom: 3mm; border-bottom: 1px solid var(--rule);
            color: var(--accent); }
  .part-eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600;
                  font-size: 9pt; letter-spacing: 0.28em;
                  text-transform: uppercase; color: var(--ink-soft);
                  text-align: center; margin: 0 0 2mm 0; }

  /* Section headers */
  h2 { font-family:'Cormorant Unicase',serif; font-weight: 600;
       font-size: 11pt; letter-spacing: 0.22em;
       text-transform: uppercase; color: var(--accent);
       margin: 9mm 0 3mm 0; }
  h3 { font-family:'Cormorant Garamond',serif; font-weight: 600;
       font-size: 13pt; color: var(--ink);
       margin: 6mm 0 2mm 0; }
  h4 { font-family:'EB Garamond',serif; font-weight: 600;
       font-style: italic; font-size: 11.5pt; color: var(--ink);
       margin: 4mm 0 1mm 0; }

  p { margin: 0 0 3mm 0; }
  ul, ol { margin: 0 0 4mm 0; padding-left: 6mm; }
  li { margin-bottom: 2.5mm; line-height: 1.6; }
  strong { color: var(--ink); }
  em { color: var(--ink); }

  /* Callout */
  .callout { border-left: 3px solid var(--accent);
             padding: 3mm 5mm; margin: 4mm 0 5mm 0;
             background: rgba(255,255,255,0.25); }
  .callout p:last-child { margin-bottom: 0; }

  /* Pull-quote */
  .pull-quote { font-family:'Cormorant Garamond',serif; font-style: italic;
                font-size: 12.5pt; line-height: 1.5;
                padding: 4mm 8mm; margin: 5mm 0 5mm 0;
                color: var(--ink); text-align: center;
                border-top: 1px solid var(--rule);
                border-bottom: 1px solid var(--rule); }

  /* Definition box */
  .def-box { border: 1px solid var(--rule);
             padding: 4mm 6mm; margin: 3mm 0 5mm 0;
             background: rgba(255,255,255,0.25); }
  .def-box .term { font-family:'Cormorant Unicase',serif; font-weight: 600;
                   font-size: 10pt; letter-spacing: 0.16em;
                   text-transform: uppercase; color: var(--accent);
                   margin: 0 0 2mm 0; }
  .def-box .def { font-size: 10.5pt; line-height: 1.6; margin: 0; }

  /* Table of contents */
  nav.toc { margin: 8mm 0 12mm; padding: 5mm 6mm;
            border: 1px solid var(--rule);
            background: rgba(255,255,255,0.25); }
  nav.toc h2 { margin: 0 0 4mm 0; text-align: center; }
  nav.toc ol { margin: 0; padding-left: 5mm; font-size: 10pt; }
  nav.toc ol ol { margin: 1mm 0 2mm 0; padding-left: 5mm; color: var(--ink-soft); }
  nav.toc li { margin-bottom: 1.5mm; }

  /* Page break helpers */
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
    <p class="eyebrow">Director's Handbook</p>
    <h1>Six Characters<br>in Search of an Author</h1>
    <p class="play">Sei personaggi in cerca d'autore &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
    <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne &nbsp;·&nbsp; late autumn 2026</p>
    <p class="credit" style="margin-top:6px;">Director: <strong>Kiarash Jamshidi</strong></p>
  </div>

  <section>
    <h2>What this handbook is</h2>
    <p>This is a personal field manual for the director of this production. It does not replace the Director's Copy, which is the production's authoritative text and scoring. The handbook is its complement: a working reference on directing technique, on Pirandello in particular, and on the specific demands this play makes of the room.</p>
    <p>It is written to be read alone — over a coffee, on the train, the night before a difficult rehearsal — and then put away. It is not handed out. It is the director's notebook, made shareable so that the thinking behind every decision in the Director's Copy can be traced when needed, and so that the techniques the director will be reaching for are gathered in one place rather than scattered across twenty books.</p>
    <p>Seven parts. The first three are about the play and the work the director must do on the play; the next three are about working with the company and with the room; the seventh is what to hold across the production when everything else is moving. Read straight through once; then return to whichever part the next rehearsal needs.</p>
  </section>

  <nav class="toc">
    <h2>Contents</h2>
    <ol>
      <li><strong>Part I — The Play and Its Demands</strong>
        <ol>
          <li>Reading Pirandello — what kind of play this is</li>
          <li>The Storer translation and its limits</li>
          <li>The four Characters and the Six (a director's reading)</li>
          <li>The three-act architecture</li>
        </ol>
      </li>
      <li><strong>Part II — Directing Technique</strong>
        <ol start="5">
          <li>The director's job, defined</li>
          <li>The reading rehearsal — the table-work phase</li>
          <li>The staging rehearsal — table to floor</li>
          <li>Working with the actor</li>
          <li>Coaching the Characters of this play</li>
        </ol>
      </li>
      <li><strong>Part III — Staging Technique for This Production</strong>
        <ol start="10">
          <li>The stage objects (chair-and-coat, bundle)</li>
          <li>The projections</li>
          <li>Light as direction</li>
          <li>Sound as direction</li>
        </ol>
      </li>
      <li><strong>Part IV — Working with the Company</strong>
        <ol start="14">
          <li>The Village Players context</li>
          <li>Casting principles</li>
          <li>Building the company</li>
          <li>The audition room</li>
        </ol>
      </li>
      <li><strong>Part V — Pirandello in Particular</strong>
        <ol start="18">
          <li>The historical context</li>
          <li>The metaphysics</li>
          <li>The metatheatricality</li>
          <li>Notable productions and what they teach</li>
        </ol>
      </li>
      <li><strong>Part VI — Practical Director's Work</strong>
        <ol start="22">
          <li>Time management across the rehearsal block</li>
          <li>Notes — the director's most public document</li>
          <li>The performance run</li>
        </ol>
      </li>
      <li><strong>Part VII — What Kiarash Must Hold</strong>
        <ol start="25">
          <li>The director's compass for this production</li>
          <li>What the production cannot do</li>
          <li>Final principles</li>
        </ol>
      </li>
    </ol>
  </nav>

  <!-- ============================================================ -->
  <!-- PART I                                                       -->
  <!-- ============================================================ -->

  <h1 class="part page-break">Part I &middot; The Play and Its Demands</h1>
  <p class="part-eyebrow">What kind of play this is, and what it asks of the director</p>

  <section>
    <h2>1. Reading Pirandello — what kind of play this is</h2>

    <h3>1.1 The metatheatrical frame</h3>
    <p><em>Six Characters in Search of an Author</em> opens on a working theatre company rehearsing a play they do not like. Onto that stage walk six figures who insist they were once written, then abandoned by their author, and who now demand to be staged. The play that follows is not the inner family drama — it is the friction between the working company and the unfinished characters who have come to disrupt them.</p>
    <p>This is a play <em>about</em> theatre, written in 1921 by a man who already understood that the form was running out of nineteenth-century furniture. The "fourth wall" naturalism Pirandello was watching collapse around him needed something new on the other side of it. He did not write theatre about heroes any more; he wrote theatre about the act of writing theatre about heroes — and what survives when the writing fails.</p>
    <p>For the director, this means the play has two simultaneous registers: the everyday register of working actors at a morning rehearsal, and the eternal register of figures who exist only as themselves and cannot stop being so. Holding both registers in the same room is the production's central technical demand.</p>

    <h3>1.2 What the Six characters represent</h3>
    <p>Pirandello's Six are not metaphors. They are creatures of a particular ontological category — characters who exist <em>as characters</em>, which is to say: fixed, eternal, identical to themselves in every moment. A character cannot become something else; an actor can. That is the gap the play is built on.</p>
    <h4>1.2.1 The eternal vs. the contingent</h4>
    <p>The Father makes this argument explicitly in Act Three: a character is fixed forever in the worst hour of his life. An actor leaves the theatre and goes home; a character has nowhere to leave. This is the play's metaphysical claim. Treat it as a claim the play believes, not as a literary device.</p>
    <h4>1.2.2 What the Six are not</h4>
    <p>They are not ghosts. They are not allegories. They are not the actors' imaginations. They are — in the play's logic — a separate category of being. The production must let them be that. The danger is staging them as <em>spooky</em> (a cheap version of mystery) or as <em>thematic</em> (a cheap version of profundity).</p>

    <h3>1.3 The hierarchy of realities</h3>
    <p>The play stages at least four nested realities. The director must know which one each beat is in.</p>
    <ol>
      <li><strong>The audience watching the production.</strong></li>
      <li><strong>The working company rehearsing a Pirandello play.</strong> This is the level the Manager and the Players occupy at the start of Act One.</li>
      <li><strong>The unfinished play the Six bring with them.</strong> The family drama they keep insisting they are inside.</li>
      <li><strong>The "real" events that play once represented before the author abandoned it.</strong> The Step-Daughter's events. The hundred francs. The shop. The fountain.</li>
    </ol>
    <p>Every line in the play sits inside one of these four. The Father's philosophical speeches frequently jump between them mid-sentence. The director's job is to know which level a line is operating from, and to make sure the actor knows too.</p>

    <h3>1.4 Why the play resists closure</h3>
    <p>The Manager closes the play with <em>I've lost a whole day over these people. A whole day.</em> That is not catharsis. The Boy is dead, or is he. The Step-Daughter has run off, or has she. The Father is still arguing. The Mother is still grieving. The audience leaves without resolution because the play's logic does not allow resolution: a fixed character cannot resolve itself.</p>
    <p>The director's temptation is to provide what the play withholds — a clear sense of what happened, a sense of moral landing. <em>Resist this</em>. The discomfort the audience walks out with is the play. If they walk out comforted, the production has failed.</p>
  </section>

  <section>
    <h2>2. The Storer translation and its limits</h2>

    <h3>2.1 What Storer gives us</h3>
    <p>Edward Storer's 1922 translation is the standard public-domain English. It has carried Pirandello into the English-speaking theatre for a century. Its merits are real: it preserves the play's syntactic peculiarity, the Father's circling philosophical sentences, the Step-Daughter's interruptions, the Manager's pragmatism. It is the version most English-speaking audiences will have read or seen.</p>

    <h3>2.2 What Storer loses</h3>
    <p>Three losses, all worth knowing.</p>
    <h4>2.2.1 The dialect</h4>
    <p>Madame Pace speaks in Pirandello's original a Italo-Spanish mongrel meant to mark her as a foreigner doing business in Italy. Storer flattens this to a stilted broken English. The production restores the foreignness by making her speak French-tinted English — she is in Lausanne, after all — and giving her the production's most distinct vocal signature.</p>
    <h4>2.2.2 The Italian rhythms</h4>
    <p>Italian sentences pulse where English sentences plod. The Storer translation has a tendency to over-formal English ("I should much like to know") where the original is conversational and broken. The director may modernise small phrases as long as the meaning is preserved — but should leave the longer speeches alone.</p>
    <h4>2.2.3 The 1922 vocabulary</h4>
    <p>"Capital!" "By Jove!" — these are real bits of 1922 English that the production cannot keep without comedy. The director's edition has already trimmed the worst; a few remain. Trim them as you find them.</p>

    <h3>2.3 Where the director must repair the prose</h3>
    <p>The four places to watch:</p>
    <ul>
      <li>The Manager's exposition speeches in Act One — Storer is wordy where Pirandello is staccato. Trim.</li>
      <li>The Father's philosophical paragraphs in Act Three — Storer is faithful but heavy. Pause more than you cut; let the breath do the work.</li>
      <li>Madame Pace's broken English — the production has given her a more performable register.</li>
      <li>The closing dialogue — keep it brutal. Do not soften the Manager's last line.</li>
    </ul>

    <h3>2.4 The Italian rhythms underneath</h3>
    <p>If you read the play aloud, you will hear three rhythms Pirandello relies on: the long argumentative paragraph (the Father), the interrupting fragment (the Step-Daughter), and the working-room pragmatic prose (the Manager). Direct each rhythm to play <em>against</em> the others. The play's friction is partly metrical.</p>
  </section>

  <section>
    <h2>3. The four Characters and the Six (a director's reading)</h2>
    <p>Each of the Six lives at the eternal level. Each of the working company lives at the contingent level. Cast and direct accordingly.</p>

    <h3>3.1 The Father — autobiographical metaphysics</h3>
    <p>The Father's long speeches are philosophy that is also confession. He talks about <em>reality</em> and <em>conscience</em> because the only alternative is to say plainly what he did at the shop. Every metaphysical statement is a refusal to be specific. The director's job is to make sure the actor knows this — that the speech is escape, not lecture.</p>
    <h4>3.1.1 The four-stage arc</h4>
    <p>Across Act Three Part I: <em>control → injury → attack → horror</em>. He starts mellifluous, capable. The Step-Daughter cuts him; he loses ground; he attacks; the attack lands and he sees what he has become. This is not interpretation. It is what the scene needs to be staged as if it is to land.</p>
    <h4>3.1.2 The body of shame</h4>
    <p>The Father sweats. Not as a prop — physiologically. The actor must arrive at a place where the body confesses what the speech refuses to. Direct rehearsals toward this: heat at the brow, breath shortening, small adjustments of a man who would prefer to be elsewhere.</p>

    <h3>3.2 The Mother — grief as architecture</h3>
    <p>The Mother is the play's only character who does not argue for herself. She wears a heavy widow's veil — half her costume. She covers her face with her hands at the first chance. She has three silences across the play that the production scores specifically (see Director's Copy).</p>
    <h4>3.2.1 The three silences</h4>
    <p>One in Act One (when the Father lifts the veil), one in Act Two (when she is forced to watch the shop scene), one in Act Three (the gap before the fountain). Each silence is a different shape. Each must be rehearsed individually.</p>
    <h4>3.2.2 The body that grieves</h4>
    <p>The Mother's body is not symbolic. It is specific. The actor decides exactly what the hands are doing in every moment — folding, clenching, releasing the veil, pressed to the bundle. Generalised "grieving" is not the role.</p>

    <h3>3.3 The Step-Daughter — moral indictment</h3>
    <p>The play's emotional and moral centre. Not a coquette; not a victim performing victimhood. A young woman holding the room accountable for what was done to her. The director must protect this reading from every direction the actor or the room might drift in.</p>
    <h4>3.3.1 The three cuts</h4>
    <p>Across Act Three Part I, she cuts her stepfather three times — each cut is a different intervention, escalating. <em>His reality. He always knew exactly where to find me.</em> The production scores all three (see Director's Copy).</p>
    <h4>3.3.2 The room she will not let be made beautiful</h4>
    <p>The Step-Daughter refuses every staging that would soften her case. She refuses to be cried for. She refuses the play's instinct to round her into pity. The director's job is to support that refusal in the staging itself: cold blocking, no soft light on her face, the audience held at arm's length.</p>

    <h3>3.4 The Son — refusal as form</h3>
    <p>The Son's role is to refuse. Refuse to participate. Refuse to acknowledge the Mother. Refuse to play his own scene. The play tries multiple times to bring him in, and he holds back each time. By the end of Act Three Part II he has refused himself entirely out of the story he was supposed to be in.</p>
    <h4>3.4.1 The discipline of withholding</h4>
    <p>The actor's instinct will be to give. Direct against this. The Son's stillness must read as <em>chosen</em>, not as passive. He has decided not to act, and he is acting that decision every second he is on stage.</p>

    <h3>3.5 The Boy and the Child — figures, not actors</h3>
    <p>In this production they are objects: the Boy is a chair with a coat folded over its back; the Child is a wrapped bundle of white cloth. They are not played by performers. The Step-Daughter and the Mother handle them as if they were children. The directorial discipline here is to make the objects read as children without ever apologising for the convention.</p>

    <h3>3.6 The Manager and the Players — the company under siege</h3>
    <p>The Manager is the production's most metatheatrically interesting role. He represents the audience's body on stage — the figure who is also trying to make sense of these strangers. His arc is his own production: he comes in skeptical, becomes fascinated, becomes appalled, ends up exhausted. The Players are working actors with a comic register that lasts the first half hour and then has nothing to do but watch.</p>
  </section>

  <section>
    <h2>4. The three-act architecture</h2>

    <h3>4.1 Act One — comedy → exposure → bargain</h3>
    <p>Three parts.</p>
    <h4>4.1.1 Part I (The Rehearsal)</h4>
    <p>White working lights. A scratchy French chanson in the wings. The Players are rehearsing a play they do not like; the Manager is half present. The audience laughs in the first ten minutes. This is committed comedy. Do not undercut it.</p>
    <h4>4.1.2 Part II (The Family Arrives)</h4>
    <p>Projection 1 plays — the Six arrive silently on video. The white lights soften to amber. The chanson cuts off mid-bar. The play's tonal hinge is here, in the second part of the first act.</p>
    <h4>4.1.3 Part III (The Bargain)</h4>
    <p>Amber drifts slowly to deep red across the part. The Step-Daughter speaks the words <em>hundred francs</em>; the Father starts to sweat. The act ends in a low blood-coloured wash. No music. The silence is the texture; the next act is the cue.</p>

    <h3>4.2 Act Two — staging the unstageable</h3>
    <p>The longest act. Three parts, each anchored by a single visual device: the projection, the shower, the doubled scene.</p>
    <h4>4.2.1 Part I (Under the Projection)</h4>
    <p>The Step-Daughter's recorded voice plays from the projection while her live body stands silent below the screen. Satie's <em>Gymnopédie No. 1</em> on the pianist's piano. The shower light falls on the live Step-Daughter only.</p>
    <h4>4.2.2 Part II (Madame Pace's Aria)</h4>
    <p>The piano shifts to a Weimar-shop vamp; Madame Pace steps into the shower. The aria is the production's hardest single beat: comic on arrival, chilling on exit. The piano dies on the Mother's line — <em>You old devil. You murderess.</em></p>
    <h4>4.2.3 Part III (The Doubled Scene and the Mother's Cry)</h4>
    <p>Leading Lady and Leading Man take the platform to play the shop scene as theatre. The Mother is forced to watch. The shower falls on her on her keystone line — <em>It's taking place now. It happens all the time.</em> The piano cuts on her cry. Accidental curtain.</p>

    <h3>4.3 Act Three — argument → refusal → fountain</h3>
    <p>The shortest act. The darkest. Three parts; the last is the play's true ending.</p>
    <h4>4.3.1 Part I (The Argument over Reality)</h4>
    <p>The cello drone, low. The Father's four-stage arc on its feet. The Step-Daughter's three cuts. He ends without having won the philosophy.</p>
    <h4>4.3.2 Part II (The Refusal)</h4>
    <p>Silence. The Son refuses to play. The Father grabs his arm; a single piano note from offstage like a slap. Silence resumes.</p>
    <h4>4.3.3 Part III (The Fountain)</h4>
    <p>The basin lit pale-blue from inside. The Step-Daughter bends over the bundle in the basin. A gunshot in real silence. The Manager's last line. Arvo Pärt for ten seconds. Lights go.</p>
  </section>

  <!-- ============================================================ -->
  <!-- PART II                                                      -->
  <!-- ============================================================ -->

  <h1 class="part page-break">Part II &middot; Directing Technique</h1>
  <p class="part-eyebrow">What you need in the room — Stanislavski, the table, the floor, the actor</p>

  <section>
    <h2>5. The director's job, defined</h2>

    <h3>5.1 What a director does</h3>
    <p>A director does five things, all of them in sequence and all of them iteratively:</p>
    <ol>
      <li><strong>Reads the play</strong> — until they know what it is for, what it cannot survive without, and what it can afford to lose.</li>
      <li><strong>Casts the play</strong> — chooses the bodies and voices that will carry the production.</li>
      <li><strong>Stages the play</strong> — decides what happens where, when, and at what tempo.</li>
      <li><strong>Coaches the actors</strong> — works with each performer on their specific demand.</li>
      <li><strong>Watches the play</strong> — sees what is happening on stage as if for the first time, and adjusts.</li>
    </ol>
    <p>Everything else — including this handbook — is in service of those five.</p>

    <h3>5.2 What a director does not do</h3>
    <ul>
      <li>Act the play themselves. The director does not demonstrate; the director invites.</li>
      <li>Substitute their taste for the play's intent. The play comes first.</li>
      <li>Try to be liked by the cast. Likability is irrelevant; trust is required.</li>
      <li>Direct over the Stage Manager or the Assistant Director's work. Each role is bounded.</li>
      <li>Solve every problem in front of the company. Some problems are diagnosed in front of the company; most are solved between sessions, alone, with the script open.</li>
    </ul>

    <h3>5.3 The director as first audience</h3>
    <p>Every rehearsal, the director is sitting in the seat the audience will sit in seven months from now. Watch the play as that audience would. Not as the writer who has studied it. Not as the producer who has paid for it. As a person who has come in from the cold to find out what happens next. If you stop being able to do this, you are no longer directing — you are managing.</p>

    <h3>5.4 The director as the production's moral compass</h3>
    <p>You decide what the production says by what you let it do. Every choice — what to keep, what to cut, what to score, what to leave bare — is an ethical choice. The Step-Daughter's three cuts. The Madame Pace bookkeeping aria. The age in the room. None of these is just a staging decision. The director's compass is the production's compass.</p>
  </section>

  <section>
    <h2>6. The reading rehearsal — the table-work phase</h2>

    <h3>6.1 The first read-through</h3>
    <p>The full company gathered around a table, reading the play aloud in order. Once. No staging, no interruptions, no notes from the director during the read. Listen for:</p>
    <ul>
      <li>Where the play landed and where it stalled — same as a film at a test screening.</li>
      <li>Which actor is over-prepared, which actor is under-prepared.</li>
      <li>Which actor is reading <em>at</em> the others vs. reading <em>with</em> them.</li>
      <li>Which scenes scared the room and which scenes the room glossed over.</li>
      <li>The play's true running length, read at the pace of a worried first-time read.</li>
    </ul>
    <p>Take notes for yourself, not the cast. The cast does not need notes on the first read; they need the experience of the play. Notes come at the second session.</p>

    <h3>6.2 Around-the-table discussion</h3>
    <p>From the second session forward, table work is discussion. The director's job at the table is to:</p>
    <ol>
      <li>Ask questions, not answer them. <em>Why is your character in this room? What does your character want? What stops them?</em></li>
      <li>Refuse to interpret the play <em>at</em> the actors. The play means what it does when staged. Discussion sharpens the question; the staging answers it.</li>
      <li>Keep the room productive — when discussion drifts to abstraction, return to a specific line.</li>
      <li>Build the company's shared vocabulary. By the end of table work, everyone knows what is meant by <em>shower</em>, <em>bundle</em>, <em>the four-stage arc</em>, <em>the three cuts</em>.</li>
    </ol>

    <h3>6.3 Action analysis — Stanislavski's method, briefly</h3>
    <p>Stanislavski's system is the bedrock of modern Western acting and directing. The director does not need to teach it; the director needs to use it.</p>
    <h4>6.3.1 The super-objective</h4>
    <div class="def-box">
      <p class="term">Super-objective</p>
      <p class="def">The single, ruling want that drives a character across the entire play. Not the moment-to-moment want — the lifelong one. <em>To be heard. To be forgiven. To be left alone. To make the room understand what happened.</em> Each character has one. The director helps the actor find it.</p>
    </div>
    <p>For this play:</p>
    <ul>
      <li><strong>Father:</strong> to be allowed to exist as more than the worst hour of his life.</li>
      <li><strong>Mother:</strong> to be relieved of the obligation to remember.</li>
      <li><strong>Step-Daughter:</strong> to make the room see what was done, exactly.</li>
      <li><strong>Son:</strong> to remain outside the play he was put into.</li>
      <li><strong>Manager:</strong> to finish the day's rehearsal and go home.</li>
      <li><strong>Madame Pace:</strong> to settle the account and move to the next customer.</li>
    </ul>
    <h4>6.3.2 Objectives and obstacles by unit</h4>
    <p>Beneath the super-objective, every unit (or beat) has a smaller objective. <em>What do I want from this person in this moment?</em> An obstacle is what stops you getting it. Action is what you do to get past the obstacle. Objective + obstacle + action = the unit.</p>
    <h4>6.3.3 Action verbs — not adjectives</h4>
    <p>An actor playing "angry" is performing an adjective. An actor <em>accusing</em>, <em>shaming</em>, <em>cornering</em>, <em>provoking</em> is playing a verb. Verbs are direct-able; adjectives are not. The director's vocabulary in the room should be 90% verbs.</p>

    <h3>6.4 Given circumstances — Pirandello's particular case</h3>
    <p>Given circumstances are everything the play tells us about who, where, when, and why. For most plays this is straightforward: the where and when are clear. For <em>Six Characters</em> the given circumstances are layered (see Section 1.3 — Hierarchy of Realities). Every scene's circumstances must be specified at the right level.</p>
    <p>Example: when the Step-Daughter says <em>hundred francs</em>, she is on level 4 (the original events). When she says <em>You know how you taught me</em> in the same scene, she is on level 3 (the family drama being staged). When she breaks the fourth wall, she is on level 2 (the rehearsal). The actor must know which level the line is coming from.</p>

    <h3>6.5 The beat — what a beat is, how to find one</h3>
    <div class="def-box">
      <p class="term">Beat</p>
      <p class="def">A unit of action between one objective shift and the next. When a character changes what they are trying to get, or who they are trying to get it from, a new beat begins. Plays are made of beats stacked into scenes stacked into acts.</p>
    </div>
    <p>To find a beat, ask: <em>what is the character doing right now, and when does that change?</em> The change is the beat boundary. Mark them in the script in pencil. Re-mark them when the staging shifts what you thought.</p>
  </section>

  <section>
    <h2>7. The staging rehearsal — table to floor</h2>

    <h3>7.1 First blocking</h3>
    <p>When you move from table to floor, do not over-block on day one. First blocking should be wide — broad geographic decisions: who is upstage, who is downstage, who sits, who stands, who enters from where. Specifics come on the second pass. The first pass is to confirm the room can hold the scene at all.</p>

    <h3>7.2 The principles of blocking</h3>

    <h4>7.2.1 Stage geography</h4>
    <p>Stand on the stage. Look at the audience. <em>Upstage</em> is away from them; <em>downstage</em> is toward them. <em>Stage right</em> is the actor's right; <em>stage left</em> is the actor's left. Use these terms with the actors and the operators consistently — there is no greater waste of rehearsal time than confusion about left and right.</p>

    <h4>7.2.2 Sight lines</h4>
    <p>Every position must be visible from every seat in the house. Sit in each section of the house at some point during tech and check. The sight lines from the cheap seats in any Lausanne theatre are the ones that betray you.</p>

    <h4>7.2.3 Composition</h4>
    <p>What does the audience's eye go to first? Pay attention to:</p>
    <ul>
      <li><strong>Focus</strong> — light, movement, position upstage of the line of vision, isolated figures.</li>
      <li><strong>Balance</strong> — too many bodies to one side feels heavy; the eye drifts.</li>
      <li><strong>Framing</strong> — what the body in the column of light reads against. The Mother standing alone reads differently from the Mother standing among Players.</li>
    </ul>

    <h4>7.2.4 Levels</h4>
    <p>This production uses a two-level set in Act Two: the upper platform (the rehearsal stage) and the lower floor (the watching company). Levels create hierarchy automatically. Use this. The Players watching the shop scene from below are positioned as the audience's stand-in.</p>

    <h4>7.2.5 Cross and counter-cross</h4>
    <p>When one actor crosses the stage, the actors around them rebalance. A cross without a counter-cross leaves the stage feeling lopsided; a counter-cross is what tells the audience the cross meant something. The Step-Daughter's three cuts in Act Three are crosses; the Father's small adjustments are the counter-crosses.</p>

    <h3>7.3 Status work</h3>
    <p>Status — Keith Johnstone's most useful contribution — is who is up and who is down in any given exchange. The room knows. The audience reads it instantly. Direct every two-hander as a status negotiation:</p>
    <ul>
      <li><em>Who has the higher status at the start of the scene?</em></li>
      <li><em>Where does it shift?</em></li>
      <li><em>Who has the higher status at the end?</em></li>
    </ul>
    <p>For this play: the Father starts Act Three Part I with the higher status (mellifluous, in control). By the end, the Step-Daughter has every inch of it. The shift happens across three named cuts.</p>

    <h3>7.4 Tempo and rhythm</h3>
    <p>Tempo is the speed of a scene; rhythm is the pattern of its speeds. A scene at a single tempo is a scene asleep. Direct against monotony: a fast beat next to a held beat next to a fast beat. The Father's long speeches are slow; the Step-Daughter's interruptions are fast. The friction is the rhythm.</p>

    <h3>7.5 Silence — the director's most underused tool</h3>
    <p>Three silences score this production. The Mother's three (see 3.2.1). The silence between the Step-Daughter's <em>hundred francs</em> and the Father's first attempted response. The silence of Act Three Part II. Rehearse silences as carefully as you rehearse lines. A silence is a beat; it has a length; it has an action under it.</p>
    <div class="callout">
      <p>Most amateur productions are afraid of silence. Audiences are not. Trust the silence.</p>
    </div>
  </section>

  <section>
    <h2>8. Working with the actor</h2>

    <h3>8.1 The actor's process — what to respect</h3>
    <p>Every actor works differently. Some come in with the lines learned; some come in cold. Some are physical first; some are vocal first. Some need to talk through every choice; some need to be left alone to find it. <em>You are not directing acting style</em>. You are directing what the play needs and what their body and voice can do.</p>
    <p>Respect the actor's process unless it is breaking the play. The actor who needs to talk through the scene for ten minutes is not a problem — until the company is waiting on them. The actor who shows up with everything decided is not a problem — until they refuse to adjust. Use your judgment.</p>

    <h3>8.2 Notes — how to give them</h3>
    <p>Notes are how the director communicates with the actor outside the moment. The rules:</p>
    <ol>
      <li><strong>Specific.</strong> Not "more energy" — "speed up the line <em>So you don't believe me?</em> by half".</li>
      <li><strong>Actionable.</strong> Not "your character is sadder than you're playing" — "let the breath catch on the word <em>child</em>".</li>
      <li><strong>One at a time.</strong> An actor can hold three notes at once, maybe four. Beyond that you are just talking to yourself.</li>
      <li><strong>Given between rehearsals, not during.</strong> Stopping a scene mid-flow to give notes is sometimes necessary; usually it is not. Take the note in your book; give it after.</li>
      <li><strong>Praise the specific.</strong> "That landed" is a useful note. "That was great" is not.</li>
    </ol>

    <h3>8.3 The actor who is stuck</h3>
    <p>Diagnostic questions, in this order:</p>
    <ol>
      <li>Does the actor know what their character wants in this scene? (If no, return to objective.)</li>
      <li>Does the actor know what is stopping them? (If no, return to obstacle.)</li>
      <li>Does the actor know who they are talking to? (If no, work the partner.)</li>
      <li>Is the actor playing an adjective? (If yes, give them a verb.)</li>
      <li>Is the actor playing a result? (If yes, return to the moment before.)</li>
    </ol>

    <h3>8.4 The actor who is too big</h3>
    <p>Direct them smaller. Specific techniques: ask them to play the scene at half-volume. Ask them to play it sitting down. Ask them to remove every gesture they have planned. <em>Trust the audience</em>. If they will not get smaller, cast the role again — but only after every adjustment has been tried.</p>

    <h3>8.5 The actor who is too small</h3>
    <p>The opposite problem, less common, more frustrating. Specific techniques: ask them to play the scene at double-volume. Ask them to take more space. Ask them what they are afraid of (sometimes the answer is "looking stupid" — fix this by promising it is not happening). Make sure they have eaten.</p>

    <h3>8.6 The actor who has decided everything already</h3>
    <p>Common in actors who have done the play before. They arrive with the role already cast inside their head. Two approaches:</p>
    <ul>
      <li><strong>Ask them to do it.</strong> See if their already-decided version is good. Sometimes it is.</li>
      <li><strong>Ask them to do something different.</strong> Not to prove they are wrong — to see what else is possible. Surprise can dislodge.</li>
    </ul>

    <h3>8.7 The amateur actor — particular considerations</h3>
    <p>The Village Players are an amateur company. Amateur does not mean unserious — it means people who have day jobs and rehearse at SSA Lausanne on Thursdays from 18:00 to 21:00. This shapes everything.</p>
    <ul>
      <li><strong>Time is the scarce resource.</strong> Use rehearsal time for what only rehearsal can do (work the room together). Use sub-rehearsals for what an actor can do alone or in a pair.</li>
      <li><strong>Energy is the second scarce resource.</strong> An amateur cast arriving at 18:00 after a workday is not at the energy level of a professional cast at 10:00. Plan accordingly.</li>
      <li><strong>Confidence varies more widely than in professional rooms.</strong> Some of your cast are deeply experienced; some are not. Adjust your vocabulary per actor.</li>
      <li><strong>The play is the point, not the careers.</strong> Nobody is auditioning for the West End next week. Direct for the play.</li>
    </ul>
  </section>

  <section>
    <h2>9. Coaching the Characters of this play</h2>

    <h3>9.1 The Father — the long speech as battle</h3>
    <p>The Father's philosophical speeches are not lectures. They are fights for his existence. Coach the actor to find <em>what is being attacked</em> in every line. When he says <em>reality</em>, what specifically is he trying to hold off? (Answer: the moment he watched her at the school gate, the moment he sat in Madame Pace's shop.) Direct the speech as a man arguing for his life against a room that already knows what he did.</p>

    <h3>9.2 The Mother — silence and the body</h3>
    <p>Coach for stillness that reads as presence, not absence. The body must be doing something every second. Specific physical scoring: the right hand at the veil's hem; the left hand pressed flat to the bundle; the breath that stops on each of the three silences. The actor must have decided what is happening internally, and the audience must read it without being told.</p>

    <h3>9.3 The Step-Daughter — moral centre</h3>
    <p>Coach against every drift toward coquettishness, victimhood, or sentimentality. She is the play's most articulate witness. She is not flirting; she is indicting. She is not crying; she is reporting. The three cuts in Act Three Part I are surgical — coach them as such. The body's age must read; the body's posture must hold her presence. She enters a room and the room knows she is there.</p>

    <h3>9.4 The Son — the work of withholding</h3>
    <p>Coach the actor to play <em>refusal</em> as an active verb. The Son is not absent; he is refusing presence. Every second on stage he is making a choice not to engage. The mirror speech in Act Three Part II is the role's only extended expression — coach it as a man who has chosen, finally, to say one true thing and then to leave the stage forever.</p>

    <h3>9.5 The Players — comedy that gives way</h3>
    <p>Coach the three Players first as a working company at a morning rehearsal — Lausanne register, local, modern, slightly bored. The comedy in Act One is theirs. By Act Two, the comedy is gone; coach them to hold the room as witnesses. By Act Three, they are watching with the audience.</p>

    <h3>9.6 Madame Pace — comic on arrival, chilling on exit</h3>
    <p>The hardest single coaching job in the production. Player 3 transforms. The arrival is funny — the broken French, the bleached wig, the silver chain. The bookkeeping aria is not funny. The exit is somewhere between threat and confession.</p>
    <p>Specific coaching beats: practice the entry until it is comically physical without being clownish. Practice the aria until the rhythm is bookkeeping (in/out, in/out) rather than seduction. Practice the exit at half-volume — the threat is in the precision, not the menace.</p>
  </section>

  <!-- ============================================================ -->
  <!-- PART III                                                     -->
  <!-- ============================================================ -->

  <h1 class="part page-break">Part III &middot; Staging Technique for This Production</h1>
  <p class="part-eyebrow">The chair-and-coat, the bundle, the projections, the shower, the fountain</p>

  <section>
    <h2>10. The stage objects</h2>

    <h3>10.1 How to direct an object as a character</h3>
    <p>The chair-and-coat is the Boy. The bundle is the Child. They are not pretending to be children — in the production's logic they <em>are</em> the children. The performers handle them with the same specificity they would handle a child. Coach the Step-Daughter and the Mother to:</p>
    <ul>
      <li>Track the object across the stage with their eyes when it is not in their hands.</li>
      <li>Pick it up the way one picks up a child — under the arms, against the shoulder, the back of the head supported.</li>
      <li>Set it down the way one sets a child down — gently, with awareness of where the head is.</li>
      <li>Speak to it when the scene requires speaking to it. The voice does not change; the addressee is real.</li>
    </ul>

    <h3>10.2 When the object is held vs. when it is set down</h3>
    <p>Track this through the staging. The bundle is held more than the chair-and-coat (because the Child is younger). The chair-and-coat is set down most of the time, and the Step-Daughter or the Mother passes by it as one passes by one's child playing in a corner. The drowning at the fountain happens with the bundle <em>inside</em> the basin — the Step-Daughter bends over it; the drowning is hidden.</p>

    <h3>10.3 The Step-Daughter's relationship with the bundle</h3>
    <p>This is the warmest physical relationship in the play. The Step-Daughter kisses the top of the cloth, gently. She presses the bundle against her shoulder. She lifts and sets down repeatedly across Act Two. The recorded voice in Projection 2 carries the dialogue she would have with a living child; the live body carries the body language.</p>

    <h3>10.4 The drowning at the fountain</h3>
    <p>This is the production's most controlled single sequence. The bundle is set in the basin; the Step-Daughter bends over it; the basin is lit pale-blue from inside; the audience sees the back of the Step-Daughter, not the bundle. Nothing is enacted. Coach the actor to hold the bend for the length of the part — not less, not more.</p>
  </section>

  <section>
    <h2>11. The projections</h2>

    <h3>11.1 The three projection beats</h3>
    <p>One per act. Each does a different job.</p>
    <h4>11.1.1 Projection 1 — silent, top of Act One Part II</h4>
    <p>The Six arrive in video. The Boy walks to the chair and leaves his coat. The Step-Daughter sets the Child down and the Child becomes the bundle. The audience watches the convention be established. The live performers are still backstage.</p>
    <h4>11.1.2 Projection 2 — audible, top of Act Two Part I</h4>
    <p>The Step-Daughter's recorded voice addresses the Child and the Boy as real children. Then the revolver is found in the coat. The live Step-Daughter stands silent below the screen during this. Two bodies; one speaking.</p>
    <h4>11.1.3 Projection 3 — a held image, Act Three Part III</h4>
    <p>A single ten-second image of the chair behind the fountain. Not a video; a photograph held on screen. The image is the act of watching, not the death itself.</p>

    <h3>11.2 The live performer below the projection</h3>
    <p>In Projection 2, the Step-Daughter stands silent below her own recorded voice. This is the production's most counter-intuitive coaching demand: stand still, do not lip-sync, do not react, let the recording happen. Coach this until the stillness is total. The audience must read two Step-Daughters at once.</p>

    <h3>11.3 The screen as the production's third actor</h3>
    <p>The rear wall of the stage is the third performer in this production. Treat it as such. Confirm in tech that the projector can reach the brightness needed under the amber and red lighting states; confirm the audio levels on Projection 2 are right under house noise.</p>
  </section>

  <section>
    <h2>12. Light as direction</h2>

    <h3>12.1 The shower</h3>
    <p>A tight vertical column from a single overhead source, narrow enough for one performer and not two. It is used three times in Act Two and not elsewhere in the production. Coach the actors to find the column with their bodies — the column does not chase the body; the body steps into the column.</p>

    <h3>12.2 The slow drift from amber to red</h3>
    <p>Across Act One Part III, the amber drifts to deep red. The drift is so slow it should be unconscious for the audience until the act ends. Coach the operator to start the drift on the Step-Daughter's first <em>hundred francs</em>. Coach the actors to ignore the light entirely; they cannot acknowledge it without breaking the slow build.</p>

    <h3>12.3 The fountain's interior light</h3>
    <p>The basin lit pale-blue from inside, with a slight ripple effect if achievable. The light comes from the water — practically, from a fixture inside the basin under a layer of water. Confirm in tech that the ripple is not distracting; if it is, drop it.</p>

    <h3>12.4 Working with the operator</h3>
    <p>The light operator is your collaborator, not your servant. Walk the cue list with them well in advance of tech. Let them ask questions. The operator who understands <em>why</em> a cue lands at a particular line will get the cue better than the operator who is just hitting a button.</p>
  </section>

  <section>
    <h2>13. Sound as direction</h2>

    <h3>13.1 The pianist as performer</h3>
    <p>The pianist is the fourth Player. Visible to the audience throughout Act Two. Sits stage-right on the lower floor. Does not speak. Coach the pianist as you would coach an actor: tempo, attack, silence, the moment they enter and the moment they leave.</p>
    <p>Three live cues in Act Two:</p>
    <ul>
      <li>Satie's <em>Gymnopédie No. 1</em> under Projection 2 in Part I.</li>
      <li>The Weimar-shop vamp (Weill / Mistinguett) under the Madame Pace aria in Part II.</li>
      <li>The fragments of the vamp under the doubled scene in Part III, plus the held final chord.</li>
    </ul>

    <h3>13.2 The radio in the wings</h3>
    <p>Pre-show and into Act One Part I. An old French chanson, scratchy, low volume. Should feel like the company forgot to turn it off. Cuts mid-bar when the Door-keeper speaks. The cut is the cue for the production to begin.</p>

    <h3>13.3 The cello drone</h3>
    <p>Act Three Part I, low and sustained. The audience should feel a pulse in the room, not hear a note. Coach the operator to keep the volume below the threshold of consciousness. The drone dies on the Step-Daughter's line <em>His reality. He always knew exactly where to find me.</em></p>

    <h3>13.4 The Arvo Pärt at the end</h3>
    <p><em>Spiegel im Spiegel</em>, the first phrase, about ten seconds. After the Manager's last line, before the blackout. Plays once and stops. Do not loop. The audience must walk out into the lobby with the phrase still hanging.</p>
  </section>

  <!-- ============================================================ -->
  <!-- PART IV                                                      -->
  <!-- ============================================================ -->

  <h1 class="part page-break">Part IV &middot; Working with the Company</h1>
  <p class="part-eyebrow">Casting, audition, communication, the Village Players context</p>

  <section>
    <h2>14. The Village Players context</h2>

    <h3>14.1 The company</h3>
    <p>The Village Players are Lausanne's English-language amateur company at SSA Lausanne. Mixed-experience cast — some have done Shakespeare in their twenties; some have not been on stage in a decade; some are stepping in for the first time. The expat community in Lausanne supplies a steady pool of strong English voices from a range of national backgrounds.</p>

    <h3>14.2 Available rehearsal time</h3>
    <p>The production calendar gives the company:</p>
    <ul>
      <li>Three audition sessions (Tue 2 / Fri 5 / Wed 10 June 2026, 18:00–21:00).</li>
      <li>Seven Thursday table-work evenings (18 June – 30 July 2026, 18:00–21:00).</li>
      <li>Thirteen weeks of staging (5 August – 1 November 2026), Thursdays plus weekend sessions as needed.</li>
      <li>Performance run in late autumn 2026.</li>
    </ul>
    <p>This is more rehearsal time than many amateur productions, less than any professional one. Plan accordingly. Do not over-block in early sessions; do not leave key beats until the last fortnight.</p>

    <h3>14.3 The Lausanne anchoring</h3>
    <p>This production is set in Lausanne. The Players are Lausanne actors at SSA Lausanne. The Father, the Mother, and the rest could be families in any European city — but the room they meet in is Swiss and English-speaking. The Lausanne anchoring matters for the Players' register (modern French slips, local geography, Swiss reserve) and for the production's overall mood: precise, controlled, never showy.</p>
  </section>

  <section>
    <h2>15. Casting principles</h2>

    <h3>15.1 What you cast for in this play</h3>
    <p>You cast for:</p>
    <ol>
      <li><strong>Voice.</strong> Can they be heard? Can they carry an emotional register without forcing? Is the breath supporting the line, or running ahead of it?</li>
      <li><strong>Body.</strong> Does the body inhabit the role? Stillness, posture, age, presence — all read instantly.</li>
      <li><strong>Specificity.</strong> Do they make specific choices, or generalised ones?</li>
      <li><strong>Direction-taking.</strong> Can they take a note and apply it? Can they sustain a change across multiple beats?</li>
      <li><strong>Range.</strong> Can they play more than one register? Most roles in this play require at least two.</li>
    </ol>

    <h3>15.2 The Step-Daughter — youth, presence, no flirting</h3>
    <p>Reads young. Carries presence without flirtation. Holds eye contact when the scene needs it; drops it when she chooses. Comfortable with proximity without seductiveness. The audience must read her as the moral centre from the first scene; cast for the body that delivers that.</p>

    <h3>15.3 The Father — heat, shame, articulation</h3>
    <p>Around fifty. Articulate enough to carry the long speeches. Capable of shame as a physiological event. Has the breath for the four-stage arc. Cannot be too soft; cannot be too hard.</p>

    <h3>15.4 The Mother — stillness, specificity</h3>
    <p>Stillness that reads as presence, not blankness. Specific physical scoring even in the silences. Comfortable being covered (the heavy widow's veil). Voice capable of breaking on the keystone Act Two line.</p>

    <h3>15.5 The Son — withholding as performance</h3>
    <p>Knows what to do with a body that is refusing to engage. Comfortable being looked at without performing a reaction. Voice clear when finally used — the mirror speech in Act Three Part II must land.</p>

    <h3>15.6 The Players — working actors with comic timing</h3>
    <p>Three actors who can play a working rehearsal room together and read as a company within seconds of curtain. Comic timing for Act One; the discipline to fade to witness across Act Two and Three. Player 3 must double convincingly as Madame Pace.</p>

    <h3>15.7 The Manager — the audience's body on stage</h3>
    <p>A figure the audience would recognise as themselves. Not glamorous; not theatrically lit. The pragmatic centre. Reads as a man trying to finish a day's rehearsal, then trying to make sense of what has invaded it, then trying to leave with his sanity. Cast for a face the audience trusts.</p>

    <h3>15.8 Madame Pace — transformation skill</h3>
    <p>The actor playing Player 3 must transform on stage into Madame Pace. The transformation is the role. Cast for an actor with the physical control to land both — comic on arrival, chilling on exit. The wig and the silver chain do half the work; the body and voice do the rest.</p>
  </section>

  <section>
    <h2>16. Building the company</h2>

    <h3>16.1 The first meeting</h3>
    <p>This is the first table reading on Thursday 18 June 2026. Set the room as a working table from the first minute — chairs in a circle, the script in front of every reader, water, paper, pencils. Open with a brief production-concept walk-through (eight performers, two stage objects, three projections, three stripped settings); then read the play.</p>

    <h3>16.2 The rehearsal contract</h3>
    <p>An unwritten agreement that you make in the first session and re-state when needed:</p>
    <ul>
      <li>Arrive on time. Leave on time.</li>
      <li>Be present in the room. Phones in bags.</li>
      <li>Bring your script every session.</li>
      <li>Memorise your part by the date the calendar names.</li>
      <li>Notes go from the director to the actor. Acting notes between actors are not given.</li>
      <li>The Stage Manager runs the production's spine; coordinate scheduling with them, not with the director.</li>
    </ul>

    <h3>16.3 Communication patterns</h3>
    <p>The director communicates with the cast through:</p>
    <ul>
      <li><strong>The Assistant Director</strong> for day-to-day cast communication.</li>
      <li><strong>The Stage Manager</strong> for scheduling, logistics, distribution.</li>
      <li><strong>Direct contact</strong> when the matter is acting-specific or sensitive.</li>
    </ul>
    <p>The director does <em>not</em> route all messages personally. The director's attention is the production's most expensive resource.</p>

    <h3>16.4 The Assistant Director and Stage Manager</h3>
    <p>Both have their own pack (see <code>assistant_director_pack.pdf</code> and <code>stage_manager_pack.pdf</code>). The director's relationship with each is described there. The short version: the Assistant Director is the director's eyes when the director is not in the room; the Stage Manager makes the production run. Trust them. Let them do their work.</p>

    <h3>16.5 The pianist</h3>
    <p>The pianist is the fourth Player, credited as such. Confirm by 16 July 2026 (the Act Two table-work session). Walk the score with them in the same session. They join the company for the staging block and rehearse alongside the actors from August.</p>
  </section>

  <section>
    <h2>17. The audition room</h2>

    <h3>17.1 The director's checklist</h3>
    <p>The <em>Audition Checklist</em> (<code>audition_checklist.pdf</code>) is the director's working document during auditions. One page per role with the four categories — voice & breath, character & text, body & presence, direction-taking & range — plus a notes column. Bring it to every session.</p>

    <h3>17.2 The reading</h3>
    <p>Each auditioner reads a side from the <em>Audition Pack</em>. The side is from the part of the play where the character is most active. The auditioner has had the side in advance; the production has not yet heard them on it. First reading should be cold — let them do what they prepared.</p>

    <h3>17.3 The cold read</h3>
    <p>After the prepared side, ask the auditioner to read a second short passage cold. This tells you how they work with text they have not lived with. Cold reads betray habit; prepared reads betray taste. You need both.</p>

    <h3>17.4 The redirection</h3>
    <p>After the cold read, give the auditioner one adjustment. <em>Try it again, but quieter</em>, or <em>try it as if she is your mother</em>, or <em>try it without moving your hands</em>. Watch whether the adjustment lands. This single beat tells you whether they will take direction in a four-month rehearsal block.</p>

    <h3>17.5 Saying no kindly</h3>
    <p>Most auditioners will not be cast. They have given you their afternoon; they deserve the kindness of a clear answer in a reasonable timeframe. Send a brief, warm note within a week of the callback. Do not list reasons. <em>Thank you for coming in. We will not be casting you in this production.</em> That is enough.</p>

    <h3>17.6 Saying yes meaningfully</h3>
    <p>Casting is the most important decision the director makes. When you offer a role, be specific: <em>I want you to play X because of Y</em>. The actor needs to know why they were chosen. It anchors them for the four months ahead.</p>
  </section>

  <!-- ============================================================ -->
  <!-- PART V                                                       -->
  <!-- ============================================================ -->

  <h1 class="part page-break">Part V &middot; Pirandello in Particular</h1>
  <p class="part-eyebrow">Context, metaphysics, metatheatre, history</p>

  <section>
    <h2>18. The historical context</h2>

    <h3>18.1 1921 — Italy after the war</h3>
    <p>The play premiered in Rome in 1921, three years after the end of the First World War. Italy was politically unsettled — Mussolini's march on Rome would come a year later. The cultural scene was actively breaking with nineteenth-century forms. Futurism had been making noise since 1909; Pirandello himself was already past fifty and had been writing novels and short fiction for two decades before he turned to the stage. <em>Six Characters</em> arrives in a country that is reorganising what it expects from art.</p>

    <h3>18.2 The Italian theatre Pirandello was attacking</h3>
    <p>What Pirandello was tearing apart: the late nineteenth-century domestic drama, the well-made play, the naturalistic family scene with its three acts and its tidy moral resolution. He had watched theatre become bourgeois entertainment; he wanted it back as philosophical interrogation. <em>Six Characters</em> is, among other things, a polemic in dramatic form.</p>

    <h3>18.3 The play's hostile premiere</h3>
    <p>The Rome premiere on 9 May 1921 at the Teatro Valle ended in a riot. Audience members shouted <em>Manicomio! Manicomio!</em> — "Madhouse! Madhouse!" Pirandello had to escape through a back door. Five months later the Milan premiere was a triumph. The play has divided audiences ever since — partly because its central device (a play about people who walked in from outside a play) was new and remains, in some hands, alienating.</p>
    <p>For the director: the original audience was not prepared for the device. Yours is. Do not over-explain it.</p>
  </section>

  <section>
    <h2>19. The metaphysics</h2>

    <h3>19.1 Reality, mask, character</h3>
    <p>Pirandello's central preoccupation across his oeuvre is the gap between the self one presents and the self one is — between mask and face, between performance and being. <em>Six Characters</em> is his most direct staging of this preoccupation. The Six are masks that walked off the page; the actors are bodies trying to wear those masks; the gap is the play.</p>

    <h3>19.2 The eternal moment vs. the contingent moment</h3>
    <p>A character is eternal in one specific moment. The Step-Daughter is eternally at Madame Pace's shop in the moment of the hundred francs. She cannot be elsewhere. An actor is contingent — anywhere, anytime, free to leave the theatre. The play asks: which is more real?</p>
    <p>The director's challenge is to stage both states in the same room. The Six should read as inhabited by a single moment they cannot leave. The Players and Manager should read as people who could leave any time.</p>

    <h3>19.3 The fixed character in the unfixed world</h3>
    <p>The Father's argument in Act Three is that he, as a character, has integrity that the actors (and by extension the audience) cannot match. He is fixed; we change. He is one thing; we are many. He is therefore more real, in some sense, than we are. This is provocative philosophy. Direct it as provocation, not as truth.</p>
  </section>

  <section>
    <h2>20. The metatheatricality</h2>

    <h3>20.1 Why a play about a play</h3>
    <p>Because Pirandello had stopped believing that a naturalistic stage could carry the questions he wanted to ask. The fourth wall was a convention pretending not to be a convention. By making the theatre itself the subject, he restored the audience's awareness of the convention — which made it newly available to be moved.</p>

    <h3>20.2 How the device works in performance</h3>
    <p>The audience walks into a theatre to find an empty stage and a working rehearsal. They are immediately disoriented: is this the play, or before the play? The Six arrive and the disorientation deepens. By the time the Manager agrees to try staging their story, the audience has accepted the convention. The rest of the play exploits this acceptance.</p>

    <h3>20.3 The risk: the device becomes the play</h3>
    <p>Many productions of <em>Six Characters</em> lose to the device. They become productions <em>about</em> the metatheatre rather than productions of the family tragedy the metatheatre is in service of. This is the trap. The Six are not interesting because they are characters; they are interesting because their story is shameful, specific, and unresolved. Direct the story. The device frames it.</p>

    <h3>20.4 How to keep the play above the device</h3>
    <p>Three principles:</p>
    <ul>
      <li><strong>Make the Six's story land before the device gets clever.</strong> The shame, the hundred francs, the shop, the school gate — these must be specific and felt by the audience before any of the theatrical play gets interesting.</li>
      <li><strong>Keep the Manager pragmatic.</strong> If the Manager becomes a theorist, the play floats. Keep him interested in the day's work.</li>
      <li><strong>Trust the audience to follow the convention.</strong> They will. Do not over-signal.</li>
    </ul>
  </section>

  <section>
    <h2>21. Notable productions and what they teach</h2>

    <h3>21.1 Pitoëff, Paris 1923</h3>
    <p>Georges Pitoëff staged the Paris premiere two years after Rome. He lowered the Six from the flies on a freight elevator, with a green spotlight on them — they descended into the rehearsal from above, like ghosts arriving from another order of reality. The image has shaped every staging since. The lesson: the Six's entrance is part of the play; do not waste it.</p>

    <h3>21.2 Pirandello's own staging, 1925</h3>
    <p>By 1925 Pirandello had founded his own company (the Teatro d'Arte di Roma) and staged the play himself. He emphasised the practical, working-room texture of the rehearsal more than the metaphysics — closer to comedy at first, sharper at the end. The lesson: the comedy in Act One is not optional. It is the floor the rest of the play falls from.</p>

    <h3>21.3 The Royal Court production, London 1963</h3>
    <p>William Ball's staging at the Mayfair Theatre, with a young Anthony Hopkins as the Father. The production leaned into the Six as eerie, white-painted figures — a horror-movie reading. It worked then; it would not work now. The lesson: the eerie reading dates. The pragmatic reading lasts.</p>

    <h3>21.4 Robert Brustein's writings on the play</h3>
    <p>The American critic Robert Brustein wrote extensively on Pirandello in <em>The Theatre of Revolt</em> (1964), placing him among the modernists who rebelled against the bourgeois nineteenth-century stage. Brustein's framing is still useful for the director: Pirandello as a revolutionary inside the form. Read him before opening night if you have not.</p>

    <h3>21.5 What recent productions have got wrong</h3>
    <p>Three common errors of recent stagings:</p>
    <ul>
      <li><strong>Over-conceptualisation.</strong> Productions that decide the Six are <em>actually</em> projections of the Father's guilt, or actually ghosts, or actually political refugees. Pirandello's play is harder than any of these readings; let it be its own metaphysics.</li>
      <li><strong>Modernisation of the family situation.</strong> Productions that transpose the Madame Pace shop to a modern setting (the internet, a particular country, a particular industry). These date instantly. The 1920s framing carries because it allows the audience to think about now without being told.</li>
      <li><strong>Sentimentalising the Step-Daughter.</strong> Productions that round her into pity. She refuses pity in the script; the staging must refuse it too.</li>
    </ul>
  </section>

  <!-- ============================================================ -->
  <!-- PART VI                                                      -->
  <!-- ============================================================ -->

  <h1 class="part page-break">Part VI &middot; Practical Director's Work</h1>
  <p class="part-eyebrow">Calendar, notes, performance run</p>

  <section>
    <h2>22. Time management across the rehearsal block</h2>

    <h3>22.1 The table-work block — what must be set</h3>
    <p>By the end of Thursday 30 July 2026, the following must be set in the company's shared understanding:</p>
    <ul>
      <li>The four-stage Father arc and the autobiographical-as-metaphysical reading.</li>
      <li>The Step-Daughter's three cuts.</li>
      <li>The Mother's three silences.</li>
      <li>The Players' Lausanne register.</li>
      <li>The Light &amp; Sound score across all three acts.</li>
      <li>The chair-and-coat and the bundle as conventions.</li>
      <li>The three projection beats.</li>
      <li>The Madame Pace arc — comic on arrival, chilling on exit.</li>
    </ul>
    <p>Nothing has yet been blocked. What has been set is what blocking will be in service of.</p>

    <h3>22.2 The staging block — pacing of the thirteen weeks</h3>
    <p>(See full week-by-week in the Director's Copy and the SM Pack.)</p>
    <h4>22.2.1 First three weeks (Aug 5–20)</h4>
    <p>Act One on its feet. Big strokes first, specifics second. Do not over-block Act One Part I; the comedy needs room.</p>
    <h4>22.2.2 Middle four weeks (Aug 27 – Sep 17)</h4>
    <p>Acts Two and Three blocked. The hardest material. The pianist joins; the projections are timed in; the shower is placed.</p>
    <h4>22.2.3 Run-through weeks (Sep 24 – Oct 15)</h4>
    <p>Full run-throughs. Notes only between runs. Costumes for principals introduced.</p>
    <h4>22.2.4 Tech and dress (Oct 22, Oct 29, Nov 1)</h4>
    <p>The technical rehearsal is the Stage Manager's night. The director sits in the house and watches; notes go to the Stage Manager, not directly to the operators. Dress is full performance. Final dress is the last rehearsal.</p>

    <h3>22.3 Tech week — what to expect</h3>
    <p>Tech is when you discover what you have. Things break. Cues misfire. Sightlines do not work. An actor who was solid last week forgets the entire third act. Allow for it. The first run of tech is for the operators; the second is for the actors; the third is for you. Do not panic in tech; panic ends tech.</p>

    <h3>22.4 The week of</h3>
    <p>The week of opening, your job is not to direct. Your job is to keep the company calm, to deliver notes that are small and specific, to be visible without being intrusive. Do not introduce new ideas. The production is what it is now. Open it.</p>
  </section>

  <section>
    <h2>23. Notes — the director's most public document</h2>

    <h3>23.1 What good notes look like</h3>
    <ul>
      <li>Specific to a line, a moment, a beat, a cue.</li>
      <li>Actionable — the actor knows what to do with the note.</li>
      <li>Phrased as a verb where possible.</li>
      <li>Short — twenty words or fewer.</li>
      <li>Delivered after the rehearsal, not during, unless the moment truly cannot be left for later.</li>
    </ul>

    <h3>23.2 What bad notes look like</h3>
    <ul>
      <li>General — "more emotion", "less", "better".</li>
      <li>Adjectival — "be sadder", "be angrier", "be more present".</li>
      <li>Long — three paragraphs about the character's inner life when one sentence about a specific gesture would do.</li>
      <li>Delivered in front of the whole company when it concerns one actor's specific work.</li>
      <li>Repeated three sessions in a row without adjusting the wording — if the note has not landed, the language is wrong, not the actor.</li>
    </ul>

    <h3>23.3 The actor who can take notes vs. the actor who cannot</h3>
    <p>Some actors absorb notes the way a sponge absorbs water; some absorb them the way a stone absorbs water. Diagnose this early. For the sponges, you can give five notes a session. For the stones, give one note a session and watch it land before adding more. The stones are not worse actors; they are differently paced learners. Adjust.</p>

    <h3>23.4 The note that is really a re-direction</h3>
    <p>Sometimes a note is not a note but a change in direction. <em>What if you played the whole scene sitting?</em> is not a note; it is a re-staging. Be honest about which you are giving. The actor needs to know whether they are adjusting or starting over.</p>
  </section>

  <section>
    <h2>24. The performance run</h2>

    <h3>24.1 Watching the run from the house</h3>
    <p>Sit in a different section of the house each night. The view from the front-row centre is not the view from the side balcony. Take small written notes during the show, not after; you will forget by the time you get home. Take care not to be visibly note-taking — it spooks the cast if they see you writing.</p>

    <h3>24.2 Notes between shows</h3>
    <p>Between performances (matinée to evening, or night to night), give the company a brief, calm notes session. Keep it short. The actors are tired. They need to know what to hold and what to adjust. Five minutes; specific; warm.</p>

    <h3>24.3 Letting go on opening night</h3>
    <p>The production is no longer yours after the first night. It belongs to the actors, to the Stage Manager who calls it, to the audience who watches it. Your job is to witness. Resist the urge to direct after opening. The Stage Manager runs the show now.</p>

    <h3>24.4 The post-mortem</h3>
    <p>After the closing performance, the company strikes the set, and the Stage Manager and the director sit down for a post-mortem within the following week. What worked. What did not. What we would do differently. What the room taught us. The post-mortem is not for the cast; it is for the next production.</p>
  </section>

  <!-- ============================================================ -->
  <!-- PART VII                                                     -->
  <!-- ============================================================ -->

  <h1 class="part page-break">Part VII &middot; What Kiarash Must Hold</h1>
  <p class="part-eyebrow">The compass — the pitfalls — the final principles</p>

  <section>
    <h2>25. The director's compass for this production</h2>

    <h3>25.1 Bounded bodies, unbounded moral force</h3>
    <p>The physical choreography of contact in this play is bounded — see <code>intimacy_protocol.pdf</code>. The moral weight is unbounded. The audience should leave uncomfortable not because the bodies did more, but because everything around the bodies did more. This is the production's first principle, and it shapes every staging decision.</p>

    <h3>25.2 The Lausanne anchoring</h3>
    <p>The play is in Lausanne. The Players are at SSA Lausanne. The Madame Pace shop is above the rue de Bourg. The French chanson in the wings is Aznavour or Piaf. The audience is Swiss-English-speaking and expat. Keep this register in your ear. Do not let the production drift toward generic European.</p>

    <h3>25.3 The Manager as the audience's body on stage</h3>
    <p>The Manager is the audience. He arrives where they arrive — at a working rehearsal, mid-comedy. He is invaded by the Six as they are. He tries to make sense of it as they do. He ends exhausted as they should. Direct him as the audience's stand-in throughout. The audience reads him as the figure most like them.</p>

    <h3>25.4 The Step-Daughter as the moral centre</h3>
    <p>Not a coquette. Not a victim performing victimhood. A young woman holding the room accountable. The production succeeds or fails on whether the audience reads her this way. Coach every other character against the temptation to soften her.</p>

    <h3>25.5 The Madame Pace arc — comedy on arrival, horror on exit</h3>
    <p>The single hardest beat of the production. The arrival is funny — the broken French, the wig, the bookkeeping. The exit is not. The audience must laugh once and then not be allowed to laugh again. Player 3's transformation is the production's hinge.</p>
  </section>

  <section>
    <h2>26. What the production cannot do</h2>

    <h3>26.1 The precocious metatheatre</h3>
    <p>If the production becomes interested in itself — in the fact that it is a play about a play — it has lost the play. The metatheatre is a frame, not a subject. Do not let the staging signal "look how clever this is". The Six's story must be the point.</p>

    <h3>26.2 The sentimental Father</h3>
    <p>If the audience pities the Father, the production has misread him. He is not a tragic hero; he is a man arguing for his life against a room that knows what he did. He may be sympathetic in flashes; he is not redeemable. The staging must hold him at arm's length.</p>

    <h3>26.3 The coquettish Step-Daughter</h3>
    <p>If she flirts, the play collapses. If she cries, the play collapses. She must hold her position as the room's most articulate witness. Cast for this and coach for this; do not allow drift.</p>

    <h3>26.4 The empty Son</h3>
    <p>If the Son's refusal reads as a passive choice — boredom, sulk, withdrawal — the role becomes nothing. The refusal must read as active. He has decided not to act, and he is acting that decision every second.</p>

    <h3>26.5 The decorative Mother</h3>
    <p>If the Mother is staged as a figure of grief — a draped silhouette, a sob behind a veil — she becomes scenery. She is a body that has chosen to be small. The actor must decide what the body is doing every second.</p>
  </section>

  <section>
    <h2>27. Final principles</h2>

    <h3>27.1 The director is also a witness</h3>
    <p>You will spend months inside this play. By opening night the play will be inside you. Your last job, on the night, is to sit in the house and witness it as the audience does. That is not abdication; it is what the play has been waiting for.</p>

    <h3>27.2 The audience leaves uncomfortable, by design</h3>
    <p>The Manager's last line — <em>I've lost a whole day over these people. A whole day.</em> — is not catharsis. The audience walks out into the Lausanne autumn carrying the play with them. Some will be angry. Some will be silent. Some will not know yet what they think. This is the production landing.</p>

    <h3>27.3 The play survives every staging</h3>
    <p>It has survived a hostile premiere in 1921, a green-spotlit Pitoëff entrance in 1923, a horror-movie Royal Court in 1963, and a century of productions in between. It will survive this one. Your job is not to honour the play. Your job is to stage it. The play will take care of itself.</p>

    <div class="pull-quote">
      A character, sir, may always ask a man who he is. Because a character has really a life of his own, marked with his especial characteristics; for which reason he is always "somebody." But a man — I'm not speaking of you now — may very well be "nobody."
      <br><br>
      &mdash; The Father, Act Three
    </div>

    <h3>27.4 One last thing</h3>
    <p>The play is harder than any director who attempts it. That is the play's nature. Do not expect to solve it. Stage what you understand; trust the rest to the room. The production will find its own shape if you keep the compass clean.</p>
  </section>

  <footer class="foot">
    <p><strong>Village Players · Lausanne</strong> &nbsp;·&nbsp; Director: Kiarash Jamshidi</p>
    <p>This is a director's notebook. Not for circulation. The Director's Copy is the production's authoritative document; this handbook is its companion.</p>
  </footer>

</main>

</body></html>
"""

HTML_PATH = OUT_DIR / "directors_handbook.html"
HTML_PATH.write_text(HTML)

OUT = OUT_DIR / "directors_handbook.pdf"
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
