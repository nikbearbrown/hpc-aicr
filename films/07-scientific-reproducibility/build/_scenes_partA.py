# ═════════════════════════════ PART A · Act I (B10) · Act II (B20, B21) · Act III (B30, B32) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PA_ / pa_ / b1x_ / b2x_ / b3x_ so the parts never collide.
PA_KRAFT = "#9C8462"                        # deep kraft: connectors and timelines (ink lines fuse the things they join, GATE T)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only (GATE T)
PA_BELT = "#E4E0D4"                         # belts stay within 28 of the stage (Gate V)


def pa_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_left(mob, x, y):
    """Place a text by its LEFT edge, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pa_right(mob, x, y):
    """Place a text by its RIGHT edge, centred on y."""
    return mob.move_to([x - mob.width / 2, y, 0])


def pa_token(x, y, s=1.0):
    """A person token standing with its feet at (x, y) (same token as the earlier films)."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head).set_z_index(7)


def pa_xmark(x, y, s=0.35, color=BAR1, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w)).set_z_index(8)


def pa_drop(self, mobs, rt=0.55, lag=0.2, dist=5.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt, rate_func=ease_in)


def pa_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PA_BELT, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def pa_calendar(cx, cy, w=1.3, h=1.1):
    """A calendar page: white card, grey outline, ghost day squares, one terracotta day."""
    card = RoundedRectangle(width=w, height=h, corner_radius=0.08, fill_color=CARD, fill_opacity=1,
                            stroke_color=BAR1, stroke_width=4).move_to([cx, cy, 0])
    sq, step = 0.1 * w / 1.3, 0.165 * w / 1.3
    x0, y0 = cx - 3 * step, cy + 0.3 * h / 1.1
    days = VGroup(*[Square(side_length=sq, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([x0 + c * step, y0 - r * step * 1.3, 0])
                    for r in range(4) for c in range(7)])
    mark = Dot([x0 + 2 * step, y0, 0], radius=sq * 0.75, color=TERRA)
    return VGroup(card, days, mark).set_z_index(6)


def pa_gear(cx, cy, r=0.42):
    """A method gear: eight teeth, a grey ring, an open hub. Small object, so dark-kraft outlines."""
    teeth = VGroup(*[Square(side_length=r * 0.38, fill_color=BAR2, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=2)
                     .move_to([cx + r * np.cos(a), cy + r * np.sin(a), 0]).rotate(a) for a in np.arange(0, 2 * PI, PI / 4)])
    ring = Circle(radius=r, fill_color=BAR2, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([cx, cy, 0])
    hub = Circle(radius=r * 0.32, fill_color=STAGE, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([cx, cy, 0])
    return VGroup(teeth, ring, hub)


def pa_page(cx, cy, w=0.9, h=1.1, plot=False, outline=INK, sw=3):
    """A flat 2-D page: a white card with ghost text lines, or a grey result curve (grey inside an ink outline, GATE T)."""
    card = RoundedRectangle(width=w, height=h, corner_radius=0.06, fill_color=CARD, fill_opacity=1,
                            stroke_color=outline, stroke_width=sw).move_to([cx, cy, 0])
    if plot:
        pts = [(0.2, 0.25), (0.4, 0.45), (0.55, 0.38), (0.8, 0.75)]
        inner = VMobject(color=BAR1, stroke_width=4).set_points_as_corners(
            [[cx - w / 2 + w * fx, cy - h / 2 + h * fy, 0] for fx, fy in pts])
        base = Line([cx - w * 0.32, cy - h * 0.3, 0], [cx + w * 0.32, cy - h * 0.3, 0], color=GHOST, stroke_width=4)
        return VGroup(card, base, inner)
    lines = VGroup(*[Line([cx - w * 0.32, cy + h * f, 0], [cx + w * 0.32, cy + h * f, 0], color=GHOST, stroke_width=4)
                     for f in (0.25, 0.08, -0.09, -0.26)])
    return VGroup(card, lines)


def pa_databox(iso, white=False):
    """A data box: closed kraft (the same data) or white (new data)."""
    if white:
        return iso.box(0, 0, 0, 1.0, 1.0, 0.7, PAGE_TOP, PAGE_L, PAGE_R)
    return iso.box(0, 0, 0, 1.0, 1.0, 0.7)


def pa_light_blocks(xs, oy=0.7, s=0.6):
    """Small dark machine blocks with ghost lights (the lights turn terracotta when busy). Returns (blocks, lights)."""
    blocks, lights = VGroup(), VGroup()
    for x in xs:
        body, light = gpu_block(Iso(x, oy, s))
        blocks.add(body)
        lights.add(light)
    return blocks, lights


# ─────────────── B10 · three words: three pipelines, the differences named ───────────────
B10_CX = (-4.3, -0.1, 3.95)                 # column centres
B10_OBJ = -1.0                              # objects sit at cx + B10_OBJ, labels start at cx + B10_LAB
B10_LAB = -0.35
B10_WORDS = ("reproducibility", "replicability", "repeatability")
B10_DOT_X = (-2.25, 5.75)                   # the terracotta dots after the first and third words (fixed: Gate A's stub over-measures text)


def b10_pipeline(k, white=False):
    """data box → gear → result page, stacked vertically, joined by deep-kraft connectors."""
    x = B10_CX[k] + B10_OBJ
    box = pa_databox(Iso(x, 1.0, 0.5), white=white)
    gear = pa_gear(x, 0.0)
    page = pa_page(x, -1.35, 0.9, 1.0, plot=True)
    c1 = Line([x, 0.92, 0], [x, 0.58, 0], color=PA_KRAFT, stroke_width=5)
    c2 = Line([x, -0.58, 0], [x, -0.8, 0], color=PA_KRAFT, stroke_width=5)
    return box, gear, page, c1, c2


def b10_label(s, k, y):
    return pa_left(T(s, 32), B10_CX[k] + B10_LAB, y)


def b10_word(k):
    return T(B10_WORDS[k], 40).move_to([B10_CX[k], 2.35, 0])


class B10_ThreeWords(Scene):
    def construct(self):
        self.add(pa_title("I · Three Words"))
        words = [b10_word(k) for k in range(3)]
        # 1 · reproducibility: same data, same method, another person
        until(self, "Reproducibility:", lead=0.3)
        box, gear, page, c1, c2 = b10_pipeline(0)
        pa_drop(self, [box, gear, page], rt=0.6, lag=0.25, dist=4.0, with_=[FadeIn(words[0])])
        self.play(Create(c1), Create(c2), run_time=0.3)
        until(self, "your same data", lead=0.2)
        self.play(FadeIn(b10_label("same data", 0, 1.45), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "your same methods", lead=0.2)
        self.play(FadeIn(b10_label("same method", 0, 0.0), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "gets your result", lead=0.2)
        pa_drop(self, [pa_token(B10_CX[0] + B10_OBJ, -3.1, 0.85)], rt=0.4, dist=3.0,
                with_=[FadeIn(b10_label("other person", 0, -2.75), shift=RIGHT * 0.15)])
        # 2 · replicability: new data (white), similar method, another team
        until(self, "Replicability:", lead=0.3)
        box, gear, page, c1, c2 = b10_pipeline(1, white=True)
        pa_drop(self, [box, gear, page], rt=0.6, lag=0.25, dist=4.0, with_=[FadeIn(words[1])])
        self.play(Create(c1), Create(c2), run_time=0.3)
        until(self, "collects new data", lead=0.2)
        self.play(FadeIn(b10_label("new data", 1, 1.45), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "uses similar methods", lead=0.2)
        self.play(FadeIn(b10_label("similar method", 1, 0.0), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "finds a comparable result", lead=0.2)
        team = [pa_token(B10_CX[1] + B10_OBJ + dx, -3.1, 0.85) for dx in (-0.6, 0.0, 0.6)]
        pa_drop(self, team, rt=0.5, lag=0.2, dist=3.0, with_=[FadeIn(b10_label("other team", 1, -2.75).shift(RIGHT * 0.45), shift=RIGHT * 0.15)])
        # 3 · repeatability: same data, same method, the same person six months later
        until(self, "Repeatability:", lead=0.3)
        box, gear, page, c1, c2 = b10_pipeline(2)
        pa_drop(self, [box, gear, page], rt=0.6, lag=0.25, dist=4.0, with_=[FadeIn(words[2])])
        self.play(Create(c1), Create(c2), run_time=0.3)
        until(self, "re-run the same methods", lead=0.2)
        self.play(FadeIn(b10_label("same method", 2, 0.0), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "on the same data", lead=0.2)
        self.play(FadeIn(b10_label("same data", 2, 1.45), shift=RIGHT * 0.15), run_time=0.35)
        until(self, "six months later", lead=0.3)
        pa_drop(self, [pa_token(B10_CX[2] - 1.45, -3.1, 0.85)], rt=0.4, dist=3.0)
        cal = pa_calendar(B10_CX[2] - 0.55, -2.7, 0.95, 0.82)
        self.play(GrowFromCenter(cal), FadeIn(pa_left(T("+6 months", 32), B10_CX[2] + 0.15, -2.7), shift=RIGHT * 0.15), run_time=0.4)
        # today: the first and the third
        until(self, "Today is mostly", lead=0.1)
        dots = [Dot([x, 2.35, 0], radius=0.13, color=TERRA) for x in B10_DOT_X]
        self.play(*[GrowFromCenter(d) for d in dots], run_time=0.4)
        done(self)


# ─────────────── B20 · the crisis in numbers: the Nature survey (approx.) and three studies ───────────────
B20_LAB_R = -4.5                            # right edge of the field labels (left panel)
B20_BAR_X0 = -4.3                           # bars start here; 100 % = B20_BAR_W
B20_BAR_W = 3.3
B20_ROWS = (("chemistry", 87, 1.75), ("biology", 77, 1.05), ("physics", 69, 0.35), ("medicine", 67, -0.35), ("earth", 64, -1.05))
B20_RX0, B20_RX1 = 0.25, 6.05               # right panel span
B20_STATS = (("psychology", "36–47 of 100", (0.36, 0.47), "Open Science Collaboration, 2015", 2.1),
             ("cancer", "11% of 53", (0.11, None), "Begley & Ellis, 2012", 0.35),
             ("economics", "49%", (0.49, None), "Chang & Li, 2015", -1.4))


def b20_bar(pct, y, h=0.44):
    w = B20_BAR_W * pct / 100
    return Rectangle(width=w, height=h, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([B20_BAR_X0 + w / 2, y, 0])


def b20_num(pct, y):
    return pa_left(T(f"{pct}%", 32), B20_BAR_X0 + B20_BAR_W * pct / 100 + 0.2, y)


def b20_track(y, h=0.4):
    return Rectangle(width=B20_RX1 - B20_RX0, height=h, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([(B20_RX0 + B20_RX1) / 2, y, 0])


def b20_fill(frac, y, x0=None, fill=BAR1, h=0.4):
    x0 = B20_RX0 if x0 is None else x0
    x1 = B20_RX0 + (B20_RX1 - B20_RX0) * frac
    return Rectangle(width=x1 - x0, height=h, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([(x0 + x1) / 2, y, 0])


def b20_stat(k):
    """(label, hero numeral, track, fills, citation) for stat row k; rows are label / bar / citation."""
    name, hero, (f0, f1), cite, yt = B20_STATS[k]
    yb = yt - 0.55
    track = b20_track(yb)
    fills = [b20_fill(f0, yb)]
    if f1:
        fills.append(b20_fill(f1, yb, x0=B20_RX0 + (B20_RX1 - B20_RX0) * f0 + 0.06, fill=BAR2))
    # the citation hangs under its track by next_to (no explicit coordinate: Gate A's stub over-measures long text)
    return (pa_left(T(name, 34), B20_RX0, yt), pa_right(T(hero, 36), B20_RX1, yt), track, fills,
            T(cite, 32).next_to(track, DOWN, buff=0.14, aligned_edge=LEFT))


class B20_TheCrisis(Scene):
    def construct(self):
        self.add(pa_title("II · Why It Matters"))
        # the survey panel: field labels, a grey axis, the 'approx.' tag and the 'failed to reproduce' header
        until(self, "In 2016 a Nature survey", lead=0.3)
        labels = VGroup(*[pa_right(T(name, 32), B20_LAB_R, y) for name, _, y in B20_ROWS])
        axis = Line([B20_BAR_X0 - 0.05, 2.05, 0], [B20_BAR_X0 - 0.05, -1.4, 0], color=BAR2, stroke_width=4)
        head = pa_left(T("failed to reproduce", 32), -6.1, 2.45)
        approx = pa_left(T("approx.", 32), -2.0, 2.45)
        self.play(FadeIn(labels, shift=RIGHT * 0.15), Create(axis), FadeIn(head), FadeIn(approx), run_time=0.5)
        until(self, "in chemistry", lead=0.2)
        self.play(GrowFromEdge(b20_bar(87, 1.75), LEFT), FadeIn(b20_num(87, 1.75)),
                  FadeIn(pa_left(T("Nature survey, 2016", 32), -6.1, -1.95), shift=UP * 0.15), run_time=0.5)
        until(self, "in biology", lead=0.2)
        self.play(GrowFromEdge(b20_bar(77, 1.05), LEFT), FadeIn(b20_num(77, 1.05)), run_time=0.45)
        until(self, "in physics", lead=0.2)
        self.play(GrowFromEdge(b20_bar(69, 0.35), LEFT), FadeIn(b20_num(69, 0.35)), run_time=0.4)
        until(self, "medicine and earth science", lead=0.2)
        self.play(GrowFromEdge(b20_bar(67, -0.35), LEFT), FadeIn(b20_num(67, -0.35)),
                  GrowFromEdge(b20_bar(64, -1.05), LEFT), FadeIn(b20_num(64, -1.05)), run_time=0.45)
        # three studies: the rows land as they are named
        until(self, "Other studies", lead=0.2)
        rows = [b20_stat(k) for k in range(3)]
        self.play(*[FadeIn(r[2]) for r in rows], run_time=0.4)
        for k, cue in enumerate(("In psychology", "In biomedicine", "In economics")):
            until(self, cue, lead=0.2)
            name, hero, track, fills, cite = rows[k]
            self.play(FadeIn(name, shift=RIGHT * 0.15), *[GrowFromEdge(f, LEFT) for f in fills], run_time=0.5)
            self.play(FadeIn(hero, shift=LEFT * 0.15), FadeIn(cite, shift=UP * 0.1), run_time=0.4)
        done(self)


# ─────────────── B21 · it bites you first: six months later, redo the plot; then the five culprits ───────────────
B21_DESK = Iso(-3.3, 0.35, 0.75)
B21_TOKEN_X = -5.1
B21_CAL = (-0.7, 1.9)
B21_BLOCKS = (2.3, 3.5, 4.7)
B21_CARD_X = (-4.9, -2.45, 0.0, 2.45, 4.9)
B21_CARD_Y = -1.5
B21_LABELS = ("no methods", "not shared", "no versions", "one machine", "absolute paths")
B21_CUES = ("methods not documented", "data and code not shared", "software versions not recorded", "depend on one machine",
            "absolute file paths")


def b21_desk():
    return B21_DESK.box(0, 0, 0, 2.2, 1.3, 0.55)


def b21_plot_page():
    """The plot page lying on the desk top: white slab, ghost base line, grey result curve."""
    iso, z = B21_DESK, 0.55
    slab = iso.box(0.25, 0.15, z, 0.85, 1.0, 0.05, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
    zt = z + 0.05
    base = Line(iso.p(0.4, 0.3, zt), iso.p(0.4, 1.0, zt), color=GHOST, stroke_width=4)
    curve = VMobject(color=GHOST, stroke_width=5).set_points_as_corners(
        [iso.p(0.45, 0.3, zt), iso.p(0.7, 0.5, zt), iso.p(0.6, 0.7, zt), iso.p(0.95, 1.0, zt)])
    return VGroup(slab, base, curve).set_z_index(3)


def b21_model_page():
    iso, z = B21_DESK, 0.55
    slab = iso.box(1.4, 0.2, z, 0.75, 0.9, 0.05, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
    zt = z + 0.05
    lines = VGroup(*[Line(iso.p(1.55, 0.2 + 0.9 * f, zt), iso.p(2.0, 0.2 + 0.9 * f, zt), color=GHOST, stroke_width=4) for f in (0.3, 0.5, 0.7)])
    return VGroup(slab, lines).set_z_index(3)


def b21_ring():
    # a terracotta dot beside the page (a ring over the page merged with the plot curve under GATE T §8.6b)
    c = B21_DESK.p(0.68, 1.35, 0.6)
    return Dot(c, radius=0.14, color=TERRA).set_z_index(5)


def b21_card(k):
    return RoundedRectangle(width=2.2, height=1.5, corner_radius=0.1, fill_color=CARD, fill_opacity=1,
                            stroke_color=INK, stroke_width=3).move_to([B21_CARD_X[k], B21_CARD_Y, 0])


def b21_glyph(k):
    """The barrier glyph inside card k. Grey / dark-kraft outlines only: these sit inside an ink outline."""
    cx, cy = B21_CARD_X[k], B21_CARD_Y
    if k == 0:      # no methods: a page with the method lines missing
        page = RoundedRectangle(width=0.8, height=1.0, corner_radius=0.05, fill_color=CARD, fill_opacity=1,
                                stroke_color=BAR1, stroke_width=3).move_to([cx, cy, 0])
        line = Line([cx - 0.25, cy + 0.3, 0], [cx + 0.25, cy + 0.3, 0], color=BAR1, stroke_width=4)
        ghosts = VGroup(*[DashedLine([cx - 0.25, cy + f, 0], [cx + 0.25, cy + f, 0], color=GHOST, stroke_width=4, dash_length=0.08)
                          for f in (0.08, -0.14, -0.36)])
        return VGroup(page, line, ghosts)
    if k == 1:      # not shared: a closed kraft box, outlined in dark kraft
        iso = Iso(cx, cy - 0.55, 0.5)
        return VGroup(*[Polygon(*pts, fill_color=f, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3) for pts, f in (
            ([iso.p(0, 0, 0), iso.p(0, 1, 0), iso.p(0, 1, 0.8), iso.p(0, 0, 0.8)], BOX_L),
            ([iso.p(0, 0, 0), iso.p(1, 0, 0), iso.p(1, 0, 0.8), iso.p(0, 0, 0.8)], BOX_R),
            ([iso.p(0, 0, 0.8), iso.p(1, 0, 0.8), iso.p(1, 1, 0.8), iso.p(0, 1, 0.8)], BOX_TOP))])
    if k == 2:      # no versions: one page, the earlier versions only ghosts
        return VGroup(*[RoundedRectangle(width=0.7, height=0.9, corner_radius=0.05, fill_color=CARD, fill_opacity=1,
                                         stroke_color=col, stroke_width=3).move_to([cx + d, cy - d, 0])
                        for d, col in ((0.22, GHOST), (0.11, BAR2), (0.0, BAR1))])
    if k == 3:      # one machine: a laptop
        screen = RoundedRectangle(width=1.0, height=0.65, corner_radius=0.04, fill_color=GHOST, fill_opacity=1,
                                  stroke_color=BAR1, stroke_width=3).move_to([cx, cy + 0.12, 0])
        base = Polygon([cx - 0.65, cy - 0.3, 0], [cx + 0.65, cy - 0.3, 0], [cx + 0.55, cy - 0.2, 0], [cx - 0.55, cy - 0.2, 0],
                       fill_color=BAR2, fill_opacity=1, stroke_color=BAR1, stroke_width=3)
        return VGroup(screen, base)
    # absolute paths: a folder chain stepping down from the root, joined in deep kraft
    folders, links = VGroup(), VGroup()
    for i in range(3):
        fx, fy = cx - 0.55 + i * 0.5, cy + 0.4 - i * 0.4
        folders.add(Rectangle(width=0.5, height=0.32, fill_color=BOX_TOP, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3).move_to([fx, fy, 0]))
        if i:
            links.add(Line([fx - 0.5, fy + 0.22, 0], [fx - 0.5, fy, 0], color=PA_KRAFT, stroke_width=3),
                      Line([fx - 0.5, fy, 0], [fx - 0.25, fy, 0], color=PA_KRAFT, stroke_width=3))
    return VGroup(links, folders)


class B21_FiveBarriers(Scene):
    def construct(self):
        desk, token = b21_desk(), pa_token(B21_TOKEN_X, 0.35)
        self.add(desk, token)
        # the real world: the plot behind a clinical decision, the model behind a policy
        until(self, "clinical decisions", lead=0.3)
        plot = b21_plot_page()
        pa_drop(self, [plot], rt=0.45, dist=2.5)
        until(self, "policy built on models", lead=0.3)
        model = b21_model_page()
        pa_drop(self, [model], rt=0.45, dist=2.5)
        # it bites you first: six months later the plot is asked for again
        until(self, "it bites you first", lead=0.2)
        self.play(token.animate.shift(UP * 0.3), run_time=0.4, rate_func=there_and_back)
        until(self, "something has to be redone", lead=0.3)
        cal = pa_calendar(*B21_CAL)
        self.play(GrowFromCenter(cal), run_time=0.4)
        leaf = cal[0].copy().set_z_index(7)
        self.play(leaf.animate.shift(UP * 0.9).set_opacity(0), FadeIn(pa_left(T("+6 months", 32), 0.2, 1.9), shift=UP * 0.15), run_time=0.5)
        self.remove(leaf)
        until(self, "a plot", lead=0.1)
        self.play(GrowFromCenter(b21_ring()), run_time=0.4)
        # the faster that is: the pipeline re-runs in minutes
        until(self, "the faster that is", lead=0.3)
        blocks, lights = pa_light_blocks(B21_BLOCKS)
        pa_drop(self, list(blocks), rt=0.5, lag=0.2, dist=3.0)
        self.add(lights)
        rt = guard(self, 0.6)
        self.play(LaggedStart(*[l.animate.set_color(TERRA) for l in lights], lag_ratio=0.4), run_time=rt)
        until(self, "the faster you publish", lead=0.2)
        self.play(FadeIn(T("redo in minutes", 32).move_to([3.5, 2.3, 0]), shift=UP * 0.15), run_time=0.4)
        # the five culprits
        until(self, "The usual culprits are five", lead=0.1)
        cards = [VGroup(b21_card(k), b21_glyph(k)) for k in range(5)]
        pa_drop(self, cards, rt=0.7, lag=0.15, dist=5.0)
        self.play(*[FadeIn(T(s, 32).move_to([x, -2.75, 0])) for s, x in zip(B21_LABELS, B21_CARD_X)], run_time=0.35)
        for k, cue in enumerate(B21_CUES):
            until(self, cue, lead=0.1)
            self.play(Create(pa_xmark(B21_CARD_X[k], B21_CARD_Y, 0.55, BAR1, 10)), run_time=0.3)
        done(self)


# ─────────────── B30 · the checklist in three phases, ticking as named, a belt running under ───────────────
B30_COL_X = (-5.95, -1.95, 2.15)            # left edge of each column
B30_HEADS = ("setup", "during", "completion")
B30_ROW_Y = (1.55, 0.95, 0.35, -0.25, -0.85)
B30_BELT_Y = -2.6
B30_BOX_X = (-4.3, -0.3, 3.8)               # where the box rests under each column
B30_ITEMS = ((("Git repository", T, "a Git repository"), ("folder layout", T, "a consistent folder layout"),
              ("environment", T, "a documented environment"), ("README", M, "a README")),
             (("commented code", T, "commented code"), ("relative paths", T, "relative paths"), ("random seeds", T, "random seeds set"),
              ("transformations", T, "every data transformation"), ("regular commits", T, "regular commits")),
             (("someone else runs", T, "have someone else run it"), ("environment file", T, "ship the environment file"),
              ("instructions", T, "and the instructions"), ("data and code", T, "share the data and the code"),
              ("limitations", T, "write down the limitations")))


def b30_box(x, y):
    return Square(side_length=0.4, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x + 0.2, y, 0])


def b30_tick(x, y):
    return check(x + 0.2, y - 0.02, 0.17, INK, 6)


def b30_crate(x):
    return Iso(x, B30_BELT_Y + 0.15, 0.55).box(0, 0, 0, 0.9, 0.9, 0.6).set_z_index(2)


class B30_ThreePhaseChecklist(Scene):
    def construct(self):
        self.add(pa_title("III · The Checklist"))
        heads = VGroup(*[pa_left(T(h, 36, bold=True), x, 2.3) for h, x in zip(B30_HEADS, B30_COL_X)])
        rows = VGroup()
        for col, items in enumerate(B30_ITEMS):
            for (s, f, _), y in zip(items, B30_ROW_Y):
                bx = b30_box(B30_COL_X[col], y)
                rows.add(bx, f(s, 32).next_to(bx, RIGHT, buff=0.3))
        belt = pa_belt(-6.0, 5.7, B30_BELT_Y)
        self.add(heads, rows, belt)
        crate = b30_crate(B30_BOX_X[0])
        until(self, "At setup", lead=0.3)
        pa_drop(self, [crate], rt=0.45, dist=3.0)
        for col, (items, move_cue) in enumerate(zip(B30_ITEMS, (None, "During the work", "At the end"))):
            if move_cue:
                until(self, move_cue, lead=0.3)
                self.play(crate.animate.shift(RIGHT * (B30_BOX_X[col] - B30_BOX_X[col - 1])), run_time=0.6)
            for (s, f, cue), y in zip(items, B30_ROW_Y):
                until(self, cue, lead=0.1)
                self.play(Create(b30_tick(B30_COL_X[col], y)), run_time=0.3)
        top = Iso(B30_BOX_X[2], B30_BELT_Y + 0.15, 0.55).p(0.45, 0.45, 0.6)
        self.play(GrowFromCenter(Dot(top, radius=0.1, color=TERRA).set_z_index(3)), run_time=0.3)
        done(self)


# ─────────────── B32 · version control in one breath: commits, revert, collaborate, history, a branch ───────────────
B32_Y = -0.5                                # the main line
B32_X = (-4.4, -2.95, -1.5, -0.05, 1.4, 4.3)  # commit dots; the last is the merge commit
B32_BRANCH = (2.85, 0.7)                    # the experiment commit, off the line
B32_PAGE = (-4.6, 1.5)
B32_TOKENS = (-0.05, 1.4)


def b32_dot(k):
    return Dot([B32_X[k], B32_Y, 0], radius=0.15, color=INK).set_z_index(4)


def b32_line():
    return Line([-5.2, B32_Y, 0], [5.1, B32_Y, 0], color=PA_KRAFT, stroke_width=6)


def b32_page_line(k):
    """The k-th grey text line on the file page (one per commit)."""
    cx, cy = B32_PAGE
    return Line([cx - 0.4, cy + 0.5 - k * 0.28, 0], [cx + 0.4, cy + 0.5 - k * 0.28, 0], color=BAR1, stroke_width=4)


def b32_revert():
    a, b = np.array([B32_X[2], B32_Y + 0.22, 0]), np.array([B32_X[0], B32_Y + 0.22, 0])
    return CurvedArrow(a, b, angle=PI / 2.2, color=PA_KRAFT, stroke_width=5, tip_length=0.22)


def b32_branch():
    x5, (xb, yb), x6 = B32_X[4], B32_BRANCH, B32_X[5]
    up = Line([x5 + 0.12, B32_Y + 0.12, 0], [xb - 0.15, yb - 0.1, 0], color=PA_KRAFT, stroke_width=5)
    down = Line([xb + 0.15, yb - 0.1, 0], [x6 - 0.12, B32_Y + 0.12, 0], color=PA_KRAFT, stroke_width=5)
    return up, down, Dot([xb, yb, 0], radius=0.15, color=TERRA).set_z_index(4)


def b32_bracket():
    y = B32_Y - 0.7
    return VGroup(Line([B32_X[0], y, 0], [B32_X[5], y, 0], color=BAR1, stroke_width=4),
                  Line([B32_X[0], y, 0], [B32_X[0], y + 0.18, 0], color=BAR1, stroke_width=4),
                  Line([B32_X[5], y, 0], [B32_X[5], y + 0.18, 0], color=BAR1, stroke_width=4))


class B32_VersionControl(Scene):
    def construct(self):
        page = pa_page(*B32_PAGE, 1.3, 1.6)
        self.add(b32_line(), page[0])
        # every change is recorded: three commits, the page gains a line each time
        until(self, "every change is recorded", lead=0.3)
        plines = [b32_page_line(k) for k in range(3)]
        for k in range(3):
            self.play(GrowFromCenter(b32_dot(k)), Create(plines[k]), run_time=0.3)
        # revert: back two dots, the page restores
        until(self, "revert to any earlier version", lead=0.3)
        self.play(Create(b32_revert()), FadeIn(T("revert", 32).move_to([-2.95, 1.1, 0]), shift=DOWN * 0.1), run_time=0.5)
        self.play(FadeOut(VGroup(*plines[1:])), run_time=0.3)
        # collaborate: two people commit to the same line
        until(self, "collaborate without overwriting", lead=0.3)
        toks = [pa_token(x, -3.05, 0.9) for x in B32_TOKENS]
        pa_drop(self, toks, rt=0.4, lag=0.2, dist=3.0, with_=[FadeIn(pa_left(T("collaborate", 32), 2.1, -2.6))])
        d3, d4 = b32_dot(3).shift(DOWN * 1.6), b32_dot(4).shift(DOWN * 1.6)
        self.add(d3, d4)
        self.play(d3.animate.shift(UP * 1.6), d4.animate.shift(UP * 1.6), run_time=0.45)
        # keep the whole history: a bracket under the line
        until(self, "keep the whole history", lead=0.2)
        self.play(Create(b32_bracket()), FadeIn(pa_left(T("history", 32), -5.2, -1.65)), run_time=0.4)
        # experiment on a branch, merge back
        until(self, "experiment on a branch", lead=0.3)
        up, down, exp = b32_branch()
        self.play(Create(up), run_time=0.3)
        self.play(GrowFromCenter(exp), FadeIn(T("branch", 32).move_to([B32_BRANCH[0], 1.3, 0]), shift=DOWN * 0.1), run_time=0.3)
        until(self, "without breaking", lead=0.2)
        self.play(Create(down), GrowFromCenter(b32_dot(5)), run_time=0.4)
        done(self)
