# ═════════════════════════════ PART A · B10, B11 (Act I) · B21 (Act II) · B31 (Act III) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PA_ / pa_ / b1x_ / b2x_ / b3x_ so the parts never collide.
PA_KRAFT = "#9C8462"                        # deep kraft: connectors and network lines (ink lines fuse the things they join, GATE T)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T)


def pa_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_left(mob, x, y):
    """Place a text by its LEFT edge, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pa_token(x, y, s=1.0):
    """A person token standing with its feet at (x, y) (the same token as the earlier films)."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head).set_z_index(7)


def pa_xmark(x, y, s=0.35, color=BAR1, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w)).set_z_index(8)


def pa_plinth(iso, w, d, m=0.15, h=0.1):
    """A thin dark plinth under a pale container (Gate V contrast): its top is the floor (z = 0)."""
    return iso.box(-m, -m, -h, w + 2 * m, d + 2 * m, h, DARK_TOP, DARK_L, DARK_R).set_z_index(-1)


def pa_drop(self, mobs, rt=0.55, lag=0.2, dist=5.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt, rate_func=ease_in)


def pa_slide_in(self, mob, vec, rt=0.7, with_=()):
    """Slide a whole object in from off-stage, fully opaque."""
    rt = guard(self, rt)
    mob.shift(-vec)
    self.add(mob)
    self.play(mob.animate.shift(vec), *with_, run_time=rt)


