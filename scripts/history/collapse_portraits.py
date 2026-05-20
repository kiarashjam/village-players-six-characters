#!/usr/bin/env python3
"""Make portraits less text-heavy. Replace the three-section
Appearance/Nature/To Play structure with a single concise paragraph that
simply explains how the character should be played."""
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
# Add minimal CSS for the new <p class="p-body"> single-paragraph portraits
# ===========================================================================
new_css = """
.portrait .p-body { margin-top: 14px; line-height: 1.7; font-size: 1rem; color: var(--ink); }
"""
if ".p-body" not in html:
    html = html.replace("</style>", new_css + "</style>", 1)
    changes.append("Added p-body CSS")

# ===========================================================================
# New portrait bodies (one paragraph each)
# ===========================================================================

# === FATHER ===
old_father = """      <div class="p-block">
        <h4>Appearance</h4>
        <p>Around fifty. Reddish hair, thinned at the temples but not yet gone. A thick moustache hanging over a still-fresh mouth that smiles at strangers without quite committing to the smile. Heavy in the body, pale in the face, wide-browed. Pale blue eyes that go sharp the moment he is interrupted. Light trousers, a dark jacket — the dress of a man in the middle of his ordinary life.</p>
      </div>

      <div class="p-block">
        <h4>Nature</h4>
        <p>Alternately mellifluous and violent. The play's philosophical voice — a man who argues for his life by way of long speeches and is always slightly ashamed, afterwards, of how much of himself he has had to admit. He believes he is reasonable. He is also a man who once paid a hundred lire to a girl who turned out to be his stepdaughter, and he cannot live the rest of his life inside that single hour.</p>
      </div>

      <div class="p-block">
        <h4>To Play</h4>
        <p>He must believe, in real time, every paradox he speaks. He is not a lecturer. He is a man fighting to be allowed to exist with all of himself, not just the worst hour of his life. Mellifluous when he controls the rhythm of his argument; violent the moment that rhythm breaks.</p>
      </div>"""
new_father = """      <p class="p-body">Around fifty, heavy in body, pale-faced, with sharp blue eyes that go sharper the moment he is interrupted. The play's philosophical voice — a man arguing for his life by way of long speeches, always slightly ashamed afterwards of how much of himself he has had to admit. He must believe, in real time, every paradox he speaks. Not a lecturer; a man fighting to be allowed to exist as more than the worst hour of his life. Mellifluous when he controls the rhythm of his argument; violent the moment it breaks.</p>"""
replace_once(old_father, new_father, "Father portrait — collapsed to one paragraph")

# === MOTHER ===
old_mother = """      <div class="p-block">
        <h4>Appearance</h4>
        <p>A woman in modest black, with a heavy widow's veil of crêpe that hides her face. Beneath it, when she lifts it, a face the colour of wax. She does not meet anyone's eyes. She looks like a person who has agreed, somewhere a long time ago, to be diminished.</p>
      </div>

      <div class="p-block">
        <h4>Nature</h4>
        <p>Crushed and terrified, as though pressed down by a weight too great to name. She is silent for most of Act One; her drama is what others do to her. Then, in Act Two, her presence becomes a sound — the only true unmediated cry in the play. She is not, the Father insists, a woman. She is a mother. The whole tragedy is contained in that flattening.</p>
      </div>

      <div class="p-block">
        <h4>To Play</h4>
        <p>Stillness is her language. She listens. She suffers. She lifts the veil only when forced. Her line in Act Two — <em>It's taking place now. It happens all the time</em> — should land like a stone learning to speak. Resist the temptation to make her sympathetic in the easy way. She is heavier than that.</p>
      </div>"""
new_mother = """      <p class="p-body">A woman in modest black under a heavy widow's veil; beneath it, when she lifts it, a face the colour of wax. Crushed and terrified, as if pressed down by a weight too great to name. Silent for most of Act One — then, in Act Two, her presence becomes a sound, the only true unmediated cry in the play. Stillness is her language. Her line <em>It's taking place now. It happens all the time</em> should land like a stone learning to speak. Do not make her sympathetic in the easy way. She is heavier than that.</p>"""
replace_once(old_mother, new_mother, "Mother portrait — collapsed")

# === STEP-DAUGHTER ===
old_stepd = """      <div class="p-block">
        <h4>Appearance</h4>
        <p>Dashing, almost impudent, beautiful. In mourning, but with great elegance — black worn with style. She holds herself the way someone holds themselves who has decided not to be ashamed in public any longer.</p>
      </div>

      <div class="p-block">
        <h4>Nature</h4>
        <p>Speed, shame turned outward, revenge wearing the dress of truth. The spine of Act Two and the engine of the family's exposure. She speaks faster than the others; she refuses every softening; she enjoys the wound. Her body is part of the argument — she knows men look at her, and she uses the knowing. Her tenderness is reserved entirely for the Child — for the bundle. Her contempt for the Boy and the Son is total. The Father she neither pities nor forgives; she has not finished punishing him.</p>
      </div>

      <div class="p-block">
        <h4>To Play</h4>
        <p>Never apologetic. The performance is propulsion. Sex, scorn, and grief crossing the same face inside a few seconds. Vulgar where vulgarity is the truth, arrogant where arrogance is armour. Sex is her oldest weapon and her oldest wound — she does not pretend either. Her tenderness toward the Child must be unbearably real — so that her contempt for the Boy reads as the same wound, pointed in the opposite direction.</p>
      </div>"""
