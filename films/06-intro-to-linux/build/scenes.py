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
# ═════════════════════════════ PART A · B10 (Act I opener), B20 (Act II opener), B32 ═════════════════════════════
# Stage map. B10: the Linux kernel (dark block) centre, Unix (kraft box) above, three devices around it on
# deep-kraft lines. B20: a directory tree of small kraft boxes down the left, the colour swatches and the two
# mono paths on the right. B32: a file page left, a directory (kraft box with pages on top) right, both removed.
# The same directory box (kraft box, pages on top) is the picture of a directory in B20 and B32.
PA_KRAFT = "#9C8462"                        # deep-kraft connector (drawing law: connectors are never ink)


def pa_title(s):
    """Act title, top-left, for the whole beat."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_left(t, x, y):
    """Place a label by its left edge (labels sit beside objects)."""
    return t.move_to([x + t.width / 2, y, 0])


def pa_slide_in(self, mob, vec, rt=0.7):
    """Slide a whole object in from off-stage, fully opaque (GATE T: never a half-faded dark block)."""
    rt = guard(self, rt)
    mob.shift(-vec)
    self.add(mob)
    self.play(mob.animate.shift(vec), run_time=rt)


def pa_drop(self, mobs, rt=0.55, lag=0.2, dist=5.0):
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), run_time=rt, rate_func=ease_in)


def pa_link(a, b, sw=5):
    """A deep-kraft connector between two screen points (both stop short of what they join)."""
    return Line([a[0], a[1], 0], [b[0], b[1], 0], color=PA_KRAFT, stroke_width=sw)


def pa_dirbox(iso, pages=0):
    """A directory: a small kraft box, optionally with file pages lying on its top (grey page outlines:
    an ink-outlined card inside an ink-outlined box reads as overlapping text under GATE T)."""
    g = VGroup(iso.box(0, 0, 0, 0.9, 0.9, 0.6, sw=3))
    for k in range(pages):
        pg = iso.page(0.08 + 0.06 * k, 0.08 + 0.04 * k, 0.6 + 0.07 * k, 0.7, 0.72)
        pg[0].set_stroke(DIM)
        g.add(pg)
    return g


def pa_token(x, y, s=1.0):
    """A person token standing with its feet at (x, y)."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head).set_z_index(7)


# ─────────────── B10 · the Linux family: kernel, 1991, Unix → Linux / macOS, phone · laptop · cluster ───────────────
B10_K = Iso(0.3, -0.75, 0.75)               # the kernel block, centre
B10_U = Iso(0.3, 1.75, 0.55)                # the Unix box, above
B10_PHONE = Iso(-4.4, -0.2, 0.75)
B10_LAPTOP = Iso(-4.6, -2.75, 0.8)
B10_RACK = Iso(3.9, -2.0, 0.8)


def b10_kernel():
    return B10_K.box(0, 0, 0, 1.3, 1.3, 0.7, DARK_TOP, DARK_L, DARK_R)


def b10_unix():
    return B10_U.box(0, 0, 0, 1.2, 1.2, 0.5)


def b10_phone(iso=B10_PHONE):
    """A phone: a dark slab standing on end, one ghost screen on its front."""
    body = iso.box(0, 0, 0, 0.6, 0.14, 1.15, DARK_TOP, DARK_L, DARK_R)
    screen = iso.quad([(0.07, 0, 0.14), (0.53, 0, 0.14), (0.53, 0, 1.02), (0.07, 0, 1.02)], GHOST, sw=0).set_z_index(1)
    return VGroup(body, screen)


def b10_laptop(iso=B10_LAPTOP):
    """A small laptop: kraft base, dark screen standing on the back edge (same as film 3)."""
    base = iso.box(0, 0, 0, 1.2, 0.9, 0.08)
    screen = iso.quad([(0, 0.9, 0.08), (1.2, 0.9, 0.08), (1.2, 0.9, 0.85), (0, 0.9, 0.85)], DARK_TOP)
    return VGroup(base, screen)


def b10_tag(text, x, y, w):
    """A tag: a white pill with an ink label (no outline, so the label is not inside an outline)."""
    return VGroup(pill(x, y, w, 0.66), T(text, 38).move_to([x, y, 0]))


