#!/usr/bin/env python3
"""Build the Blocking Storyboard PDF.

A beat-by-beat blocking book: for every part, each movement is one card —
a small top-down picture showing WHERE the move happens, paired with the
line from the script where it lands. No commentary; just the dialogue and
the picture. Opens with a "how to use it" page.

A4 portrait, cream full-bleed. Run: python scripts/build_blocking_storyboard.py
"""
import os
import math
from pathlib import Path
import _fullbleed

HERE = Path(__file__).resolve().parent.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

COL = {"F": "#8b3a3a", "M": "#2a201a", "SD": "#b03060", "S": "#2d6373",
       "MG": "#3a6b3a", "P1": "#c8781e", "P2": "#7a3f9c", "P3": "#1f8a8a",
       "MP": "#b8860b", "BOY": "#6b4a2a", "CHILD": "#a9762f"}

# mini-stage geometry
VW, VH = 240, 178
IX0, IY0, IX1, IY1 = 12, 26, 228, 162


def _xy(nx, ny):
    return (IX0 + nx / 100 * (IX1 - IX0), IY0 + ny / 100 * (IY1 - IY0))


def _dot(code, nx, ny):
    x, y = _xy(nx, ny)
    c = COL.get(code, "#555")
    if code in ("BOY", "CHILD"):
        if code == "BOY":
            return (f'<rect x="{x-9}" y="{y-9}" width="18" height="18" rx="2" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
                    f'<text x="{x}" y="{y+3.5}" text-anchor="middle" font-size="7.5" font-weight="700" fill="#fff" font-family="Arial">BOY</text>')
        return (f'<rect x="{x-8}" y="{y-8}" width="16" height="16" rx="7" transform="rotate(45 {x} {y})" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
                f'<text x="{x}" y="{y+3}" text-anchor="middle" font-size="6.5" font-weight="700" fill="#fff" font-family="Arial">CH</text>')
    return (f'<circle cx="{x}" cy="{y}" r="11" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
            f'<text x="{x}" y="{y+3.5}" text-anchor="middle" font-size="8" font-weight="700" fill="#fff" font-family="Arial">{code}</text>')


def _arrow(nx1, ny1, nx2, ny2, color="#8b3a3a"):
    x1, y1 = _xy(nx1, ny1); x2, y2 = _xy(nx2, ny2)
    ang = math.atan2(y2 - y1, x2 - x1)
    # shorten so the head sits at the target
    x2 -= 7 * math.cos(ang); y2 -= 7 * math.sin(ang)
    a1 = ang + math.radians(150); a2 = ang - math.radians(150)
    hx1, hy1 = x2 + 9 * math.cos(a1), y2 + 9 * math.sin(a1)
    hx2, hy2 = x2 + 9 * math.cos(a2), y2 + 9 * math.sin(a2)
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.4" '
            f'stroke-dasharray="2,5" stroke-linecap="round"/>'
            f'<polygon points="{x2},{y2} {hx1},{hy1} {hx2},{hy2}" fill="{color}"/>')


def _burst(nx, ny):
    x, y = _xy(nx, ny); pts = []
    for i in range(16):
        r = 13 if i % 2 == 0 else 6
        a = math.pi * i / 8
        pts.append(f"{x+r*math.cos(a):.0f},{y+r*math.sin(a):.0f}")
    return f'<polygon points="{" ".join(pts)}" fill="#8b3a3a" stroke="#fff" stroke-width="1"/>'


def _setpieces(act):
    s = [f'<rect x="{IX0}" y="{IY0}" width="{IX1-IX0}" height="{IY1-IY0}" rx="6" fill="#f4eeda" stroke="#8b3a3a" stroke-width="1.6"/>']
    if act == 1:
        cx, cy = _xy(50, 52)
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="40" ry="26" fill="none" stroke="#6b5b48" stroke-width="1.4" stroke-dasharray="3,3"/>')
        dx, dy = _xy(50, 0); s.append(f'<text x="{dx}" y="{IY0+11}" text-anchor="middle" font-size="8" fill="#6b5b48" font-family="serif">door ↑</text>')
    elif act == 2:
        px0, py0 = _xy(8, 4); px1, py1 = _xy(92, 50)
        s.append(f'<rect x="{px0}" y="{py0}" width="{px1-px0}" height="{py1-py0}" fill="#ece3c6" stroke="#8b3a3a" stroke-width="1.2" stroke-dasharray="3,3"/>')
        s.append(f'<text x="{(px0+px1)/2}" y="{py0+11}" text-anchor="middle" font-size="7.5" fill="#8b3a3a" font-family="serif">UPPER PLATFORM</text>')
        shx, shy0 = _xy(48, 8); _, shy1 = _xy(48, 50)
        s.append(f'<rect x="{shx-7}" y="{shy0}" width="14" height="{shy1-shy0}" fill="rgba(247,236,150,0.6)" stroke="#caa" stroke-width="0.7"/>')
        pnx, pny = _xy(12, 90); s.append(f'<rect x="{pnx-8}" y="{pny-7}" width="16" height="14" rx="2" fill="#888"/><text x="{pnx}" y="{pny+4}" text-anchor="middle" font-size="9" fill="#fff">♪</text>')
    else:
        cx, cy = _xy(50, 50)
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="22" fill="#dfeaf0" stroke="#2d6373" stroke-width="1.8"/>')
        s.append(f'<text x="{cx}" y="{cy+3}" text-anchor="middle" font-size="8" fill="#2d6373" font-family="serif">fountain</text>')
    return "".join(s)


