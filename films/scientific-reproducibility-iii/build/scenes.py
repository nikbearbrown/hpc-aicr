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
_ASR = {"BOPEN": [["Research", 0.0], ["Computing", 0.38], ["on", 0.78], ["Explorer", 1.0], ["and", 1.46], ["AICR,", 1.72], ["scientific", 3.42], ["reproducibility", 3.42], ["3,", 4.26], ["containers,", 5.02], ["how", 5.9], ["to", 5.98], ["put", 6.12], ["a", 6.22], ["program", 6.36], ["and", 6.66], ["everything", 6.9], ["it", 7.2], ["needs", 7.44], ["into", 7.64], ["one", 7.9], ["file,", 8.12], ["run", 8.82], ["it", 8.92], ["on", 9.04], ["a", 9.16], ["cluster", 9.28], ["with", 9.5], ["Aptainer", 9.74], ["and", 10.18], ["record", 10.58], ["it", 10.84], ["so", 11.04], ["someone", 11.24], ["else", 11.62], ["can", 11.8], ["repeat", 12.02], ["your", 12.36], ["results.", 12.54]], "BIDEA": [["Hello,", 0.64], ["this", 1.34], ["is", 1.4], ["Liam", 1.62], ["in", 1.92], ["for", 2.2], ["Bear.", 2.36], ["First", 3.06], ["a", 3.2], ["correction.", 3.38], ["To", 4.06], ["repeat", 4.12], ["a", 4.4], ["result,", 4.52], ["sharing", 5.04], ["your", 5.18], ["code", 5.44], ["is", 5.66], ["not", 5.8], ["enough.", 6.0], ["The", 6.66], ["libraries", 6.78], ["and", 7.16], ["the", 7.5], ["system", 7.62], ["under", 7.94], ["it", 8.16], ["change.", 8.34], ["A", 9.04], ["container", 9.1], ["seals", 9.42], ["the", 9.78], ["whole", 10.0], ["software", 10.18], ["stack", 10.68], ["into", 11.0], ["one", 11.22], ["file.", 11.44]], "BDEFS": [["Six", 0.0], ["terms,", 0.28], ["container,", 1.14], ["a", 1.46], ["sealed", 1.54], ["bundle", 1.74], ["of", 2.04], ["a", 2.24], ["program", 2.38], ["and", 2.6], ["what", 2.88], ["it", 3.04], ["needs.", 3.16], ["Image,", 4.0], ["the", 4.24], ["file", 4.34], ["a", 4.56], ["container", 4.72], ["is", 5.04], ["made", 5.3], ["from.", 5.54], ["Aptainer", 6.12], ["runs", 6.38], ["containers", 6.72], ["on", 7.24], ["shared", 7.56], ["clusters.", 7.82], ["SIF", 8.84], ["file,", 9.08], ["Aptainer's", 9.66], ["single", 10.14], ["file", 10.4], ["image.", 10.74], ["Bind", 11.66], ["shows", 11.72], ["a", 12.02], ["folder", 12.2], ["from", 12.42], ["the", 12.72], ["machine", 12.82], ["inside", 13.16], ["the", 13.56], ["container", 13.76], ["and", 14.2], ["tag", 14.78], ["the", 15.08], ["version", 15.34], ["label", 15.62], ["on", 15.94], ["an", 16.16], ["image.", 16.26]], "B10": [["A", 0.0], ["container", 0.16], ["is", 0.48], ["one", 0.78], ["sealed", 1.0], ["file.", 1.3], ["Inside,", 2.18], ["it's", 2.58], ["hit", 2.72], ["a", 2.78], ["program,", 2.9], ["its", 3.44], ["libraries,", 3.58], ["its", 4.28], ["settings,", 4.42], ["and", 4.96], ["a", 5.02], ["small", 5.12], ["runtime.", 5.38], ["Move", 6.58], ["that", 6.7], ["file", 6.88], ["to", 7.16], ["a", 7.38], ["laptop,", 7.48], ["to", 8.06], ["a", 8.14], ["cluster,", 8.28], ["or", 8.86], ["to", 8.96], ["the", 9.06], ["cloud,", 9.18], ["and", 9.78], ["what", 9.86], ["is", 10.0], ["inside", 10.14], ["does", 10.56], ["not", 10.8], ["change.", 11.04]], "B11": [["You", 0.0], ["will", 0.12], ["meet", 0.22], ["three", 0.38], ["names.", 0.64], ["Docker", 1.32], ["is", 1.38], ["the", 1.58], ["most", 1.68], ["common", 1.82], ["tool", 2.16], ["on", 2.46], ["laptops,", 2.74], ["cloud", 3.6], ["servers,", 3.62], ["and", 4.24], ["most", 4.32], ["published", 4.54], ["images.", 4.94], ["Singularity", 6.36], ["is", 6.72], ["the", 7.02], ["older", 7.14], ["name", 7.36], ["of", 7.6], ["the", 7.76], ["cluster", 7.86], ["tool.", 8.1], ["Aptainer", 8.92], ["is", 9.16], ["its", 9.38], ["current", 9.54], ["name,", 9.78], ["and", 10.34], ["it", 10.4], ["is", 10.48], ["what", 10.6], ["Northeastern's", 10.78], ["clusters,", 11.54], ["Explorer,", 12.2], ["and", 12.78], ["AIC", 12.88], ["are,", 13.26], ["use.", 13.8]], "B12": [["Why", 0.0], ["not", 0.14], ["use", 0.32], ["Docker", 0.56], ["on", 0.82], ["a", 1.06], ["cluster?", 1.18], ["Docker's", 2.0], ["normal", 2.16], ["setup", 2.48], ["needs", 2.82], ["administrator", 3.16], ["-level", 3.74], ["power", 3.98], ["and", 4.48], ["on", 4.92], ["a", 5.04], ["machine", 5.12], ["shared", 5.42], ["by", 5.76], ["thousands", 6.0], ["of", 6.38], ["people", 6.66], ["that", 6.94], ["is", 7.14], ["a", 7.28], ["security", 7.42], ["problem.", 7.76], ["Aptainer", 9.16], ["runs", 9.38], ["the", 9.66], ["container", 9.9], ["as", 10.26], ["you", 10.56], ["with", 10.8], ["your", 11.1], ["permissions", 11.22], ["and", 11.58], ["no", 11.92], ["more.", 12.12], ["It", 12.7], ["can", 12.8], ["still", 12.92], ["read", 13.16], ["Docker", 13.42], ["images.", 13.8]], "B20": [["First", 0.0], ["benefit,", 0.28], ["reproducible.", 0.88], ["The", 1.82], ["whole", 1.92], ["software", 2.12], ["stack", 2.54], ["is", 2.86], ["captured,", 3.04], ["so", 3.72], ["your", 3.9], ["result", 4.04], ["ties", 4.36], ["to", 4.68], ["one", 4.92], ["named", 5.12], ["versioned", 5.56], ["image.", 6.2], ["A", 7.04], ["collaborator", 7.14], ["running", 7.52], ["it", 7.96], ["six", 8.2], ["months", 8.44], ["from", 8.74], ["now", 8.98], ["gets", 9.26], ["the", 9.5], ["same", 9.74], ["software,", 9.98], ["even", 10.78], ["after", 11.08], ["the", 11.34], ["system", 11.54], ["underneath", 11.82], ["has", 12.22], ["been", 12.54], ["updated.", 12.72]], "B21": [["Portable,", 0.0], ["the", 0.58], ["same", 0.6], ["file", 0.84], ["runs", 1.18], ["on", 1.42], ["your", 1.64], ["laptop,", 1.74], ["on", 2.44], ["Explorer,", 2.46], ["on", 3.12], ["another", 3.2], ["cluster,", 3.46], ["or", 4.12], ["in", 4.24], ["the", 4.34], ["cloud,", 4.48], ["and", 5.18], ["no", 5.32], ["dependency", 5.5], ["fights.", 6.0], ["Two", 7.16], ["tools", 7.32], ["that", 7.68], ["need", 7.9], ["incompatible", 8.08], ["versions", 8.72], ["of", 9.18], ["one", 9.44], ["library", 9.64], ["each", 10.02], ["get", 10.36], ["their", 10.6], ["own", 10.78], ["image,", 10.94], ["so", 11.46], ["neither", 11.64], ["one", 11.8], ["breaks", 12.12], ["the", 12.38], ["other.", 12.64]], "B22": [["Shareable,", 0.0], ["it", 0.6], ["is", 0.64], ["one", 0.74], ["file", 0.94], ["you", 1.24], ["can", 1.4], ["hand", 1.5], ["to", 1.72], ["a", 1.88], ["collaborator,", 1.98], ["archive", 2.84], ["with", 3.1], ["your", 3.36], ["data,", 3.5], ["or", 3.98], ["point", 4.06], ["a", 4.28], ["reviewer", 4.44], ["at.", 4.7], ["And", 5.52], ["Readymade,", 5.6], ["registries", 6.3], ["such", 6.8], ["as", 6.94], ["DockerHub,", 7.2], ["Key", 7.9], [".io,", 8.02], ["NVIDIA", 9.08], ["and", 9.3], ["GC,", 9.56], ["and", 10.24], ["BioContainers", 10.42], ["host", 11.24], ["thousands", 11.52], ["of", 11.98], ["maintained", 12.34], ["images.", 12.78]], "B23": [["Containers", 0.0], ["cost", 0.5], ["something,", 0.78], ["images", 1.42], ["are", 1.58], ["large,", 1.92], ["and", 2.5], ["the", 2.54], ["first", 2.66], ["build", 2.86], ["takes", 3.12], ["effort,", 3.36], ["so", 3.92], ["try", 4.24], ["a", 4.44], ["module", 4.6], ["first,", 4.84], ["software", 5.78], ["the", 5.78], ["cluster", 6.0], ["already", 6.26], ["installed,", 6.64], ["then", 7.64], ["conda", 7.82], ["a", 8.28], ["package", 8.46], ["manager,", 8.7], ["then", 9.62], ["a", 9.78], ["container", 9.9], ["when", 10.24], ["the", 10.58], ["install", 10.7], ["is", 11.08], ["painful", 11.28], ["or", 11.64], ["you", 12.04], ["need", 12.2], ["a", 12.34], ["portable", 12.48], ["record.", 12.78]], "B30": [["Aptainer", 0.0], ["has", 0.4], ["three", 0.62], ["verbs,", 0.92], ["exec", 1.78], ["runs", 1.78], ["one", 2.04], ["command", 2.34], ["inside", 2.68], ["the", 3.06], ["container", 3.24], ["then", 3.62], ["returns,", 3.88], ["that", 4.78], ["is", 4.9], ["the", 5.02], ["verb", 5.2], ["for", 5.38], ["jobs.", 5.64], ["Shell", 6.88], ["opens", 6.88], ["an", 7.2], ["interactive", 7.38], ["shell", 7.78], ["inside", 8.18], ["it", 8.56], ["for", 8.8], ["poking", 8.98], ["around", 9.3], ["and", 9.62], ["testing,", 9.88], ["and", 10.54], ["run", 10.68], ["does", 10.88], ["the", 11.12], ["container's", 11.3], ["built", 11.88], ["-in", 12.06], ["default", 12.24], ["action.", 12.6]], "B31": [["Check", 0.0], ["the", 0.2], ["tool", 0.38], ["first,", 0.52], ["both", 1.12], ["commands", 1.24], ["are", 1.66], ["read", 1.84], ["-only", 2.02], ["and", 2.26], ["safe", 2.54], ["on", 2.78], ["a", 2.98], ["login", 3.1], ["node.", 3.32], ["On", 4.16], ["Explorer", 4.24], ["we", 4.64], ["recorded", 4.88], ["this,", 5.22], ["the", 5.78], ["path", 5.88], ["in", 6.1], ["version", 6.4], ["1", 6.6], [".4", 6.94], [".5", 7.44], ["installed", 8.08], ["system", 8.62], ["-wide", 9.06], ["so", 9.34], ["there", 9.7], ["is", 9.82], ["no", 9.92], ["module", 10.12], ["to", 10.52], ["load.", 10.8], ["AICR", 11.84], ["has", 12.32], ["aptainer", 12.5], ["and", 13.04], ["singularity", 13.24], ["as", 13.96], ["well.", 14.1]], "B32": [["Run", 0.0], ["containers", 0.24], ["on", 0.74], ["a", 0.96], ["compute", 1.12], ["node,", 1.32], ["never", 1.86], ["on", 1.96], ["the", 2.18], ["login", 2.3], ["node.", 2.58], ["The", 3.38], ["login", 3.46], ["node", 3.74], ["is", 4.08], ["shared", 4.24], ["by", 4.48], ["everyone", 4.72], ["and", 5.18], ["heavy", 5.5], ["work", 5.72], ["there", 6.0], ["gets", 6.18], ["terminated.", 6.4], ["Ask", 7.6], ["SLURM", 7.74], ["for", 8.14], ["a", 8.3], ["compute", 8.42], ["node", 8.66], ["first", 8.92], ["with", 9.2], ["srun,", 9.42], ["then", 10.12], ["work", 10.24], ["inside", 10.5], ["that", 10.86], ["session.", 11.14]], "B33": [["Then", 0.0], ["open", 0.14], ["a", 0.34], ["shell", 0.56], ["in", 0.76], ["an", 0.92], ["image.", 1.04], ["The", 1.68], ["path", 1.72], ["is", 1.9], ["a", 2.1], ["placeholder", 2.22], ["for", 2.56], ["your", 2.86], ["own", 2.98], ["project.", 3.14], ["Your", 4.0], ["prompt", 4.08], ["changes", 4.3], ["to", 4.68], ["Aptainer", 4.96], ["which", 5.4], ["tells", 5.68], ["you", 5.94], ["that", 6.2], ["you", 6.28], ["are", 6.42], ["inside.", 6.54], ["Type", 7.42], ["exit", 7.54], ["to", 7.88], ["leave.", 8.1], ["Inside", 9.08], ["you", 9.3], ["have", 9.6], ["only", 9.74], ["what", 9.94], ["the", 10.16], ["image", 10.28], ["holds", 10.48], ["plus", 10.88], ["the", 11.18], ["folders", 11.42], ["you", 11.74], ["bind", 12.0], ["in.", 12.24]], "B34": [["For", 0.0], ["a", 0.16], ["batch", 0.3], ["job,", 0.46], ["put", 0.98], ["the", 1.0], ["same", 1.16], ["command", 1.36], ["in", 1.72], ["a", 1.92], ["script.", 2.02], ["Ask", 2.8], ["for", 2.88], ["the", 3.1], ["partition,", 3.2], ["cores,", 4.04], ["memory,", 4.48], ["and", 4.9], ["time", 4.96], ["your", 5.18], ["work", 5.34], ["needs,", 5.54], ["then", 6.08], ["run", 6.2], ["exec", 6.42], ["binding", 6.72], ["your", 7.16], ["project", 7.42], ["folder", 7.78], ["in.", 8.1], ["Create", 8.98], ["the", 9.22], ["logs", 9.4], ["folder", 9.62], ["first", 9.98], ["and", 10.36], ["submit", 10.66], ["with", 10.98], ["sbatch.", 11.2]], "B35": [["On", 0.0], ["a", 0.14], ["GPU,", 0.28], ["the", 0.78], ["container", 0.92], ["can", 1.2], ["carry", 1.48], ["its", 1.74], ["own", 1.96], ["CUDA,", 2.16], ["so", 2.64], ["you", 2.8], ["do", 2.9], ["not", 2.98], ["match", 3.16], ["the", 3.42], ["node's", 3.62], ["modules,", 3.94], ["but", 4.62], ["it", 4.78], ["still", 4.9], ["needs", 5.08], ["the", 5.32], ["node's", 5.54], ["driver.", 5.86], ["The", 6.6], ["dash", 6.72], ["dash", 6.96], ["NV", 7.24], ["flag", 7.66], ["passes", 8.06], ["that", 8.54], ["driver", 8.82], ["in.", 9.16], ["Without", 9.78], ["it,", 10.0], ["the", 10.3], ["container", 10.4], ["has", 10.74], ["no", 11.04], ["link", 11.28], ["to", 11.48], ["the", 11.7], ["GPU.", 11.84]], "B36": [["For", 0.0], ["an", 0.16], ["interactive", 0.26], ["test,", 0.7], ["ask", 1.38], ["for", 1.48], ["one", 1.7], ["GPU.", 1.94], ["Naming", 3.0], ["the", 3.16], ["card", 3.34], ["type", 3.54], ["is", 3.82], ["good", 4.06], ["practice", 4.24], ["when", 4.64], ["the", 4.86], ["card", 4.98], ["matters", 5.2], ["because", 5.56], ["a", 5.94], ["bare", 6.08], ["one", 6.2], ["can", 6.4], ["land", 6.58], ["on", 6.82], ["a", 7.0], ["different", 7.1], ["card.", 7.32], ["List", 8.16], ["the", 8.26], ["types", 8.46], ["first,", 8.68], ["then", 9.4], ["run", 9.54], ["with", 9.74], ["dash", 9.98], ["dash", 10.24], ["NV", 10.54], ["and", 10.9], ["bind", 11.34], ["your", 11.54], ["project.", 11.72]], "B37": [["For", 0.0], ["a", 0.14], ["batch", 0.28], ["GPU", 0.44], ["job,", 0.92], ["here", 1.54], ["is", 1.66], ["a", 1.78], ["template,", 1.96], ["one", 2.64], ["GPU,", 2.74], ["and", 3.56], ["inside", 3.68], ["the", 4.06], ["partition's", 4.24], ["time", 4.88], ["limit.", 5.08], ["The", 6.16], ["container", 6.28], ["carries", 6.6], ["the", 7.02], ["software", 7.24], ["stack,", 7.64], ["the", 8.3], ["NV", 8.38], ["flag", 8.64], ["connects", 9.02], ["the", 9.38], ["driver,", 9.64], ["and", 10.22], ["the", 10.38], ["bind", 10.48], ["gives", 10.74], ["it", 11.02], ["your", 11.16], ["code.", 11.3]], "B38": [["Check", 0.0], ["the", 0.2], ["partition", 0.38], ["limit", 0.64], ["before", 1.0], ["you", 1.34], ["write", 1.5], ["the", 1.7], ["script.", 1.88], ["On", 2.66], ["Explorers'", 2.74], ["GPU", 3.48], ["partition,", 3.8], ["we", 4.58], ["read", 4.6], ["an", 4.78], ["8", 4.92], ["-hour", 5.16], ["limit", 5.32], ["and", 5.66], ["2", 6.02], ["hours", 6.22], ["on", 6.54], ["the", 6.78], ["short", 6.92], ["and", 7.18], ["interactive", 7.38], ["ones.", 7.78], ["A", 8.78], ["published", 8.96], ["example", 9.24], ["asks", 9.72], ["for", 10.06], ["2", 10.32], ["GPUs", 10.56], ["for", 10.88], ["12", 11.32], ["hours", 11.6], ["that", 11.94], ["cannot", 12.38], ["run", 12.64], ["there.", 12.96]], "B39": [["A", 0.0], ["container", 0.16], ["that", 0.48], ["starts", 0.76], ["is", 1.04], ["not", 1.28], ["a", 1.48], ["container", 1.58], ["that", 1.9], ["used", 2.2], ["the", 2.44], ["GPU,", 2.64], ["so", 3.48], ["print", 3.74], ["the", 3.92], ["card's", 4.08], ["name", 4.46], ["from", 4.62], ["inside", 4.86], ["it.", 5.28], ["With", 5.8], ["dash", 5.9], ["dash", 6.18], ["nv", 6.46], ["you", 6.88], ["should", 7.06], ["see", 7.22], ["true", 7.44], ["and", 7.72], ["a", 7.92], ["card", 8.02], ["name,", 8.26], ["and", 8.72], ["without", 8.86], ["it,", 9.12], ["false.", 9.42], ["We", 10.04], ["have", 10.08], ["not", 10.16], ["run", 10.34], ["this", 10.56], ["one.", 10.8]], "B40": [["A", 0.0], ["container", 0.14], ["sees", 0.5], ["its", 0.8], ["own", 0.98], ["file", 1.16], ["system,", 1.42], ["not", 2.0], ["the", 2.1], ["clusters.", 2.26], ["On", 3.2], ["Explorer,", 3.32], ["your", 3.88], ["home", 3.94], ["directory", 4.16], ["is", 4.62], ["bound", 4.9], ["for", 5.14], ["you,", 5.38], ["slash", 6.08], ["projects", 6.14], ["and", 6.64], ["slash", 6.92], ["scratch", 7.26], ["or", 7.56], ["not,", 7.78], ["to", 8.42], ["read", 8.52], ["your", 8.68], ["data", 8.84], ["and", 9.06], ["write", 9.3], ["results", 9.48], ["you", 9.9], ["bind", 10.18], ["each", 10.36], ["folder", 10.58], ["in.", 10.9]], "B41": [["The", 0.0], ["bind", 0.14], ["flag", 0.34], ["takes", 0.62], ["a", 0.86], ["folder", 1.06], ["on", 1.26], ["the", 1.52], ["host,", 1.64], ["a", 2.2], ["colon,", 2.22], ["and", 2.76], ["the", 2.86], ["path", 2.94], ["where", 3.18], ["it", 3.4], ["appears", 3.5], ["inside.", 3.7], ["Binding", 5.02], ["the", 5.12], ["same", 5.38], ["path", 5.6], ["on", 5.84], ["both", 6.04], ["sides", 6.2], ["is", 6.56], ["the", 6.8], ["simplest", 6.96], ["habit,", 7.32], ["because", 7.94], ["your", 8.14], ["script's", 8.28], ["paths", 8.74], ["then", 9.0], ["mean", 9.26], ["the", 9.46], ["same", 9.64], ["inside", 9.88], ["and", 10.3], ["out.", 10.52], ["Use", 11.14], ["absolute", 11.26], ["paths", 11.66], ["and", 12.12], ["bind", 12.38], ["only", 12.62], ["what", 12.94], ["the", 13.18], ["job", 13.32], ["needs.", 13.58]], "B42": [["or", 0.0], ["set", 0.14], ["one", 0.34], ["environment", 0.56], ["variable", 1.04], ["instead", 1.46], ["of", 1.88], ["repeating", 2.02], ["the", 2.36], ["flag,", 2.58], ["we", 3.48], ["put", 3.56], ["it", 3.7], ["inside", 3.8], ["each", 4.16], ["job", 4.44], ["script", 4.76], ["so", 5.2], ["the", 5.52], ["script", 5.66], ["carries", 5.88], ["its", 6.26], ["own", 6.48], ["record", 6.68], ["rather", 7.16], ["than", 7.56], ["in", 7.8], ["the", 7.92], [".bashrc", 8.08], ["file,", 9.04], ["which", 9.68], ["would", 9.84], ["be", 9.96], ["a", 10.06], ["permanent", 10.16], ["edit", 10.44], ["to", 10.76], ["a", 11.0], ["shared", 11.16], ["startup", 11.38], ["file.", 11.76]], "B50": [["You", 0.0], ["cannot", 0.14], ["build", 0.36], ["an", 0.62], ["image", 0.78], ["on", 1.0], ["Explorer.", 1.2], ["Building", 2.0], ["needs", 2.16], ["administrator", 2.52], ["rights.", 3.08], ["So", 3.96], ["build", 3.98], ["on", 4.18], ["a", 4.36], ["machine", 4.44], ["where", 4.7], ["you", 4.9], ["have", 5.0], ["them,", 5.22], ["like", 5.62], ["your", 5.72], ["own", 5.88], ["computer.", 6.04], ["Copy", 7.1], ["the", 7.28], ["finished", 7.48], ["SIF", 7.72], ["file", 8.2], ["to", 8.56], ["the", 8.78], ["cluster,", 8.9], ["store", 9.48], ["it", 9.76], ["in", 9.88], ["project", 10.04], ["space", 10.28], ["and", 10.7], ["run", 10.98], ["it", 11.14], ["there", 11.28], ["as", 11.44], ["yourself.", 11.62]], "B51": [["A", 0.0], [".def", 0.16], ["file", 0.54], ["is", 0.86], ["the", 1.08], ["recipe", 1.22], ["and", 1.56], ["the", 2.0], ["most", 2.1], ["valuable", 2.26], ["file", 2.7], ["for", 3.12], ["reproducibility.", 3.38], ["Bootstrap", 4.82], ["and", 5.22], ["from", 5.4], ["name", 5.56], ["the", 5.76], ["base", 5.96], ["image", 6.16], ["to", 6.38], ["start", 6.64], ["from", 6.9], ["with", 7.16], ["its", 7.34], ["tag", 7.52], ["pinned.", 7.78], ["Post", 8.7], ["runs", 8.78], ["once", 9.06], ["during", 9.38], ["the", 9.64], ["build,", 9.8], ["so", 10.3], ["install", 10.36], ["your", 10.7], ["packages", 10.9], ["there", 11.28], ["at", 11.68], ["fixed", 11.98], ["versions.", 12.24]], "B52": [["The", 0.0], ["other", 0.12], ["sections,", 0.26], ["environment", 0.92], ["sets", 1.26], ["variables", 1.7], ["every", 2.2], ["time", 2.58], ["the", 2.88], ["container", 3.06], ["runs.", 3.36], ["Run", 4.3], ["script", 4.4], ["is", 4.64], ["what", 4.9], ["Aptainer", 5.08], ["run", 5.46], ["does,", 5.72], ["labels", 6.4], ["hold", 6.54], ["metadata.", 6.96], ["The", 7.98], ["versions", 8.06], ["in", 8.28], ["the", 8.56], ["example", 8.68], ["are", 9.06], ["placeholders,", 9.3], ["pin", 10.18], ["the", 10.28], ["ones", 10.42], ["you", 10.58], ["actually", 10.74], ["tested,", 11.1], ["then", 11.9], ["build", 12.02], ["it", 12.28], ["on", 12.5], ["your", 12.74], ["own", 12.88], ["machine.", 12.98]], "B53": [["If", 0.0], ["you", 0.12], ["already", 0.22], ["have", 0.46], ["a", 0.68], ["Docker", 1.1], ["file,", 1.1], ["build", 1.6], ["the", 1.72], ["Docker", 1.9], ["image", 2.16], ["on", 2.44], ["your", 2.64], ["own", 2.74], ["machine,", 2.86], ["then", 3.4], ["convert", 3.54], ["it.", 3.92], ["Docker", 4.8], ["builds", 4.8], ["the", 5.1], ["image.", 5.32], ["Aptainer", 6.22], ["reads", 6.5], ["it", 6.78], ["from", 6.98], ["Docker's", 7.18], ["local", 7.64], ["store", 7.86], ["and", 8.32], ["writes", 8.58], ["the", 8.82], ["SIF", 9.02], ["file,", 9.4], ["or", 10.18], ["push", 10.38], ["the", 10.56], ["image", 10.74], ["to", 10.94], ["a", 11.18], ["registry", 11.3], ["and", 11.6], ["pull", 12.08], ["it", 12.28], ["on", 12.38], ["the", 12.5], ["cluster.", 12.62]], "B54": [["A", 0.0], ["Dockerfile", 0.2], ["starts", 0.68], ["from", 1.0], ["a", 1.28], ["base", 1.4], ["operating", 1.58], ["system", 1.96], ["image", 2.38], ["and", 2.7], ["uses", 3.12], ["RUN", 3.36], ["lines", 3.86], ["to", 4.22], ["install", 4.52], ["packages.", 4.92], ["A", 6.24], ["good", 6.34], ["one", 6.5], ["ends", 6.66], ["with", 6.92], ["a", 7.14], ["line", 7.26], ["that", 7.5], ["imports", 7.72], ["your", 8.04], ["tool", 8.28], ["so", 8.56], ["the", 8.94], ["build", 9.08], ["fails", 9.26], ["early", 9.56], ["if", 9.9], ["the", 10.16], ["install", 10.28], ["is", 10.68], ["broken.", 10.92], ["Here", 11.82], ["is", 11.94], ["the", 12.08], ["shape", 12.24], ["from", 12.48], ["a", 12.78], ["real", 12.9], ["example.", 13.06]], "B55": [["Then", 0.0], ["two", 0.16], ["commands", 0.42], ["on", 0.82], ["your", 1.12], ["own", 1.22], ["machine.", 1.38], ["Docker", 2.38], ["build", 2.44], ["with", 2.74], ["a", 3.02], ["name", 3.14], ["and", 3.36], ["a", 3.52], ["version.", 3.62], ["Then", 4.52], ["Aptainer", 4.58], ["build", 5.08], ["reading", 5.36], ["the", 5.76], ["image", 6.0], ["from", 6.22], ["Docker's", 6.5], ["local", 6.98], ["store.", 7.18]], "B56": [["A", 0.0], ["third", 0.14], ["option", 0.34], ["is", 0.72], ["the", 0.94], ["Remote", 1.08], ["Builder.", 1.4], ["It", 2.3], ["needs", 2.32], ["a", 2.46], ["free", 2.62], ["account", 2.78], ["with", 3.12], ["the", 3.34], ["maker,", 3.46], ["and", 4.02], ["it", 4.06], ["uploads", 4.14], ["your", 4.58], ["recipe", 4.68], ["to", 4.98], ["a", 5.26], ["third", 5.4], ["party,", 5.6], ["so", 6.22], ["that", 6.34], ["is", 6.54], ["your", 6.68], ["decision,", 6.82], ["not", 7.46], ["an", 7.56], ["agent's.", 7.74], ["If", 8.52], ["you", 8.72], ["choose", 8.86], ["it,", 9.08], ["one", 9.36], ["flag", 9.48], ["does", 9.78], ["it.", 10.04], ["If", 10.46], ["a", 10.58], ["build", 10.7], ["fails,", 10.84], ["read", 11.46], ["the", 11.62], ["error", 11.78], ["text.", 11.96]], "B60": [["To", 0.0], ["get", 0.12], ["an", 0.24], ["image", 0.36], ["onto", 0.56], ["the", 0.76], ["cluster,", 0.94], ["pull", 1.44], ["it", 1.52], ["from", 1.64], ["a", 1.78], ["registry.", 1.88], ["Pulling", 2.8], ["is", 2.98], ["heavy,", 3.1], ["so", 3.52], ["do", 3.66], ["it", 3.82], ["on", 3.92], ["a", 4.0], ["compute", 4.14], ["node.", 4.36], ["This", 5.06], ["writes", 5.16], ["a", 5.38], ["SIF", 5.56], ["file", 5.92], ["named", 6.36], ["ubuntu", 6.66], ["underscore", 7.2], ["22", 7.82], [".04.", 8.4], ["Add", 9.7], ["a", 9.76], ["name", 9.9], ["flag", 10.06], ["to", 10.4], ["choose", 10.64], ["your", 10.86], ["own.", 11.04]], "B61": [["Other", 0.0], ["registries", 0.22], ["work", 0.76], ["the", 0.98], ["same", 1.18], ["way.", 1.42], ["Docker", 2.24], ["Hub", 2.24], ["for", 2.42], ["a", 2.64], ["tool", 2.74], ["like", 2.92], ["Gia", 3.18], ["TK,", 3.52], ["the", 4.28], ["NVIDIA", 4.32], ["catalog", 4.62], ["for", 5.04], ["GPU", 5.46], ["images,", 5.86], ["bio", 6.82], ["-containers", 6.82], ["for", 7.34], ["bioinformatics,", 7.6], ["and", 8.72], ["the", 8.78], ["SciLabs", 8.9], ["library.", 9.38], ["The", 10.46], ["first", 10.58], ["three", 10.74], ["name", 11.02], ["and", 11.22], ["exact", 11.36], ["version.", 11.68], ["The", 12.46], ["last", 12.56], ["has", 12.78], ["no", 13.0], ["tag", 13.22], ["at", 13.46], ["all,", 13.62], ["so", 13.98], ["pin", 14.12], ["one", 14.3], ["there", 14.52], ["too.", 14.72]], "B62": [["Always", 0.0], ["pin", 0.34], ["the", 0.56], ["tag,", 0.68], ["a", 1.18], ["tag", 1.28], ["called", 1.52], ["latest", 1.82], ["points", 2.14], ["at", 2.46], ["a", 2.72], ["different", 2.84], ["image", 3.06], ["next", 3.36], ["month.", 3.68], ["A", 4.44], ["pinned", 4.52], ["tag", 4.74], ["keeps", 5.1], ["pointing", 5.34], ["at", 5.68], ["the", 5.92], ["same", 6.06], ["one,", 6.28], ["so", 6.84], ["never", 7.08], ["use", 7.3], ["latest", 7.54], ["for", 7.84], ["anything", 8.12], ["you", 8.36], ["must", 8.66], ["reproduce", 8.84], ["and", 9.36], ["write", 9.72], ["the", 9.92], ["exact", 10.06], ["tag", 10.38], ["into", 10.76], ["your", 10.96], ["methods.", 11.1]], "B63": [["If", 0.0], ["you", 0.12], ["built", 0.22], ["the", 0.4], ["file", 0.58], ["on", 0.8], ["your", 0.96], ["own", 1.08], ["computer,", 1.24], ["copy", 1.94], ["it", 2.08], ["through", 2.3], ["the", 2.46], ["transfer", 2.62], ["node", 2.9], ["into", 3.2], ["project", 3.44], ["space.", 3.8], ["Check", 4.92], ["research", 5.16], ["computing's", 5.58], ["documentation", 6.2], ["for", 6.76], ["the", 7.18], ["current", 7.3], ["transfer", 7.52], ["host", 7.96], ["first.", 8.24], ["For", 9.12], ["smaller", 9.22], ["files,", 9.58], ["the", 10.38], ["open", 10.42], ["on", 10.72], ["demand", 10.9], ["files", 11.2], ["app", 11.64], ["uploads", 11.9], ["up", 12.44], ["to", 12.54], ["10", 12.74], ["gigabytes.", 12.94]], "B64": [["Keep", 0.0], ["images", 0.2], ["in", 0.48], ["your", 0.78], ["project's", 0.94], ["containers", 1.46], ["folder,", 1.82], ["not", 2.62], ["in", 2.68], ["Home.", 2.9], ["Project", 3.72], ["space", 3.98], ["is", 4.3], ["shared", 4.58], ["with", 4.8], ["your", 5.0], ["lab", 5.14], ["and", 5.42], ["is", 5.74], ["not", 5.86], ["covered", 6.1], ["by", 6.42], ["the", 6.7], ["75", 6.84], ["gigabyte", 7.52], ["Home", 8.04], ["quota.", 8.34], ["Keep", 9.18], ["the", 9.32], ["recipe", 9.46], ["next", 9.76], ["to", 10.04], ["the", 10.24], ["image,", 10.34], ["commit", 10.78], ["it,", 11.06], ["and", 11.46], ["archive", 11.58], ["the", 11.88], ["image", 12.1], ["with", 12.32], ["your", 12.54], ["data.", 12.68]], "B70": [["Aptainer", 0.0], ["keeps", 0.4], ["pulled", 0.7], ["layers", 0.98], ["in", 1.34], ["a", 1.56], ["hidden", 1.68], ["folder", 1.8], ["in", 2.2], ["your", 2.4], ["home", 2.5], ["directory,", 2.7], ["and", 3.58], ["a", 3.66], ["big", 3.74], ["pull", 3.92], ["can", 4.16], ["fill", 4.38], ["your", 4.56], ["quota,", 4.72], ["after", 5.26], ["which", 5.54], ["your", 5.74], ["on", 5.86], ["-demand", 6.02], ["sessions", 6.32], ["stop", 6.74], ["working.", 7.08], ["Point", 8.08], ["both", 8.26], ["locations", 8.54], ["at", 9.14], ["project", 9.4], ["space", 9.74], ["before", 10.12], ["any", 10.5], ["large", 10.7], ["pull.", 11.0], ["The", 11.74], ["cache", 11.88], ["is", 12.12], ["only", 12.36], ["a", 12.58], ["cache.", 12.74]], "B71": [["Before", 0.0], ["a", 0.24], ["long", 0.38], ["job,", 0.56], ["test", 1.06], ["by", 1.26], ["hand", 1.5], ["on", 1.74], ["a", 1.88], ["compute", 2.02], ["node,", 2.24], ["open", 2.8], ["a", 2.96], ["shell,", 3.1], ["run", 3.5], ["your", 3.6], ["commands,", 3.76], ["check", 4.34], ["they", 4.54], ["find", 4.76], ["their", 5.0], ["files,", 5.16], ["then", 6.06], ["print", 6.24], ["versions", 6.46], ["from", 6.8], ["inside.", 7.06], ["A", 7.98], ["job", 8.12], ["that", 8.34], ["finishes", 8.58], ["has", 8.82], ["not", 9.1], ["proved", 9.34], ["it,", 9.62], ["use", 9.9], ["the", 10.06], ["container,", 10.26], ["the", 10.96], ["binds,", 11.04], ["and", 11.6], ["the", 11.68], ["GPU", 11.78], ["you", 12.12], ["meant.", 12.42]], "B72": [["Record", 0.0], ["the", 0.32], ["image,", 0.5], ["write", 0.98], ["down", 1.12], ["the", 1.32], ["exact", 1.46], ["tag,", 1.72], ["and", 2.34], ["ideally", 2.38], ["the", 2.68], ["digest", 2.96], ["in", 3.34], ["your", 3.66], ["notes", 3.8], ["and", 4.0], ["methods.", 4.2], ["For", 5.08], ["a", 5.22], ["locally", 5.34], ["built", 5.62], ["image,", 5.88], ["the", 6.56], ["recipe", 6.58], ["plus", 6.88], ["the", 7.22], ["SIF", 7.46], ["file", 7.86], ["is", 8.28], ["the", 8.5], ["record.", 8.66], ["A", 9.5], ["checksum", 9.68], ["from", 10.04], ["SH,", 10.22], ["a", 10.76], ["256", 10.86], ["sum,", 11.4], ["lets", 12.02], ["a", 12.18], ["collaborator", 12.32], ["confirm", 12.72], ["they", 13.36], ["hold", 13.66], ["the", 13.86], ["same", 14.04], ["file.", 14.26]], "B73": [["Workflow", 0.0], ["managers", 0.4], ["like", 0.78], ["Nextflow", 1.18], ["and", 1.7], ["Snakemake", 1.9], ["can", 2.42], ["run", 2.68], ["each", 2.82], ["step", 3.1], ["of", 3.36], ["a", 3.5], ["pipeline", 3.62], ["in", 3.96], ["its", 4.24], ["own", 4.36], ["container", 4.56], ["so", 5.02], ["every", 5.5], ["tool", 5.82], ["carries", 6.08], ["its", 6.46], ["own", 6.72], ["version.", 6.94], ["That", 8.06], ["is", 8.22], ["a", 8.34], ["strong", 8.52], ["pattern", 8.76], ["for", 9.16], ["reproducible", 9.4], ["pipelines", 9.98], ["and", 10.56], ["research", 11.08], ["computing", 11.4], ["offers", 11.84], ["help", 12.3], ["setting", 12.54], ["it", 12.88], ["up.", 13.1]], "B74": [["On", 0.0], ["AICR,", 0.14], ["Aptainer", 1.08], ["and", 1.36], ["Singularity", 1.56], ["are", 2.12], ["both", 2.34], ["installed,", 2.56], ["but", 3.46], ["we", 3.64], ["have", 3.74], ["no", 3.88], ["documentation", 4.12], ["of", 4.64], ["container", 5.06], ["policy", 5.38], ["there,", 5.78], ["nothing", 6.4], ["on", 6.62], ["binds", 6.86], ["or", 7.18], ["storage.", 7.44], ["The", 8.4], ["partition", 8.5], ["fixes", 8.76], ["the", 9.2], ["GPU", 9.44], ["type,", 9.82], ["so", 10.32], ["you", 10.46], ["add", 10.58], ["no", 10.72], ["type", 10.94], ["to", 11.18], ["the", 11.38], ["Gres", 11.52], ["request.", 11.66], ["Do", 12.42], ["not", 12.5], ["copy", 12.66], ["Explorer's", 12.98], ["paths,", 13.58], ["ask", 14.12], ["AICR", 14.3], ["support.", 15.08]], "B80": [["Here", 0.0], ["is", 0.16], ["what", 0.32], ["we", 0.44], ["checked", 0.54], ["and", 0.82], ["what", 1.04], ["we", 1.14], ["only", 1.26], ["read.", 1.48], ["On", 2.22], ["the", 2.28], ["login", 2.42], ["node", 2.66], ["read", 3.08], ["-only,", 3.34], ["the", 3.96], ["path", 4.06], ["and", 4.26], ["version", 4.44], ["of", 4.7], ["apptainer", 4.88], ["that", 5.38], ["no", 5.56], ["module", 5.76], ["is", 6.1], ["needed", 6.34], ["in", 6.6], ["the", 6.86], ["GPU", 7.0], ["partition", 7.38], ["limits.", 7.86], ["We", 8.96], ["did", 9.12], ["not", 9.22], ["run", 9.38], ["a", 9.58], ["container,", 9.72], ["pull", 10.3], ["an", 10.46], ["image,", 10.58], ["build", 11.04], ["one,", 11.14], ["or", 11.64], ["submit", 11.7], ["a", 11.96], ["job.", 12.14], ["The", 12.68], ["rest", 12.78], ["came", 12.98], ["from", 13.24], ["the", 13.46], ["source.", 13.62]], "BVDT": [["Let's", 0.0], ["recap", 0.7], ["with", 0.94], ["Claude.", 1.2], ["A", 1.78], ["container", 1.84], ["is", 2.14], ["one", 2.38], ["sealed", 2.6], ["file", 2.92], ["holding", 3.28], ["a", 3.58], ["program", 3.76], ["and", 4.04], ["everything", 4.28], ["it", 4.52], ["needs.", 4.72], ["Aptainer", 5.48], ["runs", 5.7], ["it", 5.96], ["as", 6.12], ["you", 6.26], ["so", 6.42], ["it", 6.62], ["fits", 6.76], ["a", 6.9], ["shared", 7.06], ["cluster.", 7.28], ["Run", 8.16], ["on", 8.26], ["a", 8.4], ["compute", 8.56], ["node", 8.74], ["with", 8.98], ["exec", 9.16], ["shell", 9.46], ["or", 9.8], ["run", 9.96], ["add", 10.18], ["the", 10.46], ["NV", 10.6], ["flag", 10.8], ["for", 11.18], ["a", 11.44], ["GPU", 11.58], ["and", 11.84], ["bind", 12.22], ["every", 12.42], ["folder", 12.7], ["the", 13.02], ["job", 13.22], ["needs.", 13.46], ["Build", 14.24], ["where", 14.46], ["you", 14.62], ["have", 14.74], ["root", 14.9], ["never", 15.08], ["on", 15.36], ["the", 15.58], ["cluster", 15.7], ["then", 16.0], ["copy", 16.24], ["the", 16.48], ["finished", 16.68], ["file", 16.9], ["in.", 17.24], ["Pull", 17.88], ["on", 18.0], ["a", 18.12], ["compute", 18.22], ["node", 18.46], ["pin", 18.8], ["the", 19.04], ["tag", 19.2], ["and", 19.48], ["keep", 19.68], ["the", 19.84], ["recipe", 20.0], ["beside", 20.34], ["the", 20.68], ["image", 20.84], ["and", 21.14], ["record", 21.44], ["the", 21.72], ["image.", 21.9], ["And", 22.76], ["say", 22.84], ["plainly", 23.06], ["what", 23.42], ["you", 23.72], ["tested", 23.9], ["and", 24.22], ["what", 24.66], ["you", 24.8], ["only", 24.96], ["raid.", 25.28]], "BHTF": [["Your", 0.0], ["turn,", 0.14], ["paste", 0.54], ["this", 0.72], ["into", 0.94], ["Claude.", 1.18], ["Replace", 1.88], ["program", 1.88], ["with", 2.2], ["a", 2.52], ["tool", 2.64], ["you", 2.82], ["use.", 3.02], ["I", 3.66], ["run", 3.74], ["program", 3.94], ["on", 4.32], ["the", 4.54], ["Explorer", 4.66], ["cluster.", 5.04], ["Is", 5.82], ["there", 5.9], ["a", 6.04], ["module", 6.16], ["for", 6.42], ["it,", 6.74], ["a", 7.0], ["conda", 7.1], ["package,", 7.34], ["or", 7.78], ["a", 7.94], ["published", 8.02], ["container", 8.32], ["image?", 8.76], ["Check", 9.54], ["module", 9.68], ["avail", 10.04], ["in", 10.28], ["the", 10.46], ["registries.", 10.58], ["Tell", 11.26], ["me", 11.38], ["which", 11.52], ["option", 11.68], ["you", 11.96], ["would", 12.12], ["choose", 12.22], ["and", 12.5], ["why.", 12.7], ["And", 13.24], ["write", 13.34], ["the", 13.48], ["exact", 13.62], ["aptainer", 13.92], ["pull", 14.32], ["and", 14.6], ["aptainer", 14.78], ["exec", 15.16], ["commands", 15.5], ["with", 15.92], ["a", 16.08], ["pin", 16.2], ["tag", 16.38], ["in", 16.66], ["my", 16.86], ["project", 17.04], ["binds.", 17.42], ["Do", 18.44], ["not", 18.6], ["run", 18.74], ["anything", 18.94], ["on", 19.32], ["the", 19.52], ["login", 19.62], ["node", 19.88], ["and", 20.24], ["do", 20.46], ["not", 20.56], ["submit", 20.72], ["any", 21.08], ["job.", 21.28], ["Then", 22.18], ["check", 22.38], ["two", 22.6], ["things", 22.88], ["yourself.", 23.2], ["Did", 24.06], ["Claude", 24.22], ["name", 24.46], ["a", 24.68], ["pin", 24.84], ["tag", 25.02], ["in", 25.38], ["your", 25.58], ["project", 25.7], ["binds?", 26.08], ["And", 26.82], ["did", 26.94], ["it", 27.06], ["run", 27.16], ["nothing", 27.32], ["and", 27.62], ["submit", 27.84], ["nothing?", 28.12]], "BOUT": [["Scientific", 0.0], ["Reproducibility", 0.56], ["3", 1.4], ["Containers", 1.9], ["at", 2.68], ["Nick", 2.98], ["Baer", 3.24], ["-Brown", 3.54]]}


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


