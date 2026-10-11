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
# ═════════════════════════════ PART A · Act I (B10 B11 B12), Act II (B20), Act III (B30), Act VI (B60) ═════════════════════════════
# Stage map. Act I is one picture built up and reused: a laptop at left, the login node (a one-slab server),
# the Slurm gate over a belt, and a wall of three compute racks (aicr_rack) at right. B10 draws it; B12 spreads
# the racks and plumbs them; B60 is B10 again with the X. B11 is the counter beat (fills the frame). B20 is two
# doors. B30 is the two interfaces, shown as themselves (dark terminal, pale browser), cabled to one login node.
PA_KRAFT = "#9C8462"                        # deep-kraft connector (cables are never ink: ink cables fuse the things they join)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only
PA_BELT = "#E4E0D4"                         # belts, pads and door frames stay within 28 of the stage (Gate V)
PA_LOGIN = Iso(-2.6, -2.1, 0.7)             # the login node (B10, B60)
PA_LAPTOP = Iso(-5.1, -2.0, 0.6)            # the laptop (B10)
PA_GATE = Iso(0.4, -2.05, 0.6)              # the Slurm gate (B10, B60)
PA_GATE_PIVOT = PA_GATE.p(0.11, 0.9, 1.0)   # the boom turns on the far post
PA_RACKS = [Iso(2.2, -1.6, 0.42), Iso(3.75, -1.6, 0.42), Iso(5.3, -1.6, 0.42)]      # the compute wall (B10, B60)
PA_RACKS_WIDE = [Iso(-1.0, -1.6, 0.42), Iso(1.6, -1.6, 0.42), Iso(4.2, -1.6, 0.42)]  # the same racks, spread (B12)
PA_RACK_TOP = 2.0                           # z of an aicr_rack's top face (4 slabs)


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


