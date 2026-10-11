# ═════════════════════════════ PART A · B10 (Act I) · B20 (Act II) · B30 B31 (Act III) · B50 (Act V) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PA_ / pa_ / b10_ / b20_ / b30_ / b31_ / b50_ so the parts never collide.
#
# Stage map. B10: three flat timeline grids stacked (serial 9 slots, pipelined 5, data-parallel 3), kraft blocks in
# three kraft tones (wash / dry / fold, legend at the top), the slot count as an ink numeral beside each grid.
# B20: a 2 x 2 grid in grey with ink axis arrows, one acronym and one tiny cast picture per cell, terracotta dots on
# SIMD and MIMD. B30: a node is a thin plinth (pale board, dark sides) with pale core pads and a kraft memory slab;
# the left node's pads cable to one slab (OpenMP), three right nodes each own a slab and share a belt (MPI), then
# "hybrid" cables each right node's pads to its own slab. B31: the same plinth, 20 pads in 4 x 5, process frames in
# deep kraft spanning the pads, one terracotta dot per process (the rank), mono flags on the right. B50: a 12 x 8
# Life grid of pale cells with gaps, live cells dark, a glider stepping twice, a kraft ring round one cell's eight
# neighbours, a grey cursor sweeping row by row, then four bands sweeping at once.
PA_KRAFT = "#9C8462"                        # deep-kraft connector: cables, frames, belt dots (lines are never ink inside an ink bbox)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T: small ink rings fuse)
PA_PAD = "#E4E0D4"                          # pads, boards and dead cells stay within 28 of the stage (Gate V does not count them as ink)


def pa_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_at(mob, x_left, y):
    """Place a text by its LEFT edge."""
    return mob.move_to([x_left + mob.width / 2, y, 0])


def pa_slide_in(self, mob, vec, rt=0.7):
    """Slide a whole object in from off-stage, fully opaque (GATE T: never a half-faded dark block)."""
    rt = guard(self, rt)
    mob.shift(-vec)
    self.add(mob)
    self.play(mob.animate.shift(vec), run_time=rt)


def pa_drop(self, mobs, rt=0.55, lag=0.2, dist=5.0):
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), run_time=rt, rate_func=ease_in)


def pa_plinth(iso, x0, y0, w, d):
    """A node: a thin plinth, pale board on top, dark sides carry Gate V's contrast."""
    return iso.box(x0, y0, -0.12, w, d, 0.12, PA_PAD, DARK_L, DARK_R).set_z_index(-1)


def pa_pad(iso, x, y, s):
    """A core pad lying on a plinth (small object: dark-kraft outline)."""
    return iso.quad([(x, y, 0.02), (x + s, y, 0.02), (x + s, y + s, 0.02), (x, y + s, 0.02)], PA_PAD, stroke=PA_SMALL, sw=3).set_z_index(1)


def pa_slab(iso, x, y, w, d, h):
    """A kraft memory slab standing at the back of a plinth."""
    return iso.box(x, y, 0, w, d, h).set_z_index(1)


def pa_cable(a, b, w=5):
    return Line(a, b, color=PA_KRAFT, stroke_width=w).set_z_index(2)


def pa_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes (edges dark kraft, never ink)."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PA_PAD, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


# ─────────────── B10 · laundry: serial 9, pipelined 5, data-parallel 3 ───────────────
B10_X0, B10_P, B10_W, B10_H, B10_RP = -5.4, 0.7, 0.6, 0.32, 0.4      # slot-0 centre, slot pitch, block size, row pitch
B10_ROWY = (1.75, 0.0, -1.75)                                        # y of load 0 in each of the three grids
B10_FILL = (BOX_L, BOX_R, BOX_FLOOR)                                 # wash / dry / fold
B10_LAB_X, B10_NUM_X = 2.6, 5.2