# ═════════════════════════════ PART A — B10 B11 B12 B20 B21 B22 B23 (+ shared helpers pA_*) ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pA_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pA_box(x, y, sc=1.0, tape=True):
    """The sealed container: a kraft box with one terracotta tape, centred on (x, y). The film's one box."""
    iso = Iso(0, 0, sc)
    g = job_box(iso, 0, 0, 0, 0.8) if tape else VGroup(iso.box(0, 0, 0, 0.8, 0.8, 0.64))
    return g.move_to([x, y, 0])


def pA_open_box(x, y, sc=1.0):
    """The same box, lid off. Returns (back, front); put contents between them."""
    iso = Iso(0, 0, sc)
    back, front = iso.open_box(0, 0, 0, 1.0, 1.0, 0.8)
    c = VGroup(back, front).get_center()
    back.shift(np.array([x, y, 0]) - c)
    front.shift(np.array([x, y, 0]) - c)
    return back, front


def pA_rack(x, y, sc=1.0, big=False):
    iso = Iso(0, 0, sc)
    st, lt = aicr_rack(iso) if big else explorer_rack(iso)
    g = VGroup(st, lt)
    g.lights = lt
    return g.move_to([x, y, 0])


def pA_laptop(x, y, s=1.0):
    bezel = RoundedRectangle(corner_radius=0.12 * s, width=2.1 * s, height=1.4 * s, fill_color=BOX_L, fill_opacity=1,
                             stroke_color=INK, stroke_width=5).move_to([x, y + 0.1 * s, 0])
    screen = Rectangle(width=1.7 * s, height=1.0 * s, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR2,
                       stroke_width=4).move_to([x, y + 0.15 * s, 0])
    base = RoundedRectangle(corner_radius=0.08 * s, width=2.6 * s, height=0.22 * s, fill_color=BOX_R, fill_opacity=1,
                            stroke_color=INK, stroke_width=5).move_to([x, y - 0.72 * s, 0])
    return VGroup(base, bezel, screen)


