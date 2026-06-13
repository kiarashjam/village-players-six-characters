#!/usr/bin/env python3
"""
Purge company role-names from the play, leaving only Player 1, Player 2,
Player 3 as the company performers.

This does the mechanical bulk of the change:
  1. Restructures every group / chorus speaker tag (All Three Players,
     Two Players, The Other Players, The Manager and The Father) into
     individually attributed lines, so every line has one definite speaker.
  2. Strips the "(as Role)" parenthetical from every speaker tag.
  3. Folds the phantom crew (Stage Manager, Stage Hand, Secretary) into the
     three Players.
  4. Converts every remaining role-name reference in stage directions and
     prose to the Player who plays it.
  5. Converts the collective "Actors / Actresses" to "Players".

The descriptive prose that enumerates roles (the three Player portraits, the
cast list, the casting-note tables, and the doubling beats) is rewritten by
hand afterwards; this script only handles the referential occurrences.

Run from the repo root:  python scripts/purge_player_roles.py
"""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PLAY = HERE / "six_characters_village_players.html"

text = PLAY.read_text()


def sub_exact(old, new, required=True):
    """Replace an exact literal block; report if it is missing."""
    global text
    if old not in text:
        if required:
            print("  !! NOT FOUND:", repr(old[:70]))
        return
    text = text.replace(old, new)


# ---------------------------------------------------------------------------
# 1. Group / chorus speaker tags -> individually attributed lines.
# ---------------------------------------------------------------------------

sub_exact(
    '  <p class="speech"><span class="speaker">All Three Players</span>. Bravo! Well done! Encore!</p>',
    '  <p class="speech"><span class="speaker">Player 1</span>. Bravo!</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 2</span>. Well done!</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 3</span>. Encore!</p>',
)

sub_exact(
    '  <p class="speech"><span class="speaker">All Three Players</span>. Is it true? Has she really fainted?</p>',
    '  <p class="speech"><span class="speaker">Player 3</span>. Is it true?</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 1</span>. Has she really fainted?</p>',
)

sub_exact(
    '  <p class="speech"><span class="speaker">The Manager and The Father</span>. Yes, yes, an ordinary envelope.</p>',
    '  <p class="speech"><span class="speaker">The Manager</span>. Yes, yes.</p>\n\n'
    '  <p class="speech"><span class="speaker">The Father</span>. An ordinary envelope.</p>',
)

sub_exact(
    '  <p class="speech"><span class="speaker">All Three Players</span> <span class="action">[half surprised, half laughing, in chorus]</span>.</p>\n'
    '\n'
    '  <div class="chorus-block">\n'
    '    <span class="chorus-line">What?</span>\n'
    '    <span class="chorus-line">Why?</span>\n'
    '    <span class="chorus-line">Our hats?</span>\n'
    '    <span class="chorus-line">What does he say?</span>\n'
    '  </div>',
    '  <p class="speech"><span class="speaker">Player 1</span> <span class="action">[half surprised, half laughing]</span>. What?</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 2</span>. Why?</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 3</span>. Our hats?</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 1</span>. What does he say?</p>',
)

sub_exact(
    '  <p class="speech"><span class="speaker">All Three Players</span>.</p>\n'
    '\n'
    '  <div class="chorus-block">\n'
    '    <span class="chorus-line">Oh, what d\'you think of that?</span>\n'
    '    <span class="chorus-line">Only the mantle?</span>\n'
    '    <span class="chorus-line">He must be mad.</span>\n'
    '  </div>',
    '  <p class="speech"><span class="speaker">Player 1</span>. Oh, what d\'you think of that?</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 2</span>. Only the mantle?</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 3</span>. He must be mad.</p>',
)

sub_exact(
    '  <p class="speech"><span class="speaker">Two Players</span>.</p>\n'
    '\n'
    '  <div class="chorus-block">\n'
    '    <span class="chorus-line">But why?</span>\n'
    '    <span class="chorus-line">Mantles as well?</span>\n'
    '  </div>',
    '  <p class="speech"><span class="speaker">Player 1</span>. But why?</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 3</span>. Mantles as well?</p>',
)

