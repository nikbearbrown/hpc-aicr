"""scenes.py — Optimizing GPU Usage on Explorer (lecture). The show-tell iso_kit is pasted below verbatim (Gate A copies
only this file), then the pacing/midpoint-guard helpers, the film's cast, its measured word times (_ASR, injected
by assemble_scenes.py from _qc/asr.json) and its scenes."""
"""
iso_kit.py — the show-tell drawing kit. PASTE this block at the top of a reel's scenes.py;
do not import it (Gate A copies only scenes.py into its sandbox).

Drawn isometric objects in the Claude palette: cardboard boxes (closed, open, taped), dark
MCP blocks with ports, flat skill pages, server stacks with lights, checks, a cursor, pills,
and a WRITING KIT (quill, inkwell, paper, scribble lines, branching outline + the write_lines /
grow_tree animations that make the quill write). A PERSON IS NEVER AN ICON: `professor_bear(ratio, …)`
places a random Professor Bear portrait of the right aspect ratio (PROFESSOR BEAR LAW).
Pacing helpers read the reel's beat_sheet.json so scenes wait for their spoken phrase.

Every rule in ../SKILL.md "DRAWING LAWS" is already obeyed by these primitives; keep it that
way when you add one (label beside, never inside; terracotta never under text; dim greys
with gaps for chart blocks; type floor 32).
"""
from manim import *
import numpy as np
import json as _json, os as _os

# ═════════════════════════════ ISO KIT (show-tell) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"          # kraft cardboard: top, left face, right face (deep enough for Gate V contrast)
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"     # inside walls + floor
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"        # MCP / server blocks
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"         # skill pages
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"                # chart segments, dim to ghost
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=36, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


