# Setting up hello@thehelpingsun.com

The site already tells people to write to `hello@thehelpingsun.com`. Right now
that address doesn't exist, so mail to it bounces. Fix that before launch.

## The thing to understand first

Two different jobs, and most free options only do one:

| | What it does |
| --- | --- |
| **Receiving** | Mail sent to you arrives somewhere you can read it |
| **Sending** | Your replies go out *from* hello@thehelpingsun.com |

**Cloudflare Email Routing is free and does receiving only.** It forwards mail
at your domain to an inbox you already have. It cannot send. If you reply, it
goes out from your personal Gmail address, which looks unprofessional and —
more importantly — hands your personal address to someone you may not want
having it.

So: Cloudflare is a good *stopgap*, not the answer.

## Recommended: Zoho Mail, free tier

A real mailbox. Sends and receives as `hello@thehelpingsun.com`. Costs nothing.

- Free forever, up to 5 users, 5 GB each, one custom domain, no card required
- Webmail and mobile app only — **no IMAP/POP** on the free tier, so you can't
  pull it into Apple Mail or Outlook
- Availability can vary by region

That missing IMAP sounds like a downside and is actually useful here: a
separate app you open on purpose, rather than crisis mail landing in the same
inbox as your receipts at 2 a.m. See `SAFETY-AND-LEGAL.md` §7 — your published
hours only mean something if there's a door you can close.

### Finding the free plan (Zoho hides it)

The plan chooser at `mailadmin.zoho.com/hosting` is the **upgrade** page for an
organization that already exists. It only shows paid plans, and there is no way
to reach the free tier from it.

The free plan is now called **Mail Free**. Use a direct signup link — the
`plan=free` parameter is what does the work:

```
https://mail.zoho.com/signup?type=org&plan=free
```

```
https://workplace.zoho.com/signup?type=org&plan=free
```

Different Zoho hosts; if one bounces you to pricing, try the other. Zoho's own
footnote says the free plan is "available only in select data centers", so it
may simply not be offered in your region.

**If it won't appear, buy Mail Lite: $1/user/month billed annually, $12/year,
and it includes IMAP** (the free tier does not). Don't lose an hour to a
signup funnel over $12 while the site points at a mailbox that doesn't exist.

⚠️ Zoho's FAQ: when you upgrade, **every user** is billed at that plan's rate,
not just the one you're upgrading. Keep it to the single `hello@` user.

### Steps

1. Sign up using one of the links above, and enter `thehelpingsun.com` as your
   domain.
2. Zoho gives you a **TXT record** to prove you own the domain. In Cloudflare:
   **DNS → Records → Add record**, type TXT, paste what Zoho gives you.
3. Back in Zoho, verify. Create the mailbox `hello`.
4. Zoho gives you **MX records** (usually `mx.zoho.com`, `mx2.zoho.com`,
   `mx3.zoho.com` with priorities 10/20/50). Add each in Cloudflare as an MX
   record. **Delete any MX records already there.**
5. Add the **SPF** and **DKIM** TXT records Zoho provides. Don't skip these —
   see below.
6. Turn on two-factor authentication. Not optional for this mailbox.

⚠️ **Cloudflare Email Routing and Zoho both want to own your MX records.** If
you turn on Email Routing first, disable it before pointing MX at Zoho, or
mail will go nowhere.

## If you want it inside Gmail instead

Cloudflare Email Routing forwards into Gmail, then Gmail's **"Send mail as"**
lets you reply from the custom address — but Gmail needs SMTP credentials from
somewhere, so you also need a free relay (SMTP2GO, Resend, Brevo). Three
services instead of one, and everything lands in your personal inbox.

Workable, but more to break, and worse for boundaries.

## If you'd rather pay

**Google Workspace Business Starter** — $7/user/month billed annually, $8.40
monthly, 30 GB. It's Gmail, which you already know, with full IMAP and no
5-user cap. Worth it once there's any money coming in.

