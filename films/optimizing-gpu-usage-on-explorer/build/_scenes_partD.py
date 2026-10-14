# ═════════════════════════════ PART D — Acts VII and VIII (manim beats) ═════════════════════════════


def pD_rack(x, y, n):
    """A small drawn rack: n dark slabs stacked (Explorer 2, AICR 4)."""
    return VGroup(*[RoundedRectangle(corner_radius=0.06, width=1.3, height=0.32, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
                    .move_to([x, y + 0.38 * i, 0]) for i in range(n)])


class B70_TheLoop(Scene):
    """Seven stations on a ring; a job box travels round and each station gets its light as it arrives."""
    def construct(self):
        title = act_title("VII · The Loop")
        names = ["baseline", "profile", "diagnose", "fix one thing", "re-profile", "record the gain", "repeat"]
        pos = [(0.0, 2.1), (3.4, 1.3), (4.3, -0.6), (1.9, -2.1), (-1.9, -2.1), (-4.3, -0.6), (-3.4, 1.3)]
        arrows = []
        for i in range(7):
            p, q = np.array(pos[i] + (0,)), np.array(pos[(i + 1) % 7] + (0,))
            m = (p + q) / 2
            d = (q - p) / np.linalg.norm(q - p)
            arrows.append(Arrow(m - d * 0.3, m + d * 0.3, color=BAR1, stroke_width=7, buff=0, max_tip_length_to_length_ratio=0.5))
        chips = [chip(n, x, y, size=34) for n, (x, y) in zip(names, pos)]
        job = job2(0.0, 0.0, 0.9)
        dots = [Dot([x - 0.0, y + 0.55, 0], radius=0.1, color=TERRA) for (x, y) in pos]
        cues = ["Baseline", "profile", "diagnose", "fix", "re", "record", "repeat"]
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "loop", lead=0.3)
        self.play(FadeIn(job), run_time=0.5)
        for i in range(7):
            hear(self, cues[i], lead=0.15)
            self.play(FadeIn(chips[i]), job.animate.move_to([pos[i][0] * 0.55, pos[i][1] * 0.55, 0]), FadeIn(dots[i]), FadeIn(arrows[i]), run_time=0.5)
        done(self)


class B71_DecisionGuide(Scene):
    """A decision tree: utilization under 50 goes to the data pipeline; 50 to 80 goes to memory, which branches; an out-of-memory track."""
    def construct(self):
        title = act_title("VII · The Loop")
        root = chip("utilization", -5.0, 0.9, size=36)
        b1 = chip("< 50", -2.4, 2.1, size=34)
        b2 = chip("50 to 80", -2.4, -0.3, size=34)
        r1 = chip("data pipeline first", 1.7, 2.1, size=34)
        r1m = chip("num_workers == 0 ?", 1.7, 1.35, mono=True, size=28)
        mem = chip("memory", -0.2, -0.3, size=34)
        s1 = chip("< 50%: raise batch", 3.9, 0.4, w=4.4, size=28)
        s2 = chip("50-85%: mixed precision", 3.9, -0.35, w=4.4, size=28)
        s3 = chip("> 90%: shrink or checkpoint", 3.9, -1.1, w=4.4, size=28)
        def ln(a, b):
            return Line([a[0], a[1], 0], [b[0], b[1], 0], color=BAR1, stroke_width=5)
        l1, l2 = ln((-4.0, 1.0), (-3.1, 2.0)), ln((-4.0, 0.8), (-3.2, -0.2))
        l3, l4 = ln((-1.7, 2.1), (-0.9, 2.1)), ln((-1.7, -0.3), (-1.2, -0.3))
        l5 = [ln((0.8, -0.3), (1.6, y)) for y in (0.4, -0.35, -1.1)]
        oom_names = ["out of memory", "smaller batch", "mixed precision", "checkpoint"]
        ox = [-4.4, -1.55, 1.45, 4.5]
        ow = [2.6, 2.6, 2.9, 2.6]
        oom = [chip(n, x, -2.7, w=w, size=30) for n, x, w in zip(oom_names, ox, ow)]
        oar = [Arrow([ox[i] + ow[i] / 2 + 0.02, -2.7, 0], [ox[i + 1] - ow[i + 1] / 2 - 0.02, -2.7, 0], color=INK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.5) for i in range(3)]
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "utilization", lead=0.2)
        self.play(FadeIn(root), Create(l1), FadeIn(b1), run_time=0.5)
        hear(self, "data pipeline", lead=0.15)
        self.play(Create(l3), FadeIn(r1), run_time=0.4)
        hear(self, "workers still", lead=0.2)
        self.play(FadeIn(r1m), run_time=0.35)
        hear(self, "50 to 80", lead=0.2)
        self.play(Create(l2), FadeIn(b2), run_time=0.4)
        hear(self, "look at memory", lead=0.1)
        self.play(Create(l4), FadeIn(mem), *[Create(l) for l in l5], run_time=0.5)
        hear(self, "Memory under", lead=0.2)
        self.play(FadeIn(s1), run_time=0.35)
        hear(self, "50 to 85", lead=0.15)
        self.play(FadeIn(s2), run_time=0.35)
        hear(self, "over 90", lead=0.15)
        self.play(FadeIn(s3), run_time=0.35)
        hear(self, "Out of memory", lead=0.1)
        self.play(FadeIn(oom[0]), run_time=0.3)
        hear(self, "smaller batch", lead=0.1)
        self.play(Create(oar[0]), FadeIn(oom[1]), run_time=0.3)
        hear(self, "then mixed", lead=0.1)
        self.play(Create(oar[1]), FadeIn(oom[2]), run_time=0.3)
        hear(self, "check", lead=0.1)
        self.play(Create(oar[2]), FadeIn(oom[3]), run_time=0.3)
        done(self)