sub_exact(
    '  <p class="speech"><span class="speaker">All Three Players</span> <span class="action">[taking off their hats, one or two also their cloaks, and going to hang them on the racks]</span>.</p>\n'
    '\n'
    '  <div class="chorus-block">\n'
    '    <span class="chorus-line">After all, why not?</span>\n'
    '    <span class="chorus-line">There you are!</span>\n'
    '    <span class="chorus-line">This is really funny.</span>\n'
    '    <span class="chorus-line">We\'ve got to put them on show.</span>\n'
    '  </div>',
    '  <p class="speech"><span class="speaker">Player 2</span> <span class="action">[taking off her hat and her cloak and going to hang them on the racks]</span>. After all, why not?</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 1</span>. There you are!</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 3</span>. This is really funny.</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 1</span>. We\'ve got to put them on show.</p>',
)

sub_exact(
    '  <p class="speech"><span class="speaker">Two Players</span>. He\'s dead! dead!</p>',
    '  <p class="speech"><span class="speaker">Player 1</span>. He\'s dead!</p>\n\n'
    '  <p class="speech"><span class="speaker">Player 2</span>. Dead!</p>',
)

sub_exact(
    '  <p class="speech"><span class="speaker">The Other Players</span>. No, no, it\'s only make believe, it\'s only pretence!</p>',
    '  <p class="speech"><span class="speaker">Player 3</span>. No, no, it\'s only make believe, it\'s only pretence!</p>',
)


# ---------------------------------------------------------------------------
# 2. Phantom crew (Stage Manager / Stage Hand / Secretary) -> Players.
#    Done before the generic role pass so the bold tags still match.
# ---------------------------------------------------------------------------

sub_exact(
    'He goes to the table prepared for him. His <strong>Secretary</strong> brings him his mail,',
    'He goes to the table prepared for him. <strong>Player 3</strong> brings him his mail,',
)

sub_exact(
    'first one, then another, then two together; nine or ten in all.',
    'first one, then another, then the third; three in all.',
)

sub_exact(
    '<span class="action">[The <strong>Actors</strong> and <strong>Actresses</strong> go from the front of the stage to the wings, all except the three who are to begin the rehearsal.]</span>',
    '<span class="action">[The <strong>Players</strong> take their places to begin the rehearsal.]</span>',
)

sub_exact(
    'Right — you there, machinist!',
    'Right — you there!',
)

sub_exact(
    '<span class="action">[two words; somehow still managing to deliver them as a Leading Man]</span>',
    '<span class="action">[two words, delivered with all his wounded grandeur]</span>',
)

sub_exact(
    '<span class="action">[she has been at work for an hour; the Property Man\'s bearing — shoulders forward, weight on the front foot]</span>',
    '<span class="action">[she has been at work for an hour; shoulders forward, weight on the front foot]</span>',
)

sub_exact(
    '<span class="action">[the Property Man\'s voice, flat and certain]</span>',
    '<span class="action">[her flat, certain working voice]</span>',
)

sub_exact(
    'From the dressing-rooms and the little door at the back of the stage the <strong>Actors</strong> and <strong>Stage Manager</strong> return, followed by the <strong>Property Man</strong>, and the <strong>Prompter</strong>.',
    'From the dressing-rooms and the little door at the back of the stage the <strong>Players</strong> return.',
)

sub_exact(
    'The <strong>Machinist</strong> runs off at once to prepare the scene, and arranges it while <strong>The Manager</strong> talks with the <strong>Stage Manager</strong>, the <strong>Property Man</strong>, and the <strong>Prompter</strong> on matters of detail.',
    '<strong>Player 1</strong> runs off at once to prepare the scene, and arranges it while <strong>The Manager</strong> talks with <strong>Player 2</strong> and <strong>Player 3</strong> on matters of detail.',
)

sub_exact(
    'While he is putting the things in their places, the <strong>Manager</strong> talks to the <strong>Prompter</strong> and then with the <strong>Characters</strong> and the <strong>Actors</strong>.',
    'While she is putting the things in their places, the <strong>Manager</strong> talks to <strong>Player 3</strong> and then with the <strong>Characters</strong> and the other <strong>Players</strong>.',
)

