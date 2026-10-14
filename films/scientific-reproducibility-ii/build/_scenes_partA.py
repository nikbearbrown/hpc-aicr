# ═════════════════════════════ PART A — B10 B11 B12 B13 B14 B15 B20 B30 (shared helpers pA_*) ═════════════════════════════
# Cue times come from hear("spoken phrase"): measured word times in _ASR. Labels are 1-3 words; real text only in mono.
def pA_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pA_arrow(a, b, w=8):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], color=INK, stroke_width=w, buff=0, max_tip_length_to_length_ratio=0.5)


def pA_disc(x, y, r=0.5, page=True):
    """A commit disc: white disc, ink outline, a small outline-free page inside (the snapshot picture)."""
    d = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    g = VGroup(d)
    if page:
        pg = Rectangle(width=r * 0.78, height=r * 1.0, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
        ls = VGroup(*[Line([x - r * 0.26, y + r * (0.22 - 0.22 * i), 0], [x + r * 0.26, y + r * (0.22 - 0.22 * i), 0], color=BAR1, stroke_width=3) for i in range(3)])
        g.add(pg, ls)
    g.d = d
    return g


def pA_hash(s, x, y):
    return M(s, 32).move_to([x, y, 0])


def pA_flag(x, y, h=1.2):
    """A flag planted with its pole foot at (x, y): ink pole, terracotta pennant (no text on it)."""
    pole = Line([x, y, 0], [x, y + h, 0], color=INK, stroke_width=7)
    pen = Polygon([x, y + h, 0], [x + 0.62, y + h - 0.24, 0], [x, y + h - 0.48, 0], fill_color=TERRA, fill_opacity=1, stroke_width=0)
    g = VGroup(pole, pen)
    g.pole, g.pen = pole, pen
    return g


def pA_label_row(items, y, size=34):
    return [chip(t, x, y, size=size) for t, x in items]


# ───────────────────────────────────────────────────────────────────────────────────────────────
class B10_ReviewerAsks(Scene):
    """A reviewer's question; eight real file and folder names pile up; which made which?"""
    def construct(self):
        title = pA_act_title("I · Why Keep History")
        bear = professor_bear("1x1", 2.3, seed="B10", x=-4.6, y=-0.5)
        ask = chip("threshold?", -4.6, 1.55, size=36)
        names = ["filter.sh", "filter_v2.sh", "filter_final.sh", "filter_final_USE_THIS.sh",
                 "results_old/", "results_new/", "results_for_paper/", "results_for_paper_FINAL/"]
        chips = [chip(n, 2.3 + (0.25 if i % 2 else -0.25), 2.55 - 0.72 * i, mono=True, size=32) for i, n in enumerate(names)]
        # "Which script made which table?": a question pair ringed by a pulse
        q = T("?", 90).move_to([-1.2, 0.2, 0])
        self.play(FadeIn(title), FadeIn(bear), run_time=0.5)
        hear(self, "a reviewer asks", lead=0.2)
        self.play(FadeIn(ask, shift=DOWN * 0.2), run_time=0.4)
        hear(self, "Without version", lead=0.1)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in chips[:4]], lag_ratio=0.25), run_time=1.4)
        hear(self, "you guess", lead=0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in chips[4:]], lag_ratio=0.25), run_time=1.4)
        hear(self, "Which script", lead=0.1)
        self.play(FadeIn(q, scale=1.3), run_time=0.4)
        self.play(Indicate(chips[3], color=INK, scale_factor=1.05), run_time=0.6)
        done(self)


class B11_OneTimeline(Scene):
    """One script and a timeline: date/author/message on each change; flag, branch, undo."""
    def construct(self):
        script = chip("filter.sh", -4.2, 2.55, mono=True, size=34)
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        y0 = 0.6
        line = Line([-5.7, y0, 0], [5.7, y0, 0], color=INK, stroke_width=6)
        dots = [pA_disc(x, y0, 0.3, page=False) for x in xs]
        c_date, c_auth, c_msg = chip("date", -4.4, -0.6, size=34), chip("author", -4.4, -1.5, size=34), chip("message", -4.4, -2.4, size=34)
        flag = pA_flag(0.0, y0 + 0.3, 1.1)
        flab = T("figure 3", 34).move_to([1.2, 2.1, 0])
        branch = Line([-2.2, y0 - 0.3, 0], [1.2, -1.6, 0], color=INK, stroke_width=6)
        bdot = pA_disc(1.2, -1.6, 0.3, page=False)
        blab = T("experiment", 34).move_to([3.0, -1.6, 0])
        undo = pA_arrow([4.2, 1.5], [2.4, 1.5])
        ulab = T("undo", 34).move_to([3.3, 2.1, 0])
        self.play(FadeIn(script), Create(line), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.15), run_time=0.9)
        hear(self, "date", lead=0.2)
        self.play(FadeIn(c_date), run_time=0.25)
        hear(self, "an author", lead=0.15)
        self.play(FadeIn(c_auth), run_time=0.25)
        hear(self, "a message", lead=0.15)
        self.play(FadeIn(c_msg), run_time=0.25)
        hear(self, "mark the exact", lead=0.15)
        self.play(Create(flag), FadeIn(flab), run_time=0.5)
        hear(self, "own branch", lead=0.4)
        self.play(Create(branch), FadeIn(bdot), FadeIn(blab), run_time=0.6)
        hear(self, "undo", lead=0.3)
        self.play(Create(undo), FadeIn(ulab), run_time=0.5)
        done(self)