class B73_ReadGpuLogs(Scene):
    """Three schematic line plots (flat high, bouncing low, flat low) with the 70 line; two readouts; under 60, fix first."""
    def construct(self):
        title = act_title("VII · The Loop")
        xs = [-4.2, 0.0, 4.2]
        def plot(x):
            fr = Rectangle(width=3.4, height=1.7, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR2, stroke_width=5).move_to([x, 1.2, 0])
            y70 = DashedLine([x - 1.7, 1.2 - 0.85 + 1.7 * 0.7, 0], [x + 1.7, 1.2 - 0.85 + 1.7 * 0.7, 0], color=BAR1, stroke_width=4)
            return VGroup(fr, y70)
        def pts(x, f):
            return [[x - 1.5 + 3.0 * i / 20, 1.2 - 0.85 + 1.7 * f(i), 0] for i in range(21)]
        def curve(x, f):
            m = VMobject(stroke_color=INK, stroke_width=7)
            m.set_points_as_corners(pts(x, f))
            return m
        high = curve(xs[0], lambda i: 0.88 + (0.03 if i % 2 else -0.03))
        bounce = curve(xs[1], lambda i: 0.45 if i % 4 < 2 else 0.12)
        low = curve(xs[2], lambda i: 0.12 + (0.02 if i % 2 else -0.02))
        frames = [plot(x) for x in xs]
        t1 = [lab_c("flat and high", xs[0], -0.05, 34), lab_c("bouncing low", xs[1], -0.05, 34), lab_c("flat and low", xs[2], -0.05, 34)]
        t2 = [lab_c("healthy", xs[0], -0.6, 34), lab_c("data starvation", xs[1], -0.6, 34), lab_c("workload too small", xs[2], -0.6, 34)]
        tag = T("shapes, not output", 32).move_to([2.6, 2.75, 0])
        c1 = chip("average utilization: above 70", -3.0, -1.7, size=32)
        c2 = chip("average VRAM: low = room", 3.3, -1.7, size=32)
        fin = T("under 60: fix it before the next submission", 40).move_to([0, -2.8, 0])
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "average", lead=0.2)
        self.play(FadeIn(c1), run_time=0.4)
        hear(self, "shape of the line", lead=0.2)
        self.play(*[FadeIn(f) for f in frames], FadeIn(tag), run_time=0.5)
        hear(self, "flat and high", lead=0.15)
        self.play(Create(high), FadeIn(t1[0]), FadeIn(t2[0]), run_time=0.7)
        hear(self, "Bouncing", lead=0.15)
        self.play(Create(bounce), FadeIn(t1[1]), FadeIn(t2[1]), run_time=0.7)
        hear(self, "Flat and low", lead=0.15)
        self.play(Create(low), FadeIn(t1[2]), FadeIn(t2[2]), run_time=0.7)
        hear(self, "VRAM", lead=0.2)
        self.play(FadeIn(c2), run_time=0.4)
        hear(self, "Under 60", lead=0.15)
        self.play(FadeIn(fin), run_time=0.5)
        done(self)


