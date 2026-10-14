# ═════════════════════════════ PART C — B32 B33 B40 B41 ═════════════════════════════

def pC_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pC_card(x, y, w=4.0, h=2.9):
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    sheet = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(shadow, sheet)


def pC_tag(x, y):
    """The 'do not copy' tag: a white pill, a terracotta dot, ink text."""
    p = pill(x, y, 3.0, h=0.8)
    sh = pill(x + 0.08, y - 0.08, 3.0, h=0.8, fill=BOX_L)
    dot = Dot([x - 1.2, y, 0], radius=0.11, color=TERRA)
    lab = T("do not copy", 34).move_to([x + 0.2, y, 0])
    return VGroup(sh, p, dot, lab)


class B32_DoNotCopy(Scene):
    """Three wrong slide lines get a 'do not copy' tag; the Claude chip nods past each and takes none."""
    def construct(self):
        ys = [1.9, 0.0, -1.9]
        cx, L0 = -1.1, -3.65
        claude = logo_chip("claude", -5.3, ys[0])
        self.play(FadeIn(claude), run_time=0.4)

        def nod(y):
            self.play(claude.animate.move_to([-5.3, y, 0]), run_time=0.35, rate_func=smooth)
            self.play(claude.animate.shift(RIGHT * 0.3), run_time=0.15)
            self.play(claude.animate.shift(LEFT * 0.3), run_time=0.15)

        def left(m, y):
            return m.move_to([L0 + m.width / 2, y, 0])
        # card 1: the line cut at the backslash
        hear(self, "a comment after a line", lead=0.3)
        c1 = pC_card(cx, ys[0], w=5.6, h=1.6)
        l1 = left(M("python train.py \\", 32), ys[0] + 0.35)
        l2 = left(M("# CHANGE", 32), ys[0] - 0.4)
        cut = Line([L0, ys[0] - 0.02, 0], [L0 + 4.2, ys[0] - 0.02, 0], color=BAR1, stroke_width=4)
        self.play(FadeIn(c1), run_time=0.3)
        self.play(FadeIn(l1), FadeIn(l2), Create(cut), run_time=0.4)
        hear(self, "which breaks the command", lead=0.2)
        t1 = pC_tag(4.2, ys[0])
        self.play(GrowFromCenter(t1), run_time=0.35)
        nod(ys[0])
        # card 2: a partition that is not there
        hear(self, "a partition called compute", lead=0.4)
        c2 = pC_card(cx, ys[1], w=5.6, h=1.6)
        p2 = left(M("--partition=compute", 32), ys[1] + 0.35)
        slab = DashedVMobject(Rectangle(width=3.2, height=0.5, color=BAR1, stroke_width=4)).move_to([L0 + 1.6, ys[1] - 0.4, 0])
        self.play(FadeIn(c2), FadeIn(p2), Create(slab), run_time=0.4)
        hear(self, "which does not exist", lead=0.3)
        t2 = pC_tag(4.2, ys[1])
        self.play(GrowFromCenter(t2), run_time=0.35)
        nod(ys[1])
        # card 3: no time, no memory
        hear(self, "a sample script", lead=0.3)
        c3 = pC_card(cx, ys[2], w=5.6, h=1.6)
        p3 = left(M("sbatch", 32), ys[2] + 0.35)
        s1 = DashedVMobject(Rectangle(width=0.9, height=0.5, color=BAR1, stroke_width=4)).move_to([-3.35, ys[2] - 0.4, 0])
        s2 = DashedVMobject(Rectangle(width=0.9, height=0.5, color=BAR1, stroke_width=4)).move_to([-0.6, ys[2] - 0.4, 0])
        n1 = M("--time", 32).move_to([-2.0, ys[2] - 0.4, 0])
        n2 = M("--mem", 32).move_to([0.8, ys[2] - 0.4, 0])
        self.play(FadeIn(c3), FadeIn(p3), Create(s1), Create(s2), FadeIn(n1), FadeIn(n2), run_time=0.4)
        hear(self, "no time and no memory", lead=-0.3)
        t3 = pC_tag(4.2, ys[2])
        self.play(GrowFromCenter(t3), run_time=0.35)
        hear(self, "told not to copy", lead=0.3)
        nod(ys[2])
        done(self)


