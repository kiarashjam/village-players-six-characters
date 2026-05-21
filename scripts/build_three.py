#!/usr/bin/env python3
"""Build three working documents for the audition process:
1. audition_packet_trimmed.pdf — the existing packet without
   the 'About the production', 'Auditions', and 'How to apply' sections.
2. sides_templates.pdf — 8 one-page blanks the user fills in locally.
3. scene_index.pdf — a one-page reference listing the speech locations
   (number + short ctrl-F fingerprint) for each role's likely sides."""
import os
from pathlib import Path
import re, json
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("PLAY_SRC", HERE / "six_characters_village_players.html"))
STATS = Path(os.environ.get("STATS_SRC", HERE / "data" / "role_stats.json"))
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

src_html = SRC.read_text()
stats = json.loads(STATS.read_text())

# ---------------------------------------------------------------------------
# Build numbered speech index from the working file
# ---------------------------------------------------------------------------
SPEECHES = []
for i, m in enumerate(re.finditer(r'<p class="speech">(.*?)</p>', src_html, re.DOTALL), 1):
    block = m.group(0)
    sp_m = re.search(r'<span class="speaker">(.*?)</span>(?:</span>)?', block, re.DOTALL)
    speaker = re.sub(r'<[^>]+>', '', sp_m.group(0)).strip() if sp_m else "?"
    body = re.sub(
        r'<span class="speaker">.*?</span>(?:</span>)?\s*\.?\s*',
        '', block, count=1, flags=re.DOTALL
    )
    body = re.sub(r'^(<span class="action">.*?</span>\s*\.?\s*)?', '', body, flags=re.DOTALL)
    plain = re.sub(r'<[^>]+>', '', body).strip()
    plain = re.sub(r'\s+', ' ', plain)
    SPEECHES.append({'num': i, 'speaker': speaker, 'opener_plain': plain})

# ---------------------------------------------------------------------------
# Pick a small set of audition-relevant speech locations per role.
# Each entry: opener-for-matching + short fingerprint to print + scene label.
# Speeches themselves stay in the user's working file — we only print numbers
# and ~5-word search fingerprints here.
# ---------------------------------------------------------------------------
PICKS = {
    "The Father": [
        ("For the drama lies all in this", "Act One — the consciousness speech"),
        ("He disappears soon, you know", "Act One — describing how the drama ends"),
    ],
    "The Mother": [
        ("It's taking place now", "Act Two — the central cry"),
        ("He forced me to it", "Act One — defending her past"),
        ("And isn't my punishment the worst", "Act Two — under accusation"),
    ],
    "The Step-Daughter": [
        ("My little darling! You're frightened", "Act Two opening — to the bundle"),
        ("Yes, in the sun, in the sun!", "Act Three — at the fountain"),
    ],
    "The Son": [
        ("Yes, but haven't you yet perceived", "Act Three — the mirror speech"),
        ("How should I know? When had I ever", "Act Two — first arrival of the family"),
        ("And they want to put it on the stage!", "Act Three — refusing the production"),
    ],
    "The Manager": [
        ("Ridiculous? Ridiculous? Is it my fault", "Act One — the anti-Pirandello rant"),
        ("Well then, we'll have it in the garden", "Act Three — directing the climax"),
    ],
    "Player 1": [
        ("What a spectacle. What an absolute treat", "Act One — at the family's arrival (Leading Man)"),
        ("It's absolutely unheard of", "Act One — outrage (Leading Man)"),
        ("I only let them in", "Act One curtain — as Door-keeper"),
    ],
    "Player 2": [
        ("A game! For heaven's sake", "Act Two — refusing the game (Leading Lady)"),
        ("Nobody has ever dared to laugh at me", "Act Two — wounded vanity (Leading Lady)"),
        ("One can't hear a word", "Act Two — during the shop scene (Leading Lady)"),
    ],
    "Player 3": [
        ("This is rank madness", "Act One — at the family's arrival (Juvenile Lead)"),
        ("I'm out of it anyway", "Act One — refusing the chaos (Juvenile Lead)"),
        ("And he takes them seriously", "Act One — disbelief (Juvenile Lead)"),
    ],
}

def find_speech_num(opener):
    """Return the speech number whose dialogue begins with `opener`."""
    for s in SPEECHES:
        if s['opener_plain'].startswith(opener):
            return s['num']
    return None

SCENE_INDEX = {}
for role, items in PICKS.items():
    resolved = []
    for opener, context in items:
        num = find_speech_num(opener)
        # Short fingerprint: first ~5 words of opener (for ctrl-F search)
        fp = ' '.join(opener.split()[:5])
        resolved.append({'num': num, 'context': context, 'fingerprint': fp})
    SCENE_INDEX[role] = resolved

