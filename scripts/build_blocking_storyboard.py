#!/usr/bin/env python3
"""Build the Blocking Storyboard PDF.

A beat-by-beat blocking book.  For every part, each movement, entrance,
exit and light change is one card — a top-down picture showing WHERE it
happens paired with the line from the script where it lands.

Each picture carries the full information of the moment:
  * the act's set, drawn from above (chair-circle / two-level platform /
    fountain), with the doors and openings labelled on the frame;
  * everyone on stage, placed as a labelled dot;
  * the move, drawn from a solid start dot, along a dashed arrow, to a
    hollow destination ring;
  * the LIGHT STATE — the stage floor is tinted to the cue and a badge
    names it (work light, amber wash, the shower column, deep red, the
    fountain glow and bare bulb, blackout, the curtain falling/rising);
  * small italic tags for entrances and exits (enters · door at back,
    EXIT, to the office, to the wings, …).

No commentary; just the verbatim dialogue and the picture.  Opens with a
"how to use it" page and a full legend.

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

CREAM = "#efe6cf"

# --- lighting: floor tint + badge (label, colour) per cue -----------------
FLOOR = {
    "halfdark":   "#d6cbad", "work": "#f4eeda", "rehearsal": "#f4eeda",
    "amber":      "#efdcad", "red":  "#e0bcae", "shower":    "#c7bb98",
    "blackout":   "#574d3f", "fountain": "#b6ab8d", "snap":   "#f7f2e2",
    "curtainfall":"#f4eeda", "curtainup": "#f4eeda",
}
BADGE = {
    "halfdark":   ("HALF-DARK", "#7a7363"), "work": ("WORK LIGHT", "#6f6757"),
    "rehearsal":  ("REHEARSAL", "#b18a2c"), "amber": ("AMBER WASH", "#cf8a2c"),
    "red":        ("DEEP RED",  "#9c3a2a"), "shower": ("SHOWER", "#5d6e86"),
    "blackout":   ("BLACKOUT",  "#2a201a"), "fountain": ("FOUNTAIN + BULB", "#2d6373"),
    "snap":       ("LIGHTS SNAP UP", "#cf8a2c"),
    "curtainfall":("CURTAIN ↓", "#8b3a3a"), "curtainup": ("CURTAIN ↑", "#8b3a3a"),
}

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


def _note(nx, ny, text, color="#8b3a3a"):
    x, y = _xy(nx, ny)
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-size="6.6" fill="{color}" '
            f'font-family="serif" font-style="italic" font-weight="600">{text}</text>')


def _opening(nx, ny, edge, label):
    """A doorway: a gap punched in the frame wall, with an italic label."""
    x, y = _xy(nx, ny); g = []
    if edge == "top":
        g.append(f'<rect x="{x-12}" y="{IY0-1.8}" width="24" height="3.6" fill="{CREAM}"/>')
        g.append(f'<text x="{x}" y="{IY0-5}" text-anchor="middle" font-size="6" fill="#8b6a4a" font-family="serif" font-style="italic">{label}</text>')
    elif edge == "right":
        g.append(f'<rect x="{IX1-1.8}" y="{y-12}" width="3.6" height="24" fill="{CREAM}"/>')
        g.append(f'<text x="{IX1-4}" y="{y+2}" text-anchor="end" font-size="6" fill="#8b6a4a" font-family="serif" font-style="italic">{label} →</text>')
    elif edge == "left":
        g.append(f'<rect x="{IX0-1.8}" y="{y-12}" width="3.6" height="24" fill="{CREAM}"/>')
        g.append(f'<text x="{IX0+4}" y="{y+2}" text-anchor="start" font-size="6" fill="#8b6a4a" font-family="serif" font-style="italic">← {label}</text>')
    return "".join(g)


def _bulb(nx, ny, glow):
    x, y = _xy(nx, ny); g = []
    if glow:
        g.append(f'<circle cx="{x}" cy="{y}" r="24" fill="#f7e08a" opacity="0.12"/>')
        g.append(f'<circle cx="{x}" cy="{y}" r="14" fill="#f7e08a" opacity="0.20"/>')
    g.append(f'<line x1="{x}" y1="{y-12}" x2="{x}" y2="{y-3}" stroke="#8a7a5a" stroke-width="0.7"/>')
    g.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{"#ffeaa0" if glow else "#d8cdab"}" stroke="#8a7a5a" stroke-width="0.6"/>')
    return "".join(g)


def _curtain(frac):
    h = (IY1 - IY0) * frac; g = [
        f'<rect x="{IX0}" y="{IY0}" width="{IX1-IX0}" height="{h:.1f}" fill="#7a2230" opacity="0.5"/>']
    n = 13
    for i in range(n + 1):
        x = IX0 + (IX1 - IX0) * i / n
        g.append(f'<line x1="{x:.1f}" y1="{IY0}" x2="{x:.1f}" y2="{IY0+h:.1f}" stroke="#5a1824" stroke-width="0.8" opacity="0.5"/>')
    g.append(f'<line x1="{IX0}" y1="{IY0+h:.1f}" x2="{IX1}" y2="{IY0+h:.1f}" stroke="#5a1824" stroke-width="1.6"/>')
    return "".join(g)


def _doors(act):
    if act == 1:
        return _opening(50, 0, "top", "door at back · USC") + _opening(100, 30, "right", "dressing rooms · SL")
    if act == 2:
        return _opening(50, 0, "top", "door at back · USC") + _opening(100, 64, "right", "office · SL")
    return _opening(2, 42, "left", "wings · SR") + _opening(98, 42, "right", "wings · SL")


def _setpieces(act, light):
    floor = FLOOR.get(light, "#f4eeda")
    s = [f'<rect x="{IX0}" y="{IY0}" width="{IX1-IX0}" height="{IY1-IY0}" rx="6" fill="{floor}" stroke="#8b3a3a" stroke-width="1.6"/>']
    if act == 1:
        cx, cy = _xy(50, 50)
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="42" ry="27" fill="none" stroke="#c9bfa6" stroke-width="1.2"/>')
        for i in range(7):
            a = 2*math.pi*i/7 - math.pi/2
            chx, chy = cx + 42*math.cos(a), cy + 27*math.sin(a)
            s.append(f'<rect x="{chx-3.5}" y="{chy-3.5}" width="7" height="7" rx="1" fill="none" stroke="#b3a888" stroke-width="1.1"/>')
    elif act == 2:
        px0, py0 = _xy(7, 4); px1, py1 = _xy(93, 49)
        s.append(f'<rect x="{px0}" y="{py0}" width="{px1-px0}" height="{py1-py0}" fill="#ece3c6" fill-opacity="0.55" stroke="#8b3a3a" stroke-width="1.1" stroke-dasharray="3,3"/>')
        s.append(f'<text x="{(px0+px1)/2}" y="{py0+10}" text-anchor="middle" font-size="7" fill="#8b3a3a" font-family="serif">UPPER PLATFORM (rehearsal stage)</text>')
        s.append(f'<text x="{(px0+px1)/2}" y="{_xy(50,95)[1]}" text-anchor="middle" font-size="7" fill="#6b5b48" font-family="serif">LOWER FLOOR (watching)</text>')
        # the shower: a faint standing column normally; a bright column when lit
        shx, shy0 = _xy(48, 6); _, shy1 = _xy(48, 49)
        if light == "shower":
            s.append(f'<polygon points="{shx},{shy0-2} {shx-13},{shy1} {shx+13},{shy1}" fill="#fff6c8" opacity="0.30"/>')
            s.append(f'<rect x="{shx-8}" y="{shy0}" width="16" height="{shy1-shy0}" fill="#fff3b0" opacity="0.80"/>')
            s.append(f'<text x="{shx}" y="{shy0+8}" text-anchor="middle" font-size="6.2" fill="#7a6a30" font-family="serif">▼ shower</text>')
        else:
            s.append(f'<rect x="{shx-7}" y="{shy0}" width="14" height="{shy1-shy0}" fill="rgba(247,236,150,0.45)" stroke="#caa" stroke-width="0.6"/>')
            s.append(f'<text x="{shx}" y="{shy0+8}" text-anchor="middle" font-size="6.2" fill="#9a8" font-family="serif">shower</text>')
        s.append(f'<text x="{(px0+px1)/2}" y="{py0+19}" text-anchor="middle" font-size="6" fill="#8b6a4a" font-family="serif" font-style="italic">pegs / hat-rack</text>')
        pnx, pny = _xy(11, 90)
        s.append(f'<rect x="{pnx-8}" y="{pny-7}" width="16" height="14" rx="2" fill="#888"/><text x="{pnx}" y="{pny+4}" text-anchor="middle" font-size="9" fill="#fff">♪</text>')
    else:
        cx, cy = _xy(50, 50)
        glow = light in ("fountain", "blackout")
        fount = "#cfe6ef" if glow else "#dfeaf0"
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="33" ry="21" fill="{fount}" stroke="#2d6373" stroke-width="1.8"/>')
        s.append(f'<text x="{cx}" y="{cy+3}" text-anchor="middle" font-size="7.5" fill="#2d6373" font-family="serif">fountain</text>')
        # the Manager's table, with its bare bulb (glowing only at the end)
        tx, ty = _xy(22, 80)
        s.append(_bulb(22, 72, glow))
        s.append(f'<rect x="{tx-9}" y="{ty-4}" width="18" height="8" rx="1.5" fill="none" stroke="#8a7a5a" stroke-width="1"/>')
        s.append(f'<text x="{tx}" y="{ty+12}" text-anchor="middle" font-size="6" fill="#8b6a4a" font-family="serif" font-style="italic">Manager’s table</text>')
    s.append(_doors(act))
    return "".join(s)


def _badge(light):
    label, color = BADGE.get(light, ("WORK LIGHT", "#6f6757"))
    w = 4.7 * len(label) + 13; x = IX1 - 2 - w; y = IY0 + 2.5
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="12.5" rx="6.2" fill="{color}" opacity="0.95"/>'
            f'<text x="{x+w/2:.1f}" y="{y+8.8}" text-anchor="middle" font-size="6.8" font-weight="700" '
            f'fill="#fff" font-family="Arial" letter-spacing="0.4">{label}</text>')


def mini(act, statics, mover=None, burst=None, light="work", notes=None):
    body = _setpieces(act, light)
    if light == "curtainfall":
        body += _curtain(0.72)
    elif light == "curtainup":
        body += _curtain(0.20)
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
    for n in (notes or []):
        body += _note(*n)
    body += _badge(light)
    body += (f'<text x="{(IX0+IX1)/2}" y="{IY1+13}" text-anchor="middle" font-size="7.5" '
             f'fill="#6b5b48" font-family="serif" font-style="italic">audience ↓ · downstage</text>')
    return f'<svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


def who(name):
    return f'<span class="who">{name}</span>'
def sd(t):
    return f'<span class="sd">[{t}]</span>'


# ===========================================================================
# Beats, driven by a tiny stage simulator so positions are CONSISTENT:
# a figure appears only by an entrance, moves only along a drawn arrow, and
# disappears only by an exit.  Everyone else holds their place frame to frame.
# ===========================================================================
class Sim:
    def __init__(self):
        self.pos = {}          # code -> (x, y)
        self.acts = []         # [(act_title, [(part_title, [(svg, line), ...])])]
        self._a = None
        self._p = None
        self.actno = 1

    def act(self, title, n):
        self.actno = n
        self._a = (title, [])
        self.acts.append(self._a)

    def part(self, title):
        self._p = (title, [])
        self._a[1].append(self._p)

    def clear(self):
        self.pos = {}

    def beat(self, light, line, move=None, enter=None, exit=None,
             burst=None, notes=None, place=None, drop=None, drop_after=None):
        if place:
            self.pos.update(place)
        if drop:
            for c in drop:
                self.pos.pop(c, None)
        mover = None
        after = list(drop_after or [])
        if enter is not None:                       # (code, x1, y1, x2, y2)
            code, x1, y1, x2, y2 = enter
            mover = (code, x1, y1, x2, y2)
            self.pos[code] = (x2, y2)
        elif move is not None:                      # (code, x2, y2)
            code, x2, y2 = move
            x1, y1 = self.pos[code]
            mover = (code, x1, y1, x2, y2)
            self.pos[code] = (x2, y2)
        elif exit is not None:                      # (code, x2, y2)  -> door
            code, x2, y2 = exit
            x1, y1 = self.pos.get(code, (x2, y2))
            mover = (code, x1, y1, x2, y2)
            after.append(code)
        mcode = mover[0] if mover else None
        statics = [(c, p[0], p[1]) for c, p in self.pos.items() if c != mcode]
        svg = mini(self.actno, statics, mover=mover, burst=burst, light=light, notes=notes)
        for c in after:
            self.pos.pop(c, None)
        self._p[1].append((svg, line))

    def result(self):
        return self.acts


def BEATS():
    S = Sim()
    B = S.beat

    # ===================== ACT ONE — THE FAMILY =====================
    S.act("Act One — The Family", 1)

    S.part("Part I — The Rehearsal")
    B("halfdark",
      sd("The Actors and Actresses of the company enter from the back of the stage: first one, then another, then two together; nine or ten in all. Some move off towards their dressing rooms. The Prompter, the &ldquo;book&rdquo; under his arm, waits for the Manager") + ".",
      place={"P1": (28, 62), "P2": (74, 60), "P3": (80, 74)},
      notes=[(50, 17, "the company assembles · enters USC")])
    B("halfdark",
      sd("Finally, the Manager enters with the precise weariness of a man who has managed the Village Players too long; he goes to his table, the Prompter turns on a light and opens the &ldquo;book&rdquo;") + ".",
      enter=("MG", 50, 3, 20, 82), notes=[(50, 16, "enters · USC")])
    B("rehearsal",
      f'{who("The Manager")} {sd("to the Property Man")}. A little light, please — if the house has any left to spare us this evening. {who("Player 2")} {sd("as Property Man")}. Yes, sir. At once. {sd("A light comes down on to the stage")}.')
    B("work",
      f'{who("The Manager")} {sd("clapping his hands")}. Come along! Second act of &ldquo;Mixing It Up&rdquo; — and try, this time, to play it as if you wanted the public to come back for the third. {sd("The Actors go to the wings, all except the three who begin the rehearsal")}.',
      notes=[(50, 38, "the rest of the company → the wings")])
    B("work",
      f'{who("Player 1")} {sd("as Leading Man")}. Excuse me, but must I absolutely wear a cook&#39;s cap? It&#39;s ridiculous. I have a reputation in this canton — fifteen years. {who("Player 2")} {sd("as Property Man, not looking up")}. Fifteen years. And the cap is what finally finishes you.')
    B("work",
      f'{who("Player 3")} {sd("as Prompter, getting into the box")}. Pardon, sir — may I get into my box? There&#39;s a draught off that door, and I&#39;d rather not be hoarse for my first proper season.',
      move=("P3", 84, 86))
    B("amber",
      sd("The white working lights soften to a warm amber. The Door-keeper carries on the Boy-chair and sets it at the edge of the stage; the four live Characters — Father, Mother, Step-Daughter, Son — enter and stop by the door at back, the Step-Daughter carrying the Child-bundle") + ".",
      enter=("BOY", 50, 2, 16, 46),
      place={"F": (44, 10), "M": (52, 8), "SD": (60, 10), "S": (38, 10), "CHILD": (64, 10)},
      notes=[(50, 20, "the Six enter USC, stop at the door")])
    B("amber",
      sd("A tenuous light surrounds the Six, almost as if irradiated by them — the faint breath of their fantastic reality. It will disappear when they come forward") + ".")

    S.part("Part II — The Interruption")
    B("amber",
      f'{who("Player 1")} {sd("as Door-keeper, cap in hand")}. Excuse me, sir — these people are asking for you. I told them you were busy; they insist on coming in. {who("The Manager")} {sd("rudely")}. I am rehearsing — and you know perfectly well no one is allowed in during rehearsals!',
      notes=[(40, 18, "the Door-keeper announces them")])
    B("amber",
      f'{who("The Father")} {sd("coming forward, the others following, embarrassed")}. No, for Heaven&#39;s sake, what are you saying? We bring you a drama, sir.',
      move=("F", 48, 40),
      place={"M": (58, 36), "S": (40, 30), "SD": (66, 42), "CHILD": (74, 34)},
      notes=[(74, 50, "the others follow forward")])
    B("amber",
      f'{who("The Manager")}. But what do you want here, all of you? {who("The Father")}. We want to live. {who("The Manager")}. For Eternity? {who("The Father")}. No, sir, only for a moment… in you.',
      move=("F", 36, 62), notes=[(26, 70, "a step toward the Manager")])
    B("amber",
      f'{who("The Step-Daughter")} {sd("crossing behind the Father; a hand on his shoulder, left one beat too long, then withdrawn")}. My passion, sir. Ah, if you only knew — my passion for <em>him</em>.',
      move=("SD", 54, 46))
    B("amber",
      f'{who("The Step-Daughter")}. I, who am a two months&#39; orphan, will show you how well I can dance and sing. {sd("Sings and dances Prenez garde à Tchou-Tchin-Tchou")}.',
      move=("SD", 52, 84))
    B("amber",
      f'{who("The Mother")} {sd("one arm tightening round the Child-bundle")}. In the name of these two little children, I beg you… {sd("she grows faint")} Oh God!')
    B("amber",
      f'{who("The Father")} {sd("going to her and raising her veil")}. Let them see you!',
      move=("F", 54, 38), burst=(58, 36))
    B("amber",
      f'{who("The Son")} {sd("hands in his pockets, body not moving")}. Leave me alone. I don&#39;t come into this. {who("The Father")}. What? You don&#39;t come into this?',
      move=("S", 34, 24), notes=[(34, 14, "the Son keeps apart · USR")])
    B("amber",
      f'{who("Player 1")} {sd("as Leading Man, beginning to relish it — then his eyes reach the Mother, and the rest does not arrive")}. What a spectacle. What an absolute…',
      move=("P1", 12, 84), notes=[(16, 90, "company to the wings · SR")])

    S.part("Part III — The Bargain")
    B("amber",
      f'{who("The Manager")}. I begin to think there&#39;s the stuff for a drama in all this. {who("The Step-Daughter")} {sd("coming forward")}. When you&#39;ve got a character like me. {who("The Father")} {sd("shutting her up")}. You be quiet!',
      move=("SD", 44, 70), notes=[(40, 80, "comes forward")])
    B("amber",
      f'{who("The Father")} {sd("to the Manager")}. No, no — look here. You must be the author. {who("The Manager")}. I? Because I have never been an author: that&#39;s why. {who("The Father")}. Then why not turn author now?',
      move=("F", 40, 66), notes=[(30, 74, "closing on the Manager")])
    B("amber",
      f'{who("The Step-Daughter")}. The room — I see it. The window with the mantles, the divan, the looking-glass, a screen, and the little mahogany table with the blue envelope and its hundred francs.')
    B("amber",
      sd("Thus talking, the Actors leave the stage; some going out by the little door at the back, others retiring to their dressing-rooms") + ".",
      exit=("P2", 98, 30), notes=[(86, 22, "out the little door / dressing rooms · SL")])
    B("red",
      f'{who("The Manager")} {sd("hooked; leading the Father and the Six off to his office")}. Come with me to my office. In a quarter of an hour, all back here again. {sd("The Manager and the Six cross the stage and go off")}.',
      exit=("MG", 98, 40), drop_after=["F", "M", "SD", "S", "CHILD", "BOY"],
      notes=[(86, 24, "all off to the office · SL")])
    B("work",
      f'{who("Player 1")} {sd("as Leading Man")}. Is he serious? He has taken six strangers into his office and left us standing here like furniture. {who("Player 2")} {sd("as Leading Lady")}. Ordinary strangers do not arrive with a tragedy already rehearsed. {who("Player 3")}. Perhaps there is a play.',
      place={"P1": (40, 52), "P2": (54, 52), "P3": (68, 54)})

    # ===================== ACT TWO — THE THEATRE =====================
    S.act("Act Two — The Theatre", 2)
    S.clear()

    S.part("Part I — The Setup")
    B("work",
      f'{who("The Step-Daughter")} {sd("comes out of the Manager&#39;s office carrying the Child-bundle and dragging the Boy-chair, and cries")}: Come on, Rosetta, let&#39;s run!',
      enter=("SD", 88, 60, 48, 30),
      place={"CHILD": (44, 30), "BOY": (62, 30), "MG": (30, 82), "P3": (22, 82), "F": (78, 40)},
      notes=[(96, 55, "out of the office · SL")])
    B("shower",
      sd("She drags the Boy-chair a little behind her and leaves it leaning. The stage darkens; the shower — a tight vertical column of light from a single overhead source — falls on the Step-Daughter only. The pianist begins Satie&#39;s Gymnopédie No. 1, and she kneels with the Child-bundle") + ".")
    B("shower",
      sd("She slides her hand into the coat pocket and finds the revolver. She holds it up briefly in the column of light, then returns it to the pocket") + ".")
    B("work",
      sd("The piano dies on her last word. The shower holds for one more breath, then releases. The working lights come up. The Step-Daughter is alone on the upper platform with the Child-bundle and the Boy-chair") + ".")
    B("work",
      sd("The Father, Manager and Step-Daughter go back into the office (off); at the same time the Son, followed by the Mother, comes out") + ".",
      enter=("S", 90, 60, 80, 78),
      place={"M": (88, 64), "CHILD": (78, 72), "BOY": (90, 70)},
      drop_after=["SD", "F"],
      notes=[(96, 55, "office (off) · SL"), (78, 86, "Son &amp; Mother come out · SL")])
    B("work",
      f'{who("The Mother")} {sd("rises; one step toward the Son")}. My son — {sd("the Son turns away before the word is finished; she stops, and the unfinished word stays in the air")}.',
      move=("M", 80, 70))
    B("work",
      sd("The stage call-bells ring. From the dressing-rooms and the little door at the back the Actors, Stage Manager, Property Man and Prompter return; the Manager comes out of his office with the Father and the Step-Daughter") + ".",
      place={"P1": (40, 84), "P2": (56, 84), "MG": (30, 82), "F": (78, 40), "SD": (70, 40)},
      notes=[(50, 16, "the company returns · USC")])
    B("work",
      f'{who("The Step-Daughter")}. And the screen! There must be a screen. Otherwise how am I to manage? {who("Player 2")} {sd("as Property Man")}. That&#39;s all right, Miss. We&#39;ve got any amount of them.',
      move=("P2", 60, 40), notes=[(60, 30, "setting the shop · USC")])

    S.part("Part II — The Apparition")
    B("work",
      f'{who("The Father")}. Oh nothing. I just want to put them on these pegs for a moment. And one of the ladies will be so kind as to take off her mantle… {sd("the actresses give up their hats; the shop window and the screen are set")}.',
      move=("P2", 64, 18), notes=[(64, 8, "to the pegs · USC")])
    B("work",
      sd("The door at the back of stage opens and Madame Pace enters and takes a few steps forward — fat, bleach-blonde, the silver chain at her waist") + ".",
      enter=("MP", 50, 2, 48, 18), notes=[(50, 16, "enters · door at back · USC")])
    B("work",
      f'{who("The Step-Daughter")} {sd("running over to her")}. There she is! There she is!',
      move=("SD", 52, 24))
    B("work",
      sd("Madame Pace places one hand under the Step-Daughter&#39;s chin to raise her head") + f'. {who("Madame Pace")}. Good morning, good morning, sir! Madame Pace, sir — dresses and coats, off the rue de Bourg.')
    B("work",
      f'{who("Madame Pace")} {sd("the comedy curdling")}. Not so old, my dear. Not so old. Forty-five, maybe fifty — the age when a man have money in the pocket and shame in the throat, eh, sir?')
    B("work",
      f'{who("The Mother")} {sd("jumping up amid the consternation of the actors — the voice she has not used for years")}. You old devil! You murderess!',
      move=("M", 58, 48))
    B("work",
      f'{who("The Step-Daughter")} {sd("running over to calm her Mother")}. Calm yourself, Mother, calm yourself! Please don&#39;t…',
      move=("SD", 62, 48))
    B("work",
      f'{who("The Manager")} {sd("leading her back to her chair")}. Come along, my dear lady, sit down now, and let&#39;s get on with the scene.',
      move=("M", 80, 66))
    B("work",
      f'{who("Madame Pace")} {sd("pausing at the door, the smile calm now, almost tender")}. There is always the next silk, my dear. There is always the debt. There is always Pace. Don&#39;t you forget the name. {sd("Exits. Not furious. Unhurried")}.',
      exit=("MP", 50, 2), notes=[(50, 16, "EXIT · USC · unhurried")])

    S.part("Part III — The Substitution")
    B("work",
      f'{who("Player 2")} {sd("as Leading Lady; goes to the hat-rack, puts her hat on, and takes the platform to play the Step-Daughter")}. One minute. I want to put my hat on again.',
      move=("P2", 54, 24), notes=[(64, 8, "hat-rack · USC")])
    B("work",
      f'{who("Player 1")} {sd("as Leading Man")}. Why, yes! I&#39;ll prepare my entrance. {sd("Exit to make his entrance")}.',
      exit=("P1", 50, 2), notes=[(50, 16, "EXIT to make his entrance · USC")])
    B("work",
      sd("The door at rear opens and the Leading Man enters with the lively manner of an old gallant") + f'. {who("Player 1")} {sd("as Leading Man")}. Good afternoon, Miss.',
      enter=("P1", 50, 2, 46, 26), notes=[(50, 16, "enters · door at rear · USC")])
    B("work",
      f'{who("The Step-Daughter")} {sd("bursting out laughing, then advancing toward the actors")}. He didn&#39;t say &ldquo;I&#39;m frightfully sorry.&rdquo; He said &ldquo;Oh.&rdquo;',
      move=("SD", 58, 36))
    B("work",
      f'{who("The Step-Daughter")} {sd("low")}. And then he didn&#39;t move. His hand stayed on the hat. {who("The Father")} {sd("turning back, quietly")}. Yes. He said &ldquo;Oh.&rdquo;',
      move=("F", 66, 42), notes=[(72, 48, "turning back")])
    B("work",
      f'{who("Player 1")} {sd("as Leading Man; two steps toward the exit — then a calculation crosses his face; he stops")}. Neither am I. I am through with this scene.',
      move=("P1", 60, 16), notes=[(64, 9, "…then stops · toward the SL exit")])
    B("work",
      f'{who("Player 2")} {sd("the diva&#39;s posture going from offended to leaving")}. I am not going to stand here being made a fool of by that woman.',
      move=("P2", 86, 20), notes=[(90, 11, "leaving · SL")])
    B("shower",
      f'{who("The Step-Daughter")}. Cry out, mother. <em>Cry out as you did then!</em> {who("The Mother")} {sd("coming forward to separate them; the shower falls on her")}. No! My daughter, my daughter! You brute!',
      move=("M", 60, 50), burst=(60, 52))
    B("curtainfall",
      f'{who("The Mother")}. It&#39;s taking place now. It happens all the time. {sd("the piano cuts out; the Machinist drops the curtain by accident — the act ends on the curtain&#39;s fall")}.')

    # ===================== ACT THREE — THE QUESTION =====================
    S.act("Act Three — The Question", 3)
    S.clear()

    S.part("Part I — The Trap")
    B("curtainup",
      sd("Curtain up. The two-level set is struck; the stage is bare but for a single fountain basin, centre. The family sit stage-right, the company stage-left; the Manager stands centre, hand over his mouth") + f'. {who("The Manager")}. Ah yes: the second act!',
      place={"M": (80, 58), "CHILD": (88, 60), "BOY": (72, 62), "S": (86, 38),
             "F": (78, 72), "SD": (68, 72), "P1": (14, 52), "P2": (14, 64),
             "P3": (14, 76), "MG": (42, 80)})
    B("work",
      f'{who("Player 2")} {sd("as Leading Lady")}. The audience needs to know which room we are in. {who("The Father")} {sd("the word lands physically — he turns too quickly")}. The illusion — for Heaven&#39;s sake, don&#39;t say illusion. Don&#39;t use that word.',
      move=("F", 58, 80), notes=[(54, 86, "turns too quickly")])
    B("work",
      f'{who("The Father")} {sd("turning out toward the house; a pause long enough to feel")}. Can you tell me who you are?',
      move=("F", 52, 88), notes=[(52, 94, "to the house · downstage")])
    B("work",
      f'{who("The Manager")}. A man who calls himself a character comes and asks me who I am! {who("The Father")} {sd("with dignity, not offended")}. A character, sir, may always ask a man who he is. Because a character really does have a life of his own.',
      move=("F", 44, 72), notes=[(34, 72, "closing on the Manager")])
    B("work",
      f'{who("The Step-Daughter")} {sd("level, never raised — colder than the philosophy")}. His <em>reality</em>. He always knew exactly where to find me.')
    B("work",
      f'{who("The Manager")}. Then you&#39;ll be saying next that you are more true and real than I am? {who("The Father")} {sd("the greatest seriousness — no smile")}. But of course. Without doubt. {who("The Step-Daughter")} {sd("flat")}. He was real that afternoon. With his hundred francs.')

    S.part("Part II — The Refusal")
    B("work",
      f'{who("The Son")} {sd("jumping up")}. Delighted! Delighted! I don&#39;t ask for anything better. {sd("begins to move away")} {who("The Manager")} {sd("at once stopping him")}. No! No! Where are you going? Wait a bit!',
      move=("S", 92, 20), notes=[(94, 12, "makes for the wings · SL"), (70, 40, "the Manager stops him")])
    B("work",
      f'{who("The Step-Daughter")} {sd("calmly — she knows him")}. Don&#39;t bother to stop him. He won&#39;t go. {who("The Son")} {sd("trapped now, and knowing it")}. If I can&#39;t go away, then I&#39;ll stop here. But I repeat — I act nothing.',
      move=("S", 86, 30))
    B("work",
      f'{who("The Father")} {sd("seizing the Son, not leaving hold")}. You&#39;ve got to obey, do you hear?',
      move=("F", 80, 42))
    B("work",
      f'{who("The Son")} {sd("the voice cracking, the body refusing the cry; they separate")}. What does it mean — this madness you&#39;ve got? I won&#39;t do it. I won&#39;t.',
      move=("S", 86, 24))
    B("work",
      f'{who("The Mother")} {sd("gets up, alarmed and terrified that he is really about to go, and instinctively lifts her arms")}. {sd("She does not reach him")}.',
      move=("M", 80, 46))

    S.part("Part III — The Fountain")
    B("work",
      f'{who("The Son")} {sd("the cry he has been holding for the whole production — surprising himself")}. Yes — but haven&#39;t you yet perceived that it isn&#39;t possible to live in front of a mirror that throws our likeness back at us with a horrible grimace?')
    B("work",
      f'{who("The Mother")}. Yes. Into his room. I couldn&#39;t bear it any more. I went to tell him what I have inside me — all of it. {sd("a hand at her chest")} But the moment he saw me come in…')
    B("work",
      f'{who("The Manager")} {sd("he stands; he picks up the Boy-chair himself and walks it across the stage, and places it behind the fountain basin")}.',
      move=("MG", 50, 32), place={"BOY": (50, 28)}, notes=[(50, 22, "sets the Boy-chair behind the basin")])
    B("work",
      f'{who("The Step-Daughter")} {sd("lifts the Child-bundle from the Mother&#39;s lap and carries it toward the fountain")}.',
      move=("SD", 58, 54), place={"CHILD": (56, 52)})
    B("work",
      sd("The Step-Daughter bends over the basin and lowers the Child-bundle into it; the basin&#39;s walls hide the action from view") + ".",
      move=("SD", 52, 52), place={"CHILD": (50, 50)})
    B("fountain",
      f'{who("The Son")} {sd("his one continuous sentence; the stage lights drop, breath by breath, until only the fountain and the bare bulb over the Manager&#39;s table remain — the Boy-chair silhouetted behind the basin")}. There in the fountain…')
    B("blackout",
      sd("Full blackout. Out of the dark, a revolver shot rings out from behind the basin where the Boy-chair is") + ".",
      burst=(50, 28))
    B("snap",
      f'{who("The Mother")} {sd("she does not cry out at once — she reaches first for the Child-bundle in the basin, then the Boy-chair behind it; her arms cannot hold both, the veil still down")}. My son! My son!',
      move=("M", 54, 46))
    B("snap",
      f'{who("Two Players")}. He&#39;s dead! dead! {who("The Other Players")}. No, no — it&#39;s only make-believe, only pretence! {who("The Father")} {sd("with a terrible cry")}. Pretence? Reality, sir — reality!')
    B("snap",
      sd("The Players lift up the Boy-chair and carry it off, handling it as if it were the Boy&#39;s body — heavy, careful, terrible") + ".",
      exit=("BOY", 98, 30), notes=[(92, 20, "carried off · SL · like a body")])
    B("work",
      f'{who("The Manager")} {sd("a look at the empty Boy-chair, then he turns and leaves the stage the way a man leaves a theatre")}. Pretence? Reality? … To hell with it all.',
      exit=("MG", 42, 94), notes=[(64, 90, "leaves toward the house · downstage")])

    return S.result()


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
      <p class="sub">Every move, entrance, exit and light change — the picture and the line it lands on. Six Characters in Search of an Author · Village Players, Lausanne · dir. Kiarash Jamshidi</p>
      <h3>How to use it</h3>
      <ul>
        <li><strong>One card = one moment.</strong> Read top to bottom, in order, act by act and part by part. The text beside each picture is the verbatim line from the script where the move happens — nothing added.</li>
        <li><strong>The picture is the stage from above.</strong> The audience sits at the bottom edge (↓). Everyone on stage in that moment is placed as a labelled dot. The move is drawn from a <strong>solid dot</strong> (where the character starts), along a <strong>dashed arrow</strong>, to a <strong>hollow ring</strong> (where they end). A <strong>burst</strong> marks a sudden event — the veil, the revolver, the gunshot.</li>
        <li><strong>Doors are labelled on the frame</strong> — the gaps in the wall. Entrances and exits run to and from them, and each tag names <em>which way</em>: <em>enters · door at back · USC</em>, <em>EXIT · unhurried</em>, <em>out of the office · SL</em>, <em>to the wings · SR</em>, <em>leaves toward the house · downstage</em>.</li>
        <li><strong>The light is named on every card</strong> — the badge top-right, and the floor is tinted to match the cue. The set is drawn per act: the chair-circle (One), the two-level platform with shower column, piano and pegs (Two), the fountain with the Manager's table and its bare bulb (Three). ▢ is the Boy-chair, ◇ the Child-bundle.</li>
      </ul>
      <h3>Orientation — which way is which</h3>
      <p class="orient">The audience sits at the foot of every map (<strong>downstage</strong>, DS); the back wall is the top (<strong>upstage</strong>, US). Because the actors face the house, the actor's right — <strong>stage-right (SR)</strong> — is the <em>left</em> of the page, and <strong>stage-left (SL)</strong> is the right. So <em>USC</em> = upstage centre (the door at back), <em>SL</em> = the prompt side here (office, dressing rooms), <em>SR</em> = the opposite wing. Every entrance and exit names its direction.</p>
      <h3>The light cues</h3>
      <div class="lkey">
        <span><b style="background:#7a7363">HALF-DARK</b> the bare work-light of an empty house, before the play</span>
        <span><b style="background:#6f6757">WORK LIGHT</b> full white rehearsal light</span>
        <span><b style="background:#b18a2c">REHEARSAL</b> the light brought down for &ldquo;Mixing It Up&rdquo;</span>
        <span><b style="background:#cf8a2c">AMBER WASH</b> the tenuous light of the Six</span>
        <span><b style="background:#9c3a2a">DEEP RED</b> as they cross off to the office</span>
        <span><b style="background:#5d6e86">SHOWER</b> the tight overhead column on one figure</span>
        <span><b style="background:#8b3a3a">CURTAIN ↓ / ↑</b> the curtain falls / rises</span>
        <span><b style="background:#2d6373">FOUNTAIN + BULB</b> only the fountain glow and the bare bulb</span>
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

    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Blocking Storyboard — Six Characters</title>
<style>
@page {{ size: A4; margin: 13mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:11pt; }}
.howto {{ page-break-after: always; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:34pt; color:#8b3a3a; margin:0 0 2mm; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 6mm; font-size:12pt; }}
.howto h3 {{ font-family:'Cormorant Unicase',serif; font-size:12pt; letter-spacing:0.18em; text-transform:uppercase; color:#8b3a3a; margin:5mm 0 2.5mm; }}
.howto ul {{ padding-left:6mm; margin:0; }} .howto li {{ margin-bottom:2.5mm; line-height:1.45; }}
.orient {{ margin:0; line-height:1.45; }}
.lkey {{ display:flex; flex-direction:column; gap:1.6mm; }}
.lkey span {{ font-size:10pt; display:flex; align-items:baseline; gap:3mm; line-height:1.3; }}
.lkey b {{ color:#fff; border-radius:3px; padding:0.6mm 2mm; font-size:7.4pt; font-family:Arial; font-weight:700;
  letter-spacing:0.4px; flex:0 0 30mm; text-align:center; white-space:nowrap; }}
.key {{ margin-top:2mm; display:flex; flex-wrap:wrap; gap:3mm 6mm; }}
.key span {{ font-size:11pt; display:flex; align-items:center; gap:2mm; }}
.key b {{ color:#fff; border-radius:50%; width:8mm; height:8mm; display:inline-flex; align-items:center;
  justify-content:center; font-size:8.5pt; font-family:Arial; }}
h1.act {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:23pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:4mm 0 3mm; padding-bottom:1mm; page-break-before:always; }}
h1.act:first-of-type {{ page-break-before:always; }}
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
