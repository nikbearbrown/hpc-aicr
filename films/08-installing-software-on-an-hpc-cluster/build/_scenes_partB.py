# ═════════════════════════════ PART B · B40 (Act IV) · B51, B52 (Act V) · B61 (Act VI) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB8_ / pb8_ / b40_ / b51_ / b52_ / b61_ so the parts never collide.
PB8_SMALL = "#917A55"                       # dark kraft: outlines of SMALL objects only (GATE T)
PB8_LINK = "#9C8462"                        # deep kraft: connectors (ink-edged connectors fuse objects into one blob)
PB8_BELT = "#E4E0D4"                        # belts stay within 28 of the stage (Gate V)
PB8_CW = 8.46 / 34                          # Menlo at 32: screen units per character (measured)


def pb8_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb8_left(mob, x, y):
    """Place a text by its LEFT edge, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def pb8_drop(self, mobs, rt=0.5, lag=0.2, dist=4.0, with_=()):
    """Drop objects in from above, fully opaque (GATE T: never a half-faded block). Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt, rate_func=ease_in)


def pb8_slide(self, mobs, rt=0.5, lag=0.2, dist=4.0, with_=()):
    """Slide objects in from the left, fully opaque. Guard first, then stage."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(LEFT * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(RIGHT * dist) for m in mobs], lag_ratio=lag), *with_, run_time=rt)


def pb8_xmark(x, y, s=0.3, color=BAR1, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w)).set_z_index(8)


def pb8_page(cx, cy, w=0.9, h=1.1, outline=INK, sw=3, fill=CARD):
    """A flat page: a card with ghost text lines (grey outline when it sits inside another outline, GATE T)."""
    card = RoundedRectangle(width=w, height=h, corner_radius=0.06, fill_color=fill, fill_opacity=1,
                            stroke_color=outline, stroke_width=sw).move_to([cx, cy, 0])
    lines = VGroup(*[Line([cx - w * 0.3, cy + h * f, 0], [cx + w * 0.3, cy + h * f, 0], color=GHOST, stroke_width=4)
                     for f in (0.24, 0.06, -0.12, -0.3)])
    return VGroup(card, lines)


def pb8_gear(cx, cy, r=0.42):
    """A build gear: eight teeth, a grey ring, an open hub. Small object, so dark-kraft outlines."""
    teeth = VGroup(*[Square(side_length=r * 0.38, fill_color=BAR2, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=2)
                     .move_to([cx + r * np.cos(a), cy + r * np.sin(a), 0]).rotate(a) for a in np.arange(0, 2 * PI, PI / 4)])
    ring = Circle(radius=r, fill_color=BAR2, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=3).move_to([cx, cy, 0])
    hub = Circle(radius=r * 0.32, fill_color=STAGE, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=3).move_to([cx, cy, 0])
    return VGroup(teeth, ring, hub)


def pb8_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PB8_BELT, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def pb8_weight(cx, cy, w=0.95, h=0.5):
    """A grey weight: a trapezoid block with a handle arc on top (the 'heavy' glyph, same in B40 and B52)."""
    body = Polygon([cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy - h / 2, 0], [cx + w * 0.36, cy + h / 2, 0], [cx - w * 0.36, cy + h / 2, 0],
                   fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    handle = Arc(radius=0.2, start_angle=0, angle=PI, color=INK, stroke_width=6).move_to([cx, cy + h / 2 + 0.12, 0])
    return VGroup(handle, body)


def pb8_pill(text, x, y, w, fill=GHOST, fn=T):
    """A label on a pill: grey or kraft fill, no outline, ink text (never terracotta)."""
    return VGroup(pill(x, y, w, 0.62, fill), fn(text, 32).move_to([x, y, 0]))


def pb8_dot(x, y, r=0.1):
    """A small grey node (graph glyphs): grey fill, dark-kraft outline."""
    return Circle(radius=r, fill_color=BAR1, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=2).move_to([x, y, 0])


# ─────────────── B40 · the Spack spec: package @version %compiler +variant, then the dependency tree it resolves ───────────────
B40_SPEC = (("hdf5", "package"), ("@1.14.3", "version"), ("%gcc@12.2.0", "compiler"), ("+mpi", "variant"))
B40_SPEC_Y, B40_LAB_Y = 1.45, 0.7
B40_ROOT = (0.0, -0.35)
B40_KIDS = ((-2.6, -1.5), (0.0, -1.5), (2.6, -1.5))
B40_GRAND = ((-2.6, -2.65), (2.6, -2.65))
B40_R = 0.34
B40_SRC = (-5.5, 1.3)                       # the source page, left margin
B40_VER_X = (4.3, 5.05, 5.8)                # three versions side by side, right margin
B40_VER_Y = -1.05


def b40_parts():
    """The four mono parts of the spec, laid out in a row centred on x = 0 (fixed gaps)."""
    parts = [M(s, 36) for s, _ in B40_SPEC]
    total = sum(p.width for p in parts) + 0.6 * 3
    x = -total / 2
    for p in parts:
        p.move_to([x + p.width / 2, B40_SPEC_Y, 0])
        x += p.width + 0.6
    return parts


def b40_label(k, parts):
    return T(B40_SPEC[k][1], 32).move_to([parts[k].get_center()[0], B40_LAB_Y, 0])


def b40_ring(part):
    """A grey editor's ring around one part of the spec (ink rings around text fuse into one blob, GATE T)."""
    ring = Ellipse(width=part.width + 0.4, height=0.78, color=BAR1, stroke_width=3).move_to(np.array(part.get_center()))
    ring._qc_intentional = True
    return ring


