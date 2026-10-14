# ═════════════════════════════ PART B — B23 B24 B25 B26 B27 B31 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pB_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pB_laptop(x, y, s=1.0):
    """The laptop, front view: a rounded bezel with a smaller white screen on a thin base. Centred on (x, y)."""
    bezel = RoundedRectangle(corner_radius=0.12 * s, width=2.1 * s, height=1.4 * s, fill_color=BOX_L, fill_opacity=1,
                             stroke_color=INK, stroke_width=5).move_to([x, y + 0.1 * s, 0])
    screen = Rectangle(width=1.7 * s, height=1.0 * s, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR2,
                       stroke_width=4).move_to([x, y + 0.15 * s, 0])
    base = RoundedRectangle(corner_radius=0.08 * s, width=2.6 * s, height=0.22 * s, fill_color=BOX_R, fill_opacity=1,
                            stroke_color=INK, stroke_width=5).move_to([x, y - 0.72 * s, 0])
    return VGroup(base, bezel, screen)


def pB_pipe(a, b, w=18):
    """A pipe: an ink outline with a grey core, straight from a to b."""
    outer = Line(a, b, color=INK, stroke_width=w + 8)
    inner = Line(a, b, color=BAR2, stroke_width=w)
    g = VGroup(outer, inner)
    return g


def pB_arrow(a, b, w=6, tip=0.3):
    return Arrow(a, b, color=INK, stroke_width=w, buff=0, tip_length=tip, max_tip_length_to_length_ratio=0.5)


class B23_TunnelTarget(Scene):
    """Two tunnels from the laptop: the first ends at localhost on the login node (nothing there), the second runs
    through it to the compute node and the model; the direct line from the laptop to the compute node is crossed out."""
    def construct(self):
        lap = pB_laptop(-4.9, -0.95, 0.9)
        lap_l = T("laptop", 36).move_to([-4.9, -2.75, 0])
        il = Iso(-0.9, -2.0, 0.95)
        lst, llt = explorer_rack(il)
        login = VGroup(lst, llt)
        login_l = T("login node", 36).move_to([-0.9, -2.75, 0])
        ic = Iso(3.9, -2.0, 1.35)
        cst, clt = explorer_rack(ic)
        comp = VGroup(cst, clt)
        comp_l = T("compute node", 36).move_to([3.9, -2.75, 0])
        oll = logo_chip("ollama", 3.9, 1.95, h=1.1)
        self.play(FadeIn(lap), FadeIn(lap_l), FadeIn(login), FadeIn(login_l), FadeIn(comp), FadeIn(comp_l), FadeIn(oll), run_time=0.5)

        # the first tunnel: it ends on the login node, at its own localhost
        p1 = pB_pipe([-3.7, -0.55, 0], [-2.0, -0.55, 0])
        p1l = M("ssh -L", 32).move_to([-2.85, -0.05, 0])
        hear(self, "tunnel", lead=0.0)
        self.play(Create(p1), FadeIn(p1l), run_time=0.6)
        hear(self, "local host", lead=0.1)
        lh = M("localhost", 32).move_to([-0.9, 0.6, 0])
        self.play(FadeIn(lh), run_time=0.3)
        hear(self, "login node", lead=0.3)
        self.play(Indicate(login_l, color=INK, scale_factor=1.12), run_time=0.5)
        hear(self, "not the machine", lead=0.15)
        xl = x_mark(0.95, 0.6, r=0.25, w=9)
        self.play(Create(xl), run_time=0.3)
        hear(self, "running your model", lead=0.1)
        self.play(Indicate(oll, color=INK, scale_factor=1.1), run_time=0.5)

        # the second tunnel: it runs behind the login node and lands on the compute node
        p2 = pB_pipe([-3.7, -1.3, 0], [2.4, -1.3, 0])
        p2.set_z_index(-1)
        p2l = M("ssh -L", 32).move_to([-2.85, -1.95, 0])
        at(self, 5.2)
        self.play(Create(p2), FadeIn(p2l), run_time=0.75)
        hear(self, "compute node because", lead=0.2)
        ck = check(1.3, -0.8, s=0.3, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.4)

        # no direct line from the laptop to the GPU node
        hear(self, "does not support", lead=0.3)
        arc = ArcBetweenPoints([-4.9, 0.1, 0], [2.3, 0.9, 0], angle=-1.85)
        dashed = DashedVMobject(arc, num_dashes=34)
        dashed.set_color(INK)
        self.play(Create(dashed), run_time=0.8)
        hear(self, "SSH straight", lead=0.1)
        top = arc.point_from_proportion(0.5)
        xd = x_mark(top[0], top[1], r=0.3, w=10)
        self.play(Create(xd), run_time=0.25)
        hear(self, "straight into", lead=0.0)
        nd = T("no direct ssh", 36).move_to([top[0], top[1] + 0.65, 0])
        self.play(FadeIn(nd), run_time=0.3)
        done(self)


