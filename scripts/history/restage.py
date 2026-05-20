#!/usr/bin/env python3
"""Transform six_characters.html for an 8-performer + screen staging:
  - 4 Character actors (Father, Mother, Step-Daughter, Son)
  - 1 Manager
  - 3 Players covering all company roles + Madame Pace
  - Boy and Child appear only as projection (cued in text)
"""
import re
from pathlib import Path

SRC = Path("/home/claude/six_characters.html")
html = SRC.read_text()

# ---------------------------------------------------------------------------
# 1. SPEAKER MAP — Character names unchanged; company roles → Player tags
# ---------------------------------------------------------------------------
# Tuple form ("Player N", "Role") renders as: Player N (as Role)
# String form renders flat.
SPEAKER_MAP = {
    # Characters — unchanged
    "The Manager":              "The Manager",
    "Manager":                  "The Manager",
    "The Father":               "The Father",
    "The Mother":               "The Mother",
    "The Step-Daughter":        "The Step-Daughter",
    "The Son":                  "The Son",
    "Manager and Father":       "The Manager and The Father",

    # ---------- PLAYER 1 ----------
    "Leading Man":              ("Player 1", "Leading Man"),
    "The Leading Man":          ("Player 1", "Leading Man"),
    "Leading Actor":            ("Player 1", "Leading Man"),
    "L'Ingénue":                ("Player 1", "L'Ingénue"),
    "Door-keeper":              ("Player 1", "Door-keeper"),
    "Machinist":                ("Player 1", "Machinist"),
    "Third Actor":              "Player 1",

    # ---------- PLAYER 2 ----------
    "Leading Lady":             ("Player 2", "Leading Lady"),
    "The Leading Lady":         ("Player 2", "Leading Lady"),
    "Property Man":             ("Player 2", "Property Man"),
    "Fourth Actor":             "Player 2",

    # ---------- PLAYER 3 ----------
    "Juvenile Lead":            ("Player 3", "Juvenile Lead"),
    "The Juvenile Lead":        ("Player 3", "Juvenile Lead"),
    "Prompter":                 ("Player 3", "Prompter"),
    "The Prompter":             ("Player 3", "Prompter"),
    "Madame Pace":              ("Player 3", "Madame Pace"),
    "An Actor":                 "Player 3",
    "Fifth Actor":              "Player 3",

    # ---------- CHORUSES ----------
    "The Actors":               "All Three Players",
    "Some Actors":              "Two Players",
    "Other Actors":             "The Other Players",
    "The Actresses":            "All Three Players",
    "Some Actresses":           "Two Players",
    "Actors and Actresses":     "All Three Players",
}

def render_speaker_html(value):
    """Render a SPEAKER_MAP value as inner HTML for <span class='speaker'>."""
    if isinstance(value, tuple):
        player, role = value
        return f'{player} <span class="as-role">(as {role})</span>'
    return value

# Replace every <span class="speaker">NAME</span>
def replace_speaker(match):
    name = match.group(1).strip()
    if name not in SPEAKER_MAP:
        # Leave unknown speakers alone (shouldn't happen)
        return match.group(0)
    return f'<span class="speaker">{render_speaker_html(SPEAKER_MAP[name])}</span>'

html = re.sub(r'<span class="speaker">([^<]+)</span>', replace_speaker, html)

