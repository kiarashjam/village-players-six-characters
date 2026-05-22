#!/usr/bin/env python3
"""Build the Actor Rehearsal Script from the Director's Copy.

Strips: character portraits, casting/production note, all part-note
asides (narrative prose, stats, beats), and the reader-UI controls.

Keeps: cover (relabelled "Rehearsal Script"), the cast list, the
scene-setting line, a single one-paragraph note on this production's
two stage objects, and the full play text — every speech, every stage
direction, every projection cue, every act header, every curtain.
"""
import os
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

HERE = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("PLAY_SRC", HERE / "six_characters_village_players.html"))
OUT = Path(os.environ.get("ACTOR_OUT", HERE / "six_characters_actor_script.html"))


# ---------------------------------------------------------------------------
# Replacement cover and minimal production note
# ---------------------------------------------------------------------------

NEW_COVER_INNER = """
    <div class="eyebrow">Actor Rehearsal Script</div>

    <div class="cover-title-block">
      <h1 class="cover-title">Six Characters<br>in Search of an Author</h1>
      <p class="cover-italian">Sei personaggi in cerca d'autore</p>
    </div>

    <div class="ornament">· · ·</div>
    <div class="subtitle">A Comedy in the Making</div>

    <div class="director-credit">
      <p>Luigi Pirandello &nbsp;·&nbsp; trans. Edward Storer (1922)</p>
      <p>Rewritten and directed by <strong>Kiarash Jamshidi</strong></p>
      <p>Village Players, Lausanne</p>
    </div>

    <p class="cast-sub" style="margin-top:32px;">Working script for rehearsal. Dialogue, stage directions, and cues only. The director's full notes &mdash; concept, portraits, part&#8209;notes, alternatives &mdash; live in the Director's Copy.</p>
    <p class="cast-sub" style="margin-top:14px; font-size:9.5pt;">All directorial readings, scorings, and production decisions in this edition are the work of Kiarash Jamshidi. Pirandello supplied the play; everything else around it is his.</p>
"""

PRODUCTION_NOTE = """
<section class="actor-production-note">
  <h2>Two stage objects, three projections</h2>
  <p>In this production the <strong>Boy</strong> is a wooden chair with a black coat folded over its back, a schoolboy's cap on the seat, and a small leather satchel at the chair leg. He is not played by a performer. Where the script asks the Step&#8209;Daughter to seize him or push him forward, she handles the chair and the coat. Where she pulls a revolver from his pocket, she pulls it from the coat hanging on the chair. The chair is at the side of the stage in Acts One and Two, and is moved behind the fountain basin in Act Three; the revolver shot is heard, not seen.</p>
  <p>The <strong>Child</strong> is a small wrapped bundle of white cloth, like a swaddling, with a black silk sash tied around it. She is carried, kissed, set down, and lifted again by the Step&#8209;Daughter and the Mother. The bundle is silent and motionless; it is moved only by other hands. The drowning at the fountain is hidden by the Step&#8209;Daughter bending over the bundle inside the basin; nothing is seen.</p>
  <p>Three brief <strong>projections</strong> appear on the rear wall. <em>Projection 1</em>, at the top of Act One, is silent: the Six arrive in video, the Boy walks to the chair and leaves his coat, the Step&#8209;Daughter sets the Child down and the Child becomes the bundle. <em>Projection 2</em>, at the top of Act Two, is the only audible projection: the Step&#8209;Daughter's recorded voice addresses the Child and the Boy as real children, then the revolver is found in the coat. Her live body stands silent below the screen during this. <em>Projection 3</em>, in Act Three, is a single ten&#8209;second held image of the chair behind the fountain &mdash; the act of watching, not the death.</p>
  <p>Player 1, Player 2, and Player 3 are the working actors of the Village Players company. Their role labels in the script (Leading Man, Property Man, Prompter, Door&#8209;keeper, Machinist, Madame Pace, etc.) are functions, not separate characters. The cast list overleaf lists which Player carries which functions.</p>
</section>
"""


def build_actor_html():
    html = SRC.read_text()
    soup = BeautifulSoup(html, "html.parser")

    # --- Strip the reader-UI controls (also print-hidden, but cleaner to remove)
    for selector in ["nav.r-controls", "aside.r-act-pin", "div.r-progress"]:
        for el in soup.select(selector):
            el.decompose()

    # --- Replace the cover content
    cover = soup.select_one("section.cover")
    if cover is not None:
        cover.clear()
        cover.append(BeautifulSoup(NEW_COVER_INNER, "html.parser"))

    # --- Drop the long character portraits section
    portraits = soup.select_one("section.portraits")
    if portraits is not None:
        portraits.decompose()

    # --- Drop the long production / casting note
    casting_note = soup.select_one("section.casting-note")
    if casting_note is not None:
        casting_note.decompose()

    # --- Drop every part-note aside (narrative prose, stats, beats)
    for note in soup.select("aside.part-note"):
        note.decompose()

    # --- Insert the minimal production note right after the cast section
    cast = soup.select_one("section.cast")
    if cast is not None:
        note_soup = BeautifulSoup(PRODUCTION_NOTE, "html.parser")
        cast.insert_after(note_soup)

    # --- Update <title>
    title_tag = soup.find("title")
    if title_tag is not None:
        title_tag.string = "Six Characters in Search of an Author — Actor Rehearsal Script"

    # --- Append a small print stylesheet so the script reads clean on paper
    extra_style = soup.new_tag("style")
    extra_style.string = """
/* Actor Rehearsal Script — additions over the Director's Copy stylesheet */
.actor-production-note { max-width: 720px; margin: 64px auto 48px; padding: 32px 0; border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); }
.actor-production-note h2 { font-family: 'Cormorant Unicase', serif; font-weight: 600; font-size: 11pt; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); margin: 0 0 18px 0; text-align: center; }
.actor-production-note p { margin: 0 0 12px 0; line-height: 1.65; font-size: 11pt; }
.actor-production-note p:last-child { margin-bottom: 0; }
"""
    head = soup.find("head")
    if head is not None:
        head.append(extra_style)

    return str(soup)


def main():
    out_html = build_actor_html()
    OUT.write_text(out_html)
    size_kb = OUT.stat().st_size // 1024
    print(f"Wrote {OUT.name} ({size_kb} KB)")


if __name__ == "__main__":
    main()
