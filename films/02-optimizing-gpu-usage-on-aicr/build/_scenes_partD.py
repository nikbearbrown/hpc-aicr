
# ═════════════════════════════ PART D · B61 B63 (Act VI) · B70 B71 B72 B73 (Act VII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PD_ / b6x_ / b7x_ so the parts never collide.

PD_BAR_H = 0.42


def pd_slab(w=1.1, h=0.36, fill=BAR1):
    """A gradient slab: a flat grey block with an ink outline."""
    return Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=3)


def pd_hbar(x0, y, w, fill=BAR1, h=PD_BAR_H):
    """A horizontal utilization bar anchored at its left edge x0."""
    return Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x0 + w / 2, y, 0])


def pd_slot(ox, oy, s=1.0):
    """An empty job slot: a pale pad with a grey outline, same picture as the previous film's devel slots."""
    return Iso(ox, oy, s).quad([(-0.1, -0.1, 0), (0.8, -0.1, 0), (0.8, 0.8, 0), (-0.1, 0.8, 0)], GHOST, stroke=BAR1, sw=3).set_z_index(-1)


# ─────────────── B61 · data parallel: three batches, three gradients, one all-reduce, one update everywhere ───────────────
B61_OY = -2.3
B61_GX = (-4.3, -2.0, 0.3)
B61_SLAB_Y = 0.05
B61_MERGE = np.array([-2.0, 1.45, 0.0])


def b61_gpu(ox):
    return gpu_block(Iso(ox, B61_OY, 1.0))


def b61_batch(ox):
    return Iso(ox, B61_OY, 1.0).box(0.25, 0.25, 0.5, 0.5, 0.5, 0.35).set_z_index(2)


class B61_AllReduce(Scene):
    def construct(self):
        gpus = [b61_gpu(x) for x in B61_GX]
        self.play(*[FadeIn(VGroup(b, l), shift=DOWN * 0.4) for b, l in gpus], run_time=0.6)
        until(self, "takes a different mini-batch", lead=0.9)
        batches = [b61_batch(x) for x in B61_GX]
        for bx in batches:
            bx.shift(UP * 1.6)
        labels = [T(f"batch {n}", 34).move_to([x, -2.75, 0]) for n, x in zip("ABC", B61_GX)]
        self.play(LaggedStart(*[bx.animate.shift(DOWN * 1.6) for bx in batches], lag_ratio=0.3), run_time=0.9, rate_func=ease_in)
        self.play(*[FadeIn(lb) for lb in labels], *[l.animate.set_color(TERRA) for b, l in gpus], run_time=0.3)
        until(self, "After the backward pass", lead=0.3)
        slabs = [pd_slab().move_to([x, B61_SLAB_Y, 0]) for x in B61_GX]
        self.play(*[FadeIn(s, shift=UP * 0.6) for s in slabs], run_time=0.6)
        until(self, "they all-reduce", lead=0.1)
        self.play(*[s.animate.move_to(B61_MERGE) for s in slabs], run_time=0.8)
        merged = pd_slab(1.4, 0.45, BAR2).move_to(B61_MERGE)
        self.play(FadeOut(VGroup(*slabs)), GrowFromCenter(merged), run_time=0.4)
        until(self, "each applies the same update", lead=0.3)
        copies = [pd_slab(1.1, 0.36, BAR2).move_to(B61_MERGE) for _ in B61_GX]
        self.add(*copies)
        self.play(*[c.animate.move_to([x, B61_SLAB_Y, 0]) for c, x in zip(copies, B61_GX)], FadeOut(merged), run_time=0.8)
        until(self, "Inside one node", lead=0.2)
        bracket = VGroup(Line([-5.2, 2.2, 0], [1.2, 2.2, 0], color=INK, stroke_width=4),
                         Line([-5.2, 2.2, 0], [-5.2, 1.9, 0], color=INK, stroke_width=4),
                         Line([1.2, 2.2, 0], [1.2, 1.9, 0], color=INK, stroke_width=4))
        self.play(Create(bracket), run_time=0.5)
        self.play(FadeIn(T("one node · NVLink", 34).move_to([-2.0, 2.75, 0])), run_time=0.3)
        until(self, "Across nodes", lead=0.2)
        far_b, far_l = b61_gpu(4.7)
        link = DashedLine([1.3, -1.5, 0], [3.75, -1.5, 0], color=INK, stroke_width=4, dash_length=0.18)
        self.play(FadeIn(VGroup(far_b, far_l), shift=DOWN * 0.4), Create(link), run_time=0.6)
        self.play(FadeIn(T("across nodes", 34).move_to([4.7, 0.3, 0])), FadeIn(T("slower", 34).move_to([4.7, -0.25, 0])), run_time=0.3)
        until(self, "single-node multi-GPU", lead=0.2)
        self.play(Indicate(VGroup(*[l for b, l in gpus]), color=TERRA, scale_factor=1.6), run_time=0.7)
        done(self)


