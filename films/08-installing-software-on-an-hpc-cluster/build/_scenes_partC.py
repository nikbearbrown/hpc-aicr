# ═════════════════════════════ PART C · B63 (Act VI) · B70 (Act VII) · B80, B81 (Act VIII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PC8_ / pc8_ / b63_ / b70_ / b80_ / b81_ so the parts never collide.
PC8_LINK = "#9C8462"                        # deep kraft: connectors and arrows (ink lines fuse the things they join, GATE T)
PC8_SMALL = "#917A55"                       # dark kraft: outlines of SMALL objects only (GATE T)


def pc8_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pc8_left(mob, x, y):
    """Place a text by its LEFT edge, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pc8_right(mob, x, y):
    """Place a text by its RIGHT edge, centred on y."""
    return mob.move_to([x - mob.width / 2, y, 0])


def pc8_arrow(a, b, color=PC8_LINK, sw=4):
    """A connector arrow in deep kraft, grey tip."""
    a, b = np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0])
    return Arrow(a, b, buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.18, max_stroke_width_to_length_ratio=20)


def pc8_xmark(x, y, s=0.35, color=BAR1, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w)).set_z_index(8)


def pc8_person(x, y, s=1.0):
    """A person token standing with its feet at (x, y): grey body, ink outline (the same token as the earlier films)."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head).set_z_index(7)


def pc8_drop(self, mobs, rt=0.5, lag=0.2, dist=4.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt, rate_func=ease_in)


def pc8_page(cx, cy, w=0.8, h=0.9):
    """A flat file page: white card, grey outline, three ghost lines (a small object: grey outline, GATE T)."""
    card = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([cx, cy, 0])
    lines = VGroup(*[Line([cx - w * 0.3, cy + h * (0.25 - 0.22 * k), 0], [cx + w * 0.3, cy + h * (0.25 - 0.22 * k), 0],
                          color=GHOST, stroke_width=4) for k in range(3)])
    return VGroup(card, lines)


# ─────────────── B63 · the module tree: name and version, three commands, switch, loads others, the default ───────────────
B63_ROWS = (("$HOME/modulefiles/", -6.0, 2.5), ("mytool/", -5.0, 1.7), ("1.0", -4.0, 0.9), ("2.0", -4.0, 0.1),
            ("otherlib/", -5.0, -0.7), ("3.4", -4.0, -1.5))
B63_CMD_X, B63_CMD_Y = -0.65, (2.5, 1.75, 1.0)
B63_CMDS = ("module avail mytool", "module load mytool/1.0", "module unload mytool/1.0")
B63_CHECK_X = 5.85
B63_ANN_X = -2.85                                                        # the bracket column; its label starts 0.3 to the right
B63_CW = 8.46 / 34 * 32 / 34                                             # Menlo at 32: screen units per character (measured at 34, scaled)
B63_PAGE = (0.5, -1.45)                                                 # the mytool/2.0 file page
B63_VPAGE = (4.3, -1.45)                                                # the .version page


def b63_tree_lines():
    """Deep-kraft tree connectors: one trunk per directory, a tick to each child, stopping 0.35 clear of the text."""
    g = VGroup()
    # root trunk: under "$HOME/modulefiles/", down past otherlib/
    g.add(Line([-5.75, 2.1, 0], [-5.75, -0.7, 0], color=PC8_LINK, stroke_width=4))
    for y in (1.7, -0.7):
        g.add(Line([-5.75, y, 0], [-5.35, y, 0], color=PC8_LINK, stroke_width=4))
    # mytool/ trunk to 1.0 and 2.0
    g.add(Line([-4.75, 1.35, 0], [-4.75, 0.1, 0], color=PC8_LINK, stroke_width=4))
    for y in (0.9, 0.1):
        g.add(Line([-4.75, y, 0], [-4.35, y, 0], color=PC8_LINK, stroke_width=4))
    # otherlib/ trunk to 3.4
    g.add(Line([-4.75, -1.05, 0], [-4.75, -1.5, 0], color=PC8_LINK, stroke_width=4))
    g.add(Line([-4.75, -1.5, 0], [-4.35, -1.5, 0], color=PC8_LINK, stroke_width=4))
    return g


def b63_row(k):
    s, x, y = B63_ROWS[k]
    return pc8_left(M(s, 32), x, y)