class Iso:
    """Isometric projection: x runs right-up, y runs left-up, z runs up. (ox, oy) is where (0,0,0) lands."""
    def __init__(self, ox=0.0, oy=0.0, s=1.0):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return np.array([self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s + z * self.s, 0.0])

    def v(self, dx, dy, dz=0.0):
        return self.p(dx, dy, dz) - self.p(0, 0, 0)

    def quad(self, pts, fill, stroke=INK, sw=4):
        return Polygon(*[self.p(*q) for q in pts], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)

    def box(self, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, sw=4):
        """Closed box: the two front faces (x = x0 and y = y0) plus the top."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, sw=sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, sw=sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, sw=sw))

    def open_box(self, x0, y0, z0, w, d, h):
        """(back, front): floor + inner back walls, then the front walls. Put contents between them."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        back = VGroup(
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], BOX_FLOOR),
            self.quad([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], BOX_IN1),
            self.quad([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], BOX_IN2))
        front = VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], BOX_L),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], BOX_R))
        back.set_z_index(0); front.set_z_index(2)
        return back, front

    def tape(self, x0, y0, z1, w, d, drop=0.35, t=0.22):
        """Terracotta tape across the top (along x) and down the left front face."""
        ym = y0 + d / 2
        return VGroup(
            self.quad([(x0, ym - t, z1), (x0 + w, ym - t, z1), (x0 + w, ym + t, z1), (x0, ym + t, z1)], TERRA, sw=0),
            self.quad([(x0, ym - t, z1), (x0, ym + t, z1), (x0, ym + t, z1 - drop), (x0, ym - t, z1 - drop)], TERRA, sw=0))

    def mcp(self, x0, y0, z0, w=1.3, d=1.3, h=0.7):
        """Dark MCP block with two light ports on its right front face."""
        body = self.box(x0, y0, z0, w, d, h, DARK_TOP, DARK_L, DARK_R)
        ports = VGroup(*[self.box(x0 + w * f, y0 - 0.18, z0 + h * 0.3, w * 0.16, 0.18, h * 0.3, GHOST, BOX_IN1, BOX_IN2, sw=1)
                         for f in (0.22, 0.58)])
        return VGroup(body, ports)

    def page(self, x0, y0, z0, w=1.1, d=1.4):
        """A skill page lying flat: white slab, three ghost text lines, one terracotta dot."""
        slab = self.box(x0, y0, z0, w, d, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
        zt = z0 + 0.06
        lines = VGroup(*[Line(self.p(x0 + 0.2, y0 + d * f, zt), self.p(x0 + w - 0.2, y0 + d * f, zt), color=GHOST, stroke_width=4)
                         for f in (0.3, 0.5, 0.7)])
        dot = Dot(self.p(x0 + 0.2, y0 + d * 0.86, zt), radius=0.06, color=TERRA)
        return VGroup(slab, lines, dot)

    def server(self, x0, y0, z0, w=1.4, d=1.4, slab=0.42, n=3):
        """A stack of dark server slabs; returns (stack, lights) — lights start ghost, turn terracotta."""
        stack = VGroup(*[self.box(x0, y0, z0 + i * (slab + 0.04), w, d, slab, DARK_TOP, DARK_L, DARK_R) for i in range(n)])
        lights = VGroup(*[Dot(self.p(x0 + 0.25, y0, z0 + i * (slab + 0.04) + slab / 2), radius=0.06, color=GHOST) for i in range(n)])
        return stack, lights


def ease_in(t):
    """Quadratic ease-in (things dropping into a box). Local: Gate A's stub has no ease_in_quad."""
    return t * t


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


def cursor(x, y, s=0.45):
    return Polygon([x, y, 0], [x, y - s, 0], [x + s * 0.28, y - s * 0.72, 0], [x + s * 0.62, y - s * 0.66, 0],
                   fill_color=INK, fill_opacity=1, stroke_color=CARD, stroke_width=2)


def pill(x, y, w, h=0.62, fill="#FFFFFF"):
    return RoundedRectangle(width=w, height=h, corner_radius=h / 2, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


# ═════════════════════════════ WRITING KIT (quill, ink, paper, scribble) ═════════════════════════════
# Added 2026-10-07 from Bear's two reference drawings: a quill drawing a branching outline on a
# scroll, and three scattered pages of scribbled handwriting with a quill. Use when a beat is
# about writing, drafting, authorship, notes, a manuscript, a log, a letter, a signature.
# Terracotta here is only the ink drop and the outline's nodes (dots) — never the lines.


def quill(x, y, s=1.0, angle=0.0, color=INK, fill=BOX_TOP):
    """A drawn quill with its NIB at (x, y); the feather points up-right. `g.nib` is the nib point.
    Kraft-filled feather, ink outline, a shaft line and one barb. Rotate with `angle` (radians)."""
    o = np.array([x, y, 0.0])
    def P(u, v):  # icon units (0..1) → scene, nib at origin, tip at (1, 1.1)·s
        return o + np.array([u * s, v * s, 0.0])
    body = VMobject(fill_color=fill, fill_opacity=1, stroke_color=color, stroke_width=4)
    body.set_points_smoothly([P(0.00, 0.00), P(0.12, 0.62), P(0.55, 1.02), P(1.00, 1.10),
                              P(0.95, 0.68), P(0.62, 0.22), P(0.00, 0.00)])
    shaft = Line(P(0.02, 0.02), P(0.98, 1.06), color=color, stroke_width=3)
    barb = Line(P(0.46, 0.50), P(0.40, 0.72), color=color, stroke_width=2.5)
    g = VGroup(body, shaft, barb)
    if angle:
        g.rotate(angle, about_point=o)
    g.nib = o.copy()
    return g


def inkwell(iso, x0=0.0, y0=0.0, z0=0.0, s=0.7):
    """A dark ink bottle (iso box + narrow neck) with one terracotta ink dot on the lid."""
    body = iso.box(x0, y0, z0, s, s, s * 0.9, DARK_TOP, DARK_L, DARK_R)
    neck = iso.box(x0 + s * 0.3, y0 + s * 0.3, z0 + s * 0.9, s * 0.4, s * 0.4, s * 0.25, DARK_TOP, DARK_L, DARK_R)
    drop = Dot(iso.p(x0 + s * 0.5, y0 + s * 0.5, z0 + s * 1.15), radius=0.07, color=TERRA)
    return VGroup(body, neck, drop)


def paper(x, y, w=2.4, h=3.0, tilt=0.0, fill=PAGE_TOP):
    """A flat 2-D sheet (the scattered-pages drawing): white page, ink outline, kraft drop shadow.
    `tilt` in radians. Returns a VGroup; `.sheet` is the page rectangle for placing lines on it."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    sheet = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    g = VGroup(shadow, sheet)
    if tilt:
        g.rotate(tilt, about_point=[x, y, 0])
    g.sheet = sheet
    g.cx, g.cy, g.w, g.h, g.tilt = float(x), float(y), float(w), float(h), float(tilt)   # read these; never ask the stub for vertices
    return g


def scribble(x, y, w, amp=0.07, waves=None, color=INK, sw=4):
    """One wavy handwriting line from (x, y) rightwards for `w` units. Reads as script, never as type."""
    n = waves or max(3, int(round(w * 3)))
    pts = []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        pts.append([x + w * t, y + amp * np.sin(t * n * 2 * np.pi) * (0.6 + 0.4 * np.cos(t * 5.3)), 0])
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_smoothly(pts)
    return m


def scribble_block(x, y, w, n=3, gap=0.34, last=0.62, color=INK, sw=4):
    """`n` scribble lines stacked downward from (x, y); the last one is `last`× as long (a paragraph end)."""
    return VGroup(*[scribble(x, y - i * gap, w * (last if i == n - 1 else 1.0), color=color, sw=sw) for i in range(n)])


def scribbles_on(page, n=3, inset=0.3, gap=0.34, color=INK, sw=4):
    """Scribble lines laid on a `paper()` group, following its tilt (uses the page's stored geometry)."""
    w = page.w - 2 * inset
    g = scribble_block(page.cx - w / 2, page.cy + page.h / 2 - inset - 0.1, w, n=n, gap=gap, color=color, sw=sw)
    if abs(page.tilt) > 1e-3:
        g.rotate(page.tilt, about_point=[page.cx, page.cy, 0])
    return g


def outline_tree(x, y, h=1.6, levels=2, spread=0.55, color=INK, node=TERRA):
    """A branching outline (the scroll drawing): a trunk rising from (x, y), forking `levels` times,
    a terracotta dot at every tip. Returns VGroup(lines, dots) — draw lines first, dots last."""
    lines, dots = VGroup(), VGroup()
    def grow(px, py, length, lvl, dx):
        qx, qy = px + dx, py + length
        lines.add(Line([px, py, 0], [qx, qy, 0], color=color, stroke_width=4))
        if lvl == 0:
            dots.add(Dot([qx, qy, 0], radius=0.075, color=node))
            return
        for d in (-spread, spread):
            grow(qx, qy, length * 0.62, lvl - 1, d * (0.75 ** (levels - lvl)))
    grow(x, y, h * 0.42, levels, 0.0)
    g = VGroup(lines, dots)
    g.lines, g.dots = lines, dots
    return g


def write_lines(self, q, lines, speed=1.6, hop=0.22, dip=0.06):
    """Animate the quill `q` WRITING each line in `lines`: the nib hops to the line's start, then the
    line draws while the nib rides its tip (the writing motion). `speed` is scene units per second.
    Call between `until()` phrases so each line lands on its words. Works with the midpoint guard."""
    for ln in lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=hop, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib
        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        try:
            length = float(ln.get_arc_length())
        except Exception:          # Gate A's stub has no arc length; any positive number keeps the check moving
            length = 2.0
        rt = max(0.35, length / speed)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=rt, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
        # the small lift between lines keeps the quill from fusing with the ink at GATE T's midpoint
        q.shift([0, dip, 0]); q.nib = q.nib + np.array([0, dip, 0])


def grow_tree(self, q, tree, per=0.45):
    """Animate the quill drawing an `outline_tree`: each segment draws as the nib rides it; dots land last."""
    for ln in tree.lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=0.18, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib
        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=per, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
    self.play(LaggedStart(*[GrowFromCenter(d) for d in tree.dots], lag_ratio=0.15), run_time=0.6)


# ═════════════════════════════ PROFESSOR BEAR (a person is never an icon) ═════════════════════════════
# PROFESSOR BEAR LAW (Bear, 2026-10-07): when a beat needs an icon of a person, or Professor Bear himself,
# do not draw a person token and do not pull a person icon. Show one of the Professor Bear portraits in
# brutalist.art/professor-bear/, chosen at random among those of the right aspect ratio (1x1 · 2x3 · 16x9).
# `./art bear <ratio> --seed <beat>` picks the same way from the shell.
def _pb_dir():
    env = _os.environ.get("ART_HOME")
    cands = [env and _os.path.join(env, "professor-bear")]
    here = _os.path.dirname(_os.path.abspath(__file__))
    for _ in range(8):
        cands.append(_os.path.join(here, "brutalist.art", "professor-bear"))
        cands.append(_os.path.join(here, "professor-bear"))
        here = _os.path.dirname(here)
    cands.append("<books>/brutalist.art/professor-bear")
    for c in cands:
        if c and _os.path.isdir(c):
            return c
    return cands[-1]


_PB_RATIOS = {"1x1": (1.0, 89), "2x3": (2 / 3, 24), "16x9": (16 / 9, 9)}


def _pb_circle(path):
    """A circular cut (alpha outside the circle), cached beside the set in _crops/. Cropping is fine (Bear, 2026-10-07)."""
    from PIL import Image as _Im, ImageDraw as _Dr
    out_dir = _os.path.join(_os.path.dirname(path), "_crops"); _os.makedirs(out_dir, exist_ok=True)
    out = _os.path.join(out_dir, _os.path.splitext(_os.path.basename(path))[0] + "-circle.png")
    if not _os.path.exists(out):
        im = _Im.open(path).convert("RGBA"); w, h = im.size; s = min(w, h); top = max(0, (h - s) // 3)
        im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s))
        mask = _Im.new("L", (s, s), 0); _Dr.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
        im.putalpha(mask); im.save(out)
    return out


def professor_bear(ratio="2x3", height=3.0, seed=None, x=0.0, y=0.0, frame=True, shape="rect"):
    """A Professor Bear portrait (random within `ratio`; `seed` = the beat id for a stable pick across re-renders).
    Returns a Group: kraft drop shadow, the photo, an ink frame. Place with `x, y`; size with `height`.
    `shape="circle"` gives a round cut (use a 1x1 portrait). Cropping is fine: circle, rounded square, tight head shot."""
    import random as _random
    ar, n = _PB_RATIOS[ratio]
    k = _random.Random(str(seed) if seed is not None else None).randint(1, n)
    path = _os.path.join(_pb_dir(), f"professor-bear-{ratio}-{k:02d}.png")
    circle = shape == "circle"
    if circle:
        ar = 1.0
    w = height * ar
    if circle:
        shadow = Circle(radius=height / 2, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Circle(radius=height / 2, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    else:
        shadow = Rectangle(width=w, height=height, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Rectangle(width=w, height=height, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    try:
        img = ImageMobject(_pb_circle(path) if circle else path)
        img.height = height
        img.move_to([x, y, 0])
    except Exception:
        img = Rectangle(width=w, height=height, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    g = Group(shadow, img, border) if frame else Group(img)
    g.path = path
    return g


# ═════════════════════════════ pacing (narration is the clock) ═════════════════════════════
try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json")))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
    _NARR = {b["beat_id"]: b["narration_text"] for b in _SHEET["beats"]}
except Exception:
    _TARGET, _NARR = {}, {}


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def until(self, phrase, lead=0.25):
    """Wait until `phrase` is spoken (its character share of the narration × the measured audio)."""
    bid = type(self).__name__.split("_")[0]
    n, target = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    if not n or not target or phrase not in n:
        return
    gap = target * n.index(phrase) / len(n) - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def finish(self):
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    self.wait(max(0.3, target - _elapsed(self)) if target else 2.0)


# ═════════════════════════════ midpoint guard + pacing (this film) ═════════════════════════════
class ST:
    """Midpoint guard: no animation straddles the clip midpoint (attached at the bottom of the file;
    the classes stay literal `(Scene)` for run.sh's scene discovery)."""
    def play(self, *anims, **kw):
        if not all(isinstance(a, Wait) for a in anims):
            kw["run_time"] = guard(self, float(kw.get("run_time", 1.0)))
        return Scene.play(self, *anims, **kw)


def guard(self, rt):
    tgt = _TARGET.get(type(self).__name__.split("_")[0], 0)
    if not tgt:
        return rt
    mid, t0 = tgt / 2.0, _elapsed(self)
    if t0 < mid + 0.22 and t0 + rt > mid - 0.22:
        room = mid - 0.24 - t0
        if room >= 0.6 * rt and room > 0.25:
            return room
        Scene.wait(self, max(0.02, mid + 0.24 - t0))
    return rt


def at(self, t):
    """Wait until `t` seconds into the beat."""
    g = t - _elapsed(self)
    if g > 0.03:
        self.wait(g)


def hear(self, phrase, lead=0.1, nth=0):
    """Wait until Liam SAYS `phrase` (measured word time from faster-whisper, _ASR). Falls back to until()."""
    import re as _re
    bid = type(self).__name__.split("_")[0]
    words = _ASR.get(bid)
    if not words:
        return until(self, phrase, lead=lead + 0.15)
    norm = lambda w: _re.sub(r"[^a-z0-9]", "", w.lower())
    toks = [norm(x) for x in phrase.split() if norm(x)]
    seq = [norm(w[0]) for w in words]
    hits = [i for i in range(len(seq) - len(toks) + 1) if seq[i:i + len(toks)] == toks]
    if len(hits) <= nth:
        return until(self, phrase, lead=lead + 0.15)
    at(self, words[hits[nth]][1] - lead)


def done(self):
    bid = type(self).__name__.split("_")[0]
    t, tgt = _elapsed(self), _TARGET.get(bid, 0)
    print(f"[pace] {bid} content={t:.2f}s target={tgt:.2f}s" + ("  OVER" if t > tgt - 0.1 else ""))
    self.wait(max(0.05, tgt - t - 0.06) if tgt else 2.0)


def L(s, x, y, size=40):
    return T(s, size).move_to([x, y, 0])


KRAFT_DEEP = "#9C8462"
MONO = "Menlo"


def M(s, size=34, color=INK):
    """Mono label for real commands, paths and error text."""
    return Text(s, font=MONO, color=color, font_size=size)


def x_mark(x, y, r=0.5, w=10):
    return VGroup(Line([x - r, y - r, 0], [x + r, y + r, 0], color=INK, stroke_width=w),
                  Line([x - r, y + r, 0], [x + r, y - r, 0], color=INK, stroke_width=w))


# ── measured word times (faster-whisper on the Kokoro mp3s): { beat id: [[word, seconds], ...] } ──
_ASR = {"BOPEN": [["Research", 0.0], ["Computing", 0.38], ["on", 0.82], ["Explorer", 1.02], ["and", 1.48], ["AICR,", 1.74], ["Optimizing", 2.96], ["GPU", 3.52], ["Usage", 3.9], ["on", 4.3], ["Explorer,", 4.54], ["how", 5.44], ["to", 5.64], ["confirm", 5.78], ["that", 6.1], ["a", 6.3], ["job", 6.38], ["really", 6.6], ["used", 6.86], ["the", 7.18], ["GPU,", 7.36], ["measure", 8.16], ["what", 8.36], ["it", 8.62], ["uses,", 8.72], ["and", 9.34], ["fix", 9.4], ["the", 9.62], ["few", 9.82], ["problems", 10.02], ["that", 10.42], ["waste", 10.68], ["most", 10.9], ["GPU", 11.22], ["time.", 11.62]], "BIDEA": [["Hallo,", 0.68], ["this", 1.26], ["is", 1.38], ["Liam", 1.58], ["in", 1.9], ["for", 2.18], ["Bear.", 2.34], ["First,", 3.1], ["a", 3.28], ["correction.", 3.32], ["A", 4.1], ["GPU", 4.2], ["job", 4.48], ["that", 4.88], ["finishes", 5.08], ["without", 5.32], ["an", 5.66], ["error", 5.82], ["has", 6.04], ["not", 6.18], ["necessarily", 6.44], ["used", 6.9], ["the", 7.32], ["GPU.", 7.52], ["Code", 8.48], ["that", 8.54], ["cannot", 8.74], ["find", 8.98], ["a", 9.24], ["card", 9.38], ["quietly", 9.58], ["runs", 9.9], ["on", 10.34], ["the", 10.54], ["CPU", 10.66], ["and", 11.0], ["code", 11.36], ["that", 11.54], ["finds", 11.74], ["one", 12.02], ["may", 12.22], ["keep", 12.38], ["it", 12.52], ["waiting", 12.66], ["for", 12.84], ["data.", 13.1], ["This", 13.8], ["lecture", 13.96], ["is", 14.2], ["a", 14.42], ["set", 14.54], ["of", 14.68], ["measuring", 14.78], ["tools", 15.02], ["for", 15.4], ["Explorer", 15.7], ["and", 16.1], ["a", 16.38], ["shortlist", 16.5], ["of", 16.84], ["fixes.", 17.02], ["Measure", 17.88], ["first,", 17.98], ["change", 18.68], ["second.", 18.84]], "BDEFS": [["Six", 0.0], ["terms,", 0.28], ["GPU", 0.9], ["utilization,", 1.16], ["the", 2.08], ["share", 2.2], ["of", 2.38], ["the", 2.52], ["last", 2.58], ["second", 2.8], ["in", 3.08], ["which", 3.24], ["the", 3.36], ["card", 3.52], ["ran", 3.72], ["any", 3.94], ["work", 4.12], ["at", 4.32], ["all,", 4.44], ["VRAM,", 5.26], ["the", 5.76], ["card's", 5.84], ["own", 6.12], ["memory", 6.24], ["where", 6.56], ["your", 6.76], ["model", 6.88], ["and", 7.16], ["your", 7.36], ["batch", 7.48], ["live,", 7.7], ["Data", 8.48], ["Loader,", 8.52], ["the", 8.94], ["part", 9.02], ["of", 9.2], ["PyTorch", 9.34], ["that", 9.88], ["reads", 10.02], ["batches", 10.34], ["and", 10.7], ["hands", 10.92], ["data", 11.18], ["to", 11.4], ["the", 11.58], ["card,", 11.72], ["Profiler,", 12.32], ["a", 12.82], ["tool", 12.88], ["that", 13.02], ["tells", 13.2], ["you", 13.38], ["where", 13.56], ["the", 13.68], ["time", 13.78], ["went,", 14.02], ["BF16,", 14.56], ["a", 15.3], ["16", 15.34], ["-bit", 15.68], ["number", 15.78], ["format", 16.0], ["that", 16.32], ["keeps", 16.58], ["the", 16.72], ["range", 16.96], ["of", 17.16], ["32", 17.34], ["-bit", 17.68], ["floats,", 17.92], ["and", 18.8], ["DDP,", 18.84], ["distributed", 19.68], ["data", 19.96], ["parallel.", 20.42], ["One", 21.54], ["model", 21.8], ["copy", 22.16], ["per", 22.48], ["card.", 22.86]], "B10": [["Three", 0.0], ["things", 0.22], ["go", 0.46], ["wrong", 0.68], ["with", 0.92], ["no", 1.1], ["error", 1.32], ["message.", 1.58], ["You", 2.4], ["ask", 2.42], ["for", 2.62], ["one", 2.84], ["kind", 3.04], ["of", 3.22], ["card", 3.4], ["and", 3.6], ["get", 3.8], ["another.", 3.92], ["The", 4.64], ["software", 4.8], ["cannot", 5.14], ["see", 5.46], ["a", 5.78], ["GPU,", 5.94], ["so", 6.58], ["it", 6.76], ["quietly", 6.88], ["runs", 7.12], ["on", 7.56], ["the", 7.82], ["CPU.", 7.98], ["Or", 8.88], ["a", 8.98], ["setting", 9.12], ["left", 9.36], ["in", 9.6], ["your", 9.8], ["shell", 9.94], ["hides", 10.18], ["the", 10.44], ["card", 10.68], ["you", 10.94], ["were", 11.1], ["given.", 11.22]], "B11": [["Explorer", 0.0], ["names", 0.4], ["its", 0.72], ["GPU", 0.94], ["partitions", 1.3], ["by", 1.88], ["purpose.", 2.18], ["GPU", 3.24], ["Short", 3.52], ["and", 3.9], ["GPU", 4.14], ["Interactive", 4.58], ["give", 5.12], ["two", 5.46], ["hours", 5.72], ["for", 6.0], ["tests,", 6.32], ["profiling,", 6.88], ["and", 7.46], ["interactive", 7.5], ["work.", 7.86], ["The", 8.64], ["GPU", 8.72], ["partition", 9.14], ["gives", 9.56], ["eight", 9.94], ["hours", 10.16], ["for", 10.5], ["real", 10.78], ["training.", 11.0], ["Sharing", 11.94], ["gives", 12.02], ["one.", 12.32], ["Multi", 13.26], ["-GPU", 13.26], ["goes", 13.72], ["to", 14.16], ["24", 14.4], ["and", 14.76], ["needs", 15.2], ["an", 15.42], ["approved", 15.58], ["access", 15.9], ["request.", 16.3]], "B12": [["Here", 0.0], ["is", 0.18], ["the", 0.32], ["cluster", 0.46], ["itself", 0.74], ["read", 1.18], ["from", 1.64], ["the", 1.88], ["login", 2.04], ["node", 2.3], ["without", 2.66], ["submitting", 3.0], ["anything.", 3.44], ["The", 4.44], ["three", 4.52], ["GPU", 4.76], ["partitions", 5.2], ["list", 5.84], ["the", 6.18], ["same", 6.4], ["25", 6.58], ["nodes", 7.1], ["with", 7.58], ["limits", 7.92], ["of", 8.2], ["eight", 8.38], ["hours,", 8.56], ["two", 9.14], ["hours,", 9.28], ["and", 9.8], ["two", 9.84], ["hours.", 10.0], ["Sharing", 11.0], ["is", 11.02], ["its", 11.28], ["own", 11.42], ["partition", 11.6], ["with", 12.06], ["one", 12.44], ["hour.", 12.68]], "B13": [["Never", 0.0], ["guess", 0.22], ["the", 0.42], ["card", 0.62], ["name,", 0.86], ["ask", 1.3], ["the", 1.42], ["cluster.", 1.62], ["Partition", 2.52], ["GPU", 2.82], ["holds", 3.22], ["5", 3.68], ["types,", 4.0], ["V100S", 4.64], ["XM2,", 5.34], ["mostly", 6.24], ["4", 6.44], ["to", 6.78], ["a", 6.94], ["node,", 7.06], ["V100PCIE2,", 7.64], ["a", 9.42], ["100,", 9.46], ["3,", 9.94], ["or", 10.24], ["4,", 10.3], ["H200,", 10.86], ["8,", 11.74], ["and", 11.98], ["T4,", 12.04], ["4.", 12.68], ["Some", 13.12], ["written", 13.26], ["guides", 13.44], ["list", 13.86], ["only", 14.06], ["two", 14.32], ["of", 14.56], ["these.", 14.7]], "B14": [["Now", 0.0], ["the", 0.18], ["request", 0.34], ["from", 0.68], ["a", 0.94], ["template", 1.06], ["in", 1.26], ["research", 1.54], ["computing's", 1.86], ["training", 2.52], ["material,", 2.76], ["a", 3.76], ["GPU", 3.8], ["partition,", 4.18], ["a", 5.28], ["Gresline", 5.34], ["that", 5.78], ["names", 5.98], ["the", 6.22], ["card,", 6.42], ["CPUs", 7.14], ["for", 7.4], ["your", 7.8], ["data", 7.94], ["loading,", 8.16], ["memory,", 9.12], ["a", 9.48], ["time", 9.5], ["limit,", 9.74], ["and", 10.28], ["a", 10.36], ["place", 10.44], ["for", 10.64], ["the", 10.88], ["logs.", 10.98]], "B15": [["Two", 0.0], ["lines", 0.16], ["deserve", 0.46], ["a", 0.8], ["pause,", 1.0], ["Mem", 1.68], ["is", 1.68], ["CPU", 1.92], ["memory.", 2.32], ["The", 3.16], ["card's", 3.26], ["own", 3.62], ["memory", 3.74], ["VRAM", 4.12], ["comes", 4.64], ["with", 4.94], ["the", 5.12], ["card,", 5.28], ["so", 5.8], ["raising", 5.92], ["Mem", 6.2], ["never", 6.48], ["fixes", 6.76], ["a", 7.06], ["GPU", 7.28], ["out", 7.6], ["of", 7.94], ["memory", 8.12], ["error,", 8.4], ["and", 9.14], ["a", 9.26], ["baregraz", 9.36], ["of", 9.82], ["GPU", 10.0], ["colon", 10.44], ["1", 10.78], ["may", 11.14], ["land", 11.3], ["you", 11.56], ["on", 11.72], ["a", 11.84], ["different", 11.94], ["card.", 12.14], ["Name", 12.92], ["the", 13.06], ["type.", 13.24]], "B16": [["The", 0.0], ["environment", 0.14], ["is", 0.56], ["plain,", 0.88], ["a", 1.44], ["virtual", 1.58], ["environment", 1.84], ["from", 2.38], ["system", 2.7], ["Python", 3.02], ["and", 3.38], ["pip", 3.82], ["wheels.", 3.96], ["PyTorch's", 5.24], ["wheel", 5.74], ["carries", 5.96], ["its", 6.32], ["own", 6.52], ["CUDA", 6.78], ["runtime,", 7.06], ["and", 7.88], ["a", 7.96], ["GPU", 8.08], ["node", 8.4], ["already", 8.86], ["has", 9.18], ["the", 9.46], ["driver,", 9.64], ["so", 10.2], ["you", 10.4], ["load", 10.54], ["no", 10.74], ["CUDA", 11.0], ["module", 11.34], ["for", 11.64], ["it.", 12.0]], "B17": [["Two", 0.0], ["facts", 0.18], ["recorded", 0.52], ["on", 0.98], ["the", 1.2], ["login", 1.32], ["node.", 1.58], ["GPU", 2.7], ["logs", 2.74], ["and", 3.16], ["SEFF", 3.46], ["are", 4.0], ["installed,", 4.3], ["but", 5.08], ["NVIDIA", 5.14], ["SMI", 5.52], ["is", 6.08], ["missing,", 6.34], ["so", 6.96], ["GPU", 7.06], ["checks", 7.42], ["belong", 7.8], ["inside", 8.16], ["a", 8.54], ["job.", 8.74], ["And", 9.66], ["a", 9.74], ["Python", 9.82], ["module", 10.12], ["does", 10.58], ["exist,", 10.82], ["version", 11.54], ["3", 11.66], [".13", 12.08], [".5,", 12.68], ["though", 13.46], ["some", 13.56], ["material", 13.76], ["says", 14.08], ["there", 14.46], ["is", 14.7], ["none.", 14.84]], "B18": [["Never", 0.0], ["trust", 0.24], ["the", 0.52], ["allocation.", 0.68], ["This", 1.8], ["verify", 1.9], ["script", 2.26], ["checks", 2.64], ["five", 2.98], ["things,", 3.28], ["Q2", 3.98], ["available,", 4.1], ["the", 4.74], ["cards", 4.82], ["and", 5.1], ["their", 5.3], ["memory,", 5.46], ["the", 6.0], ["visible", 6.1], ["device's", 6.34], ["variable,", 6.88], ["NVIDIA", 7.62], ["SMI,", 7.82], ["and", 8.78], ["a", 8.9], ["Tensor", 8.96], ["round", 9.24], ["trip.", 9.54], ["Available", 10.64], ["means", 10.64], ["PyTorch", 11.08], ["sees", 11.76], ["a", 11.92], ["card.", 12.1], ["The", 12.64], ["round", 12.74], ["trip", 12.94], ["proves", 13.18], ["it", 13.46], ["can", 13.66], ["use", 13.78], ["one.", 13.94]], "B19": [["Slurm", 0.0], ["sets", 0.38], ["cue", 0.58], ["to", 0.82], ["visible", 0.94], ["devices", 1.24], ["to", 1.7], ["your", 1.96], ["card's", 2.1], ["numbers.", 2.48], ["Zero", 3.22], ["is", 3.34], ["one", 3.5], ["card,", 3.74], ["zero", 4.26], ["comma", 4.48], ["one", 4.78], ["is", 5.08], ["two.", 5.22], ["Leave", 5.98], ["it", 6.16], ["alone", 6.32], ["unless", 6.66], ["you", 6.96], ["want", 7.16], ["a", 7.34], ["subset.", 7.48], ["It", 8.22], ["can", 8.24], ["be", 8.34], ["unset", 8.44], ["in", 8.88], ["an", 9.04], ["interactive", 9.12], ["session,", 9.56], ["so", 10.2], ["it", 10.34], ["is", 10.46], ["never", 10.58], ["proof", 10.84], ["either", 11.12], ["way.", 11.34], ["The", 12.08], ["round", 12.18], ["trip", 12.4], ["is.", 12.66]], "B20": [["Now", 0.0], ["watch", 0.18], ["it,", 0.48], ["NVIDIA", 0.9], ["SMI", 1.06], ["has", 1.68], ["two", 1.9], ["numbers", 2.14], ["that", 2.4], ["matter,", 2.66], ["GPU", 3.46], ["utilization,", 3.74], ["the", 4.8], ["share", 4.86], ["of", 5.04], ["the", 5.2], ["last", 5.26], ["second", 5.48], ["in", 5.78], ["which", 5.98], ["a", 6.1], ["kernel", 6.22], ["was", 6.38], ["running,", 6.62], ["in", 7.42], ["this", 7.5], ["example", 7.64], ["87", 8.04], ["%", 8.64], ["healthy,", 9.08], ["below", 9.86], ["50", 9.94], ["means", 10.24], ["something", 10.56], ["is", 10.84], ["wrong,", 11.08], ["and", 11.8], ["memory", 11.98], ["here", 12.26], ["about", 12.66], ["a", 12.94], ["fifth", 13.08], ["of", 13.26], ["the", 13.44], ["card.", 13.54]], "B21": [["To", 0.0], ["see", 0.12], ["it", 0.28], ["live,", 0.4], ["a", 0.84], ["person", 0.88], ["opens", 1.08], ["a", 1.5], ["second", 1.7], ["terminal", 1.94], ["on", 2.4], ["the", 2.62], ["compute", 2.76], ["node", 3.02], ["and", 3.3], ["runs", 3.56], ["watch.", 3.82], ["Nvitop", 5.16], ["is", 5.64], ["a", 5.8], ["richer", 5.9], ["view", 6.1], ["per", 6.4], ["process,", 6.64], ["so", 7.24], ["you", 7.48], ["can", 7.58], ["confirm", 7.74], ["that", 8.12], ["your", 8.32], ["own", 8.46], ["Python", 8.66], ["is", 9.0], ["using", 9.26], ["the", 9.52], ["card.", 9.68], ["A", 10.38], ["coding", 10.48], ["agent", 10.78], ["should", 11.1], ["not", 11.32], ["run", 11.52], ["watch,", 11.74], ["it", 12.32], ["never", 12.42], ["exits.", 12.66]], "B22": [["read", 0.0], ["them", 0.18], ["as", 0.36], ["two", 0.5], ["axes", 0.7], ["high", 1.06], ["memory", 1.54], ["with", 1.84], ["low", 2.08], ["utilization", 2.3], ["loaded", 2.84], ["but", 3.36], ["nothing", 3.6], ["is", 3.82], ["feeding", 4.1], ["it", 4.32], ["low", 4.62], ["and", 5.18], ["low", 5.32], ["the", 5.58], ["card", 5.8], ["sits", 6.0], ["empty", 6.28], ["high", 6.74], ["utilization", 7.3], ["with", 7.86], ["low", 8.16], ["memory", 8.38], ["healthy", 8.76], ["raise", 9.1], ["the", 9.5], ["batch", 9.66], ["high", 9.98], ["and", 10.38], ["high", 10.52], ["good", 10.76], ["fifteen", 11.08], ["percent", 11.58], ["utilization", 11.88], ["seventy", 12.58], ["five", 13.04], ["memory", 13.4], ["data", 13.86], ["starvation", 14.2]], "B23": [["Use", 0.0], ["one", 0.18], ["set", 0.42], ["of", 0.64], ["bands", 0.76], ["under", 1.08], ["50", 1.36], ["%", 1.68], ["is", 2.02], ["a", 2.22], ["problem.", 2.36], ["Under", 2.96], ["60,", 3.1], ["suspect", 3.78], ["the", 4.0], ["data", 4.26], ["pipeline.", 4.5], ["60", 5.6], ["to", 5.92], ["70", 6.1], ["is", 6.38], ["amber,", 6.66], ["70", 7.22], ["acceptable,", 7.48], ["80", 8.42], ["to", 8.62], ["100", 8.86], ["the", 9.16], ["target.", 9.38], ["For", 10.16], ["memory,", 10.32], ["60", 10.82], ["to", 11.1], ["90", 11.28], ["%", 11.6], ["is", 11.9], ["healthy.", 12.06], ["Under", 12.72], ["40", 12.84], ["means", 13.12], ["room", 13.44], ["for", 13.72], ["a", 13.96], ["bigger", 14.06], ["batch.", 14.26]], "B24": [["Explorer", 0.0], ["also", 0.4], ["watches", 0.66], ["for", 1.08], ["idle", 1.36], ["cards.", 1.62], ["A", 2.48], ["bot", 2.48], ["called", 2.64], ["idlebot", 2.94], ["emails", 3.54], ["you", 3.92], ["after", 4.22], ["about", 4.5], ["15", 4.78], ["minutes", 5.28], ["of", 5.54], ["underuse", 5.74], ["and", 6.16], ["the", 6.52], ["job", 6.66], ["is", 6.88], ["cancelled", 7.08], ["after", 7.44], ["about", 7.78], ["an", 8.08], ["hour.", 8.2], ["We", 8.88], ["found", 8.96], ["no", 9.14], ["published", 9.4], ["percentage", 9.82], ["for", 10.26], ["underuse.", 10.6], ["A", 11.44], ["stalled", 11.5], ["job", 11.8], ["holds", 12.16], ["its", 12.46], ["card", 12.68], ["in", 13.0], ["your", 13.22], ["queue", 13.36], ["place", 13.58], ["while", 13.88], ["doing", 14.12], ["nothing.", 14.34]], "B30": [["A", 0.0], ["profiler", 0.16], ["tells", 0.56], ["you", 0.8], ["where", 1.0], ["the", 1.1], ["time", 1.22], ["went,", 1.44], ["four", 1.88], ["layers,", 2.08], ["lightest", 2.72], ["first,", 2.92], ["live", 3.84], ["tools,", 3.94], ["NVIDIA", 4.5], ["SMI", 4.72], ["and", 5.46], ["NVI", 5.64], ["top,", 6.06], ["the", 6.66], ["framework", 6.72], ["profiler,", 7.02], ["insight", 8.12], ["systems", 8.32], ["for", 8.72], ["timeline", 8.98], ["and", 9.36], ["insight", 9.78], ["compute", 10.14], ["for", 10.5], ["one", 10.74], ["kernel,", 10.94], ["stop", 11.56], ["as", 11.8], ["soon", 11.98], ["as", 12.18], ["you", 12.32], ["know,", 12.44], ["most", 12.84], ["problems", 13.0], ["show", 13.42], ["by", 13.72], ["layer", 13.96], ["two.", 14.16]], "B31": [["Profile", 0.0], ["in", 0.38], ["a", 0.56], ["short", 0.7], ["interactive", 0.86], ["session,", 1.3], ["not", 2.06], ["through", 2.1], ["the", 2.32], ["batch", 2.48], ["queue.", 2.66], ["Get", 3.44], ["a", 3.6], ["session", 3.74], ["on", 3.94], ["GPU", 4.16], ["short,", 4.58], ["activate", 5.34], ["your", 5.6], ["environment,", 5.82], ["run", 6.58], ["50", 6.72], ["steps,", 7.08], ["change", 7.64], ["one", 7.84], ["thing,", 8.1], ["repeat.", 8.46], ["If", 9.1], ["it", 9.2], ["runs", 9.3], ["in", 9.5], ["under", 9.7], ["30", 9.86], ["minutes,", 10.18], ["skip", 10.54], ["the", 10.74], ["batch", 10.94], ["queue.", 11.18]], "B32": [["The", 0.0], ["PiTorch", 0.16], ["profiler", 0.7], ["needs", 1.18], ["no", 1.42], ["install.", 1.72], ["Warm", 2.7], ["up", 2.76], ["for", 2.92], ["a", 3.14], ["few", 3.22], ["untimed", 3.36], ["steps", 3.84], ["or", 4.12], ["startup", 4.4], ["cost", 4.72], ["swamps", 5.12], ["the", 5.58], ["table.", 5.76], ["Then", 6.54], ["profile", 6.74], ["a", 7.1], ["small", 7.28], ["window,", 7.54], ["wait", 8.16], ["one", 8.32], ["step,", 8.58], ["warm", 9.0], ["up", 9.16], ["one,", 9.34], ["record", 9.82], ["10,", 9.9], ["step", 10.68], ["the", 10.9], ["profiler", 11.08], ["every", 11.56], ["iteration", 11.84], ["and", 12.34], ["print", 12.7], ["the", 12.88], ["table", 13.02], ["sorted", 13.32], ["by", 13.66], ["queue", 13.94], ["to", 14.14], ["time.", 14.26]], "B33": [["Read", 0.0], ["the", 0.16], ["table", 0.32], ["in", 0.52], ["order,", 0.74], ["gaps", 1.38], ["between", 1.38], ["kernels.", 1.72], ["The", 2.36], ["GPU", 2.42], ["is", 2.72], ["idle.", 2.98], ["Large", 3.76], ["copy", 3.94], ["rows,", 4.28], ["data", 4.88], ["shuttling", 5.0], ["between", 5.44], ["CPU", 5.76], ["and", 6.2], ["GPU.", 6.5], ["CPU", 7.52], ["time", 7.82], ["far", 8.12], ["above", 8.42], ["CUDA", 8.68], ["time,", 9.02], ["the", 9.42], ["work", 9.5], ["is", 9.66], ["not", 9.82], ["on", 10.02], ["the", 10.16], ["card.", 10.3], ["And", 10.88], ["the", 10.96], ["data", 11.08], ["loader", 11.32], ["at", 11.6], ["the", 11.8], ["top,", 11.96], ["the", 12.34], ["pipeline,", 12.42], ["is", 12.9], ["the", 13.1], ["bottleneck.", 13.26], ["This", 14.08], ["example", 14.2], ["is", 14.54], ["from", 14.8], ["research", 14.98], ["computing's", 15.3], ["material,", 15.94], ["not", 16.54], ["our", 16.7], ["run.", 16.84]], "B34": [["When", 0.0], ["order", 0.14], ["matters,", 0.32], ["trace", 0.88], ["a", 0.98], ["timeline", 1.18], ["with", 1.5], ["Nsight", 1.84], ["systems.", 2.22], ["Profile", 3.28], ["one", 3.44], ["or", 3.7], ["two", 3.8], ["epochs,", 3.96], ["never", 4.62], ["a", 4.72], ["hundred.", 4.88], ["Write", 5.4], ["the", 5.54], ["report", 5.68], ["to", 5.98], ["scratch", 6.18], ["and", 6.5], ["open", 6.8], ["it", 7.0], ["on", 7.14], ["your", 7.24], ["laptop.", 7.36], ["We", 8.24], ["could", 8.32], ["not", 8.44], ["confirm", 8.6], ["that", 9.0], ["Nsys", 9.2], ["is", 9.6], ["on", 9.82], ["Explorer's", 9.98], ["path.", 10.52], ["Check", 11.18], ["the", 11.26], ["module", 11.46], ["list", 11.76], ["or", 12.06], ["ask.", 12.34]], "B35": [["On", 0.0], ["the", 0.14], ["timeline,", 0.26], ["an", 0.88], ["empty", 0.94], ["GPU", 1.22], ["row", 1.6], ["with", 2.0], ["short", 2.24], ["bursts", 2.52], ["means", 2.94], ["data", 3.26], ["arrives", 3.62], ["late.", 4.04], ["File", 5.14], ["reads", 5.14], ["filling", 5.38], ["the", 5.68], ["gaps", 5.88], ["mean", 6.12], ["you", 6.4], ["are", 6.56], ["reading", 6.66], ["a", 6.88], ["network", 7.06], ["file", 7.32], ["system", 7.62], ["during", 7.96], ["training.", 8.26], ["Copies", 9.3], ["scattered", 9.52], ["through", 9.78], ["each", 10.14], ["step", 10.34], ["mean", 10.62], ["data", 10.88], ["moves", 11.18], ["inside", 11.48], ["the", 11.92], ["loop.", 12.1], ["Pin", 12.7], ["the", 12.76], ["memory.", 12.9]], "B40": [["The", 0.0], ["most", 0.12], ["common", 0.24], ["bottleneck", 0.62], ["is", 1.04], ["not", 1.28], ["the", 1.5], ["model.", 1.64], ["A", 2.24], ["fast", 2.36], ["cook", 2.66], ["waits", 2.96], ["for", 3.22], ["slow", 3.52], ["deliveries.", 3.8], ["Say", 4.7], ["the", 4.86], ["card", 5.0], ["computes", 5.22], ["a", 5.66], ["batch", 5.78], ["in", 5.96], ["25", 6.18], ["milliseconds", 6.7], ["and", 7.16], ["the", 7.58], ["loader", 7.7], ["needs", 7.88], ["60.", 8.16], ["The", 9.1], ["card", 9.28], ["idles", 9.52], ["35", 9.92], ["of", 10.46], ["every", 10.72], ["60.", 10.98], ["No", 11.76], ["model", 11.96], ["change", 12.24], ["fixes", 12.58], ["that.", 12.98]], "B41": [["Two", 0.0], ["stopwatch", 0.2], ["tests", 0.7], ["need", 1.1], ["no", 1.34], ["profiler,", 1.6], ["first", 2.56], ["time", 2.92], ["50", 3.34], ["batches", 3.68], ["out", 4.06], ["of", 4.28], ["your", 4.36], ["loader", 4.48], ["with", 4.74], ["no", 5.08], ["GPU", 5.32], ["work", 5.66], ["at", 6.06], ["all.", 6.22]], "B42": [["Second,", 0.0], ["time", 0.62], ["50", 0.72], ["forward", 1.06], ["and", 1.42], ["backward", 1.62], ["steps", 1.92], ["on", 2.3], ["synthetic", 2.56], ["data", 2.98], ["made", 3.42], ["directly", 3.64], ["on", 4.12], ["the", 4.36], ["GPU", 4.5], ["and", 5.0], ["synchronized", 5.52], ["before", 5.98], ["you", 6.4], ["stop", 6.56], ["the", 6.82], ["clock.", 7.02], ["If", 8.0], ["loading", 8.14], ["takes", 8.42], ["longer", 8.72], ["than", 9.08], ["computing,", 9.36], ["you", 10.18], ["are", 10.28], ["data", 10.42], ["bound.", 10.66]], "B43": [["The", 0.0], ["fix", 0.14], ["usually", 0.3], ["lives", 0.58], ["in", 0.96], ["four", 1.18], ["data", 1.42], ["loader", 1.7], ["settings.", 1.94], ["Workers", 3.36], ["CPU", 3.36], ["processes", 3.84], ["that", 4.46], ["load", 4.78], ["in", 5.0], ["parallel.", 5.18], ["Pin", 6.02], ["memory", 6.14], ["page", 6.5], ["-locked", 6.9], ["RAM", 7.22], ["for", 7.64], ["faster", 8.0], ["copies.", 8.32], ["Persistent", 9.18], ["workers", 9.5], ["do", 9.94], ["not", 10.24], ["restart", 10.4], ["them", 10.78], ["every", 10.98], ["epoch.", 11.2], ["Pre", 11.96], ["-fetch", 12.06], ["factor", 12.26], ["batches", 12.74], ["each", 13.14], ["worker", 13.46], ["prepares", 13.82], ["ahead.", 14.16]], "B44": [["Starting", 0.0], ["values,", 0.32], ["workers,", 0.94], ["CPUs", 1.4], ["per", 1.66], ["task,", 2.0], ["minus", 2.48], ["one,", 2.58], ["never", 3.06], ["zero.", 3.18], ["Pin", 3.98], ["memory,", 4.12], ["always", 4.66], ["on", 4.86], ["in", 5.1], ["a", 5.22], ["GPU", 5.32], ["job.", 5.6], ["Persistent", 6.42], ["workers,", 6.76], ["on", 7.34], ["whenever", 7.44], ["workers", 7.66], ["is", 8.02], ["above", 8.22], ["zero.", 8.46], ["Prefetch", 9.44], ["two,", 9.8], ["raise", 10.32], ["it", 10.42], ["if", 10.56], ["still", 10.64], ["slow.", 10.88], ["So", 11.64], ["ask", 11.76], ["for", 11.96], ["CPUs", 12.16], ["per", 12.6], ["task", 12.88], ["equal", 13.26], ["to", 13.52], ["workers", 13.78], ["plus", 14.0], ["one", 14.36], ["and", 14.62], ["at", 14.8], ["least", 14.9], ["four.", 15.04]], "B45": [["The", 0.0], ["benchmark", 0.14], ["script", 0.38], ["tries", 0.76], ["four", 1.1], ["configurations,", 1.38], ["zero", 2.66], ["workers,", 2.84], ["two,", 3.5], ["four,", 3.76], ["and", 4.1], ["four", 4.16], ["with", 4.42], ["pinned", 4.64], ["memory,", 4.9], ["persistent", 5.54], ["workers,", 5.82], ["and", 6.48], ["prefetch.", 6.62], ["It", 7.64], ["prints", 7.82], ["the", 8.02], ["load", 8.22], ["time", 8.4], ["for", 8.66], ["each", 8.9], ["and", 9.1], ["compares", 9.3], ["it", 9.66], ["with", 9.88], ["the", 10.04], ["GPU's", 10.22], ["time.", 10.72], ["We", 11.34], ["did", 11.42], ["not", 11.52], ["run", 11.72], ["it.", 11.94]], "B46": [["and", 0.0], ["never", 0.14], ["feed", 0.36], ["the", 0.58], ["card", 0.72], ["one", 0.94], ["item", 1.2], ["at", 1.48], ["a", 1.64], ["time.", 1.76], ["Every", 2.58], ["call", 2.58], ["has", 2.84], ["a", 3.02], ["fixed", 3.16], ["cost.", 3.38], ["Launch,", 4.16], ["transfer", 4.48], ["setup,", 4.72], ["synchronization.", 5.38], ["10", 6.58], [",000", 6.74], ["single", 7.12], ["sample", 7.32], ["calls", 7.74], ["pay", 8.06], ["it", 8.38], ["10", 8.52], [",000", 8.76], ["times.", 9.18], ["One", 9.8], ["batched", 9.96], ["call", 10.34], ["pays", 10.6], ["it", 10.88], ["once.", 11.06]], "B47": [["Where", 0.0], ["the", 0.14], ["data", 0.24], ["lives", 0.44], ["matters.", 0.74], ["On", 1.46], ["Explorer,", 1.54], ["Home,", 2.26], ["Scratch,", 2.7], ["and", 2.92], ["Projects", 2.98], ["are", 3.36], ["all", 3.56], ["network", 3.76], ["file", 4.06], ["systems.", 4.4], ["Keep", 5.28], ["data", 5.42], ["in", 5.68], ["Scratch", 5.92], ["or", 6.32], ["a", 6.48], ["Projects", 6.64], ["folder", 6.92], ["packed", 7.26], ["into", 7.74], ["a", 7.98], ["few", 8.1], ["large", 8.26], ["files,", 8.54], ["never", 9.28], ["millions", 9.42], ["of", 9.76], ["small", 10.0], ["ones,", 10.28], ["and", 10.72], ["never", 10.82], ["in", 11.0], ["Home.", 11.14], ["Scratch", 11.94], ["is", 12.22], ["purged,", 12.4], ["so", 12.96], ["keep", 13.06], ["your", 13.22], ["original", 13.38], ["elsewhere.", 13.74]], "B48": [["Research", 0.0], ["Computing's", 0.34], ["material", 0.94], ["illustrates", 1.3], ["the", 1.84], ["direction,", 2.12], ["with", 2.98], ["no", 3.1], ["workers", 3.32], ["about", 3.72], ["18", 4.08], ["%", 4.44], ["utilization", 4.8], ["420", 5.34], ["images", 6.12], ["a", 6.72], ["second,", 6.98], ["8", 7.6], ["workers", 7.74], ["in", 8.12], ["pinned", 8.3], ["memory", 8.52], ["55", 8.9], ["%", 9.52], ["1300,", 10.04], ["add", 11.2], ["prefetching", 11.28], ["82", 11.96], ["%", 12.36], ["1950,", 12.78], ["no", 13.84], ["script", 14.02], ["produces", 14.34], ["these,", 14.78], ["use", 15.5], ["them", 15.64], ["for", 15.82], ["direction", 16.02], ["not", 16.46], ["as", 16.78], ["a", 16.92], ["promise.", 17.02]], "B50": [["Batch", 0.0], ["size", 0.28], ["is", 0.5], ["the", 0.74], ["simplest", 0.92], ["lever.", 1.3], ["Doubling", 2.08], ["it", 2.28], ["roughly", 2.4], ["doubles", 2.7], ["throughput", 3.08], ["until", 3.48], ["the", 3.82], ["card", 3.96], ["is", 4.18], ["saturated", 4.32], ["if", 4.84], ["the", 5.14], ["memory", 5.26], ["is", 5.46], ["there.", 5.72], ["If", 6.46], ["memory", 6.56], ["sits", 6.86], ["near", 7.18], ["20", 7.48], ["%", 7.78], ["and", 8.12], ["nothing", 8.36], ["fails,", 8.62], ["double", 9.38], ["the", 9.5], ["batch", 9.66], ["and", 9.92], ["measure", 10.1], ["again.", 10.34], ["Stop", 11.14], ["short", 11.34], ["of", 11.6], ["the", 11.74], ["largest", 11.88], ["size", 12.18], ["that", 12.62], ["fits", 12.9], ["because", 13.18], ["the", 13.56], ["optimizer", 13.74], ["needs", 14.32], ["memory", 14.58], ["too.", 14.94]], "B51": [["To", 0.0], ["find", 0.14], ["the", 0.36], ["ceiling,", 0.52], ["try", 0.98], ["sizes", 1.18], ["and", 1.64], ["narrow", 1.94], ["the", 2.18], ["search.", 2.42], ["Make", 3.18], ["a", 3.3], ["batch,", 3.44], ["run", 3.88], ["forward", 4.02], ["and", 4.36], ["backward,", 4.54], ["catch", 5.2], ["the", 5.34], ["out", 5.58], ["of", 5.72], ["memory", 5.86], ["error,", 6.14], ["free", 6.7], ["the", 6.84], ["memory", 7.0], ["and", 7.22], ["search", 7.52], ["again.", 7.74], ["Then", 8.72], ["leave", 8.82], ["a", 9.02], ["margin", 9.16], ["below", 9.48], ["the", 9.76], ["answer.", 9.98]], "B52": [["Mixed", 0.0], ["precision", 0.24], ["is", 0.64], ["next.", 0.86], ["Wrap", 1.52], ["the", 1.56], ["forward", 1.72], ["pass", 1.94], ["and", 2.28], ["the", 2.48], ["loss", 2.58], ["in", 2.8], ["autocast", 3.02], ["and", 3.56], ["leave", 3.8], ["the", 3.98], ["backward", 4.14], ["call", 4.44], ["outside", 4.74], ["it.", 5.14], ["Do", 6.06], ["not", 6.14], ["cast", 6.28], ["the", 6.54], ["model", 6.72], ["by", 6.92], ["hand.", 7.2], ["Under", 7.84], ["autocast", 7.98], ["the", 8.6], ["weights,", 8.82], ["the", 9.32], ["loss", 9.36], ["and", 9.58], ["normalization", 9.78], ["stay", 10.42], ["in", 10.84], ["32", 11.06], ["bits.", 11.48]], "B53": [["A", 0.0], ["16", 0.14], ["-bit", 0.44], ["format", 0.62], ["splits", 1.0], ["its", 1.34], ["bits", 1.54], ["between", 1.74], ["range", 2.12], ["and", 2.42], ["precision.", 2.7], ["Bf16", 3.8], ["keeps", 4.36], ["the", 4.64], ["full", 4.84], ["range,", 5.0], ["so", 5.5], ["no", 5.62], ["loss", 5.76], ["scalar.", 5.96], ["Fp16", 6.9], ["keeps", 7.46], ["more", 7.76], ["precision", 7.98], ["but", 8.32], ["little", 8.6], ["range,", 8.78], ["so", 9.28], ["it", 9.42], ["needs", 9.54], ["one.", 9.72], ["Bf16", 10.48], ["on", 11.04], ["a", 11.2], ["100", 11.3], ["and", 11.7], ["newer.", 11.92], ["Fp16", 12.66], ["on", 13.22], ["V100", 13.46], ["and", 14.08], ["T4.", 14.44]], "B54": [["Choose", 0.0], ["by", 0.26], ["compute", 0.5], ["capability,", 0.84], ["not", 1.56], ["by", 1.68], ["the", 1.9], ["library's", 2.04], ["own", 2.54], ["support", 2.7], ["call.", 3.1], ["One", 3.8], ["demo", 4.02], ["script", 4.32], ["picks", 4.68], ["with", 4.98], ["that", 5.2], ["call.", 5.4], ["A", 6.16], ["second", 6.26], ["script", 6.5], ["says", 6.82], ["the", 7.06], ["call", 7.24], ["reports", 7.44], ["true", 7.9], ["even", 8.2], ["on", 8.5], ["a", 8.64], ["V100", 8.72], ["and", 9.2], ["picks", 9.62], ["by", 9.84], ["capability.", 10.1], ["Major", 11.12], ["version", 11.34], ["8", 11.64], ["or", 12.0], ["higher", 12.28], ["means", 12.52], ["BF16.", 12.84]], "B55": [["Be", 0.0], ["honest", 0.14], ["about", 0.32], ["gains.", 0.66], ["Total", 1.5], ["memory", 1.52], ["does", 1.86], ["not", 2.1], ["drop", 2.32], ["by", 2.56], ["half", 2.82], ["because", 3.08], ["optimizer", 3.46], ["state", 4.08], ["and", 4.4], ["master", 4.6], ["weight", 4.9], ["stay", 5.16], ["put.", 5.46], ["The", 6.28], ["speed", 6.36], ["up", 6.6], ["depends", 6.78], ["on", 7.12], ["how", 7.3], ["much", 7.48], ["of", 7.68], ["your", 7.84], ["work", 7.94], ["is", 8.16], ["matrix", 8.34], ["and", 8.74], ["convolution", 9.04], ["maths.", 9.48], ["The", 10.3], ["material", 10.36], ["quotes", 10.72], ["up", 11.04], ["to", 11.22], ["eight", 11.4], ["times", 11.56], ["in", 11.94], ["one", 12.14], ["place", 12.34], ["and", 12.62], ["one", 12.88], ["and", 13.02], ["a", 13.14], ["half", 13.22], ["to", 13.4], ["three", 13.56], ["in", 13.86], ["another.", 14.02], ["Quote", 14.8], ["neither.", 14.9]], "B56": [["Gradient", 0.0], ["checkpointing", 0.4], ["is", 1.04], ["the", 1.18], ["last", 1.34], ["resort", 1.6], ["for", 1.96], ["memory.", 2.22], ["Activations", 2.98], ["are", 3.52], ["recomputed", 3.66], ["in", 4.18], ["the", 4.36], ["backward", 4.48], ["pass", 4.8], ["instead", 5.2], ["of", 5.62], ["stored.", 5.78], ["The", 6.7], ["material", 6.78], ["claims", 7.16], ["60", 7.44], ["-70", 7.92], ["%", 8.46], ["less", 8.76], ["activation", 8.98], ["memory", 9.48], ["for", 9.96], ["30", 10.28], ["%", 10.62], ["more", 10.94], ["compute", 11.16], ["with", 11.58], ["no", 11.88], ["source.", 12.12], ["In", 12.86], ["hugging", 12.94], ["face", 13.2], ["it", 13.6], ["is", 13.86], ["one", 13.98], ["call.", 14.2]], "B57": [["And", 0.0], ["watch", 0.16], ["the", 0.34], ["memory,", 0.56], ["log", 1.42], ["peak", 1.42], ["VRAM", 1.68], ["per", 2.54], ["epoch", 2.78], ["with", 3.1], ["max", 3.34], ["memory", 3.68], ["allocated,", 4.0], ["and", 4.94], ["compare", 5.04], ["it", 5.34], ["with", 5.52], ["the", 5.66], ["cards", 5.8], ["total.", 6.02], ["After", 7.06], ["an", 7.28], ["out", 7.44], ["of", 7.56], ["memory", 7.7], ["error,", 8.02], ["delete", 8.58], ["the", 8.76], ["big", 8.96], ["objects", 9.1], ["and", 9.52], ["empty", 9.82], ["the", 10.08], ["cache.", 10.24]], "B60": [["More", 0.0], ["GPUs", 0.2], ["multiply", 0.56], ["the", 1.18], ["efficiency", 1.42], ["you", 1.76], ["have.", 2.08], ["They", 2.6], ["do", 2.62], ["not", 2.7], ["create", 2.88], ["it.", 3.22], ["A", 3.92], ["job", 4.0], ["at", 4.22], ["20", 4.4], ["%", 4.68], ["on", 4.98], ["one", 5.12], ["card", 5.34], ["becomes", 5.66], ["four", 5.98], ["cards", 6.32], ["at", 6.66], ["20%.", 6.82], ["Add", 7.68], ["cards", 8.06], ["only", 8.42], ["when", 8.72], ["one", 8.94], ["is", 9.12], ["above", 9.22], ["80.", 9.44], ["Under", 10.1], ["60,", 10.26], ["fix", 10.96], ["that", 11.06], ["first.", 11.34], ["A", 12.08], ["job", 12.18], ["limited", 12.42], ["by", 12.8], ["reading", 13.06], ["data", 13.36], ["only", 13.7], ["gets", 13.96], ["worse.", 14.28]], "B61": [["In", 0.0], ["data", 0.16], ["parallel", 0.32], ["training,", 0.7], ["each", 1.32], ["card", 1.48], ["holds", 1.78], ["a", 2.04], ["full", 2.24], ["model", 2.42], ["copy", 2.7], ["and", 3.04], ["takes", 3.36], ["a", 3.54], ["different", 3.74], ["batch.", 3.94], ["They", 4.86], ["then", 4.96], ["average", 5.08], ["their", 5.42], ["gradients", 5.72], ["and", 6.28], ["all", 6.48], ["reduce", 6.62], ["and", 6.92], ["apply", 7.2], ["the", 7.48], ["same", 7.66], ["update.", 7.9], ["Fast", 8.8], ["inside", 8.92], ["a", 9.28], ["node,", 9.5], ["slower", 9.94], ["between", 10.12], ["nodes,", 10.52], ["it", 11.14], ["cannot", 11.24], ["fix", 11.48], ["a", 11.8], ["model", 11.98], ["too", 12.22], ["big", 12.5], ["for", 12.7], ["one", 12.9], ["card.", 13.1]], "B62": [["Check", 0.0], ["your", 0.2], ["code", 0.36], ["is", 0.6], ["written", 0.74], ["for", 0.94], ["it.", 1.26], ["A", 1.7], ["plain", 1.7], ["script", 1.92], ["given", 2.36], ["four", 2.62], ["cards", 2.96], ["uses", 3.32], ["one", 3.58], ["and", 3.98], ["wastes", 4.18], ["three.", 4.4], ["Is", 5.18], ["distributed", 5.38], ["available.", 5.84], ["Has", 6.8], ["the", 6.88], ["process", 7.06], ["group", 7.38], ["been", 7.64], ["initialized?", 7.86], ["And", 8.8], ["does", 8.86], ["the", 9.0], ["device", 9.14], ["count", 9.48], ["match", 9.78], ["what", 10.08], ["you", 10.34], ["requested?", 10.46]], "B63": [["The", 0.0], ["rules", 0.12], ["for", 0.3], ["the", 0.58], ["code,", 0.7], ["launch", 1.18], ["with", 1.32], ["Torch", 1.56], ["run,", 1.82], ["never", 2.28], ["plane", 2.46], ["python,", 2.72], ["use", 3.6], ["distributed", 3.78], ["data", 4.28], ["parallel", 4.62], ["not", 5.06], ["data", 5.34], ["parallel,", 5.64], ["wrap", 6.4], ["after", 6.54], ["moving", 6.86], ["the", 7.08], ["model", 7.3], ["to", 7.52], ["its", 7.8], ["device,", 7.98], ["give", 8.76], ["each", 8.9], ["card", 9.08], ["a", 9.34], ["distributed", 9.48], ["sampler", 9.88], ["and", 10.48], ["call", 10.64], ["set", 10.86], ["epoch", 11.16], ["every", 11.44], ["epoch,", 11.78], ["back", 12.6], ["end", 12.68], ["in", 13.04], ["CCL.", 13.34]], "B64": [["Three", 0.0], ["numbers", 0.22], ["must", 0.4], ["agree.", 0.74], ["The", 1.26], ["count", 1.32], ["ingres,", 1.52], ["tasks", 2.24], ["per", 2.46], ["node,", 2.7], ["and", 3.08], ["torch", 3.18], ["runs", 3.4], ["processes", 3.76], ["per", 4.24], ["node.", 4.56], ["Keep", 5.28], ["one", 5.46], ["node.", 5.68], ["This", 6.28], ["partition,", 6.38], ["multi", 7.18], ["-GPU,", 7.38], ["needs", 8.5], ["an", 8.68], ["approved", 8.84], ["access", 9.14], ["request", 9.62], ["before", 10.08], ["you", 10.42], ["use", 10.6], ["it.", 10.78]], "B65": [["One", 0.0], ["trap", 0.24], ["in", 0.48], ["both", 0.68], ["of", 0.9], ["research", 1.1], ["computing's", 1.4], ["templates.", 2.1], ["A", 2.98], ["comment", 3.12], ["after", 3.4], ["trailing", 3.74], ["backslash", 4.1], ["ends", 4.8], ["the", 5.02], ["line", 5.22], ["there,", 5.44], ["so", 5.92], ["the", 6.04], ["next", 6.18], ["argument", 6.38], ["is", 6.76], ["run", 7.02], ["as", 7.26], ["a", 7.46], ["command.", 7.56], ["Remove", 8.34], ["the", 8.58], ["comment.", 8.82], ["The", 9.56], ["templates", 9.64], ["also", 9.94], ["call", 10.26], ["scripts", 10.62], ["that", 10.96], ["you", 11.26], ["must", 11.4], ["supply", 11.54], ["yourself.", 11.98]], "B66": [["Measure", 0.0], ["the", 0.22], ["scaling.", 0.42], ["Efficiency", 1.22], ["is", 1.28], ["throughput", 1.68], ["divided", 2.04], ["by", 2.48], ["the", 2.78], ["number", 2.9], ["of", 3.02], ["cards", 3.3], ["times", 3.5], ["one", 3.86], ["card's", 4.16], ["throughput.", 4.62], ["Above", 5.4], ["80", 5.56], ["%", 5.88], ["extra", 6.32], ["cards", 6.72], ["pay.", 7.1], ["Below", 7.84], ["70,", 7.94], ["stop", 8.68], ["and", 8.94], ["look", 9.18], ["for", 9.32], ["a", 9.54], ["communication", 9.66], ["or", 10.14], ["reading", 10.6], ["bottleneck.", 10.9], ["The", 11.86], ["material", 11.92], ["says", 12.2], ["nothing", 12.56], ["about", 12.82], ["70", 13.24], ["to", 13.74], ["80.", 13.92]], "B70": [["Every", 0.0], ["bottleneck", 0.28], ["comes", 0.7], ["in", 1.06], ["roughly", 1.26], ["this", 1.44], ["order", 1.78], ["of", 2.0], ["frequency,", 2.16], ["so", 2.74], ["here", 2.84], ["is", 3.06], ["the", 3.18], ["loop.", 3.36], ["Baseline,", 4.14], ["throughput,", 4.64], ["utilization,", 5.2], ["wall", 6.08], ["time,", 6.12], ["profile", 6.78], ["a", 6.96], ["short", 7.2], ["window,", 7.38], ["diagnose,", 8.0], ["fix", 8.68], ["one", 8.78], ["thing", 9.06], ["only", 9.26], ["one,", 9.48], ["re", 10.16], ["-profile,", 10.28], ["record", 10.92], ["the", 11.18], ["gain,", 11.38], ["repeat", 11.9], ["until", 12.1], ["the", 12.4], ["returns", 12.54], ["run", 12.88], ["out.", 13.14]], "B71": [["The", 0.0], ["decision", 0.14], ["guide,", 0.4], ["utilization", 1.16], ["under", 1.46], ["50,", 1.88], ["the", 2.42], ["data", 2.5], ["pipeline", 2.72], ["first", 3.14], ["and", 3.5], ["is", 3.74], ["workers", 3.84], ["still", 4.1], ["0,", 4.44], ["50", 5.26], ["to", 5.42], ["80,", 5.6], ["look", 6.0], ["at", 6.1], ["memory.", 6.24], ["Memory", 7.4], ["under", 7.4], ["50,", 7.6], ["raise", 8.04], ["the", 8.24], ["batch,", 8.4], ["50", 8.84], ["to", 9.04], ["85,", 9.2], ["try", 9.96], ["mixed", 10.04], ["precision,", 10.28], ["over", 10.9], ["90,", 11.04], ["shrink", 11.62], ["the", 11.78], ["batch", 11.98], ["or", 12.22], ["checkpoint.", 12.44], ["Out", 13.3], ["of", 13.42], ["memory,", 13.54], ["smaller", 14.02], ["batch,", 14.3], ["then", 14.84], ["mixed", 14.96], ["precision,", 15.2], ["then", 15.86], ["check", 15.96], ["pointing.", 16.18]], "B72": [["After", 0.0], ["a", 0.24], ["batch", 0.4], ["job", 0.56], ["read", 0.94], ["its", 1.22], ["report,", 1.42], ["GPU", 2.54], ["log", 2.56], ["shows", 2.94], ["utilization", 3.28], ["over", 3.82], ["time", 4.16], ["for", 4.44], ["a", 4.68], ["finished", 4.76], ["job.", 4.96], ["It", 5.74], ["needs", 5.8], ["a", 5.96], ["compute", 6.12], ["node", 6.36], ["so", 6.66], ["we", 6.94], ["have", 7.08], ["not", 7.16], ["run", 7.34], ["it.", 7.56], ["Run", 8.06], ["it", 8.26], ["soon.", 8.42], ["It", 9.0], ["keeps", 9.0], ["about", 9.18], ["seven", 9.46], ["days", 9.84], ["and", 10.16], ["only", 10.46], ["for", 10.66], ["public", 10.9], ["nodes.", 11.2]], "B73": [["Read", 0.0], ["three", 0.18], ["things,", 0.44], ["average", 1.18], ["utilization,", 1.18], ["aim", 2.16], ["above", 2.24], ["70.", 2.46], ["The", 3.4], ["shape", 3.54], ["of", 3.72], ["the", 3.9], ["line,", 4.0], ["flat", 4.54], ["and", 4.58], ["high", 4.74], ["is", 4.94], ["healthy.", 5.08], ["Bouncing", 5.72], ["low", 5.98], ["is", 6.22], ["data", 6.4], ["starvation.", 6.64], ["Flat", 7.66], ["and", 7.72], ["low", 7.86], ["means", 8.04], ["the", 8.3], ["workload", 8.48], ["is", 8.74], ["too", 9.0], ["small", 9.16], ["for", 9.44], ["the", 9.62], ["card.", 9.74], ["And", 10.3], ["average", 10.4], ["VRAM,", 10.74], ["low", 11.8], ["means", 11.92], ["room", 12.22], ["for", 12.46], ["a", 12.68], ["bigger", 12.78], ["batch.", 12.96], ["Under", 13.52], ["60%,", 13.66], ["fix", 14.5], ["it", 14.76], ["before", 14.98], ["the", 15.22], ["next", 15.36], ["submission.", 15.56]], "B74": [["Before", 0.0], ["you", 0.24], ["submit,", 0.38], ["the", 0.78], ["check", 0.94], ["passed", 1.12], ["and", 1.42], ["you", 1.64], ["know", 1.74], ["the", 1.84], ["card", 2.0], ["and", 2.26], ["its", 2.42], ["memory.", 2.56], ["A", 3.22], ["short", 3.34], ["run", 3.54], ["showed", 3.78], ["over", 4.04], ["70%.", 4.26], ["Workers", 5.16], ["set", 5.56], ["pinned", 5.86], ["memory", 6.08], ["on.", 6.38], ["The", 6.92], ["batch", 7.02], ["uses", 7.24], ["half", 7.5], ["the", 7.72], ["memory.", 7.88], ["Precision", 8.86], ["matches", 8.86], ["the", 9.26], ["card.", 9.52], ["The", 10.08], ["request", 10.14], ["names", 10.46], ["the", 10.74], ["type", 10.96], ["with", 11.2], ["4", 11.42], ["CPUs", 11.7], ["or", 12.1], ["more.", 12.4], ["The", 12.9], ["logs", 13.02], ["folder", 13.26], ["exists", 13.64], ["and", 14.06], ["you", 14.44], ["profiled", 14.56], ["20", 15.06], ["-50", 15.36], ["steps.", 15.74]], "B80": [["None", 0.0], ["of", 0.16], ["this", 0.28], ["is", 0.4], ["only", 0.56], ["for", 0.78], ["PyTorch.", 1.02], ["PyTorch", 2.02], ["and", 2.48], ["TensorFlow,", 2.6], ["every", 3.46], ["act", 3.66], ["applies.", 3.92], ["Package", 4.96], ["tools", 5.12], ["like", 5.44], ["hugging", 5.74], ["face,", 5.94], ["verify,", 6.54], ["watch,", 7.02], ["and", 7.44], ["feed", 7.48], ["the", 7.68], ["data", 7.84], ["and", 8.06], ["the", 8.28], ["fixes", 8.38], ["are", 8.6], ["flags.", 8.84], ["Molecular", 9.96], ["dynamics,", 9.96], ["verify", 10.7], ["the", 10.96], ["card", 11.28], ["and", 11.5], ["expect", 11.72], ["trajectory", 12.06], ["writing", 12.52], ["to", 12.98], ["limit", 13.24], ["you.", 13.44], ["Custom", 14.24], ["queue", 14.46], ["to", 14.66], ["add", 14.9], ["insight", 15.14], ["compute.", 15.58]], "B81": [["In", 0.0], ["hugging", 0.14], ["face,", 0.38], ["the", 0.94], ["three", 0.96], ["fixes", 1.16], ["are", 1.48], ["arguments,", 1.78], ["Bf16", 2.66], ["gradient", 3.42], ["check", 3.9], ["pointing", 4.2], ["and", 4.56], ["data", 4.92], ["loader", 5.14], ["workers", 5.4], ["set", 5.94], ["from", 6.4], ["your", 6.6], ["CPU", 6.74], ["count.", 7.1]], "B82": [["Explorer", 0.0], ["and", 0.42], ["AICR", 0.62], ["differ,", 1.24], ["so", 1.68], ["do", 1.8], ["not", 1.92], ["carry", 2.08], ["lines", 2.26], ["between", 2.6], ["them.", 2.94], ["AICR", 3.88], ["is", 4.32], ["Northeastern's", 4.46], ["other", 5.12], ["GPU", 5.32], ["cluster.", 5.7], ["Here", 6.44], ["you", 6.52], ["name", 6.62], ["the", 6.74], ["card", 6.88], ["in", 7.1], ["Gres,", 7.3], ["there", 7.7], ["the", 7.84], ["partition", 7.98], ["fixes", 8.28], ["it.", 8.64], ["Here,", 9.34], ["a", 9.5], ["virtual", 9.56], ["environment", 9.82], ["in", 10.24], ["PIP", 10.54], ["wheels,", 10.72], ["there", 11.32], ["are", 11.44], ["CUDA", 11.6], ["modules", 11.76], ["in", 12.1], ["Conda.", 12.34], ["Here,", 13.02], ["GPU", 13.28], ["logs", 13.62], ["after", 14.0], ["a", 14.34], ["job,", 14.54], ["there", 14.9], ["are", 15.06], ["job", 15.16], ["stats.", 15.36], ["And", 16.08], ["here,", 16.14], ["the", 16.5], ["login", 16.6], ["node", 16.8], ["has", 17.16], ["no", 17.36], ["NVIDIA", 17.58], ["SMI.", 17.94]], "B83": [["Here", 0.0], ["is", 0.18], ["what", 0.32], ["we", 0.44], ["checked", 0.56], ["and", 0.8], ["what", 0.98], ["we", 1.1], ["only", 1.2], ["read.", 1.42], ["We", 2.02], ["ran", 2.04], ["nothing", 2.24], ["on", 2.48], ["a", 2.7], ["GPU", 2.84], ["node.", 3.12], ["Read", 4.02], ["only", 4.14], ["on", 4.38], ["the", 4.6], ["login", 4.72], ["node.", 4.94], ["We", 5.38], ["checked", 5.44], ["the", 5.68], ["partitions", 5.84], ["and", 6.2], ["limits,", 6.46], ["the", 7.04], ["five", 7.08], ["GPU", 7.36], ["types,", 7.74], ["which", 8.3], ["tools", 8.42], ["are", 8.74], ["on", 8.94], ["the", 9.06], ["path,", 9.18], ["and", 9.6], ["the", 9.64], ["Python", 9.74], ["module.", 10.04], ["The", 11.16], ["sessions,", 11.3], ["scripts,", 11.86], ["profilers,", 12.42], ["GPU", 13.16], ["logs,", 13.48], ["and", 14.1], ["the", 14.22], ["numbers", 14.32], ["are", 14.54], ["read", 14.72], ["from", 14.9], ["the", 15.12], ["source.", 15.28]], "B84": [["For", 0.0], ["help,", 0.16], ["write", 0.6], ["to", 0.66], ["RCHelp", 0.88], ["at", 1.52], ["Northeastern", 1.72], [".edu,", 2.28], ["come", 3.62], ["to", 3.76], ["office", 3.94], ["hours,", 4.24], ["or", 5.02], ["book", 5.16], ["a", 5.3], ["consultation", 5.44], ["with", 5.82], ["the", 6.28], ["research", 6.42], ["computing", 6.76], ["team.", 7.2]], "BVDT": [["Let's", 0.0], ["recap", 0.7], ["with", 0.94], ["Claude.", 1.2], ["Verify", 1.92], ["the", 1.96], ["card", 2.32], ["in", 2.48], ["every", 2.64], ["job,", 2.86], ["the", 3.4], ["partition,", 3.42], ["a", 4.0], ["name,", 4.06], ["type,", 4.32], ["and", 4.68], ["a", 4.78], ["tense", 4.84], ["or", 5.0], ["round", 5.2], ["trip.", 5.38], ["Read", 6.1], ["utilization", 6.22], ["and", 6.6], ["memory", 7.0], ["together.", 7.24], ["Under", 7.94], ["50", 8.04], ["%", 8.36], ["is", 8.64], ["a", 8.8], ["problem", 8.94], ["and", 9.16], ["idle", 9.42], ["cards", 9.66], ["are", 9.96], ["cancelled.", 10.14], ["Profile", 11.08], ["a", 11.08], ["short", 11.28], ["window.", 11.46], ["The", 11.94], ["biggest", 11.98], ["row", 12.2], ["says", 12.48], ["where", 12.72], ["to", 12.9], ["look.", 13.06], ["Feed", 13.4], ["the", 13.52], ["card", 13.68], ["first.", 13.88], ["Workers", 14.68], ["pin", 14.68], ["memory,", 15.0], ["prefetch,", 15.48], ["and", 16.04], ["batches.", 16.14], ["Then", 16.9], ["batch", 17.0], ["size,", 17.26], ["the", 17.8], ["right", 17.88], ["precision", 18.06], ["for", 18.42], ["the", 18.68], ["card,", 18.8], ["and", 19.18], ["checkpointing", 19.28], ["last.", 19.82], ["And", 20.5], ["add", 20.58], ["cards", 20.76], ["only", 21.08], ["past", 21.3], ["80%.", 21.58], ["Change", 22.58], ["one", 23.1], ["thing", 23.34], ["at", 23.52], ["a", 23.68], ["time", 23.84], ["and", 24.14], ["read", 24.44], ["GPU", 24.66], ["logs", 25.2], ["after", 25.68], ["every", 26.06], ["job.", 26.38]], "BHTF": [["Your", 0.0], ["turn,", 0.14], ["paste", 0.56], ["this", 0.72], ["into", 0.92], ["Claude.", 1.12], ["Here's", 1.56], ["my", 1.78], ["PyTorch", 1.96], ["training", 2.58], ["loop", 2.8], ["and", 3.08], ["my", 3.26], ["Slurm", 3.42], ["script", 3.72], ["for", 3.94], ["Explorer.", 4.2], ["Paste", 4.8], ["both", 4.92], ["here.", 5.2], ["I", 6.26], ["run", 6.36], ["it", 6.5], ["on", 6.6], ["one", 6.7], ["GPU.", 6.94], ["Walk", 7.66], ["me", 7.8], ["through", 7.94], ["the", 8.12], ["optimization", 8.24], ["loop,", 8.6], ["what", 9.2], ["to", 9.3], ["measure", 9.42], ["for", 9.6], ["a", 9.84], ["50", 9.92], ["-step", 10.14], ["baseline,", 10.34], ["how", 10.94], ["to", 11.06], ["profile", 11.2], ["20", 11.5], ["steps,", 11.84], ["and", 12.28], ["which", 12.36], ["of", 12.48], ["these", 12.62], ["to", 12.7], ["try", 12.88], ["first", 13.1], ["and", 13.36], ["why.", 13.58], ["Data", 14.22], ["loader", 14.34], ["num", 14.52], ["workers", 14.78], ["and", 15.12], ["pin", 15.4], ["memory,", 15.56], ["a", 16.1], ["larger", 16.22], ["batch,", 16.5], ["mixed", 17.06], ["precision,", 17.2], ["gradient", 17.92], ["checkpointing,", 18.14], ["or", 18.98], ["a", 19.1], ["second", 19.26], ["GPU.", 19.44], ["Give", 20.6], ["me", 20.8], ["the", 20.92], ["exact", 21.04], ["code", 21.32], ["changes", 21.68], ["for", 22.02], ["your", 22.36], ["first", 22.52], ["pick", 22.8], ["only.", 23.02], ["Do", 23.74], ["not", 23.84], ["run", 24.04], ["anything", 24.26], ["on", 24.66], ["any", 24.84], ["cluster.", 25.02], ["Then", 25.66], ["check", 25.88], ["two", 26.1], ["things", 26.4], ["yourself.", 26.68], ["Did", 27.14], ["it", 27.6], ["ask", 27.7], ["you", 27.88], ["to", 28.04], ["measure", 28.18], ["before", 28.46], ["it", 28.8], ["changed", 28.94], ["anything,", 29.24], ["and", 30.06], ["did", 30.12], ["it", 30.22], ["change", 30.36], ["exactly", 30.62], ["one", 31.04], ["thing?", 31.42]], "BOUT": [["Optimizing", 0.0], ["GPU", 0.74], ["usage", 1.06], ["on", 1.48], ["Explorer", 1.76], ["at", 2.26], ["Nick", 2.78], ["Baer", 3.04], ["Brown.", 3.34]]}


# ═════════════════════════════ the film's cast (shared by every act) ═════════════════════════════
# One cast, whole film. The same object is the same picture in every beat. (ACTS.md lists it per act.)
#   KEY        key_obj()        a flat kraft key, ink outline, large (the private key)
#   LOCK       padlock()        dark body, ink shackle, ghost keyhole/light (turns terracotta when unlocked); unlock(lock)
#   CERT       cert_page()      a white certificate page: ghost lines, a kraft seal with one terracotta dot
#   AGENT      agent_slab(iso)  one dark slab with a light (the ssh-agent); returns (stack, lights)
#   COMMAND    job_box(iso)     a small kraft box with one terracotta tape (an `ssh` command); label it M("ssh")
#   AICR       aicr_rack(iso)   the large dark rack, 4 slabs (the cluster); returns (stack, lights)
#   LOGIN NODE explorer_rack()  the small dark rack, 2 slabs
#   VAULT      vault(iso)       a dark block with a pale square door (the macOS Keychain)
#   YOU        professor_bear("2x3" | "1x1", ...)  a portrait, never a person icon
#   chip(), plaque()            white pills / cards that carry short labels or real mono text
def key_obj(x=0.0, y=0.0, s=1.0):
    """A flat kraft key lying along +x with its bow centred on (x, y). `.bow`, `.width` (approx)."""
    bow = Circle(radius=0.55 * s, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
    hole = Circle(radius=0.2 * s, fill_color=STAGE, fill_opacity=1, stroke_color=INK, stroke_width=4)
    shaft = Rectangle(width=1.9 * s, height=0.26 * s, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5)
    shaft.move_to([0.5 * s + 0.95 * s, 0, 0])
    teeth = VGroup(*[Rectangle(width=0.22 * s, height=0.4 * s, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5)
                     .move_to([(1.85 + 0.3 * i) * s, -0.3 * s, 0]) for i in range(2)])
    g = VGroup(shaft, teeth, bow, hole)
    g.bow, g.width_units = bow, 2.95 * s
    return g.shift([x, y, 0])


def padlock(x=0.0, y=0.0, s=1.0):
    """A padlock centred on (x, y). `.shackle` rises when unlocked, `.light` turns terracotta."""
    shackle = Arc(radius=0.34 * s, start_angle=0, angle=PI, color=INK, stroke_width=12).move_to([0, 0.45 * s + 0.17 * s, 0])
    body = RoundedRectangle(corner_radius=0.08 * s, width=1.1 * s, height=0.9 * s, fill_color=DARK_TOP, fill_opacity=1,
                            stroke_color=INK, stroke_width=5).move_to([0, 0, 0])
    light = Dot([0, 0.02 * s, 0], radius=0.13 * s, color=GHOST)
    g = VGroup(shackle, body, light)
    g.shackle, g.body, g.light, g.s = shackle, body, light, s
    return g.shift([x, y, 0])


def unlock_anim(lock, rt=0.5):
    """Raise the shackle and turn the light terracotta (an AnimationGroup; play it in one self.play)."""
    return AnimationGroup(lock.shackle.animate.shift(UP * 0.3 * lock.s), lock.light.animate.set_color(TERRA), run_time=rt)


def cert_page(x=0.0, y=0.0, w=1.9, h=2.4):
    """The certificate: white page, three ghost lines, a kraft seal with one terracotta dot. `.card`, `.seal`."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([0.1, -0.1, 0])
    card = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
    lines = VGroup(*[Line([-w / 2 + 0.28, h / 2 - 0.5 - 0.38 * i, 0], [w / 2 - 0.28 - (0.5 if i == 2 else 0), h / 2 - 0.5 - 0.38 * i, 0],
                          color=BAR2, stroke_width=7) for i in range(3)])
    seal = Circle(radius=0.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([w / 2 - 0.55, -h / 2 + 0.55, 0])
    dot = Dot(seal.get_center(), radius=0.09, color=TERRA)
    g = VGroup(shadow, card, lines, seal, dot)
    g.card, g.seal, g.w, g.h = card, seal, w, h
    return g.shift([x, y, 0])


def explorer_rack(iso, x0=0.0, y0=0.0, z0=0.0):
    return iso.server(x0, y0, z0, w=1.3, d=1.3, slab=0.42, n=2)


def aicr_rack(iso, x0=0.0, y0=0.0, z0=0.0):
    return iso.server(x0, y0, z0, w=2.4, d=1.6, slab=0.46, n=4)


def job_box(iso, x0=0.0, y0=0.0, z0=0.0, s=0.7):
    return VGroup(iso.box(x0, y0, z0, s, s, s * 0.8), iso.tape(x0, y0, z0 + s * 0.8, s, s, drop=0.18, t=0.08))


def home_box(iso, x0=0.0, y0=0.0, z0=0.0):
    return iso.box(x0, y0, z0, 1.2, 1.2, 0.9)


def scratch_bin(iso, x0=0.0, y0=0.0, z0=0.0):
    return iso.open_box(x0, y0, z0, 2.8, 1.8, 0.8)


def agent_slab(iso, x0=0.0, y0=0.0, z0=0.0):
    """The ssh-agent: one dark slab with a light (starts ghost; turn it terracotta when the agent holds the key)."""
    return iso.server(x0, y0, z0, w=1.5, d=1.5, slab=0.6, n=1)


def vault(iso, x0=0.0, y0=0.0, z0=0.0):
    """The macOS Keychain: a dark block with a pale square door and a dark handle on its right face."""
    body = iso.box(x0, y0, z0, 1.5, 1.5, 1.2, DARK_TOP, DARK_L, DARK_R)
    door = iso.quad([(x0 + 0.25, y0 - 0.02, z0 + 0.2), (x0 + 1.25, y0 - 0.02, z0 + 0.2),
                     (x0 + 1.25, y0 - 0.02, z0 + 1.0), (x0 + 0.25, y0 - 0.02, z0 + 1.0)], GHOST, stroke=INK, sw=4)
    handle = Dot(iso.p(x0 + 1.0, y0 - 0.03, z0 + 0.6), radius=0.09, color=DARK_L)
    return VGroup(body, door, handle)


def chip(text, x, y, w=None, mono=False, size=34):
    """A white pill with a short label (no outline, so text and outline never fuse)."""
    lab = M(text, size - 2) if mono else T(text, size)
    w = w or (lab.width + 0.8)
    shadow = pill(x + 0.08, y - 0.08, w, h=0.8, fill=BOX_L)
    p = pill(x, y, w, h=0.8)
    lab.move_to([x, y, 0])
    g = VGroup(shadow, p, lab)
    g.pill, g.label = p, lab
    return g

def _logo_path(company, n=1):
    """brutalist.art/icons/logos/<company>/<company>-NN.png (LOGO LAW, Bear 2026-10-12: a company is shown by its logo)."""
    cands = [_os.environ.get("ART_HOME") and _os.path.join(_os.environ["ART_HOME"], "icons", "logos")]
    here = _os.path.dirname(_os.path.abspath(__file__))
    for _ in range(8):
        cands.append(_os.path.join(here, "brutalist.art", "icons", "logos")); here = _os.path.dirname(here)
    cands.append("<books>/brutalist.art/icons/logos")
    for c in cands:
        p = c and _os.path.join(c, company, f"{company}-{n:02d}.png")
        if p and _os.path.exists(p):
            return p
    return None


def logo_chip(company, x, y, h=1.35, n=1):
    """A white pill carrying the company's LOGO (no word). Falls back to a text chip if the logo file is missing.
    Returns a Group (it holds an image): use FadeIn/FadeOut/self.add on it."""
    p = _logo_path(company, n)
    if p is None:
        return chip(company.title(), x, y)
    w = h * 1.35
    shadow = pill(x + 0.08, y - 0.08, w, h=h, fill=BOX_L)
    body = pill(x, y, w, h=h)
    img = ImageMobject(p)
    img.scale_to_fit_height(h * 0.78)
    img.move_to([x, y, 0])
    g = Group(shadow, body, img)
    g.pill = body
    return g


def plaque(text, x, y, w=6.2, h=1.0, size=34):
    """A white card carrying REAL error or command text in mono (no outline)."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
    card = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    lab = M(text, size).move_to([x, y, 0])
    g = VGroup(shadow, card, lab)
    g.card, g.label = card, lab
    return g


# ═════════════════════════════ this film's cast (GPU performance) ═════════════════════════════
# GPU        gpu_card(x, y)        a dark card, ghost light (`lit=True` or `.light.set_color(TERRA)` when busy)
# CPU        cpu_chip(x, y)        a dark chip with kraft pins
# JOB        job2(x, y)            a small kraft box with one terracotta tape
# TANK       tank(cx, yb, yt, w)   the VRAM tank (white fill, open-topped ink U)
# GAUGE      gauge(cx, cy, r, v)   a half-dial with a needle (v in 0..1); terracotta only at a mark you add
# STAMP      stamp(text, x, y)     a kraft pill with a short word
def act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def gpu_card(x, y, w=1.7, h=1.0, lit=False):
    """A GPU: dark card, two pale pin lines on the left, a light on the right (ghost, or terracotta when `lit`)."""
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    pins = VGroup(*[Line([x - w / 2 + 0.28, y + dy, 0], [x + w * 0.1, y + dy, 0], color=BAR1, stroke_width=6) for dy in (0.14, -0.14)])
    light = Dot([x + w / 2 - 0.3, y, 0], radius=0.11, color=TERRA if lit else GHOST)
    g = VGroup(body, pins, light)
    g.body, g.light, g.w, g.h = body, light, w, h
    return g


def cpu_chip(x, y, w=1.5, h=0.9):
    """The processor: a dark chip body with kraft pins on both sides, a light on top-right."""
    body = Rectangle(width=w, height=h, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    pins = VGroup(*[Line([x + s * w / 2, y + dy, 0], [x + s * (w / 2 + 0.26), y + dy, 0], color=KRAFT_DEEP, stroke_width=7)
                    for s in (-1, 1) for dy in (-0.25, 0.0, 0.25)])
    light = Dot([x + w / 2 - 0.25, y + h / 2 - 0.24, 0], radius=0.1, color=GHOST)
    g = VGroup(pins, body, light)
    g.body, g.light = body, light
    return g


def job2(x, y, s=0.8):
    """A small kraft box with one terracotta tape stripe (a job)."""
    box = Rectangle(width=s, height=s * 0.75, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    tape = Rectangle(width=s * 0.2, height=s * 0.75, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    g = VGroup(box, tape)
    g.box = box
    return g


def tank(cx, yb, yt, w):
    """The VRAM tank: a white fill and an open-topped U wall in ink."""
    fill = Rectangle(width=w, height=yt - yb, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([cx, (yt + yb) / 2, 0])
    wall = VMobject(stroke_color=INK, stroke_width=9, fill_opacity=0)
    wall.set_points_as_corners([[cx - w / 2, yt, 0], [cx - w / 2, yb, 0], [cx + w / 2, yb, 0], [cx + w / 2, yt, 0]])
    return VGroup(fill, wall)


def blk(cx, y0, w, h, fill=BAR1, sw=4):
    """A block standing on y0 (its bottom edge), centred on cx; grey fill, ink outline."""
    return Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=sw).move_to([cx, y0 + h / 2, 0])


def gauge(cx, cy, r=1.7, v=0.5, sw=9):
    """A half dial (left = 0, right = 1) with a needle at `v`. `.needle`, `.arc`, `.cx`, `.cy`, `.r`, `.at(v)` gives the arc point."""
    arc = Arc(radius=r, start_angle=0, angle=PI, stroke_color=BAR1, stroke_width=sw).move_arc_center_to([cx, cy, 0])
    ticks = VGroup(*[Line([cx + (r - 0.05) * np.cos(PI - f * PI), cy + (r - 0.05) * np.sin(PI - f * PI), 0],
                          [cx + (r + 0.2) * np.cos(PI - f * PI), cy + (r + 0.2) * np.sin(PI - f * PI), 0], color=INK, stroke_width=6)
                     for f in (0.0, 0.5, 1.0)])
    def pt(f, rr):
        return [cx + rr * np.cos(PI - f * PI), cy + rr * np.sin(PI - f * PI), 0]
    needle = Line([cx, cy, 0], pt(v, r - 0.15), color=INK, stroke_width=8)
    hub = Dot([cx, cy, 0], radius=0.14, color=INK)
    g = VGroup(arc, ticks, needle, hub)
    g.arc, g.needle, g.cx, g.cy, g.r, g.pt = arc, needle, cx, cy, r, pt
    return g


def stamp(text, x, y, w=None, size=32):
    """A kraft pill with a short word, a terracotta dot, ink outline."""
    lab = T(text, size)
    w = w or (lab.width + 0.9)
    sh = pill(x + 0.07, y - 0.07, w, h=0.7, fill=BOX_L)
    body = RoundedRectangle(width=w, height=0.7, corner_radius=0.35, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    dot = Dot([x - w / 2 + 0.3, y, 0], radius=0.08, color=TERRA)
    lab.move_to([x + 0.18, y, 0])
    return VGroup(sh, body, dot, lab)


def ring_around(g, pad=0.14, color=TERRA, sw=6):
    return SurroundingRectangle(g, color=color, buff=pad, stroke_width=sw, corner_radius=0.12)


def dashed_slot(x, y, w, h):
    """A faint dashed outline showing where something will land (keeps the layout visible early)."""
    return DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=min(0.25, h / 2), stroke_color=BAR2, stroke_width=4),
                          num_dashes=36).move_to([x, y, 0])


def lab_l(text, x_left, y, size=34, mono=False):
    """A label whose LEFT edge sits at x_left."""
    t = M(text, size) if mono else T(text, size)
    return t.move_to([x_left + t.width / 2, y, 0])


def lab_c(text, x, y, size=34, mono=False):
    t = M(text, size) if mono else T(text, size)
    return t.move_to([x, y, 0])


# ═════════════════════════════ PART A — Acts I and II (manim beats) ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


class B10_QuietFailures(Scene):
    """A job finishes with a check and no error; three branches show the wrong card, the CPU instead, and a hidden card."""
    def construct(self):
        title = act_title("I · Do You Have The GPU?")
        job = job2(-5.2, 1.9)
        post_l = Line([-3.6, 1.4, 0], [-3.6, 2.5, 0], color=BAR2, stroke_width=10)
        post_r = Line([-2.4, 1.4, 0], [-2.4, 2.5, 0], color=BAR2, stroke_width=10)
        ck = check(-3.0, 1.95, s=0.3, color=TERRA, w=12)
        noerr = lab_l("no error", -1.6, 1.95, 38)
        # column 1: asked for / got
        big = gpu_card(-4.5, -0.3, w=2.0, h=1.2)
        small = gpu_card(-4.5, -1.55, w=1.3, h=0.8, lit=True)
        t_ask = lab_l("asked for", -3.2, -0.3, 32)
        t_got = lab_l("got", -3.2, -1.55, 32)
        c1 = lab_c("wrong card", -3.9, -2.75, 36)
        # column 2: the CPU runs it
        dark = gpu_card(-0.2, -0.3, w=1.7, h=1.0)
        cpu = cpu_chip(-0.2, -1.65)
        jb = job2(-0.2, -1.65, 0.5)
        c2 = lab_c("CPU instead", 0.0, -2.75, 36)
        # column 3: a setting hides the card
        hid = gpu_card(4.0, -0.55, w=1.9, h=1.1)
        sh = chip("shell", 3.6, -1.6, size=34)
        c3 = lab_c("hidden card", 4.0, -2.75, 36)

        self.play(FadeIn(title), FadeIn(job), run_time=0.4)
        hear(self, "Three things", lead=0.0)
        self.play(FadeIn(post_l), FadeIn(post_r), job.animate.move_to([-3.0, 1.9, 0]), run_time=0.7)
        self.play(Create(ck), FadeIn(noerr), run_time=0.4)
        hear(self, "You ask", lead=0.1)
        self.play(FadeIn(big), FadeIn(t_ask), run_time=0.4)
        hear(self, "and get another", lead=0.25)
        self.play(FadeIn(small), FadeIn(t_got), FadeIn(c1), run_time=0.45)
        hear(self, "The software", lead=0.1)
        self.play(FadeIn(dark), run_time=0.3)
        hear(self, "quietly runs", lead=0.15)
        self.play(FadeIn(cpu), FadeIn(c2), run_time=0.35)
        self.play(FadeIn(jb), cpu.light.animate.set_color(TERRA), run_time=0.3)
        hear(self, "Or a setting", lead=0.1)
        self.play(FadeIn(hid), run_time=0.35)
        hear(self, "hides", lead=0.2)
        self.play(FadeIn(sh), hid.animate.set_opacity(0.3), FadeIn(c3), run_time=0.5)
        done(self)


class B11_Partitions(Scene):
    """Five bars on an hours ruler: sharing 1, gpu-short 2, gpu-interactive 2, gpu 8, multigpu 24 (hatched, access request)."""
    def construct(self):
        title = act_title("I · Do You Have The GPU?")
        x0, sc, bh = -2.2, 0.3, 0.55
        ys = [2.0, 1.1, 0.2, -0.7, -1.6]
        names = ["sharing", "gpu-short", "gpu-interactive", "gpu", "multigpu"]
        hours = [1, 2, 2, 8, 24]
        axis = Line([x0, 2.5, 0], [x0, -2.05, 0], color=BAR2, stroke_width=6)
        rl = Line([x0, -2.1, 0], [x0 + 24 * sc, -2.1, 0], color=INK, stroke_width=6)
        rt = VGroup(*[Line([x0 + v * sc, -2.1, 0], [x0 + v * sc, -2.38, 0], color=INK, stroke_width=6) for v in range(0, 25, 4)])
        rn = VGroup(*[T(str(v), 32).move_to([x0 + v * sc, -2.7, 0]) for v in range(0, 25, 4)])
        hrs = T("hours", 34).move_to([x0 - 0.7, -2.7, 0])
        labs = [M(n, 32) for n in names]
        for lb, y in zip(labs, ys):
            lb.move_to([x0 - 0.3 - lb.width / 2, y, 0])
        bars = []
        for i, (h, y) in enumerate(zip(hours, ys)):
            fill = BAR2 if i != 4 else PAGE_TOP
            b = Rectangle(width=h * sc, height=bh, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x0 + h * sc / 2, y, 0])
            bars.append(b)
        hat = hatch(x0, x0 + 24 * sc, ys[4] - bh / 2 + 0.03, ys[4] + bh / 2 - 0.03, gap=0.22)
        multi = VGroup(bars[4], hat)
        tg = [None, lab_l("tests", x0 + 2 * sc + 0.25, ys[1], 32), lab_l("interactive", x0 + 2 * sc + 0.25, ys[2], 32),
              lab_l("training", x0 + 8 * sc + 0.25, ys[3], 32)]
        acc = lab_l("access request", x0 + 24 * sc - 2.45, ys[4] + 0.55, 32)

        self.play(FadeIn(title), Create(axis), Create(rl), FadeIn(rt), FadeIn(rn), FadeIn(hrs), *[FadeIn(l) for l in labs], run_time=0.8)
        hear(self, "GPU Short", lead=0.2)
        self.play(GrowFromEdge(bars[1], LEFT), run_time=0.5)
        hear(self, "Interactive", lead=0.2)
        self.play(GrowFromEdge(bars[2], LEFT), FadeIn(tg[1]), run_time=0.5)
        hear(self, "tests", lead=0.1)
        self.play(FadeIn(tg[2]), run_time=0.3)
        hear(self, "eight", lead=0.55)
        self.play(GrowFromEdge(bars[3], LEFT), run_time=0.8)
        self.play(FadeIn(tg[3]), run_time=0.25)
        hear(self, "Sharing", lead=0.1)
        self.play(GrowFromEdge(bars[0], LEFT), run_time=0.4)
        hear(self, "Multi", lead=0.1)
        self.play(GrowFromEdge(multi, LEFT), run_time=1.2)
        hear(self, "approved", lead=0.2)
        self.play(FadeIn(acc), run_time=0.4)
        done(self)


class B15_MemAndType(Scene):
    """Mem is CPU memory (the RAM block grows, the VRAM tank does not); a bare gpu:1 may land on any card, a named type picks one."""
    def construct(self):
        title = act_title("I · Do You Have The GPU?")
        ram = Rectangle(width=1.5, height=1.0, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-4.9, 0.9, 0])
        ram_t = lab_c("RAM", -4.9, 0.2, 34)
        mem = chip("--mem=32G", -4.9, 2.2, mono=True, size=32)
        card = gpu_card(-2.2, 0.9, w=1.8, h=1.1)
        tk = tank(-2.2, -2.5, -0.55, 1.5)
        fillv = Rectangle(width=1.5, height=0.8, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([-2.2, -2.5 + 0.4 + 0.045, 0])
        vl = lab_c("VRAM", -2.2, -2.95, 34)
        link = Line([-2.2, 0.32, 0], [-2.2, -0.55, 0], color=INK, stroke_width=5)
        oom = chip("out of memory", -4.8, -1.8, size=32)
        # right half
        q1 = chip("gpu:1", 3.2, 2.35, mono=True, size=34)
        cards = [gpu_card(1.4 + 1.85 * i, 0.9, w=1.6, h=1.0) for i in range(3)]
        names = [lab_c(n, 1.4 + 1.85 * i, 0.05, 32) for i, n in enumerate(["V100", "A100", "T4"])]
        arrs = [Arrow([3.2, 1.9, 0], [1.4 + 1.85 * i, 1.5, 0], color=BAR1, stroke_width=6, buff=0.05, max_tip_length_to_length_ratio=0.3) for i in range(3)]
        q2 = chip("gpu:v100-sxm2:1", 3.2, 2.35, mono=True, size=32)
        arr_one = Arrow([2.4, 1.9, 0], [1.4, 1.5, 0], color=INK, stroke_width=8, buff=0.05, max_tip_length_to_length_ratio=0.3)
        ck = check(1.4, -0.85, s=0.28, color=TERRA, w=12)
        pick = lab_l("one card", 2.0, -0.85, 34)

        slots15 = [dashed_slot(3.2, 2.35, 3.6, 0.8)] + [dashed_slot(1.4 + 1.85 * i, 0.9, 1.6, 1.0) for i in range(3)]
        self.play(FadeIn(title), *[FadeIn(s_) for s_ in slots15], run_time=0.4)
        hear(self, "Mem", lead=0.2)
        self.play(FadeIn(ram), FadeIn(ram_t), FadeIn(mem), run_time=0.5)
        hear(self, "The card's own", lead=0.1)
        self.play(FadeIn(card), FadeIn(tk), FadeIn(fillv), FadeIn(vl), Create(link), run_time=0.6)
        hear(self, "raising", lead=0.2)
        self.play(ram.animate.scale(1.45).move_to([-4.9, 1.15, 0]), run_time=0.6)
        hear(self, "out of memory", lead=0.2)
        self.play(FadeIn(oom), run_time=0.3)
        hear(self, "bare", lead=0.2)
        self.remove(*slots15)
        self.play(FadeIn(q1), *[FadeIn(c) for c in cards], *[FadeIn(n) for n in names], run_time=0.5)
        self.play(*[Create(a) for a in arrs], run_time=0.5)
        hear(self, "Name", lead=0.15)
        self.play(FadeOut(q1), *[FadeOut(a) for a in arrs], FadeIn(q2), cards[1].animate.set_opacity(0.3), cards[2].animate.set_opacity(0.3),
                  names[1].animate.set_opacity(0.3), names[2].animate.set_opacity(0.3), run_time=0.5)
        self.play(Create(arr_one), Create(ck), FadeIn(pick), run_time=0.5)
        done(self)


class B19_VisibleDevices(Scene):
    """Three states of CUDA_VISIBLE_DEVICES (0, 0,1, unset) then the verdict: the variable is no proof, the tensor round trip is."""
    def construct(self):
        title = act_title("I · Do You Have The GPU?")
        tag = M("CUDA_VISIBLE_DEVICES", 36).move_to([2.0, 2.4, 0])
        p1 = [gpu_card(-4.3, 0.9, w=1.5, h=0.9, lit=True)]
        p2 = [gpu_card(-0.55, 0.9, w=1.5, h=0.9, lit=True), gpu_card(1.15, 0.9, w=1.5, h=0.9, lit=True)]
        term = RoundedRectangle(width=1.5, height=0.9, corner_radius=0.1, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([4.2, 0.9, 0])
        prompt = M(">_", 34, color="#FFFFFF").move_to([4.2, 0.9, 0])
        l1 = M("0", 48).move_to([-4.3, -0.35, 0])
        l2 = M("0,1", 48).move_to([0.3, -0.35, 0])
        l3 = T("unset", 44).move_to([4.2, -0.35, 0])
        n3 = T("interactive: normal", 34).move_to([4.2, -1.05, 0])
        # verdict row
        cross = x_mark(-4.6, -2.3, r=0.3, w=9)
        proof = T("not proof", 40).move_to([-3.1, -2.3, 0])
        cpu = cpu_chip(0.6, -2.3, w=1.3, h=0.8)
        gpu = gpu_card(3.4, -2.3, w=1.5, h=0.9)
        a1 = Arrow([1.55, -2.1, 0], [2.55, -2.1, 0], color=INK, stroke_width=7, buff=0.0, max_tip_length_to_length_ratio=0.35)
        a2 = Arrow([2.55, -2.55, 0], [1.55, -2.55, 0], color=INK, stroke_width=7, buff=0.0, max_tip_length_to_length_ratio=0.35)
        ck = check(5.1, -2.3, s=0.28, color=TERRA, w=12)
        rt = lab_c("round trip", 2.1, -3.1, 34)

        slots19 = [dashed_slot(4.2, 0.9, 1.5, 0.9), dashed_slot(-2.6, -2.3, 4.4, 0.9), dashed_slot(2.6, -2.3, 4.6, 1.1)]
        self.play(FadeIn(title), FadeIn(tag), *[FadeIn(s_) for s_ in slots19], run_time=0.5)
        hear(self, "Zero is one", lead=0.2)
        self.play(FadeIn(p1[0]), FadeIn(l1), run_time=0.4)
        hear(self, "zero comma", lead=0.2)
        self.play(*[FadeIn(g) for g in p2], FadeIn(l2), run_time=0.4)
        hear(self, "unset", lead=0.3)
        self.remove(slots19[0])
        self.play(FadeIn(term), FadeIn(prompt), FadeIn(l3), FadeIn(n3), run_time=0.5)
        hear(self, "never proof", lead=0.2)
        self.remove(slots19[1])
        self.play(FadeIn(proof), Create(cross), run_time=0.4)
        hear(self, "round trip", lead=0.2)
        self.remove(slots19[2])
        self.play(FadeIn(cpu), FadeIn(gpu), FadeIn(rt), run_time=0.3)
        self.play(Create(a1), Create(a2), run_time=0.4)
        self.play(Create(ck), gpu.light.animate.set_color(TERRA), run_time=0.3)
        done(self)


class B20_TwoNumbers(Scene):
    """Two dials: GPU-Util at 87 (share of the last second, a mark at 50) and Memory at 22 (a tank about a fifth full)."""
    def construct(self):
        title = act_title("II · Seeing The GPU Live")
        smi = logo_chip("nvidia", 0.0, 2.6, h=1.0)
        gl = gauge(-3.6, 0.3, r=1.7, v=0.87)
        gr = gauge(3.6, 0.3, r=1.7, v=0.22)
        glb = T("GPU-Util", 40).move_to([-3.6, 2.45, 0])
        grb = T("Memory", 40).move_to([3.6, 2.45, 0])
        ex1 = T("example", 32, color=INK).move_to([-2.0, -0.7, 0])
        ex2 = T("example", 32, color=INK).move_to([5.2, -0.7, 0])
        gl_empty = gauge(-3.6, 0.3, r=1.7, v=0.0)
        gr_empty = gauge(3.6, 0.3, r=1.7, v=0.0)
        n87 = T("87", 64, bold=True).move_to([-3.6, -0.7, 0])
        n22 = T("22", 64, bold=True).move_to([3.6, -0.7, 0])
        cells = VGroup(*[Rectangle(width=0.34, height=0.5, fill_color=INK if i < 9 else PAGE_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=3)
                         for i in range(10)]).arrange(RIGHT, buff=0.06).move_to([-3.6, -1.7, 0])
        sec = T("last second", 34).move_to([-3.6, -2.5, 0])
        tk = tank(3.6, -2.6, -1.2, 1.4)
        tf = Rectangle(width=1.4, height=0.3, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([3.6, -2.6 + 0.15 + 0.045, 0])
        mk = Dot(gl.pt(0.5, 1.7), radius=0.14, color=TERRA)
        below = T("below 50: wrong", 34).move_to([-3.6 + 0.0, -3.05, 0])

        self.play(FadeIn(title), run_time=0.4)
        hear(self, "NVIDIA", lead=0.1)
        self.play(FadeIn(smi), run_time=0.4)
        hear(self, "two", lead=0.1)
        self.play(FadeIn(gl_empty), FadeIn(gr_empty), FadeIn(glb), FadeIn(grb), run_time=0.5)
        hear(self, "share of the last", lead=0.1)
        self.play(FadeIn(cells), FadeIn(sec), run_time=0.4)
        hear(self, "87", lead=0.25)
        self.play(Transform(gl_empty, gl), FadeIn(n87), FadeIn(ex1), run_time=0.6)
        hear(self, "below", lead=0.1)
        self.play(FadeIn(mk), run_time=0.25)
        hear(self, "wrong", lead=0.2)
        self.play(FadeIn(below), run_time=0.3)
        hear(self, "memory", lead=0.1)
        self.play(Transform(gr_empty, gr), FadeIn(n22), FadeIn(ex2), run_time=0.6)
        hear(self, "fifth", lead=0.15)
        self.play(FadeIn(tk), FadeIn(tf), run_time=0.4)
        done(self)


class B22_TwoAxes(Scene):
    """A 2x2 of utilization against memory; each cell names its reading; the quiz dot (15 / 75) lands top-left."""
    def construct(self):
        title = act_title("II · Seeing The GPU Live")
        gx, gy, cw, ch = -2.5, -2.0, 3.4, 1.9
        cells = {}
        for (i, j) in [(0, 1), (0, 0), (1, 0), (1, 1)]:
            r = Rectangle(width=cw, height=ch, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR2, stroke_width=5)
            r.move_to([gx + cw * (i + 0.5), gy + ch * (j + 0.5), 0])
            cells[(i, j)] = r
        frame = VGroup(*cells.values())
        tags = {(0, 1): "loaded, not fed", (0, 0): "empty card", (1, 0): "raise the batch", (1, 1): "good"}
        tg = {k: T(v, 36).move_to([gx + cw * (k[0] + 0.5), gy + ch * (k[1] + 1) - 0.4, 0]) for k, v in tags.items()}
        xl = T("utilization", 38).move_to([gx + cw, gy - 0.95, 0])
        xlo, xhi = T("low", 32).move_to([gx + cw * 0.5, gy - 0.4, 0]), T("high", 32).move_to([gx + cw * 1.5, gy - 0.4, 0])
        yl = T("memory", 38).move_to([-4.55, gy + 2 * ch + 0.28, 0])
        yhi, ylo = T("high", 32).move_to([-3.2, gy + ch * 1.5, 0]), T("low", 32).move_to([-3.2, gy + ch * 0.5, 0])
        dot = Dot([gx + 0.15 * 2 * cw, gy + 0.75 * 2 * ch, 0], radius=0.17, color=TERRA)
        dlab = M("15% 75%", 30).move_to([gx + 0.15 * 2 * cw + 0.3 + 0.95, gy + 0.75 * 2 * ch, 0])
        ds = T("data starvation", 38).move_to([gx + cw * 0.5, gy + ch * 1 + 0.45, 0])

        self.play(FadeIn(title), FadeIn(frame), FadeIn(xl), FadeIn(xlo), FadeIn(xhi), FadeIn(yl), FadeIn(yhi), FadeIn(ylo), run_time=0.8)
        hear(self, "high memory", lead=0.2)
        self.play(FadeIn(tg[(0, 1)]), run_time=0.35)
        hear(self, "low and low", lead=0.15)
        self.play(FadeIn(tg[(0, 0)]), run_time=0.35)
        hear(self, "high utilization", lead=0.15)
        self.play(FadeIn(tg[(1, 0)]), run_time=0.35)
        hear(self, "high and high", lead=0.15)
        self.play(FadeIn(tg[(1, 1)]), run_time=0.35)
        hear(self, "fifteen", lead=0.2)
        dot.shift(UP * 1.2)
        self.play(FadeIn(dot), run_time=0.15)
        self.play(dot.animate.shift(DOWN * 1.2), FadeIn(dlab), run_time=0.45, rate_func=ease_in)
        hear(self, "data", lead=0.1)
        self.play(FadeIn(ds), run_time=0.35)
        done(self)


class B23_Bands(Scene):
    """Two scales grow left to right: utilization bands (problem, suspect, amber, acceptable, target) and memory bands."""
    def construct(self):
        title = act_title("II · Seeing The GPU Live")
        x0, sc = -5.2, 0.1
        def seg(a, b, y, fill, h=0.5):
            return Rectangle(width=(b - a) * sc - 0.06, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x0 + (a + b) / 2 * sc, y, 0])
        yu, ym = 1.45, -1.25
        ut = lab_l("utilization", -2.6, 2.45, 38)
        nums = VGroup(*[T(str(v), 32).move_to([x0 + v * sc, yu + 0.62, 0]) for v in (0, 50, 60, 70, 80, 100)])
        s1 = [seg(0, 50, yu, BAR1), seg(50, 60, yu, BAR2), seg(60, 70, yu, BAR3), seg(70, 80, yu, GHOST), seg(80, 100, yu, INK)]
        l1 = [lab_c("problem", x0 + 25 * sc, yu - 0.55, 34), lab_c("suspect", x0 + 55 * sc, yu - 1.1, 32), lab_c("amber", x0 + 65 * sc, yu - 0.55, 34),
              lab_c("acceptable", x0 + 75 * sc, yu - 1.1, 32), lab_c("target", x0 + 90 * sc, yu - 0.55, 36)]
        tick = Dot([x0 + 80 * sc, yu + 0.38, 0], radius=0.1, color=TERRA)
        mt = lab_l("memory", -2.6, -0.1, 38)
        mn = VGroup(*[T(str(v), 32).move_to([x0 + v * sc, ym + 0.62, 0]) for v in (0, 40, 60, 90, 100)])
        m_room = seg(0, 40, ym, BAR2)
        m_health = seg(60, 90, ym, BAR1)
        m_empty = [dashed_slot(x0 + 50 * sc, ym, 2.0 - 0.06, 0.5), dashed_slot(x0 + 95 * sc, ym, 1.0 - 0.06, 0.5)]
        lm = [lab_c("room for a bigger batch", x0 + 20 * sc, ym - 0.65, 32), lab_c("healthy", x0 + 75 * sc, ym - 0.65, 36)]

        slots23 = [dashed_slot(x0 + 75 * sc, yu, 1.0 - 0.06, 0.5), dashed_slot(x0 + 90 * sc, yu, 2.0 - 0.06, 0.5), dashed_slot(x0 + 20 * sc, ym, 4.0 - 0.06, 0.5), dashed_slot(x0 + 75 * sc, ym, 3.0 - 0.06, 0.5)]
        self.play(FadeIn(title), FadeIn(ut), FadeIn(nums), FadeIn(mt), FadeIn(mn), *[FadeIn(s_) for s_ in slots23], run_time=0.6)
        hear(self, "under 50", lead=0.2)
        self.play(GrowFromEdge(s1[0], LEFT), FadeIn(l1[0]), run_time=0.7)
        hear(self, "Under 60", lead=0.2)
        self.play(GrowFromEdge(s1[1], LEFT), FadeIn(l1[1]), run_time=0.5)
        hear(self, "60 to 70", lead=0.2)
        self.play(GrowFromEdge(s1[2], LEFT), FadeIn(l1[2]), run_time=0.5)
        hear(self, "70 acceptable", lead=0.1)
        self.remove(slots23[0])
        self.play(GrowFromEdge(s1[3], LEFT), FadeIn(l1[3]), run_time=0.5)
        hear(self, "80 to 100", lead=0.2)
        self.remove(slots23[1])
        self.play(GrowFromEdge(s1[4], LEFT), FadeIn(l1[4]), FadeIn(tick), run_time=0.6)
        hear(self, "memory", lead=0.1)
        self.play(*[FadeIn(d) for d in m_empty], run_time=0.5)
        hear(self, "60 to 90", lead=0.2)
        self.remove(slots23[3])
        self.play(GrowFromEdge(m_health, LEFT), FadeIn(lm[1]), run_time=0.6)
        hear(self, "Under 40", lead=0.15)
        self.remove(slots23[2])
        self.play(GrowFromEdge(m_room, LEFT), FadeIn(lm[0]), run_time=0.7)
        done(self)


class B24_IdleBot(Scene):
    """A utilization line sinks to a flat low stretch; Idle Bot sweeps it; an email at 15 min; the job is cancelled at 1 h."""
    def construct(self):
        title = act_title("II · Seeing The GPU Live")
        ax = Line([-5.6, -2.2, 0], [4.9, -2.2, 0], color=INK, stroke_width=6)
        ay = Line([-5.6, -2.2, 0], [-5.6, 1.5, 0], color=BAR2, stroke_width=6)
        tl = T("time", 34).move_to([5.45, -2.2, 0])
        ul = T("GPU use", 34).move_to([-4.7, 1.8, 0])
        pts = [[-5.6, 0.6, 0], [-5.3, 0.9, 0], [-5.0, 0.4, 0], [-4.7, 1.0, 0], [-4.4, 0.5, 0], [-4.1, 0.95, 0], [-3.8, 0.45, 0], [-3.5, 0.8, 0],
               [-3.2, -0.3, 0], [-3.0, -1.7, 0], [4.8, -1.7, 0]]
        line = VMobject(stroke_color=INK, stroke_width=8)
        line.set_points_as_corners(pts)
        t15 = Line([-1.9, -2.2, 0], [-1.9, -2.45, 0], color=INK, stroke_width=6)
        t60 = Line([1.4, -2.2, 0], [1.4, -2.45, 0], color=INK, stroke_width=6)
        l15 = T("15 min", 34).move_to([-1.9, -2.85, 0])
        l60 = T("1 h", 34).move_to([1.4, -2.85, 0])
        bot = VGroup(Circle(radius=0.32, stroke_color=INK, stroke_width=7, fill_color=PAGE_TOP, fill_opacity=1),
                     Line([0.23, -0.23, 0], [0.62, -0.62, 0], color=INK, stroke_width=9)).move_to([-3.0, -0.4, 0])
        botl = T("Idle Bot", 36).move_to([-1.2, 0.5, 0])
        env = VGroup(Rectangle(width=1.0, height=0.68, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5),
                     Line([-0.5, 0.34, 0], [0, -0.05, 0], color=INK, stroke_width=4), Line([0.5, 0.34, 0], [0, -0.05, 0], color=INK, stroke_width=4)).move_to([-1.9, -1.1, 0])
        job = job2(1.4, -1.1, 0.9)
        xm = x_mark(1.4, -1.1, r=0.4, w=10)
        npp = T("no published percentage", 36).move_to([3.1, 2.4, 0])
        card = gpu_card(-2.0, 2.4, w=1.5, h=0.9)
        held = T("holds the card", 34).move_to([-2.0, 1.65, 0])

        self.play(FadeIn(title), Create(ax), Create(ay), FadeIn(tl), FadeIn(ul), run_time=0.6)
        hear(self, "idle cards", lead=0.9)
        self.play(Create(line), run_time=1.4, rate_func=linear)
        hear(self, "idlebot", lead=0.2)
        self.play(FadeIn(bot), FadeIn(botl), Create(t15), Create(t60), FadeIn(l15), FadeIn(l60), run_time=0.5)
        self.play(bot.animate.shift(RIGHT * 4.4), botl.animate.shift(RIGHT * 4.4), run_time=1.6, rate_func=linear)
        hear(self, "15", lead=0.35)
        self.play(FadeIn(env), run_time=0.35)
        hear(self, "hour", lead=0.35)
        self.play(FadeIn(job), run_time=0.2)
        self.play(Create(xm), run_time=0.3)
        hear(self, "no published", lead=0.15)
        self.play(FadeIn(npp), run_time=0.4)
        hear(self, "stalled", lead=0.1)
        self.play(FadeIn(card), FadeIn(held), run_time=0.4)
        done(self)


def hatch(xa, xb, ya, yb, gap=0.2, color=BAR1, sw=3.5):
    """Diagonal hatch lines clipped to the rectangle [xa, xb] x [ya, yb]."""
    w, h = xb - xa, yb - ya
    lines = VGroup()
    c = -h
    while c < w:
        xs, xe = xa + max(0.0, c), xa + min(w, c + h)
        if xe - xs > 0.02:
            lines.add(Line([xs, ya + (xs - xa - c), 0], [xe, ya + (xe - xa - c), 0], color=color, stroke_width=sw))
        c += gap
    return lines


# ═════════════════════════════ PART B — Acts III and IV (manim beats) ═════════════════════════════


class B30_FourLayers(Scene):
    """A four-rung ladder, lightest first: live tools, framework profiler, timeline, one kernel; the first two are ringed as 'most problems'."""
    def construct(self):
        title = act_title("III · The Profiling Toolchain")
        rows = []
        spec = [("live", "nvidia", ["nvidia-smi", "nvitop"], -2.2), ("framework", "pytorch", ["torch.profiler"], -0.8),
                ("timeline", "nvidia", ["nsys"], 0.6), ("one kernel", "nvidia", ["ncu"], 2.0)]
        for name, logo, monos, y in spec:
            lab = lab_l(name, -5.9, y, 38)
            lg = logo_chip(logo, -1.9, y, h=0.9)
            ms = Group(*[chip(m, 1.4 + 3.0 * i if len(monos) > 1 else 1.6, y, mono=True, size=32) for i, m in enumerate(monos)])
            rows.append(Group(lab, lg, ms))
        rail = Line([-6.1, -2.7, 0], [-6.1, 2.5, 0], color=BAR2, stroke_width=6)
        rare = T("rarely", 38).move_to([5.4, 1.3, 0])
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "lightest", lead=0.3)
        self.play(Create(rail), run_time=0.4)
        hear(self, "live tools", lead=0.2)
        self.play(FadeIn(rows[0]), run_time=0.5)
        hear(self, "framework", lead=0.2)
        self.play(FadeIn(rows[1]), run_time=0.5)
        hear(self, "insight systems", lead=0.3)
        self.play(FadeIn(rows[2]), run_time=0.5)
        hear(self, "one kernel", lead=0.5)
        self.play(FadeIn(rows[3]), run_time=0.5)
        self.play(rows[2].animate.set_opacity(0.45), rows[3].animate.set_opacity(0.45), FadeIn(rare), run_time=0.4)
        hear(self, "layer two", lead=0.4)
        r = ring_around(Group(rows[0], rows[1]), pad=0.2)
        self.play(Create(r), run_time=0.5)
        done(self)


class B33_ReadTheTable(Scene):
    """A profiler table drawn as CPU/CUDA bar pairs; the four things to read land in order (example, not our run)."""
    def construct(self):
        title = act_title("III · The Profiling Toolchain")
        x0 = -1.0
        names = ["DataLoader.__next__", "aten::conv2d", "aten::batch_norm", "aten::copy_"]
        cpu = [1.843, 0.041, 0.019, 0.017]
        cuda = [0.0, 0.394, 0.087, 0.052]
        ys = [0.95, 0.0, -0.95, -1.9]
        sc = 2.4
        rows, cb, gb = [], [], []
        for n, c, g, y in zip(names, cpu, cuda, ys):
            lab = M(n, 30)
            lab.move_to([x0 - 0.35 - lab.width / 2, y, 0])
            b1 = Rectangle(width=max(c * sc, 0.06), height=0.3, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x0 + max(c * sc, 0.06) / 2, y + 0.19, 0])
            b2 = Rectangle(width=max(g * sc, 0.06), height=0.3, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x0 + max(g * sc, 0.06) / 2, y - 0.19, 0])
            rows.append(lab); cb.append(b1); gb.append(b2)
        table = Group(*rows, *cb, *gb)
        leg1 = Rectangle(width=0.5, height=0.3, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([2.2, 2.55, 0])
        lg1 = lab_l("CPU total", 2.55, 2.55, 32)
        leg2 = Rectangle(width=0.5, height=0.3, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([2.2, 2.05, 0])
        lg2 = lab_l("CUDA total", 2.55, 2.05, 32)
        n1 = M("1.843 s", 32).move_to([x0 + 1.843 * sc + 0.2 + 0.85, ys[0] + 0.19, 0])
        n2 = M("0.000 s", 32).move_to([x0 + 0.06 + 0.2 + 0.85, ys[0] - 0.19, 0])
        # strip showing gaps
        bursts = VGroup(*[Rectangle(width=0.35, height=0.32, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([-5.7 + 1.1 * i, 2.35, 0]) for i in range(4)])
        sl_ = lab_l("GPU", -6.2, 1.8, 32)
        ex = T("example, not our run", 34).move_to([3.6, -2.9, 0])

        self.play(FadeIn(title), FadeIn(table), FadeIn(leg1), FadeIn(lg1), FadeIn(leg2), FadeIn(lg2), FadeIn(n1), FadeIn(n2), run_time=0.8)
        hear(self, "gaps", lead=0.2)
        self.play(FadeIn(bursts), FadeIn(sl_), run_time=0.5)
        hear(self, "Large copy", lead=0.15)
        rc = ring_around(Group(rows[3], cb[3], gb[3]), pad=0.12)
        self.play(Create(rc), run_time=0.4)
        self.wait(0.9)
        self.play(FadeOut(rc), run_time=0.3)
        hear(self, "CPU time far", lead=0.1)
        self.play(cb[0].animate.set_fill(INK, opacity=0.35), run_time=0.35)
        self.play(cb[0].animate.set_fill(BAR2, opacity=1), run_time=0.3)
        hear(self, "data loader at", lead=0.2)
        rl_ = ring_around(Group(rows[0], cb[0], gb[0], n1), pad=0.12)
        self.play(Create(rl_), run_time=0.4)
        hear(self, "This example", lead=0.2)
        self.play(FadeIn(ex), run_time=0.4)
        done(self)


class B35_TimelinePatterns(Scene):
    """A timeline: GPU bursts with long gaps, file reads filling the gaps, then scattered copies that pinned memory pulls together."""
    def construct(self):
        title = act_title("III · The Profiling Toolchain")
        gl = lab_l("GPU", -6.2, 1.6, 36)
        cl = lab_l("CPU", -6.2, 0.35, 36)
        ml = lab_l("copies", -6.2, -1.0, 36)
        xs = [-3.9, -1.4, 1.1, 3.6]
        bursts = [Rectangle(width=0.5, height=0.5, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x, 1.6, 0]) for x in xs]
        base = Line([-4.4, 1.15, 0], [4.4, 1.15, 0], color=BAR2, stroke_width=5)
        reads = [chip("read()", x + 1.25, 0.35, w=1.95, mono=True, size=30) for x in xs[:3]]
        t15 = T("15 ms", 32).move_to([xs[0], 2.35, 0])
        t50 = T("50 ms", 32).move_to([xs[0] + 1.25, 2.35, 0])
        ex = T("example", 32).move_to([5.3, 1.6, 0])
        tick_x = [-4.6, -3.2, -2.0, -0.6, 0.7, 2.3, 3.8]
        ticks = [Rectangle(width=0.16, height=0.5, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=2).move_to([x, -1.0, 0]) for x in tick_x]
        pin = chip("pinned memory", 0.0, -2.35, size=34)
        near = [xs[0], xs[0] + 0.3, xs[1], xs[1] + 0.3, xs[2], xs[2] + 0.3, xs[3]]

        slots35 = [dashed_slot(x + 1.25, 0.35, 1.95, 0.8) for x in xs[:3]] + [dashed_slot(0.0, -1.0, 9.0, 0.7)]
        self.play(FadeIn(title), FadeIn(cl), FadeIn(ml), *[FadeIn(s_) for s_ in slots35], run_time=0.4)
        hear(self, "empty GPU", lead=0.2)
        self.play(FadeIn(gl), Create(base), run_time=0.4)
        hear(self, "short bursts", lead=0.2)
        self.play(LaggedStart(*[FadeIn(b) for b in bursts], lag_ratio=0.25), run_time=0.9)
        self.play(FadeIn(t15), FadeIn(t50), FadeIn(ex), run_time=0.3)
        hear(self, "File reads", lead=0.1)
        self.remove(*slots35[:3])
        self.play(*[FadeIn(r) for r in reads], run_time=0.6)
        hear(self, "Copies", lead=0.1)
        self.remove(slots35[3])
        self.play(LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.1), run_time=0.9)
        hear(self, "Pin the memory", lead=0.1)
        self.play(FadeIn(pin), *[t.animate.move_to([nx, -1.0, 0]) for t, nx in zip(ticks, near)], run_time=0.9)
        done(self)


class B40_Deliveries(Scene):
    """A truck crawls to a fast GPU; under it two time bars: GPU computes 25 ms, then waits 35 ms of a 60 ms loader."""
    def construct(self):
        title = act_title("IV · Data Starvation")
        belt = Rectangle(width=8.6, height=0.22, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([-1.3, 1.45, 0])
        truck = job2(-5.2, 1.95, 0.9)
        gpu = gpu_card(4.3, 1.75, w=1.7, h=1.0)
        idle = T("58% idle", 54, bold=True).move_to([4.3, 2.9, 0])
        x0 = -2.8
        lab_g = lab_l("GPU", x0 - 1.7, -1.7, 38)
        lab_l_ = lab_l("loader", x0 - 1.7, -0.6, 38)
        loader = Rectangle(width=6.0, height=0.55, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x0 + 3.0, -0.6, 0])
        work = Rectangle(width=2.5, height=0.55, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x0 + 1.25, -1.7, 0])
        wait = Rectangle(width=3.5, height=0.55, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x0 + 2.5 + 1.75, -1.7, 0])
        wait_h = hatch(x0 + 2.5, x0 + 6.0, -1.7 - 0.275 + 0.03, -1.7 + 0.275 - 0.03, gap=0.22)
        waitg = VGroup(wait, wait_h)
        k1 = T("25 ms", 36).move_to([x0 + 1.25, -2.35, 0])
        k2 = T("35 ms idle", 36).move_to([x0 + 4.25, -2.35, 0])
        k3 = T("60 ms", 36).move_to([x0 + 6.0 + 0.9, -0.6, 0])
        ex = T("example", 32).move_to([5.3, -1.7, 0])

        self.play(FadeIn(title), FadeIn(belt), FadeIn(gpu), run_time=0.5)
        hear(self, "fast cook", lead=0.3)
        self.play(FadeIn(truck), run_time=0.2)
        self.play(truck.animate.move_to([2.6, 1.95, 0]), run_time=3.2, rate_func=linear)
        hear(self, "25", lead=0.3)
        self.play(FadeIn(lab_g), GrowFromEdge(work, LEFT), FadeIn(k1), FadeIn(ex), run_time=0.7)
        hear(self, "60", lead=0.6)
        self.play(FadeIn(lab_l_), GrowFromEdge(loader, LEFT), FadeIn(k3), run_time=0.8)
        hear(self, "idles", lead=0.1)
        self.play(GrowFromEdge(waitg, LEFT), FadeIn(k2), run_time=0.7)
        hear(self, "of every", lead=0.3)
        self.play(FadeIn(idle), run_time=0.4)
        done(self)


class B44_StartingValues(Scene):
    """Four setting names, each with its starting value, then cpus-per-task = workers + 1 (at least 4)."""
    def construct(self):
        title = act_title("IV · Data Starvation")
        spec = [("num_workers", "CPUs minus one"), ("pin_memory", "always on"), ("persistent_workers", "on if workers > 0"), ("prefetch_factor", "2")]
        ys = [2.0, 1.0, 0.0, -1.0]
        rows = []
        for (n, v), y in zip(spec, ys):
            a = chip(n, -3.3, y, w=4.9, mono=True, size=32)
            ar = Arrow([-0.6, y, 0], [0.5, y, 0], color=INK, stroke_width=7, buff=0, max_tip_length_to_length_ratio=0.4)
            b = chip(v, 3.1, y, w=4.2, size=36)
            rows.append(Group(a, ar, b))
        e1 = chip("--cpus-per-task", -3.7, -2.35, w=4.3, mono=True, size=30)
        eq = T("=", 50).move_to([-1.2, -2.35, 0])
        e2 = chip("num_workers", 1.0, -2.35, w=3.5, mono=True, size=30)
        pl = T("+", 50).move_to([2.95, -2.35, 0])
        e3 = chip("1", 3.9, -2.35, w=1.0, size=40)
        least = T("at least 4", 38).move_to([-3.7, -3.1, 0])
        dots = VGroup(*[Dot([4.7 + 0.0, -2.35, 0])])

        slots44 = [dashed_slot(-3.3, ys[2], 4.9, 0.8), dashed_slot(3.1, ys[2], 4.2, 0.8), dashed_slot(-3.3, ys[3], 4.9, 0.8), dashed_slot(3.1, ys[3], 4.2, 0.8), dashed_slot(-0.5, -2.35, 10.0, 0.9)]
        self.play(FadeIn(title), *[FadeIn(s_) for s_ in slots44], run_time=0.4)
        hear(self, "workers", lead=0.2)
        self.play(FadeIn(rows[0]), run_time=0.45)
        hear(self, "Pin memory", lead=0.1)
        self.play(FadeIn(rows[1]), run_time=0.45)
        hear(self, "Persistent", lead=0.1)
        self.remove(slots44[0], slots44[1])
        self.play(FadeIn(rows[2]), run_time=0.45)
        hear(self, "Prefetch", lead=0.1)
        self.remove(slots44[2], slots44[3])
        self.play(FadeIn(rows[3]), run_time=0.45)
        hear(self, "equal", lead=0.9)
        self.remove(slots44[4])
        self.play(FadeIn(e1), FadeIn(eq), run_time=0.4)
        hear(self, "workers plus", lead=0.2)
        self.play(FadeIn(e2), FadeIn(pl), FadeIn(e3), run_time=0.5)
        hear(self, "at least", lead=0.1)
        self.play(FadeIn(least), run_time=0.4)
        done(self)


class B47_WhereDataLives(Scene):
    """Home, scratch and projects are all network filesystems; data goes in scratch or projects as a few large files, never home."""
    def construct(self):
        title = act_title("IV · Data Starvation")
        xs = [-2.4, 1.3, 4.8]
        names = ["/home", "/scratch", "/projects"]
        boxes = [Rectangle(width=2.2, height=1.3, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, 1.2, 0]) for x in xs]
        labs = [M(n, 36).move_to([x, 2.3, 0]) for n, x in zip(names, xs)]
        br = Line([-3.5, -0.55, 0], [6.1, -0.55, 0], color=INK, stroke_width=6)
        brl = T("network filesystems", 38).move_to([1.3, -0.95, 0])
        ck1 = check(1.2, 1.2, s=0.26, color=TERRA, w=11)
        ck2 = check(4.7, 1.2, s=0.26, color=TERRA, w=11)
        cr = x_mark(-2.4, 1.2, r=0.28, w=9)
        big = VGroup(*[Rectangle(width=1.5, height=0.42, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.2, -1.5 - 0.5 * i, 0]) for i in range(3)])
        bigl = T("a few large files", 36).move_to([3.2, -3.15, 0])
        bck = check(5.3, -2.15, s=0.26, color=TERRA, w=11)
        rng = np.random.RandomState(4)
        smalls = VGroup(*[Square(side_length=0.1, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-3.2 + rng.uniform(-1.4, 1.4), -2.2 + rng.uniform(-0.7, 0.7), 0]) for _ in range(70)])
        smalll = T("millions of small ones", 36).move_to([-3.2, -3.15, 0])
        scr = x_mark(-3.2, -1.85, r=0.0001, w=1)
        pg = chip("purged", 1.3, 0.05, size=32)

        self.play(FadeIn(title), run_time=0.4)
        hear(self, "Home", lead=0.1)
        self.play(FadeIn(boxes[0]), FadeIn(labs[0]), run_time=0.35)
        hear(self, "Scratch", lead=0.1)
        self.play(FadeIn(boxes[1]), FadeIn(labs[1]), run_time=0.35)
        hear(self, "Projects", lead=0.1)
        self.play(FadeIn(boxes[2]), FadeIn(labs[2]), run_time=0.35)
        hear(self, "network", lead=0.2)
        self.play(Create(br), FadeIn(brl), run_time=0.5)
        hear(self, "Keep data", lead=0.1)
        self.play(Create(ck1), Create(ck2), run_time=0.35)
        hear(self, "packed", lead=0.55)
        self.play(LaggedStart(*[FadeIn(b) for b in big], lag_ratio=0.2), FadeIn(bigl), run_time=0.6)
        self.play(Create(bck), run_time=0.25)
        hear(self, "millions", lead=0.2)
        self.play(FadeIn(smalls), FadeIn(smalll), run_time=0.5)
        hear(self, "never in Home", lead=0.15)
        self.play(Create(cr), run_time=0.3)
        hear(self, "purged", lead=0.2)
        self.play(FadeIn(pg), run_time=0.3)
        done(self)


class B48_Illustration(Scene):
    """Three bars (18, 55, 82 percent) with images per second, labelled as the source's illustration, not our run."""
    def construct(self):
        title = act_title("IV · Data Starvation")
        xs = [-4.2, 0.0, 4.2]
        vals = [18, 55, 82]
        base = -1.45
        sc = 0.034
        bars = [Rectangle(width=1.5, height=v * sc, fill_color=BAR2 if i < 2 else INK, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, base + v * sc / 2, 0])
                for i, (x, v) in enumerate(zip(xs, vals))]
        nums = [T(f"{v}%", 52, bold=True).move_to([x, base + v * sc + 0.5, 0]) for x, v in zip(xs, vals)]
        axis = Line([-6.0, base, 0], [6.0, base, 0], color=INK, stroke_width=6)
        cfg = [T(t, 34).move_to([x, base - 0.5, 0]) for x, t in zip(xs, ["no workers", "8 workers, pinned", "plus pre-fetch"])]
        ips = [M(t, 32).move_to([x, base - 1.15, 0]) for x, t in zip(xs, ["~420 img/s", "~1,300 img/s", "~1,950 img/s"])]
        tag = T("illustration from the source, not our run", 34).move_to([1.6, 3.0, 0])
        st = stamp("no script produces these", -3.2, 1.3, w=4.6, size=32)

        self.play(FadeIn(title), Create(axis), FadeIn(tag), run_time=0.6)
        hear(self, "no workers", lead=0.2)
        self.play(FadeIn(cfg[0]), GrowFromEdge(bars[0], DOWN), run_time=0.7)
        self.play(FadeIn(nums[0]), FadeIn(ips[0]), run_time=0.3)
        hear(self, "8 workers", lead=0.2)
        self.play(FadeIn(cfg[1]), GrowFromEdge(bars[1], DOWN), run_time=0.8)
        self.play(FadeIn(nums[1]), FadeIn(ips[1]), run_time=0.3)
        hear(self, "prefetching", lead=0.3)
        self.play(FadeIn(cfg[2]), GrowFromEdge(bars[2], DOWN), run_time=0.8)
        self.play(FadeIn(nums[2]), FadeIn(ips[2]), run_time=0.3)
        hear(self, "no script", lead=0.2)
        self.play(FadeIn(st), run_time=0.4)
        done(self)


# ═════════════════════════════ PART C — Acts V and VI (manim beats) ═════════════════════════════


class B50_BatchDoubles(Scene):
    """A batch block in the VRAM tank doubles (20, 40 percent), throughput arrows double, the ceiling and the optimizer's margin."""
    def construct(self):
        title = act_title("V · Memory And Precision")
        yb, yt, tw, cx = -2.7, 1.7, 2.4, -2.6
        H = yt - yb
        tk = tank(cx, yb, yt, tw)
        vl = lab_c("VRAM", cx, -3.15, 34)
        def blkh(f, fill=BAR2):
            return blk(cx, yb + 0.05, 1.9, H * f, fill)
        b1, b2, b3 = blkh(0.2), blkh(0.4), blkh(0.7)
        p1 = lab_l("20%", cx + 1.45, yb + H * 0.1, 36)
        p2 = lab_l("40%", cx + 1.45, yb + H * 0.2, 36)
        a1 = Arrow([0.8, -1.9, 0], [2.0, -1.9, 0], color=INK, stroke_width=9, buff=0, max_tip_length_to_length_ratio=0.35)
        a2 = Arrow([0.8, -0.8, 0], [3.2, -0.8, 0], color=INK, stroke_width=9, buff=0, max_tip_length_to_length_ratio=0.35)
        th = lab_l("throughput", 0.8, -0.1, 36)
        ceil_y = yb + H * 0.88
        ceil = DashedLine([cx - 1.5, ceil_y, 0], [cx + 1.5, ceil_y, 0], color=INK, stroke_width=5)
        cl = lab_l("largest that fits", cx + 1.65, ceil_y, 34)
        opt = blk(cx, yb + H * 0.7 + 0.05, 1.9, 0.5, BAR3)
        opl = lab_l("optimizer", cx + 1.45, yb + H * 0.7 + 0.35, 34)
        self.play(FadeIn(title), FadeIn(tk), FadeIn(vl), run_time=0.5)
        hear(self, "Doubling", lead=0.5)
        self.play(FadeIn(b1), FadeIn(p1), Create(a1), FadeIn(th), run_time=0.5)
        hear(self, "doubles", lead=0.1)
        self.play(Transform(b1, b2), Transform(p1, p2), Create(a2), run_time=0.7)
        hear(self, "saturated", lead=0.6)
        self.play(Create(ceil), FadeIn(cl), run_time=0.5)
        hear(self, "20", lead=0.2)
        self.play(Transform(b1, blkh(0.2)), Transform(p1, lab_l("20%", cx + 1.45, yb + H * 0.1, 36)), run_time=0.5)
        hear(self, "double the batch", lead=0.1)
        self.play(Transform(b1, b2), Transform(p1, p2), run_time=0.6)
        hear(self, "Stop short", lead=0.1)
        self.play(Transform(b1, b3), FadeOut(p1), run_time=0.7)
        hear(self, "optimizer", lead=0.2)
        self.play(FadeIn(opt), FadeIn(opl), run_time=0.4)
        done(self)


class B53_BitSplit(Scene):
    """Bit cells: FP32 (1, 8, 23), BF16 (1, 8, 7), FP16 (1, 5, 10); BF16 on A100 and newer, FP16 on V100 and T4 with a scaler."""
    def construct(self):
        title = act_title("V · Memory And Precision")
        x0, cwid = -4.3, 0.19
        def row(y, name, parts):
            cells = VGroup()
            x = x0
            for n, fill in parts:
                for _ in range(n):
                    cells.add(Rectangle(width=cwid - 0.03, height=0.5, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x + cwid / 2, y, 0]))
                    x += cwid
            lab = M(name, 34)
            lab.move_to([x0 - 0.35 - lab.width / 2, y, 0])
            return Group(cells, lab)
        r32 = row(1.5, "FP32", [(1, BAR3), (8, INK), (23, BAR2)])
        r16b = row(0.2, "BF16", [(1, BAR3), (8, INK), (7, BAR2)])
        r16f = row(-1.1, "FP16", [(1, BAR3), (5, INK), (10, BAR2)])
        rng = T("range", 34).move_to([x0 + cwid * 5.5, 2.2, 0])
        prc = T("precision", 34).move_to([x0 + cwid * 21, 2.2, 0])
        c_bf = chip("A100 and newer", 1.2, 0.2, size=32)
        c_ns = chip("no loss scaler", 4.6, 0.2, size=32)
        c_v = chip("V100", 0.5, -1.1, size=32)
        c_t = chip("T4", 2.1, -1.1, size=32)
        c_gs = chip("GradScaler", 4.6, -1.1, mono=True, size=30)

        self.play(FadeIn(title), run_time=0.4)
        hear(self, "splits", lead=0.3)
        self.play(FadeIn(r32), FadeIn(rng), FadeIn(prc), run_time=0.7)
        hear(self, "Bf16", lead=0.2)
        self.play(FadeIn(r16b), run_time=0.5)
        hear(self, "no loss", lead=0.15)
        self.play(FadeIn(c_ns), run_time=0.35)
        hear(self, "Fp16", lead=0.2)
        self.play(FadeIn(r16f), run_time=0.5)
        hear(self, "needs one", lead=0.2)
        self.play(FadeIn(c_gs), run_time=0.35)
        hear(self, "a 100", lead=0.2)
        self.play(FadeIn(c_bf), run_time=0.4)
        hear(self, "V100", lead=0.2)
        self.play(FadeIn(c_v), FadeIn(c_t), run_time=0.4)
        done(self)


class B55_HonestGains(Scene):
    """Only the activations segment halves; weights and optimizer state stay; two speed-up claims disagree: quote neither."""
    def construct(self):
        title = act_title("V · Memory And Precision")
        x0 = -4.6
        def seg(x, w, y, fill):
            return Rectangle(width=w - 0.05, height=0.6, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x + w / 2, y, 0])
        yb_, ya_ = 1.5, 0.2
        bef = VGroup(seg(x0, 3.0, yb_, BAR2), seg(x0 + 3.0, 1.2, yb_, BAR1), seg(x0 + 4.2, 2.0, yb_, BAR3))
        aft = VGroup(seg(x0, 1.5, ya_, BAR2), seg(x0 + 1.5, 1.2, ya_, BAR1), seg(x0 + 2.7, 2.0, ya_, BAR3))
        l1 = T("before", 36).move_to([-5.45, yb_, 0])
        l2 = T("BF16", 36).move_to([-5.45, ya_, 0])
        names = [lab_c("activations", x0 + 1.5, yb_ + 0.7, 32), lab_c("weights", x0 + 3.6, yb_ + 0.7, 32), lab_c("optimizer", x0 + 5.2, yb_ + 0.7, 32)]
        nh = lab_l("not 2x", x0 + 4.7 + 0.3, ya_, 40)
        ops = T("matrix and convolution only", 34).move_to([2.8, -0.9, 0])
        c1 = chip("up to 8x", -4.6, -2.1, size=36)
        q = T("?", 56).move_to([-2.6, -2.1, 0])
        c2 = chip("1.5 to 3x", -0.7, -2.1, size=36)
        qn = T("quote neither", 44).move_to([3.9, -2.1, 0])
        slots55 = [dashed_slot(-4.6, -2.1, 2.6, 0.8), dashed_slot(-0.7, -2.1, 3.0, 0.8), dashed_slot(3.9, -2.1, 3.6, 0.8), dashed_slot(2.8, -0.9, 4.6, 0.5)]
        self.play(FadeIn(title), *[FadeIn(s_) for s_ in slots55], run_time=0.4)
        hear(self, "Total memory", lead=0.1)
        self.play(FadeIn(bef), FadeIn(l1), *[FadeIn(n) for n in names], run_time=0.6)
        hear(self, "drop by half", lead=0.2)
        self.play(FadeIn(l2), FadeIn(aft), run_time=0.5)
        hear(self, "optimizer state", lead=0.2)
        self.play(FadeIn(nh), run_time=0.3)
        hear(self, "speed", lead=0.1)
        self.remove(slots55[3])
        self.play(FadeIn(ops), run_time=0.4)
        hear(self, "eight", lead=0.3)
        self.remove(slots55[0])
        self.play(FadeIn(c1), run_time=0.3)
        hear(self, "one and a half", lead=0.25)
        self.remove(slots55[1])
        self.play(FadeIn(q), FadeIn(c2), run_time=0.35)
        hear(self, "Quote", lead=0.1)
        self.remove(slots55[2])
        self.play(c1.animate.set_opacity(0.4), c2.animate.set_opacity(0.4), FadeIn(qn), run_time=0.4)
        done(self)


