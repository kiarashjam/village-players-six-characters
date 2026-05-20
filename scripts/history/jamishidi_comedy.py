#!/usr/bin/env python3
"""Make Kiarash Jamishidi funnier across his existing notes, and add two new
Jamishidi pieces: a Foreword in the front matter and an After-the-Curtain
piece before the colophon. Keep his working-director voice — exhausted,
specific, self-deprecating, occasionally tender."""
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
# 1. PRE-ACT I — replace each paragraph with a funnier version
# ===========================================================================

# Paragraph 1
replace_once(
    """<p>I keep coming back to the door: ordinary rehearsal, ordinary irritations, then the frame cracks. Pirandello does not hand you a plot in neat acts; he hands you a mechanism — a company that believes it owns the stage until six people walk in who claim the story is already written inside them. That is the idea I am trying to hold in my head tonight: not realism versus fantasy, but two kinds of claim on the same air — the actors' professional reality and the characters' insistence that they were alive before we ever opened the book.</p>""",
    """<p>I keep coming back to the door. Pirandello does not hand you a plot in neat acts; he hands you a mechanism — a company that believes it owns the stage until six people walk in who claim the story is already written inside them. I am trying to hold this in my head tonight, between three espressos and a bill from the costume department I have not yet had the courage to open. The idea is not realism versus fantasy. It is two kinds of claim on the same air — the actors' professional reality and the Characters' insistence that they were alive before we ever opened the book. Pirandello, sitting in 1921 Rome, handed me a hundred-year-old homework assignment with no answer key. I resent him daily and call him a genius every night.</p>""",
    "Pre-Act I para 1 — comedy"
)

# Paragraph 2 — already has "eight bodies hold the whole company..." — add comedic asides
replace_once(
    """<p>In this version, eight bodies hold the whole company between them. Three Players move through the troupe-roles — Leading Man, Leading Lady, Juvenile Lead, Property, Prompter, Door-keeper, the chorus voices — swapping hats and tones as fast as a working theatre actually does. Against them stand the Father, the Mother, the Step-Daughter, the Son: four live presences who do not leave their bodies. The Boy and the Child do not appear at all — not as performers, and not on the screen until the very end, for ten seconds. They are a black coat on a chair and a wrapped bundle of white cloth, and they are heavier than children would be, because every gesture toward them lands. I am thinking about casting not as faces but as functions: the Father as argument and wound; the Step-Daughter as speed and shame turned outward, and the body that knows it is looked at; the Mother as silence that finally screams; the Son as the one who will not grant the scene the catharsis it demands.</p>""",
    """<p>In this version, eight bodies hold the whole company between them. Three Players move through the troupe-roles — Leading Man, Leading Lady, Juvenile Lead, Property, Prompter, Door-keeper, the chorus voices — swapping hats and tones as fast as a working theatre actually does. (Note to self: ask Player 1 to slow down the cap toss. Last week he hit the front row.) Against them stand the Father, the Mother, the Step-Daughter, the Son: four live presences who do not leave their bodies. The Boy and the Child do not appear at all — not as performers, and not on the screen until the very end, for ten seconds. They are a black coat on a chair and a wrapped bundle of white cloth, and they are heavier than children would be, because every gesture toward them lands. One stagehand has taken to calling the bundle "the baby Jesus." I have asked him to stop. He has not stopped. I am thinking about casting not as faces but as functions: the Father as argument and wound; the Step-Daughter as speed and shame turned outward, and the body that knows it is looked at; the Mother as silence that finally screams; the Son as the one who refuses to grant the scene the catharsis it demands. (My Son, this evening, is refusing to do the mirror speech the way I asked. He is, in this sense, the most committed actor I have ever directed.)</p>""",
    "Pre-Act I para 2 — comedy"
)

