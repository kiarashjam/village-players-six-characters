#!/usr/bin/env python3
"""Build the FULL Blocking Storyboard PDF.

The complete play script, in order, with every blocking map dropped in
at the line where its move happens.  Lines that carry a move are shown
as a card (the top-down picture beside the verbatim line); every other
line of the script flows as ordinary script text — so the whole play is
present, not just the beats.

The maps, the lighting and the direction tags are reused verbatim from
build_blocking_storyboard.py; this script only weaves them into the
complete script harvested from the Director's Copy.

A4 portrait, cream full-bleed. Run: python scripts/build_blocking_storyboard_full.py
"""
import os
import re
import sys
import html as _html
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _fullbleed
from build_blocking_storyboard import BEATS

ROOT = HERE.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", ROOT / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")
SRC = ROOT / "six_characters_village_players.html"


# --------------------------------------------------------------------------
# 1. Harvest the complete script in document order, grouped into parts.
#    Each part carries its act name (from the eyebrow) and its elements.
# --------------------------------------------------------------------------
ACT_TITLE = {"Act One": "Act One — The Family",
             "Act Two": "Act Two — The Theatre",
             "Act Three": "Act Three — The Question"}


def harvest():
    src = SRC.read_text(encoding="utf-8")
    token = re.compile(
        r'<div class="part-eyebrow"[^>]*>(?P<eye>.*?)</div>'
        r'|<h3 class="part-title"[^>]*>(?P<part>.*?)</h3>'
        r'|<p class="speech">(?P<speech>.*?)</p>'
        r'|<p class="stage"[^>]*>(?P<stage>.*?)</p>', re.S)

    def txt(s):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

    seq = []            # list of {act, part, els:[ [kind,html,svgs], ... ]}
    pending_act = pending_no = None
    for m in token.finditer(src):
        if m.group("eye") is not None:
            e = txt(m.group("eye"))                       # "Part I of Act One"
            mm = re.match(r"(Part [IVX]+) of (Act \w+)", e)
            if mm:
                pending_no, pending_act = mm.group(1), mm.group(2)
        elif m.group("part") is not None:
            name = txt(m.group("part"))
            title = f"{pending_no} — {name}" if pending_no else name
            seq.append({"act": ACT_TITLE.get(pending_act, pending_act or ""),
                        "part": title, "els": []})
        elif not seq:
            continue
        elif m.group("speech") is not None:
            seq[-1]["els"].append(["speech", m.group("speech"), []])
        elif m.group("stage") is not None:
            seq[-1]["els"].append(["stage", m.group("stage"), []])
    return seq


def plain(inner):
    return _html.unescape(re.sub(r"<[^>]+>", " ", inner))


def norm(s):
    s = _html.unescape(s).lower()
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("—", "-"), ("–", "-"), ("…", "..."), ("œ", "oe")]:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


SHINGLE = 4


def shingles(words):
    if len(words) < SHINGLE:
        return {" ".join(words)} if words else set()
    return {" ".join(words[i:i + SHINGLE]) for i in range(len(words) - SHINGLE + 1)}


# --------------------------------------------------------------------------
# 2. From a beat's rendered line, derive candidate anchor phrases.
# --------------------------------------------------------------------------
def candidates(line):
    h = re.sub(r"</?em>", "", line)
    sds = re.findall(r'<span class="sd">(.*?)</span>', h, re.S)
    spoken = re.sub(r'<span class="(?:who|sd)">.*?</span>', "|", h, flags=re.S)
    spoken = _html.unescape(spoken)
    runs = [r.strip(" .:") for r in spoken.split("|")]
    cand = [r for r in runs if len(r) >= 12]
    cand += [_html.unescape(re.sub(r"<[^>]+>", "", s)).strip(" .[]") for s in sds]
    # longest first
    return sorted({c for c in cand if c}, key=len, reverse=True)


def beat_shingles(line):
    sh = set()
    for cand in candidates(line):
        sh |= shingles(norm(cand).split())
    return sh


def best_match(bsh, elem_sh, declared, used):
    """Index of the element with the most shingle overlap (prefer declared,
    unused), or None."""
    scored = [(len(bsh & s), i) for i, s in enumerate(elem_sh) if bsh & s]
    if not scored:
        return None
    top = max(ov for ov, _ in scored)
    best = [i for ov, i in scored if ov == top]
    for i in best:
        if i in declared and i not in used:
            return i
    for i in best:
        if i not in used:
            return i
    for i in best:
        if i in declared:
            return i
    return best[0]


