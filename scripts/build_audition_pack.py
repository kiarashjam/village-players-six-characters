#!/usr/bin/env python3
"""Build the unified Audition PDF.

Produces a single PDF with:
  1. A cover and intro (production concept, the eight performers, the
     stage objects, role list, how to audition).
  2. One section per role with an audition side pulled byte-identically
     from the play HTML — a real stretch of consecutive dialogue from
     the part where the character is most active. Approximately two
     pages of script per role.

The dialogue is extracted from six_characters_village_players.html so
that any edit to the play is reflected in the audition pack the next
time this script is run.
"""
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("PLAY_SRC", HERE / "six_characters_village_players.html"))
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
CHROMIUM = os.environ.get("CHROMIUM_PATH")

src_html = SRC.read_text()


# ---------------------------------------------------------------------------
# Scene boundaries — for each role, the start/end of the audition side.
# Anchors are matched against the opener of <p class="speech"> blocks.
# Each side is a real scene from the play: the actor reads it as written.
# ---------------------------------------------------------------------------

SIDES = [
    {
        "role": "The Father",
        "tag": "the brain of the family",
        "context": "Act One — his confession. The Step-Daughter has just exposed the hundred francs at Madame Pace's shop. The Father attempts to explain himself; the philosophy cracks; the body gives him away.",
        "from_speaker": "The Father",
        "from_opener": "Naturally enough. I would ask you",
        "to_speaker": "The Father",
        "to_opener": "Fool! That is the proof that I am a man",
    },
    {
        "role": "The Mother",
        "tag": "silence that finally screams",
        "context": "Act Two, Part III — the Step-Daughter asks for the Mother to be sent away. After an entire act and a half of silence, the Mother breaks. \"It's taking place now\" is her keystone line.",
        "from_speaker": "The Step-Daughter",
        "from_opener": "Well then, ask that Mother there to leave",
        "to_speaker": "The Mother",
        "to_opener": "No! My daughter, my daughter",
    },
    {
        "role": "The Step-Daughter",
        "tag": "the one who refuses to let it be made beautiful",
        "context": "Act One, Part II — the exposure. She forces the room to hear what happened to her and refuses to let her shame be made into a scene.",
        "from_speaker": "The Step-Daughter",
        "from_opener": "Worse? Listen!",
        "to_speaker": "The Step-Daughter",
        "to_opener": "Shame? Oh, the shame is mine",
    },
    {
        "role": "The Son",
        "tag": "the one who will not act",
        "context": "Act Three, Part II — the refusal. He tries to leave; he cannot; the Step-Daughter names what is happening to him. The mirror speech is in here. So is the closing exchange (\"Nobody can force me\" / \"I can\").",
        "from_speaker": "The Step-Daughter",
        "from_opener": "It's useless to hope he will speak",
        "to_speaker": "The Father",
        "to_opener": "I can.",
    },
    {
        "role": "The Manager",
        "tag": "the director on a deadline",
        "context": "Act One — the opening rehearsal. He bickers with the Leading Man about the cook's cap, insults the playwright, and sets the company in motion.",
        "from_speaker": "The Manager",
        "from_opener": "I can't see a thing in here",
        "to_speaker": "The Manager",
        "to_opener": "Yes, yes, of course",
    },
    {
        "role": "Player 1",
        "tag": "one character in five hats — the faded Leading Man",
        "context": "Act Two, Part III — the Leading Man takes the platform and plays the Father in the shop scene. Practised gallantry meets a woman half his age who has been through the actual room.",
        "from_speaker": "The Manager",
        "from_opener": "See here! The scene between you and Madame Pace",
        "to_speaker": "Player 1",
        "to_opener": "Neither am I. I am through",
    },
    {
        "role": "Player 2",
        "tag": "the diva and the props",
        "context": "Act Two, Part III — the Leading Lady takes the platform to play the Step-Daughter, and is corrected mid-scene by the woman whose worst hour it actually was. The glasses come off.",
        "from_speaker": "Player 2",
        "from_opener": "Of course. It's easy enough",
        "to_speaker": "Player 2",
        "to_opener": "I am not going to stand here being made a fool of",
    },
    {
        "role": "Player 3 / Madame Pace",
        "tag": "the youngest, and Madame Pace",
        "context": "Act Two, Part II — Madame Pace materialises on the platform. She arrives comic, exits chilling. Player 3 enters her costume the way an apparition enters a body.",
        "from_speaker": "Player 3",
        "from_opener": "Buongiorno, buongiorno, signor",
        "to_speaker": "Player 3",
        "to_opener": "Sì sì, certo. I go. I go",
    },
]


