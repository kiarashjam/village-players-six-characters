#!/usr/bin/env python3
"""Update the director's notes to match the current production:
- Eight performers + two stage objects + one ten-second projection
- Three Players doubling the company roles
- The committed comic register of Act One
- The modernized English
- The Step-Daughter's pushed tone
- The hiding technique for Boy and Child
- The single projection moment in Act Three"""
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
# PRE-ACT I DIRECTOR'S NOTE — major rewrite
# ===========================================================================

# Paragraph 2 — casting/performers/objects update
replace_once(
    '''<p>In this act you will see who actually "plays." The troupe — Manager, Leading Man and Lady, Juvenile Lead, the chorus of company voices, Property, Prompter, Door-keeper — are the accustomed machinery. Against them stand the Father, the Mother, the Step-Daughter, the Son, the Boy, the Child: unfinished figures who refuse to stay in the wings of someone else's convenience. I am thinking about casting not as faces but as functions: the Father as argument and wound; the Step-Daughter as speed and shame turned outward; the Mother as silence that finally screams; the Son as the one who will not grant the scene the catharsis it demands.</p>''',
    '''<p>In this version, eight bodies hold the whole company between them. Three Players move through the troupe-roles — Leading Man, Leading Lady, Juvenile Lead, Property, Prompter, Door-keeper, the chorus voices — swapping hats and tones as fast as a working theatre actually does. Against them stand the Father, the Mother, the Step-Daughter, the Son: four live presences who do not leave their bodies. The Boy and the Child do not appear at all — not as performers, and not on the screen until the very end, for ten seconds. They are a black coat on a chair and a wrapped bundle of white cloth, and they are heavier than children would be, because every gesture toward them lands. I am thinking about casting not as faces but as functions: the Father as argument and wound; the Step-Daughter as speed and shame turned outward, and the body that knows it is looked at; the Mother as silence that finally screams; the Son as the one who will not grant the scene the catharsis it demands.</p>''',
    "Pre-Act I note: paragraph 2 — casting compression + objects"
)

# Paragraph 3 — commit to the comic register
replace_once(
    '''<p>How the piece builds, for me, is cumulative irritation turned into metaphysics. First laughter, impatience, the Manager treating them as lunatics or publicity stunts — then the fainting of the Mother, the lifting of the veil, and suddenly the rehearsal is no longer a rehearsal. I am already asking where I would place bodies so that the audience feels the proscenium as a thin membrane. I want the audience to sense that every interruption — "We are rehearsing," "There is no author here" — is another nail in the coffin of the comfortable lie that theatre is only pretend.</p>''',
    '''<p>How the piece builds, for me, is comedy first — committed comedy — that turns into metaphysics. The first quarter of an hour should be funny: the Manager's exhaustion, the Leading Man's vanity, the Prompter's draught, the actors' bored professionalism. The audience laughs. Then six people walk in. The Mother lifts her veil, faints, and the temperature in the room changes. Suddenly the rehearsal is no longer a rehearsal. I am already asking where I would place bodies so that the audience feels the proscenium as a thin membrane. I want the audience to sense that every interruption — "We are rehearsing," "There is no author here" — is another nail in the coffin of the comfortable lie that theatre is only pretend. The bigger the laughter we earn in the first fifteen minutes, the harder the rest will land.</p>''',
    "Pre-Act I note: paragraph 3 — committed comedy"
)

# Paragraph 4 — language update
replace_once(
    '''<p>So Act I is groundwork and explosion at once: exposition that is also confrontation, backstory that refuses to be merely past. If I do my job, by the curtain line of the act you should not know whether you have watched a company humoring madmen or madmen exposing a company. I find that uncertainty beautiful and cruel — and I am thinking, honestly, about how much compassion to give the Manager, because he is wrong in tone so often and yet he is doing what any of us would do when the schedule is burning.</p>''',
    '''<p>So Act I is groundwork and explosion at once: exposition that is also confrontation, backstory that refuses to be merely past. The English of this version is contemporary — Storer's 1922 translation tightened for clarity but not flattened, with the long Latinate constructions broken open and the period throat-clearing cut; in the Step-Daughter's mouth, in particular, pushed harder than polite English of a hundred years ago could carry. The philosophy is preserved; what is gone is the period stiffness. If I do my job, by the curtain line of the act you should not know whether you have watched a company humouring madmen or madmen exposing a company. I find that uncertainty beautiful and cruel — and I am thinking, honestly, about how much compassion to give the Manager, because he is wrong in tone so often, and yet he is doing what any of us would do when the schedule is burning.</p>''',
    "Pre-Act I note: paragraph 4 — language update"
)

