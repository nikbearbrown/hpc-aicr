# ═════════════════════════════ PART C · B60 B61 (Act VI) · B83 (Act VIII) · B90 (Act IX) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PC_ / pc_ / b60_ / b61_ / b83_ / b90_ so the parts never collide.
#
# Stage map. Act VI opens on the CPU-against-GPU table (film 4's B20 blocks as the column heads: a grey CPU
# block with four large cores, a dark GPU block whose grey core grid fills), then B61 is the four CUDA steps in
# isometric: grey host block left, dark device block (the cast's gpu_block) right, a kraft cable between them,
# data boxes riding it both ways, sparks on the device's top face. Act VIII opens on the eight-row tool table
# (mono tool · memory icon + word · best for). Act IX is the four-row checklist (film 4's B80 grammar).
PC_KRAFT = "#9C8462"                        # deep-kraft connector (lines are never ink: ink lines fuse the things they join)
PC_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T: small ink rings fuse)
PC_PAD = "#E4E0D4"                          # pads and belts stay within 28 of the stage (Gate V does not count them as ink)
PC_CPU_TOP, PC_CPU_L, PC_CPU_R = "#C9CBCF", "#B4AFA6", "#8B8F96"   # the grey CPU block's faces (host)


def pc_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pc_left(mob, x, y):
    """Left-align a text at x, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pc_drop(self, mobs, rt=0.5, lag=0.2, dist=4.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *list(with_), run_time=rt, rate_func=ease_in)


def pc_slab(x, y, w=0.7, h=0.32):
    """One node: a flat grey slab (shared memory lives on one node). Left edge at x."""
    return VGroup(Rectangle(width=w, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x + w / 2, y, 0]))


def pc_nodes(x, y, s=0.32, gap=0.12):
    """Three nodes in a row: three grey squares with gaps (distributed memory). Left edge at x."""
    return VGroup(*[Square(side_length=s, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x + s / 2 + i * (s + gap), y, 0])
                    for i in range(3)])


# ─────────────── B60 · CPU against GPU: a two-column drawn table under the two blocks ───────────────
B60_CPU_C = np.array([-1.7, 1.75, 0.0])                              # block centres (the column heads)
B60_GPU_C = np.array([3.4, 1.75, 0.0])
B60_W, B60_H, B60_RIM = 2.6, 1.3, 0.12                               # block size, rim width (the rim is the block's colour)
B60_CORE, B60_CORE_XS = 0.46, (-0.78, -0.26, 0.26, 0.78)             # the four large cores
B60_COLS, B60_NROWS, B60_PITCH, B60_SIDE = 17, 7, 0.135, 0.095       # the small cores: 119 grey squares with gaps
B60_ROW_Y = (0.45, -0.5, -1.45)                                      # design goal · core count · best for
B60_ROWS = ("design goal", "core count", "best for")
B60_HEAD_Y = 0.95                                                    # the rule under the two blocks
B60_L, B60_R = -6.0, 6.0
B60_CAP_Y = -2.55                                                    # chefs · line cooks


def b60_block(c, rim):
    """A flat block: an ink-outlined rim in its own colour around a pale pad (the cores sit on the pad)."""
    outer = Rectangle(width=B60_W, height=B60_H, fill_color=rim, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(c)
    inner = Rectangle(width=B60_W - 2 * B60_RIM, height=B60_H - 2 * B60_RIM, fill_color=PC_PAD, fill_opacity=1, stroke_width=0).move_to(c)
    return VGroup(outer, inner)


def b60_cores():
    return VGroup(*[Square(side_length=B60_CORE, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to(B60_CPU_C + np.array([dx, 0.0, 0.0]))
                    for dx in B60_CORE_XS])


def b60_cell_xy(c, r):
    x = B60_GPU_C[0] + (c - (B60_COLS - 1) / 2) * B60_PITCH
    y = B60_GPU_C[1] + (r - (B60_NROWS - 1) / 2) * B60_PITCH
    return np.array([x, y, 0.0])


def b60_cells():
    """The small cores, one VGroup per column (filled column by column)."""
    return [VGroup(*[Square(side_length=B60_SIDE, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to(b60_cell_xy(c, r))
                     for r in range(B60_NROWS)]) for c in range(B60_COLS)]


def b60_fill(self, cols, rt):
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


def b60_rule(y, sw=3):
    return Line([B60_L, y, 0], [B60_R, y, 0], color=BAR1, stroke_width=sw)


def b60_cell(s, cx, y, size=32):
    return T(s, size).move_to([cx, y, 0])


def b60_cell2(s1, s2, cx, y, size=32):
    """A two-line cell."""
    return VGroup(T(s1, size).move_to([cx, y + 0.21, 0]), T(s2, size).move_to([cx, y - 0.21, 0]))


class B60_CpuVsGpu(Scene):
    def construct(self):
        self.add(pc_title("VI · GPU Computing"))
        labels = VGroup(*[pc_left(T(s, 34), B60_L, y) for s, y in zip(B60_ROWS, B60_ROW_Y)])
        rules = VGroup(b60_rule(B60_HEAD_Y, 5), *[b60_rule(y - 0.475) for y in B60_ROW_Y])
        self.play(FadeIn(labels, shift=RIGHT * 0.15), LaggedStart(*[Create(r) for r in rules], lag_ratio=0.15), run_time=0.7)   # the empty table
        # the CPU column
        until(self, "A CPU is built", lead=0.2)
        cpu = b60_block(B60_CPU_C, BAR2)
        pc_drop(self, [cpu], rt=0.45, dist=3.3)
        until(self, "low latency", lead=0.1)
        self.play(FadeIn(b60_cell("latency", B60_CPU_C[0], B60_ROW_Y[0]), shift=DOWN * 0.15), run_time=0.35)
        until(self, "tens of complex cores", lead=0.1)
        cores = b60_cores()
        self.play(LaggedStart(*[GrowFromCenter(k) for k in cores], lag_ratio=0.25), run_time=0.5)          # four large cores
        self.play(FadeIn(b60_cell("tens, complex", B60_CPU_C[0], B60_ROW_Y[1]), shift=DOWN * 0.15), run_time=0.35)
        until(self, "sequential logic", lead=0.15)
        self.play(FadeIn(b60_cell("sequential logic", B60_CPU_C[0], B60_ROW_Y[2]), shift=DOWN * 0.15), run_time=0.35)
        # the GPU column
        until(self, "A GPU is built", lead=0.2)
        gpu = b60_block(B60_GPU_C, DARK_TOP)
        pc_drop(self, [gpu], rt=0.45, dist=3.3)
        until(self, "throughput", lead=0.1)
        self.play(FadeIn(b60_cell("throughput", B60_GPU_C[0], B60_ROW_Y[0]), shift=DOWN * 0.15), run_time=0.35)
        until(self, "thousands of simple cores", lead=0.1)
        cells = b60_cells()
        b60_fill(self, cells, guard(self, 0.9))                                                          # the dense core grid fills
        self.play(FadeIn(b60_cell("thousands, simple", B60_GPU_C[0], B60_ROW_Y[1]), shift=DOWN * 0.15), run_time=0.35)
        until(self, "the same operation", lead=0.15)
        self.play(FadeIn(b60_cell2("same operation", "large arrays", B60_GPU_C[0], B60_ROW_Y[2]), shift=DOWN * 0.15), run_time=0.35)
        # chefs against line cooks
        until(self, "A few professional chefs", lead=0.1)
        self.play(Indicate(cores, color=None, scale_factor=1.12), FadeIn(b60_cell("chefs", B60_CPU_C[0], B60_CAP_Y, 34)), run_time=0.6)
        until(self, "a thousand line cooks", lead=0.1)
        grid = VGroup(*cells)
        self.play(Indicate(grid, color=None, scale_factor=1.05), FadeIn(b60_cell("line cooks", B60_GPU_C[0], B60_CAP_Y, 34)), run_time=0.6)
        done(self)


# ─────────────── B61 · the four steps of every GPU program: allocate · copy in · kernel · copy back ───────────────
B61_HOST = Iso(-3.4, -1.2, 1.4)                                      # the grey CPU block (host)
B61_DEV = Iso(2.6, -1.2, 1.7)                                        # the dark GPU block (device, the cast's gpu_block)
B61_DATA = 0.26                                                      # iso side of a data box
B61_CABLE_Y = -0.15
B61_CABLE_X0, B61_CABLE_X1 = -2.05, 1.0                              # clear of both blocks (a cable touching a block fuses with it)
B61_RIDE_X = (-1.85, -1.4, -0.95)                                    # where the three boxes sit on the cable before they slide
B61_SLIDE = 1.95                                                     # the slide along the cable
B61_SLAB = (0.12, 0.62, 0.5, 0.76, 0.3, 0.06)                        # memory slab on the device's top face (x0, y0, z0, w, d, h)
B61_SLAB_SPOTS = ((0.25, 0.77), (0.5, 0.77), (0.75, 0.77))           # where the data boxes land on the slab
B61_HOST_SPOTS = ((0.22, 0.5), (0.5, 0.5), (0.78, 0.5))              # where they start (and return) on the host's top face


def b61_host():
    return B61_HOST.box(0, 0, 0, 1.0, 1.0, 0.5, PC_CPU_TOP, PC_CPU_L, PC_CPU_R)


def b61_data(iso, x, y, z):
    """A small plain kraft data box centred on (x, y) of the iso, sitting on z. Small object: dark-kraft outline."""
    s = B61_DATA
    return iso.box(x - s / 2, y - s / 2, z, s, s, s * 0.8, sw=2).set_stroke(PC_SMALL).set_z_index(5)


def b61_centre(iso, x, y, z):
    return np.array(b61_data(iso, x, y, z).get_center())


def b61_cable():
    return Line([B61_CABLE_X0, B61_CABLE_Y, 0], [B61_CABLE_X1, B61_CABLE_Y, 0], color=PC_KRAFT, stroke_width=6).set_z_index(-1)


def b61_slab():
    """The allocated memory: a thin white slab on the back of the device's top face (no outline inside the ink outline)."""
    x0, y0, z0, w, d, h = B61_SLAB
    return B61_DEV.box(x0, y0, z0, w, d, h, PAGE_TOP, PAGE_L, PAGE_R, sw=0).set_z_index(3)


