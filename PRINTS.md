# Prints

Live at **thehelpingsun.com/prints** — 24 photographs, lightbox, pricing, and
the story of what the money does.

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

## You'll need a seller's permit

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

## Fulfilment — Bay Photo, Scotts Valley

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

The site currently lists:

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

**Now:** no cart. Buyers email, you reply with a **Stripe Payment Link** —
free to create, no monthly fee, works from your phone. Perfectly respectable
at this volume and it keeps the conversation human.

**Later, if volume justifies it:** Pixieset, SmugMug or Shopify will give you a
real store with automatic Bay Photo fulfilment. Don't pay a monthly fee until
prints are selling without you chasing them.

## What to track

One number: **how much of the running costs prints have covered this month.**

Insurance, the phone, petrol for rides, the Helping Hand fund. When prints
cover all of it, the support is genuinely self-sustaining and you never have to
weigh whether you can afford to answer someone.

Put that number in Golden Hour occasionally. Not as a sales pitch — as an
accounting. *"Three prints sold this month, which covered insurance and two
tanks of petrol."* People who bought one will want to know what it did.

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

and regenerate `site/prints.html` from the manifest the same way it was built.
Originals live in Google Drive; only the web sizes are tracked here.

## One caution

Your photographs are the most personal thing on this site, and the archive is
evidence that you got up on hard mornings. Selling them is right — it funds the
work and it values your own labour, which you are not naturally inclined to do.

But don't let the gallery become the business. The number that matters is still
how many people reached out, not how many prints moved.
