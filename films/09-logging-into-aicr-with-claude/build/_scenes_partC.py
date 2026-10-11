# ═════════════════════════════ PART C — Act III close and Act IV drawings (B38 B40 B41 B42 B43 B44 B45) ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.

def pC_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pC_box(x, y, s=1.0):
    """An 'ssh' command box (kraft + terracotta tape) centred on (x, y)."""
    g = job_box(Iso(0, 0, s), 0, 0, 0, s=1.0)
    return g.move_to([x, y, 0])


def pC_cpill(text, x, y, mono=True, size=34):
    """A white pill with a spare right-hand end for a check: returns (chip, check_point)."""
    lab = M(text, size - 2) if mono else T(text, size)
    c = chip(text, x, y, w=lab.width + 1.5, mono=mono, size=size)
    return c, np.array([x + (lab.width + 1.5) / 2 - 0.5, y, 0.0])


class B38_NoVault(Scene):
    """No Keychain on Linux: the ssh box bounces off the lock until you run ssh-add; then the key rises into the agent."""
    def construct(self):
        you = professor_bear("1x1", 2.1, seed="B38y", x=-5.2, y=1.7)
        ylab = T("you", 38).move_to([-5.2, -0.05, 0])
        box = pC_box(-5.2, -1.6)
        blab = M("ssh", 40).move_to([-5.2, -3.12, 0])
        key = key_obj(-2.6, -1.6, s=0.8)
        lock = padlock(-2.6, -1.6, s=0.9)
        iso = Iso(3.6, -1.9, 1.2)
        agent, alights = agent_slab(iso)
        alab = T("agent", 40).move_to([3.6, -3.0, 0])
        self.play(FadeIn(you), FadeIn(ylab), FadeIn(box), FadeIn(blab), FadeIn(key), FadeIn(lock), FadeIn(agent), FadeIn(alights), FadeIn(alab), run_time=0.5)
        # "no Keychain to reload the key": a Keychain chip, struck out
        hear(self, "no keychain", lead=0.5)
        kc = chip("Keychain", 1.6, 0.9, size=36)
        self.play(FadeIn(kc), run_time=0.25)
        hear(self, "reload the key", lead=0.2)
        kx = x_mark(3.3, 0.9, r=0.28, w=9)
        self.play(Create(kx), run_time=0.25)
        # "this same test fails": the ssh box runs into the lock and bounces
        hear(self, "same test fails", lead=0.5)
        self.play(FadeOut(kc), FadeOut(kx), box.animate.shift(RIGHT * 1.1), blab.animate.shift(RIGHT * 1.1), run_time=0.5)
        bx = x_mark(-3.5, -0.25, r=0.28, w=9)
        self.play(Create(bx), box.animate.shift(LEFT * 0.3), blab.animate.shift(LEFT * 0.3), run_time=0.25)
        self.play(box.animate.shift(LEFT * 0.8), blab.animate.shift(LEFT * 0.8), run_time=0.3)
        # "you run SSH add again": the ssh-add chip, the lock opens, the key rises into the agent
        hear(self, "run ssh add", lead=0.2)
        sa = chip("ssh-add", -2.4, 2.7, mono=True, size=36)
        self.play(FadeIn(sa, shift=DOWN * 0.3), FadeOut(bx), run_time=0.3)
        self.play(unlock_anim(lock, rt=0.5), run_time=0.5)
        self.play(FadeOut(lock), run_time=0.15)
        self.play(key.animate.scale(0.6).move_to([3.6, 0.95, 0]), run_time=1.0, rate_func=smooth)
        self.play(alights[0].animate.set_color(TERRA), run_time=0.3)
        # "That is expected": the box now passes the place where the lock was
        hear(self, "that is expected", lead=0.2)
        self.play(box.animate.shift(RIGHT * 3.9), blab.animate.shift(RIGHT * 3.9), run_time=0.9, rate_func=smooth)
        ck = check(box.get_center()[0] + 0.0, box.get_center()[1] + 0.9, s=0.2, color=TERRA)
        self.play(Create(ck), run_time=0.3)
        # "at the start of each session": a 'session start' tag lands beside the ssh-add chip
        hear(self, "start of each session", lead=0.4)
        ss = chip("session start", -2.0, 1.6, size=36)
        self.play(FadeIn(ss, shift=DOWN * 0.4), run_time=0.4)
        done(self)


