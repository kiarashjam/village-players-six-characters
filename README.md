# Six Characters in Search of an Author

**A Village Players production · Lausanne · late autumn 2026**

**Rewritten and directed by Kiarash Jamshidi.**

A director's edition of Luigi Pirandello's *Sei personaggi in cerca d'autore* (1921), in the Edward Storer 1922 English translation, prepared for a Lausanne staging by the Village Players. Every directorial reading, scoring, adaptation, and production decision in this edition — the chair-and-coat and the bundle as the Boy and the Child, the Lausanne anchoring, the four-stage Father arc, the Step-Daughter's three cuts, the Mother's three silences, the Manager as the audience's body on stage, the Madame Pace arc from comic to chilling, the production calendar, the Light & Sound score, and every part-note throughout — is the work of Kiarash Jamshidi. Pirandello supplied the play; everything else around it is his.

Nine live performers, two stage objects, three stripped settings (no projection, no screen). A short run of three or four performances.

---

## Working artifacts

```
six_characters_village_players.html   The Director's Copy — open in any browser to read.
                                       This is the authoritative source. All PDFs are
                                       generated from it.

outputs/
├── directors_copy.pdf                 Director's Copy PDF — full master version with
│                                       portraits, part-notes, staging notes, light & sound
│                                       score, all dialogue. ~105 pages.
├── actor_script.pdf                   Actor Rehearsal Script — stripped working pages for
│                                       the room: cast list, dialogue, necessary stage
│                                       directions, light and sound cues. No essays.
│                                       ~55 pages.
├── <role>_part_book.pdf               Part Books — one per speaking role (father, mother,
│                                       step_daughter, son, manager, player1, player2,
│                                       player3, madame_pace). Every line that role speaks and
│                                       every action it performs, in performance order, grouped
│                                       by act and part, each entry preceded by its cue. The
│                                       intro is the character's portrait, pulled from the play.
├── audition_pack.pdf                  Audition Pack — cover, how-to-audition, and nine
│                                       role sections (the four Characters, the Manager,
│                                       Players 1–3, and Madame Pace), each with the full
│                                       character description and ~2 pages of dialogue pulled
│                                       byte-identically from the play. ~30 pages.
├── audition_twohanders.pdf            Audition Two-Hander Pack — a paired side for the
│                                       pairings of the nine speaking roles, only those two
│                                       speaking. Organised by character; Madame Pace appears
│                                       only with the three figures she meets in the play, so
│                                       the matrix is intentionally not complete. ~58 pages.
├── audition_briefing.pdf              Audition Briefing — one page per speaking role (all
│                                       nine: the four Characters, the Manager, Players 1–3,
│                                       and Madame Pace) with the look, the behaviour, the
│                                       tone of speaking, what to coach against, and a
│                                       three-sentence solo. Madame Pace's page carries the
│                                       accent-and-ledger test. ~11 pages.
├── audition_checklist.pdf             Director's working checklist for the audition room.
│                                       One page per role with checkboxes (reading,
│                                       signature & arc, voice & body, notes), plus an
│                                       auditioner-info form and a general assessment
│                                       page. Bring this to every audition. ~16 pages.
├── assistant_director_pack.pdf        Assistant Director Pack — what the AD does, the
│                                       five areas of work, the audition / table-work /
│                                       staging blocks broken down session by session.
├── stage_manager_pack.pdf             Stage Manager Pack — what the SM does, the master
│                                       prop list, the master costume list, the full Light
│                                       & Sound cue list (called from the prompt book),
│                                       performance-day running order, and the production
│                                       calendar session by session.
├── intimacy_protocol.pdf              The production's intimacy and consent protocol —
│                                       the standalone contract, separate from script and
│                                       production notes. Every performer signs it before
│                                       the first rehearsal; the director countersigns.
├── production_meeting_brief.pdf       Production Meeting Brief — the director's brief for
│                                       the meeting with the Production Manager: the show at
│                                       a glance, what the production needs, area-by-area
│                                       questions to ask, a stage-by-stage walk-through, and
│                                       a decisions checklist. ~16 pages.
├── directors_handbook.pdf             Director's Handbook — a comprehensive field manual
│                                       for the director, in seven parts: the play and its
│                                       demands, directing technique (Stanislavski, blocking,
│                                       coaching the actor), staging technique for this
│                                       production, working with the company, Pirandello in
│                                       particular, practical director's work, and what the
│                                       director must hold across the production. ~44 pages.
├── synopsis.pdf                       The whole story, beginning to end, in plain narrative
│                                       voice. Backstory (the marriage, the secretary, the
│                                       school gate, Madame Pace's shop, the fountain), then
│                                       what happens on stage act by act. For cast, company,
│                                       and anyone who hasn't read Pirandello. ~11 pages.
├── two_deaths_note.pdf                One-page production note: how the production stages
│                                       the deaths of the Child (drowning at the fountain)
│                                       and the Boy (the gunshot) using only objects, sound,
│                                       dialogue, and light — no performer asked to die. For
│                                       the production walk-through so the company shares a
│                                       vocabulary for how the deaths are "performed" by
│                                       objects.
└── production_summary.pdf             One-page publication blurb for press, programme,
                                        festival listings, and company announcements.

scripts/                               Build pipeline (Python + Playwright + Chromium)
├── make_pdf.py                        → outputs/directors_copy.pdf
├── build_actor_script.py              → actor_script.html (then make_pdf
│                                       renders it to outputs/actor_script.pdf)
├── build_part_books.py                → outputs/<role>_part_book.pdf (×9, one per role)
├── build_audition_pack.py             → outputs/audition_pack.pdf
├── build_audition_twohanders.py       → outputs/audition_twohanders.pdf
├── build_audition_briefing.py         → outputs/audition_briefing.pdf
├── build_audition_checklist.py        → outputs/audition_checklist.pdf
├── build_assistant_director_pack.py   → outputs/assistant_director_pack.pdf
├── build_stage_manager_pack.py        → outputs/stage_manager_pack.pdf
├── build_intimacy_protocol.py         → outputs/intimacy_protocol.pdf
├── build_production_meeting_brief.py  → outputs/production_meeting_brief.pdf
├── build_directors_handbook.py        → outputs/directors_handbook.pdf
├── build_synopsis.py                  → outputs/synopsis.pdf
├── build_two_deaths_note.py           → outputs/two_deaths_note.pdf
├── build_summary.py                   → outputs/production_summary.pdf
├── recount_stats.py                   → recounts per-character speech/word counts and
│                                       updates the stats blocks in the HTML and
│                                       data/role_stats.json
├── build_audition.py                  Legacy. Builds older-style casting packet
│                                       (audition_call). Kept for reference; the canonical
│                                       audition document is now audition_pack.pdf.
├── build_three.py                     Legacy. Builds audition_packet_trimmed.pdf,
│                                       sides_templates.pdf, scene_index.pdf. Kept for
│                                       reference; superseded by audition_pack.pdf.
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
python scripts/recount_stats.py                    # refresh stats in HTML + JSON
python scripts/build_actor_script.py               # generate actor_script.html
python scripts/make_pdf.py                         # render directors_copy.pdf

PDF_SRC=actor_script.html \
PDF_OUT=outputs/actor_script.pdf \
  python scripts/make_pdf.py                       # render actor_script.pdf

python scripts/build_part_books.py                 # render all nine <role>_part_book.pdf
python scripts/build_audition_pack.py              # render audition_pack.pdf
python scripts/build_audition_twohanders.py        # render audition_twohanders.pdf
python scripts/build_audition_briefing.py          # render audition_briefing.pdf
python scripts/build_audition_checklist.py         # render audition_checklist.pdf
python scripts/build_assistant_director_pack.py    # render assistant_director_pack.pdf
python scripts/build_stage_manager_pack.py         # render stage_manager_pack.pdf
python scripts/build_intimacy_protocol.py          # render intimacy_protocol.pdf
python scripts/build_production_meeting_brief.py   # render production_meeting_brief.pdf
python scripts/build_directors_handbook.py         # render directors_handbook.pdf
python scripts/build_synopsis.py                   # render synopsis.pdf
python scripts/build_two_deaths_note.py            # render two_deaths_note.pdf
python scripts/build_summary.py                    # render production_summary.pdf
```

