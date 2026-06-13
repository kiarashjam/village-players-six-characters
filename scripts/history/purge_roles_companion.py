#!/usr/bin/env python3
"""
Purge the old company role-names from the companion production documents
(audition packs, briefing, checklist, two-handers, director's handbook,
synopsis, summary, stage-manager pack, intimacy protocol, two-deaths note,
and the three-Players audition sheet), so they speak of Player 1, Player 2,
and Player 3 — and of functions, never of named parts.

Run from the repo root:  python scripts/history/purge_roles_companion.py
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent.parent.parent
S = HERE / "scripts"

REPLACEMENTS = {
    "build_audition_checklist.py": [
        ("one character in five hats — the Leading Man underneath (forties)",
         "one performer in many hats — the company's fading star underneath (forties)"),
        ("In his forties — the eldest of the Players, and the vain faded Anglo Leading Man. The role asks an actor to play five different functions (Leading Man, L'Ingénue, Door-keeper, Machinist, Third Actor) as the same man underneath",
         "In his forties — the eldest of the Players, and the vain faded Anglo star of the company. The role asks an actor to play many small functions (the fading star, a young woman's part, the stage door, the curtain, an odd reading line) as the same man underneath"),
        ("Vocal flexibility across the five roles without losing the spine",
         "Vocal flexibility across the many parts without losing the spine"),
        ("Plays five roles as the same man underneath — the audience reads one character, five hats",
         "Plays many parts as the same man underneath — the audience reads one character, many hats"),
        ("Available to play the Leading Man playing the Father in the shop scene without losing his own ego under the role",
         "Available to play the fading star playing the Father in the shop scene without losing his own ego under the part"),
        ("Available to read each of the five hats in audition (one or two short beats apiece)",
         "Available to read several of the hats in audition (one or two short beats apiece)"),
        ("the Leading Lady's wounded vanity and the Property Man's practical irritation",
         "the diva's wounded vanity and the props hand's practical irritation"),
        ("Range from the diva's wounded indignation to the Property Man's quick functional dispatch",
         "Range from the diva's wounded indignation to the props hand's quick functional dispatch"),
        ("Practical, no-nonsense Property Man bearing",
         "Practical, no-nonsense props-hand bearing"),
        ("Comfortable flipping between Leading Lady and Property Man within a single scene",
         "Comfortable flipping between the diva and the props within a single scene"),
        ("Carries the Juvenile Lead and the Prompter, and is the audience's mirror",
         "Carries a young romantic part and the prompt box, and is the audience's mirror"),
        ("Earnest, open Juvenile Lead voice",
         "Earnest, open young-romantic voice"),
        ("Quiet, meticulous Prompter voice (slightly older, in the box)",
         "Quiet, meticulous prompt-box voice (slightly older, in the box)"),
        ("Earnest, genuinely curious in the Juvenile Lead beats — curious, not naive",
         "Earnest, genuinely curious in the young-romantic beats — curious, not naive"),
        ("Available to read both the Juvenile Lead and Prompter beats in audition",
         "Available to read both the young-romantic and prompt-box beats in audition"),
        ("Comfortable with the prompter's box for extended periods",
         "Comfortable with the prompt box for extended periods"),
    ],
    "build_three.py": [
        ("Act One — at the family's arrival (Leading Man)", "Act One — at the family's arrival"),
        ("Act One — outrage (Leading Man)", "Act One — outrage"),
        ("Act One curtain — as Door-keeper", "Act One curtain — the man who let them in"),
        ("Act Two — refusing the game (Leading Lady)", "Act Two — refusing the game"),
        ("Act Two — wounded vanity (Leading Lady)", "Act Two — wounded vanity"),
        ("Act Two — during the shop scene (Leading Lady)", "Act Two — during the shop scene"),
        ("Act One — at the family's arrival (Juvenile Lead)", "Act One — at the family's arrival"),
        ("Act One — refusing the chaos (Juvenile Lead)", "Act One — refusing the chaos"),
        ("Act One — disbelief (Juvenile Lead)", "Act One — disbelief"),
        ('role_name.replace(" (Leading Man)", "").replace(" (Door-keeper)", "")', "role_name"),
    ],
    "build_audition_twohanders.py": [
        ('"P1": "the Leading Man — forties, vain, faded, defensive",',
         '"P1": "the company\'s fading star — forties, vain, faded, defensive",'),
        ('"P2": "the Leading Lady — about 35, practical, professional, the one who books the work",',
         '"P2": "the leading woman — about 35, practical, professional, the one who books the work",'),
        ("The vain Leading Man against the tired Manager",
         "The vain star against the tired Manager"),
        ("The practical Leading Lady will act anything the moment he gives her a beginning.",
         "Player 2, the practical professional, will act anything the moment he gives her a beginning."),
        ("here I still am, at my age, arguing with a Leading Man about a hat.",
         "here I still am, at my age, arguing with a vain man about a hat."),
        ("Fifteen years I have been the Leading Man of this company. People in this city know my face",
         "Fifteen years I have carried this company. People in this city know my face"),
        ("I am only observing that a Leading Man requires a part he can take some pride in",
         "I am only observing that an actor of my standing requires a part he can take some pride in"),
        ("A Leading Man requires an audience to admire him.",
         "A man like that requires an audience to admire him."),
        ("The senior Leading Man instructs the newest member",
         "The senior actor instructs the newest member"),
        ("The Leading Man sets the tone.",
         "The senior man sets the tone."),
    ],
    "build_audition_pack.py": [
        ('three "Players" cover the dozen company roles (Leading Man, Leading Lady, Juvenile Lead, Prompter, Property Man, Door-keeper, Machinist, L\'Ingénue, and the rest);',
         'three "Players" — Player 1, Player 2, and Player 3 — cover every other figure the morning needs (the company\'s actors, the door, the props, the prompt box, the stage crew, and the small reading parts);'),
        ("The Door-keeper sets the chair at the edge of the stage as the Six walk on",
         "Player 1 sets the chair at the edge of the stage as the Six walk on"),
        ("He bickers with the Leading Man about the cook's cap",
         "He bickers with Player 1 about the cook's cap"),
        ('"tag": "one character in five hats — the faded Leading Man",',
         '"tag": "one performer in many hats — the company\'s faded star",'),
        ("Act Two, Part III — the Leading Man takes the platform and plays the Father",
         "Act Two, Part III — Player 1 takes the platform and plays the Father"),
        ("Act Two, Part III — the Leading Lady takes the platform to play the Step-Daughter",
         "Act Two, Part III — Player 2 takes the platform to play the Step-Daughter"),
        ("Act One, Part I — the Prompter takes the play down from the box",
         "Act One, Part I — Player 3 takes the play down from the box"),
        ("Leading Man · L'Ingénue · Door-keeper · Machinist · Third Actor — in his forties; one character in five hats; the faded Anglo Leading Man",
         "in his forties; one performer in many hats; the faded Anglo star of the company"),
        ("Leading Lady · Property Man · Fourth Actor · Second Lady Lead — about 35; the real working professional",
         "about 35; the real working professional"),
        ("Juvenile Lead · Prompter · An Actor · Fifth Actor — early 20s, the youngest and happiest",
         "early 20s, the youngest and happiest"),
    ],
    "build_audition_briefing.py": [
        ("the company can no longer afford a Property Man and I would rather build a screen",
         "the company can no longer afford anyone to do the props and I would rather build a screen"),
        ("which my Leading Man already considers a personal affront",
         "which my senior actor already considers a personal affront"),
        ("and a Leading Man currently arguing with me about a cook's cap",
         "and a senior actor currently arguing with me about a cook's cap"),
        ("<h2>Player 1 — the Leading Man</h2>", "<h2>Player 1</h2>"),
        ("Looks like a Leading Man who has been a Leading Man for too long",
         "Looks like a star who has been a star for too long"),
        ("For the functions he doubles into (the cook's cap, the Door-keeper's cap, L'Ingénue),",
         "For the functions he doubles into (the cook's cap, the stage-door cap, the young woman's part),"),
        ("the Door-keeper still has his self-importance; the Machinist still has his opinions; L'Ingénue is the joke",
         "the stage-door man still has his self-importance; the one who works the curtain still has his opinions; the young woman's part is the joke"),
        ("Plays five functions, all of them as himself in different hats:",
         "Plays many functions, all of them as himself in different hats:"),
        ("He speaks the way he imagines a Leading Man speaks.",
         "He speaks the way he imagines a great actor speaks."),
        ("<h2>Player 2 — the Leading Lady</h2>", "<h2>Player 2</h2>"),
        ("with this exact Leading Man, more times than she cares to count. For the Leading Lady function: a little more put together. For the Property Man function: sleeves rolled.",
         "with this exact man, more times than she cares to count. In her diva register: a little more put together. With the props: sleeves rolled."),
        ("The Property Man this season because the company could not afford a real one",
         "She took the props on this season because the company could not afford anyone else"),
        ("Treating the Property Man role as comic relief.",
         "Treating the props as comic relief."),
        ("when our Leading Man tells me, as he has just now, that he has",
         "when our senior man tells me, as he has just now, that he has"),
    ],
    "build_audition.py": [
        ("Act One — the Leading Man's vanity", "Act One — the fading star's vanity"),
        ("Act One — as Leading Man", "Act One — the cook's-cap argument"),
        ("Act One — as Door-keeper", "Act One — the man who let them in"),
        ("Act Two — the Leading Lady refusing 'the game'", "Act Two — the leading woman refusing 'the game'"),
        ("Act Two — as Leading Lady", "Act Two — refusing 'the game'"),
        ("Act One — the Juvenile Lead", "Act One — the youngest, curious"),
        ("Act One — as Juvenile Lead", "Act One — the youngest, in disbelief"),
    ],
    "build_stage_manager_pack.py": [
        ("The shop-scene replay between Leading Lady and Leading Man.",
         "The shop-scene replay between Player 2 and Player 1."),
        ("Door-keeper steps onto the stage with the chair-and-coat",
         "Player 1 steps onto the stage with the chair-and-coat"),
        ("Door-keeper's first line", "Player 1's first line"),
        ("Working lights up. Property Man, Machinist, and Manager begin the white-parlour set-up",
         "Working lights up. Player 2, Player 1, and the Manager begin the white-parlour set-up"),
        ("Leading Lady &amp; Leading Man take the platform",
         "Player 2 &amp; Player 1 take the platform"),
    ],
    "build_directors_handbook.py": [
        ("The Door-keeper carries the chair-and-coat in and sets it",
         "Player 1 carries the chair-and-coat in and sets it"),
        ("Leading Lady and Leading Man take the platform to play the shop scene",
         "Player 2 and Player 1 take the platform to play the shop scene"),
        ("The Door-keeper walks on with the chair, sets it at the edge",
         "Player 1 walks on with the chair, sets it at the edge"),
        ("by the Door-keeper's placing of the chair",
         "by Player 1's placing of the chair"),
        ("Cuts mid-bar when the Door-keeper speaks.",
         "Cuts mid-bar when Player 1 speaks."),
    ],
    "build_synopsis.py": [
        ("His three Players, all working actors, are getting into position. The Leading Man is complaining about being asked to wear a cook's cap in the opening scene. The Leading Lady, who is also doing the props this season because the company can no longer afford a Property Man, is building a folding screen out of two old flats and a hinge she bought yesterday. The youngest in the company, serving as Prompter, is taking dictation about the set in a shorthand she is privately a little proud of.",
         "His three Players, all working actors, are getting into position. Player 1, the company's fading star, is complaining about being asked to wear a cook's cap in the opening scene. Player 2, who is also doing the props this season because the company can no longer afford anyone else, is building a folding screen out of two old flats and a hinge she bought yesterday. Player 3, the youngest in the company, taking the play down from the prompt box, is taking dictation about the set in a shorthand they are privately a little proud of."),
        ("The Leading Lady, who has played leads at every house in this canton, has been made a fool of by better",
         "Player 2, who has played leads at every house in this canton, has been made a fool of by better"),
        ("The Door-keeper comes in, carrying a wooden chair.",
         "Player 1 comes in, carrying a wooden chair."),
        ("The Property Man wheels the folding screen into position.",
         "Player 2 wheels the folding screen into position."),
        ("The company's own Leading Lady and Leading Man then climb onto the upper platform",
         "The company's own Player 2 and Player 1 then climb onto the upper platform"),
    ],
    "build_two_deaths_note.py": [
        ('Two Players: <em>"He\'s dead! dead!"</em> Other Players: <em>"No, no, it\'s only make believe, it\'s only pretence!"</em>',
         'Players 1 and 2: <em>"He\'s dead! dead!"</em> Player 3: <em>"No, no, it\'s only make believe, it\'s only pretence!"</em>'),
    ],
    "build_summary.py": [
        ("The Door-keeper enters, carrying a wooden chair, and sets it at the edge",
         "Player 1 enters, carrying a wooden chair, and sets it at the edge"),
    ],
    "build_intimacy_protocol.py": [
        ("The Leading Man and Leading Lady go through the choreography",
         "Player 1 and Player 2 go through the choreography"),
        ("The Leading Lady's hat-removal is",
         "Player 2's hat-removal is"),
    ],
}

missing = 0
for fname, pairs in REPLACEMENTS.items():
    path = S / fname
    text = path.read_text()
    for old, new in pairs:
        if old not in text:
            if new not in text:  # genuinely missing (not just already applied)
                print(f"  !! NOT FOUND in {fname}: {old[:60]!r}")
                missing += 1
            continue
        text = text.replace(old, new)
    path.write_text(text)
    print(f"  updated {fname}")

print(f"done ({missing} missing)" if missing else "done — all replacements applied")
