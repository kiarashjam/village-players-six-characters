#!/usr/bin/env python3
"""Build an actor's Part Book for every speaking role.

For each of the nine speaking roles, a single PDF: every line that role
speaks and every action it performs, in performance order, grouped by act
and by part, each speech preceded by its CUE (the tail of the line
before it). The character intro is the portrait pulled from the
Director's Copy, so each book stays in sync with the play.

Output: outputs/<slug>_part_book.pdf for each role.

Run from the repo root:  python scripts/build_part_books.py
"""
import os
import re
from pathlib import Path
import _fullbleed

HERE = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("PLAY_SRC", HERE / "six_characters_village_players.html"))
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
CHROMIUM = os.environ.get("CHROMIUM_PATH")

src_html = SRC.read_text()

# ---------------------------------------------------------------------------
# Roles. "groups" are chorus/combined speaker tags this role is part of.
# ---------------------------------------------------------------------------
# Every line in the script is now spoken by a single named speaker; there are
# no chorus or combined-speaker tags left to fold in.
PLAYER_GROUPS = set()

ROLES = [
    {"name": "The Father", "slug": "father", "groups": set()},
    {"name": "The Mother", "slug": "mother", "groups": set()},
    {"name": "The Step-Daughter", "slug": "step_daughter", "groups": set()},
    {"name": "The Son", "slug": "son", "groups": set()},
    {"name": "The Manager", "slug": "manager", "groups": set()},
    {"name": "Player 1", "slug": "player1", "groups": PLAYER_GROUPS},
    {"name": "Player 2", "slug": "player2", "groups": PLAYER_GROUPS},
    {"name": "Player 3", "slug": "player3", "groups": PLAYER_GROUPS},
    {"name": "Madame Pace", "slug": "madame_pace", "groups": set()},
]

