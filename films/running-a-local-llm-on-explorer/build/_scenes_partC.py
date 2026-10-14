# ═════════════════════════════ PART C — B40 B41 B42 B43 B44 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pC_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pC_slow(t):
    """Fast, then crawling: a stopwatch hand that ends up barely moving."""
    return 1 - (1 - t) ** 5


def pC_stopwatch(x, y, r=0.6):
    face = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    knob = Rectangle(width=0.26, height=0.16, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + r + 0.12, 0])
    hand = Line([x, y, 0], [x, y + r * 0.7, 0], color=INK, stroke_width=7)
    hub = Dot([x, y, 0], radius=0.07, color=INK)
    g = VGroup(knob, face, hand, hub)
    g.hand, g.cx, g.cy = hand, x, y
    return g


def pC_blk(cx, y0, w, h, fill=BAR1, sw=4):
    """A block standing on y0 (its bottom edge), centred on cx."""
    return Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=sw).move_to([cx, y0 + h / 2, 0])


def pC_tank(cx, yb, yt, w):
    """The video-memory tank: a white fill and an open-topped U wall in ink."""
    fill = Rectangle(width=w, height=yt - yb, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([cx, (yt + yb) / 2, 0])
    wall = VMobject(stroke_color=INK, stroke_width=9, fill_opacity=0)
    wall.set_points_as_corners([[cx - w / 2, yt, 0], [cx - w / 2, yb, 0], [cx + w / 2, yb, 0], [cx + w / 2, yt, 0]])
    return VGroup(fill, wall)


def pC_proc(x, y):
    """The processor: a dark chip body with kraft pins on both sides."""
    body = Rectangle(width=2.3, height=1.0, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    pins = VGroup(*[Line([x + s * 1.15, y + dy, 0], [x + s * 1.42, y + dy, 0], color=KRAFT_DEEP, stroke_width=7)
                    for s in (-1, 1) for dy in (-0.28, 0.0, 0.28)])
    return VGroup(pins, body)


class B40_FitInVram(Scene):
    """Weights sink into the video-memory tank, the cache stacks on them (a check); a bigger cache overflows the top and
    the spilled part drops onto the processor, where the stopwatch crawls."""
    def construct(self):
        cx, yb, yt, tw, bw = -0.1, -2.75, 1.35, 2.4, 2.0
        title = pC_act_title("IV · Choose A GPU And A Model")
        tank = pC_tank(cx, yb, yt, tw)
        vlab = T("video memory", 36)
        vlab.move_to([-1.65 - vlab.width / 2, 1.0, 0])
        wt = pC_blk(cx, yb + 0.06, bw, 1.75, BAR1)
        wlab = T("weights", 34)
        wlab.move_to([-1.65 - wlab.width / 2, -1.815, 0])
        cache = pC_blk(cx, -0.88, bw, 0.9, BAR2)
        clab = T("context cache", 34)
        clab.move_to([-1.65 - clab.width / 2, -0.43, 0])
        ck = check(1.95, 0.75, s=0.3, color=TERRA, w=12)
        cache_full = pC_blk(cx, -0.88, bw, yt + 0.88, BAR2)
        spill = pC_blk(cx, yt, bw, 0.95, BAR2)
        oll = logo_chip("ollama", 5.2, 2.3, h=1.3)
        proc = pC_proc(4.2, -1.95)
        plab = T("processor", 36).move_to([4.2, -2.95, 0])
        sw = pC_stopwatch(3.0, 0.75, 0.65)
        crawl = T("crawl", 48).move_to([4.9, 0.75, 0])

        self.play(FadeIn(title), FadeIn(tank), FadeIn(vlab), run_time=0.5)
        # "the model's weights": the weights block sinks into the tank
        hear(self, "weights", lead=0.15)
        wt.shift(UP * 2.29)
        self.play(FadeIn(wt), run_time=0.15)
        self.play(wt.animate.shift(DOWN * 2.29), run_time=0.5, rate_func=ease_in)
        self.play(FadeIn(wlab), run_time=0.25)
        # "room left for the context window's cache": the cache stacks on top, then the check
        hear(self, "room left", lead=0.45)
        cache.shift(UP * 1.33)
        self.play(FadeIn(cache), run_time=0.15)
        self.play(cache.animate.shift(DOWN * 1.33), run_time=0.5, rate_func=ease_in)
        self.play(Create(ck), run_time=0.3)
        hear(self, "context windows", lead=0.1)
        self.play(FadeIn(clab), run_time=0.25)
        # "if either spills over": the cache grows to the brim, then past it
        hear(self, "spills over", lead=0.4)
        self.play(FadeOut(ck), Transform(cache, cache_full), run_time=0.5)
        hear(self, "over", lead=0.25)
        self.play(GrowFromEdge(spill, DOWN), run_time=0.4)
        # "Ollama pushes layers onto the processor": the spilled part rides over and drops on the chip
        hear(self, "Olama", lead=0.1)
        self.play(FadeIn(oll), FadeIn(proc), run_time=0.4)
        hear(self, "pushes", lead=0.05)
        a, b = np.array([cx, yt + 0.475, 0.0]), np.array([4.2, -1.45 + 0.475, 0.0])
        self.play(MoveAlongPath(spill, ArcBetweenPoints(a, b, angle=1.0)), run_time=0.85, rate_func=smooth)
        hear(self, "processor", lead=0.1)
        self.play(FadeIn(plab), run_time=0.3)
        # "generation slows to a crawl": the stopwatch spins, then its hand barely moves
        hear(self, "generation", lead=0.1)
        self.play(FadeIn(sw), run_time=0.25)
        self.play(Rotate(sw.hand, angle=-1.9 * PI, about_point=[sw.cx, sw.cy, 0]), run_time=1.0, rate_func=pC_slow)
        hear(self, "a crawl", lead=0.1)
        self.play(FadeIn(crawl), Rotate(sw.hand, angle=-0.25, about_point=[sw.cx, sw.cy, 0], rate_func=linear), run_time=0.7)
        done(self)


def pC_hatch(xa, xb, ya, yb, gap=0.2, color=BAR1, sw=3.5):
    """Diagonal hatch lines clipped to the rectangle [xa, xb] x [ya, yb]."""
    w, h = xb - xa, yb - ya
    lines = VGroup()
    c = -h
    while c < w:
        xs, xe = xa + max(0.0, c), xa + min(w, c + h)
        if xe - xs > 0.02:
            lines.add(Line([xs, ya + (xs - xa - c), 0], [xe, ya + (xe - xa - c), 0], color=color, stroke_width=sw))
        c += gap
    return lines


def pC_ruler(x0, scale, vmax, step, y, size=32):
    """A gigabyte ruler: ink line, ticks, numerals. Returns (line, ticks, numerals)."""
    line = Line([x0, y, 0], [x0 + vmax * scale, y, 0], color=INK, stroke_width=6)
    ticks = VGroup(*[Line([x0 + v * scale, y, 0], [x0 + v * scale, y - 0.28, 0], color=INK, stroke_width=6) for v in range(0, vmax + 1, step)])
    nums = VGroup(*[T(str(v), size).move_to([x0 + v * scale, y - 0.56, 0]) for v in range(0, vmax + 1, step)])
    return line, ticks, nums


def pC_model_label(company, text, x, y):
    """A maker's logo, then the model name beside it."""
    lg = logo_chip(company, x + 0.45, y, h=0.6)
    lab = T(text, 32)
    lab.move_to([x + 1.05 + lab.width / 2, y, 0])
    return Group(lg, lab)


def pC_bar_num(text, x_end, y):
    """A numeral sitting inside the right end of a bar (ink on grey)."""
    n = T(text, 38, bold=True)
    return n.move_to([x_end - 0.22 - n.width / 2, y, 0])


class B41_ModelsThatFit(Scene):
    """Three bars to scale on one gigabyte ruler: 14, 19, and 19 with a hatched extension out to 23."""
    def construct(self):
        x0, sc, bh = -5.5, 0.42, 0.64
        ys = [1.8, 0.15, -1.5]
        ex = lambda gb: x0 + gb * sc
        axis = Line([x0, 2.15, 0], [x0, -2.45, 0], color=BAR2, stroke_width=6)
        rl, rt, rn = pC_ruler(x0, sc, 25, 5, -2.45)
        gb = T("GB", 34).move_to([ex(25) + 0.7, -3.01, 0])
        dsz = T("download size", 36).move_to([6.1 - 1.31, 2.8, 0])
        labs = [pC_model_label("openai", "gpt-oss 20b", -5.4, ys[0] + 0.8),
                pC_model_label("qwen", "qwen3-coder 30b", -5.4, ys[1] + 0.8),
                pC_model_label("glm", "glm-4.7-flash", -5.4, ys[2] + 0.8)]
        b1 = pC_blk(0, 0, 14 * sc, bh, BAR2, 4).move_to([ex(7), ys[0], 0])
        b2 = pC_blk(0, 0, 19 * sc, bh, BAR2, 4).move_to([ex(9.5), ys[1], 0])
        b3 = pC_blk(0, 0, 19 * sc, bh, BAR2, 4).move_to([ex(9.5), ys[2], 0])
        n1, n2, n3 = pC_bar_num("14", ex(14), ys[0]), pC_bar_num("19", ex(19), ys[1]), pC_bar_num("19", ex(19), ys[2])
        ext_box = Rectangle(width=4 * sc, height=bh, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([ex(21), ys[2], 0])
        ext = VGroup(ext_box, pC_hatch(ex(19), ex(23), ys[2] - bh / 2 + 0.03, ys[2] + bh / 2 - 0.03, gap=0.22))
        n23 = T("23", 44, bold=True).move_to([ex(23) + 0.55, ys[2], 0])
        tag1 = T("video memory", 32)
        tag2 = T("at 64k context", 32)
        tg = VGroup(tag1, tag2).arrange(RIGHT, buff=0.2)
        tg.move_to([6.1 - tg.width / 2, ys[2] + 0.8, 0])

        self.play(Create(axis), Create(rl), FadeIn(rt), FadeIn(rn), FadeIn(gb), FadeIn(dsz), run_time=0.7)
        # "the 20 billion GPT-OSS is about 14 gigabytes"
        hear(self, "20 billion", lead=0.2)
        self.play(FadeIn(labs[0]), run_time=0.3)
        hear(self, "about 14", lead=0.25)
        self.play(GrowFromEdge(b1, LEFT), run_time=0.8)
        self.play(FadeIn(n1), run_time=0.2)
        # "the 30 billion Qwen 3 Coder is about 19"
        hear(self, "30 billion", lead=0.2)
        self.play(FadeIn(labs[1]), run_time=0.3)
        hear(self, "about 19", lead=0.25)
        self.play(GrowFromEdge(b2, LEFT), run_time=0.75)
        self.play(FadeIn(n2), run_time=0.2)
        # "GLM 4.7 Flash is also about 19 to download"
        hear(self, "GLM", lead=0.05)
        self.play(FadeIn(labs[2]), run_time=0.3)
        hear(self, "also about 19", lead=0.2)
        self.play(GrowFromEdge(b3, LEFT), run_time=0.8)
        self.play(FadeIn(n3), run_time=0.2)
        # "but Ollama puts it near 23 of video memory at 64,000 context": the hatched extension
        hear(self, "near 23", lead=0.5)
        self.play(GrowFromEdge(ext, LEFT), run_time=0.8)
        self.play(FadeIn(n23), run_time=0.2)
        hear(self, "video memory", lead=0.3)
        self.play(FadeIn(tag1), run_time=0.3)
        hear(self, "at 64", lead=0.1)
        self.play(FadeIn(tag2), run_time=0.3)
        done(self)


def pC_stamp(text, x, y, w=1.75):
    """A stamp on a card: kraft pill, ink outline, a terracotta dot, a short word."""
    sh = pill(x + 0.07, y - 0.07, w, h=0.7, fill=BOX_L)
    body = RoundedRectangle(width=w, height=0.7, corner_radius=0.35, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    dot = Dot([x - w / 2 + 0.32, y, 0], radius=0.1, color=TERRA)
    lab = T(text, 34).move_to([x + 0.22, y, 0])
    return VGroup(sh, body, dot, lab)


def pC_gear(x, y, r=0.55, teeth=8):
    """A gear: a toothed kraft polygon and a hub. `.cx`, `.cy` for rotating it about its centre."""
    pts = []
    for i in range(teeth * 2):
        ang = PI * i / teeth
        rr = r if i % 2 == 0 else r * 0.74
        pts.append([x + rr * np.cos(ang), y + rr * np.sin(ang), 0])
    body = Polygon(*pts, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
    hub = Circle(radius=r * 0.27, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    g = VGroup(body, hub)
    g.cx, g.cy = x, y
    return g


class B42_StrongestAndTools(Scene):
    """One long 65 GB bar is ringed as the strongest on one card; two model cards: the stamped one runs the call, the other prints it."""
    def construct(self):
        x0, sc, by = -2.2, 0.1014, 1.55
        ex = lambda gb: x0 + gb * sc
        rl, rt, rn = pC_ruler(x0, sc, 70, 10, 0.85)
        gb = T("GB", 34).move_to([ex(70) + 0.8, 0.23, 0])
        lab = pC_model_label("openai", "gpt-oss 120b", -6.05, by)
        bar = pC_blk(0, 0, 65 * sc, 0.7, BAR2, 4).move_to([ex(32.5), by, 0])
        n65 = pC_bar_num("65", ex(65), by)
        ring = RoundedRectangle(width=65 * sc + 0.4, height=1.1, corner_radius=0.35, color=TERRA, stroke_width=6).move_to([ex(32.5), by, 0])
        strong = T("strongest on one card", 36)
        strong.move_to([ex(65) + 0.2 - strong.width / 2, 2.62, 0])

        cy = -1.75
        lx, rx = -3.0, 3.0
        cards = [paper(lx, cy, w=4.4, h=2.7), paper(rx, cy, w=4.4, h=2.7)]
        blks = [pC_blk(0, 0, 1.1, 0.8, BAR2, 4).move_to([x - 1.45, cy + 0.2, 0]) for x in (lx, rx)]
        mlabs = [T("model", 32).move_to([x - 1.45, cy - 0.55, 0]) for x in (lx, rx)]
        stamp = pC_stamp("tools", lx + 0.5, cy + 0.85)
        gear = pC_gear(lx + 0.3, cy - 0.35, 0.58)
        ck = check(lx + 1.55, cy - 0.35, s=0.3, color=TERRA, w=12)
        ghost = DashedVMobject(RoundedRectangle(width=1.75, height=0.7, corner_radius=0.35, color=BAR1, stroke_width=4), num_dashes=22).move_to([rx + 0.5, cy + 0.85, 0])
        lines = [scribble(rx - 0.55, cy + 0.15 - 0.4 * i, 3.2 if i != 2 else 2.4, amp=0.09, sw=5) for i in range(3)]
        xm = x_mark(rx + 1.75, cy + 0.85, r=0.26, w=9)

        self.play(Create(rl), FadeIn(rt), FadeIn(rn), FadeIn(gb), run_time=0.6)
        # "the 120 billion GPT-OSS, about 65 gigabytes"
        hear(self, "120 billion", lead=0.3)
        self.play(FadeIn(lab), run_time=0.3)
        hear(self, "about 65", lead=0.3)
        self.play(GrowFromEdge(bar, LEFT), run_time=1.0)
        self.play(FadeIn(n65), run_time=0.2)
        # "is the strongest of these that fits on one card": the ring
        hear(self, "strongest", lead=0.4)
        self.play(Create(ring), FadeIn(strong), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(ring), run_time=0.3)
        # "check its page for the tools label": two model cards
        at(self, 8.05)
        self.play(FadeIn(cards[0]), FadeIn(cards[1]), FadeIn(blks[0]), FadeIn(blks[1]), FadeIn(mlabs[0]), FadeIn(mlabs[1]), run_time=0.4)
        hear(self, "tool's label", lead=0.35)
        self.play(GrowFromCenter(stamp), run_time=0.3)
        self.play(FadeIn(gear), run_time=0.2)
        self.play(Rotate(gear, angle=PI / 2, about_point=[gear.cx, gear.cy, 0]), run_time=0.6, rate_func=smooth)
        self.play(Create(ck), run_time=0.3)
        # "a model without tool support": the empty slot on the other card
        hear(self, "without tool support", lead=0.1)
        self.play(Create(ghost), run_time=0.4)
        # "prints tool calls as plain text instead of running them": the call spills across the card, then the cross
        hear(self, "calls as plain", lead=0.5)
        for ln in lines:
            self.play(Create(ln), run_time=0.42, rate_func=linear)
        hear(self, "instead of running", lead=0.2)
        self.play(Create(xm), run_time=0.3)
        done(self)


def pC_caution(x, y, r=0.3):
    """A caution mark: a kraft triangle, an ink outline, a bar and a dot."""
    tri = Polygon([x, y + r, 0], [x - r * 0.95, y - r * 0.6, 0], [x + r * 0.95, y - r * 0.6, 0],
                  fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
    bar = Line([x, y + r * 0.35, 0], [x, y - r * 0.1, 0], color=INK, stroke_width=5)
    dot = Dot([x, y - r * 0.38, 0], radius=0.045, color=INK)
    return VGroup(tri, bar, dot)


class B43_OneGpuPerJob(Scene):
    """A GPU-partition rack with five typed slots; the request picks h200 (about 140 GB), every model slots in with room left;
    the older v100 and t4 slots get a caution mark."""
    def construct(self):
        fx, fy, fw, fh = -1.25, 0.29, 4.6, 4.1
        tw, th = 4.0, 0.58
        rows = [("v100-sxm2", 1.85), ("v100-pcie", 1.07), ("t4", 0.29), ("a100", -0.49), ("h200", -1.27)]
        frame = Rectangle(width=fw, height=fh, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([fx, fy, 0])
        trays = VGroup(*[Rectangle(width=tw, height=th, fill_color=GHOST, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([fx, y, 0]) for _, y in rows])
        names = VGroup(*[M(n, 32).move_to([-3.85, y, 0]) for n, y in rows])
        for m in names:
            m.shift(RIGHT * (-3.85 - m.get_right()[0]))
        gp = T("gpu partition", 40)
        gp.move_to([-3.55 + gp.width / 2, 2.8, 0])
        yh = -1.27
        req = chip("--gres=gpu:h200:1", 3.85, yh, w=4.55, mono=True, size=34)
        ring = RoundedRectangle(width=tw + 0.2, height=th + 0.2, corner_radius=0.12, color=TERRA, stroke_width=6).move_to([fx, yh, 0])
        tag = T("about 140 GB", 34).move_to([3.85, -2.1, 0])
        left = fx - tw / 2
        per = tw / 140.0
        sizes = [14, 19, 23, 65]
        mods = [Rectangle(width=g * per, height=0.44, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([left + 0.06 + g * per / 2, yh, 0]) for g in sizes]
        mlab = T("model", 34).move_to([-2.45, -2.2, 0])
        room_x0 = left + 0.06 + 65 * per + 0.2
        room_w = fx + tw / 2 - 0.06 - room_x0
        room = DashedVMobject(Rectangle(width=room_w, height=0.44, color=BAR1, stroke_width=4), num_dashes=24).move_to([room_x0 + room_w / 2, yh, 0])
        rlab = T("context", 34).move_to([room_x0 + room_w / 2, -2.2, 0])
        cautions = [pC_caution(1.45, y) for y in (1.85, 1.07, 0.29)]
        clab = T("may fall back to CPU", 34)
        clab.move_to([1.95 + clab.width / 2, 1.07, 0])
        lg_page = paper(5.15, 2.3, w=1.2, h=1.3)
        lg_lines = scribbles_on(lg_page, n=3, inset=0.22, gap=0.3)
        lg_lab = T("log", 36).move_to([3.7, 2.3, 0])
        pulse = RoundedRectangle(width=4.55 + 0.3, height=1.1, corner_radius=0.45, color=TERRA, stroke_width=6).move_to([3.85, yh, 0])

        # "The GPU partition": the rack with its five typed slots
        self.play(FadeIn(gp), FadeIn(frame), FadeIn(trays), FadeIn(names), run_time=0.6)
        # "gives one GPU per job": the request chip
        hear(self, "per job", lead=0.5)
        self.play(FadeIn(req), run_time=0.4)
        # "so stay inside one card": the request picks the h200 slot
        hear(self, "inside one card", lead=0.3)
        self.play(Create(ring), run_time=0.45)
        self.wait(0.4)
        self.play(FadeOut(ring), run_time=0.3)
        # "an H200 has about 140 GB"
        hear(self, "about 140", lead=0.25)
        self.play(FadeIn(tag), run_time=0.3)
        # "every model on that list fits": each block slots in with room left
        hear(self, "every model", lead=0.15)
        self.play(GrowFromEdge(mods[0], LEFT), FadeIn(mlab), run_time=0.3)
        hear(self, "on that list", lead=0.1)
        self.play(FadeOut(mods[0]), run_time=0.1)
        self.play(GrowFromEdge(mods[1], LEFT), run_time=0.3)
        self.play(FadeOut(mods[1]), run_time=0.1)
        self.play(GrowFromEdge(mods[2], LEFT), run_time=0.3)
        # "with room for a large context": the biggest model, then the room it leaves
        hear(self, "room", lead=0.0)
        self.play(FadeOut(mods[2]), run_time=0.1)
        self.play(GrowFromEdge(mods[3], LEFT), run_time=0.35)
        hear(self, "large context", lead=0.0)
        self.play(Create(room), FadeIn(rlab), run_time=0.5)
        # "Older cards like V100 and T4 may fall back to the processor"
        hear(self, "V100", lead=0.25)
        self.play(GrowFromCenter(cautions[0]), GrowFromCenter(cautions[1]), run_time=0.35)
        hear(self, "T4", lead=0.2)
        self.play(GrowFromCenter(cautions[2]), run_time=0.3)
        hear(self, "may fall back", lead=0.15)
        self.play(FadeIn(clab), run_time=0.4)
        # "so check the log": a log page
        hear(self, "check the log", lead=0.2)
        self.play(FadeIn(lg_page), FadeIn(lg_lines), FadeIn(lg_lab), run_time=0.4)
        # "and ask for a newer type": the request chip is ringed again
        hear(self, "ask for a newer", lead=0.2)
        self.play(Create(pulse), run_time=0.5)
        done(self)


class B44_ContextKnobs(Scene):
    """Two cache blocks on a memory ruler (65,536 and a taller 131,072); the q8_0 knob turns and both blocks halve."""
    def construct(self):
        base = -2.6
        rx = -5.5
        ruler = Line([rx, base, 0], [rx, 2.5, 0], color=INK, stroke_width=6)
        ticks = VGroup(*[Line([rx, base + 0.52 * i, 0], [rx + 0.28, base + 0.52 * i, 0], color=INK, stroke_width=6) for i in range(1, 10)])
        mem = T("memory", 34).move_to([-6.1 + 0.65, 2.85, 0])
        ground = Line([rx, base, 0], [0.3, base, 0], color=INK, stroke_width=6)
        b1 = pC_blk(-3.9, base, 1.6, 1.6, BAR2, 4)
        b2 = pC_blk(-1.7, base, 1.6, 3.2, BAR2, 4)
        n1 = T("65,536", 38).move_to([-3.9, -3.0, 0])
        n2 = T("131,072", 38).move_to([-1.7, -3.0, 0])
        floor = chip("floor", -3.9, -0.45, size=34)
        h200 = chip("h200", -1.7, 1.2, mono=True, size=34)
        kb = Circle(radius=0.95, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([3.0, 1.55, 0])
        kp = Line([3.0, 1.55, 0], [3.0, 1.55 + 0.6, 0], color=INK, stroke_width=8)
        kd = Dot([3.0, 1.55 + 0.6, 0], radius=0.14, color=TERRA)
        knob = VGroup(kb, kp, kd)
        klab = M("OLLAMA_KV_CACHE_TYPE=q8_0", 32).move_to([3.0, 0.2, 0])
        g1 = DashedVMobject(Rectangle(width=1.6, height=1.6, color=BAR1, stroke_width=5), num_dashes=36).move_to([-3.9, base + 0.8, 0])
        g2 = DashedVMobject(Rectangle(width=1.6, height=3.2, color=BAR1, stroke_width=5), num_dashes=60).move_to([-1.7, base + 1.6, 0])
        s1 = pC_blk(-3.9, base, 1.6, 0.8, BAR2, 4)
        s2 = pC_blk(-1.7, base, 1.6, 1.6, BAR2, 4)
        cost = chip("small quality cost", 3.0, -1.35, size=34)

        self.play(Create(ruler), FadeIn(ticks), Create(ground), FadeIn(mem), run_time=0.6)
        # "sixty-five thousand is the floor for coding agents"
        hear(self, "65", lead=0.2)
        self.play(GrowFromEdge(b1, DOWN), run_time=0.7)
        self.play(FadeIn(n1), run_time=0.2)
        hear(self, "floor", lead=0.2)
        self.play(FadeIn(floor), run_time=0.3)
        # "on an H200 you can raise it": the taller block
        hear(self, "H200", lead=0.15)
        self.play(FadeIn(h200), run_time=0.3)
        hear(self, "raise it", lead=0.45)
        self.play(GrowFromEdge(b2, DOWN), run_time=0.8)
        self.play(FadeIn(n2), run_time=0.2)
        # "if memory is tight": the knob and its setting
        hear(self, "If memory", lead=0.1)
        self.play(FadeIn(knob), FadeIn(klab), run_time=0.4)
        # "storing the cache at 8 bits": the knob turns
        hear(self, "8 bits", lead=0.3)
        self.play(Rotate(knob, angle=-PI / 2, about_point=[3.0, 1.55, 0]), run_time=0.5, rate_func=smooth)
        # "roughly halves its size": both blocks halve, the old height stays as a dashed outline
        hear(self, "halves", lead=0.1)
        self.play(Create(g1), Create(g2), Transform(b1, s1), Transform(b2, s2), run_time=0.7)
        # "at a small cost in quality"
        hear(self, "small cost", lead=0.15)
        self.play(GrowFromCenter(cost), run_time=0.35)
        done(self)
