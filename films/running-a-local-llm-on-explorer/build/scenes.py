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
_ASR = {"BOPEN": [["Research", 0.0], ["computing", 0.38], ["on", 0.78], ["Explorer", 1.02], ["and", 1.44], ["AICR,", 1.76], ["running", 2.84], ["a", 3.08], ["local", 3.26], ["LLM", 3.46], ["on", 4.14], ["Explorer,", 4.32], ["how", 5.2], ["to", 5.44], ["run", 5.58], ["an", 5.7], ["open", 5.84], ["model", 6.12], ["on", 6.46], ["a", 6.66], ["cluster", 6.82], ["GPU", 6.98], ["and", 7.44], ["point", 7.84], ["a", 8.02], ["coding", 8.14], ["agent", 8.42], ["like", 8.78], ["Claude", 9.0], ["Code", 9.26], ["at", 9.56], ["it,", 9.82], ["what", 10.14], ["that", 10.26], ["saves", 10.44], ["and", 10.84], ["what", 11.16], ["it", 11.32], ["really", 11.42], ["costs.", 11.6]], "BIDEA": [["Hello,", 0.68], ["this", 1.34], ["is", 1.44], ["Liam", 1.66], ["in", 1.94], ["for", 2.22], ["Bear,", 2.4], ["first", 3.06], ["a", 3.22], ["correction,", 3.4], ["a", 4.18], ["local", 4.28], ["model", 4.54], ["on", 4.88], ["the", 5.08], ["cluster", 5.2], ["is", 5.44], ["not", 5.66], ["free", 5.88], ["and", 6.22], ["always", 6.44], ["running,", 6.68], ["it", 7.36], ["runs", 7.46], ["inside", 7.66], ["a", 8.14], ["GPU", 8.34], ["job", 8.62], ["you", 9.04], ["ask", 9.26], ["for,", 9.46], ["there", 10.06], ["is", 10.16], ["no", 10.26], ["per", 10.48], ["token", 10.66], ["billing", 10.88], ["but", 11.22], ["the", 11.58], ["cost", 11.72], ["moves", 11.94], ["to", 12.26], ["queue", 12.5], ["time", 12.7], ["and", 13.0], ["fair", 13.22], ["share.", 13.42]], "BDEFS": [["Five", 0.0], ["terms,", 0.3], ["Olama,", 0.98], ["the", 1.38], ["program", 1.48], ["that", 1.78], ["serves", 2.04], ["an", 2.26], ["open", 2.48], ["model,", 2.76], ["Aptainer,", 3.74], ["a", 4.3], ["tool", 4.36], ["that", 4.54], ["runs", 4.76], ["containers", 5.04], ["without", 5.58], ["root,", 5.94], ["a", 6.52], ["slurm", 6.6], ["job,", 7.02], ["your", 7.42], ["request", 7.48], ["for", 7.8], ["compute", 8.04], ["node,", 8.34], ["a", 9.06], ["harness,", 9.08], ["the", 9.58], ["coding", 9.68], ["agent", 9.96], ["that", 10.28], ["sends", 10.48], ["the", 10.72], ["requests", 10.9], ["in", 11.28], ["a", 11.64], ["context", 11.76], ["window,", 12.14], ["how", 12.72], ["much", 12.92], ["text", 13.1], ["the", 13.38], ["model", 13.58], ["can", 13.84], ["see", 14.06], ["at", 14.28], ["once.", 14.42]], "B10": [["Here's", 0.0], ["the", 0.28], ["idea.", 0.42], ["You", 1.02], ["ask", 1.04], ["Slurm", 1.28], ["for", 1.64], ["a", 1.82], ["GPU.", 2.0], ["On", 2.72], ["that", 2.8], ["GPU", 2.96], ["you", 3.32], ["run", 3.6], ["an", 3.78], ["open", 3.92], ["model,", 4.2], ["and", 4.96], ["a", 5.06], ["coding", 5.18], ["agent", 5.44], ["like", 5.78], ["Claude", 6.02], ["Code", 6.32], ["sends", 6.62], ["it", 6.96], ["requests", 7.12], ["and", 7.56], ["runs", 7.86], ["tools", 8.12], ["on", 8.42], ["your", 8.64], ["files.", 8.76], ["There", 9.74], ["is", 9.84], ["no", 9.94], ["per", 10.14], ["token", 10.34], ["bill", 10.6], ["because", 10.94], ["the", 11.34], ["model", 11.5], ["is", 11.76], ["yours", 12.0], ["for", 12.22], ["as", 12.52], ["long", 12.62], ["as", 12.78], ["the", 12.92], ["job", 13.04], ["runs.", 13.3]], "B11": [["There", 0.0], ["are", 0.12], ["three", 0.26], ["layers.", 0.46], ["The", 1.02], ["model", 1.04], ["host", 1.24], ["is", 1.52], ["Olama", 1.74], ["inside", 2.28], ["an", 2.66], ["Aptainer", 2.88], ["container", 3.22], ["on", 3.6], ["a", 3.9], ["GPU", 4.06], ["node", 4.32], ["that", 4.7], ["Slurm", 4.94], ["gave", 5.34], ["you.", 5.52], ["The", 6.3], ["harness", 6.4], ["is", 6.6], ["the", 6.84], ["coding", 7.02], ["agent,", 7.26], ["Claude", 8.04], ["code,", 8.06], ["Ader,", 8.76], ["or", 9.0], ["continue,", 9.18], ["and", 9.9], ["the", 10.08], ["transport", 10.2], ["is", 10.58], ["whatever", 10.86], ["joins", 11.14], ["them,", 11.58], ["nothing", 12.18], ["if", 12.4], ["they", 12.68], ["share", 12.84], ["a", 13.04], ["machine", 13.16], ["or", 13.5], ["an", 13.9], ["SSH", 14.02], ["tunnel.", 14.34]], "B12": [["Patterna", 0.0], ["keeps", 0.44], ["everything", 0.62], ["on", 1.14], ["the", 1.36], ["GPU", 1.52], ["node.", 1.84], ["The", 2.68], ["agent", 2.72], ["and", 2.98], ["the", 3.22], ["model", 3.32], ["run", 3.62], ["in", 3.9], ["the", 4.04], ["same", 4.18], ["job,", 4.42], ["so", 5.0], ["nothing", 5.14], ["crosses", 5.38], ["a", 5.74], ["network,", 6.02], ["and", 6.62], ["your", 6.68], ["code", 6.8], ["stays", 7.08], ["on", 7.4], ["Northeastern", 7.64], ["storage.", 8.14], ["Use", 9.26], ["it", 9.42], ["unless", 9.6], ["you", 9.84], ["have", 10.06], ["a", 10.2], ["specific", 10.38], ["reason", 10.64], ["not", 11.04], ["to.", 11.36]], "B13": [["Pattern", 0.0], ["B", 0.26], ["keeps", 0.48], ["your", 0.74], ["editor", 0.94], ["on", 1.18], ["your", 1.38], ["laptop,", 1.52], ["only", 2.38], ["the", 2.56], ["model's", 2.74], ["traffic", 3.1], ["goes", 3.46], ["to", 3.72], ["the", 3.96], ["cluster", 4.06], ["through", 4.4], ["an", 4.8], ["SSH", 4.96], ["tunnel", 5.3], ["to", 5.8], ["the", 6.04], ["login", 6.16], ["node", 6.38], ["and", 6.8], ["on", 7.1], ["to", 7.28], ["the", 7.46], ["GPU", 7.58], ["node,", 7.9], ["so", 8.84], ["the", 9.02], ["model", 9.16], ["must", 9.42], ["be", 9.66], ["reachable", 9.86], ["from", 10.28], ["the", 10.48], ["login", 10.62], ["node", 10.88], ["and", 11.3], ["that", 11.6], ["needs", 11.74], ["a", 11.94], ["lock", 12.12], ["in", 12.34], ["front", 12.54], ["of", 12.72], ["it.", 12.84]], "B20": [["Advice", 0.0], ["that", 0.28], ["circulates", 0.54], ["about", 1.1], ["this", 1.34], ["setup", 1.54], ["has", 1.82], ["traps,", 2.08], ["first", 2.8], ["the", 2.96], ["network,", 3.18], ["Olama", 3.96], ["has", 4.24], ["no", 4.46], ["authentication", 4.7], ["and", 5.59], ["its", 5.86], ["container", 6.02], ["image", 6.42], ["listens", 6.76], ["on", 7.14], ["every", 7.4], ["address", 7.68], ["by", 8.02], ["default,", 8.26], ["on", 9.24], ["a", 9.32], ["shared", 9.48], ["cluster", 9.66], ["that", 10.04], ["opens", 10.3], ["the", 10.62], ["whole", 10.82], ["interface", 11.0], ["including", 11.44], ["pulling", 11.9], ["and", 12.34], ["deleting", 12.58], ["models", 12.84], ["to", 13.28], ["anyone", 13.68], ["who", 13.9], ["can", 14.12], ["reach", 14.26], ["the", 14.5], ["node.", 14.7]], "B21": [["Inside", 0.0], ["Aptainer,", 0.36], ["the", 1.08], ["image", 1.1], ["zone", 1.36], ["setting", 1.6], ["beats", 1.98], ["a", 2.2], ["plain", 2.4], ["export", 2.6], ["from", 3.0], ["your", 3.26], ["shell,", 3.4], ["so", 4.0], ["pass", 4.3], ["the", 4.52], ["address", 4.72], ["with", 4.98], ["the", 5.22], ["end", 5.38], ["flag", 5.56], ["bound", 5.98], ["to", 6.44], ["local", 6.68], ["host", 6.9], ["on", 7.26], ["a", 7.48], ["random", 7.6], ["port.", 7.86], ["That", 8.62], ["is", 8.66], ["what", 8.78], ["the", 8.96], ["start", 9.12], ["script", 9.32], ["does.", 9.64]], "B22": [["Second,", 0.0], ["the", 0.52], ["address,", 0.52], ["Claude", 1.32], ["code", 1.34], ["add", 1.68], ["slash", 1.98], ["v1", 2.3], ["slash", 2.78], ["messages", 3.16], ["itself,", 3.62], ["and", 4.46], ["the", 4.54], ["documented", 4.64], ["examples", 5.08], ["give", 5.62], ["a", 5.86], ["bare", 6.0], ["host", 6.16], ["and", 6.44], ["port.", 6.68], ["A", 7.66], ["base", 7.76], ["address", 7.98], ["that", 8.28], ["already", 8.54], ["ends", 8.78], ["in", 9.12], ["slash", 9.26], ["v1", 9.58], ["doubles", 10.14], ["the", 10.48], ["path", 10.74], ["and", 11.04], ["the", 11.28], ["request", 11.38], ["fails.", 11.66], ["Give", 12.6], ["it", 12.68], ["the", 12.78], ["bare", 12.9], ["host", 13.08], ["and", 13.38], ["port.", 13.6]], "B23": [["And", 0.0], ["the", 0.14], ["tunnel,", 0.26], ["local", 0.96], ["host", 0.96], ["on", 1.26], ["the", 1.48], ["far", 1.62], ["side", 1.82], ["of", 2.08], ["a", 2.18], ["tunnel", 2.3], ["means", 2.52], ["the", 2.78], ["login", 3.04], ["node,", 3.32], ["not", 4.0], ["the", 4.1], ["machine", 4.26], ["running", 4.58], ["your", 4.88], ["model.", 5.12], ["The", 6.08], ["target", 6.2], ["has", 6.44], ["to", 6.72], ["be", 6.86], ["the", 6.98], ["compute", 7.12], ["node,", 7.4], ["because", 7.98], ["research", 8.26], ["computing", 8.64], ["does", 9.08], ["not", 9.34], ["support", 9.58], ["SSH", 10.0], ["straight", 10.5], ["into", 11.16], ["a", 11.5], ["GPU", 11.66], ["node.", 11.96]], "B24": [["Third,", 0.0], ["the", 0.42], ["model", 0.44], ["names,", 0.68], ["Claude", 1.48], ["Code", 1.48], ["uses", 1.78], ["its", 2.12], ["small", 2.3], ["model", 2.58], ["for", 2.82], ["background", 3.1], ["tasks", 3.46], ["in", 3.92], ["a", 4.2], ["separate", 4.34], ["setting", 4.56], ["for", 4.92], ["subagents.", 5.14], ["Unless", 6.48], ["you", 6.66], ["point", 6.84], ["those", 7.06], ["at", 7.28], ["your", 7.46], ["local", 7.56], ["model,", 7.84], ["Olama", 8.54], ["can", 8.88], ["be", 9.0], ["asked", 9.12], ["for", 9.32], ["Claude", 9.56], ["models", 9.8], ["it", 10.12], ["does", 10.32], ["not", 10.44], ["have,", 10.66], ["so", 11.24], ["the", 11.5], ["script", 11.64], ["sets", 11.82], ["the", 12.16], ["small,", 12.42], ["medium,", 12.98], ["and", 13.44], ["large", 13.54], ["names", 13.76], ["in", 14.16], ["the", 14.48], ["subagent", 14.6], ["model", 15.02], ["to", 15.44], ["one", 15.72], ["local", 15.92], ["model.", 16.26]], "B25": [["Fourth", 0.0], ["context,", 0.3], ["Olama", 1.28], ["sizes", 1.62], ["its", 1.92], ["default", 2.24], ["window", 2.6], ["by", 2.98], ["video", 3.22], ["memory.", 3.5], ["4", 4.3], [",000", 4.42], ["tokens", 4.88], ["under", 5.14], ["24", 5.36], ["gigabytes,", 5.86], ["32", 6.58], [",000", 6.78], ["up", 7.38], ["to", 7.48], ["48.", 7.68], ["Claude", 8.72], ["Code's", 8.78], ["instructions", 9.18], ["and", 9.72], ["tool", 9.96], ["list", 10.14], ["alone", 10.4], ["overflow", 10.76], ["a", 11.2], ["small", 11.38], ["window,", 11.64], ["and", 12.3], ["the", 12.44], ["overflow", 12.54], ["is", 12.92], ["cut", 13.14], ["without", 13.38], ["any", 13.68], ["error.", 13.88], ["Ask", 14.7], ["for", 14.84], ["65", 15.04], [",536", 15.6], ["or", 16.4], ["more.", 17.24]], "B26": [["Fifth,", 0.0], ["the", 0.54], ["model,", 0.54], ["a", 1.06], ["one", 1.14], ["and", 1.3], ["a", 1.44], ["half", 1.58], ["billion", 1.78], ["parameter", 2.06], ["reasoning", 2.66], ["model,", 3.06], ["cannot", 3.62], ["reliably", 3.88], ["drive", 4.42], ["an", 4.84], ["agent", 5.04], ["loop", 5.36], ["with", 5.6], ["dozens", 5.9], ["of", 6.2], ["tool", 6.46], ["definitions.", 6.68], ["Use", 8.08], ["a", 8.28], ["tool", 8.44], ["-capable", 8.68], ["coding", 9.14], ["model", 9.5], ["in", 9.9], ["the", 10.3], ["range", 10.4], ["of", 10.64], ["20", 10.82], ["to", 11.2], ["120", 11.48], ["billion", 12.02], ["parameters.", 12.4]], "B27": [["and", 0.0], ["drop", 0.12], ["the", 0.32], ["word", 0.48], ["zero", 0.66], ["marginal", 1.06], ["cost.", 1.48], ["GPU", 2.68], ["hours", 2.68], ["count", 3.1], ["against", 3.4], ["fair", 3.7], ["share.", 3.92], ["You", 4.4], ["wait", 4.46], ["in", 4.62], ["a", 4.72], ["queue", 4.84], ["and", 5.08], ["an", 5.32], ["idle", 5.44], ["watcher", 5.7], ["cancels", 6.14], ["jobs.", 6.58], ["The", 7.3], ["accurate", 7.32], ["claim", 7.6], ["is", 7.92], ["no", 8.08], ["per", 8.3], ["token", 8.5], ["billing.", 8.7], ["The", 9.68], ["cost", 9.88], ["moves", 10.14], ["to", 10.46], ["queue", 10.68], ["time,", 10.86], ["fair", 11.54], ["share", 11.64], ["and", 11.92], ["capability.", 12.16]], "B30": [["Setup", 0.0], ["starts", 0.24], ["with", 0.58], ["one", 0.8], ["small", 1.02], ["environment", 1.36], ["file,", 1.82], ["it", 2.56], ["says", 2.64], ["where", 2.82], ["the", 3.02], ["image", 3.18], ["is,", 3.38], ["the", 3.78], ["models", 3.86], ["and", 4.08], ["the", 4.4], ["container", 4.54], ["cache", 4.9], ["live.", 5.24], ["The", 6.1], ["default", 6.2], ["is", 6.46], ["Scratch,", 6.68], ["which", 7.3], ["is", 7.38], ["purged", 7.56], ["on", 7.94], ["the", 8.06], ["first", 8.18], ["Tuesday", 8.4], ["of", 8.78], ["every", 8.96], ["month.", 9.2], ["Model", 10.06], ["weights", 10.06], ["belong", 10.32], ["in", 10.7], ["project", 10.96], ["space,", 11.2], ["and", 11.94], ["on", 12.04], ["one", 12.16], ["real", 12.4], ["account", 12.6], ["Scratch", 12.96], ["was", 13.32], ["not", 13.58], ["even", 13.82], ["writable.", 14.06]], "B31": [["Aptainer", 0.0], ["otherwise", 0.42], ["caches", 0.84], ["into", 1.3], ["a", 1.58], ["hidden", 1.74], ["folder", 1.88], ["in", 2.28], ["Home,", 2.52], ["and", 2.94], ["Home", 3.1], ["fills", 3.34], ["first.", 3.68], ["So", 4.82], ["point", 5.02], ["its", 5.24], ["cache", 5.44], ["and", 5.78], ["temporary", 5.98], ["folders", 6.4], ["at", 6.9], ["your", 7.1], ["own", 7.22], ["storage,", 7.36], ["and", 8.06], ["pull", 8.2], ["the", 8.38], ["images", 8.52], ["there", 8.8], ["on", 9.18], ["a", 9.52], ["compute", 9.66], ["node", 9.9], ["rather", 10.26], ["than", 10.54], ["the", 10.8], ["login", 10.9], ["node.", 11.16]], "B32": [["Then", 0.0], ["two", 0.16], ["pulls", 0.42], ["olama", 0.78], ["and", 1.38], ["a", 1.5], ["small", 1.6], ["web", 1.84], ["server", 2.06], ["called", 2.34], ["caddy", 2.7], ["that", 3.04], ["the", 3.26], ["laptop", 3.4], ["pattern", 3.8], ["will", 4.14], ["need.", 4.36], ["Check", 5.08], ["the", 5.24], ["version", 5.42], ["it", 5.66], ["prints,", 5.86], ["you", 6.36], ["need", 6.48], ["0", 6.64], [".14", 7.06], ["or", 7.8], ["later,", 7.96], ["and", 8.6], ["once", 8.68], ["something", 8.84], ["works,", 9.14], ["pin", 9.64], ["the", 9.72], ["version", 9.88], ["instead", 10.14], ["of", 10.44], ["latest", 10.58], ["so", 10.84], ["a", 11.24], ["whole", 11.38], ["class", 11.56], ["does", 11.88], ["not", 12.1], ["drift.", 12.34]], "B33": [["The", 0.0], ["start", 0.18], ["script", 0.36], ["runs", 0.66], ["inside", 0.98], ["every", 1.46], ["GPU", 1.86], ["job.", 2.2], ["It", 3.2], ["picks", 3.28], ["a", 3.46], ["random", 3.62], ["free", 3.9], ["port,", 4.24], ["binds", 4.92], ["Olama", 5.1], ["to", 5.54], ["localhost", 5.68], ["only,", 6.18], ["sets", 6.88], ["the", 7.08], ["context", 7.3], ["length,", 7.66], ["and", 8.28], ["defines", 8.36], ["an", 8.66], ["Olama", 8.88], ["function", 9.34], ["that", 9.52], ["talks", 9.88], ["to", 10.1], ["your", 10.36], ["server,", 10.48], ["not", 11.12], ["the", 11.28], ["container's", 11.44], ["default", 12.04], ["port.", 12.32]], "B34": [["The", 0.0], ["Claude", 0.16], ["Code", 0.34], ["script", 0.58], ["sets", 0.92], ["the", 1.22], ["base", 1.46], ["address", 1.64], ["to", 1.9], ["your", 2.12], ["port,", 2.26], ["a", 2.8], ["placeholder", 2.84], ["token,", 3.22], ["and", 3.96], ["every", 4.08], ["model", 4.38], ["alias", 4.72], ["to", 5.12], ["your", 5.36], ["local", 5.46], ["model.", 5.74], ["Look", 6.7], ["at", 6.8], ["the", 6.92], ["first", 7.02], ["line.", 7.26], ["It", 8.02], ["clears", 8.12], ["any", 8.38], ["real", 8.62], ["API", 8.94], ["key,", 9.46], ["which", 10.02], ["would", 10.16], ["otherwise", 10.3], ["be", 10.6], ["sent", 10.9], ["to", 11.12], ["whatever", 11.32], ["is", 11.5], ["listening", 11.84], ["at", 12.16], ["that", 12.4], ["address.", 12.56]], "B35": [["Pattern", 0.0], ["B", 0.3], ["needs", 0.54], ["one", 0.78], ["persistent", 1.06], ["token,", 1.46], ["a", 2.2], ["random", 2.28], ["number", 2.56], ["kept", 2.92], ["in", 3.1], ["a", 3.3], ["file", 3.4], ["only", 3.7], ["you", 4.02], ["can", 4.22], ["read.", 4.38], ["Regenerate", 5.2], ["it", 5.72], ["any", 5.82], ["time", 6.0], ["to", 6.24], ["revoke", 6.46], ["access.", 6.78], ["Then", 7.72], ["leave", 7.8], ["the", 8.0], ["setup", 8.18], ["node", 8.38], ["and", 8.74], ["install", 9.02], ["clod", 9.38], ["code", 9.78], ["on", 10.1], ["the", 10.38], ["login", 10.5], ["node.", 10.74], ["It", 11.42], ["is", 11.48], ["a", 11.58], ["small", 11.72], ["download.", 12.0]], "B40": [["Two", 0.0], ["numbers", 0.16], ["decide", 0.44], ["whether", 0.92], ["this", 1.22], ["works.", 1.48], ["The", 2.16], ["model's", 2.26], ["weights", 2.66], ["must", 2.82], ["fit", 3.08], ["in", 3.36], ["video", 3.52], ["memory,", 3.72], ["and", 4.38], ["there", 4.48], ["must", 4.6], ["be", 4.74], ["room", 4.94], ["left", 5.12], ["for", 5.4], ["the", 5.64], ["context", 5.76], ["window's", 6.18], ["cache.", 6.76], ["If", 7.62], ["either", 7.8], ["spills", 7.98], ["over,", 8.28], ["Olama", 9.0], ["pushes", 9.4], ["layers", 9.66], ["onto", 9.96], ["the", 10.24], ["processor,", 10.44], ["and", 11.22], ["generation", 11.34], ["slows", 11.66], ["to", 12.18], ["a", 12.48], ["crawl.", 12.62]], "B41": [["Models", 0.0], ["that", 0.3], ["fit", 0.56], ["by", 0.8], ["download", 1.06], ["size.", 1.46], ["The", 2.44], ["20", 2.48], ["billion", 2.74], ["GPT", 3.04], ["-OSS", 3.62], ["is", 4.12], ["about", 4.54], ["14", 4.8], ["gigabytes.", 5.34], ["The", 6.36], ["30", 6.44], ["billion", 6.64], ["QUEN", 7.0], ["-3", 7.24], ["coder", 7.46], ["is", 7.76], ["about", 7.94], ["19.", 8.2], ["GLM", 9.16], ["4", 9.74], [".7", 10.0], ["Flash", 10.74], ["is", 10.98], ["also", 11.28], ["about", 11.6], ["19", 11.86], ["to", 12.3], ["download,", 12.5], ["but", 13.3], ["Olama", 13.46], ["puts", 13.94], ["it", 14.08], ["near", 14.22], ["23", 14.38], ["of", 14.84], ["video", 15.04], ["memory", 15.26], ["at", 15.66], ["64", 15.94], [",000", 16.4], ["context.", 16.98]], "B42": [["And", 0.0], ["the", 0.12], ["120", 0.22], ["billion", 0.66], ["GPT", 1.12], ["-OSS,", 1.86], ["about", 2.84], ["65", 3.1], ["gigabytes,", 3.8], ["is", 4.44], ["the", 4.66], ["strongest", 4.8], ["of", 5.12], ["these", 5.44], ["that", 5.62], ["fits", 5.84], ["on", 6.08], ["one", 6.28], ["card.", 6.46], ["Before", 7.2], ["you", 7.44], ["pull", 7.6], ["any", 7.78], ["model,", 7.98], ["check", 8.56], ["its", 8.68], ["page", 8.9], ["for", 9.16], ["the", 9.44], ["tool's", 9.58], ["label.", 9.88], ["A", 10.64], ["model", 10.76], ["without", 11.02], ["tool", 11.36], ["support,", 11.72], ["Prince", 12.42], ["Tool", 12.44], ["calls", 12.72], ["as", 13.06], ["plain", 13.28], ["text", 13.56], ["instead", 13.88], ["of", 14.26], ["running", 14.42], ["them.", 14.62]], "B43": [["The", 0.0], ["GPU", 0.18], ["partition", 0.46], ["gives", 0.9], ["1", 1.26], ["GPU", 1.6], ["per", 1.9], ["job,", 2.22], ["so", 2.82], ["stay", 2.88], ["inside", 3.12], ["one", 3.44], ["card,", 3.72], ["and", 4.46], ["H200", 4.58], ["has", 5.16], ["about", 5.5], ["140", 5.7], ["GB,", 6.36], ["and", 7.12], ["every", 7.26], ["model", 7.54], ["on", 7.8], ["that", 7.98], ["list", 8.14], ["fits", 8.32], ["with", 8.56], ["room", 8.8], ["for", 9.0], ["a", 9.24], ["large", 9.36], ["context.", 9.6], ["Older", 11.0], ["cards", 11.18], ["like", 11.5], ["V100", 11.72], ["and", 12.32], ["T4", 12.54], ["may", 13.04], ["fall", 13.24], ["back", 13.48], ["to", 13.74], ["the", 13.92], ["processor,", 14.04], ["so", 14.7], ["check", 14.9], ["the", 15.16], ["log", 15.34], ["and", 15.56], ["ask", 15.92], ["for", 16.14], ["a", 16.36], ["newer", 16.46], ["type.", 16.6]], "B44": [["On", 0.0], ["context,", 0.18], ["$65", 0.88], [",000", 1.32], ["is", 1.84], ["the", 2.0], ["floor", 2.14], ["for", 2.36], ["coding", 2.62], ["agents,", 2.94], ["and", 3.58], ["on", 3.74], ["an", 3.84], ["H200", 3.92], ["you", 4.5], ["can", 4.86], ["raise", 5.0], ["it", 5.2], ["for", 5.38], ["long", 5.56], ["sessions.", 5.8], ["If", 7.04], ["memory", 7.16], ["is", 7.38], ["tight,", 7.7], ["storing", 8.3], ["the", 8.48], ["cache", 8.68], ["at", 8.88], ["8", 9.08], ["bits", 9.24], ["roughly", 9.52], ["halves", 9.76], ["its", 10.16], ["size,", 10.36], ["at", 11.04], ["a", 11.16], ["small", 11.26], ["cost", 11.54], ["in", 11.84], ["quality.", 12.08]], "B50": [["Start", 0.0], ["with", 0.26], ["an", 0.44], ["interactive", 0.58], ["GPU", 1.04], ["session.", 1.56], ["The", 2.58], ["GPU", 2.62], ["interactive", 2.94], ["partition", 3.46], ["defaults", 3.98], ["to", 4.44], ["one", 4.74], ["hour,", 4.92], ["allows", 5.4], ["two,", 5.68], ["and", 6.32], ["gives", 6.38], ["one", 6.52], ["GPU.", 6.8], ["Asking", 7.9], ["for", 8.18], ["a", 8.34], ["specific", 8.44], ["type", 8.76], ["can", 9.12], ["lengthen", 9.38], ["the", 9.76], ["weight", 9.88], ["and", 10.1], ["consider", 10.48], ["TMUX", 10.86], ["first,", 11.3], ["so", 11.78], ["a", 11.98], ["dropped", 12.14], ["connection", 12.28], ["does", 12.82], ["not", 13.04], ["kill", 13.28], ["your", 13.52], ["session.", 13.7]], "B51": [["Source", 0.0], ["the", 0.24], ["start", 0.44], ["script,", 0.66], ["pull", 1.22], ["the", 1.36], ["model,", 1.52], ["then", 2.0], ["prove", 2.12], ["it.", 2.38], ["Send", 2.96], ["one", 3.1], ["message", 3.34], ["to", 3.66], ["the", 3.9], ["anthropic", 4.02], ["compatible", 4.52], ["address", 4.88], ["and", 5.4], ["run", 5.74], ["Olama", 5.96], ["PS.", 6.56], ["The", 7.5], ["processor", 7.6], ["should", 7.92], ["read", 8.24], ["100", 8.42], ["%", 8.84], ["GPU", 9.26], ["and", 9.62], ["the", 10.16], ["context", 10.26], ["should", 10.66], ["match", 10.94], ["what", 11.18], ["you", 11.42], ["asked", 11.56], ["for.", 11.78]], "B52": [["Configure", 0.0], ["Claude", 0.52], ["code", 0.72], ["for", 1.0], ["this", 1.24], ["session,", 1.4], ["go", 2.0], ["to", 2.1], ["your", 2.26], ["project", 2.36], ["and", 2.72], ["start", 3.06], ["it.", 3.34], ["Inside,", 4.62], ["run", 4.98], ["slash", 5.06], ["status", 5.38], ["to", 5.8], ["confirm", 6.04], ["it", 6.36], ["is", 6.6], ["using", 6.76], ["your", 7.02], ["local", 7.18], ["address", 7.46], ["and", 7.84], ["not", 8.14], ["enthropics.", 8.3]], "B53": [["Know", 0.0], ["the", 0.18], ["limits,", 0.32], ["Anthropic's", 0.84], ["documentation", 1.38], ["says", 1.92], ["it", 2.34], ["does", 2.5], ["not", 2.62], ["support", 2.82], ["pointing", 3.2], ["Claude", 3.6], ["code", 3.86], ["at", 4.14], ["non", 4.34], ["-Claud", 4.56], ["models,", 4.8], ["so", 5.52], ["this", 5.7], ["works", 5.84], ["through", 6.06], ["documented", 6.34], ["settings", 6.82], ["but", 7.28], ["is", 7.6], ["an", 7.72], ["unsupported", 7.82], ["route.", 8.28], ["Claude", 9.58], ["code's", 9.7], ["built", 10.12], ["-in", 10.26], ["web", 10.46], ["search", 10.62], ["runs", 10.9], ["on", 11.26], ["Anthropic's", 11.48], ["own", 12.14], ["back", 12.28], ["-end,", 12.52], ["and", 13.2], ["Olama's", 13.26], ["layer", 13.7], ["does", 13.9], ["not", 14.14], ["fully", 14.4], ["support", 14.7], ["hosted", 15.12], ["web", 15.54], ["search,", 15.78], ["prompt", 16.46], ["caching", 16.64], ["is", 17.08], ["not", 17.32], ["supported", 17.54], ["either.", 18.0]], "B54": [["So", 0.0], ["long", 0.16], ["sessions", 0.44], ["slow", 0.8], ["down", 1.12], ["as", 1.42], ["the", 1.6], ["context", 1.74], ["grows", 2.16], ["because", 2.54], ["nothing", 2.92], ["is", 3.2], ["cached,", 3.44], ["keep", 4.24], ["tool", 4.44], ["servers", 4.68], ["few", 5.06], ["since", 5.4], ["every", 5.68], ["definition", 6.02], ["uses", 6.4], ["context,", 6.78], ["and", 7.76], ["when", 7.88], ["you", 7.98], ["finish", 8.12], ["exit", 8.42], ["twice,", 8.78], ["clod", 9.58], ["code", 9.74], ["then", 10.04], ["the", 10.34], ["job", 10.48], ["which", 10.76], ["returns", 11.04], ["the", 11.42], ["GPU.", 11.68]], "B55": [["For", 0.0], ["unattended", 0.14], ["work,", 0.6], ["run", 1.06], ["clod", 1.18], ["code", 1.5], ["headless", 1.76], ["inside", 2.22], ["a", 2.58], ["batch", 2.76], ["job.", 2.92], ["The", 3.82], ["GPU", 3.9], ["stays", 4.16], ["busy", 4.58], ["for", 4.9], ["the", 5.08], ["whole", 5.18], ["job,", 5.38], ["so", 5.84], ["the", 5.98], ["idle", 6.14], ["watcher", 6.36], ["leaves", 6.74], ["it", 6.92], ["alone.", 7.1], ["Put", 7.74], ["the", 7.84], ["repository", 7.94], ["on", 8.28], ["a", 8.6], ["fresh", 8.72], ["branch", 8.92], ["and", 9.28], ["review", 9.54], ["the", 9.76], ["diff", 9.92], ["before", 10.08], ["you", 10.38], ["merge", 10.52], ["anything.", 10.74], ["Except", 12.0], ["edits", 12.1], ["lets", 12.38], ["it", 12.64], ["change", 12.82], ["files", 13.06], ["and", 13.52], ["simple", 13.82], ["file", 14.12], ["commands", 14.42], ["like", 14.82], ["move", 15.06], ["and", 15.36], ["remove", 15.56], ["inside", 15.92], ["the", 16.48], ["project,", 16.66], ["other", 17.34], ["commands", 17.52], ["still", 17.88], ["need", 18.2], ["permission.", 18.44]], "B60": [["Pattern", 0.0], ["B", 0.26], ["needs", 0.52], ["a", 0.78], ["lock,", 0.98], ["the", 1.44], ["laptop", 1.54], ["reaches", 1.84], ["the", 2.26], ["node", 2.52], ["through", 2.72], ["the", 2.96], ["login", 3.1], ["node", 3.34], ["so", 3.72], ["something", 4.06], ["has", 4.34], ["to", 4.58], ["listen", 4.74], ["on", 4.96], ["the", 5.18], ["node's", 5.3], ["cluster", 5.62], ["network.", 5.9], ["Olama", 6.9], ["stays", 7.28], ["on", 7.48], ["localhost,", 7.74], ["a", 8.68], ["small", 8.78], ["web", 9.04], ["server", 9.26], ["caddy", 9.64], ["listens", 10.0], ["instead", 10.46], ["and", 11.06], ["rejects", 11.44], ["every", 11.7], ["request", 12.1], ["that", 12.52], ["does", 12.76], ["not", 12.88], ["carry", 13.12], ["your", 13.38], ["bearer", 13.6], ["token.", 13.78]], "B61": [["Here", 0.0], ["is", 0.2], ["the", 0.36], ["proxy's", 0.5], ["whole", 0.96], ["rulebook,", 1.16], ["requests", 2.14], ["with", 2.2], ["the", 2.5], ["right", 2.64], ["header", 2.84], ["go", 3.14], ["through", 3.34], ["to", 3.6], ["Olama,", 3.82], ["everything", 4.7], ["else", 5.02], ["gets", 5.3], ["a", 5.52], ["401,", 5.72], ["and", 6.62], ["the", 6.72], ["admin", 6.82], ["interface", 7.12], ["is", 7.54], ["switched", 7.8], ["off", 8.02], ["because", 8.34], ["it", 8.64], ["would", 8.76], ["open", 8.88], ["yet", 9.16], ["another", 9.38], ["port", 9.76], ["with", 10.02], ["no", 10.26], ["lock.", 10.46]], "B62": [["On", 0.0], ["your", 0.12], ["laptop,", 0.24], ["a", 0.82], ["small", 0.88], ["script", 1.12], ["reads", 1.48], ["which", 1.82], ["node", 2.12], ["your", 2.32], ["job", 2.5], ["landed", 2.78], ["on,", 3.12], ["checks", 3.6], ["that", 3.8], ["the", 4.08], ["job", 4.2], ["is", 4.44], ["still", 4.6], ["running,", 4.8], ["writes", 5.5], ["a", 5.66], ["private", 5.84], ["environment", 6.14], ["file,", 6.66], ["and", 7.36], ["opens", 7.44], ["the", 7.76], ["tunnel.", 8.0], ["The", 9.0], ["local", 9.12], ["port", 9.36], ["is", 9.68], ["11", 9.88], ["-4", 10.22], ["-3", 10.5], ["-5,", 10.78], ["so", 11.36], ["it", 11.56], ["does", 11.66], ["not", 11.76], ["collide", 12.0], ["with", 12.34], ["an", 12.58], ["Olama", 12.7], ["on", 13.14], ["your", 13.26], ["laptop.", 13.38]], "B63": [["Check", 0.0], ["the", 0.22], ["lock,", 0.42], ["the", 0.84], ["first", 0.92], ["command", 1.12], ["should", 1.42], ["print", 1.68], ["401", 1.92], ["because", 2.42], ["it", 2.92], ["carries", 3.06], ["no", 3.34], ["token.", 3.64], ["The", 4.56], ["second", 4.66], ["sends", 4.9], ["your", 5.28], ["token", 5.5], ["and", 5.86], ["should", 6.12], ["return", 6.28], ["a", 6.56], ["short", 6.74], ["message.", 6.94], ["Then", 7.86], ["start", 7.98], ["Claude", 8.3], ["code", 8.58], ["from", 8.88], ["your", 9.14], ["project", 9.28], ["in", 9.7], ["that", 9.92], ["same", 10.1], ["terminal.", 10.36]], "B64": [["Two", 0.0], ["risks", 0.18], ["remain,", 0.42], ["the", 1.04], ["proxy", 1.14], ["blocks", 1.44], ["the", 1.78], ["rest", 2.0], ["of", 2.16], ["the", 2.34], ["cluster,", 2.42], ["but", 2.96], ["Olama's", 3.06], ["own", 3.54], ["random", 3.76], ["port", 4.12], ["is", 4.42], ["still", 4.64], ["reachable", 4.8], ["by", 5.28], ["other", 5.5], ["users", 5.7], ["on", 5.98], ["the", 6.24], ["same", 6.38], ["node.", 6.6], ["A", 7.46], ["random", 7.62], ["port", 7.9], ["is", 8.18], ["obscurity,", 8.36], ["not", 9.1], ["security,", 9.2], ["and", 10.16], ["your", 10.26], ["token", 10.38], ["sits", 10.62], ["in", 10.88], ["plain", 11.1], ["text", 11.32], ["on", 11.64], ["your", 11.84], ["laptop.", 11.96], ["When", 12.7], ["you", 12.78], ["finish,", 12.92], ["cancel", 13.5], ["the", 13.64], ["job.", 13.94]], "B70": [["Ater", 0.0], ["on", 0.24], ["the", 0.4], ["node,", 0.52], ["use", 0.94], ["the", 1.06], ["Olama", 1.26], ["underscore", 1.72], ["chat", 2.14], ["prefix.", 2.52], ["From", 3.44], ["the", 3.5], ["laptop", 3.64], ["through", 4.0], ["the", 4.32], ["proxy,", 4.48], ["use", 5.12], ["its", 5.26], ["open", 5.42], ["AI", 5.76], ["compatible", 6.08], ["mode", 6.5], ["because", 7.04], ["its", 7.4], ["Olama", 7.56], ["provider", 8.06], ["does", 8.32], ["not", 8.62], ["send", 8.84], ["a", 9.12], ["bearer", 9.26], ["token.", 9.42], ["A", 10.5], ["warning", 10.6], ["about", 10.8], ["an", 11.1], ["unknown", 11.26], ["context", 11.64], ["window", 12.18], ["is", 12.64], ["harmless.", 12.88], ["The", 13.68], ["server", 13.78], ["enforces", 14.08], ["it.", 14.62]], "B71": [["Continue", 0.0], ["in", 0.42], ["VS", 0.7], ["Code", 1.0], ["or", 1.38], ["JetBrains", 1.62], ["takes", 2.32], ["the", 2.56], ["same", 2.82], ["endpoint", 3.02], ["in", 3.42], ["a", 3.72], ["YAML", 3.82], ["file.", 4.1], ["Paste", 5.0], ["your", 5.08], ["token", 5.3], ["where", 5.52], ["it", 5.82], ["says", 5.94], ["so.", 6.14], ["The", 6.76], ["roles", 6.82], ["are", 7.06], ["Chat,", 7.3], ["Edit,", 7.94], ["and", 8.32], ["Apply.", 8.38]], "B72": [["Codex", 0.0], ["OpenCode", 0.32], ["and", 1.0], ["Droid", 1.22], ["can", 1.44], ["be", 1.7], ["set", 1.84], ["up", 2.02], ["by", 2.22], ["the", 2.42], ["Olama", 2.56], ["launch", 2.88], ["command,", 3.16], ["but", 3.82], ["only", 4.02], ["when", 4.22], ["Olama", 4.42], ["is", 4.82], ["on", 5.06], ["the", 5.2], ["same", 5.36], ["machine", 5.58], ["at", 5.94], ["its", 6.18], ["default", 6.32], ["port.", 6.64], ["Here", 7.58], ["the", 7.7], ["port", 7.84], ["is", 8.04], ["random", 8.22], ["and", 8.56], ["behind", 8.98], ["a", 9.2], ["token", 9.38], ["in", 9.66], ["Pattern", 9.96], ["B,", 10.2], ["so", 10.84], ["set", 11.06], ["them", 11.28], ["up", 11.4], ["as", 11.54], ["OpenAI", 11.74], ["-compatible", 12.38], ["providers", 12.86], ["and", 13.38], ["follow", 13.92], ["each", 14.18], ["tool's", 14.52], ["current", 14.94], ["instructions.", 15.18]], "B80": [["Four", 0.0], ["failures", 0.18], ["cover", 0.52], ["most", 0.82], ["trouble.", 1.1], ["A", 1.66], ["404", 1.82], ["on", 2.18], ["every", 2.54], ["request,", 2.8], ["the", 3.46], ["base", 3.52], ["address", 3.72], ["ends", 4.02], ["in", 4.34], ["slash", 4.56], ["V1,", 4.84], ["a", 5.78], ["Claude", 5.88], ["model", 6.08], ["name", 6.38], ["not", 6.62], ["found,", 6.86], ["the", 7.36], ["aliases", 7.44], ["are", 7.74], ["not", 7.96], ["mapped,", 8.16], ["tool", 8.82], ["calls", 8.94], ["printed", 9.26], ["as", 9.58], ["raw", 9.82], ["text,", 10.04], ["the", 10.58], ["model", 10.66], ["has", 10.9], ["no", 11.1], ["tools", 11.34], ["label,", 11.62], ["and", 12.4], ["a", 12.48], ["split", 12.56], ["between", 12.8], ["processor", 13.12], ["and", 13.52], ["GPU,", 13.9], ["the", 14.6], ["model", 14.7], ["or", 14.98], ["the", 15.2], ["window", 15.32], ["is", 15.52], ["too", 15.82], ["big.", 16.04]], "B81": [["Three", 0.0], ["more,", 0.2], ["a", 0.64], ["full", 0.7], ["home", 0.86], ["folder,", 1.1], ["the", 1.64], ["image", 1.76], ["cache", 2.02], ["or", 2.3], ["the", 2.56], ["models", 2.66], ["defaulted", 3.0], ["to", 3.58], ["home.", 3.7], ["A", 4.3], ["pull", 4.46], ["that", 4.62], ["fails", 4.78], ["on", 5.02], ["a", 5.24], ["compute", 5.34], ["node,", 5.58], ["no", 6.06], ["outbound", 6.2], ["network.", 6.66], ["On", 7.4], ["Explorer,", 7.54], ["a", 8.22], ["default", 8.3], ["module", 8.58], ["sets", 9.04], ["the", 9.32], ["proxy", 9.56], ["that", 9.88], ["nodes", 10.12], ["use.", 10.38], ["If", 11.14], ["a", 11.24], ["script", 11.34], ["begins", 11.6], ["with", 11.96], ["module", 12.22], ["purge,", 12.58], ["it", 13.04], ["loses", 13.12], ["that", 13.34], ["proxy,", 13.66], ["so", 14.32], ["load", 14.52], ["the", 14.74], ["module", 14.9], ["again", 15.26], ["right", 15.54], ["after.", 15.78]], "B82": [["And", 0.0], ["one", 0.14], ["more", 0.32], ["trap,", 0.54], ["those", 1.16], ["same", 1.26], ["proxy", 1.56], ["settings", 1.94], ["can", 2.3], ["get", 2.54], ["in", 2.68], ["the", 2.78], ["way", 2.88], ["when", 3.04], ["you", 3.2], ["talk", 3.34], ["to", 3.52], ["your", 3.72], ["own", 3.82], ["local", 4.0], ["server.", 4.32], ["Research", 5.64], ["computing's", 5.9], ["own", 6.48], ["post", 6.66], ["on", 6.98], ["running", 7.22], ["Olama", 7.48], ["tells", 8.14], ["you", 8.38], ["to", 8.62], ["unset", 8.74], ["the", 9.12], ["proxy", 9.3], ["variables", 9.64], ["before", 10.1], ["you", 10.44], ["do.", 10.66]], "B90": [["Explorer", 0.0], ["runs", 0.4], ["a", 0.66], ["watcher", 0.84], ["for", 1.18], ["idle", 1.38], ["GPUs.", 1.66], ["Under", 2.7], ["use", 2.76], ["for", 2.9], ["50", 3.1], ["minutes", 3.38], ["earns", 3.66], ["an", 3.88], ["email.", 4.08], ["Under", 4.64], ["use", 4.82], ["for", 4.96], ["an", 5.14], ["hour", 5.24], ["gets", 5.4], ["the", 5.62], ["job", 5.84], ["cancelled.", 6.12], ["Coding", 7.1], ["is", 7.24], ["bursty", 7.44], ["with", 7.88], ["long", 8.04], ["gaps", 8.28], ["while", 8.6], ["you", 8.82], ["read,", 8.96], ["so", 9.32], ["a", 9.42], ["session", 9.54], ["you", 9.76], ["walk", 9.96], ["away", 10.14], ["from", 10.4], ["will", 10.58], ["be", 10.7], ["flagged.", 10.84], ["Never", 11.6], ["add", 11.76], ["filler", 12.0], ["work", 12.22], ["to", 12.48], ["keep", 12.68], ["it", 12.8], ["alive.", 12.94], ["Start", 13.64], ["when", 13.82], ["you", 13.98], ["sit", 14.1], ["down,", 14.24], ["cancel", 14.76], ["when", 14.9], ["you", 15.14], ["stop,", 15.24], ["and", 15.76], ["put", 15.84], ["long", 15.96], ["unattended", 16.26], ["work", 16.82], ["in", 17.1], ["batch", 17.28], ["jobs.", 17.46]], "B91": [["Now", 0.0], ["the", 0.2], ["shared", 0.4], ["endpoint", 0.62], ["for", 1.04], ["a", 1.34], ["whole", 1.48], ["class.", 1.66], ["A", 2.66], ["slurm", 2.7], ["job", 3.06], ["has", 3.26], ["a", 3.44], ["time", 3.58], ["limit,", 3.76], ["eight", 4.3], ["hours", 4.4], ["on", 4.7], ["the", 4.9], ["GPU", 5.04], ["partition,", 5.38], ["so", 6.16], ["an", 6.34], ["endpoint", 6.44], ["built", 6.82], ["on", 7.04], ["one", 7.22], ["dies", 7.4], ["on", 7.66], ["a", 7.86], ["schedule", 7.98], ["and", 8.22], ["returns", 8.5], ["on", 8.84], ["a", 9.02], ["different", 9.14], ["node.", 9.36], ["Between", 10.06], ["requests,", 10.26], ["the", 10.98], ["GPU", 11.02], ["idles,", 11.46], ["and", 12.22], ["Olama", 12.32], ["serves", 12.8], ["one", 13.0], ["person", 13.34], ["well.", 13.66], ["Five", 14.4], ["students", 14.54], ["at", 14.88], ["64", 15.08], [",000", 15.54], ["context", 16.12], ["cost", 16.52], ["roughly", 16.88], ["five", 17.26], ["times", 17.6], ["the", 17.98], ["cache", 18.14], ["memory.", 18.36]], "B92": [["A", 0.0], ["service", 0.14], ["for", 0.36], ["many", 0.58], ["people", 0.76], ["would", 1.1], ["usually", 1.28], ["use", 1.58], ["VLLM,", 1.84], ["which", 2.84], ["batches", 2.98], ["concurrent", 3.32], ["requests", 3.76], ["and", 4.16], ["supports", 4.42], ["API", 4.82], ["keys,", 5.32], ["though", 6.04], ["its", 6.14], ["own", 6.24], ["documentation", 6.42], ["says", 6.96], ["not", 7.4], ["to", 7.66], ["rely", 7.84], ["on", 8.1], ["a", 8.26], ["key", 8.36], ["alone,", 8.5], ["and", 9.3], ["other", 9.42], ["people's", 9.58], ["code", 10.04], ["and", 10.24], ["prompts", 10.4], ["would", 10.7], ["then", 10.86], ["pass", 11.02], ["through", 11.26], ["a", 11.5], ["service", 11.66], ["you", 11.94], ["run.", 12.16], ["That", 12.76], ["raises", 12.92], ["questions", 13.18], ["about", 13.66], ["logging,", 14.04], ["retention,", 14.7], ["and", 15.36], ["who", 15.46], ["is", 15.62], ["responsible", 15.74], ["when", 16.18], ["it", 16.52], ["breaks.", 16.62], ["Those", 17.28], ["are", 17.42], ["questions", 17.58], ["for", 17.92], ["research", 18.24], ["computing,", 18.58], ["not", 19.28], ["settings.", 19.42]], "B93": [["So", 0.0], ["ask", 0.18], ["five", 0.52], ["questions.", 0.86], ["Is", 1.8], ["one", 1.84], ["person's", 2.08], ["interactive", 2.52], ["session", 2.92], ["in", 3.42], ["a", 3.6], ["GPU", 3.74], ["job", 4.02], ["acceptable?", 4.5], ["Is", 5.58], ["SSH", 5.7], ["port", 6.08], ["forwarding", 6.54], ["from", 6.96], ["a", 7.2], ["login", 7.34], ["node", 7.52], ["permitted?", 7.84], ["May", 8.62], ["a", 8.7], ["process", 8.8], ["listen", 9.08], ["on", 9.42], ["the", 9.62], ["node's", 9.74], ["network", 10.04], ["behind", 10.36], ["a", 10.7], ["token", 10.86], ["proxy?", 11.1], ["What", 12.04], ["is", 12.14], ["the", 12.26], ["preferred", 12.4], ["route", 12.7], ["for", 13.02], ["a", 13.24], ["cohort", 13.34], ["and", 13.72], ["where", 14.08], ["should", 14.22], ["model", 14.36], ["waits", 14.68], ["live?", 15.02]], "B94": [["On", 0.0], ["AICR,", 0.14], ["the", 1.08], ["newer", 1.1], ["AI", 1.32], ["Compute", 1.72], ["Resource", 2.1], ["Cluster,", 2.4], ["there", 3.24], ["are", 3.34], ["248", 3.44], ["B200", 4.2], ["and", 5.12], ["152", 5.44], ["RTX", 6.04], ["Pro", 6.68], ["GPUs,", 7.08], ["and", 8.02], ["access", 8.12], ["is", 8.48], ["by", 8.72], ["proposal.", 8.9], ["Research", 10.1], ["computing", 10.36], ["says", 10.76], ["to", 11.1], ["develop", 11.28], ["and", 11.56], ["test", 11.8], ["on", 12.04], ["Explorer", 12.24], ["first.", 12.6], ["Whether", 13.44], ["AICR's", 13.58], ["idle", 14.46], ["rules", 14.68], ["treat", 15.06], ["a", 15.3], ["standing", 15.44], ["service", 15.7], ["differently", 16.12], ["is", 16.58], ["a", 16.96], ["question", 17.1], ["only", 17.4], ["research", 17.74], ["computing", 18.16], ["can", 18.6], ["answer.", 18.86]], "B95": [["Here", 0.0], ["is", 0.18], ["what", 0.32], ["we", 0.48], ["have", 0.62], ["and", 0.8], ["have", 0.94], ["not", 1.06], ["checked.", 1.28], ["We", 1.88], ["have", 1.9], ["not", 1.98], ["run", 2.14], ["this", 2.32], ["whole", 2.48], ["setup", 2.72], ["from", 2.98], ["start", 3.22], ["to", 3.48], ["finish.", 3.7], ["We", 4.52], ["did", 4.62], ["check", 4.78], ["with", 5.12], ["read", 5.34], ["-only", 5.54], ["commands", 5.76], ["on", 6.14], ["Explorer", 6.36], ["the", 6.76], ["partitions", 6.98], ["that", 7.42], ["an", 7.78], ["H200", 7.9], ["type", 8.44], ["exists,", 8.78], ["that", 9.38], ["Aptainer", 9.52], ["is", 9.88], ["on", 10.1], ["the", 10.24], ["login", 10.38], ["node,", 10.58], ["that", 11.12], ["the", 11.28], ["proxy", 11.38], ["comes", 11.64], ["from", 11.94], ["a", 12.18], ["default", 12.28], ["module,", 12.56], ["and", 13.28], ["that", 13.44], ["one", 13.58], ["account's", 13.72], ["scratch", 14.1], ["folder", 14.34], ["was", 14.76], ["not", 14.98], ["writable.", 15.22], ["Research", 16.24], ["computing", 16.48], ["has", 16.86], ["a", 17.14], ["post", 17.28], ["on", 17.46], ["running", 17.66], ["Olama", 17.92], ["in", 18.46], ["a", 18.56], ["container.", 18.7], ["But", 19.7], ["no", 19.84], ["page", 20.04], ["we", 20.36], ["read", 20.58], ["covers", 20.84], ["coding", 21.24], ["agents", 21.6], ["or", 22.1], ["says", 22.48], ["whether", 22.76], ["automated", 23.06], ["agents", 23.56], ["are", 24.06], ["allowed.", 24.28]], "B100": [["Expect", 0.0], ["a", 0.34], ["weaker", 0.52], ["agent.", 0.7], ["Models", 1.62], ["in", 1.62], ["this", 1.84], ["range", 1.96], ["are", 2.24], ["capable,", 2.4], ["but", 2.94], ["Claude", 3.08], ["Code's", 3.28], ["loop", 3.7], ["is", 3.88], ["demanding.", 4.06], ["A", 4.9], ["long", 5.02], ["system", 5.22], ["prompt,", 5.56], ["dozens", 6.18], ["of", 6.36], ["tool", 6.6], ["definitions,", 6.82], ["and", 7.56], ["a", 7.64], ["growing", 7.76], ["history", 8.0], ["on", 8.4], ["every", 8.6], ["turn.", 8.88], ["Expect", 10.02], ["more", 10.3], ["malformed", 10.58], ["tool", 11.04], ["calls,", 11.32], ["more", 11.88], ["loops,", 12.02], ["and", 12.48], ["an", 12.6], ["earlier", 12.7], ["loss", 12.94], ["of", 13.24], ["the", 13.4], ["thread", 13.54], ["on", 13.76], ["big", 13.94], ["changes", 14.12], ["across", 14.64], ["many", 14.98], ["files.", 15.26]], "B101": [["Where", 0.0], ["it", 0.12], ["does", 0.22], ["well,", 0.34], ["clear", 0.78], ["tasks", 0.88], ["with", 1.26], ["clear", 1.5], ["tests,", 1.74], ["bulk", 2.38], ["work", 2.48], ["over", 2.74], ["many", 2.92], ["files", 3.1], ["and", 3.48], ["batch", 3.66], ["jobs,", 3.86], ["code", 4.64], ["that", 4.86], ["should", 5.06], ["not", 5.2], ["leave", 5.36], ["Northeastern", 5.58], ["and", 6.14], ["teaching", 6.5], ["how", 6.76], ["a", 7.02], ["smaller", 7.12], ["model", 7.42], ["differs", 7.74], ["from", 8.0], ["a", 8.34], ["frontier", 8.44], ["one.", 8.76], ["Where", 9.8], ["it", 10.02], ["does", 10.12], ["poorly,", 10.28], ["open", 11.02], ["-ended", 11.22], ["refactors,", 11.48], ["long", 12.52], ["debugging", 12.62], ["across", 13.06], ["a", 13.42], ["large", 13.64], ["code", 13.92], ["base,", 14.2], ["and", 14.78], ["anything", 14.86], ["where", 15.1], ["one", 15.36], ["wrong", 15.58], ["tool", 15.82], ["call", 16.08], ["is", 16.38], ["expensive.", 16.58]], "B102": [["A", 0.0], ["practical", 0.16], ["split,", 0.5], ["the", 1.1], ["local", 1.16], ["model", 1.36], ["for", 1.7], ["drafting", 1.96], ["boilerplate", 2.42], ["tests", 3.1], ["and", 3.46], ["batch", 3.76], ["passes", 4.0], ["and", 4.44], ["frontier", 4.72], ["credits", 5.08], ["for", 5.46], ["the", 5.72], ["hard", 5.82], ["problems.", 6.04], ["Measured", 7.26], ["that", 7.46], ["way,", 7.66], ["the", 8.04], ["savings", 8.12], ["are", 8.44], ["real.", 8.74], ["Measured", 9.5], ["as", 9.78], ["the", 9.96], ["same", 10.16], ["thing", 10.38], ["for", 10.58], ["free,", 10.82], ["they", 11.34], ["are", 11.46], ["not.", 11.54]], "BVDT": [["Let's", 0.0], ["recap", 0.7], ["with", 0.94], ["Claude.", 1.2], ["A", 1.8], ["local", 1.88], ["model", 2.08], ["runs", 2.38], ["inside", 2.64], ["a", 3.02], ["GPU", 3.2], ["job", 3.48], ["you", 3.88], ["ask", 4.08], ["for", 4.28], ["with", 4.52], ["no", 4.66], ["per", 4.88], ["-token", 5.08], ["billing.", 5.3], ["Pattern", 6.52], ["A", 6.52], ["keeps", 6.64], ["the", 6.82], ["model", 7.04], ["and", 7.28], ["the", 7.46], ["agent", 7.58], ["on", 7.8], ["one", 7.96], ["node.", 8.16], ["Pattern", 8.8], ["B", 8.88], ["adds", 9.1], ["a", 9.36], ["tunnel", 9.52], ["and", 9.68], ["a", 9.88], ["token", 10.04], ["lock.", 10.24], ["Buying", 10.98], ["to", 11.04], ["local", 11.18], ["host,", 11.4], ["use", 11.94], ["the", 12.04], ["bare", 12.24], ["base", 12.4], ["address,", 12.64], ["map", 13.18], ["every", 13.36], ["alias,", 13.72], ["and", 14.24], ["set", 14.34], ["the", 14.52], ["context", 14.68], ["window", 15.04], ["high.", 15.38], ["Pick", 16.14], ["a", 16.24], ["tool", 16.38], ["-capable", 16.58], ["model", 17.0], ["that", 17.32], ["fits", 17.58], ["video", 17.78], ["memory", 18.1], ["with", 18.38], ["room", 18.68], ["for", 18.88], ["the", 19.1], ["context.", 19.2], ["Idle", 20.34], ["GPUs", 20.34], ["are", 20.72], ["canceled.", 21.04], ["So", 22.0], ["start", 22.22], ["when", 22.46], ["you", 22.62], ["sit", 22.76], ["down", 22.92], ["and", 23.2], ["cancel", 23.44], ["when", 23.74], ["you", 23.94], ["stop,", 24.1], ["and", 24.56], ["a", 24.98], ["shared", 25.1], ["-in", 25.3], ["point", 25.48], ["for", 25.76], ["a", 25.96], ["class", 26.08], ["is", 26.34], ["a", 26.58], ["question", 26.72], ["for", 26.94], ["research", 27.28], ["computing,", 27.64], ["not", 28.54], ["a", 28.64], ["setting.", 28.76]], "BHTF": [["Your", 0.0], ["turn,", 0.14], ["paste", 0.56], ["this", 0.72], ["into", 0.94], ["Claude.", 1.18], ["I", 1.62], ["want", 1.66], ["to", 1.8], ["run", 1.92], ["a", 2.04], ["local", 2.16], ["model", 2.38], ["on", 2.74], ["Explorer", 2.94], ["for", 3.28], ["coding.", 3.56], ["Walk", 4.24], ["me", 4.38], ["through", 4.52], ["choosing", 4.72], ["between", 5.02], ["pattern", 5.36], ["and", 5.66], ["pattern", 5.94], ["B.", 6.3], ["List", 6.98], ["which", 7.12], ["commands", 7.34], ["run", 7.64], ["on", 7.92], ["my", 8.08], ["computer", 8.24], ["and", 8.56], ["which", 8.76], ["on", 8.9], ["the", 9.04], ["cluster", 9.16], ["which", 9.5], ["ones", 9.7], ["would", 9.92], ["submit", 10.06], ["a", 10.36], ["job", 10.5], ["and", 10.76], ["the", 10.96], ["five", 11.06], ["questions", 11.3], ["I", 11.74], ["should", 11.98], ["ask", 12.1], ["research", 12.36], ["computing", 12.7], ["first.", 13.18], ["Do", 13.86], ["not", 13.94], ["run", 14.08], ["anything", 14.26], ["on", 14.58], ["any", 14.74], ["cluster.", 14.9], ["Then", 15.5], ["check", 15.68], ["two", 15.92], ["things", 16.12], ["yourself.", 16.4], ["Did", 17.1], ["Claude", 17.2], ["run", 17.4], ["nothing", 17.6], ["on", 17.88], ["a", 18.08], ["cluster", 18.18], ["and", 18.5], ["did", 18.9], ["it", 19.0], ["say", 19.1], ["what", 19.28], ["it", 19.44], ["could", 19.52], ["not", 19.64], ["confirm?", 19.82]], "BOUT": [["Running", 0.0], ["a", 0.28], ["local", 0.48], ["LLM", 0.74], ["on", 1.42], ["Explorer", 1.62], ["at", 2.08], ["Nick", 2.58], ["Baer", 2.84], ["Brown.", 3.14]], "B110": [["To", 0.0], ["try", 0.12], ["it,", 0.38], ["go", 0.66], ["to", 0.76], ["the", 0.92], ["HPC", 1.02], ["-AICR", 1.54], ["repository", 2.74], ["on", 3.16], ["GitHub.", 3.7], ["In", 4.76], ["the", 4.86], ["Skills", 5.02], ["folder", 5.26], ["under", 5.72], ["Local", 6.04], ["LLM", 6.38], ["on", 7.0], ["Explorer,", 7.14], ["there", 7.94], ["is", 8.04], ["a", 8.16], ["Get", 8.26], ["Started", 8.38], ["recipe.", 8.78], ["The", 9.74], ["link", 9.76], ["is", 9.92], ["in", 10.16], ["the", 10.3], ["description.", 10.42]], "B111": [["Clone", 0.0], ["it,", 0.22], ["start", 0.52], ["Claude", 0.7], ["Code", 0.92], ["inside", 1.2], ["it", 1.58], ["and", 1.82], ["paste", 1.98], ["the", 2.2], ["prompt", 2.4], ["at", 2.62], ["the", 2.8], ["top", 2.9], ["of", 3.1], ["that", 3.26], ["file.", 3.42], ["Claude", 4.5], ["Code", 4.6], ["then", 4.86], ["guides", 5.06], ["you", 5.32], ["step", 5.58], ["by", 5.78], ["step", 6.0], ["and", 6.36], ["asks", 6.68], ["before", 6.92], ["every", 7.28], ["file", 7.6], ["it", 7.88], ["writes", 8.04], ["and", 8.28], ["every", 8.52], ["job", 8.82], ["it", 9.1], ["submits.", 9.32], ["It", 10.22], ["has", 10.3], ["not", 10.4], ["been", 10.6], ["run", 10.78], ["end", 10.98], ["to", 11.14], ["end", 11.32], ["yet,", 11.52], ["so", 11.94], ["expect", 12.04], ["to", 12.38], ["help", 12.6], ["it", 12.72], ["fix", 12.88], ["something.", 13.08]]}


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