class B60_EightyFirst(Scene):
    """A utilization scale (60 fix first, 80 more cards pay); one card at 20 percent becomes four at 20 percent; reading-bound jobs get worse."""
    def construct(self):
        title = act_title("VI · More Than One GPU")
        x0, sc, y = -5.0, 0.1, 2.2
        scale = Line([x0, y, 0], [x0 + 10, y, 0], color=INK, stroke_width=6)
        ends = VGroup(T("0", 32).move_to([x0, y + 0.45, 0]), T("100", 32).move_to([x0 + 10, y + 0.45, 0]))
        t60 = VGroup(Line([x0 + 6, y - 0.2, 0], [x0 + 6, y + 0.2, 0], color=INK, stroke_width=6), T("60", 32).move_to([x0 + 6, y + 0.45, 0]))
        t80 = VGroup(Line([x0 + 8, y - 0.2, 0], [x0 + 8, y + 0.2, 0], color=INK, stroke_width=6), T("80", 32).move_to([x0 + 8, y + 0.45, 0]))
        dot = Dot([x0 + 2, y, 0], radius=0.17, color=TERRA)
        one = gpu_card(-4.6, 0.5, w=1.5, h=0.9)
        p20 = T("20%", 40).move_to([-4.6, -0.3, 0])
        arr = Arrow([-3.6, 0.5, 0], [-2.6, 0.5, 0], color=INK, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.4)
        four = [gpu_card(-1.6 + 1.9 * i, 0.5, w=1.5, h=0.9) for i in range(4)]
        p4 = [T("20%", 36).move_to([-1.6 + 1.9 * i, -0.3, 0]) for i in range(4)]
        cost = T("four times the allocation", 36).move_to([1.2, -0.95, 0])
        f60 = T("fix first", 34).move_to([x0 + 6, y - 0.55, 0])
        pay = T("more cards pay", 34).move_to([x0 + 9, y - 0.55, 0])
        ck = check(x0 + 9.0, y - 1.0, s=0.2, color=TERRA, w=10)
        cr = x_mark(x0 + 6, y - 1.05, r=0.22, w=8)
        rd = chip("reading data", -4.2, -2.3, size=34)
        smalls = [gpu_card(-0.8 + 1.7 * i, -2.3, w=1.3, h=0.8) for i in range(4)]
        arrs = [Arrow([-2.5, -2.3, 0], [-1.6 + 1.7 * i - 0.2 + 0.0, -2.3, 0], color=BAR1, stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.0) for i in range(0)]
        rx = x_mark(5.6, -2.3, r=0.3, w=9)
        self.play(FadeIn(title), Create(scale), FadeIn(ends), run_time=0.5)
        hear(self, "20", lead=0.3)
        self.play(FadeIn(dot), FadeIn(one), FadeIn(p20), run_time=0.4)
        hear(self, "four", lead=0.2)
        self.play(Create(arr), *[FadeIn(c) for c in four], *[FadeIn(p) for p in p4], run_time=0.6)
        self.play(FadeIn(cost), run_time=0.3)
        hear(self, "Add cards", lead=0.15)
        self.play(FadeIn(t80), FadeIn(pay), Create(ck), run_time=0.5)
        hear(self, "Under 60", lead=0.15)
        self.play(FadeIn(t60), FadeIn(f60), Create(cr), run_time=0.5)
        hear(self, "limited", lead=0.2)
        self.play(FadeIn(rd), *[FadeIn(s) for s in smalls], run_time=0.5)
        self.play(Create(rx), run_time=0.3)
        done(self)


