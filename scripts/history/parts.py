#!/usr/bin/env python3
"""Divide each act into 3 parts with a substantial pre-part director's note."""
import re
from pathlib import Path

SRC = Path("/home/claude/six_characters.html")
html = SRC.read_text()

# ---------------------------------------------------------------------------
# CSS for .part-note
# ---------------------------------------------------------------------------
PART_CSS = r"""
/* === Part-of-act note panels === */
.part-note {
  margin: 64px 0 44px;
  padding: 40px 42px 38px;
  background: color-mix(in srgb, var(--paper-warm) 50%, var(--paper));
  border: 1px solid var(--rule);
  border-radius: 2px;
  position: relative;
  box-shadow: 0 18px 50px -36px color-mix(in srgb, var(--ink) 24%, transparent);
}
.part-note::before {
  content: "";
  position: absolute;
  left: 0; right: 0; top: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent) 16%, var(--accent) 84%, transparent);
  opacity: 0.55;
}
.part-note .part-eyebrow {
  font-family: 'Cormorant Unicase', serif;
  font-size: 10px;
  letter-spacing: 0.5em;
  color: var(--accent);
  margin-bottom: 10px;
  text-transform: uppercase;
  font-weight: 500;
}
.part-note h3.part-title {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 300;
  font-style: italic;
  font-size: clamp(24px, 3.1vw, 32px);
  margin: 0 0 28px;
  line-height: 1.16;
  color: var(--ink);
  letter-spacing: -0.005em;
}
.part-note .pn-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px 40px;
  margin-bottom: 22px;
}
@media (max-width: 720px) {
  .part-note .pn-grid { grid-template-columns: 1fr; gap: 16px; }
  .part-note { padding: 28px 24px 26px; }
}
.part-note .pn-section h4 {
  font-family: 'Cormorant Unicase', serif;
  font-size: 9px;
  letter-spacing: 0.5em;
  color: var(--accent);
  margin: 0 0 8px;
  text-transform: uppercase;
  font-weight: 500;
}
.part-note .pn-section p {
  margin: 0;
  font-family: 'Cormorant Garamond', 'EB Garamond', serif;
  font-style: italic;
  font-size: calc(var(--base-fs, 19px) * 0.92);
  line-height: 1.62;
  color: var(--ink-soft);
}
.part-note .pn-questions {
  border-top: 1px solid var(--rule);
  padding-top: 22px;
  margin-top: 6px;
}
.part-note .pn-q-label {
  font-family: 'Cormorant Unicase', serif;
  font-size: 9px;
  letter-spacing: 0.5em;
  color: var(--accent);
  margin-bottom: 12px;
  text-transform: uppercase;
  font-weight: 500;
}
.part-note .pn-questions p {
  margin: 0 0 10px;
  font-family: 'Cormorant Garamond', 'EB Garamond', serif;
  font-style: italic;
  font-size: calc(var(--base-fs, 19px) * 0.94);
  line-height: 1.6;
  color: var(--ink-soft);
  padding-left: 22px;
  position: relative;
}
.part-note .pn-questions p::before {
  content: "—";
  position: absolute;
  left: 0;
  color: var(--accent);
  font-style: normal;
}
.part-note .pn-questions p:last-child { margin-bottom: 0; }
"""

# Inject CSS
html = html.replace("</style>", PART_CSS + "\n</style>", 1)