def pC_stamp(text, x, y, w=2.8):
    sh = pill(x + 0.08, y - 0.08, w, h=0.8, fill=BOX_L)
    p = pill(x, y, w, h=0.8)
    dot = Dot([x - w / 2 + 0.3, y, 0], radius=0.1, color=TERRA)
    lab = T(text, 34).move_to([x + 0.15, y, 0])
    return VGroup(sh, p, dot, lab)


class B33_HonestAppendix(Scene):
    """Two sources disagree on the scratch quota; the file refuses to quote either; two stamps mark the judgment rules."""
    def construct(self):
        ax, bx, py = -4.85, -1.5, 0.9
        pa = paper(ax, py, w=2.7, h=2.8)
        pb = paper(bx, py, w=2.7, h=2.8)
        qa = T("scratch quota", 32).move_to([ax, py + 0.85, 0])
        qb = T("scratch quota", 32).move_to([bx, py + 0.85, 0])
        la = T("slides", 34).move_to([ax, -0.9, 0])
        lb = T("policy page", 34).move_to([bx, -0.9, 0])
        self.play(FadeIn(pa), FadeIn(pb), FadeIn(qa), FadeIn(qb), FadeIn(la), FadeIn(lb), run_time=0.5)
        # "the file says so": the rule line draws
        hear(self, "the file says so", lead=0.3)
        rule = Line([-5.8, -2.4, 0], [-1.6, -2.4, 0], color=BAR2, stroke_width=8)
        self.play(Create(rule), run_time=0.6)
        # 50 TB then 20 TB
        hear(self, "50 terabytes", lead=0.25)
        n50 = T("50 TB", 60, bold=True).move_to([ax, py - 0.3, 0])
        self.play(FadeIn(n50, shift=UP * 0.2), run_time=0.35)
        hear(self, "20 on the", lead=0.15)
        n20 = T("20 TB", 60, bold=True).move_to([bx, py - 0.3, 0])
        self.play(FadeIn(n20, shift=UP * 0.2), run_time=0.35)
        # not-equal sign between the pages
        hear(self, "policy page", lead=0.1)
        neq = VGroup(Line([-3.4, py + 0.25, 0], [-2.95, py + 0.25, 0], color=INK, stroke_width=9),
                     Line([-3.4, py - 0.15, 0], [-2.95, py - 0.15, 0], color=INK, stroke_width=9),
                     Line([-3.05, py + 0.5, 0], [-3.3, py - 0.4, 0], color=INK, stroke_width=9))
        self.play(Create(neq), run_time=0.4)
        # the third card: never quote a number
        hear(self, "never to quote a number", lead=0.8)
        c3 = pC_card(3.4, py, w=4.6, h=2.8)
        t1 = T("the file:", 36).move_to([3.4, py + 0.55, 0])
        t2 = T("never quote a number", 34, bold=True).move_to([3.4, py - 0.3, 0])
        self.play(FadeIn(c3), FadeIn(t1), FadeIn(t2), run_time=0.5)
        # stamps beside a rule line
        hear(self, "house rule", lead=0.2)
        s1 = pC_stamp("house rule", 0.7, -2.4)
        self.play(GrowFromCenter(s1), run_time=0.35)
        hear(self, "or inferred", lead=0.0)
        s2 = pC_stamp("inferred", 3.9, -2.4, w=2.6)
        self.play(GrowFromCenter(s2), run_time=0.35)
        done(self)


