#!/usr/bin/env python3
"""Punch the Players' dialogue with humour — dry sarcasm, theatre-insider
jokes, workplace complaint. Madame Pace's lines (Player 3 in costume) are
left alone, because she has her own specific grotesque-foreign register.
About 33 targeted punches across the three Players."""
from pathlib import Path
import re

SRC = Path("/home/claude/six_characters.html")
html = SRC.read_text()
original_len = len(html)
changes = []
misses = []

def punch(old, new, label):
    global html
    if old in html:
        html = html.replace(old, new, 1)
        changes.append(label)
        return True
    else:
        misses.append(label)
        return False

# ===========================================================================
# Player 1 — Leading Man
# ===========================================================================
punch(
    "Excuse me, but must I absolutely wear a cook's cap?",
    "Excuse me — must I really wear a cook's cap? I trained at the Conservatoire for this.",
    "LM 'cook's cap'"
)
punch(
    "I'm hanged if I do.",
    "I'd sooner resign. And I might.",
    "LM 'I'm hanged'"
)
punch(
    "One cannot let oneself be made such a fool of.",
    "One cannot allow oneself to be made a fool of — not before five o'clock, anyway.",
    "LM 'made such a fool'"
)
punch(
    "What a spectacle!",
    "What a spectacle. What an absolute treat. I shall write to my agent.",
    "LM 'what a spectacle'"
)
punch(
    "Is he serious? What the devil does he want to do?",
    "Is he serious? What does he want — improv? Devised work? I did not sign on for devised work.",
    "LM 'what the devil'"
)
punch(
    "It's absolutely unheard of. If the stage has come to this… well I'm…",
    "It's absolutely unheard of. If the stage has come to this — well, I'm going back to television. At least on television the audience cannot walk onto the set.",
    "LM 'absolutely unheard of'"
)
punch(
    "What have we to do then?",
    "What have we to do then — sit and applaud? I can do that. I've been doing that for most of this season.",
    "LM 'what have we to do'"
)
punch(
    "What's the use of us here anyway then?",
    "What is the use of us here, then? Are we props now? Have we been demoted to props?",
    "LM 'what's the use of us'"
)
punch(
    "Oh chuck it! \"Wonderful art!\" Withdraw that, please!",
    "Oh — chuck it. \"Wonderful art.\" She says it like she means it. Withdraw that, please.",
    "LM 'oh chuck it'"
)
punch(
    "Still, with a bit of go in it!",
    "Still — with a bit of go in it. Which I, of course, will provide.",
    "LM 'bit of go'"
)
punch(
    "If I've got to represent an old fellow who's coming into a house of an equivocal character…",
    "If I've got to play an old man walking into a place of, shall we say, equivocal character — and we all know what we mean — then at the very least let me find the door.",
    "LM 'equivocal house'"
)
punch(
    "Neither am I! I'm through with it!",
    "Neither am I. I am through. With this play, this company, this — actually, no, only this scene.",
    "LM 'through with it'"
)

# ===========================================================================
# Player 1 — L'Ingénue
# ===========================================================================
punch(
    "Most interesting!",
    "Most interesting. In a kind of educational way.",
    "L'Ingénue 'most interesting'"
)
punch(
    "Vanity! He fancies himself as an author now.",
    "Vanity. He thinks he's an author now. By Friday he'll think he is Pirandello.",
    "L'Ingénue 'vanity'"
)
punch(
    "They've been holding her in reserve, I guess.",
    "They've been holding her in reserve, I suppose. Saving her for the big effect.",
    "L'Ingénue 'in reserve'"
)

# ===========================================================================
# Player 1 — Door-keeper
# ===========================================================================
punch(
    "I only let them in. Don't blame me.",
    "I only let them in. Don't blame me. They had a kind of look about them. I thought they were investors.",
    "DK 'don't blame me'"
)

# ===========================================================================
# Player 1 — plain chorus
# ===========================================================================
punch(
    "Does he expect to knock up a drama in five minutes?",
    "Does he expect us to knock up a drama in five minutes? On a Tuesday?",
    "P1 'knock up a drama'"
)
punch(
    "What do you suppose? Madmen or rascals!",
    "What do you reckon? Madmen, rascals — or, more likely, both.",
    "P1 'madmen or rascals'"
)

# ===========================================================================
# Player 2 — Leading Lady
# ===========================================================================
punch(
    "Yes, for the people who like that kind of thing. The rest of us are working actors.",
    "Yes — for the kind of audience that goes in for that kind of evening. The rest of us are working actors. We have rent.",
    "LL 'people who like that kind of thing'"
)
punch(
    "If he thinks I'm going to take part in a joke like this…",
    "If he thinks I'm taking part in a joke like this — without seeing the contract first — he is gravely mistaken.",
    "LL 'joke like this'"
)
punch(
    "Nobody has ever dared to laugh at me. I insist on being treated with respect; otherwise I go away.",
    "Nobody has ever dared to laugh at me. Nobody. I insist on being treated with respect — and reasonable lighting — otherwise I go.",
    "LL 'dared to laugh at me'"
)
punch(
    "A vulgar trick!",
    "A vulgar trick. And not even a good one.",
    "LL 'vulgar trick'"
)
punch(
    "One can't hear a word.",
    "One can't hear a word. I would have preferred surtitles.",
    "LL 'can't hear a word'"
)
punch(
    "I'm not going to stop here to be made a fool of by that woman there.",
    "I am not going to stand here being made a fool of by that woman. I have been made a fool of by better.",
    "LL 'made a fool of'"
)
punch(
    "A game! We're not children here, if you please! We are serious actors.",
    "A game! For heaven's sake — we are not children. We are serious actors. With training. With agents. With opinions on Stanislavski.",
    "LL 'a game'"
)

# ===========================================================================
# Player 2 — plain
# ===========================================================================
punch(
    "I'd like to know who they are.",
    "I would like to know who they are. I would also like to know who let them in.",
    "P2 'who they are'"
)

# ===========================================================================
# Player 3 — Juvenile Lead
# ===========================================================================
punch(
    "This is rank madness.",
    "This is rank madness. Beautiful rank madness — but madness.",
    "JL 'rank madness'"
)
punch(
    "I'm out of it anyway.",
    "I'm out of it anyway. I have a thing on Tuesday.",
    "JL 'out of it'"
)
punch(
    "And he takes them seriously!",
    "And he takes them seriously! He has notes. There is — I can see from here — a notebook.",
    "JL 'takes them seriously'"
)
punch(
    "Where does she come from?",
    "Where does she come from? Wardrobe? Did anyone audition her?",
    "JL 'where does she come from'"
)

# ===========================================================================
# Player 3 — plain chorus
# ===========================================================================
punch(
    "Just listen to him!",
    "Just listen to him. Honestly — just listen.",
    "P3 'listen to him'"
)
punch(
    "It's rather a joke.",
    "It's rather a joke. It will be a much funnier joke later, I'm sure.",
    "P3 'rather a joke'"
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
if misses:
    print(f"\nMisses ({len(misses)}):")
    for m in misses:
        print(f"  !! {m}")