# ─────────────── B63 · scaling efficiency: measured bars under the ideal, three bands, back to one card ───────────────
B63_BASE = -1.6
B63_UNIT = 0.62
B63_BX = {1: -4.5, 2: -3.0, 4: -1.5}
B63_MEAS = {1: 1.0, 2: 0.9, 4: 0.77}          # measured height as a share of ideal (shape only: no number is shown)
B63_BAND_X = 3.3


def b63_bar(n):
    h = n * B63_UNIT * B63_MEAS[n]
    return Rectangle(width=1.0, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B63_BX[n], B63_BASE + h / 2, 0])


def b63_ideal(n):
    y = B63_BASE + n * B63_UNIT
    return DashedLine([B63_BX[n] - 0.65, y, 0], [B63_BX[n] + 0.65, y, 0], color=INK, stroke_width=4, dash_length=0.14)


def b63_gap(n):
    x = B63_BX[n] + 0.8
    return Line([x, B63_BASE + n * B63_UNIT * B63_MEAS[n], 0], [x, B63_BASE + n * B63_UNIT, 0], color=INK, stroke_width=5)


def b63_band(y, fill):
    return Rectangle(width=2.2, height=0.7, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([B63_BAND_X, y, 0])


class B63_ScalingEfficiency(Scene):
    def construct(self):
        self.add(Line([-5.3, B63_BASE, 0], [-0.7, B63_BASE, 0], color=INK, stroke_width=4),
                 *[T(str(n), 40).move_to([B63_BX[n], -1.95, 0]) for n in (1, 2, 4)],
                 T("GPUs", 34).move_to([-0.2, -1.95, 0]))
        bars = [b63_bar(n) for n in (1, 2, 4)]
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), run_time=1.0)
        self.play(Create(b63_ideal(2)), Create(b63_ideal(4)), run_time=0.5)
        self.play(FadeIn(T("ideal", 34).move_to([-0.1, B63_BASE + 4 * B63_UNIT, 0])), run_time=0.3)
        until(self, "Throughput divided", lead=0.2)
        self.play(FadeIn(T("efficiency", 34).move_to([1.4, 2.3, 0])), FadeIn(T("=", 34).move_to([2.55, 2.3, 0])),
                  FadeIn(T("throughput", 34).move_to([4.2, 2.85, 0])), run_time=0.4)
        self.play(Create(Line([3.0, 2.3, 0], [5.4, 2.3, 0], color=INK, stroke_width=4)), run_time=0.3)
        self.play(FadeIn(T("n × baseline", 34).move_to([4.2, 1.75, 0])), run_time=0.3)
        until(self, "gives efficiency", lead=0.1)
        self.play(Create(b63_gap(2)), Create(b63_gap(4)), run_time=0.4)
        until(self, "Above eighty percent", lead=0.2)
        self.play(GrowFromEdge(b63_band(0.5, BAR3), LEFT), FadeIn(T("> 80%", 34).move_to([5.35, 0.5, 0])), run_time=0.5)
        self.play(Create(check(1.7, 0.5, 0.2)), run_time=0.3)
        until(self, "Seventy to eighty", lead=0.2)
        self.play(GrowFromEdge(b63_band(-0.4, BAR2), LEFT), FadeIn(T("70–80%", 34).move_to([5.35, -0.4, 0])), run_time=0.5)
        until(self, "Below seventy", lead=0.2)
        self.play(GrowFromEdge(b63_band(-1.3, BAR1), LEFT), FadeIn(T("< 70%", 34).move_to([5.35, -1.3, 0])), run_time=0.5)
        self.play(GrowFromCenter(Dot([1.7, -1.3, 0], radius=0.17, color=TERRA)), run_time=0.3)
        until(self, "more GPUs won't help", lead=0.2)
        strike = VGroup(Line([-2.0, -0.4, 0], [-1.0, 0.6, 0], color=INK, stroke_width=8),
                        Line([-2.0, 0.6, 0], [-1.0, -0.4, 0], color=INK, stroke_width=8))
        self.play(Create(strike), run_time=0.4)
        until(self, "Go back", lead=0.4)
        back = VGroup(Line([1.7, -1.55, 0], [1.7, -2.75, 0], color=INK, stroke_width=5),
                      Line([1.7, -2.75, 0], [-4.5, -2.75, 0], color=INK, stroke_width=5),
                      Arrow([-4.5, -2.75, 0], [-4.5, -2.3, 0], color=INK, stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.5))
        self.play(Create(back), run_time=0.8)
        self.play(GrowFromCenter(Circle(radius=0.3, color=TERRA, stroke_width=6).move_to([-4.5, -1.95, 0])), run_time=0.3)
        done(self)


