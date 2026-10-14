# ═════════════════════════════ PART B — Act II and Act III drawings (B20 B30) ═════════════════════════════

def pB_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pB_tint(key, bow_fill, body_fill):
    """Recolour a key_obj: bow fill and shaft/teeth fill."""
    shaft, teeth, bow, hole = key
    bow.set_fill(bow_fill, 1)
    shaft.set_fill(body_fill, 1)
    for t in teeth:
        t.set_fill(body_fill, 1)
    return key


class B20_KeyPair(Scene):
    """A key in two halves: the private half stays with you; the public half is filed on Explorer's shelf; they match."""
    def construct(self):
        title = pB_act_title("II · Make And Install A Key")
        you = professor_bear("1x1", 2.3, seed="B20x", x=-5.05, y=-0.4)
        ylab = T("you", 38).move_to([-5.2, -2.25, 0])
        priv = pB_tint(key_obj(-3.3, 0.55, s=0.8), KRAFT_DEEP, BOX_R)
        lock = padlock(-3.3, -1.05, s=0.8)
        plab = T("private", 36).move_to([-1.75, -1.05, 0])
        iso = Iso(2.7, -2.3, 1.0)
        rack, rlights = explorer_rack(iso)
        elab = T("Explorer", 38).move_to([3.9, -2.7, 0])
        shelf = Rectangle(width=2.6, height=0.16, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.6, 0.15, 0])
        self.play(FadeIn(title), FadeIn(you), FadeIn(ylab), FadeIn(priv), FadeIn(lock), FadeIn(rack), FadeIn(rlights), FadeIn(elab), FadeIn(shelf), run_time=0.5)
        # "two halves": the lighter, lock-free public half appears above the private one
        hear(self, "two halves", lead=0.3)
        pub = pB_tint(key_obj(-3.3, 1.75, s=0.8), PAGE_TOP, PAGE_TOP)
        pubab = T("public", 36).move_to([-0.2, 1.75, 0])
        self.play(GrowFromCenter(pub), FadeIn(plab), run_time=0.5)
        self.play(FadeIn(pubab), run_time=0.25)
        # "stays on your computer": the padlock pulses
        hear(self, "stays on your computer", lead=0.1)
        self.play(Indicate(lock, color=INK, scale_factor=1.12), run_time=0.6)
        # "safe to hand out": the public half slides across to the login rack
        hear(self, "public half", lead=0.1)
        self.play(FadeOut(pubab), run_time=0.2)
        self.play(pub.animate.shift(RIGHT * 6.7 + DOWN * 0.3), run_time=1.0, rate_func=smooth)
        # "keep a copy": it is filed on the shelf and the rack light comes on
        hear(self, "keep a copy", lead=0.5)
        self.play(pub.animate.shift(DOWN * 0.95), rlights[0].animate.set_color(TERRA), run_time=0.6)
                # "your computer proves it holds the private half": the halves line up with a check
        hear(self, "proves it holds", lead=0.2)
        ck = check(0.5, 0.6, s=0.3, color=TERRA, w=10)
        gap = DashedLine([-1.0, 0.55, 0], [1.9, 0.55, 0], color=INK, stroke_width=4, dash_length=0.2)
        self.play(Create(gap), run_time=0.4)
        self.play(Create(ck), run_time=0.4)
        self.play(Indicate(pub, color=INK, scale_factor=1.1), Indicate(priv, color=INK, scale_factor=1.1), run_time=0.6)
        done(self)


class B30_UnlockOnce(Scene):
    """You type the passphrase once; the key goes into the agent; ssh asks the agent; the key never reaches Claude."""
    def construct(self):
        title = pB_act_title("III · Unlock It Once")
        you = professor_bear("1x1", 2.3, seed="B30x", x=-5.05, y=-0.5)
        ylab = T("you", 38).move_to([-5.2, -2.35, 0])
        key = key_obj(-3.1, -0.5, s=1.0)
        lock = padlock(-3.1, -0.5, s=1.1)
        iso = Iso(4.2, -2.0, 1.2)
        agent, alights = agent_slab(iso)
        alab = T("agent", 40).move_to([4.4, -3.0, 0])
        claude = logo_chip("claude", -1.6, 1.5)
        self.play(FadeIn(title), FadeIn(you), FadeIn(ylab), FadeIn(key), FadeIn(lock), FadeIn(agent), FadeIn(alights), FadeIn(alab), run_time=0.5)
        # "Claude cannot type a passphrase": the logo chip appears, a cross marks it
        hear(self, "Claude cannot type", lead=0.2)
        self.play(FadeIn(claude), run_time=0.3)
        hear(self, "a passphrase", lead=0.0)
        no = x_mark(0.2, 1.5, r=0.3, w=9)
        self.play(Create(no), run_time=0.3)
        # "you unlock the key yourself": the dots travel from you to the lock; it opens
        hear(self, "so you unlock", lead=0.0)
        self.play(FadeOut(claude), FadeOut(no), run_time=0.3)
        dots = chip("••••••", -4.4, 1.3, size=40)
        self.play(FadeIn(dots), run_time=0.3)
        self.play(dots.animate.move_to([-3.1, 0.9, 0]), run_time=0.6)
        self.play(unlock_anim(lock, rt=0.5), FadeOut(dots), run_time=0.5)
        # "into a helper called the ssh agent": the lock leaves, the key slides into the slab
        hear(self, "into a helper", lead=0.1)
        self.play(FadeOut(lock), run_time=0.2)
        self.play(key.animate.scale(0.6).move_to([4.4, 0.95, 0]), run_time=1.1, rate_func=smooth)
        # "the agent holds the unlocked key": light on, barrier line drawn
        hear(self, "holds the unlocked key", lead=0.2)
        self.play(alights[0].animate.set_color(TERRA), Indicate(agent, color=INK, scale_factor=1.04), run_time=0.6)
        bar = DashedLine([1.2, -2.6, 0], [1.2, 2.3, 0], color=BAR1, stroke_width=6, dash_length=0.3)
        self.play(Create(bar), run_time=0.4)
        # "ssh asks the agent": the Claude chip sends the ssh command box across
        hear(self, "ssh asks", lead=0.9)
        claude2 = logo_chip("claude", -2.6, 1.5)
        box = job_box(Iso(-2.9, -0.4, 0.9), 0, 0, 0, s=0.9)
        slab = M("ssh", 40).next_to(box, DOWN, buff=0.15)
        cmd = Group(box, slab)
        self.play(FadeIn(claude2), FadeIn(cmd), run_time=0.3)
        self.play(cmd.animate.shift(RIGHT * 4.8), run_time=0.8, rate_func=smooth)
        # "and the agent answers": a signed slip comes back; the key stays inside
        hear(self, "and the key never", lead=0.2)
        slip = Group(paper(0, 0, w=1.0, h=1.0, fill=PAGE_TOP), check(0, 0, s=0.28))
        slip.move_to([2.0, 1.5, 0])
        self.play(FadeIn(slip), run_time=0.2)
        self.play(slip.animate.move_to([-0.4, 1.5, 0]), run_time=0.6)
        # "never passes through Claude": a path from the key toward Claude is struck out
        hear(self, "passes through", lead=0.0)
        out = DashedLine([3.9, 0.95, 0], [3.3, 0.95, 0], color=BAR1, stroke_width=6, dash_length=0.2)
        self.play(Create(out), run_time=0.3)
        no2 = x_mark(3.0, 0.95, r=0.28, w=9)
        self.play(Create(no2), run_time=0.3)
        done(self)
