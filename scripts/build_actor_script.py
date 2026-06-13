#!/usr/bin/env python3
"""Build the Actor Rehearsal Script from the Director's Copy.

Strips: character portraits, casting/production note, all part-note
asides (narrative prose, stats, beats), and the reader-UI controls.

Keeps: cover (relabelled "Rehearsal Script"), the cast list, the
scene-setting line, a single one-paragraph note on this production's
two stage objects, and the full play text — every speech, every stage
direction, every cue, every act header, every curtain.
"""
import os
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

HERE = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("PLAY_SRC", HERE / "six_characters_village_players.html"))
OUT = Path(os.environ.get("ACTOR_OUT", HERE / "actor_script.html"))


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

    <p class="cast-sub" style="margin-top:32px;">Working script for rehearsal. Dialogue, stage directions, and cues only.</p>
    <p class="cast-sub" style="margin-top:14px; font-size:9.5pt;">All directorial readings, scorings, and production decisions in this edition are the work of Kiarash Jamshidi. Pirandello supplied the play; everything else around it is his.</p>
"""

PRODUCTION_NOTE = """
<section class="actor-production-note">
  <h2>Two stage objects, no projection</h2>
  <p>Two of the children are stage objects, not performers, and the script calls them by these names. The <strong>Boy&#8209;chair</strong> is a wooden chair with a black coat folded over its back, a schoolboy's cap on the seat, and a small leather satchel at the chair leg. Where the script asks the Step&#8209;Daughter to seize the Boy or push him forward, she handles the chair and the coat; where she takes a revolver from his pocket, she takes it from the coat hanging on the chair. The Boy&#8209;chair stands at the edge of the stage from the moment the Six walk on; in Act Three the Manager himself moves it behind the fountain basin, and the revolver shot is heard, not seen.</p>
  <p>The <strong>Child&#8209;bundle</strong> is a small wrapped bundle of white cloth, like a swaddling, with a black silk sash tied around it. It is carried, kissed, set down, and lifted again by the Step&#8209;Daughter and the Mother, from the moment the Step&#8209;Daughter walks on. It never moves on its own. The drowning at the fountain is hidden by the Step&#8209;Daughter bending over the Child&#8209;bundle inside the basin; nothing is seen.</p>
  <p>There is <strong>no projection, no video, no screen</strong> anywhere in the production. The Step&#8209;Daughter's Act Two opening monologue is delivered live, alone in the shower light, with the Child&#8209;bundle in her arms and the Boy&#8209;chair beside her. At the close of Act Three, as the Son narrates the drowning, the stage lights drop until only the fountain's interior glow and the bare bulb above the Manager's table remain; the Boy&#8209;chair is silhouetted behind the basin for ten seconds. Then full blackout. Then the gunshot, from where the Boy&#8209;chair is.</p>
  <p>Player 1, Player 2, and Player 3 are the working actors of the Village Players company. They carry no separate role names in this script: each plays many small functions across the morning — the actor at the cook&#8209;cap argument, the one at the stage door, the one at the prop trolley, the one in the prompt box, the one who works the curtain — but every line they speak is tagged simply <em>Player 1</em>, <em>Player 2</em>, or <em>Player 3</em>. <strong>Madame Pace</strong> is not a Player — she is a Character in her own right, carried by her own performer, conjured onto the stage in Act Two; her speeches are tagged simply <em>Madame Pace</em>.</p>
