# ═════════════════════════════ PART A · Act I (B10 B11 B12), Act II (B20), Act III (B30), Act VI (B60) ═════════════════════════════
# Stage map. Act I is one picture built up and reused: a laptop at left, the login node (a one-slab server),
# the Slurm gate over a belt, and a wall of three compute racks (aicr_rack) at right. B10 draws it; B12 spreads
# the racks and plumbs them; B60 is B10 again with the X. B11 is the counter beat (fills the frame). B20 is two
# doors. B30 is the two interfaces, shown as themselves (dark terminal, pale browser), cabled to one login node.
PA_KRAFT = "#9C8462"                        # deep-kraft connector (cables are never ink: ink cables fuse the things they join)
PA_SMALL = "#917A55"                        # dark kraft: outlines of SMALL objects only
PA_BELT = "#E4E0D4"                         # belts, pads and door frames stay within 28 of the stage (Gate V)
PA_LOGIN = Iso(-2.6, -2.1, 0.7)             # the login node (B10, B60)
PA_LAPTOP = Iso(-5.1, -2.0, 0.6)            # the laptop (B10)
PA_GATE = Iso(0.4, -2.05, 0.6)              # the Slurm gate (B10, B60)
PA_GATE_PIVOT = PA_GATE.p(0.11, 0.9, 1.0)   # the boom turns on the far post
PA_RACKS = [Iso(2.2, -1.6, 0.42), Iso(3.75, -1.6, 0.42), Iso(5.3, -1.6, 0.42)]      # the compute wall (B10, B60)
PA_RACKS_WIDE = [Iso(-1.0, -1.6, 0.42), Iso(1.6, -1.6, 0.42), Iso(4.2, -1.6, 0.42)]  # the same racks, spread (B12)
PA_RACK_TOP = 2.0                           # z of an aicr_rack's top face (4 slabs)


