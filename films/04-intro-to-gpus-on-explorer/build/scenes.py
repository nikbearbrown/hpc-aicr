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
# ═════════════════════════════ PART A · Act I (B10) and Act II (B20, B21) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PA_ / b10_ / b20_ / b21_ so the parts never collide.
#
# Stage map. Act I opens on the drawn partition table (film 2's B11 / film 3's B62 grammar: mono partition
# names, a heavy ink header rule, grey row rules, grey hour bars). Act II opens on two flat blocks side by
# side, a grey CPU and a dark GPU, each lifting its lid to show its cores (B20); B21 is the isometric city
# (kraft houses on a thin dark plinth) with the few dark carriers and the terracotta swarm, and the matrix
# grid on the right that fills all at once.
PA_KRAFT = "#9C8462"                        # deep-kraft connector (lines are never ink: ink lines fuse the things they join)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T: small ink rings fuse)
PA_PAD = "#E4E0D4"                          # pads and boards stay within 28 of the stage (Gate V does not count them as ink)


def pa_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_at(mob, x_left, y):
    """Place a text by its LEFT edge."""
    return mob.move_to([x_left + mob.width / 2, y, 0])


# ─────────────── B10 · the six GPU partitions: a drawn table with an hours bar per row ───────────────
B10_ROWS = [("gpu", 8, "8 h"), ("gpu-interactive", 2, "2 h"), ("gpu-short", 2, "2 h"),
            ("multigpu", 24, "24 h"), ("courses-gpu", 24, "24 h"), ("sharing", 1, "1 h")]
B10_X = (-6.0, -1.75, 0.95)                                          # left edge of each column (partition, max time, hours)
B10_BAR_X0, B10_BAR_UNIT = 0.95, 4.9 / 24                            # bar start, screen units per hour (24 h = 4.9, ends 5.85)
B10_Y0, B10_DY = 1.45, 0.72                                          # first row centre, row pitch
B10_HEAD_Y = B10_Y0 + B10_DY + 0.02
B10_L, B10_R = -6.0, 6.0
B10_TAG_X = 1.75                                                     # tags sit after the short bars (2 h ends 1.36, 1 h ends 1.15)


def b10_at(mob, col, y):
    return mob.move_to([B10_X[col] + mob.width / 2, y, 0])


def b10_cell(fn, s, size, col, y):
    """A table cell set on a common baseline: typeset with a trailing 'bp' (one ascender, one descender) so every
    cell has the same vertical extent, then the two extra glyphs are dropped."""
    try:
        full = b10_at(fn(s + "bp", size), col, y)
        g = VGroup(*list(full)[:len(s.replace(" ", ""))])
        if len(g) == 0:
            raise ValueError
        return g
    except Exception:                                                # Gate A's stub has no glyphs: plain centre placement
        return b10_at(fn(s, size), col, y)


def b10_y(k):
    return B10_Y0 - k * B10_DY


def b10_name(k):
    return b10_cell(M, B10_ROWS[k][0], 32, 0, b10_y(k))


def b10_time(k):
    return b10_cell(T, B10_ROWS[k][2], 40, 1, b10_y(k))


def b10_bar(k):
    w = B10_ROWS[k][1] * B10_BAR_UNIT
    return Rectangle(width=w, height=0.32, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B10_BAR_X0 + w / 2, b10_y(k), 0])


def b10_rule(k, color=BAR1, sw=3):
    """The rule under row k (k = -1 is the heavy rule under the header)."""
    y = b10_y(k) - B10_DY / 2
    return Line([B10_L, y, 0], [B10_R, y, 0], color=color, stroke_width=sw)


