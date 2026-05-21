# Six Characters in Search of an Author

**A Village Players production · Lausanne · late autumn 2026**

A director's edition of Luigi Pirandello's *Sei personaggi in cerca d'autore* (1921), in the Edward Storer 1922 English translation, prepared for a Lausanne staging by the Village Players. The English has been tightened and modernised; the production is set in Lausanne (Madame Pace's atelier off the rue de Bourg, francs instead of lire); the Players are compressed to three tracks doubling several roles each; the staging is stripped to one defining visual per act; the light and music are scored beat by beat; the intimacy and consent protocol is part of the casting contract.

Eight live performers, two stage objects, three brief projections, three stripped settings. A short run of three or four performances.

---

## Working artifacts

```
six_characters_village_players.html   The Director's Copy — open in any browser to read.
                                       This is the authoritative source. All PDFs are
                                       generated from it.

outputs/
├── six_characters.pdf                 Director's Copy PDF — full master version with
│                                       portraits, part-notes, staging notes, light & sound
│                                       score, intimacy protocol, all dialogue. ~105 pages.
├── six_characters_actor_script.pdf    Actor Rehearsal Script — stripped working pages for
│                                       the room: cast list, dialogue, necessary stage
│                                       directions, projection and sound cues. No essays.
│                                       ~55 pages.
├── audition_unified.pdf               Audition Pack — cover, how-to-audition, and eight
│                                       role sections, each with the full character
│                                       description and ~2 pages of dialogue pulled
│                                       byte-identically from the play. ~27 pages.
└── production_summary.pdf             One-page publication blurb for press, programme,
                                        festival listings, and company announcements.

scripts/                               Build pipeline (Python + Playwright + Chromium)
├── make_pdf.py                        → outputs/six_characters.pdf
├── build_actor_script.py              → six_characters_actor_script.html (then make_pdf
│                                       renders it to outputs/six_characters_actor_script.pdf)
├── build_audition_unified.py          → outputs/audition_unified.pdf
├── build_summary.py                   → outputs/production_summary.pdf
├── recount_stats.py                   → recounts per-character speech/word counts and
│                                       updates the stats blocks in the HTML and
│                                       data/role_stats.json
├── build_audition.py                  Legacy. Builds older-style casting packet
│                                       (audition_call). Kept for reference; the canonical
│                                       audition document is now audition_unified.pdf.
├── build_three.py                     Legacy. Builds audition_packet_trimmed.pdf,
│                                       sides_templates.pdf, scene_index.pdf. Kept for
│                                       reference; superseded by audition_unified.pdf.
└── history/                           Record of one-off transformations from earlier
                                       editorial passes. Audit trail, not needed for
                                       rebuilds.

data/
└── role_stats.json                    Per-character speech counts and word counts,
                                       recounted from the HTML by recount_stats.py.

docs/
└── director-notes/                    High-level director's reflections on the play —
                                       what it is, how the parts read, where productions
                                       tend to go wrong. Opinions, not blocking.
```

---

## Regenerating the PDFs

The build scripts use repo-relative paths and read the working HTML automatically. To rebuild from scratch:

```bash
# 1. Install Python 3.10+ with Playwright and Chromium
pip install playwright pypdf beautifulsoup4
playwright install chromium

# 2. From the repository root:
python scripts/recount_stats.py             # refresh stats in HTML + JSON
python scripts/build_actor_script.py        # generate actor-script HTML
python scripts/make_pdf.py                  # render six_characters.pdf

PDF_SRC=six_characters_actor_script.html \
PDF_OUT=outputs/six_characters_actor_script.pdf \
  python scripts/make_pdf.py                # render actor-script PDF

python scripts/build_audition_unified.py    # render audition_unified.pdf
python scripts/build_summary.py             # render production_summary.pdf
```

If your local Chromium install lives at a non-default path, set `CHROMIUM_PATH=/path/to/chrome` in front of each command.

---

## What's in the Director's Copy

The Director's Copy is the single source of truth. It contains, in order:

- **Cover, cast list, character portraits** (Father, Mother, Step-Daughter, Son, Boy, Child, Manager, Players 1–3, Madame Pace), each with the specific reading the actor must commit to and the signature physical object that scores the role across the production.
- **Production note** — eight performers, two stage objects, three projections, three stripped settings, the way Player 3 becomes Madame Pace, how the speaker tags work.
- **Light and Sound score** — per-act lighting (white → amber → red in Act One; the pianist and the shower in Act Two; the fountain-light and one bare bulb in Act Three) with specific track suggestions.
- **Touching, Intimacy, and the Shop Scene** — the production's consent protocol. Every physical contact is named and bounded; the Step-Daughter has absolute veto; intimacy rehearsals are not closed; the production carries the moral weight so the bodies do not have to.
- **The play itself** — three acts × three parts each, with directorial part-notes before each part (narrative, stats, "for the rehearsal room" beats, performance scoring).

---

## What's in the other documents

- **Actor Rehearsal Script** — derived from the Director's Copy automatically by `build_actor_script.py`. Strips portraits, part-notes, stats blocks, and the directorial essays. Keeps the cover, a short cast list, a one-paragraph production note on the stage objects and projections, and the full play text including every necessary stage direction, projection cue, and sound/light cue.

- **Audition Pack (audition_unified.pdf)** — cover, a one-page "how to audition" note, then eight role sections. Each section has the full character description (the portrait from the Director's Copy) followed by ~2 pages of consecutive dialogue from the part of the play where that character is most active. The dialogue is pulled byte-identically from the working HTML, so it stays in sync with edits.

- **Production Summary** — a one-page publication blurb for press releases, programme notes, festival listings, or the company's own announcements.

---

## Source

The base translation is Edward Storer's 1922 English version of Pirandello's *Six Characters in Search of an Author*, sourced from Project Gutenberg Australia (eBook No. 0608521h.html, November 2006). All directorial commentary, casting notes, part-notes, performance scoring, projection and sound cues, light score, intimacy protocol, and creative adaptations (Lausanne relocation, modernised English, compressed casting structure, broken-beat rhythm, stage-objects-for-children) are this production's own work.

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
