# ═════════════════════════════ PART D — rules 6-7 and Act V (B46 B47 B50 B51 B53 B54) ═════════════════════════════

def pD_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


class B46_OwnAccount(Scene):
    """The certificate names you; it is not for anyone else: a second slot refuses it."""
    def construct(self):
        me = professor_bear("1x1", 2.6, seed="B46y", x=-4.2, y=0.3)
        melab = T("you", 38).move_to([-4.2, -2.1, 0])
        cert = cert_page(-0.4, 0.3, w=1.9, h=2.4)
        cert[2][0].set_color(BAR1).set_stroke(width=10)   # the name line
        clab = T("certificate", 36).move_to([-0.4, -1.65, 0])
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=2.6, height=2.6, color=BAR1, stroke_width=6), num_dashes=28)
        slot.move_to([4.2, 0.3, 0])
        slab = T("someone else", 36).move_to([4.2, -1.75, 0])
        self.play(FadeIn(me), FadeIn(melab), FadeIn(cert), FadeIn(clab), FadeIn(slot), FadeIn(slab), run_time=0.5)
        # "the certificate names you": a leader line ties the certificate to the one portrait
        hear(self, "names you", lead=0.45)
        leader = Line([-1.42, 0.3, 0], [-2.85, 0.3, 0], color=INK, stroke_width=6)
        self.play(Create(leader), run_time=0.4)
        # "run work for anyone else": the certificate tries the other slot and is refused
        hear(self, "run work for", lead=0.1)
        self.play(FadeOut(clab), cert.animate.shift(RIGHT * 2.7), run_time=0.5, rate_func=smooth)
        no = x_mark(4.2, 0.3, r=0.3, w=9)
        self.play(Create(no), run_time=0.25)
        self.play(cert.animate.shift(LEFT * 2.7), run_time=0.5, rate_func=smooth)
        self.play(FadeIn(clab), FadeOut(no), run_time=0.25)
        done(self)


class B47_HomeScratch(Scene):
    """Home is small and recoverable; scratch is large and purged; check the file system page before moving data."""
    def construct(self):
        iso1 = Iso(-4.0, -1.7, 1.3)
        home = home_box(iso1)
        hlab = T("home", 40).move_to([-4.0, -2.7, 0])
        iso2 = Iso(1.6, -2.0, 1.0)
        back, front = scratch_bin(iso2)
        slab = T("scratch", 40).move_to([2.0, -2.8, 0])
        self.play(FadeIn(home), FadeIn(hlab), FadeIn(back), FadeIn(front), FadeIn(slab), run_time=0.5)
        # "Home is small and recoverable": a restore arrow circles back
        hear(self, "is small", lead=0.2)
        self.play(home.animate.scale(1.08), run_time=0.25)
        self.play(home.animate.scale(1 / 1.08), run_time=0.25)
        hear(self, "and recoverable", lead=0.4)
        arc = Arc(radius=0.5, start_angle=PI * 0.35, angle=PI * 1.5, color=INK, stroke_width=8).move_to([-4.0, 1.95, 0])
        arc.add_tip(tip_length=0.28)
        rec = T("recoverable", 36).move_to([-4.0, 2.95, 0])
        self.play(Create(arc), run_time=0.5)
        self.play(FadeIn(rec), run_time=0.25)
        # "Scratch is large": the bin fills with blocks
        hear(self, "is large", lead=0.35)
        blocks = VGroup(*[iso2.box(x, y, 0.0, 0.6, 0.6, 0.5, PAGE_TOP, PAGE_L, PAGE_R) for y in (0.25, 0.95) for x in (0.35, 1.15, 1.95)])
        blocks.set_z_index(1)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.9) for b in blocks], lag_ratio=0.15), run_time=0.6)
        # "it is purged": a sweep clears the bin
        hear(self, "it is purged", lead=0.15)
        sweep = Rectangle(width=0.3, height=2.5, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0.5, -0.3, 0])
        sweep.set_z_index(3)
        self.play(FadeIn(sweep), run_time=0.15)
        self.play(sweep.animate.shift(RIGHT * 3.4), LaggedStart(*[FadeOut(b) for b in blocks], lag_ratio=0.12), run_time=0.8)
        pur = T("purged", 36).move_to([2.0, 1.95, 0])
        self.play(FadeOut(sweep), FadeIn(pur), run_time=0.3)
        # "Check ... file system page before you move data": a 'check first' tag lands on the move arrow
        hear(self, "Check AICR's", lead=0.1)
        mv = Arrow([-2.3, -0.4, 0], [-0.3, -0.4, 0], buff=0, color=INK, stroke_width=8, max_tip_length_to_length_ratio=0.3)
        self.play(Create(mv), run_time=0.4)
        hear(self, "file system", lead=0.4)
        tag = chip("check first", -1.3, 0.55, size=36)
        self.play(FadeIn(tag, shift=DOWN * 0.5), run_time=0.4)
        hear(self, "move data", lead=0.1)
        self.play(Indicate(mv, color=INK, scale_factor=1.15), run_time=0.5)
        done(self)


