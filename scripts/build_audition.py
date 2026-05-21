#!/usr/bin/env python3
"""Audition packet builder. Two pages per role: description, then sides.

Source: the user's director's edition (six_characters.html) of Pirandello's
public-domain 1921 play (Storer 1922 translation via Project Gutenberg
Australia, explicitly cited in the source document's colophon), with the
extensive directorial modifications made across this project."""
import os
from pathlib import Path
import json, re
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("PLAY_SRC", HERE / "six_characters_village_players.html"))
STATS = Path(os.environ.get("STATS_SRC", HERE / "data" / "role_stats.json"))
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
CHROMIUM = os.environ.get("CHROMIUM_PATH")

src_html = SRC.read_text()
stats = json.loads(STATS.read_text())


def find_speech_by_opener(opener):
    """Find a speech whose dialogue begins with `opener` (after speaker label
    and any leading stage-direction). Returns the speech HTML or None."""
    for m in re.finditer(r'<p class="speech">(.*?)</p>', src_html, re.DOTALL):
        block = m.group(1)
        # Strip the speaker label — handle nested (as Role) spans for Players
        body = re.sub(
            r'<span class="speaker">.*?</span>(?:</span>)?\s*\.?\s*',
            '', block, count=1, flags=re.DOTALL
        )
        stripped = re.sub(r'^(<span class="action">.*?</span>\s*\.?\s*)?', '', body, flags=re.DOTALL)
        plain = re.sub(r'<[^>]+>', '', stripped).strip()
        if plain.startswith(opener):
            return block.strip()
    return None


def get_speaker(block):
    """Get the visible speaker label, including nested (as Role) text."""
    m = re.search(r'<span class="speaker">(.*?)</span>(?:</span>)?', block, re.DOTALL)
    if not m: return ""
    raw = m.group(0)
    return re.sub(r'<[^>]+>', '', raw).strip()


def speech_dialogue_html(block):
    """Return the dialogue portion (HTML) after stripping the speaker label."""
    return re.sub(
        r'<span class="speaker">.*?</span>(?:</span>)?\s*\.?\s*',
        '', block, count=1, flags=re.DOTALL
    ).strip()


def extract_portrait(name):
    m = re.search(
        r'<div class="portrait">\s*<div class="p-num">[^<]+</div>\s*'
        r'<h3 class="p-name">' + re.escape(name) + r'</h3>\s*'
        r'<span class="p-tag">([^<]+)</span>\s*'
        r'<p class="p-body">(.*?)</p>',
        src_html, re.DOTALL
    )
    return (m.group(1), m.group(2).strip()) if m else ("", "")


ROLES = [
    {"name": "The Father", "stats_key": "The Father",
     "cold_line": "Each one of us has within him a whole world of things, and to every one of us our own world.",
     "cold_context": "Act Three — the philosophical voice",
     "sides_picks": [
         ("For the drama lies all in this", "Act One — the consciousness speech"),
         ("He disappears soon, you know.", "Act One — describing how the drama ends"),
     ]},
    {"name": "The Mother", "stats_key": "The Mother",
     "cold_line": "It's taking place now. It happens all the time.",
     "cold_context": "Act Two — the only true unmediated cry",
     "sides_picks": [
         ("It's taking place now. It happens all the time.", "Act Two — the central cry"),
         ("He forced me to it", "Act One — defending her past"),
         ("And isn't my punishment the worst of all?", "Act Two — under accusation"),
     ]},
    {"name": "The Step-Daughter", "stats_key": "The Step-Daughter",
     "cold_line": "And I came as mistress of the house.",
     "cold_context": "Act Two — the shop scene",
     "sides_picks": [
         ("My little darling! You're frightened", "Act Two opening — to the bundle"),
         ("Yes, in the sun, in the sun!", "Act Three — at the fountain"),
     ]},
    {"name": "The Son", "stats_key": "The Son",
     "cold_line": "I am an 'unrealised' character, dramatically speaking; and I feel ill at ease in their company.",
     "cold_context": "Act Three — the refuser defines himself",
     "sides_picks": [
         ("Yes, but haven't you yet perceived", "Act Three — the mirror speech"),
         ("How should I know? When had I ever", "Act Two — first arrival of the family"),
         ("And they want to put it on the stage!", "Act Three — refusing the production"),
     ]},
    {"name": "The Manager", "stats_key": "The Manager",
     "cold_line": "I've lost a whole day over these people.",
     "cold_context": "Act Three — the curtain line",
     "sides_picks": [
         ("Ridiculous? Ridiculous? Is it my fault", "Act One — the anti-Pirandello rant"),
         ("Well then, we'll have it in the garden", "Act Three — directing the climax"),
     ]},
    {"name": "Player 1", "stats_key": "Player 1",
     "cold_line": "Excuse me — must I really wear a cook's cap? I trained at the Conservatoire for this.",
     "cold_context": "Act One — the Leading Man's vanity",
     "sides_picks": [
         ("Excuse me — must I really wear a cook's cap", "Act One — as Leading Man"),
         ("What a spectacle. What an absolute treat", "Act One — at the family's arrival"),
         ("It's absolutely unheard of. If the stage has come to this", "Act One — outrage"),
         ("I only let them in. Don't blame me.", "Act One — as Door-keeper"),
     ]},
    {"name": "Player 2", "stats_key": "Player 2",
     "cold_line": "A game! For heaven's sake — we are not children. We are serious actors.",
     "cold_context": "Act Two — the Leading Lady refusing 'the game'",
     "sides_picks": [
         ("A game! For heaven's sake", "Act Two — as Leading Lady"),
         ("Nobody has ever dared to laugh at me", "Act Two — wounded vanity"),
         ("One can't hear a word. I would have preferred surtitles.", "Act Two — during the shop scene"),
     ]},
    {"name": "Player 3", "stats_key": "Player 3",
     "cold_line": "This is rank madness. Beautiful rank madness — but madness.",
     "cold_context": "Act One — the Juvenile Lead",
     "sides_picks": [
         ("This is rank madness", "Act One — as Juvenile Lead"),
         ("I'm out of it anyway. I have a thing on Tuesday.", "Act One — refusing the chaos"),
         ("And he takes them seriously!", "Act One — disbelief"),
     ]},
]

