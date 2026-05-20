#!/usr/bin/env python3
"""Push Step-Daughter register: vulgar, arrogant, sexually charged. Preserves
her grief and her tenderness with the Child."""
from pathlib import Path

SRC = Path("/home/claude/six_characters.html")
html = SRC.read_text()
changes = []

def replace_once(old, new, label):
    global html
    if old not in html:
        print(f"!! ANCHOR NOT FOUND: {label}")
        return False
    html = html.replace(old, new, 1)
    changes.append(label)
    return True

# PORTRAIT
replace_once(
    """Speed, shame turned outward, revenge wearing the dress of truth. The spine of Act Two and the engine of the family's exposure. She speaks faster than the others; she refuses every softening; she enjoys the wound. Her tenderness is reserved entirely for the Child. Her contempt is reserved entirely for the Boy and the Son. The Father she neither pities nor forgives.""",
    """Speed, shame turned outward, revenge wearing the dress of truth. The spine of Act Two and the engine of the family's exposure. She speaks faster than the others; she refuses every softening; she enjoys the wound. Her body is part of the argument — she knows men look at her, and she uses the knowing. Her tenderness is reserved entirely for the Child. Her contempt for the Boy and the Son is total. The Father she neither pities nor forgives; she has not finished punishing him.""",
    "Portrait: Nature"
)

replace_once(
    """Never apologetic. The performance is propulsion. Sex, scorn, and grief crossing the same face inside a few seconds. Her tenderness toward the Child must be unbearably real — so that her contempt for the Boy reads as the same wound, pointed in the opposite direction.""",
    """Never apologetic. The performance is propulsion. Sex, scorn, and grief crossing the same face inside a few seconds. Vulgar where vulgarity is the truth, arrogant where arrogance is armour. Sex is her oldest weapon and her oldest wound — she does not pretend either. Her tenderness toward the Child must be unbearably real — so that her contempt for the Boy reads as the same wound, pointed in the opposite direction.""",
    "Portrait: To Play"
)

# SPEECH ORIGINALS
replace_once(
    """<p class="speech"><span class="speaker">The Step-Daughter <span class="action">[vivaciously]</span></span>. So much the better, so much the better! We can be your new piece.</p>""",
    """<p class="speech"><span class="speaker">The Step-Daughter <span class="action">[vivaciously]</span></span>. So much the better, sir, so much the better. You can put us on tonight — we shall draw better than whatever you were rehearsing.</p>""",
    "#26 swagger"
)

replace_once(
    """<p class="speech"><span class="speaker">The Step-Daughter</span>. We may be your fortune.</p>""",
    """<p class="speech"><span class="speaker">The Step-Daughter</span>. We may be your fortune, sir — if you have the nerve for us.</p>""",
    "#31 dare"
)

replace_once(
    """<p class="speech"><span class="speaker">The Step-Daughter <span class="action">[disdainful, alluring, treacherous, full of impudence]</span></span>. My passion, sir! Ah, if you only knew! My passion for him! <span class="action">[Points to the Father and makes a pretence of embracing him. Then she breaks out into a loud laugh.]</span></p>""",
    """<p class="speech"><span class="speaker">The Step-Daughter <span class="action">[disdainful, alluring, treacherous, full of impudence]</span></span>. My passion, sir! Ah, if you only knew — my passion for <em>him</em>. <span class="action">[Points to the Father and pretends to throw her arms around him, then bursts into a coarse, carrying laugh.]</span></p>""",
    "#66 passion"
)

replace_once(
    """I, who am a two months' orphan, will show you how I can dance and sing.""",
    """I, who am a two months' orphan, will show you how well I can dance and sing. <em>Don't worry — it isn't a hymn.</em>""",
    "#68 not a hymn"
)

replace_once(
    """<p class="speech"><span class="speaker">The Step-Daughter</span>. Fortunately for her, he is dead. Two months ago as I said. We are in mourning, as you see.</p>""",
    """<p class="speech"><span class="speaker">The Step-Daughter</span>. Fortunately for her, sir, he is dead. Two months ago, as I said. We are in mourning, as you see. Most respectable.</p>""",
    "#86 most respectable"
)

replace_once(
    """Yes, there was a bit of money too. Yes, yes, a bit of money. There were the hundred lire he was about to offer me in payment, gentlemen""",
    """Yes, there was a bit of money. A nice little bit. The hundred lire he was about to lay down for me, gentlemen — for what I was selling that afternoon""",
    "#110 what I was selling"
)

