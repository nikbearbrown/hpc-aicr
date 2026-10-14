"""scenes.py — Scientific Reproducibility II: Version Control (lecture). The show-tell iso_kit is pasted below verbatim (Gate A copies
only this file), then the pacing/midpoint-guard helpers, the film cast, the measured word times (_ASR, injected
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
_ASR = {"BOPEN": [["Research", 0.0], ["computing", 0.36], ["on", 0.78], ["Explorer", 1.02], ["and", 1.44], ["AICR,", 1.74], ["scientific", 3.1], ["reproducibility", 3.34], ["2,", 4.2], ["version", 4.88], ["control.", 5.04], ["Learn", 6.12], ["to", 6.24], ["use", 6.48], ["Git", 6.7], ["so", 6.86], ["that", 7.08], ["every", 7.2], ["result", 7.46], ["you", 7.8], ["produce", 8.04], ["on", 8.36], ["a", 8.68], ["laptop", 8.78], ["or", 9.06], ["on", 9.44], ["a", 9.54], ["cluster", 9.66], ["can", 10.0], ["be", 10.3], ["tied", 10.42], ["to", 10.64], ["the", 10.82], ["exact", 10.92], ["code", 11.26], ["that", 11.62], ["made", 11.88], ["it.", 12.1]], "BIDEA": [["Hallo,", 0.7], ["this", 1.3], ["is", 1.42], ["Liam", 1.6], ["in", 1.94], ["for", 2.2], ["Bear.", 2.36], ["First", 3.14], ["a", 3.22], ["correction.", 3.4], ["Version", 4.38], ["control", 4.38], ["is", 4.8], ["not", 5.0], ["a", 5.16], ["backup", 5.28], ["folder.", 5.52], ["It", 6.36], ["is", 6.48], ["a", 6.58], ["timeline", 6.7], ["of", 6.98], ["snapshots", 7.24], ["you", 7.62], ["can", 7.9], ["search,", 8.08], ["compare", 8.56], ["and", 8.82], ["rewind", 9.04], ["and", 9.46], ["each", 9.72], ["snapshot", 9.88], ["can", 10.38], ["be", 10.58], ["tied", 10.7], ["to", 10.9], ["the", 11.1], ["result", 11.2], ["it", 11.46], ["produced.", 11.66]], "BDEFS": [["Six", 0.0], ["terms,", 0.28], ["repository,", 0.88], ["the", 1.66], ["project", 1.74], ["folder", 2.08], ["plus", 2.44], ["its", 2.72], ["history.", 2.96], ["Commit", 4.16], ["a", 4.18], ["saved", 4.46], ["snapshot", 4.7], ["of", 5.12], ["your", 5.34], ["files.", 5.46], ["Branch", 6.34], ["a", 6.4], ["movable", 6.64], ["name", 7.0], ["for", 7.2], ["one", 7.42], ["line", 7.64], ["of", 7.86], ["commits.", 8.0], ["Tag", 8.82], ["a", 8.88], ["fixed", 9.14], ["name", 9.38], ["for", 9.62], ["one", 9.86], ["commit.", 10.08], ["The", 10.68], ["git", 10.76], ["ignore", 10.88], ["file,", 11.24], ["a", 11.84], ["list", 11.92], ["of", 12.06], ["what", 12.22], ["git", 12.36], ["skips,", 12.56], ["and", 13.18], ["a", 13.3], ["slurm", 13.44], ["job,", 13.8], ["your", 14.22], ["request", 14.34], ["for", 14.64], ["compute", 14.9], ["node.", 15.18]], "B10": [["Six", 0.0], ["months", 0.24], ["after", 0.46], ["you", 0.76], ["submit", 0.9], ["a", 1.1], ["paper,", 1.32], ["a", 1.9], ["reviewer", 1.9], ["asks,", 2.16], ["what", 3.0], ["threshold", 3.04], ["did", 3.48], ["you", 3.72], ["use", 3.88], ["for", 4.06], ["low", 4.24], ["count", 4.42], ["filtering?", 4.68], ["Without", 5.76], ["version", 5.96], ["control,", 6.3], ["you", 6.94], ["open", 6.98], ["a", 7.2], ["folder", 7.36], ["like", 7.6], ["this,", 7.9], ["and", 8.32], ["you", 8.42], ["guess", 8.54], ["from", 8.72], ["the", 8.94], ["file", 9.08], ["names,", 9.36], ["which", 10.04], ["script", 10.22], ["made", 10.52], ["which", 10.86], ["table.", 11.08]], "B11": [["Version", 0.0], ["Control", 0.34], ["replaces", 0.72], ["that", 1.12], ["folder", 1.48], ["with", 1.76], ["one", 2.04], ["script", 2.28], ["and", 2.6], ["a", 2.84], ["timeline.", 2.96], ["Every", 3.88], ["change", 4.08], ["carries", 4.38], ["a", 4.68], ["date,", 4.88], ["an", 5.32], ["author,", 5.36], ["and", 5.88], ["a", 5.92], ["message.", 6.02], ["You", 6.88], ["can", 6.94], ["mark", 7.08], ["the", 7.26], ["exact", 7.44], ["code", 7.72], ["behind", 8.06], ["a", 8.38], ["figure,", 8.54], ["give", 9.08], ["each", 9.24], ["experiment", 9.44], ["its", 9.92], ["own", 10.2], ["branch,", 10.4], ["and", 10.94], ["undo", 11.02], ["a", 11.24], ["bad", 11.4], ["change.", 11.58]], "B12": [["The", 0.0], ["program", 0.14], ["is", 0.42], ["called", 0.66], ["Git", 0.92], ["and", 1.18], ["its", 1.42], ["idea", 1.56], ["is", 1.92], ["simple.", 2.16], ["It", 2.84], ["stores", 2.9], ["snapshots,", 3.22], ["not", 4.16], ["edits.", 4.22], ["A", 5.2], ["commit", 5.3], ["is", 5.54], ["a", 5.74], ["full", 5.88], ["picture", 6.06], ["of", 6.32], ["your", 6.52], ["files", 6.64], ["at", 6.92], ["one", 7.16], ["moment,", 7.38], ["linked", 7.9], ["to", 8.06], ["the", 8.24], ["commit", 8.36], ["before", 8.58], ["it.", 8.98]], "B13": [["A", 0.0], ["branch", 0.14], ["is", 0.36], ["a", 0.56], ["movable", 0.66], ["name", 1.02], ["for", 1.24], ["one", 1.48], ["chain", 1.68], ["of", 1.94], ["commits,", 2.14], ["main", 2.94], ["here,", 2.98], ["and", 3.52], ["an", 3.58], ["experiment", 3.66], ["that", 4.16], ["split", 4.44], ["off.", 4.74], ["A", 5.74], ["tag", 5.86], ["is", 6.12], ["a", 6.3], ["fixed", 6.44], ["name", 6.62], ["for", 6.9], ["one", 7.12], ["commit,", 7.34], ["like", 7.88], ["a", 8.02], ["flag", 8.18], ["you", 8.4], ["plant", 8.6], ["on", 8.86], ["the", 9.04], ["code", 9.18], ["behind", 9.48], ["a", 9.84], ["paper.", 10.0]], "B14": [["Your", 0.0], ["files", 0.14], ["live", 0.46], ["in", 0.72], ["three", 0.9], ["places.", 1.1], ["The", 1.88], ["working", 1.92], ["tree", 2.16], ["is", 2.44], ["what", 2.58], ["you", 2.74], ["see", 2.88], ["in", 3.16], ["edit.", 3.38], ["The", 4.04], ["staging", 4.16], ["area", 4.42], ["is", 4.78], ["the", 5.06], ["list", 5.18], ["of", 5.32], ["changes", 5.48], ["going", 5.88], ["into", 6.2], ["the", 6.44], ["next", 6.56], ["snapshot", 6.78], ["and", 7.32], ["git", 7.7], ["add", 7.84], ["puts", 8.1], ["a", 8.36], ["change", 8.5], ["there.", 8.76], ["The", 9.6], ["repository", 9.64], ["holds", 10.08], ["the", 10.62], ["saved", 10.88], ["snapshots", 11.14], ["and", 11.72], ["git", 12.1], ["commit", 12.26], ["saves", 12.56], ["them.", 12.9]], "B15": [["Four", 0.0], ["moments", 0.2], ["where", 0.48], ["this", 0.7], ["saves", 0.86], ["you.", 1.14], ["A", 1.72], ["reviewer", 1.76], ["asks", 2.0], ["if", 2.38], ["you", 2.6], ["tried", 2.72], ["another", 2.94], ["value.", 3.18], ["Open", 3.8], ["the", 3.94], ["branch", 4.1], ["where", 4.34], ["you", 4.56], ["did.", 4.68], ["A", 5.2], ["postdoc", 5.32], ["leaves,", 5.78], ["clone", 6.28], ["the", 6.48], ["repository,", 6.64], ["and", 7.42], ["read", 7.52], ["the", 7.7], ["readme.", 7.84], ["A", 8.5], ["cluster", 8.64], ["setting", 8.86], ["changed,", 9.24], ["diff", 9.94], ["against", 10.0], ["the", 10.24], ["last", 10.44], ["commit.", 10.7], ["Publishing", 11.76], ["the", 11.76], ["code", 12.0], ["with", 12.18], ["the", 12.36], ["paper,", 12.5], ["tag", 12.96], ["a", 13.16], ["release", 13.3], ["on", 13.54], ["GitHub.", 13.76]], "B20": [["The", 0.0], ["example", 0.14], ["is", 0.44], ["a", 0.7], ["small", 0.92], ["R", 1.08], ["in", 1.32], ["a", 1.44], ["sequencing", 1.54], ["project,", 1.88], ["a", 2.84], ["table", 2.9], ["of", 3.16], ["read", 3.34], ["counts,", 3.5], ["one", 4.08], ["row", 4.26], ["per", 4.44], ["gene,", 4.66], ["three", 5.24], ["control", 5.36], ["columns,", 5.74], ["and", 6.38], ["three", 6.5], ["treated.", 6.68], ["One", 7.48], ["script", 7.72], ["drops", 8.0], ["low", 8.38], ["count", 8.64], ["genes,", 8.86], ["works", 9.44], ["out", 9.64], ["a", 9.84], ["fold", 9.96], ["change,", 10.16], ["and", 10.64], ["writes", 10.76], ["a", 10.98], ["summary.", 11.14], ["Any", 11.98], ["analysis", 12.1], ["follows", 12.54], ["the", 13.02], ["same", 13.34], ["Git", 13.62], ["workflow.", 13.82]], "B21": [["This", 0.0], ["is", 0.16], ["the", 0.3], ["script", 0.44], ["we", 0.68], ["will", 0.88], ["track,", 1.0], ["strict", 1.64], ["mode", 1.78], ["and", 2.1], ["input", 2.34], ["and", 2.66], ["output", 2.84], ["in", 3.18], ["a", 3.4], ["parameters", 3.52], ["block", 3.88], ["at", 4.24], ["the", 4.4], ["top,", 4.54], ["where", 5.0], ["the", 5.02], ["one", 5.14], ["tunable", 5.3], ["value", 5.72], ["lives,", 6.02], ["min", 6.7], ["count", 6.76], ["10,", 7.0], ["genes", 8.0], ["with", 8.22], ["a", 8.48], ["low", 8.6], ["mean", 8.74], ["count", 8.98], ["are", 9.28], ["skipped,", 9.44], ["the", 10.1], ["rest", 10.16], ["are", 10.34], ["called", 10.52], ["up", 10.74], ["down", 10.98], ["or", 11.3], ["not", 11.56], ["significant", 11.76], ["by", 12.26], ["fold", 12.58], ["change.", 12.88]], "B22": [["Start", 0.0], ["tracking", 0.24], ["before", 0.56], ["the", 0.84], ["first", 0.98], ["run,", 1.18], ["not", 1.72], ["after.", 1.76], ["Get", 2.84], ["in", 2.86], ["it", 2.98], ["makes", 3.12], ["a", 3.3], ["hidden", 3.48], ["dot", 3.62], ["get", 3.96], ["folder,", 4.18], ["gets", 4.78], ["database", 4.98], ["one", 5.38], ["per", 5.76], ["project.", 5.98], ["A", 6.78], ["caution,", 6.86], ["depending", 7.52], ["on", 7.72], ["your", 7.96], ["settings,", 8.08], ["the", 8.62], ["first", 8.66], ["branch", 8.88], ["may", 9.18], ["be", 9.34], ["called", 9.48], ["master", 9.7], ["as", 10.12], ["it", 10.38], ["was", 10.48], ["here", 10.6], ["and", 10.88], ["the", 11.08], ["later", 11.18], ["steps", 11.36], ["say", 11.66], ["main.", 11.96], ["So", 12.7], ["rename", 12.74], ["it", 13.02], ["first.", 13.22]], "B30": [["Track", 0.0], ["the", 0.22], ["code", 0.38], ["that", 0.56], ["makes", 0.7], ["results,", 0.92], ["not", 1.62], ["the", 1.68], ["results", 1.82], ["themselves.", 2.14], ["Big", 3.3], ["raw", 3.38], ["data", 3.6], ["lives", 3.94], ["in", 4.16], ["project", 4.38], ["storage", 4.7], ["outside", 5.2], ["the", 5.76], ["repository,", 5.98], ["and", 6.9], ["passwords", 7.1], ["or", 7.52], ["tokens", 7.8], ["never", 8.2], ["go", 8.56], ["in", 8.78], ["at", 8.92], ["all.", 9.04], ["Whatever", 9.74], ["git", 10.0], ["should", 10.2], ["skip", 10.42], ["goes", 10.74], ["in", 11.04], ["a", 11.24], ["file", 11.36], ["named", 11.62], [".gitignore.", 11.92]], "B31": [["Here", 0.0], ["is", 0.2], ["the", 0.34], ["source's", 0.54], ["version", 0.94], ["of", 1.16], ["that", 1.38], ["file.", 1.54], ["It", 2.26], ["ignores", 2.34], ["the", 2.64], ["whole", 2.92], ["results", 3.12], ["folder,", 3.52], ["then", 4.2], ["lists", 4.32], ["two", 4.54], ["files", 4.82], ["to", 5.16], ["let", 5.38], ["back", 5.52], ["in,", 5.78], ["the", 6.24], ["summary", 6.38], ["table", 6.7], ["and", 7.04], ["the", 7.34], ["run", 7.44], ["log.", 7.62]], "B32": [["Run", 0.0], ["that", 0.22], ["in", 0.42], ["real", 0.58], ["git", 0.84], ["and", 1.08], ["it", 1.3], ["fails.", 1.44], ["Git", 2.36], ["never", 2.38], ["looks", 2.66], ["inside", 2.92], ["an", 3.34], ["ignored", 3.5], ["folder", 3.82], ["so", 4.26], ["it", 4.62], ["never", 4.72], ["reads", 4.92], ["the", 5.2], ["to", 5.42], ["allow", 5.62], ["lines.", 5.86], ["The", 6.82], ["add", 6.88], ["is", 7.06], ["refused", 7.22], ["and", 7.68], ["check", 8.08], ["ignore", 8.26], ["names", 8.62], ["line", 8.94], ["2", 9.18], ["of", 9.46], ["the", 9.6], ["file", 9.7], ["as", 10.0], ["the", 10.2], ["reason.", 10.36]], "B33": [["The", 0.0], ["fix", 0.12], ["is", 0.3], ["one", 0.5], ["character.", 0.72], ["Ignore", 1.74], ["the", 1.76], ["folder's", 1.98], ["contents", 2.32], ["with", 2.72], ["slash", 3.08], ["star,", 3.38], ["not", 3.9], ["the", 4.02], ["folder.", 4.18], ["Now", 5.04], ["the", 5.22], ["folder", 5.38], ["itself", 5.64], ["is", 5.92], ["not", 6.2], ["ignored,", 6.42], ["so", 7.02], ["the", 7.14], ["two", 7.26], ["allow", 7.44], ["lines", 7.7], ["work", 8.02], ["in", 8.26], ["both", 8.52], ["files", 8.74], ["stage.", 9.12]], "B34": [["A", 0.0], ["second", 0.14], ["trap", 0.4], ["in", 0.66], ["the", 0.82], ["same", 0.94], ["file.", 1.16], ["The", 1.92], ["source", 2.0], ["puts", 2.22], ["a", 2.48], ["comment", 2.66], ["after", 2.9], ["the", 3.18], ["pattern", 3.38], ["on", 3.7], ["the", 3.92], ["same", 4.08], ["line.", 4.3], ["Git", 5.24], ["does", 5.24], ["not", 5.42], ["read", 5.62], ["that", 5.8], ["as", 6.02], ["a", 6.14], ["comment.", 6.28], ["The", 6.8], ["text", 6.9], ["becomes", 7.18], ["part", 7.5], ["of", 7.82], ["the", 7.94], ["pattern,", 8.04], ["which", 8.4], ["then", 8.62], ["matches", 8.84], ["nothing.", 9.2], ["So", 9.92], ["the", 10.06], ["ad", 10.18], ["is", 10.36], ["still", 10.52], ["refused.", 10.72], ["Give", 11.62], ["every", 11.68], ["comment", 11.98], ["a", 12.28], ["line", 12.44], ["of", 12.66], ["its", 12.8], ["own.", 12.92]], "B35": [["Write", 0.0], ["the", 0.2], ["readme", 0.36], ["before", 0.68], ["the", 0.96], ["first", 1.14], ["commit,", 1.4], ["list", 2.18], ["the", 2.28], ["requirements,", 2.46], ["the", 3.26], ["exact", 3.3], ["commands", 3.64], ["to", 4.04], ["reproduce", 4.3], ["the", 4.68], ["result,", 4.92], ["including", 5.58], ["the", 5.82], ["tag", 6.06], ["to", 6.22], ["checkout", 6.44], ["and", 6.7], ["the", 7.14], ["parameters.", 7.24], ["It", 8.42], ["is", 8.6], ["a", 8.7], ["contract", 8.82], ["with", 9.14], ["anyone", 9.38], ["who", 9.6], ["clones", 9.88], ["the", 10.14], ["repository,", 10.36], ["and", 11.4], ["that", 11.48], ["includes", 11.62], ["you", 11.94], ["in", 12.24], ["a", 12.36], ["year.", 12.48]], "B40": [["The", 0.0], ["habit", 0.12], ["for", 0.34], ["every", 0.56], ["result,", 0.82], ["change", 1.4], ["a", 1.54], ["value,", 1.72], ["run", 2.18], ["the", 2.3], ["script,", 2.46], ["look", 2.98], ["at", 3.08], ["the", 3.2], ["output,", 3.3], ["then", 3.92], ["commit", 4.02], ["the", 4.26], ["code", 4.44], ["and", 4.68], ["the", 4.88], ["result", 5.0], ["together.", 5.28], ["Repeat", 6.24], ["before", 6.56], ["a", 7.06], ["paper", 7.18], ["goes", 7.4], ["out,", 7.66], ["tag", 8.08], ["the", 8.28], ["commit.", 8.48], ["That", 9.08], ["ties", 9.22], ["each", 9.52], ["result", 9.76], ["to", 10.1], ["the", 10.3], ["code", 10.4], ["and", 10.66], ["the", 10.86], ["parameters", 10.96], ["behind", 11.4], ["it.", 11.92]], "B41": [["Three", 0.0], ["commands", 0.22], ["you", 0.5], ["will", 0.7], ["use", 0.82], ["dozens", 1.0], ["of", 1.26], ["times", 1.48], ["a", 1.72], ["day.", 1.9], ["Status", 2.62], ["shows", 2.62], ["what", 2.92], ["changed.", 3.2], ["Add", 4.26], ["chooses", 4.34], ["what", 4.6], ["goes", 4.88], ["into", 5.1], ["the", 5.34], ["next", 5.46], ["snapshot.", 5.68], ["That", 6.44], ["is", 6.52], ["the", 6.64], ["staging", 6.82], ["area.", 7.08], ["Commit", 7.86], ["saves", 7.88], ["it.", 8.2], ["The", 8.9], ["source", 8.98], ["stages", 9.16], ["everything", 9.6], ["with", 9.98], ["a", 10.28], ["dot.", 10.4], ["In", 10.86], ["a", 10.92], ["folder", 11.02], ["holding", 11.28], ["data,", 11.66], ["tokens", 12.56], ["or", 12.56], ["logs,", 12.88], ["name", 13.42], ["the", 13.52], ["files", 13.7], ["instead.", 14.0]], "B42": [["Now", 0.0], ["run", 0.2], ["it,", 0.44], ["the", 0.76], ["log", 0.82], ["names", 1.02], ["the", 1.32], ["commit", 1.54], ["and", 1.78], ["the", 1.96], ["counts", 2.04], ["are", 2.26], ["there,", 2.44], ["200", 2.84], ["genes,", 3.08], ["199", 3.68], ["kept,", 4.16], ["but", 5.06], ["look", 5.14], ["at", 5.28], ["the", 5.42], ["date", 5.5], ["error", 5.66], ["in", 5.96], ["the", 6.2], ["empty", 6.28], ["brackets.", 6.54], ["Dash", 7.84], ["dash", 7.92], ["ISO", 8.22], ["is", 8.72], ["a", 8.9], ["GNU", 9.02], ["option,", 9.3], ["so", 9.96], ["it", 10.08], ["fails", 10.18], ["on", 10.38], ["a", 10.56], ["Mac.", 10.68], ["It", 11.18], ["should", 11.26], ["work", 11.4], ["on", 11.6], ["Linux,", 11.78], ["but", 12.2], ["we", 12.32], ["did", 12.4], ["not", 12.5], ["run", 12.68], ["this", 12.88], ["on", 13.06], ["a", 13.22], ["cluster.", 13.34], ["On", 13.98], ["a", 14.08], ["Mac,", 14.2], ["use", 14.58], ["date", 14.7], ["dash", 14.96], ["u", 15.26], ["with", 15.5], ["a", 15.66], ["format.", 15.76]], "B43": [["Then", 0.0], ["commit", 0.18], ["the", 0.38], ["results", 0.54], ["together", 0.84], ["with", 1.22], ["the", 1.48], ["code", 1.62], ["that", 1.84], ["made", 2.0], ["them,", 2.2], ["and", 2.66], ["let", 2.82], ["the", 2.94], ["message", 3.08], ["say", 3.34], ["what", 3.6], ["the", 3.82], ["run", 3.94], ["was.", 4.1], ["The", 4.94], ["log", 5.06], ["inside", 5.28], ["this", 5.7], ["commit", 5.98], ["names", 6.24], ["the", 6.58], ["commit", 6.78], ["before", 7.0], ["it,", 7.38], ["so", 7.7], ["the", 7.88], ["result", 8.0], ["carries", 8.28], ["its", 8.58], ["own", 8.88], ["receipt.", 9.08], ["That", 9.92], ["only", 10.06], ["works", 10.3], ["because", 10.56], ["the", 10.88], ["fixed", 11.08], ["gitignore", 11.34], ["file", 11.86], ["lets", 12.34], ["the", 12.62], ["two", 12.84], ["files", 13.04], ["through.", 13.4]], "B44": [["Two", 0.0], ["habits", 0.18], ["make", 0.46], ["a", 0.74], ["history", 0.88], ["worth", 1.14], ["reading,", 1.42], ["one", 2.24], ["logical", 2.4], ["change", 2.82], ["per", 3.24], ["commit", 3.5], ["if", 3.82], ["the", 4.1], ["message", 4.22], ["needs", 4.5], ["the", 4.8], ["word", 5.02], ["and", 5.26], ["make", 5.48], ["two", 5.68], ["commits,", 5.94], ["and", 6.84], ["a", 7.06], ["consistent", 7.16], ["message", 7.52], ["style,", 7.98], ["a", 8.52], ["type,", 8.56], ["a", 9.08], ["scope,", 9.12], ["and", 9.54], ["a", 9.6], ["short", 9.74], ["summary", 9.94], ["so", 10.38], ["git", 10.84], ["log", 11.04], ["reads", 11.32], ["like", 11.64], ["a", 11.84], ["change", 11.98], ["log", 12.24], ["and", 12.54], ["grep", 12.78], ["finds", 12.94], ["things.", 13.3]], "B45": [["Before", 0.0], ["you", 0.22], ["commit", 0.34], ["anything,", 0.52], ["look", 1.1], ["at", 1.12], ["what", 1.24], ["you", 1.36], ["are", 1.5], ["about", 1.62], ["to", 1.84], ["commit.", 2.02], ["Change", 2.84], ["the", 2.96], ["threshold", 3.12], ["and", 3.46], ["git", 3.78], ["diff", 3.92], ["shows", 4.14], ["it", 4.38], ["line", 4.54], ["by", 4.7], ["line,", 4.9], ["one", 5.42], ["line", 5.6], ["out,", 5.84], ["one", 6.24], ["line", 6.34], ["in.", 6.6], ["The", 7.26], ["source", 7.44], ["edits", 7.66], ["with", 7.98], ["sed", 8.24], ["and", 8.52], ["that", 8.74], ["form", 8.88], ["fails", 9.14], ["on", 9.42], ["a", 9.62], ["mac", 9.74], ["which", 9.9], ["wants", 10.16], ["an", 10.38], ["empty", 10.52], ["backup", 10.76], ["suffix", 11.1], ["after", 11.52], ["dash", 11.9], ["i.", 12.16], ["We", 12.78], ["use", 12.88], ["the", 13.06], ["mac", 13.2], ["form.", 13.4]], "B46": [["Rerun", 0.0], ["with", 0.32], ["the", 0.5], ["new", 0.62], ["value,", 0.76], ["197", 1.3], ["genes", 1.72], ["now", 2.48], ["pass,", 2.76], ["two", 3.22], ["fewer.", 3.36], ["Commit", 4.22], ["the", 4.4], ["changed", 4.58], ["script", 4.88], ["and", 5.28], ["the", 5.58], ["new", 5.68], ["results", 5.82], ["together", 6.2], ["with", 6.56], ["a", 6.88], ["message", 7.0], ["that", 7.26], ["names", 7.56], ["the", 7.82], ["change.", 8.04], ["Three", 8.94], ["commits", 9.14], ["now,", 9.42], ["each", 9.98], ["one", 10.12], ["a", 10.36], ["documented", 10.48], ["decision.", 10.96]], "B47": [["The", 0.0], ["log", 0.12], ["is", 0.32], ["your", 0.5], ["audit", 0.64], ["trail,", 0.9], ["stats", 1.6], ["shows", 1.64], ["which", 1.9], ["files", 2.14], ["each", 2.46], ["commit", 2.68], ["touched.", 3.0], ["Grep", 4.04], ["finds", 4.1], ["every", 4.46], ["commit", 4.78], ["that", 5.08], ["mentions", 5.3], ["a", 5.56], ["word,", 5.76], ["so", 6.16], ["the", 6.3], ["reviewer's", 6.42], ["question", 6.86], ["now", 7.12], ["has", 7.5], ["an", 7.72], ["answer", 7.84], ["in", 8.06], ["two", 8.26], ["lines.", 8.44], ["Dash", 9.4], ["P", 9.48], ["shows", 9.78], ["every", 10.02], ["change", 10.4], ["to", 10.7], ["one", 10.94], ["file,", 11.12], ["and", 11.78], ["Git", 11.92], ["Blame", 12.0], ["says", 12.36], ["who", 12.62], ["wrote", 12.84], ["each", 13.04], ["line", 13.24], ["and", 13.5], ["when.", 13.74]], "B50": [["A", 0.0], ["reviewer", 0.14], ["asks", 0.4], ["you", 0.74], ["to", 0.94], ["try", 1.06], ["a", 1.22], ["fold", 1.38], ["change", 1.64], ["cut", 1.98], ["off", 2.26], ["of", 2.46], ["1", 2.62], [".5", 2.88], ["instead", 3.5], ["of", 3.86], ["2.", 4.02], ["You", 4.64], ["do", 4.84], ["not", 4.94], ["know", 5.08], ["yet", 5.28], ["whether", 5.46], ["it", 5.68], ["goes", 5.88], ["in", 6.06], ["the", 6.26], ["paper,", 6.36], ["so", 6.94], ["never", 7.2], ["edit", 7.44], ["the", 7.7], ["working", 7.86], ["script", 8.1], ["for", 8.46], ["a", 8.74], ["speculative", 8.84], ["change.", 9.26], ["Make", 10.2], ["a", 10.32], ["branch,", 10.46], ["a", 11.02], ["parallel", 11.08], ["version", 11.46], ["that", 11.88], ["leaves", 12.16], ["main", 12.46], ["untouched.", 12.74]], "B51": [["One", 0.0], ["command", 0.2], ["makes", 0.5], ["the", 0.76], ["branch", 0.98], ["and", 1.22], ["moves", 1.46], ["you", 1.68], ["onto", 1.86], ["it.", 2.08], ["Branch", 2.82], ["list", 2.82], ["shows", 3.08], ["where", 3.36], ["you", 3.6], ["are", 3.76], ["with", 3.96], ["a", 4.14], ["star.", 4.3], ["Change", 5.18], ["the", 5.3], ["two", 5.46], ["cutoffs", 5.6], ["in", 5.96], ["the", 6.16], ["script", 6.26], ["and", 6.52], ["git", 6.86], ["diff", 6.98], ["shows", 7.2], ["exactly", 7.48], ["that.", 7.9], ["The", 8.6], ["cutoff", 8.68], ["of", 8.9], ["two", 9.14], ["becomes", 9.38], ["1", 9.68], [".5", 10.04], ["and", 10.66], ["the", 10.92], ["lower", 11.04], ["one,", 11.22], ["0", 11.58], [".5,", 11.78], ["becomes", 12.3], ["0", 12.54], [".67.", 12.84]], "B52": [["Run", 0.0], ["it,", 0.22], ["check", 0.56], ["it,", 0.62], ["commit", 0.88], ["it", 1.04], ["on", 1.16], ["the", 1.28], ["branch,", 1.4], ["then", 2.02], ["switch", 2.14], ["back", 2.38], ["to", 2.7], ["main", 2.9], ["and", 3.12], ["its", 3.34], ["script", 3.46], ["is", 3.74], ["exactly", 3.98], ["as", 4.34], ["you", 4.68], ["left", 4.8], ["it.", 5.0], ["The", 5.5], ["cutoff", 5.54], ["is", 5.76], ["still", 6.02], ["2,", 6.22], ["the", 6.86], ["experiment", 6.96], ["lives", 7.42], ["only", 7.8], ["on", 8.12], ["the", 8.4], ["branch.", 8.52]], "B53": [["Merge", 0.0], ["when", 0.24], ["the", 0.38], ["idea", 0.5], ["belongs.", 0.8], ["The", 1.7], ["dash", 1.72], ["dash", 1.92], ["no", 2.2], ["FF", 2.52], ["flag", 2.86], ["keeps", 3.24], ["a", 3.48], ["visible", 3.94], ["merge", 3.94], ["point", 4.22], ["and", 4.54], ["the", 4.9], ["graph", 5.0], ["shows", 5.26], ["the", 5.52], ["line", 5.74], ["leaving", 5.98], ["and", 6.28], ["rejoining.", 6.58], ["Deleting", 7.88], ["the", 8.12], ["branch", 8.28], ["with", 8.5], ["dash", 8.74], ["lowercase", 9.04], ["D", 9.52], ["removes", 9.84], ["only", 10.16], ["the", 10.5], ["label", 10.64], ["and", 10.88], ["only", 11.28], ["if", 11.54], ["its", 11.74], ["work", 11.88], ["is", 12.1], ["merged,", 12.26], ["the", 12.94], ["commits", 13.06], ["stay.", 13.26]], "B60": [["A", 0.0], ["tag", 0.14], ["is", 0.32], ["a", 0.46], ["flag", 0.58], ["on", 0.8], ["one", 0.96], ["commit", 1.18], ["and", 1.46], ["it", 1.68], ["does", 1.76], ["not", 1.88], ["move.", 2.12], ["Branch", 3.18], ["names", 3.18], ["slide", 3.5], ["forward", 3.86], ["with", 4.18], ["every", 4.42], ["new", 4.68], ["commit.", 4.9], ["A", 5.44], ["tag", 5.54], ["stays", 5.74], ["where", 6.06], ["you", 6.3], ["planted", 6.42], ["it.", 6.72], ["Before", 7.32], ["the", 7.5], ["paper", 7.64], ["goes", 7.86], ["out,", 8.1], ["tag", 8.78], ["the", 8.84], ["commit", 9.04], ["behind", 9.26], ["your", 9.56], ["figures", 9.72], ["and", 10.08], ["check", 10.42], ["that", 10.64], ["tag", 10.86], ["out", 11.12], ["any", 11.32], ["time", 11.48], ["to", 11.76], ["get", 11.94], ["exactly", 12.08], ["that", 12.44], ["code.", 12.8]], "B61": [["The", 0.0], ["tag", 0.12], ["command", 0.34], ["and", 0.7], ["the", 0.96], ["list", 1.06], ["that", 1.24], ["shows", 1.42], ["it", 1.7], ["with", 1.92], ["its", 2.08], ["message.", 2.24], ["Tags", 3.36], ["are", 3.36], ["not", 3.54], ["sent", 3.7], ["by", 3.98], ["a", 4.2], ["plain", 4.32], ["push.", 4.52], ["Pushing", 5.38], ["uploads", 5.6], ["your", 6.1], ["work", 6.2], ["to", 6.38], ["a", 6.56], ["server", 6.64], ["such", 6.88], ["as", 7.16], ["GitHub,", 7.42], ["which", 7.82], ["changes", 8.0], ["something", 8.4], ["outside", 8.76], ["your", 9.14], ["machine.", 9.38], ["So", 10.02], ["do", 10.1], ["it", 10.24], ["on", 10.36], ["purpose", 10.5], ["and", 10.88], ["with", 11.16], ["the", 11.28], ["repository", 11.4], ["owner's", 11.84], ["agreement.", 12.48], ["We", 13.14], ["did", 13.24], ["not", 13.34], ["push,", 13.56], ["this", 14.08], ["folder", 14.22], ["has", 14.54], ["no", 14.78], ["remote.", 15.02]], "B62": [["The", 0.0], ["reviewers", 0.12], ["question", 0.4], ["what", 0.74], ["did", 1.14], ["you", 1.28], ["get", 1.38], ["with", 1.52], ["the", 1.66], ["original", 1.78], ["threshold,", 2.14], ["find", 3.14], ["the", 3.26], ["commit", 3.4], ["by", 3.66], ["its", 3.9], ["message,", 4.06], ["restore", 4.78], ["only", 5.06], ["that", 5.38], ["one", 5.6], ["file", 5.78], ["from", 6.08], ["it,", 6.36], ["run", 6.7], ["it,", 6.82], ["and", 7.14], ["read", 7.22], ["the", 7.36], ["answer,", 7.54], ["199", 8.74], ["genes", 8.76], ["kept", 9.5], ["at", 9.74], ["10", 9.96], ["against", 10.3], ["197", 10.7], ["at", 11.26], ["20,", 11.82], ["then", 12.76], ["put", 12.94], ["today's", 13.14], ["version", 13.56], ["back.", 13.82]], "B63": [["One", 0.0], ["thing", 0.2], ["to", 0.38], ["notice,", 0.56], ["restoring", 1.18], ["the", 1.5], ["script", 1.72], ["did", 1.96], ["not", 2.18], ["restore", 2.4], ["the", 2.8], ["results.", 2.96], ["The", 3.84], ["rerun", 3.92], ["overwrote", 4.22], ["the", 4.62], ["two", 4.76], ["tracked", 4.96], ["result", 5.3], ["files", 5.62], ["and", 6.04], ["git", 6.38], ["status", 6.52], ["shows", 6.92], ["them", 7.2], ["modified.", 7.44], ["Commit", 8.42], ["them", 8.58], ["or", 8.84], ["put", 9.04], ["them", 9.18], ["back", 9.34], ["before", 9.6], ["you", 9.92], ["go", 10.08], ["on.", 10.24], ["The", 10.84], ["next", 10.92], ["section", 11.12], ["shows", 11.46], ["why.", 11.82]], "B70": [["On", 0.0], ["a", 0.12], ["cluster,", 0.26], ["a", 0.68], ["slurm", 0.86], ["job", 1.12], ["runs", 1.34], ["later", 1.64], ["on", 2.04], ["another", 2.2], ["machine", 2.48], ["from", 2.88], ["the", 3.14], ["files", 3.3], ["as", 3.6], ["they", 3.86], ["are", 4.02], ["then.", 4.12], ["So", 4.92], ["two", 5.02], ["rules,", 5.24], ["commit", 6.0], ["before", 6.18], ["you", 6.52], ["submit", 6.66], ["so", 7.02], ["every", 7.32], ["job", 7.62], ["traces", 7.94], ["to", 8.28], ["one", 8.56], ["commit,", 8.78], ["and", 9.42], ["print", 9.54], ["that", 9.7], ["commit's", 9.9], ["hash", 10.3], ["in", 10.5], ["the", 10.7], ["job", 10.82], ["log", 11.06], ["so", 11.36], ["the", 11.7], ["result", 11.82], ["always", 12.1], ["points", 12.48], ["back", 12.8], ["to", 13.1], ["the", 13.28], ["code.", 13.38]], "B71": [["This", 0.0], ["is", 0.16], ["the", 0.32], ["source's", 0.5], ["job", 0.92], ["script,", 1.16], ["read", 1.84], ["from", 1.96], ["the", 2.22], ["source", 2.36], ["and", 2.64], ["not", 2.86], ["run", 3.02], ["by", 3.26], ["us,", 3.5], ["two", 4.08], ["things", 4.26], ["to", 4.48], ["fix", 4.7], ["before", 4.9], ["you", 5.2], ["copy", 5.36], ["it.", 5.6], ["The", 6.24], ["partition", 6.3], ["named", 6.64], ["compute", 6.98], ["does", 7.38], ["not", 7.62], ["exist", 7.82], ["on", 8.14], ["explorer,", 8.36], ["and", 9.12], ["the", 9.3], ["mail", 9.38], ["line", 9.58], ["is", 9.9], ["a", 10.06], ["placeholder,", 10.16], ["use", 10.96], ["your", 11.08], ["own", 11.26], ["address", 11.42], ["or", 11.8], ["none.", 12.1]], "B72": [["Use", 0.0], ["a", 0.2], ["name", 0.34], ["from", 0.48], ["a", 0.7], ["real", 0.8], ["list.", 0.98], ["Read", 1.7], ["only", 1.72], ["commands", 1.98], ["on", 2.32], ["a", 2.54], ["login", 2.64], ["node", 2.86], ["showed", 3.18], ["on", 3.48], ["Explorer", 3.72], ["short,", 4.18], ["the", 4.82], ["default", 4.86], ["with", 5.16], ["a", 5.38], ["two", 5.52], ["day", 5.68], ["limit,", 5.8], ["and", 6.34], ["sharing", 6.46], ["with", 6.7], ["one", 7.02], ["hour.", 7.26], ["On", 8.34], ["AICR,", 8.5], ["the", 9.46], ["CPU", 9.5], ["partition", 9.92], ["is", 10.38], ["CPU", 10.68], ["with", 11.12], ["one", 11.52], ["day.", 11.76], ["Check", 12.44], ["Synfo", 12.52], ["before", 12.94], ["you", 13.24], ["copy", 13.44], ["a", 13.7], ["name.", 13.9]], "B73": [["Inside", 0.0], ["the", 0.32], ["job,", 0.54], ["a", 0.96], ["header", 1.02], ["that", 1.18], ["prints", 1.42], ["the", 1.64], ["job,", 1.86], ["the", 2.34], ["commit,", 2.4], ["and", 2.82], ["the", 2.86], ["branch,", 2.96], ["then", 3.56], ["the", 3.7], ["guard.", 3.82], ["If", 4.42], ["the", 4.5], ["working", 4.62], ["tree", 4.86], ["has", 5.14], ["uncommitted", 5.3], ["changes", 5.74], ["or", 6.26], ["staged", 6.58], ["ones,", 6.88], ["the", 7.38], ["job", 7.48], ["stops.", 7.74], ["Then", 8.86], ["the", 8.98], ["pipeline", 9.1], ["and", 9.54], ["a", 9.82], ["tag", 9.92], ["named", 10.14], ["run", 10.42], ["dash", 10.76], ["the", 11.2], ["job", 11.48], ["number", 11.76], ["on", 12.1], ["exactly", 12.4], ["that", 12.76], ["commit.", 13.1]], "B74": [["We", 0.0], ["ran", 0.12], ["the", 0.32], ["guard", 0.46], ["block", 0.66], ["on", 0.88], ["its", 1.08], ["own,", 1.22], ["on", 1.62], ["the", 1.68], ["Mac,", 1.78], ["not", 2.16], ["as", 2.3], ["a", 2.44], ["slurm", 2.58], ["job.", 2.98], ["With", 3.58], ["an", 3.66], ["edited", 3.76], ["file,", 4.0], ["it", 4.42], ["prints", 4.62], ["the", 4.84], ["error", 5.06], ["and", 5.3], ["exits", 5.52], ["with", 5.82], ["code", 6.06], ["1.", 6.28], ["After", 7.24], ["the", 7.52], ["commit", 7.7], ["it", 7.84], ["passes,", 7.98], ["the", 8.6], ["only", 8.66], ["line", 8.88], ["we", 9.2], ["added", 9.36], ["is", 9.58], ["the", 9.8], ["echo", 9.96], ["that", 10.2], ["says", 10.5], ["so.", 10.76], ["That", 11.4], ["is", 11.5], ["the", 11.62], ["habit.", 11.78], ["No", 12.3], ["trace.", 12.42], ["No", 13.02], ["run.", 13.14]], "B75": [["Weak", 0.0], ["spots", 0.22], ["from", 0.54], ["our", 0.84], ["reading", 0.96], ["of", 1.18], ["the", 1.36], ["logic", 1.48], ["not", 1.86], ["tested.", 2.18], ["The", 3.1], ["guard", 3.2], ["runs", 3.44], ["when", 3.78], ["the", 3.98], ["job", 4.12], ["starts", 4.36], ["not", 4.74], ["when", 5.04], ["you", 5.18], ["submit", 5.32], ["and", 5.68], ["a", 6.0], ["job", 6.1], ["can", 6.36], ["queue", 6.58], ["for", 6.78], ["hours.", 6.98], ["Edit", 7.84], ["the", 7.9], ["script", 8.08], ["meanwhile", 8.38], ["and", 8.8], ["the", 9.18], ["job", 9.32], ["may", 9.56], ["run", 9.76], ["newer", 9.94], ["code", 10.16], ["and", 10.48], ["log", 10.72], ["the", 10.92], ["newer", 11.14], ["hash.", 11.32]], "B76": [["A", 0.0], ["stronger", 0.16], ["version,", 0.42], ["hours", 1.06], ["and", 1.26], ["untested.", 1.54], ["Check", 2.5], ["the", 2.54], ["tree", 2.72], ["when", 2.88], ["you", 3.04], ["submit", 3.18], ["and", 3.5], ["pass", 3.72], ["the", 3.96], ["hash", 4.14], ["into", 4.36], ["the", 4.56], ["job.", 4.72], ["Inside", 5.7], ["the", 5.84], ["job,", 6.06], ["compare", 6.52], ["the", 6.76], ["two", 6.94], ["hashes", 7.12], ["and", 7.44], ["stop", 7.72], ["if", 8.02], ["they", 8.2], ["differ.", 8.34], ["That", 9.0], ["closes", 9.14], ["the", 9.46], ["gap.", 9.74]], "B77": [["Three", 0.0], ["more,", 0.2], ["the", 0.64], ["results", 0.72], ["of", 0.98], ["run", 1.22], ["rights", 1.4], ["are", 1.64], ["tracked", 1.84], ["files,", 2.12], ["so", 2.82], ["the", 2.98], ["next", 3.1], ["submit", 3.3], ["is", 3.66], ["blocked", 3.88], ["until", 4.2], ["you", 4.48], ["commit", 4.64], ["them.", 4.92], ["The", 5.92], ["tag", 5.98], ["changes", 6.18], ["the", 6.64], ["repository", 6.84], ["from", 7.32], ["inside", 7.72], ["the", 8.1], ["job,", 8.3], ["so", 8.78], ["tag", 8.94], ["only", 9.3], ["from", 9.56], ["a", 9.82], ["checkout", 9.94], ["you", 10.2], ["own.", 10.52], ["And", 11.12], ["a", 11.2], ["tag", 11.32], ["made", 11.52], ["in", 11.74], ["the", 11.9], ["job", 12.0], ["exists", 12.32], ["only", 12.68], ["there", 13.06], ["until", 13.46], ["someone", 13.84], ["pushes", 14.18], ["it.", 14.48]], "B78": [["A", 0.0], ["full", 0.14], ["job", 0.3], ["record", 0.56], ["holds", 0.82], ["more", 1.2], ["than", 1.48], ["a", 1.64], ["commit,", 1.76], ["job,", 2.36], ["node,", 2.8], ["and", 3.04], ["partition,", 3.1], ["start", 3.72], ["and", 3.88], ["end", 4.0], ["times,", 4.22], ["the", 4.72], ["exact", 4.78], ["command,", 5.06], ["every", 5.76], ["parameter", 5.98], ["and", 6.34], ["random", 6.64], ["seed,", 7.0], ["input", 7.62], ["paths", 7.72], ["with", 8.04], ["checksums,", 8.28], ["software", 9.32], ["versions,", 9.32], ["the", 9.98], ["hardware", 10.0], ["used,", 10.3], ["the", 10.86], ["output", 10.9], ["folder,", 11.2], ["and", 11.82], ["the", 11.86], ["exit", 11.96], ["status.", 12.22], ["The", 13.42], ["header", 13.54], ["prints", 13.68], ["the", 13.94], ["first", 14.12], ["few.", 14.3], ["You", 14.9], ["add", 15.0], ["the", 15.14], ["rest.", 15.28]], "B80": [["Three", 0.0], ["aliases", 0.22], ["save", 0.52], ["typing", 0.92], ["and", 1.28], ["go", 1.56], ["in", 1.74], ["your", 1.86], ["global", 1.98], ["config.", 2.26], ["LG", 3.24], ["for", 3.36], ["the", 3.66], ["branch", 3.78], ["graph,", 4.0], ["ST", 4.58], ["for", 4.72], ["a", 5.08], ["short", 5.18], ["status,", 5.4], ["last", 6.26], ["for", 6.28], ["the", 6.48], ["last", 6.6], ["commit.", 6.86], ["Here's", 7.82], ["what", 8.1], ["LG", 8.26], ["draws", 8.6], ["with", 8.98], ["branch", 9.28], ["and", 9.58], ["tag", 9.8], ["labels.", 10.04], ["Main", 10.96], ["at", 10.96], ["the", 11.12], ["top,", 11.26], ["the", 11.66], ["merge", 11.72], ["and", 11.94], ["the", 12.24], ["tag", 12.34], ["on", 12.62], ["the", 12.82], ["commit", 12.96], ["behind", 13.2], ["the", 13.54], ["paper.", 13.68]], "B81": [["and", 0.0], ["a", 0.1], ["small", 0.22], ["shell", 0.44], ["function", 0.7], ["that", 1.0], ["puts", 1.38], ["the", 1.52], ["branch", 1.74], ["name", 1.96], ["in", 2.2], ["your", 2.36], ["prompt", 2.48], ["so", 2.78], ["you", 3.1], ["always", 3.22], ["know", 3.44], ["where", 3.68], ["you", 3.9], ["are.", 4.1], ["Here", 4.84], ["it", 4.92], ["prints", 5.06], ["the", 5.22], ["project", 5.4], ["name", 5.74], ["and", 6.08], ["main", 6.32], ["in", 6.54], ["brackets.", 6.78], ["It", 7.68], ["lasts", 7.78], ["for", 8.02], ["this", 8.26], ["session", 8.42], ["only,", 8.72], ["so", 9.26], ["no", 9.46], ["profile", 9.66], ["edit", 10.1], ["is", 10.38], ["needed.", 10.6]], "B82": [["Charts", 0.0], ["need", 0.32], ["node", 0.5], ["display.", 0.76], ["Two", 1.56], ["aux", 1.62], ["scripts", 1.8], ["draw", 2.12], ["a", 2.42], ["bar", 2.56], ["chart", 2.7], ["and", 3.04], ["a", 3.26], ["histogram", 3.34], ["in", 3.78], ["plain", 3.96], ["text", 4.18], ["so", 4.48], ["they", 4.82], ["run", 4.96], ["on", 5.14], ["a", 5.28], ["login", 5.4], ["node.", 5.62], ["They", 6.58], ["are", 6.66], ["exploratory,", 6.74], ["so", 7.66], ["they", 7.78], ["live", 7.92], ["on", 8.06], ["their", 8.22], ["own", 8.32], ["branch.", 8.52], ["Explore", 9.44], ["slash", 9.44], ["-cli", 9.82], ["dash", 10.22], ["charts", 10.46], ["until", 10.9], ["you", 11.24], ["decide", 11.38], ["to", 11.68], ["merge", 11.88], ["them.", 12.08]], "B83": [["Questions", 0.0], ["people", 0.38], ["ask", 0.68], ["can", 1.08], ["git", 1.34], ["hold", 1.46], ["large", 1.62], ["data", 1.98], ["sets,", 2.24], ["not", 2.8], ["directly.", 2.88], ["Git", 3.94], ["LFS", 3.98], ["handles", 4.46], ["files", 4.88], ["up", 5.22], ["to", 5.46], ["about", 5.62], ["2GB", 5.8], ["and", 6.38], ["DVC", 6.72], ["layers", 7.18], ["on", 7.56], ["git", 7.82], ["and", 8.02], ["keeps", 8.2], ["the", 8.36], ["data", 8.56], ["elsewhere,", 8.8], ["track", 9.58], ["a", 9.62], ["manifest", 9.76], ["in", 10.1], ["git.", 10.36], ["Jupyter", 11.28], ["notebooks", 11.56], ["carry", 11.9], ["their", 12.26], ["outputs", 12.48], ["which", 12.9], ["makes", 13.16], ["noisy", 13.38], ["diffs,", 13.76], ["strip", 14.32], ["them", 14.5], ["within", 14.7], ["bstripout", 14.96], ["or", 15.64], ["sync", 15.92], ["with", 16.18], ["Jupyterxt.", 16.44]], "B84": [["To", 0.0], ["fix", 0.12], ["the", 0.3], ["last", 0.48], ["commit", 0.76], ["before", 0.98], ["you", 1.28], ["push,", 1.46], ["use", 2.04], ["commit", 2.1], ["dash", 2.36], ["dash", 2.72], ["amend.", 3.02], ["To", 3.88], ["undo", 4.04], ["a", 4.28], ["commit", 4.42], ["that", 4.66], ["is", 4.86], ["already", 4.96], ["shared,", 5.26], ["use", 5.94], ["git", 6.04], ["revert,", 6.2], ["which", 6.8], ["adds", 6.9], ["a", 7.1], ["new", 7.24], ["commit", 7.38], ["that", 7.66], ["undoes", 7.92], ["it.", 8.26], ["And", 8.8], ["never", 8.94], ["run", 9.18], ["git", 9.38], ["reset", 9.6], ["dash", 9.94], ["dash", 10.28], ["hard", 10.56], ["on", 10.9], ["a", 11.08], ["branch", 11.18], ["other", 11.38], ["people", 11.6], ["use.", 11.9], ["It", 12.48], ["throws", 12.62], ["work", 12.94], ["away.", 13.22]], "B85": [["If", 0.0], ["two", 0.12], ["branches", 0.28], ["change", 0.58], ["the", 0.94], ["same", 1.18], ["lines,", 1.4], ["git", 2.1], ["stops", 2.12], ["and", 2.48], ["marks", 2.7], ["the", 2.96], ["file.", 3.18], ["Open", 4.12], ["it,", 4.32], ["keep", 4.6], ["the", 4.7], ["version", 4.86], ["you", 5.1], ["want,", 5.3], ["delete", 5.68], ["the", 5.84], ["markers,", 6.0], ["then", 6.6], ["git", 6.7], ["add", 6.86], ["the", 7.04], ["file", 7.2], ["and", 7.46], ["commit,", 7.66], ["and", 8.36], ["git", 8.44], ["stash", 8.64], ["sets", 8.96], ["half", 9.28], ["done", 9.52], ["edits", 9.76], ["aside,", 10.1], ["stash", 10.8], ["pop", 11.04], ["brings", 11.34], ["them", 11.62], ["back,", 11.86], ["we", 12.38], ["did", 12.46], ["not", 12.58], ["run", 12.76], ["either.", 12.98]], "BVDT": [["Let's", 0.0], ["recap", 0.7], ["with", 0.96], ["Claude.", 1.18], ["A", 1.78], ["commit", 1.88], ["is", 2.0], ["a", 2.18], ["saved", 2.36], ["snapshot", 2.56], ["and", 3.08], ["a", 3.34], ["tag", 3.44], ["is", 3.6], ["a", 3.76], ["fixed", 3.88], ["name", 4.06], ["for", 4.3], ["one", 4.52], ["of", 4.66], ["them.", 4.78], ["Track", 5.38], ["the", 5.4], ["code", 5.58], ["that", 5.76], ["makes", 5.92], ["results", 6.1], ["and", 6.48], ["write", 6.72], ["the", 6.88], ["ignore", 7.04], ["file", 7.32], ["so", 7.66], ["it's", 7.92], ["allow", 8.08], ["lines", 8.28], ["really", 8.64], ["work.", 8.9], ["Run", 9.78], ["look", 9.92], ["then", 10.08], ["commit", 10.28], ["the", 10.5], ["code", 10.64], ["and", 10.88], ["the", 11.0], ["result", 11.1], ["together", 11.36], ["one", 11.7], ["logical", 12.04], ["change", 12.42], ["at", 12.84], ["a", 13.02], ["time.", 13.12], ["A", 13.68], ["branch", 13.72], ["holds", 13.9], ["an", 14.16], ["experiment,", 14.32], ["merge", 14.98], ["it", 15.16], ["when", 15.32], ["it", 15.42], ["belongs", 15.52], ["and", 15.84], ["tag", 16.1], ["what", 16.34], ["you", 16.46], ["submit.", 16.6], ["Any", 17.24], ["old", 17.36], ["result", 17.54], ["comes", 17.82], ["back", 18.06], ["from", 18.38], ["its", 18.56], ["commit", 18.7], ["one", 18.98], ["file", 19.26], ["at", 19.56], ["a", 19.72], ["time.", 19.84], ["On", 20.36], ["a", 20.46], ["cluster,", 20.56], ["commit", 21.12], ["before", 21.22], ["you", 21.54], ["submit.", 21.7], ["Print", 22.62], ["the", 22.74], ["hash", 22.88], ["in", 23.06], ["the", 23.26], ["job", 23.4], ["log", 23.64], ["and", 23.92], ["guard", 24.26], ["against", 24.54], ["a", 24.84], ["dirty", 25.06], ["tree.", 25.24]], "BHTF": [["Your", 0.0], ["turn,", 0.14], ["paste", 0.56], ["this", 0.72], ["into", 0.94], ["Claude", 1.18], ["with", 1.4], ["a", 1.62], ["copy", 1.74], ["of", 1.94], ["a", 2.1], ["real", 2.2], ["project", 2.42], ["folder", 2.84], ["open,", 3.16], ["open", 3.9], ["the", 4.06], ["folder", 4.22], ["of", 4.48], ["a", 4.66], ["project", 4.8], ["I", 5.12], ["have.", 5.34], ["List", 5.94], ["every", 6.14], ["file", 6.42], ["in", 6.72], ["this", 6.88], ["folder.", 7.02], ["For", 7.7], ["each", 7.82], ["one,", 7.98], ["say", 8.32], ["whether", 8.4], ["it", 8.56], ["is", 8.7], ["code,", 8.84], ["a", 9.36], ["setting,", 9.46], ["a", 9.92], ["result,", 9.98], ["or", 10.42], ["raw", 10.5], ["data", 10.72], ["and", 11.0], ["whether", 11.24], ["it", 11.36], ["should", 11.54], ["be", 11.66], ["tracked", 11.78], ["in", 12.02], ["git.", 12.28], ["Then", 12.98], ["write", 13.22], ["a", 13.4], ["gitignore", 13.54], ["file", 13.96], ["that", 14.28], ["keeps", 14.52], ["the", 14.66], ["results", 14.86], ["out", 15.16], ["but", 15.48], ["lets", 15.68], ["one", 15.84], ["small", 16.1], ["summary", 16.46], ["file", 16.84], ["through", 17.18], ["and", 17.52], ["tell", 17.92], ["me", 18.1], ["whether", 18.24], ["your", 18.38], ["gitignore", 18.58], ["file", 19.04], ["really", 19.44], ["lets", 19.7], ["that", 19.98], ["file", 20.24], ["through.", 20.54], ["Do", 21.4], ["not", 21.58], ["run", 21.74], ["anything", 21.94], ["and", 22.34], ["do", 22.56], ["not", 22.68], ["change", 22.88], ["any", 23.18], ["file,", 23.4], ["then", 24.0], ["check", 24.24], ["two", 24.48], ["things", 24.7], ["yourself.", 24.96], ["Did", 25.73], ["Claude", 26.0], ["run", 26.24], ["nothing", 26.52], ["and", 26.84], ["change", 27.1], ["no", 27.34], ["file", 27.58], ["and", 27.9], ["does", 28.32], ["gitignore", 28.52], ["-v", 29.24], ["agree", 29.88], ["with", 30.16], ["what", 30.4], ["it", 30.6], ["said", 30.72], ["about", 30.94], ["the", 31.14], ["summary", 31.3], ["file?", 31.6]], "BOUT": [["Scientific", 0.0], ["Reproducibility", 0.6], ["II", 1.42], ["Version", 1.84], ["Control", 2.3], ["at", 2.78], ["Nick", 3.18], ["Baer", 3.44], ["Brown.", 3.7]]}


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


# ═════════════════════════════ PART A — B10 B11 B12 B13 B14 B15 B20 B30 (shared helpers pA_*) ═════════════════════════════
# Cue times come from hear("spoken phrase"): measured word times in _ASR. Labels are 1-3 words; real text only in mono.
def pA_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pA_arrow(a, b, w=8):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], color=INK, stroke_width=w, buff=0, max_tip_length_to_length_ratio=0.5)


def pA_disc(x, y, r=0.5, page=True):
    """A commit disc: white disc, ink outline, a small outline-free page inside (the snapshot picture)."""
    d = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    g = VGroup(d)
    if page:
        pg = Rectangle(width=r * 0.78, height=r * 1.0, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
        ls = VGroup(*[Line([x - r * 0.26, y + r * (0.22 - 0.22 * i), 0], [x + r * 0.26, y + r * (0.22 - 0.22 * i), 0], color=BAR1, stroke_width=3) for i in range(3)])
        g.add(pg, ls)
    g.d = d
    return g


def pA_hash(s, x, y):
    return M(s, 32).move_to([x, y, 0])


def pA_flag(x, y, h=1.2):
    """A flag planted with its pole foot at (x, y): ink pole, terracotta pennant (no text on it)."""
    pole = Line([x, y, 0], [x, y + h, 0], color=INK, stroke_width=7)
    pen = Polygon([x, y + h, 0], [x + 0.62, y + h - 0.24, 0], [x, y + h - 0.48, 0], fill_color=TERRA, fill_opacity=1, stroke_width=0)
    g = VGroup(pole, pen)
    g.pole, g.pen = pole, pen
    return g


def pA_label_row(items, y, size=34):
    return [chip(t, x, y, size=size) for t, x in items]


# ───────────────────────────────────────────────────────────────────────────────────────────────
class B10_ReviewerAsks(Scene):
    """A reviewer's question; eight real file and folder names pile up; which made which?"""
    def construct(self):
        title = pA_act_title("I · Why Keep History")
        bear = professor_bear("1x1", 2.3, seed="B10", x=-4.6, y=-0.5)
        ask = chip("threshold?", -4.6, 1.55, size=36)
        names = ["filter.sh", "filter_v2.sh", "filter_final.sh", "filter_final_USE_THIS.sh",
                 "results_old/", "results_new/", "results_for_paper/", "results_for_paper_FINAL/"]
        chips = [chip(n, 2.3 + (0.25 if i % 2 else -0.25), 2.55 - 0.72 * i, mono=True, size=32) for i, n in enumerate(names)]
        # "Which script made which table?": a question pair ringed by a pulse
        q = T("?", 90).move_to([-1.2, 0.2, 0])
        self.play(FadeIn(title), FadeIn(bear), run_time=0.5)
        hear(self, "a reviewer asks", lead=0.2)
        self.play(FadeIn(ask, shift=DOWN * 0.2), run_time=0.4)
        hear(self, "Without version", lead=0.1)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in chips[:4]], lag_ratio=0.25), run_time=1.4)
        hear(self, "you guess", lead=0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in chips[4:]], lag_ratio=0.25), run_time=1.4)
        hear(self, "Which script", lead=0.1)
        self.play(FadeIn(q, scale=1.3), run_time=0.4)
        self.play(Indicate(chips[3], color=INK, scale_factor=1.05), run_time=0.6)
        done(self)