class B50_ThreeCauses(Scene):
    """Permission denied (publickey): one error, three usual causes; the unlocked-key cause is by far the biggest."""
    def construct(self):
        title = pD_act_title("V · When It Fails")
        err = plaque("Permission denied (publickey)", 0.0, 1.9, w=9.4, h=1.0, size=34)
        self.play(FadeIn(title), FadeIn(err), run_time=0.5)
        hear(self, "permission denied", lead=0.2)
        self.play(err.animate.scale(1.04), run_time=0.25)
        self.play(err.animate.scale(1 / 1.04), run_time=0.25)
        # "one of three things": three dots under the error
        hear(self, "one of three", lead=0.3)
        dots = VGroup(*[Dot([x, 1.0, 0], radius=0.12, color=TERRA) for x in (-0.5, 0.0, 0.5)])
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.2), run_time=0.6)

        def card(lines, x, y, w, h, size):
            sh = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
            cd = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
            lb = T(lines, size).move_to([x, y, 0])
            return VGroup(sh, cd, lb)

        def fan(g):
            g.save_state()
            g.scale(0.25).move_to([0.0, 1.0, 0])
            self.add(g)
            return Restore(g)

        # the three causes land on their spoken words
        cardA = card("Key not unlocked", -3.7, -0.6, 4.2, 2.4, 40)
        hear(self, "key is not", lead=0.25)
        self.play(fan(cardA), FadeOut(dots), run_time=0.6, rate_func=smooth)
        hear(self, "by far the most", lead=0.1)
        most = T("most common", 36).move_to([-3.7, -2.35, 0])
        self.play(FadeIn(most), run_time=0.3)
        cardB = card("Certificate\nexpired or missing", 0.75, -0.35, 3.7, 1.9, 34)
        hear(self, "or the certificate", lead=0.3)
        self.play(fan(cardB), run_time=0.6, rate_func=smooth)
        cardC = card("Wrong\npermissions", 4.45, -0.35, 3.0, 1.9, 34)
        hear(self, "key's permissions", lead=0.5)
        self.play(fan(cardC), run_time=0.6, rate_func=smooth)
        done(self)


class B51_TwinErrors(Scene):
    """Two identical errors, two different causes: ssh-add -l lifts the curtain on the empty agent."""
    def construct(self):
        errs = []
        for x in (-3.2, 3.2):
            errs.append(plaque("Permission denied\n(publickey)", x, 2.45, w=5.2, h=1.5, size=32))
        iso = Iso(-3.0, -1.85, 0.9)
        agent, alights = agent_slab(iso)
        cert = cert_page(3.0, -0.7, w=1.7, h=2.1)
        curts, qs = [], []
        for x in (-3.0, 3.0):
            c = Rectangle(width=3.8, height=2.5, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, -0.7, 0])
            curts.append(c)
            qs.append(T("?", 64).move_to([x, -0.7, 0]))
        curts[0].set_z_index(3); curts[1].set_z_index(3)
        for q in qs:
            q.set_z_index(4)
        self.play(FadeIn(errs[0]), FadeIn(errs[1]), FadeIn(agent), FadeIn(alights), FadeIn(cert),
                  FadeIn(curts[0]), FadeIn(curts[1]), FadeIn(qs[0]), FadeIn(qs[1]), run_time=0.5)
        hear(self, "empty agent", lead=0.2)
        self.play(curts[0].animate.scale(1.05), run_time=0.25)
        self.play(curts[0].animate.scale(1 / 1.05), run_time=0.25)
        hear(self, "expired certificate", lead=0.2)
        self.play(curts[1].animate.scale(1.05), run_time=0.25)
        self.play(curts[1].animate.scale(1 / 1.05), run_time=0.25)
        # "The error is the same": an equals sign between the two
        hear(self, "error is the same", lead=0.5)
        eq = T("=", 64).move_to([0.0, 2.45, 0])
        self.play(FadeIn(eq), run_time=0.3)
        # "check the agent with ssh-add -l": the command chip sweeps across and lifts the left curtain
        hear(self, "with SSH", lead=0.4)
        cmd = chip("ssh-add -l", 4.6, 1.0, mono=True, size=36)
        self.play(FadeIn(cmd), run_time=0.25)
        self.play(cmd.animate.move_to([-3.0, 1.0, 0]), run_time=1.1, rate_func=smooth)
        self.play(FadeOut(qs[0]), curts[0].animate.stretch_to_fit_height(0.06).move_to([-3.0, 0.55, 0]), run_time=0.5)
        tag = chip("agent empty", -3.0, -2.8, size=36)
        self.play(FadeIn(tag, shift=DOWN * 0.4), run_time=0.4)
        done(self)


