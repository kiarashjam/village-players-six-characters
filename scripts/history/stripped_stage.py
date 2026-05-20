#!/usr/bin/env python3
"""Update all directorial commentary to reflect the new bold minimalist staging:
- Act One: an empty stage with a circle of chairs
- Act Two: a two-level set — upper platform is the rehearsal stage; lower floor
  is everything outside the performance (where the actors watch, where the Six
  wait, where the apparatus lives)
- Act Three: a single short fountain basin in the middle of an otherwise empty
  stage. The walls of the basin are high enough that nobody can see inside it."""
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
# 1. ADD a new "A Stripped Stage" section to the Casting Note
# ===========================================================================

# Insert before the "Three Projections — Briefly" header
old_anchor = """    <h3>Three Projections — Briefly</h3>"""
new_anchor = """    <h3>A Stripped Stage</h3>
    <p>The production refuses period-theatre clutter. Each act has a single defining visual element, and almost nothing else. The aesthetic is sculptural, not decorative. Light, levels, and one bold object per act do the rest.</p>
    <ul class="ul-hiding">
      <li><strong>Act One — Chairs.</strong> A bare stage with a circle of chairs. Working lights. No flats, no furniture, no props beyond the chairs themselves. The company sits in their chairs and performs boredom. The Manager has his own chair, set apart. When the Six arrive — first in the entrance video, then in the flesh — they too take chairs. The chair-and-coat that is the Boy is one of these chairs, at the edge. The bundle that is the Child sits in the Step-Daughter's lap.</li>
      <li><strong>Act Two — Two floors.</strong> The stage is built on two levels. The upper platform is the rehearsal stage — where the family's drama is played, where Madame Pace is summoned, where the white parlour is briefly fitted up. The lower floor is everything else: the space outside the performance, where the actors watch, where the Six wait between scenes, where the technical apparatus of the house lives. The vertical separation is the act's whole point. Performing is up. Watching is down. The line between them is the edge of the upper platform, and the play crosses it constantly.</li>
      <li><strong>Act Three — The fountain.</strong> A single short basin in the middle of an otherwise bare stage. Stone or concrete. The walls of the basin are high enough that nobody — neither audience nor live actors — can see inside it. When the Step-Daughter bends over the fountain to hide the Child, the basin itself does the hiding. The garden around it is empty. No trees, no flats, no painted cardboard. One basin, four live Characters, the chair-and-coat at the side, the empty stage.</li>
    </ul>

    <h3>Three Projections — Briefly</h3>"""

replace_once(old_anchor, new_anchor, "Casting note: insert A Stripped Stage section")

# ===========================================================================
# 2. Update staging summary line and cast list subtitle
# ===========================================================================
replace_once(
    '<strong>eight live performers, two stage objects, and three brief projections</strong>',
    '<strong>eight live performers, two stage objects, three brief projections, across three stripped, sculptural settings</strong>',
    "Casting note: staging summary line"
)
replace_once(
    'for an eight-performer staging, two stage objects, and three brief projections',
    'for an eight-performer staging across three stripped settings, with two stage objects and three brief projections',
    "Cast list subtitle"
)

# ===========================================================================
# 3. PART NOTE — Act I Part I: open with chairs
# ===========================================================================
replace_once(
    "<p>The curtain rises on an empty stage. The lights are working lights. The Manager arrives at his theatre to a half-rehearsed company.",
    "<p>The curtain rises on a bare stage with a circle of chairs and nothing else. Working lights. No furniture, no flats, no props. The Manager arrives at his theatre to a half-rehearsed company seated in those chairs in various postures of professional boredom.",
    "Part Note 1.1 — narrative para 1: chairs"
)

# ===========================================================================
# 4. PART NOTE — Act I Part II: minor — emphasise chairs only
# ===========================================================================
# The current text already mentions the Boy walking to a wooden chair. That fits.
# Add one sentence: "Everything else on stage is still only chairs."
replace_once(
    "The four live Characters — Father, Mother, Step-Daughter, Son — are now on the stage in flesh, having stepped out of the video as if out of a frame.",
    "The four live Characters — Father, Mother, Step-Daughter, Son — are now on the stage in flesh, having stepped out of the video as if out of a frame. Everything around them is still only chairs: the company in theirs, the Manager in his, the chair-and-coat at the edge.",
    "Part Note 1.2 — narrative para 1: chairs around them"
)

