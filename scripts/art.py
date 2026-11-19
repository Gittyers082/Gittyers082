"""Static art for the profile README. Run once (and again after editing profile.config.json):

    python scripts/art.py            # everything except the ASCII gallery
    python scripts/gallery.py        # the dense ASCII gallery (needs rsvg-convert + Pillow)

Writes assets/<name>-light.svg and assets/<name>-dark.svg.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.svgkit import (MONO_ADV, MONO_STACK, PALETTES, THEMES, config, doc, dots, frames_css, panel,
                        text, text_width, write)

W = 830

# El, seen from behind (same paths as the portfolio's AuraFarmer)
ROCK = "M24 336 L46 284 L34 260 L74 228 L112 214 L150 208 L204 210 L236 200 L272 222 L304 246 L296 286 L322 314 L330 336 Z"
ROCK_SHADE = "M236 200 L272 222 L304 246 L296 286 L322 314 L330 336 L252 336 L264 300 L242 262 Z"
BODY = "M128 142 C120 190 122 230 132 252 L208 252 C218 230 220 190 212 142 Z"
LEGS = "M140 246 L138 310 L164 310 L166 246 Z M176 246 L178 310 L204 310 L202 246 Z"
BOOTS = "M126 306 H166 V320 H122 Z M176 306 H214 V320 H180 Z"
HAIR = "M92 150 C78 108 84 66 110 44 L104 14 L126 34 L134 0 L150 30 L170 6 L172 38 L196 22 L188 58 C204 84 206 122 188 150 Z"
CAPE_A = "M132 140 C122 180 120 222 124 262 C150 272 172 252 198 258 C224 264 248 236 274 232 C290 229 302 214 314 204 C288 196 264 188 242 172 C228 162 216 150 208 140 Z"
CAPE_B = "M132 140 C120 176 116 214 118 250 C146 256 166 236 194 238 C222 240 246 210 272 204 C290 200 304 182 318 170 C292 168 266 166 244 158 C228 152 216 146 208 140 Z"


def el_on_rock(c: dict, uid: str) -> str:
    return (
        f'<path d="{ROCK}" fill="{c["rock"]}" stroke="{c["ink"]}" stroke-width="5" stroke-linejoin="round"/>'
        f'<path d="{ROCK_SHADE}" fill="url(#{uid}ink)" opacity="0.5"/>'
        '<g transform="translate(0 -110)">'
        f'<path d="{BODY}" fill="{c["ink"]}"/><path d="{LEGS}" fill="{c["ink"]}"/><path d="{BOOTS}" fill="{c["ink"]}"/>'
        f'<path d="{CAPE_A}" fill="{c["accent"]}" stroke="{c["ink"]}" stroke-width="4.5" stroke-linejoin="round">'
        f'<animate attributeName="d" dur="2.6s" repeatCount="indefinite" values="{CAPE_A};{CAPE_B};{CAPE_A}"/></path>'
        f'<g transform="translate(92 58) scale(0.55)"><path d="{HAIR}" fill="{c["ink"]}"/></g>'
        f'<path d="M130 142 C150 134 190 134 210 142" fill="none" stroke="{c["ink"]}" stroke-width="7" stroke-linecap="round"/>'
        "</g>"
    )


# ---------------------------------------------------------------- banner

def banner(theme: str, cfg: dict) -> str:
    c = PALETTES[theme]
    first, _, last = cfg["name"].upper().rpartition(" D. ")
    line1, line2 = (first, "D. " + last) if first else (cfg["name"].upper(), "")
    body = (
        f"<defs>{dots('bd', c['accent'], 9, 1.5, 0.35)}{dots('bink', c['ink'])}</defs>"
        f'<rect x="1.5" y="1.5" width="827" height="297" fill="{c["card"]}" stroke="{c["ink"]}" stroke-width="3"/>'
        '<rect x="1.5" y="1.5" width="827" height="297" fill="url(#bd)"/>'
        f'<polygon points="560,3 640,3 470,297 390,297" fill="{c["accent"]}"/>'
        f'<polygon points="655,3 672,3 502,297 485,297" fill="{c["ink"]}"/>'
        + text(cfg["episode"], 40, 64, 15, c["muted"], wght=700, ls=2.5)
        + text(line1, 38, 150, 92, c["ink"], wght=700, wdth=70)
        + text(line2, 38, 232, 92, c["ink"], wght=700, wdth=70)
    )
    tag_w = text_width(cfg["tagline"], 14, 700, 100, 1) + 24
    body += f'<rect x="40" y="252" width="{tag_w:.0f}" height="28" fill="{c["ink"]}"/>' + text(cfg["tagline"], 52, 271, 14, c["card"], ls=1)
    body += f'<g transform="translate(585 50) scale(0.735)">{el_on_rock(c, "b")}</g>'
    # the comment that pops in from nowhere
    body += (
        '<g class="pop">'
        f'<rect x="420" y="40" width="168" height="46" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="2.5"/>'
        + text("@visitor", 430, 57, 10.5, c["accent"], wght=700)
        + text("yes El, we see the fit (¬_¬)", 430, 76, 12, c["ink"], wght=600)
        + "</g>"
    )
    css = (
        ".pop{opacity:0;transform-origin:504px 63px;animation:pop 6s infinite}"
        "@keyframes pop{0%,20%{opacity:0;transform:scale(.6) rotate(-4deg)}27%{opacity:1;transform:scale(1.06) rotate(1deg)}"
        "31%,85%{opacity:1;transform:scale(1) rotate(0)}92%,100%{opacity:0;transform:scale(.9)}}"
    )
    return doc(W, 300, body, f"{cfg['name']}: {cfg['tagline'].lower()} El, seen from behind, stands on a rock with his cape in the wind.", css)


# ---------------------------------------------------------------- typing line

def typing(theme: str, cfg: dict) -> str:
    c = PALETTES[theme]
    size, char_ms, hold_ms, gap_ms = 20, 70, 1800, 350
    cw = size * MONO_ADV
    phrases = ["> " + p for p in cfg["typing"]]
    longest = max(len(p) for p in phrases)
    x0 = (W - (longest + 1) * cw) / 2
    spans = []  # (start_ms, end_ms) per phrase: type, hold, delete
    t = 0
    for p in phrases:
        n = len(p) - 2
        dur = n * char_ms + hold_ms + n * (char_ms // 2) + gap_ms
        spans.append((t, t + dur))
        t += dur
    total = t
    body, css = "", f".caret{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}"
    for i, (p, (s, e)) in enumerate(zip(phrases, spans)):
        n = len(p) - 2

        def pct(ms):
            return f"{ms / total * 100:.3f}%"

        def at(ms, chars):
            return f"{pct(ms)}{{transform:translateX({chars * cw:.1f}px)}}"

        kf = [at(0, 2)]
        if s > 0:
            kf.append(at(s - 1, 2))
        kf += [at(s + j * char_ms, 2 + j) for j in range(n + 1)]
        hold_end = s + n * char_ms + hold_ms
        kf += [at(hold_end + j * (char_ms // 2), 2 + n - j) for j in range(n + 1)]
        kf.append(f"100%{{transform:translateX({2 * cw:.1f}px)}}")
        dur = f"{total / 1000:.2f}s"
        css += f".m{i}{{animation:w{i} {dur} steps(1,end) infinite}}@keyframes w{i}{{{''.join(kf)}}}"
        # only the phrase on screen shows its cursor
        vis = f"0%{{opacity:{1 if s == 0 else 0}}}{pct(s)}{{opacity:1}}{pct(e)}{{opacity:0}}100%{{opacity:0}}"
        css += f".v{i}{{animation:v{i} {dur} steps(1,end) infinite}}@keyframes v{i}{{{vis}}}"
        # the clip rect sits just left of the text; sliding it right reveals the phrase
        body += (
            f'<clipPath id="cp{i}"><rect class="m{i}" x="{x0 - 1200:.1f}" y="4" width="1200" height="34"/></clipPath>'
            f'<g clip-path="url(#cp{i})">' + text(p, x0, 28, size, c["accent"], mono=True, bold=True) + "</g>"
            f'<g class="v{i}"><g class="m{i}"><rect class="caret" x="{x0:.1f}" y="10" width="{cw * 0.9:.1f}" height="22" fill="{c["accent"]}"/></g></g>'
        )
    css += f"@media (prefers-reduced-motion:reduce){{.m0{{transform:translateX({len(phrases[0]) * cw:.1f}px)}}.v0{{opacity:1}}}}"
    return doc(W, 40, body, "Typing: " + "; ".join(cfg["typing"]), css)


# ---------------------------------------------------------------- about tiles

def about(theme: str, cfg: dict) -> str:
    c = PALETTES[theme]
    cols, tile_h, gap = 3, 92, 3
    x0, y0, w = 0, 0, W - 12
    tw = (w - 6 - gap * (cols - 1)) / cols
    rows = (len(cfg["about"]) + cols - 1) // cols
    h = 6 + rows * tile_h + (rows - 1) * gap
    body = f"<defs>{dots('ad', c['ink'])}</defs>"
    body += f'<rect x="12" y="12" width="{w}" height="{h}" fill="url(#ad)"/>'
    body += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{c["ink"]}"/>'
    for i, a in enumerate(cfg["about"]):
        r, col = divmod(i, cols)
        x = x0 + 3 + col * (tw + gap)
        y = y0 + 3 + r * (tile_h + gap)
        hi = a.get("highlight")
        bg, fg, tag = (c["ink"], c["card"], c["on_ink_accent"]) if hi else (c["card"], c["ink"], c["accent"])
        body += f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="{tile_h}" fill="{bg}"/>'
        body += text("// " + a["key"], x + 18, y + 26, 11.5, tag, mono=True, bold=True)
        body += text(a["value"], x + 18, y + 56, 27, fg, wght=700, wdth=70)
        body += text(a["note"], x + 18, y + 77, 11.5, fg, wght=400, extra=' opacity="0.8"')
    label = "About El: " + "; ".join(f"{a['key'].replace('_', ' ')}: {a['value']}, {a['note']}" for a in cfg["about"])
    return doc(W, h + 12, body, label)


# ---------------------------------------------------------------- the commit joke

def commit(theme: str, cfg: dict) -> str:
    c = PALETTES[theme]
    cw = (W - 16 - 12) / 2
    body = (
        f'<g transform="rotate(-1.2 {cw/2+6} 60)">'
        f'<rect x="6" y="14" width="{cw}" height="78" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="3"/>'
        + text("$", 26, 46, 15, c["accent"], mono=True, bold=True)
        + text('git commit -m "fix stuff"', 26 + 15 * MONO_ADV * 2, 46, 15, c["ink"], mono=True, bold=True)
        + text("1 file changed · it works, don't touch it", 26, 72, 14, c["muted"], wght=400)
        + "</g>"
        f'<g transform="rotate(1 {cw*1.5+22} 60)">'
        f'<rect x="{cw+22}" y="14" width="{cw}" height="78" fill="{c["ink"]}" stroke="{c["ink"]}" stroke-width="3"/>'
        + text("Just kidding. These days it's:", cw + 42, 44, 14, c["card"], wght=700)
        + text("$", cw + 42, 70, 11, c["on_ink_accent"], mono=True, bold=True)
        + text('git commit -m "feat(profile): match the portfolio"', cw + 42 + 11 * MONO_ADV * 2, 70, 11, c["card"], mono=True, bold=True)
        + "</g>"
    )
    return doc(W, 108, body, 'git commit -m "fix stuff". Just kidding. These days it\'s: git commit -m "feat(profile): match the portfolio"')


# ---------------------------------------------------------------- dodge.exe

def dodge(theme: str, cfg: dict) -> str:
    c = PALETTES[theme]
    cols, ground, rx, size, lh = 84, 5, 8, 15, 18.5
    cw = size * MONO_ADV
    labels = ["ERR", "404", "NaN", "null", "TODO", "}"]
    spacing, period = 23, 92            # obstacles 23 cols apart; the loop is 92 frames
    frames = []
    for t in range(period):
        grid = [[" "] * cols for _ in range(6)]
        hot = [[False] * cols for _ in range(6)]
        for x in range(cols):
            grid[ground][x] = "." if (x + t) % 9 == 0 else "_"
        obs = []
        for i in range(4):
            x = cols - ((t + i * spacing) % period)
            lab = labels[(i + (t + i * spacing) // period) % len(labels)]
            obs.append(x)
            for j, ch in enumerate(lab):
                if 0 <= x + j < cols:
                    grid[ground - 1][x + j] = ch
                    hot[ground - 1][x + j] = True
        near = any(rx - 2 <= x <= rx + 4 for x in obs)
        lift = 2 if near else 0
        legs = "/ \\" if near else ("/ >" if t % 2 else "< \\")
        for r, s in enumerate([" o ", "/|\\", legs]):
            y = ground - 3 + r - lift
            for j, ch in enumerate(s):
                if ch != " " and y >= 0:
                    grid[y][rx + j] = ch
        frames.append((grid, hot))
    fx, fy = 28, 58
    body = panel(c, 0, 0, W - 14, 186, "dodge.exe", "> survive the bugs", uid="dg")
    from html import escape
    for i, (grid, hot) in enumerate(frames):
        rows = []
        for y in range(6):
            spans, cur, h0 = [], "", None
            for x in range(cols):
                h = hot[y][x]
                if h0 is None or h == h0:
                    cur += grid[y][x]
                else:
                    spans.append((cur, h0)); cur = grid[y][x]
                h0 = h
            spans.append((cur, h0))
            inner = "".join(f'<tspan class="h">{escape(s)}</tspan>' if hh else escape(s) for s, hh in spans)
            rows.append(f'<text x="{fx}" y="{fy + y * lh:.1f}">{inner}</text>')
        body += f'<g class="f f{i}">{"".join(rows)}</g>'
    css = (
        f"text{{font-family:{MONO_STACK};font-size:{size}px;white-space:pre;fill:{c['ink']}}}"
        f".h{{fill:{c['accent']};font-weight:700}}" + frames_css(len(frames), 0.11)
    )
    return doc(W, 200, body, "dodge.exe: a tiny ASCII runner hops over ERR, 404, NaN and TODO", css, mono=True)


# ---------------------------------------------------------------- section headings and footer

HEADINGS = {"stats": "STATS", "building": "CURRENTLY BUILDING", "stack": "STACK", "gallery": "THE GALLERY"}


def heading(theme: str, title: str) -> str:
    c = PALETTES[theme]
    body = (f'<polygon points="8,6 22,6 16,38 2,38" fill="{c["accent"]}"/>'
            + text(title, 34, 35, 34, c["ink"], wght=700, wdth=70))
    return doc(W, 44, body, title)


def footer(theme: str, cfg: dict) -> str:
    c = PALETTES[theme]
    body = (f'<rect width="{W}" height="36" fill="{c["ink"]}"/>'
            + text("main · 0 errors · EOF", 14, 23, 12, c["card"], mono=True)
            + text("Thanks for scrolling. The full story is on the portfolio.", W - 14, 23, 12, c["card"], mono=True, anchor="end"))
    return doc(W, 36, body, "End of file. Thanks for scrolling. The full story is on the portfolio.")


BUILDERS = {"banner": banner, "typing": typing, "about": about, "commit": commit, "dodge": dodge, "footer": footer}
for _key, _title in HEADINGS.items():
    BUILDERS[f"h-{_key}"] = (lambda t: (lambda theme, cfg: heading(theme, t)))(_title)

if __name__ == "__main__":
    cfg = config()
    only = sys.argv[1:] or list(BUILDERS)
    for name in only:
        for theme in THEMES:
            p = write(name, theme, BUILDERS[name](theme, cfg))
            print(f"{p.relative_to(p.parents[1])}  {p.stat().st_size // 1024} KB")
