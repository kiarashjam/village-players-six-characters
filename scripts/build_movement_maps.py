#!/usr/bin/env python3
"""Build the Movement & Blocking Maps PDF.

Top-down (plan view) staging maps for the production: a legend, one stage
plan per act showing the set, every character's starting position, and the
key movements as numbered paths, plus a per-character journey table.

A4 landscape, cream full-bleed. Run: python scripts/build_movement_maps.py
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

# ---------------------------------------------------------------------------
# Character / object colour key
# ---------------------------------------------------------------------------
CH = {
    "F":  ("#8b3a3a", "The Father"),
    "M":  ("#2a201a", "The Mother"),
    "SD": ("#b03060", "The Step-Daughter"),
    "S":  ("#2d6373", "The Son"),
    "MG": ("#3a6b3a", "The Manager"),
    "P1": ("#c8781e", "Player 1"),
    "P2": ("#7a3f9c", "Player 2"),
    "P3": ("#1f8a8a", "Player 3"),
    "MP": ("#b8860b", "Madame Pace"),
    "PN": ("#777777", "Pianist"),
}
OBJ = {
    "BOY":   ("#6b4a2a", "Boy-chair (the Boy)"),
    "CHILD": ("#a9762f", "Child-bundle (the Child)"),
}

VBW, VBH = 1480, 1040          # viewBox (≈ A4 landscape ratio)
SX0, SY0, SX1, SY1 = 70, 200, 980, 880   # stage interior box
PX0 = 1020                     # beats panel left edge


# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------
def disc(x, y, code, label=None, r=21):
    col = CH[code][0]
    lab = label if label is not None else code
    out = (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="#fff" stroke-width="2.5"/>'
           f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="15" font-weight="700" '
           f'fill="#fff" font-family="Arial,sans-serif">{lab}</text>')
    return out


def obj_marker(x, y, code, s=30):
    col = OBJ[code][0]
    if code == "BOY":
        body = (f'<rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" rx="3" '
                f'fill="{col}" stroke="#fff" stroke-width="2.5"/>'
                f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="13" font-weight="700" '
                f'fill="#fff" font-family="Arial,sans-serif">BOY</text>')
    else:
        body = (f'<rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" rx="13" '
                f'fill="{col}" stroke="#fff" stroke-width="2.5" transform="rotate(45 {x} {y})"/>'
                f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="11" font-weight="700" '
                f'fill="#fff" font-family="Arial,sans-serif">CH</text>')
    return body


def chair(x, y):
    return (f'<rect x="{x-11}" y="{y-11}" width="22" height="22" rx="3" fill="none" '
            f'stroke="#6b5b48" stroke-width="2"/>'
            f'<rect x="{x-11}" y="{y-15}" width="22" height="5" rx="2" fill="#6b5b48"/>')


def lbl(x, y, text, size=15, col="#2a201a", anchor="start", weight="400", italic=False, ff="serif"):
    st = "italic" if italic else "normal"
    fam = ("'Cormorant Garamond',Georgia,serif" if ff == "serif"
           else "'Cormorant Unicase',serif")
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
            f'font-style="{st}" font-weight="{weight}" fill="{col}" font-family="{fam}">{text}</text>')


def move(x1, y1, x2, y2, num, col="#8b3a3a", bend=0):
    """Numbered movement path with arrowhead; bend curves the path sideways."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    # perpendicular offset for the control point
    dx, dy = x2 - x1, y2 - y1
    ln = max((dx * dx + dy * dy) ** 0.5, 1)
    cx, cy = mx - dy / ln * bend, my + dx / ln * bend
    path = (f'<path d="M {x1} {y1} Q {cx} {cy} {x2} {y2}" fill="none" stroke="{col}" '
            f'stroke-width="3.2" stroke-dasharray="2,7" stroke-linecap="round" '
            f'marker-end="url(#ah)"/>')
    badge = (f'<circle cx="{cx}" cy="{cy}" r="14" fill="#efe6cf" stroke="{col}" stroke-width="2.5"/>'
             f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="15" font-weight="700" '
             f'fill="{col}" font-family="Arial,sans-serif">{num}</text>')
    return path + badge


