#!/usr/bin/env python3
"""Contrast gates for a liquid-paper-glass world file.

Usage: python3 check_world.py world.json [more.json ...]
Exit 1 if any FAIL. WARN never fails. WCAG 2.2 ratios, unrounded.
"""
import json
import sys


def parse(h):
    h = h.lstrip("#")
    if len(h) == 6:
        h += "FF"
    r, g, b, a = (int(h[i:i + 2], 16) for i in (0, 2, 4, 6))
    return (r, g, b, a / 255)


def over(fg, bg):
    """Composite fg (with alpha) over opaque bg."""
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)


def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check(path):
    w = json.load(open(path))
    p = {k: parse(v) for k, v in w["paper"].items()}
    g = {k: parse(v) for k, v in w["glass"].items()}
    fails, warns = [], []

    def need(label, fg, bg, minimum, bucket=fails):
        r = ratio(fg, bg)
        if r < minimum:
            bucket.append(f"{label}: {r:.2f} < {minimum}")

    # 1. Role contrast on paper.
    for fill in ("canvas", "surface", "raised"):
        for role in ("text", "strong", "muted"):
            need(f"{role} on {fill}", p[role], p[fill], 4.5)
    need("onAccent on accent", p["onAccent"], p["accent"], 4.5)
    need("onAccent on accentHi", p["onAccent"], p["accentHi"], 4.5)
    need("accent on surface", p["accent"], p["surface"], 3)
    need("signal on surface", p["signal"], p["surface"], 3)

    # 2. Glass worst case: label on glass fill over each paper backdrop.
    for back in ("canvas", "ground", "surface", "raised"):
        for state in ("fill", "fillHi"):
            shell = over(g[state], p[back])
            need(f"strong on glass.{state} over {back}", p["strong"], shell, 4.5)
            need(f"muted on glass.{state} over {back}", p["muted"], shell, 4.5,
                 warns)
    shell = over(g["fill"], p["accent"])
    need("strong on glass.fill over accent hero", p["strong"], shell, 4.5, warns)

    # 3. Edge: key line OR lit rim must separate glass from its surround 3:1.
    for back in ("canvas", "surface"):
        shell = over(g["fill"], p[back])
        key = ratio(g["key"], p[back])
        rim = ratio(over(g["light"], shell), p[back])
        if max(key, rim) < 3:
            fails.append(f"glass edge over {back}: key {key:.2f}, rim {rim:.2f} < 3")
        elif key < 3:
            warns.append(f"key line over {back} is {key:.2f}; edge relies on rim")

    # 4. Key line should equal ink unless declared otherwise.
    if w["glass"]["key"].upper() != w["paper"]["ink"].upper():
        warns.append("glass.key differs from paper.ink; intended?")

    print(f"== {w['id']} ({w['brightness']})")
    for m in fails:
        print("FAIL", m)
    for m in warns:
        print("WARN", m)
    if not fails:
        print("PASS" + (" (with warnings)" if warns else ""))
    return not fails


if __name__ == "__main__":
    ok = all([check(f) for f in sys.argv[1:]])
    sys.exit(0 if ok else 1)
