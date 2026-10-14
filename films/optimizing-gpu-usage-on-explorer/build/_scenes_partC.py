# ═════════════════════════════ PART C — Acts V and VI (manim beats) ═════════════════════════════


class B50_BatchDoubles(Scene):
    """A batch block in the VRAM tank doubles (20, 40 percent), throughput arrows double, the ceiling and the optimizer's margin."""
    def construct(self):
        title = act_title("V · Memory And Precision")
        yb, yt, tw, cx = -2.7, 1.7, 2.4, -2.6
        H = yt - yb
        tk = tank(cx, yb, yt, tw)
        vl = lab_c("VRAM", cx, -3.15, 34)
        def blkh(f, fill=BAR2):
            return blk(cx, yb + 0.05, 1.9, H * f, fill)
        b1, b2, b3 = blkh(0.2), blkh(0.4), blkh(0.7)
        p1 = lab_l("20%", cx + 1.45, yb + H * 0.1, 36)
        p2 = lab_l("40%", cx + 1.45, yb + H * 0.2, 36)
        a1 = Arrow([0.8, -1.9, 0], [2.0, -1.9, 0], color=INK, stroke_width=9, buff=0, max_tip_length_to_length_ratio=0.35)
        a2 = Arrow([0.8, -0.8, 0], [3.2, -0.8, 0], color=INK, stroke_width=9, buff=0, max_tip_length_to_length_ratio=0.35)
        th = lab_l("throughput", 0.8, -0.1, 36)
        ceil_y = yb + H * 0.88
        ceil = DashedLine([cx - 1.5, ceil_y, 0], [cx + 1.5, ceil_y, 0], color=INK, stroke_width=5)
        cl = lab_l("largest that fits", cx + 1.65, ceil_y, 34)
        opt = blk(cx, yb + H * 0.7 + 0.05, 1.9, 0.5, BAR3)
        opl = lab_l("optimizer", cx + 1.45, yb + H * 0.7 + 0.35, 34)
        self.play(FadeIn(title), FadeIn(tk), FadeIn(vl), run_time=0.5)
        hear(self, "Doubling", lead=0.5)
        self.play(FadeIn(b1), FadeIn(p1), Create(a1), FadeIn(th), run_time=0.5)
        hear(self, "doubles", lead=0.1)
        self.play(Transform(b1, b2), Transform(p1, p2), Create(a2), run_time=0.7)
        hear(self, "saturated", lead=0.6)
        self.play(Create(ceil), FadeIn(cl), run_time=0.5)
        hear(self, "20", lead=0.2)
        self.play(Transform(b1, blkh(0.2)), Transform(p1, lab_l("20%", cx + 1.45, yb + H * 0.1, 36)), run_time=0.5)
        hear(self, "double the batch", lead=0.1)
        self.play(Transform(b1, b2), Transform(p1, p2), run_time=0.6)
        hear(self, "Stop short", lead=0.1)
        self.play(Transform(b1, b3), FadeOut(p1), run_time=0.7)
        hear(self, "optimizer", lead=0.2)
        self.play(FadeIn(opt), FadeIn(opl), run_time=0.4)
        done(self)


class B53_BitSplit(Scene):
    """Bit cells: FP32 (1, 8, 23), BF16 (1, 8, 7), FP16 (1, 5, 10); BF16 on A100 and newer, FP16 on V100 and T4 with a scaler."""
    def construct(self):
        title = act_title("V · Memory And Precision")
        x0, cwid = -4.3, 0.19
        def row(y, name, parts):
            cells = VGroup()
            x = x0
            for n, fill in parts:
                for _ in range(n):
                    cells.add(Rectangle(width=cwid - 0.03, height=0.5, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x + cwid / 2, y, 0]))
                    x += cwid
            lab = M(name, 34)
            lab.move_to([x0 - 0.35 - lab.width / 2, y, 0])
            return Group(cells, lab)
        r32 = row(1.5, "FP32", [(1, BAR3), (8, INK), (23, BAR2)])
        r16b = row(0.2, "BF16", [(1, BAR3), (8, INK), (7, BAR2)])
        r16f = row(-1.1, "FP16", [(1, BAR3), (5, INK), (10, BAR2)])
        rng = T("range", 34).move_to([x0 + cwid * 5.5, 2.2, 0])
        prc = T("precision", 34).move_to([x0 + cwid * 21, 2.2, 0])
        c_bf = chip("A100 and newer", 1.2, 0.2, size=32)
        c_ns = chip("no loss scaler", 4.6, 0.2, size=32)
        c_v = chip("V100", 0.5, -1.1, size=32)
        c_t = chip("T4", 2.1, -1.1, size=32)
        c_gs = chip("GradScaler", 4.6, -1.1, mono=True, size=30)

        self.play(FadeIn(title), run_time=0.4)
        hear(self, "splits", lead=0.3)
        self.play(FadeIn(r32), FadeIn(rng), FadeIn(prc), run_time=0.7)
        hear(self, "Bf16", lead=0.2)
        self.play(FadeIn(r16b), run_time=0.5)
        hear(self, "no loss", lead=0.15)
        self.play(FadeIn(c_ns), run_time=0.35)
        hear(self, "Fp16", lead=0.2)
        self.play(FadeIn(r16f), run_time=0.5)
        hear(self, "needs one", lead=0.2)
        self.play(FadeIn(c_gs), run_time=0.35)
        hear(self, "a 100", lead=0.2)
        self.play(FadeIn(c_bf), run_time=0.4)
        hear(self, "V100", lead=0.2)
        self.play(FadeIn(c_v), FadeIn(c_t), run_time=0.4)
        done(self)