def b10_block(slot, row, stage, y0):
    return Rectangle(width=B10_W, height=B10_H, fill_color=B10_FILL[stage], fill_opacity=1, stroke_color=PA_SMALL, stroke_width=2) \
        .move_to([B10_X0 + slot * B10_P, y0 - row * B10_RP, 0])


def b10_grid(kind, y0):
    """Three loads x three stages, placed by the source's tables; blocks returned in slot order."""
    specs = []
    for r in range(3):
        for s in range(3):
            slot = {"serial": 3 * r + s, "pipe": r + s, "par": s}[kind]
            specs.append((slot, r, s))
    specs.sort()
    return VGroup(*[b10_block(sl, r, s, y0) for sl, r, s in specs])


def b10_legend():
    g = VGroup()
    for k, (x, w) in enumerate(((-0.1, "wash"), (1.8, "dry"), (3.5, "fold"))):
        g.add(Square(side_length=0.3, fill_color=B10_FILL[k], fill_opacity=1, stroke_color=PA_SMALL, stroke_width=2).move_to([x, 2.45, 0]),
              pa_at(T(w, 34), x + 0.45, 2.45))
    return g


def b10_label(word, k):
    return T(word, 36).move_to([B10_LAB_X, B10_ROWY[k] - 0.4, 0])


def b10_num(n, k):
    return T(n, 84).move_to([B10_NUM_X, B10_ROWY[k] - 0.4, 0])


class B10_Laundry(Scene):
    def construct(self):
        self.add(pa_title("I · Why Parallel"))
        until(self, "Simulations")
        bar = Rectangle(width=5.4, height=0.44, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-2.6, 0.0, 0])
        self.play(GrowFromEdge(bar, LEFT), run_time=0.8)                                   # the work, one piece
        until(self, "so we split the work", lead=0.3)
        pieces = VGroup(*[Rectangle(width=1.7, height=0.44, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-4.4 + 1.8 * k, 0, 0])
                          for k in range(3)])
        self.remove(bar)
        self.add(pieces)
        self.play(pieces[0].animate.shift(LEFT * 0.35), pieces[2].animate.shift(RIGHT * 0.35), run_time=0.5)   # split
        until(self, "Think of laundry")
        self.play(FadeOut(pieces), FadeIn(b10_legend()), run_time=0.5)
        until(self, "Serial:")
        ga = b10_grid("serial", B10_ROWY[0])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in ga], lag_ratio=0.12), run_time=1.3)
        self.add(b10_label("serial", 0))
        until(self, "Nine steps")
        self.play(FadeIn(b10_num("9", 0), scale=0.7), run_time=0.4)
        until(self, "Pipelining:")
        gb = b10_grid("pipe", B10_ROWY[1])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in gb], lag_ratio=0.12), run_time=1.1)
        self.add(b10_label("pipelined", 1))
        until(self, "Five steps")
        self.play(FadeIn(b10_num("5", 1), scale=0.7), run_time=0.4)
        until(self, "Data parallelism:")
        gc = b10_grid("par", B10_ROWY[2])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in gc], lag_ratio=0.12), run_time=0.9)
        self.add(b10_label("data parallel", 2))
        until(self, "Three steps")
        self.play(FadeIn(b10_num("3", 2), scale=0.7), run_time=0.4)
        until(self, "cut a big problem")
        self.play(Indicate(gc, color=None, scale_factor=1.06), run_time=0.7)
        done(self)


# ─────────────── B20 · Flynn's four kinds: a 2 x 2 grid, one tiny cast picture per cell ───────────────
B20_X0, B20_X1, B20_XM = -3.2, 4.6, 0.7                              # grid edges and the column divider
B20_Y0, B20_Y1, B20_YM = -3.1, 2.1, -0.5                             # grid edges and the row divider
B20_CW, B20_CH = 3.9, 2.6                                            # cell size
B20_CELL = {"SISD": (0, 0), "MISD": (1, 0), "SIMD": (0, 1), "MIMD": (1, 1)}   # (column: instruction, row: data)


