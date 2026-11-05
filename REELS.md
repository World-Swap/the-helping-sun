# Reels

Five vertical videos in `reels/`. **1080×1920, 9:16, 30fps, H.264** — full
screen on Instagram Reels, Facebook Reels, TikTok and YouTube Shorts with no
bars and no cropping.

All footage is Ian's own Santa Cruz photography. Each one is a slow push in on
a single frame with the text timed over it.

## Sound

They ship with a **silent audio track** so every platform accepts the file.
Add music inside the app, not here — Instagram only counts a track as
"trending" and surfaces the reel to non-followers when the audio is picked
from their own library. Pick something quiet. These are not hype videos.

For reel 04 especially: consider no music at all. Silence suits it.

---

## 01 · `01-ask-well.mp4` — 11s
*Sunrise over Walton Lighthouse.* The launch reel. Post this one first.

**Caption**
```
I spent most of my life depressed, broke, and too embarrassed to tell anyone.

I got very good at looking fine. That's the part nobody warns you about — if
you're good at it, people genuinely cannot tell, and the first move ends up
being yours. That's unfair. It's also true.

The Helping Sun is me, answering. Not therapy, and I'm not a therapist.
For people carrying something heavy who can't ask for help nicely.

Three words is enough.

thehelpingsun.com — link in bio.
If this isn't for you, send it to someone it is for.

In crisis right now? Call or text 988.
```

## 02 · `02-light-before-noon.mp4` — 11s
*The October morning sky.* The most shareable of the five — it asks nothing
of anyone and helps immediately.

**Caption**
```
One small thing, and it's free: ten to twenty minutes of outdoor light before
noon.

Not a sun lamp. Not through a window. Outside — and an overcast morning still
beats your brightest indoor room by a mile.

Nobody is telling you a walk fixes depression. It measurably helps with sleep
and mood, it costs nothing, and it asks almost nothing from you on a day when
you have almost nothing.

You don't even have to walk. Stand in a doorway with a coffee.

988 if today is bad.
```

## 03 · `03-the-word-is-hardship.mp4` — 12s
*Crimson over the rivermouth.* Money shame is the quietest of the three and
this is the single most useful thing on the whole account.

**Caption**
```
If you can't pay a bill, the word is HARDSHIP.

Almost every lender, card issuer and utility has a hardship or forbearance
program. Almost none of them will mention it first. You have to say the word.

Call the number on the statement:
"I'm having trouble making my payments. I want to stay current. What hardship
options do you have?"

Then ask: Will this show on my credit report? Does interest keep adding up?
Can you email that to me? Can I get your name and a reference number?

You don't have to explain your whole life. "I need to think about it" is a
complete sentence.

I avoided a phone call for eleven weeks once. The call took nine minutes.

If the call is the part you can't do, I'll sit on the line while you make it.
Free. Link in bio.
```

## 04 · `04-when-someone-says.mp4` — 14s
*Boardwalk lights after dark.* **Pin this one.** The most important thing on
the account.

**Caption**
```
What to say when someone tells you they want to die. Most people freeze.

Ask directly: "Are you thinking about killing yourself?" Say the words.
Asking plainly does not plant the idea — this is one of the most studied
things in the field. Avoiding it is what loses the thread.

Then: "I'm glad you told me." "I'm not going anywhere."
Not advice. Not perspective. Not "think of your family." Just stay.

Don't promise secrecy. Say it up front: "If I think you're about to die, I'm
going to get other people involved."

If there's a plan, a method at hand, or a timeline — stay with them and call
988 together, or 911 if it's immediate. Don't leave to go find help.

Tomorrow, follow up. In writing. That's the part almost everyone skips and
it's the part that proves the first conversation was real.

988 — call or text, 24/7
741741 — text HOME

Save this. You will need it one day for someone you love.
```

## 05 · `05-sunrise-log.mp4` — 12s
*Four mornings, cross-fading.* The brand thesis in twelve seconds.

**Caption**
```
I started photographing sunrises on the mornings that were hardest to start.

The photo isn't the point. The proof is. On a bad day the whole job is getting
outside once and pressing a button.

These are all mine, all Santa Cruz. There are a hundred more.

If you're up early and it's bad: go outside for ten minutes. It is not a cure.
It helps.

988 if you need it.
```

---

## Posting notes

**Order.** 01 first. Then 02, then 03. Hold 04 until you've posted at least
three times — it's the heaviest and it lands better on an account that already
has a voice. 05 whenever you want a quiet day.

**Cover frame.** Instagram lets you choose the cover from any frame. Pick one
from the first second, before the text fades in, so the grid stays photographs
rather than words.

**Hashtags.** Put them in the first comment, not the caption. Keep it to five
or six and keep them real: `#santacruz #mentalhealth #depression
#peersupport #moneyshame #988`. Avoid the giant generic ones — reach from
them is worthless and the audience is wrong.

**Every reel that touches crisis carries 988 in the caption.** No exceptions.

**Pin a comment** with 988 / 741741 / 211 on 01, 04 and 05 the moment you post.

**Don't post 04 and then go to bed.** It will bring replies. Post it on a
morning when you have the day.

## Making more

`tools/make-reels.js` holds the definitions. Each reel is a photo, a position,
and a list of timed cards. Add a new entry and run:

```bash
node tools/make-reels.js
```

Text style options are `big` (Newsreader display), `body`, `mono` (small caps
label) and `gold` (the 988 / emphasis treatment). Text is kept inside a safe
area clear of Instagram's own buttons on the right and the caption at the
bottom.
