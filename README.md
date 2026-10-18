# liquid-paper-glass

An agent skill for building **Liquid Paper Glass** UIs: Apple iOS 26 Liquid Glass chrome floating over an opaque, themed paper/ink content layer. Theme it on any game, film or world, and mix palette, glass variant, paper cut, type, motion and light independently.

## Install

```bash
git clone https://github.com/AiverReaver/liquid-paper-glass.git
cp -R liquid-paper-glass ~/.claude/skills/liquid-paper-glass
```

Then ask your agent to build or theme a UI (for example "Hades-themed liquid glass habit app"). The skill triggers on its own.

## What is inside

- `SKILL.md`: the layer contract, six axes, hard rules and workflow.
- `references/`: world-to-theme method, glass material, paper layer, platform recipes (SwiftUI, Flutter, web, Compose, React Native), gates and tests, a worked example.
- `templates/world.example.json`: the world file to copy.
- `templates/check_world.py`: contrast gates for a world file (`python3 templates/check_world.py my-world.json`).

## Notes

- Apple publishes almost no Liquid Glass numbers. Values are labeled sourced, inferred or tune-by-eye.
- Themes use palette and mood only. Do not ship a game's art, logos, sprites or fonts.
- Not legal advice.

MIT licensed.
