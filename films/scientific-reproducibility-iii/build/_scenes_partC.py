# ═════════════════════════════ PART C — B53 B62 B64 B72 B73 B74 B80 ═════════════════════════════


class B53_DockerRoute(Scene):
    """Dockerfile -> docker build -> image -> apptainer build -> .sif; a second branch pushes the image to a registry and pulls it."""
    def construct(self):
        self.add(pA_act_title("V · Building An Image"))
        pg = paper(-5.2, 0.6, w=1.3, h=1.6)
        pgl = M("Dockerfile", 26).move_to([-5.2, -0.55, 0])
        sc = scribbles_on(pg, n=3, inset=0.22, gap=0.3)
        hear(self, "Docker file", lead=0.1)
        self.play(FadeIn(pg), FadeIn(sc), FadeIn(pgl), run_time=0.4)
        a1 = pA_arrow([-4.5, 0.6, 0], [-3.85, 0.6, 0], w=5, tip=0.22)
        dk = logo_chip("docker", -2.9, 0.6, h=1.3)
        dkl = M("docker build", 26).move_to([-2.8, -0.5, 0])
        hear(self, "build the Docker image", lead=0.2)
        self.play(Create(a1), FadeIn(dk), FadeIn(dkl), run_time=0.45)
        a2 = pA_arrow([-2.0, 0.6, 0], [-1.4, 0.6, 0], w=5, tip=0.22)
        im = pA_box(-0.6, 0.6, 0.7)
        iml = T("image", 32).move_to([-0.6, -0.4, 0])
        self.play(Create(a2), FadeIn(im), FadeIn(iml), run_time=0.4)
        hear(self, "Docker builds the image", lead=0.1)
        self.play(dk.animate.scale(1.1), run_time=0.2)
        self.play(dk.animate.scale(1 / 1.1), run_time=0.2)
        hear(self, "Aptainer reads", lead=0.1)
        a3 = pA_arrow([0.2, 0.6, 0], [0.85, 0.6, 0], w=5, tip=0.22)
        ap = logo_chip("apptainer", 1.8, 0.6, h=1.3)
        apl = M("apptainer build", 26).move_to([1.8, -0.5, 0])
        self.play(Create(a3), FadeIn(ap), FadeIn(apl), run_time=0.45)
        a4 = pA_arrow([2.7, 0.6, 0], [3.7, 0.6, 0], w=5, tip=0.22)
        sif = pA_box(4.5, 0.6, 0.7)
        sifl = M(".sif", 30).move_to([4.5, -0.4, 0])
        hear(self, "writes the", lead=0.2)
        self.play(Create(a4), FadeIn(sif), FadeIn(sifl), run_time=0.45)
        hear(self, "push the image", lead=0.2)
        a5 = pA_arrow([-0.6, -0.9, 0], [-0.6, -1.5, 0], w=5, tip=0.22)
        cl = pA_cloud(-0.6, -2.2, 0.55)
        cll = T("registry", 32).move_to([-0.6, -3.15, 0])
        self.play(Create(a5), FadeIn(cl), FadeIn(cll), run_time=0.45)
        hear(self, "pull it on the cluster", lead=0.4)
        a6 = pA_arrow([0.5, -2.2, 0], [2.2, -2.2, 0], w=5, tip=0.25)
        pl = M("pull", 28).move_to([1.35, -1.75, 0])
        rk = pA_rack(3.6, -2.15, 0.7)
        self.play(Create(a6), FadeIn(pl), FadeIn(rk), run_time=0.5)
        done(self)


