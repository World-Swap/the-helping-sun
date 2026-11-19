# Drive sweep — 19 November 2026

A search of the whole Drive for high-resolution, large, vibrant photographs
not already in the gallery.

## What is there

800+ images swept. Four folders hold actual photographs:

| folder | images | >=2.5 MB |
|---|---|---|
| IANS VIEWS / LandscapePhotos | 226 | 53 |
| Marlee & I / Lake Camanche 2026 | 172 | 117 |
| Marlee & I | 192 | 37 |
| IANS VIEWS / Portrait Shots | 7 | 4 |

The rest is DiscGolfGo app assets — icons, screenshots, social cards.

## The finding, stated plainly

**There is no untapped trove.** Every photograph in the Drive is 4000x2252 —
9.0 megapixels, one camera, one resolution. No higher-resolution material
exists to be found. File size varies with scene complexity, not quality.

Measured for colourfulness (Hasler-Susstrunk) against the 98 already in the
gallery, the best new candidates rank:

| candidate | score | vs. the current 98 |
|---|---|---|
| 20260712_203927 Boardwalk, crimson sky | 46.9 | 75th percentile |
| 20260916_192350 Lake Camanche oaks | 34.7 | 42nd |
| 20261110_065828 sunrise, cypress, lighthouse | 31.4 | 34th |
| 20261106_061817 pool steam, crescent moon | 26.7 | 22nd |
| 20261116_171844 blue hour reflection | 22.8 | 16th |
| 20251225_172349 Christmas storm surf | 9.6 | 0th |

For reference the current gallery runs 10.0 to 68.8, median 36.3.

The gallery already holds the best of what exists. The 98 are the crop, not
the remainder.

## Loose ends

- **`20260522_114209.jpg`, 17.9 MB**, in LandscapePhotos — by a wide margin
  the largest file in the Drive. The Drive download tool caps at 10 MB, so it
  has never been opened. If it is a panorama or a stitched frame it would be
  the highest-resolution listing in the shop. Worth opening by hand.
- **"Marlee & I" was left alone.** It holds the most large files, but it is a
  personal album, not a body of work; one frame from the Lake Camanche trip
  (the oaks) is a genuine landscape and is listed above. Its "Adults Only"
  subfolder was not opened and must not be. Going back in for scenery only is
  Ian's call to make, not an assumption to act on.

## Method

- Enumerate: `mimeType contains 'image/'`, paged, into a title/id/size/parent table.
- Cluster burst frames into scenes on a 90–120 second gap, keep the largest
  frame per scene. 62 golden-hour Camanche frames collapsed to 14 scenes;
  145 unused LandscapePhotos to 63.
- Judge colour on pixels, never on the filename or the time of day.
