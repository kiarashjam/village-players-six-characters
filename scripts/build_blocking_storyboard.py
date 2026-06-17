#!/usr/bin/env python3
"""Build the Blocking Storyboard PDF.

A beat-by-beat blocking book: for every part, each movement is one card —
a top-down picture showing WHERE it happens (everyone present is placed;
the move is drawn from a solid start dot, along a dashed arrow, to a
hollow destination ring) paired with the line from the script where it
lands. No commentary; just the dialogue and the picture. Opens with a
"how to use it" page.

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

VW, VH = 250, 188
IX0, IY0, IX1, IY1 = 12, 26, 238, 168


def _xy(nx, ny):
    return (IX0 + nx / 100 * (IX1 - IX0), IY0 + ny / 100 * (IY1 - IY0))


def _dot(code, nx, ny, r=10.5):
    x, y = _xy(nx, ny); c = COL.get(code, "#555")
    if code == "BOY":
        return (f'<rect x="{x-9}" y="{y-9}" width="18" height="18" rx="2" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
                f'<text x="{x}" y="{y+3.5}" text-anchor="middle" font-size="7" font-weight="700" fill="#fff" font-family="Arial">BOY</text>')
    if code == "CHILD":
        return (f'<rect x="{x-8}" y="{y-8}" width="16" height="16" rx="7" transform="rotate(45 {x} {y})" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
                f'<text x="{x}" y="{y+3}" text-anchor="middle" font-size="6.5" font-weight="700" fill="#fff" font-family="Arial">CH</text>')
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
            f'<text x="{x}" y="{y+3.3}" text-anchor="middle" font-size="7.6" font-weight="700" fill="#fff" font-family="Arial">{code}</text>')


def _ring(code, nx, ny, color):
    x, y = _xy(nx, ny)
    return (f'<circle cx="{x}" cy="{y}" r="10.5" fill="#f4eeda" fill-opacity="0.55" stroke="{color}" '
            f'stroke-width="1.6" stroke-dasharray="2.5,2"/>'
            f'<text x="{x}" y="{y+3.3}" text-anchor="middle" font-size="7.4" font-weight="700" fill="{color}" font-family="Arial">{code}</text>')


def _arrow(nx1, ny1, nx2, ny2, color):
    x1, y1 = _xy(nx1, ny1); x2, y2 = _xy(nx2, ny2)
    ang = math.atan2(y2 - y1, x2 - x1)
    sx, sy = x1 + 12 * math.cos(ang), y1 + 12 * math.sin(ang)
    ex, ey = x2 - 13 * math.cos(ang), y2 - 13 * math.sin(ang)
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    h1 = f"{ex+9*math.cos(a1):.1f},{ey+9*math.sin(a1):.1f}"
    h2 = f"{ex+9*math.cos(a2):.1f},{ey+9*math.sin(a2):.1f}"
    return (f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{color}" '
            f'stroke-width="2.3" stroke-dasharray="2,4.5" stroke-linecap="round"/>'
            f'<polygon points="{ex:.1f},{ey:.1f} {h1} {h2}" fill="{color}"/>')


def _burst(nx, ny):
    x, y = _xy(nx, ny); pts = []
    for i in range(16):
        r = 12 if i % 2 == 0 else 5.5
        a = math.pi * i / 8
        pts.append(f"{x+r*math.cos(a):.0f},{y+r*math.sin(a):.0f}")
    return f'<polygon points="{" ".join(pts)}" fill="#8b3a3a" stroke="#fff" stroke-width="1"/>'


def _setpieces(act):
    s = [f'<rect x="{IX0}" y="{IY0}" width="{IX1-IX0}" height="{IY1-IY0}" rx="6" fill="#f4eeda" stroke="#8b3a3a" stroke-width="1.6"/>']
    if act == 1:
        cx, cy = _xy(50, 50)
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="42" ry="27" fill="none" stroke="#c9bfa6" stroke-width="1.2"/>')
        for i in range(7):
            a = 2*math.pi*i/7 - math.pi/2
            chx, chy = cx + 42*math.cos(a), cy + 27*math.sin(a)
            s.append(f'<rect x="{chx-3.5}" y="{chy-3.5}" width="7" height="7" rx="1" fill="none" stroke="#b3a888" stroke-width="1.1"/>')
        s.append(f'<text x="{_xy(50,0)[0]}" y="{IY0+10}" text-anchor="middle" font-size="7.5" fill="#6b5b48" font-family="serif">door ↑</text>')
    elif act == 2:
        px0, py0 = _xy(7, 4); px1, py1 = _xy(93, 49)
        s.append(f'<rect x="{px0}" y="{py0}" width="{px1-px0}" height="{py1-py0}" fill="#ece3c6" stroke="#8b3a3a" stroke-width="1.1" stroke-dasharray="3,3"/>')
        s.append(f'<text x="{(px0+px1)/2}" y="{py0+10}" text-anchor="middle" font-size="7" fill="#8b3a3a" font-family="serif">UPPER PLATFORM (rehearsal stage)</text>')
        s.append(f'<text x="{(px0+px1)/2}" y="{_xy(50,95)[1]}" text-anchor="middle" font-size="7" fill="#6b5b48" font-family="serif">LOWER FLOOR (watching)</text>')
        shx, shy0 = _xy(47, 9); _, shy1 = _xy(47, 49)
        s.append(f'<rect x="{shx-7}" y="{shy0}" width="14" height="{shy1-shy0}" fill="rgba(247,236,150,0.6)" stroke="#caa" stroke-width="0.6"/>')
        s.append(f'<text x="{shx}" y="{shy0+9}" text-anchor="middle" font-size="6.2" fill="#9a8" font-family="serif">shower</text>')
        pnx, pny = _xy(11, 90); s.append(f'<rect x="{pnx-8}" y="{pny-7}" width="16" height="14" rx="2" fill="#888"/><text x="{pnx}" y="{pny+4}" text-anchor="middle" font-size="9" fill="#fff">♪</text>')
        s.append(f'<text x="{_xy(50,0)[0]}" y="{IY0+10}" text-anchor="middle" font-size="7.5" fill="#6b5b48" font-family="serif">door ↑</text>')
    else:
        cx, cy = _xy(50, 50)
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="33" ry="21" fill="#dfeaf0" stroke="#2d6373" stroke-width="1.8"/>')
        s.append(f'<text x="{cx}" y="{cy+3}" text-anchor="middle" font-size="7.5" fill="#2d6373" font-family="serif">fountain</text>')
    return "".join(s)


def mini(act, statics, mover=None, burst=None):
    body = _setpieces(act)
    if mover:
        code, x1, y1, x2, y2 = mover; c = COL.get(code, "#8b3a3a")
        body += _arrow(x1, y1, x2, y2, c)
    if burst:
        body += _burst(*burst)
    for m in statics:
        body += _dot(*m)
    if mover:
        code, x1, y1, x2, y2 = mover; c = COL.get(code, "#8b3a3a")
        body += _dot(code, x1, y1) + _ring(code, x2, y2, c)
    body += (f'<text x="{(IX0+IX1)/2}" y="{IY1+13}" text-anchor="middle" font-size="7.5" '
             f'fill="#6b5b48" font-family="serif" font-style="italic">audience ↓</text>')
    return f'<svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


def who(name):
    return f'<span class="who">{name}</span>'
def sd(t):
    return f'<span class="sd">[{t}]</span>'


# ===========================================================================
# Beats — grouped by act and part.  beat = (mini-svg, dialogue-html)
# ===========================================================================
def BEATS():
    A1, A2, A3 = 1, 2, 3
    return [
      ("Act One — The Family", [
        ("Part I — The Rehearsal", [
          (mini(A1, [("P1",44,46),("P2",60,44),("P3",84,86)], mover=("MG",50,6,20,82)),
           f'{who("The Manager")} {sd("entering with the weariness of a man who has run the company too long; he goes to his own chair, set apart")}. I can&#39;t see a thing in here. {sd("to the Property Man")} A little light, please.'),
          (mini(A1, [("MG",20,82),("P2",60,44),("P1",46,48)], mover=("P3",70,60,86,86)),
           f'{who("Player 1")} {sd("as Leading Man")}. Excuse me, but must I absolutely wear a cook&#39;s cap? {who("Player 3")} {sd("as Prompter, getting into the box")}. Pardon, sir — may I get into my box?'),
          (mini(A1, [("MG",20,82),("P1",44,48),("P2",60,46),("P3",84,86)],
                mover=("BOY",50,4,16,46)),
           f'{sd("The white working lights soften to amber. The Door-keeper carries on the Boy-chair and sets it at the edge of the stage; the four live Characters — Father, Mother, Step-Daughter, Son — enter and stop by the door at back, the Step-Daughter carrying the Child-bundle")}.'),
        ]),
        ("Part II — The Interruption", [
          (mini(A1, [("M",58,12),("SD",68,14),("S",40,12),("BOY",16,46),("CHILD",78,14),("MG",20,82)],
                mover=("F",50,12,48,40)),
           f'{who("The Father")} {sd("coming forward, the others following, embarrassed")}. No, for Heaven&#39;s sake, what are you saying? We bring you a drama, sir.'),
          (mini(A1, [("F",48,42),("M",60,20),("S",38,18),("CHILD",70,18),("MG",22,80)],
                mover=("SD",70,22,54,46)),
           f'{who("The Step-Daughter")} {sd("crossing behind the Father; a hand on his shoulder, left one beat too long, then withdrawn")}. My passion, sir. Ah, if you only knew — my passion for <em>him</em>.'),
          (mini(A1, [("F",46,40),("M",62,22),("S",36,20),("CHILD",54,40),("MG",22,80),("P1",30,60),("P2",74,58)],
                mover=("SD",54,42,52,84)),
           f'{who("The Step-Daughter")}. I, who am a two months&#39; orphan, will show you how well I can dance and sing. {sd("Sings and dances Prenez garde à Tchou-Tchin-Tchou")}.'),
          (mini(A1, [("F",40,44),("SD",54,80),("S",34,22),("BOY",44,52),("MG",22,80)],
                mover=None, burst=None),
           f'{who("The Mother")} {sd("one arm tightening round the Child-bundle, the other reaching for the Boy-chair, as if to hold both upright")}. In the name of these two little children, I beg you… {sd("she grows faint")} Oh God!'),
          (mini(A1, [("M",56,50),("S",34,24),("SD",60,70),("CHILD",62,52),("BOY",44,52)],
                mover=("F",40,46,53,50), burst=(58,50)),
           f'{who("The Father")} {sd("raising her veil")}. Let them see you!'),
          (mini(A1, [("M",56,50),("F",46,50),("SD",58,66),("P2",70,46)],
                mover=("P1",48,44,12,84)),
           f'{who("Player 1")} {sd("as Leading Man, beginning to relish it — then his eyes reach the Mother, and the rest does not arrive; the company drifts to the wings to watch")}. What a spectacle. What an absolute…'),
        ]),
        ("Part III — The Bargain", [
          (mini(A1, [("F",50,52),("SD",62,56),("M",70,60),("S",30,30),("CHILD",76,60)],
                mover=None),
           f'{who("The Step-Daughter")}. The room — I see it. The window with the mantles, the divan, the looking-glass, a screen, and the little mahogany table with the blue envelope and its hundred francs.'),
          (mini(A1, [("P1",30,56),("P2",46,56),("P3",62,58)],
                mover=("MG",40,60,86,40)),
           f'{who("The Manager")} {sd("hooked, leading the Father and the Six off to his office to concert the scene")}. Come with me to my office. In a quarter of an hour, all back here again. {sd("Manager and the Six cross the stage and go off; the light has drifted to deep red")}.'),
        ]),
      ]),
      ("Act Two — The Theatre", [
        ("Part I — The Setup", [
          (mini(A2, [("MG",30,82),("P1",46,84),("P2",58,84),("CHILD",70,60),("BOY",78,62)],
                mover=("SD",78,60,52,32)),
           f'{who("The Step-Daughter")} {sd("comes out of the office carrying the Child-bundle and dragging the Boy-chair, and goes quickly up onto the platform")}. Come on, Rosetta, let&#39;s run!'),
          (mini(A2, [("CHILD",54,30),("BOY",64,32)],
                mover=("SD",60,40,48,28)),
           f'{sd("She drags the Boy-chair a little behind her and leaves it leaning; the stage darkens; the shower — a tight column of light — falls on her alone")}.'),
          (mini(A2, [("SD",48,28),("CHILD",44,30),("BOY",62,30)], burst=(62,30)),
           f'{who("The Step-Daughter")} {sd("bending over the Child-bundle, then turning to the coat on the Boy-chair; she takes the revolver from its pocket")}.'),
          (mini(A2, [("S",80,80),("CHILD",70,72)],
                mover=("M",74,76,68,66)),
           f'{who("The Mother")} {sd("rises; one step toward the Son")}. My son — {sd("the Son turns away before the word is finished; she stops, and the unfinished word stays in the air")}.'),
        ]),
        ("Part II — The Apparition", [
          (mini(A2, [("F",70,40),("MG",30,82),("P1",46,84),("SD",60,40)],
                mover=("P2",58,76,64,18)),
           f'{who("The Father")}. Would the ladies mind hanging their hats and mantles on the pegs at the back? {sd("the actresses climb to the platform; the shop window and the screen are set")}.'),
          (mini(A2, [("SD",52,34),("F",80,16),("MG",30,82),("P1",46,84),("P2",62,82)],
                mover=("MP",50,4,48,18)),
           f'{sd("The door at the back of stage opens and Madame Pace enters and takes a few steps forward — fat, bleach-blonde, the silver chain at her waist")}.'),
          (mini(A2, [("MP",48,18),("F",80,16)],
                mover=("SD",60,40,52,24)),
           f'{who("The Step-Daughter")} {sd("running over to her")}. There she is! There she is!'),
          (mini(A2, [("MP",46,24),("SD",54,26),("F",80,16),("CHILD",40,30)], mover=None),
           f'{sd("Madame Pace places one hand under the Step-Daughter&#39;s chin to raise her head")}. {who("Madame Pace")}. Good morning, good morning, sir! Madame Pace, sir — dresses and coats, off the rue de Bourg.'),
          (mini(A2, [("MP",48,26),("SD",56,26),("F",78,18),("P1",40,84),("P2",58,84)],
                mover=("M",78,78,58,48), burst=None),
           f'{who("The Mother")} {sd("jumping up amid the consternation of the actors — the voice she has not used for years")}. You old devil! You murderess!'),
          (mini(A2, [("M",60,52),("MP",48,26),("F",78,18)],
                mover=("SD",54,28,62,48)),
           f'{who("The Step-Daughter")} {sd("running over to calm her Mother")}. Calm yourself, Mother, calm yourself! Please don&#39;t…'),
          (mini(A2, [("M",62,60),("SD",56,52),("CHILD",70,62)],
                mover=("MG",32,82,58,64)),
           f'{who("The Manager")} {sd("leading her to her chair")}. Come along, my dear lady, sit down now, and let&#39;s get on with the scene.'),
        ]),
        ("Part III — The Substitution", [
          (mini(A2, [("MG",30,82),("SD",62,40),("P1",48,84)],
                mover=("P2",60,82,52,24)),
           f'{who("Player 2")} {sd("as Leading Lady; goes to the hat-rack, puts her hat on, and takes the platform to play the Step-Daughter")}. One minute. I want to put my hat on again.'),
          (mini(A2, [("P2",54,26),("SD",66,40),("MG",30,82)],
                mover=("P1",50,4,46,26)),
           f'{sd("The door at rear opens and the Leading Man enters with the lively manner of an old gallant")}. {who("Player 1")} {sd("as Leading Man")}. Good afternoon, Miss.'),
          (mini(A2, [("P1",46,26),("P2",54,26),("MG",30,82)],
                mover=("SD",66,40,58,34)),
           f'{who("The Step-Daughter")} {sd("bursting out laughing, then advancing toward the actors")}. He didn&#39;t say &ldquo;I&#39;m frightfully sorry.&rdquo; He said &ldquo;Oh.&rdquo;'),
          (mini(A2, [("P1",46,26),("SD",58,34),("MG",30,82)],
                mover=("P2",54,26,90,20)),
           f'{who("Player 2")} {sd("the diva&#39;s posture going from offended to leaving")}. I am not going to stand here being made a fool of by that woman.'),
          (mini(A2, [("SD",54,30),("F",60,30),("CHILD",80,76),("BOY",70,76)],
                mover=("M",78,76,60,50), burst=(60,52)),
           f'{who("The Step-Daughter")}. Cry out, mother. <em>Cry out as you did then!</em> {who("The Mother")} {sd("coming forward to separate them; the shower falls on her")}. No! My daughter, my daughter! You brute!'),
          (mini(A2, [("M",60,52),("SD",56,40),("F",64,40),("P1",44,84)], burst=(50,46)),
           f'{who("The Mother")}. It&#39;s taking place now. It happens all the time. {sd("the piano cuts out; the Machinist drops the curtain by accident — the act ends on the curtain&#39;s fall")}.'),
        ]),
      ]),
      ("Act Three — The Question", [
        ("Part I — The Trap", [
          (mini(A3, [("M",80,58),("CHILD",88,60),("BOY",72,62),("S",86,38),("F",78,72),("SD",68,72),
                     ("P1",14,52),("P2",14,64),("P3",14,76),("MG",42,80)], mover=None),
           f'{sd("Curtain up on the bare stage and the fountain. The family sit stage-right, the company stage-left; the Manager stands centre, hand over his mouth, meditating")}. {who("The Manager")}. Ah yes: the second act!'),
          (mini(A3, [("MG",42,72),("SD",66,70),("M",80,58),("S",86,38)],
                mover=("F",66,60,52,88)),
           f'{who("The Father")} {sd("turning out toward the house; a pause long enough to feel")}. Can you tell me who you are?'),
          (mini(A3, [("F",55,66),("MG",42,74),("M",80,58)],
                mover=None),
           f'{who("The Step-Daughter")} {sd("level, never raised — colder than the philosophy")}. His <em>reality</em>. He always knew exactly where to find me.'),
        ]),
        ("Part II — The Refusal", [
          (mini(A3, [("M",80,58),("MG",42,76),("SD",66,72),("CHILD",88,60)],
                mover=("F",62,58,80,42)),
           f'{who("The Father")} {sd("seizing the Son, not leaving hold")}. You&#39;ve got to obey, do you hear?'),
          (mini(A3, [("F",70,52),("M",80,60),("MG",42,76)],
                mover=("S",80,42,86,30)),
           f'{who("The Son")} {sd("the voice cracking, the body refusing the cry; they separate")}. What does it mean — this madness you&#39;ve got? I won&#39;t do it. I won&#39;t.'),
          (mini(A3, [("S",86,30),("F",70,54),("SD",66,72)],
                mover=("M",80,60,80,46)),
           f'{who("The Mother")} {sd("gets up, alarmed and terrified that he is really about to go, and instinctively lifts her arms")}. {sd("She does not reach him")}.'),
        ]),
        ("Part III — The Fountain", [
          (mini(A3, [("M",80,58),("S",86,38),("F",78,72),("MG",42,78),("BOY",72,62)],
                mover=("SD",68,70,86,56)),
           f'{who("The Step-Daughter")} {sd("lifts the Child-bundle from the Mother&#39;s lap and carries it toward the fountain")}.'),
          (mini(A3, [("M",80,58),("SD",60,55),("F",78,72),("S",86,38)],
                mover=("MG",42,78,50,30)),
           f'{who("The Manager")} {sd("he stands; he picks up the Boy-chair himself and walks it across the stage, and places it behind the fountain basin")}.'),
          (mini(A3, [("M",80,58),("BOY",50,30),("S",84,40),("MG",40,76),("CHILD",58,52)],
                mover=("SD",66,60,56,52)),
           f'{sd("The Step-Daughter bends over the basin and lowers the Child-bundle into it; the basin&#39;s walls hide the action from view")}.'),
          (mini(A3, [("M",80,58),("F",76,70),("SD",56,54),("MG",40,76),("BOY",50,30)],
                mover=("S",84,40,52,82), burst=(50,30)),
           f'{who("The Son")} {sd("his one continuous sentence; then full blackout")}. There in the fountain… {sd("a revolver shot rings out from behind the basin where the Boy-chair is")}.'),
          (mini(A3, [("F",70,76),("SD",54,54),("MG",40,76),("CHILD",54,52),("BOY",50,30)],
                mover=("M",80,58,56,42)),
           f'{who("The Mother")} {sd("she does not cry out at once — she reaches first for the Child-bundle in the basin, then the Boy-chair behind it; her arms cannot hold both, the veil still down")}. My son! My son!'),
          (mini(A3, [("M",58,46),("F",70,74),("SD",54,54),("BOY",50,30)],
                mover=("MG",42,74,42,92)),
           f'{who("The Manager")} {sd("a look at the empty Boy-chair, then he turns and leaves the stage the way a man leaves a theatre")}. Pretence? Reality? … To hell with it all.'),
        ]),
      ]),
    ]


def build():
    cards = []
    for act_title, parts in BEATS():
        cards.append(f'<h1 class="act">{act_title}</h1>')
        for part_title, beats in parts:
            cards.append(f'<h2 class="part">{part_title}</h2>')
            for i, (svg, line) in enumerate(beats, 1):
                cards.append(f'<div class="beat"><div class="map"><span class="bn">{i}</span>{svg}</div>'
                             f'<div class="line">{line}</div></div>')
    body = "".join(cards)

    howto = '''
    <section class="howto">
      <h1 class="title">Blocking Storyboard</h1>
      <p class="sub">Every move in the show — the picture and the line it lands on. Six Characters in Search of an Author · Village Players, Lausanne · dir. Kiarash Jamshidi</p>
      <h3>How to use it</h3>
      <ul>
        <li><strong>One card = one move.</strong> Read the cards top to bottom, in order, act by act and part by part.</li>
        <li><strong>The picture is the stage from above</strong> — the audience sits at the bottom edge (↓). Everyone on stage in that moment is placed. The move is drawn from a <strong>solid dot</strong> (where the character starts), along a <strong>dashed arrow</strong>, to a <strong>hollow ring</strong> (where they end). A burst marks a sudden event (a gunshot, the revolver, the veil).</li>
        <li><strong>The text beside it is the line from the script where the move happens</strong> — the spoken line and its stage direction, nothing added. If a card has no arrow, the positions are what matter.</li>
        <li><strong>Dots are the people; squares are the two stage objects</strong> (▢ the Boy-chair, ◇ the Child-bundle). The set is drawn per act: the chair-circle (One), the two-level platform with shower and piano (Two), the fountain (Three).</li>
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
  font-family:'EB Garamond','Georgia',serif; font-size:11pt; }}
.howto {{ page-break-after: always; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:34pt; color:#8b3a3a; margin:0 0 2mm; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 7mm; font-size:12pt; }}
.howto h3 {{ font-family:'Cormorant Unicase',serif; font-size:12pt; letter-spacing:0.18em; text-transform:uppercase; color:#8b3a3a; margin:6mm 0 3mm; }}
.howto ul {{ padding-left:6mm; }} .howto li {{ margin-bottom:3mm; line-height:1.5; }}
.key {{ margin-top:8mm; display:flex; flex-wrap:wrap; gap:3mm 6mm; }}
.key span {{ font-size:11pt; display:flex; align-items:center; gap:2mm; }}
.key b {{ color:#fff; border-radius:50%; width:8mm; height:8mm; display:inline-flex; align-items:center;
  justify-content:center; font-size:8.5pt; font-family:Arial; }}
h1.act {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:23pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:4mm 0 3mm; padding-bottom:1mm; page-break-before:always; }}
h1.act:first-of-type {{ page-break-before:auto; }}
h2.part {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:11.5pt; letter-spacing:0.12em;
  text-transform:uppercase; color:#2a201a; margin:5mm 0 2mm; break-after:avoid; }}
.beat {{ display:flex; gap:6mm; align-items:flex-start; break-inside:avoid; page-break-inside:avoid;
  margin:0 0 3mm; padding-bottom:3mm; border-bottom:1px solid rgba(42,32,26,0.16); }}
.map {{ position:relative; flex:0 0 64mm; }}
.map svg {{ width:64mm; display:block; }}
.bn {{ position:absolute; top:-1mm; left:-1mm; background:#8b3a3a; color:#fff; width:6mm; height:6mm;
  border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:9pt; font-weight:700;
  font-family:Arial; z-index:2; }}
.line {{ flex:1; line-height:1.5; font-size:11.5pt; padding-top:1mm; }}
.line .who {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9.5pt; letter-spacing:0.07em;
  text-transform:uppercase; color:#8b3a3a; }}
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