class B12_Snapshots(Scene):
    """The Git logo; three commit discs, each a full picture; arrows back to the parent."""
    def construct(self):
        git = logo_chip("git", -5.0, 2.3, h=1.3)
        xs = [-3.6, 0.0, 3.6]
        discs = [pA_disc(x, 0.3, 0.7) for x in xs]
        hashes = [pA_hash(h, x, -0.85) for h, x in zip(["a3f8c21", "b7d2e14", "d9c1f37"], xs)]
        arrows = [pA_arrow([xs[i] - 0.8, 0.3], [xs[i - 1] + 0.8, 0.3]) for i in (1, 2)]
        whole = T("whole picture", 36).move_to([0.0, 2.0, 0])
        par = T("parent", 34).move_to([1.8, 0.95, 0])
        hear(self, "called Git", lead=0.3)
        self.play(FadeIn(git), run_time=0.4)
        hear(self, "snapshots", lead=0.2)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in discs], lag_ratio=0.4), LaggedStart(*[FadeIn(h) for h in hashes], lag_ratio=0.4), run_time=1.3)
        hear(self, "full picture", lead=0.3)
        self.play(FadeIn(whole), run_time=0.3)
        hear(self, "linked to", lead=0.1)
        self.play(Create(arrows[0]), Create(arrows[1]), FadeIn(par), run_time=0.6)
        done(self)


class B13_BranchAndTag(Scene):
    """The same chain: main on the last commit; an experiment forks off; a flag on one commit."""
    def construct(self):
        xs = [-3.6, 0.0, 3.6]
        discs = [pA_disc(x, 0.8, 0.6) for x in xs]
        hashes = [pA_hash(h, x, -0.2) for h, x in zip(["a3f8c21", "b7d2e14", "d9c1f37"], xs)]
        arrows = [pA_arrow([xs[i] - 0.7, 0.8], [xs[i - 1] + 0.7, 0.8]) for i in (1, 2)]
        main = chip("main", 3.6, 2.15, size=34)
        fork = Line([0.45, 0.45, 0], [1.4, -1.5, 0], color=INK, stroke_width=6)
        d4 = pA_disc(1.4, -1.7, 0.45)
        h4 = pA_hash("e5a0b99", 1.4, -2.55)
        exp = chip("explore/idea", 4.2, -1.7, mono=True, size=32)
        flag = pA_flag(-3.6, 1.45, 1.0)
        v = T("v1.0", 34).move_to([-2.35, 2.2, 0])
        self.add(*discs, *hashes, *arrows)
        hear(self, "A branch", lead=0.2)
        self.play(FadeIn(main), run_time=0.3)
        hear(self, "an experiment", lead=0.3)
        self.play(Create(fork), FadeIn(d4), FadeIn(h4), run_time=0.6)
        self.play(FadeIn(exp), run_time=0.3)
        hear(self, "A tag", lead=0.2)
        self.play(Create(flag), FadeIn(v), run_time=0.5)
        done(self)


