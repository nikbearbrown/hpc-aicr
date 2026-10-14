# ═════════════════════════════ PART C — B70 B72 B75 B77 B78 (Act VII) ═════════════════════════════
def pC_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pC_poly(pts, color=INK, w=6):
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_as_corners([[p[0], p[1], 0] for p in pts])
    return m


def pC_page(x, y, w=1.3, h=1.7):
    pg = Rectangle(width=w, height=h, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    ls = VGroup(*[Line([x - w * 0.3, y + h * 0.3 - 0.3 * i, 0], [x + w * 0.3, y + h * 0.3 - 0.3 * i, 0], color=BAR2, stroke_width=5) for i in range(3)])
    return VGroup(pg, ls)


class B70_CommitBeforeSubmit(Scene):
    """Commit, submit, queue, run; a thread from the commit to the hash in the job log."""
    def construct(self):
        title = pC_act_title("VII · Git On Slurm")
        base = Line([-5.8, 0.2, 0], [5.8, 0.2, 0], color=BAR1, stroke_width=5)
        disc = pA_disc(-5.0, 0.2, 0.45)
        c_commit = chip("commit first", -4.2, 1.55, size=34)
        sb = chip("sbatch", -1.3, 1.55, mono=True, size=32)
        tick = Line([-2.4, 0.2, 0], [-2.4, 0.85, 0], color=INK, stroke_width=7)
        queue = Rectangle(width=3.0, height=0.5, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([-0.9, 0.2, 0])
        qlab = T("queue", 34).move_to([-0.9, -0.55, 0])
        job = Rectangle(width=2.0, height=0.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([2.1, 0.2, 0])
        jlab = T("job runs", 34).move_to([2.1, -0.65, 0])
        page = pC_page(5.0, 0.2, 1.3, 1.7)
        logchip = chip("d9c1f37", 4.9, 1.75, mono=True, size=30)
        thread = pC_poly([(-5.0, -0.35), (-5.0, -1.7), (5.0, -1.7), (5.0, -0.8)], INK, 6)
        tlab = T("same commit", 34).move_to([0.0, -2.35, 0])
        hlab = T("hash in the log", 34).move_to([4.2, 2.7, 0])
        self.play(FadeIn(title), Create(base), run_time=0.5)
        hear(self, "runs later", lead=0.9)
        self.play(FadeIn(queue), FadeIn(qlab), FadeIn(job), FadeIn(jlab), run_time=0.6)
        hear(self, "Commit before", lead=0.2)
        self.play(FadeIn(disc), FadeIn(c_commit), run_time=0.4)
        hear(self, "submit", lead=0.1)
        self.play(Create(tick), FadeIn(sb), run_time=0.4)
        hear(self, "traces to one commit", lead=0.4)
        self.play(Create(thread), FadeIn(tlab), run_time=0.8)
        hear(self, "print that commit", lead=0.2)
        self.play(FadeIn(page), FadeIn(logchip), FadeIn(hlab), run_time=0.5)
        done(self)


class B72_RealPartitions(Scene):
    """Explorer: short* and sharing; AICR: cpu*; 'compute' crossed out; sinfo."""
    def construct(self):
        ex = T("Explorer", 38).move_to([-3.1, 2.1, 0])
        ai = T("AICR", 38).move_to([3.2, 2.1, 0])
        iso1 = Iso(-3.55, -0.2, 0.7)
        rk1, lt1 = explorer_rack(iso1)
        iso2 = Iso(2.7, -0.55, 0.55)
        rk2, lt2 = aicr_rack(iso2)
        p1 = chip("short*   2-00:00:00", -3.1, -1.5, mono=True, size=30)
        p2 = chip("sharing  1:00:00", -3.1, -2.4, mono=True, size=30)
        p3 = chip("cpu*     1-00:00:00", 3.2, -1.5, mono=True, size=30)
        comp = chip("compute", 0.0, 2.9, mono=True, size=30)
        xm = x_mark(1.9, 2.9, r=0.4, w=9)
        sinfo = chip("sinfo", 3.2, -2.5, mono=True, size=32)
        star = T("* default", 32).move_to([-3.1, -3.15, 0])
        hear(self, "Use a name from", lead=0.2)
        self.play(FadeIn(comp), Create(xm), run_time=0.4)
        hear(self, "on Explorer", lead=0.3)
        self.play(FadeIn(ex), FadeIn(rk1), FadeIn(lt1), run_time=0.4)
        self.play(FadeIn(p1), run_time=0.3)
        hear(self, "sharing", lead=0.2)
        self.play(FadeIn(p2), FadeIn(star), run_time=0.3)
        hear(self, "On A-I-C-R|AICR|A I C R", lead=0.3)
        self.play(FadeIn(ai), FadeIn(rk2), FadeIn(lt2), run_time=0.4)
        self.play(FadeIn(p3), run_time=0.3)
        hear(self, "Check sinfo", lead=0.2)
        self.play(FadeIn(sinfo), run_time=0.3)
        done(self)


class B75_QueueWindow(Scene):
    """sbatch at commit A; an edit during the queue makes B; the job starts at B and logs B's hash."""
    def construct(self):
        base = Line([-5.8, 1.2, 0], [5.8, 1.2, 0], color=BAR1, stroke_width=5)
        sb = chip("sbatch", -4.2, 2.3, mono=True, size=32)
        tick = Line([-4.2, 1.2, 0], [-4.2, 1.85, 0], color=INK, stroke_width=7)
        queue = Rectangle(width=4.6, height=0.5, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([-1.8, 1.2, 0])
        qlab = T("queue: hours", 34).move_to([-1.8, 0.55, 0])
        da = pA_disc(-4.2, -1.1, 0.42)
        ha = pA_hash("a3f8c21", -4.2, -1.95)
        edit = chip("edit", -1.0, 2.3, size=34)
        db = pA_disc(-1.0, -1.1, 0.42)
        hb = pA_hash("b7d2e14", -1.0, -1.95)
        arr = pA_arrow([-1.55, -1.1], [-3.65, -1.1], 7)
        start = Line([0.8, 1.2, 0], [0.8, 1.85, 0], color=INK, stroke_width=7)
        slab = T("job starts", 34).move_to([1.0, 2.3, 0])
        thread = pC_poly([(-0.6, -1.1), (0.8, -1.1), (0.8, 0.9)], INK, 6)
        log = chip("b7d2e14", 4.1, 2.1, mono=True, size=30)
        stamp = chip("not tested", 4.3, -1.5, size=34)
        self.play(Create(base), run_time=0.4)
        hear(self, "when the job starts", lead=0.6)
        self.play(FadeIn(da), FadeIn(ha), Create(tick), FadeIn(sb), run_time=0.5)
        hear(self, "queue for hours", lead=0.3)
        self.play(FadeIn(queue), FadeIn(qlab), run_time=0.5)
        hear(self, "Edit the script", lead=0.2)
        self.play(FadeIn(edit), FadeIn(db), FadeIn(hb), Create(arr), run_time=0.6)
        hear(self, "may run newer code", lead=0.3)
        self.play(Create(start), FadeIn(slab), Create(thread), run_time=0.5)
        hear(self, "newer hash", lead=0.2)
        self.play(FadeIn(log), FadeIn(stamp), run_time=0.4)
        done(self)


class B77_ThreeMoreSpots(Scene):
    """Three cards: dirty results block the next submit; two jobs, one checkout; a tag that stays in the checkout."""
    def construct(self):
        xs = [-4.3, 0.0, 4.3]
        cards = [Rectangle(width=3.9, height=4.3, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, 0.1, 0]) for x in xs]
        shadows = [Rectangle(width=3.9, height=4.3, fill_color=BOX_R, fill_opacity=1, stroke_width=0).move_to([x + 0.1, 0.0, 0]) for x in xs]
        labs = [T(t, 34).move_to([x, -1.65, 0]) for t, x in zip(["dirty results", "shared checkout", "tag stays put"], xs)]
        # card 1: a results page with a dirty dot; the sbatch arrow is barred
        pg = pC_page(-4.3, 1.1, 1.2, 1.5)
        dirty = Dot([-3.75, 1.7, 0], radius=0.15, color=TERRA)
        sb = chip("sbatch", -4.3, -0.45, mono=True, size=30)
        xm1 = x_mark(-2.8, -0.45, r=0.35, w=9)
        # card 2: two job boxes reaching into one checkout
        j1 = VGroup(Rectangle(width=0.9, height=0.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-0.9, 1.5, 0]))
        j2 = VGroup(Rectangle(width=0.9, height=0.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.9, 1.5, 0]))
        co = Rectangle(width=1.4, height=0.9, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.0, -0.3, 0])
        ar1 = pA_arrow([-0.8, 1.1], [-0.2, 0.2], 6)
        ar2 = pA_arrow([0.8, 1.1], [0.2, 0.2], 6)
        # card 3: a flag inside a rack; no arrow to GitHub until push
        iso3 = Iso(3.2, -0.5, 0.55)
        rk, lt = explorer_rack(iso3)
        fl = pA_flag(4.35, 0.55, 0.8)
        gh = logo_chip("github", 5.2, 1.9, h=0.9)
        push = pA_arrow([4.55, 1.0], [4.95, 1.45], 6)
        pl = chip("push", 3.5, 1.9, mono=True, size=30)
        hear(self, "Three more", lead=0.1)
        self.play(*[FadeIn(s) for s in shadows], *[FadeIn(c) for c in cards], run_time=0.5)
        hear(self, "results a run writes", lead=0.2)
        self.play(FadeIn(pg), FadeIn(dirty), FadeIn(labs[0]), run_time=0.4)
        hear(self, "next submit", lead=0.2)
        self.play(FadeIn(sb), Create(xm1), run_time=0.4)
        hear(self, "inside the job", lead=0.3)
        self.play(FadeIn(co), FadeIn(j1), FadeIn(j2), FadeIn(labs[1]), run_time=0.4)
        self.play(Create(ar1), Create(ar2), run_time=0.4)
        hear(self, "a tag made", lead=0.3)
        self.play(FadeIn(rk), FadeIn(lt), Create(fl), FadeIn(labs[2]), FadeIn(gh), run_time=0.6)
        hear(self, "pushes it", lead=0.3)
        self.play(FadeIn(pl), Create(push), run_time=0.4)
        done(self)