If your local Chromium install lives at a non-default path, set `CHROMIUM_PATH=/path/to/chrome` in front of each command.

---

## What's in the Director's Copy

The Director's Copy is the single source of truth. It contains, in order:

- **Cover, cast list, character portraits** (Father, Mother, Step-Daughter, Son, Boy, Child, Manager, Players 1–3, Madame Pace), each with the specific reading the actor must commit to and the signature physical object that scores the role across the production.
- **Production note** — nine performers, two stage objects, three stripped settings (no projection, no screen), Madame Pace as a Character carried by her own performer, how the speaker tags work.
- **Light and Sound score** — per-act lighting (white → amber → red in Act One; the pianist and the shower in Act Two; the fountain-light and one bare bulb in Act Three) with specific track suggestions.
- **Intimacy and consent protocol** — the protocol lives in its own dedicated document (`outputs/intimacy_protocol.pdf`), not in the Director's Copy. It is a contract, signed by every performer before the first rehearsal and countersigned by the director.
- **The play itself** — three acts × three parts each, with directorial part-notes before each part (narrative, stats, "for the rehearsal room" beats, performance scoring).

---

## What's in the other documents

- **Actor Rehearsal Script** — derived from the Director's Copy automatically by `build_actor_script.py`. Strips portraits, part-notes, stats blocks, and the directorial essays. Keeps the cover, a short cast list, a production note on the two stage objects (and the explicit "no projection, no screen" decision), and the full play text including every necessary stage direction and sound/light cue.

