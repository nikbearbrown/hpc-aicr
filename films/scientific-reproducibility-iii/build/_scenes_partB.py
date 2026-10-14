# ═════════════════════════════ PART B — B32 B35 B38 B40 B50 ═════════════════════════════
# Uses the shared helpers pA_* from part A (they are in scope: the parts are concatenated).


def pB_pipe(a, b, w=18):
    return VGroup(Line(a, b, color=INK, stroke_width=w + 8), Line(a, b, color=BAR2, stroke_width=w))


class B32_ComputeNode(Scene):
    """The box is crossed out on the shared login node; srun --pty bash asks for a compute node, its lights come on, the box runs there."""
    def construct(self):
        login = pA_rack(-4.2, -0.6, 0.9)
        ll = T("login node", 36).move_to([-4.2, -2.1, 0])
        comp = pA_rack(3.6, -0.5, 1.15)
        cl = T("compute node", 36).move_to([3.6, -2.25, 0])
        self.add(pA_act_title("III · Running A Container"))
        self.play(FadeIn(login), FadeIn(ll), FadeIn(comp), FadeIn(cl), run_time=0.5)
        box = pA_box(-4.2, 0.75, 0.75)
        hear(self, "never on the login", lead=0.3)
        self.play(FadeIn(box), run_time=0.3)
        xm = x_mark(-2.7, 0.55, r=0.35, w=11)
        self.play(Create(xm), run_time=0.3)
        hear(self, "shared by everyone", lead=0.1)
        dots = pA_dots(-4.2, -0.6, n=8, rad=1.35)
        self.play(FadeIn(dots), run_time=0.4)
        hear(self, "Ask", lead=0.1)
        cmdc = chip("srun --pty bash", -2.0, 2.0, mono=True, size=32)
        self.play(FadeIn(cmdc), run_time=0.3)
        self.play(cmdc.animate.move_to([2.7, 2.0, 0]), run_time=0.7)
        self.play(*[d.animate.set_color(TERRA) for d in comp.lights], run_time=0.4)
        hear(self, "work inside", lead=0.1)
        self.play(FadeOut(box), FadeOut(xm), FadeOut(dots), run_time=0.25)
        box2 = pA_box(3.6, 1.1, 0.75)
        self.play(FadeIn(box2), run_time=0.3)
        self.play(Create(check(5.0, 1.2, s=0.3, color=TERRA, w=12)), run_time=0.35)
        done(self)


class B35_NvBridge(Scene):
    """The container carries its own CUDA but is cut off from the driver; the --nv flag lays a bridge from the node's driver in."""
    def construct(self):
        self.add(pA_act_title("III · Running A Container"))
        rack = pA_rack(-4.2, -1.9, 0.95)
        rl = T("GPU node", 36).move_to([-4.2, -3.2, 0])
        drv = logo_chip("nvidia", -4.2, -0.1, h=1.1)
        dl = T("driver", 36).move_to([-4.2, 0.85, 0])
        frame = Rectangle(width=4.2, height=2.5, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.0, 0.5, 0])
        cu = chip("CUDA", 3.0, 0.5, mono=True, size=34)
        cl = T("container", 36).move_to([3.0, -1.1, 0])
        self.play(FadeIn(rack), FadeIn(rl), FadeIn(drv), FadeIn(dl), run_time=0.4)
        hear(self, "container can carry", lead=0.1)
        self.play(FadeIn(frame), FadeIn(cl), run_time=0.35)
        self.play(FadeIn(cu), run_time=0.3)
        hear(self, "still needs", lead=0.2)
        gap = DashedLine([-3.3, -0.1, 0], [0.7, 0.3, 0], color=KRAFT_DEEP, stroke_width=6)
        self.play(Create(gap), run_time=0.4)
        xm = x_mark(-0.9, 0.1, r=0.3, w=10)
        no = T("no GPU", 34).move_to([-0.9, 0.9, 0])
        self.play(Create(xm), FadeIn(no), run_time=0.3)
        hear(self, "flag passes", lead=0.2)
        self.play(FadeOut(gap), FadeOut(xm), FadeOut(no), run_time=0.25)
        br = pB_pipe([-3.3, -0.1, 0], [0.9, -0.1, 0])
        nv = chip("--nv", -1.2, 0.6, mono=True, size=34)
        self.play(Create(br), run_time=0.45)
        self.play(FadeIn(nv), run_time=0.25)
        hear(self, "no link", lead=0.1)
        self.play(Create(check(-0.8, -1.0, s=0.3, color=TERRA, w=12)), run_time=0.35)
        done(self)


