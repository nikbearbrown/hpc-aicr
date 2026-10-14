
# ═════════════════════════════ Requesting Access to Explorer · the film's Manim scenes ═════════════════════════════
# Cast (one cast, whole film; the same object is the same picture in every beat):
#   YOU       a Professor Bear portrait, seed "req-you"         (PROFESSOR BEAR LAW: a person is never an icon)
#   SPONSOR   a Professor Bear portrait, seed "req-sponsor"
#   DELEGATE  a Professor Bear portrait, seed "req-delegate"
#   STORAGE   the tall white cabinet from the AICR cast (project directory), labelled /projects
#   GATE      a kraft panel between two ink posts; it slides open when access is granted
#   COMMAND   a small kraft box with one terracotta tape (the job box from the AICR cast)
#   FORM      a white page (iso page) with ghost lines and one terracotta dot
# Narration phrases used with until() must appear verbatim in beat_sheet.json; make_sheet.py checks them.

PB_W = 1.5     # portrait height for the standing cast


def person(seed, label, x, y, h=PB_W, size=40):
    """A portrait with a one-to-three-word label under it. Returns Group(portrait, label)."""
    pb = professor_bear("1x1", h, seed=seed, x=x, y=y)
    lab = T(label, size).next_to(pb, DOWN, buff=0.14)
    return Group(pb, lab)


def you_at(x, y, h=PB_W):
    return person("req-you", "You", x, y, h)


def sponsor_at(x, y, h=PB_W, label="Sponsor"):
    return person("req-sponsor", label, x, y, h)


def delegate_at(x, y, h=PB_W):
    return person("req-delegate", "Delegate", x, y, h)


def chip(text, x, y, w=None, size=38, fill="#FFFFFF", color=INK, mono=False, stroke=BAR1):   # grey outline: an INK outline reads to Gate T as a text run
    t = (M(text, size) if mono else T(text, size, color)).move_to([x, y, 0])
    w = w or (t.width + 0.6)
    box = RoundedRectangle(width=w, height=t.height + 0.42, corner_radius=0.2, fill_color=fill, fill_opacity=1,
                           stroke_color=stroke, stroke_width=4).move_to([x, y, 0])
    return VGroup(box, t)