# --------------------------------------------------------------------------
# 3. Render the script elements into our CSS.
# --------------------------------------------------------------------------
def render_speech(inner):
    h = inner.replace('<span class="speaker">', '<span class="who">')
    h = h.replace('<span class="action">', '<span class="sd">')
    return f'<p class="sp">{h}</p>'


def render_stage(inner):
    return f'<p class="stagedir">{inner}</p>'


def render_el(el):
    return render_speech(el[1]) if el[0] == "speech" else render_stage(el[1])


def build():
    seq = harvest()
    # Flatten elements into one global list; remember which part each belongs to.
    flat = []                       # (part_index, element)
    part_of = {}                    # global idx -> part_index
    for pi, p in enumerate(seq):
        for el in p["els"]:
            part_of[len(flat)] = pi
            flat.append(el)
    elem_sh = [shingles(norm(plain(el[1])).split()) for el in flat]

    # Map each part-title -> the global indices it contains (for "declared").
    part_idxs = {}
    for gi, pi in part_of.items():
        part_idxs.setdefault(seq[pi]["part"], set()).add(gi)

    used = set()
    misses = []
    for act_title, plist in BEATS():
        for part_title, beats in plist:
            declared = part_idxs.get(part_title, set())
            for svg, line in beats:
                gi = best_match(beat_shingles(line), elem_sh, declared, used)
                if gi is None:
                    misses.append((part_title, line[:70]))
                    continue
                used.add(gi)
                flat[gi][2].append(svg)

    # Render in true document order, with act/part headings.
    blocks = []
    last_act = None
    for p in seq:
        if p["act"] != last_act:
            blocks.append(f'<h1 class="act">{p["act"]}</h1>')
            last_act = p["act"]
        blocks.append(f'<h2 class="part">{p["part"]}</h2>')
        for el in p["els"]:
            if el[2]:
                maps = "".join(f'<div class="m1">{s}</div>' for s in el[2])
                blocks.append(
                    f'<div class="beat"><div class="map">{maps}</div>'
                    f'<div class="line">{render_el(el)}</div></div>')
            else:
                blocks.append(render_el(el))
    body = "".join(blocks)

    if misses:
        print(f"WARNING: {len(misses)} beats unmatched:")
        for p, l in misses:
            print("   ", p, "::", l)
    else:
        print(f"All {len(used)} beats matched to a script line.")

    howto = '''
    <section class="howto">
      <h1 class="title">Blocking Storyboard — Full Script</h1>
      <p class="sub">The complete play, in order, with every blocking map dropped in at the line where the move happens. Six Characters in Search of an Author · Village Players, Lausanne · dir. Kiarash Jamshidi</p>
      <h3>How to use it</h3>
      <ul>
        <li><strong>This is the whole script.</strong> Every line is here, act by act and part by part. Read it straight through.</li>
        <li><strong>Where a line carries a move</strong> it becomes a card: the top-down picture of the stage beside that line. Lines with no move flow as ordinary script.</li>
        <li><strong>The picture is the stage from above.</strong> Audience at the foot (↓ downstage). Everyone present is a labelled dot; the move runs from a <strong>solid dot</strong> along a <strong>dashed arrow</strong> to a <strong>hollow ring</strong>. A burst marks a sudden event.</li>
        <li><strong>Doors and light.</strong> Doors are labelled on the frame and entrances/exits name the direction (USC, SR, SL, downstage). The light cue is named top-right and the floor is tinted to match.</li>
      </ul>
      <h3>Orientation</h3>
      <p class="orient">Audience at the foot (downstage, DS); back wall at the top (upstage, US). The actors face the house, so stage-right (SR) is the <em>left</em> of the page and stage-left (SL) the right. USC = the door at back.</p>
      <h3>The light cues</h3>
      <div class="lkey">
        <span><b style="background:#7a7363">HALF-DARK</b> the bare work-light before the play</span>
        <span><b style="background:#6f6757">WORK LIGHT</b> full white rehearsal light</span>
        <span><b style="background:#b18a2c">REHEARSAL</b> the light for &ldquo;Mixing It Up&rdquo;</span>
        <span><b style="background:#cf8a2c">AMBER WASH</b> the tenuous light of the Six</span>
        <span><b style="background:#9c3a2a">DEEP RED</b> the cross to the office</span>
        <span><b style="background:#5d6e86">SHOWER</b> the overhead column on one figure</span>
        <span><b style="background:#8b3a3a">CURTAIN ↓ / ↑</b> the curtain falls / rises</span>
        <span><b style="background:#2d6373">FOUNTAIN + BULB</b> only the fountain and the bare bulb</span>
        <span><b style="background:#2a201a">BLACKOUT</b> full dark — the gunshot</span>
        <span><b style="background:#cf8a2c">LIGHTS SNAP UP</b> the snap back after the shot</span>
      </div>
      <h3>Who is who</h3>
      <div class="key">
        <span><b style="background:#8b3a3a">F</b> Father</span><span><b style="background:#2a201a">M</b> Mother</span>
        <span><b style="background:#b03060">SD</b> Step-Daughter</span><span><b style="background:#2d6373">S</b> Son</span>
        <span><b style="background:#3a6b3a">MG</b> Manager</span><span><b style="background:#c8781e">P1</b> Player 1</span>
        <span><b style="background:#7a3f9c">P2</b> Player 2</span><span><b style="background:#1f8a8a">P3</b> Player 3</span>
        <span><b style="background:#b8860b">MP</b> Madame Pace</span><span><b style="background:#6b4a2a">BOY</b> Boy-chair</span>
        <span><b style="background:#a9762f">CH</b> Child-bundle</span>
      </div>
    </section>'''

    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Blocking Storyboard — Full Script</title>
