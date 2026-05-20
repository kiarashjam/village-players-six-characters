#!/usr/bin/env python3
"""Rebuild six_characters.html with a vastly improved reading UI.
Preserves all dialogue and director's notes — only changes <head>, adds reader chrome,
and lightly enhances a few in-body elements (drop caps, scene tags)."""

import re
from pathlib import Path

src_path = Path("/home/claude/six_characters.html")
out_path = Path("/home/claude/six_characters.html")  # overwrite

src = src_path.read_text()

# Extract the body content (everything between <body> and </body>, excluding the <main>
# wrapper — we'll re-wrap it ourselves to insert chrome).
m_body_open  = src.find("<body>") + len("<body>")
m_body_close = src.rfind("</body>")
body_inner   = src[m_body_open:m_body_close].strip()

# Strip the existing <main>...</main> wrapper from the inner body so we control wrapping.
# The first non-whitespace token should be <main>.
body_inner = re.sub(r"^\s*<main>\s*", "", body_inner)
body_inner = re.sub(r"\s*</main>\s*$", "", body_inner)

# Add a class to the first stage-direction paragraph of each act so we can drop-cap it.
# Act I — "The spectators will find the curtain raised..."
# Act II — "The stage call-bells ring..."
# Act III — "When the curtain goes up again..."
body_inner = re.sub(
    r'(<p class="stage")(>The spectators will find)',
    r'\1 data-opener="1"\2',
    body_inner, count=1
)
body_inner = re.sub(
    r'(<p class="stage")(>The stage call-bells ring)',
    r'\1 data-opener="1"\2',
    body_inner, count=1
)
body_inner = re.sub(
    r'(<p class="stage")(>When the curtain goes up again)',
    r'\1 data-opener="1"\2',
    body_inner, count=1
)

# Wrap each act in an <article id="act-1|2|3"> so the floating nav can jump to it.
# Find the three <!-- ============ ACT ... ============ --> markers.
def wrap_acts(text):
    # Replace markers and inject <article> open/close.
    text = text.replace(
        "<!-- ============ ACT I ============ -->",
        '</section><!-- preface end -->\n  <article id="act-1" class="act">'
    )
    text = text.replace(
        "<!-- ============ ACT II ============ -->",
        '</article>\n  <article id="act-2" class="act">'
    )
    text = text.replace(
        "<!-- ============ ACT III ============ -->",
        '</article>\n  <article id="act-3" class="act">'
    )
    return text

# Wrap the front matter (cover + cast + scene-setting) inside a <section class="preface">.
# Easiest: open <section class="preface"> after the start, and our wrap_acts() above will
# close it with the </section> token right before Act I opens.
body_inner = '<section class="preface">\n' + body_inner
body_inner = wrap_acts(body_inner)

# Add a closing </article> at the end (after Act III, before the colophon if any).
# Find the colophon and inject </article> before it.
if 'class="colophon"' in body_inner:
    body_inner = body_inner.replace(
        '<div class="colophon"',
        '</article>\n  <div class="colophon"',
        1
    )
else:
    # Otherwise just append the closing tag at the end
    body_inner = body_inner + "\n  </article>"

# ---------------------------------------------------------------------------
# Build the new <head> + chrome + closing script.
# ---------------------------------------------------------------------------

