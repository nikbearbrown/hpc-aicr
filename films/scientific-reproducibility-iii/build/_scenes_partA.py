# ═════════════════════════════ PART A — B10 B11 B12 B20 B21 B22 B23 (+ shared helpers pA_*) ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pA_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pA_box(x, y, sc=1.0, tape=True):
    """The sealed container: a kraft box with one terracotta tape, centred on (x, y). The film's one box."""
    iso = Iso(0, 0, sc)
    g = job_box(iso, 0, 0, 0, 0.8) if tape else VGroup(iso.box(0, 0, 0, 0.8, 0.8, 0.64))
    return g.move_to([x, y, 0])


def pA_open_box(x, y, sc=1.0):
    """The same box, lid off. Returns (back, front); put contents between them."""
    iso = Iso(0, 0, sc)
    back, front = iso.open_box(0, 0, 0, 1.0, 1.0, 0.8)
    c = VGroup(back, front).get_center()
    back.shift(np.array([x, y, 0]) - c)
    front.shift(np.array([x, y, 0]) - c)
    return back, front


def pA_rack(x, y, sc=1.0, big=False):
    iso = Iso(0, 0, sc)
    st, lt = aicr_rack(iso) if big else explorer_rack(iso)
    g = VGroup(st, lt)
    g.lights = lt
    return g.move_to([x, y, 0])


def pA_laptop(x, y, s=1.0):
    bezel = RoundedRectangle(corner_radius=0.12 * s, width=2.1 * s, height=1.4 * s, fill_color=BOX_L, fill_opacity=1,
                             stroke_color=INK, stroke_width=5).move_to([x, y + 0.1 * s, 0])
    screen = Rectangle(width=1.7 * s, height=1.0 * s, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR2,
                       stroke_width=4).move_to([x, y + 0.15 * s, 0])
    base = RoundedRectangle(corner_radius=0.08 * s, width=2.6 * s, height=0.22 * s, fill_color=BOX_R, fill_opacity=1,
                            stroke_color=INK, stroke_width=5).move_to([x, y - 0.72 * s, 0])
    return VGroup(base, bezel, screen)


def pA_cloud(x, y, s=1.0):
    parts = VGroup(
        Circle(radius=0.55 * s, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x - 0.55 * s, y - 0.1 * s, 0]),
        Circle(radius=0.75 * s, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x + 0.05 * s, y + 0.15 * s, 0]),
        Circle(radius=0.55 * s, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x + 0.7 * s, y - 0.1 * s, 0]),
        Rectangle(width=1.8 * s, height=0.6 * s, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x + 0.08 * s, y - 0.4 * s, 0]))
    return parts


def pA_folder(x, y, w=1.6, h=1.1, fill=BOX_L):
    tab = Rectangle(width=w * 0.45, height=0.2, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x - w * 0.27, y + h / 2 + 0.08, 0])
    body = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    return VGroup(tab, body)


def pA_arrow(a, b, w=6, tip=0.3):
    return Arrow(a, b, color=INK, stroke_width=w, buff=0, tip_length=tip, max_tip_length_to_length_ratio=0.5)


def pA_dots(cx, cy, n=8, r=0.12, rad=1.9, seed=3):
    """Small plain dots for 'other users': deterministic ring-ish scatter."""
    out = VGroup()
    for i in range(n):
        a = 2 * PI * i / n + 0.3
        rr = rad * (0.8 + 0.25 * ((i * 7 + seed) % 3) / 2)
        out.add(Dot([cx + rr * np.cos(a) * 1.35, cy + rr * np.sin(a) * 0.9, 0], radius=r, color=DIM))
    return out


