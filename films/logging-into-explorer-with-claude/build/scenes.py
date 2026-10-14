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
_ASR = {"BOPEN": [["Research", 0.0], ["computing", 0.38], ["on", 0.78], ["Explorer", 1.0], ["and", 1.42], ["AICR,", 1.66], ["logging", 2.9], ["into", 3.04], ["Explorer", 3.36], ["HPC", 3.84], ["with", 4.52], ["Claude,", 4.88], ["how", 5.52], ["to", 5.7], ["make", 5.8], ["a", 5.92], ["key,", 6.1], ["unlock", 6.48], ["it", 6.74], ["once,", 6.96], ["and", 7.42], ["let", 7.5], ["Claude", 7.68], ["code", 7.96], ["log", 8.26], ["into", 8.6], ["the", 8.82], ["Explorer", 8.96], ["cluster", 9.36], ["for", 9.64], ["you", 9.96], ["without", 10.18], ["ever", 10.66], ["handing", 10.92], ["it", 11.14], ["a", 11.4], ["password.", 11.52]], "BIDEA": [["Hallo,", 0.74], ["this", 1.26], ["is", 1.36], ["Liam", 1.56], ["in", 1.86], ["for", 2.16], ["Bear,", 2.3], ["first", 3.04], ["a", 3.08], ["correction.", 3.28], ["To", 4.06], ["let", 4.16], ["Claude", 4.32], ["log", 4.56], ["into", 4.82], ["Explorer,", 5.1], ["you", 5.8], ["do", 5.84], ["not", 5.92], ["hand", 6.06], ["it", 6.28], ["your", 6.38], ["password.", 6.5], ["You", 7.22], ["make", 7.32], ["a", 7.44], ["key,", 7.6], ["you", 8.02], ["unlock", 8.08], ["it", 8.38], ["once", 8.56], ["yourself,", 8.7], ["and", 9.32], ["Claude", 9.4], ["never", 9.62], ["sees", 9.92], ["either.", 10.18]], "BDEFS": [["Six", 0.0], ["terms,", 0.24], ["a", 0.76], ["private", 0.8], ["key,", 1.08], ["a", 1.54], ["secret", 1.62], ["file", 1.88], ["that", 2.28], ["proves", 2.48], ["who", 2.72], ["you", 2.92], ["are,", 3.04], ["a", 3.38], ["public", 3.5], ["key,", 3.72], ["it's", 4.16], ["matching", 4.26], ["half", 4.58], ["safe", 4.84], ["to", 5.12], ["share,", 5.38], ["an", 5.98], ["SSH", 6.1], ["agent,", 6.32], ["a", 7.0], ["helper", 7.06], ["that", 7.24], ["holds", 7.5], ["your", 7.72], ["unlocked", 7.92], ["key,", 8.26], ["batch", 9.16], ["mode,", 9.16], ["a", 9.6], ["setting", 9.64], ["that", 9.82], ["makes", 10.02], ["SSH", 10.16], ["refuse", 10.58], ["to", 11.08], ["ask", 11.34], ["any", 11.54], ["question,", 11.74], ["a", 12.5], ["host", 12.6], ["alias,", 12.82], ["a", 13.46], ["short", 13.54], ["name", 13.72], ["for", 13.94], ["the", 14.14], ["cluster", 14.26], ["in", 14.52], ["your", 14.72], ["SSH", 14.82], ["config,", 15.14], ["and", 16.08], ["a", 16.2], ["login", 16.3], ["node,", 16.54], ["the", 17.08], ["shared", 17.16], ["computer", 17.4], ["you", 17.8], ["land", 18.02], ["on", 18.22], ["when", 18.46], ["you", 18.6], ["connect.", 18.72]], "B10": [["Explorer", 0.0], ["lets", 0.4], ["you", 0.64], ["in", 0.84], ["with", 0.96], ["your", 1.1], ["Northeastern", 1.24], ["password.", 1.68], ["You", 2.68], ["connect", 2.72], ["to", 2.96], ["the", 3.16], ["login", 3.28], ["host,", 3.52], ["answer", 4.1], ["the", 4.28], ["first", 4.46], ["host", 4.68], ["key", 4.98], ["question", 5.22], ["with", 5.6], ["yes,", 5.86], ["type", 6.34], ["the", 6.48], ["password", 6.66], ["and", 7.08], ["you", 7.34], ["land", 7.46], ["on", 7.66], ["a", 7.84], ["login", 7.94], ["node.", 8.16], ["On", 9.02], ["our", 9.12], ["account", 9.24], ["there", 9.56], ["was", 9.72], ["no", 9.84], ["Duo", 10.06], ["prompt", 10.34], ["for", 10.64], ["SSH.", 10.9], ["The", 11.7], ["web", 11.84], ["portal", 12.0], ["is", 12.28], ["different,", 12.54], ["the", 13.06], ["documentation", 13.14], ["says", 13.54], ["it", 14.16], ["asks.", 14.32]], "B11": [["That", 0.0], ["works", 0.18], ["for", 0.38], ["you", 0.64], ["at", 0.76], ["a", 0.88], ["keyboard,", 1.02], ["it", 1.54], ["does", 1.62], ["not", 1.72], ["work", 1.92], ["for", 2.12], ["Claude.", 2.5], ["Claude", 3.12], ["code", 3.34], ["runs", 3.6], ["commands", 3.96], ["with", 4.34], ["no", 4.58], ["keyboard", 4.8], ["attached,", 5.16], ["and", 5.86], ["a", 5.96], ["password", 6.06], ["is", 6.4], ["the", 6.62], ["one", 6.78], ["thing", 6.96], ["you", 7.18], ["must", 7.36], ["never", 7.5], ["hand", 7.82], ["it.", 8.06], ["So", 8.56], ["we", 8.7], ["replace", 8.8], ["the", 9.08], ["password", 9.3], ["with", 9.7], ["something", 9.92], ["the", 10.16], ["agent", 10.42], ["can", 10.7], ["use", 10.96], ["without", 11.24], ["ever", 11.52], ["seeing", 11.74], ["it,", 12.0], ["a", 12.54], ["key.", 12.72]], "B12": [["One", 0.0], ["detail", 0.22], ["on", 0.62], ["the", 0.88], ["login", 1.0], ["name.", 1.28], ["The", 2.06], ["one", 2.14], ["that", 2.26], ["worked", 2.4], ["was", 2.64], ["the", 2.82], ["name", 2.98], ["from", 3.14], ["the", 3.36], ["access", 3.5], ["form,", 3.84], ["the", 4.5], ["user", 4.52], ["ID,", 4.76], ["not", 5.38], ["the", 5.5], ["first", 5.66], ["part", 5.86], ["of", 6.14], ["an", 6.26], ["email", 6.4], ["address.", 6.68], ["If", 7.66], ["your", 7.78], ["first", 7.92], ["guess", 8.18], ["is", 8.38], ["refused,", 8.58], ["try", 9.32], ["the", 9.44], ["other,", 9.62], ["and", 10.0], ["wait", 10.14], ["a", 10.32], ["little", 10.46], ["after", 10.58], ["any", 10.88], ["password", 11.1], ["change.", 11.48]], "B20": [["A", 0.0], ["key", 0.14], ["comes", 0.28], ["in", 0.54], ["two", 0.74], ["halves.", 0.96], ["The", 1.64], ["private", 1.68], ["half", 1.98], ["stays", 2.2], ["on", 2.46], ["your", 2.66], ["computer", 2.78], ["and", 3.14], ["proves", 3.4], ["who", 3.64], ["you", 3.86], ["are.", 3.96], ["The", 4.56], ["public", 4.64], ["half", 4.92], ["is", 5.18], ["safe", 5.34], ["to", 5.56], ["hand", 5.78], ["out,", 5.98], ["and", 6.48], ["Explorer", 6.54], ["will", 6.92], ["keep", 7.22], ["a", 7.38], ["copy.", 7.54], ["When", 8.5], ["you", 8.6], ["connect,", 8.74], ["your", 9.24], ["computer", 9.32], ["proves", 9.64], ["it", 10.0], ["holds", 10.18], ["the", 10.4], ["private", 10.62], ["half", 10.92], ["that", 11.2], ["matches.", 11.38]], "B21": [["Make", 0.0], ["it", 0.18], ["with", 0.3], ["SSH", 0.44], ["keygen.", 0.78], ["The", 1.72], ["type", 1.82], ["is", 2.04], ["ED25", 2.24], ["-519,", 3.2], ["a", 4.1], ["modern", 4.2], ["default.", 4.46], ["You", 5.24], ["choose", 5.32], ["a", 5.52], ["passphrase", 5.68], ["which", 6.1], ["locks", 6.38], ["the", 6.66], ["private", 6.88], ["file", 7.18], ["in", 7.56], ["which", 7.78], ["Claude", 8.0], ["never", 8.22], ["sees.", 8.52], ["The", 9.6], ["command", 9.72], ["prints", 9.98], ["where", 10.28], ["both", 10.46], ["halves", 10.66], ["went", 10.94], ["and", 11.22], ["a", 11.5], ["fingerprint,", 11.6], ["a", 12.3], ["short", 12.42], ["name", 12.64], ["for", 12.86], ["this", 13.1], ["key.", 13.26]], "B22": [["To", 0.0], ["install", 0.14], ["the", 0.54], ["public", 0.7], ["half", 0.96], ["one", 1.22], ["command", 1.56], ["ssh", 1.96], ["copy", 2.42], ["id,", 2.9], ["it", 3.82], ["asks", 3.88], ["for", 4.08], ["your", 4.32], ["Northeastern", 4.44], ["password", 4.86], ["this", 5.36], ["one", 5.62], ["time", 5.86], ["typed", 6.2], ["by", 6.56], ["you", 6.84], ["and", 7.08], ["it", 7.34], ["reports", 7.44], ["that", 7.78], ["one", 8.08], ["key", 8.3], ["was", 8.5], ["added.", 8.68], ["After", 9.58], ["this,", 9.74], ["Explorer", 10.24], ["knows", 10.52], ["your", 10.8], ["key.", 11.06]], "B30": [["Now", 0.0], ["the", 0.22], ["old", 0.38], ["problem,", 0.58], ["Claude", 1.46], ["cannot", 1.46], ["type", 1.76], ["a", 2.06], ["passphrase,", 2.24], ["so", 2.92], ["you", 3.1], ["unlock", 3.22], ["the", 3.52], ["key", 3.72], ["yourself", 3.88], ["once", 4.28], ["into", 4.62], ["a", 4.92], ["helper", 5.06], ["called", 5.28], ["the", 5.58], ["SSH", 5.74], ["agent.", 6.1], ["The", 7.26], ["agent", 7.42], ["holds", 7.72], ["the", 8.0], ["unlocked", 8.22], ["key,", 8.6], ["SSH", 9.36], ["asks", 9.6], ["the", 10.1], ["agent,", 10.32], ["and", 10.94], ["the", 11.02], ["key", 11.12], ["never", 11.26], ["passes", 11.48], ["through", 11.88], ["Claude.", 12.18]], "B31": [["On", 0.0], ["a", 0.14], ["Mac", 0.26], ["one", 0.42], ["command", 0.7], ["SSH", 1.08], ["add", 1.48], ["with", 1.98], ["the", 2.22], ["Apple", 2.36], ["keychain", 2.62], ["flag,", 3.06], ["you", 3.84], ["type", 3.94], ["the", 4.16], ["passphrase", 4.34], ["here", 4.78], ["in", 5.1], ["your", 5.26], ["own", 5.36], ["terminal.", 5.52], ["It", 6.24], ["answers", 6.32], ["that", 6.64], ["the", 6.92], ["identity", 7.06], ["was", 7.44], ["added.", 7.74], ["With", 8.62], ["the", 8.74], ["keychain,", 8.9], ["the", 9.48], ["key", 9.56], ["can", 9.72], ["reload", 9.92], ["itself", 10.24], ["when", 10.6], ["the", 10.82], ["agent", 10.94], ["is", 11.26], ["emptied.", 11.48]], "B32": [["Then", 0.0], ["give", 0.16], ["the", 0.3], ["cluster", 0.44], ["a", 0.68], ["short", 0.9], ["name,", 1.08], ["one", 1.62], ["block", 1.74], ["in", 1.98], ["your", 2.16], ["SSH", 2.26], ["config,", 2.52], ["host", 3.42], ["explorer,", 3.58], ["the", 4.42], ["real", 4.52], ["host", 4.72], ["name,", 5.02], ["your", 5.54], ["username,", 5.6], ["the", 6.3], ["key", 6.4], ["file,", 6.56], ["and", 7.1], ["identities", 7.14], ["only", 7.6], ["so", 7.98], ["SSH", 8.28], ["offers", 8.64], ["just", 9.12], ["this", 9.44], ["key.", 9.64], ["Add", 10.38], ["keys", 10.54], ["to", 10.74], ["agent,", 11.0], ["use", 11.54], ["keychain,", 11.68], ["and", 12.3], ["a", 12.38], ["keep", 12.46], ["alive.", 12.64]], "B33": [["Here", 0.0], ["is", 0.18], ["a", 0.28], ["real", 0.42], ["mistake", 0.58], ["from", 1.0], ["this", 1.26], ["setup,", 1.42], ["so", 1.96], ["you", 1.96], ["do", 2.08], ["not", 2.16], ["repeat", 2.32], ["it.", 2.6], ["Before", 3.02], ["that", 3.16], ["block", 3.36], ["existed,", 3.58], ["the", 4.24], ["test", 4.28], ["failed,", 4.5], ["could", 5.2], ["not", 5.28], ["resolve", 5.48], ["host", 5.92], ["name", 6.16], ["explorer.", 6.48], ["SSH", 7.66], ["treated", 7.92], ["explorer", 8.46], ["as", 8.92], ["a", 9.18], ["computer", 9.28], ["name", 9.56], ["because", 9.88], ["nothing", 10.24], ["told", 10.54], ["it", 10.82], ["otherwise.", 11.02], ["The", 11.72], ["fix", 11.88], ["is", 12.08], ["the", 12.34], ["block", 12.48], ["you", 12.74], ["just", 12.94], ["saw.", 13.1]], "B40": [["Tested", 0.0], ["the", 0.36], ["way", 0.44], ["Claude", 0.62], ["will", 0.88], ["connect.", 1.06], ["Batch", 1.8], ["mode", 1.92], ["makes", 2.16], ["SSH", 2.44], ["fail", 2.82], ["at", 3.3], ["once", 3.46], ["instead", 3.74], ["of", 4.0], ["asking", 4.14], ["a", 4.42], ["question.", 4.6], ["It", 5.52], ["printed", 5.64], ["the", 5.86], ["username", 6.06], ["and", 6.34], ["the", 6.8], ["login", 6.9], ["node", 7.12], ["explorer", 7.58], ["-01.", 8.04], ["No", 9.46], ["password,", 9.56], ["no", 10.26], ["passphrase,", 10.36], ["no", 11.12], ["duo.", 11.16]], "B41": [["Then", 0.0], ["Claude", 0.18], ["Code", 0.42], ["ran", 0.74], ["the", 1.02], ["same", 1.22], ["login", 1.42], ["itself", 1.74], ["with", 2.16], ["4", 2.5], ["read", 2.78], ["-only", 3.04], ["commands,", 3.26], ["who", 4.1], ["am", 4.18], ["I,", 4.28], ["which", 4.72], ["host,", 4.84], ["which", 5.34], ["folder,", 5.48], ["and", 6.06], ["my", 6.08], ["own", 6.26], ["jobs.", 6.46], ["The", 7.5], ["job", 7.7], ["list", 7.98], ["printed", 8.2], ["only", 8.52], ["its", 8.88], ["header", 9.12], ["because", 9.36], ["there", 9.7], ["were", 9.9], ["none.", 10.04]], "B42": [["From", 0.0], ["here,", 0.16], ["Claude", 0.56], ["follows", 0.68], ["the", 1.12], ["rules", 1.34], ["in", 1.58], ["the", 1.84], ["HPC", 1.96], [".md", 2.54], ["file.", 3.2], ["Read", 4.14], ["only", 4.22], ["first.", 4.48], ["Ask", 5.18], ["before", 5.36], ["it", 5.7], ["submits,", 5.84], ["cancels,", 6.26], ["or", 6.98], ["deletes.", 7.06], ["Never", 7.86], ["compute", 8.02], ["on", 8.4], ["the", 8.58], ["login", 8.7], ["node.", 8.94], ["And", 9.58], ["if", 9.66], ["any", 9.74], ["command", 9.9], ["ever", 10.22], ["prompts,", 10.46], ["it", 11.02], ["stops", 11.14], ["and", 11.44], ["tells", 11.72], ["you.", 11.94]], "B43": [["Then", 0.0], ["the", 0.12], ["hardest", 0.22], ["test", 0.46], ["which", 0.84], ["is", 1.04], ["a", 1.18], ["deliberate", 1.3], ["one,", 1.56], ["empty", 2.26], ["the", 2.44], ["agent,", 2.64], ["it", 3.28], ["reports", 3.36], ["no", 3.66], ["identities,", 3.96], ["log", 4.96], ["in", 5.08], ["anyway", 5.28], ["and", 5.58], ["it", 5.82], ["still", 5.96], ["works", 6.14], ["because", 6.42], ["the", 6.76], ["keychain", 6.92], ["reloaded", 7.28], ["the", 7.74], ["key", 7.88], ["and", 8.12], ["the", 8.36], ["list", 8.46], ["shows", 8.64], ["it", 8.92], ["back.", 9.14], ["This", 9.98], ["command", 10.12], ["empties", 10.44], ["every", 10.86], ["key", 11.16], ["so", 11.46], ["our", 11.76], ["rules", 11.9], ["say", 12.14], ["only", 12.42], ["you", 12.66], ["run", 12.9], ["it", 13.08], ["on", 13.26], ["purpose", 13.44], ["as", 13.78], ["a", 14.1], ["test.", 14.24]], "B50": [["How", 0.0], ["is", 0.14], ["this", 0.26], ["different", 0.42], ["from", 0.7], ["AICR?", 0.9], ["On", 1.88], ["Explorer,", 1.98], ["you", 2.48], ["start", 2.5], ["with", 2.72], ["your", 2.88], ["password", 3.0], ["and", 3.3], ["you", 3.58], ["make", 3.68], ["your", 3.84], ["own", 3.98], ["key.", 4.12], ["On", 4.72], ["AICR,", 4.82], ["there", 5.46], ["is", 5.54], ["no", 5.62], ["password", 5.78], ["at", 6.14], ["all.", 6.3], ["You", 6.7], ["download", 6.76], ["a", 7.04], ["key", 7.26], ["in", 7.46], ["a", 7.6], ["certificate", 7.72], ["that", 8.08], ["the", 8.32], ["AICR", 8.44], ["Certificate", 9.1], ["Authority", 9.46], ["signed.", 9.86], ["Your", 10.74], ["Explorer", 10.86], ["username", 11.24], ["is", 11.72], ["your", 11.94], ["university", 12.06], ["login.", 12.48], ["Your", 13.28], ["AICR", 13.38], ["name", 13.98], ["is", 14.16], ["built", 14.36], ["from", 14.54], ["it", 14.76], ["with", 14.92], ["an", 15.06], ["underscore", 15.16], ["in", 15.6], ["the", 15.82], ["institution", 15.9], ["on", 16.34], ["the", 16.6], ["end.", 16.74], ["And", 17.36], ["access", 17.4], ["comes", 17.7], ["from", 17.98], ["a", 18.18], ["project", 18.34], ["sponsor", 18.6], ["on", 18.96], ["Explorer", 19.18], ["and", 19.58], ["from", 19.96], ["a", 20.1], ["proposal", 20.2], ["on", 20.56], ["AICR.", 20.82]], "B51": [["What", 0.0], ["is", 0.14], ["the", 0.24], ["same", 0.4], ["matters", 0.6], ["more,", 0.92], ["both", 1.52], ["are", 1.66], ["SSH.", 1.86], ["Both", 2.7], ["need", 2.82], ["you", 3.06], ["to", 3.22], ["unlock", 3.32], ["a", 3.62], ["key", 3.8], ["once", 3.94], ["into", 4.2], ["the", 4.46], ["agent.", 4.58], ["Both", 5.4], ["are", 5.54], ["tested", 5.72], ["with", 6.02], ["batch", 6.3], ["mode.", 6.54], ["And", 7.22], ["on", 7.28], ["both,", 7.4], ["Claude", 7.98], ["never", 8.0], ["holds", 8.3], ["your", 8.66], ["password,", 8.84], ["your", 9.48], ["passphrase", 9.52], ["or", 10.02], ["your", 10.3], ["key.", 10.46]], "B52": [["And", 0.0], ["what", 0.14], ["we", 0.24], ["did", 0.36], ["not", 0.48], ["test,", 0.66], ["logging", 1.44], ["in", 1.56], ["from", 1.86], ["off", 2.02], ["campus", 2.2], ["or", 2.56], ["another", 2.86], ["network,", 3.08], ["the", 3.82], ["web", 3.92], ["portal,", 4.08], ["and", 4.76], ["weather", 4.84], ["research", 5.08], ["computing", 5.46], ["permits", 5.9], ["automated", 6.38], ["agent", 6.88], ["access.", 7.34], ["The", 8.46], ["policy", 8.56], ["pages", 8.92], ["mention", 9.34], ["none", 9.66], ["of", 9.98], ["them,", 10.1], ["so", 10.32], ["ask", 10.46], ["once", 10.66], ["by", 11.0], ["email", 11.26], ["to", 11.54], ["rchelp", 11.8], ["at", 12.52], ["northeastern", 12.8], [".edu.", 13.2]], "BVDT": [["Let's", 0.0], ["recap", 0.7], ["with", 0.94], ["Claude.", 1.2], ["Explorer", 2.14], ["starts", 2.14], ["with", 2.46], ["your", 2.64], ["password", 2.76], ["which", 3.08], ["Claude", 3.36], ["must", 3.6], ["never", 3.76], ["hold.", 3.98], ["Make", 4.54], ["a", 4.64], ["key,", 4.82], ["install", 5.16], ["its", 5.48], ["public", 5.7], ["half,", 6.0], ["and", 6.44], ["keep", 6.48], ["the", 6.6], ["private", 6.76], ["half", 7.02], ["yours.", 7.28], ["Unlock", 8.14], ["the", 8.34], ["key", 8.58], ["once", 8.7], ["into", 8.9], ["the", 9.12], ["SSH", 9.22], ["agent", 9.46], ["and", 9.92], ["give", 10.16], ["the", 10.26], ["cluster", 10.42], ["a", 10.62], ["host", 10.82], ["alias.", 11.04], ["Test", 11.82], ["with", 11.98], ["batch", 12.18], ["mode", 12.42], ["then", 12.72], ["let", 12.9], ["Claude", 13.06], ["run", 13.26], ["read", 13.46], ["-only", 13.68], ["commands.", 13.86], ["AICR", 14.88], ["differs,", 15.32], ["no", 15.78], ["password,", 15.9], ["and", 16.48], ["a", 16.54], ["key", 16.66], ["and", 16.82], ["certificate", 16.92], ["you", 17.28], ["download.", 17.6], ["And", 18.34], ["on", 18.42], ["both,", 18.52], ["Claude", 18.98], ["never", 19.12], ["holds", 19.36], ["your", 19.66], ["password,", 19.84], ["passphrase,", 20.46], ["or", 21.02], ["key.", 21.1]], "BHTF": [["Your", 0.0], ["turn,", 0.14], ["paste", 0.54], ["this", 0.7], ["into", 0.92], ["Claude,", 1.14], ["log", 1.66], ["into", 1.68], ["the", 1.9], ["Explorer", 2.04], ["cluster", 2.42], ["with", 2.7], ["SSH", 3.04], ["Explorer", 3.32], ["and", 3.86], ["run", 4.14], ["read", 4.3], ["-only", 4.54], ["commands", 4.74], ["only.", 5.14], ["Run,", 6.14], ["who", 6.44], ["am", 6.58], ["I,", 6.68], ["hostname,", 7.0], ["pwd,", 7.42], ["and", 8.24], ["sq", 8.32], ["for", 8.5], ["my", 8.8], ["own", 8.96], ["user.", 9.08], ["Tell", 9.68], ["me", 9.78], ["the", 9.92], ["username,", 10.02], ["the", 10.6], ["host,", 10.64], ["and", 10.98], ["which", 11.08], ["folder", 11.24], ["I", 11.52], ["land", 11.8], ["in.", 12.04], ["Do", 12.64], ["not", 12.72], ["submit,", 12.86], ["cancel,", 13.34], ["or", 13.74], ["change", 13.82], ["anything", 14.04], ["and", 14.36], ["do", 14.6], ["not", 14.72], ["run", 14.86], ["computation", 15.06], ["on", 15.6], ["the", 15.92], ["login", 16.06], ["node.", 16.26], ["Then", 16.88], ["check", 17.04], ["two", 17.26], ["things", 17.48], ["yourself.", 17.72], ["Did", 18.4], ["Claude", 18.5], ["run", 18.72], ["only", 18.9], ["read", 19.16], ["-only", 19.34], ["commands", 19.52], ["and", 19.96], ["did", 20.3], ["it", 20.4], ["ever", 20.48], ["ask", 20.68], ["for?", 20.9], ["Or", 21.66], ["print", 21.88], ["your", 22.14], ["passphrase", 22.34], ["or", 22.96], ["your", 23.22], ["key.", 23.44]], "BOUT": [["Logging", 0.0], ["into", 0.4], ["ExplorerHPC", 0.6], ["with", 1.8], ["Claude", 2.18], ["at", 2.54], ["Nick", 2.96], ["Bear", 3.2], ["Brown.", 3.42]]}


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