def pA_cloud(x, y, s=1.0):
    parts = VGroup(
        Circle(radius=0.55 * s, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x - 0.55 * s, y - 0.1 * s, 0]),
        Circle(radius=0.75 * s, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x + 0.05 * s, y + 0.15 * s, 0]),
        Circle(radius=0.55 * s, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x + 0.7 * s, y - 0.1 * s, 0]),
        Rectangle(width=1.8 * s, height=0.6 * s, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x + 0.08 * s, y - 0.4 * s, 0]))
    return parts


def pA_folder(x, y, w=1.6, h=1.1, fill=BOX_L):
    tab = Rectangle(width=w * 0.45, height=0.2, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x - w * 0.27, y + h / 2 + 0.08, 0])
    body = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    return VGroup(tab, body)


def pA_arrow(a, b, w=6, tip=0.3):
    return Arrow(a, b, color=INK, stroke_width=w, buff=0, tip_length=tip, max_tip_length_to_length_ratio=0.5)


def pA_dots(cx, cy, n=8, r=0.12, rad=1.9, seed=3):
    """Small plain dots for 'other users': deterministic ring-ish scatter."""
    out = VGroup()
    for i in range(n):
        a = 2 * PI * i / n + 0.3
        rr = rad * (0.8 + 0.25 * ((i * 7 + seed) % 3) / 2)
        out.add(Dot([cx + rr * np.cos(a) * 1.35, cy + rr * np.sin(a) * 0.9, 0], radius=r, color=DIM))
    return out