# ===========================================================================
# Shared CSS for all three PDFs
# ===========================================================================
SHARED_CSS = """
  :root { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }
  @page { size: A4; margin: 22mm 20mm 22mm 20mm; }
  *,*::before,*::after { box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif; font-size: 11pt; line-height: 1.55; margin: 0; padding: 0; }
"""

# ===========================================================================
# PDF 1 — Trimmed audition packet (cover + summary + role cards + silent note)
# ===========================================================================
existing = (OUT_DIR / "audition_call.html").read_text()

# Remove the entire <section class="front">...</section>
trimmed = re.sub(r'<section class="front">.*?</section>', '', existing, count=1, flags=re.DOTALL)
# Cover eyebrow → simpler
trimmed = trimmed.replace(
    '<p class="cover-eyebrow">Audition Call · with sides</p>',
    '<p class="cover-eyebrow">Audition Call</p>'
).replace(
    '<p class="cover-eyebrow">Audition Packet · with sides</p>',
    '<p class="cover-eyebrow">Audition Call</p>'
)
# Drop the "sides follow on the next page" line and any sides-page sections
trimmed = re.sub(
    r'<p class="sides-note">Audition sides for this role follow on the next page\.</p>',
    '', trimmed
)
trimmed = re.sub(r'<section class="sides-page">.*?</section>', '', trimmed, flags=re.DOTALL)

# Replace "speeches" with "lines" in role-card stats
trimmed = trimmed.replace(
    '</strong> speeches</span>',
    '</strong> lines</span>'
)

# Inject a summary section right after the cover
SUMMARY_SECTION = """
  <section class="summary-page">
    <header class="summary-head">
      <p class="summary-eyebrow">Audition packet · summary</p>
      <h2>About this audition</h2>
    </header>

    <p>The Village Players, Lausanne, are casting Pirandello's metatheatrical comedy <em>Six Characters in Search of an Author</em> for a bold minimalist staging. Eight live performers carry the production. The first quarter of an hour is committed comedy. The last quarter of an hour is not.</p>

    <p>The play opens on a working theatre company at rehearsal — and is interrupted, in front of the audience, by six characters from an unfinished play, who arrive demanding to be staged. What follows is one long argument about whether the actors can play them, whether the play they carry is real enough to be staged, and what kind of reality a theatre can hold. By turns very funny and very dark.</p>

    <p>Our staging strips the stage to one visual element per act: a circle of chairs in Act One; a two-level set (rehearsal stage above, watching floor below) in Act Two; a single short fountain basin alone on stage in Act Three. The English of this version is contemporary, with the Step-Daughter's register pushed harder than polite English of a hundred years ago could carry. Comedy is in the working actors' bickering and in the Manager's increasing exhaustion. The tragedy belongs to the Six.</p>

    <h3 class="summary-sub">How to read what follows</h3>
    <p>For each of the eight casting tracks — four Characters, the Manager, three Players — this packet gives you a role card with the stats (lines and total word count across the production), a single paragraph of playing direction, a short cold-read line, and the audition scenes to prepare. The Boy and the Child, the two youngest of the Six, are not cast — they are objects on the stage (a coat-and-chair, a wrapped bundle) and appear only briefly in three short video projections. They are described at the end of the packet for reference.</p>
  </section>
"""

# Insert after the cover section's closing tag (the </section> that closes class="cover")
trimmed = re.sub(
    r'(<section class="cover">.*?</section>)',
    r'\1\n' + SUMMARY_SECTION,
    trimmed,
    count=1,
    flags=re.DOTALL
)

# Add summary-page styles by injecting before the </style> tag
SUMMARY_CSS = """
  .summary-page { max-width: 165mm; margin: 0 auto; page-break-after: always; padding-top: 4mm; }
  .summary-head { margin-bottom: 8mm; padding-bottom: 4mm; border-bottom: 1px solid var(--rule); }
  .summary-eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.20em; text-transform:uppercase; color:var(--accent); margin:0 0 2mm 0; }
  .summary-head h2 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size:26pt; margin:0; }
  .summary-page p { margin: 0 0 5mm 0; line-height: 1.7; font-size: 11.5pt; }
  .summary-sub { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.18em; text-transform:uppercase; color:var(--accent); margin: 8mm 0 3mm 0; }
"""
trimmed = trimmed.replace('</style>', SUMMARY_CSS + '\n</style>', 1)