class B11_OneTimeline(Scene):
    """One script and a timeline: date/author/message on each change; flag, branch, undo."""
    def construct(self):
        script = chip("filter.sh", -4.2, 2.55, mono=True, size=34)
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        y0 = 0.6
        line = Line([-5.7, y0, 0], [5.7, y0, 0], color=INK, stroke_width=6)
        dots = [pA_disc(x, y0, 0.3, page=False) for x in xs]
        c_date, c_auth, c_msg = chip("date", -4.4, -0.6, size=34), chip("author", -4.4, -1.5, size=34), chip("message", -4.4, -2.4, size=34)
        flag = pA_flag(0.0, y0 + 0.3, 1.1)
        flab = T("figure 3", 34).move_to([1.2, 2.1, 0])
        branch = Line([-2.2, y0 - 0.3, 0], [1.2, -1.6, 0], color=INK, stroke_width=6)
        bdot = pA_disc(1.2, -1.6, 0.3, page=False)
        blab = T("experiment", 34).move_to([3.0, -1.6, 0])
        undo = pA_arrow([4.2, 1.5], [2.4, 1.5])
        ulab = T("undo", 34).move_to([3.3, 2.1, 0])
        self.play(FadeIn(script), Create(line), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.15), run_time=0.9)
        hear(self, "date", lead=0.2)
        self.play(FadeIn(c_date), run_time=0.25)
        hear(self, "an author", lead=0.15)
        self.play(FadeIn(c_auth), run_time=0.25)
        hear(self, "a message", lead=0.15)
        self.play(FadeIn(c_msg), run_time=0.25)
        hear(self, "mark the exact", lead=0.15)
        self.play(Create(flag), FadeIn(flab), run_time=0.5)
        hear(self, "own branch", lead=0.4)
        self.play(Create(branch), FadeIn(bdot), FadeIn(blab), run_time=0.6)
        hear(self, "undo", lead=0.3)
        self.play(Create(undo), FadeIn(ulab), run_time=0.5)
        done(self)