class B24_AliasMap(Scene):
    """Claude fans out four model names; unmapped, they all hit ollama's empty shelf; mapped, all four land on one local model."""
    def construct(self):
        sx = -3.55
        yc = -0.1
        rows = {"haiku": 1.5, "sonnet": 0.5, "opus": -0.5, "subagent": -1.65}
        claude = logo_chip("claude", -5.0, yc)
        stub = Line([-4.1, yc, 0], [sx, yc, 0], color=INK, stroke_width=6)
        panel = Rectangle(width=2.0, height=4.0, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.4, yc, 0])
        slots = VGroup(*[Rectangle(width=1.5, height=0.5, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([3.4, y, 0]) for y in rows.values()])
        oll = logo_chip("ollama", 3.4, 2.4, h=1.0)
        self.play(FadeIn(claude), Create(stub), FadeIn(panel), FadeIn(slots), FadeIn(oll), run_time=0.5)

        def row(name, y):
            seg = Line([sx, yc, 0], [sx, y, 0], color=INK, stroke_width=6)
            arr = pB_arrow([sx, y, 0], [2.35, y, 0])
            lab = T(name, 34)
            dy = -0.42 if name == "subagent" else 0.38
            lab.move_to([sx + 0.3 + lab.width / 2, y + dy, 0])
            return seg, arr, lab

        r = {n: row(n, y) for n, y in rows.items()}
        # the small model does the background tasks
        hear(self, "small model", lead=0.3)
        self.play(Create(r["haiku"][0]), Create(r["haiku"][1]), FadeIn(r["haiku"][2]), run_time=0.5)
        hear(self, "background tasks", lead=0.2)
        bg = chip("background tasks", -0.2, 2.2, size=32)
        self.play(FadeIn(bg), run_time=0.3)
        # subagents have a setting of their own
        hear(self, "separate setting", lead=0.3)
        self.play(Create(r["subagent"][0]), Create(r["subagent"][1]), FadeIn(r["subagent"][2]), run_time=0.5)
        # the other two names are asked for as well, none of them mapped
        hear(self, "Unless you point", lead=0.2)
        self.play(*[Create(m) for n in ("sonnet", "opus") for m in r[n][:2]], *[FadeIn(r[n][2]) for n in ("sonnet", "opus")], run_time=0.6)

        # ollama has none of these models
        hear(self, "Claude models it does not have", lead=0.3)
        crosses = VGroup(*[x_mark(3.4, y, r=0.2, w=7) for y in rows.values()])
        nf = chip("model not found", 3.4, -2.75, mono=True, size=32)
        self.play(*[Create(c) for c in crosses], FadeIn(nf), run_time=0.5)

        # the script sets every name to one local model
        hear(self, "So the script sets", lead=0.1)
        block = Rectangle(width=1.4, height=1.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.4, yc, 0])
        lm = T("local model", 38).move_to([3.4, -2.6, 0])
        self.play(FadeOut(slots), FadeOut(crosses), FadeOut(nf), run_time=0.3)
        self.play(FadeIn(block), FadeIn(lm), run_time=0.4)
        ends = {"haiku": 0.25, "sonnet": 0.05, "opus": -0.15, "subagent": -0.35}
        new = {}

        def remap(n):
            y = rows[n]
            a = pB_arrow([sx, y, 0], [2.7, yc + ends[n], 0])
            new[n] = a
            return a
        hear(self, "small medium", lead=0.0)
        self.play(FadeOut(r["haiku"][1]), Create(remap("haiku")), run_time=0.45)
        hear(self, "medium", lead=0.0)
        self.play(FadeOut(r["sonnet"][1]), Create(remap("sonnet")), run_time=0.45)
        hear(self, "large", lead=0.0)
        self.play(FadeOut(r["opus"][1]), Create(remap("opus")), run_time=0.45)
        hear(self, "subagent model", lead=0.1)
        self.play(FadeOut(r["subagent"][1]), Create(remap("subagent")), run_time=0.45)
        hear(self, "to one local model", lead=0.1)
        ck = check(3.4, 1.3, s=0.28, color=TERRA, w=12)
        en = chip("every name", -0.4, -2.75, mono=True, size=32)
        self.play(Create(ck), FadeIn(en), run_time=0.45)
        done(self)


