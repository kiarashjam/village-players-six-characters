#!/usr/bin/env python3
"""Final annotation sweep — sync remaining loose ends with the current play."""
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
# 1. CAST LIST subtitle — no longer "with screen"; now objects + one projection
# ===========================================================================
replace_once(
    '<p class="cast-sub">for an eight-performer staging with screen</p>',
    '<p class="cast-sub">for an eight-performer staging, two stage objects, and one projection</p>',
    "Cast list subtitle"
)

# ===========================================================================
# 2. MOTHER PORTRAIT — match the iconic line exactly to how the play reads now
# ===========================================================================
replace_once(
    "Her line in Act Two — It is taking place now. It happens all the time — should land like a stone learning to speak.",
    "Her line in Act Two — <em>It's taking place now. It happens all the time</em> — should land like a stone learning to speak.",
    "Mother portrait: italicise iconic line, match current text"
)

# ===========================================================================
# 3. MADAME PACE PORTRAIT — "by a screen" was the folding privacy screen in the
# shop; now that "screen" mostly evokes the projection wall, disambiguate.
# ===========================================================================
replace_once(
    "she is summoned into being by the very arrangement of the stage: by hats on pegs, by a shop window, by a screen.",
    "she is summoned into being by the very arrangement of the stage: by hats on pegs, by a shop window, by a folding screen.",
    "Madame Pace portrait: folding screen for clarity"
)

# ===========================================================================
# 4. APPARITION PART NOTE — same disambiguation
# ===========================================================================
replace_once(
    "A Character not in the original six is invited into being by the setting alone — by pegs, by a screen, by the magic of arranged objects.",
    "A Character not in the original six is invited into being by the setting alone — by pegs, by a folding screen, by the magic of arranged objects.",
    "Apparition part note: folding screen"
)

# ===========================================================================
# 5. STEP-DAUGHTER PORTRAIT — small refinement: her tenderness is reserved
# entirely for the Child, but the Child is now a bundle. Update so it reads
# consistently with the staging.
# ===========================================================================
replace_once(
    "Her tenderness is reserved entirely for the Child.",
    "Her tenderness is reserved entirely for the Child — for the bundle.",
    "Step-D portrait: tenderness for the bundle"
)

# ===========================================================================
# 6. SON PORTRAIT — "indissolubly bound to the chain" is in his portrait;
# good. But mention his mirror line is in Act Three Part II ("The Refusal")
# would be useful for staging. Light touch.
# (No change — current text already reads well.)

# ===========================================================================
# 7. FATHER PORTRAIT — current text reads "He believes he is reasonable.
# He is also a man who once paid a hundred lire..." — accurate. No change.

# ===========================================================================
# 8. MANAGER PORTRAIT — current text reads accurate. The Manager's exhaustion
# in the new comic opening is consistent with the portrait. No change.

# ===========================================================================
# 9. CASTING NOTE — small consistency check.
# "eight live performers, two stage objects, and one screen used exactly once"
# — already updated. Good.

# ===========================================================================
# 10. COVER — fine, no change.
# SCENE-SETTING — Pirandello's own NB, leave.
# COLOPHON — fine.

# ===========================================================================
# 11. CASTING NOTE — verify the "Madame Pace" line still says she's a Character
# embodied by Player 3, and check phrasing aligns.
# Current text: "Madame Pace, who is a Character rather than a company actor
# but who appears only briefly in Act Two by the magic of the stage, is also
# embodied by Player 3 in costume and wig." — good.

# ===========================================================================
# 12. PRE-ACT III NOTE — already says "bundle at the fountain." Good.

# ===========================================================================
# Save & report
# ===========================================================================
SRC.write_text(html)

print(f"File: {SRC} ({len(html):,} bytes; Δ {len(html)-original_len:+,})")
print(f"\nChanges applied: {len(changes)}")
for c in changes:
    print(f"  – {c}")