# Paragraph 3
replace_once(
    """<p>How the piece builds, for me, is comedy first — committed comedy — that turns into metaphysics. The first quarter of an hour should be funny: the Manager's exhaustion, the Leading Man's vanity, the Prompter's draught, the actors' bored professionalism. The audience laughs. Then six people walk in. The Mother lifts her veil, faints, and the temperature in the room changes. Suddenly the rehearsal is no longer a rehearsal. I am already asking where I would place bodies so that the audience feels the proscenium as a thin membrane. I want the audience to sense that every interruption — "We are rehearsing," "There is no author here" — is another nail in the coffin of the comfortable lie that theatre is only pretend. The bigger the laughter we earn in the first fifteen minutes, the harder the rest will land.</p>""",
    """<p>How the piece builds, for me, is comedy first — committed comedy — that turns into metaphysics. The first quarter of an hour should be funny: the Manager's exhaustion (which is, increasingly, my exhaustion), the Leading Man's vanity, the Prompter's draught, the actors' bored professionalism. The audience laughs. Then six people walk in. The Mother lifts her veil, faints, and the temperature in the room changes. Suddenly the rehearsal is no longer a rehearsal. I am already asking where I would place bodies so that the audience feels the proscenium as a thin membrane. I want the audience to sense that every interruption — "We are rehearsing," "There is no author here" — is another nail in the coffin of the comfortable lie that theatre is only pretend. The bigger the laughter we earn in the first fifteen minutes, the harder the rest will land. If we earn no laughter, these notes should be considered the rambling of a man who has had four espressos and no dinner.</p>""",
    "Pre-Act I para 3 — comedy"
)

# Paragraph 4
replace_once(
    """<p>So Act I is groundwork and explosion at once: exposition that is also confrontation, backstory that refuses to be merely past. The English of this version is contemporary — Storer's 1922 translation tightened for clarity but not flattened, with the long Latinate constructions broken open and the period throat-clearing cut; in the Step-Daughter's mouth, in particular, pushed harder than polite English of a hundred years ago could carry. The philosophy is preserved; what is gone is the period stiffness. If I do my job, by the curtain line of the act you should not know whether you have watched a company humouring madmen or madmen exposing a company. I find that uncertainty beautiful and cruel — and I am thinking, honestly, about how much compassion to give the Manager, because he is wrong in tone so often, and yet he is doing what any of us would do when the schedule is burning.</p>""",
    """<p>So Act I is groundwork and explosion at once: exposition that is also confrontation, backstory that refuses to be merely past. The English of this version is contemporary — Storer's 1922 translation tightened for clarity but not flattened, with the long Latinate constructions broken open and the period throat-clearing cut; in the Step-Daughter's mouth, in particular, pushed harder than polite English of a hundred years ago could carry. The philosophy is preserved; what is gone is the period stiffness. If I do my job, by the curtain line of the act you should not know whether you have watched a company humouring madmen or madmen exposing a company. I find that uncertainty beautiful and cruel — and I am thinking, honestly, about how much compassion to give the Manager, because he is wrong in tone so often, and yet he is doing what any of us would do when the schedule is burning. (The schedule, increasingly, is me. I have not yet decided whether to find this funny.)</p>""",
    "Pre-Act I para 4 — comedy"
)

# ===========================================================================
# 2. PRE-ACT II — comedy punch
# ===========================================================================
replace_once(
    """<p>Act II is where the theatre eats the story — or tries to. I am thinking about furniture, light cues, the Property Man's patience, the Prompter suddenly becoming a kind of court stenographer: the apparatus of the house asserting itself while the characters keep insisting on the exact grain of their humiliation. Madame Pace arrives like a wrong note that proves the key was never stable — Player 3 stepping into her costume the way an apparition steps into a body. The Step-Daughter is carrying her wrapped bundle and speaking to it as a sister; she handles the chair-and-coat that is her brother. I keep turning over the doubling — Player 1 and Player 2 stepping into Father and Step-Daughter — and whether the audience should feel relief or vertigo when the "real" voices bleed through the professional ones. Who plays whom here becomes almost a moral question. The company thinks they are watching; the Six think they are finally being seen. I am asking how much to sharpen the comedy of rehearsal against the ugliness of the shop scene without letting either cancel the other. The idea builds by tightening the screw: if Act I asks who has the right to speak, Act II asks who has the right to arrange the room in which the speaking happens — and whether a mirror, a folding screen, an envelope can be innocent props.</p>""",
    """<p>Act II is where the theatre eats the story — or tries to. I am thinking about furniture, light cues, the Property Man's patience (which I have personally exhausted), the Prompter suddenly becoming a kind of court stenographer: the apparatus of the house asserting itself while the Characters keep insisting on the exact grain of their humiliation. Madame Pace arrives like a wrong note that proves the key was never stable — Player 3 stepping into her costume the way an apparition steps into a body, then immediately stepping back out to ask wardrobe for a higher heel. The Step-Daughter is carrying her wrapped bundle and speaking to it as a sister; she handles the chair-and-coat that is her brother. (Both bundle and chair have, at this point, logged more rehearsal hours than several of my actors. They have, so far, asked for no overtime.) I keep turning over the doubling — Player 1 and Player 2 stepping into Father and Step-Daughter — and whether the audience should feel relief or vertigo when the "real" voices bleed through the professional ones. Who plays whom here becomes almost a moral question. The company thinks they are watching; the Six think they are finally being seen. I am asking how much to sharpen the comedy of rehearsal against the ugliness of the shop scene without letting either cancel the other. The idea builds by tightening the screw: if Act I asks who has the right to speak, Act II asks who has the right to arrange the room in which the speaking happens — and whether a mirror, a folding screen, an envelope can be innocent props. (The answer is no. Nothing on a stage is innocent. Including, on certain evenings, the espresso cups.)</p>""",
    "Pre-Act II — comedy"
)

