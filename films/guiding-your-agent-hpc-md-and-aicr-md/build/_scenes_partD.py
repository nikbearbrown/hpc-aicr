# ═════════════════════════════ PART D — B44 B45 B59 B60 B61 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pD_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pD_bar(x0, y, frac, w=6.8, h=0.5, color=BAR1):
    """A jobstats-style bar: (track, fill). The fill grows from the left edge."""
    track = Rectangle(width=w, height=h, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x0 + w / 2, y, 0])
    fw = max(0.05, w * frac)
    fill = Rectangle(width=fw, height=h, fill_color=color, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x0 + fw / 2, y, 0])
    return track, fill


def pD_tick(x, y0, y1):
    return Line([x, y0, 0], [x, y1, 0], color=INK, stroke_width=7)


class B44_JobstatsTargets(Scene):
    """jobstats draws four bars and a time bar; the GPU bar is the filled one and two ticks mark 50 and 70."""
    def construct(self):
        x0, W = -2.4, 6.8
        rows = [("CPU utilisation", 2.55, 0.13, "13%"), ("CPU memory", 1.55, 0.25, "25%"),
                ("GPU utilisation", 0.2, 0.80, "80%"), ("GPU memory", -1.2, 0.17, "17%")]
        tag = M("jobstats", 36).move_to([-4.6, 3.05, 0])
        tracks, fills, labs, nums = [], [], [], []
        for name, y, f, n in rows:
            col = TERRA if name == "GPU utilisation" else BAR1
            tr, fl = pD_bar(x0, y, f, W, color=col)
            lb = T(name, 32)
            lb.move_to([-6.0 + lb.width / 2, y, 0])
            nm = T(n, 36).move_to([5.35, y, 0])
            tracks.append(tr); fills.append(fl); labs.append(lb); nums.append(nm)
        ttr, tfl = pD_bar(x0, -2.35, 55 / 480, W, color=INK)
        tlab = T("time", 32)
        tlab.move_to([-6.0 + tlab.width / 2, -2.35, 0])
        asked = T("8 h asked", 32).move_to([x0 + W - 0.9, -2.9, 0])
        ran = T("55 min ran", 32).move_to([x0 + 0.1 + 0.85, -2.9, 0])

        # "job stats": the command's name lands and the four empty tracks with their names
        hear(self, "job stats", lead=0.15)
        self.play(FadeIn(tag), *[FadeIn(t) for t in tracks], *[FadeIn(l) for l in labs], run_time=0.5)
        # "real example": the three quiet bars fill
        hear(self, "real example", lead=0.1)
        quiet = [0, 1, 3]
        self.play(*[GrowFromEdge(fills[i], LEFT) for i in quiet], *[FadeIn(nums[i]) for i in quiet], run_time=0.7)
        # "8 hours": the time bar and what was asked
        hear(self, "8 hours", lead=0.15)
        self.play(FadeIn(ttr), FadeIn(tlab), FadeIn(asked), run_time=0.4)
        # "ran 55 minutes": the short fill
        hear(self, "ran 55", lead=0.1)
        self.play(GrowFromEdge(tfl, LEFT), FadeIn(ran), run_time=0.5)
        # "GPU 80% busy": the terracotta bar fills
        hear(self, "GPU 80", lead=0.15)
        self.play(GrowFromEdge(fills[2], LEFT), run_time=0.7)
        self.play(FadeIn(nums[2]), run_time=0.2)
        # "over 70 ... acceptable"
        t70 = x0 + W * 0.7
        t50 = x0 + W * 0.5
        k70 = pD_tick(t70, 0.55, -0.1)
        n70 = T("70", 34).move_to([t70, 0.85, 0])
        acc = T("acceptable", 32).move_to([t70 + 1.3, -0.45, 0])
        hear(self, "over 70", lead=0.2)
        self.play(Create(k70), FadeIn(n70), run_time=0.4)
        hear(self, "is acceptable", lead=0.1)
        self.play(FadeIn(acc), run_time=0.3)
        # "under 50 is a problem"
        k50 = pD_tick(t50, 0.55, -0.1)
        n50 = T("50", 34).move_to([t50, 0.85, 0])
        prob = T("problem", 32).move_to([t50 - 0.85, -0.45, 0])
        hear(self, "under 50", lead=0.2)
        self.play(Create(k50), FadeIn(n50), run_time=0.4)
        hear(self, "is a problem", lead=0.15)
        self.play(FadeIn(prob), run_time=0.3)
        done(self)


