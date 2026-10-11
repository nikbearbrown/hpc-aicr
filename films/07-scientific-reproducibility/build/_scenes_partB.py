# ═════════════════════════════ PART B · B52 (Act V) · B60, B62 (Act VI) · B80 (Act VIII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB7_ / pb7_ / b52_ / b60_ / b62_ / b80_ so the parts never collide.
PB7_SMALL = "#917A55"                       # dark kraft: outlines of SMALL objects only (GATE T)
PB7_LINK = "#9C8462"                        # deep kraft: connectors (ink-edged connectors fuse objects into one blob)
PB7_PAD = "#EFEADF"                         # plinth top, within 28 of the stage (Gate V counts darker pads as ink)


def pb7_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb7_left(mob, x, y):
    """Left-align a text at x, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pb7_drop(self, mobs, rt=0.5, lag=0.2, dist=4.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt, rate_func=ease_in)


def pb7_plinth(iso, x0, y0, w, d, h=0.14):
    """A plinth: pale board on top, dark sides carry Gate V's contrast."""
    return iso.box(x0, y0, -h, w, d, h, PB7_PAD, DARK_L, DARK_R).set_z_index(-1)


def pb7_dashes(a, b, n=5, color=DIM, sw=5):
    """A broken (dashed) line from a to b: n dashes with gaps."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    g = VGroup()
    for k in range(n):
        t0, t1 = (k + 0.1) / n, (k + 0.65) / n
        g.add(Line(a + (b - a) * t0, a + (b - a) * t1, color=color, stroke_width=sw))
    return g


def pb7_dirbox(iso, sw=3):
    """A directory: a small kraft box (B60's cast; also the file-layout icon in B80)."""
    return iso.box(0, 0, 0, 0.9, 0.9, 0.6, sw=sw)


def pb7_page_on(iso, x=0.1, y=0.1, z=0.6, w=0.7, d=0.72):
    """A README page lying on a box top. Grey outline: an ink card inside an ink box reads as overlapping text (GATE T)."""
    pg = iso.page(x, y, z, w, d)
    pg[0].set_stroke(DIM)
    return pg


def pb7_person(x, y, s=1.0):
    """A person token standing with its feet at (x, y): grey body, ink outline."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head)


# ─────────────── B52 · accretion over months (clash, won't rebuild) vs one session from one file (rebuilds anywhere) ───────────────
B52_BIN = Iso(-4.3, -2.2, 0.62)             # the left environment bin (open: packages land inside)
B52_BOX = Iso(2.0, -2.2, 0.62)              # the right environment box, on its plinth
B52_BOX2 = Iso(4.9, -2.2, 0.62)             # the second plinth: the rebuilt copy
B52_PAGE = Iso(0.85, 1.55, 0.6)             # the environment.yml page
B52_CAL_Y = 2.3
B52_CAL_X = (-5.4, -4.2, -3.0, -1.8)        # four month cards: the calendar strip
B52_PKG = ((0.15, 0.15), (0.95, 0.2), (0.2, 0.95), (0.95, 0.9))   # package slots inside a bin (x, y on its floor)


def b52_month(cx):
    """A month card: white, grey outline, ghost day squares, one ghost day that turns terracotta when a package lands."""
    card = RoundedRectangle(width=1.05, height=0.9, corner_radius=0.07, fill_color=CARD, fill_opacity=1,
                            stroke_color=BAR1, stroke_width=4).move_to([cx, B52_CAL_Y, 0])
    days = VGroup()
    for r in range(3):
        for c in range(5):
            days.add(Square(side_length=0.11, fill_color=GHOST, fill_opacity=1, stroke_width=0)
                     .move_to([cx - 0.36 + c * 0.18, B52_CAL_Y + 0.22 - r * 0.22, 0]))
    mark = Dot([cx - 0.36 + 2 * 0.18, B52_CAL_Y + 0.22 - 1 * 0.22, 0], radius=0.075, color=GHOST)
    return VGroup(card, days, mark)


def b52_pkg(iso, x, y, s=0.55, clash=False):
    """A package: a small kraft cube with a dark-kraft outline (small object). A clashing one has grey faces."""
    if clash:
        return iso.box(x, y, 0, s, s, s * 1.1, BAR3, BAR2, BAR1, sw=3).set_z_index(1)
    b = iso.box(x, y, 0, s, s, s * 1.1, sw=3)
    b.set_stroke(PB7_SMALL)
    return b.set_z_index(1)


def b52_cross(iso, x, y, s=0.55):
    """A grey X over two clashing packages (grey: it sits inside the bin's ink outline)."""
    # the X sat on top of the packages and GATE T §8.6b read it as a label overlapping them; lift it above the bin
    c = iso.p(x + s / 2, y + s / 2, s * 1.1) + np.array([0, 0.75, 0])
    r = 0.3
    return VGroup(Line(c + np.array([-r, -r, 0]), c + np.array([r, r, 0]), color=BAR1, stroke_width=8),
                  Line(c + np.array([-r, r, 0]), c + np.array([r, -r, 0]), color=BAR1, stroke_width=8)).set_z_index(3)


def b52_broken_box(iso, w=1.9, d=1.5, h=0.55):
    """The rebuild that would not resolve: a box drawn only as grey dashes along its edges."""
    P = iso.p
    edges = [((0, 0, 0), (w, 0, 0)), ((0, 0, 0), (0, d, 0)), ((0, 0, 0), (0, 0, h)), ((w, 0, 0), (w, 0, h)),
             ((0, d, 0), (0, d, h)), ((0, 0, h), (w, 0, h)), ((0, 0, h), (0, d, h)), ((w, 0, h), (w, d, h)), ((0, d, h), (w, d, h))]
    return VGroup(*[pb7_dashes(P(*a), P(*b), n=4) for a, b in edges])


def b52_arrow(a, b):
    """A deep-kraft rebuild arrow between two screen points."""
    return Arrow(np.array(a), np.array(b), color=PB7_LINK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.18)


class B52_OneSessionVsAccretion(Scene):
    def construct(self):
        # LEFT · the calendar strip and the empty bin on its plinth are up from the first frame
        months = VGroup(*[b52_month(x) for x in B52_CAL_X])
        back, front = B52_BIN.open_box(0, 0, 0, 1.9, 1.5, 0.55)
        self.add(months, pb7_plinth(B52_BIN, -0.2, -0.2, 2.3, 1.9), back, front)
        self.play(FadeIn(T("over months", 34).move_to([-3.6, 1.45, 0]), shift=DOWN * 0.15), run_time=0.4)
        # added to over months: packages land one at a time, each lighting a day on the next month
        until(self, "Added to over months", lead=0.3)
        pkgs = []
        for k, (x, y) in enumerate(B52_PKG):
            p = b52_pkg(B52_BIN, x, y, clash=(k in (1, 3)))
            pkgs.append(p)
            p.shift(UP * 3.5)
            self.add(p)
            rt = guard(self, 0.32)
            self.play(p.animate.shift(DOWN * 3.5), months[k][2].animate.set_color(TERRA), run_time=rt, rate_func=ease_in)
        # two of them clash
        until(self, "collects conflicts", lead=0.2)
        self.play(Create(b52_cross(B52_BIN, 0.95, 0.55)), run_time=0.4)
        # the rebuild arrow ends in a broken box
        until(self, "it won't resolve", lead=0.6)
        broken = b52_broken_box(Iso(-1.35, -2.2, 0.62))
        arrow = b52_arrow(B52_BIN.p(2.25, 0.3, 0.45), Iso(-1.35, -2.2, 0.62).p(-0.55, 1.5, 0.45))
        self.play(Create(arrow), run_time=0.35)
        self.play(Create(broken), FadeIn(T("won't resolve", 34).move_to([-1.3, -2.85, 0])), run_time=0.5)
        # RIGHT · one file feeds one box in one session
        until(self, "Built in one session", lead=0.5)
        page = B52_PAGE.page(0, 0, 0, 1.1, 1.4)
        yml = pb7_left(M("environment.yml", 32), 1.75, 1.95)
        back2, front2 = B52_BOX.open_box(0, 0, 0, 1.9, 1.5, 0.55)
        pl2 = pb7_plinth(B52_BOX, -0.2, -0.2, 2.3, 1.9)
        link = Line(B52_PAGE.p(0.55, 0.7, -0.15), B52_BOX.p(0.95, 0.75, 1.25), color=PB7_LINK, stroke_width=5)
        self.play(FadeIn(page, shift=DOWN * 0.2), FadeIn(yml), FadeIn(pl2), FadeIn(back2), FadeIn(front2), run_time=0.45)
        self.play(Create(link), FadeIn(T("one session", 34).move_to([4.6, 0.3, 0])), run_time=0.3)
        pkgs2 = [b52_pkg(B52_BOX, x, y) for x, y in B52_PKG]
        pb7_drop(self, pkgs2, rt=0.45, lag=0.0, dist=2.6)                       # all at once
        # it resolves once: a check lands beside the box
        until(self, "it resolves once", lead=0.3)
        self.play(Create(check(3.6, -1.15, 0.26, TERRA, 8)), run_time=0.3)
        # and rebuilds anywhere: a copy appears on the second plinth
        until(self, "rebuilds anywhere", lead=0.75)
        pl3 = pb7_plinth(B52_BOX2, -0.2, -0.2, 2.3, 1.9)
        self.play(FadeIn(pl3), run_time=0.2)
        copy = VGroup(back2.copy(), *[p.copy() for p in pkgs2], front2.copy()).set_z_index(5)
        self.add(copy)
        self.play(copy.animate.shift(RIGHT * (B52_BOX2.ox - B52_BOX.ox)),
                  FadeIn(T("rebuilds anywhere", 34).move_to([3.9, -2.95, 0])), run_time=0.5)
        done(self)


# ─────────────── B60 · data/ → raw/ (locked, chmod 555) · processed/ · metadata/, each with a README; names that sort themselves ───────────────
B60_ROOT = Iso(0.0, 1.75, 0.6)
B60_KIDS = (Iso(-3.2, 0.35, 0.6), Iso(0.4, 0.35, 0.6), Iso(4.0, 0.35, 0.6))
B60_KID_NAMES = ("raw/", "processed/", "metadata/")
B60_LABEL_Y = -0.2
B60_NAMES = ("2024-01-15_experiment-data_v01.csv", "participant_demographics_2024-01-20.csv", "survey_responses_wave1_v03.csv")
B60_NAME_X, B60_NAME_Y = -5.9, (-1.45, -2.15, -2.85)
B60_CW = 8.46 / 34                          # Menlo at 32: screen units per character (measured)


def b60_link(iso_from, iso_to):
    """An elbow connector from the root box's base to a child box's top, in deep kraft, stopping short of both."""
    a = iso_from.p(0.45, 0.45, 0)
    b = iso_to.p(0.9, 0.9, 0.6)
    ymid = 1.5
    return VGroup(Line([a[0], a[1] - 0.08, 0], [a[0], ymid, 0], color=PB7_LINK, stroke_width=4),
                  Line([a[0], ymid, 0], [b[0], ymid, 0], color=PB7_LINK, stroke_width=4),
                  Line([b[0], ymid, 0], [b[0], b[1] + 0.08, 0], color=PB7_LINK, stroke_width=4))


def b60_lock(x, y):
    """A padlock beside raw/: kraft body with an ink outline, an ink shackle (drawn large: tiny locks read as sub-floor text)."""
    body = RoundedRectangle(width=0.62, height=0.5, corner_radius=0.08, fill_color=BOX_L, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    shackle = Arc(radius=0.2, start_angle=0, angle=PI, color=INK, stroke_width=6).move_to([x, y + 0.36, 0])
    return VGroup(shackle, body)


def b60_ring(row, i, n, color=BAR1, sw=3):
    """A grey ring around characters i..i+n of file-name row `row` (mono is fixed pitch: positions are arithmetic)."""
    cx = B60_NAME_X + (i + n / 2) * B60_CW
    ring = Ellipse(width=n * B60_CW + 0.18, height=0.56, color=color, stroke_width=sw).move_to([cx, B60_NAME_Y[row], 0])
    ring._qc_intentional = True                 # an editor's ring around part of a label, by design (layout audit's annotation flag)
    return ring


def b60_rings_for(kind):
    rings = VGroup()
    for r, name in enumerate(B60_NAMES):
        if kind == "date":
            i = name.find("2024-")
            if i >= 0:
                rings.add(b60_ring(r, i, 10))
        elif kind == "version":
            i = name.find("_v0")
            if i >= 0:
                rings.add(b60_ring(r, i + 1, 3))
        else:
            for i, ch in enumerate(name):
                if ch == "_":
                    rings.add(b60_ring(r, i, 1))
    return rings


class B60_DataTree(Scene):
    def construct(self):
        self.add(pb7_title("VI · Data"))
        root = pb7_dirbox(B60_ROOT)
        self.play(FadeIn(root, shift=DOWN * 0.2), FadeIn(pb7_left(M("data/", 32), 0.95, 2.25)), run_time=0.4)
        # three folders drop in under their connectors
        until(self, "Three folders", lead=0.2)
        links = VGroup(*[b60_link(B60_ROOT, k) for k in B60_KIDS])
        self.play(Create(links), run_time=0.4)
        kids = [pb7_dirbox(k) for k in B60_KIDS]
        labels = [M(s, 32).move_to([k.ox, B60_LABEL_Y, 0]) for s, k in zip(B60_KID_NAMES, B60_KIDS)]
        pb7_drop(self, kids, rt=0.6, lag=0.25, dist=3.0)
        self.play(*[FadeIn(l, shift=UP * 0.1) for l in labels], run_time=0.3)
        # each with its own README
        until(self, "Each with its own README", lead=0.2)
        pages = [pb7_page_on(k) for k in B60_KIDS]
        pb7_drop(self, pages, rt=0.5, lag=0.2, dist=2.5)
        self.play(FadeIn(pb7_left(M("README", 32), 4.75, 1.3), shift=LEFT * 0.1), run_time=0.3)
        # raw is read-only: a lock lands beside it, then the command
        until(self, "Make raw read-only", lead=0.2)
        lock = b60_lock(-4.3, 0.75)
        self.play(GrowFromCenter(lock), run_time=0.35)
        until(self, "c h mod", lead=0.1)
        self.play(FadeIn(M("chmod 555", 32).move_to([-3.2, -0.75, 0]), shift=UP * 0.1), run_time=0.3)
        until(self, "only the owner", lead=0.2)
        self.play(GrowFromCenter(Dot([-4.3, 0.75, 0], radius=0.08, color=TERRA)), run_time=0.25)   # the owner's key
        # names that sort themselves
        until(self, "And name files", lead=0.3)
        names = [pb7_left(M(s, 32), B60_NAME_X, y) for s, y in zip(B60_NAMES, B60_NAME_Y)]
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.2) for n in names], lag_ratio=0.3), run_time=0.7)
        until(self, "ISO dates", lead=0.15)
        self.play(Create(b60_rings_for("date")), run_time=0.35)
        until(self, "version numbers", lead=0.15)
        self.play(Create(b60_rings_for("version")), run_time=0.35)
        until(self, "underscores", lead=0.15)
        self.play(Create(b60_rings_for("under")), run_time=0.35)
        done(self)