class B40_YouApprove(Scene):
    """Act IV opens: the ssh command waits at a gate; your check lands on its tag; the gate lifts and it goes on to AICR."""
    def construct(self):
        title = pC_act_title("IV · Rules For A Shared Cluster")
        you = professor_bear("1x1", 2.0, seed="B40", x=-2.2, y=1.2)
        ylab = T("you", 38).move_to([-0.4, 1.2, 0])
        gate = Rectangle(width=0.5, height=2.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-2.2, -1.0, 0])
        iso = Iso(3.8, -2.0, 1.0)
        rack, rlights = aicr_rack(iso)
        rlab = T("AICR", 40).move_to([4.3, -3.05, 0])
        box = pC_box(-5.4, -1.6)
        blab = M("ssh", 40).move_to([-5.4, -2.9, 0])
        bx = VGroup(box, blab)
        self.play(FadeIn(title), FadeIn(you), FadeIn(ylab), FadeIn(gate), FadeIn(rack), FadeIn(rlights), FadeIn(rlab), FadeIn(bx), run_time=0.5)
        # "Claude runs one ssh command": the box slides up to the gate and waits
        hear(self, "runs one ssh", lead=0.3)
        self.play(bx.animate.shift(RIGHT * 2.0), run_time=0.9, rate_func=smooth)
        # "with BatchMode on": the mono chip
        hear(self, "batch mode", lead=0.3)
        bm = chip("BatchMode", -4.7, 0.2, mono=True, size=34)
        self.play(FadeIn(bm), run_time=0.25)
        # the empty approval tag on the box
        hear(self, "asks you to", lead=0.4)
        tag = pill(-3.1, -0.35, 1.0, h=0.6)
        self.play(FadeIn(tag), run_time=0.25)
        # "approve it": your check lands on the tag
        hear(self, "approve it", lead=0.45)
        ck = check(-2.2, 0.45, s=0.2, color=TERRA)
        self.play(FadeIn(ck), run_time=0.15)
        self.play(ck.animate.move_to([-3.1, -0.35, 0]), run_time=0.4)
        # the gate lifts, the box goes on to the rack
        hear(self, "on a shared system", lead=0.3)
        bx.add(tag, ck)
        self.play(FadeOut(gate, shift=UP * 0.6), FadeOut(bm), run_time=0.4)
        self.play(bx.animate.shift(RIGHT * 4.1), run_time=1.1, rate_func=smooth)
        hear(self, "approve each", lead=0.1)
        self.play(*[l.animate.set_color(TERRA) for l in rlights], run_time=0.5)
        done(self)


class B41_ReadOnly(Scene):
    """Rule one: look before you change anything. Six read-only commands land one by one and each takes a check."""
    def construct(self):
        head = chip("Read only first", 0.9, 2.6, size=40)
        eye_out = Ellipse(width=1.9, height=1.0, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6)
        pupil = Dot([0, 0, 0], radius=0.22, color=INK)
        eye = VGroup(eye_out, pupil).move_to([-3.4, 2.6, 0])
        names = ["sinfo", "squeue -u $USER", "sacct", "jobstats", "ls", "module avail"]
        built = []
        for n in names:
            c, cp = pC_cpill(n, 0.0, 0.0)
            built.append((c, cp))
        rows = [[0, 1, 2], [3, 4, 5]]
        ys = [0.7, -1.0]
        pos = {}
        for r, ri in enumerate(rows):
            total = sum(built[i][0].width for i in ri) + 0.4 * (len(ri) - 1)
            x = -total / 2
            for i in ri:
                w = built[i][0].width
                pos[i] = np.array([x + w / 2, ys[r], 0.0])
                x += w + 0.4
        # "Rule one. Read only first": heading and the eye appear together
        hear(self, "read only first", lead=0.45)
        self.play(FadeIn(head), GrowFromCenter(eye), run_time=0.4)
        hear(self, "look before", lead=0.1)
        self.play(pupil.animate.shift(LEFT * 0.3), run_time=0.25)
        self.play(pupil.animate.shift(RIGHT * 0.6), run_time=0.3)
        cues = [("sinfo", 0.3), ("sq for", 0.3), ("sact", 0.3), ("job stats", 0.3), ("ls", 0.25), ("module avail", 0.3)]
        for i, (ph, ld) in enumerate(cues):
            c, cp = built[i]
            dx = pos[i] - c.get_center()
            c.shift(dx)
            hear(self, ph, lead=ld + 0.25)
            ck = check(cp[0] + (pos[i][0] - built[i][0].get_center()[0]) * 0, pos[i][1], s=0.15, color=TERRA, w=6)
            ck.move_to(c.get_right() + LEFT * 0.5)
            self.play(FadeIn(c, shift=DOWN * 0.4), run_time=0.25)
            self.play(Create(ck), run_time=0.2)
        self.play(pupil.animate.shift(LEFT * 0.3), run_time=0.3)
        done(self)