class B10_LinuxFamily(Scene):
    def construct(self):
        self.add(pa_title("I · What Linux Is"))
        pa_slide_in(self, b10_kernel(), UP * 5.5, 0.6)                      # the kernel rises into the centre
        self.add(pa_left(T("Linux", 44), 1.45, 0.45))
        until(self, "in 1991", lead=0.6)
        rule = Line([-0.6, -1.35, 0], [2.1, -1.35, 0], color=BAR1, stroke_width=4)
        self.play(GrowFromEdge(rule, LEFT), run_time=0.4)
        tick = Dot([0.3, -1.35, 0], radius=0.11, color=TERRA)
        self.play(GrowFromCenter(tick), FadeIn(T("1991", 40).move_to([1.15, -1.85, 0]), shift=UP * 0.15), run_time=0.35)
        until(self, "in the tradition of Unix", lead=0.4)
        pa_drop(self, [b10_unix()], 0.5)
        self.add(T("Unix", 44).move_to([-1.3, 2.2, 0]))
        until(self, "the much older system")
        self.play(Create(pa_link((0.3, 1.6), (0.3, 0.95))), run_time=0.35)           # Unix → Linux
        until(self, "also shaped macOS", lead=0.3)
        self.play(Create(pa_link((0.75, 1.65), (2.45, 1.05))), run_time=0.4)          # Unix → macOS
        self.add(pa_left(T("macOS", 44), 2.75, 0.9))
        until(self, "It runs on Android phones", lead=0.1)
        pa_slide_in(self, b10_phone(), RIGHT * 5, 0.5)
        self.play(Create(pa_link((-0.8, 0.0), (-3.8, 0.3))), run_time=0.3)
        self.add(T("phone", 40).move_to([-4.25, -0.72, 0]))
        until(self, "on laptops", lead=0.1)
        pa_slide_in(self, b10_laptop(), RIGHT * 5, 0.5)
        self.play(Create(pa_link((-0.85, -0.55), (-3.45, -1.75))), run_time=0.3)
        self.add(T("laptop", 40).move_to([-2.7, -2.4, 0]))
        until(self, "and on nearly every HPC cluster", lead=0.1)
        st, li = explorer_rack(B10_RACK)
        pa_slide_in(self, VGroup(st, li), LEFT * 5, 0.5)
        self.play(Create(pa_link((1.3, -0.5), (2.7, -0.95))), run_time=0.3)
        self.add(T("cluster", 40).move_to([3.9, -2.55, 0]))
        until(self, "It's free and open source", lead=0.2)
        self.play(GrowFromCenter(b10_tag("free · open source", 0.6, -2.75, 4.2)), run_time=0.4)
        until(self, "so anyone can contribute", lead=0.1)
        dots = VGroup(*[Dot([x, -2.35, 0], radius=0.1, color=TERRA) for x in (-0.5, 0.6, 1.7)]).set_z_index(5)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2), run_time=0.3)
        self.play(*[d.animate.move_to([0.3 + 0.35 * (k - 1), -0.95, 0]) for k, d in enumerate(dots)], run_time=0.7)   # contributions flow in
        self.play(FadeOut(dots, scale=0.3), run_time=0.25)
        until(self, "and it's considered secure and robust", lead=0.1)
        self.play(GrowFromCenter(b10_tag("secure · robust", 4.2, 2.4, 3.6)), run_time=0.4)
        until(self, "which is why servers")
        self.play(LaggedStart(*[l.animate.set_color(TERRA) for l in li], lag_ratio=0.3), run_time=0.5)   # the cluster runs it
        done(self)


# ─────────────── B20 · the tree, four colours, an absolute path from /, a relative path from where you stand ───────────────
B20_S = 0.5
B20_ROOT, B20_HOME, B20_USER = Iso(-4.4, 1.75, B20_S), Iso(-4.4, 0.35, B20_S), Iso(-4.4, -1.05, B20_S)
B20_DIR, B20_HERE = Iso(-5.4, -2.5, B20_S), Iso(-2.7, -2.5, B20_S)
B20_LBL_X = -3.7                                                      # left edge of the tree labels
B20_SW_X, B20_SW_LBL = 1.3, 1.9                                       # swatch centre, label left edge
B20_ROWS = ((BAR1, "directory", 2.4), ("#8A9A7B", "executable", 1.7), ("#B06A4A", "compressed", 1.0), (INK, "file", 0.3))
B20_PATH_X = 0.9                                                      # left edge of the two mono paths


