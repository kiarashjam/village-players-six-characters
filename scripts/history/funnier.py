#!/usr/bin/env python3
"""Make Act I funnier — punch up existing comic moments, add a handful of
new actor mutters, sharpen the Part 1 brief to commit to the comic register.
Serious beats (Mother's faint, family's pain, philosophical speeches) untouched."""
import re
from pathlib import Path

SRC = Path("/home/claude/six_characters.html")
html = SRC.read_text()

original_length = len(html)
changes = []

def replace_once(old, new, label):
    """str_replace one occurrence with logging."""
    global html
    if old not in html:
        print(f"!! ANCHOR NOT FOUND for change: {label}")
        return False
    html = html.replace(old, new, 1)
    changes.append(label)
    return True

# ===========================================================================
# PART 1 — THE REHEARSAL: punch up the comic register
# ===========================================================================

# Manager's entrance — wearier, drier
replace_once(
    'Finally, the <strong>Manager</strong> enters and goes to the table prepared for him. His <strong>Secretary</strong> brings him his mail, through which he glances.',
    'Finally, the <strong>Manager</strong> enters with the precise weariness of a man who has been managing things for too long. He goes to the table prepared for him. His <strong>Secretary</strong> brings him his mail, through which he glances with the expression of one who has never, in his life, received good news from an envelope.',
    "Manager's entrance — wearier stage direction"
)

# Manager's "I can't see" — sharper
replace_once(
    '. I can\'t see <span class="action">[To <strong>Property Man</strong>.]</span> Let\'s have a little light, please!',
    '. I can\'t see a thing in here. <span class="action">[To <strong>Property Man</strong>.]</span> A little light, please — if the theatre has any left to spare.',
    "Manager: I can't see → sharper"
)

# Manager calling rehearsal — adds a needling beat at the actors
replace_once(
    '. Come along! Come along! Second act of "Mixing It Up." <span class="action">[Sits down.]</span>',
    '. Come along! Come along! Second act of "Mixing It Up" — and try, this time, to play it as if you wanted the public to come back for the third. <span class="action">[Sits down.]</span>',
    "Manager: Come along — needling beat"
)

# Leading Man's "ridiculous" — vanity reveal
replace_once(
    '. But it\'s ridiculous!</p>',
    '. But it\'s ridiculous! I have a reputation. Or I had one, before this play.</p>',
    "Leading Man: ridiculous → vanity reveal"
)

# Manager's anti-Pirandello rant — sharpen, add royalty joke
replace_once(
    '. Ridiculous? Ridiculous? Is it my fault if France won\'t send us any more good comedies, and we are reduced to putting on Pirandello\'s works, where nobody understands anything, and where the author plays the fool with us all?',
    '. Ridiculous? Ridiculous? Is it my fault if France won\'t send us any more good comedies, and we are reduced to putting on Pirandello — Pirandello, whom nobody understands, including, I begin to suspect, Pirandello himself, and where the author plays the fool with all of us, and pockets the royalties while he does it?',
    "Manager: anti-Pirandello rant punched up"
)

# Manager's "glorious failure" — wider sweep
replace_once(
    '. Neither do I. But let\'s get on with it. It\'s sure to be a glorious failure anyway. <span class="action">[Confidentially.]</span>',
    '. Neither do I. But let\'s get on with it. It\'s sure to be a glorious failure anyway — and a glorious failure is, in this theatre, the closest thing we have to a guarantee. <span class="action">[Confidentially.]</span>',
    "Manager: glorious failure → wider sweep"
)

# Manager's face-three-quarters — adds the critics
replace_once(
    'But I say, please face three-quarters. Otherwise, what with the abstruseness of the dialogue, and the public that won\'t be able to hear you, the whole thing will go to hell. Come on! come on!',
    'But I say, please face three-quarters. Otherwise — what with the abstruseness of the dialogue, the public that won\'t be able to hear a word of it, and the critics who will hear far too much — the whole thing will go to hell. And I shall be blamed for all of it. Come on! come on!',
    "Manager: face-three-quarters expanded"
)

# Prompter's draught — make it grimmer-funny
replace_once(
    '. Pardon sir, may I get into my box? There\'s a bit of a draught.',
    '. Pardon sir, may I get into my box? There\'s a bit of a draught, and at my age, sir, that is how it begins.',
    "Prompter: draught → grimmer-funny"
)

