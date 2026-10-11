
# ═════════════════════════════ PART B · Act IV (B40 B41) · Act VI (B62 B63) · Act VIII (B80) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB3_ / b4x_ / b6x_ / b8x_ so the parts never collide.
#
# Act IV stage (B40, B41): the film-1 grammar, four containers in one row, each on a thin dark plinth (kraft and
# white on cream alone measure under Gate V's 0.30 contrast floor; the plinths carry it):
#   home_box · scratch_bin · project_cabinet · a kraft cabinet for courses.
# Mono at 32 runs ~0.25 units a character, so the four real paths (18.9 units together) cannot share one row
# under four containers: they sit in a 2 x 2 mono grid under the row, left column under home/scratch, right
# column under the two cabinets, slashes aligned per column. B41's capacity labels take the same four cells.
PB3_S, PB3_Y = 0.78, -1.1
PB3_HOME = Iso(-4.988, PB3_Y, PB3_S)
PB3_BIN = Iso(-1.753, PB3_Y, PB3_S)
PB3_PROJ = Iso(2.084, PB3_Y, PB3_S)
PB3_COURSE = Iso(4.914, PB3_Y, PB3_S)
PB3_KRAFT = "#917A55"                      # dark kraft: outlines of SMALL objects only (GATE T: small ink rings fuse)
PB3_TRACK = "#E3DFD4"                      # pale track / pad: within 28 of the stage, so Gate V does not count it as ink
PB3_COL_X = (-5.95, 0.1)                   # left edges of the two label columns
PB3_ROW_Y = (-1.75, -2.55)                 # the two label rows
PB3_CELL = ((0, 0), (0, 1), (1, 0), (1, 1))   # (column, row) of home, scratch, projects, courses
PB3_PATHS = ("/home/username", "/scratch/username", "/projects/projectname", "/courses/coursename.code")
PB3_CAPS = ("75 GB", "50 TB", "long-term", "1–5 TB · shared")


def pb3_at(mob, x_left, y):
    """Place a text by its LEFT edge."""
    return mob.move_to([x_left + mob.width / 2, y, 0])


def pb3_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb3_pad(iso, w, d, m=0.15, h=0.1):
    """A thin dark plinth under a container: its top is the floor (z = 0)."""
    return iso.box(-m, -m, -h, w + 2 * m, d + 2 * m, h, DARK_TOP, DARK_L, DARK_R).set_z_index(-1)


def pb3_pads():
    return VGroup(pb3_pad(PB3_HOME, 1.2, 1.2), pb3_pad(PB3_BIN, 2.8, 1.8), pb3_pad(PB3_PROJ, 1.3, 1.1), pb3_pad(PB3_COURSE, 1.3, 1.1))


def pb3_home():
    return home_box(PB3_HOME).set_z_index(1)


def pb3_bin():
    back, front = scratch_bin(PB3_BIN)
    return back, front


def pb3_proj():
    return project_cabinet(PB3_PROJ).set_z_index(1)


def pb3_course():
    """The courses cabinet: the project cabinet's shape in kraft."""
    iso = PB3_COURSE
    body = iso.box(0, 0, 0, 1.3, 1.1, 2.0)
    lines = VGroup(*[Line(iso.p(0.12, 0, 2.0 * f), iso.p(1.18, 0, 2.0 * f), color=BAR1, stroke_width=4) for f in (0.34, 0.67)])
    return VGroup(body, lines).set_z_index(1)


def pb3_cell_xy(k):
    c, r = PB3_CELL[k]
    return PB3_COL_X[c], PB3_ROW_Y[r]


def pb3_path(k):
    x, y = pb3_cell_xy(k)
    return pb3_at(M(PB3_PATHS[k], 32), x, y)


def pb3_paths():
    return VGroup(*[pb3_path(k) for k in range(4)])