replace_once(
    """You know Madame Pace — one of those ladies who attract poor girls of good family into their ateliers, under the pretext of their selling robes et manteaux.""",
    """You know Madame Pace, sir — one of those <em>ladies</em> who lure poor girls of good family into their ateliers, on the pretext of selling <em>robes et manteaux</em>. The pretext is always <em>robes</em>.""",
    "#112 pretext"
)

replace_once(
    """Shame indeed! This is my revenge! I am dying to live that scene… The room… I see it… Here is the window with the mantles exposed, there the divan, the looking-glass, a screen, there in front of the window the little mahogany table with the blue envelope containing one hundred lire. I see it. I see it. I could take hold of it… But you, gentlemen, you ought to turn your backs now: I am almost nude, you know. But I don't blush: I leave that to him.""",
    """Shame? Oh, the shame is mine — and the <em>revenge</em>. I am dying to live that scene. The room — I see it. Here is the window with the mantles in display, there the divan, the looking-glass, a screen, and in front of the window the little mahogany table with the blue envelope and its hundred lire. I see it. I can almost take hold of it. But you, gentlemen, ought to turn your backs now — I am almost nude in this scene. I do not blush, however. <em>He</em> does.""",
    "#116 almost nude"
)

replace_once(
    """But imagine moral sanity from him, if you please — the client of certain ateliers like that of Madame Pace!""",
    """But imagine moral sanity from <em>him</em>, if you please — a regular customer of Madame Pace's atelier. A very regular customer.""",
    "#145 very regular"
)

replace_once(
    """I used to see him waiting outside the school for me to come out. He came to see how I was growing up.""",
    """I used to see him waiting outside the school for me to come out. He came, sir, to see how I was <em>growing up</em>.""",
    "#151 growing up"
)

replace_once(
    """A real high-class modiste, you must know, gentlemen. In appearance, she works for the leaders of the best society; but she arranges matters so that these elegant ladies serve her purpose… without prejudice to other ladies who are… well… only so so.""",
    """A real high-class modiste, gentlemen. In appearance she dresses the leaders of the best society — but she arranges matters so those elegant ladies serve her purpose, and the rest of us — well, the rest of us serve hers in a different way.""",
    "#174 Madame Pace plain"
)

replace_once(
    """Absurd! How can I possibly be expected — after that — to be a modest young miss, a fit person to go with his confounded aspirations for &ldquo;a solid moral sanity&rdquo;?""",
    """Absurd! How can I possibly be expected — after <em>that</em> — to play the modest young miss, fit company for his confounded aspirations of &ldquo;a solid moral sanity&rdquo;?""",
    "#182 modest miss"
)

replace_once(
    """We are only vulgar folk! He is the fine gentleman. You may have noticed, Mr. Manager, that I fix him now and again with a look of scorn while he lowers his eyes — for he knows the evil he has done me.""",
    """We are vulgar folk, sir. <em>He</em> is the fine gentleman. You may have noticed, Mr. Manager, that I fix him now and again with a look that makes him lower his eyes — because he knows what he did to me.""",
    "#187 knows what he did"
)

replace_once(
    """<p class="speech"><span class="speaker">The Step-Daughter</span>. You! you! I owe my life on the streets to you. Did you or did you not deny us, with your behaviour, I won't say the intimacy of home, but even that mere hospitality which makes guests feel at their ease? We were intruders who had come to disturb the kingdom of your legitimacy. I should like to have you witness, Mr. Manager, certain scenes between him and me. He says I have tyrannized over everyone. But it was just his behaviour which made me insist on the reason for which I had come into the house, — this reason he calls &ldquo;vile&rdquo; — into his house, with my mother who is his mother too. And I came as mistress of the house.</p>""",
    """<p class="speech"><span class="speaker">The Step-Daughter</span>. You — <em>you</em>! I owe my life on the streets to you. Did you, or did you not, deny us — I won't say the warmth of home, but even the bare hospitality that makes a guest feel at ease? We were intruders, come to disturb the kingdom of your <em>legitimacy</em>. I should like to have you witness, Mr. Manager, certain scenes between him and me. He says I have tyrannised over everyone. But it was <em>his</em> behaviour that made me insist — on the reason for which I had come into the house, this reason he calls &ldquo;vile,&rdquo; with my mother who is his mother too. <em>And I came as mistress of the house.</em></p>""",
    "#189 mistress"
)