def b63_bracket(y):
    """A grey bracket beside a tree row: a short vertical bar with two ticks (grey: never an ink line inside text)."""
    x = B63_ANN_X
    return VGroup(Line([x, y - 0.26, 0], [x, y + 0.26, 0], color=BAR1, stroke_width=4),
                  Line([x - 0.12, y - 0.26, 0], [x, y - 0.26, 0], color=BAR1, stroke_width=4),
                  Line([x - 0.12, y + 0.26, 0], [x, y + 0.26, 0], color=BAR1, stroke_width=4))


def b63_ring(k):
    """A grey ring around tree row k (an editor's ring around a label, by design)."""
    s, x, y = B63_ROWS[k]
    w = len(s) * B63_CW
    ring = Ellipse(width=w + 0.3, height=0.6, color=BAR1, stroke_width=4).move_to([x + w / 2, y, 0])
    ring._qc_intentional = True
    return ring


class B63_PersonalModuleStack(Scene):
    def construct(self):
        # the tree draws in: connectors, then every row
        lines = b63_tree_lines()
        rows = [b63_row(k) for k in range(6)]
        self.play(Create(lines), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.15), run_time=0.6)
        # directory name = module name; file name = version
        until(self, "directory name", lead=0.15)
        self.play(Create(b63_bracket(1.7)), FadeIn(pc8_left(T("name", 32), B63_ANN_X + 0.3, 1.7)), run_time=0.35)
        until(self, "file name becomes", lead=0.15)
        self.play(Create(b63_bracket(0.9)), FadeIn(pc8_left(T("version", 32), B63_ANN_X + 0.3, 0.9)), run_time=0.35)
        # the three commands land in turn, each with a check
        for cue, k in (("module avail", 0), ("module load", 1), ("unload reverses", 2)):
            until(self, cue, lead=0.15)
            self.play(FadeIn(pc8_left(M(B63_CMDS[k], 32), B63_CMD_X, B63_CMD_Y[k]), shift=RIGHT * 0.2), run_time=0.3)
            self.play(Create(check(B63_CHECK_X, B63_CMD_Y[k], 0.18)), run_time=0.25)
        # a personal stack: each tool its own subdirectory, each version a file, switch with one load
        until(self, "each tool its own", lead=0.15)
        ring = b63_ring(1)
        self.play(Create(ring), run_time=0.3)
        until(self, "each version a file", lead=0.15)
        self.play(Transform(ring, b63_ring(2)), run_time=0.4)                      # ellipse to ellipse: it travels, it does not crumple
        until(self, "switch with one load", lead=0.2)
        self.play(Transform(ring, b63_ring(3)), run_time=0.4)
        self.play(FadeIn(pc8_left(T("switch", 32), B63_ANN_X + 0.3, 0.1), shift=RIGHT * 0.1), run_time=0.25)
        # a module file can load other modules: the mytool/2.0 page with a gcc pill hanging under it
        until(self, "can load other modules", lead=0.3)
        px, py = B63_PAGE
        page = pc8_page(px, py)
        pc8_drop(self, [page], rt=0.45, dist=3.0, with_=[FadeIn(M("mytool/2.0", 32).move_to([px, -0.5, 0]))])
        until(self, "such as the right", lead=0.1)
        hang = Line([px, py - 0.5, 0], [px, -2.44, 0], color=PC8_LINK, stroke_width=4)
        gcc = VGroup(pill(px, -2.8, 1.15, 0.62, CARD), M("gcc", 32).move_to([px, -2.8, 0]))
        self.play(Create(hang), GrowFromCenter(gcc), FadeIn(pc8_left(T("loads others", 32), px + 0.8, -2.8)), run_time=0.4)
        # a .version file names the default
        until(self, "dot version file", lead=0.2)
        vx, vy = B63_VPAGE
        vpage = pc8_page(vx, vy)
        pc8_drop(self, [vpage], rt=0.45, dist=3.0, with_=[FadeIn(M(".version", 32).move_to([vx, -0.5, 0]))])
        until(self, "names the default", lead=0.1)
        self.play(Create(pc8_arrow([vx - 0.45, vy], [px + 0.5, vy])),
                  FadeIn(T("default", 32).move_to([vx, -2.8, 0]), shift=UP * 0.1), run_time=0.4)
        done(self)


