#!/usr/bin/env python3
"""
Recount speeches and words per part in the play HTML.
Updates the nine per-part `Who speaks, and how much` blocks
inside the part-notes, and the aggregated data/role_stats.json.

Run from the repo root:  python scripts/recount_stats.py
"""

import re
import json
from pathlib import Path
from collections import OrderedDict, defaultdict

HERE = Path(__file__).resolve().parent.parent
PLAY = HERE / "six_characters_village_players.html"
STATS = HERE / "data" / "role_stats.json"

PARTS = [
    ("Act 1 Part I",   "Part I of Act One",     '<div class="part-eyebrow">Part II of Act One</div>'),
    ("Act 1 Part II",  "Part II of Act One",    '<div class="part-eyebrow">Part III of Act One</div>'),
    ("Act 1 Part III", "Part III of Act One",   '<div class="curtain">— End of Act I —</div>'),
    ("Act 2 Part I",   "Part I of Act Two",     '<div class="part-eyebrow">Part II of Act Two</div>'),
    ("Act 2 Part II",  "Part II of Act Two",    '<div class="part-eyebrow">Part III of Act Two</div>'),
    ("Act 2 Part III", "Part III of Act Two",   '<div class="curtain">— End of Act II —</div>'),
    ("Act 3 Part I",   "Part I of Act Three",   '<div class="part-eyebrow">Part II of Act Three</div>'),
    ("Act 3 Part II",  "Part II of Act Three",  '<div class="part-eyebrow">Part III of Act Three</div>'),
    ("Act 3 Part III", "Part III of Act Three", '<div class="curtain">Curtain.</div>'),
]


def strip_html(text):
    return re.sub(r'<[^>]+>', '', text)


def extract_speaker(speech_inner):
    """Pull the bare speaker name out of the <p class='speech'> inner HTML.

    Handles both <span class="speaker">NAME</span> and
    <span class="speaker">NAME <span class="as-role">(as ROLE)</span></span>.
    """
    m = re.search(r'<span class="speaker">(.*?)</span>(?:</span>)?',
                  speech_inner, flags=re.DOTALL)
    if not m:
        return None
    raw = m.group(1)
    if '<span class="as-role">' in raw:
        return raw.split('<span class="as-role">')[0].strip()
    text_before_tag = re.match(r'([^<]+)', raw)
    return (text_before_tag.group(1).strip() if text_before_tag else raw.strip())


def count_speech_words(speech_inner):
    """Count words in a speech, excluding the speaker span and stage actions."""
    s = re.sub(
        r'<span class="speaker">[^<]*(?:<span class="as-role">[^<]*</span>)?\s*</span>',
        '', speech_inner, count=1, flags=re.DOTALL,
    )
    s = re.sub(r'<span class="action">.*?</span>', '', s, flags=re.DOTALL)
    text = strip_html(s).strip().lstrip('.').strip()
    return len(text.split()) if text else 0


def count_chorus_words(chorus_html):
    return len(strip_html(chorus_html).split())


def find_part_boundaries(html):
    """Return {part_name: (start, end)} where start is just after the part's
    closing </aside> and end is the next part-eyebrow / curtain."""
    boundaries = {}
    for name, eyebrow_text, end_marker in PARTS:
        eb_pat = re.escape(f'<div class="part-eyebrow">{eyebrow_text}</div>')
        eb = re.search(eb_pat, html)
        if not eb:
            print(f"  WARN: missing eyebrow for {name}")
            continue
        aside_close = html.find('</aside>', eb.end())
        if aside_close == -1:
            print(f"  WARN: missing </aside> for {name}")
            continue
        end_idx = html.find(end_marker, aside_close)
        if end_idx == -1:
            print(f"  WARN: missing end marker for {name}")
            continue
        boundaries[name] = (aside_close + len('</aside>'), end_idx)
    return boundaries


SPEECH_AND_CHORUS_RE = re.compile(
    r'<p class="speech">(.*?)</p>'
    r'(\s*<div class="chorus-block">(.*?)</div>)?',
    re.DOTALL,
)


def count_part(chunk):
    counts = defaultdict(lambda: {'speeches': 0, 'words': 0})
    order = []
    for m in SPEECH_AND_CHORUS_RE.finditer(chunk):
        speaker = extract_speaker(m.group(1))
        if not speaker:
            continue
        if speaker not in counts:
            order.append(speaker)
        counts[speaker]['speeches'] += 1
        if m.group(3) is not None:
            counts[speaker]['words'] += count_chorus_words(m.group(3))
        else:
            counts[speaker]['words'] += count_speech_words(m.group(1))
    return OrderedDict((spk, counts[spk]) for spk in order)


def format_stats_block(part_counts):
    lines = []
    total_s = 0
    total_w = 0
    for spk, st in part_counts.items():
        s_label = "speech" if st['speeches'] == 1 else "speeches"
        w_label = "word" if st['words'] == 1 else "words"
        lines.append(
            f'        <li><span class="stats-name">{spk}</span>'
            f'<span class="stats-numbers">{st["speeches"]} {s_label} &middot; '
            f'{st["words"]:,} {w_label}</span></li>'
        )
        total_s += st['speeches']
        total_w += st['words']
    lines.append(
        f'        <li class="stats-total"><span class="stats-name">Total</span>'
        f'<span class="stats-numbers">{total_s} speeches &middot; '
        f'{total_w:,} words</span></li>'
    )
    return '\n'.join(lines)


def replace_stats_block(html, eyebrow_text, new_inner):
    eb_pat = re.escape(f'<div class="part-eyebrow">{eyebrow_text}</div>')
    eb = re.search(eb_pat, html)
    if not eb:
        return html
    ul_start = html.find('<ul class="stats-list">', eb.end())
    if ul_start == -1:
        return html
    ul_end = html.find('</ul>', ul_start)
    if ul_end == -1:
        return html
    new_chunk = '<ul class="stats-list">\n' + new_inner + '\n      </ul>'
    return html[:ul_start] + new_chunk + html[ul_end + len('</ul>'):]


def main():
    html = PLAY.read_text()
    boundaries = find_part_boundaries(html)

    per_part = OrderedDict()
    for name, eyebrow, _ in PARTS:
        if name not in boundaries:
            continue
        s, e = boundaries[name]
        per_part[name] = count_part(html[s:e])

    # Totals
    totals = defaultdict(lambda: {'speeches': 0, 'words': 0})
    for name, counts in per_part.items():
        for spk, st in counts.items():
            totals[spk]['speeches'] += st['speeches']
            totals[spk]['words'] += st['words']

    # Report
    print("=== Per-part counts ===")
    for name, counts in per_part.items():
        ts = sum(c['speeches'] for c in counts.values())
        tw = sum(c['words'] for c in counts.values())
        print(f"\n{name}: {ts} speeches, {tw:,} words")
        for spk, st in counts.items():
            print(f"  {spk:30s} {st['speeches']:4d}  {st['words']:6,}")

    print("\n=== Aggregated totals ===")
    for spk, st in sorted(totals.items(), key=lambda x: -x[1]['speeches']):
        print(f"  {spk:30s} {st['speeches']:4d}  {st['words']:6,}")

    # Apply HTML updates
    new_html = html
    for name, eyebrow, _ in PARTS:
        if name not in per_part:
            continue
        new_html = replace_stats_block(
            new_html, eyebrow, format_stats_block(per_part[name])
        )

    PLAY.write_text(new_html)
    print(f"\nUpdated {PLAY.name}")

    STATS.write_text(json.dumps(dict(totals), indent=2) + "\n")
    print(f"Updated data/{STATS.name}")


if __name__ == "__main__":
    main()
