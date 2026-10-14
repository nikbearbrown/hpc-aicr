# ═════════════════════════════ PART B — B40 B44 B50 B60 ═════════════════════════════
def pB_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pB_card(lines, x, y, w, size=32, h=None):
    """An outline-free white card carrying one or two serif lines."""
    h = h or (0.5 + 0.5 * len(lines))
    sh = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
    cd = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    labs = VGroup(*[T(s, size) for s in lines]).arrange(DOWN, buff=0.18).move_to([x, y, 0])
    g = VGroup(sh, cd, labs)
    g.card = cd
    return g


class B40_RunInspectCommit(Scene):
    """A four-step loop with a rider dot; a flag plants on the commit step; code and result slide into it."""
    def construct(self):
        title = pB_act_title("IV · Save And Inspect")
        top = chip("change a value", 0.0, 2.2, size=34)
        right = chip("run", 3.6, 0.2, size=34)
        bot = chip("inspect", 0.0, -1.9, size=34)
        left = chip("commit", -3.4, 0.2, size=34)
        a1 = pA_arrow([1.9, 1.85], [3.2, 0.7], 7)
        a2 = pA_arrow([3.4, -0.3], [1.3, -1.6], 7)
        a3 = pA_arrow([-1.3, -1.6], [-3.1, -0.3], 7)
        a4 = pA_arrow([-3.6, 0.7], [-1.9, 1.85], 7)
        rider = Dot([0.0, 1.55, 0], radius=0.16, color=TERRA)
        code = chip("code", -5.0, 1.5, size=34)
        res = chip("result", -5.0, 2.45, size=34)
        flag = pA_flag(-4.9, -2.3, 1.2)
        tag = T("tag", 36).move_to([-3.9, -1.6, 0])
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "change a value", lead=0.2)
        self.play(FadeIn(top), run_time=0.3)
        hear(self, "run the script", lead=0.2)
        self.play(Create(a1), FadeIn(right), run_time=0.4)
        hear(self, "look at the output", lead=0.2)
        self.play(Create(a2), FadeIn(bot), run_time=0.4)
        hear(self, "then commit", lead=0.2)
        self.play(Create(a3), FadeIn(left), run_time=0.4)
        hear(self, "code and the result", lead=0.2)
        self.play(FadeIn(code), FadeIn(res), run_time=0.3)
        self.play(code.animate.move_to([-3.4, 0.2, 0]).set_opacity(0), res.animate.move_to([-3.4, 0.2, 0]).set_opacity(0), run_time=0.5)
        hear(self, "Repeat", lead=0.1)
        self.add(rider)
        self.play(MoveAlongPath(rider, Polygon([0.0, 1.55, 0], [2.9, 0.2, 0], [0.0, -1.3, 0], [-2.7, 0.2, 0], [0.0, 1.55, 0], stroke_width=0)), Create(a4), run_time=1.6, rate_func=linear)
        self.play(FadeOut(rider), run_time=0.15)
        hear(self, "tag the commit", lead=0.3)
        self.play(Create(flag), FadeIn(tag), run_time=0.5)
        done(self)


class B44_GoodCommits(Scene):
    """The 'and' message crossed out beside the one-change message; six message types; one typed example."""
    def construct(self):
        bad = pB_card(["fixed stuff and added new", "feature and changed config"], -3.0, 2.2, 5.4)
        xm = x_mark(0.2, 2.2, r=0.4, w=10)
        good = pB_card(["Fix off-by-one in", "loop bounds"], 3.2, 2.2, 4.6)
        ck = check(5.55, 2.2, s=0.3, w=9)
        types = VGroup(*[chip(t, 0, 0, size=32) for t in ["feat", "fix", "data", "analysis", "docs", "config"]]).arrange(RIGHT, buff=0.25).move_to([0.0, 0.3, 0])
        ex = plaque("analysis(fig3): reproduce\nwith corrected normalization".split("\n")[0], 0, -1.7, w=8.8, h=1.7, size=32)
        ex2 = M("with corrected normalization", 32).move_to([0.0, -2.05, 0])
        ex.label.move_to([0.0, -1.35, 0])
        ghosts = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.4, width=1.6, height=0.8, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x, 0.3, 0]), num_dashes=24) for x in [-4.8, -2.9, -1.0, 1.1, 3.1, 4.9]])
        gex = DashedVMobject(Rectangle(width=8.8, height=1.7, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([0.0, -1.7, 0]), num_dashes=48)
        self.add(ghosts, gex)
        hear(self, "One logical change", lead=0.3)
        self.play(FadeIn(bad), FadeIn(good), run_time=0.5)
        hear(self, "the word and", lead=0.3)
        self.play(Create(xm), run_time=0.35)
        hear(self, "make two commits", lead=0.3)
        self.play(Create(ck), run_time=0.3)
        hear(self, "consistent message style", lead=0.3)
        self.play(FadeOut(ghosts), LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in types], lag_ratio=0.2), run_time=1.3)
        hear(self, "reads like a change log", lead=0.3)
        self.play(FadeOut(gex), FadeIn(ex), FadeIn(ex2), run_time=0.5)
        done(self)


