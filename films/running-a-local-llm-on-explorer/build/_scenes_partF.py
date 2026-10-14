# ═════════════════════════════ PART F — B92 B94 B95 B100 B101 B102 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pF_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pF_clamp(a):
    return max(0.0, min(1.0, float(a)))


def pF_when(self, phrase, nth=0, lead=0.0, default=0.0):
    """The measured time Liam says `phrase` (same matching as hear(), but returns the time)."""
    import re as _re
    bid = type(self).__name__.split("_")[0]
    words = _ASR.get(bid)
    if not words:
        return default
    norm = lambda w: _re.sub(r"[^a-z0-9]", "", w.lower())
    toks = [norm(x) for x in phrase.split() if norm(x)]
    seq = [norm(w[0]) for w in words]
    hits = [i for i in range(len(seq) - len(toks) + 1) if seq[i:i + len(toks)] == toks]
    if len(hits) <= nth:
        return default
    return float(words[hits[nth]][1]) - lead


def pF_page(x, y, w=1.0, h=0.9, n=2):
    """A small prompt page: white sheet, ink outline, handwriting lines."""
    pg = paper(x, y, w=w, h=h)
    _w = w - 2 * 0.18
    ln = VGroup(*[scribble(pg.cx - _w / 2, pg.cy + pg.h / 2 - 0.18 - 0.1 - i * 0.26, _w, amp=0.09, sw=3) for i in range(n)])
    return VGroup(pg, ln)


def pF_belt(x0, x1, y, h=0.3):
    """A conveyor belt: kraft band, deep-kraft edge (never an ink edge: GATE T reads that as text)."""
    return Rectangle(width=x1 - x0, height=h, fill_color=BOX_L, fill_opacity=1, stroke_color=KRAFT_DEEP,
                     stroke_width=4).move_to([(x0 + x1) / 2, y, 0])


def pF_crate(x, y, s=0.5, dark=False):
    """A small isometric crate whose near corner sits at (x, y)."""
    ci = Iso(x, y, s)
    if dark:
        return ci.box(0, 0, 0, 1, 1, 0.8, DARK_TOP, DARK_L, DARK_R)
    return ci.box(0, 0, 0, 1, 1, 0.8)


def pF_stamp(text, x, y, w=None, h=0.68, size=32, sub=None, marker="dot", left=False):
    """A white pill with a marker dot and a 1-3 word label. x is the pill's LEFT edge when left=True, else its centre."""
    lab = T(text, size)
    sl = T(sub, size) if sub else None
    textw = max(lab.width, sl.width if sl else 0)
    w = w or (textw + 1.15)
    cx = x + w / 2 if left else x
    if sl:
        h = max(h, 1.1)
    shadow = pill(cx + 0.08, y - 0.08, w, h=h, fill=BOX_L)
    body = pill(cx, y, w, h=h)
    lx = cx - w / 2 + 0.72 + textw / 2
    if sl:
        lab.move_to([lx - textw / 2 + lab.width / 2, y + 0.2, 0])
        sl.move_to([lx - textw / 2 + sl.width / 2, y - 0.2, 0])
    else:
        lab.move_to([lx, y, 0])
    mx = cx - w / 2 + 0.38
    if marker == "dot":
        mk = Dot([mx, y, 0], radius=0.12, color=TERRA)
    else:
        mk = Circle(radius=0.12, color=DIM, stroke_width=4).move_to([mx, y, 0])
    parts = [shadow, body, lab, mk] + ([sl] if sl else [])
    g = VGroup(*parts)
    g.w, g.h = w, h
    return g


# ───────────────────────────────────── B92 ─────────────────────────────────────
def pF_lock_for(x, y):
    return padlock(x + 0.3, y + 0.56, s=0.46)