# ─────────────── B62 · the data dictionary as a table, then 3 copies · 2 media · 1 off-site ───────────────
B62_COLS = ("variable", "type", "units", "range", "missing")
B62_X = (-5.9, -2.45, -0.15, 1.3, 4.75)                              # left edge of each column
B62_ROWS = (("subject_id", "integer", "", "", ""),
            ("age", "integer", "years", "18-65", "-99"),
            ("treatment", "categorical", "", "control/treatment", ""),
            ("response_time", "float", "ms", "200-5000", "-99"))
B62_HY, B62_Y0, B62_DY = 2.55, 1.9, 0.62
B62_L, B62_R = -6.0, 6.0
B62_STAGE = Iso(0.0, -2.35, 0.55)                                    # the backup row's floor
B62_BOX_X = (-4.4, -1.8, 0.8)                                        # the three copies (iso x of each box origin → screen x)


def b62_cell(fn, s, size, col, y):
    if not s:
        return VGroup()
    m = fn(s, size)
    return m.move_to([B62_X[col] + m.width / 2, y, 0])


def b62_row(k):
    cells = B62_ROWS[k]
    y = B62_Y0 - k * B62_DY
    g = VGroup(b62_cell(M, cells[0], 32, 0, y))
    for c in range(1, 5):
        g.add(b62_cell(T, cells[c], 32, c, y))
    return g


