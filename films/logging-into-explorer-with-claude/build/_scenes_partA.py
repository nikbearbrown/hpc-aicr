# ═════════════════════════════ PART A — Act I opening (B10 B11 B12) ═════════════════════════════
# Cue times come from hear("spoken phrase"): measured word times. Labels are 1-3 words; real text only in mono.

def pA_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


class B10_PasswordToday(Scene):
    """You type the password to the login node; host key answered yes; no Duo on ssh; the web portal asks."""
    def construct(self):
        title = pA_act_title("I · What Explorer Asks For")
        you = professor_bear("1x1", 2.3, seed="B10x", x=-5.1, y=-0.7)
        ylab = T("you", 36).move_to([-5.1, -2.4, 0])
        iso = Iso(3.2, -2.2, 1.0)
        rack, rlights = explorer_rack(iso)
        rlab = T("login node", 36).move_to([4.0, -3.0, 0])
        self.play(FadeIn(title), FadeIn(you), FadeIn(ylab), FadeIn(rack), FadeIn(rlights), FadeIn(rlab), run_time=0.5)
        # "Northeastern password": an empty password chip appears beside the portrait
        hear(self, "Northeastern password", lead=0.3)
        pw = chip("password", -2.6, 1.0, size=36)
        self.play(FadeIn(pw), run_time=0.3)
        # "connect to the login host": the ssh arrow runs from you to the rack
        hear(self, "connect to the", lead=0.2)
        arrow = Arrow([-3.5, -0.9, 0], [2.1, -0.9, 0], buff=0, color=INK, stroke_width=8, max_tip_length_to_length_ratio=0.12)
        ssh = M("ssh", 36).move_to([-0.6, -0.45, 0])
        self.play(GrowArrow(arrow), FadeIn(ssh), run_time=0.8)
        # "first host key question": the question chip appears on the way
        hear(self, "first host key", lead=0.2)
        hk = chip("host key?", 0.3, 0.55, size=36)
        self.play(FadeIn(hk), run_time=0.3)
        # "with yes": the question is answered
        hear(self, "with yes", lead=0.15)
        hk2 = chip("host key? yes", 0.3, 0.55, size=36)
        self.play(ReplacementTransform(hk, hk2), run_time=0.3)
        self.play(Create(check(2.2, 0.55, s=0.22, w=8)), run_time=0.25)
        # "type the password": dots fill the password chip
        hear(self, "type the password", lead=0.2)
        dots = chip("••••••", -2.6, 1.0, size=40)
        self.play(ReplacementTransform(pw, dots), run_time=0.4)
        # "land on a login node": the rack's light comes on
        hear(self, "land on a", lead=0.3)
        self.play(rlights[0].animate.set_color(TERRA), rlights[1].animate.set_color(TERRA), Indicate(rack, color=INK, scale_factor=1.04), run_time=0.6)
        # "no Duo prompt for ssh": a Duo chip beside the arrow, struck out
        hear(self, "no Duo", lead=0.3)
        duo1 = chip("Duo", -0.3, -1.9, size=36)
        self.play(FadeIn(duo1), run_time=0.3)
        cross = x_mark(1.0, -1.9, r=0.28, w=9)
        self.play(Create(cross), run_time=0.3)
        # "The web portal is different": a web portal box with a Duo chip
        hear(self, "web portal", lead=0.3)
        portal = Rectangle(width=1.8, height=1.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([5.1, 1.5, 0])
        plab = T("web portal", 36).move_to([5.0, 2.45, 0])
        duo2 = chip("Duo", 2.6, 1.5, size=36)
        self.play(FadeIn(portal), FadeIn(plab), FadeIn(duo2), run_time=0.4)
        # "the documentation says it asks": ticked, 'asks (documented)'
        hear(self, "says it asks", lead=0.6)
        tick = check(3.9, 1.5, s=0.24, w=9)
        alab = T("asks (documented)", 34).move_to([4.45, 0.55, 0])
        self.play(Create(tick), FadeIn(alab), run_time=0.5)
        done(self)


class B11_NotForClaude(Scene):
    """Claude's hand stops short of the password; a key slides in beside the logo and opens the door to the login rack."""
    def construct(self):
        claude = logo_chip("claude", -5.3, 1.4)
        you = professor_bear("1x1", 2.0, seed="B11x", x=-2.3, y=-1.2)
        ylab = T("you", 36).move_to([-2.3, -2.65, 0])
        pw = chip("••••••", -2.3, 1.4, size=40)
        door = Rectangle(width=1.0, height=3.4, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.9, -0.5, 0])
        iso = Iso(3.2, -2.2, 1.0)
        rack, rlights = explorer_rack(iso)
        rlab = T("login node", 36).move_to([4.0, -3.0, 0])
        self.play(FadeIn(claude), FadeIn(you), FadeIn(ylab), FadeIn(pw), FadeIn(door), FadeIn(rack), FadeIn(rlights), FadeIn(rlab), run_time=0.5)
        # "does not work for Claude": the hand reaches toward the password and is stopped
        hear(self, "does not work", lead=0.3)
        hand = Arrow([-4.5, 1.4, 0], [-3.95, 1.4, 0], buff=0, color=INK, stroke_width=9, max_tip_length_to_length_ratio=0.4)
        self.play(GrowArrow(hand), run_time=0.5)
        stop = x_mark(-3.65, 1.4, r=0.22, w=9)
        self.play(Create(stop), run_time=0.25)
        # "no keyboard attached": a keyboard-less label under the logo
        hear(self, "no keyboard", lead=0.3)
        nk = T("no keyboard", 36).move_to([-4.85, 2.6, 0])
        self.play(FadeIn(nk), run_time=0.3)
        # "never hand it": the password stays with you, the hand pulls back
        hear(self, "never hand", lead=0.3)
        self.play(FadeOut(hand), FadeOut(stop), run_time=0.3)
        # "something the agent can use": a key slides in beside the logo
        hear(self, "something the agent", lead=0.3)
        key = key_obj(-8.2, 0.25, s=0.7)
        self.add(key)
        self.play(key.animate.shift(RIGHT * 2.6), run_time=0.7, rate_func=smooth)
        # "A key": the key goes to the door; the door opens to the rack
        hear(self, "a key", lead=0.5, nth=1)
        self.play(FadeOut(nk), FadeOut(pw), key.animate.shift(RIGHT * 4.0), run_time=0.7, rate_func=smooth)
        self.play(door.animate.stretch_to_fit_width(0.3).shift(LEFT * 0.5), *[l.animate.set_color(TERRA) for l in rlights], run_time=0.6)
        done(self)


