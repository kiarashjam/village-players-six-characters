#!/usr/bin/env python3
"""One PDF per part of each act (9 in all): that part's script, each spoken
line preceded by its 'why it happens / why they say it' note, and opened by
the director's scene-note for the part. Reuses data/reading_glosses.json."""
import os, re, json, html as _html
from pathlib import Path
import _fullbleed

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("OUT_DIR", HERE.parent / "outputs")); OUT.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")
SRC = HERE.parent / "six_characters_village_players.html"
GLOSS = HERE.parent / "data" / "reading_glosses.json"
ACT_TITLE = {"Act One": "Act One — The Family", "Act Two": "Act Two — The Theatre",
             "Act Three": "Act Three — The Question"}

src = SRC.read_text(encoding="utf-8")
def txt(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

# scene-note (why this part) keyed by part title
narr = {}
for a in re.findall(r'<aside class="part-note">(.*?)</aside>', src, re.S):
    tt = re.search(r'<h3 class="part-title"[^>]*>(.*?)</h3>', a, re.S)
    nv = re.search(r'<div class="part-narrative">(.*?)</div>', a, re.S)
    if tt and nv:
        inner = re.sub(r'\sclass="[^"]*"', '', nv.group(1))      # keep tags, drop classes
        inner = re.sub(r'<(?!/?(?:p|em|strong|i|b)\b)[^>]+>', '', inner)  # keep only basic inline/p tags
        narr[txt(tt.group(1))] = inner.strip()

# harvest parts in order (speech/stage with global speech index matching the glosses)
token = re.compile(r'<div class="part-eyebrow"[^>]*>(?P<eye>.*?)</div>'
                   r'|<h3 class="part-title"[^>]*>(?P<part>.*?)</h3>'
                   r'|<p class="speech">(?P<sp>.*?)</p>'
                   r'|<p class="stage"[^>]*>(?P<st>.*?)</p>', re.S)
seq=[]; act=no=None; gi=0
for m in token.finditer(src):
    if m.group("eye") is not None:
        mm=re.match(r"(Part [IVX]+) of (Act \w+)", txt(m.group("eye")))
        if mm: no,act=mm.group(1),ACT_TITLE.get(mm.group(2),mm.group(2))
    elif m.group("part") is not None:
        nm=txt(m.group("part"))
        seq.append({"act":act or "","ptitle":f"{no} — {nm}","name":nm,"els":[]})
    elif not seq: continue
    elif m.group("sp") is not None:
        h=m.group("sp").replace('<span class="speaker">','<span class="who">').replace('<span class="action">','<span class="sd">')
        seq[-1]["els"].append(("speech",h,gi)); gi+=1
    elif m.group("st") is not None:
        seq[-1]["els"].append(("stage",m.group("st"),None))

glosses=json.loads(GLOSS.read_text(encoding="utf-8"))

CSS = """
@page { size: A4; margin: 14mm; }
html,body { background:#efe6cf; color:#2a201a; margin:0; padding:0; font-family:'EB Garamond','Georgia',serif; font-size:11pt; }
.act { font-family:'Cormorant Unicase',serif; font-size:11pt; letter-spacing:0.16em; text-transform:uppercase; color:#8b3a3a; margin:0 0 1mm; }
.ptitle { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:30pt; color:#8b3a3a; margin:0 0 4mm; line-height:1.05; }
.why { background:#f4eeda; border-left:3px solid #8b3a3a; padding:3mm 4mm; margin:0 0 6mm; }
.why h4 { font-family:'Cormorant Unicase',serif; font-size:10pt; letter-spacing:0.16em; text-transform:uppercase; color:#8b3a3a; margin:0 0 2mm; }
.why p { margin:0 0 2.4mm; line-height:1.5; } .why p:last-child { margin-bottom:0; }
.scripthead { font-family:'Cormorant Unicase',serif; font-size:10pt; letter-spacing:0.16em; text-transform:uppercase; color:#8b3a3a; margin:0 0 3mm; border-top:1px solid rgba(42,32,26,0.25); padding-top:3mm; }
.unit { break-inside:avoid; page-break-inside:avoid; margin:0 0 3.4mm; }
.note { font-style:italic; font-size:8.7pt; color:#7c6a4f; border-left:2.2px solid #c39a52; padding-left:3mm; margin:0 0 1.1mm; line-height:1.38; }
.sp { margin:0; line-height:1.5; }
.who { font-family:'Cormorant Unicase',serif; font-weight:600; font-size:9pt; letter-spacing:0.07em; text-transform:uppercase; color:#8b3a3a; }
.sd { font-style:italic; color:#6b5b48; }
.stagedir { font-style:italic; color:#5d513f; margin:3mm 7mm; line-height:1.42; }
"""

def slug(name): return re.sub(r'[^a-z0-9]+','_',name.lower()).strip('_')

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    kw={"executable_path":CHROMIUM} if CHROMIUM else {}
    b=p.chromium.launch(**kw); pg=b.new_page()
    for i,part in enumerate(seq,1):
        body=[f'<p class="act">{part["act"]}</p><h1 class="ptitle">{part["ptitle"]}</h1>']
        why=narr.get(part["name"])
        if why: body.append(f'<div class="why"><h4>Why this part — what is happening and why</h4>{why}</div>')
        body.append('<p class="scripthead">The script, line by line — with what each line is doing</p>')
        for kind,h,g in part["els"]:
            if kind=="stage": body.append(f'<p class="stagedir">{h}</p>')
            else:
                note=glosses.get(str(g),"")
                body.append(f'<div class="unit"><p class="note">{_html.escape(note)}</p><p class="sp">{h}</p></div>')
        doc=f"<!DOCTYPE html><html lang=en><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(body)}</body></html>"
        doc=_fullbleed.apply(doc, top="14mm", side="14mm")
        hp=OUT/f"part_{i}_{slug(part['name'])}.html"; hp.write_text(doc)
        outp=OUT/f"part_{i}_{slug(part['name'])}.pdf"
        pg.goto(f"file://{hp.resolve()}", wait_until="networkidle", timeout=60000); pg.wait_for_timeout(400)
        pg.pdf(path=str(outp), format="A4", print_background=True, prefer_css_page_size=True)
        hp.unlink(missing_ok=True)
        print("wrote", outp.name)
    b.close()
print("done — 9 part PDFs")
