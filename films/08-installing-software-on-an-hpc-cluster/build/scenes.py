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


# ─────────────── midpoint guard: GATE T and Gate V sample each clip at its midpoint ───────────────
class ST:
    """Midpoint guard: no animation straddles the clip midpoint. Attached to every beat class at the
    bottom of scenes.py (run.sh finds scenes only by the literal `(Scene)`)."""
    def play(self, *anims, **kw):
        if not all(isinstance(a, Wait) for a in anims):
            kw["run_time"] = guard(self, float(kw.get("run_time", 1.0)))
        return Scene.play(self, *anims, **kw)


def guard(self, rt):
    """If an animation of length rt starting now would straddle the midpoint, either shorten it to land
    before the midpoint or wait until just after it. Returns the run time to use."""
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


def done(self):
    """finish() plus a pacing report (a clip must not outrun its audio: compile centre-cuts it)."""
    bid = type(self).__name__.split("_")[0]
    t = _elapsed(self)
    tgt = _TARGET.get(bid, 0)
    print(f"[pace] {bid} content={t:.2f}s target={tgt:.2f}s" + ("  OVER" if t > tgt - 0.1 else ""))
    if tgt:
        self.wait(max(0.05, tgt - t - 0.05))     # end 0.05 s under the audio (4K frame rounding)
    else:
        self.wait(2.0)


# ═════════════════════════════ the lecture's cast (shared by every act) ═════════════════════════════
# One cast, whole film. The same object is the same picture in every beat:
#   EXPLORER  small dark rack, 2 slabs      (Northeastern's own cluster)      explorer_rack()
#   AICR      large dark rack, 4 slabs, wide (the shared GPU cluster)          aicr_rack()
#   JOB       a small kraft box with one terracotta tape                        job_box()
#   HOME      a small closed kraft box                                          home_box()
#   SCRATCH   a wide open kraft bin                                             scratch_bin()  -> (back, front)
#   PROJECT   a tall white cabinet with ghost drawer lines                      project_cabinet()
#   GPU       a dark block with a ghost light that turns terracotta when busy   gpu_block()    -> (body, light)
MONO = "Menlo"


def M(s, size=34, color=INK):
    """Mono label for real paths, usernames and commands."""
    return Text(s, font=MONO, color=color, font_size=size)


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


def project_cabinet(iso, x0=0.0, y0=0.0, z0=0.0):
    body = iso.box(x0, y0, z0, 1.3, 1.1, 2.0, PAGE_TOP, PAGE_L, PAGE_R)
    lines = VGroup(*[Line(iso.p(x0 + 0.12, y0, z0 + 2.0 * f), iso.p(x0 + 1.18, y0, z0 + 2.0 * f), color=BAR1, stroke_width=4)
                     for f in (0.34, 0.67)])
    return VGroup(body, lines)


def gpu_block(iso, x0=0.0, y0=0.0, z0=0.0):
    body = iso.box(x0, y0, z0, 1.0, 1.0, 0.5, DARK_TOP, DARK_L, DARK_R)
    light = Dot(iso.p(x0 + 0.2, y0, z0 + 0.25), radius=0.07, color=GHOST)
    return body, light
# ═════════════════════════════ PART A · B10, B11 (Act I) · B21 (Act II) · B31 (Act III) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PA_ / pa_ / b1x_ / b2x_ / b3x_ so the parts never collide.
PA_KRAFT = "#9C8462"                        # deep kraft: connectors and network lines (ink lines fuse the things they join, GATE T)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T)


def pa_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_left(mob, x, y):
    """Place a text by its LEFT edge, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pa_token(x, y, s=1.0):
    """A person token standing with its feet at (x, y) (the same token as the earlier films)."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head).set_z_index(7)


def pa_xmark(x, y, s=0.35, color=BAR1, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w)).set_z_index(8)


def pa_plinth(iso, w, d, m=0.15, h=0.1):
    """A thin dark plinth under a pale container (Gate V contrast): its top is the floor (z = 0)."""
    return iso.box(-m, -m, -h, w + 2 * m, d + 2 * m, h, DARK_TOP, DARK_L, DARK_R).set_z_index(-1)


def pa_drop(self, mobs, rt=0.55, lag=0.2, dist=5.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt, rate_func=ease_in)


def pa_slide_in(self, mob, vec, rt=0.7, with_=()):
    """Slide a whole object in from off-stage, fully opaque."""
    rt = guard(self, rt)
    mob.shift(-vec)
    self.add(mob)
    self.play(mob.animate.shift(vec), *with_, run_time=rt)