(OUT_DIR / "audition_packet_trimmed.html").write_text(trimmed)

# ===========================================================================
# PDF 2 — Sides templates (8 one-page blanks)
# ===========================================================================
TEMPLATES_HEAD = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Sides Templates — Village Players</title>
<style>
{SHARED_CSS}
  .template-page {{ max-width:165mm; margin:0 auto; page-break-after:always; padding-top:4mm; }}
  .template-page:last-child {{ page-break-after:auto; }}
  .t-header {{ padding-bottom:5mm; border-bottom:1px solid var(--rule); margin-bottom:8mm; }}
  .t-eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.20em; text-transform:uppercase; color:var(--accent); margin:0 0 2mm 0; }}
  .t-header h2 {{ font-family:'Cormorant Garamond',serif; font-weight:500; font-size:28pt; margin:0; }}
  .t-tag {{ font-style:italic; color:var(--ink-soft); margin:1mm 0 3mm 0; font-size:11pt; }}
  .t-stats {{ font-size:10pt; color:var(--ink-soft); margin:0; font-variant-numeric:tabular-nums; }}
  .t-stats .dot {{ margin:0 3mm; }}

  .slot {{ margin-bottom:7mm; }}
  .slot-head {{ display:flex; align-items:baseline; gap:5mm; margin-bottom:3mm; }}
  .slot-num {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); }}
  .slot-label {{ font-style:italic; font-size:10pt; color:var(--ink-soft); }}
  .blank {{ height:42mm; border:1px solid var(--rule); border-radius:1mm;
            background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 6mm, var(--rule) 6mm, var(--rule) 6.1mm);
            background-position: 0 4mm; padding:3mm 4mm; }}
  .blank-label {{ font-size:8pt; color:var(--ink-soft); font-style:italic; letter-spacing:0.05em; }}
  .footer-note {{ margin-top:auto; padding-top:5mm; border-top:1px dotted var(--rule); font-size:9pt; color:var(--ink-soft); font-style:italic; }}
</style>
</head><body>
"""

def render_template(role_name):
    s = stats.get(role_name.replace(" (Leading Man)", "").replace(" (Door-keeper)", ""), {"speeches": 0, "words": 0})
    # Extract tag from the portrait
    m = re.search(
        r'<h3 class="p-name">' + re.escape(role_name) + r'</h3>\s*<span class="p-tag">([^<]+)</span>',
        src_html
    )
    tag = m.group(1) if m else ""
    return f"""
  <section class="template-page">
    <header class="t-header">
      <p class="t-eyebrow">Sides Template · paste or print below</p>
      <h2>{role_name}</h2>
      <p class="t-tag">{tag}</p>
      <p class="t-stats">
        <span><strong>{s['speeches']}</strong> lines</span><span class="dot">·</span>
        <span><strong>{s['words']:,}</strong> words across the production</span>
      </p>
    </header>

    <div class="slot">
      <div class="slot-head"><span class="slot-num">Side 1</span><span class="slot-label">scene title:</span></div>
      <div class="blank"><span class="blank-label">paste or write the speech here</span></div>
    </div>

    <div class="slot">
      <div class="slot-head"><span class="slot-num">Side 2</span><span class="slot-label">scene title:</span></div>
      <div class="blank"><span class="blank-label">paste or write the speech here</span></div>
    </div>

    <div class="slot">
      <div class="slot-head"><span class="slot-num">Side 3 (optional)</span><span class="slot-label">scene title:</span></div>
      <div class="blank"><span class="blank-label">paste or write the speech here</span></div>
    </div>

    <p class="footer-note">Cross-reference the <em>Scene Index</em> for the speech numbers to use, or pull directly from <em>six_characters_village_players.html</em>.</p>
  </section>
"""

TEMPLATE_HTML = TEMPLATES_HEAD + "".join(render_template(r) for r in [
    "The Father", "The Mother", "The Step-Daughter", "The Son",
    "The Manager", "Player 1", "Player 2", "Player 3"
]) + "</body></html>"

(OUT_DIR / "sides_templates.html").write_text(TEMPLATE_HTML)

# ===========================================================================
# PDF 3 — Scene index (one or two pages of pointers)
# ===========================================================================
INDEX_ROWS = []
for role, items in SCENE_INDEX.items():
    rows_html = []
    for it in items:
        num_display = f"#{it['num']}" if it['num'] else "—"
        rows_html.append(
            f'<tr><td class="ix-num">{num_display}</td>'
            f'<td class="ix-context">{it["context"]}</td>'
            f'<td class="ix-fp">&ldquo;{it["fingerprint"]}…&rdquo;</td></tr>'
        )
    INDEX_ROWS.append(f"""
    <section class="ix-role">
      <h3>{role}</h3>
      <table class="ix-table">
        <thead><tr><th>Line</th><th>Scene</th><th>Search hint</th></tr></thead>
        <tbody>
          {''.join(rows_html)}
        </tbody>
      </table>
    </section>