class B42_LoginCap(Scene):
    """Rule two: the login node is capped at 4 cores and 8 GB; the heavy job is stopped and goes through Slurm to the big rack."""
    def construct(self):
        iso = Iso(-4.4, -2.0, 1.0)
        small, slights = explorer_rack(iso)
        slab = T("login node", 38).move_to([-4.4, -2.95, 0])
        # the meter: ink-outlined bar, partly filled, with a cap line
        mx, my, mw, mh = -4.4, 1.2, 3.4, 0.5
        bar = Rectangle(width=mw, height=mh, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([mx, my, 0])
        left = mx - mw / 2
        fill = Rectangle(width=0.9, height=mh - 0.1, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([left + 0.05 + 0.45, my, 0])
        capx = left + 2.4
        cap = Line([capx, my - 0.5, 0], [capx, my + 0.5, 0], color=INK, stroke_width=10)
        big, blights = aicr_rack(Iso(4.1, -2.4, 1.0))
        blab = T("AICR", 40).move_to([4.5, -3.05, 0])
        gate = Rectangle(width=0.5, height=2.6, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([1.5, -1.1, 0])
        glab = T("Slurm", 40).move_to([1.5, 0.7, 0])
        heavy = pC_box(-0.3, -1.45, s=1.4)
        self.play(FadeIn(small), FadeIn(slights), FadeIn(slab), FadeIn(bar), FadeIn(fill), FadeIn(cap), FadeIn(big), FadeIn(blights), FadeIn(blab), run_time=0.5)
        # "never compute": the heavy job comes up to the login node and fills the meter to the cap
        hear(self, "never compute", lead=0.1)
        self.play(FadeIn(heavy), run_time=0.2)
        self.play(heavy.animate.shift(LEFT * 1.4), fill.animate.stretch_to_fit_width(2.35).move_to([left + 0.05 + 1.175, my, 0]), run_time=0.9, rate_func=smooth)
        stop = x_mark(-2.75, -0.2, r=0.3, w=9)
        self.play(Create(stop), run_time=0.25)
        # "capped at four ... eight": the hero labels
        hear(self, "four cpu cores", lead=0.45)
        n4 = T("4 cores", 46).move_to([-5.3, 2.35, 0])
        self.play(FadeIn(n4, shift=DOWN * 0.2), run_time=0.3)
        hear(self, "eight gigabytes", lead=0.45)
        n8 = T("8 GB", 46).move_to([-2.9, 2.35, 0])
        self.play(FadeIn(n8, shift=DOWN * 0.2), run_time=0.3)
        # "Heavy work goes through Slurm": back off, the Slurm gate rises
        hear(self, "heavy work", lead=0.2)
        self.play(FadeOut(stop), heavy.animate.shift(RIGHT * 1.7), FadeIn(gate), run_time=0.5)
        hear(self, "slurm", lead=0.3)
        self.play(FadeIn(glab), run_time=0.3)
        # "the scheduler": the gate lifts, the box shrinks and goes on to the big rack
        hear(self, "the scheduler", lead=0.2)
        self.play(FadeOut(gate, shift=UP * 0.6), run_time=0.35)
        self.play(heavy.animate.scale(0.5).move_to([1.35, -1.7, 0]), run_time=0.9, rate_func=smooth)
        hear(self, "for a live session", lead=0.5)
        self.play(*[l.animate.set_color(TERRA) for l in blights], run_time=0.5)
        done(self)


class B43_AskFirst(Scene):
    """Rule three: sbatch, scancel and rm each wait at the gate for your check; the shared GPUs count against your project."""
    def construct(self):
        you = professor_bear("1x1", 2.0, seed="B43q", x=0.0, y=2.0)
        ylab = T("you", 38).move_to([1.8, 2.0, 0])
        gate = Rectangle(width=0.5, height=3.0, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.0, -0.9, 0])
        iso = Iso(3.8, -2.2, 1.0)
        gpu, glights = iso.server(0, 0, 0, w=2.0, d=1.6, slab=0.5, n=2)
        glab = T("shared GPU", 38).move_to([4.0, -3.1, 0])
        self.play(FadeIn(you), FadeIn(ylab), FadeIn(gate), FadeIn(gpu), FadeIn(glights), FadeIn(glab), run_time=0.5)
        cmds = [("sbatch", "batch", 0.0), ("scancel", "cancel", 0.0), ("rm", "r m", -1.0)]
        for (name, ph, _), y in zip(cmds, [0.0, -1.0, -2.0]):
            c, cp = pC_cpill(name, -2.2, y)
            hear(self, ph, lead=0.2)
            self.play(FadeIn(c, shift=RIGHT * 0.3), run_time=0.2)
            ck = check(0.0, 1.0, s=0.16, color=TERRA, w=6)
            tx = -2.2 + (c.width / 2 - 0.5)
            self.play(FadeIn(ck), run_time=0.1)
            self.play(ck.animate.move_to([tx, y, 0]), run_time=0.3)
            grp = VGroup(c, ck)
            self.play(FadeOut(gate), run_time=0.12)
            self.play(grp.animate.shift(RIGHT * 3.6), run_time=0.45, rate_func=smooth)
            self.play(FadeIn(gate), run_time=0.12)
        # "shared GPUs ... count against your project"
        hear(self, "count against your project", lead=0.5)
        proj = chip("your project", 3.6, 1.2, size=38)
        self.play(FadeIn(proj, shift=DOWN * 0.3), *[l.animate.set_color(TERRA) for l in glights], run_time=0.6)
        done(self)


class B44_KeyStays(Scene):
    """Rule four: cat, scp and chat all bounce off the glass; the key stays in the agent and the agent's own arrow to AICR stays open."""
    def construct(self):
        side = T("Claude's side", 36).move_to([-4.4, 3.0, 0])
        iso = Iso(0.8, -1.9, 1.2)
        agent, alights = agent_slab(iso)
        alights[0].set_color(TERRA)
        key = key_obj(0.8, 0.95, s=0.6)
        alab = T("agent", 40).move_to([0.8, -3.0, 0])
        iso3 = Iso(4.5, -2.1, 0.75)
        rack, rlights = aicr_rack(iso3)
        rlab = T("AICR", 40).move_to([4.8, -3.0, 0])
        barrier = DashedLine([-1.5, -2.8, 0], [-1.5, 2.7, 0], color=BAR1, stroke_width=6, dash_length=0.3)
        arrow = Arrow([2.4, -1.0, 0], [3.4, -1.0, 0], color=INK, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.5)
        self.play(FadeIn(side), FadeIn(agent), FadeIn(alights), FadeIn(key), FadeIn(alab), FadeIn(rack), FadeIn(rlights), FadeIn(rlab), Create(barrier), Create(arrow), run_time=0.5)
        # "print, copy or upload": three pills wait on Claude's side
        items = [("cat", True, 1.9), ("scp", True, 0.6), ("chat", False, -0.7)]
        built = []
        for k, (name, mono, y) in enumerate(items):
            c = chip(name, -4.8, y, mono=mono, size=36)
            built.append((c, y))
        hear(self, "never print", lead=0.1)
        self.play(FadeIn(built[0][0]), run_time=0.2)
        hear(self, "copy", lead=0.2)
        self.play(FadeIn(built[1][0]), run_time=0.2)
        hear(self, "upload", lead=0.2)
        self.play(FadeIn(built[2][0]), run_time=0.2)
        marks = []
        for k, ((c, y), ph, ld) in enumerate(zip(built, ["not cat", "scp", "the chat"], [0.45, 0.45, 0.2])):
            hear(self, ph, lead=ld)
            self.play(c.animate.move_to([-2.5, y, 0]), run_time=0.35)
            xm = x_mark(-1.5, y, r=0.28, w=9)
            marks.append(xm)
            self.play(Create(xm), run_time=0.15)
            self.play(c.animate.move_to([-3.6, y, 0]), run_time=0.25)
        # "The agent does that": the agent's own arrow to AICR, the rack wakes
        hear(self, "the agent does that", lead=0.2)
        self.play(Indicate(arrow, color=TERRA, scale_factor=1.3), *[l.animate.set_color(TERRA) for l in rlights], run_time=0.7)
        done(self)


class B45_PassphraseStays(Scene):
    """Rule five: the passphrase dots are refused by a prompt, a file and a command; they go back to you, who unlock the key yourself."""
    def construct(self):
        you = professor_bear("1x1", 2.2, seed="B45", x=-5.0, y=1.0)
        term = RoundedRectangle(corner_radius=0.1, width=2.0, height=1.0, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-5.0, -1.2, 0])
        tmark = M("$", 40, color=GHOST).move_to([-5.45, -1.2, 0])
        tlab = T("terminal", 38).move_to([-5.0, -2.2, 0])
        key = key_obj(-3.3, -1.3, s=0.55)
        lock = padlock(-3.3, -1.3, s=0.8)
        # three targets
        prompt = VGroup(RoundedRectangle(corner_radius=0.12, width=2.0, height=0.9, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([2.2, 2.0, 0]),
                        Line([1.5, 2.0, 0], [2.3, 2.0, 0], color=GHOST, stroke_width=7))
        plab = T("prompt", 38).move_to([3.5, 2.0, 0], aligned_edge=LEFT)
        plab.move_to([3.6 + plab.width / 2, 2.0, 0])
        page = cert_page(2.2, 0.0, w=1.3, h=1.5)
        flab = T("file", 38)
        flab.move_to([3.6 + flab.width / 2, 0.0, 0])
        cmd = chip("", 2.2, -2.0, w=2.0)
        clab = T("command", 38)
        clab.move_to([3.6 + clab.width / 2, -2.0, 0])
        dots = chip("••••••", -2.2, 1.0, size=40)
        self.play(FadeIn(you), FadeIn(term), FadeIn(tmark), FadeIn(tlab), FadeIn(key), FadeIn(lock), FadeIn(dots), run_time=0.5)
        targets = [(prompt, plab, 2.0, "a prompt"), (page, flab, 0.0, "a file"), (cmd, clab, -2.0, "a command")]
        for (obj, lab, y, ph) in targets:
            hear(self, ph, lead=0.45)
            self.play(FadeIn(obj), FadeIn(lab), run_time=0.2)
            self.play(dots.animate.move_to([-0.3, y, 0]), run_time=0.4)
            self.play(Create(x_mark(0.85, y, r=0.28, w=9)), run_time=0.15)
        # "stop and unlock the key yourself": the dots return to you, the lock opens
        hear(self, "stop and unlock", lead=0.1)
        self.play(dots.animate.move_to([-3.3, 1.0, 0]), run_time=0.6, rate_func=smooth)
        hear(self, "yourself", lead=0.6)
        self.play(dots.animate.move_to([-3.3, -0.55, 0]), run_time=0.4)
        self.play(unlock_anim(lock, rt=0.5), FadeOut(dots), run_time=0.5)
        done(self)
