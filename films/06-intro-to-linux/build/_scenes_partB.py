# ═════════════════════════════ PART B · B50 B51 (Act V) · B71 (Act VII) ═════════════════════════════
# Everything in _kit.py is in scope (the final scenes.py is the kit + the part files concatenated).
# Helpers and constants are prefixed PB_ / pb_ / b50_ / b51_ / b71_ so the parts never collide.
# Laws kept here: brackets and grid rules in BAR1 grey (never an ink line under ink text); terracotta only as
# dots; numerals and labels in ink, beside objects; small objects outlined in dark kraft; every number and name
# on screen is in the beat's narration or visual_intent (B51's line is copied exactly).
PB_SMALL = "#917A55"      # dark kraft: outlines of SMALL objects only (tokens, the directory icon)
PB_BELT = "#E4E0D4"       # belts stay within 28 of the stage (Gate V)
PB_ADV32 = 0.249          # Menlo advance per character at size 32 (measured; Gate A's stub measures text differently, so fixed)


def pb_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pb_base(mob, s, size, x, y, mono=False):
    """Set a text on a BASELINE at y (centre x), so neighbouring words with and without descenders line up.
    Descender depth is proportional to the size (measured: Menlo 0.098 at 32, EB Garamond 0.134 at 32)."""
    desc = (0.00306 if mono else 0.0042) * size if any(c in "gjpqy" for c in s) else 0.0
    return mob.move_to([x, y - desc + mob.height / 2.0, 0])


def pb_M(s, size, x, y_base):
    return pb_base(M(s, size), s, size, x, y_base, mono=True)


def pb_T(s, size, x, y_base):
    return pb_base(T(s, size), s, size, x, y_base)


def pb_figure(x, y, s=1.0, sw=3):
    """A person token standing at (x, y): film 1's B20 token (trapezoid body, round head), flat on the stage."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2 * s, 0, 0]), b + np.array([0.2 * s, 0, 0]), b + np.array([0.1 * s, 0.5 * s, 0]),
                   b + np.array([-0.1 * s, 0.5 * s, 0]), fill_color=BAR1, fill_opacity=1, stroke_color=PB_SMALL, stroke_width=sw)
    head = Circle(radius=0.18 * s, fill_color=BAR1, fill_opacity=1, stroke_color=PB_SMALL, stroke_width=sw).move_to(b + np.array([0, 0.66 * s, 0]))
    return VGroup(body, head)


def pb_drop(self, mobs, rt=0.5, lag=0.2, dist=3.0):
    """Land objects from above, fully opaque (GATE T: never a half-faded object)."""
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), run_time=rt, rate_func=ease_in)


def pb_bracket(x0, x1, y, tick=0.13):
    """A grey bracket under a run of text: a bar at y with ticks pointing up toward the text."""
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=BAR1, stroke_width=4),
                  Line([x0, y, 0], [x0, y + tick, 0], color=BAR1, stroke_width=4),
                  Line([x1, y, 0], [x1, y + tick, 0], color=BAR1, stroke_width=4))


# ─────────────── B50 · three audiences × three permissions ───────────────
B50_CX = (-1.0, 1.4, 3.8)                   # column centres: user · group · others
B50_RY = (0.55, -0.55, -1.65)               # row centres: read · write · execute
B50_GX = (-2.2, 0.2, 2.6, 5.0)              # grid rules (vertical)
B50_GY = (1.1, 0.0, -1.1, -2.2)             # grid rules (horizontal)
B50_TOK_Y = 1.75                            # feet of the audience tokens
B50_WORD_Y = 1.42                           # the audience words, under their tokens
B50_LABEL_R = -2.6                          # row words end here (beside the grid)
B50_NUM_X = -4.45                           # the numerals, beside the row words
B50_DIR = np.array([-5.45, -1.65, 0.0])     # the directory icon, beside 'execute'


def b50_grid():
    return VGroup(*[Line([x, B50_GY[0], 0], [x, B50_GY[-1], 0], color=BAR1, stroke_width=4) for x in B50_GX],
                  *[Line([B50_GX[0], y, 0], [B50_GX[-1], y, 0], color=BAR1, stroke_width=4) for y in B50_GY])


def b50_audience(k):
    """Column k's token(s): one figure, three figures, a crowd of five."""
    x = B50_CX[k]
    if k == 0:
        return VGroup(pb_figure(x, B50_TOK_Y, 0.95))
    if k == 1:
        return VGroup(*[pb_figure(x + d, B50_TOK_Y + 0.08, 0.72) for d in (-0.6, 0.0, 0.6)])
    return VGroup(*[pb_figure(x + d, B50_TOK_Y + 0.18, 0.52) for d in (-0.88, -0.44, 0.0, 0.44, 0.88)])


