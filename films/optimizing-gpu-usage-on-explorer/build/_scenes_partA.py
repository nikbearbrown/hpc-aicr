# ═════════════════════════════ PART A — Acts I and II (manim beats) ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


class B10_QuietFailures(Scene):
    """A job finishes with a check and no error; three branches show the wrong card, the CPU instead, and a hidden card."""
    def construct(self):
        title = act_title("I · Do You Have The GPU?")
        job = job2(-5.2, 1.9)
        post_l = Line([-3.6, 1.4, 0], [-3.6, 2.5, 0], color=BAR2, stroke_width=10)
        post_r = Line([-2.4, 1.4, 0], [-2.4, 2.5, 0], color=BAR2, stroke_width=10)
        ck = check(-3.0, 1.95, s=0.3, color=TERRA, w=12)
        noerr = lab_l("no error", -1.6, 1.95, 38)
        # column 1: asked for / got
        big = gpu_card(-4.5, -0.3, w=2.0, h=1.2)
        small = gpu_card(-4.5, -1.55, w=1.3, h=0.8, lit=True)
        t_ask = lab_l("asked for", -3.2, -0.3, 32)
        t_got = lab_l("got", -3.2, -1.55, 32)
        c1 = lab_c("wrong card", -3.9, -2.75, 36)
        # column 2: the CPU runs it
        dark = gpu_card(-0.2, -0.3, w=1.7, h=1.0)
        cpu = cpu_chip(-0.2, -1.65)
        jb = job2(-0.2, -1.65, 0.5)
        c2 = lab_c("CPU instead", 0.0, -2.75, 36)
        # column 3: a setting hides the card
        hid = gpu_card(4.0, -0.55, w=1.9, h=1.1)
        sh = chip("shell", 3.6, -1.6, size=34)
        c3 = lab_c("hidden card", 4.0, -2.75, 36)

        self.play(FadeIn(title), FadeIn(job), run_time=0.4)
        hear(self, "Three things", lead=0.0)
        self.play(FadeIn(post_l), FadeIn(post_r), job.animate.move_to([-3.0, 1.9, 0]), run_time=0.7)
        self.play(Create(ck), FadeIn(noerr), run_time=0.4)
        hear(self, "You ask", lead=0.1)
        self.play(FadeIn(big), FadeIn(t_ask), run_time=0.4)
        hear(self, "and get another", lead=0.25)
        self.play(FadeIn(small), FadeIn(t_got), FadeIn(c1), run_time=0.45)
        hear(self, "The software", lead=0.1)
        self.play(FadeIn(dark), run_time=0.3)
        hear(self, "quietly runs", lead=0.15)
        self.play(FadeIn(cpu), FadeIn(c2), run_time=0.35)
        self.play(FadeIn(jb), cpu.light.animate.set_color(TERRA), run_time=0.3)
        hear(self, "Or a setting", lead=0.1)
        self.play(FadeIn(hid), run_time=0.35)
        hear(self, "hides", lead=0.2)
        self.play(FadeIn(sh), hid.animate.set_opacity(0.3), FadeIn(c3), run_time=0.5)
        done(self)