def b10_tag(cx, cy):
    """A kraft luggage tag with a hole (small object: dark-kraft outline, never ink)."""
    body = Polygon([cx - 0.42, cy, 0], [cx - 0.22, cy + 0.22, 0], [cx + 0.42, cy + 0.22, 0], [cx + 0.42, cy - 0.22, 0], [cx - 0.22, cy - 0.22, 0],
                   fill_color=BOX_L, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    hole = Dot([cx - 0.2, cy, 0], radius=0.05, color=CARD)
    return VGroup(body, hole)


class B10_GpuPartitions(Scene):
    def construct(self):
        self.add(pa_title("I · The GPU Partitions"))
        hb = lambda t, size: T(t, size, bold=True)
        head = VGroup(b10_cell(hb, "partition", 36, 0, B10_HEAD_Y), b10_cell(hb, "max time", 36, 1, B10_HEAD_Y),
                      b10_cell(hb, "hours", 36, 2, B10_HEAD_Y))
        until(self, "Start with where", lead=0.0)
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.4)
        until(self, "into partitions", lead=0.2)
        self.play(Create(b10_rule(-1, INK, 5)), run_time=0.5)                                      # the heavy header rule
        until(self, "six are the ones", lead=0.2)
        self.play(LaggedStart(*[Create(b10_rule(k)) for k in range(6)], lag_ratio=0.2), run_time=0.9)   # six rows open
        until(self, "gpu, the general one", lead=0.2)
        self.play(FadeIn(b10_name(0), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "up to eight hours", lead=0.1)
        self.play(FadeIn(b10_time(0)), GrowFromEdge(b10_bar(0), LEFT), run_time=0.5)
        until(self, "gpu-interactive", lead=0.2)
        self.play(FadeIn(b10_name(1), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "two hours.", lead=0.1)
        self.play(FadeIn(b10_time(1)), GrowFromEdge(b10_bar(1), LEFT), run_time=0.4)
        until(self, "gpu-short", lead=0.2)
        self.play(FadeIn(b10_name(2), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "two hours too", lead=0.1)
        self.play(FadeIn(b10_time(2)), GrowFromEdge(b10_bar(2), LEFT), run_time=0.4)
        until(self, "but prioritised", lead=0.1)
        self.play(FadeIn(pa_at(T("prioritised", 32), B10_TAG_X, b10_y(2)), shift=RIGHT * 0.2), run_time=0.4)   # the ink tag
        until(self, "multigpu", lead=0.2)
        self.play(FadeIn(b10_name(3), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "twenty-four hours", lead=0.1)
        self.play(FadeIn(b10_time(3)), GrowFromEdge(b10_bar(3), LEFT), run_time=0.6)
        until(self, "courses-gpu", lead=0.2)
        self.play(FadeIn(b10_name(4), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "for classes, twenty-four", lead=0.0)
        self.play(FadeIn(b10_time(4)), GrowFromEdge(b10_bar(4), LEFT), run_time=0.6)
        until(self, "And sharing", lead=0.2)
        self.play(FadeIn(b10_name(5), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "lend to everyone", lead=0.1)
        self.play(GrowFromCenter(b10_tag(B10_TAG_X + 0.42, b10_y(5))),                                # the kraft tag
                  FadeIn(pa_at(T("lent by PIs", 32), B10_TAG_X + 1.05, b10_y(5)), shift=RIGHT * 0.2), run_time=0.4)
        until(self, "one hour at a time", lead=0.1)
        self.play(FadeIn(b10_time(5)), GrowFromEdge(b10_bar(5), LEFT), run_time=0.35)
        done(self)


# ─────────────── B20 · a few large cores against thousands of small ones ───────────────
B20_CPU_C = np.array([-3.2, -0.25, 0.0])                             # block centres
B20_GPU_C = np.array([3.2, -0.25, 0.0])
B20_W, B20_H, B20_RIM = 4.4, 3.3, 0.2                                # block size, rim width (the rim is the block's colour)
B20_CORE, B20_CORE_OFF = 1.05, 0.7                                   # the four large cores: side, offset from centre
B20_COLS, B20_NROWS, B20_PITCH, B20_SIDE = 24, 16, 0.16, 0.11        # the small cores: 384 grey squares with gaps
B20_TOP_Y = 2.3                                                      # the lone core, then the problem bar
B20_LAB_Y = -2.45


def b20_block(c, rim):
    """A flat block: an ink-outlined rim in its own colour around a pale pad (the cores sit on the pad)."""
    outer = Rectangle(width=B20_W, height=B20_H, fill_color=rim, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(c)
    inner = Rectangle(width=B20_W - 2 * B20_RIM, height=B20_H - 2 * B20_RIM, fill_color=PA_PAD, fill_opacity=1, stroke_width=0).move_to(c)
    return VGroup(outer, inner)


def b20_lid(c, fill):
    """The lid that covers the pad until the block opens (fully opaque, no outline inside the ink rim)."""
    return Rectangle(width=B20_W - 2 * B20_RIM, height=B20_H - 2 * B20_RIM, fill_color=fill, fill_opacity=1, stroke_width=0).move_to(c)


def b20_slot(k):
    """Centre of large core k (0..3) in the CPU block."""
    dx, dy = ((-1, 1), (1, 1), (-1, -1), (1, -1))[k]
    return B20_CPU_C + np.array([dx * B20_CORE_OFF, dy * B20_CORE_OFF, 0.0])


def b20_core(k):
    return Square(side_length=B20_CORE, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to(b20_slot(k))


def b20_cell_xy(c, r):
    x = B20_GPU_C[0] + (c - (B20_COLS - 1) / 2) * B20_PITCH
    y = B20_GPU_C[1] + (r - (B20_NROWS - 1) / 2) * B20_PITCH
    return np.array([x, y, 0.0])


def b20_cells():
    """The small cores, one VGroup per column (filled column by column)."""
    return [VGroup(*[Square(side_length=B20_SIDE, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to(b20_cell_xy(c, r))
                     for r in range(B20_NROWS)]) for c in range(B20_COLS)]


def b20_fill(self, cols, rt):
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


def b20_bar():
    return Rectangle(width=3.6, height=0.34, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([0, B20_TOP_Y, 0])


def b20_slivers():
    """The problem bar cut into one sliver per GPU column."""
    return [Rectangle(width=0.1, height=0.34, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-1.8 + 0.075 + 0.15 * i, B20_TOP_Y, 0])
            for i in range(B20_COLS)]


class B20_FewVsThousands(Scene):
    def construct(self):
        self.add(pa_title("II · What A GPU Is"))
        cpu, gpu = b20_block(B20_CPU_C, BAR2), b20_block(B20_GPU_C, DARK_TOP)
        lid_c, lid_g = b20_lid(B20_CPU_C, BAR2), b20_lid(B20_GPU_C, DARK_TOP)
        self.add(cpu, lid_c, gpu, lid_g)                                                             # two closed blocks
        until(self, "Start with a core", lead=0.2)
        core = Square(side_length=0.6, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([0, B20_TOP_Y, 0])
        self.play(GrowFromCenter(core), run_time=0.4)                                               # one core, on its own
        until(self, "A CPU has", lead=0.2)
        self.play(lid_c.animate.shift(UP * 0.35).set_opacity(0), run_time=0.4)                      # the CPU opens
        self.remove(lid_c)
        self.play(core.animate.move_to(b20_slot(0)).scale(B20_CORE / 0.6), run_time=0.5)           # the core becomes the first of four
        self.play(LaggedStart(*[GrowFromCenter(b20_core(k)) for k in (1, 2, 3)], lag_ratio=0.35), run_time=0.6)
        self.play(FadeIn(T("a few complex cores", 34).move_to([B20_CPU_C[0], B20_LAB_Y, 0]), shift=UP * 0.15), run_time=0.35)
        until(self, "A GPU has thousands", lead=0.2)
        self.play(lid_g.animate.shift(UP * 0.35).set_opacity(0), run_time=0.4)                      # the GPU opens
        self.remove(lid_g)
        cells = b20_cells()
        b20_fill(self, cells, 1.1)                                                                   # hundreds of small cores fill in
        self.play(FadeIn(T("thousands of simple cores", 34).move_to([B20_GPU_C[0], B20_LAB_Y, 0]), shift=UP * 0.15), run_time=0.35)
        until(self, "For a problem", lead=0.2)
        bar = b20_bar()
        self.play(GrowFromCenter(bar), run_time=0.4)                                                # the problem
        until(self, "split into thousands", lead=0.1)
        slivers = b20_slivers()
        self.remove(bar)
        self.add(*slivers)
        self.play(LaggedStart(*[s.animate.move_to(b20_cell_xy(i, B20_NROWS - 1) + UP * 0.1) for i, s in enumerate(slivers)], lag_ratio=0.02),
                  run_time=0.9)                                                                      # the slivers land on the grid
        self.play(*[c.animate.set_color(BAR1) for c in cells], *[FadeOut(s) for s in slivers], run_time=0.4)   # every small core busy
        self.remove(*slivers)
        until(self, "the GPU is the right tool", lead=0.1)
        self.play(GrowFromCenter(check(B20_GPU_C[0] + 1.75, B20_TOP_Y - 0.2, s=0.22, color=TERRA)), run_time=0.4)
        done(self)


# ─────────────── B21 · Ferraris and bicycles: a few fast against thousands at once, then the matrix ───────────────
B21_CITY = Iso(-3.2, -2.75, 0.46)                                    # the city: 6 x 6 kraft houses on a 1-unit street grid
B21_N = 6
B21_HW, B21_HH = 0.5, 0.4                                            # house footprint and height
B21_FERRARI_HOUSES = ((0, 4), (0, 1), (3, 0))                        # the three houses the carriers reach (front edges: nothing occludes a parked carrier)
B21_PARK = {(0, 4): (-0.55, 4.35), (0, 1): (-0.55, 1.35), (3, 0): (3.27, -0.55)}   # where each carrier parks (x0, y0), on the plinth margin
B21_DEPOT_CAR = (np.array([4.3, 1.9, 0.0]), np.array([5.0, 1.9, 0.0]), np.array([5.7, 1.9, 0.0]))
B21_DEPOT_DOTS = np.array([5.0, 1.05, 0.0])                          # the swarm waits here, 9 x 4
B21_LAB_X = 0.85                                                     # labels sit to the left of the depot rows
B21_MAT_C = np.array([3.3, -1.2, 0.0])                               # the matrix: 14 x 8 cells
B21_MAT_COLS, B21_MAT_ROWS, B21_MAT_PITCH, B21_MAT_SIDE = 14, 8, 0.3, 0.23
B21_PROFS = (16, 60, 94)                                             # the three cells the professors fill (one at a time)
B21_MAT_SCALE0 = 0.85                                                # drawn small, grows at "a very large matrix"


def b21_zi(x, y):
    """Painter's order in the city: things nearer the viewer (smaller x + y) draw later."""
    return 30.0 - 2.0 * (x + y)


def b21_plinth():
    """A thin plinth under the city: pale board on top, dark sides carry Gate V's contrast."""
    return B21_CITY.box(-0.6, -0.6, -0.12, B21_N + 1.2, B21_N + 1.2, 0.12, PA_PAD, DARK_L, DARK_R).set_z_index(-1)


def b21_house(i, j):
    """A small kraft house (small object: dark-kraft outline)."""
    iso, x0, y0 = B21_CITY, i + 0.25, j + 0.25
    x1, y1, z1 = x0 + B21_HW, y0 + B21_HW, B21_HH
    h = VGroup(iso.quad([(x0, y0, 0), (x0, y1, 0), (x0, y1, z1), (x0, y0, z1)], BOX_L, stroke=PA_SMALL, sw=2),
               iso.quad([(x0, y0, 0), (x1, y0, 0), (x1, y0, z1), (x0, y0, z1)], BOX_R, stroke=PA_SMALL, sw=2),
               iso.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], BOX_TOP, stroke=PA_SMALL, sw=2))
    return h.set_z_index(b21_zi(x0 + 0.25, y0 + 0.25))


def b21_houses():
    """All 36 houses, back row first."""
    order = sorted([(i, j) for i in range(B21_N) for j in range(B21_N)], key=lambda ij: -(ij[0] + ij[1]))
    return VGroup(*[b21_house(i, j) for i, j in order])


def b21_roof(i, j):
    return B21_CITY.p(i + 0.5, j + 0.5, B21_HH)


def b21_dot(i, j):
    return Dot(b21_roof(i, j), radius=0.07, color=TERRA).set_z_index(b21_zi(i + 0.5, j + 0.5) + 0.5)


def b21_carrier(i, j):
    """A dark carrier parked on the plinth margin beside house (i, j), at the city's front edge."""
    iso = B21_CITY
    x0, y0 = B21_PARK[(i, j)]
    return iso.box(x0, y0, 0, 0.45, 0.3, 0.22, DARK_TOP, DARK_L, DARK_R, sw=2).set_z_index(b21_zi(x0 + 0.225, y0 + 0.15))


def b21_cell(k):
    c, r = k % B21_MAT_COLS, k // B21_MAT_COLS
    x = B21_MAT_C[0] + (c - (B21_MAT_COLS - 1) / 2) * B21_MAT_PITCH
    y = B21_MAT_C[1] + (r - (B21_MAT_ROWS - 1) / 2) * B21_MAT_PITCH
    return Square(side_length=B21_MAT_SIDE, fill_color=PA_PAD, fill_opacity=1, stroke_color=BAR3, stroke_width=1.5).move_to([x, y, 0])


def b21_matrix():
    return VGroup(*[b21_cell(k) for k in range(B21_MAT_COLS * B21_MAT_ROWS)])


def b21_park(mob, depot):
    """Move a finished object to its depot spot; returns the vector that brings it back (the stub's centre is a list)."""
    v = depot - np.array(mob.get_center())
    mob.shift(v)
    return -v


class B21_FerrarisAndBicycles(Scene):
    def construct(self):
        self.add(b21_plinth())
        cars = [b21_carrier(i, j) for i, j in B21_FERRARI_HOUSES]
        car_back = [b21_park(c, d) for c, d in zip(cars, B21_DEPOT_CAR)]
        rest = [(i, j) for i in range(B21_N) for j in range(B21_N) if (i, j) not in B21_FERRARI_HOUSES]
        dots = [b21_dot(i, j) for i, j in rest]
        slots = [B21_DEPOT_DOTS + np.array([(k % 9 - 4) * 0.16, (1.5 - k // 9) * 0.16, 0.0]) for k in range(len(dots))]
        dot_back = [b21_park(d, s) for d, s in zip(dots, slots)]
        self.add(*cars, *dots)                                                                       # the few and the many wait
        until(self, "Delivering thousands", lead=0.2)
        houses = b21_houses()
        rt = guard(self, 1.0)
        for h in houses:
            h.shift(UP * 4.0)
        self.add(houses)
        self.play(LaggedStart(*[h.animate.shift(DOWN * 4.0) for h in houses], lag_ratio=0.02), run_time=rt, rate_func=ease_in)   # the city
        until(self, "a few Ferraris", lead=0.2)
        self.play(FadeIn(pa_at(T("a few fast", 34), B21_LAB_X, B21_DEPOT_CAR[0][1]), shift=RIGHT * 0.2), run_time=0.3)
        self.play(LaggedStart(*[c.animate.shift(v) for c, v in zip(cars, car_back)], lag_ratio=0.3), run_time=1.3)   # one house each
        self.play(*[GrowFromCenter(b21_dot(i, j)) for i, j in B21_FERRARI_HOUSES], run_time=0.25)
        until(self, "or thousands of bicycles", lead=0.1)
        self.play(FadeIn(pa_at(T("thousands at once", 34), B21_LAB_X, B21_DEPOT_DOTS[1]), shift=RIGHT * 0.2), run_time=0.3)
        until(self, "The bicycles.", lead=0.1)
        self.play(LaggedStart(*[d.animate.shift(v) for d, v in zip(dots, dot_back)], lag_ratio=0.01), run_time=1.1)   # every house at once
        until(self, "Or a room of professors", lead=0.1)
        mat = b21_matrix().scale(B21_MAT_SCALE0)
        self.play(FadeIn(mat, shift=UP * 0.15), run_time=0.5)                                       # the matrix, empty
        until(self, "The professors win", lead=0.1)
        profs = VGroup(*[Square(side_length=B21_MAT_SIDE * B21_MAT_SCALE0, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0)
                         .move_to(np.array(mat[k].get_center())) for k in B21_PROFS])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in profs], lag_ratio=0.45), run_time=1.0)   # a few cells, one at a time
        mat.add(*profs)
        until(self, "a very large matrix", lead=0.1)
        self.play(mat.animate.scale(1.0 / B21_MAT_SCALE0), run_time=0.5)                            # very large
        until(self, "a multiply and an add", lead=0.1)
        self.play(mat[0].animate.scale(1.6), run_time=0.25)                                          # one cell's work
        self.play(mat[0].animate.scale(1.0 / 1.6), run_time=0.25)
        until(self, "the stadium wins", lead=0.1)
        self.play(*[c.animate.set_color(BAR1) for c in list(mat)[:B21_MAT_COLS * B21_MAT_ROWS]], run_time=0.5)   # every cell, all at once
        until(self, "those are stadium jobs", lead=0.1)
        self.play(GrowFromCenter(check(5.7, 0.35, s=0.22, color=TERRA)), run_time=0.4)
        done(self)
# ═════════════════════════════ PART B · B60 (Act VI) · B72 (Act VII) · B80 (Act VIII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB_ / pb_ / b6x_ / b7x_ / b8x_ so the parts never collide.
PB_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T)


def pb_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb_left(mob, x, y):
    """Left-align a text at x, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pb_drop(self, mobs, rt=0.5, lag=0.2, dist=4.0, **extra):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    anims = [LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag)]
    self.play(*anims, *extra.get("with_", []), run_time=rt, rate_func=ease_in)


# ─────────────── B60 · the real gpu-logs record: memory climbs, utilization waits, 56% only at the end ───────────────
# Source timings (minute-by-minute, job 2374457): memory 0% to 12:56, 22.56% from 12:57, 77.98% from 13:02,
# 81.1% from 13:07; utilization 0% to 13:06, 56% from 13:07. Axis 12:52 → 13:11 (19 minutes).
B60_X0, B60_X1 = -5.2, 5.6                  # 12:52 … 13:11
B60_Y0, B60_YS = -2.55, 0.037               # 0 % baseline; screen units per percent (100 % = 1.15)
B60_MEM_OFF = 0.1                           # memory's zero stretch sits a hair above the baseline so the two lines never fuse


def b60_x(minute):
    """Screen x of a time given as minutes after 12:52."""
    return B60_X0 + (B60_X1 - B60_X0) * minute / 19.0


def b60_y(pct):
    return B60_Y0 + B60_YS * pct


def b60_seg(x0, y0, x1, y1, color, sw):
    return Line([x0, y0, 0], [x1, y1, 0], color=color, stroke_width=sw)


def b60_mem(x0, y0, x1, y1):
    return b60_seg(x0, y0, x1, y1, BAR1, 9)


def b60_util(x0, y0, x1, y1):
    return b60_seg(x0, y0, x1, y1, INK, 6).set_z_index(2)


def b60_axes():
    return VGroup(Line([B60_X0, B60_Y0, 0], [B60_X1 + 0.2, B60_Y0, 0], color=BAR1, stroke_width=4),
                  Line([B60_X0, B60_Y0, 0], [B60_X0, 1.45, 0], color=BAR1, stroke_width=4))


def b60_tick(minute):
    x = b60_x(minute)
    return Line([x, B60_Y0, 0], [x, B60_Y0 - 0.16, 0], color=BAR1, stroke_width=4)


class B60_GpuLogs(Scene):
    def construct(self):
        self.add(pb_title("VI · Watching The GPU"), b60_axes(),
                 M("12:52", 32).move_to([B60_X0, -2.98, 0]), M("13:11", 32).move_to([B60_X1, -2.98, 0]))
        until(self, "Put NVIDIA S M I", lead=0.1)
        smi = M("nvidia-smi", 34).move_to([4.3, 3.0, 0])
        self.play(FadeIn(smi, shift=DOWN * 0.15), run_time=0.4)
        until(self, "gpu-logs with the job ID", lead=0.1)
        self.play(FadeIn(pb_left(M("$ gpu-logs 2374457", 34), -6.1, 2.25), shift=RIGHT * 0.15), run_time=0.4)
        until(self, "minute-by-minute record", lead=0.1)
        self.play(Create(VGroup(b60_tick(5), b60_tick(10), b60_tick(15))), FadeIn(M("13:07", 32).move_to([b60_x(15), -2.98, 0])), run_time=0.4)
        # five minutes of nothing: both lines flat at zero, 12:52 → 12:57
        until(self, "for five minutes nothing", lead=0.2)
        m0 = b60_mem(B60_X0, B60_Y0 + B60_MEM_OFF, b60_x(5), B60_Y0 + B60_MEM_OFF)
        u0 = b60_util(B60_X0, B60_Y0, b60_x(5), B60_Y0)
        self.play(Create(m0), Create(u0), run_time=0.9)
        # memory climbs to 22.56 %, holds to 13:02
        until(self, "Then memory climbs", lead=0.1)
        m1 = VGroup(b60_mem(b60_x(5), B60_Y0 + B60_MEM_OFF, b60_x(5), b60_y(22.56)), b60_mem(b60_x(5), b60_y(22.56), b60_x(10), b60_y(22.56)))
        self.play(Create(m1), run_time=0.6)
        self.add(T("22.56%", 32).move_to([-0.95, -1.25, 0]))
        # then 77.98 %, holds to 13:07
        until(self, "then seventy-eight", lead=0.1)
        m2 = VGroup(b60_mem(b60_x(10), b60_y(22.56), b60_x(10), b60_y(77.98)), b60_mem(b60_x(10), b60_y(77.98), b60_x(15), b60_y(77.98)))
        self.play(Create(m2), run_time=0.6)
        self.add(T("77.98%", 32).move_to([1.9, 0.8, 0]))
        # utilization still zero: the ink line runs flat to 13:07
        until(self, "with utilization still zero", lead=0.1)
        u1 = b60_util(b60_x(5), B60_Y0, b60_x(15), B60_Y0)
        self.play(Create(u1), run_time=0.8)
        until(self, "the model is loading", lead=0.1)
        self.play(Indicate(VGroup(m1, m2), color=None, scale_factor=1.03), run_time=0.6)
        # only at the end: utilization steps to 56 %, memory to 81.1 %, both hold to 13:11
        until(self, "Only at the end", lead=0.1)
        u2 = VGroup(b60_util(b60_x(15), B60_Y0, b60_x(15), b60_y(56)), b60_util(b60_x(15), b60_y(56), B60_X1, b60_y(56)))
        m3 = VGroup(b60_mem(b60_x(15), b60_y(77.98), b60_x(15), b60_y(81.1)), b60_mem(b60_x(15), b60_y(81.1), B60_X1, b60_y(81.1)))
        self.play(Create(u2), Create(m3), run_time=0.8)
        self.add(T("81.1%", 32).move_to([4.5, 0.95, 0]))
        until(self, "fifty-six percent", lead=0.1)
        dot = Dot([b60_x(15), b60_y(56), 0], radius=0.12, color=TERRA).set_z_index(3)
        self.play(GrowFromCenter(dot), FadeIn(T("56%", 32).move_to([4.5, -0.95, 0])), run_time=0.4)
        # most of the job's time: the flat stretch is 'waiting'
        until(self, "the GPU was waiting", lead=0.3)
        self.play(FadeIn(T("waiting", 40).move_to([-3.9, -1.95, 0]), shift=UP * 0.15), run_time=0.4)
        self.play(Indicate(VGroup(u0, u1), color=None, scale_factor=1.02), run_time=0.6)
        done(self)


# ─────────────── B72 · fifty thousand parcels one at a time, or one crate and every core at once ───────────────
B72_L = Iso(-3.0, -1.7, 1.6)                # the left GPU block (parcels)
B72_R = Iso(3.0, -1.7, 1.6)                 # the right GPU block (the crate)
B72_PARCEL = 0.2                            # iso side of a tiny parcel (no tape: a short tape stripe reads as accent text)
B72_CRATE = 0.72                            # iso side of the crate


def b72_parcel(iso, s=B72_PARCEL):
    """A tiny plain kraft parcel on the block's top face. Small object: dark-kraft outline."""
    return iso.box(0.5 - s / 2, 0.5 - s / 2, 0.5, s, s, s * 0.8, sw=2).set_z_index(4)


def b72_parcel_outline(p):
    return p.set_stroke(PB_SMALL)


def b72_crate(iso, s=B72_CRATE):
    return iso.box(0.5 - s / 2, 0.5 - s / 2, 0.5, s, s, s * 0.75).set_z_index(4)


def b72_sparks(iso, n=4, inset=0.16):
    """A grid of terracotta sparks INSIDE the top face (never crossing its outline)."""
    pts = [iso.p(inset + (1 - 2 * inset) * i / (n - 1), inset + (1 - 2 * inset) * j / (n - 1), 0.5) for i in range(n) for j in range(n)]
    return VGroup(*[Dot(p, radius=0.075, color=TERRA) for p in pts]).set_z_index(3)


class B72_ParcelsVsCrate(Scene):
    def construct(self):
        lb, ll = gpu_block(B72_L)
        rb, rl = gpu_block(B72_R)
        ll.scale(1.7)
        rl.scale(1.7)
        self.add(lb, ll, rb, rl)
        until(self, "Fifty thousand tiny parcels", lead=0.15)
        self.add(T("50,000 × 1", 40).move_to([-3.0, -2.5, 0]))
        for k in range(6):                                  # one parcel at a time; the light flickers on each landing
            p = b72_parcel_outline(b72_parcel(B72_L))
            rt = guard(self, 0.26)
            p.shift(UP * 3.4)
            self.add(p)
            self.play(p.animate.shift(DOWN * 3.4), ll.animate.set_color(TERRA), run_time=rt, rate_func=ease_in)
            rt = guard(self, 0.2)
            self.play(FadeOut(p, scale=0.3), ll.animate.set_color(GHOST), run_time=rt)
        until(self, "Or one crate", lead=0.15)
        self.add(T("1 × 50,000", 40).move_to([3.0, -2.5, 0]))
        c = b72_crate(B72_R)
        pb_drop(self, [c], rt=0.5, dist=3.6)
        until(self, "every core busy", lead=0.1)
        self.play(FadeOut(c, scale=0.3), rl.animate.set_color(TERRA), run_time=0.3)
        sparks = b72_sparks(B72_R)
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sparks], lag_ratio=0.04), run_time=0.7)
        done(self)


# ─────────────── B80 · four habits tick in order, each with its cast icon; then where to get help ───────────────
B80_ROW_Y = (1.85, 0.75, -0.35, -1.45)
B80_BOX_X = -5.4
B80_ICON_X = 0.3
B80_ITEMS = ("right partition", "only what you need", "GPU libraries", "profile first")


def b80_box(y):
    return Square(side_length=0.42, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([B80_BOX_X, y, 0])


def b80_tick(y):
    return check(B80_BOX_X, y - 0.02, 0.18, INK, 6)


def b80_tag(x, y):
    """A partition tag: a pale pill with a grey outline, a hole and one terracotta dot."""
    body = RoundedRectangle(width=1.1, height=0.5, corner_radius=0.16, fill_color=CARD, fill_opacity=1,
                            stroke_color=PB_SMALL, stroke_width=3).move_to([x, y, 0])
    hole = Dot([x - 0.35, y, 0], radius=0.07, color=BAR1)
    dot = Dot([x + 0.22, y, 0], radius=0.09, color=TERRA)
    return VGroup(body, hole, dot)


def b80_slot(x, y, s=0.62):
    """An empty job slot: a pale pad with a grey outline."""
    return Iso(x, y, s).quad([(-0.1, -0.1, 0), (0.8, -0.1, 0), (0.8, 0.8, 0), (-0.1, 0.8, 0)], GHOST, stroke=BAR1, sw=3).set_z_index(-1)


def b80_job(x, y, s=0.62):
    return job_box(Iso(x, y, s)).set_z_index(2)


def b80_library(x, y, s=0.62):
    """A dark library block."""
    return Iso(x, y, s).box(-0.1, -0.1, 0, 0.95, 0.95, 0.55, DARK_TOP, DARK_L, DARK_R)


def b80_glass(x, y):
    return VGroup(Circle(radius=0.3, color=INK, stroke_width=6).move_to([x, y, 0]),
                  Line([x + 0.22, y - 0.22, 0], [x + 0.5, y - 0.5, 0], color=INK, stroke_width=9)).set_z_index(4)


class B80_FourHabits(Scene):
    def construct(self):
        self.add(pb_title("VIII · Habits"))
        rows = VGroup()
        for y, s in zip(B80_ROW_Y, B80_ITEMS):
            bx = b80_box(y)
            rows.add(bx, T(s, 36).next_to(bx, RIGHT, buff=0.35))
        self.play(FadeIn(rows, shift=RIGHT * 0.15), run_time=0.5)
        # 1 · the right partition
        until(self, "Choose the right partition", lead=0.1)
        self.play(Create(b80_tick(B80_ROW_Y[0])), GrowFromCenter(b80_tag(B80_ICON_X, B80_ROW_Y[0])), run_time=0.4)
        until(self, "gpu-short", lead=0.1)
        self.play(FadeIn(M("gpu-short", 34).move_to([2.5, B80_ROW_Y[0], 0]), shift=DOWN * 0.15), run_time=0.35)
        until(self, "s batch", lead=0.1)
        self.play(FadeIn(M("sbatch", 34).move_to([5.3, B80_ROW_Y[0], 0]), shift=DOWN * 0.15), run_time=0.35)
        # 2 · only what you need: a job box shrinks to fit its slot
        until(self, "Request only what you need", lead=0.1)
        slot = b80_slot(B80_ICON_X - 0.3, B80_ROW_Y[1] - 0.42)
        self.play(Create(b80_tick(B80_ROW_Y[1])), FadeIn(slot), run_time=0.4)
        job = b80_job(B80_ICON_X - 0.3, B80_ROW_Y[1] - 0.42)
        big = job.copy().scale(1.6, about_point=job.get_center())
        pb_drop(self, [big], rt=0.45, dist=3.0)
        rt = guard(self, 0.5)
        self.play(big.animate.scale(1 / 1.6, about_point=job.get_center()), run_time=rt)
        until(self, "seff", lead=0.1)
        self.play(FadeIn(M("seff", 34).move_to([3.3, B80_ROW_Y[1], 0]), shift=DOWN * 0.15), run_time=0.35)
        # 3 · GPU libraries: a dark library block
        until(self, "Use the GPU-tuned libraries", lead=0.1)
        lib = b80_library(B80_ICON_X - 0.3, B80_ROW_Y[2] - 0.42)
        pb_drop(self, [lib], rt=0.45, dist=3.0, with_=[Create(b80_tick(B80_ROW_Y[2]))])
        until(self, "CUDA and cuDNN", lead=0.1)
        self.play(FadeIn(M("CUDA", 34).move_to([2.7, B80_ROW_Y[2], 0]), shift=DOWN * 0.15),
                  FadeIn(M("cuDNN", 34).move_to([4.9, B80_ROW_Y[2], 0]), shift=DOWN * 0.15), run_time=0.35)
        # 4 · profile first: the magnifier sweeps
        until(self, "And profile before you optimise", lead=0.1)
        glass = b80_glass(B80_ICON_X - 0.45, B80_ROW_Y[3] + 0.05)
        self.play(Create(b80_tick(B80_ROW_Y[3])), GrowFromCenter(glass), run_time=0.4)
        self.play(glass.animate.shift(RIGHT * 0.8), run_time=0.6)
        # stuck? the help address
        until(self, "Email r c help", lead=0.2)
        self.play(FadeIn(M("rchelp@northeastern.edu", 34).move_to([0.0, -2.6, 0]), shift=UP * 0.15), run_time=0.5)
        done(self)


# attach the midpoint guard (see ST)
for _cls in (B60_GpuLogs, B72_ParcelsVsCrate, B80_FourHabits, B10_GpuPartitions, B20_FewVsThousands, B21_FerrarisAndBicycles):
    _cls.play = ST.play
