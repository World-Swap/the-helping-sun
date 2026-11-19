"""Regenerate the <figure> list in site/prints.html from the gallery manifest.

Run after tools/make-gallery.py so the page can never drift from the images
that actually exist. Everything outside the .grid block is left untouched, so
prose, prices and the lightbox script are safe to edit by hand.
"""
import json, re

PAGE = "site/prints.html"
MAN  = "site/gallery/manifest.json"


def label(m):
    """What to call a photograph on the site: when it was taken.

    No titles at all. The machine-made ones collided with the names Ian gives
    things on the shop, and carrying only some titles made the gallery look
    like two different systems. A date and a place are true of every
    photograph and need no upkeep.
    """
    return m["when"]


def sub(m):
    """The second line: where it was taken."""
    return m["place"]


man = json.load(open(MAN))
figures = "\n".join(
f'''      <figure class="shot" data-slug="{m['slug']}" data-title="{label(m)}" data-when="{m['when']}" data-place="{m['place']}">
        <button type="button" class="shot-btn" aria-label="Enlarge photograph from {m['when']}">
          <img src="gallery/{m['slug']}-t.jpg" alt="Photograph taken {m['when']} at {m['place']}" loading="lazy" width="{m['w']}" height="{m['h']}">
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

HOME = "site/index.html"

# --- homepage: a slideshow of every photograph. A column of 147 is a very
# long page on a phone; one at a time, swipeable, is the same work in a
# screenful. These carry class "shot", so the existing lightbox picks them all
# up and opening one starts at the right photograph.
slides = "\n".join(
f'''      <figure class="shot ss-slide" data-slug="{m['slug']}" data-title="{label(m)}" data-when="{m['when']}" data-place="{m['place']}">
        <button type="button" class="shot-btn" aria-label="Enlarge photograph from {m['when']}">
          <img src="gallery/{m['slug']}.jpg" alt="Photograph taken {m['when']} at {m['place']}" loading="lazy" decoding="async" width="{round(m['w']*1600/760)}" height="{round(m['h']*1600/760)}">
        </button>
      </figure>''' for m in man)

h = open(HOME).read()
new_h, n2 = re.subn(r'(<div class="ss-track" id="ss-track">\n).*?(\n      </div><!-- /ss-track -->)',
                    lambda _: _.group(1) + slides + _.group(2),
                    h, count=1, flags=re.S)
if n2 != 1:
    raise SystemExit("could not locate the slideshow track in " + HOME)
new_h = re.sub(r'<span id="ss-total">\d+</span>', f'<span id="ss-total">{len(man)}</span>', new_h)
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
print(f"rebuilt {HOME} slideshow ({len(man)} photographs)")