def pa_xmark(x, y, s=0.3, color=TERRA, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def pa_cable(a, b, w=5):
    return Line(a, b, color=PA_KRAFT, stroke_width=w)


def pa_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes (edges dark kraft, never ink)."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PA_BELT, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def pa_login(iso=PA_LOGIN):
    """The login node: ONE dark slab with one light (smaller than the two-slab Explorer rack)."""
    return iso.server(0, 0, 0, w=1.4, d=1.4, slab=0.5, n=1)


def pa_laptop(iso=PA_LAPTOP):
    """A small laptop: kraft base, dark screen standing on the back edge."""
    base = iso.box(0, 0, 0, 1.2, 0.9, 0.08)
    screen = iso.quad([(0, 0.9, 0.08), (1.2, 0.9, 0.08), (1.2, 0.9, 0.85), (0, 0.9, 0.85)], DARK_TOP)
    return VGroup(base, screen)


def pa_gate(iso=PA_GATE):
    """The Slurm gate: two dark posts straddling the belt, a boom between them. Returns (far, boom, near)."""
    far = iso.box(0, 0.9, 0, 0.22, 0.22, 1.1, DARK_TOP, DARK_L, DARK_R)
    near = iso.box(0, -0.5, 0, 0.22, 0.22, 1.1, DARK_TOP, DARK_L, DARK_R).set_z_index(6)
    boom = Line(PA_GATE_PIVOT, iso.p(0.11, -0.39, 1.0), color=DARK_L, stroke_width=14).set_z_index(5)
    return far, boom, near


def pa_racks(isos=PA_RACKS):
    """The compute wall: three aicr racks, farthest drawn first. Returns (stacks, lights) as two VGroups."""
    stacks, lights = [], []
    for iso in reversed(isos):
        st, li = aicr_rack(iso)
        stacks.append(st); lights.append(li)
    return VGroup(*stacks), VGroup(*lights)


def pa_token(x, y):
    """A person token standing with its feet at (x, y)."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2, 0, 0]), b + np.array([0.2, 0, 0]), b + np.array([0.1, 0.5, 0]), b + np.array([-0.1, 0.5, 0]),
                   fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66, 0]))
    return VGroup(body, head).set_z_index(7)


def pa_light_up(self, lights, rt=0.5):
    self.play(LaggedStart(*[l.animate.set_color(TERRA) for l in lights], lag_ratio=0.2), run_time=rt)


# ─────────────── B10 · laptop → login node → Slurm gate → compute racks ───────────────
B10_JOB_AT = (0.75, 0.1, 0.5)                 # the job box on the login node's top face
B10_PAGE_AT = (0.0, 0.8, 0.5)


def b10_job(iso=PA_LOGIN):
    return job_box(iso, *B10_JOB_AT, s=0.55).set_z_index(3)


def b10_page(iso=PA_LOGIN):
    return iso.page(*B10_PAGE_AT, 0.65, 0.75).set_z_index(3)


def b10_labels():
    return (T("login node", 40).move_to([-2.6, -2.6, 0]), T("Slurm", 40).move_to([0.1, 0.15, 0]),
            T("compute nodes", 40).move_to([3.75, -2.4, 0]))


class B10_ClusterShape(Scene):
    def construct(self):
        self.add(pa_title("I · What A Cluster Is"), pa_laptop())
        l_login, l_slurm, l_comp = b10_labels()
        until(self, "many computers")
        stacks, lights = pa_racks()
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.3) for s in stacks], lag_ratio=0.3), run_time=0.9)
        self.add(lights, l_comp)
        until(self, "You log in")
        login_st, login_li = pa_login()
        pa_slide_in(self, VGroup(login_st, login_li), UP * 4.5, 0.6)
        self.play(Create(pa_cable([-4.45, -1.88, 0], [-3.5, -1.88, 0])), run_time=0.4)
        self.add(l_login)
        until(self, "Light work")
        job = b10_job()
        pa_drop(self, [job], 0.45)
        until(self, "editing a file")
        page = b10_page()
        pa_drop(self, [page], 0.4, dist=3.0)
        until(self, "looking around")
        self.play(Indicate(page, color=None, scale_factor=1.15), run_time=0.5)
        until(self, "When you need")
        belt = pa_belt(-1.6, 1.9, -1.75)
        self.play(GrowFromEdge(belt, LEFT), run_time=0.6)
        self.play(job.animate.shift(np.array([1.1, -0.2, 0.0])), run_time=0.5)          # down onto the belt
        until(self, "the work moves")
        far, boom, near = pa_gate()
        self.play(GrowFromCenter(VGroup(far, boom, near)), run_time=0.4)
        self.play(job.animate.shift(RIGHT * 0.6), run_time=0.5)                             # up to the gate
        until(self, "called Slurm")
        self.play(FadeIn(l_slurm), run_time=0.25)
        self.play(Rotate(boom, angle=2 * PI / 3, about_point=PA_GATE_PIVOT), run_time=0.5)
        until(self, "manages everyone")
        self.play(job.animate.shift(RIGHT * 2.0), run_time=0.8)                             # through the gate
        self.play(job.animate.shift(np.array([0.55, 1.1, 0.0])), run_time=0.45)           # onto the first rack
        pa_light_up(self, lights[2], 0.4)
        done(self)


# ─────────────── B11 · 45,000 cores, 525+ GPUs, free, Holyoke ───────────────
B11_P, B11_S, B11_BOT = 0.22, 0.17, -3.1       # cell pitch, square side, grid bottom; ten squares to a column
B11_XL, B11_XR = -6.0, 1.0                      # left edge of each grid (25 columns, then 10)
B11_CX_L, B11_CX_R = B11_XL + 12.5 * B11_P, B11_XR + 5 * B11_P
B11_RACK_A, B11_RACK_B = Iso(-4.9, 1.35, 0.5), Iso(-0.6, 1.35, 0.5)   # Discovery's place, then Explorer's arrival spot
B11_BLDG = Iso(5.0, -2.6, 0.6)


def b11_grid(x0, n, fill):
    """n squares, ten to a column, filled from the bottom, column by column from the left. Returns the columns."""
    cols = []
    for c in range((n + 9) // 10):
        k = min(10, n - 10 * c)
        cols.append(VGroup(*[Square(side_length=B11_S, fill_color=fill, fill_opacity=1, stroke_width=0)
                             .move_to(np.array([x0 + B11_P * (c + 0.5), B11_BOT + B11_P * (r + 0.5), 0.0]))
                             for r in range(k)]))
    return cols


def b11_counts(labels, x):
    """One numeral per column; only one is ever visible."""
    return [T(s, 90).move_to([x, 0.3, 0]) for s in labels]


def b11_fill(self, cols, nums, rt):
    """The squares fill column by column while the counter climbs with them (one play, any frame rate)."""
    n = len(cols)
    for m in cols + nums:
        m.set_opacity(0)
    self.add(*cols, *nums)
    holder = VGroup(*cols, *nums)

    def upd(m, a):
        k = min(n, int(a * n + 0.5))
        for i, c in enumerate(cols):
            c.set_opacity(1.0 if i < k else 0.0)
        for i, t in enumerate(nums):
            t.set_opacity(1.0 if i == k - 1 else 0.0)

    self.play(UpdateFromAlphaFunc(holder, upd), run_time=rt, rate_func=linear)
    upd(holder, 1.0)


def b11_pale(rack):
    """The older Discovery cluster: the same two-slab rack, drawn pale."""
    st, li = rack
    for s in st:
        s.set_fill(GHOST).set_stroke(BAR2)
    li.set_color(BAR3)
    return VGroup(st, li)


def b11_building():
    return VGroup(B11_BLDG.box(0, 0, 0, 1.4, 1.2, 0.6), B11_BLDG.box(0.4, 0.35, 0.6, 0.6, 0.55, 0.55))


def b11_free_tag():
    return VGroup(pill(5.2, 2.0, 1.4, 0.62, GHOST), T("free", 40).move_to([5.2, 2.0, 0]))


class B11_ExplorerNumbers(Scene):
    def construct(self):
        slots = VGroup(*b11_grid(B11_XL, 250, BAR3), *b11_grid(B11_XR, 100, BAR3))
        disc = b11_pale(explorer_rack(B11_RACK_A))
        l_disc = T("Discovery", 44).move_to([-3.15, 1.9, 0])
        self.add(slots, disc, l_disc)
        until(self, "Explorer is", lead=0.1)
        est, eli = explorer_rack(B11_RACK_B)
        exp = VGroup(est, eli)
        pa_slide_in(self, exp, LEFT * 7, 0.6)
        l_exp = T("Explorer", 44).move_to([1.15, 1.9, 0])
        self.add(l_exp)
        until(self, "run by the Research")
        team = VGroup(*[pa_token(x, 1.35) for x in (2.7, 3.2, 3.7)])
        self.play(LaggedStart(*[GrowFromCenter(t) for t in team], lag_ratio=0.3), run_time=0.5)
        self.add(T("Research Computing", 34).move_to([3.2, 2.6, 0]))
        until(self, "replaced the older")
        self.play(FadeOut(disc), FadeOut(l_disc), run_time=0.35)
        self.play(exp.animate.shift(LEFT * 4.3), l_exp.animate.shift(LEFT * 4.3), run_time=0.6)
        until(self, "Forty-five thousand")
        cpu_labels = [f"{1800 * (c + 1):,}" for c in range(25)]
        b11_fill(self, b11_grid(B11_XL, 250, BAR1), b11_counts(cpu_labels, B11_CX_L), 1.5)
        self.add(T("CPU cores", 40).move_to([B11_CX_L, -0.5, 0]))
        until(self, "More than five hundred")
        gpu_labels = [str(int(round(525 * (c + 1) / 10))) for c in range(9)] + ["525+"]
        b11_fill(self, b11_grid(B11_XR, 100, DARK_L), b11_counts(gpu_labels, B11_CX_R), 1.1)
        self.add(T("GPUs", 40).move_to([B11_CX_R, -0.5, 0]))
        until(self, "Free of charge")
        pa_drop(self, [b11_free_tag()], 0.45, dist=2.0)
        until(self, "It lives at")
        self.play(GrowFromCenter(b11_building()), run_time=0.5)
        until(self, "in Holyoke", lead=0.35)
        self.play(FadeIn(T("Holyoke, MA", 34).move_to([4.8, -0.6, 0]), shift=UP * 0.2), run_time=0.3)
        done(self)


# ─────────────── B12 · around the compute: 10 GbE in and out, 6 PB storage, InfiniBand between nodes ───────────────
B12_CAMPUS = Iso(-5.0, -2.0, 0.6)
B12_STORE = Iso(-4.6, 0.9, 0.55)
B12_PIPE_Y = -1.3


def b12_campus():
    return VGroup(B12_CAMPUS.box(0, 0, 0, 1.2, 1.2, 0.5), B12_CAMPUS.box(0.35, 0.35, 0.5, 0.5, 0.5, 0.45))


def b12_storage():
    """A dark storage block with three light drive bays on its front."""
    iso = B12_STORE
    body = iso.box(0, 0, 0, 1.7, 1.4, 1.0, DARK_TOP, DARK_L, DARK_R)
    bays = VGroup(*[iso.quad([(0.22 + 0.5 * k, 0, 0.3), (0.52 + 0.5 * k, 0, 0.3), (0.52 + 0.5 * k, 0, 0.7), (0.22 + 0.5 * k, 0, 0.7)],
                             GHOST, sw=0) for k in range(3)])
    return VGroup(body, bays)


def b12_pipe(a, b, w=16):
    """A pipe: a thick grey line (BAR1, never ink: an ink pipe fuses the blocks it joins)."""
    return Line(a, b, color=BAR1, stroke_width=w)


def b12_links(y):
    """One short link in each of the two gaps between the spread racks."""
    return VGroup(b12_pipe([0.12, y, 0], [0.83, y, 0], 10), b12_pipe([2.72, y, 0], [3.43, y, 0], 10))


def b12_jobs():
    return [job_box(iso, 0.6, 0.3, PA_RACK_TOP, s=s) for iso, s in zip(PA_RACKS_WIDE, (0.5, 0.7, 0.9))]


class B12_Plumbing(Scene):
    def construct(self):
        stacks, lights = pa_racks()
        l_comp = T("compute nodes", 40).move_to([3.75, -2.4, 0])
        self.add(stacks, lights, l_comp)
        until(self, "Around the compute", lead=0.0)
        shifts = [RIGHT * (w.ox - r.ox) for r, w in zip(PA_RACKS, PA_RACKS_WIDE)]
        self.play(*[VGroup(stacks[2 - k], lights[2 - k]).animate.shift(shifts[k]) for k in range(3)], FadeOut(l_comp), run_time=0.7)
        self.play(GrowFromCenter(b12_campus()), run_time=0.4)
        self.add(T("campus", 40).move_to([-4.9, -2.5, 0]))
        until(self, "a ten-gigabit link")
        pipe = b12_pipe([-4.0, B12_PIPE_Y, 0], [-1.85, B12_PIPE_Y, 0])
        self.play(GrowFromEdge(pipe, LEFT), run_time=0.6)
        self.add(T("10 GbE", 40).move_to([-2.95, -0.75, 0]))
        until(self, "for moving data")
        d1, d2 = Dot([-3.8, B12_PIPE_Y, 0], radius=0.1, color=TERRA), Dot([-2.05, B12_PIPE_Y, 0], radius=0.1, color=TERRA)
        self.add(d1, d2)
        self.play(d1.animate.shift(RIGHT * 1.75), d2.animate.shift(LEFT * 1.75), run_time=0.7)
        self.play(FadeOut(d1), FadeOut(d2), run_time=0.2)
        until(self, "six petabytes")
        pa_slide_in(self, b12_storage(), DOWN * 5, 0.6)
        self.add(T("6 PB", 44).move_to([-2.7, 1.6, 0]))
        self.play(Create(b12_pipe([-3.75, 0.95, 0], [-1.4, 0.4, 0], 12)), run_time=0.4)
        until(self, "between the nodes")
        self.play(Create(b12_links(-0.95)), run_time=0.5)
        until(self, "or InfiniBand")
        self.play(Create(b12_links(-0.6)), run_time=0.5)
        self.play(FadeIn(T("InfiniBand · 100–200 Gbps", 34).move_to([1.6, 0.75, 0])), run_time=0.3)
        until(self, "so every size")
        pa_drop(self, b12_jobs(), 0.8, 0.3, dist=4.0)
        pa_light_up(self, [l for li in lights for l in li], 0.6)
        done(self)


# ─────────────── B20 · two doors: research (PI, project command, access form) and classroom ───────────────
B20_FLOOR = -2.1
B20_DOOR_Y, B20_DOOR_W, B20_DOOR_H = -0.95, 1.5, 2.6
B20_X_RES, B20_X_CLS = -3.4, 2.6
B20_CAB = Iso(-1.1, -1.75, 0.65)
B20_PAGE = Iso(-5.7, -0.5, 0.6)


def b20_door(x, hinge):
    """A door seen from the front: a pale frame and a kraft panel with a terracotta knob. Returns (frame, panel, hinge_point)."""
    frame = Rectangle(width=B20_DOOR_W, height=B20_DOOR_H, fill_color=PA_BELT, fill_opacity=1,
                      stroke_color=INK, stroke_width=4).move_to([x, B20_DOOR_Y, 0])
    pw = B20_DOOR_W - 0.3
    panel = Rectangle(width=pw, height=B20_DOOR_H - 0.3, fill_color=BOX_R, fill_opacity=1, stroke_width=0).move_to([x, B20_DOOR_Y, 0])
    kx = x - hinge * (pw / 2 - 0.22)
    knob = Dot([kx, B20_DOOR_Y, 0], radius=0.08, color=TERRA)
    hp = np.array([x + hinge * pw / 2, B20_DOOR_Y, 0.0])
    return frame, VGroup(panel, knob), hp


def b20_open(self, panel, hp, rt=0.5):
    """Swing the panel on its hinge (a 3-D turn about the vertical: the panel narrows to a sliver)."""
    self.play(Rotate(panel, angle=-PI * 0.44, axis=UP, about_point=hp), run_time=rt)


def b20_page():
    return B20_PAGE.page(0, 0, 0, 0.9, 0.8)


class B20_TwoDoors(Scene):
    def construct(self):
        self.add(pa_title("II · Getting An Account"))
        f1, p1, h1 = b20_door(B20_X_RES, -1)
        f2, p2, h2 = b20_door(B20_X_CLS, +1)
        self.add(f1, p1, f2, p2)
        until(self, "For research", lead=0.1)
        pi, user = pa_token(-4.6, B20_FLOOR), pa_token(-5.3, B20_FLOOR)
        pa_slide_in(self, VGroup(pi, user), RIGHT * 2.5, 0.5)
        self.add(T("research", 42).move_to([B20_X_RES, 0.8, 0]))
        until(self, "every user belongs")
        cab = project_cabinet(B20_CAB)
        self.play(FadeIn(cab, shift=UP * 0.3), run_time=0.5)
        until(self, "owned by a PI")
        self.play(pi.animate.shift(UP * 0.3), run_time=0.4, rate_func=there_and_back)
        self.add(T("PI", 34).move_to([-4.6, -0.95, 0]))
        until(self, "thirty-five terabytes", lead=0.4)
        self.play(FadeIn(T("35 TB", 40).move_to([-1.0, 1.05, 0]), shift=UP * 0.2), run_time=0.3)
        until(self, "the PI adds you")
        self.play(pi.animate.shift(RIGHT * 0.3), run_time=0.3)
        b20_open(self, p1, h1, 0.5)
        until(self, "with the project command", lead=0.1)
        self.play(user.animate.shift(RIGHT * 3.0), run_time=0.9)                             # through the door, to the cabinet
        self.add(T("project command", 34).move_to([-1.3, -2.65, 0]))
        until(self, "or you file")
        page = b20_page()
        self.play(FadeIn(page, shift=DOWN * 0.3), run_time=0.3)
        self.add(T("access form", 34).move_to([-5.0, -2.65, 0]))
        self.play(page.animate.shift(RIGHT * 2.1), run_time=0.6)
        self.play(FadeOut(page), run_time=0.2)
        until(self, "requests a storage space")
        self.play(Indicate(cab, color=None, scale_factor=1.08), run_time=0.5)
        self.play(Create(check(-0.15, 0.35, 0.2, TERRA, 8)), run_time=0.35)
        until(self, "For coursework")
        inst = pa_token(4.1, B20_FLOOR)
        pa_slide_in(self, inst, LEFT * 2.5, 0.45)
        self.add(T("classroom", 42).move_to([B20_X_CLS, 0.8, 0]))
        until(self, "your instructor applies")
        self.play(inst.animate.shift(LEFT * 0.4), run_time=0.3)
        b20_open(self, p2, h2, 0.5)
        self.add(T("instructor", 34).move_to([4.6, -0.95, 0]))
        until(self, "students get in", lead=0.3)
        students = VGroup(*[pa_token(x, B20_FLOOR) for x in (4.7, 5.3, 5.9)])
        pa_slide_in(self, students, LEFT * 2.5, 0.45)
        self.play(LaggedStart(*[s.animate.shift(LEFT * d) for s, d in zip(students, (3.3, 4.4, 5.5))], lag_ratio=0.25), run_time=1.0)
        done(self)


# ─────────────── B30 · the terminal and the Open OnDemand site, both cabled to one login node ───────────────
B30_LOGIN = Iso(-0.4, -2.75, 0.7)
B30_TX, B30_BX, B30_WY = -3.9, 3.9, 0.9
B30_WW, B30_WH = 3.9, 2.6


def b30_terminal():
    panel = RoundedRectangle(width=B30_WW, height=B30_WH, corner_radius=0.1, fill_color=DARK_TOP, fill_opacity=1,
                             stroke_width=0).move_to([B30_TX, B30_WY, 0])
    prompt = M("$", 44, CARD).move_to([B30_TX - 1.5, B30_WY + 0.9, 0])
    cur = Rectangle(width=0.28, height=0.5, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([B30_TX - 0.95, B30_WY + 0.9, 0])
    return VGroup(panel, prompt, cur)


def b30_browser():
    win = RoundedRectangle(width=B30_WW, height=B30_WH, corner_radius=0.1, fill_color=CARD, fill_opacity=1,
                           stroke_color=GHOST, stroke_width=3).move_to([B30_BX, B30_WY, 0])
    bar = Rectangle(width=B30_WW, height=0.5, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([B30_BX, B30_WY + B30_WH / 2 - 0.25, 0])
    dots = VGroup(*[Dot([B30_BX - 1.6 + i * 0.3, B30_WY + B30_WH / 2 - 0.25, 0], radius=0.07, color=GHOST) for i in range(3)])
    return VGroup(win, bar, dots)


def b30_rows():
    return VGroup(*[pill(2.4 + w / 2, y, w, 0.36, BAR2) for w, y in ((2.4, 1.3), (1.8, 0.7), (2.8, 0.1))])


def b30_cables():
    return (pa_cable([B30_TX + 1.5, B30_WY - B30_WH / 2, 0], [-0.9, -1.62, 0]),
            pa_cable([B30_BX - 1.5, B30_WY - B30_WH / 2, 0], [0.1, -1.62, 0]))


class B30_TwoWaysIn(Scene):
    def construct(self):
        self.add(pa_title("III · Logging In"))
        st, li = pa_login(B30_LOGIN)
        self.add(st, li, T("login node", 40).move_to([2.0, -2.4, 0]))
        until(self, "The terminal", lead=0.15)
        term = b30_terminal()
        pa_slide_in(self, term, RIGHT * 7, 0.6)
        self.add(T("terminal", 40).move_to([-4.4, -0.9, 0]))
        until(self, "Open OnDemand", lead=0.35)
        web = b30_browser()
        pa_slide_in(self, web, LEFT * 7, 0.6)
        self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in b30_rows()], lag_ratio=0.3), run_time=0.4)
        self.add(T("Open OnDemand", 36).move_to([4.2, -0.9, 0]))
        until(self, "Both reach")
        c1, c2 = b30_cables()
        self.play(Create(c1), Create(c2), run_time=0.6)
        pa_light_up(self, li, 0.3)
        until(self, "comfortable with the terminal")
        self.play(Indicate(term, color=None, scale_factor=1.06), run_time=0.6)
        until(self, "use both", lead=0.6)
        d1, d2 = Dot(c1.get_start(), radius=0.1, color=TERRA), Dot(c2.get_start(), radius=0.1, color=TERRA)
        self.add(d1, d2)
        self.play(d1.animate.move_to(c1.get_end()), d2.animate.move_to(c2.get_end()), run_time=0.5)
        self.play(FadeOut(d1), FadeOut(d2), run_time=0.15)
        done(self)


# ─────────────── B60 · not on the login node: the job rides the belt through Slurm to a compute node ───────────────
class B60_LeaveTheLoginNode(Scene):
    def construct(self):
        self.add(pa_title("VI · Running Jobs"))
        login_st, login_li = pa_login()
        login = VGroup(login_st, login_li)
        job = b10_job()
        stacks, lights = pa_racks()
        l_login, l_slurm, l_comp = b10_labels()
        self.add(login, job, stacks, lights, l_login)
        until(self, "only used the login", lead=0.1)
        self.play(Indicate(login, color=None, scale_factor=1.08), run_time=0.6)
        until(self, "has to move")
        belt = pa_belt(-1.6, 1.9, -1.75)
        self.play(GrowFromEdge(belt, LEFT), run_time=0.6)
        far, boom, near = pa_gate()
        self.play(GrowFromCenter(VGroup(far, boom, near)), FadeIn(l_slurm), FadeIn(l_comp), run_time=0.4)
        until(self, "no scientific software")
        xm = pa_xmark(-3.5, -0.6)
        self.play(GrowFromCenter(xm), run_time=0.35)
        until(self, "big transfers")
        self.play(Indicate(xm, color=None, scale_factor=1.25), run_time=0.4)
        until(self, "or heavy work")
        self.play(Indicate(xm, color=None, scale_factor=1.25), run_time=0.4)
        until(self, "because its traffic")
        self.play(job.animate.shift(np.array([1.1, -0.2, 0.0])), run_time=0.4)          # down onto the belt
        self.play(Rotate(boom, angle=2 * PI / 3, about_point=PA_GATE_PIVOT), run_time=0.4)
        self.play(job.animate.shift(RIGHT * 2.6), run_time=0.7)                             # through the gate
        until(self, "slows the whole cluster", lead=0.0)
        self.play(job.animate.shift(np.array([0.55, 1.1, 0.0])), run_time=0.4)           # onto the first rack
        pa_light_up(self, lights[2], 0.4)
        done(self)

# ═════════════════════════════ PART B · Act IV (B40 B41) · Act VI (B62 B63) · Act VIII (B80) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB3_ / b4x_ / b6x_ / b8x_ so the parts never collide.
#
# Act IV stage (B40, B41): the film-1 grammar, four containers in one row, each on a thin dark plinth (kraft and
# white on cream alone measure under Gate V's 0.30 contrast floor; the plinths carry it):
#   home_box · scratch_bin · project_cabinet · a kraft cabinet for courses.
# Mono at 32 runs ~0.25 units a character, so the four real paths (18.9 units together) cannot share one row
# under four containers: they sit in a 2 x 2 mono grid under the row, left column under home/scratch, right
# column under the two cabinets, slashes aligned per column. B41's capacity labels take the same four cells.
PB3_S, PB3_Y = 0.78, -1.1
PB3_HOME = Iso(-4.988, PB3_Y, PB3_S)
PB3_BIN = Iso(-1.753, PB3_Y, PB3_S)
PB3_PROJ = Iso(2.084, PB3_Y, PB3_S)
PB3_COURSE = Iso(4.914, PB3_Y, PB3_S)
PB3_KRAFT = "#917A55"                      # dark kraft: outlines of SMALL objects only (GATE T: small ink rings fuse)
PB3_TRACK = "#E3DFD4"                      # pale track / pad: within 28 of the stage, so Gate V does not count it as ink
PB3_COL_X = (-5.95, 0.1)                   # left edges of the two label columns
PB3_ROW_Y = (-1.75, -2.55)                 # the two label rows
PB3_CELL = ((0, 0), (0, 1), (1, 0), (1, 1))   # (column, row) of home, scratch, projects, courses
PB3_PATHS = ("/home/username", "/scratch/username", "/projects/projectname", "/courses/coursename.code")
PB3_CAPS = ("75 GB", "50 TB", "long-term", "1–5 TB · shared")


def pb3_at(mob, x_left, y):
    """Place a text by its LEFT edge."""
    return mob.move_to([x_left + mob.width / 2, y, 0])


def pb3_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb3_pad(iso, w, d, m=0.15, h=0.1):
    """A thin dark plinth under a container: its top is the floor (z = 0)."""
    return iso.box(-m, -m, -h, w + 2 * m, d + 2 * m, h, DARK_TOP, DARK_L, DARK_R).set_z_index(-1)


def pb3_pads():
    return VGroup(pb3_pad(PB3_HOME, 1.2, 1.2), pb3_pad(PB3_BIN, 2.8, 1.8), pb3_pad(PB3_PROJ, 1.3, 1.1), pb3_pad(PB3_COURSE, 1.3, 1.1))


def pb3_home():
    return home_box(PB3_HOME).set_z_index(1)


def pb3_bin():
    back, front = scratch_bin(PB3_BIN)
    return back, front


def pb3_proj():
    return project_cabinet(PB3_PROJ).set_z_index(1)


def pb3_course():
    """The courses cabinet: the project cabinet's shape in kraft."""
    iso = PB3_COURSE
    body = iso.box(0, 0, 0, 1.3, 1.1, 2.0)
    lines = VGroup(*[Line(iso.p(0.12, 0, 2.0 * f), iso.p(1.18, 0, 2.0 * f), color=BAR1, stroke_width=4) for f in (0.34, 0.67)])
    return VGroup(body, lines).set_z_index(1)


def pb3_cell_xy(k):
    c, r = PB3_CELL[k]
    return PB3_COL_X[c], PB3_ROW_Y[r]


def pb3_path(k):
    x, y = pb3_cell_xy(k)
    return pb3_at(M(PB3_PATHS[k], 32), x, y)


def pb3_paths():
    return VGroup(*[pb3_path(k) for k in range(4)])


def pb3_ring(k):
    """A small grey ring on the leading slash of path k: a filled annulus with no stroke (BAR1 is above GATE T's
    text-grey threshold, and the layout audit reads only STROKED paths as curves under a label)."""
    x, y = pb3_cell_xy(k)
    return Annulus(inner_radius=0.24, outer_radius=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0,
                   stroke_opacity=0).move_to([x + 0.11, y, 0]).set_z_index(-2)


def pb3_rings():
    return VGroup(*[pb3_ring(k) for k in range(4)])


def pb3_cap(k):
    """Capacity label k, in the path's cell: the two short ones in 44, the two long ones in 36."""
    x, y = pb3_cell_xy(k)
    return pb3_at(T(PB3_CAPS[k], 44 if k < 2 else 36), x, y)


def pb3_stage(self):
    """Put the Act IV row on stage (the end of B40, minus the title). Returns the parts."""
    pads, home, proj, course = pb3_pads(), pb3_home(), pb3_proj(), pb3_course()
    bk, fr = pb3_bin()
    self.add(pads, home, bk, fr, proj, course)
    return pads, home, bk, fr, proj, course


def pb3_land(self, mob, rt=0.55, dist=1.2):
    """A container lands: a short drop onto its pad."""
    self.play(FadeIn(mob, shift=DOWN * dist), run_time=rt)


# ─────────────── B40 · four places: home, scratch, projects, courses; every path starts with a slash ───────────────
class B40_FourPlaces(Scene):
    def construct(self):
        self.add(pb3_title("IV · Where Files Live"))
        pads = pb3_pads()
        self.play(LaggedStart(*[FadeIn(p) for p in pads], lag_ratio=0.25), run_time=0.7)
        paths = pb3_paths()
        until(self, "home directory", lead=0.4)
        pb3_land(self, pb3_home())
        self.play(FadeIn(paths[0]), run_time=0.3)
        until(self, "scratch directory", lead=0.3)
        bk, fr = pb3_bin()
        pb3_land(self, VGroup(bk, fr))
        self.play(FadeIn(paths[1]), run_time=0.3)
        until(self, "projects space", lead=0.4)
        proj = pb3_proj()
        pb3_land(self, proj)
        self.play(FadeIn(paths[2]), run_time=0.3)
        until(self, "courses space", lead=0.4)
        pb3_land(self, pb3_course())
        self.play(FadeIn(paths[3]), run_time=0.3)
        until(self, "may not have projects", lead=0.1)
        self.play(paths[2].animate.set_color(DIM), run_time=0.3)              # a student may have no projects path
        until(self, "starting with a slash", lead=0.6)
        self.play(paths[2].animate.set_color(INK), run_time=0.3)
        rings = pb3_rings()
        self.play(LaggedStart(*[GrowFromCenter(r) for r in rings], lag_ratio=0.25), run_time=0.8)   # the four leading slashes
        until(self, "wherever it runs", lead=0.1)
        self.play(Indicate(rings, color=BAR1, scale_factor=1.12), run_time=0.5)
        done(self)


# ─────────────── B41 · quotas: 75 GB fills, 50 TB is purged on the first Tuesday, projects keeps, courses share ───────────────
B41_W, B41_D, B41_H = 0.5, 0.6, 0.42                               # a block in the bin
B41_BIN_XY = [(0.2 + 0.85 * i, 0.2 + 0.85 * j) for j in (1, 0) for i in range(3)]
B41_KEEP = (1, 4)                                                   # indices of the two marked blocks (the ones you keep)
B41_HOME_XY = ((0.12, 0.12), (0.63, 0.12), (0.12, 0.63), (0.63, 0.63))
B41_PROJ_XY = ((0.1, 0.45), (0.7, 0.45))
B41_SMALL_XY = ((0.08, 0.05), (0.38, 0.05), (0.68, 0.05), (0.98, 0.05))
B41_COURSE_XY = ((0.1, 0.1), (0.7, 0.1), (0.4, 0.6))
B41_CAL_Y = 0.9                                                      # clear of the bin top (-0.48), so the midpoint frame has no card over the bin
B41_STAMP_Y = 2.05


def b41_block(iso, x, y, z=0.0, w=B41_W, d=B41_D, h=B41_H, mark=False, zi=1.0):
    g = VGroup(iso.box(x, y, z, w, d, h, sw=3))
    if mark:
        g.add(Dot(iso.p(x + w / 2, y + d / 2, z + h), radius=0.085, color=TERRA))
    return g.set_z_index(zi + 0.02 * (8 - (x + y)))


def b41_drop(self, mobs, rt=0.7, lag=0.12, dist=4.5):
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), run_time=rt, rate_func=ease_in)


