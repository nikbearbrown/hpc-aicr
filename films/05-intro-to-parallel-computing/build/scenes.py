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
# ═════════════════════════════ PART A · B10 (Act I) · B20 (Act II) · B30 B31 (Act III) · B50 (Act V) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PA_ / pa_ / b10_ / b20_ / b30_ / b31_ / b50_ so the parts never collide.
#
# Stage map. B10: three flat timeline grids stacked (serial 9 slots, pipelined 5, data-parallel 3), kraft blocks in
# three kraft tones (wash / dry / fold, legend at the top), the slot count as an ink numeral beside each grid.
# B20: a 2 x 2 grid in grey with ink axis arrows, one acronym and one tiny cast picture per cell, terracotta dots on
# SIMD and MIMD. B30: a node is a thin plinth (pale board, dark sides) with pale core pads and a kraft memory slab;
# the left node's pads cable to one slab (OpenMP), three right nodes each own a slab and share a belt (MPI), then
# "hybrid" cables each right node's pads to its own slab. B31: the same plinth, 20 pads in 4 x 5, process frames in
# deep kraft spanning the pads, one terracotta dot per process (the rank), mono flags on the right. B50: a 12 x 8
# Life grid of pale cells with gaps, live cells dark, a glider stepping twice, a kraft ring round one cell's eight
# neighbours, a grey cursor sweeping row by row, then four bands sweeping at once.
PA_KRAFT = "#9C8462"                        # deep-kraft connector: cables, frames, belt dots (lines are never ink inside an ink bbox)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T: small ink rings fuse)
PA_PAD = "#E4E0D4"                          # pads, boards and dead cells stay within 28 of the stage (Gate V does not count them as ink)


def pa_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_at(mob, x_left, y):
    """Place a text by its LEFT edge."""
    return mob.move_to([x_left + mob.width / 2, y, 0])


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


def pa_plinth(iso, x0, y0, w, d):
    """A node: a thin plinth, pale board on top, dark sides carry Gate V's contrast."""
    return iso.box(x0, y0, -0.12, w, d, 0.12, PA_PAD, DARK_L, DARK_R).set_z_index(-1)


def pa_pad(iso, x, y, s):
    """A core pad lying on a plinth (small object: dark-kraft outline)."""
    return iso.quad([(x, y, 0.02), (x + s, y, 0.02), (x + s, y + s, 0.02), (x, y + s, 0.02)], PA_PAD, stroke=PA_SMALL, sw=3).set_z_index(1)


def pa_slab(iso, x, y, w, d, h):
    """A kraft memory slab standing at the back of a plinth."""
    return iso.box(x, y, 0, w, d, h).set_z_index(1)


def pa_cable(a, b, w=5):
    return Line(a, b, color=PA_KRAFT, stroke_width=w).set_z_index(2)


def pa_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes (edges dark kraft, never ink)."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PA_PAD, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


# ─────────────── B10 · laundry: serial 9, pipelined 5, data-parallel 3 ───────────────
B10_X0, B10_P, B10_W, B10_H, B10_RP = -5.4, 0.7, 0.6, 0.32, 0.4      # slot-0 centre, slot pitch, block size, row pitch
B10_ROWY = (1.75, 0.0, -1.75)                                        # y of load 0 in each of the three grids
B10_FILL = (BOX_L, BOX_R, BOX_FLOOR)                                 # wash / dry / fold
B10_LAB_X, B10_NUM_X = 2.6, 5.2


def b10_block(slot, row, stage, y0):
    return Rectangle(width=B10_W, height=B10_H, fill_color=B10_FILL[stage], fill_opacity=1, stroke_color=PA_SMALL, stroke_width=2) \
        .move_to([B10_X0 + slot * B10_P, y0 - row * B10_RP, 0])


def b10_grid(kind, y0):
    """Three loads x three stages, placed by the source's tables; blocks returned in slot order."""
    specs = []
    for r in range(3):
        for s in range(3):
            slot = {"serial": 3 * r + s, "pipe": r + s, "par": s}[kind]
            specs.append((slot, r, s))
    specs.sort()
    return VGroup(*[b10_block(sl, r, s, y0) for sl, r, s in specs])


def b10_legend():
    g = VGroup()
    for k, (x, w) in enumerate(((-0.1, "wash"), (1.8, "dry"), (3.5, "fold"))):
        g.add(Square(side_length=0.3, fill_color=B10_FILL[k], fill_opacity=1, stroke_color=PA_SMALL, stroke_width=2).move_to([x, 2.45, 0]),
              pa_at(T(w, 34), x + 0.45, 2.45))
    return g


def b10_label(word, k):
    return T(word, 36).move_to([B10_LAB_X, B10_ROWY[k] - 0.4, 0])


def b10_num(n, k):
    return T(n, 84).move_to([B10_NUM_X, B10_ROWY[k] - 0.4, 0])


class B10_Laundry(Scene):
    def construct(self):
        self.add(pa_title("I · Why Parallel"))
        until(self, "Simulations")
        bar = Rectangle(width=5.4, height=0.44, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-2.6, 0.0, 0])
        self.play(GrowFromEdge(bar, LEFT), run_time=0.8)                                   # the work, one piece
        until(self, "so we split the work", lead=0.3)
        pieces = VGroup(*[Rectangle(width=1.7, height=0.44, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-4.4 + 1.8 * k, 0, 0])
                          for k in range(3)])
        self.remove(bar)
        self.add(pieces)
        self.play(pieces[0].animate.shift(LEFT * 0.35), pieces[2].animate.shift(RIGHT * 0.35), run_time=0.5)   # split
        until(self, "Think of laundry")
        self.play(FadeOut(pieces), FadeIn(b10_legend()), run_time=0.5)
        until(self, "Serial:")
        ga = b10_grid("serial", B10_ROWY[0])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in ga], lag_ratio=0.12), run_time=1.3)
        self.add(b10_label("serial", 0))
        until(self, "Nine steps")
        self.play(FadeIn(b10_num("9", 0), scale=0.7), run_time=0.4)
        until(self, "Pipelining:")
        gb = b10_grid("pipe", B10_ROWY[1])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in gb], lag_ratio=0.12), run_time=1.1)
        self.add(b10_label("pipelined", 1))
        until(self, "Five steps")
        self.play(FadeIn(b10_num("5", 1), scale=0.7), run_time=0.4)
        until(self, "Data parallelism:")
        gc = b10_grid("par", B10_ROWY[2])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in gc], lag_ratio=0.12), run_time=0.9)
        self.add(b10_label("data parallel", 2))
        until(self, "Three steps")
        self.play(FadeIn(b10_num("3", 2), scale=0.7), run_time=0.4)
        until(self, "cut a big problem")
        self.play(Indicate(gc, color=None, scale_factor=1.06), run_time=0.7)
        done(self)


# ─────────────── B20 · Flynn's four kinds: a 2 x 2 grid, one tiny cast picture per cell ───────────────
B20_X0, B20_X1, B20_XM = -3.2, 4.6, 0.7                              # grid edges and the column divider
B20_Y0, B20_Y1, B20_YM = -3.1, 2.1, -0.5                             # grid edges and the row divider
B20_CW, B20_CH = 3.9, 2.6                                            # cell size
B20_CELL = {"SISD": (0, 0), "MISD": (1, 0), "SIMD": (0, 1), "MIMD": (1, 1)}   # (column: instruction, row: data)


def b20_cell(name):
    """(x0, y1): the top-left corner of the cell."""
    i, j = B20_CELL[name]
    return B20_X0 + i * B20_CW, B20_Y1 - j * B20_CH


def b20_pic(name):
    """Centre of the picture area in the cell."""
    x0, y1 = b20_cell(name)
    return x0 + 1.95, y1 - 1.6


def b20_grid():
    return VGroup(Rectangle(width=B20_X1 - B20_X0, height=B20_Y1 - B20_Y0, stroke_color=BAR2, stroke_width=3, fill_opacity=0)
                  .move_to([(B20_X0 + B20_X1) / 2, (B20_Y0 + B20_Y1) / 2, 0]),
                  Line([B20_XM, B20_Y0, 0], [B20_XM, B20_Y1, 0], color=BAR2, stroke_width=3),
                  Line([B20_X0, B20_YM, 0], [B20_X1, B20_YM, 0], color=BAR2, stroke_width=3))


def b20_axis_x():
    return Arrow([B20_X0, B20_Y1, 0], [B20_X1 + 0.3, B20_Y1, 0], color=INK, stroke_width=5, buff=0)


def b20_axis_y():
    return Arrow([B20_X0, B20_Y1, 0], [B20_X0, B20_Y0 - 0.1, 0], color=INK, stroke_width=5, buff=0)


def b20_acr(name):
    x0, y1 = b20_cell(name)
    return pa_at(T(name, 44), x0 + 0.25, y1 - 0.45)


def b20_dot(name):
    x0, y1 = b20_cell(name)
    return Dot([x0 + 1.95, y1 - 0.45, 0], radius=0.12, color=TERRA)


def b20_tag(name, word):
    x0, y1 = b20_cell(name)
    return pa_at(T(word, 34), x0 + 2.3, y1 - 0.45)


def b20_data(x, y, pale=False):
    return Square(side_length=0.26, fill_color=GHOST if pale else BOX_L, fill_opacity=1,
                  stroke_color=BAR3 if pale else PA_SMALL, stroke_width=2).move_to([x, y, 0])


