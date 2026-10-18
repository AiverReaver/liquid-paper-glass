# Gates and tests

Test first. A world is not done until every gate passes and the manual list is checked.

## Automated gates

| Gate | Check | Failing means |
|---|---|---|
| Role contrast | per world x brightness: text, strong, muted, onAccent on their fills >= 4.5; accent, signal vs surface >= 3 | illegible palette |
| Glass worst case | composite glass fill over canvas/ground/surface/raised, label >= 4.5, in Regular, Tinted, Reduce Transparency, High Contrast | glass incompatible with this world |
| Glass edge | key line OR lit rim vs surround >= 3:1 | glass has no visible boundary |
| Pinned hexes | each role equals its declared literal; derived roles flagged | seed drift |
| No raw colors | scan source for colour literals outside the token file | axis leakage |
| Light singleton | every glass part and paper shadow read one light; assert shadow side matches rim side | mixed light |
| Reduced motion | animations off: tilt/drift constant, paper steppers finish in zero frames | motion fallback broken |
| Layout | targets >= 44; no overflow at 200% text; goldens per part over backdrop matrix (lightest paper, darkest ink, busy art) at scale 1.0 and 2.0 | layout regression |
| Color-blind | state pairs differ >= 3:1 luminance plus a non-color cue | hue-only coding |

Run the first three on any world file:

```bash
python3 ~/.claude/skills/liquid-paper-glass/templates/check_world.py my-world.json
```

FAIL exits 1. WARN lists risks (label over accent hero, key line equals backdrop). APCA is warn-only (WCAG 3 candidate).

## Test tips (Flutter)

Widget tests default to the Ahem font; golden tests load real fonts and run on one platform. Make shadows opaque in goldens. Zero tolerance for hard-shadow paper; small tolerance for blur. A `BackdropFilter` exists by default; under high contrast there is none and the fill is flat. Use a fixed clock and in-memory DB for logic.

## Manual checks (cannot be automated)

Real gyro feel · blur frame time on an older phone · grain on OLED · 200% text · each OS accessibility toggle (Reduce Transparency, Increase Contrast, Reduce Motion) · VoiceOver/TalkBack order · sunlight legibility · iOS 26.1 Clear/Tinted setting.