def b20_links():
    return VGroup(pa_link((-4.4, 1.65), (-4.4, 1.2)), pa_link((-4.4, 0.25), (-4.4, -0.2)),
                  pa_link((-4.75, -1.15), (-5.15, -1.55)), pa_link((-4.05, -1.15), (-3.1, -1.6)))


def b20_labels():
    return VGroup(pa_left(M("/", 40), B20_LBL_X, 2.1), pa_left(M("home", 40), B20_LBL_X, 0.7),
                  pa_left(M("user", 40), B20_LBL_X, -0.7), M("dir", 40).move_to([-4.2, -2.15, 0]))


def b20_swatch(k):
    fill, word, y = B20_ROWS[k]
    sq = Square(side_length=0.5, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([B20_SW_X, y, 0])
    return VGroup(sq, pa_left(T(word, 40), B20_SW_LBL, y))


def b20_path(points):
    p = VMobject()
    p.set_points_as_corners([np.array([x, y, 0.0]) for x, y in points])
    return p


class B20_PathsAndColours(Scene):
    def construct(self):
        self.add(pa_title("II · Finding Your Way"))
        root, home, user = pa_dirbox(B20_ROOT), pa_dirbox(B20_HOME), pa_dirbox(B20_USER)
        pa_drop(self, [root, home, user], 0.8, 0.3)                                   # the tree draws, top down
        links, labels = b20_links(), b20_labels()
        self.play(Create(links[0]), Create(links[1]), run_time=0.35)
        self.add(labels[0], labels[1], labels[2])
        here = pa_dirbox(B20_HERE)
        dirbox = pa_dirbox(B20_DIR)
        pa_drop(self, [dirbox, here], 0.5, 0.3)
        self.play(Create(links[2]), Create(links[3]), run_time=0.3)
        self.add(labels[3])
        until(self, "as on Windows or a Mac", lead=0.3)
        files = pa_dirbox(B20_DIR, pages=2)
        pa_drop(self, [files[1], files[2]], 0.5, 0.3, dist=3.0)                      # files land in dir
        until(self, "blue for directories", lead=0.3)
        self.play(FadeIn(b20_swatch(0), shift=LEFT * 0.3), run_time=0.35)
        until(self, "green for executables", lead=0.3)
        self.play(FadeIn(b20_swatch(1), shift=LEFT * 0.3), run_time=0.35)
        until(self, "red for compressed", lead=0.3)
        self.play(FadeIn(b20_swatch(2), shift=LEFT * 0.3), run_time=0.35)
        until(self, "plain for ordinary files", lead=0.3)
        self.play(FadeIn(b20_swatch(3), shift=LEFT * 0.3), run_time=0.35)
        until(self, "A path is", lead=0.1)
        self.play(FadeIn(pa_left(M("/home/user/dir", 40), B20_PATH_X, -1.0), shift=UP * 0.2), run_time=0.4)
        until(self, "Absolute: from the root", lead=0.2)
        dot = Dot([-4.4, 2.1, 0], radius=0.12, color=TERRA).set_z_index(9)
        self.play(GrowFromCenter(dot), run_time=0.25)
        self.play(MoveAlongPath(dot, b20_path([(-4.4, 2.1), (-4.4, 0.7), (-4.4, -0.7), (-5.4, -2.0)])), run_time=1.3)   # / → home → user → dir
        until(self, "Relative: from where you stand", lead=0.2)
        self.play(FadeIn(pa_token(-2.7, -1.98, 0.7), shift=DOWN * 0.5), run_time=0.4)        # you stand here
        self.play(FadeIn(pa_left(M("../dir", 40), B20_PATH_X, -2.1), shift=UP * 0.2), run_time=0.35)
        dot2 = Dot([-2.7, -2.15, 0], radius=0.12, color=TERRA).set_z_index(9)
        self.play(GrowFromCenter(dot2), run_time=0.2)
        self.play(MoveAlongPath(dot2, b20_path([(-2.7, -2.15), (-4.4, -0.7), (-5.4, -2.0)])), run_time=0.9)   # up one, over into dir
        until(self, "One dot is here", lead=0.2)
        self.play(FadeIn(pa_left(M(". here", 40), -2.0, -2.15), shift=LEFT * 0.2), run_time=0.35)
        until(self, "Two dots is one level up", lead=0.2)
        self.play(FadeIn(pa_left(M(".. up", 40), -1.7, -0.7), shift=LEFT * 0.2), run_time=0.35)
        done(self)


# ─────────────── B32 · rm removes the file, rm -r the directory; no trash can, no undo ───────────────
B32_PAGE = Iso(-3.3, -1.0, 1.3)
B32_DIR = Iso(2.3, -1.6, 1.5)
B32_RACK = Iso(4.6, -2.75, 0.8)


def b32_page():
    return B32_PAGE.page(0, 0, 0, 1.4, 1.7)


def b32_bin():
    """Where a trash can would be: a dashed grey outline of one, and nothing in it."""
    body = DashedVMobject(Polygon([-1.0, -2.9, 0], [0.4, -2.9, 0], [0.55, -1.3, 0], [-1.15, -1.3, 0],
                                  stroke_color=BAR1, stroke_width=5, fill_opacity=0), num_dashes=22)
    lid = DashedVMobject(Line([-1.35, -1.1, 0], [0.75, -1.1, 0], stroke_color=BAR1, stroke_width=5), num_dashes=7)
    return VGroup(body, lid)


class B32_RemoveIsForever(Scene):
    def construct(self):
        self.add(pa_title("III · Making And Moving Files"))
        page, folder = b32_page(), pa_dirbox(B32_DIR, pages=2)
        self.add(page, folder)
        cmd1 = M("rm new_name", 44).move_to([-3.3, 2.0, 0])
        self.play(FadeIn(cmd1, shift=DOWN * 0.3), run_time=0.35)                     # the command lands
        until(self, "removes a file", lead=0.0)
        self.play(FadeOut(page, scale=0.6), run_time=0.5)                             # and the file is gone
        until(self, "dash r removes a directory", lead=0.2)
        cmd2 = M("rm -r new_dir_copy", 44).move_to([2.3, 1.3, 0])
        self.play(FadeIn(cmd2, shift=DOWN * 0.3), run_time=0.35)
        until(self, "and everything in it", lead=0.3)
        self.play(FadeOut(folder[2], scale=0.6), FadeOut(folder[1], scale=0.6), run_time=0.35)   # its contents first
        self.play(FadeOut(folder[0], scale=0.6), run_time=0.4)                                    # then the directory
        until(self, "There is no trash can", lead=0.1)
        self.play(Create(b32_bin()), run_time=0.7)                                    # the outline where a trash can would be
        until(self, "and no undo", lead=0.1)
        self.play(FadeIn(T("no undo", 44).move_to([1.9, -2.1, 0]), shift=LEFT * 0.2), run_time=0.35)
        until(self, "On a cluster", lead=0.1)
        st, li = explorer_rack(B32_RACK)
        pa_slide_in(self, VGroup(st, li), LEFT * 4, 0.5)
        until(self, "so read the command twice", lead=0.1)
        self.play(Indicate(cmd1, color=None, scale_factor=1.12), run_time=0.45)      # read it ...
        self.play(Indicate(cmd2, color=None, scale_factor=1.12), run_time=0.45)      # ... twice
        until(self, "before you press return", lead=0.1)
        self.play(LaggedStart(*[l.animate.set_color(TERRA) for l in li], lag_ratio=0.3), run_time=0.4)
        done(self)
# ═════════════════════════════ PART B · B50 B51 (Act V) · B71 (Act VII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB_ / pb_ / b50_ / b51_ / b71_ so the parts never collide.
# Laws kept here: brackets and grid rules in BAR1 grey (never an ink line under ink text); terracotta only as
# dots; numerals and labels in ink, beside objects; small objects outlined in dark kraft; every number and name
# on screen is in the beat's narration or visual_intent (B51's line is copied exactly).
PB_SMALL = "#917A55"      # dark kraft: outlines of SMALL objects only (tokens, the directory icon)
PB_BELT = "#E4E0D4"       # belts stay within 28 of the stage (Gate V)
PB_ADV32 = 0.249          # Menlo advance per character at size 32 (measured; Gate A's stub measures text differently, so fixed)


def pb_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb_base(mob, s, size, x, y, mono=False):
    """Set a text on a BASELINE at y (centre x), so neighbouring words with and without descenders line up.
    Descender depth is proportional to the size (measured: Menlo 0.098 at 32, EB Garamond 0.134 at 32)."""
    desc = (0.00306 if mono else 0.0042) * size if any(c in "gjpqy" for c in s) else 0.0
    return mob.move_to([x, y - desc + mob.height / 2.0, 0])


def pb_M(s, size, x, y_base):
    return pb_base(M(s, size), s, size, x, y_base, mono=True)


def pb_T(s, size, x, y_base):
    return pb_base(T(s, size), s, size, x, y_base)


def pb_figure(x, y, s=1.0, sw=3):
    """A person token standing at (x, y): film 1's B20 token (trapezoid body, round head), flat on the stage."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=PB_SMALL, stroke_width=sw)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=PB_SMALL, stroke_width=sw).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head)


def pb_drop(self, mobs, rt=0.5, lag=0.2, dist=3.0):
    """Land objects from above, fully opaque (GATE T: never a half-faded object)."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), run_time=rt, rate_func=ease_in)


def pb_bracket(x0, x1, y, tick=0.13):
    """A grey bracket under a run of text: a bar at y with ticks pointing up toward the text."""
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=BAR1, stroke_width=4),
                  Line([x0, y, 0], [x0, y + tick, 0], color=BAR1, stroke_width=4),
                  Line([x1, y, 0], [x1, y + tick, 0], color=BAR1, stroke_width=4))