# ---------------------------------------------------------------------------
# THE 9 PART NOTES
# ---------------------------------------------------------------------------
PARTS = [
    # ============ ACT I ============
    {
        "act_roman": "I", "act_word": "Act One", "part_roman": "I",
        "title": "The Rehearsal",
        "what": "The company arrives at a half-lit theatre to rehearse a Pirandello play, Mixing It Up. The Manager bickers with the Leading Man about wearing a cook's cap. The Prompter settles into his box. The apparatus of the working theatre asserts itself first — letters, props, dim light, irritation.",
        "how": "We open inside the machine before we know what the play is. The audience watches a rehearsal that does not yet know it is about to become a play. Lighting is ordinary stage work-light; bodies move as people, not as Characters. The Manager is brisk and theatrical, performing professionalism for an audience he doesn't yet know is there.",
        "when": "The world's default state — before any rupture. Imagined real time: a quarter of an hour before the action of the comedy proper begins. Nothing has happened. The clock has not started.",
        "feeling": "Casual, comic, slightly bored. Coffee-cup-and-paper energy. An air of well-worn complaint. The smell of a closed rehearsal room. The audience should feel they have walked in too early.",
        "questions": [
            "What does an honest rehearsal look like to an audience that has paid to watch a play?",
            "When the Manager mocks the playwright he is forced to stage, is he a fool or the most honest theatre-maker in the room?",
            "Has the play already started — or is it still waiting for a door to open?",
        ],
    },
    {
        "act_roman": "I", "act_word": "Act One", "part_roman": "II",
        "title": "The Plea",
        "what": "Six figures enter through the back door, carrying a strange tenuous light. The Father asks for an author. The Step-Daughter taunts and exposes. The Mother lifts her veil and faints. The Father explains his marriage, the secretary he sent his wife away with, the wet-nurse for his son in the country. Every confession is contradicted by the next mouth. The family is laid bare, and laid bare twice.",
        "how": "The screen ignites: pre-recorded footage of The Boy and The Child joins the family tableau at the rear of the set. The four live Characters stand on the apron in actual flesh. The actors slowly recede to the wings, becoming audience to their own stage. The lighting tightens on the family while the rehearsal room dims around them. Tones travel from comedy to interrogation.",
        "when": "The play's first real entry into its subject. We pass from talking about a rehearsal to being inside a thing that has no name yet. The proscenium begins to thin.",
        "feeling": "Beginning amused, ending unbearable. The actors laugh at first. The Mother's faint changes the temperature in the room. By the end the laughter has been silenced and the family stands inside its own argument. Something has been opened that cannot be politely closed.",
        "questions": [
            "Whose truth wins on a stage — the loudest, the first, or the most wounded?",
            "Can the Mother's silent body argue better than the Father's eloquent mouth?",
            "Can a play be inside people the way the Father claims — and if so, where is it stored?",
            "If these six are characters in search of an author, what does that make us, the watchers?",
        ],
    },
    {
        "act_roman": "I", "act_word": "Act One", "part_roman": "III",
        "title": "The Bargain",
        "what": "The shop of Madame Pace is named for the first time. The hundred lire. The pale blue envelope. The Father offers his great speech on the many-sided conscience: we are not one self, and to be caught in one moment is to be falsified by it. The Son refuses to enter the story. The Father describes how the drama ends — the death of the Child, the tragedy of the Boy, the flight of the Step-Daughter. The Manager begins to think there is a play in this. He exits to his office with the Characters. The actors are left alone, baffled.",
        "how": "The Father's monologues are the philosophical engine of the act. They must be played as urgent, not as essays — a man arguing for his life, not lecturing about it. The Son stands apart and refuses, and his refusal is itself a performance. The Manager's transformation from cynic to interested party should feel both slightly comic and slightly chilling. By the curtain on this part, the actors-as-audience are the only ones left on stage.",
        "when": "The end of the first act. The bargain has been struck. The audience leaves this part knowing only that something serious has begun, that the rules of theatre are not the ones we walked in with, and that the Manager has accepted authorship of something he did not write.",
        "feeling": "Charged, philosophical, ironic. The Step-Daughter is feverish; the Father is in mid-flight; the Son is cold; the Mother is present like a stone. The actors hover at the edge — comic, unsettled, beginning to lose their professional ground.",
        "questions": [
            "Who is the author when the writer has refused? Can a director become one by accident?",
            "What does it mean to have a drama inside you — and is that the same as having a soul?",
            "The Son says I don't come into this. Why does a refusal to act still register as acting?",
            "Should the audience leave this act on the side of the actors, or the side of the Characters?",
        ],
    },

    # ============ ACT II ============
    {
        "act_roman": "II", "act_word": "Act Two", "part_roman": "I",
        "title": "Backstage",
        "what": "The Step-Daughter erupts from the Manager's office with The Child and The Boy. She speaks tenderly to the Child about an imaginary garden, an imaginary fountain. She discovers the revolver in the Boy's pocket. The Son and Mother come out and circle each other in silence and accusation. The Manager organises the rehearsal: the white parlour, the table, the screen, the pegs. The Prompter is told to take shorthand. Names are assigned to the Characters. The Father falters at the sound of his own name.",
        "how": "The act opens behind the scenes. The screen ignites again: pre-recorded footage of The Child and The Boy joins the Step-Daughter as she handles them with one hand tender and one hand hard. Then the apparatus reasserts itself — Property Man, Machinist, Prompter, the white parlour fitted up around the family's pain like furniture. Two registers cross each other in this part: the metaphysical (Step-Daughter and Child) and the technical (the room being built).",
        "when": "Twenty imagined minutes after Act One. The bargain is being executed. The drama is being prepared for the stage by hands that don't know what they are preparing.",
        "feeling": "Strange and suspended. The Step-Daughter's tenderness with the Child is unbearable because we know what is coming. The room fills with stagehands and the air goes commercial again. There is something terrible about how easily the technical takes over from the holy.",
        "questions": [
            "Why is the Step-Daughter — the most worldly Character — the one who speaks to the doomed children?",
            "How does a screen carry a child? What does it mean to address pre-recorded video as if it were present?",
            "When the Prompter is told to take shorthand, has authorship already begun — and if so, who is the author?",
            "What is gained, and what is lost, when the Father's name (Amalia, his wife's name) is suddenly heard as a stage name?",
        ],
    },
    {
        "act_roman": "II", "act_word": "Act Two", "part_roman": "II",
        "title": "The Apparition",
        "what": "The Father asks the actresses to hang their hats and mantles on pegs. The door at the back of the stage opens. Madame Pace appears, summoned, it seems, by the very mise-en-scène. The Step-Daughter recognises her. Madame Pace speaks in half-Italian, half-English, comical and grotesque. The Step-Daughter begins to play the scene of the shop with her. Then the Mother sees her, recognises her, and erupts: You old devil! You murderess!",
        "how": "The strangest scene of the play. A Character not in the original six is invited into being by the setting alone — by pegs, by a screen, by the magic of arranged objects. Player 3 enters Madame Pace's costume the way an apparition enters a body. She is fat, oxygenated, ridiculous. The Step-Daughter speaks her shop dialogue half-mimed, half-spoken, almost inaudibly. Then the Mother's living rage tears the apparition's spell apart.",
        "when": "The middle of Act Two. The drama's scene of shame is about to be played — but it cannot proceed while the Mother is present. The play breaks its own scene, and the actors, watching, do not understand what they are watching.",
        "feeling": "Sleazy, theatrical, comic — and then suddenly horrible. The pale blue envelope. The screen. The hundred lire. The Step-Daughter's coquetry. The Mother's scream. The temperature in the room collapses in seconds.",
        "questions": [
            "Can a setting summon a character? If so, who is more real — the actress hired to play Madame Pace, or this thing that is Madame Pace herself?",
            "When the Mother breaks the scene by recognising it, is she ruining the play or saving it?",
            "Is Madame Pace's comical jargon a mercy or an obscenity? Why does Pirandello let us laugh at her?",
            "What does it mean to play a scene only on condition that the witness leaves the room?",
        ],
    },
    {
        "act_roman": "II", "act_word": "Act Two", "part_roman": "III",
        "title": "The Substitution",
        "what": "The Father and Step-Daughter play out the first beats of the shop scene themselves. Then the Manager hands the scene to his Leading Lady and Leading Man. They try the same lines. The Step-Daughter laughs at them. The Father objects: they are not us. The Step-Daughter insists on the truth — what was actually said, what was actually done. The Mother breaks in: It's taking place now. It happens all the time. She cries out as she did in life. Curtain.",
        "how": "The structural inversion of the act. Characters and Actors trade places, and neither can stand the other. The Father's complaint is metaphysical; the Step-Daughter's is sharper — the actor will soften it, package it, make it sayable. Pirandello forces the audience to watch the same scene twice and feel both versions as inadequate. The Mother's cry is the act's first true unmediated sound, and the curtain must fall on it.",
        "when": "End of Act Two. The play's first real climax. The Machinist drops the curtain by mistake, in earnest, on what was only supposed to be a rehearsal effect. The audience leaves the act unsettled and a little ashamed of having been entertained.",
        "feeling": "Comic, then increasingly raw. The Leading Lady is offended; the Step-Daughter is in pain; the Father is in disbelief; the Mother has finally been allowed to scream. By the curtain line all the irony has burned off and only the insistence of grief in the present tense remains.",
        "questions": [
            "Can a professional actor play a real person without falsifying them? Is the falsification the point of theatre, or its sin?",
            "When the Machinist drops the curtain by accident, who is the author of that accident?",
            "Whose now is the Mother's now? Is it 1921, the night of the performance, or every night a Mother has watched her daughter walk into Madame Pace's shop?",
            "Should the curtain fall on the cry, or should it be held up just long enough for the audience to be implicated in not stopping it?",
        ],
    },

    # ============ ACT III ============
    {
        "act_roman": "III", "act_word": "Act Three", "part_roman": "I",
        "title": "The Argument over Reality",
        "what": "The curtain rises on a garden set hurriedly by the stagehands. A drop, a fountain basin, two wings. The Manager is plotting. The Step-Daughter complains that the garden cannot hold the whole drama because the Son is always shut in his room. The Father objects to the word illusion. He says the Characters have no other reality outside this one — and that the Manager's reality, by contrast, may seem an illusion to him tomorrow. Can you tell me who you are?",
        "how": "This is the play's most philosophical stretch. The Father becomes the dramatist that Pirandello cannot help being. The Manager refuses the bait; the Step-Daughter is impatient with the metaphysics. Yet the Father's argument holds, because of how directly it is aimed: at the Manager, at the actors, at us. Lighting can pull in. The garden set must seem hastily improvised — painted cardboard, as the Step-Daughter said in Act Two.",
        "when": "Opening of Act Three. The Manager misnumbers his own play (Ah yes: the second act!) — a quiet joke that places us inside Pirandello's recursion. We have begun again, and the beginning is an argument about whether we exist.",
        "feeling": "Cool, argumentative, then quietly terrifying. The audience is being asked, without warning, whether it exists in the same way the Characters do. The Father is reasonable, then philosophical, then almost desperate. The Manager's stage-manager pragmatism begins to look thin.",
        "questions": [
            "If a Character's reality cannot change, is the actor playing the Character free, or doubly imprisoned?",
            "Are we, watching, more or less real than the people on the stage?",
            "When the Father says you and I… and the Manager cuts him off — what did he almost say?",
            "Why does Pirandello let the Manager misnumber the act? What does it mean that the Manager doesn't know which act of his own life he is in?",
        ],
    },
    {
        "act_roman": "III", "act_word": "Act Three", "part_roman": "II",
        "title": "The Refusal",
        "what": "The Manager tries to combine the garden scene and the indoor scene into one staged action. The Boy is to hide behind a tree. The Child is to play by the fountain. The Son refuses to act. The Step-Daughter laughs at his refusal — he cannot leave, she says, he is indissolubly bound to the chain. The Son delivers his speech on the mirror that freezes him with a likeness thrown back as a horrible grimace. The Father tries to force him to play the scene. The Mother begs.",
        "how": "This is the Son's hour. He refuses the play and yet remains in it — the perfect Pirandellian condition. The Step-Daughter taunts him precisely because she knows he cannot leave. The Mother trembles because she knows it too. The mirror image is the play's most terrible figure. Staging must isolate the Son physically — alone on stage, surrounded by people who want him to move. The Boy stands behind a tree in projection, mute and waiting.",
        "when": "Middle of Act Three. The action drags itself toward the climax against the resistance of its own central refuser. The Son is the one who has been right all along, and being right does not save him.",
        "feeling": "Tense, frozen, miserable. There is no laughter left in the room. Everything is being arranged for a tragedy that no one on stage wants to perform. The audience feels the weight of an inevitability they cannot stop watching.",
        "questions": [
            "Why does a refusal not free you from a play? Why does saying no still count as a performance?",
            "Can a Character be a critic of the play they are in?",
            "When the Son says I act nothing and we watch him do exactly that — is the play winning or losing?",
            "Is staging itself the mirror the Son is afraid of? Are we, the audience, the grimace?",
        ],
    },
    {
        "act_roman": "III", "act_word": "Act Three", "part_roman": "III",
        "title": "The Fountain",
        "what": "The Step-Daughter takes The Child to the fountain. The Son finally tells what he saw: he ran across the garden, jumped to drag the Child out, and was frozen by the sight of The Boy standing stock still, his eyes mad, watching his little drowned sister. A revolver shot rings out from behind the trees. The Mother cries out. The actors lift the body. Some say he is dead, others say it is only pretence. The Father, with a terrible cry: Pretence? Reality, sir, reality! The Manager: To hell with it all. I've lost a whole day over these people. Curtain.",
        "how": "The climax is delivered as a memory, not as a scene. The Son narrates the fountain and the revolver. The screen carries the action — the drowning, the shot — and no live actor enters the violence. This is Pirandello's strictest cruelty: the most terrible thing in the play is the thing the audience does not actually see happen. The final exchange must be played as a real argument the play refuses to settle. The Manager's last word — contempt, fatigue — should not be allowed to feel like a punchline.",
        "when": "The end. There is nothing after this. The Manager's exhaustion is the play's final word, and it is contempt for the people who took up his day.",
        "feeling": "Cold, fast, brutal — then over. The make-believe debate that ends the play is a debate the play has refused to resolve. The lights must come down on disagreement, not on understanding.",
        "questions": [
            "If the audience never sees the children die, does that make their deaths more or less real?",
            "Whose voice is right at the end — the Father's Reality! or the Manager's Pretence!?",
            "Is the play asking us to choose, or asking us to notice we cannot?",
            "When we leave the theatre and forget the play, which side of the final argument have we joined?",
        ],
    },
]