class B12_Snapshots(Scene):
    """The Git logo; three commit discs, each a full picture; arrows back to the parent."""
    def construct(self):
        git = logo_chip("git", -5.0, 2.3, h=1.3)
        xs = [-3.6, 0.0, 3.6]
        discs = [pA_disc(x, 0.3, 0.7) for x in xs]
        hashes = [pA_hash(h, x, -0.85) for h, x in zip(["a3f8c21", "b7d2e14", "d9c1f37"], xs)]
        arrows = [pA_arrow([xs[i] - 0.8, 0.3], [xs[i - 1] + 0.8, 0.3]) for i in (1, 2)]
        whole = T("whole picture", 36).move_to([0.0, 2.0, 0])
        par = T("parent", 34).move_to([1.8, 0.95, 0])
        hear(self, "called Git", lead=0.3)
        self.play(FadeIn(git), run_time=0.4)
        hear(self, "snapshots", lead=0.2)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in discs], lag_ratio=0.4), LaggedStart(*[FadeIn(h) for h in hashes], lag_ratio=0.4), run_time=1.3)
        hear(self, "full picture", lead=0.3)
        self.play(FadeIn(whole), run_time=0.3)
        hear(self, "linked to", lead=0.1)
        self.play(Create(arrows[0]), Create(arrows[1]), FadeIn(par), run_time=0.6)
        done(self)


