"""Regenerate the <figure> list in site/prints.html from the gallery manifest.

Run after tools/make-gallery.py so the page can never drift from the images
that actually exist. Everything outside the .grid block is left untouched, so
prose, prices and the lightbox script are safe to edit by hand.
"""
import json, re

PAGE = "site/prints.html"
MAN  = "site/gallery/manifest.json"

man = json.load(open(MAN))
figures = "\n".join(
f'''      <figure class="shot" data-slug="{m['slug']}" data-title="{m['title']}" data-when="{m['when']}" data-place="{m['place']}" data-faa="{m.get('faa','')}">
        <button type="button" class="shot-btn" aria-label="Enlarge {m['title']}">
          <img src="gallery/{m['slug']}-t.jpg" alt="{m['title']} — {m['place']}" loading="lazy" width="{m['w']}" height="{m['h']}">
        </button>
        <figcaption><span class="t">{m['title']}</span><span class="w">{m['when']}</span></figcaption>
      </figure>''' for m in man)

s = open(PAGE).read()
new, n = re.subn(r'(<div class="grid">\n).*?(\n</div>\n\n<p style="margin-top:34px)',
                 lambda _: _.group(1) + figures + _.group(2),
                 s, count=1, flags=re.S)
if n != 1:
    raise SystemExit("could not locate the grid block in " + PAGE)
open(PAGE, "w").write(new)
print(f"rebuilt {PAGE} with {len(man)} photographs")

# --- homepage featured grid: the first 12 of the manifest (the named works)
HOME = "site/index.html"
feat = man[:12]
home_figs = "\n".join(
f'''        <figure class="shot" data-slug="{m['slug']}" data-title="{m['title']}" data-when="{m['when']}" data-place="{m['place']}" data-faa="{m.get('faa','')}">
          <button type="button" class="shot-btn" aria-label="Enlarge {m['title']}">
            <img src="gallery/{m['slug']}-t.jpg" alt="{m['title']} — {m['place']}" loading="lazy" width="{m['w']}" height="{m['h']}">
          </button>
          <figcaption><span class="t">{m['title']}</span><span class="w">{m['when']}</span></figcaption>
        </figure>''' for m in feat)

h = open(HOME).read()
new_h, n2 = re.subn(r'(<div class="home-grid">\n).*?(\n    </div>)',
                    lambda _: _.group(1) + home_figs + _.group(2),
                    h, count=1, flags=re.S)
if n2 != 1:
    raise SystemExit("could not locate the home-grid block in " + HOME)
new_h = re.sub(r'See all \d+ photographs', f'See all {len(man)} photographs', new_h)
new_h = re.sub(r'Browse all \d+ photographs', f'Browse all {len(man)} photographs', new_h)

# "Available now": only photographs with a product URL that was read off the
# live shop and answered 200. Everything else in the archive is work you can
# look at but not yet buy, and the page must not blur the two.
avail = [m for m in man if m.get("faa")]
cards = []
for m in avail:
    cards.append(
        f'      <a class="sale" href="{m["faa"]}" target="_blank" rel="noopener">\n'
        f'        <img src="gallery/{m["slug"]}-t.jpg" alt="{m["title"]}" loading="lazy" width="760" height="507">\n'
        f'        <figcaption>{m["title"]}<span class="buy-tag">Buy a print</span></figcaption>\n'
        f'      </a>')
new_h, n3 = re.subn(r'(<div class="sale-grid">\n).*?(\n    </div>)',
                    lambda mm: mm.group(1) + "\n".join(cards) + mm.group(2),
                    new_h, count=1, flags=re.S)
if not n3:
    raise SystemExit("could not locate the sale-grid block in " + HOME)
note = (f"These {len(avail)} are listed in the shop right now and ship worldwide. "
        f"The other {len(man)-len(avail)} in the archive are not listed yet \u2014 "
        f'<a href="#ask" style="color:var(--sun)">tell me which you want</a> and I will put it up next.')
new_h = re.sub(r'(<p class="sale-note">).*?(</p>)', lambda mm: mm.group(1)+note+mm.group(2),
               new_h, count=1, flags=re.S)
print(f"rebuilt the Available-now showcase ({len(avail)} listed of {len(man)})")
open(HOME, "w").write(new_h)
print(f"rebuilt {HOME} featured grid ({len(feat)} of {len(man)})")