# ---------------------------------------------------------------------------
# Render each part note as HTML
# ---------------------------------------------------------------------------
def render_part_note(p):
    questions_html = "\n      ".join(
        f"<p>{q}</p>" for q in p["questions"]
    )
    return f'''
  <aside class="part-note">
    <div class="part-eyebrow">Part {p["part_roman"]} of {p["act_word"]}</div>
    <h3 class="part-title">{p["title"]}</h3>

    <div class="pn-grid">
      <div class="pn-section">
        <h4>What</h4>
        <p>{p["what"]}</p>
      </div>
      <div class="pn-section">
        <h4>How</h4>
        <p>{p["how"]}</p>
      </div>
      <div class="pn-section">
        <h4>When</h4>
        <p>{p["when"]}</p>
      </div>
      <div class="pn-section">
        <h4>The Feeling</h4>
        <p>{p["feeling"]}</p>
      </div>
    </div>

    <div class="pn-questions">
      <div class="pn-q-label">Theatre Questions</div>
      {questions_html}
    </div>
  </aside>
'''

# Build the 9 rendered notes
notes = [render_part_note(p) for p in PARTS]

# ---------------------------------------------------------------------------
# INSERT THE 9 NOTES
# Each act has 3 inserts: Part I goes after the existing directors-note
# closing tag; Parts II & III go before specific dialogue anchors.
# ---------------------------------------------------------------------------