class B14_ThreePlaces(Scene):
    """Working tree, staging area, repository: a page travels on git add, then git commit."""
    def construct(self):
        xs = [-4.4, 0.0, 4.4]
        boxes = [Rectangle(width=2.9, height=2.3, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, 0.8, 0]) for x in xs]
        labs = [T(t, 36).move_to([x, -0.7, 0]) for t, x in zip(["working tree", "staging area", "repository"], xs)]
        page = Rectangle(width=0.8, height=1.0, fill_color="#FFFFFF", fill_opacity=1, stroke_width=0).move_to([xs[0], 0.8, 0])
        pl = VGroup(*[Line([xs[0] - 0.25, 0.8 + 0.2 - 0.2 * i, 0], [xs[0] + 0.25, 0.8 + 0.2 - 0.2 * i, 0], color=BAR1, stroke_width=3) for i in range(3)])
        pg = VGroup(page, pl)
        stack = VGroup(*[Rectangle(width=1.1, height=0.28, fill_color="#FFFFFF", fill_opacity=1, stroke_width=0).move_to([xs[2], 0.35 + 0.4 * i, 0]) for i in range(3)])
        add_c = chip("git add", -2.2, -2.2, mono=True, size=32)
        com_c = chip("git commit", 2.2, -2.2, mono=True, size=32)
        a1 = pA_arrow([-2.7, -1.75], [-2.1, -0.95], 6)
        a2 = pA_arrow([1.7, -1.75], [2.3, -0.95], 6)
        self.play(*[FadeIn(b) for b in boxes], run_time=0.5)
        hear(self, "working tree", lead=0.25)
        self.play(FadeIn(labs[0]), FadeIn(pg), run_time=0.4)
        hear(self, "staging area", lead=0.25)
        self.play(FadeIn(labs[1]), run_time=0.3)
        hear(self, "git add", lead=0.25)
        self.play(FadeIn(add_c), run_time=0.25)
        self.play(pg.animate.move_to([xs[1], 0.8, 0]), run_time=0.7)
        hear(self, "repository holds", lead=0.2)
        self.play(FadeIn(labs[2]), FadeIn(stack), run_time=0.4)
        hear(self, "git commit", lead=0.25)
        self.play(FadeIn(com_c), run_time=0.25)
        self.play(pg.animate.move_to([xs[2], 1.7, 0]).scale(0.7), run_time=0.7)
        done(self)


class B15_FourMoments(Scene):
    """Four rows: a research moment and its Git answer."""
    def construct(self):
        ys = [2.4, 0.8, -0.8, -2.4]
        situ = ["another value?", "postdoc leaves", "setting changed", "with the paper"]
        ans = ["a branch", "clone + README", "git diff HEAD~1", "a tag"]
        cues = ["reviewer asks", "postdoc", "cluster setting", "Publishing"]
        rows = []
        for y, s, a in zip(ys, situ, ans):
            l = chip(s, -3.6, y, size=38)
            ar = pA_arrow([-1.4, y], [-0.4, y], 7)
            r = chip(a, 2.0, y, mono=(a not in ("a branch", "a tag")), size=38)
            rows.append(VGroup(l, ar, r))
        gh = logo_chip("github", 5.3, ys[3], h=1.3)
        self.play(*[FadeIn(r[0]) for r in rows], *[FadeIn(r[1]) for r in rows], run_time=0.5)
        for row, cue in zip(rows, cues):
            hear(self, cue, lead=0.25)
            self.play(FadeIn(row[2], shift=LEFT * 0.2), Indicate(row[0], color=INK, scale_factor=1.04), run_time=0.5)
        hear(self, "GitHub", lead=0.2)
        self.play(FadeIn(gh), run_time=0.4)
        done(self)


