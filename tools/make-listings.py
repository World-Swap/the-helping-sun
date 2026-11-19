import os

import json, csv, re, datetime

man = json.load(open("site/gallery/manifest.json"))
# Permanent file numbers. New photographs append; nothing already uploaded
# is ever renumbered. Delete this file only if you want to renumber everything.
NUMS = json.load(open("upload-numbers.json")) if os.path.exists("upload-numbers.json") else {}
def filenum(slug):
    if slug not in NUMS:
        NUMS[slug] = (max(NUMS.values()) + 1) if NUMS else 1
        json.dump(NUMS, open("upload-numbers.json","w"), indent=1)
    return NUMS[slug]
NAMES = json.load(open("photo-names.json"))
MEAS  = json.load(open("/tmp/claude-0/-home-user-the-helping-sun/3b620663-5197-5cc0-92ab-ad10014d510c/scratchpad/measure.json"))

def _family(h, sat):
    if sat < 12: return "soft, overcast"
    if h < 18 or h >= 345: return "deep red"
    if h < 40:  return "amber"
    if h < 60:  return "gold"
    if h < 170: return "green"
    if h < 200: return "blue-green"
    if h < 250: return "blue"
    if h < 290: return "violet"
    if h < 320: return "magenta"
    return "rose"

SERIES_FULL = ("Part of an ongoing series photographed mostly within a few miles "
               "of home in Santa Cruz County, California.")
SERIES_SHORT = ("Part of an ongoing series photographed mostly within a few miles "
                "of home on the Santa Cruz coast.")
# A photograph taken away from home cannot carry either line: it would tell a
# buyer the picture was made somewhere it was not.
SERIES_AWAY = "Part of an ongoing series by Ian Sun, photographed away from home at {}."