# --- ACT I ---
# Part I: insert after closing </aside> of "before Act I" directors-note,
# right before the data-opener stage direction.
html = html.replace(
    '</aside>\n\n  <p class="stage" data-opener="1">The spectators will find',
    '</aside>\n' + notes[0] + '\n  <p class="stage" data-opener="1">The spectators will find',
    1
)

# Part II: insert before the projection-begin cue (which sits right after
# the Son's description ending in "...on the stage against his will.").
html = html.replace(
    'He looks as if he had come on the stage against his will.</p>\n\n  <p class="projection-cue">',
    'He looks as if he had come on the stage against his will.</p>\n' +
    notes[1] +
    '\n  <p class="projection-cue">',
    1
)

# Part III: insert before Manager's "There is something in what you say"
html = html.replace(
    '<p class="speech"><span class="speaker">The Manager</span>. There is something in what you say.',
    notes[2] +
    '\n  <p class="speech"><span class="speaker">The Manager</span>. There is something in what you say.',
    1
)

# --- ACT II ---
# Part I: after the directors-note for "before Act II"
html = html.replace(
    '</aside>\n\n  <p class="stage" data-opener="1">The stage call-bells ring',
    '</aside>\n' + notes[3] + '\n  <p class="stage" data-opener="1">The stage call-bells ring',
    1
)