def pa_title(s):
    """Act title, top-left, for the whole first beat of an act."""
    t = T(s, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def pa_at(mob, x_left, y):
    """Place a text by its LEFT edge."""
    return mob.move_to([x_left + mob.width / 2, y, 0])


def pa_slide_in(self, mob, vec, rt=0.7):
    """Slide a whole object in from off-stage, fully opaque (GATE T: never a half-faded dark block)."""
    rt = guard(self, rt)
    mob.shift(-vec)
    self.add(mob)
    self.play(mob.animate.shift(vec), run_time=rt)


def pa_drop(self, mobs, rt=0.55, lag=0.2, dist=5.0):
    rt = guard(self, rt)
    mobs = list(mobs)
    for m in mobs:
        m.shift(UP * dist)
        self.add(m)
    self.play(LaggedStart(*[m.animate.shift(DOWN * dist) for m in mobs], lag_ratio=lag), run_time=rt, rate_func=ease_in)


def pa_xmark(x, y, s=0.3, color=TERRA, w=10):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def pa_cable(a, b, w=5):
    return Line(a, b, color=PA_KRAFT, stroke_width=w)


def pa_belt(x0, x1, y, dx=0.3, h=0.3, th=0.2):
    """A flat belt running left-right: front strip, top, pale centre dashes (edges dark kraft, never ink)."""
    front = Polygon([x0, y - th, 0], [x1, y - th, 0], [x1, y, 0], [x0, y, 0],
                    fill_color=BOX_R, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    top = Polygon([x0, y, 0], [x1, y, 0], [x1 + dx, y + h, 0], [x0 + dx, y + h, 0],
                  fill_color=PA_BELT, fill_opacity=1, stroke_color=PA_SMALL, stroke_width=3)
    mid = DashedLine([x0 + 0.45, y + h / 2, 0], [x1 - 0.15, y + h / 2, 0], color=GHOST, stroke_width=3, dash_length=0.14)
    return VGroup(front, top, mid).set_z_index(-1)


def pa_login(iso=PA_LOGIN):
    """The login node: ONE dark slab with one light (smaller than the two-slab Explorer rack)."""
    return iso.server(0, 0, 0, w=1.4, d=1.4, slab=0.5, n=1)


def pa_laptop(iso=PA_LAPTOP):
    """A small laptop: kraft base, dark screen standing on the back edge."""
    base = iso.box(0, 0, 0, 1.2, 0.9, 0.08)
    screen = iso.quad([(0, 0.9, 0.08), (1.2, 0.9, 0.08), (1.2, 0.9, 0.85), (0, 0.9, 0.85)], DARK_TOP)
    return VGroup(base, screen)


def pa_gate(iso=PA_GATE):
    """The Slurm gate: two dark posts straddling the belt, a boom between them. Returns (far, boom, near)."""
    far = iso.box(0, 0.9, 0, 0.22, 0.22, 1.1, DARK_TOP, DARK_L, DARK_R)
    near = iso.box(0, -0.5, 0, 0.22, 0.22, 1.1, DARK_TOP, DARK_L, DARK_R).set_z_index(6)
    boom = Line(PA_GATE_PIVOT, iso.p(0.11, -0.39, 1.0), color=DARK_L, stroke_width=14).set_z_index(5)
    return far, boom, near


def pa_racks(isos=PA_RACKS):
    """The compute wall: three aicr racks, farthest drawn first. Returns (stacks, lights) as two VGroups."""
    stacks, lights = [], []
    for iso in reversed(isos):
        st, li = aicr_rack(iso)
        stacks.append(st); lights.append(li)
    return VGroup(*stacks), VGroup(*lights)


def pa_token(x, y):
    """A person token standing with its feet at (x, y)."""
    b = np.array([x, y, 0.0])
    body = Polygon(b + np.array([-0.2, 0, 0]), b + np.array([0.2, 0, 0]), b + np.array([0.1, 0.5, 0]), b + np.array([-0.1, 0.5, 0]),
                   fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    head = Circle(radius=0.18, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(b + np.array([0, 0.66, 0]))
    return VGroup(body, head).set_z_index(7)


def pa_light_up(self, lights, rt=0.5):
    self.play(LaggedStart(*[l.animate.set_color(TERRA) for l in lights], lag_ratio=0.2), run_time=rt)


# ─────────────── B10 · laptop → login node → Slurm gate → compute racks ───────────────
B10_JOB_AT = (0.75, 0.1, 0.5)                 # the job box on the login node's top face
B10_PAGE_AT = (0.0, 0.8, 0.5)


def b10_job(iso=PA_LOGIN):
    return job_box(iso, *B10_JOB_AT, s=0.55).set_z_index(3)


def b10_page(iso=PA_LOGIN):
    return iso.page(*B10_PAGE_AT, 0.65, 0.75).set_z_index(3)


def b10_labels():
    return (T("login node", 40).move_to([-2.6, -2.6, 0]), T("Slurm", 40).move_to([0.1, 0.15, 0]),
            T("compute nodes", 40).move_to([3.75, -2.4, 0]))


class B10_ClusterShape(Scene):
    def construct(self):
        self.add(pa_title("I · What A Cluster Is"), pa_laptop())
        l_login, l_slurm, l_comp = b10_labels()
        until(self, "many computers")
        stacks, lights = pa_racks()
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.3) for s in stacks], lag_ratio=0.3), run_time=0.9)
        self.add(lights, l_comp)
        until(self, "You log in")
        login_st, login_li = pa_login()
        pa_slide_in(self, VGroup(login_st, login_li), UP * 4.5, 0.6)
        self.play(Create(pa_cable([-4.45, -1.88, 0], [-3.5, -1.88, 0])), run_time=0.4)
        self.add(l_login)
        until(self, "Light work")
        job = b10_job()
        pa_drop(self, [job], 0.45)
        until(self, "editing a file")
        page = b10_page()
        pa_drop(self, [page], 0.4, dist=3.0)
        until(self, "looking around")
        self.play(Indicate(page, color=None, scale_factor=1.15), run_time=0.5)
        until(self, "When you need")
        belt = pa_belt(-1.6, 1.9, -1.75)
        self.play(GrowFromEdge(belt, LEFT), run_time=0.6)
        self.play(job.animate.shift(np.array([1.1, -0.2, 0.0])), run_time=0.5)          # down onto the belt
        until(self, "the work moves")
        far, boom, near = pa_gate()
        self.play(GrowFromCenter(VGroup(far, boom, near)), run_time=0.4)
        self.play(job.animate.shift(RIGHT * 0.6), run_time=0.5)                             # up to the gate
        until(self, "called Slurm")
        self.play(FadeIn(l_slurm), run_time=0.25)
        self.play(Rotate(boom, angle=2 * PI / 3, about_point=PA_GATE_PIVOT), run_time=0.5)
        until(self, "manages everyone")
        self.play(job.animate.shift(RIGHT * 2.0), run_time=0.8)                             # through the gate
        self.play(job.animate.shift(np.array([0.55, 1.1, 0.0])), run_time=0.45)           # onto the first rack
        pa_light_up(self, lights[2], 0.4)
        done(self)


