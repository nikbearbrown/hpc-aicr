# ═════════════════════════════ PART E — B80 B81 B90 B91 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pE_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pE_chip_left(text, xl, y, mono=False, size=34):
    """A chip whose LEFT edge sits at xl (table columns line up on the left)."""
    lab = M(text, size - 2) if mono else T(text, size)
    w = lab.width + 0.8
    return chip(text, xl + w / 2, y, w=w, mono=mono, size=size)


def pE_chip_mixed(parts, xl, y):
    """A chip holding a serif word and a mono address side by side, left edge at xl. `.pill`."""
    grp = VGroup(*parts).arrange(RIGHT, buff=0.16)
    w = grp.width + 0.8
    cx = xl + w / 2
    shadow = pill(cx + 0.08, y - 0.08, w, h=0.8, fill=BOX_L)
    body = pill(cx, y, w, h=0.8)
    grp.move_to([cx, y, 0])
    g = VGroup(shadow, body, grp)
    g.pill = body
    return g


def pE_ring(g, pad=0.14):
    """A terracotta ring round a chip (the ring pulse that marks the cause)."""
    p = g.pill
    hh = 0.8 + 2 * pad
    return RoundedRectangle(width=p.width + 2 * pad, height=hh, corner_radius=hh / 2, stroke_color=TERRA,
                            stroke_width=6, fill_opacity=0).move_to(p.get_center())


class B80_FourFailures(Scene):
    """A two-column table builds row by row: symptom chip left, cause chip right, each cause ringed in terracotta."""
    def construct(self):
        title = pE_act_title("VIII · When It Breaks")
        ys = [1.15, 0.0, -1.15, -2.3]
        xl, xr = -6.0, 0.95
        h1 = T("symptom", 34)
        h1.move_to([xl + h1.width / 2, 2.1, 0])
        h2 = T("cause", 34)
        h2.move_to([xr + h2.width / 2, 2.15, 0])
        top = Line([-6.1, 1.75, 0], [6.1, 1.75, 0], color=BAR2, stroke_width=4)
        div = DashedLine([0.05, 2.5, 0], [0.05, -2.85, 0], color=BAR2, stroke_width=4, dash_length=0.2)
        rules = [Line([-6.1, y - 0.575, 0], [6.1, y - 0.575, 0], color=BAR2, stroke_width=4) for y in ys]
        sym = [pE_chip_left("404 every request", xl, ys[0]),
               Group(logo_chip("claude", xl + 0.54, ys[1], h=0.8), pE_chip_left("model not found", xl + 1.3, ys[1])),
               pE_chip_left("raw tool calls", xl, ys[2]),
               pE_chip_left("CPU/GPU split", xl, ys[3])]
        cau = [pE_chip_mixed([T("base URL ends", 34), M("/v1", 34)], xr, ys[0]),
               pE_chip_left("aliases not mapped", xr, ys[1]),
               pE_chip_left("no tools label", xr, ys[2]),
               pE_chip_left("model/window too big", xr, ys[3])]
        arrs = [Arrow([-0.55, y, 0], [0.5, y, 0], buff=0, color=INK, stroke_width=7, max_tip_length_to_length_ratio=0.5) for y in ys]
        rings = [pE_ring(c) for c in cau]

        self.play(FadeIn(title), FadeIn(h1), FadeIn(h2), Create(top), Create(div), run_time=0.5)
        # row 1: 404 on every request -> the base address ends in /v1
        hear(self, "404 on", lead=0.2)
        self.play(FadeIn(sym[0]), Create(rules[0]), run_time=0.3)
        hear(self, "the base address", lead=0.2)
        self.play(Create(arrs[0]), FadeIn(cau[0]), run_time=0.35)
        hear(self, "slash V1", lead=0.3)
        self.play(Create(rings[0]), run_time=0.35)
        self.wait(0.25)
        self.play(FadeOut(rings[0]), run_time=0.25)
        # row 2: a Claude model name not found -> the aliases are not mapped
        hear(self, "Claude model name", lead=0.2)
        self.play(FadeIn(sym[1]), Create(rules[1]), run_time=0.3)
        hear(self, "the aliases", lead=0.2)
        self.play(Create(arrs[1]), FadeIn(cau[1]), run_time=0.3)
        at(self, 9.05)        # after the clip midpoint: a ring alive at the midpoint is read as accent text by GATE T
        self.play(Create(rings[1]), run_time=0.3)
        self.wait(0.25)
        self.play(FadeOut(rings[1]), run_time=0.25)
        # row 3: tool calls printed as raw text -> the model has no tools label
        hear(self, "tool calls printed", lead=0.15)
        self.play(FadeIn(sym[2]), Create(rules[2]), run_time=0.3)
        hear(self, "the model has", lead=0.15)
        self.play(Create(arrs[2]), FadeIn(cau[2]), run_time=0.3)
        hear(self, "tools label", lead=0.25)
        self.play(Create(rings[2]), run_time=0.35)
        self.wait(0.25)
        self.play(FadeOut(rings[2]), run_time=0.25)
        # row 4: a split between processor and GPU -> the model or the window is too big
        hear(self, "a split between", lead=0.15)
        self.play(FadeIn(sym[3]), Create(rules[3]), run_time=0.3)
        hear(self, "model or the window", lead=0.3)
        self.play(Create(arrs[3]), FadeIn(cau[3]), run_time=0.3)
        hear(self, "too big", lead=0.3)
        self.play(Create(rings[3]), run_time=0.35)
        done(self)