# ═════════════════════════════ PART A — B10 B11 B12 B13 B20 B22 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.
def pA_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pA_stopwatch(x, y, r=0.55):
    face = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    knob = Rectangle(width=0.26, height=0.16, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + r + 0.12, 0])
    hand = Line([x, y, 0], [x, y + r * 0.7, 0], color=INK, stroke_width=7)
    hub = Dot([x, y, 0], radius=0.07, color=INK)
    g = VGroup(knob, face, hand, hub)
    g.hand, g.cx, g.cy = hand, x, y
    return g


def pA_folder(x, y, w=1.7, h=1.1):
    """A flat kraft folder: tab, back, front (centre x, y)."""
    back = Rectangle(width=w, height=h * 0.8, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y - 0.1 * h, 0])
    tab = Rectangle(width=w * 0.38, height=h * 0.24, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x - w * 0.31, y + 0.4 * h, 0])
    front = Rectangle(width=w, height=h * 0.55, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y - 0.225 * h, 0])
    return VGroup(tab, back, front)


def pA_laptop(x, y, w=2.3, h=1.5):
    """A plain laptop slab: a flat rounded rectangle with a smaller screen rectangle."""
    body = RoundedRectangle(corner_radius=0.14, width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    screen = Rectangle(width=w - 0.4, height=h - 0.4, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(body, screen)


def pA_pipe(x0, x1, y, h=0.42):
    return Rectangle(width=x1 - x0, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([(x0 + x1) / 2, y, 0])


def pA_arrow(a, b, w=8):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], color=INK, stroke_width=w, buff=0, max_tip_length_to_length_ratio=0.5)


def pA_slot(iso, x0, y0, z0, w, d, h):
    """A dashed ghost outline of an empty rack slot (three visible faces)."""
    x1, y1, z1 = x0 + w, y0 + d, z0 + h
    faces = [[(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],
             [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
             [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    out = VGroup()
    for f in faces:
        poly = Polygon(*[iso.p(*q) for q in f], color=BAR1, stroke_width=5)
        out.add(DashedVMobject(poly, num_dashes=24))
    return out


def pA_cloud(cx, cy, s=1.0, sw=6):
    """A dotted cloud outline (union of five circles, outline walked by angle)."""
    lobes = [(-0.75, -0.12, 0.42), (-0.28, 0.2, 0.52), (0.32, 0.22, 0.48), (0.78, -0.1, 0.42), (0.05, -0.2, 0.46)]
    pts = []
    for (lx, ly, r) in lobes:
        for k in range(120):
            a = 2 * np.pi * k / 120
            px, py = lx + r * np.cos(a), ly + r * np.sin(a)
            inside = any((px - ox) ** 2 + (py - oy) ** 2 < (orr - 1e-3) ** 2 for (ox, oy, orr) in lobes if (ox, oy, orr) != (lx, ly, r))
            if not inside:
                pts.append((px, py))
    c = np.mean(pts, axis=0)
    pts.sort(key=lambda q: np.arctan2(q[1] - c[1], q[0] - c[0]))
    pts.append(pts[0])
    m = VMobject(stroke_color=BAR1, stroke_width=sw)
    m.set_points_as_corners([[cx + q[0] * s, cy + q[1] * s, 0] for q in pts])
    return DashedVMobject(m, num_dashes=46)


def pA_piece(text, cx, cy, w, fill=PAGE_TOP, shadow=BOX_L, size=32):
    """A plaque piece of an address: a pill-edged card carrying real mono text (outline-free)."""
    sh = Rectangle(width=w, height=0.8, fill_color=shadow, fill_opacity=1, stroke_width=0).move_to([cx + 0.09, cy - 0.09, 0])
    card = Rectangle(width=w, height=0.8, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([cx, cy, 0])
    lab = M(text, size).move_to([cx, cy, 0])
    g = VGroup(sh, card, lab)
    g.card, g.label = card, lab
    return g


# ───────────────────────────────────────────────────────────────────────────────────────────────
class B10_TheIdea(Scene):
    """You ask for a GPU: the node appears; the model drops in; the agent sends requests and uses your files; no per-token bill; the job clock ticks."""
    def construct(self):
        title = pA_act_title("I · The Idea And Its Layers")
        iso = Iso(2.2, -2.5, 1.2)
        rack, lights = explorer_rack(iso)
        rack_g = VGroup(rack, lights)
        slot = pA_slot(iso, 0, 0, 0.92, 1.3, 1.3, 0.42)
        slab = iso.box(0, 0, 0.92, 1.3, 1.3, 0.42)
        glab = T("GPU node", 36).move_to([2.2, -2.98, 0])
        mlab = T("model", 36).move_to([4.4, -0.4, 0])
        claude = logo_chip("claude", -4.3, -0.4)
        a1 = pA_arrow([-3.25, -0.2], [0.65, -0.2])
        a2 = pA_arrow([0.65, -0.58], [-3.25, -0.58])
        rl = T("requests", 34).move_to([-1.3, 0.2, 0])
        pl = T("replies", 34).move_to([-1.3, -0.98, 0])
        folder = pA_folder(-4.3, -2.5, 1.7, 1.1)
        tool = pA_arrow([-4.3, -1.2], [-4.3, -1.9])
        tlab = T("tools", 34).move_to([-3.5, -1.55, 0])
        flab = T("your files", 34).move_to([-2.25, -2.5, 0])
        tag = chip("per token", -1.8, 1.7, size=34)
        xm = x_mark(-0.3, 1.7, r=0.3, w=9)
        clock = pA_stopwatch(2.2, 1.6)
        jlab = T("job", 36).move_to([3.2, 1.6, 0])

        self.play(FadeIn(title), run_time=0.4)
        # "You ask Slurm for a GPU": the node appears, one slot waiting
        hear(self, "ask Slurm", lead=0.3)
        self.play(FadeIn(rack_g), FadeIn(glab), Create(slot), run_time=0.5)
        # "On that GPU you run an open model": the model block drops into the slot
        hear(self, "open model", lead=0.55)
        self.play(FadeIn(slab, shift=DOWN * 0.9), FadeOut(slot), run_time=0.5, rate_func=ease_in)
        self.play(lights[0].animate.set_color(TERRA), FadeIn(mlab), run_time=0.3)
        # "a coding agent like Claude Code": the Claude chip arrives
        hear(self, "like Claude", lead=0.35)
        self.play(FadeIn(claude), run_time=0.4)
        # "sends it requests": the request arrow lands before the clip midpoint
        hear(self, "sends it", lead=0.12)
        self.play(Create(a1), FadeIn(rl), run_time=0.35)
        # the reply comes back (just after the midpoint)
        hear(self, "requests and", lead=-0.35)
        self.play(Create(a2), FadeIn(pl), run_time=0.3)
        # "runs tools on your files": the folder, the tool arrow touching it
        hear(self, "runs tools", lead=0.15)
        self.play(FadeIn(folder), run_time=0.3)
        self.play(Create(tool), FadeIn(tlab), run_time=0.35)
        hear(self, "on your files", lead=0.2)
        self.play(FadeIn(flab), run_time=0.3)
        # "no per token bill": the price tag appears and is crossed out
        hear(self, "per token", lead=0.35)
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.3)
        hear(self, "bill", lead=0.15)
        self.play(Create(xm), run_time=0.3)
        # "the model is yours": the second light comes on
        hear(self, "yours", lead=0.2)
        self.play(lights[1].animate.set_color(TERRA), run_time=0.2)
        # "for as long as the job runs": the job clock ticks on the rack
        hear(self, "as long as", lead=0.3)
        self.play(FadeIn(clock), FadeIn(jlab), run_time=0.3)
        self.play(Rotate(clock.hand, angle=-2 * PI, about_point=[clock.cx, clock.cy, 0]), run_time=1.3, rate_func=linear)
        done(self)


class B11_ThreeLayers(Scene):
    """Three bands build bottom to top: model host (rack + Apptainer holding ollama), harness (Claude, aider, continue), transport (nothing, or an ssh tunnel)."""
    def construct(self):
        bx, bw = 1.375, 9.35
        ys = [-2.05, 0.0, 2.05]
        strips = [RoundedRectangle(corner_radius=0.2, width=bw, height=1.9, stroke_color=BAR2, stroke_width=4).move_to([bx, y, 0]) for y in ys]

        def side(s):
            t = T(s, 38)
            return t

        l1, l2, l3 = side("model host"), side("harness"), side("transport")
        for lab, y in ((l1, ys[0]), (l2, ys[1]), (l3, ys[2])):
            lab.move_to([-6.05 + lab.width / 2, y, 0])
        # band 1: GPU node rack + Apptainer container holding the ollama logo
        iso = Iso(-1.4, -2.9, 0.5)
        rk, lt = explorer_rack(iso)
        rack = VGroup(rk, lt)
        rlab = T("GPU node", 32).move_to([-1.4, -1.45, 0])
        cont = RoundedRectangle(corner_radius=0.18, width=3.4, height=1.1, fill_color=BOX_TOP, fill_opacity=1, stroke_color=KRAFT_DEEP, stroke_width=5).move_to([2.9, -2.3, 0])
        ollama = logo_chip("ollama", 2.9, -2.3, h=0.85)
        clab = T("Apptainer", 32).move_to([2.9, -1.45, 0])
        # band 2: the harness
        claude = logo_chip("claude", -0.6, 0.0, h=1.2)
        aider = chip("aider", 2.5, 0.0, mono=True, size=36)
        cont2 = logo_chip("continue", 5.0, 0.0, h=1.2)
        # band 3: the transport
        tline = DashedLine([-0.9, 1.6, 0], [5.3, 1.6, 0], color=BAR1, stroke_width=7, dash_length=0.25)
        nothing = chip("nothing", 2.2, 2.45, size=34)
        pipe = pA_pipe(-0.9, 5.3, 1.6, h=0.4)
        ssh = chip("ssh tunnel", 2.2, 2.45, mono=True, size=34)

        # "three layers": the three empty bands
        hear(self, "three layers", lead=0.3)
        self.play(*[FadeIn(s) for s in strips], run_time=0.5)
        # "The model host is Olama": label, then the ollama logo
        hear(self, "model host", lead=0.1)
        self.play(FadeIn(l1), run_time=0.3)
        hear(self, "is Olama", lead=0.2)
        self.play(FadeIn(ollama), run_time=0.3)
        # "inside an Apptainer container": the container wraps it
        hear(self, "inside an", lead=0.1)
        self.add(cont)
        cont.set_z_index(0); ollama.set_z_index(2)
        self.play(FadeIn(cont), FadeIn(clab), run_time=0.4)
        # "on a GPU node that Slurm gave you": the rack
        hear(self, "on a GPU", lead=0.25)
        self.play(FadeIn(rack), FadeIn(rlab), run_time=0.4)
        # "The harness is the coding agent": label (before the midpoint)
        hear(self, "The harness", lead=0.15)
        self.play(FadeIn(l2), run_time=0.3)
        # "Claude Code, Aider, or Continue": three harnesses, one by one
        hear(self, "Claude code", lead=0.0)
        self.play(FadeIn(claude), run_time=0.3)
        hear(self, "Claude code", lead=-0.55)        # Aider (heard as 'Ader') lands 0.55 s after 'Claude code'
        self.play(FadeIn(aider), run_time=0.3)
        hear(self, "or continue", lead=0.0)
        self.play(FadeIn(cont2), run_time=0.3)
        # "and the transport is whatever joins them"
        hear(self, "the transport", lead=0.15)
        self.play(FadeIn(l3), run_time=0.3)
        hear(self, "joins them", lead=0.3)
        self.play(Create(tline), run_time=0.5)
        # "nothing, if they share a machine"
        hear(self, "nothing if", lead=0.2)
        self.play(FadeIn(nothing), run_time=0.3)
        # "or an SSH tunnel": the line becomes a tunnel
        hear(self, "an SSH", lead=0.3)
        self.play(FadeOut(nothing), Create(pipe), run_time=0.35)
        self.play(FadeIn(ssh), run_time=0.3)
        done(self)


class B12_PatternA(Scene):
    """One GPU job holds the agent, the model and your repo; nothing crosses to the network; a check lands on the boundary."""
    def construct(self):
        bound = RoundedRectangle(corner_radius=0.35, width=7.8, height=4.7, stroke_color=INK, stroke_width=6).move_to([-2.0, -0.35, 0])
        blab = T("one GPU job", 38).move_to([-5.9 + 0.0, 2.55, 0])
        blab.move_to([-5.9 + blab.width / 2, 2.55, 0])
        claude = logo_chip("claude", -4.5, 0.55)
        ollama = logo_chip("ollama", -0.5, 0.55)
        arr = pA_arrow([-3.45, 0.55], [-1.5, 0.55])
        lh = M("localhost", 32).move_to([-0.5, -0.55, 0])
        folder = pA_folder(-4.6, -1.55, 1.7, 1.1)
        flab = T("your repo", 34).move_to([-2.65, -1.55, 0])
        cloud = pA_cloud(4.4, 0.55, 1.05)
        nlab = T("network", 34).move_to([4.4, -0.55, 0])
        netline = DashedLine([1.95, 0.55, 0], [3.2, 0.55, 0], color=BAR1, stroke_width=6, dash_length=0.2)
        xm = x_mark(2.58, 0.55, r=0.3, w=9)
        ring = Circle(radius=0.9, stroke_color=TERRA, stroke_width=7).move_to([-4.6, -1.55, 0])
        ck = check(1.9, 2.0, s=0.34, color=TERRA, w=13)

        # "keeps everything on the GPU node": the job boundary and its label
        hear(self, "everything", lead=0.4)
        self.play(Create(bound), FadeIn(blab), run_time=0.7)
        # "The agent": the Claude chip
        hear(self, "The agent", lead=0.2)
        self.play(FadeIn(claude), run_time=0.4)
        # "and the model": the arrow and the ollama logo
        hear(self, "the model", lead=0.15)
        self.play(Create(arr), FadeIn(ollama), run_time=0.4)
        # "in the same job": localhost
        hear(self, "same job", lead=0.3)
        self.play(FadeIn(lh), run_time=0.3)
        # "nothing crosses a network": the cloud, the line, the cross
        hear(self, "nothing crosses", lead=0.45)
        self.play(FadeIn(cloud), FadeIn(nlab), run_time=0.4)
        self.play(Create(netline), run_time=0.3)
        self.play(Create(xm), run_time=0.3)
        # "and your code": the repo folder (after the midpoint)
        hear(self, "your code", lead=0.2)
        self.play(FadeIn(folder), FadeIn(flab), run_time=0.4)
        # "stays on Northeastern storage": a ring pulse on the folder
        hear(self, "Northeastern", lead=0.2)
        self.add(ring)
        self.play(ring.animate.scale(1.5).set_stroke(opacity=0), run_time=0.8)
        self.remove(ring)
        # "Use it": the check lands on the boundary
        hear(self, "Use it", lead=0.2)
        self.play(Create(ck), run_time=0.4)
        done(self)


class B13_PatternB(Scene):
    """Laptop (you + Claude) -> ssh tunnel -> login node -> GPU node; a request packet travels and stops at the lock in front of the model."""
    def construct(self):
        yc = 0.4
        you = professor_bear("1x1", 1.7, seed="B13", x=-5.1, y=yc)
        ylab = T("you", 34).move_to([-5.1, yc - 1.15, 0])
        lap = pA_laptop(-2.95, yc, 2.1, 1.4)
        claude = logo_chip("claude", -2.95, yc, h=0.8)
        llab = T("laptop", 34).move_to([-2.95, yc - 1.15, 0])
        seg1 = pA_pipe(-1.75, 1.3, yc, h=0.42)
        seg2 = pA_pipe(1.3, 2.8, yc, h=0.42)
        tlab = M("ssh tunnel", 32).move_to([-0.6, yc + 0.85, 0])
        liso = Iso(1.3, yc - 0.93, 0.85)
        lrk, llt = explorer_rack(liso)
        login = VGroup(lrk, llt)
        lglab = T("login node", 34).move_to([1.3, yc - 1.4, 0])
        giso = Iso(4.85, yc - 1.2, 1.1)
        grk, glt = explorer_rack(giso)
        gpu = VGroup(grk, glt)
        gplab = T("GPU node", 34).move_to([4.85, yc - 1.75, 0])
        ollama = logo_chip("ollama", 4.85, yc - 0.1, h=1.0)
        lock = padlock(3.2, yc, s=0.7)
        pkt = Dot([-2.0, yc, 0], radius=0.15, color=TERRA)
        pkt2 = Dot([1.3, yc, 0], radius=0.15, color=TERRA)
        ring = Circle(radius=0.75, stroke_color=TERRA, stroke_width=7).move_to([4.85, yc - 0.1, 0])
        for m_, z in ((seg1, 0), (seg2, 0), (login, 2), (gpu, 2), (ollama, 3), (lock, 4), (pkt, 6), (pkt2, 6)):
            m_.set_z_index(z)

        # "Pattern B keeps your editor on your laptop": the laptop with Claude on its screen, then you
        hear(self, "keeps", lead=0.3)
        self.play(FadeIn(lap), FadeIn(claude), run_time=0.4)
        hear(self, "your editor", lead=0.3)
        self.play(FadeIn(you), FadeIn(ylab), run_time=0.4)
        hear(self, "your laptop", lead=0.25)
        self.play(FadeIn(llab), run_time=0.3)
        # "only the model's traffic": the packet leaves the laptop
        hear(self, "traffic", lead=0.2)
        self.play(FadeIn(pkt), run_time=0.3)
        # "through an SSH tunnel": the pipe grows, the packet rides it to the login node
        hear(self, "an SSH", lead=0.45)
        self.play(GrowFromEdge(seg1, LEFT), FadeIn(tlab), run_time=0.5)
        self.play(pkt.animate.move_to([1.3, yc, 0]), run_time=0.9, rate_func=smooth)
        # "to the login node": the small rack
        hear(self, "login node", lead=0.35)
        self.play(FadeIn(login), FadeIn(lglab), run_time=0.4)
        # "and on to the GPU node": the pipe continues, the big rack with the ollama logo
        hear(self, "on to", lead=0.04)
        self.play(GrowFromEdge(seg2, LEFT), FadeIn(gpu), FadeIn(gplab), FadeIn(ollama), run_time=0.5)
        # "so the model must be": a ring pulse on the model
        hear(self, "the model must", lead=0.15)
        self.add(ring)
        self.play(ring.animate.scale(1.5).set_stroke(opacity=0), run_time=0.7)
        self.remove(ring)
        # "reachable from the login node": the packet goes on from the login node to the model
        hear(self, "reachable", lead=0.1)
        self.play(pkt.animate.move_to([4.45, yc - 0.1, 0]), run_time=0.9, rate_func=smooth)
        self.play(FadeOut(pkt), run_time=0.2)
        # "that needs a lock in front of it": the padlock lands in front of the model
        hear(self, "needs a lock", lead=0.3)
        self.play(FadeIn(lock, shift=DOWN * 0.4), run_time=0.4)
        # a second packet runs up to the lock and stops there
        hear(self, "in front of it", lead=0.3)
        self.add(pkt2)
        self.play(pkt2.animate.move_to([2.8, yc, 0]), run_time=0.65, rate_func=smooth)
        self.play(pkt2.animate.shift(LEFT * 0.12), run_time=0.12)
        done(self)


class B20_OpenDoor(Scene):
    """A GPU node with its door open at 0.0.0.0: other users pull and delete a model; the door closes to 127.0.0.1 and they stop outside."""
    def construct(self):
        title = pA_act_title("II · Wrong Turns To Avoid")
        iso = Iso(3.4, -2.45, 1.5)
        rk, lt = explorer_rack(iso)
        rack = VGroup(rk, lt)

        def lface(ya, yb, za, zb):
            return [(0, ya, za), (0, yb, za), (0, yb, zb), (0, ya, zb)]

        recess = iso.quad(lface(0.1, 1.2, 0.08, 0.8), GHOST, sw=3)
        door_pts_closed = lface(0.1, 1.2, 0.08, 0.8)
        door_pts_open = [(0, 0.1, 0.08), (-1.1, 0.1, 0.08), (-1.1, 0.1, 0.8), (0, 0.1, 0.8)]
        door = iso.quad(door_pts_closed, BOX_L, sw=5)
        door_open = iso.quad(door_pts_open, BOX_L, sw=5)
        rc = iso.p(0, 0.85, 0.5)
        ollama = logo_chip("ollama", rc[0], rc[1], h=0.75)
        glab = T("GPU node", 36).move_to([5.0, 1.25, 0])
        recess.set_z_index(1); ollama.set_z_index(2); door.set_z_index(4)
        lab_open = chip("0.0.0.0", 5.0, -2.85, mono=True, size=34)
        lab_shut = chip("127.0.0.1", 5.0, -2.85, mono=True, size=34)
        # the four other users
        start = [(-5.5, -0.9), (-5.5, -1.5), (-5.5, -2.1), (-5.5, -2.7)]
        stop = [(1.45, -0.85), (1.0, -1.5), (0.4, -2.05), (-0.2, -2.6)]
        dots = [Dot([x, y, 0], radius=0.18, color=INK) for (x, y) in start]
        ulab = T("other users", 36).move_to([-4.0, -3.05, 0])
        blk = Iso(0.0, 0.0, 0.5).box(0, 0, 0, 0.9, 0.9, 0.7)
        plab = T("pull", 34)
        dlab = T("delete", 34)

        self.play(FadeIn(title), run_time=0.4)
        # "this setup": the node appears with its door shut
        hear(self, "this setup", lead=0.45)
        self.add(recess, ollama)
        self.play(FadeIn(rack), FadeIn(door), FadeIn(recess), FadeIn(ollama), FadeIn(glab), run_time=0.5)
        # "has no authentication": the door swings open
        hear(self, "has no", lead=0.25)
        self.play(Transform(door, door_open), run_time=0.6, rate_func=smooth)
        # "listens on every address": the 0.0.0.0 label
        hear(self, "listens on", lead=0.0)
        self.play(FadeIn(lab_open), run_time=0.3)
        # "on a shared cluster": four other users arrive
        hear(self, "on a shared", lead=0.3)
        self.play(*[FadeIn(d) for d in dots], FadeIn(ulab), run_time=0.4)
        # "opens the whole interface": they walk up to the open door
        hear(self, "opens the whole", lead=0.2)
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(dots, stop)], ulab.animate.move_to([-2.2, -3.05, 0]), run_time=0.9, rate_func=smooth)
        # "including pulling": the first one carries a model block in
        hear(self, "including", lead=0.3)
        blk.move_to([0.55, -0.7, 0]); plab.move_to([0.55, -0.15, 0])
        self.play(FadeIn(blk), FadeIn(plab), run_time=0.3)
        hear(self, "pulling", lead=0.3)
        self.play(blk.animate.move_to([2.2, -1.0, 0]).scale(0.5), dots[0].animate.move_to([1.9, -0.9, 0]), run_time=0.45, rate_func=smooth)
        self.play(FadeOut(blk), FadeOut(plab), dots[0].animate.move_to([1.45, -0.85, 0]), run_time=0.25)
        # "and deleting models": the second one reaches in and carries one away
        hear(self, "deleting", lead=0.3)
        dlab.move_to([0.3, -1.0, 0])
        blk2 = Iso(2.0, -1.3, 0.5).box(0, 0, 0, 0.9, 0.9, 0.7).scale(0.5)
        blk2.move_to([2.0, -1.4, 0])
        self.play(dots[1].animate.move_to([1.85, -1.5, 0]), FadeIn(blk2), run_time=0.35)
        self.play(dots[1].animate.move_to([0.0, -1.45, 0]), blk2.animate.move_to([-0.25, -1.65, 0]), FadeIn(dlab), run_time=0.7, rate_func=smooth)
        self.play(FadeOut(blk2), FadeOut(dlab), run_time=0.2)
        # "to anyone who can reach the node": the door swings closed to 127.0.0.1 and they stop outside
        hear(self, "who can reach", lead=0.25)
        self.play(Transform(door, iso.quad(door_pts_closed, BOX_L, sw=5)), FadeOut(lab_open), dots[1].animate.move_to([1.0, -1.5, 0]), run_time=0.6, rate_func=smooth)
        self.play(FadeIn(lab_shut), run_time=0.3)
        done(self)


class B22_BareBaseUrl(Scene):
    """Claude adds /v1/messages to a bare host and port (right); a base ending /v1 doubles it (404); the bare base gets the check."""
    def construct(self):
        yu, yl, ym = 1.7, -1.6, -0.1
        x0 = -4.0
        wb, ws = 5.22 + 0.5, 2.95 + 0.5
        wb2 = 5.95 + 0.5
        claude = logo_chip("claude", -5.2, ym, h=1.2)
        base = pA_piece("http://127.0.0.1:PORT", x0 + wb / 2, yu, wb)
        suf = pA_piece("/v1/messages", -2.3, ym, ws, fill=BOX_L, shadow=BOX_R)
        jx = x0 + wb + 0.04 + ws / 2                  # where the suffix joins the upper row
        brk = VGroup(Line([x0 + 0.1, 1.1, 0], [x0 + wb - 0.1, 1.1, 0], color=INK, stroke_width=6),
                     Line([x0 + 0.1, 1.1, 0], [x0 + 0.1, 1.3, 0], color=INK, stroke_width=6),
                     Line([x0 + wb - 0.1, 1.1, 0], [x0 + wb - 0.1, 1.3, 0], color=INK, stroke_width=6))
        bare = T("bare", 34).move_to([x0 + wb / 2, 0.68, 0])
        base2 = pA_piece("http://127.0.0.1:PORT/v1", x0 + wb2 / 2, yl, wb2)
        lab2 = base2.label
        ul = Line([lab2.get_right()[0] - 0.75, yl - 0.27, 0], [lab2.get_right()[0], yl - 0.27, 0], color=INK, stroke_width=8)
        suf2 = pA_piece("/v1/messages", -2.3, ym, ws, fill=BOX_L, shadow=BOX_R)
        jx2 = x0 + wb2 + 0.04 + ws / 2
        ring = Circle(radius=0.55, stroke_color=TERRA, stroke_width=8).move_to([x0 + wb2 + 0.02, yl, 0])
        tag = chip("404", x0 + wb2 + 0.02, -2.65, mono=True, size=38)
        ck = check(5.75, yu, s=0.3, color=TERRA, w=13)

        # "Second, the address": the bare base
        hear(self, "the address", lead=0.2)
        self.play(FadeIn(base), run_time=0.4)
        # "Claude Code adds slash v1 slash messages itself": the chip makes the suffix and slides it on
        hear(self, "Claude code", lead=0.35)
        self.play(FadeIn(claude), run_time=0.3)
        hear(self, "slash v1", lead=0.6)
        self.play(FadeIn(suf, shift=RIGHT * 0.3), run_time=0.25)
        self.play(suf.animate.move_to([jx, ym, 0]), run_time=0.45, rate_func=smooth)
        self.play(suf.animate.move_to([jx, yu, 0]), run_time=0.3, rate_func=smooth)
        # "a bare host and port": a bracket under the base
        hear(self, "a bare host", lead=0.35)
        self.play(Create(brk), FadeIn(bare), run_time=0.45)
        # "A base address": a second base, this one ending /v1 (after the clip midpoint)
        hear(self, "A base address", lead=0.1)
        self.play(FadeIn(base2), run_time=0.35)
        hear(self, "slash v1", lead=0.15, nth=1)
        self.play(Create(ul), run_time=0.3)
        # "doubles the path": the suffix slides in and collides
        hear(self, "doubles", lead=0.8)
        self.play(FadeIn(suf2, shift=RIGHT * 0.3), run_time=0.2)
        self.play(suf2.animate.move_to([jx2 + 0.6, ym, 0]), run_time=0.3, rate_func=smooth)
        self.play(suf2.animate.move_to([jx2 + 0.6, yl, 0]), run_time=0.25, rate_func=smooth)
        self.play(suf2.animate.move_to([jx2, yl, 0]), run_time=0.15, rate_func=ease_in)
        self.add(ring)
        self.play(ring.animate.scale(1.6).set_stroke(opacity=0), run_time=0.45)
        self.remove(ring)
        # "the request fails": the 404 tag lands
        hear(self, "request fails", lead=0.15)
        self.play(FadeIn(tag, shift=DOWN * 0.3), run_time=0.3)
        # "Give it the bare host and port": the check lands on the right one
        hear(self, "Give it", lead=0.25)
        self.play(Create(ck), run_time=0.4)
        done(self)


# ═════════════════════════════ PART B — B23 B24 B25 B26 B27 B31 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pB_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pB_laptop(x, y, s=1.0):
    """The laptop, front view: a rounded bezel with a smaller white screen on a thin base. Centred on (x, y)."""
    bezel = RoundedRectangle(corner_radius=0.12 * s, width=2.1 * s, height=1.4 * s, fill_color=BOX_L, fill_opacity=1,
                             stroke_color=INK, stroke_width=5).move_to([x, y + 0.1 * s, 0])
    screen = Rectangle(width=1.7 * s, height=1.0 * s, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR2,
                       stroke_width=4).move_to([x, y + 0.15 * s, 0])
    base = RoundedRectangle(corner_radius=0.08 * s, width=2.6 * s, height=0.22 * s, fill_color=BOX_R, fill_opacity=1,
                            stroke_color=INK, stroke_width=5).move_to([x, y - 0.72 * s, 0])
    return VGroup(base, bezel, screen)


def pB_pipe(a, b, w=18):
    """A pipe: an ink outline with a grey core, straight from a to b."""
    outer = Line(a, b, color=INK, stroke_width=w + 8)
    inner = Line(a, b, color=BAR2, stroke_width=w)
    g = VGroup(outer, inner)
    return g


def pB_arrow(a, b, w=6, tip=0.3):
    return Arrow(a, b, color=INK, stroke_width=w, buff=0, tip_length=tip, max_tip_length_to_length_ratio=0.5)


class B23_TunnelTarget(Scene):
    """Two tunnels from the laptop: the first ends at localhost on the login node (nothing there), the second runs
    through it to the compute node and the model; the direct line from the laptop to the compute node is crossed out."""
    def construct(self):
        lap = pB_laptop(-4.9, -0.95, 0.9)
        lap_l = T("laptop", 36).move_to([-4.9, -2.75, 0])
        il = Iso(-0.9, -2.0, 0.95)
        lst, llt = explorer_rack(il)
        login = VGroup(lst, llt)
        login_l = T("login node", 36).move_to([-0.9, -2.75, 0])
        ic = Iso(3.9, -2.0, 1.35)
        cst, clt = explorer_rack(ic)
        comp = VGroup(cst, clt)
        comp_l = T("compute node", 36).move_to([3.9, -2.75, 0])
        oll = logo_chip("ollama", 3.9, 1.95, h=1.1)
        self.play(FadeIn(lap), FadeIn(lap_l), FadeIn(login), FadeIn(login_l), FadeIn(comp), FadeIn(comp_l), FadeIn(oll), run_time=0.5)

        # the first tunnel: it ends on the login node, at its own localhost
        p1 = pB_pipe([-3.7, -0.55, 0], [-2.0, -0.55, 0])
        p1l = M("ssh -L", 32).move_to([-2.85, -0.05, 0])
        hear(self, "tunnel", lead=0.0)
        self.play(Create(p1), FadeIn(p1l), run_time=0.6)
        hear(self, "local host", lead=0.1)
        lh = M("localhost", 32).move_to([-0.9, 0.6, 0])
        self.play(FadeIn(lh), run_time=0.3)
        hear(self, "login node", lead=0.3)
        self.play(Indicate(login_l, color=INK, scale_factor=1.12), run_time=0.5)
        hear(self, "not the machine", lead=0.15)
        xl = x_mark(0.95, 0.6, r=0.25, w=9)
        self.play(Create(xl), run_time=0.3)
        hear(self, "running your model", lead=0.1)
        self.play(Indicate(oll, color=INK, scale_factor=1.1), run_time=0.5)

        # the second tunnel: it runs behind the login node and lands on the compute node
        p2 = pB_pipe([-3.7, -1.3, 0], [2.4, -1.3, 0])
        p2.set_z_index(-1)
        p2l = M("ssh -L", 32).move_to([-2.85, -1.95, 0])
        at(self, 5.2)
        self.play(Create(p2), FadeIn(p2l), run_time=0.75)
        hear(self, "compute node because", lead=0.2)
        ck = check(1.3, -0.8, s=0.3, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.4)

        # no direct line from the laptop to the GPU node
        hear(self, "does not support", lead=0.3)
        arc = ArcBetweenPoints([-4.9, 0.1, 0], [2.3, 0.9, 0], angle=-1.85)
        dashed = DashedVMobject(arc, num_dashes=34)
        dashed.set_color(INK)
        self.play(Create(dashed), run_time=0.8)
        hear(self, "SSH straight", lead=0.1)
        top = arc.point_from_proportion(0.5)
        xd = x_mark(top[0], top[1], r=0.3, w=10)
        self.play(Create(xd), run_time=0.25)
        hear(self, "straight into", lead=0.0)
        nd = T("no direct ssh", 36).move_to([top[0], top[1] + 0.65, 0])
        self.play(FadeIn(nd), run_time=0.3)
        done(self)


class B24_AliasMap(Scene):
    """Claude fans out four model names; unmapped, they all hit ollama's empty shelf; mapped, all four land on one local model."""
    def construct(self):
        sx = -3.55
        yc = -0.1
        rows = {"haiku": 1.5, "sonnet": 0.5, "opus": -0.5, "subagent": -1.65}
        claude = logo_chip("claude", -5.0, yc)
        stub = Line([-4.1, yc, 0], [sx, yc, 0], color=INK, stroke_width=6)
        panel = Rectangle(width=2.0, height=4.0, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.4, yc, 0])
        slots = VGroup(*[Rectangle(width=1.5, height=0.5, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([3.4, y, 0]) for y in rows.values()])
        oll = logo_chip("ollama", 3.4, 2.4, h=1.0)
        self.play(FadeIn(claude), Create(stub), FadeIn(panel), FadeIn(slots), FadeIn(oll), run_time=0.5)

        def row(name, y):
            seg = Line([sx, yc, 0], [sx, y, 0], color=INK, stroke_width=6)
            arr = pB_arrow([sx, y, 0], [2.35, y, 0])
            lab = T(name, 34)
            dy = -0.42 if name == "subagent" else 0.38
            lab.move_to([sx + 0.3 + lab.width / 2, y + dy, 0])
            return seg, arr, lab

        r = {n: row(n, y) for n, y in rows.items()}
        # the small model does the background tasks
        hear(self, "small model", lead=0.3)
        self.play(Create(r["haiku"][0]), Create(r["haiku"][1]), FadeIn(r["haiku"][2]), run_time=0.5)
        hear(self, "background tasks", lead=0.2)
        bg = chip("background tasks", -0.2, 2.2, size=32)
        self.play(FadeIn(bg), run_time=0.3)
        # subagents have a setting of their own
        hear(self, "separate setting", lead=0.3)
        self.play(Create(r["subagent"][0]), Create(r["subagent"][1]), FadeIn(r["subagent"][2]), run_time=0.5)
        # the other two names are asked for as well, none of them mapped
        hear(self, "Unless you point", lead=0.2)
        self.play(*[Create(m) for n in ("sonnet", "opus") for m in r[n][:2]], *[FadeIn(r[n][2]) for n in ("sonnet", "opus")], run_time=0.6)

        # ollama has none of these models
        hear(self, "Claude models it does not have", lead=0.3)
        crosses = VGroup(*[x_mark(3.4, y, r=0.2, w=7) for y in rows.values()])
        nf = chip("model not found", 3.4, -2.75, mono=True, size=32)
        self.play(*[Create(c) for c in crosses], FadeIn(nf), run_time=0.5)

        # the script sets every name to one local model
        hear(self, "So the script sets", lead=0.1)
        block = Rectangle(width=1.4, height=1.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.4, yc, 0])
        lm = T("local model", 38).move_to([3.4, -2.6, 0])
        self.play(FadeOut(slots), FadeOut(crosses), FadeOut(nf), run_time=0.3)
        self.play(FadeIn(block), FadeIn(lm), run_time=0.4)
        ends = {"haiku": 0.25, "sonnet": 0.05, "opus": -0.15, "subagent": -0.35}
        new = {}

        def remap(n):
            y = rows[n]
            a = pB_arrow([sx, y, 0], [2.7, yc + ends[n], 0])
            new[n] = a
            return a
        hear(self, "small medium", lead=0.0)
        self.play(FadeOut(r["haiku"][1]), Create(remap("haiku")), run_time=0.45)
        hear(self, "medium", lead=0.0)
        self.play(FadeOut(r["sonnet"][1]), Create(remap("sonnet")), run_time=0.45)
        hear(self, "large", lead=0.0)
        self.play(FadeOut(r["opus"][1]), Create(remap("opus")), run_time=0.45)
        hear(self, "subagent model", lead=0.1)
        self.play(FadeOut(r["subagent"][1]), Create(remap("subagent")), run_time=0.45)
        hear(self, "to one local model", lead=0.1)
        ck = check(3.4, 1.3, s=0.28, color=TERRA, w=12)
        en = chip("every name", -0.4, -2.75, mono=True, size=32)
        self.play(Create(ck), FadeIn(en), run_time=0.45)
        done(self)


class B25_SilentTruncation(Scene):
    """The default window is a short bar: instructions and tools pour in, the overflow is cut without a sound; at 65,536 all fit."""
    def construct(self):
        x0, per_k, h = -5.6, 10.5 / 65.536, 1.3
        bh = 1.0
        cw = T("context window", 40)
        cw.move_to([x0 + cw.width / 2, 2.3, 0])
        ruler = Line([x0, -2.1, 0], [x0 + 10.5, -2.1, 0], color=INK, stroke_width=5)
        t0 = Line([x0, -2.1, 0], [x0, -1.85, 0], color=INK, stroke_width=5)
        self.play(FadeIn(cw), Create(ruler), Create(t0), run_time=0.45)

        def tick(k, txt):
            x = x0 + k * per_k
            ln = Line([x, -2.1, 0], [x, -1.8, 0], color=INK, stroke_width=6)
            lab = T(txt, 36).move_to([x, -2.65, 0])
            return ln, lab

        # the 4k default: a short window with a wall at its edge, then the 32k tick
        hear(self, "4 000 tokens", lead=0.45)
        w4 = Rectangle(width=4.0 * per_k, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
        w4.move_to([x0 + 2.0 * per_k, 0, 0])
        wall = Line([x0 + 4.0 * per_k, -0.9, 0], [x0 + 4.0 * per_k, 0.9, 0], color=INK, stroke_width=9)
        wall.set_z_index(5)
        k4, l4 = tick(4.0, "4k")
        self.play(GrowFromEdge(w4, LEFT), Create(wall), Create(k4), FadeIn(l4), run_time=0.45)
        hear(self, "32 000", lead=0.3)
        k32, l32 = tick(32.0, "32k")
        self.play(Create(k32), FadeIn(l32), run_time=0.35)

        def blocks():
            specs = [("instructions", 1.9), ("tools", 2.6), ("your code", 2.2)]
            out, xs = [], x0
            for name, w in specs:
                b = Rectangle(width=w, height=bh, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
                b.move_to([xs + w / 2, 0, 0])
                lab = T(name, 36).move_to([xs + w / 2, -1.15, 0])
                out.append((b, lab, xs, w))
                xs += w + 0.2
            return out

        bl = blocks()
        # the instructions pour in: only a sliver fits in the window
        inside_w = 4.0 * per_k
        b0, lab0, bx0, bw0 = bl[0]
        ins_in = Rectangle(width=inside_w, height=bh, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([bx0 + inside_w / 2, 0, 0])
        ins_out = Rectangle(width=bw0 - inside_w, height=bh, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([bx0 + inside_w + (bw0 - inside_w) / 2, 0, 0])
        grp0 = VGroup(ins_in, ins_out)
        grp0.shift(UP * 1.4)
        at(self, 8.0)
        self.add(grp0)
        self.play(grp0.animate.shift(DOWN * 1.4), run_time=0.5, rate_func=ease_in)
        self.play(FadeIn(lab0), run_time=0.2)
        # the tool list pours in behind it
        hear(self, "tool list", lead=0.35)
        b1, lab1, bx1, bw1 = bl[1]
        b1.shift(UP * 1.4)
        self.add(b1)
        self.play(b1.animate.shift(DOWN * 1.4), run_time=0.45, rate_func=ease_in)
        self.play(FadeIn(lab1), run_time=0.2)
        # the overflow is cut, silently
        hear(self, "is cut", lead=0.2)
        self.play(FadeOut(ins_out), FadeOut(b1), FadeOut(lab0), FadeOut(lab1), run_time=0.7)

        # a window of 65,536: every block fits
        hear(self, "Ask for", lead=0.1)
        w65 = Rectangle(width=65.536 * per_k, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
        w65.move_to([x0 + 65.536 * per_k / 2, 0, 0])
        wall2 = Line([x0 + 10.5, -0.9, 0], [x0 + 10.5, 0.9, 0], color=INK, stroke_width=9)
        wall2.set_z_index(5)
        k65 = Line([x0 + 10.5, -2.1, 0], [x0 + 10.5, -1.8, 0], color=INK, stroke_width=6)
        num = M("65,536", 44).move_to([x0 + 10.5 - 0.95, 2.3, 0])
        self.play(FadeOut(w4), FadeOut(wall), FadeOut(ins_in), GrowFromEdge(w65, LEFT), Create(wall2), Create(k65), FadeIn(num), run_time=0.65)
        hear(self, "65 536", lead=0.1)
        fresh = blocks()
        for b, lab, bx, bw in fresh:
            b.shift(UP * 1.4)
            self.add(b)
        self.play(LaggedStart(*[b.animate.shift(DOWN * 1.4) for b, _, _, _ in fresh], lag_ratio=0.3), run_time=1.0, rate_func=ease_in)
        self.play(*[FadeIn(lab) for _, lab, _, _ in fresh], run_time=0.3)
        hear(self, "or more", lead=0.3)
        ck = check(3.7, 0.0, s=0.35, color=TERRA, w=13)
        ck.set_z_index(6)
        self.play(Create(ck), run_time=0.4)
        done(self)


def pB_cards(cx, cy, cols=6, rows=4, cw=0.42, ch=0.56, gap=0.08):
    """A pile of small tool cards laid out as a block (24 by default: dozens)."""
    cards = VGroup()
    w = cols * cw + (cols - 1) * gap
    h = rows * ch + (rows - 1) * gap
    for r_ in range(rows):
        for c_ in range(cols):
            x = cx - w / 2 + cw / 2 + c_ * (cw + gap)
            y = cy + h / 2 - ch / 2 - r_ * (ch + gap)
            cards.add(Rectangle(width=cw, height=ch, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y, 0]))
    return cards


class B26_TooSmallModel(Scene):
    """A tiny model is offered the pile of tool definitions and drops it; the big model holds the whole pile."""
    def construct(self):
        ruler = Line([-5.6, -3.0, 0], [5.6, -3.0, 0], color=INK, stroke_width=5)
        ticks = VGroup(*[Line([x, -3.0, 0], [x, -2.8 if i % 5 else -2.65, 0], color=INK, stroke_width=3) for i, x in enumerate(np.arange(-5.6, 5.61, 0.4))])
        self.play(Create(ruler), Create(ticks), run_time=0.5)
        # the tiny model
        hear(self, "one and a half billion", lead=0.2)
        tiny = Rectangle(width=1.7, height=1.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-3.5, -0.9, 0])
        tl = T("1.5B", 44).move_to([-3.5, -2.3, 0])
        self.play(FadeIn(tiny), FadeIn(tl), run_time=0.4)
        hear(self, "reasoning model", lead=0.2)
        led = Dot([-3.5 + 0.55, -0.9 + 0.55, 0], radius=0.14, color=TERRA)
        self.play(FadeIn(led, scale=1.8), run_time=0.3)
        # the pile of tool definitions is offered to it
        hear(self, "cannot reliably", lead=0.15)
        pile = pB_cards(-3.5, 1.25)
        self.play(FadeIn(pile, shift=DOWN * 1.6), run_time=0.55)
        # it cannot hold them: every card spills
        hear(self, "drive an agent loop", lead=0.3)
        rng = np.random.RandomState(7)
        spills = []
        for i, c_ in enumerate(pile):
            side = 1 if i % 2 else -1
            tx = -3.5 + side * rng.uniform(1.3, 2.3)
            ty = -1.55 + rng.uniform(-0.12, 0.12)
            spills.append(c_.animate.move_to([tx, ty, 0]).rotate(float(rng.uniform(-1.2, 1.2))))
        self.play(LaggedStart(*spills, lag_ratio=0.03), run_time=1.2)
        xm = x_mark(-1.0, 0.9, r=0.3, w=10)
        self.play(Create(xm), run_time=0.3)

        # dozens of tool definitions
        hear(self, "dozens of tool definitions", lead=0.3)
        td = T("tool definitions", 36).move_to([-0.7, 2.85, 0])
        self.play(FadeIn(td), run_time=0.3)

        # the big model holds the whole pile
        hear(self, "Use a tool capable", lead=0.1)
        big = Rectangle(width=4.6, height=3.8, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([2.9, 0.15, 0])
        bl = T("20B to 120B", 44).move_to([2.9, -2.3, 0])
        self.play(FadeIn(big), FadeIn(bl), run_time=0.45)
        pile2 = pB_cards(2.9, 0.15)
        self.play(FadeIn(pile2, shift=DOWN * 1.6), run_time=0.6)
        hear(self, "in the range", lead=0.2)
        ck = check(5.55, 1.8, s=0.32, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.4)
        hear(self, "20 to 120", lead=0.1)
        self.play(Indicate(bl, color=INK, scale_factor=1.1), run_time=0.5)
        done(self)


def pB_clock(x, y, r=0.5):
    face = Circle(radius=r, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    minute = Line([x, y, 0], [x, y + r * 0.7, 0], color=INK, stroke_width=6)
    hour = Line([x, y, 0], [x + r * 0.4, y, 0], color=INK, stroke_width=7)
    hub = Dot([x, y, 0], radius=0.07, color=INK)
    g = VGroup(face, hour, minute, hub)
    g.minute, g.cx, g.cy = minute, x, y
    return g


def pB_tag(text, x, y, w=6.2, h=1.5):
    """A price tag: a white tag with a pointed end and a punched hole, carrying a short phrase."""
    pts = [[x - w / 2, y, 0], [x - w / 2 + 0.7, y + h / 2, 0], [x + w / 2, y + h / 2, 0], [x + w / 2, y - h / 2, 0], [x - w / 2 + 0.7, y - h / 2, 0]]
    shadow = Polygon(*[[p[0] + 0.1, p[1] - 0.1, 0] for p in pts], fill_color=BOX_L, fill_opacity=1, stroke_width=0)
    card = Polygon(*pts, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0)
    hole = Circle(radius=0.12, fill_color=STAGE, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x - w / 2 + 0.55, y, 0])
    lab = T(text, 44).move_to([x + 0.4, y, 0])
    g = VGroup(shadow, card, hole, lab)
    g.lab = lab
    return g


def pB_label(txt, size, x, y_base):
    """A label whose BASELINE sits at y_base (a row of labels shares one line, descenders or not)."""
    lab = T(txt, size)
    d = 0.0
    if any(c in "gjpqy" for c in txt):
        d = T("x", size).get_bottom()[1] - T("q", size).get_bottom()[1]
    lab.move_to([x, y_base, 0])
    lab.shift(UP * ((y_base - d) - lab.get_bottom()[1]))
    return lab


class B27_NotFree(Scene):
    """'zero marginal cost' is struck out and slides off; a queue, a draining fair share and an idle watcher take its place; no per-token billing lands below."""
    def construct(self):
        tag = pB_tag("zero marginal cost", -0.4, 1.0)
        strike = x_mark(3.45, 1.0, r=0.38, w=12)
        hear(self, "zero marginal cost", lead=0.3)
        self.play(FadeIn(tag), run_time=0.4)
        hear(self, "marginal cost", lead=0.1)
        self.play(Create(strike), run_time=0.3)

        ly = -0.95   # baseline of every meter label
        # the tag slides off and the fair-share gauge takes its place
        hear(self, "GPU hours", lead=0.95)
        self.play(FadeOut(VGroup(tag, strike), shift=RIGHT * 3.0), run_time=0.35)
        gc, gw, gh = 1.3, 1.3, 2.9
        tank = Rectangle(width=gw, height=gh, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([0.0, gc, 0])
        fh = gh - 0.3
        base = gc - gh / 2 + 0.15
        full = Rectangle(width=gw - 0.3, height=fh, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([0.0, base + fh / 2, 0])
        low = Rectangle(width=gw - 0.3, height=0.6, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([0.0, base + 0.3, 0])
        fl = pB_label("fair share", 40, 0.0, ly)
        self.play(FadeIn(tank), FadeIn(full), FadeIn(fl), run_time=0.35)
        hear(self, "fair share", lead=0.1)
        self.play(Transform(full, low), run_time=0.7)
        # the queue: boxes in a line, a clock that waits
        hear(self, "you wait in a queue", lead=0.2)
        clk = pB_clock(-4.1, 2.0, 0.65)
        boxes = VGroup(*[Rectangle(width=0.5, height=0.66, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-5.15 + 0.72 * i, 0.55, 0]) for i in range(4)])
        desk = Line([-2.65, 0.1, 0], [-2.65, 1.0, 0], color=INK, stroke_width=9)
        ql = pB_label("queue", 40, -4.1, ly)
        self.play(FadeIn(clk), FadeIn(ql), FadeIn(desk), LaggedStart(*[FadeIn(b, shift=LEFT * 0.3) for b in boxes], lag_ratio=0.2), run_time=0.6)
        self.play(Rotate(clk.minute, angle=-2 * PI, about_point=[clk.cx, clk.cy, 0]), run_time=0.7, rate_func=linear)
        # the idle watcher
        hear(self, "idle watcher", lead=0.2)
        lens = Circle(radius=0.85, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=8).move_to([3.8, 1.6, 0])
        handle = Line([3.8 + 0.6, 1.6 - 0.6, 0], [3.8 + 1.4, 1.6 - 1.4, 0], color=INK, stroke_width=16)
        job = Rectangle(width=0.7, height=0.55, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.8, 1.6, 0])
        wl = pB_label("idle watcher", 40, 4.0, ly)
        self.play(FadeIn(lens), FadeIn(handle), FadeIn(job), FadeIn(wl), run_time=0.45)
        hear(self, "cancels jobs", lead=0.3)
        xj = x_mark(3.8, 1.6, r=0.3, w=9)
        self.play(Create(xj), run_time=0.3)

        # the accurate claim
        hear(self, "no per token billing", lead=0.6)
        plq = chip("no per-token billing", -1.5, -2.25, size=44)
        plq.shift(UP * 0.7)
        self.add(plq)
        self.play(plq.animate.shift(DOWN * 0.7), run_time=0.5, rate_func=smooth)
        # where the cost went
        hear(self, "queue time", lead=0.1)
        self.play(Indicate(ql, color=INK, scale_factor=1.2), run_time=0.5)
        hear(self, "fair share", lead=0.1, nth=1)
        self.play(Indicate(fl, color=INK, scale_factor=1.2), run_time=0.5)
        hear(self, "capability", lead=0.2)
        cap = chip("capability", 4.0, -2.25, size=44)
        self.play(FadeIn(cap, shift=LEFT * 0.3), run_time=0.4)
        done(self)


def pB_folder(x, y, w=1.6, h=1.1):
    """A folder with a dotted outline: a hidden folder."""
    body = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    tab = Rectangle(width=w * 0.4, height=0.24, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x - w * 0.3, y + h / 2 + 0.12, 0])
    ob = DashedVMobject(Rectangle(width=w, height=h, color=INK, stroke_width=5).move_to([x, y, 0]), num_dashes=30)
    ot = DashedVMobject(Rectangle(width=w * 0.4, height=0.24, color=INK, stroke_width=5).move_to([x - w * 0.3, y + h / 2 + 0.12, 0]), num_dashes=10)
    return VGroup(tab, body, ob, ot)


class B31_HomeFills(Scene):
    """The hidden cache fills home's quota (cross); cache and temp are redirected to your storage; the pull runs on the compute node, not the login node."""
    def construct(self):
        ih = Iso(-4.1, 0.4, 1.05)
        home = home_box(ih)
        hl = T("home", 38).move_to([-4.1, 0.0, 0])
        gx, gy0, gh = -5.8, 0.55, 2.0
        gauge = Rectangle(width=0.5, height=gh, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([gx, gy0 + gh / 2, 0])
        gl = T("quota", 34).move_to([gx + 0.1, 0.0, 0])
        self.play(FadeIn(home), FadeIn(hl), FadeIn(gauge), FadeIn(gl), run_time=0.5)

        # the hidden cache folder, inside home, filling the quota
        hear(self, "hidden folder", lead=0.4)
        fold = pB_folder(-1.3, 1.55)
        fl = M(".apptainer", 32).move_to([-1.3, 0.7, 0])
        self.play(FadeIn(fold), FadeIn(fl), run_time=0.4)
        hear(self, "in home", lead=0.25)
        into = pB_arrow([-2.25, 1.55, 0], [-3.1, 1.55, 0], w=7, tip=0.28)
        self.play(Create(into), run_time=0.3)
        hear(self, "fills first", lead=0.6)
        fill = Rectangle(width=0.38, height=gh - 0.1, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([gx, gy0 + 0.05 + (gh - 0.1) / 2, 0])
        self.play(GrowFromEdge(fill, DOWN), run_time=0.9, rate_func=linear)
        xg = x_mark(gx, 2.95, r=0.22, w=9)
        self.play(Create(xg), run_time=0.25)

        # point the cache and temp folders at your own storage
        hear(self, "So point", lead=0.4)
        isb = Iso(3.4, 0.3, 0.75)
        sb_back, sb_front = scratch_bin(isb)
        sl = T("your storage", 38).move_to([3.7, 3.0, 0])
        self.play(FadeOut(into), FadeIn(sb_back), FadeIn(sb_front), FadeIn(sl), run_time=0.45)
        a1 = pB_arrow([-0.35, 1.85, 0], [2.0, 1.85, 0], w=7, tip=0.28)
        a2 = pB_arrow([-0.35, 1.3, 0], [2.0, 1.3, 0], w=7, tip=0.28)
        l1 = T("cache", 34).move_to([0.8, 2.3, 0])
        l2 = T("temp", 34).move_to([0.8, 0.85, 0])
        self.play(Create(a1), Create(a2), FadeIn(l1), FadeIn(l2), run_time=0.55)

        # pull the images there, on a compute node rather than the login node
        hear(self, "pull the images", lead=1.0)
        il = Iso(-2.6, -2.65, 0.95)
        lst, llt = explorer_rack(il)
        login = VGroup(lst, llt)
        lll = T("login node", 36).move_to([-2.6, -3.05, 0])
        ic = Iso(1.9, -2.65, 0.95)
        cst, clt = explorer_rack(ic)
        comp = VGroup(cst, clt)
        cl = T("compute node", 36).move_to([1.9, -3.05, 0])
        self.play(FadeIn(login), FadeIn(lll), FadeIn(comp), FadeIn(cl), run_time=0.5)
        hear(self, "pull the images", lead=0.1)
        img = Iso(0, 0, 0.8).box(0, 0, 0, 0.7, 0.7, 0.6)
        img.move_to([1.9, -0.45, 0])
        img.set_z_index(1)
        self.play(FadeIn(img), run_time=0.2)
        target = isb.p(1.35, 0.9, 0.35)
        self.play(img.animate.move_to([target[0], target[1] + 0.1, 0]), run_time=0.9, rate_func=smooth)
        hear(self, "on a compute node", lead=0.1)
        ck = check(3.45, -1.2, s=0.3, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.35)
        hear(self, "login node", lead=0.0)
        xl = x_mark(-2.6, -0.3, r=0.3, w=10)
        self.play(Create(xl), login.animate.set_opacity(0.4), run_time=0.4)
        done(self)


# ═════════════════════════════ PART C — B40 B41 B42 B43 B44 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pC_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pC_slow(t):
    """Fast, then crawling: a stopwatch hand that ends up barely moving."""
    return 1 - (1 - t) ** 5


def pC_stopwatch(x, y, r=0.6):
    face = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    knob = Rectangle(width=0.26, height=0.16, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + r + 0.12, 0])
    hand = Line([x, y, 0], [x, y + r * 0.7, 0], color=INK, stroke_width=7)
    hub = Dot([x, y, 0], radius=0.07, color=INK)
    g = VGroup(knob, face, hand, hub)
    g.hand, g.cx, g.cy = hand, x, y
    return g


def pC_blk(cx, y0, w, h, fill=BAR1, sw=4):
    """A block standing on y0 (its bottom edge), centred on cx."""
    return Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=sw).move_to([cx, y0 + h / 2, 0])


def pC_tank(cx, yb, yt, w):
    """The video-memory tank: a white fill and an open-topped U wall in ink."""
    fill = Rectangle(width=w, height=yt - yb, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([cx, (yt + yb) / 2, 0])
    wall = VMobject(stroke_color=INK, stroke_width=9, fill_opacity=0)
    wall.set_points_as_corners([[cx - w / 2, yt, 0], [cx - w / 2, yb, 0], [cx + w / 2, yb, 0], [cx + w / 2, yt, 0]])
    return VGroup(fill, wall)


def pC_proc(x, y):
    """The processor: a dark chip body with kraft pins on both sides."""
    body = Rectangle(width=2.3, height=1.0, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    pins = VGroup(*[Line([x + s * 1.15, y + dy, 0], [x + s * 1.42, y + dy, 0], color=KRAFT_DEEP, stroke_width=7)
                    for s in (-1, 1) for dy in (-0.28, 0.0, 0.28)])
    return VGroup(pins, body)


class B40_FitInVram(Scene):
    """Weights sink into the video-memory tank, the cache stacks on them (a check); a bigger cache overflows the top and
    the spilled part drops onto the processor, where the stopwatch crawls."""
    def construct(self):
        cx, yb, yt, tw, bw = -0.1, -2.75, 1.35, 2.4, 2.0
        title = pC_act_title("IV · Choose A GPU And A Model")
        tank = pC_tank(cx, yb, yt, tw)
        vlab = T("video memory", 36)
        vlab.move_to([-1.65 - vlab.width / 2, 1.0, 0])
        wt = pC_blk(cx, yb + 0.06, bw, 1.75, BAR1)
        wlab = T("weights", 34)
        wlab.move_to([-1.65 - wlab.width / 2, -1.815, 0])
        cache = pC_blk(cx, -0.88, bw, 0.9, BAR2)
        clab = T("context cache", 34)
        clab.move_to([-1.65 - clab.width / 2, -0.43, 0])
        ck = check(1.95, 0.75, s=0.3, color=TERRA, w=12)
        cache_full = pC_blk(cx, -0.88, bw, yt + 0.88, BAR2)
        spill = pC_blk(cx, yt, bw, 0.95, BAR2)
        oll = logo_chip("ollama", 5.2, 2.3, h=1.3)
        proc = pC_proc(4.2, -1.95)
        plab = T("processor", 36).move_to([4.2, -2.95, 0])
        sw = pC_stopwatch(3.0, 0.75, 0.65)
        crawl = T("crawl", 48).move_to([4.9, 0.75, 0])

        self.play(FadeIn(title), FadeIn(tank), FadeIn(vlab), run_time=0.5)
        # "the model's weights": the weights block sinks into the tank
        hear(self, "weights", lead=0.15)
        wt.shift(UP * 2.29)
        self.play(FadeIn(wt), run_time=0.15)
        self.play(wt.animate.shift(DOWN * 2.29), run_time=0.5, rate_func=ease_in)
        self.play(FadeIn(wlab), run_time=0.25)
        # "room left for the context window's cache": the cache stacks on top, then the check
        hear(self, "room left", lead=0.45)
        cache.shift(UP * 1.33)
        self.play(FadeIn(cache), run_time=0.15)
        self.play(cache.animate.shift(DOWN * 1.33), run_time=0.5, rate_func=ease_in)
        self.play(Create(ck), run_time=0.3)
        hear(self, "context windows", lead=0.1)
        self.play(FadeIn(clab), run_time=0.25)
        # "if either spills over": the cache grows to the brim, then past it
        hear(self, "spills over", lead=0.4)
        self.play(FadeOut(ck), Transform(cache, cache_full), run_time=0.5)
        hear(self, "over", lead=0.25)
        self.play(GrowFromEdge(spill, DOWN), run_time=0.4)
        # "Ollama pushes layers onto the processor": the spilled part rides over and drops on the chip
        hear(self, "Olama", lead=0.1)
        self.play(FadeIn(oll), FadeIn(proc), run_time=0.4)
        hear(self, "pushes", lead=0.05)
        a, b = np.array([cx, yt + 0.475, 0.0]), np.array([4.2, -1.45 + 0.475, 0.0])
        self.play(MoveAlongPath(spill, ArcBetweenPoints(a, b, angle=1.0)), run_time=0.85, rate_func=smooth)
        hear(self, "processor", lead=0.1)
        self.play(FadeIn(plab), run_time=0.3)
        # "generation slows to a crawl": the stopwatch spins, then its hand barely moves
        hear(self, "generation", lead=0.1)
        self.play(FadeIn(sw), run_time=0.25)
        self.play(Rotate(sw.hand, angle=-1.9 * PI, about_point=[sw.cx, sw.cy, 0]), run_time=1.0, rate_func=pC_slow)
        hear(self, "a crawl", lead=0.1)
        self.play(FadeIn(crawl), Rotate(sw.hand, angle=-0.25, about_point=[sw.cx, sw.cy, 0], rate_func=linear), run_time=0.7)
        done(self)


def pC_hatch(xa, xb, ya, yb, gap=0.2, color=BAR1, sw=3.5):
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


def pC_ruler(x0, scale, vmax, step, y, size=32):
    """A gigabyte ruler: ink line, ticks, numerals. Returns (line, ticks, numerals)."""
    line = Line([x0, y, 0], [x0 + vmax * scale, y, 0], color=INK, stroke_width=6)
    ticks = VGroup(*[Line([x0 + v * scale, y, 0], [x0 + v * scale, y - 0.28, 0], color=INK, stroke_width=6) for v in range(0, vmax + 1, step)])
    nums = VGroup(*[T(str(v), size).move_to([x0 + v * scale, y - 0.56, 0]) for v in range(0, vmax + 1, step)])
    return line, ticks, nums


def pC_model_label(company, text, x, y):
    """A maker's logo, then the model name beside it."""
    lg = logo_chip(company, x + 0.45, y, h=0.6)
    lab = T(text, 32)
    lab.move_to([x + 1.05 + lab.width / 2, y, 0])
    return Group(lg, lab)


def pC_bar_num(text, x_end, y):
    """A numeral sitting inside the right end of a bar (ink on grey)."""
    n = T(text, 38, bold=True)
    return n.move_to([x_end - 0.22 - n.width / 2, y, 0])


class B41_ModelsThatFit(Scene):
    """Three bars to scale on one gigabyte ruler: 14, 19, and 19 with a hatched extension out to 23."""
    def construct(self):
        x0, sc, bh = -5.5, 0.42, 0.64
        ys = [1.8, 0.15, -1.5]
        ex = lambda gb: x0 + gb * sc
        axis = Line([x0, 2.15, 0], [x0, -2.45, 0], color=BAR2, stroke_width=6)
        rl, rt, rn = pC_ruler(x0, sc, 25, 5, -2.45)
        gb = T("GB", 34).move_to([ex(25) + 0.7, -3.01, 0])
        dsz = T("download size", 36).move_to([6.1 - 1.31, 2.8, 0])
        labs = [pC_model_label("openai", "gpt-oss 20b", -5.4, ys[0] + 0.8),
                pC_model_label("qwen", "qwen3-coder 30b", -5.4, ys[1] + 0.8),
                pC_model_label("glm", "glm-4.7-flash", -5.4, ys[2] + 0.8)]
        b1 = pC_blk(0, 0, 14 * sc, bh, BAR2, 4).move_to([ex(7), ys[0], 0])
        b2 = pC_blk(0, 0, 19 * sc, bh, BAR2, 4).move_to([ex(9.5), ys[1], 0])
        b3 = pC_blk(0, 0, 19 * sc, bh, BAR2, 4).move_to([ex(9.5), ys[2], 0])
        n1, n2, n3 = pC_bar_num("14", ex(14), ys[0]), pC_bar_num("19", ex(19), ys[1]), pC_bar_num("19", ex(19), ys[2])
        ext_box = Rectangle(width=4 * sc, height=bh, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([ex(21), ys[2], 0])
        ext = VGroup(ext_box, pC_hatch(ex(19), ex(23), ys[2] - bh / 2 + 0.03, ys[2] + bh / 2 - 0.03, gap=0.22))
        n23 = T("23", 44, bold=True).move_to([ex(23) + 0.55, ys[2], 0])
        tag1 = T("video memory", 32)
        tag2 = T("at 64k context", 32)
        tg = VGroup(tag1, tag2).arrange(RIGHT, buff=0.2)
        tg.move_to([6.1 - tg.width / 2, ys[2] + 0.8, 0])

        self.play(Create(axis), Create(rl), FadeIn(rt), FadeIn(rn), FadeIn(gb), FadeIn(dsz), run_time=0.7)
        # "the 20 billion GPT-OSS is about 14 gigabytes"
        hear(self, "20 billion", lead=0.2)
        self.play(FadeIn(labs[0]), run_time=0.3)
        hear(self, "about 14", lead=0.25)
        self.play(GrowFromEdge(b1, LEFT), run_time=0.8)
        self.play(FadeIn(n1), run_time=0.2)
        # "the 30 billion Qwen 3 Coder is about 19"
        hear(self, "30 billion", lead=0.2)
        self.play(FadeIn(labs[1]), run_time=0.3)
        hear(self, "about 19", lead=0.25)
        self.play(GrowFromEdge(b2, LEFT), run_time=0.75)
        self.play(FadeIn(n2), run_time=0.2)
        # "GLM 4.7 Flash is also about 19 to download"
        hear(self, "GLM", lead=0.05)
        self.play(FadeIn(labs[2]), run_time=0.3)
        hear(self, "also about 19", lead=0.2)
        self.play(GrowFromEdge(b3, LEFT), run_time=0.8)
        self.play(FadeIn(n3), run_time=0.2)
        # "but Ollama puts it near 23 of video memory at 64,000 context": the hatched extension
        hear(self, "near 23", lead=0.5)
        self.play(GrowFromEdge(ext, LEFT), run_time=0.8)
        self.play(FadeIn(n23), run_time=0.2)
        hear(self, "video memory", lead=0.3)
        self.play(FadeIn(tag1), run_time=0.3)
        hear(self, "at 64", lead=0.1)
        self.play(FadeIn(tag2), run_time=0.3)
        done(self)


def pC_stamp(text, x, y, w=1.75):
    """A stamp on a card: kraft pill, ink outline, a terracotta dot, a short word."""
    sh = pill(x + 0.07, y - 0.07, w, h=0.7, fill=BOX_L)
    body = RoundedRectangle(width=w, height=0.7, corner_radius=0.35, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    dot = Dot([x - w / 2 + 0.32, y, 0], radius=0.1, color=TERRA)
    lab = T(text, 34).move_to([x + 0.22, y, 0])
    return VGroup(sh, body, dot, lab)


def pC_gear(x, y, r=0.55, teeth=8):
    """A gear: a toothed kraft polygon and a hub. `.cx`, `.cy` for rotating it about its centre."""
    pts = []
    for i in range(teeth * 2):
        ang = PI * i / teeth
        rr = r if i % 2 == 0 else r * 0.74
        pts.append([x + rr * np.cos(ang), y + rr * np.sin(ang), 0])
    body = Polygon(*pts, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
    hub = Circle(radius=r * 0.27, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    g = VGroup(body, hub)
    g.cx, g.cy = x, y
    return g


class B42_StrongestAndTools(Scene):
    """One long 65 GB bar is ringed as the strongest on one card; two model cards: the stamped one runs the call, the other prints it."""
    def construct(self):
        x0, sc, by = -2.2, 0.1014, 1.55
        ex = lambda gb: x0 + gb * sc
        rl, rt, rn = pC_ruler(x0, sc, 70, 10, 0.85)
        gb = T("GB", 34).move_to([ex(70) + 0.8, 0.23, 0])
        lab = pC_model_label("openai", "gpt-oss 120b", -6.05, by)
        bar = pC_blk(0, 0, 65 * sc, 0.7, BAR2, 4).move_to([ex(32.5), by, 0])
        n65 = pC_bar_num("65", ex(65), by)
        ring = RoundedRectangle(width=65 * sc + 0.4, height=1.1, corner_radius=0.35, color=TERRA, stroke_width=6).move_to([ex(32.5), by, 0])
        strong = T("strongest on one card", 36)
        strong.move_to([ex(65) + 0.2 - strong.width / 2, 2.62, 0])

        cy = -1.75
        lx, rx = -3.0, 3.0
        cards = [paper(lx, cy, w=4.4, h=2.7), paper(rx, cy, w=4.4, h=2.7)]
        blks = [pC_blk(0, 0, 1.1, 0.8, BAR2, 4).move_to([x - 1.45, cy + 0.2, 0]) for x in (lx, rx)]
        mlabs = [T("model", 32).move_to([x - 1.45, cy - 0.55, 0]) for x in (lx, rx)]
        stamp = pC_stamp("tools", lx + 0.5, cy + 0.85)
        gear = pC_gear(lx + 0.3, cy - 0.35, 0.58)
        ck = check(lx + 1.55, cy - 0.35, s=0.3, color=TERRA, w=12)
        ghost = DashedVMobject(RoundedRectangle(width=1.75, height=0.7, corner_radius=0.35, color=BAR1, stroke_width=4), num_dashes=22).move_to([rx + 0.5, cy + 0.85, 0])
        lines = [scribble(rx - 0.55, cy + 0.15 - 0.4 * i, 3.2 if i != 2 else 2.4, amp=0.09, sw=5) for i in range(3)]
        xm = x_mark(rx + 1.75, cy + 0.85, r=0.26, w=9)

        self.play(Create(rl), FadeIn(rt), FadeIn(rn), FadeIn(gb), run_time=0.6)
        # "the 120 billion GPT-OSS, about 65 gigabytes"
        hear(self, "120 billion", lead=0.3)
        self.play(FadeIn(lab), run_time=0.3)
        hear(self, "about 65", lead=0.3)
        self.play(GrowFromEdge(bar, LEFT), run_time=1.0)
        self.play(FadeIn(n65), run_time=0.2)
        # "is the strongest of these that fits on one card": the ring
        hear(self, "strongest", lead=0.4)
        self.play(Create(ring), FadeIn(strong), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(ring), run_time=0.3)
        # "check its page for the tools label": two model cards
        at(self, 8.05)
        self.play(FadeIn(cards[0]), FadeIn(cards[1]), FadeIn(blks[0]), FadeIn(blks[1]), FadeIn(mlabs[0]), FadeIn(mlabs[1]), run_time=0.4)
        hear(self, "tool's label", lead=0.35)
        self.play(GrowFromCenter(stamp), run_time=0.3)
        self.play(FadeIn(gear), run_time=0.2)
        self.play(Rotate(gear, angle=PI / 2, about_point=[gear.cx, gear.cy, 0]), run_time=0.6, rate_func=smooth)
        self.play(Create(ck), run_time=0.3)
        # "a model without tool support": the empty slot on the other card
        hear(self, "without tool support", lead=0.1)
        self.play(Create(ghost), run_time=0.4)
        # "prints tool calls as plain text instead of running them": the call spills across the card, then the cross
        hear(self, "calls as plain", lead=0.5)
        for ln in lines:
            self.play(Create(ln), run_time=0.42, rate_func=linear)
        hear(self, "instead of running", lead=0.2)
        self.play(Create(xm), run_time=0.3)
        done(self)


def pC_caution(x, y, r=0.3):
    """A caution mark: a kraft triangle, an ink outline, a bar and a dot."""
    tri = Polygon([x, y + r, 0], [x - r * 0.95, y - r * 0.6, 0], [x + r * 0.95, y - r * 0.6, 0],
                  fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
    bar = Line([x, y + r * 0.35, 0], [x, y - r * 0.1, 0], color=INK, stroke_width=5)
    dot = Dot([x, y - r * 0.38, 0], radius=0.045, color=INK)
    return VGroup(tri, bar, dot)


class B43_OneGpuPerJob(Scene):
    """A GPU-partition rack with five typed slots; the request picks h200 (about 140 GB), every model slots in with room left;
    the older v100 and t4 slots get a caution mark."""
    def construct(self):
        fx, fy, fw, fh = -1.25, 0.29, 4.6, 4.1
        tw, th = 4.0, 0.58
        rows = [("v100-sxm2", 1.85), ("v100-pcie", 1.07), ("t4", 0.29), ("a100", -0.49), ("h200", -1.27)]
        frame = Rectangle(width=fw, height=fh, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([fx, fy, 0])
        trays = VGroup(*[Rectangle(width=tw, height=th, fill_color=GHOST, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([fx, y, 0]) for _, y in rows])
        names = VGroup(*[M(n, 32).move_to([-3.85, y, 0]) for n, y in rows])
        for m in names:
            m.shift(RIGHT * (-3.85 - m.get_right()[0]))
        gp = T("gpu partition", 40)
        gp.move_to([-3.55 + gp.width / 2, 2.8, 0])
        yh = -1.27
        req = chip("--gres=gpu:h200:1", 3.85, yh, w=4.55, mono=True, size=34)
        ring = RoundedRectangle(width=tw + 0.2, height=th + 0.2, corner_radius=0.12, color=TERRA, stroke_width=6).move_to([fx, yh, 0])
        tag = T("about 140 GB", 34).move_to([3.85, -2.1, 0])
        left = fx - tw / 2
        per = tw / 140.0
        sizes = [14, 19, 23, 65]
        mods = [Rectangle(width=g * per, height=0.44, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([left + 0.06 + g * per / 2, yh, 0]) for g in sizes]
        mlab = T("model", 34).move_to([-2.45, -2.2, 0])
        room_x0 = left + 0.06 + 65 * per + 0.2
        room_w = fx + tw / 2 - 0.06 - room_x0
        room = DashedVMobject(Rectangle(width=room_w, height=0.44, color=BAR1, stroke_width=4), num_dashes=24).move_to([room_x0 + room_w / 2, yh, 0])
        rlab = T("context", 34).move_to([room_x0 + room_w / 2, -2.2, 0])
        cautions = [pC_caution(1.45, y) for y in (1.85, 1.07, 0.29)]
        clab = T("may fall back to CPU", 34)
        clab.move_to([1.95 + clab.width / 2, 1.07, 0])
        lg_page = paper(5.15, 2.3, w=1.2, h=1.3)
        lg_lines = scribbles_on(lg_page, n=3, inset=0.22, gap=0.3)
        lg_lab = T("log", 36).move_to([3.7, 2.3, 0])
        pulse = RoundedRectangle(width=4.55 + 0.3, height=1.1, corner_radius=0.45, color=TERRA, stroke_width=6).move_to([3.85, yh, 0])

        # "The GPU partition": the rack with its five typed slots
        self.play(FadeIn(gp), FadeIn(frame), FadeIn(trays), FadeIn(names), run_time=0.6)
        # "gives one GPU per job": the request chip
        hear(self, "per job", lead=0.5)
        self.play(FadeIn(req), run_time=0.4)
        # "so stay inside one card": the request picks the h200 slot
        hear(self, "inside one card", lead=0.3)
        self.play(Create(ring), run_time=0.45)
        self.wait(0.4)
        self.play(FadeOut(ring), run_time=0.3)
        # "an H200 has about 140 GB"
        hear(self, "about 140", lead=0.25)
        self.play(FadeIn(tag), run_time=0.3)
        # "every model on that list fits": each block slots in with room left
        hear(self, "every model", lead=0.15)
        self.play(GrowFromEdge(mods[0], LEFT), FadeIn(mlab), run_time=0.3)
        hear(self, "on that list", lead=0.1)
        self.play(FadeOut(mods[0]), run_time=0.1)
        self.play(GrowFromEdge(mods[1], LEFT), run_time=0.3)
        self.play(FadeOut(mods[1]), run_time=0.1)
        self.play(GrowFromEdge(mods[2], LEFT), run_time=0.3)
        # "with room for a large context": the biggest model, then the room it leaves
        hear(self, "room", lead=0.0)
        self.play(FadeOut(mods[2]), run_time=0.1)
        self.play(GrowFromEdge(mods[3], LEFT), run_time=0.35)
        hear(self, "large context", lead=0.0)
        self.play(Create(room), FadeIn(rlab), run_time=0.5)
        # "Older cards like V100 and T4 may fall back to the processor"
        hear(self, "V100", lead=0.25)
        self.play(GrowFromCenter(cautions[0]), GrowFromCenter(cautions[1]), run_time=0.35)
        hear(self, "T4", lead=0.2)
        self.play(GrowFromCenter(cautions[2]), run_time=0.3)
        hear(self, "may fall back", lead=0.15)
        self.play(FadeIn(clab), run_time=0.4)
        # "so check the log": a log page
        hear(self, "check the log", lead=0.2)
        self.play(FadeIn(lg_page), FadeIn(lg_lines), FadeIn(lg_lab), run_time=0.4)
        # "and ask for a newer type": the request chip is ringed again
        hear(self, "ask for a newer", lead=0.2)
        self.play(Create(pulse), run_time=0.5)
        done(self)


class B44_ContextKnobs(Scene):
    """Two cache blocks on a memory ruler (65,536 and a taller 131,072); the q8_0 knob turns and both blocks halve."""
    def construct(self):
        base = -2.6
        rx = -5.5
        ruler = Line([rx, base, 0], [rx, 2.5, 0], color=INK, stroke_width=6)
        ticks = VGroup(*[Line([rx, base + 0.52 * i, 0], [rx + 0.28, base + 0.52 * i, 0], color=INK, stroke_width=6) for i in range(1, 10)])
        mem = T("memory", 34).move_to([-6.1 + 0.65, 2.85, 0])
        ground = Line([rx, base, 0], [0.3, base, 0], color=INK, stroke_width=6)
        b1 = pC_blk(-3.9, base, 1.6, 1.6, BAR2, 4)
        b2 = pC_blk(-1.7, base, 1.6, 3.2, BAR2, 4)
        n1 = T("65,536", 38).move_to([-3.9, -3.0, 0])
        n2 = T("131,072", 38).move_to([-1.7, -3.0, 0])
        floor = chip("floor", -3.9, -0.45, size=34)
        h200 = chip("h200", -1.7, 1.2, mono=True, size=34)
        kb = Circle(radius=0.95, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([3.0, 1.55, 0])
        kp = Line([3.0, 1.55, 0], [3.0, 1.55 + 0.6, 0], color=INK, stroke_width=8)
        kd = Dot([3.0, 1.55 + 0.6, 0], radius=0.14, color=TERRA)
        knob = VGroup(kb, kp, kd)
        klab = M("OLLAMA_KV_CACHE_TYPE=q8_0", 32).move_to([3.0, 0.2, 0])
        g1 = DashedVMobject(Rectangle(width=1.6, height=1.6, color=BAR1, stroke_width=5), num_dashes=36).move_to([-3.9, base + 0.8, 0])
        g2 = DashedVMobject(Rectangle(width=1.6, height=3.2, color=BAR1, stroke_width=5), num_dashes=60).move_to([-1.7, base + 1.6, 0])
        s1 = pC_blk(-3.9, base, 1.6, 0.8, BAR2, 4)
        s2 = pC_blk(-1.7, base, 1.6, 1.6, BAR2, 4)
        cost = chip("small quality cost", 3.0, -1.35, size=34)

        self.play(Create(ruler), FadeIn(ticks), Create(ground), FadeIn(mem), run_time=0.6)
        # "sixty-five thousand is the floor for coding agents"
        hear(self, "65", lead=0.2)
        self.play(GrowFromEdge(b1, DOWN), run_time=0.7)
        self.play(FadeIn(n1), run_time=0.2)
        hear(self, "floor", lead=0.2)
        self.play(FadeIn(floor), run_time=0.3)
        # "on an H200 you can raise it": the taller block
        hear(self, "H200", lead=0.15)
        self.play(FadeIn(h200), run_time=0.3)
        hear(self, "raise it", lead=0.45)
        self.play(GrowFromEdge(b2, DOWN), run_time=0.8)
        self.play(FadeIn(n2), run_time=0.2)
        # "if memory is tight": the knob and its setting
        hear(self, "If memory", lead=0.1)
        self.play(FadeIn(knob), FadeIn(klab), run_time=0.4)
        # "storing the cache at 8 bits": the knob turns
        hear(self, "8 bits", lead=0.3)
        self.play(Rotate(knob, angle=-PI / 2, about_point=[3.0, 1.55, 0]), run_time=0.5, rate_func=smooth)
        # "roughly halves its size": both blocks halve, the old height stays as a dashed outline
        hear(self, "halves", lead=0.1)
        self.play(Create(g1), Create(g2), Transform(b1, s1), Transform(b2, s2), run_time=0.7)
        # "at a small cost in quality"
        hear(self, "small cost", lead=0.15)
        self.play(GrowFromCenter(cost), run_time=0.35)
        done(self)


# ═════════════════════════════ PART D — B53 B54 B60 B64 B72 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pD_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


# ── placement helpers: the iso origin is the left-back corner, so centre a block with these ──
def pD_rack(cx, cy, s=0.8):
    """explorer_rack centred on (cx, cy): returns (stack, lights). Its 2 slabs are 0.88 tall, 1.3 x 1.3."""
    iso = Iso(cx, cy - 1.09 * s, s)
    return explorer_rack(iso)


def pD_box(cx, cy, w=1.4, d=1.4, h=0.9, s=0.8):
    """A plain kraft block centred on (cx, cy)."""
    ox = cx - (w - d) / 2 * C30 * s
    oy = cy - ((w + d) / 4 + h / 2) * s
    return Iso(ox, oy, s).box(0, 0, 0, w, d, h)


def pD_job(cx, cy, s=0.85, b=0.8):
    """job_box centred on (cx, cy): a kraft box with one terracotta tape."""
    iso = Iso(cx, cy - (b * 2 / 4 + b * 0.8 / 2) * s, s)
    return job_box(iso, 0, 0, 0, s=b)


def pD_stopwatch(x, y, r=0.6):
    face = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    knob = Rectangle(width=0.26, height=0.16, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + r + 0.12, 0])
    hand = Line([x, y, 0], [x, y + r * 0.7, 0], color=INK, stroke_width=10)
    hub = Dot([x, y, 0], radius=0.1, color=INK)
    g = VGroup(knob, face, hand, hub)
    g.hand, g.cx, g.cy = hand, x, y
    return g


def pD_laptop(x, y, w=1.8):
    """Your laptop: a flat rounded slab with a smaller screen rectangle (grey outline, so it does not fuse with the slab)."""
    slab = RoundedRectangle(corner_radius=0.14, width=w, height=1.25, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    screen = Rectangle(width=w * 0.7, height=0.75, fill_color=BAR2, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([x, y + 0.1, 0])
    return VGroup(slab, screen)


def pD_gate(x, y):
    """The caddy gate: two kraft posts, a top bar and a closed panel across the lane. `.panel` opens (fades) for a valid token."""
    pl = Rectangle(width=0.3, height=2.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x - 0.8, y, 0])
    pr = Rectangle(width=0.3, height=2.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x + 0.8, y, 0])
    bar = Rectangle(width=1.9, height=0.3, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y + 1.0, 0])
    panel = Rectangle(width=1.3, height=1.9, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y - 0.1, 0])
    g = VGroup(pl, pr, panel, bar)
    g.panel = panel
    return g


def pD_gate_lock(x, y, s=0.5):
    """The padlock hangs on the gate's left post (so it stays put when the panel opens)."""
    lk = padlock(x - 0.8, y + 0.45, s=s)
    lk.set_z_index(6)
    return lk


def pD_packet(x, y, token=False):
    """A request packet: a small kraft envelope with one terracotta seal; with `token`, a key lies on top of it."""
    body = Rectangle(width=1.0, height=0.6, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    seal = Dot([x, y, 0], radius=0.1, color=TERRA)
    parts = [body, seal]
    if token:
        s = 0.36
        parts.append(key_obj(x - 0.85 * s, y + 0.62, s=s))
    return VGroup(*parts)


def pD_caution(x, y):
    """A caution mark: an ink-outlined white triangle with an exclamation mark."""
    tri = Polygon([x, y + 0.5, 0], [x - 0.55, y - 0.42, 0], [x + 0.55, y - 0.42, 0],
                  fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
    bang = T("!", 44, bold=True).move_to([x, y - 0.06, 0])
    return VGroup(tri, bang)


def pD_ring(cx, cy, w, h, color=TERRA):
    return RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=color, stroke_width=7, fill_opacity=0).move_to([cx, cy, 0])


def pD_road(x0, x1, y):
    """A road: a band with deep-kraft edges and pale ghost centre dashes (the kit's belt rule)."""
    band = Rectangle(width=x1 - x0, height=0.5, fill_color=BAR2, fill_opacity=1, stroke_color=KRAFT_DEEP, stroke_width=4).move_to([(x0 + x1) / 2, y, 0])
    dash = DashedLine([x0 + 0.15, y, 0], [x1 - 0.15, y, 0], color=GHOST, stroke_width=5, dash_length=0.3)
    g = VGroup(band, dash)
    g.band, g.dash = band, dash
    return g


def pD_cable(a, b, w=6):
    return Line(a, b, color=KRAFT_DEEP, stroke_width=w)


class B53_UnsupportedRoute(Scene):
    """A road drawn from Claude to a local model carries a sign 'unsupported route'; web search and prompt caching get crossed."""
    def construct(self):
        claude = logo_chip("claude", -4.6, 2.05, h=1.55)
        mod = pD_box(4.6, 1.9, s=1.0)
        mlab = T("local model", 40).move_to([5.0, 0.35, 0])
        caps = [("edit files", 0.5), ("run tools", -0.5), ("web search", -1.5), ("prompt caching", -2.5)]
        chips = [chip(s, -3.9, y, w=4.2, size=40) for s, y in caps]
        ticks = [check(-1.4, y, s=0.26, w=10) for y in (0.5, -0.5)]
        crosses = [x_mark(-1.3, y, r=0.3, w=9) for y in (-1.5, -2.5)]
        road = pD_road(-3.2, 3.2, 2.05)
        # the sign hangs below the road on a deep-kraft pole
        board = RoundedRectangle(corner_radius=0.3, width=4.0, height=1.45, fill_color="#FFFFFF", fill_opacity=1, stroke_width=0).move_to([1.15, 0.5, 0])
        shadow = RoundedRectangle(corner_radius=0.3, width=4.0, height=1.45, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([1.23, 0.42, 0])
        pole = pD_cable([1.15, 1.22, 0], [1.15, 1.8, 0], w=8)
        sl1 = T("documented settings", 34).move_to([1.15, 0.84, 0])
        sl2 = T("unsupported route", 34).move_to([1.15, 0.18, 0])
        # web search runs on Anthropic's backend: the label carries the Anthropic logo
        t1 = T("runs on", 36).move_to([-0.1, -1.5, 0])
        alogo = logo_chip("anthropic", 1.35, -1.5, h=0.95)
        t2 = T("backend", 36).move_to([3.0, -1.5, 0])
        tag = Group(t1, alogo, t2)

        self.play(FadeIn(claude), FadeIn(mod), FadeIn(mlab), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.2), run_time=0.9)
        # "pointing Claude Code at non-Claude models": the road is drawn from Claude to the local model
        hear(self, "pointing", lead=0.15)
        self.play(GrowFromEdge(road.band, LEFT), Create(road.dash), run_time=1.4, rate_func=smooth)
        # "this works": edit files and run tools tick
        hear(self, "this works", lead=0.1)
        self.play(*[Create(t) for t in ticks], run_time=0.4)
        # "documented settings": the sign goes up; "unsupported route": its second line lands
        hear(self, "documented settings", lead=0.2)
        self.play(FadeIn(shadow), FadeIn(board), Create(pole), FadeIn(sl1), run_time=0.5)
        hear(self, "unsupported route", lead=0.1)
        self.play(FadeIn(sl2), run_time=0.4)
        # after the midpoint: "web search runs on Anthropic's own backend"
        hear(self, "web search", lead=0.3)
        self.play(FadeIn(tag), run_time=0.5)
        hear(self, "not fully support", lead=0.2)
        self.play(Create(crosses[0]), run_time=0.35)
        hear(self, "is not supported", lead=0.1)
        self.play(Create(crosses[1]), run_time=0.4)
        done(self)


class B54_ContextGrowsThenExit(Scene):
    """Blocks stack into the context bar as the stopwatch slows; one tool server is crossed and the bar drops; then two exits leave and the rack dims."""
    def construct(self):
        claude = logo_chip("claude", -4.9, 0.2, h=1.5)
        watch = pD_stopwatch(-4.9, 2.15, r=0.75)
        tank = Rectangle(width=1.3, height=5.0, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-2.4, -0.25, 0])
        ctx = T("context", 40).move_to([-2.4, 2.65, 0])
        blocks = [Rectangle(width=1.06, height=0.52, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3)
                  .move_to([-2.4, -2.35 + 0.64 * i, 0]) for i in range(7)]
        tdef = T("tool definition", 36).move_to([0.0, -1.7, 0])
        cache = chip("cache", 1.4, 2.5, w=2.4, size=38)
        cache_x = x_mark(3.05, 2.5, r=0.3, w=9)
        srv = [chip("tool server", 1.5, 1.0, w=3.6, size=38), chip("tool server", 1.5, -0.2, w=3.6, size=38)]
        srv_x = x_mark(3.95, -0.2, r=0.3, w=9)
        ring = pD_ring(-2.4, -0.25, 1.7, 5.4)
        # the exit chain: Claude chip -> exit -> the job -> exit -> GPU node
        jobbox = pD_job(0.0, 0.4, s=1.1)
        jlab = T("the job", 40).move_to([0.0, -1.15, 0])
        st, lt = pD_rack(5.0, 0.4, s=1.0)
        rack = VGroup(st, lt)
        rlab = T("GPU node", 40).move_to([5.0, -1.2, 0])
        a1 = Arrow([-3.65, 0.2, 0], [-1.35, 0.2, 0], color=INK, stroke_width=9, buff=0, max_tip_length_to_length_ratio=0.25)
        e1 = M("exit", 38).move_to([-2.5, 0.85, 0])
        a2 = Arrow([1.25, 0.4, 0], [3.5, 0.4, 0], color=INK, stroke_width=9, buff=0, max_tip_length_to_length_ratio=0.28)
        e2 = M("exit", 38).move_to([2.4, 1.05, 0])
        ring1 = pD_ring(-4.9, 0.2, 2.5, 1.9)
        ring2 = pD_ring(0.0, 0.1, 2.3, 2.5)

        self.play(FadeIn(claude), FadeIn(watch), FadeIn(tank), FadeIn(ctx), run_time=0.4)
        # turn 1 ("long sessions"): two blocks stack, the stopwatch is quick
        hear(self, "long sessions", lead=0.15)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.4) for b in blocks[:2]], lag_ratio=0.4),
                  Rotate(watch.hand, angle=-2 * PI, about_point=[watch.cx, watch.cy, 0], rate_func=linear), run_time=0.7)
        # turn 2 ("as the context grows"): more blocks, the stopwatch slows
        hear(self, "as the context grows", lead=0.2)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.4) for b in blocks[2:4]], lag_ratio=0.4),
                  Rotate(watch.hand, angle=-PI, about_point=[watch.cx, watch.cy, 0], rate_func=linear), run_time=1.0)
        # turn 3 ("because nothing is cached"): more again, slower still; the cache is crossed
        hear(self, "because nothing", lead=0.1)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.4) for b in blocks[4:6]], lag_ratio=0.4),
                  Rotate(watch.hand, angle=-PI / 2, about_point=[watch.cx, watch.cy, 0], rate_func=linear), run_time=1.0)
        self.play(FadeIn(cache), Create(cache_x), run_time=0.45)
        # "Keep tool servers few": two tool servers; one is crossed and its blocks leave the bar
        hear(self, "Keep tool servers", lead=0.1)
        self.play(*[FadeIn(c) for c in srv], run_time=0.5)
        hear(self, "few", lead=0.2)
        self.play(Create(srv_x), *[FadeOut(b, shift=UP * 0.3) for b in blocks[3:6]], run_time=0.5)
        # "every definition uses context"
        hear(self, "every definition", lead=0.25)
        self.play(FadeIn(tdef), run_time=0.4)
        at(self, 6.75)
        self.add(ring)
        self.play(ring.animate.scale(1.1).set_opacity(0), run_time=0.55)
        # "And when you finish": the bar and servers go; the job and the GPU node arrive
        hear(self, "And when you finish", lead=0.4)
        gone = [watch, tank, ctx, tdef, cache, cache_x, srv[0], srv[1], srv_x, blocks[0], blocks[1], blocks[2], blocks[6]]
        self.play(*[FadeOut(m) for m in gone], run_time=0.35)
        self.play(FadeIn(jobbox), FadeIn(jlab), FadeIn(rack), FadeIn(rlab), run_time=0.45)
        # "exit twice": two exit arrows, in order
        hear(self, "exit twice", lead=0.1)
        self.play(Create(a1), FadeIn(e1), run_time=0.4)
        hear(self, "twice", lead=0.1)
        self.play(Create(a2), FadeIn(e2), run_time=0.4)
        # "Claude Code", then "the job"
        hear(self, "clod code", lead=0.0)
        self.add(ring1)
        self.play(ring1.animate.scale(1.18).set_opacity(0), run_time=0.6)
        hear(self, "then the job", lead=0.05)
        self.add(ring2)
        self.play(ring2.animate.scale(1.18).set_opacity(0), run_time=0.6)
        # "returns the GPU": the node dims and its lights go out
        hear(self, "returns the GPU", lead=0.2)
        self.play(rack.animate.set_opacity(0.3), run_time=0.8)
        done(self)


class B60_LockInFront(Scene):
    """The laptop reaches the node through the login node; Ollama stays on localhost; Caddy's locked gate rejects a packet with no token and opens for one with the key."""
    def construct(self):
        title = pD_act_title("VI · Pattern B, From Your Laptop")
        lane = -0.35
        gy = 0.2
        laptop = pD_laptop(-5.3, -0.1)
        llab = T("laptop", 34).move_to([-5.3, -1.6, 0])
        lst, llt = pD_rack(-2.95, -0.05, s=0.8)
        login = VGroup(lst, llt)
        nlab = T("login node", 34).move_to([-2.95, -1.6, 0])
        road1 = pD_road(-4.35, -3.8, lane)
        road2 = pD_road(-2.05, 2.05, lane)
        clab = T("cluster network", 34).move_to([0.1, -1.6, 0])
        gst, glt = pD_rack(5.2, -0.05, s=0.85)
        grack = VGroup(gst, glt)
        glab = T("GPU node", 38).move_to([4.1, -1.6, 0])
        olla = logo_chip("ollama", 2.9, -0.1, h=1.3)
        local = M("localhost", 34).move_to([2.9, 0.95, 0])
        gate = pD_gate(0.0, gy)
        lock = pD_gate_lock(0.0, gy)
        caddy = logo_chip("caddy", 0.0, 1.95, h=1.1)
        pkA = pD_packet(-4.55, lane - 0.05, token=True)
        pkB = pD_packet(-4.55, lane - 0.05, token=False)
        tag401 = chip("401", -2.0, 1.25, w=1.3, mono=True, size=36)

        self.play(FadeIn(title), run_time=0.4)
        # "needs a lock": the padlock appears
        hear(self, "needs a lock", lead=0.1)
        self.play(GrowFromCenter(lock), run_time=0.45)
        # "The laptop reaches the node through the login node"
        hear(self, "The laptop", lead=0.1)
        self.play(FadeIn(laptop), FadeIn(llab), run_time=0.4)
        hear(self, "through the login node", lead=0.3)
        self.play(FadeIn(login), FadeIn(nlab), Create(road1.dash), GrowFromEdge(road1.band, LEFT), run_time=0.5)
        # "so something has to listen on the node's cluster network"
        hear(self, "so something has to listen", lead=0.1)
        self.play(GrowFromEdge(road2.band, LEFT), Create(road2.dash), run_time=0.9, rate_func=smooth)
        hear(self, "the node's cluster", lead=0.15)
        self.play(FadeIn(grack), FadeIn(glab), FadeIn(clab), run_time=0.5)
        # "Ollama stays on localhost"
        hear(self, "stays on", lead=0.5)
        self.play(FadeIn(olla), run_time=0.4)
        at(self, 7.75)
        self.play(FadeIn(local), run_time=0.35)
        # "a small web server, Caddy, listens instead": the gate goes up in front of Ollama
        hear(self, "a small web server", lead=0.1)
        self.play(FadeIn(gate), run_time=0.5)
        hear(self, "caddy", lead=0.2)
        self.play(FadeIn(caddy), run_time=0.4)
        # "listens instead": the packet with the token comes up, the lock opens, the gate opens, the packet goes through
        hear(self, "listens instead", lead=0.0)
        self.play(FadeIn(pkA), run_time=0.15)
        self.play(pkA.animate.shift(RIGHT * 2.9), run_time=0.75, rate_func=linear)
        self.play(unlock_anim(lock, 0.35), run_time=0.35)
        self.play(gate.panel.animate.set_opacity(0.1), run_time=0.25)
        # "rejects every request": a second packet, no token, follows; the first goes through to Ollama
        self.add(pkB)
        self.play(pkA.animate.shift(RIGHT * 3.1), pkB.animate.shift(RIGHT * 2.9), run_time=0.8, rate_func=linear)
        # the gate closes again and the lock turns back
        self.play(gate.panel.animate.set_opacity(1.0), lock.shackle.animate.shift(DOWN * 0.3 * lock.s), lock.light.animate.set_color(GHOST), run_time=0.35)
        # "does not carry": the 401 tag lands and the packet is thrown out
        self.add(tag401)
        tag401.shift(UP * 0.6)
        self.play(tag401.animate.shift(DOWN * 0.6), FadeOut(pkB, shift=DOWN * 0.5), run_time=0.4, rate_func=smooth)
        # "your bearer token": a ring pulses round the packet that carried it
        hear(self, "your bearer token", lead=0.2)
        ring = pD_ring(1.45, lane + 0.2, 1.6, 1.6)
        self.add(ring)
        self.play(ring.animate.scale(1.2).set_opacity(0), run_time=0.6)
        done(self)


class B64_TwoRisks(Scene):
    """Other users on the node reach the random port beside the gate; your token sits in plain text on the laptop; scancel stamps and the node dims."""
    def construct(self):
        gy = 0.2
        gate = pD_gate(0.0, gy)
        lock = pD_gate_lock(0.0, gy)
        caddy = logo_chip("caddy", 0.0, 1.95, h=1.1)
        olla = logo_chip("ollama", 2.9, -0.1, h=1.3)
        gst, glt = pD_rack(5.2, -0.05, s=0.85)
        grack = VGroup(gst, glt)
        glab = T("GPU node", 38).move_to([4.1, -1.6, 0])
        node = Group(gate, lock, caddy, olla, grack)
        # the rest of the cluster: grey dots stopped by the gate
        rest = VGroup(*[Dot([x, y, 0], radius=0.16, color=BAR1) for x, y in ((-3.9, 1.1), (-3.5, 0.55), (-3.9, 0.0))])
        rlab = T("rest of cluster", 34).move_to([-3.5, 1.95, 0])
        # the random port: a small socket on the Ollama block
        port = Rectangle(width=0.4, height=0.4, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([2.4, 0.78, 0])
        plab = T("random port", 34).move_to([2.7, 1.7, 0])
        # other users: terracotta dots sitting on the rack's top face, then reaching the port
        users = VGroup(*[Dot([5.2 + dx, 0.38 + dy, 0], radius=0.14, color=TERRA) for dx, dy in ((-0.4, 0.0), (0.0, 0.12), (0.4, 0.0))])
        ulab = T("other users", 34).move_to([5.25, 1.35, 0])
        caut = pD_caution(1.35, 2.75)
        clab = T("obscurity, not security", 34).move_to([4.15, 2.75, 0])
        # the token on your laptop
        laptop = pD_laptop(-5.2, -1.0)
        llab = T("laptop", 34).move_to([-5.2, -2.0, 0])
        page = paper(-3.5, -0.95, w=1.0, h=1.3)
        pl = scribbles_on(page, n=3, inset=0.2, gap=0.32)
        tlab = M("token", 34).move_to([-3.5, 0.05, 0])
        open_lock = padlock(-2.05, -0.95, s=0.7)
        open_lock.shackle.shift(UP * 0.3 * open_lock.s)
        open_lock.light.set_color(TERRA)
        plain = T("plain text", 34).move_to([-2.8, -2.0, 0])
        cmd = plaque("scancel --name=ollama-serve", 0.4, -2.8, w=9.8, h=0.9, size=32)

        self.play(FadeIn(node), FadeIn(glab), run_time=0.5)
        # "The proxy blocks the rest of the cluster": grey dots come up and the gate stops them
        hear(self, "proxy blocks", lead=0.2)
        self.play(FadeIn(rest), FadeIn(rlab), run_time=0.3)
        self.play(rest.animate.shift(RIGHT * 2.1), run_time=0.9, rate_func=smooth)
        # "Ollama's own random port": a socket beside the gate
        hear(self, "random port", lead=0.3)
        self.play(FadeIn(port), FadeIn(plab), run_time=0.4)
        # "other users on the same node": dots on the rack reach the port, past the gate
        hear(self, "other users", lead=0.3)
        self.play(FadeIn(users), FadeIn(ulab), run_time=0.3)
        self.play(users.animate.move_to([2.75, 1.0, 0]), run_time=1.2, rate_func=smooth)
        # after the midpoint: "A random port is obscurity, not security"
        at(self, 7.75)
        self.play(FadeIn(caut), FadeIn(clab), run_time=0.4)
        # "your token sits in plain text on your laptop"
        hear(self, "your token", lead=0.3)
        self.play(FadeIn(laptop), FadeIn(llab), FadeIn(page), FadeIn(pl), FadeIn(tlab), run_time=0.5)
        hear(self, "plain text", lead=0.15)
        self.play(FadeIn(open_lock), FadeIn(plain), run_time=0.4)
        # "cancel the job": the command stamps, the node dims
        hear(self, "cancel the job", lead=0.4)
        self.play(FadeIn(cmd, scale=1.25), run_time=0.35)
        self.play(node.animate.fade(0.7), run_time=0.8)
        done(self)


class B72_LaunchDefaults(Scene):
    """ollama launch wires the tools up at the default port; here the port is random and locked so it breaks; OpenAI-compatible routes take over."""
    def construct(self):
        ys = (1.7, 0.2, -1.3)
        tx = -2.2
        codex = logo_chip("codex", tx, ys[0], h=1.2)
        opencode = logo_chip("opencode", tx, ys[1], h=1.2)
        dshadow = pill(tx + 0.08, ys[2] - 0.08, 1.62, h=1.2, fill=BOX_L)
        dbody = pill(tx, ys[2], 1.62, h=1.2)
        dlab = M("droid", 34).move_to([tx, ys[2], 0])
        droid = VGroup(dshadow, dbody, dlab)
        # the ollama launch command box (two mono lines)
        lshadow = Rectangle(width=2.4, height=1.6, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([-4.9, 0.1, 0])
        lcard = Rectangle(width=2.4, height=1.6, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([-5.0, 0.2, 0])
        la = M("ollama", 34).move_to([-5.0, 0.55, 0])
        lb = M("launch", 34).move_to([-5.0, -0.15, 0])
        launch = VGroup(lshadow, lcard, la, lb)
        fan = VGroup(*[pD_cable([-3.8, 0.2, 0], [tx - 0.85, y, 0]) for y in ys])
        # the model block with its plain slot
        cx, cy, w, d, h, s = 3.0, 0.25, 1.5, 1.5, 1.5, 1.0
        ox = cx - (w - d) / 2 * C30 * s
        oy = cy - ((w + d) / 4 + h / 2) * s
        iso = Iso(ox, oy, s)
        mod = iso.box(0, 0, 0, w, d, h)
        slot1 = iso.quad([(0, 0.3, 0.95), (0, 1.2, 0.95), (0, 1.2, 1.3), (0, 0.3, 1.3)], GHOST, stroke=INK, sw=3)
        s1 = iso.p(0, 0.75, 1.12)
        mlab = T("model", 40).move_to([5.4, 0.25, 0])
        route1 = VGroup(*[pD_cable([tx + 0.85, y, 0], [s1[0] - 0.95, s1[1], 0]) for y in ys])
        loc = M("localhost:11434", 34).move_to([2.9, 2.5, 0])
        ok = check(0.15, 2.5, s=0.24, w=10)
        rnd = T("random port", 38).move_to([2.9, 2.5, 0])
        lock = padlock(s1[0] - 0.55, s1[1] + 0.1, s=0.6)
        lock.set_z_index(6)
        cross1 = x_mark(0.2, 0.55, r=0.4, w=10)
        # the second route: OpenAI-compatible socket, three keyed cables
        slot2 = iso.quad([(0, 0.3, 0.2), (0, 1.2, 0.2), (0, 1.2, 0.55), (0, 0.3, 0.55)], GHOST, stroke=INK, sw=3)
        s2 = iso.p(0, 0.75, 0.37)
        oai = logo_chip("openai", 2.0, -2.3, h=0.95)
        comp = T("compatible", 38).move_to([3.75, -2.3, 0])
        route2 = VGroup(*[pD_cable([tx + 0.85, y, 0], [s2[0] - 0.1, s2[1], 0], w=6) for y in ys])
        keys = []
        for y in ys:
            a = np.array([tx + 0.85, y, 0.0]); b = np.array([s2[0] - 0.1, s2[1], 0.0])
            m = a + (b - a) * 0.5
            keys.append(key_obj(m[0] - 0.85 * 0.36, m[1], s=0.36))
        # the tools' own instructions
        pages = [paper(-4.4, y, w=1.1, h=1.0) for y in ys]
        pls = [scribbles_on(p, n=2, inset=0.2, gap=0.3) for p in pages]

        # "Codex, OpenCode and Droid": the three tools arrive on their names
        self.play(FadeIn(codex), run_time=0.35)
        hear(self, "OpenCode", lead=0.05)
        self.play(FadeIn(opencode), run_time=0.35)
        hear(self, "Droid", lead=0.1)
        self.play(FadeIn(droid), run_time=0.3)
        # "the ollama launch command": the command box, then its lines to the three tools
        hear(self, "Olama launch", lead=0.15)
        self.play(FadeIn(launch), run_time=0.4)
        hear(self, "command", lead=0.1)
        self.play(*[Create(l) for l in fan], run_time=0.5)
        # "only when Ollama is on the same machine at its default port": the model block with the plain slot
        hear(self, "same machine", lead=0.2)
        self.play(FadeIn(mod), FadeIn(mlab), run_time=0.5)
        hear(self, "default port", lead=0.2)
        self.play(FadeIn(slot1), *[Create(l) for l in route1], run_time=0.5)
        self.play(FadeIn(loc), Create(ok), run_time=0.35)
        # "Here the port is random": the slot's address changes to a random port
        hear(self, "Here", lead=0.05)
        self.play(FadeOut(loc), FadeOut(ok), FadeIn(rnd), run_time=0.45)
        # after the midpoint: "behind a token": a padlock sits on the slot
        at(self, 8.56)
        self.play(GrowFromCenter(lock), run_time=0.4)
        # "in Pattern B": the cables to the slot break
        hear(self, "Pattern B", lead=0.1)
        self.play(Create(cross1), route1.animate.set_opacity(0.3), run_time=0.4)
        # "set them up as OpenAI-compatible providers": the broken cables go, a second socket, three keyed cables
        hear(self, "set them up", lead=0.0)
        self.play(FadeOut(cross1), FadeOut(route1), FadeIn(slot2), FadeIn(oai), FadeIn(comp), run_time=0.4)
        hear(self, "OpenAI", lead=0.1)
        self.play(LaggedStart(*[AnimationGroup(Create(r), FadeIn(k)) for r, k in zip(route2, keys)], lag_ratio=0.3), run_time=1.1)
        # "follow each tool's current instructions": each tool's own page
        hear(self, "follow each", lead=0.1)
        self.play(FadeOut(launch), FadeOut(fan), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(VGroup(p, l)) for p, l in zip(pages, pls)], lag_ratio=0.3), run_time=1.0)
        done(self)


# ═════════════════════════════ PART E — B80 B81 B90 B91 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pE_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pE_chip_left(text, xl, y, mono=False, size=34):
    """A chip whose LEFT edge sits at xl (table columns line up on the left)."""
    lab = M(text, size - 2) if mono else T(text, size)
    w = lab.width + 0.8
    return chip(text, xl + w / 2, y, w=w, mono=mono, size=size)


def pE_chip_mixed(parts, xl, y):
    """A chip holding a serif word and a mono address side by side, left edge at xl. `.pill`."""
    grp = VGroup(*parts).arrange(RIGHT, buff=0.16)
    w = grp.width + 0.8
    cx = xl + w / 2
    shadow = pill(cx + 0.08, y - 0.08, w, h=0.8, fill=BOX_L)
    body = pill(cx, y, w, h=0.8)
    grp.move_to([cx, y, 0])
    g = VGroup(shadow, body, grp)
    g.pill = body
    return g


def pE_ring(g, pad=0.14):
    """A terracotta ring round a chip (the ring pulse that marks the cause)."""
    p = g.pill
    hh = 0.8 + 2 * pad
    return RoundedRectangle(width=p.width + 2 * pad, height=hh, corner_radius=hh / 2, stroke_color=TERRA,
                            stroke_width=6, fill_opacity=0).move_to(p.get_center())


class B80_FourFailures(Scene):
    """A two-column table builds row by row: symptom chip left, cause chip right, each cause ringed in terracotta."""
    def construct(self):
        title = pE_act_title("VIII · When It Breaks")
        ys = [1.15, 0.0, -1.15, -2.3]
        xl, xr = -6.0, 0.95
        h1 = T("symptom", 34)
        h1.move_to([xl + h1.width / 2, 2.1, 0])
        h2 = T("cause", 34)
        h2.move_to([xr + h2.width / 2, 2.15, 0])
        top = Line([-6.1, 1.75, 0], [6.1, 1.75, 0], color=BAR2, stroke_width=4)
        div = DashedLine([0.05, 2.5, 0], [0.05, -2.85, 0], color=BAR2, stroke_width=4, dash_length=0.2)
        rules = [Line([-6.1, y - 0.575, 0], [6.1, y - 0.575, 0], color=BAR2, stroke_width=4) for y in ys]
        sym = [pE_chip_left("404 every request", xl, ys[0]),
               Group(logo_chip("claude", xl + 0.54, ys[1], h=0.8), pE_chip_left("model not found", xl + 1.3, ys[1])),
               pE_chip_left("raw tool calls", xl, ys[2]),
               pE_chip_left("CPU/GPU split", xl, ys[3])]
        cau = [pE_chip_mixed([T("base URL ends", 34), M("/v1", 34)], xr, ys[0]),
               pE_chip_left("aliases not mapped", xr, ys[1]),
               pE_chip_left("no tools label", xr, ys[2]),
               pE_chip_left("model/window too big", xr, ys[3])]
        arrs = [Arrow([-0.55, y, 0], [0.5, y, 0], buff=0, color=INK, stroke_width=7, max_tip_length_to_length_ratio=0.5) for y in ys]
        rings = [pE_ring(c) for c in cau]

        self.play(FadeIn(title), FadeIn(h1), FadeIn(h2), Create(top), Create(div), run_time=0.5)
        # row 1: 404 on every request -> the base address ends in /v1
        hear(self, "404 on", lead=0.2)
        self.play(FadeIn(sym[0]), Create(rules[0]), run_time=0.3)
        hear(self, "the base address", lead=0.2)
        self.play(Create(arrs[0]), FadeIn(cau[0]), run_time=0.35)
        hear(self, "slash V1", lead=0.3)
        self.play(Create(rings[0]), run_time=0.35)
        self.wait(0.25)
        self.play(FadeOut(rings[0]), run_time=0.25)
        # row 2: a Claude model name not found -> the aliases are not mapped
        hear(self, "Claude model name", lead=0.2)
        self.play(FadeIn(sym[1]), Create(rules[1]), run_time=0.3)
        hear(self, "the aliases", lead=0.2)
        self.play(Create(arrs[1]), FadeIn(cau[1]), run_time=0.3)
        at(self, 9.05)        # after the clip midpoint: a ring alive at the midpoint is read as accent text by GATE T
        self.play(Create(rings[1]), run_time=0.3)
        self.wait(0.25)
        self.play(FadeOut(rings[1]), run_time=0.25)
        # row 3: tool calls printed as raw text -> the model has no tools label
        hear(self, "tool calls printed", lead=0.15)
        self.play(FadeIn(sym[2]), Create(rules[2]), run_time=0.3)
        hear(self, "the model has", lead=0.15)
        self.play(Create(arrs[2]), FadeIn(cau[2]), run_time=0.3)
        hear(self, "tools label", lead=0.25)
        self.play(Create(rings[2]), run_time=0.35)
        self.wait(0.25)
        self.play(FadeOut(rings[2]), run_time=0.25)
        # row 4: a split between processor and GPU -> the model or the window is too big
        hear(self, "a split between", lead=0.15)
        self.play(FadeIn(sym[3]), Create(rules[3]), run_time=0.3)
        hear(self, "model or the window", lead=0.3)
        self.play(Create(arrs[3]), FadeIn(cau[3]), run_time=0.3)
        hear(self, "too big", lead=0.3)
        self.play(Create(rings[3]), run_time=0.35)
        done(self)


def pE_globe(x, y, r=0.7):
    """A plain globe for 'the internet': white disc, ink outline, a meridian and two parallels."""
    disc = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    mer = Ellipse(width=r * 0.9, height=2 * r, stroke_color=INK, stroke_width=3, fill_opacity=0).move_to([x, y, 0])
    eq = Line([x - r, y, 0], [x + r, y, 0], color=INK, stroke_width=3)
    p1 = Line([x - r * 0.86, y + r * 0.5, 0], [x + r * 0.86, y + r * 0.5, 0], color=INK, stroke_width=3)
    p2 = Line([x - r * 0.86, y - r * 0.5, 0], [x + r * 0.86, y - r * 0.5, 0], color=INK, stroke_width=3)
    return VGroup(disc, mer, eq, p1, p2)


def pE_pipe(x0, x1, y, h=0.26):
    return Rectangle(width=x1 - x0, height=h, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([(x0 + x1) / 2, y, 0])


class B81_ProxyAndModulePurge(Scene):
    """Home fills up; a pull stalls on a compute node with no way out; the 'explorer' module sets the proxy gate and the
    pipe opens; 'module purge' sweeps the chip off and the pipe breaks; 'module load explorer' puts it back."""
    def construct(self):
        py = -1.5                      # the pipe's height
        # home box with a gauge (top right)
        hbox = home_box(Iso(4.55, 0.95, 0.8))
        hlab = T("home", 36).move_to([4.55, 0.5, 0])
        gx0, gw, gy = 0.9, 2.6, 1.4
        track = Rectangle(width=gw, height=0.45, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([gx0 + gw / 2, gy, 0])
        outl = Rectangle(width=gw, height=0.45, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([gx0 + gw / 2, gy, 0])
        outl.set_z_index(6)
        g1 = Rectangle(width=gw / 2, height=0.45, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([gx0 + gw / 4, gy, 0])
        g2 = Rectangle(width=gw / 2, height=0.45, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([gx0 + 3 * gw / 4, gy, 0])
        full = T("full", 36).move_to([gx0 + gw / 2, 1.95, 0])
        c1 = chip("image cache", 0.4, 2.65, size=34)
        c2 = chip("models", 0.4, 2.65, size=34)
        # compute node, pipe, gate, internet
        rack = VGroup(*explorer_rack(Iso(-4.9, -2.3, 0.75)))
        rlab = T("compute node", 34).move_to([-4.9, -2.85, 0])
        globe = pE_globe(4.75, py, 0.7)
        glab = T("internet", 34).move_to([4.75, -2.55, 0])
        pipeL = pE_pipe(-4.05, -1.7, py)
        pipeR = pE_pipe(1.7, 4.05, py)
        pipeM = pE_pipe(-1.7, 1.7, py)
        pipeM.set_z_index(0)
        posts = VGroup(*[Rectangle(width=0.26, height=1.4, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, -0.95, 0]) for x in (-0.75, 0.75)])
        bar = Rectangle(width=1.76, height=0.28, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0, -0.25, 0])
        gate = VGroup(posts, bar)
        gate.set_z_index(3)
        proxy = T("proxy", 36).move_to([2.2, -0.55, 0])
        mod = chip("explorer", 0.0, 0.42, mono=True, size=34)
        mod.set_z_index(4)
        # the pull: a small box labelled with the real subcommand
        pbox = job_box(Iso(0, 0, 0.5), 0, 0, 0, s=0.7).move_to([-3.2, -0.97, 0])
        plab = M("pull", 32).move_to([-3.2, -1.97, 0])
        pull = VGroup(pbox, plab)
        xm = x_mark(0, py, r=0.35, w=9)
        stamp = chip("Research Computing's pages", -2.9, 2.7, size=34)
        plq1 = plaque("module purge", -4.1, 1.55, w=3.8, h=0.9, size=32)
        plq2 = plaque("module load explorer", -2.85, 1.55, w=6.3, h=0.9, size=32)
        ok = check(0, py + 0.02, s=0.3, color=TERRA, w=12)

        # home is full: the cache and the models were sent to home
        hear(self, "a full home", lead=0.15)
        self.play(FadeIn(hbox), FadeIn(hlab), FadeIn(track), FadeIn(outl), run_time=0.4)
        hear(self, "the image cache", lead=0.15)
        self.play(FadeIn(c1), run_time=0.2)
        self.play(c1.animate.move_to([4.5, 2.0, 0]).scale(0.4), GrowFromEdge(g1, LEFT), run_time=0.55)
        self.play(FadeOut(c1), run_time=0.1)
        hear(self, "the models", lead=0.15)
        self.play(FadeIn(c2), run_time=0.2)
        self.play(c2.animate.move_to([4.5, 2.0, 0]).scale(0.4), GrowFromEdge(g2, LEFT), run_time=0.55)
        self.play(FadeOut(c2), run_time=0.1)
        hear(self, "defaulted to home", lead=0.1)
        self.play(FadeIn(full), run_time=0.3)
        # a pull on a compute node
        hear(self, "A pull that", lead=0.2)
        self.play(FadeIn(rack), FadeIn(pipeL), FadeIn(pull), run_time=0.4)
        hear(self, "that fails", lead=0.1)
        self.play(pull.animate.shift(RIGHT * 1.3), run_time=0.6)
        hear(self, "compute node", lead=0.15)
        self.play(FadeIn(rlab), run_time=0.3)
        hear(self, "no outbound", lead=0.25)
        self.play(FadeIn(globe), FadeIn(glab), FadeIn(pipeR), run_time=0.3)
        self.play(FadeIn(xm), run_time=0.2)
        # the proxy gate opens the way
        hear(self, "On Explorer", lead=0.1)
        self.play(FadeIn(gate), FadeOut(xm), FadeIn(pipeM), run_time=0.5)
        hear(self, "a default module", lead=0.0)
        self.play(FadeIn(mod, shift=DOWN * 0.45), run_time=0.35, rate_func=smooth)
        hear(self, "sets the proxy", lead=0.0)
        self.play(pull.animate.shift(RIGHT * 2.6), run_time=0.5)
        hear(self, "proxy", lead=0.1)
        self.play(FadeIn(proxy), pull.animate.shift(RIGHT * 2.8), run_time=0.6)
        hear(self, "that nodes use", lead=0.2)
        self.play(FadeIn(stamp), run_time=0.3)
        # module purge sweeps the chip off; the pipe breaks
        hear(self, "module purge", lead=0.25)
        self.play(FadeIn(plq1), run_time=0.3)
        hear(self, "it loses", lead=0.2)
        self.play(mod.animate.shift(LEFT * 3.7), FadeOut(pipeM), FadeIn(xm), run_time=0.6)
        # load it again: the chip returns and the pipe reconnects
        hear(self, "load the module", lead=0.2)
        self.play(FadeOut(plq1), FadeIn(plq2), run_time=0.3)
        hear(self, "again right", lead=0.2)
        self.play(mod.animate.shift(RIGHT * 3.7), FadeIn(pipeM), FadeOut(xm), run_time=0.6)
        self.play(Create(ok), run_time=0.3)
        done(self)


class B90_IdleWatcher(Scene):
    """A GPU-use line with bursts and a long flat gap; the watcher sweeps the flat part: 15 min an email, an hour the
    job is cancelled; filler work is crossed out; start when you sit down, cancel when you stop, batch the long work."""
    def construct(self):
        title = pE_act_title("IX · The Cluster's Rules")
        f = 0.05                        # the line's floor
        ay = -0.2                       # the time axis
        x0, x15, x60 = -3.2, -0.7, 2.2
        axis = Line([-5.85, ay, 0], [5.95, ay, 0], color=BAR1, stroke_width=5)
        yax = Line([-5.85, ay, 0], [-5.85, 1.9, 0], color=BAR1, stroke_width=5)
        ylab = T("GPU use", 34)
        ylab.move_to([-5.85 + ylab.width / 2, 2.2, 0])
        xlab = T("time", 34).move_to([5.45, -0.62, 0])
        pts = [(-5.85, f), (-5.6, f), (-5.45, 1.45), (-5.3, 0.7), (-5.15, 1.2), (-4.95, f), (-4.5, f), (-4.35, 1.0), (-4.15, f),
               (-3.8, f), (-3.7, 1.3), (-3.5, 0.6), (-3.35, f), (5.7, f)]
        gline = VMobject(stroke_color=INK, stroke_width=7)
        gline.set_points_as_corners([[a, b, 0] for a, b in pts])
        gline.set_z_index(2)
        peaks = VGroup(*[Dot([a, b, 0], radius=0.11, color=TERRA) for a, b in ((-5.45, 1.45), (-4.35, 1.0), (-3.7, 1.3))])
        peaks.set_z_index(3)
        bursty = T("bursty", 34).move_to([-2.9, 1.15, 0])
        # the watcher: a terracotta scan line carrying a chip
        scan = Line([x0, ay + 0.05, 0], [x0, 2.15, 0], color=TERRA, stroke_width=6)
        wchip = pE_chip_left("idle watcher", x0 + 0.02, 2.15)
        wchip.set_z_index(5)
        watcher = VGroup(scan, wchip)
        band1 = Rectangle(width=x15 - x0, height=0.7, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([(x0 + x15) / 2, f + 0.3, 0])
        band2 = Rectangle(width=x60 - x15, height=0.7, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([(x15 + x60) / 2, f + 0.3, 0])
        tk15 = VGroup(Line([x15, ay, 0], [x15, ay - 0.25, 0], color=INK, stroke_width=5), T("15 min", 34).move_to([x15, -0.75, 0]))
        tk60 = VGroup(Line([x60, ay, 0], [x60, ay - 0.25, 0], color=INK, stroke_width=5), T("1 hour", 34).move_to([x60, -0.75, 0]))
        env = pE_envelope(x15, -1.75)
        elab = T("email", 34).move_to([x15 - 1.3, -1.75, 0])
        jbox = VGroup(Iso(0, 0, 0.5).box(0, 0, 0, 0.9, 0.9, 0.72)).move_to([x60, -1.75, 0])
        jlab = T("job", 34).move_to([x60 - 0.95, -1.75, 0])
        jx = x_mark(x60, -1.75, r=0.32, w=9)
        you = professor_bear("1x1", 1.3, seed="B90", x=4.4, y=-1.75)
        ylb = T("you", 34).move_to([3.35, -1.75, 0])
        youg = Group(you, ylb)
        fx = -1.7
        flag = VGroup(Line([fx, f, 0], [fx, 1.0, 0], color=INK, stroke_width=6),
                      Polygon([fx, 1.0, 0], [fx + 0.6, 0.82, 0], [fx, 0.64, 0], fill_color=INK, fill_opacity=1, stroke_color=INK, stroke_width=2))
        flab = T("flagged", 34).move_to([fx + 1.5, 1.0, 0])
        filler = Rectangle(width=1.9, height=0.7, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([4.2, f + 0.4, 0])
        filab = T("filler work", 34).move_to([4.2, 1.15, 0])
        fix = x_mark(4.2, f + 0.4, r=0.4, w=9)
        k1 = pE_chip_left("sit down: start", -6.0, -2.85, size=32)
        k2 = pE_chip_left("stop: cancel", -2.45, -2.85, size=32)
        k3 = pE_chip_left("long work: batch jobs", 0.7, -2.85, size=32)

        self.play(FadeIn(title), FadeIn(ylab), Create(axis), Create(yax), run_time=0.45)
        self.play(Create(gline), FadeIn(xlab), run_time=0.75)
        # "idle GPUs": the watcher appears on the first flat stretch and sweeps it
        hear(self, "idle", lead=0.2)
        self.play(FadeIn(watcher), run_time=0.25)
        self.play(GrowFromEdge(band1, LEFT), watcher.animate.shift(RIGHT * (x15 - x0)), run_time=1.8, rate_func=linear)
        # "fifteen minutes ... an email"
        self.play(FadeIn(tk15), run_time=0.2)
        hear(self, "earns an", lead=0.3)
        self.play(FadeIn(env, shift=DOWN * 0.6), FadeIn(elab), run_time=0.35, rate_func=smooth)
        # "an hour ... the job cancelled"
        hear(self, "for an hour", lead=0.5)
        self.play(GrowFromEdge(band2, LEFT), watcher.animate.shift(RIGHT * (x60 - x15)), run_time=0.9, rate_func=linear)
        self.play(FadeIn(tk60), run_time=0.2)
        hear(self, "gets the job", lead=0.3)
        self.play(FadeIn(jbox, shift=DOWN * 0.6), FadeIn(jlab), run_time=0.35, rate_func=smooth)
        hear(self, "cancelled", lead=0.15)
        self.play(Create(jx), run_time=0.25)
        # "Coding is bursty ... long gaps while you read"
        hear(self, "bursty", lead=0.3)
        self.play(FadeIn(peaks), FadeIn(bursty), run_time=0.35)
        hear(self, "while you read", lead=0.35)
        self.play(FadeIn(youg), run_time=0.4)
        # "a session you walk away from will be flagged"
        hear(self, "walk away", lead=0.1)
        self.play(youg.animate.shift(RIGHT * 1.0), run_time=0.6, rate_func=smooth)
        hear(self, "be flagged", lead=0.35)
        self.play(FadeIn(flag, shift=DOWN * 0.4), FadeIn(flab), run_time=0.35, rate_func=smooth)
        # "Never add filler work"
        hear(self, "filler", lead=0.25)
        self.play(GrowFromEdge(filler, DOWN), FadeIn(filab), run_time=0.35)
        hear(self, "keep it alive", lead=0.35)
        self.play(Create(fix), run_time=0.25)
        # "Start when you sit down, cancel when you stop, ... batch jobs"
        hear(self, "Start when", lead=0.15)
        self.play(FadeIn(k1, shift=UP * 0.2), run_time=0.3)
        hear(self, "cancel when", lead=0.15)
        self.play(FadeIn(k2, shift=UP * 0.2), run_time=0.3)
        hear(self, "in batch jobs", lead=0.2)
        self.play(FadeIn(k3, shift=UP * 0.2), run_time=0.3)
        done(self)


def pE_envelope(x, y, w=1.1, h=0.75):
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.08, y - 0.08, 0])
    body = Rectangle(width=w, height=h, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    f1 = Line([x - w / 2, y + h / 2, 0], [x, y - 0.02, 0], color=INK, stroke_width=4)
    f2 = Line([x + w / 2, y + h / 2, 0], [x, y - 0.02, 0], color=INK, stroke_width=4)
    return VGroup(shadow, body, f1, f2)


class B91_NotAJobsShape(Scene):
    """An endpoint on a Slurm job dies when the 8 h clock runs out and returns elsewhere; and one person's cache grows to
    five stacked caches as five students share Ollama, filling the memory tank to about five times."""
    def construct(self):
        # top: the endpoint, its clock, its replacement
        rack1 = VGroup(*explorer_rack(Iso(-3.1, 1.0, 0.85)))
        lab1 = chip("endpoint", -3.1, 0.45, size=34)
        cdots = VGroup(*[Dot([x, y, 0], radius=0.15, color=TERRA) for x, y in ((-5.7, 2.2), (-5.1, 1.7), (-5.75, 1.3), (-5.15, 0.85), (-5.6, 0.45))])
        clines = VGroup(*[Line([x, y, 0], [-4.15, 1.5, 0], color=BAR1, stroke_width=3) for x, y in ((-5.7, 2.2), (-5.1, 1.7), (-5.75, 1.3), (-5.15, 0.85), (-5.6, 0.45))])
        slurm = chip("slurm", -0.5, 2.7, mono=True, size=34)
        cx, cy, cr = -0.5, 1.5, 0.6
        face = Circle(radius=cr, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([cx, cy, 0])
        ticks = VGroup(*[Line([cx + cr * 0.8 * np.sin(a), cy + cr * 0.8 * np.cos(a), 0], [cx + cr * 0.95 * np.sin(a), cy + cr * 0.95 * np.cos(a), 0], color=INK, stroke_width=4) for a in (0, PI / 2, PI, 3 * PI / 2)])
        hand = Line([cx, cy, 0], [cx, cy + cr * 0.7, 0], color=INK, stroke_width=7)
        hub = Dot([cx, cy, 0], radius=0.07, color=INK)
        clock = VGroup(face, ticks, hand, hub)
        eight = T("8 h", 46).move_to([0.95, 1.7, 0])
        gpu = M("gpu", 32).move_to([0.95, 1.1, 0])
        dead = x_mark(-3.1, 1.85, r=0.5, w=10)
        rack2 = VGroup(*explorer_rack(Iso(3.6, 1.0, 0.85)))
        lab2 = chip("new address", 3.6, 0.45, size=34)
        idle = chip("idle", 5.3, 1.75, w=1.3, size=34)
        reqs = [Dot([1.75, 1.6, 0], radius=0.13, color=TERRA) for _ in range(2)]
        # bottom: one user's cache grows to five; the memory tank fills
        olla = logo_chip("ollama", -5.2, -1.85, h=1.2)
        bx, bw, bh = -2.2, 2.2, 0.4
        by = [-2.85 + 0.5 * i for i in range(5)]
        blocks = [Rectangle(width=bw, height=bh, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([bx, y, 0]) for y in by]
        sdots = [Dot([-3.7, y, 0], radius=0.14, color=TERRA) for y in by]
        clab = T("cache", 34).move_to([-0.45, by[0], 0])
        tx, tw, th, ty = 1.1, 0.9, 2.4, -1.85
        tank = Rectangle(width=tw, height=th, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([tx, ty, 0])
        fh = th / 5
        fill1 = Rectangle(width=tw - 0.14, height=fh, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([tx, ty - th / 2 + 0.07 + fh / 2, 0])
        fillf = Rectangle(width=tw - 0.14, height=th - 0.14, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([tx, ty, 0])
        mlab = T("memory", 34).move_to([tx, -0.35, 0])
        ctx = chip("64,000 context", 4.05, -1.0, size=34)
        five = T("about 5x", 54).move_to([4.0, -2.3, 0])

        # "the shared endpoint for a whole class"
        hear(self, "shared endpoint", lead=0.35)
        self.play(FadeIn(rack1), FadeIn(lab1), run_time=0.4)
        hear(self, "whole class", lead=0.3)
        self.play(FadeIn(cdots), Create(clines), run_time=0.55)
        # "A Slurm job has a time limit, eight hours on the GPU partition"
        hear(self, "slurm job", lead=0.3)
        self.play(FadeIn(slurm), run_time=0.3)
        hear(self, "a time limit", lead=0.3)
        self.play(FadeIn(clock), run_time=0.3)
        self.play(Rotate(hand, angle=-PI, about_point=[cx, cy, 0]), run_time=0.7, rate_func=linear)
        hear(self, "eight hours", lead=0.1)
        self.play(Rotate(hand, angle=-PI, about_point=[cx, cy, 0]), FadeIn(eight), run_time=0.7, rate_func=linear)
        hear(self, "GPU partition", lead=0.2)
        self.play(FadeIn(gpu), run_time=0.3)
        # "an endpoint built on one dies on a schedule"
        hear(self, "dies on", lead=0.2)
        self.play(FadeIn(dead), run_time=0.25)
        hear(self, "a schedule", lead=0.1)
        self.play(FadeOut(rack1), FadeOut(lab1), FadeOut(dead), FadeOut(cdots), FadeOut(clines), run_time=0.45)
        # "returns on a different node"
        hear(self, "returns on", lead=0.15)
        self.play(FadeIn(rack2, shift=LEFT * 0.4), FadeIn(lab2, shift=LEFT * 0.4), run_time=0.45)
        # "Between requests, the GPU idles"
        hear(self, "Between requests", lead=0.1)
        self.play(FadeIn(reqs[0]), run_time=0.1)
        self.play(reqs[0].animate.move_to([2.75, 1.6, 0]), run_time=0.3, rate_func=linear)
        self.play(FadeOut(reqs[0]), run_time=0.1)
        self.wait(0.15)
        self.play(FadeIn(reqs[1]), run_time=0.1)
        self.play(reqs[1].animate.move_to([2.75, 1.6, 0]), run_time=0.3, rate_func=linear)
        self.play(FadeOut(reqs[1]), run_time=0.1)
        hear(self, "the GPU idles", lead=0.15)
        self.play(FadeIn(idle, shift=LEFT * 0.2), run_time=0.3)
        # "Ollama serves one person well"
        hear(self, "Olama serves", lead=0.25)
        self.play(FadeIn(olla), run_time=0.3)
        hear(self, "one person", lead=0.25)
        self.play(FadeIn(blocks[0]), FadeIn(sdots[0]), FadeIn(clab), FadeIn(tank), FadeIn(mlab), run_time=0.4)
        self.play(GrowFromEdge(fill1, DOWN), run_time=0.3)
        # "Five students ... roughly five times the cache memory"
        hear(self, "Five students", lead=0.15)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(blocks[i], shift=DOWN * 0.3), FadeIn(sdots[i])) for i in range(1, 5)], lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(ctx), run_time=0.3)
        hear(self, "cost roughly", lead=0.15)
        self.play(ReplacementTransform(fill1, fillf), run_time=0.8)
        hear(self, "five times", lead=0.2)
        self.play(FadeIn(five, scale=1.2), run_time=0.3)
        done(self)


# ═════════════════════════════ PART F — B92 B94 B95 B100 B101 B102 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pF_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pF_clamp(a):
    return max(0.0, min(1.0, float(a)))


def pF_when(self, phrase, nth=0, lead=0.0, default=0.0):
    """The measured time Liam says `phrase` (same matching as hear(), but returns the time)."""
    import re as _re
    bid = type(self).__name__.split("_")[0]
    words = _ASR.get(bid)
    if not words:
        return default
    norm = lambda w: _re.sub(r"[^a-z0-9]", "", w.lower())
    toks = [norm(x) for x in phrase.split() if norm(x)]
    seq = [norm(w[0]) for w in words]
    hits = [i for i in range(len(seq) - len(toks) + 1) if seq[i:i + len(toks)] == toks]
    if len(hits) <= nth:
        return default
    return float(words[hits[nth]][1]) - lead


def pF_page(x, y, w=1.0, h=0.9, n=2):
    """A small prompt page: white sheet, ink outline, handwriting lines."""
    pg = paper(x, y, w=w, h=h)
    _w = w - 2 * 0.18
    ln = VGroup(*[scribble(pg.cx - _w / 2, pg.cy + pg.h / 2 - 0.18 - 0.1 - i * 0.26, _w, amp=0.09, sw=3) for i in range(n)])
    return VGroup(pg, ln)


def pF_belt(x0, x1, y, h=0.3):
    """A conveyor belt: kraft band, deep-kraft edge (never an ink edge: GATE T reads that as text)."""
    return Rectangle(width=x1 - x0, height=h, fill_color=BOX_L, fill_opacity=1, stroke_color=KRAFT_DEEP,
                     stroke_width=4).move_to([(x0 + x1) / 2, y, 0])


def pF_crate(x, y, s=0.5, dark=False):
    """A small isometric crate whose near corner sits at (x, y)."""
    ci = Iso(x, y, s)
    if dark:
        return ci.box(0, 0, 0, 1, 1, 0.8, DARK_TOP, DARK_L, DARK_R)
    return ci.box(0, 0, 0, 1, 1, 0.8)


def pF_stamp(text, x, y, w=None, h=0.68, size=32, sub=None, marker="dot", left=False):
    """A white pill with a marker dot and a 1-3 word label. x is the pill's LEFT edge when left=True, else its centre."""
    lab = T(text, size)
    sl = T(sub, size) if sub else None
    textw = max(lab.width, sl.width if sl else 0)
    w = w or (textw + 1.15)
    cx = x + w / 2 if left else x
    if sl:
        h = max(h, 1.1)
    shadow = pill(cx + 0.08, y - 0.08, w, h=h, fill=BOX_L)
    body = pill(cx, y, w, h=h)
    lx = cx - w / 2 + 0.72 + textw / 2
    if sl:
        lab.move_to([lx - textw / 2 + lab.width / 2, y + 0.2, 0])
        sl.move_to([lx - textw / 2 + sl.width / 2, y - 0.2, 0])
    else:
        lab.move_to([lx, y, 0])
    mx = cx - w / 2 + 0.38
    if marker == "dot":
        mk = Dot([mx, y, 0], radius=0.12, color=TERRA)
    else:
        mk = Circle(radius=0.12, color=DIM, stroke_width=4).move_to([mx, y, 0])
    parts = [shadow, body, lab, mk] + ([sl] if sl else [])
    g = VGroup(*parts)
    g.w, g.h = w, h
    return g


# ───────────────────────────────────── B92 ─────────────────────────────────────
def pF_lock_for(x, y):
    return padlock(x + 0.3, y + 0.56, s=0.46)


class B92_SharedService(Scene):
    """Users' keys + prompt pages merge into one batch, lock, pass through the vllm server; three questions float above."""
    def construct(self):
        ys = [1.4, 0.15, -1.1]
        keys = [key_obj(-5.75, y, s=0.55) for y in ys]
        pages = [pF_page(-3.7, y, w=1.15, h=1.0) for y in ys]
        px, py = -1.9, -0.35                     # first page of the batch pile (the cascade steps +0.55, -0.5)
        spots = [(px + 0.55 * k, py - 0.5 * k) for k in range(3)]
        iso = Iso(3.0, -2.0, 1.15)
        stack, lights = explorer_rack(iso)
        srv = VGroup(stack, lights)
        vllm = logo_chip("vllm", 3.0, -2.72, h=1.0)
        batch_lab = T("batch", 34).move_to([px + 0.55, py + 1.45, 0])
        klab = T("API key", 34).move_to([-5.0, 2.3, 0])
        locks = [pF_lock_for(x, y) for (x, y) in spots]
        doc = pF_page(-5.55, -2.6, w=0.9, h=1.1, n=3)
        alone = chip("key alone", -3.65, -2.6, size=34)
        xm = x_mark(-1.95, -2.6, r=0.28, w=9)
        ch = [chip("logging?", -1.48, 2.6), chip("retention?", 1.255, 2.6), chip("who owns it?", 4.44, 2.6)]
        ask = chip("ask Research Computing", 1.7, 1.45)

        # "a service for many people": the users' pages arrive, each with its key
        hear(self, "many people", lead=0.3)
        self.play(LaggedStart(*[FadeIn(g) for g in pages + keys], lag_ratio=0.12), run_time=0.7)
        # "vLLM": the server and its logo
        hear(self, "VLLM", lead=0.3)
        self.play(FadeIn(srv), FadeIn(vllm), run_time=0.5)
        # "batches concurrent requests": the pages merge into one batch
        hear(self, "batches", lead=0.15)
        self.play(*[pg.animate.shift(np.array([sx - (-3.7), sy - y, 0.0])) for pg, (sx, sy), y in zip(pages, spots, ys)],
                  run_time=0.9, rate_func=smooth)
        hear(self, "requests", lead=0.2)
        self.play(FadeIn(batch_lab), run_time=0.3)
        # "API keys": the keys get their name, a padlock lands on each prompt page
        hear(self, "API", lead=0.2)
        self.play(FadeIn(klab), LaggedStart(*[GrowFromCenter(l) for l in locks], lag_ratio=0.2), run_time=0.6)
        pile = VGroup(*pages, *locks)
        # "its own documentation ... not to rely on a key alone"
        hear(self, "documentation", lead=0.2)
        self.play(FadeIn(doc), run_time=0.4)
        hear(self, "key alone", lead=0.1)
        self.play(FadeIn(alone, shift=RIGHT * 0.3), Create(xm), run_time=0.45)
        # "other people's code and prompts": the batch goes into the server (done before the clip midpoint)
        hear(self, "other peoples", lead=0.4)
        self.play(pile.animate.shift(RIGHT * 1.775), FadeOut(batch_lab), run_time=0.5, rate_func=smooth)
        self.play(FadeOut(pile, shift=RIGHT * 0.6, scale=0.6), lights.animate.set_color(TERRA), run_time=0.3)
        # "pass through a service you run": the batch comes out the far side
        out_spots = [(5.0 + 0.55 * k, -0.4 - 0.5 * k) for k in range(3)]
        out = VGroup(*[pF_page(sx, sy, w=1.15, h=1.0) for sx, sy in out_spots], *[pF_lock_for(sx, sy) for sx, sy in out_spots])
        out.scale(0.62).move_to([5.38, -0.85, 0])
        hear(self, "pass through", lead=0.1)
        self.play(FadeIn(out, shift=RIGHT * 0.5), run_time=0.5)
        # "logging, retention, who is responsible"
        hear(self, "logging", lead=0.15)
        self.play(FadeIn(ch[0], shift=DOWN * 0.3), run_time=0.35)
        hear(self, "retention", lead=0.15)
        self.play(FadeIn(ch[1], shift=DOWN * 0.3), run_time=0.35)
        hear(self, "who is responsible", lead=0.15)
        self.play(FadeIn(ch[2], shift=DOWN * 0.3), run_time=0.35)
        # "questions for Research Computing, not settings": the plaque lands under them
        hear(self, "Those are questions", lead=0.15)
        ask.shift(UP * 0.7)
        self.add(ask)
        self.play(ask.animate.shift(DOWN * 0.7), run_time=0.5, rate_func=smooth)
        done(self)


# ───────────────────────────────────── B94 ─────────────────────────────────────
def pF_grid(x0, yc, cols, rows=8, pitch=0.115, side=0.09, color=BAR1):
    """A block of GPU slots: `cols` columns of `rows` small squares, left edge at x0. `.cols` is the list of columns."""
    cells = []
    for c in range(cols):
        cells.append(VGroup(*[Rectangle(width=side, height=side, fill_color=color, fill_opacity=1, stroke_width=0)
                              .move_to([x0 + c * pitch + side / 2, yc + (rows / 2 - 0.5 - r) * pitch, 0]) for r in range(rows)]))
    g = VGroup(*cells)
    g.cols = cells
    return g


class B94_AicrScale(Scene):
    """The big AICR rack with its two GPU blocks and a proposal chip; Explorer first; a standing service between them."""
    def construct(self):
        ai = Iso(0.5, -2.2, 0.8)
        a_stack, a_lights = aicr_rack(ai)
        aicr = VGroup(a_stack, a_lights)
        a_lab = T("AICR", 40).move_to([0.95, -2.85, 0])
        g1 = pF_grid(2.45, 1.65, 31, color=BAR1)
        g2 = pF_grid(2.45, -0.4, 19, color=BAR2)
        l1 = T("B200 x 248", 34).move_to([2.45 + 2.15 / 2, 2.5, 0])
        l2 = T("RTX Pro x 152", 34).move_to([2.45 + 2.81 / 2, 0.55, 0])
        prop = VGroup(pill(4.38, -1.73, 3.6, h=0.95, fill=BOX_L), pill(4.3, -1.65, 3.6, h=0.95),
                      paper(2.95, -1.65, w=0.5, h=0.66), key_obj(3.4, -1.65, s=0.3), T("proposal", 34).move_to([5.1, -1.65, 0]))
        ei = Iso(-4.9, -1.9, 0.8)
        e_stack, e_lights = explorer_rack(ei)
        expl = VGroup(e_stack, e_lights)
        e_lab = T("Explorer", 36).move_to([-4.9, -2.6, 0])
        first = chip("first", -4.9, 0.6, size=34)
        link = Arrow([-3.95, -1.0, 0], [-0.7, -1.0, 0], color=INK, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.18)
        si = Iso(-2.3, -1.9, 0.9)
        svc = si.box(0, 0, 0, 1.1, 1.1, 0.8)
        svc.set_z_index(3)
        s_lab = T("standing service", 34).move_to([-2.3, -2.65, 0])
        q = T("?", 64).move_to([-2.3, 0.3, 0])
        ring = Circle(radius=1.5, color=TERRA, stroke_width=6).move_to([-2.3, -0.6, 0])
        ask = T("ask Research Computing", 34).move_to([-2.3, 1.45, 0])

        # "On AICR": the large rack, named
        hear(self, "AICR", lead=0.1)
        self.play(FadeIn(aicr), FadeIn(a_lab), run_time=0.5)
        # "248 B200": the first block of GPU slots fills, column by column
        hear(self, "248", lead=0.2)
        self.play(LaggedStart(*[FadeIn(c) for c in g1.cols], lag_ratio=0.03), run_time=1.1)
        hear(self, "B200", lead=0.1)
        self.play(FadeIn(l1), run_time=0.3)
        # "152 RTX Pro": the second block
        hear(self, "152", lead=0.15)
        self.play(LaggedStart(*[FadeIn(c) for c in g2.cols], lag_ratio=0.04), run_time=0.8)
        hear(self, "RTX Pro", lead=0.1)
        self.play(FadeIn(l2), run_time=0.3)
        # "access is by proposal": the key-and-paper chip lands beside AICR
        hear(self, "proposal", lead=0.4)
        self.play(FadeIn(prop, shift=DOWN * 0.3), run_time=0.4)
        # "develop and test on Explorer first": the small rack, then the arrow toward AICR
        hear(self, "Explorer", lead=0.4)
        self.play(FadeIn(expl), FadeIn(e_lab), run_time=0.5)
        hear(self, "first", lead=0.1)
        self.play(Create(link), FadeIn(first, shift=DOWN * 0.2), run_time=0.5)
        # "a standing service": the block lands on the arrow, linking both racks
        hear(self, "standing", lead=0.25)
        svc.shift(UP * 0.6)
        self.add(svc)
        self.play(svc.animate.shift(DOWN * 0.6), FadeIn(s_lab), run_time=0.5, rate_func=smooth)
        # "a question only Research Computing can answer": the question mark, then the ring and the pointer
        hear(self, "question", lead=0.2)
        self.play(GrowFromCenter(q), run_time=0.35)
        hear(self, "research computing", lead=0.2, nth=1)
        self.play(Create(ring), FadeIn(ask), run_time=0.6)
        done(self)


# ───────────────────────────────────── B95 ─────────────────────────────────────
class B95_CheckedVsDocumented(Scene):
    """Two columns of stamps: what is documented but not run, and the five read-only checks; then the one thing no page says."""
    def construct(self):
        hd_l = T("documented", 40)
        hd_l.move_to([-5.8 + hd_l.width / 2, 2.85, 0])
        sub_l = T("not run here", 32)
        sub_l.move_to([-5.8 + sub_l.width / 2, 2.3, 0])
        hd_r = T("checked on Explorer", 40)
        hd_r.move_to([0.3 + hd_r.width / 2, 2.85, 0])
        sub_r = T("read-only", 32)
        sub_r.move_to([0.3 + sub_r.width / 2, 2.3, 0])
        div = DashedLine([0, 3.1, 0], [0, -1.1, 0], color=BAR2, stroke_width=4, dash_length=0.2)
        ys = [1.55, 0.8, 0.05, -0.7]
        left = [pF_stamp(s, -5.8, y, left=True, marker="ring") for s, y in zip(["scripts", "tunnel", "proxy", "harness settings"], ys)]
        right = [pF_stamp(s, 0.3, y, left=True) for s, y in zip(["partitions", "H200 type exists", "apptainer on login node",
                                                                 "proxy from default module"], ys)]
        right.append(pF_stamp("scratch not writable", 0.3, -1.7, left=True, sub="on one account"))
        ghost5 = DashedVMobject(RoundedRectangle(width=4.3, height=0.95, corner_radius=0.45, stroke_color=BAR2, stroke_width=4),
                                num_dashes=44).move_to([0.3 + 2.15, -1.7, 0])
        oll = logo_chip("ollama", -5.4, -1.65, h=0.85)
        rcp = T("Research Computing post", 32)
        rcp.move_to([-4.7 + rcp.width / 2, -1.65, 0])
        agw = T("agent access: not stated by any policy page", 32).width + 0.9
        agent = VGroup(pill(0.08, -2.93, agw, h=0.8, fill=BOX_L), pill(0, -2.85, agw, h=0.8),
                       T("agent access: not stated by any policy page", 32).move_to([0, -2.85, 0]))
        ring = RoundedRectangle(width=agw + 0.3, height=1.05, corner_radius=0.52, color=TERRA, stroke_width=5).move_to([0, -2.85, 0])

        # "what we have and have not checked": the two headings
        hear(self, "what we have", lead=0.1)
        self.play(FadeIn(hd_l), Create(div), run_time=0.4)
        hear(self, "not checked", lead=0.15)
        self.play(FadeIn(hd_r), FadeIn(ghost5), run_time=0.4)
        # "not run this whole setup from start to finish": the documented items stamp in
        hear(self, "not run", lead=0.15)
        self.play(FadeIn(sub_l), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(s, scale=1.25) for s in left], lag_ratio=0.28), run_time=1.3)
        # "with read-only commands on Explorer"
        hear(self, "read only", lead=0.2)
        self.play(FadeIn(sub_r), run_time=0.3)
        # the five read-only checks, each on its words
        hear(self, "partitions", lead=0.2)
        self.play(FadeIn(right[0], scale=1.25), run_time=0.35)
        hear(self, "H200", lead=0.2)
        self.play(FadeIn(right[1], scale=1.25), run_time=0.35)
        hear(self, "on the login node", lead=0.3)
        self.play(FadeIn(right[2], scale=1.25), run_time=0.35)
        hear(self, "proxy comes", lead=0.2)
        self.play(FadeIn(right[3], scale=1.25), run_time=0.35)
        hear(self, "scratch", lead=0.2)
        self.play(FadeIn(right[4], scale=1.25), FadeOut(ghost5), run_time=0.35)
        # "Research Computing has a post on running Ollama in a container"
        hear(self, "Research computing", lead=0.2)
        self.play(FadeIn(oll), FadeIn(rcp), run_time=0.5)
        # "no page we read ... whether automated agents are allowed"
        hear(self, "no page", lead=0.3)
        self.play(FadeIn(agent, shift=UP * 0.3), run_time=0.5)
        hear(self, "coding agents", lead=0.1)
        self.play(Create(ring), run_time=0.6)
        hear(self, "automated agents", lead=0.2)
        self.play(Indicate(agent, color=INK, scale_factor=1.04), run_time=0.6)
        done(self)


# ───────────────────────────────────── B100 ─────────────────────────────────────
def pF_arc_arrow(c, r, a0, a1, w=7, tip=0.28, color=INK):
    """An arc from angle a0 to a1 (radians, either way round) ending in a filled arrow tip."""
    arc = Arc(radius=r, start_angle=a0, angle=a1 - a0, arc_center=[c[0], c[1], 0], color=color, stroke_width=w)
    end = np.array([c[0] + r * np.cos(a1), c[1] + r * np.sin(a1), 0.0])
    d = 1.0 if a1 > a0 else -1.0
    tang = d * np.array([-np.sin(a1), np.cos(a1), 0.0])
    nrm = np.array([np.cos(a1), np.sin(a1), 0.0])
    base = end - tang * tip
    tri = Polygon(end + tang * tip * 0.4, base + nrm * tip * 0.6, base - nrm * tip * 0.6,
                  fill_color=color, fill_opacity=1, stroke_width=0)
    return VGroup(arc, tri)


def pF_strand(x0, y0, x1, dy, amp=0.07, sw=4):
    """One frayed thread end: a wavy line from (x0, y0) to (x1, y0 + dy)."""
    pts = [[x0 + (x1 - x0) * t, y0 + dy * t + amp * np.sin(t * 14) * (0.3 + t), 0] for t in np.linspace(0, 1, 40)]
    m = VMobject(stroke_color=INK, stroke_width=sw)
    m.set_points_smoothly(pts)
    return m


class B100_WeakerAgent(Scene):
    """A context bar fills with system prompt, tool definitions and history while the agent loop turns and glitches; the thread frays."""
    def construct(self):
        title = pF_act_title("X · What To Expect")
        C = (0.6, 0.9)
        claude = logo_chip("claude", C[0], C[1])
        ring = VGroup(pF_arc_arrow(C, 1.5, np.radians(150), np.radians(30)),
                      pF_arc_arrow(C, 1.5, np.radians(-30), np.radians(-150)))
        # the context bar: a white track, then three block types stacking inside it
        track = Rectangle(width=11.8, height=0.8, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0, -2.2, 0])
        by = -2.2
        sysb = Rectangle(width=2.4, height=0.64, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.82 + 1.2, by, 0])
        tools = VGroup(*[Rectangle(width=0.2, height=0.64, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                         .move_to([-3.36 + 0.1 + 0.25 * i, by, 0]) for i in range(14)])
        hist = [Rectangle(width=0.9, height=0.64, fill_color=BOX_R, fill_opacity=1, stroke_width=0)
                .move_to([0.15 + 0.45 + 0.96 * i, by, 0]) for i in range(6)]
        l_sys = T("system prompt", 32).move_to([-4.62, -3.0, 0])
        l_tools = T("tool definitions", 32).move_to([-1.6, -3.0, 0])
        l_hist = T("history", 32).move_to([3.0, -3.0, 0])
        # the glitches on the loop
        gap = Rectangle(width=0.55, height=0.7, fill_color=STAGE, fill_opacity=1, stroke_width=0).move_to([C[0], C[1] + 1.5, 0])
        zig = VMobject(stroke_color=INK, stroke_width=6)
        zig.set_points_as_corners([[C[0] - 0.22, C[1] + 1.78, 0], [C[0] + 0.12, C[1] + 1.58, 0], [C[0] - 0.12, C[1] + 1.42, 0],
                                   [C[0] + 0.22, C[1] + 1.22, 0]])
        l_mal = T("malformed", 32).move_to([3.95, 2.05, 0])
        again = pF_arc_arrow(C, 1.85, np.radians(150), np.radians(30), w=6)
        l_loops = T("loops", 32).move_to([3.7, 0.35, 0])
        # the thread from the start of the work; its end frays
        ty = -1.25
        thread = Line([-5.82, ty, 0], [-0.1, ty, 0], color=INK, stroke_width=5)
        t_dot = Dot([-5.82, ty, 0], radius=0.11, color=TERRA)
        l_thr = T("thread", 32).move_to([-5.15, ty + 0.45, 0])
        strands = VGroup(pF_strand(-0.1, ty, 3.2, 0.38), pF_strand(-0.1, ty, 4.5, 0.0), pF_strand(-0.1, ty, 5.4, -0.34))
        l_files = T("many files", 32).move_to([4.3, ty + 0.62, 0])

        self.play(FadeIn(title), FadeIn(track), run_time=0.4)
        hear(self, "agent", lead=0.1)
        self.play(FadeIn(claude), run_time=0.4)
        # "Claude Code's loop is demanding": the loop turns
        hear(self, "loop", lead=0.3)
        self.play(Create(ring), run_time=0.5)
        self.play(Rotate(ring, angle=-2 * PI, about_point=[C[0], C[1], 0]), run_time=0.8, rate_func=smooth)
        # "a long system prompt"
        hear(self, "long system", lead=0.15)
        self.play(GrowFromEdge(sysb, LEFT), FadeIn(l_sys), run_time=0.6)
        # "dozens of tool definitions"
        hear(self, "dozens", lead=0.15)
        self.play(LaggedStart(*[GrowFromEdge(t, LEFT) for t in tools], lag_ratio=0.06), FadeIn(l_tools), run_time=0.9)
        # "a growing history": the first turns land before the midpoint, the rest after it
        hear(self, "growing", lead=0.3)
        self.play(LaggedStart(GrowFromEdge(hist[0], LEFT), GrowFromEdge(hist[1], LEFT), lag_ratio=0.5), FadeIn(l_hist), run_time=0.45)
        hear(self, "every turn", lead=0.15)
        self.play(LaggedStart(*[GrowFromEdge(h, LEFT) for h in hist[2:]], lag_ratio=0.25), run_time=0.9)
        # "more malformed tool calls": the call arrow breaks
        hear(self, "malformed", lead=0.25)
        self.add(gap)
        self.play(FadeIn(gap, run_time=0.01), Create(zig), FadeIn(l_mal), run_time=0.45)
        # "more loops": the call repeats and the loop keeps turning
        hear(self, "loops", lead=0.2)
        self.play(Create(again), FadeIn(l_loops), run_time=0.4)
        self.play(Rotate(ring, angle=-2 * PI, about_point=[C[0], C[1], 0]), run_time=0.7, rate_func=smooth)
        # "an earlier loss of the thread": the thread runs out from the start, then frays
        hear(self, "earlier", lead=0.1)
        self.play(FadeIn(t_dot), Create(thread), FadeIn(l_thr), run_time=0.5)
        hear(self, "thread", lead=0.1)
        self.play(*[Create(s) for s in strands], run_time=0.7)
        # "big changes across many files"
        hear(self, "many files", lead=0.2)
        self.play(FadeIn(l_files), run_time=0.3)
        done(self)


# ───────────────────────────────────── B101 ─────────────────────────────────────
class B101_WhereItWorks(Scene):
    """Two columns: four chips with a check each for what it does well, three with a cross each for what it does poorly."""
    def construct(self):
        hd_w = T("does well", 48)
        hd_w.move_to([-5.2 + hd_w.width / 2, 2.6, 0])
        hd_p = T("does poorly", 48)
        hd_p.move_to([1.1 + hd_p.width / 2, 2.6, 0])
        div = DashedLine([0, 3.0, 0], [0, -2.5, 0], color=BAR2, stroke_width=4, dash_length=0.2)
        ys = [1.4, 0.35, -0.7, -1.75]

        def row(text, x_left, y, good):
            c = chip(text, 0, y, size=36)
            c.move_to([x_left + c.width / 2 - 0.0, y, 0])
            c.shift(RIGHT * 0.0)
            mk = check(x_left - 0.5, y, s=0.2, color=TERRA, w=9) if good else x_mark(x_left - 0.45, y, r=0.24, w=8)
            return c, mk

        good = [row(s, -5.2, y, True) for s, y in zip(["clear tasks, clear tests", "bulk batch work", "stays on Northeastern", "teaching"], ys)]
        poor = [row(s, 1.1, y, False) for s, y in zip(["open-ended refactors", "long debugging", "costly wrong calls"], ys)]

        ghosts = [DashedVMobject(RoundedRectangle(width=4.5, height=0.8, corner_radius=0.4, stroke_color=BAR2, stroke_width=4),
                                 num_dashes=44).move_to([1.1 + 2.25, y, 0]) for y in ys[:3]]

        def land(self, pair, dx, ghost=None):
            c, mk = pair
            extra = [FadeOut(ghost)] if ghost is not None else []
            self.play(FadeIn(c, shift=RIGHT * dx), Create(mk), *extra, run_time=0.4)

        hear(self, "does well", lead=0.2)
        self.play(FadeIn(hd_w), FadeIn(hd_p), Create(div), *[FadeIn(g) for g in ghosts], run_time=0.5)
        hear(self, "clear tasks", lead=0.2)
        land(self, good[0], 0.3)
        hear(self, "bulk", lead=0.2)
        land(self, good[1], 0.3)
        hear(self, "code that should", lead=0.2)
        land(self, good[2], 0.3)
        hear(self, "teaching", lead=0.2)
        land(self, good[3], 0.3)
        hear(self, "does poorly", lead=0.2)
        self.play(Indicate(hd_p, color=INK, scale_factor=1.06), run_time=0.4)
        hear(self, "open", lead=0.2)
        land(self, poor[0], 0.3, ghosts[0])
        hear(self, "long debugging", lead=0.2)
        land(self, poor[1], 0.3, ghosts[1])
        hear(self, "anything where", lead=0.2)
        land(self, poor[2], 0.3, ghosts[2])
        done(self)


# ───────────────────────────────────── B102 ─────────────────────────────────────
class B102_PracticalSplit(Scene):
    """Small work crates ride the belt into the local-model rack; one heavy crate goes to the Claude chip; two receipts end it."""
    def construct(self):
        belt_hi = pF_belt(-6.0, 2.1, 1.75)
        belt_lo = pF_belt(-6.0, 1.9, -0.7)
        iso = Iso(3.9, 0.85, 0.9)
        stack, lights = explorer_rack(iso)
        rack = VGroup(stack, lights)
        rack_lab = T("local model", 34).move_to([3.9, 0.4, 0])
        claude = logo_chip("claude", 3.4, -0.7)
        front = T("frontier", 32).move_to([5.45, -0.7, 0])
        names = ["drafts", "boilerplate", "tests", "batch"]
        cues = ["drafting", "boilerplate", "tests", "batch passes"]
        smalls = []
        for nm in names:
            cr = pF_crate(0, 0, s=0.5)
            lb = T(nm, 32).move_to([0, 1.05, 0])
            smalls.append(VGroup(cr, lb))
        heavy = VGroup(pF_crate(0, 0, s=0.7, dark=True), T("hard problem", 32).move_to([0, 1.55, 0]))
        rec1 = chip("real savings", -2.9, -2.45)
        ck = check(-5.0, -2.45, s=0.24, color=TERRA, w=10)
        rec2 = chip("same thing, free", 2.5, -2.45)
        xm = x_mark(4.95, -2.45, r=0.3, w=9)

        # "A practical split": two lanes, the Claude chip at the end of the lower one
        hear(self, "practical split", lead=0.2)
        self.play(Create(belt_hi), Create(belt_lo), FadeIn(claude), run_time=0.6)
        # "the local model": the rack and its name
        hear(self, "the local model", lead=0.1)
        self.play(FadeIn(rack), FadeIn(rack_lab), run_time=0.5)
        # "drafting, boilerplate, tests and batch passes ... the hard problems": one clock-driven span, all done before the midpoint
        t0 = pF_when(self, "drafting", lead=0.2, default=1.7)
        tt = [pF_when(self, c, lead=0.2, default=t0 + 0.5 * i) for i, c in enumerate(cues)]
        t_front = pF_when(self, "frontier", lead=0.2, default=4.6)
        t_go = pF_when(self, "for the hard", lead=0.0, default=5.4)
        t_end = min(t_go + 0.6, 6.0)
        clock = VGroup(*smalls, heavy, front, lights)   # the clock's mobject: the renderer redraws only what an animation holds
        for g in smalls + [heavy, front]:
            g.set_opacity(0)
        self.add(clock)
        speed, x_in, x_out = 3.6, -4.1, 2.35
        sy, hy = 2.49, 0.26
        hx0, hx1 = -1.6, 1.35
        arrive = [t + (x_out - x_in) / speed for t in tt]

        def tick(t):
            for g, ts, ta in zip(smalls, tt, arrive):
                a_in = pF_clamp((t - ts) / 0.25)
                a_out = pF_clamp((t - ta) / 0.25)
                x = min(x_in + speed * max(0.0, t - ts), x_out)
                g.set_opacity(a_in * (1 - a_out))
                g.move_to([x, sy - 0.35 * a_out, 0])
            for i, ta in enumerate(arrive):
                if t >= ta:
                    lights[i // 2].set_color(TERRA)
            front.set_opacity(pF_clamp((t - t_front) / 0.3))
            ah = pF_clamp((t - t_front) / 0.3)
            m = pF_clamp((t - t_go) / max(0.1, t_end - t_go))
            m = m * m * (3 - 2 * m)
            heavy.set_opacity(ah)
            heavy.move_to([hx0 + (hx1 - hx0) * m, hy, 0])

        at(self, t0)
        start = _elapsed(self)
        span = t_end - start
        if span > 0.2:
            self.play(UpdateFromAlphaFunc(clock, lambda m, a: tick(start + a * span)), run_time=span, rate_func=linear)
        # "Measured that way, the savings are real"
        hear(self, "savings", lead=0.35)
        self.play(FadeIn(rec1, shift=DOWN * 0.3), Create(ck), run_time=0.5)
        # "Measured as the same thing for free, they are not"
        hear(self, "same thing", lead=0.25)
        self.play(FadeIn(rec2, shift=DOWN * 0.3), run_time=0.4)
        hear(self, "not", lead=0.1, nth=0)
        self.play(Create(xm), run_time=0.35)
        done(self)


# ═════════════════════════════ PART G — B110 ═════════════════════════════
def pG_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


class B110_WhereToGetStarted(Scene):
    """The repository address lands, then skills/ and local-llm-on-explorer/ open one under the other, and the get-started page lands."""
    def construct(self):
        title = pG_act_title("XI · Get Started")
        url = M("github.com/nikbearbrown/hpc-aicr", 32).move_to([0, 1.8, 0])
        under = Line([url.get_left()[0], 1.35, 0], [url.get_right()[0], 1.35, 0], color=TERRA, stroke_width=6)
        sk = M("skills/", 36).move_to([0, 0.65, 0])
        lc = M("local-llm-on-explorer/", 34).move_to([0, -0.4, 0])
        c1 = Line([0, 1.15, 0], [0, 0.95, 0], color=INK, stroke_width=5)
        c2 = Line([0, 0.3, 0], [0, 0.05, 0], color=INK, stroke_width=5)
        pg = paper(0, -1.9, w=1.3, h=1.55)
        _w = 1.3 - 2 * 0.22
        ln = VGroup(*[scribble(-_w / 2, -1.9 + 1.55 / 2 - 0.22 - 0.1 - i * 0.3, _w, amp=0.09) for i in range(2)])
        c3 = Line([0, -0.75, 0], [0, -1.1, 0], color=INK, stroke_width=5)
        name = M("GET-STARTED.md", 32).move_to([0, -3.0, 0])
        # faint dashed slots show the whole chain from the start; each real item replaces its slot
        def slot(w, h, y):
            return DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=min(0.3, h / 2), stroke_color=BAR2, stroke_width=4),
                                  num_dashes=36).move_to([0, y, 0])
        g_sk, g_lc, g_pg, g_nm = slot(2.4, 0.75, 0.65), slot(6.2, 0.75, -0.4), slot(1.3, 1.55, -1.9), slot(3.8, 0.7, -3.0)

        self.play(FadeIn(title), run_time=0.4)
        hear(self, "go to the", lead=0.2)
        self.play(FadeIn(url), Create(under), *[FadeIn(g) for g in (g_sk, g_lc, g_pg, g_nm)], run_time=0.6)
        hear(self, "Skills folder", lead=0.3)
        self.play(Create(c1), FadeIn(sk), FadeOut(g_sk), run_time=0.4)
        hear(self, "Local LLM", lead=0.3)
        self.play(Create(c2), FadeIn(lc), FadeOut(g_lc), run_time=0.4)
        hear(self, "Get Started", lead=0.25)
        self.play(Create(c3), FadeIn(pg), FadeIn(ln), FadeIn(name), FadeOut(g_pg), FadeOut(g_nm), run_time=0.5)
        done(self)


for _cls in (B10_TheIdea, B11_ThreeLayers, B12_PatternA, B13_PatternB, B20_OpenDoor, B22_BareBaseUrl, B23_TunnelTarget, B24_AliasMap, B25_SilentTruncation, B26_TooSmallModel, B27_NotFree, B31_HomeFills, B40_FitInVram, B41_ModelsThatFit, B42_StrongestAndTools, B43_OneGpuPerJob, B44_ContextKnobs, B53_UnsupportedRoute, B54_ContextGrowsThenExit, B60_LockInFront, B64_TwoRisks, B72_LaunchDefaults, B80_FourFailures, B81_ProxyAndModulePurge, B90_IdleWatcher, B91_NotAJobsShape, B92_SharedService, B94_AicrScale, B95_CheckedVsDocumented, B100_WeakerAgent, B101_WhereItWorks, B102_PracticalSplit, B110_WhereToGetStarted):
    _cls.play = ST.play