def b20_sisd():
    cx, cy = b20_pic("SISD")
    return VGroup(Square(side_length=0.55, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([cx, cy + 0.25, 0]),
                  b20_data(cx, cy - 0.75))


def b20_simd():
    cx, cy = b20_pic("SIMD")
    body, light = gpu_block(Iso(cx - 0.55, cy - 0.2, 0.6))
    return VGroup(body, light, *[b20_data(cx + (k - 2.5) * 0.36, cy - 0.65) for k in range(6)])


def b20_misd():
    cx, cy = b20_pic("MISD")
    return VGroup(*[Square(side_length=0.5, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([cx + dx, cy + 0.25, 0]) for dx in (-0.7, 0, 0.7)],
                  b20_data(cx, cy - 0.75, pale=True))


def b20_mimd():
    cx, cy = b20_pic("MIMD")
    g = VGroup()
    for k in range(3):
        st, li = explorer_rack(Iso(cx - 1.2 + 1.15 * k, cy - 0.3, 0.36))
        g.add(st, li, b20_data(cx - 1.2 + 1.15 * k, cy - 0.7))
    return g


class B20_Flynn(Scene):
    def construct(self):
        self.add(pa_title("II · Flynn's Four Kinds"))
        until(self, "sorts machines")
        self.play(Create(b20_grid()), run_time=0.8)
        until(self, "Single or multiple instruction", lead=0.4)
        self.play(GrowArrow(b20_axis_x()), run_time=0.5)
        self.play(FadeIn(T("instruction", 36).move_to([0.7, 2.95, 0])),
                  FadeIn(T("single", 36).move_to([-1.25, 2.45, 0])), FadeIn(T("multiple", 36).move_to([2.65, 2.45, 0])), run_time=0.4)
        until(self, "single or multiple data", lead=0.4)
        self.play(GrowArrow(b20_axis_y()), run_time=0.5)
        self.play(FadeIn(T("data", 36).move_to([-5.5, -0.5, 0])),
                  FadeIn(T("single", 36).move_to([-4.3, 0.8, 0])), FadeIn(T("multiple", 36).move_to([-4.3, -1.8, 0])), run_time=0.4)
        until(self, "SISD is")
        self.play(FadeIn(b20_acr("SISD")), GrowFromCenter(b20_sisd()), run_time=0.5)
        until(self, "SIMD is")
        self.play(FadeIn(b20_acr("SIMD")), GrowFromCenter(b20_simd()), run_time=0.5)
        until(self, "that is a GPU", lead=0.2)
        self.play(FadeIn(b20_tag("SIMD", "GPU"), shift=LEFT * 0.2), run_time=0.3)
        until(self, "MISD is")
        self.play(FadeIn(b20_acr("MISD")), GrowFromCenter(b20_misd()), run_time=0.5)
        until(self, "MIMD is")
        self.play(FadeIn(b20_acr("MIMD")), run_time=0.3)
        pa_drop(self, [b20_mimd()], 0.6, dist=3.5)
        until(self, "a multi-node cluster", lead=0.2)
        self.play(FadeIn(b20_tag("MIMD", "cluster"), shift=LEFT * 0.2), run_time=0.3)
        until(self, "two are SIMD", lead=0.1)
        self.play(GrowFromCenter(b20_dot("SIMD")), run_time=0.3)
        until(self, "and MIMD, the cluster", lead=0.1)
        self.play(GrowFromCenter(b20_dot("MIMD")), run_time=0.3)
        done(self)


# ─────────────── B30 · shared memory (one node, one slab, OpenMP) vs distributed (three nodes, a belt, MPI), then hybrid ───────────────
B30_L = Iso(-3.8, -1.3, 0.65)                                        # the one shared-memory node, left
B30_R = [Iso(0.9 + 2.0 * k, -0.5, 0.5) for k in range(3)]            # three distributed nodes, right
B30_LPADS = (0.2, 1.0, 1.8, 2.6)                                     # x of the left node's four pads (size 0.6, at y 0.4)
B30_RPADS = (0.15, 1.05)                                             # x of each right node's two pads (size 0.6, at y 0.05)
B30_BELT_Y = -1.65


def b30_left_plinth():
    return pa_plinth(B30_L, -0.3, -0.3, 3.6, 2.8)


def b30_left_pads():
    return VGroup(*[pa_pad(B30_L, x, 0.4, 0.6) for x in B30_LPADS])


def b30_left_slab():
    return pa_slab(B30_L, 0.1, 1.8, 3.2, 0.6, 0.7)


def b30_left_cable_ends(x):
    return B30_L.p(x + 0.3, 1.0, 0.03), B30_L.p(x + 0.3, 1.8, 0.3)


def b30_left_cables():
    return VGroup(*[pa_cable(*b30_left_cable_ends(x)) for x in B30_LPADS])


def b30_right_node(k):
    iso = B30_R[k]
    return VGroup(pa_plinth(iso, -0.3, -0.3, 2.2, 2.2), *[pa_pad(iso, x, 0.05, 0.6) for x in B30_RPADS], pa_slab(iso, 0.1, 1.3, 1.6, 0.45, 0.6))


def b30_right_cables(k):
    iso = B30_R[k]
    return VGroup(*[pa_cable(iso.p(x + 0.3, 0.65, 0.03), iso.p(x + 0.3, 1.3, 0.3)) for x in B30_RPADS])


def b30_belt():
    return pa_belt(-0.1, 5.8, B30_BELT_Y)


def b30_belt_run(self, rt=0.7):
    """A packet rides the belt from the first node to the last and is gone."""
    rt = guard(self, rt)
    d = Dot([0.5, B30_BELT_Y + 0.15, 0], radius=0.1, color=TERRA)
    self.add(d)
    self.play(d.animate.move_to([5.3, B30_BELT_Y + 0.15, 0]), run_time=rt)
    self.remove(d)


class B30_SharedVsDistributed(Scene):
    def construct(self):
        self.add(pa_title("III · Shared Or Distributed"))
        self.play(GrowFromCenter(b30_left_plinth()), run_time=0.5)
        until(self, "Shared memory:", lead=0.3)
        self.play(FadeIn(T("shared memory", 40).move_to([-3.8, 2.0, 0])), run_time=0.35)
        until(self, "the cores of one node", lead=0.2)
        pads = b30_left_pads()
        self.play(LaggedStart(*[GrowFromCenter(p) for p in pads], lag_ratio=0.2), run_time=0.7)
        until(self, "one pool of RAM", lead=0.3)
        pa_slide_in(self, b30_left_slab(), DOWN * 4.5, 0.6)
        self.add(T("RAM", 34).move_to([-5.6, 0.6, 0]))
        until(self, "any core any address", lead=0.3)
        self.play(Create(b30_left_cables()), run_time=0.5)
        dots = VGroup(*[Dot(b30_left_cable_ends(x)[0], radius=0.09, color=TERRA).set_z_index(3) for x in B30_LPADS])
        self.add(dots)
        self.play(LaggedStart(*[d.animate.move_to(b30_left_cable_ends(x)[1]) for d, x in zip(dots, B30_LPADS)], lag_ratio=0.15), run_time=0.6)
        self.play(FadeOut(dots), run_time=0.2)
        self.remove(dots)
        until(self, "the tool is OpenMP", lead=0.2)
        self.play(FadeIn(T("OpenMP", 44).move_to([-3.8, -2.4, 0]), shift=UP * 0.2), run_time=0.35)
        until(self, "the limit is one machine", lead=0.2)
        self.play(Indicate(pads, color=None, scale_factor=1.08), run_time=0.6)
        until(self, "Distributed memory:", lead=0.3)
        nodes = [b30_right_node(k) for k in range(3)]
        self.play(FadeIn(T("distributed memory", 40).move_to([2.9, 2.0, 0])), run_time=0.3)
        pa_drop(self, nodes, 0.8, 0.25, dist=4.0)
        until(self, "node A", lead=0.2)
        self.play(Indicate(nodes[0], color=None, scale_factor=1.06), run_time=0.35)
        self.play(Indicate(nodes[1], color=None, scale_factor=1.06), run_time=0.35)
        until(self, "Programs send data", lead=0.3)
        self.play(GrowFromEdge(b30_belt(), LEFT), run_time=0.6)
        b30_belt_run(self, 0.7)
        until(self, "the tool is MPI", lead=0.2)
        self.play(FadeIn(T("MPI", 44).move_to([2.9, -2.4, 0]), shift=UP * 0.2), run_time=0.35)
        until(self, "scale across nodes", lead=0.2)
        self.play(Indicate(VGroup(*nodes), color=None, scale_factor=1.04), run_time=0.6)
        until(self, "hybrid", lead=0.3)
        self.play(FadeIn(T("hybrid", 44).move_to([-0.5, -2.9, 0]), shift=UP * 0.2), run_time=0.35)
        until(self, "MPI between nodes", lead=0.2)
        b30_belt_run(self, 0.6)
        until(self, "OpenMP inside each", lead=0.3)
        self.play(*[Create(b30_right_cables(k)) for k in range(3)], run_time=0.6)
        done(self)


# ─────────────── B31 · ntasks x cpus-per-task: 4 x 5, then 1 x 20 (OpenMP), then 20 x 1 (MPI), then back to 4 x 5 (hybrid) ───────────────
B31 = Iso(-3.2, -1.63, 0.75)                                         # one node, 20 pads in 4 rows x 5 columns
B31_PS, B31_PP, B31_M = 0.6, 0.95, 0.14                              # pad size, pad pitch, process-frame margin
B31_FLAG_X, B31_TXT_X = 0.9, 3.3                                     # mono flags (left edge) and the T column (centre)
B31_FLAG_Y = (2.5, 1.8)


def b31_plinth():
    return pa_plinth(B31, -0.35, -0.35, 5.1, 4.15)


def b31_pads():
    return VGroup(*[pa_pad(B31, c * B31_PP, r * B31_PP, B31_PS) for r in range(4) for c in range(5)])


def b31_frame(c0, c1, r0, r1):
    """A process frame spanning pads c0..c1 x r0..r1, deep kraft (a line inside the plinth's ink bbox is never ink)."""
    x0, y0 = c0 * B31_PP - B31_M, r0 * B31_PP - B31_M
    x1, y1 = c1 * B31_PP + B31_PS + B31_M, r1 * B31_PP + B31_PS + B31_M
    return Polygon(B31.p(x0, y0, 0.04), B31.p(x1, y0, 0.04), B31.p(x1, y1, 0.04), B31.p(x0, y1, 0.04),
                   stroke_color=PA_KRAFT, stroke_width=5, fill_opacity=0).set_z_index(2)


def b31_rank(c, r):
    """The rank dot on the first pad of a process."""
    return Dot(B31.p(c * B31_PP + B31_PS / 2, r * B31_PP + B31_PS / 2, 0.05), radius=0.1, color=TERRA).set_z_index(3)


def b31_arr(kind):
    """(frames, rank dots) for an arrangement."""
    if kind == "4x5":
        return VGroup(*[b31_frame(0, 4, r, r) for r in range(4)]), VGroup(*[b31_rank(0, r) for r in range(4)])
    if kind == "1x20":
        return VGroup(b31_frame(0, 4, 0, 3)), VGroup(b31_rank(0, 0))
    return (VGroup(*[b31_frame(c, c, r, r) for r in range(4) for c in range(5)]),
            VGroup(*[b31_rank(c, r) for r in range(4) for c in range(5)]))


def b31_flags(n, c):
    return VGroup(pa_at(M(f"--ntasks-per-node={n}", 32), B31_FLAG_X, B31_FLAG_Y[0]),
                  pa_at(M(f"--cpus-per-task={c}", 32), B31_FLAG_X, B31_FLAG_Y[1]))


def b31_product(s):
    return T(s, 52).move_to([B31_TXT_X, 0.5, 0])


def b31_tool(s):
    return T(s, 44).move_to([B31_TXT_X, -2.4, 0])


def b31_regroup(self, old, new, rt=0.7):
    """Swap (frames, dots, flags, product, tool) in one play; the plinth and the 20 pads never move."""
    rt = guard(self, rt)
    outs = [FadeOut(m) for m in old if m is not None]
    ins = [FadeIn(m) for m in new if m is not None]
    self.play(*outs, *ins, run_time=rt)
    for m in old:
        if m is not None:
            self.remove(m)


class B31_TasksTimesCpus(Scene):
    def construct(self):
        pa_slide_in(self, b31_plinth(), RIGHT * 7.5, 0.7)
        until(self, "n tasks is", lead=0.2)
        fr, dots = b31_arr("4x5")
        self.play(LaggedStart(*[Create(f) for f in fr], lag_ratio=0.2), run_time=0.8)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2), run_time=0.35)
        flags = b31_flags(4, 5)
        self.play(FadeIn(flags[0], shift=LEFT * 0.2), run_time=0.3)
        until(self, "CPUs per task is", lead=0.2)
        pads = b31_pads()
        self.play(LaggedStart(*[GrowFromCenter(p) for p in pads], lag_ratio=0.06), run_time=1.0)
        self.play(FadeIn(flags[1], shift=LEFT * 0.2), run_time=0.3)
        until(self, "They multiply", lead=0.2)
        prod = b31_product("4 × 5")
        self.play(FadeIn(prod, shift=UP * 0.2), run_time=0.35)
        until(self, "is twenty cores", lead=0.2)
        self.play(FadeIn(T("20", 100).move_to([B31_TXT_X, -0.9, 0]), scale=0.7), run_time=0.45)
        until(self, "Pure OpenMP", lead=0.3)
        fr2, dots2 = b31_arr("1x20")
        flags2, prod2, tool2 = b31_flags(1, 20), b31_product("1 × 20"), b31_tool("OpenMP")
        b31_regroup(self, (fr, dots, flags, prod, None), (fr2, dots2, flags2, prod2, tool2), 0.7)
        until(self, "Pure MPI", lead=0.3)
        fr3, dots3 = b31_arr("20x1")
        flags3, prod3, tool3 = b31_flags(20, 1), b31_product("20 × 1"), b31_tool("MPI")
        b31_regroup(self, (fr2, dots2, flags2, prod2, tool2), (fr3, dots3, flags3, prod3, tool3), 0.7)
        until(self, "Hybrid sits", lead=0.3)
        fr4, dots4 = b31_arr("4x5")
        flags4, prod4, tool4 = b31_flags(4, 5), b31_product("4 × 5"), b31_tool("hybrid")
        b31_regroup(self, (fr3, dots3, flags3, prod3, tool3), (fr4, dots4, flags4, prod4, tool4), 0.6)
        done(self)


