"""scenes.py — Logging into AICR with Claude (lecture). The show-tell iso_kit is pasted below verbatim (Gate A copies
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
_ASR = {"BOPEN": [["Research", 0.0], ["Computing", 0.38], ["on", 0.8], ["Explorer", 1.0], ["and", 1.44], ["AICR,", 1.68], ["logging", 2.9], ["into", 2.98], ["AICR", 3.3], ["with", 4.0], ["Claude,", 4.14], ["how", 4.96], ["to", 5.12], ["let", 5.24], ["Claude", 5.38], ["code", 5.64], ["log", 5.92], ["into", 6.24], ["the", 6.46], ["AICR", 6.62], ["cluster", 7.32], ["for", 7.52], ["you", 7.84], ["and", 8.02], ["run", 8.2], ["commands", 8.38], ["there,", 8.8], ["while", 9.26], ["your", 9.44], ["key", 9.62], ["and", 9.86], ["your", 10.06], ["passphrase", 10.18], ["never", 10.7], ["leave", 11.02], ["your", 11.28], ["hands.", 11.44]], "BIDEA": [["Hallo,", 0.7], ["this", 1.26], ["is", 1.36], ["Liam", 1.58], ["in", 1.86], ["for", 2.16], ["Bear.", 2.32], ["First", 3.06], ["a", 3.14], ["correction.", 3.32], ["To", 4.1], ["let", 4.18], ["Claude", 4.36], ["log", 4.58], ["into", 4.82], ["AICR,", 5.08], ["the", 6.0], ["shared", 6.04], ["GPU", 6.28], ["cluster,", 6.66], ["you", 7.3], ["do", 7.38], ["not", 7.48], ["hand", 7.62], ["it", 7.82], ["your", 7.92], ["password.", 8.06], ["AICR", 9.06], ["has", 9.54], ["no", 9.72], ["password.", 9.94], ["You", 10.7], ["unlock", 10.78], ["a", 11.08], ["key", 11.24], ["once", 11.38], ["yourself", 11.64], ["and", 12.08], ["Claude", 12.38], ["never", 12.6], ["sees", 12.9], ["it.", 13.18]], "BDEFS": [["Six", 0.0], ["terms,", 0.26], ["a", 0.76], ["private", 0.82], ["key,", 1.08], ["a", 1.54], ["secret", 1.66], ["file", 1.88], ["that", 2.28], ["proves", 2.5], ["who", 2.74], ["you", 2.94], ["are,", 3.04], ["a", 3.58], ["certificate,", 3.68], ["a", 4.32], ["signed", 4.42], ["note", 4.68], ["from", 4.94], ["AICR", 5.14], ["saying", 5.8], ["that", 6.08], ["key", 6.26], ["is", 6.42], ["yours,", 6.58], ["a", 7.16], ["passphrase,", 7.26], ["the", 7.82], ["password", 7.92], ["that", 8.24], ["locks", 8.44], ["the", 8.66], ["key", 8.88], ["file,", 9.02], ["the", 9.9], ["SSH", 10.0], ["agent,", 10.22], ["a", 10.94], ["helper", 10.98], ["that", 11.14], ["holds", 11.34], ["your", 11.54], ["unlocked", 11.72], ["key", 12.1], ["in", 12.38], ["memory,", 12.5], ["batch", 13.4], ["mode,", 13.42], ["a", 13.86], ["setting", 13.92], ["that", 14.12], ["makes", 14.34], ["SSH", 14.5], ["refuse", 14.98], ["to", 15.46], ["ask", 15.68], ["any", 15.88], ["question,", 16.1], ["and", 16.86], ["a", 16.98], ["login", 17.08], ["node,", 17.3], ["the", 17.88], ["shared", 17.96], ["computer", 18.18], ["you", 18.56], ["land", 18.8], ["on", 19.0], ["when", 19.26], ["you", 19.42], ["log", 19.56], ["in.", 19.78]], "B10": [["AICR", 0.0], ["has", 0.7], ["no", 0.84], ["password,", 1.08], ["at", 1.82], ["the", 1.94], ["front", 2.06], ["door", 2.18], ["it", 2.42], ["checks", 2.54], ["two", 2.78], ["things,", 3.06], ["a", 3.66], ["private", 3.78], ["key,", 4.08], ["a", 4.68], ["secret", 4.74], ["file", 5.0], ["that", 5.4], ["only", 5.6], ["you", 5.78], ["hold,", 5.98], ["and", 6.66], ["a", 6.82], ["certificate,", 6.94], ["a", 7.62], ["note", 7.74], ["that", 7.9], ["ICR's", 8.16], ["own", 8.84], ["certificate", 9.02], ["authority", 9.48], ["signed", 9.92], ["saying", 10.56], ["that", 10.92], ["key", 11.14], ["is", 11.38], ["yours.", 11.58]], "B11": [["To", 0.0], ["get", 0.12], ["in", 0.24], ["at", 0.38], ["all,", 0.5], ["you", 0.86], ["need", 0.94], ["an", 1.06], ["account.", 1.22], ["A", 1.86], ["faculty", 1.92], ["member's", 2.26], ["proposal", 2.74], ["opens", 3.06], ["a", 3.5], ["project", 3.68], ["and", 4.1], ["your", 4.5], ["institution", 4.62], ["creates", 5.08], ["your", 5.54], ["user.", 5.76], ["Your", 6.84], ["AICR", 6.98], ["username", 7.7], ["is", 8.16], ["your", 8.4], ["campus", 8.56], ["name", 8.86], ["with", 9.14], ["the", 9.34], ["institution", 9.46], ["on", 9.9], ["the", 10.18], ["end,", 10.32], ["like", 10.9], ["jsmith", 10.94], ["underscore", 11.58], ["neu.", 12.16]], "B12": [["The", 0.0], ["key", 0.14], ["files", 0.28], ["come", 0.62], ["from", 0.86], ["one", 1.06], ["place,", 1.24], ["the", 1.86], ["AICR", 1.88], ["on", 2.56], ["-demand", 2.68], ["portal", 2.96], ["at", 3.38], ["OOD", 3.7], [".AICR", 4.2], [".AI.", 5.34], ["You", 6.52], ["sign", 6.62], ["in", 6.86], ["there", 7.06], ["with", 7.22], ["your", 7.4], ["institutional", 7.52], ["credentials.", 7.98], ["That", 9.12], ["step", 9.18], ["is", 9.44], ["yours,", 9.64], ["not", 10.16], ["Claude's.", 10.34]], "B13": [["Download", 0.0], ["the", 0.36], ["folder", 0.54], ["called", 0.82], ["AICR", 1.1], ["Keys.", 1.94], ["Inside", 3.02], ["are", 3.12], ["four", 3.34], ["files,", 3.58], ["your", 4.2], ["private", 4.3], ["key", 4.62], ["locked", 4.94], ["with", 5.26], ["a", 5.48], ["passphrase,", 5.6], ["its", 6.24], ["public", 6.36], ["half,", 6.7], ["your", 7.32], ["certificate", 7.4], ["which", 7.8], ["is", 8.18], ["the", 8.36], ["credential,", 8.52], ["and", 9.28], ["a", 9.42], ["file", 9.52], ["holding", 9.78], ["your", 10.14], ["first", 10.36], ["passphrase.", 10.62]], "B14": [["Signing", 0.0], ["in", 0.46], ["is", 0.6], ["the", 0.78], ["human", 0.92], ["step,", 1.16], ["so", 1.86], ["are", 2.0], ["putting", 2.1], ["the", 2.26], ["files", 2.44], ["in", 2.72], ["place", 2.96], ["and", 3.2], ["choosing", 3.48], ["a", 3.72], ["new", 3.96], ["passphrase.", 4.06], ["Do", 5.18], ["not", 5.24], ["give", 5.42], ["Claude", 5.62], ["your", 5.86], ["institutional", 6.04], ["password", 6.48], ["and", 7.16], ["do", 7.52], ["not", 7.62], ["ask", 7.78], ["it", 8.0], ["to", 8.16], ["sign", 8.3], ["in", 8.54], ["for", 8.7], ["you.", 8.88]], "B15": [["Put", 0.0], ["the", 0.14], ["files", 0.26], ["in", 0.5], ["your", 0.7], [".ssh", 0.84], ["folder,", 1.74], ["set", 2.28], ["their", 2.5], ["permissions,", 2.68], ["and", 3.36], ["swap", 3.42], ["the", 3.7], ["first", 3.88], ["passphrase", 4.12], ["for", 4.6], ["one", 4.84], ["only", 5.04], ["you", 5.36], ["know.", 5.52], ["Windows", 6.3], ["is", 6.48], ["the", 6.8], ["same", 6.98], ["in", 7.24], ["PowerShell.", 7.54], ["Then", 8.56], ["delete", 8.64], ["the", 8.88], ["downloaded", 9.1], ["passphrase", 9.5], ["file.", 10.12]], "B16": [["Check", 0.0], ["the", 0.2], ["certificate", 0.38], ["with", 0.76], ["SSH", 1.06], ["Kegen", 1.4], ["-L.", 2.0], ["Principles", 2.86], ["must", 2.92], ["be", 3.36], ["your", 3.6], ["AICR", 3.74], ["username.", 4.5], ["Valid", 5.58], ["is", 5.64], ["a", 5.84], ["date", 5.98], ["range", 6.12], ["or", 6.5], ["forever.", 6.8], ["When", 7.56], ["it", 7.7], ["nears", 7.8], ["its", 8.12], ["end,", 8.26], ["renew", 8.78], ["it", 8.92], ["in", 9.12], ["the", 9.28], ["on", 9.38], ["-demand", 9.56], ["portal.", 9.8]], "B20": [["Now", 0.0], ["the", 0.22], ["problem,", 0.4], ["Claude", 1.22], ["Code", 1.22], ["runs", 1.5], ["commands", 1.84], ["with", 2.24], ["no", 2.54], ["keyboard", 2.78], ["attached.", 3.18], ["If", 4.24], ["SSH", 4.38], ["stops", 4.68], ["to", 5.12], ["ask", 5.38], ["for", 5.58], ["the", 5.78], ["passphrase,", 5.9], ["nobody", 6.72], ["can", 6.88], ["answer", 7.18], ["and", 7.58], ["the", 7.84], ["command", 7.94], ["hangs", 8.26], ["or", 8.66], ["fails.", 8.96]], "B21": [["The", 0.0], ["fix", 0.16], ["is", 0.28], ["not", 0.5], ["to", 0.72], ["give", 0.94], ["Claude", 1.12], ["the", 1.34], ["passphrase.", 1.52], ["The", 2.5], ["fix", 2.62], ["is", 2.82], ["to", 3.02], ["unlock", 3.2], ["the", 3.52], ["key", 3.74], ["before", 3.96], ["Claude", 4.28], ["arrives", 4.54], ["once", 5.0], ["in", 5.44], ["your", 5.74], ["own", 5.84], ["terminal", 6.02], ["into", 6.46], ["a", 6.8], ["helper", 6.98], ["called", 7.18], ["SSH", 7.56], ["agent.", 7.96], ["The", 9.08], ["agent", 9.22], ["holds", 9.52], ["the", 9.86], ["unlocked", 10.08], ["key", 10.5], ["in", 10.84], ["memory.", 11.04]], "B22": [["From", 0.0], ["then", 0.12], ["on,", 0.26], ["when", 0.5], ["SSH", 0.66], ["needs", 1.02], ["the", 1.5], ["key,", 1.76], ["it", 2.22], ["asks", 2.32], ["the", 2.58], ["agent", 2.82], ["and", 3.16], ["the", 3.38], ["agent", 3.5], ["answers.", 3.8], ["The", 4.78], ["key", 4.92], ["never", 5.06], ["leaves", 5.28], ["the", 5.56], ["agent.", 5.8], ["Claude", 6.62], ["does", 6.62], ["the", 6.88], ["work.", 7.04], ["The", 7.46], ["secret", 7.56], ["never", 7.84], ["passes", 8.14], ["through", 8.54], ["it.", 8.88]], "B23": [["Add", 0.0], ["one", 0.2], ["block", 0.42], ["to", 0.66], ["your", 0.86], ["SSH", 0.96], ["config.", 1.24], ["Host", 2.62], ["AICR", 2.62], ["gives", 3.38], ["the", 3.6], ["cluster", 3.82], ["a", 4.02], ["short", 4.28], ["name,", 4.5], ["then", 5.22], ["its", 5.34], ["host", 5.52], ["name,", 5.72], ["your", 6.36], ["AICR", 6.38], ["username,", 7.08], ["your", 7.82], ["key", 7.9], ["file,", 8.1], ["and", 8.7], ["your", 8.74], ["certificate", 8.84], ["file.", 9.22]], "B24": [["Identities", 0.0], ["only", 0.52], ["offers", 0.72], ["just", 1.16], ["this", 1.44], ["key.", 1.68], ["Server", 2.5], ["Alive", 2.5], ["Interval", 2.84], ["stops", 3.3], ["idle", 3.58], ["connections", 3.94], ["dropping.", 4.44], ["Add", 5.72], ["keys", 5.82], ["to", 5.98], ["Agent", 6.26], ["loads", 6.56], ["the", 6.88], ["key", 7.14], ["into", 7.28], ["the", 7.46], ["Agent", 7.62], ["on", 7.9], ["first", 8.12], ["use.", 8.4], ["Use", 9.14], ["keychain", 9.28], ["is", 9.76], ["for", 9.92], ["Mac", 10.12], ["OS", 10.36], ["only,", 10.68], ["and", 11.44], ["Ignore", 11.52], ["Unknown", 11.84], ["makes", 12.32], ["other", 12.66], ["systems", 12.98], ["skip", 13.3], ["it.", 13.62]], "B25": [["On", 0.0], ["a", 0.14], ["Mac,", 0.24], ["unlock", 0.78], ["it", 0.86], ["with", 1.06], ["SSH", 1.22], ["add", 1.58], ["in", 2.08], ["the", 2.24], ["Apple", 2.34], ["keychain", 2.6], ["flag", 3.0], ["so", 3.38], ["the", 3.76], ["passphrase", 3.9], ["survives", 4.32], ["restarts.", 4.8], ["On", 6.22], ["Linux,", 6.32], ["start", 6.72], ["an", 6.98], ["agent,", 7.12], ["add", 7.7], ["the", 7.8], ["key,", 7.96], ["and", 8.4], ["start", 8.5], ["clod", 8.74], ["code", 9.02], ["from", 9.3], ["that", 9.56], ["same", 9.74], ["terminal.", 10.02]], "B26": [["On", 0.0], ["Windows,", 0.18], ["open", 0.78], ["PowerShell", 1.0], ["as", 1.54], ["administrator", 1.8], ["once,", 2.32], ["set", 3.3], ["the", 3.58], ["agent", 3.74], ["service", 3.98], ["to", 4.26], ["start", 4.56], ["automatically,", 4.84], ["start", 5.88], ["it,", 6.06], ["and", 6.48], ["add", 6.54], ["the", 6.7], ["key.", 6.84]], "B27": [["Each", 0.0], ["of", 0.2], ["these", 0.34], ["asks", 0.48], ["for", 0.76], ["your", 0.96], ["passphrase", 1.08], ["in", 1.58], ["your", 1.82], ["own", 1.92], ["terminal,", 2.1], ["type", 2.82], ["it", 3.0], ["there,", 3.2], ["never", 3.6], ["in", 3.72], ["a", 3.9], ["prompt", 3.98], ["to", 4.2], ["Claude,", 4.4], ["then", 5.14], ["ask", 5.3], ["the", 5.54], ["agent", 5.72], ["what", 6.0], ["it", 6.24], ["holds.", 6.34], ["One", 7.08], ["line", 7.22], ["ending", 7.48], ["in", 7.88], ["ED25519", 8.1], ["means", 9.88], ["the", 10.28], ["key", 10.52], ["is", 10.72], ["loaded.", 10.9]], "B30": [["Test", 0.0], ["it", 0.22], ["by", 0.36], ["hand", 0.5], ["first.", 0.76], ["Run", 1.56], ["SSH", 1.62], ["AICR", 2.0], ["host", 2.92], ["name.", 3.14], ["You", 3.86], ["should", 3.86], ["get", 4.0], ["login", 4.18], [".aicr", 4.44], [".ai.", 5.64], ["The", 6.74], ["very", 6.84], ["first", 7.06], ["connection", 7.32], ["asks", 7.7], ["you", 8.08], ["to", 8.3], ["confirm", 8.42], ["the", 8.76], ["host", 8.94], ["key.", 9.16], ["Type", 9.86], ["yes", 9.98], ["yourself", 10.2], ["because", 10.64], ["Claude", 11.02], ["cannot", 11.3], ["answer", 11.64], ["that.", 12.0]], "B31": [["Then", 0.0], ["test", 0.18], ["it", 0.4], ["the", 0.56], ["way", 0.66], ["Claude", 0.82], ["connects", 1.08], ["with", 1.48], ["batch", 1.84], ["mode", 2.06], ["on.", 2.34], ["Batch", 3.22], ["mode", 3.34], ["makes", 3.6], ["SSH", 3.86], ["fail", 4.24], ["at", 4.72], ["once", 4.92], ["instead", 5.2], ["of", 5.52], ["asking", 5.66], ["anything.", 5.94], ["If", 6.74], ["it", 6.86], ["prints", 6.96], ["your", 7.14], ["username", 7.32], ["in", 7.7], ["the", 7.9], ["host,", 8.02], ["Claude", 8.66], ["can", 8.72], ["log", 8.98], ["in.", 9.22]], "B32": [["Now", 0.0], ["a", 0.2], ["real", 0.4], ["run,", 0.64], ["Claude", 1.48], ["Code", 1.5], ["ran", 1.86], ["one", 2.12], ["SSH", 2.4], ["command", 2.72], ["with", 3.3], ["Batch", 3.54], ["Mode", 3.88], ["on,", 4.06], ["before", 4.64], ["this", 4.8], ["call", 5.04], ["the", 5.26], ["agent", 5.44], ["held", 5.72], ["no", 5.98], ["keys.", 6.26], ["The", 7.16], ["command", 7.22], ["asks", 7.5], ["for", 7.84], ["the", 8.1], ["username,", 8.22], ["the", 8.86], ["host,", 8.92], ["and", 9.4], ["the", 9.46], ["date.", 9.56]], "B33": [["The", 0.0], ["cluster", 0.14], ["answered", 0.42], ["with", 0.82], ["its", 1.04], ["seven", 1.2], ["partitions", 1.52], ["and", 2.0], ["an", 2.48], ["empty", 2.58], ["job", 2.84], ["queue", 3.14], ["because", 3.5], ["nothing", 3.86], ["was", 4.14], ["running.", 4.44], ["The", 5.44], ["last", 5.54], ["line", 5.8], ["is", 6.14], ["the", 6.34], ["home", 6.5], ["directory", 6.7], ["named", 7.28], ["after", 7.72], ["the", 8.04], ["user.", 8.22]], "B34": [["Now", 0.0], ["the", 0.2], ["test", 0.36], ["that", 0.56], ["matters,", 0.76], ["when", 1.42], ["you", 1.58], ["reboot,", 1.7], ["the", 2.24], ["agent", 2.26], ["forgets", 2.58], ["everything,", 3.06], ["so", 3.96], ["empty", 4.1], ["it", 4.34], ["on", 4.5], ["purpose", 4.64], ["and", 4.94], ["see", 5.32], ["whether", 5.48], ["Claude", 5.72], ["can", 5.96], ["still", 6.2], ["get", 6.46], ["in.", 6.68]], "B35": [["Ask", 0.0], ["the", 0.2], ["agent", 0.4], ["what", 0.68], ["it", 0.86], ["holds,", 0.98], ["one", 1.52], ["key.", 1.56], ["Empty", 2.42], ["it", 2.46], ["with", 2.64], ["SSH", 2.78], ["add", 3.14], ["dash", 3.58], ["capital", 3.9], ["D.", 4.26], ["Ask", 4.86], ["again,", 5.08], ["nothing.", 5.58], ["The", 6.2], ["agent", 6.24], ["is", 6.52], ["empty,", 6.72], ["just", 7.2], ["as", 7.38], ["it", 7.6], ["is", 7.72], ["after", 7.84], ["a", 8.14], ["reboot.", 8.28]], "B36": [["Now", 0.0], ["log", 0.2], ["in", 0.46], ["the", 0.6], ["way", 0.68], ["Claude", 0.86], ["does", 1.14], ["with", 1.44], ["batch", 1.72], ["mode", 1.96], ["on", 2.22], ["and", 2.46], ["an", 2.58], ["empty", 2.68], ["agent,", 2.94], ["it", 3.52], ["still", 3.64], ["works.", 3.86], ["No", 4.72], ["prompt,", 4.9], ["no", 5.42], ["passphrase", 5.54], ["typed,", 6.0], ["and", 6.64], ["ask", 6.72], ["the", 6.92], ["agent", 7.08], ["again,", 7.36], ["the", 7.88], ["key", 7.98], ["is", 8.12], ["back.", 8.28]], "B37": [["On", 0.0], ["a", 0.14], ["Mac,", 0.3], ["that", 0.58], ["is", 0.68], ["the", 0.8], ["key", 0.96], ["chain", 1.1], ["at", 1.36], ["work.", 1.54], ["Add", 2.5], ["keys", 2.6], ["to", 2.78], ["agent", 3.06], ["asks", 3.3], ["it", 3.68], ["for", 3.92], ["the", 4.06], ["passphrase", 4.18], ["and", 4.7], ["the", 5.0], ["key", 5.12], ["goes", 5.28], ["back", 5.48], ["into", 5.78], ["the", 5.98], ["agent.", 6.12], ["Nothing", 6.9], ["was", 7.08], ["typed", 7.3], ["and", 7.66], ["nothing", 7.92], ["passed", 8.16], ["to", 8.52], ["Claude.", 8.76]], "B38": [["On", 0.0], ["Linux", 0.2], ["and", 0.42], ["Windows,", 0.68], ["there", 1.22], ["is", 1.3], ["no", 1.38], ["keychain", 1.6], ["to", 2.06], ["reload", 2.28], ["the", 2.54], ["key,", 2.72], ["so", 3.28], ["this", 3.5], ["same", 3.66], ["test", 3.9], ["fails", 4.22], ["until", 4.56], ["you", 4.86], ["run", 5.0], ["SSH", 5.22], ["add", 5.72], ["again.", 6.12], ["That", 6.86], ["is", 6.92], ["expected.", 7.06], ["It", 8.02], ["tells", 8.14], ["you", 8.34], ["to", 8.54], ["run", 8.68], ["SSH", 8.86], ["add", 9.3], ["at", 9.8], ["the", 9.92], ["start", 10.02], ["of", 10.26], ["each", 10.44], ["session.", 10.58]], "B39": [["How", 0.0], ["did", 0.14], ["it", 0.28], ["get", 0.38], ["in?", 0.52], ["Ask", 0.78], ["SSH", 0.98], ["to", 1.34], ["show", 1.8], ["its", 2.0], ["steps.", 2.2], ["It", 2.9], ["found", 2.96], ["one", 3.16], ["key", 3.42], ["in", 3.62], ["the", 3.8], ["agent", 3.92], ["and", 4.26], ["offered", 4.54], ["the", 4.74], ["certificate.", 4.94], ["The", 6.02], ["server", 6.14], ["accepted", 6.42], ["it", 6.9], ["and", 7.18], ["SSH", 7.44], ["reports", 7.86], ["it", 8.46], ["authenticated", 8.66], ["with", 9.18], ["public", 9.58], ["key.", 9.88]], "B40": [["When", 0.0], ["you", 0.14], ["ask,", 0.24], ["Claude", 0.82], ["runs", 0.82], ["one", 1.1], ["SSH", 1.4], ["command", 1.68], ["with", 2.24], ["Batch", 2.5], ["Mode", 2.82], ["on,", 3.0], ["followed", 3.48], ["by", 3.8], ["your", 4.04], ["read", 4.2], ["-only", 4.4], ["commands.", 4.64], ["Claude", 5.66], ["Code", 5.94], ["asks", 6.24], ["you", 6.54], ["to", 6.78], ["approve", 6.9], ["it.", 7.18], ["On", 7.7], ["a", 7.78], ["shared", 7.92], ["system,", 8.06], ["approve", 8.94], ["each", 8.96], ["SSH", 9.26], ["command", 9.72], ["at", 10.26], ["least", 10.6], ["the", 10.74], ["first", 10.96], ["few", 11.12], ["times.", 11.36]], "B41": [["Rule", 0.0], ["1", 0.22], ["read", 0.5], ["only", 0.74], ["first,", 0.98], ["look", 1.66], ["before", 1.72], ["you", 2.0], ["change", 2.14], ["anything,", 2.38], ["sinfo,", 3.18], ["sq", 3.78], ["for", 3.96], ["your", 4.2], ["own", 4.32], ["jobs,", 4.5], ["sact,", 5.1], ["job", 5.68], ["stats,", 5.86], ["ls,", 6.46], ["and", 6.9], ["module", 6.94], ["avail.", 7.34]], "B42": [["Rule", 0.0], ["two,", 0.22], ["never", 0.7], ["compute", 0.82], ["on", 1.18], ["a", 1.34], ["login", 1.5], ["node.", 1.64], ["Login", 2.68], ["nodes", 2.68], ["are", 3.0], ["shared", 3.2], ["capped", 3.5], ["at", 3.8], ["four", 3.98], ["CPU", 4.22], ["cores", 4.58], ["and", 5.02], ["eight", 5.28], ["gigabytes", 5.46], ["of", 5.92], ["memory", 6.14], ["per", 6.34], ["user.", 6.66], ["Heavy", 7.54], ["work", 7.66], ["goes", 7.92], ["through", 8.16], ["SLURM,", 8.44], ["the", 9.04], ["scheduler,", 9.1], ["S", 9.9], ["-Batch", 10.02], ["or", 10.26], ["S", 10.58], ["-Alloc", 10.82], ["and", 11.16], ["S", 11.36], ["-Run", 11.6], ["for", 11.8], ["a", 12.04], ["live", 12.14], ["session.", 12.32]], "B43": [["Rule", 0.0], ["3,", 0.22], ["ask", 0.78], ["before", 0.9], ["s", 1.28], ["-batch,", 1.48], ["s", 1.94], ["-cancel,", 2.1], ["r", 2.8], ["-m,", 2.92], ["or", 3.44], ["anything", 3.52], ["that", 3.84], ["writes", 4.16], ["outside", 4.42], ["your", 4.84], ["own", 5.02], ["project.", 5.16], ["Jobs", 6.4], ["you", 6.52], ["shared", 6.8], ["GPUs", 7.08], ["and", 7.58], ["they", 7.9], ["count", 8.02], ["against", 8.24], ["your", 8.48], ["project.", 8.72]], "B44": [["Rule", 0.0], ["four,", 0.22], ["never", 0.72], ["print,", 0.84], ["copy", 1.34], ["or", 1.52], ["upload", 1.82], ["the", 2.14], ["private", 2.32], ["key.", 2.6], ["Not", 3.46], ["cat,", 3.54], ["not", 4.1], ["SCP,", 4.16], ["not", 4.92], ["into", 5.08], ["the", 5.26], ["chat.", 5.4], ["Claude", 6.18], ["does", 6.2], ["not", 6.36], ["need", 6.52], ["to", 6.68], ["read", 6.82], ["the", 6.98], ["key", 7.14], ["to", 7.3], ["use", 7.5], ["it.", 7.68], ["The", 8.12], ["agent", 8.22], ["does", 8.44], ["that.", 8.76]], "B45": [["Rule", 0.0], ["5", 0.24], ["never", 0.6], ["put", 0.9], ["the", 1.14], ["passphrase", 1.28], ["in", 1.68], ["a", 1.86], ["prompt,", 1.96], ["a", 2.42], ["file,", 2.46], ["or", 2.94], ["a", 3.06], ["command.", 3.12], ["If", 3.92], ["a", 4.08], ["command", 4.18], ["asks", 4.44], ["for", 4.76], ["it,", 5.04], ["stop", 5.3], ["and", 5.56], ["unlock", 5.82], ["the", 6.18], ["key", 6.4], ["yourself", 6.56], ["in", 6.94], ["your", 7.22], ["own", 7.34], ["terminal.", 7.5]], "B46": [["Rule", 0.0], ["6,", 0.24], ["use", 0.94], ["your", 1.0], ["own", 1.16], ["account", 1.32], ["only.", 1.66], ["The", 2.56], ["certificate", 2.6], ["names", 2.94], ["you,", 3.34], ["so", 3.72], ["do", 3.88], ["not", 4.0], ["use", 4.2], ["it", 4.42], ["to", 4.56], ["run", 4.7], ["work", 4.88], ["for", 5.14], ["anyone", 5.36], ["else.", 5.62]], "B47": [["In", 0.0], ["Rule", 0.16], ["7,", 0.3], ["Mind", 0.88], ["Where", 1.02], ["Files", 1.2], ["Live,", 1.46], ["Home", 2.24], ["is", 2.36], ["small", 2.5], ["and", 2.84], ["recoverable,", 3.08], ["Scratch", 4.1], ["is", 4.24], ["large", 4.44], ["and", 4.78], ["it", 5.1], ["is", 5.18], ["purged.", 5.34], ["Check", 6.14], ["AICR's", 6.32], ["file", 7.28], ["system", 7.42], ["page", 7.8], ["before", 8.14], ["you", 8.52], ["move", 8.68], ["data.", 8.86]], "B50": [["The", 0.0], ["error", 0.12], ["you", 0.34], ["will", 0.52], ["see", 0.66], ["most", 0.84], ["is", 1.12], ["permission", 1.36], ["denied", 1.7], ["public", 2.2], ["key.", 2.62], ["It", 3.58], ["usually", 3.66], ["means", 3.92], ["one", 4.24], ["of", 4.48], ["three", 4.6], ["things.", 4.8], ["The", 5.48], ["key", 5.6], ["is", 5.76], ["not", 5.9], ["unlocked", 6.12], ["by", 6.58], ["far", 6.86], ["the", 7.08], ["most", 7.2], ["common", 7.38], ["after", 7.74], ["a", 8.06], ["reboot,", 8.2], ["or", 8.8], ["the", 8.86], ["certificate", 8.98], ["is", 9.32], ["expired", 9.58], ["or", 10.06], ["missing,", 10.36], ["or", 11.02], ["the", 11.1], ["key's", 11.2], ["permissions", 11.48], ["are", 11.76], ["wrong.", 12.1]], "B51": [["Here's", 0.0], ["the", 0.32], ["trap,", 0.46], ["an", 0.98], ["empty", 1.02], ["agent", 1.26], ["looks", 1.62], ["exactly", 1.86], ["like", 2.3], ["an", 2.64], ["expired", 2.74], ["certificate.", 3.22], ["The", 4.28], ["error", 4.36], ["is", 4.62], ["the", 4.84], ["same.", 5.0], ["So", 5.84], ["check", 6.02], ["the", 6.24], ["agent", 6.46], ["with", 6.8], ["SSH", 6.98], ["add", 7.36], ["dash", 7.9], ["L", 8.16], ["before", 8.48], ["you", 8.76], ["blame", 8.92], ["the", 9.14], ["certificate.", 9.32]], "B52": [["Then", 0.0], ["if", 0.18], ["the", 0.32], ["agent", 0.48], ["holds", 0.72], ["the", 1.06], ["key,", 1.28], ["check", 1.66], ["the", 1.8], ["certificate.", 2.0], ["Is", 2.84], ["it", 2.9], ["still", 3.02], ["valid?", 3.28], ["If", 4.02], ["it", 4.1], ["is", 4.2], ["not,", 4.36], ["renew", 4.92], ["it", 5.12], ["in", 5.3], ["on", 5.4], ["-demand", 5.56], ["and", 5.9], ["set", 6.48], ["the", 6.68], ["private", 6.82], ["key's", 7.16], ["permissions", 7.52], ["to", 7.88], ["600.", 8.22]], "B53": [["Other", 0.0], ["messages", 0.22], ["have", 0.58], ["short", 0.92], ["fixes.", 1.22], ["A", 2.14], ["command", 2.14], ["that", 2.38], ["hangs", 2.6], ["or", 2.88], ["wants", 3.18], ["a", 3.42], ["passphrase,", 3.58], ["unlock", 4.24], ["the", 4.52], ["key", 4.76], ["yourself.", 4.9], ["Host", 6.0], ["key", 6.0], ["verification", 6.22], ["failed.", 6.7], ["Remove", 7.82], ["the", 7.84], ["old", 8.02], ["entry", 8.18], ["with", 8.5], ["SSH", 8.72], ["keygen", 9.0], ["-r,", 9.58], ["then", 10.32], ["connect", 10.4], ["once", 10.74], ["yourself.", 10.96], ["A", 11.82], ["new", 11.9], ["host", 12.06], ["key", 12.28], ["prompt,", 12.58], ["type", 13.1], ["yes.", 13.28]], "B54": [["Bad", 0.0], ["configuration", 0.2], ["option,", 0.72], ["add", 1.66], ["ignore", 1.68], ["unknown", 2.02], ["above", 2.54], ["the", 2.88], ["keychain", 3.06], ["line.", 3.42], ["Connection", 4.54], ["timed", 4.7], ["out,", 5.02], ["try", 5.44], ["another", 5.56], ["network", 5.8], ["because", 6.22], ["AICR", 6.52], ["needs", 7.28], ["no", 7.52], ["VPN.", 7.82], ["Drops", 8.92], ["when", 8.98], ["idle,", 9.26], ["server", 9.86], ["alive", 10.0], ["interval", 10.36], ["60.", 10.74], ["Empty", 11.84], ["after", 11.98], ["a", 12.3], ["restart,", 12.42], ["SSH", 13.1], ["add", 13.34], ["again", 13.78], ["on", 14.06], ["a", 14.32], ["Mac", 14.42], ["with", 14.58], ["the", 14.8], ["keychain", 14.94], ["flag.", 15.3]], "BVDT": [["Let's", 0.0], ["recap", 0.7], ["with", 0.94], ["Claude.", 1.22], ["AICR", 1.86], ["checks", 2.34], ["a", 2.6], ["key", 2.8], ["in", 2.98], ["a", 3.12], ["certificate,", 3.22], ["not", 3.86], ["a", 3.88], ["password.", 4.04], ["Claude", 4.78], ["cannot", 4.88], ["type", 5.12], ["a", 5.4], ["passphrase,", 5.54], ["so", 6.14], ["you", 6.2], ["unlock", 6.32], ["the", 6.6], ["key", 6.82], ["once", 6.96], ["into", 7.2], ["the", 7.44], ["SSH", 7.56], ["agent.", 7.8], ["Test", 8.92], ["with", 8.96], ["batch", 9.16], ["mode,", 9.4], ["even", 9.88], ["an", 10.02], ["emptied", 10.18], ["agent", 10.46], ["logged", 10.82], ["in", 11.1], ["on", 11.3], ["a", 11.42], ["Mac.", 11.54], ["Claude", 12.0], ["runs", 12.16], ["read", 12.46], ["-only", 12.68], ["commands", 12.86], ["and", 13.28], ["asks", 13.62], ["before", 13.86], ["it", 14.22], ["changes", 14.34], ["anything.", 14.66], ["The", 15.58], ["key", 15.7], ["and", 15.86], ["the", 15.98], ["passphrase", 16.1], ["never", 16.52], ["go", 16.78], ["into", 17.02], ["a", 17.2], ["prompt,", 17.38], ["and", 17.88], ["when", 18.0], ["you", 18.1], ["see", 18.22], ["permission", 18.36], ["denied,", 18.7], ["check", 19.4], ["the", 19.52], ["agent", 19.72], ["before", 20.0], ["you", 20.3], ["blame", 20.48], ["the", 20.68], ["certificate.", 20.86]], "BHTF": [["Your", 0.0], ["turn,", 0.14], ["paste", 0.58], ["this", 0.76], ["into", 0.96], ["Claude.", 1.2], ["Log", 1.98], ["into", 1.98], ["the", 2.2], ["AICR", 2.36], ["cluster", 2.98], ["with", 3.22], ["SSH", 3.5], ["AICR", 3.78], ["and", 4.64], ["run", 4.76], ["read", 4.96], ["-only", 5.2], ["commands", 5.4], ["only.", 5.78], ["Run,", 6.8], ["who", 7.16], ["am", 7.3], ["I,", 7.4], ["host", 7.72], ["name,", 7.84], ["PWD,", 8.16], ["S", 8.86], ["info", 9.0], ["with", 9.18], ["its", 9.42], ["output", 9.54], ["format", 9.82], ["set", 10.16], ["to", 10.38], ["percent", 10.54], ["14P,", 10.78], ["percent", 11.6], ["11L,", 11.8], ["percent", 12.44], ["6D,", 12.58], ["and", 13.18], ["SQ", 13.3], ["for", 13.54], ["my", 13.82], ["own", 13.98], ["user.", 14.12], ["Tell", 14.94], ["me", 15.08], ["the", 15.2], ["username,", 15.32], ["the", 15.86], ["host,", 15.94], ["and", 16.26], ["which", 16.38], ["partitions", 16.54], ["exist.", 16.92], ["Do", 17.78], ["not", 17.86], ["submit,", 18.0], ["cancel,", 18.56], ["or", 18.96], ["change", 19.08], ["anything", 19.36], ["and", 19.7], ["do", 19.96], ["not", 20.06], ["run", 20.22], ["computation", 20.4], ["on", 20.98], ["the", 21.32], ["login", 21.46], ["node.", 21.68], ["Then", 22.62], ["check", 22.8], ["two", 23.02], ["things", 23.28], ["yourself.", 23.54], ["Did", 24.36], ["Claude", 24.5], ["run", 24.72], ["only", 24.96], ["read", 25.3], ["-only", 25.54], ["commands", 25.76], ["and", 26.2], ["did", 26.68], ["it", 26.8], ["ever", 26.9], ["ask", 27.1], ["for", 27.38], ["or", 27.64], ["print", 27.84], ["your", 28.1], ["passphrase", 28.34], ["or", 28.9], ["your", 29.14], ["key?", 29.3]], "BOUT": [["Logging", 0.0], ["into", 0.42], ["AICR", 0.62], ["with", 1.4], ["Claude", 1.6], ["at", 1.98], ["Nick", 2.38], ["Baer", 2.64], ["Brown.", 2.94]]}


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


def plaque(text, x, y, w=6.2, h=1.0, size=34):
    """A white card carrying REAL error or command text in mono (no outline)."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
    card = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    lab = M(text, size).move_to([x, y, 0])
    g = VGroup(shadow, card, lab)
    g.card, g.label = card, lab
    return g


