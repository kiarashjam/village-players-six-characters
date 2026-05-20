#!/usr/bin/env python3
"""Minimize the projection. Replace the three full-act projection envelopes
with ONE short cue at Act III's fountain climax. Everywhere else, the Boy and
Child are hidden — handled by stage objects (a small wrapped bundle for the
Child, a chair-and-coat for the Boy). Update casting note, portraits, and the
relevant part notes accordingly."""
from pathlib import Path
import re

SRC = Path("/home/claude/six_characters.html")
html = SRC.read_text()
original_len = len(html)
changes = []

def replace_once(old, new, label):
    global html
    if old not in html:
        print(f"!! MISS: {label}")
        return False
    html = html.replace(old, new, 1)
    changes.append(label)
    return True

# ===========================================================================
# 1. REMOVE all 6 existing projection cues
# ===========================================================================
projection_cues_to_remove = [
    # Act I begin
    """\n  <p class="projection-cue"><span class="proj-label">Projection begins</span>Pre-recorded footage of THE BOY (fourteen, in black) and THE CHILD (about four, in white with a black silk sash) appears on the rear screen, taking their place at the edge of the family tableau. They remain visible throughout the act, treated by the others as present in the room.</p>""",
    # Act I end
    """\n  <p class="projection-cue ends"><span class="proj-label">Projection ends</span>THE BOY and THE CHILD leave the screen as the family exits with The Manager. The actors of the company are left alone.</p>""",
    # Act II begin
    """\n  <p class="projection-cue"><span class="proj-label">Projection begins</span>Pre-recorded footage of THE CHILD (Rosetta) and THE BOY appears on the rear screen. THE STEP-DAUGHTER kneels and speaks to the projected face of THE CHILD as if cradling her; later she handles THE BOY's pocket and discovers the revolver in the same projected image.</p>""",
    # Act II end
    """\n  <p class="projection-cue ends"><span class="proj-label">Projection ends</span>THE BOY and THE CHILD fade from the screen as the curtain falls on Act II.</p>""",
    # Act III begin
    """\n  <p class="projection-cue"><span class="proj-label">Projection begins</span>Pre-recorded footage of THE BOY and THE CHILD returns to the rear screen. THE BOY is later shown taking position behind a tree; THE CHILD is shown drifting toward the fountain basin. The screen carries both their final actions of the play — the drowning, and the revolver — without any live actor entering the projection.</p>""",
    # Act III end
    """\n  <p class="projection-cue ends"><span class="proj-label">Projection ends</span>The screen cuts to black on the boy's body. What remains on stage is only the family, the company, and the Manager.</p>""",
]

for cue in projection_cues_to_remove:
    if cue in html:
        html = html.replace(cue, '', 1)
        changes.append("removed cue")
    else:
        print(f"!! cue not found: {cue[:60]}...")

# ===========================================================================
# 2. INSERT THE ONE NEW PROJECTION MOMENT — Act III fountain
# ===========================================================================
# Place it right before the Son's "I ran over to her" speech (#627),
# and end it right after the revolver-shot stage direction.

# Find the Son's narration speech and insert a BEGIN cue just before it
son_narration = '''<p class="speech"><span class="speaker">The Son</span>. I ran over to her; I was jumping in to drag her out when I saw something that froze my blood'''

new_begin_cue = '''<p class="projection-cue"><span class="proj-label">Projection begins</span>The rear wall ignites for the first and only time. For roughly ten seconds, a single held shot: THE BOY by the fountain, motionless, watching his drowned sister. No camera movement. Then darkness again.</p>

  '''

replace_once(son_narration, new_begin_cue + son_narration, "Act III: insert single projection begin (Son's narration)")

# End cue immediately after the revolver-shot stage direction
revolver_shot = '''<span class="action">[A revolver shot rings out behind the trees where the <strong>Boy</strong> is hidden.]</span>'''

new_end_cue = '''</p>

  <p class="projection-cue ends"><span class="proj-label">Projection ends</span>The screen cuts to black on the shot. The Boy is never shown dead — only the sound. What remains is the family, the company, the Manager, and what the audience has just seen for ten seconds and may not see again.</p>

  '''

# This is trickier — the shot stage direction is inside a paragraph. Let me find the paragraph it's in.
# Actually the shot ends the Son's paragraph. Let me find the close of that paragraph.

# Find the line: ...] Then... [A revolver shot rings out behind the trees where the Boy is hidden.]</p>
old_pattern = '''Then… <span class="action">[A revolver shot rings out behind the trees where the <strong>Boy</strong> is hidden.]</span></p>'''
new_pattern = '''Then… <span class="action">[A revolver shot rings out behind the trees where the <strong>Boy</strong> is hidden.]</span></p>

  <p class="projection-cue ends"><span class="proj-label">Projection ends</span>The screen cuts to black on the shot. The Boy is never shown dead — only the sound. What remains is the family, the company, the Manager, and what the audience has just seen for ten seconds and may not see again.</p>'''

