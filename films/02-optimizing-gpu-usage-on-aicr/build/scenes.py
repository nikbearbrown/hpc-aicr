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
# ═════════════════════════════ PART A · Act I (B10 B11 B13 B14 B15 B16) and Act II (B20) ═════════════════════════════
# Stage map. Act I is about one question: do you actually have the GPU? The cast is the kit's: grey CPU slabs
# (the "CPU only" block of film 1), the dark gpu_block with its light, the kraft job_box. B11 is the drawn
# table of film 1's B40 with this film's columns; B16 is film 1's B43 re-paced. Act II opens on the dark
# nvidia-smi terminal (B20), the one real interface in this part, shown as itself.
PA_KRAFT = "#9C8462"                        # deep-kraft connector (cables never ink: ink cables fuse the things they join)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only
PA_PAD = "#E4E0D4"                          # pads stay within 28 of the stage (Gate V does not count them as ink)
PA_TERM = DARK_TOP                          # the terminal panel (a real tool keeps its real look: dark, pale mono)


def pa_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


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


def pa_cpu(iso, x0=0.0, y0=0.0, n=2):
    """The CPU block: n lighter grey slabs, no GPU light (film 1's "CPU only" cast)."""
    return VGroup(*[iso.box(x0, y0, i * 0.46, 1.4, 1.4, 0.42, BAR3, BAR2, BAR1) for i in range(n)])


def pa_xmark(x, y, s=0.35, color=INK, w=9):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def pa_at(mob, x_left, y):
    """Place a text by its LEFT edge."""
    return mob.move_to([x_left + mob.width / 2, y, 0])


# ─────────────── B10 · three silent failures on one stage ───────────────
B10_S1 = Iso(-4.5, -1.3, 0.62)               # left: CPU block + a dark GPU beside it
B10_S2 = Iso(-0.2, -1.5, 0.62)               # centre: the wrong node (a CPU-only rack)
B10_S3 = Iso(3.9, -1.0, 0.75)                # right: the GPU you were given


def b10_stage1():
    cpu = pa_cpu(B10_S1)
    body, light = gpu_block(B10_S1, 2.6, 0.2)
    return cpu, body, light


def b10_tag():
    return Rectangle(width=1.0, height=0.42, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([4.05, -0.74, 0]).set_z_index(5)


class B10_SilentFailures(Scene):
    def construct(self):
        self.add(pa_title("I · Do You Have The GPU?"))
        until(self, "If the CUDA module", lead=0.5)
        cpu, body, light = b10_stage1()
        pa_slide_in(self, VGroup(cpu, body, light), RIGHT * 6.5, 0.6)
        self.add(T("CPU", 36).move_to([-4.9, -1.85, 0]), T("GPU", 36).move_to([-3.0, -1.0, 0]))
        until(self, "PyTorch runs on the CPU")
        pa_drop(self, [job_box(B10_S1, 0.35, 0.35, 0.92).set_z_index(2)], 0.5)
        until(self, "raises no error")
        ring = Circle(radius=0.3, color=GHOST, stroke_width=5).move_to(np.array(light.get_center()))   # no alarm: a ghost ring
        self.play(GrowFromCenter(ring), run_time=0.3)
        self.play(FadeOut(ring), run_time=0.3)
        until(self, "A typo", lead=0.4)
        pa_slide_in(self, pa_cpu(B10_S2, n=3), UP * 5.5, 0.6)
        until(self, "lands you on the wrong")
        pa_drop(self, [job_box(B10_S2, 0.35, 0.35, 1.38).set_z_index(2)], 0.5)
        self.add(T("wrong node", 36).move_to([-0.3, -2.05, 0]))
        until(self, "a leftover", lead=0.4)
        body3, light3 = gpu_block(B10_S3)
        light3.scale(1.4).set_color(TERRA)
        pa_slide_in(self, VGroup(body3, light3), LEFT * 4.2, 0.6)
        until(self, "can hide the card")
        tag = b10_tag()
        tag.shift(RIGHT * 4)
        self.add(tag)
        self.play(tag.animate.shift(LEFT * 4), run_time=0.6)
        self.add(M("CUDA_VISIBLE_DEVICES", 32).move_to([3.55, -2.0, 0]))
        done(self)


# ─────────────── B11 · the partition table (film 1's B40 approach, this film's columns) ───────────────
B11_ROWS = [("b200-devel", "B200", "192 GB", 192, "4 h", "interactive"),
            ("b200-batch", "B200", "192 GB", 192, "24 h", "production"),
            ("rtx-devel", "RTX", "96 GB", 96, "4 h", "interactive"),
            ("rtx-batch", "RTX", "96 GB", 96, "24 h", "production")]
B11_X = (-6.0, -2.75, -1.3, 1.95, 3.85)                              # left edge of each column
B11_BAR_X0, B11_BAR_UNIT = 0.45, 1.2 / 192                           # VRAM bar start, screen units per GB (192 GB = 1.2)
B11_PURPOSE_CX = 4.95                                                # purpose column centre ("production" spans 3.82–6.09)
B11_Y0, B11_DY = 1.3, 0.8                                            # first row centre, row pitch
B11_L, B11_R = -6.0, 6.0


def b11_at(mob, col, y):
    return mob.move_to([B11_X[col] + mob.width / 2, y, 0])


def b11_cell(fn, s, size, col, y):
    """A table cell set on a common baseline: typeset with a trailing 'bp' (one ascender, one descender) so every
    cell has the same vertical extent, then the two extra glyphs are dropped."""
    try:
        full = b11_at(fn(s + "bp", size), col, y)
        g = VGroup(*list(full)[:len(s.replace(" ", ""))])
        if len(g) == 0:
            raise ValueError
        return g
    except Exception:                                                # Gate A's stub has no glyphs: plain centre placement
        return b11_at(fn(s, size), col, y)


def b11_y(k):
    return B11_Y0 - k * B11_DY


def b11_name(k):
    name, gpu = B11_ROWS[k][0], B11_ROWS[k][1]
    return VGroup(b11_cell(M, name, 32, 0, b11_y(k)), b11_cell(T, gpu, 40, 1, b11_y(k)))


def b11_vram(k):
    return b11_cell(T, B11_ROWS[k][2], 40, 2, b11_y(k))


def b11_bar(k):
    w = B11_ROWS[k][3] * B11_BAR_UNIT
    return Rectangle(width=w, height=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B11_BAR_X0 + w / 2, b11_y(k), 0])


def b11_wall(k):
    return b11_cell(T, B11_ROWS[k][4], 40, 3, b11_y(k))


def b11_purpose(k):
    """Purpose cells are centred on a fixed x (Gate A's stub measures text widths differently)."""
    return T(B11_ROWS[k][5], 34).move_to([B11_PURPOSE_CX, b11_y(k), 0])


def b11_rule(k, color=BAR1, sw=3):
    """The rule under row k (k = -1 is the heavy rule under the header)."""
    y = b11_y(k) - B11_DY / 2
    return Line([B11_L, y, 0], [B11_R, y, 0], color=color, stroke_width=sw)


class B11_PartitionTable(Scene):
    def construct(self):
        hy = B11_Y0 + B11_DY + 0.05
        hb = lambda t, size: T(t, size, bold=True)
        head = VGroup(*[b11_cell(hb, t, 36, k, hy) for k, t in enumerate(("partition", "GPU", "VRAM", "walltime", "purpose"))])
        rules = [b11_rule(-1, INK, 5)] + [b11_rule(k) for k in range(3)] + [b11_rule(3, INK, 5)]
        until(self, "two GPU families", lead=0.7)
        self.play(FadeIn(head), run_time=0.4)
        self.play(LaggedStart(*[Create(r) for r in rules], lag_ratio=0.25), run_time=1.0)   # the frame splits into rows
        until(self, "B200 devel and B200 batch")
        self.play(FadeIn(b11_name(0), shift=RIGHT * 0.3), FadeIn(b11_name(1), shift=RIGHT * 0.3), run_time=0.45)
        until(self, "one hundred ninety-two")
        self.play(FadeIn(b11_vram(0)), FadeIn(b11_vram(1)), run_time=0.3)
        self.play(GrowFromEdge(b11_bar(0), LEFT), GrowFromEdge(b11_bar(1), LEFT), run_time=0.6)
        until(self, "RTX devel and RTX batch")
        self.play(FadeIn(b11_name(2), shift=RIGHT * 0.3), FadeIn(b11_name(3), shift=RIGHT * 0.3), run_time=0.45)
        until(self, "with ninety-six")
        self.play(FadeIn(b11_vram(2)), FadeIn(b11_vram(3)), run_time=0.3)
        self.play(GrowFromEdge(b11_bar(2), LEFT), GrowFromEdge(b11_bar(3), LEFT), run_time=0.4)
        until(self, "Devel partitions run four hours")
        self.play(FadeIn(b11_wall(0), shift=RIGHT * 0.2), FadeIn(b11_wall(2), shift=RIGHT * 0.2), run_time=0.4)
        until(self, "interactive work")
        self.play(FadeIn(b11_purpose(0), shift=RIGHT * 0.2), FadeIn(b11_purpose(2), shift=RIGHT * 0.2), run_time=0.4)
        until(self, "Batch partitions run twenty-four")
        self.play(FadeIn(b11_wall(1), shift=RIGHT * 0.2), FadeIn(b11_wall(3), shift=RIGHT * 0.2), run_time=0.4)
        until(self, "for production")
        self.play(FadeIn(b11_purpose(1), shift=RIGHT * 0.2), FadeIn(b11_purpose(3), shift=RIGHT * 0.2), run_time=0.4)
        done(self)


# ─────────────── B13 · 32G is CPU RAM; VRAM comes with the GPU; eight cores = seven workers + one main ───────────────
B13_L = Iso(-3.6, -0.9, 0.75)               # the CPU block, left
B13_R = Iso(2.4, -1.1, 0.75)                # the GPU block, right
B13_PAD_X = [-5.5 + 0.5 * k for k in range(8)]
B13_PAD_Y = -2.3


def b13_ram():
    return B13_L.box(0.1, 1.9, 0, 1.0, 1.0, 0.7)


def b13_vram():
    return B13_R.box(1.6, 0, 0, 1.8, 1.4, 0.4, DARK_TOP, DARK_L, DARK_R)


def b13_pad(k):
    return Square(side_length=0.36, fill_color=PA_PAD, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([B13_PAD_X[k], B13_PAD_Y, 0])


def b13_core(k, color=TERRA):
    return Dot([B13_PAD_X[k], B13_PAD_Y, 0], radius=0.09, color=color)


class B13_RamVsVram(Scene):
    def construct(self):
        cpu = pa_cpu(B13_L)
        body, light = gpu_block(B13_R, 0, 0.3)
        self.add(cpu, body, light, T("CPU", 36).move_to([-2.6, -1.5, 0]), T("GPU", 36).move_to([1.6, -1.6, 0]))
        until(self, "Mem equals", lead=0.4)
        pa_slide_in(self, b13_ram(), RIGHT * 4.5, 0.6)
        self.add(M("32G", 34).move_to([-4.8, 2.15, 0]), T("CPU RAM", 36).move_to([-4.8, 1.6, 0]))
        until(self, "The GPU's own memory", lead=0.4)
        pa_slide_in(self, b13_vram(), LEFT * 4.0, 0.6)
        self.add(T("VRAM", 36).move_to([5.4, -0.5, 0]))
        until(self, "And CPUs per task")
        pads = VGroup(*[b13_pad(k) for k in range(8)])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in pads], lag_ratio=0.12), run_time=0.8)
        until(self, "run on those cores")
        workers = VGroup(*[b13_core(k) for k in range(7)])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in workers], lag_ratio=0.12), run_time=0.7)
        self.add(T("7 workers", 36).move_to([-4.0, -2.95, 0]))
        until(self, "and one main process")
        self.play(GrowFromCenter(b13_core(7, INK)), run_time=0.3)
        self.add(T("1 main", 36).move_to([-2.0, -2.95, 0]))
        done(self)


# ─────────────── B14 · the verify script: five checks, then a tensor round trip CPU → GPU → CPU ───────────────
B14_CPU = Iso(1.3, -2.0, 0.65)
B14_GPU = Iso(4.6, -2.0, 0.65)
B14_ROW_Y = (2.0, 1.3, 0.6, -0.1, -0.8)
B14_BULLET_X, B14_TEXT_X = -5.85, -5.5
B14_A = np.array([1.3, -0.65, 0.0])        # tensor over the CPU top
B14_B = np.array([4.6, -1.05, 0.0])        # tensor over the GPU top


def b14_bullet(k):
    return Square(side_length=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B14_BULLET_X, B14_ROW_Y[k], 0])


def b14_row(k):
    y = B14_ROW_Y[k]
    if k == 0:
        lab = pa_at(T("CUDA reachable", 36), B14_TEXT_X, y)
    elif k == 1:
        lab = pa_at(T("GPUs · model · VRAM", 36), B14_TEXT_X, y)
    elif k == 2:
        lab = pa_at(M("CUDA_VISIBLE_DEVICES", 32), B14_TEXT_X, y)
    elif k == 3:
        cmd = pa_at(M("nvidia-smi", 32), B14_TEXT_X, y)
        lab = VGroup(cmd, pa_at(T("agrees", 36), B14_TEXT_X + cmd.width + 0.25, y - 0.09))   # serif descender: sit on the mono baseline
    else:
        lab = pa_at(T("round trip", 36), B14_TEXT_X, y)
    return VGroup(b14_bullet(k), lab)