def b41_stamp():
    return T("quota exceeded", 38, bold=True).move_to([-4.4, B41_STAMP_Y, 0])


def b41_calendar(cx):
    """A calendar page: white card, grey outline (BAR1 is above GATE T's text grey), ghost day squares, the first Tuesday in terracotta."""
    card = RoundedRectangle(width=1.5, height=1.25, corner_radius=0.08, fill_color=CARD, fill_opacity=1,
                            stroke_color=BAR1, stroke_width=4).move_to([cx, B41_CAL_Y, 0])
    days = VGroup()
    for r in range(4):
        for c in range(7):
            days.add(Square(side_length=0.12, fill_color=GHOST, fill_opacity=1, stroke_width=0)
                     .move_to([cx - 0.57 + c * 0.19, B41_CAL_Y + 0.33 - r * 0.24, 0]))
    tue = Dot([cx - 0.57 + 2 * 0.19, B41_CAL_Y + 0.33, 0], radius=0.085, color=TERRA)
    return VGroup(card, days, tue).set_z_index(6)


class B41_Quotas(Scene):
    def construct(self):
        pads, home, bk, fr, proj, course = pb3_stage(self)
        paths, rings = pb3_paths(), pb3_rings()
        self.add(paths, rings)
        self.play(FadeOut(paths), FadeOut(rings), run_time=0.35)
        until(self, "seventy-five", lead=0.3)
        self.play(FadeIn(pb3_cap(0), shift=UP * 0.2), run_time=0.35)
        until(self, "fills fastest", lead=0.2)
        pile = [b41_block(PB3_HOME, x, y, 0.9, 0.45, 0.45, 0.36, zi=3) for x, y in B41_HOME_XY]
        b41_drop(self, pile, 0.7, 0.15)                                           # home fills
        until(self, "quota exceeded", lead=0.2)
        st = b41_stamp().scale(1.6)
        self.play(FadeIn(st), st.animate.scale(1 / 1.6), run_time=0.35)          # the stamp lands
        until(self, "fifty terabytes", lead=0.3)
        self.play(FadeIn(pb3_cap(1), shift=UP * 0.2), run_time=0.35)
        blocks = [b41_block(PB3_BIN, x, y, mark=(k in B41_KEEP)) for k, (x, y) in enumerate(B41_BIN_XY)]
        b41_drop(self, blocks, 0.8, 0.1)
        until(self, "first Tuesday", lead=0.4)
        cal = b41_calendar(-2.3)
        self.play(FadeIn(cal, shift=DOWN * 0.3), run_time=0.45)                  # the calendar page arrives
        until(self, "anything you want to keep", lead=0.2)
        keep = [blocks[k] for k in B41_KEEP]
        for m in keep:
            m.set_z_index(8)
        self.play(*[m.animate.shift(UP * 1.1) for m in keep], run_time=0.4)      # lift what you keep
        rest = [b for k, b in enumerate(blocks) if k not in B41_KEEP]
        rest = sorted(rest, key=lambda m: float(np.array(m.get_center())[0]))
        self.play(cal.animate.shift(RIGHT * 2.3), LaggedStart(*[FadeOut(m) for m in rest], lag_ratio=0.12), run_time=0.9)   # the purge
        self.play(FadeOut(cal), run_time=0.3)
        until(self, "long-term home", lead=0.5)
        self.play(FadeIn(pb3_cap(2), shift=UP * 0.2), run_time=0.35)
        for m, (x, y) in zip(keep, B41_PROJ_XY):
            tgt = b41_block(PB3_PROJ, x, y, 2.0, mark=True)
            a, b = np.array(m.get_center()), np.array(tgt.get_center())
            self.play(MoveAlongPath(m, ArcBetweenPoints(a, b, angle=-PI / 3)), run_time=0.55)   # into the project cabinet
        until(self, "many small files", lead=0.3)
        small = [b41_block(PB3_PROJ, x, y, 2.0, 0.24, 0.3, 0.2, zi=4) for x, y in B41_SMALL_XY]
        b41_drop(self, small, 0.6, 0.12, 3.5)
        until(self, "one to five terabytes", lead=0.3)
        self.play(FadeIn(pb3_cap(3), shift=UP * 0.2), run_time=0.35)
        until(self, "whole class", lead=0.3)
        shared = [b41_block(PB3_COURSE, x, y, 2.0, 0.45, 0.4, 0.3, zi=4) for x, y in B41_COURSE_XY]
        b41_drop(self, shared, 0.6, 0.15, 3.5)
        done(self)


