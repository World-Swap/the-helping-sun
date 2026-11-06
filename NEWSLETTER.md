# Golden Hour

One letter, Sunday morning. Four things every time:

1. **One honest thing** about the week
2. **One small thing** to try
3. **One script** — the actual words to say to someone
4. **One sunrise**

No course at the end. Nothing to buy. The format is deliberately small enough
to write on a bad week, because a letter that only arrives when you're well
isn't a letter anyone can rely on.

---

## Platform

**Beehiiv**, free tier — up to 2,500 subscribers, custom domain, no cost. Ghost
is better-looking but starts around $9/month and you don't need it yet.

Whatever you pick, **send from `hello@thehelpingsun.com`** so replies land in
the mailbox you just set up.

### One technical note

The newsletter platform sends through its own servers, so it needs its own
domain authentication. It will give you **CNAME records** to add in Cloudflare.

**Add those CNAMEs. Do not touch your existing MX, SPF or DKIM records.**
Beehiiv uses its own return-path domain and its own DKIM selector, so it won't
collide with Zoho's `zmail` selector. If any platform ever asks you to *replace*
your SPF record rather than add a CNAME, stop — that would break your regular
email.

Send a test to mail-tester.com from the newsletter platform too. The score
there is separate from your Zoho score.

---

# THE WELCOME EMAIL

Sends automatically the moment someone subscribes. This is the most important
email you will ever write, because a share of people will sign up at their
lowest and this is what they get.

**Subject:** `You're in. Here's what this is.`

```
Hi —

Thanks for signing up. I'm Ian.

Golden Hour comes out on Sunday mornings. Every one has four things in it:

— one honest thing about the week
— one small thing to try
— one script: the actual words to say to a doctor, a creditor, or a friend
  you've gone quiet on
— one sunrise, taken somewhere in Santa Cruz

That's the whole thing. No course at the end. Nothing to buy.

A few things worth saying up front.

I'm not a therapist and this isn't therapy. I'm someone who spent most of his
life depressed, broke, and too embarrassed to tell anyone. I got through it
without anyone reaching back, and I don't recommend that route. That's the
entire reason this exists.

If you ever want to talk, you can just reply to this email. It comes to me and
nobody else. You don't have to be articulate or have it organised in your head.
Three words is enough.

And if things are bad right now, please don't wait for a Sunday:

988 — Suicide & Crisis Lifeline, call or text, 24/7
741741 — Crisis Text Line, text HOME
211 — rent, food, utilities, local help
911 — immediate danger

One small thing before you go. If you're reading this during daylight, go
outside for ten minutes. Not a walk, not exercise. Just outside. It's the
cheapest thing on the whole list and it does more than it sounds like it
should.

See you Sunday.

— Ian
thehelpingsun.com
```

> Don't add a "confirm your subscription" step on top of this if you can avoid
> it. Every extra click loses someone, and the people you most want to reach
> are the ones with the least energy for clicks.

---

# ISSUE 01

Lands Sunday morning. The honest thing is timed to arrive about ten hours
before the thing it describes.

**Subject:** `It passes at nine`

```
GOLDEN HOUR 01

---

THE HONEST THING

Sunday, around 7pm, the light goes and something in my chest changes.

It isn't about Monday. I've had it on Sundays when I had nowhere to be on
Monday, and nothing to dread. It's the specific feeling of a week ending when
the week contained nothing you could point to.

For years I thought this was a personal defect. A thing about me. It turns out
it's close to universal and almost nobody mentions it, which means a very large
number of people are sitting through the same hour alone, separately, at the
same time.

I don't have a fix. I have two things.

The first is that it's extremely common, so you've been doing it on your own
for no reason.

The second is that it passes by about nine. Every time. That sounds like
nothing, but knowing it's a tide and not a permanent new fact about your life
is the difference between waiting it out and drowning in it.

If it's Sunday evening when you read this: it's seven. It passes at nine. You
can wait that out.

---

ONE SMALL THING

Ten to twenty minutes of outdoor light, before noon.

Not a sun lamp. Not through a window. Outside — and an overcast morning still
beats your brightest indoor room by a wide margin.

Nobody is claiming a walk fixes depression. It measurably helps with sleep and
mood, it costs nothing, and it asks almost nothing from you on a day when you
have almost nothing to give.

You don't even have to walk. Stand in a doorway with a coffee.

---

THE SCRIPT

What to say when you can't pay a bill.

The word you need is HARDSHIP. Almost every lender, card issuer and utility
has a hardship or forbearance program. Almost none of them will mention it
first. You have to say the word.

Call the number on the statement. When someone picks up:

  "I'm having trouble making my payments. I want to stay current. What
   hardship options do you have?"

Then ask these four, in order:

  1. "Will this show on my credit report?"
  2. "Does interest keep adding up during the program?"
  3. "Can you email me that in writing?"
  4. "Can I get your name and a reference number?"

Things you do not have to do: explain your whole life, apologise, or agree to
anything on the first call. "I need to think about it" is a complete sentence.

I avoided one phone call for eleven weeks once. The call took nine minutes.
The eleven weeks cost me more than the debt did.

If the call itself is the part you can't do, I'll sit on the line while you
make it. That's a real thing I do and it's free. Just reply to this.

---

THE SUNRISE

[ATTACH: site/img/sunrise-lighthouse-1400.jpg]

Walton Lighthouse, 6:43am, November 4th.

Third morning in a row I'd got up for this. That part mattered a lot more than
the photograph did.

---

That's the whole letter. Reply any time — it comes to me and nobody else.

If today is bad: 988, call or text, any hour.

— Ian
thehelpingsun.com

The Helping Sun is peer support, not therapy, and not an emergency service.
```

---

# TEMPLATE FOR EVERY ISSUE AFTER

```
GOLDEN HOUR [NN]

THE HONEST THING
[One specific thing, in the first person, unresolved. Name the real detail —
the pile of mail, the 3pm shower, the $12 on a Tuesday. Specificity is the
entire value. Don't end it with a lesson.]

ONE SMALL THING
[One action. Not five. Something doable on a bad day.]

THE SCRIPT
[Word-for-word language for one conversation people avoid.]

THE SUNRISE
[One photo, the date and time, one line about that morning.]

Reply any time — it comes to me and nobody else.
If today is bad: 988, call or text, any hour.

— Ian
thehelpingsun.com

The Helping Sun is peer support, not therapy, and not an emergency service.
```

## Sending rules

- **Sunday morning**, consistently. The day matters more than the time.
- **988 in every single issue.** No exceptions.
- **Never write and send on the same day.** Draft midweek, read it Saturday,
  send Sunday. This catches the ones written from inside a bad day.
- **Never send from inside a bad day** at all. A short, calm "this week is hard
  for me, back next Sunday" is honest and fine. Raw distress is not a
  newsletter — it's you needing support, and you deserve the real kind.
- **Replies are the point, not opens.** The metric is how many people write
  back, not the open rate. Answer every one.
- Keep it under about 700 words. It should be readable in one sitting on a
  phone, in bed.

## Where the next twelve issues come from

`POSTS.md` and `REELS.md` already hold the raw material: the unopened mail,
looking fine, the ghosted friend, 211, the doctor script, the boss script.
Each one is an honest thing and a script that can pair with any small thing
and any sunrise. You have roughly a quarter's worth of letters already written
in rougher form.