def pD_card(x, y, w=3.6, h=4.0):
    return paper(x, y, w=w, h=h)


def pD_rule(lines, x, y, w=3.7, h=1.25):
    """A rule chip: white pill carrying two short lines."""
    shadow = pill(x + 0.08, y - 0.08, w, h=h, fill=BOX_L)
    body = pill(x, y, w, h=h)
    a = T(lines[0], 32)
    b = T(lines[1], 32)
    txt = VGroup(a, b).arrange(DOWN, buff=0.08).move_to([x, y, 0])
    g = VGroup(shadow, body, txt)
    return g


class B45_QuietLessons(Scene):
    """Three quiet failures, drawn as three cards; each ends in a rule chip."""
    def construct(self):
        cy = 0.75
        xs = [-4.1, 0.0, 4.1]
        cards = [pD_card(x, cy) for x in xs]
        # card 1: a model box, random dots inside, a 'loaded, no error' badge
        mbox = Rectangle(width=1.9, height=1.5, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([xs[0], cy + 0.5, 0])
        rng = np.random.RandomState(11)
        dots = VGroup(*[Dot([xs[0] + rng.uniform(-0.75, 0.75), cy + 0.5 + rng.uniform(-0.55, 0.55), 0], radius=0.07, color=INK) for _ in range(16)])
        badge = VGroup(pill(xs[0] + 0.05, cy - 0.65, 3.4, h=0.7, fill=PAGE_L), check(xs[0] - 1.4, cy - 0.65, s=0.16, w=6))
        blab = T("loaded, no error", 32).move_to([xs[0] + 0.3, cy - 0.65, 0])
        # card 2: a flat audio line between faint limits, a tiny peak
        top = Line([xs[1] - 1.4, cy + 1.2, 0], [xs[1] + 1.4, cy + 1.2, 0], color=BAR2, stroke_width=4)
        bot = Line([xs[1] - 1.4, cy - 0.2, 0], [xs[1] + 1.4, cy - 0.2, 0], color=BAR2, stroke_width=4)
        mid = cy + 0.5
        wave = VMobject(stroke_color=INK, stroke_width=7)
        wave.set_points_as_corners([[xs[1] - 1.4, mid, 0], [xs[1] - 0.2, mid, 0], [xs[1] - 0.1, mid + 0.08, 0],
                                    [xs[1], mid - 0.06, 0], [xs[1] + 0.1, mid, 0], [xs[1] + 1.4, mid, 0]])
        peak = M("4 of 32767", 32).move_to([xs[1], cy - 0.85, 0])
        # card 3: two files, the old one on a cache shelf, the new one beside it
        shelf = Line([xs[2] - 1.5, cy - 0.4, 0], [xs[2] - 0.2, cy - 0.4, 0], color=INK, stroke_width=10)
        oldp = paper(xs[2] - 0.85, cy + 0.25, w=1.0, h=1.3, fill=PAGE_L)
        oldl = scribbles_on(oldp, n=2, inset=0.22, gap=0.3)
        newp = paper(xs[2] + 0.85, cy + 0.25, w=1.0, h=1.3)
        newl = scribbles_on(newp, n=2, inset=0.22, gap=0.3)
        cache = T("cache", 32).move_to([xs[2] - 0.85, cy - 0.85, 0])
        same = T("same path", 32).move_to([xs[2] + 0.2, cy - 1.45, 0])
        served = chip("served", xs[2] - 0.6, cy + 1.45, w=1.7, size=30)
        r1 = pD_rule(("prove the", "weights loaded"), xs[0], -2.35)
        r2 = pD_rule(("gate every input", "with a number"), xs[1], -2.35)
        r3 = pD_rule(("give it a", "new name"), xs[2], -2.35)

        self.play(*[FadeIn(c) for c in cards], run_time=0.5)
        # "a checkpoint": the model box; "loaded without error": the badge; "random weights": the dots
        hear(self, "a checkpoint", lead=0.2)
        self.play(FadeIn(mbox), run_time=0.3)
        hear(self, "loaded without error", lead=0.3)
        self.play(FadeIn(badge), FadeIn(blab), run_time=0.4)
        hear(self, "random weights", lead=0.3)
        self.play(FadeIn(dots), run_time=0.5)
        # "an input clip so quiet": limits, then the flat line with its tiny peak
        hear(self, "an input clip", lead=0.2)
        self.play(FadeIn(top), FadeIn(bot), Create(wave), run_time=0.8)
        hear(self, "produced silence", lead=0.4)
        self.play(FadeIn(peak), run_time=0.3)
        # "a cached file": the old file on the shelf; "served": it is the one handed out; "replaced": the new file
        hear(self, "a cached file", lead=0.2)
        self.play(FadeIn(shelf), FadeIn(oldp), FadeIn(oldl), FadeIn(cache), run_time=0.5)
        hear(self, "served", lead=0.15)
        self.play(FadeIn(served), run_time=0.3)
        hear(self, "was replaced", lead=0.3)
        self.play(FadeIn(newp), FadeIn(newl), FadeIn(same), run_time=0.5)
        # the three rules
        hear(self, "prove the weights loaded", lead=0.2)
        self.play(FadeIn(r1, shift=UP * 0.2), run_time=0.4)
        hear(self, "gate every input", lead=0.2)
        self.play(FadeIn(r2, shift=UP * 0.2), run_time=0.4)
        hear(self, "give a replaced file", lead=0.2)
        self.play(FadeIn(r3, shift=UP * 0.2), run_time=0.4)
        done(self)


class B59_WhereToFindThem(Scene):
    """The repo address lands, then the skills folder opens into hpc/HPC.md and aicr/AICR.md."""
    def construct(self):
        title = pD_act_title("V · Using The Files")
        url = M("github.com/nikbearbrown/hpc-aicr", 32).move_to([0, 1.75, 0])
        under = Line([url.get_left()[0], 1.3, 0], [url.get_right()[0], 1.3, 0], color=TERRA, stroke_width=6)
        sk = M("skills/", 36).move_to([0, 0.45, 0])
        lx = [-3.0, 3.0]
        stem = Line([0, 0.05, 0], [0, -0.2, 0], color=INK, stroke_width=5)
        bar = Line([lx[0], -0.2, 0], [lx[1], -0.2, 0], color=INK, stroke_width=5)
        drops = [Line([x, -0.2, 0], [x, -0.5, 0], color=INK, stroke_width=5) for x in lx]
        subs = [M(s, 34).move_to([x, -0.85, 0]) for s, x in zip(["hpc/", "aicr/"], lx)]
        pgs = [paper(x, -1.95, w=1.3, h=1.55) for x in lx]
        gls = [scribbles_on(p, n=2, inset=0.22, gap=0.3) for p in pgs]
        names = [M(s, 30).move_to([x, -2.95, 0]) for s, x in zip(["HPC.md", "AICR.md"], lx)]

        self.play(FadeIn(title), run_time=0.4)
        hear(self, "free on GitHub", lead=0.2)
        self.play(FadeIn(url), Create(under), run_time=0.6)
        hear(self, "skills folder", lead=0.3)
        self.play(FadeIn(sk), run_time=0.3)
        self.play(Create(stem), Create(bar), *[Create(d) for d in drops], run_time=0.4)
        hear(self, "in the hpc folder", lead=0.2)
        self.play(FadeIn(subs[0]), FadeIn(pgs[0]), FadeIn(gls[0]), FadeIn(names[0]), run_time=0.5)
        hear(self, "in the aicr folder", lead=0.2)
        self.play(FadeIn(subs[1]), FadeIn(pgs[1]), FadeIn(gls[1]), FadeIn(names[1]), run_time=0.5)
        done(self)


class B60_ThreeSteps(Scene):
    """Three steps land left to right on a line: files in a folder, one line in the instructions, the rules said back."""
    def construct(self):
        title = pD_act_title("V · Using The Files")
        lx = [-4.2, 0.0, 4.2]
        line = Line([-5.6, -2.3, 0], [5.6, -2.3, 0], color=BAR2, stroke_width=8)
        dots = [Dot([x, -2.3, 0], radius=0.14, color=TERRA) for x in lx]
        caps = [T(s, 44).move_to([x, -2.9, 0]) for s, x in zip(["both files", "one line", "say back"], lx)]
        # step 1: a folder with two pages
        pg1 = paper(lx[0] - 0.7, 0.85, w=1.25, h=1.5)
        pg2 = paper(lx[0] + 0.7, 0.85, w=1.25, h=1.5)
        gl1, gl2 = scribbles_on(pg1, n=2, inset=0.22, gap=0.3), scribbles_on(pg2, n=2, inset=0.22, gap=0.3)
        back = Rectangle(width=3.0, height=1.5, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([lx[0], -0.1, 0])
        tab = Rectangle(width=1.1, height=0.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([lx[0] - 0.95, 0.75, 0])
        front = Rectangle(width=3.0, height=1.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([lx[0], -0.25, 0])
        f1 = M("HPC.md", 30).move_to([lx[0], -1.15, 0])
        f2 = M("AICR.md", 30).move_to([lx[0], -1.65, 0])
        folder_back = VGroup(tab, back)
        # step 2: an instructions page with one highlighted line
        ip = paper(lx[1], 0.55, w=2.3, h=2.7)
        rows = [1.45, 1.0, 0.55, 0.1]
        band = Rectangle(width=1.95, height=0.36, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([lx[1], rows[2], 0])
        scr = VGroup(*[scribble(lx[1] - 0.85, y, 1.7 if i != 3 else 1.0, sw=4, amp=0.09) for i, y in enumerate(rows)])
        mark = Dot([lx[1] - 1.0, rows[2], 0], radius=0.1, color=TERRA)
        n1 = M("CLAUDE.md", 30).move_to([lx[1], -1.15, 0])
        n2 = M("AGENTS.md", 30).move_to([lx[1], -1.65, 0])
        # step 3: Claude says the rules back
        claude = logo_chip("claude", lx[2] - 0.5, 1.9)
        bub = RoundedRectangle(corner_radius=0.3, width=3.0, height=1.3, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([lx[2] - 0.2, 0.2, 0])
        tail = Polygon([lx[2] - 1.0, 0.82, 0], [lx[2] - 0.4, 0.82, 0], [lx[2] - 0.7, 1.22, 0], fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
        cover = Line([lx[2] - 0.95, 0.83, 0], [lx[2] - 0.45, 0.83, 0], color=PAGE_TOP, stroke_width=8)
        rl = VGroup(*[VGroup(check(lx[2] - 1.15, 0.38 - 0.5 * i, s=0.13, w=5), scribble(lx[2] - 0.85, 0.38 - 0.5 * i, 1.5, sw=4)) for i in range(2)])
        bubble = VGroup(tail, bub, cover, rl)
        box = job_box(Iso(5.0, 1.15, 0.55), 0, 0, 0, s=0.9)

        self.play(FadeIn(title), FadeIn(line), run_time=0.4)
        # "put both files": the two pages slide into the folder, named in mono
        hear(self, "put both files", lead=0.15)
        self.play(FadeIn(folder_back), FadeIn(pg1), FadeIn(gl1), FadeIn(pg2), FadeIn(gl2), run_time=0.5)
        hear(self, "where your agent", lead=0.1)
        self.play(FadeIn(front), FadeIn(f1), FadeIn(f2), FadeIn(dots[0]), FadeIn(caps[0]), run_time=0.6)
        # "Add the one line": the instructions page, the one line gets its band
        hear(self, "Add the one line", lead=0.2)
        self.play(FadeIn(ip), FadeIn(scr), run_time=0.5)
        self.play(FadeIn(band), FadeIn(mark), FadeIn(dots[1]), FadeIn(caps[1]), run_time=0.4)
        scr.set_z_index(3); mark.set_z_index(3)
        hear(self, "claw md", lead=0.2)
        self.play(FadeIn(n1), run_time=0.3)
        hear(self, "agents md", lead=0.2)
        self.play(FadeIn(n2), run_time=0.3)
        # "ask the agent": Claude arrives
        hear(self, "ask the agent", lead=0.2)
        self.play(FadeIn(claude), FadeIn(dots[2]), FadeIn(caps[2]), run_time=0.5)
        # "say back which rules apply": the bubble with the rules
        hear(self, "say back", lead=0.1)
        self.play(FadeIn(bubble), run_time=0.5)
        hear(self, "which rules apply", lead=0.1)
        self.play(*[Indicate(r, color=INK, scale_factor=1.08) for r in rl], run_time=0.6)
        # "before it runs anything": only now does the command box show up, and it waits
        hear(self, "before it runs", lead=0.15)
        self.play(FadeIn(box), run_time=0.4)
        done(self)


class B61_WhatRulesCannotDo(Scene):
    """You hold the key at a closed gate with Claude waiting; the note lands on the gate; three labels follow."""
    def construct(self):
        you = professor_bear("1x1", 2.3, seed="B61", x=-4.4, y=0.5)
        ylab = T("you", 36).move_to([-4.4, -0.95, 0])
        key = key_obj(-3.55, -0.25, s=0.45)
        p1 = Rectangle(width=0.28, height=2.6, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-1.2, 0.5, 0])
        p2 = Rectangle(width=0.28, height=2.6, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.6, 0.5, 0])
        bar = Rectangle(width=1.5, height=0.3, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-0.3, 0.5, 0])
        lock = padlock(-0.3, 0.5, s=0.55)
        gate = VGroup(p1, p2, bar, lock)
        claude = logo_chip("claude", 2.5, 0.5)
        page = paper(5.2, 0.5, w=1.45, h=1.9)
        pl = scribbles_on(page, n=3, inset=0.25, gap=0.36)
        q = T("?", 64).move_to([5.2, 2.0, 0])
        note = chip("ask Research Computing once", -0.3, 2.35, size=32)
        w = 3.85
        sx = [-4.15, 0.0, 4.15]
        ghosts = [Rectangle(width=w, height=0.8, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([x, -2.3, 0]) for x in sx]
        st = [chip(s, x, -2.3, w=w, size=32) for s, x in zip(["from the sources", "from a real run", "our own judgment"], sx)]

        self.play(FadeIn(you), FadeIn(ylab), FadeIn(key), FadeIn(gate), run_time=0.5)
        # "do not replace judgment": Claude walks up and waits at the gate
        hear(self, "do not replace", lead=0.3)
        self.play(FadeIn(claude), run_time=0.5)
        # "policy page": a page with nothing on it to answer
        hear(self, "policy page", lead=0.4)
        self.play(FadeIn(page), FadeIn(pl), run_time=0.4)
        hear(self, "whether automated agents", lead=0.2)
        self.play(FadeIn(q), run_time=0.3)
        # "so the files say to ask Research Computing once": the note lands on the gate
        hear(self, "so the files", lead=0.0)
        self.play(FadeOut(page), FadeOut(pl), FadeOut(q), run_time=0.2)
        note.shift(UP * 0.8)
        self.add(note)
        self.play(note.animate.shift(DOWN * 0.8), run_time=0.5, rate_func=smooth)
        # "every claim is labelled": three empty slots, then the three stamps
        hear(self, "every claim", lead=0.2)
        self.play(*[FadeIn(g) for g in ghosts], run_time=0.4)
        hear(self, "from the sources", lead=0.2)
        self.play(FadeIn(st[0], scale=1.25), run_time=0.35)
        hear(self, "from a real run", lead=0.2)
        self.play(FadeIn(st[1], scale=1.25), run_time=0.35)
        hear(self, "our own judgment", lead=0.2)
        self.play(FadeIn(st[2], scale=1.25), run_time=0.35)
        done(self)