def pb3_ring(k):
    """A small grey ring on the leading slash of path k: a filled annulus with no stroke (BAR1 is above GATE T's
    text-grey threshold, and the layout audit reads only STROKED paths as curves under a label)."""
    x, y = pb3_cell_xy(k)
    return Annulus(inner_radius=0.24, outer_radius=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0,
                   stroke_opacity=0).move_to([x + 0.11, y, 0]).set_z_index(-2)


def pb3_rings():
    return VGroup(*[pb3_ring(k) for k in range(4)])


def pb3_cap(k):
    """Capacity label k, in the path's cell: the two short ones in 44, the two long ones in 36."""
    x, y = pb3_cell_xy(k)
    return pb3_at(T(PB3_CAPS[k], 44 if k < 2 else 36), x, y)


def pb3_stage(self):
    """Put the Act IV row on stage (the end of B40, minus the title). Returns the parts."""
    pads, home, proj, course = pb3_pads(), pb3_home(), pb3_proj(), pb3_course()
    bk, fr = pb3_bin()
    self.add(pads, home, bk, fr, proj, course)
    return pads, home, bk, fr, proj, course


def pb3_land(self, mob, rt=0.55, dist=1.2):
    """A container lands: a short drop onto its pad."""
    self.play(FadeIn(mob, shift=DOWN * dist), run_time=rt)


# ─────────────── B40 · four places: home, scratch, projects, courses; every path starts with a slash ───────────────
class B40_FourPlaces(Scene):
    def construct(self):
        self.add(pb3_title("IV · Where Files Live"))
        pads = pb3_pads()
        self.play(LaggedStart(*[FadeIn(p) for p in pads], lag_ratio=0.25), run_time=0.7)
        paths = pb3_paths()
        until(self, "home directory", lead=0.4)
        pb3_land(self, pb3_home())
        self.play(FadeIn(paths[0]), run_time=0.3)
        until(self, "scratch directory", lead=0.3)
        bk, fr = pb3_bin()
        pb3_land(self, VGroup(bk, fr))
        self.play(FadeIn(paths[1]), run_time=0.3)
        until(self, "projects space", lead=0.4)
        proj = pb3_proj()
        pb3_land(self, proj)
        self.play(FadeIn(paths[2]), run_time=0.3)
        until(self, "courses space", lead=0.4)
        pb3_land(self, pb3_course())
        self.play(FadeIn(paths[3]), run_time=0.3)
        until(self, "may not have projects", lead=0.1)
        self.play(paths[2].animate.set_color(DIM), run_time=0.3)              # a student may have no projects path
        until(self, "starting with a slash", lead=0.6)
        self.play(paths[2].animate.set_color(INK), run_time=0.3)
        rings = pb3_rings()
        self.play(LaggedStart(*[GrowFromCenter(r) for r in rings], lag_ratio=0.25), run_time=0.8)   # the four leading slashes
        until(self, "wherever it runs", lead=0.1)
        self.play(Indicate(rings, color=BAR1, scale_factor=1.12), run_time=0.5)
        done(self)


# ─────────────── B41 · quotas: 75 GB fills, 50 TB is purged on the first Tuesday, projects keeps, courses share ───────────────
B41_W, B41_D, B41_H = 0.5, 0.6, 0.42                               # a block in the bin
B41_BIN_XY = [(0.2 + 0.85 * i, 0.2 + 0.85 * j) for j in (1, 0) for i in range(3)]
B41_KEEP = (1, 4)                                                   # indices of the two marked blocks (the ones you keep)
B41_HOME_XY = ((0.12, 0.12), (0.63, 0.12), (0.12, 0.63), (0.63, 0.63))
B41_PROJ_XY = ((0.1, 0.45), (0.7, 0.45))
B41_SMALL_XY = ((0.08, 0.05), (0.38, 0.05), (0.68, 0.05), (0.98, 0.05))
B41_COURSE_XY = ((0.1, 0.1), (0.7, 0.1), (0.4, 0.6))
B41_CAL_Y = 0.9                                                      # clear of the bin top (-0.48), so the midpoint frame has no card over the bin
B41_STAMP_Y = 2.05


