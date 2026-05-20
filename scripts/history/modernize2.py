#!/usr/bin/env python3
"""Targeted line-level modernizations. Each one preserves meaning, character voice,
and philosophical weight, but smooths Storer's 1922 stiffness."""
from pathlib import Path
import re

SRC = Path("/home/claude/six_characters.html")
html_in = SRC.read_text()
html = html_in

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
# Targeted line modernizations
# ===========================================================================

# #35 Father — paradox of stagecraft
replace_once(
    "I say that to reverse the ordinary process may well be considered a madness:",
    "I say that reversing the ordinary process may well seem like madness:",
    "#35 Father: ordinary process"
)

# #38 Manager — comedian's profession
replace_once(
    "But I would beg you to believe, my dear sir, that the profession of the comedian is a noble one.",
    "But I beg you to believe, my dear sir, that the actor's profession is a noble one.",
    "#38 Manager: comedian's profession"
)
replace_once(
    "If today, as things go, the playwrights give us stupid comedies to play and puppets to represent instead of men, remember we are proud to have given life to immortal works here on these very boards!",
    "If today's playwrights give us stupid comedies to play and puppets to represent instead of men, remember — we are proud to have given life to immortal works on these very boards!",
    "#38 Manager: today playwrights"
)

# #51 Father — disbelief
replace_once(
    "I marvel at your incredulity, gentlemen. Are you not accustomed to see the characters created by an author spring to life in yourselves and face each other?",
    "Your disbelief amazes me, gentlemen. Aren't you used to seeing the characters created by an author spring to life in yourselves and face each other?",
    "#51 Father: incredulity"
)

# #87 Father — Mother's drama
replace_once(
    "for whom she was incapable of feeling anything except possibly a little gratitude",
    "for whom she could feel nothing except, perhaps, a little gratitude",
    "#87 Father: incapable of feeling"
)

# #124 Father — mental deafness
replace_once(
    "Her mental deafness, believe me, is phenomenal, the limit:",
    "Her mental deafness, believe me, is total:",
    "#124 Father: phenomenal/the limit"
)

# #126 Father — evil from good
replace_once(
    "If we could see all the evil that may spring from good, what should we do?",
    "If we could see all the evil that can come from good, what would we do?",
    "#126 Father: evil from good"
)

# #133 Father — clerk and Mother
replace_once(
    "They understood one another, were kindred souls in fact, without, however, the least suspicion of any evil existing.",
    "They understood each other, kindred souls in fact, without the slightest suspicion of evil between them.",
    "#133 Father: kindred souls"
)

# #135 Father — mute appeal
replace_once(
    "Things had come to the point that I could not say a word to either of them without their making a mute appeal, one to the other, with their eyes.",
    "Things had reached the point where I couldn't say a word to either of them without their making a silent appeal to each other with their eyes.",
    "#135 Father: mute appeal"
)
replace_once(
    "And this, believe me, was just about enough of itself to keep me in a constant rage, to exasperate me beyond measure.",
    "And this alone, believe me, was enough to keep me in a constant rage, to exasperate me beyond measure.",
    "#135 Father: enough of itself"
)

# #146 Father — incongruity proof
replace_once(
    "Why, it is just for this very incongruity in my nature that I have had to suffer what I have.",
    "It is precisely this incongruity in my nature that has made me suffer what I have suffered.",
    "#146 Father: incongruity in my nature"
)
replace_once(
    "I could not live by the side of that woman",
    "I couldn't live beside that woman",
    "#146 Father: live by the side of"
)
replace_once(
    "any longer; but not so much for the boredom she inspired me with as for the pity I felt for her.",
    "any longer; not so much for the boredom she inspired in me, as for the pity I felt for her.",
    "#146 Father: boredom inspired with"
)

# #164 Father — minor cleanup
replace_once(
    "They came back here, unknown to me.",
    "They came back here, without my knowing.",
    "#164 Father: unknown to me"
)
replace_once(
    "but she could anyhow have got her daughter to write to me that they were in need",
    "but she could at least have had her daughter write to me that they were in need",
    "#164 Father: anyhow have got"
)

