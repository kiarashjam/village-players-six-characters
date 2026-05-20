#!/usr/bin/env python3
"""Rebuild the projection scheme:
- Projection 1: Entrance of the Six (Act I) — silent video; ends as the Boy
  takes his place at the chair and the Child is set down as a bundle.
- Projection 2: Step-Daughter's monologue at Act II opening — the only
  projection with audible dialogue. She speaks to the Child, then finds the
  revolver in the Boy's pocket.
- Projection 3: Fountain at Act III — silent held shot, ten seconds. Kept.

Then update casting note, portraits (Boy, Child, Step-Daughter), the three
pre-act director's notes, the Foreword, and the relevant part notes."""
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
# 1. ENTRANCE PROJECTION — Act I
# ===========================================================================

# The entrance paragraph
entrance_para = """<p class="stage">At this point, the <strong>Door-keeper</strong> has entered from the stage door and advances towards the manager's table, taking off his braided cap. During this manoeuvre, the Six <strong>Characters</strong> enter, and stop by the door at back of stage, so that when the <strong>Door-keeper</strong> is about to announce their coming to the <strong>Manager</strong>, they are already on the stage. A tenuous light surrounds them, almost as if irradiated by them — the faint breath of their fantastic reality.</p>"""

# Insert BEGIN cue before this paragraph
new_block_1 = """<p class="projection-cue"><span class="proj-label">Projection begins</span>The rear wall ignites with a silent video — no dialogue. The Six are shown arriving: the Father and the Mother walking down the aisle, the Step-Daughter and the Son climbing onto the stage with them. A tenuous light surrounds them, almost as if they were lit from inside. The Boy, in the video, walks to a wooden chair at the edge of the stage and sits down; his coat is left on the chair, his cap on the seat, his satchel on the floor. The Step-Daughter, in the video, sets the Child down beside her — and as she does, the Child becomes a small wrapped bundle of white cloth. The light fades. The screen goes dark.</p>

  """ + entrance_para

replace_once(entrance_para, new_block_1, "Insert Entrance projection BEGIN")

# Find the end of the "dream lightness" paragraph and insert the END cue after it
dream_para = """<p class="stage">This light will disappear when they come forward towards the actors. They preserve, however, something of the dream lightness in which they seem almost suspended; but this does not detract from the essential reality of their forms and expressions.</p>"""

new_block_2 = dream_para + """

  <p class="projection-cue ends"><span class="proj-label">Projection ends</span>The screen is dark. The four live Characters — Father, Mother, Step-Daughter, Son — are now on the stage in flesh, having stepped out of the video as if out of a frame. The chair-and-coat is at the edge of the stage where the Boy sat down. The wrapped bundle is in the Step-Daughter's arms where the Child was set down. The tenuous light is gone. From here, the play is live."""

replace_once(dream_para, new_block_2, "Insert Entrance projection END")

# ===========================================================================
# 2. STEP-DAUGHTER PROJECTION — Act II opening
# ===========================================================================

# The full Step-Daughter speech (one paragraph)
stepd_speech = """<p class="speech"><span class="speaker">The Step-Daughter</span> <span class="action">[bends over the Child and takes her face between her hands]</span>. My little darling! You're frightened, aren't you? You don't know where we are. <span class="action">[Pretending to reply to a question of the Child.]</span> What is the stage? It's a place, baby, where people play at being serious — and we've got to act a comedy now, dead serious. You're in it too. A garden — a fountain — look — just suppose, kiddie, it's here, right in the middle. It's all pretence, my pet. All make-believe here. Better to imagine it, because if they fix it up for you, it'll only be painted cardboard — for the rockery, the water, the plants. Ah, but I think a baby like this would sooner have a make-believe fountain than a real one. What a joke it'll be for the others! But for you, alas, not such a joke. You who are real, baby dear, and really play by a real fountain, big and green and beautiful, with bamboos around and a whole lot of little ducks swimming. — <span class="action">[Seizes the Boy by the arm.]</span> What have you got there? <span class="action">[Catches the glint of a revolver.]</span> Ah! Where did you get this? Idiot! If I'd been in your place, instead of killing myself I'd have shot one of those two — or both. Father and son.</p>"""