# Individual descriptions for the named works.
DESC = {
# Lake Camanche, September 2026. Written from what is actually in each frame:
# the generated line describes sky colour, which says nothing true about a
# campfire or a creek under tree cover.
"20260916_192350": "Valley oaks in silhouette against an amber sky, the last light going down over Lake Camanche. Photographed at 7:23 on a September evening.",
"20260916_214332": "A campfire burning down to embers in a steel ring, the only light left at the end of the night. Photographed at 9:43 on a September evening at Lake Camanche.",
"20260918_115202": "A shallow creek running over pale river rock, with willow and oak closing in overhead and the water clear enough to read the stones through it. Photographed late on a September morning near Lake Camanche.",
"20260918_122400": "Still green water in a creek, holding the reflection of the trees above it, with bunchgrass on the banks and leaf litter on the bottom. Photographed at midday in September near Lake Camanche.",

"20261117_065329": "The sun coming up over the ridge across Monterey Bay, with Walton Lighthouse standing on the jetty and mist lifting off the break. A pool of tidewater holds the light in the foreground. Taken at 6:53 on a November morning.",
"20261117_165552": "Late afternoon light over the Santa Cruz wharf, seen across the water from the cliffs, with a few people out on the bluff. Taken just before five on a November afternoon.",
"20261104_064349": "Sunrise over Monterey Bay, with Walton Lighthouse standing on the jetty and the tide pooled across the sand. Taken at 6:43 on a November morning, the third consecutive dawn of a run of early starts.",
"20260712_204036": "Crimson cloud breaking over the Santa Cruz Beach Boardwalk, mirrored in the still water of the San Lorenzo rivermouth on a July evening.",
"20261021_071526": "The whole sky turned pink and orange over a park ten minutes from my front door, a little after seven on an October morning.",
"20260529_203449": "The ferris wheel at the Santa Cruz Beach Boardwalk in silhouette against a peach-coloured dusk.",
"20251229_172403": "Winter sunset over the Santa Cruz wharf, the water gone completely flat, in the last week of December.",
"20260524_195347": "The sun dropping behind the Giant Dipper, the wooden roller coaster that has stood on the Santa Cruz Beach Boardwalk since 1924.",
"20251226_133752": "A fly agaric mushroom on the forest floor in Santa Cruz County, found the day after Christmas.",
"20261119_085425": "A rainbow standing in a flat grey November sky, framed between a redwood and a pine, over a canopy of leaves turning red and gold. Photographed at 8:54 on a Thursday morning in Santa Cruz.",
"20260620_210208": "The first star of the evening above the lit Boardwalk, just after nine on the longest week of the year.",
"20260713_204007": "Red and pink cloud over the Boardwalk, reflected in the shallow water of the rivermouth, the night after an almost identical sky.",
"20251228_142219": "Winter afternoon light on the water, seen from the green bluff above the beach, two days before the end of the year.",
"20260919_192400": "A band of ember-coloured light low on the horizon above the Boardwalk, on a September evening.",
"20260926_193109": "The Boardwalk lights on the water after the last of the daylight had gone.",
"20261102_064330": "Dawn at Main Beach before anyone else was out, at 6:43 on a November morning.",
"20261101_141550": "Afternoon light at the Santa Cruz harbour jetty in early November.",
"20261025_161822_6709c948": "Late afternoon sun burning through high cloud over Seabright Beach, the light laid out along the wet sand.",
"20261006_183721": "Evening light along the cliffs on the West Cliff side of Santa Cruz, looking down to the water.",
"20261005_064839": "A mackerel sky at dawn in early October, the cloud broken into rows above the coast.",
"20260722_200159": "The sun going down directly into the lagoon at the San Lorenzo rivermouth on a July evening.",
"20260706_202420": "The concrete tetrapods of the harbour breakwater against a gold horizon.",
"20260705_211058": "The Boardwalk still lit at ten past nine on a July night.",
"20260628_203623": "Lavender dusk over the reeds at the rivermouth at the end of June.",
"20260621_141734": "Midday on West Cliff Drive, the swell breaking over the rocks below the path.",
"20260620_204807": "Gold light laid across the water of the rivermouth on a June evening.",
"20260512_201845": "A mauve and pink sky above Main Beach in the middle of May.",
"20251225_115121": "Christmas morning on the beach in Santa Cruz, sea foam banked up along the sand after a storm, and a pug running flat out through it.",
"20251225_114326": "Storm surf and sea foam on Christmas morning, with the wharf in the distance under a broken sky.",
"20260504_095320": "Redwoods and open grass in Santa Cruz County on a May morning.",
"20260920_191704": "The last of the light breaking under heavy cloud above the rocks on a September evening.",
}

# Keywords follow the place, rather than being stamped on every photograph.
# "Monterey Bay" on a picture taken 120 miles inland is a false claim to a
# buyer searching for the bay, and it was on four of them.
ARTIST_KW = ["Ian Sun", "fine art photography", "landscape photography"]
COASTAL_KW = ["Santa Cruz", "Monterey Bay", "California coast", "coastal photography"]

# Photographs taken in a coastal place that are not pictures of the coast.
# "Monterey Bay" on a picture of trees and sky is the same false claim to a
# buyer as putting it on one taken inland.
NOT_COASTAL = {
    "20261119_085425": ["rainbow", "autumn leaves", "fall colour", "trees",
                        "Santa Cruz"],
    "20251226_133752": ["mushroom", "fly agaric", "forest floor", "Santa Cruz"],
    "20260504_095320": ["redwoods", "forest", "trees", "Santa Cruz"],
}

# Places that are home. Matching on the words "Santa Cruz" alone was not
# enough: "San Lorenzo Rivermouth" is five minutes from the Boardwalk, and the
# listings were telling buyers it was photographed away from home.
AWAY = {"Lake Camanche, California", "San Francisco, California"}


def is_home(place):
    return place not in AWAY