def gate_panel(cx, cy=-0.5, h=2.6):
    """The gate: two ink posts and a kraft panel between them. Returns (posts, panel)."""
    posts = VGroup(*[Rectangle(width=0.2, height=h + 0.3, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([cx + dx, cy, 0])
                     for dx in (-0.7, 0.7)])
    panel = Rectangle(width=1.2, height=h, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([cx, cy, 0])
    return posts, panel


def open_gate(panel):
    return panel.animate.stretch(0.08, 1, about_point=panel.get_bottom())


def cabinet(ox, oy, s=0.95):
    return project_cabinet(Iso(ox, oy, s))


def ghost_cabinet(ox, oy, s=0.95):
    """The cabinet as a dashed outline: a storage space that does not exist yet."""
    iso = Iso(ox, oy, s)
    top = iso.quad([(0, 0, 2.0), (1.3, 0, 2.0), (1.3, 1.1, 2.0), (0, 1.1, 2.0)], STAGE, stroke=BAR1, sw=4)
    front = iso.quad([(0, 0, 0), (1.3, 0, 0), (1.3, 0, 2.0), (0, 0, 2.0)], STAGE, stroke=BAR1, sw=4)
    side = iso.quad([(0, 0, 0), (0, 1.1, 0), (0, 1.1, 2.0), (0, 0, 2.0)], STAGE, stroke=BAR1, sw=4)
    g = VGroup(side, front, top)
    for m in g:
        m.set_stroke(opacity=0.9)
    return g


def form_page(ox, oy, s=0.9):
    return Iso(ox, oy, s).page(0, 0, 0, 1.3, 1.6)


def cmd_box(x, y, s=0.8):
    """The command box (job box from the AICR cast) with its word under it."""
    box = job_box(Iso(0, 0, s))
    box.move_to([x, y, 0])
    lab = T("add", 34).next_to(box, DOWN, buff=0.12)
    return VGroup(box, lab)


def big_x(x, y, s=0.38, color=TERRA, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def qmark(x, y, size=96):
    return T("?", size, TERRA, bold=True).move_to([x, y, 0])


def curve(a, b, bend=0.6, color=INK, w=6):
    return CurvedArrow(np.array(a, dtype=float), np.array(b, dtype=float), angle=bend, color=color, stroke_width=w, tip_length=0.28)


# ─────────────── B10 · a login alone does not open the gate ───────────────
class B10_GateNeedsStorage(Scene):
    # GATE T portrait mask (type_check._pb_slots_in_scene reads these): professor_bear("1x1", 1.5, x=-5.4, y=-0.2)  professor_bear("1x1", 1.2, x=5.2, y=2.4)
    def construct(self):
        you = you_at(-5.4, -0.2)
        posts, panel = gate_panel(-1.4, -0.5)
        self.add(you, posts, panel)
        login = chip("Login", -3.7, -0.2, w=1.6)
        until(self, "A Northeastern login", lead=0.3)
        self.play(FadeIn(login, shift=RIGHT * 0.3), run_time=0.4)
        self.play(login.animate.shift(RIGHT * 0.7), run_time=0.7)                 # the login reaches the gate ...
        until(self, "won't get you")
        self.play(login.animate.shift(LEFT * 0.4), run_time=0.45, rate_func=rate_functions.ease_out_bounce)   # ... and is turned back
        self.play(FadeIn(big_x(-1.4, 1.2)), run_time=0.3)
        until(self, "Every user has to belong", lead=0.3)
        cab = cabinet(3.2, -1.5)
        lab = M("/projects", 34).move_to([3.7, -2.5, 0])
        self.play(FadeIn(cab, shift=DOWN * 0.5), FadeIn(lab), run_time=0.6)
        until(self, "a sponsor owns", lead=2.6)
        sp = sponsor_at(5.2, 2.4, 1.2)
        self.play(FadeIn(sp, shift=LEFT * 0.4), run_time=0.5)
        own = Line([4.5, 1.05, 0], [4.1, 0.55, 0], color=TERRA, stroke_width=7)
        self.play(Create(own), run_time=0.5)
        xx10 = [m for m in self.mobjects if isinstance(m, VGroup) and len(m) == 2 and isinstance(m[0], Line)]
        chip_m = chip("Member", 3.7, 2.6, size=36)
        self.play(FadeIn(chip_m, shift=DOWN * 0.3), run_time=0.4)
        self.play(chip_m.animate.move_to([-5.4, 1.9, 0]), run_time=0.9)           # membership travels to you ...
        self.play(open_gate(panel), FadeOut(login), *[FadeOut(m) for m in xx10], run_time=0.7)                # ... and the gate opens
        done(self)


# ─────────────── B11 · the storage space: a folder, 35 TB, request first ───────────────
class B11_StorageSpace(Scene):
    def construct(self):
        cab = cabinet(-1.2, -1.7, 1.2)
        lab = M("/projects", 38).move_to([-0.4, -2.75, 0])
        self.add(cab, lab)
        until(self, "The sponsor is", lead=0.2)
        sp = sponsor_at(-5.0, 0.2, 1.7, "PI or staff")
        self.play(FadeIn(sp, shift=RIGHT * 0.4), run_time=0.5)
        until(self, "free, up to thirty-five", lead=0.1)
        bar_o = Rectangle(width=4.4, height=0.5, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([4.2, -0.2, 0])
        bar_f = Rectangle(width=4.4, height=0.5, stroke_width=0, fill_color=BAR1, fill_opacity=1).move_to([4.2, -0.2, 0])
        self.add(bar_o)
        self.play(GrowFromEdge(bar_f, LEFT), run_time=1.2)
        self.play(FadeIn(T("35 TB", 56, bold=True).move_to([4.2, 0.8, 0])), FadeIn(chip("free", 4.2, -1.0, size=36, fill=TERRA, color="#FFFFFF", stroke=TERRA)), run_time=0.4)
        until(self, "has no space yet", lead=0.2)
        gh = ghost_cabinet(-1.2, -1.7, 1.2)
        self.play(FadeOut(cab), FadeOut(lab), FadeIn(gh), FadeOut(bar_f), run_time=0.5)
        until(self, "they request one first", lead=0.2)
        pg = form_page(-1.6, 1.5, 0.8)
        self.play(FadeIn(pg, shift=DOWN * 0.3), run_time=0.4)
        self.play(pg.animate.shift(DOWN * 1.4 + RIGHT * 0.2), run_time=0.7)
        self.play(FadeOut(gh), FadeOut(pg), FadeIn(cabinet(-1.2, -1.7, 1.2)), FadeIn(lab), FadeIn(bar_f), run_time=0.6)
        done(self)


# ─────────────── B12 · four roles as a ladder ───────────────
class B12_RoleLadder(Scene):
    ROWS = [("PI", "owns it · adds members, guests, delegates", 11.2),
            ("Delegate", "adds members", 8.6),
            ("Member", "reads · writes · runs", 8.6),
            ("Guest", "reads · runs · can't write", 8.6)]
    YS = [2.55, 0.85, -0.85, -2.55]

    def row(self, i):
        role, what, w = self.ROWS[i]
        y = self.YS[i]
        box = RoundedRectangle(width=w, height=1.25, corner_radius=0.2, fill_color="#FFFFFF" if i != 3 else CARD, fill_opacity=1,
                               stroke_color=BAR1, stroke_width=4).move_to([-5.7 + w / 2, y, 0])
        rl = T(role, 48, bold=True).move_to([-6.2, y, 0], aligned_edge=LEFT)
        rl.align_to(box, LEFT).shift(RIGHT * 0.35)
        wl = T(what, 38).move_to([0, y, 0])
        wl.next_to(rl, RIGHT, buff=0.55)
        return VGroup(box, rl, wl)

    def construct(self):
        rows = [self.row(i) for i in range(4)]
        rails = VGroup(*[Line([x, 3.4, 0], [x, -3.4, 0], color=BAR2, stroke_width=5) for x in (-6.0,)])
        self.add(rails)
        until(self, "The PI owns", lead=0.3)
        self.play(FadeIn(rows[0], shift=RIGHT * 0.4), run_time=0.5)
        until(self, "A delegate can add", lead=0.3)
        self.play(FadeIn(rows[1], shift=RIGHT * 0.4), run_time=0.5)
        until(self, "A member reads", lead=0.3)
        self.play(FadeIn(rows[2], shift=RIGHT * 0.4), run_time=0.5)
        until(self, "A guest reads", lead=0.3)
        self.play(FadeIn(rows[3], shift=RIGHT * 0.4), run_time=0.5)
        until(self, "can't write", lead=0.4)
        strike = Line(rows[3][2].get_right() + LEFT * 1.75, rows[3][2].get_right() + LEFT * 0.05, color=TERRA, stroke_width=8)
        strike.shift(DOWN * 0.0)
        self.play(Create(strike), rows[3][0].animate.set_stroke(TERRA), run_time=0.5)
        done(self)


# ─────────────── B20 · two routes in ───────────────
class B20_TwoRoutes(Scene):
    # GATE T portrait mask: professor_bear("1x1", 1.5, x=-5.6, y=0.0)  professor_bear("1x1", 1.0, x=-0.7, y=2.9)  professor_bear("1x1", 1.0, x=1.3, y=2.9)
    def construct(self):
        you = you_at(-5.6, 0.0, 1.5)
        cab = cabinet(3.8, -0.9, 0.95)
        stor = M("/projects", 32).move_to([4.3, -1.95, 0])
        sp = sponsor_at(-0.7, 2.9, 1.0)
        self.add(you, cab, stor)
        until(self, "Route A", lead=0.2)
        pa = curve([-4.6, 0.7, 0], [3.0, 0.9, 0], bend=-0.5, color=INK)
        la = chip("A · Sponsor adds you", -3.9, 2.2, size=34)
        self.play(FadeIn(sp, shift=DOWN * 0.3), Create(pa), FadeIn(la), run_time=0.9)
        until(self, "Route B", lead=0.2)
        pb = curve([-4.6, -0.9, 0], [3.0, -1.2, 0], bend=0.5, color=INK)
        pg = form_page(-2.3, -3.5, 0.7)
        lb = chip("B · The form", 1.2, -3.0, size=34)
        self.play(Create(pb), FadeIn(lb), FadeIn(pg), run_time=0.9)
        until(self, "recommends every PI", lead=0.2)
        dg = delegate_at(1.3, 2.9, 1.0)
        self.play(FadeIn(dg, shift=LEFT * 0.4), run_time=0.5)
        until(self, "never waits", lead=0.4)
        dot = Dot([-4.6, 0.7, 0], radius=0.16, color=TERRA)
        self.add(dot)
        self.play(sp.animate.set_opacity(0.35), MoveAlongPath(dot, pa), run_time=1.3, rate_func=linear)   # the route flows without the PI
        self.play(FadeOut(dot), run_time=0.2)
        done(self)


# ─────────────── B21 · route A without a terminal: the Managing /projects app (rung 3 sketch; labels from the announcement only) ───────────────
class B21_ManagingApp(Scene):
    def construct(self):
        win = RoundedRectangle(width=11.0, height=5.9, corner_radius=0.25, fill_color="#FFFFFF", fill_opacity=1,
                               stroke_color=INK, stroke_width=4).move_to([0, 0.1, 0])
        bar = M("Files → Managing /projects", 38).move_to([-0.5, 2.55, 0])
        rule = Line([-5.3, 2.1, 0], [5.3, 2.1, 0], color=GHOST, stroke_width=4)
        g_lab = T("Group", 40, bold=True).move_to([-4.0, 1.35, 0])
        g_box = RoundedRectangle(width=5.0, height=0.7, corner_radius=0.12, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([0.2, 1.35, 0])
        g_car = T("▼", 30).move_to([2.3, 1.35, 0])
        u_lab = T("Usernames", 40, bold=True).move_to([-3.85, 0.35, 0])
        u_box = RoundedRectangle(width=5.0, height=0.7, corner_radius=0.12, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([0.2, 0.35, 0])
        u_hint = T("comma-separated, no spaces", 38, DIM).move_to([0.2, -0.35, 0])
        launch = chip("Launch", 4.4, 0.85, w=1.8, size=40, fill=TERRA, color="#FFFFFF", stroke=TERRA)
        log_box = RoundedRectangle(width=10.0, height=1.3, corner_radius=0.12, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([0, -1.95, 0])
        log_lab = T("Output log", 38, bold=True).move_to([-4.0, -1.0, 0])
        ghosts = VGroup(*[Line([-4.6, -1.65 - 0.27 * i, 0], [-4.6 + w, -1.65 - 0.27 * i, 0], color=GHOST, stroke_width=7) for i, w in enumerate((5.8, 4.2, 5.0))])
        cap = T("Sketch of the announced controls", 38, DIM).move_to([0, -3.2, 0])
        self.add(win)
        until(self, "Open OnDemand", lead=0.3)
        self.play(FadeIn(bar, shift=DOWN * 0.2), Create(rule), FadeIn(cap), run_time=0.7)
        until(self, "picks the group", lead=0.2)
        self.play(FadeIn(g_lab), FadeIn(g_box), FadeIn(g_car), run_time=0.5)
        self.play(Indicate(g_box, color=TERRA, scale_factor=1.04), run_time=0.5)
        until(self, "types the usernames", lead=0.2)
        self.play(FadeIn(u_lab), FadeIn(u_box), run_time=0.4)
        typed = M("user1,user2", 38).next_to(u_box.get_left(), RIGHT, buff=0.2)
        self.play(Write(typed), FadeIn(u_hint), run_time=0.9)
        until(self, "clicks Launch", lead=0.2)
        self.play(FadeIn(launch, scale=0.8), run_time=0.4)
        self.play(launch.animate.scale(0.9), run_time=0.15)
        self.play(launch.animate.scale(1 / 0.9), run_time=0.15)
        until(self, "A log shows", lead=0.2)
        self.play(FadeIn(log_box), FadeIn(log_lab), run_time=0.4)
        self.play(LaggedStart(*[Create(g) for g in ghosts], lag_ratio=0.3), run_time=0.9)
        done(self)


# ─────────────── B23 · the delay: up to two hours, then a fresh session ───────────────
class B23_TwoHourDelay(Scene):
    def construct(self):
        face = Circle(radius=1.6, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-3.6, 0.6, 0])
        ticks = VGroup(*[Line(face.get_center() + 1.35 * np.array([np.sin(a), np.cos(a), 0]), face.get_center() + 1.55 * np.array([np.sin(a), np.cos(a), 0]),
                              color=INK, stroke_width=5) for a in np.linspace(0, 2 * PI, 12, endpoint=False)])
        hand = Line(face.get_center(), face.get_center() + UP * 1.2, color=TERRA, stroke_width=9)
        lab = T("up to 2 hours", 56, bold=True).move_to([-3.6, -1.7, 0])
        self.add(face, ticks, hand)
        until(self, "up to two hours", lead=0.3)
        self.play(Rotate(hand, angle=-2 * PI, about_point=face.get_center()), FadeIn(lab), run_time=1.8, rate_func=linear)
        until(self, "start a fresh login session", lead=0.4)
        old = chip("old session", 3.0, 1.6, w=3.6, size=40, fill=CARD, color=DIM, stroke=BAR2)
        new = chip("new session", 3.0, -0.2, w=3.6, size=40)
        self.play(FadeIn(old, shift=LEFT * 0.3), run_time=0.4)
        self.play(FadeIn(new, shift=LEFT * 0.3), run_time=0.4)
        self.play(Create(check(5.4, -0.2, 0.3, TERRA, 10)), run_time=0.5)
        done(self)


# ─────────────── B24 · the caveat: a first-time account is not confirmed ───────────────
class B24_NewUserCaveat(Scene):
    def construct(self):
        you = you_at(-4.2, -0.4, 1.8)
        sp = sponsor_at(5.2, 0.2, 1.4)
        self.add(you, sp)
        until(self, "Whether either way", lead=0.3)
        cmd = cmd_box(3.4, 0.2)
        self.play(FadeIn(cmd, shift=LEFT * 0.4), run_time=0.4)
        self.play(cmd.animate.move_to([-0.8, 0.2, 0]), run_time=1.2)               # the command travels toward you ...
        until(self, "never had an Explorer account", lead=0.5)
        tag = chip("No account yet", -4.2, 2.3, size=34)
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.4)
        q = qmark(-2.1, 0.5)
        self.play(FadeIn(q, scale=0.5), run_time=0.4)                             # ... and stops short: not confirmed
        until(self, "ask Research Computing", lead=0.3)
        self.play(Indicate(q, color=TERRA, scale_factor=1.15), run_time=0.5)
        until(self, "at r c help", lead=0.8)
        self.play(FadeIn(M("rchelp@northeastern.edu", 36).move_to([0.0, -2.9, 0]), shift=UP * 0.2), run_time=0.4)
        done(self)


# ─────────────── B36 · after you submit: HEDGED ("we think"), never stated as fact ───────────────
class B36_AfterSubmit(Scene):
    def construct(self):
        sp = sponsor_at(4.6, 0.9, 1.7)
        self.add(sp)
        until(self, "What happens after you submit", lead=0.3)
        pg = form_page(-5.4, -0.9, 1.0)
        self.play(FadeIn(pg, shift=RIGHT * 0.3), run_time=0.5)
        until(self, "We think your sponsor", lead=0.3)
        self.play(pg.animate.shift(RIGHT * 4.6 + UP * 0.2), run_time=1.0)
        lab = chip("We think this is how it works", -0.3, 2.9, size=40, stroke=BAR1)
        ap = chip("Approve", 0.6, -1.2, w=2.4, size=38, fill=CARD, color=INK, stroke=BAR1)
        dn = chip("Deny", 3.2, -1.2, w=2.0, size=38, fill=CARD, color=INK, stroke=BAR1)
        for c in (ap, dn):
            c[0].set_stroke(color=BAR1, width=4, opacity=1)
        self.play(FadeIn(lab, shift=DOWN * 0.2), FadeIn(ap), FadeIn(dn), run_time=0.6)
        until(self, "not a confirmed step", lead=0.3)
        q = qmark(1.9, -2.15, 90)
        self.play(FadeIn(q, scale=0.5), run_time=0.4)
        until(self, "Confirm with Research", lead=0.3)
        self.play(Indicate(q, color=TERRA, scale_factor=1.15), run_time=0.5)
        until(self, "at r c help", lead=0.8)
        self.play(FadeIn(M("rchelp@northeastern.edu", 36).move_to([0.0, -3.05, 0]), shift=UP * 0.2), run_time=0.4)
        done(self)


# ─────────────── B40 · which name is yours: the first login settles it ───────────────
class B40_WhichName(Scene):
    def construct(self):
        ex = M("s.caplins", 72).move_to([-1.6, 2.3, 0])
        exl = T("an example from Research Computing", 38, DIM).next_to(ex, DOWN, buff=0.25)
        slot = RoundedRectangle(width=3.4, height=1.6, corner_radius=0.25, fill_color="#FFFFFF", fill_opacity=1,
                                stroke_color=INK, stroke_width=4).move_to([4.3, -1.3, 0])
        slot_l = T("First login", 44, bold=True).move_to(slot)
        c1 = chip("UserID", -4.4, -1.1, size=40, fill=BOX_L, color=INK)
        t1 = T("try first", 36).next_to(c1, DOWN, buff=0.2)
        c2 = chip("email prefix", -1.0, -1.1, size=36)
        t2 = T("second", 36, DIM).next_to(c2, DOWN, buff=0.2)
        self.add(slot, slot_l)
        until(self, "s dot caplins", lead=0.4)
        self.play(Write(ex), run_time=0.9)
        self.play(FadeIn(exl), run_time=0.4)
        until(self, "In the one real login", lead=0.3)
        self.play(FadeIn(c1, shift=UP * 0.3), FadeIn(t1), run_time=0.6)
        until(self, "not the email prefix", lead=0.2)
        self.play(FadeIn(c2, shift=UP * 0.3), FadeIn(t2), run_time=0.5)
        until(self, "Your first login", lead=0.3)
        self.play(c1.animate.move_to([0.5, -0.8, 0]).scale(0.85), c2.animate.move_to([0.5, -1.7, 0]).scale(0.85),
                  FadeOut(t1), FadeOut(t2), run_time=0.9)
        self.play(Create(check(4.3, -0.15, 0.3, TERRA, 10)), run_time=0.5)
        done(self)


# ─────────────── B44 · home and scratch ───────────────
class B44_HomeScratch(Scene):
    def construct(self):
        iso_h, iso_s = Iso(-4.3, -1.0, 0.95), Iso(1.6, -1.6, 0.95)
        until(self, "Your home", lead=0.3)
        hb = home_box(iso_h)
        self.play(FadeIn(hb, shift=DOWN * 0.5), run_time=0.5)
        hl = M("/home/<username>", 36).move_to([-3.4, -2.55, 0])
        until(self, "slash home", lead=0.2)
        self.play(Write(hl), run_time=0.8)
        until(self, "Your scratch", lead=0.3)
        back, front = scratch_bin(iso_s)
        self.play(FadeIn(back, shift=DOWN * 0.5), FadeIn(front, shift=DOWN * 0.5), run_time=0.5)
        sl = M("/scratch/<username>", 36).move_to([3.1, -2.75, 0])
        until(self, "slash scratch", lead=0.2)
        self.play(Write(sl), run_time=0.9)
        done(self)


# ─────────────── B50 · rejected at the door ───────────────
class B50_Rejected(Scene):
    # GATE T portrait mask: professor_bear("1x1", 1.5, x=-5.4, y=-0.2)
    def construct(self):
        you = you_at(-5.4, -0.2)
        posts, panel = gate_panel(-1.6, -0.5)
        x50 = big_x(-1.6, 1.0)
        self.add(you, posts, panel, x50)
        until(self, "Either you have no", lead=0.3)
        t1 = chip("No account yet", 2.4, 2.5, size=36)
        self.play(FadeIn(t1, shift=LEFT * 0.3), run_time=0.4)
        until(self, "or the username is wrong", lead=0.3)
        t2 = chip("Wrong username", 2.4, 1.3, size=36)
        self.play(FadeIn(t2, shift=LEFT * 0.3), run_time=0.4)
        until(self, "Try the user I D", lead=0.3)
        pg = form_page(1.2, -2.5, 0.9)
        self.play(FadeIn(pg, shift=UP * 0.3), run_time=0.4)
        ring = Circle(radius=0.32, color=TERRA, stroke_width=8).move_to(Iso(1.2, -2.5, 0.9).p(0.2, 1.4, 0.06))
        self.play(Create(ring), run_time=0.4)
        self.wait(0.2)
        self.play(FadeOut(ring), run_time=0.3)           # transient: a terracotta ring alive at the clip midpoint trips GATE T
        pgr = VGroup(pg)
        until(self, "then your email prefix", lead=0.2)
        t3 = chip("email prefix", 5.0, -0.3, size=34)
        self.play(FadeIn(t3, shift=LEFT * 0.3), run_time=0.4)
        until(self, "wait a while", lead=0.5)
        t4 = chip("Wait a while", 5.0, -1.5, size=34)
        self.play(FadeIn(t4, shift=LEFT * 0.3), run_time=0.4)
        until(self, "submit the form", lead=0.3)
        self.play(pgr.animate.shift(LEFT * 2.9 + UP * 0.1), run_time=0.9)
        self.play(open_gate(panel), FadeOut(x50), FadeOut(t1), FadeOut(t2), FadeOut(t3), FadeOut(t4), run_time=0.6)
        done(self)


# ─────────────── B51 · in, but not in the project ───────────────
class B51_NotInProject(Scene):
    def construct(self):
        you = you_at(-5.4, 0.0)
        sp = sponsor_at(4.6, 1.9, 1.3, "PI or delegate")
        cab = cabinet(1.8, -1.9)
        lab = M("/projects", 32).move_to([2.3, -2.9, 0])
        lst_box = RoundedRectangle(width=3.6, height=2.0, corner_radius=0.2, fill_color="#FFFFFF", fill_opacity=1,
                                   stroke_color=INK, stroke_width=4).move_to([-2.0, 0.1, 0])
        lst_h = M("groups", 36).move_to([-2.0, 0.75, 0])
        slot = RoundedRectangle(width=3.0, height=0.6, corner_radius=0.12, fill_opacity=0, stroke_color=BAR2, stroke_width=3).move_to([-2.0, -0.2, 0])
        self.add(you, cab, lab, lst_box, lst_h, slot)
        until(self, "You can log in", lead=0.2)
        self.play(Create(check(-3.7, 1.9, 0.3, TERRA, 10)), run_time=0.5)
        until(self, "doesn't list the project", lead=0.3)
        self.play(Indicate(slot, color=TERRA, scale_factor=1.06), run_time=0.7)
        until(self, "hasn't added you", lead=0.3)
        self.play(FadeIn(sp, shift=LEFT * 0.4), run_time=0.5)
        until(self, "run the add command", lead=0.4)
        cmd = cmd_box(3.3, -0.6, 0.7)
        self.play(FadeIn(cmd), run_time=0.3)
        self.play(cmd.animate.move_to([0.5, -0.2, 0]).scale(0.6), run_time=1.1)
        row = M("project", 34).move_to([-2.0, -0.2, 0])
        self.play(FadeOut(cmd), FadeIn(row), slot.animate.set_stroke(TERRA), run_time=0.5)
        done(self)


# ─────────────── B52 · a sponsor with no storage space ───────────────
class B52_NoStorage(Scene):
    def construct(self):
        sp = sponsor_at(-5.0, 0.0, 1.7)
        gh = ghost_cabinet(0.2, -1.5, 1.05)
        self.add(sp, gh)
        until(self, "nothing to add people to", lead=0.5)
        cmd = cmd_box(-2.8, 0.3, 0.7)
        self.play(FadeIn(cmd), run_time=0.3)
        self.play(cmd.animate.shift(RIGHT * 1.7), run_time=0.7)
        self.play(cmd.animate.shift(LEFT * 0.5), run_time=0.4, rate_func=rate_functions.ease_out_bounce)     # nothing to land in
        xx = big_x(-0.4, 0.5, 0.3)
        self.play(FadeIn(xx), run_time=0.3)
        until(self, "Submit the storage", lead=0.3)
        self.play(FadeOut(cmd), FadeOut(xx), run_time=0.2)
        pg = form_page(-3.0, 1.8, 0.85)
        self.play(FadeIn(pg, shift=DOWN * 0.3), run_time=0.4)
        self.play(pg.animate.shift(RIGHT * 3.2 + DOWN * 1.3), run_time=0.8)
        self.play(FadeOut(gh), FadeOut(pg), FadeIn(cabinet(0.2, -1.5, 1.05)), run_time=0.6)
        until(self, "write to r c help", lead=0.4)
        self.play(FadeIn(M("rchelp@northeastern.edu", 36).move_to([2.6, -3.0, 0]), shift=UP * 0.2), run_time=0.4)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh scene discovery
for _cls in (B10_GateNeedsStorage, B11_StorageSpace, B12_RoleLadder, B20_TwoRoutes, B36_AfterSubmit, B21_ManagingApp, B23_TwoHourDelay, B24_NewUserCaveat,
             B40_WhichName, B44_HomeScratch, B50_Rejected, B51_NotInProject, B52_NoStorage):
    _cls.play = ST.play
