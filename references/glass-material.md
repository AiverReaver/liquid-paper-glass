# Glass material

Apple publishes physics and rules, not numbers. Values are **[TUNE]** starts unless marked.

## Layer stack, bottom to top [INF]

1. Drop shadow, cut out under the glass so it never shows through. Black ~0.35, blur ~14, offset away from the light.
2. Clip to the shape.
3. Backdrop blur + saturation (blur 12-20, saturate 1.6-1.8).
4. Paper-tone scrim (the world-coloured version of Apple's dim layer) 0.55-0.8.
5. Fill (`glass.fill`). Tint (`accent` at ~0.55) only on the primary action.
6. Child content (glyph/label).
7. Inner depth: bottom inner shadow (key at ~0.28, ~5 px) and a 1-2 px inner ring (white ~0.16).
8. Sheen: hard-edged diagonal band on the top third, white ~0.14, angle 152 deg + 14 deg x tilt.
9. Rim: 2-4 px conic stroke, bright arc `glass.light` ~18% of the circumference starting at 230 deg + 40 deg x tilt, faint opposite arc.
10. **Ink key line**, 1.5-2 px, `glass.key`, outside the shape. It makes glass read as an object and adds the edge boundary that plain Apple glass lacks.
11. Optional glint: small top-left arc + dot, rotates up to 9 deg with tilt.

Larger glass = deeper shadow, stronger lensing [SRC]. Keep gaps between glass items >= 8 px.

**Angle convention:** angles above are CSS (0 = up, clockwise). In Flutter `SweepGradient` / canvas (0 = right) subtract 90 deg.

**Dark worlds: key line recipe.** A near-black key line on near-black paper measures ~1.0:1 and only reads as a shadow. Keep `glass.key = ink` for object-ness, and let the lit rim carry the 3:1 edge (`check_world.py` WARNs when it does). If the rim is also weak, add a 1 px outer hairline of `strong` at ~0.35 alpha outside the key line, or tint the rim with the world's metal (gold, silver) [INF].

## One light (tilt)

One value, each axis -1..1, shared by every glass part and paper shadow. Sources in priority: device sensor, pointer, idle drift. Idle drift after ~2.5 s of no input: `x = sin(0.7 t) * 0.8`, `y = cos(0.5 t) * 0.5`, eased 12% per 60 Hz frame (frame-rate independent) [REPO]. Painting reads tilt through a repaint listenable, so only the painter repaints. Reduce Motion: tilt frozen at 0.

## States

| State | Trigger | Treatment |
|---|---|---|
| Regular | default | stack above |
| Tinted | user toggle (mirrors iOS 26.1) | fill 0.5-0.7, stronger rim, same key line |
| Reduce Transparency | OS flag / toggle | scrim ~1.0, no blur, key line kept |
| Increase Contrast | high-contrast flag | flat fill, key line 2 px, no sheen |
| Reduce Motion | OS flag | light frozen, no drift, springs lose overshoot, paper steps become instant |

Default for a paper world should be the Tinted equivalent [INF].

## Press motion

Scale 1.04 (range 1.03-1.08), fill -> `fillHi`, ~350 ms ease-out-back, release same curve. Neighbour glass rim +0.1 for ~300 ms. Materialize/dismiss: animate blur strength, not just opacity. No shimmer while scrolling, no wiggling tab bar (NN/g).

## Geometry

Tab bar: floating capsule, 62 px tall, 21 px from sides, ~19 px above the bottom inset, radius 31, 4 equal items, 11 px labels, single-word labels. Circle buttons: 44 visible in a 48 hit area. Sheet: grabber, medium/large detents, radius ~32-40. Alert: ~270-300 wide, <= 3 actions, verb titles. Scroll edge: 24-40 px soft fade or paper strip instead of a divider so text never runs under chrome.

## Legibility

Text over glass needs a scrim over the worst-case backdrop: >= 4.5:1 text, >= 3:1 icons. Never put text on glass over illustration without a scrim. Avoid steady-state intersections of text and glass edges.