# ===========================================================================
# 5. PART NOTE — Act II Part I "Backstage": two-level set reveal
# ===========================================================================
replace_once(
    "<p>The act opens behind the scenes. The Step-Daughter erupts from the Manager's office with the wrapped bundle in her arms and the chair-and-coat at her side. She has just lost an argument we did not witness. The Son and Mother emerge after her, circling each other in silence and accusation. The Father follows last.</p>",
    "<p>The act opens with a transformation of the set. The bare chair-circle of Act One is gone; what is revealed is built on two levels. The upper platform is the rehearsal stage — where the family's drama will be staged. The lower floor is everything outside the performance: where the actors watch, where the Six wait between scenes, where the technical apparatus of the house lives. The Step-Daughter erupts from the lower floor onto the upper platform with the wrapped bundle in her arms and the chair-and-coat at her side. She has just lost an argument we did not witness. The Son and Mother emerge after her on the lower floor, circling each other in silence and accusation. The Father follows last.</p>",
    "Part Note 2.1 — narrative para 1: two-level reveal"
)

replace_once(
    "Then the apparatus of the theatre reasserts itself. The Property Man brings in the table. The Machinist places the pegs. The folding screen is wheeled to its position. The white parlour is fitted up around the family's pain like furniture, because that is what theatres do with grief. The Prompter is told to take shorthand. Names are assigned to the Characters by the Manager, who is acting now as a kind of stage-clerk. The Father falters at the sound of his own name.",
    "Then the apparatus of the theatre reasserts itself — all of it now on the upper platform. The Property Man carries the table up. The Machinist places the pegs. The folding screen is wheeled into position. The white parlour is fitted up on the upper level, built around the family's pain like furniture, because that is what theatres do with grief. The Prompter takes shorthand from his box on the lower floor. The Manager paces between levels as he assigns names to the Characters. The Father falters at the sound of his own name.",
    "Part Note 2.1 — narrative para 3: apparatus on upper level"
)

# ===========================================================================
# 6. PART NOTE — Act II Part II "The Apparition": upper level
# ===========================================================================
replace_once(
    "<p>The Father asks the actresses if they would mind hanging their hats and mantles on the pegs at the back of the set. They do, half-amused, not knowing why. The Father asks them to look toward the door upstage. The door opens. Madame Pace appears — though she was not in the original six, and no one called her, and no one walks through a stage door on cue. The Step-Daughter recognises her at once.</p>",
    "<p>The Father asks the actresses if they would mind hanging their hats and mantles on the pegs at the back of the upper platform. They climb up to do so, half-amused, not knowing why. The Father asks them to look toward the door upstage. The door opens. Madame Pace appears on the upper level — though she was not in the original six, and no one called her, and no one walks through a stage door on cue. The Step-Daughter, on the platform with her, recognises her at once.</p>",
    "Part Note 2.2 — narrative para 1: upper level"
)

replace_once(
    "This is the production's strangest scene. A Character not in the original cast list is summoned by the very arrangement of the stage — by the hats on the pegs, by the shop window the Property Man has set up, by the folding screen.",
    "This is the production's strangest scene, and the most architecturally bold. A Character not in the original cast list is summoned onto the upper level by the very arrangement of the stage — by the hats on the pegs, by the shop window the Property Man has set up, by the folding screen.",
    "Part Note 2.2 — narrative para 2: architecturally bold"
)

replace_once(
    "Then the Mother sees her. The Mother, who has barely spoken in this play, sees Madame Pace and erupts: <em>You old devil! You murderess!</em> The temperature in the room collapses in seconds.",
    "Then the Mother sees her, from the lower floor. The Mother, who has barely spoken in this play, looks up at the upper platform and erupts: <em>You old devil! You murderess!</em> Her voice crosses from below to above. The temperature in the room collapses in seconds.",
    "Part Note 2.2 — narrative para 3: Mother from below"
)