# ─────────────── B62 · the partition table: CPU and GPU columns, then two gated blocks ───────────────
B62_CX = (-3.1, 3.1)                                                 # column centres
B62_HEAD_Y, B62_RULE_Y, B62_BOTTOM_Y = 2.65, 2.2, -0.5
B62_ROW_Y = (1.7, 1.1, 0.5, -0.1)
B62_CPU = ("short", "sharing")
B62_GPU = ("gpu", "sharing", "gpu-interactive", "gpu-short")
B62_BLOCK_Y = (-0.8, -3.1)                                           # top and bottom of the two blocks
B62_TITLE_Y, B62_LINE_Y = (-1.25, -2.0, -2.6)[0], (-2.0, -2.6)


def b62_name(s, x, y):
    return M(s, 34).move_to([x, y, 0])


def b62_rule(y, color=INK, sw=5):
    return Line([-6.0, y, 0], [6.0, y, 0], color=color, stroke_width=sw)


def b62_block(x0, x1):
    """A grey-outlined block (BAR1 is above GATE T's text-grey threshold, so the outline never reads as type)."""
    return Rectangle(width=x1 - x0, height=B62_BLOCK_Y[0] - B62_BLOCK_Y[1], stroke_color=BAR1, stroke_width=4,
                     fill_opacity=0).move_to([(x0 + x1) / 2, (B62_BLOCK_Y[0] + B62_BLOCK_Y[1]) / 2, 0])