class B10_SealedBox(Scene):
    """Four parts drop into one box; it is taped shut; the sealed box visits a laptop, a cluster and a cloud unchanged."""
    def construct(self):
        self.add(pA_act_title("I · What A Container Is"))
        back, front = pA_open_box(-4.7, -1.45, 1.35)
        self.play(FadeIn(back), FadeIn(front), run_time=0.4)
        names = ["program", "libraries", "settings", "runtime"]
        chips = [chip(n, -4.7, 2.4 - 0.72 * i, size=32) for i, n in enumerate(names)]
        phrases = ["a program", "its libraries", "its settings", "small runtime"]
        for c, ph in zip(chips, phrases):
            hear(self, ph, lead=0.05)
            self.play(FadeIn(c, shift=DOWN * 0.15), run_time=0.3)
        for c in chips:
            self.play(ShrinkToCenter(c), run_time=0.22)
        sealed = pA_box(-4.7, -1.3, 1.35)
        self.play(FadeOut(back), FadeOut(front), FadeIn(sealed), run_time=0.35)
        tgt = [(pA_laptop(-1.1, -1.35, 0.85), -1.1, "laptop"), (pA_rack(1.9, -1.15, 0.95), 1.9, "cluster"), (pA_cloud(4.8, -1.0, 0.8), 4.8, "cloud")]
        labs = []
        hear(self, "Move that file", lead=0.0)
        for i, (obj, tx, nm) in enumerate(tgt):
            lab = T(nm, 34).move_to([tx, -2.75, 0])
            labs.append(lab)
            self.play(FadeIn(obj), FadeIn(lab), run_time=0.3)
            hear(self, ["laptop", "cluster", "cloud"][i], lead=0.25)
            self.play(sealed.animate.move_to([tx, 0.75, 0]), run_time=0.5)
        hear(self, "does not change", lead=0.3)
        ck = check(5.7, 0.8, s=0.3, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.35)
        done(self)


class B11_ThreeNames(Scene):
    """Docker, then the older name Singularity, then Apptainer (renamed from it) with the clusters that use it."""
    def construct(self):
        self.add(pA_act_title("I · What A Container Is"))
        dk = logo_chip("docker", -4.6, 0.7, h=1.6)
        dkl = T("laptops, cloud", 34).move_to([-4.6, -0.55, 0])
        sg = chip("singularity", 0.0, 0.7, mono=True, size=34)
        sgl = T("older name", 34).move_to([0.0, -0.55, 0])
        ap = logo_chip("apptainer", 4.6, 0.7, h=1.6)
        apl = T("Explorer, AICR", 34).move_to([4.6, -0.55, 0])
        self.add(dk)
        hear(self, "Docker is", lead=0.1)
        self.play(FadeIn(dk), run_time=0.3)
        self.play(FadeIn(dkl), run_time=0.3)
        hear(self, "Singularity is", lead=0.1)
        self.play(FadeIn(sg), FadeIn(sgl), run_time=0.4)
        hear(self, "current name", lead=0.5)
        self.play(FadeIn(ap), run_time=0.35)
        ar = pA_arrow([1.55, 0.7, 0], [3.5, 0.7, 0])
        rn = T("renamed", 34).move_to([2.55, 1.35, 0])
        self.play(Create(ar), FadeIn(rn), run_time=0.45)
        hear(self, "Explorer", lead=0.1)
        self.play(FadeIn(apl), run_time=0.3)
        hear(self, "use", lead=0.0)
        ck = check(4.6, -1.75, s=0.3, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.35)
        done(self)