HEAD = r"""<!DOCTYPE html>
<html lang="en" data-theme="day" data-size="medium" data-width="comfortable">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Six Characters in Search of an Author — Pirandello</title>
<meta name="description" content="A reading edition of Luigi Pirandello's 1921 metatheatrical comedy, translated by Edward Storer, with director's notes by Kiarash Jamishidi.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500&family=Cormorant+Unicase:wght@300;400;500;600;700&family=Cormorant+Infant:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">
<style>

/* =========================================================================
   THEMES — three carefully calibrated palettes for different reading hours
   ========================================================================= */

:root,
[data-theme="day"] {
  --paper:        #efe6cf;
  --paper-warm:   #e8dec3;
  --paper-deep:   #e2d6b6;
  --ink:          #1c160d;
  --ink-soft:     #574736;
  --ink-faint:    #8a7558;
  --accent:       #832027;
  --accent-deep:  #5e1517;
  --accent-soft:  #b04a3d;
  --gold:         #95762e;
  --gold-soft:    #b89544;
  --rule:         rgba(28, 22, 13, 0.18);
  --rule-strong:  rgba(28, 22, 13, 0.32);
  --grain-opacity: 0.5;
  --noise-tone:   "0 0 0 0 0.10  0 0 0 0 0.08  0 0 0 0 0.05  0 0 0 0.06 0";
  --shadow:       0 1px 0 rgba(28,22,13,0.04), 0 30px 80px -40px rgba(28,22,13,0.25);
  color-scheme: light;
}

[data-theme="dusk"] {
  --paper:        #2c2419;
  --paper-warm:   #322a1e;
  --paper-deep:   #261e14;
  --ink:          #ecdcb6;
  --ink-soft:     #bda783;
  --ink-faint:    #897962;
  --accent:       #c46b56;
  --accent-deep:  #9e4938;
  --accent-soft:  #d4866e;
  --gold:         #c89e51;
  --gold-soft:    #e0b96a;
  --rule:         rgba(236, 220, 182, 0.16);
  --rule-strong:  rgba(236, 220, 182, 0.32);
  --grain-opacity: 0.35;
  --shadow:       0 1px 0 rgba(0,0,0,0.2), 0 30px 80px -40px rgba(0,0,0,0.6);
  color-scheme: dark;
}

[data-theme="night"] {
  --paper:        #14110d;
  --paper-warm:   #1a1611;
  --paper-deep:   #100d09;
  --ink:          #e6d9b7;
  --ink-soft:     #a89578;
  --ink-faint:    #756450;
  --accent:       #b6493d;
  --accent-deep:  #8a3429;
  --accent-soft:  #c97062;
  --gold:         #c2944a;
  --gold-soft:    #d6ad65;
  --rule:         rgba(230, 217, 183, 0.14);
  --rule-strong:  rgba(230, 217, 183, 0.30);
  --grain-opacity: 0.22;
  --shadow:       0 1px 0 rgba(0,0,0,0.4), 0 30px 80px -40px rgba(0,0,0,0.8);
  color-scheme: dark;
}

/* Reading-size knobs */
[data-size="small"]  { --base-fs: 17px; --base-lh: 1.65; --measure: 640px; }
[data-size="medium"] { --base-fs: 19px; --base-lh: 1.7;  --measure: 720px; }
[data-size="large"]  { --base-fs: 21px; --base-lh: 1.72; --measure: 760px; }

[data-width="narrow"]     { --measure: 580px; }
[data-width="comfortable"] {}
[data-width="wide"]       { --measure: 820px; }

/* =========================================================================
   RESET + BASE
   ========================================================================= */
*, *::before, *::after { box-sizing: border-box; }

html {
  scroll-behavior: smooth;
  scroll-padding-top: 80px;
}

body {
  margin: 0;
  background:
    radial-gradient(circle at 18% 8%, color-mix(in srgb, var(--gold) 10%, transparent), transparent 55%),
    radial-gradient(circle at 82% 88%, color-mix(in srgb, var(--accent) 8%, transparent), transparent 55%),
    var(--paper);
  color: var(--ink);
  font-family: 'EB Garamond', 'Cormorant Garamond', Georgia, serif;
  font-size: var(--base-fs, 19px);
  line-height: var(--base-lh, 1.7);
  font-feature-settings: "liga" 1, "kern" 1, "onum" 1, "calt" 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  transition: background-color 600ms ease, color 600ms ease;
  overflow-x: hidden;
}

/* Subtle paper grain over everything */
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.1  0 0 0 0 0.08  0 0 0 0 0.05  0 0 0 0.07 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  opacity: var(--grain-opacity);
  z-index: 1;
  mix-blend-mode: multiply;
}
[data-theme="dusk"] body::before,
[data-theme="night"] body::before {
  mix-blend-mode: overlay;
}

::selection {
  background: color-mix(in srgb, var(--accent) 35%, transparent);
  color: var(--ink);
}

/* =========================================================================
   READER CHROME — progress bar, controls, floating act indicator
   ========================================================================= */
.r-progress {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 2px;
  z-index: 100;
  pointer-events: none;
  background: transparent;
}
.r-progress::after {
  content: "";
  display: block;
  height: 100%;
  width: var(--progress, 0%);
  background: linear-gradient(90deg, var(--gold-soft), var(--accent));
  transition: width 80ms linear;
}

.r-controls {
  position: fixed;
  top: 18px;
  right: 18px;
  z-index: 50;
  display: flex;
  gap: 6px;
  padding: 6px;
  background: color-mix(in srgb, var(--paper) 92%, transparent);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid var(--rule);
  border-radius: 999px;
  box-shadow: var(--shadow);
}
.r-controls button,
.r-controls .r-divider {
  appearance: none;
  background: transparent;
  border: 0;
  color: var(--ink-soft);
  font-family: 'Cormorant Unicase', 'EB Garamond', serif;
  font-size: 11px;
  letter-spacing: 0.18em;
  padding: 9px 12px;
  cursor: pointer;
  border-radius: 999px;
  transition: background 200ms ease, color 200ms ease;
  text-transform: uppercase;
  font-weight: 500;
  line-height: 1;
}
.r-controls button:hover {
  background: color-mix(in srgb, var(--accent) 14%, transparent);
  color: var(--accent);
}
.r-controls button.active {
  background: color-mix(in srgb, var(--accent) 16%, transparent);
  color: var(--accent);
}
.r-controls .r-divider {
  width: 1px;
  padding: 0;
  margin: 6px 2px;
  background: var(--rule);
  pointer-events: none;
}
.r-controls .icon {
  display: inline-block;
  width: 14px; height: 14px;
  vertical-align: -2px;
}

.r-act-pin {
  position: fixed;
  right: 22px;
  bottom: 22px;
  z-index: 50;
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: flex-end;
  padding: 14px 18px;
  background: color-mix(in srgb, var(--paper) 92%, transparent);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid var(--rule);
  border-radius: 14px;
  box-shadow: var(--shadow);
  font-family: 'Cormorant Unicase', serif;
  font-size: 10px;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: var(--ink-faint);
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 400ms ease, transform 400ms ease;
  pointer-events: none;
}
.r-act-pin.visible {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}
.r-act-pin .label {
  font-size: 9px;
  color: var(--ink-faint);
}
.r-act-pin .value {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  font-weight: 400;
  letter-spacing: 0.08em;
  color: var(--accent);
  font-feature-settings: "smcp" 0;
  text-transform: none;
  font-style: italic;
}
.r-act-pin button {
  appearance: none;
  background: transparent;
  border: 0;
  font: inherit;
  color: inherit;
  padding: 4px 6px;
  cursor: pointer;
  letter-spacing: 0.32em;
  border-radius: 6px;
  transition: color 200ms ease;
}
.r-act-pin button:hover { color: var(--accent); }
.r-act-pin .acts {
  display: flex;
  gap: 0;
  margin-top: 8px;
  border-top: 1px solid var(--rule);
  padding-top: 8px;
}
.r-act-pin .acts button + button {
  border-left: 1px solid var(--rule);
}

/* =========================================================================
   LAYOUT
   ========================================================================= */
main {
  position: relative;
  z-index: 2;
  max-width: var(--measure, 720px);
  margin: 0 auto;
  padding: 88px 28px 160px;
  transition: max-width 400ms ease;
}

/* =========================================================================
   COVER — title page composed like a private edition
   ========================================================================= */
.cover {
  text-align: center;
  padding: 90px 0 110px;
  position: relative;
  border-bottom: 1px solid var(--rule);
  margin-bottom: 80px;
  opacity: 0;
  animation: fadeUp 1100ms cubic-bezier(0.2, 0.7, 0.2, 1) 100ms forwards;
}
.cover::before,
.cover::after {
  content: "";
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 56px;
  height: 1px;
  background: var(--accent);
  opacity: 0.5;
}
.cover::before { top: 24px; }
.cover::after  { bottom: 24px; }

.cover .eyebrow {
  font-family: 'Cormorant Unicase', 'EB Garamond', serif;
  font-size: 11px;
  letter-spacing: 0.5em;
  color: var(--accent);
  margin-bottom: 56px;
  font-weight: 500;
  text-transform: uppercase;
}

/* SVG curtain motif behind the title */
.cover-curtain {
  display: block;
  margin: 0 auto 36px;
  width: 110px;
  height: auto;
  opacity: 0.85;
}

.cover h1 {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 300;
  font-size: clamp(44px, 7.6vw, 76px);
  line-height: 1.02;
  margin: 0 0 22px;
  letter-spacing: -0.012em;
  color: var(--ink);
}
.cover h1 .h1-italic {
  font-style: italic;
  color: var(--accent);
  font-weight: 400;
}
.cover .italian {
  font-family: 'Cormorant Infant', 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: clamp(20px, 2.5vw, 26px);
  color: var(--ink-soft);
  margin: 0 0 56px;
  font-weight: 300;
  letter-spacing: 0.01em;
}
.cover .subtitle {
  font-family: 'Cormorant Unicase', serif;
  font-size: 11px;
  letter-spacing: 0.55em;
  color: var(--ink-soft);
  margin: 0 0 64px;
  text-transform: uppercase;
  font-weight: 500;
}
.cover .ornament {
  color: var(--accent);
  font-size: 22px;
  margin: 32px 0;
  letter-spacing: 0.6em;
  opacity: 0.7;
}
.cover .author {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(28px, 3.2vw, 34px);
  font-weight: 400;
  margin: 0 0 6px;
  letter-spacing: 0.02em;
}
.cover .translator {
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
  font-style: italic;
  font-size: 17px;
  color: var(--ink-soft);
  margin: 0 0 64px;
  font-weight: 300;
}
.cover .director-credit {
  font-family: 'Cormorant Unicase', serif;
  font-size: 10px;
  letter-spacing: 0.4em;
  color: var(--ink-soft);
  border-top: 1px solid var(--rule);
  padding-top: 26px;
  margin: 56px auto 0;
  display: inline-block;
  text-transform: uppercase;
}
.cover .director-credit .name {
  color: var(--accent);
  font-weight: 600;
}
.cover .pub {
  font-size: 13px;
  color: var(--ink-faint);
  font-style: italic;
  margin-top: 30px;
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
  letter-spacing: 0.04em;
}
.cover .roman-year {
  display: block;
  font-family: 'Cormorant Unicase', serif;
  font-size: 11px;
  letter-spacing: 0.5em;
  color: var(--accent);
  margin-top: 8px;
  font-style: normal;
}

/* =========================================================================
   CAST — dramatis personae
   ========================================================================= */
.cast {
  margin: 80px 0;
  padding: 56px 0;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
  position: relative;
}
.cast h2 {
  font-family: 'Cormorant Unicase', serif;
  font-size: 11px;
  letter-spacing: 0.5em;
  color: var(--accent);
  font-weight: 500;
  text-align: center;
  margin: 0 0 10px;
  text-transform: uppercase;
}
.cast .cast-sub {
  text-align: center;
  font-style: italic;
  color: var(--ink-soft);
  margin-bottom: 40px;
  font-size: 16px;
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
}
.cast .cast-group + .cast-group { margin-top: 44px; }
.cast ul {
  list-style: none;
  padding: 0;
  margin: 0;
  columns: 2;
  column-gap: 56px;
  text-align: center;
}
.cast li {
  font-family: 'Cormorant Garamond', 'EB Garamond', serif;
  font-variant: small-caps;
  letter-spacing: 0.08em;
  font-size: 16px;
  padding: 5px 0;
  break-inside: avoid;
  color: var(--ink);
  font-weight: 500;
  transition: color 200ms ease;
}
.cast li:hover {
  color: var(--accent);
}
.cast li .silent {
  display: block;
  font-style: italic;
  font-size: 12px;
  letter-spacing: 0.05em;
  color: var(--ink-faint);
  font-variant: normal;
  margin-top: 2px;
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
}

/* Scene setting card */
.scene-setting {
  margin: 0 auto 80px;
  max-width: 540px;
  text-align: center;
}
.scene-setting .daytime {
  font-family: 'Cormorant Unicase', serif;
  font-size: 11px;
  letter-spacing: 0.5em;
  color: var(--accent);
  margin-bottom: 22px;
  text-transform: uppercase;
  font-weight: 500;
}
.scene-setting .nb {
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
  font-style: italic;
  color: var(--ink-soft);
  font-size: 15.5px;
  line-height: 1.7;
  margin: 0;
  padding: 24px 36px;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}

/* =========================================================================
   ACT HEADER — Roman numeral, theatrical announcement
   ========================================================================= */
.act-header {
  text-align: center;
  margin: 120px 0 56px;
  position: relative;
}
.act-header::before,
.act-header::after {
  content: "";
  display: block;
  width: 1px;
  height: 36px;
  background: var(--accent);
  margin: 0 auto;
  opacity: 0.4;
}
.act-header::before { margin-bottom: 28px; }
.act-header::after  { margin-top: 28px; }
.act-header .label {
  font-family: 'Cormorant Unicase', serif;
  font-size: 11px;
  letter-spacing: 0.55em;
  color: var(--accent);
  margin-bottom: 14px;
  text-transform: uppercase;
  font-weight: 500;
}
.act-header .numeral {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 300;
  font-size: clamp(72px, 11vw, 120px);
  line-height: 1;
  margin: 0;
  color: var(--ink);
  font-style: italic;
  letter-spacing: 0.04em;
}
.act-header .ornament {
  color: var(--accent);
  font-size: 18px;
  margin-top: 22px;
  letter-spacing: 0.6em;
  opacity: 0.6;
}

/* =========================================================================
   DIRECTOR'S NOTES — set apart like an inserted manuscript page
   ========================================================================= */
.directors-note {
  margin: 56px 0 72px;
  padding: 44px 44px 42px;
  background: color-mix(in srgb, var(--paper-warm) 70%, var(--paper));
  border: 1px solid var(--rule);
  border-radius: 2px;
  position: relative;
  box-shadow: 0 1px 0 var(--rule),
              0 24px 60px -36px color-mix(in srgb, var(--ink) 30%, transparent);
}
.directors-note::before {
  content: "";
  position: absolute;
  left: 0; right: 0;
  top: 0;
  height: 2px;
  background: linear-gradient(90deg,
    transparent, var(--gold) 18%, var(--gold) 82%, transparent);
  opacity: 0.7;
}
.directors-note::after {
  content: "K. J.";
  position: absolute;
  top: 14px;
  right: 20px;
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
  font-style: italic;
  font-size: 11px;
  color: var(--gold);
  letter-spacing: 0.18em;
  opacity: 0.7;
}
.directors-note .note-eyebrow {
  font-family: 'Cormorant Unicase', serif;
  font-size: 10px;
  letter-spacing: 0.45em;
  color: var(--gold);
  margin-bottom: 14px;
  text-transform: uppercase;
  font-weight: 500;
}
.directors-note h3 {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 400;
  font-style: italic;
  font-size: clamp(22px, 2.6vw, 28px);
  line-height: 1.3;
  margin: 0 0 24px;
  color: var(--ink);
  letter-spacing: 0;
}
.directors-note h3 .by {
  color: var(--ink-faint);
  font-size: 0.7em;
  font-style: italic;
  display: block;
  margin-top: 6px;
  letter-spacing: 0.02em;
}
.directors-note p {
  font-family: 'Cormorant Garamond', 'EB Garamond', serif;
  font-style: italic;
  font-size: calc(var(--base-fs, 19px) * 0.94);
  line-height: 1.78;
  color: var(--ink-soft);
  margin: 0 0 16px;
  text-align: left;
}
.directors-note p:last-child { margin-bottom: 0; }
.directors-note em { font-style: normal; color: var(--accent); }

/* =========================================================================
   DIALOGUE — speakers, stage directions, asides
   ========================================================================= */

.speech {
  margin: 0 0 14px;
  text-align: justify;
  hyphens: auto;
  -webkit-hyphens: auto;
}
.speaker {
  font-family: 'Cormorant Garamond', 'EB Garamond', serif;
  font-variant: small-caps;
  font-feature-settings: "smcp" 1, "c2sc" 1;
  letter-spacing: 0.1em;
  font-weight: 600;
  color: var(--accent);
  white-space: nowrap;
}
.action {
  font-style: italic;
  color: var(--ink-faint);
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
  font-size: 0.94em;
}
.action strong {
  font-weight: 600;
  font-style: italic;
  font-variant: small-caps;
  letter-spacing: 0.06em;
  color: var(--ink-soft);
}

.stage {
  font-style: italic;
  color: var(--ink-soft);
  border-left: 2px solid var(--accent);
  padding: 4px 0 4px 18px;
  margin: 22px 0 22px 4px;
  font-family: 'Cormorant Garamond', 'EB Garamond', serif;
  font-size: 0.96em;
  line-height: 1.65;
  background: linear-gradient(90deg,
    color-mix(in srgb, var(--accent) 4%, transparent),
    transparent 80%);
}
.stage strong {
  font-style: italic;
  font-variant: small-caps;
  letter-spacing: 0.06em;
  color: var(--accent);
  font-weight: 500;
}

/* DROP CAP — first stage direction of each act */
.stage[data-opener="1"] {
  border-left: 0;
  padding-left: 0;
  background: none;
  margin-top: 10px;
  font-size: 1em;
}
.stage[data-opener="1"]::first-letter {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-weight: 400;
  font-size: 5.6em;
  line-height: 0.86;
  float: left;
  padding: 6px 14px 0 0;
  color: var(--accent);
  font-feature-settings: "swsh" 1;
}

.song {
  font-family: 'Cormorant Infant', 'Cormorant Garamond', serif;
  font-style: italic;
  text-align: center;
  margin: 18px auto;
  max-width: 80%;
  color: var(--ink-soft);
  font-size: 0.96em;
  line-height: 1.55;
  padding: 10px 0;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
.chorus-block {
  font-family: 'Cormorant Garamond', 'EB Garamond', serif;
  font-style: italic;
  color: var(--ink-soft);
  margin: 8px 0;
  padding-left: 20px;
}
.chorus-block .speaker {
  font-style: normal;
}
.chorus-block .line {
  display: block;
  padding: 1px 0;
}

/* =========================================================================
   CURTAIN markers + interludes
   ========================================================================= */
.curtain {
  text-align: center;
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 22px;
  color: var(--accent);
  margin: 48px auto;
  letter-spacing: 0.06em;
  position: relative;
  padding: 16px 0;
  max-width: 200px;
  border-top: 1px solid var(--accent);
  border-bottom: 1px solid var(--accent);
  border-left: 0;
  background: none;
}
.curtain::before {
  content: "✦";
  display: block;
  font-size: 11px;
  color: var(--accent);
  margin-bottom: 4px;
  letter-spacing: 0;
  opacity: 0.6;
}

.pause-note {
  text-align: center;
  font-style: italic;
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
  color: var(--ink-faint);
  font-size: 0.92em;
  margin: 32px auto;
  max-width: 60%;
  padding: 18px 0;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}

/* =========================================================================
   COLOPHON
   ========================================================================= */
.colophon {
  margin: 120px auto 0;
  padding-top: 56px;
  border-top: 1px solid var(--rule);
  text-align: center;
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
  font-style: italic;
  font-size: 14px;
  color: var(--ink-faint);
  line-height: 1.65;
}
.colophon a {
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid color-mix(in srgb, var(--accent) 40%, transparent);
  transition: border-bottom-color 200ms ease;
}
.colophon a:hover { border-bottom-color: var(--accent); }
.colophon .mark {
  display: block;
  color: var(--accent);
  font-family: 'Cormorant Unicase', serif;
  font-size: 10px;
  letter-spacing: 0.5em;
  margin-bottom: 18px;
  text-transform: uppercase;
  font-style: normal;
}

/* =========================================================================
   ACT WRAPPER — quietly demarcates each act for navigation
   ========================================================================= */
.act { scroll-margin-top: 80px; }

/* =========================================================================
   RESPONSIVE
   ========================================================================= */
@media (max-width: 720px) {
  main { padding: 64px 22px 100px; }
  .cover { padding: 56px 0 70px; }
  .cast ul { columns: 1; }
  .directors-note { padding: 32px 26px; }
  .directors-note::after { display: none; }
  .r-controls {
    top: auto;
    bottom: 14px;
    right: 50%;
    transform: translateX(50%);
    padding: 4px;
  }
  .r-controls button { padding: 8px 10px; font-size: 10px; }
  .r-act-pin {
    right: 14px;
    bottom: 72px;
    padding: 10px 14px;
  }
  .stage[data-opener="1"]::first-letter {
    font-size: 4.4em;
  }
}

/* Reduce motion preference */
@media (prefers-reduced-motion: reduce) {
  .cover { animation: none; opacity: 1; }
  * { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
}

/* =========================================================================
   ANIMATIONS
   ========================================================================= */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Print styles — clean output if anyone wants paper */
@media print {
  body { background: #fff; color: #000; }
  body::before, .r-progress, .r-controls, .r-act-pin { display: none !important; }
  main { max-width: 100%; padding: 0; }
  .directors-note { break-inside: avoid; box-shadow: none; }
  .act-header, .cover { break-after: page; }
}

</style>
</head>
<body>

<!-- ========== READER CHROME ========== -->
<div class="r-progress" aria-hidden="true"></div>

<nav class="r-controls" aria-label="Reader controls">
  <button class="r-theme" data-theme-value="day" title="Day theme">Day</button>
  <button class="r-theme" data-theme-value="dusk" title="Dusk theme">Dusk</button>
  <button class="r-theme" data-theme-value="night" title="Night theme">Night</button>
  <span class="r-divider"></span>
  <button class="r-size" data-size-value="small" title="Smaller text">A&minus;</button>
  <button class="r-size" data-size-value="medium" title="Medium text">A</button>
  <button class="r-size" data-size-value="large" title="Larger text">A+</button>
</nav>

<aside class="r-act-pin" id="actPin" aria-label="Act navigation">
  <span class="label">You are reading</span>
  <span class="value" id="actPinValue">Preface</span>
  <div class="acts">
    <button data-jump="act-1">I</button>
    <button data-jump="act-2">II</button>
    <button data-jump="act-3">III</button>
  </div>
</aside>

<main>
"""