class B78_JobRecord(Scene):
    """Twelve record items; the header covers the first few; you add the rest."""
    def construct(self):
        items = ["commit and tag", "job and node", "start and end", "exact command", "parameters", "random seeds",
                 "input checksums", "software", "hardware", "container image", "output folder", "exit status"]
        xs = [-4.3, 0.0, 4.3]
        ys = [2.2, 0.85, -0.5, -1.85]
        pills, labels = [], []
        for i, t in enumerate(items):
            x, y = xs[i % 3], ys[i // 3]
            p = pill(x, y, 3.9, h=0.9, fill="#A39E94")
            lb = T(t, 34).move_to([x, y, 0])
            pills.append(p); labels.append(lb)
        dots = [Dot([xs[i % 3] - 1.7, ys[i // 3], 0], radius=0.13, color=TERRA) for i in range(3)]
        leg = T("printed by the header", 34).move_to([-3.2, -3.0, 0])
        ldot = Dot([-5.6, -3.0, 0], radius=0.13, color=TERRA)
        add = T("you add the rest", 34).move_to([3.4, -3.0, 0])
        hear(self, "A full job record", lead=0.2)
        self.play(*[FadeIn(p) for p in pills], run_time=0.5)
        order = [(0, "more than a commit"), (1, "job, node"), (2, "start and end"), (3, "exact command"), (4, "every parameter"), (5, "random seed"),
                 (6, "input paths"), (7, "software versions"), (8, "hardware"), (10, "output folder"), (11, "exit status")]
        for i, ph in order:
            hear(self, ph, lead=0.15)
            self.play(FadeIn(labels[i]), *([FadeIn(labels[9])] if i == 10 else []), run_time=0.2)
        hear(self, "The header prints", lead=0.2)
        self.play(*[FadeIn(d) for d in dots], FadeIn(leg), FadeIn(ldot), run_time=0.4)
        hear(self, "You add the rest", lead=0.1)
        self.play(FadeIn(add), *[p.animate.set_fill("#FFFFFF") for p in pills[3:]], run_time=0.5)
        done(self)