class B62_PinTheTag(Scene):
    """:latest follows a different image next month; a pinned tag keeps pointing at the same one; the pinned tag goes into the methods."""
    def construct(self):
        self.add(pA_act_title("VI · Getting An Image Onto The Cluster"))
        h1 = T("today", 36).move_to([-2.7, 2.1, 0])
        h2 = T("next month", 36).move_to([2.9, 2.1, 0])
        sep = DashedLine([0.1, 2.4, 0], [0.1, -1.6, 0], color=KRAFT_DEEP, stroke_width=4)
        self.play(FadeIn(h1), FadeIn(h2), Create(sep), run_time=0.4)

        def tagrow(y, tagtxt, x_tag, x_box, boxlabel, taped=True):
            t = chip(tagtxt, x_tag, y, mono=True, size=28)
            ar = pA_arrow([x_tag + t.width / 2 + 0.1, y, 0], [x_box - 0.9, y, 0], w=5, tip=0.22)
            bx = pA_box(x_box, y, 0.62, tape=taped)
            lb = T(boxlabel, 32).move_to([x_box, y - 0.75, 0])
            return t, ar, bx, lb

        hear(self, "latest points", lead=0.2)
        l1 = tagrow(1.15, ":latest", -4.6, -1.6, "A")
        p1 = tagrow(-0.55, ":4.5.0.0", -4.7, -1.6, "A")
        self.play(*[FadeIn(m) for m in l1], *[FadeIn(m) for m in p1], run_time=0.6)
        hear(self, "different image", lead=0.2)
        l2 = tagrow(1.15, ":latest", 1.4, 4.6, "B", taped=False)
        self.play(*[FadeIn(m) for m in l2], run_time=0.5)
        self.play(Create(x_mark(6.0, 1.15, r=0.25, w=9)), run_time=0.25)
        hear(self, "pinned tag keeps", lead=0.1)
        p2 = tagrow(-0.55, ":4.5.0.0", 1.5, 4.6, "A")
        self.play(*[FadeIn(m) for m in p2], run_time=0.5)
        self.play(Create(check(6.0, -0.55, s=0.25, color=TERRA, w=10)), run_time=0.3)
        hear(self, "methods", lead=0.4)
        pm = paper(-0.2, -2.45, w=1.9, h=1.2)
        pml = T("methods", 32).move_to([-2.0, -2.45, 0])
        self.play(FadeIn(pm), FadeIn(pml), run_time=0.3)
        tg = chip(":4.5.0.0", 1.5, -0.55, mono=True, size=28)
        self.add(tg)
        self.play(tg.animate.scale(0.8).move_to([-0.2, -2.45, 0]), run_time=0.6)
        done(self)


class B64_WhereToKeep(Scene):
    """Not in home (75 GB quota); in project space, the .sif and its .def side by side, committed, archived with the data."""
    def construct(self):
        self.add(pA_act_title("VI · Getting An Image Onto The Cluster"))
        home = pA_folder(-4.7, 0.9, 1.6, 1.0)
        hl = T("home", 36).move_to([-4.7, 0.0, 0])
        track = Rectangle(width=2.6, height=0.3, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([-4.7, -0.65, 0])
        fill = Rectangle(width=1.9, height=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.35 + 0.0, -0.65, 0]).align_to(track, LEFT)
        q = M("75 GB", 30).move_to([-4.7, -1.2, 0])
        hear(self, "not in home", lead=0.3)
        self.play(FadeIn(home), FadeIn(hl), FadeIn(track), run_time=0.4)
        self.play(FadeIn(fill), FadeIn(q), run_time=0.3)
        sif = pA_box(-2.3, 2.1, 0.7)
        sl = M(".sif", 28).move_to([-2.3, 1.3, 0])
        self.play(FadeIn(sif), FadeIn(sl), run_time=0.3)
        self.play(sif.animate.move_to([-3.5, 1.6, 0]), sl.animate.move_to([-3.5, 0.9, 0]), run_time=0.35)
        self.play(Create(x_mark(-2.4, 1.3, r=0.3, w=10)), run_time=0.25)
        hear(self, "Project space", lead=0.2)
        self.play(FadeOut(sif), FadeOut(sl), run_time=0.2)
        fol = pA_folder(2.0, 1.4, 2.4, 1.5)
        fl = M("containers/", 30).move_to([2.0, 0.3, 0])
        self.play(FadeIn(fol), FadeIn(fl), run_time=0.4)
        sif2 = pA_box(1.4, 1.4, 0.62)
        self.play(FadeIn(sif2), run_time=0.3)
        hear(self, "recipe", lead=0.2)
        df = paper(4.1, 1.4, w=0.95, h=1.15)
        dfs = scribbles_on(df, n=3, inset=0.18, gap=0.26)
        dfl = M(".def", 28).move_to([4.1, 0.3, 0])
        self.play(FadeIn(df), FadeIn(dfs), FadeIn(dfl), run_time=0.35)
        hear(self, "commit it", lead=0.2)
        gt = chip("git", 5.6, 1.4, mono=True, size=30)
        self.play(FadeIn(gt), run_time=0.3)
        hear(self, "archive the image", lead=0.2)
        arc = pA_folder(2.4, -1.8, 2.6, 1.2)
        arl = T("archive with data", 34).move_to([2.4, -2.85, 0])
        self.play(FadeIn(arc), FadeIn(arl), run_time=0.4)
        self.play(sif2.animate.scale(0.6).move_to([1.8, -1.8, 0]), df.animate.scale(0.6).move_to([3.2, -1.8, 0]), run_time=0.6)
        done(self)


