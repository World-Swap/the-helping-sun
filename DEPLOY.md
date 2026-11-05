# Putting the site on thehelpingsun.com

Free, about fifteen minutes, no build step. The site is plain HTML, so there's
nothing to compile — Cloudflare just serves the `site/` folder.

One useful thing already true: `claude/adoring-hypatia-us33gp` is the repo's
**default branch**, so Cloudflare will select it as the production branch on its
own. You don't need to merge anything first.

---

## Step 1 — Connect the repo

1. Go to **dash.cloudflare.com** and sign in.
2. In the left sidebar: **Compute (Workers & Pages)** → **Create** → the
   **Pages** tab → **Connect to Git**.
3. Authorize Cloudflare for GitHub if it asks. When GitHub offers
   *All repositories* or *Only select repositories*, pick **Only select
   repositories** and choose **World-Swap/the-helping-sun**.
4. Select the repo, then **Begin setup**.

## Step 2 — Build settings

This is the only screen where a wrong answer causes trouble. Set:

| Field | Value |
| --- | --- |
| Project name | `the-helping-sun` (becomes `the-helping-sun.pages.dev`) |
| Production branch | `claude/adoring-hypatia-us33gp` |
| Framework preset | **None** |
| Build command | **leave completely empty** |
| Build output directory | `site` |

> ⚠️ `site` is the one that matters. Point it at the repository root instead and
> you'll get a 404, because `index.html` lives inside `site/`.

Click **Save and Deploy**. It finishes in under a minute and gives you a
`.pages.dev` address. **Open it and confirm the site looks right before moving
on** — it's much easier to debug now than after DNS is involved.

## Step 3 — Attach thehelpingsun.com

1. In the project: **Custom domains** → **Set up a domain**.
2. Enter `thehelpingsun.com` → **Continue**.

**If the domain is registered at Cloudflare** (most likely, since you mentioned
Cloudflare): it adds the DNS record itself. Click **Activate domain** and you're
done. Live in a minute or two, sometimes up to an hour.

**If it's registered somewhere else** (GoDaddy, Namecheap): the simplest route
is to move the domain's **nameservers** to Cloudflare — Cloudflare shows you the
two to use, and you paste them into the registrar's nameserver settings. This is
free, you keep ownership, and it makes the root domain work properly. A plain
CNAME can't be used on a root domain at most registrars, which is why the
nameserver route is worth the extra ten minutes.

## Step 4 — Add the www version

Repeat Step 3 with `www.thehelpingsun.com`. Cloudflare will serve the same site
at both. If you'd rather have one canonical address, go to **Rules** →
**Redirect Rules** and send `www` to the root domain with a 301.

HTTPS is automatic on both. No certificate to buy or renew.

---

## Publishing changes later

Every push to `claude/adoring-hypatia-us33gp` redeploys automatically, usually
within a minute. To edit text without touching a terminal, you can open
`site/index.html` on github.com, click the pencil icon, make the change, and
commit — Cloudflare picks it up the same way.

Every deploy keeps its own permanent preview URL, so a bad edit is never
unrecoverable. **Deployments** → find a previous one → **Rollback**.

## If something goes wrong

| What you see | Cause |
| --- | --- |
| 404 on the home page | Build output directory isn't `site` |
| Site loads, photos don't | The `site/img/` folder didn't get committed |
| Domain shows a Cloudflare error page | DNS hasn't finished; wait, then hard-refresh |
| Old version keeps appearing | Browser cache — try a private window |

## One thing to do once it's live

Set up a free uptime check (UptimeRobot, Better Stack) pointing at
`https://thehelpingsun.com`. If someone in a bad moment reaches a dead site,
you want to be the first to know, not the last.
