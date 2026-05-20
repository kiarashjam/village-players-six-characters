# Six Characters in Search of an Author

**A Village Players production · Lausanne · late autumn 2026**

A director's edition of Luigi Pirandello's *Sei personaggi in cerca d'autore* (1921), in the Edward Storer 1922 English translation, prepared for a Lausanne staging by the Village Players. The English has been tightened and modernised; the production is set in Lausanne (Madame Pace's shop on the rue de Bourg, francs instead of lire); the Players have been compressed to three tracks doubling several roles each; the comedy has been punched; the staging has been stripped to one defining visual per act.

Eight live performers. Three acts with intervals. Mostly black-box minimalist. Lighting and music carry much of the storytelling. A short run of three or four performances.

---

## Structure

```
six_characters_village_players.html    The working director's edition (open in any browser)

outputs/                               Generated PDFs, ready to share
├── six_characters.pdf                 Full director's edition · 78 pages
├── audition_call.pdf                  Casting call with cold-read lines · 11 pages
├── audition_packet_trimmed.pdf        Casting packet without front-matter, with summary page · 11 pages
├── sides_templates.pdf                Blank fill-in templates, one page per role · 8 pages
├── scene_index.pdf                    Speech-locator reference for assembling sides locally · 2 pages
└── production_summary.pdf             Short publication blurb for press/programme · 2 pages

scripts/                               Python build pipeline (uses Playwright + Chromium)
├── make_pdf.py                        → outputs/six_characters.pdf
├── build_audition.py                  → outputs/audition_call.pdf
├── build_three.py                     → outputs/audition_packet_trimmed.pdf, sides_templates.pdf, scene_index.pdf
├── build_summary.py                   → outputs/production_summary.pdf
└── history/                           Record of one-off transformations applied during the build
                                       (modernization, restage, comedy passes, etc.) — kept as a
                                       creative-decision audit trail, not needed for rebuilds.

data/
└── role_stats.json                    Per-character speech counts and word counts across the production

docs/
└── director-notes/                    Working reflections on the play — what it is, how the parts read,
                                       where productions tend to go wrong. Opinions, not blocking.
```

---

## Regenerating the PDFs

The build scripts use absolute paths matching the original build environment (`/home/claude/...`). To run them locally:

1. Install Python 3.10+ with Playwright and pypdf:
   ```bash
   pip install playwright pypdf
   playwright install chromium
   ```
2. Open each script under `scripts/` and replace the `/home/claude/` and `/mnt/user-data/outputs/` paths with paths matching your local checkout.
3. Run, e.g.: `python scripts/make_pdf.py`

Or simply use the PDFs already in `outputs/`.

---

## Source

The base translation is Edward Storer's 1922 English version of Pirandello's *Six Characters in Search of an Author*, sourced from Project Gutenberg Australia (eBook No. 0608521h.html, November 2006). All directorial commentary, casting notes, part notes, statistics, projection cues, and creative adaptations (Lausanne relocation, modernised English, compressed casting structure, comedy punches, staging choices) are this production's own work.

---

## Production timeline

| Phase | Dates |
|---|---|
| Open auditions in Lausanne | June 2026 |
| Line readings (cast as available) | Late June – July 2026 |
| Weekly rehearsals | August – November 2026 |
| Opening — short run of 3–4 performances | Late autumn 2026 |

---

## License

This is a working production document and is **not licensed for redistribution**. The base translation is public-domain via Project Gutenberg Australia; all directorial adaptations, commentary, and production materials are the work of the Village Players and the director, and are made available here for production use only.
