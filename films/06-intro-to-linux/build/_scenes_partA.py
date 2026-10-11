# ═════════════════════════════ PART A · B10 (Act I opener), B20 (Act II opener), B32 ═════════════════════════════
# Stage map. B10: the Linux kernel (dark block) centre, Unix (kraft box) above, three devices around it on
# deep-kraft lines. B20: a directory tree of small kraft boxes down the left, the colour swatches and the two
# mono paths on the right. B32: a file page left, a directory (kraft box with pages on top) right, both removed.
# The same directory box (kraft box, pages on top) is the picture of a directory in B20 and B32.
PA_KRAFT = "#9C8462"                        # deep-kraft connector (drawing law: connectors are never ink)


def pa_title(s):
    """Act title, top-left, for the whole beat."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_left(t, x, y):
    """Place a label by its left edge (labels sit beside objects)."""
    return t.move_to([x + t.width / 2, y, 0])


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


def pa_link(a, b, sw=5):
    """A deep-kraft connector between two screen points (both stop short of what they join)."""
    return Line([a[0], a[1], 0], [b[0], b[1], 0], color=PA_KRAFT, stroke_width=sw)


def pa_dirbox(iso, pages=0):
    """A directory: a small kraft box, optionally with file pages lying on its top (grey page outlines:
    an ink-outlined card inside an ink-outlined box reads as overlapping text under GATE T)."""
    g = VGroup(iso.box(0, 0, 0, 0.9, 0.9, 0.6, sw=3))
    for k in range(pages):
        pg = iso.page(0.08 + 0.06 * k, 0.08 + 0.04 * k, 0.6 + 0.07 * k, 0.7, 0.72)
        pg[0].set_stroke(DIM)
        g.add(pg)
    return g


def pa_token(x, y, s=1.0):
    """A person token standing with its feet at (x, y)."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head).set_z_index(7)


# ─────────────── B10 · the Linux family: kernel, 1991, Unix → Linux / macOS, phone · laptop · cluster ───────────────
B10_K = Iso(0.3, -0.75, 0.75)               # the kernel block, centre
B10_U = Iso(0.3, 1.75, 0.55)                # the Unix box, above
B10_PHONE = Iso(-4.4, -0.2, 0.75)
B10_LAPTOP = Iso(-4.6, -2.75, 0.8)
B10_RACK = Iso(3.9, -2.0, 0.8)


def b10_kernel():
    return B10_K.box(0, 0, 0, 1.3, 1.3, 0.7, DARK_TOP, DARK_L, DARK_R)


def b10_unix():
    return B10_U.box(0, 0, 0, 1.2, 1.2, 0.5)


def b10_phone(iso=B10_PHONE):
    """A phone: a dark slab standing on end, one ghost screen on its front."""
    body = iso.box(0, 0, 0, 0.6, 0.14, 1.15, DARK_TOP, DARK_L, DARK_R)
    screen = iso.quad([(0.07, 0, 0.14), (0.53, 0, 0.14), (0.53, 0, 1.02), (0.07, 0, 1.02)], GHOST, sw=0).set_z_index(1)
    return VGroup(body, screen)


def b10_laptop(iso=B10_LAPTOP):
    """A small laptop: kraft base, dark screen standing on the back edge (same as film 3)."""
    base = iso.box(0, 0, 0, 1.2, 0.9, 0.08)
    screen = iso.quad([(0, 0.9, 0.08), (1.2, 0.9, 0.08), (1.2, 0.9, 0.85), (0, 0.9, 0.85)], DARK_TOP)
    return VGroup(base, screen)


def b10_tag(text, x, y, w):
    """A tag: a white pill with an ink label (no outline, so the label is not inside an outline)."""
    return VGroup(pill(x, y, w, 0.66), T(text, 38).move_to([x, y, 0]))


