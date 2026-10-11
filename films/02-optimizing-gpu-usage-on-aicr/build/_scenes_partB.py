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