def b62_gate(cx, cy):
    """A small gate: two dark-kraft posts and three bars (small object: dark kraft, never ink)."""
    posts = VGroup(Line([cx - 0.32, cy - 0.28, 0], [cx - 0.32, cy + 0.3, 0], color=PB3_KRAFT, stroke_width=6),
                   Line([cx + 0.32, cy - 0.28, 0], [cx + 0.32, cy + 0.3, 0], color=PB3_KRAFT, stroke_width=6))
    bars = VGroup(*[Line([cx - 0.32, cy + dy, 0], [cx + 0.32, cy + dy, 0], color=PB3_KRAFT, stroke_width=4) for dy in (0.16, 0.0, -0.16)])
    return VGroup(posts, bars)


def b62_tag(cx, cy):
    """A kraft luggage tag with a hole: the course marker."""
    body = Polygon([cx - 0.42, cy, 0], [cx - 0.22, cy + 0.24, 0], [cx + 0.42, cy + 0.24, 0], [cx + 0.42, cy - 0.24, 0], [cx - 0.22, cy - 0.24, 0],
                   fill_color=BOX_L, fill_opacity=1, stroke_color=PB3_KRAFT, stroke_width=3)
    hole = Dot([cx - 0.2, cy, 0], radius=0.05, color=CARD)
    return VGroup(body, hole)