new_block_3 = """<p class="projection-cue"><span class="proj-label">Projection begins</span><em>The only projection in the production with audible dialogue.</em> The rear wall lights up. The Step-Daughter is shown in video, kneeling, addressing the Child as a real four-year-old; partway through, she seizes the Boy by the arm — also live in the video — and finds the revolver. The bundle and the chair-and-coat remain visible on the live stage in front of the screen. Her voice plays from the speakers, not from the live Step-Daughter, who stands silent below.</p>

  """ + stepd_speech + """

  <p class="projection-cue ends"><span class="proj-label">Projection ends</span>The screen cuts to black. The Step-Daughter is once again live below it, alone with the bundle and the chair. The voice has stopped. The Boy and Child are objects on the stage again."""

replace_once(stepd_speech, new_block_3, "Insert Step-D projection around 'My little darling!' speech")

# ===========================================================================
# 3. CASTING NOTE — rewrite "One Projection — Once" section to describe THREE moments
# ===========================================================================

old_casting_projection = """    <h3>One Projection — Once</h3>
    <p>The rear wall lights up only once in the entire production: at Act Three's fountain, during the Son's narration of the drowning. For roughly ten seconds — a single held shot of the Boy by the fountain, motionless, watching — then darkness again. The revolver shot is never shown; only heard. The Boy is never shown dead. The cue <span class="cue">[Projection begins]</span> and <span class="cue">[Projection ends]</span> bracket this single moment of visibility. Before and after, the rear wall is dark; before and after, the children are objects and absence.</p>"""

new_casting_projection = """    <h3>Three Projections — Briefly</h3>
    <p>The rear wall lights up three times in the production, briefly each time. The Boy and Child are seen in the first two; the Boy alone is seen in the third. Otherwise the screen is dark and the children are objects.</p>
    <ul class="ul-hiding">
      <li><strong>The Entrance (Act One)</strong> — A silent video. The Six arrive, lit by a tenuous light. The Boy, in the video, walks to a wooden chair at the edge of the stage and sits down, leaving his coat and cap on it. The Step-Daughter sets the Child down beside her, and the Child becomes a wrapped bundle of white cloth. The light fades; the screen goes dark; from here, the play is live.</li>
      <li><strong>The Step-Daughter's monologue (Act Two opening)</strong> — The only projection with audible dialogue. The Step-Daughter is shown in video addressing the Child as a real four-year-old, then seizing the Boy and finding the revolver. The bundle and the chair-and-coat remain on the live stage, visible in front of the screen; her voice plays from the speakers, not from the live Step-Daughter, who stands silent below. When the projection ends, the Boy and Child are objects again.</li>
      <li><strong>The Fountain (Act Three)</strong> — A silent held shot, roughly ten seconds. The Boy by the fountain, motionless, watching his drowned sister. The shot is not the death; it is the act of watching. The revolver shot is heard, not seen.</li>
    </ul>
    <p>The cue <span class="cue">[Projection begins]</span> and <span class="cue">[Projection ends]</span> bracket each of these three moments. Everywhere else, the rear wall is dark and the children live in the audience's reading of a bundle and a chair.</p>"""

replace_once(old_casting_projection, new_casting_projection, "Casting note: Three Projections — Briefly")

# Also update the staging summary at the top
replace_once(
    '<strong>eight live performers, two stage objects, and one screen used exactly once</strong>',
    '<strong>eight live performers, two stage objects, and three brief projections</strong>',
    "Casting note: staging summary line"
)

# Update the subtitle on the cast list
replace_once(
    'for an eight-performer staging, two stage objects, and one projection',
    'for an eight-performer staging, two stage objects, and three brief projections',
    "Cast list subtitle"
)

# ===========================================================================
# 4. BOY PORTRAIT — mention the entrance and Act II projection moments
# ===========================================================================
old_boy = """      <p class="p-body">A silent fourteen-year-old in black — in this production, a black coat with a schoolboy's cap on a wooden chair, with a small leather satchel by the chair leg. The chair sits at the edge of the stage. The Step-Daughter <em>seizes</em> the chair, <em>pushes</em> the chair, pulls the revolver from the coat's pocket. The other Characters speak to the chair as if to him. In Act Three the chair is moved into the garden, behind a tree-flat; the gunshot is heard, not seen. The Boy is shown — projected — only once: a single held shot at the fountain, ten seconds, then darkness. The chair is everywhere else he is.</p>"""

