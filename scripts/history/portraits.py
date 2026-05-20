#!/usr/bin/env python3
"""Insert a 'Portraits' section between the cast list and scene-setting,
giving each Character (and the Manager) a body, a nature, and a note to the actor."""
import re
from pathlib import Path

SRC = Path("/home/claude/six_characters.html")
html = SRC.read_text()

# ---------------------------------------------------------------------------
# CSS for .portraits and .portrait
# ---------------------------------------------------------------------------
PORTRAIT_CSS = r"""
/* === Portraits gallery before Act I === */
.portraits {
  margin: 96px 0 80px;
  padding: 0;
}
.portraits-h2 {
  font-family: 'Cormorant Unicase', serif;
  font-size: 11px;
  letter-spacing: 0.5em;
  color: var(--accent);
  font-weight: 500;
  text-align: center;
  margin: 0 0 10px;
  text-transform: uppercase;
}
.portraits-sub {
  text-align: center;
  font-style: italic;
  color: var(--ink-soft);
  margin: 0 auto 12px;
  font-size: 16px;
  max-width: 540px;
  font-family: 'Cormorant Infant', 'Cormorant Garamond', serif;
}
.portraits-intro {
  text-align: center;
  font-style: italic;
  color: var(--ink-faint);
  margin: 0 auto 48px;
  font-size: 14.5px;
  max-width: 560px;
  line-height: 1.65;
  font-family: 'Cormorant Infant', 'EB Garamond', serif;
  padding: 16px 0 22px;
  border-bottom: 1px solid var(--rule);
}

.portrait {
  position: relative;
  padding: 44px 0 38px;
  border-bottom: 1px solid var(--rule);
}
.portrait:last-child {
  border-bottom: 0;
  padding-bottom: 20px;
}
.portrait .p-num {
  position: absolute;
  top: 50px;
  left: -8px;
  font-family: 'Cormorant Infant', 'Cormorant Garamond', serif;
  font-style: italic;
  color: var(--accent);
  font-size: 13px;
  letter-spacing: 0.18em;
  opacity: 0.65;
}
.portrait .p-name {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 300;
  font-style: italic;
  font-size: clamp(28px, 4vw, 38px);
  text-align: center;
  margin: 0 0 10px;
  color: var(--ink);
  letter-spacing: -0.005em;
  line-height: 1.08;
}
.portrait .p-tag {
  display: block;
  text-align: center;
  font-family: 'Cormorant Unicase', serif;
  font-size: 9px;
  letter-spacing: 0.5em;
  color: var(--ink-faint);
  margin: 0 0 32px;
  text-transform: uppercase;
  font-weight: 500;
}
.portrait .p-block {
  margin: 0 0 18px;
  display: grid;
  grid-template-columns: 110px 1fr;
  gap: 20px;
  align-items: baseline;
}
.portrait .p-block:last-child {
  margin-bottom: 0;
}
.portrait .p-block h4 {
  font-family: 'Cormorant Unicase', serif;
  font-size: 10px;
  letter-spacing: 0.42em;
  color: var(--accent);
  margin: 0;
  text-transform: uppercase;
  font-weight: 500;
  text-align: right;
  padding-top: 4px;
}
.portrait .p-block p {
  margin: 0;
  font-family: 'Cormorant Garamond', 'EB Garamond', serif;
  font-style: italic;
  font-size: calc(var(--base-fs, 19px) * 0.96);
  line-height: 1.66;
  color: var(--ink-soft);
}
@media (max-width: 720px) {
  .portrait .p-block {
    grid-template-columns: 1fr;
    gap: 6px;
  }
  .portrait .p-block h4 {
    text-align: left;
    padding-top: 0;
  }
  .portrait .p-num { display: none; }
  .portraits { margin: 64px 0; }
}
"""

html = html.replace("</style>", PORTRAIT_CSS + "\n</style>", 1)