# ─────────────── B50 · the Game of Life: a glider steps twice, eight neighbours, row by row, then four bands at once ───────────────
B50_C, B50_R, B50_P, B50_S = 12, 8, 0.52, 0.42                       # columns, rows, pitch, cell side (gaps keep the grid from fusing)
B50_X0, B50_Y0 = -5.7, 1.3                                           # centre of cell (0, 0), top-left
B50_LIVE, B50_DEAD = DARK_TOP, PA_PAD
B50_GLIDER = ((2, 1), (3, 2), (1, 3), (2, 3), (3, 3))                # (col, row) of the glider's five cells at generation 0
B50_RING = (6, 4)                                                    # the cell whose eight neighbours get ringed
B50_LAB_X = 3.3


def b50_xy(c, r):
    return np.array([B50_X0 + c * B50_P, B50_Y0 - r * B50_P, 0.0])


def b50_cells():
    """All cells, dead; a list of rows, each a VGroup of Squares."""
    return [VGroup(*[Square(side_length=B50_S, fill_color=B50_DEAD, fill_opacity=1, stroke_width=0).move_to(b50_xy(c, r)) for c in range(B50_C)])
            for r in range(B50_R)]


def b50_step(live):
    """One Life generation on the bounded grid: a set of (col, row)."""
    counts = {}
    for c, r in live:
        for dc in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if dc or dr:
                    counts[(c + dc, r + dr)] = counts.get((c + dc, r + dr), 0) + 1
    return {p for p, n in counts.items() if (n == 3 or (n == 2 and p in live)) and 0 <= p[0] < B50_C and 0 <= p[1] < B50_R}


def b50_gens(n):
    g, out = set(B50_GLIDER), []
    for _ in range(n + 1):
        out.append(g)
        g = b50_step(g)
    return out


def b50_apply(self, rows, old, new, rt):
    """Recolour only the cells that change between two generations."""
    anims = [rows[r][c].animate.set_color(B50_LIVE) for c, r in new - old] + [rows[r][c].animate.set_color(B50_DEAD) for c, r in old - new]
    if anims:
        self.play(*anims, run_time=rt)


def b50_ring():
    return Square(side_length=3 * B50_P - 0.1, stroke_color=PA_KRAFT, stroke_width=5, fill_opacity=0).move_to(b50_xy(*B50_RING))


def b50_neigh(rows):
    c0, r0 = B50_RING
    return [rows[r0 + dr][c0 + dc] for dc in (-1, 0, 1) for dr in (-1, 0, 1) if dc or dr]


def b50_bar(r):
    """The core's cursor, parked at the left of row r."""
    return Rectangle(width=0.14, height=B50_S + 0.06, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to(b50_xy(0, r) + LEFT * (B50_P / 2 + 0.1))


def b50_band_lines():
    x0, x1 = B50_X0 - B50_P / 2, B50_X0 + (B50_C - 0.5) * B50_P
    return VGroup(*[Line([x0, B50_Y0 - (r + 0.5) * B50_P, 0], [x1, B50_Y0 - (r + 0.5) * B50_P, 0], color=PA_KRAFT, stroke_width=4) for r in (1, 3, 5)])


def b50_sweep(self, bars, starts, rows_each, rt):
    """Each bar sweeps its rows left to right, one row after another, all bars at once (one play, any frame rate)."""
    rt = guard(self, rt)
    x0, span = B50_X0 - B50_P / 2 - 0.1, B50_C * B50_P + 0.2
    holder = VGroup(*bars)

    def upd(m, a):
        t = min(a * rows_each, rows_each - 1e-6)
        k, f = int(t), t - int(t)
        for b, r0 in zip(bars, starts):
            b.move_to([x0 + f * span, B50_Y0 - (r0 + k) * B50_P, 0])

    self.play(UpdateFromAlphaFunc(holder, upd), run_time=rt, rate_func=linear)
    upd(holder, 1.0)


class B50_GameOfLife(Scene):
    def construct(self):
        self.add(pa_title("V · The Game Of Life"))
        rows = b50_cells()
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.1), run_time=0.7)
        gens = b50_gens(2)
        until(self, "Conway", lead=0.1)
        b50_apply(self, rows, set(), gens[0], 0.4)                                            # the glider
        until(self, "a grid where", lead=0.2)
        b50_apply(self, rows, gens[0], gens[1], 0.5)                                          # step one
        until(self, "next state depends", lead=0.2)
        b50_apply(self, rows, gens[1], gens[2], 0.5)                                          # step two
        until(self, "eight neighbours", lead=0.4)
        ring, neigh = b50_ring(), b50_neigh(rows)
        mark = Dot(b50_xy(*B50_RING), radius=0.09, color=TERRA)
        self.play(Create(ring), *[n.animate.set_color(BAR2) for n in neigh], GrowFromCenter(mark), run_time=0.5)
        lab8 = T("eight neighbours", 40).move_to([B50_LAB_X, b50_xy(*B50_RING)[1], 0])
        self.play(FadeIn(lab8), run_time=0.3)
        until(self, "embarrassingly parallel", lead=0.2)
        self.play(Indicate(ring, color=None, scale_factor=1.08), run_time=0.5)
        until(self, "every cell is independent", lead=0.2)
        self.play(FadeOut(ring), FadeOut(mark), FadeOut(lab8), *[n.animate.set_color(B50_DEAD) for n in neigh], run_time=0.4)
        self.remove(ring, mark, lab8)
        until(self, "A single core", lead=0.25)
        bar = b50_bar(0)
        self.add(bar)
        self.play(FadeIn(T("serial", 40).move_to([B50_LAB_X, 0.3, 0])), run_time=0.25)
        b50_sweep(self, [bar], [0], B50_R, 1.6)                                               # one core, row by row
        self.play(FadeOut(bar), run_time=0.15)
        self.remove(bar)
        until(self, "Many cores", lead=0.25)
        self.play(Create(b50_band_lines()), run_time=0.3)                                     # the rows split into four bands
        bars = [b50_bar(2 * k) for k in range(4)]
        self.add(*bars)
        self.play(FadeIn(T("parallel", 40).move_to([B50_LAB_X, -1.4, 0])), run_time=0.25)
        b50_sweep(self, bars, [0, 2, 4, 6], 2, 0.8)                                           # four cores, the bands at once
        done(self)

# ═════════════════════════════ PART B · B40 B41 (Act IV) · B53 B55 (Act V) · B73 (Act VII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB_ / pb_ / b4x_ / b5x_ / b7x_ so the parts never collide.
# Charts: axes in BAR1, curves in INK (labels placed clear of them), dashed ideals in INK,
# terracotta only as dots and rings. Every number on screen is in the beat's narration or visual_intent.

PB_SMALL = "#917A55"      # dark kraft: outlines of SMALL objects only


def pb_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb_axes(x0, y0, x1, y1):
    """Plain chart axes in dim grey (ink curves sit on them without fusing)."""
    return VGroup(Line([x0, y0, 0], [x1 + 0.15, y0, 0], color=BAR1, stroke_width=4),
                  Line([x0, y0, 0], [x0, y1 + 0.15, 0], color=BAR1, stroke_width=4))


def pb_dashed(p0, p1):
    return DashedLine([p0[0], p0[1], 0], [p1[0], p1[1], 0], color=INK, stroke_width=4, dash_length=0.14)


def pb_curve(pts, color=INK, sw=7):
    c = VMobject(color=color, stroke_width=sw)
    c.set_points_smoothly([np.array([p[0], p[1], 0.0]) for p in pts])
    return c


