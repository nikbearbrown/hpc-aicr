
# ═════════════════════════════ PART B · B40 B41 (Act IV) · B53 B55 (Act V) · B73 (Act VII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB_ / pb_ / b4x_ / b5x_ / b7x_ so the parts never collide.
# Charts: axes in BAR1, curves in INK (labels placed clear of them), dashed ideals in INK,
# terracotta only as dots and rings. Every number on screen is in the beat's narration or visual_intent.

PB_SMALL = "#917A55"      # dark kraft: outlines of SMALL objects only


def pb_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb_axes(x0, y0, x1, y1):
    """Plain chart axes in dim grey (ink curves sit on them without fusing)."""
    return VGroup(Line([x0, y0, 0], [x1 + 0.15, y0, 0], color=BAR1, stroke_width=4),
                  Line([x0, y0, 0], [x0, y1 + 0.15, 0], color=BAR1, stroke_width=4))


def pb_dashed(p0, p1):
    return DashedLine([p0[0], p0[1], 0], [p1[0], p1[1], 0], color=INK, stroke_width=4, dash_length=0.14)


def pb_curve(pts, color=INK, sw=7):
    c = VMobject(color=color, stroke_width=sw)
    c.set_points_smoothly([np.array([p[0], p[1], 0.0]) for p in pts])
    return c


def pb_vbracket(x, y0, y1, tick=0.15):
    """A vertical bracket at x spanning y0..y1, ticks pointing left."""
    return VGroup(Line([x, y0, 0], [x, y1, 0], color=INK, stroke_width=4),
                  Line([x, y0, 0], [x - tick, y0, 0], color=INK, stroke_width=4),
                  Line([x, y1, 0], [x - tick, y1, 0], color=INK, stroke_width=4))


def pb_hbracket(x0, x1, y, tick=0.2):
    """A horizontal bracket above two bars, ticks pointing down."""
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=INK, stroke_width=4),
                  Line([x0, y, 0], [x0, y - tick, 0], color=INK, stroke_width=4),
                  Line([x1, y, 0], [x1, y - tick, 0], color=INK, stroke_width=4))


# ─────────────── B40 / B41 shared chart frame: processors N (1…64) along x ───────────────
B4_X0, B4_X1, B4_Y0 = -5.5, 0.7, -2.5
B4_SX = (B4_X1 - B4_X0) / 64.0


def b4_x(n):
    return B4_X0 + n * B4_SX


def b4_amdahl(n, s=0.1):
    return 1.0 / (s + (1.0 - s) / n)


def b4_gustafson(n, s=0.1):
    return s + (1.0 - s) * n


# ─────────────── B40 · Amdahl: the formula, the S = 0.1 curve bending toward a ceiling at 10× ───────────────
B40_SY = 0.38                                   # speedup axis 0…12
B40_STRIP_X0, B40_STRIP_Y = 2.75, -0.6


def b40_y(s):
    return B4_Y0 + s * B40_SY


def b40_seg(k, fill):
    return Rectangle(width=0.24, height=0.45, fill_color=fill, fill_opacity=1, stroke_width=0).move_to(
        [B40_STRIP_X0 + 0.12 + k * 0.27, B40_STRIP_Y, 0])


