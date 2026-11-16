# Selling the prints, hands-off

The goal: somebody sees a photograph, picks whatever they want it printed on,
pays, and it arrives — with you doing nothing. No stock, no packing, no trips
to the post office, no customer emails about delivery.

**Recommendation: Fine Art America** (same company as Pixels.com).

---

## Why this one

Everything else in this category is a *supplier* — Printful, Printify, Gelato,
Prodigi. They print and ship, but you still have to run a shop: Shopify at
$39/month, or Etsy listing fees, plus building 96 photographs × 20 products
into thousands of listings and keeping them in sync.

Fine Art America is the shop **and** the supplier. You upload one image; every
product is generated from it automatically. You never create a listing.

Verified on their membership page today:

| | |
| --- | --- |
| **Free tier** | $0. Limited to **25 images** |
| **Premium** | **$30/year**. Unlimited images, plus a white-label website |
| **Who prints and ships** | They do — 14–16 facilities across 5 countries, routed to whichever is nearest the buyer |
| **Who takes payment** | They do |
| **Who handles returns and support** | They do |
| **What you earn** | *"We set a base price... then you add a markup on top of that base price. Whatever you set as your markup — that's exactly how much you'll earn on the sale."* |

**They take no percentage of your markup on prints.** Their money is in the
base price. Their example: $50 base on a 24×36 canvas, you add $25, buyer pays
$75, you get $25.

## What a buyer can put a photograph on

Prints, posters, canvas, framed, metal, acrylic, wood, tapestries · greeting
cards, spiral notebooks, stickers · iPhone and Galaxy cases, battery chargers ·
throw pillows, duvet covers, shower curtains, bath and hand towels, fleece
blankets, coffee mugs · tote bags, weekender bags, carry-all pouches, beach
towels, yoga mats, jigsaw puzzles, ornaments · t-shirts, tank tops,
sweatshirts, baby one-pieces · plus digital downloads.

You choose which product types to enable. You don't have to offer yoga mats.

---

## The sales-tax consequence, which is good news

Earlier I told you to get a **CDTFA seller's permit** before selling prints.
**If you sell only through Fine Art America, you probably don't need one.**

They are the retailer — they take the payment, so they are the *marketplace
facilitator* and they collect and remit the sales tax. You are not selling
tangible goods to the public; you are receiving a markup. California's own
guidance says that where a registered marketplace facilitator handles all your
sales, a seller's permit isn't required.

**This flips the moment you sell one print directly** — a friend, a local
market, an invoice you send yourself. Then you are the retailer for that sale
and the permit applies.

So: pick a lane. All sales through the platform = no permit, no sales-tax
admin. Mixed = get the permit. Confirm with CDTFA before the first direct sale.

Your earnings still count as business income. Expect a 1099 and report it.

---

## Setup — about an hour, once

**1. Open the account.** `fineartamerica.com/sell-art-online`. Free, no card.

**2. Set your default markups before uploading anything.** This is the step
that makes it automatic: set them once and every future upload inherits them.
Don't price image by image — you'll never keep up.

A sane starting point, given they take nothing from your markup:

| Product | Markup |
| --- | --- |
| Small prints (8×10 and under) | $15–20 |
| Larger prints | $30–50 |
| Canvas and metal | $40–75 |
| Mugs, totes, cases, pillows | $8–12 |
| Greeting cards | $3–5 |

Check the final buyer price on a few before you commit. If a mug lands at $38,
your markup is too high for the product.

**3. Upload.** Free tier: your best 25 — the named works in the gallery are
already that selection. Premium at $30/year: upload all 96.

**4. Title and keyword each one as you upload.** Keywords are the only way
anyone finds you inside their marketplace — "Santa Cruz", "Boardwalk",
"sunrise", "Monterey Bay", "California coast", "lighthouse". Use the same
titles as the site so the two stay recognisable.

**5. Enable the product types you actually want.**

**6. Set up payment.** They pay monthly on sales above a threshold.

---

## How your site connects

Two ways, and you can run both.

### A. One link (works immediately, zero maintenance)

A **Buy prints** button pointing at your Fine Art America storefront. Visitors
browse there, pick any photo, any product. Nothing to keep in sync, ever.

### B. Per-photograph deep links (better conversion)

Their product URLs are predictable:

```
https://fineartamerica.com/featured/{title-slug}-ian-sun.html
```

So "First Light" becomes `.../featured/first-light-ian-sun.html`.

The site is already built for this. Each photo in the manifest can carry an
`faa` slug; where one exists, the lightbox shows **Buy this print →** going
straight to that photograph's product page. Where it doesn't, the button falls
back to the storefront.

⚠️ **Only deep-link a slug you've actually opened and confirmed.** Fine Art
America appends numbers when titles collide, and 60+ photographs called
"Sunset" will collide. Verify, don't predict — the same mistake as inventing a
location for a photograph.

### Switching it on

In `site/index.html`, near the top of the script:

```js
var FAA_STORE = '';   // paste your storefront URL here
```

Fill that in and the Buy buttons appear across the site automatically. Leave it
empty and everything stays as it is now, with ordering by email. Nothing
half-finished goes live.

---

## What to change on the site once it's live

The price table in the prints section is for **direct** orders. Once the shop
is running, either:

- **Keep both** — the table for direct/local sales, the shop for everything
  else. More money per direct sale, but you handle those yourself and the
  seller's permit applies.
- **Point everything at the shop** — replace the table with "every size and
  product, from $X". Entirely hands-off, slightly less per sale.

**For a system you don't want to think about: point everything at the shop.**

---

## The honest trade-offs

**It isn't quite free.** $0 gets you 25 images. All 96 needs $30/year. That's
one 8×12 print a year to cover it.

**Less per sale than printing locally.** Bay Photo direct would net you more.
But direct means you handle payment, packing, postage and complaints, and you
said you want to focus on the main project. The margin you give up is the
price of never thinking about it.

**Their marketplace is crowded.** Don't count on strangers finding you there.
Traffic will come from your own site, Instagram and the newsletter — the shop
is the checkout, not the marketing.

**You lose the Bay Photo story.** "Printed fifteen minutes from where it was
taken" is a genuinely good line you can't use for platform orders. Worth
keeping a direct option alive for anyone local who asks.

---

## Do this in order

1. Open the free account — $0, no card
2. Set default markups **before** uploading
3. Upload the 25 named works
4. Paste the storefront URL into `FAA_STORE` and push
5. Sell something
6. Then, and only then, pay the $30 and upload the other 71
