#!/usr/bin/env python3
"""For every (long speech, shorter version) pair: keep only the shorter version,
re-styled as a normal speech paragraph. The original long versions are removed."""
import re
from pathlib import Path

SRC = Path("/home/claude/six_characters.html")
html = SRC.read_text()

# ---------------------------------------------------------------------------
# Convert the inner content of a speech-shorter paragraph into the inner
# content of a normal speech paragraph.
# ---------------------------------------------------------------------------
def convert_shorter_to_speech(shorter_html: str) -> str:
    new = shorter_html

    # 1. Drop the "Shorter" label entirely
    new = re.sub(r'<span class="ss-label">Shorter</span>\s*', '', new, count=1)

    # 2. Speaker tag with nested action: <span class="ss-speaker">SPEAKER <action>[X]</action>.</span>
    #    -> <span class="speaker">SPEAKER</span> <action>[X]</action>.
    new = re.sub(
        r'<span class="ss-speaker">([^<]+?) <span class="action">\[([^\]]+)\]</span>\.</span>',
        r'<span class="speaker">\1</span> <span class="action">[\2]</span>.',
        new
    )

    # 3. Speaker tag with simple period: <span class="ss-speaker">SPEAKER.</span>
    #    -> <span class="speaker">SPEAKER</span>.
    new = re.sub(
        r'<span class="ss-speaker">([^<]+?)\.</span>',
        r'<span class="speaker">\1</span>.',
        new
    )

    # 4. Outer wrapper: speech-shorter -> speech
    new = new.replace('<p class="speech-shorter">', '<p class="speech">', 1)

    return new

# ---------------------------------------------------------------------------
# Find every (long-speech, shorter) pair and collapse to just the shorter
# (re-styled as a real speech).
# ---------------------------------------------------------------------------
pair_pattern = re.compile(
    r'<p class="speech">.*?</p>\n  (<p class="speech-shorter">.*?</p>)',
    re.DOTALL
)

count = 0
def collapse(m):
    global count
    count += 1
    shorter = m.group(1)
    return convert_shorter_to_speech(shorter)

html = pair_pattern.sub(collapse, html)

# Sanity: there should be no .speech-shorter remaining
remaining = len(re.findall(r'<p class="speech-shorter">', html))
if remaining:
    print(f"!! Warning: {remaining} unprocessed .speech-shorter paragraphs still present.")
    # Print first one for inspection
    m = re.search(r'<p class="speech-shorter">.*?</p>', html, re.DOTALL)
    if m:
        print(f"   First: {m.group(0)[:200]}")

SRC.write_text(html)
print(f"File: {SRC} ({len(html):,} bytes, {html.count(chr(10)):,} lines)")
print(f"Pairs collapsed: {count}")
print(f"Remaining .speech-shorter: {remaining}")