# ===========================================================================
# 3. PRE-ACT III — comedy punch
# ===========================================================================
replace_once(
    """<p>Act III is the garden, the refusal, the bundle at the fountain — the place where the Son's "I will not" collides with everyone else's hunger for a completed shape. I am thinking about stillness as violence: how much silence the stage can hold before the audience leans forward and becomes complicit. The Manager wants a workable scene; the Father wants witness; the Step-Daughter wants revenge dressed as truth; the Mother wants an impossible repair. I keep circling the question Pirandello forces on a director — when the drowned child is "only" theatre, why does it land like a verdict? In this version I hope it lands harder, because the audience has watched the bundle be loved for two hours and has not yet seen the face it has been loving. For ten seconds at the fountain — and only then — the screen lights: a single held shot of the Boy, motionless. Then darkness. Then the gunshot.</p>""",
    """<p>Act III is the garden, the refusal, the bundle at the fountain — the place where the Son's "I will not" collides with everyone else's hunger for a completed shape. (The Son, I should note, is again refusing to do the mirror speech the way I asked. He is, in this sense, perfect for the role.) I am thinking about stillness as violence: how much silence the stage can hold before the audience leans forward and becomes complicit. The Manager wants a workable scene; the Father wants witness; the Step-Daughter wants revenge dressed as truth; the Mother wants an impossible repair. I want, by this point in the evening, all four of them to leave on time so I can go home.</p>

    <p>I keep circling the question Pirandello forces on a director — when the drowned child is "only" theatre, why does it land like a verdict? In this version I hope it lands harder, because the audience has watched the bundle be loved for two hours and has not yet seen the face it has been loving. For ten seconds at the fountain — and only then — the screen lights: a single held shot of the Boy, motionless. Then darkness. Then the gunshot.</p>""",
    "Pre-Act III — comedy + paragraph break"
)

replace_once(
    """<p>The idea completes itself not by solving the riddle but by stripping the comfort from the word "pretence." I want the final chaos to feel earned: actors who are also audience, characters who are also authors of their own agony, and me in the dark wondering which side I have been feeding all evening.</p>""",
    """<p>The idea completes itself not by solving the riddle but by stripping the comfort from the word "pretence." I want the final chaos to feel earned: actors who are also audience, Characters who are also authors of their own agony, and me in the dark wondering which side I have been feeding all evening. If you find me in the lobby afterwards, please do not ask me what it meant. I will be tired, and I will probably cry, and my publicist has asked me to stop crying in lobbies.</p>""",
    "Pre-Act III closing — comedy"
)

# ===========================================================================
# 4. NEW: DIRECTOR'S FOREWORD — insert in front matter
# ===========================================================================
foreword_html = '''
  <aside class="directors-note">
    <div class="note-eyebrow">From the Director's Notebook</div>
    <h3>Before the curtain <span class="by">— K. J., on the night</span></h3>
    <p>This is the version of Pirandello's play I would have wanted to read at twenty-three, before I knew what staging anything was actually like. It is also the version I have to live with now, because it is the one I am directing tonight. The twenty-three-year-old me thought theatre was sacred. The forty-something me has signed a contract. The two of us have been arguing for six weeks. The play in your hands is what we agreed on, more or less, around four in the morning, after the wine ran out.</p>
    <p>The plot, as Pirandello sometimes admitted under interview pressure, is a trick. Six fictional people appear in a working theatre and demand to be made into a play. The company resists. They negotiate. They fail to negotiate. By the end of the evening, two of the fictional children are dead and the company has lost a working day. That, in three sentences, is the story. The reason it has survived a hundred years and is being staged tonight in front of you is not the story. It is the question the story leaves open: <em>which of the people on the stage is real?</em></p>
    <p>For this version we have made a few decisions. There are eight live performers, not the original eleven plus extras. The Boy and the Child are not played by anyone — they are a coat on a chair and a wrapped bundle of cloth, and the rest of the company speaks to those objects as if to children. The rear wall of the set lights up exactly once, for about ten seconds, at the very end. The English has been tightened. The Step-Daughter has been allowed to be as vulgar as Pirandello's Italian always was and Storer's 1922 translation never quite let her be. The first fifteen minutes are comedy. The last fifteen minutes are not. The Manager — Pirandello's harried theatre director, who is also, increasingly, me — is in the play because every working theatre-maker is somewhere inside him.</p>
    <p>I am writing these notes from a small office at the back of the theatre, where the espresso machine and I have an understanding I would prefer not to describe. If you are reading them in the programme, I have either trusted them or run out of time to change them. Either reading is correct. Whatever happens in the next two hours, please remember: nobody on the stage <em>chose</em> any of this. Including, on bad nights, me. Have a good night.</p>
  </aside>
'''