class B38_TimeLimits(Scene):
    """Partition limits as bars (8 h, 2 h, 2 h); a two-GPU, 12 hour request grows past the 8 h line and is crossed out."""
    def construct(self):
        self.add(pA_act_title("III · Running A Container"))
        x0, u = -2.0, 0.6
        X = lambda h: x0 + u * h
        axis = Line([x0, -2.0, 0], [X(12), -2.0, 0], color=INK, stroke_width=5)
        ticks = VGroup(*[Line([X(h), -2.0, 0], [X(h), -2.18, 0], color=INK, stroke_width=4) for h in range(0, 13, 2)])
        nums = VGroup(*[T(str(h), 32).move_to([X(h), -2.55, 0]) for h in range(0, 13, 4)])
        hrs = T("hours", 32).move_to([X(12) - 0.1, -3.05, 0])
        self.play(Create(axis), Create(ticks), FadeIn(nums), FadeIn(hrs), run_time=0.5)
        rows = [("gpu-interactive", 2, 1.75), ("gpu-short", 2, 0.9), ("gpu", 8, 0.05)]
        hear(self, "partition limit", lead=0.2)
        for name, h, y in rows:
            lab = M(name, 28).move_to([x0 - 0.3 - M(name, 28).width / 2, y, 0])
            bar = Rectangle(width=u * h, height=0.5, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([X(h / 2), y, 0])
            val = M(f"{h}:00:00", 28).move_to([X(h) + 0.25 + 0.7, y, 0])
            self.play(FadeIn(lab), GrowFromEdge(bar, LEFT), FadeIn(val), run_time=0.45)
        line = DashedLine([X(8), 2.3, 0], [X(8), -2.0, 0], color=KRAFT_DEEP, stroke_width=5)
        self.play(Create(line), run_time=0.3)
        hear(self, "published example", lead=0.3)
        rl = M("--gres=gpu:2", 28).move_to([x0 - 0.3 - M("--gres=gpu:2", 28).width / 2, -1.0, 0])
        req = Rectangle(width=u * 12, height=0.5, fill_color=KRAFT_DEEP, fill_opacity=1, stroke_width=0).move_to([X(6), -1.0, 0])
        self.play(FadeIn(rl), GrowFromEdge(req, LEFT), run_time=1.0)
        hear(self, "cannot run", lead=0.25)
        self.play(Create(x_mark(X(12) + 0.45, -1.0, r=0.3, w=10)), run_time=0.3)
        done(self)


class B40_WhatItSees(Scene):
    """Home slides into the container by itself; /projects and /scratch wait outside until --bind carries each in."""
    def construct(self):
        self.add(pA_act_title("IV · Binding Folders"))
        frame = Rectangle(width=4.6, height=4.6, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.2, -0.2, 0])
        fl = T("container", 36).move_to([3.2, 2.45, 0])
        slots = VGroup(*[DashedVMobject(Rectangle(width=3.0, height=1.05, color=BAR1, stroke_width=4).move_to([3.2, y, 0]), num_dashes=24)
                         for y in (1.2, -0.2, -1.6)])
        self.play(FadeIn(frame), FadeIn(fl), FadeIn(slots), run_time=0.5)
        hear(self, "own file system", lead=0.3)
        specs = [("home", 1.2, None), ("/projects", -0.2, "mono"), ("/scratch", -1.6, "mono")]
        folders = []
        for nm, y, kind in specs:
            f = pA_folder(-5.0, y, 1.5, 0.9)
            lab = (M(nm, 32) if kind else T(nm, 36)).move_to([-3.35 + (0.55 if kind else 0.0), y, 0])
            if nm == "home":
                f.add(Dot([-5.0, y, 0], radius=0.11, color=TERRA))
            folders.append(VGroup(f, lab))
        self.play(*[FadeIn(g) for g in folders], run_time=0.45)
        hear(self, "home directory", lead=0.2)
        self.play(folders[0].animate.move_to([3.2, 1.2, 0]), run_time=0.6)
        self.play(FadeOut(slots[0]), run_time=0.15)
        hear(self, "slash projects", lead=0.2)
        for g in folders[1:]:
            self.play(g.animate.shift(RIGHT * 0.25), run_time=0.2)
            self.play(g.animate.shift(LEFT * 0.25), run_time=0.2)
        hear(self, "bind each", lead=0.3)
        for g, y in zip(folders[1:], (-0.2, -1.6)):
            br = pB_pipe([-1.5, y, 0], [1.2, y, 0], w=14)
            c = chip("--bind", -0.1, y + 0.7, mono=True, size=28)
            self.play(Create(br), FadeIn(c), run_time=0.35)
            self.play(FadeOut(slots[2 if y < -1 else 1]), run_time=0.15)
            self.play(g.animate.move_to([3.2, y, 0]), run_time=0.4)
        done(self)