# ---------------------------------------------------------------------------
# 2. NEW CSS — for (as Role), casting note, projection cues, cast table
# ---------------------------------------------------------------------------
NEW_CSS = r"""
/* === (as Role) sub-tag inside .speaker === */
.speaker .as-role {
  font-variant: normal;
  font-feature-settings: "smcp" 0;
  font-style: italic;
  font-weight: 400;
  color: var(--ink-soft);
  letter-spacing: 0.01em;
  font-size: 0.82em;
  text-transform: none;
  margin-left: 0.18em;
}

/* === Casting note section before Act I === */
.casting-note {
  margin: 96px 0 64px;
  padding: 52px 48px 48px;
  background: color-mix(in srgb, var(--paper-warm) 65%, var(--paper));
  border: 1px solid var(--rule);
  border-radius: 2px;
  position: relative;
  box-shadow: 0 1px 0 var(--rule),
              0 28px 70px -40px color-mix(in srgb, var(--ink) 30%, transparent);
}
.casting-note::before {
  content: "";
  position: absolute;
  left: 0; right: 0; top: 0;
  height: 2px;
  background: linear-gradient(90deg,
    transparent, var(--accent) 18%, var(--accent) 82%, transparent);
  opacity: 0.65;
}
.casting-note::after {
  content: "PRODUCTION";
  position: absolute;
  top: 14px;
  right: 22px;
  font-family: 'Cormorant Unicase', serif;
  font-size: 9px;
  letter-spacing: 0.35em;
  color: var(--accent);
  opacity: 0.65;
}
.casting-note .cn-eyebrow {
  font-family: 'Cormorant Unicase', serif;
  font-size: 10px;
  letter-spacing: 0.5em;
  color: var(--accent);
  margin-bottom: 18px;
  text-transform: uppercase;
  font-weight: 500;
  text-align: center;
}
.casting-note h2 {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 300;
  font-style: italic;
  font-size: clamp(26px, 3.4vw, 34px);
  margin: 0 0 36px;
  text-align: center;
  line-height: 1.18;
  color: var(--ink);
  letter-spacing: -0.005em;
}
.casting-note h3 {
  font-family: 'Cormorant Unicase', serif;
  font-size: 11px;
  letter-spacing: 0.42em;
  color: var(--accent);
  font-weight: 500;
  margin: 32px 0 14px;
  text-transform: uppercase;
}
.casting-note p {
  margin: 0 0 16px;
  font-size: calc(var(--base-fs, 19px) * 0.94);
  line-height: 1.72;
  color: var(--ink);
}
.casting-note p strong {
  color: var(--accent);
  font-weight: 600;
}
.casting-note .cue {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  color: var(--accent);
  font-weight: 500;
}
.casting-note table.cast-table {
  border-collapse: collapse;
  margin: 18px 0 6px;
  width: 100%;
  font-size: calc(var(--base-fs, 19px) * 0.9);
}
.casting-note table.cast-table th {
  text-align: left;
  font-family: 'Cormorant Garamond', serif;
  font-variant: small-caps;
  font-feature-settings: "smcp" 1;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: var(--accent);
  padding: 12px 18px 12px 0;
  vertical-align: top;
  width: 110px;
  white-space: nowrap;
  border-right: 1px solid var(--rule);
}
.casting-note table.cast-table td {
  padding: 12px 0 12px 18px;
  font-family: 'Cormorant Garamond', 'EB Garamond', serif;
  color: var(--ink-soft);
  line-height: 1.6;
  font-style: italic;
}
.casting-note .cn-quote {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: calc(var(--base-fs, 19px) * 0.98);
  color: var(--ink-soft);
  border-left: 2px solid var(--accent);
  padding: 4px 0 4px 16px;
  margin: 12px 0 20px;
  background: linear-gradient(90deg, color-mix(in srgb, var(--accent) 4%, transparent), transparent 80%);
}
.casting-note .cn-sign {
  text-align: right;
  font-family: 'Cormorant Infant', serif;
  font-style: italic;
  color: var(--accent);
  margin: 30px 0 0;
  letter-spacing: 0.12em;
  font-size: 14px;
}

/* === Projection cue paragraphs === */
.projection-cue {
  text-align: center;
  margin: 32px auto;
  padding: 12px 20px;
  max-width: 78%;
  border-top: 1px dashed var(--accent);
  border-bottom: 1px dashed var(--accent);
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  color: var(--accent);
  font-size: 0.95em;
  letter-spacing: 0.01em;
  line-height: 1.55;
}
.projection-cue .proj-label {
  display: block;
  font-family: 'Cormorant Unicase', serif;
  font-style: normal;
  font-size: 9px;
  letter-spacing: 0.5em;
  color: var(--accent);
  margin-bottom: 6px;
  text-transform: uppercase;
  font-weight: 500;
}
.projection-cue .proj-label::before {
  content: "▶ ";
  margin-right: 4px;
}
.projection-cue.ends .proj-label::before {
  content: "■ ";
}

/* === Cast subsection heading === */
.cast-h3 {
  font-family: 'Cormorant Infant', 'Cormorant Garamond', serif;
  font-style: italic;
  font-weight: 400;
  font-size: 17px;
  letter-spacing: 0.03em;
  text-align: center;
  color: var(--ink-soft);
  margin: 0 0 22px;
  font-feature-settings: "smcp" 0;
}
.cast li .role-list {
  display: block;
  font-style: italic;
  font-size: 12px;
  letter-spacing: 0.04em;
  color: var(--ink-faint);
  font-variant: normal;
  margin-top: 2px;
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
}
"""