# ═════════════════════════════ PART A — Act I opening (B10 B11 B12) ═════════════════════════════
# Cue times come from hear("spoken phrase"): measured word times. Labels are 1-3 words; real text only in mono.

def pA_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


class B10_PasswordToday(Scene):
    """You type the password to the login node; host key answered yes; no Duo on ssh; the web portal asks."""
    def construct(self):
        title = pA_act_title("I · What Explorer Asks For")
        you = professor_bear("1x1", 2.3, seed="B10x", x=-5.1, y=-0.7)
        ylab = T("you", 36).move_to([-5.1, -2.4, 0])
        iso = Iso(3.2, -2.2, 1.0)
        rack, rlights = explorer_rack(iso)
        rlab = T("login node", 36).move_to([4.0, -3.0, 0])
        self.play(FadeIn(title), FadeIn(you), FadeIn(ylab), FadeIn(rack), FadeIn(rlights), FadeIn(rlab), run_time=0.5)
        # "Northeastern password": an empty password chip appears beside the portrait
        hear(self, "Northeastern password", lead=0.3)
        pw = chip("password", -2.6, 1.0, size=36)
        self.play(FadeIn(pw), run_time=0.3)
        # "connect to the login host": the ssh arrow runs from you to the rack
        hear(self, "connect to the", lead=0.2)
        arrow = Arrow([-3.5, -0.9, 0], [2.1, -0.9, 0], buff=0, color=INK, stroke_width=8, max_tip_length_to_length_ratio=0.12)
        ssh = M("ssh", 36).move_to([-0.6, -0.45, 0])
        self.play(GrowArrow(arrow), FadeIn(ssh), run_time=0.8)
        # "first host key question": the question chip appears on the way
        hear(self, "first host key", lead=0.2)
        hk = chip("host key?", 0.3, 0.55, size=36)
        self.play(FadeIn(hk), run_time=0.3)
        # "with yes": the question is answered
        hear(self, "with yes", lead=0.15)
        hk2 = chip("host key? yes", 0.3, 0.55, size=36)
        self.play(ReplacementTransform(hk, hk2), run_time=0.3)
        self.play(Create(check(2.2, 0.55, s=0.22, w=8)), run_time=0.25)
        # "type the password": dots fill the password chip
        hear(self, "type the password", lead=0.2)
        dots = chip("••••••", -2.6, 1.0, size=40)
        self.play(ReplacementTransform(pw, dots), run_time=0.4)
        # "land on a login node": the rack's light comes on
        hear(self, "land on a", lead=0.3)
        self.play(rlights[0].animate.set_color(TERRA), rlights[1].animate.set_color(TERRA), Indicate(rack, color=INK, scale_factor=1.04), run_time=0.6)
        # "no Duo prompt for ssh": a Duo chip beside the arrow, struck out
        hear(self, "no Duo", lead=0.3)
        duo1 = chip("Duo", -0.3, -1.9, size=36)
        self.play(FadeIn(duo1), run_time=0.3)
        cross = x_mark(1.0, -1.9, r=0.28, w=9)
        self.play(Create(cross), run_time=0.3)
        # "The web portal is different": a web portal box with a Duo chip
        hear(self, "web portal", lead=0.3)
        portal = Rectangle(width=1.8, height=1.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([5.1, 1.5, 0])
        plab = T("web portal", 36).move_to([5.0, 2.45, 0])
        duo2 = chip("Duo", 2.6, 1.5, size=36)
        self.play(FadeIn(portal), FadeIn(plab), FadeIn(duo2), run_time=0.4)
        # "the documentation says it asks": ticked, 'asks (documented)'
        hear(self, "says it asks", lead=0.6)
        tick = check(3.9, 1.5, s=0.24, w=9)
        alab = T("asks (documented)", 34).move_to([4.45, 0.55, 0])
        self.play(Create(tick), FadeIn(alab), run_time=0.5)
        done(self)


class B11_NotForClaude(Scene):
    """Claude's hand stops short of the password; a key slides in beside the logo and opens the door to the login rack."""
    def construct(self):
        claude = logo_chip("claude", -5.3, 1.4)
        you = professor_bear("1x1", 2.0, seed="B11x", x=-2.3, y=-1.2)
        ylab = T("you", 36).move_to([-2.3, -2.65, 0])
        pw = chip("••••••", -2.3, 1.4, size=40)
        door = Rectangle(width=1.0, height=3.4, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.9, -0.5, 0])
        iso = Iso(3.2, -2.2, 1.0)
        rack, rlights = explorer_rack(iso)
        rlab = T("login node", 36).move_to([4.0, -3.0, 0])
        self.play(FadeIn(claude), FadeIn(you), FadeIn(ylab), FadeIn(pw), FadeIn(door), FadeIn(rack), FadeIn(rlights), FadeIn(rlab), run_time=0.5)
        # "does not work for Claude": the hand reaches toward the password and is stopped
        hear(self, "does not work", lead=0.3)
        hand = Arrow([-4.5, 1.4, 0], [-3.95, 1.4, 0], buff=0, color=INK, stroke_width=9, max_tip_length_to_length_ratio=0.4)
        self.play(GrowArrow(hand), run_time=0.5)
        stop = x_mark(-3.65, 1.4, r=0.22, w=9)
        self.play(Create(stop), run_time=0.25)
        # "no keyboard attached": a keyboard-less label under the logo
        hear(self, "no keyboard", lead=0.3)
        nk = T("no keyboard", 36).move_to([-4.85, 2.6, 0])
        self.play(FadeIn(nk), run_time=0.3)
        # "never hand it": the password stays with you, the hand pulls back
        hear(self, "never hand", lead=0.3)
        self.play(FadeOut(hand), FadeOut(stop), run_time=0.3)
        # "something the agent can use": a key slides in beside the logo
        hear(self, "something the agent", lead=0.3)
        key = key_obj(-8.2, 0.25, s=0.7)
        self.add(key)
        self.play(key.animate.shift(RIGHT * 2.6), run_time=0.7, rate_func=smooth)
        # "A key": the key goes to the door; the door opens to the rack
        hear(self, "a key", lead=0.5, nth=1)
        self.play(FadeOut(nk), FadeOut(pw), key.animate.shift(RIGHT * 4.0), run_time=0.7, rate_func=smooth)
        self.play(door.animate.stretch_to_fit_width(0.3).shift(LEFT * 0.5), *[l.animate.set_color(TERRA) for l in rlights], run_time=0.6)
        done(self)