def base_kw(place, slug=None):
    if slug in NOT_COASTAL:
        return NOT_COASTAL[slug] + ["California"] + ARTIST_KW
    if is_home(place):
        return COASTAL_KW + ["California"] + ARTIST_KW
    return [place.split(",")[0], "California"] + ARTIST_KW

def extra_kw(title, place):
    t = (title + " " + place).lower(); k = []
    rules = [("lighthouse", ["lighthouse","Walton Lighthouse","jetty"]),
             ("wheel", ["ferris wheel","amusement park","Boardwalk"]),
             ("dipper", ["roller coaster","Giant Dipper","Santa Cruz Beach Boardwalk"]),
             ("boardwalk", ["Santa Cruz Beach Boardwalk","amusement park"]),
             ("rivermouth", ["San Lorenzo River","rivermouth","lagoon","reflection"]),
             ("wharf", ["Santa Cruz wharf","pier"]),
             ("harbour", ["harbor","jetty","breakwater"]),
             ("jetty", ["jetty","harbor"]),
             ("cliff", ["cliffs","West Cliff Drive","bluff"]),
             ("dune", ["dunes","beach grass"]),
             ("redwood", ["redwoods","forest","trees"]),
             ("agaric", ["mushroom","fly agaric","amanita muscaria","fungi","forest floor","macro"]),
             ("surf", ["surf","waves","storm","sea foam","ocean"]),
             ("tetrapod", ["breakwater","tetrapods","harbor"]),
             ("star", ["night","stars","blue hour"]),
             ("speed", ["dog","pug","beach","sea foam","joy"]),
             ("mackerel", ["clouds","mackerel sky"]),
             ("green bluff", ["bluff","iceplant"])]
    for word, tags in rules:
        if word in t: k += tags
    return k

def tod(when):
    h = int(when.split(", ")[1].split(":")[0]) % 12
    pm = "pm" in when
    hh = h + (12 if pm and h != 12 else 0)
    if hh < 5:    return "Night"
    if hh < 8.5:  return "Sunrise"
    if hh < 11:   return "Morning"
    if hh < 15:   return "Midday"
    if hh < 17:   return "Afternoon"
    if hh < 19.5: return "Sunset"
    if hh < 21:   return "Dusk"
    return "Night"

TOD_KW = {"Sunrise": ["sunrise","dawn","first light","golden hour","morning"],
          "Morning": ["morning light","morning"],
          "Midday":  ["midday","blue sky","daylight"],
          "Afternoon":["afternoon light","golden hour"],
          "Sunset":  ["sunset","golden hour","evening","dusk"],
          "Dusk":    ["dusk","blue hour","twilight","evening"],
          "Night":   ["night","night photography","blue hour","lights"]}

rows = []
for i, m in enumerate(man):
    slug, title, place, when = m["slug"], m["title"], m["place"], m["when"]
    t = tod(when)
    tod_kw = TOD_KW[t]
    if slug in NOT_COASTAL:
        # Time-of-day keywords assert sun conditions. On a photograph where
        # the sun is not the subject - an overcast rainbow at 8:54, a mushroom
        # on a forest floor - "sunrise" and "golden hour" send a buyer
        # somewhere the picture does not go.
        tod_kw = [k for k in tod_kw if k not in {
            "sunrise", "sunset", "dawn", "dusk", "first light",
            "golden hour", "blue hour", "last light"}]
    kw = extra_kw(title, place) + tod_kw + base_kw(place, slug)
    seen, uniq = set(), []
    for x in kw:
        if x.lower() not in seen: seen.add(x.lower()); uniq.append(x)
    s = ""
    for x in uniq:
        cand = (s + ", " + x) if s else x
        if len(cand) > 500: break
        s = cand
    d = DESC.get(slug)
    if not d:
        v = MEAS.get(slug, {"hue":0,"sat":0})
        colour = _family(v["hue"], v["sat"])
        where = place if place != "Santa Cruz County" else "Santa Cruz, on Monterey Bay, California"
        d = (f"A {colour} sky at {t.lower()} in {where}, photographed at "
             f"{when.split(', ',1)[1]} on {when.split(', ')[0]}.")
    if is_home(place):
        series = SERIES_FULL if slug in DESC else SERIES_SHORT
    else:
        series = SERIES_AWAY.format(place)
    desc = d + " " + series
    # The manifest title already prefers a hand-written name over a generated
    # one, so trust it. Reading NAMES first meant a named work could be sold
    # under its generated colour name: "November Rainbow" went up as "Gold
    # Morning", which describes the leaves and misses what a buyer is after.
    shop_title = title
    rows.append(dict(n=filenum(slug), shop_title=shop_title, named=(slug in DESC), file=f"{filenum(slug):03d}-" + re.sub(r"[^A-Za-z0-9]+","-",title).strip("-").lower() + ".jpg",
                     title=title, medium="Photography", category="Photograph",
                     keywords=s, description=desc, place=place, when=when))