class B12_WhyApptainer(Scene):
    """Docker's admin key into a shared rack is crossed out; Apptainer enters as you with one small key; it reads Docker images."""
    def construct(self):
        self.add(pA_act_title("I · What A Container Is"))
        rack = pA_rack(0.0, -0.55, 1.15, big=True)
        users = pA_dots(0.0, -0.55, n=9, rad=2.15)
        self.play(FadeIn(rack), FadeIn(users), run_time=0.5)
        dk = logo_chip("docker", -4.8, 1.35, h=1.3)
        key = key_obj(-3.9, 1.35, 0.55)
        kl = T("admin", 34).move_to([-3.0, 1.95, 0])
        hear(self, "Docker's normal setup", lead=0.1)
        self.play(FadeIn(dk), run_time=0.3)
        self.play(FadeIn(key), FadeIn(kl), run_time=0.3)
        self.play(key.animate.shift([1.3, -1.2, 0]), run_time=0.5)
        hear(self, "security problem", lead=0.3)
        xm = x_mark(-2.9, -0.35, r=0.4, w=11)
        self.play(Create(xm), run_time=0.3)
        ap = logo_chip("apptainer", 4.9, 1.9, h=1.3)
        bear = professor_bear("1x1", 1.5, seed="B12", x=5.0, y=-0.95)
        hear(self, "Apptainer runs", lead=0.1)
        self.play(FadeIn(ap), FadeIn(bear), run_time=0.4)
        skey = key_obj(3.6, 0.0, 0.32)
        ayou = T("as you", 34).move_to([4.9, 0.7, 0])
        self.play(FadeIn(skey), FadeIn(ayou), run_time=0.3)
        self.play(skey.animate.shift([-1.2, -0.4, 0]), run_time=0.45)
        hear(self, "Docker images", lead=0.35)
        img = chip("Docker image", -4.6, -2.65, size=30)
        ar = pA_arrow([-3.0, -2.65, 0], [3.8, -2.65, 0])
        self.play(FadeIn(img), Create(ar), run_time=0.5)
        ck = check(4.4, -2.6, s=0.28, color=TERRA, w=12)
        self.play(Create(ck), run_time=0.3)
        done(self)


class B20_Reproducible(Scene):
    """A result tied to image 1.0; six months pass and the system updates; the box does not change; a collaborator gets the same."""
    def construct(self):
        self.add(pA_act_title("II · Why Use One"))
        res = paper(-5.0, 0.2, w=1.7, h=2.1, tilt=0.0)
        resl = T("result", 34).move_to([-5.0, 1.6, 0])
        rl = scribbles_on(res, n=3)
        box = pA_box(-1.9, 0.5, 1.05)
        tag = chip("image 1.0", -1.9, -0.95, mono=True, size=32)
        self.play(FadeIn(res), FadeIn(rl), FadeIn(resl), run_time=0.4)
        hear(self, "ties to", lead=0.2)
        self.play(FadeIn(box), FadeIn(tag), run_time=0.35)
        tie = Line([-4.1, 0.25, 0], [-2.85, 0.45, 0], color=INK, stroke_width=7)
        self.play(Create(tie), run_time=0.35)
        rack = pA_rack(1.5, -1.5, 0.95)
        rl2 = T("system", 34).move_to([1.5, -2.75, 0])
        hear(self, "six months", lead=0.15)
        self.play(FadeIn(rack), FadeIn(rl2), run_time=0.3)
        strip = Line([-0.2, 2.2, 0], [4.6, 2.2, 0], color=INK, stroke_width=6)
        ticks = VGroup(*[Line([x, 2.05, 0], [x, 2.35, 0], color=INK, stroke_width=5) for x in np.linspace(-0.2, 4.6, 7)])
        mo = T("six months", 34).move_to([2.2, 2.85, 0])
        dot = Dot([-0.2, 2.2, 0], radius=0.13, color=TERRA)
        self.play(Create(strip), Create(ticks), FadeIn(mo), FadeIn(dot), run_time=0.4)
        self.play(dot.animate.move_to([4.6, 2.2, 0]), run_time=0.9)
        hear(self, "system underneath", lead=0.2)
        new_top = pA_rack(1.5, -1.5, 0.95)
        upd = chip("updated", 1.5, 0.15, size=32)
        self.play(FadeIn(upd), Indicate(rack, color=INK, scale_factor=1.06), run_time=0.6)
        hear(self, "collaborator", lead=0.1)
        bear = professor_bear("1x1", 1.7, seed="B20", x=4.9, y=0.3)
        self.play(FadeIn(bear), run_time=0.35)
        ck = check(4.9, -1.1, s=0.3, color=TERRA, w=12)
        same = T("same software", 34).move_to([4.9, -1.85, 0])
        hear(self, "same software", lead=0.1)
        self.play(Create(ck), FadeIn(same), run_time=0.4)
        done(self)


