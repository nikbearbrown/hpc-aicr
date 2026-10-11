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