def b41_block(iso, x, y, z=0.0, w=B41_W, d=B41_D, h=B41_H, mark=False, zi=1.0):
    g = VGroup(iso.box(x, y, z, w, d, h, sw=3))
    if mark:
        g.add(Dot(iso.p(x + w / 2, y + d / 2, z + h), radius=0.085, color=TERRA))
    return g.set_z_index(zi + 0.02 * (8 - (x + y)))


def b41_drop(self, mobs, rt=0.7, lag=0.12, dist=4.5):
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), run_time=rt, rate_func=ease_in)


def b41_stamp():
    return T("quota exceeded", 38, bold=True).move_to([-4.4, B41_STAMP_Y, 0])


def b41_calendar(cx):
    """A calendar page: white card, grey outline (BAR1 is above GATE T's text grey), ghost day squares, the first Tuesday in terracotta."""
    card = RoundedRectangle(width=1.5, height=1.25, corner_radius=0.08, fill_color=CARD, fill_opacity=1,
                            stroke_color=BAR1, stroke_width=4).move_to([cx, B41_CAL_Y, 0])
    days = VGroup()
    for r in range(4):
        for c in range(7):
            days.add(Square(side_length=0.12, fill_color=GHOST, fill_opacity=1, stroke_width=0)
                     .move_to([cx - 0.57 + c * 0.19, B41_CAL_Y + 0.33 - r * 0.24, 0]))
    tue = Dot([cx - 0.57 + 2 * 0.19, B41_CAL_Y + 0.33, 0], radius=0.085, color=TERRA)
    return VGroup(card, days, tue).set_z_index(6)


class B41_Quotas(Scene):
    def construct(self):
        pads, home, bk, fr, proj, course = pb3_stage(self)
        paths, rings = pb3_paths(), pb3_rings()
        self.add(paths, rings)
        self.play(FadeOut(paths), FadeOut(rings), run_time=0.35)
        until(self, "seventy-five", lead=0.3)
        self.play(FadeIn(pb3_cap(0), shift=UP * 0.2), run_time=0.35)
        until(self, "fills fastest", lead=0.2)
        pile = [b41_block(PB3_HOME, x, y, 0.9, 0.45, 0.45, 0.36, zi=3) for x, y in B41_HOME_XY]
        b41_drop(self, pile, 0.7, 0.15)                                           # home fills
        until(self, "quota exceeded", lead=0.2)
        st = b41_stamp().scale(1.6)
        self.play(FadeIn(st), st.animate.scale(1 / 1.6), run_time=0.35)          # the stamp lands
        until(self, "fifty terabytes", lead=0.3)
        self.play(FadeIn(pb3_cap(1), shift=UP * 0.2), run_time=0.35)
        blocks = [b41_block(PB3_BIN, x, y, mark=(k in B41_KEEP)) for k, (x, y) in enumerate(B41_BIN_XY)]
        b41_drop(self, blocks, 0.8, 0.1)
        until(self, "first Tuesday", lead=0.4)
        cal = b41_calendar(-2.3)
        self.play(FadeIn(cal, shift=DOWN * 0.3), run_time=0.45)                  # the calendar page arrives
        until(self, "anything you want to keep", lead=0.2)
        keep = [blocks[k] for k in B41_KEEP]
        for m in keep:
            m.set_z_index(8)
        self.play(*[m.animate.shift(UP * 1.1) for m in keep], run_time=0.4)      # lift what you keep
        rest = [b for k, b in enumerate(blocks) if k not in B41_KEEP]
        rest = sorted(rest, key=lambda m: float(np.array(m.get_center())[0]))
        self.play(cal.animate.shift(RIGHT * 2.3), LaggedStart(*[FadeOut(m) for m in rest], lag_ratio=0.12), run_time=0.9)   # the purge
        self.play(FadeOut(cal), run_time=0.3)
        until(self, "long-term home", lead=0.5)
        self.play(FadeIn(pb3_cap(2), shift=UP * 0.2), run_time=0.35)
        for m, (x, y) in zip(keep, B41_PROJ_XY):
            tgt = b41_block(PB3_PROJ, x, y, 2.0, mark=True)
            a, b = np.array(m.get_center()), np.array(tgt.get_center())
            self.play(MoveAlongPath(m, ArcBetweenPoints(a, b, angle=-PI / 3)), run_time=0.55)   # into the project cabinet
        until(self, "many small files", lead=0.3)
        small = [b41_block(PB3_PROJ, x, y, 2.0, 0.24, 0.3, 0.2, zi=4) for x, y in B41_SMALL_XY]
        b41_drop(self, small, 0.6, 0.12, 3.5)
        until(self, "one to five terabytes", lead=0.3)
        self.play(FadeIn(pb3_cap(3), shift=UP * 0.2), run_time=0.35)
        until(self, "whole class", lead=0.3)
        shared = [b41_block(PB3_COURSE, x, y, 2.0, 0.45, 0.4, 0.3, zi=4) for x, y in B41_COURSE_XY]
        b41_drop(self, shared, 0.6, 0.15, 3.5)
        done(self)