# Resolve picks
for r in ROLES:
    resolved = []
    for opener, context in r["sides_picks"]:
        block = find_speech_by_opener(opener)
        if block:
            resolved.append({
                "speaker": get_speaker(block),
                "context": context or "",
                "dialogue_html": speech_dialogue_html(block),
            })
        else:
            print(f"!! MISS for {r['name']}: '{opener[:50]}'")
    r["sides_resolved"] = resolved


def render_role_description(r):
    tag, body = extract_portrait(r["name"])
    s = stats.get(r["stats_key"], {"speeches": 0, "words": 0})
    return f"""
  <section class="role-page">
    <header class="role-head">
      <p class="role-eyebrow">Role · Track</p>
      <h2>{r["name"]}</h2>
      <p class="role-tag">{tag}</p>
    </header>
    <p class="role-stats">
      <span><strong>{s['speeches']}</strong> speeches</span>
      <span class="dot">·</span>
      <span><strong>{s['words']:,}</strong> words across the production</span>
    </p>
    <p class="role-body">{body}</p>
    <div class="cold-line">
      <span class="cold-label">Cold-read line</span>
      <p class="cold-quote">&ldquo;{r["cold_line"]}&rdquo;</p>
      <p class="cold-context">{r["cold_context"]}</p>
    </div>
    <p class="sides-note">Audition sides for this role follow on the next page.</p>
  </section>
"""


def render_sides_page(r):
    parts = []
    for i, side in enumerate(r["sides_resolved"], 1):
        ctx = f'<span class="side-context">{side["context"]}</span>' if side["context"] else ""
        parts.append(f"""
    <article class="side">
      <header class="side-head"><span class="side-num">Side {i}</span> {ctx}</header>
      <p class="side-line"><span class="side-speaker">{side["speaker"]}.</span> {side["dialogue_html"]}</p>
    </article>
""")
    return f"""
  <section class="sides-page">
    <header class="sides-header">
      <p class="sides-eyebrow">Audition Sides</p>
      <h2>{r["name"]}</h2>
    </header>
    {"".join(parts)}
    <footer class="sides-footer">
      <p>Prepare one or more of the sides above. Callbacks may include cold reads from other scenes.</p>
    </footer>
  </section>
"""


ROLE_PAGES_HTML = "\n".join(render_role_description(r) + render_sides_page(r) for r in ROLES)


HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Audition Packet — Six Characters in Search of an Author</title>
<style>
  :root {{ --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }}
  @page {{ size: A4; margin: 22mm 20mm 22mm 20mm; }}
  *,*::before,*::after {{ box-sizing: border-box; }}
  html, body {{ background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif; font-size: 11pt; line-height: 1.55; margin: 0; padding: 0; }}

  .cover {{ min-height: 250mm; display:flex; flex-direction:column; justify-content:center; text-align:center; page-break-after: always; }}
  .cover-eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; letter-spacing:0.32em; font-size:12pt; color:var(--accent); text-transform:uppercase; margin-bottom:14mm; }}
  .cover h1 {{ font-family:'Cormorant Garamond',serif; font-weight:500; font-size:38pt; line-height:1.05; margin:0 0 4mm 0; }}
  .cover-italian {{ font-style:italic; font-size:14pt; color:var(--ink-soft); margin:0 0 18mm 0; }}
  .cover-byline {{ font-size:11pt; color:var(--ink-soft); margin:0 0 14mm 0; }}
  .cover-divider {{ width:60mm; height:1px; background:var(--rule); margin:6mm auto; }}
  .cover-production {{ font-size:14pt; letter-spacing:0.08em; margin:0 0 2mm 0; }}
  .cover-place {{ font-style:italic; font-size:11pt; color:var(--ink-soft); }}

  section.front {{ max-width:165mm; margin:0 auto; page-break-after:always; }}
  section.front h2 {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.20em; text-transform:uppercase; color:var(--accent); margin:14mm 0 4mm 0; }}
  section.front p {{ margin:0 0 4mm 0; }}
  dl.logistics {{ margin:0; display:grid; grid-template-columns:36mm 1fr; gap:3mm 5mm; }}
  dl.logistics dt {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.10em; text-transform:uppercase; color:var(--ink-soft); padding-top:1pt; }}
  dl.logistics dd {{ margin:0; }}

  .role-page {{ max-width:165mm; margin:0 auto; page-break-after:always; padding-top:4mm; }}
  .role-head {{ margin-bottom:8mm; }}
  .role-eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.20em; text-transform:uppercase; color:var(--accent); margin:0 0 2mm 0; }}
  .role-page h2 {{ font-family:'Cormorant Garamond',serif; font-weight:500; font-size:30pt; margin:0; letter-spacing:0.01em; }}
  .role-tag {{ font-style:italic; color:var(--ink-soft); margin:1mm 0 0 0; font-size:12pt; }}
  .role-stats {{ font-size:10pt; color:var(--ink-soft); margin:0 0 6mm 0; font-variant-numeric:tabular-nums; }}
  .role-stats .dot {{ margin:0 3mm; }}
  .role-body {{ margin:0 0 8mm 0; line-height:1.7; font-size:11.5pt; }}
  .cold-line {{ margin:0 0 6mm 0; padding:5mm 6mm; background:rgba(42,32,26,0.04); border:1px solid var(--rule); border-radius:1mm; }}
  .cold-label {{ display:block; font-family:'Cormorant Unicase',serif; font-weight:600; font-size:8.5pt; letter-spacing:0.15em; text-transform:uppercase; color:var(--ink-soft); margin-bottom:2mm; }}
  .cold-quote {{ font-family:'Cormorant Garamond',serif; font-style:italic; font-size:15pt; line-height:1.4; color:var(--ink); margin:0 0 2mm 0; }}
  .cold-context {{ font-size:9.5pt; color:var(--ink-soft); margin:0; }}
  .sides-note {{ font-style:italic; color:var(--accent); font-size:10pt; margin-top:6mm; }}

  .sides-page {{ max-width:165mm; margin:0 auto; page-break-after:always; padding-top:4mm; }}
  .sides-header {{ margin-bottom:8mm; padding-bottom:4mm; border-bottom:1px solid var(--rule); }}
  .sides-eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.20em; text-transform:uppercase; color:var(--accent); margin:0 0 2mm 0; }}
  .sides-page h2 {{ font-family:'Cormorant Garamond',serif; font-weight:500; font-size:26pt; margin:0; }}
  article.side {{ margin-bottom:7mm; page-break-inside:avoid; }}
  .side-head {{ margin-bottom:2mm; display:flex; align-items:baseline; gap:5mm; }}
  .side-num {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); }}
  .side-context {{ font-style:italic; font-size:10pt; color:var(--ink-soft); }}
  .side-line {{ margin:0; padding:3mm 0 3mm 4mm; border-left:2px solid var(--rule); line-height:1.65; font-size:11.5pt; }}
  .side-speaker {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10.5pt; letter-spacing:0.05em; margin-right:3mm; color:var(--ink); }}
  .side-line .action {{ font-style:italic; color:var(--ink-soft); font-size:10.5pt; }}
  .sides-footer {{ margin-top:8mm; padding-top:4mm; border-top:1px solid var(--rule); font-style:italic; font-size:9.5pt; color:var(--ink-soft); }}
  .sides-footer p {{ margin:0; }}

  .silent-note {{ max-width:165mm; margin:8mm auto 0; padding:6mm 7mm; border:1px dashed var(--rule); font-size:10.5pt; color:var(--ink-soft); line-height:1.6; }}
  .silent-note h3 {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); margin:0 0 3mm 0; }}
  .footer-strip {{ max-width:165mm; margin:12mm auto 0; padding-top:4mm; border-top:1px solid var(--rule); font-size:9pt; color:var(--ink-soft); text-align:center; font-style:italic; }}