class B12_WhichLoginName(Scene):
    """The user ID from the access form works; the email prefix is the second try; wait after a password change."""
    def construct(self):
        c1 = chip("user ID", -3.0, 1.3, mono=True, size=40)
        cap1 = T("from the access form", 34).move_to([-3.0, 0.35, 0])
        c2 = chip("email prefix", 3.0, 1.3, mono=True, size=40)
        cap2 = T("second try", 34).move_to([3.0, 0.35, 0])
        title_anchor = c1  # keeps the first frame non-empty
        self.play(FadeIn(c1), FadeIn(cap1), run_time=0.5)
        # "the name from the access form": the user ID chip is ringed and ticked
        hear(self, "from the access form", lead=0.2)
        ring = RoundedRectangle(width=c1.pill.width + 0.35, height=1.15, corner_radius=0.57, color=INK, stroke_width=7).move_to([-3.0, 1.3, 0])
        tick = check(-0.6, 1.3, s=0.24, w=9)
        self.play(Create(ring), run_time=0.4)
        self.play(Create(tick), run_time=0.3)
        # "not the first part of an email address": the email prefix chip
        hear(self, "not the first part", lead=0.3)
        self.play(FadeIn(c2), run_time=0.3)
        # "try the other": the second try caption
        hear(self, "try the other", lead=0.3)
        self.play(FadeIn(cap2), run_time=0.3)
        # "wait a little after any password change": a clock lands under them
        hear(self, "wait a little", lead=0.5)
        clock = VGroup(Circle(radius=0.55, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=6),
                       Line([0, 0, 0], [0, 0.34, 0], color=INK, stroke_width=7),
                       Line([0, 0, 0], [0.26, 0, 0], color=INK, stroke_width=7),
                       Dot([0, 0, 0], radius=0.07, color=TERRA))
        clock.move_to([-4.2, -1.4, 0])
        self.play(FadeIn(clock, shift=UP * 1.0), run_time=0.7, rate_func=smooth)
        wl = T("wait after a password change", 36).move_to([0.9, -1.4, 0])
        self.play(FadeIn(wl), run_time=0.35)
        done(self)