def pb_vbracket(x, y0, y1, tick=0.15):
    """A vertical bracket at x spanning y0..y1, ticks pointing left."""
    return VGroup(Line([x, y0, 0], [x, y1, 0], color=INK, stroke_width=4),
                  Line([x, y0, 0], [x - tick, y0, 0], color=INK, stroke_width=4),
                  Line([x, y1, 0], [x - tick, y1, 0], color=INK, stroke_width=4))


def pb_hbracket(x0, x1, y, tick=0.2):
    """A horizontal bracket above two bars, ticks pointing down."""
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=INK, stroke_width=4),
                  Line([x0, y, 0], [x0, y - tick, 0], color=INK, stroke_width=4),
                  Line([x1, y, 0], [x1, y - tick, 0], color=INK, stroke_width=4))


# ─────────────── B40 / B41 shared chart frame: processors N (1…64) along x ───────────────
B4_X0, B4_X1, B4_Y0 = -5.5, 0.7, -2.5
B4_SX = (B4_X1 - B4_X0) / 64.0


def b4_x(n):
    return B4_X0 + n * B4_SX


def b4_amdahl(n, s=0.1):
    return 1.0 / (s + (1.0 - s) / n)


def b4_gustafson(n, s=0.1):
    return s + (1.0 - s) * n


# ─────────────── B40 · Amdahl: the formula, the S = 0.1 curve bending toward a ceiling at 10× ───────────────
B40_SY = 0.38                                   # speedup axis 0…12
B40_STRIP_X0, B40_STRIP_Y = 2.75, -0.6


def b40_y(s):
    return B4_Y0 + s * B40_SY


def b40_seg(k, fill):
    return Rectangle(width=0.24, height=0.45, fill_color=fill, fill_opacity=1, stroke_width=0).move_to(
        [B40_STRIP_X0 + 0.12 + k * 0.27, B40_STRIP_Y, 0])


class B40_Amdahl(Scene):
    def construct(self):
        procs = T("processors N", 34).move_to([-2.4, -2.9, 0])
        self.add(pb_title("IV · The Speed Limit"), pb_axes(B4_X0, B4_Y0, B4_X1, b40_y(12)),
                 T("1", 32).move_to([b4_x(1), -2.85, 0]), T("64", 32).move_to([b4_x(64), -2.85, 0]),
                 procs, T("speedup", 34).move_to([-5.0, 2.45, 0]))
        ideal = pb_dashed((b4_x(1), b40_y(1)), (b4_x(12), b40_y(12)))
        self.play(Create(ideal), FadeIn(T("ideal", 34).move_to([-3.6, 1.95, 0])), run_time=0.6)
        # not everything parallelises: ten segments, one of them serial
        until(self, "Not everything parallelises", lead=0.1)
        segs = [b40_seg(k, BAR2) for k in range(10)]
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in segs], lag_ratio=0.08), run_time=0.7)
        until(self, "reading data", lead=0.2)
        serial = b40_seg(0, INK)
        self.play(FadeIn(serial), FadeIn(T("serial", 32).move_to([2.87, -1.15, 0])),
                  FadeIn(T("parallel", 32).move_to([4.4, -1.15, 0])), run_time=0.4)
        # the law
        until(self, "Amdahl's law", lead=0.2)
        formula = MathTex(r"\text{Speedup} = \frac{1}{S + \frac{P}{N}}", font_size=56, color=INK).move_to([3.5, 2.2, 0])
        self.play(FadeIn(formula, shift=DOWN * 0.15), run_time=0.6)
        until(self, "where S is the serial", lead=0.2)
        self.play(Indicate(serial, color=None, scale_factor=1.25), run_time=0.5)
        until(self, "P the parallel", lead=0.2)
        self.play(FadeIn(MathTex(r"P = 1 - S", font_size=60, color=INK).move_to([4.1, 0.4, 0])),
                  Indicate(VGroup(*segs[1:]), color=None, scale_factor=1.08), run_time=0.5)
        until(self, "and N the number", lead=0.2)
        self.play(Indicate(procs, color=None, scale_factor=1.08), run_time=0.5)
        # S = 0.1: the curve climbs, then flattens toward 10
        until(self, "If ten percent", lead=0.1)
        curve = pb_curve([(b4_x(n), b40_y(b4_amdahl(n))) for n in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64)])
        self.play(Create(curve), run_time=1.5)
        self.play(FadeIn(T("S = 0.1", 34).move_to([-0.6, 0.0, 0])), run_time=0.3)
        until(self, "the most you can ever get", lead=0.2)
        ceiling = pb_dashed((B4_X0, b40_y(10)), (B4_X1, b40_y(10)))
        self.play(Create(ceiling), run_time=0.6)
        self.play(FadeIn(T("10× at most", 34).move_to([1.95, b40_y(10), 0])), run_time=0.3)
        until(self, "however many processors", lead=0.2)
        self.play(GrowFromCenter(Dot([b4_x(64), b40_y(b4_amdahl(64)), 0], radius=0.12, color=TERRA).set_z_index(3)), run_time=0.3)
        until(self, "The curve climbs", lead=0.2)
        rider = Dot([b4_x(1), b40_y(1), 0], radius=0.12, color=TERRA).set_z_index(3)
        self.add(rider)
        self.play(MoveAlongPath(rider, curve), run_time=1.4)
        self.play(FadeOut(rider), run_time=0.2)
        until(self, "This is strong scaling", lead=0.2)
        self.play(FadeIn(T("strong scaling", 34).move_to([-1.6, -1.5, 0]), shift=UP * 0.15), run_time=0.4)
        done(self)


# ─────────────── B41 · Gustafson: the problem grows with the cores; a near-straight line beside the flattening curve ───────────────
B41_SY = 4.4 / 64.0                             # speedup axis 0…64
B41_CLOCK = np.array([2.9, 1.3, 0.0])
B41_BLOCK = np.array([4.1, -0.5, 0.0])


def b41_y(s):
    return B4_Y0 + s * B41_SY


def b41_clock():
    face = Circle(radius=0.5, color=INK, stroke_width=5).move_to(B41_CLOCK)
    hands = VGroup(Line(B41_CLOCK, B41_CLOCK + np.array([0.0, 0.34, 0.0]), color=BAR1, stroke_width=5),
                   Line(B41_CLOCK, B41_CLOCK + np.array([0.24, 0.0, 0.0]), color=BAR1, stroke_width=5))
    return VGroup(face, hands)


def b41_page():
    slab = Rectangle(width=1.5, height=1.9, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.2, -0.3, 0])
    lines = VGroup(*[Line([2.6, y, 0], [3.8, y, 0], color=GHOST, stroke_width=4) for y in (0.3, -0.1, -0.5, -0.9)])
    return VGroup(slab, lines)