class B92_SharedService(Scene):
    """Users' keys + prompt pages merge into one batch, lock, pass through the vllm server; three questions float above."""
    def construct(self):
        ys = [1.4, 0.15, -1.1]
        keys = [key_obj(-5.75, y, s=0.55) for y in ys]
        pages = [pF_page(-3.7, y, w=1.15, h=1.0) for y in ys]
        px, py = -1.9, -0.35                     # first page of the batch pile (the cascade steps +0.55, -0.5)
        spots = [(px + 0.55 * k, py - 0.5 * k) for k in range(3)]
        iso = Iso(3.0, -2.0, 1.15)
        stack, lights = explorer_rack(iso)
        srv = VGroup(stack, lights)
        vllm = logo_chip("vllm", 3.0, -2.72, h=1.0)
        batch_lab = T("batch", 34).move_to([px + 0.55, py + 1.45, 0])
        klab = T("API key", 34).move_to([-5.0, 2.3, 0])
        locks = [pF_lock_for(x, y) for (x, y) in spots]
        doc = pF_page(-5.55, -2.6, w=0.9, h=1.1, n=3)
        alone = chip("key alone", -3.65, -2.6, size=34)
        xm = x_mark(-1.95, -2.6, r=0.28, w=9)
        ch = [chip("logging?", -1.48, 2.6), chip("retention?", 1.255, 2.6), chip("who owns it?", 4.44, 2.6)]
        ask = chip("ask Research Computing", 1.7, 1.45)

        # "a service for many people": the users' pages arrive, each with its key
        hear(self, "many people", lead=0.3)
        self.play(LaggedStart(*[FadeIn(g) for g in pages + keys], lag_ratio=0.12), run_time=0.7)
        # "vLLM": the server and its logo
        hear(self, "VLLM", lead=0.3)
        self.play(FadeIn(srv), FadeIn(vllm), run_time=0.5)
        # "batches concurrent requests": the pages merge into one batch
        hear(self, "batches", lead=0.15)
        self.play(*[pg.animate.shift(np.array([sx - (-3.7), sy - y, 0.0])) for pg, (sx, sy), y in zip(pages, spots, ys)],
                  run_time=0.9, rate_func=smooth)
        hear(self, "requests", lead=0.2)
        self.play(FadeIn(batch_lab), run_time=0.3)
        # "API keys": the keys get their name, a padlock lands on each prompt page
        hear(self, "API", lead=0.2)
        self.play(FadeIn(klab), LaggedStart(*[GrowFromCenter(l) for l in locks], lag_ratio=0.2), run_time=0.6)
        pile = VGroup(*pages, *locks)
        # "its own documentation ... not to rely on a key alone"
        hear(self, "documentation", lead=0.2)
        self.play(FadeIn(doc), run_time=0.4)
        hear(self, "key alone", lead=0.1)
        self.play(FadeIn(alone, shift=RIGHT * 0.3), Create(xm), run_time=0.45)
        # "other people's code and prompts": the batch goes into the server (done before the clip midpoint)
        hear(self, "other peoples", lead=0.4)
        self.play(pile.animate.shift(RIGHT * 1.775), FadeOut(batch_lab), run_time=0.5, rate_func=smooth)
        self.play(FadeOut(pile, shift=RIGHT * 0.6, scale=0.6), lights.animate.set_color(TERRA), run_time=0.3)
        # "pass through a service you run": the batch comes out the far side
        out_spots = [(5.0 + 0.55 * k, -0.4 - 0.5 * k) for k in range(3)]
        out = VGroup(*[pF_page(sx, sy, w=1.15, h=1.0) for sx, sy in out_spots], *[pF_lock_for(sx, sy) for sx, sy in out_spots])
        out.scale(0.62).move_to([5.38, -0.85, 0])
        hear(self, "pass through", lead=0.1)
        self.play(FadeIn(out, shift=RIGHT * 0.5), run_time=0.5)
        # "logging, retention, who is responsible"
        hear(self, "logging", lead=0.15)
        self.play(FadeIn(ch[0], shift=DOWN * 0.3), run_time=0.35)
        hear(self, "retention", lead=0.15)
        self.play(FadeIn(ch[1], shift=DOWN * 0.3), run_time=0.35)
        hear(self, "who is responsible", lead=0.15)
        self.play(FadeIn(ch[2], shift=DOWN * 0.3), run_time=0.35)
        # "questions for Research Computing, not settings": the plaque lands under them
        hear(self, "Those are questions", lead=0.15)
        ask.shift(UP * 0.7)
        self.add(ask)
        self.play(ask.animate.shift(DOWN * 0.7), run_time=0.5, rate_func=smooth)
        done(self)