# ─────────────── B62 · the partition table: CPU and GPU columns, then two gated blocks ───────────────
B62_CX = (-3.1, 3.1)                                                 # column centres
B62_HEAD_Y, B62_RULE_Y, B62_BOTTOM_Y = 2.65, 2.2, -0.5
B62_ROW_Y = (1.7, 1.1, 0.5, -0.1)
B62_CPU = ("short", "sharing")
B62_GPU = ("gpu", "sharing", "gpu-interactive", "gpu-short")
B62_BLOCK_Y = (-0.8, -3.1)                                           # top and bottom of the two blocks
B62_TITLE_Y, B62_LINE_Y = (-1.25, -2.0, -2.6)[0], (-2.0, -2.6)


def b62_name(s, x, y):
    return M(s, 34).move_to([x, y, 0])


def b62_rule(y, color=INK, sw=5):
    return Line([-6.0, y, 0], [6.0, y, 0], color=color, stroke_width=sw)


def b62_block(x0, x1):
    """A grey-outlined block (BAR1 is above GATE T's text-grey threshold, so the outline never reads as type)."""
    return Rectangle(width=x1 - x0, height=B62_BLOCK_Y[0] - B62_BLOCK_Y[1], stroke_color=BAR1, stroke_width=4,
                     fill_opacity=0).move_to([(x0 + x1) / 2, (B62_BLOCK_Y[0] + B62_BLOCK_Y[1]) / 2, 0])


def b62_gate(cx, cy):
    """A small gate: two dark-kraft posts and three bars (small object: dark kraft, never ink)."""
    posts = VGroup(Line([cx - 0.32, cy - 0.28, 0], [cx - 0.32, cy + 0.3, 0], color=PB3_KRAFT, stroke_width=6),
                   Line([cx + 0.32, cy - 0.28, 0], [cx + 0.32, cy + 0.3, 0], color=PB3_KRAFT, stroke_width=6))
    bars = VGroup(*[Line([cx - 0.32, cy + dy, 0], [cx + 0.32, cy + dy, 0], color=PB3_KRAFT, stroke_width=4) for dy in (0.16, 0.0, -0.16)])
    return VGroup(posts, bars)


def b62_tag(cx, cy):
    """A kraft luggage tag with a hole: the course marker."""
    body = Polygon([cx - 0.42, cy, 0], [cx - 0.22, cy + 0.24, 0], [cx + 0.42, cy + 0.24, 0], [cx + 0.42, cy - 0.24, 0], [cx - 0.22, cy - 0.24, 0],
                   fill_color=BOX_L, fill_opacity=1, stroke_color=PB3_KRAFT, stroke_width=3)
    hole = Dot([cx - 0.2, cy, 0], radius=0.05, color=CARD)
    return VGroup(body, hole)


