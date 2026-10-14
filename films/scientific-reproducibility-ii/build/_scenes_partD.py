# ═════════════════════════════ PART D — B83 B84 B85 (Act VIII) ═════════════════════════════
def pD_page(x, y, w=1.1, h=1.4, stroke=True):
    pg = Rectangle(width=w, height=h, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK if stroke else "#FFFFFF", stroke_width=4 if stroke else 0).move_to([x, y, 0])
    ls = VGroup(*[Line([x - w * 0.3, y + h * 0.28 - 0.28 * i, 0], [x + w * 0.3, y + h * 0.28 - 0.28 * i, 0], color=BAR2, stroke_width=5) for i in range(3)])
    return VGroup(pg, ls)


class B83_BigFilesNotebooks(Scene):
    """Big data stays in storage, Git keeps a manifest; notebook outputs lift off with nbstripout."""
    def construct(self):
        title_l = T("VIII · Daily Habits And Questions", 40)
        title_l.move_to([-6.1 + title_l.width / 2, 3.0, 0])
        git = logo_chip("git", -4.9, 1.9, h=1.2)
        box = Rectangle(width=2.6, height=1.7, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-4.2, 0.1, 0])
        man = pD_page(-4.2, 0.1, 0.8, 1.0, stroke=False)
        mlab = T("manifest", 34).move_to([-4.2, -1.2, 0])
        iso = Iso(-0.2, -1.2, 0.65)
        rk, lt = explorer_rack(iso)
        stor = T("storage", 34).move_to([1.6, -1.2, 0])
        data = Rectangle(width=1.1, height=0.8, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-1.9, 1.5, 0])
        dlab = T("big data", 34).move_to([-1.9, 2.2, 0])
        arr = pA_arrow([-2.8, 0.4], [-0.9, 0.4], 7)
        lfs = chip("Git LFS", -3.4, -2.55, mono=True, size=30)
        dvc = chip("DVC", -0.9, -2.55, mono=True, size=30)
        jup = logo_chip("jupyter", 2.6, 2.0, h=1.2)
        nb = pD_page(4.1, 0.3, 2.3, 3.0)
        outs = VGroup(*[Rectangle(width=1.5, height=0.3, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([4.1, 0.3 - 0.0 - 0.55 + 0.55 * i - 0.55, 0]) for i in range(3)])
        outs.move_to([4.1, -0.35, 0])
        nbs = chip("nbstripout", 4.0, -2.2, mono=True, size=30)
        jt = chip("Jupytext", 4.0, -3.0, mono=True, size=30)
        self.play(FadeIn(title_l), run_time=0.4)
        hear(self, "large datasets", lead=0.2)
        self.play(FadeIn(git), FadeIn(box), FadeIn(man), FadeIn(mlab), run_time=0.5)
        hear(self, "Not directly", lead=0.2)
        self.play(FadeIn(data), FadeIn(dlab), run_time=0.3)
        hear(self, "Git L F S", lead=0.3)
        self.play(FadeIn(lfs), run_time=0.25)
        hear(self, "D V C", lead=0.3)
        self.play(FadeIn(dvc), Create(arr), FadeIn(rk), FadeIn(lt), FadeIn(stor), run_time=0.5)
        self.play(data.animate.move_to([0.4, 0.45, 0]).scale(0.6), FadeOut(dlab), run_time=0.7)
        hear(self, "Jupyter notebooks", lead=0.2)
        self.play(FadeIn(jup), FadeIn(nb), FadeIn(outs), run_time=0.5)
        hear(self, "strip them", lead=0.3)
        self.play(FadeIn(nbs), outs.animate.shift(RIGHT * 0.0).set_opacity(0.0), run_time=0.7)
        hear(self, "Jupytext", lead=0.3)
        self.play(FadeIn(jt), run_time=0.3)
        done(self)


class B84_UndoSafely(Scene):
    """Amend swaps the last commit; revert adds an undo commit; reset --hard on a shared branch is crossed out."""
    def construct(self):
        xs = [-5.0, -3.0, -1.0]
        ys = [2.0, 0.3, -1.5]

        def chain(y):
            ds = [pA_disc(x, y, 0.42) for x in xs]
            ars = [pA_arrow([xs[i] - 0.5, y], [xs[i - 1] + 0.5, y], 6) for i in (1, 2)]
            return ds, ars
        c1, a1 = chain(ys[0]); c2, a2 = chain(ys[1]); c3, a3 = chain(ys[2])
        fix = pA_disc(-1.0, ys[0], 0.42)
        amend = chip("commit --amend", 3.4, ys[0], mono=True, size=30)
        d4 = pA_disc(1.0, ys[1], 0.42)
        ar4 = pA_arrow([0.5, ys[1]], [-0.5, ys[1]], 6)
        undo = CurvedArrow([1.0, ys[1] + 0.5, 0], [-1.0, ys[1] + 0.5, 0], angle=-1.0, color=INK, stroke_width=6)
        revert = chip("git revert", 3.9, ys[1], mono=True, size=30)
        reset = chip("git reset --hard", 3.4, ys[2], mono=True, size=30)
        xm = x_mark(0.3, ys[2], r=0.45, w=10)
        shared = T("shared branch", 34).move_to([-2.0, -2.45, 0])
        hear(self, "fix the last commit", lead=0.3)
        self.add(*c1, *a1)
        self.play(FadeOut(c1[2]), FadeIn(fix), FadeIn(amend), run_time=0.6)
        hear(self, "already shared", lead=0.3)
        self.add(*c2, *a2)
        self.play(FadeIn(d4), Create(ar4), FadeIn(revert), run_time=0.5)
        self.play(Create(undo), run_time=0.4)
        hear(self, "never run", lead=0.2)
        self.add(*c3, *a3)
        self.play(FadeIn(reset), FadeIn(shared), run_time=0.4)
        hear(self, "throws work away", lead=0.3)
        self.play(FadeOut(c3[2]), FadeOut(c3[1]), Create(xm), run_time=0.6)
        done(self)


class B85_ConflictsAndStash(Scene):
    """Conflict markers around two versions; keep one, add, commit; stash and pop."""
    def construct(self):
        page = Rectangle(width=4.8, height=3.4, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-3.4, 0.8, 0])
        m1 = M("<<<<<<<", 32).move_to([-4.6, 2.1, 0])
        v1 = Rectangle(width=3.0, height=0.45, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([-3.4, 1.5, 0])
        m2 = M("=======", 32).move_to([-4.6, 0.8, 0])
        v2 = Rectangle(width=3.0, height=0.45, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([-3.4, 0.2, 0])
        m3 = M(">>>>>>>", 32).move_to([-4.6, -0.5, 0])
        add = chip("git add", -4.7, -2.1, mono=True, size=30)
        com = chip("git commit", -1.9, -2.1, mono=True, size=30)
        drawer = Rectangle(width=3.0, height=1.5, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.6, 1.6, 0])
        half = pD_page(3.6, 0.0, 0.9, 1.1, stroke=False)
        stash = chip("git stash", 3.6, -1.0, mono=True, size=30)
        pop = chip("git stash pop", 3.6, -2.1, mono=True, size=30)
        self.play(FadeIn(page), FadeIn(drawer), FadeIn(stash), FadeIn(pop), run_time=0.4)
        hear(self, "same lines", lead=0.3)
        self.play(FadeIn(m1), FadeIn(v1), FadeIn(m2), FadeIn(v2), FadeIn(m3), run_time=0.6)
        hear(self, "keep the version", lead=0.3)
        self.play(FadeOut(v2), run_time=0.3)
        hear(self, "delete the markers", lead=0.2)
        self.play(FadeOut(m1), FadeOut(m2), FadeOut(m3), v1.animate.move_to([-3.4, 0.8, 0]), run_time=0.5)
        hear(self, "git add", lead=0.2)
        self.play(FadeIn(add), run_time=0.25)
        hear(self, "and commit", lead=0.2)
        self.play(FadeIn(com), run_time=0.25)
        hear(self, "git stash", lead=0.3)
        self.play(FadeIn(half), run_time=0.4)
        self.play(half.animate.move_to([3.6, 1.6, 0]).set_opacity(0.0), run_time=0.5)
        hear(self, "brings them back", lead=0.4)
        self.play(half.animate.move_to([3.6, 0.0, 0]).set_opacity(1.0), run_time=0.6)
        done(self)