class B20_TheExample(Scene):
    """A counts table flows through a MIN_COUNT funnel into a smaller summary table with UP, DOWN, NS."""
    def construct(self):
        cw, ch = 0.55, 0.5
        x0, y0 = -6.0, 1.3

        def table(xl, yt, ncols, nrows, hdr_fill=BOX_L):
            cells = VGroup()
            for r in range(nrows):
                for c in range(ncols):
                    f = hdr_fill if r == 0 else "#A39E94"
                    cells.add(Rectangle(width=cw - 0.05, height=ch - 0.05, fill_color=f, fill_opacity=1, stroke_width=0)
                              .move_to([xl + cw * c + cw / 2, yt - ch * r - ch / 2, 0]))
            return cells
        t1 = table(x0, y0, 7, 6)
        lab_c = T("control", 34).move_to([x0 + cw * 2.5, y0 + 0.4, 0])
        lab_t = T("treated", 34).move_to([x0 + cw * 5.5, y0 + 0.4, 0])
        lab_g = M("gene_id", 32).move_to([x0 + 1.0, y0 - ch * 6 - 0.4, 0])
        funnel = Polygon([-1.1, 1.3, 0], [1.1, 1.3, 0], [0.35, -0.6, 0], [-0.35, -0.6, 0], fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5)
        flab = M("MIN_COUNT", 32).move_to([0.0, -1.2, 0])
        sx0 = 2.6
        t2 = table(sx0, y0, 5, 4)
        stat = [chip(t, x, -1.6, size=32) for t, x in zip(["UP", "DOWN", "NS"], [2.0, 3.9, 5.5])]
        slab = T("summary", 34).move_to([sx0 + 1.4, y0 + 0.4, 0])
        d1 = Rectangle(width=0.9, height=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-3.2, 0.0, 0])
        d2 = d1.copy().move_to([-3.2, -0.5, 0])
        arr1 = pA_arrow([-1.95, 0.4], [-1.2, 0.4], 7)
        arr2 = pA_arrow([1.2, 0.4], [2.3, 0.4], 7)
        hear(self, "small R N A", lead=0.4)
        self.play(FadeIn(t1), run_time=0.5)
        hear(self, "one row per gene", lead=0.1)
        self.play(FadeIn(lab_g), run_time=0.3)
        hear(self, "three control", lead=0.2)
        self.play(FadeIn(lab_c), run_time=0.3)
        hear(self, "treated", lead=0.2)
        self.play(FadeIn(lab_t), run_time=0.3)
        hear(self, "drops low", lead=0.3)
        self.play(FadeIn(funnel), FadeIn(flab), Create(arr1), run_time=0.5)
        self.play(FadeIn(d1), FadeIn(d2), run_time=0.2)
        self.play(d1.animate.move_to([0.0, 0.5, 0]), d2.animate.move_to([0.0, 0.1, 0]), run_time=0.7)
        self.play(d2.animate.shift(DOWN * 2.2).set_opacity(0), run_time=0.5)
        hear(self, "writes a summary", lead=0.2)
        self.play(Create(arr2), FadeIn(t2), FadeIn(slab), run_time=0.5)
        self.play(*[FadeIn(s) for s in stat], run_time=0.4)
        done(self)


class B30_CodeNotResults(Scene):
    """Code goes into the repository, big data to storage, tokens never; the ignore page lists what to skip."""
    def construct(self):
        title = pA_act_title("III · What To Leave Out")
        box = Rectangle(width=2.9, height=2.1, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-4.3, 0.8, 0])
        blab = T("repository", 34).move_to([-4.3, -0.55, 0])
        script = VGroup(Rectangle(width=0.9, height=1.1, fill_color="#FFFFFF", fill_opacity=1, stroke_width=0),
                        *[Line([-0.28, 0.25 - 0.22 * i, 0], [0.28, 0.25 - 0.22 * i, 0], color=BAR1, stroke_width=3) for i in range(3)]).move_to([-4.3, 2.0, 0])
        slab = T("scripts", 34).move_to([-2.5, 2.0, 0])
        data = Rectangle(width=1.5, height=1.1, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-0.3, 1.3, 0])
        dlab = T("big data", 34).move_to([-0.3, 2.45, 0])
        iso = Iso(-0.9, -3.0, 0.7)
        rk, lt = explorer_rack(iso)
        stor = VGroup(rk, lt)
        slab2 = T("project storage", 34).move_to([2.0, -2.4, 0])
        down = pA_arrow([-0.3, 0.7], [-0.3, -0.6], 7)
        key = chip("tokens", -4.3, -1.9, size=34)
        xm = x_mark(-2.35, -1.9, r=0.3, w=9)
        page = Rectangle(width=1.7, height=2.1, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([4.5, 1.5, 0])
        pl = VGroup(*[Line([3.9, 2.2 - 0.38 * i, 0], [5.1 - (0.5 if i == 3 else 0), 2.2 - 0.38 * i, 0], color=BAR2, stroke_width=6) for i in range(4)])
        gi = chip(".gitignore", 4.5, -0.1, mono=True, size=32)
        skip = VGroup(*[pill(4.5, -1.2 - 0.62 * i, 2.4, h=0.46, fill=GHOST) for i in range(3)])
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "Track the code", lead=0.2)
        self.play(FadeIn(box), FadeIn(blab), FadeIn(script), FadeIn(slab), run_time=0.5)
        self.play(script.animate.move_to([-4.3, 0.8, 0]), run_time=0.6)
        hear(self, "Big raw data", lead=0.25)
        self.play(FadeIn(data), FadeIn(dlab), run_time=0.4)
        hear(self, "project storage", lead=0.3)
        self.play(Create(down), FadeIn(stor), FadeIn(slab2), run_time=0.5)
        hear(self, "passwords", lead=0.3)
        self.play(FadeIn(key), run_time=0.3)
        self.play(Create(xm), run_time=0.3)
        hear(self, "dot git ignore", lead=0.3)
        self.play(FadeIn(page), Create(pl), FadeIn(gi), run_time=0.5)
        self.play(FadeIn(skip), run_time=0.4)
        done(self)