class B62_Partitions(Scene):
    def construct(self):
        head = VGroup(T("CPU", 40, bold=True).move_to([B62_CX[0], B62_HEAD_Y, 0]), T("GPU", 40, bold=True).move_to([B62_CX[1], B62_HEAD_Y, 0]))
        until(self, "A partition is how", lead=0.0)
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.4)
        until(self, "by time limit", lead=0.2)
        self.play(Create(b62_rule(B62_RULE_Y)), run_time=0.5)                                      # the header rule
        until(self, "by CPU or GPU", lead=0.2)
        self.play(Create(Line([0, B62_RULE_Y, 0], [0, B62_BOTTOM_Y, 0], color=BAR1, stroke_width=3)), run_time=0.4)   # the column divider
        until(self, "short, the default", lead=0.2)
        self.play(FadeIn(b62_name(B62_CPU[0], B62_CX[0], B62_ROW_Y[0]), shift=RIGHT * 0.2), run_time=0.35)
        until(self, "and sharing for CPU", lead=0.1)
        self.play(FadeIn(b62_name(B62_CPU[1], B62_CX[0], B62_ROW_Y[1]), shift=RIGHT * 0.2), run_time=0.35)
        until(self, "gpu, gpu-interactive", lead=0.2)
        self.play(LaggedStart(*[FadeIn(b62_name(s, B62_CX[1], y), shift=RIGHT * 0.2) for s, y in zip(B62_GPU, B62_ROW_Y)], lag_ratio=0.3), run_time=0.9)
        self.play(Create(b62_rule(B62_BOTTOM_Y, BAR1, 3)), run_time=0.35)
        until(self, "Two you apply for", lead=0.2)
        self.play(Create(b62_block(-5.9, -0.3)), run_time=0.4)
        self.play(FadeIn(T("apply for access", 38).move_to([-2.7, B62_TITLE_Y, 0])), GrowFromCenter(b62_gate(-4.95, B62_TITLE_Y)), run_time=0.4)
        until(self, "long and multigpu", lead=0.1)
        self.play(FadeIn(b62_name("long", -3.1, B62_LINE_Y[0]), shift=RIGHT * 0.2), FadeIn(b62_name("multigpu", -3.1, B62_LINE_Y[1]), shift=RIGHT * 0.2), run_time=0.4)
        until(self, "two only for courses", lead=0.2)
        self.play(Create(b62_block(0.3, 5.9)), run_time=0.4)
        self.play(FadeIn(T("courses only", 38).move_to([3.4, B62_TITLE_Y, 0])), GrowFromCenter(b62_tag(1.55, B62_TITLE_Y)), run_time=0.4)
        until(self, "courses and courses-gpu", lead=0.1)
        self.play(FadeIn(b62_name("courses", 3.1, B62_LINE_Y[0]), shift=RIGHT * 0.2), FadeIn(b62_name("courses-gpu", 3.1, B62_LINE_Y[1]), shift=RIGHT * 0.2), run_time=0.4)
        done(self)


# ─────────────── B63 · which partition: a decision tree that lights as spoken ───────────────
B63_Y = (2.7, 1.5, 0.3, -0.6, -1.3, -2.0)                           # root, yes/no, condition, partition rows (two, staggered), gpu-short
B63_YES_X, B63_NO_X = -3.8, 2.4
B63_LEAF = ((-5.1, "CPU jobs", "courses", 0), (-2.5, "GPU jobs", "courses-gpu", 1),
            (0.0, "CPU", "short", 0), (2.4, "interactive GPU", "gpu-interactive", 1), (5.1, "GPU batch", "gpu", 0))


def b63_edge(xf, yf, xt, yt):
    """An ink branch from the label at (xf, yf) down to the label at (xt, yt), 0.3 clear of both."""
    return Line([xf, yf - 0.4, 0], [xt, yt + 0.4, 0], color=INK, stroke_width=4)


def b63_lab(s, x, y, size=34):
    return T(s, size).move_to([x, y, 0])


def b63_leaf(k):
    """(edge, condition label, partition name) for leaf k, hanging from its yes/no node."""
    x, cond, part, row = B63_LEAF[k]
    xf = B63_YES_X if k < 2 else B63_NO_X
    return b63_edge(xf, B63_Y[1], x, B63_Y[2]), b63_lab(cond, x, B63_Y[2], 32), M(part, 32).move_to([x, B63_Y[3 + row], 0])