# ----- CURTAIN SVG inserted into the cover -----
# We splice an SVG curtain motif into the cover by replacing the ornament line.
# The motif: two stylized curtain panels with a central tieback.
CURTAIN_SVG = """  <svg class="cover-curtain" viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <defs>
      <linearGradient id="cg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="currentColor" stop-opacity="0.85"/>
        <stop offset="100%" stop-color="currentColor" stop-opacity="0.35"/>
      </linearGradient>
    </defs>
    <g fill="none" stroke="currentColor" stroke-width="0.7" opacity="0.8">
      <path d="M10 6 Q12 30 14 54 Q16 72 18 76" />
      <path d="M22 6 Q24 30 26 54 Q28 72 30 76" />
      <path d="M34 6 Q36 30 38 54 Q40 72 42 76" />
      <path d="M78 6 Q80 30 82 54 Q84 72 86 76" />
      <path d="M90 6 Q92 30 94 54 Q96 72 98 76" />
      <path d="M102 6 Q104 30 106 54 Q108 72 110 76" />
    </g>
    <line x1="6" y1="6" x2="114" y2="6" stroke="currentColor" stroke-width="1.1"/>
    <circle cx="60" cy="42" r="2.2" fill="currentColor"/>
    <line x1="48" y1="42" x2="72" y2="42" stroke="currentColor" stroke-width="0.6" opacity="0.55"/>
  </svg>"""

