#!/usr/bin/env python3
"""Build the Audition Two-Hander Pack PDF.

For every pair of speaking characters, a self-contained two-hander side
in which ONLY those two speak. Organised by character: each character's
section contains a scene with every other character, so in the audition
room you flip to whoever is reading and find all their pairings together.

Eight speaking roles: Father, Mother, Step-Daughter, Son, Manager,
Player 1, Player 2, Player 3 (who also plays Madame Pace). That is 28
unique pairings; each is printed in both partners' sections.

Each scene runs well above the minimum of five exchanges, draws on the
character voices established in the Director's Copy, and uses the
metatheatrical frame for Character-meets-Player pairings (the Player is
cast to play the Character, and they meet to work on the role).
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

# ---------------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------------

ROLE_ORDER = ["F", "M", "SD", "S", "MG", "P1", "P2", "P3"]
ROLE_NAME = {
    "F": "The Father",
    "M": "The Mother",
    "SD": "The Step-Daughter",
    "S": "The Son",
    "MG": "The Manager",
    "P1": "Player 1",
    "P2": "Player 2",
    "P3": "Player 3",
}
ROLE_NOTE = {
    "F": "the brain of the family — philosophy as confession",
    "M": "grief, the veil, the three silences",
    "SD": "the moral centre — sharp, indicting, never coquettish",
    "S": "the refuser — withholding as an act",
    "MG": "the audience's body on stage — pragmatic, tired",
    "P1": "the Leading Man — vain, faded, defensive",
    "P2": "the Leading Lady — practical, professional, employed",
    "P3": "the youngest, curious — and Madame Pace",
}

# ---------------------------------------------------------------------------
# Scenes — keyed by a sorted pair of role keys.
# Each scene: {"context": str, "lines": [(SPEAKER_LABEL, text), ...]}
# ---------------------------------------------------------------------------

def key(a, b):
    return tuple(sorted((a, b), key=ROLE_ORDER.index))

SCENES = {
    key("F", "M"): {
        "context": "Years after he sent her away to another man. He defends the choice as kindness; she will not let him call it that.",
        "lines": [
            ("FATHER", "You needn't look away from me. I am not the man who wronged you. That man is gone; I have to live as what is left of him."),
            ("MOTHER", "You always have an answer. I only have the children."),
            ("FATHER", "I gave you to a better man. I thought it was kindness."),
            ("MOTHER", "You sent me away. Call it whatever you like — you sent me away."),
            ("FATHER", "I pitied you. Is that nothing?"),
            ("MOTHER", "Pity is what you felt. Loss is what I carried. They are not the same weight."),
            ("FATHER", "...No. They are not."),
            ("MOTHER", "Then do not ask me to stand here and call it kindness."),
        ],
    },
    key("F", "SD"): {
        "context": "The core confrontation. She refuses to let his philosophy bury what happened in the shop.",
        "lines": [
            ("STEP-DAUGHTER", "Go on. Tell them the philosophy. Tell them all about reality."),
            ("FATHER", "I am trying to explain —"),
            ("STEP-DAUGHTER", "Explain the shop. Explain the hundred francs. Start there."),
            ("FATHER", "You will not let me be more than that one afternoon."),
            ("STEP-DAUGHTER", "You were not more than that, to me, in that room."),
            ("FATHER", "I did not know who you were."),
            ("STEP-DAUGHTER", "You knew I was young. You knew that much, and it did not stop you."),
            ("FATHER", "...I have to live with what you are saying."),
            ("STEP-DAUGHTER", "Good. Live with it out loud, where they can all hear."),
        ],
    },
    key("F", "S"): {
        "context": "The father reaches for the son who has decided to give him nothing.",
        "lines": [
            ("FATHER", "Look at me. Once. You can refuse everything else, but look at me."),
            ("SON", "I have nothing to say to you."),
            ("FATHER", "You have everything to say. You simply will not."),
            ("SON", "What you call my silence is the only thing in this family that is mine."),
            ("FATHER", "I am your father."),
            ("SON", "You are a man who keeps announcing it, as though saying it could make it true."),
            ("FATHER", "And if I beg?"),
            ("SON", "Then I will watch you beg. I still will not move."),
        ],
    },
    key("F", "MG"): {
        "context": "The Father argues the company into staging the family at all. The Manager is the audience deciding whether to stay.",
        "lines": [
            ("FATHER", "You think we are mad. I saw it the moment we walked in."),
            ("MANAGER", "I think you are six people interrupting a rehearsal I am already behind on."),
            ("FATHER", "And yet you have not thrown us out."),
            ("MANAGER", "...No. I haven't."),
            ("FATHER", "Because something in you wants to know how it ends."),
            ("MANAGER", "What I want is my morning back."),
            ("FATHER", "That is not a denial."),
            ("MANAGER", "No. God help me, it isn't. Go on, then. Show me."),
        ],
    },
    key("M", "SD"): {
        "context": "Mother and daughter over the same wound. The Mother wants it to stop; the Step-Daughter will not let it.",
        "lines": [
            ("STEP-DAUGHTER", "Don't cover your face. Not with me."),
            ("MOTHER", "I cannot watch you do this to yourself."),
            ("STEP-DAUGHTER", "I am not doing it to myself. I am doing it to him. You should want that too."),
            ("MOTHER", "I want it to stop. That is all I have ever wanted."),
            ("STEP-DAUGHTER", "It does not stop. It is taking place now. It is always taking place."),
            ("MOTHER", "You sound like him when you talk that way."),
            ("STEP-DAUGHTER", "...Don't. Don't ever say that to me."),
            ("MOTHER", "Then come away from the edge of it. Please."),
        ],
    },
    key("M", "S"): {
        "context": "The mother who was sent away, and the son she left behind to remember it.",
        "lines": [
            ("MOTHER", "I only want to look at you. I am not asking for anything else."),
            ("SON", "You left."),
            ("MOTHER", "I was sent."),
            ("SON", "It is the same house either way, with you not in it."),
            ("MOTHER", "I have carried you every day since."),
            ("SON", "You carried the others. I was the one you left behind to do the remembering."),
            ("MOTHER", "Is there nothing I can say?"),
            ("SON", "There is nothing either of us can say. That is what we are."),
        ],
    },
    key("M", "MG"): {
        "context": "The Manager wants a clean version he can stage. The Mother instructs the audience-proxy in what a play cannot do.",
        "lines": [
            ("MANAGER", "Madam — please — if you could just tell me, plainly, what happened."),
            ("MOTHER", "You want it plainly. There is no plainly."),
            ("MANAGER", "A sentence. Anything I can stage."),
            ("MOTHER", "You cannot stage it. You can only make us do it again."),
            ("MANAGER", "That is what a play is, madam."),
            ("MOTHER", "Then your play is cruel, and you do not know it yet."),
            ("MANAGER", "..."),
            ("MOTHER", "Now you are quiet. Good. That is the right thing to be."),
        ],
    },
    key("SD", "S"): {
        "context": "She taunts him for refusing to stand even for his own mother. He insists his refusal is freedom.",
        "lines": [
            ("STEP-DAUGHTER", "Look at him. He will not even stand for his own mother."),
            ("SON", "Leave me out of your performance."),
            ("STEP-DAUGHTER", "It is not a performance. It is the truth, and you are in it whether you speak or not."),
            ("SON", "I am bound to nothing."),
            ("STEP-DAUGHTER", "You are bound to this chain like the rest of us. You simply pretend the chain is a choice."),
            ("SON", "Better to pretend than to display myself the way you do."),
            ("STEP-DAUGHTER", "I display myself so the room cannot look away. You hide so it can."),
            ("SON", "Then let it look away. I would prefer that."),
        ],
    },
    key("SD", "MG"): {
        "context": "She catches the Manager softening her story into something the audience can bear. This is her central fight.",
        "lines": [
            ("STEP-DAUGHTER", "You keep softening it. Every time I say what happened, you reach for a nicer word."),
            ("MANAGER", "I am trying to make it playable."),
            ("STEP-DAUGHTER", "Make it true first. Playable after."),
            ("MANAGER", "An audience has to be able to bear it."),
            ("STEP-DAUGHTER", "Why? I had to bear it. Let them do the same, for two hours."),
            ("MANAGER", "You are not making this easy."),
            ("STEP-DAUGHTER", "It was not easy. That is the part you keep editing out."),
            ("MANAGER", "...All right. Say it your way. I'm listening."),
        ],
    },
    key("S", "MG"): {
        "context": "The Manager needs the Son in the scene. The Son refuses to be made convenient.",
        "lines": [
            ("MANAGER", "I need you in the scene. The whole thing turns on you."),
            ("SON", "Then your whole thing does not turn."),
            ("MANAGER", "You are a character in a play. Characters play their scenes."),
            ("SON", "I am a character who was never finished. You cannot make me act what was never written."),
            ("MANAGER", "Everyone here is improvising. Join us."),
            ("SON", "No. My refusal is the only finished thing about me."),
            ("MANAGER", "You are impossible."),
            ("SON", "I am consistent. You simply wanted me to be convenient."),
        ],
    },
    key("SD", "P3"): {
        "context": "The atelier. Madame Pace (Player 3) and the Step-Daughter, back in the room of the hundred francs.",
        "lines": [
            ("MADAME PACE", "Cara, you come back. I knew you come back. The young ones, they always come back."),
            ("STEP-DAUGHTER", "I did not come back. You dragged me here by remembering it."),
            ("MADAME PACE", "Eh — remember, come back, for the book it is the same. The book must balance."),
            ("STEP-DAUGHTER", "There is no book. There was a girl, and a hundred francs, and you, smiling."),
            ("MADAME PACE", "I smile because I am polite. The polite ones, they pay more."),
            ("STEP-DAUGHTER", "You sold me an afternoon you knew was poison."),
            ("MADAME PACE", "I sold what was asked. You want to be angry — be angry at the one who asked."),
            ("STEP-DAUGHTER", "I am angry at both of you. There is enough of it to go around."),
        ],
    },
    key("F", "P3"): {
        "context": "The customer and the keeper of the shop. Madame Pace (Player 3) ties his shame to her ledger.",
        "lines": [
            ("MADAME PACE", "Ah, monsieur. You, I remember. The good coat, the quiet voice. The ones with the quiet voice — they are the worst."),
            ("FATHER", "I did not know who she was."),
            ("MADAME PACE", "You did not ask. That is not the same as not knowing."),
            ("FATHER", "You arranged it. You put her in that room."),
            ("MADAME PACE", "I put many girls in that room. You were not special, monsieur. You only think so now, because it shames you."),
            ("FATHER", "Do not speak to me as if we are the same."),
            ("MADAME PACE", "We are not the same. I kept a book. You kept a philosophy. The girl paid for both."),
            ("FATHER", "..."),
            ("MADAME PACE", "Now you are quiet too. Bon. The quiet ones — the worst."),
        ],
    },
    key("M", "P3"): {
        "context": "The Mother's eruption. Madame Pace (Player 3) answers with the cold arithmetic of the trade.",
        "lines": [
            ("MOTHER", "You. You old devil. You murderess."),
            ("MADAME PACE", "Eh, madame, such words. I am a businesswoman."),
            ("MOTHER", "You sold my daughter."),
            ("MADAME PACE", "I sold a dress, a room, a half-hour. What happened inside — that is not on my book."),
            ("MOTHER", "Everything that happened is on your book. You wrote it in francs."),
            ("MADAME PACE", "Francs do not lie, madame. People lie. Francs, they only add up."),
            ("MOTHER", "May they add up to your damnation."),
            ("MADAME PACE", "...You pray very prettily. It will not change the total."),
        ],
    },
    key("MG", "P1"): {
        "context": "The cook's-cap argument. The vain Leading Man against the tired Manager.",
        "lines": [
            ("PLAYER 1", "Must I absolutely wear the cook's cap?"),
            ("MANAGER", "It is in the script. The script you signed for."),
            ("PLAYER 1", "I have a reputation in this canton."),
            ("MANAGER", "You had one. Put the cap on, and you may keep what's left of it."),
            ("PLAYER 1", "I'd sooner resign."),
            ("MANAGER", "You say that every season. You never do."),
            ("PLAYER 1", "One day I shall surprise you."),
            ("MANAGER", "Surprise me by being ready when I call the scene. Cap on. Go."),
        ],
    },
    key("MG", "P2"): {
        "context": "The Manager has no scene yet. The practical Leading Lady will act anything — once he gives her a beginning.",
        "lines": [
            ("MANAGER", "Can we please just rehearse? I've lost half the morning."),
            ("PLAYER 2", "We can rehearse the moment someone tells me what the scene actually is."),
            ("MANAGER", "The scene is six strangers and their tragedy."),
            ("PLAYER 2", "That is not a scene. That is a situation. A scene has a beginning."),
            ("MANAGER", "...You're right. I don't have a beginning yet."),
            ("PLAYER 2", "Then find one, and I'll act it. I'm a professional. I just need something to be professional about."),
            ("MANAGER", "Give me five minutes."),
            ("PLAYER 2", "I'll be here. I'm always here. That's rather the problem."),
        ],
    },
    key("MG", "P3"): {
        "context": "The tired Manager and the youngest member of the company, who has never seen a rehearsal do this.",
        "lines": [
            ("PLAYER 3", "Sorry — should I still be taking this down? In shorthand?"),
            ("MANAGER", "Take everything down. I don't know yet what matters."),
            ("PLAYER 3", "It's only — I've never seen a rehearsal do this before."),
            ("MANAGER", "Neither have I, and I've done forty of them."),
            ("PLAYER 3", "Is that exciting, or is that bad?"),
            ("MANAGER", "At my age the two feel remarkably similar."),
            ("PLAYER 3", "I think it's exciting."),
            ("MANAGER", "Hold on to that. You'll need it more than the shorthand."),
        ],
    },
    key("P1", "P2"): {
        "context": "Two registers of the same profession. The vain one and the employed one.",
        "lines": [
            ("PLAYER 1", "In my day a script made sense before we started."),
            ("PLAYER 2", "In your day. Yes. We've all heard about your day."),
            ("PLAYER 1", "I am only saying a Leading Man requires a part."),
            ("PLAYER 2", "A Leading Man requires an audience. A working actor requires a wage. Guess which of us booked the job."),
            ("PLAYER 1", "You wound me."),
            ("PLAYER 2", "I pay rent. Wounding you is a hobby, not a profession."),
            ("PLAYER 1", "...You are very hard, you know."),
            ("PLAYER 2", "I'm very employed. Take notes."),
        ],
    },
    key("P1", "P3"): {
        "context": "The senior Leading Man instructs the newest member of the company in how things 'really' work.",
        "lines": [
            ("PLAYER 1", "You're new, so I'll tell you how this works. The Leading Man sets the tone."),
            ("PLAYER 3", "Oh — does he? I thought the director did."),
            ("PLAYER 1", "The director thinks he does. That is a different matter."),
            ("PLAYER 3", "I'll write that down."),
            ("PLAYER 1", "Don't write it down. That's exactly the sort of thing one does not write down."),
            ("PLAYER 3", "Sorry. I write everything down. It's my first proper season."),
            ("PLAYER 1", "...It shows. But not unpleasantly."),
            ("PLAYER 3", "Was that a compliment?"),
            ("PLAYER 1", "From me, child, it was practically a bouquet."),
        ],
    },
    key("P2", "P3"): {
        "context": "The veteran and the beginner. The youngest wants it all to mean something; the elder has made her peace.",
        "lines": [
            ("PLAYER 3", "Can I ask you something? How do you stay so calm when it all falls apart?"),
            ("PLAYER 2", "Practice. And lowered expectations. Mostly the second one."),
            ("PLAYER 3", "I keep wanting it to mean something."),
            ("PLAYER 2", "It will, sometimes. Don't build your week around those times."),
            ("PLAYER 3", "That's a little bleak."),
            ("PLAYER 2", "It's a little true. The bleakness is free; the truth you earn."),
            ("PLAYER 3", "I hope I'm like you in twenty years."),
            ("PLAYER 2", "Aim higher, love. Aim to be employed and unbothered. I only ever managed the first."),
        ],
    },
    # ---- Character × Player: the metatheatrical frame ----
    key("F", "P1"): {
        "context": "Player 1 is cast to play the Father in the staged version, and comes to him for the character.",
        "lines": [
            ("PLAYER 1", "So I'm to play you. I'll need to understand the man. What's my motivation?"),
            ("FATHER", "My motivation is not to be reduced to a motivation."),
            ("PLAYER 1", "That's not very helpful for an actor."),
            ("FATHER", "It is the truest thing I can give you. The moment you decide what I 'want,' you have already made me smaller than I am."),
            ("PLAYER 1", "Then how do I play you?"),
            ("FATHER", "Play a man who is ashamed and cannot stop talking — because the talking is the only thing keeping the shame from arriving."),
            ("PLAYER 1", "...That, I can do."),
            ("FATHER", "I was afraid you could."),
        ],
    },
    key("F", "P2"): {
        "context": "Player 2 is reading the Mother in the staged version. The Father, of all people, coaches her on his wife's grief.",
        "lines": [
            ("PLAYER 2", "They've got me reading your wife. I want to get her right."),
            ("FATHER", "Then do not act her grief. Carry it. There is a difference, and the audience knows it before you do."),
            ("PLAYER 2", "That's a note I'd give, not take."),
            ("FATHER", "You asked. I have watched her grief from inside the marriage that caused it. I know its weight to the gram."),
            ("PLAYER 2", "...All right. Carry it. Not perform it."),
            ("FATHER", "Yes. And when you cover your face, mean it. She is not hiding from us. She is hiding from the memory."),
            ("PLAYER 2", "You speak about her very tenderly, for a man who ruined her."),
            ("FATHER", "Tenderness and ruin are not opposites. That is the whole tragedy. Write that one down."),
        ],
    },
    key("M", "P1"): {
        "context": "Player 1 is cast as the husband. The Mother tells him the one thing that will hurt the man most: ordinariness.",
        "lines": [
            ("PLAYER 1", "I'm to play your husband in the staged version. Any guidance?"),
            ("MOTHER", "Do not make him a villain. He would love that. It would let him off."),
            ("PLAYER 1", "Off how?"),
            ("MOTHER", "A villain is interesting. He would rather be interesting than ordinary. Play him ordinary. It will hurt him more."),
            ("PLAYER 1", "That's rather a sophisticated note."),
            ("MOTHER", "I had years to arrive at it. You have a fortnight. Use mine."),
            ("PLAYER 1", "...Ordinary. Right."),
            ("MOTHER", "Ordinary, and certain he is kind. That is the man. That is exactly the man."),
        ],
    },
    key("M", "P2"): {
        "context": "Player 2 is cast to play the Mother and wants to get her right. The Mother warns her off sympathy.",
        "lines": [
            ("PLAYER 2", "I'm playing you. I don't want to get you wrong."),
            ("MOTHER", "You will get me wrong if you try to make me sympathetic."),
            ("PLAYER 2", "Aren't you?"),
            ("MOTHER", "I am silent. Silence is not sympathy. People decide I am gentle because I do not argue. I do not argue because there is nothing left to win."),
            ("PLAYER 2", "So I play... defeat?"),
            ("MOTHER", "You play someone who is still here after defeat. That is harder. That is the part."),
            ("PLAYER 2", "I've been acting forty years, and that's the best note I've had all week."),
            ("MOTHER", "Then it was worth saying out loud. I do so little of that."),
        ],
    },
    key("S", "P1"): {
        "context": "Player 1 is sent to coax the Son into the scene, actor to actor. It does not go well.",
        "lines": [
            ("PLAYER 1", "They want me to coax you into the scene. Actor to actor."),
            ("SON", "Then they have wasted your morning as well as mine."),
            ("PLAYER 1", "Come now. We all play parts we'd rather not."),
            ("SON", "You play parts you'd rather not, for a wage. I am asked to play the worst night of a family that was never even finished."),
            ("PLAYER 1", "...When you put it like that."),
            ("SON", "There is no other way to put it. That is why I put it like that."),
            ("PLAYER 1", "I shan't coax you, then."),
            ("SON", "Good. You're the first one all day with the sense not to."),
        ],
    },
    key("S", "P2"): {
        "context": "Player 2 doesn't pretend to understand the Son. He respects her for it.",
        "lines": [
            ("PLAYER 2", "I won't pretend I understand you. But I'd like to."),
            ("SON", "That's more honest than the others. They all pretend."),
            ("PLAYER 2", "I'm too old to pretend off the clock."),
            ("SON", "Then understand this: I am not sulking. I have made a decision, and I am keeping it. People mistake the two."),
            ("PLAYER 2", "A decision to do nothing."),
            ("SON", "A decision not to be used. There's a difference — and you of all people should feel it."),
            ("PLAYER 2", "...I do, actually."),
            ("SON", "Then we understand each other. That's rarer here than you'd think."),
        ],
    },
    key("S", "P3"): {
        "context": "The youngest in the company asks the Son the question no one else dares: why won't you just do it?",
        "lines": [
            ("PLAYER 3", "Can I ask — and tell me to stop — why won't you just do the scene?"),
            ("SON", "Because the scene is my family being torn open, and I am asked to hold it open with my own hands."),
            ("PLAYER 3", "I think I'd refuse too."),
            ("SON", "You're the only one who's said so."),
            ("PLAYER 3", "I'm new. I haven't learned to pretend it's normal yet."),
            ("SON", "Don't learn. The day it looks normal to you, you've lost something."),
            ("PLAYER 3", "I'll try to remember that."),
            ("SON", "You won't. But it was kind of you to say."),
        ],
    },
    key("SD", "P1"): {
        "context": "Player 1 is cast as the gentleman in the shop scene. The Step-Daughter tells him exactly how to play her abuser.",
        "lines": [
            ("PLAYER 1", "I'm cast as the gentleman in your... in the shop scene."),
            ("STEP-DAUGHTER", "The gentleman. Is that what they're calling him today."),
            ("PLAYER 1", "It's the role as written."),
            ("STEP-DAUGHTER", "Then play him as he was. Polite. Soft-voiced. Certain he'd done nothing wrong. Don't give him horns — he didn't have any. That's what made it worse."),
            ("PLAYER 1", "You want me to make the audience comfortable with him."),
            ("STEP-DAUGHTER", "I want you to make them comfortable — and then I'll do the rest. Your comfort is my weapon. Hand it to me."),
            ("PLAYER 1", "...That's almost frightening."),
            ("STEP-DAUGHTER", "It's supposed to be. You're learning."),
        ],
    },
    key("SD", "P2"): {
        "context": "Player 2 is cast to play the Step-Daughter and laughed while reading it. The Step-Daughter turns the laugh into the performance.",
        "lines": [
            ("PLAYER 2", "They've given me you to play. I'd like to do you justice."),
            ("STEP-DAUGHTER", "Don't do me justice. Justice is what I never got. Do me accurately."),
            ("PLAYER 2", "Tell me the difference."),
            ("STEP-DAUGHTER", "Justice makes me a martyr. Accurate makes me furious, and right, and not at all interested in your tears."),
            ("PLAYER 2", "I laughed at you, earlier. When I first read it. I'm sorry."),
            ("STEP-DAUGHTER", "Everyone laughs first. Then they hear what they laughed at. Use that. Make them laugh — then make them choke on it."),
            ("PLAYER 2", "...I've been made a fool of by worse than this play."),
            ("STEP-DAUGHTER", "Then you'll play me perfectly. A woman who's been made a fool of, and has stopped allowing it."),
        ],
    },
}

# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render_scene(role, other):
    sc = SCENES[key(role, other)]
    lines_html = "".join(
        f'<p class="line"><span class="sp">{spk}.</span> {txt}</p>'
        for spk, txt in sc["lines"]
    )
    return f"""
    <div class="scene">
      <div class="scene-head">
        <span class="scene-with">with</span>
        <span class="scene-partner">{ROLE_NAME[other]}</span>
      </div>
      <p class="scene-context">{sc['context']}</p>
      {lines_html}
    </div>
    """

def render_section(role):
    partners = [r for r in ROLE_ORDER if r != role]
    scenes_html = "".join(render_scene(role, other) for other in partners)
    return f"""
    <section class="role-section">
      <div class="role-head">
        <h2>{ROLE_NAME[role]}</h2>
        <p class="role-note">{ROLE_NOTE[role]}</p>
        <p class="role-count">{len(partners)} two-handers &middot; one with each other speaking role</p>
      </div>
      {scenes_html}
    </section>
    """

SECTIONS_HTML = "".join(render_section(r) for r in ROLE_ORDER)

# Build a simple "who reads with whom" matrix for the front matter
matrix_rows = ""
for r in ROLE_ORDER:
    cells = ""
    for c in ROLE_ORDER:
        if r == c:
            cells += '<td class="x">&mdash;</td>'
        else:
            cells += '<td class="y">&#10003;</td>'
    matrix_rows += f'<tr><th>{ROLE_NAME[r]}</th>{cells}</tr>'
matrix_head = "".join(f'<th class="rot">{ROLE_NAME[c]}</th>' for c in ROLE_ORDER)

HTML = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Audition Two-Hander Pack — Six Characters in Search of an Author</title>
<style>
  :root {{ --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }}
  @page {{ size: A4; margin: 20mm 20mm 20mm 20mm; }}
  *,*::before,*::after {{ box-sizing: border-box; }}
  html, body {{ background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif;
    font-size: 11pt; line-height: 1.6; margin: 0; padding: 0; }}
  main {{ max-width: 168mm; margin: 0 auto; }}

  .masthead {{ text-align: center; margin-bottom: 7mm; padding-bottom: 5mm; border-bottom: 1px solid var(--rule); }}
  .eyebrow {{ font-family:'Cormorant Unicase',serif; font-weight:600; font-size: 9pt;
             letter-spacing: 0.26em; text-transform: uppercase; color: var(--accent); margin: 0 0 4mm 0; }}
  h1 {{ font-family:'Cormorant Garamond',serif; font-weight: 500; font-size: 21pt; line-height: 1.15; margin: 0 0 2mm 0; }}
  .play {{ font-style: italic; font-size: 11pt; color: var(--ink-soft); margin: 0 0 3mm 0; }}
  .credit {{ font-size: 10.5pt; color: var(--ink); margin: 0; letter-spacing: 0.04em; }}

  .intro h2 {{ font-family:'Cormorant Unicase',serif; font-weight: 600; font-size: 11pt;
              letter-spacing: 0.20em; text-transform: uppercase; color: var(--accent); margin: 7mm 0 3mm 0; }}
  .intro p {{ margin: 0 0 3mm 0; }}
  .intro ul {{ margin: 0 0 3mm 0; padding-left: 6mm; }}
  .intro li {{ margin-bottom: 2mm; }}

  /* Matrix */
  table.matrix {{ border-collapse: collapse; margin: 4mm auto 2mm; font-size: 9pt; }}
  table.matrix th, table.matrix td {{ border: 1px solid var(--rule); padding: 1.6mm 2mm; text-align: center; }}
  table.matrix th {{ font-family:'Cormorant Garamond',serif; font-weight: 600; color: var(--ink); }}
  table.matrix th.rot {{ font-size: 8pt; }}
  table.matrix tr th:first-child {{ text-align: left; white-space: nowrap; color: var(--accent); }}
  table.matrix td.y {{ color: var(--accent); }}
  table.matrix td.x {{ color: var(--ink-soft); background: rgba(42,32,26,0.05); }}

  /* Role sections */
  .role-section {{ page-break-before: always; }}
  .role-head {{ border-bottom: 2px solid var(--accent); margin-bottom: 5mm; padding-bottom: 2mm; }}
  .role-head h2 {{ font-family:'Cormorant Garamond',serif; font-weight: 500; font-size: 24pt;
                  color: var(--accent); margin: 0; }}
  .role-note {{ font-style: italic; color: var(--ink-soft); margin: 1mm 0 0 0; font-size: 11pt; }}
  .role-count {{ font-family:'Cormorant Unicase',serif; font-size: 8.5pt; letter-spacing: 0.14em;
                text-transform: uppercase; color: var(--ink-soft); margin: 2mm 0 0 0; }}

  /* Scene */
  .scene {{ page-break-inside: avoid; margin: 0 0 7mm 0; padding: 4mm 5mm 4mm 5mm;
           border-left: 2px solid var(--rule); background: rgba(255,255,255,0.22); }}
  .scene-head {{ margin: 0 0 1mm 0; }}
  .scene-with {{ font-family:'Cormorant Unicase',serif; font-size: 8.5pt; letter-spacing: 0.16em;
                text-transform: uppercase; color: var(--ink-soft); }}
  .scene-partner {{ font-family:'Cormorant Garamond',serif; font-weight: 600; font-size: 14pt; color: var(--ink); }}
  .scene-context {{ font-style: italic; color: var(--ink-soft); font-size: 10pt; margin: 0 0 3mm 0; line-height: 1.45; }}
  .line {{ margin: 0 0 2mm 0; line-height: 1.5; }}
  .sp {{ font-family:'Cormorant Unicase',serif; font-weight: 600; font-size: 8.5pt;
        letter-spacing: 0.10em; text-transform: uppercase; color: var(--accent); }}

  footer.foot {{ margin-top: 9mm; padding-top: 4mm; border-top: 1px solid var(--rule);
                font-size: 9.5pt; color: var(--ink-soft); font-style: italic; text-align: center; line-height: 1.55; }}
  footer.foot strong {{ font-style: normal; color: var(--ink); }}
</style>
</head><body>

<main>

  <div class="masthead">
    <p class="eyebrow">Audition Two-Hander Pack</p>
    <h1>Six Characters<br>in Search of an Author</h1>
    <p class="play">Sei personaggi in cerca d'autore &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
    <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne</p>
    <p class="credit" style="margin-top:6px;">Director: <strong>Kiarash Jamshidi</strong></p>
  </div>

  <section class="intro">
    <h2>What this is</h2>
    <p>A two-hander side for every pairing of the eight speaking roles. In each scene <strong>only the two named characters speak</strong> — so you can sit any two auditioners (or an auditioner and a reader) down and run a clean scene with no third voice.</p>
    <p>Each side carries well above the minimum of five exchanges, so there is enough to read, redirect, and read again. The voices follow the production's readings in the Director's Copy.</p>

    <h2>How it's organised</h2>
    <p>By character. Each of the eight speaking roles has its own section containing a two-hander with <strong>every other speaking role</strong>. So if you are seeing people for the Father today, go to <em>The Father</em> and every Father pairing is there in one place — you never have to flip.</p>
    <ul>
      <li>Every scene therefore appears <strong>twice</strong> — once in each partner's section. That is deliberate, not an error: it keeps each character's material whole.</li>
      <li>Where a <strong>Character meets a Player</strong> (e.g. the Father and Player 1), the scene uses the production's own logic — the Player has been cast to play that Character, and they meet to work on the role. These sides test something rare and very Pirandellian: a reader playing an actor playing a part.</li>
      <li>Player 3's scenes with the Step-Daughter, the Father, and the Mother are played <strong>as Madame Pace</strong> — the shop, the ledger, the cold.</li>
    </ul>

    <h2>How to use it in the room</h2>
    <ul>
      <li>Pick the pairing that fits who is auditioning. Hand each reader their lines.</li>
      <li>Let them read it once as prepared, then give <strong>one</strong> adjustment and read it again — that single redirection tells you more than the first read.</li>
      <li>For the Character–Player sides, you can cast the auditioner as either the Character or the Player, depending on which role you are testing them for.</li>
    </ul>

    <h2>The pairing matrix</h2>
    <p>Every cell marked is a scene in this pack (found in both roles' sections).</p>
    <table class="matrix">
      <tr><th></th>{matrix_head}</tr>
      {matrix_rows}
    </table>
  </section>

  {SECTIONS_HTML}

  <footer class="foot">
    <p><strong>Village Players · Lausanne</strong> &nbsp;·&nbsp; Director: Kiarash Jamshidi</p>
    <p>Companion to the Audition Pack (single-character sides) and the Audition Checklist. The character readings follow the Director's Copy.</p>
  </footer>

</main>

</body></html>
"""

HTML_PATH = OUT_DIR / "audition_twohanders.html"
HTML_PATH.write_text(HTML)

OUT = OUT_DIR / "audition_twohanders.pdf"
with sync_playwright() as p:
    launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
    browser = p.chromium.launch(**launch_kwargs)
    page = browser.new_page()
    page.goto(f"file://{HTML_PATH.resolve()}", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(600)
    page.pdf(path=str(OUT), format="A4",
             margin={"top": "20mm", "right": "20mm", "bottom": "20mm", "left": "20mm"},
             print_background=True, prefer_css_page_size=True)
    browser.close()

try:
    from pypdf import PdfReader
    r = PdfReader(str(OUT))
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes) · {len(r.pages)} pages")
except BaseException:
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes)")