# ═════════════════════════════ PART A — Act I and Act II drawings (B10 B11 B13 B14 B20 B21 B22) ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.

def act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


class B10_KeyAndCert(Scene):
    """AICR checks two things at its door: a private key and a certificate; together they open the lock."""
    def construct(self):
        title = act_title("I · What AICR Checks")
        iso = Iso(3.6, -2.0, 1.15)
        stack, lights = aicr_rack(iso)
        door = Rectangle(width=2.5, height=3.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.5, -0.15, 0])
        lock = padlock(0.5, -0.1, s=1.4)
        aicr = T("AICR", 40).move_to([4.0, -3.05, 0])
        self.play(FadeIn(title), FadeIn(stack), FadeIn(lights), FadeIn(door), FadeIn(lock), FadeIn(aicr), run_time=0.5)
        # "AICR has no password": a password chip appears and is struck out
        hear(self, "has no password", lead=0.35)
        pw = chip("password", -2.2, 1.9, size=36)
        self.play(FadeIn(pw), run_time=0.3)
        hear(self, "at the front door", lead=0.35)
        cross = x_mark(-0.8, 1.9, r=0.3, w=9)
        self.play(Create(cross), run_time=0.3)
        # "a private key": slides in from the left
        hear(self, "a private key", lead=0.5)
        key = key_obj(-8.6, 0.6, s=1.0)
        self.add(key)
        self.play(key.animate.shift(RIGHT * 4.6), run_time=0.7, rate_func=smooth)
        klab = T("private key", 36).move_to([-2.9, -0.25, 0])
        self.play(FadeIn(klab), run_time=0.25)
        # "a certificate": slides in from below
        hear(self, "and a certificate", lead=0.5)
        cert = cert_page(-2.6, -5.0, w=1.7, h=2.1)
        self.add(cert)
        self.play(cert.animate.shift(UP * 3.4), run_time=0.7, rate_func=smooth)
        clab = T("certificate", 36).move_to([-2.6, -2.95, 0])
        self.play(FadeIn(clab), run_time=0.25)
        # "AICR's own certificate authority signed": the seal pulses, 'signed by AICR' lands
        hear(self, "own certificate authority", lead=0.3)
        self.play(Indicate(cert.seal, color=TERRA, scale_factor=1.5), run_time=0.7)
        # "saying that key is yours": key and certificate go to the lock; it opens; the rack wakes
        hear(self, "saying that key", lead=0.6)
        self.play(FadeOut(klab), FadeOut(clab), FadeOut(pw), FadeOut(cross), run_time=0.2)
        self.play(key.animate.shift(RIGHT * 2.5 + DOWN * 0.1), cert.animate.shift(RIGHT * 1.3 + UP * 0.1), run_time=0.8)
        self.play(unlock_anim(lock), run_time=0.5)
        self.play(door.animate.stretch_to_fit_width(0.4).shift(LEFT * 1.0), *[l.animate.set_color(TERRA) for l in lights], run_time=0.7)
        done(self)