def pa_gauge(x, y, w=0.4, h=1.4, n=5):
    """A quota gauge: a grey outline and n grey segments (with gaps) stacked from the bottom. Returns (outline, segments)."""
    out = Rectangle(width=w, height=h, stroke_color=BAR1, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    gap, sh = 0.06, (h - 0.06 * (n + 1)) / n
    segs = VGroup(*[Rectangle(width=w - 0.12, height=sh, fill_color=BAR1, fill_opacity=1, stroke_width=0)
                    .move_to([x, y - h / 2 + gap + sh / 2 + k * (sh + gap), 0]) for k in range(n)])
    return out, segs


def pa_fill(self, segs, k0, k1, rt=0.6):
    """Raise the gauge from segment k0 to k1 (exclusive), one segment after another."""
    rt = guard(self, rt)
    self.play(LaggedStart(*[GrowFromEdge(segs[k], DOWN) for k in range(k0, k1)], lag_ratio=0.35), run_time=rt)


def pa_env_box(iso, s=0.6, outline=PA_SMALL):
    """A conda environment / generic binary: a small white box (small object, dark-kraft outline)."""
    return iso.box(0, 0, 0, s, s, s * 0.75, PAGE_TOP, PAGE_L, PAGE_R, sw=3).set_stroke(outline)


def pa_file_dots(n, x0, x1, y0, y1, seed=7, r=0.045):
    rng = np.random.RandomState(seed)
    return VGroup(*[Dot([rng.uniform(x0, x1), rng.uniform(y0, y1), 0], radius=r, color=BAR1) for _ in range(n)])


def pa_pour(self, dots, iso, x0, y0, w, d, z, rt=1.0, seed=3):
    """The file dots pour onto a box top (a random point each on the top face) and shrink away."""
    rt = guard(self, rt)
    rng = np.random.RandomState(seed)
    self.add(dots)
    self.play(LaggedStart(*[dd.animate.move_to(iso.p(x0 + rng.uniform(0.1, w - 0.1), y0 + rng.uniform(0.1, d - 0.1), z)).scale(0.2)
                            for dd in dots], lag_ratio=0.04), run_time=rt, rate_func=ease_in)
    self.remove(dots, *dots)


# ─────────────── B10 · laptop vs cluster: two columns, row by row ───────────────
B10_LAP = Iso(-5.3, -1.6, 0.75)                                   # the laptop, far left
B10_RACK = Iso(0.15, -1.9, 0.75)                                 # the Explorer rack, between the columns
B10_ROWS_Y = (0.95, 0.15, -0.65, -1.45)
B10_XL, B10_XR = -3.9, 1.5                                       # left edge of each label column
B10_LEFT = ("root", "one user", "local disk", "generic binaries")
B10_RIGHT = ("user space only", "hundreds of users", "shared filesystem, quota", "match cluster libraries")


def b10_laptop():
    """A small laptop: a kraft base, a dark screen standing on its back edge."""
    iso = B10_LAP
    screen = iso.quad([(0.1, 1.3, 0.1), (1.5, 1.3, 0.1), (1.5, 1.3, 1.15), (0.1, 1.3, 1.15)], DARK_L, sw=4)
    base = iso.box(0, 0, 0, 1.6, 1.3, 0.1)
    keys = iso.quad([(0.25, 0.3, 0.1), (1.35, 0.3, 0.1), (1.35, 0.9, 0.1), (0.25, 0.9, 0.1)], GHOST, sw=0)
    return VGroup(screen, base, keys)


B10_WL, B10_WR = (0.82, 1.55, 1.7, 2.83), (2.77, 3.27, 4.4, 4.0)       # measured label widths (fixed centres: Gate A's stub over-estimates text width)


def b10_row(k, left=True):
    x, w = (B10_XL, B10_WL[k]) if left else (B10_XR, B10_WR[k])
    return T(B10_LEFT[k] if left else B10_RIGHT[k], 36).move_to([x + w / 2, B10_ROWS_Y[k], 0])


def b10_binary():
    """The generic binary, born on the laptop's base."""
    return pa_env_box(Iso(B10_LAP.ox, B10_LAP.oy, 0.75), s=0.7).shift(B10_LAP.v(0.45, 0.3, 0.1))


class B10_LaptopVsCluster(Scene):
    def construct(self):
        self.add(pa_title("I · Why HPC Is Different"), b10_laptop())
        until(self, "root access")
        self.play(FadeIn(b10_row(0), shift=DOWN * 0.3), run_time=0.3)
        until(self, "one user")
        self.play(FadeIn(b10_row(1), shift=DOWN * 0.3), run_time=0.3)
        until(self, "a local disk")
        self.play(FadeIn(b10_row(2), shift=DOWN * 0.3), run_time=0.3)
        until(self, "and generic downloads")
        self.play(FadeIn(b10_row(3), shift=DOWN * 0.3), run_time=0.3)
        until(self, "The cluster:")
        st, li = explorer_rack(B10_RACK)
        pa_slide_in(self, VGroup(st, li), LEFT * 7.0, 0.6)
        until(self, "user space only")
        self.play(FadeIn(b10_row(0, False), shift=DOWN * 0.3), run_time=0.3)
        until(self, "hundreds of people")
        self.play(FadeIn(b10_row(1, False), shift=DOWN * 0.3), run_time=0.3)
        until(self, "a network filesystem")
        self.play(FadeIn(b10_row(2, False), shift=DOWN * 0.3), run_time=0.3)
        until(self, "and builds that should link")
        self.play(FadeIn(b10_row(3, False), shift=DOWN * 0.3), run_time=0.3)
        until(self, "own compilers")
        self.play(LaggedStart(*[l.animate.set_color(TERRA) for l in li], lag_ratio=0.3), run_time=0.5)
        until(self, "A generic binary from")
        bn = b10_binary()
        self.play(GrowFromCenter(bn), run_time=0.4)
        until(self, "ignores all of that", lead=0.4)
        top = B10_RACK.p(0.65, 0.65, 0.92)
        self.play(bn.animate.move_to([top[0], top[1] + 0.3, 0]), run_time=0.9)
        until(self, "so it runs slower")
        self.play(Create(pa_xmark(top[0], top[1] + 0.3, 0.5)), run_time=0.35)
        done(self)


# ─────────────── B11 · do not build on the login node; mind the filesystem ───────────────
B11_RACK = Iso(-5.0, -1.55, 0.7)                                  # the login node, left
B11_JOB = Iso(-2.3, -2.95, 0.75)                                  # the job box, lower left
B11_TOK_Y, B11_TOK_X = -1.35, (-3.7, -3.2, -2.7, -2.2, -1.7)      # five people beside the node
B11_HOME = Iso(2.6, 0.7, 0.7)                                     # the home box, upper right
B11_NODES_X, B11_NODE_Y = (1.1, 2.7, 4.3), -2.6                  # three small nodes under it
B11_NET_Y = -0.75                                                 # the network line
B11_CLOCK = np.array([5.55, -2.05, 0.0])


def b11_build_glyph(c):
    """The build: a gear with a hammer across it. Small object, dark-kraft outlines."""
    cx, cy = c[0], c[1]
    r = 0.3
    teeth = VGroup(*[Square(side_length=r * 0.38, fill_color=BAR2, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=2)
                     .move_to([cx + r * np.cos(a), cy + r * np.sin(a), 0]).rotate(a) for a in np.arange(0, 2 * PI, PI / 4)])
    ring = Circle(radius=r, fill_color=BAR2, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([cx, cy, 0])
    hub = Circle(radius=r * 0.32, fill_color=STAGE, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([cx, cy, 0])
    handle = Line([cx - 0.05, cy - 0.05, 0], [cx + 0.5, cy + 0.5, 0], color=PA_SMALL, stroke_width=7)
    head = Rectangle(width=0.36, height=0.2, fill_color=BAR1, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([cx + 0.5, cy + 0.5, 0]).rotate(PI / 4)
    return VGroup(teeth, ring, hub, handle, head).set_z_index(9)


def b11_node(x):
    return Iso(x, B11_NODE_Y, 0.6).box(0, 0, 0, 0.9, 0.9, 0.42, DARK_TOP, DARK_L, DARK_R)


def b11_net():
    """The network: a kraft trunk line with a drop from the home box and a riser to each node."""
    hb = B11_HOME.p(0.6, 0.6, 0)
    trunk = Line([0.7, B11_NET_Y, 0], [5.0, B11_NET_Y, 0], color=PA_KRAFT, stroke_width=5)
    drop = Line([hb[0], hb[1] - 0.1, 0], [hb[0], B11_NET_Y, 0], color=PA_KRAFT, stroke_width=5)
    tops = [Iso(x, B11_NODE_Y, 0.6).p(0.45, 0.45, 0.42) for x in B11_NODES_X]
    risers = VGroup(*[Line([tp[0], B11_NET_Y, 0], tp, color=PA_KRAFT, stroke_width=5) for tp in tops])
    return VGroup(trunk, drop, risers).set_z_index(-2)


def b11_clock(c, r=0.45):
    """A clock: white face, dark-kraft ring, grey hands (never ink inside an outline)."""
    face = Circle(radius=r, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=5).move_to(c)
    hands = VGroup(Line(c, c + np.array([0, r * 0.7, 0]), color=BAR1, stroke_width=6),
                   Line(c, c + np.array([r * 0.5, 0, 0]), color=BAR1, stroke_width=6))
    return VGroup(face, hands)


class B11_LoginNodeAndFilesystem(Scene):
    def construct(self):
        st, li = explorer_rack(B11_RACK)
        self.add(st, li, T("login node", 36).move_to([-5.0, -2.1, 0]))
        until(self, "do not build")
        rt = B11_RACK.p(0.65, 0.65, 0.88)
        glyph = b11_build_glyph(rt + np.array([0, 0.3, 0]))
        pa_drop(self, [glyph], 0.5, dist=4.0)
        until(self, "Everyone who is connected")
        toks = VGroup(*[pa_token(x, B11_TOK_Y, 0.75) for x in B11_TOK_X])
        self.play(LaggedStart(*[GrowFromCenter(t) for t in toks], lag_ratio=0.2), run_time=0.7)
        until(self, "a long compile")
        self.play(Rotate(glyph[0], angle=PI / 2), run_time=0.8)
        until(self, "slows the system")
        self.play(toks.animate.set_fill(BAR3).set_stroke(BAR2), run_time=0.5)
        until(self, "Heavy builds go into")
        job = job_box(B11_JOB)
        pa_drop(self, [job], 0.5, dist=4.0)
        self.add(T("job", 36).move_to([-1.3, -2.55, 0]))
        a = np.array(glyph.get_center())
        b = B11_JOB.p(0.35, 0.35, 0.56) + np.array([0, 0.3, 0])
        self.play(MoveAlongPath(glyph, ArcBetweenPoints(a, b, angle=PI / 3)), run_time=0.8)
        until(self, "or a batch job")
        self.play(toks.animate.set_fill(BAR1).set_stroke(INK), run_time=0.4)
        until(self, "Second, mind")
        home = VGroup(pa_plinth(B11_HOME, 1.2, 1.2), home_box(B11_HOME))
        pa_slide_in(self, home, LEFT * 5.5, 0.6)
        self.add(T("home", 36).move_to([1.05, 1.45, 0]))
        until(self, "is a network filesystem")
        net = b11_net()
        nodes = VGroup(*[b11_node(x) for x in B11_NODES_X])
        self.play(Create(net), run_time=0.6)
        pa_drop(self, nodes, 0.6, lag=0.25, dist=4.0)
        until(self, "shared across every node")
        self.play(FadeIn(T("every node", 36).move_to([2.7, -3.08, 0]), shift=UP * 0.2), run_time=0.3)
        until(self, "Quotas are tight")
        out, segs = pa_gauge(4.3, 1.45)
        self.play(Create(out), FadeIn(T("quota", 36).move_to([5.25, 1.45, 0])), run_time=0.4)
        pa_fill(self, segs, 0, 3, 0.5)
        until(self, "the tens of thousands")
        dots = pa_file_dots(36, 1.4, 3.9, 2.2, 3.2)
        self.play(FadeIn(T("tens of thousands", 36).move_to([2.9, 2.7, 0]), shift=DOWN * 0.2), run_time=0.3)
        pa_pour(self, dots, B11_HOME, 0, 0, 1.2, 1.2, 0.9, 1.0)
        pa_fill(self, segs, 3, 5, 0.4)
        until(self, "That is a real reason")
        clock = b11_clock(B11_CLOCK, 0.42)
        self.play(GrowFromCenter(clock), run_time=0.4)
        self.add(T("slow", 36).move_to([5.55, -3.08, 0]))
        until(self, "job launches are slow")
        self.play(Rotate(clock[1], angle=-PI / 2, about_point=B11_CLOCK), clock[0].animate.scale(1.25), run_time=0.6)
        done(self)


# ─────────────── B21 · what module load does: PATH gains a directory in front ───────────────
B21_PANEL = (-1.9, -0.35, 8.4, 3.3)                              # dark shell panel: centre x, centre y, width, height
B21_PROMPT_Y, B21_PATH_Y = 0.55, -0.5
B21_PKG = Iso(4.6, -1.6, 0.75)                                   # the admin's package box, right
B21_SLOT_X = -4.2                                                # where the package-dir pill lands (left edge) inside PATH


def b21_panel():
    return Rectangle(width=B21_PANEL[2], height=B21_PANEL[3], fill_color=DARK_L, fill_opacity=1, stroke_color=DARK_R, stroke_width=4)\
        .move_to([B21_PANEL[0], B21_PANEL[1], 0]).set_z_index(-3)


def b21_light(s, x, y, size=34):
    return pa_left(M(s, size, GHOST), x, y)


def b21_pill(s, x, y, w):
    """A kraft pill (no outline) with ink mono text, left edge at x."""
    p = RoundedRectangle(width=w, height=0.6, corner_radius=0.3, fill_color=BOX_TOP, fill_opacity=1, stroke_width=0).move_to([x + w / 2, y, 0])
    return VGroup(p, M(s, 32).move_to([x + w / 2, y, 0])).set_z_index(3)


class B21_WhatModuleLoadDoes(Scene):
    def construct(self):
        self.add(b21_panel())
        path = b21_light("PATH=/usr/bin", -5.85, B21_PATH_Y)
        self.play(FadeIn(path, shift=RIGHT * 0.3), run_time=0.4)
        until(self, "It edits your shell")
        self.play(Indicate(path, color=None, scale_factor=1.08), run_time=0.6)
        until(self, "so the shell can find")
        pkg = VGroup(pa_plinth(B21_PKG, 1.3, 1.3), B21_PKG.box(0, 0, 0, 1.3, 1.3, 0.9))
        pa_slide_in(self, pkg, LEFT * 5.0, 0.6)
        until(self, "an administrator built once")
        tok = pa_token(5.95, -1.5, 0.95)
        self.play(GrowFromCenter(tok), run_time=0.4)
        until(self, "shares with everyone")
        self.play(FadeIn(T("built once, shared", 36).move_to([4.45, -2.65, 0]), shift=UP * 0.2), run_time=0.35)
        until(self, "Load a module")
        prompt = b21_light("$ module load python/3.11", -5.85, B21_PROMPT_Y)
        self.play(FadeIn(prompt, shift=RIGHT * 0.3), run_time=0.35)
        until(self, "PATH gains")
        tail = VGroup(*path[5:])                                   # "/usr/bin" steps right to make room
        pill = b21_pill("package dir", B21_SLOT_X, B21_PATH_Y, 3.25)
        colon = b21_light(":", B21_SLOT_X + 3.3, B21_PATH_Y)
        pill.shift(UP * 2.4)
        self.add(pill)
        self.play(tail.animate.shift(RIGHT * 3.65), pill.animate.shift(DOWN * 2.4), FadeIn(colon), run_time=0.6)
        arrow = Arrow([-2.7, -1.0, 0], [3.5, -1.3, 0], color=BAR2, stroke_width=5, buff=0).set_z_index(2)
        self.play(GrowArrow(arrow), run_time=0.5)
        until(self, "Unload it")
        prompt2 = b21_light("$ module unload python/3.11", -5.85, B21_PROMPT_Y)
        self.remove(prompt); self.add(prompt2)
        self.play(pill.animate.shift(UP * 2.4), FadeOut(arrow), FadeOut(colon), run_time=0.5)
        self.remove(pill, *pill)
        self.play(tail.animate.shift(LEFT * 3.65), run_time=0.4)
        until(self, "switch between versions")
        self.remove(prompt2)
        p311 = b21_pill("3.11", B21_SLOT_X, B21_PATH_Y, 1.3)
        colon2 = b21_light(":", B21_SLOT_X + 1.4, B21_PATH_Y)
        p311.shift(UP * 2.4)
        self.add(p311)
        self.play(tail.animate.shift(RIGHT * 1.75), p311.animate.shift(DOWN * 2.4), FadeIn(colon2), run_time=0.5)
        until(self, "with no conflicts")
        p313 = b21_pill("3.13", B21_SLOT_X, B21_PATH_Y, 1.3).shift(DOWN * 2.2)
        self.add(p313)
        self.play(p311.animate.shift(UP * 2.4), p313.animate.shift(UP * 2.2), run_time=0.5)
        self.remove(p311, *p311)
        until(self, "the fastest install")
        self.play(Indicate(p313, color=None, scale_factor=1.1), run_time=0.5)
        done(self)


# ─────────────── B31 · Conda pitfalls: solve in a job, mind home, never scratch, cache only ───────────────
B31_RACK = Iso(-5.1, -0.2, 0.6)                                  # the login node, upper left
B31_JOB = Iso(-3.35, -2.3, 0.75)                                 # the job box, lower left
B31_HOME = Iso(-0.9, -1.1, 0.75)                                 # the home box, centre
B31_BIN = Iso(3.0, -1.7, 0.6)                                    # the scratch bin, right
B31_CAB = Iso(5.4, -1.0, 0.6)                                    # the project cabinet, far right
B31_GAUGE = (0.75, -0.3)


def b31_env(iso):
    return pa_env_box(iso, 0.6)


def b31_dashed(mob):
    """The vanished environment: the same box as a grey dashed outline."""
    return VGroup(*[DashedVMobject(f.copy().set_fill(opacity=0).set_stroke(BAR1, 3), num_dashes=10) for f in mob]).set_z_index(mob.z_index)


class B31_CondaPitfalls(Scene):
    def construct(self):
        st, li = explorer_rack(B31_RACK)
        self.add(st, li, T("login node", 34).move_to([-5.1, -0.7, 0]))
        until(self, "Solving an environment")
        env = b31_env(Iso(B31_RACK.ox, B31_RACK.oy, 0.6)).shift(B31_RACK.v(0.35, 0.35, 0.88))
        pa_drop(self, [env], 0.5, dist=4.0)
        until(self, "so do it in an interactive job")
        job = job_box(B31_JOB)
        pa_drop(self, [job], 0.45, dist=4.0)
        self.add(T("job", 34).move_to([-3.35, -2.65, 0]))
        a = np.array(env.get_center())
        tgt = b31_env(Iso(B31_JOB.ox, B31_JOB.oy, 0.6)).shift(B31_JOB.v(0.05, 0.05, 0.56))
        b = np.array(tgt.get_center())
        env.set_z_index(9)
        self.play(MoveAlongPath(env, ArcBetweenPoints(a, b, angle=PI / 3)), run_time=0.7)
        until(self, "not on the login node")
        self.play(Create(check(-2.55, -1.2, 0.2, TERRA, 8)), run_time=0.35)
        until(self, "Watch your home quota")
        home = VGroup(pa_plinth(B31_HOME, 1.2, 1.2), home_box(B31_HOME))
        out, segs = pa_gauge(B31_GAUGE[0], B31_GAUGE[1])
        pa_drop(self, [home], 0.5, dist=4.0, with_=(Create(out),))
        self.add(T("home", 34).move_to([-0.9, -1.7, 0]), T("quota", 34).move_to([0.75, -1.35, 0]))
        pa_fill(self, segs, 0, 2, 0.4)
        until(self, "tens of thousands of small files")
        dots = pa_file_dots(36, -1.9, 0.1, 1.9, 3.1, seed=11)
        pa_pour(self, dots, B31_HOME, 0, 0, 1.2, 1.2, 0.9, 1.0, seed=5)
        pa_fill(self, segs, 2, 5, 0.5)
        until(self, "But do not put")
        bk, fr = scratch_bin(B31_BIN)
        binp = pa_plinth(B31_BIN, 2.8, 1.8)
        pa_slide_in(self, VGroup(binp, bk, fr), LEFT * 6.0, 0.6)
        self.add(T("scratch", 34).move_to([3.1, -2.2, 0]))
        env2 = b31_env(Iso(B31_BIN.ox, B31_BIN.oy, 0.6)).shift(B31_BIN.v(1.0, 0.6, 0)).set_z_index(1)
        pa_drop(self, [env2], 0.45, dist=4.0)
        until(self, "because scratch is purged")
        line = Line(B31_BIN.p(-0.25, -0.2, 0.95), B31_BIN.p(-0.25, 2.0, 0.95), color=TERRA, stroke_width=7).set_z_index(6)
        ghost = b31_dashed(env2)
        self.play(Create(line), run_time=0.3)
        self.play(line.animate.shift(B31_BIN.v(3.25, 0, 0)), FadeOut(env2), FadeIn(ghost), run_time=0.8)
        self.play(FadeOut(line), FadeIn(T("purged", 34).move_to([3.5, 0.7, 0]), shift=UP * 0.2), run_time=0.3)
        until(self, "Keep environments")
        cab = VGroup(pa_plinth(B31_CAB, 1.3, 1.1), project_cabinet(B31_CAB))
        pa_slide_in(self, cab, LEFT * 2.5, 0.5)
        self.add(T("project", 34).move_to([5.45, -1.4, 0]))
        until(self, "home or a project directory")
        env3 = b31_env(Iso(B31_CAB.ox, B31_CAB.oy, 0.6)).shift(B31_CAB.v(0.35, 0.25, 2.0))
        pa_drop(self, [env3], 0.5, dist=3.0)
        until(self, "The one piece")
        self.play(FadeOut(ghost), run_time=0.4)
        until(self, "is the package cache")
        pk = pa_env_box(Iso(B31_BIN.ox, B31_BIN.oy, 0.6), 0.45).shift(B31_BIN.v(1.05, 0.65, 0)).set_z_index(1)
        pa_drop(self, [pk], 0.45, dist=4.0)
        self.add(M("pkgs", 32).move_to([2.2, -0.15, 0]))
        until(self, "which is regenerable")
        ck = check(3.85, -0.6, 0.2, TERRA, 8).set_z_index(8)
        self.play(Create(ck), run_time=0.35)
        until(self, "Or just empty it")
        self.play(FadeOut(pk, shift=UP * 0.3), run_time=0.4)
        done(self)
# ═════════════════════════════ PART B · B40 (Act IV) · B51, B52 (Act V) · B61 (Act VI) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB8_ / pb8_ / b40_ / b51_ / b52_ / b61_ so the parts never collide.
PB8_SMALL = "#917A55"                       # dark kraft: outlines of SMALL objects only (GATE T)
PB8_LINK = "#9C8462"                        # deep kraft: connectors (ink-edged connectors fuse objects into one blob)
PB8_BELT = "#E4E0D4"                        # belts stay within 28 of the stage (Gate V)
PB8_CW = 8.46 / 34                          # Menlo at 32: screen units per character (measured)


def pb8_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb8_left(mob, x, y):
    """Place a text by its LEFT edge, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pb8_drop(self, mobs, rt=0.5, lag=0.2, dist=4.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt, rate_func=ease_in)


def pb8_slide(self, mobs, rt=0.5, lag=0.2, dist=4.0, with_=()):
    """Slide objects in from the left, fully opaque. Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(LEFT * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(RIGHT * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt)


def pb8_xmark(x, y, s=0.3, color=BAR1, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w)).set_z_index(8)


def pb8_page(cx, cy, w=0.9, h=1.1, outline=INK, sw=3, fill=CARD):
    """A flat page: a card with ghost text lines (grey outline when it sits inside another outline, GATE T)."""
    card = RoundedRectangle(width=w, height=h, corner_radius=0.06, fill_color=fill, fill_opacity=1,
                            stroke_color=outline, stroke_width=sw).move_to([cx, cy, 0])
    lines = VGroup(*[Line([cx - w * 0.3, cy + h * f, 0], [cx + w * 0.3, cy + h * f, 0], color=GHOST, stroke_width=4)
                     for f in (0.24, 0.06, -0.12, -0.3)])
    return VGroup(card, lines)


def pb8_gear(cx, cy, r=0.42):
    """A build gear: eight teeth, a grey ring, an open hub. Small object, so dark-kraft outlines."""
    teeth = VGroup(*[Square(side_length=r * 0.38, fill_color=BAR2, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=2)
                     .move_to([cx + r * np.cos(a), cy + r * np.sin(a), 0]).rotate(a) for a in np.arange(0, 2 * PI, PI / 4)])
    ring = Circle(radius=r, fill_color=BAR2, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=3).move_to([cx, cy, 0])
    hub = Circle(radius=r * 0.32, fill_color=STAGE, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=3).move_to([cx, cy, 0])
    return VGroup(teeth, ring, hub)


def pb8_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PB8_BELT, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def pb8_weight(cx, cy, w=0.95, h=0.5):
    """A grey weight: a trapezoid block with a handle arc on top (the 'heavy' glyph, same in B40 and B52)."""
    body = Polygon([cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy - h / 2, 0], [cx + w * 0.36, cy + h / 2, 0], [cx - w * 0.36, cy + h / 2, 0],
                   fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    handle = Arc(radius=0.2, start_angle=0, angle=PI, color=INK, stroke_width=6).move_to([cx, cy + h / 2 + 0.12, 0])
    return VGroup(handle, body)


def pb8_pill(text, x, y, w, fill=GHOST, fn=T):
    """A label on a pill: grey or kraft fill, no outline, ink text (never terracotta)."""
    return VGroup(pill(x, y, w, 0.62, fill), fn(text, 32).move_to([x, y, 0]))


def pb8_dot(x, y, r=0.1):
    """A small grey node (graph glyphs): grey fill, dark-kraft outline."""
    return Circle(radius=r, fill_color=BAR1, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=2).move_to([x, y, 0])


# ─────────────── B40 · the Spack spec: package @version %compiler +variant, then the dependency tree it resolves ───────────────
B40_SPEC = (("hdf5", "package"), ("@1.14.3", "version"), ("%gcc@12.2.0", "compiler"), ("+mpi", "variant"))
B40_SPEC_Y, B40_LAB_Y = 1.45, 0.7
B40_ROOT = (0.0, -0.35)
B40_KIDS = ((-2.6, -1.5), (0.0, -1.5), (2.6, -1.5))
B40_GRAND = ((-2.6, -2.65), (2.6, -2.65))
B40_R = 0.34
B40_SRC = (-5.5, 1.3)                       # the source page, left margin
B40_VER_X = (4.3, 5.05, 5.8)                # three versions side by side, right margin
B40_VER_Y = -1.05


def b40_parts():
    """The four mono parts of the spec, laid out in a row centred on x = 0 (fixed gaps)."""
    parts = [M(s, 36) for s, _ in B40_SPEC]
    total = sum(p.width for p in parts) + 0.6 * 3
    x = -total / 2
    for p in parts:
        p.move_to([x + p.width / 2, B40_SPEC_Y, 0])
        x += p.width + 0.6
    return parts


def b40_label(k, parts):
    return T(B40_SPEC[k][1], 32).move_to([parts[k].get_center()[0], B40_LAB_Y, 0])


def b40_ring(part):
    """A grey editor's ring around one part of the spec (ink rings around text fuse into one blob, GATE T)."""
    ring = Ellipse(width=part.width + 0.4, height=0.78, color=BAR1, stroke_width=3).move_to(np.array(part.get_center()))
    ring._qc_intentional = True
    return ring


def b40_node(x, y):
    return Circle(radius=B40_R, fill_color=CARD, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=3).move_to([x, y, 0])


def b40_link(a, b):
    """Elbow connector from node a's base to node b's top, deep kraft, stopping short of both."""
    x0, y0 = a[0], a[1] - B40_R - 0.08
    x1, y1 = b[0], b[1] + B40_R + 0.08
    if abs(x0 - x1) < 0.01:
        return VGroup(Line([x0, y0, 0], [x1, y1, 0], color=PB8_LINK, stroke_width=4))
    ym = (y0 + y1) / 2
    return VGroup(Line([x0, y0, 0], [x0, ym, 0], color=PB8_LINK, stroke_width=4),
                  Line([x0, ym, 0], [x1, ym, 0], color=PB8_LINK, stroke_width=4),
                  Line([x1, ym, 0], [x1, y1, 0], color=PB8_LINK, stroke_width=4))


def b40_version_box(x):
    return Iso(x, B40_VER_Y, 0.45).box(0, 0, 0, 0.8, 0.8, 0.6, sw=3)


class B40_TheSpackSpec(Scene):
    def construct(self):
        self.play(FadeIn(pb8_title("IV · Spack")), run_time=0.3)
        # builds from source: a source page lands at the left margin
        until(self, "builds from source", lead=0.3)
        src = pb8_page(*B40_SRC)
        pb8_drop(self, [src], rt=0.45, dist=3.0, with_=[FadeIn(T("source", 32).move_to([B40_SRC[0], 2.2, 0]))])
        # many versions side by side: three small boxes at the right margin
        until(self, "many versions", lead=0.3)
        pb8_drop(self, [b40_version_box(x) for x in B40_VER_X], rt=0.55, lag=0.25, dist=3.0)
        self.play(FadeIn(T("versions", 32).move_to([5.05, -1.95, 0]), shift=UP * 0.1), run_time=0.3)
        # the honest note: a grey caveat pill, top-right; heavy: the weight glyph under it
        until(self, "One honest note", lead=0.2)
        self.play(FadeIn(pb8_pill("not the first option", 4.3, 2.95, 3.7), shift=DOWN * 0.2), run_time=0.4)
        until(self, "are heavy", lead=0.1)
        pb8_drop(self, [pb8_weight(4.3, 2.1)], rt=0.4, dist=2.0)
        # if a module or Conda covers you, use that: a check beside the words
        until(self, "If a module or Conda", lead=0.2)
        self.play(FadeIn(T("module · Conda", 32).move_to([4.75, 0.0, 0]), shift=LEFT * 0.15), run_time=0.3)
        until(self, "use that", lead=0.1)
        self.play(Create(check(3.0, 0.0, 0.18, INK, 6)), run_time=0.3)
        # the spec builds, one part at a time, each with its label
        parts = b40_parts()
        for k, cue in enumerate(("package, at version", "at version", "percent compiler", "plus variant")):
            until(self, cue, lead=0.15)
            self.play(FadeIn(parts[k], shift=UP * 0.15), FadeIn(b40_label(k, parts)), run_time=0.3)
        # each part ringed as it is named
        for k, cue in enumerate(("H D F five", "one point fourteen", "percent G C C", "plus M P I")):
            until(self, cue, lead=0.1)
            self.play(Create(b40_ring(parts[k])), run_time=0.3)
        # the dependency tree grows downward from the hdf5 node
        until(self, "resolves the whole", lead=0.3)
        nodes = [b40_node(*B40_ROOT)] + [b40_node(*k) for k in B40_KIDS] + [b40_node(*g) for g in B40_GRAND]
        links = VGroup(*[b40_link(B40_ROOT, k) for k in B40_KIDS], b40_link(B40_KIDS[0], B40_GRAND[0]), b40_link(B40_KIDS[2], B40_GRAND[1]))
        self.play(GrowFromCenter(nodes[0]), run_time=0.25)
        self.play(Create(links), LaggedStart(*[GrowFromCenter(n) for n in nodes[1:]], lag_ratio=0.2), run_time=0.8)
        # builds each piece: nodes tint kraft from the leaves up
        until(self, "builds each piece", lead=0.2)
        order = [nodes[4], nodes[5], nodes[1], nodes[2], nodes[3], nodes[0]]
        self.play(LaggedStart(*[n.animate.set_fill(BOX_L) for n in order], lag_ratio=0.25), run_time=1.2)
        until(self, "exactly those choices", lead=0.1)
        self.play(GrowFromCenter(Dot([0.75, B40_ROOT[1], 0], radius=0.09, color=TERRA)), run_time=0.25)
        done(self)


# ─────────────── B51 · three flags into a config file; EasyBuild's output is a modulefile; module use, module load ───────────────
B51_FLAGS = (("--modules-tool=EnvironmentModules", "not Lmod", "Modules tool equals", "this cluster does not run it"),
             ("--module-syntax=Tcl", "not Lua", "Module syntax equals", "will not load here"),
             ("--installpath=$HOME/easybuild", "your space", "And install path", "you cannot write"))
B51_ROW_Y = (2.55, 1.75, 0.95)
B51_X0 = -5.9
B51_CFG = (5.2, -0.35)                      # the config page
B51_GEAR = (-4.6, -0.6)
B51_PAGE_OUT = (-2.4, -0.6)                 # where the emitted modulefile page pauses
B51_DIR = Iso(0.15, -1.1, 0.6)              # the modules folder
B51_PATH_Y = -1.45
B51_CMD_Y = (-2.2, -2.95)


def b51_mono(s, y, x0=B51_X0):
    """A mono line placed by its left edge, by character count (fixed pitch; Gate A's stub over-measures long text)."""
    return M(s, 32).move_to([x0 + len(s) * PB8_CW / 2, y, 0])


def b51_flag(k):
    return b51_mono(B51_FLAGS[k][0], B51_ROW_Y[k])


def b51_reason(k):
    return pb8_left(T(B51_FLAGS[k][1], 32), B51_X0 + len(B51_FLAGS[k][0]) * PB8_CW + 0.5, B51_ROW_Y[k])


def b51_gather(k):
    """One short grey line landing on the config page: the flag, gathered."""
    cx, cy = B51_CFG
    return Line([cx - 0.27, cy + 0.26 - 0.26 * k, 0], [cx + 0.27, cy + 0.26 - 0.26 * k, 0], color=BAR1, stroke_width=5)


def b51_dirbox():
    return B51_DIR.box(0, 0, 0, 1.0, 1.0, 0.65, sw=3)


class B51_ThreeFlagsToModulefile(Scene):
    def construct(self):
        # the EasyBuild gear is the act's cast: on stage from the first frame, with its name beside it
        gear = pb8_gear(*B51_GEAR)
        self.add(gear, T("EasyBuild", 32).move_to([B51_GEAR[0], B51_PATH_Y, 0]))
        self.play(FadeIn(pb8_page(*B51_CFG, w=0.9, h=1.1)), FadeIn(M("config.cfg", 32).move_to([4.9, 0.5, 0])), run_time=0.3)
        # three flags land one by one, each followed by its reason
        for k in range(3):
            until(self, B51_FLAGS[k][2], lead=0.2)
            flag = b51_flag(k)
            self.play(FadeIn(flag, shift=RIGHT * 0.2), run_time=0.3)
            until(self, B51_FLAGS[k][3], lead=0.1)
            self.play(FadeIn(b51_reason(k), shift=LEFT * 0.1), run_time=0.3)
        # put them in a config file once: three lines land on the page
        until(self, "Put them in a config", lead=0.2)
        self.play(LaggedStart(*[Create(b51_gather(k)) for k in range(3)], lag_ratio=0.3), run_time=0.7)
        # the output is a modulefile: the gear turns and emits a page
        until(self, "EasyBuild's output", lead=0.2)
        page = pb8_page(B51_GEAR[0] + 0.3, B51_GEAR[1], w=0.75, h=0.9, outline=DIM).set_z_index(3)
        self.add(page)
        self.play(Rotate(gear, angle=PI / 2), page.animate.move_to([B51_PAGE_OUT[0], B51_PAGE_OUT[1], 0]), run_time=0.6)
        self.play(FadeIn(T("modulefile", 32).move_to([B51_PAGE_OUT[0], 0.15, 0])), run_time=0.25)
        # it slides into the modules folder, whose path is named beneath
        until(self, "Point module at its directory", lead=0.3)
        folder = b51_dirbox()
        pb8_drop(self, [folder], rt=0.4, dist=2.5)
        top = B51_DIR.p(0.5, 0.5, 0.65)
        self.play(page.animate.scale(0.75).move_to([top[0], top[1] + 0.25, 0]), run_time=0.45)
        self.play(FadeIn(M("$HOME/easybuild/modules/all", 32).move_to([0.5, B51_PATH_Y, 0])), run_time=0.25)
        # module use, module load, a check
        until(self, "module use", lead=0.15)
        self.play(FadeIn(b51_mono("module use $HOME/easybuild/modules/all", B51_CMD_Y[0]), shift=RIGHT * 0.2), run_time=0.3)
        until(self, "module load", lead=0.15)
        load = b51_mono("module load HDF5/1.14.3-gompi-2023a", B51_CMD_Y[1])
        self.play(FadeIn(load, shift=RIGHT * 0.2), run_time=0.3)
        until(self, "like any preinstalled", lead=0.1)
        self.play(Create(check(B51_X0 + len("module load HDF5/1.14.3-gompi-2023a") * PB8_CW + 0.6, B51_CMD_Y[1], 0.18, INK, 6)), run_time=0.3)
        done(self)


# ─────────────── B52 · Spack versus EasyBuild in four rows, then the weight: heavy, not the first option ───────────────
B52_ROWS = ("install", "dependencies", "output", "strength")
B52_ROW_Y = (1.85, 0.85, -0.15, -1.15)
B52_HEAD_Y = 2.7
B52_COL = (-1.6, 3.3)                       # column centres: Spack, EasyBuild
B52_GLYPH = (-3.05, 1.65)                   # glyph centres
B52_LAB = (-2.45, 2.4)                     # label left edges
B52_CELLS = (("a spec", "a recipe"), ("a graph", "a toolchain"), ("load or module", "a modulefile"), ("flexible", "strict"))
B52_CUES = (("a spec on the command line", "versus a named recipe"), ("Spack resolves a flexible", "EasyBuild follows a fixed"),
            ("spack load or a module", "versus always a module"), ("flexible variants", "versus strict"))
B52_RULE_Y = (2.3, 1.35, 0.35, -0.65, -1.65)
B52_WEIGHT = (-1.6, -2.55)


def b52_rule(y, sw=3):
    return Line([-6.0, y, 0], [6.0, y, 0], color=BAR1, stroke_width=sw)


def b52_terminal(cx, cy):
    """A spec on the command line: a tiny dark terminal chip with a ghost prompt line."""
    chip = RoundedRectangle(width=0.7, height=0.46, corner_radius=0.05, fill_color=DARK_TOP, fill_opacity=1,
                            stroke_color=INK, stroke_width=3).move_to([cx, cy, 0])
    prompt = Line([cx - 0.22, cy + 0.08, 0], [cx + 0.1, cy + 0.08, 0], color=GHOST, stroke_width=4)
    return VGroup(chip, prompt)


def b52_recipe(cx, cy):
    return pb8_page(cx, cy, w=0.5, h=0.6, outline=PB8_SMALL, sw=2)


def b52_graph(cx, cy):
    """A flexible graph: one node branching to three, deep-kraft links."""
    a = (cx - 0.35, cy)
    bs = ((cx + 0.32, cy + 0.28), (cx + 0.32, cy), (cx + 0.32, cy - 0.28))
    links = VGroup(*[Line([a[0] + 0.12, a[1], 0], [b[0] - 0.12, b[1], 0], color=PB8_LINK, stroke_width=3) for b in bs])
    return VGroup(links, pb8_dot(*a), *[pb8_dot(*b, r=0.08) for b in bs])


def b52_chain(cx, cy):
    """A fixed chain: three nodes in a straight line."""
    xs = (cx - 0.38, cx, cx + 0.38)
    links = VGroup(*[Line([xs[i] + 0.12, cy, 0], [xs[i + 1] - 0.12, cy, 0], color=PB8_LINK, stroke_width=3) for i in range(2)])
    return VGroup(links, *[pb8_dot(x, cy) for x in xs])


def b52_load_or_module(cx, cy):
    """Output: a grey pill (spack load) beside a tiny page (a module)."""
    return VGroup(pill(cx - 0.22, cy, 0.5, 0.3, GHOST), b52_recipe(cx + 0.25, cy))


def b52_flexible(cx, cy):
    """Strength: a flexible curve, grey."""
    c = VMobject(color=BAR1, stroke_width=6).set_points_smoothly(
        [[cx - 0.4, cy - 0.15, 0], [cx - 0.15, cy + 0.2, 0], [cx + 0.15, cy - 0.2, 0], [cx + 0.4, cy + 0.15, 0]])
    return VGroup(c)


def b52_strict(cx, cy):
    """Strength: a straight grey rule between two small square ends."""
    return VGroup(Line([cx - 0.3, cy, 0], [cx + 0.3, cy, 0], color=BAR1, stroke_width=6),
                  Square(side_length=0.16, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([cx - 0.38, cy, 0]),
                  Square(side_length=0.16, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([cx + 0.38, cy, 0]))


B52_GLYPHS = ((b52_terminal, b52_recipe), (b52_graph, b52_chain), (b52_load_or_module, b52_recipe), (b52_flexible, b52_strict))


def b52_cell(r, c):
    y = B52_ROW_Y[r]
    glyph = B52_GLYPHS[r][c](B52_GLYPH[c], y)
    return VGroup(glyph, pb8_left(T(B52_CELLS[r][c], 32), B52_LAB[c], y))


class B52_SpackVsEasyBuild(Scene):
    def construct(self):
        heads = VGroup(T("Spack", 36, bold=True).move_to([B52_COL[0], B52_HEAD_Y, 0]),
                       T("EasyBuild", 36, bold=True).move_to([B52_COL[1], B52_HEAD_Y, 0]))
        rules = VGroup(b52_rule(B52_RULE_Y[0], 5), *[b52_rule(y) for y in B52_RULE_Y[1:]])
        self.play(FadeIn(heads), run_time=0.3)
        self.play(Create(rules), run_time=0.45)                                             # the frame splits into four rows
        # four rows land in turn: the row label, then the Spack cell, then the EasyBuild cell
        for r in range(4):
            until(self, B52_CUES[r][0], lead=0.45)
            self.play(FadeIn(pb8_left(T(B52_ROWS[r], 32), -5.9, B52_ROW_Y[r]), shift=RIGHT * 0.15), run_time=0.25)
            self.play(FadeIn(b52_cell(r, 0), shift=UP * 0.1), run_time=0.3)
            until(self, B52_CUES[r][1], lead=0.1)
            self.play(FadeIn(b52_cell(r, 1), shift=UP * 0.1), run_time=0.3)
        # the candid note: the weight lands under the columns, 'heavy' beside it, the kraft pill
        until(self, "neither is the recommended", lead=0.3)
        pb8_drop(self, [pb8_weight(*B52_WEIGHT)], rt=0.45, dist=2.5)
        self.play(FadeIn(pb8_pill("not the first option", B52_COL[1], B52_WEIGHT[1], 3.7, fill=BOX_TOP), shift=DOWN * 0.15), run_time=0.35)
        until(self, "Both are heavy", lead=0.1)
        self.play(FadeIn(pb8_left(T("heavy", 32), B52_WEIGHT[0] + 0.75, B52_WEIGHT[1]), shift=LEFT * 0.1), run_time=0.3)
        # Spack in particular, when builds break: a grey cross by its name
        until(self, "Spack in particular", lead=0.2)
        self.play(Create(pb8_xmark(B52_COL[0] - 1.1, B52_HEAD_Y, 0.22)), run_time=0.3)
        # reach for them only when you need source-level control: one terracotta dot, the deliberate choice
        until(self, "Reach for them", lead=0.2)
        self.play(GrowFromCenter(Dot([0.85, B52_WEIGHT[1], 0], radius=0.1, color=TERRA)), run_time=0.3)
        done(self)


# ─────────────── B61 · the five-station source build: prefix, modules first, the cluster's libraries, make in a job ───────────────
B61_BELT_Y = -1.95
B61_ST_X = (-5.0, -2.5, 0.0, 2.5, 5.0)
B61_NAMES = (("load modules", T), ("configure", M), ("make", M), ("install", M), ("expose", T))
B61_NAME_CUES = ("load modules,", "configure with", "compile inside", "install into", "expose it on PATH")
B61_NUM_Y, B61_NAME_Y = -2.4, -2.95
B61_PILL_Y = (-1.45, -1.02, -0.59)
B61_JOB = Iso(-0.35, -1.9, 0.7)
B61_GEAR = (0.4, -0.5)
B61_PREFIX = Iso(2.0, -1.95, 0.6)           # the install prefix: an open folder
B61_LIB = Iso(3.85, 0.9, 0.7)               # the cluster's library block
B61_LIB_LABEL_Y = 2.5


def b61_job():
    return job_box(B61_JOB, 0, 0, 0, s=0.7)


def b61_prefix():
    return B61_PREFIX.open_box(0, 0, 0, 1.1, 1.1, 0.55)


def b61_installed():
    return Iso(B61_PREFIX.ox, B61_PREFIX.oy + 0.1, 0.6).box(0.3, 0.3, 0.02, 0.5, 0.5, 0.4, sw=3).set_z_index(1)


def b61_lib_block():
    return B61_LIB.mcp(0, 0, 0, 1.3, 1.3, 0.7)


def b61_lib_line():
    """The ghost link from the cluster's libraries to the make station, stopping short of both."""
    return Line([3.75, 0.85, 0], [0.95, -0.2, 0], color=GHOST, stroke_width=5)


def b61_link_1_2():
    """Modules loaded first: a deep-kraft link from the module pills to the configure page."""
    return Line([-4.25, -1.0, 0], [-3.0, -1.0, 0], color=PB8_LINK, stroke_width=4)


class B61_SourceBuildPipeline(Scene):
    def construct(self):
        self.add(pb8_belt(-6.0, 5.9, B61_BELT_Y))
        # always set a prefix; never the system's user local directory
        until(self, "Always set a prefix", lead=0.4)
        self.play(FadeIn(pb8_left(M("--prefix=$HOME/software/mytool", 32), -5.9, 1.65), shift=RIGHT * 0.2), run_time=0.3)
        until(self, "you cannot install", lead=0.1)
        usr = pb8_left(M("/usr/local", 32), -5.0, 2.5)
        self.play(FadeIn(usr), run_time=0.2)
        self.play(Create(pb8_xmark(-5.6, 2.5, 0.25)), run_time=0.25)
        # load the cluster's modules first: three pills slide onto station 1; then the configure page at station 2
        until(self, "Load the cluster", lead=0.2)
        pb8_slide(self, [pill(B61_ST_X[0], y, 1.3, 0.36, GHOST) for y in B61_PILL_Y], rt=0.6, lag=0.25, dist=2.0)
        until(self, "before you configure", lead=0.2)
        pb8_drop(self, [pb8_page(B61_ST_X[1], -1.1, w=0.8, h=1.0)], rt=0.4, dist=1.8)
        until(self, "so the build links", lead=0.1)
        self.play(Create(b61_link_1_2()), run_time=0.3)
        until(self, "fast binaries", lead=0.2)
        self.play(GrowFromCenter(Dot([B61_ST_X[1], -0.4, 0], radius=0.09, color=TERRA)), run_time=0.25)
        # the cluster's MPI, BLAS and LAPACK: a dark library block, linked to the make station
        until(self, "cluster's M P I", lead=0.3)
        pb8_drop(self, [b61_lib_block()], rt=0.45, dist=2.5, with_=[FadeIn(T("MPI · BLAS · LAPACK", 32).move_to([4.1, B61_LIB_LABEL_Y, 0]))])
        until(self, "not a slow", lead=0.2)
        self.play(Create(b61_lib_line()), run_time=0.35)
        # run make inside a job: the job box lands at station 3 and its gear turns
        until(self, "run the make step", lead=0.2)
        pb8_drop(self, [b61_job()], rt=0.45, dist=2.5)
        until(self, "dash j eight", lead=0.1)
        gear = pb8_gear(*B61_GEAR, r=0.38)
        self.play(GrowFromCenter(gear), run_time=0.25)
        self.play(Rotate(gear, angle=PI / 2), run_time=0.6)
        # five steps: the numerals, then each station's name as it is spoken
        until(self, "Five steps", lead=0.2)
        self.play(LaggedStart(*[FadeIn(T(str(k + 1), 32).move_to([x, B61_NUM_Y, 0]), shift=UP * 0.1) for k, x in enumerate(B61_ST_X)],
                              lag_ratio=0.15), run_time=0.5)
        for k, (cue, (name, fn)) in enumerate(zip(B61_NAME_CUES, B61_NAMES)):
            until(self, cue, lead=0.1)
            extra = []
            if k == 3:
                back, front = b61_prefix()
                self.add(back, front)
                pb8_drop(self, [b61_installed()], rt=0.35, dist=2.0, with_=[FadeIn(fn(name, 32).move_to([B61_ST_X[k], B61_NAME_Y, 0]))])
                continue
            if k == 4:
                extra = [FadeIn(VGroup(pill(B61_ST_X[4], -1.3, 1.3, 0.5, GHOST), M("PATH", 32).move_to([B61_ST_X[4], -1.3, 0])))]
            self.play(FadeIn(fn(name, 32).move_to([B61_ST_X[k], B61_NAME_Y, 0]), shift=UP * 0.1), *extra, run_time=0.3)
        until(self, "or with a module", lead=0.1)
        pb8_drop(self, [pb8_page(B61_ST_X[4], -0.4, w=0.7, h=0.85)], rt=0.35, dist=2.0)
        done(self)
# ═════════════════════════════ PART C · B63 (Act VI) · B70 (Act VII) · B80, B81 (Act VIII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PC8_ / pc8_ / b63_ / b70_ / b80_ / b81_ so the parts never collide.
PC8_LINK = "#9C8462"                        # deep kraft: connectors and arrows (ink lines fuse the things they join, GATE T)
PC8_SMALL = "#917A55"                       # dark kraft: outlines of SMALL objects only (GATE T)


def pc8_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pc8_left(mob, x, y):
    """Place a text by its LEFT edge, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pc8_right(mob, x, y):
    """Place a text by its RIGHT edge, centred on y."""
    return mob.move_to([x - mob.width / 2, y, 0])


def pc8_arrow(a, b, color=PC8_LINK, sw=4):
    """A connector arrow in deep kraft, grey tip."""
    a, b = np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0])
    return Arrow(a, b, buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.18, max_stroke_width_to_length_ratio=20)


def pc8_xmark(x, y, s=0.35, color=BAR1, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w)).set_z_index(8)


def pc8_person(x, y, s=1.0):
    """A person token standing with its feet at (x, y): grey body, ink outline (the same token as the earlier films)."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head).set_z_index(7)


def pc8_drop(self, mobs, rt=0.5, lag=0.2, dist=4.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt, rate_func=ease_in)


def pc8_page(cx, cy, w=0.8, h=0.9):
    """A flat file page: white card, grey outline, three ghost lines (a small object: grey outline, GATE T)."""
    card = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([cx, cy, 0])
    lines = VGroup(*[Line([cx - w * 0.3, cy + h * (0.25 - 0.22 * k), 0], [cx + w * 0.3, cy + h * (0.25 - 0.22 * k), 0],
                          color=GHOST, stroke_width=4) for k in range(3)])
    return VGroup(card, lines)


# ─────────────── B63 · the module tree: name and version, three commands, switch, loads others, the default ───────────────
B63_ROWS = (("$HOME/modulefiles/", -6.0, 2.5), ("mytool/", -5.0, 1.7), ("1.0", -4.0, 0.9), ("2.0", -4.0, 0.1),
            ("otherlib/", -5.0, -0.7), ("3.4", -4.0, -1.5))
B63_CMD_X, B63_CMD_Y = -0.65, (2.5, 1.75, 1.0)
B63_CMDS = ("module avail mytool", "module load mytool/1.0", "module unload mytool/1.0")
B63_CHECK_X = 5.85
B63_ANN_X = -2.85                                                        # the bracket column; its label starts 0.3 to the right
B63_CW = 8.46 / 34 * 32 / 34                                             # Menlo at 32: screen units per character (measured at 34, scaled)
B63_PAGE = (0.5, -1.45)                                                 # the mytool/2.0 file page
B63_VPAGE = (4.3, -1.45)                                                # the .version page


def b63_tree_lines():
    """Deep-kraft tree connectors: one trunk per directory, a tick to each child, stopping 0.35 clear of the text."""
    g = VGroup()
    # root trunk: under "$HOME/modulefiles/", down past otherlib/
    g.add(Line([-5.75, 2.1, 0], [-5.75, -0.7, 0], color=PC8_LINK, stroke_width=4))
    for y in (1.7, -0.7):
        g.add(Line([-5.75, y, 0], [-5.35, y, 0], color=PC8_LINK, stroke_width=4))
    # mytool/ trunk to 1.0 and 2.0
    g.add(Line([-4.75, 1.35, 0], [-4.75, 0.1, 0], color=PC8_LINK, stroke_width=4))
    for y in (0.9, 0.1):
        g.add(Line([-4.75, y, 0], [-4.35, y, 0], color=PC8_LINK, stroke_width=4))
    # otherlib/ trunk to 3.4
    g.add(Line([-4.75, -1.05, 0], [-4.75, -1.5, 0], color=PC8_LINK, stroke_width=4))
    g.add(Line([-4.75, -1.5, 0], [-4.35, -1.5, 0], color=PC8_LINK, stroke_width=4))
    return g


def b63_row(k):
    s, x, y = B63_ROWS[k]
    return pc8_left(M(s, 32), x, y)


def b63_bracket(y):
    """A grey bracket beside a tree row: a short vertical bar with two ticks (grey: never an ink line inside text)."""
    x = B63_ANN_X
    return VGroup(Line([x, y - 0.26, 0], [x, y + 0.26, 0], color=BAR1, stroke_width=4),
                  Line([x - 0.12, y - 0.26, 0], [x, y - 0.26, 0], color=BAR1, stroke_width=4),
                  Line([x - 0.12, y + 0.26, 0], [x, y + 0.26, 0], color=BAR1, stroke_width=4))


def b63_ring(k):
    """A grey ring around tree row k (an editor's ring around a label, by design)."""
    s, x, y = B63_ROWS[k]
    w = len(s) * B63_CW
    ring = Ellipse(width=w + 0.3, height=0.6, color=BAR1, stroke_width=4).move_to([x + w / 2, y, 0])
    ring._qc_intentional = True
    return ring


class B63_PersonalModuleStack(Scene):
    def construct(self):
        # the tree draws in: connectors, then every row
        lines = b63_tree_lines()
        rows = [b63_row(k) for k in range(6)]
        self.play(Create(lines), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.15), run_time=0.6)
        # directory name = module name; file name = version
        until(self, "directory name", lead=0.15)
        self.play(Create(b63_bracket(1.7)), FadeIn(pc8_left(T("name", 32), B63_ANN_X + 0.3, 1.7)), run_time=0.35)
        until(self, "file name becomes", lead=0.15)
        self.play(Create(b63_bracket(0.9)), FadeIn(pc8_left(T("version", 32), B63_ANN_X + 0.3, 0.9)), run_time=0.35)
        # the three commands land in turn, each with a check
        for cue, k in (("module avail", 0), ("module load", 1), ("unload reverses", 2)):
            until(self, cue, lead=0.15)
            self.play(FadeIn(pc8_left(M(B63_CMDS[k], 32), B63_CMD_X, B63_CMD_Y[k]), shift=RIGHT * 0.2), run_time=0.3)
            self.play(Create(check(B63_CHECK_X, B63_CMD_Y[k], 0.18)), run_time=0.25)
        # a personal stack: each tool its own subdirectory, each version a file, switch with one load
        until(self, "each tool its own", lead=0.15)
        ring = b63_ring(1)
        self.play(Create(ring), run_time=0.3)
        until(self, "each version a file", lead=0.15)
        self.play(Transform(ring, b63_ring(2)), run_time=0.4)                      # ellipse to ellipse: it travels, it does not crumple
        until(self, "switch with one load", lead=0.2)
        self.play(Transform(ring, b63_ring(3)), run_time=0.4)
        self.play(FadeIn(pc8_left(T("switch", 32), B63_ANN_X + 0.3, 0.1), shift=RIGHT * 0.1), run_time=0.25)
        # a module file can load other modules: the mytool/2.0 page with a gcc pill hanging under it
        until(self, "can load other modules", lead=0.3)
        px, py = B63_PAGE
        page = pc8_page(px, py)
        pc8_drop(self, [page], rt=0.45, dist=3.0, with_=[FadeIn(M("mytool/2.0", 32).move_to([px, -0.5, 0]))])
        until(self, "such as the right", lead=0.1)
        hang = Line([px, py - 0.5, 0], [px, -2.44, 0], color=PC8_LINK, stroke_width=4)
        gcc = VGroup(pill(px, -2.8, 1.15, 0.62, CARD), M("gcc", 32).move_to([px, -2.8, 0]))
        self.play(Create(hang), GrowFromCenter(gcc), FadeIn(pc8_left(T("loads others", 32), px + 0.8, -2.8)), run_time=0.4)
        # a .version file names the default
        until(self, "dot version file", lead=0.2)
        vx, vy = B63_VPAGE
        vpage = pc8_page(vx, vy)
        pc8_drop(self, [vpage], rt=0.45, dist=3.0, with_=[FadeIn(M(".version", 32).move_to([vx, -0.5, 0]))])
        until(self, "names the default", lead=0.1)
        self.play(Create(pc8_arrow([vx - 0.45, vy], [px + 0.5, vy])),
                  FadeIn(T("default", 32).move_to([vx, -2.8, 0]), shift=UP * 0.1), run_time=0.4)
        done(self)


# ─────────────── B70 · the .sif stacks up; Docker needs root (X); Apptainer runs as you (check); GPU and MPI; pulls docker:// ───────────────
B70_STACK = Iso(-2.6, -1.6, 0.75)
B70_SLABS = ("OS layer", "libraries", "application")
B70_LABEL_X = -3.9                                                      # right edge of the slab labels (the stack's left edge is -3.57)
B70_KEY = (2.3, -2.1)                                                   # the root key's ring centre


def b70_slab(k):
    fills = ((BOX_TOP, BOX_L, BOX_R), (BOX_TOP, BOX_L, BOX_R), (PAGE_TOP, PAGE_L, PAGE_R))
    return B70_STACK.box(0, 0, 1.0 * k, 2.0, 1.5, 0.95, *fills[k])


def b70_slab_label(k):
    """The slab's label, right-aligned left of the stack, on the slab's front-left face centre line."""
    return pc8_right(T(B70_SLABS[k], 32), B70_LABEL_X, -0.96 + 0.75 * k)


def b70_key():
    """A root key: ink-outlined kraft ring and shaft with two teeth (drawn large: tiny icons read as sub-floor text)."""
    x, y = B70_KEY
    ring = Circle(radius=0.32, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    hole = Circle(radius=0.1, fill_color=STAGE, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y, 0])
    shaft = Rectangle(width=1.0, height=0.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x + 0.8, y, 0])
    teeth = VGroup(*[Rectangle(width=0.14, height=0.22, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=3)
                     .move_to([x + 1.2 - 0.26 * k, y - 0.2, 0]) for k in range(2)])
    return VGroup(shaft, teeth, ring, hole)


class B70_ApptainerVsDocker(Scene):
    def construct(self):
        self.add(pc8_title("VII · Apptainer"))
        # the image stacks: OS layer first, then libraries and the application on top
        slabs = [b70_slab(k) for k in range(3)]
        labels = [b70_slab_label(k) for k in range(3)]
        pc8_drop(self, [slabs[0]], rt=0.5, dist=3.0, with_=[FadeIn(labels[0])])
        until(self, "packs an application", lead=0.2)
        pc8_drop(self, [slabs[1], slabs[2]], rt=0.6, lag=0.35, dist=3.0, with_=[FadeIn(labels[1]), FadeIn(labels[2])])
        until(self, "a dot S I F", lead=0.15)
        self.play(FadeIn(M(".sif", 34).move_to([-0.3, 2.1, 0]), shift=DOWN * 0.15), run_time=0.3)
        # why not Docker: the root key, crossed out
        until(self, "Why not Docker", lead=0.15)
        self.play(Create(pc8_arrow([-0.8, -0.9], [1.4, -1.9])), run_time=0.35)
        self.play(GrowFromCenter(b70_key()), FadeIn(pc8_left(M("root", 32), 3.9, -2.1)), run_time=0.35)
        until(self, "needs root to run", lead=0.1)
        self.play(Create(pc8_xmark(2.8, -2.1, 0.42)), run_time=0.3)
        until(self, "a security problem", lead=0.15)
        self.play(FadeIn(T("Docker needs root", 32).move_to([3.3, -2.95, 0]), shift=UP * 0.1), run_time=0.3)
        # Apptainer runs as you
        until(self, "runs a container as you", lead=0.2)
        self.play(Create(pc8_arrow([-0.8, 0.3], [1.4, 1.1])), run_time=0.35)
        self.play(GrowFromCenter(pc8_person(2.3, 0.75)), run_time=0.3)
        until(self, "no elevated privileges", lead=0.1)
        self.play(Create(check(3.3, 1.2, 0.2)), FadeIn(T("runs as you", 32).move_to([2.8, 2.35, 0]), shift=UP * 0.1), run_time=0.35)
        # GPU and MPI workloads: the cast GPU block, its light goes busy
        until(self, "runs G P U", lead=0.2)
        body, light = gpu_block(Iso(4.4, 0.5, 0.55))
        pc8_drop(self, [VGroup(body, light)], rt=0.4, dist=2.5, with_=[FadeIn(T("GPU · MPI", 32).move_to([4.9, -0.15, 0]))])
        until(self, "M P I workloads", lead=0.1)
        self.play(light.animate.set_color(TERRA), run_time=0.25)
        # pulls and converts Docker images
        until(self, "pull and convert", lead=0.2)
        self.play(FadeIn(M("docker://", 32).move_to([-4.9, -2.6, 0]), shift=RIGHT * 0.15), run_time=0.3)
        self.play(Create(pc8_arrow([-3.45, -2.6], [-2.75, -2.0])),
                  FadeIn(T("pulls Docker images", 32).move_to([-0.9, -2.9, 0]), shift=UP * 0.1), run_time=0.4)
        done(self)


# ─────────────── B80 · six tools, one table: root? · from source? · best for · drawback ───────────────
B80_HY, B80_ROW_Y = 2.2, (1.45, 0.7, -0.05, -0.8, -1.55, -2.3)
B80_TOOL_X, B80_PILL_X, B80_SRC_X, B80_BEST_X, B80_DRAW_X = -6.0, -3.4, -2.45, 0.05, 2.7
B80_TOOLS = ("modules", "Conda", "Spack", "EasyBuild", "source", "Apptainer")
B80_SRC = ("no", "no", "yes", "yes", "yes", "image")
B80_BEST = ("already there", "Python, R", "variants", "toolchains", "patches", "portability")
B80_DRAW = ("admins only", "quota", "heavy", "toolchain-bound", "manual", "build locally")
B80_CUES = (("Environment modules", "best for what the cluster", "limited to what admins"),
            ("Conda:", "best for Python", "heavy on quota"),
            ("Spack:", "source-level control", "heavy and slow"),
            ("EasyBuild:", "reproducible toolchain", "mostly an admin tool"),
            ("A source install", "patches and niche", "the most manual"),
            ("App-tainer:", "for hard dependencies", "built locally"))


def b80_rule(y, sw=3):
    """A grey rule between rows (table dividers never ink)."""
    return Line([-6.1, y, 0], [6.1, y, 0], color=BAR1, stroke_width=sw)


def b80_no_pill(y):
    return VGroup(pill(B80_PILL_X, y, 0.95, 0.56, GHOST), T("no", 32).move_to([B80_PILL_X, y, 0]))


class B80_SixToolsTable(Scene):
    def construct(self):
        self.add(pc8_title("VIII · Choosing The Tool"))
        head = VGroup(pc8_left(T("tool", 32, bold=True), B80_TOOL_X, B80_HY),
                      T("root?", 32, bold=True).move_to([B80_PILL_X, B80_HY, 0]),
                      pc8_left(T("from source?", 32, bold=True), B80_SRC_X, B80_HY),
                      pc8_left(T("best for", 32, bold=True), B80_BEST_X, B80_HY),
                      pc8_left(T("drawback", 32, bold=True), B80_DRAW_X, B80_HY))
        rules = VGroup(b80_rule(B80_HY - 0.4, 5), *[b80_rule(y - 0.375) for y in B80_ROW_Y[:-1]])
        self.play(FadeIn(head), run_time=0.35)
        self.play(Create(rules), run_time=0.45)
        # none needs root: six grey "no" pills at once
        until(self, "none needs root", lead=0.15)
        self.play(LaggedStart(*[GrowFromCenter(b80_no_pill(y)) for y in B80_ROW_Y], lag_ratio=0.1), run_time=0.5)
        # each row lands one cell at a time, on its words
        for k, (c_tool, c_best, c_draw) in enumerate(B80_CUES):
            y = B80_ROW_Y[k]
            until(self, c_tool, lead=0.1)
            self.play(FadeIn(pc8_left(T(B80_TOOLS[k], 32), B80_TOOL_X, y), shift=RIGHT * 0.2),
                      FadeIn(pc8_left(T(B80_SRC[k], 32), B80_SRC_X, y), shift=RIGHT * 0.2), run_time=0.3)
            until(self, c_best, lead=0.1)
            self.play(FadeIn(pc8_left(T(B80_BEST[k], 32), B80_BEST_X, y), shift=RIGHT * 0.2), run_time=0.25)
            until(self, c_draw, lead=0.1)
            self.play(FadeIn(pc8_left(T(B80_DRAW[k], 32), B80_DRAW_X, y), shift=RIGHT * 0.2), run_time=0.25)
        done(self)


# ─────────────── B81 · the practical order: five questions, yes → a tool, no ↓ the next question; then ask RC ───────────────
B81_ROW_Y = (2.45, 1.35, 0.25, -0.85, -1.95)
B81_Q_X, B81_Q_W = -3.25, 4.3                                           # question pills: -5.4 .. -1.1
B81_T_X, B81_T_W = 2.75, 3.7                                            # tool pills: 0.9 .. 4.6
B81_NUM_X = -5.85
B81_DOT = (5.05, 2.45)                                                  # the start-here dot, beside row 1's tool pill
B81_QS = ("a module?", "Python or R?", "portable or fragile?", "patch or flag?", "compiler, MPI, variants?")
B81_TOOLS = ("modules", "Conda", "Apptainer", "from source", "Spack or EasyBuild")
B81_ASK_Y = -2.85


def b81_qpill(k):
    y = B81_ROW_Y[k]
    return VGroup(pill(B81_Q_X, y, B81_Q_W, 0.62, CARD), T(B81_QS[k], 32).move_to([B81_Q_X, y, 0]))


def b81_tpill(k):
    y = B81_ROW_Y[k]
    return VGroup(pill(B81_T_X, y, B81_T_W, 0.62, GHOST if k == 4 else CARD), T(B81_TOOLS[k], 32).move_to([B81_T_X, y, 0]))


def b81_yes(k):
    y = B81_ROW_Y[k]
    return pc8_arrow([B81_Q_X + B81_Q_W / 2 + 0.15, y], [B81_T_X - B81_T_W / 2 - 0.1, y])


def b81_no(k):
    """The 'no' arrow from question k down to question k+1 (or to the ask pill)."""
    y0 = B81_ROW_Y[k] - 0.31 - 0.05
    y1 = (B81_ROW_Y[k + 1] if k < 4 else B81_ASK_Y) + 0.31 + 0.05
    return pc8_arrow([B81_Q_X, y0], [B81_Q_X, y1])


def b81_weight():
    """A kettlebell beside the grey pill: willing to maintain it (ink outline, drawn large)."""
    x, y = 5.5, B81_ROW_Y[4]
    ball = Circle(radius=0.3, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y - 0.12, 0])
    handle = Arc(radius=0.22, start_angle=0, angle=PI, arc_center=np.array([x, y + 0.1, 0.0]), color=INK, stroke_width=6)
    return VGroup(handle, ball)


class B81_DecisionOrder(Scene):
    def construct(self):
        heads = VGroup(T("no", 32).move_to([B81_Q_X, 3.0, 0]), T("yes", 32).move_to([(B81_Q_X + B81_Q_W / 2 + B81_T_X - B81_T_W / 2) / 2, 3.0, 0]))
        self.play(FadeIn(heads), run_time=0.3)
        cues = (("One: check for a module", "the best install is no install"),
                ("Two: a Python", "Conda, with the quota"),
                ("Three: isolated", "Build a container"),
                ("Four: a patch", "Build from source"),
                ("Five: source-level", "Then, and mostly then"))
        for k, (c_q, c_t) in enumerate(cues):
            until(self, c_q, lead=0.15)
            anims = [GrowFromCenter(b81_qpill(k)), FadeIn(T(str(k + 1), 36).move_to([B81_NUM_X, B81_ROW_Y[k], 0]))]
            if k > 0:
                anims.append(Create(b81_no(k - 1)))
            self.play(*anims, run_time=0.35)
            if k == 0:
                self.play(GrowFromCenter(Dot([*B81_DOT, 0], radius=0.09, color=TERRA)), run_time=0.2)   # start here
            until(self, c_t, lead=0.15)
            tool = [Create(b81_yes(k)), GrowFromCenter(b81_tpill(k))]
            if k == 4:
                tool.append(GrowFromCenter(b81_weight()))
            self.play(*tool, run_time=0.4)
        # none of that fits: ask Research Computing
        until(self, "ask the Research Computing", lead=0.3)
        ask = VGroup(pill(B81_Q_X, B81_ASK_Y, B81_Q_W, 0.62, GHOST), T("ask Research Computing", 32).move_to([B81_Q_X, B81_ASK_Y, 0]))
        self.play(Create(b81_no(4)), GrowFromCenter(ask), run_time=0.4)
        done(self)


# attach the midpoint guard (see ST)
for _cls in (B10_LaptopVsCluster, B11_LoginNodeAndFilesystem, B21_WhatModuleLoadDoes, B31_CondaPitfalls, B40_TheSpackSpec, B51_ThreeFlagsToModulefile, B52_SpackVsEasyBuild, B61_SourceBuildPipeline, B63_PersonalModuleStack, B70_ApptainerVsDocker, B80_SixToolsTable, B81_DecisionOrder):
    _cls.play = ST.play