class B40_AssumeNotExplorer(Scene):
    """AICR.md sits on top of HPC.md and wins; four Explorer items slide toward the AICR rack and bounce off."""
    def construct(self):
        hpc = paper(-4.7, 0.1, w=2.4, h=3.0, fill=GHOST)
        hl = VGroup(*[Line([-5.7, 0.9 - 0.45 * i, 0], [-3.7 - (0.5 if i == 2 else 0), 0.9 - 0.45 * i, 0], color=BAR2, stroke_width=7) for i in range(3)])
        hlab = M("HPC.md", 32).move_to([-4.7, -1.75, 0])
        stack, lights = aicr_rack(Iso(3.8, -2.0, 1.1))
        rlab = T("AICR", 40).move_to([4.2, -3.05, 0])
        title = pC_act_title("III · What AICR.md Changes")
        self.play(FadeIn(title), FadeIn(hpc), FadeIn(hl), FadeIn(hlab), FadeIn(stack), FadeIn(lights), FadeIn(rlab), run_time=0.5)
        # "AICR.md ... it wins on AICR": the white page lands on top, then lights
        hear(self, "AICR", lead=0.2)
        aic = paper(-3.9, 0.5, w=2.4, h=3.0)
        al = VGroup(*[Line([-4.9, 1.3 - 0.45 * i, 0], [-2.9 - (0.5 if i == 2 else 0), 1.3 - 0.45 * i, 0], color=INK, stroke_width=6) for i in range(3)])
        alab = M("AICR.md", 32).move_to([-3.9, 2.5, 0])
        page = VGroup(aic, al)
        self.play(FadeIn(page, shift=DOWN * 1.2), FadeIn(alab), run_time=0.6)
        hear(self, "wins on", lead=0.1)
        ring = Rectangle(width=2.7, height=3.3, color=TERRA, stroke_width=6).move_to([-3.9, 0.5, 0])
        self.play(Create(ring), run_time=0.5)
        # four Explorer items bounce off the rack
        items = [("host", 1.6, "hosts"), ("partition", 0.55, "partitions"), ("storage", -0.5, "storage rules"), ("module", -1.5, "module setup")]
        for name, y, cue in items:
            hear(self, cue, lead=0.5)
            c = chip(name, -1.15, y, w=2.5, size=32)
            self.play(FadeIn(c), run_time=0.15)
            self.play(c.animate.shift(RIGHT * 1.7), run_time=0.3, rate_func=smooth)
            bump = x_mark(2.15, y, r=0.25, w=8)
            self.play(Create(bump), c.animate.shift(LEFT * 0.6), run_time=0.25, rate_func=smooth)
            self.play(FadeOut(bump), run_time=0.15)
        hear(self, "assume AICR", lead=0.2)
        line = T("AICR is not Explorer", 46, bold=True).move_to([2.6, 2.7, 0])
        self.play(FadeIn(line, shift=DOWN * 0.3), run_time=0.4)
        self.play(*[l.animate.set_color(TERRA) for l in lights], run_time=0.5)
        done(self)


class B41_AICRDiffers(Scene):
    """A two-column table builds row by row, each row on its spoken words."""
    def construct(self):
        rows = [("user name", "dot becomes underscore, _neu added", "username is built"),
                ("login", "key + certificate, no password", "no password"),
                ("GPU", "the partition picks it", "partition decides"),
                ("idle GPU", "cancelled automatically", "idle GPUs"),
                ("scratch", "purged after 30 days, no off-site backup", "purged after 30 days")]
        ys = [2.1, 1.05, 0.0, -1.05, -2.1]
        top = Line([-6.0, 2.75, 0], [6.0, 2.75, 0], color=INK, stroke_width=6)
        div = Line([-3.5, 2.75, 0], [-3.5, -2.75, 0], color=BAR2, stroke_width=6)
        self.play(Create(top), Create(div), run_time=0.5)
        for (k, v, cue), y in zip(rows, ys):
            hear(self, cue, lead=0.2)
            key = T(k, 38, bold=True)
            key.move_to([-6.0 + key.width / 2, y, 0])
            val = T(v, 34)
            val.move_to([-3.2 + val.width / 2, y, 0])
            sep = Line([-6.0, y - 0.52, 0], [6.0, y - 0.52, 0], color=BAR3, stroke_width=5)
            self.play(FadeIn(key), Create(sep), run_time=0.3)
            self.play(FadeIn(val, shift=RIGHT * 0.3), run_time=0.35)
        done(self)
