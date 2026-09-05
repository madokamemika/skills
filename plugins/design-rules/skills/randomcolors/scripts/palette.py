#!/usr/bin/env python3
"""Turn a seed palette into a UI colour system whose every rendered pair
passes WCAG, and emit it as CSS custom properties.

The seed supplies hues; this script rebuilds lightness and chroma. That
split is the whole idea: hue relationships are what a human chose and what
is worth keeping, while the lightness ladder is what makes an interface
readable and is almost never right in an aesthetic four-swatch palette.

The trap it exists to avoid: OKLCH lightness is not luminance. Yellow at
L=0.75 and blue at L=0.75 differ by more than 2:1 in WCAG contrast against
white, so a palette built by assigning lightnesses fails on some hues and
not others. Every foreground here is solved against its actual background
by binary search, then verified.

No dependencies. Python 3.8+.
"""

import argparse, colorsys, json, math, random, sys, urllib.request

# ---------------------------------------------------------------- colour math

def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def linear_to_srgb(c):
    v = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return max(0.0, min(1.0, v)) * 255.0

def rgb_to_oklab(r, g, b):
    lr, lg, lb = srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b)
    l = 0.4122214708 * lr + 0.5363325363 * lg + 0.0514459929 * lb
    m = 0.2119034982 * lr + 0.6806995451 * lg + 0.1073969566 * lb
    s = 0.0883024619 * lr + 0.2817188376 * lg + 0.6299787005 * lb
    l_, m_, s_ = l ** (1 / 3) if l > 0 else 0, m ** (1 / 3) if m > 0 else 0, s ** (1 / 3) if s > 0 else 0
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)

def oklab_to_linear(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)

def rgb_to_oklch(r, g, b):
    L, a, bb = rgb_to_oklab(r, g, b)
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360

def in_gamut(L, C, H, eps=1e-4):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    return all(-eps <= v <= 1 + eps for v in oklab_to_linear(L, a, b))

def oklch_to_rgb(L, C, H):
    """Reduce chroma until the colour fits sRGB, then convert. Clipping RGB
    instead would shift the hue, which is what makes naive OKLCH pickers
    produce colours that do not match the number you asked for."""
    if not in_gamut(L, C, H):
        lo, hi = 0.0, C
        for _ in range(40):
            mid = (lo + hi) / 2
            if in_gamut(L, mid, H):
                lo = mid
            else:
                hi = mid
        C = lo
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    # Rounded to 8-bit here, not later. Contrast has to be measured on the
    # values that actually ship: solving on floats and emitting hex costs up
    # to 0.03 of a ratio, which is invisible until a pair solved to exactly
    # 4.50 reaches the browser at 4.47 and an audit fails a page that the
    # generator called clean.
    rgb = tuple(float(round(linear_to_srgb(v))) for v in oklab_to_linear(L, a, b))
    return rgb, C

def to_hex(rgb):
    return '#%02x%02x%02x' % tuple(int(round(max(0, min(255, v)))) for v in rgb)