def b20_cell(name):
    """(x0, y1): the top-left corner of the cell."""
    i, j = B20_CELL[name]
    return B20_X0 + i * B20_CW, B20_Y1 - j * B20_CH


def b20_pic(name):
    """Centre of the picture area in the cell."""
    x0, y1 = b20_cell(name)
    return x0 + 1.95, y1 - 1.6


def b20_grid():
    return VGroup(Rectangle(width=B20_X1 - B20_X0, height=B20_Y1 - B20_Y0, stroke_color=BAR2, stroke_width=3, fill_opacity=0)
                  .move_to([(B20_X0 + B20_X1) / 2, (B20_Y0 + B20_Y1) / 2, 0]),
                  Line([B20_XM, B20_Y0, 0], [B20_XM, B20_Y1, 0], color=BAR2, stroke_width=3),
                  Line([B20_X0, B20_YM, 0], [B20_X1, B20_YM, 0], color=BAR2, stroke_width=3))


def b20_axis_x():
    return Arrow([B20_X0, B20_Y1, 0], [B20_X1 + 0.3, B20_Y1, 0], color=INK, stroke_width=5, buff=0)


def b20_axis_y():
    return Arrow([B20_X0, B20_Y1, 0], [B20_X0, B20_Y0 - 0.1, 0], color=INK, stroke_width=5, buff=0)


def b20_acr(name):
    x0, y1 = b20_cell(name)
    return pa_at(T(name, 44), x0 + 0.25, y1 - 0.45)


def b20_dot(name):
    x0, y1 = b20_cell(name)
    return Dot([x0 + 1.95, y1 - 0.45, 0], radius=0.12, color=TERRA)


def b20_tag(name, word):
    x0, y1 = b20_cell(name)
    return pa_at(T(word, 34), x0 + 2.3, y1 - 0.45)


def b20_data(x, y, pale=False):
    return Square(side_length=0.26, fill_color=GHOST if pale else BOX_L, fill_opacity=1,
                  stroke_color=BAR3 if pale else PA_SMALL, stroke_width=2).move_to([x, y, 0])


