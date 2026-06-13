#!/usr/bin/env python3
"""Build the Audition Two-Hander Pack PDF.

For every pair of speaking characters, a self-contained two-hander side
in which ONLY those two speak. Organised by character: each character's
section contains a scene with every other character, so in the audition
room you flip to whoever is reading and find all their pairings together.

Nine speaking roles: Father, Mother, Step-Daughter, Son, Manager,
Player 1, Player 2, Player 3, and Madame Pace (a Character carried by
her own performer). Each pairing is printed in both partners' sections.
Madame Pace shares scenes only with the three figures she meets in the
play — the Step-Daughter, the Father, and the Mother — so the matrix is
intentionally not complete.

The dialogue is written to carry real story weight — the secretary, the
school gate, the shop and the hundred francs, the drowning at the
fountain, the fixed-character metaphysics — and to give an auditioner
room to build, not just trade short lines. Voices follow the readings in
the Director's Copy. Character-meets-Player pairings use the
metatheatrical frame (the Player has been cast to play the Character).
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

ROLE_ORDER = ["F", "M", "SD", "S", "MG", "P1", "P2", "P3", "MP"]
ROLE_NAME = {
    "F": "The Father",
    "M": "The Mother",
    "SD": "The Step-Daughter",
    "S": "The Son",
    "MG": "The Manager",
    "P1": "Player 1",
    "P2": "Player 2",
    "P3": "Player 3",
    "MP": "Madame Pace",
}
ROLE_NOTE = {
    "F": "the brain of the family — philosophy as confession",
    "M": "grief, the veil, the three silences",
    "SD": "the moral centre — sharp, indicting, never coquettish",
    "S": "the refuser — withholding as an act",
    "MG": "a tired director — and, without trying, the audience's stand-in",
    "P1": "the Leading Man — forties, vain, faded, defensive",
    "P2": "the Leading Lady — about 35, practical, professional, the one who books the work",
    "P3": "the youngest — early 20s, curious, happiest in the company",
    "MP": "the businesswoman of shame — comic on arrival, chilling on exit",
}

# ---------------------------------------------------------------------------
# Scenes — keyed by a sorted pair of role keys.
# Each scene: {"context": str, "lines": [(SPEAKER_LABEL, text), ...]}
# ---------------------------------------------------------------------------

def key(a, b):
    return tuple(sorted((a, b), key=ROLE_ORDER.index))

SCENES = {
    key("F", "M"): {
        "context": "Years after he sent her away to live with his secretary. He defends the choice as kindness; she carries what it cost. The school gate he names here is the same watching that ends in the shop.",
        "lines": [
            ("FATHER", "You needn't look away from me. I am not the man who wronged you — that man made his choices twenty years ago, and I have had to go on living as whatever was left of him. When I gave you to my secretary, I told myself I was setting you both free. I half believe it still."),
            ("MOTHER", "You always have an answer ready, a reason that lets you sleep at night. I was never given a reason. I was given a household to leave, and another man's name, and three more children to raise — and then his death, and then everything that came after it."),
            ("FATHER", "I watched over you, even so. I sent the little one gifts. I stood at the school gate to see how the children were growing —"),
            ("MOTHER", "You stood at the school gate. Do you hear yourself say it? You watched my children the way a man watches a shop window. And one of those children you would meet again — in a far worse place than any school gate."),
            ("FATHER", "I did not know it was her. Before God, in that room, I did not know."),
            ("MOTHER", "Pity is what you felt at the window. Loss is what I carried through every cheap room we moved to after he died. They are not the same weight, and you will never make them the same by talking, however long you talk."),
            ("FATHER", "...No. They are not the same."),
            ("MOTHER", "Then do not stand in front of these people and call any part of it kindness. Call it what it was, or say nothing at all."),
        ],
    },
    key("F", "SD"): {
        "context": "The core confrontation. She drags his philosophy back to the one room he will not name: Madame Pace's, the hundred francs, the little black dress.",
        "lines": [
            ("STEP-DAUGHTER", "Go on — tell them the philosophy. Tell them all about reality, and conscience, and the many people we each contain. You can talk for a whole hour, Father, and never once let the word 'shop' past your lips."),
            ("FATHER", "I am trying to explain how a man can be one thing in a single moment and something else across the whole length of his life —"),
            ("STEP-DAUGHTER", "Then explain the single moment. The back room at Madame Pace's. The hundred francs you laid on the little table. The black dress you asked me, so gently, to take off. Start there, since you love so much to start at the beginning."),
            ("FATHER", "You will not allow me to be anything more than that one afternoon. A whole life of mine, and you nail me to a single hour of it and call it the truth."),
            ("STEP-DAUGHTER", "That hour was my whole life, in that room. I was two months an orphan, and you were a 'kind gentleman' who happened to be my mother's husband, and you did not recognise me. That is your defence — and it is the very worst thing about you."),
            ("FATHER", "I did not know who you were. If I had known, do you imagine for one moment —"),
            ("STEP-DAUGHTER", "You knew I was little more than a child, and behind that screen anyway. You knew that much, and it did not stop you, and it would not have stopped you, if my mother had not come through that door and seen us both."),
            ("FATHER", "...I have to stand here and live inside what you are saying."),
            ("STEP-DAUGHTER", "Good. Live inside it out loud, where every one of them can hear it. That is the only stage I will ever want to see you on."),
        ],
    },
    key("F", "S"): {
        "context": "The father reaches for the son he abandoned in infancy. The son turns the silence into a verdict.",
        "lines": [
            ("FATHER", "Look at me. Once, just once. You may refuse everything else they ask of you this morning, but you can look at the man who gave you your name."),
            ("SON", "My name is the only thing you ever gave me, and you gave it the way a man hands his coat to a stranger at the door. I have nothing to say to you, and I have said exactly that, in every way I know how."),
            ("FATHER", "You have everything to say. You watched this family come apart, and you decided that watching was cleaner than speaking. That is not silence. That is a sentence you have passed on all of us."),
            ("SON", "What you call my silence is the one thing in this house that belongs to me. You sent my mother away before I could walk, you filled the place with another man's children, and now you would have me perform the loving family we never once were."),
            ("FATHER", "I am your father."),
            ("SON", "You are a man who keeps announcing it, in that warm voice, as though the announcement could make twenty empty years arrive on cue. It cannot. I was raised by no one, in a house you paid for and never set foot inside."),
            ("FATHER", "And if I were to beg you — here, now, in front of all of them?"),
            ("SON", "Then I would watch you beg, exactly as I have watched everything else in this family. And I would still not move one single step toward the scene you so badly want."),
        ],
    },
    key("F", "MG"): {
        "context": "The Father argues the company into staging them at all — and the metaphysics arrive: a character is fixed forever, an actor goes home. The Manager is deciding whether to stay.",
        "lines": [
            ("FATHER", "You think we are mad. I saw it in your face the instant we walked onto your stage — six people in mourning, asking to be put into a play."),
            ("MANAGER", "I think you are six strangers interrupting a rehearsal I am already a week behind on, with a script my company can barely stomach. That is precisely what I think."),
            ("FATHER", "And yet you have not had us thrown out. Your notebook is open. You have stopped pretending to glance at your watch."),
            ("MANAGER", "...No. I haven't thrown you out. God alone knows why."),
            ("FATHER", "Because you have begun to understand, before you will let yourself admit it, that we are more real than the play you were rehearsing. A character is fixed forever in what he is; he cannot lie his way out of it. Your actors go home at night and become other people. We cannot. We have nowhere else to go, and no other hour to live in."),
            ("MANAGER", "What I want is my morning back, and a play I can sell three nights of tickets to. That is the entire height of my ambition today."),
            ("FATHER", "That is not a denial of one word I have said."),
            ("MANAGER", "No. God help me, it isn't. Sit them down. Show me this thing of yours. But if it bores me, every last one of you is out on the street by lunch."),
        ],
    },
    key("M", "SD"): {
        "context": "Mother and daughter over the same wound. The Mother came through the shop door too late to stop it; the Step-Daughter will not let it be smoothed over now.",
        "lines": [
            ("STEP-DAUGHTER", "Don't cover your face. Not with me, not here. You have hidden behind that veil through every room we have lived in, and not once has it protected either of us from anything."),
            ("MOTHER", "I cannot watch you tear yourself open in front of strangers, only so that he will suffer. I have already lost one daughter to that room. I will not stand here and watch you walk back into it for an audience's evening out."),
            ("STEP-DAUGHTER", "I am not doing it to myself — I am doing it to him, and you, of all the people in the world, should want it done. He watched me at the school gate. He very nearly bought me in a shop. You came through that door too late to stop it, and just in time to see it. Don't ask me to be quiet now."),
            ("MOTHER", "I want it to stop. That is the only thing I have ever wanted, from the very first day of all this to this one. To have it stop, and to have my children in a single room, and breathing."),
            ("STEP-DAUGHTER", "It does not stop. That is the thing none of them in this theatre understand. It is taking place now, this very minute, and it will go on taking place forever, because that is what we are. We are not remembering it. We are inside it."),
            ("MOTHER", "You sound like him when you talk that way — like your father, with all his reasons, and his 'forever.'"),
            ("STEP-DAUGHTER", "...Don't. Don't you ever say that to me again. Not that."),
            ("MOTHER", "Then step back from the edge of it. For me, if for nothing else. Just this once, come away."),
        ],
    },
    key("M", "S"): {
        "context": "The mother who was sent away, and the son she left behind to do the family's remembering.",
        "lines": [
            ("MOTHER", "I only want to look at you. I am not asking for your forgiveness, or for you to call me anything at all — I only want to stand in the same room as my first child and look at his face."),
            ("SON", "You left."),
            ("MOTHER", "I was sent. You know that I was sent — you were far too small to remember it, but you have been told, surely, by someone, across all these years."),
            ("SON", "It is the same house either way, with you not in it. A small boy does not feel the reason a mother is gone. He feels only the gone. The reason came later, and it changed nothing about the years without you."),
            ("MOTHER", "I have carried you with me every single day of twenty years. Through that man's house, through his death, through the poverty, through the very room where your sister was lost. You were in all of it, with me, the whole time."),
            ("SON", "You carried the others — the ones you could actually hold in your arms. I was the one left behind to do the remembering for the entire family. That is a different kind of carrying, mother, and it weighs a great deal more."),
            ("MOTHER", "Is there nothing I can say to you? Nothing at all, after everything?"),
            ("SON", "There is nothing either of us can say. We are not a mother and a son — we are two people a story put under the same roof and never once introduced. That is all we have ever been, and it is twenty years too late to be anything more."),
        ],
    },
    key("M", "MG"): {
        "context": "The Manager wants a clean sentence he can stage. The Mother teaches the tired director what a play actually does to the people inside it.",
        "lines": [
            ("MANAGER", "Madam — please — if you could just tell me, plainly, in your own words, what happened to your family, I might be able to build something I can put on a stage."),
            ("MOTHER", "You want it plainly. There is no plainly. There is a husband who sent me away, a man I was given to who died, a daughter pushed into a back room, a little one lost at a fountain, a boy with a revolver. Tell me — where, in all of that, is the plain sentence you can stage?"),
            ("MANAGER", "One moment, then. Give me a single true moment, and I will put two actors inside it."),
            ("MOTHER", "You cannot put actors inside it. You can only make us live it again, in front of you, for as long as you choose to keep us here under your lights. That is not staging a thing. That is making it happen twice."),
            ("MANAGER", "That is what a play is, madam. We take a true thing, and we repeat it — night after night, on purpose."),
            ("MOTHER", "Then your play is a cruelty, sir, and the very worst of it is that you do not yet understand that it is one. You will, I think, before this morning is over."),
            ("MANAGER", "..."),
            ("MOTHER", "Now you have gone quiet. Good. When a man has no answer ready, quiet is the only honest thing left to him. Stay in it one moment longer than is comfortable."),
        ],
    },
    key("SD", "S"): {
        "context": "She taunts him for refusing to rise even for his mother; she names the moment at the fountain when he was the only one of them with feet to move, and didn't. He insists his refusal is freedom — she calls it the same chain that binds them all.",
        "lines": [
            ("STEP-DAUGHTER", "Look at him. He will not even rise from that chair for his own mother — the one person in this whole room who has never once done him a single wrong."),
            ("SON", "Leave me out of your performance. I did not ask to be in your story, and I will not be dragged into the middle of it now, for you or for anyone."),
            ("STEP-DAUGHTER", "It is not a performance, it is the truth, and you are standing in the very middle of it whether you open your mouth or keep it shut. The Child was lost in your father's garden, and you were the one of us who almost moved. You ran toward her. You were a single step from the water. And then you stopped, and you watched a boy watching his little sister in the water, and you did not take that step. That is yours. Not mine. Yours."),
            ("SON", "I am bound to nothing, and to no one. I never once agreed to belong to this invented family."),
            ("STEP-DAUGHTER", "You are bound to this chain exactly as the rest of us are — you only flatter yourself that the chain is a decision you have made. I am the one who runs from this house when the worst of it happens, and even I am still here, still inside it. So are you. So you always will be."),
            ("SON", "Better to stand still and apart than to put myself on display the way you do — for strangers, for a director with his notebook, for whoever has paid to watch."),
            ("STEP-DAUGHTER", "I put myself on display so that the room cannot look away from what was done to us. You stand still and silent precisely so that it can. That is the whole difference between you and me, and it has never once been in your favour."),
            ("SON", "Then let them look away. I would take the dark over your kind of light any hour of any day."),
        ],
    },
    key("SD", "MG"): {
        "context": "She catches the Manager softening her story for the interval crowd. This is her central fight — to keep it true before it is made playable.",
        "lines": [
            ("STEP-DAUGHTER", "You keep softening it. Every single time I tell you what happened, you reach for a gentler word, a prettier angle, something the audience can swallow along with their interval drinks."),
            ("MANAGER", "I am trying to make it playable. There is a real difference between the truth and a thing that can be performed for two hours without the whole house getting up and leaving."),
            ("STEP-DAUGHTER", "Then make it true first, and playable second. Reverse those two, and you will have a very smooth, very forgettable evening about precisely nothing at all."),
            ("MANAGER", "An audience has to be able to bear what we put in front of them. That is not cowardice, young woman. That is the trade I have given my life to."),
            ("STEP-DAUGHTER", "Why must they bear it so lightly? I had to bear it whole — a girl of eighteen, two months an orphan, in a back room with my own stepfather across the table. Let them sit with that for two hours. It is a good deal less time than I have had to sit with it."),
            ("MANAGER", "You are not making any of this easy for me."),
            ("STEP-DAUGHTER", "It was not made easy for me either. That, precisely, is the part you keep so quietly editing out of every version you reach for."),
            ("MANAGER", "...All right. All right. Tell it your way, then. I am listening — and this time I will keep my pencil still."),
        ],
    },
    key("S", "MG"): {
        "context": "The Manager needs the Son in the scene; the Son, an unfinished character, refuses to be made convenient.",
        "lines": [
            ("MANAGER", "I need you in this scene. I have turned it over every way I can, and the whole thing finally hinges on you — the son who stood there and watched and did nothing."),
            ("SON", "Then your whole thing does not hinge, because I will not stand inside it. You are welcome to build the rest of your evening around a man who has decided not to move."),
            ("MANAGER", "You are a character in a play. Characters play their scenes. That is the single rule of the only world you have to live in."),
            ("SON", "I am a character whose author lost interest halfway and left me unfinished. You cannot make me act what was never written for me. There is no scene buried inside me to perform — only the refusal, and that one I will hand you freely, all night long."),
            ("MANAGER", "Everyone in this room is making it up as they go. The whole company is improvising. For God's sake, man — join us."),
            ("SON", "No. My refusal is the one finished thing about me. Take it away, and there is genuinely nothing left where I am standing — so I will keep it, thank you, and you will simply have to work around the gap."),
            ("MANAGER", "You are impossible to direct."),
            ("SON", "I am perfectly, completely consistent. You only call it impossible because you wanted me to be convenient — and I never have been, to anyone in this family, from the very start."),
        ],
    },
    key("SD", "MP"): {
        "context": "The atelier. Madame Pace and the Step-Daughter, back in the room of the hundred francs — where the debt that put her there was her mother's ruined sewing.",
        "lines": [
            ("MADAME PACE", "My dear! You come back to me. I knew you come back — the young ones, they always come back to Madame Pace, sooner or later, one way or another way. It is the one thing in life you can put in the book ahead of time."),
            ("STEP-DAUGHTER", "I did not come back. You have dragged me here by being remembered — you live on inside that half-hour the way a stain lives on inside a dress that can never be worn again."),
            ("MADAME PACE", "Eh — remember, come back, for the book it is all the same thing, my dear. You owe. Your mother, she owe — the silk she ruin with her poor bad sewing, somebody must pay for it. The book, you understand, it must always, always balance."),
            ("STEP-DAUGHTER", "There was no book. There was a frightened girl, and a hundred francs laid out on a little table, and you in the doorway, smiling, and already counting it in your head."),
            ("MADAME PACE", "I smile because I am a polite woman, and I count because that is my trade and I am good at it. The polite ones, my dear, the ones who keep the count — we are the ones who are still here at the end. Your mother, she only weep. And weeping, you will find, pays nobody anything."),
            ("STEP-DAUGHTER", "You sold me an afternoon you knew perfectly well was poison, to a man you were very careful never to look at too closely."),
            ("MADAME PACE", "I sell what is asked for, no more, no less. If you must be angry, my dear, be angry at the one who asked — he had the good coat, the soft quiet voice, the money already folded in the pocket. Me, I only opened the door for him. That is all I ever do. I open the door."),
            ("STEP-DAUGHTER", "I am angry at both of you. Don't trouble yourself — there is more than enough of it in me to keep two separate accounts, and I balance mine too."),
        ],
    },
    key("F", "MP"): {
        "context": "The customer and the keeper of the shop. Madame Pace ties his philosophy to her ledger, and the girl who paid for both.",
        "lines": [
            ("MADAME PACE", "Ah, monsieur. You, I remember very well. The good coat, the soft voice, the money already counted in the pocket before you sit down. The quiet ones, monsieur — in all my long experience, they are without fail the very worst of them."),
            ("FATHER", "I did not know who she was. You must tell them that. You were there — tell them I did not know she was my own wife's daughter."),
            ("MADAME PACE", "You did not ask. That, monsieur, is not at all the same thing as not knowing. A man who truly does not wish to know a thing — he is always very, very careful never once to ask the question."),
            ("FATHER", "You arranged it. You put her in that room, in that dress, and you sent her in to me."),
            ("MADAME PACE", "I put a great many girls in that room, in that dress, monsieur. You were not special — you only think so now, today, because the shame has made you the hero of your own small sad story. In my book you were one line among many."),
            ("FATHER", "Do not speak to me as though we were the same kind of creature."),
            ("MADAME PACE", "Oh, we are not the same, you and I. I kept a book of accounts, and you kept a fine philosophy. But the girl, monsieur — the girl paid for both of them, in the very same coin, inside the very same half-hour. On that one point the book and the philosophy agree."),
            ("FATHER", "..."),
            ("MADAME PACE", "And now you also go quiet on me. Bon. You see, monsieur? I told you at the start. The quiet ones — always, always the worst."),
        ],
    },
    key("M", "MP"): {
        "context": "The Mother's eruption — the line that stops the scene. Madame Pace answers with the cold arithmetic of the trade.",
        "lines": [
            ("MOTHER", "You. You old devil. You murderess. I knew, the very moment I came through that door, exactly what you had made of my daughter."),
            ("MADAME PACE", "Eh, madame, such words, and so very loud. I am a businesswoman, nothing more and nothing less. I keep a small shop. People come in, people go out. That is the whole of my crime."),
            ("MOTHER", "You used my child. While I sat sewing in your back room for a few miserable francs, you were in the front room trading on my own child."),
            ("MADAME PACE", "I sold a dress, madame, a room, an afternoon of somebody's quiet time. What happens between two people behind the folding screen — that, you understand, is not written anywhere on my book."),
            ("MOTHER", "Everything that happened is on your book. You wrote it down in francs, and you balanced the column that same night, and then you slept the whole night through."),
            ("MADAME PACE", "Francs do not lie, madame. People — people lie all day long. They weep, they swear, they say after that they did not know. But the francs, they only ever add up. That is exactly why I trust them, and never once the people."),
            ("MOTHER", "Then may they add up — every last one of them — to your damnation."),
            ("MADAME PACE", "...You pray very prettily, madame. I will give you that much, freely. But prettily or not, your little prayer does not change the total written at the bottom of the page."),
        ],
    },
    key("MG", "P1"): {
        "context": "The cook's-cap argument that opens the rehearsal. The vain Leading Man against the tired Manager who has heard the resignation speech before.",
        "lines": [
            ("PLAYER 1", "Must I absolutely wear the cook's cap? I ask it as a perfectly serious question, you understand — from an actor with a certain standing in this canton."),
            ("MANAGER", "It is in the script. The very same script you read, and discussed, and signed, and cashed the advance against, some weeks ago now."),
            ("PLAYER 1", "I have a reputation. Fifteen years I have been the Leading Man of this company. People in this city know my face, sir, and they did not pay to see it under a kitchen cap."),
            ("MANAGER", "They will know it perfectly well under a cook's cap. Put it on, play the scene, and you may yet keep what is left of the reputation. Argue with me another ten minutes, and I make you no promises about any of it."),
            ("PLAYER 1", "I would sooner resign the whole engagement than be made ridiculous in front of strangers."),
            ("MANAGER", "You threaten to resign every single season — usually somewhere around the first read-through — and every single season you are here on opening night, in precisely whatever hat I have decided to give you."),
            ("PLAYER 1", "One day, sir, I promise you, I shall genuinely surprise you."),
            ("MANAGER", "Then surprise me today. Be ready the instant I call the scene. Cap on. Downstage. And — go."),
        ],
    },
    key("MG", "P2"): {
        "context": "The Manager has no scene yet, only an ending. The practical Leading Lady will act anything the moment he gives her a beginning.",
        "lines": [
            ("MANAGER", "Can we please, for the love of God, just rehearse something? I have lost half a morning now to six strangers and a lecture on the nature of reality."),
            ("PLAYER 2", "We can rehearse the very moment that somebody tells me what the scene actually is. I have been standing here, off-book and ready, for the better part of an hour."),
            ("MANAGER", "The scene is six characters and the tragedy they walked in carrying. That is the scene. That is what we are doing today."),
            ("PLAYER 2", "That is not a scene, that is a situation. A scene has a beginning, and a person who wants something badly, and another person standing in the way of it. What you have handed me is a weather system."),
            ("MANAGER", "...You are quite right. I don't have a beginning yet. I have an ending — God knows I have an ending, it is the clearest thing in the room — but I have no way into it."),
            ("PLAYER 2", "Then go away and find me the way in, and I will act it the very instant you do. I am a professional, after all. I simply require something to actually be professional about."),
            ("MANAGER", "Give me five minutes alone with the Father."),
            ("PLAYER 2", "I shall be right here. I am always right here — which, if you want the honest truth of it, is rather the whole story of my career."),
        ],
    },
    key("MG", "P3"): {
        "context": "The tired Manager and the youngest member of the company, who has never seen a rehearsal turn into this and is half-afraid to admit they love it.",
        "lines": [
            ("PLAYER 3", "Sorry — should I still be taking all of this down? In shorthand, I mean. Only it stopped being the rehearsal quite a while ago, and I honestly wasn't sure whether to keep going."),
            ("MANAGER", "Take everything down. I don't yet know what matters in all this and what doesn't, so for the moment, as far as you are concerned, every word of it matters."),
            ("PLAYER 3", "It's only — I have never once seen a rehearsal turn into a thing like this. Real strangers, and a real story, and you sitting there actually listening to them."),
            ("MANAGER", "Neither have I, child, and I have run something close to forty of these in my time. Which is either a wonderful sign or an absolute catastrophe, and the trouble is I genuinely cannot tell you which."),
            ("PLAYER 3", "Is it exciting, or is it bad? Because from where I am sitting it honestly feels like both at the very same time."),
            ("MANAGER", "At my age, child, exciting and bad have come to feel remarkably alike. The whole art of it is learning to move toward the thing anyway, before you can talk yourself out of it."),
            ("PLAYER 3", "I think it's exciting. I think we are going to remember this particular morning for a long time."),
            ("MANAGER", "Then hold on to that feeling with both hands. You will need it far more than the shorthand — and, I suspect, a great deal longer."),
        ],
    },
    key("P1", "P2"): {
        "context": "Two registers of the same profession sparring while the company waits — the one who wants admiration and the one who wants a wage.",
        "lines": [
            ("PLAYER 1", "In my day, a script made sense before the first rehearsal. One read it, one understood it, one performed it beautifully. There was an order to things, a respect."),
            ("PLAYER 2", "In your day. Yes. We have all of us heard a very great deal about your day. It appears to have been a golden age chiefly remarkable for prominently featuring you."),
            ("PLAYER 1", "I am only observing that a Leading Man requires a part he can take some pride in. Is that vanity? Perhaps it is. It is also, I would remind you, craft."),
            ("PLAYER 2", "A Leading Man requires an audience to admire him. A working actor requires a wage at the end of the month. I will let you guess which of the two of us actually booked the job this season."),
            ("PLAYER 1", "You wound me, you know. You always have, from the very first season we played together."),
            ("PLAYER 2", "I pay my rent, in francs, on the first of the month. Wounding you is merely a little hobby I take up between paying jobs — it costs me nothing, and it has never once let me down."),
            ("PLAYER 1", "...You are a very hard woman, when all is said and done."),
            ("PLAYER 2", "I am a very employed woman. There is a quiet connection between those two facts, and one day, if you watch me closely enough, you may even manage to spot it."),
        ],
    },
    key("P1", "P3"): {
        "context": "The senior Leading Man instructs the newest member of the company in how things 'really' work. They keep trying to write it down.",
        "lines": [
            ("PLAYER 1", "You are new here, so allow me to explain how a company like this one actually works. The Leading Man sets the tone. Everything and everyone else simply arranges itself around that single fact."),
            ("PLAYER 3", "Oh — does he? I rather thought that was the director's job. The setting of the tone, I mean to say."),
            ("PLAYER 1", "The director believes, sincerely, that he sets the tone. That is an entirely separate matter — and, frankly, a small kindness that we all agree to extend to him."),
            ("PLAYER 3", "I see. I'll write that down — it sounds rather like the sort of thing one ought to know early."),
            ("PLAYER 1", "No, no, no — that is precisely the sort of thing one does not write down. One absorbs it. One carries it in the bearing, in the spine. The notebook is for lines, child, not for wisdom."),
            ("PLAYER 3", "Sorry. I write everything down. It is my first proper season, and I am quietly terrified of missing something that turns out to matter."),
            ("PLAYER 1", "...It shows, you know. The terror. Though — and I surprise myself by saying it — not at all unpleasantly. There is a freshness to it that the rest of us seem to have mislaid somewhere along the years."),
            ("PLAYER 3", "Was that — was that a compliment, just now?"),
            ("PLAYER 1", "From me, child, that was very nearly a bouquet. Enjoy it. I do not, as a rule, issue them more than once a season."),
        ],
    },
    key("P2", "P3"): {
        "context": "The seasoned professional and the beginner. The youngest wants every morning to mean something; the elder has made a harder, wiser peace.",
        "lines": [
            ("PLAYER 3", "Can I ask you something, honestly? How do you manage to stay so completely calm when the whole morning falls apart like this around us?"),
            ("PLAYER 2", "Practice, mostly. And steadily lowered expectations. If I am being truthful with you, rather more of the second of those than the first."),
            ("PLAYER 3", "I keep wanting it to mean something. Every scene, every rehearsal, every morning. Is that very foolish of me?"),
            ("PLAYER 2", "It is not foolish, it is young — which is very nearly the same thing, and far better company. It will mean something, now and then, when you least expect it. The whole trick is not to build your entire week around the few days that it does."),
            ("PLAYER 3", "That sounds a little bleak, put quite like that."),
            ("PLAYER 2", "It is a little true, put quite like that. The bleakness, you will find, comes free with the years; the truth you have to earn, one disappointment at a time, and pay for in full."),
            ("PLAYER 3", "I do hope I am like you in twenty years' time."),
            ("PLAYER 2", "Aim a good deal higher than that, love. Aim to be employed and entirely unbothered. I have only ever managed the first of the two — and here I still am, at my age, arguing with a Leading Man about a hat."),
        ],
    },
    # ---- Character × Player: the metatheatrical frame ----
    key("F", "P1"): {
        "context": "Player 1 has been cast to play the Father in the staged version, and comes to him for the character. The Father refuses to be reduced to a motivation.",
        "lines": [
            ("PLAYER 1", "So I am to play you, in the staged version of all this. I shall need to properly understand the man. What is my motivation, as it were — what is it that the Father actually wants?"),
            ("FATHER", "My motivation, as you put it, is precisely not to be reduced to a motivation. The very moment you decide, in a single tidy word, what I 'want' — you have already made me smaller than I am, and the audience will believe your small version of me, because it is easier to carry home."),
            ("PLAYER 1", "That is not, if I may say so, terribly useful to a working actor with a fortnight in which to learn the part."),
            ("FATHER", "It is the truest thing I am able to put into your hands. I am a man of a dozen contradictions held together in one body — tender and monstrous within the very same hour. If you smooth all of that into one clean intention, you will be playing a character. I am not a character. I am a man — which is a great deal worse to play, and worse to be."),
            ("PLAYER 1", "Then tell me, plainly, how to do it. I will gladly take plainly, at this point."),
            ("FATHER", "Very well. Play a man who cannot stop talking — because in the half-second of silence, the shame arrives, and he simply cannot survive its arrival. The philosophy is not wisdom, whatever it sounds like. It is a man running, out loud, from a single room, for the whole rest of his life."),
            ("PLAYER 1", "...That, I believe I can do. God help me — I think I actually know that man."),
            ("FATHER", "I was rather afraid that you would. Most men do, if they are honest, which is why most men look away."),
        ],
    },
    key("F", "P2"): {
        "context": "Player 2 is cast to read the Mother in the staged version. The Father — of all people — coaches her on his own wife's grief.",
        "lines": [
            ("PLAYER 2", "They have handed me your wife to play, in the staged scenes. I should very much like to get her right, and you are the only one in this room who truly knew her."),
            ("FATHER", "Then do not act her grief. Carry it. There is a world of difference between performing a sorrow and walking, all evening, under its actual weight — and the audience knows which of the two it is watching long before its mind has caught up with its eyes."),
            ("PLAYER 2", "That is a note I would expect to give, frankly, not to be given."),
            ("FATHER", "You asked me, and I have watched that particular grief from the inside of the marriage that made it. I know its exact weight, to the gram. When she covers her face with her hands, understand this — she is not hiding from the room. She is hiding from the memory, which is standing in the room with her, and which will not leave when the scene ends."),
            ("PLAYER 2", "So — restraint, then. Not the large gesture."),
            ("FATHER", "The precise opposite of the large gesture. She lost a daughter to a back room and a child to a fountain, and she has been given almost no lines to say about either. Let the silence carry everything that I, God knows, never once could."),
            ("PLAYER 2", "You speak about her very tenderly, I notice — for the man who ruined her whole life."),
            ("FATHER", "Tenderness and ruin are not opposites, madam. A man may do both to the same woman, across the same years, and mean each of them entirely. That is the whole of the tragedy — and if you can play that, you will be playing me every bit as much as you are playing her. Write that one down, if you write down anything."),
        ],
    },
    key("M", "P1"): {
        "context": "Player 1 is cast as the husband. The Mother gives him the one note that will cost the man most: do not make him grand.",
        "lines": [
            ("PLAYER 1", "I am to play your husband, in the staged version. Have you any guidance for me? You knew the man better than anyone, after all."),
            ("MOTHER", "One thing, above every other. Do not make him a villain. He would love that — it is the very performance he gives of himself, in private, when no one is watching. A villain is grand, you see. And he would so much rather be grand than be what he actually was."),
            ("PLAYER 1", "And what was he, in your view, if not that?"),
            ("MOTHER", "Ordinary. A perfectly, completely ordinary man — who was certain, every single day of his life, that he was being kind. He sent me away and he called it generosity. He watched my children grow up from a distance and he called it love. Play that certainty, sir. It will cost the audience a great deal more than any villain ever could."),
            ("PLAYER 1", "That is a remarkably exact note, madam. Very nearly a director's note, if you'll forgive me."),
            ("MOTHER", "I had twenty years in which to arrive at it. You have a fortnight. You are entirely welcome to mine — I have no other use left for it now."),
            ("PLAYER 1", "...Ordinary. And certain that he is kind. Yes. I have it."),
            ("MOTHER", "Ordinary, and certain that he is kind, even with the very worst of it standing right there in front of him. That is the man, exactly. Get that, and you will frighten people who came in expecting nothing but a melodrama."),
        ],
    },
    key("M", "P2"): {
        "context": "Player 2 is cast to play the Mother. The Mother warns her off the trap everyone falls into — sympathy.",
        "lines": [
            ("PLAYER 2", "I am playing you. I have read it through three times now, and I still find I don't want to get you wrong."),
            ("MOTHER", "You will get me wrong the very moment you try to make me sympathetic. Everyone reaches for that door first. It is the one door, of all of them, that leads absolutely nowhere."),
            ("PLAYER 2", "Aren't you sympathetic, though? You seem to me the one person in the whole play who is owed everything and given nothing."),
            ("MOTHER", "I am silent. That is all. People mistake silence for gentleness, and gentleness for sympathy, and so they decide, comfortably, that I am a sweet, sad woman in a veil. I am not sweet. I am a woman who simply stopped arguing — because there was nothing left anywhere in the house that was still worth the winning."),
            ("PLAYER 2", "So what I am playing is — defeat. Is that it, at bottom?"),
            ("MOTHER", "You are playing someone who is still on her feet after the defeat, and still in the room, and still searching the crowd for her son's face. That is a great deal harder than defeat. Defeat sits down and is done. I was never once allowed to sit down."),
            ("PLAYER 2", "I have been acting for forty years, and that is the finest single note anyone has handed me all week."),
            ("MOTHER", "Then it was well worth the breath it cost me. I spend so very few words, these days — it is good to learn that one of them at last landed somewhere it was needed."),
        ],
    },
    key("S", "P1"): {
        "context": "Player 1 is sent to coax the Son into the scene, actor to actor. The Son makes the coaxing impossible.",
        "lines": [
            ("PLAYER 1", "They have sent me over to coax you into the scene — actor to actor, you understand, one professional to another, that sort of thing entirely."),
            ("SON", "Then they have wasted your morning along with mine — and you strike me as a man who rather values his mornings."),
            ("PLAYER 1", "Come now. We all of us play parts we would much rather not. I am, this very morning, about to play a man in a cook's cap. Dignity, in this trade, is a thing one surrenders by small instalments."),
            ("SON", "You play parts you would rather not, for a wage, and then you go home afterward and pour yourself a drink and become yourself again by the fire. I am being asked to play the worst night of a family that was never even finished being written. There is no drink afterward, for me. There is no afterward at all."),
            ("PLAYER 1", "...When you put it in quite those terms, I confess the whole thing lands rather differently than I expected."),
            ("SON", "There is no other way to put it. That is exactly why I put it that way — so that even a coaxer, even a kind one, would have to stop his coaxing and go away."),
            ("PLAYER 1", "Then I shan't coax you. I shall go back and report that you are entirely immovable, and then I shall go and find my cap."),
            ("SON", "Good. You are the first one they have sent across all morning with the plain sense to stop. I find I almost respect it."),
        ],
    },
    key("S", "P2"): {
        "context": "Player 2 doesn't pretend to understand the Son. He respects her honesty — and they find a quiet, exact understanding.",
        "lines": [
            ("PLAYER 2", "I won't pretend that I understand you. But I would like to, if you'll let me — and I am far too old, at this point, to pretend off the clock."),
            ("SON", "That is more honest than the rest of them have managed all morning. They all pretend to understand me. It is simply their chosen method of getting me to stand up and move."),
            ("PLAYER 2", "I've no interest at all in moving you. I just don't much like playing opposite a man I can't read. It is bad for the work, and the work is the only part of this I still care about."),
            ("SON", "Then read this much, and we are square, you and I. I am not sulking, whatever my stepsister keeps announcing to the room. I made a decision a very long time ago, and I am simply keeping it — and people insist, endlessly, on mistaking the keeping of a decision for a passing mood."),
            ("PLAYER 2", "A decision to do nothing at all, then."),
            ("SON", "A decision not to be used. By my father, by that director with his notebook, by a story that handed me a whole family and never once gave me a single line worth the saying inside it. There is a real difference between doing nothing and refusing to be used — and you, of anyone in this room, ought to feel that difference in your bones."),
            ("PLAYER 2", "...I do, as it happens. Rather more than I would care to say out loud in front of the others."),
            ("SON", "Then we understand one another, you and I. That is a good deal rarer in this room than you would ever think — and I have no intention of wasting it by explaining myself a second time."),
        ],
    },
    key("S", "P3"): {
        "context": "The youngest in the company asks the Son the question no one else dares — and is the only one who grants that his refusal might be right.",
        "lines": [
            ("PLAYER 3", "Can I ask you something — and please, do tell me to stop — why won't you simply do the scene? Everyone is waiting on you, and it would all be over so very quickly."),
            ("SON", "Because the 'scene,' as you so lightly call it, is my family being torn open straight down the middle — and I am the one being asked to hold the two raw halves apart with my own bare hands, while a room full of strangers sits and watches it happen."),
            ("PLAYER 3", "...When you say it like that — I think that I would refuse it too. I think anyone would."),
            ("SON", "You are the only person in this entire company who has said so out loud. The rest of them are all far too busy being professional to notice what it is they are actually asking me to perform."),
            ("PLAYER 3", "I am new. I haven't yet learned how to make a thing like this look normal. I rather expect that I will, in time — and I am not at all sure that I want to."),
            ("SON", "Then don't learn it. The morning this starts to look normal to you is the morning you will have lost the one thing in you that was ever worth the keeping. Guard it carefully. Nobody else in this place will guard it for you, I can promise you that."),
            ("PLAYER 3", "I'll try to remember that. I really will, I promise."),
            ("SON", "You won't. The work wears it clean off everyone, in the end. But it was a kind thing to say — and I have heard very few kind things under this roof. So I will keep it for you, since you won't be able to."),
        ],
    },
    key("SD", "P1"): {
        "context": "Player 1 is cast as the gentleman in the shop scene. The Step-Daughter teaches him exactly how to play the man who nearly bought her.",
        "lines": [
            ("PLAYER 1", "I'm cast as the gentleman in your — in the shop scene. I want to be quite sure that I play him correctly, given everything."),
            ("STEP-DAUGHTER", "The gentleman. So that is the word they have settled on this particular morning. Very well, then — the gentleman. We shall see how long the word survives the scene."),
            ("PLAYER 1", "It is the role exactly as it is written. I did not choose the word, I assure you."),
            ("STEP-DAUGHTER", "Then play him precisely as he was, and the word will turn to ash all on its own, with no help from either of us. Polite. Soft-voiced. Beautifully, faultlessly mannered. And certain, the whole way through, that he was doing nothing whatever wrong. Don't give him horns, and don't give him a leer — he had neither. The complete absence of them is the entire horror of the thing."),
            ("PLAYER 1", "You are asking me, then, to make the audience comfortable with him. That is an unusual note."),
            ("STEP-DAUGHTER", "I am asking you to make them comfortable — to let them like him, lean toward him, recognise him as a man they might know. And then I will do the rest of the work myself. Your charm is my weapon, you understand. The more completely they trust him, the harder it lands when they finally remember who I am, and how old. Hand me that. Play him beautifully."),
            ("PLAYER 1", "...That is almost frightening, the way you have thought the whole of it through."),
            ("STEP-DAUGHTER", "It is entirely meant to be frightening. You are beginning, at last, to understand the part. Now stand just there, and be charming — and you may leave the knife safely to me."),
        ],
    },
    key("SD", "P2"): {
        "context": "Player 2 is cast as the Step-Daughter — and laughed while first reading it. The Step-Daughter turns that very laugh into the shape of the performance.",
        "lines": [
            ("PLAYER 2", "They have given me you to play. I would genuinely like to do you justice, if only I can find the way in."),
            ("STEP-DAUGHTER", "Don't do me justice — justice is the one thing in the world I was never given, and a performance full of it would be a lie from the first line. Do me accurately. That, I can actually use."),
            ("PLAYER 2", "Then tell me the difference between the two, in your own words."),
            ("STEP-DAUGHTER", "Justice turns me into a martyr — pale, wronged, weeping prettily in a good light, the sort of girl an audience can comfortably pity and then forget on the tram home. Accurate makes me furious, and right, and completely uninterested in anyone's tears, my own included. One of those lets them off the hook. The other does not, ever."),
            ("PLAYER 2", "I laughed at you, you know. Earlier, when I first read the lines aloud to the room. I'm genuinely sorry for it."),
            ("STEP-DAUGHTER", "Of course you laughed. Everyone laughs first — at the accent, at the situation, at the sheer indecency of hearing it said out loud at all. And then they hear what it was, exactly, that they were laughing at. Use that. Make them laugh in the first half, precisely as you did — and then make them choke on the laugh in the second. That is the whole shape of the part, start to finish."),
            ("PLAYER 2", "...I have been made a fool of by a great deal worse than this play, in forty years."),
            ("STEP-DAUGHTER", "Then you will play me to the very life — a woman who has been made a fool of, and who has decided, coldly and for good and all, that she will not allow it for one single second longer."),
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
    partners = [r for r in ROLE_ORDER if r != role and key(role, r) in SCENES]
    scenes_html = "".join(render_scene(role, other) for other in partners)
    n = len(partners)
    count_label = (
        f"{n} two-hander &middot; her only scene partner in the play"
        if n == 1 else
        f"{n} two-handers &middot; one with each role she shares the stage with"
        if role == "MP" else
        f"{n} two-handers &middot; one with each other speaking role"
    )
    return f"""
    <section class="role-section">
      <div class="role-head">
        <h2>{ROLE_NAME[role]}</h2>
        <p class="role-note">{ROLE_NOTE[role]}</p>
        <p class="role-count">{count_label}</p>
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
        elif key(r, c) in SCENES:
            cells += '<td class="y">&#10003;</td>'
        else:
            cells += '<td class="x">&middot;</td>'
    matrix_rows += f'<tr><th>{ROLE_NAME[r]}</th>{cells}</tr>'