class B50_BuildCopyRun(Scene):
    """Build on your own computer (root), copy the finished file, store it in project space, run it on a compute node as you."""
    def construct(self):
        self.add(pA_act_title("V · Building An Image"))
        lap = pA_laptop(-4.6, -0.4, 0.8)
        ll = T("your computer", 34).move_to([-4.6, -1.7, 0])
        dk = logo_chip("docker", -5.3, 1.9, h=0.9)
        ap = logo_chip("apptainer", -3.9, 1.9, h=0.9)
        root = chip("root", -4.6, 0.9, mono=True, size=30)
        hear(self, "cannot build", lead=0.1)
        self.play(FadeIn(lap), FadeIn(ll), run_time=0.35)
        hear(self, "administrator rights", lead=0.2)
        self.play(FadeIn(root), FadeIn(dk), FadeIn(ap), run_time=0.4)
        hear(self, "build on a machine", lead=0.1)
        box = pA_box(-2.6, -0.2, 0.85)
        box.set_z_index(6)
        self.play(GrowFromCenter(box), run_time=0.4)
        fol = pA_folder(0.3, -0.35, 1.7, 1.0)
        fl = T("project space", 34).move_to([0.3, -1.6, 0])
        rack = pA_rack(4.0, -0.7, 1.0)
        rl = T("compute node", 34).move_to([4.0, -2.2, 0])
        hear(self, "Copy the finished", lead=0.2)
        a1 = pA_arrow([-1.8, -0.2, 0], [-0.7, -0.2, 0], w=5, tip=0.25)
        cp = T("copy", 34).move_to([-1.25, 0.35, 0])
        self.play(Create(a1), FadeIn(cp), FadeIn(fol), FadeIn(fl), run_time=0.45)
        self.play(box.animate.move_to([0.3, -0.1, 0]), run_time=0.5)
        hear(self, "store it", lead=0.1)
        self.play(Create(check(1.5, 0.35, s=0.28, color=TERRA, w=11)), run_time=0.4)
        hear(self, "run it there", lead=0.3)
        a2 = pA_arrow([1.4, -0.3, 0], [2.6, -0.3, 0], w=5, tip=0.25)
        self.play(Create(a2), FadeIn(rack), FadeIn(rl), run_time=0.4)
        self.play(box.animate.move_to([4.0, 0.75, 0]), run_time=0.5)
        bear = professor_bear("1x1", 1.3, seed="B50", x=5.5, y=1.9)
        ay = T("as yourself", 32).move_to([5.2, 2.95, 0])
        self.play(FadeIn(bear), FadeIn(ay), run_time=0.3)
        done(self)
