# ═════════════════════════════ PART C — Act IV close and Act V (B42 B50 B51 B52) ═════════════════════════════

def pC_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pC_rule_chip(text, left, y, size=32):
    """A white rule pill, left edge at `left`; returns the chip group."""
    w = 0.165 * len(text) + 0.8
    return chip(text, left + w / 2, y, w=w, size=size)


def pC_stop(x, y, r=0.38):
    """A stop mark: ink octagon with a pale bar."""
    o = RegularPolygon(n=8, radius=r, start_angle=PI / 8, fill_color=INK, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y, 0])
    bar = Rectangle(width=r * 1.1, height=r * 0.3, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    return VGroup(o, bar)


class B42_AskBeforeChange(Scene):
    """Four rules land beside the agent at the login rack: read-only, ask first, no compute, stop on a prompt."""
    def construct(self):
        iso = Iso(-4.9, -2.55, 0.8)
        rack, rlights = explorer_rack(iso)
        rlab = T("login node", 36).move_to([-4.6, -3.0, 0])
        claude = logo_chip("claude", -5.1, 0.6, h=1.3)
        self.play(FadeIn(rack), FadeIn(rlights), FadeIn(rlab), FadeIn(claude), run_time=0.5)
        hear(self, "follows the rules", lead=0.3)
        self.play(Indicate(claude, color=INK, scale_factor=1.08), run_time=0.7)

        left = 0.0
        ys = [2.0, 0.7, -0.6, -1.9]
        ix = -2.0
        # rule 1: read-only first (ticked)
        hear(self, "Read only first", lead=0.35)
        c1 = pC_rule_chip("read-only first", left, ys[0])
        t1 = check(ix, ys[0], s=0.3, w=9)
        self.play(FadeIn(c1, shift=LEFT * 0.5), run_time=0.35)
        self.play(Create(t1), run_time=0.3)
        # rule 2: ask before submit, cancel, delete (a gate; the portrait holds the key)
        hear(self, "Ask before it submits", lead=0.4)
        c2 = pC_rule_chip("ask before submit, cancel, delete", left, ys[1])
        you = professor_bear("1x1", 1.0, seed="B42gate", x=-3.0, y=ys[1])
        key = key_obj(-2.35, ys[1] - 0.05, s=0.2)
        post1 = Line([-1.5, ys[1] - 0.45, 0], [-1.5, ys[1] + 0.45, 0], color=INK, stroke_width=8)
        post2 = Line([-0.8, ys[1] - 0.45, 0], [-0.8, ys[1] + 0.45, 0], color=INK, stroke_width=8)
        bar = Line([-1.5, ys[1] + 0.1, 0], [-0.8, ys[1] + 0.1, 0], color=INK, stroke_width=8)
        self.play(FadeIn(c2, shift=LEFT * 0.5), run_time=0.35)
        self.play(FadeIn(you), FadeIn(key), Create(post1), Create(post2), Create(bar), run_time=0.4)
        # rule 3: no compute on the login node (a crossed job box on the login rack)
        hear(self, "Never compute", lead=0.35)
        c3 = pC_rule_chip("no compute on the login node", left, ys[2])
        box = job_box(iso, 0.35, 0.35, 0.9, s=0.5)
        self.play(FadeIn(c3, shift=LEFT * 0.5), run_time=0.35)
        self.play(FadeIn(box, shift=DOWN * 0.5), run_time=0.4)
        no = x_mark(-4.9, -1.1, r=0.3, w=9)
        x3 = x_mark(ix, ys[2], r=0.3, w=9)
        self.play(Create(no), Create(x3), run_time=0.3)
        # rule 4: a prompt means stop
        hear(self, "if any command", lead=0.4)
        c4 = pC_rule_chip("prompt: stop and tell you", left, ys[3])
        st = pC_stop(ix, ys[3])
        self.play(FadeIn(c4, shift=LEFT * 0.5), run_time=0.35)
        self.play(GrowFromCenter(st), run_time=0.3)
        hear(self, "stops and tells you", lead=0.2)
        self.play(Indicate(st, color=TERRA, scale_factor=1.25), run_time=0.6)
        done(self)


class B50_ExplorerVsAICR(Scene):
    """A three-column table builds row by row; each differing cell gets a terracotta dot as it lands."""
    def construct(self):
        title = pC_act_title("V · How It Differs From AICR")
        cx = [-4.3, -0.25, 3.85]
        rows = [1.85, 0.95, 0.03, -0.89, -1.81, -2.73]      # header, then five rows
        left, right = -6.0, 5.9
        top = 2.35
        bottom = rows[-1] - 0.46
        frame = VGroup(
            Line([left, top, 0], [right, top, 0], color=INK, stroke_width=4),
            Line([left, bottom, 0], [right, bottom, 0], color=INK, stroke_width=4),
            Line([-2.55, top, 0], [-2.55, bottom, 0], color=BAR1, stroke_width=4),
            Line([1.8, top, 0], [1.8, bottom, 0], color=BAR1, stroke_width=4))
        h1 = T("Explorer", 38, bold=True).move_to([cx[1], rows[0], 0])
        h2 = T("AICR", 38, bold=True).move_to([cx[2], rows[0], 0])
        self.play(FadeIn(title), Create(frame), run_time=0.5)
        hear(self, "On Explorer", lead=0.5)
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.3)

        def rule(i):
            y = rows[i] - 0.46
            return Line([left, y, 0], [right, y, 0], color=BAR2, stroke_width=3)

        def cell(text, col, i, mono=False):
            lab = M(text, 32) if mono else T(text, 32)
            lab.move_to([cx[col], rows[i], 0])
            dot = Dot([cx[col] - lab.width / 2 - 0.28, rows[i], 0], radius=0.1, color=TERRA)
            return lab, dot

        def land(*pairs, rt=0.3):
            anims = []
            for lab, dot in pairs:
                anims += [FadeIn(lab), GrowFromCenter(dot)]
            self.play(*anims, run_time=rt)

        # row 1: starts with
        r1 = T("starts with", 36).move_to([cx[0], rows[1], 0])
        self.play(FadeIn(r1), Create(rule(1)), run_time=0.3)
        hear(self, "you start with your password", lead=0.35)
        land(cell("password", 1, 1))
        # row 2: key
        hear(self, "you make your own key", lead=0.5)
        r2 = T("key", 36).move_to([cx[0], rows[2], 0])
        self.play(FadeIn(r2), Create(rule(2)), run_time=0.3)
        land(cell("you make it", 1, 2))
        hear(self, "there is no password", lead=0.35)
        land(cell("no password", 2, 1))
        hear(self, "You download a key", lead=0.35)
        land(cell("you download it", 2, 2))
        # row 3: certificate
        hear(self, "in a certificate", lead=0.35)
        r3 = T("certificate", 36).move_to([cx[0], rows[3], 0])
        self.play(FadeIn(r3), Create(rule(3)), run_time=0.3)
        land(cell("none", 1, 3))
        hear(self, "Certificate Authority", lead=0.4)
        land(cell("signed by AICR", 2, 3))
        # row 4: user name
        hear(self, "Your Explorer username", lead=0.4)
        r4 = T("user name", 36).move_to([cx[0], rows[4], 0])
        self.play(FadeIn(r4), Create(rule(4)), run_time=0.3)
        hear(self, "your university login", lead=0.4)
        land(cell("your university login", 1, 4))
        hear(self, "Your AICR name", lead=0.3)
        land(cell("<aicr-username>", 2, 4, mono=True))
        # row 5: access
        hear(self, "And access comes", lead=0.4)
        r5 = T("access", 36).move_to([cx[0], rows[5], 0])
        self.play(FadeIn(r5), Create(rule(5)), run_time=0.3)
        hear(self, "a project sponsor", lead=0.4)
        land(cell("project sponsor", 1, 5))
        hear(self, "from a proposal", lead=0.4)
        land(cell("proposal", 2, 5))
        done(self)