# ---------------------------------------------------------------------------
# Speech extraction helpers
# ---------------------------------------------------------------------------

def get_speaker(block_html):
    m = re.search(r'<span class="speaker">(.*?)</span>(?:</span>)?', block_html, re.DOTALL)
    if not m:
        return ""
    raw = m.group(0)
    return re.sub(r'<[^>]+>', '', raw).strip()


def speech_plain(block_html):
    """Plain text of the dialogue (without speaker label or stage directions)."""
    body = re.sub(
        r'<span class="speaker">.*?</span>(?:</span>)?\s*\.?\s*',
        '', block_html, count=1, flags=re.DOTALL
    )
    body = re.sub(r'<span class="action">.*?</span>', '', body, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', body)
    # Strip any leading punctuation/whitespace residue left behind by removed spans
    return re.sub(r'^[\s\.,;:!?\-—…]+', '', text).strip()


def _norm(text):
    """Normalise text for matching — collapse all curly quotes / dashes /
    ellipses to their ASCII equivalents, lowercase, collapse whitespace."""
    if not text:
        return ""
    t = text
    # Curly apostrophes and quotes
    t = t.replace("’", "'").replace("‘", "'")
    t = t.replace("“", '"').replace("”", '"')
    # Em-dash and en-dash → simple dash
    t = t.replace("—", "-").replace("–", "-")
    # Ellipsis
    t = t.replace("…", "...")
    # Non-breaking spaces and other whitespace
    t = re.sub(r'\s+', ' ', t)
    return t.strip().lower()


def find_speech_index(speaker, opener):
    """Find the index of a speech matching both speaker and opener-text.
    Returns the match span (start, end) in src_html, or None.
    """
    target_speaker = _norm(speaker)
    target_opener = _norm(opener)[:50]   # match on the first 50 chars
    for m in re.finditer(r'<p class="speech">.*?</p>', src_html, re.DOTALL):
        block = m.group(0)
        sp = _norm(get_speaker(block))
        # Speaker test: starts with the target. Player 1 / Player 1 (as ...) both ok.
        if not sp.startswith(target_speaker):
            continue
        plain = _norm(speech_plain(block))
        if plain.startswith(target_opener):
            return m.span()
    return None


def extract_portrait(name):
    """Pull the portrait HTML for a character (name = 'The Father', 'Player 1', etc).
    Returns (tag, body_html) — the body_html may be multiple <p class="p-body"> blocks.
    """
    pattern = (
        r'<div class="portrait">\s*<div class="p-num">[^<]+</div>\s*'
        r'<h3 class="p-name">' + re.escape(name) + r'</h3>\s*'
        r'<span class="p-tag">([^<]+)</span>\s*'
        r'(.*?)'
        r'</div>'
    )
    m = re.search(pattern, src_html, re.DOTALL)
    if not m:
        return ("", "")
    tag = m.group(1).strip()
    body = m.group(2).strip()
    return (tag, body)


def extract_scene(side):
    """Pull every <p class="speech"> and <p class="stage"> block between
    the start and end anchors (inclusive). Returns the raw HTML stretch."""
    start = find_speech_index(side["from_speaker"], side["from_opener"])
    end = find_speech_index(side["to_speaker"], side["to_opener"])
    if not start or not end:
        missing = []
        if not start:
            missing.append(f"start anchor: {side['from_speaker']} / {side['from_opener'][:40]}")
        if not end:
            missing.append(f"end anchor: {side['to_speaker']} / {side['to_opener'][:40]}")
        raise ValueError(f"Anchor miss for {side['role']}: {', '.join(missing)}")
    if end[1] <= start[0]:
        raise ValueError(f"End anchor precedes start for {side['role']}")
    # Pull everything from start of first speech to end of last
    stretch = src_html[start[0]:end[1]]
    # Drop any <aside class="part-note">…</aside> that may have been mid-stretch
    stretch = re.sub(r'<aside class="part-note">.*?</aside>', '', stretch, flags=re.DOTALL)
    # Drop any <section class="act-header">…</section>
    stretch = re.sub(r'<section class="act-header">.*?</section>', '', stretch, flags=re.DOTALL)
    return stretch.strip()


# ---------------------------------------------------------------------------
# HTML page composition
# ---------------------------------------------------------------------------

# The audition HTML reuses the play's existing CSS (linked inline) so the
# extracted dialogue renders with the same typography as the play.
# We pull the entire <style> block from the source HTML.
style_match = re.search(r'<style[^>]*>(.*?)</style>', src_html, re.DOTALL)
PLAY_CSS = style_match.group(1) if style_match else ""

EXTRA_CSS = """
/* Audition pack — additions on top of the play stylesheet */
@page { size: A4; margin: 22mm 20mm 22mm 20mm; }
html, body { background: #efe6cf !important; color: #2a201a !important; }
body { font-family: 'EB Garamond','Georgia','Times New Roman',serif; font-size: 11pt; line-height: 1.6; }
.r-controls, .r-progress, .r-act-pin { display: none !important; }

main.audition { max-width: 168mm; margin: 0 auto; }

.cover { page-break-after: always; padding-top: 18mm; text-align: center; }
.cover .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.28em; text-transform:uppercase; color:var(--accent, #8b3a3a); margin: 0 0 14mm 0; }
.cover h1 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size:36pt; line-height:1.05; margin: 0 0 4mm 0; }
.cover .italian { font-style:italic; font-size:14pt; color:#6b5b48; margin: 0 0 10mm 0; }
.cover .credit { font-size:11pt; margin: 4mm 0; }
.cover .company { margin-top:14mm; font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.22em; text-transform:uppercase; }

.intro { page-break-after: always; padding-top: 6mm; }
.intro h2 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size:22pt; margin: 0 0 4mm 0; }
.intro h3 { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.18em; text-transform:uppercase; color:var(--accent, #8b3a3a); margin: 10mm 0 3mm 0; }
.intro p { margin: 0 0 4mm 0; line-height: 1.7; }
.intro ul { margin: 0 0 4mm 0; padding-left: 5mm; }
.intro ul li { margin-bottom: 2mm; line-height: 1.6; }

.role-list { page-break-after: always; padding-top: 6mm; }
.role-list h2 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size:22pt; margin: 0 0 4mm 0; }
.role-list .group { margin-top: 8mm; }
.role-list .group h3 { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.18em; text-transform:uppercase; color:var(--accent, #8b3a3a); margin: 0 0 3mm 0; }
.role-list .group ul { list-style:none; padding:0; margin:0; }
.role-list .group li { padding: 1mm 0; border-bottom: 1px dotted rgba(42,32,26,0.2); display:flex; justify-content:space-between; }
.role-list .group li .role-name { font-weight:600; }
.role-list .group li .role-sub { font-size: 9.5pt; color:#6b5b48; font-style: italic; text-align:right; max-width: 90mm; }

.side { page-break-before: always; padding-top: 4mm; }
.side > header { padding-bottom: 6mm; margin-bottom: 6mm; border-bottom: 1px solid rgba(42,32,26,0.18); }
.side > header .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.20em; text-transform:uppercase; color:var(--accent, #8b3a3a); margin: 0 0 2mm 0; }
.side > header h2 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size:28pt; margin: 0 0 2mm 0; }
.side > header .tag { font-style:italic; color:#6b5b48; font-size:11pt; margin: 0; }

.character-reading { margin-bottom: 10mm; }
.character-reading .p-body { font-size: 10.5pt; line-height: 1.65; margin: 0 0 3mm 0; text-align: justify; }
.character-reading .p-body em { font-style: italic; }
.character-reading .p-body strong { font-weight: 600; }

.scene-intro { margin: 8mm 0 6mm 0; padding: 4mm 0; border-top: 1px dotted rgba(42,32,26,0.25); border-bottom: 1px dotted rgba(42,32,26,0.25); }
.scene-intro .scene-eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.20em; text-transform:uppercase; color:var(--accent, #8b3a3a); margin: 0 0 2mm 0; }
.scene-intro p { font-size: 10.5pt; line-height: 1.6; margin: 0; font-style: italic; color: #4d3f30; }

.side .scene { font-size: 11pt; line-height: 1.6; }
.side .scene .speech { margin: 0 0 3mm 0; orphans: 2; widows: 2; }
.side .scene .stage { font-style: italic; color:#6b5b48; margin: 3mm 0; line-height: 1.55; }
"""

COVER_HTML = """
<section class="cover">
  <p class="eyebrow">Audition Pack</p>
  <h1>Six Characters<br>in Search of an Author</h1>
  <p class="italian">Sei personaggi in cerca d'autore</p>
  <p class="credit">Luigi Pirandello &nbsp;·&nbsp; trans. Edward Storer (1922)</p>
  <p class="credit">Director's edition — Village Players, Lausanne</p>
  <p class="credit"><strong>Rewritten and directed by Kiarash Jamshidi</strong></p>
  <p class="company">Auditions for the production</p>
</section>
"""

INTRO_HTML = """
<section class="intro">
  <h2>About the production</h2>
  <p>This is a director's edition of Pirandello's 1921 play, performed by the Village Players of Lausanne — an English-speaking amateur company based at SSA Lausanne. The text is the Storer 1922 translation, modernised throughout and anchored locally: the Players speak as expat actors in the canton; Madame Pace runs her atelier off the rue de Bourg; the Manager is on a deadline he is already losing.</p>

  <p>The production is built for <strong>eight live performers, two stage objects, and three stripped settings</strong> — no projection, no video, no screen. Four actors play the family (Father, Mother, Step-Daughter, Son); one plays the Manager; three "Players" cover the dozen company roles (Leading Man, Leading Lady, Juvenile Lead, Prompter, Property Man, Door-keeper, Machinist, L'Ingénue, and the rest), with Player 3 also becoming Madame Pace when she materialises.</p>

  <h3>Two stage objects</h3>
  <p>The <strong>Boy</strong> (in Pirandello, a silent fourteen-year-old) is, in this production, a wooden chair with a black coat folded over its back, a schoolboy's cap on the seat, and a small leather satchel at the chair leg. He is not played by a performer. The Door-keeper sets the chair at the edge of the stage as the Six walk on, and the family treats it as the Boy from that moment forward. Where the Step-Daughter seizes him or pushes him forward, she handles the chair and the coat. Where she pulls a revolver from his pocket, she pulls it from the coat hanging on the chair.</p>

  <p>The <strong>Child</strong> (Pirandello's silent four-year-old) is a small wrapped bundle of white cloth, like a swaddling, with a black silk sash. The Step-Daughter walks on already carrying her, and from then on the bundle is carried, kissed, set down, and lifted again by the Step-Daughter and the Mother. The bundle is silent and motionless; it is moved only by other hands. The drowning at the fountain is hidden by the Step-Daughter bending over the bundle inside the basin; nothing is seen.</p>

  <h3>Three stripped settings</h3>
  <p>Act One — a bare stage with a circle of chairs. Act Two — a two-level set; the upper platform is where the family's drama is rehearsed, the lower floor is everywhere else. Act Three — a single short fountain basin centre stage, the chair-and-coat moved behind it, otherwise empty.</p>

  <h3>What we are casting for</h3>
  <p>Tone matters more than type. The Characters — Father, Mother, Step-Daughter, Son — must feel timeless, serious, almost ghost-like. The Players — Manager, Player 1, Player 2, Player 3 — must feel modern, local, alive, like a real Village Players rehearsal that has been invaded by a tragedy. The contrast between the two worlds is the production. We are not casting types; we are casting voices that can hold one of those two registers cleanly.</p>
</section>
"""

ROLE_LIST_HTML = """
<section class="role-list">
  <h2>Roles to be cast</h2>

  <div class="group">
    <h3>The Six Characters &nbsp;·&nbsp; live performers</h3>
    <ul>
      <li><span class="role-name">The Father</span><span class="role-sub">~50, the philosophical voice; mellifluous and violent by turns</span></li>
      <li><span class="role-name">The Mother</span><span class="role-sub">silence that finally screams; veil and bundle as language</span></li>
      <li><span class="role-name">The Step-Daughter</span><span class="role-sub">the moral centre; sharp, controlled, never coquettish</span></li>
      <li><span class="role-name">The Son</span><span class="role-sub">~22, the refuser; hands in pockets, every line a door closing</span></li>
    </ul>
  </div>

  <div class="group">
    <h3>The Six Characters &nbsp;·&nbsp; stage objects</h3>
    <ul>
      <li><span class="role-name">The Boy</span><span class="role-sub">chair-and-coat — no performer needed</span></li>
      <li><span class="role-name">The Child</span><span class="role-sub">wrapped bundle — no performer needed</span></li>
    </ul>
  </div>

  <div class="group">
    <h3>The Village Players &nbsp;·&nbsp; live performers</h3>
    <ul>
      <li><span class="role-name">The Manager</span><span class="role-sub">a Lausanne theatre veteran on a deadline; cynicism is technique, compassion is real</span></li>
      <li><span class="role-name">Player 1</span><span class="role-sub">Leading Man · L'Ingénue · Door-keeper · Machinist · Third Actor — one character in five hats; the faded Anglo Leading Man</span></li>
      <li><span class="role-name">Player 2</span><span class="role-sub">Leading Lady · Property Man · Fourth Actor · Second Lady Lead — the veteran character actress; the diva and the props in one body</span></li>
      <li><span class="role-name">Player 3</span><span class="role-sub">Juvenile Lead · Prompter · Madame Pace · An Actor · Fifth Actor — the youngest, with the most theatrical transformation; comic on entry, chilling on exit</span></li>
    </ul>
  </div>
</section>
"""

HOW_TO_AUDITION_HTML = """
<section class="intro" style="page-break-after: auto;">
  <h2>How to audition</h2>

  <p>Each role on the following pages has a <strong>side</strong> — a real stretch of consecutive dialogue from the production script, pulled from the part where the character is most active. Bring your side. Read it as written.</p>

  <h3>Format</h3>
  <ul>
    <li>Each side is presented exactly as it appears in the production script, including the bracketed stage directions that name what the body should be doing — heat at the brow, a small grooming gesture, the chin lifting, the breath catching, the bearing arriving. You do not need to perform every gesture — they are there so you can read the moment the way the production reads it.</li>
    <li>For multi-speaker scenes, the auditioning actor reads <em>their character's lines only</em>. A reader will give you the cues.</li>
    <li>Where stage directions specify physical actions (e.g., <em>[a hand goes to his brow, almost despite himself]</em>), feel free to mark them or ignore them — they are a guide to the moment, not a test of mime.</li>
  </ul>

  <h3>What we're looking for</h3>
  <ul>
    <li>For the four <strong>Characters</strong> (Father, Mother, Step-Daughter, Son): can you hold a register that is serious without being heavy? Tragic without being theatrical? Can you let the play come through you, rather than perform it?</li>
    <li>For the <strong>Manager</strong> and <strong>Players</strong> (1, 2, 3): can you carry a working rehearsal-room voice — local, modern, amateur in the best sense — and let the tragedy in the room change your face without you commenting on it?</li>
  </ul>

  <h3>Optional</h3>
  <p>If you have a short monologue you have already prepared — anything modern, any language — bring it. We are interested in how you sound when you are working from material you have lived with. The side will tell us how you read the production's specific text. Your prepared piece tells us who you are when you are alone with a script.</p>
</section>
"""


def render_side(side, scene_html, portrait_body):
    """Render one role section: full character description, then the audition side."""
    return f"""
<section class="side">
  <header>
    <p class="eyebrow">Audition · {side['role']}</p>
    <h2>{side['role']}</h2>
    <p class="tag">{side['tag']}</p>
  </header>

  <div class="character-reading">
    {portrait_body}
  </div>

  <div class="scene-intro">
    <p class="scene-eyebrow">Audition side — read this</p>
    <p>{side['context']}</p>
  </div>

  <div class="scene">
    {scene_html}
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sections = []
    for side in SIDES:
        # Portrait — the full character description from the play HTML.
        # Some entries (Player 3 / Madame Pace) need a single name for portrait lookup.
        portrait_name = side["role"].split(" / ")[0]
        tag, portrait_body = extract_portrait(portrait_name)
        if not portrait_body:
            print(f"  !! No portrait found for {side['role']}")
        try:
            scene = extract_scene(side)
            sections.append(render_side(side, scene, portrait_body))
            wc = len(re.sub(r'<[^>]+>', ' ', scene).split())
            print(f"  {side['role']:30s}  portrait + {wc:4d} words of scene")
        except ValueError as e:
            print(f"  !! {e}")

    body = COVER_HTML + HOW_TO_AUDITION_HTML + "".join(sections)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Six Characters — Audition Pack · Village Players Lausanne</title>
<style>
{PLAY_CSS}
{EXTRA_CSS}
</style>
</head>
<body>
<main class="audition">
{body}
</main>
</body>
</html>
"""

    out_html = OUT_DIR / "audition_pack.html"
    out_html.write_text(html)
    print(f"\nWrote {out_html.name} ({out_html.stat().st_size // 1024} KB)")

    out_pdf = OUT_DIR / "audition_pack.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page()
        page.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(800)
        page.pdf(
            path=str(out_pdf), format="A4",
            margin={"top": "22mm", "right": "20mm", "bottom": "22mm", "left": "20mm"},
            print_background=True, prefer_css_page_size=True,
        )
        browser.close()
    print(f"Wrote {out_pdf.name} ({out_pdf.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build()