def b14_cable():
    return Line([2.2, -0.95, 0], [3.9, -1.3, 0], color=PA_KRAFT, stroke_width=6)


def b14_tensor():
    return Iso(0, 0, 0.45).box(0, 0, 0, 0.6, 0.6, 0.5).move_to(B14_A).set_z_index(3)


class B14_VerifyFive(Scene):
    def construct(self):
        cpu = pa_cpu(B14_CPU)
        body, light = gpu_block(B14_GPU)
        light.scale(1.4).set_color(TERRA)
        self.add(pa_at(M("01_gpu_verify.py", 34), -5.9, 2.9), cpu, body, light, b14_cable(),
                 T("CPU", 36).move_to([1.3, -2.5, 0]), T("GPU", 36).move_to([4.6, -2.5, 0]))
        until(self, "Is CUDA reachable", lead=0.3)
        self.play(FadeIn(b14_row(0), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "How many GPUs", lead=0.3)
        self.play(FadeIn(b14_row(1), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "What CUDA visible", lead=0.3)
        self.play(FadeIn(b14_row(2), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "Does nvidia-smi agree", lead=0.3)
        self.play(FadeIn(b14_row(3), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "And a tensor round trip", lead=0.3)
        row4 = b14_row(4)
        self.play(FadeIn(row4, shift=RIGHT * 0.3), run_time=0.4)
        until(self, "CPU to GPU")
        tensor = b14_tensor()
        self.play(GrowFromCenter(tensor), run_time=0.3)
        self.play(MoveAlongPath(tensor, Line(B14_A, B14_B)), run_time=0.8)
        until(self, "and back")
        self.play(MoveAlongPath(tensor, Line(B14_B, B14_A)), run_time=0.8)
        until(self, "The round trip proves")
        tick = check(B14_BULLET_X, B14_ROW_Y[4], 0.2, TERRA, 8)
        self.play(FadeOut(row4[0]), Create(tick), run_time=0.4)
        done(self)


# ─────────────── B15 · CUDA_VISIBLE_DEVICES: =0 one GPU, =0,1 two, not set outside Slurm; never override ───────────────
B15_ROW_Y = (2.3, 1.1, -0.1)
B15_X0 = -6.0
B15_EQ_X = -0.07                              # where '=' falls in row 1 (rows 2 and 3 align under it)
B15_G1 = Iso(3.3, 1.95, 0.55)
B15_G2 = (Iso(3.0, 0.75, 0.55), Iso(4.4, 0.75, 0.55))


def b15_gpu(iso):
    body, light = gpu_block(iso)
    return body, light


def b15_shell():
    """A plain shell window: card panel, dark title strip, a prompt and a cursor block."""
    panel = Rectangle(width=2.6, height=1.1, fill_color=CARD, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([3.7, -0.1, 0])
    strip = Rectangle(width=2.6, height=0.28, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([3.7, 0.31, 0])
    prompt = M("$", 32).move_to([2.75, -0.22, 0])
    cur = Rectangle(width=0.18, height=0.34, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([3.1, -0.22, 0])
    return VGroup(panel, strip, prompt, cur)


class B15_VisibleDevices(Scene):
    def construct(self):
        until(self, "Slurm sets", lead=0.5)
        row1 = pa_at(M("CUDA_VISIBLE_DEVICES=0", 34), B15_X0, B15_ROW_Y[0])
        b1, l1 = b15_gpu(B15_G1)
        self.play(FadeIn(row1, shift=RIGHT * 0.3), run_time=0.4)
        pa_slide_in(self, VGroup(b1, l1), LEFT * 4.5, 0.5)
        until(self, "Zero means one GPU")
        self.play(l1.animate.scale(1.5).set_color(TERRA), run_time=0.35)
        until(self, "Zero comma one means two", lead=0.4)
        row2 = pa_at(M("=0,1", 34), B15_EQ_X, B15_ROW_Y[1])
        g2 = [b15_gpu(iso) for iso in B15_G2]
        self.play(FadeIn(row2, shift=RIGHT * 0.3), run_time=0.4)
        pa_slide_in(self, VGroup(*[VGroup(b, l) for b, l in g2]), LEFT * 5.0, 0.5)
        self.play(*[l.animate.scale(1.5).set_color(TERRA) for b, l in g2], run_time=0.35)
        until(self, "Not set means", lead=0.4)
        row3 = pa_at(M("NOT SET", 34), B15_EQ_X, B15_ROW_Y[2])
        self.play(FadeIn(row3, shift=RIGHT * 0.3), run_time=0.4)
        pa_slide_in(self, b15_shell(), LEFT * 4.5, 0.5)
        until(self, "which is normal")
        self.play(Create(check(5.45, -0.1, 0.2, INK, 7)), run_time=0.35)
        until(self, "Never override it", lead=0.4)
        line = pa_at(M("export CUDA_VISIBLE_DEVICES=...", 32), -4.6, -2.3)
        self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.4)
        until(self, "unless you deliberately", lead=0.6)
        self.play(Create(pa_xmark(-5.5, -2.3, 0.35, TERRA, 10)), run_time=0.35)
        done(self)


# ─────────────── B16 · idle is watched: utilization flat, job cancelled, GPU to the next in the queue (film 1's B43, re-paced) ───────────────
B16_GPU = Iso(3.7, -0.9, 1.5)
B16_Q1 = np.array([0.3, -2.8, 0.0])
B16_Q2 = np.array([-1.9, -2.8, 0.0])


def b16_axes():
    return VGroup(Line([-5.7, 0.7, 0], [0.9, 0.7, 0], color=BAR1, stroke_width=4),
                  Line([-5.7, 0.7, 0], [-5.7, 2.7, 0], color=BAR1, stroke_width=4))


def b16_glass(x, y):
    return VGroup(Circle(radius=0.4, color=INK, stroke_width=6).move_to([x, y, 0]),
                  Line([x + 0.29, y - 0.29, 0], [x + 0.62, y - 0.62, 0], color=INK, stroke_width=9)).set_z_index(4)


def b16_busy():
    """The next job's utilization: rises from the floor and runs high."""
    c = VMobject(color=INK, stroke_width=7)
    c.set_points_smoothly([np.array(p) for p in ([-5.7, 0.9, 0], [-4.9, 2.0, 0], [-4.0, 2.3, 0], [-3.0, 2.15, 0],
                                                 [-2.0, 2.35, 0], [-1.0, 2.2, 0], [0.0, 2.3, 0], [0.7, 2.22, 0])])
    return c


class B16_IdleCancel(Scene):
    def construct(self):
        axes = b16_axes()
        body, light = gpu_block(B16_GPU)
        light.scale(1.7).set_color(TERRA)
        job = job_box(B16_GPU, 0.15, 0.15, 0.5).set_z_index(2)
        q1 = job_box(Iso(0.3, -2.8, 1.5)).set_z_index(2)
        q2 = job_box(Iso(-1.9, -2.8, 1.5)).set_z_index(2)
        self.add(axes, body, light, job, q1, q2,
                 T("GPU utilization", 36).move_to([-3.6, 3.05, 0]), T("queue", 40).move_to([2.05, -2.3, 0]))
        hi = VMobject(color=INK, stroke_width=7)
        hi.set_points_smoothly([np.array(p) for p in ([-5.7, 2.2, 0], [-5.0, 2.36, 0], [-4.3, 2.14, 0], [-3.6, 2.32, 0], [-3.0, 2.2, 0])])
        lo = VMobject(color=INK, stroke_width=7)
        lo.set_points_as_corners([np.array(p) for p in ([-3.0, 2.2, 0], [-2.6, 0.8, 0], [0.7, 0.8, 0])])
        until(self, "A background process", lead=0.6)
        self.play(Create(hi), run_time=0.9)
        self.play(Create(lo), run_time=0.8)
        idle = T("idle", 40).move_to([-0.9, 1.8, 0])
        self.add(idle)
        until(self, "watches GPU utilization")
        glass = b16_glass(-4.6, 2.3)
        self.play(GrowFromCenter(glass), run_time=0.3)
        path = VMobject()
        path.set_points_as_corners([np.array(p) for p in ([-4.49, 2.19, 0], [-2.89, 2.09, 0], [-2.49, 0.69, 0], [-0.79, 0.69, 0])])
        self.play(MoveAlongPath(glass, path), run_time=1.2)
        until(self, "is cancelled")
        strike = VGroup(Line([3.2, 0.8, 0], [4.2, 1.7, 0], color=INK, stroke_width=9),
                        Line([3.2, 1.7, 0], [4.2, 0.8, 0], color=INK, stroke_width=9)).set_z_index(5)
        self.play(Create(strike), run_time=0.35)
        self.play(FadeOut(job, scale=0.7), FadeOut(strike, scale=0.7), light.animate.set_color(GHOST), run_time=0.5)
        gone = T("cancelled", 40).move_to([3.7, 2.6, 0])
        self.add(gone)
        until(self, "Run the verify script first")
        hop = np.array([3.7, 0.075, 0.0]) - B16_Q1
        self.play(q1.animate.shift(hop), q2.animate.shift(B16_Q1 - B16_Q2), FadeOut(gone), FadeOut(glass), run_time=0.9)
        self.play(light.animate.set_color(TERRA), run_time=0.3)
        until(self, "keep the batch partitions")
        self.play(FadeOut(hi), FadeOut(lo), FadeOut(idle), run_time=0.3)
        self.play(Create(b16_busy()), run_time=1.1)
        done(self)


# ─────────────── B20 · nvidia-smi live: the dark terminal, two numbers ringed ───────────────
B20_PX, B20_PY, B20_PW, B20_PH = 1.2, 0.05, 7.8, 4.5                 # the terminal panel (x −2.7 … 5.1)
B20_TX = -2.4                                                        # left edge of the mono text
B20_CMD_Y = 1.65
B20_ROW_Y = (0.9, 0.2, -0.5, -1.3)
B20_ROWS = ("GPU 0 NVIDIA B200", "52C 387W / 1000W", "84%")       # the memory row is set in two pieces (b20_mem_row)
B20_MEM_FIGS = "24576MiB / 196608MiB"


def b20_panel():
    panel = Rectangle(width=B20_PW, height=B20_PH, fill_color=PA_TERM, fill_opacity=1, stroke_width=0).move_to([B20_PX, B20_PY, 0])
    strip = Rectangle(width=B20_PW, height=0.32, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B20_PX, B20_PY + B20_PH / 2 - 0.16, 0])
    return VGroup(panel, strip)


def b20_text(s, y):
    return pa_at(M(s, 32, CARD), B20_TX, y)


def b20_ring_util():
    return Ellipse(width=1.5, height=0.85, color=CARD, stroke_width=6).move_to([B20_TX + 0.45, B20_ROW_Y[2], 0])


def b20_mem_row():
    """'Memory 24576MiB / 196608MiB' as two mono pieces, so the ring can enclose the figures without crossing a text box."""
    word = b20_text("Memory", B20_ROW_Y[3])
    figs = pa_at(M(B20_MEM_FIGS, 32, CARD), B20_TX + word.width + 0.6, B20_ROW_Y[3])   # a wide gap: the ring must clear 'Memory'
    return VGroup(word, figs)


def b20_ring_mem(figs):
    """Encloses the figures' box (corners inside the ellipse) without touching 'Memory' to its left."""
    return Ellipse(width=5.8, height=0.95, color=CARD, stroke_width=6).move_to(np.array(figs.get_center()))


def b20_track():
    return Rectangle(width=2.6, height=0.26, fill_color=PA_PAD, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=2).move_to([-4.4, -1.85, 0])


def b20_fill():
    w = 2.6 * 0.12
    return Rectangle(width=w, height=0.26, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.7 + w / 2, -1.85, 0])


class B20_NvidiaSmi(Scene):
    def construct(self):
        self.add(pa_title("II · Seeing The GPU Live"))
        until(self, "The fastest profiler", lead=0.2)
        pa_slide_in(self, b20_panel(), UP * 6.8, 0.7)
        until(self, "prints a snapshot", lead=0.5)
        self.play(FadeIn(b20_text("$ watch -n 1 nvidia-smi", B20_CMD_Y)), run_time=0.4)
        until(self, "watch it every second")
        mem = b20_mem_row()
        rows = [b20_text(s, y) for s, y in zip(B20_ROWS, B20_ROW_Y)] + [mem]
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=0.8)
        until(self, "eighty-four percent here")
        ring = b20_ring_util()
        self.play(Create(ring), run_time=0.5)
        self.add(T("utilization", 36).move_to([-4.4, B20_ROW_Y[2], 0]))
        until(self, "Below fifty")
        self.play(Indicate(ring, color=TERRA, scale_factor=1.15), run_time=0.6)
        until(self, "And memory", lead=0.3)
        ring2 = b20_ring_mem(mem[1])
        self.play(FadeOut(ring), run_time=0.2)
        self.play(Create(ring2), run_time=0.6)
        until(self, "Twelve percent")
        self.add(T("12% of VRAM", 36).move_to([-4.4, B20_ROW_Y[3], 0]))
        self.play(FadeIn(b20_track()), run_time=0.2)
        self.play(GrowFromEdge(b20_fill(), LEFT), run_time=0.5)
        done(self)
# ═════════════════════════════ PART B · B21 B22 B30 B31 B33 B40 B42 ═════════════════════════════
# Act II: B21 (two gauges), B22 (the two axes). Act III: B30 (the ladder, act title), B31 (devel → batch),
# B33 (reading a trace). Act IV: B40 (the factory, act title), B42 (45 and 9). Cast from _kit.py throughout.
PB_KRAFT = "#9C8462"      # deep kraft: rails, belt edges, connectors (ink joins the things it touches, GATE T)
PB_SMALL = "#917A55"      # dark kraft: outlines of SMALL objects only
PB_BELT = "#E4E0D4"       # belts stay within 28 of the stage (Gate V)
PB_DARK = "#1A1714"       # kernel blocks: darker than the kit faces so a packed row never fuses (GATE T)


def pb_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.0 + t.width / 2, 3.0, 0])


def pb_left(t, x, y):
    """Left-align a text at x (fixed numbers: Gate A's stub measures widths differently, so never chain on it)."""
    return t.move_to([x + t.width / 2, y, 0])


def pb_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes (edges dark kraft, never ink)."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PB_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PB_BELT, fill_opacity=1, stroke_color=PB_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def pb_slide_in(self, mob, vec, rt=0.7):
    """Slide a whole object in from off-stage, fully opaque (GATE T: never a half-faded dark block)."""
    rt = guard(self, rt)
    mob.shift(-vec)
    self.add(mob)
    self.play(mob.animate.shift(vec), run_time=rt)


def pb_drop(self, mobs, rt=0.55, lag=0.2, dist=5.0):
    """Objects drop in from above and land (quadratic ease-in)."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), run_time=rt, rate_func=ease_in)


def pb_cpu(iso):
    """A CPU block: two light slabs, no GPU light (the previous film's CPU-only section)."""
    return VGroup(*[iso.box(0, 0, i * 0.46, 1.4, 1.4, 0.42, BAR3, BAR2, BAR1) for i in range(2)])


# ─────────────── B21 · utilization 12 %, memory 91 %: loaded, full, starved ───────────────
B21_GX = (-4.7, -2.7)                       # gauge centres
B21_GY0, B21_GH, B21_GW = -1.9, 3.1, 0.9    # gauge bottom, height, width
B21_CPU = Iso(0.3, -1.95, 0.8)
B21_GPU = Iso(4.6, -1.95, 1.1)


def b21_tube(x):
    return RoundedRectangle(width=B21_GW, height=B21_GH, corner_radius=0.2, fill_color=CARD, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, B21_GY0 + B21_GH / 2, 0])


def b21_fill(x, pct):
    h = (B21_GH - 0.24) * pct / 100.0
    return Rectangle(width=B21_GW - 0.26, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x, B21_GY0 + 0.12 + h / 2, 0])


