"""Build gallery images + manifest from photos/original.

Titles: the 24 selected works keep their given names. Everything else is
labelled documentary-style by time of day and date, which comes from the
file's own timestamp — no invented place names. Edit TITLES to name any of
them, and REJECT to drop one.
"""
import os, json, re, datetime
from PIL import Image, ImageOps, ImageEnhance

SRC="photos/original"; OUT="site/gallery"
os.makedirs(OUT, exist_ok=True)

# Not in the gallery, and why.
REJECT = {
 # Not photographs, or nothing in the frame. The gallery is the whole body of
 # work now, not only sunrises, so the bar is "is it a good picture" rather
 # than "is it a sunset".
 "20260627_123834.jpg": "a snapshot, not a photograph",
 "20251222_171317.jpg": "flat grey, nothing happening",
 "20251225_172350.jpg": "muddy, no subject",
 "20251226_105513.jpg": "confused framing - the Fly Agaric is the better mushroom",
 "20260102_162108.jpg": "flat overcast",
 "20260617_200603.jpg": "flat overcast",
 "20260617_201628.jpg": "same scene, same problem",
}

# Named works. Everything else gets a documentary label.
TITLES = {
 "20261104_064349.jpg": ("First Light", "Walton Lighthouse, Santa Cruz"),
 "20261021_071526.jpg": ("The Morning It Caught Fire", "Santa Cruz"),
 "20261005_064839.jpg": ("Mackerel Sky", "West Cliff, Santa Cruz"),
 "20261102_064330.jpg": ("Before Anyone Else", "Main Beach, Santa Cruz"),
 "20260712_204036.jpg": ("Crimson Rivermouth", "San Lorenzo Rivermouth"),
 "20260713_204007.jpg": ("The Night After", "San Lorenzo Rivermouth"),
 "20260524_195347.jpg": ("Behind the Giant Dipper", "Beach Boardwalk, Santa Cruz"),
 "20260529_203449.jpg": ("The Wheel", "Beach Boardwalk, Santa Cruz"),
 "20260620_204807.jpg": ("Gold on the Water", "San Lorenzo Rivermouth"),
 "20260620_210208.jpg": ("First Star", "Main Beach, Santa Cruz"),
 "20260512_201845.jpg": ("Mauve", "Main Beach, Santa Cruz"),
 "20260919_192400.jpg": ("Ember Band", "Main Beach, Santa Cruz"),
 "20260926_193109.jpg": ("After the Light Went", "Santa Cruz"),
 "20260920_191704.jpg": ("The Last Light", "Santa Cruz County"),
 "20260722_200159.jpg": ("Into the Lagoon", "San Lorenzo Rivermouth"),
 "20260628_203623.jpg": ("Lavender at the Reeds", "San Lorenzo Rivermouth"),
 "20260705_211058.jpg": ("Late", "Main Beach, Santa Cruz"),
 "20260620_204117.jpg": ("The Dunes", "Santa Cruz"),
 "20260621_141734.jpg": ("West Cliff, Midday", "West Cliff Drive, Santa Cruz"),
 "20260706_202420.jpg": ("The Tetrapods", "Santa Cruz Harbour"),
 "20261006_183721.jpg": ("Cliffside", "West Cliff, Santa Cruz"),
 "20261025_161822_6709c948.jpg": ("Sun Through", "Seabright Beach, Santa Cruz"),
 "20261101_141550.jpg": ("Afternoon, Jetty", "Santa Cruz Harbour"),
 "20260504_095320.jpg": ("The Redwoods", "Santa Cruz County"),
 "20251226_133752.jpg": ("Fly Agaric", "Santa Cruz County"),
 "20261117_065329.jpg": ("Daybreak", "Walton Lighthouse, Santa Cruz"),
 "20261117_165552.jpg": ("Across the Bay", "Santa Cruz"),
 "20251229_172403.jpg": ("December Wharf", "Santa Cruz"),
 "20251228_142219.jpg": ("The Green Bluff", "Santa Cruz"),
 "20251225_114326.jpg": ("Christmas Surf", "Santa Cruz"),
 "20251225_115121.jpg": ("Full Speed", "Santa Cruz"),
}

def label(hhmm):
    h = hhmm.hour + hhmm.minute/60
    if   h < 5:    return "Night"
    elif h < 8.5:  return "Sunrise"
    elif h < 11:   return "Morning"
    elif h < 15:   return "Midday"
    elif h < 17:   return "Afternoon"
    elif h < 19.5: return "Sunset"
    elif h < 21:   return "Dusk"
    return "Night"

def fit(im, longest):
    w, h = im.size
    s = longest / max(w, h)
    return im.copy() if s >= 1 else im.resize((round(w*s), round(h*s)), Image.LANCZOS)

man = []
for fn in sorted(os.listdir(SRC)):
    if not fn.endswith(".jpg") or fn in REJECT: continue
    m = re.match(r"(\d{8}_\d{6})", fn)
    if not m: continue
    dt = datetime.datetime.strptime(m.group(1), "%Y%m%d_%H%M%S")
    slug = m.group(1)
    title, place = TITLES.get(fn, (label(dt), "Santa Cruz County"))
    when = dt.strftime("%-d %B %Y, %-I:%M %p").replace("AM","am").replace("PM","pm")
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, fn))).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.05)
    fit(im, 1600).save(f"{OUT}/{slug}.jpg",   "JPEG", quality=76, optimize=True, progressive=True)
    th = fit(im, 760); th.save(f"{OUT}/{slug}-t.jpg", "JPEG", quality=74, optimize=True, progressive=True)
    man.append({"slug":slug,"title":title,"when":when,"place":place,
                "w":th.size[0],"h":th.size[1],
                "orient":"portrait" if th.size[1]>th.size[0] else "landscape",
                "named": fn in TITLES})

# LEAD sets the first twelve, which are also the homepage featured strip.
LEAD = ["20261104_064349","20260712_204036","20261021_071526","20260529_203449",
        "20251229_172403","20260524_195347","20251226_133752","20260620_210208",
        "20260713_204007","20251228_142219","20260919_192400","20260926_193109"]
by = {m["slug"]: m for m in man}
lead  = [by[s] for s in LEAD if s in by]
rest_named = sorted([m for m in man if m["named"] and m["slug"] not in LEAD], key=lambda m: m["slug"], reverse=True)
docs       = sorted([m for m in man if not m["named"]], key=lambda m: m["slug"], reverse=True)
man = lead + rest_named + docs
for m in man: m.pop("named")
json.dump(man, open(f"{OUT}/manifest.json","w"), indent=1)
print(f"{len(man)} images ({len(lead)} leading, {len(rest_named)} other named, {len(docs)} documentary)")