# Insert AFTER the preface end and BEFORE the casting note
replace_once(
    '</section><!-- preface end -->\n\n  <section class="casting-note">',
    '</section><!-- preface end -->\n' + foreword_html + '\n  <section class="casting-note">',
    "Insert NEW Foreword in front matter"
)

# ===========================================================================
# 5. NEW: AFTER THE CURTAIN — insert after Act III closes, before colophon
# ===========================================================================
afterword_html = '''
  <aside class="directors-note">
    <div class="note-eyebrow">From the Director's Notebook</div>
    <h3>After the curtain <span class="by">— K. J., afterwards</span></h3>
    <p>If all has gone according to plan, you have just watched a comedy that turned into a tragedy that turned into an argument. The Father said <em>Reality!</em> The Manager said <em>Pretence!</em> The play declined to declare a winner. I have a few things to say about that — partly to you, partly to myself, partly to the espresso machine which has, by now, earned a credit in the programme.</p>
    <p>First, the gunshot. We tried it three different ways and the version you heard tonight is the one that did not blow out the speakers. If it startled you, our apologies; if it did not startle you, our apologies in a different direction. The sound designer would like it known that the original plan was louder.</p>
    <p>Second, the bundle. I have lost count of the times in rehearsal I have spoken about the bundle as if it were a four-year-old child. The Step-Daughter has stopped correcting me. The bundle now has a name in our private working language — <em>Rosetta</em>, after the Child she plays — and I no longer find this strange, which is, I suppose, exactly what Pirandello was trying to demonstrate. The audience was supposed to be the one fooled into believing in the prop, not the company. I am at peace with our failure. So is Rosetta.</p>
    <p>Third, the Manager. I have done my best not to play him as a fool, though there are evenings when I, as a director, do not deserve the compassion I asked the actor to give him. He is the audience proxy. He is everyone in any room who has been forced to make sense of someone else's grief on a deadline. He is also a coward, and he is also a working theatre-maker, and these are not contradictions; they are the working conditions.</p>
    <p>Fourth, Pirandello. You will have heard, in the Manager's first long rant, a joke about Pirandello himself — about an author whom nobody understands, including, the Manager suspects, Pirandello himself, who pockets the royalties while he does it. That joke is mine, not Pirandello's. I owe him an apology if he ever comes back to claim it. So far, he has not.</p>
    <p>Thank you for staying. Please walk home carefully. The make-believe debate that ended the play is still going on somewhere out there, even after the lights come up. I find that beautiful and cruel — and yes, I have been asked to stop saying that, but as long as it remains true, I will not.</p>
  </aside>
'''

# Insert AFTER act-3 closes and BEFORE the colophon
replace_once(
    '</article>\n\n  <footer class="colophon">',
    '</article>\n' + afterword_html + '\n  <footer class="colophon">',
    "Insert NEW After-the-Curtain note before colophon"
)

# ===========================================================================
# Save & report
# ===========================================================================
SRC.write_text(html)

# Verify
n_speech = len(re.findall(r'<p class="speech">', html))
n_directors_notes = len(re.findall(r'class="directors-note"', html))
print(f"File: {SRC} ({len(html):,} bytes; Δ {len(html)-original_len:+,})")
print(f"Speeches: {n_speech} (expected 634)")
print(f"Director's notes: {n_directors_notes} (expected 5 — was 3, plus 2 new)")
print(f"\nChanges applied: {len(changes)}")
for c in changes:
    print(f"  – {c}")
