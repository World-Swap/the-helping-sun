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
f'''      <figure class="shot" data-slug="{m['slug']}" data-title="{m['title']}" data-when="{m['when']}" data-place="{m['place']}">
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