class B41_Gustafson(Scene):
    def construct(self):
        self.add(pb_axes(B4_X0, B4_Y0, B4_X1, b41_y(64)),
                 T("1", 32).move_to([b4_x(1), -2.85, 0]), T("64", 32).move_to([b4_x(64), -2.85, 0]),
                 T("processors N", 34).move_to([-2.4, -2.9, 0]), T("speedup", 34).move_to([-5.0, 2.45, 0]))
        amdahl = pb_curve([(b4_x(n), b41_y(b4_amdahl(n))) for n in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64)], BAR1, 6)
        ideal = pb_dashed((b4_x(1), b41_y(1)), (b4_x(64), b41_y(64)))
        self.play(Create(amdahl), Create(ideal), run_time=0.7)
        self.play(FadeIn(T("Amdahl", 34).move_to([-0.1, -1.4, 0])), FadeIn(T("ideal", 34).move_to([-0.6, 2.2, 0])), run_time=0.3)
        # the other question: a block of work, a clock that holds at ten minutes
        until(self, "A researcher", lead=0.2)
        block = Square(side_length=0.35, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(B41_BLOCK)
        self.play(GrowFromCenter(block), run_time=0.4)
        until(self, "ten-minute problem", lead=0.3)
        clock = b41_clock()
        tenmin = T("10 min", 34).move_to([4.3, 1.3, 0])
        self.play(Create(clock), FadeIn(tenmin), run_time=0.5)
        until(self, "They solve a problem", lead=0.2)
        self.play(block.animate.scale(4.57), run_time=1.2)
        cores = T("100 cores", 34).move_to([4.1, -1.75, 0])
        bigger = T("100× the problem", 34).move_to([4.1, -2.25, 0])
        self.play(FadeIn(cores), FadeIn(bigger), run_time=0.4)
        until(self, "in the same ten minutes", lead=0.2)
        pin = Dot(B41_CLOCK, radius=0.08, color=TERRA).set_z_index(3)
        self.play(GrowFromCenter(pin), Indicate(tenmin, color=None, scale_factor=1.1), run_time=0.5)
        # the law and its line
        until(self, "Speedup equals S plus P times N", lead=0.2)
        formula = MathTex(r"\text{Speedup} = S + P \cdot N", font_size=56, color=INK).move_to([3.4, 2.7, 0])
        self.play(FadeIn(formula, shift=DOWN * 0.15), run_time=0.5)
        line = Line([b4_x(1), b41_y(b4_gustafson(1)), 0], [b4_x(64), b41_y(b4_gustafson(64)), 0], color=INK, stroke_width=7)
        self.play(Create(line), run_time=1.2)
        self.play(GrowFromCenter(Dot([b4_x(64), b41_y(b4_gustafson(64)), 0], radius=0.12, color=TERRA).set_z_index(3)), run_time=0.3)
        until(self, "That is weak scaling", lead=0.2)
        self.play(FadeIn(T("weak scaling", 34).move_to([-2.4, 1.5, 0]), shift=UP * 0.15), run_time=0.4)
        until(self, "Both laws are right", lead=0.2)
        self.play(Indicate(VGroup(amdahl, line), color=None, scale_factor=1.02), run_time=0.6)
        # plan first: the page replaces the clock and the block
        until(self, "One tip before any code", lead=0.2)
        page = b41_page()
        self.play(FadeOut(VGroup(clock, tenmin, pin, block, cores, bigger)), FadeIn(page, shift=UP * 0.2), run_time=0.6)
        until(self, "plan what can be parallel", lead=0.2)
        self.play(Create(check(4.5, -0.1, 0.24)), run_time=0.4)
        self.play(FadeIn(T("plan what can be parallel", 32).move_to([3.9, -1.75, 0])), run_time=0.3)
        until(self, "Retrofitting", lead=0.2)
        self.play(Indicate(page, color=None, scale_factor=1.04), run_time=0.5)
        done(self)


# ─────────────── B53 · halo exchange: one grid into four strips on four node plinths, boundary rows swap ───────────────
B53_CELL = 0.26
B53_COLS, B53_ROWS = 14, 12
B53_GX, B53_GY = -2.4, 0.0                      # grid centre
B53_W = B53_COLS * B53_CELL                     # 3.64
B53_STRIP_Y = (2.61, 0.87, -0.87, -2.61)         # strip centres after the split
B53_GHOST = 0.64                                # ghost row offset from its strip centre


def b53_cell_xy(c, r):
    return (B53_GX - B53_W / 2 + B53_CELL / 2 + c * B53_CELL, B53_GY + B53_ROWS * B53_CELL / 2 - B53_CELL / 2 - r * B53_CELL)


def b53_cell(c, r, fill=BAR2):
    x, y = b53_cell_xy(c, r)
    return Square(side_length=B53_CELL, fill_color=fill, fill_opacity=1, stroke_color=CARD, stroke_width=1.5).move_to([x, y, 0])


def b53_row(r, fill=BAR2):
    return VGroup(*[b53_cell(c, r, fill) for c in range(B53_COLS)])


def b53_plinth(k):
    return Rectangle(width=B53_W + 0.3, height=3 * B53_CELL + 0.18, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to(
        [B53_GX, B53_STRIP_Y[k], 0]).set_z_index(-1)


def b53_ghost_outline(y):
    return DashedVMobject(Rectangle(width=B53_W, height=B53_CELL).move_to([B53_GX, y, 0]), num_dashes=44).set_stroke(INK, 3)


class B53_HaloExchange(Scene):
    def construct(self):
        strips = [VGroup(*[b53_row(r) for r in range(3 * k, 3 * k + 3)]) for k in range(4)]
        self.play(FadeIn(VGroup(*strips)), run_time=0.6)
        until(self, "domain decomposition", lead=0.2)
        self.play(FadeIn(T("domain decomposition", 34).move_to([3.8, 3.0, 0]), shift=DOWN * 0.15), run_time=0.4)
        # the cut: four strips slide apart onto four node plinths
        until(self, "The grid is cut", lead=0.2)
        shifts = [B53_STRIP_Y[k] - (1.17 - 0.78 * k) for k in range(4)]
        self.play(*[s.animate.shift(UP * dy) for s, dy in zip(strips, shifts)], run_time=1.0)
        plinths = [b53_plinth(k) for k in range(4)]
        self.play(*[FadeIn(p) for p in plinths], run_time=0.4)
        until(self, "one per MPI rank", lead=0.2)
        self.play(*[FadeIn(T(f"rank {k}", 34).move_to([0.6, B53_STRIP_Y[k], 0])) for k in range(4)], run_time=0.4)
        # the edge needs the neighbour: boundary rows light up, two cells across a gap
        until(self, "But a cell on the edge", lead=0.2)
        edges = [strips[k][i] for k in range(4) for i in (0, 2)]
        self.play(*[e.animate.set_fill(CARD) for e in edges], run_time=0.5)
        until(self, "needs neighbours", lead=0.1)
        x6, _ = b53_cell_xy(6, 0)
        self.play(GrowFromCenter(Dot([x6, B53_STRIP_Y[1] + B53_CELL, 0], radius=0.09, color=TERRA).set_z_index(3)),
                  GrowFromCenter(Dot([x6, B53_STRIP_Y[0] - B53_CELL, 0], radius=0.09, color=TERRA).set_z_index(3)), run_time=0.3)
        # the swap: copies of the boundary rows cross the gaps and land as ghost rows
        until(self, "the ranks swap", lead=0.3)
        copies, moves, outlines = [], [], []
        for k in range(3):
            down = strips[k][2].copy().set_fill(BAR2).set_z_index(1)          # strip k's bottom row -> above strip k+1
            up = strips[k + 1][0].copy().set_fill(BAR2).set_z_index(1)        # strip k+1's top row -> below strip k
            y_down, y_up = B53_STRIP_Y[k + 1] + B53_GHOST, B53_STRIP_Y[k] - B53_GHOST
            copies += [down, up]
            moves += [down.animate.move_to([B53_GX, y_down, 0]), up.animate.move_to([B53_GX, y_up, 0])]
            outlines += [b53_ghost_outline(y_down), b53_ghost_outline(y_up)]
        self.add(*copies)
        self.play(*moves, run_time=0.9)
        self.play(*[Create(o) for o in outlines], run_time=0.4)
        until(self, "MPI send and receive", lead=0.3)
        self.play(FadeIn(M("MPI_Send / MPI_Recv", 32).move_to([3.6, 0.0, 0]), shift=UP * 0.15), run_time=0.4)
        until(self, "Those borrowed rows are the halo", lead=0.2)
        self.play(FadeIn(T("halo", 34).move_to([0.55, B53_STRIP_Y[0] - B53_GHOST, 0])),
                  Indicate(VGroup(*copies), color=None, scale_factor=1.03), run_time=0.6)
        done(self)


# ─────────────── B55 · the real numbers: ten points, grey OpenMP and dark MPI, under a dashed ideal ───────────────
B55_X0, B55_X1, B55_Y0 = -5.3, 0.9, -2.5
B55_SX = (B55_X1 - B55_X0) / np.sqrt(80.0)       # both axes stretched by sqrt so 1…20 stays readable; the ideal stays a diagonal
B55_SY = 4.6 / np.sqrt(80.0)
B55_DATA = ((1, 1.0, "250.7 s", "1 core"), (2, 2.2, "116.8 s", "2 cores"), (4, 4.3, "58.1 s", "4 cores"), (8, 8.5, "29.4 s", "8 cores"),
            (12, 7.5, "33.4 s", "12 cores"), (16, 10.0, "25.2 s", "16 cores"), (20, 12.4, "20.2 s", "20 cores"),
            (40, 25.1, "10.0 s", "40 cores"), (60, 36.9, "6.8 s", "60 cores"), (80, 44.0, "5.7 s", "80 cores"))
B55_CUES = ("Serial:", "OpenMP on two cores", "Four cores", "Eight,", "Twelve,", "Sixteen,", "Twenty,", "forty cores", "Sixty,", "Eighty,")
B55_COL_X = 4.7


def b55_x(c):
    return B55_X0 + B55_SX * np.sqrt(c)


def b55_y(s):
    return B55_Y0 + B55_SY * np.sqrt(s)


def b55_pt(i):
    c, s = B55_DATA[i][0], B55_DATA[i][1]
    return np.array([b55_x(c), b55_y(s), 0.0])


def b55_column(i):
    """The wall-time column: cores, the measured time, the speedup."""
    c, s, wall, cores = B55_DATA[i]
    return VGroup(T(cores, 34).move_to([B55_COL_X, 1.9, 0]), M(wall, 44).move_to([B55_COL_X, 1.1, 0]),
                  T(f"{s:.1f}×", 40).move_to([B55_COL_X, 0.2, 0]))


class B55_Benchmark(Scene):
    def construct(self):
        self.add(pb_axes(B55_X0, B55_Y0, B55_X1, b55_y(80)),
                 T("1", 32).move_to([b55_x(1), -2.85, 0]), T("20", 32).move_to([b55_x(20), -2.85, 0]),
                 T("40", 32).move_to([b55_x(40), -2.85, 0]), T("80", 32).move_to([b55_x(80), -2.85, 0]),
                 T("cores", 34).move_to([-3.5, -2.9, 0]), T("speedup", 34).move_to([-4.8, 2.5, 0]),
                 T("10×", 32).move_to([-5.75, b55_y(10), 0]), T("80×", 32).move_to([-5.75, b55_y(80), 0]))
        ideal = pb_dashed((b55_x(1), b55_y(1)), (b55_x(80), b55_y(80)))
        self.play(Create(ideal), FadeIn(T("ideal", 34).move_to([-0.9, 1.6, 0])), run_time=0.6)
        until(self, "five hundred iterations", lead=0.2)
        self.play(FadeIn(T("500 iterations", 32).move_to([-4.3, 2.95, 0])), run_time=0.3)
        legend = VGroup(Dot([3.7, -1.2, 0], radius=0.11, color=BAR1), T("OpenMP", 34).move_to([4.75, -1.2, 0]))
        dots, col = [], None
        for i, cue in enumerate(B55_CUES):
            until(self, cue, lead=0.15)
            p = b55_pt(i)
            dot = Dot(p, radius=0.11, color=BAR1 if i < 7 else INK).set_z_index(3)
            dots.append(dot)
            anims = [GrowFromCenter(dot)]
            if i > 0:
                anims.append(Create(Line(b55_pt(i - 1), p, color=INK, stroke_width=5)))
            newcol = b55_column(i)
            if col is not None:
                anims.append(FadeOut(col))
            anims.append(FadeIn(newcol))
            if i == 0:
                anims.append(FadeIn(legend))
            if i == 7:
                anims.append(FadeIn(VGroup(Dot([3.7, -1.8, 0], radius=0.11, color=INK), T("MPI", 34).move_to([4.45, -1.8, 0]))))
            self.play(*anims, run_time=0.35)
            col = newcol
            if i == 4:
                until(self, "slower than eight", lead=0.2)
                self.play(GrowFromCenter(Circle(radius=0.24, color=TERRA, stroke_width=5).move_to(p)), run_time=0.3)
        until(self, "Inside one node", lead=0.2)
        self.play(Indicate(VGroup(*dots[:7]), color=None, scale_factor=1.15), run_time=0.6)
        until(self, "Across nodes the communication", lead=0.2)
        self.play(Indicate(VGroup(*dots[7:]), color=None, scale_factor=1.15), run_time=0.6)
        until(self, "bends under the ideal line", lead=0.3)
        self.play(Create(pb_vbracket(1.3, b55_y(44.0) + 0.04, b55_y(80) - 0.04)), run_time=0.5)
        self.play(FadeIn(T("communication", 34).move_to([2.65, 2.4, 0])), run_time=0.3)
        until(self, "exactly as Amdahl", lead=0.2)
        self.play(GrowFromCenter(Dot(b55_pt(9), radius=0.13, color=TERRA).set_z_index(4)), run_time=0.3)
        done(self)


# ─────────────── B73 · the GPU benchmark: three bars, three wall times, sync beats maths across nodes ───────────────
B73_BASE = -1.9
B73_BX = (-4.05, -1.15, 1.75)
B73_SEC = 0.29                                  # bar height per second
B73_TIMES = (11.73, 5.48, 5.08)
B73_WALL = ("11.73 s", "5.48 s", "5.08 s")
B73_SPEED = ("1.0×", "2.1×", "2.3×")
B73_UNDER = (("1 GPU",), ("2 GPUs", "1 node"), ("4 GPUs", "2 nodes"))
B73_PIVOT = np.array([3.9, -0.3, 0.0])
B73_PAN_L, B73_PAN_R, B73_PAN_Y = 3.1, 4.7, -0.95


def b73_bar(i):
    h = B73_TIMES[i] * B73_SEC
    return Rectangle(width=1.2, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B73_BX[i], B73_BASE + h / 2, 0])


def b73_top(i):
    return B73_BASE + B73_TIMES[i] * B73_SEC


def b73_under(i):
    return VGroup(*[T(s, 32).move_to([B73_BX[i], -2.3 - 0.45 * j, 0]) for j, s in enumerate(B73_UNDER[i])])


def b73_scale():
    """A small balance: ink beam on an ink fulcrum, grey strings, ink pans, one grey weight on each pan."""
    fulcrum = Polygon([B73_PIVOT[0] - 0.25, -0.9, 0], [B73_PIVOT[0] + 0.25, -0.9, 0], [B73_PIVOT[0], -0.37, 0],
                      fill_color=INK, fill_opacity=1, stroke_width=0)
    beam = Line([B73_PAN_L, B73_PIVOT[1], 0], [B73_PAN_R, B73_PIVOT[1], 0], color=INK, stroke_width=5)
    strings = VGroup(*[Line([x, B73_PIVOT[1], 0], [x, B73_PAN_Y, 0], color=BAR1, stroke_width=4) for x in (B73_PAN_L, B73_PAN_R)])
    pans = VGroup(*[Line([x - 0.3, B73_PAN_Y, 0], [x + 0.3, B73_PAN_Y, 0], color=INK, stroke_width=5) for x in (B73_PAN_L, B73_PAN_R)])
    w_l = Square(side_length=0.28, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B73_PAN_L, B73_PAN_Y + 0.17, 0])
    w_r = Square(side_length=0.28, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B73_PAN_R, B73_PAN_Y + 0.17, 0])
    return fulcrum, VGroup(beam, strings, pans, w_l), w_r