def b61_sparks():
    """Terracotta sparks on the front of the device's top face, inside the outline."""
    pts = [B61_DEV.p(0.15 + 0.7 * i / 3, y, 0.5) for i in range(4) for y in (0.15, 0.42)]
    return VGroup(*[Dot(p, radius=0.08, color=TERRA) for p in pts]).set_z_index(4)


def b61_ride(self, boxes, targets, rt):
    """Move the three boxes to three target centres in one play (guarded)."""
    rt = guard(self, rt)
    self.play(LaggedStart(*[b.animate.move_to(t) for b, t in zip(boxes, targets)], lag_ratio=0.15), run_time=rt)


class B61_FourSteps(Scene):
    def construct(self):
        host = b61_host()
        dev, light = gpu_block(B61_DEV)
        light.scale(1.6)
        self.add(host, dev, light, T("host", 36).move_to([-3.4, -1.7, 0]), T("device", 36).move_to([2.6, -1.7, 0]))
        until(self, "follows four steps", lead=0.1)
        self.play(Create(b61_cable()), run_time=0.5)                                                      # the cable between them
        # 1 · allocate
        until(self, "Allocate memory", lead=0.15)
        slab = b61_slab()
        self.play(GrowFromCenter(slab), run_time=0.4)
        self.play(FadeIn(M("cudaMalloc", 32).move_to([2.6, 1.95, 0]), shift=DOWN * 0.15), run_time=0.3)
        # 2 · copy in: the data boxes ride the cable host → device
        until(self, "Copy the data", lead=0.15)
        boxes = [b61_data(B61_HOST, x, y, 0.5) for x, y in B61_HOST_SPOTS]
        self.play(LaggedStart(*[GrowFromCenter(b) for b in boxes], lag_ratio=0.2), run_time=0.4)
        self.play(FadeIn(M("cudaMemcpy", 32).move_to([-0.55, 0.8, 0]), shift=DOWN * 0.15), run_time=0.3)
        ride = [np.array([x, B61_CABLE_Y + 0.2, 0.0]) for x in B61_RIDE_X]
        b61_ride(self, boxes, ride, 0.4)
        b61_ride(self, boxes, [r + RIGHT * B61_SLIDE for r in ride], 0.5)
        until(self, "CPU to GPU", lead=0.1)
        b61_ride(self, boxes, [b61_centre(B61_DEV, x, y, 0.56) for x, y in B61_SLAB_SPOTS], 0.4)
        # 3 · launch the kernel: sparks across the device
        until(self, "Launch a kernel", lead=0.1)
        self.play(FadeIn(M("kernel", 32).move_to([5.2, 0.4, 0]), shift=DOWN * 0.15), light.animate.set_color(TERRA), run_time=0.3)
        until(self, "thousands of threads", lead=0.1)
        sparks = b61_sparks()
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sparks], lag_ratio=0.06), run_time=0.6)
        until(self, "on different data", lead=0.1)
        self.play(Indicate(sparks, color=None, scale_factor=1.15), run_time=0.5)
        # 4 · copy back: the result boxes ride the cable device → host
        until(self, "Then copy the results back", lead=0.15)
        self.play(FadeIn(M("cudaMemcpy", 32).move_to([-0.55, -0.75, 0]), shift=UP * 0.15), FadeOut(sparks), light.animate.set_color(GHOST), run_time=0.3)
        self.remove(sparks)
        b61_ride(self, boxes, [r + RIGHT * B61_SLIDE for r in ride], 0.4)
        b61_ride(self, boxes, ride, 0.5)
        b61_ride(self, boxes, [b61_centre(B61_HOST, x, y, 0.5) for x, y in B61_HOST_SPOTS], 0.4)
        # host is the CPU; device is the GPU
        until(self, "Host is the CPU", lead=0.1)
        self.play(FadeIn(T("CPU", 34).move_to([-3.4, -2.25, 0]), shift=UP * 0.15), run_time=0.3)
        until(self, "device is the GPU", lead=0.1)
        self.play(FadeIn(T("GPU", 34).move_to([2.6, -2.25, 0]), shift=UP * 0.15), run_time=0.3)
        done(self)