class B10_SealedBox(Scene):
    """Four parts drop into one box; it is taped shut; the sealed box visits a laptop, a cluster and a cloud unchanged."""
    def construct(self):
        self.add(pA_act_title("I · What A Container Is"))
        back, front = pA_open_box(-4.7, -1.45, 1.35)
        self.play(FadeIn(back), FadeIn(front), run_time=0.4)
        names = ["program", "libraries", "settings", "runtime"]
        chips = [chip(n, -4.7, 2.4 - 0.72 * i, size=32) for i, n in enumerate(names)]
        phrases = ["a program", "its libraries", "its settings", "small runtime"]
        for c, ph in zip(chips, phrases):
            hear(self, ph, lead=0.05)
            self.play(FadeIn(c, shift=DOWN * 0.15), run_time=0.3)
        for c in chips:
            self.play(ShrinkToCenter(c), run_time=0.22)
        sealed = pA_box(-4.7, -1.3, 1.35)
        self.play(FadeOut(back), FadeOut(front), FadeIn(sealed), run_time=0.35)
        tgt = [(pA_laptop(-1.1, -1.35, 0.85), -1.1, "laptop"), (pA_rack(1.9, -1.15, 0.95), 1.9, "cluster"), (pA_cloud(4.8, -1.0, 0.8), 4.8, "cloud")]
        labs = []
        hear(self, "Move that file", lead=0.0)
        for i, (obj, tx, nm) in enumerate(tgt):
            lab = T(nm, 34).move_to([tx, -2.75, 0])
            labs.append(lab)
            self.play(FadeIn(obj), FadeIn(lab), run_time=0.3)
            hear(self, ["laptop", "cluster", "cloud"][i], lead=0.25)
            self.play(sealed.animate.move_to([tx, 0.75, 0]), run_time=0.5)
        hear(self, "does not change", lead=0.3)
        ck = check(5.7, 0.8, s=0.3, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.35)
        done(self)