class B21_UnlockOnce(Scene):
    """You, not Claude, type the passphrase once: the lock opens and the key goes into the ssh-agent."""
    def construct(self):
        you = professor_bear("1x1", 2.8, seed="B21x", x=-5.0, y=-0.2)
        ylab = T("you", 38).move_to([-5.0, -2.3, 0])
        key = key_obj(-2.4, 0.2, s=1.2)
        lock = padlock(-2.4, 0.2, s=1.2)
        iso = Iso(4.4, -1.9, 1.2)
        agent, alights = agent_slab(iso)
        alab = T("agent", 40).move_to([4.4, -3.0, 0])
        claude = chip("Claude", 1.2, 2.5, size=38)
        self.play(FadeIn(you), FadeIn(ylab), FadeIn(key), FadeIn(lock), FadeIn(agent), FadeIn(alights), FadeIn(alab), run_time=0.5)
        # "not to give Claude the passphrase": the passphrase dots head for Claude and are refused
        hear(self, "give Claude the passphrase", lead=0.6)
        dots = chip("••••••", -3.6, 1.7, size=40)
        self.play(FadeIn(claude), FadeIn(dots), run_time=0.3)
        self.play(dots.animate.move_to([-0.9, 2.5, 0]), run_time=0.6)
        refuse = x_mark(2.6, 2.5, r=0.3, w=9)
        self.play(Create(refuse), run_time=0.25)
        self.play(dots.animate.move_to([-3.6, 1.7, 0]), FadeOut(claude), FadeOut(refuse), run_time=0.5)
        # "unlock the key ... in your own terminal": the dots go to the lock, which opens
        hear(self, "unlock the key", lead=0.2)
        self.play(dots.animate.move_to([-2.4, 1.3, 0]), run_time=0.6)
        self.play(unlock_anim(lock, rt=0.5), FadeOut(dots), run_time=0.5)
        # "into a helper called ssh-agent": the key travels into the agent slab
        hear(self, "into a helper", lead=0.2)
        self.play(FadeOut(lock), run_time=0.2)
        self.play(key.animate.scale(0.6).move_to([4.4, 0.95, 0]), run_time=1.0, rate_func=smooth)
        # "holds the unlocked key in memory": the agent's light comes on
        hear(self, "holds the unlocked key", lead=0.2)
        self.play(alights[0].animate.set_color(TERRA), Indicate(agent, color=INK, scale_factor=1.04), run_time=0.7)
        done(self)