# ─────────────── B70 · the .sif stacks up; Docker needs root (X); Apptainer runs as you (check); GPU and MPI; pulls docker:// ───────────────
B70_STACK = Iso(-2.6, -1.6, 0.75)
B70_SLABS = ("OS layer", "libraries", "application")
B70_LABEL_X = -3.9                                                      # right edge of the slab labels (the stack's left edge is -3.57)
B70_KEY = (2.3, -2.1)                                                   # the root key's ring centre


def b70_slab(k):
    fills = ((BOX_TOP, BOX_L, BOX_R), (BOX_TOP, BOX_L, BOX_R), (PAGE_TOP, PAGE_L, PAGE_R))
    return B70_STACK.box(0, 0, 1.0 * k, 2.0, 1.5, 0.95, *fills[k])


def b70_slab_label(k):
    """The slab's label, right-aligned left of the stack, on the slab's front-left face centre line."""
    return pc8_right(T(B70_SLABS[k], 32), B70_LABEL_X, -0.96 + 0.75 * k)


def b70_key():
    """A root key: ink-outlined kraft ring and shaft with two teeth (drawn large: tiny icons read as sub-floor text)."""
    x, y = B70_KEY
    ring = Circle(radius=0.32, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    hole = Circle(radius=0.1, fill_color=STAGE, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y, 0])
    shaft = Rectangle(width=1.0, height=0.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x + 0.8, y, 0])
    teeth = VGroup(*[Rectangle(width=0.14, height=0.22, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=3)
                     .move_to([x + 1.2 - 0.26 * k, y - 0.2, 0]) for k in range(2)])
    return VGroup(shaft, teeth, ring, hole)


class B70_ApptainerVsDocker(Scene):
    def construct(self):
        self.add(pc8_title("VII · Apptainer"))
        # the image stacks: OS layer first, then libraries and the application on top
        slabs = [b70_slab(k) for k in range(3)]
        labels = [b70_slab_label(k) for k in range(3)]
        pc8_drop(self, [slabs[0]], rt=0.5, dist=3.0, with_=[FadeIn(labels[0])])
        until(self, "packs an application", lead=0.2)
        pc8_drop(self, [slabs[1], slabs[2]], rt=0.6, lag=0.35, dist=3.0, with_=[FadeIn(labels[1]), FadeIn(labels[2])])
        until(self, "a dot S I F", lead=0.15)
        self.play(FadeIn(M(".sif", 34).move_to([-0.3, 2.1, 0]), shift=DOWN * 0.15), run_time=0.3)
        # why not Docker: the root key, crossed out
        until(self, "Why not Docker", lead=0.15)
        self.play(Create(pc8_arrow([-0.8, -0.9], [1.4, -1.9])), run_time=0.35)
        self.play(GrowFromCenter(b70_key()), FadeIn(pc8_left(M("root", 32), 3.9, -2.1)), run_time=0.35)
        until(self, "needs root to run", lead=0.1)
        self.play(Create(pc8_xmark(2.8, -2.1, 0.42)), run_time=0.3)
        until(self, "a security problem", lead=0.15)
        self.play(FadeIn(T("Docker needs root", 32).move_to([3.3, -2.95, 0]), shift=UP * 0.1), run_time=0.3)
        # Apptainer runs as you
        until(self, "runs a container as you", lead=0.2)
        self.play(Create(pc8_arrow([-0.8, 0.3], [1.4, 1.1])), run_time=0.35)
        self.play(GrowFromCenter(pc8_person(2.3, 0.75)), run_time=0.3)
        until(self, "no elevated privileges", lead=0.1)
        self.play(Create(check(3.3, 1.2, 0.2)), FadeIn(T("runs as you", 32).move_to([2.8, 2.35, 0]), shift=UP * 0.1), run_time=0.35)
        # GPU and MPI workloads: the cast GPU block, its light goes busy
        until(self, "runs G P U", lead=0.2)
        body, light = gpu_block(Iso(4.4, 0.5, 0.55))
        pc8_drop(self, [VGroup(body, light)], rt=0.4, dist=2.5, with_=[FadeIn(T("GPU · MPI", 32).move_to([4.9, -0.15, 0]))])
        until(self, "M P I workloads", lead=0.1)
        self.play(light.animate.set_color(TERRA), run_time=0.25)
        # pulls and converts Docker images
        until(self, "pull and convert", lead=0.2)
        self.play(FadeIn(M("docker://", 32).move_to([-4.9, -2.6, 0]), shift=RIGHT * 0.15), run_time=0.3)
        self.play(Create(pc8_arrow([-3.45, -2.6], [-2.75, -2.0])),
                  FadeIn(T("pulls Docker images", 32).move_to([-0.9, -2.9, 0]), shift=UP * 0.1), run_time=0.4)
        done(self)