class B50_BranchOff(Scene):
    """Main as it stands; a branch forks and gets its own commits; main stays untouched."""
    def construct(self):
        title = pB_act_title("V · Branches And Merges")
        xs = [-4.4, -1.8, 0.8]
        discs = [pA_disc(x, 1.0, 0.5) for x in xs]
        arrows = [pA_arrow([xs[i] - 0.6, 1.0], [xs[i - 1] + 0.6, 1.0], 7) for i in (1, 2)]
        main = chip("main", 0.8, 2.3, size=34)
        fork = Line([0.8, 0.5, 0], [2.6, -0.85, 0], color=INK, stroke_width=6)
        d4, d5 = pA_disc(2.6, -1.1, 0.5), pA_disc(5.0, -1.1, 0.5)
        a45 = pA_arrow([4.4, -1.1], [3.2, -1.1], 7)
        lab = chip("explore/fc-cutoff-1.5", 3.1, -2.5, mono=True, size=30)
        untouched = chip("main untouched", -3.0, -1.0, size=34)
        self.play(FadeIn(title), run_time=0.4)
        self.add(*discs, *arrows)
        hear(self, "A reviewer asks", lead=0.1)
        self.play(FadeIn(main), run_time=0.3)
        hear(self, "Make a branch", lead=0.3)
        self.play(Create(fork), FadeIn(d4), FadeIn(lab), run_time=0.6)
        hear(self, "parallel version", lead=0.3)
        self.play(FadeIn(d5), Create(a45), run_time=0.5)
        hear(self, "main untouched", lead=0.3)
        self.play(FadeIn(untouched), run_time=0.4)
        done(self)


class B60_FixedFlag(Scene):
    """A tag stays where it was planted while main slides forward with each new commit."""
    def construct(self):
        title = pB_act_title("VI · Tags And Time Travel")
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        discs = [pA_disc(x, 0.5, 0.5) for x in xs]
        arrows = [pA_arrow([xs[i] - 0.6, 0.5], [xs[i - 1] + 0.6, 0.5], 7) for i in range(1, 5)]
        main = chip("main", 0.0, 1.9, size=34)
        flag = pA_flag(0.0, -1.9, 1.1)
        tl = chip("v1.0-submission", 3.0, -1.4, mono=True, size=30)
        co = chip("git checkout v1.0-submission", -0.4, -2.85, mono=True, size=30)
        up = pA_arrow([-1.2, -2.35], [-0.2, -1.95], 6)
        self.play(FadeIn(title), run_time=0.4)
        self.add(discs[0], discs[1], discs[2], arrows[0], arrows[1])
        hear(self, "A tag is a flag", lead=0.1)
        self.play(FadeIn(main), Create(flag), FadeIn(tl), run_time=0.5)
        hear(self, "Branch names slide forward", lead=0.2)
        self.play(FadeIn(discs[3]), Create(arrows[2]), main.animate.move_to([2.2, 1.9, 0]), run_time=0.6)
        self.play(FadeIn(discs[4]), Create(arrows[3]), main.animate.move_to([4.4, 1.9, 0]), run_time=0.6)
        hear(self, "check that tag out", lead=0.3)
        self.play(FadeIn(co), Create(up), run_time=0.5)
        done(self)