def b21_ghost():
    """An empty slot on the belt: a dashed grey outline where a batch should be."""
    return DashedVMobject(Square(side_length=0.5, stroke_color=BAR1, stroke_width=4), num_dashes=12).move_to([1.95, -1.0, 0])


class B21_TwoGauges(Scene):
    def construct(self):
        self.add(b21_tube(B21_GX[0]), b21_tube(B21_GX[1]),
                 T("utilization", 36).move_to([B21_GX[0], -2.4, 0]), T("memory", 36).move_to([B21_GX[1], -2.4, 0]))
        body, light = gpu_block(B21_GPU)
        light.scale(1.5)
        self.add(pb_cpu(B21_CPU), pb_belt(1.5, 3.55, -1.3), body, light,
                 T("CPU", 36).move_to([0.3, -2.55, 0]), T("GPU", 36).move_to([4.6, -2.55, 0]))
        until(self, "Utilization twelve")
        self.play(GrowFromEdge(b21_fill(B21_GX[0], 12), DOWN), run_time=0.45)
        self.play(FadeIn(T("12%", 52).move_to([B21_GX[0], 1.75, 0]), shift=UP * 0.2), run_time=0.3)
        until(self, "memory ninety-one")
        mem = b21_fill(B21_GX[1], 91)
        self.play(GrowFromEdge(mem, DOWN), run_time=0.8)
        self.play(FadeIn(T("91%", 52).move_to([B21_GX[1], 1.75, 0]), shift=UP * 0.2), run_time=0.3)
        until(self, "The model is loaded")
        pb_drop(self, [job_box(B21_GPU, 0.15, 0.15, 0.5).set_z_index(2)], 0.5, dist=3.5)
        until(self, "the card is full")
        self.play(Indicate(mem, color=None, scale_factor=1.06), run_time=0.5)
        until(self, "barely computing")
        self.play(light.animate.set_color(TERRA), run_time=0.15)                        # one flicker, then dark again
        self.play(light.animate.set_color(GHOST), run_time=0.15)
        until(self, "Nothing on the CPU side")
        slot = b21_ghost()
        self.play(FadeIn(slot), run_time=0.2)
        self.play(slot.animate.shift(RIGHT * 1.35), run_time=0.9, rate_func=linear)      # the empty belt runs
        self.play(FadeOut(slot), run_time=0.2)
        until(self, "That is data starvation")
        self.play(FadeIn(T("starved", 44).move_to([4.6, 1.3, 0]), shift=UP * 0.2), run_time=0.35)
        until(self, "gets its own act")
        ring = Circle(radius=1.4, color=TERRA, stroke_width=6).move_to([4.6, -0.75, 0])
        self.play(GrowFromCenter(ring), run_time=0.35)
        self.play(FadeOut(ring, scale=1.3), run_time=0.4)
        done(self)


# ─────────────── B22 · utilization across, memory up: four quadrants, one target ───────────────
B22_OX, B22_OY = -4.6, -2.7                 # axes origin
B22_XM, B22_YM = 0.4, 0.05                  # grid midlines
B22_XE, B22_YE = 5.5, 2.7                   # axis ends
B22_CX, B22_CY = (-2.1, 2.95), (-1.3, 1.35)  # quadrant centres (left, right), (bottom, top)


def b22_axes():
    return VGroup(Arrow([B22_OX, B22_OY, 0], [B22_XE, B22_OY, 0], color=INK, stroke_width=5, buff=0),
                  Arrow([B22_OX, B22_OY, 0], [B22_OX, B22_YE, 0], color=INK, stroke_width=5, buff=0))


def b22_grid():
    return VGroup(Line([B22_XM, B22_OY + 0.1, 0], [B22_XM, B22_YE - 0.3, 0], color=BAR2, stroke_width=3),
                  Line([B22_OX + 0.1, B22_YM, 0], [B22_XE - 0.3, B22_YM, 0], color=BAR2, stroke_width=3))


def b22_mini(cx, cy, lit, job):
    """A GPU card miniature: dark block, light (ghost or terracotta), and a job box of size `job` (0 = none)."""
    iso = Iso(cx - 0.2, cy - 1.0, 0.75)
    body, light = gpu_block(iso)
    light.scale(1.3)
    if lit:
        light.set_color(TERRA)
    g = VGroup(body, light)
    if job:
        g.add(job_box(iso, 0.5 - job / 2, 0.5 - job / 2, 0.5, s=job).set_z_index(2))
    return g


class B22_TwoAxes(Scene):
    def construct(self):
        self.add(b22_grid())
        until(self, "two axes")
        axes = b22_axes()
        self.play(GrowArrow(axes[0]), GrowArrow(axes[1]), run_time=0.7)
        until(self, "Across: utilization")
        self.play(FadeIn(T("utilization", 36).move_to([0.4, -3.05, 0])), run_time=0.35)
        until(self, "Up: memory")
        self.play(FadeIn(T("memory", 34).move_to([-4.6, 3.02, 0])), run_time=0.35)
        until(self, "Top left is")
        pb_drop(self, [b22_mini(B22_CX[0], B22_CY[1], False, 0.7)], 0.5, dist=3.0)
        until(self, "a data pipeline problem", lead=0.4)
        self.play(FadeIn(T("pipeline", 38).move_to([-0.4, B22_CY[1], 0])), run_time=0.3)
        until(self, "Bottom left is")
        pb_drop(self, [b22_mini(B22_CX[0], B22_CY[0], False, 0)], 0.5, dist=3.0)
        self.play(FadeIn(T("nothing", 38).move_to([-0.4, B22_CY[0], 0])), run_time=0.3)
        until(self, "Bottom right is")
        pb_drop(self, [b22_mini(B22_CX[1], B22_CY[0], True, 0.4)], 0.5, dist=3.0)
        self.play(FadeIn(T("headroom", 38).move_to([4.75, B22_CY[0], 0])), run_time=0.3)
        until(self, "Top right is")
        pb_drop(self, [b22_mini(B22_CX[1], B22_CY[1], True, 0.7)], 0.5, dist=3.0)
        ring = Circle(radius=1.12, color=TERRA, stroke_width=6).move_to([B22_CX[1] - 0.2, B22_CY[1] - 0.2, 0])
        self.play(GrowFromCenter(ring), FadeIn(T("target", 38).move_to([4.75, B22_CY[1], 0])), run_time=0.4)
        until(self, "Eighty to a hundred")
        self.play(FadeIn(T("80–100%", 36).move_to([4.2, -3.05, 0]), shift=UP * 0.2), run_time=0.35)
        until(self, "seventy to ninety")
        self.play(FadeIn(T("70–90%", 36).move_to([-5.4, 1.65, 0]), shift=UP * 0.2), run_time=0.35)
        done(self)


# ─────────────── B30 · four rungs: system, framework, timeline, kernel ───────────────
B30_RAIL = (-4.7, -1.9)
B30_Y = (-2.3, -0.9, 0.5, 1.9)
B30_LAYERS = (("system", "nvidia-smi, nvitop", "busy?"), ("framework", "PyTorch Profiler", "which?"),
              ("timeline", "nsys", "order?"), ("kernel", "ncu", "bound?"))
B30_GLASS_X = -5.6


def b30_rails():
    return VGroup(*[Line([x, -2.9, 0], [x, 2.5, 0], color=PB_KRAFT, stroke_width=8) for x in B30_RAIL])


def b30_rung(k):
    return Rectangle(width=B30_RAIL[1] - B30_RAIL[0], height=0.5, fill_color=BAR2, fill_opacity=1,
                     stroke_color=PB_SMALL, stroke_width=3).move_to([(B30_RAIL[0] + B30_RAIL[1]) / 2, B30_Y[k], 0])


def b30_labels(k):
    layer, tool, q = B30_LAYERS[k]
    y = B30_Y[k]
    return (pb_left(T(layer, 40), -1.4, y + 0.3), pb_left(M(tool, 32) if k != 1 else T(tool, 34), -1.4, y - 0.3),
            T(q, 40).move_to([4.5, y, 0]))


def b30_glass(y):
    return VGroup(Circle(radius=0.36, color=INK, stroke_width=6).move_to([B30_GLASS_X, y, 0]),
                  Line([B30_GLASS_X + 0.26, y - 0.26, 0], [B30_GLASS_X + 0.56, y - 0.56, 0], color=INK, stroke_width=9)).set_z_index(4)


class B30_FourLayers(Scene):
    def construct(self):
        self.add(pb_title("III · The Profiling Toolchain"))
        body, light = gpu_block(Iso(4.5, 0.9, 0.9))
        light.scale(1.5).set_color(TERRA)
        self.add(body, light)
        until(self, "there's a problem")
        self.play(light.animate.set_color(GHOST), run_time=0.2)                           # nvidia-smi: the light goes out
        self.play(light.animate.set_color(TERRA), run_time=0.2)
        until(self, "where the time goes", lead=0.5)
        glass = b30_glass(B30_Y[0])
        self.play(GrowFromCenter(glass), run_time=0.35)
        until(self, "There are layers")
        self.play(Create(b30_rails()), FadeOut(VGroup(body, light)), run_time=0.6)
        cues = (("System level", "NVIDIA S M I and N V I top", "Is the GPU busy"),
                ("Framework level", "the PyTorch profiler", "Which operator"),
                ("Timeline: N-sight", "N-sight Systems", "in order"),
                ("And kernel level", "N-sight Compute", "memory-bound"))
        for k in range(4):
            layer, tool, q = b30_labels(k)
            until(self, cues[k][0])
            anims = [GrowFromEdge(b30_rung(k), LEFT), FadeIn(layer)]
            if k:
                anims.append(glass.animate.shift(UP * (B30_Y[k] - B30_Y[k - 1])))
            self.play(*anims, run_time=0.5)
            until(self, cues[k][1])
            self.play(FadeIn(tool, shift=RIGHT * 0.2), run_time=0.3)
            until(self, cues[k][2])
            self.play(FadeIn(q, shift=UP * 0.15), run_time=0.3)
        until(self, "first two rungs", lead=0.4)
        marks = VGroup(*[Dot([B30_GLASS_X, B30_Y[k], 0], radius=0.12, color=TERRA) for k in (0, 1)])
        self.play(FadeOut(glass), run_time=0.25)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.4), run_time=0.45)
        done(self)


# ─────────────── B31 · profile in devel, run production in batch ───────────────
B31_L = Iso(-1.7, -2.05, 1.0)               # the devel GPU
B31_R = Iso(3.9, -2.05, 1.0)                # the batch GPU
B31_RIDE = 5.6
B31_STEPS = ("verify", "50–100 steps", "profile", "fix", "re-profile", "> 70%")
B31_SX, B31_SY0, B31_SDY = -4.7, 1.7, 0.72