class B55_HonestGains(Scene):
    """Only the activations segment halves; weights and optimizer state stay; two speed-up claims disagree: quote neither."""
    def construct(self):
        title = act_title("V · Memory And Precision")
        x0 = -4.6
        def seg(x, w, y, fill):
            return Rectangle(width=w - 0.05, height=0.6, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x + w / 2, y, 0])
        yb_, ya_ = 1.5, 0.2
        bef = VGroup(seg(x0, 3.0, yb_, BAR2), seg(x0 + 3.0, 1.2, yb_, BAR1), seg(x0 + 4.2, 2.0, yb_, BAR3))
        aft = VGroup(seg(x0, 1.5, ya_, BAR2), seg(x0 + 1.5, 1.2, ya_, BAR1), seg(x0 + 2.7, 2.0, ya_, BAR3))
        l1 = T("before", 36).move_to([-5.45, yb_, 0])
        l2 = T("BF16", 36).move_to([-5.45, ya_, 0])
        names = [lab_c("activations", x0 + 1.5, yb_ + 0.7, 32), lab_c("weights", x0 + 3.6, yb_ + 0.7, 32), lab_c("optimizer", x0 + 5.2, yb_ + 0.7, 32)]
        nh = lab_l("not 2x", x0 + 4.7 + 0.3, ya_, 40)
        ops = T("matrix and convolution only", 34).move_to([2.8, -0.9, 0])
        c1 = chip("up to 8x", -4.6, -2.1, size=36)
        q = T("?", 56).move_to([-2.6, -2.1, 0])
        c2 = chip("1.5 to 3x", -0.7, -2.1, size=36)
        qn = T("quote neither", 44).move_to([3.9, -2.1, 0])
        slots55 = [dashed_slot(-4.6, -2.1, 2.6, 0.8), dashed_slot(-0.7, -2.1, 3.0, 0.8), dashed_slot(3.9, -2.1, 3.6, 0.8), dashed_slot(2.8, -0.9, 4.6, 0.5)]
        self.play(FadeIn(title), *[FadeIn(s_) for s_ in slots55], run_time=0.4)
        hear(self, "Total memory", lead=0.1)
        self.play(FadeIn(bef), FadeIn(l1), *[FadeIn(n) for n in names], run_time=0.6)
        hear(self, "drop by half", lead=0.2)
        self.play(FadeIn(l2), FadeIn(aft), run_time=0.5)
        hear(self, "optimizer state", lead=0.2)
        self.play(FadeIn(nh), run_time=0.3)
        hear(self, "speed", lead=0.1)
        self.remove(slots55[3])
        self.play(FadeIn(ops), run_time=0.4)
        hear(self, "eight", lead=0.3)
        self.remove(slots55[0])
        self.play(FadeIn(c1), run_time=0.3)
        hear(self, "one and a half", lead=0.25)
        self.remove(slots55[1])
        self.play(FadeIn(q), FadeIn(c2), run_time=0.35)
        hear(self, "Quote", lead=0.1)
        self.remove(slots55[2])
        self.play(c1.animate.set_opacity(0.4), c2.animate.set_opacity(0.4), FadeIn(qn), run_time=0.4)
        done(self)