""")

INDEX_HTML = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Scene Index — Audition Sides Reference</title>
<style>
{SHARED_CSS}
  body {{ padding: 0; }}
  main {{ max-width:170mm; margin:0 auto; padding-top: 4mm; }}
  header.ix-head {{ margin-bottom:6mm; padding-bottom:4mm; border-bottom:1px solid var(--rule); }}
  .ix-eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.20em; text-transform:uppercase; color:var(--accent); margin:0 0 2mm 0; }}
  header.ix-head h1 {{ font-family:'Cormorant Garamond',serif; font-weight:500; font-size:24pt; margin:0 0 2mm 0; }}
  header.ix-head p {{ margin:0; font-style:italic; font-size:10pt; color:var(--ink-soft); }}

  .ix-role {{ margin-bottom:6mm; page-break-inside:avoid; }}
  .ix-role h3 {{ font-family:'Cormorant Garamond',serif; font-weight:500; font-size:14pt; margin:0 0 2mm 0; color:var(--ink); border-bottom:1px dotted var(--rule); padding-bottom:1mm; }}
  table.ix-table {{ width:100%; border-collapse:collapse; font-size:10pt; }}
  table.ix-table th {{ text-align:left; font-family:'Cormorant Unicase',serif; font-weight:600; font-size:8pt; letter-spacing:0.12em; text-transform:uppercase; color:var(--ink-soft); padding:1mm 4mm 1mm 0; border-bottom:1px solid var(--rule); }}
  table.ix-table td {{ padding:1.5mm 4mm 1.5mm 0; vertical-align:top; }}
  td.ix-num {{ font-variant-numeric:tabular-nums; font-weight:600; color:var(--accent); white-space:nowrap; width:18mm; }}
  td.ix-context {{ width:62mm; font-style:italic; color:var(--ink); }}
  td.ix-fp {{ color:var(--ink-soft); font-size:9.5pt; }}
  footer.ix-foot {{ margin-top:8mm; padding-top:4mm; border-top:1px solid var(--rule); font-size:9pt; color:var(--ink-soft); font-style:italic; }}
</style>
</head><body>
<main>
  <header class="ix-head">
    <p class="ix-eyebrow">Working reference · Audition sides</p>
    <h1>Scene Index — where to find each role's sides</h1>
    <p>Open <code>six_characters_village_players.html</code> and locate each line by number (count <code>p class="speech"</code> elements) or by the short search hint shown. Copy the line you choose into the matching slot in <em>sides_templates.pdf</em>.</p>
  </header>

  {''.join(INDEX_ROWS)}

  <footer class="ix-foot">
    <p>Line numbers reflect document order in <code>six_characters_village_players.html</code> at the time this index was generated. If you re-order or insert lines, regenerate the index.</p>
  </footer>
</main>
</body></html>
"""

(OUT_DIR / "scene_index.html").write_text(INDEX_HTML)

# ===========================================================================
# Render all three to PDF
# ===========================================================================
def render(html_path, pdf_path):
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page()
        page.goto(f"file://{Path(html_path).resolve()}", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(600)
        page.pdf(
            path=str(pdf_path), format="A4",
            margin={"top":"22mm","right":"20mm","bottom":"22mm","left":"20mm"},
            print_background=True, prefer_css_page_size=True,
        )
        browser.close()

render(OUT_DIR/"audition_packet_trimmed.html", OUT_DIR/"audition_packet_trimmed.pdf")
render(OUT_DIR/"sides_templates.html", OUT_DIR/"sides_templates.pdf")
render(OUT_DIR/"scene_index.html", OUT_DIR/"scene_index.pdf")

try:
    from pypdf import PdfReader
    for name in ["audition_packet_trimmed.pdf", "sides_templates.pdf", "scene_index.pdf"]:
        p = OUT_DIR / name
        r = PdfReader(str(p))
        print(f"  {name}: {p.stat().st_size:,} bytes · {len(r.pages)} pages")
except BaseException:
    for name in ["audition_packet_trimmed.pdf", "sides_templates.pdf", "scene_index.pdf"]:
        p = OUT_DIR / name
        print(f"  {name}: {p.stat().st_size:,} bytes")
