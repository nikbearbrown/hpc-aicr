# ═════════════════════════════ PART A — B10 B11 B12 B13 B20 B22 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.
def pA_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pA_stopwatch(x, y, r=0.55):
    face = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    knob = Rectangle(width=0.26, height=0.16, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + r + 0.12, 0])
    hand = Line([x, y, 0], [x, y + r * 0.7, 0], color=INK, stroke_width=7)
    hub = Dot([x, y, 0], radius=0.07, color=INK)
    g = VGroup(knob, face, hand, hub)
    g.hand, g.cx, g.cy = hand, x, y
    return g


def pA_folder(x, y, w=1.7, h=1.1):
    """A flat kraft folder: tab, back, front (centre x, y)."""
    back = Rectangle(width=w, height=h * 0.8, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y - 0.1 * h, 0])
    tab = Rectangle(width=w * 0.38, height=h * 0.24, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x - w * 0.31, y + 0.4 * h, 0])
    front = Rectangle(width=w, height=h * 0.55, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y - 0.225 * h, 0])
    return VGroup(tab, back, front)


def pA_laptop(x, y, w=2.3, h=1.5):
    """A plain laptop slab: a flat rounded rectangle with a smaller screen rectangle."""
    body = RoundedRectangle(corner_radius=0.14, width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    screen = Rectangle(width=w - 0.4, height=h - 0.4, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(body, screen)


def pA_pipe(x0, x1, y, h=0.42):
    return Rectangle(width=x1 - x0, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([(x0 + x1) / 2, y, 0])


def pA_arrow(a, b, w=8):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], color=INK, stroke_width=w, buff=0, max_tip_length_to_length_ratio=0.5)


def pA_slot(iso, x0, y0, z0, w, d, h):
    """A dashed ghost outline of an empty rack slot (three visible faces)."""
    x1, y1, z1 = x0 + w, y0 + d, z0 + h
    faces = [[(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],
             [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
             [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    out = VGroup()
    for f in faces:
        poly = Polygon(*[iso.p(*q) for q in f], color=BAR1, stroke_width=5)
        out.add(DashedVMobject(poly, num_dashes=24))
    return out


def pA_cloud(cx, cy, s=1.0, sw=6):
    """A dotted cloud outline (union of five circles, outline walked by angle)."""
    lobes = [(-0.75, -0.12, 0.42), (-0.28, 0.2, 0.52), (0.32, 0.22, 0.48), (0.78, -0.1, 0.42), (0.05, -0.2, 0.46)]
    pts = []
    for (lx, ly, r) in lobes:
        for k in range(120):
            a = 2 * np.pi * k / 120
            px, py = lx + r * np.cos(a), ly + r * np.sin(a)
            inside = any((px - ox) ** 2 + (py - oy) ** 2 < (orr - 1e-3) ** 2 for (ox, oy, orr) in lobes if (ox, oy, orr) != (lx, ly, r))
            if not inside:
                pts.append((px, py))
    c = np.mean(pts, axis=0)
    pts.sort(key=lambda q: np.arctan2(q[1] - c[1], q[0] - c[0]))
    pts.append(pts[0])
    m = VMobject(stroke_color=BAR1, stroke_width=sw)
    m.set_points_as_corners([[cx + q[0] * s, cy + q[1] * s, 0] for q in pts])
    return DashedVMobject(m, num_dashes=46)


def pA_piece(text, cx, cy, w, fill=PAGE_TOP, shadow=BOX_L, size=32):
    """A plaque piece of an address: a pill-edged card carrying real mono text (outline-free)."""
    sh = Rectangle(width=w, height=0.8, fill_color=shadow, fill_opacity=1, stroke_width=0).move_to([cx + 0.09, cy - 0.09, 0])
    card = Rectangle(width=w, height=0.8, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([cx, cy, 0])
    lab = M(text, size).move_to([cx, cy, 0])
    g = VGroup(sh, card, lab)
    g.card, g.label = card, lab
    return g


# ───────────────────────────────────────────────────────────────────────────────────────────────
class B10_TheIdea(Scene):
    """You ask for a GPU: the node appears; the model drops in; the agent sends requests and uses your files; no per-token bill; the job clock ticks."""
    def construct(self):
        title = pA_act_title("I · The Idea And Its Layers")
        iso = Iso(2.2, -2.5, 1.2)
        rack, lights = explorer_rack(iso)
        rack_g = VGroup(rack, lights)
        slot = pA_slot(iso, 0, 0, 0.92, 1.3, 1.3, 0.42)
        slab = iso.box(0, 0, 0.92, 1.3, 1.3, 0.42)
        glab = T("GPU node", 36).move_to([2.2, -2.98, 0])
        mlab = T("model", 36).move_to([4.4, -0.4, 0])
        claude = logo_chip("claude", -4.3, -0.4)
        a1 = pA_arrow([-3.25, -0.2], [0.65, -0.2])
        a2 = pA_arrow([0.65, -0.58], [-3.25, -0.58])
        rl = T("requests", 34).move_to([-1.3, 0.2, 0])
        pl = T("replies", 34).move_to([-1.3, -0.98, 0])
        folder = pA_folder(-4.3, -2.5, 1.7, 1.1)
        tool = pA_arrow([-4.3, -1.2], [-4.3, -1.9])
        tlab = T("tools", 34).move_to([-3.5, -1.55, 0])
        flab = T("your files", 34).move_to([-2.25, -2.5, 0])
        tag = chip("per token", -1.8, 1.7, size=34)
        xm = x_mark(-0.3, 1.7, r=0.3, w=9)
        clock = pA_stopwatch(2.2, 1.6)
        jlab = T("job", 36).move_to([3.2, 1.6, 0])

        self.play(FadeIn(title), run_time=0.4)
        # "You ask Slurm for a GPU": the node appears, one slot waiting
        hear(self, "ask Slurm", lead=0.3)
        self.play(FadeIn(rack_g), FadeIn(glab), Create(slot), run_time=0.5)
        # "On that GPU you run an open model": the model block drops into the slot
        hear(self, "open model", lead=0.55)
        self.play(FadeIn(slab, shift=DOWN * 0.9), FadeOut(slot), run_time=0.5, rate_func=ease_in)
        self.play(lights[0].animate.set_color(TERRA), FadeIn(mlab), run_time=0.3)
        # "a coding agent like Claude Code": the Claude chip arrives
        hear(self, "like Claude", lead=0.35)
        self.play(FadeIn(claude), run_time=0.4)
        # "sends it requests": the request arrow lands before the clip midpoint
        hear(self, "sends it", lead=0.12)
        self.play(Create(a1), FadeIn(rl), run_time=0.35)
        # the reply comes back (just after the midpoint)
        hear(self, "requests and", lead=-0.35)
        self.play(Create(a2), FadeIn(pl), run_time=0.3)
        # "runs tools on your files": the folder, the tool arrow touching it
        hear(self, "runs tools", lead=0.15)
        self.play(FadeIn(folder), run_time=0.3)
        self.play(Create(tool), FadeIn(tlab), run_time=0.35)
        hear(self, "on your files", lead=0.2)
        self.play(FadeIn(flab), run_time=0.3)
        # "no per token bill": the price tag appears and is crossed out
        hear(self, "per token", lead=0.35)
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.3)
        hear(self, "bill", lead=0.15)
        self.play(Create(xm), run_time=0.3)
        # "the model is yours": the second light comes on
        hear(self, "yours", lead=0.2)
        self.play(lights[1].animate.set_color(TERRA), run_time=0.2)
        # "for as long as the job runs": the job clock ticks on the rack
        hear(self, "as long as", lead=0.3)
        self.play(FadeIn(clock), FadeIn(jlab), run_time=0.3)
        self.play(Rotate(clock.hand, angle=-2 * PI, about_point=[clock.cx, clock.cy, 0]), run_time=1.3, rate_func=linear)
        done(self)


class B11_ThreeLayers(Scene):
    """Three bands build bottom to top: model host (rack + Apptainer holding ollama), harness (Claude, aider, continue), transport (nothing, or an ssh tunnel)."""
    def construct(self):
        bx, bw = 1.375, 9.35
        ys = [-2.05, 0.0, 2.05]
        strips = [RoundedRectangle(corner_radius=0.2, width=bw, height=1.9, stroke_color=BAR2, stroke_width=4).move_to([bx, y, 0]) for y in ys]

        def side(s):
            t = T(s, 38)
            return t

        l1, l2, l3 = side("model host"), side("harness"), side("transport")
        for lab, y in ((l1, ys[0]), (l2, ys[1]), (l3, ys[2])):
            lab.move_to([-6.05 + lab.width / 2, y, 0])
        # band 1: GPU node rack + Apptainer container holding the ollama logo
        iso = Iso(-1.4, -2.9, 0.5)
        rk, lt = explorer_rack(iso)
        rack = VGroup(rk, lt)
        rlab = T("GPU node", 32).move_to([-1.4, -1.45, 0])
        cont = RoundedRectangle(corner_radius=0.18, width=3.4, height=1.1, fill_color=BOX_TOP, fill_opacity=1, stroke_color=KRAFT_DEEP, stroke_width=5).move_to([2.9, -2.3, 0])
        ollama = logo_chip("ollama", 2.9, -2.3, h=0.85)
        clab = T("Apptainer", 32).move_to([2.9, -1.45, 0])
        # band 2: the harness
        claude = logo_chip("claude", -0.6, 0.0, h=1.2)
        aider = chip("aider", 2.5, 0.0, mono=True, size=36)
        cont2 = logo_chip("continue", 5.0, 0.0, h=1.2)
        # band 3: the transport
        tline = DashedLine([-0.9, 1.6, 0], [5.3, 1.6, 0], color=BAR1, stroke_width=7, dash_length=0.25)
        nothing = chip("nothing", 2.2, 2.45, size=34)
        pipe = pA_pipe(-0.9, 5.3, 1.6, h=0.4)
        ssh = chip("ssh tunnel", 2.2, 2.45, mono=True, size=34)

        # "three layers": the three empty bands
        hear(self, "three layers", lead=0.3)
        self.play(*[FadeIn(s) for s in strips], run_time=0.5)
        # "The model host is Olama": label, then the ollama logo
        hear(self, "model host", lead=0.1)
        self.play(FadeIn(l1), run_time=0.3)
        hear(self, "is Olama", lead=0.2)
        self.play(FadeIn(ollama), run_time=0.3)
        # "inside an Apptainer container": the container wraps it
        hear(self, "inside an", lead=0.1)
        self.add(cont)
        cont.set_z_index(0); ollama.set_z_index(2)
        self.play(FadeIn(cont), FadeIn(clab), run_time=0.4)
        # "on a GPU node that Slurm gave you": the rack
        hear(self, "on a GPU", lead=0.25)
        self.play(FadeIn(rack), FadeIn(rlab), run_time=0.4)
        # "The harness is the coding agent": label (before the midpoint)
        hear(self, "The harness", lead=0.15)
        self.play(FadeIn(l2), run_time=0.3)
        # "Claude Code, Aider, or Continue": three harnesses, one by one
        hear(self, "Claude code", lead=0.0)
        self.play(FadeIn(claude), run_time=0.3)
        hear(self, "Claude code", lead=-0.55)        # Aider (heard as 'Ader') lands 0.55 s after 'Claude code'
        self.play(FadeIn(aider), run_time=0.3)
        hear(self, "or continue", lead=0.0)
        self.play(FadeIn(cont2), run_time=0.3)
        # "and the transport is whatever joins them"
        hear(self, "the transport", lead=0.15)
        self.play(FadeIn(l3), run_time=0.3)
        hear(self, "joins them", lead=0.3)
        self.play(Create(tline), run_time=0.5)
        # "nothing, if they share a machine"
        hear(self, "nothing if", lead=0.2)
        self.play(FadeIn(nothing), run_time=0.3)
        # "or an SSH tunnel": the line becomes a tunnel
        hear(self, "an SSH", lead=0.3)
        self.play(FadeOut(nothing), Create(pipe), run_time=0.35)
        self.play(FadeIn(ssh), run_time=0.3)
        done(self)


class B12_PatternA(Scene):
    """One GPU job holds the agent, the model and your repo; nothing crosses to the network; a check lands on the boundary."""
    def construct(self):
        bound = RoundedRectangle(corner_radius=0.35, width=7.8, height=4.7, stroke_color=INK, stroke_width=6).move_to([-2.0, -0.35, 0])
        blab = T("one GPU job", 38).move_to([-5.9 + 0.0, 2.55, 0])
        blab.move_to([-5.9 + blab.width / 2, 2.55, 0])
        claude = logo_chip("claude", -4.5, 0.55)
        ollama = logo_chip("ollama", -0.5, 0.55)
        arr = pA_arrow([-3.45, 0.55], [-1.5, 0.55])
        lh = M("localhost", 32).move_to([-0.5, -0.55, 0])
        folder = pA_folder(-4.6, -1.55, 1.7, 1.1)
        flab = T("your repo", 34).move_to([-2.65, -1.55, 0])
        cloud = pA_cloud(4.4, 0.55, 1.05)
        nlab = T("network", 34).move_to([4.4, -0.55, 0])
        netline = DashedLine([1.95, 0.55, 0], [3.2, 0.55, 0], color=BAR1, stroke_width=6, dash_length=0.2)
        xm = x_mark(2.58, 0.55, r=0.3, w=9)
        ring = Circle(radius=0.9, stroke_color=TERRA, stroke_width=7).move_to([-4.6, -1.55, 0])
        ck = check(1.9, 2.0, s=0.34, color=TERRA, w=13)

        # "keeps everything on the GPU node": the job boundary and its label
        hear(self, "everything", lead=0.4)
        self.play(Create(bound), FadeIn(blab), run_time=0.7)
        # "The agent": the Claude chip
        hear(self, "The agent", lead=0.2)
        self.play(FadeIn(claude), run_time=0.4)
        # "and the model": the arrow and the ollama logo
        hear(self, "the model", lead=0.15)
        self.play(Create(arr), FadeIn(ollama), run_time=0.4)
        # "in the same job": localhost
        hear(self, "same job", lead=0.3)
        self.play(FadeIn(lh), run_time=0.3)
        # "nothing crosses a network": the cloud, the line, the cross
        hear(self, "nothing crosses", lead=0.45)
        self.play(FadeIn(cloud), FadeIn(nlab), run_time=0.4)
        self.play(Create(netline), run_time=0.3)
        self.play(Create(xm), run_time=0.3)
        # "and your code": the repo folder (after the midpoint)
        hear(self, "your code", lead=0.2)
        self.play(FadeIn(folder), FadeIn(flab), run_time=0.4)
        # "stays on Northeastern storage": a ring pulse on the folder
        hear(self, "Northeastern", lead=0.2)
        self.add(ring)
        self.play(ring.animate.scale(1.5).set_stroke(opacity=0), run_time=0.8)
        self.remove(ring)
        # "Use it": the check lands on the boundary
        hear(self, "Use it", lead=0.2)
        self.play(Create(ck), run_time=0.4)
        done(self)


class B13_PatternB(Scene):
    """Laptop (you + Claude) -> ssh tunnel -> login node -> GPU node; a request packet travels and stops at the lock in front of the model."""
    def construct(self):
        yc = 0.4
        you = professor_bear("1x1", 1.7, seed="B13", x=-5.1, y=yc)
        ylab = T("you", 34).move_to([-5.1, yc - 1.15, 0])
        lap = pA_laptop(-2.95, yc, 2.1, 1.4)
        claude = logo_chip("claude", -2.95, yc, h=0.8)
        llab = T("laptop", 34).move_to([-2.95, yc - 1.15, 0])
        seg1 = pA_pipe(-1.75, 1.3, yc, h=0.42)
        seg2 = pA_pipe(1.3, 2.8, yc, h=0.42)
        tlab = M("ssh tunnel", 32).move_to([-0.6, yc + 0.85, 0])
        liso = Iso(1.3, yc - 0.93, 0.85)
        lrk, llt = explorer_rack(liso)
        login = VGroup(lrk, llt)
        lglab = T("login node", 34).move_to([1.3, yc - 1.4, 0])
        giso = Iso(4.85, yc - 1.2, 1.1)
        grk, glt = explorer_rack(giso)
        gpu = VGroup(grk, glt)
        gplab = T("GPU node", 34).move_to([4.85, yc - 1.75, 0])
        ollama = logo_chip("ollama", 4.85, yc - 0.1, h=1.0)
        lock = padlock(3.2, yc, s=0.7)
        pkt = Dot([-2.0, yc, 0], radius=0.15, color=TERRA)
        pkt2 = Dot([1.3, yc, 0], radius=0.15, color=TERRA)
        ring = Circle(radius=0.75, stroke_color=TERRA, stroke_width=7).move_to([4.85, yc - 0.1, 0])
        for m_, z in ((seg1, 0), (seg2, 0), (login, 2), (gpu, 2), (ollama, 3), (lock, 4), (pkt, 6), (pkt2, 6)):
            m_.set_z_index(z)

        # "Pattern B keeps your editor on your laptop": the laptop with Claude on its screen, then you
        hear(self, "keeps", lead=0.3)
        self.play(FadeIn(lap), FadeIn(claude), run_time=0.4)
        hear(self, "your editor", lead=0.3)
        self.play(FadeIn(you), FadeIn(ylab), run_time=0.4)
        hear(self, "your laptop", lead=0.25)
        self.play(FadeIn(llab), run_time=0.3)
        # "only the model's traffic": the packet leaves the laptop
        hear(self, "traffic", lead=0.2)
        self.play(FadeIn(pkt), run_time=0.3)
        # "through an SSH tunnel": the pipe grows, the packet rides it to the login node
        hear(self, "an SSH", lead=0.45)
        self.play(GrowFromEdge(seg1, LEFT), FadeIn(tlab), run_time=0.5)
        self.play(pkt.animate.move_to([1.3, yc, 0]), run_time=0.9, rate_func=smooth)
        # "to the login node": the small rack
        hear(self, "login node", lead=0.35)
        self.play(FadeIn(login), FadeIn(lglab), run_time=0.4)
        # "and on to the GPU node": the pipe continues, the big rack with the ollama logo
        hear(self, "on to", lead=0.04)
        self.play(GrowFromEdge(seg2, LEFT), FadeIn(gpu), FadeIn(gplab), FadeIn(ollama), run_time=0.5)
        # "so the model must be": a ring pulse on the model
        hear(self, "the model must", lead=0.15)
        self.add(ring)
        self.play(ring.animate.scale(1.5).set_stroke(opacity=0), run_time=0.7)
        self.remove(ring)
        # "reachable from the login node": the packet goes on from the login node to the model
        hear(self, "reachable", lead=0.1)
        self.play(pkt.animate.move_to([4.45, yc - 0.1, 0]), run_time=0.9, rate_func=smooth)
        self.play(FadeOut(pkt), run_time=0.2)
        # "that needs a lock in front of it": the padlock lands in front of the model
        hear(self, "needs a lock", lead=0.3)
        self.play(FadeIn(lock, shift=DOWN * 0.4), run_time=0.4)
        # a second packet runs up to the lock and stops there
        hear(self, "in front of it", lead=0.3)
        self.add(pkt2)
        self.play(pkt2.animate.move_to([2.8, yc, 0]), run_time=0.65, rate_func=smooth)
        self.play(pkt2.animate.shift(LEFT * 0.12), run_time=0.12)
        done(self)


class B20_OpenDoor(Scene):
    """A GPU node with its door open at 0.0.0.0: other users pull and delete a model; the door closes to 127.0.0.1 and they stop outside."""
    def construct(self):
        title = pA_act_title("II · Wrong Turns To Avoid")
        iso = Iso(3.4, -2.45, 1.5)
        rk, lt = explorer_rack(iso)
        rack = VGroup(rk, lt)

        def lface(ya, yb, za, zb):
            return [(0, ya, za), (0, yb, za), (0, yb, zb), (0, ya, zb)]

        recess = iso.quad(lface(0.1, 1.2, 0.08, 0.8), GHOST, sw=3)
        door_pts_closed = lface(0.1, 1.2, 0.08, 0.8)
        door_pts_open = [(0, 0.1, 0.08), (-1.1, 0.1, 0.08), (-1.1, 0.1, 0.8), (0, 0.1, 0.8)]
        door = iso.quad(door_pts_closed, BOX_L, sw=5)
        door_open = iso.quad(door_pts_open, BOX_L, sw=5)
        rc = iso.p(0, 0.85, 0.5)
        ollama = logo_chip("ollama", rc[0], rc[1], h=0.75)
        glab = T("GPU node", 36).move_to([5.0, 1.25, 0])
        recess.set_z_index(1); ollama.set_z_index(2); door.set_z_index(4)
        lab_open = chip("0.0.0.0", 5.0, -2.85, mono=True, size=34)
        lab_shut = chip("127.0.0.1", 5.0, -2.85, mono=True, size=34)
        # the four other users
        start = [(-5.5, -0.9), (-5.5, -1.5), (-5.5, -2.1), (-5.5, -2.7)]
        stop = [(1.45, -0.85), (1.0, -1.5), (0.4, -2.05), (-0.2, -2.6)]
        dots = [Dot([x, y, 0], radius=0.18, color=INK) for (x, y) in start]
        ulab = T("other users", 36).move_to([-4.0, -3.05, 0])
        blk = Iso(0.0, 0.0, 0.5).box(0, 0, 0, 0.9, 0.9, 0.7)
        plab = T("pull", 34)
        dlab = T("delete", 34)

        self.play(FadeIn(title), run_time=0.4)
        # "this setup": the node appears with its door shut
        hear(self, "this setup", lead=0.45)
        self.add(recess, ollama)
        self.play(FadeIn(rack), FadeIn(door), FadeIn(recess), FadeIn(ollama), FadeIn(glab), run_time=0.5)
        # "has no authentication": the door swings open
        hear(self, "has no", lead=0.25)
        self.play(Transform(door, door_open), run_time=0.6, rate_func=smooth)
        # "listens on every address": the 0.0.0.0 label
        hear(self, "listens on", lead=0.0)
        self.play(FadeIn(lab_open), run_time=0.3)
        # "on a shared cluster": four other users arrive
        hear(self, "on a shared", lead=0.3)
        self.play(*[FadeIn(d) for d in dots], FadeIn(ulab), run_time=0.4)
        # "opens the whole interface": they walk up to the open door
        hear(self, "opens the whole", lead=0.2)
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(dots, stop)], ulab.animate.move_to([-2.2, -3.05, 0]), run_time=0.9, rate_func=smooth)
        # "including pulling": the first one carries a model block in
        hear(self, "including", lead=0.3)
        blk.move_to([0.55, -0.7, 0]); plab.move_to([0.55, -0.15, 0])
        self.play(FadeIn(blk), FadeIn(plab), run_time=0.3)
        hear(self, "pulling", lead=0.3)
        self.play(blk.animate.move_to([2.2, -1.0, 0]).scale(0.5), dots[0].animate.move_to([1.9, -0.9, 0]), run_time=0.45, rate_func=smooth)
        self.play(FadeOut(blk), FadeOut(plab), dots[0].animate.move_to([1.45, -0.85, 0]), run_time=0.25)
        # "and deleting models": the second one reaches in and carries one away
        hear(self, "deleting", lead=0.3)
        dlab.move_to([0.3, -1.0, 0])
        blk2 = Iso(2.0, -1.3, 0.5).box(0, 0, 0, 0.9, 0.9, 0.7).scale(0.5)
        blk2.move_to([2.0, -1.4, 0])
        self.play(dots[1].animate.move_to([1.85, -1.5, 0]), FadeIn(blk2), run_time=0.35)
        self.play(dots[1].animate.move_to([0.0, -1.45, 0]), blk2.animate.move_to([-0.25, -1.65, 0]), FadeIn(dlab), run_time=0.7, rate_func=smooth)
        self.play(FadeOut(blk2), FadeOut(dlab), run_time=0.2)
        # "to anyone who can reach the node": the door swings closed to 127.0.0.1 and they stop outside
        hear(self, "who can reach", lead=0.25)
        self.play(Transform(door, iso.quad(door_pts_closed, BOX_L, sw=5)), FadeOut(lab_open), dots[1].animate.move_to([1.0, -1.5, 0]), run_time=0.6, rate_func=smooth)
        self.play(FadeIn(lab_shut), run_time=0.3)
        done(self)


class B22_BareBaseUrl(Scene):
    """Claude adds /v1/messages to a bare host and port (right); a base ending /v1 doubles it (404); the bare base gets the check."""
    def construct(self):
        yu, yl, ym = 1.7, -1.6, -0.1
        x0 = -4.0
        wb, ws = 5.22 + 0.5, 2.95 + 0.5
        wb2 = 5.95 + 0.5
        claude = logo_chip("claude", -5.2, ym, h=1.2)
        base = pA_piece("http://127.0.0.1:PORT", x0 + wb / 2, yu, wb)
        suf = pA_piece("/v1/messages", -2.3, ym, ws, fill=BOX_L, shadow=BOX_R)
        jx = x0 + wb + 0.04 + ws / 2                  # where the suffix joins the upper row
        brk = VGroup(Line([x0 + 0.1, 1.1, 0], [x0 + wb - 0.1, 1.1, 0], color=INK, stroke_width=6),
                     Line([x0 + 0.1, 1.1, 0], [x0 + 0.1, 1.3, 0], color=INK, stroke_width=6),
                     Line([x0 + wb - 0.1, 1.1, 0], [x0 + wb - 0.1, 1.3, 0], color=INK, stroke_width=6))
        bare = T("bare", 34).move_to([x0 + wb / 2, 0.68, 0])
        base2 = pA_piece("http://127.0.0.1:PORT/v1", x0 + wb2 / 2, yl, wb2)
        lab2 = base2.label
        ul = Line([lab2.get_right()[0] - 0.75, yl - 0.27, 0], [lab2.get_right()[0], yl - 0.27, 0], color=INK, stroke_width=8)
        suf2 = pA_piece("/v1/messages", -2.3, ym, ws, fill=BOX_L, shadow=BOX_R)
        jx2 = x0 + wb2 + 0.04 + ws / 2
        ring = Circle(radius=0.55, stroke_color=TERRA, stroke_width=8).move_to([x0 + wb2 + 0.02, yl, 0])
        tag = chip("404", x0 + wb2 + 0.02, -2.65, mono=True, size=38)
        ck = check(5.75, yu, s=0.3, color=TERRA, w=13)

        # "Second, the address": the bare base
        hear(self, "the address", lead=0.2)
        self.play(FadeIn(base), run_time=0.4)
        # "Claude Code adds slash v1 slash messages itself": the chip makes the suffix and slides it on
        hear(self, "Claude code", lead=0.35)
        self.play(FadeIn(claude), run_time=0.3)
        hear(self, "slash v1", lead=0.6)
        self.play(FadeIn(suf, shift=RIGHT * 0.3), run_time=0.25)
        self.play(suf.animate.move_to([jx, ym, 0]), run_time=0.45, rate_func=smooth)
        self.play(suf.animate.move_to([jx, yu, 0]), run_time=0.3, rate_func=smooth)
        # "a bare host and port": a bracket under the base
        hear(self, "a bare host", lead=0.35)
        self.play(Create(brk), FadeIn(bare), run_time=0.45)
        # "A base address": a second base, this one ending /v1 (after the clip midpoint)
        hear(self, "A base address", lead=0.1)
        self.play(FadeIn(base2), run_time=0.35)
        hear(self, "slash v1", lead=0.15, nth=1)
        self.play(Create(ul), run_time=0.3)
        # "doubles the path": the suffix slides in and collides
        hear(self, "doubles", lead=0.8)
        self.play(FadeIn(suf2, shift=RIGHT * 0.3), run_time=0.2)
        self.play(suf2.animate.move_to([jx2 + 0.6, ym, 0]), run_time=0.3, rate_func=smooth)
        self.play(suf2.animate.move_to([jx2 + 0.6, yl, 0]), run_time=0.25, rate_func=smooth)
        self.play(suf2.animate.move_to([jx2, yl, 0]), run_time=0.15, rate_func=ease_in)
        self.add(ring)
        self.play(ring.animate.scale(1.6).set_stroke(opacity=0), run_time=0.45)
        self.remove(ring)
        # "the request fails": the 404 tag lands
        hear(self, "request fails", lead=0.15)
        self.play(FadeIn(tag, shift=DOWN * 0.3), run_time=0.3)
        # "Give it the bare host and port": the check lands on the right one
        hear(self, "Give it", lead=0.25)
        self.play(Create(ck), run_time=0.4)
        done(self)