# ═════════════════════════════ PART B — Act II and Act III drawings (B20 B30) ═════════════════════════════

def pB_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pB_tint(key, bow_fill, body_fill):
    """Recolour a key_obj: bow fill and shaft/teeth fill."""
    shaft, teeth, bow, hole = key
    bow.set_fill(bow_fill, 1)
    shaft.set_fill(body_fill, 1)
    for t in teeth:
        t.set_fill(body_fill, 1)
    return key


class B20_KeyPair(Scene):
    """A key in two halves: the private half stays with you; the public half is filed on Explorer's shelf; they match."""
    def construct(self):
        title = pB_act_title("II · Make And Install A Key")
        you = professor_bear("1x1", 2.3, seed="B20x", x=-5.05, y=-0.4)
        ylab = T("you", 38).move_to([-5.2, -2.25, 0])
        priv = pB_tint(key_obj(-3.3, 0.55, s=0.8), KRAFT_DEEP, BOX_R)
        lock = padlock(-3.3, -1.05, s=0.8)
        plab = T("private", 36).move_to([-1.75, -1.05, 0])
        iso = Iso(2.7, -2.3, 1.0)
        rack, rlights = explorer_rack(iso)
        elab = T("Explorer", 38).move_to([3.9, -2.7, 0])
        shelf = Rectangle(width=2.6, height=0.16, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.6, 0.15, 0])
        self.play(FadeIn(title), FadeIn(you), FadeIn(ylab), FadeIn(priv), FadeIn(lock), FadeIn(rack), FadeIn(rlights), FadeIn(elab), FadeIn(shelf), run_time=0.5)
        # "two halves": the lighter, lock-free public half appears above the private one
        hear(self, "two halves", lead=0.3)
        pub = pB_tint(key_obj(-3.3, 1.75, s=0.8), PAGE_TOP, PAGE_TOP)
        pubab = T("public", 36).move_to([-0.2, 1.75, 0])
        self.play(GrowFromCenter(pub), FadeIn(plab), run_time=0.5)
        self.play(FadeIn(pubab), run_time=0.25)
        # "stays on your computer": the padlock pulses
        hear(self, "stays on your computer", lead=0.1)
        self.play(Indicate(lock, color=INK, scale_factor=1.12), run_time=0.6)
        # "safe to hand out": the public half slides across to the login rack
        hear(self, "public half", lead=0.1)
        self.play(FadeOut(pubab), run_time=0.2)
        self.play(pub.animate.shift(RIGHT * 6.7 + DOWN * 0.3), run_time=1.0, rate_func=smooth)
        # "keep a copy": it is filed on the shelf and the rack light comes on
        hear(self, "keep a copy", lead=0.5)
        self.play(pub.animate.shift(DOWN * 0.95), rlights[0].animate.set_color(TERRA), run_time=0.6)
                # "your computer proves it holds the private half": the halves line up with a check
        hear(self, "proves it holds", lead=0.2)
        ck = check(0.5, 0.6, s=0.3, color=TERRA, w=10)
        gap = DashedLine([-1.0, 0.55, 0], [1.9, 0.55, 0], color=INK, stroke_width=4, dash_length=0.2)
        self.play(Create(gap), run_time=0.4)
        self.play(Create(ck), run_time=0.4)
        self.play(Indicate(pub, color=INK, scale_factor=1.1), Indicate(priv, color=INK, scale_factor=1.1), run_time=0.6)
        done(self)