# ─────────────── B70 · the loop: seven steps round a ring, one fix at a time, exit above eighty ───────────────
B70_C = np.array([-2.2, -0.2, 0.0])
B70_R = 1.8
B70_STEP = 360.0 / 7
B70_A0 = -B70_STEP                    # baseline sits lower-right; the ring runs clockwise; repeat lands at 0° (right)
B70_NAMES = ("baseline", "profile", "diagnose", "fix one", "re-profile", "record", "repeat")
B70_LABEL_AT = {"baseline": (-0.58, -2.23), "profile": (-2.78, -2.73), "diagnose": (-4.75, -1.4), "fix one": (-4.75, 1.0),
                "re-profile": (-2.78, 2.33), "record": (-0.5, 1.9), "repeat": (0.55, 0.45)}


def b70_ang(k):
    return B70_A0 - B70_STEP * k


def b70_pt(deg, r=B70_R):
    a = deg * PI / 180
    return B70_C + r * np.array([np.cos(a), np.sin(a), 0.0])


def b70_arc(k0, k1):
    """Clockwise arc from step k0 to step k1 along the ring."""
    a0, a1 = b70_ang(k0), b70_ang(k1)
    return Arc(radius=B70_R, start_angle=a0 * PI / 180, angle=(a1 - a0) * PI / 180, arc_center=B70_C)


def b70_node(k):
    return Dot(b70_pt(b70_ang(k)), radius=0.14, color=INK)


def b70_label(k):
    x, y = B70_LABEL_AT[B70_NAMES[k]]
    return T(B70_NAMES[k], 34).move_to([x, y, 0])


def b70_card(x, y):
    return RoundedRectangle(width=0.9, height=0.55, corner_radius=0.1, fill_color=BOX_TOP, fill_opacity=1,
                            stroke_color=INK, stroke_width=3).move_to([x, y, 0])