class B22_AgentAnswers(Scene):
    """ssh asks the agent; the agent answers; the key never leaves it; the command reaches AICR."""
    def construct(self):
        iso = Iso(-4.8, -1.9, 1.1)
        box = job_box(iso, 0, 0, 0, s=1.0)
        blab = M("ssh", 40).move_to([-4.8, -2.9, 0])
        side = T("Claude's side", 36).move_to([-4.6, 3.0, 0])
        iso2 = Iso(0.4, -1.9, 1.2)
        agent, alights = agent_slab(iso2)
        alights[0].set_color(TERRA)
        key = key_obj(-0.2, 0.55, s=0.6)
        alab = T("agent", 40).move_to([0.4, -3.0, 0])
        iso3 = Iso(4.4, -2.0, 0.9)
        rack, rlights = aicr_rack(iso3)
        rlab = T("AICR", 40).move_to([4.8, -3.05, 0])
        bar = DashedLine([-2.2, -2.6, 0], [-2.2, 3.0, 0], color=BAR1, stroke_width=6, dash_length=0.3)
        self.play(FadeIn(box), FadeIn(blab), FadeIn(side), FadeIn(agent), FadeIn(alights), FadeIn(key), FadeIn(alab), FadeIn(rack), FadeIn(rlights), FadeIn(rlab), Create(bar), run_time=0.5)
        # "it asks the agent": a question chip travels to the agent
        hear(self, "it asks the agent", lead=0.35)
        q = chip("key?", -3.4, 1.4, size=36)
        self.play(FadeIn(q), run_time=0.2)
        self.play(q.animate.move_to([-0.6, 1.4, 0]), run_time=0.6)
        # "the agent answers": a signed slip comes back
        hear(self, "and the agent answers", lead=0.3)
        slip = VGroup(paper(0.0, 0.0, w=1.0, h=1.0, fill=PAGE_TOP), check(0.0, 0.0, s=0.28))
        slip.move_to([-0.6, 1.4, 0])
        self.play(FadeOut(q), FadeIn(slip), run_time=0.25)
        self.play(slip.animate.move_to([-3.4, 1.4, 0]), run_time=0.6)
        # "the key never leaves the agent": a dashed path from the key toward Claude's side is struck out
        hear(self, "never leaves the agent", lead=0.2)
        out = DashedLine([-0.9, 0.55, 0], [-1.8, 0.55, 0], color=BAR1, stroke_width=6, dash_length=0.2)
        self.play(Create(out), run_time=0.4)
        no = x_mark(-2.0, 0.55, r=0.28, w=9)
        self.play(Create(no), run_time=0.3)
        # "Claude does the work": the command box, slip in hand, rides on to AICR
        hear(self, "Claude does the work", lead=0.3)
        self.play(FadeOut(out), FadeOut(no), FadeOut(slip), run_time=0.2)
        self.play(box.animate.shift(UP * 1.9), blab.animate.shift(UP * 0.0), run_time=0.4)
        self.play(box.animate.shift(RIGHT * 6.6), run_time=0.9, rate_func=smooth)
        self.play(box.animate.shift(DOWN * 1.4), run_time=0.3)
        hear(self, "never passes through it", lead=0.3)
        self.play(*[l.animate.set_color(TERRA) for l in rlights], run_time=0.5)
        done(self)


# ═════════════════════════════ PART B — B11 B13 B14 B20 B31 B34 B37 ═════════════════════════════

def pB_slot(x, y, w=2.0, h=1.1, color=BAR1):
    """A dashed empty slot (outline only)."""
    try:
        return DashedVMobject(RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=6, fill_opacity=0).move_to([x, y, 0]),
                              num_dashes=28)
    except Exception:
        r = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=6, fill_opacity=0).move_to([x, y, 0])
        return r


def pB_brk(x0, x1, y, tick=0.16):
    b = VMobject(stroke_color=INK, stroke_width=5)
    b.set_points_as_corners([[x0, y + tick, 0], [x0, y, 0], [x1, y, 0], [x1, y + tick, 0]])
    return b


def pB_row(name, role, y, x0=-3.5, w=9.3):
    """A table row: white card (kraft shadow), real file name in mono, short role label on the right."""
    shadow = Rectangle(width=w, height=0.9, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x0 + w / 2 + 0.08, y - 0.08, 0])
    card = Rectangle(width=w, height=0.9, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x0 + w / 2, y, 0])
    f = M(name, 32)
    f.move_to([x0 + 0.3 + f.width / 2, y, 0])
    r = T(role, 36)
    r.move_to([x0 + w - 0.3 - r.width / 2, y, 0])
    g = VGroup(shadow, card, f, r)
    g.card = card
    return g


