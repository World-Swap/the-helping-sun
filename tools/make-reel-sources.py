"""Cut 9:16 vertical masters from the full-res originals, framed on the sun."""
import os, colorsys
import numpy as np
from PIL import Image, ImageEnhance

SRC="photos/original"; OUT="reels/src"
os.makedirs(OUT, exist_ok=True)
PHOTOS = [
 ("20261104_064349.jpg","sunrise-lighthouse"), ("20261021_071526.jpg","fire-morning"),
 ("20260529_203449.jpg","ferris-wheel"),       ("20260712_204036.jpg","crimson-rivermouth"),
 ("20260524_195347.jpg","golden-coaster"),     ("20260722_200159.jpg","sun-into-lagoon"),
 ("20260926_193109.jpg","night-lights"),       ("20260628_203623.jpg","lavender-dusk"),
 ("20260919_192400.jpg","ember-band"),         ("20260622_211835.jpg","deep-night"),
 ("20260706_202420.jpg","rocks-dusk"),         ("20261005_064839.jpg","mackerel-dawn"),
 ("20260512_201110.jpg","pale-dusk"),
]
for fn, slug in PHOTOS:
    p = os.path.join(SRC, fn)
    if not os.path.exists(p):
        print("MISSING", fn); continue
    im = Image.open(p).convert("RGB"); w, h = im.size
    # frame horizontally on the brightest part of the sky (the sun)
    a = np.asarray(im.resize((400, round(h*400/w)))).astype(float).mean(axis=2)
    sky = a[:int(a.shape[0]*0.55)]
    xs = np.where(sky >= np.percentile(sky, 99.5))[1]
    cx = (xs.mean()/400) if len(xs) else 0.5
    cw = round(h * 9/16)                      # full height, 9:16 wide
    left = int(min(max(cx*w - cw/2, 0), w - cw))
    c = im.crop((left, 0, left+cw, h))
    c = ImageEnhance.Color(c).enhance(1.08)
    c.save(os.path.join(OUT, f"{slug}.jpg"), "JPEG", quality=88, optimize=True)
    print(f"{slug:<20} {c.size[0]}x{c.size[1]}  framed at x={cx:.2f}")