def mini(act, marks, arrow=None, burst=None):
    body = _setpieces(act)
    if arrow:
        body += _arrow(*arrow)
    if burst:
        body += _burst(*burst)
    for m in marks:
        body += _dot(*m)
    body += (f'<text x="{(IX0+IX1)/2}" y="{IY1+13}" text-anchor="middle" font-size="7.5" '
             f'fill="#6b5b48" font-family="serif" font-style="italic">audience ↓</text>')
    return f'<svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


def who(name):
    return f'<span class="who">{name}</span>'
def sd(t):
    return f'<span class="sd">[{t}]</span>'


# ===========================================================================
# The beats — grouped by act and part. Each: (mini-svg, dialogue-html)
# ===========================================================================
def BEATS():
    return [
      ("Act One — The Family", [
        ("Part I — The Rehearsal", [
          (mini(1, [("MG",50,52)], arrow=(50,52,16,88,COL["MG"])),
           f'{who("The Manager")} {sd("throwing the morning&#39;s letter onto the table; he goes to his own chair, set apart")}. I can&#39;t see a thing in here. {sd("to Property Man")} A little light, please.'),
          (mini(1, [("P3",78,52)], arrow=(78,52,88,90,COL["P3"])),
           f'{who("Player 3")} {sd("as Prompter")}. Pardon, sir — may I get into my box? There&#39;s a draught off that door they still haven&#39;t mended.'),
          (mini(1, [("F",50,12),("M",62,12),("SD",74,14),("S",38,12),("BOY",16,46),("CHILD",84,16)],
                arrow=(50,4,16,46,COL["BOY"])),
           f'{sd("The white working lights soften to amber. The Door-keeper carries on the Boy-chair and sets it at the edge of the stage; the four live Characters — Father, Mother, Step-Daughter, Son — enter, and stop by the door at back; the Step-Daughter already carrying the Child-bundle")}.'),
        ]),
        ("Part II — The Interruption", [
          (mini(1, [("SD",50,40),("CHILD",60,40)], arrow=(50,40,50,82,COL["SD"])),
           f'{who("The Step-Daughter")}. With your permission, gentlemen, I, who am a two months&#39; orphan, will show you how well I can dance and sing. {sd("Sings and dances Prenez garde à Tchou-Tchin-Tchou")}.'),
          (mini(1, [("M",52,48),("CHILD",62,50),("BOY",44,52)]),
           f'{who("The Mother")} {sd("one arm tightens around the Child-bundle, the other goes toward the Boy-chair as if to keep both upright")}. In the name of these two little children, I beg you… {sd("She grows faint and is about to fall")} Oh God!'),
          (mini(1, [("F",46,48),("M",56,50)], arrow=(46,48,55,50,COL["F"]), burst=(58,50)),
           f'{who("The Father")} {sd("raising her veil")}. Let them see you!'),
          (mini(1, [("P1",48,46)], arrow=(48,46,12,86,COL["P1"])),
           f'{who("Player 1")} {sd("as Leading Man, beginning to relish it — then his eyes reach the Mother, and the rest does not arrive; the company recedes to the wings")}. What a spectacle. What an absolute…'),
        ]),
        ("Part III — The Bargain", [
          (mini(1, [("SD",50,55),("F",66,60)]),
           f'{who("The Step-Daughter")}. The room — I see it. Here is the window with the mantles, the divan, the looking-glass, a screen, and the little mahogany table with the blue envelope and its hundred francs. {sd("the Father sweats; the light drifts to deep red")}.'),
        ]),
      ]),
      ("Act Two — The Theatre", [
        ("Part I — The Setup", [
          (mini(2, [("SD",70,75)], arrow=(70,75,50,30,COL["SD"])),
           f'{sd("The Step-Daughter erupts from the lower floor onto the upper platform with the Child-bundle in her arms and the Boy-chair dragged behind her")}.'),
          (mini(2, [("SD",48,28),("CHILD",58,30),("BOY",64,30)], burst=(64,30)),
           f'{who("The Step-Daughter")} {sd("alone in the shower light; she turns to the coat on the Boy-chair and takes the revolver from its pocket")}.'),
        ]),
        ("Part II — The Apparition", [
          (mini(2, [("P2",55,70)], arrow=(55,70,60,18,COL["P2"])),
           f'{who("The Father")}. Would the ladies mind hanging their hats and mantles on the pegs at the back? {sd("the actresses climb to the platform; the pegs, the shop window, the screen are set")}.'),
          (mini(2, [("MP",50,16),("SD",50,30)], arrow=(50,4,50,16,COL["MP"])),
           f'{sd("The door at the back of stage opens and Madame Pace enters and takes a few steps forward")}.'),
          (mini(2, [("MP",46,28),("SD",54,30),("F",80,16)]),
           f'{sd("Madame Pace has placed one hand under the Step-Daughter&#39;s chin to raise her head; the Father waits behind the door")}.'),
          (mini(2, [("M",78,76)], arrow=(78,76,60,48,COL["M"])),
           f'{who("The Mother")} {sd("from the lower floor, erupting upward")}. You old devil! You murderess!'),
        ]),
        ("Part III — The Substitution", [
          (mini(2, [("P1",50,72)], arrow=(50,72,52,22,COL["P1"])),
           f'{sd("The door at the back opens and the Leading Man enters with the lively manner of an old gallant; the company replays the shop scene on the platform")}.'),
          (mini(2, [("P2",46,24),("P1",58,24),("M",78,76),("CHILD",86,78),("BOY",70,78)], burst=(78,60)),
           f'{who("The Step-Daughter")}. Cry out, mother. <em>Cry out as you did then!</em><br>{who("The Mother")} {sd("the shower falls on her on the lower floor")}. It&#39;s taking place now. It happens all the time.'),
          (mini(2, [("M",78,76)], burst=(50,50)),
           f'{sd("The Machinist drops the curtain by accident; the act ends not on a line but on the curtain&#39;s fall")}.'),
        ]),
      ]),
      ("Act Three — The Question", [
        ("Part I — The Trap", [
          (mini(3, [("F",62,62)], arrow=(62,62,50,90,COL["F"])),
           f'{who("The Father")} {sd("turns out toward the house; a pause long enough to feel")}. Can you tell me who you are?'),
        ]),
        ("Part II — The Refusal", [
          (mini(3, [("F",70,55),("S",82,40)], arrow=(70,55,80,42,COL["F"])),
           f'{who("The Father")} {sd("not leaving hold of the Son")}. You&#39;ve got to obey, do you hear?<br>{who("The Son")} {sd("the body refusing the cry; they separate")}. I won&#39;t do it. I won&#39;t.'),
        ]),
        ("Part III — The Fountain", [
          (mini(3, [("MG",40,78),("BOY",78,62)], arrow=(78,62,50,28,COL["MG"])),
           f'{who("The Manager")} {sd("he stands; he picks up the Boy-chair himself and walks it across the stage and places it behind the fountain basin")}.'),
          (mini(3, [("SD",70,70)], arrow=(70,70,55,52,COL["SD"])),
           f'{sd("The Step-Daughter bends over the basin and lowers the Child-bundle into it — the basin&#39;s walls hide the action")}.'),
          (mini(3, [("S",82,40)], arrow=(82,40,50,80,COL["S"]), burst=(50,30)),
           f'{who("The Son")} {sd("his one continuous sentence")}. I ran over to her… the boy, standing stock still, watching his little sister in the water. {sd("full blackout; a revolver shot rings out from behind the basin where the Boy-chair is")}.'),
          (mini(3, [("M",80,56),("CHILD",54,52),("BOY",50,28)], arrow=(80,56,56,40,COL["M"])),
           f'{who("The Mother")} {sd("she does not cry out at once — she reaches first for the Child-bundle in the basin, then the Boy-chair behind it; her arms cannot hold both, the veil still down")}. My son! My son!'),
          (mini(3, [("MG",45,72),("BOY",50,28)], arrow=(45,72,45,92,COL["MG"])),
           f'{who("The Manager")} {sd("a look at the empty Boy-chair; then he turns and leaves the stage the way a man leaves a theatre")}. Pretence? Reality? … To hell with it all.'),
        ]),
      ]),
    ]