class B11_UserName(Scene):
    """Your AICR user name = campus name + institution; the pattern becomes jsmith_neu."""
    def construct(self):
        acct = chip("account", 0.0, 0.5, size=40)
        self.add(acct)
        # "A faculty member's proposal opens a project and your institution creates your user"
        hear(self, "faculty member's proposal", lead=0.5)
        c1 = chip("proposal", -4.0, 0.5, size=38)
        c2 = chip("project", 0.0, 0.5, size=38)
        c3 = chip("your user", 4.0, 0.5, size=38)
        a1 = Arrow([-2.7, 0.5, 0], [-1.4, 0.5, 0], buff=0, color=INK, stroke_width=6, max_tip_length_to_length_ratio=0.4)
        a2 = Arrow([1.3, 0.5, 0], [2.4, 0.5, 0], buff=0, color=INK, stroke_width=6, max_tip_length_to_length_ratio=0.4)
        self.play(FadeOut(acct), FadeIn(c1), run_time=0.3)
        hear(self, "opens a project", lead=0.4)
        self.play(Create(a1), FadeIn(c2), run_time=0.4)
        hear(self, "creates your user", lead=0.5)
        self.play(Create(a2), FadeIn(c3), run_time=0.4)
        # "Your AICR username is": the pattern replaces the flow
        hear(self, "Your AICR username", lead=1.0)
        pat = M("institutionalusername_institutioncode", 34)
        if pat.width > 11.4:
            pat.scale_to_fit_width(11.4)
        pat.move_to([0, 0.6, 0])
        bg = pill(0, 0.6, pat.width + 0.9, h=0.95)
        shadow = pill(0.08, 0.52, pat.width + 0.9, h=0.95, fill=BOX_L)
        pc = VGroup(shadow, bg)
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(c3), FadeOut(a1), FadeOut(a2), FadeIn(pc), FadeIn(pat), run_time=0.35)
        # "your campus name" / "the institution on the end": the two halves are bracketed and labelled
        L0 = pat.get_left()[0]
        split = L0 + pat.width * 21 / 37
        hear(self, "your campus name", lead=0.3)
        b1 = pB_brk(L0 + 0.05, split - 0.05, 0.0)
        l1 = T("campus name", 36).move_to([(L0 + split) / 2, -0.65, 0])
        self.play(Create(b1), FadeIn(l1), run_time=0.45)
        hear(self, "institution on the end", lead=0.3)
        R0 = pat.get_right()[0]
        b2 = pB_brk(split + 0.05, R0 - 0.05, 0.0)
        l2 = T("institution", 36).move_to([(split + R0) / 2 + 0.2, -0.65, 0])
        self.play(Create(b2), FadeIn(l2), run_time=0.45)
        # "like jsmith underscore neu": it becomes jsmith_neu
        hear(self, "like jsmith", lead=0.4)
        out = M("jsmith_neu", 80).move_to([0, 0.6, 0])
        bg2 = pill(0, 0.6, out.width + 0.9, h=0.95)
        sh2 = pill(0.08, 0.52, out.width + 0.9, h=0.95, fill=BOX_L)
        self.play(FadeOut(b1), FadeOut(b2), FadeOut(l1), FadeOut(l2), Transform(pat, out), Transform(bg, bg2), Transform(shadow, sh2), run_time=0.9)
        done(self)


class B13_FourFiles(Scene):
    """The aicr keys folder holds four files; the certificate is the credential."""
    def construct(self):
        fold = chip("AICR keys", -4.3, 2.5, size=38)
        self.add(fold)
        ys = [1.4, 0.35, -0.7, -1.75]
        r1 = pB_row("id_ed25519_aicr", "private key", ys[0])
        r2 = pB_row("id_ed25519_aicr.pub", "public key", ys[1])
        r3 = pB_row("id_ed25519_aicr-cert.pub", "certificate", ys[2])
        r4 = pB_row(".passphrase", "first passphrase", ys[3])
        key = key_obj(-6.0, ys[0], s=0.5)
        page = cert_page(-5.4, ys[2], w=0.95, h=1.1)
        hear(self, "your private key", lead=0.5)
        self.play(FadeIn(r1), FadeIn(key), run_time=0.4)
        hear(self, "its public half", lead=0.6)
        self.play(FadeIn(r2), run_time=0.35)
        hear(self, "your certificate", lead=0.5)
        self.play(FadeIn(r3), FadeIn(page), run_time=0.4)
        hear(self, "which is the credential", lead=0.4)
        ring = RoundedRectangle(corner_radius=0.25, width=9.7, height=1.2, stroke_color=TERRA, stroke_width=8, fill_opacity=0).move_to([-3.5 + 4.65 + 0.04, ys[2] - 0.04, 0])
        self.play(Create(ring), run_time=0.5)
        hear(self, "and a file holding", lead=0.3)
        self.play(FadeIn(r4), run_time=0.35)
        done(self)