# ── the shared two-column table (B53 = rows 1-3, B54 = the same table, rows 1-4) ──
pD_COLX, pD_RX = -5.8, -1.1


def pD_y(i):
    return 1.5 - 1.35 * i


def pD_head():
    a = T("You see", 38, bold=True)
    a.move_to([0, 2.95, 0]).align_to([pD_COLX, 0, 0], LEFT)
    b = T("Fix", 38, bold=True)
    b.move_to([0, 2.95, 0]).align_to([pD_RX, 0, 0], LEFT)
    rule = Line([-6.1, 2.5, 0], [6.1, 2.5, 0], color=INK, stroke_width=5)
    return VGroup(a, b, rule)


def pD_left(text, i):
    t = T(text, 34)
    t.move_to([0, pD_y(i), 0]).align_to([pD_COLX, 0, 0], LEFT)
    return t


def pD_rights(items, i):
    out = []
    n = len(items)
    for k, (txt, mono) in enumerate(items):
        t = M(txt, 32) if mono else T(txt, 34)
        dy = 0.0 if n == 1 else (0.3 if k == 0 else -0.3)
        t.move_to([0, pD_y(i) + dy, 0]).align_to([pD_RX, 0, 0], LEFT)
        out.append(t)
    return out


def pD_ring(i):
    """The row marker: a short thick ink bar at the left of the row being spoken (an outline round the row fused the
    whole row into one GATE T text blob; a fill dragged Gate V's contrast under 0.3)."""
    return Rectangle(width=0.14, height=1.0, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([-6.05, pD_y(i), 0])


def pD_table(self, rows):
    """rows = [(index, left text, left cue, [(right text, mono, cue, lead), ...]), ...]; rings the row being spoken."""
    head = pD_head()
    self.play(FadeIn(head), run_time=0.4)
    ring = None
    for i, ltxt, lcue, rights in rows:
        hear(self, lcue, lead=0.3)
        left = pD_left(ltxt, i)
        if ring is None:
            ring = pD_ring(i)
            self.play(Create(ring), FadeIn(left), run_time=0.35)
        else:
            self.play(ring.animate.move_to([-6.05, pD_y(i), 0]), FadeIn(left), run_time=0.35)
        ys = pD_rights([(r[0], r[1]) for r in rights], i)
        arr = Arrow([-1.7, pD_y(i), 0], [-1.35, pD_y(i), 0], buff=0, color=INK, stroke_width=6, max_tip_length_to_length_ratio=0.6)
        for (rtxt, mono, cue, lead), mob in zip(rights, ys):
            hear(self, cue, lead=lead)
            self.play(FadeIn(mob, shift=RIGHT * 0.2), *([FadeIn(arr)] if mob is ys[0] else []), run_time=0.3)


class B53_TableA(Scene):
    """The fix table, part one: hang, changed host key, new host key prompt."""
    def construct(self):
        pD_table(self, [
            (0, "Hangs, wants\npassphrase", "A command that hangs", [("Unlock the key yourself", False, "unlock the key", 0.3)]),
            (1, "Host key verification\nfailed", "Host key verification", [("ssh-keygen -R login.aicr.ai,", True, "Remove the old entry", 0.25), ("connect once", False, "then connect once", 0.25)]),
            (2, "New host key prompt", "A new host key", [("Type yes yourself", False, "type yes", 0.25)]),
        ])
        done(self)


class B54_TableB(Scene):
    """The fix table, part two: bad option, timeout, idle drops, empty agent after restart."""
    def construct(self):
        pD_table(self, [
            (0, "Bad configuration\noption", "Bad configuration option", [("IgnoreUnknown UseKeychain", True, "add ignore unknown", 0.25)]),
            (1, "Connection\ntimed out", "Connection timed out", [("Other network, no VPN needed", False, "try another network", 0.25)]),
            (2, "Drops when idle", "Drops when idle", [("ServerAliveInterval 60", True, "server alive interval", 0.3)]),
            (3, "Empty after restart", "Empty after a restart", [("ssh-add again", True, "SSH add again", 0.25)]),
        ])
        done(self)
