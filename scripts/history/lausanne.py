#!/usr/bin/env python3
"""Relocate the production from Italy/Rome to Lausanne, Switzerland, and name
the fictional theatre company in the play 'Village Players'. The play text
(Pirandello/Storer) is unchanged; the relocation happens through the
directorial framing only."""
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
# 1. CAST LIST — rename theatre company group to Village Players
# ===========================================================================
replace_once(
    '<h3 class="cast-h3">The Theatre Company</h3>',
    '<h3 class="cast-h3">The Village Players <span class="cast-place">— Lausanne</span></h3>',
    "Cast list: theatre company → Village Players"
)

# Add minimal CSS for the place tag
new_css = """
.cast-place { font-family: 'Cormorant Infant', 'EB Garamond', serif; font-style: italic; font-weight: 400; font-size: 0.85em; opacity: 0.75; letter-spacing: 0.02em; }
"""
if ".cast-place" not in html:
    html = html.replace("</style>", new_css + "</style>", 1)
    changes.append("Added cast-place CSS")

# ===========================================================================
# 2. CASTING NOTE — insert "Where It Happens" section before A Stripped Stage
# ===========================================================================
replace_once(
    '    <h3>A Stripped Stage</h3>',
    '''    <h3>Where It Happens</h3>
    <p>The production is set in Lausanne, Switzerland — not the Rome that Pirandello half-implied in 1921, but a modern Swiss city of equal civility and equal cruelty. The theatre company on stage is the <strong>Village Players</strong>, a working repertory house in residence at Lausanne. Their season has been forced to include a play they did not choose, by a playwright they do not particularly trust. They are now in technical rehearsal for it on the morning we walk in. Six strangers will walk in too.</p>
    <p>Madame Pace's atelier — the back room where the hundred lire changed hands — sits somewhere off the rue de Bourg, in a courtyard near Saint-François. Her shop sign reads <em>robes et manteaux</em>, as Pirandello's stage directions already require. She is Italian-Swiss, an immigrant who has built a small business of dressmaking and other less nameable commerce. Her dialect mix in Storer\'s translation — half Italian, half English — remains a foreigner\'s broken speech: ridiculous, grotesque, instantly recognisable to anyone in the Lausanne audience who has been overcharged at any small shop run by a woman who knows more about them than they would like.</p>
    <p>The relocation is a directorial choice, not a textual one. Pirandello\'s dialogue is unchanged. What changes is the room the play imagines itself inside — the air outside its windows, the language overheard from the street, the city the family fled from and the city they are now trapped inside.</p>

    <h3>A Stripped Stage</h3>''',
    "Casting note: insert Where It Happens"
)

# ===========================================================================
# 3. PART NOTE 2.3 — update "1921 Rome" reference
# ===========================================================================
replace_once(
    "The lines they say are the lines they actually said, in 1921 Rome, in a back room of a real dressmaker's atelier.",
    "The lines they say are the lines they actually said, some years ago, in a back room of a real dressmaker's atelier in Lausanne.",
    "Part Note 2.3 — Lausanne replaces 1921 Rome"
)

# ===========================================================================
# 4. MADAME PACE PORTRAIT (now folded into Player 3) — add Lausanne context
# ===========================================================================
# Player 3's portrait describes Madame Pace. Add a phrase about Lausanne/immigrant.
replace_once(
    "Then comes the production's most theatrically demanding moment: Madame Pace, an apparition summoned by the very arrangement of the stage — hats on pegs, a shop window, a folding screen.",
    "Then comes the production's most theatrically demanding moment: Madame Pace, an Italian-Swiss immigrant who runs an atelier off the rue de Bourg in Lausanne, an apparition summoned by the very arrangement of the stage — hats on pegs, a shop window with the sign <em>robes et manteaux</em>, a folding screen.",
    "Player 3 portrait — Madame Pace Lausanne context"
)

# ===========================================================================
# 5. PART NOTE 2.2 — Madame Pace's atelier in Lausanne
# ===========================================================================
replace_once(
    "by the hats on the pegs, by the shop window the Property Man has set up, by the folding screen.",
    "by the hats on the pegs, by the shop window the Property Man has set up (the sign reads <em>robes et manteaux</em>), by the folding screen.",
    "Part Note 2.2 — shop window sign"
)

replace_once(
    "Player 3 enters her costume the way an apparition enters a body. She is fat, bleach-blonde, rouged.",
    "Player 3 enters her costume the way an apparition enters a body. She is fat, bleach-blonde, rouged — an Italian-Swiss woman who has lived in Lausanne long enough to half-forget her first language and never quite learn her second.",
    "Part Note 2.2 — Italian-Swiss in Lausanne"
)

# ===========================================================================
# 6. PORTRAITS-INTRO or other commentary mentioning the company generically
# ===========================================================================
# Check the casting note eyebrow text mentioning the company
replace_once(
    "Three play everyone else. The dozen lesser company roles of the original — Leading Man, Leading Lady, Juvenile",
    "Three play everyone else. The dozen lesser company roles of the Village Players — Leading Man, Leading Lady, Juvenile",
    "Casting note: 'company roles' → 'Village Players' roles"
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