new_stepd = """      <p class="p-body">Dashing, almost impudent, beautiful — in elegant mourning, black worn with style. Speed, shame turned outward, revenge wearing the dress of truth. She knows men look at her and uses the knowing; sex is her oldest weapon and her oldest wound, and she does not pretend either. Never apologetic — the performance is propulsion. Vulgar where vulgarity is the truth, arrogant where arrogance is armour. Her tenderness for the Child — for the bundle — must be unbearably real, so that her contempt for the Boy reads as the same wound, pointed in the opposite direction. The Father she neither pities nor forgives; she has not finished punishing him.</p>"""
replace_once(old_stepd, new_stepd, "Step-Daughter portrait — collapsed")

# === SON ===
old_son = """      <div class="p-block">
        <h4>Appearance</h4>
        <p>Twenty-two. Tall. Severe in his attitude of contempt for the Father. Supercilious and indifferent to the Mother. He stands at the edge of his own family as if he had walked onto the stage against his will — which, in fact, he did.</p>
      </div>

      <div class="p-block">
        <h4>Nature</h4>
        <p>The refuser. <em>An unrealised character</em>, he calls himself — meaning he was never given dramatic life by his author and refuses to ask for it now. And yet he is on the stage, indissolubly bound to the chain. The bond is the same one that holds anyone in a family they did not choose: refusal, contempt, and the impossibility of leaving.</p>
      </div>

      <div class="p-block">
        <h4>To Play</h4>
        <p>Quiet, cold, with the energy of someone who would leave if he could. Every line is a door closing. His speech in Act Three about the mirror that throws his likeness back as a horrible grimace is the only moment he allows himself a real cry. Make it count.</p>
      </div>"""
new_son = """      <p class="p-body">Twenty-two, tall, severe — at the edge of his own family as if he had walked onto the stage against his will, which in fact he did. The refuser. He calls himself <em>an unrealised character</em>, never given dramatic life by his author and refusing to ask for it now — yet he is on the stage, indissolubly bound to the chain. Play him quiet, cold, with the energy of someone who would leave if he could. Every line is a door closing. His mirror speech in Act Three — his likeness thrown back as a horrible grimace — is the only moment he allows himself a real cry. Make it count.</p>"""
replace_once(old_son, new_son, "Son portrait — collapsed")

# === BOY ===
old_boy = """      <div class="p-block">
        <h4>Appearance</h4>
        <p>Fourteen years old, dressed in black. Wretched, half-frightened, mostly silent. He clings to his Mother. He carries a revolver in his pocket without speaking of it.</p>
      </div>

      <div class="p-block">
        <h4>Nature</h4>
        <p>The doomed witness. He sees his little sister drown in the fountain and cannot move. Then, behind the trees, he shoots himself. The audience never sees the suicide; only the sound reaches them.</p>
      </div>

      <div class="p-block">
        <h4>To Play</h4>
        <p>A black coat with a schoolboy's cap on a wooden chair, with a small leather satchel by the chair leg. The chair sits at the edge of the stage. The Step-Daughter <em>seizes</em> the chair, <em>pushes</em> the chair, pulls the revolver from the coat's pocket. The other Characters speak to the chair as if to him. In Act Three the chair is moved into the garden, behind a tree-flat. The Boy is shown — projected — only once: a single held shot at the fountain in Act Three, then darkness. Everywhere else, the chair is everywhere he is.</p>
      </div>"""
new_boy = """      <p class="p-body">A silent fourteen-year-old in black — in this production, a black coat with a schoolboy's cap on a wooden chair, with a small leather satchel by the chair leg. The chair sits at the edge of the stage. The Step-Daughter <em>seizes</em> the chair, <em>pushes</em> the chair, pulls the revolver from the coat's pocket. The other Characters speak to the chair as if to him. In Act Three the chair is moved into the garden, behind a tree-flat; the gunshot is heard, not seen. The Boy is shown — projected — only once: a single held shot at the fountain, ten seconds, then darkness. The chair is everywhere else he is.</p>"""
replace_once(old_boy, new_boy, "Boy portrait — collapsed")