class B73_GpuBench(Scene):
    def construct(self):
        fulcrum, arm, w_r = b73_scale()
        self.play(Create(Line([-4.9, B73_BASE, 0], [2.6, B73_BASE, 0], color=BAR1, stroke_width=4)),
                  FadeIn(VGroup(fulcrum, arm, w_r)), run_time=0.6)
        self.play(FadeIn(T("compute", 32).move_to([B73_PAN_L, -1.45, 0])), FadeIn(T("communication", 32).move_to([B73_PAN_R, -1.9, 0])), run_time=0.3)
        until(self, "a four-thousand-square matmul", lead=0.2)
        self.play(FadeIn(T("4000 × 4000 · 100 times", 32).move_to([-3.0, 2.95, 0]), shift=DOWN * 0.15), run_time=0.4)
        bars, walls, speeds = [], [], []
        for i, (cue_bar, cue_wall, cue_speed) in enumerate((("One GPU", "eleven point seven", None),
                                                             ("Two GPUs on one node", "five and a half seconds", "two point one times"),
                                                             ("Four GPUs across two nodes", "five point one seconds", "only two point three"))):
            until(self, cue_bar, lead=0.2)
            bars.append(b73_bar(i))
            self.play(GrowFromEdge(bars[i], DOWN), FadeIn(b73_under(i)), run_time=0.6)
            until(self, cue_wall, lead=0.15)
            walls.append(M(B73_WALL[i], 36).move_to([B73_BX[i], b73_top(i) + 0.33, 0]))
            speeds.append(T(B73_SPEED[i], 36).move_to([B73_BX[i], b73_top(i) + 0.78, 0]))
            if cue_speed is None:
                self.play(FadeIn(walls[i]), FadeIn(speeds[i]), run_time=0.3)
            else:
                self.play(FadeIn(walls[i]), run_time=0.3)
                until(self, cue_speed, lead=0.15)
                self.play(FadeIn(speeds[i]), run_time=0.3)
            if i == 1:
                until(self, "near linear", lead=0.2)
                self.play(Indicate(speeds[1], color=None, scale_factor=1.2), run_time=0.5)
        # tiny shards, then sync beats maths: the bracket and the tilt
        until(self, "each GPU gets a tiny shard", lead=0.2)
        shards = VGroup(*[Square(side_length=0.2, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([1.35 + 0.27 * j, 0.72, 0]) for j in range(4)])
        self.play(LaggedStart(*[GrowFromCenter(s) for s in shards], lag_ratio=0.2), run_time=0.5)
        until(self, "sync costs more than the maths", lead=0.3)
        self.play(Create(pb_hbracket(B73_BX[1], B73_BX[2], 1.3)), run_time=0.5)
        self.play(FadeIn(T("sync > maths", 34).move_to([0.3, 1.75, 0])), run_time=0.3)
        self.play(w_r.animate.scale(1.6).shift(UP * 0.08), run_time=0.4)
        self.play(Rotate(VGroup(arm, w_r), angle=-10 * DEGREES, about_point=B73_PIVOT), run_time=0.7)
        until(self, "ratio decides", lead=0.2)
        self.play(Indicate(VGroup(arm, w_r, fulcrum), color=None, scale_factor=1.04), run_time=0.6)
        done(self)
# ═════════════════════════════ PART C · B60 B61 (Act VI) · B83 (Act VIII) · B90 (Act IX) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PC_ / pc_ / b60_ / b61_ / b83_ / b90_ so the parts never collide.
#
# Stage map. Act VI opens on the CPU-against-GPU table (film 4's B20 blocks as the column heads: a grey CPU
# block with four large cores, a dark GPU block whose grey core grid fills), then B61 is the four CUDA steps in
# isometric: grey host block left, dark device block (the cast's gpu_block) right, a kraft cable between them,
# data boxes riding it both ways, sparks on the device's top face. Act VIII opens on the eight-row tool table
# (mono tool · memory icon + word · best for). Act IX is the four-row checklist (film 4's B80 grammar).
PC_KRAFT = "#9C8462"                        # deep-kraft connector (lines are never ink: ink lines fuse the things they join)
PC_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T: small ink rings fuse)
PC_PAD = "#E4E0D4"                          # pads and belts stay within 28 of the stage (Gate V does not count them as ink)
PC_CPU_TOP, PC_CPU_L, PC_CPU_R = "#C9CBCF", "#B4AFA6", "#8B8F96"   # the grey CPU block's faces (host)


