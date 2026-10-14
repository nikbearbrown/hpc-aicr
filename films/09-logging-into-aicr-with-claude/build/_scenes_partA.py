# ═════════════════════════════ PART A — Act I and Act II drawings (B10 B11 B13 B14 B20 B21 B22) ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.

def act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


class B10_KeyAndCert(Scene):
    """AICR checks two things at its door: a private key and a certificate; together they open the lock."""
    def construct(self):
        title = act_title("I · What AICR Checks")
        iso = Iso(3.6, -2.0, 1.15)
        stack, lights = aicr_rack(iso)
        door = Rectangle(width=2.5, height=3.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.5, -0.15, 0])
        lock = padlock(0.5, -0.1, s=1.4)
        aicr = T("AICR", 40).move_to([4.0, -3.05, 0])
        self.play(FadeIn(title), FadeIn(stack), FadeIn(lights), FadeIn(door), FadeIn(lock), FadeIn(aicr), run_time=0.5)
        # "AICR has no password": a password chip appears and is struck out
        hear(self, "has no password", lead=0.35)
        pw = chip("password", -2.2, 1.9, size=36)
        self.play(FadeIn(pw), run_time=0.3)
        hear(self, "at the front door", lead=0.35)
        cross = x_mark(-0.8, 1.9, r=0.3, w=9)
        self.play(Create(cross), run_time=0.3)
        # "a private key": slides in from the left
        hear(self, "a private key", lead=0.5)
        key = key_obj(-8.6, 0.6, s=1.0)
        self.add(key)
        self.play(key.animate.shift(RIGHT * 4.6), run_time=0.7, rate_func=smooth)
        klab = T("private key", 36).move_to([-2.9, -0.25, 0])
        self.play(FadeIn(klab), run_time=0.25)
        # "a certificate": slides in from below
        hear(self, "and a certificate", lead=0.5)
        cert = cert_page(-2.6, -5.0, w=1.7, h=2.1)
        self.add(cert)
        self.play(cert.animate.shift(UP * 3.4), run_time=0.7, rate_func=smooth)
        clab = T("certificate", 36).move_to([-2.6, -2.95, 0])
        self.play(FadeIn(clab), run_time=0.25)
        # "AICR's own certificate authority signed": the seal pulses, 'signed by AICR' lands
        hear(self, "own certificate authority", lead=0.3)
        self.play(Indicate(cert.seal, color=TERRA, scale_factor=1.5), run_time=0.7)
        # "saying that key is yours": key and certificate go to the lock; it opens; the rack wakes
        hear(self, "saying that key", lead=0.6)
        self.play(FadeOut(klab), FadeOut(clab), FadeOut(pw), FadeOut(cross), run_time=0.2)
        self.play(key.animate.shift(RIGHT * 2.5 + DOWN * 0.1), cert.animate.shift(RIGHT * 1.3 + UP * 0.1), run_time=0.8)
        self.play(unlock_anim(lock), run_time=0.5)
        self.play(door.animate.stretch_to_fit_width(0.4).shift(LEFT * 1.0), *[l.animate.set_color(TERRA) for l in lights], run_time=0.7)
        done(self)


class B21_UnlockOnce(Scene):
    """You, not Claude, type the passphrase once: the lock opens and the key goes into the ssh-agent."""
    def construct(self):
        you = professor_bear("1x1", 2.8, seed="B21x", x=-5.0, y=-0.2)
        ylab = T("you", 38).move_to([-5.0, -2.3, 0])
        key = key_obj(-2.4, 0.2, s=1.2)
        lock = padlock(-2.4, 0.2, s=1.2)
        iso = Iso(4.4, -1.9, 1.2)
        agent, alights = agent_slab(iso)
        alab = T("agent", 40).move_to([4.4, -3.0, 0])
        claude = logo_chip("claude", 1.2, 2.5)
        self.play(FadeIn(you), FadeIn(ylab), FadeIn(key), FadeIn(lock), FadeIn(agent), FadeIn(alights), FadeIn(alab), run_time=0.5)
        # "not to give Claude the passphrase": the passphrase dots head for Claude and are refused
        hear(self, "give Claude the passphrase", lead=0.6)
        dots = chip("••••••", -3.6, 1.7, size=40)
        self.play(FadeIn(claude), FadeIn(dots), run_time=0.3)
        self.play(dots.animate.move_to([-0.9, 2.5, 0]), run_time=0.6)
        refuse = x_mark(2.6, 2.5, r=0.3, w=9)
        self.play(Create(refuse), run_time=0.25)
        self.play(dots.animate.move_to([-3.6, 1.7, 0]), FadeOut(claude), FadeOut(refuse), run_time=0.5)
        # "unlock the key ... in your own terminal": the dots go to the lock, which opens
        hear(self, "unlock the key", lead=0.2)
        self.play(dots.animate.move_to([-2.4, 1.3, 0]), run_time=0.6)
        self.play(unlock_anim(lock, rt=0.5), FadeOut(dots), run_time=0.5)
        # "into a helper called ssh-agent": the key travels into the agent slab
        hear(self, "into a helper", lead=0.2)
        self.play(FadeOut(lock), run_time=0.2)
        self.play(key.animate.scale(0.6).move_to([4.4, 0.95, 0]), run_time=1.0, rate_func=smooth)
        # "holds the unlocked key in memory": the agent's light comes on
        hear(self, "holds the unlocked key", lead=0.2)
        self.play(alights[0].animate.set_color(TERRA), Indicate(agent, color=INK, scale_factor=1.04), run_time=0.7)
        done(self)


