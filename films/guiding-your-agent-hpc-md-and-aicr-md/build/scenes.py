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
_ASR = {"BOPEN": [["Research", 0.0], ["Computing", 0.38], ["on", 0.78], ["Explorer", 1.0], ["and", 1.46], ["AICR,", 1.68], ["Guiding", 2.96], ["Your", 3.1], ["Agent", 3.3], ["HPC", 3.68], [".md", 4.36], ["and", 5.14], ["AICR", 5.46], [".md,", 6.22], ["why", 7.48], ["an", 7.62], ["agent", 7.78], ["on", 8.04], ["a", 8.2], ["shared", 8.36], ["cluster", 8.54], ["needs", 8.98], ["written", 9.26], ["rules", 9.58], ["and", 10.0], ["a", 10.34], ["walk", 10.44], ["through", 10.62], ["the", 10.82], ["two", 10.96], ["rule", 11.14], ["files", 11.36], ["that", 11.7], ["give", 12.0], ["them.", 12.18]], "BIDEA": [["Hallo,", 0.74], ["this", 1.26], ["is", 1.36], ["Liam", 1.58], ["in", 1.88], ["for", 2.14], ["Bear,", 2.3], ["first", 2.96], ["a", 3.1], ["correction.", 3.28], ["To", 4.02], ["let", 4.1], ["an", 4.24], ["agent", 4.4], ["work", 4.58], ["on", 4.82], ["a", 4.98], ["cluster,", 5.14], ["you", 5.56], ["do", 5.6], ["not", 5.7], ["just", 5.84], ["say", 6.0], ["run", 6.24], ["my", 6.48], ["job,", 6.7], ["the", 7.16], ["cluster", 7.3], ["is", 7.54], ["shared", 7.76], ["and", 8.08], ["the", 8.3], ["agent", 8.4], ["is", 8.7], ["fast", 8.86], ["and", 9.18], ["literal.", 9.44], ["You", 10.2], ["give", 10.34], ["it", 10.44], ["two", 10.56], ["short", 10.72], ["rule", 11.0], ["files", 11.24], ["first", 11.64], ["and", 11.98], ["you", 12.28], ["point", 12.4], ["it", 12.62], ["at", 12.76], ["them.", 12.9]], "BDEFS": [["Five", 0.0], ["terms,", 0.3], ["a", 0.88], ["rule", 0.9], ["file,", 1.08], ["a", 1.6], ["plain", 1.62], ["text", 1.84], ["file", 2.14], ["the", 2.42], ["agent", 2.58], ["reads", 2.82], ["before", 3.1], ["it", 3.46], ["acts.", 3.6], ["A", 4.2], ["hard", 4.3], ["never,", 4.48], ["a", 5.0], ["rule", 5.06], ["with", 5.24], ["no", 5.42], ["exceptions.", 5.64], ["A", 6.54], ["login", 6.66], ["node,", 6.88], ["the", 7.38], ["shared", 7.48], ["computer", 7.72], ["you", 8.12], ["land", 8.32], ["on", 8.52], ["when", 8.72], ["you", 8.86], ["connect.", 8.98], ["A", 9.66], ["slurm", 9.74], ["job,", 10.16], ["your", 10.56], ["request", 10.64], ["for", 10.96], ["compute", 11.2], ["node", 11.48], ["written", 11.8], ["as", 12.06], ["a", 12.24], ["script.", 12.4], ["And", 12.96], ["fair", 13.1], ["share,", 13.28], ["the", 13.7], ["priority", 13.8], ["you", 14.14], ["lose", 14.4], ["when", 14.6], ["you", 14.8], ["ask", 14.92], ["for", 15.12], ["more", 15.32], ["than", 15.5], ["you", 15.66], ["use.", 15.8]], "B10": [["An", 0.0], ["agent", 0.14], ["is", 0.4], ["fast,", 0.62], ["literal,", 1.16], ["and", 1.7], ["never", 1.74], ["tired.", 1.98], ["That", 2.8], ["is", 2.88], ["the", 3.02], ["good", 3.16], ["news.", 3.32], ["On", 3.96], ["a", 4.06], ["shared", 4.18], ["cluster", 4.4], ["it", 4.78], ["is", 4.98], ["also", 5.1], ["the", 5.34], ["risk.", 5.48], ["It", 6.16], ["will", 6.24], ["do", 6.34], ["exactly", 6.48], ["what", 6.84], ["you", 7.14], ["asked", 7.28], ["as", 7.64], ["many", 7.86], ["times", 8.04], ["as", 8.36], ["you", 8.56], ["asked", 8.68], ["and", 9.0], ["it", 9.24], ["will", 9.32], ["not", 9.44], ["feel", 9.62], ["the", 9.84], ["cost", 10.0], ["to", 10.18], ["anyone", 10.36], ["else.", 10.58]], "B11": [["Most", 0.0], ["trouble", 0.18], ["on", 0.42], ["a", 0.66], ["cluster", 0.78], ["is", 1.04], ["not", 1.28], ["hard", 1.52], ["computer", 1.82], ["science.", 2.16], ["It", 3.0], ["is", 3.04], ["work", 3.14], ["on", 3.36], ["the", 3.56], ["wrong", 3.68], ["machine.", 3.88], ["It", 4.58], ["is", 4.66], ["a", 4.76], ["request", 4.86], ["far", 5.16], ["bigger", 5.44], ["than", 5.68], ["the", 5.94], ["job,", 6.04], ["and", 6.68], ["it", 6.76], ["is", 6.86], ["a", 6.98], ["check", 7.1], ["that", 7.34], ["passes", 7.58], ["when", 7.94], ["it", 8.18], ["should", 8.3], ["fail.", 8.44], ["These", 9.42], ["are", 9.6], ["quiet", 9.74], ["failures,", 10.06], ["nothing", 10.8], ["crashes,", 10.96], ["and", 11.64], ["you", 11.74], ["find", 11.84], ["out", 12.06], ["later.", 12.26]], "B12": [["So", 0.0], ["there", 0.14], ["are", 0.26], ["two", 0.38], ["files.", 0.54], ["HPC", 1.46], [".md", 1.84], ["holds", 2.54], ["the", 2.88], ["rules", 3.12], ["for", 3.32], ["any", 3.58], ["shared", 3.76], ["cluster,", 4.04], ["written", 4.76], ["for", 4.86], ["Northeastern's", 5.12], ["Explorer.", 5.84], ["AICR", 7.12], [".md", 7.64], ["builds", 8.16], ["on", 8.48], ["it", 8.72], ["and", 8.84], ["adds", 9.0], ["what", 9.24], ["is", 9.4], ["different", 9.52], ["or", 9.84], ["stricter", 10.02], ["on", 10.3], ["the", 10.56], ["AICR", 10.7], ["GPU", 11.36], ["cluster.", 11.74], ["Read", 12.68], ["the", 12.82], ["first,", 12.98], ["then", 13.5], ["the", 13.6], ["second.", 13.76]], "B13": [["You", 0.0], ["do", 0.12], ["not", 0.2], ["paste", 0.38], ["either", 0.64], ["file", 0.86], ["into", 1.18], ["your", 1.4], ["instructions.", 1.56], ["You", 2.68], ["put", 2.7], ["one", 2.86], ["line", 3.06], ["in", 3.3], ["your", 3.44], ["claw", 3.58], [".md", 3.8], ["or", 4.5], ["agents", 4.98], [".md", 5.36], ["and", 6.06], ["the", 6.58], ["agent", 6.7], ["reads", 7.0], ["the", 7.3], ["files", 7.56], ["when", 7.9], ["the", 8.16], ["work", 8.26], ["is", 8.44], ["cluster", 8.66], ["work.", 8.98], ["Here", 9.92], ["are", 10.04], ["the", 10.16], ["two", 10.26], ["lines", 10.44], ["copied", 10.88], ["from", 11.26], ["the", 11.52], ["files", 11.68], ["themselves.", 11.98]], "B20": [["Open", 0.0], ["the", 0.26], ["file", 0.38], ["hpc", 0.62], [".md", 1.18], ["and", 1.94], ["the", 2.2], ["first", 2.32], ["thing", 2.48], ["you", 2.72], ["see", 2.84], ["is", 3.0], ["not", 3.14], ["a", 3.34], ["rule.", 3.48], ["It", 4.1], ["is", 4.16], ["a", 4.26], ["short", 4.42], ["summary,", 4.6], ["what", 5.3], ["it", 5.4], ["is,", 5.52], ["why", 5.82], ["it", 6.0], ["exists,", 6.1], ["what", 6.62], ["was", 6.74], ["found,", 6.86], ["and", 7.4], ["what", 7.44], ["is", 7.54], ["not", 7.64], ["verified.", 7.84], ["Then", 8.86], ["a", 8.96], ["line", 9.08], ["that", 9.24], ["says", 9.42], ["everything", 9.6], ["below", 9.94], ["is", 10.38], ["for", 10.62], ["the", 10.8], ["agent.", 10.92], ["Then", 11.62], ["14", 11.74], ["numbered", 12.16], ["sections,", 12.48], ["0", 13.32], ["to", 13.52], ["13,", 13.7], ["and", 14.38], ["an", 14.5], ["honest", 14.66], ["appendix", 14.94], ["of", 15.34], ["conflicts.", 15.64]], "B21": [["Section", 0.0], ["0", 0.34], ["is", 0.64], ["the", 0.94], ["prime", 1.1], ["directive.", 1.32], ["The", 2.34], ["agent", 2.36], ["does", 2.5], ["the", 2.74], ["pipeline", 2.9], ["work,", 3.24], ["inspect,", 3.82], ["measure,", 4.34], ["size,", 4.78], ["check,", 5.18], ["keep", 5.6], ["records.", 5.72], ["The", 6.7], ["researcher", 6.8], ["keeps", 7.12], ["the", 7.44], ["judgment", 7.66], ["what", 7.92], ["to", 8.26], ["spend,", 8.38], ["who", 8.74], ["gets", 8.84], ["access,", 9.02], ["and", 9.6], ["anything", 9.66], ["that", 9.88], ["cannot", 10.16], ["be", 10.42], ["undone.", 10.64], ["Look", 11.3], ["before", 11.4], ["you", 11.68], ["act,", 11.82], ["measure", 12.26], ["before", 12.44], ["you", 12.76], ["change,", 12.94], ["ask", 13.54], ["before", 13.7], ["you", 14.0], ["spend,", 14.16], ["delete,", 14.62], ["or", 15.1], ["share.", 15.16]], "B22": [["Section", 0.0], ["1", 0.24], ["is", 0.62], ["the", 0.8], ["list", 0.94], ["the", 1.1], ["agent", 1.28], ["checks", 1.54], ["before", 1.84], ["every", 2.16], ["command.", 2.48], ["Never", 3.24], ["run", 3.32], ["computation", 3.56], ["on", 4.18], ["a", 4.46], ["login", 4.6], ["node.", 4.74], ["Never", 5.42], ["ask", 5.56], ["for", 5.84], ["read", 6.08], ["or", 6.34], ["print", 6.58], ["a", 6.76], ["password", 6.88], ["or", 7.22], ["a", 7.44], ["key.", 7.54], ["Never", 8.26], ["delete", 8.44], ["without", 8.72], ["listing", 8.98], ["what", 9.3], ["will", 9.46], ["go", 9.6], ["and", 9.76], ["getting", 9.9], ["a", 10.06], ["yes.", 10.24], ["Never", 10.72], ["submit", 10.88], ["a", 11.2], ["job", 11.34], ["until", 11.62], ["you", 11.86], ["have", 11.98], ["confirmed", 12.1], ["what", 12.46], ["it", 12.68], ["asks", 12.76], ["for.", 13.0], ["Never", 13.58], ["cancel", 13.74], ["with", 14.14], ["scancel", 14.32], ["-u.", 14.82], ["And", 15.74], ["never", 15.88], ["invent", 16.1], ["a", 16.4], ["flag,", 16.6], ["a", 17.18], ["module,", 17.18], ["or", 17.74], ["a", 17.94], ["limit.", 18.02]], "B23": [["Notice", 0.0], ["that", 0.24], ["every", 0.5], ["never", 0.78], ["comes", 0.98], ["with", 1.3], ["a", 1.52], ["because.", 1.64], ["A", 2.42], ["rule", 2.52], ["the", 2.72], ["agent", 2.94], ["understands", 3.24], ["is", 3.8], ["a", 4.14], ["rule", 4.32], ["it", 4.48], ["can", 4.68], ["apply", 4.82], ["to", 5.14], ["a", 5.34], ["case", 5.48], ["the", 5.66], ["file", 5.86], ["never", 6.16], ["listed.", 6.44], ["And", 7.48], ["some", 7.56], ["rules", 7.8], ["are", 8.1], ["labeled", 8.32], ["house", 8.6], ["rule", 8.92], ["because", 9.28], ["they", 9.78], ["are", 9.98], ["our", 10.14], ["judgment,", 10.3], ["not", 10.96], ["the", 11.06], ["cluster's", 11.24], ["policy.", 11.66]], "B24": [["Section", 0.0], ["2", 0.28], ["is", 0.62], ["before", 0.82], ["the", 1.08], ["first", 1.22], ["command.", 1.44], ["If", 2.4], ["a", 2.44], ["read", 2.56], ["-only", 2.7], ["command", 2.92], ["can", 3.34], ["answer", 3.56], ["a", 3.8], ["question,", 3.94], ["the", 4.48], ["agent", 4.48], ["runs", 4.74], ["it", 5.08], ["instead", 5.32], ["of", 5.62], ["asking", 5.76], ["you,", 6.04], ["Who", 6.72], ["am", 6.84], ["I?", 6.94], ["Where", 7.3], ["am", 7.44], ["I?", 7.58], ["Which", 7.88], ["groups?", 8.04], ["What", 8.48], ["is", 8.54], ["free?", 8.68], ["It", 9.34], ["asks", 9.46], ["only", 9.66], ["what", 9.98], ["only", 10.16], ["you", 10.34], ["can", 10.52], ["answer,", 10.64], ["your", 11.18], ["access,", 11.3], ["what", 11.92], ["it", 12.0], ["may", 12.1], ["submit,", 12.22], ["whether", 12.78], ["the", 12.9], ["data", 13.08], ["is", 13.26], ["restricted,", 13.48], ["and", 14.22], ["what", 14.32], ["you", 14.46], ["are", 14.6], ["trying", 14.72], ["to", 14.94], ["do.", 15.12]], "B25": [["Section", 0.0], ["4", 0.28], ["stops", 0.68], ["the", 1.0], ["agent", 1.24], ["asking", 1.44], ["for", 1.8], ["more", 2.1], ["than", 2.28], ["it", 2.42], ["needs,", 2.54], ["is", 3.06], ["parallel", 3.14], ["even", 3.5], ["the", 3.84], ["answer.", 4.04], ["In", 4.8], ["research", 4.92], ["computing's", 5.22], ["own", 5.9], ["benchmark,", 6.04], ["1", 6.8], ["core", 6.94], ["took", 7.12], ["250", 7.36], ["seconds,", 8.02], ["8", 8.88], ["cores", 9.04], ["took", 9.3], ["29,", 9.56], ["12", 10.44], ["cores", 10.74], ["took", 11.04], ["33,", 11.26], ["slower", 12.06], ["than", 12.24], ["8.", 12.52], ["Never", 13.08], ["promise", 13.24], ["that", 13.56], ["n", 13.84], ["cores", 14.0], ["is", 14.28], ["n", 14.5], ["times", 14.7], ["faster.", 15.0]], "B26": [["Section", 0.0], ["5", 0.28], ["every", 0.7], ["script", 1.1], ["states", 1.4], ["its", 1.72], ["numbers,", 1.98], ["partition,", 2.74], ["time,", 3.3], ["memory,", 3.74], ["cores,", 4.2], ["a", 4.66], ["name,", 4.7], ["and", 5.08], ["a", 5.12], ["log", 5.24], ["file.", 5.42], ["Time", 6.48], ["is", 6.62], ["the", 6.8], ["expected", 6.92], ["runtime", 7.32], ["plus", 7.82], ["about", 8.16], ["20%,", 8.42], ["never", 9.16], ["the", 9.48], ["maximum", 9.66], ["just", 10.0], ["to", 10.32], ["be", 10.5], ["safe.", 10.62], ["And", 11.34], ["memory", 11.42], ["is", 11.62], ["computer", 11.94], ["memory,", 12.28], ["not", 13.04], ["GPU", 13.14], ["memory.", 13.56]], "B27": [["Section", 0.0], ["6", 0.32], ["is", 0.64], ["GPUs,", 0.92], ["never", 1.78], ["trust", 1.92], ["the", 2.22], ["allocation.", 2.38], ["A", 3.56], ["job", 3.7], ["that", 3.92], ["work", 4.12], ["may", 4.32], ["have", 4.52], ["run", 4.62], ["on", 4.82], ["the", 4.98], ["processor", 5.1], ["with", 5.44], ["no", 5.72], ["error,", 5.94], ["so", 6.58], ["every", 6.82], ["GPU", 7.1], ["script", 7.46], ["proves", 7.86], ["the", 8.22], ["GPU", 8.46], ["is", 8.9], ["there", 9.1], ["before", 9.34], ["the", 9.64], ["expensive", 9.8], ["part,", 10.18], ["the", 11.04], ["device", 11.08], ["name,", 11.36], ["the", 11.88], ["memory,", 11.9], ["and", 12.54], ["a", 12.64], ["number", 12.76], ["that", 12.86], ["travels", 13.12], ["to", 13.42], ["the", 13.7], ["GPU", 13.82], ["and", 14.16], ["back.", 14.46]], "B28": [["Section", 0.0], ["7", 0.3], ["is", 0.66], ["where", 0.9], ["files", 1.1], ["live,", 1.44], ["code", 2.16], ["and", 2.38], ["environments", 2.62], ["in", 3.12], ["home,", 3.46], ["temporary", 4.54], ["job", 4.54], ["data", 4.92], ["in", 5.26], ["Scratch", 5.48], ["which", 5.9], ["is", 6.16], ["wiped", 6.32], ["on", 6.58], ["the", 6.78], ["first", 6.9], ["Tuesday", 7.14], ["of", 7.5], ["every", 7.7], ["month,", 7.92], ["anything", 8.54], ["you", 8.76], ["keep", 9.0], ["in", 9.18], ["projects", 9.36], ["and", 9.82], ["the", 10.22], ["agent", 10.34], ["never", 10.62], ["keeps", 10.9], ["the", 11.18], ["only", 11.4], ["copy", 11.62], ["of", 11.96], ["anything", 12.2], ["in", 12.46], ["Scratch.", 12.72]], "B29": [["Section", 0.0], ["8", 0.3], ["is", 0.5], ["software", 0.68], ["in", 1.08], ["order,", 1.28], ["first", 1.76], ["a", 1.9], ["module,", 2.1], ["then", 2.64], ["conda,", 2.78], ["then", 3.52], ["a", 3.6], ["container", 3.7], ["built", 4.08], ["on", 4.32], ["your", 4.52], ["own", 4.62], ["machine,", 4.72], ["then", 5.34], ["a", 5.46], ["source", 5.62], ["build,", 5.78], ["and", 6.48], ["a", 6.56], ["tool", 6.68], ["like", 6.82], ["SPAC", 7.04], ["only", 7.32], ["last", 7.52], ["because", 7.9], ["each", 8.26], ["step", 8.46], ["down", 8.74], ["costs", 9.04], ["more", 9.34], ["to", 9.64], ["keep.", 9.82], ["Before", 10.4], ["installing", 10.6], ["anything,", 11.02], ["the", 11.66], ["agent", 11.68], ["checks", 11.9], ["whether", 12.24], ["a", 12.48], ["module", 12.7], ["already", 13.04], ["exists.", 13.38]], "B30": [["Section", 0.0], ["9", 0.28], ["is", 0.62], ["the", 0.82], ["record", 0.96], ["every", 1.22], ["job", 1.56], ["leaves", 1.86], ["behind,", 2.14], ["the", 3.02], ["job", 3.1], ["and", 3.34], ["node", 3.52], ["when", 3.78], ["it", 4.06], ["started,", 4.16], ["the", 4.92], ["git", 4.96], ["commit", 5.1], ["it", 5.38], ["ran", 5.52], ["from,", 5.76], ["the", 6.36], ["exact", 6.4], ["command,", 6.66], ["the", 7.26], ["parameters,", 7.26], ["the", 8.0], ["seeds,", 8.02], ["the", 8.54], ["inputs,", 8.54], ["the", 9.24], ["software", 9.34], ["and", 9.7], ["the", 10.02], ["hardware", 10.12], ["it", 10.46], ["really", 10.62], ["used,", 10.9], ["12", 11.6], ["items", 11.74], ["so", 12.12], ["a", 12.46], ["stranger", 12.58], ["can", 12.88], ["rerun", 13.2], ["it.", 13.54]], "B31": [["Section", 0.0], ["10", 0.28], ["is", 0.62], ["about", 0.82], ["being", 1.02], ["an", 1.2], ["agent", 1.36], ["on", 1.62], ["the", 1.84], ["cluster.", 1.98], ["The", 2.76], ["researcher", 2.8], ["creates", 3.12], ["and", 3.6], ["unlocks", 3.84], ["the", 4.16], ["key,", 4.46], ["never", 4.94], ["the", 5.06], ["agent.", 5.28], ["If", 5.98], ["a", 6.08], ["command", 6.18], ["prompts,", 6.48], ["hangs,", 6.94], ["or", 7.58], ["says", 7.62], ["permission", 7.82], ["denied,", 8.12], ["the", 8.8], ["agent", 8.82], ["stops", 9.08], ["and", 9.42], ["reports", 9.68], ["the", 10.06], ["exact", 10.3], ["error.", 10.58], ["It", 11.48], ["does", 11.62], ["not", 11.74], ["retry", 11.96], ["in", 12.38], ["a", 12.54], ["loop,", 12.64], ["and", 12.98], ["it", 13.04], ["never", 13.16], ["asks", 13.36], ["for", 13.7], ["a", 13.96], ["password.", 14.04]], "B32": [["Section", 0.0], ["12", 0.3], ["is", 0.66], ["a", 0.92], ["list", 1.04], ["of", 1.12], ["things", 1.34], ["the", 1.52], ["training", 1.74], ["slides", 1.98], ["get", 2.36], ["wrong,", 2.68], ["a", 3.32], ["comment", 3.46], ["after", 3.74], ["a", 4.06], ["line", 4.2], ["continuation", 4.42], ["which", 5.0], ["breaks", 5.42], ["the", 5.7], ["command,", 5.92], ["a", 6.8], ["partition", 6.9], ["called", 7.2], ["compute", 7.62], ["which", 8.02], ["does", 8.3], ["not", 8.5], ["exist,", 8.72], ["a", 9.44], ["sample", 9.54], ["script", 9.86], ["with", 10.2], ["no", 10.44], ["time", 10.7], ["and", 11.0], ["no", 11.22], ["memory,", 11.44], ["the", 12.14], ["agent", 12.26], ["is", 12.5], ["told", 12.76], ["not", 13.0], ["to", 13.32], ["copy", 13.52], ["them.", 13.76]], "B33": [["And", 0.0], ["the", 0.12], ["appendix", 0.24], ["is", 0.52], ["the", 0.8], ["honest", 0.92], ["part,", 1.16], ["where", 1.8], ["the", 1.9], ["sources", 2.04], ["disagree,", 2.26], ["the", 2.98], ["file", 3.06], ["says", 3.36], ["so", 3.64], ["and", 3.9], ["picks", 4.06], ["the", 4.26], ["safe", 4.48], ["reading.", 4.7], ["The", 5.58], ["scratch", 5.66], ["quota,", 5.94], ["50", 6.56], ["terabytes", 6.76], ["in", 7.22], ["the", 7.46], ["slides,", 7.58], ["20", 8.16], ["on", 8.28], ["the", 8.5], ["policy", 8.62], ["page.", 8.94], ["So", 9.68], ["the", 9.78], ["agent", 9.9], ["is", 10.12], ["told", 10.34], ["never", 10.56], ["to", 10.82], ["quote", 11.06], ["a", 11.24], ["number.", 11.4], ["Rules", 12.26], ["marked", 12.26], ["house", 12.64], ["rule", 12.9], ["or", 13.24], ["inferred", 13.52], ["are", 13.9], ["our", 14.14], ["judgment,", 14.28], ["not", 14.86], ["policy.", 14.98]], "B40": [["Now", 0.0], ["AICR", 0.24], [".md,", 1.0], ["it", 1.98], ["builds", 2.1], ["on", 2.3], ["the", 2.48], ["first", 2.58], ["file", 2.78], ["and", 3.12], ["where", 3.34], ["the", 3.44], ["two", 3.58], ["differ", 3.76], ["it", 4.08], ["wins", 4.3], ["on", 4.52], ["AICR.", 4.74], ["Explorers", 6.18], ["hosts,", 6.36], ["partitions,", 6.98], ["storage", 7.68], ["rules", 7.86], ["and", 8.22], ["module", 8.48], ["setup", 8.84], ["do", 9.16], ["not", 9.44], ["carry", 9.64], ["over.", 9.9], ["The", 10.64], ["first", 10.76], ["rule", 10.94], ["of", 11.18], ["the", 11.32], ["second", 11.42], ["file,", 11.62], ["assume", 12.2], ["AICR", 12.44], ["is", 13.3], ["not", 13.46], ["Explorer.", 13.68]], "B41": [["AICR", 0.0], ["differs", 0.7], ["in", 0.88], ["ways", 1.14], ["that", 1.28], ["byte,", 1.54], ["your", 2.08], ["username", 2.18], ["is", 2.5], ["built", 2.82], ["differently,", 3.0], ["there", 3.76], ["is", 3.92], ["no", 4.0], ["password", 4.2], ["only", 4.68], ["a", 4.98], ["key", 5.2], ["and", 5.4], ["a", 5.6], ["certificate,", 5.7], ["the", 6.5], ["partition", 6.62], ["decides", 6.94], ["which", 7.42], ["GPU", 7.72], ["you", 8.1], ["get,", 8.36], ["idle", 9.24], ["GPUs", 9.24], ["are", 9.68], ["cancelled", 9.92], ["automatically", 10.28], ["and", 10.94], ["scratch", 11.48], ["is", 11.74], ["purged", 11.96], ["after", 12.36], ["30", 12.62], ["days", 12.96], ["with", 13.22], ["no", 13.52], ["offsite", 13.76], ["backup.", 14.2]], "B42": [["AICR's", 0.0], ["own", 0.8], ["Nevers", 1.0], ["are", 1.34], ["specific.", 1.52], ["Never", 2.5], ["run", 2.62], ["SSH", 2.82], ["add", 3.22], ["-D", 3.68], ["because", 4.58], ["it", 4.92], ["empties", 5.1], ["every", 5.42], ["key.", 5.74], ["Never", 6.54], ["source", 6.72], ["activate", 7.0], ["in", 7.48], ["a", 7.66], ["batch", 7.78], ["script", 7.94], ["because", 8.3], ["a", 8.66], ["real", 8.8], ["job", 9.06], ["died", 9.4], ["on", 9.7], ["it.", 9.92], ["And", 10.36], ["never", 10.46], ["copy", 10.66], ["the", 10.96], ["workshop's", 11.16], ["GPU", 11.74], ["check", 12.02], ["because", 12.44], ["it", 12.82], ["exits", 12.94], ["zero", 13.22], ["even", 13.66], ["when", 14.0], ["the", 14.16], ["GPU", 14.3], ["is", 14.6], ["missing.", 14.9]], "B43": [["Section", 0.0], ["5", 0.3], ["is", 0.68], ["a", 0.96], ["template", 1.1], ["built", 1.36], ["from", 1.64], ["flags", 1.9], ["that", 2.26], ["real", 2.56], ["completed", 2.82], ["jobs", 3.28], ["used.", 3.66], ["Every", 4.48], ["setting", 4.64], ["is", 4.94], ["stated.", 5.14], ["The", 5.98], ["environment", 6.06], ["is", 6.44], ["added", 6.78], ["to", 7.04], ["the", 7.24], ["path", 7.36], ["not", 7.68], ["activated,", 8.0], ["and", 8.94], ["the", 9.04], ["script", 9.16], ["fails", 9.36], ["itself", 9.74], ["on", 10.16], ["purpose", 10.48], ["if", 10.78], ["the", 11.2], ["GPU", 11.36], ["is", 11.66], ["not", 12.02], ["visible.", 12.26]], "B44": [["After", 0.0], ["every", 0.24], ["batch", 0.56], ["job,", 0.8], ["the", 1.3], ["agent", 1.32], ["runs", 1.52], ["job", 1.9], ["stats,", 2.22], ["a", 2.82], ["command", 2.82], ["that", 3.08], ["exists", 3.28], ["only", 3.58], ["on", 3.96], ["AICR.", 4.14], ["It's", 5.34], ["real", 5.5], ["example,", 5.7], ["a", 6.42], ["job", 6.54], ["that", 6.76], ["asked", 6.94], ["for", 7.14], ["8", 7.36], ["hours", 7.56], ["and", 7.88], ["ran", 8.1], ["55", 8.32], ["minutes", 8.86], ["with", 9.26], ["the", 9.54], ["GPU", 9.7], ["80", 10.02], ["%", 10.46], ["busy.", 10.84], ["The", 11.86], ["targets", 11.96], ["are", 12.22], ["written", 12.46], ["down,", 12.66], ["over", 13.3], ["70", 13.4], ["%", 13.8], ["GPU", 14.22], ["use", 14.56], ["is", 14.9], ["acceptable,", 15.06], ["and", 15.94], ["under", 16.04], ["50", 16.2], ["is", 16.52], ["a", 16.76], ["problem.", 16.9]], "B45": [["Section", 0.0], ["11", 0.28], ["is", 0.6], ["lessons", 0.9], ["from", 1.18], ["real", 1.48], ["AICR", 1.74], ["runs", 2.52], ["and", 2.8], ["they", 3.1], ["are", 3.2], ["all", 3.28], ["quiet", 3.48], ["failures,", 3.78], ["a", 4.7], ["checkpoint", 4.86], ["that", 5.24], ["loaded", 5.5], ["without", 5.76], ["error", 6.1], ["and", 6.4], ["left", 6.64], ["random", 6.82], ["weights,", 7.3], ["an", 7.88], ["input", 7.94], ["clip", 8.2], ["so", 8.42], ["quiet", 8.68], ["it", 9.0], ["produced", 9.16], ["silence,", 9.4], ["a", 10.32], ["cached", 10.42], ["file", 10.66], ["served", 11.06], ["under", 11.38], ["the", 11.58], ["same", 11.7], ["path", 11.92], ["after", 12.24], ["it", 12.52], ["was", 12.64], ["replaced.", 12.74], ["Each", 13.52], ["became", 13.7], ["a", 14.02], ["rule,", 14.2], ["prove", 14.68], ["the", 14.86], ["weights", 15.0], ["loaded,", 15.22], ["gate", 15.94], ["every", 16.02], ["input", 16.3], ["with", 16.6], ["a", 16.76], ["number,", 16.88], ["give", 17.34], ["a", 17.42], ["replaced", 17.56], ["file", 17.9], ["a", 18.24], ["new", 18.44], ["name.", 18.52]], "B46": [["And", 0.0], ["before", 0.12], ["any", 0.34], ["GPU", 0.56], ["job,", 0.88], ["the", 1.54], ["agent", 1.58], ["asks", 1.8], ["only", 2.16], ["what", 2.56], ["only", 2.74], ["you", 2.96], ["can", 3.16], ["answer,", 3.3], ["your", 4.12], ["username", 4.26], ["and", 4.54], ["account,", 4.9], ["whether", 5.5], ["any", 5.62], ["data", 5.88], ["is", 6.14], ["restricted,", 6.34], ["whether", 7.32], ["it", 7.46], ["may", 7.62], ["submit", 7.76], ["for", 8.06], ["you,", 8.3], ["and", 8.74], ["what", 8.9], ["success", 9.04], ["looks", 9.42], ["like.", 9.7]], "B50": [["Rules", 0.0], ["also", 0.26], ["come", 0.58], ["from", 0.86], ["mistakes.", 1.06], ["While", 1.98], ["making", 2.04], ["the", 2.24], ["film", 2.42], ["about", 2.58], ["rendering", 2.82], ["on", 3.14], ["Explorer,", 3.4], ["the", 4.06], ["agent", 4.1], ["listed", 4.42], ["every", 4.74], ["folder", 5.12], ["under", 5.44], ["projects", 5.72], ["that", 6.22], ["showed", 6.64], ["other", 6.92], ["people's", 7.16], ["names.", 7.64], ["Then", 8.3], ["it", 8.4], ["ran", 8.52], ["a", 8.7], ["disk", 8.86], ["usage", 9.02], ["command", 9.3], ["over", 9.72], ["a", 9.98], ["shared", 10.14], ["folder", 10.34], ["and", 10.78], ["it", 11.0], ["hung.", 11.1], ["Neither", 11.92], ["was", 11.92], ["forbidden", 12.18], ["by", 12.54], ["the", 12.84], ["file.", 12.98], ["Now", 13.6], ["both", 13.7], ["are.", 13.92]], "B51": [["Another,", 0.0], ["a", 0.44], ["job", 0.54], ["script", 0.78], ["began", 1.1], ["with", 1.5], ["Module", 1.76], ["Purge.", 2.06], ["That", 2.82], ["removed", 2.9], ["the", 3.18], ["module", 3.42], ["that", 3.74], ["sets", 3.98], ["the", 4.2], ["cluster's", 4.46], ["proxy", 4.88], ["so", 5.22], ["every", 5.5], ["download", 5.76], ["timed", 6.2], ["out.", 6.52], ["A", 7.26], ["one", 7.38], ["-line", 7.56], ["test", 7.78], ["showed", 8.08], ["the", 8.32], ["network", 8.46], ["was", 8.72], ["fine.", 8.96], ["Now", 9.74], ["the", 9.86], ["file", 10.02], ["says,", 10.28], ["Module", 10.96], ["Purge", 11.14], ["can", 11.56], ["remove", 11.72], ["your", 12.02], ["network,", 12.18], ["so", 12.72], ["load", 12.88], ["that", 13.1], ["module", 13.32], ["again.", 13.72]], "B52": [["And", 0.0], ["a", 0.14], ["third,", 0.24], ["the", 0.68], ["scripts", 0.76], ["assumed", 0.98], ["scratch", 1.38], ["belonged", 1.74], ["to", 2.16], ["the", 2.38], ["user,", 2.48], ["on", 3.1], ["this", 3.26], ["account", 3.4], ["it", 3.72], ["belonged", 3.88], ["to", 4.12], ["root", 4.38], ["and", 4.56], ["refused", 4.78], ["every", 5.18], ["write,", 5.46], ["the", 6.04], ["agent", 6.1], ["had", 6.36], ["checked", 6.58], ["with", 6.82], ["a", 7.02], ["read", 7.12], ["first", 7.28], ["which", 7.58], ["is", 7.88], ["exactly", 8.04], ["what", 8.42], ["the", 8.74], ["file", 8.88], ["asks,", 9.14], ["now", 10.1], ["the", 10.32], ["file", 10.52], ["says", 10.76], ["why,", 11.0], ["test", 11.68], ["before", 11.8], ["you", 12.1], ["write.", 12.28]], "B60": [["To", 0.0], ["use", 0.12], ["them,", 0.34], ["put", 0.66], ["both", 0.78], ["files", 1.02], ["where", 1.36], ["your", 1.66], ["agent", 1.8], ["can", 2.12], ["read", 2.36], ["them.", 2.54], ["Add", 3.34], ["the", 3.44], ["one", 3.56], ["line", 3.72], ["to", 3.98], ["your", 4.18], ["claw", 4.34], [".md", 4.52], ["or", 5.28], ["agents", 5.72], [".md,", 6.14], ["and", 7.3], ["at", 7.44], ["the", 7.54], ["start", 7.68], ["of", 7.88], ["cluster", 8.02], ["work,", 8.22], ["ask", 8.82], ["the", 8.92], ["agent", 9.12], ["to", 9.42], ["say", 9.62], ["back", 9.82], ["which", 10.08], ["rules", 10.26], ["apply", 10.6], ["before", 11.04], ["it", 11.6], ["runs", 11.72], ["anything.", 11.96]], "B61": [["The", 0.0], ["files", 0.1], ["do", 0.38], ["not", 0.6], ["replace", 0.74], ["judgment.", 1.12], ["Nothing", 2.08], ["in", 2.18], ["any", 2.4], ["policy", 2.54], ["page", 2.88], ["says", 3.3], ["whether", 3.58], ["automated", 3.86], ["agents", 4.32], ["are", 4.78], ["allowed", 4.98], ["on", 5.22], ["Explorer", 5.46], ["or", 5.86], ["AICR,", 6.16], ["so", 7.06], ["the", 7.3], ["files", 7.42], ["say", 7.7], ["to", 7.96], ["ask", 8.1], ["research", 8.3], ["computing", 8.68], ["once.", 9.16], ["And", 10.54], ["every", 10.6], ["claim", 10.86], ["is", 11.1], ["labeled", 11.3], ["by", 11.56], ["how", 11.86], ["we", 12.06], ["know", 12.24], ["it", 12.42], ["from", 12.62], ["the", 12.86], ["sources", 13.02], ["from", 13.38], ["a", 13.82], ["real", 13.94], ["run", 14.16], ["or", 14.44], ["our", 14.82], ["own", 14.96], ["judgment.", 15.18]], "BVDT": [["Let's", 0.0], ["recap", 0.7], ["with", 0.94], ["Claude.", 1.16], ["An", 1.68], ["agent", 1.72], ["is", 1.96], ["fast", 2.14], ["and", 2.44], ["literal,", 2.68], ["so", 3.14], ["a", 3.22], ["shared", 3.38], ["cluster", 3.56], ["needs", 3.92], ["written", 4.18], ["rules.", 4.46], ["HPC", 5.46], [".md", 5.76], ["holds", 6.3], ["the", 6.6], ["general", 6.84], ["rules.", 7.08], ["Never", 7.76], ["compute", 7.9], ["on", 8.24], ["a", 8.38], ["login", 8.56], ["node.", 8.68], ["Ask", 9.14], ["before", 9.28], ["you", 9.58], ["spend.", 9.72], ["Verify", 10.34], ["the", 10.34], ["GPU.", 10.68], ["AICR", 11.74], [".md", 12.22], ["adds", 12.68], ["what", 12.96], ["is", 13.08], ["stricter.", 13.2], ["No", 13.72], ["idle", 13.84], ["GPUs.", 14.18], ["No", 14.86], ["source", 14.98], ["activate", 15.22], ["and", 15.64], ["scratch", 15.9], ["is", 16.2], ["purged.", 16.44], ["Every", 17.24], ["rule", 17.42], ["comes", 17.66], ["with", 17.92], ["a", 18.12], ["because.", 18.2], ["Real", 18.9], ["mistakes", 18.96], ["become", 19.46], ["new", 19.88], ["rules.", 20.1], ["And", 21.2], ["one", 21.32], ["line", 21.5], ["in", 21.78], ["your", 21.9], ["instructions", 22.02], ["points", 22.56], ["the", 23.08], ["agent", 23.34], ["at", 23.66], ["both", 23.88], ["files.", 24.08]], "BHTF": [["Your", 0.0], ["turn,", 0.14], ["paste", 0.52], ["this", 0.7], ["into", 0.9], ["Claude.", 1.12], ["Read", 1.6], ["the", 1.68], ["files", 1.84], ["hpc", 2.06], [".md", 2.66], ["and", 3.3], ["aicr", 3.58], [".md", 4.24], ["completely.", 4.7], ["Do", 5.52], ["not", 5.62], ["run", 5.76], ["anything", 5.94], ["on", 6.22], ["any", 6.4], ["cluster.", 6.56], ["Then", 7.32], ["tell", 7.48], ["me", 7.64], ["the", 7.76], ["five", 7.9], ["hard", 8.1], ["nevers", 8.38], ["that", 8.76], ["matter", 8.86], ["most", 9.06], ["for", 9.3], ["my", 9.52], ["task,", 9.68], ["which", 10.1], ["questions", 10.26], ["you", 10.64], ["would", 10.86], ["ask", 10.96], ["me", 11.16], ["before", 11.34], ["your", 11.52], ["first", 11.68], ["command", 11.9], ["and", 12.28], ["anything", 12.56], ["in", 12.8], ["the", 12.94], ["files", 13.04], ["that", 13.34], ["you", 13.54], ["could", 13.66], ["not", 13.8], ["confirm.", 13.98], ["My", 14.88], ["task,", 15.04], ["then", 15.52], ["describe", 15.64], ["your", 16.0], ["job", 16.2], ["in", 16.46], ["one", 16.64], ["sentence.", 16.8], ["Then", 17.52], ["check", 17.64], ["two", 17.86], ["things", 18.1], ["yourself.", 18.38], ["Did", 19.08], ["Claude", 19.16], ["run", 19.42], ["nothing", 19.68], ["on", 20.0], ["a", 20.18], ["cluster?", 20.28], ["And", 21.3], ["did", 21.42], ["it", 21.54], ["say", 21.68], ["what", 21.92], ["it", 22.14], ["could", 22.28], ["not", 22.44], ["confirm?", 22.68]], "BOUT": [["Guiding", 0.0], ["Your", 0.34], ["Agent,", 0.5], ["HPC", 1.04], [".md", 1.52], ["and", 2.2], ["AICR", 2.54], [".md,", 3.34], ["at", 4.36], ["Nick", 4.46], ["Baer", 4.72], ["Brown.", 5.0]], "B59": [["Where", 0.0], ["to", 0.12], ["find", 0.24], ["them,", 0.52], ["both", 0.82], ["files", 0.98], ["are", 1.28], ["free", 1.48], ["on", 1.68], ["GitHub", 1.88], ["in", 2.18], ["the", 2.6], ["HPC", 2.7], ["-AICR", 3.24], ["repository", 4.3], ["inside", 4.78], ["the", 5.56], ["Skills", 5.8], ["folder.", 6.02], ["HPC", 7.32], [".md", 7.84], ["is", 8.36], ["in", 8.64], ["the", 8.76], ["HPC", 8.86], ["folder", 9.36], ["and", 9.84], ["AICR", 10.24], [".md", 10.98], ["is", 11.52], ["in", 11.76], ["the", 11.92], ["AICR", 12.04], ["folder.", 12.78], ["The", 13.42], ["link", 13.5], ["is", 13.66], ["in", 13.9], ["the", 14.04], ["description.", 14.14]]}


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


