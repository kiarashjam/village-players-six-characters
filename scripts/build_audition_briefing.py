#!/usr/bin/env python3
"""Build the Audition Briefing PDF.

A director's briefing for the audition room — one page per speaking role
for all nine (Father, Mother, Step-Daughter, Son, Manager, Player 1,
Player 2, Player 3, Madame Pace). Each page gives the look, the
behaviour, the tone of speaking, what to coach against, plus a
three-sentence solo monologue the auditioner can read alone, and a
"what to listen for" note for the director's ear.

Madame Pace is a Character carried by her own performer; her page
includes the accent-and-ledger test that finds the role.
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


  footer.foot { margin-top: 9mm; padding-top: 4mm;
                border-top: 1px solid var(--rule);
                font-size: 9.5pt; color: var(--ink-soft);
                font-style: italic; text-align: center; line-height: 1.55; }
  footer.foot strong { font-style: normal; color: var(--ink); }
</style>
</head><body>

<main>

  <div class="masthead">
    <p class="eyebrow">Audition Briefing &nbsp;·&nbsp; All Nine Speaking Roles</p>
    <h1>Six Characters<br>in Search of an Author</h1>
    <p class="play">Sei personaggi in cerca d'autore &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
    <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne &nbsp;·&nbsp; late autumn 2026</p>
    <p class="credit" style="margin-top:6px;">Director: <strong>Kiarash Jamshidi</strong></p>
  </div>

  <section class="intro">
    <h2>What this is</h2>
    <p>A director's briefing for the audition room, covering all nine speaking roles in the order they appear in the Director's Copy: <strong>the Father, the Mother, the Step-Daughter, the Son, the Manager, Player 1, Player 2, Player 3, and Madame Pace</strong>. For each role, one page: what the character should look like, how they should behave, the tone of speaking, what to coach against — and a <strong>three-sentence solo monologue</strong> the auditioner can read alone, cold or prepared. Each solo is written to show the character's whole personality in a minute or less. (The Boy and the Child are stage objects, not played by performers; they are not auditioned.)</p>

    <h2>How to use it in the room</h2>
    <ul>
      <li><strong>Prepared first.</strong> Let the auditioner read the solo once as they have prepared it. Do not interrupt.</li>
      <li><strong>One adjustment, then read it again.</strong> A single redirection — "play it quieter"; "play the third sentence as if you were telling it to your closest friend"; "start it as if you have just walked in" — tells you more about their range than the first read does.</li>
      <li><strong>Watch the body, not just the voice.</strong> Where does the chin go on a vain line? Where does the breath shorten on a shameful one? Does the auditioner stay still during a silence, or fill it?</li>
      <li><strong>For Madame Pace</strong>, the page includes an accent-and-ledger test: the same lines read twice — once for the accent, once for the cold underneath it. That second reading is the one that finds the role.</li>
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
  <!-- THE MOTHER                                                   -->
  <!-- ============================================================ -->

  <section class="role">
    <div class="role-head">
      <h2>The Mother</h2>
      <p class="role-tag">grief carried, not performed — the three silences</p>
    </div>

    <h3>Look</h3>
    <p><strong>Late 40s to mid-50s.</strong> Pirandello: she "seems crushed and terrified as if by an intolerable weight of shame and abasement. She is dressed in modest black and wears a thick widow's veil of crêpe. When she lifts this, she reveals a wax-like face. She always keeps her eyes downcast." Costume: full mourning, with the <strong>heavy widow's veil of black crêpe</strong> — the veil is half the costume, and the actor must have lived with it long enough that she carries it the way a real widow carries hers, not the way a costumed one does. Body: small, contained, pressed in on itself. When the veil is lifted (once in Act One by the Father; once at the end by herself), the face beneath is pale, set, and unmoving.</p>

    <h3>Behaviour</h3>
    <p>The play's only character who does not argue for herself. She has been silent for so long that silence has become her register, and the few moments she does speak land with the weight of all the silence around them. <strong>She has three silences</strong>, each a different shape — one in Act One when the Father lifts the veil, one in Act Two when she is forced to watch the shop scene, one in Act Three before the fountain. The body is doing something specific every second: the right hand at the veil's hem; the left hand pressed flat to the bundle she carries; the breath that stops when the line cuts. Carries the bundle (the Child) almost throughout; stays close to the chair-and-coat (the Boy). <strong>Her eruption is the keystone:</strong> <em>"It's taking place now. It happens all the time."</em> She has been silent for an entire act and a half; she finds her voice in one breath, and the room changes with her.</p>

    <h3>Tone of speaking</h3>
    <p><strong>Few words. Simple words.</strong> Direct, not articulate — the precise opposite of the Father's circling philosophy. When she does speak, you must hear that she has been holding it for a long time before she let it out. The voice <strong>breaks under pressure</strong> rather than resists it: it does not push, it falters. The keystone line — <em>"It's taking place now. It happens all the time"</em> — is the only moment she comes fully into voice across the whole production. Coach her elsewhere as a person who is reaching for words she has not used in twenty years.</p>

    <h3>Coach against</h3>
    <ul>
      <li><strong>Sentimentality.</strong> The Mother is not pitiable — she is contained. People decide she is gentle because she does not argue; she does not argue because there is nothing left to win.</li>
      <li><strong>Performing grief.</strong> The grief is carried, not displayed. Generalised "grieving" is not the role; specificity is.</li>
      <li><strong>Being scenery.</strong> She is a body that has <em>chosen</em> to be small. The actor decides what the body is doing every second the veil is down.</li>
    </ul>

    <div class="solo">
      <p class="solo-label">Three-sentence solo &nbsp;·&nbsp; read alone</p>
      <p class="solo-text">"I have spent twenty years in other people's rooms — first my own husband's, who sent me away with no reason except his own, then another man's, who at least believed he loved me until he died, then a rented one off the rue de Bourg, and a smaller one after that, with the children. I have not the words my husband has, nor the anger my daughter has, nor whatever it is my son keeps shut behind his face all these years — I have only the children, and the years between them, and a veil I have not been able to put down since the day they buried him. If I were to start speaking now, sir, all that would come out would be the names of those children, in the order the years took them from me — and I cannot trust my voice to hold even that, so I will not start."</p>
    </div>

    <div class="listen">
      <p class="listen-label">What to listen for</p>
      <p>A voice that <em>almost</em> doesn't make it through the third sentence. The Mother is at the edge of speech, not in command of it. Listen for restraint without going blank — does the auditioner stay specific (the children, the rooms, the veil) without slipping into general sorrow? The button — <em>"so I will not start"</em> — is the line that should make you look up. If the auditioner pushes the speech, redirect: "say it as quietly as you can without losing the room."</p>
    </div>
  </section>

  <!-- ============================================================ -->
  <!-- THE STEP-DAUGHTER                                            -->
  <!-- ============================================================ -->

  <section class="role">
    <div class="role-head">
      <h2>The Step-Daughter</h2>
      <p class="role-tag">the moral centre — sharp, indicting, never coquettish</p>
    </div>

    <h3>Look</h3>
    <p><strong>Late teens to early twenties.</strong> Pirandello: "dashing, almost impudent, beautiful. She wears mourning too, but with great elegance." Costume: black mourning, but cut with elegance — sharp lines, not soft. The audience must read the age difference with the Father from the back row, instantly. Body: holds a room without flirting. She knows where her eyes go and keeps them there. Hair and makeup understated — the elegance is in the posture, not in the styling.</p>

    <h3>Behaviour</h3>
    <p>The moral centre of the play. Not the Father with his philosophy, not the Manager with his stagecraft — <em>her</em>. Her anger is precise: she is in a room of theatre people who would like to turn what was done to her into <em>a scene</em>, <em>a moment</em>, <em>a confession</em> — anything but what it actually is — and she refuses every single one of those softenings. <strong>Tender to the bundle</strong> (the Child) — her tenderness must be unbearably real. <strong>Contempt for the chair-and-coat</strong> (the Boy) — the same wound, pointed the other way. Across Act Three Part I she cuts the Father three times, surgically, with escalating force. The seduction the old text gestures at is <strong>not flirtation</strong>; it is <strong>exposure</strong>, a weapon turned outward because everything else has been taken from her.</p>

    <h3>Tone of speaking</h3>
    <p><strong>Precise. Indicting. She lands.</strong> The opposite of the Father's spiral — every sentence reaches its target. Sharp consonants, clear vowels. Cold rage; wit that is rage. Specific, never ornamental. The register is: <em>stop making this beautiful. Stop making this clever. Stop making this safe. This happened. Look at it.</em> Her one moment of softness is with the bundle in the Act Two opening monologue; that softness must read as the same person in a different room, not as a different woman.</p>

    <h3>Coach against</h3>
    <ul>
      <li><strong>Coquettishness.</strong> Not a flirt. The play collapses if she flirts.</li>
      <li><strong>Crying.</strong> The play also collapses if she cries. The audience has not earned her tears, and she knows it.</li>
      <li><strong>Bigness.</strong> Specific is more frightening than big. She does not need to raise her voice.</li>
      <li><strong>Coldness as performance.</strong> She is cold because she has decided to be cold; the choice must be readable, not the temperature.</li>
    </ul>

    <div class="solo">
      <p class="solo-label">Three-sentence solo &nbsp;·&nbsp; read alone</p>
      <p class="solo-text">"Everyone in this room has been working very hard for the last ten minutes not to look directly at me — I have been watching you do it, very politely, the way you all look at the corner of the room when a difficult subject has been raised at dinner. There is a man, sitting somewhere behind me right now, who paid a hundred francs in a back room off the rue de Bourg for half an hour with a girl who turned out to be his own wife's daughter; I am the girl, and what I have come for, this morning, is the half-hour. I am not interested in your tears, or your tact, or whatever face it is you are currently arranging to listen to me with — I want it told, as it was, in the room it happened in, and I will tell it whether you stage it or not."</p>
    </div>

    <div class="listen">
      <p class="listen-label">What to listen for</p>
      <p>Surgical, not loud. The audition value is in how she carries the second sentence — <em>"I am the girl, and what I have come for, this morning, is the half-hour"</em> — without ornament, without breaking, without inviting pity. If the auditioner softens, redirect: "say the second sentence as if you were reading the time off a clock." If she warms, you have lost her. The right reading is a cold room temperature; you should feel slightly less safe by the end.</p>
    </div>
  </section>

  <!-- ============================================================ -->
  <!-- THE SON                                                      -->
  <!-- ============================================================ -->

  <section class="role">
    <div class="role-head">
      <h2>The Son</h2>
      <p class="role-tag">the refuser — withholding as an act</p>
    </div>

    <h3>Look</h3>
    <p><strong>Around 22.</strong> Pirandello: "tall, severe in his attitude of contempt for the Father, supercilious and indifferent to the Mother. He looks as if he had come on the stage against his will." Dark suit, mourning, withdrawn. <strong>Closed posture</strong> — hands in pockets or arms folded, the geometry of refusal made physical. Reads older than twenty-two because of how withdrawn he is. The body has decided not to move; the face has decided not to react.</p>

    <h3>Behaviour</h3>
    <p>The refuser. Will not participate. Will not engage. Will not perform the family. <strong>His silence is active, chosen, kept</strong> — not absence, not sulking, not a mood. He has been making the same decision since he was a small boy in an empty house, and he is keeping it in front of strangers now. Eyes stay on the floor for long stretches without dropping focus. The Step-Daughter's accusations land on him and the body does not move. His one extended moment of voice is the <strong>mirror speech in Act Three Part II</strong> — the single sentence he has decided to say, after years of holding it. After the speech, he returns to silence. <strong>The Father grabs his arm</strong> at <em>"You can force him, sir"</em>; the Son lets him, and does not give him the scene he has come for.</p>

    <h3>Tone of speaking</h3>
    <p>When he does speak, <strong>clean, sharp, declarative.</strong> No ornament, no spiralling, no philosophy. The Father's exact opposite. Cold in a different way from the Step-Daughter — hers is hot rage frozen; his is just deep cold. Slow rhythm: he gives the room time to feel each sentence land. The voice has been kept quiet for years; it does not need to push. <strong>He never raises it.</strong></p>

    <h3>Coach against</h3>
    <ul>
      <li><strong>Sulking.</strong> Refusal must read as a chosen position, not a mood. The audience must feel the decision underneath, not the petulance on top.</li>
      <li><strong>Blankness.</strong> The Son is alive inside the refusal. He is having a continuous decision, not sleeping. Stillness must read as presence.</li>
      <li><strong>Loudness when he does break silence.</strong> The mirror speech is not a release; it is a single chosen sentence said by a man who has decided, finally, to say it.</li>
      <li><strong>Generalised brooding.</strong> The actor must have decided what the body is doing in every silence — looking where, breathing how. Generic withdrawn-young-man is not the role.</li>
    </ul>

    <div class="solo">
      <p class="solo-label">Three-sentence solo &nbsp;·&nbsp; read alone</p>
      <p class="solo-text">"I have not asked to be here this morning, and I do not propose to pretend that I have — my father can stand in front of you and talk for an hour about the philosophy of why we are characters and what reality means and what suffering owes to art, and I can sit in this chair, exactly as I am sitting in it now, and tell you with my whole body that I disagree. You will read me, sooner or later, as sulking, or as withholding, or as a young man who is going to be drawn into the scene if you all just give him a little time and a glass of water — and you will be wrong, all three of you who think it, in three slightly different ways. I have been making the same decision since I was six years old, in a house that should have had a mother in it and did not, and the decision is no — the only thing that has changed across all those years is that I am now old enough to say it out loud, in a room of strangers, without raising my voice once."</p>
    </div>

    <div class="listen">
      <p class="listen-label">What to listen for</p>
      <p>Stillness that reads as presence, not blankness. The voice does not push; the auditioner does not need volume to be heard. Listen for whether the third sentence — <em>"the same decision since I was six years old"</em> — carries weight without sentimentality. The button — <em>"without raising my voice once"</em> — should be exactly that: kept quiet. If the auditioner gets loud, redirect: "play it as if there is one person in the room you would like to hear you, and everyone else is in the next room."</p>
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
  <!-- PLAYER 2                                                     -->
  <!-- ============================================================ -->

  <section class="role">
    <div class="role-head">
      <h2>Player 2 — the Leading Lady</h2>
      <p class="role-tag">the veteran character actress who actually <em>is</em> what Player 1 pretends to be</p>
    </div>

    <h3>Look</h3>
    <p><strong>Mid-50s to 60.</strong> The bearing of the most experienced person in the room, worn lightly. Costume: working-rehearsal clothes, slightly less groomed than Player 1, because she does not need to perform seniority — she has it. <strong>Shoulders down, weight forward</strong> — the bearing of someone who has been in this room before, in this exact argument, with this exact Leading Man. For the Leading Lady function: a little more put together. For the Property Man function: sleeves rolled. The flip between the two is in the bearing alone, no prop signals it.</p>

    <h3>Behaviour</h3>
    <p>Has done leads at every house in the canton — a Marivaux at Vidy years ago, a Beckett at the Pulloff that they still talk about. Has had drinks with the cantonal arts council. She is, in fact, the senior actor in the company; she does not need to say so. Her seniority is in her shoulders. <strong>The diva is real, earned, tired.</strong> The Property Man this season because the company could not afford a real one and she would not let the show open without a folding screen — she built the screen herself, out of two old flats and a hinge she bought yesterday. <strong>The wound:</strong> when she climbs onto the upper platform in Act Two to play the Step-Daughter and is laughed at by a woman half her age who has actually been through the room she is being asked to fake. The diva's posture collapses; the voice changes; she has been made a fool of by better, and she means it.</p>

    <h3>Tone of speaking</h3>
    <p><strong>Pragmatic, professional, often dry.</strong> Working-actor vocabulary — <em>rent, wage, professional, the trade.</em> Level voice; she does not raise it. The wit is real but never showy — the wit of a person making the morning tolerable. A note of weariness that has earned its place. Where Player 1 stretches every sentence to make himself important, Player 2 lands hers in the fewest syllables and moves on.</p>

    <h3>Coach against</h3>
    <ul>
      <li><strong>Bitterness.</strong> Player 2 is not bitter; she is level. There is a real warmth under the dryness — coach for that.</li>
      <li><strong>Maternal warmth.</strong> She is not anyone's mother. The warmth is collegial, not parental.</li>
      <li><strong>Camping the working-actor pragmatism.</strong> The lines should sound true, not performed. The audience must believe she actually has rent to pay.</li>
      <li><strong>Treating the Property Man role as comic relief.</strong> She does the props because she is the only person who will do them properly. She is not a clown in either register.</li>
    </ul>

    <div class="solo">
      <p class="solo-label">Three-sentence solo &nbsp;·&nbsp; read alone</p>
      <p class="solo-text">"I have been at the Village Players for thirty-one years this season — which is, I am told, rather longer than several of the actors currently in this company have been alive, although nobody has yet had the kindness to confirm the figure for me directly. I have played leads at Vidy, at the Pulloff, at every house in this canton that still has a roof on it, and this morning I am building a folding screen out of two old flats and a hinge I bought yesterday from a shop you have never heard of, because the company can no longer afford a Property Man and I would rather build a screen than open a show without one. So when our Leading Man tells me, as he has just now, that he has <em>principles</em> about which hat he will or will not wear in Act One — well, sir, I have a hinge, a script, and a wage to earn before the end of the month, and you can perhaps imagine which of those three things I am proposing we discuss first."</p>
    </div>

    <div class="listen">
      <p class="listen-label">What to listen for</p>
      <p>A level voice that does the work without effort. Listen for whether the auditioner can land the phrase <em>"longer than several of the actors currently in this company have been alive"</em> without bitterness or pride — that is the test of the role. The button line — <em>"which of those three things I am proposing we discuss first"</em> — should land as a working actor's punchline, dry, almost weary, not as a comic beat. If the auditioner pushes for laughs, redirect: "play it as if you are still building the screen while you say it."</p>
    </div>
  </section>

  <!-- ============================================================ -->
  <!-- PLAYER 3                                                     -->
  <!-- ============================================================ -->

  <section class="role">
    <div class="role-head">
      <h2>Player 3 — the youngest in the company</h2>
      <p class="role-tag">curious, leaning in, the audience's mirror</p>
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
      <li><strong>Disappearing in the second half.</strong> She has few lines after Act One, but her face is the audience's mirror at every horror. Cast someone who stays alive while watching.</li>
    </ul>

    <div class="solo">
      <p class="solo-label">Three-sentence solo &nbsp;·&nbsp; read alone</p>
      <p class="solo-text">"This is my first proper season — I keep saying that, I know, but it is true, and I keep saying it because I want you to know that whatever I get wrong this morning I will write down, and learn, and not get wrong again next time. I have spent every evening for two weeks reading the Pirandello on the tram on the way home from work, and the strangest thing is that the more I read it the less it stops being strange — there is a family in it that I think I almost know, and a young woman in it who is trying so hard to be heard that I find I am sitting up straighter on the tram every time she speaks. I do not yet know whether I am an actress or a person who is currently acting, but I would very much like, if you will let me, to spend the next six months finding out — and I promise you I will not be the easiest person in the room, but I will be the most awake."</p>
    </div>

    <div class="listen">
      <p class="listen-label">What to listen for</p>
      <p>Young, clear, slightly rising at the end of clauses — the voice of someone who has not decided yet, but wants you to consider it. Resist the urge (theirs or yours) to make her a generic ingenue: she is <strong>curious</strong>, not naive. The audition value is in the last line: can the auditioner <em>promise</em> without becoming cute?</p>
    </div>

  </section>

  <!-- ============================================================ -->
  <!-- MADAME PACE                                                  -->
  <!-- ============================================================ -->

  <section class="role">
    <div class="role-head">
      <h2>Madame Pace — the businesswoman of shame</h2>
      <p class="role-tag">comic on arrival, chilling on exit — a Character, her own performer</p>
    </div>

    <h3>Look</h3>
    <p><strong>Indeterminate middle age — read as older than the company.</strong> Fat, bleach-blonde, rouged and powdered, dressed with a comical elegance in black silk, a long silver chain at the waist ending in a pair of scissors. An Italian-Swiss immigrant who has run an atelier off the rue de Bourg long enough to half-forget her first language and never quite learn her second. She is not played by one of the Players — she is a Character of her own, conjured onto the stage in Act Two by its very arrangement (the hats on the pegs, the shop window, the folding screen). The actor walks through the upstage door and is simply <em>there</em>, as if she had always been.</p>

    <h3>Behaviour</h3>
    <p><strong>A hostess at her own front door, all evening.</strong> Pleased to be here, generous with the smile, never hurried, never loud. Her danger is that she is calm. She does not threaten; she keeps accounts. The comedy of the accent is the entrance; the bookkeeping is the body of her. <strong>Arc inside one scene:</strong> the room laughs at her first line and is disgusted with itself for having laughed by her last — and the smile never drops, only what she is saying changes.</p>

    <h3>Tone of speaking</h3>
    <p>A thick accent — Italian-Swiss and French both worn into her English, the speech of a woman who has lived in Lausanne too long to sound native and not long enough to lose her first tongue. Warm, smiling, practical. The cold is in the content, never in the volume. Phrases that land for her: <em>"I am a good woman, sir." "He clean. He polite. He pay cash." "Pace, she always balance the book."</em></p>

    <h3>Coach against</h3>
    <ul>
      <li><strong>An accent joke.</strong> The accent is the gateway, not the role. If she is only funny, she has not done her job.</li>
      <li><strong>Menace played loud.</strong> She never raises her voice. The chill comes from the smile staying exactly where it was.</li>
      <li><strong>Dropping the comedy too early.</strong> Play the comedy at full strength on arrival so the turn has something to turn from.</li>
    </ul>

    <div class="solo">
      <p class="solo-label">Three-sentence solo &nbsp;·&nbsp; read alone</p>
      <p class="solo-text">"Good morning, good morning, sir — so sorry I am late, the trams in this town, always the same, but here I am, here I am, and Madame Pace she never disappoint a customer. I am a good woman, sir — forty years in this canton and never one bad word about Pace — only, you understand, the lady over there she ruin the silk again, the third time this month, and silk you no pay with the tears, somebody must pay, the mother she pay with the hands or the little one she pay, eh, either way the book she balance. I no wanta be hard — I never wanta be hard — but the polite ones, sir, the ones who keep the count, we are the ones who are still here at the end; the rest, they only weep, and weeping, you will find, it pay nobody nothing."</p>
    </div>

    <div class="listen">
      <p class="listen-label">What to listen for</p>
      <p>Read it twice. First for the accent — can the auditioner carry it without flinching, without apologising for it? Then again, in the same voice but <strong>calm, smiling, as if reading a column of figures in a ledger</strong>. The second reading is the test: can they be <em>cold</em> inside the comedy — the bookkeeping smile that makes the room regret having laughed? If the second reading frightens you a little, you have your Madame Pace.</p>
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