class B12_WhichLoginName(Scene):
    """The user ID from the access form works; the email prefix is the second try; wait after a password change."""
    def construct(self):
        c1 = chip("user ID", -3.0, 1.3, mono=True, size=40)
        cap1 = T("from the access form", 34).move_to([-3.0, 0.35, 0])
        c2 = chip("email prefix", 3.0, 1.3, mono=True, size=40)
        cap2 = T("second try", 34).move_to([3.0, 0.35, 0])
        title_anchor = c1  # keeps the first frame non-empty
        self.play(FadeIn(c1), FadeIn(cap1), run_time=0.5)
        # "the name from the access form": the user ID chip is ringed and ticked
        hear(self, "from the access form", lead=0.2)
        ring = RoundedRectangle(width=c1.pill.width + 0.35, height=1.15, corner_radius=0.57, color=INK, stroke_width=7).move_to([-3.0, 1.3, 0])
        tick = check(-0.6, 1.3, s=0.24, w=9)
        self.play(Create(ring), run_time=0.4)
        self.play(Create(tick), run_time=0.3)
        # "not the first part of an email address": the email prefix chip
        hear(self, "not the first part", lead=0.3)
        self.play(FadeIn(c2), run_time=0.3)
        # "try the other": the second try caption
        hear(self, "try the other", lead=0.3)
        self.play(FadeIn(cap2), run_time=0.3)
        # "wait a little after any password change": a clock lands under them
        hear(self, "wait a little", lead=0.5)
        clock = VGroup(Circle(radius=0.55, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=6),
                       Line([0, 0, 0], [0, 0.34, 0], color=INK, stroke_width=7),
                       Line([0, 0, 0], [0.26, 0, 0], color=INK, stroke_width=7),
                       Dot([0, 0, 0], radius=0.07, color=TERRA))
        clock.move_to([-4.2, -1.4, 0])
        self.play(FadeIn(clock, shift=UP * 1.0), run_time=0.7, rate_func=smooth)
        wl = T("wait after a password change", 36).move_to([0.9, -1.4, 0])
        self.play(FadeIn(wl), run_time=0.35)
        done(self)
