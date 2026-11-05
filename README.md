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
| `CONTENT.md` | Social strategy, the five pillars, first 30 days of posts |
| `SAFETY-AND-LEGAL.md` | **Read this first.** Scope of practice, crisis protocol, insurance, burnout |
| `tools/prep-photos.py` | Turns new full-res photos into web-ready sizes |

## Fill these in before launch

Search the repo for each:

- `hello@thehelpingsun.com` — set up the real mailbox, or change the address
- `@thehelpingsun` — claim the handles, or remove the footer links
- The county crisis line in `SAFETY-AND-LEGAL.md` §4 — currently blank
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

It's a static site, so hosting is free. Easiest path:

1. Push this repository to GitHub.
2. Create a site on **Cloudflare Pages** or **Netlify**, point it at the repo,
   and set the publish directory to `site`. No build command.
3. Add `thehelpingsun.com` as a custom domain and update the nameservers or
   DNS records where the domain is registered.
4. HTTPS is automatic on both.

## Wiring up the form

The "Reach out" form currently shows a confirmation and the email address, but
doesn't send anything anywhere. To make it deliver:

**Netlify** — add `netlify` and `name="ask"` to the `<form>` tag; Netlify
collects submissions automatically.

**Anywhere else** — create a form at [Formspree](https://formspree.io) or
[Basin](https://usebasin.com) (both have free tiers), then in the `<script>`
block at the bottom of `site/index.html`, replace the comment inside the submit
handler with:

```js
fetch('https://formspree.io/f/YOUR_ID', {
  method: 'POST',
  body: new FormData(form),
  headers: { Accept: 'application/json' }
});
```

Keep the `preventDefault()` and the confirmation panel exactly as they are, so
someone who reaches out always sees an acknowledgement even if the network
fails them.

⚠️ Form submissions will contain some of the most sensitive information anyone
will ever send you. Turn on two-factor authentication on whichever service you
choose, and read `SAFETY-AND-LEGAL.md` §6 before the form goes live.

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