def stage_frame(extra_top=""):
    return f'''
    <rect x="{SX0}" y="{SY0}" width="{SX1-SX0}" height="{SY1-SY0}" rx="10"
          fill="#f4eeda" stroke="#8b3a3a" stroke-width="2.5"/>
    {lbl((SX0+SX1)/2, SY0-14, "UPSTAGE — back wall", 15, "#8b3a3a", "middle", "600", ff="uni")}
    {lbl((SX0+SX1)/2, SY1+34, "DOWNSTAGE  ·  the audience is here", 15, "#8b3a3a", "middle", "600", ff="uni")}
    <text x="{SX0-12}" y="{(SY0+SY1)/2}" text-anchor="middle" font-size="12.5" font-weight="600"
          fill="#6b5b48" font-family="'Cormorant Unicase',serif"
          transform="rotate(-90 {SX0-12} {(SY0+SY1)/2})">STAGE RIGHT</text>
    <text x="{SX1+14}" y="{(SY0+SY1)/2}" text-anchor="middle" font-size="12.5" font-weight="600"
          fill="#6b5b48" font-family="'Cormorant Unicase',serif"
          transform="rotate(90 {SX1+14} {(SY0+SY1)/2})">STAGE LEFT</text>
    {extra_top}'''


def beats_panel(title, items):
    rows = []
    y = 200
    rows.append(lbl(PX0, 168, title, 19, "#8b3a3a", "start", "600", ff="uni"))
    rows.append(f'<line x1="{PX0}" y1="178" x2="{VBW-30}" y2="178" stroke="#8b3a3a" stroke-width="1.5"/>')
    for n, txt in items:
        rows.append(f'<circle cx="{PX0+13}" cy="{y-5}" r="13" fill="#8b3a3a"/>'
                    f'<text x="{PX0+13}" y="{y}" text-anchor="middle" font-size="14" font-weight="700" '
                    f'fill="#fff" font-family="Arial,sans-serif">{n}</text>')
        # wrap text
        words, line, lines = txt.split(), "", []
        for w in words:
            if len(line) + len(w) > 44:
                lines.append(line); line = w
            else:
                line = (line + " " + w).strip()
        lines.append(line)
        ty = y - 8
        for i, L in enumerate(lines):
            rows.append(lbl(PX0+34, ty + i*19, L, 14.5, "#2a201a", "start"))
        y += 18 + len(lines) * 19
    return "\n".join(rows)


def page(title, subtitle, body_svg, beats_title, beats):
    svg = f'''<svg viewBox="0 0 {VBW} {VBH}" width="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="ah" markerWidth="11" markerHeight="11" refX="8" refY="4" orient="auto">
          <path d="M0,0 L9,4 L0,8 Z" fill="#8b3a3a"/>
        </marker>
      </defs>
      {lbl(70, 70, title, 40, "#8b3a3a", "start", "600")}
      {lbl(70, 108, subtitle, 19, "#6b5b48", "start", "400", italic=True)}
      <line x1="70" y1="128" x2="{VBW-30}" y2="128" stroke="#8b3a3a" stroke-width="1"/>
      {body_svg}
      {beats_panel(beats_title, beats)}
    </svg>'''
    return f'<section class="page">{svg}</section>'


def burst(x, y, label):
    pts = []
    import math
    for i in range(16):
        r = 26 if i % 2 == 0 else 12
        a = math.pi * i / 8
        pts.append(f"{x+r*math.cos(a):.0f},{y+r*math.sin(a):.0f}")
    return (f'<polygon points="{" ".join(pts)}" fill="#8b3a3a" stroke="#fff" stroke-width="1.5"/>'
            f'<text x="{x}" y="{y+44}" text-anchor="middle" font-size="13" font-weight="700" '
            f'fill="#8b3a3a" font-family="\'Cormorant Unicase\',serif">{label}</text>')


