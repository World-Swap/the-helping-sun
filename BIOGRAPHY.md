# Biography — Ian Sun

Four lengths. Use whichever fits the box you're filling.

Everything here is true and nothing is padded with art-world language. If a
line doesn't sound like you, change it — this reads better in your voice than
in anyone else's.

**Rewritten 19 November 2026.** The old version was built on "a year, the same
few miles," and said the work was made "most often before sunrise." Neither
survived contact with the archive: it is now 18 months and 147 photographs,
some of them 120 miles inland, and there are **75 taken after 5pm against 19
before 8am**. The shape below is the real one.

---

## One line
*Photo credits, Instagram, email signature*

```
Ian Sun — photographer, Santa Cruz, California.
```

```
Ian Sun photographs the Monterey Bay coast, and whatever else makes him stop walking.
```

---

## Short — 60 words
*Pixels profile, gallery labels, anywhere with a small box*

```
Ian Sun was born in Hawaii and raised in Santa Cruz, California — two places
that teach you early what light does to water.

He started photographing sunrises because he needed a reason to get out of
bed. Eighteen months on it has widened: the coast, the redwoods, a lake two
hours inland, a rainbow over a canopy turning red.
```

---

## Medium — 160 words
*Artist statement, press, exhibition blurb*

```
Ian Sun was born in Hawaii and raised in Santa Cruz, California — two places
that teach you early what light does to water.

He started photographing sunrises because he needed a reason to get out of
bed. The photograph was never really the point; getting outside once and
pressing a button was.

Eighteen months and a hundred and forty-seven photographs later it has
changed shape. There are more evenings than mornings now, which is its own
kind of progress report. And it stopped being only the coast — mushrooms
after rain, storm surf on Christmas morning, sea stars at low water, a creek
running over pale rock a long way inland.

These are not expeditions. They are the record of someone who went outside
and looked.

Prints fund The Helping Sun, the free peer-support project Ian runs for
people carrying hard things. Buying a photograph keeps it free for someone
who can't afford to ask.
```

---

## Long — 320 words
*Website About page, feature pieces, grant and exhibition applications*

```
Ian Sun was born in Hawaii and raised in Santa Cruz, California — two places
that teach you early what light does to water.

He started photographing sunrises because he needed a reason to get out of
bed. That was during a long stretch of depression, and the photograph was
never really the point — getting outside once and pressing a button was. A
good number of these pictures are, quite literally, proof that he did.

Eighteen months and a hundred and forty-seven photographs later, the work has
changed shape twice over.

There are more evenings in it than mornings now, which is its own kind of
progress report: the dawn ones were a discipline, the dusk ones are a choice.
And it stopped being only the coast. Mushrooms on the forest floor after
rain. Storm surf on Christmas morning. Sea stars under a ledge at low water.
A rainbow standing in a flat grey sky over a canopy turning red. A creek
running clear over pale rock, a long way from any ocean. A city waterfront at
dusk, which is not his subject at all, photographed anyway because the light
was doing something.

Most of it is still made within a few miles of home on Monterey Bay — the
Beach Boardwalk and its ferris wheel, the San Lorenzo rivermouth where the
lagoon goes still enough to hold the whole sky, West Cliff Drive, Walton
Lighthouse on the jetty. But the frame has widened, and that is the honest
story of this body of work.

These are not expeditions. They are the record of somebody who went outside
and looked.

Prints fund The Helping Sun, a free peer-support project Ian runs for people
carrying hard things: their mental health, their physical health, their
money. He offers it free because nobody should have to work out whether they
can afford to ask. Buying a photograph is what keeps it that way.

Ian lives and works in Santa Cruz County.
```

---

## What changed, and why it matters

The old bio's spine was **"a year, the same few miles"** — a photographer who
kept returning to one stretch of coast until it gave something up. That was a
good story and it is no longer the true one.

**The new spine is the widening.** It started as one thing — a reason to get
up, pointed at one horizon — and became another: someone who now notices light
anywhere, including two hours inland and in a city he wasn't photographing.
That is a better story than the old one, and it is better because it is what
actually happened. Nobody needs it spelled out as a metaphor for recovery.
Leave it as a fact about the pictures and let people arrive on their own.

**The evening/morning count is worth keeping.** 75 after 5pm against 19
before 8am is a real detail, and the line it earns — *the dawn ones were a
discipline, the dusk ones are a choice* — is the best sentence here. It is
also checkable, which is why it works.

## How much of the personal story to include

**The short and medium versions work without it.** They stand on consistency
and range, which is a good artist story on its own.

**The long version names the depression openly**, because on your own site it
is already public, and it is the truest thing about how the work came to
exist.

For a **gallery submission or a corporate buyer**, use the medium version
without the final paragraph. For **your own site, press, or anyone asking what
The Helping Sun is**, use the long one. Nobody gets to tell you the personal
part is oversharing — it is the reason the photographs exist, and it is why
someone would rather buy from you than from a stock library.

## Keep these accurate

These numbers are in the text and they will drift:

- **147 photographs**, **18 months** (25 May 2025 to 19 November 2026)
- **75 after 5pm, 19 before 8am**

Re-run the count before you reuse the long version somewhere that matters:

```bash
python3 -c "
import json, datetime, collections
m = json.load(open('site/gallery/manifest.json'))
d = sorted(datetime.datetime.fromisoformat(x['iso']) for x in m)
h = collections.Counter(x.hour for x in d)
print(len(m), 'photographs |', d[0].date(), 'to', d[-1].date())
print('before 8am:', sum(v for k,v in h.items() if k<8),
      ' after 5pm:', sum(v for k,v in h.items() if k>=17))
"
```