def b62_rule(k, sw=3):
    """The grey rule under row k (k = -1 is the rule under the header). Grey: table dividers never ink."""
    y = B62_Y0 - k * B62_DY - B62_DY / 2 + 0.03
    return Line([B62_L, y, 0], [B62_R, y, 0], color=BAR1, stroke_width=sw)


def b62_databox(sx):
    """A copy of the data: a small kraft box with a README page on its lid, standing at screen x = sx on the backup floor."""
    iso = Iso(sx, B62_STAGE.oy, 0.55)
    return VGroup(iso.box(0, 0, 0, 0.9, 0.9, 0.6, sw=3), pb7_page_on(iso))


def b62_disk(sx):
    """A disk under a copy: a dark squat cylinder (ellipse top, dark drum)."""
    top = Ellipse(width=1.25, height=0.5, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([sx, B62_STAGE.oy, 0])
    drum = Rectangle(width=1.25, height=0.3, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to([sx, B62_STAGE.oy - 0.15, 0])
    rim = Arc(radius=0.625, start_angle=PI, angle=PI, color=INK, stroke_width=3).stretch(0.4, 1).move_to([sx, B62_STAGE.oy - 0.3, 0])
    return VGroup(drum, rim, top).set_z_index(-1)


def b62_tape(sx):
    """A tape/cloud block under a copy: a dark block with two ghost ports."""
    iso = Iso(sx, B62_STAGE.oy - 0.22, 0.55)
    return iso.mcp(-0.15, -0.15, 0, 1.2, 1.2, 0.4).set_z_index(-1)


class B62_DictionaryAnd321(Scene):
    def construct(self):
        head = VGroup(*[b62_cell(lambda s, z: T(s, z, bold=True), t, 32, k, B62_HY) for k, t in enumerate(B62_COLS)])
        rules = VGroup(b62_rule(-1, 5), *[b62_rule(k) for k in range(4)])
        self.play(FadeIn(head), run_time=0.35)
        self.play(Create(rules), run_time=0.45)                                             # the frame splits into rows
        until(self, "makes the variables a table", lead=0.3)
        rows = [b62_row(k) for k in range(4)]
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.25) for r in rows], lag_ratio=0.3), run_time=1.0)
        # name, type, units, range, missing: a terracotta dot lands under each header as it is spoken
        for word, col in (("name", 0), ("type", 1), ("units", 2), ("range", 3), ("the missing code", 4)):
            until(self, word, lead=0.1)
            self.play(GrowFromCenter(Dot([B62_X[col] - 0.2, B62_HY, 0], radius=0.08, color=TERRA)), run_time=0.2)
        # three copies land
        until(self, "three copies", lead=0.35)
        boxes = [b62_databox(x) for x in B62_BOX_X]
        pb7_drop(self, boxes, rt=0.5, lag=0.25, dist=3.0, with_=[FadeIn(T("3", 44).move_to([-5.6, -2.0, 0]))])
        # two different media rise under the first two
        until(self, "two different media", lead=0.3)
        self.play(FadeIn(b62_disk(B62_BOX_X[0] - 0.05), shift=UP * 0.15), FadeIn(b62_tape(B62_BOX_X[1]), shift=UP * 0.15),
                  FadeIn(T("2", 44).move_to([-5.6, -2.9, 0])), run_time=0.4)
        # one goes off-site: the third copy rides to a distant plinth
        until(self, "one of them off-site", lead=0.55)
        far = pb7_plinth(Iso(4.6, B62_STAGE.oy, 0.55), -0.25, -0.25, 1.4, 1.4)
        self.play(FadeIn(far), FadeIn(T("1", 44).move_to([3.3, -2.0, 0])), run_time=0.2)
        b3 = boxes[2].set_z_index(5)
        a, b = np.array(b3.get_center()), np.array(b3.get_center()) + np.array([4.6 - B62_BOX_X[2], 0.0, 0.0])
        self.play(MoveAlongPath(b3, ArcBetweenPoints(a, b, angle=-PI / 3)),
                  FadeIn(T("off-site", 34).move_to([4.6, -3.0, 0])), run_time=0.55)
        done(self)