# ─────────────── B80 · six tools, one table: root? · from source? · best for · drawback ───────────────
B80_HY, B80_ROW_Y = 2.2, (1.45, 0.7, -0.05, -0.8, -1.55, -2.3)
B80_TOOL_X, B80_PILL_X, B80_SRC_X, B80_BEST_X, B80_DRAW_X = -6.0, -3.4, -2.45, 0.05, 2.7
B80_TOOLS = ("modules", "Conda", "Spack", "EasyBuild", "source", "Apptainer")
B80_SRC = ("no", "no", "yes", "yes", "yes", "image")
B80_BEST = ("already there", "Python, R", "variants", "toolchains", "patches", "portability")
B80_DRAW = ("admins only", "quota", "heavy", "toolchain-bound", "manual", "build locally")
B80_CUES = (("Environment modules", "best for what the cluster", "limited to what admins"),
            ("Conda:", "best for Python", "heavy on quota"),
            ("Spack:", "source-level control", "heavy and slow"),
            ("EasyBuild:", "reproducible toolchain", "mostly an admin tool"),
            ("A source install", "patches and niche", "the most manual"),
            ("App-tainer:", "for hard dependencies", "built locally"))


def b80_rule(y, sw=3):
    """A grey rule between rows (table dividers never ink)."""
    return Line([-6.1, y, 0], [6.1, y, 0], color=BAR1, stroke_width=sw)


def b80_no_pill(y):
    return VGroup(pill(B80_PILL_X, y, 0.95, 0.56, GHOST), T("no", 32).move_to([B80_PILL_X, y, 0]))


class B80_SixToolsTable(Scene):
    def construct(self):
        self.add(pc8_title("VIII · Choosing The Tool"))
        head = VGroup(pc8_left(T("tool", 32, bold=True), B80_TOOL_X, B80_HY),
                      T("root?", 32, bold=True).move_to([B80_PILL_X, B80_HY, 0]),
                      pc8_left(T("from source?", 32, bold=True), B80_SRC_X, B80_HY),
                      pc8_left(T("best for", 32, bold=True), B80_BEST_X, B80_HY),
                      pc8_left(T("drawback", 32, bold=True), B80_DRAW_X, B80_HY))
        rules = VGroup(b80_rule(B80_HY - 0.4, 5), *[b80_rule(y - 0.375) for y in B80_ROW_Y[:-1]])
        self.play(FadeIn(head), run_time=0.35)
        self.play(Create(rules), run_time=0.45)
        # none needs root: six grey "no" pills at once
        until(self, "none needs root", lead=0.15)
        self.play(LaggedStart(*[GrowFromCenter(b80_no_pill(y)) for y in B80_ROW_Y], lag_ratio=0.1), run_time=0.5)
        # each row lands one cell at a time, on its words
        for k, (c_tool, c_best, c_draw) in enumerate(B80_CUES):
            y = B80_ROW_Y[k]
            until(self, c_tool, lead=0.1)
            self.play(FadeIn(pc8_left(T(B80_TOOLS[k], 32), B80_TOOL_X, y), shift=RIGHT * 0.2),
                      FadeIn(pc8_left(T(B80_SRC[k], 32), B80_SRC_X, y), shift=RIGHT * 0.2), run_time=0.3)
            until(self, c_best, lead=0.1)
            self.play(FadeIn(pc8_left(T(B80_BEST[k], 32), B80_BEST_X, y), shift=RIGHT * 0.2), run_time=0.25)
            until(self, c_draw, lead=0.1)
            self.play(FadeIn(pc8_left(T(B80_DRAW[k], 32), B80_DRAW_X, y), shift=RIGHT * 0.2), run_time=0.25)
        done(self)