# ===========================================================================
# Page 1 — Legend / how to read
# ===========================================================================
def legend_page():
    p = []
    p.append(lbl(70, 90, "Movement &amp; Blocking Maps", 46, "#8b3a3a", "start", "600"))
    p.append(lbl(70, 132, "Top-down staging plans — Six Characters in Search of an Author · Village Players, Lausanne · dir. Kiarash Jamshidi",
                 18, "#6b5b48", "start", "400", italic=True))
    p.append(f'<line x1="70" y1="150" x2="{VBW-60}" y2="150" stroke="#8b3a3a" stroke-width="1"/>')
    # mini orientation stage
    ox0, oy0, ox1, oy1 = 90, 230, 470, 540
    p.append(f'<rect x="{ox0}" y="{oy0}" width="{ox1-ox0}" height="{oy1-oy0}" rx="8" fill="#f4eeda" stroke="#8b3a3a" stroke-width="2.5"/>')
    p.append(lbl((ox0+ox1)/2, oy0-12, "UPSTAGE — back wall", 14, "#8b3a3a", "middle", "600", ff="uni"))
    p.append(lbl((ox0+ox1)/2, oy1+28, "DOWNSTAGE · audience", 14, "#8b3a3a", "middle", "600", ff="uni"))
    p.append(f'<text x="{ox0-12}" y="{(oy0+oy1)/2}" text-anchor="middle" font-size="12" font-weight="600" fill="#6b5b48" font-family="\'Cormorant Unicase\',serif" transform="rotate(-90 {ox0-12} {(oy0+oy1)/2})">STAGE RIGHT</text>')
    p.append(f'<text x="{ox1+12}" y="{(oy0+oy1)/2}" text-anchor="middle" font-size="12" font-weight="600" fill="#6b5b48" font-family="\'Cormorant Unicase\',serif" transform="rotate(90 {ox1+12} {(oy0+oy1)/2})">STAGE LEFT</text>')
    p.append(move(180, 480, 380, 300, "n", bend=30))
    p.append(lbl((ox0+ox1)/2, oy1+70, "Every plan is seen from above. The audience sits at the bottom edge.", 15, "#2a201a", "middle", italic=True))
    # character key
    kx, ky = 560, 240
    p.append(lbl(kx, ky-22, "THE COMPANY ON STAGE", 16, "#8b3a3a", "start", "600", ff="uni"))
    items = list(CH.items())
    for i, (code, (col, name)) in enumerate(items):
        cyk = ky + i * 46
        p.append(disc(kx+18, cyk, code))
        p.append(lbl(kx+50, cyk+6, name, 17, "#2a201a", "start"))
    # object + symbol key (right column)
    sx, sy = 1010, 240
    p.append(lbl(sx, sy-22, "THE TWO STAGE OBJECTS", 16, "#8b3a3a", "start", "600", ff="uni"))
    p.append(obj_marker(sx+18, sy, "BOY")); p.append(lbl(sx+50, sy+6, OBJ["BOY"][1], 17, "#2a201a", "start"))
    p.append(obj_marker(sx+18, sy+50, "CHILD")); p.append(lbl(sx+50, sy+56, OBJ["CHILD"][1], 17, "#2a201a", "start"))
    p.append(lbl(sx, sy+118, "SYMBOLS", 16, "#8b3a3a", "start", "600", ff="uni"))
    p.append(move(sx+4, sy+150, sx+120, sy+150, "1"))
    p.append(lbl(sx+150, sy+156, "a movement, in order", 16, "#2a201a", "start"))
    p.append(chair(sx+18, sy+200)); p.append(lbl(sx+50, sy+206, "a chair (Act One circle)", 16, "#2a201a", "start"))
    p.append(burst(sx+18, sy+262, "")); p.append(lbl(sx+50, sy+268, "the gunshot / a sudden event", 16, "#2a201a", "start"))
    p.append(f'<rect x="{sx+4}" y="{sy+300}" width="30" height="34" fill="rgba(247,236,150,0.55)" stroke="#caa" stroke-width="1"/>')
    p.append(lbl(sx+50, sy+322, "the &ldquo;shower&rdquo; light column (Act Two)", 16, "#2a201a", "start"))
    p.append(lbl(70, 980, "Read each act's plan with its numbered key on the right; the per-character journey is the last page.",
                 15, "#6b5b48", "start", italic=True))
    svg = (f'<svg viewBox="0 0 {VBW} {VBH}" width="100%" xmlns="http://www.w3.org/2000/svg">'
           f'<defs><marker id="ah" markerWidth="11" markerHeight="11" refX="8" refY="4" orient="auto">'
           f'<path d="M0,0 L9,4 L0,8 Z" fill="#8b3a3a"/></marker></defs>' + "\n".join(p) + "</svg>")
    return f'<section class="page">{svg}</section>'