class B21_PortableNoFights(Scene):
    """One box runs on laptop, rack and cloud; then two tools clash over one library until each gets its own box."""
    def construct(self):
        self.add(pA_act_title("II · Why Use One"))
        box = pA_box(-5.0, 1.55, 0.8)
        lap = pA_laptop(-1.7, 1.55, 0.6)
        rk = pA_rack(1.2, 1.6, 0.75)
        cl = pA_cloud(4.3, 1.65, 0.6)
        hear(self, "Portable", lead=0.1)
        self.play(FadeIn(box), run_time=0.3)
        for obj, x, ph in ((lap, -1.7, "your laptop"), (rk, 1.2, "Explorer"), (cl, 4.3, "cloud")):
            hear(self, ph, lead=0.35)
            a = pA_arrow([-4.2 if x < 0 else (-1.0 if x < 3 else 2.2), 1.55, 0], [x - 1.15, 1.55, 0], w=5, tip=0.25)
            self.play(FadeIn(obj), Create(a), run_time=0.35)
            self.play(Create(check(x + 1.25 if x < 3 else x + 1.0, 2.2, s=0.2, color=TERRA, w=9)), run_time=0.2)
        # no dependency fights
        hear(self, "dependency fights", lead=0.1)
        ta = chip("tool A", -4.4, -1.0, size=32)
        tb = chip("tool B", -4.4, -2.45, size=32)
        lib = Rectangle(width=1.9, height=1.2, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-0.6, -1.7, 0])
        libl = T("library", 34).move_to([-0.6, -2.65, 0])
        v1 = M("v1", 30).move_to([-2.35, -0.75, 0])
        v2 = M("v2", 30).move_to([-2.35, -2.7, 0])
        self.play(FadeIn(ta), FadeIn(tb), FadeIn(lib), FadeIn(libl), run_time=0.4)
        hear(self, "incompatible versions", lead=0.1)
        a1 = pA_arrow([-3.4, -1.0, 0], [-1.6, -1.4, 0], w=5, tip=0.25)
        a2 = pA_arrow([-3.4, -2.45, 0], [-1.6, -2.05, 0], w=5, tip=0.25)
        self.play(Create(a1), Create(a2), FadeIn(v1), FadeIn(v2), run_time=0.45)
        xm = x_mark(-0.6, -1.7, r=0.3, w=10)
        self.play(Create(xm), run_time=0.25)
        hear(self, "each get their own", lead=0.1)
        self.play(*[FadeOut(m) for m in (a1, a2, v1, v2, lib, libl, xm, ta, tb)], run_time=0.3)
        bx1, bx2 = pA_box(1.6, -1.55, 0.85), pA_box(4.4, -1.55, 0.85)
        t1 = chip("tool A  v1", 1.6, -2.7, size=30)
        t2 = chip("tool B  v2", 4.4, -2.7, size=30)
        self.play(FadeIn(bx1), FadeIn(bx2), FadeIn(t1), FadeIn(t2), run_time=0.4)
        hear(self, "neither one", lead=0.2)
        self.play(Create(check(3.0, -1.5, s=0.3, color=TERRA, w=12)), run_time=0.3)
        done(self)


