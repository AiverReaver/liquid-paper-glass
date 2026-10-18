# Platform recipes

One ladder everywhere: **premium** (real refraction) -> **standard** (blur + saturate + rim + key line) -> **flat** (opaque scrim + key line). Implement standard first; add premium behind a capability check; flat is one switch away.

| Platform | Premium | Standard | Flat trigger |
|---|---|---|---|
| SwiftUI/UIKit | `glassEffect(.regular.tint(_).interactive(), in: shape)` in one `GlassEffectContainer`; `glassEffectID` + `@Namespace` to morph; `.buttonStyle(.glass)` / `.glassProminent` | `if #available(iOS 26, *)` else `.background(.ultraThinMaterial, in: shape)` + manual tint, rim, key line | System honours Reduce Transparency etc. for native glass |
| Flutter | `liquid_glass_renderer` (Impeller only, pre-release, 16 shapes/group) or `liquid_glass_widgets`; gate on `ImageFilter.isShaderFilterSupported` | `BackdropFilter` + `ImageFilter.compose(outer: saturateMatrix, inner: blur)`, tint, `CustomPainter` rim/key, `ClipPath`; group with `BackdropGroup` / `BackdropFilter.grouped` | `MediaQuery.highContrastOf`, `disableAnimationsOf`; Reduce Transparency needs a platform channel |
| Web | SVG `feDisplacementMap` via `backdrop-filter: url(#lens)` (Chromium only) | `backdrop-filter: blur(16px) saturate(1.7)` + fill + inset rim | `prefers-reduced-transparency`, `prefers-contrast: more`, `@supports not (backdrop-filter: blur(1px))` |
| Compose | Haze `hazeGlass` (v2 beta) | `Modifier.hazeSource` / `hazeBlur` with tint + border | min API unverified; fall back to opaque below blur support |
| React Native | `expo-glass-effect` `GlassView`, `@callstack/liquid-glass` (iOS 26 only) | `expo-blur` or translucent View | `isLiquidGlassAvailable()`, `AccessibilityInfo.isReduceTransparencyEnabled()` |

Unverified: `glassEffectUnion`, `UIDesignRequiresCompatibility`, UIKit class names, Haze minimum API, expo-blur details. Check headers/docs before relying on them.

## Web: standard tier (one example)

```css
.glass {
  position: relative; isolation: isolate; overflow: hidden;
  border-radius: var(--r);                       /* capsule: height/2 */
  background:
    linear-gradient(var(--glass-scrim), var(--glass-scrim)),  /* paper-tone scrim, alpha .55-.8 */
    var(--glass-fill);                           /* alpha token */
  backdrop-filter: blur(16px) saturate(1.7);
  box-shadow:
    0 0 0 1.5px var(--glass-key),                /* ink key line */
    inset 0 -5px 0 -1px color-mix(in srgb, var(--glass-key) 28%, transparent),
    0 8px 28px rgb(0 0 0 / .35);
  transition: transform 350ms cubic-bezier(.34,1.56,.64,1);
}
.glass:active { transform: scale(1.04); background: var(--glass-fill-hi); }
.glass::after {                                   /* rim, follows --tilt-x (-1..1) */
  content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
  /* CSS conic angles: 0deg = up, clockwise. Canvas/Flutter sweep: 0 = right, so subtract 90deg there. */
  background: conic-gradient(from calc(230deg + var(--tilt-x) * 40deg),
    var(--glass-light) 0 18%, transparent 18% 50%,
    rgb(255 255 255 / .22) 50% 62%, transparent 62%);
  mask: linear-gradient(#000 0 0) content-box exclude, linear-gradient(#000 0 0);
  padding: 2px;
}
@media (prefers-reduced-transparency: reduce), (prefers-contrast: more) {
  .glass { background: var(--paper-surface); backdrop-filter: none; }
}
@supports not (backdrop-filter: blur(1px)) {
  .glass { background: var(--paper-surface); }
}
@media (prefers-reduced-motion: reduce) { .glass { transition: none } .glass:active { transform: none } }
```

## Traps

- Web: a parent with `filter`, `opacity < 1`, `mask`, `clip-path` or `mix-blend-mode` bounds the child's backdrop. `prefers-reduced-transparency` ships in Chromium only, so back it with `prefers-contrast` and a manual toggle.
- Flutter: `ImageFilter.shader` throws when Impeller is off. Flutter does not expose iOS Reduce Transparency; high contrast is only a proxy.
- Refraction only inside the element box on web. Spill past the edge is not reproducible.
- `feTurbulence` recipes give a random wobble, not a lens.

## Performance [INF, no published benchmarks]

2-4 blurred surfaces per screen. Never glass inside list rows. Share one backdrop pass. Skip blur (`blur: 0`) where glass sits on a known flat fill, such as a hold button on a row. Snapshot-blur sheets over static content. Measure on a low-end Android device.
