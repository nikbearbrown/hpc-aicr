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
# ═════════════════════════════ PART A · Act I (B10) · Act II (B20, B21) · Act III (B30, B32) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PA_ / pa_ / b1x_ / b2x_ / b3x_ so the parts never collide.
PA_KRAFT = "#9C8462"                        # deep kraft: connectors and timelines (ink lines fuse the things they join, GATE T)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T)
PA_BELT = "#E4E0D4"                         # belts stay within 28 of the stage (Gate V)


def pa_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_left(mob, x, y):
    """Place a text by its LEFT edge, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pa_right(mob, x, y):
    """Place a text by its RIGHT edge, centred on y."""
    return mob.move_to([x - mob.width / 2, y, 0])


def pa_token(x, y, s=1.0):
    """A person token standing with its feet at (x, y) (same token as the earlier films)."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head).set_z_index(7)


def pa_xmark(x, y, s=0.35, color=BAR1, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w)).set_z_index(8)


def pa_drop(self, mobs, rt=0.55, lag=0.2, dist=5.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt, rate_func=ease_in)


def pa_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PA_BELT, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def pa_calendar(cx, cy, w=1.3, h=1.1):
    """A calendar page: white card, grey outline, ghost day squares, one terracotta day."""
    card = RoundedRectangle(width=w, height=h, corner_radius=0.08, fill_color=CARD, fill_opacity=1,
                            stroke_color=BAR1, stroke_width=4).move_to([cx, cy, 0])
    sq, step = 0.1 * w / 1.3, 0.165 * w / 1.3
    x0, y0 = cx - 3 * step, cy + 0.3 * h / 1.1
    days = VGroup(*[Square(side_length=sq, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([x0 + c * step, y0 - r * step * 1.3, 0])
                    for r in range(4) for c in range(7)])
    mark = Dot([x0 + 2 * step, y0, 0], radius=sq * 0.75, color=TERRA)
    return VGroup(card, days, mark).set_z_index(6)


def pa_gear(cx, cy, r=0.42):
    """A method gear: eight teeth, a grey ring, an open hub. Small object, so dark-kraft outlines."""
    teeth = VGroup(*[Square(side_length=r * 0.38, fill_color=BAR2, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=2)
                     .move_to([cx + r * np.cos(a), cy + r * np.sin(a), 0]).rotate(a) for a in np.arange(0, 2 * PI, PI / 4)])
    ring = Circle(radius=r, fill_color=BAR2, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([cx, cy, 0])
    hub = Circle(radius=r * 0.32, fill_color=STAGE, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([cx, cy, 0])
    return VGroup(teeth, ring, hub)


def pa_page(cx, cy, w=0.9, h=1.1, plot=False, outline=INK, sw=3):
    """A flat 2-D page: a white card with ghost text lines, or a grey result curve (grey inside an ink outline, GATE T)."""
    card = RoundedRectangle(width=w, height=h, corner_radius=0.06, fill_color=CARD, fill_opacity=1,
                            stroke_color=outline, stroke_width=sw).move_to([cx, cy, 0])
    if plot:
        pts = [(0.2, 0.25), (0.4, 0.45), (0.55, 0.38), (0.8, 0.75)]
        inner = VMobject(color=BAR1, stroke_width=4).set_points_as_corners(
            [[cx - w / 2 + w * fx, cy - h / 2 + h * fy, 0] for fx, fy in pts])
        base = Line([cx - w * 0.32, cy - h * 0.3, 0], [cx + w * 0.32, cy - h * 0.3, 0], color=GHOST, stroke_width=4)
        return VGroup(card, base, inner)
    lines = VGroup(*[Line([cx - w * 0.32, cy + h * f, 0], [cx + w * 0.32, cy + h * f, 0], color=GHOST, stroke_width=4)
                     for f in (0.25, 0.08, -0.09, -0.26)])
    return VGroup(card, lines)


def pa_databox(iso, white=False):
    """A data box: closed kraft (the same data) or white (new data)."""
    if white:
        return iso.box(0, 0, 0, 1.0, 1.0, 0.7, PAGE_TOP, PAGE_L, PAGE_R)
    return iso.box(0, 0, 0, 1.0, 1.0, 0.7)


def pa_light_blocks(xs, oy=0.7, s=0.6):
    """Small dark machine blocks with ghost lights (the lights turn terracotta when busy). Returns (blocks, lights)."""
    blocks, lights = VGroup(), VGroup()
    for x in xs:
        body, light = gpu_block(Iso(x, oy, s))
        blocks.add(body)
        lights.add(light)
    return blocks, lights


# ─────────────── B10 · three words: three pipelines, the differences named ───────────────
B10_CX = (-4.3, -0.1, 3.95)                 # column centres
B10_OBJ = -1.0                              # objects sit at cx + B10_OBJ, labels start at cx + B10_LAB
B10_LAB = -0.35
B10_WORDS = ("reproducibility", "replicability", "repeatability")
B10_DOT_X = (-2.25, 5.75)                   # the terracotta dots after the first and third words (fixed: Gate A's stub over-measures text)


def b10_pipeline(k, white=False):
    """data box → gear → result page, stacked vertically, joined by deep-kraft connectors."""
    x = B10_CX[k] + B10_OBJ
    box = pa_databox(Iso(x, 1.0, 0.5), white=white)
    gear = pa_gear(x, 0.0)
    page = pa_page(x, -1.35, 0.9, 1.0, plot=True)
    c1 = Line([x, 0.92, 0], [x, 0.58, 0], color=PA_KRAFT, stroke_width=5)
    c2 = Line([x, -0.58, 0], [x, -0.8, 0], color=PA_KRAFT, stroke_width=5)
    return box, gear, page, c1, c2


def b10_label(s, k, y):
    return pa_left(T(s, 32), B10_CX[k] + B10_LAB, y)


def b10_word(k):
    return T(B10_WORDS[k], 40).move_to([B10_CX[k], 2.35, 0])


class B10_ThreeWords(Scene):
    def construct(self):
        self.add(pa_title("I · Three Words"))
        words = [b10_word(k) for k in range(3)]
        # 1 · reproducibility: same data, same method, another person
        until(self, "Reproducibility:", lead=0.3)
        box, gear, page, c1, c2 = b10_pipeline(0)
        pa_drop(self, [box, gear, page], rt=0.6, lag=0.25, dist=4.0, with_=[FadeIn(words[0])])
        self.play(Create(c1), Create(c2), run_time=0.3)
        until(self, "your same data", lead=0.2)
        self.play(FadeIn(b10_label("same data", 0, 1.45), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "your same methods", lead=0.2)
        self.play(FadeIn(b10_label("same method", 0, 0.0), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "gets your result", lead=0.2)
        pa_drop(self, [pa_token(B10_CX[0] + B10_OBJ, -3.1, 0.85)], rt=0.4, dist=3.0,
                with_=[FadeIn(b10_label("other person", 0, -2.75), shift=RIGHT * 0.15)])
        # 2 · replicability: new data (white), similar method, another team
        until(self, "Replicability:", lead=0.3)
        box, gear, page, c1, c2 = b10_pipeline(1, white=True)
        pa_drop(self, [box, gear, page], rt=0.6, lag=0.25, dist=4.0, with_=[FadeIn(words[1])])
        self.play(Create(c1), Create(c2), run_time=0.3)
        until(self, "collects new data", lead=0.2)
        self.play(FadeIn(b10_label("new data", 1, 1.45), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "uses similar methods", lead=0.2)
        self.play(FadeIn(b10_label("similar method", 1, 0.0), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "finds a comparable result", lead=0.2)
        team = [pa_token(B10_CX[1] + B10_OBJ + dx, -3.1, 0.85) for dx in (-0.6, 0.0, 0.6)]
        pa_drop(self, team, rt=0.5, lag=0.2, dist=3.0, with_=[FadeIn(b10_label("other team", 1, -2.75).shift(RIGHT * 0.45), shift=RIGHT * 0.15)])
        # 3 · repeatability: same data, same method, the same person six months later
        until(self, "Repeatability:", lead=0.3)
        box, gear, page, c1, c2 = b10_pipeline(2)
        pa_drop(self, [box, gear, page], rt=0.6, lag=0.25, dist=4.0, with_=[FadeIn(words[2])])
        self.play(Create(c1), Create(c2), run_time=0.3)
        until(self, "re-run the same methods", lead=0.2)
        self.play(FadeIn(b10_label("same method", 2, 0.0), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "on the same data", lead=0.2)
        self.play(FadeIn(b10_label("same data", 2, 1.45), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "six months later", lead=0.3)
        pa_drop(self, [pa_token(B10_CX[2] - 1.45, -3.1, 0.85)], rt=0.4, dist=3.0)
        cal = pa_calendar(B10_CX[2] - 0.55, -2.7, 0.95, 0.82)
        self.play(GrowFromCenter(cal), FadeIn(pa_left(T("+6 months", 32), B10_CX[2] + 0.15, -2.7), shift=RIGHT * 0.15), run_time=0.4)
        # today: the first and the third
        until(self, "Today is mostly", lead=0.1)
        dots = [Dot([x, 2.35, 0], radius=0.13, color=TERRA) for x in B10_DOT_X]
        self.play(*[GrowFromCenter(d) for d in dots], run_time=0.4)
        done(self)


# ─────────────── B20 · the crisis in numbers: the Nature survey (approx.) and three studies ───────────────
B20_LAB_R = -4.5                            # right edge of the field labels (left panel)
B20_BAR_X0 = -4.3                           # bars start here; 100 % = B20_BAR_W
B20_BAR_W = 3.3
B20_ROWS = (("chemistry", 87, 1.75), ("biology", 77, 1.05), ("physics", 69, 0.35), ("medicine", 67, -0.35), ("earth", 64, -1.05))
B20_RX0, B20_RX1 = 0.25, 6.05               # right panel span
B20_STATS = (("psychology", "36–47 of 100", (0.36, 0.47), "Open Science Collaboration, 2015", 2.1),
             ("cancer", "11% of 53", (0.11, None), "Begley & Ellis, 2012", 0.35),
             ("economics", "49%", (0.49, None), "Chang & Li, 2015", -1.4))


def b20_bar(pct, y, h=0.44):
    w = B20_BAR_W * pct / 100
    return Rectangle(width=w, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B20_BAR_X0 + w / 2, y, 0])


def b20_num(pct, y):
    return pa_left(T(f"{pct}%", 32), B20_BAR_X0 + B20_BAR_W * pct / 100 + 0.2, y)


def b20_track(y, h=0.4):
    return Rectangle(width=B20_RX1 - B20_RX0, height=h, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([(B20_RX0 + B20_RX1) / 2, y, 0])


def b20_fill(frac, y, x0=None, fill=BAR1, h=0.4):
    x0 = B20_RX0 if x0 is None else x0
    x1 = B20_RX0 + (B20_RX1 - B20_RX0) * frac
    return Rectangle(width=x1 - x0, height=h, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([(x0 + x1) / 2, y, 0])


def b20_stat(k):
    """(label, hero numeral, track, fills, citation) for stat row k; rows are label / bar / citation."""
    name, hero, (f0, f1), cite, yt = B20_STATS[k]
    yb = yt - 0.55
    track = b20_track(yb)
    fills = [b20_fill(f0, yb)]
    if f1:
        fills.append(b20_fill(f1, yb, x0=B20_RX0 + (B20_RX1 - B20_RX0) * f0 + 0.06, fill=BAR2))
    # the citation hangs under its track by next_to (no explicit coordinate: Gate A's stub over-measures long text)
    return (pa_left(T(name, 34), B20_RX0, yt), pa_right(T(hero, 36), B20_RX1, yt), track, fills,
            T(cite, 32).next_to(track, DOWN, buff=0.14, aligned_edge=LEFT))


class B20_TheCrisis(Scene):
    def construct(self):
        self.add(pa_title("II · Why It Matters"))
        # the survey panel: field labels, a grey axis, the 'approx.' tag and the 'failed to reproduce' header
        until(self, "In 2016 a Nature survey", lead=0.3)
        labels = VGroup(*[pa_right(T(name, 32), B20_LAB_R, y) for name, _, y in B20_ROWS])
        axis = Line([B20_BAR_X0 - 0.05, 2.05, 0], [B20_BAR_X0 - 0.05, -1.4, 0], color=BAR2, stroke_width=4)
        head = pa_left(T("failed to reproduce", 32), -6.1, 2.45)
        approx = pa_left(T("approx.", 32), -2.0, 2.45)
        self.play(FadeIn(labels, shift=RIGHT * 0.15), Create(axis), FadeIn(head), FadeIn(approx), run_time=0.5)
        until(self, "in chemistry", lead=0.2)
        self.play(GrowFromEdge(b20_bar(87, 1.75), LEFT), FadeIn(b20_num(87, 1.75)),
                  FadeIn(pa_left(T("Nature survey, 2016", 32), -6.1, -1.95), shift=UP * 0.15), run_time=0.5)
        until(self, "in biology", lead=0.2)
        self.play(GrowFromEdge(b20_bar(77, 1.05), LEFT), FadeIn(b20_num(77, 1.05)), run_time=0.45)
        until(self, "in physics", lead=0.2)
        self.play(GrowFromEdge(b20_bar(69, 0.35), LEFT), FadeIn(b20_num(69, 0.35)), run_time=0.4)
        until(self, "medicine and earth science", lead=0.2)
        self.play(GrowFromEdge(b20_bar(67, -0.35), LEFT), FadeIn(b20_num(67, -0.35)),
                  GrowFromEdge(b20_bar(64, -1.05), LEFT), FadeIn(b20_num(64, -1.05)), run_time=0.45)
        # three studies: the rows land as they are named
        until(self, "Other studies", lead=0.2)
        rows = [b20_stat(k) for k in range(3)]
        self.play(*[FadeIn(r[2]) for r in rows], run_time=0.4)
        for k, cue in enumerate(("In psychology", "In biomedicine", "In economics")):
            until(self, cue, lead=0.2)
            name, hero, track, fills, cite = rows[k]
            self.play(FadeIn(name, shift=RIGHT * 0.15), *[GrowFromEdge(f, LEFT) for f in fills], run_time=0.5)
            self.play(FadeIn(hero, shift=LEFT * 0.15), FadeIn(cite, shift=UP * 0.1), run_time=0.4)
        done(self)


# ─────────────── B21 · it bites you first: six months later, redo the plot; then the five culprits ───────────────
B21_DESK = Iso(-3.3, 0.35, 0.75)
B21_TOKEN_X = -5.1
B21_CAL = (-0.7, 1.9)
B21_BLOCKS = (2.3, 3.5, 4.7)
B21_CARD_X = (-4.9, -2.45, 0.0, 2.45, 4.9)
B21_CARD_Y = -1.5
B21_LABELS = ("no methods", "not shared", "no versions", "one machine", "absolute paths")
B21_CUES = ("methods not documented", "data and code not shared", "software versions not recorded", "depend on one machine",
            "absolute file paths")


def b21_desk():
    return B21_DESK.box(0, 0, 0, 2.2, 1.3, 0.55)


def b21_plot_page():
    """The plot page lying on the desk top: white slab, ghost base line, grey result curve."""
    iso, z = B21_DESK, 0.55
    slab = iso.box(0.25, 0.15, z, 0.85, 1.0, 0.05, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
    zt = z + 0.05
    base = Line(iso.p(0.4, 0.3, zt), iso.p(0.4, 1.0, zt), color=GHOST, stroke_width=4)
    curve = VMobject(color=GHOST, stroke_width=5).set_points_as_corners(
        [iso.p(0.45, 0.3, zt), iso.p(0.7, 0.5, zt), iso.p(0.6, 0.7, zt), iso.p(0.95, 1.0, zt)])
    return VGroup(slab, base, curve).set_z_index(3)


def b21_model_page():
    iso, z = B21_DESK, 0.55
    slab = iso.box(1.4, 0.2, z, 0.75, 0.9, 0.05, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
    zt = z + 0.05
    lines = VGroup(*[Line(iso.p(1.55, 0.2 + 0.9 * f, zt), iso.p(2.0, 0.2 + 0.9 * f, zt), color=GHOST, stroke_width=4) for f in (0.3, 0.5, 0.7)])
    return VGroup(slab, lines).set_z_index(3)


def b21_ring():
    # a terracotta dot beside the page (a ring over the page merged with the plot curve under GATE T §8.6b)
    c = B21_DESK.p(0.68, 1.35, 0.6)
    return Dot(c, radius=0.14, color=TERRA).set_z_index(5)


def b21_card(k):
    return RoundedRectangle(width=2.2, height=1.5, corner_radius=0.1, fill_color=CARD, fill_opacity=1,
                            stroke_color=INK, stroke_width=3).move_to([B21_CARD_X[k], B21_CARD_Y, 0])


def b21_glyph(k):
    """The barrier glyph inside card k. Grey / dark-kraft outlines only: these sit inside an ink outline."""
    cx, cy = B21_CARD_X[k], B21_CARD_Y
    if k == 0:      # no methods: a page with the method lines missing
        page = RoundedRectangle(width=0.8, height=1.0, corner_radius=0.05, fill_color=CARD, fill_opacity=1,
                                stroke_color=BAR1, stroke_width=3).move_to([cx, cy, 0])
        line = Line([cx - 0.25, cy + 0.3, 0], [cx + 0.25, cy + 0.3, 0], color=BAR1, stroke_width=4)
        ghosts = VGroup(*[DashedLine([cx - 0.25, cy + f, 0], [cx + 0.25, cy + f, 0], color=GHOST, stroke_width=4, dash_length=0.08)
                          for f in (0.08, -0.14, -0.36)])
        return VGroup(page, line, ghosts)
    if k == 1:      # not shared: a closed kraft box, outlined in dark kraft
        iso = Iso(cx, cy - 0.55, 0.5)
        return VGroup(*[Polygon(*pts, fill_color=f, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3) for pts, f in (
            ([iso.p(0, 0, 0), iso.p(0, 1, 0), iso.p(0, 1, 0.8), iso.p(0, 0, 0.8)], BOX_L),
            ([iso.p(0, 0, 0), iso.p(1, 0, 0), iso.p(1, 0, 0.8), iso.p(0, 0, 0.8)], BOX_R),
            ([iso.p(0, 0, 0.8), iso.p(1, 0, 0.8), iso.p(1, 1, 0.8), iso.p(0, 1, 0.8)], BOX_TOP))])
    if k == 2:      # no versions: one page, the earlier versions only ghosts
        return VGroup(*[RoundedRectangle(width=0.7, height=0.9, corner_radius=0.05, fill_color=CARD, fill_opacity=1,
                                         stroke_color=col, stroke_width=3).move_to([cx + d, cy - d, 0])
                        for d, col in ((0.22, GHOST), (0.11, BAR2), (0.0, BAR1))])
    if k == 3:      # one machine: a laptop
        screen = RoundedRectangle(width=1.0, height=0.65, corner_radius=0.04, fill_color=GHOST, fill_opacity=1,
                                  stroke_color=BAR1, stroke_width=3).move_to([cx, cy + 0.12, 0])
        base = Polygon([cx - 0.65, cy - 0.3, 0], [cx + 0.65, cy - 0.3, 0], [cx + 0.55, cy - 0.2, 0], [cx - 0.55, cy - 0.2, 0],
                       fill_color=BAR2, fill_opacity=1, stroke_color=BAR1, stroke_width=3)
        return VGroup(screen, base)
    # absolute paths: a folder chain stepping down from the root, joined in deep kraft
    folders, links = VGroup(), VGroup()
    for i in range(3):
        fx, fy = cx - 0.55 + i * 0.5, cy + 0.4 - i * 0.4
        folders.add(Rectangle(width=0.5, height=0.32, fill_color=BOX_TOP, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([fx, fy, 0]))
        if i:
            links.add(Line([fx - 0.5, fy + 0.22, 0], [fx - 0.5, fy, 0], color=PA_KRAFT, stroke_width=3),
                      Line([fx - 0.5, fy, 0], [fx - 0.25, fy, 0], color=PA_KRAFT, stroke_width=3))
    return VGroup(links, folders)


class B21_FiveBarriers(Scene):
    def construct(self):
        desk, token = b21_desk(), pa_token(B21_TOKEN_X, 0.35)
        self.add(desk, token)
        # the real world: the plot behind a clinical decision, the model behind a policy
        until(self, "clinical decisions", lead=0.3)
        plot = b21_plot_page()
        pa_drop(self, [plot], rt=0.45, dist=2.5)
        until(self, "policy built on models", lead=0.3)
        model = b21_model_page()
        pa_drop(self, [model], rt=0.45, dist=2.5)
        # it bites you first: six months later the plot is asked for again
        until(self, "it bites you first", lead=0.2)
        self.play(token.animate.shift(UP * 0.3), run_time=0.4, rate_func=there_and_back)
        until(self, "something has to be redone", lead=0.3)
        cal = pa_calendar(*B21_CAL)
        self.play(GrowFromCenter(cal), run_time=0.4)
        leaf = cal[0].copy().set_z_index(7)
        self.play(leaf.animate.shift(UP * 0.9).set_opacity(0), FadeIn(pa_left(T("+6 months", 32), 0.2, 1.9), shift=UP * 0.15), run_time=0.5)
        self.remove(leaf)
        until(self, "a plot", lead=0.1)
        self.play(GrowFromCenter(b21_ring()), run_time=0.4)
        # the faster that is: the pipeline re-runs in minutes
        until(self, "the faster that is", lead=0.3)
        blocks, lights = pa_light_blocks(B21_BLOCKS)
        pa_drop(self, list(blocks), rt=0.5, lag=0.2, dist=3.0)
        self.add(lights)
        rt = guard(self, 0.6)
        self.play(LaggedStart(*[l.animate.set_color(TERRA) for l in lights], lag_ratio=0.4), run_time=rt)
        until(self, "the faster you publish", lead=0.2)
        self.play(FadeIn(T("redo in minutes", 32).move_to([3.5, 2.3, 0]), shift=UP * 0.15), run_time=0.4)
        # the five culprits
        until(self, "The usual culprits are five", lead=0.1)
        cards = [VGroup(b21_card(k), b21_glyph(k)) for k in range(5)]
        pa_drop(self, cards, rt=0.7, lag=0.15, dist=5.0)
        self.play(*[FadeIn(T(s, 32).move_to([x, -2.75, 0])) for s, x in zip(B21_LABELS, B21_CARD_X)], run_time=0.35)
        for k, cue in enumerate(B21_CUES):
            until(self, cue, lead=0.1)
            self.play(Create(pa_xmark(B21_CARD_X[k], B21_CARD_Y, 0.55, BAR1, 10)), run_time=0.3)
        done(self)


# ─────────────── B30 · the checklist in three phases, ticking as named, a belt running under ───────────────
B30_COL_X = (-5.95, -1.95, 2.15)            # left edge of each column
B30_HEADS = ("setup", "during", "completion")
B30_ROW_Y = (1.55, 0.95, 0.35, -0.25, -0.85)
B30_BELT_Y = -2.6
B30_BOX_X = (-4.3, -0.3, 3.8)               # where the box rests under each column
B30_ITEMS = ((("Git repository", T, "a Git repository"), ("folder layout", T, "a consistent folder layout"),
              ("environment", T, "a documented environment"), ("README", M, "a README")),
             (("commented code", T, "commented code"), ("relative paths", T, "relative paths"), ("random seeds", T, "random seeds set"),
              ("transformations", T, "every data transformation"), ("regular commits", T, "regular commits")),
             (("someone else runs", T, "have someone else run it"), ("environment file", T, "ship the environment file"),
              ("instructions", T, "and the instructions"), ("data and code", T, "share the data and the code"),
              ("limitations", T, "write down the limitations")))


def b30_box(x, y):
    return Square(side_length=0.4, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x + 0.2, y, 0])


def b30_tick(x, y):
    return check(x + 0.2, y - 0.02, 0.17, INK, 6)


def b30_crate(x):
    return Iso(x, B30_BELT_Y + 0.15, 0.55).box(0, 0, 0, 0.9, 0.9, 0.6).set_z_index(2)


class B30_ThreePhaseChecklist(Scene):
    def construct(self):
        self.add(pa_title("III · The Checklist"))
        heads = VGroup(*[pa_left(T(h, 36, bold=True), x, 2.3) for h, x in zip(B30_HEADS, B30_COL_X)])
        rows = VGroup()
        for col, items in enumerate(B30_ITEMS):
            for (s, f, _), y in zip(items, B30_ROW_Y):
                bx = b30_box(B30_COL_X[col], y)
                rows.add(bx, f(s, 32).next_to(bx, RIGHT, buff=0.3))
        belt = pa_belt(-6.0, 5.7, B30_BELT_Y)
        self.add(heads, rows, belt)
        crate = b30_crate(B30_BOX_X[0])
        until(self, "At setup", lead=0.3)
        pa_drop(self, [crate], rt=0.45, dist=3.0)
        for col, (items, move_cue) in enumerate(zip(B30_ITEMS, (None, "During the work", "At the end"))):
            if move_cue:
                until(self, move_cue, lead=0.3)
                self.play(crate.animate.shift(RIGHT * (B30_BOX_X[col] - B30_BOX_X[col - 1])), run_time=0.6)
            for (s, f, cue), y in zip(items, B30_ROW_Y):
                until(self, cue, lead=0.1)
                self.play(Create(b30_tick(B30_COL_X[col], y)), run_time=0.3)
        top = Iso(B30_BOX_X[2], B30_BELT_Y + 0.15, 0.55).p(0.45, 0.45, 0.6)
        self.play(GrowFromCenter(Dot(top, radius=0.1, color=TERRA).set_z_index(3)), run_time=0.3)
        done(self)


# ─────────────── B32 · version control in one breath: commits, revert, collaborate, history, a branch ───────────────
B32_Y = -0.5                                # the main line
B32_X = (-4.4, -2.95, -1.5, -0.05, 1.4, 4.3)  # commit dots; the last is the merge commit
B32_BRANCH = (2.85, 0.7)                    # the experiment commit, off the line
B32_PAGE = (-4.6, 1.5)
B32_TOKENS = (-0.05, 1.4)


def b32_dot(k):
    return Dot([B32_X[k], B32_Y, 0], radius=0.15, color=INK).set_z_index(4)


def b32_line():
    return Line([-5.2, B32_Y, 0], [5.1, B32_Y, 0], color=PA_KRAFT, stroke_width=6)


def b32_page_line(k):
    """The k-th grey text line on the file page (one per commit)."""
    cx, cy = B32_PAGE
    return Line([cx - 0.4, cy + 0.5 - k * 0.28, 0], [cx + 0.4, cy + 0.5 - k * 0.28, 0], color=BAR1, stroke_width=4)


def b32_revert():
    a, b = np.array([B32_X[2], B32_Y + 0.22, 0]), np.array([B32_X[0], B32_Y + 0.22, 0])
    return CurvedArrow(a, b, angle=PI / 2.2, color=PA_KRAFT, stroke_width=5, tip_length=0.22)


def b32_branch():
    x5, (xb, yb), x6 = B32_X[4], B32_BRANCH, B32_X[5]
    up = Line([x5 + 0.12, B32_Y + 0.12, 0], [xb - 0.15, yb - 0.1, 0], color=PA_KRAFT, stroke_width=5)
    down = Line([xb + 0.15, yb - 0.1, 0], [x6 - 0.12, B32_Y + 0.12, 0], color=PA_KRAFT, stroke_width=5)
    return up, down, Dot([xb, yb, 0], radius=0.15, color=TERRA).set_z_index(4)


def b32_bracket():
    y = B32_Y - 0.7
    return VGroup(Line([B32_X[0], y, 0], [B32_X[5], y, 0], color=BAR1, stroke_width=4),
                  Line([B32_X[0], y, 0], [B32_X[0], y + 0.18, 0], color=BAR1, stroke_width=4),
                  Line([B32_X[5], y, 0], [B32_X[5], y + 0.18, 0], color=BAR1, stroke_width=4))


class B32_VersionControl(Scene):
    def construct(self):
        page = pa_page(*B32_PAGE, 1.3, 1.6)
        self.add(b32_line(), page[0])
        # every change is recorded: three commits, the page gains a line each time
        until(self, "every change is recorded", lead=0.3)
        plines = [b32_page_line(k) for k in range(3)]
        for k in range(3):
            self.play(GrowFromCenter(b32_dot(k)), Create(plines[k]), run_time=0.3)
        # revert: back two dots, the page restores
        until(self, "revert to any earlier version", lead=0.3)
        self.play(Create(b32_revert()), FadeIn(T("revert", 32).move_to([-2.95, 1.1, 0]), shift=DOWN * 0.1), run_time=0.5)
        self.play(FadeOut(VGroup(*plines[1:])), run_time=0.3)
        # collaborate: two people commit to the same line
        until(self, "collaborate without overwriting", lead=0.3)
        toks = [pa_token(x, -3.05, 0.9) for x in B32_TOKENS]
        pa_drop(self, toks, rt=0.4, lag=0.2, dist=3.0, with_=[FadeIn(pa_left(T("collaborate", 32), 2.1, -2.6))])
        d3, d4 = b32_dot(3).shift(DOWN * 1.6), b32_dot(4).shift(DOWN * 1.6)
        self.add(d3, d4)
        self.play(d3.animate.shift(UP * 1.6), d4.animate.shift(UP * 1.6), run_time=0.45)
        # keep the whole history: a bracket under the line
        until(self, "keep the whole history", lead=0.2)
        self.play(Create(b32_bracket()), FadeIn(pa_left(T("history", 32), -5.2, -1.65)), run_time=0.4)
        # experiment on a branch, merge back
        until(self, "experiment on a branch", lead=0.3)
        up, down, exp = b32_branch()
        self.play(Create(up), run_time=0.3)
        self.play(GrowFromCenter(exp), FadeIn(T("branch", 32).move_to([B32_BRANCH[0], 1.3, 0]), shift=DOWN * 0.1), run_time=0.3)
        until(self, "without breaking", lead=0.2)
        self.play(Create(down), GrowFromCenter(b32_dot(5)), run_time=0.4)
        done(self)
# ═════════════════════════════ PART B · B52 (Act V) · B60, B62 (Act VI) · B80 (Act VIII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB7_ / pb7_ / b52_ / b60_ / b62_ / b80_ so the parts never collide.
PB7_SMALL = "#917A55"                       # dark kraft: outlines of SMALL objects only (GATE T)
PB7_LINK = "#9C8462"                        # deep kraft: connectors (ink-edged connectors fuse objects into one blob)
PB7_PAD = "#EFEADF"                         # plinth top, within 28 of the stage (Gate V counts darker pads as ink)


def pb7_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb7_left(mob, x, y):
    """Left-align a text at x, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pb7_drop(self, mobs, rt=0.5, lag=0.2, dist=4.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt, rate_func=ease_in)


def pb7_plinth(iso, x0, y0, w, d, h=0.14):
    """A plinth: pale board on top, dark sides carry Gate V's contrast."""
    return iso.box(x0, y0, -h, w, d, h, PB7_PAD, DARK_L, DARK_R).set_z_index(-1)


def pb7_dashes(a, b, n=5, color=DIM, sw=5):
    """A broken (dashed) line from a to b: n dashes with gaps."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    g = VGroup()
    for k in range(n):
        t0, t1 = (k + 0.1) / n, (k + 0.65) / n
        g.add(Line(a + (b - a) * t0, a + (b - a) * t1, color=color, stroke_width=sw))
    return g


def pb7_dirbox(iso, sw=3):
    """A directory: a small kraft box (B60's cast; also the file-layout icon in B80)."""
    return iso.box(0, 0, 0, 0.9, 0.9, 0.6, sw=sw)


def pb7_page_on(iso, x=0.1, y=0.1, z=0.6, w=0.7, d=0.72):
    """A README page lying on a box top. Grey outline: an ink card inside an ink box reads as overlapping text (GATE T)."""
    pg = iso.page(x, y, z, w, d)
    pg[0].set_stroke(DIM)
    return pg


def pb7_person(x, y, s=1.0):
    """A person token standing with its feet at (x, y): grey body, ink outline."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head)


# ─────────────── B52 · accretion over months (clash, won't rebuild) vs one session from one file (rebuilds anywhere) ───────────────
B52_BIN = Iso(-4.3, -2.2, 0.62)             # the left environment bin (open: packages land inside)
B52_BOX = Iso(2.0, -2.2, 0.62)              # the right environment box, on its plinth
B52_BOX2 = Iso(4.9, -2.2, 0.62)             # the second plinth: the rebuilt copy
B52_PAGE = Iso(0.85, 1.55, 0.6)             # the environment.yml page
B52_CAL_Y = 2.3
B52_CAL_X = (-5.4, -4.2, -3.0, -1.8)        # four month cards: the calendar strip
B52_PKG = ((0.15, 0.15), (0.95, 0.2), (0.2, 0.95), (0.95, 0.9))   # package slots inside a bin (x, y on its floor)


def b52_month(cx):
    """A month card: white, grey outline, ghost day squares, one ghost day that turns terracotta when a package lands."""
    card = RoundedRectangle(width=1.05, height=0.9, corner_radius=0.07, fill_color=CARD, fill_opacity=1,
                            stroke_color=BAR1, stroke_width=4).move_to([cx, B52_CAL_Y, 0])
    days = VGroup()
    for r in range(3):
        for c in range(5):
            days.add(Square(side_length=0.11, fill_color=GHOST, fill_opacity=1, stroke_width=0)
                     .move_to([cx - 0.36 + c * 0.18, B52_CAL_Y + 0.22 - r * 0.22, 0]))
    mark = Dot([cx - 0.36 + 2 * 0.18, B52_CAL_Y + 0.22 - 1 * 0.22, 0], radius=0.075, color=GHOST)
    return VGroup(card, days, mark)


def b52_pkg(iso, x, y, s=0.55, clash=False):
    """A package: a small kraft cube with a dark-kraft outline (small object). A clashing one has grey faces."""
    if clash:
        return iso.box(x, y, 0, s, s, s * 1.1, BAR3, BAR2, BAR1, sw=3).set_z_index(1)
    b = iso.box(x, y, 0, s, s, s * 1.1, sw=3)
    b.set_stroke(PB7_SMALL)
    return b.set_z_index(1)


def b52_cross(iso, x, y, s=0.55):
    """A grey X over two clashing packages (grey: it sits inside the bin's ink outline)."""
    # the X sat on top of the packages and GATE T §8.6b read it as a label overlapping them; lift it above the bin
    c = iso.p(x + s / 2, y + s / 2, s * 1.1) + np.array([0, 0.75, 0])
    r = 0.3
    return VGroup(Line(c + np.array([-r, -r, 0]), c + np.array([r, r, 0]), color=BAR1, stroke_width=8),
                  Line(c + np.array([-r, r, 0]), c + np.array([r, -r, 0]), color=BAR1, stroke_width=8)).set_z_index(3)


def b52_broken_box(iso, w=1.9, d=1.5, h=0.55):
    """The rebuild that would not resolve: a box drawn only as grey dashes along its edges."""
    P = iso.p
    edges = [((0, 0, 0), (w, 0, 0)), ((0, 0, 0), (0, d, 0)), ((0, 0, 0), (0, 0, h)), ((w, 0, 0), (w, 0, h)),
             ((0, d, 0), (0, d, h)), ((0, 0, h), (w, 0, h)), ((0, 0, h), (0, d, h)), ((w, 0, h), (w, d, h)), ((0, d, h), (w, d, h))]
    return VGroup(*[pb7_dashes(P(*a), P(*b), n=4) for a, b in edges])


def b52_arrow(a, b):
    """A deep-kraft rebuild arrow between two screen points."""
    return Arrow(np.array(a), np.array(b), color=PB7_LINK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.18)


class B52_OneSessionVsAccretion(Scene):
    def construct(self):
        # LEFT · the calendar strip and the empty bin on its plinth are up from the first frame
        months = VGroup(*[b52_month(x) for x in B52_CAL_X])
        back, front = B52_BIN.open_box(0, 0, 0, 1.9, 1.5, 0.55)
        self.add(months, pb7_plinth(B52_BIN, -0.2, -0.2, 2.3, 1.9), back, front)
        self.play(FadeIn(T("over months", 34).move_to([-3.6, 1.45, 0]), shift=DOWN * 0.15), run_time=0.4)
        # added to over months: packages land one at a time, each lighting a day on the next month
        until(self, "Added to over months", lead=0.3)
        pkgs = []
        for k, (x, y) in enumerate(B52_PKG):
            p = b52_pkg(B52_BIN, x, y, clash=(k in (1, 3)))
            pkgs.append(p)
            p.shift(UP * 3.5)
            self.add(p)
            rt = guard(self, 0.32)
            self.play(p.animate.shift(DOWN * 3.5), months[k][2].animate.set_color(TERRA), run_time=rt, rate_func=ease_in)
        # two of them clash
        until(self, "collects conflicts", lead=0.2)
        self.play(Create(b52_cross(B52_BIN, 0.95, 0.55)), run_time=0.4)
        # the rebuild arrow ends in a broken box
        until(self, "it won't resolve", lead=0.6)
        broken = b52_broken_box(Iso(-1.35, -2.2, 0.62))
        arrow = b52_arrow(B52_BIN.p(2.25, 0.3, 0.45), Iso(-1.35, -2.2, 0.62).p(-0.55, 1.5, 0.45))
        self.play(Create(arrow), run_time=0.35)
        self.play(Create(broken), FadeIn(T("won't resolve", 34).move_to([-1.3, -2.85, 0])), run_time=0.5)
        # RIGHT · one file feeds one box in one session
        until(self, "Built in one session", lead=0.5)
        page = B52_PAGE.page(0, 0, 0, 1.1, 1.4)
        yml = pb7_left(M("environment.yml", 32), 1.75, 1.95)
        back2, front2 = B52_BOX.open_box(0, 0, 0, 1.9, 1.5, 0.55)
        pl2 = pb7_plinth(B52_BOX, -0.2, -0.2, 2.3, 1.9)
        link = Line(B52_PAGE.p(0.55, 0.7, -0.15), B52_BOX.p(0.95, 0.75, 1.25), color=PB7_LINK, stroke_width=5)
        self.play(FadeIn(page, shift=DOWN * 0.2), FadeIn(yml), FadeIn(pl2), FadeIn(back2), FadeIn(front2), run_time=0.45)
        self.play(Create(link), FadeIn(T("one session", 34).move_to([4.6, 0.3, 0])), run_time=0.3)
        pkgs2 = [b52_pkg(B52_BOX, x, y) for x, y in B52_PKG]
        pb7_drop(self, pkgs2, rt=0.45, lag=0.0, dist=2.6)                       # all at once
        # it resolves once: a check lands beside the box
        until(self, "it resolves once", lead=0.3)
        self.play(Create(check(3.6, -1.15, 0.26, TERRA, 8)), run_time=0.3)
        # and rebuilds anywhere: a copy appears on the second plinth
        until(self, "rebuilds anywhere", lead=0.75)
        pl3 = pb7_plinth(B52_BOX2, -0.2, -0.2, 2.3, 1.9)
        self.play(FadeIn(pl3), run_time=0.2)
        copy = VGroup(back2.copy(), *[p.copy() for p in pkgs2], front2.copy()).set_z_index(5)
        self.add(copy)
        self.play(copy.animate.shift(RIGHT * (B52_BOX2.ox - B52_BOX.ox)),
                  FadeIn(T("rebuilds anywhere", 34).move_to([3.9, -2.95, 0])), run_time=0.5)
        done(self)


# ─────────────── B60 · data/ → raw/ (locked, chmod 555) · processed/ · metadata/, each with a README; names that sort themselves ───────────────
B60_ROOT = Iso(0.0, 1.75, 0.6)
B60_KIDS = (Iso(-3.2, 0.35, 0.6), Iso(0.4, 0.35, 0.6), Iso(4.0, 0.35, 0.6))
B60_KID_NAMES = ("raw/", "processed/", "metadata/")
B60_LABEL_Y = -0.2
B60_NAMES = ("2024-01-15_experiment-data_v01.csv", "participant_demographics_2024-01-20.csv", "survey_responses_wave1_v03.csv")
B60_NAME_X, B60_NAME_Y = -5.9, (-1.45, -2.15, -2.85)
B60_CW = 8.46 / 34                          # Menlo at 32: screen units per character (measured)


def b60_link(iso_from, iso_to):
    """An elbow connector from the root box's base to a child box's top, in deep kraft, stopping short of both."""
    a = iso_from.p(0.45, 0.45, 0)
    b = iso_to.p(0.9, 0.9, 0.6)
    ymid = 1.5
    return VGroup(Line([a[0], a[1] - 0.08, 0], [a[0], ymid, 0], color=PB7_LINK, stroke_width=4),
                  Line([a[0], ymid, 0], [b[0], ymid, 0], color=PB7_LINK, stroke_width=4),
                  Line([b[0], ymid, 0], [b[0], b[1] + 0.08, 0], color=PB7_LINK, stroke_width=4))


def b60_lock(x, y):
    """A padlock beside raw/: kraft body with an ink outline, an ink shackle (drawn large: tiny locks read as sub-floor text)."""
    body = RoundedRectangle(width=0.62, height=0.5, corner_radius=0.08, fill_color=BOX_L, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    shackle = Arc(radius=0.2, start_angle=0, angle=PI, color=INK, stroke_width=6).move_to([x, y + 0.36, 0])
    return VGroup(shackle, body)


def b60_ring(row, i, n, color=BAR1, sw=3):
    """A grey ring around characters i..i+n of file-name row `row` (mono is fixed pitch: positions are arithmetic)."""
    cx = B60_NAME_X + (i + n / 2) * B60_CW
    ring = Ellipse(width=n * B60_CW + 0.18, height=0.56, color=color, stroke_width=sw).move_to([cx, B60_NAME_Y[row], 0])
    ring._qc_intentional = True                 # an editor's ring around part of a label, by design (layout audit's annotation flag)
    return ring


def b60_rings_for(kind):
    rings = VGroup()
    for r, name in enumerate(B60_NAMES):
        if kind == "date":
            i = name.find("2024-")
            if i >= 0:
                rings.add(b60_ring(r, i, 10))
        elif kind == "version":
            i = name.find("_v0")
            if i >= 0:
                rings.add(b60_ring(r, i + 1, 3))
        else:
            for i, ch in enumerate(name):
                if ch == "_":
                    rings.add(b60_ring(r, i, 1))
    return rings


class B60_DataTree(Scene):
    def construct(self):
        self.add(pb7_title("VI · Data"))
        root = pb7_dirbox(B60_ROOT)
        self.play(FadeIn(root, shift=DOWN * 0.2), FadeIn(pb7_left(M("data/", 32), 0.95, 2.25)), run_time=0.4)
        # three folders drop in under their connectors
        until(self, "Three folders", lead=0.2)
        links = VGroup(*[b60_link(B60_ROOT, k) for k in B60_KIDS])
        self.play(Create(links), run_time=0.4)
        kids = [pb7_dirbox(k) for k in B60_KIDS]
        labels = [M(s, 32).move_to([k.ox, B60_LABEL_Y, 0]) for s, k in zip(B60_KID_NAMES, B60_KIDS)]
        pb7_drop(self, kids, rt=0.6, lag=0.25, dist=3.0)
        self.play(*[FadeIn(l, shift=UP * 0.1) for l in labels], run_time=0.3)
        # each with its own README
        until(self, "Each with its own README", lead=0.2)
        pages = [pb7_page_on(k) for k in B60_KIDS]
        pb7_drop(self, pages, rt=0.5, lag=0.2, dist=2.5)
        self.play(FadeIn(pb7_left(M("README", 32), 4.75, 1.3), shift=LEFT * 0.1), run_time=0.3)
        # raw is read-only: a lock lands beside it, then the command
        until(self, "Make raw read-only", lead=0.2)
        lock = b60_lock(-4.3, 0.75)
        self.play(GrowFromCenter(lock), run_time=0.35)
        until(self, "c h mod", lead=0.1)
        self.play(FadeIn(M("chmod 555", 32).move_to([-3.2, -0.75, 0]), shift=UP * 0.1), run_time=0.3)
        until(self, "only the owner", lead=0.2)
        self.play(GrowFromCenter(Dot([-4.3, 0.75, 0], radius=0.08, color=TERRA)), run_time=0.25)   # the owner's key
        # names that sort themselves
        until(self, "And name files", lead=0.3)
        names = [pb7_left(M(s, 32), B60_NAME_X, y) for s, y in zip(B60_NAMES, B60_NAME_Y)]
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.2) for n in names], lag_ratio=0.3), run_time=0.7)
        until(self, "ISO dates", lead=0.15)
        self.play(Create(b60_rings_for("date")), run_time=0.35)
        until(self, "version numbers", lead=0.15)
        self.play(Create(b60_rings_for("version")), run_time=0.35)
        until(self, "underscores", lead=0.15)
        self.play(Create(b60_rings_for("under")), run_time=0.35)
        done(self)


# ─────────────── B62 · the data dictionary as a table, then 3 copies · 2 media · 1 off-site ───────────────
B62_COLS = ("variable", "type", "units", "range", "missing")
B62_X = (-5.9, -2.45, -0.15, 1.3, 4.75)                              # left edge of each column
B62_ROWS = (("subject_id", "integer", "", "", ""),
            ("age", "integer", "years", "18-65", "-99"),
            ("treatment", "categorical", "", "control/treatment", ""),
            ("response_time", "float", "ms", "200-5000", "-99"))
B62_HY, B62_Y0, B62_DY = 2.55, 1.9, 0.62
B62_L, B62_R = -6.0, 6.0
B62_STAGE = Iso(0.0, -2.35, 0.55)                                    # the backup row's floor
B62_BOX_X = (-4.4, -1.8, 0.8)                                        # the three copies (iso x of each box origin → screen x)


def b62_cell(fn, s, size, col, y):
    if not s:
        return VGroup()
    m = fn(s, size)
    return m.move_to([B62_X[col] + m.width / 2, y, 0])


def b62_row(k):
    cells = B62_ROWS[k]
    y = B62_Y0 - k * B62_DY
    g = VGroup(b62_cell(M, cells[0], 32, 0, y))
    for c in range(1, 5):
        g.add(b62_cell(T, cells[c], 32, c, y))
    return g


def b62_rule(k, sw=3):
    """The grey rule under row k (k = -1 is the rule under the header). Grey: table dividers never ink."""
    y = B62_Y0 - k * B62_DY - B62_DY / 2 + 0.03
    return Line([B62_L, y, 0], [B62_R, y, 0], color=BAR1, stroke_width=sw)


def b62_databox(sx):
    """A copy of the data: a small kraft box with a README page on its lid, standing at screen x = sx on the backup floor."""
    iso = Iso(sx, B62_STAGE.oy, 0.55)
    return VGroup(iso.box(0, 0, 0, 0.9, 0.9, 0.6, sw=3), pb7_page_on(iso))


def b62_disk(sx):
    """A disk under a copy: a dark squat cylinder (ellipse top, dark drum)."""
    top = Ellipse(width=1.25, height=0.5, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([sx, B62_STAGE.oy, 0])
    drum = Rectangle(width=1.25, height=0.3, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to([sx, B62_STAGE.oy - 0.15, 0])
    rim = Arc(radius=0.625, start_angle=PI, angle=PI, color=INK, stroke_width=3).stretch(0.4, 1).move_to([sx, B62_STAGE.oy - 0.3, 0])
    return VGroup(drum, rim, top).set_z_index(-1)


def b62_tape(sx):
    """A tape/cloud block under a copy: a dark block with two ghost ports."""
    iso = Iso(sx, B62_STAGE.oy - 0.22, 0.55)
    return iso.mcp(-0.15, -0.15, 0, 1.2, 1.2, 0.4).set_z_index(-1)


class B62_DictionaryAnd321(Scene):
    def construct(self):
        head = VGroup(*[b62_cell(lambda s, z: T(s, z, bold=True), t, 32, k, B62_HY) for k, t in enumerate(B62_COLS)])
        rules = VGroup(b62_rule(-1, 5), *[b62_rule(k) for k in range(4)])
        self.play(FadeIn(head), run_time=0.35)
        self.play(Create(rules), run_time=0.45)                                             # the frame splits into rows
        until(self, "makes the variables a table", lead=0.3)
        rows = [b62_row(k) for k in range(4)]
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.25) for r in rows], lag_ratio=0.3), run_time=1.0)
        # name, type, units, range, missing: a terracotta dot lands under each header as it is spoken
        for word, col in (("name", 0), ("type", 1), ("units", 2), ("range", 3), ("the missing code", 4)):
            until(self, word, lead=0.1)
            self.play(GrowFromCenter(Dot([B62_X[col] - 0.2, B62_HY, 0], radius=0.08, color=TERRA)), run_time=0.2)
        # three copies land
        until(self, "three copies", lead=0.35)
        boxes = [b62_databox(x) for x in B62_BOX_X]
        pb7_drop(self, boxes, rt=0.5, lag=0.25, dist=3.0, with_=[FadeIn(T("3", 44).move_to([-5.6, -2.0, 0]))])
        # two different media rise under the first two
        until(self, "two different media", lead=0.3)
        self.play(FadeIn(b62_disk(B62_BOX_X[0] - 0.05), shift=UP * 0.15), FadeIn(b62_tape(B62_BOX_X[1]), shift=UP * 0.15),
                  FadeIn(T("2", 44).move_to([-5.6, -2.9, 0])), run_time=0.4)
        # one goes off-site: the third copy rides to a distant plinth
        until(self, "one of them off-site", lead=0.55)
        far = pb7_plinth(Iso(4.6, B62_STAGE.oy, 0.55), -0.25, -0.25, 1.4, 1.4)
        self.play(FadeIn(far), FadeIn(T("1", 44).move_to([3.3, -2.0, 0])), run_time=0.2)
        b3 = boxes[2].set_z_index(5)
        a, b = np.array(b3.get_center()), np.array(b3.get_center()) + np.array([4.6 - B62_BOX_X[2], 0.0, 0.0])
        self.play(MoveAlongPath(b3, ArcBetweenPoints(a, b, angle=-PI / 3)),
                  FadeIn(T("off-site", 34).move_to([4.6, -3.0, 0])), run_time=0.55)
        done(self)


# ─────────────── B80 · five things to keep, each with its cast icon; the exercise card; any improvement counts ───────────────
B80_ROW_Y = (2.05, 1.2, 0.35, -0.5, -1.35)
B80_BOX_X = -5.7
B80_ICON_X = -0.55
B80_ITEMS = ("version control", "environment", "file layout", "documentation", "someone else runs it")
B80_CARD_X0, B80_CARD_X1, B80_CARD_Y0, B80_CARD_Y1 = 0.55, 6.05, -1.95, 2.6
B80_STEPS = ("environment.yml", "conda env create", "source activate", "conda install", "conda env export")
B80_STEP_Y = (1.9, 1.15, 0.4, -0.35, -1.1)
B80_STEP_BOX_X = 1.05
B80_DOT_X = -6.1                             # the "start this way" dots, left of the checkboxes


def b80_box(y, x=B80_BOX_X, stroke=INK):
    return Square(side_length=0.42, fill_color=CARD, fill_opacity=1, stroke_color=stroke, stroke_width=3).move_to([x, y, 0])


def b80_tick(y, x=B80_BOX_X, color=INK):
    return check(x, y - 0.02, 0.18, color, 6)


def b80_icon_versions(x, y):
    """Version control: three pages fanned (the cast page), one terracotta dot each."""
    iso = Iso(x - 0.3, y - 0.45, 0.5)
    return VGroup(*[iso.page(0.08 * k, 0.06 * k, 0.08 * k, 0.9, 1.0) for k in range(3)])


def b80_icon_env(x, y):
    """Environment: the kraft box with one terracotta tape (the cast job box)."""
    return job_box(Iso(x - 0.2, y - 0.5, 0.75))


def b80_icon_layout(x, y):
    """File layout: three small directory boxes in a row (B60's cast)."""
    return VGroup(*[pb7_dirbox(Iso(x - 0.55 + 0.5 * k, y - 0.45, 0.32)) for k in range(3)])


def b80_icon_docs(x, y):
    """Documentation: one README page."""
    return Iso(x - 0.2, y - 0.35, 0.6).page(0, 0, 0, 1.0, 1.1)


def b80_icon_runner(x, y):
    """Someone else runs it: a person token beside a small GPU block."""
    body, light = gpu_block(Iso(x + 0.1, y - 0.45, 0.5))
    return VGroup(pb7_person(x - 0.6, y - 0.4, 0.75), body, light)


def b80_card():
    return RoundedRectangle(width=B80_CARD_X1 - B80_CARD_X0, height=B80_CARD_Y1 - B80_CARD_Y0, corner_radius=0.12,
                            fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4) \
        .move_to([(B80_CARD_X0 + B80_CARD_X1) / 2, (B80_CARD_Y0 + B80_CARD_Y1) / 2, 0])


class B80_FiveAndTheExercise(Scene):
    def construct(self):
        self.add(pb7_title("VIII · Start Tomorrow"))
        rows = VGroup()
        for y, s in zip(B80_ROW_Y, B80_ITEMS):
            bx = b80_box(y)
            rows.add(bx, T(s, 34).next_to(bx, RIGHT, buff=0.35))
        self.play(FadeIn(rows, shift=RIGHT * 0.15), run_time=0.5)
        icons = (b80_icon_versions, b80_icon_env, b80_icon_layout, b80_icon_docs, b80_icon_runner)
        cues = ("Use version control", "Document your environment", "Organise files", "Write the documentation", "And test reproducibility")
        for k, (cue, mk) in enumerate(zip(cues, icons)):
            until(self, cue, lead=0.15)
            icon = mk(B80_ICON_X, B80_ROW_Y[k])
            self.play(Create(b80_tick(B80_ROW_Y[k])), GrowFromCenter(icon), run_time=0.4)
            if k == 4:
                self.play(icon[2].animate.set_color(TERRA), run_time=0.25)                # their machine lights up
        # the exercise card lands
        until(self, "The exercise", lead=0.3)
        card = b80_card()
        steps = VGroup()
        for y, s in zip(B80_STEP_Y, B80_STEPS):
            steps.add(b80_box(y, B80_STEP_BOX_X, stroke=PB7_SMALL), pb7_left(M(s, 32), B80_STEP_BOX_X + 0.45, y))
        pb7_drop(self, [VGroup(card, steps)], rt=0.5, dist=3.5,
                 with_=[FadeIn(T("exercise", 34).move_to([(B80_CARD_X0 + B80_CARD_X1) / 2, 2.95, 0]))])
        for cue, y in zip(("write an environment dot yml", "build it", "activate it", "install a couple more", "export the final file"), B80_STEP_Y):
            until(self, cue, lead=0.15)
            self.play(Create(b80_tick(y, B80_STEP_BOX_X, TERRA)), run_time=0.3)   # terracotta: an ink line inside the card's ink outline fuses (GATE T)
        # start the next project this way
        until(self, "Start the next project", lead=0.2)
        self.play(GrowFromCenter(Dot([B80_DOT_X, B80_ROW_Y[0], 0], radius=0.09, color=TERRA)), run_time=0.25)
        until(self, "document as you go", lead=0.15)
        self.play(GrowFromCenter(Dot([B80_DOT_X, B80_ROW_Y[3], 0], radius=0.09, color=TERRA)), run_time=0.25)
        until(self, "share when you can", lead=0.15)
        self.play(GrowFromCenter(Dot([B80_DOT_X, B80_ROW_Y[4], 0], radius=0.09, color=TERRA)), run_time=0.25)
        # any improvement counts
        until(self, "any improvement counts", lead=0.35)
        self.play(FadeIn(T("any improvement counts", 36).move_to([-2.9, -2.75, 0]), shift=UP * 0.15), run_time=0.45)
        done(self)


# attach the midpoint guard (see ST)
for _cls in (B10_ThreeWords, B20_TheCrisis, B21_FiveBarriers, B30_ThreePhaseChecklist, B32_VersionControl, B52_OneSessionVsAccretion, B60_DataTree, B62_DictionaryAnd321, B80_FiveAndTheExercise):
    _cls.play = ST.play