class B22_ShareRegistries(Scene):
    """One file goes to a collaborator, an archive and a reviewer; four registries each hold stacks of ready-made images."""
    def construct(self):
        self.add(pA_act_title("II · Why Use One"))
        box = pA_box(-5.3, -0.4, 1.0)
        bear = professor_bear("1x1", 1.35, seed="B22", x=-2.5, y=0.55)
        arc = pA_folder(-2.5, -1.0, 1.3, 0.8)
        rev = paper(-2.5, -2.35, w=1.2, h=1.0)
        hear(self, "Shareable", lead=0.1)
        self.play(FadeIn(box), run_time=0.3)
        for obj, lab, y, ph in ((bear, "collaborator", 0.55, "collaborator"), (arc, "archive", -1.0, "archive"), (rev, "reviewer", -2.35, "reviewer")):
            hear(self, ph, lead=0.3)
            a = pA_arrow([-4.5, -0.4, 0], [-3.4, y, 0], w=5, tip=0.25)
            l = T(lab, 32).move_to([-1.2 + len(lab) * 0.09, y, 0])
            self.play(FadeIn(obj), Create(a), FadeIn(l), run_time=0.4)
        hear(self, "registries", lead=0.1)
        shelf = Line([1.2, 2.0, 0], [6.1, 2.0, 0], color=INK, stroke_width=6)
        self.play(Create(shelf), run_time=0.25)
        names = [("docker", None), (None, "quay.io"), ("nvidia", None), (None, "BioContainers")]
        ys = [1.1, 0.0, -1.1, -2.2]
        for (logo, mono), y in zip(names, ys):
            c = logo_chip(logo, 2.1, y, h=0.9) if logo else chip(mono, 2.7 if mono == "quay.io" else 2.9, y, mono=True, size=28)
            stack = VGroup(*[pA_box(5.15 + 0.4 * k, y, 0.28, tape=False) for k in range(3)])
            self.play(FadeIn(c), LaggedStart(*[FadeIn(s) for s in stack], lag_ratio=0.2), run_time=0.6)
        done(self)


class B23_TheLadder(Scene):
    """module, then conda, then container: an arrow climbs three steps; the top step carries large images."""
    def construct(self):
        self.add(pA_act_title("II · Why Use One"))
        step_x = [-4.2, 0.0, 4.2]
        step_y = [-1.9, -0.9, 0.1]
        steps = VGroup(*[Rectangle(width=3.6, height=1.4 + 1.0 * i, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
                         .move_to([x, -2.4 + (1.4 + i) / 2, 0]) for i, x in enumerate(step_x)])
        sl_ = [T("module", 36).move_to([-4.2, -2.95, 0]), T("conda", 36).move_to([0.0, -2.95, 0]), T("container", 36).move_to([4.2, -2.95, 0])]
        hear(self, "images are large", lead=0.3)
        self.play(FadeIn(steps), *[FadeIn(l) for l in sl_], run_time=0.5)
        big = T("large images", 34).move_to([4.2, 3.05, 0])
        self.play(FadeIn(big), run_time=0.3)
        mod = pA_rack(-4.2, -0.3, 0.5)
        hear(self, "module first", lead=0.1)
        self.play(FadeIn(mod), run_time=0.35)
        ar1 = pA_arrow([-3.2, 0.2, 0], [-1.1, 0.8, 0], w=6, tip=0.3)
        cd = logo_chip("anaconda", 0.0, 1.55, h=1.0)
        hear(self, "then conda", lead=0.15)
        self.play(Create(ar1), FadeIn(cd), run_time=0.45)
        ar2 = pA_arrow([1.0, 1.0, 0], [3.0, 1.6, 0], w=6, tip=0.3)
        bx = pA_box(4.2, 2.1, 0.55)
        hear(self, "then a container", lead=0.15)
        self.play(Create(ar2), FadeIn(bx), run_time=0.45)
        hear(self, "painful", lead=0.2)
        ring = Circle(radius=0.65, color=TERRA, stroke_width=7).move_to([4.2, 2.1, 0])
        self.play(Create(ring), run_time=0.4)
        self.play(FadeOut(ring), run_time=0.25)
        done(self)
