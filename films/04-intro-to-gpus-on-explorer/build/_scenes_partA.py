# ═════════════════════════════ PART A · Act I (B10) and Act II (B20, B21) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PA_ / b10_ / b20_ / b21_ so the parts never collide.
#
# Stage map. Act I opens on the drawn partition table (film 2's B11 / film 3's B62 grammar: mono partition
# names, a heavy ink header rule, grey row rules, grey hour bars). Act II opens on two flat blocks side by
# side, a grey CPU and a dark GPU, each lifting its lid to show its cores (B20); B21 is the isometric city
# (kraft houses on a thin dark plinth) with the few dark carriers and the terracotta swarm, and the matrix
# grid on the right that fills all at once.
PA_KRAFT = "#9C8462"                        # deep-kraft connector (lines are never ink: ink lines fuse the things they join)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T: small ink rings fuse)
PA_PAD = "#E4E0D4"                          # pads and boards stay within 28 of the stage (Gate V does not count them as ink)


def pa_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_at(mob, x_left, y):
    """Place a text by its LEFT edge."""
    return mob.move_to([x_left + mob.width / 2, y, 0])


# ─────────────── B10 · the six GPU partitions: a drawn table with an hours bar per row ───────────────
B10_ROWS = [("gpu", 8, "8 h"), ("gpu-interactive", 2, "2 h"), ("gpu-short", 2, "2 h"),
            ("multigpu", 24, "24 h"), ("courses-gpu", 24, "24 h"), ("sharing", 1, "1 h")]
B10_X = (-6.0, -1.75, 0.95)                                          # left edge of each column (partition, max time, hours)
B10_BAR_X0, B10_BAR_UNIT = 0.95, 4.9 / 24                            # bar start, screen units per hour (24 h = 4.9, ends 5.85)
B10_Y0, B10_DY = 1.45, 0.72                                          # first row centre, row pitch
B10_HEAD_Y = B10_Y0 + B10_DY + 0.02
B10_L, B10_R = -6.0, 6.0
B10_TAG_X = 1.75                                                     # tags sit after the short bars (2 h ends 1.36, 1 h ends 1.15)


def b10_at(mob, col, y):
    return mob.move_to([B10_X[col] + mob.width / 2, y, 0])


def b10_cell(fn, s, size, col, y):
    """A table cell set on a common baseline: typeset with a trailing 'bp' (one ascender, one descender) so every
    cell has the same vertical extent, then the two extra glyphs are dropped."""
    try:
        full = b10_at(fn(s + "bp", size), col, y)
        g = VGroup(*list(full)[:len(s.replace(" ", ""))])
        if len(g) == 0:
            raise ValueError
        return g
    except Exception:                                                # Gate A's stub has no glyphs: plain centre placement
        return b10_at(fn(s, size), col, y)


def b10_y(k):
    return B10_Y0 - k * B10_DY


def b10_name(k):
    return b10_cell(M, B10_ROWS[k][0], 32, 0, b10_y(k))


def b10_time(k):
    return b10_cell(T, B10_ROWS[k][2], 40, 1, b10_y(k))


def b10_bar(k):
    w = B10_ROWS[k][1] * B10_BAR_UNIT
    return Rectangle(width=w, height=0.32, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B10_BAR_X0 + w / 2, b10_y(k), 0])


def b10_rule(k, color=BAR1, sw=3):
    """The rule under row k (k = -1 is the heavy rule under the header)."""
    y = b10_y(k) - B10_DY / 2
    return Line([B10_L, y, 0], [B10_R, y, 0], color=color, stroke_width=sw)