# ───────────────────────────────────── B94 ─────────────────────────────────────
def pF_grid(x0, yc, cols, rows=8, pitch=0.115, side=0.09, color=BAR1):
    """A block of GPU slots: `cols` columns of `rows` small squares, left edge at x0. `.cols` is the list of columns."""
    cells = []
    for c in range(cols):
        cells.append(VGroup(*[Rectangle(width=side, height=side, fill_color=color, fill_opacity=1, stroke_width=0)
                              .move_to([x0 + c * pitch + side / 2, yc + (rows / 2 - 0.5 - r) * pitch, 0]) for r in range(rows)]))
    g = VGroup(*cells)
    g.cols = cells
    return g


class B94_AicrScale(Scene):
    """The big AICR rack with its two GPU blocks and a proposal chip; Explorer first; a standing service between them."""
    def construct(self):
        ai = Iso(0.5, -2.2, 0.8)
        a_stack, a_lights = aicr_rack(ai)
        aicr = VGroup(a_stack, a_lights)
        a_lab = T("AICR", 40).move_to([0.95, -2.85, 0])
        g1 = pF_grid(2.45, 1.65, 31, color=BAR1)
        g2 = pF_grid(2.45, -0.4, 19, color=BAR2)
        l1 = T("B200 x 248", 34).move_to([2.45 + 2.15 / 2, 2.5, 0])
        l2 = T("RTX Pro x 152", 34).move_to([2.45 + 2.81 / 2, 0.55, 0])
        prop = VGroup(pill(4.38, -1.73, 3.6, h=0.95, fill=BOX_L), pill(4.3, -1.65, 3.6, h=0.95),
                      paper(2.95, -1.65, w=0.5, h=0.66), key_obj(3.4, -1.65, s=0.3), T("proposal", 34).move_to([5.1, -1.65, 0]))
        ei = Iso(-4.9, -1.9, 0.8)
        e_stack, e_lights = explorer_rack(ei)
        expl = VGroup(e_stack, e_lights)
        e_lab = T("Explorer", 36).move_to([-4.9, -2.6, 0])
        first = chip("first", -4.9, 0.6, size=34)
        link = Arrow([-3.95, -1.0, 0], [-0.7, -1.0, 0], color=INK, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.18)
        si = Iso(-2.3, -1.9, 0.9)
        svc = si.box(0, 0, 0, 1.1, 1.1, 0.8)
        svc.set_z_index(3)
        s_lab = T("standing service", 34).move_to([-2.3, -2.65, 0])
        q = T("?", 64).move_to([-2.3, 0.3, 0])
        ring = Circle(radius=1.5, color=TERRA, stroke_width=6).move_to([-2.3, -0.6, 0])
        ask = T("ask Research Computing", 34).move_to([-2.3, 1.45, 0])

        # "On AICR": the large rack, named
        hear(self, "AICR", lead=0.1)
        self.play(FadeIn(aicr), FadeIn(a_lab), run_time=0.5)
        # "248 B200": the first block of GPU slots fills, column by column
        hear(self, "248", lead=0.2)
        self.play(LaggedStart(*[FadeIn(c) for c in g1.cols], lag_ratio=0.03), run_time=1.1)
        hear(self, "B200", lead=0.1)
        self.play(FadeIn(l1), run_time=0.3)
        # "152 RTX Pro": the second block
        hear(self, "152", lead=0.15)
        self.play(LaggedStart(*[FadeIn(c) for c in g2.cols], lag_ratio=0.04), run_time=0.8)
        hear(self, "RTX Pro", lead=0.1)
        self.play(FadeIn(l2), run_time=0.3)
        # "access is by proposal": the key-and-paper chip lands beside AICR
        hear(self, "proposal", lead=0.4)
        self.play(FadeIn(prop, shift=DOWN * 0.3), run_time=0.4)
        # "develop and test on Explorer first": the small rack, then the arrow toward AICR
        hear(self, "Explorer", lead=0.4)
        self.play(FadeIn(expl), FadeIn(e_lab), run_time=0.5)
        hear(self, "first", lead=0.1)
        self.play(Create(link), FadeIn(first, shift=DOWN * 0.2), run_time=0.5)
        # "a standing service": the block lands on the arrow, linking both racks
        hear(self, "standing", lead=0.25)
        svc.shift(UP * 0.6)
        self.add(svc)
        self.play(svc.animate.shift(DOWN * 0.6), FadeIn(s_lab), run_time=0.5, rate_func=smooth)
        # "a question only Research Computing can answer": the question mark, then the ring and the pointer
        hear(self, "question", lead=0.2)
        self.play(GrowFromCenter(q), run_time=0.35)
        hear(self, "research computing", lead=0.2, nth=1)
        self.play(Create(ring), FadeIn(ask), run_time=0.6)
        done(self)


