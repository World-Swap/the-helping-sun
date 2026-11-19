"""Regenerate the <figure> list in site/prints.html from the gallery manifest.

Run after tools/make-gallery.py so the page can never drift from the images
that actually exist. Everything outside the .grid block is left untouched, so
prose, prices and the lightbox script are safe to edit by hand.
"""
import json, re

PAGE = "site/prints.html"
MAN  = "site/gallery/manifest.json"


def label(m):
    """What to call a photograph on the site.

    Only the works Ian actually named carry a title here. The rest were named
    by measuring their colour, and those machine names collided with the names
    he gives things on the shop - the same picture reading "Cobalt Morning"
    here and something else there. Showing the date instead says something
    true and nothing confusing.
    """
    return m["title"] if m.get("named") else m["when"]


def sub(m):
    """The second line: the date, unless the date is already the title."""
    return m["when"] if m.get("named") else m["place"]


man = json.load(open(MAN))
figures = "\n".join(
f'''      <figure class="shot" data-slug="{m['slug']}" data-title="{label(m)}" data-when="{m['when']}" data-place="{m['place']}">
        <button type="button" class="shot-btn" aria-label="Enlarge photograph from {m['when']}">
          <img src="gallery/{m['slug']}-t.jpg" alt="{label(m)} — {m['place']}" loading="lazy" width="{m['w']}" height="{m['h']}">
        </button>
        <figcaption><span class="t">{label(m)}</span><span class="w">{sub(m)}</span></figcaption>
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
f'''        <figure class="shot" data-slug="{m['slug']}" data-title="{label(m)}" data-when="{m['when']}" data-place="{m['place']}">
          <button type="button" class="shot-btn" aria-label="Enlarge photograph from {m['when']}">
            <img src="gallery/{m['slug']}-t.jpg" alt="{label(m)} — {m['place']}" loading="lazy" width="{m['w']}" height="{m['h']}">
          </button>
          <figcaption><span class="t">{label(m)}</span><span class="w">{sub(m)}</span></figcaption>
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
# The "Available now" showcase and the in-the-shop badges used to mirror the
# storefront here. They are gone: every photograph now points at the shop
# front and the shop keeps its own catalogue. Nothing on this site needs to
# be re-matched after an upload.
open(HOME, "w").write(new_h)
print(f"rebuilt {HOME} featured grid ({len(feat)} of {len(man)})")