matrix_head = "".join(f'<th class="rot">{ROLE_NAME[c]}</th>' for c in ROLE_ORDER)

HTML = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Audition Two-Hander Pack — Six Characters in Search of an Author</title>
<style>
  :root {{ --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }}
  @page {{ size: A4; margin: 12mm; }}
  *,*::before,*::after {{ box-sizing: border-box; }}
  html, body {{ background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif;
    font-size: 11pt; line-height: 1.6; margin: 0; padding: 0; }}
  main {{ max-width: none; margin: 0; }}

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
  .line {{ margin: 0 0 2.5mm 0; line-height: 1.5; }}
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
    <p>A two-hander side for every pairing of the nine speaking roles. In each scene <strong>only the two named characters speak</strong> — so you can sit any two auditioners (or an auditioner and a reader) down and run a clean scene with no third voice. Madame Pace, now a Character carried by her own performer, has a section of her own — her three scenes are the only ones she has in the play.</p>
    <p>Each side is written to carry real story weight — the secretary, the school gate, the shop and the hundred francs, the drowning at the fountain, the fixed-character argument — and the speeches are long enough to give an auditioner something to build, redirect, and build again. The voices follow the production's readings in the Director's Copy.</p>

    <h2>How it's organised</h2>
    <p>By character. Each of the nine speaking roles has its own section containing a two-hander with <strong>every other role it shares the stage with</strong>. So if you are seeing people for the Father today, go to <em>The Father</em> and every Father pairing is there in one place — you never have to flip.</p>
    <ul>
      <li>Every scene therefore appears <strong>twice</strong> — once in each partner's section. That is deliberate, not an error: it keeps each character's material whole.</li>
      <li>Where a <strong>Character meets a Player</strong> (e.g. the Father and Player 1), the scene uses the production's own logic — the Player has been cast to play that Character, and they meet to work on the role. These sides test something rare and very Pirandellian: a reader playing an actor playing a part.</li>
      <li><strong>Madame Pace</strong> has her own section — the shop, the ledger, the cold — with the Step-Daughter, the Father, and the Mother, the only three she meets in the play. Player 3's scenes are the young company member's own: with the Son, the Manager, and the other two Players.</li>
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
             margin={"top": "12mm", "right": "12mm", "bottom": "12mm", "left": "12mm"},
             print_background=True, prefer_css_page_size=True)
    browser.close()

try:
    from pypdf import PdfReader
    r = PdfReader(str(OUT))
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes) · {len(r.pages)} pages")
except BaseException:
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes)")