new_boy = """      <p class="p-body">A silent fourteen-year-old in black — in this production, a black coat with a schoolboy's cap on a wooden chair, with a small leather satchel by the chair leg. The chair sits at the edge of the stage. The other Characters speak to the chair as if to him. He is shown three times in projection, briefly each time: in the entrance video at the start of Act One, walking to the chair and leaving his coat on it; in the Step-Daughter's monologue at the start of Act Two, when she seizes him and finds the revolver in his pocket; and at the fountain in Act Three, a single held shot, ten seconds, then darkness. Everywhere else, the chair is everywhere he is. In Act Three the chair is moved behind a tree-flat; the gunshot is heard, not seen.</p>"""

replace_once(old_boy, new_boy, "Boy portrait — three projection moments")

# ===========================================================================
# 5. CHILD PORTRAIT — mention the entrance and Act II projection moments
# ===========================================================================
old_child = """      <p class="p-body">A silent four-year-old in white, with a black silk sash — in this production, a small bundle of white cloth, like a swaddling, carried and kissed and set down and lifted again by the Step-Daughter and the Mother. The bundle is silent and motionless; it is moved only by other hands. The audience reads it as the Child because the Step-Daughter does. The Child is never shown on the screen. The drowning is told by the Son, the bundle is hidden by the Step-Daughter bending over the fountain, and the rest is sound and silence.</p>"""

new_child = """      <p class="p-body">A silent four-year-old in white, with a black silk sash — in this production, a small bundle of white cloth, like a swaddling, carried and kissed and set down and lifted again by the Step-Daughter and the Mother. The bundle is silent and motionless; it is moved only by other hands. The audience reads it as the bundle because the Step-Daughter does. She is shown twice in projection, briefly: in the entrance video at the start of Act One, where the Step-Daughter sets her down beside her and she becomes the bundle; and in the Step-Daughter's monologue at the start of Act Two, where she is addressed tenderly as a real child. The drowning is never shown — told by the Son, hidden by the Step-Daughter bending over the bundle at the fountain. The rest is sound and silence.</p>"""

replace_once(old_child, new_child, "Child portrait — entrance + Act II projection")

# ===========================================================================
# 6. STEP-DAUGHTER PORTRAIT — mention her video monologue
# ===========================================================================
old_stepd = """      <p class="p-body">Dashing, almost impudent, beautiful — in elegant mourning, black worn with style. Speed, shame turned outward, revenge wearing the dress of truth. She knows men look at her and uses the knowing; sex is her oldest weapon and her oldest wound, and she does not pretend either. Never apologetic — the performance is propulsion. Vulgar where vulgarity is the truth, arrogant where arrogance is armour. Her tenderness for the Child — for the bundle — must be unbearably real, so that her contempt for the Boy reads as the same wound, pointed in the opposite direction. The Father she neither pities nor forgives; she has not finished punishing him.</p>"""

new_stepd = """      <p class="p-body">Dashing, almost impudent, beautiful — in elegant mourning, black worn with style. Speed, shame turned outward, revenge wearing the dress of truth. She knows men look at her and uses the knowing; sex is her oldest weapon and her oldest wound, and she does not pretend either. Never apologetic — the performance is propulsion. Vulgar where vulgarity is the truth, arrogant where arrogance is armour. Her tenderness for the Child — for the bundle — must be unbearably real, so that her contempt for the Boy reads as the same wound, pointed in the opposite direction. She has a single projected moment in Act Two — the only audible projection in the production — where she speaks to her silent siblings as real children: tender to the Child, then violent with the Boy when she finds the revolver in his pocket. Below the screen, her live body stands silent, listening to her own recorded voice. The Father she neither pities nor forgives; she has not finished punishing him.</p>"""

replace_once(old_stepd, new_stepd, "Step-D portrait — video monologue note")

# ===========================================================================
# 7. PRE-ACT I NOTE — update for the entrance projection
# ===========================================================================
# Touch paragraph 2 (the casting compression one)
old_pre1_p2 = """They are a black coat on a chair and a wrapped bundle of white cloth, and they are heavier than children would be, because every gesture toward them lands. One stagehand has taken to calling the bundle "the baby Jesus." I have asked him to stop. He has not stopped."""

new_pre1_p2 = """They are a black coat on a chair and a wrapped bundle of white cloth, and they are heavier than children would be, because every gesture toward them lands. They appear in flesh exactly twice — both times in projection — at the entrance, when the family arrives on video and the children, in the video, become the chair and the bundle; and in Act Two, when the Step-Daughter speaks to them as real children one last time. The Boy is also shown, alone, for ten seconds at the fountain. One stagehand has taken to calling the bundle "the baby Jesus." I have asked him to stop. He has not stopped."""