def b40_node(x, y):
    return Circle(radius=B40_R, fill_color=CARD, fill_opacity=1, stroke_color=PB8_SMALL, stroke_width=3).move_to([x, y, 0])


def b40_link(a, b):
    """Elbow connector from node a's base to node b's top, deep kraft, stopping short of both."""
    x0, y0 = a[0], a[1] - B40_R - 0.08
    x1, y1 = b[0], b[1] + B40_R + 0.08
    if abs(x0 - x1) < 0.01:
        return VGroup(Line([x0, y0, 0], [x1, y1, 0], color=PB8_LINK, stroke_width=4))
    ym = (y0 + y1) / 2
    return VGroup(Line([x0, y0, 0], [x0, ym, 0], color=PB8_LINK, stroke_width=4),
                  Line([x0, ym, 0], [x1, ym, 0], color=PB8_LINK, stroke_width=4),
                  Line([x1, ym, 0], [x1, y1, 0], color=PB8_LINK, stroke_width=4))


def b40_version_box(x):
    return Iso(x, B40_VER_Y, 0.45).box(0, 0, 0, 0.8, 0.8, 0.6, sw=3)


class B40_TheSpackSpec(Scene):
    def construct(self):
        self.play(FadeIn(pb8_title("IV · Spack")), run_time=0.3)
        # builds from source: a source page lands at the left margin
        until(self, "builds from source", lead=0.3)
        src = pb8_page(*B40_SRC)
        pb8_drop(self, [src], rt=0.45, dist=3.0, with_=[FadeIn(T("source", 32).move_to([B40_SRC[0], 2.2, 0]))])
        # many versions side by side: three small boxes at the right margin
        until(self, "many versions", lead=0.3)
        pb8_drop(self, [b40_version_box(x) for x in B40_VER_X], rt=0.55, lag=0.25, dist=3.0)
        self.play(FadeIn(T("versions", 32).move_to([5.05, -1.95, 0]), shift=UP * 0.1), run_time=0.3)
        # the honest note: a grey caveat pill, top-right; heavy: the weight glyph under it
        until(self, "One honest note", lead=0.2)
        self.play(FadeIn(pb8_pill("not the first option", 4.3, 2.95, 3.7), shift=DOWN * 0.2), run_time=0.4)
        until(self, "are heavy", lead=0.1)
        pb8_drop(self, [pb8_weight(4.3, 2.1)], rt=0.4, dist=2.0)
        # if a module or Conda covers you, use that: a check beside the words
        until(self, "If a module or Conda", lead=0.2)
        self.play(FadeIn(T("module · Conda", 32).move_to([4.75, 0.0, 0]), shift=LEFT * 0.15), run_time=0.3)
        until(self, "use that", lead=0.1)
        self.play(Create(check(3.0, 0.0, 0.18, INK, 6)), run_time=0.3)
        # the spec builds, one part at a time, each with its label
        parts = b40_parts()
        for k, cue in enumerate(("package, at version", "at version", "percent compiler", "plus variant")):
            until(self, cue, lead=0.15)
            self.play(FadeIn(parts[k], shift=UP * 0.15), FadeIn(b40_label(k, parts)), run_time=0.3)
        # each part ringed as it is named
        for k, cue in enumerate(("H D F five", "one point fourteen", "percent G C C", "plus M P I")):
            until(self, cue, lead=0.1)
            self.play(Create(b40_ring(parts[k])), run_time=0.3)
        # the dependency tree grows downward from the hdf5 node
        until(self, "resolves the whole", lead=0.3)
        nodes = [b40_node(*B40_ROOT)] + [b40_node(*k) for k in B40_KIDS] + [b40_node(*g) for g in B40_GRAND]
        links = VGroup(*[b40_link(B40_ROOT, k) for k in B40_KIDS], b40_link(B40_KIDS[0], B40_GRAND[0]), b40_link(B40_KIDS[2], B40_GRAND[1]))
        self.play(GrowFromCenter(nodes[0]), run_time=0.25)
        self.play(Create(links), LaggedStart(*[GrowFromCenter(n) for n in nodes[1:]], lag_ratio=0.2), run_time=0.8)
        # builds each piece: nodes tint kraft from the leaves up
        until(self, "builds each piece", lead=0.2)
        order = [nodes[4], nodes[5], nodes[1], nodes[2], nodes[3], nodes[0]]
        self.play(LaggedStart(*[n.animate.set_fill(BOX_L) for n in order], lag_ratio=0.25), run_time=1.2)
        until(self, "exactly those choices", lead=0.1)
        self.play(GrowFromCenter(Dot([0.75, B40_ROOT[1], 0], radius=0.09, color=TERRA)), run_time=0.25)
        done(self)