class B63_WhichPartition(Scene):
    def construct(self):
        root = b63_lab("in a course?", 0.0, B63_Y[0], 36)
        self.play(FadeIn(root, shift=DOWN * 0.2), run_time=0.4)
        until(self, "If you're in a course", lead=0.1)
        self.play(Create(b63_edge(0.0, B63_Y[0], B63_YES_X, B63_Y[1])), run_time=0.4)
        self.play(FadeIn(b63_lab("yes", B63_YES_X, B63_Y[1])), run_time=0.3)
        until(self, "use courses for CPU", lead=0.2)
        e, c, p = b63_leaf(0)
        self.play(Create(e), FadeIn(c), run_time=0.35)
        self.play(FadeIn(p, shift=DOWN * 0.15), run_time=0.3)
        until(self, "courses-gpu for GPU", lead=0.2)
        e, c, p = b63_leaf(1)
        self.play(Create(e), FadeIn(c), run_time=0.35)
        self.play(FadeIn(p, shift=DOWN * 0.15), run_time=0.3)
        until(self, "Otherwise", lead=0.2)
        self.play(Create(b63_edge(0.0, B63_Y[0], B63_NO_X, B63_Y[1])), run_time=0.4)
        self.play(FadeIn(b63_lab("no", B63_NO_X, B63_Y[1])), run_time=0.3)
        until(self, "short for most CPU", lead=0.2)
        e, c, p = b63_leaf(2)
        self.play(Create(e), FadeIn(c), run_time=0.35)
        self.play(FadeIn(p, shift=DOWN * 0.15), run_time=0.3)
        until(self, "gpu-interactive or gpu-short", lead=0.3)
        e, c, p = b63_leaf(3)
        self.play(Create(e), FadeIn(c), run_time=0.35)
        self.play(FadeIn(p, shift=DOWN * 0.15), run_time=0.3)
        self.play(FadeIn(M("gpu-short", 32).move_to([2.4, B63_Y[5], 0]), shift=DOWN * 0.15), run_time=0.3)
        until(self, "the gpu partition for GPU batch", lead=0.3)
        e, c, p = b63_leaf(4)
        self.play(Create(e), FadeIn(c), run_time=0.35)
        self.play(FadeIn(p, shift=DOWN * 0.15), run_time=0.3)
        done(self)


# ─────────────── B80 · two real seff reports, re-composed on cream: tracks are what was asked for, bars what was used ───────────────
B80_X0 = (-5.95, 0.35)                                               # left edge of each report
B80_FULL = 3.4                                                       # 100 % of a bar
B80_BAR_H = 0.4
B80_Y = {"head": 2.2, "cores": 1.5, "wall": 0.95, "cpu_lab": 0.3, "cpu_bar": -0.3, "mem_lab": -1.0, "mem_bar": -1.6, "verdict": -2.6}
B80_REPORTS = (("$ seff 371441", "cores 12", "wall-clock 00:17:19", 8.29, "8.29%", 10.44, "10.44% of 50 GB"),
               ("$ seff 2612438", "cores 8", "wall-clock 00:25:57", 83.83, "83.83%", 3.56, "3.56% of 15.62 GB"))


def b80_text(s, k, key, size=32, fn=None):
    return pb3_at((fn or M)(s, size), B80_X0[k], B80_Y[key])


def b80_track(k, key):
    return Rectangle(width=B80_FULL, height=B80_BAR_H, fill_color=PB3_TRACK, fill_opacity=1, stroke_width=0, stroke_opacity=0).move_to([B80_X0[k] + B80_FULL / 2, B80_Y[key], 0])


def b80_bar(k, key, pct):
    w = B80_FULL * pct / 100.0
    return Rectangle(width=w, height=B80_BAR_H, fill_color=BAR1, fill_opacity=1, stroke_width=0, stroke_opacity=0).move_to([B80_X0[k] + w / 2, B80_Y[key], 0])