def b20_sisd():
    cx, cy = b20_pic("SISD")
    return VGroup(Square(side_length=0.55, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([cx, cy + 0.25, 0]),
                  b20_data(cx, cy - 0.75))


def b20_simd():
    cx, cy = b20_pic("SIMD")
    body, light = gpu_block(Iso(cx - 0.55, cy - 0.2, 0.6))
    return VGroup(body, light, *[b20_data(cx + (k - 2.5) * 0.36, cy - 0.65) for k in range(6)])


def b20_misd():
    cx, cy = b20_pic("MISD")
    return VGroup(*[Square(side_length=0.5, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([cx + dx, cy + 0.25, 0]) for dx in (-0.7, 0, 0.7)],
                  b20_data(cx, cy - 0.75, pale=True))


def b20_mimd():
    cx, cy = b20_pic("MIMD")
    g = VGroup()
    for k in range(3):
        st, li = explorer_rack(Iso(cx - 1.2 + 1.15 * k, cy - 0.3, 0.36))
        g.add(st, li, b20_data(cx - 1.2 + 1.15 * k, cy - 0.7))
    return g


class B20_Flynn(Scene):
    def construct(self):
        self.add(pa_title("II · Flynn's Four Kinds"))
        until(self, "sorts machines")
        self.play(Create(b20_grid()), run_time=0.8)
        until(self, "Single or multiple instruction", lead=0.4)
        self.play(GrowArrow(b20_axis_x()), run_time=0.5)
        self.play(FadeIn(T("instruction", 36).move_to([0.7, 2.95, 0])),
                  FadeIn(T("single", 36).move_to([-1.25, 2.45, 0])), FadeIn(T("multiple", 36).move_to([2.65, 2.45, 0])), run_time=0.4)
        until(self, "single or multiple data", lead=0.4)
        self.play(GrowArrow(b20_axis_y()), run_time=0.5)
        self.play(FadeIn(T("data", 36).move_to([-5.5, -0.5, 0])),
                  FadeIn(T("single", 36).move_to([-4.3, 0.8, 0])), FadeIn(T("multiple", 36).move_to([-4.3, -1.8, 0])), run_time=0.4)
        until(self, "SISD is")
        self.play(FadeIn(b20_acr("SISD")), GrowFromCenter(b20_sisd()), run_time=0.5)
        until(self, "SIMD is")
        self.play(FadeIn(b20_acr("SIMD")), GrowFromCenter(b20_simd()), run_time=0.5)
        until(self, "that is a GPU", lead=0.2)
        self.play(FadeIn(b20_tag("SIMD", "GPU"), shift=LEFT * 0.2), run_time=0.3)
        until(self, "MISD is")
        self.play(FadeIn(b20_acr("MISD")), GrowFromCenter(b20_misd()), run_time=0.5)
        until(self, "MIMD is")
        self.play(FadeIn(b20_acr("MIMD")), run_time=0.3)
        pa_drop(self, [b20_mimd()], 0.6, dist=3.5)
        until(self, "a multi-node cluster", lead=0.2)
        self.play(FadeIn(b20_tag("MIMD", "cluster"), shift=LEFT * 0.2), run_time=0.3)
        until(self, "two are SIMD", lead=0.1)
        self.play(GrowFromCenter(b20_dot("SIMD")), run_time=0.3)
        until(self, "and MIMD, the cluster", lead=0.1)
        self.play(GrowFromCenter(b20_dot("MIMD")), run_time=0.3)
        done(self)


# ─────────────── B30 · shared memory (one node, one slab, OpenMP) vs distributed (three nodes, a belt, MPI), then hybrid ───────────────
B30_L = Iso(-3.8, -1.3, 0.65)                                        # the one shared-memory node, left
B30_R = [Iso(0.9 + 2.0 * k, -0.5, 0.5) for k in range(3)]            # three distributed nodes, right
B30_LPADS = (0.2, 1.0, 1.8, 2.6)                                     # x of the left node's four pads (size 0.6, at y 0.4)
B30_RPADS = (0.15, 1.05)                                             # x of each right node's two pads (size 0.6, at y 0.05)
B30_BELT_Y = -1.65


def b30_left_plinth():
    return pa_plinth(B30_L, -0.3, -0.3, 3.6, 2.8)


def b30_left_pads():
    return VGroup(*[pa_pad(B30_L, x, 0.4, 0.6) for x in B30_LPADS])


def b30_left_slab():
    return pa_slab(B30_L, 0.1, 1.8, 3.2, 0.6, 0.7)


def b30_left_cable_ends(x):
    return B30_L.p(x + 0.3, 1.0, 0.03), B30_L.p(x + 0.3, 1.8, 0.3)


def b30_left_cables():
    return VGroup(*[pa_cable(*b30_left_cable_ends(x)) for x in B30_LPADS])


def b30_right_node(k):
    iso = B30_R[k]
    return VGroup(pa_plinth(iso, -0.3, -0.3, 2.2, 2.2), *[pa_pad(iso, x, 0.05, 0.6) for x in B30_RPADS], pa_slab(iso, 0.1, 1.3, 1.6, 0.45, 0.6))


def b30_right_cables(k):
    iso = B30_R[k]
    return VGroup(*[pa_cable(iso.p(x + 0.3, 0.65, 0.03), iso.p(x + 0.3, 1.3, 0.3)) for x in B30_RPADS])


def b30_belt():
    return pa_belt(-0.1, 5.8, B30_BELT_Y)


def b30_belt_run(self, rt=0.7):
    """A packet rides the belt from the first node to the last and is gone."""
    rt = guard(self, rt)
    d = Dot([0.5, B30_BELT_Y + 0.15, 0], radius=0.1, color=TERRA)
    self.add(d)
    self.play(d.animate.move_to([5.3, B30_BELT_Y + 0.15, 0]), run_time=rt)
    self.remove(d)


class B30_SharedVsDistributed(Scene):
    def construct(self):
        self.add(pa_title("III · Shared Or Distributed"))
        self.play(GrowFromCenter(b30_left_plinth()), run_time=0.5)
        until(self, "Shared memory:", lead=0.3)
        self.play(FadeIn(T("shared memory", 40).move_to([-3.8, 2.0, 0])), run_time=0.35)
        until(self, "the cores of one node", lead=0.2)
        pads = b30_left_pads()
        self.play(LaggedStart(*[GrowFromCenter(p) for p in pads], lag_ratio=0.2), run_time=0.7)
        until(self, "one pool of RAM", lead=0.3)
        pa_slide_in(self, b30_left_slab(), DOWN * 4.5, 0.6)
        self.add(T("RAM", 34).move_to([-5.6, 0.6, 0]))
        until(self, "any core any address", lead=0.3)
        self.play(Create(b30_left_cables()), run_time=0.5)
        dots = VGroup(*[Dot(b30_left_cable_ends(x)[0], radius=0.09, color=TERRA).set_z_index(3) for x in B30_LPADS])
        self.add(dots)
        self.play(LaggedStart(*[d.animate.move_to(b30_left_cable_ends(x)[1]) for d, x in zip(dots, B30_LPADS)], lag_ratio=0.15), run_time=0.6)
        self.play(FadeOut(dots), run_time=0.2)
        self.remove(dots)
        until(self, "the tool is OpenMP", lead=0.2)
        self.play(FadeIn(T("OpenMP", 44).move_to([-3.8, -2.4, 0]), shift=UP * 0.2), run_time=0.35)
        until(self, "the limit is one machine", lead=0.2)
        self.play(Indicate(pads, color=None, scale_factor=1.08), run_time=0.6)
        until(self, "Distributed memory:", lead=0.3)
        nodes = [b30_right_node(k) for k in range(3)]
        self.play(FadeIn(T("distributed memory", 40).move_to([2.9, 2.0, 0])), run_time=0.3)
        pa_drop(self, nodes, 0.8, 0.25, dist=4.0)
        until(self, "node A", lead=0.2)
        self.play(Indicate(nodes[0], color=None, scale_factor=1.06), run_time=0.35)
        self.play(Indicate(nodes[1], color=None, scale_factor=1.06), run_time=0.35)
        until(self, "Programs send data", lead=0.3)
        self.play(GrowFromEdge(b30_belt(), LEFT), run_time=0.6)
        b30_belt_run(self, 0.7)
        until(self, "the tool is MPI", lead=0.2)
        self.play(FadeIn(T("MPI", 44).move_to([2.9, -2.4, 0]), shift=UP * 0.2), run_time=0.35)
        until(self, "scale across nodes", lead=0.2)
        self.play(Indicate(VGroup(*nodes), color=None, scale_factor=1.04), run_time=0.6)
        until(self, "hybrid", lead=0.3)
        self.play(FadeIn(T("hybrid", 44).move_to([-0.5, -2.9, 0]), shift=UP * 0.2), run_time=0.35)
        until(self, "MPI between nodes", lead=0.2)
        b30_belt_run(self, 0.6)
        until(self, "OpenMP inside each", lead=0.3)
        self.play(*[Create(b30_right_cables(k)) for k in range(3)], run_time=0.6)
        done(self)


# ─────────────── B31 · ntasks x cpus-per-task: 4 x 5, then 1 x 20 (OpenMP), then 20 x 1 (MPI), then back to 4 x 5 (hybrid) ───────────────
B31 = Iso(-3.2, -1.63, 0.75)                                         # one node, 20 pads in 4 rows x 5 columns
B31_PS, B31_PP, B31_M = 0.6, 0.95, 0.14                              # pad size, pad pitch, process-frame margin
B31_FLAG_X, B31_TXT_X = 0.9, 3.3                                     # mono flags (left edge) and the T column (centre)
B31_FLAG_Y = (2.5, 1.8)


def b31_plinth():
    return pa_plinth(B31, -0.35, -0.35, 5.1, 4.15)


def b31_pads():
    return VGroup(*[pa_pad(B31, c * B31_PP, r * B31_PP, B31_PS) for r in range(4) for c in range(5)])


def b31_frame(c0, c1, r0, r1):
    """A process frame spanning pads c0..c1 x r0..r1, deep kraft (a line inside the plinth's ink bbox is never ink)."""
    x0, y0 = c0 * B31_PP - B31_M, r0 * B31_PP - B31_M
    x1, y1 = c1 * B31_PP + B31_PS + B31_M, r1 * B31_PP + B31_PS + B31_M
    return Polygon(B31.p(x0, y0, 0.04), B31.p(x1, y0, 0.04), B31.p(x1, y1, 0.04), B31.p(x0, y1, 0.04),
                   stroke_color=PA_KRAFT, stroke_width=5, fill_opacity=0).set_z_index(2)


def b31_rank(c, r):
    """The rank dot on the first pad of a process."""
    return Dot(B31.p(c * B31_PP + B31_PS / 2, r * B31_PP + B31_PS / 2, 0.05), radius=0.1, color=TERRA).set_z_index(3)


def b31_arr(kind):
    """(frames, rank dots) for an arrangement."""
    if kind == "4x5":
        return VGroup(*[b31_frame(0, 4, r, r) for r in range(4)]), VGroup(*[b31_rank(0, r) for r in range(4)])
    if kind == "1x20":
        return VGroup(b31_frame(0, 4, 0, 3)), VGroup(b31_rank(0, 0))
    return (VGroup(*[b31_frame(c, c, r, r) for r in range(4) for c in range(5)]),
            VGroup(*[b31_rank(c, r) for r in range(4) for c in range(5)]))


def b31_flags(n, c):
    return VGroup(pa_at(M(f"--ntasks-per-node={n}", 32), B31_FLAG_X, B31_FLAG_Y[0]),
                  pa_at(M(f"--cpus-per-task={c}", 32), B31_FLAG_X, B31_FLAG_Y[1]))


def b31_product(s):
    return T(s, 52).move_to([B31_TXT_X, 0.5, 0])


def b31_tool(s):
    return T(s, 44).move_to([B31_TXT_X, -2.4, 0])


def b31_regroup(self, old, new, rt=0.7):
    """Swap (frames, dots, flags, product, tool) in one play; the plinth and the 20 pads never move."""
    rt = guard(self, rt)
    outs = [FadeOut(m) for m in old if m is not None]
    ins = [FadeIn(m) for m in new if m is not None]
    self.play(*outs, *ins, run_time=rt)
    for m in old:
        if m is not None:
            self.remove(m)


class B31_TasksTimesCpus(Scene):
    def construct(self):
        pa_slide_in(self, b31_plinth(), RIGHT * 7.5, 0.7)
        until(self, "n tasks is", lead=0.2)
        fr, dots = b31_arr("4x5")
        self.play(LaggedStart(*[Create(f) for f in fr], lag_ratio=0.2), run_time=0.8)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2), run_time=0.35)
        flags = b31_flags(4, 5)
        self.play(FadeIn(flags[0], shift=LEFT * 0.2), run_time=0.3)
        until(self, "CPUs per task is", lead=0.2)
        pads = b31_pads()
        self.play(LaggedStart(*[GrowFromCenter(p) for p in pads], lag_ratio=0.06), run_time=1.0)
        self.play(FadeIn(flags[1], shift=LEFT * 0.2), run_time=0.3)
        until(self, "They multiply", lead=0.2)
        prod = b31_product("4 × 5")
        self.play(FadeIn(prod, shift=UP * 0.2), run_time=0.35)
        until(self, "is twenty cores", lead=0.2)
        self.play(FadeIn(T("20", 100).move_to([B31_TXT_X, -0.9, 0]), scale=0.7), run_time=0.45)
        until(self, "Pure OpenMP", lead=0.3)
        fr2, dots2 = b31_arr("1x20")
        flags2, prod2, tool2 = b31_flags(1, 20), b31_product("1 × 20"), b31_tool("OpenMP")
        b31_regroup(self, (fr, dots, flags, prod, None), (fr2, dots2, flags2, prod2, tool2), 0.7)
        until(self, "Pure MPI", lead=0.3)
        fr3, dots3 = b31_arr("20x1")
        flags3, prod3, tool3 = b31_flags(20, 1), b31_product("20 × 1"), b31_tool("MPI")
        b31_regroup(self, (fr2, dots2, flags2, prod2, tool2), (fr3, dots3, flags3, prod3, tool3), 0.7)
        until(self, "Hybrid sits", lead=0.3)
        fr4, dots4 = b31_arr("4x5")
        flags4, prod4, tool4 = b31_flags(4, 5), b31_product("4 × 5"), b31_tool("hybrid")
        b31_regroup(self, (fr3, dots3, flags3, prod3, tool3), (fr4, dots4, flags4, prod4, tool4), 0.6)
        done(self)