class B22_AgentAnswers(Scene):
    """ssh asks the agent; the agent answers; the key never leaves it; the command reaches AICR."""
    def construct(self):
        iso = Iso(-4.8, -1.9, 1.1)
        box = job_box(iso, 0, 0, 0, s=1.0)
        blab = M("ssh", 40).move_to([-4.8, -2.9, 0])
        side = T("Claude's side", 36).move_to([-4.6, 3.0, 0])
        iso2 = Iso(0.4, -1.9, 1.2)
        agent, alights = agent_slab(iso2)
        alights[0].set_color(TERRA)
        key = key_obj(-0.2, 0.55, s=0.6)
        alab = T("agent", 40).move_to([0.4, -3.0, 0])
        iso3 = Iso(4.4, -2.0, 0.9)
        rack, rlights = aicr_rack(iso3)
        rlab = T("AICR", 40).move_to([4.8, -3.05, 0])
        bar = DashedLine([-2.2, -2.6, 0], [-2.2, 3.0, 0], color=BAR1, stroke_width=6, dash_length=0.3)
        self.play(FadeIn(box), FadeIn(blab), FadeIn(side), FadeIn(agent), FadeIn(alights), FadeIn(key), FadeIn(alab), FadeIn(rack), FadeIn(rlights), FadeIn(rlab), Create(bar), run_time=0.5)
        # "it asks the agent": a question chip travels to the agent
        hear(self, "it asks the agent", lead=0.35)
        q = chip("key?", -3.4, 1.4, size=36)
        self.play(FadeIn(q), run_time=0.2)
        self.play(q.animate.move_to([-0.6, 1.4, 0]), run_time=0.6)
        # "the agent answers": a signed slip comes back
        hear(self, "and the agent answers", lead=0.3)
        slip = VGroup(paper(0.0, 0.0, w=1.0, h=1.0, fill=PAGE_TOP), check(0.0, 0.0, s=0.28))
        slip.move_to([-0.6, 1.4, 0])
        self.play(FadeOut(q), FadeIn(slip), run_time=0.25)
        self.play(slip.animate.move_to([-3.4, 1.4, 0]), run_time=0.6)
        # "the key never leaves the agent": a dashed path from the key toward Claude's side is struck out
        hear(self, "never leaves the agent", lead=0.2)
        out = DashedLine([-0.9, 0.55, 0], [-1.8, 0.55, 0], color=BAR1, stroke_width=6, dash_length=0.2)
        self.play(Create(out), run_time=0.4)
        no = x_mark(-2.0, 0.55, r=0.28, w=9)
        self.play(Create(no), run_time=0.3)
        # "Claude does the work": the command box, slip in hand, rides on to AICR
        hear(self, "Claude does the work", lead=0.3)
        self.play(FadeOut(out), FadeOut(no), FadeOut(slip), run_time=0.2)
        self.play(box.animate.shift(UP * 1.9), blab.animate.shift(UP * 0.0), run_time=0.4)
        self.play(box.animate.shift(RIGHT * 6.6), run_time=0.9, rate_func=smooth)
        self.play(box.animate.shift(DOWN * 1.4), run_time=0.3)
        hear(self, "never passes through it", lead=0.3)
        self.play(*[l.animate.set_color(TERRA) for l in rlights], run_time=0.5)
        done(self)
