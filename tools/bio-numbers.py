#!/usr/bin/env python3
"""The numbers quoted in BIOGRAPHY.md, recounted from the archive."""
import json, datetime, collections

m = json.load(open("site/gallery/manifest.json"))
d = sorted(datetime.datetime.fromisoformat(x["iso"]) for x in m)
h = collections.Counter(x.hour for x in d)
early = sum(v for k, v in h.items() if k < 8)
late  = sum(v for k, v in h.items() if k >= 17)
months = round((d[-1] - d[0]).days / 30.4)

print(f"{len(m)} photographs over {months} months "
      f"({d[0]:%-d %B %Y} to {d[-1]:%-d %B %Y})")
print(f"{late} after 5pm, {early} before 8am")
