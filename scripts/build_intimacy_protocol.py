#!/usr/bin/env python3
"""Build the Intimacy and Consent Protocol PDF.

A standalone document containing the complete intimacy and consent
protocol for the production. Distributed to every cast member before
the first rehearsal. Every performer signs it. The protocol is
absolute; no role on the production is senior to it.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
OUT_DIR = Path(os.environ.get("OUT_DIR", HERE / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get("CHROMIUM_PATH")

HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Intimacy and Consent Protocol — Six Characters in Search of an Author</title>
<style>
  :root { --bg:#efe6cf; --ink:#2a201a; --ink-soft:#6b5b48; --accent:#8b3a3a; --rule:rgba(42,32,26,0.18); }
  @page { size: A4; margin: 22mm 22mm 22mm 22mm; }
  *,*::before,*::after { box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--ink);
    font-family: 'EB Garamond','Georgia','Times New Roman',serif;
    font-size: 11pt; line-height: 1.65; margin: 0; padding: 0; }

  main { max-width: 162mm; margin: 0 auto; }

  .masthead { text-align: center; margin-bottom: 8mm; padding-bottom: 6mm;
              border-bottom: 1px solid var(--rule); }
  .eyebrow { font-family:'Cormorant Unicase',serif; font-weight:600;
             font-size: 9pt; letter-spacing: 0.28em;
             text-transform: uppercase; color: var(--accent);
             margin: 0 0 4mm 0; }
  h1 { font-family:'Cormorant Garamond',serif; font-weight: 500;
       font-size: 22pt; line-height: 1.15; margin: 0 0 2mm 0; }
  .play { font-style: italic; font-size: 11pt; color: var(--ink-soft);
          margin: 0 0 4mm 0; }
  .credit { font-size: 10.5pt; color: var(--ink); margin: 0; letter-spacing: 0.04em; }

  h2 { font-family:'Cormorant Unicase',serif; font-weight: 600;
       font-size: 11pt; letter-spacing: 0.22em;
       text-transform: uppercase; color: var(--accent);
       margin: 8mm 0 3mm 0; }
  h3 { font-family:'Cormorant Garamond',serif; font-weight: 600;
       font-size: 13pt; color: var(--ink);
       margin: 5mm 0 2mm 0; }

  p { margin: 0 0 3mm 0; }
  ul { margin: 0 0 4mm 0; padding-left: 6mm; }
  li { margin-bottom: 3mm; line-height: 1.6; }
  strong { color: var(--ink); }
  em { color: var(--ink); }

  .callout { border-left: 3px solid var(--accent);
             padding: 3mm 5mm; margin: 4mm 0 5mm 0;
             background: rgba(255,255,255,0.25); }
  .callout p:last-child { margin-bottom: 0; }

  .summary-box { border: 1px solid var(--rule);
                 padding: 5mm 6mm; margin: 4mm 0 6mm 0;
                 background: rgba(255,255,255,0.25); }
  .summary-box h2 { margin-top: 0; }

  /* Signature block */
  .signature { margin-top: 10mm; padding: 6mm 6mm;
               border: 1px solid var(--accent);
               background: rgba(139,58,58,0.04); }
  .signature h2 { margin-top: 0; color: var(--accent); }
  .signature .sig-line { margin: 5mm 0 3mm 0;
                         border-bottom: 1px solid var(--ink);
                         min-height: 12mm; }
  .signature .sig-label { font-size: 9.5pt; color: var(--ink-soft);
                          letter-spacing: 0.04em; }
  .signature .sig-row { display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 8mm; margin-top: 4mm; }
  .signature .sig-statement { font-size: 10.5pt; line-height: 1.6;
                              margin-bottom: 5mm; }

  .page-break { page-break-before: always; }
  section { page-break-inside: avoid; }

  footer.foot { margin-top: 10mm; padding-top: 4mm;
                border-top: 1px solid var(--rule);
                font-size: 9.5pt; color: var(--ink-soft);
                font-style: italic; text-align: center; line-height: 1.6; }
  footer.foot strong { font-style: normal; color: var(--ink); }
</style>
</head><body>

<main>

  <div class="masthead">
    <p class="eyebrow">Intimacy and Consent Protocol</p>
    <h1>Six Characters<br>in Search of an Author</h1>
    <p class="play">Sei personaggi in cerca d'autore &nbsp;·&nbsp; Pirandello, trans. Storer 1922</p>
    <p class="credit">A Village Players production &nbsp;·&nbsp; Lausanne &nbsp;·&nbsp; late autumn 2026</p>
    <p class="credit" style="margin-top:6px;">Director: <strong>Kiarash Jamshidi</strong></p>
  </div>

  <section class="summary-box">
    <h2>What this document is</h2>
    <p>This is the production's intimacy and consent protocol. It is a separate document from the script and the production notes because the protocol is separate from them in principle: it is a contract, not a directorial reading.</p>
    <p>Every performer cast in this production receives a copy before the first rehearsal. Every performer signs it. The director also signs each performer's copy. The signed copies are held in the production archive.</p>
    <p>The protocol is absolute. No role on the production is senior to it — not the director's, not the Assistant Director's, not the Stage Manager's. If anything during an intimacy rehearsal or performance feels wrong to any performer, the action stops. That authority is built into the contract.</p>
  </section>

  <section>
    <h2>Why this play needs a protocol</h2>
    <p>This play has at its centre an unstaged transaction between a middle-aged man and a young woman who is his stepdaughter, in the back room of a dressmaker's shop. The Step-Daughter says, of the moment behind the screen, that she was <em>almost nude</em>. The production does not show this. It does not need to. The Step-Daughter's recounting carries it; the lighting and the screen do the rest.</p>
    <p>But the play also requires real physical contact between the actor playing the Father and the actor playing the Step-Daughter — at the shop-scene replay, and at the <em>Cry out mother</em> moment in Act Two. There is also bounded contact between the Father and the Mother (the veil moment), between Madame Pace and the Step-Daughter (a hand under the chin), and between the Father and the Son (held grip in Act Three). Each of those moments must be rehearsed, scored, and consented to, line by line, before they are ever played in front of anyone.</p>
  </section>

  <section>
    <h2>First principles</h2>
    <ul>
      <li><strong>Every physical contact in this play is choreographed.</strong> Nothing is improvised in the moment. The actors know, before any rehearsal in front of the company, exactly where each hand goes, for how long, and what happens after. The choreography is written down.</li>
      <li><strong>The actor playing the Step-Daughter has absolute veto, at any moment, including in performance.</strong> If she signals that a contact is not happening, the contact does not happen, and the production has a substitute in place for it. The same applies to the Mother (the veil moment), the Boy/Child (handled here as object, not as person), and any Player asked to perform intimacy on the upper platform.</li>
      <li><strong>The director does not work intimacy alone with the performers.</strong> A third party — an intimacy consultant where one is available, or a trusted member of the company who is not in the scene — is present at every intimacy rehearsal. Doors are not closed. The Assistant Director and the Stage Manager are both valid third parties when not themselves in the scene.</li>
      <li><strong>Intimacy is rehearsed separately</strong> from the rest of the play, at the start of the staging block, with the full text of the moment laid out and discussed before any blocking. The performers say <em>yes</em> to each beat individually. They are also told, in writing, what they may say <em>no</em> to and how to do it.</li>
      <li><strong>When the scene requires more than the performers have agreed to, the production carries the weight, not the bodies.</strong> Light, music, the screen, the projection, the bundle, the chair-and-coat, the wig — these are the production's substitutes. The script's "almost nude" is not a costume note; it is a line the Step-Daughter says about herself. What the audience sees is a young woman fully dressed, in a column of light, behind a folding screen, while a piano plays. The intensity is in the report, not the display.</li>
    </ul>
  </section>

  <section class="page-break">
    <h2>Every moment of contact in the play, and what the production does with it</h2>
    <ul>
      <li><strong>The Step-Daughter's "My passion, sir!" in Act One.</strong> The Step-Daughter places <em>a deliberate hand on the Father's shoulder, leaves it there one beat too long, withdraws</em>. That is the contact. Hand on shoulder. One beat. Withdraw. No embrace. No kiss. No proximity beyond what the gesture requires. The cruelty is in the deliberateness, not the duration.</li>

      <li><strong>The Father lifting the Mother's veil in Act One.</strong> The Father <em>raises her veil</em> against her will. He does not touch her face. His hand goes only to the lower edge of the veil. The Mother does not push him away — she covers her face with her hands the moment the veil is up. The actor playing the Mother controls the speed of the lift; the actor playing the Father follows. If the Mother does not raise her arms in time, the Father has already chosen, in advance, to release the veil and step back. The blocking is rehearsed both ways.</li>

      <li><strong>Madame Pace handling the Step-Daughter.</strong> Madame Pace places <em>one hand under the Step-Daughter's chin to raise her head</em>. That is all. The hand does not stay. The proximity is dressmaker-to-customer; the wrongness is in the framing, not in any further touch.</li>

      <li><strong>The Step-Daughter and the bundle, Act Two.</strong> Tender, never sexual. The Step-Daughter holds the bundle, kisses it (top of the cloth, brief), sets it down, lifts it again. The recorded voice in the projection carries the rest. There is no contact with a performer.</li>

      <li><strong>The shop scene — Father and Step-Daughter playing themselves, Act Two.</strong> The Father offers the hat; the Step-Daughter declines; the Father reaches toward her dress (the mourning reveal). <strong>The Father's hand stops at a fixed distance from her body — six inches, agreed in rehearsal — and never crosses it.</strong> The script's "let's take off this little dress" is said but never enacted; the Step-Daughter herself only <em>touches the front of her black dress, once</em>, on her own. The folding screen is positioned so that, when she "went there behind that screen," she steps out of the audience's line of sight entirely for two seconds. Nothing else happens. The screen is a literal screen.</li>

      <li><strong>The shop scene replayed by Player 1 and Player 2.</strong> Same rules, transposed. The Leading Man and Leading Lady go through the choreography the Father and the Step-Daughter just established, with the same six-inch limit. The Leading Lady's hat-removal is "efficient, the gesture of a woman who has done it a hundred times in front of a mirror" — it is a costume action, not a sexualised one.</li>

      <li><strong>The Step-Daughter's "Cry out mother!" moment, end of Act Two.</strong> The most physically demanding moment in the play, after the shop scene. The Step-Daughter <em>goes close to the Father and leans her head on his breast, with her arms round his neck</em>. This is rehearsed with maximum care. The agreed blocking: she stands beside him, places her right cheek lightly against his shoulder (not chest), and rests one hand on his upper arm. He does not reciprocate. He does not touch her. The audience reads the closeness; the bodies do not need to enact it. If, at any rehearsal or performance, the Step-Daughter signals that even this contact is not happening, she stands at half a metre's distance and the Mother breaks them up before any contact would have started.</li>

      <li><strong>The Mother separating them.</strong> The Mother <em>pulls her away</em>. The action is brief, physical, and choreographed: the Mother's hand on the Step-Daughter's shoulder or upper arm, never higher. Both actors know the move before the scene begins.</li>

      <li><strong>The Father grabbing the Son in Act Three, Part II.</strong> The script: <em>taking hold of him and shaking him</em>. In our staging the contact is hands on shoulders, no shaking — just held grip. The Son <em>takes hold of the Father</em> in return; this contact is also hands on shoulders. Neither face goes near the other's. The agitation in the scene is in voice and in the room around them.</li>
    </ul>
  </section>

  <section>
    <h2>When the scene wants more than the actors have agreed to</h2>
    <p>There will be moments in the rehearsal process when the script appears to ask for more intensity than the choreography delivers — the Step-Daughter's "almost nude," the Father's "in the arms of her," the "fingers tingling with shame." This is a real tension. The production resolves it not by asking more of the bodies but by giving the staging more to do.</p>
    <ul>
      <li><strong>Light carries the heat.</strong> The shower light in Act Two — the narrow column the Step-Daughter and Madame Pace stand inside — does the work of focus that a closer contact would have done.</li>
      <li><strong>Music carries the seduction.</strong> The Weill / Mistinguett vamp under the Madame Pace aria says, in two bars, what no physical proximity should be asked to say.</li>
      <li><strong>The screen is the screen.</strong> Pirandello already gives us a literal hiding-place. When the script needs the Step-Daughter to disappear from view for two seconds, the screen disappears her. The audience reads what happens behind it. The bodies do not enact it.</li>
      <li><strong>The bundle and the chair-and-coat carry the family.</strong> The play's most intimate relationships — Step-Daughter-and-Child, Step-Daughter-and-Boy, Mother-and-children — are with objects. The objects can be held, kissed, embraced freely. The performers do not have to do any of that with each other.</li>
      <li><strong>If a moment still feels wrong in rehearsal, it is rewritten.</strong> The director rewrites the blocking, not the script. We have done it before. We will do it again. The play survives. It always survives.</li>
    </ul>
  </section>

  <section>
    <h2>The third party at every intimacy rehearsal</h2>
    <p>No intimacy rehearsal in this production takes place without a third party present in the room. The director does not work intimacy with the performers alone. Doors are not closed.</p>
    <p>The third party is one of:</p>
    <ul>
      <li>An intimacy consultant, where one is available and engaged for the production.</li>
      <li>The <strong>Assistant Director</strong>, provided they are not themselves in the scene being worked.</li>
      <li>The <strong>Stage Manager</strong>, on the same terms.</li>
      <li>A trusted member of the company who is not in the scene, agreed in advance by the performers.</li>
    </ul>
    <p>The third party is present, attentive, and silent during the rehearsal itself. They do not direct from the side. They raise any concerns with the director afterwards, in writing if needed. If the named third party is not available, the rehearsal is rescheduled. The intimacy rehearsal never proceeds with the director and the performer or performers alone.</p>
  </section>

  <section class="page-break">
    <h2>Calendar — when intimacy rehearsals happen</h2>
    <p>No intimacy work happens during the audition block (2 / 5 / 10 June 2026) or during the seven-Thursday table-work block (18 June – 30 July 2026). The seven Thursdays are table work only — discussion, reading, walk-through of the production concept. No blocking. No physical work.</p>
    <p>Intimacy rehearsals are scheduled in the staging block (5 August – 1 November 2026), as separate dedicated sessions outside the standard Thursday rehearsals. The specific dates are confirmed by the Stage Manager once the cast is in place, and shared with the affected performers (the actors playing the Father, the Mother, the Step-Daughter, Player 1, Player 2, and Player 3) at least two weeks in advance.</p>
    <p>Each intimacy moment in the play (listed above) has at least one dedicated rehearsal session, scheduled before any blocking with the rest of the company. The choreography is fixed in that session. The session is short — typically thirty to forty-five minutes — because the work is precise and tiring. The performers walk away knowing exactly what will happen on stage.</p>
  </section>

  <section>
    <h2>What every performer may say no to</h2>
    <p>Every performer in this production has the right, at any moment, to:</p>
    <ul>
      <li>Say <em>no</em> to any specific contact or proximity, with no requirement to explain why.</li>
      <li>Ask for a third party to be present, beyond the third party already required by this protocol.</li>
      <li>Ask for any rehearsal of intimacy to be paused, reset, or rescheduled.</li>
      <li>Ask for the blocking to be rewritten if a moment is not landing safely.</li>
      <li>Ask for a substitution — an object, a piece of staging, a change in lighting — to do what the body was being asked to do.</li>
      <li>Withdraw consent for a contact that was previously agreed, including during a performance.</li>
    </ul>
    <p>Saying <em>no</em> never affects the performer's role in the production or their standing with the company. The director, the Assistant Director, and the Stage Manager are bound by this provision.</p>
  </section>

  <section>
    <h2>The principle, in one line</h2>
    <div class="callout">
      <p><strong>Bounded bodies, unbounded moral force.</strong> The choreography above is what the actors do. The production around them — the language, the light, the props, the age in the room, the silence on stage — is what does the rest. What the bodies do not enact, the audience reads as something they cannot un-see. The discomfort the audience leaves with lives in the script and the staging, not in the actors' contact.</p>
    </div>
  </section>

  <section class="page-break signature">
    <h2>Performer acknowledgement and signature</h2>
    <p class="sig-statement">By signing below, I acknowledge that I have read this protocol in full and I understand what is being asked of me — and what I am being protected from being asked. I understand that I may withdraw consent for any contact at any time, including during a performance. I understand that a third party is present at every intimacy rehearsal, and that the director, the Assistant Director, and the Stage Manager are bound by every provision of this document.</p>

    <div class="sig-row">
      <div>
        <p class="sig-label">Performer name</p>
        <div class="sig-line"></div>
      </div>
      <div>
        <p class="sig-label">Role</p>
        <div class="sig-line"></div>
      </div>
    </div>

    <div class="sig-row">
      <div>
        <p class="sig-label">Signature</p>
        <div class="sig-line"></div>
      </div>
      <div>
        <p class="sig-label">Date</p>
        <div class="sig-line"></div>
      </div>
    </div>

    <p class="sig-statement" style="margin-top:10mm;">By countersigning, I acknowledge that I have read this protocol in full and I bind myself to every provision of it. I will not work intimacy with this performer without a third party present. I will honour the right of veto stated above, including during performance. If I fail in any of these provisions, the protocol authorises any performer to stop the rehearsal or the performance.</p>

    <div class="sig-row">
      <div>
        <p class="sig-label">Director (Kiarash Jamshidi)</p>
        <div class="sig-line"></div>
      </div>
      <div>
        <p class="sig-label">Date</p>
        <div class="sig-line"></div>
      </div>
    </div>
  </section>

  <footer class="foot">
    <p><strong>Village Players · Lausanne</strong> &nbsp;·&nbsp; Director: Kiarash Jamshidi</p>
    <p>This is a contract. Two signed copies are produced for every performer — one for the performer, one for the production archive.</p>
  </footer>

</main>

</body></html>
"""

HTML_PATH = OUT_DIR / "intimacy_protocol.html"
HTML_PATH.write_text(HTML)

OUT = OUT_DIR / "intimacy_protocol.pdf"
with sync_playwright() as p:
    launch_kwargs = {"executable_path": CHROMIUM} if CHROMIUM else {}
    browser = p.chromium.launch(**launch_kwargs)
    page = browser.new_page()
    page.goto(f"file://{HTML_PATH.resolve()}", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(600)
    page.pdf(path=str(OUT), format="A4",
             margin={"top":"22mm","right":"22mm","bottom":"22mm","left":"22mm"},
             print_background=True, prefer_css_page_size=True)
    browser.close()

try:
    from pypdf import PdfReader
    r = PdfReader(str(OUT))
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes) · {len(r.pages)} pages")
except BaseException:
    print(f"Done: {OUT} ({OUT.stat().st_size:,} bytes)")