# #173 Father — sack metaphor
replace_once(
    "But a fact is like a sack which won't stand up when it is empty.",
    "A fact is like a sack — it won't stand up when it's empty.",
    "#173 Father: sack which won't"
)
replace_once(
    "I couldn't possibly know that after the death of that man, they had decided to return here, that they were in misery, and that she",
    "I couldn't possibly know that after his death they had decided to come back here, that they were in misery, and that she",
    "#173 Father: death of that man"
)

# #195 Father — aloofness
replace_once(
    "But isn't that a situation in itself? This aloofness of yours which is so cruel to me and to your mother, who returns home and sees you almost for the first time grown up, who doesn't recognize you but knows you are her son",
    "But isn't that a situation in itself? This aloofness of yours, so cruel to me and to your mother, who comes home and sees you almost for the first time as a grown man, who doesn't recognise you but knows you are her son",
    "#195 Father: aloofness"
)

# #248 Mother — insist others see
replace_once(
    "Must you then insist on others seeing it also?",
    "Must you make others see it too?",
    "#248 Mother: insist on others seeing"
)

# #289 Manager — already mostly fine, but "It makes me laugh!"
replace_once(
    "You're not going to pretend that you can act?",
    "You're not seriously going to pretend you can act?",
    "#289 Manager: pretend that you can act"
)

# #292 Father — confused
replace_once(
    "Why ever not, if it is her name?",
    "Why not, if it's her name?",
    "#292 Father: Why ever not"
)
replace_once(
    "Already, I begin to hear my own words ring false, as if they had another sound",
    "Already I begin to hear my own words ring false — as if they had a different sound",
    "#292 Father: another sound"
)

# #293 Manager — Amalia
replace_once(
    "if you want her Amalia, Amalia it shall be; and if you don't like it, we'll find another!",
    "if you want her to be Amalia, Amalia she is. If you don't like it, we'll find another!",
    "#293 Manager: Amalia it shall be"
)

# #304 Manager — soul takes shape
replace_once(
    "And my actors — I may tell you — have given expression to much more lofty material than this little drama of yours, which may or may not hold up on the stage.",
    "And my actors have given voice to material far more lofty than this little drama of yours — which may or may not hold up on the stage.",
    "#304 Manager: I may tell you/lofty"
)

# #315 Father — effect of acting
replace_once(
    "The effect will be rather — apart from the make-up — according as to how he supposes I am, as he senses me — if he does sense me — and not as I inside of myself feel myself to be.",
    "The effect will be more — apart from the make-up — how he supposes I am, how he senses me — if he senses me at all — and not how I, inside myself, feel myself to be.",
    "#315 Father: effect according as to"
)
replace_once(
    "It seems to me then that account should be taken of this by everyone whose duty it may become to criticize us",
    "So it seems to me that anyone whose job it becomes to criticise us should take this into account",
    "#315 Father: account taken"
)

# #369 Manager — comic relief
replace_once(
    "Exactly what was wanted to put a little comic relief into the crudity of the situation.",
    "Exactly what was needed to put a little comic relief into the crudity of the situation.",
    "#369 Manager: was wanted"
)

# #383 Step-Daughter — entrance
replace_once(
    "I'm here with bowed head, modest like.",
    "I'm here with my head bowed, modest-like.",
    "#383 Step-D: bowed head modest like"
)

# #388 Father — first-time entry
replace_once(
    "this is not the first time that you have come here, is it?",
    "this isn't the first time you've come here, is it?",
    "#388 Father: first time you have come"
)

# #418 Step-Daughter — burst out laughing
replace_once(
    "I should burst out laughing as I did.",
    "I would burst out laughing — exactly as I did.",
    "#418 Step-D: should burst out laughing"
)