# ─────────────── B83 · choosing the tool: eight rows, tool (mono) · memory model (icon + word) · best for ───────────────
B83_ROWS = (("OpenMP", "shared", "loop-level"),
            ("MPI", "distributed", "multi-node sims"),
            ("mpi4py", "distributed", "multi-node Python"),
            ("multiprocessing", "shared", "single-node tasks"),
            ("PyTorch DDP", "distributed", "training"),
            ("Dask / Ray", "both", "large data"),
            ("R parallel/foreach", "shared", "loops"),
            ("MATLAB parfor", "shared", "loops"))
B83_Y0, B83_DY = 2.1, 0.62                                           # first row centre, row pitch
B83_X_TOOL, B83_X_ICON, B83_X_WORD, B83_X_BEST = -6.0, -1.25, 0.75, 2.85  # left edges of the columns
B83_L, B83_R = -6.0, 6.0


def b83_y(k):
    return B83_Y0 - k * B83_DY


def b83_rule(k, sw=3):
    """The rule under row k (k = -1 is the heavier rule above the first row)."""
    return Line([B83_L, b83_y(k) - B83_DY / 2, 0], [B83_R, b83_y(k) - B83_DY / 2, 0], color=BAR1, stroke_width=sw)


def b83_cell(fn, s, size, x, y):
    """A table cell set on a common baseline: typeset with a trailing 'bp' (one ascender, one descender) so every
    cell has the same vertical extent, then the two extra glyphs are dropped."""
    try:
        full = fn(s + "bp", size).move_to([0, y, 0])
        g = VGroup(*list(full)[:len(s.replace(" ", ""))])
        if len(g) == 0:
            raise ValueError
        g.shift(RIGHT * (x - g.get_left()[0]))                      # left edge at x (the 'bp' only set the vertical extent)
        return g
    except Exception:                                                # Gate A's stub has no glyphs: plain left placement
        return pc_left(fn(s, size), x, y)