def pc_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pc_left(mob, x, y):
    """Left-align a text at x, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pc_drop(self, mobs, rt=0.5, lag=0.2, dist=4.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *list(with_), run_time=rt, rate_func=ease_in)


def pc_slab(x, y, w=0.7, h=0.32):
    """One node: a flat grey slab (shared memory lives on one node). Left edge at x."""
    return VGroup(Rectangle(width=w, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x + w / 2, y, 0]))


def pc_nodes(x, y, s=0.32, gap=0.12):
    """Three nodes in a row: three grey squares with gaps (distributed memory). Left edge at x."""
    return VGroup(*[Square(side_length=s, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x + s / 2 + i * (s + gap), y, 0])
                    for i in range(3)])


# ─────────────── B60 · CPU against GPU: a two-column drawn table under the two blocks ───────────────
B60_CPU_C = np.array([-1.7, 1.75, 0.0])                              # block centres (the column heads)
B60_GPU_C = np.array([3.4, 1.75, 0.0])
B60_W, B60_H, B60_RIM = 2.6, 1.3, 0.12                               # block size, rim width (the rim is the block's colour)
B60_CORE, B60_CORE_XS = 0.46, (-0.78, -0.26, 0.26, 0.78)             # the four large cores
B60_COLS, B60_NROWS, B60_PITCH, B60_SIDE = 17, 7, 0.135, 0.095       # the small cores: 119 grey squares with gaps
B60_ROW_Y = (0.45, -0.5, -1.45)                                      # design goal · core count · best for
B60_ROWS = ("design goal", "core count", "best for")
B60_HEAD_Y = 0.95                                                    # the rule under the two blocks
B60_L, B60_R = -6.0, 6.0
B60_CAP_Y = -2.55                                                    # chefs · line cooks


def b60_block(c, rim):
    """A flat block: an ink-outlined rim in its own colour around a pale pad (the cores sit on the pad)."""
    outer = Rectangle(width=B60_W, height=B60_H, fill_color=rim, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(c)
    inner = Rectangle(width=B60_W - 2 * B60_RIM, height=B60_H - 2 * B60_RIM, fill_color=PC_PAD, fill_opacity=1, stroke_width=0).move_to(c)
    return VGroup(outer, inner)


def b60_cores():
    return VGroup(*[Square(side_length=B60_CORE, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to(B60_CPU_C + np.array([dx, 0.0, 0.0]))
                    for dx in B60_CORE_XS])


def b60_cell_xy(c, r):
    x = B60_GPU_C[0] + (c - (B60_COLS - 1) / 2) * B60_PITCH
    y = B60_GPU_C[1] + (r - (B60_NROWS - 1) / 2) * B60_PITCH
    return np.array([x, y, 0.0])


def b60_cells():
    """The small cores, one VGroup per column (filled column by column)."""
    return [VGroup(*[Square(side_length=B60_SIDE, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to(b60_cell_xy(c, r))
                     for r in range(B60_NROWS)]) for c in range(B60_COLS)]


def b60_fill(self, cols, rt):
    """The columns appear left to right in one play (any frame rate)."""
    n = len(cols)
    for m in cols:
        m.set_opacity(0)
    self.add(*cols)
    holder = VGroup(*cols)

    def upd(m, a):
        k = min(n, int(a * n + 0.5))
        for i, c in enumerate(cols):
            c.set_opacity(1.0 if i < k else 0.0)

    self.play(UpdateFromAlphaFunc(holder, upd), run_time=rt, rate_func=linear)
    upd(holder, 1.0)


def b60_rule(y, sw=3):
    return Line([B60_L, y, 0], [B60_R, y, 0], color=BAR1, stroke_width=sw)


def b60_cell(s, cx, y, size=32):
    return T(s, size).move_to([cx, y, 0])


def b60_cell2(s1, s2, cx, y, size=32):
    """A two-line cell."""
    return VGroup(T(s1, size).move_to([cx, y + 0.21, 0]), T(s2, size).move_to([cx, y - 0.21, 0]))


class B60_CpuVsGpu(Scene):
    def construct(self):
        self.add(pc_title("VI · GPU Computing"))
        labels = VGroup(*[pc_left(T(s, 34), B60_L, y) for s, y in zip(B60_ROWS, B60_ROW_Y)])
        rules = VGroup(b60_rule(B60_HEAD_Y, 5), *[b60_rule(y - 0.475) for y in B60_ROW_Y])
        self.play(FadeIn(labels, shift=RIGHT * 0.15), LaggedStart(*[Create(r) for r in rules], lag_ratio=0.15), run_time=0.7)   # the empty table
        # the CPU column
        until(self, "A CPU is built", lead=0.2)
        cpu = b60_block(B60_CPU_C, BAR2)
        pc_drop(self, [cpu], rt=0.45, dist=3.3)
        until(self, "low latency", lead=0.1)
        self.play(FadeIn(b60_cell("latency", B60_CPU_C[0], B60_ROW_Y[0]), shift=DOWN * 0.15), run_time=0.35)
        until(self, "tens of complex cores", lead=0.1)
        cores = b60_cores()
        self.play(LaggedStart(*[GrowFromCenter(k) for k in cores], lag_ratio=0.25), run_time=0.5)          # four large cores
        self.play(FadeIn(b60_cell("tens, complex", B60_CPU_C[0], B60_ROW_Y[1]), shift=DOWN * 0.15), run_time=0.35)
        until(self, "sequential logic", lead=0.15)
        self.play(FadeIn(b60_cell("sequential logic", B60_CPU_C[0], B60_ROW_Y[2]), shift=DOWN * 0.15), run_time=0.35)
        # the GPU column
        until(self, "A GPU is built", lead=0.2)
        gpu = b60_block(B60_GPU_C, DARK_TOP)
        pc_drop(self, [gpu], rt=0.45, dist=3.3)
        until(self, "throughput", lead=0.1)
        self.play(FadeIn(b60_cell("throughput", B60_GPU_C[0], B60_ROW_Y[0]), shift=DOWN * 0.15), run_time=0.35)
        until(self, "thousands of simple cores", lead=0.1)
        cells = b60_cells()
        b60_fill(self, cells, guard(self, 0.9))                                                          # the dense core grid fills
        self.play(FadeIn(b60_cell("thousands, simple", B60_GPU_C[0], B60_ROW_Y[1]), shift=DOWN * 0.15), run_time=0.35)
        until(self, "the same operation", lead=0.15)
        self.play(FadeIn(b60_cell2("same operation", "large arrays", B60_GPU_C[0], B60_ROW_Y[2]), shift=DOWN * 0.15), run_time=0.35)
        # chefs against line cooks
        until(self, "A few professional chefs", lead=0.1)
        self.play(Indicate(cores, color=None, scale_factor=1.12), FadeIn(b60_cell("chefs", B60_CPU_C[0], B60_CAP_Y, 34)), run_time=0.6)
        until(self, "a thousand line cooks", lead=0.1)
        grid = VGroup(*cells)
        self.play(Indicate(grid, color=None, scale_factor=1.05), FadeIn(b60_cell("line cooks", B60_GPU_C[0], B60_CAP_Y, 34)), run_time=0.6)
        done(self)


# ─────────────── B61 · the four steps of every GPU program: allocate · copy in · kernel · copy back ───────────────
B61_HOST = Iso(-3.4, -1.2, 1.4)                                      # the grey CPU block (host)
B61_DEV = Iso(2.6, -1.2, 1.7)                                        # the dark GPU block (device, the cast's gpu_block)
B61_DATA = 0.26                                                      # iso side of a data box
B61_CABLE_Y = -0.15
B61_CABLE_X0, B61_CABLE_X1 = -2.05, 1.0                              # clear of both blocks (a cable touching a block fuses with it)
B61_RIDE_X = (-1.85, -1.4, -0.95)                                    # where the three boxes sit on the cable before they slide
B61_SLIDE = 1.95                                                     # the slide along the cable
B61_SLAB = (0.12, 0.62, 0.5, 0.76, 0.3, 0.06)                        # memory slab on the device's top face (x0, y0, z0, w, d, h)
B61_SLAB_SPOTS = ((0.25, 0.77), (0.5, 0.77), (0.75, 0.77))           # where the data boxes land on the slab
B61_HOST_SPOTS = ((0.22, 0.5), (0.5, 0.5), (0.78, 0.5))              # where they start (and return) on the host's top face


def b61_host():
    return B61_HOST.box(0, 0, 0, 1.0, 1.0, 0.5, PC_CPU_TOP, PC_CPU_L, PC_CPU_R)


def b61_data(iso, x, y, z):
    """A small plain kraft data box centred on (x, y) of the iso, sitting on z. Small object: dark-kraft outline."""
    s = B61_DATA
    return iso.box(x - s / 2, y - s / 2, z, s, s, s * 0.8, sw=2).set_stroke(PC_SMALL).set_z_index(5)


def b61_centre(iso, x, y, z):
    return np.array(b61_data(iso, x, y, z).get_center())


def b61_cable():
    return Line([B61_CABLE_X0, B61_CABLE_Y, 0], [B61_CABLE_X1, B61_CABLE_Y, 0], color=PC_KRAFT, stroke_width=6).set_z_index(-1)


def b61_slab():
    """The allocated memory: a thin white slab on the back of the device's top face (no outline inside the ink outline)."""
    x0, y0, z0, w, d, h = B61_SLAB
    return B61_DEV.box(x0, y0, z0, w, d, h, PAGE_TOP, PAGE_L, PAGE_R, sw=0).set_z_index(3)


def b61_sparks():
    """Terracotta sparks on the front of the device's top face, inside the outline."""
    pts = [B61_DEV.p(0.15 + 0.7 * i / 3, y, 0.5) for i in range(4) for y in (0.15, 0.42)]
    return VGroup(*[Dot(p, radius=0.08, color=TERRA) for p in pts]).set_z_index(4)


def b61_ride(self, boxes, targets, rt):
    """Move the three boxes to three target centres in one play (guarded)."""
    rt = guard(self, rt)
    self.play(LaggedStart(*[b.animate.move_to(t) for b, t in zip(boxes, targets)], lag_ratio=0.15), run_time=rt)


class B61_FourSteps(Scene):
    def construct(self):
        host = b61_host()
        dev, light = gpu_block(B61_DEV)
        light.scale(1.6)
        self.add(host, dev, light, T("host", 36).move_to([-3.4, -1.7, 0]), T("device", 36).move_to([2.6, -1.7, 0]))
        until(self, "follows four steps", lead=0.1)
        self.play(Create(b61_cable()), run_time=0.5)                                                      # the cable between them
        # 1 · allocate
        until(self, "Allocate memory", lead=0.15)
        slab = b61_slab()
        self.play(GrowFromCenter(slab), run_time=0.4)
        self.play(FadeIn(M("cudaMalloc", 32).move_to([2.6, 1.95, 0]), shift=DOWN * 0.15), run_time=0.3)
        # 2 · copy in: the data boxes ride the cable host → device
        until(self, "Copy the data", lead=0.15)
        boxes = [b61_data(B61_HOST, x, y, 0.5) for x, y in B61_HOST_SPOTS]
        self.play(LaggedStart(*[GrowFromCenter(b) for b in boxes], lag_ratio=0.2), run_time=0.4)
        self.play(FadeIn(M("cudaMemcpy", 32).move_to([-0.55, 0.8, 0]), shift=DOWN * 0.15), run_time=0.3)
        ride = [np.array([x, B61_CABLE_Y + 0.2, 0.0]) for x in B61_RIDE_X]
        b61_ride(self, boxes, ride, 0.4)
        b61_ride(self, boxes, [r + RIGHT * B61_SLIDE for r in ride], 0.5)
        until(self, "CPU to GPU", lead=0.1)
        b61_ride(self, boxes, [b61_centre(B61_DEV, x, y, 0.56) for x, y in B61_SLAB_SPOTS], 0.4)
        # 3 · launch the kernel: sparks across the device
        until(self, "Launch a kernel", lead=0.1)
        self.play(FadeIn(M("kernel", 32).move_to([5.2, 0.4, 0]), shift=DOWN * 0.15), light.animate.set_color(TERRA), run_time=0.3)
        until(self, "thousands of threads", lead=0.1)
        sparks = b61_sparks()
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sparks], lag_ratio=0.06), run_time=0.6)
        until(self, "on different data", lead=0.1)
        self.play(Indicate(sparks, color=None, scale_factor=1.15), run_time=0.5)
        # 4 · copy back: the result boxes ride the cable device → host
        until(self, "Then copy the results back", lead=0.15)
        self.play(FadeIn(M("cudaMemcpy", 32).move_to([-0.55, -0.75, 0]), shift=UP * 0.15), FadeOut(sparks), light.animate.set_color(GHOST), run_time=0.3)
        self.remove(sparks)
        b61_ride(self, boxes, [r + RIGHT * B61_SLIDE for r in ride], 0.4)
        b61_ride(self, boxes, ride, 0.5)
        b61_ride(self, boxes, [b61_centre(B61_HOST, x, y, 0.5) for x, y in B61_HOST_SPOTS], 0.4)
        # host is the CPU; device is the GPU
        until(self, "Host is the CPU", lead=0.1)
        self.play(FadeIn(T("CPU", 34).move_to([-3.4, -2.25, 0]), shift=UP * 0.15), run_time=0.3)
        until(self, "device is the GPU", lead=0.1)
        self.play(FadeIn(T("GPU", 34).move_to([2.6, -2.25, 0]), shift=UP * 0.15), run_time=0.3)
        done(self)


# ─────────────── B83 · choosing the tool: eight rows, tool (mono) · memory model (icon + word) · best for ───────────────
B83_ROWS = (("OpenMP", "shared", "loop-level"),
            ("MPI", "distributed", "multi-node sims"),
            ("mpi4py", "distributed", "multi-node Python"),
            ("multiprocessing", "shared", "single-node tasks"),
            ("PyTorch DDP", "distributed", "training"),
            ("Dask / Ray", "both", "large data"),
            ("R parallel/foreach", "shared", "loops"),
            ("MATLAB parfor", "shared", "loops"))
B83_Y0, B83_DY = 2.1, 0.62                                           # first row centre, row pitch
B83_X_TOOL, B83_X_ICON, B83_X_WORD, B83_X_BEST = -6.0, -1.25, 0.75, 2.85  # left edges of the columns
B83_L, B83_R = -6.0, 6.0


