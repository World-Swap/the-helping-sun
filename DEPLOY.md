# Putting the site on thehelpingsun.com

The site is plain HTML with no build step. Cloudflare just needs to be told
which folder to serve.

## Important: this is a Worker, not a Pages project

When you connect a Git repo today, Cloudflare creates a **Worker** (with
Workers Builds), not a Pages project. You can tell from the dashboard: it shows
**Bindings**, **Workers Logs**, a `*.workers.dev` subdomain, and a **Deploy
command** of `npx wrangler deploy`.

That matters because a Worker doesn't have a "build output directory" setting.
It runs `npx wrangler deploy`, and wrangler reads **`wrangler.toml`** in the
repo root to learn what to publish. Without that file it deploys an empty
Worker, the build goes green, and the URL shows nothing.

`wrangler.toml` is committed to this repo and does exactly one job:

```toml
name = "the-helping-sun"
compatibility_date = "2026-11-01"

[assets]
directory = "./site"
```

No `main` entrypoint, because there's no server-side code. The `[assets]`
block is what makes the deploy publish `site/`.

> If you rename the Worker in the dashboard, change `name` here to match.

## The dashboard settings

With `wrangler.toml` in place, these are correct as-is. Confirm under
**Settings → Builds**:

| Field | Value |
| --- | --- |
| Production branch | `claude/adoring-hypatia-us33gp` |
| Build command | **empty / None** |
| Deploy command | `npx wrangler deploy` |
| Root directory | `/` |

Root directory stays `/` — that's where `wrangler.toml` lives. The config
points at `site/` from there. Setting root directory to `site` would break it,
because wrangler would no longer find the config.

## Custom domain

Already done: `thehelpingsun.com` is attached under **Domains**. Because the
domain is on Cloudflare, the DNS record was created automatically.

Add `www.thehelpingsun.com` the same way if you want both. To make one
canonical, use **Rules → Redirect Rules** and send `www` to the root with a 301.

HTTPS is automatic. Nothing to buy or renew.

## Publishing changes

Push to `claude/adoring-hypatia-us33gp` and it redeploys, usually within a
minute. To edit text without a terminal, open `site/index.html` on github.com,
click the pencil, and commit — same result.

Every deploy is kept. **Deployments** → pick an earlier one → **Rollback**.

## Testing a deploy before pushing

```bash
npx wrangler deploy --dry-run
```

It should print `Read N files from the assets directory`. If N is 0 or it
errors, the deploy will produce a blank site.

To preview locally exactly as Cloudflare will serve it:

```bash
npx wrangler dev
```

## Troubleshooting

| What you see | Cause |
| --- | --- |
| Build green, URL blank or "not found" | No `wrangler.toml`, or `[assets] directory` points somewhere wrong |
| `Deployment failed: name` | `name` in `wrangler.toml` doesn't match the Worker |
| Site loads, photos don't | `site/img/` wasn't committed |
| Old version keeps appearing | Browser cache — try a private window |
| Domain shows a Cloudflare error | DNS still propagating; wait, then hard-refresh |

## Once it's live

Set up a free uptime check (UptimeRobot, Better Stack) on
`https://thehelpingsun.com`. If someone in a bad moment hits a dead site, you
want to be the first to know rather than the last.
