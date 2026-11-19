#!/usr/bin/env python3
"""Build faa-links.json: photograph slug -> its own product page on the shop.

Two sources, both grounded in pages that actually exist:

  1. The live storefront index. A listing whose title still matches the
     photograph's gallery title is matched automatically.
  2. faa-manual.json, for listings renamed during upload. Keyed by upload
     number so it survives renames at either end.

Every URL is requested before it is written. A URL that does not return 200
is dropped with a warning rather than shipped, because a dead "Buy this
print" button is worse than no button at all.

Never write a URL into faa-links.json by hand or by guessing it from a title.
"""
import json, re, sys, urllib.request

STORE = "https://ian-sun.pixels.com/"
UA    = {"User-Agent": "the-helping-sun-site-build/1.0"}


def get(url, timeout=40):
    try:
        with urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as e:
        return getattr(e, "code", 0), ""


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t.lower())).strip("-")


# Read /shop, not the profile front page. The front page shows a selection
# (25 at the time of writing) while /shop lists everything, so reading the
# front page silently hid 20 live works and made them look unlisted.
status, html = get(STORE + "shop")
if status != 200:
    sys.exit(f"shop unreachable ({status}) — leaving faa-links.json alone")

listings = sorted(set(re.findall(r"/featured/([a-z0-9\-]+)-ian-sun\.html", html)))
print(f"/shop lists {len(listings)} works")

manifest = json.load(open("site/gallery/manifest.json"))
numbers  = json.load(open("upload-numbers.json"))
manual   = {k: v for k, v in json.load(open("faa-manual.json")).items()
            if not k.startswith("_")}
by_num   = {v: k for k, v in numbers.items()}

# title -> photograph, for the automatic pass
by_title = {slugify(m["title"]): m["slug"] for m in manifest}

pairs = {}                                    # photo slug -> storefront slug
for listing in listings:
    photo = by_title.get(listing)
    if photo:
        pairs[photo] = listing

manual_hits = 0
for num, listing in manual.items():
    photo = by_num.get(int(num))
    if not photo:
        print(f"  ! no photograph numbered {num}")
        continue
    pairs[photo] = listing
    manual_hits += 1

links, dead = {}, []
for photo, listing in sorted(pairs.items()):
    url = f"{STORE}featured/{listing}-ian-sun.html"
    code, _ = get(url, timeout=25)
    if code == 200:
        links[photo] = url
    else:
        dead.append((code, url))

json.dump(links, open("faa-links.json", "w"), indent=1, sort_keys=True)
print(f"wrote faa-links.json: {len(links)} verified product links "
      f"({manual_hits} by hand, rest matched on title)")
for code, url in dead:
    print(f"  ! dropped, returned {code}: {url}")

unplaced = [l for l in listings if l not in set(pairs.values())]
if unplaced:
    print("\nlistings not matched to a photograph — rename them back, or add "
          "them to faa-manual.json by upload number:")
    for u in unplaced:
        print("  ", u)