class B11_ThreeNames(Scene):
    """Docker, then the older name Singularity, then Apptainer (renamed from it) with the clusters that use it."""
    def construct(self):
        self.add(pA_act_title("I · What A Container Is"))
        dk = logo_chip("docker", -4.6, 0.7, h=1.6)
        dkl = T("laptops, cloud", 34).move_to([-4.6, -0.55, 0])
        sg = chip("singularity", 0.0, 0.7, mono=True, size=34)
        sgl = T("older name", 34).move_to([0.0, -0.55, 0])
        ap = logo_chip("apptainer", 4.6, 0.7, h=1.6)
        apl = T("Explorer, AICR", 34).move_to([4.6, -0.55, 0])
        self.add(dk)
        hear(self, "Docker is", lead=0.1)
        self.play(FadeIn(dk), run_time=0.3)
        self.play(FadeIn(dkl), run_time=0.3)
        hear(self, "Singularity is", lead=0.1)
        self.play(FadeIn(sg), FadeIn(sgl), run_time=0.4)
        hear(self, "current name", lead=0.5)
        self.play(FadeIn(ap), run_time=0.35)
        ar = pA_arrow([1.55, 0.7, 0], [3.5, 0.7, 0])
        rn = T("renamed", 34).move_to([2.55, 1.35, 0])
        self.play(Create(ar), FadeIn(rn), run_time=0.45)
        hear(self, "Explorer", lead=0.1)
        self.play(FadeIn(apl), run_time=0.3)
        hear(self, "use", lead=0.0)
        ck = check(4.6, -1.75, s=0.3, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.35)
        done(self)


class B12_WhyApptainer(Scene):
    """Docker's admin key into a shared rack is crossed out; Apptainer enters as you with one small key; it reads Docker images."""
    def construct(self):
        self.add(pA_act_title("I · What A Container Is"))
        rack = pA_rack(0.0, -0.55, 1.15, big=True)
        users = pA_dots(0.0, -0.55, n=9, rad=2.15)
        self.play(FadeIn(rack), FadeIn(users), run_time=0.5)
        dk = logo_chip("docker", -4.8, 1.35, h=1.3)
        key = key_obj(-3.9, 1.35, 0.55)
        kl = T("admin", 34).move_to([-3.0, 1.95, 0])
        hear(self, "Docker's normal setup", lead=0.1)
        self.play(FadeIn(dk), run_time=0.3)
        self.play(FadeIn(key), FadeIn(kl), run_time=0.3)
        self.play(key.animate.shift([1.3, -1.2, 0]), run_time=0.5)
        hear(self, "security problem", lead=0.3)
        xm = x_mark(-2.9, -0.35, r=0.4, w=11)
        self.play(Create(xm), run_time=0.3)
        ap = logo_chip("apptainer", 4.9, 1.9, h=1.3)
        bear = professor_bear("1x1", 1.5, seed="B12", x=5.0, y=-0.95)
        hear(self, "Apptainer runs", lead=0.1)
        self.play(FadeIn(ap), FadeIn(bear), run_time=0.4)
        skey = key_obj(3.6, 0.0, 0.32)
        ayou = T("as you", 34).move_to([4.9, 0.7, 0])
        self.play(FadeIn(skey), FadeIn(ayou), run_time=0.3)
        self.play(skey.animate.shift([-1.2, -0.4, 0]), run_time=0.45)
        hear(self, "Docker images", lead=0.35)
        img = chip("Docker image", -4.6, -2.65, size=30)
        ar = pA_arrow([-3.0, -2.65, 0], [3.8, -2.65, 0])
        self.play(FadeIn(img), Create(ar), run_time=0.5)
        ck = check(4.4, -2.6, s=0.28, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.3)
        done(self)


class B20_Reproducible(Scene):
    """A result tied to image 1.0; six months pass and the system updates; the box does not change; a collaborator gets the same."""
    def construct(self):
        self.add(pA_act_title("II · Why Use One"))
        res = paper(-5.0, 0.2, w=1.7, h=2.1, tilt=0.0)
        resl = T("result", 34).move_to([-5.0, 1.6, 0])
        rl = scribbles_on(res, n=3)
        box = pA_box(-1.9, 0.5, 1.05)
        tag = chip("image 1.0", -1.9, -0.95, mono=True, size=32)
        self.play(FadeIn(res), FadeIn(rl), FadeIn(resl), run_time=0.4)
        hear(self, "ties to", lead=0.2)
        self.play(FadeIn(box), FadeIn(tag), run_time=0.35)
        tie = Line([-4.1, 0.25, 0], [-2.85, 0.45, 0], color=INK, stroke_width=7)
        self.play(Create(tie), run_time=0.35)
        rack = pA_rack(1.5, -1.5, 0.95)
        rl2 = T("system", 34).move_to([1.5, -2.75, 0])
        hear(self, "six months", lead=0.15)
        self.play(FadeIn(rack), FadeIn(rl2), run_time=0.3)
        strip = Line([-0.2, 2.2, 0], [4.6, 2.2, 0], color=INK, stroke_width=6)
        ticks = VGroup(*[Line([x, 2.05, 0], [x, 2.35, 0], color=INK, stroke_width=5) for x in np.linspace(-0.2, 4.6, 7)])
        mo = T("six months", 34).move_to([2.2, 2.85, 0])
        dot = Dot([-0.2, 2.2, 0], radius=0.13, color=TERRA)
        self.play(Create(strip), Create(ticks), FadeIn(mo), FadeIn(dot), run_time=0.4)
        self.play(dot.animate.move_to([4.6, 2.2, 0]), run_time=0.9)
        hear(self, "system underneath", lead=0.2)
        new_top = pA_rack(1.5, -1.5, 0.95)
        upd = chip("updated", 1.5, 0.15, size=32)
        self.play(FadeIn(upd), Indicate(rack, color=INK, scale_factor=1.06), run_time=0.6)
        hear(self, "collaborator", lead=0.1)
        bear = professor_bear("1x1", 1.7, seed="B20", x=4.9, y=0.3)
        self.play(FadeIn(bear), run_time=0.35)
        ck = check(4.9, -1.1, s=0.3, color=TERRA, w=12)
        same = T("same software", 34).move_to([4.9, -1.85, 0])
        hear(self, "same software", lead=0.1)
        self.play(Create(ck), FadeIn(same), run_time=0.4)
        done(self)