# ═════════════════════════════ PART A — B10 B11 B12 B21 ═════════════════════════════
def pA_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pA_stopwatch(x, y, r=0.6):
    face = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    knob = Rectangle(width=0.26, height=0.16, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + r + 0.12, 0])
    hand = Line([x, y, 0], [x, y + r * 0.7, 0], color=INK, stroke_width=7)
    hub = Dot([x, y, 0], radius=0.07, color=INK)
    g = VGroup(knob, face, hand, hub)
    g.hand, g.cx, g.cy = hand, x, y
    return g


class B10_FastAndLiteral(Scene):
    """A fast agent fires many job boxes; they all pile into one shared rack and crowd out everyone else's dots."""
    def construct(self):
        title = pA_act_title("I · Why An Agent Needs Rules")
        claude = logo_chip("claude", -4.9, 1.5)
        sw = pA_stopwatch(-2.6, 1.5)
        self.play(FadeIn(title), FadeIn(claude), run_time=0.4)
        # a stack of small job boxes waits at the left
        iso = Iso(-4.9, -3.0, 0.5)
        stack = VGroup(*[job_box(iso, (i % 3) * 0.9, (i // 3) * 0.9, 0, s=0.7) for i in range(6)])
        # "fast": the stopwatch ticks and the boxes start to fly out
        hear(self, "fast", lead=0.1)
        self.play(FadeIn(sw), FadeIn(stack), run_time=0.3)
        self.play(Rotate(sw.hand, angle=-2 * PI, about_point=[sw.cx, sw.cy, 0]), run_time=1.0, rate_func=linear)
        hear(self, "never tired", lead=0.2)
        self.play(Rotate(sw.hand, angle=-2 * PI, about_point=[sw.cx, sw.cy, 0]), run_time=0.8, rate_func=linear)
        # "shared cluster": racks appear, each with a different count of other people's dots
        hear(self, "On a shared cluster", lead=0.25)
        racks, dots, rows = [], [], []
        spots = [(1.9, -2.5, 1), (4.5, -2.5, 2), (1.9, -0.1, 3), (4.5, -0.1, 1)]
        for (cx, cy, n) in spots:
            ri = Iso(cx, cy, 0.8)
            st, lt = explorer_rack(ri)
            ds = VGroup(*[Dot([cx + 1.3, cy + 0.15 + 0.3 * k, 0], radius=0.11, color=TERRA) for k in range(n)])
            racks.append(VGroup(st, lt)); dots.append(ds)
        clab = T("shared cluster", 38).move_to([3.5, 2.5, 0])
        self.play(*[FadeIn(r) for r in racks], *[FadeIn(d) for d in dots], FadeIn(clab), run_time=0.7)
        # "exactly what you asked": a volley of boxes crosses to the target rack and lands
        hear(self, "exactly what you asked", lead=0.3)
        # re-use the stack: 3 boxes leave it, fly right
        leave = VGroup(*stack[:3])
        self.play(leave.animate.shift(RIGHT * 5.4 + UP * 0.6), run_time=0.8, rate_func=smooth)
        self.play(FadeOut(leave, scale=0.5), run_time=0.2)
        hear(self, "as many times", lead=0.3)
        rest = VGroup(*stack[3:])
        self.play(rest.animate.shift(RIGHT * 5.4 + UP * 0.6), run_time=0.8, rate_func=smooth)
        self.play(FadeOut(rest, scale=0.5), run_time=0.2)
        # "will not feel the cost": the target rack's dots crowd out the others, which dim
        hear(self, "not feel the cost", lead=0.3)
        crowd = VGroup(*[Dot([1.9 + 1.3 + 0.3 * (k % 2), -2.5 + 0.15 + 0.3 * (k // 2), 0], radius=0.11, color=TERRA) for k in range(1, 8)])
        self.play(FadeIn(crowd), *[r.animate.set_opacity(0.3) for r in racks[1:]], *[d.animate.set_opacity(0.3) for d in dots[1:]], run_time=0.8)
        done(self)


class B11_ThreeQuietFailures(Scene):
    """Three cards fan out; each shows one quiet failure; a 'no error' tag lands on all three."""
    def construct(self):
        xs = [-4.15, 0.0, 4.15]
        cards = [paper(0, 0.5, w=3.5, h=3.1) for _ in xs]
        for c, x in zip(cards, xs):
            c.shift(RIGHT * 0)
        # start stacked in the centre, then fan out
        self.play(FadeIn(cards[1]), run_time=0.3)
        self.add(cards[0], cards[2]); cards[0].move_to([0, 0.5, 0]); cards[2].move_to([0, 0.5, 0])
        self.bring_to_front(cards[1])
        self.play(cards[0].animate.move_to([xs[0], 0.5, 0]), cards[2].animate.move_to([xs[2], 0.5, 0]), run_time=0.7, rate_func=smooth)
        # card 1: wrong machine
        hear(self, "wrong machine", lead=0.5)
        iso1 = Iso(xs[0] - 0.3, -0.55, 0.62)
        r1, l1 = explorer_rack(iso1)
        door = Rectangle(width=0.55, height=0.9, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([xs[0] + 0.78, 0.15, 0])
        job1 = job_box(iso1, 0.35, 0.35, 0.88 + 0.08, s=0.6)
        lab1 = M("login node", 32).move_to([xs[0], -1.45, 0])
        self.play(FadeIn(r1), FadeIn(l1), FadeIn(door), FadeIn(lab1), run_time=0.4)
        self.play(FadeIn(job1, shift=DOWN * 0.4), run_time=0.3)
        # card 2: wrong size
        hear(self, "bigger than the job", lead=0.9)
        bar = Rectangle(width=2.7, height=0.55, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([xs[1], 0.5, 0])
        lab2 = M("8 h for 25 min", 32).move_to([xs[1], -1.45, 0])
        self.play(Create(bar), FadeIn(lab2), run_time=0.4)
        fill = Rectangle(width=0.45, height=0.55, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([xs[1] - 1.35 + 0.225, 0.5, 0])
        self.play(GrowFromEdge(fill, LEFT), run_time=0.4)
        # card 3: passing check, no CUDA
        hear(self, "a check that passes", lead=0.5)
        iso3 = Iso(xs[2] - 0.3, -0.55, 0.62)
        r3, l3 = explorer_rack(iso3)
        slot = iso3.quad([(0, 0, 0.46), (0, 1.3, 0.46), (0, 1.3, 0.84), (0, 0, 0.84)], GHOST, stroke=INK, sw=3)
        lab3 = M("exit 0, no CUDA", 32).move_to([xs[2], -1.45, 0])
        self.play(FadeIn(r3), FadeIn(l3), FadeIn(slot), FadeIn(lab3), run_time=0.4)
        ck = check(xs[2] + 1.0, 1.35, s=0.3, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.4)
        # "quiet failures": 'no error' lands on all three
        hear(self, "quiet failures", lead=0.2)
        tags = [chip("no error", x, -2.5, size=34) for x in xs]
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in tags], lag_ratio=0.4), run_time=1.0)
        hear(self, "nothing crashes", lead=0.2)
        self.play(*[Indicate(t, color=INK, scale_factor=1.08) for t in tags], run_time=0.6)
        done(self)


class B12_TwoFiles(Scene):
    """HPC.md lands first; AICR.md lands on it and builds on it; read the first, then the second."""
    def construct(self):
        lo = paper(-2.2, -1.0, w=2.8, h=3.2)
        up = paper(-1.3, 0.1, w=2.8, h=3.2)
        lo_l = scribbles_on(lo, n=4)
        up_l = scribbles_on(up, n=4)
        ghost = DashedVMobject(Rectangle(width=2.8, height=3.2, color=BAR1, stroke_width=5).move_to([-1.3, 0.1, 0]), num_dashes=28)
        self.play(FadeIn(lo), FadeIn(lo_l), run_time=0.3)
        hear(self, "two files", lead=0.3)
        self.play(Create(ghost), run_time=0.4)
        hear(self, "HPC", lead=0.3)
        hpc = M("HPC.md", 42).move_to([3.4, -1.0, 0])
        self.play(FadeIn(hpc), run_time=0.3)
        hear(self, "any shared cluster", lead=0.3)
        hsub = T("any shared cluster (Explorer)", 34).move_to([3.4, -1.7, 0])
        self.play(FadeIn(hsub), run_time=0.4)
        # AICR.md page lands on it (before the clip midpoint)
        hear(self, "AICR", lead=0.55)
        self.play(FadeOut(ghost), FadeIn(up, shift=DOWN * 0.8), FadeIn(up_l, shift=DOWN * 0.8), run_time=0.3)
        hear(self, "builds on", lead=0.0)
        aicr = M("AICR.md", 42).move_to([3.4, 2.0, 0])
        self.play(FadeIn(aicr), run_time=0.25)
        arr = Arrow([3.4, 0.7, 0], [3.4, -0.3, 0], color=INK, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.5)
        blab = T("builds on", 36).move_to([5.0, 0.2, 0])
        self.play(Create(arr), FadeIn(blab), run_time=0.4)
        hear(self, "stricter", lead=0.2)
        asub = T("stricter on AICR", 34).move_to([3.4, 1.35, 0])
        self.play(FadeIn(asub), run_time=0.4)
        hear(self, "Read the first", lead=0.2)
        first = chip("first", -5.2, -1.0, size=34)
        self.play(FadeIn(first, shift=RIGHT * 0.3), run_time=0.3)
        hear(self, "then the second", lead=0.2)
        then = chip("then", -5.2, 0.4, size=34)
        self.play(FadeIn(then, shift=RIGHT * 0.3), run_time=0.3)
        done(self)


class B21_PrimeDirective(Scene):
    """Agent column does the pipeline work; the researcher keeps spend, access and what cannot be undone."""
    def construct(self):
        rule = Line([-6.0, -2.3, 0], [6.0, -2.3, 0], color=INK, stroke_width=12)
        div = DashedLine([0, 3.0, 0], [0, -1.8, 0], color=BAR1, stroke_width=6, dash_length=0.25)
        self.play(Create(rule), Create(div), run_time=0.5)
        hear(self, "The agent does", lead=0.3)
        claude = logo_chip("claude", -4.7, 2.2)
        alab = T("agent", 44).move_to([-3.1, 2.2, 0])
        self.play(FadeIn(claude), FadeIn(alab), run_time=0.4)
        verbs = []
        for v, ph, y in (("inspect", "inspect", 0.9), ("measure", "measure", 0.1), ("size", "size", -0.7), ("record", "records", -1.5)):
            hear(self, ph, lead=0.2)
            tick = check(-5.5, y, s=0.2, w=8)
            lab = T(v, 46)
            lab.move_to([-4.8 + lab.width / 2, y, 0])
            self.play(Create(tick), FadeIn(lab), run_time=0.3)
            verbs.append(VGroup(tick, lab))
        hear(self, "The researcher", lead=0.3)
        you = professor_bear("1x1", 1.7, seed="B21", x=3.3, y=2.1)
        ylab = T("you", 44).move_to([4.8, 2.1, 0])
        self.play(FadeIn(you), FadeIn(ylab), run_time=0.4)
        hear(self, "spend", lead=0.1)
        c1 = chip("spend", 3.7, 0.4, size=44)
        self.play(FadeIn(c1, shift=LEFT * 0.3), run_time=0.25)
        hear(self, "access", lead=0.15)
        c2 = chip("access", 3.7, -0.55, size=44)
        self.play(FadeIn(c2, shift=LEFT * 0.3), run_time=0.25)
        hear(self, "cannot be undone", lead=0.5)
        c3 = chip("cannot undo", 3.7, -1.5, size=44)
        self.play(FadeIn(c3, shift=LEFT * 0.3), run_time=0.25)
        hear(self, "Look before", lead=0.2)
        p1 = T("look first", 44).move_to([-4.0, -2.9, 0])
        self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.3)
        hear(self, "measure before", lead=0.2)
        p2 = T("measure first", 44).move_to([0.0, -2.9, 0])
        self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.3)
        hear(self, "ask before", lead=0.2)
        p3 = T("ask first", 44).move_to([4.0, -2.9, 0])
        self.play(FadeIn(p3, shift=UP * 0.2), run_time=0.3)
        done(self)


# ═════════════════════════════ PART B — B22 B25 B28 B29 ═════════════════════════════

def pB_left(mob, x0, y):
    return mob.move_to([x0 + mob.width / 2, y, 0])


class B22_HardNevers(Scene):
    """Six hard nevers land as table rows, each with a cross."""
    def construct(self):
        top = Line([-5.9, 3.05, 0], [5.9, 3.05, 0], color=INK, stroke_width=5)
        self.play(Create(top), run_time=0.4)
        items = [("compute on a login node", "run computation"), ("password or key", "ask for read"),
                 ("delete without a list", "delete without"), ("submit unconfirmed", "submit a job"),
                 ("scancel -u", "cancel with"), ("invent a flag", "invent a flag")]
        ys = [2.55 - 1.0 * i for i in range(6)]
        for (txt, cue), y in zip(items, ys):
            hear(self, cue, lead=0.5)
            p = pill(-5.0, y, 1.9, h=0.7, fill=BOX_L)
            nv = T("never", 36, bold=True).move_to([-5.0, y, 0])
            it = pB_left(M(txt, 32), -3.5, y)
            sep = Line([-5.9, y - 0.5, 0], [5.9, y - 0.5, 0], color=GHOST, stroke_width=3)
            xm = x_mark(5.2, y, r=0.25, w=9)
            self.play(FadeIn(p), FadeIn(nv), FadeIn(it), Create(sep), run_time=0.35)
            self.play(Create(xm), run_time=0.2)
        done(self)


class B25_TwelveSlowerThanEight(Scene):
    """Bars grow on the spoken core counts; the 12-core bar is ringed: slower than 8."""
    def construct(self):
        data = [(1, 250.7), (2, 116.8), (4, 58.1), (8, 29.4), (12, 33.4), (16, 25.2), (20, 20.2)]
        base, k = -2.2, 4.0 / 250.7
        xs = [-4.8 + 1.6 * i for i in range(7)]
        axis = Line([-5.8, base, 0], [5.8, base, 0], color=INK, stroke_width=5)
        unit = T("seconds", 34).move_to([-5.0, 3.1, 0])
        self.play(Create(axis), FadeIn(unit), run_time=0.4)
        bars, tops, labs = [], [], []
        for (c, s), x in zip(data, xs):
            h = s * k
            b = Rectangle(width=1.0, height=h, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
            b.move_to([x, base + h / 2, 0])
            v = T(f"{s} s", 32).move_to([x, base + h + 0.4, 0])
            l = T(f"{c} core" if c == 1 else (f"{c} cores"), 32).move_to([x, base - 0.45, 0])
            bars.append(b); tops.append(v); labs.append(l)

        def grow(i, rt=0.5):
            return [GrowFromEdge(bars[i], DOWN), FadeIn(tops[i]), FadeIn(labs[i])]
        hear(self, "1 core took", lead=0.2)
        self.play(*grow(0), run_time=0.5)
        hear(self, "250 seconds", lead=0.0)
        self.play(*grow(1), *grow(2), run_time=0.45)
        hear(self, "8 cores took", lead=0.2)
        self.play(*grow(3), run_time=0.5)
        hear(self, "12 cores took", lead=0.2)
        self.play(*grow(4), run_time=0.5)
        hear(self, "slower than 8", lead=0.1)
        ring = Rectangle(width=1.5, height=bars[4].height + 0.5 + 0.9, stroke_color=TERRA, stroke_width=7, fill_opacity=0)
        ring.move_to([xs[4], base + (bars[4].height + 0.5 + 0.9) / 2 - 0.1, 0])
        tag = T("slower than 8", 34).move_to([xs[4], base + 3.0, 0])
        self.play(Create(ring), FadeIn(tag), run_time=0.45)
        hear(self, "promise that", lead=0.2)
        self.play(*grow(5), run_time=0.45)
        hear(self, "times faster", lead=0.3)
        self.play(*grow(6), run_time=0.45)
        done(self)


class B28_WhereFilesLive(Scene):
    """home / scratch / projects; the only copy leaves scratch for projects before the first-Tuesday sweep."""
    def construct(self):
        ih = Iso(-4.5, -1.3, 0.9)
        home = home_box(ih)
        hn = T("home", 40).move_to([-4.5, -2.7, 0])
        hc1 = T("code", 34).move_to([-4.5, 1.7, 0]); hc2 = T("environments", 34).move_to([-4.5, 1.25, 0])
        isx = Iso(-0.5, -1.7, 0.9)
        back, front = scratch_bin(isx)
        sn = T("scratch", 40).move_to([0.2, -2.9, 0])
        junk1 = job_box(isx, 0.3, 0.3, 0.0, s=0.55); junk2 = job_box(isx, 1.5, 0.9, 0.0, s=0.55)
        only = job_box(isx, 1.4, 0.2, 0.0, s=0.55)
        olab = T("only copy", 34).move_to([1.2, 1.1, 0])
        self.play(FadeIn(home), FadeIn(hn), run_time=0.4)
        hear(self, "code and environments", lead=0.2)
        self.play(FadeIn(hc1), FadeIn(hc2), run_time=0.3)
        hear(self, "temporary job data", lead=0.3)
        self.play(FadeIn(back), FadeIn(front), FadeIn(sn), FadeIn(junk1), FadeIn(junk2), run_time=0.4)
        hear(self, "wiped on", lead=0.9)
        cal = paper(-1.0, 2.2, w=1.5, h=1.5)
        grid = VGroup(*[Line([-1.55, 2.2 + 0.4 - 0.3 * i, 0], [-0.45, 2.2 + 0.4 - 0.3 * i, 0], color=BAR3, stroke_width=4) for i in range(4)])
        cdot = Dot([-1.3, 2.2 - 0.05, 0], radius=0.09, color=TERRA)
        ft = T("first Tuesday", 34).move_to([1.2, 2.2, 0])
        self.play(FadeIn(cal), Create(grid), FadeIn(cdot), run_time=0.4)
        self.play(FadeIn(ft), run_time=0.25)
        hear(self, "keep in projects", lead=0.5)
        ip = Iso(4.5, -1.3, 0.9)
        proj = home_box(ip)
        pn = T("projects", 40).move_to([4.5, -2.7, 0])
        pc = T("long-term", 34).move_to([4.5, 2.0, 0])
        ck = check(5.7, 1.6, s=0.28, color=INK)
        self.play(FadeIn(proj), FadeIn(pn), FadeIn(pc), Create(ck), run_time=0.45)
        hear(self, "never keeps the only", lead=0.6)
        self.play(FadeIn(only), FadeIn(olab), run_time=0.3)
        grp = VGroup(only, olab)
        path = VMobject()
        c0 = grp.get_center()
        path.set_points_smoothly([c0, [2.5, 1.2, 0], [4.0, 1.0, 0], [4.5, 0.0, 0]])
        self.play(MoveAlongPath(grp, path), run_time=1.0, rate_func=smooth)
        hear(self, "of anything in", lead=0.3)
        broom = Rectangle(width=0.3, height=1.6, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.9, -1.0, 0])
        self.play(FadeIn(broom), run_time=0.2)
        self.play(broom.animate.shift(RIGHT * 3.6), AnimationGroup(FadeOut(junk1), FadeOut(junk2), lag_ratio=0.6), run_time=0.7, rate_func=smooth)
        self.play(FadeOut(broom), run_time=0.25)
        done(self)


class B29_InstallLadder(Scene):
    """Five rungs, cost bar widening; the agent checks module avail on the top rung."""
    def construct(self):
        names = ["module", "conda", "container (built at home)", "source build", "Spack / EasyBuild (last)"]
        cues = ["first a module", "then conda", "a container", "a source build", "a tool like"]
        ys = [2.5 - 1.2 * i for i in range(5)]
        rails = VGroup(Line([-5.9, 3.0, 0], [-5.9, -3.0, 0], color=INK, stroke_width=7),
                       Line([-4.7, 3.0, 0], [-4.7, -3.0, 0], color=INK, stroke_width=7))
        self.play(Create(rails), run_time=0.4)
        labs, bars = [], []
        for i, (n, c, y) in enumerate(zip(names, cues, ys)):
            hear(self, c, lead=0.6 if i == 4 else 0.35)
            rung = Line([-5.9, y, 0], [-4.7, y, 0], color=INK, stroke_width=7)
            lab = pB_left(T(n, 36), -4.3, y)
            w = 0.7 * (i + 1)
            bar = Rectangle(width=w, height=0.5, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3)
            bar.move_to([1.2 + w / 2, y, 0])
            self.play(Create(rung), FadeIn(lab), GrowFromEdge(bar, LEFT), run_time=0.45)
            labs.append(lab); bars.append(bar)
        hear(self, "costs more", lead=0.3)
        ct = T("cost", 36).move_to([2.2, 3.05, 0])
        self.play(FadeIn(ct), run_time=0.3)
        hear(self, "Before installing", lead=0.2)
        claude = logo_chip("claude", 5.2, 2.7, h=1.0)
        self.play(FadeIn(claude), run_time=0.3)
        lens = Circle(radius=0.3, stroke_color=INK, stroke_width=7, fill_color=PAGE_TOP, fill_opacity=0.9).move_to([3.6, 2.5, 0])
        handle = Line([3.82, 2.28, 0], [4.1, 2.0, 0], color=INK, stroke_width=9)
        mag = VGroup(lens, handle)
        cmd = M("module avail", 32).move_to([4.2, 1.95, 0])
        self.play(FadeIn(mag), FadeIn(cmd), run_time=0.3)
        hear(self, "whether a module", lead=0.2)
        self.play(mag.animate.shift(LEFT * 5.4), run_time=1.2, rate_func=smooth)
        self.play(Indicate(labs[0], color=TERRA, scale_factor=1.1), run_time=0.5)
        done(self)


# ═════════════════════════════ PART C — B32 B33 B40 B41 ═════════════════════════════

def pC_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pC_card(x, y, w=4.0, h=2.9):
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    sheet = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(shadow, sheet)


def pC_tag(x, y):
    """The 'do not copy' tag: a white pill, a terracotta dot, ink text."""
    p = pill(x, y, 3.0, h=0.8)
    sh = pill(x + 0.08, y - 0.08, 3.0, h=0.8, fill=BOX_L)
    dot = Dot([x - 1.2, y, 0], radius=0.11, color=TERRA)
    lab = T("do not copy", 34).move_to([x + 0.2, y, 0])
    return VGroup(sh, p, dot, lab)


class B32_DoNotCopy(Scene):
    """Three wrong slide lines get a 'do not copy' tag; the Claude chip nods past each and takes none."""
    def construct(self):
        ys = [1.9, 0.0, -1.9]
        cx, L0 = -1.1, -3.65
        claude = logo_chip("claude", -5.3, ys[0])
        self.play(FadeIn(claude), run_time=0.4)

        def nod(y):
            self.play(claude.animate.move_to([-5.3, y, 0]), run_time=0.35, rate_func=smooth)
            self.play(claude.animate.shift(RIGHT * 0.3), run_time=0.15)
            self.play(claude.animate.shift(LEFT * 0.3), run_time=0.15)

        def left(m, y):
            return m.move_to([L0 + m.width / 2, y, 0])
        # card 1: the line cut at the backslash
        hear(self, "a comment after a line", lead=0.3)
        c1 = pC_card(cx, ys[0], w=5.6, h=1.6)
        l1 = left(M("python train.py \\", 32), ys[0] + 0.35)
        l2 = left(M("# CHANGE", 32), ys[0] - 0.4)
        cut = Line([L0, ys[0] - 0.02, 0], [L0 + 4.2, ys[0] - 0.02, 0], color=BAR1, stroke_width=4)
        self.play(FadeIn(c1), run_time=0.3)
        self.play(FadeIn(l1), FadeIn(l2), Create(cut), run_time=0.4)
        hear(self, "which breaks the command", lead=0.2)
        t1 = pC_tag(4.2, ys[0])
        self.play(GrowFromCenter(t1), run_time=0.35)
        nod(ys[0])
        # card 2: a partition that is not there
        hear(self, "a partition called compute", lead=0.4)
        c2 = pC_card(cx, ys[1], w=5.6, h=1.6)
        p2 = left(M("--partition=compute", 32), ys[1] + 0.35)
        slab = DashedVMobject(Rectangle(width=3.2, height=0.5, color=BAR1, stroke_width=4)).move_to([L0 + 1.6, ys[1] - 0.4, 0])
        self.play(FadeIn(c2), FadeIn(p2), Create(slab), run_time=0.4)
        hear(self, "which does not exist", lead=0.3)
        t2 = pC_tag(4.2, ys[1])
        self.play(GrowFromCenter(t2), run_time=0.35)
        nod(ys[1])
        # card 3: no time, no memory
        hear(self, "a sample script", lead=0.3)
        c3 = pC_card(cx, ys[2], w=5.6, h=1.6)
        p3 = left(M("sbatch", 32), ys[2] + 0.35)
        s1 = DashedVMobject(Rectangle(width=0.9, height=0.5, color=BAR1, stroke_width=4)).move_to([-3.35, ys[2] - 0.4, 0])
        s2 = DashedVMobject(Rectangle(width=0.9, height=0.5, color=BAR1, stroke_width=4)).move_to([-0.6, ys[2] - 0.4, 0])
        n1 = M("--time", 32).move_to([-2.0, ys[2] - 0.4, 0])
        n2 = M("--mem", 32).move_to([0.8, ys[2] - 0.4, 0])
        self.play(FadeIn(c3), FadeIn(p3), Create(s1), Create(s2), FadeIn(n1), FadeIn(n2), run_time=0.4)
        hear(self, "no time and no memory", lead=-0.3)
        t3 = pC_tag(4.2, ys[2])
        self.play(GrowFromCenter(t3), run_time=0.35)
        hear(self, "told not to copy", lead=0.3)
        nod(ys[2])
        done(self)


def pC_stamp(text, x, y, w=2.8):
    sh = pill(x + 0.08, y - 0.08, w, h=0.8, fill=BOX_L)
    p = pill(x, y, w, h=0.8)
    dot = Dot([x - w / 2 + 0.3, y, 0], radius=0.1, color=TERRA)
    lab = T(text, 34).move_to([x + 0.15, y, 0])
    return VGroup(sh, p, dot, lab)


class B33_HonestAppendix(Scene):
    """Two sources disagree on the scratch quota; the file refuses to quote either; two stamps mark the judgment rules."""
    def construct(self):
        ax, bx, py = -4.85, -1.5, 0.9
        pa = paper(ax, py, w=2.7, h=2.8)
        pb = paper(bx, py, w=2.7, h=2.8)
        qa = T("scratch quota", 32).move_to([ax, py + 0.85, 0])
        qb = T("scratch quota", 32).move_to([bx, py + 0.85, 0])
        la = T("slides", 34).move_to([ax, -0.9, 0])
        lb = T("policy page", 34).move_to([bx, -0.9, 0])
        self.play(FadeIn(pa), FadeIn(pb), FadeIn(qa), FadeIn(qb), FadeIn(la), FadeIn(lb), run_time=0.5)
        # "the file says so": the rule line draws
        hear(self, "the file says so", lead=0.3)
        rule = Line([-5.8, -2.4, 0], [-1.6, -2.4, 0], color=BAR2, stroke_width=8)
        self.play(Create(rule), run_time=0.6)
        # 50 TB then 20 TB
        hear(self, "50 terabytes", lead=0.25)
        n50 = T("50 TB", 60, bold=True).move_to([ax, py - 0.3, 0])
        self.play(FadeIn(n50, shift=UP * 0.2), run_time=0.35)
        hear(self, "20 on the", lead=0.15)
        n20 = T("20 TB", 60, bold=True).move_to([bx, py - 0.3, 0])
        self.play(FadeIn(n20, shift=UP * 0.2), run_time=0.35)
        # not-equal sign between the pages
        hear(self, "policy page", lead=0.1)
        neq = VGroup(Line([-3.4, py + 0.25, 0], [-2.95, py + 0.25, 0], color=INK, stroke_width=9),
                     Line([-3.4, py - 0.15, 0], [-2.95, py - 0.15, 0], color=INK, stroke_width=9),
                     Line([-3.05, py + 0.5, 0], [-3.3, py - 0.4, 0], color=INK, stroke_width=9))
        self.play(Create(neq), run_time=0.4)
        # the third card: never quote a number
        hear(self, "never to quote a number", lead=0.8)
        c3 = pC_card(3.4, py, w=4.6, h=2.8)
        t1 = T("the file:", 36).move_to([3.4, py + 0.55, 0])
        t2 = T("never quote a number", 34, bold=True).move_to([3.4, py - 0.3, 0])
        self.play(FadeIn(c3), FadeIn(t1), FadeIn(t2), run_time=0.5)
        # stamps beside a rule line
        hear(self, "house rule", lead=0.2)
        s1 = pC_stamp("house rule", 0.7, -2.4)
        self.play(GrowFromCenter(s1), run_time=0.35)
        hear(self, "or inferred", lead=0.0)
        s2 = pC_stamp("inferred", 3.9, -2.4, w=2.6)
        self.play(GrowFromCenter(s2), run_time=0.35)
        done(self)


class B40_AssumeNotExplorer(Scene):
    """AICR.md sits on top of HPC.md and wins; four Explorer items slide toward the AICR rack and bounce off."""
    def construct(self):
        hpc = paper(-4.7, 0.1, w=2.4, h=3.0, fill=GHOST)
        hl = VGroup(*[Line([-5.7, 0.9 - 0.45 * i, 0], [-3.7 - (0.5 if i == 2 else 0), 0.9 - 0.45 * i, 0], color=BAR2, stroke_width=7) for i in range(3)])
        hlab = M("HPC.md", 32).move_to([-4.7, -1.75, 0])
        stack, lights = aicr_rack(Iso(3.8, -2.0, 1.1))
        rlab = T("AICR", 40).move_to([4.2, -3.05, 0])
        title = pC_act_title("III · What AICR.md Changes")
        self.play(FadeIn(title), FadeIn(hpc), FadeIn(hl), FadeIn(hlab), FadeIn(stack), FadeIn(lights), FadeIn(rlab), run_time=0.5)
        # "AICR.md ... it wins on AICR": the white page lands on top, then lights
        hear(self, "AICR", lead=0.2)
        aic = paper(-3.9, 0.5, w=2.4, h=3.0)
        al = VGroup(*[Line([-4.9, 1.3 - 0.45 * i, 0], [-2.9 - (0.5 if i == 2 else 0), 1.3 - 0.45 * i, 0], color=INK, stroke_width=6) for i in range(3)])
        alab = M("AICR.md", 32).move_to([-3.9, 2.5, 0])
        page = VGroup(aic, al)
        self.play(FadeIn(page, shift=DOWN * 1.2), FadeIn(alab), run_time=0.6)
        hear(self, "wins on", lead=0.1)
        ring = Rectangle(width=2.7, height=3.3, color=TERRA, stroke_width=6).move_to([-3.9, 0.5, 0])
        self.play(Create(ring), run_time=0.5)
        # four Explorer items bounce off the rack
        items = [("host", 1.6, "hosts"), ("partition", 0.55, "partitions"), ("storage", -0.5, "storage rules"), ("module", -1.5, "module setup")]
        for name, y, cue in items:
            hear(self, cue, lead=0.5)
            c = chip(name, -1.15, y, w=2.5, size=32)
            self.play(FadeIn(c), run_time=0.15)
            self.play(c.animate.shift(RIGHT * 1.7), run_time=0.3, rate_func=smooth)
            bump = x_mark(2.15, y, r=0.25, w=8)
            self.play(Create(bump), c.animate.shift(LEFT * 0.6), run_time=0.25, rate_func=smooth)
            self.play(FadeOut(bump), run_time=0.15)
        hear(self, "assume AICR", lead=0.2)
        line = T("AICR is not Explorer", 46, bold=True).move_to([2.6, 2.7, 0])
        self.play(FadeIn(line, shift=DOWN * 0.3), run_time=0.4)
        self.play(*[l.animate.set_color(TERRA) for l in lights], run_time=0.5)
        done(self)


class B41_AICRDiffers(Scene):
    """A two-column table builds row by row, each row on its spoken words."""
    def construct(self):
        rows = [("user name", "dot becomes underscore, _neu added", "username is built"),
                ("login", "key + certificate, no password", "no password"),
                ("GPU", "the partition picks it", "partition decides"),
                ("idle GPU", "cancelled automatically", "idle GPUs"),
                ("scratch", "purged after 30 days, no off-site backup", "purged after 30 days")]
        ys = [2.1, 1.05, 0.0, -1.05, -2.1]
        top = Line([-6.0, 2.75, 0], [6.0, 2.75, 0], color=INK, stroke_width=6)
        div = Line([-3.5, 2.75, 0], [-3.5, -2.75, 0], color=BAR2, stroke_width=6)
        self.play(Create(top), Create(div), run_time=0.5)
        for (k, v, cue), y in zip(rows, ys):
            hear(self, cue, lead=0.2)
            key = T(k, 38, bold=True)
            key.move_to([-6.0 + key.width / 2, y, 0])
            val = T(v, 34)
            val.move_to([-3.2 + val.width / 2, y, 0])
            sep = Line([-6.0, y - 0.52, 0], [6.0, y - 0.52, 0], color=BAR3, stroke_width=5)
            self.play(FadeIn(key), Create(sep), run_time=0.3)
            self.play(FadeIn(val, shift=RIGHT * 0.3), run_time=0.35)
        done(self)


# ═════════════════════════════ PART D — B44 B45 B59 B60 B61 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pD_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pD_bar(x0, y, frac, w=6.8, h=0.5, color=BAR1):
    """A jobstats-style bar: (track, fill). The fill grows from the left edge."""
    track = Rectangle(width=w, height=h, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x0 + w / 2, y, 0])
    fw = max(0.05, w * frac)
    fill = Rectangle(width=fw, height=h, fill_color=color, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x0 + fw / 2, y, 0])
    return track, fill


def pD_tick(x, y0, y1):
    return Line([x, y0, 0], [x, y1, 0], color=INK, stroke_width=7)


class B44_JobstatsTargets(Scene):
    """jobstats draws four bars and a time bar; the GPU bar is the filled one and two ticks mark 50 and 70."""
    def construct(self):
        x0, W = -2.4, 6.8
        rows = [("CPU utilisation", 2.55, 0.13, "13%"), ("CPU memory", 1.55, 0.25, "25%"),
                ("GPU utilisation", 0.2, 0.80, "80%"), ("GPU memory", -1.2, 0.17, "17%")]
        tag = M("jobstats", 36).move_to([-4.6, 3.05, 0])
        tracks, fills, labs, nums = [], [], [], []
        for name, y, f, n in rows:
            col = TERRA if name == "GPU utilisation" else BAR1
            tr, fl = pD_bar(x0, y, f, W, color=col)
            lb = T(name, 32)
            lb.move_to([-6.0 + lb.width / 2, y, 0])
            nm = T(n, 36).move_to([5.35, y, 0])
            tracks.append(tr); fills.append(fl); labs.append(lb); nums.append(nm)
        ttr, tfl = pD_bar(x0, -2.35, 55 / 480, W, color=INK)
        tlab = T("time", 32)
        tlab.move_to([-6.0 + tlab.width / 2, -2.35, 0])
        asked = T("8 h asked", 32).move_to([x0 + W - 0.9, -2.9, 0])
        ran = T("55 min ran", 32).move_to([x0 + 0.1 + 0.85, -2.9, 0])

        # "job stats": the command's name lands and the four empty tracks with their names
        hear(self, "job stats", lead=0.15)
        self.play(FadeIn(tag), *[FadeIn(t) for t in tracks], *[FadeIn(l) for l in labs], run_time=0.5)
        # "real example": the three quiet bars fill
        hear(self, "real example", lead=0.1)
        quiet = [0, 1, 3]
        self.play(*[GrowFromEdge(fills[i], LEFT) for i in quiet], *[FadeIn(nums[i]) for i in quiet], run_time=0.7)
        # "8 hours": the time bar and what was asked
        hear(self, "8 hours", lead=0.15)
        self.play(FadeIn(ttr), FadeIn(tlab), FadeIn(asked), run_time=0.4)
        # "ran 55 minutes": the short fill
        hear(self, "ran 55", lead=0.1)
        self.play(GrowFromEdge(tfl, LEFT), FadeIn(ran), run_time=0.5)
        # "GPU 80% busy": the terracotta bar fills
        hear(self, "GPU 80", lead=0.15)
        self.play(GrowFromEdge(fills[2], LEFT), run_time=0.7)
        self.play(FadeIn(nums[2]), run_time=0.2)
        # "over 70 ... acceptable"
        t70 = x0 + W * 0.7
        t50 = x0 + W * 0.5
        k70 = pD_tick(t70, 0.55, -0.1)
        n70 = T("70", 34).move_to([t70, 0.85, 0])
        acc = T("acceptable", 32).move_to([t70 + 1.3, -0.45, 0])
        hear(self, "over 70", lead=0.2)
        self.play(Create(k70), FadeIn(n70), run_time=0.4)
        hear(self, "is acceptable", lead=0.1)
        self.play(FadeIn(acc), run_time=0.3)
        # "under 50 is a problem"
        k50 = pD_tick(t50, 0.55, -0.1)
        n50 = T("50", 34).move_to([t50, 0.85, 0])
        prob = T("problem", 32).move_to([t50 - 0.85, -0.45, 0])
        hear(self, "under 50", lead=0.2)
        self.play(Create(k50), FadeIn(n50), run_time=0.4)
        hear(self, "is a problem", lead=0.15)
        self.play(FadeIn(prob), run_time=0.3)
        done(self)


def pD_card(x, y, w=3.6, h=4.0):
    return paper(x, y, w=w, h=h)


def pD_rule(lines, x, y, w=3.7, h=1.25):
    """A rule chip: white pill carrying two short lines."""
    shadow = pill(x + 0.08, y - 0.08, w, h=h, fill=BOX_L)
    body = pill(x, y, w, h=h)
    a = T(lines[0], 32)
    b = T(lines[1], 32)
    txt = VGroup(a, b).arrange(DOWN, buff=0.08).move_to([x, y, 0])
    g = VGroup(shadow, body, txt)
    return g


class B45_QuietLessons(Scene):
    """Three quiet failures, drawn as three cards; each ends in a rule chip."""
    def construct(self):
        cy = 0.75
        xs = [-4.1, 0.0, 4.1]
        cards = [pD_card(x, cy) for x in xs]
        # card 1: a model box, random dots inside, a 'loaded, no error' badge
        mbox = Rectangle(width=1.9, height=1.5, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([xs[0], cy + 0.5, 0])
        rng = np.random.RandomState(11)
        dots = VGroup(*[Dot([xs[0] + rng.uniform(-0.75, 0.75), cy + 0.5 + rng.uniform(-0.55, 0.55), 0], radius=0.07, color=INK) for _ in range(16)])
        badge = VGroup(pill(xs[0] + 0.05, cy - 0.65, 3.4, h=0.7, fill=PAGE_L), check(xs[0] - 1.4, cy - 0.65, s=0.16, w=6))
        blab = T("loaded, no error", 32).move_to([xs[0] + 0.3, cy - 0.65, 0])
        # card 2: a flat audio line between faint limits, a tiny peak
        top = Line([xs[1] - 1.4, cy + 1.2, 0], [xs[1] + 1.4, cy + 1.2, 0], color=BAR2, stroke_width=4)
        bot = Line([xs[1] - 1.4, cy - 0.2, 0], [xs[1] + 1.4, cy - 0.2, 0], color=BAR2, stroke_width=4)
        mid = cy + 0.5
        wave = VMobject(stroke_color=INK, stroke_width=7)
        wave.set_points_as_corners([[xs[1] - 1.4, mid, 0], [xs[1] - 0.2, mid, 0], [xs[1] - 0.1, mid + 0.08, 0],
                                    [xs[1], mid - 0.06, 0], [xs[1] + 0.1, mid, 0], [xs[1] + 1.4, mid, 0]])
        peak = M("4 of 32767", 32).move_to([xs[1], cy - 0.85, 0])
        # card 3: two files, the old one on a cache shelf, the new one beside it
        shelf = Line([xs[2] - 1.5, cy - 0.4, 0], [xs[2] - 0.2, cy - 0.4, 0], color=INK, stroke_width=10)
        oldp = paper(xs[2] - 0.85, cy + 0.25, w=1.0, h=1.3, fill=PAGE_L)
        oldl = scribbles_on(oldp, n=2, inset=0.22, gap=0.3)
        newp = paper(xs[2] + 0.85, cy + 0.25, w=1.0, h=1.3)
        newl = scribbles_on(newp, n=2, inset=0.22, gap=0.3)
        cache = T("cache", 32).move_to([xs[2] - 0.85, cy - 0.85, 0])
        same = T("same path", 32).move_to([xs[2] + 0.2, cy - 1.45, 0])
        served = chip("served", xs[2] - 0.6, cy + 1.45, w=1.7, size=30)
        r1 = pD_rule(("prove the", "weights loaded"), xs[0], -2.35)
        r2 = pD_rule(("gate every input", "with a number"), xs[1], -2.35)
        r3 = pD_rule(("give it a", "new name"), xs[2], -2.35)

        self.play(*[FadeIn(c) for c in cards], run_time=0.5)
        # "a checkpoint": the model box; "loaded without error": the badge; "random weights": the dots
        hear(self, "a checkpoint", lead=0.2)
        self.play(FadeIn(mbox), run_time=0.3)
        hear(self, "loaded without error", lead=0.3)
        self.play(FadeIn(badge), FadeIn(blab), run_time=0.4)
        hear(self, "random weights", lead=0.3)
        self.play(FadeIn(dots), run_time=0.5)
        # "an input clip so quiet": limits, then the flat line with its tiny peak
        hear(self, "an input clip", lead=0.2)
        self.play(FadeIn(top), FadeIn(bot), Create(wave), run_time=0.8)
        hear(self, "produced silence", lead=0.4)
        self.play(FadeIn(peak), run_time=0.3)
        # "a cached file": the old file on the shelf; "served": it is the one handed out; "replaced": the new file
        hear(self, "a cached file", lead=0.2)
        self.play(FadeIn(shelf), FadeIn(oldp), FadeIn(oldl), FadeIn(cache), run_time=0.5)
        hear(self, "served", lead=0.15)
        self.play(FadeIn(served), run_time=0.3)
        hear(self, "was replaced", lead=0.3)
        self.play(FadeIn(newp), FadeIn(newl), FadeIn(same), run_time=0.5)
        # the three rules
        hear(self, "prove the weights loaded", lead=0.2)
        self.play(FadeIn(r1, shift=UP * 0.2), run_time=0.4)
        hear(self, "gate every input", lead=0.2)
        self.play(FadeIn(r2, shift=UP * 0.2), run_time=0.4)
        hear(self, "give a replaced file", lead=0.2)
        self.play(FadeIn(r3, shift=UP * 0.2), run_time=0.4)
        done(self)


class B59_WhereToFindThem(Scene):
    """The repo address lands, then the skills folder opens into hpc/HPC.md and aicr/AICR.md."""
    def construct(self):
        title = pD_act_title("V · Using The Files")
        url = M("github.com/nikbearbrown/hpc-aicr", 32).move_to([0, 1.75, 0])
        under = Line([url.get_left()[0], 1.3, 0], [url.get_right()[0], 1.3, 0], color=TERRA, stroke_width=6)
        sk = M("skills/", 36).move_to([0, 0.45, 0])
        lx = [-3.0, 3.0]
        stem = Line([0, 0.05, 0], [0, -0.2, 0], color=INK, stroke_width=5)
        bar = Line([lx[0], -0.2, 0], [lx[1], -0.2, 0], color=INK, stroke_width=5)
        drops = [Line([x, -0.2, 0], [x, -0.5, 0], color=INK, stroke_width=5) for x in lx]
        subs = [M(s, 34).move_to([x, -0.85, 0]) for s, x in zip(["hpc/", "aicr/"], lx)]
        pgs = [paper(x, -1.95, w=1.3, h=1.55) for x in lx]
        gls = [scribbles_on(p, n=2, inset=0.22, gap=0.3) for p in pgs]
        names = [M(s, 30).move_to([x, -2.95, 0]) for s, x in zip(["HPC.md", "AICR.md"], lx)]

        self.play(FadeIn(title), run_time=0.4)
        hear(self, "free on GitHub", lead=0.2)
        self.play(FadeIn(url), Create(under), run_time=0.6)
        hear(self, "skills folder", lead=0.3)
        self.play(FadeIn(sk), run_time=0.3)
        self.play(Create(stem), Create(bar), *[Create(d) for d in drops], run_time=0.4)
        hear(self, "in the hpc folder", lead=0.2)
        self.play(FadeIn(subs[0]), FadeIn(pgs[0]), FadeIn(gls[0]), FadeIn(names[0]), run_time=0.5)
        hear(self, "in the aicr folder", lead=0.2)
        self.play(FadeIn(subs[1]), FadeIn(pgs[1]), FadeIn(gls[1]), FadeIn(names[1]), run_time=0.5)
        done(self)


class B60_ThreeSteps(Scene):
    """Three steps land left to right on a line: files in a folder, one line in the instructions, the rules said back."""
    def construct(self):
        title = pD_act_title("V · Using The Files")
        lx = [-4.2, 0.0, 4.2]
        line = Line([-5.6, -2.3, 0], [5.6, -2.3, 0], color=BAR2, stroke_width=8)
        dots = [Dot([x, -2.3, 0], radius=0.14, color=TERRA) for x in lx]
        caps = [T(s, 44).move_to([x, -2.9, 0]) for s, x in zip(["both files", "one line", "say back"], lx)]
        # step 1: a folder with two pages
        pg1 = paper(lx[0] - 0.7, 0.85, w=1.25, h=1.5)
        pg2 = paper(lx[0] + 0.7, 0.85, w=1.25, h=1.5)
        gl1, gl2 = scribbles_on(pg1, n=2, inset=0.22, gap=0.3), scribbles_on(pg2, n=2, inset=0.22, gap=0.3)
        back = Rectangle(width=3.0, height=1.5, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([lx[0], -0.1, 0])
        tab = Rectangle(width=1.1, height=0.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([lx[0] - 0.95, 0.75, 0])
        front = Rectangle(width=3.0, height=1.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([lx[0], -0.25, 0])
        f1 = M("HPC.md", 30).move_to([lx[0], -1.15, 0])
        f2 = M("AICR.md", 30).move_to([lx[0], -1.65, 0])
        folder_back = VGroup(tab, back)
        # step 2: an instructions page with one highlighted line
        ip = paper(lx[1], 0.55, w=2.3, h=2.7)
        rows = [1.45, 1.0, 0.55, 0.1]
        band = Rectangle(width=1.95, height=0.36, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([lx[1], rows[2], 0])
        scr = VGroup(*[scribble(lx[1] - 0.85, y, 1.7 if i != 3 else 1.0, sw=4, amp=0.09) for i, y in enumerate(rows)])
        mark = Dot([lx[1] - 1.0, rows[2], 0], radius=0.1, color=TERRA)
        n1 = M("CLAUDE.md", 30).move_to([lx[1], -1.15, 0])
        n2 = M("AGENTS.md", 30).move_to([lx[1], -1.65, 0])
        # step 3: Claude says the rules back
        claude = logo_chip("claude", lx[2] - 0.5, 1.9)
        bub = RoundedRectangle(corner_radius=0.3, width=3.0, height=1.3, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([lx[2] - 0.2, 0.2, 0])
        tail = Polygon([lx[2] - 1.0, 0.82, 0], [lx[2] - 0.4, 0.82, 0], [lx[2] - 0.7, 1.22, 0], fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
        cover = Line([lx[2] - 0.95, 0.83, 0], [lx[2] - 0.45, 0.83, 0], color=PAGE_TOP, stroke_width=8)
        rl = VGroup(*[VGroup(check(lx[2] - 1.15, 0.38 - 0.5 * i, s=0.13, w=5), scribble(lx[2] - 0.85, 0.38 - 0.5 * i, 1.5, sw=4)) for i in range(2)])
        bubble = VGroup(tail, bub, cover, rl)
        box = job_box(Iso(5.0, 1.15, 0.55), 0, 0, 0, s=0.9)

        self.play(FadeIn(title), FadeIn(line), run_time=0.4)
        # "put both files": the two pages slide into the folder, named in mono
        hear(self, "put both files", lead=0.15)
        self.play(FadeIn(folder_back), FadeIn(pg1), FadeIn(gl1), FadeIn(pg2), FadeIn(gl2), run_time=0.5)
        hear(self, "where your agent", lead=0.1)
        self.play(FadeIn(front), FadeIn(f1), FadeIn(f2), FadeIn(dots[0]), FadeIn(caps[0]), run_time=0.6)
        # "Add the one line": the instructions page, the one line gets its band
        hear(self, "Add the one line", lead=0.2)
        self.play(FadeIn(ip), FadeIn(scr), run_time=0.5)
        self.play(FadeIn(band), FadeIn(mark), FadeIn(dots[1]), FadeIn(caps[1]), run_time=0.4)
        scr.set_z_index(3); mark.set_z_index(3)
        hear(self, "claw md", lead=0.2)
        self.play(FadeIn(n1), run_time=0.3)
        hear(self, "agents md", lead=0.2)
        self.play(FadeIn(n2), run_time=0.3)
        # "ask the agent": Claude arrives
        hear(self, "ask the agent", lead=0.2)
        self.play(FadeIn(claude), FadeIn(dots[2]), FadeIn(caps[2]), run_time=0.5)
        # "say back which rules apply": the bubble with the rules
        hear(self, "say back", lead=0.1)
        self.play(FadeIn(bubble), run_time=0.5)
        hear(self, "which rules apply", lead=0.1)
        self.play(*[Indicate(r, color=INK, scale_factor=1.08) for r in rl], run_time=0.6)
        # "before it runs anything": only now does the command box show up, and it waits
        hear(self, "before it runs", lead=0.15)
        self.play(FadeIn(box), run_time=0.4)
        done(self)


class B61_WhatRulesCannotDo(Scene):
    """You hold the key at a closed gate with Claude waiting; the note lands on the gate; three labels follow."""
    def construct(self):
        you = professor_bear("1x1", 2.3, seed="B61", x=-4.4, y=0.5)
        ylab = T("you", 36).move_to([-4.4, -0.95, 0])
        key = key_obj(-3.55, -0.25, s=0.45)
        p1 = Rectangle(width=0.28, height=2.6, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-1.2, 0.5, 0])
        p2 = Rectangle(width=0.28, height=2.6, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.6, 0.5, 0])
        bar = Rectangle(width=1.5, height=0.3, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-0.3, 0.5, 0])
        lock = padlock(-0.3, 0.5, s=0.55)
        gate = VGroup(p1, p2, bar, lock)
        claude = logo_chip("claude", 2.5, 0.5)
        page = paper(5.2, 0.5, w=1.45, h=1.9)
        pl = scribbles_on(page, n=3, inset=0.25, gap=0.36)
        q = T("?", 64).move_to([5.2, 2.0, 0])
        note = chip("ask Research Computing once", -0.3, 2.35, size=32)
        w = 3.85
        sx = [-4.15, 0.0, 4.15]
        ghosts = [Rectangle(width=w, height=0.8, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([x, -2.3, 0]) for x in sx]
        st = [chip(s, x, -2.3, w=w, size=32) for s, x in zip(["from the sources", "from a real run", "our own judgment"], sx)]

        self.play(FadeIn(you), FadeIn(ylab), FadeIn(key), FadeIn(gate), run_time=0.5)
        # "do not replace judgment": Claude walks up and waits at the gate
        hear(self, "do not replace", lead=0.3)
        self.play(FadeIn(claude), run_time=0.5)
        # "policy page": a page with nothing on it to answer
        hear(self, "policy page", lead=0.4)
        self.play(FadeIn(page), FadeIn(pl), run_time=0.4)
        hear(self, "whether automated agents", lead=0.2)
        self.play(FadeIn(q), run_time=0.3)
        # "so the files say to ask Research Computing once": the note lands on the gate
        hear(self, "so the files", lead=0.0)
        self.play(FadeOut(page), FadeOut(pl), FadeOut(q), run_time=0.2)
        note.shift(UP * 0.8)
        self.add(note)
        self.play(note.animate.shift(DOWN * 0.8), run_time=0.5, rate_func=smooth)
        # "every claim is labelled": three empty slots, then the three stamps
        hear(self, "every claim", lead=0.2)
        self.play(*[FadeIn(g) for g in ghosts], run_time=0.4)
        hear(self, "from the sources", lead=0.2)
        self.play(FadeIn(st[0], scale=1.25), run_time=0.35)
        hear(self, "from a real run", lead=0.2)
        self.play(FadeIn(st[1], scale=1.25), run_time=0.35)
        hear(self, "our own judgment", lead=0.2)
        self.play(FadeIn(st[2], scale=1.25), run_time=0.35)
        done(self)


for _cls in (B10_FastAndLiteral, B11_ThreeQuietFailures, B12_TwoFiles, B21_PrimeDirective, B22_HardNevers, B25_TwelveSlowerThanEight, B28_WhereFilesLive, B29_InstallLadder, B32_DoNotCopy, B33_HonestAppendix, B40_AssumeNotExplorer, B41_AICRDiffers, B44_JobstatsTargets, B45_QuietLessons, B59_WhereToFindThem, B60_ThreeSteps, B61_WhatRulesCannotDo):
    _cls.play = ST.play