def b83_tool(k):
    return b83_cell(M, B83_ROWS[k][0], 32, B83_X_TOOL, b83_y(k))


def b83_icon(k):
    """shared → one slab; distributed → three nodes; both → the slab and the three nodes."""
    kind, y = B83_ROWS[k][1], b83_y(k)
    if kind == "shared":
        g = pc_slab(B83_X_ICON, y, w=0.6, h=0.28)
    elif kind == "distributed":
        g = pc_nodes(B83_X_ICON, y, s=0.28, gap=0.1)
    else:
        g = VGroup(pc_slab(B83_X_ICON, y, w=0.6, h=0.28), pc_nodes(B83_X_ICON + 0.76, y, s=0.28, gap=0.1))
    g.b83_icon = True
    return g


def b83_word(k):
    return b83_cell(T, B83_ROWS[k][1], 32, B83_X_WORD, b83_y(k))


def b83_best(k):
    return b83_cell(T, B83_ROWS[k][2], 32, B83_X_BEST, b83_y(k))


def b83_land(self, mobs, rt=0.4):
    """Icon + word + best-for land together."""
    anims = []
    for m in mobs:
        anims.append(GrowFromCenter(m) if getattr(m, "b83_icon", False) else FadeIn(m, shift=DOWN * 0.15))
    self.play(*anims, run_time=rt)