class B10_LinuxFamily(Scene):
    def construct(self):
        self.add(pa_title("I · What Linux Is"))
        pa_slide_in(self, b10_kernel(), UP * 5.5, 0.6)                      # the kernel rises into the centre
        self.add(pa_left(T("Linux", 44), 1.45, 0.45))
        until(self, "in 1991", lead=0.6)
        rule = Line([-0.6, -1.35, 0], [2.1, -1.35, 0], color=BAR1, stroke_width=4)
        self.play(GrowFromEdge(rule, LEFT), run_time=0.4)
        tick = Dot([0.3, -1.35, 0], radius=0.11, color=TERRA)
        self.play(GrowFromCenter(tick), FadeIn(T("1991", 40).move_to([1.15, -1.85, 0]), shift=UP * 0.15), run_time=0.35)
        until(self, "in the tradition of Unix", lead=0.4)
        pa_drop(self, [b10_unix()], 0.5)
        self.add(T("Unix", 44).move_to([-1.3, 2.2, 0]))
        until(self, "the much older system")
        self.play(Create(pa_link((0.3, 1.6), (0.3, 0.95))), run_time=0.35)           # Unix → Linux
        until(self, "also shaped macOS", lead=0.3)
        self.play(Create(pa_link((0.75, 1.65), (2.45, 1.05))), run_time=0.4)          # Unix → macOS
        self.add(pa_left(T("macOS", 44), 2.75, 0.9))
        until(self, "It runs on Android phones", lead=0.1)
        pa_slide_in(self, b10_phone(), RIGHT * 5, 0.5)
        self.play(Create(pa_link((-0.8, 0.0), (-3.8, 0.3))), run_time=0.3)
        self.add(T("phone", 40).move_to([-4.25, -0.72, 0]))
        until(self, "on laptops", lead=0.1)
        pa_slide_in(self, b10_laptop(), RIGHT * 5, 0.5)
        self.play(Create(pa_link((-0.85, -0.55), (-3.45, -1.75))), run_time=0.3)
        self.add(T("laptop", 40).move_to([-2.7, -2.4, 0]))
        until(self, "and on nearly every HPC cluster", lead=0.1)
        st, li = explorer_rack(B10_RACK)
        pa_slide_in(self, VGroup(st, li), LEFT * 5, 0.5)
        self.play(Create(pa_link((1.3, -0.5), (2.7, -0.95))), run_time=0.3)
        self.add(T("cluster", 40).move_to([3.9, -2.55, 0]))
        until(self, "It's free and open source", lead=0.2)
        self.play(GrowFromCenter(b10_tag("free · open source", 0.6, -2.75, 4.2)), run_time=0.4)
        until(self, "so anyone can contribute", lead=0.1)
        dots = VGroup(*[Dot([x, -2.35, 0], radius=0.1, color=TERRA) for x in (-0.5, 0.6, 1.7)]).set_z_index(5)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2), run_time=0.3)
        self.play(*[d.animate.move_to([0.3 + 0.35 * (k - 1), -0.95, 0]) for k, d in enumerate(dots)], run_time=0.7)   # contributions flow in
        self.play(FadeOut(dots, scale=0.3), run_time=0.25)
        until(self, "and it's considered secure and robust", lead=0.1)
        self.play(GrowFromCenter(b10_tag("secure · robust", 4.2, 2.4, 3.6)), run_time=0.4)
        until(self, "which is why servers")
        self.play(LaggedStart(*[l.animate.set_color(TERRA) for l in li], lag_ratio=0.3), run_time=0.5)   # the cluster runs it
        done(self)


# ─────────────── B20 · the tree, four colours, an absolute path from /, a relative path from where you stand ───────────────
B20_S = 0.5
B20_ROOT, B20_HOME, B20_USER = Iso(-4.4, 1.75, B20_S), Iso(-4.4, 0.35, B20_S), Iso(-4.4, -1.05, B20_S)
B20_DIR, B20_HERE = Iso(-5.4, -2.5, B20_S), Iso(-2.7, -2.5, B20_S)
B20_LBL_X = -3.7                                                      # left edge of the tree labels
B20_SW_X, B20_SW_LBL = 1.3, 1.9                                       # swatch centre, label left edge
B20_ROWS = ((BAR1, "directory", 2.4), ("#8A9A7B", "executable", 1.7), ("#B06A4A", "compressed", 1.0), (INK, "file", 0.3))
B20_PATH_X = 0.9                                                      # left edge of the two mono paths