class B13_BranchAndTag(Scene):
    """The same chain: main on the last commit; an experiment forks off; a flag on one commit."""
    def construct(self):
        xs = [-3.6, 0.0, 3.6]
        discs = [pA_disc(x, 0.8, 0.6) for x in xs]
        hashes = [pA_hash(h, x, -0.2) for h, x in zip(["a3f8c21", "b7d2e14", "d9c1f37"], xs)]
        arrows = [pA_arrow([xs[i] - 0.7, 0.8], [xs[i - 1] + 0.7, 0.8]) for i in (1, 2)]
        main = chip("main", 3.6, 2.15, size=34)
        fork = Line([0.45, 0.45, 0], [1.4, -1.5, 0], color=INK, stroke_width=6)
        d4 = pA_disc(1.4, -1.7, 0.45)
        h4 = pA_hash("e5a0b99", 1.4, -2.55)
        exp = chip("explore/idea", 4.2, -1.7, mono=True, size=32)
        flag = pA_flag(-3.6, 1.45, 1.0)
        v = T("v1.0", 34).move_to([-2.35, 2.2, 0])
        self.add(*discs, *hashes, *arrows)
        hear(self, "A branch", lead=0.2)
        self.play(FadeIn(main), run_time=0.3)
        hear(self, "an experiment", lead=0.3)
        self.play(Create(fork), FadeIn(d4), FadeIn(h4), run_time=0.6)
        self.play(FadeIn(exp), run_time=0.3)
        hear(self, "A tag", lead=0.2)
        self.play(Create(flag), FadeIn(v), run_time=0.5)
        done(self)