# Inject the new CSS before </style>
html = html.replace("</style>", NEW_CSS + "\n</style>", 1)

# ---------------------------------------------------------------------------
# 3. REPLACE the cast list section
# ---------------------------------------------------------------------------
NEW_CAST_HTML = r"""<section class="cast">
    <h2>Dramatis Personæ</h2>
    <p class="cast-sub">for an eight-performer staging with screen</p>

    <div class="cast-group">
      <h3 class="cast-h3">The Six Characters</h3>
      <ul>
        <li>The Father</li>
        <li>The Mother</li>
        <li>The Step-Daughter</li>
        <li>The Son</li>
        <li>The Boy<span class="silent">silent — pre-recorded projection</span></li>
        <li>The Child<span class="silent">silent — pre-recorded projection</span></li>
        <li>Madame Pace<span class="silent">embodied by Player 3</span></li>
      </ul>
    </div>

    <div class="cast-group" style="margin-top:48px;">
      <h3 class="cast-h3">The Theatre Company</h3>
      <ul>
        <li>The Manager</li>
        <li>Player 1<span class="role-list">Leading Man · L'Ingénue · Door-keeper · Machinist · Third Actor</span></li>
        <li>Player 2<span class="role-list">Leading Lady · Property Man · Fourth Actor · Second Lady Lead</span></li>
        <li>Player 3<span class="role-list">Juvenile Lead · Prompter · Madame Pace · An Actor · Fifth Actor</span></li>
      </ul>
    </div>
  </section>"""

html = re.sub(
    r'<section class="cast">.*?</section>',
    NEW_CAST_HTML,
    html,
    count=1,
    flags=re.DOTALL,
)