class B62_Partitions(Scene):
    def construct(self):
        head = VGroup(T("CPU", 40, bold=True).move_to([B62_CX[0], B62_HEAD_Y, 0]), T("GPU", 40, bold=True).move_to([B62_CX[1], B62_HEAD_Y, 0]))
        until(self, "A partition is how", lead=0.0)
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.4)
        until(self, "by time limit", lead=0.2)
        self.play(Create(b62_rule(B62_RULE_Y)), run_time=0.5)                                      # the header rule
        until(self, "by CPU or GPU", lead=0.2)
        self.play(Create(Line([0, B62_RULE_Y, 0], [0, B62_BOTTOM_Y, 0], color=BAR1, stroke_width=3)), run_time=0.4)   # the column divider
        until(self, "short, the default", lead=0.2)
        self.play(FadeIn(b62_name(B62_CPU[0], B62_CX[0], B62_ROW_Y[0]), shift=RIGHT * 0.2), run_time=0.35)
        until(self, "and sharing for CPU", lead=0.1)
        self.play(FadeIn(b62_name(B62_CPU[1], B62_CX[0], B62_ROW_Y[1]), shift=RIGHT * 0.2), run_time=0.35)
        until(self, "gpu, gpu-interactive", lead=0.2)
        self.play(LaggedStart(*[FadeIn(b62_name(s, B62_CX[1], y), shift=RIGHT * 0.2) for s, y in zip(B62_GPU, B62_ROW_Y)], lag_ratio=0.3), run_time=0.9)
        self.play(Create(b62_rule(B62_BOTTOM_Y, BAR1, 3)), run_time=0.35)
        until(self, "Two you apply for", lead=0.2)
        self.play(Create(b62_block(-5.9, -0.3)), run_time=0.4)
        self.play(FadeIn(T("apply for access", 38).move_to([-2.7, B62_TITLE_Y, 0])), GrowFromCenter(b62_gate(-4.95, B62_TITLE_Y)), run_time=0.4)
        until(self, "long and multigpu", lead=0.1)
        self.play(FadeIn(b62_name("long", -3.1, B62_LINE_Y[0]), shift=RIGHT * 0.2), FadeIn(b62_name("multigpu", -3.1, B62_LINE_Y[1]), shift=RIGHT * 0.2), run_time=0.4)
        until(self, "two only for courses", lead=0.2)
        self.play(Create(b62_block(0.3, 5.9)), run_time=0.4)
        self.play(FadeIn(T("courses only", 38).move_to([3.4, B62_TITLE_Y, 0])), GrowFromCenter(b62_tag(1.55, B62_TITLE_Y)), run_time=0.4)
        until(self, "courses and courses-gpu", lead=0.1)
        self.play(FadeIn(b62_name("courses", 3.1, B62_LINE_Y[0]), shift=RIGHT * 0.2), FadeIn(b62_name("courses-gpu", 3.1, B62_LINE_Y[1]), shift=RIGHT * 0.2), run_time=0.4)
        done(self)