class B30_UnlockOnce(Scene):
    """You type the passphrase once; the key goes into the agent; ssh asks the agent; the key never reaches Claude."""
    def construct(self):
        title = pB_act_title("III · Unlock It Once")
        you = professor_bear("1x1", 2.3, seed="B30x", x=-5.05, y=-0.5)
        ylab = T("you", 38).move_to([-5.2, -2.35, 0])
        key = key_obj(-3.1, -0.5, s=1.0)
        lock = padlock(-3.1, -0.5, s=1.1)
        iso = Iso(4.2, -2.0, 1.2)
        agent, alights = agent_slab(iso)
        alab = T("agent", 40).move_to([4.4, -3.0, 0])
        claude = logo_chip("claude", -1.6, 1.5)
        self.play(FadeIn(title), FadeIn(you), FadeIn(ylab), FadeIn(key), FadeIn(lock), FadeIn(agent), FadeIn(alights), FadeIn(alab), run_time=0.5)
        # "Claude cannot type a passphrase": the logo chip appears, a cross marks it
        hear(self, "Claude cannot type", lead=0.2)
        self.play(FadeIn(claude), run_time=0.3)
        hear(self, "a passphrase", lead=0.0)
        no = x_mark(0.2, 1.5, r=0.3, w=9)
        self.play(Create(no), run_time=0.3)
        # "you unlock the key yourself": the dots travel from you to the lock; it opens
        hear(self, "so you unlock", lead=0.0)
        self.play(FadeOut(claude), FadeOut(no), run_time=0.3)
        dots = chip("••••••", -4.4, 1.3, size=40)
        self.play(FadeIn(dots), run_time=0.3)
        self.play(dots.animate.move_to([-3.1, 0.9, 0]), run_time=0.6)
        self.play(unlock_anim(lock, rt=0.5), FadeOut(dots), run_time=0.5)
        # "into a helper called the ssh agent": the lock leaves, the key slides into the slab
        hear(self, "into a helper", lead=0.1)
        self.play(FadeOut(lock), run_time=0.2)
        self.play(key.animate.scale(0.6).move_to([4.4, 0.95, 0]), run_time=1.1, rate_func=smooth)
        # "the agent holds the unlocked key": light on, barrier line drawn
        hear(self, "holds the unlocked key", lead=0.2)
        self.play(alights[0].animate.set_color(TERRA), Indicate(agent, color=INK, scale_factor=1.04), run_time=0.6)
        bar = DashedLine([1.2, -2.6, 0], [1.2, 2.3, 0], color=BAR1, stroke_width=6, dash_length=0.3)
        self.play(Create(bar), run_time=0.4)
        # "ssh asks the agent": the Claude chip sends the ssh command box across
        hear(self, "ssh asks", lead=0.9)
        claude2 = logo_chip("claude", -2.6, 1.5)
        box = job_box(Iso(-2.9, -0.4, 0.9), 0, 0, 0, s=0.9)
        slab = M("ssh", 40).next_to(box, DOWN, buff=0.15)
        cmd = Group(box, slab)
        self.play(FadeIn(claude2), FadeIn(cmd), run_time=0.3)
        self.play(cmd.animate.shift(RIGHT * 4.8), run_time=0.8, rate_func=smooth)
        # "and the agent answers": a signed slip comes back; the key stays inside
        hear(self, "and the key never", lead=0.2)
        slip = Group(paper(0, 0, w=1.0, h=1.0, fill=PAGE_TOP), check(0, 0, s=0.28))
        slip.move_to([2.0, 1.5, 0])
        self.play(FadeIn(slip), run_time=0.2)
        self.play(slip.animate.move_to([-0.4, 1.5, 0]), run_time=0.6)
        # "never passes through Claude": a path from the key toward Claude is struck out
        hear(self, "passes through", lead=0.0)
        out = DashedLine([3.9, 0.95, 0], [3.3, 0.95, 0], color=BAR1, stroke_width=6, dash_length=0.2)
        self.play(Create(out), run_time=0.3)
        no2 = x_mark(3.0, 0.95, r=0.28, w=9)
        self.play(Create(no2), run_time=0.3)
        done(self)