# ───────────────────────────────────── B95 ─────────────────────────────────────
class B95_CheckedVsDocumented(Scene):
    """Two columns of stamps: what is documented but not run, and the five read-only checks; then the one thing no page says."""
    def construct(self):
        hd_l = T("documented", 40)
        hd_l.move_to([-5.8 + hd_l.width / 2, 2.85, 0])
        sub_l = T("not run here", 32)
        sub_l.move_to([-5.8 + sub_l.width / 2, 2.3, 0])
        hd_r = T("checked on Explorer", 40)
        hd_r.move_to([0.3 + hd_r.width / 2, 2.85, 0])
        sub_r = T("read-only", 32)
        sub_r.move_to([0.3 + sub_r.width / 2, 2.3, 0])
        div = DashedLine([0, 3.1, 0], [0, -1.1, 0], color=BAR2, stroke_width=4, dash_length=0.2)
        ys = [1.55, 0.8, 0.05, -0.7]
        left = [pF_stamp(s, -5.8, y, left=True, marker="ring") for s, y in zip(["scripts", "tunnel", "proxy", "harness settings"], ys)]
        right = [pF_stamp(s, 0.3, y, left=True) for s, y in zip(["partitions", "H200 type exists", "apptainer on login node",
                                                                 "proxy from default module"], ys)]
        right.append(pF_stamp("scratch not writable", 0.3, -1.7, left=True, sub="on one account"))
        ghost5 = DashedVMobject(RoundedRectangle(width=4.3, height=0.95, corner_radius=0.45, stroke_color=BAR2, stroke_width=4),
                                num_dashes=44).move_to([0.3 + 2.15, -1.7, 0])
        oll = logo_chip("ollama", -5.4, -1.65, h=0.85)
        rcp = T("Research Computing post", 32)
        rcp.move_to([-4.7 + rcp.width / 2, -1.65, 0])
        agw = T("agent access: not stated by any policy page", 32).width + 0.9
        agent = VGroup(pill(0.08, -2.93, agw, h=0.8, fill=BOX_L), pill(0, -2.85, agw, h=0.8),
                       T("agent access: not stated by any policy page", 32).move_to([0, -2.85, 0]))
        ring = RoundedRectangle(width=agw + 0.3, height=1.05, corner_radius=0.52, color=TERRA, stroke_width=5).move_to([0, -2.85, 0])

        # "what we have and have not checked": the two headings
        hear(self, "what we have", lead=0.1)
        self.play(FadeIn(hd_l), Create(div), run_time=0.4)
        hear(self, "not checked", lead=0.15)
        self.play(FadeIn(hd_r), FadeIn(ghost5), run_time=0.4)
        # "not run this whole setup from start to finish": the documented items stamp in
        hear(self, "not run", lead=0.15)
        self.play(FadeIn(sub_l), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(s, scale=1.25) for s in left], lag_ratio=0.28), run_time=1.3)
        # "with read-only commands on Explorer"
        hear(self, "read only", lead=0.2)
        self.play(FadeIn(sub_r), run_time=0.3)
        # the five read-only checks, each on its words
        hear(self, "partitions", lead=0.2)
        self.play(FadeIn(right[0], scale=1.25), run_time=0.35)
        hear(self, "H200", lead=0.2)
        self.play(FadeIn(right[1], scale=1.25), run_time=0.35)
        hear(self, "on the login node", lead=0.3)
        self.play(FadeIn(right[2], scale=1.25), run_time=0.35)
        hear(self, "proxy comes", lead=0.2)
        self.play(FadeIn(right[3], scale=1.25), run_time=0.35)
        hear(self, "scratch", lead=0.2)
        self.play(FadeIn(right[4], scale=1.25), FadeOut(ghost5), run_time=0.35)
        # "Research Computing has a post on running Ollama in a container"
        hear(self, "Research computing", lead=0.2)
        self.play(FadeIn(oll), FadeIn(rcp), run_time=0.5)
        # "no page we read ... whether automated agents are allowed"
        hear(self, "no page", lead=0.3)
        self.play(FadeIn(agent, shift=UP * 0.3), run_time=0.5)
        hear(self, "coding agents", lead=0.1)
        self.play(Create(ring), run_time=0.6)
        hear(self, "automated agents", lead=0.2)
        self.play(Indicate(agent, color=INK, scale_factor=1.04), run_time=0.6)
        done(self)