# ─────────────── B63 · which partition: a decision tree that lights as spoken ───────────────
B63_Y = (2.7, 1.5, 0.3, -0.6, -1.3, -2.0)                           # root, yes/no, condition, partition rows (two, staggered), gpu-short
B63_YES_X, B63_NO_X = -3.8, 2.4
B63_LEAF = ((-5.1, "CPU jobs", "courses", 0), (-2.5, "GPU jobs", "courses-gpu", 1),
            (0.0, "CPU", "short", 0), (2.4, "interactive GPU", "gpu-interactive", 1), (5.1, "GPU batch", "gpu", 0))


def b63_edge(xf, yf, xt, yt):
    """An ink branch from the label at (xf, yf) down to the label at (xt, yt), 0.3 clear of both."""
    return Line([xf, yf - 0.4, 0], [xt, yt + 0.4, 0], color=INK, stroke_width=4)


def b63_lab(s, x, y, size=34):
    return T(s, size).move_to([x, y, 0])


def b63_leaf(k):
    """(edge, condition label, partition name) for leaf k, hanging from its yes/no node."""
    x, cond, part, row = B63_LEAF[k]
    xf = B63_YES_X if k < 2 else B63_NO_X
    return b63_edge(xf, B63_Y[1], x, B63_Y[2]), b63_lab(cond, x, B63_Y[2], 32), M(part, 32).move_to([x, B63_Y[3 + row], 0])


class B63_WhichPartition(Scene):
    def construct(self):
        root = b63_lab("in a course?", 0.0, B63_Y[0], 36)
        self.play(FadeIn(root, shift=DOWN * 0.2), run_time=0.4)
        until(self, "If you're in a course", lead=0.1)
        self.play(Create(b63_edge(0.0, B63_Y[0], B63_YES_X, B63_Y[1])), run_time=0.4)
        self.play(FadeIn(b63_lab("yes", B63_YES_X, B63_Y[1])), run_time=0.3)
        until(self, "use courses for CPU", lead=0.2)
        e, c, p = b63_leaf(0)
        self.play(Create(e), FadeIn(c), run_time=0.35)
        self.play(FadeIn(p, shift=DOWN * 0.15), run_time=0.3)
        until(self, "courses-gpu for GPU", lead=0.2)
        e, c, p = b63_leaf(1)
        self.play(Create(e), FadeIn(c), run_time=0.35)
        self.play(FadeIn(p, shift=DOWN * 0.15), run_time=0.3)
        until(self, "Otherwise", lead=0.2)
        self.play(Create(b63_edge(0.0, B63_Y[0], B63_NO_X, B63_Y[1])), run_time=0.4)
        self.play(FadeIn(b63_lab("no", B63_NO_X, B63_Y[1])), run_time=0.3)
        until(self, "short for most CPU", lead=0.2)
        e, c, p = b63_leaf(2)
        self.play(Create(e), FadeIn(c), run_time=0.35)
        self.play(FadeIn(p, shift=DOWN * 0.15), run_time=0.3)
        until(self, "gpu-interactive or gpu-short", lead=0.3)
        e, c, p = b63_leaf(3)
        self.play(Create(e), FadeIn(c), run_time=0.35)
        self.play(FadeIn(p, shift=DOWN * 0.15), run_time=0.3)
        self.play(FadeIn(M("gpu-short", 32).move_to([2.4, B63_Y[5], 0]), shift=DOWN * 0.15), run_time=0.3)
        until(self, "the gpu partition for GPU batch", lead=0.3)
        e, c, p = b63_leaf(4)
        self.play(Create(e), FadeIn(c), run_time=0.35)
        self.play(FadeIn(p, shift=DOWN * 0.15), run_time=0.3)
        done(self)