def from_hex(h):
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def luminance(rgb):
    r, g, b = (srgb_to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(rgb1, rgb2):
    a, b = sorted((luminance(rgb1), luminance(rgb2)), reverse=True)
    return (a + 0.05) / (b + 0.05)

# ------------------------------------------------------------------- solving

def solve_lightness(H, C, backgrounds, target, direction):
    """Smallest departure from the background that still reaches `target`
    against every background given. Overshooting is a real cost: muted text
    that lands at 9:1 is not muted any more, it is just text."""
    def ok(L):
        rgb, _ = oklch_to_rgb(L, C, H)
        return all(contrast(rgb, bg) >= target for bg in backgrounds)

    lo, hi = (0.0, 1.0) if direction == 'down' else (1.0, 0.0)
    if not ok(lo):
        return None                      # unreachable even at the extreme
    for _ in range(60):
        mid = (lo + hi) / 2
        if ok(mid):
            lo = mid
        else:
            hi = mid
    return lo

def build_role(name, H, C, backgrounds, target, direction, notes):
    L = solve_lightness(H, C, backgrounds, target, direction)
    if L is None:
        # Hue cannot reach the target at this chroma; drop chroma and retry.
        for c in (C * 0.6, C * 0.3, 0.0):
            L = solve_lightness(H, c, backgrounds, target, direction)
            if L is not None:
                notes.append(f"{name}: chroma reduced to {c:.3f} to reach {target}:1")
                C = c
                break
    if L is None:
        raise SystemExit(f"cannot reach {target}:1 for {name} at hue {H:.0f}")
    rgb, C_used = oklch_to_rgb(L, C, H)
    if C_used < C - 1e-3:
        notes.append(f"{name}: chroma clipped to sRGB gamut ({C:.3f} -> {C_used:.3f})")
    return {'name': name, 'rgb': rgb, 'hex': to_hex(rgb),
            'oklch': (round(L, 4), round(C_used, 4), round(H, 1))}

# ------------------------------------------------------------------- seeding

def seed_from_colormind(model='ui', locked=None, timeout=20):
    payload = {'model': model}
    if locked:
        inp = [list(from_hex(h)) for h in locked] + ['N'] * (5 - len(locked))
        payload['input'] = inp[:5]
    # Without an explicit User-Agent the endpoint answers 403: urllib's default
    # identifies itself as a script and is refused.
    req = urllib.request.Request(
        'http://colormind.io/api/', data=json.dumps(payload).encode(),
        headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return [to_hex(c) for c in json.loads(r.read())['result']]

def seed_random(rng):
    """Local fallback. Rolls a hue geometry rather than emitting remembered
    hex codes, which is the entire point: a recalled palette is the average
    of every palette seen, and the average is what looks generic."""
    base = rng.uniform(0, 360)
    geometry = rng.choice(['analogous', 'complement', 'split', 'triad'])
    offsets = {'analogous': [0, 24, -24, 48], 'complement': [0, 180, 20, 200],
               'split': [0, 150, 210, 30], 'triad': [0, 120, 240, 60]}[geometry]
    out = []
    for off in offsets:
        H = (base + off) % 360
        L = rng.uniform(0.45, 0.75)
        C = rng.uniform(0.08, 0.18)
        rgb, _ = oklch_to_rgb(L, C, H)
        out.append(to_hex(rgb))
    return out, geometry

# ------------------------------------------------------------- the system

# Every entry: (role, target ratio against the backgrounds named, why).
# A ratio of None means the pair carries no WCAG requirement.
def build_system(seed_hexes, dark=False, notes=None):
    notes = notes if notes is not None else []
    parsed = [rgb_to_oklch(*from_hex(h)) for h in seed_hexes]
    by_chroma = sorted(range(len(parsed)), key=lambda i: parsed[i][1], reverse=True)

    accent_H = parsed[by_chroma[0]][2]
    accent_C = max(0.10, min(0.20, parsed[by_chroma[0]][1]))
    neutral_H = parsed[by_chroma[-1]][2] if len(parsed) > 1 else accent_H
    extra_H = [parsed[i][2] for i in by_chroma[1:4]]

    # Surfaces first: everything else is solved against them.
    if dark:
        bg_L, surf_L, sunk_L = 0.17, 0.21, 0.13
    else:
        bg_L, surf_L, sunk_L = 0.985, 1.0, 0.955
    nC = 0.012                      # neutrals carry a trace of the seed hue,
                                    # which is what stops them reading as grey
    surfaces = {}
    for nm, L in (('bg', bg_L), ('surface', surf_L), ('surface-sunken', sunk_L)):
        rgb, c = oklch_to_rgb(L, nC, neutral_H)
        surfaces[nm] = {'name': nm, 'rgb': rgb, 'hex': to_hex(rgb),
                        'oklch': (round(L, 4), round(c, 4), round(neutral_H, 1))}

    bgs = [surfaces['bg']['rgb'], surfaces['surface']['rgb'],
           surfaces['surface-sunken']['rgb']]
    d = 'up' if dark else 'down'
    roles = dict(surfaces)

    roles['text'] = build_role('text', neutral_H, nC * 2, bgs, 7.0, d, notes)
    roles['text-muted'] = build_role('text-muted', neutral_H, nC * 2, bgs, 4.5, d, notes)
    roles['border'] = build_role('border', neutral_H, nC, [surfaces['bg']['rgb']], 1.5, d, notes)
    roles['border-strong'] = build_role('border-strong', neutral_H, nC, bgs, 3.0, d, notes)
    roles['accent'] = build_role('accent', accent_H, accent_C, bgs, 3.0, d, notes)

    # on-accent is text ON the accent fill, so the accent is its background.
    a_rgb = roles['accent']['rgb']
    white, black = (255, 255, 255), (0, 0, 0)
    if contrast(white, a_rgb) >= 4.5:
        on = build_role('on-accent', accent_H, 0.02, [a_rgb], 4.5, 'up', notes)
    else:
        on = build_role('on-accent', accent_H, 0.02, [a_rgb], 4.5, 'down', notes)
    roles['on-accent'] = on

    # Hover and active move the fill AWAY from whatever sits on it. Stepping
    # by a fixed delta in a fixed direction is the obvious approach and it is
    # wrong half the time: when on-accent is dark text, darkening the fill on
    # hover walks the pair straight through 4.5:1. Direction comes from the
    # foreground, and the step shrinks if it would cost the 3:1 against the page.
    aL = roles['accent']['oklch'][0]
    away = 1 if on['oklch'][0] < aL else -1        # dark text -> lighten, light -> darken
    for nm, step in (('accent-hover', 0.05), ('accent-active', 0.10)):
        L = max(0.03, min(0.99, aL + away * step))
        while step > 0.005:
            rgb, c = oklch_to_rgb(L, accent_C, accent_H)
            if (contrast(rgb, on['rgb']) >= 4.5
                    and contrast(rgb, surfaces['bg']['rgb']) >= 3.0):
                break
            step *= 0.75
            L = max(0.03, min(0.99, aL + away * step))
        rgb, c = oklch_to_rgb(L, accent_C, accent_H)
        if contrast(rgb, on['rgb']) < 4.5:
            notes.append(f"{nm}: hue cannot hold 4.5:1 under its label; "
                         f"flattened to the resting accent")
            L = aL
            rgb, c = oklch_to_rgb(L, accent_C, accent_H)
        roles[nm] = {'name': nm, 'rgb': rgb, 'hex': to_hex(rgb),
                     'oklch': (round(L, 4), round(c, 4), round(accent_H, 1))}

    # Tinted chip background, plus text solved to sit on it.
    subtle_L = 0.26 if dark else 0.94
    rgb, c = oklch_to_rgb(subtle_L, accent_C * 0.35, accent_H)
    roles['accent-subtle'] = {'name': 'accent-subtle', 'rgb': rgb, 'hex': to_hex(rgb),
                              'oklch': (round(subtle_L, 4), round(c, 4), round(accent_H, 1))}
    roles['on-accent-subtle'] = build_role('on-accent-subtle', accent_H, accent_C * 0.8,
                                           [rgb], 4.5, d, notes)
    roles['focus'] = build_role('focus', accent_H, accent_C, bgs, 3.0, d, notes)

    for nm, H in (('success', 148.0), ('warning', 75.0), ('danger', 27.0)):
        roles[nm] = build_role(nm, H, 0.15, bgs, 3.0, d, notes)
        s_rgb = roles[nm]['rgb']
        up = contrast(white, s_rgb) >= contrast(black, s_rgb)
        roles['on-' + nm] = build_role('on-' + nm, H, 0.02, [s_rgb], 4.5,
                                       'up' if up else 'down', notes)
        roles[nm + '-text'] = build_role(nm + '-text', H, 0.12, bgs, 4.5, d, notes)

    for i, H in enumerate(extra_H, start=2):
        roles[f'accent-{i}'] = build_role(f'accent-{i}', H, accent_C, bgs, 3.0, d, notes)

    return roles, {'accent_hue': round(accent_H, 1), 'neutral_hue': round(neutral_H, 1),
                   'extra_hues': [round(h, 1) for h in extra_H]}

# ------------------------------------------------------------------ checking

PAIRS = [
    ('text', 'bg', 7.0), ('text', 'surface', 7.0), ('text', 'surface-sunken', 7.0),
    ('text-muted', 'bg', 4.5), ('text-muted', 'surface', 4.5),
    ('text-muted', 'surface-sunken', 4.5),
    ('border-strong', 'bg', 3.0), ('accent', 'bg', 3.0), ('accent', 'surface', 3.0),
    ('on-accent', 'accent', 4.5), ('on-accent', 'accent-hover', 4.5),
    ('on-accent', 'accent-active', 4.5),
    ('on-accent-subtle', 'accent-subtle', 4.5),
    ('focus', 'bg', 3.0), ('focus', 'surface', 3.0),
    ('success', 'bg', 3.0), ('warning', 'bg', 3.0), ('danger', 'bg', 3.0),
    ('on-success', 'success', 4.5), ('on-warning', 'warning', 4.5),
    ('on-danger', 'danger', 4.5),
    ('success-text', 'bg', 4.5), ('warning-text', 'bg', 4.5), ('danger-text', 'bg', 4.5),
]

def check(roles):
    rows = []
    for fg, bg, need in PAIRS:
        if fg not in roles or bg not in roles:
            continue
        r = contrast(roles[fg]['rgb'], roles[bg]['rgb'])
        rows.append((fg, bg, round(r, 2), need, r >= need - 0.005))
    for k in list(roles):
        if k.startswith('accent-') and k[7:].isdigit():
            r = contrast(roles[k]['rgb'], roles['bg']['rgb'])
            rows.append((k, 'bg', round(r, 2), 3.0, r >= 2.995))
    return rows

# -------------------------------------------------------------------- output

def css(light, dark):
    def block(roles, indent='  '):
        return '\n'.join(f"{indent}--color-{k}: {v['hex']};"
                         for k, v in sorted(roles.items()))
    return (":root {\n" + block(light) + "\n}\n\n"
            ":root:not([data-theme=\"light\"]) {\n"
            "  @media (prefers-color-scheme: dark) {\n" + block(dark, '    ') +
            "\n  }\n}\n\n"
            ":root[data-theme=\"dark\"] {\n" + block(dark) + "\n}\n")

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group()
    src.add_argument('--seed', help='comma-separated hex colours to take hues from')
    src.add_argument('--colormind', nargs='?', const='ui', metavar='MODEL',
                     help='fetch a seed from colormind.io (ui, default, fauvism, '
                          'akira_film, contempt_1963, game_of_thrones)')
    src.add_argument('--random', action='store_true',
                     help='roll a hue geometry locally, no network')
    p.add_argument('--lock', help='hex colours to keep when using --colormind')
    p.add_argument('--rng-seed', type=int, help='make --random reproducible')
    p.add_argument('--format', choices=['css', 'json', 'report', 'all'], default='all')
    args = p.parse_args()

    rng = random.Random(args.rng_seed)
    origin, geometry = '', None
    if args.seed:
        seed = [h.strip() for h in args.seed.split(',') if h.strip()]
        origin = 'given'
    elif args.colormind:
        locked = [h.strip() for h in args.lock.split(',')] if args.lock else None
        try:
            seed = seed_from_colormind(args.colormind, locked)
            origin = f'colormind:{args.colormind}'
        except Exception as e:
            print(f"colormind unreachable ({e}); rolling locally instead", file=sys.stderr)
            seed, geometry = seed_random(rng)
            origin = 'random'
    else:
        seed, geometry = seed_random(rng)
        origin = 'random'

    notes = []
    light, meta = build_system(seed, dark=False, notes=notes)
    darkr, _ = build_system(seed, dark=True, notes=notes)
    rows_l, rows_d = check(light), check(darkr)
    failed = [r for r in rows_l + rows_d if not r[4]]

    if args.format in ('report', 'all'):
        print(f"seed ({origin}{', ' + geometry if geometry else ''}): {', '.join(seed)}")
        print(f"accent hue {meta['accent_hue']}  neutral hue {meta['neutral_hue']}"
              f"  extra {meta['extra_hues']}\n")
        for label, rows in (('light', rows_l), ('dark', rows_d)):
            print(f"--- {label}")
            for fg, bg, r, need, ok in rows:
                print(f"  {'ok  ' if ok else 'FAIL'} {fg:>18} on {bg:<16} "
                      f"{r:>6.2f}:1  (needs {need})")
        for n in dict.fromkeys(notes):
            print(f"  note: {n}")
        print()
    if args.format in ('css', 'all'):
        print(css(light, darkr))
    if args.format == 'json':
        print(json.dumps({'seed': seed, 'origin': origin, 'meta': meta,
                          'light': {k: v['hex'] for k, v in light.items()},
                          'dark': {k: v['hex'] for k, v in darkr.items()},
                          'checks': {'light': rows_l, 'dark': rows_d}}, indent=2))
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())