class B21_PortableNoFights(Scene):
    """One box runs on laptop, rack and cloud; then two tools clash over one library until each gets its own box."""
    def construct(self):
        self.add(pA_act_title("II · Why Use One"))
        box = pA_box(-5.0, 1.55, 0.8)
        lap = pA_laptop(-1.7, 1.55, 0.6)
        rk = pA_rack(1.2, 1.6, 0.75)
        cl = pA_cloud(4.3, 1.65, 0.6)
        hear(self, "Portable", lead=0.1)
        self.play(FadeIn(box), run_time=0.3)
        for obj, x, ph in ((lap, -1.7, "your laptop"), (rk, 1.2, "Explorer"), (cl, 4.3, "cloud")):
            hear(self, ph, lead=0.35)
            a = pA_arrow([-4.2 if x < 0 else (-1.0 if x < 3 else 2.2), 1.55, 0], [x - 1.15, 1.55, 0], w=5, tip=0.25)
            self.play(FadeIn(obj), Create(a), run_time=0.35)
            self.play(Create(check(x + 1.25 if x < 3 else x + 1.0, 2.2, s=0.2, color=TERRA, w=9)), run_time=0.2)
        # no dependency fights
        hear(self, "dependency fights", lead=0.1)
        ta = chip("tool A", -4.4, -1.0, size=32)
        tb = chip("tool B", -4.4, -2.45, size=32)
        lib = Rectangle(width=1.9, height=1.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-0.6, -1.7, 0])
        libl = T("library", 34).move_to([-0.6, -2.65, 0])
        v1 = M("v1", 30).move_to([-2.35, -0.75, 0])
        v2 = M("v2", 30).move_to([-2.35, -2.7, 0])
        self.play(FadeIn(ta), FadeIn(tb), FadeIn(lib), FadeIn(libl), run_time=0.4)
        hear(self, "incompatible versions", lead=0.1)
        a1 = pA_arrow([-3.4, -1.0, 0], [-1.6, -1.4, 0], w=5, tip=0.25)
        a2 = pA_arrow([-3.4, -2.45, 0], [-1.6, -2.05, 0], w=5, tip=0.25)
        self.play(Create(a1), Create(a2), FadeIn(v1), FadeIn(v2), run_time=0.45)
        xm = x_mark(-0.6, -1.7, r=0.3, w=10)
        self.play(Create(xm), run_time=0.25)
        hear(self, "each get their own", lead=0.1)
        self.play(*[FadeOut(m) for m in (a1, a2, v1, v2, lib, libl, xm, ta, tb)], run_time=0.3)
        bx1, bx2 = pA_box(1.6, -1.55, 0.85), pA_box(4.4, -1.55, 0.85)
        t1 = chip("tool A  v1", 1.6, -2.7, size=30)
        t2 = chip("tool B  v2", 4.4, -2.7, size=30)
        self.play(FadeIn(bx1), FadeIn(bx2), FadeIn(t1), FadeIn(t2), run_time=0.4)
        hear(self, "neither one", lead=0.2)
        self.play(Create(check(3.0, -1.5, s=0.3, color=TERRA, w=12)), run_time=0.3)
        done(self)


class B22_ShareRegistries(Scene):
    """One file goes to a collaborator, an archive and a reviewer; four registries each hold stacks of ready-made images."""
    def construct(self):
        self.add(pA_act_title("II · Why Use One"))
        box = pA_box(-5.3, -0.4, 1.0)
        bear = professor_bear("1x1", 1.35, seed="B22", x=-2.5, y=0.55)
        arc = pA_folder(-2.5, -1.0, 1.3, 0.8)
        rev = paper(-2.5, -2.35, w=1.2, h=1.0)
        hear(self, "Shareable", lead=0.1)
        self.play(FadeIn(box), run_time=0.3)
        for obj, lab, y, ph in ((bear, "collaborator", 0.55, "collaborator"), (arc, "archive", -1.0, "archive"), (rev, "reviewer", -2.35, "reviewer")):
            hear(self, ph, lead=0.3)
            a = pA_arrow([-4.5, -0.4, 0], [-3.4, y, 0], w=5, tip=0.25)
            l = T(lab, 32).move_to([-1.2 + len(lab) * 0.09, y, 0])
            self.play(FadeIn(obj), Create(a), FadeIn(l), run_time=0.4)
        hear(self, "registries", lead=0.1)
        shelf = Line([1.2, 2.0, 0], [6.1, 2.0, 0], color=INK, stroke_width=6)
        self.play(Create(shelf), run_time=0.25)
        names = [("docker", None), (None, "quay.io"), ("nvidia", None), (None, "BioContainers")]
        ys = [1.1, 0.0, -1.1, -2.2]
        for (logo, mono), y in zip(names, ys):
            c = logo_chip(logo, 2.1, y, h=0.9) if logo else chip(mono, 2.7 if mono == "quay.io" else 2.9, y, mono=True, size=28)
            stack = VGroup(*[pA_box(5.15 + 0.4 * k, y, 0.28, tape=False) for k in range(3)])
            self.play(FadeIn(c), LaggedStart(*[FadeIn(s) for s in stack], lag_ratio=0.2), run_time=0.6)
        done(self)


class B23_TheLadder(Scene):
    """module, then conda, then container: an arrow climbs three steps; the top step carries large images."""
    def construct(self):
        self.add(pA_act_title("II · Why Use One"))
        step_x = [-4.2, 0.0, 4.2]
        step_y = [-1.9, -0.9, 0.1]
        steps = VGroup(*[Rectangle(width=3.6, height=1.4 + 1.0 * i, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
                         .move_to([x, -2.4 + (1.4 + i) / 2, 0]) for i, x in enumerate(step_x)])
        sl_ = [T("module", 36).move_to([-4.2, -2.95, 0]), T("conda", 36).move_to([0.0, -2.95, 0]), T("container", 36).move_to([4.2, -2.95, 0])]
        hear(self, "images are large", lead=0.3)
        self.play(FadeIn(steps), *[FadeIn(l) for l in sl_], run_time=0.5)
        big = T("large images", 34).move_to([4.2, 3.05, 0])
        self.play(FadeIn(big), run_time=0.3)
        mod = pA_rack(-4.2, -0.3, 0.5)
        hear(self, "module first", lead=0.1)
        self.play(FadeIn(mod), run_time=0.35)
        ar1 = pA_arrow([-3.2, 0.2, 0], [-1.1, 0.8, 0], w=6, tip=0.3)
        cd = logo_chip("anaconda", 0.0, 1.55, h=1.0)
        hear(self, "then conda", lead=0.15)
        self.play(Create(ar1), FadeIn(cd), run_time=0.45)
        ar2 = pA_arrow([1.0, 1.0, 0], [3.0, 1.6, 0], w=6, tip=0.3)
        bx = pA_box(4.2, 2.1, 0.55)
        hear(self, "then a container", lead=0.15)
        self.play(Create(ar2), FadeIn(bx), run_time=0.45)
        hear(self, "painful", lead=0.2)
        ring = Circle(radius=0.65, color=TERRA, stroke_width=7).move_to([4.2, 2.1, 0])
        self.play(Create(ring), run_time=0.4)
        self.play(FadeOut(ring), run_time=0.25)
        done(self)


# ═════════════════════════════ PART B — B32 B35 B38 B40 B50 ═════════════════════════════
# Uses the shared helpers pA_* from part A (they are in scope: the parts are concatenated).


def pB_pipe(a, b, w=18):
    return VGroup(Line(a, b, color=INK, stroke_width=w + 8), Line(a, b, color=BAR2, stroke_width=w))


class B32_ComputeNode(Scene):
    """The box is crossed out on the shared login node; srun --pty bash asks for a compute node, its lights come on, the box runs there."""
    def construct(self):
        login = pA_rack(-4.2, -0.6, 0.9)
        ll = T("login node", 36).move_to([-4.2, -2.1, 0])
        comp = pA_rack(3.6, -0.5, 1.15)
        cl = T("compute node", 36).move_to([3.6, -2.25, 0])
        self.add(pA_act_title("III · Running A Container"))
        self.play(FadeIn(login), FadeIn(ll), FadeIn(comp), FadeIn(cl), run_time=0.5)
        box = pA_box(-4.2, 0.75, 0.75)
        hear(self, "never on the login", lead=0.3)
        self.play(FadeIn(box), run_time=0.3)
        xm = x_mark(-2.7, 0.55, r=0.35, w=11)
        self.play(Create(xm), run_time=0.3)
        hear(self, "shared by everyone", lead=0.1)
        dots = pA_dots(-4.2, -0.6, n=8, rad=1.35)
        self.play(FadeIn(dots), run_time=0.4)
        hear(self, "Ask", lead=0.1)
        cmdc = chip("srun --pty bash", -2.0, 2.0, mono=True, size=32)
        self.play(FadeIn(cmdc), run_time=0.3)
        self.play(cmdc.animate.move_to([2.7, 2.0, 0]), run_time=0.7)
        self.play(*[d.animate.set_color(TERRA) for d in comp.lights], run_time=0.4)
        hear(self, "work inside", lead=0.1)
        self.play(FadeOut(box), FadeOut(xm), FadeOut(dots), run_time=0.25)
        box2 = pA_box(3.6, 1.1, 0.75)
        self.play(FadeIn(box2), run_time=0.3)
        self.play(Create(check(5.0, 1.2, s=0.3, color=TERRA, w=12)), run_time=0.35)
        done(self)


class B35_NvBridge(Scene):
    """The container carries its own CUDA but is cut off from the driver; the --nv flag lays a bridge from the node's driver in."""
    def construct(self):
        self.add(pA_act_title("III · Running A Container"))
        rack = pA_rack(-4.2, -1.9, 0.95)
        rl = T("GPU node", 36).move_to([-4.2, -3.2, 0])
        drv = logo_chip("nvidia", -4.2, -0.1, h=1.1)
        dl = T("driver", 36).move_to([-4.2, 0.85, 0])
        frame = Rectangle(width=4.2, height=2.5, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.0, 0.5, 0])
        cu = chip("CUDA", 3.0, 0.5, mono=True, size=34)
        cl = T("container", 36).move_to([3.0, -1.1, 0])
        self.play(FadeIn(rack), FadeIn(rl), FadeIn(drv), FadeIn(dl), run_time=0.4)
        hear(self, "container can carry", lead=0.1)
        self.play(FadeIn(frame), FadeIn(cl), run_time=0.35)
        self.play(FadeIn(cu), run_time=0.3)
        hear(self, "still needs", lead=0.2)
        gap = DashedLine([-3.3, -0.1, 0], [0.7, 0.3, 0], color=KRAFT_DEEP, stroke_width=6)
        self.play(Create(gap), run_time=0.4)
        xm = x_mark(-0.9, 0.1, r=0.3, w=10)
        no = T("no GPU", 34).move_to([-0.9, 0.9, 0])
        self.play(Create(xm), FadeIn(no), run_time=0.3)
        hear(self, "flag passes", lead=0.2)
        self.play(FadeOut(gap), FadeOut(xm), FadeOut(no), run_time=0.25)
        br = pB_pipe([-3.3, -0.1, 0], [0.9, -0.1, 0])
        nv = chip("--nv", -1.2, 0.6, mono=True, size=34)
        self.play(Create(br), run_time=0.45)
        self.play(FadeIn(nv), run_time=0.25)
        hear(self, "no link", lead=0.1)
        self.play(Create(check(-0.8, -1.0, s=0.3, color=TERRA, w=12)), run_time=0.35)
        done(self)


