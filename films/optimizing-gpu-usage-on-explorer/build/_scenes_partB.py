# ═════════════════════════════ PART B — Acts III and IV (manim beats) ═════════════════════════════


class B30_FourLayers(Scene):
    """A four-rung ladder, lightest first: live tools, framework profiler, timeline, one kernel; the first two are ringed as 'most problems'."""
    def construct(self):
        title = act_title("III · The Profiling Toolchain")
        rows = []
        spec = [("live", "nvidia", ["nvidia-smi", "nvitop"], -2.2), ("framework", "pytorch", ["torch.profiler"], -0.8),
                ("timeline", "nvidia", ["nsys"], 0.6), ("one kernel", "nvidia", ["ncu"], 2.0)]
        for name, logo, monos, y in spec:
            lab = lab_l(name, -5.9, y, 38)
            lg = logo_chip(logo, -1.9, y, h=0.9)
            ms = Group(*[chip(m, 1.4 + 3.0 * i if len(monos) > 1 else 1.6, y, mono=True, size=32) for i, m in enumerate(monos)])
            rows.append(Group(lab, lg, ms))
        rail = Line([-6.1, -2.7, 0], [-6.1, 2.5, 0], color=BAR2, stroke_width=6)
        rare = T("rarely", 38).move_to([5.4, 1.3, 0])
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "lightest", lead=0.3)
        self.play(Create(rail), run_time=0.4)
        hear(self, "live tools", lead=0.2)
        self.play(FadeIn(rows[0]), run_time=0.5)
        hear(self, "framework", lead=0.2)
        self.play(FadeIn(rows[1]), run_time=0.5)
        hear(self, "insight systems", lead=0.3)
        self.play(FadeIn(rows[2]), run_time=0.5)
        hear(self, "one kernel", lead=0.5)
        self.play(FadeIn(rows[3]), run_time=0.5)
        self.play(rows[2].animate.set_opacity(0.45), rows[3].animate.set_opacity(0.45), FadeIn(rare), run_time=0.4)
        hear(self, "layer two", lead=0.4)
        r = ring_around(Group(rows[0], rows[1]), pad=0.2)
        self.play(Create(r), run_time=0.5)
        done(self)