class B25_SilentTruncation(Scene):
    """The default window is a short bar: instructions and tools pour in, the overflow is cut without a sound; at 65,536 all fit."""
    def construct(self):
        x0, per_k, h = -5.6, 10.5 / 65.536, 1.3
        bh = 1.0
        cw = T("context window", 40)
        cw.move_to([x0 + cw.width / 2, 2.3, 0])
        ruler = Line([x0, -2.1, 0], [x0 + 10.5, -2.1, 0], color=INK, stroke_width=5)
        t0 = Line([x0, -2.1, 0], [x0, -1.85, 0], color=INK, stroke_width=5)
        self.play(FadeIn(cw), Create(ruler), Create(t0), run_time=0.45)

        def tick(k, txt):
            x = x0 + k * per_k
            ln = Line([x, -2.1, 0], [x, -1.8, 0], color=INK, stroke_width=6)
            lab = T(txt, 36).move_to([x, -2.65, 0])
            return ln, lab

        # the 4k default: a short window with a wall at its edge, then the 32k tick
        hear(self, "4 000 tokens", lead=0.45)
        w4 = Rectangle(width=4.0 * per_k, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
        w4.move_to([x0 + 2.0 * per_k, 0, 0])
        wall = Line([x0 + 4.0 * per_k, -0.9, 0], [x0 + 4.0 * per_k, 0.9, 0], color=INK, stroke_width=9)
        wall.set_z_index(5)
        k4, l4 = tick(4.0, "4k")
        self.play(GrowFromEdge(w4, LEFT), Create(wall), Create(k4), FadeIn(l4), run_time=0.45)
        hear(self, "32 000", lead=0.3)
        k32, l32 = tick(32.0, "32k")
        self.play(Create(k32), FadeIn(l32), run_time=0.35)

        def blocks():
            specs = [("instructions", 1.9), ("tools", 2.6), ("your code", 2.2)]
            out, xs = [], x0
            for name, w in specs:
                b = Rectangle(width=w, height=bh, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
                b.move_to([xs + w / 2, 0, 0])
                lab = T(name, 36).move_to([xs + w / 2, -1.15, 0])
                out.append((b, lab, xs, w))
                xs += w + 0.2
            return out

        bl = blocks()
        # the instructions pour in: only a sliver fits in the window
        inside_w = 4.0 * per_k
        b0, lab0, bx0, bw0 = bl[0]
        ins_in = Rectangle(width=inside_w, height=bh, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([bx0 + inside_w / 2, 0, 0])
        ins_out = Rectangle(width=bw0 - inside_w, height=bh, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([bx0 + inside_w + (bw0 - inside_w) / 2, 0, 0])
        grp0 = VGroup(ins_in, ins_out)
        grp0.shift(UP * 1.4)
        at(self, 8.0)
        self.add(grp0)
        self.play(grp0.animate.shift(DOWN * 1.4), run_time=0.5, rate_func=ease_in)
        self.play(FadeIn(lab0), run_time=0.2)
        # the tool list pours in behind it
        hear(self, "tool list", lead=0.35)
        b1, lab1, bx1, bw1 = bl[1]
        b1.shift(UP * 1.4)
        self.add(b1)
        self.play(b1.animate.shift(DOWN * 1.4), run_time=0.45, rate_func=ease_in)
        self.play(FadeIn(lab1), run_time=0.2)
        # the overflow is cut, silently
        hear(self, "is cut", lead=0.2)
        self.play(FadeOut(ins_out), FadeOut(b1), FadeOut(lab0), FadeOut(lab1), run_time=0.7)

        # a window of 65,536: every block fits
        hear(self, "Ask for", lead=0.1)
        w65 = Rectangle(width=65.536 * per_k, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
        w65.move_to([x0 + 65.536 * per_k / 2, 0, 0])
        wall2 = Line([x0 + 10.5, -0.9, 0], [x0 + 10.5, 0.9, 0], color=INK, stroke_width=9)
        wall2.set_z_index(5)
        k65 = Line([x0 + 10.5, -2.1, 0], [x0 + 10.5, -1.8, 0], color=INK, stroke_width=6)
        num = M("65,536", 44).move_to([x0 + 10.5 - 0.95, 2.3, 0])
        self.play(FadeOut(w4), FadeOut(wall), FadeOut(ins_in), GrowFromEdge(w65, LEFT), Create(wall2), Create(k65), FadeIn(num), run_time=0.65)
        hear(self, "65 536", lead=0.1)
        fresh = blocks()
        for b, lab, bx, bw in fresh:
            b.shift(UP * 1.4)
            self.add(b)
        self.play(LaggedStart(*[b.animate.shift(DOWN * 1.4) for b, _, _, _ in fresh], lag_ratio=0.3), run_time=1.0, rate_func=ease_in)
        self.play(*[FadeIn(lab) for _, lab, _, _ in fresh], run_time=0.3)
        hear(self, "or more", lead=0.3)
        ck = check(3.7, 0.0, s=0.35, color=TERRA, w=13)
        ck.set_z_index(6)
        self.play(Create(ck), run_time=0.4)
        done(self)


def pB_cards(cx, cy, cols=6, rows=4, cw=0.42, ch=0.56, gap=0.08):
    """A pile of small tool cards laid out as a block (24 by default: dozens)."""
    cards = VGroup()
    w = cols * cw + (cols - 1) * gap
    h = rows * ch + (rows - 1) * gap
    for r_ in range(rows):
        for c_ in range(cols):
            x = cx - w / 2 + cw / 2 + c_ * (cw + gap)
            y = cy + h / 2 - ch / 2 - r_ * (ch + gap)
            cards.add(Rectangle(width=cw, height=ch, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y, 0]))
    return cards


class B26_TooSmallModel(Scene):
    """A tiny model is offered the pile of tool definitions and drops it; the big model holds the whole pile."""
    def construct(self):
        ruler = Line([-5.6, -3.0, 0], [5.6, -3.0, 0], color=INK, stroke_width=5)
        ticks = VGroup(*[Line([x, -3.0, 0], [x, -2.8 if i % 5 else -2.65, 0], color=INK, stroke_width=3) for i, x in enumerate(np.arange(-5.6, 5.61, 0.4))])
        self.play(Create(ruler), Create(ticks), run_time=0.5)
        # the tiny model
        hear(self, "one and a half billion", lead=0.2)
        tiny = Rectangle(width=1.7, height=1.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-3.5, -0.9, 0])
        tl = T("1.5B", 44).move_to([-3.5, -2.3, 0])
        self.play(FadeIn(tiny), FadeIn(tl), run_time=0.4)
        hear(self, "reasoning model", lead=0.2)
        led = Dot([-3.5 + 0.55, -0.9 + 0.55, 0], radius=0.14, color=TERRA)
        self.play(FadeIn(led, scale=1.8), run_time=0.3)
        # the pile of tool definitions is offered to it
        hear(self, "cannot reliably", lead=0.15)
        pile = pB_cards(-3.5, 1.25)
        self.play(FadeIn(pile, shift=DOWN * 1.6), run_time=0.55)
        # it cannot hold them: every card spills
        hear(self, "drive an agent loop", lead=0.3)
        rng = np.random.RandomState(7)
        spills = []
        for i, c_ in enumerate(pile):
            side = 1 if i % 2 else -1
            tx = -3.5 + side * rng.uniform(1.3, 2.3)
            ty = -1.55 + rng.uniform(-0.12, 0.12)
            spills.append(c_.animate.move_to([tx, ty, 0]).rotate(float(rng.uniform(-1.2, 1.2))))
        self.play(LaggedStart(*spills, lag_ratio=0.03), run_time=1.2)
        xm = x_mark(-1.0, 0.9, r=0.3, w=10)
        self.play(Create(xm), run_time=0.3)

        # dozens of tool definitions
        hear(self, "dozens of tool definitions", lead=0.3)
        td = T("tool definitions", 36).move_to([-0.7, 2.85, 0])
        self.play(FadeIn(td), run_time=0.3)

        # the big model holds the whole pile
        hear(self, "Use a tool capable", lead=0.1)
        big = Rectangle(width=4.6, height=3.8, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([2.9, 0.15, 0])
        bl = T("20B to 120B", 44).move_to([2.9, -2.3, 0])
        self.play(FadeIn(big), FadeIn(bl), run_time=0.45)
        pile2 = pB_cards(2.9, 0.15)
        self.play(FadeIn(pile2, shift=DOWN * 1.6), run_time=0.6)
        hear(self, "in the range", lead=0.2)
        ck = check(5.55, 1.8, s=0.32, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.4)
        hear(self, "20 to 120", lead=0.1)
        self.play(Indicate(bl, color=INK, scale_factor=1.1), run_time=0.5)
        done(self)


def pB_clock(x, y, r=0.5):
    face = Circle(radius=r, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    minute = Line([x, y, 0], [x, y + r * 0.7, 0], color=INK, stroke_width=6)
    hour = Line([x, y, 0], [x + r * 0.4, y, 0], color=INK, stroke_width=7)
    hub = Dot([x, y, 0], radius=0.07, color=INK)
    g = VGroup(face, hour, minute, hub)
    g.minute, g.cx, g.cy = minute, x, y
    return g


def pB_tag(text, x, y, w=6.2, h=1.5):
    """A price tag: a white tag with a pointed end and a punched hole, carrying a short phrase."""
    pts = [[x - w / 2, y, 0], [x - w / 2 + 0.7, y + h / 2, 0], [x + w / 2, y + h / 2, 0], [x + w / 2, y - h / 2, 0], [x - w / 2 + 0.7, y - h / 2, 0]]
    shadow = Polygon(*[[p[0] + 0.1, p[1] - 0.1, 0] for p in pts], fill_color=BOX_L, fill_opacity=1, stroke_width=0)
    card = Polygon(*pts, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0)
    hole = Circle(radius=0.12, fill_color=STAGE, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x - w / 2 + 0.55, y, 0])
    lab = T(text, 44).move_to([x + 0.4, y, 0])
    g = VGroup(shadow, card, hole, lab)
    g.lab = lab
    return g


def pB_label(txt, size, x, y_base):
    """A label whose BASELINE sits at y_base (a row of labels shares one line, descenders or not)."""
    lab = T(txt, size)
    d = 0.0
    if any(c in "gjpqy" for c in txt):
        d = T("x", size).get_bottom()[1] - T("q", size).get_bottom()[1]
    lab.move_to([x, y_base, 0])
    lab.shift(UP * ((y_base - d) - lab.get_bottom()[1]))
    return lab


class B27_NotFree(Scene):
    """'zero marginal cost' is struck out and slides off; a queue, a draining fair share and an idle watcher take its place; no per-token billing lands below."""
    def construct(self):
        tag = pB_tag("zero marginal cost", -0.4, 1.0)
        strike = x_mark(3.45, 1.0, r=0.38, w=12)
        hear(self, "zero marginal cost", lead=0.3)
        self.play(FadeIn(tag), run_time=0.4)
        hear(self, "marginal cost", lead=0.1)
        self.play(Create(strike), run_time=0.3)

        ly = -0.95   # baseline of every meter label
        # the tag slides off and the fair-share gauge takes its place
        hear(self, "GPU hours", lead=0.95)
        self.play(FadeOut(VGroup(tag, strike), shift=RIGHT * 3.0), run_time=0.35)
        gc, gw, gh = 1.3, 1.3, 2.9
        tank = Rectangle(width=gw, height=gh, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([0.0, gc, 0])
        fh = gh - 0.3
        base = gc - gh / 2 + 0.15
        full = Rectangle(width=gw - 0.3, height=fh, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([0.0, base + fh / 2, 0])
        low = Rectangle(width=gw - 0.3, height=0.6, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([0.0, base + 0.3, 0])
        fl = pB_label("fair share", 40, 0.0, ly)
        self.play(FadeIn(tank), FadeIn(full), FadeIn(fl), run_time=0.35)
        hear(self, "fair share", lead=0.1)
        self.play(Transform(full, low), run_time=0.7)
        # the queue: boxes in a line, a clock that waits
        hear(self, "you wait in a queue", lead=0.2)
        clk = pB_clock(-4.1, 2.0, 0.65)
        boxes = VGroup(*[Rectangle(width=0.5, height=0.66, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-5.15 + 0.72 * i, 0.55, 0]) for i in range(4)])
        desk = Line([-2.65, 0.1, 0], [-2.65, 1.0, 0], color=INK, stroke_width=9)
        ql = pB_label("queue", 40, -4.1, ly)
        self.play(FadeIn(clk), FadeIn(ql), FadeIn(desk), LaggedStart(*[FadeIn(b, shift=LEFT * 0.3) for b in boxes], lag_ratio=0.2), run_time=0.6)
        self.play(Rotate(clk.minute, angle=-2 * PI, about_point=[clk.cx, clk.cy, 0]), run_time=0.7, rate_func=linear)
        # the idle watcher
        hear(self, "idle watcher", lead=0.2)
        lens = Circle(radius=0.85, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=8).move_to([3.8, 1.6, 0])
        handle = Line([3.8 + 0.6, 1.6 - 0.6, 0], [3.8 + 1.4, 1.6 - 1.4, 0], color=INK, stroke_width=16)
        job = Rectangle(width=0.7, height=0.55, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.8, 1.6, 0])
        wl = pB_label("idle watcher", 40, 4.0, ly)
        self.play(FadeIn(lens), FadeIn(handle), FadeIn(job), FadeIn(wl), run_time=0.45)
        hear(self, "cancels jobs", lead=0.3)
        xj = x_mark(3.8, 1.6, r=0.3, w=9)
        self.play(Create(xj), run_time=0.3)

        # the accurate claim
        hear(self, "no per token billing", lead=0.6)
        plq = chip("no per-token billing", -1.5, -2.25, size=44)
        plq.shift(UP * 0.7)
        self.add(plq)
        self.play(plq.animate.shift(DOWN * 0.7), run_time=0.5, rate_func=smooth)
        # where the cost went
        hear(self, "queue time", lead=0.1)
        self.play(Indicate(ql, color=INK, scale_factor=1.2), run_time=0.5)
        hear(self, "fair share", lead=0.1, nth=1)
        self.play(Indicate(fl, color=INK, scale_factor=1.2), run_time=0.5)
        hear(self, "capability", lead=0.2)
        cap = chip("capability", 4.0, -2.25, size=44)
        self.play(FadeIn(cap, shift=LEFT * 0.3), run_time=0.4)
        done(self)


def pB_folder(x, y, w=1.6, h=1.1):
    """A folder with a dotted outline: a hidden folder."""
    body = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    tab = Rectangle(width=w * 0.4, height=0.24, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x - w * 0.3, y + h / 2 + 0.12, 0])
    ob = DashedVMobject(Rectangle(width=w, height=h, color=INK, stroke_width=5).move_to([x, y, 0]), num_dashes=30)
    ot = DashedVMobject(Rectangle(width=w * 0.4, height=0.24, color=INK, stroke_width=5).move_to([x - w * 0.3, y + h / 2 + 0.12, 0]), num_dashes=10)
    return VGroup(tab, body, ob, ot)


class B31_HomeFills(Scene):
    """The hidden cache fills home's quota (cross); cache and temp are redirected to your storage; the pull runs on the compute node, not the login node."""
    def construct(self):
        ih = Iso(-4.1, 0.4, 1.05)
        home = home_box(ih)
        hl = T("home", 38).move_to([-4.1, 0.0, 0])
        gx, gy0, gh = -5.8, 0.55, 2.0
        gauge = Rectangle(width=0.5, height=gh, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([gx, gy0 + gh / 2, 0])
        gl = T("quota", 34).move_to([gx + 0.1, 0.0, 0])
        self.play(FadeIn(home), FadeIn(hl), FadeIn(gauge), FadeIn(gl), run_time=0.5)

        # the hidden cache folder, inside home, filling the quota
        hear(self, "hidden folder", lead=0.4)
        fold = pB_folder(-1.3, 1.55)
        fl = M(".apptainer", 32).move_to([-1.3, 0.7, 0])
        self.play(FadeIn(fold), FadeIn(fl), run_time=0.4)
        hear(self, "in home", lead=0.25)
        into = pB_arrow([-2.25, 1.55, 0], [-3.1, 1.55, 0], w=7, tip=0.28)
        self.play(Create(into), run_time=0.3)
        hear(self, "fills first", lead=0.6)
        fill = Rectangle(width=0.38, height=gh - 0.1, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([gx, gy0 + 0.05 + (gh - 0.1) / 2, 0])
        self.play(GrowFromEdge(fill, DOWN), run_time=0.9, rate_func=linear)
        xg = x_mark(gx, 2.95, r=0.22, w=9)
        self.play(Create(xg), run_time=0.25)

        # point the cache and temp folders at your own storage
        hear(self, "So point", lead=0.4)
        isb = Iso(3.4, 0.3, 0.75)
        sb_back, sb_front = scratch_bin(isb)
        sl = T("your storage", 38).move_to([3.7, 3.0, 0])
        self.play(FadeOut(into), FadeIn(sb_back), FadeIn(sb_front), FadeIn(sl), run_time=0.45)
        a1 = pB_arrow([-0.35, 1.85, 0], [2.0, 1.85, 0], w=7, tip=0.28)
        a2 = pB_arrow([-0.35, 1.3, 0], [2.0, 1.3, 0], w=7, tip=0.28)
        l1 = T("cache", 34).move_to([0.8, 2.3, 0])
        l2 = T("temp", 34).move_to([0.8, 0.85, 0])
        self.play(Create(a1), Create(a2), FadeIn(l1), FadeIn(l2), run_time=0.55)

        # pull the images there, on a compute node rather than the login node
        hear(self, "pull the images", lead=1.0)
        il = Iso(-2.6, -2.65, 0.95)
        lst, llt = explorer_rack(il)
        login = VGroup(lst, llt)
        lll = T("login node", 36).move_to([-2.6, -3.05, 0])
        ic = Iso(1.9, -2.65, 0.95)
        cst, clt = explorer_rack(ic)
        comp = VGroup(cst, clt)
        cl = T("compute node", 36).move_to([1.9, -3.05, 0])
        self.play(FadeIn(login), FadeIn(lll), FadeIn(comp), FadeIn(cl), run_time=0.5)
        hear(self, "pull the images", lead=0.1)
        img = Iso(0, 0, 0.8).box(0, 0, 0, 0.7, 0.7, 0.6)
        img.move_to([1.9, -0.45, 0])
        img.set_z_index(1)
        self.play(FadeIn(img), run_time=0.2)
        target = isb.p(1.35, 0.9, 0.35)
        self.play(img.animate.move_to([target[0], target[1] + 0.1, 0]), run_time=0.9, rate_func=smooth)
        hear(self, "on a compute node", lead=0.1)
        ck = check(3.45, -1.2, s=0.3, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.35)
        hear(self, "login node", lead=0.0)
        xl = x_mark(-2.6, -0.3, r=0.3, w=10)
        self.play(Create(xl), login.animate.set_opacity(0.4), run_time=0.4)
        done(self)