replace_once(old_pattern, new_pattern, "Act III: insert single projection end (after the shot)")

# ===========================================================================
# 3. REWRITE the CASTING NOTE section about the screen
# ===========================================================================

# Replace the "One Surface in Place of Two Bodies" block
old_screen_block = '''<h3>One Surface in Place of Two Bodies</h3>
    <p>The Boy (fourteen) and the Child (about four) — the silent youngest of the Six — are not embodied by live performers. Their presence is <strong>pre-recorded video, projected onto the rear wall of the set</strong> at the moments their roles require. The other Characters look at them, speak about them, handle them: the audience sees only the screen.</p>
    <p>The cues <span class="cue">[Projection begins]</span> and <span class="cue">[Projection ends]</span> mark when the footage must run. Between cues, the screen is dark; the family addresses an absence.</p>'''

new_screen_block = '''<h3>Two Objects in Place of Two Bodies</h3>
    <p>The Boy (fourteen) and the Child (about four) — the silent youngest of the Six — are not embodied by live performers <em>and almost never appear on screen</em>. They are present, instead, as objects on the stage:</p>
    <ul class="ul-hiding">
      <li><strong>The Child</strong> is a small wrapped bundle of white cloth — a swaddling, like an infant in a blanket — which the Step-Daughter carries, kisses, sets down, lifts again. The bundle never moves on its own. The other Characters address it as if it were the Child.</li>
      <li><strong>The Boy</strong> is a black coat and a schoolboy's cap on a wooden chair, with a small leather satchel by the chair leg. The chair sits at the side of the stage and is later moved to the garden in Act Three, where it stands behind a tree-flat. Where Pirandello's text has the Step-Daughter <em>seizing</em> the Boy or <em>pushing</em> him forward, she handles the chair and the coat. Where she pulls a revolver from his pocket, she pulls it from the coat hanging on the chair.</li>
    </ul>
    <p>This is a deliberate refusal. The audience reads the children from the absences left on the stage, exactly as the family does. The bundle and the chair are heavier than performers would be — every gesture toward them lands.</p>

    <h3>One Projection — Once</h3>
    <p>The rear wall lights up only once in the entire production: at Act Three's fountain, during the Son's narration of the drowning. For roughly ten seconds — a single held shot of the Boy by the fountain, motionless, watching — then darkness again. The revolver shot is never shown; only heard. The Boy is never shown dead. The cue <span class="cue">[Projection begins]</span> and <span class="cue">[Projection ends]</span> bracket this single moment of visibility. Before and after, the rear wall is dark; before and after, the children are objects and absence.</p>'''

replace_once(old_screen_block, new_screen_block, "Casting note: rewrite screen→objects+single projection")

# Also update the casting note's preamble paragraph about "eight live performers and one screen"
replace_once(
    '<strong>eight live performers and one screen</strong>',
    '<strong>eight live performers, two stage objects, and one screen used exactly once</strong>',
    "Casting note: subtitle of the production"
)

# Update cast list silent tag for Boy and Child
replace_once(
    'The Boy<span class="silent">silent — pre-recorded projection</span>',
    'The Boy<span class="silent">silent — coat and chair</span>',
    "Cast list: Boy tag"
)
replace_once(
    'The Child<span class="silent">silent — pre-recorded projection</span>',
    'The Child<span class="silent">silent — wrapped bundle</span>',
    "Cast list: Child tag"
)

# ===========================================================================
# 4. REWRITE the BOY and CHILD portraits
# ===========================================================================

# Boy portrait: tagline and "To Play"
replace_once(
    '<span class="p-tag">silent — appears only in projection</span>',
    '<span class="p-tag">silent — a black coat on a chair</span>',
    "Boy portrait: tagline"
)
replace_once(
    'Pre-recorded footage on the rear screen. A face that says nothing and registers everything. The boy on film should never seem to be performing for an audience. He should seem to be inside a room that is slowly closing on him. Use long held shots; trust stillness.',
    'A black coat with a schoolboy\'s cap on a wooden chair, with a small leather satchel by the chair leg. The chair sits at the edge of the stage. The Step-Daughter <em>seizes</em> the chair, <em>pushes</em> the chair, pulls the revolver from the coat\'s pocket. The other Characters speak to the chair as if to him. In Act Three the chair is moved into the garden, behind a tree-flat. The Boy is shown — projected — only once: a single held shot at the fountain in Act Three, then darkness. Everywhere else, the chair is everywhere he is.',
    "Boy portrait: To Play"
)

