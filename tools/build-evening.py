#!/usr/bin/env python3
"""Build site/evening.html — the 5 November sunset, in sequence.

The photographs are pulled from the gallery manifest by date, so the page
cannot drift from the archive. SERIES names the ten Ian entered into the Sony
Series competition; leave it empty and the page shows the whole evening.
"""
import datetime, json, re

MAN  = "site/gallery/manifest.json"
PAGE = "site/evening.html"
DAY  = "20261105"

# The ten entered into the Sony Series competition. Empty = show them all.
SERIES = []

man = json.load(open(MAN))
shots = sorted([m for m in man if m["slug"].startswith(DAY)], key=lambda m: m["iso"])
if SERIES:
    shots = [m for m in shots if m["slug"] in SERIES]

first = datetime.datetime.fromisoformat(shots[0]["iso"])
last  = datetime.datetime.fromisoformat(shots[-1]["iso"])
mins  = round((last - first).total_seconds() / 60)
start = first.strftime("%-I:%M").lstrip("0")
end   = last.strftime("%-I:%M %p").replace("PM", "pm").replace("AM", "am")

def clock(m):
    d = datetime.datetime.fromisoformat(m["iso"])
    return d.strftime("%-I:%M").lstrip("0")

figs = []
for i, m in enumerate(shots):
    elapsed = round((datetime.datetime.fromisoformat(m["iso"]) - first).total_seconds() / 60)
    since = "the first frame" if i == 0 else f"{elapsed} min later"
    figs.append(
f'''      <figure class="shot ev-shot" data-slug="{m['slug']}" data-title="{m['when']}" data-when="{m['when']}" data-place="{m['place']}">
        <button type="button" class="shot-btn" aria-label="Enlarge the frame taken at {clock(m)}">
          <img src="gallery/{m['slug']}-t.jpg" alt="The sunset at {clock(m)} on 5 November 2026" loading="lazy" decoding="async" width="{m['w']}" height="{m['h']}">
        </button>
        <figcaption><span class="t">{clock(m)}</span><span class="w">{since}</span></figcaption>
      </figure>''')

src = open("site/prints.html").read()
head  = src[:src.index("</head>")]
header = re.search(r"<header.*?</header>", src, re.S).group(0)
footer = re.search(r"<footer.*?</footer>", src, re.S).group(0)
lb     = re.search(r'<dialog class="lb".*?</dialog>', src, re.S).group(0)
script = re.findall(r"<script>.*?</script>", src, re.S)[-1]

head = re.sub(r"<title>[^<]*</title>", "<title>One evening &mdash; The Helping Sun</title>", head, count=1)
head = re.sub(r'<link rel="canonical" href="[^"]*">',
              '<link rel="canonical" href="https://thehelpingsun.com/evening">', head, count=1)
desc = (f"One sunset over Santa Cruz photographed from {start} to {end} on 5 November 2026 "
        f"by Ian Sun &mdash; {len(shots)} frames across {mins} minutes.")
head = re.sub(r'<meta name="description" content="[^"]*">',
              f'<meta name="description" content="{desc}">', head, count=1)
head = re.sub(r'<meta property="og:url" content="[^"]*">',
              '<meta property="og:url" content="https://thehelpingsun.com/evening">', head, count=1)
head = re.sub(r'<meta property="og:title" content="[^"]*">',
              '<meta property="og:title" content="One evening — The Helping Sun">', head, count=1)
head = re.sub(r'<meta property="og:description" content="[^"]*">',
              f'<meta property="og:description" content="{desc}">', head, count=1)
head += '''<style>
.ev-lede{max-width:60ch}
.ev-stat{display:flex;gap:26px;flex-wrap:wrap;margin-top:26px;padding-top:20px;
  border-top:1px solid var(--line,#dfe4ec)}
.ev-stat div{min-width:0}
.ev-stat .n{font-family:var(--ff-display);font-size:clamp(26px,4vw,34px);display:block;line-height:1}
.ev-stat .l{font-family:var(--ff-mono);font-size:10.5px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--muted);display:block;margin-top:5px}
.ev-shot .t{font-family:var(--ff-mono);font-size:13px;letter-spacing:.02em;display:block}
.ev-shot .w{font-family:var(--ff-mono);font-size:9.5px;letter-spacing:.04em;color:var(--muted);
  text-transform:uppercase;display:block;margin-top:1px}
</style>'''

body = f'''
{header}
<main>
<section class="band">
  <div class="wrap">
    <p class="eyebrow">One evening</p>
    <h1 style="font-size:clamp(30px,5vw,46px);max-width:17ch;margin-top:8px">The whole sunset, in order.</h1>
    <p class="lede ev-lede" style="margin-top:16px">5 November 2026. I stood in one place from {start} to {end} and kept photographing while the light went. These are the frames in the order they happened &mdash; no rearranging, nothing skipped for being dull.</p>
    <p class="lede ev-lede" style="margin-top:14px">It is the clearest answer I have to what the photographs are for. Not one perfect picture. Just staying out there while it changed.</p>

    <div class="ev-stat">
      <div><span class="n">{len(shots)}</span><span class="l">frames</span></div>
      <div><span class="n">{mins}</span><span class="l">minutes</span></div>
      <div><span class="n">{start}&ndash;{end.split()[0]}</span><span class="l">{end.split()[1]}</span></div>
    </div>

    <div class="grid" style="margin-top:30px">
{chr(10).join(figs)}
    </div>

    <p style="margin-top:34px;display:flex;gap:13px;flex-wrap:wrap">
      <a class="btn btn--ghost" href="/prints">The full archive &rarr;</a>
      <a class="btn btn--ghost" href="https://ian-sun.pixels.com/shop" target="_blank" rel="noopener">Shop prints &rarr;</a>
    </p>
  </div>
</section>
</main>
{footer}
{lb}
{script}
</body>
</html>
'''
open(PAGE, "w").write(head + "</head>\n<body>\n" + body)
print(f"rebuilt {PAGE}: {len(shots)} frames, {start}–{end}, {mins} minutes")