</style>
</head>
<body>

  <section class="cover">
    <p class="cover-eyebrow">Audition Packet · with sides</p>
    <h1>Six Characters<br>in Search of an Author</h1>
    <p class="cover-italian">Sei personaggi in cerca d'autore</p>
    <p class="cover-byline">by Luigi Pirandello &nbsp;·&nbsp; translated by Edward Storer</p>
    <div class="cover-divider"></div>
    <p class="cover-production">A Village Players production</p>
    <p class="cover-place">Lausanne, Switzerland</p>
  </section>

  <section class="front">
    <h2>About the production</h2>
    <p>The Village Players are casting Pirandello's metatheatrical comedy for a bold minimalist staging in Lausanne. Eight live performers carry the production. The Boy and the Child are not cast — they are objects on the stage (a coat-and-chair, a wrapped bundle). The rear wall lights up three times briefly; otherwise the stage is bare.</p>
    <p>Each act has a single defining visual element: a circle of chairs in Act One; a two-level set in Act Two; a single short fountain basin alone on stage in Act Three. The English of this version is contemporary. The first quarter of an hour is committed comedy. The last quarter of an hour is not.</p>

    <h2>What this packet contains</h2>
    <p>For each of the eight casting tracks you will find <strong>two pages</strong>: first, a description of the role with stats, playing direction, and a short cold-read line; then, on the following page, a set of <strong>audition sides</strong> — actual lines from the production, ready to prepare. Choose one or more sides per role. Callbacks may include cold reads from other scenes.</p>

    <h2>Auditions</h2>
    <dl class="logistics">
      <dt>Where</dt><dd>Lausanne — venue to be confirmed</dd>
      <dt>When</dt><dd>By appointment</dd>
      <dt>What to prepare</dt><dd>One sides selection from the role you are auditioning for, plus an optional one-minute monologue of your choice.</dd>
      <dt>Self-tapes</dt><dd>Accepted for the first round.</dd>
    </dl>

    <h2>How to apply</h2>
    <p>Send headshot, CV, and a brief note on which role you wish to audition for, to: <em>casting&nbsp;[at]&nbsp;villageplayers&nbsp;[dot]&nbsp;ch</em>. Please indicate any access requirements.</p>
  </section>

  {ROLE_PAGES_HTML}

  <div class="silent-note">
    <h3>Silent presences — not cast</h3>
    <p>The Boy and the Child — the two youngest of the Six — are not played by performers in this production. The Boy is a black coat and a schoolboy's cap on a wooden chair, with a leather satchel at the chair leg. The Child is a small wrapped bundle of white cloth, carried by the Step-Daughter and the Mother. They appear briefly in three short projections and otherwise live in the chair and the bundle.</p>
  </div>

  <p class="footer-strip">Village Players · Lausanne &nbsp;·&nbsp; Casting Packet</p>

</body>
</html>
"""

OUT_DIR.mkdir(parents=True, exist_ok=True)
HTML_PATH = OUT_DIR / "audition_call.html"
HTML_PATH.write_text(HTML)
print(f"Wrote {HTML_PATH} ({HTML_PATH.stat().st_size:,} bytes)")

OUT = OUT_DIR / "audition_call.pdf"
with sync_playwright() as p:
    launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
    browser = p.chromium.launch(**launch_kwargs)
    page = browser.new_page()
    page.goto(f"file://{HTML_PATH.resolve()}", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(800)
    page.pdf(path=str(OUT), format="A4",
             margin={"top":"22mm","right":"20mm","bottom":"22mm","left":"20mm"},
             print_background=True, prefer_css_page_size=True)
    browser.close()

try:
    from pypdf import PdfReader
    r = PdfReader(str(OUT))
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes) · {len(r.pages)} pages")
except BaseException:
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes)")
