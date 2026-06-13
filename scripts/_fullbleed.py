#!/usr/bin/env python3
"""Full-bleed page helper for the PDF builders.

Chromium leaves the @page margin area unpainted (white). To get the cream
background to the very paper edge with NO white border — while still
keeping a readable text inset on every page, including continuation pages
— we:

  1. force @page margin to 0 (cream then fills the whole sheet), and
  2. wrap the document body in a one-cell table whose <thead>/<tfoot>
     spacer rows repeat on every printed page (giving a top/bottom inset
     that survives page breaks, which plain padding does not), and whose
     body cell carries the left/right inset.

Call apply(html) on the final HTML string just before rendering to PDF.
"""
import re

TOP = "13mm"     # repeating top/bottom text inset
SIDE = "14mm"    # left/right text inset


def apply(html, top=TOP, side=SIDE):
    # 1) Force every "@page { size: A4; margin: ...; }" to margin: 0.
    html = re.sub(r'(@page\s*\{\s*size:\s*A4;\s*margin:\s*)[^;}]+;', r'\g<1>0;', html)

    # 2) Inject the full-bleed + spacer-table CSS just before </head>.
    css = (
        '<style id="fullbleed-overrides">'
        'html,body{background:#efe6cf !important;margin:0 !important;padding:0 !important;}'
        'table.fb-page{width:100%;border-collapse:collapse;}'
        f'table.fb-page>thead>tr>td,table.fb-page>tfoot>tr>td{{height:{top};border:0;padding:0;}}'
        f'table.fb-page>tbody>tr>td{{border:0;padding:0 {side};vertical-align:top;}}'
        '</style>'
    )
    if "</head>" in html:
        html = html.replace("</head>", css + "\n</head>", 1)
    else:
        html = css + html

    # 3) Wrap the body content in the spacer table.
    open_tbl = ('<table class="fb-page"><thead><tr><td></td></tr></thead>'
                '<tbody><tr><td>')
    close_tbl = '</td></tr></tbody><tfoot><tr><td></td></tr></tfoot></table>'
    html = re.sub(r'(<body[^>]*>)', r'\1' + open_tbl, html, count=1)
    html = html.replace("</body>", close_tbl + "</body>", 1)
    return html