# ─────────────── B51 · three flags into a config file; EasyBuild's output is a modulefile; module use, module load ───────────────
B51_FLAGS = (("--modules-tool=EnvironmentModules", "not Lmod", "Modules tool equals", "this cluster does not run it"),
             ("--module-syntax=Tcl", "not Lua", "Module syntax equals", "will not load here"),
             ("--installpath=$HOME/easybuild", "your space", "And install path", "you cannot write"))
B51_ROW_Y = (2.55, 1.75, 0.95)
B51_X0 = -5.9
B51_CFG = (5.2, -0.35)                      # the config page
B51_GEAR = (-4.6, -0.6)
B51_PAGE_OUT = (-2.4, -0.6)                 # where the emitted modulefile page pauses
B51_DIR = Iso(0.15, -1.1, 0.6)              # the modules folder
B51_PATH_Y = -1.45
B51_CMD_Y = (-2.2, -2.95)


def b51_mono(s, y, x0=B51_X0):
    """A mono line placed by its left edge, by character count (fixed pitch; Gate A's stub over-measures long text)."""
    return M(s, 32).move_to([x0 + len(s) * PB8_CW / 2, y, 0])


def b51_flag(k):
    return b51_mono(B51_FLAGS[k][0], B51_ROW_Y[k])


def b51_reason(k):
    return pb8_left(T(B51_FLAGS[k][1], 32), B51_X0 + len(B51_FLAGS[k][0]) * PB8_CW + 0.5, B51_ROW_Y[k])


def b51_gather(k):
    """One short grey line landing on the config page: the flag, gathered."""
    cx, cy = B51_CFG
    return Line([cx - 0.27, cy + 0.26 - 0.26 * k, 0], [cx + 0.27, cy + 0.26 - 0.26 * k, 0], color=BAR1, stroke_width=5)