class B38_TimeLimits(Scene):
    """Partition limits as bars (8 h, 2 h, 2 h); a two-GPU, 12 hour request grows past the 8 h line and is crossed out."""
    def construct(self):
        self.add(pA_act_title("III · Running A Container"))
        x0, u = -2.0, 0.6
        X = lambda h: x0 + u * h
        axis = Line([x0, -2.0, 0], [X(12), -2.0, 0], color=INK, stroke_width=5)
        ticks = VGroup(*[Line([X(h), -2.0, 0], [X(h), -2.18, 0], color=INK, stroke_width=4) for h in range(0, 13, 2)])
        nums = VGroup(*[T(str(h), 32).move_to([X(h), -2.55, 0]) for h in range(0, 13, 4)])
        hrs = T("hours", 32).move_to([X(12) - 0.1, -3.05, 0])
        self.play(Create(axis), Create(ticks), FadeIn(nums), FadeIn(hrs), run_time=0.5)
        rows = [("gpu-interactive", 2, 1.75), ("gpu-short", 2, 0.9), ("gpu", 8, 0.05)]
        hear(self, "partition limit", lead=0.2)
        for name, h, y in rows:
            lab = M(name, 28).move_to([x0 - 0.3 - M(name, 28).width / 2, y, 0])
            bar = Rectangle(width=u * h, height=0.5, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([X(h / 2), y, 0])
            val = M(f"{h}:00:00", 28).move_to([X(h) + 0.25 + 0.7, y, 0])
            self.play(FadeIn(lab), GrowFromEdge(bar, LEFT), FadeIn(val), run_time=0.45)
        line = DashedLine([X(8), 2.3, 0], [X(8), -2.0, 0], color=KRAFT_DEEP, stroke_width=5)
        self.play(Create(line), run_time=0.3)
        hear(self, "published example", lead=0.3)
        rl = M("--gres=gpu:2", 28).move_to([x0 - 0.3 - M("--gres=gpu:2", 28).width / 2, -1.0, 0])
        req = Rectangle(width=u * 12, height=0.5, fill_color=KRAFT_DEEP, fill_opacity=1, stroke_width=0).move_to([X(6), -1.0, 0])
        self.play(FadeIn(rl), GrowFromEdge(req, LEFT), run_time=1.0)
        hear(self, "cannot run", lead=0.25)
        self.play(Create(x_mark(X(12) + 0.45, -1.0, r=0.3, w=10)), run_time=0.3)
        done(self)


class B40_WhatItSees(Scene):
    """Home slides into the container by itself; /projects and /scratch wait outside until --bind carries each in."""
    def construct(self):
        self.add(pA_act_title("IV · Binding Folders"))
        frame = Rectangle(width=4.6, height=4.6, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.2, -0.2, 0])
        fl = T("container", 36).move_to([3.2, 2.45, 0])
        slots = VGroup(*[DashedVMobject(Rectangle(width=3.0, height=1.05, color=BAR1, stroke_width=4).move_to([3.2, y, 0]), num_dashes=24)
                         for y in (1.2, -0.2, -1.6)])
        self.play(FadeIn(frame), FadeIn(fl), FadeIn(slots), run_time=0.5)
        hear(self, "own file system", lead=0.3)
        specs = [("home", 1.2, None), ("/projects", -0.2, "mono"), ("/scratch", -1.6, "mono")]
        folders = []
        for nm, y, kind in specs:
            f = pA_folder(-5.0, y, 1.5, 0.9)
            lab = (M(nm, 32) if kind else T(nm, 36)).move_to([-3.35 + (0.55 if kind else 0.0), y, 0])
            if nm == "home":
                f.add(Dot([-5.0, y, 0], radius=0.11, color=TERRA))
            folders.append(VGroup(f, lab))
        self.play(*[FadeIn(g) for g in folders], run_time=0.45)
        hear(self, "home directory", lead=0.2)
        self.play(folders[0].animate.move_to([3.2, 1.2, 0]), run_time=0.6)
        self.play(FadeOut(slots[0]), run_time=0.15)
        hear(self, "slash projects", lead=0.2)
        for g in folders[1:]:
            self.play(g.animate.shift(RIGHT * 0.25), run_time=0.2)
            self.play(g.animate.shift(LEFT * 0.25), run_time=0.2)
        hear(self, "bind each", lead=0.3)
        for g, y in zip(folders[1:], (-0.2, -1.6)):
            br = pB_pipe([-1.5, y, 0], [1.2, y, 0], w=14)
            c = chip("--bind", -0.1, y + 0.7, mono=True, size=28)
            self.play(Create(br), FadeIn(c), run_time=0.35)
            self.play(FadeOut(slots[2 if y < -1 else 1]), run_time=0.15)
            self.play(g.animate.move_to([3.2, y, 0]), run_time=0.4)
        done(self)


class B50_BuildCopyRun(Scene):
    """Build on your own computer (root), copy the finished file, store it in project space, run it on a compute node as you."""
    def construct(self):
        self.add(pA_act_title("V · Building An Image"))
        lap = pA_laptop(-4.6, -0.4, 0.8)
        ll = T("your computer", 34).move_to([-4.6, -1.7, 0])
        dk = logo_chip("docker", -5.3, 1.9, h=0.9)
        ap = logo_chip("apptainer", -3.9, 1.9, h=0.9)
        root = chip("root", -4.6, 0.9, mono=True, size=30)
        hear(self, "cannot build", lead=0.1)
        self.play(FadeIn(lap), FadeIn(ll), run_time=0.35)
        hear(self, "administrator rights", lead=0.2)
        self.play(FadeIn(root), FadeIn(dk), FadeIn(ap), run_time=0.4)
        hear(self, "build on a machine", lead=0.1)
        box = pA_box(-2.6, -0.2, 0.85)
        box.set_z_index(6)
        self.play(GrowFromCenter(box), run_time=0.4)
        fol = pA_folder(0.3, -0.35, 1.7, 1.0)
        fl = T("project space", 34).move_to([0.3, -1.6, 0])
        rack = pA_rack(4.0, -0.7, 1.0)
        rl = T("compute node", 34).move_to([4.0, -2.2, 0])
        hear(self, "Copy the finished", lead=0.2)
        a1 = pA_arrow([-1.8, -0.2, 0], [-0.7, -0.2, 0], w=5, tip=0.25)
        cp = T("copy", 34).move_to([-1.25, 0.35, 0])
        self.play(Create(a1), FadeIn(cp), FadeIn(fol), FadeIn(fl), run_time=0.45)
        self.play(box.animate.move_to([0.3, -0.1, 0]), run_time=0.5)
        hear(self, "store it", lead=0.1)
        self.play(Create(check(1.5, 0.35, s=0.28, color=TERRA, w=11)), run_time=0.4)
        hear(self, "run it there", lead=0.3)
        a2 = pA_arrow([1.4, -0.3, 0], [2.6, -0.3, 0], w=5, tip=0.25)
        self.play(Create(a2), FadeIn(rack), FadeIn(rl), run_time=0.4)
        self.play(box.animate.move_to([4.0, 0.75, 0]), run_time=0.5)
        bear = professor_bear("1x1", 1.3, seed="B50", x=5.5, y=1.9)
        ay = T("as yourself", 32).move_to([5.2, 2.95, 0])
        self.play(FadeIn(bear), FadeIn(ay), run_time=0.3)
        done(self)


# ═════════════════════════════ PART C — B53 B62 B64 B72 B73 B74 B80 ═════════════════════════════


class B53_DockerRoute(Scene):
    """Dockerfile -> docker build -> image -> apptainer build -> .sif; a second branch pushes the image to a registry and pulls it."""
    def construct(self):
        self.add(pA_act_title("V · Building An Image"))
        pg = paper(-5.2, 0.6, w=1.3, h=1.6)
        pgl = M("Dockerfile", 26).move_to([-5.2, -0.55, 0])
        sc = scribbles_on(pg, n=3, inset=0.22, gap=0.3)
        hear(self, "Docker file", lead=0.1)
        self.play(FadeIn(pg), FadeIn(sc), FadeIn(pgl), run_time=0.4)
        a1 = pA_arrow([-4.5, 0.6, 0], [-3.85, 0.6, 0], w=5, tip=0.22)
        dk = logo_chip("docker", -2.9, 0.6, h=1.3)
        dkl = M("docker build", 26).move_to([-2.8, -0.5, 0])
        hear(self, "build the Docker image", lead=0.2)
        self.play(Create(a1), FadeIn(dk), FadeIn(dkl), run_time=0.45)
        a2 = pA_arrow([-2.0, 0.6, 0], [-1.4, 0.6, 0], w=5, tip=0.22)
        im = pA_box(-0.6, 0.6, 0.7)
        iml = T("image", 32).move_to([-0.6, -0.4, 0])
        self.play(Create(a2), FadeIn(im), FadeIn(iml), run_time=0.4)
        hear(self, "Docker builds the image", lead=0.1)
        self.play(dk.animate.scale(1.1), run_time=0.2)
        self.play(dk.animate.scale(1 / 1.1), run_time=0.2)
        hear(self, "Aptainer reads", lead=0.1)
        a3 = pA_arrow([0.2, 0.6, 0], [0.85, 0.6, 0], w=5, tip=0.22)
        ap = logo_chip("apptainer", 1.8, 0.6, h=1.3)
        apl = M("apptainer build", 26).move_to([1.8, -0.5, 0])
        self.play(Create(a3), FadeIn(ap), FadeIn(apl), run_time=0.45)
        a4 = pA_arrow([2.7, 0.6, 0], [3.7, 0.6, 0], w=5, tip=0.22)
        sif = pA_box(4.5, 0.6, 0.7)
        sifl = M(".sif", 30).move_to([4.5, -0.4, 0])
        hear(self, "writes the", lead=0.2)
        self.play(Create(a4), FadeIn(sif), FadeIn(sifl), run_time=0.45)
        hear(self, "push the image", lead=0.2)
        a5 = pA_arrow([-0.6, -0.9, 0], [-0.6, -1.5, 0], w=5, tip=0.22)
        cl = pA_cloud(-0.6, -2.2, 0.55)
        cll = T("registry", 32).move_to([-0.6, -3.15, 0])
        self.play(Create(a5), FadeIn(cl), FadeIn(cll), run_time=0.45)
        hear(self, "pull it on the cluster", lead=0.4)
        a6 = pA_arrow([0.5, -2.2, 0], [2.2, -2.2, 0], w=5, tip=0.25)
        pl = M("pull", 28).move_to([1.35, -1.75, 0])
        rk = pA_rack(3.6, -2.15, 0.7)
        self.play(Create(a6), FadeIn(pl), FadeIn(rk), run_time=0.5)
        done(self)


class B62_PinTheTag(Scene):
    """:latest follows a different image next month; a pinned tag keeps pointing at the same one; the pinned tag goes into the methods."""
    def construct(self):
        self.add(pA_act_title("VI · Getting An Image Onto The Cluster"))
        h1 = T("today", 36).move_to([-2.7, 2.1, 0])
        h2 = T("next month", 36).move_to([2.9, 2.1, 0])
        sep = DashedLine([0.1, 2.4, 0], [0.1, -1.6, 0], color=KRAFT_DEEP, stroke_width=4)
        self.play(FadeIn(h1), FadeIn(h2), Create(sep), run_time=0.4)

        def tagrow(y, tagtxt, x_tag, x_box, boxlabel, taped=True):
            t = chip(tagtxt, x_tag, y, mono=True, size=28)
            ar = pA_arrow([x_tag + t.width / 2 + 0.1, y, 0], [x_box - 0.9, y, 0], w=5, tip=0.22)
            bx = pA_box(x_box, y, 0.62, tape=taped)
            lb = T(boxlabel, 32).move_to([x_box, y - 0.75, 0])
            return t, ar, bx, lb

        hear(self, "latest points", lead=0.2)
        l1 = tagrow(1.15, ":latest", -4.6, -1.6, "A")
        p1 = tagrow(-0.55, ":4.5.0.0", -4.7, -1.6, "A")
        self.play(*[FadeIn(m) for m in l1], *[FadeIn(m) for m in p1], run_time=0.6)
        hear(self, "different image", lead=0.2)
        l2 = tagrow(1.15, ":latest", 1.4, 4.6, "B", taped=False)
        self.play(*[FadeIn(m) for m in l2], run_time=0.5)
        self.play(Create(x_mark(6.0, 1.15, r=0.25, w=9)), run_time=0.25)
        hear(self, "pinned tag keeps", lead=0.1)
        p2 = tagrow(-0.55, ":4.5.0.0", 1.5, 4.6, "A")
        self.play(*[FadeIn(m) for m in p2], run_time=0.5)
        self.play(Create(check(6.0, -0.55, s=0.25, color=TERRA, w=10)), run_time=0.3)
        hear(self, "methods", lead=0.4)
        pm = paper(-0.2, -2.45, w=1.9, h=1.2)
        pml = T("methods", 32).move_to([-2.0, -2.45, 0])
        self.play(FadeIn(pm), FadeIn(pml), run_time=0.3)
        tg = chip(":4.5.0.0", 1.5, -0.55, mono=True, size=28)
        self.add(tg)
        self.play(tg.animate.scale(0.8).move_to([-0.2, -2.45, 0]), run_time=0.6)
        done(self)