def b20_links():
    return VGroup(pa_link((-4.4, 1.65), (-4.4, 1.2)), pa_link((-4.4, 0.25), (-4.4, -0.2)),
                  pa_link((-4.75, -1.15), (-5.15, -1.55)), pa_link((-4.05, -1.15), (-3.1, -1.6)))


def b20_labels():
    return VGroup(pa_left(M("/", 40), B20_LBL_X, 2.1), pa_left(M("home", 40), B20_LBL_X, 0.7),
                  pa_left(M("user", 40), B20_LBL_X, -0.7), M("dir", 40).move_to([-4.2, -2.15, 0]))


def b20_swatch(k):
    fill, word, y = B20_ROWS[k]
    sq = Square(side_length=0.5, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([B20_SW_X, y, 0])
    return VGroup(sq, pa_left(T(word, 40), B20_SW_LBL, y))


def b20_path(points):
    p = VMobject()
    p.set_points_as_corners([np.array([x, y, 0.0]) for x, y in points])
    return p


class B20_PathsAndColours(Scene):
    def construct(self):
        self.add(pa_title("II · Finding Your Way"))
        root, home, user = pa_dirbox(B20_ROOT), pa_dirbox(B20_HOME), pa_dirbox(B20_USER)
        pa_drop(self, [root, home, user], 0.8, 0.3)                                   # the tree draws, top down
        links, labels = b20_links(), b20_labels()
        self.play(Create(links[0]), Create(links[1]), run_time=0.35)
        self.add(labels[0], labels[1], labels[2])
        here = pa_dirbox(B20_HERE)
        dirbox = pa_dirbox(B20_DIR)
        pa_drop(self, [dirbox, here], 0.5, 0.3)
        self.play(Create(links[2]), Create(links[3]), run_time=0.3)
        self.add(labels[3])
        until(self, "as on Windows or a Mac", lead=0.3)
        files = pa_dirbox(B20_DIR, pages=2)
        pa_drop(self, [files[1], files[2]], 0.5, 0.3, dist=3.0)                      # files land in dir
        until(self, "blue for directories", lead=0.3)
        self.play(FadeIn(b20_swatch(0), shift=LEFT * 0.3), run_time=0.35)
        until(self, "green for executables", lead=0.3)
        self.play(FadeIn(b20_swatch(1), shift=LEFT * 0.3), run_time=0.35)
        until(self, "red for compressed", lead=0.3)
        self.play(FadeIn(b20_swatch(2), shift=LEFT * 0.3), run_time=0.35)
        until(self, "plain for ordinary files", lead=0.3)
        self.play(FadeIn(b20_swatch(3), shift=LEFT * 0.3), run_time=0.35)
        until(self, "A path is", lead=0.1)
        self.play(FadeIn(pa_left(M("/home/user/dir", 40), B20_PATH_X, -1.0), shift=UP * 0.2), run_time=0.4)
        until(self, "Absolute: from the root", lead=0.2)
        dot = Dot([-4.4, 2.1, 0], radius=0.12, color=TERRA).set_z_index(9)
        self.play(GrowFromCenter(dot), run_time=0.25)
        self.play(MoveAlongPath(dot, b20_path([(-4.4, 2.1), (-4.4, 0.7), (-4.4, -0.7), (-5.4, -2.0)])), run_time=1.3)   # / → home → user → dir
        until(self, "Relative: from where you stand", lead=0.2)
        self.play(FadeIn(pa_token(-2.7, -1.98, 0.7), shift=DOWN * 0.5), run_time=0.4)        # you stand here
        self.play(FadeIn(pa_left(M("../dir", 40), B20_PATH_X, -2.1), shift=UP * 0.2), run_time=0.35)
        dot2 = Dot([-2.7, -2.15, 0], radius=0.12, color=TERRA).set_z_index(9)
        self.play(GrowFromCenter(dot2), run_time=0.2)
        self.play(MoveAlongPath(dot2, b20_path([(-2.7, -2.15), (-4.4, -0.7), (-5.4, -2.0)])), run_time=0.9)   # up one, over into dir
        until(self, "One dot is here", lead=0.2)
        self.play(FadeIn(pa_left(M(". here", 40), -2.0, -2.15), shift=LEFT * 0.2), run_time=0.35)
        until(self, "Two dots is one level up", lead=0.2)
        self.play(FadeIn(pa_left(M(".. up", 40), -1.7, -0.7), shift=LEFT * 0.2), run_time=0.35)
        done(self)


# ─────────────── B32 · rm removes the file, rm -r the directory; no trash can, no undo ───────────────
B32_PAGE = Iso(-3.3, -1.0, 1.3)
B32_DIR = Iso(2.3, -1.6, 1.5)
B32_RACK = Iso(4.6, -2.75, 0.8)


def b32_page():
    return B32_PAGE.page(0, 0, 0, 1.4, 1.7)


def b32_bin():
    """Where a trash can would be: a dashed grey outline of one, and nothing in it."""
    body = DashedVMobject(Polygon([-1.0, -2.9, 0], [0.4, -2.9, 0], [0.55, -1.3, 0], [-1.15, -1.3, 0],
                                  stroke_color=BAR1, stroke_width=5, fill_opacity=0), num_dashes=22)
    lid = DashedVMobject(Line([-1.35, -1.1, 0], [0.75, -1.1, 0], stroke_color=BAR1, stroke_width=5), num_dashes=7)
    return VGroup(body, lid)


class B32_RemoveIsForever(Scene):
    def construct(self):
        self.add(pa_title("III · Making And Moving Files"))
        page, folder = b32_page(), pa_dirbox(B32_DIR, pages=2)
        self.add(page, folder)
        cmd1 = M("rm new_name", 44).move_to([-3.3, 2.0, 0])
        self.play(FadeIn(cmd1, shift=DOWN * 0.3), run_time=0.35)                     # the command lands
        until(self, "removes a file", lead=0.0)
        self.play(FadeOut(page, scale=0.6), run_time=0.5)                             # and the file is gone
        until(self, "dash r removes a directory", lead=0.2)
        cmd2 = M("rm -r new_dir_copy", 44).move_to([2.3, 1.3, 0])
        self.play(FadeIn(cmd2, shift=DOWN * 0.3), run_time=0.35)
        until(self, "and everything in it", lead=0.3)
        self.play(FadeOut(folder[2], scale=0.6), FadeOut(folder[1], scale=0.6), run_time=0.35)   # its contents first
        self.play(FadeOut(folder[0], scale=0.6), run_time=0.4)                                    # then the directory
        until(self, "There is no trash can", lead=0.1)
        self.play(Create(b32_bin()), run_time=0.7)                                    # the outline where a trash can would be
        until(self, "and no undo", lead=0.1)
        self.play(FadeIn(T("no undo", 44).move_to([1.9, -2.1, 0]), shift=LEFT * 0.2), run_time=0.35)
        until(self, "On a cluster", lead=0.1)
        st, li = explorer_rack(B32_RACK)
        pa_slide_in(self, VGroup(st, li), LEFT * 4, 0.5)
        until(self, "so read the command twice", lead=0.1)
        self.play(Indicate(cmd1, color=None, scale_factor=1.12), run_time=0.45)      # read it ...
        self.play(Indicate(cmd2, color=None, scale_factor=1.12), run_time=0.45)      # ... twice
        until(self, "before you press return", lead=0.1)
        self.play(LaggedStart(*[l.animate.set_color(TERRA) for l in li], lag_ratio=0.3), run_time=0.4)
        done(self)