# ─────────────── B50 · three audiences × three permissions ───────────────
B50_CX = (-1.0, 1.4, 3.8)                   # column centres: user · group · others
B50_RY = (0.55, -0.55, -1.65)               # row centres: read · write · execute
B50_GX = (-2.2, 0.2, 2.6, 5.0)              # grid rules (vertical)
B50_GY = (1.1, 0.0, -1.1, -2.2)             # grid rules (horizontal)
B50_TOK_Y = 1.75                            # feet of the audience tokens
B50_WORD_Y = 1.42                           # the audience words, under their tokens
B50_LABEL_R = -2.6                          # row words end here (beside the grid)
B50_NUM_X = -4.45                           # the numerals, beside the row words
B50_DIR = np.array([-5.45, -1.65, 0.0])     # the directory icon, beside 'execute'


def b50_grid():
    return VGroup(*[Line([x, B50_GY[0], 0], [x, B50_GY[-1], 0], color=BAR1, stroke_width=4) for x in B50_GX],
                  *[Line([B50_GX[0], y, 0], [B50_GX[-1], y, 0], color=BAR1, stroke_width=4) for y in B50_GY])


def b50_audience(k):
    """Column k's token(s): one figure, three figures, a crowd of five."""
    x = B50_CX[k]
    if k == 0:
        return VGroup(pb_figure(x, B50_TOK_Y, 0.95))
    if k == 1:
        return VGroup(*[pb_figure(x + d, B50_TOK_Y + 0.08, 0.72) for d in (-0.6, 0.0, 0.6)])
    return VGroup(*[pb_figure(x + d, B50_TOK_Y + 0.18, 0.52) for d in (-0.88, -0.44, 0.0, 0.44, 0.88)])