# ─────────────── B80 · five things to keep, each with its cast icon; the exercise card; any improvement counts ───────────────
B80_ROW_Y = (2.05, 1.2, 0.35, -0.5, -1.35)
B80_BOX_X = -5.7
B80_ICON_X = -0.55
B80_ITEMS = ("version control", "environment", "file layout", "documentation", "someone else runs it")
B80_CARD_X0, B80_CARD_X1, B80_CARD_Y0, B80_CARD_Y1 = 0.55, 6.05, -1.95, 2.6
B80_STEPS = ("environment.yml", "conda env create", "source activate", "conda install", "conda env export")
B80_STEP_Y = (1.9, 1.15, 0.4, -0.35, -1.1)
B80_STEP_BOX_X = 1.05
B80_DOT_X = -6.1                             # the "start this way" dots, left of the checkboxes


def b80_box(y, x=B80_BOX_X, stroke=INK):
    return Square(side_length=0.42, fill_color=CARD, fill_opacity=1, stroke_color=stroke, stroke_width=3).move_to([x, y, 0])


def b80_tick(y, x=B80_BOX_X, color=INK):
    return check(x, y - 0.02, 0.18, color, 6)


def b80_icon_versions(x, y):
    """Version control: three pages fanned (the cast page), one terracotta dot each."""
    iso = Iso(x - 0.3, y - 0.45, 0.5)
    return VGroup(*[iso.page(0.08 * k, 0.06 * k, 0.08 * k, 0.9, 1.0) for k in range(3)])