class B14_ThreePlaces(Scene):
    """Working tree, staging area, repository: a page travels on git add, then git commit."""
    def construct(self):
        xs = [-4.4, 0.0, 4.4]
        boxes = [Rectangle(width=2.9, height=2.3, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, 0.8, 0]) for x in xs]
        labs = [T(t, 36).move_to([x, -0.7, 0]) for t, x in zip(["working tree", "staging area", "repository"], xs)]
        page = Rectangle(width=0.8, height=1.0, fill_color="#FFFFFF", fill_opacity=1, stroke_width=0).move_to([xs[0], 0.8, 0])
        pl = VGroup(*[Line([xs[0] - 0.25, 0.8 + 0.2 - 0.2 * i, 0], [xs[0] + 0.25, 0.8 + 0.2 - 0.2 * i, 0], color=BAR1, stroke_width=3) for i in range(3)])
        pg = VGroup(page, pl)
        stack = VGroup(*[Rectangle(width=1.1, height=0.28, fill_color="#FFFFFF", fill_opacity=1, stroke_width=0).move_to([xs[2], 0.35 + 0.4 * i, 0]) for i in range(3)])
        add_c = chip("git add", -2.2, -2.2, mono=True, size=32)
        com_c = chip("git commit", 2.2, -2.2, mono=True, size=32)
        a1 = pA_arrow([-2.7, -1.75], [-2.1, -0.95], 6)
        a2 = pA_arrow([1.7, -1.75], [2.3, -0.95], 6)
        self.play(*[FadeIn(b) for b in boxes], run_time=0.5)
        hear(self, "working tree", lead=0.25)
        self.play(FadeIn(labs[0]), FadeIn(pg), run_time=0.4)
        hear(self, "staging area", lead=0.25)
        self.play(FadeIn(labs[1]), run_time=0.3)
        hear(self, "git add", lead=0.25)
        self.play(FadeIn(add_c), run_time=0.25)
        self.play(pg.animate.move_to([xs[1], 0.8, 0]), run_time=0.7)
        hear(self, "repository holds", lead=0.2)
        self.play(FadeIn(labs[2]), FadeIn(stack), run_time=0.4)
        hear(self, "git commit", lead=0.25)
        self.play(FadeIn(com_c), run_time=0.25)
        self.play(pg.animate.move_to([xs[2], 1.7, 0]).scale(0.7), run_time=0.7)
        done(self)