def b51_dirbox():
    return B51_DIR.box(0, 0, 0, 1.0, 1.0, 0.65, sw=3)


class B51_ThreeFlagsToModulefile(Scene):
    def construct(self):
        # the EasyBuild gear is the act's cast: on stage from the first frame, with its name beside it
        gear = pb8_gear(*B51_GEAR)
        self.add(gear, T("EasyBuild", 32).move_to([B51_GEAR[0], B51_PATH_Y, 0]))
        self.play(FadeIn(pb8_page(*B51_CFG, w=0.9, h=1.1)), FadeIn(M("config.cfg", 32).move_to([4.9, 0.5, 0])), run_time=0.3)
        # three flags land one by one, each followed by its reason
        for k in range(3):
            until(self, B51_FLAGS[k][2], lead=0.2)
            flag = b51_flag(k)
            self.play(FadeIn(flag, shift=RIGHT * 0.2), run_time=0.3)
            until(self, B51_FLAGS[k][3], lead=0.1)
            self.play(FadeIn(b51_reason(k), shift=LEFT * 0.1), run_time=0.3)
        # put them in a config file once: three lines land on the page
        until(self, "Put them in a config", lead=0.2)
        self.play(LaggedStart(*[Create(b51_gather(k)) for k in range(3)], lag_ratio=0.3), run_time=0.7)
        # the output is a modulefile: the gear turns and emits a page
        until(self, "EasyBuild's output", lead=0.2)
        page = pb8_page(B51_GEAR[0] + 0.3, B51_GEAR[1], w=0.75, h=0.9, outline=DIM).set_z_index(3)
        self.add(page)
        self.play(Rotate(gear, angle=PI / 2), page.animate.move_to([B51_PAGE_OUT[0], B51_PAGE_OUT[1], 0]), run_time=0.6)
        self.play(FadeIn(T("modulefile", 32).move_to([B51_PAGE_OUT[0], 0.15, 0])), run_time=0.25)
        # it slides into the modules folder, whose path is named beneath
        until(self, "Point module at its directory", lead=0.3)
        folder = b51_dirbox()
        pb8_drop(self, [folder], rt=0.4, dist=2.5)
        top = B51_DIR.p(0.5, 0.5, 0.65)
        self.play(page.animate.scale(0.75).move_to([top[0], top[1] + 0.25, 0]), run_time=0.45)
        self.play(FadeIn(M("$HOME/easybuild/modules/all", 32).move_to([0.5, B51_PATH_Y, 0])), run_time=0.25)
        # module use, module load, a check
        until(self, "module use", lead=0.15)
        self.play(FadeIn(b51_mono("module use $HOME/easybuild/modules/all", B51_CMD_Y[0]), shift=RIGHT * 0.2), run_time=0.3)
        until(self, "module load", lead=0.15)
        load = b51_mono("module load HDF5/1.14.3-gompi-2023a", B51_CMD_Y[1])
        self.play(FadeIn(load, shift=RIGHT * 0.2), run_time=0.3)
        until(self, "like any preinstalled", lead=0.1)
        self.play(Create(check(B51_X0 + len("module load HDF5/1.14.3-gompi-2023a") * PB8_CW + 0.6, B51_CMD_Y[1], 0.18, INK, 6)), run_time=0.3)
        done(self)


# ─────────────── B52 · Spack versus EasyBuild in four rows, then the weight: heavy, not the first option ───────────────
B52_ROWS = ("install", "dependencies", "output", "strength")
B52_ROW_Y = (1.85, 0.85, -0.15, -1.15)
B52_HEAD_Y = 2.7
B52_COL = (-1.6, 3.3)                       # column centres: Spack, EasyBuild
B52_GLYPH = (-3.05, 1.65)                   # glyph centres
B52_LAB = (-2.45, 2.4)                     # label left edges
B52_CELLS = (("a spec", "a recipe"), ("a graph", "a toolchain"), ("load or module", "a modulefile"), ("flexible", "strict"))
B52_CUES = (("a spec on the command line", "versus a named recipe"), ("Spack resolves a flexible", "EasyBuild follows a fixed"),
            ("spack load or a module", "versus always a module"), ("flexible variants", "versus strict"))