def pE_globe(x, y, r=0.7):
    """A plain globe for 'the internet': white disc, ink outline, a meridian and two parallels."""
    disc = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    mer = Ellipse(width=r * 0.9, height=2 * r, stroke_color=INK, stroke_width=3, fill_opacity=0).move_to([x, y, 0])
    eq = Line([x - r, y, 0], [x + r, y, 0], color=INK, stroke_width=3)
    p1 = Line([x - r * 0.86, y + r * 0.5, 0], [x + r * 0.86, y + r * 0.5, 0], color=INK, stroke_width=3)
    p2 = Line([x - r * 0.86, y - r * 0.5, 0], [x + r * 0.86, y - r * 0.5, 0], color=INK, stroke_width=3)
    return VGroup(disc, mer, eq, p1, p2)


def pE_pipe(x0, x1, y, h=0.26):
    return Rectangle(width=x1 - x0, height=h, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([(x0 + x1) / 2, y, 0])


class B81_ProxyAndModulePurge(Scene):
    """Home fills up; a pull stalls on a compute node with no way out; the 'explorer' module sets the proxy gate and the
    pipe opens; 'module purge' sweeps the chip off and the pipe breaks; 'module load explorer' puts it back."""
    def construct(self):
        py = -1.5                      # the pipe's height
        # home box with a gauge (top right)
        hbox = home_box(Iso(4.55, 0.95, 0.8))
        hlab = T("home", 36).move_to([4.55, 0.5, 0])
        gx0, gw, gy = 0.9, 2.6, 1.4
        track = Rectangle(width=gw, height=0.45, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([gx0 + gw / 2, gy, 0])
        outl = Rectangle(width=gw, height=0.45, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([gx0 + gw / 2, gy, 0])
        outl.set_z_index(6)
        g1 = Rectangle(width=gw / 2, height=0.45, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([gx0 + gw / 4, gy, 0])
        g2 = Rectangle(width=gw / 2, height=0.45, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([gx0 + 3 * gw / 4, gy, 0])
        full = T("full", 36).move_to([gx0 + gw / 2, 1.95, 0])
        c1 = chip("image cache", 0.4, 2.65, size=34)
        c2 = chip("models", 0.4, 2.65, size=34)
        # compute node, pipe, gate, internet
        rack = VGroup(*explorer_rack(Iso(-4.9, -2.3, 0.75)))
        rlab = T("compute node", 34).move_to([-4.9, -2.85, 0])
        globe = pE_globe(4.75, py, 0.7)
        glab = T("internet", 34).move_to([4.75, -2.55, 0])
        pipeL = pE_pipe(-4.05, -1.7, py)
        pipeR = pE_pipe(1.7, 4.05, py)
        pipeM = pE_pipe(-1.7, 1.7, py)
        pipeM.set_z_index(0)
        posts = VGroup(*[Rectangle(width=0.26, height=1.4, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, -0.95, 0]) for x in (-0.75, 0.75)])
        bar = Rectangle(width=1.76, height=0.28, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0, -0.25, 0])
        gate = VGroup(posts, bar)
        gate.set_z_index(3)
        proxy = T("proxy", 36).move_to([2.2, -0.55, 0])
        mod = chip("explorer", 0.0, 0.42, mono=True, size=34)
        mod.set_z_index(4)
        # the pull: a small box labelled with the real subcommand
        pbox = job_box(Iso(0, 0, 0.5), 0, 0, 0, s=0.7).move_to([-3.2, -0.97, 0])
        plab = M("pull", 32).move_to([-3.2, -1.97, 0])
        pull = VGroup(pbox, plab)
        xm = x_mark(0, py, r=0.35, w=9)
        stamp = chip("Research Computing's pages", -2.9, 2.7, size=34)
        plq1 = plaque("module purge", -4.1, 1.55, w=3.8, h=0.9, size=32)
        plq2 = plaque("module load explorer", -2.85, 1.55, w=6.3, h=0.9, size=32)
        ok = check(0, py + 0.02, s=0.3, color=TERRA, w=12)

        # home is full: the cache and the models were sent to home
        hear(self, "a full home", lead=0.15)
        self.play(FadeIn(hbox), FadeIn(hlab), FadeIn(track), FadeIn(outl), run_time=0.4)
        hear(self, "the image cache", lead=0.15)
        self.play(FadeIn(c1), run_time=0.2)
        self.play(c1.animate.move_to([4.5, 2.0, 0]).scale(0.4), GrowFromEdge(g1, LEFT), run_time=0.55)
        self.play(FadeOut(c1), run_time=0.1)
        hear(self, "the models", lead=0.15)
        self.play(FadeIn(c2), run_time=0.2)
        self.play(c2.animate.move_to([4.5, 2.0, 0]).scale(0.4), GrowFromEdge(g2, LEFT), run_time=0.55)
        self.play(FadeOut(c2), run_time=0.1)
        hear(self, "defaulted to home", lead=0.1)
        self.play(FadeIn(full), run_time=0.3)
        # a pull on a compute node
        hear(self, "A pull that", lead=0.2)
        self.play(FadeIn(rack), FadeIn(pipeL), FadeIn(pull), run_time=0.4)
        hear(self, "that fails", lead=0.1)
        self.play(pull.animate.shift(RIGHT * 1.3), run_time=0.6)
        hear(self, "compute node", lead=0.15)
        self.play(FadeIn(rlab), run_time=0.3)
        hear(self, "no outbound", lead=0.25)
        self.play(FadeIn(globe), FadeIn(glab), FadeIn(pipeR), run_time=0.3)
        self.play(FadeIn(xm), run_time=0.2)
        # the proxy gate opens the way
        hear(self, "On Explorer", lead=0.1)
        self.play(FadeIn(gate), FadeOut(xm), FadeIn(pipeM), run_time=0.5)
        hear(self, "a default module", lead=0.0)
        self.play(FadeIn(mod, shift=DOWN * 0.45), run_time=0.35, rate_func=smooth)
        hear(self, "sets the proxy", lead=0.0)
        self.play(pull.animate.shift(RIGHT * 2.6), run_time=0.5)
        hear(self, "proxy", lead=0.1)
        self.play(FadeIn(proxy), pull.animate.shift(RIGHT * 2.8), run_time=0.6)
        hear(self, "that nodes use", lead=0.2)
        self.play(FadeIn(stamp), run_time=0.3)
        # module purge sweeps the chip off; the pipe breaks
        hear(self, "module purge", lead=0.25)
        self.play(FadeIn(plq1), run_time=0.3)
        hear(self, "it loses", lead=0.2)
        self.play(mod.animate.shift(LEFT * 3.7), FadeOut(pipeM), FadeIn(xm), run_time=0.6)
        # load it again: the chip returns and the pipe reconnects
        hear(self, "load the module", lead=0.2)
        self.play(FadeOut(plq1), FadeIn(plq2), run_time=0.3)
        hear(self, "again right", lead=0.2)
        self.play(mod.animate.shift(RIGHT * 3.7), FadeIn(pipeM), FadeOut(xm), run_time=0.6)
        self.play(Create(ok), run_time=0.3)
        done(self)


class B90_IdleWatcher(Scene):
    """A GPU-use line with bursts and a long flat gap; the watcher sweeps the flat part: 15 min an email, an hour the
    job is cancelled; filler work is crossed out; start when you sit down, cancel when you stop, batch the long work."""
    def construct(self):
        title = pE_act_title("IX · The Cluster's Rules")
        f = 0.05                        # the line's floor
        ay = -0.2                       # the time axis
        x0, x15, x60 = -3.2, -0.7, 2.2
        axis = Line([-5.85, ay, 0], [5.95, ay, 0], color=BAR1, stroke_width=5)
        yax = Line([-5.85, ay, 0], [-5.85, 1.9, 0], color=BAR1, stroke_width=5)
        ylab = T("GPU use", 34)
        ylab.move_to([-5.85 + ylab.width / 2, 2.2, 0])
        xlab = T("time", 34).move_to([5.45, -0.62, 0])
        pts = [(-5.85, f), (-5.6, f), (-5.45, 1.45), (-5.3, 0.7), (-5.15, 1.2), (-4.95, f), (-4.5, f), (-4.35, 1.0), (-4.15, f),
               (-3.8, f), (-3.7, 1.3), (-3.5, 0.6), (-3.35, f), (5.7, f)]
        gline = VMobject(stroke_color=INK, stroke_width=7)
        gline.set_points_as_corners([[a, b, 0] for a, b in pts])
        gline.set_z_index(2)
        peaks = VGroup(*[Dot([a, b, 0], radius=0.11, color=TERRA) for a, b in ((-5.45, 1.45), (-4.35, 1.0), (-3.7, 1.3))])
        peaks.set_z_index(3)
        bursty = T("bursty", 34).move_to([-2.9, 1.15, 0])
        # the watcher: a terracotta scan line carrying a chip
        scan = Line([x0, ay + 0.05, 0], [x0, 2.15, 0], color=TERRA, stroke_width=6)
        wchip = pE_chip_left("idle watcher", x0 + 0.02, 2.15)
        wchip.set_z_index(5)
        watcher = VGroup(scan, wchip)
        band1 = Rectangle(width=x15 - x0, height=0.7, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([(x0 + x15) / 2, f + 0.3, 0])
        band2 = Rectangle(width=x60 - x15, height=0.7, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([(x15 + x60) / 2, f + 0.3, 0])
        tk15 = VGroup(Line([x15, ay, 0], [x15, ay - 0.25, 0], color=INK, stroke_width=5), T("15 min", 34).move_to([x15, -0.75, 0]))
        tk60 = VGroup(Line([x60, ay, 0], [x60, ay - 0.25, 0], color=INK, stroke_width=5), T("1 hour", 34).move_to([x60, -0.75, 0]))
        env = pE_envelope(x15, -1.75)
        elab = T("email", 34).move_to([x15 - 1.3, -1.75, 0])
        jbox = VGroup(Iso(0, 0, 0.5).box(0, 0, 0, 0.9, 0.9, 0.72)).move_to([x60, -1.75, 0])
        jlab = T("job", 34).move_to([x60 - 0.95, -1.75, 0])
        jx = x_mark(x60, -1.75, r=0.32, w=9)
        you = professor_bear("1x1", 1.3, seed="B90", x=4.4, y=-1.75)
        ylb = T("you", 34).move_to([3.35, -1.75, 0])
        youg = Group(you, ylb)
        fx = -1.7
        flag = VGroup(Line([fx, f, 0], [fx, 1.0, 0], color=INK, stroke_width=6),
                      Polygon([fx, 1.0, 0], [fx + 0.6, 0.82, 0], [fx, 0.64, 0], fill_color=INK, fill_opacity=1, stroke_color=INK, stroke_width=2))
        flab = T("flagged", 34).move_to([fx + 1.5, 1.0, 0])
        filler = Rectangle(width=1.9, height=0.7, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([4.2, f + 0.4, 0])
        filab = T("filler work", 34).move_to([4.2, 1.15, 0])
        fix = x_mark(4.2, f + 0.4, r=0.4, w=9)
        k1 = pE_chip_left("sit down: start", -6.0, -2.85, size=32)
        k2 = pE_chip_left("stop: cancel", -2.45, -2.85, size=32)
        k3 = pE_chip_left("long work: batch jobs", 0.7, -2.85, size=32)

        self.play(FadeIn(title), FadeIn(ylab), Create(axis), Create(yax), run_time=0.45)
        self.play(Create(gline), FadeIn(xlab), run_time=0.75)
        # "idle GPUs": the watcher appears on the first flat stretch and sweeps it
        hear(self, "idle", lead=0.2)
        self.play(FadeIn(watcher), run_time=0.25)
        self.play(GrowFromEdge(band1, LEFT), watcher.animate.shift(RIGHT * (x15 - x0)), run_time=1.8, rate_func=linear)
        # "fifteen minutes ... an email"
        self.play(FadeIn(tk15), run_time=0.2)
        hear(self, "earns an", lead=0.3)
        self.play(FadeIn(env, shift=DOWN * 0.6), FadeIn(elab), run_time=0.35, rate_func=smooth)
        # "an hour ... the job cancelled"
        hear(self, "for an hour", lead=0.5)
        self.play(GrowFromEdge(band2, LEFT), watcher.animate.shift(RIGHT * (x60 - x15)), run_time=0.9, rate_func=linear)
        self.play(FadeIn(tk60), run_time=0.2)
        hear(self, "gets the job", lead=0.3)
        self.play(FadeIn(jbox, shift=DOWN * 0.6), FadeIn(jlab), run_time=0.35, rate_func=smooth)
        hear(self, "cancelled", lead=0.15)
        self.play(Create(jx), run_time=0.25)
        # "Coding is bursty ... long gaps while you read"
        hear(self, "bursty", lead=0.3)
        self.play(FadeIn(peaks), FadeIn(bursty), run_time=0.35)
        hear(self, "while you read", lead=0.35)
        self.play(FadeIn(youg), run_time=0.4)
        # "a session you walk away from will be flagged"
        hear(self, "walk away", lead=0.1)
        self.play(youg.animate.shift(RIGHT * 1.0), run_time=0.6, rate_func=smooth)
        hear(self, "be flagged", lead=0.35)
        self.play(FadeIn(flag, shift=DOWN * 0.4), FadeIn(flab), run_time=0.35, rate_func=smooth)
        # "Never add filler work"
        hear(self, "filler", lead=0.25)
        self.play(GrowFromEdge(filler, DOWN), FadeIn(filab), run_time=0.35)
        hear(self, "keep it alive", lead=0.35)
        self.play(Create(fix), run_time=0.25)
        # "Start when you sit down, cancel when you stop, ... batch jobs"
        hear(self, "Start when", lead=0.15)
        self.play(FadeIn(k1, shift=UP * 0.2), run_time=0.3)
        hear(self, "cancel when", lead=0.15)
        self.play(FadeIn(k2, shift=UP * 0.2), run_time=0.3)
        hear(self, "in batch jobs", lead=0.2)
        self.play(FadeIn(k3, shift=UP * 0.2), run_time=0.3)
        done(self)


def pE_envelope(x, y, w=1.1, h=0.75):
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.08, y - 0.08, 0])
    body = Rectangle(width=w, height=h, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    f1 = Line([x - w / 2, y + h / 2, 0], [x, y - 0.02, 0], color=INK, stroke_width=4)
    f2 = Line([x + w / 2, y + h / 2, 0], [x, y - 0.02, 0], color=INK, stroke_width=4)
    return VGroup(shadow, body, f1, f2)


class B91_NotAJobsShape(Scene):
    """An endpoint on a Slurm job dies when the 8 h clock runs out and returns elsewhere; and one person's cache grows to
    five stacked caches as five students share Ollama, filling the memory tank to about five times."""
    def construct(self):
        # top: the endpoint, its clock, its replacement
        rack1 = VGroup(*explorer_rack(Iso(-3.1, 1.0, 0.85)))
        lab1 = chip("endpoint", -3.1, 0.45, size=34)
        cdots = VGroup(*[Dot([x, y, 0], radius=0.15, color=TERRA) for x, y in ((-5.7, 2.2), (-5.1, 1.7), (-5.75, 1.3), (-5.15, 0.85), (-5.6, 0.45))])
        clines = VGroup(*[Line([x, y, 0], [-4.15, 1.5, 0], color=BAR1, stroke_width=3) for x, y in ((-5.7, 2.2), (-5.1, 1.7), (-5.75, 1.3), (-5.15, 0.85), (-5.6, 0.45))])
        slurm = chip("slurm", -0.5, 2.7, mono=True, size=34)
        cx, cy, cr = -0.5, 1.5, 0.6
        face = Circle(radius=cr, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([cx, cy, 0])
        ticks = VGroup(*[Line([cx + cr * 0.8 * np.sin(a), cy + cr * 0.8 * np.cos(a), 0], [cx + cr * 0.95 * np.sin(a), cy + cr * 0.95 * np.cos(a), 0], color=INK, stroke_width=4) for a in (0, PI / 2, PI, 3 * PI / 2)])
        hand = Line([cx, cy, 0], [cx, cy + cr * 0.7, 0], color=INK, stroke_width=7)
        hub = Dot([cx, cy, 0], radius=0.07, color=INK)
        clock = VGroup(face, ticks, hand, hub)
        eight = T("8 h", 46).move_to([0.95, 1.7, 0])
        gpu = M("gpu", 32).move_to([0.95, 1.1, 0])
        dead = x_mark(-3.1, 1.85, r=0.5, w=10)
        rack2 = VGroup(*explorer_rack(Iso(3.6, 1.0, 0.85)))
        lab2 = chip("new address", 3.6, 0.45, size=34)
        idle = chip("idle", 5.3, 1.75, w=1.3, size=34)
        reqs = [Dot([1.75, 1.6, 0], radius=0.13, color=TERRA) for _ in range(2)]
        # bottom: one user's cache grows to five; the memory tank fills
        olla = logo_chip("ollama", -5.2, -1.85, h=1.2)
        bx, bw, bh = -2.2, 2.2, 0.4
        by = [-2.85 + 0.5 * i for i in range(5)]
        blocks = [Rectangle(width=bw, height=bh, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([bx, y, 0]) for y in by]
        sdots = [Dot([-3.7, y, 0], radius=0.14, color=TERRA) for y in by]
        clab = T("cache", 34).move_to([-0.45, by[0], 0])
        tx, tw, th, ty = 1.1, 0.9, 2.4, -1.85
        tank = Rectangle(width=tw, height=th, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([tx, ty, 0])
        fh = th / 5
        fill1 = Rectangle(width=tw - 0.14, height=fh, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([tx, ty - th / 2 + 0.07 + fh / 2, 0])
        fillf = Rectangle(width=tw - 0.14, height=th - 0.14, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([tx, ty, 0])
        mlab = T("memory", 34).move_to([tx, -0.35, 0])
        ctx = chip("64,000 context", 4.05, -1.0, size=34)
        five = T("about 5x", 54).move_to([4.0, -2.3, 0])

        # "the shared endpoint for a whole class"
        hear(self, "shared endpoint", lead=0.35)
        self.play(FadeIn(rack1), FadeIn(lab1), run_time=0.4)
        hear(self, "whole class", lead=0.3)
        self.play(FadeIn(cdots), Create(clines), run_time=0.55)
        # "A Slurm job has a time limit, eight hours on the GPU partition"
        hear(self, "slurm job", lead=0.3)
        self.play(FadeIn(slurm), run_time=0.3)
        hear(self, "a time limit", lead=0.3)
        self.play(FadeIn(clock), run_time=0.3)
        self.play(Rotate(hand, angle=-PI, about_point=[cx, cy, 0]), run_time=0.7, rate_func=linear)
        hear(self, "eight hours", lead=0.1)
        self.play(Rotate(hand, angle=-PI, about_point=[cx, cy, 0]), FadeIn(eight), run_time=0.7, rate_func=linear)
        hear(self, "GPU partition", lead=0.2)
        self.play(FadeIn(gpu), run_time=0.3)
        # "an endpoint built on one dies on a schedule"
        hear(self, "dies on", lead=0.2)
        self.play(FadeIn(dead), run_time=0.25)
        hear(self, "a schedule", lead=0.1)
        self.play(FadeOut(rack1), FadeOut(lab1), FadeOut(dead), FadeOut(cdots), FadeOut(clines), run_time=0.45)
        # "returns on a different node"
        hear(self, "returns on", lead=0.15)
        self.play(FadeIn(rack2, shift=LEFT * 0.4), FadeIn(lab2, shift=LEFT * 0.4), run_time=0.45)
        # "Between requests, the GPU idles"
        hear(self, "Between requests", lead=0.1)
        self.play(FadeIn(reqs[0]), run_time=0.1)
        self.play(reqs[0].animate.move_to([2.75, 1.6, 0]), run_time=0.3, rate_func=linear)
        self.play(FadeOut(reqs[0]), run_time=0.1)
        self.wait(0.15)
        self.play(FadeIn(reqs[1]), run_time=0.1)
        self.play(reqs[1].animate.move_to([2.75, 1.6, 0]), run_time=0.3, rate_func=linear)
        self.play(FadeOut(reqs[1]), run_time=0.1)
        hear(self, "the GPU idles", lead=0.15)
        self.play(FadeIn(idle, shift=LEFT * 0.2), run_time=0.3)
        # "Ollama serves one person well"
        hear(self, "Olama serves", lead=0.25)
        self.play(FadeIn(olla), run_time=0.3)
        hear(self, "one person", lead=0.25)
        self.play(FadeIn(blocks[0]), FadeIn(sdots[0]), FadeIn(clab), FadeIn(tank), FadeIn(mlab), run_time=0.4)
        self.play(GrowFromEdge(fill1, DOWN), run_time=0.3)
        # "Five students ... roughly five times the cache memory"
        hear(self, "Five students", lead=0.15)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(blocks[i], shift=DOWN * 0.3), FadeIn(sdots[i])) for i in range(1, 5)], lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(ctx), run_time=0.3)
        hear(self, "cost roughly", lead=0.15)
        self.play(ReplacementTransform(fill1, fillf), run_time=0.8)
        hear(self, "five times", lead=0.2)
        self.play(FadeIn(five, scale=1.2), run_time=0.3)
        done(self)