PARTS = [
    ("Act One — The Family", "Part I", "Part I of Act One", '<div class="part-eyebrow">Part II of Act One</div>'),
    ("Act One — The Family", "Part II", "Part II of Act One", '<div class="part-eyebrow">Part III of Act One</div>'),
    ("Act One — The Family", "Part III", "Part III of Act One", '<div class="curtain">— End of Act I —</div>'),
    ("Act Two — The Theatre", "Part I", "Part I of Act Two", '<div class="part-eyebrow">Part II of Act Two</div>'),
    ("Act Two — The Theatre", "Part II", "Part II of Act Two", '<div class="part-eyebrow">Part III of Act Two</div>'),
    ("Act Two — The Theatre", "Part III", "Part III of Act Two", '<div class="curtain">— End of Act II —</div>'),
    ("Act Three — The Question", "Part I", "Part I of Act Three", '<div class="part-eyebrow">Part II of Act Three</div>'),
    ("Act Three — The Question", "Part II", "Part II of Act Three", '<div class="part-eyebrow">Part III of Act Three</div>'),
    ("Act Three — The Question", "Part III", "Part III of Act Three", '<div class="curtain">Curtain.</div>'),
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
    eb = re.search(re.escape(f'<div class="part-eyebrow">{eyebrow_text}</div>'), src_html)
    if not eb:
        return ""
    m = re.search(r'<h3 class="part-title">(.*?)</h3>', src_html[eb.end():eb.end() + 400], re.DOTALL)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ""


def bare_speaker(block_html):
    m = re.search(r'<span class="speaker">(.*?)</span>(?:</span>)?', block_html, re.DOTALL)
    if not m:
        return ""
    return re.sub(r'<[^>]+>', '', m.group(0)).strip()


def plain_text(block_html):
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


def extract_portrait(name):
    """Return (tag, body_html) for a character's portrait in the play."""
    pattern = (
        r'<div class="portrait">\s*<div class="p-num">[^<]+</div>\s*'
        r'<h3 class="p-name">' + re.escape(name) + r'</h3>\s*'
        r'<span class="p-tag">([^<]+)</span>\s*(.*?)</div>'
    )
    m = re.search(pattern, src_html, re.DOTALL)
    if not m:
        return ("", "")
    return (m.group(1).strip(), m.group(2).strip())


def speaks(speaker, role):
    """Does this bare speaker belong to the role's part book?"""
    s = speaker.strip().lower()
    name = role["name"].lower()
    if name.startswith("player"):
        own = s.startswith(name)
    else:
        own = (s == name)
    return own or s in role["groups"]


BLOCK_RE = re.compile(r'<p class="(speech|stage)">(.*?)</p>', re.DOTALL)


def collect_part(chunk, role):
    entries, n_sp, n_wd = [], 0, 0
    prev_speech = None
    for m in BLOCK_RE.finditer(chunk):
        kind, full = m.group(1), m.group(0)
        if kind == "speech":
            if speaks(bare_speaker(full), role):
                entries.append({"kind": "line", "html": full,
                                "cue": cue_tail(prev_speech) if prev_speech else None})
                n_sp += 1
                n_wd += len(plain_text(full).split())
            prev_speech = full
        else:
            if re.search(rf'\b{re.escape(role["name"])}\b', re.sub(r'<[^>]+>', '', m.group(2))):
                entries.append({"kind": "stage", "html": full})
    return entries, n_sp, n_wd


# ---------------------------------------------------------------------------
# Style — fills the page (small margins, full-width column)
# ---------------------------------------------------------------------------

style_match = re.search(r'<style[^>]*>(.*?)</style>', src_html, re.DOTALL)
PLAY_CSS = style_match.group(1) if style_match else ""

EXTRA_CSS = """
/* Part Book — fills the page: tight margins, full-width column */
@page { size: A4; margin: 12mm 13mm 13mm 13mm; }
html, body { background: #efe6cf !important; color: #2a201a !important; }
body { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a;
       --rule:rgba(42,32,26,0.18); --suggest:#2d6373;
       font-family:'EB Garamond','Georgia','Times New Roman',serif; font-size:11.5pt; line-height:1.55; }
.r-controls, .r-progress, .r-act-pin { display:none !important; }
main.partbook { max-width: none; width: 100%; margin: 0; padding: 0; }

.cover { page-break-after: always; padding-top: 8mm; text-align:center; }
.cover .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.28em; text-transform:uppercase; color:var(--accent); margin:0 0 10mm 0; }
.cover h1 { font-family:'Cormorant Garamond',serif; font-weight:500; font-size:42pt; line-height:1.0; margin:0 0 3mm 0; }
.cover .who { font-family:'Cormorant Garamond',serif; font-style:italic; font-size:15pt; color:var(--ink-soft); margin:0 auto 10mm; max-width:150mm; }
.cover .play { font-style:italic; font-size:12pt; color:var(--ink-soft); margin:0 0 2mm 0; }
.cover .credit { font-size:11pt; margin:2mm 0; }
.cover .company { margin-top:10mm; font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10pt; letter-spacing:0.22em; text-transform:uppercase; }

.intro h2 { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:11pt; letter-spacing:0.2em; text-transform:uppercase; color:var(--accent); margin:7mm 0 3mm 0; }
.intro .portrait-body p { margin:0 0 3mm 0; line-height:1.6; }
.intro p { margin:0 0 3mm 0; }

.act-head { page-break-before: always; font-family:'Cormorant Garamond',serif; font-weight:500;
            font-size:26pt; color:var(--accent); border-bottom:2px solid var(--accent);
            margin:0 0 6mm 0; padding-bottom:2mm; }
.part-head { margin:8mm 0 3mm 0; }
.part-head .pp { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:12pt; letter-spacing:0.14em; text-transform:uppercase; color:var(--ink); }
.part-head .pt { font-family:'Cormorant Garamond',serif; font-style:italic; font-size:14pt; color:var(--ink-soft); margin-left:4mm; }
.part-meta { font-family:'Cormorant Unicase',serif; font-size:8.5pt; letter-spacing:0.1em; text-transform:uppercase; color:var(--ink-soft); margin:1mm 0 3mm 0; }

.cue { font-size:9.5pt; color:var(--ink-soft); margin:4mm 0 0.5mm 0; padding-left:3mm; border-left:2px solid var(--rule); }
.cue .lab { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:8pt; letter-spacing:0.12em; text-transform:uppercase; color:var(--accent); margin-right:2mm; }
.cue .who { font-style:italic; }

.partbook .speech { margin:0.5mm 0 2mm 0; }
.partbook .stage { font-style:italic; color:var(--ink-soft); margin:3mm 0; }

footer.foot { margin-top:9mm; padding-top:4mm; border-top:1px solid var(--rule); font-size:9.5pt; color:var(--ink-soft); font-style:italic; text-align:center; }
"""

SHOW_OPENING = """
  <h2>The play, and how it begins</h2>
  <p><strong>What it is.</strong> Pirandello's <em>Six Characters in Search of an Author</em> (1921). A theatre company's ordinary rehearsal is interrupted by six figures — a Father, a Mother, a Step-Daughter, a Son, and two silent children — who claim to be unfinished Characters, abandoned by their author, and demand that their drama be staged. The evening is the collision between their fixed, unbearable story and a working company's attempt to turn it into theatre.</p>
  <p><strong>This production.</strong> Set in Lausanne, played by <strong>nine live performers</strong> with <strong>two stage objects</strong> in place of the two youngest children (a coat-and-chair for the Boy, a wrapped bundle for the Child), on three stripped settings — <strong>no projection, no screen</strong>. One interval, after Act One; the second half plays unbroken to the fountain.</p>
  <p><strong>How it opens.</strong> The curtain is already up on a half-lit working stage. The Village Players are dragging themselves into a rehearsal of another Pirandello play, <em>Mixing It Up</em> — the Manager arrives tired and behind, there is the business of the cook's cap, the Players bicker. Then the working lights soften to a strange amber: Player 1 carries in the Boy-chair, and the four family Characters walk on, the Step-Daughter already holding the Child-bundle. From that entrance the play has begun, and it does not let go.</p>
"""

HOWTO = """
  <h2>How to read this book</h2>
  <p>Everything this role says and does, in performance order, grouped by act and by part. Each speech is preceded by a short <strong>CUE</strong> — the tail of the line before it — so you can find your entrance. Every line has a single named speaker, so there is never any doubt which of you speaks. Blocking lives in the bracketed action cues inside the speeches. The text is pulled byte-for-byte from the Director's Copy, so it always matches the current script.</p>
"""


def render_role(role):
    name = role["name"]
    tag, portrait_body = extract_portrait(name)
    sections, total_sp, total_wd = [], 0, 0
    current_act = None
    for act, part, eyebrow, end_marker in PARTS:
        b = part_bounds(eyebrow, end_marker)
        if not b:
            continue
        entries, n_sp, n_wd = collect_part(src_html[b[0]:b[1]], role)
        total_sp += n_sp
        total_wd += n_wd
        if act != current_act:
            sections.append(f'<h2 class="act-head">{act}</h2>')
            current_act = act
        title = part_title(eyebrow)
        head = f'<div class="part-head"><span class="pp">{part}</span><span class="pt">{title}</span></div>'
        if n_sp:
            meta = (f'<div class="part-meta">{n_sp} {"speech" if n_sp == 1 else "speeches"} '
                    f'&middot; {n_wd} words</div>')
        else:
            meta = f'<div class="part-meta">{name} does not speak in this part.</div>'
        body = []
        for e in entries:
            if e["kind"] == "stage":
                body.append(e["html"])
            else:
                if e["cue"]:
                    who, t = e["cue"]
                    body.append(f'<p class="cue"><span class="lab">Cue</span><span class="who">{who}:</span> {t}</p>')
                body.append(e["html"])
        sections.append(head + meta + "".join(body))

    cover = f"""
    <section class="cover">
      <p class="eyebrow">Actor Part Book</p>
      <h1>{name}</h1>
      <p class="who">{tag}</p>
      <p class="play">Six Characters in Search of an Author</p>
      <p class="play">Sei personaggi in cerca d'autore &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
      <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne</p>
      <p class="credit">Director: <strong>Kiarash Jamshidi</strong></p>
      <p class="company">{total_sp} speeches &middot; {total_wd} words across the play</p>
    </section>
    """
    intro = (f'<section class="intro"><h2>Who {name} is</h2>'
             f'<div class="portrait-body">{portrait_body}</div>'
             f'{SHOW_OPENING}{HOWTO}</section>')
    foot = (f'<footer class="foot"><strong>Village Players &middot; Lausanne</strong> &nbsp;·&nbsp; '
            f'{name} part book &nbsp;·&nbsp; lines and actions pulled from the Director\'s Copy.</footer>')

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{name} — Part Book</title>
<style>
{PLAY_CSS}
{EXTRA_CSS}
</style></head>
<body><main class="partbook">
{cover}
{intro}
{"".join(sections)}
{foot}
</main></body></html>
"""
    return html, total_sp, total_wd


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        browser = p.chromium.launch(**launch_kwargs)
        for role in ROLES:
            html, n_sp, n_wd = render_role(role)
            out_html = OUT_DIR / f"{role['slug']}_part_book.html"
            out_html.write_text(_fullbleed.apply(html))
            out_pdf = OUT_DIR / f"{role['slug']}_part_book.pdf"
            page = browser.new_page()
            page.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(500)
            page.pdf(path=str(out_pdf), format="A4", print_background=True, prefer_css_page_size=True)
            page.close()
            out_html.unlink(missing_ok=True)
            print(f"  {role['name']:20s} → {out_pdf.name}  ({n_sp} speeches, {n_wd} words, {out_pdf.stat().st_size//1024} KB)")
        browser.close()


if __name__ == "__main__":
    main()