def pC_tick_chip(text, x, y, size=34):
    """A white pill with a ticked label (the tick sits left of the text)."""
    lab = T(text, size)
    w = lab.width + 1.5
    c = chip(text, x, y, w=w, size=size)
    c.label.move_to([x + 0.3, y, 0])
    tk = check(x - w / 2 + 0.5, y, s=0.17, w=7)
    return VGroup(c, tk)


class B51_WhatIsTheSame(Scene):
    """Both racks reach the same agent: the key goes into it once; four ticks land."""
    def construct(self):
        iso1 = Iso(-4.6, -0.35, 1.0)
        ex, exl = explorer_rack(iso1)
        exlab = T("Explorer", 40).move_to([-4.2, -0.95, 0])
        iso2 = Iso(3.7, -0.65, 0.8)
        ai, ail = aicr_rack(iso2)
        ailab = T("AICR", 40).move_to([4.2, -1.1, 0])
        iso3 = Iso(0.3, -0.35, 0.9)
        ag, agl = agent_slab(iso3)
        aglab = T("agent", 38).move_to([0.3, -0.95, 0])
        self.play(FadeIn(ex), FadeIn(exl), FadeIn(exlab), FadeIn(ai), FadeIn(ail), FadeIn(ailab), FadeIn(ag), FadeIn(agl), FadeIn(aglab), run_time=0.5)
        # "both are ssh"
        hear(self, "both are SSH", lead=0.5)
        l1 = DashedLine([-2.6, 0.7, 0], [-1.0, 0.7, 0], color=BAR1, stroke_width=6, dash_length=0.2)
        l2 = DashedLine([1.6, 0.7, 0], [2.4, 0.7, 0], color=BAR1, stroke_width=6, dash_length=0.2)
        self.play(Create(l1), Create(l2), run_time=0.4)
        c1 = pC_tick_chip("ssh", -4.6, -1.8)
        self.play(FadeIn(c1, shift=UP * 0.3), run_time=0.3)
        # "unlock a key once into the agent"
        hear(self, "unlock a key once", lead=0.45)
        key = key_obj(-0.35, 2.3, s=0.6)
        self.play(FadeIn(key), run_time=0.25)
        c2 = pC_tick_chip("unlock once", -1.6, -1.8)
        self.play(FadeIn(c2, shift=UP * 0.3), run_time=0.3)
        self.play(key.animate.shift(DOWN * 1.65), run_time=0.7, rate_func=smooth)
        self.play(agl[0].animate.set_color(TERRA), run_time=0.3)
        # "tested with batch mode"
        hear(self, "tested with batch mode", lead=0.45)
        c3 = pC_tick_chip("BatchMode", 2.6, -1.8)
        self.play(FadeIn(c3, shift=UP * 0.3), run_time=0.3)
        # "Claude never holds your password, passphrase or key"
        hear(self, "Claude never holds", lead=0.45)
        c4 = pC_tick_chip("Claude never holds it", 0.0, -2.85)
        self.play(FadeIn(c4, shift=UP * 0.3), run_time=0.35)
        hear(self, "or your key", lead=0.3)
        self.play(Indicate(c4, color=INK, scale_factor=1.06), run_time=0.5)
        done(self)