class B40_Amdahl(Scene):
    def construct(self):
        procs = T("processors N", 34).move_to([-2.4, -2.9, 0])
        self.add(pb_title("IV · The Speed Limit"), pb_axes(B4_X0, B4_Y0, B4_X1, b40_y(12)),
                 T("1", 32).move_to([b4_x(1), -2.85, 0]), T("64", 32).move_to([b4_x(64), -2.85, 0]),
                 procs, T("speedup", 34).move_to([-5.0, 2.45, 0]))
        ideal = pb_dashed((b4_x(1), b40_y(1)), (b4_x(12), b40_y(12)))
        self.play(Create(ideal), FadeIn(T("ideal", 34).move_to([-3.6, 1.95, 0])), run_time=0.6)
        # not everything parallelises: ten segments, one of them serial
        until(self, "Not everything parallelises", lead=0.1)
        segs = [b40_seg(k, BAR2) for k in range(10)]
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in segs], lag_ratio=0.08), run_time=0.7)
        until(self, "reading data", lead=0.2)
        serial = b40_seg(0, INK)
        self.play(FadeIn(serial), FadeIn(T("serial", 32).move_to([2.87, -1.15, 0])),
                  FadeIn(T("parallel", 32).move_to([4.4, -1.15, 0])), run_time=0.4)
        # the law
        until(self, "Amdahl's law", lead=0.2)
        formula = MathTex(r"\text{Speedup} = \frac{1}{S + \frac{P}{N}}", font_size=56, color=INK).move_to([3.5, 2.2, 0])
        self.play(FadeIn(formula, shift=DOWN * 0.15), run_time=0.6)
        until(self, "where S is the serial", lead=0.2)
        self.play(Indicate(serial, color=None, scale_factor=1.25), run_time=0.5)
        until(self, "P the parallel", lead=0.2)
        self.play(FadeIn(MathTex(r"P = 1 - S", font_size=60, color=INK).move_to([4.1, 0.4, 0])),
                  Indicate(VGroup(*segs[1:]), color=None, scale_factor=1.08), run_time=0.5)
        until(self, "and N the number", lead=0.2)
        self.play(Indicate(procs, color=None, scale_factor=1.08), run_time=0.5)
        # S = 0.1: the curve climbs, then flattens toward 10
        until(self, "If ten percent", lead=0.1)
        curve = pb_curve([(b4_x(n), b40_y(b4_amdahl(n))) for n in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64)])
        self.play(Create(curve), run_time=1.5)
        self.play(FadeIn(T("S = 0.1", 34).move_to([-0.6, 0.0, 0])), run_time=0.3)
        until(self, "the most you can ever get", lead=0.2)
        ceiling = pb_dashed((B4_X0, b40_y(10)), (B4_X1, b40_y(10)))
        self.play(Create(ceiling), run_time=0.6)
        self.play(FadeIn(T("10× at most", 34).move_to([1.95, b40_y(10), 0])), run_time=0.3)
        until(self, "however many processors", lead=0.2)
        self.play(GrowFromCenter(Dot([b4_x(64), b40_y(b4_amdahl(64)), 0], radius=0.12, color=TERRA).set_z_index(3)), run_time=0.3)
        until(self, "The curve climbs", lead=0.2)
        rider = Dot([b4_x(1), b40_y(1), 0], radius=0.12, color=TERRA).set_z_index(3)
        self.add(rider)
        self.play(MoveAlongPath(rider, curve), run_time=1.4)
        self.play(FadeOut(rider), run_time=0.2)
        until(self, "This is strong scaling", lead=0.2)
        self.play(FadeIn(T("strong scaling", 34).move_to([-1.6, -1.5, 0]), shift=UP * 0.15), run_time=0.4)
        done(self)


# ─────────────── B41 · Gustafson: the problem grows with the cores; a near-straight line beside the flattening curve ───────────────
B41_SY = 4.4 / 64.0                             # speedup axis 0…64
B41_CLOCK = np.array([2.9, 1.3, 0.0])
B41_BLOCK = np.array([4.1, -0.5, 0.0])


def b41_y(s):
    return B4_Y0 + s * B41_SY


def b41_clock():
    face = Circle(radius=0.5, color=INK, stroke_width=5).move_to(B41_CLOCK)
    hands = VGroup(Line(B41_CLOCK, B41_CLOCK + np.array([0.0, 0.34, 0.0]), color=BAR1, stroke_width=5),
                   Line(B41_CLOCK, B41_CLOCK + np.array([0.24, 0.0, 0.0]), color=BAR1, stroke_width=5))
    return VGroup(face, hands)


def b41_page():
    slab = Rectangle(width=1.5, height=1.9, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.2, -0.3, 0])
    lines = VGroup(*[Line([2.6, y, 0], [3.8, y, 0], color=GHOST, stroke_width=4) for y in (0.3, -0.1, -0.5, -0.9)])
    return VGroup(slab, lines)


