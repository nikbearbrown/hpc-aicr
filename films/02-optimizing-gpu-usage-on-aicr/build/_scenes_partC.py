# ═════════════════════════════ PART C · B44 · Act V (B50 B51 B52 B54 B55) · B60 ═════════════════════════════
# Gauges are the recurring picture of this part: a half-dial (0 at the left, 100 at the right, upper half) for the
# big meters, and a small round dial with a dark-kraft ring for icons (GATE T: small ink rings fuse with their pointer).
PC_SMALL = "#917A55"                         # dark kraft: outlines of SMALL objects only
PC_KRAFT = "#9C8462"                         # deep kraft: cables and connectors (ink cables fuse what they join)
PC_GTOP, PC_GL, PC_GR = "#A8A29B", "#9A938C", "#918A83"   # a block that has gone BF16 grey (all above GATE T's grey-120 floor)


def pc_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pc_left(mob, x, y):
    """Left-align a label at x (fixed numbers: Gate A's stub measures text differently)."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pc_ang(frac):
    return PI * (1.0 - frac)


def pc_pt(c, r, frac):
    a = pc_ang(frac)
    return np.array([c[0] + r * np.cos(a), c[1] + r * np.sin(a), 0.0])


def pc_gauge(c, r, sw=6, ticks=(0.0, 0.25, 0.5, 0.75, 1.0)):
    """A big half-dial: open ink arc from 0 (left) to 100 (right), tick marks, a pivot."""
    arc = Arc(radius=r, start_angle=PI, angle=-PI, arc_center=np.array([c[0], c[1], 0.0]), color=INK, stroke_width=sw)
    tk = VGroup(*[Line(pc_pt(c, r - 0.16, f), pc_pt(c, r + 0.16, f), color=INK, stroke_width=sw - 1) for f in ticks])
    pivot = Dot(np.array([c[0], c[1], 0.0]), radius=0.11, color=INK)
    return VGroup(arc, tk, pivot)


def pc_needle(c, r, frac, sw=8):
    return Line(np.array([c[0], c[1], 0.0]), pc_pt(c, r * 0.82, frac), color=INK, stroke_width=sw).set_z_index(3)


def pc_turn(needle, c, f0, f1):
    """The animation that swings a needle from reading f0 to reading f1."""
    return Rotate(needle, angle=-(f1 - f0) * PI, about_point=np.array([c[0], c[1], 0.0]))


def pc_dial(c, r=0.3, frac=0.15, sw=3):
    """A small round dial: white face, dark-kraft ring, ink needle (index 1), ink pin."""
    face = Circle(radius=r, stroke_color=PC_SMALL, stroke_width=sw, fill_color=PAGE_TOP, fill_opacity=1).move_to(np.array([c[0], c[1], 0.0]))
    needle = Line(np.array([c[0], c[1], 0.0]), pc_pt(c, r * 0.72, frac), color=INK, stroke_width=4)
    pin = Dot(np.array([c[0], c[1], 0.0]), radius=0.045, color=INK)
    return VGroup(face, needle, pin)


def pc_cross(x, y, s=0.2, w=7):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


# ─────────────── B44 · four dials land with their start values; num_workers 0 → 4 lifts utilization 20% → 60–80% ───────────────
B44_Y = (2.1, 0.8, -0.5, -1.8)
B44_NAMES = ("num_workers", "pin_memory", "persistent_workers", "prefetch_factor")
B44_VALS = ("cpus-1", "True", "True", "2")
B44_FRAC = (0.0, 0.9, 0.9, 0.3)                       # dial readings; num_workers starts at the PyTorch default, zero
B44_DX = -5.3                                          # dial centres
B44_BAR_X, B44_BAR_W, B44_BAR_Y0, B44_BAR_H = 3.9, 0.8, -2.6, 4.9


def b44_row(k):
    y = B44_Y[k]
    dial = pc_dial((B44_DX, y), r=0.5, frac=B44_FRAC[k], sw=4)
    name = pc_left(M(B44_NAMES[k], 32), -4.5, y)
    val = pc_left(M(B44_VALS[k], 36), 0.5, y)
    return VGroup(dial, name, val)


def b44_fill(frac):
    h = B44_BAR_H * frac - 0.16
    return Rectangle(width=B44_BAR_W - 0.16, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B44_BAR_X, B44_BAR_Y0 + 0.08 + h / 2, 0])


def b44_pct(s, frac):
    return T(s, 36).move_to([5.25, B44_BAR_Y0 + B44_BAR_H * frac - 0.08, 0])


class B44_FourKnobs(Scene):
    def construct(self):
        rows = [b44_row(k) for k in range(4)]
        until(self, "Workers")
        self.play(FadeIn(rows[0], shift=DOWN * 0.5), run_time=0.45)
        until(self, "Pin memory")
        self.play(FadeIn(rows[1], shift=DOWN * 0.5), run_time=0.45)
        until(self, "Persistent workers")
        self.play(FadeIn(rows[2], shift=DOWN * 0.5), run_time=0.45)
        until(self, "Prefetch")
        self.play(FadeIn(rows[3], shift=DOWN * 0.5), run_time=0.45)
        until(self, "The single biggest win")
        bar = Rectangle(width=B44_BAR_W, height=B44_BAR_H, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([B44_BAR_X, B44_BAR_Y0 + B44_BAR_H / 2, 0])
        fill = b44_fill(0.2)
        lab = M("num_workers=0", 32).move_to([B44_BAR_X, -3.0, 0])
        self.play(Create(bar), run_time=0.5)
        self.play(GrowFromEdge(fill, DOWN), FadeIn(lab), FadeIn(b44_pct("20%", 0.2)), run_time=0.5)
        self.add(T("utilization", 36).move_to([B44_BAR_X, 2.65, 0]))
        until(self, "from zero")
        needle = rows[0][0][1]
        self.play(pc_turn(needle, (B44_DX, B44_Y[0]), 0.0, 0.4), run_time=0.6)
        until(self, "to four or more")
        lab4 = M("num_workers=4", 32).move_to([B44_BAR_X, -3.0, 0])
        self.play(FadeOut(lab), FadeIn(lab4), run_time=0.3)
        until(self, "That alone often takes a job")
        self.play(Transform(fill, b44_fill(0.7)), run_time=0.9)
        self.play(FadeIn(b44_pct("60–80%", 0.7)), run_time=0.3)
        done(self)


# ─────────────── B50 · two meters that mean different things: utilization sweeps to 100 (fine); memory climbs to the OOM edge ───────────────
B50_L, B50_R, B50_RAD = (-3.1, -0.4), (3.1, -0.4), 2.0


def b50_ends(c):
    return VGroup(T("0", 32).move_to([c[0] - B50_RAD - 0.35, -0.85, 0]), T("100%", 32).move_to([c[0] + B50_RAD + 0.35, -0.85, 0]))


class B50_TwoMeters(Scene):
    def construct(self):
        self.add(pc_title("V · Memory vs Utilization"))
        gl, gr = pc_gauge(B50_L, B50_RAD), pc_gauge(B50_R, B50_RAD)
        self.play(Create(gl), Create(gr), run_time=0.8)
        self.add(b50_ends(B50_L), b50_ends(B50_R))
        until(self, "Utilization")
        nl = pc_needle(B50_L, B50_RAD, 0.05, sw=10).set_color(BAR1)   # grey: GATE T read an ink needle along the arc base as a second text run
        self.play(FadeIn(T("utilization", 44).move_to([-3.1, -1.5, 0])), FadeIn(nl), run_time=0.4)
        until(self, "the share of the last second")
        self.play(pc_turn(nl, B50_L, 0.05, 0.55), run_time=0.7)
        until(self, "Low means idle")
        self.play(pc_turn(nl, B50_L, 0.55, 0.12), run_time=0.5)
        until(self, "A hundred percent sustained")
        self.play(pc_turn(nl, B50_L, 0.12, 1.0), run_time=0.9)
        self.play(Create(check(-3.1, 0.55, 0.3, TERRA, 9)), run_time=0.35)
        until(self, "Memory")
        nr = pc_needle(B50_R, B50_RAD, 0.05, sw=10).set_color(BAR1)
        self.play(FadeIn(T("memory", 44).move_to([3.1, -1.5, 0])), FadeIn(nr), run_time=0.4)
        until(self, "the share of VRAM")
        self.play(pc_turn(nr, B50_R, 0.05, 0.45), pc_turn(nl, B50_L, 1.0, 0.9), run_time=0.7)      # independent needles
        until(self, "Low means you could hold")
        self.play(pc_turn(nr, B50_R, 0.45, 0.2), run_time=0.5)
        until(self, "High is only bad near the edge")
        self.play(pc_turn(nr, B50_R, 0.2, 0.97), pc_turn(nl, B50_L, 0.9, 1.0), run_time=0.9)
        until(self, "runs out of memory")
        oom = Dot(pc_pt(B50_R, B50_RAD + 0.32, 1.0), radius=0.15, color=TERRA)
        self.play(GrowFromCenter(oom), run_time=0.3)
        self.add(T("OOM", 36).move_to([5.5, 0.25, 0]))
        done(self)


# ─────────────── B51 · read the pair: five rows, gauge icons for what you see, a cause, a first thing to try ───────────────
B51_Y = (1.5, 0.55, -0.4, -1.35, -2.3)
B51_HY = 2.85
B51_UX, B51_MX = -5.25, -4.45                           # the two icon columns (utilization, memory)
B51_C2, B51_C3 = -3.1, 1.9                              # left edges of the word columns
B51_LO, B51_HI = 0.15, 0.85
B51_ROWS = [((B51_LO, B51_LO), "GPU doing nothing", "verify CUDA"),
            ((B51_LO, B51_HI), "loaded, not running", "fix the pipeline"),
            ((B51_HI, B51_LO), "healthy, VRAM unused", "increase batch size"),
            ((B51_HI, B51_HI), "good shape", None),
            ((B51_LO, 1.02), "out of memory", "mixed precision")]


def b51_rule(y, color=BAR1, sw=3):
    return Line([-6.0, y, 0], [6.0, y, 0], color=color, stroke_width=sw)


def b51_row(k):
    (fu, fm), cause, fix = B51_ROWS[k]
    y = B51_Y[k]
    icons = VGroup(pc_dial((B51_UX, y), 0.3, fu), pc_dial((B51_MX, y), 0.3, fm))
    if k == 4:
        icons.add(Dot([B51_MX + 0.46, y, 0], radius=0.09, color=TERRA))      # the OOM edge, as in B50
    words = VGroup(pc_left(T(cause, 36), B51_C2, y))
    if fix is None:
        words.add(check(B51_C3 + 0.3, y, 0.2, INK, 6))
    else:
        words.add(pc_left(T(fix, 36), B51_C3, y))
    return icons, words


class B51_DecisionTable(Scene):
    def construct(self):
        head = VGroup(T("what you see", 36, bold=True).move_to([-4.8, B51_HY, 0]),
                      pc_left(T("likely cause", 36, bold=True), B51_C2, B51_HY),
                      pc_left(T("first thing to try", 36, bold=True), B51_C3, B51_HY),
                      T("util", 32).move_to([B51_UX, 2.25, 0]), T("mem", 32).move_to([B51_MX, 2.25, 0]))
        rules = VGroup(b51_rule(1.95, INK, 5), *[b51_rule(B51_Y[k] - 0.475) for k in range(4)], b51_rule(-2.775, INK, 5))
        self.add(head, rules)
        mark = Dot([-5.8, B51_Y[0], 0], radius=0.1, color=TERRA)
        until(self, "Low and low")
        ic, wd = b51_row(0)
        self.play(GrowFromCenter(ic), FadeIn(wd, shift=RIGHT * 0.3), GrowFromCenter(mark), run_time=0.5)
        until(self, "Low utilization, high memory")
        ic, wd = b51_row(1)
        self.play(GrowFromCenter(ic), FadeIn(wd, shift=RIGHT * 0.3), mark.animate.shift(DOWN * 0.95), run_time=0.5)
        until(self, "High utilization, low memory")
        ic, wd = b51_row(2)
        self.play(GrowFromCenter(ic), FadeIn(wd, shift=RIGHT * 0.3), mark.animate.shift(DOWN * 0.95), run_time=0.5)
        until(self, "High and high")
        ic, wd = b51_row(3)
        self.play(GrowFromCenter(ic), FadeIn(wd, shift=RIGHT * 0.3), mark.animate.shift(DOWN * 0.95), run_time=0.5)
        until(self, "And an out-of-memory crash")
        ic, wd = b51_row(4)
        self.play(GrowFromCenter(ic), FadeIn(wd, shift=RIGHT * 0.3), mark.animate.shift(DOWN * 0.95), run_time=0.5)
        done(self)


# ─────────────── B52 · batch size moves both axes; binary-search the ceiling; run production at 70–85% of it ───────────────
B52_BAR_Y, B52_AX_Y = 1.8, -1.3
B52_X0, B52_X1 = -5.0, 5.0


def b52_x(batch):
    return B52_X0 + (B52_X1 - B52_X0) * batch / 4096.0


def b52_fill(frac):
    w = (B52_X1 - B52_X0 - 0.16) * min(frac, 1.0)
    return Rectangle(width=w, height=0.64, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B52_X0 + 0.08 + w / 2, B52_BAR_Y, 0])


def b52_hop(mark, b0, b1):
    return MoveAlongPath(mark, ArcBetweenPoints(np.array([b52_x(b0), B52_AX_Y, 0.0]), np.array([b52_x(b1), B52_AX_Y, 0.0]), angle=-PI / 2))


def b52_num(batch):
    return M(str(batch), 32).move_to([b52_x(batch), -1.85, 0])


class B52_BinarySearch(Scene):
    def construct(self):
        bar = Rectangle(width=B52_X1 - B52_X0, height=0.8, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([0, B52_BAR_Y, 0])
        fill = b52_fill(0.175)
        axis = Line([B52_X0, B52_AX_Y, 0], [B52_X1, B52_AX_Y, 0], color=INK, stroke_width=4)
        mark = Dot([b52_x(512), B52_AX_Y, 0], radius=0.15, color=INK).set_z_index(3)
        self.add(bar, fill, axis, mark, pc_left(T("VRAM", 36), -5.0, 2.55), T("batch size", 36).move_to([4.3, -2.5, 0]),
                 T("1", 32).move_to([B52_X0, -1.85, 0]), M("4096", 32).move_to([B52_X1, -1.85, 0]))
        until(self, "Batch size moves both axes")
        self.play(b52_hop(mark, 512, 1024), Transform(fill, b52_fill(0.35)), run_time=0.8)
        until(self, "as long as the GPU")
        self.play(b52_hop(mark, 1024, 512), Transform(fill, b52_fill(0.175)), run_time=0.8)
        until(self, "On a B200")
        self.play(FadeIn(M("B200", 36).move_to([0, 2.55, 0])), run_time=0.3)
        until(self, "one hundred ninety-two gigabytes")
        self.play(FadeIn(T("192 GB", 36).move_to([4.3, 2.55, 0])), run_time=0.3)
        until(self, "fifteen or twenty percent")
        pct = T("15–20%", 36).move_to([-3.3, 1.05, 0])
        self.play(FadeIn(pct, shift=UP * 0.2), run_time=0.35)
        until(self, "four to eight times the batch")
        room = T("4–8×", 40).move_to([1.0, 1.05, 0])
        self.play(FadeIn(room, shift=UP * 0.2), run_time=0.35)
        until(self, "try a size")
        self.play(FadeOut(pct), FadeOut(room), b52_hop(mark, 512, 2048), Transform(fill, b52_fill(0.7)), run_time=0.8)
        until(self, "see if it fits")
        self.play(Create(check(b52_x(2048), -0.75, 0.2, INK, 6)), FadeIn(b52_num(2048)), run_time=0.35)
        until(self, "halve the gap")
        oom = Dot([B52_X1, B52_BAR_Y, 0], radius=0.15, color=TERRA).set_z_index(3)
        self.play(b52_hop(mark, 2048, 3072), Transform(fill, b52_fill(1.0)), run_time=0.7)
        self.play(GrowFromCenter(oom), Create(pc_cross(b52_x(3072), -0.75, 0.18, 6)), FadeIn(b52_num(3072)), run_time=0.35)
        until(self, "repeat")
        self.play(b52_hop(mark, 3072, 2560), Transform(fill, b52_fill(0.875)), FadeOut(oom), run_time=0.7)
        self.play(Create(check(b52_x(2560), -0.75, 0.2, INK, 6)), FadeIn(b52_num(2560)), run_time=0.35)
        self.play(FadeIn(T("ceiling", 36).move_to([b52_x(2560), -0.15, 0]), shift=DOWN * 0.2), run_time=0.3)
        until(self, "seventy to eighty-five percent")
        band = Rectangle(width=b52_x(2560 * 0.85) - b52_x(2560 * 0.70), height=0.5, fill_color=BAR2, fill_opacity=1, stroke_width=0)
        band.move_to([(b52_x(2560 * 0.85) + b52_x(2560 * 0.70)) / 2, B52_AX_Y, 0]).set_z_index(1)
        self.play(GrowFromCenter(band), run_time=0.5)
        self.play(FadeIn(T("production · 70–85%", 36).move_to([-0.6, -2.5, 0]), shift=UP * 0.2), run_time=0.35)
        done(self)


# ─────────────── B54 · the bit ladder: FP32 8|23, BF16 8|7, FP16 5|10, FP8 4|3 ───────────────
B54_FMT = (("FP32", 8, 23), ("BF16", 8, 7), ("FP16", 5, 10), ("FP8", 4, 3))
B54_Y = (2.0, 0.75, -0.5, -1.75)
B54_X0, B54_U, B54_CW, B54_H, B54_SPLIT = -3.9, 0.28, 0.25, 0.5, 0.1


def b54_cells(n, x0, y, fill):
    return VGroup(*[Rectangle(width=B54_CW, height=B54_H, fill_color=fill, fill_opacity=1, stroke_width=0)
                    .move_to([x0 + i * B54_U + B54_CW / 2, y, 0]) for i in range(n)])


def b54_row(k):
    """(label, exponent cells, mantissa cells, exponent count, mantissa count) for format k."""
    name, e, m = B54_FMT[k]
    y = B54_Y[k]
    xe, xm = B54_X0, B54_X0 + e * B54_U + B54_SPLIT
    lab = M(name, 36).move_to([-5.0, y, 0])
    ec, mc = b54_cells(e, xe, y, BAR1), b54_cells(m, xm, y, BAR2)
    en = T(str(e), 34).move_to([xe + (e * B54_U - 0.03) / 2, y + 0.5, 0])
    mn = T(str(m), 34).move_to([xm + (m * B54_U - 0.03) / 2, y + 0.5, 0])
    return lab, ec, mc, en, mn


def b54_end(k):
    name, e, m = B54_FMT[k]
    return B54_X0 + e * B54_U + B54_SPLIT + m * B54_U


def b54_grow(self, cells, rt):
    self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.08), run_time=rt)


class B54_BitLadder(Scene):
    def construct(self):
        r32, r16b, r16, r8 = [b54_row(k) for k in range(4)]
        self.add(r32[0], r16b[0], r16[0], r8[0])
        until(self, "exponent, which is range")
        self.play(FadeIn(T("exponent", 36).move_to([-2.8, 3.0, 0]), shift=DOWN * 0.2), run_time=0.35)
        until(self, "mantissa, which is precision")
        self.play(FadeIn(T("mantissa", 36).move_to([1.6, 3.0, 0]), shift=DOWN * 0.2), run_time=0.35)
        until(self, "FP32 has eight exponent bits")
        b54_grow(self, r32[1], 0.5)
        self.add(r32[3])
        until(self, "twenty-three of mantissa")
        b54_grow(self, r32[2], 0.8)
        self.add(r32[4])
        until(self, "BF16 keeps the same eight")
        b54_grow(self, r16b[1], 0.5)
        self.add(r16b[3])
        self.play(Indicate(VGroup(r32[1], r16b[1]), color=None, scale_factor=1.06), run_time=0.5)   # the same eight, aligned
        until(self, "keeps only seven for precision")
        b54_grow(self, r16b[2], 0.5)
        self.add(r16b[4])
        until(self, "so gradients don't underflow")
        self.play(Create(check(b54_end(1) + 0.55, B54_Y[1], 0.22, TERRA, 8)), run_time=0.35)
        until(self, "FP16 bets the other way")
        self.play(Indicate(r16[0], color=None, scale_factor=1.1), run_time=0.35)
        until(self, "ten bits of precision")
        b54_grow(self, r16[2], 0.6)
        self.add(r16[4])
        until(self, "but only five of exponent")
        b54_grow(self, r16[1], 0.4)
        self.add(r16[3])
        until(self, "which underflows")
        self.play(FadeIn(T("underflow", 36).move_to([b54_end(2) + 1.15, B54_Y[2], 0]), shift=LEFT * 0.2),
                  Indicate(r16[1], color=None, scale_factor=1.08), run_time=0.45)
        until(self, "FP8 goes further still")
        b54_grow(self, r8[1], 0.35)
        b54_grow(self, r8[2], 0.3)
        self.add(r8[3], r8[4])
        until(self, "Every step down")
        arrow = Arrow([5.5, 2.1, 0], [5.5, -2.0, 0], color=INK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.08)
        self.play(Create(arrow), run_time=0.6)
        self.add(T("quality", 34).move_to([5.5, 2.45, 0]))
        until(self, "for speed and memory")
        self.play(FadeIn(T("speed, memory", 34).move_to([4.6, -2.5, 0]), shift=UP * 0.2), run_time=0.35)
        done(self)


# ─────────────── B55 · what BF16 buys: activations halve, matmuls 2–4×, four risky blocks stay FP32 ───────────────
B55_X = tuple(-5.4 + k * 1.55 for k in range(8))       # activations ×2, matmul ×2, weights, loss, softmax, norm
B55_OY, B55_S = -1.0, 0.65
B55_FP32 = ("weights", "loss", "softmax", "norm")


def b55_block(k, h=1.4, grey=False):
    iso = Iso(B55_X[k], B55_OY, B55_S)
    if grey:
        return iso.box(0, 0, 0, 1.1, 1.0, h, PC_GTOP, PC_GL, PC_GR).set_stroke(DIM, width=3)
    return iso.box(0, 0, 0, 1.1, 1.0, h, DARK_TOP, DARK_L, DARK_R)


def b55_spark(k):
    return Dot(Iso(B55_X[k], B55_OY, B55_S).p(0.55, 0.5, 1.4), radius=0.11, color=TERRA).set_z_index(3)


class B55_MixedSafetyNet(Scene):
    def construct(self):
        blocks = [b55_block(k) for k in range(8)]
        self.add(*blocks, T("activations", 36).move_to([-4.625, -1.45, 0]), T("matmul", 36).move_to([-1.525, -1.45, 0]))
        until(self, "Activation memory roughly halves")
        self.play(Transform(blocks[0], b55_block(0, 0.7)), Transform(blocks[1], b55_block(1, 0.7)), run_time=0.8)
        until(self, "so a much bigger batch fits")
        self.play(*[FadeIn(T("½", 44).move_to([B55_X[k], 0.75, 0]), shift=DOWN * 0.3) for k in (0, 1)], run_time=0.4)
        until(self, "Matrix operations run two to four times faster")
        sparks = VGroup(b55_spark(2), b55_spark(3))
        self.play(GrowFromCenter(sparks), run_time=0.35)
        self.play(*[FadeIn(T("2–4×", 40).move_to([B55_X[k], 1.05, 0]), shift=DOWN * 0.3) for k in (2, 3)], run_time=0.4)
        until(self, "the risky parts stay in thirty-two bit")
        self.play(*[Transform(blocks[k], b55_block(k, 0.7 if k < 2 else 1.4, grey=True)) for k in range(4)], run_time=0.8)
        self.play(FadeIn(M("BF16", 36).move_to([-3.075, -2.3, 0])), FadeIn(M("FP32", 36).move_to([3.125, -2.3, 0])), run_time=0.35)
        for k, phrase in enumerate(("Master weights", "the loss", "softmax", "normalization")):
            until(self, phrase)
            self.play(FadeIn(T(B55_FP32[k], 34).move_to([B55_X[4 + k], -1.45, 0]), shift=UP * 0.2),
                      Indicate(blocks[4 + k], color=None, scale_factor=1.06), run_time=0.4)
        until(self, "Autocast handles that")
        self.play(FadeIn(M("autocast", 36).move_to([0.0, 2.4, 0]), shift=DOWN * 0.2), run_time=0.35)
        until(self, "largest for matrix multiplies")
        self.play(Indicate(sparks, color=None, scale_factor=1.7), run_time=0.6)
        done(self)


# ─────────────── B60 · the eighty percent rule: > 80% split the work four ways; < 60% four starved GPUs; I/O-bound compete for files ───────────────
B60_C, B60_R = (-4.0, 0.5), 1.1
B60_GX = (-0.9, 0.9, 2.7, 4.5)
B60_ONE = Iso(-4.0, -2.0, 0.8)
B60_CAB = Iso(1.75, 0.75, 0.45)


def b60_small(x, frac):
    return pc_dial((x, -0.3), 0.45, frac, sw=3)


class B60_EightyRule(Scene):
    def construct(self):
        self.add(pc_title("VI · More Than One GPU"))
        gauge = pc_gauge(B60_C, B60_R, sw=5, ticks=(0.0, 0.6, 0.8, 1.0))
        needle = pc_needle(B60_C, B60_R, 0.3, sw=9).set_color(BAR1)   # grey: GATE T read the ink needle inside the arc bbox as an overlapping text run
        body, light = gpu_block(B60_ONE)
        light.scale(1.5).set_color(TERRA)
        job = job_box(B60_ONE, 0.15, 0.15, 0.5).set_z_index(2)
        self.add(gauge, needle, body, light, job, T("60%", 32).move_to([-4.7, 2.05, 0]), T("80%", 32).move_to([-2.3, 1.7, 0]),
                 T("one GPU", 36).move_to([-4.0, -2.55, 0]))
        until(self, "Multi-GPU is the first thing")
        four = VGroup()
        lights, dials = VGroup(), VGroup()
        for x in B60_GX:
            b, l = gpu_block(Iso(x, -2.0, 0.65))
            l.scale(1.5)
            four.add(b); lights.add(l); dials.add(b60_small(x, 0.0))
        four.add(lights, dials, T("four GPUs", 36).move_to([1.8, -2.55, 0]))
        four.shift(RIGHT * 9)
        self.add(four)
        self.play(four.animate.shift(LEFT * 9), run_time=0.8)
        until(self, "More GPUs amplify")
        self.play(pc_turn(needle, B60_C, 0.3, 0.5), run_time=0.5)
        until(self, "already above eighty percent")
        self.play(pc_turn(needle, B60_C, 0.5, 0.88), run_time=0.7)
        until(self, "adding cards divides the work")
        jobs = VGroup(*[job_box(Iso(x, -2.0, 0.65), 0.2, 0.2, 0.5, s=0.5).set_z_index(2) for x in B60_GX])
        self.play(FadeIn(jobs, shift=DOWN * 0.6), lights.animate.set_color(TERRA),
                  *[pc_turn(dials[i][1], (B60_GX[i], -0.3), 0.0, 0.88) for i in range(4)], run_time=0.7)
        ok = check(3.3, -2.55, 0.22, INK, 7)
        self.play(Create(ok), run_time=0.3)
        until(self, "If it's below sixty")
        self.play(pc_turn(needle, B60_C, 0.88, 0.4), run_time=0.6)
        until(self, "four starved GPUs waste four times")
        idle = VGroup(*[Dot([x + 0.2, -0.3 + 0.2, 0], radius=0.075, color=TERRA).set_z_index(3) for x in B60_GX])
        self.play(*[pc_turn(dials[i][1], (B60_GX[i], -0.3), 0.88, 0.4) for i in range(4)], lights.animate.set_color(GHOST), FadeOut(ok), run_time=0.6)
        self.play(GrowFromCenter(idle), FadeIn(T("×4", 44).move_to([5.65, -0.3, 0])), run_time=0.4)
        until(self, "And an I/O-bound job gets worse")
        cab = project_cabinet(B60_CAB).set_z_index(2)
        self.play(FadeIn(cab, shift=DOWN * 0.4), run_time=0.5)
        until(self, "compete for the same files")
        wires = VGroup(*[Line([x, 0.22, 0], [1.75, 0.62, 0], color=PC_KRAFT, stroke_width=5) for x in B60_GX]).set_z_index(1)
        self.play(Create(wires), run_time=0.6)
        self.play(FadeIn(T("same files", 36).move_to([3.7, 1.5, 0]), shift=LEFT * 0.2), run_time=0.35)
        done(self)