def build():
    cards_html = []
    for act_title, parts in BEATS():
        cards_html.append(f'<h1 class="act">{act_title}</h1>')
        for part_title, beats in parts:
            cards_html.append(f'<h2 class="part">{part_title}</h2>')
            n = 1
            for svg, line in beats:
                cards_html.append(
                    f'<div class="beat"><div class="map"><span class="bn">{n}</span>{svg}</div>'
                    f'<div class="line">{line}</div></div>')
                n += 1
    body = "".join(cards_html)

    howto = '''
    <section class="howto">
      <h1 class="title">Blocking Storyboard</h1>
      <p class="sub">Every move in the show — the picture and the line it lands on. Six Characters in Search of an Author · Village Players, Lausanne · dir. Kiarash Jamshidi</p>
      <h3>How to use it</h3>
      <ul>
        <li><strong>One card = one move.</strong> Read the cards top to bottom, in order, act by act and part by part.</li>
        <li><strong>The picture is the stage seen from above</strong> — the audience sits at the bottom edge (↓). A dashed arrow shows the move; a burst marks a sudden event (a gunshot, the revolver, the veil).</li>
        <li><strong>The text beside it is the line from the script where the move happens</strong> — the spoken line and its stage direction, nothing added. If there is no move on a card, the position is what matters.</li>
        <li><strong>The dots are the people; the squares are the two stage objects</strong> (▢ the Boy-chair, ◇ the Child-bundle).</li>
      </ul>
      <div class="key">
        <span><b style="background:#8b3a3a">F</b> Father</span><span><b style="background:#2a201a">M</b> Mother</span>
        <span><b style="background:#b03060">SD</b> Step-Daughter</span><span><b style="background:#2d6373">S</b> Son</span>
        <span><b style="background:#3a6b3a">MG</b> Manager</span><span><b style="background:#c8781e">P1</b> Player 1</span>
        <span><b style="background:#7a3f9c">P2</b> Player 2</span><span><b style="background:#1f8a8a">P3</b> Player 3</span>
        <span><b style="background:#b8860b">MP</b> Madame Pace</span><span><b style="background:#6b4a2a">BOY</b> Boy-chair</span>
        <span><b style="background:#a9762f">CH</b> Child-bundle</span>
      </div>
    </section>'''

    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Blocking Storyboard — Six Characters</title>