def b31_step(k):
    y = B31_SY0 - k * B31_SDY
    return VGroup(pill(B31_SX, y, 2.6, 0.56, CARD), T(B31_STEPS[k], 34).move_to([B31_SX, y, 0]))


def b31_job(iso):
    return job_box(iso, 0.15, 0.15, 0.5).set_z_index(3)


class B31_DevelToBatch(Scene):
    def construct(self):
        lb, ll = gpu_block(B31_L)
        rb, rl = gpu_block(B31_R)
        ll.scale(1.5); rl.scale(1.5)
        self.add(pb_belt(-0.7, 3.0, -1.95), lb, ll, rb, rl,
                 M("b200-devel · srun", 32).move_to([-3.3, 2.75, 0]), M("b200-batch · sbatch", 32).move_to([3.3, 2.75, 0]),
                 DashedLine([0.95, 2.35, 0], [0.95, -1.0, 0], color=BAR2, stroke_width=3, dash_length=0.2))
        until(self, "In a B200 devel session")
        job = b31_job(B31_L)
        pb_drop(self, [job], 0.5, dist=3.5)
        self.play(ll.animate.set_color(TERRA), run_time=0.2)
        cues = ("the verify script", "fifty to a hundred steps", "profile,", "fix the bottleneck", "profile again", "above seventy percent")
        for k in range(6):
            until(self, cues[k], lead=0.35)
            pb_drop(self, [b31_step(k)], 0.45, dist=4.0)
        self.play(Create(check(-3.05, B31_SY0 - 5 * B31_SDY, 0.2, TERRA, 8)), run_time=0.3)
        until(self, "Only then does the job go", lead=0.1)
        self.play(ll.animate.set_color(GHOST), run_time=0.2)
        self.play(job.animate.shift(RIGHT * B31_RIDE), run_time=1.1)                       # across the belt to batch
        self.play(rl.animate.set_color(TERRA), run_time=0.2)
        pb_drop(self, [VGroup(pill(4.6, 1.7, 2.0, 0.56, CARD), T("run", 34).move_to([4.6, 1.7, 0]))], 0.45, dist=4.0)
        until(self, "read jobstats", lead=0.4)
        self.play(rl.animate.set_color(GHOST), run_time=0.2)                                # it finishes
        self.play(FadeIn(M("jobstats", 34).move_to([4.6, 0.98, 0]), shift=UP * 0.2), run_time=0.35)
        done(self)


# ─────────────── B33 · reading the trace: gaps, copies, CPU vs CUDA, DataLoader on top ───────────────
B33_TY = 2.2
B33_KERN = ((-5.4, -3.6), (-3.1, -1.0), (-0.3, 2.3), (3.0, 5.4))     # kernel spans; the gaps between them are the point
B33_ROWS = (-1.95, -2.45, -2.95)


def b33_kernels():
    return VGroup(*[Rectangle(width=x1 - x0, height=0.5, fill_color=PB_DARK, fill_opacity=1, stroke_width=0)
                    .move_to([(x0 + x1) / 2, B33_TY, 0]) for x0, x1 in B33_KERN])


def b33_rings():
    return VGroup(*[Circle(radius=0.5, color=TERRA, stroke_width=5).move_to([(B33_KERN[k][1] + B33_KERN[k + 1][0]) / 2, B33_TY, 0])
                    for k in range(3)])


