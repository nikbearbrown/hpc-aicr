# ═════════════════════════════ PART B — B11 B13 B14 B20 B31 B34 B37 ═════════════════════════════

def pB_slot(x, y, w=2.0, h=1.1, color=BAR1):
    """A dashed empty slot (outline only)."""
    try:
        return DashedVMobject(RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=6, fill_opacity=0).move_to([x, y, 0]),
                              num_dashes=28)
    except Exception:
        r = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=6, fill_opacity=0).move_to([x, y, 0])
        return r


def pB_brk(x0, x1, y, tick=0.16):
    b = VMobject(stroke_color=INK, stroke_width=5)
    b.set_points_as_corners([[x0, y + tick, 0], [x0, y, 0], [x1, y, 0], [x1, y + tick, 0]])
    return b


def pB_row(name, role, y, x0=-3.5, w=9.3):
    """A table row: white card (kraft shadow), real file name in mono, short role label on the right."""
    shadow = Rectangle(width=w, height=0.9, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x0 + w / 2 + 0.08, y - 0.08, 0])
    card = Rectangle(width=w, height=0.9, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x0 + w / 2, y, 0])
    f = M(name, 32)
    f.move_to([x0 + 0.3 + f.width / 2, y, 0])
    r = T(role, 36)
    r.move_to([x0 + w - 0.3 - r.width / 2, y, 0])
    g = VGroup(shadow, card, f, r)
    g.card = card
    return g


class B11_UserName(Scene):
    """Your AICR user name = campus name + institution; the pattern becomes <aicr-username>."""
    def construct(self):
        acct = chip("account", 0.0, 0.5, size=40)
        self.add(acct)
        # "A faculty member's proposal opens a project and your institution creates your user"
        hear(self, "faculty member's proposal", lead=0.5)
        c1 = chip("proposal", -4.0, 0.5, size=38)
        c2 = chip("project", 0.0, 0.5, size=38)
        c3 = chip("your user", 4.0, 0.5, size=38)
        a1 = Arrow([-2.7, 0.5, 0], [-1.4, 0.5, 0], buff=0, color=INK, stroke_width=6, max_tip_length_to_length_ratio=0.4)
        a2 = Arrow([1.3, 0.5, 0], [2.4, 0.5, 0], buff=0, color=INK, stroke_width=6, max_tip_length_to_length_ratio=0.4)
        self.play(FadeOut(acct), FadeIn(c1), run_time=0.3)
        hear(self, "opens a project", lead=0.4)
        self.play(Create(a1), FadeIn(c2), run_time=0.4)
        hear(self, "creates your user", lead=0.5)
        self.play(Create(a2), FadeIn(c3), run_time=0.4)
        # "Your AICR username is": the pattern replaces the flow
        hear(self, "Your AICR username", lead=1.0)
        pat = M("institutionalusername_institutioncode", 34)
        if pat.width > 11.4:
            pat.scale_to_fit_width(11.4)
        pat.move_to([0, 0.6, 0])
        bg = pill(0, 0.6, pat.width + 0.9, h=0.95)
        shadow = pill(0.08, 0.52, pat.width + 0.9, h=0.95, fill=BOX_L)
        pc = VGroup(shadow, bg)
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(c3), FadeOut(a1), FadeOut(a2), FadeIn(pc), FadeIn(pat), run_time=0.35)
        # "your campus name" / "the institution on the end": the two halves are bracketed and labelled
        L0 = pat.get_left()[0]
        split = L0 + pat.width * 21 / 37
        hear(self, "your campus name", lead=0.3)
        b1 = pB_brk(L0 + 0.05, split - 0.05, 0.0)
        l1 = T("campus name", 36).move_to([(L0 + split) / 2, -0.65, 0])
        self.play(Create(b1), FadeIn(l1), run_time=0.45)
        hear(self, "institution on the end", lead=0.3)
        R0 = pat.get_right()[0]
        b2 = pB_brk(split + 0.05, R0 - 0.05, 0.0)
        l2 = T("institution", 36).move_to([(split + R0) / 2 + 0.2, -0.65, 0])
        self.play(Create(b2), FadeIn(l2), run_time=0.45)
        # "like jsmith underscore neu": it becomes <aicr-username>
        hear(self, "like jsmith", lead=0.4)
        out = M("<aicr-username>", 80).move_to([0, 0.6, 0])
        bg2 = pill(0, 0.6, out.width + 0.9, h=0.95)
        sh2 = pill(0.08, 0.52, out.width + 0.9, h=0.95, fill=BOX_L)
        self.play(FadeOut(b1), FadeOut(b2), FadeOut(l1), FadeOut(l2), Transform(pat, out), Transform(bg, bg2), Transform(shadow, sh2), run_time=0.9)
        done(self)