def b10_tag(cx, cy):
    """A kraft luggage tag with a hole (small object: dark-kraft outline, never ink)."""
    body = Polygon([cx - 0.42, cy, 0], [cx - 0.22, cy + 0.22, 0], [cx + 0.42, cy + 0.22, 0], [cx + 0.42, cy - 0.22, 0], [cx - 0.22, cy - 0.22, 0],
                   fill_color=BOX_L, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    hole = Dot([cx - 0.2, cy, 0], radius=0.05, color=CARD)
    return VGroup(body, hole)


class B10_GpuPartitions(Scene):
    def construct(self):
        self.add(pa_title("I · The GPU Partitions"))
        hb = lambda t, size: T(t, size, bold=True)
        head = VGroup(b10_cell(hb, "partition", 36, 0, B10_HEAD_Y), b10_cell(hb, "max time", 36, 1, B10_HEAD_Y),
                      b10_cell(hb, "hours", 36, 2, B10_HEAD_Y))
        until(self, "Start with where", lead=0.0)
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.4)
        until(self, "into partitions", lead=0.2)
        self.play(Create(b10_rule(-1, INK, 5)), run_time=0.5)                                      # the heavy header rule
        until(self, "six are the ones", lead=0.2)
        self.play(LaggedStart(*[Create(b10_rule(k)) for k in range(6)], lag_ratio=0.2), run_time=0.9)   # six rows open
        until(self, "gpu, the general one", lead=0.2)
        self.play(FadeIn(b10_name(0), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "up to eight hours", lead=0.1)
        self.play(FadeIn(b10_time(0)), GrowFromEdge(b10_bar(0), LEFT), run_time=0.5)
        until(self, "gpu-interactive", lead=0.2)
        self.play(FadeIn(b10_name(1), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "two hours.", lead=0.1)
        self.play(FadeIn(b10_time(1)), GrowFromEdge(b10_bar(1), LEFT), run_time=0.4)
        until(self, "gpu-short", lead=0.2)
        self.play(FadeIn(b10_name(2), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "two hours too", lead=0.1)
        self.play(FadeIn(b10_time(2)), GrowFromEdge(b10_bar(2), LEFT), run_time=0.4)
        until(self, "but prioritised", lead=0.1)
        self.play(FadeIn(pa_at(T("prioritised", 32), B10_TAG_X, b10_y(2)), shift=RIGHT * 0.2), run_time=0.4)   # the ink tag
        until(self, "multigpu", lead=0.2)
        self.play(FadeIn(b10_name(3), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "twenty-four hours", lead=0.1)
        self.play(FadeIn(b10_time(3)), GrowFromEdge(b10_bar(3), LEFT), run_time=0.6)
        until(self, "courses-gpu", lead=0.2)
        self.play(FadeIn(b10_name(4), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "for classes, twenty-four", lead=0.0)
        self.play(FadeIn(b10_time(4)), GrowFromEdge(b10_bar(4), LEFT), run_time=0.6)
        until(self, "And sharing", lead=0.2)
        self.play(FadeIn(b10_name(5), shift=RIGHT * 0.3), run_time=0.4)
        until(self, "lend to everyone", lead=0.1)
        self.play(GrowFromCenter(b10_tag(B10_TAG_X + 0.42, b10_y(5))),                                # the kraft tag
                  FadeIn(pa_at(T("lent by PIs", 32), B10_TAG_X + 1.05, b10_y(5)), shift=RIGHT * 0.2), run_time=0.4)
        until(self, "one hour at a time", lead=0.1)
        self.play(FadeIn(b10_time(5)), GrowFromEdge(b10_bar(5), LEFT), run_time=0.35)
        done(self)


# ─────────────── B20 · a few large cores against thousands of small ones ───────────────
B20_CPU_C = np.array([-3.2, -0.25, 0.0])                             # block centres
B20_GPU_C = np.array([3.2, -0.25, 0.0])
B20_W, B20_H, B20_RIM = 4.4, 3.3, 0.2                                # block size, rim width (the rim is the block's colour)
B20_CORE, B20_CORE_OFF = 1.05, 0.7                                   # the four large cores: side, offset from centre
B20_COLS, B20_NROWS, B20_PITCH, B20_SIDE = 24, 16, 0.16, 0.11        # the small cores: 384 grey squares with gaps
B20_TOP_Y = 2.3                                                      # the lone core, then the problem bar
B20_LAB_Y = -2.45


def b20_block(c, rim):
    """A flat block: an ink-outlined rim in its own colour around a pale pad (the cores sit on the pad)."""
    outer = Rectangle(width=B20_W, height=B20_H, fill_color=rim, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(c)
    inner = Rectangle(width=B20_W - 2 * B20_RIM, height=B20_H - 2 * B20_RIM, fill_color=PA_PAD, fill_opacity=1, stroke_width=0).move_to(c)
    return VGroup(outer, inner)


def b20_lid(c, fill):
    """The lid that covers the pad until the block opens (fully opaque, no outline inside the ink rim)."""
    return Rectangle(width=B20_W - 2 * B20_RIM, height=B20_H - 2 * B20_RIM, fill_color=fill, fill_opacity=1, stroke_width=0).move_to(c)


def b20_slot(k):
    """Centre of large core k (0..3) in the CPU block."""
    dx, dy = ((-1, 1), (1, 1), (-1, -1), (1, -1))[k]
    return B20_CPU_C + np.array([dx * B20_CORE_OFF, dy * B20_CORE_OFF, 0.0])


def b20_core(k):
    return Square(side_length=B20_CORE, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to(b20_slot(k))


def b20_cell_xy(c, r):
    x = B20_GPU_C[0] + (c - (B20_COLS - 1) / 2) * B20_PITCH
    y = B20_GPU_C[1] + (r - (B20_NROWS - 1) / 2) * B20_PITCH
    return np.array([x, y, 0.0])


def b20_cells():
    """The small cores, one VGroup per column (filled column by column)."""
    return [VGroup(*[Square(side_length=B20_SIDE, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to(b20_cell_xy(c, r))
                     for r in range(B20_NROWS)]) for c in range(B20_COLS)]


def b20_fill(self, cols, rt):
    """The columns appear left to right in one play (any frame rate)."""
    n = len(cols)
    for m in cols:
        m.set_opacity(0)
    self.add(*cols)
    holder = VGroup(*cols)

    def upd(m, a):
        k = min(n, int(a * n + 0.5))
        for i, c in enumerate(cols):
            c.set_opacity(1.0 if i < k else 0.0)

    self.play(UpdateFromAlphaFunc(holder, upd), run_time=rt, rate_func=linear)
    upd(holder, 1.0)


def b20_bar():
    return Rectangle(width=3.6, height=0.34, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([0, B20_TOP_Y, 0])


def b20_slivers():
    """The problem bar cut into one sliver per GPU column."""
    return [Rectangle(width=0.1, height=0.34, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-1.8 + 0.075 + 0.15 * i, B20_TOP_Y, 0])
            for i in range(B20_COLS)]


class B20_FewVsThousands(Scene):
    def construct(self):
        self.add(pa_title("II · What A GPU Is"))
        cpu, gpu = b20_block(B20_CPU_C, BAR2), b20_block(B20_GPU_C, DARK_TOP)
        lid_c, lid_g = b20_lid(B20_CPU_C, BAR2), b20_lid(B20_GPU_C, DARK_TOP)
        self.add(cpu, lid_c, gpu, lid_g)                                                             # two closed blocks
        until(self, "Start with a core", lead=0.2)
        core = Square(side_length=0.6, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([0, B20_TOP_Y, 0])
        self.play(GrowFromCenter(core), run_time=0.4)                                               # one core, on its own
        until(self, "A CPU has", lead=0.2)
        self.play(lid_c.animate.shift(UP * 0.35).set_opacity(0), run_time=0.4)                      # the CPU opens
        self.remove(lid_c)
        self.play(core.animate.move_to(b20_slot(0)).scale(B20_CORE / 0.6), run_time=0.5)           # the core becomes the first of four
        self.play(LaggedStart(*[GrowFromCenter(b20_core(k)) for k in (1, 2, 3)], lag_ratio=0.35), run_time=0.6)
        self.play(FadeIn(T("a few complex cores", 34).move_to([B20_CPU_C[0], B20_LAB_Y, 0]), shift=UP * 0.15), run_time=0.35)
        until(self, "A GPU has thousands", lead=0.2)
        self.play(lid_g.animate.shift(UP * 0.35).set_opacity(0), run_time=0.4)                      # the GPU opens
        self.remove(lid_g)
        cells = b20_cells()
        b20_fill(self, cells, 1.1)                                                                   # hundreds of small cores fill in
        self.play(FadeIn(T("thousands of simple cores", 34).move_to([B20_GPU_C[0], B20_LAB_Y, 0]), shift=UP * 0.15), run_time=0.35)
        until(self, "For a problem", lead=0.2)
        bar = b20_bar()
        self.play(GrowFromCenter(bar), run_time=0.4)                                                # the problem
        until(self, "split into thousands", lead=0.1)
        slivers = b20_slivers()
        self.remove(bar)
        self.add(*slivers)
        self.play(LaggedStart(*[s.animate.move_to(b20_cell_xy(i, B20_NROWS - 1) + UP * 0.1) for i, s in enumerate(slivers)], lag_ratio=0.02),
                  run_time=0.9)                                                                      # the slivers land on the grid
        self.play(*[c.animate.set_color(BAR1) for c in cells], *[FadeOut(s) for s in slivers], run_time=0.4)   # every small core busy
        self.remove(*slivers)
        until(self, "the GPU is the right tool", lead=0.1)
        self.play(GrowFromCenter(check(B20_GPU_C[0] + 1.75, B20_TOP_Y - 0.2, s=0.22, color=TERRA)), run_time=0.4)
        done(self)


# ─────────────── B21 · Ferraris and bicycles: a few fast against thousands at once, then the matrix ───────────────
B21_CITY = Iso(-3.2, -2.75, 0.46)                                    # the city: 6 x 6 kraft houses on a 1-unit street grid
B21_N = 6
B21_HW, B21_HH = 0.5, 0.4                                            # house footprint and height
B21_FERRARI_HOUSES = ((0, 4), (0, 1), (3, 0))                        # the three houses the carriers reach (front edges: nothing occludes a parked carrier)
B21_PARK = {(0, 4): (-0.55, 4.35), (0, 1): (-0.55, 1.35), (3, 0): (3.27, -0.55)}   # where each carrier parks (x0, y0), on the plinth margin
B21_DEPOT_CAR = (np.array([4.3, 1.9, 0.0]), np.array([5.0, 1.9, 0.0]), np.array([5.7, 1.9, 0.0]))
B21_DEPOT_DOTS = np.array([5.0, 1.05, 0.0])                          # the swarm waits here, 9 x 4
B21_LAB_X = 0.85                                                     # labels sit to the left of the depot rows
B21_MAT_C = np.array([3.3, -1.2, 0.0])                               # the matrix: 14 x 8 cells
B21_MAT_COLS, B21_MAT_ROWS, B21_MAT_PITCH, B21_MAT_SIDE = 14, 8, 0.3, 0.23
B21_PROFS = (16, 60, 94)                                             # the three cells the professors fill (one at a time)
B21_MAT_SCALE0 = 0.85                                                # drawn small, grows at "a very large matrix"


def b21_zi(x, y):
    """Painter's order in the city: things nearer the viewer (smaller x + y) draw later."""
    return 30.0 - 2.0 * (x + y)


def b21_plinth():
    """A thin plinth under the city: pale board on top, dark sides carry Gate V's contrast."""
    return B21_CITY.box(-0.6, -0.6, -0.12, B21_N + 1.2, B21_N + 1.2, 0.12, PA_PAD, DARK_L, DARK_R).set_z_index(-1)


def b21_house(i, j):
    """A small kraft house (small object: dark-kraft outline)."""
    iso, x0, y0 = B21_CITY, i + 0.25, j + 0.25
    x1, y1, z1 = x0 + B21_HW, y0 + B21_HW, B21_HH
    h = VGroup(iso.quad([(x0, y0, 0), (x0, y1, 0), (x0, y1, z1), (x0, y0, z1)], BOX_L, stroke=PA_SMALL, sw=2),
               iso.quad([(x0, y0, 0), (x1, y0, 0), (x1, y0, z1), (x0, y0, z1)], BOX_R, stroke=PA_SMALL, sw=2),
               iso.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], BOX_TOP, stroke=PA_SMALL, sw=2))
    return h.set_z_index(b21_zi(x0 + 0.25, y0 + 0.25))


def b21_houses():
    """All 36 houses, back row first."""
    order = sorted([(i, j) for i in range(B21_N) for j in range(B21_N)], key=lambda ij: -(ij[0] + ij[1]))
    return VGroup(*[b21_house(i, j) for i, j in order])


def b21_roof(i, j):
    return B21_CITY.p(i + 0.5, j + 0.5, B21_HH)


def b21_dot(i, j):
    return Dot(b21_roof(i, j), radius=0.07, color=TERRA).set_z_index(b21_zi(i + 0.5, j + 0.5) + 0.5)


def b21_carrier(i, j):
    """A dark carrier parked on the plinth margin beside house (i, j), at the city's front edge."""
    iso = B21_CITY
    x0, y0 = B21_PARK[(i, j)]
    return iso.box(x0, y0, 0, 0.45, 0.3, 0.22, DARK_TOP, DARK_L, DARK_R, sw=2).set_z_index(b21_zi(x0 + 0.225, y0 + 0.15))


def b21_cell(k):
    c, r = k % B21_MAT_COLS, k // B21_MAT_COLS
    x = B21_MAT_C[0] + (c - (B21_MAT_COLS - 1) / 2) * B21_MAT_PITCH
    y = B21_MAT_C[1] + (r - (B21_MAT_ROWS - 1) / 2) * B21_MAT_PITCH
    return Square(side_length=B21_MAT_SIDE, fill_color=PA_PAD, fill_opacity=1, stroke_color=BAR3, stroke_width=1.5).move_to([x, y, 0])


def b21_matrix():
    return VGroup(*[b21_cell(k) for k in range(B21_MAT_COLS * B21_MAT_ROWS)])


def b21_park(mob, depot):
    """Move a finished object to its depot spot; returns the vector that brings it back (the stub's centre is a list)."""
    v = depot - np.array(mob.get_center())
    mob.shift(v)
    return -v


class B21_FerrarisAndBicycles(Scene):
    def construct(self):
        self.add(b21_plinth())
        cars = [b21_carrier(i, j) for i, j in B21_FERRARI_HOUSES]
        car_back = [b21_park(c, d) for c, d in zip(cars, B21_DEPOT_CAR)]
        rest = [(i, j) for i in range(B21_N) for j in range(B21_N) if (i, j) not in B21_FERRARI_HOUSES]
        dots = [b21_dot(i, j) for i, j in rest]
        slots = [B21_DEPOT_DOTS + np.array([(k % 9 - 4) * 0.16, (1.5 - k // 9) * 0.16, 0.0]) for k in range(len(dots))]
        dot_back = [b21_park(d, s) for d, s in zip(dots, slots)]
        self.add(*cars, *dots)                                                                       # the few and the many wait
        until(self, "Delivering thousands", lead=0.2)
        houses = b21_houses()
        rt = guard(self, 1.0)
        for h in houses:
            h.shift(UP * 4.0)
        self.add(houses)
        self.play(LaggedStart(*[h.animate.shift(DOWN * 4.0) for h in houses], lag_ratio=0.02), run_time=rt, rate_func=ease_in)   # the city
        until(self, "a few Ferraris", lead=0.2)
        self.play(FadeIn(pa_at(T("a few fast", 34), B21_LAB_X, B21_DEPOT_CAR[0][1]), shift=RIGHT * 0.2), run_time=0.3)
        self.play(LaggedStart(*[c.animate.shift(v) for c, v in zip(cars, car_back)], lag_ratio=0.3), run_time=1.3)   # one house each
        self.play(*[GrowFromCenter(b21_dot(i, j)) for i, j in B21_FERRARI_HOUSES], run_time=0.25)
        until(self, "or thousands of bicycles", lead=0.1)
        self.play(FadeIn(pa_at(T("thousands at once", 34), B21_LAB_X, B21_DEPOT_DOTS[1]), shift=RIGHT * 0.2), run_time=0.3)
        until(self, "The bicycles.", lead=0.1)
        self.play(LaggedStart(*[d.animate.shift(v) for d, v in zip(dots, dot_back)], lag_ratio=0.01), run_time=1.1)   # every house at once
        until(self, "Or a room of professors", lead=0.1)
        mat = b21_matrix().scale(B21_MAT_SCALE0)
        self.play(FadeIn(mat, shift=UP * 0.15), run_time=0.5)                                       # the matrix, empty
        until(self, "The professors win", lead=0.1)
        profs = VGroup(*[Square(side_length=B21_MAT_SIDE * B21_MAT_SCALE0, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0)
                         .move_to(np.array(mat[k].get_center())) for k in B21_PROFS])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in profs], lag_ratio=0.45), run_time=1.0)   # a few cells, one at a time
        mat.add(*profs)
        until(self, "a very large matrix", lead=0.1)
        self.play(mat.animate.scale(1.0 / B21_MAT_SCALE0), run_time=0.5)                            # very large
        until(self, "a multiply and an add", lead=0.1)
        self.play(mat[0].animate.scale(1.6), run_time=0.25)                                          # one cell's work
        self.play(mat[0].animate.scale(1.0 / 1.6), run_time=0.25)
        until(self, "the stadium wins", lead=0.1)
        self.play(*[c.animate.set_color(BAR1) for c in list(mat)[:B21_MAT_COLS * B21_MAT_ROWS]], run_time=0.5)   # every cell, all at once
        until(self, "those are stadium jobs", lead=0.1)
        self.play(GrowFromCenter(check(5.7, 0.35, s=0.22, color=TERRA)), run_time=0.4)
        done(self)