# ═════════════════════════════ PART C — Act IV close and Act V (B42 B50 B51 B52) ═════════════════════════════

def pC_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pC_rule_chip(text, left, y, size=32):
    """A white rule pill, left edge at `left`; returns the chip group."""
    w = 0.165 * len(text) + 0.8
    return chip(text, left + w / 2, y, w=w, size=size)


def pC_stop(x, y, r=0.38):
    """A stop mark: ink octagon with a pale bar."""
    o = RegularPolygon(n=8, radius=r, start_angle=PI / 8, fill_color=INK, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y, 0])
    bar = Rectangle(width=r * 1.1, height=r * 0.3, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    return VGroup(o, bar)


class B42_AskBeforeChange(Scene):
    """Four rules land beside the agent at the login rack: read-only, ask first, no compute, stop on a prompt."""
    def construct(self):
        iso = Iso(-4.9, -2.55, 0.8)
        rack, rlights = explorer_rack(iso)
        rlab = T("login node", 36).move_to([-4.6, -3.0, 0])
        claude = logo_chip("claude", -5.1, 0.6, h=1.3)
        self.play(FadeIn(rack), FadeIn(rlights), FadeIn(rlab), FadeIn(claude), run_time=0.5)
        hear(self, "follows the rules", lead=0.3)
        self.play(Indicate(claude, color=INK, scale_factor=1.08), run_time=0.7)

        left = 0.0
        ys = [2.0, 0.7, -0.6, -1.9]
        ix = -2.0
        # rule 1: read-only first (ticked)
        hear(self, "Read only first", lead=0.35)
        c1 = pC_rule_chip("read-only first", left, ys[0])
        t1 = check(ix, ys[0], s=0.3, w=9)
        self.play(FadeIn(c1, shift=LEFT * 0.5), run_time=0.35)
        self.play(Create(t1), run_time=0.3)
        # rule 2: ask before submit, cancel, delete (a gate; the portrait holds the key)
        hear(self, "Ask before it submits", lead=0.4)
        c2 = pC_rule_chip("ask before submit, cancel, delete", left, ys[1])
        you = professor_bear("1x1", 1.0, seed="B42gate", x=-3.0, y=ys[1])
        key = key_obj(-2.35, ys[1] - 0.05, s=0.2)
        post1 = Line([-1.5, ys[1] - 0.45, 0], [-1.5, ys[1] + 0.45, 0], color=INK, stroke_width=8)
        post2 = Line([-0.8, ys[1] - 0.45, 0], [-0.8, ys[1] + 0.45, 0], color=INK, stroke_width=8)
        bar = Line([-1.5, ys[1] + 0.1, 0], [-0.8, ys[1] + 0.1, 0], color=INK, stroke_width=8)
        self.play(FadeIn(c2, shift=LEFT * 0.5), run_time=0.35)
        self.play(FadeIn(you), FadeIn(key), Create(post1), Create(post2), Create(bar), run_time=0.4)
        # rule 3: no compute on the login node (a crossed job box on the login rack)
        hear(self, "Never compute", lead=0.35)
        c3 = pC_rule_chip("no compute on the login node", left, ys[2])
        box = job_box(iso, 0.35, 0.35, 0.9, s=0.5)
        self.play(FadeIn(c3, shift=LEFT * 0.5), run_time=0.35)
        self.play(FadeIn(box, shift=DOWN * 0.5), run_time=0.4)
        no = x_mark(-4.9, -1.1, r=0.3, w=9)
        x3 = x_mark(ix, ys[2], r=0.3, w=9)
        self.play(Create(no), Create(x3), run_time=0.3)
        # rule 4: a prompt means stop
        hear(self, "if any command", lead=0.4)
        c4 = pC_rule_chip("prompt: stop and tell you", left, ys[3])
        st = pC_stop(ix, ys[3])
        self.play(FadeIn(c4, shift=LEFT * 0.5), run_time=0.35)
        self.play(GrowFromCenter(st), run_time=0.3)
        hear(self, "stops and tells you", lead=0.2)
        self.play(Indicate(st, color=TERRA, scale_factor=1.25), run_time=0.6)
        done(self)


class B50_ExplorerVsAICR(Scene):
    """A three-column table builds row by row; each differing cell gets a terracotta dot as it lands."""
    def construct(self):
        title = pC_act_title("V · How It Differs From AICR")
        cx = [-4.3, -0.25, 3.85]
        rows = [1.85, 0.95, 0.03, -0.89, -1.81, -2.73]      # header, then five rows
        left, right = -6.0, 5.9
        top = 2.35
        bottom = rows[-1] - 0.46
        frame = VGroup(
            Line([left, top, 0], [right, top, 0], color=INK, stroke_width=4),
            Line([left, bottom, 0], [right, bottom, 0], color=INK, stroke_width=4),
            Line([-2.55, top, 0], [-2.55, bottom, 0], color=BAR1, stroke_width=4),
            Line([1.8, top, 0], [1.8, bottom, 0], color=BAR1, stroke_width=4))
        h1 = T("Explorer", 38, bold=True).move_to([cx[1], rows[0], 0])
        h2 = T("AICR", 38, bold=True).move_to([cx[2], rows[0], 0])
        self.play(FadeIn(title), Create(frame), run_time=0.5)
        hear(self, "On Explorer", lead=0.5)
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.3)

        def rule(i):
            y = rows[i] - 0.46
            return Line([left, y, 0], [right, y, 0], color=BAR2, stroke_width=3)

        def cell(text, col, i, mono=False):
            lab = M(text, 32) if mono else T(text, 32)
            lab.move_to([cx[col], rows[i], 0])
            dot = Dot([cx[col] - lab.width / 2 - 0.28, rows[i], 0], radius=0.1, color=TERRA)
            return lab, dot

        def land(*pairs, rt=0.3):
            anims = []
            for lab, dot in pairs:
                anims += [FadeIn(lab), GrowFromCenter(dot)]
            self.play(*anims, run_time=rt)

        # row 1: starts with
        r1 = T("starts with", 36).move_to([cx[0], rows[1], 0])
        self.play(FadeIn(r1), Create(rule(1)), run_time=0.3)
        hear(self, "you start with your password", lead=0.35)
        land(cell("password", 1, 1))
        # row 2: key
        hear(self, "you make your own key", lead=0.5)
        r2 = T("key", 36).move_to([cx[0], rows[2], 0])
        self.play(FadeIn(r2), Create(rule(2)), run_time=0.3)
        land(cell("you make it", 1, 2))
        hear(self, "there is no password", lead=0.35)
        land(cell("no password", 2, 1))
        hear(self, "You download a key", lead=0.35)
        land(cell("you download it", 2, 2))
        # row 3: certificate
        hear(self, "in a certificate", lead=0.35)
        r3 = T("certificate", 36).move_to([cx[0], rows[3], 0])
        self.play(FadeIn(r3), Create(rule(3)), run_time=0.3)
        land(cell("none", 1, 3))
        hear(self, "Certificate Authority", lead=0.4)
        land(cell("signed by AICR", 2, 3))
        # row 4: user name
        hear(self, "Your Explorer username", lead=0.4)
        r4 = T("user name", 36).move_to([cx[0], rows[4], 0])
        self.play(FadeIn(r4), Create(rule(4)), run_time=0.3)
        hear(self, "your university login", lead=0.4)
        land(cell("your university login", 1, 4))
        hear(self, "Your AICR name", lead=0.3)
        land(cell("<aicr-username>", 2, 4, mono=True))
        # row 5: access
        hear(self, "And access comes", lead=0.4)
        r5 = T("access", 36).move_to([cx[0], rows[5], 0])
        self.play(FadeIn(r5), Create(rule(5)), run_time=0.3)
        hear(self, "a project sponsor", lead=0.4)
        land(cell("project sponsor", 1, 5))
        hear(self, "from a proposal", lead=0.4)
        land(cell("proposal", 2, 5))
        done(self)


