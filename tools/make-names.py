"""Generate a starting-point name for every photograph that still lacks one.

Names are built only from things that can be measured in the file: the
dominant hue of the sky, how bright it is, the time of day and the month,
all from the pixels and the timestamp. Nothing about place or subject is
asserted beyond the Bay itself, which Ian confirmed. Specific landmarks are
not guessed - that is how a rooftop got called "Boardwalk, Reflected".

These are starting points. Rename freely while uploading.
"""
import json, datetime, re

MEAS = json.load(open("/tmp/claude-0/-home-user-the-helping-sun/3b620663-5197-5cc0-92ab-ad10014d510c/scratchpad/measure.json"))
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
        v  = MEAS[slug]
        dt = datetime.datetime.strptime(slug[:15], "%Y%m%d_%H%M%S")
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
        v=MEAS[s]; print(f"  {s}  hue{v['hue']:>6.1f} sat{v['sat']:>5.1f} br{v['bright']:>5.1f}  ->  {n}")
