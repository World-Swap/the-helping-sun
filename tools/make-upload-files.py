"""Full-resolution, print-ready, maximally-compatible JPEGs for upload.

Phone JPEGs carry vendor segments (Samsung writes APP4) plus ICC and XMP
blocks. Strict uploaders sometimes reject those as "wrong file type". This
re-encodes each selected photograph to a plain baseline sRGB JPEG with every
marker stripped, rotation baked in, at full resolution for printing.
"""
import os, json, re
from PIL import Image, ImageOps, ImageEnhance

SRC="photos/original"; OUT="faa-upload"
os.makedirs(OUT, exist_ok=True)
man = json.load(open("site/gallery/manifest.json"))
order = {m["slug"]: (i, m["title"]) for i, m in enumerate(man)}

def safe(t):
    return re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()

n = 0
for fn in sorted(os.listdir(SRC)):
    m = re.match(r"(\d{8}_\d{6})", fn or "")
    if not fn.endswith(".jpg") or not m or m.group(1) not in order: continue
    idx, title = order[m.group(1)]
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, fn)))   # bake rotation in
    im = im.convert("RGB")                                            # force sRGB, drop ICC
    im = ImageEnhance.Color(im).enhance(1.05)                         # match the site
    out = os.path.join(OUT, f"{idx+1:03d}-{safe(title)}.jpg")
    im.save(out, "JPEG", quality=92, optimize=True,
            progressive=False,      # baseline: the most widely accepted
            subsampling=0,          # 4:4:4, best for print
            exif=b"", icc_profile=None)
    n += 1
print(f"{n} files written to {OUT}/")
tot = sum(os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT))
print(f"total {tot/1048576:.0f} MB, largest {max(os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT))/1048576:.1f} MB (limit 25 MB)")