<style>
@page {{ size: A4; margin: 13mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:11.5pt; }}
.howto {{ page-break-after: always; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:34pt; color:#8b3a3a; margin:0 0 2mm; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 7mm; font-size:12pt; }}
.howto h3 {{ font-family:'Cormorant Unicase',serif; font-size:12pt; letter-spacing:0.18em; text-transform:uppercase; color:#8b3a3a; margin:6mm 0 3mm; }}
.howto ul {{ padding-left:6mm; }} .howto li {{ margin-bottom:3mm; line-height:1.5; }}
.key {{ margin-top:8mm; display:flex; flex-wrap:wrap; gap:3mm 6mm; }}
.key span {{ font-size:11pt; display:flex; align-items:center; gap:2mm; }}
.key b {{ color:#fff; border-radius:50%; width:8mm; height:8mm; display:inline-flex; align-items:center;
  justify-content:center; font-size:8.5pt; font-family:Arial; }}
h1.act {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:24pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:4mm 0 3mm; padding-bottom:1mm; page-break-before:always; }}
h1.act:first-of-type {{ page-break-before:auto; }}
h2.part {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:12pt; letter-spacing:0.12em;
  text-transform:uppercase; color:#2a201a; margin:5mm 0 2mm; }}
.beat {{ display:flex; gap:6mm; align-items:flex-start; break-inside:avoid; page-break-inside:avoid;
  margin:0 0 3.5mm; padding-bottom:3.5mm; border-bottom:1px solid rgba(42,32,26,0.16); }}
.map {{ position:relative; flex:0 0 60mm; }}
.map svg {{ width:60mm; display:block; }}
.bn {{ position:absolute; top:-1mm; left:-1mm; background:#8b3a3a; color:#fff; width:6mm; height:6mm;
  border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:9pt; font-weight:700;
  font-family:Arial; z-index:2; }}
.line {{ flex:1; line-height:1.5; font-size:12pt; padding-top:1mm; }}
.line .who {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9.5pt; letter-spacing:0.08em;
  text-transform:uppercase; color:#8b3a3a; margin-right:1mm; }}
.line .sd {{ font-style:italic; color:#6b5b48; }}
</style></head><body>
{howto}
{body}
</body></html>"""

    html = _fullbleed.apply(html, top="13mm", side="13mm")
    out_html = OUT_DIR / "blocking_storyboard.html"
    out_html.write_text(html)
    out_pdf = OUT_DIR / "blocking_storyboard.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**launch_kwargs)
        pg = b.new_page()
        pg.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(700)
        pg.pdf(path=str(out_pdf), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    out_html.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