class B60_EightyFirst(Scene):
    """A utilization scale (60 fix first, 80 more cards pay); one card at 20 percent becomes four at 20 percent; reading-bound jobs get worse."""
    def construct(self):
        title = act_title("VI · More Than One GPU")
        x0, sc, y = -5.0, 0.1, 2.2
        scale = Line([x0, y, 0], [x0 + 10, y, 0], color=INK, stroke_width=6)
        ends = VGroup(T("0", 32).move_to([x0, y + 0.45, 0]), T("100", 32).move_to([x0 + 10, y + 0.45, 0]))
        t60 = VGroup(Line([x0 + 6, y - 0.2, 0], [x0 + 6, y + 0.2, 0], color=INK, stroke_width=6), T("60", 32).move_to([x0 + 6, y + 0.45, 0]))
        t80 = VGroup(Line([x0 + 8, y - 0.2, 0], [x0 + 8, y + 0.2, 0], color=INK, stroke_width=6), T("80", 32).move_to([x0 + 8, y + 0.45, 0]))
        dot = Dot([x0 + 2, y, 0], radius=0.17, color=TERRA)
        one = gpu_card(-4.6, 0.5, w=1.5, h=0.9)
        p20 = T("20%", 40).move_to([-4.6, -0.3, 0])
        arr = Arrow([-3.6, 0.5, 0], [-2.6, 0.5, 0], color=INK, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.4)
        four = [gpu_card(-1.6 + 1.9 * i, 0.5, w=1.5, h=0.9) for i in range(4)]
        p4 = [T("20%", 36).move_to([-1.6 + 1.9 * i, -0.3, 0]) for i in range(4)]
        cost = T("four times the allocation", 36).move_to([1.2, -0.95, 0])
        f60 = T("fix first", 34).move_to([x0 + 6, y - 0.55, 0])
        pay = T("more cards pay", 34).move_to([x0 + 9, y - 0.55, 0])
        ck = check(x0 + 9.0, y - 1.0, s=0.2, color=TERRA, w=10)
        cr = x_mark(x0 + 6, y - 1.05, r=0.22, w=8)
        rd = chip("reading data", -4.2, -2.3, size=34)
        smalls = [gpu_card(-0.8 + 1.7 * i, -2.3, w=1.3, h=0.8) for i in range(4)]
        arrs = [Arrow([-2.5, -2.3, 0], [-1.6 + 1.7 * i - 0.2 + 0.0, -2.3, 0], color=BAR1, stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.0) for i in range(0)]
        rx = x_mark(5.6, -2.3, r=0.3, w=9)
        self.play(FadeIn(title), Create(scale), FadeIn(ends), run_time=0.5)
        hear(self, "20", lead=0.3)
        self.play(FadeIn(dot), FadeIn(one), FadeIn(p20), run_time=0.4)
        hear(self, "four", lead=0.2)
        self.play(Create(arr), *[FadeIn(c) for c in four], *[FadeIn(p) for p in p4], run_time=0.6)
        self.play(FadeIn(cost), run_time=0.3)
        hear(self, "Add cards", lead=0.15)
        self.play(FadeIn(t80), FadeIn(pay), Create(ck), run_time=0.5)
        hear(self, "Under 60", lead=0.15)
        self.play(FadeIn(t60), FadeIn(f60), Create(cr), run_time=0.5)
        hear(self, "limited", lead=0.2)
        self.play(FadeIn(rd), *[FadeIn(s) for s in smalls], run_time=0.5)
        self.play(Create(rx), run_time=0.3)
        done(self)