def b33_bar(x0, x1, y, fill):
    return Rectangle(width=x1 - x0, height=0.45, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([(x0 + x1) / 2, y, 0])


def b33_row(k, fill):
    return pill(0.0, B33_ROWS[k], 4.0, 0.36, fill)


class B33_ReadTheTrace(Scene):
    def construct(self):
        self.add(Line([-5.6, B33_TY - 0.4, 0], [5.6, B33_TY - 0.4, 0], color=BAR1, stroke_width=3))
        kern = b33_kernels()
        self.play(LaggedStart(*[GrowFromEdge(k, LEFT) for k in kern], lag_ratio=0.3), run_time=0.9)
        until(self, "Gaps between kernels", lead=0.1)
        rings = b33_rings()
        self.play(LaggedStart(*[GrowFromCenter(r) for r in rings], lag_ratio=0.3), run_time=0.6)
        self.play(FadeIn(T("idle", 38).move_to([-0.65, 3.05, 0])), run_time=0.3)
        until(self, "Large copy entries")
        self.add(M("aten::copy_", 32).move_to([-4.6, 0.9, 0]))
        self.play(GrowFromEdge(b33_bar(-2.9, 4.6, 0.9, BAR1), LEFT), run_time=1.0)
        until(self, "CPU total far above", lead=0.1)
        self.add(T("CPU total", 36).move_to([-4.9, -0.3, 0]), T("CUDA total", 36).move_to([-4.8, -1.0, 0]))
        self.play(GrowFromEdge(b33_bar(-3.4, 5.0, -0.3, BAR1), LEFT), GrowFromEdge(b33_bar(-3.4, -1.6, -1.0, BAR2), LEFT), run_time=0.9)
        until(self, "And DataLoader functions", lead=0.1)
        r1, r2 = b33_row(0, BAR2), b33_row(1, BAR3)
        dl = VGroup(b33_row(2, CARD), M("DataLoader", 32).move_to([0.0, B33_ROWS[2], 0])).set_z_index(2)
        self.play(FadeIn(r1), FadeIn(r2), FadeIn(dl), FadeIn(T("CPU table", 36).move_to([3.4, B33_ROWS[0], 0])), run_time=0.4)
        until(self, "at the top of the CPU table", lead=0.1)
        self.play(dl.animate.shift(UP * (B33_ROWS[0] - B33_ROWS[2])), r1.animate.shift(DOWN * 0.5), r2.animate.shift(DOWN * 0.5), run_time=0.6)
        done(self)


# ─────────────── B40 · the factory (B200) and the supply truck (the loader) ───────────────
B40_I = Iso(0.6, -1.9, 1.0)
B40_TRUCK_X0, B40_TRUCK_Y = -5.5, -1.55


def b40_machine():
    """The dark press: body, two posts, a crossbar; the ram is separate (it moves)."""
    i = B40_I
    body = i.box(2.2, 0.0, 0.0, 2.0, 1.8, 0.9, DARK_TOP, DARK_L, DARK_R)
    posts = VGroup(i.box(2.6, 1.4, 0.9, 0.25, 0.25, 0.8, DARK_TOP, DARK_L, DARK_R),
                   i.box(3.8, 1.4, 0.9, 0.25, 0.25, 0.8, DARK_TOP, DARK_L, DARK_R))
    bar = i.box(2.6, 1.4, 1.7, 1.45, 0.25, 0.18, DARK_TOP, DARK_L, DARK_R)
    light = Dot(i.p(2.55, 0.0, 0.55), radius=0.11, color=TERRA).set_z_index(2)
    return VGroup(body, posts, bar), light


def b40_ram():
    return B40_I.box(2.95, 0.65, 1.25, 0.6, 0.6, 0.4, BAR3, BAR2, BAR1, sw=3).set_z_index(3)


def b40_truck(ox):
    """A kraft truck: bed, cab, three wheels, '50 ms' riding above it."""
    i = Iso(ox, B40_TRUCK_Y, 0.8)
    bed = i.box(0.0, 0.0, 0.22, 1.3, 0.7, 0.5)
    cab = i.box(1.3, 0.0, 0.22, 0.45, 0.7, 0.68)
    wheels = VGroup(*[Dot(i.p(x, 0.0, 0.1), radius=0.13, color=DARK_L) for x in (0.3, 1.1, 1.58)])
    return VGroup(wheels, bed, cab, T("50 ms", 46).move_to([ox + 0.4, 0.55, 0])).set_z_index(1)


class B40_Factory(Scene):
    def construct(self):
        self.add(pb_title("IV · Data Starvation"), pb_belt(-5.8, 0.55, -1.4))
        until(self, "Picture a high-speed factory", lead=0.5)
        machine, light = b40_machine()
        ram = b40_ram()
        pb_slide_in(self, VGroup(machine, light, ram), LEFT * 6.5, 0.7)
        until(self, "It finishes a batch", lead=0.1)
        for _ in range(2):                                                               # two quick stamps
            self.play(ram.animate.shift(B40_I.v(0, 0, -0.35)), run_time=0.18, rate_func=ease_in)
            self.play(ram.animate.shift(B40_I.v(0, 0, 0.35)), run_time=0.18)
        self.play(FadeIn(T("8 ms", 46).move_to([5.3, 0.6, 0]), shift=UP * 0.2), run_time=0.3)
        until(self, "The supply truck", lead=0.1)
        truck = b40_truck(B40_TRUCK_X0)
        pb_slide_in(self, truck, RIGHT * 2.2, 0.6)
        until(self, "takes fifty milliseconds", lead=0.1)
        self.play(truck.animate.shift(RIGHT * 1.6), run_time=1.5, rate_func=linear)      # it crawls
        until(self, "The factory stops and waits")
        self.play(light.animate.set_color(GHOST), run_time=0.3)                          # light off, ram held up
        until(self, "Nothing is wrong with the factory", lead=0.1)
        self.play(Indicate(VGroup(machine, ram), color=None, scale_factor=1.04), run_time=0.6)
        until(self, "The supply chain", lead=0.1)
        self.play(truck.animate.shift(RIGHT * 1.5), run_time=1.5, rate_func=linear)      # still crawling
        until(self, "And a B200 eats batches", lead=0.1)
        self.play(ram.animate.shift(B40_I.v(0, 0, -0.35)), run_time=0.18, rate_func=ease_in)   # one more stamp on nothing
        self.play(ram.animate.shift(B40_I.v(0, 0, 0.35)), run_time=0.18)
        until(self, "will starve it here", lead=0.5)
        self.play(truck.animate.shift(RIGHT * 0.8), run_time=0.8, rate_func=linear)
        self.play(FadeIn(T("waiting", 44).move_to([-0.3, 2.4, 0]), shift=UP * 0.2), run_time=0.35)
        done(self)


# ─────────────── B42 · loader 45 ms, compute 9 ms: 36 ms of waiting, 80 % ───────────────
B42_X0, B42_U = -5.2, 0.2                   # t = 0 on screen, screen units per millisecond
B42_YC, B42_YL, B42_YA = 1.3, -0.45, -1.1   # compute row, loader row, time axis


def b42_x(ms):
    return B42_X0 + B42_U * ms


def b42_compute():
    return Rectangle(width=b42_x(9) - b42_x(0), height=0.7, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to([b42_x(4.5), B42_YC, 0])


def b42_loader():
    return Rectangle(width=b42_x(45) - b42_x(0), height=0.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([b42_x(22.5), B42_YL, 0])


def b42_wait():
    """The waiting span: a pale grey block with grey hatching, from 9 to 45."""
    x0, x1 = b42_x(9) + 0.08, b42_x(45)
    block = Rectangle(width=x1 - x0, height=0.7, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([(x0 + x1) / 2, B42_YC, 0])
    hatch = VGroup()
    x = x0 + 0.2
    while x + 0.45 < x1:
        hatch.add(Line([x, B42_YC - 0.3, 0], [x + 0.45, B42_YC + 0.3, 0], color=BAR1, stroke_width=3))
        x += 0.42
    return VGroup(block, hatch)


def b42_tick(ms, label):
    return VGroup(Line([b42_x(ms), B42_YA - 0.1, 0], [b42_x(ms), B42_YA + 0.1, 0], color=INK, stroke_width=4),
                  T(label, 34).move_to([b42_x(ms), B42_YA - 0.45, 0]))


class B42_FortyFiveNine(Scene):
    def construct(self):
        self.add(Line([b42_x(0), B42_YA, 0], [b42_x(45) + 0.5, B42_YA, 0], color=BAR1, stroke_width=4), b42_tick(0, "0"))
        until(self, "loader forty-five", lead=0.3)
        self.play(GrowFromEdge(b42_loader(), LEFT), FadeIn(b42_tick(45, "45")), run_time=0.9)
        self.play(FadeIn(T("loader 45 ms", 38).move_to([-3.95, 0.42, 0])), run_time=0.3)
        until(self, "compute nine", lead=0.1)
        comp = b42_compute()
        self.play(GrowFromEdge(comp, LEFT), FadeIn(b42_tick(9, "9")), run_time=0.4)
        self.play(FadeIn(T("compute 9 ms", 38).move_to([-4.05, 2.05, 0])), run_time=0.3)
        until(self, "works for nine")
        self.play(Indicate(comp, color=None, scale_factor=1.08), run_time=0.4)
        until(self, "waits for thirty-six", lead=0.1)
        self.play(GrowFromEdge(b42_wait(), LEFT), run_time=0.8)
        self.play(FadeIn(T("36 ms waiting", 38).move_to([1.1, 2.05, 0])), run_time=0.3)
        until(self, "Eighty percent", lead=0.1)
        self.play(FadeIn(T("80%", 120).move_to([0.6, -2.55, 0]), scale=0.7), run_time=0.5)
        done(self)
# ═════════════════════════════ PART C · B44 · Act V (B50 B51 B52 B54 B55) · B60 ═════════════════════════════
# Gauges are the recurring picture of this part: a half-dial (0 at the left, 100 at the right, upper half) for the
# big meters, and a small round dial with a dark-kraft ring for icons (GATE T: small ink rings fuse with their pointer).
PC_SMALL = "#917A55"                         # dark kraft: outlines of SMALL objects only
PC_KRAFT = "#9C8462"                         # deep kraft: cables and connectors (ink cables fuse what they join)
PC_GTOP, PC_GL, PC_GR = "#A8A29B", "#9A938C", "#918A83"   # a block that has gone BF16 grey (all above GATE T's grey-120 floor)


def pc_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pc_left(mob, x, y):
    """Left-align a label at x (fixed numbers: Gate A's stub measures text differently)."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pc_ang(frac):
    return PI * (1.0 - frac)


def pc_pt(c, r, frac):
    a = pc_ang(frac)
    return np.array([c[0] + r * np.cos(a), c[1] + r * np.sin(a), 0.0])


def pc_gauge(c, r, sw=6, ticks=(0.0, 0.25, 0.5, 0.75, 1.0)):
    """A big half-dial: open ink arc from 0 (left) to 100 (right), tick marks, a pivot."""
    arc = Arc(radius=r, start_angle=PI, angle=-PI, arc_center=np.array([c[0], c[1], 0.0]), color=INK, stroke_width=sw)
    tk = VGroup(*[Line(pc_pt(c, r - 0.16, f), pc_pt(c, r + 0.16, f), color=INK, stroke_width=sw - 1) for f in ticks])
    pivot = Dot(np.array([c[0], c[1], 0.0]), radius=0.11, color=INK)
    return VGroup(arc, tk, pivot)


def pc_needle(c, r, frac, sw=8):
    return Line(np.array([c[0], c[1], 0.0]), pc_pt(c, r * 0.82, frac), color=INK, stroke_width=sw).set_z_index(3)


def pc_turn(needle, c, f0, f1):
    """The animation that swings a needle from reading f0 to reading f1."""
    return Rotate(needle, angle=-(f1 - f0) * PI, about_point=np.array([c[0], c[1], 0.0]))


def pc_dial(c, r=0.3, frac=0.15, sw=3):
    """A small round dial: white face, dark-kraft ring, ink needle (index 1), ink pin."""
    face = Circle(radius=r, stroke_color=PC_SMALL, stroke_width=sw, fill_color=PAGE_TOP, fill_opacity=1).move_to(np.array([c[0], c[1], 0.0]))
    needle = Line(np.array([c[0], c[1], 0.0]), pc_pt(c, r * 0.72, frac), color=INK, stroke_width=4)
    pin = Dot(np.array([c[0], c[1], 0.0]), radius=0.045, color=INK)
    return VGroup(face, needle, pin)


def pc_cross(x, y, s=0.2, w=7):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


# ─────────────── B44 · four dials land with their start values; num_workers 0 → 4 lifts utilization 20% → 60–80% ───────────────
B44_Y = (2.1, 0.8, -0.5, -1.8)
B44_NAMES = ("num_workers", "pin_memory", "persistent_workers", "prefetch_factor")
B44_VALS = ("cpus-1", "True", "True", "2")
B44_FRAC = (0.0, 0.9, 0.9, 0.3)                       # dial readings; num_workers starts at the PyTorch default, zero
B44_DX = -5.3                                          # dial centres
B44_BAR_X, B44_BAR_W, B44_BAR_Y0, B44_BAR_H = 3.9, 0.8, -2.6, 4.9


def b44_row(k):
    y = B44_Y[k]
    dial = pc_dial((B44_DX, y), r=0.5, frac=B44_FRAC[k], sw=4)
    name = pc_left(M(B44_NAMES[k], 32), -4.5, y)
    val = pc_left(M(B44_VALS[k], 36), 0.5, y)
    return VGroup(dial, name, val)


def b44_fill(frac):
    h = B44_BAR_H * frac - 0.16
    return Rectangle(width=B44_BAR_W - 0.16, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B44_BAR_X, B44_BAR_Y0 + 0.08 + h / 2, 0])


def b44_pct(s, frac):
    return T(s, 36).move_to([5.25, B44_BAR_Y0 + B44_BAR_H * frac - 0.08, 0])


class B44_FourKnobs(Scene):
    def construct(self):
        rows = [b44_row(k) for k in range(4)]
        until(self, "Workers")
        self.play(FadeIn(rows[0], shift=DOWN * 0.5), run_time=0.45)
        until(self, "Pin memory")
        self.play(FadeIn(rows[1], shift=DOWN * 0.5), run_time=0.45)
        until(self, "Persistent workers")
        self.play(FadeIn(rows[2], shift=DOWN * 0.5), run_time=0.45)
        until(self, "Prefetch")
        self.play(FadeIn(rows[3], shift=DOWN * 0.5), run_time=0.45)
        until(self, "The single biggest win")
        bar = Rectangle(width=B44_BAR_W, height=B44_BAR_H, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([B44_BAR_X, B44_BAR_Y0 + B44_BAR_H / 2, 0])
        fill = b44_fill(0.2)
        lab = M("num_workers=0", 32).move_to([B44_BAR_X, -3.0, 0])
        self.play(Create(bar), run_time=0.5)
        self.play(GrowFromEdge(fill, DOWN), FadeIn(lab), FadeIn(b44_pct("20%", 0.2)), run_time=0.5)
        self.add(T("utilization", 36).move_to([B44_BAR_X, 2.65, 0]))
        until(self, "from zero")
        needle = rows[0][0][1]
        self.play(pc_turn(needle, (B44_DX, B44_Y[0]), 0.0, 0.4), run_time=0.6)
        until(self, "to four or more")
        lab4 = M("num_workers=4", 32).move_to([B44_BAR_X, -3.0, 0])
        self.play(FadeOut(lab), FadeIn(lab4), run_time=0.3)
        until(self, "That alone often takes a job")
        self.play(Transform(fill, b44_fill(0.7)), run_time=0.9)
        self.play(FadeIn(b44_pct("60–80%", 0.7)), run_time=0.3)
        done(self)


# ─────────────── B50 · two meters that mean different things: utilization sweeps to 100 (fine); memory climbs to the OOM edge ───────────────
B50_L, B50_R, B50_RAD = (-3.1, -0.4), (3.1, -0.4), 2.0


def b50_ends(c):
    return VGroup(T("0", 32).move_to([c[0] - B50_RAD - 0.35, -0.85, 0]), T("100%", 32).move_to([c[0] + B50_RAD + 0.35, -0.85, 0]))


class B50_TwoMeters(Scene):
    def construct(self):
        self.add(pc_title("V · Memory vs Utilization"))
        gl, gr = pc_gauge(B50_L, B50_RAD), pc_gauge(B50_R, B50_RAD)
        self.play(Create(gl), Create(gr), run_time=0.8)
        self.add(b50_ends(B50_L), b50_ends(B50_R))
        until(self, "Utilization")
        nl = pc_needle(B50_L, B50_RAD, 0.05, sw=10).set_color(BAR1)   # grey: GATE T read an ink needle along the arc base as a second text run
        self.play(FadeIn(T("utilization", 44).move_to([-3.1, -1.5, 0])), FadeIn(nl), run_time=0.4)
        until(self, "the share of the last second")
        self.play(pc_turn(nl, B50_L, 0.05, 0.55), run_time=0.7)
        until(self, "Low means idle")
        self.play(pc_turn(nl, B50_L, 0.55, 0.12), run_time=0.5)
        until(self, "A hundred percent sustained")
        self.play(pc_turn(nl, B50_L, 0.12, 1.0), run_time=0.9)
        self.play(Create(check(-3.1, 0.55, 0.3, TERRA, 9)), run_time=0.35)
        until(self, "Memory")
        nr = pc_needle(B50_R, B50_RAD, 0.05, sw=10).set_color(BAR1)
        self.play(FadeIn(T("memory", 44).move_to([3.1, -1.5, 0])), FadeIn(nr), run_time=0.4)
        until(self, "the share of VRAM")
        self.play(pc_turn(nr, B50_R, 0.05, 0.45), pc_turn(nl, B50_L, 1.0, 0.9), run_time=0.7)      # independent needles
        until(self, "Low means you could hold")
        self.play(pc_turn(nr, B50_R, 0.45, 0.2), run_time=0.5)
        until(self, "High is only bad near the edge")
        self.play(pc_turn(nr, B50_R, 0.2, 0.97), pc_turn(nl, B50_L, 0.9, 1.0), run_time=0.9)
        until(self, "runs out of memory")
        oom = Dot(pc_pt(B50_R, B50_RAD + 0.32, 1.0), radius=0.15, color=TERRA)
        self.play(GrowFromCenter(oom), run_time=0.3)
        self.add(T("OOM", 36).move_to([5.5, 0.25, 0]))
        done(self)


# ─────────────── B51 · read the pair: five rows, gauge icons for what you see, a cause, a first thing to try ───────────────
B51_Y = (1.5, 0.55, -0.4, -1.35, -2.3)
B51_HY = 2.85
B51_UX, B51_MX = -5.25, -4.45                           # the two icon columns (utilization, memory)
B51_C2, B51_C3 = -3.1, 1.9                              # left edges of the word columns
B51_LO, B51_HI = 0.15, 0.85
B51_ROWS = [((B51_LO, B51_LO), "GPU doing nothing", "verify CUDA"),
            ((B51_LO, B51_HI), "loaded, not running", "fix the pipeline"),
            ((B51_HI, B51_LO), "healthy, VRAM unused", "increase batch size"),
            ((B51_HI, B51_HI), "good shape", None),
            ((B51_LO, 1.02), "out of memory", "mixed precision")]


def b51_rule(y, color=BAR1, sw=3):
    return Line([-6.0, y, 0], [6.0, y, 0], color=color, stroke_width=sw)


def b51_row(k):
    (fu, fm), cause, fix = B51_ROWS[k]
    y = B51_Y[k]
    icons = VGroup(pc_dial((B51_UX, y), 0.3, fu), pc_dial((B51_MX, y), 0.3, fm))
    if k == 4:
        icons.add(Dot([B51_MX + 0.46, y, 0], radius=0.09, color=TERRA))      # the OOM edge, as in B50
    words = VGroup(pc_left(T(cause, 36), B51_C2, y))
    if fix is None:
        words.add(check(B51_C3 + 0.3, y, 0.2, INK, 6))
    else:
        words.add(pc_left(T(fix, 36), B51_C3, y))
    return icons, words


class B51_DecisionTable(Scene):
    def construct(self):
        head = VGroup(T("what you see", 36, bold=True).move_to([-4.8, B51_HY, 0]),
                      pc_left(T("likely cause", 36, bold=True), B51_C2, B51_HY),
                      pc_left(T("first thing to try", 36, bold=True), B51_C3, B51_HY),
                      T("util", 32).move_to([B51_UX, 2.25, 0]), T("mem", 32).move_to([B51_MX, 2.25, 0]))
        rules = VGroup(b51_rule(1.95, INK, 5), *[b51_rule(B51_Y[k] - 0.475) for k in range(4)], b51_rule(-2.775, INK, 5))
        self.add(head, rules)
        mark = Dot([-5.8, B51_Y[0], 0], radius=0.1, color=TERRA)
        until(self, "Low and low")
        ic, wd = b51_row(0)
        self.play(GrowFromCenter(ic), FadeIn(wd, shift=RIGHT * 0.3), GrowFromCenter(mark), run_time=0.5)
        until(self, "Low utilization, high memory")
        ic, wd = b51_row(1)
        self.play(GrowFromCenter(ic), FadeIn(wd, shift=RIGHT * 0.3), mark.animate.shift(DOWN * 0.95), run_time=0.5)
        until(self, "High utilization, low memory")
        ic, wd = b51_row(2)
        self.play(GrowFromCenter(ic), FadeIn(wd, shift=RIGHT * 0.3), mark.animate.shift(DOWN * 0.95), run_time=0.5)
        until(self, "High and high")
        ic, wd = b51_row(3)
        self.play(GrowFromCenter(ic), FadeIn(wd, shift=RIGHT * 0.3), mark.animate.shift(DOWN * 0.95), run_time=0.5)
        until(self, "And an out-of-memory crash")
        ic, wd = b51_row(4)
        self.play(GrowFromCenter(ic), FadeIn(wd, shift=RIGHT * 0.3), mark.animate.shift(DOWN * 0.95), run_time=0.5)
        done(self)


# ─────────────── B52 · batch size moves both axes; binary-search the ceiling; run production at 70–85% of it ───────────────
B52_BAR_Y, B52_AX_Y = 1.8, -1.3
B52_X0, B52_X1 = -5.0, 5.0


def b52_x(batch):
    return B52_X0 + (B52_X1 - B52_X0) * batch / 4096.0


def b52_fill(frac):
    w = (B52_X1 - B52_X0 - 0.16) * min(frac, 1.0)
    return Rectangle(width=w, height=0.64, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B52_X0 + 0.08 + w / 2, B52_BAR_Y, 0])


def b52_hop(mark, b0, b1):
    return MoveAlongPath(mark, ArcBetweenPoints(np.array([b52_x(b0), B52_AX_Y, 0.0]), np.array([b52_x(b1), B52_AX_Y, 0.0]), angle=-PI / 2))


def b52_num(batch):
    return M(str(batch), 32).move_to([b52_x(batch), -1.85, 0])


class B52_BinarySearch(Scene):
    def construct(self):
        bar = Rectangle(width=B52_X1 - B52_X0, height=0.8, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([0, B52_BAR_Y, 0])
        fill = b52_fill(0.175)
        axis = Line([B52_X0, B52_AX_Y, 0], [B52_X1, B52_AX_Y, 0], color=INK, stroke_width=4)
        mark = Dot([b52_x(512), B52_AX_Y, 0], radius=0.15, color=INK).set_z_index(3)
        self.add(bar, fill, axis, mark, pc_left(T("VRAM", 36), -5.0, 2.55), T("batch size", 36).move_to([4.3, -2.5, 0]),
                 T("1", 32).move_to([B52_X0, -1.85, 0]), M("4096", 32).move_to([B52_X1, -1.85, 0]))
        until(self, "Batch size moves both axes")
        self.play(b52_hop(mark, 512, 1024), Transform(fill, b52_fill(0.35)), run_time=0.8)
        until(self, "as long as the GPU")
        self.play(b52_hop(mark, 1024, 512), Transform(fill, b52_fill(0.175)), run_time=0.8)
        until(self, "On a B200")
        self.play(FadeIn(M("B200", 36).move_to([0, 2.55, 0])), run_time=0.3)
        until(self, "one hundred ninety-two gigabytes")
        self.play(FadeIn(T("192 GB", 36).move_to([4.3, 2.55, 0])), run_time=0.3)
        until(self, "fifteen or twenty percent")
        pct = T("15–20%", 36).move_to([-3.3, 1.05, 0])
        self.play(FadeIn(pct, shift=UP * 0.2), run_time=0.35)
        until(self, "four to eight times the batch")
        room = T("4–8×", 40).move_to([1.0, 1.05, 0])
        self.play(FadeIn(room, shift=UP * 0.2), run_time=0.35)
        until(self, "try a size")
        self.play(FadeOut(pct), FadeOut(room), b52_hop(mark, 512, 2048), Transform(fill, b52_fill(0.7)), run_time=0.8)
        until(self, "see if it fits")
        self.play(Create(check(b52_x(2048), -0.75, 0.2, INK, 6)), FadeIn(b52_num(2048)), run_time=0.35)
        until(self, "halve the gap")
        oom = Dot([B52_X1, B52_BAR_Y, 0], radius=0.15, color=TERRA).set_z_index(3)
        self.play(b52_hop(mark, 2048, 3072), Transform(fill, b52_fill(1.0)), run_time=0.7)
        self.play(GrowFromCenter(oom), Create(pc_cross(b52_x(3072), -0.75, 0.18, 6)), FadeIn(b52_num(3072)), run_time=0.35)
        until(self, "repeat")
        self.play(b52_hop(mark, 3072, 2560), Transform(fill, b52_fill(0.875)), FadeOut(oom), run_time=0.7)
        self.play(Create(check(b52_x(2560), -0.75, 0.2, INK, 6)), FadeIn(b52_num(2560)), run_time=0.35)
        self.play(FadeIn(T("ceiling", 36).move_to([b52_x(2560), -0.15, 0]), shift=DOWN * 0.2), run_time=0.3)
        until(self, "seventy to eighty-five percent")
        band = Rectangle(width=b52_x(2560 * 0.85) - b52_x(2560 * 0.70), height=0.5, fill_color=BAR2, fill_opacity=1, stroke_width=0)
        band.move_to([(b52_x(2560 * 0.85) + b52_x(2560 * 0.70)) / 2, B52_AX_Y, 0]).set_z_index(1)
        self.play(GrowFromCenter(band), run_time=0.5)
        self.play(FadeIn(T("production · 70–85%", 36).move_to([-0.6, -2.5, 0]), shift=UP * 0.2), run_time=0.35)
        done(self)


# ─────────────── B54 · the bit ladder: FP32 8|23, BF16 8|7, FP16 5|10, FP8 4|3 ───────────────
B54_FMT = (("FP32", 8, 23), ("BF16", 8, 7), ("FP16", 5, 10), ("FP8", 4, 3))
B54_Y = (2.0, 0.75, -0.5, -1.75)
B54_X0, B54_U, B54_CW, B54_H, B54_SPLIT = -3.9, 0.28, 0.25, 0.5, 0.1


def b54_cells(n, x0, y, fill):
    return VGroup(*[Rectangle(width=B54_CW, height=B54_H, fill_color=fill, fill_opacity=1, stroke_width=0)
                    .move_to([x0 + i * B54_U + B54_CW / 2, y, 0]) for i in range(n)])


def b54_row(k):
    """(label, exponent cells, mantissa cells, exponent count, mantissa count) for format k."""
    name, e, m = B54_FMT[k]
    y = B54_Y[k]
    xe, xm = B54_X0, B54_X0 + e * B54_U + B54_SPLIT
    lab = M(name, 36).move_to([-5.0, y, 0])
    ec, mc = b54_cells(e, xe, y, BAR1), b54_cells(m, xm, y, BAR2)
    en = T(str(e), 34).move_to([xe + (e * B54_U - 0.03) / 2, y + 0.5, 0])
    mn = T(str(m), 34).move_to([xm + (m * B54_U - 0.03) / 2, y + 0.5, 0])
    return lab, ec, mc, en, mn


def b54_end(k):
    name, e, m = B54_FMT[k]
    return B54_X0 + e * B54_U + B54_SPLIT + m * B54_U


def b54_grow(self, cells, rt):
    self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.08), run_time=rt)


class B54_BitLadder(Scene):
    def construct(self):
        r32, r16b, r16, r8 = [b54_row(k) for k in range(4)]
        self.add(r32[0], r16b[0], r16[0], r8[0])
        until(self, "exponent, which is range")
        self.play(FadeIn(T("exponent", 36).move_to([-2.8, 3.0, 0]), shift=DOWN * 0.2), run_time=0.35)
        until(self, "mantissa, which is precision")
        self.play(FadeIn(T("mantissa", 36).move_to([1.6, 3.0, 0]), shift=DOWN * 0.2), run_time=0.35)
        until(self, "FP32 has eight exponent bits")
        b54_grow(self, r32[1], 0.5)
        self.add(r32[3])
        until(self, "twenty-three of mantissa")
        b54_grow(self, r32[2], 0.8)
        self.add(r32[4])
        until(self, "BF16 keeps the same eight")
        b54_grow(self, r16b[1], 0.5)
        self.add(r16b[3])
        self.play(Indicate(VGroup(r32[1], r16b[1]), color=None, scale_factor=1.06), run_time=0.5)   # the same eight, aligned
        until(self, "keeps only seven for precision")
        b54_grow(self, r16b[2], 0.5)
        self.add(r16b[4])
        until(self, "so gradients don't underflow")
        self.play(Create(check(b54_end(1) + 0.55, B54_Y[1], 0.22, TERRA, 8)), run_time=0.35)
        until(self, "FP16 bets the other way")
        self.play(Indicate(r16[0], color=None, scale_factor=1.1), run_time=0.35)
        until(self, "ten bits of precision")
        b54_grow(self, r16[2], 0.6)
        self.add(r16[4])
        until(self, "but only five of exponent")
        b54_grow(self, r16[1], 0.4)
        self.add(r16[3])
        until(self, "which underflows")
        self.play(FadeIn(T("underflow", 36).move_to([b54_end(2) + 1.15, B54_Y[2], 0]), shift=LEFT * 0.2),
                  Indicate(r16[1], color=None, scale_factor=1.08), run_time=0.45)
        until(self, "FP8 goes further still")
        b54_grow(self, r8[1], 0.35)
        b54_grow(self, r8[2], 0.3)
        self.add(r8[3], r8[4])
        until(self, "Every step down")
        arrow = Arrow([5.5, 2.1, 0], [5.5, -2.0, 0], color=INK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.08)
        self.play(Create(arrow), run_time=0.6)
        self.add(T("quality", 34).move_to([5.5, 2.45, 0]))
        until(self, "for speed and memory")
        self.play(FadeIn(T("speed, memory", 34).move_to([4.6, -2.5, 0]), shift=UP * 0.2), run_time=0.35)
        done(self)


# ─────────────── B55 · what BF16 buys: activations halve, matmuls 2–4×, four risky blocks stay FP32 ───────────────
B55_X = tuple(-5.4 + k * 1.55 for k in range(8))       # activations ×2, matmul ×2, weights, loss, softmax, norm
B55_OY, B55_S = -1.0, 0.65
B55_FP32 = ("weights", "loss", "softmax", "norm")


def b55_block(k, h=1.4, grey=False):
    iso = Iso(B55_X[k], B55_OY, B55_S)
    if grey:
        return iso.box(0, 0, 0, 1.1, 1.0, h, PC_GTOP, PC_GL, PC_GR).set_stroke(DIM, width=3)
    return iso.box(0, 0, 0, 1.1, 1.0, h, DARK_TOP, DARK_L, DARK_R)


def b55_spark(k):
    return Dot(Iso(B55_X[k], B55_OY, B55_S).p(0.55, 0.5, 1.4), radius=0.11, color=TERRA).set_z_index(3)


class B55_MixedSafetyNet(Scene):
    def construct(self):
        blocks = [b55_block(k) for k in range(8)]
        self.add(*blocks, T("activations", 36).move_to([-4.625, -1.45, 0]), T("matmul", 36).move_to([-1.525, -1.45, 0]))
        until(self, "Activation memory roughly halves")
        self.play(Transform(blocks[0], b55_block(0, 0.7)), Transform(blocks[1], b55_block(1, 0.7)), run_time=0.8)
        until(self, "so a much bigger batch fits")
        self.play(*[FadeIn(T("½", 44).move_to([B55_X[k], 0.75, 0]), shift=DOWN * 0.3) for k in (0, 1)], run_time=0.4)
        until(self, "Matrix operations run two to four times faster")
        sparks = VGroup(b55_spark(2), b55_spark(3))
        self.play(GrowFromCenter(sparks), run_time=0.35)
        self.play(*[FadeIn(T("2–4×", 40).move_to([B55_X[k], 1.05, 0]), shift=DOWN * 0.3) for k in (2, 3)], run_time=0.4)
        until(self, "the risky parts stay in thirty-two bit")
        self.play(*[Transform(blocks[k], b55_block(k, 0.7 if k < 2 else 1.4, grey=True)) for k in range(4)], run_time=0.8)
        self.play(FadeIn(M("BF16", 36).move_to([-3.075, -2.3, 0])), FadeIn(M("FP32", 36).move_to([3.125, -2.3, 0])), run_time=0.35)
        for k, phrase in enumerate(("Master weights", "the loss", "softmax", "normalization")):
            until(self, phrase)
            self.play(FadeIn(T(B55_FP32[k], 34).move_to([B55_X[4 + k], -1.45, 0]), shift=UP * 0.2),
                      Indicate(blocks[4 + k], color=None, scale_factor=1.06), run_time=0.4)
        until(self, "Autocast handles that")
        self.play(FadeIn(M("autocast", 36).move_to([0.0, 2.4, 0]), shift=DOWN * 0.2), run_time=0.35)
        until(self, "largest for matrix multiplies")
        self.play(Indicate(sparks, color=None, scale_factor=1.7), run_time=0.6)
        done(self)


# ─────────────── B60 · the eighty percent rule: > 80% split the work four ways; < 60% four starved GPUs; I/O-bound compete for files ───────────────
B60_C, B60_R = (-4.0, 0.5), 1.1
B60_GX = (-0.9, 0.9, 2.7, 4.5)
B60_ONE = Iso(-4.0, -2.0, 0.8)
B60_CAB = Iso(1.75, 0.75, 0.45)


def b60_small(x, frac):
    return pc_dial((x, -0.3), 0.45, frac, sw=3)


class B60_EightyRule(Scene):
    def construct(self):
        self.add(pc_title("VI · More Than One GPU"))
        gauge = pc_gauge(B60_C, B60_R, sw=5, ticks=(0.0, 0.6, 0.8, 1.0))
        needle = pc_needle(B60_C, B60_R, 0.3, sw=9).set_color(BAR1)   # grey: GATE T read the ink needle inside the arc bbox as an overlapping text run
        body, light = gpu_block(B60_ONE)
        light.scale(1.5).set_color(TERRA)
        job = job_box(B60_ONE, 0.15, 0.15, 0.5).set_z_index(2)
        self.add(gauge, needle, body, light, job, T("60%", 32).move_to([-4.7, 2.05, 0]), T("80%", 32).move_to([-2.3, 1.7, 0]),
                 T("one GPU", 36).move_to([-4.0, -2.55, 0]))
        until(self, "Multi-GPU is the first thing")
        four = VGroup()
        lights, dials = VGroup(), VGroup()
        for x in B60_GX:
            b, l = gpu_block(Iso(x, -2.0, 0.65))
            l.scale(1.5)
            four.add(b); lights.add(l); dials.add(b60_small(x, 0.0))
        four.add(lights, dials, T("four GPUs", 36).move_to([1.8, -2.55, 0]))
        four.shift(RIGHT * 9)
        self.add(four)
        self.play(four.animate.shift(LEFT * 9), run_time=0.8)
        until(self, "More GPUs amplify")
        self.play(pc_turn(needle, B60_C, 0.3, 0.5), run_time=0.5)
        until(self, "already above eighty percent")
        self.play(pc_turn(needle, B60_C, 0.5, 0.88), run_time=0.7)
        until(self, "adding cards divides the work")
        jobs = VGroup(*[job_box(Iso(x, -2.0, 0.65), 0.2, 0.2, 0.5, s=0.5).set_z_index(2) for x in B60_GX])
        self.play(FadeIn(jobs, shift=DOWN * 0.6), lights.animate.set_color(TERRA),
                  *[pc_turn(dials[i][1], (B60_GX[i], -0.3), 0.0, 0.88) for i in range(4)], run_time=0.7)
        ok = check(3.3, -2.55, 0.22, INK, 7)
        self.play(Create(ok), run_time=0.3)
        until(self, "If it's below sixty")
        self.play(pc_turn(needle, B60_C, 0.88, 0.4), run_time=0.6)
        until(self, "four starved GPUs waste four times")
        idle = VGroup(*[Dot([x + 0.2, -0.3 + 0.2, 0], radius=0.075, color=TERRA).set_z_index(3) for x in B60_GX])
        self.play(*[pc_turn(dials[i][1], (B60_GX[i], -0.3), 0.88, 0.4) for i in range(4)], lights.animate.set_color(GHOST), FadeOut(ok), run_time=0.6)
        self.play(GrowFromCenter(idle), FadeIn(T("×4", 44).move_to([5.65, -0.3, 0])), run_time=0.4)
        until(self, "And an I/O-bound job gets worse")
        cab = project_cabinet(B60_CAB).set_z_index(2)
        self.play(FadeIn(cab, shift=DOWN * 0.4), run_time=0.5)
        until(self, "compete for the same files")
        wires = VGroup(*[Line([x, 0.22, 0], [1.75, 0.62, 0], color=PC_KRAFT, stroke_width=5) for x in B60_GX]).set_z_index(1)
        self.play(Create(wires), run_time=0.6)
        self.play(FadeIn(T("same files", 36).move_to([3.7, 1.5, 0]), shift=LEFT * 0.2), run_time=0.35)
        done(self)

# ═════════════════════════════ PART D · B61 B63 (Act VI) · B70 B71 B72 B73 (Act VII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PD_ / b6x_ / b7x_ so the parts never collide.

PD_BAR_H = 0.42


def pd_slab(w=1.1, h=0.36, fill=BAR1):
    """A gradient slab: a flat grey block with an ink outline."""
    return Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=3)


def pd_hbar(x0, y, w, fill=BAR1, h=PD_BAR_H):
    """A horizontal utilization bar anchored at its left edge x0."""
    return Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x0 + w / 2, y, 0])


def pd_slot(ox, oy, s=1.0):
    """An empty job slot: a pale pad with a grey outline, same picture as the previous film's devel slots."""
    return Iso(ox, oy, s).quad([(-0.1, -0.1, 0), (0.8, -0.1, 0), (0.8, 0.8, 0), (-0.1, 0.8, 0)], GHOST, stroke=BAR1, sw=3).set_z_index(-1)


# ─────────────── B61 · data parallel: three batches, three gradients, one all-reduce, one update everywhere ───────────────
B61_OY = -2.3
B61_GX = (-4.3, -2.0, 0.3)
B61_SLAB_Y = 0.05
B61_MERGE = np.array([-2.0, 1.45, 0.0])


def b61_gpu(ox):
    return gpu_block(Iso(ox, B61_OY, 1.0))


def b61_batch(ox):
    return Iso(ox, B61_OY, 1.0).box(0.25, 0.25, 0.5, 0.5, 0.5, 0.35).set_z_index(2)


class B61_AllReduce(Scene):
    def construct(self):
        gpus = [b61_gpu(x) for x in B61_GX]
        self.play(*[FadeIn(VGroup(b, l), shift=DOWN * 0.4) for b, l in gpus], run_time=0.6)
        until(self, "takes a different mini-batch", lead=0.9)
        batches = [b61_batch(x) for x in B61_GX]
        for bx in batches:
            bx.shift(UP * 1.6)
        labels = [T(f"batch {n}", 34).move_to([x, -2.75, 0]) for n, x in zip("ABC", B61_GX)]
        self.play(LaggedStart(*[bx.animate.shift(DOWN * 1.6) for bx in batches], lag_ratio=0.3), run_time=0.9, rate_func=ease_in)
        self.play(*[FadeIn(lb) for lb in labels], *[l.animate.set_color(TERRA) for b, l in gpus], run_time=0.3)
        until(self, "After the backward pass", lead=0.3)
        slabs = [pd_slab().move_to([x, B61_SLAB_Y, 0]) for x in B61_GX]
        self.play(*[FadeIn(s, shift=UP * 0.6) for s in slabs], run_time=0.6)
        until(self, "they all-reduce", lead=0.1)
        self.play(*[s.animate.move_to(B61_MERGE) for s in slabs], run_time=0.8)
        merged = pd_slab(1.4, 0.45, BAR2).move_to(B61_MERGE)
        self.play(FadeOut(VGroup(*slabs)), GrowFromCenter(merged), run_time=0.4)
        until(self, "each applies the same update", lead=0.3)
        copies = [pd_slab(1.1, 0.36, BAR2).move_to(B61_MERGE) for _ in B61_GX]
        self.add(*copies)
        self.play(*[c.animate.move_to([x, B61_SLAB_Y, 0]) for c, x in zip(copies, B61_GX)], FadeOut(merged), run_time=0.8)
        until(self, "Inside one node", lead=0.2)
        bracket = VGroup(Line([-5.2, 2.2, 0], [1.2, 2.2, 0], color=INK, stroke_width=4),
                         Line([-5.2, 2.2, 0], [-5.2, 1.9, 0], color=INK, stroke_width=4),
                         Line([1.2, 2.2, 0], [1.2, 1.9, 0], color=INK, stroke_width=4))
        self.play(Create(bracket), run_time=0.5)
        self.play(FadeIn(T("one node · NVLink", 34).move_to([-2.0, 2.75, 0])), run_time=0.3)
        until(self, "Across nodes", lead=0.2)
        far_b, far_l = b61_gpu(4.7)
        link = DashedLine([1.3, -1.5, 0], [3.75, -1.5, 0], color=INK, stroke_width=4, dash_length=0.18)
        self.play(FadeIn(VGroup(far_b, far_l), shift=DOWN * 0.4), Create(link), run_time=0.6)
        self.play(FadeIn(T("across nodes", 34).move_to([4.7, 0.3, 0])), FadeIn(T("slower", 34).move_to([4.7, -0.25, 0])), run_time=0.3)
        until(self, "single-node multi-GPU", lead=0.2)
        self.play(Indicate(VGroup(*[l for b, l in gpus]), color=TERRA, scale_factor=1.6), run_time=0.7)
        done(self)


# ─────────────── B63 · scaling efficiency: measured bars under the ideal, three bands, back to one card ───────────────
B63_BASE = -1.6
B63_UNIT = 0.62
B63_BX = {1: -4.5, 2: -3.0, 4: -1.5}
B63_MEAS = {1: 1.0, 2: 0.9, 4: 0.77}          # measured height as a share of ideal (shape only: no number is shown)
B63_BAND_X = 3.3


def b63_bar(n):
    h = n * B63_UNIT * B63_MEAS[n]
    return Rectangle(width=1.0, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B63_BX[n], B63_BASE + h / 2, 0])


def b63_ideal(n):
    y = B63_BASE + n * B63_UNIT
    return DashedLine([B63_BX[n] - 0.65, y, 0], [B63_BX[n] + 0.65, y, 0], color=INK, stroke_width=4, dash_length=0.14)


def b63_gap(n):
    x = B63_BX[n] + 0.8
    return Line([x, B63_BASE + n * B63_UNIT * B63_MEAS[n], 0], [x, B63_BASE + n * B63_UNIT, 0], color=INK, stroke_width=5)


def b63_band(y, fill):
    return Rectangle(width=2.2, height=0.7, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([B63_BAND_X, y, 0])


class B63_ScalingEfficiency(Scene):
    def construct(self):
        self.add(Line([-5.3, B63_BASE, 0], [-0.7, B63_BASE, 0], color=INK, stroke_width=4),
                 *[T(str(n), 40).move_to([B63_BX[n], -1.95, 0]) for n in (1, 2, 4)],
                 T("GPUs", 34).move_to([-0.2, -1.95, 0]))
        bars = [b63_bar(n) for n in (1, 2, 4)]
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), run_time=1.0)
        self.play(Create(b63_ideal(2)), Create(b63_ideal(4)), run_time=0.5)
        self.play(FadeIn(T("ideal", 34).move_to([-0.1, B63_BASE + 4 * B63_UNIT, 0])), run_time=0.3)
        until(self, "Throughput divided", lead=0.2)
        self.play(FadeIn(T("efficiency", 34).move_to([1.4, 2.3, 0])), FadeIn(T("=", 34).move_to([2.55, 2.3, 0])),
                  FadeIn(T("throughput", 34).move_to([4.2, 2.85, 0])), run_time=0.4)
        self.play(Create(Line([3.0, 2.3, 0], [5.4, 2.3, 0], color=INK, stroke_width=4)), run_time=0.3)
        self.play(FadeIn(T("n × baseline", 34).move_to([4.2, 1.75, 0])), run_time=0.3)
        until(self, "gives efficiency", lead=0.1)
        self.play(Create(b63_gap(2)), Create(b63_gap(4)), run_time=0.4)
        until(self, "Above eighty percent", lead=0.2)
        self.play(GrowFromEdge(b63_band(0.5, BAR3), LEFT), FadeIn(T("> 80%", 34).move_to([5.35, 0.5, 0])), run_time=0.5)
        self.play(Create(check(1.7, 0.5, 0.2)), run_time=0.3)
        until(self, "Seventy to eighty", lead=0.2)
        self.play(GrowFromEdge(b63_band(-0.4, BAR2), LEFT), FadeIn(T("70–80%", 34).move_to([5.35, -0.4, 0])), run_time=0.5)
        until(self, "Below seventy", lead=0.2)
        self.play(GrowFromEdge(b63_band(-1.3, BAR1), LEFT), FadeIn(T("< 70%", 34).move_to([5.35, -1.3, 0])), run_time=0.5)
        self.play(GrowFromCenter(Dot([1.7, -1.3, 0], radius=0.17, color=TERRA)), run_time=0.3)
        until(self, "more GPUs won't help", lead=0.2)
        strike = VGroup(Line([-2.0, -0.4, 0], [-1.0, 0.6, 0], color=INK, stroke_width=8),
                        Line([-2.0, 0.6, 0], [-1.0, -0.4, 0], color=INK, stroke_width=8))
        self.play(Create(strike), run_time=0.4)
        until(self, "Go back", lead=0.4)
        back = VGroup(Line([1.7, -1.55, 0], [1.7, -2.75, 0], color=INK, stroke_width=5),
                      Line([1.7, -2.75, 0], [-4.5, -2.75, 0], color=INK, stroke_width=5),
                      Arrow([-4.5, -2.75, 0], [-4.5, -2.3, 0], color=INK, stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.5))
        self.play(Create(back), run_time=0.8)
        self.play(GrowFromCenter(Circle(radius=0.3, color=TERRA, stroke_width=6).move_to([-4.5, -1.95, 0])), run_time=0.3)
        done(self)


# ─────────────── B70 · the loop: seven steps round a ring, one fix at a time, exit above eighty ───────────────
B70_C = np.array([-2.2, -0.2, 0.0])
B70_R = 1.8
B70_STEP = 360.0 / 7
B70_A0 = -B70_STEP                    # baseline sits lower-right; the ring runs clockwise; repeat lands at 0° (right)
B70_NAMES = ("baseline", "profile", "diagnose", "fix one", "re-profile", "record", "repeat")
B70_LABEL_AT = {"baseline": (-0.58, -2.23), "profile": (-2.78, -2.73), "diagnose": (-4.75, -1.4), "fix one": (-4.75, 1.0),
                "re-profile": (-2.78, 2.33), "record": (-0.5, 1.9), "repeat": (0.55, 0.45)}


def b70_ang(k):
    return B70_A0 - B70_STEP * k


def b70_pt(deg, r=B70_R):
    a = deg * PI / 180
    return B70_C + r * np.array([np.cos(a), np.sin(a), 0.0])


def b70_arc(k0, k1):
    """Clockwise arc from step k0 to step k1 along the ring."""
    a0, a1 = b70_ang(k0), b70_ang(k1)
    return Arc(radius=B70_R, start_angle=a0 * PI / 180, angle=(a1 - a0) * PI / 180, arc_center=B70_C)


def b70_node(k):
    return Dot(b70_pt(b70_ang(k)), radius=0.14, color=INK)


def b70_label(k):
    x, y = B70_LABEL_AT[B70_NAMES[k]]
    return T(B70_NAMES[k], 34).move_to([x, y, 0])


def b70_card(x, y):
    return RoundedRectangle(width=0.9, height=0.55, corner_radius=0.1, fill_color=BOX_TOP, fill_opacity=1,
                            stroke_color=INK, stroke_width=3).move_to([x, y, 0])


class B70_TheLoop(Scene):
    def construct(self):
        self.add(T("VII · The Loop", 40).move_to([-4.7, 3.0, 0]))
        ring = Circle(radius=B70_R, color=BAR1, stroke_width=4).move_to(B70_C)
        self.play(Create(ring), run_time=0.9)
        nodes = [b70_node(k) for k in range(7)]
        labels = [b70_label(k) for k in range(7)]
        self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(n), FadeIn(l)) for n, l in zip(nodes, labels)], lag_ratio=0.3), run_time=2.4)
        until(self, "Baseline:", lead=0.2)
        mark = Dot(b70_pt(b70_ang(0)), radius=0.19, color=TERRA).set_z_index(4)
        self.play(GrowFromCenter(mark), run_time=0.3)
        until(self, "Profile twenty", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(0, 1)), run_time=0.6)
        until(self, "Diagnose:", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(1, 2)), run_time=0.6)
        until(self, "Fix one thing", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(2, 3)), run_time=0.6)
        until(self, "Only one", lead=0.1)
        card = b70_card(-6.0, 0.3)
        self.add(card)
        self.play(card.animate.shift(RIGHT * 1.5), run_time=0.45, rate_func=ease_in)                     # a second fix arrives ...
        self.play(card.animate.shift(LEFT * 1.1), run_time=0.35, rate_func=rate_functions.ease_out_bounce)  # ... and is pushed out
        self.play(FadeOut(card, shift=LEFT * 0.6), run_time=0.3)
        until(self, "Re-profile:", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(3, 4)), run_time=0.6)
        until(self, "Record the gain", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(4, 5)), run_time=0.5)
        until(self, "Repeat until", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(5, 6)), run_time=0.5)
        until(self, "above eighty", lead=0.2)
        exit_arrow = Arrow([-0.15, -0.2, 0], [1.75, -0.2, 0], color=INK, stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.18)
        self.play(GrowArrow(exit_arrow), run_time=0.4)
        self.play(FadeIn(T("> 80%", 56).move_to([3.3, -0.2, 0]), shift=RIGHT * 0.2), run_time=0.3)
        until(self, "or the returns run out", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(6, 7)), run_time=0.7)
        done(self)