class B70_TheLoop(Scene):
    def construct(self):
        self.add(T("VII · The Loop", 40).move_to([-4.7, 3.0, 0]))
        ring = Circle(radius=B70_R, color=BAR1, stroke_width=4).move_to(B70_C)
        self.play(Create(ring), run_time=0.9)
        nodes = [b70_node(k) for k in range(7)]
        labels = [b70_label(k) for k in range(7)]
        self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(n), FadeIn(l)) for n, l in zip(nodes, labels)], lag_ratio=0.3), run_time=2.4)
        until(self, "Baseline:", lead=0.2)
        mark = Dot(b70_pt(b70_ang(0)), radius=0.19, color=TERRA).set_z_index(4)
        self.play(GrowFromCenter(mark), run_time=0.3)
        until(self, "Profile twenty", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(0, 1)), run_time=0.6)
        until(self, "Diagnose:", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(1, 2)), run_time=0.6)
        until(self, "Fix one thing", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(2, 3)), run_time=0.6)
        until(self, "Only one", lead=0.1)
        card = b70_card(-6.0, 0.3)
        self.add(card)
        self.play(card.animate.shift(RIGHT * 1.5), run_time=0.45, rate_func=ease_in)                     # a second fix arrives ...
        self.play(card.animate.shift(LEFT * 1.1), run_time=0.35, rate_func=rate_functions.ease_out_bounce)  # ... and is pushed out
        self.play(FadeOut(card, shift=LEFT * 0.6), run_time=0.3)
        until(self, "Re-profile:", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(3, 4)), run_time=0.6)
        until(self, "Record the gain", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(4, 5)), run_time=0.5)
        until(self, "Repeat until", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(5, 6)), run_time=0.5)
        until(self, "above eighty", lead=0.2)
        exit_arrow = Arrow([-0.15, -0.2, 0], [1.75, -0.2, 0], color=INK, stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.18)
        self.play(GrowArrow(exit_arrow), run_time=0.4)
        self.play(FadeIn(T("> 80%", 56).move_to([3.3, -0.2, 0]), shift=RIGHT * 0.2), run_time=0.3)
        until(self, "or the returns run out", lead=0.2)
        self.play(MoveAlongPath(mark, b70_arc(6, 7)), run_time=0.7)
        done(self)


# ─────────────── B71 · the decision tree: utilization at the root, memory leaves, multi-GPU, the OOM order ───────────────
B71_Y = (2.9, 1.6, 0.3, -1.0, -1.7, -2.3)


def b71_edge(xf, yf, xt, yt):
    """An ink branch from the label at (xf, yf) down to the label at (xt, yt), 0.3 clear of both."""
    return Line([xf, yf - 0.45, 0], [xt, yt + 0.45, 0], color=INK, stroke_width=4)


def b71_lab(s, x, y, size=32):
    return T(s, size).move_to([x, y, 0])


class B71_DecisionTree(Scene):
    def construct(self):
        y0, y1, y2, y3, y4, y5 = B71_Y
        root = b71_lab("utilization?", -1.3, y0)
        self.play(FadeIn(root, shift=DOWN * 0.2), run_time=0.4)
        until(self, "Utilization under fifty?", lead=0.1)
        self.play(Create(b71_edge(-1.3, y0, -5.0, y1)), run_time=0.4)
        self.play(FadeIn(b71_lab("< 50%", -5.0, y1)), run_time=0.3)
        until(self, "the data pipeline", lead=0.2)
        self.play(Create(b71_edge(-5.0, y1, -5.0, y2)), FadeIn(b71_lab("data pipeline", -5.0, y2)), run_time=0.4)
        until(self, "workers is zero", lead=0.2)
        self.play(FadeIn(b71_lab("workers = 0", -5.0, -0.4)), run_time=0.3)
        self.play(FadeIn(b71_lab("first", -5.0, y3)), run_time=0.3)
        until(self, "Fifty to eighty?", lead=0.2)
        self.play(Create(b71_edge(-1.3, y0, -1.3, y1)), FadeIn(b71_lab("50–80%", -1.3, y1)), run_time=0.4)
        until(self, "Look at memory", lead=0.1)
        self.play(Create(b71_edge(-1.3, y1, -1.3, y2)), FadeIn(b71_lab("memory?", -1.3, y2)), run_time=0.4)
        leaves = ((-3.6, "< 40%", "batch ↑", "Under forty percent"), (-2.0, "40–85%", "BF16", "Forty to eighty-five"),
                  (-0.45, "> 90%", "batch ↓", "Over ninety"), (1.15, "OK", "profile", "Memory fine?"))
        for x, cond, act, cue in leaves:
            until(self, cue, lead=0.2)
            self.play(Create(b71_edge(-1.3, y2, x, y3)), FadeIn(b71_lab(cond, x, y3)), run_time=0.35)
            self.play(FadeIn(b71_lab(act, x, y4), shift=DOWN * 0.15), run_time=0.3)
            if cond == "> 90%":
                self.play(FadeIn(b71_lab("checkpoint", x, y5), shift=DOWN * 0.15), run_time=0.3)
        until(self, "Above eighty with healthy memory?", lead=0.2)
        self.play(Create(b71_edge(-1.3, y0, 2.9, y1)), FadeIn(b71_lab("> 80%", 2.9, y1)), run_time=0.4)
        self.play(Create(b71_edge(2.9, y1, 2.9, y2)), FadeIn(b71_lab("multi-GPU?", 2.9, y2)), run_time=0.4)
        until(self, "only if the single card", lead=0.2)
        self.play(Create(b71_edge(2.9, y2, 2.9, y3)), FadeIn(b71_lab("if saturated", 2.9, y3)), run_time=0.4)
        until(self, "And out of memory", lead=0.1)
        self.play(FadeIn(b71_lab("OOM", 5.25, y1), shift=DOWN * 0.2), run_time=0.3)
        oom = (("BF16", 0.9, "BF16, then"), ("checkpoint", 0.2, "then checkpointing"), ("batch ↓", -0.5, "then a smaller batch"))
        for s, y, cue in oom:
            until(self, cue, lead=0.1)
            self.play(FadeIn(b71_lab(s, 5.25, y), shift=DOWN * 0.15), run_time=0.3)
        until(self, "In that order", lead=0.1)
        order = Arrow([4.15, 1.15, 0], [4.15, -0.75, 0], color=INK, stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.14)
        self.play(GrowArrow(order), run_time=0.5)
        done(self)


