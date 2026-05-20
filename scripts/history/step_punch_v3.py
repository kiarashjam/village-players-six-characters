#!/usr/bin/env python3
"""Fix the 9 anchors that missed: non-nested speaker spans, ASCII quotes,
<em> wrappers around foreign text."""
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

# #26 — sibling spans, not nested
replace_once(
    """<p class="speech"><span class="speaker">The Step-Daughter</span> <span class="action">[vivaciously]</span>. So much the better, so much the better! We can be your new piece.</p>""",
    """<p class="speech"><span class="speaker">The Step-Daughter</span> <span class="action">[vivaciously]</span>. So much the better, sir, so much the better. You can put us on tonight — we shall draw better than whatever you were rehearsing.</p>""",
    "#26 swagger"
)

# #66 — sibling spans, plus <strong>Father</strong> in stage direction
replace_once(
    """<p class="speech"><span class="speaker">The Step-Daughter</span> <span class="action">[disdainful, alluring, treacherous, full of impudence]</span>. My passion, sir! Ah, if you only knew! My passion for him! <span class="action">[Points to the <strong>Father</strong> and makes a pretence of embracing him. Then she breaks out into a loud laugh.]</span></p>""",
    """<p class="speech"><span class="speaker">The Step-Daughter</span> <span class="action">[disdainful, alluring, treacherous, full of impudence]</span>. My passion, sir! Ah, if you only knew — my passion for <em>him</em>. <span class="action">[Points to the <strong>Father</strong> and pretends to throw her arms around him, then bursts into a coarse, carrying laugh.]</span></p>""",
    "#66 passion"
)

# #112 — has <em>robes et manteaux</em>
replace_once(
    """You know Madame Pace — one of those ladies who attract poor girls of good family into their ateliers, under the pretext of their selling <em>robes et manteaux</em>.""",
    """You know Madame Pace, sir — one of those <em>ladies</em> who lure poor girls of good family into their ateliers, on the pretext of selling <em>robes et manteaux</em>. The pretext is always <em>robes</em>.""",
    "#112 pretext"
)

# #182 — uses ASCII quotes "..."
replace_once(
    """Absurd! How can I possibly be expected — after that — to be a modest young miss, a fit person to go with his confounded aspirations for "a solid moral sanity"?""",
    """Absurd! How can I possibly be expected — after <em>that</em> — to play the modest young miss, fit company for his confounded aspirations of "a solid moral sanity"?""",
    "#182 modest miss"
)

# #189 — long speech, ASCII quotes around "vile"
replace_once(
    """<p class="speech"><span class="speaker">The Step-Daughter</span>. You! you! I owe my life on the streets to you. Did you or did you not deny us, with your behaviour, I won't say the intimacy of home, but even that mere hospitality which makes guests feel at their ease? We were intruders who had come to disturb the kingdom of your legitimacy. I should like to have you witness, Mr. Manager, certain scenes between him and me. He says I have tyrannized over everyone. But it was just his behaviour which made me insist on the reason for which I had come into the house, — this reason he calls "vile" — into his house, with my mother who is his mother too. And I came as mistress of the house.</p>""",
    """<p class="speech"><span class="speaker">The Step-Daughter</span>. You — <em>you</em>! I owe my life on the streets to you. Did you, or did you not, deny us — I won't say the warmth of home, but even the bare hospitality that makes a guest feel at ease? We were intruders, come to disturb the kingdom of your <em>legitimacy</em>. I should like to have you witness, Mr. Manager, certain scenes between him and me. He says I have tyrannised over everyone. But it was <em>his</em> behaviour that made me insist — on the reason for which I had come into the house, this reason he calls "vile," with my mother who is his mother too. <em>And I came as mistress of the house.</em></p>""",
    "#189 mistress"
)

# #381 — ASCII quotes
replace_once(
    """Nonsense! Introduce this "old signore" who wants to talk nicely to me.""",
    """Nonsense! Bring on this <em>old signore</em> who wants to talk so nicely to me.""",
    "#381 bring him on"
)

# #456 — ASCII quotes
replace_once(
    """Not at all! See here: when I told him that it was useless for me to be thinking about my wearing mourning, do you know how he answered me? "Ah well," he said, "then let's take off this little frock.\"""",
    """Not at all! See here, sir — when I told him it was useless for me to think about wearing mourning, do you know what he said? "Ah well," he said, "then let's take this little frock off." """,
    "#456 take this frock off"
)

# #468 — ASCII quotes
replace_once(
    """I won't stop here! I won't! I can see you've fixed it all up with him in your office. All this talk about what is possible for the stage… I understand! He wants to get at his complicated "cerebral drama," to have his famous remorses and torments acted; but I want to act my part, my part!""",
    """I won't stay here. I will not! I can see you've fixed it all up with him in your office. All this talk about what is <em>possible</em> on the stage — I understand! He wants his complicated "cerebral drama," his famous remorses and torments performed in good taste. But I want to act my part. <em>My</em> part.""",
    "#468 cerebral drama"
)

# #474 — ASCII quotes
replace_once(
    """How? How can he act all his "noble remorses," all his "moral torments," if you want to spare him the horror of being discovered one day — after he had asked her what he did ask her — in the arms of her, that already fallen woman, that child, sir, that child he used to watch come out of school?""",
    """How? How can he act all his "noble remorses," all his "moral torments," if you want to spare him the horror of being discovered one day — after he had asked her what he asked her — in the arms of her, that already fallen woman, that <em>child</em>, sir — the child he used to watch come out of school?""",
    "#474 that child sir"
)

SRC.write_text(html)
print(f"File: {SRC} ({len(html):,} bytes)")
print()
print(f"Changes applied: {len(changes)}")
for i, c in enumerate(changes, 1):
    print(f"  {i:2}. {c}")
