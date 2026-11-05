import os, base64, io, json
from PIL import Image, ImageFilter
SRC="/home/user/the-helping-sun/photos/original"; OUT="/home/user/the-helping-sun/site/img"
os.makedirs(OUT, exist_ok=True)
PICKS=[
 ("20261104_064349.jpg","sunrise-lighthouse","Sunrise over Monterey Bay with Walton Lighthouse on the jetty","Nov 4, 2026 · 6:43 am",(2400,1400,800)),
 ("20261021_071526.jpg","fire-morning","A morning sky burning pink and orange above the park","Oct 21, 2026 · 7:15 am",(1600,800)),
 ("20260529_203449.jpg","ferris-wheel","The Boardwalk ferris wheel in silhouette against a peach dusk","May 29, 2026 · 8:34 pm",(1600,800)),
 ("20260712_204036.jpg","crimson-rivermouth","Crimson clouds over the Boardwalk, mirrored in the rivermouth","Jul 12, 2026 · 8:40 pm",(1600,800)),
 ("20260524_195347.jpg","golden-coaster","The sun dropping behind the Giant Dipper","May 24, 2026 · 7:53 pm",(1600,800)),
 ("20260722_200159.jpg","sun-into-lagoon","The sun going down into the lagoon at the rivermouth","Jul 22, 2026 · 8:01 pm",(1600,800)),
 ("20260926_193109.jpg","night-lights","Boardwalk lights on the water after dark","Sep 26, 2026 · 7:31 pm",(1600,800)),
 ("20260628_203623.jpg","lavender-dusk","Lavender dusk over the reeds at the rivermouth","Jun 28, 2026 · 8:36 pm",(1600,800)),
]
man=[]
for fn,slug,alt,when,widths in PICKS:
    p=os.path.join(SRC,fn)
    if not os.path.exists(p): print("MISSING",fn); continue
    im=Image.open(p).convert("RGB"); w,h=im.size
    for width in widths:
        if width>w: continue
        r=im.resize((width,round(h*width/w)), Image.LANCZOS)
        r.save(os.path.join(OUT,f"{slug}-{width}.jpg"),"JPEG",quality=72,optimize=True,progressive=True)
    tiny=im.resize((18,max(1,round(h*18/w))),Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
    b=io.BytesIO(); tiny.save(b,"JPEG",quality=35)
    man.append({"slug":slug,"alt":alt,"when":when,"w":w,"h":h,"widths":list(widths),
                "lqip":"data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()})
json.dump(man,open(os.path.join(OUT,"manifest.json"),"w"),indent=1)
for m in man: print(f"{m['slug']:<20} {m['w']}x{m['h']}  lqip={len(m['lqip'])}b")