class B13_FourFiles(Scene):
    """The aicr keys folder holds four files; the certificate is the credential."""
    def construct(self):
        fold = chip("AICR keys", -4.3, 2.5, size=38)
        self.add(fold)
        ys = [1.4, 0.35, -0.7, -1.75]
        r1 = pB_row("id_ed25519_aicr", "private key", ys[0])
        r2 = pB_row("id_ed25519_aicr.pub", "public key", ys[1])
        r3 = pB_row("id_ed25519_aicr-cert.pub", "certificate", ys[2])
        r4 = pB_row(".passphrase", "first passphrase", ys[3])
        key = key_obj(-6.0, ys[0], s=0.5)
        page = cert_page(-5.4, ys[2], w=0.95, h=1.1)
        hear(self, "your private key", lead=0.5)
        self.play(FadeIn(r1), FadeIn(key), run_time=0.4)
        hear(self, "its public half", lead=0.6)
        self.play(FadeIn(r2), run_time=0.35)
        hear(self, "your certificate", lead=0.5)
        self.play(FadeIn(r3), FadeIn(page), run_time=0.4)
        hear(self, "which is the credential", lead=0.4)
        ring = RoundedRectangle(corner_radius=0.25, width=9.7, height=1.2, stroke_color=TERRA, stroke_width=8, fill_opacity=0).move_to([-3.5 + 4.65 + 0.04, ys[2] - 0.04, 0])
        self.play(Create(ring), run_time=0.5)
        hear(self, "and a file holding", lead=0.3)
        self.play(FadeIn(r4), run_time=0.35)
        done(self)


