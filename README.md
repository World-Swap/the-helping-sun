# The Helping Sun

Website and launch materials for **thehelpingsun.com** — peer support for
people carrying hard things, by Ian Sun. Santa Cruz, California.

## What's here

| File | What it's for |
| --- | --- |
| `site/` | The website. Static HTML — no build step, no dependencies. |
| `site/img/` | Web-optimised photographs (Ian's own, from the Drive folder) |
| `BRAND.md` | Palette, type, voice, naming, the Sunrise Log concept |
| `LAUNCH-PLAN.md` | Entity structure, 90-day plan, how this makes money |
| `CONTENT.md` | Social strategy, the five pillars, platform choice |
| `POSTS.md` | **The launch post and 30 days of content, written and ready to post** |
| `DEPLOY.md` | Step-by-step Cloudflare setup for thehelpingsun.com |
| `EMAIL.md` | Setting up hello@thehelpingsun.com, and why SPF/DKIM matter here |
| `NEWSLETTER.md` | **Golden Hour: the welcome email, issue 01, and the repeatable template** |
| `SOCIAL-PROFILES.md` | **Bios, About copy, categories and images for Instagram and Facebook** |
| `SAFETY-AND-LEGAL.md` | **Read this first.** Scope of practice, crisis protocol, insurance, burnout |
| `tools/prep-photos.py` | Turns new full-res photos into web-ready sizes |

## Fill these in before launch

Search the repo for each:

- Social handles are live: Instagram `@the_helping_sun`, Facebook `thehelpingsun`
- ~~`hello@thehelpingsun.com`~~ — done: live, authenticated, 10/10 on mail-tester
- ~~County crisis line~~ — done: 1-800-952-2335, in the protocol and the site footer
- `Opening early 2027` / `Santa Cruz County first` — adjust the Circle and
  Helping Hand timing to what's true
- The story in the "Who's behind this" section is a **draft in your voice**.
  Rewrite it until it's actually yours. It's the most important text on the site.

## Running it locally

```bash
cd site && python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Deploying to thehelpingsun.com

**Full step-by-step walkthrough in `DEPLOY.md`.** Short version:

1. Push this repository to GitHub.
2. Create a site on **Cloudflare Pages** or **Netlify**, point it at the repo,
   and set the publish directory to `site`. No build command.
3. Add `thehelpingsun.com` as a custom domain and update the nameservers or
   DNS records where the domain is registered.
4. HTTPS is automatic on both.

## Wiring up the form

**Current behaviour:** the form has no backend. On submit it composes the
message and hands off to the visitor's own email app with everything
prefilled, then shows them the address as a fallback. Nothing is stored
anywhere in between, and **the page never tells anyone their message was
received when it wasn't.**

That last part is the rule. A support site that says "I'll come back to you
within a day" and then drops the message is worse than having no form at all.

### To take submissions in the background instead

1. Create a free form at [Formspree](https://formspree.io) (50/month free) or
   [Basin](https://usebasin.com). Point it at `hello@thehelpingsun.com`.
2. In `site/index.html`, find `var ENDPOINT = '';` near the top of the script
   and paste the URL in:

```js
var ENDPOINT = 'https://formspree.io/f/YOUR_ID';
```

Nothing else changes. The page switches to a real background submit, shows the
original "That took something, thank you" confirmation, and **falls back to the
email hand-off automatically if the request fails** — so a network error still
can't swallow someone's message.

⚠️ Submissions will contain some of the most sensitive information anyone
sends you. Turn on two-factor authentication on whichever service you choose,
and read `SAFETY-AND-LEGAL.md` §6 first. The no-backend hand-off above is
actually the most private option, since no third party ever holds the message.

## Adding new sunrise photos

Drop full-resolution files into `photos/original/`, then:

```bash
python3 tools/prep-photos.py
```

It writes resized, compressed versions into `site/img/` and prints the dominant
colours of each photo, so the palette can keep coming from real pixels. Add the
new entries to the Sunrise Log list in `site/index.html`.

Originals aren't tracked in git — they live in the Drive folder.

## Accessibility and browser notes

- Works at 390px phone width through desktop; no horizontal scrolling.
- Light and dark themes both defined; follows the visitor's system setting.
- Crisis resources appear at the top of every page and again in the footer,
  and are plain text — never behind a tap or an expander.
- Respects `prefers-reduced-motion`.