class B61_AllReduce(Scene):
    """Four cards each hold a model copy and a different batch; gradients average at one point; every card applies the same update."""
    def construct(self):
        title = act_title("VI · More Than One GPU")
        xs = [-4.5, -1.5, 1.5, 4.5]
        cards = [gpu_card(x, 0.4, w=1.9, h=1.1) for x in xs]
        models = [Rectangle(width=0.7, height=0.4, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x - 0.15, 0.4, 0]) for x in xs]
        mlab = lab_c("model copy", -4.5, 1.35, 32)
        batches = [paper(x, 2.35, w=0.9, h=0.7) for x in xs]
        letters = [T(ch, 36).move_to([x, 2.35, 0]) for ch, x in zip("ABCD", xs)]
        avg = chip("average", 0.0, -1.4, size=36)
        arrs = [Arrow([x, -0.25, 0], [x * 0.35, -1.0, 0], color=INK, stroke_width=6, buff=0.05, max_tip_length_to_length_ratio=0.25) for x in xs]
        thick = Rectangle(width=2.0, height=0.35, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-4.6, -2.7, 0])
        thick_l = lab_l("inside a node: fast", -3.4, -2.7, 34)
        thin = Rectangle(width=3.0, height=0.12, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([2.2, -2.7, 0])
        thin_l = lab_c("between nodes: slower", 2.2, -3.2, 34)
        big = Rectangle(width=2.4, height=1.3, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([4.9, -1.5, 0])
        bigl = lab_c("too big", 4.9, -0.65, 34)
        bx = x_mark(4.9, -1.5, r=0.4, w=10)
        self.play(FadeIn(title), *[FadeIn(c) for c in cards], run_time=0.5)
        hear(self, "full model", lead=0.2)
        self.play(*[FadeIn(m) for m in models], FadeIn(mlab), run_time=0.5)
        hear(self, "different batch", lead=0.45)
        self.play(*[FadeIn(b) for b in batches], *[FadeIn(l) for l in letters], run_time=0.5)
        hear(self, "average", lead=0.2)
        self.play(FadeIn(avg), *[Create(a) for a in arrs], run_time=0.6)
        hear(self, "apply", lead=0.2)
        self.play(*[c.light.animate.set_color(TERRA) for c in cards], run_time=0.4)
        hear(self, "Fast", lead=0.1)
        self.play(FadeIn(thick), FadeIn(thick_l), run_time=0.4)
        hear(self, "slower", lead=0.2)
        self.play(FadeIn(thin), FadeIn(thin_l), run_time=0.4)
        hear(self, "cannot fix", lead=0.1)
        self.play(FadeIn(big), FadeIn(bigl), run_time=0.3)
        self.play(Create(bx), run_time=0.3)
        done(self)


class B66_ScalingEfficiency(Scene):
    """Efficiency = throughput on N cards over N times one card's; above 80 extra cards pay, below 70 stop, 70 to 80 not described."""
    def construct(self):
        title = act_title("VI · More Than One GPU")
        num_l = lab_l("throughput on N cards", -5.7, 2.35, 36)
        num = Rectangle(width=4.0, height=0.45, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0.7, 2.35, 0])
        fl = Line([-5.7, 1.65, 0], [2.9, 1.65, 0], color=INK, stroke_width=6)
        den_l = lab_l("N x one card", -5.7, 0.95, 36)
        den = VGroup(*[Rectangle(width=0.95, height=0.45, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.5 + 1.0 * i + 0.5, 0.95, 0]) for i in range(4)])
        eff = T("= efficiency", 48).move_to([4.5, 1.65, 0])
        x0, sc, y = -5.0, 0.1, -1.2
        s1 = Rectangle(width=7.0 - 0.06, height=0.5, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x0 + 3.5, y, 0])
        s2 = dashed_slot(x0 + 7.5, y, 1.0 - 0.06, 0.5)
        s3 = Rectangle(width=2.0 - 0.06, height=0.5, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x0 + 9.0, y, 0])
        nums = VGroup(*[T(str(v), 32).move_to([x0 + v * sc, y + 0.55, 0]) for v in (0, 70, 80, 100)])
        l1 = lab_c("stop: look for a bottleneck", x0 + 3.5, y - 0.65, 34)
        l2 = T("?", 52).move_to([x0 + 7.5, y - 0.65, 0])
        l2b = lab_c("not described", x0 + 7.5, y - 1.3, 32)
        l3 = lab_c("extra cards pay", x0 + 9.0, y - 0.65, 34)
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "Efficiency", lead=0.2)
        self.play(FadeIn(num_l), GrowFromEdge(num, LEFT), run_time=0.5)
        hear(self, "divided", lead=0.2)
        self.play(Create(fl), FadeIn(den_l), LaggedStart(*[FadeIn(d) for d in den], lag_ratio=0.2), FadeIn(eff), run_time=0.9)
        hear(self, "Above", lead=0.2)
        self.play(FadeIn(nums), GrowFromEdge(s3, LEFT), FadeIn(l3), run_time=0.6)
        hear(self, "Below", lead=0.2)
        self.play(GrowFromEdge(s1, LEFT), FadeIn(l1), run_time=0.7)
        hear(self, "70 to 80", lead=0.4)
        self.play(FadeIn(s2), FadeIn(l2), FadeIn(l2b), run_time=0.4)
        done(self)