B52_RULE_Y = (2.3, 1.35, 0.35, -0.65, -1.65)
B52_WEIGHT = (-1.6, -2.55)


def b52_rule(y, sw=3):
    return Line([-6.0, y, 0], [6.0, y, 0], color=BAR1, stroke_width=sw)


def b52_terminal(cx, cy):
    """A spec on the command line: a tiny dark terminal chip with a ghost prompt line."""
    chip = RoundedRectangle(width=0.7, height=0.46, corner_radius=0.05, fill_color=DARK_TOP, fill_opacity=1,
                            stroke_color=INK, stroke_width=3).move_to([cx, cy, 0])
    prompt = Line([cx - 0.22, cy + 0.08, 0], [cx + 0.1, cy + 0.08, 0], color=GHOST, stroke_width=4)
    return VGroup(chip, prompt)


def b52_recipe(cx, cy):
    return pb8_page(cx, cy, w=0.5, h=0.6, outline=PB8_SMALL, sw=2)


def b52_graph(cx, cy):
    """A flexible graph: one node branching to three, deep-kraft links."""
    a = (cx - 0.35, cy)
    bs = ((cx + 0.32, cy + 0.28), (cx + 0.32, cy), (cx + 0.32, cy - 0.28))
    links = VGroup(*[Line([a[0] + 0.12, a[1], 0], [b[0] - 0.12, b[1], 0], color=PB8_LINK, stroke_width=3) for b in bs])
    return VGroup(links, pb8_dot(*a), *[pb8_dot(*b, r=0.08) for b in bs])


def b52_chain(cx, cy):
    """A fixed chain: three nodes in a straight line."""
    xs = (cx - 0.38, cx, cx + 0.38)
    links = VGroup(*[Line([xs[i] + 0.12, cy, 0], [xs[i + 1] - 0.12, cy, 0], color=PB8_LINK, stroke_width=3) for i in range(2)])
    return VGroup(links, *[pb8_dot(x, cy) for x in xs])


def b52_load_or_module(cx, cy):
    """Output: a grey pill (spack load) beside a tiny page (a module)."""
    return VGroup(pill(cx - 0.22, cy, 0.5, 0.3, GHOST), b52_recipe(cx + 0.25, cy))


def b52_flexible(cx, cy):
    """Strength: a flexible curve, grey."""
    c = VMobject(color=BAR1, stroke_width=6).set_points_smoothly(
        [[cx - 0.4, cy - 0.15, 0], [cx - 0.15, cy + 0.2, 0], [cx + 0.15, cy - 0.2, 0], [cx + 0.4, cy + 0.15, 0]])
    return VGroup(c)


