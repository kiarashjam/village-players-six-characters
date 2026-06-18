#!/usr/bin/env python3
"""Build the Sound & Music Score PDF.

A single sheet of the whole show's music and sound: per act and part, what
plays, HOW it is made (live piano on stage, the wings radio, sung live, a
cello drone, an offstage/recorded note, the fountain water, silence, a
recorded coda), and the cue that starts and stops it. Drawn from the Light &
Sound section of the Director's Copy.

A4 portrait, cream full-bleed. Run: python scripts/build_sound_score.py
"""
import os
from pathlib import Path
import _fullbleed

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE.parent / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

# source tag -> (label, colour)
TAG = {
    "live":    ("LIVE PIANO", "#8b3a3a"),
    "radio":   ("RADIO · wings", "#6f6757"),
    "voice":   ("SUNG LIVE", "#b03060"),
    "cello":   ("CELLO DRONE", "#2d6373"),
    "offpno":  ("PIANO · offstage / recorded", "#9c6b1e"),
    "water":   ("WATER · live or recorded", "#2d6373"),
    "rec":     ("RECORDED", "#3a6b3a"),
    "silence": ("SILENCE", "#9a9080"),
}


def chips(*keys):
    out = []
    for k in keys:
        label, col = TAG[k]
        out.append(f'<span class="chip" style="background:{col}">{label}</span>')
    return "".join(out)


# act -> (context line, [ (part, [tagkeys], what-html, cue-html) ])
SCORE = [
    ("Act One — The Family",
     "Three colours, one per part. White working light → amber → deep red. No piano in this act.",
     [
        ("Part I — The Rehearsal", ["radio"],
         "An old French <strong>chanson</strong> on a small radio in the wings — crackling, low, domestic, as if the company forgot to turn it off. "
         "<em>Suggested:</em> Aznavour, <em>La Bohème</em> (low), or a scratchy Piaf record (<em>La Vie en rose</em>, <em>Sous le ciel de Paris</em>).",
         "Plays under the whole rehearsal. <strong>Cuts off</strong> the instant the Door-keeper speaks."),
        ("Part II — The Interruption", ["voice"],
         "No instrument — &ldquo;the warmth is the score.&rdquo; The only music is the Step-Daughter&#39;s own: she <strong>sings <em>Prenez garde à Tchou-Tchin-Tchou</em></strong>, live, as the script requires.",
         "Her song during the dance, where the script places it. Otherwise the amber wash carries the act."),
        ("Part III — The Bargain", ["silence"],
         "<strong>No music.</strong> The silence under the deepening red is the texture.",
         "Held to the end of the act — the cue into Act Two is the <em>absence</em> of sound."),
     ]),
    ("Act Two — The Theatre",
     "A small upright piano sits stage-right on the lower floor, in view all act. The pianist is a credited performer (a fourth Player, in effect), plays from their seat, and does not speak. The shower is a single overhead column of light, used three times.",
     [
        ("Part I — The Setup", ["live"],
         "<strong>Satie — <em>Gymnopédie No. 1</em></strong>: slow, simple, repeated, child-haunted. Played once through, beneath the Step-Daughter&#39;s monologue alone in the shower.",
         "Begins as the shower falls on her. <strong>Ends on her last line</strong> — the Child-bundle set down, the revolver back in the coat."),
        ("Part II — The Apparition", ["live"],
         "A slow, sleazy <strong>Weimar-shop vamp</strong> — comic-cabaret — under Madame Pace&#39;s whole aria. "
         "<em>Suggested:</em> Kurt Weill, <em>Bilbao Song</em> at half tempo, or a vamp on Mistinguett&#39;s <em>Mon Homme</em>.",
         "Plays continuously from her entrance through the transaction. <strong>Dies mid-bar</strong> on the Mother&#39;s &ldquo;You old devil. You murderess.&rdquo;"),
        ("Part III — The Substitution", ["live"],
         "Fragments of the Madame Pace vamp, <strong>in tatters</strong> — as if rehearsing the same tune badly — while the Leading Lady and Leading Man take the platform. Then a single held <strong>piano chord</strong>.",
         "Returns cautiously for the doubled scene. <strong>Cuts out the moment the Mother&#39;s cry begins</strong> and does not return; one chord held as the accidental curtain falls."),
     ]),
    ("Act Three — The Question",
     "Dark stage; the fountain basin lit from inside, pale blue; one bare bulb swinging over the Manager's table. The pianist's chair is empty — no live piano in this act.",
     [
        ("Part I — The Trap", ["cello"],
         "A single sustained <strong>cello drone</strong>, very low — one barely-varying note, felt rather than heard, giving the room a pulse. "
         "<em>Suggested:</em> a sustained low C, or a low organ pedal-tone.",
         "Under the whole philosophical stretch. <strong>Dies</strong> as the Step-Daughter cuts the Father with &ldquo;His reality. He always knew exactly where to find me.&rdquo;"),
        ("Part II — The Refusal", ["silence", "offpno"],
         "<strong>Silence</strong> — only footsteps and breath. One exception: a <strong>single sharp piano note</strong>, like a slap (offstage or recorded — the pianist&#39;s seat is empty now).",
         "The note sounds as the Father seizes the Son at &ldquo;You can force him, sir.&rdquo; Then silence again."),
        ("Part III — The Fountain", ["water", "rec"],
         "The <strong>sound of water</strong> — the fountain itself — and, at the very end, the opening phrase of <strong>Arvo Pärt — <em>Spiegel im Spiegel</em></strong> (about ten seconds).",
         "Water enters at the start and stays, louder as the Step-Daughter nears the basin; <strong>the gunshot is real, in real silence</strong> (the water briefly stops). The Pärt opens after &ldquo;To hell with it all.&rdquo; and the Manager&#39;s exit — then the lights go."),
     ]),
]