# ===========================================================================
# PART 2 — THE PLEA: light comic touches only (no serious beats)
# ===========================================================================

# Leading Lady's barb — sharpen the working-actor sting
replace_once(
    '. Yes, for the people who like that kind of thing. <span class="action">[Casts a glance at <strong>Leading Man</strong>.]</span>',
    '. Yes, for the people who like that kind of thing. The rest of us are working actors. <span class="action">[Casts a glance at <strong>Leading Man</strong>.]</span>',
    "Leading Lady: sharper barb"
)

# ===========================================================================
# PART 3 — THE BARGAIN: punch up the Manager's professionalism + actor finale
# ===========================================================================

# Manager's "Are you amateur actors then?" — professionalism reveal
replace_once(
    '. Are you amateur actors then?</p>',
    '. Are you amateur actors then? Because we, sir, are a professional company, with a season to fill.</p>',
    "Manager: amateur actors → professional sting"
)

# Add new actor asides at end of Act I — three new mutters before exit
# Anchor: just before "Thus talking, the Actors leave the stage..."
NEW_ENDING_MUTTERS = '''<p class="speech"><span class="speaker">Player 1</span>. Well, we'll see what's going to happen next.</p>

  <p class="speech"><span class="speaker">Player 2 <span class="as-role">(as Property Man)</span></span>. First the script makes no sense, now the audience walks in off the street.</p>

  <p class="speech"><span class="speaker">Player 1 <span class="as-role">(as Door-keeper)</span></span>. I only let them in. Don't blame me.</p>

  <p class="speech"><span class="speaker">Player 3 <span class="as-role">(as Prompter)</span></span>. And I'm to take this down in shorthand, am I? — In shorthand.</p>

  <p class="stage">Thus talking,'''

OLD_ENDING = '''<p class="speech"><span class="speaker">Player 1</span>. Well, we'll see what's going to happen next.</p>

  <p class="stage">Thus talking,'''

replace_once(OLD_ENDING, NEW_ENDING_MUTTERS, "End of Act I: 3 new actor mutters")

# ===========================================================================
# PART-NOTE BRIEFS: update Part 1's "The Feeling" + add a theatre question
# ===========================================================================

# Part 1 mood — commit to comedy
OLD_MOOD = '''<h4>The Feeling</h4>
        <p>Casual, comic, slightly bored. Coffee-cup-and-paper energy. An air of well-worn complaint. The smell of a closed rehearsal room. The audience should feel they have walked in too early.</p>'''

NEW_MOOD = '''<h4>The Feeling</h4>
        <p>Comic, first and frankly. Working light, working bodies, working irritation. The Manager is exhausted; the Leading Man is vain; the company is bored. Lean into the comedy — the audience should be laughing within three minutes. The bigger the laughter we earn here, the harder the metaphysical weight will land when it comes.</p>'''

replace_once(OLD_MOOD, NEW_MOOD, "Part 1 mood — commit to comedy")

# Part 1 — add a fourth theatre question about comedy/seriousness
OLD_Q_BLOCK = '''<div class="pn-q-label">Theatre Questions</div>
      <p>What does an honest rehearsal look like to an audience that has paid to watch a play?</p>
      <p>When the Manager mocks the playwright he is forced to stage, is he a fool or the most honest theatre-maker in the room?</p>
      <p>Has the play already started — or is it still waiting for a door to open?</p>'''

NEW_Q_BLOCK = '''<div class="pn-q-label">Theatre Questions</div>
      <p>What does an honest rehearsal look like to an audience that has paid to watch a play?</p>
      <p>When the Manager mocks the playwright he is forced to stage, is he a fool or the most honest theatre-maker in the room?</p>
      <p>Has the play already started — or is it still waiting for a door to open?</p>
      <p>How funny does Act One have to be for the family's pain in Act Two to land at full weight?</p>'''

replace_once(OLD_Q_BLOCK, NEW_Q_BLOCK, "Part 1: add 4th theatre question")

# ===========================================================================
# SAVE
# ===========================================================================
SRC.write_text(html)

print(f"Original length: {original_length:,} bytes")
print(f"New length:      {len(html):,} bytes  ({'+' if len(html) > original_length else ''}{len(html)-original_length:,})")
print()
print(f"Changes applied: {len(changes)}")
for i, c in enumerate(changes, 1):
    print(f"  {i:2}. {c}")