class B33_ReadTheTable(Scene):
    """A profiler table drawn as CPU/CUDA bar pairs; the four things to read land in order (example, not our run)."""
    def construct(self):
        title = act_title("III · The Profiling Toolchain")
        x0 = -1.0
        names = ["DataLoader.__next__", "aten::conv2d", "aten::batch_norm", "aten::copy_"]
        cpu = [1.843, 0.041, 0.019, 0.017]
        cuda = [0.0, 0.394, 0.087, 0.052]
        ys = [0.95, 0.0, -0.95, -1.9]
        sc = 2.4
        rows, cb, gb = [], [], []
        for n, c, g, y in zip(names, cpu, cuda, ys):
            lab = M(n, 30)
            lab.move_to([x0 - 0.35 - lab.width / 2, y, 0])
            b1 = Rectangle(width=max(c * sc, 0.06), height=0.3, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x0 + max(c * sc, 0.06) / 2, y + 0.19, 0])
            b2 = Rectangle(width=max(g * sc, 0.06), height=0.3, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x0 + max(g * sc, 0.06) / 2, y - 0.19, 0])
            rows.append(lab); cb.append(b1); gb.append(b2)
        table = Group(*rows, *cb, *gb)
        leg1 = Rectangle(width=0.5, height=0.3, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([2.2, 2.55, 0])
        lg1 = lab_l("CPU total", 2.55, 2.55, 32)
        leg2 = Rectangle(width=0.5, height=0.3, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([2.2, 2.05, 0])
        lg2 = lab_l("CUDA total", 2.55, 2.05, 32)
        n1 = M("1.843 s", 32).move_to([x0 + 1.843 * sc + 0.2 + 0.85, ys[0] + 0.19, 0])
        n2 = M("0.000 s", 32).move_to([x0 + 0.06 + 0.2 + 0.85, ys[0] - 0.19, 0])
        # strip showing gaps
        bursts = VGroup(*[Rectangle(width=0.35, height=0.32, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([-5.7 + 1.1 * i, 2.35, 0]) for i in range(4)])
        sl_ = lab_l("GPU", -6.2, 1.8, 32)
        ex = T("example, not our run", 34).move_to([3.6, -2.9, 0])

        self.play(FadeIn(title), FadeIn(table), FadeIn(leg1), FadeIn(lg1), FadeIn(leg2), FadeIn(lg2), FadeIn(n1), FadeIn(n2), run_time=0.8)
        hear(self, "gaps", lead=0.2)
        self.play(FadeIn(bursts), FadeIn(sl_), run_time=0.5)
        hear(self, "Large copy", lead=0.15)
        rc = ring_around(Group(rows[3], cb[3], gb[3]), pad=0.12)
        self.play(Create(rc), run_time=0.4)
        self.wait(0.9)
        self.play(FadeOut(rc), run_time=0.3)
        hear(self, "CPU time far", lead=0.1)
        self.play(cb[0].animate.set_fill(INK, opacity=0.35), run_time=0.35)
        self.play(cb[0].animate.set_fill(BAR2, opacity=1), run_time=0.3)
        hear(self, "data loader at", lead=0.2)
        rl_ = ring_around(Group(rows[0], cb[0], gb[0], n1), pad=0.12)
        self.play(Create(rl_), run_time=0.4)
        hear(self, "This example", lead=0.2)
        self.play(FadeIn(ex), run_time=0.4)
        done(self)


class B35_TimelinePatterns(Scene):
    """A timeline: GPU bursts with long gaps, file reads filling the gaps, then scattered copies that pinned memory pulls together."""
    def construct(self):
        title = act_title("III · The Profiling Toolchain")
        gl = lab_l("GPU", -6.2, 1.6, 36)
        cl = lab_l("CPU", -6.2, 0.35, 36)
        ml = lab_l("copies", -6.2, -1.0, 36)
        xs = [-3.9, -1.4, 1.1, 3.6]
        bursts = [Rectangle(width=0.5, height=0.5, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x, 1.6, 0]) for x in xs]
        base = Line([-4.4, 1.15, 0], [4.4, 1.15, 0], color=BAR2, stroke_width=5)
        reads = [chip("read()", x + 1.25, 0.35, w=1.95, mono=True, size=30) for x in xs[:3]]
        t15 = T("15 ms", 32).move_to([xs[0], 2.35, 0])
        t50 = T("50 ms", 32).move_to([xs[0] + 1.25, 2.35, 0])
        ex = T("example", 32).move_to([5.3, 1.6, 0])
        tick_x = [-4.6, -3.2, -2.0, -0.6, 0.7, 2.3, 3.8]
        ticks = [Rectangle(width=0.16, height=0.5, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=2).move_to([x, -1.0, 0]) for x in tick_x]
        pin = chip("pinned memory", 0.0, -2.35, size=34)
        near = [xs[0], xs[0] + 0.3, xs[1], xs[1] + 0.3, xs[2], xs[2] + 0.3, xs[3]]

        slots35 = [dashed_slot(x + 1.25, 0.35, 1.95, 0.8) for x in xs[:3]] + [dashed_slot(0.0, -1.0, 9.0, 0.7)]
        self.play(FadeIn(title), FadeIn(cl), FadeIn(ml), *[FadeIn(s_) for s_ in slots35], run_time=0.4)
        hear(self, "empty GPU", lead=0.2)
        self.play(FadeIn(gl), Create(base), run_time=0.4)
        hear(self, "short bursts", lead=0.2)
        self.play(LaggedStart(*[FadeIn(b) for b in bursts], lag_ratio=0.25), run_time=0.9)
        self.play(FadeIn(t15), FadeIn(t50), FadeIn(ex), run_time=0.3)
        hear(self, "File reads", lead=0.1)
        self.remove(*slots35[:3])
        self.play(*[FadeIn(r) for r in reads], run_time=0.6)
        hear(self, "Copies", lead=0.1)
        self.remove(slots35[3])
        self.play(LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.1), run_time=0.9)
        hear(self, "Pin the memory", lead=0.1)
        self.play(FadeIn(pin), *[t.animate.move_to([nx, -1.0, 0]) for t, nx in zip(ticks, near)], run_time=0.9)
        done(self)


class B40_Deliveries(Scene):
    """A truck crawls to a fast GPU; under it two time bars: GPU computes 25 ms, then waits 35 ms of a 60 ms loader."""
    def construct(self):
        title = act_title("IV · Data Starvation")
        belt = Rectangle(width=8.6, height=0.22, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([-1.3, 1.45, 0])
        truck = job2(-5.2, 1.95, 0.9)
        gpu = gpu_card(4.3, 1.75, w=1.7, h=1.0)
        idle = T("58% idle", 54, bold=True).move_to([4.3, 2.9, 0])
        x0 = -2.8
        lab_g = lab_l("GPU", x0 - 1.7, -1.7, 38)
        lab_l_ = lab_l("loader", x0 - 1.7, -0.6, 38)
        loader = Rectangle(width=6.0, height=0.55, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x0 + 3.0, -0.6, 0])
        work = Rectangle(width=2.5, height=0.55, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x0 + 1.25, -1.7, 0])
        wait = Rectangle(width=3.5, height=0.55, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x0 + 2.5 + 1.75, -1.7, 0])
        wait_h = hatch(x0 + 2.5, x0 + 6.0, -1.7 - 0.275 + 0.03, -1.7 + 0.275 - 0.03, gap=0.22)
        waitg = VGroup(wait, wait_h)
        k1 = T("25 ms", 36).move_to([x0 + 1.25, -2.35, 0])
        k2 = T("35 ms idle", 36).move_to([x0 + 4.25, -2.35, 0])
        k3 = T("60 ms", 36).move_to([x0 + 6.0 + 0.9, -0.6, 0])
        ex = T("example", 32).move_to([5.3, -1.7, 0])

        self.play(FadeIn(title), FadeIn(belt), FadeIn(gpu), run_time=0.5)
        hear(self, "fast cook", lead=0.3)
        self.play(FadeIn(truck), run_time=0.2)
        self.play(truck.animate.move_to([2.6, 1.95, 0]), run_time=3.2, rate_func=linear)
        hear(self, "25", lead=0.3)
        self.play(FadeIn(lab_g), GrowFromEdge(work, LEFT), FadeIn(k1), FadeIn(ex), run_time=0.7)
        hear(self, "60", lead=0.6)
        self.play(FadeIn(lab_l_), GrowFromEdge(loader, LEFT), FadeIn(k3), run_time=0.8)
        hear(self, "idles", lead=0.1)
        self.play(GrowFromEdge(waitg, LEFT), FadeIn(k2), run_time=0.7)
        hear(self, "of every", lead=0.3)
        self.play(FadeIn(idle), run_time=0.4)
        done(self)