class B41_Gustafson(Scene):
    def construct(self):
        self.add(pb_axes(B4_X0, B4_Y0, B4_X1, b41_y(64)),
                 T("1", 32).move_to([b4_x(1), -2.85, 0]), T("64", 32).move_to([b4_x(64), -2.85, 0]),
                 T("processors N", 34).move_to([-2.4, -2.9, 0]), T("speedup", 34).move_to([-5.0, 2.45, 0]))
        amdahl = pb_curve([(b4_x(n), b41_y(b4_amdahl(n))) for n in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64)], BAR1, 6)
        ideal = pb_dashed((b4_x(1), b41_y(1)), (b4_x(64), b41_y(64)))
        self.play(Create(amdahl), Create(ideal), run_time=0.7)
        self.play(FadeIn(T("Amdahl", 34).move_to([-0.1, -1.4, 0])), FadeIn(T("ideal", 34).move_to([-0.6, 2.2, 0])), run_time=0.3)
        # the other question: a block of work, a clock that holds at ten minutes
        until(self, "A researcher", lead=0.2)
        block = Square(side_length=0.35, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(B41_BLOCK)
        self.play(GrowFromCenter(block), run_time=0.4)
        until(self, "ten-minute problem", lead=0.3)
        clock = b41_clock()
        tenmin = T("10 min", 34).move_to([4.3, 1.3, 0])
        self.play(Create(clock), FadeIn(tenmin), run_time=0.5)
        until(self, "They solve a problem", lead=0.2)
        self.play(block.animate.scale(4.57), run_time=1.2)
        cores = T("100 cores", 34).move_to([4.1, -1.75, 0])
        bigger = T("100× the problem", 34).move_to([4.1, -2.25, 0])
        self.play(FadeIn(cores), FadeIn(bigger), run_time=0.4)
        until(self, "in the same ten minutes", lead=0.2)
        pin = Dot(B41_CLOCK, radius=0.08, color=TERRA).set_z_index(3)
        self.play(GrowFromCenter(pin), Indicate(tenmin, color=None, scale_factor=1.1), run_time=0.5)
        # the law and its line
        until(self, "Speedup equals S plus P times N", lead=0.2)
        formula = MathTex(r"\text{Speedup} = S + P \cdot N", font_size=56, color=INK).move_to([3.4, 2.7, 0])
        self.play(FadeIn(formula, shift=DOWN * 0.15), run_time=0.5)
        line = Line([b4_x(1), b41_y(b4_gustafson(1)), 0], [b4_x(64), b41_y(b4_gustafson(64)), 0], color=INK, stroke_width=7)
        self.play(Create(line), run_time=1.2)
        self.play(GrowFromCenter(Dot([b4_x(64), b41_y(b4_gustafson(64)), 0], radius=0.12, color=TERRA).set_z_index(3)), run_time=0.3)
        until(self, "That is weak scaling", lead=0.2)
        self.play(FadeIn(T("weak scaling", 34).move_to([-2.4, 1.5, 0]), shift=UP * 0.15), run_time=0.4)
        until(self, "Both laws are right", lead=0.2)
        self.play(Indicate(VGroup(amdahl, line), color=None, scale_factor=1.02), run_time=0.6)
        # plan first: the page replaces the clock and the block
        until(self, "One tip before any code", lead=0.2)
        page = b41_page()
        self.play(FadeOut(VGroup(clock, tenmin, pin, block, cores, bigger)), FadeIn(page, shift=UP * 0.2), run_time=0.6)
        until(self, "plan what can be parallel", lead=0.2)
        self.play(Create(check(4.5, -0.1, 0.24)), run_time=0.4)
        self.play(FadeIn(T("plan what can be parallel", 32).move_to([3.9, -1.75, 0])), run_time=0.3)
        until(self, "Retrofitting", lead=0.2)
        self.play(Indicate(page, color=None, scale_factor=1.04), run_time=0.5)
        done(self)


# ─────────────── B53 · halo exchange: one grid into four strips on four node plinths, boundary rows swap ───────────────
B53_CELL = 0.26
B53_COLS, B53_ROWS = 14, 12
B53_GX, B53_GY = -2.4, 0.0                      # grid centre
B53_W = B53_COLS * B53_CELL                     # 3.64
B53_STRIP_Y = (2.61, 0.87, -0.87, -2.61)         # strip centres after the split
B53_GHOST = 0.64                                # ghost row offset from its strip centre


def b53_cell_xy(c, r):
    return (B53_GX - B53_W / 2 + B53_CELL / 2 + c * B53_CELL, B53_GY + B53_ROWS * B53_CELL / 2 - B53_CELL / 2 - r * B53_CELL)


def b53_cell(c, r, fill=BAR2):
    x, y = b53_cell_xy(c, r)
    return Square(side_length=B53_CELL, fill_color=fill, fill_opacity=1, stroke_color=CARD, stroke_width=1.5).move_to([x, y, 0])


def b53_row(r, fill=BAR2):
    return VGroup(*[b53_cell(c, r, fill) for c in range(B53_COLS)])


def b53_plinth(k):
    return Rectangle(width=B53_W + 0.3, height=3 * B53_CELL + 0.18, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to(
        [B53_GX, B53_STRIP_Y[k], 0]).set_z_index(-1)


def b53_ghost_outline(y):
    return DashedVMobject(Rectangle(width=B53_W, height=B53_CELL).move_to([B53_GX, y, 0]), num_dashes=44).set_stroke(INK, 3)


class B53_HaloExchange(Scene):
    def construct(self):
        strips = [VGroup(*[b53_row(r) for r in range(3 * k, 3 * k + 3)]) for k in range(4)]
        self.play(FadeIn(VGroup(*strips)), run_time=0.6)
        until(self, "domain decomposition", lead=0.2)
        self.play(FadeIn(T("domain decomposition", 34).move_to([3.8, 3.0, 0]), shift=DOWN * 0.15), run_time=0.4)
        # the cut: four strips slide apart onto four node plinths
        until(self, "The grid is cut", lead=0.2)
        shifts = [B53_STRIP_Y[k] - (1.17 - 0.78 * k) for k in range(4)]
        self.play(*[s.animate.shift(UP * dy) for s, dy in zip(strips, shifts)], run_time=1.0)
        plinths = [b53_plinth(k) for k in range(4)]
        self.play(*[FadeIn(p) for p in plinths], run_time=0.4)
        until(self, "one per MPI rank", lead=0.2)
        self.play(*[FadeIn(T(f"rank {k}", 34).move_to([0.6, B53_STRIP_Y[k], 0])) for k in range(4)], run_time=0.4)
        # the edge needs the neighbour: boundary rows light up, two cells across a gap
        until(self, "But a cell on the edge", lead=0.2)
        edges = [strips[k][i] for k in range(4) for i in (0, 2)]
        self.play(*[e.animate.set_fill(CARD) for e in edges], run_time=0.5)
        until(self, "needs neighbours", lead=0.1)
        x6, _ = b53_cell_xy(6, 0)
        self.play(GrowFromCenter(Dot([x6, B53_STRIP_Y[1] + B53_CELL, 0], radius=0.09, color=TERRA).set_z_index(3)),
                  GrowFromCenter(Dot([x6, B53_STRIP_Y[0] - B53_CELL, 0], radius=0.09, color=TERRA).set_z_index(3)), run_time=0.3)
        # the swap: copies of the boundary rows cross the gaps and land as ghost rows
        until(self, "the ranks swap", lead=0.3)
        copies, moves, outlines = [], [], []
        for k in range(3):
            down = strips[k][2].copy().set_fill(BAR2).set_z_index(1)          # strip k's bottom row -> above strip k+1
            up = strips[k + 1][0].copy().set_fill(BAR2).set_z_index(1)        # strip k+1's top row -> below strip k
            y_down, y_up = B53_STRIP_Y[k + 1] + B53_GHOST, B53_STRIP_Y[k] - B53_GHOST
            copies += [down, up]
            moves += [down.animate.move_to([B53_GX, y_down, 0]), up.animate.move_to([B53_GX, y_up, 0])]
            outlines += [b53_ghost_outline(y_down), b53_ghost_outline(y_up)]
        self.add(*copies)
        self.play(*moves, run_time=0.9)
        self.play(*[Create(o) for o in outlines], run_time=0.4)
        until(self, "MPI send and receive", lead=0.3)
        self.play(FadeIn(M("MPI_Send / MPI_Recv", 32).move_to([3.6, 0.0, 0]), shift=UP * 0.15), run_time=0.4)
        until(self, "Those borrowed rows are the halo", lead=0.2)
        self.play(FadeIn(T("halo", 34).move_to([0.55, B53_STRIP_Y[0] - B53_GHOST, 0])),
                  Indicate(VGroup(*copies), color=None, scale_factor=1.03), run_time=0.6)
        done(self)


# ─────────────── B55 · the real numbers: ten points, grey OpenMP and dark MPI, under a dashed ideal ───────────────
B55_X0, B55_X1, B55_Y0 = -5.3, 0.9, -2.5
B55_SX = (B55_X1 - B55_X0) / np.sqrt(80.0)       # both axes stretched by sqrt so 1…20 stays readable; the ideal stays a diagonal
B55_SY = 4.6 / np.sqrt(80.0)
B55_DATA = ((1, 1.0, "250.7 s", "1 core"), (2, 2.2, "116.8 s", "2 cores"), (4, 4.3, "58.1 s", "4 cores"), (8, 8.5, "29.4 s", "8 cores"),
            (12, 7.5, "33.4 s", "12 cores"), (16, 10.0, "25.2 s", "16 cores"), (20, 12.4, "20.2 s", "20 cores"),
            (40, 25.1, "10.0 s", "40 cores"), (60, 36.9, "6.8 s", "60 cores"), (80, 44.0, "5.7 s", "80 cores"))
B55_CUES = ("Serial:", "OpenMP on two cores", "Four cores", "Eight,", "Twelve,", "Sixteen,", "Twenty,", "forty cores", "Sixty,", "Eighty,")
B55_COL_X = 4.7


def b55_x(c):
    return B55_X0 + B55_SX * np.sqrt(c)


def b55_y(s):
    return B55_Y0 + B55_SY * np.sqrt(s)


def b55_pt(i):
    c, s = B55_DATA[i][0], B55_DATA[i][1]
    return np.array([b55_x(c), b55_y(s), 0.0])


def b55_column(i):
    """The wall-time column: cores, the measured time, the speedup."""
    c, s, wall, cores = B55_DATA[i]
    return VGroup(T(cores, 34).move_to([B55_COL_X, 1.9, 0]), M(wall, 44).move_to([B55_COL_X, 1.1, 0]),
                  T(f"{s:.1f}×", 40).move_to([B55_COL_X, 0.2, 0]))


class B55_Benchmark(Scene):
    def construct(self):
        self.add(pb_axes(B55_X0, B55_Y0, B55_X1, b55_y(80)),
                 T("1", 32).move_to([b55_x(1), -2.85, 0]), T("20", 32).move_to([b55_x(20), -2.85, 0]),
                 T("40", 32).move_to([b55_x(40), -2.85, 0]), T("80", 32).move_to([b55_x(80), -2.85, 0]),
                 T("cores", 34).move_to([-3.5, -2.9, 0]), T("speedup", 34).move_to([-4.8, 2.5, 0]),
                 T("10×", 32).move_to([-5.75, b55_y(10), 0]), T("80×", 32).move_to([-5.75, b55_y(80), 0]))
        ideal = pb_dashed((b55_x(1), b55_y(1)), (b55_x(80), b55_y(80)))
        self.play(Create(ideal), FadeIn(T("ideal", 34).move_to([-0.9, 1.6, 0])), run_time=0.6)
        until(self, "five hundred iterations", lead=0.2)
        self.play(FadeIn(T("500 iterations", 32).move_to([-4.3, 2.95, 0])), run_time=0.3)
        legend = VGroup(Dot([3.7, -1.2, 0], radius=0.11, color=BAR1), T("OpenMP", 34).move_to([4.75, -1.2, 0]))
        dots, col = [], None
        for i, cue in enumerate(B55_CUES):
            until(self, cue, lead=0.15)
            p = b55_pt(i)
            dot = Dot(p, radius=0.11, color=BAR1 if i < 7 else INK).set_z_index(3)
            dots.append(dot)
            anims = [GrowFromCenter(dot)]
            if i > 0:
                anims.append(Create(Line(b55_pt(i - 1), p, color=INK, stroke_width=5)))
            newcol = b55_column(i)
            if col is not None:
                anims.append(FadeOut(col))
            anims.append(FadeIn(newcol))
            if i == 0:
                anims.append(FadeIn(legend))
            if i == 7:
                anims.append(FadeIn(VGroup(Dot([3.7, -1.8, 0], radius=0.11, color=INK), T("MPI", 34).move_to([4.45, -1.8, 0]))))
            self.play(*anims, run_time=0.35)
            col = newcol
            if i == 4:
                until(self, "slower than eight", lead=0.2)
                self.play(GrowFromCenter(Circle(radius=0.24, color=TERRA, stroke_width=5).move_to(p)), run_time=0.3)
        until(self, "Inside one node", lead=0.2)
        self.play(Indicate(VGroup(*dots[:7]), color=None, scale_factor=1.15), run_time=0.6)
        until(self, "Across nodes the communication", lead=0.2)
        self.play(Indicate(VGroup(*dots[7:]), color=None, scale_factor=1.15), run_time=0.6)
        until(self, "bends under the ideal line", lead=0.3)
        self.play(Create(pb_vbracket(1.3, b55_y(44.0) + 0.04, b55_y(80) - 0.04)), run_time=0.5)
        self.play(FadeIn(T("communication", 34).move_to([2.65, 2.4, 0])), run_time=0.3)
        until(self, "exactly as Amdahl", lead=0.2)
        self.play(GrowFromCenter(Dot(b55_pt(9), radius=0.13, color=TERRA).set_z_index(4)), run_time=0.3)
        done(self)


# ─────────────── B73 · the GPU benchmark: three bars, three wall times, sync beats maths across nodes ───────────────
B73_BASE = -1.9
B73_BX = (-4.05, -1.15, 1.75)
B73_SEC = 0.29                                  # bar height per second
B73_TIMES = (11.73, 5.48, 5.08)
B73_WALL = ("11.73 s", "5.48 s", "5.08 s")
B73_SPEED = ("1.0×", "2.1×", "2.3×")
B73_UNDER = (("1 GPU",), ("2 GPUs", "1 node"), ("4 GPUs", "2 nodes"))
B73_PIVOT = np.array([3.9, -0.3, 0.0])
B73_PAN_L, B73_PAN_R, B73_PAN_Y = 3.1, 4.7, -0.95


def b73_bar(i):
    h = B73_TIMES[i] * B73_SEC
    return Rectangle(width=1.2, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B73_BX[i], B73_BASE + h / 2, 0])


def b73_top(i):
    return B73_BASE + B73_TIMES[i] * B73_SEC


def b73_under(i):
    return VGroup(*[T(s, 32).move_to([B73_BX[i], -2.3 - 0.45 * j, 0]) for j, s in enumerate(B73_UNDER[i])])


def b73_scale():
    """A small balance: ink beam on an ink fulcrum, grey strings, ink pans, one grey weight on each pan."""
    fulcrum = Polygon([B73_PIVOT[0] - 0.25, -0.9, 0], [B73_PIVOT[0] + 0.25, -0.9, 0], [B73_PIVOT[0], -0.37, 0],
                      fill_color=INK, fill_opacity=1, stroke_width=0)
    beam = Line([B73_PAN_L, B73_PIVOT[1], 0], [B73_PAN_R, B73_PIVOT[1], 0], color=INK, stroke_width=5)
    strings = VGroup(*[Line([x, B73_PIVOT[1], 0], [x, B73_PAN_Y, 0], color=BAR1, stroke_width=4) for x in (B73_PAN_L, B73_PAN_R)])
    pans = VGroup(*[Line([x - 0.3, B73_PAN_Y, 0], [x + 0.3, B73_PAN_Y, 0], color=INK, stroke_width=5) for x in (B73_PAN_L, B73_PAN_R)])
    w_l = Square(side_length=0.28, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B73_PAN_L, B73_PAN_Y + 0.17, 0])
    w_r = Square(side_length=0.28, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B73_PAN_R, B73_PAN_Y + 0.17, 0])
    return fulcrum, VGroup(beam, strings, pans, w_l), w_r


