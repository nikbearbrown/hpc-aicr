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
