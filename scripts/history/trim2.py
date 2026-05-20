#!/usr/bin/env python3
"""Rebuild shorter director's-cut suggestions, now including the stage
directions [in brackets] that the originals carry: addressee tags ([To Mother.]),
indications ([Indicating the Son.]), physical actions ([Seizes Boy's arm.]),
manner tags ([with a cry], [dominating the protests]). Style them as upright
inside the italic shorter line so they stand out clearly."""
import re
from pathlib import Path
from html import unescape

SRC = Path("/home/claude/six_characters.html")
h = SRC.read_text()

# ---------------------------------------------------------------------------
# 1. STRIP all existing speech-shorter paragraphs (we will reinsert below)
# ---------------------------------------------------------------------------
removed = len(re.findall(r'<p class="speech-shorter">', h))
h = re.sub(
    r'\n  <p class="speech-shorter">.*?</p>',
    '',
    h,
    flags=re.DOTALL,
)
print(f"Stripped {removed} existing speech-shorter paragraphs.")

# ---------------------------------------------------------------------------
# 2. CSS — ensure stage directions render upright inside italic shorter line
# ---------------------------------------------------------------------------
# Only add if not already present (re-runnable)
EXTRA_CSS = "\n.speech-shorter .action { font-style: normal; opacity: 0.85; }\n"
if ".speech-shorter .action" not in h:
    h = h.replace("</style>", EXTRA_CSS + "</style>", 1)