def pa_gauge(x, y, w=0.4, h=1.4, n=5):
    """A quota gauge: a grey outline and n grey segments (with gaps) stacked from the bottom. Returns (outline, segments)."""
    out = Rectangle(width=w, height=h, stroke_color=BAR1, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    gap, sh = 0.06, (h - 0.06 * (n + 1)) / n
    segs = VGroup(*[Rectangle(width=w - 0.12, height=sh, fill_color=BAR1, fill_opacity=1, stroke_width=0)
                    .move_to([x, y - h / 2 + gap + sh / 2 + k * (sh + gap), 0]) for k in range(n)])
    return out, segs


def pa_fill(self, segs, k0, k1, rt=0.6):
    """Raise the gauge from segment k0 to k1 (exclusive), one segment after another."""
    rt = guard(self, rt)
    self.play(LaggedStart(*[GrowFromEdge(segs[k], DOWN) for k in range(k0, k1)], lag_ratio=0.35), run_time=rt)


def pa_env_box(iso, s=0.6, outline=PA_SMALL):
    """A conda environment / generic binary: a small white box (small object, dark-kraft outline)."""
    return iso.box(0, 0, 0, s, s, s * 0.75, PAGE_TOP, PAGE_L, PAGE_R, sw=3).set_stroke(outline)


def pa_file_dots(n, x0, x1, y0, y1, seed=7, r=0.045):
    rng = np.random.RandomState(seed)
    return VGroup(*[Dot([rng.uniform(x0, x1), rng.uniform(y0, y1), 0], radius=r, color=BAR1) for _ in range(n)])


def pa_pour(self, dots, iso, x0, y0, w, d, z, rt=1.0, seed=3):
    """The file dots pour onto a box top (a random point each on the top face) and shrink away."""
    rt = guard(self, rt)
    rng = np.random.RandomState(seed)
    self.add(dots)
    self.play(LaggedStart(*[dd.animate.move_to(iso.p(x0 + rng.uniform(0.1, w - 0.1), y0 + rng.uniform(0.1, d - 0.1), z)).scale(0.2)
                            for dd in dots], lag_ratio=0.04), run_time=rt, rate_func=ease_in)
    self.remove(dots, *dots)


# ─────────────── B10 · laptop vs cluster: two columns, row by row ───────────────
B10_LAP = Iso(-5.3, -1.6, 0.75)                                   # the laptop, far left
B10_RACK = Iso(0.15, -1.9, 0.75)                                 # the Explorer rack, between the columns
B10_ROWS_Y = (0.95, 0.15, -0.65, -1.45)
B10_XL, B10_XR = -3.9, 1.5                                       # left edge of each label column
B10_LEFT = ("root", "one user", "local disk", "generic binaries")
B10_RIGHT = ("user space only", "hundreds of users", "shared filesystem, quota", "match cluster libraries")


def b10_laptop():
    """A small laptop: a kraft base, a dark screen standing on its back edge."""
    iso = B10_LAP
    screen = iso.quad([(0.1, 1.3, 0.1), (1.5, 1.3, 0.1), (1.5, 1.3, 1.15), (0.1, 1.3, 1.15)], DARK_L, sw=4)
    base = iso.box(0, 0, 0, 1.6, 1.3, 0.1)
    keys = iso.quad([(0.25, 0.3, 0.1), (1.35, 0.3, 0.1), (1.35, 0.9, 0.1), (0.25, 0.9, 0.1)], GHOST, sw=0)
    return VGroup(screen, base, keys)


B10_WL, B10_WR = (0.82, 1.55, 1.7, 2.83), (2.77, 3.27, 4.4, 4.0)       # measured label widths (fixed centres: Gate A's stub over-estimates text width)


def b10_row(k, left=True):
    x, w = (B10_XL, B10_WL[k]) if left else (B10_XR, B10_WR[k])
    return T(B10_LEFT[k] if left else B10_RIGHT[k], 36).move_to([x + w / 2, B10_ROWS_Y[k], 0])


def b10_binary():
    """The generic binary, born on the laptop's base."""
    return pa_env_box(Iso(B10_LAP.ox, B10_LAP.oy, 0.75), s=0.7).shift(B10_LAP.v(0.45, 0.3, 0.1))


class B10_LaptopVsCluster(Scene):
    def construct(self):
        self.add(pa_title("I · Why HPC Is Different"), b10_laptop())
        until(self, "root access")
        self.play(FadeIn(b10_row(0), shift=DOWN * 0.3), run_time=0.3)
        until(self, "one user")
        self.play(FadeIn(b10_row(1), shift=DOWN * 0.3), run_time=0.3)
        until(self, "a local disk")
        self.play(FadeIn(b10_row(2), shift=DOWN * 0.3), run_time=0.3)
        until(self, "and generic downloads")
        self.play(FadeIn(b10_row(3), shift=DOWN * 0.3), run_time=0.3)
        until(self, "The cluster:")
        st, li = explorer_rack(B10_RACK)
        pa_slide_in(self, VGroup(st, li), LEFT * 7.0, 0.6)
        until(self, "user space only")
        self.play(FadeIn(b10_row(0, False), shift=DOWN * 0.3), run_time=0.3)
        until(self, "hundreds of people")
        self.play(FadeIn(b10_row(1, False), shift=DOWN * 0.3), run_time=0.3)
        until(self, "a network filesystem")
        self.play(FadeIn(b10_row(2, False), shift=DOWN * 0.3), run_time=0.3)
        until(self, "and builds that should link")
        self.play(FadeIn(b10_row(3, False), shift=DOWN * 0.3), run_time=0.3)
        until(self, "own compilers")
        self.play(LaggedStart(*[l.animate.set_color(TERRA) for l in li], lag_ratio=0.3), run_time=0.5)
        until(self, "A generic binary from")
        bn = b10_binary()
        self.play(GrowFromCenter(bn), run_time=0.4)
        until(self, "ignores all of that", lead=0.4)
        top = B10_RACK.p(0.65, 0.65, 0.92)
        self.play(bn.animate.move_to([top[0], top[1] + 0.3, 0]), run_time=0.9)
        until(self, "so it runs slower")
        self.play(Create(pa_xmark(top[0], top[1] + 0.3, 0.5)), run_time=0.35)
        done(self)


# ─────────────── B11 · do not build on the login node; mind the filesystem ───────────────
B11_RACK = Iso(-5.0, -1.55, 0.7)                                  # the login node, left
B11_JOB = Iso(-2.3, -2.95, 0.75)                                  # the job box, lower left
B11_TOK_Y, B11_TOK_X = -1.35, (-3.7, -3.2, -2.7, -2.2, -1.7)      # five people beside the node
B11_HOME = Iso(2.6, 0.7, 0.7)                                     # the home box, upper right
B11_NODES_X, B11_NODE_Y = (1.1, 2.7, 4.3), -2.6                  # three small nodes under it
B11_NET_Y = -0.75                                                 # the network line
B11_CLOCK = np.array([5.55, -2.05, 0.0])


def b11_build_glyph(c):
    """The build: a gear with a hammer across it. Small object, dark-kraft outlines."""
    cx, cy = c[0], c[1]
    r = 0.3
    teeth = VGroup(*[Square(side_length=r * 0.38, fill_color=BAR2, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=2)
                     .move_to([cx + r * np.cos(a), cy + r * np.sin(a), 0]).rotate(a) for a in np.arange(0, 2 * PI, PI / 4)])
    ring = Circle(radius=r, fill_color=BAR2, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([cx, cy, 0])
    hub = Circle(radius=r * 0.32, fill_color=STAGE, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([cx, cy, 0])
    handle = Line([cx - 0.05, cy - 0.05, 0], [cx + 0.5, cy + 0.5, 0], color=PA_SMALL, stroke_width=7)
    head = Rectangle(width=0.36, height=0.2, fill_color=BAR1, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([cx + 0.5, cy + 0.5, 0]).rotate(PI / 4)
    return VGroup(teeth, ring, hub, handle, head).set_z_index(9)


def b11_node(x):
    return Iso(x, B11_NODE_Y, 0.6).box(0, 0, 0, 0.9, 0.9, 0.42, DARK_TOP, DARK_L, DARK_R)


def b11_net():
    """The network: a kraft trunk line with a drop from the home box and a riser to each node."""
    hb = B11_HOME.p(0.6, 0.6, 0)
    trunk = Line([0.7, B11_NET_Y, 0], [5.0, B11_NET_Y, 0], color=PA_KRAFT, stroke_width=5)
    drop = Line([hb[0], hb[1] - 0.1, 0], [hb[0], B11_NET_Y, 0], color=PA_KRAFT, stroke_width=5)
    tops = [Iso(x, B11_NODE_Y, 0.6).p(0.45, 0.45, 0.42) for x in B11_NODES_X]
    risers = VGroup(*[Line([tp[0], B11_NET_Y, 0], tp, color=PA_KRAFT, stroke_width=5) for tp in tops])
    return VGroup(trunk, drop, risers).set_z_index(-2)


def b11_clock(c, r=0.45):
    """A clock: white face, dark-kraft ring, grey hands (never ink inside an outline)."""
    face = Circle(radius=r, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=5).move_to(c)
    hands = VGroup(Line(c, c + np.array([0, r * 0.7, 0]), color=BAR1, stroke_width=6),
                   Line(c, c + np.array([r * 0.5, 0, 0]), color=BAR1, stroke_width=6))
    return VGroup(face, hands)


class B11_LoginNodeAndFilesystem(Scene):
    def construct(self):
        st, li = explorer_rack(B11_RACK)
        self.add(st, li, T("login node", 36).move_to([-5.0, -2.1, 0]))
        until(self, "do not build")
        rt = B11_RACK.p(0.65, 0.65, 0.88)
        glyph = b11_build_glyph(rt + np.array([0, 0.3, 0]))
        pa_drop(self, [glyph], 0.5, dist=4.0)
        until(self, "Everyone who is connected")
        toks = VGroup(*[pa_token(x, B11_TOK_Y, 0.75) for x in B11_TOK_X])
        self.play(LaggedStart(*[GrowFromCenter(t) for t in toks], lag_ratio=0.2), run_time=0.7)
        until(self, "a long compile")
        self.play(Rotate(glyph[0], angle=PI / 2), run_time=0.8)
        until(self, "slows the system")
        self.play(toks.animate.set_fill(BAR3).set_stroke(BAR2), run_time=0.5)
        until(self, "Heavy builds go into")
        job = job_box(B11_JOB)
        pa_drop(self, [job], 0.5, dist=4.0)
        self.add(T("job", 36).move_to([-1.3, -2.55, 0]))
        a = np.array(glyph.get_center())
        b = B11_JOB.p(0.35, 0.35, 0.56) + np.array([0, 0.3, 0])
        self.play(MoveAlongPath(glyph, ArcBetweenPoints(a, b, angle=PI / 3)), run_time=0.8)
        until(self, "or a batch job")
        self.play(toks.animate.set_fill(BAR1).set_stroke(INK), run_time=0.4)
        until(self, "Second, mind")
        home = VGroup(pa_plinth(B11_HOME, 1.2, 1.2), home_box(B11_HOME))
        pa_slide_in(self, home, LEFT * 5.5, 0.6)
        self.add(T("home", 36).move_to([1.05, 1.45, 0]))
        until(self, "is a network filesystem")
        net = b11_net()
        nodes = VGroup(*[b11_node(x) for x in B11_NODES_X])
        self.play(Create(net), run_time=0.6)
        pa_drop(self, nodes, 0.6, lag=0.25, dist=4.0)
        until(self, "shared across every node")
        self.play(FadeIn(T("every node", 36).move_to([2.7, -3.08, 0]), shift=UP * 0.2), run_time=0.3)
        until(self, "Quotas are tight")
        out, segs = pa_gauge(4.3, 1.45)
        self.play(Create(out), FadeIn(T("quota", 36).move_to([5.25, 1.45, 0])), run_time=0.4)
        pa_fill(self, segs, 0, 3, 0.5)
        until(self, "the tens of thousands")
        dots = pa_file_dots(36, 1.4, 3.9, 2.2, 3.2)
        self.play(FadeIn(T("tens of thousands", 36).move_to([2.9, 2.7, 0]), shift=DOWN * 0.2), run_time=0.3)
        pa_pour(self, dots, B11_HOME, 0, 0, 1.2, 1.2, 0.9, 1.0)
        pa_fill(self, segs, 3, 5, 0.4)
        until(self, "That is a real reason")
        clock = b11_clock(B11_CLOCK, 0.42)
        self.play(GrowFromCenter(clock), run_time=0.4)
        self.add(T("slow", 36).move_to([5.55, -3.08, 0]))
        until(self, "job launches are slow")
        self.play(Rotate(clock[1], angle=-PI / 2, about_point=B11_CLOCK), clock[0].animate.scale(1.25), run_time=0.6)
        done(self)


# ─────────────── B21 · what module load does: PATH gains a directory in front ───────────────
B21_PANEL = (-1.9, -0.35, 8.4, 3.3)                              # dark shell panel: centre x, centre y, width, height
B21_PROMPT_Y, B21_PATH_Y = 0.55, -0.5
B21_PKG = Iso(4.6, -1.6, 0.75)                                   # the admin's package box, right
B21_SLOT_X = -4.2                                                # where the package-dir pill lands (left edge) inside PATH


def b21_panel():
    return Rectangle(width=B21_PANEL[2], height=B21_PANEL[3], fill_color=DARK_L, fill_opacity=1, stroke_color=DARK_R, stroke_width=4)\
        .move_to([B21_PANEL[0], B21_PANEL[1], 0]).set_z_index(-3)


def b21_light(s, x, y, size=34):
    return pa_left(M(s, size, GHOST), x, y)


def b21_pill(s, x, y, w):
    """A kraft pill (no outline) with ink mono text, left edge at x."""
    p = RoundedRectangle(width=w, height=0.6, corner_radius=0.3, fill_color=BOX_TOP, fill_opacity=1, stroke_width=0).move_to([x + w / 2, y, 0])
    return VGroup(p, M(s, 32).move_to([x + w / 2, y, 0])).set_z_index(3)


class B21_WhatModuleLoadDoes(Scene):
    def construct(self):
        self.add(b21_panel())
        path = b21_light("PATH=/usr/bin", -5.85, B21_PATH_Y)
        self.play(FadeIn(path, shift=RIGHT * 0.3), run_time=0.4)
        until(self, "It edits your shell")
        self.play(Indicate(path, color=None, scale_factor=1.08), run_time=0.6)
        until(self, "so the shell can find")
        pkg = VGroup(pa_plinth(B21_PKG, 1.3, 1.3), B21_PKG.box(0, 0, 0, 1.3, 1.3, 0.9))
        pa_slide_in(self, pkg, LEFT * 5.0, 0.6)
        until(self, "an administrator built once")
        tok = pa_token(5.95, -1.5, 0.95)
        self.play(GrowFromCenter(tok), run_time=0.4)
        until(self, "shares with everyone")
        self.play(FadeIn(T("built once, shared", 36).move_to([4.45, -2.65, 0]), shift=UP * 0.2), run_time=0.35)
        until(self, "Load a module")
        prompt = b21_light("$ module load python/3.11", -5.85, B21_PROMPT_Y)
        self.play(FadeIn(prompt, shift=RIGHT * 0.3), run_time=0.35)
        until(self, "PATH gains")
        tail = VGroup(*path[5:])                                   # "/usr/bin" steps right to make room
        pill = b21_pill("package dir", B21_SLOT_X, B21_PATH_Y, 3.25)
        colon = b21_light(":", B21_SLOT_X + 3.3, B21_PATH_Y)
        pill.shift(UP * 2.4)
        self.add(pill)
        self.play(tail.animate.shift(RIGHT * 3.65), pill.animate.shift(DOWN * 2.4), FadeIn(colon), run_time=0.6)
        arrow = Arrow([-2.7, -1.0, 0], [3.5, -1.3, 0], color=BAR2, stroke_width=5, buff=0).set_z_index(2)
        self.play(GrowArrow(arrow), run_time=0.5)
        until(self, "Unload it")
        prompt2 = b21_light("$ module unload python/3.11", -5.85, B21_PROMPT_Y)
        self.remove(prompt); self.add(prompt2)
        self.play(pill.animate.shift(UP * 2.4), FadeOut(arrow), FadeOut(colon), run_time=0.5)
        self.remove(pill, *pill)
        self.play(tail.animate.shift(LEFT * 3.65), run_time=0.4)
        until(self, "switch between versions")
        self.remove(prompt2)
        p311 = b21_pill("3.11", B21_SLOT_X, B21_PATH_Y, 1.3)
        colon2 = b21_light(":", B21_SLOT_X + 1.4, B21_PATH_Y)
        p311.shift(UP * 2.4)
        self.add(p311)
        self.play(tail.animate.shift(RIGHT * 1.75), p311.animate.shift(DOWN * 2.4), FadeIn(colon2), run_time=0.5)
        until(self, "with no conflicts")
        p313 = b21_pill("3.13", B21_SLOT_X, B21_PATH_Y, 1.3).shift(DOWN * 2.2)
        self.add(p313)
        self.play(p311.animate.shift(UP * 2.4), p313.animate.shift(UP * 2.2), run_time=0.5)
        self.remove(p311, *p311)
        until(self, "the fastest install")
        self.play(Indicate(p313, color=None, scale_factor=1.1), run_time=0.5)
        done(self)


# ─────────────── B31 · Conda pitfalls: solve in a job, mind home, never scratch, cache only ───────────────
B31_RACK = Iso(-5.1, -0.2, 0.6)                                  # the login node, upper left
B31_JOB = Iso(-3.35, -2.3, 0.75)                                 # the job box, lower left
B31_HOME = Iso(-0.9, -1.1, 0.75)                                 # the home box, centre
B31_BIN = Iso(3.0, -1.7, 0.6)                                    # the scratch bin, right
B31_CAB = Iso(5.4, -1.0, 0.6)                                    # the project cabinet, far right
B31_GAUGE = (0.75, -0.3)


def b31_env(iso):
    return pa_env_box(iso, 0.6)


def b31_dashed(mob):
    """The vanished environment: the same box as a grey dashed outline."""
    return VGroup(*[DashedVMobject(f.copy().set_fill(opacity=0).set_stroke(BAR1, 3), num_dashes=10) for f in mob]).set_z_index(mob.z_index)


class B31_CondaPitfalls(Scene):
    def construct(self):
        st, li = explorer_rack(B31_RACK)
        self.add(st, li, T("login node", 34).move_to([-5.1, -0.7, 0]))
        until(self, "Solving an environment")
        env = b31_env(Iso(B31_RACK.ox, B31_RACK.oy, 0.6)).shift(B31_RACK.v(0.35, 0.35, 0.88))
        pa_drop(self, [env], 0.5, dist=4.0)
        until(self, "so do it in an interactive job")
        job = job_box(B31_JOB)
        pa_drop(self, [job], 0.45, dist=4.0)
        self.add(T("job", 34).move_to([-3.35, -2.65, 0]))
        a = np.array(env.get_center())
        tgt = b31_env(Iso(B31_JOB.ox, B31_JOB.oy, 0.6)).shift(B31_JOB.v(0.05, 0.05, 0.56))
        b = np.array(tgt.get_center())
        env.set_z_index(9)
        self.play(MoveAlongPath(env, ArcBetweenPoints(a, b, angle=PI / 3)), run_time=0.7)
        until(self, "not on the login node")
        self.play(Create(check(-2.55, -1.2, 0.2, TERRA, 8)), run_time=0.35)
        until(self, "Watch your home quota")
        home = VGroup(pa_plinth(B31_HOME, 1.2, 1.2), home_box(B31_HOME))
        out, segs = pa_gauge(B31_GAUGE[0], B31_GAUGE[1])
        pa_drop(self, [home], 0.5, dist=4.0, with_=(Create(out),))
        self.add(T("home", 34).move_to([-0.9, -1.7, 0]), T("quota", 34).move_to([0.75, -1.35, 0]))
        pa_fill(self, segs, 0, 2, 0.4)
        until(self, "tens of thousands of small files")
        dots = pa_file_dots(36, -1.9, 0.1, 1.9, 3.1, seed=11)
        pa_pour(self, dots, B31_HOME, 0, 0, 1.2, 1.2, 0.9, 1.0, seed=5)
        pa_fill(self, segs, 2, 5, 0.5)
        until(self, "But do not put")
        bk, fr = scratch_bin(B31_BIN)
        binp = pa_plinth(B31_BIN, 2.8, 1.8)
        pa_slide_in(self, VGroup(binp, bk, fr), LEFT * 6.0, 0.6)
        self.add(T("scratch", 34).move_to([3.1, -2.2, 0]))
        env2 = b31_env(Iso(B31_BIN.ox, B31_BIN.oy, 0.6)).shift(B31_BIN.v(1.0, 0.6, 0)).set_z_index(1)
        pa_drop(self, [env2], 0.45, dist=4.0)
        until(self, "because scratch is purged")
        line = Line(B31_BIN.p(-0.25, -0.2, 0.95), B31_BIN.p(-0.25, 2.0, 0.95), color=TERRA, stroke_width=7).set_z_index(6)
        ghost = b31_dashed(env2)
        self.play(Create(line), run_time=0.3)
        self.play(line.animate.shift(B31_BIN.v(3.25, 0, 0)), FadeOut(env2), FadeIn(ghost), run_time=0.8)
        self.play(FadeOut(line), FadeIn(T("purged", 34).move_to([3.5, 0.7, 0]), shift=UP * 0.2), run_time=0.3)
        until(self, "Keep environments")
        cab = VGroup(pa_plinth(B31_CAB, 1.3, 1.1), project_cabinet(B31_CAB))
        pa_slide_in(self, cab, LEFT * 2.5, 0.5)
        self.add(T("project", 34).move_to([5.45, -1.4, 0]))
        until(self, "home or a project directory")
        env3 = b31_env(Iso(B31_CAB.ox, B31_CAB.oy, 0.6)).shift(B31_CAB.v(0.35, 0.25, 2.0))
        pa_drop(self, [env3], 0.5, dist=3.0)
        until(self, "The one piece")
        self.play(FadeOut(ghost), run_time=0.4)
        until(self, "is the package cache")
        pk = pa_env_box(Iso(B31_BIN.ox, B31_BIN.oy, 0.6), 0.45).shift(B31_BIN.v(1.05, 0.65, 0)).set_z_index(1)
        pa_drop(self, [pk], 0.45, dist=4.0)
        self.add(M("pkgs", 32).move_to([2.2, -0.15, 0]))
        until(self, "which is regenerable")
        ck = check(3.85, -0.6, 0.2, TERRA, 8).set_z_index(8)
        self.play(Create(ck), run_time=0.35)
        until(self, "Or just empty it")
        self.play(FadeOut(pk, shift=UP * 0.3), run_time=0.4)
        done(self)