def pC_dash_chip(text, left, y, size=32):
    lab = T(text, size)
    w = lab.width + 0.7
    x = left + w / 2
    body = RoundedRectangle(width=w, height=0.85, corner_radius=0.42, fill_color=PAGE_L, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    edge = DashedVMobject(RoundedRectangle(width=w, height=0.85, corner_radius=0.42, stroke_color=BAR1, stroke_width=5, fill_opacity=0).move_to([x, y, 0]), num_dashes=36)
    lab.move_to([x, y, 0])
    return VGroup(body, edge, lab)


class B52_NotTested(Scene):
    """Three untested things land with open rings; then the one email that settles them."""
    def construct(self):
        left = -3.0
        ring_x = left - 0.55
        items = [("off campus or another network", 1.7, "off campus"), ("the web portal", 0.5, "the web portal"), ("agent access policy", -0.7, "research computing")]
        for text, y, cue in items:
            hear(self, cue, lead=0.5)
            c = pC_dash_chip(text, left, y)
            ring = Circle(radius=0.24, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([ring_x, y, 0])
            self.play(FadeIn(c, shift=LEFT * 0.4), run_time=0.35)
            self.play(Create(ring), run_time=0.3)
        hear(self, "ask once", lead=0.45)
        lab = M("rchelp@northeastern.edu", 32)
        w = lab.width + 1.5
        mail = chip("rchelp@northeastern.edu", 0.4, -2.2, w=w, mono=True, size=34)
        mail.label.move_to([0.4 + 0.3, -2.2, 0])
        env = VGroup(Rectangle(width=0.62, height=0.42, stroke_color=INK, stroke_width=4, fill_opacity=0),
                     Line([-0.31, 0.21, 0], [0, -0.03, 0], color=INK, stroke_width=4),
                     Line([0.31, 0.21, 0], [0, -0.03, 0], color=INK, stroke_width=4)).move_to([0.4 - w / 2 + 0.55, -2.2, 0])
        self.play(FadeIn(mail, shift=UP * 0.4), run_time=0.4)
        self.play(Create(env), run_time=0.3)
        done(self)