</section>
"""


# ---------------------------------------------------------------------------
# Actor-script stage-direction policy
# ---------------------------------------------------------------------------
# The Director's Copy keeps every stage direction in full, including the
# interpretive / psychological notes (why a beat lands, the audience effect,
# an actor's arc). Those are a director's-notebook layer. In the actor
# rehearsal script we keep only the playable part: trim the gloss off a
# direction, or drop one that is wholly interpretive. The Director's Copy
# source is never touched — this lives only in the actor build.

def _norm(s):
    """Normalise quotes, dashes and whitespace for robust matching."""
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'),
                 ("”", '"'), ("—", "-"), ("–", "-")):
        s = s.replace(a, b)
    return " ".join(s.split()).strip()


# Wholly interpretive directions — dropped from the actor script entirely.
_ACTION_DROP = {
    "the audience's confusion, on stage",
    "interpreting the rising anger of the Company",
    "the threat empty; both of them know it",
    "the only continuous sentence he gives the room; he tells it because he cannot keep it inside any longer",
    "the word arrives before he can stop it",
}

# Directions trimmed to their playable part (the psychological gloss removed).
_ACTION_TRIM = {
    "stung; it lands because it is half true":
        "stung",
    "he is sweating, very slightly, and trying to keep it from being read; the recovery is visible, that is the trouble":
        "he is sweating, very slightly, and trying to keep it from being read",
    "He says the line straight — no commentary, no irony, the audience's own thought said aloud by their proxy before they can say it themselves. He turns and leaves the stage the way a man leaves a theatre.":
        "He says the line straight. He turns and leaves the stage the way a man leaves a theatre.",
    "He stands. He picks up the Boy-chair himself and walks it across the stage. This is the pivot of his arc: until this gesture he has been the audience, watching from a remove. From this gesture forward he is the audience's complicity made physical. He places the Boy-chair behind the fountain basin, where it is partly hidden by the rim. The audience must read the move land.":
        "He stands. He picks up the Boy-chair himself and walks it across the stage, and places it behind the fountain basin, where it is partly hidden by the rim.",
    "a beat — the smallest pause. He did not, in fact, say \"I'm frightfully sorry.\" He said something else. The audience must see the lie being made in real time.":
        "a beat — the smallest pause.",
    "beginning to get really interested — leaning slightly forward, the way an audience member does when they have started to listen":
        "beginning to get really interested — leaning slightly forward",
    "cupping a hand to his ear, the bearing of a man used to being heard at the back of the house":
        "cupping a hand to his ear",
    "he is hooked, in spite of himself; the schedule he came in trying to defend is no longer in his mind":
        "he is hooked, in spite of himself",
    "looking up from the book; an unusual request to receive at this hour":
        "looking up from the book",
    "she cannot quite stop yet; the voice has been waiting too long":
        "she cannot quite stop yet",
    "she has been at work for an hour; shoulders forward, weight on the front foot":
        "shoulders forward, weight on the front foot",
    "the cry breaks; afterward the body goes still — not the composure he had at the start of this part, but a different stillness, as if he has just walked into the wall of his own argument she has just shown him":
        "the cry breaks; afterward the body goes still",
    "the diva fully present; she has done a thousand scenes harder than this":
        "the diva fully present",
    "the voice short again now, as if she has spent what she had":
        "the voice short again now",
    "The room hears the word \"naturally\". He does not look up.":
        "He does not look up.",
}

_ACTION_DROP_N = {_norm(k) for k in _ACTION_DROP}
_ACTION_TRIM_N = {_norm(k): v for k, v in _ACTION_TRIM.items()}


def simplify_stage_directions(soup):
    """Keep only the playable part of each stage direction in the actor script."""
    seen = set()
    for span in soup.select("span.action"):
        inner = span.get_text().strip()
        if inner.startswith("[") and inner.endswith("]"):
            inner = inner[1:-1].strip()
        key = _norm(inner)
        if key in _ACTION_DROP_N:
            prev = span.previous_sibling
            nxt = span.next_sibling
            span.decompose()
            if isinstance(prev, NavigableString) and str(prev).strip() == "":
                # lone space between speaker and the following ". dialogue"
                prev.extract()
            elif (isinstance(prev, NavigableString) and isinstance(nxt, NavigableString)
                  and str(prev).endswith(" ") and str(nxt).startswith(" ")):
                # mid-sentence drop: collapse the seam so no double space is left
                nxt.replace_with(str(nxt)[1:])
            seen.add(key)
        elif key in _ACTION_TRIM_N:
            span.clear()
            span.append("[" + _ACTION_TRIM_N[key] + "]")
            seen.add(key)
    missing = (_ACTION_DROP_N | set(_ACTION_TRIM_N)) - seen
    if missing:
        print("WARNING: stage-direction policy keys not matched (Director's Copy reworded?):")
        for m in sorted(missing):
            print("   ·", m)
    else:
        print(f"Simplified {len(seen)} director-only stage directions for the actor script.")


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

    # --- Keep only playable stage directions; the psychology stays in the Director's Copy
    simplify_stage_directions(soup)

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
/* Actor Rehearsal Script — additions over the base stylesheet */
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