# ═════════════════════════════ PART D — Acts VII and VIII (manim beats) ═════════════════════════════


def pD_rack(x, y, n):
    """A small drawn rack: n dark slabs stacked (Explorer 2, AICR 4)."""
    return VGroup(*[RoundedRectangle(corner_radius=0.06, width=1.3, height=0.32, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
                    .move_to([x, y + 0.38 * i, 0]) for i in range(n)])


class B70_TheLoop(Scene):
    """Seven stations on a ring; a job box travels round and each station gets its light as it arrives."""
    def construct(self):
        title = act_title("VII · The Loop")
        names = ["baseline", "profile", "diagnose", "fix one thing", "re-profile", "record the gain", "repeat"]
        pos = [(0.0, 2.1), (3.4, 1.3), (4.3, -0.6), (1.9, -2.1), (-1.9, -2.1), (-4.3, -0.6), (-3.4, 1.3)]
        arrows = []
        for i in range(7):
            p, q = np.array(pos[i] + (0,)), np.array(pos[(i + 1) % 7] + (0,))
            m = (p + q) / 2
            d = (q - p) / np.linalg.norm(q - p)
            arrows.append(Arrow(m - d * 0.3, m + d * 0.3, color=BAR1, stroke_width=7, buff=0, max_tip_length_to_length_ratio=0.5))
        chips = [chip(n, x, y, size=34) for n, (x, y) in zip(names, pos)]
        job = job2(0.0, 0.0, 0.9)
        dots = [Dot([x - 0.0, y + 0.55, 0], radius=0.1, color=TERRA) for (x, y) in pos]
        cues = ["Baseline", "profile", "diagnose", "fix", "re", "record", "repeat"]
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "loop", lead=0.3)
        self.play(FadeIn(job), run_time=0.5)
        for i in range(7):
            hear(self, cues[i], lead=0.15)
            self.play(FadeIn(chips[i]), job.animate.move_to([pos[i][0] * 0.55, pos[i][1] * 0.55, 0]), FadeIn(dots[i]), FadeIn(arrows[i]), run_time=0.5)
        done(self)