# ─────────────── B72 · the real jobstats report, re-composed on cream: command, header rows, four bars ───────────────
B72_X0 = -3.1            # bars start here
B72_FULL = 4.6           # 100 % of a bar
B72_ROWS = (("CPU", 13, 0.1), ("CPU memory", 25, -0.6), ("GPU", 80, -1.3), ("GPU memory", 17, -2.0))


def b72_row_label(name, y):
    return M(name, 32).move_to([-4.7, y, 0])


def b72_bar(pct, y):
    return pd_hbar(B72_X0, y, B72_FULL * pct / 100.0)


def b72_pct(pct, y):
    return M(f"{pct}%", 32).move_to([B72_X0 + B72_FULL * pct / 100.0 + 0.65, y, 0])


def b72_ring(pct, y):
    return Circle(radius=0.5, color=TERRA, stroke_width=6).move_to([B72_X0 + B72_FULL * pct / 100.0 + 0.65, y, 0])


class B72_Jobstats(Scene):
    def construct(self):
        self.play(FadeIn(M("$ jobstats 318592", 32).move_to([-3.8, 2.05, 0])), run_time=0.4)
        until(self, "runs on AICR", lead=0.3)
        header = VGroup(M("Job Name", 32).move_to([-4.9, 1.45, 0]), M("f5tune-voice", 32).move_to([-1.9, 1.45, 0]),
                        M("rtx-batch", 32).move_to([1.6, 1.45, 0]), M("GPUs 1", 32).move_to([4.2, 1.45, 0]),
                        M("Run Time", 32).move_to([-4.9, 0.9, 0]), M("00:55:09", 32).move_to([-1.9, 0.9, 0]),
                        M("Time Limit", 32).move_to([1.6, 0.9, 0]), M("08:00:00", 32).move_to([4.2, 0.9, 0]))
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(VGroup(*[b72_row_label(n, y) for n, p, y in B72_ROWS]), shift=RIGHT * 0.15), run_time=0.4)
        until(self, "Here is a real one", lead=0.1)
        self.play(Create(Line([B72_X0, 0.45, 0], [B72_X0, -2.35, 0], color=INK, stroke_width=4)), run_time=0.4)
        until(self, "fifty-five-minute", lead=0.1)
        self.play(Indicate(header[5], color=INK, scale_factor=1.15), run_time=0.6)      # 00:55:09
        until(self, "on an RTX card", lead=0.1)
        self.play(Indicate(header[2], color=INK, scale_factor=1.15), run_time=0.6)      # rtx-batch
        until(self, "GPU utilization eighty percent", lead=0.2)
        self.play(GrowFromEdge(b72_bar(80, -1.3), LEFT), run_time=0.7)
        self.play(FadeIn(b72_pct(80, -1.3)), run_time=0.2)
        ring = b72_ring(80, -1.3)
        self.play(GrowFromCenter(ring), run_time=0.3)
        until(self, "GPU memory seventeen percent", lead=0.2)
        self.play(GrowFromEdge(b72_bar(17, -2.0), LEFT), run_time=0.5)
        self.play(FadeIn(b72_pct(17, -2.0)), run_time=0.2)
        self.play(ring.animate.move_to([B72_X0 + B72_FULL * 0.17 + 0.65, -2.0, 0]), run_time=0.4)
        until(self, "CPU utilization thirteen percent", lead=0.2)
        self.play(GrowFromEdge(b72_bar(13, 0.1), LEFT), GrowFromEdge(b72_bar(25, -0.6), LEFT), run_time=0.5)
        self.play(FadeIn(b72_pct(13, 0.1)), FadeIn(b72_pct(25, -0.6)), run_time=0.2)
        until(self, "the job needed eleven percent", lead=0.2)
        self.play(FadeOut(ring), FadeIn(M("needed 11% of the requested time", 32).move_to([0.0, -2.8, 0]), shift=UP * 0.15), run_time=0.4)
        until(self, "under sixty percent GPU", lead=0.2)
        self.play(GrowFromCenter(b72_ring(80, -1.3)), run_time=0.3)
        done(self)