class B72_RecordIt(Scene):
    """Tag, digest and recipe-plus-image are stamped into the notes; sha256sum shows the same file on both sides."""
    def construct(self):
        self.add(pA_act_title("VII · Habits That Keep It Honest"))
        notes = paper(-5.2, 0.2, w=1.9, h=2.7)
        nl = VGroup(*[scribble(-5.9, 1.2 - i * 0.4, 1.4 * (0.62 if i == 3 else 1.0), amp=0.11) for i in range(4)]); nl.rotate(notes.tilt, about_point=[-5.2, 0.2, 0]) if abs(notes.tilt) > 1e-3 else None
        nt = T("notes", 40).move_to([-5.2, 1.85, 0])
        self.play(FadeIn(notes), FadeIn(nl), FadeIn(nt), run_time=0.4)
        for txt, y, ph in (("tag", 1.0, "exact tag"), ("digest", 0.2, "the digest"), (".def + .sif", -0.6, "recipe plus")):
            hear(self, ph, lead=0.15)
            c = chip(txt, -2.2, y, mono=(txt != "tag" and txt != "digest"), size=38)
            self.play(FadeIn(c, shift=LEFT * 0.3), run_time=0.35)
        mine = pA_box(1.1, 1.2, 0.85)
        ml = T("mine", 40).move_to([1.1, 0.1, 0])
        theirs = pA_box(5.1, 1.2, 0.85)
        tl = T("theirs", 40).move_to([5.1, 0.1, 0])
        hear(self, "A checksum", lead=0.1)
        self.play(FadeIn(mine), FadeIn(ml), FadeIn(theirs), FadeIn(tl), run_time=0.4)
        cs = chip("sha256sum myimage.sif", 3.1, -1.3, mono=True, size=34)
        self.play(FadeIn(cs), run_time=0.3)
        hear(self, "confirm they hold", lead=0.2)
        eq = T("=", 110).move_to([3.1, 1.2, 0])
        self.play(FadeIn(eq), run_time=0.3)
        self.play(Create(check(3.1, 2.3, s=0.3, color=TERRA, w=12)), run_time=0.35)
        done(self)


class B73_WorkflowManager(Scene):
    """Two workflow managers run a three-step pipeline; every step is its own box carrying its own version."""
    def construct(self):
        self.add(pA_act_title("VII · Habits That Keep It Honest"))
        nf = chip("nextflow", -2.4, 2.0, mono=True, size=32)
        sm = chip("snakemake", 2.4, 2.0, mono=True, size=32)
        hear(self, "Workflow managers", lead=0.1)
        self.play(FadeIn(nf), FadeIn(sm), run_time=0.35)
        belt = Line([-6.0, -0.3, 0], [6.0, -0.3, 0], color=INK, stroke_width=6)
        xs = [-4.0, 0.0, 4.0]
        steps = []
        for i, x in enumerate(xs):
            bx = pA_box(x, 0.45, 0.95)
            lab = T(f"step {i + 1}", 34).move_to([x, -1.1, 0])
            steps.append((bx, lab))
        a1 = pA_arrow([-1.2, 1.7, 0], [-3.4, 1.35, 0], w=4, tip=0.2)
        a2 = pA_arrow([1.2, 1.7, 0], [3.4, 1.35, 0], w=4, tip=0.2)
        hear(self, "each step", lead=0.2)
        self.play(Create(belt), Create(a1), Create(a2), run_time=0.4)
        work = Dot([-6.0, -0.3, 0], radius=0.14, color=TERRA)
        self.add(work)
        vers = ["v1", "v2", "v3"]
        hear(self, "its own container", lead=0.3)
        for (bx, lab), x, v in zip(steps, xs, vers):
            self.play(FadeIn(bx), FadeIn(lab), run_time=0.3)
            self.play(work.animate.move_to([x, -0.3, 0]), run_time=0.45)
            if x == xs[0]:
                hear(self, "every tool carries", lead=0.1)
            vc = chip(v, x, -2.1, mono=True, size=30)
            self.play(FadeIn(vc), run_time=0.25)
        self.play(work.animate.move_to([6.0, -0.3, 0]), run_time=0.4)
        done(self)


