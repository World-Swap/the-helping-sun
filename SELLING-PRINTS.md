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

## If uploads are rejected as the wrong file type

Your phone writes an **APP4 segment** into every JPEG — a Samsung vendor block,
alongside ICC and XMP. The files are valid, but a strict uploader that sniffs
the format can trip over the unexpected marker and report it as a bad file
type. That is why the error names file extensions you are already using, and
why its two lists of "acceptable" formats disagree with each other.

The fix is to re-encode clean:

```bash
python3 tools/make-upload-files.py
```

That writes `faa-upload/` — every selected photograph at full resolution,
plain baseline sRGB JPEG, rotation baked in, **every marker stripped**, numbered
in gallery order with readable names (`001-first-light.jpg`). Largest file is
3.2 MB against their 25 MB limit.

These files are also simply better to sell: 4000 px on the long edge, 4:4:4
chroma, no compression artefacts from a second round of phone processing.

## Setup — about an hour, once

**1. Open the account.** `fineartamerica.com/sell-art-online`. Free, no card.

> **You upload photographs, never products.** Their words: *"Create hundreds
> of products in seconds from a single image upload. Our technology
> automatically positions your design onto each available product."* One JPEG
> becomes the canvas, the mug, the tote and the phone case. You then *"choose
> which products you want to sell and for how much."*

**2. Set your markups.** This is the step that decides whether the thing is
actually hands-off, so do it before you upload a pile of images.

What their site states plainly:

> *"We set a base price for each product that can be manufactured by our
> fulfillment partners, and then you add a markup on top of that base price."*
> …and *"you can change them at any time."*

**What I could not verify:** the exact menu path, or whether a markup you set
once is inherited by later uploads. Their FAQ and help pages are both 404 and
the control panel is behind the login, so anyone telling you the precise
button name without an account is guessing.

When you're in, look for pricing controls that apply across images rather than
to one — wording like "all images", "defaults", or a copy/apply-to-all option
on the pricing screen. Nearly every platform of this type has one, because the
alternative is unusable at 96 images. **Confirm it exists before you upload in
bulk.** If it turns out there's no apply-to-all, that changes the plan — tell
me and we'll rethink, because pricing 96 images by hand is not automation.

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

### It's switched on

`FAA_STORE` is set to `https://ian-sun.pixels.com/` in both
`site/index.html` and `site/prints.html`. **Buy a print** appears in every
lightbox across all 98 photographs, and the prints section links to the shop
directly. Email ordering and the price table are gone.

The button says **Buy a print** rather than *Buy this print*, because it goes
to the storefront rather than that specific photograph. Only 18 of 98 are
listed so far, so the site says plainly that the shop is filling up and invites
people to ask for anything missing.

To deep-link an individual photograph once it is listed, add an `faa` field to
its entry in the manifest — **only using a URL you have actually opened.**

The mapping lives in `faa-links.json`, built by reading the live storefront
index and matching slugs against the gallery manifest — never by predicting a
URL from a title. `tools/make-gallery.py` copies it into the manifest, and
`tools/build-prints-page.py` writes it onto each figure as `data-faa`. A
photograph with a link gets a **Buy this print** button straight to its own
product page; everything else gets **Buy a print** to the shop front. All 25
current links were opened and returned 200 on 19 November 2026.

Run `python3 tools/match-storefront.py` after every batch of uploads. It reads
the live index, requests each product page, and drops any that does not answer
200 — a dead *Buy this print* button is worse than no button.

A listing you rename during upload cannot be matched on its title, so record it
in `faa-manual.json` by upload number (the `001-` prefix on the file you sent
up). Keying on the number means neither a new site title nor a new shop title
breaks the link. Note that the storefront index page showed only 24 of the 25
listings, so trust the script over the index.

---

## The site now points everything at the shop

Done. The price table, the Bay Photo mention and email ordering have all been
removed from the site — every route to buying goes through the storefront.

That means the sales-tax position is the simple one: the platform is the
retailer and handles it. **Sell one print directly and that changes**, so if
you ever do a local sale, read the tax section above again first.

---

## You will get fake buyer emails

Within days of listing, expect messages like: vague praise, no photograph
named, first name only, "interested in acquiring few of your artworks". The
script is always the same — they agree without asking the price, insist on
their own shipper, then send a check for too much and ask you to forward the
difference. The check bounces weeks later and the bank takes it back out of
your account.

A second wave offers large sums in cryptocurrency to mint your work as NFTs
for an "exhibition", and asks whether you have any experience with NFTs. That
question is the whole email. What follows is a platform charging minting, gas
or verification fees, or a wallet connection that drains it.

`REPLIES.md` has templates that answer both warmly and route everything to
the shop. It costs nothing if they're genuine and gives them nothing if
they're not.

**This is the strongest argument for selling through a platform.** The money
never passes through your hands, so the overpayment fraud has nothing to
attach to.

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
2. Check the pricing screen for an apply-to-all control, and set markups
3. Upload the 25 named works
4. Paste the storefront URL into `FAA_STORE` and push
5. Sell something
6. Then, and only then, pay the $30 and upload the other 71