# ===========================================================================
# PRE-ACT II DIRECTOR'S NOTE — light update
# ===========================================================================
replace_once(
    '''Madame Pace arrives like a wrong note that proves the key was never stable. I keep turning over the doubling — Leading Man and Lady stepping into Father and Step-Daughter — and whether the audience should feel relief or vertigo when the "real" voices bleed through the professional ones.''',
    '''Madame Pace arrives like a wrong note that proves the key was never stable — Player 3 stepping into her costume the way an apparition steps into a body. The Step-Daughter is carrying her wrapped bundle and speaking to it as a sister; she handles the chair-and-coat that is her brother. I keep turning over the doubling — Player 1 and Player 2 stepping into Father and Step-Daughter — and whether the audience should feel relief or vertigo when the "real" voices bleed through the professional ones.''',
    "Pre-Act II note: casting + objects update"
)

replace_once(
    '''I am asking myself how much to sharpen the comedy of rehearsal against the ugliness of the shop scene without letting either cancel the other.''',
    '''I am asking how much to sharpen the comedy of rehearsal against the ugliness of the shop scene without letting either cancel the other.''',
    "Pre-Act II note: minor tightening"
)

replace_once(
    '''whether a mirror, a screen, an envelope can be innocent props.''',
    '''whether a mirror, a folding screen, an envelope can be innocent props.''',
    "Pre-Act II note: folding screen for clarity"
)

# ===========================================================================
# PRE-ACT III DIRECTOR'S NOTE — add the single projection moment
# ===========================================================================
replace_once(
    '''Act III is the garden, the refusal, the child at the fountain — the place where the Son's "I will not" collides with everyone else's hunger for a completed shape.''',
    '''Act III is the garden, the refusal, the bundle at the fountain — the place where the Son's "I will not" collides with everyone else's hunger for a completed shape.''',
    "Pre-Act III note: bundle at the fountain"
)

replace_once(
    '''I keep circling the question Pirandello forces on a director — when the drowned child is "only" theatre, why does it land like a verdict? The idea completes itself not by solving the riddle but by stripping the comfort from the word "pretence."''',
    '''I keep circling the question Pirandello forces on a director — when the drowned child is "only" theatre, why does it land like a verdict? In this version I hope it lands harder, because the audience has watched the bundle be loved for two hours and has not yet seen the face it has been loving. For ten seconds at the fountain — and only then — the screen lights: a single held shot of the Boy, motionless. Then darkness. Then the gunshot. The idea completes itself not by solving the riddle but by stripping the comfort from the word "pretence."''',
    "Pre-Act III note: single projection moment"
)

# ===========================================================================
# PART NOTE — Act One Part III (The Bargain) — add the new actor mutters
# ===========================================================================
replace_once(
    '''The Manager begins to think there is a play in this. He exits to his office with the Characters. The actors are left alone, baffled.''',
    '''The Manager begins to think there is a play in this. He exits to his office with the Characters. The Players are left on stage in a small chorus of bewilderment — the Door-keeper protesting he only let them in, the Property Man muttering that first the script made no sense and now the audience walks in off the street, the Prompter asking, in shorthand, in shorthand?''',
    "Part Note Act I Part III: new actor mutters"
)

# ===========================================================================
# Save & report
# ===========================================================================
SRC.write_text(html)

n_speech = len(re.findall(r'<p class="speech">', html))
print(f"File: {SRC} ({len(html):,} bytes; Δ {len(html)-original_len:+,})")
print(f"Speeches: {n_speech}")
print(f"\nChanges applied: {len(changes)}")
for c in changes:
    print(f"  – {c}")