class B44_StartingValues(Scene):
    """Four setting names, each with its starting value, then cpus-per-task = workers + 1 (at least 4)."""
    def construct(self):
        title = act_title("IV · Data Starvation")
        spec = [("num_workers", "CPUs minus one"), ("pin_memory", "always on"), ("persistent_workers", "on if workers > 0"), ("prefetch_factor", "2")]
        ys = [2.0, 1.0, 0.0, -1.0]
        rows = []
        for (n, v), y in zip(spec, ys):
            a = chip(n, -3.3, y, w=4.9, mono=True, size=32)
            ar = Arrow([-0.6, y, 0], [0.5, y, 0], color=INK, stroke_width=7, buff=0, max_tip_length_to_length_ratio=0.4)
            b = chip(v, 3.1, y, w=4.2, size=36)
            rows.append(Group(a, ar, b))
        e1 = chip("--cpus-per-task", -3.7, -2.35, w=4.3, mono=True, size=30)
        eq = T("=", 50).move_to([-1.2, -2.35, 0])
        e2 = chip("num_workers", 1.0, -2.35, w=3.5, mono=True, size=30)
        pl = T("+", 50).move_to([2.95, -2.35, 0])
        e3 = chip("1", 3.9, -2.35, w=1.0, size=40)
        least = T("at least 4", 38).move_to([-3.7, -3.1, 0])
        dots = VGroup(*[Dot([4.7 + 0.0, -2.35, 0])])

        slots44 = [dashed_slot(-3.3, ys[2], 4.9, 0.8), dashed_slot(3.1, ys[2], 4.2, 0.8), dashed_slot(-3.3, ys[3], 4.9, 0.8), dashed_slot(3.1, ys[3], 4.2, 0.8), dashed_slot(-0.5, -2.35, 10.0, 0.9)]
        self.play(FadeIn(title), *[FadeIn(s_) for s_ in slots44], run_time=0.4)
        hear(self, "workers", lead=0.2)
        self.play(FadeIn(rows[0]), run_time=0.45)
        hear(self, "Pin memory", lead=0.1)
        self.play(FadeIn(rows[1]), run_time=0.45)
        hear(self, "Persistent", lead=0.1)
        self.remove(slots44[0], slots44[1])
        self.play(FadeIn(rows[2]), run_time=0.45)
        hear(self, "Prefetch", lead=0.1)
        self.remove(slots44[2], slots44[3])
        self.play(FadeIn(rows[3]), run_time=0.45)
        hear(self, "equal", lead=0.9)
        self.remove(slots44[4])
        self.play(FadeIn(e1), FadeIn(eq), run_time=0.4)
        hear(self, "workers plus", lead=0.2)
        self.play(FadeIn(e2), FadeIn(pl), FadeIn(e3), run_time=0.5)
        hear(self, "at least", lead=0.1)
        self.play(FadeIn(least), run_time=0.4)
        done(self)