# ---------------------------------------------------------------------------
# THE 8 PORTRAITS
# ---------------------------------------------------------------------------
PORTRAITS = [
    {
        "num": "i", "name": "The Father", "tag": "the brain of the family",
        "appearance": "Around fifty. Reddish hair, thinned at the temples but not yet gone. A thick moustache hanging over a still-fresh mouth that smiles at strangers without quite committing to the smile. Heavy in the body, pale in the face, wide-browed. Pale blue eyes that go sharp the moment he is interrupted. Light trousers, a dark jacket — the dress of a man in the middle of his ordinary life.",
        "nature": "Alternately mellifluous and violent. The play's philosophical voice — a man who argues for his life by way of long speeches and is always slightly ashamed, afterwards, of how much of himself he has had to admit. He believes he is reasonable. He is also a man who once paid a hundred lire to a girl who turned out to be his stepdaughter, and he cannot live the rest of his life inside that single hour.",
        "to_play": "He must believe, in real time, every paradox he speaks. He is not a lecturer. He is a man fighting to be allowed to exist with all of himself, not just the worst hour of his life. Mellifluous when he controls the rhythm of his argument; violent the moment that rhythm breaks.",
    },
    {
        "num": "ii", "name": "The Mother", "tag": "silence that finally screams",
        "appearance": "A woman in modest black, with a heavy widow's veil of crêpe that hides her face. Beneath it, when she lifts it, a face the colour of wax. She does not meet anyone's eyes. She looks like a person who has agreed, somewhere a long time ago, to be diminished.",
        "nature": "Crushed and terrified, as though pressed down by a weight too great to name. She is silent for most of Act One; her drama is what others do to her. Then, in Act Two, her presence becomes a sound — the only true unmediated cry in the play. She is not, the Father insists, a woman. She is a mother. The whole tragedy is contained in that flattening.",
        "to_play": "Stillness is her language. She listens. She suffers. She lifts the veil only when forced. Her line in Act Two — It is taking place now. It happens all the time — should land like a stone learning to speak. Resist the temptation to make her sympathetic in the easy way. She is heavier than that.",
    },
    {
        "num": "iii", "name": "The Step-Daughter", "tag": "speed and shame turned outward",
        "appearance": "Dashing, almost impudent, beautiful. In mourning, but with great elegance — black worn with style. She holds herself the way someone holds themselves who has decided not to be ashamed in public any longer.",
        "nature": "Speed, shame turned outward, revenge wearing the dress of truth. The spine of Act Two and the engine of the family's exposure. She speaks faster than the others; she refuses every softening; she enjoys the wound. Her tenderness is reserved entirely for the Child. Her contempt is reserved entirely for the Boy and the Son. The Father she neither pities nor forgives.",
        "to_play": "Never apologetic. The performance is propulsion. Sex, scorn, and grief crossing the same face inside a few seconds. Her tenderness toward the Child must be unbearably real — so that her contempt for the Boy reads as the same wound, pointed in the opposite direction.",
    },
    {
        "num": "iv", "name": "The Son", "tag": "the one who will not act",
        "appearance": "Twenty-two. Tall. Severe in his attitude of contempt for the Father. Supercilious and indifferent to the Mother. He stands at the edge of his own family as if he had walked onto the stage against his will — which, in fact, he did.",
        "nature": "The refuser. An unrealised character, he calls himself — meaning he was never given dramatic life by his author and refuses to ask for it now. And yet he is on the stage, indissolubly bound to the chain. The bond is the same one that holds anyone in a family they did not choose: refusal, contempt, and the impossibility of leaving.",
        "to_play": "Quiet, cold, with the energy of someone who would leave if he could. Every line is a door closing. His speech in Act Three about the mirror that throws his likeness back as a horrible grimace is the only moment he allows himself a real cry. Make it count.",
    },
    {
        "num": "v", "name": "The Boy", "tag": "silent — appears only in projection",
        "appearance": "Fourteen years old, dressed in black. Wretched, half-frightened, mostly silent. He clings to his Mother. He carries a revolver in his pocket without speaking of it.",
        "nature": "The doomed witness. He sees his little sister drown in the fountain and cannot move. Then, behind the trees, he shoots himself. The audience never sees the suicide; only the sound reaches them.",
        "to_play": "Pre-recorded footage on the rear screen. A face that says nothing and registers everything. The boy on film should never seem to be performing for an audience. He should seem to be inside a room that is slowly closing on him. Use long held shots; trust stillness.",
    },
    {
        "num": "vi", "name": "The Child", "tag": "silent — appears only in projection",
        "appearance": "About four years old. Dressed in white, with a black silk sash at the waist. Held, lifted, kissed, led by the hand. Easily the most fragile body in the play.",
        "nature": "The first to vanish. The Step-Daughter speaks to her about a garden that will not be real, a fountain that will only be painted cardboard. In Act Three she drowns in the fountain. Her death is the death the play refuses to show.",
        "to_play": "Pre-recorded footage on the rear screen. The film must never look performed. The more ordinary the child looks — playing, laughing, looking up — the more devastating her drowning becomes when it is described, much later, by the Son who could not save her.",
    },
    {
        "num": "vii", "name": "Madame Pace", "tag": "an apparition of the stage",
        "appearance": "A fat, older woman with puffy bleach-blonde hair. Rouged and powdered. Dressed with a comical elegance in black silk. A long silver chain at her waist, ending in a pair of scissors.",
        "nature": "An apparition. Not one of the original six Characters — she is summoned into being by the very arrangement of the stage: by hats on pegs, by a shop window, by a screen. She runs the atelier where the Step-Daughter was offered to the Father for a hundred lire. She speaks half in Italian and half in English, ridiculous and grotesque. She is at once a comic stage trick and the obscene heart of the family's wound.",
        "to_play": "She must arrive like a wrong note that proves the key was never stable. Play the comedy of her dialect at full strength. Play the obscenity beneath the comedy at full strength too. The audience laughs, and is then disgusted with itself for having laughed — that double sensation is the point of her.",
    },
    {
        "num": "viii", "name": "The Manager", "tag": "the director on a deadline",
        "appearance": "Pirandello does not give him a body, and the omission is itself a kind of direction. He should look like whatever the audience expects an exhausted, competent theatre director to look like — a man at the end of a difficult week, the schedule burning, faintly contemptuous of the playwright he has been forced to stage, faintly proud of his company.",
        "nature": "Pragmatic, cynical, slightly ridiculous, slightly brave. The play's director-figure. He treats the play in front of him as a job — until the job turns into something he does not have a name for. Then he tries to make a play out of it anyway, because that is what one does when six strangers walk into a rehearsal claiming there is a drama inside them.",
        "to_play": "He is wrong in tone almost constantly, and right in instinct almost as often. Do not play him as a fool. Give him compassion. He is everyone in the audience who has ever been forced to make sense of someone else's grief on a deadline.",
    },
]