class B61_AllReduce(Scene):
    """Four cards each hold a model copy and a different batch; gradients average at one point; every card applies the same update."""
    def construct(self):
        title = act_title("VI · More Than One GPU")
        xs = [-4.5, -1.5, 1.5, 4.5]
        cards = [gpu_card(x, 0.4, w=1.9, h=1.1) for x in xs]
        models = [Rectangle(width=0.7, height=0.4, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x - 0.15, 0.4, 0]) for x in xs]
        mlab = lab_c("model copy", -4.5, 1.35, 32)
        batches = [paper(x, 2.35, w=0.9, h=0.7) for x in xs]
        letters = [T(ch, 36).move_to([x, 2.35, 0]) for ch, x in zip("ABCD", xs)]
        avg = chip("average", 0.0, -1.4, size=36)
        arrs = [Arrow([x, -0.25, 0], [x * 0.35, -1.0, 0], color=INK, stroke_width=6, buff=0.05, max_tip_length_to_length_ratio=0.25) for x in xs]
        thick = Rectangle(width=2.0, height=0.35, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-4.6, -2.7, 0])
        thick_l = lab_l("inside a node: fast", -3.4, -2.7, 34)
        thin = Rectangle(width=3.0, height=0.12, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([2.2, -2.7, 0])
        thin_l = lab_c("between nodes: slower", 2.2, -3.2, 34)
        big = Rectangle(width=2.4, height=1.3, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([4.9, -1.5, 0])
        bigl = lab_c("too big", 4.9, -0.65, 34)
        bx = x_mark(4.9, -1.5, r=0.4, w=10)
        self.play(FadeIn(title), *[FadeIn(c) for c in cards], run_time=0.5)
        hear(self, "full model", lead=0.2)
        self.play(*[FadeIn(m) for m in models], FadeIn(mlab), run_time=0.5)
        hear(self, "different batch", lead=0.45)
        self.play(*[FadeIn(b) for b in batches], *[FadeIn(l) for l in letters], run_time=0.5)
        hear(self, "average", lead=0.2)
        self.play(FadeIn(avg), *[Create(a) for a in arrs], run_time=0.6)
        hear(self, "apply", lead=0.2)
        self.play(*[c.light.animate.set_color(TERRA) for c in cards], run_time=0.4)
        hear(self, "Fast", lead=0.1)
        self.play(FadeIn(thick), FadeIn(thick_l), run_time=0.4)
        hear(self, "slower", lead=0.2)
        self.play(FadeIn(thin), FadeIn(thin_l), run_time=0.4)
        hear(self, "cannot fix", lead=0.1)
        self.play(FadeIn(big), FadeIn(bigl), run_time=0.3)
        self.play(Create(bx), run_time=0.3)
        done(self)


class B66_ScalingEfficiency(Scene):
    """Efficiency = throughput on N cards over N times one card's; above 80 extra cards pay, below 70 stop, 70 to 80 not described."""
    def construct(self):
        title = act_title("VI · More Than One GPU")
        num_l = lab_l("throughput on N cards", -5.7, 2.35, 36)
        num = Rectangle(width=4.0, height=0.45, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0.7, 2.35, 0])
        fl = Line([-5.7, 1.65, 0], [2.9, 1.65, 0], color=INK, stroke_width=6)
        den_l = lab_l("N x one card", -5.7, 0.95, 36)
        den = VGroup(*[Rectangle(width=0.95, height=0.45, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.5 + 1.0 * i + 0.5, 0.95, 0]) for i in range(4)])
        eff = T("= efficiency", 48).move_to([4.5, 1.65, 0])
        x0, sc, y = -5.0, 0.1, -1.2
        s1 = Rectangle(width=7.0 - 0.06, height=0.5, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x0 + 3.5, y, 0])
        s2 = dashed_slot(x0 + 7.5, y, 1.0 - 0.06, 0.5)
        s3 = Rectangle(width=2.0 - 0.06, height=0.5, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x0 + 9.0, y, 0])
        nums = VGroup(*[T(str(v), 32).move_to([x0 + v * sc, y + 0.55, 0]) for v in (0, 70, 80, 100)])
        l1 = lab_c("stop: look for a bottleneck", x0 + 3.5, y - 0.65, 34)
        l2 = T("?", 52).move_to([x0 + 7.5, y - 0.65, 0])
        l2b = lab_c("not described", x0 + 7.5, y - 1.3, 32)
        l3 = lab_c("extra cards pay", x0 + 9.0, y - 0.65, 34)
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "Efficiency", lead=0.2)
        self.play(FadeIn(num_l), GrowFromEdge(num, LEFT), run_time=0.5)
        hear(self, "divided", lead=0.2)
        self.play(Create(fl), FadeIn(den_l), LaggedStart(*[FadeIn(d) for d in den], lag_ratio=0.2), FadeIn(eff), run_time=0.9)
        hear(self, "Above", lead=0.2)
        self.play(FadeIn(nums), GrowFromEdge(s3, LEFT), FadeIn(l3), run_time=0.6)
        hear(self, "Below", lead=0.2)
        self.play(GrowFromEdge(s1, LEFT), FadeIn(l1), run_time=0.7)
        hear(self, "70 to 80", lead=0.4)
        self.play(FadeIn(s2), FadeIn(l2), FadeIn(l2b), run_time=0.4)
        done(self)