class B71_DecisionGuide(Scene):
    """A decision tree: utilization under 50 goes to the data pipeline; 50 to 80 goes to memory, which branches; an out-of-memory track."""
    def construct(self):
        title = act_title("VII · The Loop")
        root = chip("utilization", -5.0, 0.9, size=36)
        b1 = chip("< 50", -2.4, 2.1, size=34)
        b2 = chip("50 to 80", -2.4, -0.3, size=34)
        r1 = chip("data pipeline first", 1.7, 2.1, size=34)
        r1m = chip("num_workers == 0 ?", 1.7, 1.35, mono=True, size=28)
        mem = chip("memory", -0.2, -0.3, size=34)
        s1 = chip("< 50%: raise batch", 3.9, 0.4, w=4.4, size=28)
        s2 = chip("50-85%: mixed precision", 3.9, -0.35, w=4.4, size=28)
        s3 = chip("> 90%: shrink or checkpoint", 3.9, -1.1, w=4.4, size=28)
        def ln(a, b):
            return Line([a[0], a[1], 0], [b[0], b[1], 0], color=BAR1, stroke_width=5)
        l1, l2 = ln((-4.0, 1.0), (-3.1, 2.0)), ln((-4.0, 0.8), (-3.2, -0.2))
        l3, l4 = ln((-1.7, 2.1), (-0.9, 2.1)), ln((-1.7, -0.3), (-1.2, -0.3))
        l5 = [ln((0.8, -0.3), (1.6, y)) for y in (0.4, -0.35, -1.1)]
        oom_names = ["out of memory", "smaller batch", "mixed precision", "checkpoint"]
        ox = [-4.4, -1.55, 1.45, 4.5]
        ow = [2.6, 2.6, 2.9, 2.6]
        oom = [chip(n, x, -2.7, w=w, size=30) for n, x, w in zip(oom_names, ox, ow)]
        oar = [Arrow([ox[i] + ow[i] / 2 + 0.02, -2.7, 0], [ox[i + 1] - ow[i + 1] / 2 - 0.02, -2.7, 0], color=INK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.5) for i in range(3)]
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "utilization", lead=0.2)
        self.play(FadeIn(root), Create(l1), FadeIn(b1), run_time=0.5)
        hear(self, "data pipeline", lead=0.15)
        self.play(Create(l3), FadeIn(r1), run_time=0.4)
        hear(self, "workers still", lead=0.2)
        self.play(FadeIn(r1m), run_time=0.35)
        hear(self, "50 to 80", lead=0.2)
        self.play(Create(l2), FadeIn(b2), run_time=0.4)
        hear(self, "look at memory", lead=0.1)
        self.play(Create(l4), FadeIn(mem), *[Create(l) for l in l5], run_time=0.5)
        hear(self, "Memory under", lead=0.2)
        self.play(FadeIn(s1), run_time=0.35)
        hear(self, "50 to 85", lead=0.15)
        self.play(FadeIn(s2), run_time=0.35)
        hear(self, "over 90", lead=0.15)
        self.play(FadeIn(s3), run_time=0.35)
        hear(self, "Out of memory", lead=0.1)
        self.play(FadeIn(oom[0]), run_time=0.3)
        hear(self, "smaller batch", lead=0.1)
        self.play(Create(oar[0]), FadeIn(oom[1]), run_time=0.3)
        hear(self, "then mixed", lead=0.1)
        self.play(Create(oar[1]), FadeIn(oom[2]), run_time=0.3)
        hear(self, "check", lead=0.1)
        self.play(Create(oar[2]), FadeIn(oom[3]), run_time=0.3)
        done(self)