# ─────────────── B71 · the decision tree: utilization at the root, memory leaves, multi-GPU, the OOM order ───────────────
B71_Y = (2.9, 1.6, 0.3, -1.0, -1.7, -2.3)


def b71_edge(xf, yf, xt, yt):
    """An ink branch from the label at (xf, yf) down to the label at (xt, yt), 0.3 clear of both."""
    return Line([xf, yf - 0.45, 0], [xt, yt + 0.45, 0], color=INK, stroke_width=4)


def b71_lab(s, x, y, size=32):
    return T(s, size).move_to([x, y, 0])


class B71_DecisionTree(Scene):
    def construct(self):
        y0, y1, y2, y3, y4, y5 = B71_Y
        root = b71_lab("utilization?", -1.3, y0)
        self.play(FadeIn(root, shift=DOWN * 0.2), run_time=0.4)
        until(self, "Utilization under fifty?", lead=0.1)
        self.play(Create(b71_edge(-1.3, y0, -5.0, y1)), run_time=0.4)
        self.play(FadeIn(b71_lab("< 50%", -5.0, y1)), run_time=0.3)
        until(self, "the data pipeline", lead=0.2)
        self.play(Create(b71_edge(-5.0, y1, -5.0, y2)), FadeIn(b71_lab("data pipeline", -5.0, y2)), run_time=0.4)
        until(self, "workers is zero", lead=0.2)
        self.play(FadeIn(b71_lab("workers = 0", -5.0, -0.4)), run_time=0.3)
        self.play(FadeIn(b71_lab("first", -5.0, y3)), run_time=0.3)
        until(self, "Fifty to eighty?", lead=0.2)
        self.play(Create(b71_edge(-1.3, y0, -1.3, y1)), FadeIn(b71_lab("50–80%", -1.3, y1)), run_time=0.4)
        until(self, "Look at memory", lead=0.1)
        self.play(Create(b71_edge(-1.3, y1, -1.3, y2)), FadeIn(b71_lab("memory?", -1.3, y2)), run_time=0.4)
        leaves = ((-3.6, "< 40%", "batch ↑", "Under forty percent"), (-2.0, "40–85%", "BF16", "Forty to eighty-five"),
                  (-0.45, "> 90%", "batch ↓", "Over ninety"), (1.15, "OK", "profile", "Memory fine?"))
        for x, cond, act, cue in leaves:
            until(self, cue, lead=0.2)
            self.play(Create(b71_edge(-1.3, y2, x, y3)), FadeIn(b71_lab(cond, x, y3)), run_time=0.35)
            self.play(FadeIn(b71_lab(act, x, y4), shift=DOWN * 0.15), run_time=0.3)
            if cond == "> 90%":
                self.play(FadeIn(b71_lab("checkpoint", x, y5), shift=DOWN * 0.15), run_time=0.3)
        until(self, "Above eighty with healthy memory?", lead=0.2)
        self.play(Create(b71_edge(-1.3, y0, 2.9, y1)), FadeIn(b71_lab("> 80%", 2.9, y1)), run_time=0.4)
        self.play(Create(b71_edge(2.9, y1, 2.9, y2)), FadeIn(b71_lab("multi-GPU?", 2.9, y2)), run_time=0.4)
        until(self, "only if the single card", lead=0.2)
        self.play(Create(b71_edge(2.9, y2, 2.9, y3)), FadeIn(b71_lab("if saturated", 2.9, y3)), run_time=0.4)
        until(self, "And out of memory", lead=0.1)
        self.play(FadeIn(b71_lab("OOM", 5.25, y1), shift=DOWN * 0.2), run_time=0.3)
        oom = (("BF16", 0.9, "BF16, then"), ("checkpoint", 0.2, "then checkpointing"), ("batch ↓", -0.5, "then a smaller batch"))
        for s, y, cue in oom:
            until(self, cue, lead=0.1)
            self.play(FadeIn(b71_lab(s, 5.25, y), shift=DOWN * 0.15), run_time=0.3)
        until(self, "In that order", lead=0.1)
        order = Arrow([4.15, 1.15, 0], [4.15, -0.75, 0], color=INK, stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.14)
        self.play(GrowArrow(order), run_time=0.5)
        done(self)