# ---------------------------------------------------------------------------
# 4. INSERT new "Director's Casting Note" section between scene-setting and Act I
# ---------------------------------------------------------------------------
CASTING_NOTE_HTML = r"""
  <section class="casting-note">
    <div class="cn-eyebrow">A Note on This Production</div>
    <h2>How this version is to be performed</h2>

    <p>This edition adapts Pirandello's play for a chamber staging of <strong>eight live performers and one screen</strong>. Every line of the Storer translation is preserved. Only the <em>who-plays-what</em> is rearranged.</p>

    <h3>Eight Bodies on the Stage</h3>
    <p><strong>Four play the family.</strong> The Father, The Mother, The Step-Daughter, and The Son are each played by a single actor in flesh, and each remains so for the whole play.</p>
    <p><strong>One plays The Manager.</strong> Pirandello's director-figure stays exactly as written.</p>
    <p><strong>Three play everyone else.</strong> The dozen lesser company roles of the original — Leading Man, Leading Lady, Juvenile Lead, L'Ingénue, Property Man, Prompter, Door-keeper, Machinist, the Second Lady Lead, the Third / Fourth / Fifth Actors — are divided among three Players. <strong>Madame Pace</strong>, who is a Character rather than a company actor but who appears only briefly in Act Two by the magic of the stage, is also embodied by Player 3 in costume and wig.</p>

    <h3>One Surface in Place of Two Bodies</h3>
    <p>The Boy (fourteen) and the Child (about four) — the silent youngest of the Six — are not embodied by live performers. Their presence is <strong>pre-recorded video, projected onto the rear wall of the set</strong> at the moments their roles require. The other Characters look at them, speak about them, handle them: the audience sees only the screen.</p>
    <p>The cues <span class="cue">[Projection begins]</span> and <span class="cue">[Projection ends]</span> mark when the footage must run. Between cues, the screen is dark; the family addresses an absence.</p>

    <h3>How the Three Players Divide the Company</h3>
    <p>The division is built on a single rule: <em>no Player should ever speak as one of their roles in direct dialogue with another of their own roles.</em> Every adjacency in the play was checked against this rule.</p>

    <table class="cast-table">
      <tr><th>Player 1</th><td>Leading Man · L'Ingénue · Door-keeper · Machinist · Third Actor</td></tr>
      <tr><th>Player 2</th><td>Leading Lady · Property Man · Second Lady Lead (silent) · Fourth Actor</td></tr>
      <tr><th>Player 3</th><td>Juvenile Lead · Prompter · Madame Pace · An Actor · Fifth Actor</td></tr>
    </table>

    <p>The graph admits one unavoidable corner: in the beat of Act Two where Madame Pace materialises, Player 1 must speak briefly as L'Ingénue and as Leading Man within a few moments. The director should handle this with a wig signifier or a brief turn of the body. All other transitions are clean.</p>

    <p>Chorus moments — what Pirandello marks as <em>The Actors, Some Actresses, Actors and Actresses</em> — are gathered in this text under <strong>All Three Players</strong> or <strong>Two Players</strong>, and may be split between them at the director's discretion.</p>

    <h3>How Speaker Tags Look in This Edition</h3>
    <p>When a Player speaks one of their assigned roles, the speaker tag in this text reads:</p>
    <p class="cn-quote"><strong>Player 1 <span style="font-style:italic;color:var(--ink-soft);font-weight:400;">(as Leading Man)</span></strong>. Excuse me, but must I absolutely wear a cook's cap?</p>
    <p>The bold word is the performer; the lighter italic in parentheses is the role they are inhabiting in that moment. The four family Characters and The Manager keep their proper names without parentheses, because each is played by only one performer throughout.</p>

    <p class="cn-sign">— K. J.</p>
  </section>
"""

# Insert immediately before the first <section class="act-header"> (which is Act I)
html = html.replace(
    '<section class="act-header">\n    <div class="label">Act the First</div>',
    CASTING_NOTE_HTML.strip() + '\n\n  <section class="act-header">\n    <div class="label">Act the First</div>',
    1
)

# ---------------------------------------------------------------------------
# 5. PROJECTION CUES — inject [Projection begins/ends] at Boy/Child moments
# ---------------------------------------------------------------------------
def proj_begin(text):
    return (
        f'<p class="projection-cue"><span class="proj-label">Projection begins</span>'
        f'{text}</p>'
    )

def proj_end(text="The screen fades to black."):
    return (
        f'<p class="projection-cue ends"><span class="proj-label">Projection ends</span>'
        f'{text}</p>'
    )

# ---- ACT I projection envelope ----
# BEGIN: after the Son's description, before Door-keeper's first line.
# The Son description ends with "He looks as if he had come on the stage against his will."
html = html.replace(
    'He looks as if he had come on the stage against his will.</p>\n\n  <p class="speech"><span class="speaker">Player 1 <span class="as-role">(as Door-keeper)</span></span>',
    'He looks as if he had come on the stage against his will.</p>\n\n  ' +
    proj_begin("Pre-recorded footage of THE BOY (fourteen, in black) and THE CHILD (about four, in white with a black silk sash) appears on the rear screen, taking their place at the edge of the family tableau. They remain visible throughout the act, treated by the others as present in the room.") +
    '\n\n  <p class="speech"><span class="speaker">Player 1 <span class="as-role">(as Door-keeper)</span></span>',
    1
)