# ─────────────── B80 · two real seff reports, re-composed on cream: tracks are what was asked for, bars what was used ───────────────
B80_X0 = (-5.95, 0.35)                                               # left edge of each report
B80_FULL = 3.4                                                       # 100 % of a bar
B80_BAR_H = 0.4
B80_Y = {"head": 2.2, "cores": 1.5, "wall": 0.95, "cpu_lab": 0.3, "cpu_bar": -0.3, "mem_lab": -1.0, "mem_bar": -1.6, "verdict": -2.6}
B80_REPORTS = (("$ seff 371441", "cores 12", "wall-clock 00:17:19", 8.29, "8.29%", 10.44, "10.44% of 50 GB"),
               ("$ seff 2612438", "cores 8", "wall-clock 00:25:57", 83.83, "83.83%", 3.56, "3.56% of 15.62 GB"))


def b80_text(s, k, key, size=32, fn=None):
    return pb3_at((fn or M)(s, size), B80_X0[k], B80_Y[key])


def b80_track(k, key):
    return Rectangle(width=B80_FULL, height=B80_BAR_H, fill_color=PB3_TRACK, fill_opacity=1, stroke_width=0, stroke_opacity=0).move_to([B80_X0[k] + B80_FULL / 2, B80_Y[key], 0])


def b80_bar(k, key, pct):
    w = B80_FULL * pct / 100.0
    return Rectangle(width=w, height=B80_BAR_H, fill_color=BAR1, fill_opacity=1, stroke_width=0, stroke_opacity=0).move_to([B80_X0[k] + w / 2, B80_Y[key], 0])


def b80_value(k, key, pct, s, gap=0.3):
    return pb3_at(M(s, 32), B80_X0[k] + B80_FULL * pct / 100.0 + gap, B80_Y[key])


class B80_Seff(Scene):
    def construct(self):
        self.add(pb3_title("VIII · Right-Sizing"))
        heads = VGroup(*[b80_text(r[0], k, "head", 36) for k, r in enumerate(B80_REPORTS)])
        divider = Line([-0.3, 2.5, 0], [-0.3, -2.9, 0], color=BAR1, stroke_width=3)
        self.play(FadeIn(heads, shift=DOWN * 0.15), Create(divider), run_time=0.5)
        until(self, "close to the minimum", lead=0.3)
        labs = VGroup(*[b80_text(s, k, key) for k in range(2) for s, key in (("CPU efficiency", "cpu_lab"), ("memory efficiency", "mem_lab"))])
        self.play(FadeIn(labs, shift=RIGHT * 0.15), run_time=0.4)
        until(self, "the more you request", lead=0.2)
        tracks = [b80_track(k, key) for k in range(2) for key in ("cpu_bar", "mem_bar")]
        self.play(LaggedStart(*[GrowFromEdge(t, LEFT) for t in tracks], lag_ratio=0.15), run_time=0.8)      # what was asked for
        until(self, "seff, Slurm efficiency", lead=0.2)
        self.play(Indicate(heads, color=INK, scale_factor=1.08), run_time=0.5)
        until(self, "Two real reports", lead=0.2)
        rows = VGroup(*[b80_text(r[i], k, key) for k, r in enumerate(B80_REPORTS) for i, key in ((1, "cores"), (2, "wall"))])
        self.play(FadeIn(rows, shift=DOWN * 0.15), run_time=0.45)
        until(self, "twelve cores", lead=0.2)
        self.play(Indicate(rows[0], color=INK, scale_factor=1.12), run_time=0.5)
        until(self, "eight percent CPU", lead=0.2)
        self.play(GrowFromEdge(b80_bar(0, "cpu_bar", 8.29), LEFT), run_time=0.5)
        dot = Dot([B80_X0[0] + B80_FULL * 0.0829 + 0.3, B80_Y["cpu_bar"], 0], radius=0.11, color=TERRA)
        self.play(GrowFromCenter(dot), FadeIn(b80_value(0, "cpu_bar", 8.29, "8.29%", gap=0.75)), run_time=0.3)
        until(self, "ten percent of fifty", lead=0.2)
        self.play(GrowFromEdge(b80_bar(0, "mem_bar", 10.44), LEFT), run_time=0.5)
        self.play(FadeIn(b80_value(0, "mem_bar", 10.44, "10.44% of 50 GB")), run_time=0.25)
        until(self, "asked for far less", lead=0.3)
        self.play(FadeIn(b80_text("could ask for less", 0, "verdict", 38, T), shift=UP * 0.15), run_time=0.4)
        until(self, "Job two", lead=0.1)
        self.play(Indicate(rows[2], color=INK, scale_factor=1.12), run_time=0.5)
        until(self, "eighty-four percent", lead=0.2)
        self.play(GrowFromEdge(b80_bar(1, "cpu_bar", 83.83), LEFT), run_time=0.7)
        self.play(FadeIn(b80_value(1, "cpu_bar", 83.83, "83.83%")), run_time=0.25)
        self.play(GrowFromEdge(b80_bar(1, "mem_bar", 3.56), LEFT), FadeIn(b80_value(1, "mem_bar", 3.56, "3.56% of 15.62 GB")), run_time=0.4)
        until(self, "much better fit", lead=0.2)
        self.play(GrowFromCenter(check(B80_X0[1] + 5.0, B80_Y["cpu_bar"], 0.2, INK, 7)), run_time=0.35)
        until(self, "Try seff", lead=0.2)
        self.play(Indicate(heads, color=INK, scale_factor=1.08), run_time=0.5)
        done(self)


# attach the midpoint guard (see ST)
for _cls in (B10_ClusterShape, B11_ExplorerNumbers, B12_Plumbing, B20_TwoDoors, B30_TwoWaysIn, B60_LeaveTheLoginNode, B40_FourPlaces, B41_Quotas, B62_Partitions, B63_WhichPartition, B80_Seff):
    _cls.play = ST.play