class B73_ReadGpuLogs(Scene):
    """Three schematic line plots (flat high, bouncing low, flat low) with the 70 line; two readouts; under 60, fix first."""
    def construct(self):
        title = act_title("VII · The Loop")
        xs = [-4.2, 0.0, 4.2]
        def plot(x):
            fr = Rectangle(width=3.4, height=1.7, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR2, stroke_width=5).move_to([x, 1.2, 0])
            y70 = DashedLine([x - 1.7, 1.2 - 0.85 + 1.7 * 0.7, 0], [x + 1.7, 1.2 - 0.85 + 1.7 * 0.7, 0], color=BAR1, stroke_width=4)
            return VGroup(fr, y70)
        def pts(x, f):
            return [[x - 1.5 + 3.0 * i / 20, 1.2 - 0.85 + 1.7 * f(i), 0] for i in range(21)]
        def curve(x, f):
            m = VMobject(stroke_color=INK, stroke_width=7)
            m.set_points_as_corners(pts(x, f))
            return m
        high = curve(xs[0], lambda i: 0.88 + (0.03 if i % 2 else -0.03))
        bounce = curve(xs[1], lambda i: 0.45 if i % 4 < 2 else 0.12)
        low = curve(xs[2], lambda i: 0.12 + (0.02 if i % 2 else -0.02))
        frames = [plot(x) for x in xs]
        t1 = [lab_c("flat and high", xs[0], -0.05, 34), lab_c("bouncing low", xs[1], -0.05, 34), lab_c("flat and low", xs[2], -0.05, 34)]
        t2 = [lab_c("healthy", xs[0], -0.6, 34), lab_c("data starvation", xs[1], -0.6, 34), lab_c("workload too small", xs[2], -0.6, 34)]
        tag = T("shapes, not output", 32).move_to([2.6, 2.75, 0])
        c1 = chip("average utilization: above 70", -3.0, -1.7, size=32)
        c2 = chip("average VRAM: low = room", 3.3, -1.7, size=32)
        fin = T("under 60: fix it before the next submission", 40).move_to([0, -2.8, 0])
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "average", lead=0.2)
        self.play(FadeIn(c1), run_time=0.4)
        hear(self, "shape of the line", lead=0.2)
        self.play(*[FadeIn(f) for f in frames], FadeIn(tag), run_time=0.5)
        hear(self, "flat and high", lead=0.15)
        self.play(Create(high), FadeIn(t1[0]), FadeIn(t2[0]), run_time=0.7)
        hear(self, "Bouncing", lead=0.15)
        self.play(Create(bounce), FadeIn(t1[1]), FadeIn(t2[1]), run_time=0.7)
        hear(self, "Flat and low", lead=0.15)
        self.play(Create(low), FadeIn(t1[2]), FadeIn(t2[2]), run_time=0.7)
        hear(self, "VRAM", lead=0.2)
        self.play(FadeIn(c2), run_time=0.4)
        hear(self, "Under 60", lead=0.15)
        self.play(FadeIn(fin), run_time=0.5)
        done(self)


