# ═════════════════════════════ PART B — B22 B25 B28 B29 ═════════════════════════════

def pB_left(mob, x0, y):
    return mob.move_to([x0 + mob.width / 2, y, 0])


class B22_HardNevers(Scene):
    """Six hard nevers land as table rows, each with a cross."""
    def construct(self):
        top = Line([-5.9, 3.05, 0], [5.9, 3.05, 0], color=INK, stroke_width=5)
        self.play(Create(top), run_time=0.4)
        items = [("compute on a login node", "run computation"), ("password or key", "ask for read"),
                 ("delete without a list", "delete without"), ("submit unconfirmed", "submit a job"),
                 ("scancel -u", "cancel with"), ("invent a flag", "invent a flag")]
        ys = [2.55 - 1.0 * i for i in range(6)]
        for (txt, cue), y in zip(items, ys):
            hear(self, cue, lead=0.5)
            p = pill(-5.0, y, 1.9, h=0.7, fill=BOX_L)
            nv = T("never", 36, bold=True).move_to([-5.0, y, 0])
            it = pB_left(M(txt, 32), -3.5, y)
            sep = Line([-5.9, y - 0.5, 0], [5.9, y - 0.5, 0], color=GHOST, stroke_width=3)
            xm = x_mark(5.2, y, r=0.25, w=9)
            self.play(FadeIn(p), FadeIn(nv), FadeIn(it), Create(sep), run_time=0.35)
            self.play(Create(xm), run_time=0.2)
        done(self)


class B25_TwelveSlowerThanEight(Scene):
    """Bars grow on the spoken core counts; the 12-core bar is ringed: slower than 8."""
    def construct(self):
        data = [(1, 250.7), (2, 116.8), (4, 58.1), (8, 29.4), (12, 33.4), (16, 25.2), (20, 20.2)]
        base, k = -2.2, 4.0 / 250.7
        xs = [-4.8 + 1.6 * i for i in range(7)]
        axis = Line([-5.8, base, 0], [5.8, base, 0], color=INK, stroke_width=5)
        unit = T("seconds", 34).move_to([-5.0, 3.1, 0])
        self.play(Create(axis), FadeIn(unit), run_time=0.4)
        bars, tops, labs = [], [], []
        for (c, s), x in zip(data, xs):
            h = s * k
            b = Rectangle(width=1.0, height=h, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
            b.move_to([x, base + h / 2, 0])
            v = T(f"{s} s", 32).move_to([x, base + h + 0.4, 0])
            l = T(f"{c} core" if c == 1 else (f"{c} cores"), 32).move_to([x, base - 0.45, 0])
            bars.append(b); tops.append(v); labs.append(l)

        def grow(i, rt=0.5):
            return [GrowFromEdge(bars[i], DOWN), FadeIn(tops[i]), FadeIn(labs[i])]
        hear(self, "1 core took", lead=0.2)
        self.play(*grow(0), run_time=0.5)
        hear(self, "250 seconds", lead=0.0)
        self.play(*grow(1), *grow(2), run_time=0.45)
        hear(self, "8 cores took", lead=0.2)
        self.play(*grow(3), run_time=0.5)
        hear(self, "12 cores took", lead=0.2)
        self.play(*grow(4), run_time=0.5)
        hear(self, "slower than 8", lead=0.1)
        ring = Rectangle(width=1.5, height=bars[4].height + 0.5 + 0.9, stroke_color=TERRA, stroke_width=7, fill_opacity=0)
        ring.move_to([xs[4], base + (bars[4].height + 0.5 + 0.9) / 2 - 0.1, 0])
        tag = T("slower than 8", 34).move_to([xs[4], base + 3.0, 0])
        self.play(Create(ring), FadeIn(tag), run_time=0.45)
        hear(self, "promise that", lead=0.2)
        self.play(*grow(5), run_time=0.45)
        hear(self, "times faster", lead=0.3)
        self.play(*grow(6), run_time=0.45)
        done(self)


class B28_WhereFilesLive(Scene):
    """home / scratch / projects; the only copy leaves scratch for projects before the first-Tuesday sweep."""
    def construct(self):
        ih = Iso(-4.5, -1.3, 0.9)
        home = home_box(ih)
        hn = T("home", 40).move_to([-4.5, -2.7, 0])
        hc1 = T("code", 34).move_to([-4.5, 1.7, 0]); hc2 = T("environments", 34).move_to([-4.5, 1.25, 0])
        isx = Iso(-0.5, -1.7, 0.9)
        back, front = scratch_bin(isx)
        sn = T("scratch", 40).move_to([0.2, -2.9, 0])
        junk1 = job_box(isx, 0.3, 0.3, 0.0, s=0.55); junk2 = job_box(isx, 1.5, 0.9, 0.0, s=0.55)
        only = job_box(isx, 1.4, 0.2, 0.0, s=0.55)
        olab = T("only copy", 34).move_to([1.2, 1.1, 0])
        self.play(FadeIn(home), FadeIn(hn), run_time=0.4)
        hear(self, "code and environments", lead=0.2)
        self.play(FadeIn(hc1), FadeIn(hc2), run_time=0.3)
        hear(self, "temporary job data", lead=0.3)
        self.play(FadeIn(back), FadeIn(front), FadeIn(sn), FadeIn(junk1), FadeIn(junk2), run_time=0.4)
        hear(self, "wiped on", lead=0.9)
        cal = paper(-1.0, 2.2, w=1.5, h=1.5)
        grid = VGroup(*[Line([-1.55, 2.2 + 0.4 - 0.3 * i, 0], [-0.45, 2.2 + 0.4 - 0.3 * i, 0], color=BAR3, stroke_width=4) for i in range(4)])
        cdot = Dot([-1.3, 2.2 - 0.05, 0], radius=0.09, color=TERRA)
        ft = T("first Tuesday", 34).move_to([1.2, 2.2, 0])
        self.play(FadeIn(cal), Create(grid), FadeIn(cdot), run_time=0.4)
        self.play(FadeIn(ft), run_time=0.25)
        hear(self, "keep in projects", lead=0.5)
        ip = Iso(4.5, -1.3, 0.9)
        proj = home_box(ip)
        pn = T("projects", 40).move_to([4.5, -2.7, 0])
        pc = T("long-term", 34).move_to([4.5, 2.0, 0])
        ck = check(5.7, 1.6, s=0.28, color=INK)
        self.play(FadeIn(proj), FadeIn(pn), FadeIn(pc), Create(ck), run_time=0.45)
        hear(self, "never keeps the only", lead=0.6)
        self.play(FadeIn(only), FadeIn(olab), run_time=0.3)
        grp = VGroup(only, olab)
        path = VMobject()
        c0 = grp.get_center()
        path.set_points_smoothly([c0, [2.5, 1.2, 0], [4.0, 1.0, 0], [4.5, 0.0, 0]])
        self.play(MoveAlongPath(grp, path), run_time=1.0, rate_func=smooth)
        hear(self, "of anything in", lead=0.3)
        broom = Rectangle(width=0.3, height=1.6, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.9, -1.0, 0])
        self.play(FadeIn(broom), run_time=0.2)
        self.play(broom.animate.shift(RIGHT * 3.6), AnimationGroup(FadeOut(junk1), FadeOut(junk2), lag_ratio=0.6), run_time=0.7, rate_func=smooth)
        self.play(FadeOut(broom), run_time=0.25)
        done(self)