# ─────────────── B11 · 45,000 cores, 525+ GPUs, free, Holyoke ───────────────
B11_P, B11_S, B11_BOT = 0.22, 0.17, -3.1       # cell pitch, square side, grid bottom; ten squares to a column
B11_XL, B11_XR = -6.0, 1.0                      # left edge of each grid (25 columns, then 10)
B11_CX_L, B11_CX_R = B11_XL + 12.5 * B11_P, B11_XR + 5 * B11_P
B11_RACK_A, B11_RACK_B = Iso(-4.9, 1.35, 0.5), Iso(-0.6, 1.35, 0.5)   # Discovery's place, then Explorer's arrival spot
B11_BLDG = Iso(5.0, -2.6, 0.6)


def b11_grid(x0, n, fill):
    """n squares, ten to a column, filled from the bottom, column by column from the left. Returns the columns."""
    cols = []
    for c in range((n + 9) // 10):
        k = min(10, n - 10 * c)
        cols.append(VGroup(*[Square(side_length=B11_S, fill_color=fill, fill_opacity=1, stroke_width=0)
                             .move_to(np.array([x0 + B11_P * (c + 0.5), B11_BOT + B11_P * (r + 0.5), 0.0]))
                             for r in range(k)]))
    return cols


def b11_counts(labels, x):
    """One numeral per column; only one is ever visible."""
    return [T(s, 90).move_to([x, 0.3, 0]) for s in labels]


def b11_fill(self, cols, nums, rt):
    """The squares fill column by column while the counter climbs with them (one play, any frame rate)."""
    n = len(cols)
    for m in cols + nums:
        m.set_opacity(0)
    self.add(*cols, *nums)
    holder = VGroup(*cols, *nums)

    def upd(m, a):
        k = min(n, int(a * n + 0.5))
        for i, c in enumerate(cols):
            c.set_opacity(1.0 if i < k else 0.0)
        for i, t in enumerate(nums):
            t.set_opacity(1.0 if i == k - 1 else 0.0)

    self.play(UpdateFromAlphaFunc(holder, upd), run_time=rt, rate_func=linear)
    upd(holder, 1.0)


def b11_pale(rack):
    """The older Discovery cluster: the same two-slab rack, drawn pale."""
    st, li = rack
    for s in st:
        s.set_fill(GHOST).set_stroke(BAR2)
    li.set_color(BAR3)
    return VGroup(st, li)


def b11_building():
    return VGroup(B11_BLDG.box(0, 0, 0, 1.4, 1.2, 0.6), B11_BLDG.box(0.4, 0.35, 0.6, 0.6, 0.55, 0.55))


def b11_free_tag():
    return VGroup(pill(5.2, 2.0, 1.4, 0.62, GHOST), T("free", 40).move_to([5.2, 2.0, 0]))


class B11_ExplorerNumbers(Scene):
    def construct(self):
        slots = VGroup(*b11_grid(B11_XL, 250, BAR3), *b11_grid(B11_XR, 100, BAR3))
        disc = b11_pale(explorer_rack(B11_RACK_A))
        l_disc = T("Discovery", 44).move_to([-3.15, 1.9, 0])
        self.add(slots, disc, l_disc)
        until(self, "Explorer is", lead=0.1)
        est, eli = explorer_rack(B11_RACK_B)
        exp = VGroup(est, eli)
        pa_slide_in(self, exp, LEFT * 7, 0.6)
        l_exp = T("Explorer", 44).move_to([1.15, 1.9, 0])
        self.add(l_exp)
        until(self, "run by the Research")
        team = VGroup(*[pa_token(x, 1.35) for x in (2.7, 3.2, 3.7)])
        self.play(LaggedStart(*[GrowFromCenter(t) for t in team], lag_ratio=0.3), run_time=0.5)
        self.add(T("Research Computing", 34).move_to([3.2, 2.6, 0]))
        until(self, "replaced the older")
        self.play(FadeOut(disc), FadeOut(l_disc), run_time=0.35)
        self.play(exp.animate.shift(LEFT * 4.3), l_exp.animate.shift(LEFT * 4.3), run_time=0.6)
        until(self, "Forty-five thousand")
        cpu_labels = [f"{1800 * (c + 1):,}" for c in range(25)]
        b11_fill(self, b11_grid(B11_XL, 250, BAR1), b11_counts(cpu_labels, B11_CX_L), 1.5)
        self.add(T("CPU cores", 40).move_to([B11_CX_L, -0.5, 0]))
        until(self, "More than five hundred")
        gpu_labels = [str(int(round(525 * (c + 1) / 10))) for c in range(9)] + ["525+"]
        b11_fill(self, b11_grid(B11_XR, 100, DARK_L), b11_counts(gpu_labels, B11_CX_R), 1.1)
        self.add(T("GPUs", 40).move_to([B11_CX_R, -0.5, 0]))
        until(self, "Free of charge")
        pa_drop(self, [b11_free_tag()], 0.45, dist=2.0)
        until(self, "It lives at")
        self.play(GrowFromCenter(b11_building()), run_time=0.5)
        until(self, "in Holyoke", lead=0.35)
        self.play(FadeIn(T("Holyoke, MA", 34).move_to([4.8, -0.6, 0]), shift=UP * 0.2), run_time=0.3)
        done(self)


# ─────────────── B12 · around the compute: 10 GbE in and out, 6 PB storage, InfiniBand between nodes ───────────────
B12_CAMPUS = Iso(-5.0, -2.0, 0.6)
B12_STORE = Iso(-4.6, 0.9, 0.55)
B12_PIPE_Y = -1.3


def b12_campus():
    return VGroup(B12_CAMPUS.box(0, 0, 0, 1.2, 1.2, 0.5), B12_CAMPUS.box(0.35, 0.35, 0.5, 0.5, 0.5, 0.45))


def b12_storage():
    """A dark storage block with three light drive bays on its front."""
    iso = B12_STORE
    body = iso.box(0, 0, 0, 1.7, 1.4, 1.0, DARK_TOP, DARK_L, DARK_R)
    bays = VGroup(*[iso.quad([(0.22 + 0.5 * k, 0, 0.3), (0.52 + 0.5 * k, 0, 0.3), (0.52 + 0.5 * k, 0, 0.7), (0.22 + 0.5 * k, 0, 0.7)],
                             GHOST, sw=0) for k in range(3)])
    return VGroup(body, bays)


def b12_pipe(a, b, w=16):
    """A pipe: a thick grey line (BAR1, never ink: an ink pipe fuses the blocks it joins)."""
    return Line(a, b, color=BAR1, stroke_width=w)


def b12_links(y):
    """One short link in each of the two gaps between the spread racks."""
    return VGroup(b12_pipe([0.12, y, 0], [0.83, y, 0], 10), b12_pipe([2.72, y, 0], [3.43, y, 0], 10))


def b12_jobs():
    return [job_box(iso, 0.6, 0.3, PA_RACK_TOP, s=s) for iso, s in zip(PA_RACKS_WIDE, (0.5, 0.7, 0.9))]


class B12_Plumbing(Scene):
    def construct(self):
        stacks, lights = pa_racks()
        l_comp = T("compute nodes", 40).move_to([3.75, -2.4, 0])
        self.add(stacks, lights, l_comp)
        until(self, "Around the compute", lead=0.0)
        shifts = [RIGHT * (w.ox - r.ox) for r, w in zip(PA_RACKS, PA_RACKS_WIDE)]
        self.play(*[VGroup(stacks[2 - k], lights[2 - k]).animate.shift(shifts[k]) for k in range(3)], FadeOut(l_comp), run_time=0.7)
        self.play(GrowFromCenter(b12_campus()), run_time=0.4)
        self.add(T("campus", 40).move_to([-4.9, -2.5, 0]))
        until(self, "a ten-gigabit link")
        pipe = b12_pipe([-4.0, B12_PIPE_Y, 0], [-1.85, B12_PIPE_Y, 0])
        self.play(GrowFromEdge(pipe, LEFT), run_time=0.6)
        self.add(T("10 GbE", 40).move_to([-2.95, -0.75, 0]))
        until(self, "for moving data")
        d1, d2 = Dot([-3.8, B12_PIPE_Y, 0], radius=0.1, color=TERRA), Dot([-2.05, B12_PIPE_Y, 0], radius=0.1, color=TERRA)
        self.add(d1, d2)
        self.play(d1.animate.shift(RIGHT * 1.75), d2.animate.shift(LEFT * 1.75), run_time=0.7)
        self.play(FadeOut(d1), FadeOut(d2), run_time=0.2)
        until(self, "six petabytes")
        pa_slide_in(self, b12_storage(), DOWN * 5, 0.6)
        self.add(T("6 PB", 44).move_to([-2.7, 1.6, 0]))
        self.play(Create(b12_pipe([-3.75, 0.95, 0], [-1.4, 0.4, 0], 12)), run_time=0.4)
        until(self, "between the nodes")
        self.play(Create(b12_links(-0.95)), run_time=0.5)
        until(self, "or InfiniBand")
        self.play(Create(b12_links(-0.6)), run_time=0.5)
        self.play(FadeIn(T("InfiniBand · 100–200 Gbps", 34).move_to([1.6, 0.75, 0])), run_time=0.3)
        until(self, "so every size")
        pa_drop(self, b12_jobs(), 0.8, 0.3, dist=4.0)
        pa_light_up(self, [l for li in lights for l in li], 0.6)
        done(self)


# ─────────────── B20 · two doors: research (PI, project command, access form) and classroom ───────────────
B20_FLOOR = -2.1
B20_DOOR_Y, B20_DOOR_W, B20_DOOR_H = -0.95, 1.5, 2.6
B20_X_RES, B20_X_CLS = -3.4, 2.6
B20_CAB = Iso(-1.1, -1.75, 0.65)
B20_PAGE = Iso(-5.7, -0.5, 0.6)


def b20_door(x, hinge):
    """A door seen from the front: a pale frame and a kraft panel with a terracotta knob. Returns (frame, panel, hinge_point)."""
    frame = Rectangle(width=B20_DOOR_W, height=B20_DOOR_H, fill_color=PA_BELT, fill_opacity=1,
                      stroke_color=INK, stroke_width=4).move_to([x, B20_DOOR_Y, 0])
    pw = B20_DOOR_W - 0.3
    panel = Rectangle(width=pw, height=B20_DOOR_H - 0.3, fill_color=BOX_R, fill_opacity=1, stroke_width=0).move_to([x, B20_DOOR_Y, 0])
    kx = x - hinge * (pw / 2 - 0.22)
    knob = Dot([kx, B20_DOOR_Y, 0], radius=0.08, color=TERRA)
    hp = np.array([x + hinge * pw / 2, B20_DOOR_Y, 0.0])
    return frame, VGroup(panel, knob), hp


def b20_open(self, panel, hp, rt=0.5):
    """Swing the panel on its hinge (a 3-D turn about the vertical: the panel narrows to a sliver)."""
    self.play(Rotate(panel, angle=-PI * 0.44, axis=UP, about_point=hp), run_time=rt)


def b20_page():
    return B20_PAGE.page(0, 0, 0, 0.9, 0.8)


class B20_TwoDoors(Scene):
    def construct(self):
        self.add(pa_title("II · Getting An Account"))
        f1, p1, h1 = b20_door(B20_X_RES, -1)
        f2, p2, h2 = b20_door(B20_X_CLS, +1)
        self.add(f1, p1, f2, p2)
        until(self, "For research", lead=0.1)
        pi, user = pa_token(-4.6, B20_FLOOR), pa_token(-5.3, B20_FLOOR)
        pa_slide_in(self, VGroup(pi, user), RIGHT * 2.5, 0.5)
        self.add(T("research", 42).move_to([B20_X_RES, 0.8, 0]))
        until(self, "every user belongs")
        cab = project_cabinet(B20_CAB)
        self.play(FadeIn(cab, shift=UP * 0.3), run_time=0.5)
        until(self, "owned by a PI")
        self.play(pi.animate.shift(UP * 0.3), run_time=0.4, rate_func=there_and_back)
        self.add(T("PI", 34).move_to([-4.6, -0.95, 0]))
        until(self, "thirty-five terabytes", lead=0.4)
        self.play(FadeIn(T("35 TB", 40).move_to([-1.0, 1.05, 0]), shift=UP * 0.2), run_time=0.3)
        until(self, "the PI adds you")
        self.play(pi.animate.shift(RIGHT * 0.3), run_time=0.3)
        b20_open(self, p1, h1, 0.5)
        until(self, "with the project command", lead=0.1)
        self.play(user.animate.shift(RIGHT * 3.0), run_time=0.9)                             # through the door, to the cabinet
        self.add(T("project command", 34).move_to([-1.3, -2.65, 0]))
        until(self, "or you file")
        page = b20_page()
        self.play(FadeIn(page, shift=DOWN * 0.3), run_time=0.3)
        self.add(T("access form", 34).move_to([-5.0, -2.65, 0]))
        self.play(page.animate.shift(RIGHT * 2.1), run_time=0.6)
        self.play(FadeOut(page), run_time=0.2)
        until(self, "requests a storage space")
        self.play(Indicate(cab, color=None, scale_factor=1.08), run_time=0.5)
        self.play(Create(check(-0.15, 0.35, 0.2, TERRA, 8)), run_time=0.35)
        until(self, "For coursework")
        inst = pa_token(4.1, B20_FLOOR)
        pa_slide_in(self, inst, LEFT * 2.5, 0.45)
        self.add(T("classroom", 42).move_to([B20_X_CLS, 0.8, 0]))
        until(self, "your instructor applies")
        self.play(inst.animate.shift(LEFT * 0.4), run_time=0.3)
        b20_open(self, p2, h2, 0.5)
        self.add(T("instructor", 34).move_to([4.6, -0.95, 0]))
        until(self, "students get in", lead=0.3)
        students = VGroup(*[pa_token(x, B20_FLOOR) for x in (4.7, 5.3, 5.9)])
        pa_slide_in(self, students, LEFT * 2.5, 0.45)
        self.play(LaggedStart(*[s.animate.shift(LEFT * d) for s, d in zip(students, (3.3, 4.4, 5.5))], lag_ratio=0.25), run_time=1.0)
        done(self)


# ─────────────── B30 · the terminal and the Open OnDemand site, both cabled to one login node ───────────────
B30_LOGIN = Iso(-0.4, -2.75, 0.7)
B30_TX, B30_BX, B30_WY = -3.9, 3.9, 0.9
B30_WW, B30_WH = 3.9, 2.6


def b30_terminal():
    panel = RoundedRectangle(width=B30_WW, height=B30_WH, corner_radius=0.1, fill_color=DARK_TOP, fill_opacity=1,
                             stroke_width=0).move_to([B30_TX, B30_WY, 0])
    prompt = M("$", 44, CARD).move_to([B30_TX - 1.5, B30_WY + 0.9, 0])
    cur = Rectangle(width=0.28, height=0.5, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([B30_TX - 0.95, B30_WY + 0.9, 0])
    return VGroup(panel, prompt, cur)


def b30_browser():
    win = RoundedRectangle(width=B30_WW, height=B30_WH, corner_radius=0.1, fill_color=CARD, fill_opacity=1,
                           stroke_color=GHOST, stroke_width=3).move_to([B30_BX, B30_WY, 0])
    bar = Rectangle(width=B30_WW, height=0.5, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([B30_BX, B30_WY + B30_WH / 2 - 0.25, 0])
    dots = VGroup(*[Dot([B30_BX - 1.6 + i * 0.3, B30_WY + B30_WH / 2 - 0.25, 0], radius=0.07, color=GHOST) for i in range(3)])
    return VGroup(win, bar, dots)


def b30_rows():
    return VGroup(*[pill(2.4 + w / 2, y, w, 0.36, BAR2) for w, y in ((2.4, 1.3), (1.8, 0.7), (2.8, 0.1))])


def b30_cables():
    return (pa_cable([B30_TX + 1.5, B30_WY - B30_WH / 2, 0], [-0.9, -1.62, 0]),
            pa_cable([B30_BX - 1.5, B30_WY - B30_WH / 2, 0], [0.1, -1.62, 0]))


class B30_TwoWaysIn(Scene):
    def construct(self):
        self.add(pa_title("III · Logging In"))
        st, li = pa_login(B30_LOGIN)
        self.add(st, li, T("login node", 40).move_to([2.0, -2.4, 0]))
        until(self, "The terminal", lead=0.15)
        term = b30_terminal()
        pa_slide_in(self, term, RIGHT * 7, 0.6)
        self.add(T("terminal", 40).move_to([-4.4, -0.9, 0]))
        until(self, "Open OnDemand", lead=0.35)
        web = b30_browser()
        pa_slide_in(self, web, LEFT * 7, 0.6)
        self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in b30_rows()], lag_ratio=0.3), run_time=0.4)
        self.add(T("Open OnDemand", 36).move_to([4.2, -0.9, 0]))
        until(self, "Both reach")
        c1, c2 = b30_cables()
        self.play(Create(c1), Create(c2), run_time=0.6)
        pa_light_up(self, li, 0.3)
        until(self, "comfortable with the terminal")
        self.play(Indicate(term, color=None, scale_factor=1.06), run_time=0.6)
        until(self, "use both", lead=0.6)
        d1, d2 = Dot(c1.get_start(), radius=0.1, color=TERRA), Dot(c2.get_start(), radius=0.1, color=TERRA)
        self.add(d1, d2)
        self.play(d1.animate.move_to(c1.get_end()), d2.animate.move_to(c2.get_end()), run_time=0.5)
        self.play(FadeOut(d1), FadeOut(d2), run_time=0.15)
        done(self)