def b50_word(s, k):
    return pb_T(s, 34, B50_CX[k], B50_WORD_Y - 0.1)


def b50_row_word(s, r):
    t = T(s, 36)
    return pb_base(t, s, 36, B50_LABEL_R - t.width / 2, B50_RY[r] - 0.12)


def b50_dots(r):
    return VGroup(*[Dot([x, B50_RY[r], 0], radius=0.17, color=TERRA) for x in B50_CX])


def b50_numeral(s, r):
    return T(s, 48, bold=True).move_to([B50_NUM_X, B50_RY[r], 0])


def b50_directory():
    """A small directory: kraft folder with a tab, dark-kraft outline. Returns (folder, door); the door swings open."""
    c = B50_DIR
    body = RoundedRectangle(width=0.95, height=0.68, corner_radius=0.06, fill_color=BOX_TOP, fill_opacity=1,
                            stroke_color=PB_SMALL, stroke_width=3).move_to(c)
    tab = Rectangle(width=0.36, height=0.14, fill_color=BOX_TOP, fill_opacity=1, stroke_color=PB_SMALL,
                    stroke_width=3).move_to(c + np.array([-0.29, 0.40, 0]))
    door = Rectangle(width=0.24, height=0.4, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to(c + np.array([0.0, -0.12, 0]))
    return VGroup(body, tab), door


class B50_ThreeByThree(Scene):
    def construct(self):
        self.add(pb_title("V · Who May Do What"))
        self.play(Create(b50_grid()), run_time=0.7)
        until(self, "the user who owns it")
        pb_drop(self, [b50_audience(0), b50_word("user", 0)], 0.45, 0.1)
        until(self, "the group that owns it")
        pb_drop(self, [b50_audience(1), b50_word("group", 1)], 0.45, 0.1)
        until(self, "and others")
        pb_drop(self, [b50_audience(2), b50_word("others", 2)], 0.45, 0.1)
        until(self, "read, write, and")
        self.play(FadeIn(b50_row_word("read", 0)), LaggedStart(*[GrowFromCenter(d) for d in b50_dots(0)], lag_ratio=0.3), run_time=0.45)
        until(self, "write, and execute")
        self.play(FadeIn(b50_row_word("write", 1)), LaggedStart(*[GrowFromCenter(d) for d in b50_dots(1)], lag_ratio=0.3), run_time=0.45)
        until(self, "execute, which")
        self.play(FadeIn(b50_row_word("execute", 2)), LaggedStart(*[GrowFromCenter(d) for d in b50_dots(2)], lag_ratio=0.3), run_time=0.45)
        until(self, "for a directory")
        folder, door = b50_directory()
        self.play(FadeIn(folder, shift=UP * 0.3), run_time=0.35)
        self.add(door)
        until(self, "means entering it")
        hinge = door.get_left()
        self.play(Rotate(door, angle=-PI / 4, about_point=np.array(hinge)), run_time=0.5)
        until(self, "read four")
        self.play(FadeIn(b50_numeral("4", 0), shift=RIGHT * 0.25), run_time=0.3)
        until(self, "write two")
        self.play(FadeIn(b50_numeral("2", 1), shift=RIGHT * 0.25), run_time=0.3)
        until(self, "execute one")
        self.play(FadeIn(b50_numeral("1", 2), shift=RIGHT * 0.25), run_time=0.3)
        done(self)


# ─────────────── B51 · the long-listing line, decoded ───────────────
# The line is `-rwxrw-r-- 1 user group 46 Feb 14 16:37 File.txt` (49 characters), one row at size 32 (11.95 units,
# the largest size that fits ±6.2). Each token is its own mono Text placed by character index × advance, so no
# token holds a space (Pango collapses some single spaces on this Mac).
B51_Y = 2.5                                  # the line
B51_X0 = -5.83                               # left edge of character 0 (line centred at x = +0.15)
B51_TOKENS = (("-", 0), ("rwx", 1), ("rw-", 4), ("r--", 7), ("1", 11), ("user", 13), ("group", 18), ("46", 24),
              ("Feb", 27), ("14", 31), ("16:37", 34), ("File.txt", 40))
B51_BR_Y = 2.05                              # brackets under the line (ticks rise to 2.18; glyph bottoms sit at 2.28)
B51_HI_Y, B51_LO_Y = 1.68, 1.24              # two label rows, so neighbouring labels never touch
B51_BAND_X = (-3.6, 0.0, 3.6)                # the lifted triads
B51_BAND_Y = 0.3
B51_BAND_BR_Y = -0.3
B51_BAND_LABEL_Y = -0.72
B51_READ_Y = -1.5


def b51_x(start, n):
    """Centre x of the run of n characters starting at character index `start`."""
    return B51_X0 + PB_ADV32 * (start + n / 2.0)


def b51_token(s, start, size=32):
    return pb_M(s, size, b51_x(start, len(s)), B51_Y - 0.17)


def b51_line():
    """The twelve tokens of the line, in order. Index 0 is the type character; 1–3 the three triads."""
    return [b51_token(s, i) for s, i in B51_TOKENS]


def b51_under(start, n):
    """A grey bracket under the run of n characters at `start` (0.03 in from each end)."""
    x0 = B51_X0 + PB_ADV32 * start + 0.03
    return pb_bracket(x0, x0 + PB_ADV32 * n - 0.06, B51_BR_Y)


def b51_label(s, start, n, hi=True):
    return pb_T(s, 32, b51_x(start, n), (B51_HI_Y if hi else B51_LO_Y) - 0.1)


def b51_band_bracket(k):
    x = B51_BAND_X[k]
    return pb_bracket(x - 0.52, x + 0.52, B51_BAND_BR_Y)


def b51_band_label(s, k):
    return pb_T(s, 34, B51_BAND_X[k], B51_BAND_LABEL_Y - 0.1)


def b51_reading(s, k):
    return pb_T(s, 36, B51_BAND_X[k], B51_READ_Y - 0.1)


class B51_DecodeTheLine(Scene):
    def construct(self):
        toks = b51_line()
        line = VGroup(*toks)
        line.shift(UP * 0.5)
        self.play(line.animate.shift(DOWN * 0.5), run_time=0.6)
        until(self, "The first character")
        self.play(Create(b51_under(0, 1)), FadeIn(b51_label("type", 0, 1)), run_time=0.4)
        # the type character tries its three values: - for a file, d for a directory, l for a link
        type_tok = toks[0]
        until(self, "d for a directory")
        d_tok = b51_token("d", 0)
        self.play(FadeOut(type_tok), FadeIn(d_tok), run_time=0.25)
        until(self, "l for a link")
        l_tok = b51_token("l", 0)
        self.play(FadeOut(d_tok), FadeIn(l_tok), run_time=0.25)
        until(self, "Then nine characters")
        dash_tok = b51_token("-", 0)
        self.play(FadeOut(l_tok), FadeIn(dash_tok), run_time=0.25)
        self.play(*[Create(b51_under(s, 3)) for s in (1, 4, 7)], run_time=0.4)
        until(self, "three groups of three")
        triads = toks[1:4]
        self.play(*[t.animate.scale(1.5).move_to([B51_BAND_X[k], B51_BAND_Y, 0]) for k, t in enumerate(triads)], run_time=0.8)
        until(self, "the owner's permissions")
        self.play(Create(b51_band_bracket(0)), FadeIn(b51_band_label("owner", 0)), run_time=0.35)
        until(self, "the group's")
        self.play(Create(b51_band_bracket(1)), FadeIn(b51_band_label("group", 1)), run_time=0.35)
        until(self, "everyone else's")
        self.play(Create(b51_band_bracket(2)), FadeIn(b51_band_label("others", 2)), run_time=0.35)
        until(self, "the owner can read")
        self.play(FadeIn(b51_reading("read write execute", 0), shift=UP * 0.2), run_time=0.4)
        until(self, "the group can read")
        self.play(FadeIn(b51_reading("read write", 1), shift=UP * 0.2), run_time=0.4)
        until(self, "others can only read")
        self.play(FadeIn(b51_reading("read", 2), shift=UP * 0.2), run_time=0.4)
        until(self, "the link count")
        self.play(Create(b51_under(11, 1)), FadeIn(b51_label("links", 11, 1)), run_time=0.3)
        until(self, "the owner, the group")
        self.play(Create(b51_under(13, 4)), FadeIn(b51_label("owner", 13, 4, hi=False)), run_time=0.3)
        until(self, "the group, the size")
        self.play(Create(b51_under(18, 5)), FadeIn(b51_label("group", 18, 5)), run_time=0.3)
        until(self, "the size in bytes")
        self.play(Create(b51_under(24, 2)), FadeIn(b51_label("size", 24, 2, hi=False)), run_time=0.3)
        until(self, "the modification time")
        self.play(Create(b51_under(27, 12)), FadeIn(b51_label("time", 27, 12)), run_time=0.3)
        until(self, "and the name")
        self.play(Create(b51_under(40, 8)), FadeIn(b51_label("name", 40, 8, hi=False)), run_time=0.3)
        done(self)


# ─────────────── B71 · the toolbelt: ten commands, one address ───────────────
B71_CMDS = ("pwd", "ls", "cd", "touch", "mkdir", "cp", "mv", "rm", "less", "chmod")
B71_CUES = ("Prompt", "path", "list", "move", "make", "copy", "copy", "remove", "read", "permissions")
B71_PAD, B71_GAP = 0.17, 0.08                # pill padding each side of the mono text, gap between pills (ten pills span 12.1)
B71_BELT_Y = -0.5                            # the belt's front edge; its top face runs -0.5 … -0.2
B71_CHIP_Y = -0.02                           # pills sit on the belt's top face
B71_TAG_Y = 0.98                             # the 'no undo' tag above the rm chip
B71_MAIL_Y = -1.75                           # the address, beneath the belt
B71_HOURS_Y = -2.6                           # 'office hours on Zoom', beneath the address


def b71_widths():
    return [len(c) * PB_ADV32 + 2 * B71_PAD for c in B71_CMDS]


def b71_centres():
    """Pill centres, the whole row centred on x = 0 (fixed arithmetic, not measured text)."""
    ws = b71_widths()
    total = sum(ws) + B71_GAP * (len(ws) - 1)
    xs, x = [], -total / 2.0
    for w in ws:
        xs.append(x + w / 2.0)
        x += w + B71_GAP
    return xs


def b71_belt(x0=-6.1, x1=5.8, y=B71_BELT_Y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes (edges dark kraft, never ink). Film 1's B13 belt."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PB_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PB_BELT, fill_opacity=1, stroke_color=PB_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def b71_chip(k):
    """A pale pill (CARD fill, grey outline) carrying one mono command in ink."""
    x, w = b71_centres()[k], b71_widths()[k]
    body = RoundedRectangle(width=w, height=0.62, corner_radius=0.31, fill_color=CARD, fill_opacity=1,
                            stroke_color=BAR1, stroke_width=2.5).move_to([x, B71_CHIP_Y, 0])
    return VGroup(body, pb_M(B71_CMDS[k], 32, x, B71_CHIP_Y - 0.12))


def b71_tag():
    """The dashed 'no undo' tag above the rm chip: grey dashed frame, ink words."""
    x = b71_centres()[7]
    w, h = 1.9, 0.56
    pts = [np.array([x - w / 2, B71_TAG_Y - h / 2, 0]), np.array([x + w / 2, B71_TAG_Y - h / 2, 0]),
           np.array([x + w / 2, B71_TAG_Y + h / 2, 0]), np.array([x - w / 2, B71_TAG_Y + h / 2, 0])]
    frame = VGroup(*[DashedLine(pts[i], pts[(i + 1) % 4], color=BAR1, stroke_width=3, dash_length=0.12) for i in range(4)])
    return VGroup(frame, T("no undo", 32).move_to([x, B71_TAG_Y, 0]))


class B71_TheToolbelt(Scene):
    def construct(self):
        self.add(pb_title("VII · Quick Tips"))
        self.play(GrowFromEdge(b71_belt(), LEFT), run_time=0.6)
        for k, cue in enumerate(B71_CUES):
            until(self, cue, lead=0.3)
            pb_drop(self, [b71_chip(k)], 0.3, dist=2.6)
            if k == 7:
                until(self, "with care", lead=0.0)
                self.play(FadeIn(b71_tag(), shift=DOWN * 0.2), run_time=0.35)
        until(self, "r c help")
        mail = pb_M("rchelp@northeastern.edu", 40, 0.0, B71_MAIL_Y)
        pb_drop(self, [mail], 0.45, dist=1.2)
        until(self, "office hours")
        self.play(FadeIn(pb_T("office hours on Zoom", 34, 0.0, B71_HOURS_Y), shift=UP * 0.2), run_time=0.4)
        done(self)