class B73_GpuBench(Scene):
    def construct(self):
        fulcrum, arm, w_r = b73_scale()
        self.play(Create(Line([-4.9, B73_BASE, 0], [2.6, B73_BASE, 0], color=BAR1, stroke_width=4)),
                  FadeIn(VGroup(fulcrum, arm, w_r)), run_time=0.6)
        self.play(FadeIn(T("compute", 32).move_to([B73_PAN_L, -1.45, 0])), FadeIn(T("communication", 32).move_to([B73_PAN_R, -1.9, 0])), run_time=0.3)
        until(self, "a four-thousand-square matmul", lead=0.2)
        self.play(FadeIn(T("4000 × 4000 · 100 times", 32).move_to([-3.0, 2.95, 0]), shift=DOWN * 0.15), run_time=0.4)
        bars, walls, speeds = [], [], []
        for i, (cue_bar, cue_wall, cue_speed) in enumerate((("One GPU", "eleven point seven", None),
                                                             ("Two GPUs on one node", "five and a half seconds", "two point one times"),
                                                             ("Four GPUs across two nodes", "five point one seconds", "only two point three"))):
            until(self, cue_bar, lead=0.2)
            bars.append(b73_bar(i))
            self.play(GrowFromEdge(bars[i], DOWN), FadeIn(b73_under(i)), run_time=0.6)
            until(self, cue_wall, lead=0.15)
            walls.append(M(B73_WALL[i], 36).move_to([B73_BX[i], b73_top(i) + 0.33, 0]))
            speeds.append(T(B73_SPEED[i], 36).move_to([B73_BX[i], b73_top(i) + 0.78, 0]))
            if cue_speed is None:
                self.play(FadeIn(walls[i]), FadeIn(speeds[i]), run_time=0.3)
            else:
                self.play(FadeIn(walls[i]), run_time=0.3)
                until(self, cue_speed, lead=0.15)
                self.play(FadeIn(speeds[i]), run_time=0.3)
            if i == 1:
                until(self, "near linear", lead=0.2)
                self.play(Indicate(speeds[1], color=None, scale_factor=1.2), run_time=0.5)
        # tiny shards, then sync beats maths: the bracket and the tilt
        until(self, "each GPU gets a tiny shard", lead=0.2)
        shards = VGroup(*[Square(side_length=0.2, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([1.35 + 0.27 * j, 0.72, 0]) for j in range(4)])
        self.play(LaggedStart(*[GrowFromCenter(s) for s in shards], lag_ratio=0.2), run_time=0.5)
        until(self, "sync costs more than the maths", lead=0.3)
        self.play(Create(pb_hbracket(B73_BX[1], B73_BX[2], 1.3)), run_time=0.5)
        self.play(FadeIn(T("sync > maths", 34).move_to([0.3, 1.75, 0])), run_time=0.3)
        self.play(w_r.animate.scale(1.6).shift(UP * 0.08), run_time=0.4)
        self.play(Rotate(VGroup(arm, w_r), angle=-10 * DEGREES, about_point=B73_PIVOT), run_time=0.7)
        until(self, "ratio decides", lead=0.2)
        self.play(Indicate(VGroup(arm, w_r, fulcrum), color=None, scale_factor=1.04), run_time=0.6)
        done(self)