**Fastmail** (~$5/month) and **Migadu** (~$19/year) are both good and more
privacy-minded than Google.

## Current status — verified 6 Nov 2026

Mailbox live on the Zoho free plan. Sending and receiving both confirmed.
mail-tester score **9/10**.

| | Record | Value |
| --- | --- | --- |
| ✅ | MX | `mx.zoho.com` (10), `mx2.zoho.com` (20), `mx3.zoho.com` (50) |
| ✅ | SPF | `v=spf1 include:zohomail.com ~all` |
| ✅ | DKIM key in DNS | selector `zmail`, published |
| ✅ | DMARC | `v=DMARC1; p=none; rua=mailto:hello@thehelpingsun.com` |
| ⚠️ | DKIM **signing** | key published but Zoho is not signing yet |

### The last point: turn DKIM signing on

Publishing the key and signing with it are two separate steps. The record is in
DNS; Zoho hasn't been told to use it.

Exact path, per Zoho's own documentation:

1. Sign in at **https://mailadmin.zoho.com**
2. Left menu → **Domains** → choose **thehelpingsun.com**
3. **Email Configuration** tab → **DKIM**
4. Click **Verify** on the row for the `zmail` selector
5. When asked, choose to **enable DKIM immediately**, and set the selector as
   **default**

Step 5 is the one people miss. Verifying alone does not start signing — the
selector has to be verified *and* enabled *and* default.

On a phone, switch Chrome to **⋮ → Desktop site** first; the console collapses
its left menu on mobile and Domains becomes hard to reach.

Zoho's own checker is at **https://zohomail.tools** → Run Checks. DNS changes
can take up to 12–24 hours to propagate depending on TTL, though Cloudflare is
usually near-instant. Re-test at mail-tester.com afterwards for 10/10.

**Why it's worth the two minutes.** DMARC currently passes on SPF alone, which
is fine for mail sent straight from you to someone. But **SPF breaks when a
message is forwarded** and DKIM survives it. People will forward your emails —
to a partner, a parent, a doctor, a caseworker. Without a DKIM signature those
forwarded copies can fail authentication and land in spam, at exactly the
moment someone is trying to bring another person in to help.

### Remaining

- [ ] DKIM signing verified in Zoho (above)
- [ ] Two-factor authentication on the Zoho account
- [ ] Push notifications off, or limited to answering hours

## Don't skip SPF, DKIM and DMARC

Without them your mail lands in spam. For a normal business that's annoying.
For this one it means **someone who finally worked up to asking for help never
hears back, and concludes nobody answered.**

SPF and DKIM are already done. DMARC is the one still missing.

**In Cloudflare: DNS → Records → Add record**

| Field | Value |
| --- | --- |
| Type | `TXT` |
| Name | `_dmarc` |
| Content | `v=DMARC1; p=none; rua=mailto:hello@thehelpingsun.com` |
| TTL | Auto |

Name is just `_dmarc`, not the full domain — Cloudflare appends it. The record:

```
v=DMARC1; p=none; rua=mailto:hello@thehelpingsun.com
```

`p=none` just monitors at first. Once you've seen a few weeks of reports and
nothing legitimate is failing, tighten to `p=quarantine`.

## Test it before you trust it

1. Send from your personal Gmail **to** hello@thehelpingsun.com → it arrives
2. **Reply** from hello@ → check the From address is right
3. Send to a friend on a different provider and ask whether it landed in spam
4. Run the address through mail-tester.com — aim for 9/10 or better

## Then update these

- `site/index.html` — the confirmation panel shows the address
- Instagram and Facebook contact fields (`SOCIAL-PROFILES.md`)
- The form endpoint, if you point it at an inbox (`README.md`)

## One boundary setting

Turn **off** push notifications for this mailbox on your phone, or set them to
your published hours. Mail from this address will sometimes be heavy, and a
3 a.m. buzz you can't act on until morning helps nobody — least of all you.
