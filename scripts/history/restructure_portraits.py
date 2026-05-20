#!/usr/bin/env python3
"""Portrait restructure:
- Remove the Madame Pace portrait (her playing direction folds into Player 3)
- Renumber the Manager from viii. to vii.
- Add three new Player portraits: viii. Player 1, ix. Player 2, x. Player 3"""
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
# 1. DELETE the Madame Pace portrait (vii.)
# ===========================================================================
old_pace = """    <div class="portrait">
      <div class="p-num">vii.</div>
      <h3 class="p-name">Madame Pace</h3>
      <span class="p-tag">an apparition of the stage</span>

      <p class="p-body">An apparition — not one of the original six Characters, but summoned by the very arrangement of the stage: hats on pegs, a shop window, a folding screen. Fat, with puffy bleach-blonde hair, rouged and powdered, dressed in comical black silk with a long silver chain at her waist ending in a pair of scissors. She speaks half in Italian, half in English, ridiculous and grotesque. She must arrive like a wrong note that proves the key was never stable. Play the comedy of her dialect at full strength; play the obscenity beneath it at full strength too. The audience laughs, and is then disgusted with itself for having laughed — that double sensation is the point of her.</p>
    </div>"""

replace_once(old_pace, "", "Delete Madame Pace portrait")

# ===========================================================================
# 2. RENUMBER Manager from viii. to vii.
# ===========================================================================
replace_once(
    """    <div class="portrait">
      <div class="p-num">viii.</div>
      <h3 class="p-name">The Manager</h3>""",
    """    <div class="portrait">
      <div class="p-num">vii.</div>
      <h3 class="p-name">The Manager</h3>""",
    "Renumber Manager viii → vii"
)

# ===========================================================================
# 3. ADD three Player portraits AFTER the Manager portrait
# ===========================================================================

# The Manager portrait ends with the closing </div> of its block.
# Anchor on the Manager's closing </p>...</div> and append the Players right after.

manager_close = """He is everyone in the audience who has ever been forced to make sense of someone else's grief on a deadline.</p>
    </div>"""

player_portraits = """He is everyone in the audience who has ever been forced to make sense of someone else's grief on a deadline.</p>
    </div>

    <div class="portrait">
      <div class="p-num">viii.</div>
      <h3 class="p-name">Player 1</h3>
      <span class="p-tag">the man with all the hats</span>

      <p class="p-body">Carries the Leading Man, L'Ingénue, the Door-keeper, the Machinist, and the Third Actor — the largest collection of company roles in the production. The Leading Man's vanity is his spine in Act One: the cook's-cap argument with the Manager, the strut, the offence at being asked to wear a chef's hat in a serious play. The Door-keeper is small, apologetic, and lets the wrong six people in. The Machinist is the one who drops the curtain by mistake at the end of Act Two. Every transition between roles must be visible to the audience — the hat-toss, the change of bearing, the lift of the chin. Lean into the Leading Man early. The contrast with everything else will land harder later.</p>
    </div>

    <div class="portrait">
      <div class="p-num">ix.</div>
      <h3 class="p-name">Player 2</h3>
      <span class="p-tag">the diva and the props</span>

      <p class="p-body">Carries the Leading Lady, the Property Man, the Fourth Actor, and the Second Lady Lead. The Leading Lady is offended at being made to play the Step-Daughter, and offended again when the Step-Daughter laughs at her attempt. The Property Man is the working theatre itself — the table, the folding screen, the pegs, the patience the director has personally exhausted. Two opposite registers in the same body: the vanity that costs nothing, and the labour that costs everything. Let the audience see her flip between them in the same scene. The hat-rack and the prop trolley are both her territory.</p>
    </div>

    <div class="portrait">
      <div class="p-num">x.</div>
      <h3 class="p-name">Player 3</h3>
      <span class="p-tag">the youngest, and Madame Pace</span>

      <p class="p-body">Carries the Juvenile Lead, the Prompter, Madame Pace, An Actor, and the Fifth Actor. The Juvenile Lead is eager and slightly ridiculous. The Prompter is in his box, sometimes a court stenographer, sometimes complaining about the draught. Then comes the production's most theatrically demanding moment: Madame Pace, an apparition summoned by the very arrangement of the stage — hats on pegs, a shop window, a folding screen. Player 3 enters her costume the way an apparition enters a body — fat, bleach-blonde, rouged, dressed in comical black silk with a long silver chain at her waist ending in a pair of scissors. Half Italian, half English, ridiculous and grotesque. Play the comedy of her dialect at full strength; play the obscenity beneath it at full strength too. The audience laughs, and is then disgusted with itself for having laughed — that double sensation is the point of her.</p>
    </div>"""

replace_once(manager_close, player_portraits, "Add Player 1, 2, 3 portraits after Manager")

# ===========================================================================
# Save & report
# ===========================================================================
SRC.write_text(html)

n_portraits = len(re.findall(r'class="portrait"', html))
print(f"File: {SRC} ({len(html):,} bytes; Δ {len(html)-original_len:+,})")
print(f"Portraits now: {n_portraits} (expected 10: 6 Characters + Manager + 3 Players)")
print(f"\nChanges applied: {len(changes)}")
for c in changes:
    print(f"  – {c}")