def pC_tick_chip(text, x, y, size=34):
    """A white pill with a ticked label (the tick sits left of the text)."""
    lab = T(text, size)
    w = lab.width + 1.5
    c = chip(text, x, y, w=w, size=size)
    c.label.move_to([x + 0.3, y, 0])
    tk = check(x - w / 2 + 0.5, y, s=0.17, w=7)
    return VGroup(c, tk)


class B51_WhatIsTheSame(Scene):
    """Both racks reach the same agent: the key goes into it once; four ticks land."""
    def construct(self):
        iso1 = Iso(-4.6, -0.35, 1.0)
        ex, exl = explorer_rack(iso1)
        exlab = T("Explorer", 40).move_to([-4.2, -0.95, 0])
        iso2 = Iso(3.7, -0.65, 0.8)
        ai, ail = aicr_rack(iso2)
        ailab = T("AICR", 40).move_to([4.2, -1.1, 0])
        iso3 = Iso(0.3, -0.35, 0.9)
        ag, agl = agent_slab(iso3)
        aglab = T("agent", 38).move_to([0.3, -0.95, 0])
        self.play(FadeIn(ex), FadeIn(exl), FadeIn(exlab), FadeIn(ai), FadeIn(ail), FadeIn(ailab), FadeIn(ag), FadeIn(agl), FadeIn(aglab), run_time=0.5)
        # "both are ssh"
        hear(self, "both are SSH", lead=0.5)
        l1 = DashedLine([-2.6, 0.7, 0], [-1.0, 0.7, 0], color=BAR1, stroke_width=6, dash_length=0.2)
        l2 = DashedLine([1.6, 0.7, 0], [2.4, 0.7, 0], color=BAR1, stroke_width=6, dash_length=0.2)
        self.play(Create(l1), Create(l2), run_time=0.4)
        c1 = pC_tick_chip("ssh", -4.6, -1.8)
        self.play(FadeIn(c1, shift=UP * 0.3), run_time=0.3)
        # "unlock a key once into the agent"
        hear(self, "unlock a key once", lead=0.45)
        key = key_obj(-0.35, 2.3, s=0.6)
        self.play(FadeIn(key), run_time=0.25)
        c2 = pC_tick_chip("unlock once", -1.6, -1.8)
        self.play(FadeIn(c2, shift=UP * 0.3), run_time=0.3)
        self.play(key.animate.shift(DOWN * 1.65), run_time=0.7, rate_func=smooth)
        self.play(agl[0].animate.set_color(TERRA), run_time=0.3)
        # "tested with batch mode"
        hear(self, "tested with batch mode", lead=0.45)
        c3 = pC_tick_chip("BatchMode", 2.6, -1.8)
        self.play(FadeIn(c3, shift=UP * 0.3), run_time=0.3)
        # "Claude never holds your password, passphrase or key"
        hear(self, "Claude never holds", lead=0.45)
        c4 = pC_tick_chip("Claude never holds it", 0.0, -2.85)
        self.play(FadeIn(c4, shift=UP * 0.3), run_time=0.35)
        hear(self, "or your key", lead=0.3)
        self.play(Indicate(c4, color=INK, scale_factor=1.06), run_time=0.5)
        done(self)