replace_once(old_pre1_p2, new_pre1_p2, "Pre-Act I note: mention three projections")

# ===========================================================================
# 8. PRE-ACT II NOTE — update for the Step-D monologue projection
# ===========================================================================
old_pre2 = """The Step-Daughter is carrying her wrapped bundle and speaking to it as a sister; she handles the chair-and-coat that is her brother. (Both bundle and chair have, at this point, logged more rehearsal hours than several of my actors. They have, so far, asked for no overtime.)"""

new_pre2 = """The Step-Daughter has, just before this, finished her one projected speech of the evening — the only audible projection in the production, where she addressed her silent siblings as real children, the Child tenderly and the Boy with a revolver in her grip. She comes off that recording into the rest of the act with her bundle in her arms and her brother's chair-and-coat at the edge. (Bundle and chair have, at this point, logged more rehearsal hours than several of my actors. They have, so far, asked for no overtime.)"""

replace_once(old_pre2, new_pre2, "Pre-Act II note: Step-D's video monologue")

# ===========================================================================
# 9. PART NOTE — Act One Part II "The Plea" — mention entrance projection
# ===========================================================================
old_plea = """<p>Six figures enter through the back door, carrying a strange tenuous light. The Father asks for an author."""

new_plea = """<p>Six figures arrive — on the rear wall, in a silent video — carrying a strange tenuous light. They walk in as bodies in a frame. The Boy, in the video, sits down at a chair; the Child is set down as a bundle. The light fades. When the screen goes dark, the four live Characters — Father, Mother, Step-Daughter, Son — are on the stage in flesh, with the chair and the bundle at the edge. The Father asks for an author."""

replace_once(old_plea, new_plea, "Part Note Act I Part II: entrance via projection")

# ===========================================================================
# 10. PART NOTE — Act Two Part I "Backstage" — mention the Step-D projection
# ===========================================================================
old_backstage_what = """<p>The Step-Daughter erupts from the Manager's office with The Child and The Boy. She speaks tenderly to the Child about an imaginary garden, an imaginary fountain. She discovers the revolver in the Boy's pocket."""

new_backstage_what = """<p>The Step-Daughter erupts from the Manager's office with the bundle and the chair-and-coat. The rear wall lights up: she is shown in video speaking tenderly to the Child as a real four-year-old about an imaginary garden, an imaginary fountain; then seizing the Boy and finding the revolver in his pocket. Her voice plays from the speakers. Below the screen, her live body stands silent. When the projection ends, the bundle and the chair are once again only objects."""

replace_once(old_backstage_what, new_backstage_what, "Part Note Act II Part I: Step-D projection in What")

# ===========================================================================
# 11. FOREWORD — mention the new projection scheme
# ===========================================================================
old_foreword = """The Boy and the Child are not played by anyone — they are a coat on a chair and a wrapped bundle of cloth, and the rest of the company speaks to those objects as if to children. The rear wall of the set lights up exactly once, for about ten seconds, at the very end."""

new_foreword = """The Boy and the Child are not played by anyone — they are a coat on a chair and a wrapped bundle of cloth, and the rest of the company speaks to those objects as if to children. The rear wall of the set lights up three times, briefly: at the entrance, in silent video, where the Six arrive and the children, in the frame, become the chair and the bundle; in Act Two, when the Step-Daughter speaks to them one last time as real children (the only projection with audible voice); and at the fountain in Act Three, a held shot of the Boy that lasts ten seconds and is the play's last image."""

replace_once(old_foreword, new_foreword, "Foreword: three projection moments")

# ===========================================================================
# Save & report
# ===========================================================================
SRC.write_text(html)

# Verify
n_speech = len(re.findall(r'<p class="speech">', html))
n_proj_begin = len(re.findall(r'<p class="projection-cue">', html))
n_proj_end   = len(re.findall(r'<p class="projection-cue ends">', html))
print(f"File: {SRC} ({len(html):,} bytes; Δ {len(html)-original_len:+,})")
print(f"Speeches: {n_speech} (expected 634)")
print(f"Projection BEGINs: {n_proj_begin} (expected 3)")
print(f"Projection ENDs:   {n_proj_end}   (expected 3)")
print(f"\nChanges applied: {len(changes)}")
for c in changes:
    print(f"  – {c}")