class B74_AicrContainers(Scene):
    """AICR has both tools; policy is not documented; the partition fixes the GPU type; Explorer's paths are not copied."""
    def construct(self):
        self.add(pA_act_title("VII · Habits That Keep It Honest"))
        rack = pA_rack(-4.0, -0.2, 1.0, big=True)
        rl = T("AICR", 40).move_to([-4.0, -2.4, 0])
        self.play(FadeIn(rack), FadeIn(rl), run_time=0.4)
        hear(self, "installed", lead=1.0)
        ap = logo_chip("apptainer", -0.2, 1.8, h=1.1)
        sg = chip("singularity", -0.2, 0.35, mono=True, size=30)
        self.play(FadeIn(ap), FadeIn(sg), run_time=0.4)
        self.play(Create(check(1.0, 1.8, s=0.25, color=TERRA, w=10)), Create(check(1.9, 0.35, s=0.25, color=TERRA, w=10)), run_time=0.35)
        hear(self, "no documentation", lead=0.2)
        pl = T("container policy", 34).move_to([4.2, 2.3, 0])
        nd = chip("not documented", 4.2, 1.5, size=32)
        self.play(FadeIn(pl), FadeIn(nd), run_time=0.4)
        hear(self, "The partition", lead=0.2)
        gr = chip("--gres=gpu:1", 4.0, 0.2, mono=True, size=28)
        nt = T("no GPU type", 34).move_to([4.0, -0.7, 0])
        self.play(FadeIn(gr), FadeIn(nt), run_time=0.4)
        hear(self, "Do not copy", lead=0.15)
        pj = chip("/projects", 0.3, -2.0, mono=True, size=28)
        self.play(FadeIn(pj), run_time=0.3)
        self.play(Create(x_mark(1.95, -2.0, r=0.28, w=9)), run_time=0.25)
        hear(self, "ask", lead=0.1)
        sup = chip("ask AICR support", 4.4, -2.1, size=30)
        self.play(FadeIn(sup), run_time=0.35)
        done(self)


class B80_CheckedVsRead(Scene):
    """Three read-only checks stamp in on the left; four things only read from the source stamp in on the right."""
    def construct(self):
        self.add(pA_act_title("VIII · What Was Checked"))
        hl = T("checked on the login node", 34).move_to([-3.1, 2.3, 0])
        hr = T("only read, not run", 34).move_to([3.4, 2.3, 0])
        left_items = [("apptainer 1.4.5", True, 1.4), ("no module needed", False, 0.4), ("GPU time limits", False, -0.6)]
        right_items = [("run a container", 1.5), ("pull an image", 0.6), ("build an image", -0.3), ("submit a job", -1.2)]
        slots = VGroup()
        for _, _, y in left_items:
            slots.add(DashedVMobject(Rectangle(width=4.3, height=0.8, color=BAR1, stroke_width=3).move_to([-3.1, y, 0]), num_dashes=30))
        for _, y in right_items:
            slots.add(DashedVMobject(Rectangle(width=3.6, height=0.8, color=BAR1, stroke_width=3).move_to([3.4, y, 0]), num_dashes=26))
        self.play(FadeIn(hl), FadeIn(hr), FadeIn(slots), run_time=0.5)
        hear(self, "read only", lead=0.2)
        for txt, mono, y in left_items:
            c = chip(txt, -3.1, y, mono=mono or True, size=28)
            self.play(FadeIn(c), run_time=0.3)
            self.play(Create(check(-0.45, y, s=0.2, color=TERRA, w=9)), run_time=0.2)
        hear(self, "did not run", lead=0.2)
        for txt, y in right_items:
            c = chip(txt, 3.4, y, mono=True, size=28)
            self.play(FadeIn(c), run_time=0.3)
        hear(self, "came from", lead=0.2)
        fs = chip("from the source", 3.4, -2.3, size=32)
        self.play(FadeIn(fs), run_time=0.35)
        done(self)