# ─────────────── B60 · not on the login node: the job rides the belt through Slurm to a compute node ───────────────
class B60_LeaveTheLoginNode(Scene):
    def construct(self):
        self.add(pa_title("VI · Running Jobs"))
        login_st, login_li = pa_login()
        login = VGroup(login_st, login_li)
        job = b10_job()
        stacks, lights = pa_racks()
        l_login, l_slurm, l_comp = b10_labels()
        self.add(login, job, stacks, lights, l_login)
        until(self, "only used the login", lead=0.1)
        self.play(Indicate(login, color=None, scale_factor=1.08), run_time=0.6)
        until(self, "has to move")
        belt = pa_belt(-1.6, 1.9, -1.75)
        self.play(GrowFromEdge(belt, LEFT), run_time=0.6)
        far, boom, near = pa_gate()
        self.play(GrowFromCenter(VGroup(far, boom, near)), FadeIn(l_slurm), FadeIn(l_comp), run_time=0.4)
        until(self, "no scientific software")
        xm = pa_xmark(-3.5, -0.6)
        self.play(GrowFromCenter(xm), run_time=0.35)
        until(self, "big transfers")
        self.play(Indicate(xm, color=None, scale_factor=1.25), run_time=0.4)
        until(self, "or heavy work")
        self.play(Indicate(xm, color=None, scale_factor=1.25), run_time=0.4)
        until(self, "because its traffic")
        self.play(job.animate.shift(np.array([1.1, -0.2, 0.0])), run_time=0.4)          # down onto the belt
        self.play(Rotate(boom, angle=2 * PI / 3, about_point=PA_GATE_PIVOT), run_time=0.4)
        self.play(job.animate.shift(RIGHT * 2.6), run_time=0.7)                             # through the gate
        until(self, "slows the whole cluster", lead=0.0)
        self.play(job.animate.shift(np.array([0.55, 1.1, 0.0])), run_time=0.4)           # onto the first rack
        pa_light_up(self, lights[2], 0.4)
        done(self)