# ─────────────── B72 · the real jobstats report, re-composed on cream: command, header rows, four bars ───────────────
B72_X0 = -3.1            # bars start here
B72_FULL = 4.6           # 100 % of a bar
B72_ROWS = (("CPU", 13, 0.1), ("CPU memory", 25, -0.6), ("GPU", 80, -1.3), ("GPU memory", 17, -2.0))


def b72_row_label(name, y):
    return M(name, 32).move_to([-4.7, y, 0])


def b72_bar(pct, y):
    return pd_hbar(B72_X0, y, B72_FULL * pct / 100.0)


def b72_pct(pct, y):
    return M(f"{pct}%", 32).move_to([B72_X0 + B72_FULL * pct / 100.0 + 0.65, y, 0])


def b72_ring(pct, y):
    return Circle(radius=0.5, color=TERRA, stroke_width=6).move_to([B72_X0 + B72_FULL * pct / 100.0 + 0.65, y, 0])


class B72_Jobstats(Scene):
    def construct(self):
        self.play(FadeIn(M("$ jobstats 318592", 32).move_to([-3.8, 2.05, 0])), run_time=0.4)
        until(self, "runs on AICR", lead=0.3)
        header = VGroup(M("Job Name", 32).move_to([-4.9, 1.45, 0]), M("f5tune-voice", 32).move_to([-1.9, 1.45, 0]),
                        M("rtx-batch", 32).move_to([1.6, 1.45, 0]), M("GPUs 1", 32).move_to([4.2, 1.45, 0]),
                        M("Run Time", 32).move_to([-4.9, 0.9, 0]), M("00:55:09", 32).move_to([-1.9, 0.9, 0]),
                        M("Time Limit", 32).move_to([1.6, 0.9, 0]), M("08:00:00", 32).move_to([4.2, 0.9, 0]))
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(VGroup(*[b72_row_label(n, y) for n, p, y in B72_ROWS]), shift=RIGHT * 0.15), run_time=0.4)
        until(self, "Here is a real one", lead=0.1)
        self.play(Create(Line([B72_X0, 0.45, 0], [B72_X0, -2.35, 0], color=INK, stroke_width=4)), run_time=0.4)
        until(self, "fifty-five-minute", lead=0.1)
        self.play(Indicate(header[5], color=INK, scale_factor=1.15), run_time=0.6)      # 00:55:09
        until(self, "on an RTX card", lead=0.1)
        self.play(Indicate(header[2], color=INK, scale_factor=1.15), run_time=0.6)      # rtx-batch
        until(self, "GPU utilization eighty percent", lead=0.2)
        self.play(GrowFromEdge(b72_bar(80, -1.3), LEFT), run_time=0.7)
        self.play(FadeIn(b72_pct(80, -1.3)), run_time=0.2)
        ring = b72_ring(80, -1.3)
        self.play(GrowFromCenter(ring), run_time=0.3)
        until(self, "GPU memory seventeen percent", lead=0.2)
        self.play(GrowFromEdge(b72_bar(17, -2.0), LEFT), run_time=0.5)
        self.play(FadeIn(b72_pct(17, -2.0)), run_time=0.2)
        self.play(ring.animate.move_to([B72_X0 + B72_FULL * 0.17 + 0.65, -2.0, 0]), run_time=0.4)
        until(self, "CPU utilization thirteen percent", lead=0.2)
        self.play(GrowFromEdge(b72_bar(13, 0.1), LEFT), GrowFromEdge(b72_bar(25, -0.6), LEFT), run_time=0.5)
        self.play(FadeIn(b72_pct(13, 0.1)), FadeIn(b72_pct(25, -0.6)), run_time=0.2)
        until(self, "the job needed eleven percent", lead=0.2)
        self.play(FadeOut(ring), FadeIn(M("needed 11% of the requested time", 32).move_to([0.0, -2.8, 0]), shift=UP * 0.15), run_time=0.4)
        until(self, "under sixty percent GPU", lead=0.2)
        self.play(GrowFromCenter(b72_ring(80, -1.3)), run_time=0.3)
        done(self)


