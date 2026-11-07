"""Build gallery images + manifest from photos/original."""
import os, json
from PIL import Image, ImageOps, ImageEnhance

SRC="photos/original"; OUT="site/gallery"
os.makedirs(OUT, exist_ok=True)

# file, slug, title, when, place
PICKS = [
("20261104_064349.jpg","first-light","First Light","4 November 2026, 6:43 am","Walton Lighthouse, Santa Cruz"),
("20261021_071526.jpg","caught-fire","The Morning It Caught Fire","21 October 2026, 7:15 am","Santa Cruz"),
("20261005_064839.jpg","mackerel-sky","Mackerel Sky","5 October 2026, 6:48 am","West Cliff, Santa Cruz"),
("20261102_064330.jpg","before-anyone","Before Anyone Else","2 November 2026, 6:43 am","Main Beach, Santa Cruz"),
("20260712_204036.jpg","crimson","Crimson Rivermouth","12 July 2026, 8:40 pm","San Lorenzo Rivermouth"),
("20260713_204007.jpg","night-after","The Night After","13 July 2026, 8:40 pm","San Lorenzo Rivermouth"),
("20260524_195347.jpg","giant-dipper","Behind the Giant Dipper","24 May 2026, 7:53 pm","Beach Boardwalk, Santa Cruz"),
("20260529_203449.jpg","the-wheel","The Wheel","29 May 2026, 8:34 pm","Beach Boardwalk, Santa Cruz"),
("20260620_204807.jpg","gold-on-water","Gold on the Water","20 June 2026, 8:48 pm","San Lorenzo Rivermouth"),
("20260620_210208.jpg","first-star","First Star","20 June 2026, 9:02 pm","Main Beach, Santa Cruz"),
("20260512_201845.jpg","mauve","Mauve","12 May 2026, 8:18 pm","Main Beach, Santa Cruz"),
("20260919_192400.jpg","ember-band","Ember Band","19 September 2026, 7:24 pm","Main Beach, Santa Cruz"),
("20260926_193109.jpg","after-the-light","After the Light Went","26 September 2026, 7:31 pm","Santa Cruz"),
("20260712_210904.jpg","reflected","Boardwalk, Reflected","12 July 2026, 9:09 pm","San Lorenzo Rivermouth"),
("20260722_200159.jpg","into-the-lagoon","Into the Lagoon","22 July 2026, 8:01 pm","San Lorenzo Rivermouth"),
("20260628_203623.jpg","lavender","Lavender at the Reeds","28 June 2026, 8:36 pm","San Lorenzo Rivermouth"),
("20260705_211058.jpg","late","Late","5 July 2026, 9:10 pm","Main Beach, Santa Cruz"),
("20260620_204117.jpg","the-dunes","The Dunes","20 June 2026, 8:41 pm","Santa Cruz"),
("20260621_141734.jpg","west-cliff","West Cliff, Midday","21 June 2026, 2:17 pm","West Cliff Drive, Santa Cruz"),
("20260706_202420.jpg","tetrapods","The Tetrapods","6 July 2026, 8:24 pm","Santa Cruz Harbour"),
("20261006_183721.jpg","cliffside","Cliffside","6 October 2026, 6:37 pm","West Cliff, Santa Cruz"),
("20261025_161822_6709c948.jpg","sun-through","Sun Through","25 October 2026, 4:18 pm","Seabright Beach, Santa Cruz"),
("20261101_141550.jpg","afternoon-jetty","Afternoon, Jetty","1 November 2026, 2:15 pm","Santa Cruz Harbour"),
("20260504_095320.jpg","the-redwoods","The Redwoods","4 May 2026, 9:53 am","Santa Cruz County"),
]

def fit(im, longest):
    w, h = im.size
    s = longest / max(w, h)
    if s >= 1: return im.copy()
    return im.resize((round(w*s), round(h*s)), Image.LANCZOS)

man = []
for fn, slug, title, when, place in PICKS:
    p = os.path.join(SRC, fn)
    if not os.path.exists(p):
        print("MISSING", fn); continue
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")   # honour EXIF rotation
    im = ImageEnhance.Color(im).enhance(1.05)
    big = fit(im, 1600);  big.save(f"{OUT}/{slug}.jpg", "JPEG", quality=76, optimize=True, progressive=True)
    th  = fit(im, 760);   th.save(f"{OUT}/{slug}-t.jpg", "JPEG", quality=74, optimize=True, progressive=True)
    man.append({"slug":slug,"title":title,"when":when,"place":place,
                "w":th.size[0],"h":th.size[1],
                "orient":"portrait" if th.size[1] > th.size[0] else "landscape"})
json.dump(man, open(f"{OUT}/manifest.json","w"), indent=1)
print(f"{len(man)} images")
for m in man[:3]: print(" ", m["slug"], m["w"], "x", m["h"], m["orient"])