class B14_HumanSteps(Scene):
    """Sign in, download, passphrase are yours (checks land); the password is turned away from Claude."""
    def construct(self):
        bear = professor_bear("1x1", 2.8, seed="B14", x=-5.0, y=0.2)
        door = Rectangle(width=1.8, height=2.8, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([4.7, -0.1, 0])
        knob = Dot([5.3, -0.1, 0], radius=0.12, color=INK)
        claude = logo_chip("claude", 4.7, 2.3)
        self.add(bear, door, knob, claude)
        ys = [1.5, 0.4, -0.7]
        names = ["Sign in", "Download", "Passphrase"]
        cues = ["Signing in", "putting the files", "choosing a new"]
        leads = [-0.1, 0.35, 0.3]
        for nme, cue, y, ld in zip(names, cues, ys, leads):
            hear(self, cue, lead=ld)
            c = chip(nme, -1.6, y, size=38)
            self.play(FadeIn(c), run_time=0.25)
            ck = check(0.1, y, s=0.22, color=TERRA, w=9)
            self.play(Create(ck), run_time=0.25)
        # "Do not give Claude your institutional password": the password heads for the door and is turned away
        hear(self, "give Claude", lead=0.5)
        pw = chip("password", 1.4, -1.9, size=36)
        self.play(FadeIn(pw), run_time=0.25)
        hear(self, "institutional password", lead=0.2)
        self.play(pw.animate.move_to([1.9, -1.9, 0]), run_time=0.6)
        nope = x_mark(3.45, -1.9, r=0.3, w=9)
        self.play(Create(nope), run_time=0.3)
        hear(self, "ask it to sign in", lead=0.3)
        self.play(pw.animate.move_to([0.8, -1.9, 0]), run_time=0.5)
        done(self)


class B20_NobodyAnswers(Scene):
    """ssh meets the passphrase-locked key; nobody can answer; the command waits."""
    def construct(self):
        title = act_title("II · Unlock Once")
        key = key_obj(0.4, 0.3, s=1.1)
        lock = padlock(2.5, 0.3, s=1.4)
        iso = Iso(-5.4, -2.2, 0.9)
        box = job_box(iso, 0, 0, 0, s=0.9)
        box.move_to([-5.4, -0.5, 0])
        lab = M("ssh", 38).move_to([-5.4, -1.6, 0])
        self.play(FadeIn(title), FadeIn(key), FadeIn(lock), FadeIn(box), FadeIn(lab), run_time=0.5)
        # "Claude Code runs commands with no keyboard attached": the ssh box rides to the locked key
        hear(self, "runs commands", lead=0.3)
        self.play(box.animate.shift(RIGHT * 4.2), lab.animate.shift(RIGHT * 4.2), run_time=1.1, rate_func=smooth)
        # "ask for the passphrase": the lock raises the chip
        hear(self, "ask for the", lead=0.2)
        q = chip("passphrase?", 2.7, 1.9, size=38)
        self.play(FadeIn(q), run_time=0.2)
        self.play(q.animate.shift(UP * 0.4), run_time=0.4)
        # "nobody can answer": an empty answer slot appears beside the box
        hear(self, "nobody can answer", lead=0.35)
        slot = pB_slot(-3.0, -0.5)
        self.play(Create(slot), run_time=0.5)
        # "hangs or fails": the box waits, dimmed
        hear(self, "hangs", lead=0.3)
        self.play(box.animate.set_opacity(0.4), lab.animate.set_opacity(0.4), run_time=0.5)
        done(self)


class B31_FailFast(Scene):
    """Without BatchMode the box waits at the lock; with it the box bounces at once; unlocked, it passes."""
    def construct(self):
        ys = [1.3, -1.7]
        keys, locks, boxes, labs = [], [], [], []
        for y in ys:
            keys.append(key_obj(2.6, y, s=0.6))
            locks.append(padlock(3.5, y, s=0.9))
            iso = Iso(-4.4, y - 1.2, 0.8)
            b = job_box(iso, 0, 0, 0, s=0.7)
            b.move_to([-4.4, y - 0.1, 0])
            boxes.append(b)
            labs.append(M("ssh", 34).move_to([-4.4, y - 0.95, 0]))
        self.add(*keys, *locks)
        self.play(*[FadeIn(b) for b in boxes], *[FadeIn(l) for l in labs], run_time=0.4)
        # "test it the way Claude connects": the top box rides to the lock and waits
        hear(self, "way Claude connects", lead=0.3)
        self.play(boxes[0].animate.shift(RIGHT * 5.5), labs[0].animate.shift(RIGHT * 5.5), run_time=1.0, rate_func=smooth)
        waits = T("waits", 36).move_to([1.1, ys[0] + 1.05, 0])
        self.play(FadeIn(waits), run_time=0.25)
        # "with batch mode on": the lower lane is labelled
        hear(self, "mode on", lead=0.5)
        bm = chip("BatchMode", -4.4, ys[1] + 1.2, mono=True, size=34)
        self.play(FadeIn(bm), run_time=0.3)
        # "Batch mode makes ssh fail at once": the box meets the lock and bounces back with a cross
        hear(self, "Batch mode makes", lead=0.3)
        self.play(boxes[1].animate.shift(RIGHT * 5.5), labs[1].animate.shift(RIGHT * 5.5), run_time=0.8, rate_func=smooth)
        no = x_mark(0.95, ys[1] + 0.8, r=0.3, w=9)
        hear(self, "fail at", lead=0.0)
        self.play(Create(no), boxes[1].animate.shift(LEFT * 3.0), labs[1].animate.shift(LEFT * 3.0), run_time=0.5)
        # "If it prints your username": the lock opens and the box passes through
        hear(self, "If it prints", lead=0.5)
        self.play(FadeOut(no), unlock_anim(locks[1]), run_time=0.5)
        boxes[1].set_z_index(5); labs[1].set_z_index(5)
        self.play(boxes[1].animate.shift(RIGHT * 7.6), labs[1].animate.shift(RIGHT * 7.6), run_time=1.1, rate_func=smooth)
        # "Claude can log in": the check lands
        hear(self, "Claude can log in", lead=0.3)
        ok = check(5.5, ys[1] + 1.15, s=0.3, color=TERRA, w=10)
        self.play(Create(ok), run_time=0.4)
        done(self)


class B34_EmptyOnPurpose(Scene):
    """Reboot dial sweeps; the agent forgets (key leaves, light goes dark); the box waits before the empty agent."""
    def construct(self):
        iso = Iso(0.2, -1.9, 1.2)
        agent, alights = agent_slab(iso)
        alights[0].set_color(TERRA)
        key = key_obj(0, 0, s=0.6).move_to([0.2, 0.95, 0])
        alab = T("agent", 40).move_to([0.2, -3.0, 0])
        self.play(FadeIn(agent), FadeIn(alights), FadeIn(key), FadeIn(alab), run_time=0.4)
        # "when you reboot": a dial sweeps
        hear(self, "when you reboot", lead=0.3)
        dial = Circle(radius=0.85, stroke_color=INK, stroke_width=6, fill_color=PAGE_TOP, fill_opacity=1).move_to([-4.6, 0.9, 0])
        hand = Line([-4.6, 0.9, 0], [-4.6, 1.65, 0], color=INK, stroke_width=8)
        hub = Dot([-4.6, 0.9, 0], radius=0.1, color=INK)
        rl = T("reboot", 38).move_to([-4.6, -0.5, 0])
        self.play(FadeIn(dial), FadeIn(hub), FadeIn(rl), FadeIn(hand), run_time=0.3)
        self.play(Rotate(hand, angle=-2 * PI, about_point=[-4.6, 0.9, 0]), run_time=1.1, rate_func=smooth)
        # "the agent forgets everything": the key is pulled out and the light goes dark
        hear(self, "forgets everything", lead=0.6)
        self.play(key.animate.shift(UP * 1.5), alights[0].animate.set_color(GHOST), run_time=0.6)
        self.play(FadeOut(key), run_time=0.2)
        slot = pB_slot(0.2, 0.95, w=1.9, h=0.8)
        self.play(Create(slot), run_time=0.4)
        # "empty it on purpose": the ssh box arrives before the empty agent
        hear(self, "empty it", lead=0.2)
        iso2 = Iso(4.6, -2.0, 0.9)
        box = job_box(iso2, 0, 0, 0, s=0.9)
        box.move_to([4.6, -0.8, 0])
        blab = M("ssh", 38).move_to([4.6, -1.9, 0])
        self.play(FadeIn(box), FadeIn(blab), run_time=0.3)
        hear(self, "get in", lead=1.2)
        self.play(box.animate.shift(LEFT * 1.2), blab.animate.shift(LEFT * 1.2), run_time=0.7, rate_func=smooth)
        done(self)


class B37_VaultRefills(Scene):
    """macOS Keychain gives the key back to the agent; the box passes on; the key never crosses Claude's side."""
    def construct(self):
        iso = Iso(-1.7, -1.9, 1.1)
        agent, alights = agent_slab(iso)
        alab = T("agent", 40).move_to([-1.7, -3.0, 0])
        iso_v = Iso(2.0, -1.9, 1.1)
        vlt = vault(iso_v)
        vlab = T("Keychain", 40).move_to([2.4, -3.0, 0])
        iso_r = Iso(4.3, -2.0, 0.7)
        rack, rlights = aicr_rack(iso_r)
        rlab = T("AICR", 38).move_to([4.6, -3.05, 0])
        iso_b = Iso(-5.2, -2.2, 0.9)
        box = job_box(iso_b, 0, 0, 0, s=0.9)
        box.move_to([-5.2, -0.9, 0])
        blab = M("ssh", 38).move_to([-5.2, -1.95, 0])
        bar = DashedLine([-3.3, -2.8, 0], [-3.3, 3.0, 0], color=BAR1, stroke_width=6, dash_length=0.3)
        side = T("Claude's side", 36).move_to([-4.6, 3.0, 0])
        self.play(FadeIn(agent), FadeIn(alights), FadeIn(alab), FadeIn(vlt), FadeIn(vlab), FadeIn(rack), FadeIn(rlights), FadeIn(rlab),
                  FadeIn(box), FadeIn(blab), Create(bar), FadeIn(side), run_time=0.5)
        # "Add keys to agent asks it": the box asks the empty agent
        hear(self, "Add keys to agent", lead=0.2)
        q = chip("key?", -3.6, 1.3, size=36)
        self.play(FadeIn(q), run_time=0.2)
        self.play(q.animate.move_to([-1.4, 1.3, 0]), run_time=0.6)
        # "for the passphrase": the question goes on to the vault
        hear(self, "for the passphrase", lead=0.5)
        self.play(q.animate.move_to([2.4, 1.3, 0]), run_time=0.6)
        # the vault door opens, a key rises out
        self.play(FadeOut(q), FadeOut(vlt[1]), FadeOut(vlt[2]), run_time=0.35)
        key = key_obj(0, 0, s=0.6).move_to([2.3, 0.2, 0])
        self.play(GrowFromCenter(key), run_time=0.3)
        # "the key goes back into the agent": the key flies in, the light turns terracotta
        hear(self, "goes back into", lead=0.6)
        self.play(key.animate.move_to([2.3, 1.5, 0]), run_time=0.3)
        self.play(key.animate.move_to([-1.7, 1.0, 0]), run_time=0.9, rate_func=smooth)
        self.play(alights[0].animate.set_color(TERRA), Indicate(agent, color=INK, scale_factor=1.04), run_time=0.5)
        # "nothing passed to Claude": the box passes on toward the right; nothing crosses the barrier
        hear(self, "Nothing was typed", lead=0.3)
        self.play(box.animate.shift(UP * 2.6), blab.animate.shift(UP * 2.6), run_time=0.35)
        self.play(box.animate.shift(RIGHT * 9.3), blab.animate.shift(RIGHT * 9.3), run_time=1.0, rate_func=smooth)
        self.play(FadeOut(blab), box.animate.shift(DOWN * 1.3), run_time=0.3)
        done(self)