def b52_strict(cx, cy):
    """Strength: a straight grey rule between two small square ends."""
    return VGroup(Line([cx - 0.3, cy, 0], [cx + 0.3, cy, 0], color=BAR1, stroke_width=6),
                  Square(side_length=0.16, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([cx - 0.38, cy, 0]),
                  Square(side_length=0.16, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([cx + 0.38, cy, 0]))


B52_GLYPHS = ((b52_terminal, b52_recipe), (b52_graph, b52_chain), (b52_load_or_module, b52_recipe), (b52_flexible, b52_strict))


def b52_cell(r, c):
    y = B52_ROW_Y[r]
    glyph = B52_GLYPHS[r][c](B52_GLYPH[c], y)
    return VGroup(glyph, pb8_left(T(B52_CELLS[r][c], 32), B52_LAB[c], y))


class B52_SpackVsEasyBuild(Scene):
    def construct(self):
        heads = VGroup(T("Spack", 36, bold=True).move_to([B52_COL[0], B52_HEAD_Y, 0]),
                       T("EasyBuild", 36, bold=True).move_to([B52_COL[1], B52_HEAD_Y, 0]))
        rules = VGroup(b52_rule(B52_RULE_Y[0], 5), *[b52_rule(y) for y in B52_RULE_Y[1:]])
        self.play(FadeIn(heads), run_time=0.3)
        self.play(Create(rules), run_time=0.45)                                             # the frame splits into four rows
        # four rows land in turn: the row label, then the Spack cell, then the EasyBuild cell
        for r in range(4):
            until(self, B52_CUES[r][0], lead=0.45)
            self.play(FadeIn(pb8_left(T(B52_ROWS[r], 32), -5.9, B52_ROW_Y[r]), shift=RIGHT * 0.15), run_time=0.25)
            self.play(FadeIn(b52_cell(r, 0), shift=UP * 0.1), run_time=0.3)
            until(self, B52_CUES[r][1], lead=0.1)
            self.play(FadeIn(b52_cell(r, 1), shift=UP * 0.1), run_time=0.3)
        # the candid note: the weight lands under the columns, 'heavy' beside it, the kraft pill
        until(self, "neither is the recommended", lead=0.3)
        pb8_drop(self, [pb8_weight(*B52_WEIGHT)], rt=0.45, dist=2.5)
        self.play(FadeIn(pb8_pill("not the first option", B52_COL[1], B52_WEIGHT[1], 3.7, fill=BOX_TOP), shift=DOWN * 0.15), run_time=0.35)
        until(self, "Both are heavy", lead=0.1)
        self.play(FadeIn(pb8_left(T("heavy", 32), B52_WEIGHT[0] + 0.75, B52_WEIGHT[1]), shift=LEFT * 0.1), run_time=0.3)
        # Spack in particular, when builds break: a grey cross by its name
        until(self, "Spack in particular", lead=0.2)
        self.play(Create(pb8_xmark(B52_COL[0] - 1.1, B52_HEAD_Y, 0.22)), run_time=0.3)
        # reach for them only when you need source-level control: one terracotta dot, the deliberate choice
        until(self, "Reach for them", lead=0.2)
        self.play(GrowFromCenter(Dot([0.85, B52_WEIGHT[1], 0], radius=0.1, color=TERRA)), run_time=0.3)
        done(self)


# ─────────────── B61 · the five-station source build: prefix, modules first, the cluster's libraries, make in a job ───────────────
B61_BELT_Y = -1.95
B61_ST_X = (-5.0, -2.5, 0.0, 2.5, 5.0)
B61_NAMES = (("load modules", T), ("configure", M), ("make", M), ("install", M), ("expose", T))
B61_NAME_CUES = ("load modules,", "configure with", "compile inside", "install into", "expose it on PATH")
B61_NUM_Y, B61_NAME_Y = -2.4, -2.95
B61_PILL_Y = (-1.45, -1.02, -0.59)
B61_JOB = Iso(-0.35, -1.9, 0.7)
B61_GEAR = (0.4, -0.5)
B61_PREFIX = Iso(2.0, -1.95, 0.6)           # the install prefix: an open folder
B61_LIB = Iso(3.85, 0.9, 0.7)               # the cluster's library block
B61_LIB_LABEL_Y = 2.5


def b61_job():
    return job_box(B61_JOB, 0, 0, 0, s=0.7)


def b61_prefix():
    return B61_PREFIX.open_box(0, 0, 0, 1.1, 1.1, 0.55)


def b61_installed():
    return Iso(B61_PREFIX.ox, B61_PREFIX.oy + 0.1, 0.6).box(0.3, 0.3, 0.02, 0.5, 0.5, 0.4, sw=3).set_z_index(1)


def b61_lib_block():
    return B61_LIB.mcp(0, 0, 0, 1.3, 1.3, 0.7)


def b61_lib_line():
    """The ghost link from the cluster's libraries to the make station, stopping short of both."""
    return Line([3.75, 0.85, 0], [0.95, -0.2, 0], color=GHOST, stroke_width=5)


def b61_link_1_2():
    """Modules loaded first: a deep-kraft link from the module pills to the configure page."""
    return Line([-4.25, -1.0, 0], [-3.0, -1.0, 0], color=PB8_LINK, stroke_width=4)


class B61_SourceBuildPipeline(Scene):
    def construct(self):
        self.add(pb8_belt(-6.0, 5.9, B61_BELT_Y))
        # always set a prefix; never the system's user local directory
        until(self, "Always set a prefix", lead=0.4)
        self.play(FadeIn(pb8_left(M("--prefix=$HOME/software/mytool", 32), -5.9, 1.65), shift=RIGHT * 0.2), run_time=0.3)
        until(self, "you cannot install", lead=0.1)
        usr = pb8_left(M("/usr/local", 32), -5.0, 2.5)
        self.play(FadeIn(usr), run_time=0.2)
        self.play(Create(pb8_xmark(-5.6, 2.5, 0.25)), run_time=0.25)
        # load the cluster's modules first: three pills slide onto station 1; then the configure page at station 2
        until(self, "Load the cluster", lead=0.2)
        pb8_slide(self, [pill(B61_ST_X[0], y, 1.3, 0.36, GHOST) for y in B61_PILL_Y], rt=0.6, lag=0.25, dist=2.0)
        until(self, "before you configure", lead=0.2)
        pb8_drop(self, [pb8_page(B61_ST_X[1], -1.1, w=0.8, h=1.0)], rt=0.4, dist=1.8)
        until(self, "so the build links", lead=0.1)
        self.play(Create(b61_link_1_2()), run_time=0.3)
        until(self, "fast binaries", lead=0.2)
        self.play(GrowFromCenter(Dot([B61_ST_X[1], -0.4, 0], radius=0.09, color=TERRA)), run_time=0.25)
        # the cluster's MPI, BLAS and LAPACK: a dark library block, linked to the make station
        until(self, "cluster's M P I", lead=0.3)
        pb8_drop(self, [b61_lib_block()], rt=0.45, dist=2.5, with_=[FadeIn(T("MPI · BLAS · LAPACK", 32).move_to([4.1, B61_LIB_LABEL_Y, 0]))])
        until(self, "not a slow", lead=0.2)
        self.play(Create(b61_lib_line()), run_time=0.35)
        # run make inside a job: the job box lands at station 3 and its gear turns
        until(self, "run the make step", lead=0.2)
        pb8_drop(self, [b61_job()], rt=0.45, dist=2.5)
        until(self, "dash j eight", lead=0.1)
        gear = pb8_gear(*B61_GEAR, r=0.38)
        self.play(GrowFromCenter(gear), run_time=0.25)
        self.play(Rotate(gear, angle=PI / 2), run_time=0.6)
        # five steps: the numerals, then each station's name as it is spoken
        until(self, "Five steps", lead=0.2)
        self.play(LaggedStart(*[FadeIn(T(str(k + 1), 32).move_to([x, B61_NUM_Y, 0]), shift=UP * 0.1) for k, x in enumerate(B61_ST_X)],
                              lag_ratio=0.15), run_time=0.5)
        for k, (cue, (name, fn)) in enumerate(zip(B61_NAME_CUES, B61_NAMES)):
            until(self, cue, lead=0.1)
            extra = []
            if k == 3:
                back, front = b61_prefix()
                self.add(back, front)
                pb8_drop(self, [b61_installed()], rt=0.35, dist=2.0, with_=[FadeIn(fn(name, 32).move_to([B61_ST_X[k], B61_NAME_Y, 0]))])
                continue
            if k == 4:
                extra = [FadeIn(VGroup(pill(B61_ST_X[4], -1.3, 1.3, 0.5, GHOST), M("PATH", 32).move_to([B61_ST_X[4], -1.3, 0])))]
            self.play(FadeIn(fn(name, 32).move_to([B61_ST_X[k], B61_NAME_Y, 0]), shift=UP * 0.1), *extra, run_time=0.3)
        until(self, "or with a module", lead=0.1)
        pb8_drop(self, [pb8_page(B61_ST_X[4], -0.4, w=0.7, h=0.85)], rt=0.35, dist=2.0)
        done(self)