class B64_WhereToKeep(Scene):
    """Not in home (75 GB quota); in project space, the .sif and its .def side by side, committed, archived with the data."""
    def construct(self):
        self.add(pA_act_title("VI · Getting An Image Onto The Cluster"))
        home = pA_folder(-4.7, 0.9, 1.6, 1.0)
        hl = T("home", 36).move_to([-4.7, 0.0, 0])
        track = Rectangle(width=2.6, height=0.3, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([-4.7, -0.65, 0])
        fill = Rectangle(width=1.9, height=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.35 + 0.0, -0.65, 0]).align_to(track, LEFT)
        q = M("75 GB", 30).move_to([-4.7, -1.2, 0])
        hear(self, "not in home", lead=0.3)
        self.play(FadeIn(home), FadeIn(hl), FadeIn(track), run_time=0.4)
        self.play(FadeIn(fill), FadeIn(q), run_time=0.3)
        sif = pA_box(-2.3, 2.1, 0.7)
        sl = M(".sif", 28).move_to([-2.3, 1.3, 0])
        self.play(FadeIn(sif), FadeIn(sl), run_time=0.3)
        self.play(sif.animate.move_to([-3.5, 1.6, 0]), sl.animate.move_to([-3.5, 0.9, 0]), run_time=0.35)
        self.play(Create(x_mark(-2.4, 1.3, r=0.3, w=10)), run_time=0.25)
        hear(self, "Project space", lead=0.2)
        self.play(FadeOut(sif), FadeOut(sl), run_time=0.2)
        fol = pA_folder(2.0, 1.4, 2.4, 1.5)
        fl = M("containers/", 30).move_to([2.0, 0.3, 0])
        self.play(FadeIn(fol), FadeIn(fl), run_time=0.4)
        sif2 = pA_box(1.4, 1.4, 0.62)
        self.play(FadeIn(sif2), run_time=0.3)
        hear(self, "recipe", lead=0.2)
        df = paper(4.1, 1.4, w=0.95, h=1.15)
        dfs = scribbles_on(df, n=3, inset=0.18, gap=0.26)
        dfl = M(".def", 28).move_to([4.1, 0.3, 0])
        self.play(FadeIn(df), FadeIn(dfs), FadeIn(dfl), run_time=0.35)
        hear(self, "commit it", lead=0.2)
        gt = chip("git", 5.6, 1.4, mono=True, size=30)
        self.play(FadeIn(gt), run_time=0.3)
        hear(self, "archive the image", lead=0.2)
        arc = pA_folder(2.4, -1.8, 2.6, 1.2)
        arl = T("archive with data", 34).move_to([2.4, -2.85, 0])
        self.play(FadeIn(arc), FadeIn(arl), run_time=0.4)
        self.play(sif2.animate.scale(0.6).move_to([1.8, -1.8, 0]), df.animate.scale(0.6).move_to([3.2, -1.8, 0]), run_time=0.6)
        done(self)


class B72_RecordIt(Scene):
    """Tag, digest and recipe-plus-image are stamped into the notes; sha256sum shows the same file on both sides."""
    def construct(self):
        self.add(pA_act_title("VII · Habits That Keep It Honest"))
        notes = paper(-5.2, 0.2, w=1.9, h=2.7)
        nl = VGroup(*[scribble(-5.9, 1.2 - i * 0.4, 1.4 * (0.62 if i == 3 else 1.0), amp=0.11) for i in range(4)]); nl.rotate(notes.tilt, about_point=[-5.2, 0.2, 0]) if abs(notes.tilt) > 1e-3 else None
        nt = T("notes", 40).move_to([-5.2, 1.85, 0])
        self.play(FadeIn(notes), FadeIn(nl), FadeIn(nt), run_time=0.4)
        for txt, y, ph in (("tag", 1.0, "exact tag"), ("digest", 0.2, "the digest"), (".def + .sif", -0.6, "recipe plus")):
            hear(self, ph, lead=0.15)
            c = chip(txt, -2.2, y, mono=(txt != "tag" and txt != "digest"), size=38)
            self.play(FadeIn(c, shift=LEFT * 0.3), run_time=0.35)
        mine = pA_box(1.1, 1.2, 0.85)
        ml = T("mine", 40).move_to([1.1, 0.1, 0])
        theirs = pA_box(5.1, 1.2, 0.85)
        tl = T("theirs", 40).move_to([5.1, 0.1, 0])
        hear(self, "A checksum", lead=0.1)
        self.play(FadeIn(mine), FadeIn(ml), FadeIn(theirs), FadeIn(tl), run_time=0.4)
        cs = chip("sha256sum myimage.sif", 3.1, -1.3, mono=True, size=34)
        self.play(FadeIn(cs), run_time=0.3)
        hear(self, "confirm they hold", lead=0.2)
        eq = T("=", 110).move_to([3.1, 1.2, 0])
        self.play(FadeIn(eq), run_time=0.3)
        self.play(Create(check(3.1, 2.3, s=0.3, color=TERRA, w=12)), run_time=0.35)
        done(self)


class B73_WorkflowManager(Scene):
    """Two workflow managers run a three-step pipeline; every step is its own box carrying its own version."""
    def construct(self):
        self.add(pA_act_title("VII · Habits That Keep It Honest"))
        nf = chip("nextflow", -2.4, 2.0, mono=True, size=32)
        sm = chip("snakemake", 2.4, 2.0, mono=True, size=32)
        hear(self, "Workflow managers", lead=0.1)
        self.play(FadeIn(nf), FadeIn(sm), run_time=0.35)
        belt = Line([-6.0, -0.3, 0], [6.0, -0.3, 0], color=INK, stroke_width=6)
        xs = [-4.0, 0.0, 4.0]
        steps = []
        for i, x in enumerate(xs):
            bx = pA_box(x, 0.45, 0.95)
            lab = T(f"step {i + 1}", 34).move_to([x, -1.1, 0])
            steps.append((bx, lab))
        a1 = pA_arrow([-1.2, 1.7, 0], [-3.4, 1.35, 0], w=4, tip=0.2)
        a2 = pA_arrow([1.2, 1.7, 0], [3.4, 1.35, 0], w=4, tip=0.2)
        hear(self, "each step", lead=0.2)
        self.play(Create(belt), Create(a1), Create(a2), run_time=0.4)
        work = Dot([-6.0, -0.3, 0], radius=0.14, color=TERRA)
        self.add(work)
        vers = ["v1", "v2", "v3"]
        hear(self, "its own container", lead=0.3)
        for (bx, lab), x, v in zip(steps, xs, vers):
            self.play(FadeIn(bx), FadeIn(lab), run_time=0.3)
            self.play(work.animate.move_to([x, -0.3, 0]), run_time=0.45)
            if x == xs[0]:
                hear(self, "every tool carries", lead=0.1)
            vc = chip(v, x, -2.1, mono=True, size=30)
            self.play(FadeIn(vc), run_time=0.25)
        self.play(work.animate.move_to([6.0, -0.3, 0]), run_time=0.4)
        done(self)


class B74_AicrContainers(Scene):
    """AICR has both tools; policy is not documented; the partition fixes the GPU type; Explorer's paths are not copied."""
    def construct(self):
        self.add(pA_act_title("VII · Habits That Keep It Honest"))
        rack = pA_rack(-4.0, -0.2, 1.0, big=True)
        rl = T("AICR", 40).move_to([-4.0, -2.4, 0])
        self.play(FadeIn(rack), FadeIn(rl), run_time=0.4)
        hear(self, "installed", lead=1.0)
        ap = logo_chip("apptainer", -0.2, 1.8, h=1.1)
        sg = chip("singularity", -0.2, 0.35, mono=True, size=30)
        self.play(FadeIn(ap), FadeIn(sg), run_time=0.4)
        self.play(Create(check(1.0, 1.8, s=0.25, color=TERRA, w=10)), Create(check(1.9, 0.35, s=0.25, color=TERRA, w=10)), run_time=0.35)
        hear(self, "no documentation", lead=0.2)
        pl = T("container policy", 34).move_to([4.2, 2.3, 0])
        nd = chip("not documented", 4.2, 1.5, size=32)
        self.play(FadeIn(pl), FadeIn(nd), run_time=0.4)
        hear(self, "The partition", lead=0.2)
        gr = chip("--gres=gpu:1", 4.0, 0.2, mono=True, size=28)
        nt = T("no GPU type", 34).move_to([4.0, -0.7, 0])
        self.play(FadeIn(gr), FadeIn(nt), run_time=0.4)
        hear(self, "Do not copy", lead=0.15)
        pj = chip("/projects", 0.3, -2.0, mono=True, size=28)
        self.play(FadeIn(pj), run_time=0.3)
        self.play(Create(x_mark(1.95, -2.0, r=0.28, w=9)), run_time=0.25)
        hear(self, "ask", lead=0.1)
        sup = chip("ask AICR support", 4.4, -2.1, size=30)
        self.play(FadeIn(sup), run_time=0.35)
        done(self)


class B80_CheckedVsRead(Scene):
    """Three read-only checks stamp in on the left; four things only read from the source stamp in on the right."""
    def construct(self):
        self.add(pA_act_title("VIII · What Was Checked"))
        hl = T("checked on the login node", 34).move_to([-3.1, 2.3, 0])
        hr = T("only read, not run", 34).move_to([3.4, 2.3, 0])
        left_items = [("apptainer 1.4.5", True, 1.4), ("no module needed", False, 0.4), ("GPU time limits", False, -0.6)]
        right_items = [("run a container", 1.5), ("pull an image", 0.6), ("build an image", -0.3), ("submit a job", -1.2)]
        slots = VGroup()
        for _, _, y in left_items:
            slots.add(DashedVMobject(Rectangle(width=4.3, height=0.8, color=BAR1, stroke_width=3).move_to([-3.1, y, 0]), num_dashes=30))
        for _, y in right_items:
            slots.add(DashedVMobject(Rectangle(width=3.6, height=0.8, color=BAR1, stroke_width=3).move_to([3.4, y, 0]), num_dashes=26))
        self.play(FadeIn(hl), FadeIn(hr), FadeIn(slots), run_time=0.5)
        hear(self, "read only", lead=0.2)
        for txt, mono, y in left_items:
            c = chip(txt, -3.1, y, mono=mono or True, size=28)
            self.play(FadeIn(c), run_time=0.3)
            self.play(Create(check(-0.45, y, s=0.2, color=TERRA, w=9)), run_time=0.2)
        hear(self, "did not run", lead=0.2)
        for txt, y in right_items:
            c = chip(txt, 3.4, y, mono=True, size=28)
            self.play(FadeIn(c), run_time=0.3)
        hear(self, "came from", lead=0.2)
        fs = chip("from the source", 3.4, -2.3, size=32)
        self.play(FadeIn(fs), run_time=0.35)
        done(self)


for _cls in (B10_SealedBox, B11_ThreeNames, B12_WhyApptainer, B20_Reproducible, B21_PortableNoFights, B22_ShareRegistries, B23_TheLadder, B32_ComputeNode, B35_NvBridge, B38_TimeLimits, B40_WhatItSees, B50_BuildCopyRun, B53_DockerRoute, B62_PinTheTag, B64_WhereToKeep, B72_RecordIt, B73_WorkflowManager, B74_AicrContainers, B80_CheckedVsRead):
    _cls.play = ST.play