replace_once(
    """<p class="speech"><span class="speaker">The Step-Daughter</span>. And the screen! We must have a screen. Otherwise how can I manage?</p>""",
    """<p class="speech"><span class="speaker">The Step-Daughter</span>. And the screen! There must be a screen. Otherwise how am I to <em>manage</em>?</p>""",
    "#264 manage"
)

replace_once(
    """But I wasn't speaking of you, you know. I was speaking of myself — whom I can't see at all in you! That is all. I don't know… but… you… aren't in the least like me…""",
    """But I wasn't speaking of <em>you</em>, you know. I was speaking of myself — whom I cannot see, in the least, in <em>you</em>. I don't know quite how to put it — but no, you really aren't anything like me.""",
    "#300 Leading Lady dismissed"
)

replace_once(
    """Louder? Louder? What are you talking about? These aren't matters which can be shouted at the top of one's voice. If I have spoken them out loud, it was to shame him and have my revenge.""",
    """Louder? <em>Louder</em>? What on earth are you talking about? These aren't matters one shouts at the top of one's voice. If I spoke them loud, sir, it was to <em>shame</em> him and have my revenge.""",
    "#355 louder"
)

replace_once(
    """Nonsense! Introduce this &ldquo;old signore&rdquo; who wants to talk nicely to me.""",
    """Nonsense! Bring on this <em>old signore</em> who wants to talk so nicely to me.""",
    "#381 bring him on"
)

replace_once(
    """Not at all! See here: when I told him that it was useless for me to be thinking about my wearing mourning, do you know how he answered me? &ldquo;Ah well,&rdquo; he said, &ldquo;then let's take off this little frock.&rdquo;""",
    """Not at all! See here, sir — when I told him it was useless for me to think about wearing mourning, do you know what he said? &ldquo;Ah well,&rdquo; he said, &ldquo;then let's take this little frock off.&rdquo;""",
    "#456 take this frock off"
)

replace_once(
    """I won't stop here! I won't! I can see you've fixed it all up with him in your office. All this talk about what is possible for the stage… I understand! He wants to get at his complicated &ldquo;cerebral drama,&rdquo; to have his famous remorses and torments acted; but I want to act my part, my part!""",
    """I won't stay here. I will not! I can see you've fixed it all up with him in your office. All this talk about what is <em>possible</em> on the stage — I understand! He wants his complicated &ldquo;cerebral drama,&rdquo; his famous remorses and torments performed in good taste. But I want to act my part. <em>My</em> part.""",
    "#468 cerebral drama"
)

replace_once(
    """For one who has gone wrong, sir, he who was responsible for the first fault is responsible for all that follow. He is responsible for my faults, was, even before I was born. Look at him, and see if it isn't true!""",
    """For a woman who has gone wrong, sir, the man responsible for the first fault is responsible for everything that follows. He is responsible for <em>all</em> my faults — was responsible, before I was even born. Look at him, sir. See if it isn't true.""",
    "#472 before I was born"
)

replace_once(
    """How? How can he act all his &ldquo;noble remorses,&rdquo; all his &ldquo;moral torments,&rdquo; if you want to spare him the horror of being discovered one day — after he had asked her what he did ask her — in the arms of her, that already fallen woman, that child, sir, that child he used to watch come out of school?""",
    """How? How can he act all his <em>noble remorses</em>, all his <em>moral torments</em>, if you want to spare him the horror of being discovered one day — after he had asked her what he asked her — in the arms of her, that already fallen woman, that <em>child</em>, sir — the child he used to watch come out of school?""",
    "#474 that child sir"
)

# SHORTER VERSIONS
replace_once(
    """Worse? Listen! Stage this drama now! At a certain moment, when God takes this little darling from her mother, and this imbecile here <span class="action">[Seizing the Boy.]</span> does the stupidest things, like the fool he is — you will see me run away. Yes, gentlemen, I shall be off. But the moment hasn't come yet. After what has taken place between him and me <span class="action">[Indicating the Father with a horrible wink.]</span> I cannot remain — watching her anguish for that fool <span class="action">[Indicates the Son.]</span>. Look at him! Frigid, indifferent, because he is the legitimate son. He despises me, the Boy, this baby — because we are bastards. <span class="action">[Goes to the Mother and embraces her.]</span> And he doesn't want to recognise her as his mother — she who is the common mother of us all. Wretch!""",
    """Worse? Listen! Stage this drama now, sir! At a certain moment, when God takes this little darling from her mother, and this fool here <span class="action">[Seizing the Boy.]</span> does the stupidest things — you will see me run away. Yes, gentlemen, I shall be off. But the moment hasn't come yet. After what has taken place between him and me <span class="action">[Indicating the Father with a horrible wink.]</span>, I cannot stay here, watching her anguish over that fool <span class="action">[Indicates the Son.]</span>. Look at him — frigid, indifferent, because he is the <em>legitimate</em> son. He despises us all because we are bastards. <span class="action">[Goes to the Mother and embraces her.]</span> And he won't even recognise her as his mother. <em>Wretch.</em>""",
    "Shorter #72"
)