class B15_FourMoments(Scene):
    """Four rows: a research moment and its Git answer."""
    def construct(self):
        ys = [2.4, 0.8, -0.8, -2.4]
        situ = ["another value?", "postdoc leaves", "setting changed", "with the paper"]
        ans = ["a branch", "clone + README", "git diff HEAD~1", "a tag"]
        cues = ["reviewer asks", "postdoc", "cluster setting", "Publishing"]
        rows = []
        for y, s, a in zip(ys, situ, ans):
            l = chip(s, -3.6, y, size=38)
            ar = pA_arrow([-1.4, y], [-0.4, y], 7)
            r = chip(a, 2.0, y, mono=(a not in ("a branch", "a tag")), size=38)
            rows.append(VGroup(l, ar, r))
        gh = logo_chip("github", 5.3, ys[3], h=1.3)
        self.play(*[FadeIn(r[0]) for r in rows], *[FadeIn(r[1]) for r in rows], run_time=0.5)
        for row, cue in zip(rows, cues):
            hear(self, cue, lead=0.25)
            self.play(FadeIn(row[2], shift=LEFT * 0.2), Indicate(row[0], color=INK, scale_factor=1.04), run_time=0.5)
        hear(self, "GitHub", lead=0.2)
        self.play(FadeIn(gh), run_time=0.4)
        done(self)


class B20_TheExample(Scene):
    """A counts table flows through a MIN_COUNT funnel into a smaller summary table with UP, DOWN, NS."""
    def construct(self):
        cw, ch = 0.55, 0.5
        x0, y0 = -6.0, 1.3

        def table(xl, yt, ncols, nrows, hdr_fill=BOX_L):
            cells = VGroup()
            for r in range(nrows):
                for c in range(ncols):
                    f = hdr_fill if r == 0 else "#A39E94"
                    cells.add(Rectangle(width=cw - 0.05, height=ch - 0.05, fill_color=f, fill_opacity=1, stroke_width=0)
                              .move_to([xl + cw * c + cw / 2, yt - ch * r - ch / 2, 0]))
            return cells
        t1 = table(x0, y0, 7, 6)
        lab_c = T("control", 34).move_to([x0 + cw * 2.5, y0 + 0.4, 0])
        lab_t = T("treated", 34).move_to([x0 + cw * 5.5, y0 + 0.4, 0])
        lab_g = M("gene_id", 32).move_to([x0 + 1.0, y0 - ch * 6 - 0.4, 0])
        funnel = Polygon([-1.1, 1.3, 0], [1.1, 1.3, 0], [0.35, -0.6, 0], [-0.35, -0.6, 0], fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5)
        flab = M("MIN_COUNT", 32).move_to([0.0, -1.2, 0])
        sx0 = 2.6
        t2 = table(sx0, y0, 5, 4)
        stat = [chip(t, x, -1.6, size=32) for t, x in zip(["UP", "DOWN", "NS"], [2.0, 3.9, 5.5])]
        slab = T("summary", 34).move_to([sx0 + 1.4, y0 + 0.4, 0])
        d1 = Rectangle(width=0.9, height=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-3.2, 0.0, 0])
        d2 = d1.copy().move_to([-3.2, -0.5, 0])
        arr1 = pA_arrow([-1.95, 0.4], [-1.2, 0.4], 7)
        arr2 = pA_arrow([1.2, 0.4], [2.3, 0.4], 7)
        hear(self, "small R N A", lead=0.4)
        self.play(FadeIn(t1), run_time=0.5)
        hear(self, "one row per gene", lead=0.1)
        self.play(FadeIn(lab_g), run_time=0.3)
        hear(self, "three control", lead=0.2)
        self.play(FadeIn(lab_c), run_time=0.3)
        hear(self, "treated", lead=0.2)
        self.play(FadeIn(lab_t), run_time=0.3)
        hear(self, "drops low", lead=0.3)
        self.play(FadeIn(funnel), FadeIn(flab), Create(arr1), run_time=0.5)
        self.play(FadeIn(d1), FadeIn(d2), run_time=0.2)
        self.play(d1.animate.move_to([0.0, 0.5, 0]), d2.animate.move_to([0.0, 0.1, 0]), run_time=0.7)
        self.play(d2.animate.shift(DOWN * 2.2).set_opacity(0), run_time=0.5)
        hear(self, "writes a summary", lead=0.2)
        self.play(Create(arr2), FadeIn(t2), FadeIn(slab), run_time=0.5)
        self.play(*[FadeIn(s) for s in stat], run_time=0.4)
        done(self)


class B30_CodeNotResults(Scene):
    """Code goes into the repository, big data to storage, tokens never; the ignore page lists what to skip."""
    def construct(self):
        title = pA_act_title("III · What To Leave Out")
        box = Rectangle(width=2.9, height=2.1, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-4.3, 0.8, 0])
        blab = T("repository", 34).move_to([-4.3, -0.55, 0])
        script = VGroup(Rectangle(width=0.9, height=1.1, fill_color="#FFFFFF", fill_opacity=1, stroke_width=0),
                        *[Line([-0.28, 0.25 - 0.22 * i, 0], [0.28, 0.25 - 0.22 * i, 0], color=BAR1, stroke_width=3) for i in range(3)]).move_to([-4.3, 2.0, 0])
        slab = T("scripts", 34).move_to([-2.5, 2.0, 0])
        data = Rectangle(width=1.5, height=1.1, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-0.3, 1.3, 0])
        dlab = T("big data", 34).move_to([-0.3, 2.45, 0])
        iso = Iso(-0.9, -3.0, 0.7)
        rk, lt = explorer_rack(iso)
        stor = VGroup(rk, lt)
        slab2 = T("project storage", 34).move_to([2.0, -2.4, 0])
        down = pA_arrow([-0.3, 0.7], [-0.3, -0.6], 7)
        key = chip("tokens", -4.3, -1.9, size=34)
        xm = x_mark(-2.35, -1.9, r=0.3, w=9)
        page = Rectangle(width=1.7, height=2.1, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([4.5, 1.5, 0])
        pl = VGroup(*[Line([3.9, 2.2 - 0.38 * i, 0], [5.1 - (0.5 if i == 3 else 0), 2.2 - 0.38 * i, 0], color=BAR2, stroke_width=6) for i in range(4)])
        gi = chip(".gitignore", 4.5, -0.1, mono=True, size=32)
        skip = VGroup(*[pill(4.5, -1.2 - 0.62 * i, 2.4, h=0.46, fill=GHOST) for i in range(3)])
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "Track the code", lead=0.2)
        self.play(FadeIn(box), FadeIn(blab), FadeIn(script), FadeIn(slab), run_time=0.5)
        self.play(script.animate.move_to([-4.3, 0.8, 0]), run_time=0.6)
        hear(self, "Big raw data", lead=0.25)
        self.play(FadeIn(data), FadeIn(dlab), run_time=0.4)
        hear(self, "project storage", lead=0.3)
        self.play(Create(down), FadeIn(stor), FadeIn(slab2), run_time=0.5)
        hear(self, "passwords", lead=0.3)
        self.play(FadeIn(key), run_time=0.3)
        self.play(Create(xm), run_time=0.3)
        hear(self, "dot git ignore", lead=0.3)
        self.play(FadeIn(page), Create(pl), FadeIn(gi), run_time=0.5)
        self.play(FadeIn(skip), run_time=0.4)
        done(self)


# ═════════════════════════════ PART B — B40 B44 B50 B60 ═════════════════════════════
def pB_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pB_card(lines, x, y, w, size=32, h=None):
    """An outline-free white card carrying one or two serif lines."""
    h = h or (0.5 + 0.5 * len(lines))
    sh = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
    cd = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    labs = VGroup(*[T(s, size) for s in lines]).arrange(DOWN, buff=0.18).move_to([x, y, 0])
    g = VGroup(sh, cd, labs)
    g.card = cd
    return g


class B40_RunInspectCommit(Scene):
    """A four-step loop with a rider dot; a flag plants on the commit step; code and result slide into it."""
    def construct(self):
        title = pB_act_title("IV · Save And Inspect")
        top = chip("change a value", 0.0, 2.2, size=34)
        right = chip("run", 3.6, 0.2, size=34)
        bot = chip("inspect", 0.0, -1.9, size=34)
        left = chip("commit", -3.4, 0.2, size=34)
        a1 = pA_arrow([1.9, 1.85], [3.2, 0.7], 7)
        a2 = pA_arrow([3.4, -0.3], [1.3, -1.6], 7)
        a3 = pA_arrow([-1.3, -1.6], [-3.1, -0.3], 7)
        a4 = pA_arrow([-3.6, 0.7], [-1.9, 1.85], 7)
        rider = Dot([0.0, 1.55, 0], radius=0.16, color=TERRA)
        code = chip("code", -5.0, 1.5, size=34)
        res = chip("result", -5.0, 2.45, size=34)
        flag = pA_flag(-4.9, -2.3, 1.2)
        tag = T("tag", 36).move_to([-3.9, -1.6, 0])
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "change a value", lead=0.2)
        self.play(FadeIn(top), run_time=0.3)
        hear(self, "run the script", lead=0.2)
        self.play(Create(a1), FadeIn(right), run_time=0.4)
        hear(self, "look at the output", lead=0.2)
        self.play(Create(a2), FadeIn(bot), run_time=0.4)
        hear(self, "then commit", lead=0.2)
        self.play(Create(a3), FadeIn(left), run_time=0.4)
        hear(self, "code and the result", lead=0.2)
        self.play(FadeIn(code), FadeIn(res), run_time=0.3)
        self.play(code.animate.move_to([-3.4, 0.2, 0]).set_opacity(0), res.animate.move_to([-3.4, 0.2, 0]).set_opacity(0), run_time=0.5)
        hear(self, "Repeat", lead=0.1)
        self.add(rider)
        self.play(MoveAlongPath(rider, Polygon([0.0, 1.55, 0], [2.9, 0.2, 0], [0.0, -1.3, 0], [-2.7, 0.2, 0], [0.0, 1.55, 0], stroke_width=0)), Create(a4), run_time=1.6, rate_func=linear)
        self.play(FadeOut(rider), run_time=0.15)
        hear(self, "tag the commit", lead=0.3)
        self.play(Create(flag), FadeIn(tag), run_time=0.5)
        done(self)