# ─────────────── B50 · the Game of Life: a glider steps twice, eight neighbours, row by row, then four bands at once ───────────────
B50_C, B50_R, B50_P, B50_S = 12, 8, 0.52, 0.42                       # columns, rows, pitch, cell side (gaps keep the grid from fusing)
B50_X0, B50_Y0 = -5.7, 1.3                                           # centre of cell (0, 0), top-left
B50_LIVE, B50_DEAD = DARK_TOP, PA_PAD
B50_GLIDER = ((2, 1), (3, 2), (1, 3), (2, 3), (3, 3))                # (col, row) of the glider's five cells at generation 0
B50_RING = (6, 4)                                                    # the cell whose eight neighbours get ringed
B50_LAB_X = 3.3


def b50_xy(c, r):
    return np.array([B50_X0 + c * B50_P, B50_Y0 - r * B50_P, 0.0])


def b50_cells():
    """All cells, dead; a list of rows, each a VGroup of Squares."""
    return [VGroup(*[Square(side_length=B50_S, fill_color=B50_DEAD, fill_opacity=1, stroke_width=0).move_to(b50_xy(c, r)) for c in range(B50_C)])
            for r in range(B50_R)]


def b50_step(live):
    """One Life generation on the bounded grid: a set of (col, row)."""
    counts = {}
    for c, r in live:
        for dc in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if dc or dr:
                    counts[(c + dc, r + dr)] = counts.get((c + dc, r + dr), 0) + 1
    return {p for p, n in counts.items() if (n == 3 or (n == 2 and p in live)) and 0 <= p[0] < B50_C and 0 <= p[1] < B50_R}


