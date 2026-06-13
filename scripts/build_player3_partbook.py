#!/usr/bin/env python3
"""Build the Player 3 Part Book PDF.

A single actor's part book for Player 3: every line she speaks and every
action she performs, in performance order, grouped by act and by part.
Each of her speeches is preceded by a short CUE (the tail of the line
before hers) so the book is usable in the rehearsal room.

The text is extracted byte-identically from
six_characters_village_players.html, so the part book stays in sync with
the play the next time this script is run.

Run from the repo root:  python scripts/build_player3_partbook.py
"""
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("PLAY_SRC", HERE / "six_characters_village_players.html"))
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
CHROMIUM = os.environ.get("CHROMIUM_PATH")

src_html = SRC.read_text()

# Whose part book this is. Matched against the start of the bare speaker name,
# so "Player 3" also catches "Player 3 (as Prompter)".
ROLE = "Player 3"

# ---------------------------------------------------------------------------
# Parts — same boundaries as recount_stats.py: the chunk of each part is the
# stretch from just after its part-note </aside> to the next part-eyebrow or
# act curtain.
# ---------------------------------------------------------------------------

PARTS = [
    ("Act One", "Part I", "Part I of Act One", '<div class="part-eyebrow">Part II of Act One</div>'),
    ("Act One", "Part II", "Part II of Act One", '<div class="part-eyebrow">Part III of Act One</div>'),
    ("Act One", "Part III", "Part III of Act One", '<div class="curtain">— End of Act I —</div>'),
    ("Act Two", "Part I", "Part I of Act Two", '<div class="part-eyebrow">Part II of Act Two</div>'),
    ("Act Two", "Part II", "Part II of Act Two", '<div class="part-eyebrow">Part III of Act Two</div>'),
    ("Act Two", "Part III", "Part III of Act Two", '<div class="curtain">— End of Act II —</div>'),
    ("Act Three", "Part I", "Part I of Act Three", '<div class="part-eyebrow">Part II of Act Three</div>'),
    ("Act Three", "Part II", "Part II of Act Three", '<div class="part-eyebrow">Part III of Act Three</div>'),
    ("Act Three", "Part III", "Part III of Act Three", '<div class="curtain">Curtain.</div>'),
]


def part_bounds(eyebrow_text, end_marker):
    eb = re.search(re.escape(f'<div class="part-eyebrow">{eyebrow_text}</div>'), src_html)
    if not eb:
        return None
    aside_close = src_html.find('</aside>', eb.end())
    if aside_close == -1:
        return None
    end_idx = src_html.find(end_marker, aside_close)
    if end_idx == -1:
        return None
    return (aside_close + len('</aside>'), end_idx)


def part_title(eyebrow_text):
    """Pull the <h3 class="part-title"> that follows the part eyebrow."""
    eb = re.search(re.escape(f'<div class="part-eyebrow">{eyebrow_text}</div>'), src_html)
    if not eb:
        return ""
    m = re.search(r'<h3 class="part-title">(.*?)</h3>', src_html[eb.end():eb.end() + 400], re.DOTALL)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ""


# ---------------------------------------------------------------------------
# Speech helpers
# ---------------------------------------------------------------------------

def bare_speaker(block_html):
    m = re.search(r'<span class="speaker">(.*?)</span>(?:</span>)?', block_html, re.DOTALL)
    if not m:
        return ""
    return re.sub(r'<[^>]+>', '', m.group(0)).strip()


def as_role(block_html):
    m = re.search(r'<span class="as-role">\(as ([^<]+)\)</span>', block_html)
    return m.group(1).strip() if m else ""


def plain_text(block_html):
    """The spoken text, without the speaker label or the bracketed actions."""
    s = re.sub(r'<span class="speaker">.*?</span>(?:</span>)?\s*\.?\s*', '', block_html, count=1, flags=re.DOTALL)
    s = re.sub(r'<span class="action">.*?</span>', '', s, flags=re.DOTALL)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'^[\s\.,;:!?\-—…]+', '', s).strip()


def cue_tail(block_html, words=12):
    spk = bare_speaker(block_html)
    txt = plain_text(block_html)
    if not txt:
        return None
    parts = txt.split()
    tail = " ".join(parts[-words:])
    if len(parts) > words:
        tail = "… " + tail
    return spk, tail


BLOCK_RE = re.compile(r'<p class="(speech|stage)">(.*?)</p>', re.DOTALL)