class B14_HumanSteps(Scene):
    """Sign in, download, passphrase are yours (checks land); the password is turned away from Claude."""
    def construct(self):
        bear = professor_bear("1x1", 2.8, seed="B14", x=-5.0, y=0.2)
        door = Rectangle(width=1.8, height=2.8, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([4.7, -0.1, 0])
        knob = Dot([5.3, -0.1, 0], radius=0.12, color=INK)
        claude = chip("Claude", 4.7, 2.0, size=38)
        self.add(bear, door, knob, claude)
        ys = [1.5, 0.4, -0.7]
        names = ["Sign in", "Download", "Passphrase"]
        cues = ["Signing in", "putting the files", "choosing a new"]
        leads = [-0.1, 0.35, 0.3]
        for nme, cue, y, ld in zip(names, cues, ys, leads):
            hear(self, cue, lead=ld)
            c = chip(nme, -1.6, y, size=38)
            self.play(FadeIn(c), run_time=0.25)
            ck = check(0.1, y, s=0.22, color=TERRA, w=9)
            self.play(Create(ck), run_time=0.25)
        # "Do not give Claude your institutional password": the password heads for the door and is turned away
        hear(self, "give Claude", lead=0.5)
        pw = chip("password", 1.4, -1.9, size=36)
        self.play(FadeIn(pw), run_time=0.25)
        hear(self, "institutional password", lead=0.2)
        self.play(pw.animate.move_to([1.9, -1.9, 0]), run_time=0.6)
        nope = x_mark(3.45, -1.9, r=0.3, w=9)
        self.play(Create(nope), run_time=0.3)
        hear(self, "ask it to sign in", lead=0.3)
        self.play(pw.animate.move_to([0.8, -1.9, 0]), run_time=0.5)
        done(self)


class B20_NobodyAnswers(Scene):
    """ssh meets the passphrase-locked key; nobody can answer; the command waits."""
    def construct(self):
        title = act_title("II · Unlock Once")
        key = key_obj(0.4, 0.3, s=1.1)
        lock = padlock(2.5, 0.3, s=1.4)
        iso = Iso(-5.4, -2.2, 0.9)
        box = job_box(iso, 0, 0, 0, s=0.9)
        box.move_to([-5.4, -0.5, 0])
        lab = M("ssh", 38).move_to([-5.4, -1.6, 0])
        self.play(FadeIn(title), FadeIn(key), FadeIn(lock), FadeIn(box), FadeIn(lab), run_time=0.5)
        # "Claude Code runs commands with no keyboard attached": the ssh box rides to the locked key
        hear(self, "runs commands", lead=0.3)
        self.play(box.animate.shift(RIGHT * 4.2), lab.animate.shift(RIGHT * 4.2), run_time=1.1, rate_func=smooth)
        # "ask for the passphrase": the lock raises the chip
        hear(self, "ask for the", lead=0.2)
        q = chip("passphrase?", 2.7, 1.9, size=38)
        self.play(FadeIn(q), run_time=0.2)
        self.play(q.animate.shift(UP * 0.4), run_time=0.4)
        # "nobody can answer": an empty answer slot appears beside the box
        hear(self, "nobody can answer", lead=0.35)
        slot = pB_slot(-3.0, -0.5)
        self.play(Create(slot), run_time=0.5)
        # "hangs or fails": the box waits, dimmed
        hear(self, "hangs", lead=0.3)
        self.play(box.animate.set_opacity(0.4), lab.animate.set_opacity(0.4), run_time=0.5)
        done(self)


class B31_FailFast(Scene):
    """Without BatchMode the box waits at the lock; with it the box bounces at once; unlocked, it passes."""
    def construct(self):
        ys = [1.3, -1.7]
        keys, locks, boxes, labs = [], [], [], []
        for y in ys:
            keys.append(key_obj(2.6, y, s=0.6))
            locks.append(padlock(3.5, y, s=0.9))
            iso = Iso(-4.4, y - 1.2, 0.8)
            b = job_box(iso, 0, 0, 0, s=0.7)
            b.move_to([-4.4, y - 0.1, 0])
            boxes.append(b)
            labs.append(M("ssh", 34).move_to([-4.4, y - 0.95, 0]))
        self.add(*keys, *locks)
        self.play(*[FadeIn(b) for b in boxes], *[FadeIn(l) for l in labs], run_time=0.4)
        # "test it the way Claude connects": the top box rides to the lock and waits
        hear(self, "way Claude connects", lead=0.3)
        self.play(boxes[0].animate.shift(RIGHT * 5.5), labs[0].animate.shift(RIGHT * 5.5), run_time=1.0, rate_func=smooth)
        waits = T("waits", 36).move_to([1.1, ys[0] + 1.05, 0])
        self.play(FadeIn(waits), run_time=0.25)
        # "with batch mode on": the lower lane is labelled
        hear(self, "mode on", lead=0.5)
        bm = chip("BatchMode", -4.4, ys[1] + 1.2, mono=True, size=34)
        self.play(FadeIn(bm), run_time=0.3)
        # "Batch mode makes ssh fail at once": the box meets the lock and bounces back with a cross
        hear(self, "Batch mode makes", lead=0.3)
        self.play(boxes[1].animate.shift(RIGHT * 5.5), labs[1].animate.shift(RIGHT * 5.5), run_time=0.8, rate_func=smooth)
        no = x_mark(0.95, ys[1] + 0.8, r=0.3, w=9)
        hear(self, "fail at", lead=0.0)
        self.play(Create(no), boxes[1].animate.shift(LEFT * 3.0), labs[1].animate.shift(LEFT * 3.0), run_time=0.5)
        # "If it prints your username": the lock opens and the box passes through
        hear(self, "If it prints", lead=0.5)
        self.play(FadeOut(no), unlock_anim(locks[1]), run_time=0.5)
        boxes[1].set_z_index(5); labs[1].set_z_index(5)
        self.play(boxes[1].animate.shift(RIGHT * 7.6), labs[1].animate.shift(RIGHT * 7.6), run_time=1.1, rate_func=smooth)
        # "Claude can log in": the check lands
        hear(self, "Claude can log in", lead=0.3)
        ok = check(5.5, ys[1] + 1.15, s=0.3, color=TERRA, w=10)
        self.play(Create(ok), run_time=0.4)
        done(self)


class B34_EmptyOnPurpose(Scene):
    """Reboot dial sweeps; the agent forgets (key leaves, light goes dark); the box waits before the empty agent."""
    def construct(self):
        iso = Iso(0.2, -1.9, 1.2)
        agent, alights = agent_slab(iso)
        alights[0].set_color(TERRA)
        key = key_obj(0, 0, s=0.6).move_to([0.2, 0.95, 0])
        alab = T("agent", 40).move_to([0.2, -3.0, 0])
        self.play(FadeIn(agent), FadeIn(alights), FadeIn(key), FadeIn(alab), run_time=0.4)
        # "when you reboot": a dial sweeps
        hear(self, "when you reboot", lead=0.3)
        dial = Circle(radius=0.85, stroke_color=INK, stroke_width=6, fill_color=PAGE_TOP, fill_opacity=1).move_to([-4.6, 0.9, 0])
        hand = Line([-4.6, 0.9, 0], [-4.6, 1.65, 0], color=INK, stroke_width=8)
        hub = Dot([-4.6, 0.9, 0], radius=0.1, color=INK)
        rl = T("reboot", 38).move_to([-4.6, -0.5, 0])
        self.play(FadeIn(dial), FadeIn(hub), FadeIn(rl), FadeIn(hand), run_time=0.3)
        self.play(Rotate(hand, angle=-2 * PI, about_point=[-4.6, 0.9, 0]), run_time=1.1, rate_func=smooth)
        # "the agent forgets everything": the key is pulled out and the light goes dark
        hear(self, "forgets everything", lead=0.6)
        self.play(key.animate.shift(UP * 1.5), alights[0].animate.set_color(GHOST), run_time=0.6)
        self.play(FadeOut(key), run_time=0.2)
        slot = pB_slot(0.2, 0.95, w=1.9, h=0.8)
        self.play(Create(slot), run_time=0.4)
        # "empty it on purpose": the ssh box arrives before the empty agent
        hear(self, "empty it", lead=0.2)
        iso2 = Iso(4.6, -2.0, 0.9)
        box = job_box(iso2, 0, 0, 0, s=0.9)
        box.move_to([4.6, -0.8, 0])
        blab = M("ssh", 38).move_to([4.6, -1.9, 0])
        self.play(FadeIn(box), FadeIn(blab), run_time=0.3)
        hear(self, "get in", lead=1.2)
        self.play(box.animate.shift(LEFT * 1.2), blab.animate.shift(LEFT * 1.2), run_time=0.7, rate_func=smooth)
        done(self)


class B37_VaultRefills(Scene):
    """macOS Keychain gives the key back to the agent; the box passes on; the key never crosses Claude's side."""
    def construct(self):
        iso = Iso(-1.7, -1.9, 1.1)
        agent, alights = agent_slab(iso)
        alab = T("agent", 40).move_to([-1.7, -3.0, 0])
        iso_v = Iso(2.0, -1.9, 1.1)
        vlt = vault(iso_v)
        vlab = T("Keychain", 40).move_to([2.4, -3.0, 0])
        iso_r = Iso(4.3, -2.0, 0.7)
        rack, rlights = aicr_rack(iso_r)
        rlab = T("AICR", 38).move_to([4.6, -3.05, 0])
        iso_b = Iso(-5.2, -2.2, 0.9)
        box = job_box(iso_b, 0, 0, 0, s=0.9)
        box.move_to([-5.2, -0.9, 0])
        blab = M("ssh", 38).move_to([-5.2, -1.95, 0])
        bar = DashedLine([-3.3, -2.8, 0], [-3.3, 3.0, 0], color=BAR1, stroke_width=6, dash_length=0.3)
        side = T("Claude's side", 36).move_to([-4.6, 3.0, 0])
        self.play(FadeIn(agent), FadeIn(alights), FadeIn(alab), FadeIn(vlt), FadeIn(vlab), FadeIn(rack), FadeIn(rlights), FadeIn(rlab),
                  FadeIn(box), FadeIn(blab), Create(bar), FadeIn(side), run_time=0.5)
        # "Add keys to agent asks it": the box asks the empty agent
        hear(self, "Add keys to agent", lead=0.2)
        q = chip("key?", -3.6, 1.3, size=36)
        self.play(FadeIn(q), run_time=0.2)
        self.play(q.animate.move_to([-1.4, 1.3, 0]), run_time=0.6)
        # "for the passphrase": the question goes on to the vault
        hear(self, "for the passphrase", lead=0.5)
        self.play(q.animate.move_to([2.4, 1.3, 0]), run_time=0.6)
        # the vault door opens, a key rises out
        self.play(FadeOut(q), FadeOut(vlt[1]), FadeOut(vlt[2]), run_time=0.35)
        key = key_obj(0, 0, s=0.6).move_to([2.3, 0.2, 0])
        self.play(GrowFromCenter(key), run_time=0.3)
        # "the key goes back into the agent": the key flies in, the light turns terracotta
        hear(self, "goes back into", lead=0.6)
        self.play(key.animate.move_to([2.3, 1.5, 0]), run_time=0.3)
        self.play(key.animate.move_to([-1.7, 1.0, 0]), run_time=0.9, rate_func=smooth)
        self.play(alights[0].animate.set_color(TERRA), Indicate(agent, color=INK, scale_factor=1.04), run_time=0.5)
        # "nothing passed to Claude": the box passes on toward the right; nothing crosses the barrier
        hear(self, "Nothing was typed", lead=0.3)
        self.play(box.animate.shift(UP * 2.6), blab.animate.shift(UP * 2.6), run_time=0.35)
        self.play(box.animate.shift(RIGHT * 9.3), blab.animate.shift(RIGHT * 9.3), run_time=1.0, rate_func=smooth)
        self.play(FadeOut(blab), box.animate.shift(DOWN * 1.3), run_time=0.3)
        done(self)


# ═════════════════════════════ PART C — Act III close and Act IV drawings (B38 B40 B41 B42 B43 B44 B45) ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.

def pC_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pC_box(x, y, s=1.0):
    """An 'ssh' command box (kraft + terracotta tape) centred on (x, y)."""
    g = job_box(Iso(0, 0, s), 0, 0, 0, s=1.0)
    return g.move_to([x, y, 0])


def pC_cpill(text, x, y, mono=True, size=34):
    """A white pill with a spare right-hand end for a check: returns (chip, check_point)."""
    lab = M(text, size - 2) if mono else T(text, size)
    c = chip(text, x, y, w=lab.width + 1.5, mono=mono, size=size)
    return c, np.array([x + (lab.width + 1.5) / 2 - 0.5, y, 0.0])


class B38_NoVault(Scene):
    """No Keychain on Linux: the ssh box bounces off the lock until you run ssh-add; then the key rises into the agent."""
    def construct(self):
        you = professor_bear("1x1", 2.1, seed="B38y", x=-5.2, y=1.7)
        ylab = T("you", 38).move_to([-5.2, -0.05, 0])
        box = pC_box(-5.2, -1.6)
        blab = M("ssh", 40).move_to([-5.2, -3.12, 0])
        key = key_obj(-2.6, -1.6, s=0.8)
        lock = padlock(-2.6, -1.6, s=0.9)
        iso = Iso(3.6, -1.9, 1.2)
        agent, alights = agent_slab(iso)
        alab = T("agent", 40).move_to([3.6, -3.0, 0])
        self.play(FadeIn(you), FadeIn(ylab), FadeIn(box), FadeIn(blab), FadeIn(key), FadeIn(lock), FadeIn(agent), FadeIn(alights), FadeIn(alab), run_time=0.5)
        # "no Keychain to reload the key": a Keychain chip, struck out
        hear(self, "no keychain", lead=0.5)
        kc = chip("Keychain", 1.6, 0.9, size=36)
        self.play(FadeIn(kc), run_time=0.25)
        hear(self, "reload the key", lead=0.2)
        kx = x_mark(3.3, 0.9, r=0.28, w=9)
        self.play(Create(kx), run_time=0.25)
        # "this same test fails": the ssh box runs into the lock and bounces
        hear(self, "same test fails", lead=0.5)
        self.play(FadeOut(kc), FadeOut(kx), box.animate.shift(RIGHT * 1.1), blab.animate.shift(RIGHT * 1.1), run_time=0.5)
        bx = x_mark(-3.5, -0.25, r=0.28, w=9)
        self.play(Create(bx), box.animate.shift(LEFT * 0.3), blab.animate.shift(LEFT * 0.3), run_time=0.25)
        self.play(box.animate.shift(LEFT * 0.8), blab.animate.shift(LEFT * 0.8), run_time=0.3)
        # "you run SSH add again": the ssh-add chip, the lock opens, the key rises into the agent
        hear(self, "run ssh add", lead=0.2)
        sa = chip("ssh-add", -2.4, 2.7, mono=True, size=36)
        self.play(FadeIn(sa, shift=DOWN * 0.3), FadeOut(bx), run_time=0.3)
        self.play(unlock_anim(lock, rt=0.5), run_time=0.5)
        self.play(FadeOut(lock), run_time=0.15)
        self.play(key.animate.scale(0.6).move_to([3.6, 0.95, 0]), run_time=1.0, rate_func=smooth)
        self.play(alights[0].animate.set_color(TERRA), run_time=0.3)
        # "That is expected": the box now passes the place where the lock was
        hear(self, "that is expected", lead=0.2)
        self.play(box.animate.shift(RIGHT * 3.9), blab.animate.shift(RIGHT * 3.9), run_time=0.9, rate_func=smooth)
        ck = check(box.get_center()[0] + 0.0, box.get_center()[1] + 0.9, s=0.2, color=TERRA)
        self.play(Create(ck), run_time=0.3)
        # "at the start of each session": a 'session start' tag lands beside the ssh-add chip
        hear(self, "start of each session", lead=0.4)
        ss = chip("session start", -2.0, 1.6, size=36)
        self.play(FadeIn(ss, shift=DOWN * 0.4), run_time=0.4)
        done(self)


class B40_YouApprove(Scene):
    """Act IV opens: the ssh command waits at a gate; your check lands on its tag; the gate lifts and it goes on to AICR."""
    def construct(self):
        title = pC_act_title("IV · Rules For A Shared Cluster")
        you = professor_bear("1x1", 2.0, seed="B40", x=-2.2, y=1.2)
        ylab = T("you", 38).move_to([-0.4, 1.2, 0])
        gate = Rectangle(width=0.5, height=2.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-2.2, -1.0, 0])
        iso = Iso(3.8, -2.0, 1.0)
        rack, rlights = aicr_rack(iso)
        rlab = T("AICR", 40).move_to([4.3, -3.05, 0])
        box = pC_box(-5.4, -1.6)
        blab = M("ssh", 40).move_to([-5.4, -2.9, 0])
        bx = VGroup(box, blab)
        self.play(FadeIn(title), FadeIn(you), FadeIn(ylab), FadeIn(gate), FadeIn(rack), FadeIn(rlights), FadeIn(rlab), FadeIn(bx), run_time=0.5)
        # "Claude runs one ssh command": the box slides up to the gate and waits
        hear(self, "runs one ssh", lead=0.3)
        self.play(bx.animate.shift(RIGHT * 2.0), run_time=0.9, rate_func=smooth)
        # "with BatchMode on": the mono chip
        hear(self, "batch mode", lead=0.3)
        bm = chip("BatchMode", -4.7, 0.2, mono=True, size=34)
        self.play(FadeIn(bm), run_time=0.25)
        # the empty approval tag on the box
        hear(self, "asks you to", lead=0.4)
        tag = pill(-3.1, -0.35, 1.0, h=0.6)
        self.play(FadeIn(tag), run_time=0.25)
        # "approve it": your check lands on the tag
        hear(self, "approve it", lead=0.45)
        ck = check(-2.2, 0.45, s=0.2, color=TERRA)
        self.play(FadeIn(ck), run_time=0.15)
        self.play(ck.animate.move_to([-3.1, -0.35, 0]), run_time=0.4)
        # the gate lifts, the box goes on to the rack
        hear(self, "on a shared system", lead=0.3)
        bx.add(tag, ck)
        self.play(FadeOut(gate, shift=UP * 0.6), FadeOut(bm), run_time=0.4)
        self.play(bx.animate.shift(RIGHT * 4.1), run_time=1.1, rate_func=smooth)
        hear(self, "approve each", lead=0.1)
        self.play(*[l.animate.set_color(TERRA) for l in rlights], run_time=0.5)
        done(self)


class B41_ReadOnly(Scene):
    """Rule one: look before you change anything. Six read-only commands land one by one and each takes a check."""
    def construct(self):
        head = chip("Read only first", 0.9, 2.6, size=40)
        eye_out = Ellipse(width=1.9, height=1.0, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6)
        pupil = Dot([0, 0, 0], radius=0.22, color=INK)
        eye = VGroup(eye_out, pupil).move_to([-3.4, 2.6, 0])
        names = ["sinfo", "squeue -u $USER", "sacct", "jobstats", "ls", "module avail"]
        built = []
        for n in names:
            c, cp = pC_cpill(n, 0.0, 0.0)
            built.append((c, cp))
        rows = [[0, 1, 2], [3, 4, 5]]
        ys = [0.7, -1.0]
        pos = {}
        for r, ri in enumerate(rows):
            total = sum(built[i][0].width for i in ri) + 0.4 * (len(ri) - 1)
            x = -total / 2
            for i in ri:
                w = built[i][0].width
                pos[i] = np.array([x + w / 2, ys[r], 0.0])
                x += w + 0.4
        # "Rule one. Read only first": heading and the eye appear together
        hear(self, "read only first", lead=0.45)
        self.play(FadeIn(head), GrowFromCenter(eye), run_time=0.4)
        hear(self, "look before", lead=0.1)
        self.play(pupil.animate.shift(LEFT * 0.3), run_time=0.25)
        self.play(pupil.animate.shift(RIGHT * 0.6), run_time=0.3)
        cues = [("sinfo", 0.3), ("sq for", 0.3), ("sact", 0.3), ("job stats", 0.3), ("ls", 0.25), ("module avail", 0.3)]
        for i, (ph, ld) in enumerate(cues):
            c, cp = built[i]
            dx = pos[i] - c.get_center()
            c.shift(dx)
            hear(self, ph, lead=ld + 0.25)
            ck = check(cp[0] + (pos[i][0] - built[i][0].get_center()[0]) * 0, pos[i][1], s=0.15, color=TERRA, w=6)
            ck.move_to(c.get_right() + LEFT * 0.5)
            self.play(FadeIn(c, shift=DOWN * 0.4), run_time=0.25)
            self.play(Create(ck), run_time=0.2)
        self.play(pupil.animate.shift(LEFT * 0.3), run_time=0.3)
        done(self)