class B44_GoodCommits(Scene):
    """The 'and' message crossed out beside the one-change message; six message types; one typed example."""
    def construct(self):
        bad = pB_card(["fixed stuff and added new", "feature and changed config"], -3.0, 2.2, 5.4)
        xm = x_mark(0.2, 2.2, r=0.4, w=10)
        good = pB_card(["Fix off-by-one in", "loop bounds"], 3.2, 2.2, 4.6)
        ck = check(5.55, 2.2, s=0.3, w=9)
        types = VGroup(*[chip(t, 0, 0, size=32) for t in ["feat", "fix", "data", "analysis", "docs", "config"]]).arrange(RIGHT, buff=0.25).move_to([0.0, 0.3, 0])
        ex = plaque("analysis(fig3): reproduce\nwith corrected normalization".split("\n")[0], 0, -1.7, w=8.8, h=1.7, size=32)
        ex2 = M("with corrected normalization", 32).move_to([0.0, -2.05, 0])
        ex.label.move_to([0.0, -1.35, 0])
        ghosts = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.4, width=1.6, height=0.8, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x, 0.3, 0]), num_dashes=24) for x in [-4.8, -2.9, -1.0, 1.1, 3.1, 4.9]])
        gex = DashedVMobject(Rectangle(width=8.8, height=1.7, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([0.0, -1.7, 0]), num_dashes=48)
        self.add(ghosts, gex)
        hear(self, "One logical change", lead=0.3)
        self.play(FadeIn(bad), FadeIn(good), run_time=0.5)
        hear(self, "the word and", lead=0.3)
        self.play(Create(xm), run_time=0.35)
        hear(self, "make two commits", lead=0.3)
        self.play(Create(ck), run_time=0.3)
        hear(self, "consistent message style", lead=0.3)
        self.play(FadeOut(ghosts), LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in types], lag_ratio=0.2), run_time=1.3)
        hear(self, "reads like a change log", lead=0.3)
        self.play(FadeOut(gex), FadeIn(ex), FadeIn(ex2), run_time=0.5)
        done(self)


class B50_BranchOff(Scene):
    """Main as it stands; a branch forks and gets its own commits; main stays untouched."""
    def construct(self):
        title = pB_act_title("V · Branches And Merges")
        xs = [-4.4, -1.8, 0.8]
        discs = [pA_disc(x, 1.0, 0.5) for x in xs]
        arrows = [pA_arrow([xs[i] - 0.6, 1.0], [xs[i - 1] + 0.6, 1.0], 7) for i in (1, 2)]
        main = chip("main", 0.8, 2.3, size=34)
        fork = Line([0.8, 0.5, 0], [2.6, -0.85, 0], color=INK, stroke_width=6)
        d4, d5 = pA_disc(2.6, -1.1, 0.5), pA_disc(5.0, -1.1, 0.5)
        a45 = pA_arrow([4.4, -1.1], [3.2, -1.1], 7)
        lab = chip("explore/fc-cutoff-1.5", 3.1, -2.5, mono=True, size=30)
        untouched = chip("main untouched", -3.0, -1.0, size=34)
        self.play(FadeIn(title), run_time=0.4)
        self.add(*discs, *arrows)
        hear(self, "A reviewer asks", lead=0.1)
        self.play(FadeIn(main), run_time=0.3)
        hear(self, "Make a branch", lead=0.3)
        self.play(Create(fork), FadeIn(d4), FadeIn(lab), run_time=0.6)
        hear(self, "parallel version", lead=0.3)
        self.play(FadeIn(d5), Create(a45), run_time=0.5)
        hear(self, "main untouched", lead=0.3)
        self.play(FadeIn(untouched), run_time=0.4)
        done(self)


class B60_FixedFlag(Scene):
    """A tag stays where it was planted while main slides forward with each new commit."""
    def construct(self):
        title = pB_act_title("VI · Tags And Time Travel")
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        discs = [pA_disc(x, 0.5, 0.5) for x in xs]
        arrows = [pA_arrow([xs[i] - 0.6, 0.5], [xs[i - 1] + 0.6, 0.5], 7) for i in range(1, 5)]
        main = chip("main", 0.0, 1.9, size=34)
        flag = pA_flag(0.0, -1.9, 1.1)
        tl = chip("v1.0-submission", 3.0, -1.4, mono=True, size=30)
        co = chip("git checkout v1.0-submission", -0.4, -2.85, mono=True, size=30)
        up = pA_arrow([-1.2, -2.35], [-0.2, -1.95], 6)
        self.play(FadeIn(title), run_time=0.4)
        self.add(discs[0], discs[1], discs[2], arrows[0], arrows[1])
        hear(self, "A tag is a flag", lead=0.1)
        self.play(FadeIn(main), Create(flag), FadeIn(tl), run_time=0.5)
        hear(self, "Branch names slide forward", lead=0.2)
        self.play(FadeIn(discs[3]), Create(arrows[2]), main.animate.move_to([2.2, 1.9, 0]), run_time=0.6)
        self.play(FadeIn(discs[4]), Create(arrows[3]), main.animate.move_to([4.4, 1.9, 0]), run_time=0.6)
        hear(self, "check that tag out", lead=0.3)
        self.play(FadeIn(co), Create(up), run_time=0.5)
        done(self)


# ═════════════════════════════ PART C — B70 B72 B75 B77 B78 (Act VII) ═════════════════════════════
def pC_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pC_poly(pts, color=INK, w=6):
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_as_corners([[p[0], p[1], 0] for p in pts])
    return m


def pC_page(x, y, w=1.3, h=1.7):
    pg = Rectangle(width=w, height=h, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    ls = VGroup(*[Line([x - w * 0.3, y + h * 0.3 - 0.3 * i, 0], [x + w * 0.3, y + h * 0.3 - 0.3 * i, 0], color=BAR2, stroke_width=5) for i in range(3)])
    return VGroup(pg, ls)


class B70_CommitBeforeSubmit(Scene):
    """Commit, submit, queue, run; a thread from the commit to the hash in the job log."""
    def construct(self):
        title = pC_act_title("VII · Git On Slurm")
        base = Line([-5.8, 0.2, 0], [5.8, 0.2, 0], color=BAR1, stroke_width=5)
        disc = pA_disc(-5.0, 0.2, 0.45)
        c_commit = chip("commit first", -4.2, 1.55, size=34)
        sb = chip("sbatch", -1.3, 1.55, mono=True, size=32)
        tick = Line([-2.4, 0.2, 0], [-2.4, 0.85, 0], color=INK, stroke_width=7)
        queue = Rectangle(width=3.0, height=0.5, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([-0.9, 0.2, 0])
        qlab = T("queue", 34).move_to([-0.9, -0.55, 0])
        job = Rectangle(width=2.0, height=0.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([2.1, 0.2, 0])
        jlab = T("job runs", 34).move_to([2.1, -0.65, 0])
        page = pC_page(5.0, 0.2, 1.3, 1.7)
        logchip = chip("d9c1f37", 4.9, 1.75, mono=True, size=30)
        thread = pC_poly([(-5.0, -0.35), (-5.0, -1.7), (5.0, -1.7), (5.0, -0.8)], INK, 6)
        tlab = T("same commit", 34).move_to([0.0, -2.35, 0])
        hlab = T("hash in the log", 34).move_to([4.2, 2.7, 0])
        self.play(FadeIn(title), Create(base), run_time=0.5)
        hear(self, "runs later", lead=0.9)
        self.play(FadeIn(queue), FadeIn(qlab), FadeIn(job), FadeIn(jlab), run_time=0.6)
        hear(self, "Commit before", lead=0.2)
        self.play(FadeIn(disc), FadeIn(c_commit), run_time=0.4)
        hear(self, "submit", lead=0.1)
        self.play(Create(tick), FadeIn(sb), run_time=0.4)
        hear(self, "traces to one commit", lead=0.4)
        self.play(Create(thread), FadeIn(tlab), run_time=0.8)
        hear(self, "print that commit", lead=0.2)
        self.play(FadeIn(page), FadeIn(logchip), FadeIn(hlab), run_time=0.5)
        done(self)


class B72_RealPartitions(Scene):
    """Explorer: short* and sharing; AICR: cpu*; 'compute' crossed out; sinfo."""
    def construct(self):
        ex = T("Explorer", 38).move_to([-3.1, 2.1, 0])
        ai = T("AICR", 38).move_to([3.2, 2.1, 0])
        iso1 = Iso(-3.55, -0.2, 0.7)
        rk1, lt1 = explorer_rack(iso1)
        iso2 = Iso(2.7, -0.55, 0.55)
        rk2, lt2 = aicr_rack(iso2)
        p1 = chip("short*   2-00:00:00", -3.1, -1.5, mono=True, size=30)
        p2 = chip("sharing  1:00:00", -3.1, -2.4, mono=True, size=30)
        p3 = chip("cpu*     1-00:00:00", 3.2, -1.5, mono=True, size=30)
        comp = chip("compute", 0.0, 2.9, mono=True, size=30)
        xm = x_mark(1.9, 2.9, r=0.4, w=9)
        sinfo = chip("sinfo", 3.2, -2.5, mono=True, size=32)
        star = T("* default", 32).move_to([-3.1, -3.15, 0])
        hear(self, "Use a name from", lead=0.2)
        self.play(FadeIn(comp), Create(xm), run_time=0.4)
        hear(self, "on Explorer", lead=0.3)
        self.play(FadeIn(ex), FadeIn(rk1), FadeIn(lt1), run_time=0.4)
        self.play(FadeIn(p1), run_time=0.3)
        hear(self, "sharing", lead=0.2)
        self.play(FadeIn(p2), FadeIn(star), run_time=0.3)
        hear(self, "On A-I-C-R|AICR|A I C R", lead=0.3)
        self.play(FadeIn(ai), FadeIn(rk2), FadeIn(lt2), run_time=0.4)
        self.play(FadeIn(p3), run_time=0.3)
        hear(self, "Check sinfo", lead=0.2)
        self.play(FadeIn(sinfo), run_time=0.3)
        done(self)


class B75_QueueWindow(Scene):
    """sbatch at commit A; an edit during the queue makes B; the job starts at B and logs B's hash."""
    def construct(self):
        base = Line([-5.8, 1.2, 0], [5.8, 1.2, 0], color=BAR1, stroke_width=5)
        sb = chip("sbatch", -4.2, 2.3, mono=True, size=32)
        tick = Line([-4.2, 1.2, 0], [-4.2, 1.85, 0], color=INK, stroke_width=7)
        queue = Rectangle(width=4.6, height=0.5, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([-1.8, 1.2, 0])
        qlab = T("queue: hours", 34).move_to([-1.8, 0.55, 0])
        da = pA_disc(-4.2, -1.1, 0.42)
        ha = pA_hash("a3f8c21", -4.2, -1.95)
        edit = chip("edit", -1.0, 2.3, size=34)
        db = pA_disc(-1.0, -1.1, 0.42)
        hb = pA_hash("b7d2e14", -1.0, -1.95)
        arr = pA_arrow([-1.55, -1.1], [-3.65, -1.1], 7)
        start = Line([0.8, 1.2, 0], [0.8, 1.85, 0], color=INK, stroke_width=7)
        slab = T("job starts", 34).move_to([1.0, 2.3, 0])
        thread = pC_poly([(-0.6, -1.1), (0.8, -1.1), (0.8, 0.9)], INK, 6)
        log = chip("b7d2e14", 4.1, 2.1, mono=True, size=30)
        stamp = chip("not tested", 4.3, -1.5, size=34)
        self.play(Create(base), run_time=0.4)
        hear(self, "when the job starts", lead=0.6)
        self.play(FadeIn(da), FadeIn(ha), Create(tick), FadeIn(sb), run_time=0.5)
        hear(self, "queue for hours", lead=0.3)
        self.play(FadeIn(queue), FadeIn(qlab), run_time=0.5)
        hear(self, "Edit the script", lead=0.2)
        self.play(FadeIn(edit), FadeIn(db), FadeIn(hb), Create(arr), run_time=0.6)
        hear(self, "may run newer code", lead=0.3)
        self.play(Create(start), FadeIn(slab), Create(thread), run_time=0.5)
        hear(self, "newer hash", lead=0.2)
        self.play(FadeIn(log), FadeIn(stamp), run_time=0.4)
        done(self)


class B77_ThreeMoreSpots(Scene):
    """Three cards: dirty results block the next submit; two jobs, one checkout; a tag that stays in the checkout."""
    def construct(self):
        xs = [-4.3, 0.0, 4.3]
        cards = [Rectangle(width=3.9, height=4.3, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, 0.1, 0]) for x in xs]
        shadows = [Rectangle(width=3.9, height=4.3, fill_color=BOX_R, fill_opacity=1, stroke_width=0).move_to([x + 0.1, 0.0, 0]) for x in xs]
        labs = [T(t, 34).move_to([x, -1.65, 0]) for t, x in zip(["dirty results", "shared checkout", "tag stays put"], xs)]
        # card 1: a results page with a dirty dot; the sbatch arrow is barred
        pg = pC_page(-4.3, 1.1, 1.2, 1.5)
        dirty = Dot([-3.75, 1.7, 0], radius=0.15, color=TERRA)
        sb = chip("sbatch", -4.3, -0.45, mono=True, size=30)
        xm1 = x_mark(-2.8, -0.45, r=0.35, w=9)
        # card 2: two job boxes reaching into one checkout
        j1 = VGroup(Rectangle(width=0.9, height=0.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-0.9, 1.5, 0]))
        j2 = VGroup(Rectangle(width=0.9, height=0.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.9, 1.5, 0]))
        co = Rectangle(width=1.4, height=0.9, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.0, -0.3, 0])
        ar1 = pA_arrow([-0.8, 1.1], [-0.2, 0.2], 6)
        ar2 = pA_arrow([0.8, 1.1], [0.2, 0.2], 6)
        # card 3: a flag inside a rack; no arrow to GitHub until push
        iso3 = Iso(3.2, -0.5, 0.55)
        rk, lt = explorer_rack(iso3)
        fl = pA_flag(4.35, 0.55, 0.8)
        gh = logo_chip("github", 5.2, 1.9, h=0.9)
        push = pA_arrow([4.55, 1.0], [4.95, 1.45], 6)
        pl = chip("push", 3.5, 1.9, mono=True, size=30)
        hear(self, "Three more", lead=0.1)
        self.play(*[FadeIn(s) for s in shadows], *[FadeIn(c) for c in cards], run_time=0.5)
        hear(self, "results a run writes", lead=0.2)
        self.play(FadeIn(pg), FadeIn(dirty), FadeIn(labs[0]), run_time=0.4)
        hear(self, "next submit", lead=0.2)
        self.play(FadeIn(sb), Create(xm1), run_time=0.4)
        hear(self, "inside the job", lead=0.3)
        self.play(FadeIn(co), FadeIn(j1), FadeIn(j2), FadeIn(labs[1]), run_time=0.4)
        self.play(Create(ar1), Create(ar2), run_time=0.4)
        hear(self, "a tag made", lead=0.3)
        self.play(FadeIn(rk), FadeIn(lt), Create(fl), FadeIn(labs[2]), FadeIn(gh), run_time=0.6)
        hear(self, "pushes it", lead=0.3)
        self.play(FadeIn(pl), Create(push), run_time=0.4)
        done(self)