ROWS = "".join(
    f'<section class="act"><h2>{title}</h2><p class="ctx">{ctx}</p>'
    + "".join(
        f'<div class="cue"><div class="head"><span class="part">{part}</span>{chips(*tags)}</div>'
        f'<p class="what">{what}</p><p class="when"><span class="lbl">CUE</span> {cue}</p></div>'
        for part, tags, what, cue in parts)
    + "</section>"
    for title, ctx, parts in SCORE)


HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Sound &amp; Music Score — Six Characters</title>
<style>
@page {{ size: A4; margin: 14mm; }}
html,body {{ background:#efe6cf; color:#2a201a; margin:0; padding:0;
  font-family:'EB Garamond','Georgia',serif; font-size:11pt; }}
.title {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:33pt; color:#8b3a3a; margin:0 0 1mm; }}
.sub {{ font-style:italic; color:#6b5b48; margin:0 0 5mm; font-size:12pt; line-height:1.4; }}
.legend {{ display:flex; flex-wrap:wrap; gap:2mm 3mm; margin:0 0 6mm; padding:3mm 0; border-top:1px solid rgba(42,32,26,0.2); border-bottom:1px solid rgba(42,32,26,0.2); }}
.chip {{ color:#fff; font-family:Arial; font-weight:700; font-size:7.4pt; letter-spacing:0.4px;
  border-radius:3px; padding:0.7mm 2mm; white-space:nowrap; }}
h2 {{ font-family:'Cormorant Garamond',serif; font-weight:600; font-size:19pt; color:#8b3a3a;
  border-bottom:2px solid #8b3a3a; margin:6mm 0 1.5mm; padding-bottom:1mm; break-after:avoid; }}
.act:first-of-type h2 {{ margin-top:2mm; }}
.ctx {{ font-style:italic; color:#5d513f; margin:0 0 3mm; line-height:1.42; font-size:10.5pt; }}
.cue {{ break-inside:avoid; margin:0 0 3.2mm; padding:2.4mm 0 0; border-top:1px dotted rgba(42,32,26,0.28); }}
.head {{ display:flex; align-items:center; flex-wrap:wrap; gap:2mm; margin-bottom:1.4mm; }}
.part {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size:10.5pt; letter-spacing:0.08em;
  text-transform:uppercase; color:#2a201a; margin-right:1mm; }}
.what {{ margin:0 0 1.2mm; line-height:1.46; }}
.when {{ margin:0; line-height:1.44; color:#4a4035; font-size:10.5pt; }}
.lbl {{ font-family:Arial; font-weight:700; font-size:6.8pt; letter-spacing:0.6px; color:#fff;
  background:#9a8f78; border-radius:2px; padding:0.5mm 1.6mm; vertical-align:1.5px; margin-right:1mm; }}
.foot {{ margin-top:7mm; padding-top:3mm; border-top:1px solid rgba(42,32,26,0.2);
  font-style:italic; color:#6b5b48; line-height:1.45; }}
</style></head><body>
<h1 class="title">Sound &amp; Music Score</h1>
<p class="sub">Everything the audience hears, act by act — what plays, how it is made, and the cue that starts and stops it. Six Characters in Search of an Author · Village Players, Lausanne · dir. Kiarash Jamshidi</p>
<div class="legend">{chips("live","radio","voice","cello","offpno","water","rec","silence")}</div>
{ROWS}
<p class="foot">One rule over all of it: the score should be <strong>felt, not heard</strong> — the audience need not know they are being scored. The only musician on stage is the Act Two pianist; everything in Acts One and Three is the wings radio, a low recorded drone, the live (or recorded) fountain, an offstage note, and the Pärt coda. The cues above are fixed; the suggested tracks are taste.</p>
</body></html>"""


def build():
    doc = _fullbleed.apply(HTML, top="14mm", side="14mm")
    out_html = OUT_DIR / "sound_score.html"
    out_html.write_text(doc)
    out_pdf = OUT_DIR / "sound_score.pdf"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
        b = p.chromium.launch(**launch_kwargs)
        pg = b.new_page()
        pg.goto(f"file://{out_html.resolve()}", wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(600)
        pg.pdf(path=str(out_pdf), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    out_html.unlink(missing_ok=True)
    print(f"Done: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