# ───────────────────────────────────── B100 ─────────────────────────────────────
def pF_arc_arrow(c, r, a0, a1, w=7, tip=0.28, color=INK):
    """An arc from angle a0 to a1 (radians, either way round) ending in a filled arrow tip."""
    arc = Arc(radius=r, start_angle=a0, angle=a1 - a0, arc_center=[c[0], c[1], 0], color=color, stroke_width=w)
    end = np.array([c[0] + r * np.cos(a1), c[1] + r * np.sin(a1), 0.0])
    d = 1.0 if a1 > a0 else -1.0
    tang = d * np.array([-np.sin(a1), np.cos(a1), 0.0])
    nrm = np.array([np.cos(a1), np.sin(a1), 0.0])
    base = end - tang * tip
    tri = Polygon(end + tang * tip * 0.4, base + nrm * tip * 0.6, base - nrm * tip * 0.6,
                  fill_color=color, fill_opacity=1, stroke_width=0)
    return VGroup(arc, tri)


def pF_strand(x0, y0, x1, dy, amp=0.07, sw=4):
    """One frayed thread end: a wavy line from (x0, y0) to (x1, y0 + dy)."""
    pts = [[x0 + (x1 - x0) * t, y0 + dy * t + amp * np.sin(t * 14) * (0.3 + t), 0] for t in np.linspace(0, 1, 40)]
    m = VMobject(stroke_color=INK, stroke_width=sw)
    m.set_points_smoothly(pts)
    return m