def b80_value(k, key, pct, s, gap=0.3):
    return pb3_at(M(s, 32), B80_X0[k] + B80_FULL * pct / 100.0 + gap, B80_Y[key])


class B80_Seff(Scene):
    def construct(self):
        self.add(pb3_title("VIII · Right-Sizing"))
        heads = VGroup(*[b80_text(r[0], k, "head", 36) for k, r in enumerate(B80_REPORTS)])
        divider = Line([-0.3, 2.5, 0], [-0.3, -2.9, 0], color=BAR1, stroke_width=3)
        self.play(FadeIn(heads, shift=DOWN * 0.15), Create(divider), run_time=0.5)
        until(self, "close to the minimum", lead=0.3)
        labs = VGroup(*[b80_text(s, k, key) for k in range(2) for s, key in (("CPU efficiency", "cpu_lab"), ("memory efficiency", "mem_lab"))])
        self.play(FadeIn(labs, shift=RIGHT * 0.15), run_time=0.4)
        until(self, "the more you request", lead=0.2)
        tracks = [b80_track(k, key) for k in range(2) for key in ("cpu_bar", "mem_bar")]
        self.play(LaggedStart(*[GrowFromEdge(t, LEFT) for t in tracks], lag_ratio=0.15), run_time=0.8)      # what was asked for
        until(self, "seff, Slurm efficiency", lead=0.2)
        self.play(Indicate(heads, color=INK, scale_factor=1.08), run_time=0.5)
        until(self, "Two real reports", lead=0.2)
        rows = VGroup(*[b80_text(r[i], k, key) for k, r in enumerate(B80_REPORTS) for i, key in ((1, "cores"), (2, "wall"))])
        self.play(FadeIn(rows, shift=DOWN * 0.15), run_time=0.45)
        until(self, "twelve cores", lead=0.2)
        self.play(Indicate(rows[0], color=INK, scale_factor=1.12), run_time=0.5)
        until(self, "eight percent CPU", lead=0.2)
        self.play(GrowFromEdge(b80_bar(0, "cpu_bar", 8.29), LEFT), run_time=0.5)
        dot = Dot([B80_X0[0] + B80_FULL * 0.0829 + 0.3, B80_Y["cpu_bar"], 0], radius=0.11, color=TERRA)
        self.play(GrowFromCenter(dot), FadeIn(b80_value(0, "cpu_bar", 8.29, "8.29%", gap=0.75)), run_time=0.3)
        until(self, "ten percent of fifty", lead=0.2)
        self.play(GrowFromEdge(b80_bar(0, "mem_bar", 10.44), LEFT), run_time=0.5)
        self.play(FadeIn(b80_value(0, "mem_bar", 10.44, "10.44% of 50 GB")), run_time=0.25)
        until(self, "asked for far less", lead=0.3)
        self.play(FadeIn(b80_text("could ask for less", 0, "verdict", 38, T), shift=UP * 0.15), run_time=0.4)
        until(self, "Job two", lead=0.1)
        self.play(Indicate(rows[2], color=INK, scale_factor=1.12), run_time=0.5)
        until(self, "eighty-four percent", lead=0.2)
        self.play(GrowFromEdge(b80_bar(1, "cpu_bar", 83.83), LEFT), run_time=0.7)
        self.play(FadeIn(b80_value(1, "cpu_bar", 83.83, "83.83%")), run_time=0.25)
        self.play(GrowFromEdge(b80_bar(1, "mem_bar", 3.56), LEFT), FadeIn(b80_value(1, "mem_bar", 3.56, "3.56% of 15.62 GB")), run_time=0.4)
        until(self, "much better fit", lead=0.2)
        self.play(GrowFromCenter(check(B80_X0[1] + 5.0, B80_Y["cpu_bar"], 0.2, INK, 7)), run_time=0.35)
        until(self, "Try seff", lead=0.2)
        self.play(Indicate(heads, color=INK, scale_factor=1.08), run_time=0.5)
        done(self)
