# Prints

**The homepage leads with the photography now.** The gallery and the sales
floor come first; the support story is the *why* underneath it.

| Page | What's on it |
| --- | --- |
| **thehelpingsun.com** | Hero, 12 featured photographs, **sizes and prices**, what the money pays for, then the story and the support |
| **thehelpingsun.com/prints** | The Archive — all 24 photographs with a lightbox, linking back to the homepage for pricing |

**Prices live in one place only: the `#prints` section of `site/index.html`.**
The archive page links to it rather than repeating it, so the two can't drift
apart.

The model in one line: **people buy a photograph, and the margin keeps the
support free.**

---

## The framing rule — read this before writing any caption

There's a meaningful legal difference between these two sentences:

| | |
| --- | --- |
| ✅ **"Prints pay for the free support I offer."** | You're selling a product and spending the profit on your own operations. Ordinary business. |
| ❌ **"Proceeds go to charity."** / "A portion benefits those in need." | This is a **charitable sales promotion**. In California it brings registration and disclosure obligations, and you'd be representing that a charity benefits when none does. |

The site copy already does this correctly — *"you're not donating to a
charity, you're buying a photograph, and the margin keeps somebody's First
Light call free."* **Keep that framing everywhere**: captions, Instagram, the
newsletter, replies to buyers.

This isn't pedantry. Say "proceeds go to charity" on an Instagram post and
you've made a representation you can't back, about the one subject where your
credibility is the entire asset.

> **Update:** if everything sells through Fine Art America, you probably do
> **not** need a seller's permit — they are the retailer and handle the tax.
> See `SELLING-PRINTS.md`. The section below applies to **direct** sales only.

## For direct sales, you'll need a seller's permit

Prints are tangible goods. California requires a **seller's permit from CDTFA**
for anyone regularly selling physical products, and you collect sales tax on
California sales.

- **It's free.** Apply online at `cdtfa.ca.gov`.
- One source cites a threshold of three or more sales in twelve months; truly
  occasional sales may not require one. You'll pass that quickly.
- Keep records of every sale. CDTFA expects you to be able to show them.
- Out-of-state buyers: you only owe tax in states where you've hit economic
  nexus thresholds, which you won't be close to. California is what matters.

Sort this before the first order, not after the tenth.

## Fulfilment — not currently used

> **Superseded.** All sales now go through Fine Art America, which prints and
> ships. See `SELLING-PRINTS.md`. Keep this only if you ever want to print
> locally for a direct, in-person sale.

### Bay Photo, Scotts Valley

**920 Disc Drive, Scotts Valley, CA 95066** — Santa Cruz County, roughly
fifteen minutes from where most of these were taken.

They do **white-label drop shipping**: they print it, they ship it straight to
your buyer, and the box doesn't say Bay Photo. You hold no stock and front no
money. Some integrations even let you put your own label on the outer box.

The fact that the prints are made in the same county as the photographs is a
genuinely good line. Use it.

**Set up:** open a pro account at `bayphoto.com`, pull their current price
list, and order **one print of your best image for yourself first.** Never sell
a product you haven't held.

## Pricing

> **Superseded.** Prices are set in the shop now, per product, and the site
> no longer lists a table. Kept for reference if you ever sell direct.

The site previously listed:

| Size | Material | Price |
| --- | --- | --- |
| 8 × 12″ | Archival lustre | $45 |
| 12 × 18″ | Archival lustre | $85 |
| 16 × 24″ | Archival lustre | $140 |
| 16 × 24″ | Metal | $225 |
| 24 × 36″ | Metal | $340 |

These are plausible market prices for signed work by a local photographer, but
**check them against Bay Photo's actual costs before you take an order.** The
rule of thumb is lab cost × 3 to 4, which covers shipping, Stripe's cut
(2.9% + 30¢), sales tax, and leaves a real margin.

If a size comes out underwater, raise the price rather than shrink the margin.
Nobody buying a sunrise to hang in their house is price-shopping to the dollar,
and an underpriced print that funds nothing defeats the entire point.

## Taking payment

> **Superseded.** The shop takes payment. Below applies only to direct sales.

**Hands-off (recommended):** Fine Art America. Free for 25 images, $30/year
for all 96. They print, ship, take payment and handle support — see
`SELLING-PRINTS.md` for the full setup.

**Direct, for local or bespoke orders:** buyers email, you reply with a
**Stripe Payment Link** — free, no monthly fee, works from your phone. Better
margin, and it keeps the Bay Photo story, but you do the work.

## What to track

One number: **how much of the running costs prints have covered this month.**

Insurance, the phone, petrol for rides, the Helping Hand fund. When prints
cover all of it, the support is genuinely self-sustaining and you never have to
weigh whether you can afford to answer someone.

Put that number in Golden Hour occasionally. Not as a sales pitch — as an
accounting. *"Three prints sold this month, which covered insurance and two
tanks of petrol."* People who bought one will want to know what it did.

## Location data does not survive the trip to me

**Corrected twice, 19 November 2026.** This file first said location tagging
was off in the camera. Then it said Google Drive was stripping it. Both were
wrong, and Ian disproved each one.

What is actually established:

- His phone's gallery shows these photographs on a map, reading the file at
  `/Internal storage/DCIM/Camera`. **The originals on the phone have
  coordinates.**
- Of 153 originals pulled from Drive, 150 carry a GPS block that is present
  but zeroed, 3 carry none. Real coordinates: zero.
- A photograph **uploaded straight into the chat, never touching Drive**,
  arrived with the same zeroed block.

So the data is lost somewhere between the phone's storage and this session,
on every route tried. Which step empties it is not established and should not
be guessed at again - it could be the Android share sheet, Samsung Gallery's
sharing behaviour, or the chat upload itself. Three guesses have now cost
more than the answer is worth.

**The practical consequence: do not try to recover location from a file.**
Read it off the phone instead - open the photograph in Gallery, swipe up or
tap Details, and the place is written there under the map. Telling me "132 is
Natural Bridges" is faster than any amount of metadata archaeology, and it is
the only source that has actually proved reliable.

**It does not leak to buyers.** `tools/make-upload-files.py` strips every
metadata block before upload, coordinates included. You get accurate titles
for your own records; the public file carries nothing.

Worth doing before the next morning you go out.

## Adding or changing photographs

Edit the `PICKS` list in `tools/make-gallery.py` — each entry is a filename,
a slug, a title, a date and a place — then:

```bash
python3 tools/make-gallery.py
```

It handles EXIF rotation and writes both sizes plus the manifest. Then rebuild
the page:

```bash
python3 -c "import runpy; runpy.run_path('tools/make-gallery.py')"
```

```bash
python3 tools/build-prints-page.py
```

That rebuilds the archive page from the manifest. The 12 featured photographs
on the homepage are the first 12 in the manifest — reorder `PICKS` to change
which ones lead. Originals live in Google Drive; only the web sizes are tracked
here.

## One caution

Your photographs are the most personal thing on this site, and the archive is
evidence that you got up on hard mornings. Selling them is right — it funds the
work and it values your own labour, which you are not naturally inclined to do.

But don't let the gallery become the business. The number that matters is still
how many people reached out, not how many prints moved.