def b80_icon_env(x, y):
    """Environment: the kraft box with one terracotta tape (the cast job box)."""
    return job_box(Iso(x - 0.2, y - 0.5, 0.75))


def b80_icon_layout(x, y):
    """File layout: three small directory boxes in a row (B60's cast)."""
    return VGroup(*[pb7_dirbox(Iso(x - 0.55 + 0.5 * k, y - 0.45, 0.32)) for k in range(3)])


def b80_icon_docs(x, y):
    """Documentation: one README page."""
    return Iso(x - 0.2, y - 0.35, 0.6).page(0, 0, 0, 1.0, 1.1)


def b80_icon_runner(x, y):
    """Someone else runs it: a person token beside a small GPU block."""
    body, light = gpu_block(Iso(x + 0.1, y - 0.45, 0.5))
    return VGroup(pb7_person(x - 0.6, y - 0.4, 0.75), body, light)


def b80_card():
    return RoundedRectangle(width=B80_CARD_X1 - B80_CARD_X0, height=B80_CARD_Y1 - B80_CARD_Y0, corner_radius=0.12,
                            fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4) \
        .move_to([(B80_CARD_X0 + B80_CARD_X1) / 2, (B80_CARD_Y0 + B80_CARD_Y1) / 2, 0])


class B80_FiveAndTheExercise(Scene):
    def construct(self):
        self.add(pb7_title("VIII · Start Tomorrow"))
        rows = VGroup()
        for y, s in zip(B80_ROW_Y, B80_ITEMS):
            bx = b80_box(y)
            rows.add(bx, T(s, 34).next_to(bx, RIGHT, buff=0.35))
        self.play(FadeIn(rows, shift=RIGHT * 0.15), run_time=0.5)
        icons = (b80_icon_versions, b80_icon_env, b80_icon_layout, b80_icon_docs, b80_icon_runner)
        cues = ("Use version control", "Document your environment", "Organise files", "Write the documentation", "And test reproducibility")
        for k, (cue, mk) in enumerate(zip(cues, icons)):
            until(self, cue, lead=0.15)
            icon = mk(B80_ICON_X, B80_ROW_Y[k])
            self.play(Create(b80_tick(B80_ROW_Y[k])), GrowFromCenter(icon), run_time=0.4)
            if k == 4:
                self.play(icon[2].animate.set_color(TERRA), run_time=0.25)                # their machine lights up
        # the exercise card lands
        until(self, "The exercise", lead=0.3)
        card = b80_card()
        steps = VGroup()
        for y, s in zip(B80_STEP_Y, B80_STEPS):
            steps.add(b80_box(y, B80_STEP_BOX_X, stroke=PB7_SMALL), pb7_left(M(s, 32), B80_STEP_BOX_X + 0.45, y))
        pb7_drop(self, [VGroup(card, steps)], rt=0.5, dist=3.5,
                 with_=[FadeIn(T("exercise", 34).move_to([(B80_CARD_X0 + B80_CARD_X1) / 2, 2.95, 0]))])
        for cue, y in zip(("write an environment dot yml", "build it", "activate it", "install a couple more", "export the final file"), B80_STEP_Y):
            until(self, cue, lead=0.15)
            self.play(Create(b80_tick(y, B80_STEP_BOX_X, TERRA)), run_time=0.3)   # terracotta: an ink line inside the card's ink outline fuses (GATE T)
        # start the next project this way
        until(self, "Start the next project", lead=0.2)
        self.play(GrowFromCenter(Dot([B80_DOT_X, B80_ROW_Y[0], 0], radius=0.09, color=TERRA)), run_time=0.25)
        until(self, "document as you go", lead=0.15)
        self.play(GrowFromCenter(Dot([B80_DOT_X, B80_ROW_Y[3], 0], radius=0.09, color=TERRA)), run_time=0.25)
        until(self, "share when you can", lead=0.15)
        self.play(GrowFromCenter(Dot([B80_DOT_X, B80_ROW_Y[4], 0], radius=0.09, color=TERRA)), run_time=0.25)
        # any improvement counts
        until(self, "any improvement counts", lead=0.35)
        self.play(FadeIn(T("any improvement counts", 36).move_to([-2.9, -2.75, 0]), shift=UP * 0.15), run_time=0.45)
        done(self)