def collect_part(chunk):
    """Return (entries, functions, n_speeches, n_words).

    entries: list of dicts — either {"kind":"cue", ...} paired with the
    following {"kind":"line", ...}, or {"kind":"stage", ...}.
    """
    entries = []
    functions = []
    n_speeches = 0
    n_words = 0
    prev_speech = None
    for m in BLOCK_RE.finditer(chunk):
        kind, inner = m.group(1), m.group(2)
        full = m.group(0)
        if kind == "speech":
            spk = bare_speaker(full)
            if spk.lower().startswith(ROLE.lower()):
                cue = cue_tail(prev_speech) if prev_speech else None
                role = as_role(full)
                if role and role not in functions:
                    functions.append(role)
                entries.append({"kind": "line", "html": full, "cue": cue})
                n_speeches += 1
                n_words += len(plain_text(full).split())
            prev_speech = full
        else:  # stage
            if re.search(rf'\b{re.escape(ROLE)}\b', re.sub(r'<[^>]+>', '', inner)):
                entries.append({"kind": "stage", "html": full})
    return entries, functions, n_speeches, n_words


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

style_match = re.search(r'<style[^>]*>(.*?)</style>', src_html, re.DOTALL)
PLAY_CSS = style_match.group(1) if style_match else ""

EXTRA_CSS = """
/* Player 3 Part Book — additions on top of the play stylesheet */
@page { size: A4; margin: 20mm 18mm 20mm 18mm; }
html, body { background: #efe6cf !important; color: #2a201a !important; }
body { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a;
       --rule:rgba(42,32,26,0.18); --suggest:#2d6373;
       font-family:'EB Garamond','Georgia','Times New Roman',serif; font-size:11pt; line-height:1.6; }
.r-controls, .r-progress, .r-act-pin { display:none !important; }
main.partbook { max-width: 170mm; margin: 0 auto; }

.cover { page-break-after: always; padding-top: 22mm; text-align:center; }
.cover .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.28em; text-transform:uppercase; color:var(--accent); margin:0 0 14mm 0; }
.cover h1 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size:40pt; line-height:1.0; margin:0 0 3mm 0; }
.cover .who { font-family:'Cormorant Garamond',serif; font-style:italic; font-size:15pt; color:var(--ink-soft); margin:0 0 12mm 0; }
.cover .play { font-style:italic; font-size:12pt; color:var(--ink-soft); margin:0 0 2mm 0; }
.cover .credit { font-size:11pt; margin:2mm 0; }
.cover .company { margin-top:12mm; font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.22em; text-transform:uppercase; }

.intro { page-break-after: always; }
.intro h2 { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:11pt; letter-spacing:0.2em; text-transform:uppercase; color:var(--accent); margin:7mm 0 3mm 0; }
.intro p { margin:0 0 3mm 0; }
.intro .funcs { margin:0 0 3mm 0; padding-left:6mm; }
.intro .funcs li { margin-bottom:1.5mm; }

.act-head { page-break-before: always; font-family:'Cormorant Garamond',serif; font-weight:500;
            font-size:26pt; color:var(--accent); border-bottom:2px solid var(--accent);
            margin:0 0 6mm 0; padding-bottom:2mm; }
.part-head { margin:8mm 0 4mm 0; }
.part-head .pp { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:12pt; letter-spacing:0.14em; text-transform:uppercase; color:var(--ink); }
.part-head .pt { font-family:'Cormorant Garamond',serif; font-style:italic; font-size:14pt; color:var(--ink-soft); margin-left:4mm; }
.part-meta { font-family:'Cormorant Unicase',serif; font-size:8.5pt; letter-spacing:0.1em; text-transform:uppercase; color:var(--ink-soft); margin:1mm 0 4mm 0; }
.part-meta.none { font-style:normal; }

.cue { font-size:9.5pt; color:var(--ink-soft); margin:4mm 0 0.5mm 0; padding-left:3mm; border-left:2px solid var(--rule); }
.cue .lab { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:8pt; letter-spacing:0.12em; text-transform:uppercase; color:var(--accent); margin-right:2mm; }
.cue .who { font-style:italic; }

/* her speeches reuse the play's .speech / .speaker / .as-role / .action styling */
.partbook .speech { margin:0.5mm 0 2mm 0; }
.partbook .stage { font-style:italic; color:var(--ink-soft); margin:3mm 0; }

footer.foot { margin-top:10mm; padding-top:4mm; border-top:1px solid var(--rule); font-size:9.5pt; color:var(--ink-soft); font-style:italic; text-align:center; }
"""