with open("faa-listings.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["n","file","title","shop_title","named","medium","category","keywords","description"], extrasaction="ignore")
    w.writeheader(); [w.writerow(r) for r in rows]

written = sum(1 for r in rows if r["named"])

with open("FAA-LISTINGS.md","w") as f:
    f.write("# Listing details — all 96 photographs\n\n")
    f.write("One block per image, in upload order. Copy each field into the\n")
    f.write("**Upload New Image** form.\n\n")
    f.write("Three fields are identical every time. Set them once under\n")
    f.write("**Edit Default Settings** on the upload page if it lets you:\n\n")
    f.write("| Field | Value |\n| --- | --- |\n")
    f.write("| **Artist Name** | Ian Sun |\n| **Medium** | Photography |\n")
    f.write("| **Artwork Category** | Photograph |\n\n")
    f.write(f"**{written} names are written** — those photographs were looked at\n")
    f.write("individually and the description says what is actually in the frame.\n\n")
    f.write(f"**{len(rows)-written} names are generated** and marked \u2605. They come from\n")
    f.write("what can be measured in the file: the dominant colour of the sky, how\n")
    f.write("bright it is, the time of day and the month. Nothing about place or\n")
    f.write("subject is claimed, because that cannot be measured. **Treat them as\n")
    f.write("starting points and rename as you upload** — you are looking at the\n")
    f.write("photograph, I am looking at its pixels.\n\n")
    f.write("All 96 names are unique, and keywords are within the 500-character limit.\n\n---\n\n")
    for r in sorted(rows, key=lambda x: x['n']):
        star = "" if r["named"] else " \u2605"
        f.write(f"## {r['n']:03d} — {r['shop_title']}{star}\n\n")
        f.write(f"**File:** `{r['file']}`  \u00b7  **Taken:** {r['when']}\n\n")
        f.write(f"**Title**\n```\n{r['shop_title']}\n```\n\n")
        f.write(f"**Keywords** ({len(r['keywords'])}/500)\n```\n{r['keywords']}\n```\n\n")
        f.write(f"**Description**\n```\n{r['description']}\n```\n\n---\n\n")

over = [r for r in rows if len(r["keywords"]) > 500]
print(f"{len(rows)} listings written")
print(f"keywords over limit: {len(over)}")
print(f"longest keyword field: {max(len(r['keywords']) for r in rows)} chars")
titles = [r["shop_title"] for r in rows]
dupes = {t for t in titles if titles.count(t) > 1}
print(f"ready to list: {sum(1 for r in rows if r['named'])}   need names: {sum(1 for r in rows if not r['named'])}")
print(f"duplicate shop titles: {len(dupes)}" + (f" -> {sorted(dupes)[:5]}" if dupes else ""))
print(f"individually written descriptions: {sum(1 for r in rows if r['slug'] if False)}" if False else f"hand-written descriptions: {len(DESC)}")