# ===========================================================================
# 7. PART NOTE — Act II Part III "The Substitution": two levels
# ===========================================================================
replace_once(
    "<p>The Father and the Step-Daughter play out the first beats of the shop scene themselves. The lines they say are the lines they actually said, in 1921 Rome, in a back room of a real dressmaker's atelier. The Manager listens, the actors watch, the Mother trembles in the corner. Then the Manager hands the scene to his Leading Lady and Leading Man — they will play this, properly, with stagecraft, in the version that will eventually go on. They try the same lines. The Step-Daughter laughs at them.</p>",
    "<p>The Father and the Step-Daughter play out the first beats of the shop scene themselves, on the upper platform. The lines they say are the lines they actually said, in 1921 Rome, in a back room of a real dressmaker's atelier. The Manager listens from below. The actors watch from below. The Mother trembles on the lower floor. Then the Manager hands the scene to his Leading Lady and Leading Man — they climb up to the platform, taking the place of the Characters, and try the same lines. The Step-Daughter, also up there, laughs at them.</p>",
    "Part Note 2.3 — narrative para 1: shop scene on upper level"
)

replace_once(
    "The Father objects: they are not us. The Step-Daughter is sharper — the actor will soften it, package it, make it sayable, when the whole point of what was said is that it could not be said. The Mother breaks in: <em>It's taking place now. It happens all the time.</em> She cries out as she did in life. The Machinist, by accident, drops the curtain on what was supposed to be only a rehearsal effect.",
    "The Father, on the platform, objects: they are not us. The Step-Daughter is sharper — the actor will soften it, package it, make it sayable, when the whole point of what was said is that it could not be said. The Mother, from the lower floor, breaks in: <em>It's taking place now. It happens all the time.</em> She cries out as she did in life, from below up into the rehearsal stage. The Machinist, by accident, drops the curtain on what was supposed to be only a rehearsal effect.",
    "Part Note 2.3 — narrative para 2: Mother from below"
)

# ===========================================================================
# 8. PART NOTE — Act III Part I "The Argument over Reality": fountain alone
# ===========================================================================
replace_once(
    "<p>The curtain rises on a garden set hurriedly assembled by the stagehands during the interval. A backdrop. A fountain basin. Two flat trees in the wings. The chair-and-coat — the Boy — has been moved to the edge of the garden. The bundle is in the Step-Daughter's arms.</p>",
    "<p>The curtain rises on an otherwise empty stage with a single short fountain basin in the middle. The two-level set of Act Two is gone — struck during the interval. There is no garden, no backdrop, no trees, no painted cardboard. Only the basin: stone or concrete, with walls high enough that nobody can see inside it. The chair-and-coat — the Boy — has been moved to the edge of the stage. The bundle is in the Step-Daughter's arms.</p>",
    "Part Note 3.1 — narrative para 1: fountain alone"
)

replace_once(
    "The Manager is plotting. The Step-Daughter complains that the garden cannot hold the whole drama, because the Son spends most of the action shut in his room; how can a garden contain a man who refuses to come into a garden?",
    "The Manager is plotting how to stage a tragedy on an empty stage with one prop. The Step-Daughter complains that this stripped set cannot hold the whole drama, because the Son spends most of the action shut in his room; how can an empty stage contain a man who refuses to come into it?",
    "Part Note 3.1 — narrative para 2: stripped set"
)

# ===========================================================================
# 9. PART NOTE — Act III Part II "The Refusal": chair behind fountain
# ===========================================================================
replace_once(
    "<p>The Manager tries to combine the garden scene and the indoor scene into one staged action. The Boy — the chair-and-coat — is to be moved behind a tree-flat at the back. The Child — the bundle — is to be brought down to the fountain by the Step-Daughter. The Son is to enter from the side and come down to the fountain in time to see the drowning.</p>",
    "<p>The Manager tries to combine the garden scene and the indoor scene into one staged action — though there is no garden and no indoor scene, only the fountain basin and the empty stage. The Boy — the chair-and-coat — is to be moved behind the fountain, where it will be partly hidden by the basin. The Child — the bundle — is to be brought down to the basin by the Step-Daughter. The Son is to enter from somewhere off and approach the fountain in time to see the drowning.</p>",
    "Part Note 3.2 — narrative para 1: chair behind fountain"
)

# Beats — update the tree-flat reference
replace_once(
    "The chair-and-coat is moved behind the tree-flat during this part. Stage the move with weight. The audience should notice a chair being placed.",
    "The chair-and-coat is moved behind the fountain basin during this part. Stage the move with weight. The audience should notice a chair being placed behind a basin in an empty stage.",
    "Part Note 3.2 — beats: chair behind fountain"
)