sub_exact(
    'Good! <span class="action">[Turning to a <strong>Stage Hand</strong>.]</span> Go and get some paper from my office, plenty, as much as you can find. <span class="action">[The <strong>Stage Hand</strong> goes off, and soon returns with a handful of paper which he gives to the <strong>Prompter</strong>.]</span>',
    'Good! <span class="action">[He digs a thick stack of paper out of his own table and pushes it across to <strong>Player 3</strong>.]</span> As much as you can find.',
)

sub_exact(
    'Bring that little table a bit further forward. <span class="action">[The <strong>Stage Hands</strong> obey the order. To <strong>Property Man</strong>.]</span>',
    'Bring that little table a bit further forward. <span class="action">[<strong>Player 1</strong> moves the table forward. To <strong>Player 2</strong>.]</span>',
)

sub_exact(
    'A second interruption of the action takes place when, by mistake, the stage hands let the curtain down.',
    'A second interruption of the action takes place when, by mistake, Player 1 lets the curtain down.',
)


# ---------------------------------------------------------------------------
# 3. Strip the "(as Role)" parenthetical from every speaker tag.
# ---------------------------------------------------------------------------

text, n = re.subn(r'\s*<span class="as-role">\(as [^<]*\)</span>', '', text)
print(f"  stripped {n} (as Role) speaker parentheticals")


# ---------------------------------------------------------------------------
# 4. Generic role-name -> Player, with article / possessive / <strong> forms.
# ---------------------------------------------------------------------------

ROLE_TO_PLAYER = [
    # most specific first so substrings don't collide
    ("Second Lady Lead", "Player 2"),
    ("Third Actor", "Player 1"),
    ("Fourth Actor", "Player 2"),
    ("Fifth Actor", "Player 3"),
    ("An Actor", "Player 3"),
    ("Leading Man", "Player 1"),
    ("Leading Lady", "Player 2"),
    ("Juvenile Lead", "Player 3"),
    ("L'Ingénue", "Player 1"),
    ("Door-keeper", "Player 1"),
    ("Property Man", "Player 2"),
    ("Prompter", "Player 3"),
    ("Machinist", "Player 1"),
]

for role, player in ROLE_TO_PLAYER:
    e = re.escape(role)
    # the <strong>Role</strong>  /  <strong>Role</strong>
    text = re.sub(r'(?:[Tt]he )?<strong>' + e + r'</strong>',
                  '<strong>' + player + '</strong>', text)
    # Role's  (with optional leading article/pronoun)  -> Player's
    text = re.sub(r'(?:[Tt]he |[Hh]is |[Hh]er |[Aa] )?' + e + r"'s",
                  player + "'s", text)
    # the/a/an/his/her Role -> Player
    text = re.sub(r'(?:[Tt]he |[Aa]n? |[Hh]is |[Hh]er )' + e, player, text)
    # bare Role -> Player
    text = re.sub(e, player, text)


# ---------------------------------------------------------------------------
# 5. Collective "Actors / Actresses" -> "Players".
# ---------------------------------------------------------------------------

text = text.replace('<strong>Actors</strong> and <strong>Actresses</strong>',
                    '<strong>Players</strong>')
text = re.sub(r'(?:[Ss]ome )?[Aa]ctors and [Aa]ctresses', 'the Players', text)
text = re.sub(r'[Ss]ome Actresses', 'some of the Players', text)
text = re.sub(r'[Ss]ome Actors', 'some of the Players', text)
text = text.replace('<strong>Actors</strong>', '<strong>Players</strong>')
text = text.replace('<strong>Actresses</strong>', '<strong>Players</strong>')
text = re.sub(r'\bThe Actors\b', 'The Players', text)
text = re.sub(r'\bthe Actors\b', 'the Players', text)
text = re.sub(r'\bThe Actresses\b', 'The Players', text)
text = re.sub(r'\bthe Actresses\b', 'the Players', text)
text = re.sub(r"\bActors'", "Players'", text)
text = re.sub(r'\bActors\b', 'Players', text)
text = re.sub(r'\bActresses\b', 'Players', text)


PLAY.write_text(text)
print("  wrote", PLAY.name)