# ─────────────── B73 · the pre-submission checklist ticks, then the devel job leaves its slot ───────────────
B73_ROW_Y = (2.4, 1.65, 0.9, 0.15, -0.6)
B73_ITEMS = (("verify", T, "The verify script passes"), ("util > 70%", T, "shows over seventy percent"),
             ("workers ≠ 0", T, "Workers is not zero"), ("pin_memory", M, "Pin memory is on"),
             ("batch ≥ 60% VRAM", T, "at least sixty percent of VRAM"), ("BF16", T, "BF16 autocast is on"),
             ("partition", T, "names the right partition"), ("cpus = workers+1", T, "CPUs per task"),
             ("logs/", M, "The logs folder exists"), ("profiled 20", T, "profiled twenty steps"))
B73_SLOTS = ((4.3, -1.2), (5.4, -1.2), (4.3, -2.6), (5.4, -2.6))     # (ox, oy) of four job slots, iso scale 0.75


def b73_box(x, y):
    return Square(side_length=0.4, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y, 0])


def b73_tick(x, y):
    return check(x, y - 0.02, 0.17, INK, 6)


def b73_job(ox, oy):
    return job_box(Iso(ox, oy, 0.75)).set_z_index(2)


class B73_Checklist(Scene):
    def construct(self):
        boxes, labels = [], []
        for i, (s, f, cue) in enumerate(B73_ITEMS):
            x = -5.7 if i < 5 else -0.7
            y = B73_ROW_Y[i % 5]
            bx = b73_box(x, y)
            lb = f(s, 32).next_to(bx, RIGHT, buff=0.35)
            boxes.append(bx)
            labels.append(lb)
        slots = [pd_slot(ox, oy, 0.75) for ox, oy in B73_SLOTS]
        jobs = [b73_job(ox, oy) for ox, oy in B73_SLOTS]
        self.add(*boxes, *labels, *slots, *jobs, T("devel", 34).move_to([4.3, 0.3, 0]))
        for i, (s, f, cue) in enumerate(B73_ITEMS):
            until(self, cue, lead=0.1)
            x = -5.7 if i < 5 else -0.7
            self.play(Create(b73_tick(x, B73_ROW_Y[i % 5])), run_time=0.3)
        until(self, "Then cancel the devel session", lead=0.2)
        self.play(FadeOut(jobs[0], shift=UP * 0.8), run_time=0.6)
        until(self, "four running jobs", lead=0.2)
        self.play(FadeIn(T("4 running jobs", 32).move_to([4.8, 2.4, 0]), shift=DOWN * 0.15), run_time=0.4)
        until(self, "an idle one blocks", lead=0.2)
        self.play(Indicate(slots[0], color=TERRA, scale_factor=1.15), run_time=0.6)
        done(self)
