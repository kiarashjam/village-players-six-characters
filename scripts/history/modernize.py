#!/usr/bin/env python3
"""Modernize Storer's 1922 English while preserving meaning, character voice, and
philosophical weight. Each change is a precise, meaning-preserving swap. Run
verifications after each change."""
import re
from pathlib import Path
from html import unescape

SRC = Path("/home/claude/six_characters.html")
html_in = SRC.read_text()
html = html_in

changes_log = []

def replace_safe(old, new, label, expected_count=None):
    """Replace and log. If expected_count given, must match exactly."""
    global html
    n = html.count(old)
    if expected_count is not None and n != expected_count:
        print(f"!! {label}: found {n}, expected {expected_count}")
        return False
    if n == 0:
        print(f"!! {label}: anchor not found")
        return False
    html = html.replace(old, new)
    changes_log.append((label, n))
    return True

# ===========================================================================
# TIER 1 — GLOBAL SAFE SWAPS
# Each swap preserves meaning in every context where it occurs in this file.
# ===========================================================================

# "in order to" → "to" (3 instances, all safe)
replace_safe("in order to pursue", "to pursue", "in order to → to (#1)")
replace_safe("in order to make his entrance", "to make his entrance", "in order to → to (#2)")
replace_safe("only in order to know", "only to know", "in order to → to (#3)")

# "in order that" → "so" (2 instances)
replace_safe("in order that they may appear true", "so that they appear true", "in order that #1")
replace_safe("In order that it may stand up, one has to put", "For it to stand up, you have to put", "in order that #2")

# "for which reason" → "which is why" (1 instance)
replace_safe("for which reason he is always", "which is why he is always", "for which reason")

# "as a matter of fact" → "in fact" / "actually" (5 instances)
replace_safe("As a matter of fact… we have come here", "Actually… we have come here", "AMOF→actually #1")
replace_safe("lies, as a matter of fact, all in these four children", "lies, in fact, all in these four children", "AMOF→in fact #2")
replace_safe("I have, as a matter of fact, this obligation", "I have, in fact, this obligation", "AMOF→in fact #3")
replace_safe("It will form, as a matter of fact, the nucleus", "It will form, in fact, the nucleus", "AMOF→in fact #4")
replace_safe("As a matter of fact, I was just starting to rehearse", "In fact, I was just starting to rehearse", "AMOF→in fact #5")

# "ought to" → "should" (7 instances — verb modal, always safe)
replace_safe(" ought to be here", " should be here", "ought→should (#1)")
replace_safe(" ought to turn your backs", " should turn your backs", "ought→should (#2)")
replace_safe("You ought to feel honored", "You should feel honored", "ought→should (#3)")
replace_safe("ought to have a smarter hat", "should have a smarter hat", "ought→should (#4)")
replace_safe("you ought to understand", "you should understand", "ought→should (#5)")
replace_safe("you ought to be grateful", "you should be grateful", "ought→should (#6)")
replace_safe("ought never to have", "should never have", "ought never→should never")

# "I should like to" → "I'd like to" (3 instances)
replace_safe("I should like Mr. Manager to witness", "I'd like Mr. Manager to witness", "I should like (Step-D)")
replace_safe("I should like to know who they are", "I'd like to know who they are", "I should like to (#2)")
replace_safe("I should like to request you to abandon", "I'd like to ask you to abandon", "I should like to (#3) + request→ask")
replace_safe("I should like to know if anyone has ever heard", "I'd like to know if anyone has ever heard", "I should like to (#4)")

# "I shall" → "I'll" (mostly; preserve emphatic "will" for the Son's refusal)
replace_safe("And I shall be blamed for all of it.", "And I'll be blamed for all of it.", "I shall→I'll (Manager)")
replace_safe("Yes, gentlemen, I shall be off.", "Yes, gentlemen, I'll be off.", "I shall→I'll (Step-D off)")
replace_safe("How I shall play it, how I shall live it", "How I'll play it, how I'll live it", "I shall→I'll (Step-D play)")
replace_safe("I shall live it also, you may be sure", "I'll live it too, you may be sure", "I shall→I'll (Leading Lady)")
replace_safe("I shall be upset if you don't", "I'll be upset if you don't", "I shall→I'll (Father)")
replace_safe("But I shall be, and much more effectively", "But I'll be, and much more effectively", "I shall→I'll (Leading Lady #2)")
# Son's "I shall act nothing at all" — preserve emphatic "I will" instead of "I'll"
replace_safe("I shall act nothing at all.", "I will act nothing at all.", "Son: I shall→I will (emphatic)")