# #525 Father — caught in a trap
replace_once(
    "And you can therefore object that it's only for a joke that that gentleman there",
    "And so you can object that it's only a joke for that gentleman there",
    "#525 Father: it's only for a joke"
)
replace_once(
    "who naturally is himself, has to be me, who am on the contrary myself — this thing you see here.",
    "who is naturally himself, to play me — who am, on the contrary, myself: this thing you see here.",
    "#525 Father: who am on the contrary"
)

# #529 Father — somebody/nobody
replace_once(
    "Because a character has really a life of his own, marked with his especial characteristics;",
    "Because a character really does have a life of his own, marked with his own particular features;",
    "#529 Father: especial characteristics"
)

# #533 Father — illusion of yesterday/tomorrow
replace_once(
    "It's only to show you that if we",
    "It's only to show you that if we",
    "#533 placeholder (no-op anchor)"
)
replace_once(
    "you too must not count overmuch on your reality as you feel it today, since, like that of yesterday, it may prove an illusion for you tomorrow.",
    "you too mustn't count too much on your reality as you feel it today — since, like yesterday's, it may turn out to be an illusion to you tomorrow.",
    "#533 Father: count overmuch"
)

# #542 Manager — philosophising
replace_once(
    "You argue and philosophize a bit too much, my dear sir.",
    "You argue and philosophise a bit too much, my dear sir.",
    "#542 Manager: philosophize spelling"
)
replace_once(
    "I think you introduced yourself to me as a — what shall we say —",
    "I think you introduced yourself to me as a — what shall we call it —",
    "#542 Manager: what shall we say"
)

# #551 Father — misfortune of characters
replace_once(
    "What is there then to marvel at in us?",
    "So what is there to wonder at in us?",
    "#551 Father: marvel at"
)
replace_once(
    "weren't right in doing what they did do and are doing now, after they have attempted everything in their power to persuade him to give them their stage life.",
    "weren't right to do what they did, and are doing now, after trying everything in their power to persuade him to give them their stage life.",
    "#551 Father: they did do"
)

# #568 Manager — combine and group up
replace_once(
    "What we've got to do is to combine and group up all the facts in one simultaneous, close-knit, action.",
    "What we've got to do is combine and group all the facts into one simultaneous, close-knit action.",
    "#568 Manager: combine and group up"
)

# #521 Father — just you think it over
replace_once(
    "Just you think it over well.",
    "Just think it over.",
    "#521 Father: just you think"
)

# ===========================================================================
# Smaller swaps still safe to make globally
# ===========================================================================

# "It cannot be helped" → "It can't be helped"
replace_once(
    "It cannot be helped,",
    "It can't be helped,",
    "It cannot be helped → can't"
)

# "I do not know what to say to you." (Father #292 area) → keep period for character
# Father can use formal "I do not" in some places — character

# Strong global: "I shall" → "I'll" for any remaining (we did the targeted ones; let's not blanket)

# "isn't it" → already fine

# ===========================================================================
# Verify iconic lines are still present
# ===========================================================================
iconic = [
    "Each one of us has within him a whole world of things",
    "Blind yourself, for I am blind",
    "It's taking place now",
    "Pretence? Reality, sir, reality!",
    "indissolubly bound to the chain",
    "Who was Sancho Panza? Who was Don Abbondio?",
    "Crocodile's tears, that's what it is",
    "lost a whole day over these people",
    "Cry out as you did then!",
    "And I came as mistress of the house",
    "what I was selling that afternoon",
    "We may be your fortune, sir — if you have the nerve for us",
    "isn't a hymn",
]
missing = [s for s in iconic if s not in html]
if missing:
    print("!! Iconic lines missing:")
    for s in missing:
        print(f"   {s}")
else:
    print(f"\nAll {len(iconic)} iconic lines verified present.")

# ===========================================================================
# Save
# ===========================================================================
SRC.write_text(html)
n_speech = len(re.findall(r'<p class="speech">', html))
print(f"\nFile: {SRC} ({len(html):,} bytes; Δ {len(html)-len(html_in):+,})")
print(f"Speeches: {n_speech} (expected 634)")
print(f"\nLine modernizations applied: {len(changes)}")