# ---------------------------------------------------------------------------
# 3. NEW SHORTER MAP — same shortened content, now with proper stage directions
# ---------------------------------------------------------------------------
SHORTER = {
53: """<span class="ss-speaker">The Father.</span> Yes, that is the word! <span class="action">[To Manager.]</span> The author who created us alive no longer wished, or was no longer able, to put us into a work of art. That was a real crime, sir. He who is born a character can laugh even at death. The writer dies; the creation does not — and it needs no extraordinary gift to live forever. Who was Sancho Panza? Who was Don Abbondio? They live eternally, because they found a fantasy that could nourish them. We had no such fortune.""",

72: """<span class="ss-speaker">The Step-Daughter <span class="action">[to Manager]</span>.</span> Worse? Listen! Stage this drama now! At a certain moment, when God takes this little darling from her mother, and this imbecile here <span class="action">[Seizing the Boy.]</span> does the stupidest things, like the fool he is — you will see me run away. Yes, gentlemen, I shall be off. But the moment hasn't come yet. After what has taken place between him and me <span class="action">[Indicating the Father with a horrible wink.]</span> I cannot remain — watching her anguish for that fool <span class="action">[Indicates the Son.]</span>. Look at him! Frigid, indifferent, because he is the legitimate son. He despises me, the Boy, this baby — because we are bastards. <span class="action">[Goes to the Mother and embraces her.]</span> And he doesn't want to recognise her as his mother — she who is the common mother of us all. Wretch!""",

120: """<span class="ss-speaker">The Father.</span> But don't you see that the whole trouble lies here. In words, words. Each one of us has within him a whole world of things, his own special world. And how can we ever understand each other, if I give my words the sense I have in me, while you who listen must translate them according to the conception of things you have within yourself? We think we understand. We never really do.""",

143: """<span class="ss-speaker">The Father <span class="action">[quickly]</span>.</span> Is it my fault if he has grown up like this? I sent him to a wet nurse in the country, a peasant, as his mother did not seem strong enough. That, sir, was the reason I married her. Unpleasant — but how can it be helped? All my life I have had these confounded aspirations toward a moral sanity I never quite reach.""",

150: """<span class="ss-speaker">The Father.</span> Yes, I admit it. It was also a liberation for me. But great evil has come of it. I meant well, sir; and I did it more for her sake than mine — I swear it. <span class="action">[Crosses his arms; then turns to the Mother.]</span> Did I ever lose sight of you until that other man carried you off to another town? Out of pure interest in you, that had no base motive in it, I watched with the tenderest concern the new family that grew up around her. <span class="action">[Points to the Step-Daughter.]</span>""",

154: """<span class="ss-speaker">The Father.</span> Infamous! infamous! After she <span class="action">[Indicating the Mother.]</span> went away, my house seemed suddenly empty. She had been my incubus, but she filled my house. I was like a dazed fly alone in the empty rooms. This boy here <span class="action">[Indicating the Son.]</span> was educated away from home; when he came back, he seemed to me to be no more mine. With no mother between him and me, he grew up apart, on his own, with no tie of intellect or affection. And then — strange but true — I was driven, by curiosity at first and then by some tender sentiment, toward her family, which had come into being through my will. The thought of her began gradually to fill the emptiness I felt all around me.""",

155: """<span class="ss-speaker">The Step-Daughter.</span> Yes, yes. True. He used to follow me in the street and smile at me, wave his hand like this. I looked at him, doubtful, wondering who he might be. I told my mother, who guessed at once. <span class="action">[The Mother agrees with a nod.]</span> Then she wouldn't send me to school for some days. When I went back, there he was again — looking so ridiculous — with a paper parcel: a fine straw hat, a bouquet of flowers, all for me.""",

168: """<span class="ss-speaker">The Father.</span> Was it my fault if that fellow carried you away? After he had found some job, I could find no trace of them, and naturally my interest dwindled. But the drama culminated, unforeseen and violent, on their return — when I was impelled by my miserable flesh that still lives. Ah, what wretchedness is that of the man who is alone and disdains debasing liaisons! Not old enough to do without women, not young enough to seek one without shame. It is worse than misery; it is a horror. Every man knows what unconfessable things pass in the secrecy of his own heart. One gives way to temptation, and rises again with a great eagerness to re-establish one's dignity, as a tombstone on the grave of one's shame. Some folks haven't the courage to say certain things, that's all.""",

170: """<span class="ss-speaker">The Father.</span> Yes, but in secret. Therefore, you want more courage to say these things. Let a man only speak them out, and folks at once label him a cynic. But it isn't true. He is like all the others — better indeed, because he isn't afraid to reveal with the light of intelligence the red shame of human bestiality which most men close their eyes upon. Woman — look at her case. She turns inviting glances on you. You seize her. No sooner does she feel herself in your grasp than she closes her eyes. It is the sign of her mission, by which she says: "Blind yourself, for I am blind.\"""",

171: """<span class="ss-speaker">The Step-Daughter.</span> Sometimes she can close them no more — when she no longer feels the need of hiding her shame from herself, but dry-eyed and dispassionately sees only that of the man who has blinded himself without love. Oh, all this philosophy that uncovers the beast in man and then seeks to excuse him — I can't stand it, sir. When a man simplifies life bestially, throwing aside every chaste aspiration, every sense of duty, modesty, shame — then nothing is more revolting than the remorse that follows. Crocodile's tears, that's what it is.""",

183: """<span class="ss-speaker">The Father.</span> For the drama lies all in this — in the conscience that I have, that each one of us has. We believe this conscience to be a single thing; but it is many-sided. So we have the illusion of being one person for all, of having a personality that is unique in all our acts. But it isn't true. We perceive this when, tragically perhaps, in something we do, we are caught up, suspended on a kind of hook. Then we see that all of us was not in that act, and that it would be an atrocious injustice to judge us by that action alone, as if all our existence were summed up in that one deed. Now do you understand the perfidy of this girl? She surprised me in a place where she ought not to have known me — and now seeks to attach to me a reality I could never have supposed I would have to assume, in a shameful and fleeting moment of my life.""",

189: """<span class="ss-speaker">The Step-Daughter.</span> You! you! I owe my life on the streets to you. Did you or did you not deny us — I won't say the intimacy of home, but even that mere hospitality which makes guests feel at ease? We were intruders, come to disturb the kingdom of your legitimacy. I should like to have you witness, Mr. Manager, certain scenes between him and me. He says I have tyrannised over everyone. But it was just his behaviour that made me insist on the reason for which I had come into the house — with my mother, who is his mother too.""",

190: """<span class="ss-speaker">The Son.</span> It's easy for them to put me always in the wrong. But imagine, gentlemen, the position of a son who sees arrive one day at his home a young woman of impudent bearing, asking for his father — with whom, who knows what business she has. Then she returns, bolder, with that child there. He has to watch her treat his father in an equivocal and confidential manner. She asks him for money — in a way that lets one suppose he must give it. Must. Because he has every obligation.""",

192: """<span class="ss-speaker">The Son.</span> How should I know? When had I ever seen or heard of her? One day there arrive with her <span class="action">[Indicating Step-Daughter.]</span> that lad and this baby here. I am told: "This is your mother too, you know." I divine from her manner why they have come home. I had rather not say what I feel about it. I shouldn't even care to confess it to myself. No action can therefore be hoped for from me in this affair. Believe me, sir — I am an "unrealised" character. Leave me out of it, I beg you.""",

197: """<span class="ss-speaker">The Father <span class="action">[indicating Step-Daughter]</span>.</span> She can't stand him, you know. <span class="action">[Then referring again to the Son.]</span> He says he doesn't come into the affair, whereas he is really the hinge of the whole action. Look at that lad who is always clinging to his mother, frightened and humiliated. It is on account of this fellow here. Possibly his situation is the most painful of all. He feels himself more a stranger than the others — mortified at being brought into a home out of charity, as it were. <span class="action">[In confidence.]</span> The image of his father. Hardly talks at all.""",

199: """<span class="ss-speaker">The Father.</span> He disappears soon, you know. And the baby too. She is the first to vanish from the scene. The drama consists finally in this: when that mother re-enters my house, her family — born outside of it and superimposed on the original — ends with the death of the little girl, the tragedy of the boy, and the flight of the elder daughter. It cannot go on, because it is foreign to its surroundings. So we three remain — I, the mother, that son — and find ourselves strange to one another. We live in an atmosphere of mortal desolation, which is the revenge, as he <span class="action">[Indicating the Son.]</span> scornfully said, of the Demon of Experiment that unfortunately hides in me. When faith is lacking, it becomes impossible to create certain states of happiness.""",

243: """<span class="ss-speaker">The Step-Daughter <span class="action">[bends over the Child and takes her face between her hands]</span>.</span> My little darling! You're frightened, aren't you? You don't know where we are. <span class="action">[Pretending to reply to a question of the Child.]</span> What is the stage? It's a place, baby, where people play at being serious — and we've got to act a comedy now, dead serious. You're in it too. A garden — a fountain — look — just suppose, kiddie, it's here, right in the middle. It's all pretence, my pet. All make-believe here. Better to imagine it, because if they fix it up for you, it'll only be painted cardboard — for the rockery, the water, the plants. Ah, but I think a baby like this would sooner have a make-believe fountain than a real one. What a joke it'll be for the others! But for you, alas, not such a joke. You who are real, baby dear, and really play by a real fountain, big and green and beautiful, with bamboos around and a whole lot of little ducks swimming. — <span class="action">[Seizes the Boy by the arm.]</span> What have you got there? <span class="action">[Catches the glint of a revolver.]</span> Ah! Where did you get this? Idiot! If I'd been in your place, instead of killing myself I'd have shot one of those two — or both. Father and son.""",

249: """<span class="ss-speaker">The Son <span class="action">[half to himself, meaning the Mother to hear]</span>.</span> And they want to put it on the stage! If there was at least a reason for it! He thinks he has got at the meaning of it all. Just as if each one of us in every circumstance of life couldn't find his own explanation of it! <span class="action">[Pauses.]</span> He complains he was discovered in a place where he ought not to have been seen, in a moment of his life that should have stayed hidden. And what about my case? Haven't I had to reveal what no son ought ever to reveal — how father and mother live and are man and wife for themselves, quite apart from that idea of father and mother which we give them?""",

350: """<span class="ss-speaker">The Father <span class="action">[dominating the protests]</span>.</span> Excuse me, all of you! Why are you so anxious to destroy, in the name of a vulgar, commonplace sense of truth, this reality which comes to birth, attracted and formed by the magic of the stage itself — which has indeed more right to live here than you, since it is much truer than you, if you don't mind my saying so? Which is the actress among you who is to play Madame Pace? Well, here is Madame Pace herself. You'll allow, I fancy, that the actress who acts her will be less true than this woman, who is herself in person.""",

462: """<span class="ss-speaker">The Step-Daughter.</span> No, sir! What you want to do is to piece together a little romantic sentimental scene out of my disgust — out of all the reasons, each more cruel and viler than the last, why I am what I am. He's to ask me why I'm in mourning; and I'm to answer, with tears in my eyes, that it is just two months since papa died. No, sir! He's got to say to me, as he did say: "Well, let's take off this little dress at once.\"""",

469: """<span class="ss-speaker">The Manager <span class="action">[annoyed, shaking his shoulders]</span>.</span> Ah! Just your part! But, if you will pardon me, there are other parts than yours — his <span class="action">[Indicating the Father.]</span> and hers <span class="action">[Indicating the Mother.]</span>. On the stage you can't have a character becoming too prominent and overshadowing all the others. The thing is to pack them all into a neat little framework, and then act what is actable. I am aware that everyone has his own interior life he wants to put forward. But the difficulty lies in this: to set out just so much as is necessary for the stage, taking the other characters into consideration, and at the same time hint at the unrevealed interior life of each. From your point of view, it would be a fine idea if each character could tell the public all his troubles in a nice monologue. <span class="action">[Good humoredly.]</span> You must restrain yourself, my dear — in your own interest, too — because this fury of yours, this exaggerated disgust, may make a bad impression.""",

482: """<span class="ss-speaker">The Mother.</span> It's taking place now. It happens all the time. My torment isn't a pretended one. I live and feel every minute of my torture. Those two children there — have you heard them speak? They can't speak any more. They cling to me to keep my torment actual and vivid. But for themselves, they do not exist. They aren't any more. And she <span class="action">[Indicating the Step-Daughter.]</span> has run away, she has left me, and is lost.""",

486: """<span class="ss-speaker">The Step-Daughter.</span> I can hear it still in my ears. It's driven me mad, that cry. You can put me on as you like — fully dressed, if you like — provided I have at least the arm bare. Because, standing like this <span class="action">[She goes close to the Father and leans her head on his breast.]</span> with my head so, and my arms round his neck, I saw a vein pulsing in my arm here; and then, as if that live vein had awakened disgust in me, I closed my eyes like this, and let my head sink on his breast. <span class="action">[Turning to the Mother.]</span> Cry out, mother! Cry out as you did then!""",

531: """<span class="ss-speaker">The Father.</span> But only in order to know if you, as you really are now, see yourself as you once were — with all the illusions that were yours then, with all the things both inside and outside of you as they seemed to you, as they were for you. Well, sir, if you think of all those illusions that mean nothing to you now, of all those things which don't even seem to you to exist any more, while once they were for you — don't you feel that the very earth under your feet is sinking, when you reflect that this you of today is fated to seem a mere illusion to you tomorrow?""",

541: """<span class="ss-speaker">The Father <span class="action">[with a cry]</span>.</span> No, sir, not ours! Look here! That is the very difference! Our reality doesn't change: it can't change! It can't be other than what it is, because it is already fixed forever. It's terrible. Ours is an immutable reality — which should make you shudder when you approach us, if you are really conscious that your reality is a mere transitory and fleeting illusion, taking this form today and that tomorrow, according to your will. Illusions of reality, represented in this fatuous comedy of life that never ends, nor can ever end.""",

544: """<span class="ss-speaker">The Manager.</span> Nonsense! Cut that out, please! None of us believes it, because it isn't a thing one can believe seriously. If you want to know, it seems to me you are trying to imitate the manner of a certain author whom I heartily detest — I warn you — although I have unfortunately bound myself to put on one of his works. As a matter of fact, I was just starting to rehearse it when you arrived. <span class="action">[Turning to the Actors.]</span> And this is what we've gained — out of the frying-pan into the fire!""",

545: """<span class="ss-speaker">The Father.</span> I don't know to what author you may be alluding, but believe me, I feel what I think; and I seem to be philosophising only for those who do not think what they feel, because they blind themselves with their own sentiment. I know that for many, this self-blinding seems much more "human"; but the contrary is true. For man never reasons so much, and becomes so introspective, as when he suffers — since he is anxious to get at the cause of his sufferings, to learn who has produced them, and whether it is just that he should have to bear them. The animals suffer without reasoning. But take a man who suffers and begins to reason about it — oh no, it can't be allowed. Let him suffer like an animal, and then — ah yes, he is "human"!""",

549: """<span class="ss-speaker">The Father.</span> You have never met such a case, sir, because authors, as a rule, hide the labour of their creations. When the characters are really alive before their author, the latter does nothing but follow them in their actions, their words, the situations they suggest to him; he has to will them the way they will themselves — for there's trouble if he doesn't. When a character is born, he acquires at once such an independence, even of his own author, that everyone can imagine him in many other situations the author never dreamed of placing him in.""",

552: """<span class="ss-speaker">The Step-Daughter.</span> It's true. I too have sought to tempt him, many, many times — when he was sitting at his writing table, feeling a bit melancholy at the twilight hour. He would sit in his armchair too lazy to switch on the light, and all the shadows that crept into his room were full of our presence, coming to tempt him. <span class="action">[As if she saw herself still there.]</span> Oh, if you would only go away, go away and leave us alone — mother here with that son of hers, I with that Child, that Boy there always alone, and then I with him <span class="action">[Hinting at the Father.]</span> — and then I alone, alone, in those shadows. <span class="action">[A sudden movement, as if she would seize herself in the vision.]</span> Ah! my life! my life! Oh, what scenes we proposed to him — and I tempted him more than any of the others!""",

561: """<span class="ss-speaker">The Father.</span> Well, if you want to take away from me the possibility of representing the torment of my spirit, which never gives me peace, you will be suppressing me — that's all. Every true man, sir, who is a little above the level of the beasts and plants, does not live for the sake of living, without knowing how to live; but lives so as to give a meaning and a value of his own to life. For me, this is everything. I cannot give it up just to represent a mere fact, as she <span class="action">[Indicating the Step-Daughter.]</span> wants. It's all very well for her — but I'm not going to do it. It destroys my raison d'être.""",

571: """<span class="ss-speaker">The Step-Daughter.</span> Yes, in the sun, in the sun! That is my only pleasure — to see her happy and careless in the garden, after the misery and squalor of the horrible room where we all four slept together. And I had to sleep with her — I, do you understand? — with my vile contaminated body next to hers, with her folding me in her loving little arms. In the garden, whenever she spied me, she would run to take me by the hand. She loved the little flowers, and would show them to me.""",

572: """<span class="ss-speaker">The Manager.</span> Well then, we'll have it in the garden. Everything shall happen in the garden — we'll group the other scenes there. <span class="action">[Calls a Stage Hand.]</span> A backcloth with trees, and something to do as a fountain basin. Good — you've fixed it up. <span class="action">[To Step-Daughter.]</span> This is just to give an idea, of course. The Boy, instead of hiding behind the doors, will wander about here in the garden, hiding behind the trees. It's going to be rather difficult to find a child to do the scene with you where she shows you the flowers. <span class="action">[To the Boy.]</span> Come forward a little. Let's try it. It's a nice business, this lad. What's the matter with him? We'll have to give him a word or two to say. <span class="action">[Leads him behind one of the trees.]</span> Hide here — like that. Show your head a little, as if looking for someone.""",

581: """<span class="ss-speaker">The Step-Daughter <span class="action">[going over to the Manager]</span>.</span> Allow me? <span class="action">[Puts down the Manager's arm.]</span> Well, go away then, if you want to! <span class="action">[The Son looks at her with contempt and hatred. She laughs.]</span> You see, he can't, he can't go away! He is obliged to stay here, indissolubly bound to the chain. If I, who fly off when that happens which has to happen, because I can't bear him — if I am still here and support that face of his, you can well imagine he is unable to move. He has to remain, with that nice father of his, and that mother whose only son he is. <span class="action">[To the Mother.]</span> Come on, mother, come along! <span class="action">[To Manager.]</span> You see, she was getting up to keep him back. You can imagine how little she wants to show your actors what she really feels — but so eager is she to get near him that... There, you see? She is willing to act her part.""",
}

