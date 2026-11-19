
import json, csv, re, datetime

man = json.load(open("site/gallery/manifest.json"))
SERIES_FULL = ("Part of a year-long series photographed entirely within a few miles "
               "of home in Santa Cruz County, California, and made on a phone.")
SERIES_SHORT = ("Part of a year-long series photographed within a few miles of home, "
                "and made on a phone.")

# Individual descriptions for the named works.
DESC = {
"20261104_064349": "Sunrise over Monterey Bay, with Walton Lighthouse standing on the jetty and the tide pooled across the sand. Taken at 6:43 on a November morning, the third consecutive dawn of a run of early starts.",
"20260712_204036": "Crimson cloud breaking over the Santa Cruz Beach Boardwalk, mirrored in the still water of the San Lorenzo rivermouth on a July evening.",
"20261021_071526": "The whole sky turned pink and orange over a park ten minutes from my front door, a little after seven on an October morning.",
"20260529_203449": "The ferris wheel at the Santa Cruz Beach Boardwalk in silhouette against a peach-coloured dusk.",
"20251229_172403": "Winter sunset over the Santa Cruz wharf, the water gone completely flat, in the last week of December.",
"20260524_195347": "The sun dropping behind the Giant Dipper, the wooden roller coaster that has stood on the Santa Cruz Beach Boardwalk since 1924.",
"20251226_133752": "A fly agaric mushroom on the forest floor in Santa Cruz County, found the day after Christmas.",
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

BASE_KW = ["Santa Cruz", "California", "Monterey Bay", "California coast",
           "coastal photography", "Ian Sun", "fine art photography", "phone photography"]

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
    kw = extra_kw(title, place) + TOD_KW[t] + BASE_KW
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
        where = place if place != "Santa Cruz County" else "Santa Cruz County, California"
        d = f"{t} in {where}, photographed at {when.split(', ',1)[1]} on {when.split(', ')[0]}."
    desc = d + " " + (SERIES_FULL if slug in DESC else SERIES_SHORT)
    if slug in DESC:
        shop_title = title
    else:
        day_month = " ".join(when.split(", ")[0].split()[:2])
        shop_title = f"{title} \u2014 {day_month}"
    rows.append(dict(n=i+1, shop_title=shop_title, named=(slug in DESC), file=f"{i+1:03d}-" + re.sub(r"[^A-Za-z0-9]+","-",title).strip("-").lower() + ".jpg",
                     title=title, medium="Photography", category="Photograph",
                     keywords=s, description=desc, place=place, when=when))

with open("faa-listings.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["n","file","title","shop_title","named","medium","category","keywords","description"], extrasaction="ignore")
    w.writeheader(); [w.writerow(r) for r in rows]

ready = [r for r in rows if r["named"]]
later = [r for r in rows if not r["named"]]

with open("FAA-LISTINGS.md","w") as f:
    f.write("# Listing details\n\n")
    f.write(f"**{len(ready)} photographs are ready to list.** Each has a real name, real\n")
    f.write("keywords and a written description. Copy the fields straight into the\n")
    f.write("**Upload New Image** form.\n\n")
    f.write(f"The other {len(later)} are listed at the end **without names**, on purpose.\n")
    f.write("See the note there before you list any of them.\n\n")
    f.write("Two fields are the same every time:\n\n")
    f.write("| Field | Value |\n| --- | --- |\n")
    f.write("| **Artist Name** | Ian Sun |\n| **Medium** | Photography |\n| **Artwork Category** | Photograph |\n\n")
    f.write("Set those once under **Edit Default Settings** on the upload page if it\n")
    f.write("lets you — that link is very likely where apply-to-all lives, so check it\n")
    f.write("before typing anything 96 times.\n\n")
    f.write("Keywords are kept under the 500-character limit. Descriptions are in\n")
    f.write("complete sentences, as the form asks.\n\n---\n\n")
    f.write("# Ready to list\n\n")
    for r in ready:
        f.write(f"## {r['n']:03d} — {r['shop_title']}\n\n")
        f.write(f"**File:** `{r['file']}`\n\n")
        f.write(f"**Title**\n```\n{r['shop_title']}\n```\n\n")
        f.write(f"**Keywords** ({len(r['keywords'])}/500)\n```\n{r['keywords']}\n```\n\n")
        f.write(f"**Description**\n```\n{r['description']}\n```\n\n---\n\n")

    f.write("""# The remaining photographs — name these before listing

These have no real names, and that is deliberate.

A shop with thirty photographs called "Sunrise" sells nothing. It reads as a
camera roll rather than a body of work, and buyers scroll past it. The archive
on your own site is the right home for volume, because there it shows a year of
turning up. A shop wants selection.

**My advice: list the %d named works and stop there.** That is almost exactly
the free tier's 25-image limit, and they are the strongest frames anyway.

If you want to add more later, name them a handful at a time as you go — tell
me which numbers and I will open each one properly and write a name and a
description for it. What I will not do is invent names for ninety-six
photographs I have only seen in contact sheets. That is how one of them ended
up called "Boardwalk, Reflected" when it was a rooftop and a tree.

Each entry below has its file, date, time and keywords ready. Only the name and
the description are missing.

""" % len(ready))
    for r in later:
        f.write(f"## {r['n']:03d} — *(needs a name)*\n\n")
        f.write(f"**File:** `{r['file']}`  ·  **Taken:** {r['when']}\n\n")
        f.write(f"**Keywords** ({len(r['keywords'])}/500)\n```\n{r['keywords']}\n```\n\n---\n\n")

over = [r for r in rows if len(r["keywords"]) > 500]
print(f"{len(rows)} listings written")
print(f"keywords over limit: {len(over)}")
print(f"longest keyword field: {max(len(r['keywords']) for r in rows)} chars")
titles = [r["shop_title"] for r in rows]
dupes = {t for t in titles if titles.count(t) > 1}
print(f"ready to list: {sum(1 for r in rows if r['named'])}   need names: {sum(1 for r in rows if not r['named'])}")
print(f"duplicate shop titles: {len(dupes)}" + (f" -> {sorted(dupes)[:5]}" if dupes else ""))
print(f"individually written descriptions: {sum(1 for r in rows if r['slug'] if False)}" if False else f"hand-written descriptions: {len(DESC)}")

