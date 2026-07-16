#!/usr/bin/env python3
"""Build the Actor Rehearsal Script as an editable Microsoft Word (.docx) file.

Reuses build_actor_script.build_actor_html() (same trimming/stripping as the
PDF actor script), then walks the cleaned HTML and emits a plain, editable
Word document: a title block, the cast, the production note, act headings,
part headings, stage directions in italic, and every speech as
"SPEAKER  spoken text" with the speaker in bold. No colour, no theme — a
working script anyone can edit in Word.

Output: outputs/actor_script.docx
Run: python scripts/build_actor_script_docx.py
"""
import os
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

import build_actor_script  # same content pipeline as the PDF actor script

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", ROOT / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _runs_from(node, para, italic=False, bold=False):
    """Append the text of an inline node to a paragraph, honouring <em>/<i>/<strong>/<b>."""
    if isinstance(node, NavigableString):
        text = str(node)
        if text:
            r = para.add_run(text)
            r.italic = italic
            r.bold = bold
        return
    if isinstance(node, Tag):
        it = italic or node.name in ("em", "i")
        bd = bold or node.name in ("strong", "b")
        if node.name == "br":
            para.add_run().add_break()
            return
        for child in node.children:
            _runs_from(child, para, italic=it, bold=bd)


def build():
    html = build_actor_script.build_actor_html()
    soup = BeautifulSoup(html, "html.parser")

    doc = Document()
    # Base style: a clean serif, readable size
    normal = doc.styles["Normal"]
    normal.font.name = "Georgia"
    normal.font.size = Pt(11)

    # ---- Title block (from the cover) ----
    doc.add_paragraph("ACTOR REHEARSAL SCRIPT").alignment = WD_ALIGN_PARAGRAPH.CENTER
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Six Characters in Search of an Author")
    r.bold = True
    r.font.size = Pt(20)
    sub = doc.add_paragraph("Luigi Pirandello · trans. Edward Storer (1922)\n"
                            "Rewritten and directed by Kiarash Jamshidi · Village Players, Lausanne")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for rr in sub.runs:
        rr.italic = True
    doc.add_page_break()

    # ---- Cast list ----
    cast = soup.select_one("section.cast")
    if cast is not None:
        doc.add_heading("The Company & The Characters", level=1)
        for li in cast.select("li"):
            txt = li.get_text(" ", strip=True)
            if txt:
                doc.add_paragraph(txt, style="List Bullet")

    # ---- Production note ----
    prod = soup.select_one("section.actor-production-note")
    if prod is not None:
        h = prod.select_one("h2")
        doc.add_heading(h.get_text(" ", strip=True) if h else "Note", level=1)
        for p in prod.select("p"):
            para = doc.add_paragraph()
            _runs_from(p, para)

    doc.add_page_break()

    # ---- Walk the play body in document order ----
    main = soup.select_one("main") or soup.body or soup
    handled = set()
    for el in main.descendants:
        if not isinstance(el, Tag):
            continue
        # Act headers (a <section class="act-header"> with a label + theme)
        if el.name == "section" and "act-header" in (el.get("class") or []):
            doc.add_page_break()
            label = el.select_one(".label")
            theme = el.select_one(".act-theme")
            doc.add_heading(label.get_text(" ", strip=True) if label else "Act", level=1)
            if theme:
                tp = doc.add_paragraph(theme.get_text(" ", strip=True))
                tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for rr in tp.runs:
                    rr.italic = True
            continue
        # Part headings
        if el.name == "div" and "actor-part" in (el.get("class") or []):
            eyebrow = el.select_one(".part-eyebrow")
            title = el.select_one(".part-title")
            label = ""
            if eyebrow:
                label += eyebrow.get_text(" ", strip=True)
            if title:
                label += (" — " if label else "") + title.get_text(" ", strip=True)
            doc.add_heading(label, level=2)
            continue
        # Speeches
        if el.name == "p" and "speech" in (el.get("class") or []):
            para = doc.add_paragraph()
            sp = el.select_one(".speaker")
            speaker = sp.get_text(" ", strip=True) if sp else ""
            if speaker:
                rr = para.add_run(speaker.upper() + ".  ")
                rr.bold = True
            # everything after the speaker span, in order
            after_speaker = False
            for child in el.children:
                if isinstance(child, Tag) and "speaker" in (child.get("class") or []):
                    after_speaker = True
                    continue
                if not after_speaker and sp is not None:
                    continue
                # action spans -> italic; em -> italic
                if isinstance(child, Tag) and "action" in (child.get("class") or []):
                    r = para.add_run(child.get_text(" ", strip=True) + " ")
                    r.italic = True
                else:
                    _runs_from(child, para)
            continue
        # Bare stage paragraphs
        if el.name == "p" and "stage" in (el.get("class") or []):
            para = doc.add_paragraph()
            _runs_from(el, para)
            for rr in para.runs:
                rr.italic = True
            continue
        # Song block
        if el.name == "div" and "song" in (el.get("class") or []):
            para = doc.add_paragraph()
            para.paragraph_format.left_indent = Pt(24)
            _runs_from(el, para)
            for rr in para.runs:
                rr.italic = True
            continue
        # Curtain
        if el.name == "div" and "curtain" in (el.get("class") or []):
            p = doc.add_paragraph(el.get_text(" ", strip=True))
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for rr in p.runs:
                rr.bold = True

    out = OUT_DIR / "actor_script.docx"
    doc.save(str(out))
    # quick stats
    speeches = len(soup.select("p.speech"))
    print(f"Done: {out} ({out.stat().st_size:,} bytes, {speeches} speeches)")


if __name__ == "__main__":
    build()