<style>
@page {{ size: A4; margin: 13mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:10.5pt; }}
.howto {{ page-break-after: always; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:30pt; color:#8b3a3a; margin:0 0 2mm; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 6mm; font-size:11.5pt; }}
.howto h3 {{ font-family:'Cormorant Unicase',serif; font-size:11.5pt; letter-spacing:0.18em; text-transform:uppercase; color:#8b3a3a; margin:5mm 0 2.5mm; }}
.howto ul {{ padding-left:6mm; margin:0; }} .howto li {{ margin-bottom:2.2mm; line-height:1.4; }}
.orient {{ margin:0; line-height:1.4; }}
.lkey {{ display:flex; flex-direction:column; gap:1.4mm; }}
.lkey span {{ font-size:9.5pt; display:flex; align-items:baseline; gap:3mm; }}
.lkey b {{ color:#fff; border-radius:3px; padding:0.6mm 2mm; font-size:7pt; font-family:Arial; font-weight:700;
  letter-spacing:0.4px; flex:0 0 30mm; text-align:center; white-space:nowrap; }}
.key {{ margin-top:2mm; display:flex; flex-wrap:wrap; gap:2.5mm 6mm; }}
.key span {{ font-size:10.5pt; display:flex; align-items:center; gap:2mm; }}
.key b {{ color:#fff; border-radius:50%; width:7.5mm; height:7.5mm; display:inline-flex; align-items:center;
  justify-content:center; font-size:8pt; font-family:Arial; }}
h1.act {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:22pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:4mm 0 3mm; padding-bottom:1mm; page-break-before:always; }}
h2.part {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:11pt; letter-spacing:0.12em;
  text-transform:uppercase; color:#2a201a; margin:5mm 0 2.5mm; break-after:avoid; }}
.sp {{ margin:0 0 2.1mm; line-height:1.48; }}
.who {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.07em;
  text-transform:uppercase; color:#8b3a3a; }}
.sd {{ font-style:italic; color:#6b5b48; }}
.stagedir {{ font-style:italic; color:#5d513f; margin:2.6mm 7mm; line-height:1.42; }}
.beat {{ display:flex; gap:5mm; align-items:flex-start; break-inside:avoid; page-break-inside:avoid;
  margin:2mm 0; padding:2mm 0; border-top:1px solid rgba(42,32,26,0.14); border-bottom:1px solid rgba(42,32,26,0.14); }}
.map {{ flex:0 0 58mm; }} .map svg {{ width:58mm; display:block; }}
.map .m1 + .m1 {{ margin-top:2mm; }}
.line {{ flex:1; }} .line .sp, .line .stagedir {{ margin:0; }}
</style></head><body>
{howto}
{body}
</body></html>"""

    doc = _fullbleed.apply(doc, top="13mm", side="13mm")
    out_html = OUT_DIR / "blocking_storyboard_full.html"
    out_html.write_text(doc)
    out_pdf = OUT_DIR / "blocking_storyboard_full.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**launch_kwargs)
        pg = b.new_page()
        pg.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=90000)
        pg.wait_for_timeout(800)
        pg.pdf(path=str(out_pdf), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    out_html.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