class B47_WhereDataLives(Scene):
    """Home, scratch and projects are all network filesystems; data goes in scratch or projects as a few large files, never home."""
    def construct(self):
        title = act_title("IV · Data Starvation")
        xs = [-2.4, 1.3, 4.8]
        names = ["/home", "/scratch", "/projects"]
        boxes = [Rectangle(width=2.2, height=1.3, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, 1.2, 0]) for x in xs]
        labs = [M(n, 36).move_to([x, 2.3, 0]) for n, x in zip(names, xs)]
        br = Line([-3.5, -0.55, 0], [6.1, -0.55, 0], color=INK, stroke_width=6)
        brl = T("network filesystems", 38).move_to([1.3, -0.95, 0])
        ck1 = check(1.2, 1.2, s=0.26, color=TERRA, w=11)
        ck2 = check(4.7, 1.2, s=0.26, color=TERRA, w=11)
        cr = x_mark(-2.4, 1.2, r=0.28, w=9)
        big = VGroup(*[Rectangle(width=1.5, height=0.42, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.2, -1.5 - 0.5 * i, 0]) for i in range(3)])
        bigl = T("a few large files", 36).move_to([3.2, -3.15, 0])
        bck = check(5.3, -2.15, s=0.26, color=TERRA, w=11)
        rng = np.random.RandomState(4)
        smalls = VGroup(*[Square(side_length=0.1, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-3.2 + rng.uniform(-1.4, 1.4), -2.2 + rng.uniform(-0.7, 0.7), 0]) for _ in range(70)])
        smalll = T("millions of small ones", 36).move_to([-3.2, -3.15, 0])
        scr = x_mark(-3.2, -1.85, r=0.0001, w=1)
        pg = chip("purged", 1.3, 0.05, size=32)

        self.play(FadeIn(title), run_time=0.4)
        hear(self, "Home", lead=0.1)
        self.play(FadeIn(boxes[0]), FadeIn(labs[0]), run_time=0.35)
        hear(self, "Scratch", lead=0.1)
        self.play(FadeIn(boxes[1]), FadeIn(labs[1]), run_time=0.35)
        hear(self, "Projects", lead=0.1)
        self.play(FadeIn(boxes[2]), FadeIn(labs[2]), run_time=0.35)
        hear(self, "network", lead=0.2)
        self.play(Create(br), FadeIn(brl), run_time=0.5)
        hear(self, "Keep data", lead=0.1)
        self.play(Create(ck1), Create(ck2), run_time=0.35)
        hear(self, "packed", lead=0.55)
        self.play(LaggedStart(*[FadeIn(b) for b in big], lag_ratio=0.2), FadeIn(bigl), run_time=0.6)
        self.play(Create(bck), run_time=0.25)
        hear(self, "millions", lead=0.2)
        self.play(FadeIn(smalls), FadeIn(smalll), run_time=0.5)
        hear(self, "never in Home", lead=0.15)
        self.play(Create(cr), run_time=0.3)
        hear(self, "purged", lead=0.2)
        self.play(FadeIn(pg), run_time=0.3)
        done(self)