# Replace the existing cover ornament div with the curtain SVG + ornament for variety
body_inner = body_inner.replace(
    '<div class="eyebrow">Project Gutenberg Australia &nbsp;·&nbsp; A Treasure-Trove of Literature</div>\n    <h1>',
    f'<div class="eyebrow">A Reading Edition</div>\n{CURTAIN_SVG}\n    <h1>'
)

# Add a roman year under the pub line for atmosphere
body_inner = body_inner.replace(
    '<p class="pub">Published 1921 &nbsp;·&nbsp; eBook No. 0608521h</p>',
    '<p class="pub">Published 1921 &nbsp;·&nbsp; eBook No. 0608521h<span class="roman-year">MCMXXI &nbsp; · &nbsp; ROMA</span></p>'
)

# Apply 'mark' class header to colophon if present
body_inner = body_inner.replace(
    '<div class="colophon">',
    '<div class="colophon">\n  <span class="mark">Colophon</span>'
)
# Remove duplicate "mark" insertions if any (defensive — only insert if not already there)
body_inner = body_inner.replace(
    '<span class="mark">Colophon</span>\n  <span class="mark">Colophon</span>',
    '<span class="mark">Colophon</span>'
)

FOOT = r"""
</main>

<script>
(function () {
  'use strict';

  var root = document.documentElement;
  var KEY_T = 'six-chars-theme';
  var KEY_S = 'six-chars-size';

  // Restore prefs
  try {
    var t = localStorage.getItem(KEY_T);
    var s = localStorage.getItem(KEY_S);
    if (t) root.setAttribute('data-theme', t);
    if (s) root.setAttribute('data-size', s);
  } catch (e) {}

  function setActiveButtons() {
    var theme = root.getAttribute('data-theme') || 'day';
    var size  = root.getAttribute('data-size')  || 'medium';
    document.querySelectorAll('.r-theme').forEach(function (b) {
      b.classList.toggle('active', b.dataset.themeValue === theme);
    });
    document.querySelectorAll('.r-size').forEach(function (b) {
      b.classList.toggle('active', b.dataset.sizeValue === size);
    });
  }

  document.querySelectorAll('.r-theme').forEach(function (b) {
    b.addEventListener('click', function () {
      root.setAttribute('data-theme', b.dataset.themeValue);
      try { localStorage.setItem(KEY_T, b.dataset.themeValue); } catch (e) {}
      setActiveButtons();
    });
  });

  document.querySelectorAll('.r-size').forEach(function (b) {
    b.addEventListener('click', function () {
      root.setAttribute('data-size', b.dataset.sizeValue);
      try { localStorage.setItem(KEY_S, b.dataset.sizeValue); } catch (e) {}
      setActiveButtons();
    });
  });

  setActiveButtons();

  // -------- Reading progress bar --------
  var progress = document.querySelector('.r-progress');
  function updateProgress() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var pct = max > 0 ? (h.scrollTop / max) * 100 : 0;
    progress.style.setProperty('--progress', pct.toFixed(2) + '%');
  }
  document.addEventListener('scroll', updateProgress, { passive: true });
  window.addEventListener('resize', updateProgress);
  updateProgress();

  // -------- Floating act pin --------
  var pin = document.getElementById('actPin');
  var pinValue = document.getElementById('actPinValue');
  var acts = [
    { id: 'act-1', label: 'Act I' },
    { id: 'act-2', label: 'Act II' },
    { id: 'act-3', label: 'Act III' }
  ];

  function getCurrentAct() {
    var top = window.scrollY + 120;
    var current = null;
    acts.forEach(function (a) {
      var el = document.getElementById(a.id);
      if (el && el.offsetTop <= top) current = a;
    });
    return current;
  }

  function refreshPin() {
    var cur = getCurrentAct();
    if (!cur) {
      pin.classList.remove('visible');
      pinValue.textContent = 'Preface';
      return;
    }
    if (window.scrollY < 200) {
      pin.classList.remove('visible');
      return;
    }
    pin.classList.add('visible');
    pinValue.textContent = cur.label;
  }
  document.addEventListener('scroll', refreshPin, { passive: true });
  refreshPin();

  document.querySelectorAll('[data-jump]').forEach(function (b) {
    b.addEventListener('click', function () {
      var el = document.getElementById(b.dataset.jump);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // -------- Keyboard shortcuts --------
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var tag = document.activeElement && document.activeElement.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA') return;
    if (e.key === '1') document.getElementById('act-1').scrollIntoView({ behavior: 'smooth' });
    else if (e.key === '2') document.getElementById('act-2').scrollIntoView({ behavior: 'smooth' });
    else if (e.key === '3') document.getElementById('act-3').scrollIntoView({ behavior: 'smooth' });
    else if (e.key === 't' || e.key === 'T') {
      var cur = root.getAttribute('data-theme') || 'day';
      var next = cur === 'day' ? 'dusk' : cur === 'dusk' ? 'night' : 'day';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem(KEY_T, next); } catch (e) {}
      setActiveButtons();
    }
  });
})();
</script>

</body>
</html>
"""

# Assemble the new file
new_html = HEAD + "\n" + body_inner + "\n" + FOOT

# Write it
out_path.write_text(new_html)
print(f"Wrote {out_path}: {len(new_html):,} bytes")
print(f"Body content preserved: {len(body_inner):,} bytes")
