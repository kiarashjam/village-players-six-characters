#!/usr/bin/env python3
"""Replace each long speech with its shorter version, then delete the originals.
Uses negative-lookahead bounded matching so .*? cannot cross paragraph boundaries."""
import re
from pathlib import Path

SRC = Path("/home/claude/six_characters.html")
html = SRC.read_text()

original_len = len(html)
n_speech_before  = len(re.findall(r'<p class="speech">',         html))
n_shorter_before = len(re.findall(r'<p class="speech-shorter">', html))
print(f"Before: {n_speech_before} speeches, {n_shorter_before} shorters, {original_len:,} bytes")

def convert_shorter_to_speech(shorter_html: str) -> str:
    new = shorter_html

    # Drop the "Shorter" label
    new = re.sub(r'<span class="ss-label">Shorter</span>\s*', '', new, count=1)

    # Speaker with nested action span: <span class="ss-speaker">SPEAKER <action>[X]</action>.</span>
    new = re.sub(
        r'<span class="ss-speaker">([^<]+?) <span class="action">\[([^\]]+)\]</span>\.</span>',
        r'<span class="speaker">\1</span> <span class="action">[\2]</span>.',
        new
    )

    # Simple speaker:  <span class="ss-speaker">SPEAKER.</span>
    new = re.sub(
        r'<span class="ss-speaker">([^<]+?)\.</span>',
        r'<span class="speaker">\1</span>.',
        new
    )

    # Outer class
    new = new.replace('<p class="speech-shorter">', '<p class="speech">', 1)
    return new

# Bounded regex: .*? cannot contain another <p class="speech"> opening tag,
# so the long speech only matches its own content.
pair_pattern = re.compile(
    r'<p class="speech">'
    r'(?:(?!<p class="speech">).)*?'
    r'</p>\s*\n\s*'
    r'(<p class="speech-shorter">.*?</p>)',
    re.DOTALL
)

count = 0
def collapse(m):
    global count
    count += 1
    shorter = m.group(1)
    return convert_shorter_to_speech(shorter)

html = pair_pattern.sub(collapse, html)

n_speech_after  = len(re.findall(r'<p class="speech">',         html))
n_shorter_after = len(re.findall(r'<p class="speech-shorter">', html))
SRC.write_text(html)
print(f"Pairs collapsed: {count}")
print(f"After:  {n_speech_after} speeches, {n_shorter_after} shorters, {len(html):,} bytes")
print(f"Net speech change: {n_speech_after - n_speech_before}  (expect -{count} since each pair: removed 1 long + 1 shorter, added 1 new speech)")