class B48_Illustration(Scene):
    """Three bars (18, 55, 82 percent) with images per second, labelled as the source's illustration, not our run."""
    def construct(self):
        title = act_title("IV · Data Starvation")
        xs = [-4.2, 0.0, 4.2]
        vals = [18, 55, 82]
        base = -1.45
        sc = 0.034
        bars = [Rectangle(width=1.5, height=v * sc, fill_color=BAR2 if i < 2 else INK, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, base + v * sc / 2, 0])
                for i, (x, v) in enumerate(zip(xs, vals))]
        nums = [T(f"{v}%", 52, bold=True).move_to([x, base + v * sc + 0.5, 0]) for x, v in zip(xs, vals)]
        axis = Line([-6.0, base, 0], [6.0, base, 0], color=INK, stroke_width=6)
        cfg = [T(t, 34).move_to([x, base - 0.5, 0]) for x, t in zip(xs, ["no workers", "8 workers, pinned", "plus pre-fetch"])]
        ips = [M(t, 32).move_to([x, base - 1.15, 0]) for x, t in zip(xs, ["~420 img/s", "~1,300 img/s", "~1,950 img/s"])]
        tag = T("illustration from the source, not our run", 34).move_to([1.6, 3.0, 0])
        st = stamp("no script produces these", -3.2, 1.3, w=4.6, size=32)

        self.play(FadeIn(title), Create(axis), FadeIn(tag), run_time=0.6)
        hear(self, "no workers", lead=0.2)
        self.play(FadeIn(cfg[0]), GrowFromEdge(bars[0], DOWN), run_time=0.7)
        self.play(FadeIn(nums[0]), FadeIn(ips[0]), run_time=0.3)
        hear(self, "8 workers", lead=0.2)
        self.play(FadeIn(cfg[1]), GrowFromEdge(bars[1], DOWN), run_time=0.8)
        self.play(FadeIn(nums[1]), FadeIn(ips[1]), run_time=0.3)
        hear(self, "prefetching", lead=0.3)
        self.play(FadeIn(cfg[2]), GrowFromEdge(bars[2], DOWN), run_time=0.8)
        self.play(FadeIn(nums[2]), FadeIn(ips[2]), run_time=0.3)
        hear(self, "no script", lead=0.2)
        self.play(FadeIn(st), run_time=0.4)
        done(self)