class B74_Checklist(Scene):
    """A clipboard page of eight rows; each box gets a check on its spoken cue."""
    def construct(self):
        title = act_title("VII · The Loop")
        shadow = Rectangle(width=12.0, height=5.2, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([0.1, -0.4, 0])
        page = Rectangle(width=12.0, height=5.2, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([0, -0.3, 0])
        labels = ["verify passed", "over 70% in a short run", "workers + pin set", "half the VRAM used",
                  "precision matches card", "type named, 4+ CPUs", "logs/ exists", "profiled 20 to 50 steps"]
        pos = [(-5.5, 1.4), (-5.5, 0.3), (-5.5, -0.8), (-5.5, -1.9), (0.5, 1.4), (0.5, 0.3), (0.5, -0.8), (0.5, -1.9)]
        boxes, labs, cks = [], [], []
        for (x, y), t in zip(pos, labels):
            boxes.append(Rectangle(width=0.45, height=0.45, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=4).move_to([x + 0.22, y, 0]))
            labs.append(lab_l(t, x + 0.7, y, 34))
            cks.append(check(x + 0.2, y, s=0.2, color=TERRA, w=11))
        cues = ["check passed", "short run", "Workers", "batch uses", "Precision", "request", "logs folder", "profiled"]
        self.play(FadeIn(title), FadeIn(shadow), FadeIn(page), run_time=0.4)
        for i in range(8):
            hear(self, cues[i], lead=0.2)
            self.play(FadeIn(boxes[i]), FadeIn(labs[i]), run_time=0.25)
            self.play(Create(cks[i]), run_time=0.2)
        done(self)


class B80_YourDomain(Scene):
    """Four rows: PyTorch and TensorFlow (every act), Hugging Face (flags), molecular dynamics (trajectory writes), custom CUDA (Nsight Compute)."""
    def construct(self):
        title = act_title("VIII · Your Domain")
        ys = [1.7, 0.5, -0.7, -1.9]
        r1 = Group(logo_chip("pytorch", -5.2, ys[0], h=0.95), logo_chip("tensorflow", -3.7, ys[0], h=0.95), lab_c("every act", 1.4, ys[0], 40))
        r2 = Group(logo_chip("huggingface", -5.2, ys[1], h=0.95), lab_c("verify, watch, feed; fixes are flags", 3.15, ys[1], 36))
        r3 = Group(chip("GROMACS  NAMD  AMBER", -3.2, ys[2], w=5.7, mono=True, size=30), lab_c("trajectory writes limit you", 2.8, ys[2], 38))
        r4 = Group(logo_chip("nvidia", -5.2, ys[3], h=0.95), chip("custom CUDA", -3.0, ys[3], mono=True, size=30), lab_c("add Nsight Compute", 2.2, ys[3], 38))
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "PyTorch and", lead=0.15)
        self.play(FadeIn(r1), run_time=0.5)
        hear(self, "Package", lead=0.15)
        self.play(FadeIn(r2), run_time=0.5)
        hear(self, "Molecular", lead=0.15)
        self.play(FadeIn(r3), run_time=0.5)
        hear(self, "Custom", lead=0.15)
        self.play(FadeIn(r4), run_time=0.5)
        done(self)


class B82_ExplorerNotAicr(Scene):
    """Two columns, Explorer and AICR, row by row: the card, the environment, the post-job report, nvidia-smi on the login node."""
    def construct(self):
        title = act_title("VIII · Your Domain")
        div = Line([0, 2.6, 0], [0, -2.8, 0], color=BAR2, stroke_width=6)
        r_e, r_a = pD_rack(-1.6, 1.5, 2), pD_rack(4.6, 1.5, 4)
        h_e, h_a = T("Explorer", 42).move_to([-4.0, 1.75, 0]), T("AICR", 42).move_to([2.6, 1.75, 0])
        ys = [0.5, -0.4, -1.3, -2.2]
        L = [chip("gres: gpu:v100-sxm2:1", -3.2, ys[0], w=5.8, mono=True, size=30), chip("venv + pip wheels", -3.2, ys[1], w=5.8, size=34),
             chip("gpu-logs", -3.2, ys[2], w=5.8, mono=True, size=32), chip("no nvidia-smi on login", -3.2, ys[3], w=5.8, size=34)]
        R = [chip("the partition fixes the card", 3.2, ys[0], w=5.8, size=34), chip("CUDA module + conda", 3.2, ys[1], w=5.8, size=34),
             chip("jobstats", 3.2, ys[2], w=5.8, mono=True, size=32), chip("nvidia-smi on login", 3.2, ys[3], w=5.8, size=34)]
        self.play(FadeIn(title), Create(div), FadeIn(r_e), FadeIn(h_e), FadeIn(r_a), FadeIn(h_a), run_time=0.6)
        hear(self, "name the card", lead=0.3)
        self.play(FadeIn(L[0]), run_time=0.4)
        hear(self, "partition fixes", lead=0.2)
        self.play(FadeIn(R[0]), run_time=0.4)
        hear(self, "virtual environment", lead=0.3)
        self.play(FadeIn(L[1]), run_time=0.4)
        hear(self, "CUDA modules", lead=0.2)
        self.play(FadeIn(R[1]), run_time=0.4)
        hear(self, "GPU logs", lead=0.3)
        self.play(FadeIn(L[2]), run_time=0.4)
        hear(self, "job stats", lead=0.2)
        self.play(FadeIn(R[2]), run_time=0.4)
        hear(self, "login node", lead=0.3)
        self.play(FadeIn(L[3]), run_time=0.4)
        hear(self, "SMI", lead=0.2)
        self.play(FadeIn(R[3]), run_time=0.3)
        done(self)


class B83_CheckedVsRead(Scene):
    """Left, four read-only checks stamp in; right, five things only read from the source; 'nothing ran on a GPU node' first."""
    def construct(self):
        title = act_title("VIII · Your Domain")
        h1 = T("checked here, read-only", 40).move_to([-3.2, 2.05, 0])
        h2 = T("only read", 40).move_to([3.2, 2.05, 0])
        div = Line([0, 2.9, 0], [0, -2.0, 0], color=BAR2, stroke_width=6)
        left = [stamp(t, -3.2, y, w=5.4, size=32) for t, y in zip(["partitions and limits", "five GPU types", "tools on the path", "python module"], [1.3, 0.45, -0.4, -1.25])]
        for _s in left:
            _s[1].set_stroke(KRAFT_DEEP, width=4)  # Gate T: an ink outline round the text reads as one blob over the label
        right = [chip(t, 3.2, y, w=4.6, size=32) for t, y in zip(["sessions", "demo scripts", "profilers", "gpu-logs output", "numbers"], [1.4, 0.7, 0.0, -0.7, -1.4])]
        nothing = chip("nothing ran on a GPU node", 0.0, -2.8, size=38)
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "ran nothing", lead=0.3)
        self.play(FadeIn(nothing), Create(div), FadeIn(h1), FadeIn(h2), run_time=0.5)
        for cue, s in zip(["partitions", "five", "tools", "Python"], left):
            hear(self, cue, lead=0.2)
            self.play(FadeIn(s), run_time=0.3)
        for cue, c in zip(["sessions", "scripts", "profilers", "GPU logs", "numbers"], right):
            hear(self, cue, lead=0.15)
            self.play(FadeIn(c), run_time=0.25)
        done(self)


class B84_GetHelp(Scene):
    """Professor Bear beside three chips: the Research Computing help address, office hours, a consultation."""
    def construct(self):
        title = act_title("VIII · Your Domain")
        pb = professor_bear("1x1", 2.6, seed="B84", x=-4.4, y=0.0)
        c1 = chip("rchelp@northeastern.edu", 1.9, 1.3, w=6.9, mono=True, size=32)
        c2 = chip("office hours", 1.9, 0.0, w=6.9, size=38)
        c3 = chip("book a consultation", 1.9, -1.3, w=6.9, size=38)
        d = [Dot([-1.35, y, 0], radius=0.12, color=TERRA) for y in (1.3, 0.0, -1.3)]
        self.play(FadeIn(title), FadeIn(pb), run_time=0.5)
        hear(self, "write", lead=0.2)
        self.play(FadeIn(c1), FadeIn(d[0]), run_time=0.4)
        hear(self, "office hours", lead=0.2)
        self.play(FadeIn(c2), FadeIn(d[1]), run_time=0.4)
        hear(self, "consultation", lead=0.2)
        self.play(FadeIn(c3), FadeIn(d[2]), run_time=0.4)
        done(self)


for _cls in (B10_QuietFailures, B11_Partitions, B15_MemAndType, B19_VisibleDevices, B20_TwoNumbers, B22_TwoAxes, B23_Bands, B24_IdleBot, B30_FourLayers, B33_ReadTheTable, B35_TimelinePatterns, B40_Deliveries, B44_StartingValues, B47_WhereDataLives, B48_Illustration, B50_BatchDoubles, B53_BitSplit, B55_HonestGains, B60_EightyFirst, B61_AllReduce, B66_ScalingEfficiency, B70_TheLoop, B71_DecisionGuide, B73_ReadGpuLogs, B74_Checklist, B80_YourDomain, B82_ExplorerNotAicr, B83_CheckedVsRead, B84_GetHelp):
    _cls.play = ST.play