replace_once(
    """You! you! I owe my life on the streets to you. Did you or did you not deny us — I won't say the intimacy of home, but even that mere hospitality which makes guests feel at ease? We were intruders, come to disturb the kingdom of your legitimacy. I should like to have you witness, Mr. Manager, certain scenes between him and me. He says I have tyrannised over everyone. But it was just his behaviour that made me insist on the reason for which I had come into the house — with my mother, who is his mother too.""",
    """You — <em>you</em>! I owe my life on the streets to you. Did you, or did you not, deny us — I won't say the warmth of home, but even the bare hospitality that makes a guest feel at ease? We were intruders, come to disturb the kingdom of your <em>legitimacy</em>. I should like Mr. Manager to witness certain scenes between him and me. He says I have tyrannised. It was <em>his</em> behaviour that made me insist on the reason I had come — with my mother, who is his mother too. <em>And I came as mistress of the house.</em>""",
    "Shorter #189"
)

replace_once(
    """No, sir! What you want to do is to piece together a little romantic sentimental scene out of my disgust — out of all the reasons, each more cruel and viler than the last, why I am what I am. He's to ask me why I'm in mourning; and I'm to answer, with tears in my eyes, that it is just two months since papa died. No, sir! He's got to say to me, as he did say: "Well, let's take off this little dress at once.\"""",
    """No, sir! What you want is a little <em>romantic sentimental</em> scene pieced together out of my disgust — out of every cruel and vile reason I am what I am. He is to ask me why I wear mourning; I am to answer, with tears in my eyes, that it is just two months since papa died. No, sir, no. He has to say to me, as he did say: <em>Well, let's take this little frock off.</em>""",
    "Shorter #462"
)

replace_once(
    """I can hear it still in my ears. It's driven me mad, that cry. You can put me on as you like — fully dressed, if you like — provided I have at least the arm bare. Because, standing like this <span class="action">[She goes close to the Father and leans her head on his breast.]</span> with my head so, and my arms round his neck, I saw a vein pulsing in my arm here; and then, as if that live vein had awakened disgust in me, I closed my eyes like this, and let my head sink on his breast. <span class="action">[Turning to the Mother.]</span> Cry out, mother! Cry out as you did then!""",
    """I can hear it still in my ears. It has driven me mad, that cry. You may put me on as you like — fully dressed, if you like — provided I have at least my arm bare. Because, standing like this <span class="action">[She leans her head on the Father's breast.]</span>, with my head so and my arms round his neck, I saw a vein pulsing in my arm here; and then, as if that live vein had awakened disgust in me, I closed my eyes like this, and let my head sink against his breast. <span class="action">[Turning to the Mother.]</span> Cry out, mother. <em>Cry out as you did then!</em>""",
    "Shorter #486"
)

replace_once(
    """Allow me? <span class="action">[Puts down the Manager's arm.]</span> Well, go away then, if you want to! <span class="action">[The Son looks at her with contempt and hatred. She laughs.]</span> You see, he can't, he can't go away! He is obliged to stay here, indissolubly bound to the chain. If I, who fly off when that happens which has to happen, because I can't bear him — if I am still here and support that face of his, you can well imagine he is unable to move. He has to remain, with that nice father of his, and that mother whose only son he is.""",
    """Allow me? <span class="action">[Puts down the Manager's arm.]</span> Well, go on then — go away. <span class="action">[The Son looks at her with contempt and hatred. She laughs.]</span> You see? He <em>can't</em>. He is obliged to stay here, <em>indissolubly bound to the chain</em>. If I, who fly off when what has to happen happens, because I cannot bear him — if I am still here, supporting that face of his — you can well imagine he is unable to move. He has to remain. With that nice father of his, and that mother whose only son he is.""",
    "Shorter #581"
)

SRC.write_text(html)
print(f"File: {SRC} ({len(html):,} bytes)")
print()
print(f"Changes applied: {len(changes)}")
for i, c in enumerate(changes, 1):
    print(f"  {i:2}. {c}")