INTRO_HTML = """
<section class="intro">
  <h2>Who Player 3 is</h2>
  <p><strong>The youngest in the company, by a good ten years — early twenties, first proper season.</strong> She is the happiest person in the building; she still cannot quite believe she is being paid (a little) to spend her evenings inside a theatre. She does a bit of everything, and no job is beneath her, because all of it is theatre, and theatre is the thing she loves.</p>
  <p>Her dominant register is <em>curious</em>. Where Player 1 has opinions and Player 2 has shoulders, Player 3 has questions. <strong>The notebook is her tell:</strong> she writes everything down — and the moment she stops writing is the moment the play has stopped being a curiosity and become something she would rather not have on record.</p>
  <p><strong>Her arc:</strong> Act One, enthralled by the strangers and a little embarrassed by it — the one Player who says out loud that the Father <em>means</em> every word. Act Two, she stops nodding; the pencil goes still. Act Three, she is the conscience who asks whether someone should stop this, and waits, and is not answered. Her face is the audience's mirror at every horror in the second half.</p>

  <h2>The functions she carries</h2>
  <ul class="funcs">
    <li><strong>Juvenile Lead</strong> — eager, slightly ridiculous; she has been told she has "stage presence" and heard it as a promise.</li>
    <li><strong>Prompter</strong> — in the wooden box, frowning at the draught and the shorthand, pleased to be useful, compensating for her youth with seriousness.</li>
    <li><strong>An Actor</strong> and the <strong>Fifth Actor</strong> — she reads the small parts clean, no pretension, and looks to Player 2 to check she did it right.</li>
  </ul>

  <h2>How to read this book</h2>
  <p>Everything Player 3 says and does, in performance order, grouped by act and by part. Each of her speeches is preceded by a short <strong>CUE</strong> — the tail of the line before hers — so you can find your entrance. The function she is in (<em>as Prompter</em>, <em>as Juvenile Lead</em>) is printed beside each line. Her blocking lives in the bracketed action cues inside her speeches. The text is pulled byte-for-byte from the Director's Copy, so it always matches the current script.</p>
</section>
"""


def render():
    sections = []
    total_speeches = 0
    total_words = 0
    current_act = None
    for act, part, eyebrow, end_marker in PARTS:
        bounds = part_bounds(eyebrow, end_marker)
        if not bounds:
            print(f"  WARN: no bounds for {act} {part}")
            continue
        chunk = src_html[bounds[0]:bounds[1]]
        entries, functions, n_sp, n_wd = collect_part(chunk)
        total_speeches += n_sp
        total_words += n_wd

        if act != current_act:
            sections.append(f'<h2 class="act-head">{act}</h2>')
            current_act = act

        title = part_title(eyebrow)
        head = (f'<div class="part-head"><span class="pp">{part}</span>'
                f'<span class="pt">{title}</span></div>')
        if n_sp:
            funcs = ", ".join(functions) if functions else "as herself"
            meta = (f'<div class="part-meta">Player 3 here &middot; {n_sp} '
                    f'{"speech" if n_sp == 1 else "speeches"} &middot; {n_wd} words &middot; {funcs}</div>')
        else:
            meta = '<div class="part-meta none">Player 3 does not speak in this part — she is on the floor with the company, watching.</div>'

        body = []
        for e in entries:
            if e["kind"] == "stage":
                body.append(f'<p class="stage">{re.sub(r"^<p class=.stage.>|</p>$", "", e["html"])}</p>')
            else:
                if e["cue"]:
                    who, tail = e["cue"]
                    body.append(f'<p class="cue"><span class="lab">Cue</span>'
                                f'<span class="who">{who}:</span> {tail}</p>')
                body.append(e["html"])
        sections.append(head + meta + "".join(body))

    cover = f"""
    <section class="cover">
      <p class="eyebrow">Actor Part Book</p>
      <h1>Player 3</h1>
      <p class="who">the youngest in the company — Juvenile Lead, Prompter, and the small parts</p>
      <p class="play">Six Characters in Search of an Author</p>
      <p class="play">Sei personaggi in cerca d'autore &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
      <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne</p>
      <p class="credit">Director: <strong>Kiarash Jamshidi</strong></p>
      <p class="company">{total_speeches} speeches &middot; {total_words} words across the play</p>
    </section>
    """

    foot = ('<footer class="foot"><strong>Village Players &middot; Lausanne</strong> &nbsp;·&nbsp; '
            'Player 3 part book &nbsp;·&nbsp; lines and actions pulled from the Director\'s Copy.</footer>')

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Player 3 — Part Book</title>
<style>
{PLAY_CSS}
{EXTRA_CSS}
</style></head>
<body><main class="partbook">
{cover}
{INTRO_HTML}
{"".join(sections)}
{foot}
</main></body></html>
"""

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_html = OUT_DIR / "player3_part_book.html"
    out_html.write_text(html)
    print(f"Wrote {out_html.name} ({out_html.stat().st_size // 1024} KB) · "
          f"{total_speeches} speeches, {total_words} words")

    out_pdf = OUT_DIR / "player3_part_book.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page()
        page.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(700)
        page.pdf(path=str(out_pdf), format="A4",
                 margin={"top": "20mm", "right": "18mm", "bottom": "20mm", "left": "18mm"},
                 print_background=True, prefer_css_page_size=True)
        browser.close()
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    render()