# ===========================================================================
# Per-character journey table
# ===========================================================================
def table_page():
    rows = [
        ("The Father", "Enters with the Six (upstage); crosses to plead with the Manager; lifts the Mother's veil.",
         "On the lower floor; waits behind the upstage door of the platform to play the shop scene.",
         "Seated right-front; argues the reality debate centre; pinned, ends in stillness."),
        ("The Mother", "Enters with the Six; faints centre; veil lifted against her will.",
         "On the lower floor; erupts upward at Madame Pace; forced to watch the doubled scene.",
         "Seated right with both children; rises and reaches for Child-bundle then Boy-chair — cannot hold both."),
        ("The Step-Daughter", "Enters with the Child-bundle; comes downstage to sing and taunt; drives the exposure.",
         "Erupts up onto the platform; solo in the shower; plays the shop scene with Madame Pace.",
         "Crosses to the basin, lowers the Child-bundle in; then runs, and is gone."),
        ("The Son", "Enters with the Six; stays at the edge, refusing.",
         "On the lower floor, apart; will not go up.",
         "Isolated stage-right; comes downstage to narrate the drowning — his one continuous speech."),
        ("The Manager", "At his own chair, apart; receives the Father; runs the room.",
         "On the lower floor; casts and directs the doubled scene from below.",
         "Centre, standing; picks up the Boy-chair and sets it behind the fountain; then walks out."),
        ("Player 1", "Leading Man in the chair circle; Door-keeper carries in the Boy-chair; recedes to the wings.",
         "Climbs to the platform as the Leading Man in the doubled scene; the Machinist drops the curtain.",
         "Seated stage-left with the company; watches."),
        ("Player 2", "Leading Lady in the circle; gives her hat; recedes to the wings.",
         "Climbs to the platform as the Leading Lady (doubled scene); walks off, offended.",
         "Seated stage-left; watches."),
        ("Player 3", "Youngest; near the Prompter's box; recedes to the wings with the company.",
         "On the lower floor; the company's witness as the scene turns.",
         "Seated stage-left; the audience's mirror."),
        ("Madame Pace", "—  (not yet present).",
         "Conjured through the upstage door of the platform; into the shower; plays the shop, then exits.",
         "—  (her scene is over)."),
        ("Boy-chair", "Carried in by the Door-keeper; set at the stage-right edge.",
         "Dragged up onto the platform; the revolver taken from its coat.",
         "Carried by the Manager behind the fountain; the gunshot comes from there."),
        ("Child-bundle", "Carried on by the Step-Daughter; held centre.",
         "In the Step-Daughter's arms through the monologue and the shop.",
         "Lowered into the fountain basin; the drowning is hidden by its walls."),
    ]
    th = ('<th style="width:17%">Character</th><th>Act One — The Family</th>'
          '<th>Act Two — The Theatre</th><th>Act Three — The Question</th>')
    trs = ""
    for name, a1, a2, a3 in rows:
        trs += f'<tr><td class="who">{name}</td><td>{a1}</td><td>{a2}</td><td>{a3}</td></tr>'
    return f'''<section class="page tablepage">
      <h1>Where everyone goes — the journey in one view</h1>
      <table class="journey"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>
    </section>'''