class B74_Checklist(Scene):
    """A clipboard page of eight rows; each box gets a check on its spoken cue."""
    def construct(self):
        title = act_title("VII · The Loop")
        shadow = Rectangle(width=12.0, height=5.2, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([0.1, -0.4, 0])
        page = Rectangle(width=12.0, height=5.2, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([0, -0.3, 0])
        labels = ["verify passed", "over 70% in a short run", "workers + pin set", "half the VRAM used",
                  "precision matches card", "type named, 4+ CPUs", "logs/ exists", "profiled 20 to 50 steps"]
        pos = [(-5.5, 1.4), (-5.5, 0.3), (-5.5, -0.8), (-5.5, -1.9), (0.5, 1.4), (0.5, 0.3), (0.5, -0.8), (0.5, -1.9)]
        boxes, labs, cks = [], [], []
        for (x, y), t in zip(pos, labels):
            boxes.append(Rectangle(width=0.45, height=0.45, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=4).move_to([x + 0.22, y, 0]))
            labs.append(lab_l(t, x + 0.7, y, 34))
            cks.append(check(x + 0.2, y, s=0.2, color=TERRA, w=11))
        cues = ["check passed", "short run", "Workers", "batch uses", "Precision", "request", "logs folder", "profiled"]
        self.play(FadeIn(title), FadeIn(shadow), FadeIn(page), run_time=0.4)
        for i in range(8):
            hear(self, cues[i], lead=0.2)
            self.play(FadeIn(boxes[i]), FadeIn(labs[i]), run_time=0.25)
            self.play(Create(cks[i]), run_time=0.2)
        done(self)


class B80_YourDomain(Scene):
    """Four rows: PyTorch and TensorFlow (every act), Hugging Face (flags), molecular dynamics (trajectory writes), custom CUDA (Nsight Compute)."""
    def construct(self):
        title = act_title("VIII · Your Domain")
        ys = [1.7, 0.5, -0.7, -1.9]
        r1 = Group(logo_chip("pytorch", -5.2, ys[0], h=0.95), logo_chip("tensorflow", -3.7, ys[0], h=0.95), lab_c("every act", 1.4, ys[0], 40))
        r2 = Group(logo_chip("huggingface", -5.2, ys[1], h=0.95), lab_c("verify, watch, feed; fixes are flags", 3.15, ys[1], 36))
        r3 = Group(chip("GROMACS  NAMD  AMBER", -3.2, ys[2], w=5.7, mono=True, size=30), lab_c("trajectory writes limit you", 2.8, ys[2], 38))
        r4 = Group(logo_chip("nvidia", -5.2, ys[3], h=0.95), chip("custom CUDA", -3.0, ys[3], mono=True, size=30), lab_c("add Nsight Compute", 2.2, ys[3], 38))
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "PyTorch and", lead=0.15)
        self.play(FadeIn(r1), run_time=0.5)
        hear(self, "Package", lead=0.15)
        self.play(FadeIn(r2), run_time=0.5)
        hear(self, "Molecular", lead=0.15)
        self.play(FadeIn(r3), run_time=0.5)
        hear(self, "Custom", lead=0.15)
        self.play(FadeIn(r4), run_time=0.5)
        done(self)


class B82_ExplorerNotAicr(Scene):
    """Two columns, Explorer and AICR, row by row: the card, the environment, the post-job report, nvidia-smi on the login node."""
    def construct(self):
        title = act_title("VIII · Your Domain")
        div = Line([0, 2.6, 0], [0, -2.8, 0], color=BAR2, stroke_width=6)
        r_e, r_a = pD_rack(-1.6, 1.5, 2), pD_rack(4.6, 1.5, 4)
        h_e, h_a = T("Explorer", 42).move_to([-4.0, 1.75, 0]), T("AICR", 42).move_to([2.6, 1.75, 0])
        ys = [0.5, -0.4, -1.3, -2.2]
        L = [chip("gres: gpu:v100-sxm2:1", -3.2, ys[0], w=5.8, mono=True, size=30), chip("venv + pip wheels", -3.2, ys[1], w=5.8, size=34),
             chip("gpu-logs", -3.2, ys[2], w=5.8, mono=True, size=32), chip("no nvidia-smi on login", -3.2, ys[3], w=5.8, size=34)]
        R = [chip("the partition fixes the card", 3.2, ys[0], w=5.8, size=34), chip("CUDA module + conda", 3.2, ys[1], w=5.8, size=34),
             chip("jobstats", 3.2, ys[2], w=5.8, mono=True, size=32), chip("nvidia-smi on login", 3.2, ys[3], w=5.8, size=34)]
        self.play(FadeIn(title), Create(div), FadeIn(r_e), FadeIn(h_e), FadeIn(r_a), FadeIn(h_a), run_time=0.6)
        hear(self, "name the card", lead=0.3)
        self.play(FadeIn(L[0]), run_time=0.4)
        hear(self, "partition fixes", lead=0.2)
        self.play(FadeIn(R[0]), run_time=0.4)
        hear(self, "virtual environment", lead=0.3)
        self.play(FadeIn(L[1]), run_time=0.4)
        hear(self, "CUDA modules", lead=0.2)
        self.play(FadeIn(R[1]), run_time=0.4)
        hear(self, "GPU logs", lead=0.3)
        self.play(FadeIn(L[2]), run_time=0.4)
        hear(self, "job stats", lead=0.2)
        self.play(FadeIn(R[2]), run_time=0.4)
        hear(self, "login node", lead=0.3)
        self.play(FadeIn(L[3]), run_time=0.4)
        hear(self, "SMI", lead=0.2)
        self.play(FadeIn(R[3]), run_time=0.3)
        done(self)


class B83_CheckedVsRead(Scene):
    """Left, four read-only checks stamp in; right, five things only read from the source; 'nothing ran on a GPU node' first."""
    def construct(self):
        title = act_title("VIII · Your Domain")
        h1 = T("checked here, read-only", 40).move_to([-3.2, 2.05, 0])
        h2 = T("only read", 40).move_to([3.2, 2.05, 0])
        div = Line([0, 2.9, 0], [0, -2.0, 0], color=BAR2, stroke_width=6)
        left = [stamp(t, -3.2, y, w=5.4, size=32) for t, y in zip(["partitions and limits", "five GPU types", "tools on the path", "python module"], [1.3, 0.45, -0.4, -1.25])]
        for _s in left:
            _s[1].set_stroke(KRAFT_DEEP, width=4)  # Gate T: an ink outline round the text reads as one blob over the label
        right = [chip(t, 3.2, y, w=4.6, size=32) for t, y in zip(["sessions", "demo scripts", "profilers", "gpu-logs output", "numbers"], [1.4, 0.7, 0.0, -0.7, -1.4])]
        nothing = chip("nothing ran on a GPU node", 0.0, -2.8, size=38)
        self.play(FadeIn(title), run_time=0.4)
        hear(self, "ran nothing", lead=0.3)
        self.play(FadeIn(nothing), Create(div), FadeIn(h1), FadeIn(h2), run_time=0.5)
        for cue, s in zip(["partitions", "five", "tools", "Python"], left):
            hear(self, cue, lead=0.2)
            self.play(FadeIn(s), run_time=0.3)
        for cue, c in zip(["sessions", "scripts", "profilers", "GPU logs", "numbers"], right):
            hear(self, cue, lead=0.15)
            self.play(FadeIn(c), run_time=0.25)
        done(self)


class B84_GetHelp(Scene):
    """Professor Bear beside three chips: the Research Computing help address, office hours, a consultation."""
    def construct(self):
        title = act_title("VIII · Your Domain")
        pb = professor_bear("1x1", 2.6, seed="B84", x=-4.4, y=0.0)
        c1 = chip("rchelp@northeastern.edu", 1.9, 1.3, w=6.9, mono=True, size=32)
        c2 = chip("office hours", 1.9, 0.0, w=6.9, size=38)
        c3 = chip("book a consultation", 1.9, -1.3, w=6.9, size=38)
        d = [Dot([-1.35, y, 0], radius=0.12, color=TERRA) for y in (1.3, 0.0, -1.3)]
        self.play(FadeIn(title), FadeIn(pb), run_time=0.5)
        hear(self, "write", lead=0.2)
        self.play(FadeIn(c1), FadeIn(d[0]), run_time=0.4)
        hear(self, "office hours", lead=0.2)
        self.play(FadeIn(c2), FadeIn(d[1]), run_time=0.4)
        hear(self, "consultation", lead=0.2)
        self.play(FadeIn(c3), FadeIn(d[2]), run_time=0.4)
        done(self)