class B42_LoginCap(Scene):
    """Rule two: the login node is capped at 4 cores and 8 GB; the heavy job is stopped and goes through Slurm to the big rack."""
    def construct(self):
        iso = Iso(-4.4, -2.0, 1.0)
        small, slights = explorer_rack(iso)
        slab = T("login node", 38).move_to([-4.4, -2.95, 0])
        # the meter: ink-outlined bar, partly filled, with a cap line
        mx, my, mw, mh = -4.4, 1.2, 3.4, 0.5
        bar = Rectangle(width=mw, height=mh, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([mx, my, 0])
        left = mx - mw / 2
        fill = Rectangle(width=0.9, height=mh - 0.1, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([left + 0.05 + 0.45, my, 0])
        capx = left + 2.4
        cap = Line([capx, my - 0.5, 0], [capx, my + 0.5, 0], color=INK, stroke_width=10)
        big, blights = aicr_rack(Iso(4.1, -2.4, 1.0))
        blab = T("AICR", 40).move_to([4.5, -3.05, 0])
        gate = Rectangle(width=0.5, height=2.6, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([1.5, -1.1, 0])
        glab = T("Slurm", 40).move_to([1.5, 0.7, 0])
        heavy = pC_box(-0.3, -1.45, s=1.4)
        self.play(FadeIn(small), FadeIn(slights), FadeIn(slab), FadeIn(bar), FadeIn(fill), FadeIn(cap), FadeIn(big), FadeIn(blights), FadeIn(blab), run_time=0.5)
        # "never compute": the heavy job comes up to the login node and fills the meter to the cap
        hear(self, "never compute", lead=0.1)
        self.play(FadeIn(heavy), run_time=0.2)
        self.play(heavy.animate.shift(LEFT * 1.4), fill.animate.stretch_to_fit_width(2.35).move_to([left + 0.05 + 1.175, my, 0]), run_time=0.9, rate_func=smooth)
        stop = x_mark(-2.75, -0.2, r=0.3, w=9)
        self.play(Create(stop), run_time=0.25)
        # "capped at four ... eight": the hero labels
        hear(self, "four cpu cores", lead=0.45)
        n4 = T("4 cores", 46).move_to([-5.3, 2.35, 0])
        self.play(FadeIn(n4, shift=DOWN * 0.2), run_time=0.3)
        hear(self, "eight gigabytes", lead=0.45)
        n8 = T("8 GB", 46).move_to([-2.9, 2.35, 0])
        self.play(FadeIn(n8, shift=DOWN * 0.2), run_time=0.3)
        # "Heavy work goes through Slurm": back off, the Slurm gate rises
        hear(self, "heavy work", lead=0.2)
        self.play(FadeOut(stop), heavy.animate.shift(RIGHT * 1.7), FadeIn(gate), run_time=0.5)
        hear(self, "slurm", lead=0.3)
        self.play(FadeIn(glab), run_time=0.3)
        # "the scheduler": the gate lifts, the box shrinks and goes on to the big rack
        hear(self, "the scheduler", lead=0.2)
        self.play(FadeOut(gate, shift=UP * 0.6), run_time=0.35)
        self.play(heavy.animate.scale(0.5).move_to([1.35, -1.7, 0]), run_time=0.9, rate_func=smooth)
        hear(self, "for a live session", lead=0.5)
        self.play(*[l.animate.set_color(TERRA) for l in blights], run_time=0.5)
        done(self)


class B43_AskFirst(Scene):
    """Rule three: sbatch, scancel and rm each wait at the gate for your check; the shared GPUs count against your project."""
    def construct(self):
        you = professor_bear("1x1", 2.0, seed="B43q", x=0.0, y=2.0)
        ylab = T("you", 38).move_to([1.8, 2.0, 0])
        gate = Rectangle(width=0.5, height=3.0, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.0, -0.9, 0])
        iso = Iso(3.8, -2.2, 1.0)
        gpu, glights = iso.server(0, 0, 0, w=2.0, d=1.6, slab=0.5, n=2)
        glab = T("shared GPU", 38).move_to([4.0, -3.1, 0])
        self.play(FadeIn(you), FadeIn(ylab), FadeIn(gate), FadeIn(gpu), FadeIn(glights), FadeIn(glab), run_time=0.5)
        cmds = [("sbatch", "batch", 0.0), ("scancel", "cancel", 0.0), ("rm", "r m", -1.0)]
        for (name, ph, _), y in zip(cmds, [0.0, -1.0, -2.0]):
            c, cp = pC_cpill(name, -2.2, y)
            hear(self, ph, lead=0.2)
            self.play(FadeIn(c, shift=RIGHT * 0.3), run_time=0.2)
            ck = check(0.0, 1.0, s=0.16, color=TERRA, w=6)
            tx = -2.2 + (c.width / 2 - 0.5)
            self.play(FadeIn(ck), run_time=0.1)
            self.play(ck.animate.move_to([tx, y, 0]), run_time=0.3)
            grp = VGroup(c, ck)
            self.play(FadeOut(gate), run_time=0.12)
            self.play(grp.animate.shift(RIGHT * 3.6), run_time=0.45, rate_func=smooth)
            self.play(FadeIn(gate), run_time=0.12)
        # "shared GPUs ... count against your project"
        hear(self, "count against your project", lead=0.5)
        proj = chip("your project", 3.6, 1.2, size=38)
        self.play(FadeIn(proj, shift=DOWN * 0.3), *[l.animate.set_color(TERRA) for l in glights], run_time=0.6)
        done(self)


class B44_KeyStays(Scene):
    """Rule four: cat, scp and chat all bounce off the glass; the key stays in the agent and the agent's own arrow to AICR stays open."""
    def construct(self):
        side = T("Claude's side", 36).move_to([-4.4, 3.0, 0])
        iso = Iso(0.8, -1.9, 1.2)
        agent, alights = agent_slab(iso)
        alights[0].set_color(TERRA)
        key = key_obj(0.8, 0.95, s=0.6)
        alab = T("agent", 40).move_to([0.8, -3.0, 0])
        iso3 = Iso(4.5, -2.1, 0.75)
        rack, rlights = aicr_rack(iso3)
        rlab = T("AICR", 40).move_to([4.8, -3.0, 0])
        barrier = DashedLine([-1.5, -2.8, 0], [-1.5, 2.7, 0], color=BAR1, stroke_width=6, dash_length=0.3)
        arrow = Arrow([2.4, -1.0, 0], [3.4, -1.0, 0], color=INK, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.5)
        self.play(FadeIn(side), FadeIn(agent), FadeIn(alights), FadeIn(key), FadeIn(alab), FadeIn(rack), FadeIn(rlights), FadeIn(rlab), Create(barrier), Create(arrow), run_time=0.5)
        # "print, copy or upload": three pills wait on Claude's side
        items = [("cat", True, 1.9), ("scp", True, 0.6), ("chat", False, -0.7)]
        built = []
        for k, (name, mono, y) in enumerate(items):
            c = chip(name, -4.8, y, mono=mono, size=36)
            built.append((c, y))
        hear(self, "never print", lead=0.1)
        self.play(FadeIn(built[0][0]), run_time=0.2)
        hear(self, "copy", lead=0.2)
        self.play(FadeIn(built[1][0]), run_time=0.2)
        hear(self, "upload", lead=0.2)
        self.play(FadeIn(built[2][0]), run_time=0.2)
        marks = []
        for k, ((c, y), ph, ld) in enumerate(zip(built, ["not cat", "scp", "the chat"], [0.45, 0.45, 0.2])):
            hear(self, ph, lead=ld)
            self.play(c.animate.move_to([-2.5, y, 0]), run_time=0.35)
            xm = x_mark(-1.5, y, r=0.28, w=9)
            marks.append(xm)
            self.play(Create(xm), run_time=0.15)
            self.play(c.animate.move_to([-3.6, y, 0]), run_time=0.25)
        # "The agent does that": the agent's own arrow to AICR, the rack wakes
        hear(self, "the agent does that", lead=0.2)
        self.play(Indicate(arrow, color=TERRA, scale_factor=1.3), *[l.animate.set_color(TERRA) for l in rlights], run_time=0.7)
        done(self)


class B45_PassphraseStays(Scene):
    """Rule five: the passphrase dots are refused by a prompt, a file and a command; they go back to you, who unlock the key yourself."""
    def construct(self):
        you = professor_bear("1x1", 2.2, seed="B45", x=-5.0, y=1.0)
        term = RoundedRectangle(corner_radius=0.1, width=2.0, height=1.0, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-5.0, -1.2, 0])
        tmark = M("$", 40, color=GHOST).move_to([-5.45, -1.2, 0])
        tlab = T("terminal", 38).move_to([-5.0, -2.2, 0])
        key = key_obj(-3.3, -1.3, s=0.55)
        lock = padlock(-3.3, -1.3, s=0.8)
        # three targets
        prompt = VGroup(RoundedRectangle(corner_radius=0.12, width=2.0, height=0.9, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([2.2, 2.0, 0]),
                        Line([1.5, 2.0, 0], [2.3, 2.0, 0], color=GHOST, stroke_width=7))
        plab = T("prompt", 38).move_to([3.5, 2.0, 0], aligned_edge=LEFT)
        plab.move_to([3.6 + plab.width / 2, 2.0, 0])
        page = cert_page(2.2, 0.0, w=1.3, h=1.5)
        flab = T("file", 38)
        flab.move_to([3.6 + flab.width / 2, 0.0, 0])
        cmd = chip("", 2.2, -2.0, w=2.0)
        clab = T("command", 38)
        clab.move_to([3.6 + clab.width / 2, -2.0, 0])
        dots = chip("••••••", -2.2, 1.0, size=40)
        self.play(FadeIn(you), FadeIn(term), FadeIn(tmark), FadeIn(tlab), FadeIn(key), FadeIn(lock), FadeIn(dots), run_time=0.5)
        targets = [(prompt, plab, 2.0, "a prompt"), (page, flab, 0.0, "a file"), (cmd, clab, -2.0, "a command")]
        for (obj, lab, y, ph) in targets:
            hear(self, ph, lead=0.45)
            self.play(FadeIn(obj), FadeIn(lab), run_time=0.2)
            self.play(dots.animate.move_to([-0.3, y, 0]), run_time=0.4)
            self.play(Create(x_mark(0.85, y, r=0.28, w=9)), run_time=0.15)
        # "stop and unlock the key yourself": the dots return to you, the lock opens
        hear(self, "stop and unlock", lead=0.1)
        self.play(dots.animate.move_to([-3.3, 1.0, 0]), run_time=0.6, rate_func=smooth)
        hear(self, "yourself", lead=0.6)
        self.play(dots.animate.move_to([-3.3, -0.55, 0]), run_time=0.4)
        self.play(unlock_anim(lock, rt=0.5), FadeOut(dots), run_time=0.5)
        done(self)


# ═════════════════════════════ PART D — rules 6-7 and Act V (B46 B47 B50 B51 B53 B54) ═════════════════════════════

def pD_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


class B46_OwnAccount(Scene):
    """The certificate names you; it is not for anyone else: a second slot refuses it."""
    def construct(self):
        me = professor_bear("1x1", 2.6, seed="B46y", x=-4.2, y=0.3)
        melab = T("you", 38).move_to([-4.2, -2.1, 0])
        cert = cert_page(-0.4, 0.3, w=1.9, h=2.4)
        cert[2][0].set_color(BAR1).set_stroke(width=10)   # the name line
        clab = T("certificate", 36).move_to([-0.4, -1.65, 0])
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=2.6, height=2.6, color=BAR1, stroke_width=6), num_dashes=28)
        slot.move_to([4.2, 0.3, 0])
        slab = T("someone else", 36).move_to([4.2, -1.75, 0])
        self.play(FadeIn(me), FadeIn(melab), FadeIn(cert), FadeIn(clab), FadeIn(slot), FadeIn(slab), run_time=0.5)
        # "the certificate names you": a leader line ties the certificate to the one portrait
        hear(self, "names you", lead=0.45)
        leader = Line([-1.42, 0.3, 0], [-2.85, 0.3, 0], color=INK, stroke_width=6)
        self.play(Create(leader), run_time=0.4)
        # "run work for anyone else": the certificate tries the other slot and is refused
        hear(self, "run work for", lead=0.1)
        self.play(FadeOut(clab), cert.animate.shift(RIGHT * 2.7), run_time=0.5, rate_func=smooth)
        no = x_mark(4.2, 0.3, r=0.3, w=9)
        self.play(Create(no), run_time=0.25)
        self.play(cert.animate.shift(LEFT * 2.7), run_time=0.5, rate_func=smooth)
        self.play(FadeIn(clab), FadeOut(no), run_time=0.25)
        done(self)