# ---------------------------------------------------------------------------
# 4. Apply: append a new shorter paragraph after each long original
# ---------------------------------------------------------------------------
pattern = re.compile(r'<p class="speech">.*?</p>', re.DOTALL)
matches = list(pattern.finditer(h))

def wc(text):
    txt = re.sub(r'<[^>]+>', ' ', text)
    return len(unescape(txt).split())

to_apply = []
matched_indices = set()
for i, m in enumerate(matches):
    if wc(m.group(0)) > 100 and i in SHORTER:
        original = m.group(0)
        shorter_html = (
            '\n  <p class="speech-shorter">'
            '<span class="ss-label">Shorter</span>'
            f'{SHORTER[i].strip()}'
            '</p>'
        )
        to_apply.append((original, original + shorter_html))
        matched_indices.add(i)

for original, new in to_apply:
    if original in h:
        h = h.replace(original, new, 1)

SRC.write_text(h)

# Report
applied = sorted(matched_indices)
all_long = [i for i, m in enumerate(matches) if wc(m.group(0)) > 100]
skipped = [i for i in all_long if i not in matched_indices]
print(f"File: {SRC} ({len(h):,} bytes, {h.count(chr(10)):,} lines)")
print(f"Shorter versions reinserted (with stage directions): {len(applied)}")
print(f"Intentionally skipped: {skipped}")