def render_portrait(p):
    return f'''
    <div class="portrait">
      <div class="p-num">{p["num"]}.</div>
      <h3 class="p-name">{p["name"]}</h3>
      <span class="p-tag">{p["tag"]}</span>

      <div class="p-block">
        <h4>Appearance</h4>
        <p>{p["appearance"]}</p>
      </div>

      <div class="p-block">
        <h4>Nature</h4>
        <p>{p["nature"]}</p>
      </div>

      <div class="p-block">
        <h4>To Play</h4>
        <p>{p["to_play"]}</p>
      </div>
    </div>
'''

portraits_html = "\n".join(render_portrait(p) for p in PORTRAITS)

PORTRAITS_SECTION = f'''
  <section class="portraits">
    <h2 class="portraits-h2">Portraits</h2>
    <p class="portraits-sub">the bodies, the natures, and the playing of them</p>
    <p class="portraits-intro">What follows is the director's gallery of the people who will walk into Act One — a body for each, a nature for each, and a note to the company on how to play them. Pirandello supplied the bodies; the readings beside them are the work of K. J., and are offered as starting points, not as commands.</p>
{portraits_html}
  </section>
'''

# ---------------------------------------------------------------------------
# Insert between the cast list and the scene-setting div
# ---------------------------------------------------------------------------
# Anchor: closing </section> of cast list immediately before <div class="scene-setting">
html = html.replace(
    '</section>\n\n  <div class="scene-setting">',
    '</section>\n' + PORTRAITS_SECTION + '\n  <div class="scene-setting">',
    1
)

SRC.write_text(html)
print(f"Wrote {SRC}: {len(html):,} bytes  ({html.count(chr(10)):,} lines)")