class B78_JobRecord(Scene):
    """Twelve record items; the header covers the first few; you add the rest."""
    def construct(self):
        items = ["commit and tag", "job and node", "start and end", "exact command", "parameters", "random seeds",
                 "input checksums", "software", "hardware", "container image", "output folder", "exit status"]
        xs = [-4.3, 0.0, 4.3]
        ys = [2.2, 0.85, -0.5, -1.85]
        pills, labels = [], []
        for i, t in enumerate(items):
            x, y = xs[i % 3], ys[i // 3]
            p = pill(x, y, 3.9, h=0.9, fill="#A39E94")
            lb = T(t, 34).move_to([x, y, 0])
            pills.append(p); labels.append(lb)
        dots = [Dot([xs[i % 3] - 1.7, ys[i // 3], 0], radius=0.13, color=TERRA) for i in range(3)]
        leg = T("printed by the header", 34).move_to([-3.2, -3.0, 0])
        ldot = Dot([-5.6, -3.0, 0], radius=0.13, color=TERRA)
        add = T("you add the rest", 34).move_to([3.4, -3.0, 0])
        hear(self, "A full job record", lead=0.2)
        self.play(*[FadeIn(p) for p in pills], run_time=0.5)
        order = [(0, "more than a commit"), (1, "job, node"), (2, "start and end"), (3, "exact command"), (4, "every parameter"), (5, "random seed"),
                 (6, "input paths"), (7, "software versions"), (8, "hardware"), (10, "output folder"), (11, "exit status")]
        for i, ph in order:
            hear(self, ph, lead=0.15)
            self.play(FadeIn(labels[i]), *([FadeIn(labels[9])] if i == 10 else []), run_time=0.2)
        hear(self, "The header prints", lead=0.2)
        self.play(*[FadeIn(d) for d in dots], FadeIn(leg), FadeIn(ldot), run_time=0.4)
        hear(self, "You add the rest", lead=0.1)
        self.play(FadeIn(add), *[p.animate.set_fill("#FFFFFF") for p in pills[3:]], run_time=0.5)
        done(self)


# ═════════════════════════════ PART D — B83 B84 B85 (Act VIII) ═════════════════════════════
def pD_page(x, y, w=1.1, h=1.4, stroke=True):
    pg = Rectangle(width=w, height=h, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK if stroke else "#FFFFFF", stroke_width=4 if stroke else 0).move_to([x, y, 0])
    ls = VGroup(*[Line([x - w * 0.3, y + h * 0.28 - 0.28 * i, 0], [x + w * 0.3, y + h * 0.28 - 0.28 * i, 0], color=BAR2, stroke_width=5) for i in range(3)])
    return VGroup(pg, ls)


class B83_BigFilesNotebooks(Scene):
    """Big data stays in storage, Git keeps a manifest; notebook outputs lift off with nbstripout."""
    def construct(self):
        title_l = T("VIII · Daily Habits And Questions", 40)
        title_l.move_to([-6.1 + title_l.width / 2, 3.0, 0])
        git = logo_chip("git", -4.9, 1.9, h=1.2)
        box = Rectangle(width=2.6, height=1.7, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-4.2, 0.1, 0])
        man = pD_page(-4.2, 0.1, 0.8, 1.0, stroke=False)
        mlab = T("manifest", 34).move_to([-4.2, -1.2, 0])
        iso = Iso(-0.2, -1.2, 0.65)
        rk, lt = explorer_rack(iso)
        stor = T("storage", 34).move_to([1.6, -1.2, 0])
        data = Rectangle(width=1.1, height=0.8, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-1.9, 1.5, 0])
        dlab = T("big data", 34).move_to([-1.9, 2.2, 0])
        arr = pA_arrow([-2.8, 0.4], [-0.9, 0.4], 7)
        lfs = chip("Git LFS", -3.4, -2.55, mono=True, size=30)
        dvc = chip("DVC", -0.9, -2.55, mono=True, size=30)
        jup = logo_chip("jupyter", 2.6, 2.0, h=1.2)
        nb = pD_page(4.1, 0.3, 2.3, 3.0)
        outs = VGroup(*[Rectangle(width=1.5, height=0.3, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([4.1, 0.3 - 0.0 - 0.55 + 0.55 * i - 0.55, 0]) for i in range(3)])
        outs.move_to([4.1, -0.35, 0])
        nbs = chip("nbstripout", 4.0, -2.2, mono=True, size=30)
        jt = chip("Jupytext", 4.0, -3.0, mono=True, size=30)
        self.play(FadeIn(title_l), run_time=0.4)
        hear(self, "large datasets", lead=0.2)
        self.play(FadeIn(git), FadeIn(box), FadeIn(man), FadeIn(mlab), run_time=0.5)
        hear(self, "Not directly", lead=0.2)
        self.play(FadeIn(data), FadeIn(dlab), run_time=0.3)
        hear(self, "Git L F S", lead=0.3)
        self.play(FadeIn(lfs), run_time=0.25)
        hear(self, "D V C", lead=0.3)
        self.play(FadeIn(dvc), Create(arr), FadeIn(rk), FadeIn(lt), FadeIn(stor), run_time=0.5)
        self.play(data.animate.move_to([0.4, 0.45, 0]).scale(0.6), FadeOut(dlab), run_time=0.7)
        hear(self, "Jupyter notebooks", lead=0.2)
        self.play(FadeIn(jup), FadeIn(nb), FadeIn(outs), run_time=0.5)
        hear(self, "strip them", lead=0.3)
        self.play(FadeIn(nbs), outs.animate.shift(RIGHT * 0.0).set_opacity(0.0), run_time=0.7)
        hear(self, "Jupytext", lead=0.3)
        self.play(FadeIn(jt), run_time=0.3)
        done(self)


class B84_UndoSafely(Scene):
    """Amend swaps the last commit; revert adds an undo commit; reset --hard on a shared branch is crossed out."""
    def construct(self):
        xs = [-5.0, -3.0, -1.0]
        ys = [2.0, 0.3, -1.5]

        def chain(y):
            ds = [pA_disc(x, y, 0.42) for x in xs]
            ars = [pA_arrow([xs[i] - 0.5, y], [xs[i - 1] + 0.5, y], 6) for i in (1, 2)]
            return ds, ars
        c1, a1 = chain(ys[0]); c2, a2 = chain(ys[1]); c3, a3 = chain(ys[2])
        fix = pA_disc(-1.0, ys[0], 0.42)
        amend = chip("commit --amend", 3.4, ys[0], mono=True, size=30)
        d4 = pA_disc(1.0, ys[1], 0.42)
        ar4 = pA_arrow([0.5, ys[1]], [-0.5, ys[1]], 6)
        undo = CurvedArrow([1.0, ys[1] + 0.5, 0], [-1.0, ys[1] + 0.5, 0], angle=-1.0, color=INK, stroke_width=6)
        revert = chip("git revert", 3.9, ys[1], mono=True, size=30)
        reset = chip("git reset --hard", 3.4, ys[2], mono=True, size=30)
        xm = x_mark(0.3, ys[2], r=0.45, w=10)
        shared = T("shared branch", 34).move_to([-2.0, -2.45, 0])
        hear(self, "fix the last commit", lead=0.3)
        self.add(*c1, *a1)
        self.play(FadeOut(c1[2]), FadeIn(fix), FadeIn(amend), run_time=0.6)
        hear(self, "already shared", lead=0.3)
        self.add(*c2, *a2)
        self.play(FadeIn(d4), Create(ar4), FadeIn(revert), run_time=0.5)
        self.play(Create(undo), run_time=0.4)
        hear(self, "never run", lead=0.2)
        self.add(*c3, *a3)
        self.play(FadeIn(reset), FadeIn(shared), run_time=0.4)
        hear(self, "throws work away", lead=0.3)
        self.play(FadeOut(c3[2]), FadeOut(c3[1]), Create(xm), run_time=0.6)
        done(self)


class B85_ConflictsAndStash(Scene):
    """Conflict markers around two versions; keep one, add, commit; stash and pop."""
    def construct(self):
        page = Rectangle(width=4.8, height=3.4, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-3.4, 0.8, 0])
        m1 = M("<<<<<<<", 32).move_to([-4.6, 2.1, 0])
        v1 = Rectangle(width=3.0, height=0.45, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([-3.4, 1.5, 0])
        m2 = M("=======", 32).move_to([-4.6, 0.8, 0])
        v2 = Rectangle(width=3.0, height=0.45, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([-3.4, 0.2, 0])
        m3 = M(">>>>>>>", 32).move_to([-4.6, -0.5, 0])
        add = chip("git add", -4.7, -2.1, mono=True, size=30)
        com = chip("git commit", -1.9, -2.1, mono=True, size=30)
        drawer = Rectangle(width=3.0, height=1.5, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.6, 1.6, 0])
        half = pD_page(3.6, 0.0, 0.9, 1.1, stroke=False)
        stash = chip("git stash", 3.6, -1.0, mono=True, size=30)
        pop = chip("git stash pop", 3.6, -2.1, mono=True, size=30)
        self.play(FadeIn(page), FadeIn(drawer), FadeIn(stash), FadeIn(pop), run_time=0.4)
        hear(self, "same lines", lead=0.3)
        self.play(FadeIn(m1), FadeIn(v1), FadeIn(m2), FadeIn(v2), FadeIn(m3), run_time=0.6)
        hear(self, "keep the version", lead=0.3)
        self.play(FadeOut(v2), run_time=0.3)
        hear(self, "delete the markers", lead=0.2)
        self.play(FadeOut(m1), FadeOut(m2), FadeOut(m3), v1.animate.move_to([-3.4, 0.8, 0]), run_time=0.5)
        hear(self, "git add", lead=0.2)
        self.play(FadeIn(add), run_time=0.25)
        hear(self, "and commit", lead=0.2)
        self.play(FadeIn(com), run_time=0.25)
        hear(self, "git stash", lead=0.3)
        self.play(FadeIn(half), run_time=0.4)
        self.play(half.animate.move_to([3.6, 1.6, 0]).set_opacity(0.0), run_time=0.5)
        hear(self, "brings them back", lead=0.4)
        self.play(half.animate.move_to([3.6, 0.0, 0]).set_opacity(1.0), run_time=0.6)
        done(self)


for _cls in (B10_ReviewerAsks, B11_OneTimeline, B12_Snapshots, B13_BranchAndTag, B14_ThreePlaces, B15_FourMoments, B20_TheExample, B30_CodeNotResults, B40_RunInspectCommit, B44_GoodCommits, B50_BranchOff, B60_FixedFlag, B70_CommitBeforeSubmit, B72_RealPartitions, B75_QueueWindow, B77_ThreeMoreSpots, B78_JobRecord, B83_BigFilesNotebooks, B84_UndoSafely, B85_ConflictsAndStash):
    _cls.play = ST.play