# ─────────────── B73 · the pre-submission checklist ticks, then the devel job leaves its slot ───────────────
B73_ROW_Y = (2.4, 1.65, 0.9, 0.15, -0.6)
B73_ITEMS = (("verify", T, "The verify script passes"), ("util > 70%", T, "shows over seventy percent"),
             ("workers ≠ 0", T, "Workers is not zero"), ("pin_memory", M, "Pin memory is on"),
             ("batch ≥ 60% VRAM", T, "at least sixty percent of VRAM"), ("BF16", T, "BF16 autocast is on"),
             ("partition", T, "names the right partition"), ("cpus = workers+1", T, "CPUs per task"),
             ("logs/", M, "The logs folder exists"), ("profiled 20", T, "profiled twenty steps"))
B73_SLOTS = ((4.3, -1.2), (5.4, -1.2), (4.3, -2.6), (5.4, -2.6))     # (ox, oy) of four job slots, iso scale 0.75


def b73_box(x, y):
    return Square(side_length=0.4, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y, 0])


def b73_tick(x, y):
    return check(x, y - 0.02, 0.17, INK, 6)


def b73_job(ox, oy):
    return job_box(Iso(ox, oy, 0.75)).set_z_index(2)


class B73_Checklist(Scene):
    def construct(self):
        boxes, labels = [], []
        for i, (s, f, cue) in enumerate(B73_ITEMS):
            x = -5.7 if i < 5 else -0.7
            y = B73_ROW_Y[i % 5]
            bx = b73_box(x, y)
            lb = f(s, 32).next_to(bx, RIGHT, buff=0.35)
            boxes.append(bx)
            labels.append(lb)
        slots = [pd_slot(ox, oy, 0.75) for ox, oy in B73_SLOTS]
        jobs = [b73_job(ox, oy) for ox, oy in B73_SLOTS]
        self.add(*boxes, *labels, *slots, *jobs, T("devel", 34).move_to([4.3, 0.3, 0]))
        for i, (s, f, cue) in enumerate(B73_ITEMS):
            until(self, cue, lead=0.1)
            x = -5.7 if i < 5 else -0.7
            self.play(Create(b73_tick(x, B73_ROW_Y[i % 5])), run_time=0.3)
        until(self, "Then cancel the devel session", lead=0.2)
        self.play(FadeOut(jobs[0], shift=UP * 0.8), run_time=0.6)
        until(self, "four running jobs", lead=0.2)
        self.play(FadeIn(T("4 running jobs", 32).move_to([4.8, 2.4, 0]), shift=DOWN * 0.15), run_time=0.4)
        until(self, "an idle one blocks", lead=0.2)
        self.play(Indicate(slots[0], color=TERRA, scale_factor=1.15), run_time=0.6)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh scene discovery
for _cls in (B21_TwoGauges, B22_TwoAxes, B30_FourLayers, B31_DevelToBatch, B33_ReadTheTrace, B40_Factory, B42_FortyFiveNine, B10_SilentFailures, B11_PartitionTable, B13_RamVsVram, B14_VerifyFive, B15_VisibleDevices, B16_IdleCancel, B20_NvidiaSmi, B44_FourKnobs, B50_TwoMeters, B51_DecisionTable, B52_BinarySearch, B54_BitLadder, B55_MixedSafetyNet, B60_EightyRule, B61_AllReduce, B63_ScalingEfficiency, B70_TheLoop, B71_DecisionTree, B72_Jobstats, B73_Checklist):
    _cls.play = ST.play