# END Act I projection: after MANAGER and Six CHARACTERS cross off and before "Leading Man. Is he serious?"
html = html.replace(
    'looking at one another in astonishment.]</span></p>\n\n  <p class="speech"><span class="speaker">Player 1 <span class="as-role">(as Leading Man)</span></span>. Is he serious?',
    'looking at one another in astonishment.]</span></p>\n\n  ' +
    proj_end("THE BOY and THE CHILD leave the screen as the family exits with The Manager. The actors of the company are left alone.") +
    '\n\n  <p class="speech"><span class="speaker">Player 1 <span class="as-role">(as Leading Man)</span></span>. Is he serious?',
    1
)

# ---- ACT II projection envelope ----
# BEGIN: after "The stage call-bells ring to warn the company that the play is about to begin again."
# But the act-opener has data-opener="1" wrapping that phrase. The next paragraph starts the Step-Daughter scene.
# Locate the second stage paragraph of Act II (after "the Step-Daughter comes out..."):
html = html.replace(
    'remaining a little behind and seeming perplexed.]</span></p>\n\n  <p class="speech"><span class="speaker">The Step-Daughter</span> <span class="action">[stops, bends over the <strong>Child</strong>',
    'remaining a little behind and seeming perplexed.]</span></p>\n\n  ' +
    proj_begin("Pre-recorded footage of THE CHILD (Rosetta) and THE BOY appears on the rear screen. THE STEP-DAUGHTER kneels and speaks to the projected face of THE CHILD as if cradling her; later she handles THE BOY's pocket and discovers the revolver in the same projected image.") +
    '\n\n  <p class="speech"><span class="speaker">The Step-Daughter</span> <span class="action">[stops, bends over the <strong>Child</strong>',
    1
)

# END Act II projection: at curtain. After Manager's "I'll guarantee the first act at any rate."
html = html.replace(
    'I\'ll guarantee the first act at any rate.</p>\n\n  <div class="curtain">— End of Act II —</div>',
    'I\'ll guarantee the first act at any rate.</p>\n\n  ' +
    proj_end("THE BOY and THE CHILD fade from the screen as the curtain falls on Act II.") +
    '\n\n  <div class="curtain">— End of Act II —</div>',
    1
)

# ---- ACT III projection envelope ----
# BEGIN: after the opening Act III stage direction.
# The opening direction ends "in the act of meditating."
html = html.replace(
    'in the act of meditating.</p>\n\n  <p class="speech"><span class="speaker">The Manager</span> <span class="action">[shaking his shoulders after a brief pause]</span>. Ah yes: the second act!',
    'in the act of meditating.</p>\n\n  ' +
    proj_begin("Pre-recorded footage of THE BOY and THE CHILD returns to the rear screen. THE BOY is later shown taking position behind a tree; THE CHILD is shown drifting toward the fountain basin. The screen carries both their final actions of the play — the drowning, and the revolver — without any live actor entering the projection.") +
    '\n\n  <p class="speech"><span class="speaker">The Manager</span> <span class="action">[shaking his shoulders after a brief pause]</span>. Ah yes: the second act!',
    1
)

# END Act III projection: after the revolver shot stage direction, before Mother's cry of "My son!"
html = html.replace(
    'A revolver shot rings out behind the trees where the <strong>Boy</strong> is hidden.]</span></p>\n\n  <p class="speech"><span class="speaker">The Mother</span>',
    'A revolver shot rings out behind the trees where the <strong>Boy</strong> is hidden.]</span></p>\n\n  ' +
    proj_end("The screen cuts to black on the boy's body. What remains on stage is only the family, the company, and the Manager.") +
    '\n\n  <p class="speech"><span class="speaker">The Mother</span>',
    1
)

# ---------------------------------------------------------------------------
# 6. WRITE OUTPUT
# ---------------------------------------------------------------------------
SRC.write_text(html)
print(f"Wrote {SRC}: {len(html):,} bytes  ({html.count(chr(10)):,} lines)")