def b50_gens(n):
    g, out = set(B50_GLIDER), []
    for _ in range(n + 1):
        out.append(g)
        g = b50_step(g)
    return out


def b50_apply(self, rows, old, new, rt):
    """Recolour only the cells that change between two generations."""
    anims = [rows[r][c].animate.set_color(B50_LIVE) for c, r in new - old] + [rows[r][c].animate.set_color(B50_DEAD) for c, r in old - new]
    if anims:
        self.play(*anims, run_time=rt)


def b50_ring():
    return Square(side_length=3 * B50_P - 0.1, stroke_color=PA_KRAFT, stroke_width=5, fill_opacity=0).move_to(b50_xy(*B50_RING))


def b50_neigh(rows):
    c0, r0 = B50_RING
    return [rows[r0 + dr][c0 + dc] for dc in (-1, 0, 1) for dr in (-1, 0, 1) if dc or dr]


def b50_bar(r):
    """The core's cursor, parked at the left of row r."""
    return Rectangle(width=0.14, height=B50_S + 0.06, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to(b50_xy(0, r) + LEFT * (B50_P / 2 + 0.1))


def b50_band_lines():
    x0, x1 = B50_X0 - B50_P / 2, B50_X0 + (B50_C - 0.5) * B50_P
    return VGroup(*[Line([x0, B50_Y0 - (r + 0.5) * B50_P, 0], [x1, B50_Y0 - (r + 0.5) * B50_P, 0], color=PA_KRAFT, stroke_width=4) for r in (1, 3, 5)])


def b50_sweep(self, bars, starts, rows_each, rt):
    """Each bar sweeps its rows left to right, one row after another, all bars at once (one play, any frame rate)."""
    rt = guard(self, rt)
    x0, span = B50_X0 - B50_P / 2 - 0.1, B50_C * B50_P + 0.2
    holder = VGroup(*bars)

    def upd(m, a):
        t = min(a * rows_each, rows_each - 1e-6)
        k, f = int(t), t - int(t)
        for b, r0 in zip(bars, starts):
            b.move_to([x0 + f * span, B50_Y0 - (r0 + k) * B50_P, 0])

    self.play(UpdateFromAlphaFunc(holder, upd), run_time=rt, rate_func=linear)
    upd(holder, 1.0)


class B50_GameOfLife(Scene):
    def construct(self):
        self.add(pa_title("V · The Game Of Life"))
        rows = b50_cells()
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.1), run_time=0.7)
        gens = b50_gens(2)
        until(self, "Conway", lead=0.1)
        b50_apply(self, rows, set(), gens[0], 0.4)                                            # the glider
        until(self, "a grid where", lead=0.2)
        b50_apply(self, rows, gens[0], gens[1], 0.5)                                          # step one
        until(self, "next state depends", lead=0.2)
        b50_apply(self, rows, gens[1], gens[2], 0.5)                                          # step two
        until(self, "eight neighbours", lead=0.4)
        ring, neigh = b50_ring(), b50_neigh(rows)
        mark = Dot(b50_xy(*B50_RING), radius=0.09, color=TERRA)
        self.play(Create(ring), *[n.animate.set_color(BAR2) for n in neigh], GrowFromCenter(mark), run_time=0.5)
        lab8 = T("eight neighbours", 40).move_to([B50_LAB_X, b50_xy(*B50_RING)[1], 0])
        self.play(FadeIn(lab8), run_time=0.3)
        until(self, "embarrassingly parallel", lead=0.2)
        self.play(Indicate(ring, color=None, scale_factor=1.08), run_time=0.5)
        until(self, "every cell is independent", lead=0.2)
        self.play(FadeOut(ring), FadeOut(mark), FadeOut(lab8), *[n.animate.set_color(B50_DEAD) for n in neigh], run_time=0.4)
        self.remove(ring, mark, lab8)
        until(self, "A single core", lead=0.25)
        bar = b50_bar(0)
        self.add(bar)
        self.play(FadeIn(T("serial", 40).move_to([B50_LAB_X, 0.3, 0])), run_time=0.25)
        b50_sweep(self, [bar], [0], B50_R, 1.6)                                               # one core, row by row
        self.play(FadeOut(bar), run_time=0.15)
        self.remove(bar)
        until(self, "Many cores", lead=0.25)
        self.play(Create(b50_band_lines()), run_time=0.3)                                     # the rows split into four bands
        bars = [b50_bar(2 * k) for k in range(4)]
        self.add(*bars)
        self.play(FadeIn(T("parallel", 40).move_to([B50_LAB_X, -1.4, 0])), run_time=0.25)
        b50_sweep(self, bars, [0, 2, 4, 6], 2, 0.8)                                           # four cores, the bands at once
        done(self)