class B11_Partitions(Scene):
    """Five bars on an hours ruler: sharing 1, gpu-short 2, gpu-interactive 2, gpu 8, multigpu 24 (hatched, access request)."""
    def construct(self):
        title = act_title("I · Do You Have The GPU?")
        x0, sc, bh = -2.2, 0.3, 0.55
        ys = [2.0, 1.1, 0.2, -0.7, -1.6]
        names = ["sharing", "gpu-short", "gpu-interactive", "gpu", "multigpu"]
        hours = [1, 2, 2, 8, 24]
        axis = Line([x0, 2.5, 0], [x0, -2.05, 0], color=BAR2, stroke_width=6)
        rl = Line([x0, -2.1, 0], [x0 + 24 * sc, -2.1, 0], color=INK, stroke_width=6)
        rt = VGroup(*[Line([x0 + v * sc, -2.1, 0], [x0 + v * sc, -2.38, 0], color=INK, stroke_width=6) for v in range(0, 25, 4)])
        rn = VGroup(*[T(str(v), 32).move_to([x0 + v * sc, -2.7, 0]) for v in range(0, 25, 4)])
        hrs = T("hours", 34).move_to([x0 - 0.7, -2.7, 0])
        labs = [M(n, 32) for n in names]
        for lb, y in zip(labs, ys):
            lb.move_to([x0 - 0.3 - lb.width / 2, y, 0])
        bars = []
        for i, (h, y) in enumerate(zip(hours, ys)):
            fill = BAR2 if i != 4 else PAGE_TOP
            b = Rectangle(width=h * sc, height=bh, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x0 + h * sc / 2, y, 0])
            bars.append(b)
        hat = hatch(x0, x0 + 24 * sc, ys[4] - bh / 2 + 0.03, ys[4] + bh / 2 - 0.03, gap=0.22)
        multi = VGroup(bars[4], hat)
        tg = [None, lab_l("tests", x0 + 2 * sc + 0.25, ys[1], 32), lab_l("interactive", x0 + 2 * sc + 0.25, ys[2], 32),
              lab_l("training", x0 + 8 * sc + 0.25, ys[3], 32)]
        acc = lab_l("access request", x0 + 24 * sc - 2.45, ys[4] + 0.55, 32)

        self.play(FadeIn(title), Create(axis), Create(rl), FadeIn(rt), FadeIn(rn), FadeIn(hrs), *[FadeIn(l) for l in labs], run_time=0.8)
        hear(self, "GPU Short", lead=0.2)
        self.play(GrowFromEdge(bars[1], LEFT), run_time=0.5)
        hear(self, "Interactive", lead=0.2)
        self.play(GrowFromEdge(bars[2], LEFT), FadeIn(tg[1]), run_time=0.5)
        hear(self, "tests", lead=0.1)
        self.play(FadeIn(tg[2]), run_time=0.3)
        hear(self, "eight", lead=0.55)
        self.play(GrowFromEdge(bars[3], LEFT), run_time=0.8)
        self.play(FadeIn(tg[3]), run_time=0.25)
        hear(self, "Sharing", lead=0.1)
        self.play(GrowFromEdge(bars[0], LEFT), run_time=0.4)
        hear(self, "Multi", lead=0.1)
        self.play(GrowFromEdge(multi, LEFT), run_time=1.2)
        hear(self, "approved", lead=0.2)
        self.play(FadeIn(acc), run_time=0.4)
        done(self)


