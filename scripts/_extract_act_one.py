#!/usr/bin/env python3
"""Extract every speech in Act One (speaker + plain dialogue) to JSON."""
from pathlib import Path
import re, json

SRC = Path(__file__).resolve().parent.parent / "six_characters_village_players.html"
html = SRC.read_text(encoding="utf-8")

# Slice Act One: from <article id="act-1"> up to <article id="act-2">
start = html.index('id="act-1"')
end = html.index('id="act-2"')
act = html[start:end]

speeches = []
for m in re.finditer(r'<p class="speech">(.*?)</p>', act, re.DOTALL):
    block = m.group(1)
    # speaker (including nested (as Role))
    sp = re.search(r'<span class="speaker">(.*?)</span>(?:</span>)?', block, re.DOTALL)
    speaker = re.sub(r'<[^>]+>', '', sp.group(0)).strip() if sp else "?"
    # dialogue = block minus speaker label
    body = re.sub(r'<span class="speaker">.*?</span>(?:</span>)?\s*\.?\s*', '', block, count=1, flags=re.DOTALL)
    # remove stage-direction action spans entirely
    body = re.sub(r'<span class="action">.*?</span>', '', body, flags=re.DOTALL)
    # strip remaining tags, collapse whitespace
    plain = re.sub(r'<[^>]+>', '', body)
    plain = re.sub(r'\s+', ' ', plain).strip()
    if plain:
        speeches.append({"n": len(speeches) + 1, "speaker": speaker, "text": plain})

out = Path(__file__).resolve().parent.parent / "data" / "act_one_speeches.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(speeches, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Extracted {len(speeches)} speeches -> {out}")
for s in speeches:
    print(f'{s["n"]:>3}. {s["speaker"]}: {s["text"][:90]}')