# ===========================================================================
# 10. PART NOTE — Act III Part III "The Fountain": basin hides everything
# ===========================================================================
replace_once(
    "<p>The Step-Daughter takes the bundle to the fountain. The Son finally tells what he saw on that afternoon: he ran across the garden, he jumped to drag the Child out of the water, and he was frozen by the sight of the Boy standing stock still by the side of the fountain, his eyes mad, watching his little drowned sister.</p>",
    "<p>The Step-Daughter takes the bundle to the fountain. She bends over the basin and lowers the bundle into it — but the basin's walls are high enough that nobody, neither the audience nor the live actors, can see inside it. The drowning happens in plain sight, in an unseeable space. The Son finally tells what he saw on that afternoon: he ran across the garden, he jumped to drag the Child out of the water, and he was frozen by the sight of the Boy standing stock still by the side of the fountain, his eyes mad, watching his little drowned sister.</p>",
    "Part Note 3.3 — narrative para 1: basin hides"
)

replace_once(
    "The rear wall lights up for the first and only time in the production. For roughly ten seconds, a single held shot: the Boy by the fountain, motionless, watching. No camera movement. No sound. Then darkness. From the darkness, the gunshot. The Mother cries out. The actors lift what they think is the Boy's body, which is the chair-and-coat now being treated as a body.",
    "The rear wall lights up for the first and only time in the production. For roughly ten seconds, a single held shot: the Boy by the fountain, motionless, watching. No camera movement. No sound. Then darkness. From the darkness, the gunshot — from behind the basin, where the chair-and-coat has been placed. The Mother cries out. The actors lift what they think is the Boy's body, which is the chair-and-coat now being treated as a body.",
    "Part Note 3.3 — narrative para 2: gunshot from behind basin"
)

replace_once(
    "The climax is delivered as memory, not as scene. The drowning is hidden by the Step-Daughter bending over the bundle at the fountain. The gunshot comes from behind a tree-flat. The Boy is shown — briefly, motionless, on the rear wall — only as the act of watching, not as the act of dying.",
    "The climax is delivered as memory, not as scene. The drowning is hidden by the basin itself — its walls do the work the Step-Daughter's body used to do. The gunshot comes from behind the same basin, where the chair-and-coat has been placed. The Boy is shown — briefly, motionless, on the rear wall — only as the act of watching, not as the act of dying.",
    "Part Note 3.3 — narrative para 3: basin and chair"
)

# Beats — update "the Step-Daughter at the fountain" beat
replace_once(
    "The Step-Daughter at the fountain is the play's last live image of love. She is holding a bundle and bending over a basin of nothing. Stage the action with the tenderness of the Act Two opening.",
    "The Step-Daughter at the fountain is the play's last live image of love. She is holding a bundle and bending over a basin whose interior nobody can see. Stage the action with the tenderness of the Act Two opening — and trust the basin to do the hiding for you.",
    "Part Note 3.3 — beats: trust the basin"
)

# ===========================================================================
# 11. BOY PORTRAIT — tree-flat → fountain basin
# ===========================================================================
replace_once(
    "In Act Three the chair is moved behind a tree-flat; the gunshot is heard, not seen.",
    "In Act Three the chair is moved behind the fountain basin; the gunshot is heard, not seen.",
    "Boy portrait: chair behind basin"
)

# ===========================================================================
# 12. CASTING NOTE "Two Objects" — chair location update
# ===========================================================================
replace_once(
    "The chair sits at the side of the stage and is later moved to the garden in Act Three, where it stands behind a tree-flat.",
    "The chair sits at the side of the stage and is later moved behind the fountain basin in Act Three.",
    "Casting note: chair behind basin"
)

# ===========================================================================
# 13. ACT III PART I BEATS — remove "painted cardboard / visible joins"
# ===========================================================================
replace_once(
    "The garden set must look hastily improvised. Painted cardboard. Visible joins. The Step-Daughter called it cardboard in Act Two; let it be cardboard.",
    "The stripped stage of Act Three is the most demanding visual decision. Resist the urge to dress it up. One fountain basin, four live Characters, the chair-and-coat at the side, an empty floor. Light does the rest.",
    "Part Note 3.1 — beats: stripped stage, light does the rest"
)

# ===========================================================================
# Save & report
# ===========================================================================
SRC.write_text(html)

n_speech = len(re.findall(r'<p class="speech">', html))
print(f"\nFile: {SRC} ({len(html):,} bytes; Δ {len(html)-original_len:+,})")
print(f"Speeches: {n_speech} (expected 634)")
print(f"\nChanges applied: {len(changes)}")
for c in changes:
    print(f"  – {c}")