class B15_MemAndType(Scene):
    """Mem is CPU memory (the RAM block grows, the VRAM tank does not); a bare gpu:1 may land on any card, a named type picks one."""
    def construct(self):
        title = act_title("I · Do You Have The GPU?")
        ram = Rectangle(width=1.5, height=1.0, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-4.9, 0.9, 0])
        ram_t = lab_c("RAM", -4.9, 0.2, 34)
        mem = chip("--mem=32G", -4.9, 2.2, mono=True, size=32)
        card = gpu_card(-2.2, 0.9, w=1.8, h=1.1)
        tk = tank(-2.2, -2.5, -0.55, 1.5)
        fillv = Rectangle(width=1.5, height=0.8, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([-2.2, -2.5 + 0.4 + 0.045, 0])
        vl = lab_c("VRAM", -2.2, -2.95, 34)
        link = Line([-2.2, 0.32, 0], [-2.2, -0.55, 0], color=INK, stroke_width=5)
        oom = chip("out of memory", -4.8, -1.8, size=32)
        # right half
        q1 = chip("gpu:1", 3.2, 2.35, mono=True, size=34)
        cards = [gpu_card(1.4 + 1.85 * i, 0.9, w=1.6, h=1.0) for i in range(3)]
        names = [lab_c(n, 1.4 + 1.85 * i, 0.05, 32) for i, n in enumerate(["V100", "A100", "T4"])]
        arrs = [Arrow([3.2, 1.9, 0], [1.4 + 1.85 * i, 1.5, 0], color=BAR1, stroke_width=6, buff=0.05, max_tip_length_to_length_ratio=0.3) for i in range(3)]
        q2 = chip("gpu:v100-sxm2:1", 3.2, 2.35, mono=True, size=32)
        arr_one = Arrow([2.4, 1.9, 0], [1.4, 1.5, 0], color=INK, stroke_width=8, buff=0.05, max_tip_length_to_length_ratio=0.3)
        ck = check(1.4, -0.85, s=0.28, color=TERRA, w=12)
        pick = lab_l("one card", 2.0, -0.85, 34)

        slots15 = [dashed_slot(3.2, 2.35, 3.6, 0.8)] + [dashed_slot(1.4 + 1.85 * i, 0.9, 1.6, 1.0) for i in range(3)]
        self.play(FadeIn(title), *[FadeIn(s_) for s_ in slots15], run_time=0.4)
        hear(self, "Mem", lead=0.2)
        self.play(FadeIn(ram), FadeIn(ram_t), FadeIn(mem), run_time=0.5)
        hear(self, "The card's own", lead=0.1)
        self.play(FadeIn(card), FadeIn(tk), FadeIn(fillv), FadeIn(vl), Create(link), run_time=0.6)
        hear(self, "raising", lead=0.2)
        self.play(ram.animate.scale(1.45).move_to([-4.9, 1.15, 0]), run_time=0.6)
        hear(self, "out of memory", lead=0.2)
        self.play(FadeIn(oom), run_time=0.3)
        hear(self, "bare", lead=0.2)
        self.remove(*slots15)
        self.play(FadeIn(q1), *[FadeIn(c) for c in cards], *[FadeIn(n) for n in names], run_time=0.5)
        self.play(*[Create(a) for a in arrs], run_time=0.5)
        hear(self, "Name", lead=0.15)
        self.play(FadeOut(q1), *[FadeOut(a) for a in arrs], FadeIn(q2), cards[1].animate.set_opacity(0.3), cards[2].animate.set_opacity(0.3),
                  names[1].animate.set_opacity(0.3), names[2].animate.set_opacity(0.3), run_time=0.5)
        self.play(Create(arr_one), Create(ck), FadeIn(pick), run_time=0.5)
        done(self)


class B19_VisibleDevices(Scene):
    """Three states of CUDA_VISIBLE_DEVICES (0, 0,1, unset) then the verdict: the variable is no proof, the tensor round trip is."""
    def construct(self):
        title = act_title("I · Do You Have The GPU?")
        tag = M("CUDA_VISIBLE_DEVICES", 36).move_to([2.0, 2.4, 0])
        p1 = [gpu_card(-4.3, 0.9, w=1.5, h=0.9, lit=True)]
        p2 = [gpu_card(-0.55, 0.9, w=1.5, h=0.9, lit=True), gpu_card(1.15, 0.9, w=1.5, h=0.9, lit=True)]
        term = RoundedRectangle(width=1.5, height=0.9, corner_radius=0.1, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([4.2, 0.9, 0])
        prompt = M(">_", 34, color="#FFFFFF").move_to([4.2, 0.9, 0])
        l1 = M("0", 48).move_to([-4.3, -0.35, 0])
        l2 = M("0,1", 48).move_to([0.3, -0.35, 0])
        l3 = T("unset", 44).move_to([4.2, -0.35, 0])
        n3 = T("interactive: normal", 34).move_to([4.2, -1.05, 0])
        # verdict row
        cross = x_mark(-4.6, -2.3, r=0.3, w=9)
        proof = T("not proof", 40).move_to([-3.1, -2.3, 0])
        cpu = cpu_chip(0.6, -2.3, w=1.3, h=0.8)
        gpu = gpu_card(3.4, -2.3, w=1.5, h=0.9)
        a1 = Arrow([1.55, -2.1, 0], [2.55, -2.1, 0], color=INK, stroke_width=7, buff=0.0, max_tip_length_to_length_ratio=0.35)
        a2 = Arrow([2.55, -2.55, 0], [1.55, -2.55, 0], color=INK, stroke_width=7, buff=0.0, max_tip_length_to_length_ratio=0.35)
        ck = check(5.1, -2.3, s=0.28, color=TERRA, w=12)
        rt = lab_c("round trip", 2.1, -3.1, 34)

        slots19 = [dashed_slot(4.2, 0.9, 1.5, 0.9), dashed_slot(-2.6, -2.3, 4.4, 0.9), dashed_slot(2.6, -2.3, 4.6, 1.1)]
        self.play(FadeIn(title), FadeIn(tag), *[FadeIn(s_) for s_ in slots19], run_time=0.5)
        hear(self, "Zero is one", lead=0.2)
        self.play(FadeIn(p1[0]), FadeIn(l1), run_time=0.4)
        hear(self, "zero comma", lead=0.2)
        self.play(*[FadeIn(g) for g in p2], FadeIn(l2), run_time=0.4)
        hear(self, "unset", lead=0.3)
        self.remove(slots19[0])
        self.play(FadeIn(term), FadeIn(prompt), FadeIn(l3), FadeIn(n3), run_time=0.5)
        hear(self, "never proof", lead=0.2)
        self.remove(slots19[1])
        self.play(FadeIn(proof), Create(cross), run_time=0.4)
        hear(self, "round trip", lead=0.2)
        self.remove(slots19[2])
        self.play(FadeIn(cpu), FadeIn(gpu), FadeIn(rt), run_time=0.3)
        self.play(Create(a1), Create(a2), run_time=0.4)
        self.play(Create(ck), gpu.light.animate.set_color(TERRA), run_time=0.3)
        done(self)


class B20_TwoNumbers(Scene):
    """Two dials: GPU-Util at 87 (share of the last second, a mark at 50) and Memory at 22 (a tank about a fifth full)."""
    def construct(self):
        title = act_title("II · Seeing The GPU Live")
        smi = logo_chip("nvidia", 0.0, 2.6, h=1.0)
        gl = gauge(-3.6, 0.3, r=1.7, v=0.87)
        gr = gauge(3.6, 0.3, r=1.7, v=0.22)
        glb = T("GPU-Util", 40).move_to([-3.6, 2.45, 0])
        grb = T("Memory", 40).move_to([3.6, 2.45, 0])
        ex1 = T("example", 32, color=INK).move_to([-2.0, -0.7, 0])
        ex2 = T("example", 32, color=INK).move_to([5.2, -0.7, 0])
        gl_empty = gauge(-3.6, 0.3, r=1.7, v=0.0)
        gr_empty = gauge(3.6, 0.3, r=1.7, v=0.0)
        n87 = T("87", 64, bold=True).move_to([-3.6, -0.7, 0])
        n22 = T("22", 64, bold=True).move_to([3.6, -0.7, 0])
        cells = VGroup(*[Rectangle(width=0.34, height=0.5, fill_color=INK if i < 9 else PAGE_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=3)
                         for i in range(10)]).arrange(RIGHT, buff=0.06).move_to([-3.6, -1.7, 0])
        sec = T("last second", 34).move_to([-3.6, -2.5, 0])
        tk = tank(3.6, -2.6, -1.2, 1.4)
        tf = Rectangle(width=1.4, height=0.3, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([3.6, -2.6 + 0.15 + 0.045, 0])
        mk = Dot(gl.pt(0.5, 1.7), radius=0.14, color=TERRA)
        below = T("below 50: wrong", 34).move_to([-3.6 + 0.0, -3.05, 0])

        self.play(FadeIn(title), run_time=0.4)
        hear(self, "NVIDIA", lead=0.1)
        self.play(FadeIn(smi), run_time=0.4)
        hear(self, "two", lead=0.1)
        self.play(FadeIn(gl_empty), FadeIn(gr_empty), FadeIn(glb), FadeIn(grb), run_time=0.5)
        hear(self, "share of the last", lead=0.1)
        self.play(FadeIn(cells), FadeIn(sec), run_time=0.4)
        hear(self, "87", lead=0.25)
        self.play(Transform(gl_empty, gl), FadeIn(n87), FadeIn(ex1), run_time=0.6)
        hear(self, "below", lead=0.1)
        self.play(FadeIn(mk), run_time=0.25)
        hear(self, "wrong", lead=0.2)
        self.play(FadeIn(below), run_time=0.3)
        hear(self, "memory", lead=0.1)
        self.play(Transform(gr_empty, gr), FadeIn(n22), FadeIn(ex2), run_time=0.6)
        hear(self, "fifth", lead=0.15)
        self.play(FadeIn(tk), FadeIn(tf), run_time=0.4)
        done(self)


class B22_TwoAxes(Scene):
    """A 2x2 of utilization against memory; each cell names its reading; the quiz dot (15 / 75) lands top-left."""
    def construct(self):
        title = act_title("II · Seeing The GPU Live")
        gx, gy, cw, ch = -2.5, -2.0, 3.4, 1.9
        cells = {}
        for (i, j) in [(0, 1), (0, 0), (1, 0), (1, 1)]:
            r = Rectangle(width=cw, height=ch, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR2, stroke_width=5)
            r.move_to([gx + cw * (i + 0.5), gy + ch * (j + 0.5), 0])
            cells[(i, j)] = r
        frame = VGroup(*cells.values())
        tags = {(0, 1): "loaded, not fed", (0, 0): "empty card", (1, 0): "raise the batch", (1, 1): "good"}
        tg = {k: T(v, 36).move_to([gx + cw * (k[0] + 0.5), gy + ch * (k[1] + 1) - 0.4, 0]) for k, v in tags.items()}
        xl = T("utilization", 38).move_to([gx + cw, gy - 0.95, 0])
        xlo, xhi = T("low", 32).move_to([gx + cw * 0.5, gy - 0.4, 0]), T("high", 32).move_to([gx + cw * 1.5, gy - 0.4, 0])
        yl = T("memory", 38).move_to([-4.55, gy + 2 * ch + 0.28, 0])
        yhi, ylo = T("high", 32).move_to([-3.2, gy + ch * 1.5, 0]), T("low", 32).move_to([-3.2, gy + ch * 0.5, 0])
        dot = Dot([gx + 0.15 * 2 * cw, gy + 0.75 * 2 * ch, 0], radius=0.17, color=TERRA)
        dlab = M("15% 75%", 30).move_to([gx + 0.15 * 2 * cw + 0.3 + 0.95, gy + 0.75 * 2 * ch, 0])
        ds = T("data starvation", 38).move_to([gx + cw * 0.5, gy + ch * 1 + 0.45, 0])

        self.play(FadeIn(title), FadeIn(frame), FadeIn(xl), FadeIn(xlo), FadeIn(xhi), FadeIn(yl), FadeIn(yhi), FadeIn(ylo), run_time=0.8)
        hear(self, "high memory", lead=0.2)
        self.play(FadeIn(tg[(0, 1)]), run_time=0.35)
        hear(self, "low and low", lead=0.15)
        self.play(FadeIn(tg[(0, 0)]), run_time=0.35)
        hear(self, "high utilization", lead=0.15)
        self.play(FadeIn(tg[(1, 0)]), run_time=0.35)
        hear(self, "high and high", lead=0.15)
        self.play(FadeIn(tg[(1, 1)]), run_time=0.35)
        hear(self, "fifteen", lead=0.2)
        dot.shift(UP * 1.2)
        self.play(FadeIn(dot), run_time=0.15)
        self.play(dot.animate.shift(DOWN * 1.2), FadeIn(dlab), run_time=0.45, rate_func=ease_in)
        hear(self, "data", lead=0.1)
        self.play(FadeIn(ds), run_time=0.35)
        done(self)


class B23_Bands(Scene):
    """Two scales grow left to right: utilization bands (problem, suspect, amber, acceptable, target) and memory bands."""
    def construct(self):
        title = act_title("II · Seeing The GPU Live")
        x0, sc = -5.2, 0.1
        def seg(a, b, y, fill, h=0.5):
            return Rectangle(width=(b - a) * sc - 0.06, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x0 + (a + b) / 2 * sc, y, 0])
        yu, ym = 1.45, -1.25
        ut = lab_l("utilization", -2.6, 2.45, 38)
        nums = VGroup(*[T(str(v), 32).move_to([x0 + v * sc, yu + 0.62, 0]) for v in (0, 50, 60, 70, 80, 100)])
        s1 = [seg(0, 50, yu, BAR1), seg(50, 60, yu, BAR2), seg(60, 70, yu, BAR3), seg(70, 80, yu, GHOST), seg(80, 100, yu, INK)]
        l1 = [lab_c("problem", x0 + 25 * sc, yu - 0.55, 34), lab_c("suspect", x0 + 55 * sc, yu - 1.1, 32), lab_c("amber", x0 + 65 * sc, yu - 0.55, 34),
              lab_c("acceptable", x0 + 75 * sc, yu - 1.1, 32), lab_c("target", x0 + 90 * sc, yu - 0.55, 36)]
        tick = Dot([x0 + 80 * sc, yu + 0.38, 0], radius=0.1, color=TERRA)
        mt = lab_l("memory", -2.6, -0.1, 38)
        mn = VGroup(*[T(str(v), 32).move_to([x0 + v * sc, ym + 0.62, 0]) for v in (0, 40, 60, 90, 100)])
        m_room = seg(0, 40, ym, BAR2)
        m_health = seg(60, 90, ym, BAR1)
        m_empty = [dashed_slot(x0 + 50 * sc, ym, 2.0 - 0.06, 0.5), dashed_slot(x0 + 95 * sc, ym, 1.0 - 0.06, 0.5)]
        lm = [lab_c("room for a bigger batch", x0 + 20 * sc, ym - 0.65, 32), lab_c("healthy", x0 + 75 * sc, ym - 0.65, 36)]

        slots23 = [dashed_slot(x0 + 75 * sc, yu, 1.0 - 0.06, 0.5), dashed_slot(x0 + 90 * sc, yu, 2.0 - 0.06, 0.5), dashed_slot(x0 + 20 * sc, ym, 4.0 - 0.06, 0.5), dashed_slot(x0 + 75 * sc, ym, 3.0 - 0.06, 0.5)]
        self.play(FadeIn(title), FadeIn(ut), FadeIn(nums), FadeIn(mt), FadeIn(mn), *[FadeIn(s_) for s_ in slots23], run_time=0.6)
        hear(self, "under 50", lead=0.2)
        self.play(GrowFromEdge(s1[0], LEFT), FadeIn(l1[0]), run_time=0.7)
        hear(self, "Under 60", lead=0.2)
        self.play(GrowFromEdge(s1[1], LEFT), FadeIn(l1[1]), run_time=0.5)
        hear(self, "60 to 70", lead=0.2)
        self.play(GrowFromEdge(s1[2], LEFT), FadeIn(l1[2]), run_time=0.5)
        hear(self, "70 acceptable", lead=0.1)
        self.remove(slots23[0])
        self.play(GrowFromEdge(s1[3], LEFT), FadeIn(l1[3]), run_time=0.5)
        hear(self, "80 to 100", lead=0.2)
        self.remove(slots23[1])
        self.play(GrowFromEdge(s1[4], LEFT), FadeIn(l1[4]), FadeIn(tick), run_time=0.6)
        hear(self, "memory", lead=0.1)
        self.play(*[FadeIn(d) for d in m_empty], run_time=0.5)
        hear(self, "60 to 90", lead=0.2)
        self.remove(slots23[3])
        self.play(GrowFromEdge(m_health, LEFT), FadeIn(lm[1]), run_time=0.6)
        hear(self, "Under 40", lead=0.15)
        self.remove(slots23[2])
        self.play(GrowFromEdge(m_room, LEFT), FadeIn(lm[0]), run_time=0.7)
        done(self)


class B24_IdleBot(Scene):
    """A utilization line sinks to a flat low stretch; Idle Bot sweeps it; an email at 15 min; the job is cancelled at 1 h."""
    def construct(self):
        title = act_title("II · Seeing The GPU Live")
        ax = Line([-5.6, -2.2, 0], [4.9, -2.2, 0], color=INK, stroke_width=6)
        ay = Line([-5.6, -2.2, 0], [-5.6, 1.5, 0], color=BAR2, stroke_width=6)
        tl = T("time", 34).move_to([5.45, -2.2, 0])
        ul = T("GPU use", 34).move_to([-4.7, 1.8, 0])
        pts = [[-5.6, 0.6, 0], [-5.3, 0.9, 0], [-5.0, 0.4, 0], [-4.7, 1.0, 0], [-4.4, 0.5, 0], [-4.1, 0.95, 0], [-3.8, 0.45, 0], [-3.5, 0.8, 0],
               [-3.2, -0.3, 0], [-3.0, -1.7, 0], [4.8, -1.7, 0]]
        line = VMobject(stroke_color=INK, stroke_width=8)
        line.set_points_as_corners(pts)
        t15 = Line([-1.9, -2.2, 0], [-1.9, -2.45, 0], color=INK, stroke_width=6)
        t60 = Line([1.4, -2.2, 0], [1.4, -2.45, 0], color=INK, stroke_width=6)
        l15 = T("15 min", 34).move_to([-1.9, -2.85, 0])
        l60 = T("1 h", 34).move_to([1.4, -2.85, 0])
        bot = VGroup(Circle(radius=0.32, stroke_color=INK, stroke_width=7, fill_color=PAGE_TOP, fill_opacity=1),
                     Line([0.23, -0.23, 0], [0.62, -0.62, 0], color=INK, stroke_width=9)).move_to([-3.0, -0.4, 0])
        botl = T("Idle Bot", 36).move_to([-1.2, 0.5, 0])
        env = VGroup(Rectangle(width=1.0, height=0.68, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5),
                     Line([-0.5, 0.34, 0], [0, -0.05, 0], color=INK, stroke_width=4), Line([0.5, 0.34, 0], [0, -0.05, 0], color=INK, stroke_width=4)).move_to([-1.9, -1.1, 0])
        job = job2(1.4, -1.1, 0.9)
        xm = x_mark(1.4, -1.1, r=0.4, w=10)
        npp = T("no published percentage", 36).move_to([3.1, 2.4, 0])
        card = gpu_card(-2.0, 2.4, w=1.5, h=0.9)
        held = T("holds the card", 34).move_to([-2.0, 1.65, 0])

        self.play(FadeIn(title), Create(ax), Create(ay), FadeIn(tl), FadeIn(ul), run_time=0.6)
        hear(self, "idle cards", lead=0.9)
        self.play(Create(line), run_time=1.4, rate_func=linear)
        hear(self, "idlebot", lead=0.2)
        self.play(FadeIn(bot), FadeIn(botl), Create(t15), Create(t60), FadeIn(l15), FadeIn(l60), run_time=0.5)
        self.play(bot.animate.shift(RIGHT * 4.4), botl.animate.shift(RIGHT * 4.4), run_time=1.6, rate_func=linear)
        hear(self, "15", lead=0.35)
        self.play(FadeIn(env), run_time=0.35)
        hear(self, "hour", lead=0.35)
        self.play(FadeIn(job), run_time=0.2)
        self.play(Create(xm), run_time=0.3)
        hear(self, "no published", lead=0.15)
        self.play(FadeIn(npp), run_time=0.4)
        hear(self, "stalled", lead=0.1)
        self.play(FadeIn(card), FadeIn(held), run_time=0.4)
        done(self)


def hatch(xa, xb, ya, yb, gap=0.2, color=BAR1, sw=3.5):
    """Diagonal hatch lines clipped to the rectangle [xa, xb] x [ya, yb]."""
    w, h = xb - xa, yb - ya
    lines = VGroup()
    c = -h
    while c < w:
        xs, xe = xa + max(0.0, c), xa + min(w, c + h)
        if xe - xs > 0.02:
            lines.add(Line([xs, ya + (xs - xa - c), 0], [xe, ya + (xe - xa - c), 0], color=color, stroke_width=sw))
        c += gap
    return lines
