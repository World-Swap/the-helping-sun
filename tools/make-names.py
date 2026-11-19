"""Generate a starting-point name for every photograph that still lacks one.

Names are built only from things that can be measured in the file: the
dominant hue of the sky, how bright it is, the time of day and the month,
all from the pixels and the timestamp. Nothing about place or subject is
asserted beyond the Bay itself, which Ian confirmed. Specific landmarks are
not guessed - that is how a rooftop got called "Boardwalk, Reflected".

These are starting points. Rename freely while uploading.
"""
import json, datetime, re, colorsys, os
from PIL import Image, ImageOps

def measure(slug):
    """Measure a photograph's colour from its own pixels.

    Done here rather than read from a cache so that a photograph added later
    is named like every other one. An earlier version read a file in a
    session scratchpad; when that was cleared, new photographs silently fell
    back to generic labels and the gallery showed "Sunset" three times.
    """
    import glob
    hit = glob.glob(f"photos/original/{slug}.jpg") or \
          [p for p in glob.glob("photos/original/*.jpg")
           if re.sub(r"[^A-Za-z0-9]+","-",os.path.splitext(os.path.basename(p))[0]).strip("-").lower() == slug]
    im = ImageOps.exif_transpose(Image.open(hit[0])).convert("RGB")
    w, h = im.size
    sm = im.resize((120, max(1, int(120 * h / w))))
    px = list(sm.getdata())
    sky = px[:len(px) // 3]                       # top third, where the light is
    def stats(sample):
        hs = [colorsys.rgb_to_hsv(r/255, g/255, b/255) for r, g, b in sample]
        # circular mean of hue, weighted by saturation so grey pixels do not vote
        import math
        x = sum(math.cos(hh*2*math.pi) * ss for hh, ss, _ in hs)
        y = sum(math.sin(hh*2*math.pi) * ss for hh, ss, _ in hs)
        hue = (math.degrees(math.atan2(y, x)) + 360) % 360
        return hue, 255*sum(s for _, s, _ in hs)/len(hs), 255*sum(v for _, _, v in hs)/len(hs)
    hue, sat, bright = stats(px)
    _, _, skybright = stats(sky)
    return {"hue": round(hue,1), "sat": round(sat,1),
            "bright": round(bright,1), "skybright": round(skybright,1)}

MEAS = {}
man  = json.load(open("site/gallery/manifest.json"))

def family(h, sat, sky):
    if sat < 12:                       return "pale"
    if h < 18 or h >= 345:             return "red"
    if h < 40:                         return "amber"
    if h < 60:                         return "gold"
    if h < 170:                        return "green"
    if h < 200:                        return "cyan"
    if h < 250:                        return "blue"
    if h < 290:                        return "violet"
    if h < 320:                        return "magenta"
    return "rose"

def part_of_day(dt):
    h = dt.hour + dt.minute/60
    if h < 5:    return "night"
    if h < 8.5:  return "dawn"
    if h < 11:   return "morning"
    if h < 15:   return "midday"
    if h < 17:   return "afternoon"
    if h < 19.5: return "evening"
    if h < 21:   return "dusk"
    return "night"

# colour word options per family, so repeated conditions don't repeat wording
WORDS = {
 "red":     ["Ember", "Rust", "Furnace", "Red Hour", "Burnt"],
 "amber":   ["Amber", "Honey", "Copper", "Brass", "Sodium", "Tangerine"],
 "gold":    ["Gold", "Gilt", "Bright Gold", "Old Gold"],
 "rose":    ["Rose", "Blush", "Coral"],
 "magenta": ["Magenta", "Fuchsia"],
 "violet":  ["Violet", "Mauve", "Plum", "Iris"],
 "blue":    ["Blue", "Cobalt", "Steel", "Slate", "Indigo", "Deep Blue"],
 "cyan":    ["Aqua", "Teal", "Sea Glass"],
 "green":   ["Green", "Verdigris"],
 "pale":    ["Pale", "Pewter", "Silver", "Ash", "Overcast", "Soft"],
}
DAY = {"dawn":"Dawn","morning":"Morning","midday":"Midday",
       "afternoon":"Afternoon","evening":"Evening","dusk":"Dusk","night":"Night"}

def candidates(colour_words, dayword, month, dark):
    c = []
    for w in colour_words:
        c += [f"{w} {dayword}", f"{dayword} in {w}", f"{month} {w}", f"The {w} Hour",
              f"{w} over the Bay", f"{w} Light", f"{w} {month}"]
    c += [f"{dayword}, {month}", f"{month} {dayword}"]
    if dark: c += [f"Low Light, {month}", f"{dayword} After Dark"]
    return c

def build():
    used, names = set(), {}
    # hand-named works keep their names and reserve them
    for m in man:
        if m["place"] != "Santa Cruz County" or m["title"] not in ("Sunrise","Sunset","Dawn","Dusk","Night","Midday","Morning","Afternoon"):
            used.add(m["title"].lower())
    for m in man:
        slug = m["slug"]
        if m["title"].lower() in used and m["title"] not in ("Sunrise","Sunset","Dawn","Dusk","Night","Midday","Morning","Afternoon"):
            names[slug] = m["title"]; continue
        v  = MEAS.setdefault(slug, measure(slug))
        dt = datetime.datetime.fromisoformat(m["iso"])
        fam = family(v["hue"], v["sat"], v["skybright"])
        day = DAY[part_of_day(dt)]
        month = dt.strftime("%B")
        for cand in candidates(WORDS[fam], day, month, v["bright"] < 55):
            if cand.lower() not in used:
                used.add(cand.lower()); names[slug] = cand; break
        else:
            n = f"{day}, {dt.strftime('%-d %B')}"
            used.add(n.lower()); names[slug] = n
    return names

if __name__ == "__main__":
    names = build()
    json.dump(names, open("photo-names.json","w"), indent=1)
    vals = list(names.values())
    print(f"{len(names)} names, {len(set(v.lower() for v in vals))} unique")
    gen = [ (m['slug'], names[m['slug']]) for m in man if m['place']=="Santa Cruz County" ]
    print("\nsample of generated names:")
    for s,n in gen[:18]:
        v=MEAS.setdefault(s, measure(s)); print(f"  {s}  hue{v['hue']:>6.1f} sat{v['sat']:>5.1f} br{v['bright']:>5.1f}  ->  {n}")