# ─────────────── B81 · the practical order: five questions, yes → a tool, no ↓ the next question; then ask RC ───────────────
B81_ROW_Y = (2.45, 1.35, 0.25, -0.85, -1.95)
B81_Q_X, B81_Q_W = -3.25, 4.3                                           # question pills: -5.4 .. -1.1
B81_T_X, B81_T_W = 2.75, 3.7                                            # tool pills: 0.9 .. 4.6
B81_NUM_X = -5.85
B81_DOT = (5.05, 2.45)                                                  # the start-here dot, beside row 1's tool pill
B81_QS = ("a module?", "Python or R?", "portable or fragile?", "patch or flag?", "compiler, MPI, variants?")
B81_TOOLS = ("modules", "Conda", "Apptainer", "from source", "Spack or EasyBuild")
B81_ASK_Y = -2.85


def b81_qpill(k):
    y = B81_ROW_Y[k]
    return VGroup(pill(B81_Q_X, y, B81_Q_W, 0.62, CARD), T(B81_QS[k], 32).move_to([B81_Q_X, y, 0]))


def b81_tpill(k):
    y = B81_ROW_Y[k]
    return VGroup(pill(B81_T_X, y, B81_T_W, 0.62, GHOST if k == 4 else CARD), T(B81_TOOLS[k], 32).move_to([B81_T_X, y, 0]))


def b81_yes(k):
    y = B81_ROW_Y[k]
    return pc8_arrow([B81_Q_X + B81_Q_W / 2 + 0.15, y], [B81_T_X - B81_T_W / 2 - 0.1, y])


def b81_no(k):
    """The 'no' arrow from question k down to question k+1 (or to the ask pill)."""
    y0 = B81_ROW_Y[k] - 0.31 - 0.05
    y1 = (B81_ROW_Y[k + 1] if k < 4 else B81_ASK_Y) + 0.31 + 0.05
    return pc8_arrow([B81_Q_X, y0], [B81_Q_X, y1])


def b81_weight():
    """A kettlebell beside the grey pill: willing to maintain it (ink outline, drawn large)."""
    x, y = 5.5, B81_ROW_Y[4]
    ball = Circle(radius=0.3, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y - 0.12, 0])
    handle = Arc(radius=0.22, start_angle=0, angle=PI, arc_center=np.array([x, y + 0.1, 0.0]), color=INK, stroke_width=6)
    return VGroup(handle, ball)


class B81_DecisionOrder(Scene):
    def construct(self):
        heads = VGroup(T("no", 32).move_to([B81_Q_X, 3.0, 0]), T("yes", 32).move_to([(B81_Q_X + B81_Q_W / 2 + B81_T_X - B81_T_W / 2) / 2, 3.0, 0]))
        self.play(FadeIn(heads), run_time=0.3)
        cues = (("One: check for a module", "the best install is no install"),
                ("Two: a Python", "Conda, with the quota"),
                ("Three: isolated", "Build a container"),
                ("Four: a patch", "Build from source"),
                ("Five: source-level", "Then, and mostly then"))
        for k, (c_q, c_t) in enumerate(cues):
            until(self, c_q, lead=0.15)
            anims = [GrowFromCenter(b81_qpill(k)), FadeIn(T(str(k + 1), 36).move_to([B81_NUM_X, B81_ROW_Y[k], 0]))]
            if k > 0:
                anims.append(Create(b81_no(k - 1)))
            self.play(*anims, run_time=0.35)
            if k == 0:
                self.play(GrowFromCenter(Dot([*B81_DOT, 0], radius=0.09, color=TERRA)), run_time=0.2)   # start here
            until(self, c_t, lead=0.15)
            tool = [Create(b81_yes(k)), GrowFromCenter(b81_tpill(k))]
            if k == 4:
                tool.append(GrowFromCenter(b81_weight()))
            self.play(*tool, run_time=0.4)
        # none of that fits: ask Research Computing
        until(self, "ask the Research Computing", lead=0.3)
        ask = VGroup(pill(B81_Q_X, B81_ASK_Y, B81_Q_W, 0.62, GHOST), T("ask Research Computing", 32).move_to([B81_Q_X, B81_ASK_Y, 0]))
        self.play(Create(b81_no(4)), GrowFromCenter(ask), run_time=0.4)
        done(self)