# === CHILD ===
old_child = """      <div class="p-block">
        <h4>Appearance</h4>
        <p>About four years old. Dressed in white, with a black silk sash at the waist. Held, lifted, kissed, led by the hand. Easily the most fragile body in the play.</p>
      </div>

      <div class="p-block">
        <h4>Nature</h4>
        <p>The first to vanish. The Step-Daughter speaks to her about a garden that will not be real, a fountain that will only be painted cardboard. In Act Three she drowns in the fountain. Her death is the death the play refuses to show.</p>
      </div>

      <div class="p-block">
        <h4>To Play</h4>
        <p>A small bundle of white cloth — a swaddling, like an infant in a blanket — carried, kissed, set down, lifted again by the Step-Daughter and by the Mother. The bundle is silent and motionless; it is moved only by other hands. The audience reads it as the Child because the Step-Daughter does. The Child is never shown on the screen. The drowning is told by the Son, the bundle is hidden by the Step-Daughter bending over the fountain, and the rest is sound and silence.</p>
      </div>"""
new_child = """      <p class="p-body">A silent four-year-old in white, with a black silk sash — in this production, a small bundle of white cloth, like a swaddling, carried and kissed and set down and lifted again by the Step-Daughter and the Mother. The bundle is silent and motionless; it is moved only by other hands. The audience reads it as the Child because the Step-Daughter does. The Child is never shown on the screen. The drowning is told by the Son, the bundle is hidden by the Step-Daughter bending over the fountain, and the rest is sound and silence.</p>"""
replace_once(old_child, new_child, "Child portrait — collapsed")

# === MADAME PACE ===
old_pace = """      <div class="p-block">
        <h4>Appearance</h4>
        <p>A fat, older woman with puffy bleach-blonde hair. Rouged and powdered. Dressed with a comical elegance in black silk. A long silver chain at her waist, ending in a pair of scissors.</p>
      </div>

      <div class="p-block">
        <h4>Nature</h4>
        <p>An apparition. Not one of the original six Characters — she is summoned into being by the very arrangement of the stage: by hats on pegs, by a shop window, by a folding screen. She runs the atelier where the Step-Daughter was offered to the Father for a hundred lire. She speaks half in Italian and half in English, ridiculous and grotesque. She is at once a comic stage trick and the obscene heart of the family's wound.</p>
      </div>

      <div class="p-block">
        <h4>To Play</h4>
        <p>She must arrive like a wrong note that proves the key was never stable. Play the comedy of her dialect at full strength. Play the obscenity beneath the comedy at full strength too. The audience laughs, and is then disgusted with itself for having laughed — that double sensation is the point of her.</p>
      </div>"""
new_pace = """      <p class="p-body">An apparition — not one of the original six Characters, but summoned by the very arrangement of the stage: hats on pegs, a shop window, a folding screen. Fat, with puffy bleach-blonde hair, rouged and powdered, dressed in comical black silk with a long silver chain at her waist ending in a pair of scissors. She speaks half in Italian, half in English, ridiculous and grotesque. She must arrive like a wrong note that proves the key was never stable. Play the comedy of her dialect at full strength; play the obscenity beneath it at full strength too. The audience laughs, and is then disgusted with itself for having laughed — that double sensation is the point of her.</p>"""
replace_once(old_pace, new_pace, "Madame Pace portrait — collapsed")

# === MANAGER ===
old_mgr = """      <div class="p-block">
        <h4>Appearance</h4>
        <p>Pirandello does not give him a body, and the omission is itself a kind of direction. He should look like whatever the audience expects an exhausted, competent theatre director to look like — a man at the end of a difficult week, the schedule burning, faintly contemptuous of the playwright he has been forced to stage, faintly proud of his company.</p>
      </div>

      <div class="p-block">
        <h4>Nature</h4>
        <p>Pragmatic, cynical, slightly ridiculous, slightly brave. The play's director-figure. He treats the play in front of him as a job — until the job turns into something he does not have a name for. Then he tries to make a play out of it anyway, because that is what one does when six strangers walk into a rehearsal claiming there is a drama inside them.</p>
      </div>

      <div class="p-block">
        <h4>To Play</h4>
        <p>He is wrong in tone almost constantly, and right in instinct almost as often. Do not play him as a fool. Give him compassion. He is everyone in the audience who has ever been forced to make sense of someone else's grief on a deadline.</p>
      </div>"""
new_mgr = """      <p class="p-body">Whatever an exhausted, competent theatre director at the end of a difficult week looks like — the schedule burning, faintly contemptuous of the playwright he has been forced to stage, faintly proud of his company. Pragmatic, cynical, slightly ridiculous, slightly brave. He treats the play in front of him as a job, until the job turns into something he does not have a name for, and then he tries to make a play out of it anyway. He is wrong in tone almost constantly, and right in instinct almost as often. Do not play him as a fool. Give him compassion. He is everyone in the audience who has ever been forced to make sense of someone else's grief on a deadline.</p>"""
replace_once(old_mgr, new_mgr, "Manager portrait — collapsed")

# ===========================================================================
# Save & report
# ===========================================================================
SRC.write_text(html)

print(f"File: {SRC} ({len(html):,} bytes; Δ {len(html)-original_len:+,})")
print(f"\nChanges applied: {len(changes)}")
for c in changes:
    print(f"  – {c}")