# Part II: before "The door at the back of stage opens and Madame Pace enters"
html = html.replace(
    '<p class="stage">The door at the back of stage opens and <strong>Madame Pace</strong> enters',
    notes[4] +
    '\n  <p class="stage">The door at the back of stage opens and <strong>Madame Pace</strong> enters',
    1
)

# Part III: before Leading Lady's "Of course! It's easy enough!"
html = html.replace(
    '<p class="speech"><span class="speaker">Player 2 <span class="as-role">(as Leading Lady)</span></span>. Of course! It\'s easy enough!',
    notes[5] +
    '\n  <p class="speech"><span class="speaker">Player 2 <span class="as-role">(as Leading Lady)</span></span>. Of course! It\'s easy enough!',
    1
)

# --- ACT III ---
# Part I: after the directors-note for "before Act III"
html = html.replace(
    '</aside>\n\n  <p class="stage" data-opener="1">When the curtain goes up again',
    '</aside>\n' + notes[6] + '\n  <p class="stage" data-opener="1">When the curtain goes up again',
    1
)

# Part II: before Manager's "Oh for God's sake, will you at least finish with this philosophizing"
html = html.replace(
    '<p class="speech"><span class="speaker">The Manager</span>. Oh for God\'s sake, will you at least finish with this philosophizing',
    notes[7] +
    '\n  <p class="speech"><span class="speaker">The Manager</span>. Oh for God\'s sake, will you at least finish with this philosophizing',
    1
)

# Part III: before Step-Daughter's "Wait a minute, wait... First of all, the baby has to go to the fountain..."
html = html.replace(
    '<p class="speech"><span class="speaker">The Step-Daughter</span>. Wait a minute, wait',
    notes[8] +
    '\n  <p class="speech"><span class="speaker">The Step-Daughter</span>. Wait a minute, wait',
    1
)

# ---------------------------------------------------------------------------
# SAVE
# ---------------------------------------------------------------------------
SRC.write_text(html)
print(f"Wrote {SRC}: {len(html):,} bytes  ({html.count(chr(10)):,} lines)")
