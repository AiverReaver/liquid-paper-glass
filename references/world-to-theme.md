# World to theme

Turns any source world (game, film, book, place) into a world file. Silksong is only the worked example in `worked-example-silksong.md`.

## Pipeline [INF]

1. **Collect** 5-15 official-style references you may legally view (screenshots, promo art, trailers). Note each in the provenance list.
2. **Extract candidates.** Quantize (Material Color Utilities uses Celebi: Wu then WSMeans, then a UI-suitability score) or k-means in OKLab. Weight by chroma so small accents survive. Candidates are proposals only.
3. **A human assigns roles.** Do not accept generated roles.
4. **Store literal hexes** per theme and per brightness. Do not call `fromSeed`-style generators at build time: they re-derive every role and pinned hexes drift.
5. **Run the gates** (`gates-and-tests.md`). Adjust lightness, not hue, until roles pass.
6. **Log provenance:** `{role, source, derived}` per role.

Expect thin sources. Silksong has no published area colors; only ~12 of ~30 areas have any visual description. Sample real screenshots; never trust recalled colors.

## Roles (15 paper + 4 glass)

| Role | Use |
|---|---|
| canvas | deepest background / void |
| ground | page gradient end |
| surface | default panel fill |
| raised | selected / elevated paper |
| seam | hairline edge at rest |
| ink | key line, outlines, text-on-light |
| text | body text |
| strong | titles, selected text |
| muted | secondary text (>= 4.5:1) |
| faint | disabled, decor only |
| accent / accentHi | the one primary tint / its hover |
| onAccent | label on accent (>= 4.5:1) |
| deep | featured-panel edge |
| signal | meter / status mark (>= 3:1 on surface) |
| glass.fill / fillHi | resting / pressed glass fill (alpha) |
| glass.light | lit rim colour (alpha) |
| glass.key | ink key line (default = ink) |

Dark worlds: white fill ~0.05-0.15 alpha. Light worlds: paper-tinted white ~0.55-0.65, pressed ~0.9 [INF, from a shipped app]. Choose each brightness explicitly; do not invert.

## Naming themes

Biomes, zones, chapters, seasons: any list. Each theme = one full world file. Adding a theme appends to the end (stored as int/enum); it never renames. Cross-fade between themes by lerping each role (OKLab lerp avoids sRGB mud) [INF].

## IP preflight (practical guidance, not legal advice) [INF]

- Take palette and mood. Do not ship logos, sprites, screenshots, lifted icons, sounds or original fonts.
- Use generic evocative theme names ("Underworld", "Moss Grotto"-style), not official trademarks, in the product UI.
- Use OFL/Apache fonts that match the mood (e.g. a high-contrast serif for display).
- Keep the provenance manifest. Credit "feel, never its art, characters or fonts".
- User-built "own world" features ship only original presets.
- Fan work is an unlicensed derivative; commercial use raises takedown risk. Tell the user this once.

## Color-blind rule

Every pair of states that differ only by hue must also differ by >= 3:1 luminance **and** carry a non-color cue (icon, label, shape). Hue-only coding fails [INF].