class B100_WeakerAgent(Scene):
    """A context bar fills with system prompt, tool definitions and history while the agent loop turns and glitches; the thread frays."""
    def construct(self):
        title = pF_act_title("X · What To Expect")
        C = (0.6, 0.9)
        claude = logo_chip("claude", C[0], C[1])
        ring = VGroup(pF_arc_arrow(C, 1.5, np.radians(150), np.radians(30)),
                      pF_arc_arrow(C, 1.5, np.radians(-30), np.radians(-150)))
        # the context bar: a white track, then three block types stacking inside it
        track = Rectangle(width=11.8, height=0.8, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0, -2.2, 0])
        by = -2.2
        sysb = Rectangle(width=2.4, height=0.64, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.82 + 1.2, by, 0])
        tools = VGroup(*[Rectangle(width=0.2, height=0.64, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                         .move_to([-3.36 + 0.1 + 0.25 * i, by, 0]) for i in range(14)])
        hist = [Rectangle(width=0.9, height=0.64, fill_color=BOX_R, fill_opacity=1, stroke_width=0)
                .move_to([0.15 + 0.45 + 0.96 * i, by, 0]) for i in range(6)]
        l_sys = T("system prompt", 32).move_to([-4.62, -3.0, 0])
        l_tools = T("tool definitions", 32).move_to([-1.6, -3.0, 0])
        l_hist = T("history", 32).move_to([3.0, -3.0, 0])
        # the glitches on the loop
        gap = Rectangle(width=0.55, height=0.7, fill_color=STAGE, fill_opacity=1, stroke_width=0).move_to([C[0], C[1] + 1.5, 0])
        zig = VMobject(stroke_color=INK, stroke_width=6)
        zig.set_points_as_corners([[C[0] - 0.22, C[1] + 1.78, 0], [C[0] + 0.12, C[1] + 1.58, 0], [C[0] - 0.12, C[1] + 1.42, 0],
                                   [C[0] + 0.22, C[1] + 1.22, 0]])
        l_mal = T("malformed", 32).move_to([3.95, 2.05, 0])
        again = pF_arc_arrow(C, 1.85, np.radians(150), np.radians(30), w=6)
        l_loops = T("loops", 32).move_to([3.7, 0.35, 0])
        # the thread from the start of the work; its end frays
        ty = -1.25
        thread = Line([-5.82, ty, 0], [-0.1, ty, 0], color=INK, stroke_width=5)
        t_dot = Dot([-5.82, ty, 0], radius=0.11, color=TERRA)
        l_thr = T("thread", 32).move_to([-5.15, ty + 0.45, 0])
        strands = VGroup(pF_strand(-0.1, ty, 3.2, 0.38), pF_strand(-0.1, ty, 4.5, 0.0), pF_strand(-0.1, ty, 5.4, -0.34))
        l_files = T("many files", 32).move_to([4.3, ty + 0.62, 0])

        self.play(FadeIn(title), FadeIn(track), run_time=0.4)
        hear(self, "agent", lead=0.1)
        self.play(FadeIn(claude), run_time=0.4)
        # "Claude Code's loop is demanding": the loop turns
        hear(self, "loop", lead=0.3)
        self.play(Create(ring), run_time=0.5)
        self.play(Rotate(ring, angle=-2 * PI, about_point=[C[0], C[1], 0]), run_time=0.8, rate_func=smooth)
        # "a long system prompt"
        hear(self, "long system", lead=0.15)
        self.play(GrowFromEdge(sysb, LEFT), FadeIn(l_sys), run_time=0.6)
        # "dozens of tool definitions"
        hear(self, "dozens", lead=0.15)
        self.play(LaggedStart(*[GrowFromEdge(t, LEFT) for t in tools], lag_ratio=0.06), FadeIn(l_tools), run_time=0.9)
        # "a growing history": the first turns land before the midpoint, the rest after it
        hear(self, "growing", lead=0.3)
        self.play(LaggedStart(GrowFromEdge(hist[0], LEFT), GrowFromEdge(hist[1], LEFT), lag_ratio=0.5), FadeIn(l_hist), run_time=0.45)
        hear(self, "every turn", lead=0.15)
        self.play(LaggedStart(*[GrowFromEdge(h, LEFT) for h in hist[2:]], lag_ratio=0.25), run_time=0.9)
        # "more malformed tool calls": the call arrow breaks
        hear(self, "malformed", lead=0.25)
        self.add(gap)
        self.play(FadeIn(gap, run_time=0.01), Create(zig), FadeIn(l_mal), run_time=0.45)
        # "more loops": the call repeats and the loop keeps turning
        hear(self, "loops", lead=0.2)
        self.play(Create(again), FadeIn(l_loops), run_time=0.4)
        self.play(Rotate(ring, angle=-2 * PI, about_point=[C[0], C[1], 0]), run_time=0.7, rate_func=smooth)
        # "an earlier loss of the thread": the thread runs out from the start, then frays
        hear(self, "earlier", lead=0.1)
        self.play(FadeIn(t_dot), Create(thread), FadeIn(l_thr), run_time=0.5)
        hear(self, "thread", lead=0.1)
        self.play(*[Create(s) for s in strands], run_time=0.7)
        # "big changes across many files"
        hear(self, "many files", lead=0.2)
        self.play(FadeIn(l_files), run_time=0.3)
        done(self)


# ───────────────────────────────────── B101 ─────────────────────────────────────
class B101_WhereItWorks(Scene):
    """Two columns: four chips with a check each for what it does well, three with a cross each for what it does poorly."""
    def construct(self):
        hd_w = T("does well", 48)
        hd_w.move_to([-5.2 + hd_w.width / 2, 2.6, 0])
        hd_p = T("does poorly", 48)
        hd_p.move_to([1.1 + hd_p.width / 2, 2.6, 0])
        div = DashedLine([0, 3.0, 0], [0, -2.5, 0], color=BAR2, stroke_width=4, dash_length=0.2)
        ys = [1.4, 0.35, -0.7, -1.75]

        def row(text, x_left, y, good):
            c = chip(text, 0, y, size=36)
            c.move_to([x_left + c.width / 2 - 0.0, y, 0])
            c.shift(RIGHT * 0.0)
            mk = check(x_left - 0.5, y, s=0.2, color=TERRA, w=9) if good else x_mark(x_left - 0.45, y, r=0.24, w=8)
            return c, mk

        good = [row(s, -5.2, y, True) for s, y in zip(["clear tasks, clear tests", "bulk batch work", "stays on Northeastern", "teaching"], ys)]
        poor = [row(s, 1.1, y, False) for s, y in zip(["open-ended refactors", "long debugging", "costly wrong calls"], ys)]

        ghosts = [DashedVMobject(RoundedRectangle(width=4.5, height=0.8, corner_radius=0.4, stroke_color=BAR2, stroke_width=4),
                                 num_dashes=44).move_to([1.1 + 2.25, y, 0]) for y in ys[:3]]

        def land(self, pair, dx, ghost=None):
            c, mk = pair
            extra = [FadeOut(ghost)] if ghost is not None else []
            self.play(FadeIn(c, shift=RIGHT * dx), Create(mk), *extra, run_time=0.4)

        hear(self, "does well", lead=0.2)
        self.play(FadeIn(hd_w), FadeIn(hd_p), Create(div), *[FadeIn(g) for g in ghosts], run_time=0.5)
        hear(self, "clear tasks", lead=0.2)
        land(self, good[0], 0.3)
        hear(self, "bulk", lead=0.2)
        land(self, good[1], 0.3)
        hear(self, "code that should", lead=0.2)
        land(self, good[2], 0.3)
        hear(self, "teaching", lead=0.2)
        land(self, good[3], 0.3)
        hear(self, "does poorly", lead=0.2)
        self.play(Indicate(hd_p, color=INK, scale_factor=1.06), run_time=0.4)
        hear(self, "open", lead=0.2)
        land(self, poor[0], 0.3, ghosts[0])
        hear(self, "long debugging", lead=0.2)
        land(self, poor[1], 0.3, ghosts[1])
        hear(self, "anything where", lead=0.2)
        land(self, poor[2], 0.3, ghosts[2])
        done(self)


# ───────────────────────────────────── B102 ─────────────────────────────────────
class B102_PracticalSplit(Scene):
    """Small work crates ride the belt into the local-model rack; one heavy crate goes to the Claude chip; two receipts end it."""
    def construct(self):
        belt_hi = pF_belt(-6.0, 2.1, 1.75)
        belt_lo = pF_belt(-6.0, 1.9, -0.7)
        iso = Iso(3.9, 0.85, 0.9)
        stack, lights = explorer_rack(iso)
        rack = VGroup(stack, lights)
        rack_lab = T("local model", 34).move_to([3.9, 0.4, 0])
        claude = logo_chip("claude", 3.4, -0.7)
        front = T("frontier", 32).move_to([5.45, -0.7, 0])
        names = ["drafts", "boilerplate", "tests", "batch"]
        cues = ["drafting", "boilerplate", "tests", "batch passes"]
        smalls = []
        for nm in names:
            cr = pF_crate(0, 0, s=0.5)
            lb = T(nm, 32).move_to([0, 1.05, 0])
            smalls.append(VGroup(cr, lb))
        heavy = VGroup(pF_crate(0, 0, s=0.7, dark=True), T("hard problem", 32).move_to([0, 1.55, 0]))
        rec1 = chip("real savings", -2.9, -2.45)
        ck = check(-5.0, -2.45, s=0.24, color=TERRA, w=10)
        rec2 = chip("same thing, free", 2.5, -2.45)
        xm = x_mark(4.95, -2.45, r=0.3, w=9)

        # "A practical split": two lanes, the Claude chip at the end of the lower one
        hear(self, "practical split", lead=0.2)
        self.play(Create(belt_hi), Create(belt_lo), FadeIn(claude), run_time=0.6)
        # "the local model": the rack and its name
        hear(self, "the local model", lead=0.1)
        self.play(FadeIn(rack), FadeIn(rack_lab), run_time=0.5)
        # "drafting, boilerplate, tests and batch passes ... the hard problems": one clock-driven span, all done before the midpoint
        t0 = pF_when(self, "drafting", lead=0.2, default=1.7)
        tt = [pF_when(self, c, lead=0.2, default=t0 + 0.5 * i) for i, c in enumerate(cues)]
        t_front = pF_when(self, "frontier", lead=0.2, default=4.6)
        t_go = pF_when(self, "for the hard", lead=0.0, default=5.4)
        t_end = min(t_go + 0.6, 6.0)
        clock = VGroup(*smalls, heavy, front, lights)   # the clock's mobject: the renderer redraws only what an animation holds
        for g in smalls + [heavy, front]:
            g.set_opacity(0)
        self.add(clock)
        speed, x_in, x_out = 3.6, -4.1, 2.35
        sy, hy = 2.49, 0.26
        hx0, hx1 = -1.6, 1.35
        arrive = [t + (x_out - x_in) / speed for t in tt]

        def tick(t):
            for g, ts, ta in zip(smalls, tt, arrive):
                a_in = pF_clamp((t - ts) / 0.25)
                a_out = pF_clamp((t - ta) / 0.25)
                x = min(x_in + speed * max(0.0, t - ts), x_out)
                g.set_opacity(a_in * (1 - a_out))
                g.move_to([x, sy - 0.35 * a_out, 0])
            for i, ta in enumerate(arrive):
                if t >= ta:
                    lights[i // 2].set_color(TERRA)
            front.set_opacity(pF_clamp((t - t_front) / 0.3))
            ah = pF_clamp((t - t_front) / 0.3)
            m = pF_clamp((t - t_go) / max(0.1, t_end - t_go))
            m = m * m * (3 - 2 * m)
            heavy.set_opacity(ah)
            heavy.move_to([hx0 + (hx1 - hx0) * m, hy, 0])

        at(self, t0)
        start = _elapsed(self)
        span = t_end - start
        if span > 0.2:
            self.play(UpdateFromAlphaFunc(clock, lambda m, a: tick(start + a * span)), run_time=span, rate_func=linear)
        # "Measured that way, the savings are real"
        hear(self, "savings", lead=0.35)
        self.play(FadeIn(rec1, shift=DOWN * 0.3), Create(ck), run_time=0.5)
        # "Measured as the same thing for free, they are not"
        hear(self, "same thing", lead=0.25)
        self.play(FadeIn(rec2, shift=DOWN * 0.3), run_time=0.4)
        hear(self, "not", lead=0.1, nth=0)
        self.play(Create(xm), run_time=0.35)
        done(self)
