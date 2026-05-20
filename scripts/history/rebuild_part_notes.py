#!/usr/bin/env python3
"""Rebuild all 9 part notes:
- Replace the What/How/When/Feeling grid with an expanded narrative
- Add a 'Who speaks, and how much' block with per-character speech and word counts
- Replace 'Theatre Questions' with 'For the rehearsal room' — practical notes"""
from pathlib import Path
import re

SRC = Path("/home/claude/six_characters.html")
html = SRC.read_text()
original_len = len(html)

# ===========================================================================
# Helpers
# ===========================================================================

def normalize_speaker(raw):
    raw = raw.strip()
    if raw.startswith('Player 1'):
        return 'Player 1'
    if raw.startswith('Player 2'):
        return 'Player 2'
    if raw.startswith('Player 3'):
        return 'Player 3'
    if raw == 'All Three Players' or raw == 'The Other Players':
        return 'All Three Players'
    if raw == 'Two Players':
        return 'Two Players'
    if raw == 'The Manager and The Father':
        return 'The Manager and The Father'
    return raw  # The Manager / Father / Mother / Step-Daughter / Son

def count_words(speech_html):
    text = re.sub(r'<span class="speaker">.*?</span>', '', speech_html, flags=re.DOTALL)
    text = re.sub(r'<span class="action">.*?</span>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'[—…]', ' ', text)
    words = re.findall(r"\b\w[\w']*\b", text)
    return len(words)

# ===========================================================================
# Parse parts and collect speeches per part
# ===========================================================================

def parse_parts(h):
    acts = re.findall(r'<article[^>]*class="act"[^>]*>(.*?)</article>', h, re.DOTALL)
    parts = []
    for act_idx, act_html in enumerate(acts):
        elements = []
        for m in re.finditer(
            r'<aside class="part-note">.*?</aside>|<p class="speech">.*?</p>',
            act_html, re.DOTALL
        ):
            elements.append((m.start(), m.group(0)))
        elements.sort()

        current = None
        for pos, content in elements:
            if 'class="part-note"' in content:
                title_m = re.search(r'<h3 class="part-title">([^<]+)</h3>', content)
                eyebrow_m = re.search(r'<div class="part-eyebrow">([^<]+)</div>', content)
                current = {
                    'act': act_idx + 1,
                    'eyebrow': eyebrow_m.group(1) if eyebrow_m else '',
                    'title': title_m.group(1) if title_m else '',
                    'speeches': [],
                    'old_html': content,
                }
                parts.append(current)
            elif current is not None:
                current['speeches'].append(content)
    return parts

parts = parse_parts(html)
print(f"Parsed {len(parts)} parts")

# Compute stats for each part
for p in parts:
    stats = {}
    for s in p['speeches']:
        m = re.search(r'<span class="speaker">(.*?)</span>', s, re.DOTALL)
        if not m:
            continue
        raw = re.sub(r'<[^>]+>', '', m.group(1))
        spk = normalize_speaker(raw)
        w = count_words(s)
        if spk not in stats:
            stats[spk] = {'count': 0, 'words': 0}
        stats[spk]['count'] += 1
        stats[spk]['words'] += w
    p['stats'] = stats

# ===========================================================================
# New narrative + rehearsal-room notes for each part
# ===========================================================================

PARTS_CONTENT = {
    (1, 1): {
        "narrative": [
            "The curtain rises on an empty stage. The lights are working lights. The Manager arrives at his theatre to a half-rehearsed company. The play they are meant to rehearse this morning is one of Pirandello's own — <em>Mixing It Up</em> — which the Manager believes is unstageable, and which his contract has forced him to stage anyway. He bickers with the Leading Man about being asked to wear a cook's cap in a serious play. He insults the playwright. He insults the script. He insults the conditions under which any working theatre is forced to operate. None of this surprises his actors, who have heard it before; some are tying their shoes, some are reading the paper, none is rehearsing.",
            "The Prompter takes his place in the box, complaining about the draught. The Property Man enters with furniture for an entirely different scene than the one being rehearsed. The Door-keeper waits at the back of the house with a stack of unread letters. The apparatus of the working theatre — irritation, vanity, exhaustion, the small professional dignities — is performing itself, for nobody it knows is watching.",
            "The audience watches all of this comedy and does not yet know it is watching a comedy. The play has not announced itself. We are inside the engine room of the production, not the production. There is no Pirandello here yet, except in the contract burning quietly on the table."
        ],
        "beats": [
            "The Manager is the engine of this part. Comic register must be committed — full anti-Pirandello rant, no protective irony.",
            "Player 1's Leading Man (the cook's-cap argument) is the largest single comic vehicle here. Play the vanity at full pitch.",
            "The audience should be laughing within three minutes. Pacing is everything; do not slow down for jokes you trust.",
            "Player 1 is doing three roles in quick succession (Leading Man, L'Ingénue, Door-keeper). Rehearse the transitions until they are physical reflex.",
            "The Property Man and Door-keeper are small comic anchors. Give them their beats.",
            "No metaphysics. None. Foreshadowing is a temptation that kills the rest of the evening.",
            "Work-lights stay up the whole part. Atmospheric lighting changes do not begin until the Six enter."
        ]
    },
    (1, 2): {
        "narrative": [
            "Six figures arrive — on the rear wall, in a silent video. They walk in carrying a strange tenuous light, almost as if lit from inside. In the video the Boy walks to a wooden chair at the edge of the stage and sits down, leaving his coat and cap on the chair. The Step-Daughter sets the Child down beside her, and the Child becomes a small wrapped bundle of white cloth. The light fades. The screen goes dark. The four live Characters — Father, Mother, Step-Daughter, Son — are now on the stage in flesh, having stepped out of the video as if out of a frame.",
            "The Father asks for an author. The Manager, baffled, asks what kind of madmen have walked in off the street. The Step-Daughter taunts the Father and exposes him: a hundred lire in a back-room of a dressmaker's shop, the kind of transaction one does not name. The Mother lifts her veil and faints. The Father explains his marriage, the secretary he sent his wife away with, the wet-nurse for his son in the country. Every confession is contradicted by the next mouth that opens. The family is laid bare, and laid bare twice.",
            "The actors of the company, who began this part as bored professionals, slowly recede to the wings. They are now an audience to the spectacle that has walked into their rehearsal. The lighting tightens on the family. The rehearsal room dims around them. By the end of this part, the comic register has burned off and what is left is the family standing inside its own argument, with no author in sight."
        ],
        "beats": [
            "The transition from comedy to interrogation is the most important pacing decision in Act One. It should be gradual, not signalled.",
            "The Step-Daughter is the engine of exposure. Her first taunts must land — she is already enjoying the wound she is opening.",
            "The Mother's faint is the temperature change. The actors-as-audience must visibly register it before the dialogue does.",
            "The Father's first long speeches should be played as urgent, not eloquent. He is a man fighting to be allowed to exist, not lecturing about it.",
            "The Son does not move much in this part. His stillness must be a presence, not a passivity.",
            "Keep the Players visible as they recede to the wings. They are an onstage audience now — they should be doing what audiences do (watch, react, fail to look away)."
        ]
    },
    (1, 3): {
        "narrative": [
            "The shop of Madame Pace is named for the first time. The hundred lire. The pale blue envelope. The Father offers his great speech on the many-sided conscience: we are not one self but many, and to be caught in one moment is to be falsified by it. The Manager, who began this part still believing he was being held hostage by lunatics, begins instead to think there is a play in this — perhaps even one his contract should be wishing for. The bargain begins to be struck.",
            "The Step-Daughter is feverish. The Father is in mid-flight. The Son is cold; he announces, without much ceremony, that he does not come into this drama, and that any attempt to make him come into it will fail. The Father describes how the drama ends — the death of the Child by the fountain, the tragedy of the Boy behind the trees, the flight of the Step-Daughter into the night. He describes it not as memory but as fact, already written, already inside him.",
            "The Manager exits to his office with the Characters to organise the rehearsal. The Players are left on stage in a small chorus of bewilderment — the Door-keeper protesting he only let them in, the Property Man muttering that first the script made no sense and now the audience walks in off the street, the Prompter asking, in shorthand, in shorthand? The curtain falls on a theatre that has not yet decided whether it has been broken into or rescued."
        ],
        "beats": [
            "The Father's long monologues are the philosophical engine of the act. They must be played as urgent, not as essays. A man arguing for his life is not a man lecturing.",
            "The Son's refusal is itself a performance. He should be aware of how dramatic his refusal is. That awareness is the comedy underneath the metaphysics.",
            "The Manager's pivot from cynic to interested party is the act's quiet pivot. Play it with both relief and unease.",
            "The final actor chorus is comic relief after a metaphysical climb. Don't undercut it; let the audience laugh again before the act ends.",
            "The Step-Daughter's narration of the shop scene must already contain the violence we will see in Act Two. She is rehearsing it for herself even as she describes it.",
            "By the curtain, the work-lights are gone and the rehearsal-room atmosphere is gone. We are inside the family's drama now, even though officially we are still backstage."
        ]
    },
    (2, 1): {
        "narrative": [
            "The act opens behind the scenes. The Step-Daughter erupts from the Manager's office with the wrapped bundle in her arms and the chair-and-coat at her side. She has just lost an argument we did not witness. The Son and Mother emerge after her, circling each other in silence and accusation. The Father follows last.",
            "The rear wall lights up. The Step-Daughter is shown in video, kneeling — addressing the Child as a real four-year-old, telling her about the imaginary garden and the imaginary fountain and the make-believe water. Partway through, on the same screen, she seizes the Boy and finds the revolver in his pocket. Her voice plays from the speakers. Below the screen, her live body stands silent. This is the only projection in the production with audible voice. The bundle and the chair-and-coat remain on the live stage, visible in front of the screen. When the projection ends, they are once again only objects.",
            "Then the apparatus of the theatre reasserts itself. The Property Man brings in the table. The Machinist places the pegs. The folding screen is wheeled to its position. The white parlour is fitted up around the family's pain like furniture, because that is what theatres do with grief. The Prompter is told to take shorthand. Names are assigned to the Characters by the Manager, who is acting now as a kind of stage-clerk. The Father falters at the sound of his own name."
        ],
        "beats": [
            "The Step-Daughter's projected monologue is the production's most technically delicate moment. Live body silent, recorded voice playing, audience reading both at once. The video and the live performer must look like the same body in two states.",
            "The Mother's circling of the Son is a silent duel. Stage it physically — proximity, evasion, the refusal to meet the eyes. No words yet.",
            "The Property Man should bring in the furniture as if for any other rehearsal, not as if for a family's tragedy. The casualness of the work is the cruelty of this part.",
            "The Father's stumble at his own name is the small moment that signals the rest of the act. Mark it. Do not over-play it.",
            "The Step-Daughter's live body, while the video plays, should be doing something specific. Watching herself? Looking away? Holding the bundle? Choose, and commit.",
            "Use the working lights again here for the technical setup. Atmospheric lighting comes back only when Madame Pace is summoned."
        ]
    },
    (2, 2): {
        "narrative": [
            "The Father asks the actresses if they would mind hanging their hats and mantles on the pegs at the back of the set. They do, half-amused, not knowing why. The Father asks them to look toward the door upstage. The door opens. Madame Pace appears — though she was not in the original six, and no one called her, and no one walks through a stage door on cue. The Step-Daughter recognises her at once.",
            "This is the production's strangest scene. A Character not in the original cast list is summoned by the very arrangement of the stage — by the hats on the pegs, by the shop window the Property Man has set up, by the folding screen. Player 3 enters her costume the way an apparition enters a body. She is fat, bleach-blonde, rouged. She speaks half in Italian and half in English, ridiculous and grotesque. The Step-Daughter begins to play the scene of the atelier with her — half-mimed, half-spoken, almost inaudibly, because the scene is shame and shame is quiet.",
            "Then the Mother sees her. The Mother, who has barely spoken in this play, sees Madame Pace and erupts: <em>You old devil! You murderess!</em> The temperature in the room collapses in seconds. The scene of the shop cannot be played in the presence of its witness. The play breaks its own scene, and the actors, watching from the wings, do not understand what they are watching."
        ],
        "beats": [
            "Madame Pace's entrance must feel inexplicable to the audience. The folding screen, the hats, the shop window — let the audience read them as set-dressing, not as summoning.",
            "Player 3's transformation is the production's most demanding moment. The wig, the heels, the powder — every visual element must commit. The dialect must be performed with no protective irony.",
            "The Step-Daughter's coquetry with Madame Pace should be uncomfortable to watch. It is also funny. Both at once. The audience should laugh and be disgusted simultaneously.",
            "The pale blue envelope and the hundred lire are the props that make the scene material. Treat them with weight. They are not symbols; they are evidence.",
            "The Mother's eruption must be earned. She has been silent for an entire act and a half. Do not let her find her voice slowly — she finds it in one beat, and the room changes with her.",
            "The Mother's silence before and after that eruption is the architecture of the scene. The actor must commit to the silence as much as to the cry."
        ]
    },
    (2, 3): {
        "narrative": [
            "The Father and the Step-Daughter play out the first beats of the shop scene themselves. The lines they say are the lines they actually said, in 1921 Rome, in a back room of a real dressmaker's atelier. The Manager listens, the actors watch, the Mother trembles in the corner. Then the Manager hands the scene to his Leading Lady and Leading Man — they will play this, properly, with stagecraft, in the version that will eventually go on. They try the same lines. The Step-Daughter laughs at them.",
            "The Father objects: they are not us. The Step-Daughter is sharper — the actor will soften it, package it, make it sayable, when the whole point of what was said is that it could not be said. The Mother breaks in: <em>It's taking place now. It happens all the time.</em> She cries out as she did in life. The Machinist, by accident, drops the curtain on what was supposed to be only a rehearsal effect.",
            "This is the act's first real climax. Pirandello forces the audience to watch the same scene twice and feel both versions as inadequate — the live one too raw, the rehearsed one too polished. The audience leaves the act unsettled and a little ashamed of having been entertained."
        ],
        "beats": [
            "Two performances of the same shop scene, back to back, must feel like two genres. The Characters' version is shame in real time; the Actors' version is melodrama in air-quotes.",
            "The Step-Daughter's laughter at the Leading Lady must not be mocking. It must be heartbroken. She is watching her worst hour be made decorative.",
            "The Leading Lady and Leading Man — Players 2 and 1 — must not be in on the joke. They must believe they are doing fine work. The audience should be embarrassed for them.",
            "The Mother's <em>It's taking place now</em> is the moral centre of the play. Surround it with silence. Let the actors freeze around her. Then the curtain falls before they can recover.",
            "The accidental curtain-drop must look genuinely accidental. The Machinist (Player 1) should look surprised. The audience should be unsure for a half-second whether the play is over.",
            "The act ends not on a line but on the collapse of the curtain. Calibrate the descent — neither slow nor fast, but inevitable."
        ]
    },
    (3, 1): {
        "narrative": [
            "The curtain rises on a garden set hurriedly assembled by the stagehands during the interval. A backdrop. A fountain basin. Two flat trees in the wings. The chair-and-coat — the Boy — has been moved to the edge of the garden. The bundle is in the Step-Daughter's arms.",
            "The Manager is plotting. The Step-Daughter complains that the garden cannot hold the whole drama, because the Son spends most of the action shut in his room; how can a garden contain a man who refuses to come into a garden? The Father, suddenly philosophical, objects to the word <em>illusion</em>. He says the Characters have no other reality outside this one — that the Manager's reality, by contrast, may seem an illusion to him tomorrow. <em>Can you tell me who you are?</em>",
            "This is the play's most philosophical stretch. The Father becomes, almost openly, the dramatist that Pirandello cannot help being. The Manager refuses the bait but is visibly unsettled. The Step-Daughter is impatient with the metaphysics — she wants the drama played, not theorised. Yet the Father's argument holds, because of how directly it is aimed: at the Manager, at the actors, at us. The audience is being asked, without warning, whether it exists in the same way the Characters do."
        ],
        "beats": [
            "The garden set must look hastily improvised. Painted cardboard. Visible joins. The Step-Daughter called it cardboard in Act Two; let it be cardboard.",
            "The Father's <em>Can you tell me who you are?</em> must be aimed not at the Manager but at the audience. The actor should let the question land in the house, not on the stage.",
            "The Manager's discomfort during the philosophical stretch is the audience's discomfort. He is the audience proxy. Play him as a man who would like to leave but cannot.",
            "The Step-Daughter's impatience keeps the philosophy from becoming a lecture. Use her interruptions.",
            "The bundle remains in her arms throughout this part. The chair remains at the edge. The Boy and Child are present as objects through every philosophical sentence; the philosophy is happening over their silent bodies.",
            "The Manager's misnumbering of his own act (<em>Ah yes: the second act!</em>) is a quiet joke. Let it land lightly. The audience will catch it."
        ]
    },
    (3, 2): {
        "narrative": [
            "The Manager tries to combine the garden scene and the indoor scene into one staged action. The Boy — the chair-and-coat — is to be moved behind a tree-flat at the back. The Child — the bundle — is to be brought down to the fountain by the Step-Daughter. The Son is to enter from the side and come down to the fountain in time to see the drowning.",
            "The Son refuses. He will not act this. He has never agreed to act it. He cannot leave, but he can refuse to participate, and he intends to. The Step-Daughter laughs at his refusal — he cannot leave, she tells him, because he is <em>indissolubly bound to the chain</em>. The Son delivers his speech on the mirror that throws his own likeness back at him as a horrible grimace. He is, in his own family, an image he cannot live with. The Father tries to force him to play the scene. The Mother begs. The Son does not move.",
            "This is the Son's hour. He refuses the play and yet remains in it — the perfect Pirandellian condition. He is the one who has been right all along, and being right does not save him from anything."
        ],
        "beats": [
            "The Son must be physically isolated. Other actors around him; him alone in his frame. Stage him to be unmoveable, not still.",
            "The Step-Daughter taunts him because she knows he cannot leave. The taunt is therefore loving, not cruel. Find that note.",
            "The Mother trembles because she knows it too. Her trembling is involuntary, not performed.",
            "The mirror speech is the Son's only real cry. He must arrive at it. Do not let him perform it from the first beat — he must be surprised, mid-speech, by what he is saying.",
            "The chair-and-coat is moved behind the tree-flat during this part. Stage the move with weight. The audience should notice a chair being placed.",
            "The Manager is exhausted in this part. Play him as a director who has lost control of his rehearsal and has not yet admitted it.",
            "No laughter in the room. The comedy has burned off completely. What remains is grief that has not yet found a body."
        ]
    },
    (3, 3): {
        "narrative": [
            "The Step-Daughter takes the bundle to the fountain. The Son finally tells what he saw on that afternoon: he ran across the garden, he jumped to drag the Child out of the water, and he was frozen by the sight of the Boy standing stock still by the side of the fountain, his eyes mad, watching his little drowned sister.",
            "The rear wall lights up for the first and only time in the production. For roughly ten seconds, a single held shot: the Boy by the fountain, motionless, watching. No camera movement. No sound. Then darkness. From the darkness, the gunshot. The Mother cries out. The actors lift what they think is the Boy's body, which is the chair-and-coat now being treated as a body. Some say he is dead. Others say it is only pretence. The Father, with a terrible cry: <em>Pretence? Reality, sir, reality!</em> The Manager has had enough: <em>To hell with it all. I've lost a whole day over these people.</em> Curtain.",
            "The climax is delivered as memory, not as scene. The drowning is hidden by the Step-Daughter bending over the bundle at the fountain. The gunshot comes from behind a tree-flat. The Boy is shown — briefly, motionless, on the rear wall — only as the act of watching, not as the act of dying. This is Pirandello's strictest cruelty: the most terrible thing in the play is the thing the audience does not actually see happen."
        ],
        "beats": [
            "The Step-Daughter at the fountain is the play's last live image of love. She is holding a bundle and bending over a basin of nothing. Stage the action with the tenderness of the Act Two opening.",
            "The Son's narration must be the slowest passage in the third act. He is the man who could not move; let his words refuse to move too.",
            "The ten-second projection must feel unhurried. Hold it. The audience should have time to register what they are seeing — and that this is the only time they are seeing it.",
            "The gunshot must be a single, sharp report. Choose between startling the audience and not blowing out the speakers.",
            "The actors lifting the chair-and-coat must treat it as a body. Heavy. Carried with care. The audience reads what the actors give them.",
            "<em>Pretence? Reality, sir, reality!</em> must not be played as resolution. Play it as a contradiction the play cannot solve. The line is a wound, not an answer.",
            "The Manager's last line is not a punchline. He is tired and contemptuous and right and wrong. Play him as the man who has lost a day. Then the curtain comes down on his exhaustion, not on the family's tragedy."
        ]
    },
}

# ===========================================================================
# Generate new HTML for each part-note
# ===========================================================================

SPEAKER_ORDER = [
    'The Manager', 'The Father', 'The Step-Daughter', 'The Son', 'The Mother',
    'Player 1', 'Player 2', 'Player 3',
    'All Three Players', 'Two Players', 'The Manager and The Father'
]

def speaker_sort_key(spk):
    if spk in SPEAKER_ORDER:
        return SPEAKER_ORDER.index(spk)
    return 999

def build_new_part_html(p, idx):
    act, partn = p['act'], None
    # Determine part number within act
    same_act = [x for x in parts if x['act'] == act]
    partn = same_act.index(p) + 1
    key = (act, partn)
    content = PARTS_CONTENT[key]

    # Build narrative paragraphs
    narrative_paras = "\n      ".join(f"<p>{para}</p>" for para in content["narrative"])

    # Build stats list (sorted by speaker order, then word count)
    stats_items = []
    sorted_speakers = sorted(
        p['stats'].items(),
        key=lambda kv: (speaker_sort_key(kv[0]), -kv[1]['words'])
    )
    for spk, st in sorted_speakers:
        c = st['count']
        w = st['words']
        speech_label = 'speech' if c == 1 else 'speeches'
        word_label = 'word' if w == 1 else 'words'
        stats_items.append(
            f'<li><span class="stats-name">{spk}</span>'
            f'<span class="stats-numbers">{c} {speech_label} &middot; {w:,} {word_label}</span></li>'
        )
    # Total
    total_c = sum(st['count'] for st in p['stats'].values())
    total_w = sum(st['words'] for st in p['stats'].values())
    stats_items.append(
        f'<li class="stats-total"><span class="stats-name">Total</span>'
        f'<span class="stats-numbers">{total_c} speeches &middot; {total_w:,} words</span></li>'
    )
    stats_block = "\n        ".join(stats_items)

    # Build beats list
    beats_items = "\n        ".join(f"<li>{b}</li>" for b in content["beats"])

    # Compose the full aside
    html_block = f'''<aside class="part-note">
    <div class="part-eyebrow">{p["eyebrow"]}</div>
    <h3 class="part-title">{p["title"]}</h3>

    <div class="part-narrative">
      {narrative_paras}
    </div>

    <div class="part-divider"></div>

    <div class="part-stats">
      <h4>Who speaks, and how much</h4>
      <ul class="stats-list">
        {stats_block}
      </ul>
    </div>

    <div class="part-divider"></div>

    <div class="part-beats">
      <h4>For the rehearsal room</h4>
      <ul class="beats-list">
        {beats_items}
      </ul>
    </div>
  </aside>'''
    return html_block

# Replace each part-note in the file (in order)
for i, p in enumerate(parts):
    new_block = build_new_part_html(p, i)
    if p['old_html'] in html:
        html = html.replace(p['old_html'], new_block, 1)
    else:
        print(f"!! MISS: part {p['eyebrow']} — {p['title']}")

# ===========================================================================
# Add CSS for the new part-note layout
# ===========================================================================
new_css = """
/* === Rebuilt part notes === */
.part-narrative p { margin: 12px 0; line-height: 1.7; }
.part-narrative p:first-child { margin-top: 0; }
.part-narrative p:last-child { margin-bottom: 0; }

.part-stats { margin: 8px 0; }
.part-stats h4,
.part-beats h4 {
  font-family: 'Cormorant Unicase', 'Cormorant Garamond', serif;
  font-weight: 600;
  font-size: 0.78rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent, #8b3a3a);
  margin: 0 0 12px 0;
}
.stats-list { list-style: none; padding: 0; margin: 0; }
.stats-list li {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 4px 0;
  font-size: 0.95rem;
  border-bottom: 1px dotted var(--rule, rgba(0,0,0,0.12));
}
.stats-list li:last-child { border-bottom: none; }
.stats-list .stats-name { font-style: italic; }
.stats-list .stats-numbers {
  font-variant-numeric: tabular-nums;
  font-size: 0.88rem;
  opacity: 0.82;
  white-space: nowrap;
  margin-left: 16px;
}
.stats-list .stats-total {
  border-top: 1px solid var(--rule, rgba(0,0,0,0.25));
  border-bottom: none;
  margin-top: 4px;
  padding-top: 8px;
  font-weight: 600;
}
.stats-list .stats-total .stats-name { font-style: normal; }

.part-beats { margin: 8px 0 0; }
.beats-list { list-style: none; padding: 0; margin: 0; }
.beats-list li {
  position: relative;
  padding: 6px 0 6px 22px;
  line-height: 1.65;
  font-size: 0.97rem;
}
.beats-list li::before {
  content: "—";
  position: absolute;
  left: 0;
  color: var(--accent, #8b3a3a);
  font-weight: 600;
}

.part-divider {
  height: 1px;
  background: var(--rule, rgba(0,0,0,0.12));
  margin: 18px 0;
}
"""
if ".part-narrative p" not in html:
    html = html.replace("</style>", new_css + "</style>", 1)

# ===========================================================================
# Save & report
# ===========================================================================
SRC.write_text(html)

n_speech = len(re.findall(r'<p class="speech">', html))
n_parts = len(re.findall(r'class="part-note"', html))
print(f"\nFile: {SRC} ({len(html):,} bytes; Δ {len(html)-original_len:+,})")
print(f"Speeches: {n_speech} (expected 634)")
print(f"Part notes: {n_parts} (expected 9)")

# Per-part summary
print("\n=== PART STATS SUMMARY ===")
for p in parts:
    act = p['act']
    same_act = [x for x in parts if x['act'] == act]
    pn = same_act.index(p) + 1
    total_c = sum(st['count'] for st in p['stats'].values())
    total_w = sum(st['words'] for st in p['stats'].values())
    print(f"  Act {act}, Part {pn}: {p['title']:25} → {total_c:3} speeches · {total_w:5,} words")