class B83_ToolTable(Scene):
    def construct(self):
        self.add(pc_title("VIII · Python, R, MATLAB"))
        until(self, "Choosing the tool", lead=0.0)
        self.play(Create(b83_rule(-1, 5)), run_time=0.4)
        self.play(LaggedStart(*[Create(b83_rule(k)) for k in range(8)], lag_ratio=0.12), run_time=0.8)   # eight rows open
        # OpenMP
        until(self, "OpenMP:", lead=0.15)
        self.play(FadeIn(b83_tool(0), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "shared memory,", lead=0.1)
        b83_land(self, [b83_icon(0), b83_word(0)])
        until(self, "loop-level", lead=0.1)
        b83_land(self, [b83_best(0)], 0.35)
        # MPI
        until(self, "MPI:", lead=0.15)
        self.play(FadeIn(b83_tool(1), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "distributed, multi-node", lead=0.1)
        b83_land(self, [b83_icon(1), b83_word(1), b83_best(1)])
        # mpi4py
        until(self, "mpi4py", lead=0.15)
        self.play(FadeIn(b83_tool(2), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "multi-node Python", lead=0.1)
        b83_land(self, [b83_icon(2), b83_word(2), b83_best(2)])
        # multiprocessing
        until(self, "multiprocessing", lead=0.15)
        self.play(FadeIn(b83_tool(3), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "single-node Python tasks", lead=0.1)
        b83_land(self, [b83_icon(3), b83_word(3), b83_best(3)])
        # PyTorch DDP
        until(self, "PyTorch DDP", lead=0.15)
        self.play(FadeIn(b83_tool(4), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "for training", lead=0.1)
        b83_land(self, [b83_icon(4), b83_word(4), b83_best(4)])
        # Dask / Ray
        until(self, "Dask or Ray", lead=0.15)
        self.play(FadeIn(b83_tool(5), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "big data and pipelines", lead=0.1)
        b83_land(self, [b83_best(5)], 0.35)
        until(self, "both memory models", lead=0.1)
        b83_land(self, [b83_icon(5), b83_word(5)])
        # R parallel / foreach, MATLAB parfor
        until(self, "R's parallel and foreach", lead=0.15)
        self.play(FadeIn(b83_tool(6), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "MATLAB's parfor", lead=0.1)
        self.play(FadeIn(b83_tool(7), shift=RIGHT * 0.3), run_time=0.35)
        until(self, "embarrassingly parallel loops", lead=0.1)
        b83_land(self, [b83_icon(6), b83_word(6), b83_best(6), b83_icon(7), b83_word(7), b83_best(7)], 0.45)
        done(self)


# ─────────────── B90 · four takeaways tick in order, each with its cast icon; then where to get help ───────────────
B90_ROW_Y = (1.85, 0.75, -0.35, -1.45)
B90_BOX_X = -5.4
B90_ICON_X = 0.3
B90_ITEMS = ("profile first", "choose the level", "communication costs", "plan for parallelism")


def b90_box(y):
    return Square(side_length=0.42, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([B90_BOX_X, y, 0])


def b90_tick(y):
    return check(B90_BOX_X, y - 0.02, 0.18, INK, 6)


def b90_glass(x, y):
    return VGroup(Circle(radius=0.3, color=INK, stroke_width=6).move_to([x, y, 0]),
                  Line([x + 0.22, y - 0.22, 0], [x + 0.5, y - 0.5, 0], color=INK, stroke_width=9)).set_z_index(4)


def b90_gpu(x, y, s=0.5):
    """The cast's GPU block, small, with its light."""
    body, light = gpu_block(Iso(x, y, s))
    return VGroup(body, light)


def b90_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes (edges in dark kraft, never ink)."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PC_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PC_PAD, fill_opacity=1, stroke_color=PC_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def b90_tag(cx, cy):
    """A kraft luggage tag with a hole: the cost tag (small object: dark-kraft outline, never ink)."""
    body = Polygon([cx - 0.42, cy, 0], [cx - 0.22, cy + 0.22, 0], [cx + 0.42, cy + 0.22, 0], [cx + 0.42, cy - 0.22, 0], [cx - 0.22, cy - 0.22, 0],
                   fill_color=BOX_L, fill_opacity=1, stroke_color=PC_SMALL, stroke_width=3)
    hole = Dot([cx - 0.2, cy, 0], radius=0.05, color=CARD)
    return VGroup(body, hole).set_z_index(3)


def b90_page(x, y, s=0.7):
    return Iso(x, y, s).page(0, 0, 0)


class B90_Takeaways(Scene):
    def construct(self):
        self.add(pc_title("IX · Takeaways"))
        rows = VGroup()
        for y, s in zip(B90_ROW_Y, B90_ITEMS):
            bx = b90_box(y)
            rows.add(bx, T(s, 36).next_to(bx, RIGHT, buff=0.35))
        self.play(FadeIn(rows, shift=RIGHT * 0.15), run_time=0.5)
        # 1 · profile first: the magnifier sweeps and finds the bottleneck
        until(self, "Profile first", lead=0.1)
        glass = b90_glass(B90_ICON_X, B90_ROW_Y[0] + 0.05)
        self.play(Create(b90_tick(B90_ROW_Y[0])), GrowFromCenter(glass), run_time=0.4)
        until(self, "find the bottleneck", lead=0.1)
        self.play(glass.animate.shift(RIGHT * 1.6), run_time=0.6)
        self.play(GrowFromCenter(Dot([B90_ICON_X + 1.6, B90_ROW_Y[0] + 0.05, 0], radius=0.1, color=TERRA).set_z_index(5)), run_time=0.3)
        # 2 · choose the level: one node, three nodes, a GPU block, in a row
        until(self, "Choose the level", lead=0.1)
        self.play(Create(b90_tick(B90_ROW_Y[1])), run_time=0.3)
        until(self, "shared memory on one node", lead=0.1)
        self.play(GrowFromCenter(pc_slab(B90_ICON_X - 0.2, B90_ROW_Y[1], w=0.9, h=0.4)), run_time=0.35)
        until(self, "MPI across nodes", lead=0.1)
        self.play(GrowFromCenter(pc_nodes(B90_ICON_X + 1.2, B90_ROW_Y[1], s=0.4, gap=0.14)), run_time=0.35)
        until(self, "GPUs for data-parallel", lead=0.1)
        pc_drop(self, [b90_gpu(B90_ICON_X + 3.9, B90_ROW_Y[1] - 0.45)], rt=0.4, dist=3.0)
        # 3 · communication costs: a belt with a cost tag riding it
        until(self, "Communication costs", lead=0.1)
        belt = b90_belt(B90_ICON_X - 0.2, B90_ICON_X + 4.2, B90_ROW_Y[2] - 0.2)
        tag = b90_tag(B90_ICON_X + 0.6, B90_ROW_Y[2] + 0.22)
        self.play(Create(b90_tick(B90_ROW_Y[2])), FadeIn(belt), run_time=0.4)
        self.play(GrowFromCenter(tag), run_time=0.3)
        until(self, "more nodes are not always faster", lead=0.1)
        self.play(tag.animate.shift(RIGHT * 2.6), run_time=0.8)
        # 4 · plan for parallelism: a planning page lands
        until(self, "And plan for parallelism", lead=0.1)
        pc_drop(self, [b90_page(B90_ICON_X + 0.1, B90_ROW_Y[3] - 0.45)], rt=0.45, dist=3.0, with_=[Create(b90_tick(B90_ROW_Y[3]))])
        # questions: the help address
        until(self, "Questions", lead=0.2)
        self.play(FadeIn(M("rchelp@northeastern.edu", 34).move_to([0.0, -2.6, 0]), shift=UP * 0.15), run_time=0.5)
        done(self)
