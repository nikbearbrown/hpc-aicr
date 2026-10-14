# ═════════════════════════════ PART A — B10 B11 B12 B21 ═════════════════════════════
def pA_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pA_stopwatch(x, y, r=0.6):
    face = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    knob = Rectangle(width=0.26, height=0.16, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + r + 0.12, 0])
    hand = Line([x, y, 0], [x, y + r * 0.7, 0], color=INK, stroke_width=7)
    hub = Dot([x, y, 0], radius=0.07, color=INK)
    g = VGroup(knob, face, hand, hub)
    g.hand, g.cx, g.cy = hand, x, y
    return g


class B10_FastAndLiteral(Scene):
    """A fast agent fires many job boxes; they all pile into one shared rack and crowd out everyone else's dots."""
    def construct(self):
        title = pA_act_title("I · Why An Agent Needs Rules")
        claude = logo_chip("claude", -4.9, 1.5)
        sw = pA_stopwatch(-2.6, 1.5)
        self.play(FadeIn(title), FadeIn(claude), run_time=0.4)
        # a stack of small job boxes waits at the left
        iso = Iso(-4.9, -3.0, 0.5)
        stack = VGroup(*[job_box(iso, (i % 3) * 0.9, (i // 3) * 0.9, 0, s=0.7) for i in range(6)])
        # "fast": the stopwatch ticks and the boxes start to fly out
        hear(self, "fast", lead=0.1)
        self.play(FadeIn(sw), FadeIn(stack), run_time=0.3)
        self.play(Rotate(sw.hand, angle=-2 * PI, about_point=[sw.cx, sw.cy, 0]), run_time=1.0, rate_func=linear)
        hear(self, "never tired", lead=0.2)
        self.play(Rotate(sw.hand, angle=-2 * PI, about_point=[sw.cx, sw.cy, 0]), run_time=0.8, rate_func=linear)
        # "shared cluster": racks appear, each with a different count of other people's dots
        hear(self, "On a shared cluster", lead=0.25)
        racks, dots, rows = [], [], []
        spots = [(1.9, -2.5, 1), (4.5, -2.5, 2), (1.9, -0.1, 3), (4.5, -0.1, 1)]
        for (cx, cy, n) in spots:
            ri = Iso(cx, cy, 0.8)
            st, lt = explorer_rack(ri)
            ds = VGroup(*[Dot([cx + 1.3, cy + 0.15 + 0.3 * k, 0], radius=0.11, color=TERRA) for k in range(n)])
            racks.append(VGroup(st, lt)); dots.append(ds)
        clab = T("shared cluster", 38).move_to([3.5, 2.5, 0])
        self.play(*[FadeIn(r) for r in racks], *[FadeIn(d) for d in dots], FadeIn(clab), run_time=0.7)
        # "exactly what you asked": a volley of boxes crosses to the target rack and lands
        hear(self, "exactly what you asked", lead=0.3)
        # re-use the stack: 3 boxes leave it, fly right
        leave = VGroup(*stack[:3])
        self.play(leave.animate.shift(RIGHT * 5.4 + UP * 0.6), run_time=0.8, rate_func=smooth)
        self.play(FadeOut(leave, scale=0.5), run_time=0.2)
        hear(self, "as many times", lead=0.3)
        rest = VGroup(*stack[3:])
        self.play(rest.animate.shift(RIGHT * 5.4 + UP * 0.6), run_time=0.8, rate_func=smooth)
        self.play(FadeOut(rest, scale=0.5), run_time=0.2)
        # "will not feel the cost": the target rack's dots crowd out the others, which dim
        hear(self, "not feel the cost", lead=0.3)
        crowd = VGroup(*[Dot([1.9 + 1.3 + 0.3 * (k % 2), -2.5 + 0.15 + 0.3 * (k // 2), 0], radius=0.11, color=TERRA) for k in range(1, 8)])
        self.play(FadeIn(crowd), *[r.animate.set_opacity(0.3) for r in racks[1:]], *[d.animate.set_opacity(0.3) for d in dots[1:]], run_time=0.8)
        done(self)


class B11_ThreeQuietFailures(Scene):
    """Three cards fan out; each shows one quiet failure; a 'no error' tag lands on all three."""
    def construct(self):
        xs = [-4.15, 0.0, 4.15]
        cards = [paper(0, 0.5, w=3.5, h=3.1) for _ in xs]
        for c, x in zip(cards, xs):
            c.shift(RIGHT * 0)
        # start stacked in the centre, then fan out
        self.play(FadeIn(cards[1]), run_time=0.3)
        self.add(cards[0], cards[2]); cards[0].move_to([0, 0.5, 0]); cards[2].move_to([0, 0.5, 0])
        self.bring_to_front(cards[1])
        self.play(cards[0].animate.move_to([xs[0], 0.5, 0]), cards[2].animate.move_to([xs[2], 0.5, 0]), run_time=0.7, rate_func=smooth)
        # card 1: wrong machine
        hear(self, "wrong machine", lead=0.5)
        iso1 = Iso(xs[0] - 0.3, -0.55, 0.62)
        r1, l1 = explorer_rack(iso1)
        door = Rectangle(width=0.55, height=0.9, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([xs[0] + 0.78, 0.15, 0])
        job1 = job_box(iso1, 0.35, 0.35, 0.88 + 0.08, s=0.6)
        lab1 = M("login node", 32).move_to([xs[0], -1.45, 0])
        self.play(FadeIn(r1), FadeIn(l1), FadeIn(door), FadeIn(lab1), run_time=0.4)
        self.play(FadeIn(job1, shift=DOWN * 0.4), run_time=0.3)
        # card 2: wrong size
        hear(self, "bigger than the job", lead=0.9)
        bar = Rectangle(width=2.7, height=0.55, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([xs[1], 0.5, 0])
        lab2 = M("8 h for 25 min", 32).move_to([xs[1], -1.45, 0])
        self.play(Create(bar), FadeIn(lab2), run_time=0.4)
        fill = Rectangle(width=0.45, height=0.55, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([xs[1] - 1.35 + 0.225, 0.5, 0])
        self.play(GrowFromEdge(fill, LEFT), run_time=0.4)
        # card 3: passing check, no CUDA
        hear(self, "a check that passes", lead=0.5)
        iso3 = Iso(xs[2] - 0.3, -0.55, 0.62)
        r3, l3 = explorer_rack(iso3)
        slot = iso3.quad([(0, 0, 0.46), (0, 1.3, 0.46), (0, 1.3, 0.84), (0, 0, 0.84)], GHOST, stroke=INK, sw=3)
        lab3 = M("exit 0, no CUDA", 32).move_to([xs[2], -1.45, 0])
        self.play(FadeIn(r3), FadeIn(l3), FadeIn(slot), FadeIn(lab3), run_time=0.4)
        ck = check(xs[2] + 1.0, 1.35, s=0.3, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.4)
        # "quiet failures": 'no error' lands on all three
        hear(self, "quiet failures", lead=0.2)
        tags = [chip("no error", x, -2.5, size=34) for x in xs]
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in tags], lag_ratio=0.4), run_time=1.0)
        hear(self, "nothing crashes", lead=0.2)
        self.play(*[Indicate(t, color=INK, scale_factor=1.08) for t in tags], run_time=0.6)
        done(self)


class B12_TwoFiles(Scene):
    """HPC.md lands first; AICR.md lands on it and builds on it; read the first, then the second."""
    def construct(self):
        lo = paper(-2.2, -1.0, w=2.8, h=3.2)
        up = paper(-1.3, 0.1, w=2.8, h=3.2)
        lo_l = scribbles_on(lo, n=4)
        up_l = scribbles_on(up, n=4)
        ghost = DashedVMobject(Rectangle(width=2.8, height=3.2, color=BAR1, stroke_width=5).move_to([-1.3, 0.1, 0]), num_dashes=28)
        self.play(FadeIn(lo), FadeIn(lo_l), run_time=0.3)
        hear(self, "two files", lead=0.3)
        self.play(Create(ghost), run_time=0.4)
        hear(self, "HPC", lead=0.3)
        hpc = M("HPC.md", 42).move_to([3.4, -1.0, 0])
        self.play(FadeIn(hpc), run_time=0.3)
        hear(self, "any shared cluster", lead=0.3)
        hsub = T("any shared cluster (Explorer)", 34).move_to([3.4, -1.7, 0])
        self.play(FadeIn(hsub), run_time=0.4)
        # AICR.md page lands on it (before the clip midpoint)
        hear(self, "AICR", lead=0.55)
        self.play(FadeOut(ghost), FadeIn(up, shift=DOWN * 0.8), FadeIn(up_l, shift=DOWN * 0.8), run_time=0.3)
        hear(self, "builds on", lead=0.0)
        aicr = M("AICR.md", 42).move_to([3.4, 2.0, 0])
        self.play(FadeIn(aicr), run_time=0.25)
        arr = Arrow([3.4, 0.7, 0], [3.4, -0.3, 0], color=INK, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.5)
        blab = T("builds on", 36).move_to([5.0, 0.2, 0])
        self.play(Create(arr), FadeIn(blab), run_time=0.4)
        hear(self, "stricter", lead=0.2)
        asub = T("stricter on AICR", 34).move_to([3.4, 1.35, 0])
        self.play(FadeIn(asub), run_time=0.4)
        hear(self, "Read the first", lead=0.2)
        first = chip("first", -5.2, -1.0, size=34)
        self.play(FadeIn(first, shift=RIGHT * 0.3), run_time=0.3)
        hear(self, "then the second", lead=0.2)
        then = chip("then", -5.2, 0.4, size=34)
        self.play(FadeIn(then, shift=RIGHT * 0.3), run_time=0.3)
        done(self)


class B21_PrimeDirective(Scene):
    """Agent column does the pipeline work; the researcher keeps spend, access and what cannot be undone."""
    def construct(self):
        rule = Line([-6.0, -2.3, 0], [6.0, -2.3, 0], color=INK, stroke_width=12)
        div = DashedLine([0, 3.0, 0], [0, -1.8, 0], color=BAR1, stroke_width=6, dash_length=0.25)
        self.play(Create(rule), Create(div), run_time=0.5)
        hear(self, "The agent does", lead=0.3)
        claude = logo_chip("claude", -4.7, 2.2)
        alab = T("agent", 44).move_to([-3.1, 2.2, 0])
        self.play(FadeIn(claude), FadeIn(alab), run_time=0.4)
        verbs = []
        for v, ph, y in (("inspect", "inspect", 0.9), ("measure", "measure", 0.1), ("size", "size", -0.7), ("record", "records", -1.5)):
            hear(self, ph, lead=0.2)
            tick = check(-5.5, y, s=0.2, w=8)
            lab = T(v, 46)
            lab.move_to([-4.8 + lab.width / 2, y, 0])
            self.play(Create(tick), FadeIn(lab), run_time=0.3)
            verbs.append(VGroup(tick, lab))
        hear(self, "The researcher", lead=0.3)
        you = professor_bear("1x1", 1.7, seed="B21", x=3.3, y=2.1)
        ylab = T("you", 44).move_to([4.8, 2.1, 0])
        self.play(FadeIn(you), FadeIn(ylab), run_time=0.4)
        hear(self, "spend", lead=0.1)
        c1 = chip("spend", 3.7, 0.4, size=44)
        self.play(FadeIn(c1, shift=LEFT * 0.3), run_time=0.25)
        hear(self, "access", lead=0.15)
        c2 = chip("access", 3.7, -0.55, size=44)
        self.play(FadeIn(c2, shift=LEFT * 0.3), run_time=0.25)
        hear(self, "cannot be undone", lead=0.5)
        c3 = chip("cannot undo", 3.7, -1.5, size=44)
        self.play(FadeIn(c3, shift=LEFT * 0.3), run_time=0.25)
        hear(self, "Look before", lead=0.2)
        p1 = T("look first", 44).move_to([-4.0, -2.9, 0])
        self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.3)
        hear(self, "measure before", lead=0.2)
        p2 = T("measure first", 44).move_to([0.0, -2.9, 0])
        self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.3)
        hear(self, "ask before", lead=0.2)
        p3 = T("ask first", 44).move_to([4.0, -2.9, 0])
        self.play(FadeIn(p3, shift=UP * 0.2), run_time=0.3)
        done(self)
