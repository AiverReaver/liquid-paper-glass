# Worked example: Silksong-inspired "Hearthrise"

One world filled in. Replace with yours. It proves the contract, it is not outside validation; the values are tuned by eye. It was built in the author's private Flutter app (palette extension, shared tilt notifier, glass surface painter).

## What it chose

- **World:** Hollow Knight: Silksong, five themes (Pharloom, Deep Docks, Choral Chambers, Moss Grotto, Greymoor). Two light, three dark. Full world file: `templates/world.example.json` (Pharloom).
- **Layer split:** content = "needle-cut" paper (1 px edge, radii 8/6/4, solid fill). Chrome = glass: back/profile/settings circles, floating tab bar, sheets, alerts, switches, the hold button and the strike-result panel.
- **Glass:** blur sigma 16, saturation 1.7, fill white 8% (dark) or paper-white 60% (light), pressed 16% / 90%. 2 px ink key line outside, 5 px bottom inner shadow, 1 px inner ring, diagonal sheen, conic rim, small glint.
- **Light:** one `GlassTilt` notifier shared by all glass; idle drift; frozen under reduced motion. Painter repaints alone.
- **Press:** scale 1.04, 350 ms ease-out-back, glass-only (the paper rule forbids overshoot).
- **Type:** Cormorant Garamond display + Hanken Grotesk UI.
- **Motion:** paper redraws held in 140 ms steps; glass continuous.
- **High contrast:** flat shell fill, no blur, no sheen, key line kept.

## Light vs dark

Choral (light): fill `#FFFAF0` 60%, key `#2A1E0F`. Pharloom (dark): white 8%, key `#050307`. Brightness is chosen per world, never inverted.

## Findings from running the gate on Pharloom

`check_world.py` PASSes with warnings: muted text on pressed glass over `raised` is 3.89:1; strong label over a glass-over-accent hero is 2.71:1; ink key line is ~1.0:1 against dark paper so the edge relies on the lit rim. These are the real risks of the example.

## Swapping to another game

Keep every file except the world file. Change `id`, `inspiredBy`, `brightness`, all hexes, optionally type pair and cut tiers. Re-run the gates. Done.