def pC_dash_chip(text, left, y, size=32):
    lab = T(text, size)
    w = lab.width + 0.7
    x = left + w / 2
    body = RoundedRectangle(width=w, height=0.85, corner_radius=0.42, fill_color=PAGE_L, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    edge = DashedVMobject(RoundedRectangle(width=w, height=0.85, corner_radius=0.42, stroke_color=BAR1, stroke_width=5, fill_opacity=0).move_to([x, y, 0]), num_dashes=36)
    lab.move_to([x, y, 0])
    return VGroup(body, edge, lab)


class B52_NotTested(Scene):
    """Three untested things land with open rings; then the one email that settles them."""
    def construct(self):
        left = -3.0
        ring_x = left - 0.55
        items = [("off campus or another network", 1.7, "off campus"), ("the web portal", 0.5, "the web portal"), ("agent access policy", -0.7, "research computing")]
        for text, y, cue in items:
            hear(self, cue, lead=0.5)
            c = pC_dash_chip(text, left, y)
            ring = Circle(radius=0.24, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([ring_x, y, 0])
            self.play(FadeIn(c, shift=LEFT * 0.4), run_time=0.35)
            self.play(Create(ring), run_time=0.3)
        hear(self, "ask once", lead=0.45)
        lab = M("rchelp@northeastern.edu", 32)
        w = lab.width + 1.5
        mail = chip("rchelp@northeastern.edu", 0.4, -2.2, w=w, mono=True, size=34)
        mail.label.move_to([0.4 + 0.3, -2.2, 0])
        env = VGroup(Rectangle(width=0.62, height=0.42, stroke_color=INK, stroke_width=4, fill_opacity=0),
                     Line([-0.31, 0.21, 0], [0, -0.03, 0], color=INK, stroke_width=4),
                     Line([0.31, 0.21, 0], [0, -0.03, 0], color=INK, stroke_width=4)).move_to([0.4 - w / 2 + 0.55, -2.2, 0])
        self.play(FadeIn(mail, shift=UP * 0.4), run_time=0.4)
        self.play(Create(env), run_time=0.3)
        done(self)


for _cls in (B10_PasswordToday, B11_NotForClaude, B12_WhichLoginName, B20_KeyPair, B30_UnlockOnce, B42_AskBeforeChange, B50_ExplorerVsAICR, B51_WhatIsTheSame, B52_NotTested):
    _cls.play = ST.play