def b83_y(k):
    return B83_Y0 - k * B83_DY


def b83_rule(k, sw=3):
    """The rule under row k (k = -1 is the heavier rule above the first row)."""
    return Line([B83_L, b83_y(k) - B83_DY / 2, 0], [B83_R, b83_y(k) - B83_DY / 2, 0], color=BAR1, stroke_width=sw)


def b83_cell(fn, s, size, x, y):
    """A table cell set on a common baseline: typeset with a trailing 'bp' (one ascender, one descender) so every
    cell has the same vertical extent, then the two extra glyphs are dropped."""
    try:
        full = fn(s + "bp", size).move_to([0, y, 0])
        g = VGroup(*list(full)[:len(s.replace(" ", ""))])
        if len(g) == 0:
            raise ValueError
        g.shift(RIGHT * (x - g.get_left()[0]))                      # left edge at x (the 'bp' only set the vertical extent)
        return g
    except Exception:                                                # Gate A's stub has no glyphs: plain left placement
        return pc_left(fn(s, size), x, y)


def b83_tool(k):
    return b83_cell(M, B83_ROWS[k][0], 32, B83_X_TOOL, b83_y(k))


def b83_icon(k):
    """shared → one slab; distributed → three nodes; both → the slab and the three nodes."""
    kind, y = B83_ROWS[k][1], b83_y(k)
    if kind == "shared":
        g = pc_slab(B83_X_ICON, y, w=0.6, h=0.28)
    elif kind == "distributed":
        g = pc_nodes(B83_X_ICON, y, s=0.28, gap=0.1)
    else:
        g = VGroup(pc_slab(B83_X_ICON, y, w=0.6, h=0.28), pc_nodes(B83_X_ICON + 0.76, y, s=0.28, gap=0.1))
    g.b83_icon = True
    return g


def b83_word(k):
    return b83_cell(T, B83_ROWS[k][1], 32, B83_X_WORD, b83_y(k))


def b83_best(k):
    return b83_cell(T, B83_ROWS[k][2], 32, B83_X_BEST, b83_y(k))


def b83_land(self, mobs, rt=0.4):
    """Icon + word + best-for land together."""
    anims = []
    for m in mobs:
        anims.append(GrowFromCenter(m) if getattr(m, "b83_icon", False) else FadeIn(m, shift=DOWN * 0.15))
    self.play(*anims, run_time=rt)


class B83_ToolTable(Scene):
    def construct(self):
        self.add(pc_title("VIII · Python, R, MATLAB"))
        until(self, "Choosing the tool", lead=0.0)
        self.play(Create(b83_rule(-1, 5)), run_time=0.4)
        self.play(LaggedStart(*[Create(b83_rule(k)) for k in range(8)], lag_ratio=0.12), run_time=0.8)   # eight rows open
        # OpenMP
        until(self, "OpenMP:", lead=0.15)
        self.play(FadeIn(b83_tool(0), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "shared memory,", lead=0.1)
        b83_land(self, [b83_icon(0), b83_word(0)])
        until(self, "loop-level", lead=0.1)
        b83_land(self, [b83_best(0)], 0.35)
        # MPI
        until(self, "MPI:", lead=0.15)
        self.play(FadeIn(b83_tool(1), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "distributed, multi-node", lead=0.1)
        b83_land(self, [b83_icon(1), b83_word(1), b83_best(1)])
        # mpi4py
        until(self, "mpi4py", lead=0.15)
        self.play(FadeIn(b83_tool(2), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "multi-node Python", lead=0.1)
        b83_land(self, [b83_icon(2), b83_word(2), b83_best(2)])
        # multiprocessing
        until(self, "multiprocessing", lead=0.15)
        self.play(FadeIn(b83_tool(3), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "single-node Python tasks", lead=0.1)
        b83_land(self, [b83_icon(3), b83_word(3), b83_best(3)])
        # PyTorch DDP
        until(self, "PyTorch DDP", lead=0.15)
        self.play(FadeIn(b83_tool(4), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "for training", lead=0.1)
        b83_land(self, [b83_icon(4), b83_word(4), b83_best(4)])
        # Dask / Ray
        until(self, "Dask or Ray", lead=0.15)
        self.play(FadeIn(b83_tool(5), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "big data and pipelines", lead=0.1)
        b83_land(self, [b83_best(5)], 0.35)
        until(self, "both memory models", lead=0.1)
        b83_land(self, [b83_icon(5), b83_word(5)])
        # R parallel / foreach, MATLAB parfor
        until(self, "R's parallel and foreach", lead=0.15)
        self.play(FadeIn(b83_tool(6), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "MATLAB's parfor", lead=0.1)
        self.play(FadeIn(b83_tool(7), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "embarrassingly parallel loops", lead=0.1)
        b83_land(self, [b83_icon(6), b83_word(6), b83_best(6), b83_icon(7), b83_word(7), b83_best(7)], 0.45)
        done(self)


# ─────────────── B90 · four takeaways tick in order, each with its cast icon; then where to get help ───────────────
B90_ROW_Y = (1.85, 0.75, -0.35, -1.45)
B90_BOX_X = -5.4
B90_ICON_X = 0.3
B90_ITEMS = ("profile first", "choose the level", "communication costs", "plan for parallelism")


def b90_box(y):
    return Square(side_length=0.42, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([B90_BOX_X, y, 0])


def b90_tick(y):
    return check(B90_BOX_X, y - 0.02, 0.18, INK, 6)


def b90_glass(x, y):
    return VGroup(Circle(radius=0.3, color=INK, stroke_width=6).move_to([x, y, 0]),
                  Line([x + 0.22, y - 0.22, 0], [x + 0.5, y - 0.5, 0], color=INK, stroke_width=9)).set_z_index(4)


def b90_gpu(x, y, s=0.5):
    """The cast's GPU block, small, with its light."""
    body, light = gpu_block(Iso(x, y, s))
    return VGroup(body, light)


def b90_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes (edges in dark kraft, never ink)."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PC_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PC_PAD, fill_opacity=1, stroke_color=PC_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def b90_tag(cx, cy):
    """A kraft luggage tag with a hole: the cost tag (small object: dark-kraft outline, never ink)."""
    body = Polygon([cx - 0.42, cy, 0], [cx - 0.22, cy + 0.22, 0], [cx + 0.42, cy + 0.22, 0], [cx + 0.42, cy - 0.22, 0], [cx - 0.22, cy - 0.22, 0],
                   fill_color=BOX_L, fill_opacity=1, stroke_color=PC_SMALL, stroke_width=3)
    hole = Dot([cx - 0.2, cy, 0], radius=0.05, color=CARD)
    return VGroup(body, hole).set_z_index(3)


def b90_page(x, y, s=0.7):
    return Iso(x, y, s).page(0, 0, 0)


class B90_Takeaways(Scene):
    def construct(self):
        self.add(pc_title("IX · Takeaways"))
        rows = VGroup()
        for y, s in zip(B90_ROW_Y, B90_ITEMS):
            bx = b90_box(y)
            rows.add(bx, T(s, 36).next_to(bx, RIGHT, buff=0.35))
        self.play(FadeIn(rows, shift=RIGHT * 0.15), run_time=0.5)
        # 1 · profile first: the magnifier sweeps and finds the bottleneck
        until(self, "Profile first", lead=0.1)
        glass = b90_glass(B90_ICON_X, B90_ROW_Y[0] + 0.05)
        self.play(Create(b90_tick(B90_ROW_Y[0])), GrowFromCenter(glass), run_time=0.4)
        until(self, "find the bottleneck", lead=0.1)
        self.play(glass.animate.shift(RIGHT * 1.6), run_time=0.6)
        self.play(GrowFromCenter(Dot([B90_ICON_X + 1.6, B90_ROW_Y[0] + 0.05, 0], radius=0.1, color=TERRA).set_z_index(5)), run_time=0.3)
        # 2 · choose the level: one node, three nodes, a GPU block, in a row
        until(self, "Choose the level", lead=0.1)
        self.play(Create(b90_tick(B90_ROW_Y[1])), run_time=0.3)
        until(self, "shared memory on one node", lead=0.1)
        self.play(GrowFromCenter(pc_slab(B90_ICON_X - 0.2, B90_ROW_Y[1], w=0.9, h=0.4)), run_time=0.35)
        until(self, "MPI across nodes", lead=0.1)
        self.play(GrowFromCenter(pc_nodes(B90_ICON_X + 1.2, B90_ROW_Y[1], s=0.4, gap=0.14)), run_time=0.35)
        until(self, "GPUs for data-parallel", lead=0.1)
        pc_drop(self, [b90_gpu(B90_ICON_X + 3.9, B90_ROW_Y[1] - 0.45)], rt=0.4, dist=3.0)
        # 3 · communication costs: a belt with a cost tag riding it
        until(self, "Communication costs", lead=0.1)
        belt = b90_belt(B90_ICON_X - 0.2, B90_ICON_X + 4.2, B90_ROW_Y[2] - 0.2)
        tag = b90_tag(B90_ICON_X + 0.6, B90_ROW_Y[2] + 0.22)
        self.play(Create(b90_tick(B90_ROW_Y[2])), FadeIn(belt), run_time=0.4)
        self.play(GrowFromCenter(tag), run_time=0.3)
        until(self, "more nodes are not always faster", lead=0.1)
        self.play(tag.animate.shift(RIGHT * 2.6), run_time=0.8)
        # 4 · plan for parallelism: a planning page lands
        until(self, "And plan for parallelism", lead=0.1)
        pc_drop(self, [b90_page(B90_ICON_X + 0.1, B90_ROW_Y[3] - 0.45)], rt=0.45, dist=3.0, with_=[Create(b90_tick(B90_ROW_Y[3]))])
        # questions: the help address
        until(self, "Questions", lead=0.2)
        self.play(FadeIn(M("rchelp@northeastern.edu", 34).move_to([0.0, -2.6, 0]), shift=UP * 0.15), run_time=0.5)
        done(self)


# attach the midpoint guard (see ST)
for _cls in (B40_Amdahl, B41_Gustafson, B53_HaloExchange, B55_Benchmark, B73_GpuBench, B60_CpuVsGpu, B61_FourSteps, B83_ToolTable, B90_Takeaways, B10_Laundry, B20_Flynn, B30_SharedVsDistributed, B31_TasksTimesCpus, B50_GameOfLife):
    _cls.play = ST.play