# "confounded" → "damned" (3 instances, all in dialogue, all safe)
replace_safe("these confounded aspirations", "these damned aspirations", "confounded→damned #1")
replace_safe("his confounded aspirations", "his damned aspirations", "confounded→damned #2")
replace_safe("not confounded philosophy", "not damned philosophy", "confounded→damned #3")

# "incubus" → "nightmare" (1 instance — Father describes his wife)
replace_safe("She had been my incubus, but she filled my house", "She had been my nightmare, but she filled my house", "incubus→nightmare")

# ===========================================================================
# TIER 2 — TARGETED LINE-LEVEL REWRITES
# Specific awkward sentences that don't fit a pattern.
# ===========================================================================

# Step-Daughter's "I cannot see, in the least, in you" — restructure
replace_safe(
    "I was speaking of myself — whom I cannot see, in the least, in <em>you</em>.",
    "I was speaking of myself — whom I cannot see in you at all.",
    "Step-D: cannot see in the least → cannot see at all"
)

# "It is true" → "It's true" (sentence-initial, three instances all conversational)
replace_safe("</span>. It is true. It was my doing.", "</span>. It's true. It was my doing.", "It is true→It's true #1")
replace_safe("It is true she can barely write her own name", "It's true she can barely write her own name", "It is true→It's true #2")
replace_safe("because it is true! I enjoy it immensely", "because it's true! I enjoy it immensely", "It is true→It's true #3")

# Father's "I do not believe" type formality — find and modernize
# Step-Daughter "I do not blush, however" — keep, the formal "do" is emphatic ("HE does")
# Son "I do nothing!" — keep, emphatic

# Manager: "What is it then anyway?" → drop redundant "anyway"
replace_safe("What is it then anyway?", "What is it, then?", "What is it then anyway → cleaner")

# Common period filler "what say you / verily / etc." — none found

# "by way of" — none found in dialogue
# "needs must" — none found
# "wherefore" — none found

# Manager's "Eh? What is it?" — fine as is
# But there's "Eh? What is it?" — keep, theatrical

# Long sentence: "We must create credible situations, in order that they may appear true. But permit me to observe that..."
# After our in-order-that swap above, this reads: "We must create credible situations, so that they appear true. But permit me to observe that..."
# "permit me to observe" is stiff → "let me point out"
replace_safe(
    "But permit me to observe that",
    "But let me point out that",
    "permit me to observe → let me point out"
)

# "I beg you" / "I beg of you" — keep, period-flavored but understood

# ===========================================================================
# TIER 3 — VERIFY KEY PHILOSOPHICAL LINES UNCHANGED
# ===========================================================================
must_remain = [
    "Each one of us has within him a whole world of things",
    "Blind yourself, for I am blind",
    "It's taking place now",
    "Pretence? Reality, sir, reality!",
    "indissolubly bound to the chain",
    "Who was Sancho Panza? Who was Don Abbondio?",
    "I am an \"unrealised\" character",
    "Crocodile's tears, that's what it is.",
    "lost a whole day over these people",
    "Cry out as you did then!",
]
missing = [s for s in must_remain if s not in html]
if missing:
    print()
    print(f"!! WARNING — some iconic lines went missing:")
    for s in missing:
        print(f"   {s}")
else:
    print(f"\nAll {len(must_remain)} iconic lines verified present.")

# ===========================================================================
# SAVE & REPORT
# ===========================================================================
SRC.write_text(html)

n_speech = len(re.findall(r'<p class="speech">', html))
print(f"\nFile: {SRC} ({len(html):,} bytes; was {len(html_in):,} bytes; Δ {len(html)-len(html_in):+,})")
print(f"Speeches: {n_speech} (expected 634)")
print(f"\nTotal swaps applied: {sum(c for _, c in changes_log)}")
print(f"Unique change types: {len(changes_log)}")