# Child portrait: tagline and "To Play"
replace_once(
    '<span class="p-tag">silent — appears only in projection</span>',
    '<span class="p-tag">silent — a wrapped white bundle</span>',
    "Child portrait: tagline"
)
replace_once(
    'Pre-recorded footage on the rear screen. The film must never look performed. The more ordinary the child looks — playing, laughing, looking up — the more devastating her absence becomes when it is narrated by the Son who could not save her.',
    'A small bundle of white cloth — a swaddling, like an infant in a blanket — carried, kissed, set down, lifted again by the Step-Daughter and by the Mother. The bundle is silent and motionless; it is moved only by other hands. The audience reads it as the Child because the Step-Daughter does. The Child is never shown on the screen. The drowning is told by the Son, the bundle is hidden by the Step-Daughter bending over the fountain, and the rest is sound and silence.',
    "Child portrait: To Play"
)

# ===========================================================================
# 5. UPDATE THE PART NOTES that previously described the screen
# ===========================================================================

# Act I, Part 2 "The Plea" — How section mentioned screen ignition
replace_once(
    '<p>The screen ignites: pre-recorded footage of The Boy and The Child joins the family tableau at the rear of the set. The four live Characters stand on the apron in actual flesh. The actors slowly recede to the wings, becoming audience to their own stage. The lighting tightens on the family while the rehearsal room dims around them. Tones travel from comedy to interrogation.</p>',
    '<p>The four live Characters stand on the apron in actual flesh. The two silent children are present only as objects on the stage: the wrapped bundle in the Step-Daughter\'s arms, the black coat on its chair at the edge. The screen stays dark. The actors slowly recede to the wings, becoming audience to their own stage. Lighting tightens on the family while the rehearsal room dims around them. Tones travel from comedy to interrogation.</p>',
    "Part Note Act I Part 2: How — replace screen with objects"
)

# Act II, Part 1 "Backstage" — How section
replace_once(
    '<p>The act opens behind the scenes. The screen ignites again: pre-recorded footage of The Child and The Boy joins the Step-Daughter as she handles them with one hand tender and one hand hard. Then the apparatus reasserts itself — Property Man, Machinist, Prompter, the white parlour fitted up around the family\'s pain like furniture. Two registers cross each other in this part: the metaphysical (Step-Daughter and Child) and the technical (the room being built).</p>',
    '<p>The act opens behind the scenes. The Step-Daughter carries the wrapped bundle and speaks to it as if to her little sister; she handles the chair-and-coat and finds the revolver in its pocket. The screen is dark. Then the apparatus reasserts itself — Property Man, Machinist, Prompter, the white parlour fitted up around the family\'s pain like furniture. Two registers cross each other in this part: the metaphysical (Step-Daughter and the object she is loving) and the technical (the room being built).</p>',
    "Part Note Act II Part 1: How — replace screen with objects"
)

# Act II, Part 1 — Theatre Questions about screen
replace_once(
    '<p>How does a screen carry a child? What does it mean to address pre-recorded video as if it were present?</p>',
    '<p>How does a wrapped bundle carry a child? What does it mean to speak tenderly to a piece of cloth, and to a chair?</p>',
    "Part Note Act II Part 1: Question about screen"
)

# Act III, Part 2 "The Refusal" — How section mentions Boy in projection
replace_once(
    'The Boy stands behind a tree in projection, mute and waiting.',
    'The chair-and-coat — the Boy — has been moved behind a tree-flat, mute and waiting.',
    "Part Note Act III Part 2: Boy behind tree"
)

# Act III, Part 3 "The Fountain" — How section about screen
replace_once(
    'The climax is delivered as a memory, not as a scene. The Son narrates the fountain and the revolver. The screen carries the action — the drowning, the shot — and no live actor enters the violence.',
    'The climax is delivered as a memory, not as a scene. The Son narrates. The screen lights up for the first and only time in the production — a single held shot of the Boy by the fountain, motionless, ten seconds — then darkness. The drowning is hidden by the Step-Daughter bending over the bundle; the revolver shot is heard, not seen.',
    "Part Note Act III Part 3: How — single projection"
)

# ===========================================================================
# 6. ADD CSS for the new <ul class="ul-hiding"> if not already styled
# ===========================================================================
extra_css = """
.casting-note .ul-hiding { margin: 16px 0 18px; padding-left: 22px; }
.casting-note .ul-hiding li { margin-bottom: 12px; line-height: 1.65; }
"""
if ".ul-hiding" not in html:
    html = html.replace("</style>", extra_css + "</style>", 1)
    changes.append("Added ul-hiding CSS")

# ===========================================================================
# Save & report
# ===========================================================================
SRC.write_text(html)

# Verify
n_speech = len(re.findall(r'<p class="speech">', html))
n_proj_begin = len(re.findall(r'Projection begins', html))
n_proj_end   = len(re.findall(r'Projection ends',   html))

print(f"File: {SRC} ({len(html):,} bytes; Δ {len(html)-original_len:+,})")
print(f"Speeches: {n_speech}")
print(f"Projection begins mentions: {n_proj_begin}")
print(f"Projection ends mentions:   {n_proj_end}")
print(f"\nChanges applied: {len(changes)}")
for c in changes:
    print(f"  – {c}")