def b50_word(s, k):
    return pb_T(s, 34, B50_CX[k], B50_WORD_Y - 0.1)


def b50_row_word(s, r):
    t = T(s, 36)
    return pb_base(t, s, 36, B50_LABEL_R - t.width / 2, B50_RY[r] - 0.12)


def b50_dots(r):
    return VGroup(*[Dot([x, B50_RY[r], 0], radius=0.17, color=TERRA) for x in B50_CX])


def b50_numeral(s, r):
    return T(s, 48, bold=True).move_to([B50_NUM_X, B50_RY[r], 0])


def b50_directory():
    """A small directory: kraft folder with a tab, dark-kraft outline. Returns (folder, door); the door swings open."""
    c = B50_DIR
    body = RoundedRectangle(width=0.95, height=0.68, corner_radius=0.06, fill_color=BOX_TOP, fill_opacity=1,
                            stroke_color=PB_SMALL, stroke_width=3).move_to(c)
    tab = Rectangle(width=0.36, height=0.14, fill_color=BOX_TOP, fill_opacity=1, stroke_color=PB_SMALL,
                    stroke_width=3).move_to(c + np.array([-0.29, 0.40, 0]))
    door = Rectangle(width=0.24, height=0.4, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to(c + np.array([0.0, -0.12, 0]))
    return VGroup(body, tab), door


class B50_ThreeByThree(Scene):
    def construct(self):
        self.add(pb_title("V · Who May Do What"))
        self.play(Create(b50_grid()), run_time=0.7)
        until(self, "the user who owns it")
        pb_drop(self, [b50_audience(0), b50_word("user", 0)], 0.45, 0.1)
        until(self, "the group that owns it")
        pb_drop(self, [b50_audience(1), b50_word("group", 1)], 0.45, 0.1)
        until(self, "and others")
        pb_drop(self, [b50_audience(2), b50_word("others", 2)], 0.45, 0.1)
        until(self, "read, write, and")
        self.play(FadeIn(b50_row_word("read", 0)), LaggedStart(*[GrowFromCenter(d) for d in b50_dots(0)], lag_ratio=0.3), run_time=0.45)
        until(self, "write, and execute")
        self.play(FadeIn(b50_row_word("write", 1)), LaggedStart(*[GrowFromCenter(d) for d in b50_dots(1)], lag_ratio=0.3), run_time=0.45)
        until(self, "execute, which")
        self.play(FadeIn(b50_row_word("execute", 2)), LaggedStart(*[GrowFromCenter(d) for d in b50_dots(2)], lag_ratio=0.3), run_time=0.45)
        until(self, "for a directory")
        folder, door = b50_directory()
        self.play(FadeIn(folder, shift=UP * 0.3), run_time=0.35)
        self.add(door)
        until(self, "means entering it")
        hinge = door.get_left()
        self.play(Rotate(door, angle=-PI / 4, about_point=np.array(hinge)), run_time=0.5)
        until(self, "read four")
        self.play(FadeIn(b50_numeral("4", 0), shift=RIGHT * 0.25), run_time=0.3)
        until(self, "write two")
        self.play(FadeIn(b50_numeral("2", 1), shift=RIGHT * 0.25), run_time=0.3)
        until(self, "execute one")
        self.play(FadeIn(b50_numeral("1", 2), shift=RIGHT * 0.25), run_time=0.3)
        done(self)


# ─────────────── B51 · the long-listing line, decoded ───────────────
# The line is `-rwxrw-r-- 1 user group 46 Feb 14 16:37 File.txt` (49 characters), one row at size 32 (11.95 units,
# the largest size that fits ±6.2). Each token is its own mono Text placed by character index × advance, so no
# token holds a space (Pango collapses some single spaces on this Mac).
B51_Y = 2.5                                  # the line
B51_X0 = -5.83                               # left edge of character 0 (line centred at x = +0.15)
B51_TOKENS = (("-", 0), ("rwx", 1), ("rw-", 4), ("r--", 7), ("1", 11), ("user", 13), ("group", 18), ("46", 24),
              ("Feb", 27), ("14", 31), ("16:37", 34), ("File.txt", 40))
B51_BR_Y = 2.05                              # brackets under the line (ticks rise to 2.18; glyph bottoms sit at 2.28)
B51_HI_Y, B51_LO_Y = 1.68, 1.24              # two label rows, so neighbouring labels never touch
B51_BAND_X = (-3.6, 0.0, 3.6)                # the lifted triads
B51_BAND_Y = 0.3
B51_BAND_BR_Y = -0.3
B51_BAND_LABEL_Y = -0.72
B51_READ_Y = -1.5


def b51_x(start, n):
    """Centre x of the run of n characters starting at character index `start`."""
    return B51_X0 + PB_ADV32 * (start + n / 2.0)


def b51_token(s, start, size=32):
    return pb_M(s, size, b51_x(start, len(s)), B51_Y - 0.17)


def b51_line():
    """The twelve tokens of the line, in order. Index 0 is the type character; 1–3 the three triads."""
    return [b51_token(s, i) for s, i in B51_TOKENS]


def b51_under(start, n):
    """A grey bracket under the run of n characters at `start` (0.03 in from each end)."""
    x0 = B51_X0 + PB_ADV32 * start + 0.03
    return pb_bracket(x0, x0 + PB_ADV32 * n - 0.06, B51_BR_Y)


def b51_label(s, start, n, hi=True):
    return pb_T(s, 32, b51_x(start, n), (B51_HI_Y if hi else B51_LO_Y) - 0.1)


def b51_band_bracket(k):
    x = B51_BAND_X[k]
    return pb_bracket(x - 0.52, x + 0.52, B51_BAND_BR_Y)


def b51_band_label(s, k):
    return pb_T(s, 34, B51_BAND_X[k], B51_BAND_LABEL_Y - 0.1)


def b51_reading(s, k):
    return pb_T(s, 36, B51_BAND_X[k], B51_READ_Y - 0.1)


class B51_DecodeTheLine(Scene):
    def construct(self):
        toks = b51_line()
        line = VGroup(*toks)
        line.shift(UP * 0.5)
        self.play(line.animate.shift(DOWN * 0.5), run_time=0.6)
        until(self, "The first character")
        self.play(Create(b51_under(0, 1)), FadeIn(b51_label("type", 0, 1)), run_time=0.4)
        # the type character tries its three values: - for a file, d for a directory, l for a link
        type_tok = toks[0]
        until(self, "d for a directory")
        d_tok = b51_token("d", 0)
        self.play(FadeOut(type_tok), FadeIn(d_tok), run_time=0.25)
        until(self, "l for a link")
        l_tok = b51_token("l", 0)
        self.play(FadeOut(d_tok), FadeIn(l_tok), run_time=0.25)
        until(self, "Then nine characters")
        dash_tok = b51_token("-", 0)
        self.play(FadeOut(l_tok), FadeIn(dash_tok), run_time=0.25)
        self.play(*[Create(b51_under(s, 3)) for s in (1, 4, 7)], run_time=0.4)
        until(self, "three groups of three")
        triads = toks[1:4]
        self.play(*[t.animate.scale(1.5).move_to([B51_BAND_X[k], B51_BAND_Y, 0]) for k, t in enumerate(triads)], run_time=0.8)
        until(self, "the owner's permissions")
        self.play(Create(b51_band_bracket(0)), FadeIn(b51_band_label("owner", 0)), run_time=0.35)
        until(self, "the group's")
        self.play(Create(b51_band_bracket(1)), FadeIn(b51_band_label("group", 1)), run_time=0.35)
        until(self, "everyone else's")
        self.play(Create(b51_band_bracket(2)), FadeIn(b51_band_label("others", 2)), run_time=0.35)
        until(self, "the owner can read")
        self.play(FadeIn(b51_reading("read write execute", 0), shift=UP * 0.2), run_time=0.4)
        until(self, "the group can read")
        self.play(FadeIn(b51_reading("read write", 1), shift=UP * 0.2), run_time=0.4)
        until(self, "others can only read")
        self.play(FadeIn(b51_reading("read", 2), shift=UP * 0.2), run_time=0.4)
        until(self, "the link count")
        self.play(Create(b51_under(11, 1)), FadeIn(b51_label("links", 11, 1)), run_time=0.3)
        until(self, "the owner, the group")
        self.play(Create(b51_under(13, 4)), FadeIn(b51_label("owner", 13, 4, hi=False)), run_time=0.3)
        until(self, "the group, the size")
        self.play(Create(b51_under(18, 5)), FadeIn(b51_label("group", 18, 5)), run_time=0.3)
        until(self, "the size in bytes")
        self.play(Create(b51_under(24, 2)), FadeIn(b51_label("size", 24, 2, hi=False)), run_time=0.3)
        until(self, "the modification time")
        self.play(Create(b51_under(27, 12)), FadeIn(b51_label("time", 27, 12)), run_time=0.3)
        until(self, "and the name")
        self.play(Create(b51_under(40, 8)), FadeIn(b51_label("name", 40, 8, hi=False)), run_time=0.3)
        done(self)


# ─────────────── B71 · the toolbelt: ten commands, one address ───────────────
B71_CMDS = ("pwd", "ls", "cd", "touch", "mkdir", "cp", "mv", "rm", "less", "chmod")
B71_CUES = ("Prompt", "path", "list", "move", "make", "copy", "copy", "remove", "read", "permissions")
B71_PAD, B71_GAP = 0.17, 0.08                # pill padding each side of the mono text, gap between pills (ten pills span 12.1)
B71_BELT_Y = -0.5                            # the belt's front edge; its top face runs -0.5 … -0.2
B71_CHIP_Y = -0.02                           # pills sit on the belt's top face
B71_TAG_Y = 0.98                             # the 'no undo' tag above the rm chip
B71_MAIL_Y = -1.75                           # the address, beneath the belt
B71_HOURS_Y = -2.6                           # 'office hours on Zoom', beneath the address


def b71_widths():
    return [len(c) * PB_ADV32 + 2 * B71_PAD for c in B71_CMDS]


def b71_centres():
    """Pill centres, the whole row centred on x = 0 (fixed arithmetic, not measured text)."""
    ws = b71_widths()
    total = sum(ws) + B71_GAP * (len(ws) - 1)
    xs, x = [], -total / 2.0
    for w in ws:
        xs.append(x + w / 2.0)
        x += w + B71_GAP
    return xs


def b71_belt(x0=-6.1, x1=5.8, y=B71_BELT_Y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes (edges dark kraft, never ink). Film 1's B13 belt."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PB_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PB_BELT, fill_opacity=1, stroke_color=PB_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def b71_chip(k):
    """A pale pill (CARD fill, grey outline) carrying one mono command in ink."""
    x, w = b71_centres()[k], b71_widths()[k]
    body = RoundedRectangle(width=w, height=0.62, corner_radius=0.31, fill_color=CARD, fill_opacity=1,
                            stroke_color=BAR1, stroke_width=2.5).move_to([x, B71_CHIP_Y, 0])
    return VGroup(body, pb_M(B71_CMDS[k], 32, x, B71_CHIP_Y - 0.12))


def b71_tag():
    """The dashed 'no undo' tag above the rm chip: grey dashed frame, ink words."""
    x = b71_centres()[7]
    w, h = 1.9, 0.56
    pts = [np.array([x - w / 2, B71_TAG_Y - h / 2, 0]), np.array([x + w / 2, B71_TAG_Y - h / 2, 0]),
           np.array([x + w / 2, B71_TAG_Y + h / 2, 0]), np.array([x - w / 2, B71_TAG_Y + h / 2, 0])]
    frame = VGroup(*[DashedLine(pts[i], pts[(i + 1) % 4], color=BAR1, stroke_width=3, dash_length=0.12) for i in range(4)])
    return VGroup(frame, T("no undo", 32).move_to([x, B71_TAG_Y, 0]))


class B71_TheToolbelt(Scene):
    def construct(self):
        self.add(pb_title("VII · Quick Tips"))
        self.play(GrowFromEdge(b71_belt(), LEFT), run_time=0.6)
        for k, cue in enumerate(B71_CUES):
            until(self, cue, lead=0.3)
            pb_drop(self, [b71_chip(k)], 0.3, dist=2.6)
            if k == 7:
                until(self, "with care", lead=0.0)
                self.play(FadeIn(b71_tag(), shift=DOWN * 0.2), run_time=0.35)
        until(self, "r c help")
        mail = pb_M("rchelp@northeastern.edu", 40, 0.0, B71_MAIL_Y)
        pb_drop(self, [mail], 0.45, dist=1.2)
        until(self, "office hours")
        self.play(FadeIn(pb_T("office hours on Zoom", 34, 0.0, B71_HOURS_Y), shift=UP * 0.2), run_time=0.4)
        done(self)


# attach the midpoint guard (see ST)
for _cls in (B50_ThreeByThree, B51_DecodeTheLine, B71_TheToolbelt, B10_LinuxFamily, B20_PathsAndColours, B32_RemoveIsForever):
    _cls.play = ST.play