- **Audition Pack (audition_pack.pdf)** — cover, a one-page "how to audition" note, then nine role sections (the four Characters, the Manager, Players 1–3, and Madame Pace). Each section has the full character description (the portrait from the Director's Copy) followed by ~2 pages of consecutive dialogue from the part of the play where that character is most active. The dialogue is pulled byte-identically from the working HTML, so it stays in sync with edits.

- **Production Summary** — a one-page publication blurb for press releases, programme notes, festival listings, or the company's own announcements.

---

## Source and attribution

The base translation is Edward Storer's 1922 English version of Pirandello's *Six Characters in Search of an Author*, sourced from Project Gutenberg Australia (eBook No. 0608521h.html, November 2006).

All directorial commentary, casting notes, part-notes, performance scoring, light and sound cues, light score, intimacy and consent protocol, and creative adaptations — the Lausanne relocation, the modernised English, the compressed casting structure, the broken-beat rhythm, the stage-objects-for-children (with no projection, no screen), the audience-symbol Manager, the four-stage Father arc, the Step-Daughter's three cuts, the Mother's three silences, the Madame Pace arc, the production calendar (audition / table-work / staging blocks), the Assistant Director and Stage Manager role notes — are the original work of **Kiarash Jamshidi**, the director of this production. The ideas in this edition belong to him.

---

## Production timeline

| Phase | Dates |
|---|---|
| Audition block — three sessions, SSA Lausanne 18:00–21:00 | Tue 2 / Fri 5 / Wed 10 June 2026 |
| Table-work block — seven Thursdays, SSA Lausanne 18:00–21:00 | Thu 18 June – Thu 30 July 2026 |
| Summer break — no rehearsal | 5 & 13 August 2026 |
| Staging block — weekly Thursdays at SSA Lausanne | Thu 20 August – Sun 1 November 2026 |
| Opening — short run of 3–4 performances | Late autumn 2026 |

The three June audition dates are open auditions plus callbacks. The seven Thursdays from 18 June through 30 July are pure table work — first reading, production walk-through, Acts 1 / 2 / 3 table work, Light & Sound walk-through, full read-through with cues. The first two weeks of August (the 5th and 13th) are the company's summer break — no rehearsal. The staging block from 20 August to 1 November is blocking, run-throughs, technical and dress rehearsals — see the *Rehearsal Schedule* section in the Director's Copy and the *Stage Manager Pack* for the per-session breakdown.

---

## License

This is a working production document and is **not licensed for redistribution**. The base translation is public-domain via Project Gutenberg Australia; all directorial adaptations, commentary, and production materials are the work of the Village Players and the director, and are made available here for production use only.