class B29_InstallLadder(Scene):
    """Five rungs, cost bar widening; the agent checks module avail on the top rung."""
    def construct(self):
        names = ["module", "conda", "container (built at home)", "source build", "Spack / EasyBuild (last)"]
        cues = ["first a module", "then conda", "a container", "a source build", "a tool like"]
        ys = [2.5 - 1.2 * i for i in range(5)]
        rails = VGroup(Line([-5.9, 3.0, 0], [-5.9, -3.0, 0], color=INK, stroke_width=7),
                       Line([-4.7, 3.0, 0], [-4.7, -3.0, 0], color=INK, stroke_width=7))
        self.play(Create(rails), run_time=0.4)
        labs, bars = [], []
        for i, (n, c, y) in enumerate(zip(names, cues, ys)):
            hear(self, c, lead=0.6 if i == 4 else 0.35)
            rung = Line([-5.9, y, 0], [-4.7, y, 0], color=INK, stroke_width=7)
            lab = pB_left(T(n, 36), -4.3, y)
            w = 0.7 * (i + 1)
            bar = Rectangle(width=w, height=0.5, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3)
            bar.move_to([1.2 + w / 2, y, 0])
            self.play(Create(rung), FadeIn(lab), GrowFromEdge(bar, LEFT), run_time=0.45)
            labs.append(lab); bars.append(bar)
        hear(self, "costs more", lead=0.3)
        ct = T("cost", 36).move_to([2.2, 3.05, 0])
        self.play(FadeIn(ct), run_time=0.3)
        hear(self, "Before installing", lead=0.2)
        claude = logo_chip("claude", 5.2, 2.7, h=1.0)
        self.play(FadeIn(claude), run_time=0.3)
        lens = Circle(radius=0.3, stroke_color=INK, stroke_width=7, fill_color=PAGE_TOP, fill_opacity=0.9).move_to([3.6, 2.5, 0])
        handle = Line([3.82, 2.28, 0], [4.1, 2.0, 0], color=INK, stroke_width=9)
        mag = VGroup(lens, handle)
        cmd = M("module avail", 32).move_to([4.2, 1.95, 0])
        self.play(FadeIn(mag), FadeIn(cmd), run_time=0.3)
        hear(self, "whether a module", lead=0.2)
        self.play(mag.animate.shift(LEFT * 5.4), run_time=1.2, rate_func=smooth)
        self.play(Indicate(labs[0], color=TERRA, scale_factor=1.1), run_time=0.5)
        done(self)