# ===========================================================================
# Build
# ===========================================================================
def main():
    # ---- ACT ONE ----
    a1 = []
    a1.append(stage_frame())
    # chair circle
    import math
    cx, cy = 540, 560
    for i in range(7):
        a = 2*math.pi*i/7 - math.pi/2
        a1.append(chair(cx+150*math.cos(a), cy+95*math.sin(a)))
    a1.append(lbl(cx, cy+6, "the circle", 13, "#6b5b48", "middle", italic=True))
    a1.append(lbl(525, 252, "▯ upstage door", 13, "#6b5b48", "middle", ff="uni"))
    a1.append(f'<rect x="855" y="800" width="70" height="44" rx="4" fill="none" stroke="#6b5b48" stroke-width="2"/>')
    a1.append(lbl(890, 858, "Prompter's box", 12, "#6b5b48", "middle", italic=True))
    # movements first (under markers)
    a1.append(move(525, 270, 175, 440, "1", CH["F"][0], bend=60))
    a1.append(move(520, 300, 520, 470, "2", bend=-40))
    a1.append(move(640, 320, 560, 690, "3", CH["SD"][0], bend=70))
    a1.append(move(450, 320, 270, 700, "4", CH["F"][0], bend=-50))
    a1.append(move(575, 470, 595, 540, "5", CH["M"][0], bend=0))
    a1.append(move(470, 470, 130, 830, "6", CH["P1"][0], bend=40))
    a1.append(burst(600, 545, "veil lifted"))
    # start markers
    a1.append(disc(220, 770, "MG", "MG"))
    a1.append(lbl(220, 805, "(his chair, apart)", 11, "#6b5b48", "middle", italic=True))
    a1.append(disc(470, 470, "P1")); a1.append(disc(620, 470, "P2")); a1.append(disc(855, 790, "P3"))
    a1.append(disc(440, 285, "F")); a1.append(disc(520, 285, "M")); a1.append(disc(650, 300, "SD"))
    a1.append(disc(370, 285, "S"))
    a1.append(obj_marker(720, 300, "CHILD"))
    a1.append(obj_marker(170, 445, "BOY"))
    beats1 = [
        ("1", "The Door-keeper carries the Boy-chair in from the upstage door and sets it at the stage-right edge."),
        ("2", "The Six enter from the upstage door in a tenuous light and advance to centre."),
        ("3", "The Step-Daughter comes downstage with the Child-bundle — sings and dances, then taunts the Father."),
        ("4", "The Father crosses to the Manager (at his chair, apart) and pleads to be staged."),
        ("5", "The Mother faints centre; the Father lifts her veil against her will."),
        ("6", "The company recedes to the wings and becomes the on-stage audience; the bargain — light drifts amber to deep red."),
    ]
    P1 = page("Act One — The Family",
              "A bare stage, a circle of chairs. The rehearsal is interrupted; the Six walk in.",
              "\n".join(a1), "Movement key", beats1)

    # ---- ACT TWO ----
    a2 = []
    a2.append(stage_frame())
    # upper platform
    a2.append(f'<rect x="180" y="235" width="700" height="300" rx="6" fill="#ece3c6" stroke="#8b3a3a" stroke-width="2" stroke-dasharray="6,4"/>')
    a2.append(lbl(530, 262, "UPPER PLATFORM — the rehearsal stage", 14, "#8b3a3a", "middle", "600", ff="uni"))
    a2.append(lbl(530, 620, "LOWER FLOOR — the actors watch · the Six wait · technical", 14, "#6b5b48", "middle", "600", ff="uni"))
    # shower column
    a2.append(f'<rect x="495" y="300" width="70" height="235" fill="rgba(247,236,150,0.5)" stroke="#caa" stroke-width="1"/>')
    a2.append(lbl(530, 320, "shower", 12, "#6b5b48", "middle", italic=True))
    a2.append(lbl(525, 250, "▯ door", 12, "#6b5b48", "middle", ff="uni"))
    # piano
    a2.append(f'<rect x="120" y="760" width="74" height="46" rx="3" fill="#777" stroke="#fff" stroke-width="2"/>')
    a2.append(lbl(157, 789, "♪", 22, "#fff", "middle", weight="700"))
    a2.append(lbl(157, 826, "piano", 12, "#6b5b48", "middle", italic=True))
    # movements
    a2.append(move(650, 660, 540, 430, "1", CH["SD"][0], bend=50))
    a2.append(move(540, 430, 530, 360, "2", CH["SD"][0], bend=0))
    a2.append(move(525, 268, 545, 345, "3", CH["MP"][0], bend=0))
    a2.append(move(770, 770, 640, 540, "5", CH["M"][0], bend=40))
    a2.append(move(470, 830, 470, 470, "6", CH["P1"][0], bend=-30))
    a2.append(move(560, 830, 580, 470, "6", CH["P2"][0], bend=30))
    # markers
    a2.append(disc(300, 820, "MG")); a2.append(disc(430, 830, "P1")); a2.append(disc(560, 830, "P2")); a2.append(disc(680, 830, "P3"))
    a2.append(disc(770, 770, "M")); a2.append(obj_marker(815, 800, "CHILD", s=26))
    a2.append(disc(860, 810, "S"))
    a2.append(disc(650, 660, "SD"))
    a2.append(disc(770, 280, "F")); a2.append(lbl(770, 312, "(waits behind the door)", 10.5, "#6b5b48", "middle", italic=True))
    a2.append(disc(525, 300, "MP"))
    a2.append(obj_marker(610, 430, "BOY", s=26))
    beats2 = [
        ("1", "The Step-Daughter erupts from the lower floor up onto the platform, dragging the Boy-chair, carrying the Child-bundle."),
        ("2", "She steps into the shower for her solo monologue, and takes the revolver from the coat on the Boy-chair."),
        ("3", "Conjured: the upstage door opens and Madame Pace enters onto the platform, into the shower — the shop scene."),
        ("4", "The Father waits behind the upstage door, ready to enter the scene on cue."),
        ("5", "The Mother, on the lower floor, erupts upward at Madame Pace — &ldquo;You old devil!&rdquo; — her voice crossing up."),
        ("6", "The Leading Lady and Leading Man climb up to replay the scene (the doubled scene); the Mother is forced to watch; the Machinist drops the curtain by accident."),
    ]
    P2 = page("Act Two — The Theatre",
              "Two levels. Performing is up; watching is down. The line between them is the platform's edge.",
              "\n".join(a2), "Movement key", beats2)

    # ---- ACT THREE ----
    a3 = []
    a3.append(stage_frame())
    # fountain basin
    a3.append(f'<ellipse cx="525" cy="520" rx="95" ry="62" fill="#dfeaf0" stroke="#2d6373" stroke-width="3"/>')
    a3.append(lbl(525, 525, "fountain", 14, "#2d6373", "middle", "600", ff="uni"))
    a3.append(lbl(525, 600, "(walls high — the interior is hidden)", 11.5, "#6b5b48", "middle", italic=True))
    # movements
    a3.append(move(820, 600, 540, 430, "1", CH["MG"][0], bend=70))
    a3.append(move(700, 700, 575, 545, "2", CH["SD"][0], bend=30))
    a3.append(move(870, 410, 540, 720, "3", CH["S"][0], bend=-80))
    a3.append(move(820, 560, 560, 500, "5", CH["M"][0], bend=30))
    a3.append(move(430, 770, 430, 920, "6", CH["MG"][0], bend=0))
    a3.append(burst(525, 425, "gunshot"))
    # markers — family right, actors left, manager centre
    a3.append(disc(820, 560, "M")); a3.append(obj_marker(862, 595, "CHILD", s=24))
    a3.append(obj_marker(770, 600, "BOY", s=26))
    a3.append(disc(880, 410, "S")); a3.append(lbl(880, 442, "(apart)", 10.5, "#6b5b48", "middle", italic=True))
    a3.append(disc(790, 700, "F")); a3.append(disc(700, 700, "SD"))
    a3.append(disc(200, 540, "P1")); a3.append(disc(200, 620, "P2")); a3.append(disc(200, 700, "P3"))
    a3.append(disc(430, 770, "MG"))
    beats3 = [
        ("1", "The Manager picks up the Boy-chair himself and carries it behind the fountain — the moment he stops being audience and becomes accessory."),
        ("2", "The Step-Daughter crosses to the basin, bends over it, and lowers the Child-bundle into the water."),
        ("3", "The Son comes downstage-centre to narrate the drowning he could not stop — his one continuous speech."),
        ("4", "Blackout. A real gunshot from behind the basin, where the Boy-chair is."),
        ("5", "The Mother rises and reaches — first for the Child-bundle in the basin, then for the Boy-chair behind it — and cannot hold both."),
        ("6", "The Manager looks at the empty Boy-chair, says &ldquo;To hell with it all,&rdquo; and walks out the way a man leaves a theatre."),
    ]
    P3 = page("Act Three — The Question",
              "A bare stage; one fountain basin. Family stage-right, the company stage-left, the Manager centre.",
              "\n".join(a3), "Movement key", beats3)

    body = legend_page() + P1 + P2 + P3 + table_page()
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Movement &amp; Blocking Maps — Six Characters</title>
<style>
@page {{ size: A4 landscape; margin: 0; }}
html,body {{ background:#efe6cf; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; color:#2a201a; }}
.page {{ page-break-after: always; padding: 6mm; box-sizing:border-box; text-align:center;
  height: 210mm; overflow: hidden; }}
.page:last-child {{ page-break-after: auto; }}
svg {{ display:block; height: 196mm; width:auto; max-width:100%; margin:0 auto; }}
.tablepage {{ text-align:left; }}
.tablepage h1 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:26pt;
  color:#8b3a3a; margin:0 0 4mm 0; }}
table.journey {{ width:100%; border-collapse:collapse; font-size:10pt; }}
table.journey th {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9.5pt;
  letter-spacing:0.08em; text-transform:uppercase; color:#8b3a3a; text-align:left;
  padding:3mm; border-bottom:2px solid #8b3a3a; vertical-align:bottom; }}
table.journey td {{ padding:2.6mm 3mm; border-bottom:1px solid rgba(42,32,26,0.18);
  vertical-align:top; line-height:1.4; }}
table.journey td.who {{ font-weight:700; color:#8b3a3a; font-family:'Cormorant Garamond',serif;
  font-size:12pt; }}
table.journey tbody tr:nth-child(even) {{ background:rgba(255,255,255,0.22); }}
</style></head><body>
{body}
</body></html>"""
    out_html = OUT_DIR / "movement_maps.html"
    out_html.write_text(html)
    out_pdf = OUT_DIR / "movement_maps.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**launch_kwargs)
        pg = b.new_page()
        pg.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(700)
        pg.pdf(path=str(out_pdf), landscape=True, print_background=True, prefer_css_page_size=True)
        b.close()
    out_html.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
