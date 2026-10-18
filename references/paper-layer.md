# Paper layer

The content layer. Everything here is **opaque**: no blur, no translucency.

## Five traits [INF from practitioner sources]

1. Opaque flat fills from `surface` / `raised`.
2. One consistent ink line weight (`seam` at rest, 1 px; neobrutalist variant 2-5 px).
3. Hard shadow: zero blur, offset away from the shared light.
4. Slight irregularity: jittered corners or fill/line misregistration. Static, not animated.
5. Editorial type: a serif or distinctive display face over a clean grotesk for UI.

## Hand-cut jitter

Generate once per card from a stable seed (the card id), never per frame. Flutter: a `ShapeBorder` with 4 corner offsets of 0-1.5 px. Web: `clip-path: polygon(...)` with the corners nudged by the seeded offsets (`--j1`..`--j4`), set inline once. Jitter must not clip text: keep it inside the card padding. It is decoration; the DOM text stays real.

## Cut (shape language)

Three radius tiers, `const` across all worlds: lg 8 panels/sheets, md 6 rows/buttons/fields, sm 4 tags. State changes the **edge colour**, never the shape: seam at rest, accent on selection, strong when a hold is ready, deep on featured panels. Ornaments stay pointed (diamond pips, skewed shards). A world may swap tiers (soft rounded vs hard cut) as the Paper-cut axis.

## Type

Max two families. One display (titles, names, lessons), one text face (UI, data). A small uppercase label style (12 px, 600, +1.6 tracking) only for meter labels. Avoid light weights on or near glass.

## Grain

Optional. One static tiled texture under a repaint boundary, never animated (an animating layer defeats raster caches). Verify on OLED. Grain must not lower text contrast; gate with the contrast check over the grain's worst pixel.

## Motion

Paper moves in **held steps** (stop-motion, "on twos": ~140 ms steps, 3-7 frames), not eases. Glass springs. The contrast between the two is the personality. Reduce Motion: paper becomes instant or a single crossfade.

## Where paper meets glass

- Glass floats over paper; paper never overlaps its own glass chrome except under a scroll-edge fade.
- Chrome scrim = paper tone so edges blend, key line = paper ink so one world reads.
- Dark paper: near-black key lines vanish. Lighten ink or lean on the lit rim; re-check 3:1.
- Light paper: ink key line is strong; keep glass fill 0.55-0.65 so labels stay >= 4.5:1.
