---
name: liquid-paper-glass
description: Use when building or restyling an app or site UI that combines Apple iOS 26 Liquid Glass chrome with a themed opaque paper/ink content layer, when theming a UI on any game, film, book or other world (Hades, Hollow Knight, Zelda, Studio Ghibli) with swappable palettes, or when choosing glass, palette, shape, type and motion independently and mixing them.
---

# Liquid Paper Glass

## Overview

A **contract, not a look.** Two layers and six independent axes. Any world (a game, a film, a place) fills the axes; the layer rules and gates stay fixed.

- **Paper** = opaque content: cards, rows, fields, pages, art, body type. Solid fill, ink outline, no blur.
- **Glass** = floating chrome: tab bar, circle buttons, sheets, alerts, switches, confirm panels. Blur + tint + lit rim + ink key line.

This matches Apple's own split (functional layer vs content layer). Apple publishes almost no numbers, so every value here is a labeled tuning start: **[SRC]** sourced, **[INF]** inference, **[TUNE]** adjust by eye.

For native SwiftUI glass API detail, also see `ecc:liquid-glass-design`. This skill adds themed worlds, the paper layer, cross-platform tiers and gates.

## Workflow

1. **World + IP preflight.** Name the world. Take palette and mood only, never art, logos, sprites, original fonts or official names. See `references/world-to-theme.md`.
2. **Write a world file.** Copy `templates/world.example.json`; replace every hex with a literal. Never derive roles at build time.
3. **Pick the six axes** (preset or mix, below).
4. **Pick the platform tier** (premium / standard / flat) from `references/platform-recipes.md`.
5. **Build the parts** in order: tokens, paper frame, glass surface, light, chrome parts. Details: `references/glass-material.md`, `references/paper-layer.md`.
6. **Run the gates:** `python3 templates/check_world.py my-world.json`, then the rest of `references/gates-and-tests.md`.
7. **Do the manual checks** listed there. Device feel, 200% text and OS toggles cannot be automated.

## The six axes (independent)

| Axis | Chooses | Default start |
|---|---|---|
| World palette | 15 paper roles + 4 glass roles, hex literal per brightness | from the world |
| Glass variant | Regular / Tinted / Flat; blur, fill, rim, saturation | Tinted over paper [INF] |
| Paper cut | radius tiers, stroke, shadow, jitter | tiers 8/6/4, 1 px edge |
| Type pairing | one display + one text family | serif display + grotesk UI |
| Motion | paper stepping vs glass spring | paper on twos, glass spring |
| Light | ONE shared vector, global | upper-left, tilt -1..1 |

Mix is safe only if the gates pass. Presets are curated; "mix" mode runs the gates and warns instead of blocking.

## Hard rules (Apple [SRC] unless noted)

- Glass only as floating chrome. Never on content rows. Exception: a switch or slider thumb may turn glass while pressed.
- **Never glass on glass.** Never mix Regular and Clear.
- **Tint only the one primary action**, by its background, never its glyph.
- Capsule radius = height/2. Nested radius = parent radius minus padding.
- Hit target >= 44 pt. No Thin/Light weights on glass.
- Clear glass over bright content needs a 35% dark dim; skip it over dark content.
- Ship the flat tier and Reduce Transparency / Increase Contrast / Reduce Motion states for every glass part. They are first-class, not a fallback.
- One light drives every rim, sheen, inner shadow and paper shadow [INF].
- Chrome never loops animation on its own. Only input-driven motion.

## Common mistakes

| Mistake | Fix |
|---|---|
| Blur on cards "for consistency" | Cards are paper. Blur only chrome. |
| Palette derived from a seed color | Pin literal hexes; seeds drift every role. |
| Two light directions (CSS shadow vs rim) | One light token feeds all. |
| Ink key line near-black on a dark paper | It vanishes; rely on lit rim or lighten ink, re-check 3:1. |
| Label over accent-colored hero | Scrim it or move chrome; `check_world.py` WARNs this. |
| Calling plain blur + border "Liquid Glass" | It is glassmorphism until it has a lit rim and press response. |
| Copying a game's logo, font or sprites | Palette and mood only. |

## Red flags: stop

"It looks fine on my screenshot" (no gate run) · "Reduce Transparency is a later task" · "just this one card gets glass" · "I'll hand-tune this hex per screen".