class B47_HomeScratch(Scene):
    """Home is small and recoverable; scratch is large and purged; check the file system page before moving data."""
    def construct(self):
        iso1 = Iso(-4.0, -1.7, 1.3)
        home = home_box(iso1)
        hlab = T("home", 40).move_to([-4.0, -2.7, 0])
        iso2 = Iso(1.6, -2.0, 1.0)
        back, front = scratch_bin(iso2)
        slab = T("scratch", 40).move_to([2.0, -2.8, 0])
        self.play(FadeIn(home), FadeIn(hlab), FadeIn(back), FadeIn(front), FadeIn(slab), run_time=0.5)
        # "Home is small and recoverable": a restore arrow circles back
        hear(self, "is small", lead=0.2)
        self.play(home.animate.scale(1.08), run_time=0.25)
        self.play(home.animate.scale(1 / 1.08), run_time=0.25)
        hear(self, "and recoverable", lead=0.4)
        arc = Arc(radius=0.5, start_angle=PI * 0.35, angle=PI * 1.5, color=INK, stroke_width=8).move_to([-4.0, 1.95, 0])
        arc.add_tip(tip_length=0.28)
        rec = T("recoverable", 36).move_to([-4.0, 2.95, 0])
        self.play(Create(arc), run_time=0.5)
        self.play(FadeIn(rec), run_time=0.25)
        # "Scratch is large": the bin fills with blocks
        hear(self, "is large", lead=0.35)
        blocks = VGroup(*[iso2.box(x, y, 0.0, 0.6, 0.6, 0.5, PAGE_TOP, PAGE_L, PAGE_R) for y in (0.25, 0.95) for x in (0.35, 1.15, 1.95)])
        blocks.set_z_index(1)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.9) for b in blocks], lag_ratio=0.15), run_time=0.6)
        # "it is purged": a sweep clears the bin
        hear(self, "it is purged", lead=0.15)
        sweep = Rectangle(width=0.3, height=2.5, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0.5, -0.3, 0])
        sweep.set_z_index(3)
        self.play(FadeIn(sweep), run_time=0.15)
        self.play(sweep.animate.shift(RIGHT * 3.4), LaggedStart(*[FadeOut(b) for b in blocks], lag_ratio=0.12), run_time=0.8)
        pur = T("purged", 36).move_to([2.0, 1.95, 0])
        self.play(FadeOut(sweep), FadeIn(pur), run_time=0.3)
        # "Check ... file system page before you move data": a 'check first' tag lands on the move arrow
        hear(self, "Check AICR's", lead=0.1)
        mv = Arrow([-2.3, -0.4, 0], [-0.3, -0.4, 0], buff=0, color=INK, stroke_width=8, max_tip_length_to_length_ratio=0.3)
        self.play(Create(mv), run_time=0.4)
        hear(self, "file system", lead=0.4)
        tag = chip("check first", -1.3, 0.55, size=36)
        self.play(FadeIn(tag, shift=DOWN * 0.5), run_time=0.4)
        hear(self, "move data", lead=0.1)
        self.play(Indicate(mv, color=INK, scale_factor=1.15), run_time=0.5)
        done(self)


class B50_ThreeCauses(Scene):
    """Permission denied (publickey): one error, three usual causes; the unlocked-key cause is by far the biggest."""
    def construct(self):
        title = pD_act_title("V · When It Fails")
        err = plaque("Permission denied (publickey)", 0.0, 1.9, w=9.4, h=1.0, size=34)
        self.play(FadeIn(title), FadeIn(err), run_time=0.5)
        hear(self, "permission denied", lead=0.2)
        self.play(err.animate.scale(1.04), run_time=0.25)
        self.play(err.animate.scale(1 / 1.04), run_time=0.25)
        # "one of three things": three dots under the error
        hear(self, "one of three", lead=0.3)
        dots = VGroup(*[Dot([x, 1.0, 0], radius=0.12, color=TERRA) for x in (-0.5, 0.0, 0.5)])
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.2), run_time=0.6)

        def card(lines, x, y, w, h, size):
            sh = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
            cd = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
            lb = T(lines, size).move_to([x, y, 0])
            return VGroup(sh, cd, lb)

        def fan(g):
            g.save_state()
            g.scale(0.25).move_to([0.0, 1.0, 0])
            self.add(g)
            return Restore(g)

        # the three causes land on their spoken words
        cardA = card("Key not unlocked", -3.7, -0.6, 4.2, 2.4, 40)
        hear(self, "key is not", lead=0.25)
        self.play(fan(cardA), FadeOut(dots), run_time=0.6, rate_func=smooth)
        hear(self, "by far the most", lead=0.1)
        most = T("most common", 36).move_to([-3.7, -2.35, 0])
        self.play(FadeIn(most), run_time=0.3)
        cardB = card("Certificate\nexpired or missing", 0.75, -0.35, 3.7, 1.9, 34)
        hear(self, "or the certificate", lead=0.3)
        self.play(fan(cardB), run_time=0.6, rate_func=smooth)
        cardC = card("Wrong\npermissions", 4.45, -0.35, 3.0, 1.9, 34)
        hear(self, "key's permissions", lead=0.5)
        self.play(fan(cardC), run_time=0.6, rate_func=smooth)
        done(self)


class B51_TwinErrors(Scene):
    """Two identical errors, two different causes: ssh-add -l lifts the curtain on the empty agent."""
    def construct(self):
        errs = []
        for x in (-3.2, 3.2):
            errs.append(plaque("Permission denied\n(publickey)", x, 2.45, w=5.2, h=1.5, size=32))
        iso = Iso(-3.0, -1.85, 0.9)
        agent, alights = agent_slab(iso)
        cert = cert_page(3.0, -0.7, w=1.7, h=2.1)
        curts, qs = [], []
        for x in (-3.0, 3.0):
            c = Rectangle(width=3.8, height=2.5, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, -0.7, 0])
            curts.append(c)
            qs.append(T("?", 64).move_to([x, -0.7, 0]))
        curts[0].set_z_index(3); curts[1].set_z_index(3)
        for q in qs:
            q.set_z_index(4)
        self.play(FadeIn(errs[0]), FadeIn(errs[1]), FadeIn(agent), FadeIn(alights), FadeIn(cert),
                  FadeIn(curts[0]), FadeIn(curts[1]), FadeIn(qs[0]), FadeIn(qs[1]), run_time=0.5)
        hear(self, "empty agent", lead=0.2)
        self.play(curts[0].animate.scale(1.05), run_time=0.25)
        self.play(curts[0].animate.scale(1 / 1.05), run_time=0.25)
        hear(self, "expired certificate", lead=0.2)
        self.play(curts[1].animate.scale(1.05), run_time=0.25)
        self.play(curts[1].animate.scale(1 / 1.05), run_time=0.25)
        # "The error is the same": an equals sign between the two
        hear(self, "error is the same", lead=0.5)
        eq = T("=", 64).move_to([0.0, 2.45, 0])
        self.play(FadeIn(eq), run_time=0.3)
        # "check the agent with ssh-add -l": the command chip sweeps across and lifts the left curtain
        hear(self, "with SSH", lead=0.4)
        cmd = chip("ssh-add -l", 4.6, 1.0, mono=True, size=36)
        self.play(FadeIn(cmd), run_time=0.25)
        self.play(cmd.animate.move_to([-3.0, 1.0, 0]), run_time=1.1, rate_func=smooth)
        self.play(FadeOut(qs[0]), curts[0].animate.stretch_to_fit_height(0.06).move_to([-3.0, 0.55, 0]), run_time=0.5)
        tag = chip("agent empty", -3.0, -2.8, size=36)
        self.play(FadeIn(tag, shift=DOWN * 0.4), run_time=0.4)
        done(self)


# ── the shared two-column table (B53 = rows 1-3, B54 = the same table, rows 1-4) ──
pD_COLX, pD_RX = -5.8, -1.1


def pD_y(i):
    return 1.5 - 1.35 * i


def pD_head():
    a = T("You see", 38, bold=True)
    a.move_to([0, 2.95, 0]).align_to([pD_COLX, 0, 0], LEFT)
    b = T("Fix", 38, bold=True)
    b.move_to([0, 2.95, 0]).align_to([pD_RX, 0, 0], LEFT)
    rule = Line([-6.1, 2.5, 0], [6.1, 2.5, 0], color=INK, stroke_width=5)
    return VGroup(a, b, rule)


def pD_left(text, i):
    t = T(text, 34)
    t.move_to([0, pD_y(i), 0]).align_to([pD_COLX, 0, 0], LEFT)
    return t


def pD_rights(items, i):
    out = []
    n = len(items)
    for k, (txt, mono) in enumerate(items):
        t = M(txt, 32) if mono else T(txt, 34)
        dy = 0.0 if n == 1 else (0.3 if k == 0 else -0.3)
        t.move_to([0, pD_y(i) + dy, 0]).align_to([pD_RX, 0, 0], LEFT)
        out.append(t)
    return out


def pD_ring(i):
    """The row marker: a short thick ink bar at the left of the row being spoken (an outline round the row fused the
    whole row into one GATE T text blob; a fill dragged Gate V's contrast under 0.3)."""
    return Rectangle(width=0.14, height=1.0, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([-6.05, pD_y(i), 0])


def pD_table(self, rows):
    """rows = [(index, left text, left cue, [(right text, mono, cue, lead), ...]), ...]; rings the row being spoken."""
    head = pD_head()
    self.play(FadeIn(head), run_time=0.4)
    ring = None
    for i, ltxt, lcue, rights in rows:
        hear(self, lcue, lead=0.3)
        left = pD_left(ltxt, i)
        if ring is None:
            ring = pD_ring(i)
            self.play(Create(ring), FadeIn(left), run_time=0.35)
        else:
            self.play(ring.animate.move_to([-6.05, pD_y(i), 0]), FadeIn(left), run_time=0.35)
        ys = pD_rights([(r[0], r[1]) for r in rights], i)
        arr = Arrow([-1.7, pD_y(i), 0], [-1.35, pD_y(i), 0], buff=0, color=INK, stroke_width=6, max_tip_length_to_length_ratio=0.6)
        for (rtxt, mono, cue, lead), mob in zip(rights, ys):
            hear(self, cue, lead=lead)
            self.play(FadeIn(mob, shift=RIGHT * 0.2), *([FadeIn(arr)] if mob is ys[0] else []), run_time=0.3)


class B53_TableA(Scene):
    """The fix table, part one: hang, changed host key, new host key prompt."""
    def construct(self):
        pD_table(self, [
            (0, "Hangs, wants\npassphrase", "A command that hangs", [("Unlock the key yourself", False, "unlock the key", 0.3)]),
            (1, "Host key verification\nfailed", "Host key verification", [("ssh-keygen -R login.aicr.ai,", True, "Remove the old entry", 0.25), ("connect once", False, "then connect once", 0.25)]),
            (2, "New host key prompt", "A new host key", [("Type yes yourself", False, "type yes", 0.25)]),
        ])
        done(self)


class B54_TableB(Scene):
    """The fix table, part two: bad option, timeout, idle drops, empty agent after restart."""
    def construct(self):
        pD_table(self, [
            (0, "Bad configuration\noption", "Bad configuration option", [("IgnoreUnknown UseKeychain", True, "add ignore unknown", 0.25)]),
            (1, "Connection\ntimed out", "Connection timed out", [("Other network, no VPN needed", False, "try another network", 0.25)]),
            (2, "Drops when idle", "Drops when idle", [("ServerAliveInterval 60", True, "server alive interval", 0.3)]),
            (3, "Empty after restart", "Empty after a restart", [("ssh-add again", True, "SSH add again", 0.25)]),
        ])
        done(self)


for _cls in (B10_KeyAndCert, B21_UnlockOnce, B22_AgentAnswers, B11_UserName, B13_FourFiles, B14_HumanSteps, B20_NobodyAnswers, B31_FailFast, B34_EmptyOnPurpose, B37_VaultRefills, B38_NoVault, B40_YouApprove, B41_ReadOnly, B42_LoginCap, B43_AskFirst, B44_KeyStays, B45_PassphraseStays, B46_OwnAccount, B47_HomeScratch, B50_ThreeCauses, B51_TwinErrors, B53_TableA, B54_TableB):
    _cls.play = ST.play
