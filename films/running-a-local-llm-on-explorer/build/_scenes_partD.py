# ═════════════════════════════ PART D — B53 B54 B60 B64 B72 ═════════════════════════════
# Cue times come from hear("spoken phrase"): the measured word times in _ASR. Labels are 1-3 words; real text only in mono.


def pD_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


# ── placement helpers: the iso origin is the left-back corner, so centre a block with these ──
def pD_rack(cx, cy, s=0.8):
    """explorer_rack centred on (cx, cy): returns (stack, lights). Its 2 slabs are 0.88 tall, 1.3 x 1.3."""
    iso = Iso(cx, cy - 1.09 * s, s)
    return explorer_rack(iso)


def pD_box(cx, cy, w=1.4, d=1.4, h=0.9, s=0.8):
    """A plain kraft block centred on (cx, cy)."""
    ox = cx - (w - d) / 2 * C30 * s
    oy = cy - ((w + d) / 4 + h / 2) * s
    return Iso(ox, oy, s).box(0, 0, 0, w, d, h)


def pD_job(cx, cy, s=0.85, b=0.8):
    """job_box centred on (cx, cy): a kraft box with one terracotta tape."""
    iso = Iso(cx, cy - (b * 2 / 4 + b * 0.8 / 2) * s, s)
    return job_box(iso, 0, 0, 0, s=b)


def pD_stopwatch(x, y, r=0.6):
    face = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    knob = Rectangle(width=0.26, height=0.16, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + r + 0.12, 0])
    hand = Line([x, y, 0], [x, y + r * 0.7, 0], color=INK, stroke_width=10)
    hub = Dot([x, y, 0], radius=0.1, color=INK)
    g = VGroup(knob, face, hand, hub)
    g.hand, g.cx, g.cy = hand, x, y
    return g


def pD_laptop(x, y, w=1.8):
    """Your laptop: a flat rounded slab with a smaller screen rectangle (grey outline, so it does not fuse with the slab)."""
    slab = RoundedRectangle(corner_radius=0.14, width=w, height=1.25, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    screen = Rectangle(width=w * 0.7, height=0.75, fill_color=BAR2, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([x, y + 0.1, 0])
    return VGroup(slab, screen)


def pD_gate(x, y):
    """The caddy gate: two kraft posts, a top bar and a closed panel across the lane. `.panel` opens (fades) for a valid token."""
    pl = Rectangle(width=0.3, height=2.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x - 0.8, y, 0])
    pr = Rectangle(width=0.3, height=2.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x + 0.8, y, 0])
    bar = Rectangle(width=1.9, height=0.3, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y + 1.0, 0])
    panel = Rectangle(width=1.3, height=1.9, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y - 0.1, 0])
    g = VGroup(pl, pr, panel, bar)
    g.panel = panel
    return g


def pD_gate_lock(x, y, s=0.5):
    """The padlock hangs on the gate's left post (so it stays put when the panel opens)."""
    lk = padlock(x - 0.8, y + 0.45, s=s)
    lk.set_z_index(6)
    return lk


def pD_packet(x, y, token=False):
    """A request packet: a small kraft envelope with one terracotta seal; with `token`, a key lies on top of it."""
    body = Rectangle(width=1.0, height=0.6, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    seal = Dot([x, y, 0], radius=0.1, color=TERRA)
    parts = [body, seal]
    if token:
        s = 0.36
        parts.append(key_obj(x - 0.85 * s, y + 0.62, s=s))
    return VGroup(*parts)


def pD_caution(x, y):
    """A caution mark: an ink-outlined white triangle with an exclamation mark."""
    tri = Polygon([x, y + 0.5, 0], [x - 0.55, y - 0.42, 0], [x + 0.55, y - 0.42, 0],
                  fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
    bang = T("!", 44, bold=True).move_to([x, y - 0.06, 0])
    return VGroup(tri, bang)


def pD_ring(cx, cy, w, h, color=TERRA):
    return RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=color, stroke_width=7, fill_opacity=0).move_to([cx, cy, 0])


def pD_road(x0, x1, y):
    """A road: a band with deep-kraft edges and pale ghost centre dashes (the kit's belt rule)."""
    band = Rectangle(width=x1 - x0, height=0.5, fill_color=BAR2, fill_opacity=1, stroke_color=KRAFT_DEEP, stroke_width=4).move_to([(x0 + x1) / 2, y, 0])
    dash = DashedLine([x0 + 0.15, y, 0], [x1 - 0.15, y, 0], color=GHOST, stroke_width=5, dash_length=0.3)
    g = VGroup(band, dash)
    g.band, g.dash = band, dash
    return g


def pD_cable(a, b, w=6):
    return Line(a, b, color=KRAFT_DEEP, stroke_width=w)


class B53_UnsupportedRoute(Scene):
    """A road drawn from Claude to a local model carries a sign 'unsupported route'; web search and prompt caching get crossed."""
    def construct(self):
        claude = logo_chip("claude", -4.6, 2.05, h=1.55)
        mod = pD_box(4.6, 1.9, s=1.0)
        mlab = T("local model", 40).move_to([5.0, 0.35, 0])
        caps = [("edit files", 0.5), ("run tools", -0.5), ("web search", -1.5), ("prompt caching", -2.5)]
        chips = [chip(s, -3.9, y, w=4.2, size=40) for s, y in caps]
        ticks = [check(-1.4, y, s=0.26, w=10) for y in (0.5, -0.5)]
        crosses = [x_mark(-1.3, y, r=0.3, w=9) for y in (-1.5, -2.5)]
        road = pD_road(-3.2, 3.2, 2.05)
        # the sign hangs below the road on a deep-kraft pole
        board = RoundedRectangle(corner_radius=0.3, width=4.0, height=1.45, fill_color="#FFFFFF", fill_opacity=1, stroke_width=0).move_to([1.15, 0.5, 0])
        shadow = RoundedRectangle(corner_radius=0.3, width=4.0, height=1.45, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([1.23, 0.42, 0])
        pole = pD_cable([1.15, 1.22, 0], [1.15, 1.8, 0], w=8)
        sl1 = T("documented settings", 34).move_to([1.15, 0.84, 0])
        sl2 = T("unsupported route", 34).move_to([1.15, 0.18, 0])
        # web search runs on Anthropic's backend: the label carries the Anthropic logo
        t1 = T("runs on", 36).move_to([-0.1, -1.5, 0])
        alogo = logo_chip("anthropic", 1.35, -1.5, h=0.95)
        t2 = T("backend", 36).move_to([3.0, -1.5, 0])
        tag = Group(t1, alogo, t2)

        self.play(FadeIn(claude), FadeIn(mod), FadeIn(mlab), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.2), run_time=0.9)
        # "pointing Claude Code at non-Claude models": the road is drawn from Claude to the local model
        hear(self, "pointing", lead=0.15)
        self.play(GrowFromEdge(road.band, LEFT), Create(road.dash), run_time=1.4, rate_func=smooth)
        # "this works": edit files and run tools tick
        hear(self, "this works", lead=0.1)
        self.play(*[Create(t) for t in ticks], run_time=0.4)
        # "documented settings": the sign goes up; "unsupported route": its second line lands
        hear(self, "documented settings", lead=0.2)
        self.play(FadeIn(shadow), FadeIn(board), Create(pole), FadeIn(sl1), run_time=0.5)
        hear(self, "unsupported route", lead=0.1)
        self.play(FadeIn(sl2), run_time=0.4)
        # after the midpoint: "web search runs on Anthropic's own backend"
        hear(self, "web search", lead=0.3)
        self.play(FadeIn(tag), run_time=0.5)
        hear(self, "not fully support", lead=0.2)
        self.play(Create(crosses[0]), run_time=0.35)
        hear(self, "is not supported", lead=0.1)
        self.play(Create(crosses[1]), run_time=0.4)
        done(self)


class B54_ContextGrowsThenExit(Scene):
    """Blocks stack into the context bar as the stopwatch slows; one tool server is crossed and the bar drops; then two exits leave and the rack dims."""
    def construct(self):
        claude = logo_chip("claude", -4.9, 0.2, h=1.5)
        watch = pD_stopwatch(-4.9, 2.15, r=0.75)
        tank = Rectangle(width=1.3, height=5.0, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-2.4, -0.25, 0])
        ctx = T("context", 40).move_to([-2.4, 2.65, 0])
        blocks = [Rectangle(width=1.06, height=0.52, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3)
                  .move_to([-2.4, -2.35 + 0.64 * i, 0]) for i in range(7)]
        tdef = T("tool definition", 36).move_to([0.0, -1.7, 0])
        cache = chip("cache", 1.4, 2.5, w=2.4, size=38)
        cache_x = x_mark(3.05, 2.5, r=0.3, w=9)
        srv = [chip("tool server", 1.5, 1.0, w=3.6, size=38), chip("tool server", 1.5, -0.2, w=3.6, size=38)]
        srv_x = x_mark(3.95, -0.2, r=0.3, w=9)
        ring = pD_ring(-2.4, -0.25, 1.7, 5.4)
        # the exit chain: Claude chip -> exit -> the job -> exit -> GPU node
        jobbox = pD_job(0.0, 0.4, s=1.1)
        jlab = T("the job", 40).move_to([0.0, -1.15, 0])
        st, lt = pD_rack(5.0, 0.4, s=1.0)
        rack = VGroup(st, lt)
        rlab = T("GPU node", 40).move_to([5.0, -1.2, 0])
        a1 = Arrow([-3.65, 0.2, 0], [-1.35, 0.2, 0], color=INK, stroke_width=9, buff=0, max_tip_length_to_length_ratio=0.25)
        e1 = M("exit", 38).move_to([-2.5, 0.85, 0])
        a2 = Arrow([1.25, 0.4, 0], [3.5, 0.4, 0], color=INK, stroke_width=9, buff=0, max_tip_length_to_length_ratio=0.28)
        e2 = M("exit", 38).move_to([2.4, 1.05, 0])
        ring1 = pD_ring(-4.9, 0.2, 2.5, 1.9)
        ring2 = pD_ring(0.0, 0.1, 2.3, 2.5)

        self.play(FadeIn(claude), FadeIn(watch), FadeIn(tank), FadeIn(ctx), run_time=0.4)
        # turn 1 ("long sessions"): two blocks stack, the stopwatch is quick
        hear(self, "long sessions", lead=0.15)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.4) for b in blocks[:2]], lag_ratio=0.4),
                  Rotate(watch.hand, angle=-2 * PI, about_point=[watch.cx, watch.cy, 0], rate_func=linear), run_time=0.7)
        # turn 2 ("as the context grows"): more blocks, the stopwatch slows
        hear(self, "as the context grows", lead=0.2)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.4) for b in blocks[2:4]], lag_ratio=0.4),
                  Rotate(watch.hand, angle=-PI, about_point=[watch.cx, watch.cy, 0], rate_func=linear), run_time=1.0)
        # turn 3 ("because nothing is cached"): more again, slower still; the cache is crossed
        hear(self, "because nothing", lead=0.1)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.4) for b in blocks[4:6]], lag_ratio=0.4),
                  Rotate(watch.hand, angle=-PI / 2, about_point=[watch.cx, watch.cy, 0], rate_func=linear), run_time=1.0)
        self.play(FadeIn(cache), Create(cache_x), run_time=0.45)
        # "Keep tool servers few": two tool servers; one is crossed and its blocks leave the bar
        hear(self, "Keep tool servers", lead=0.1)
        self.play(*[FadeIn(c) for c in srv], run_time=0.5)
        hear(self, "few", lead=0.2)
        self.play(Create(srv_x), *[FadeOut(b, shift=UP * 0.3) for b in blocks[3:6]], run_time=0.5)
        # "every definition uses context"
        hear(self, "every definition", lead=0.25)
        self.play(FadeIn(tdef), run_time=0.4)
        at(self, 6.75)
        self.add(ring)
        self.play(ring.animate.scale(1.1).set_opacity(0), run_time=0.55)
        # "And when you finish": the bar and servers go; the job and the GPU node arrive
        hear(self, "And when you finish", lead=0.4)
        gone = [watch, tank, ctx, tdef, cache, cache_x, srv[0], srv[1], srv_x, blocks[0], blocks[1], blocks[2], blocks[6]]
        self.play(*[FadeOut(m) for m in gone], run_time=0.35)
        self.play(FadeIn(jobbox), FadeIn(jlab), FadeIn(rack), FadeIn(rlab), run_time=0.45)
        # "exit twice": two exit arrows, in order
        hear(self, "exit twice", lead=0.1)
        self.play(Create(a1), FadeIn(e1), run_time=0.4)
        hear(self, "twice", lead=0.1)
        self.play(Create(a2), FadeIn(e2), run_time=0.4)
        # "Claude Code", then "the job"
        hear(self, "clod code", lead=0.0)
        self.add(ring1)
        self.play(ring1.animate.scale(1.18).set_opacity(0), run_time=0.6)
        hear(self, "then the job", lead=0.05)
        self.add(ring2)
        self.play(ring2.animate.scale(1.18).set_opacity(0), run_time=0.6)
        # "returns the GPU": the node dims and its lights go out
        hear(self, "returns the GPU", lead=0.2)
        self.play(rack.animate.set_opacity(0.3), run_time=0.8)
        done(self)


class B60_LockInFront(Scene):
    """The laptop reaches the node through the login node; Ollama stays on localhost; Caddy's locked gate rejects a packet with no token and opens for one with the key."""
    def construct(self):
        title = pD_act_title("VI · Pattern B, From Your Laptop")
        lane = -0.35
        gy = 0.2
        laptop = pD_laptop(-5.3, -0.1)
        llab = T("laptop", 34).move_to([-5.3, -1.6, 0])
        lst, llt = pD_rack(-2.95, -0.05, s=0.8)
        login = VGroup(lst, llt)
        nlab = T("login node", 34).move_to([-2.95, -1.6, 0])
        road1 = pD_road(-4.35, -3.8, lane)
        road2 = pD_road(-2.05, 2.05, lane)
        clab = T("cluster network", 34).move_to([0.1, -1.6, 0])
        gst, glt = pD_rack(5.2, -0.05, s=0.85)
        grack = VGroup(gst, glt)
        glab = T("GPU node", 38).move_to([4.1, -1.6, 0])
        olla = logo_chip("ollama", 2.9, -0.1, h=1.3)
        local = M("localhost", 34).move_to([2.9, 0.95, 0])
        gate = pD_gate(0.0, gy)
        lock = pD_gate_lock(0.0, gy)
        caddy = logo_chip("caddy", 0.0, 1.95, h=1.1)
        pkA = pD_packet(-4.55, lane - 0.05, token=True)
        pkB = pD_packet(-4.55, lane - 0.05, token=False)
        tag401 = chip("401", -2.0, 1.25, w=1.3, mono=True, size=36)

        self.play(FadeIn(title), run_time=0.4)
        # "needs a lock": the padlock appears
        hear(self, "needs a lock", lead=0.1)
        self.play(GrowFromCenter(lock), run_time=0.45)
        # "The laptop reaches the node through the login node"
        hear(self, "The laptop", lead=0.1)
        self.play(FadeIn(laptop), FadeIn(llab), run_time=0.4)
        hear(self, "through the login node", lead=0.3)
        self.play(FadeIn(login), FadeIn(nlab), Create(road1.dash), GrowFromEdge(road1.band, LEFT), run_time=0.5)
        # "so something has to listen on the node's cluster network"
        hear(self, "so something has to listen", lead=0.1)
        self.play(GrowFromEdge(road2.band, LEFT), Create(road2.dash), run_time=0.9, rate_func=smooth)
        hear(self, "the node's cluster", lead=0.15)
        self.play(FadeIn(grack), FadeIn(glab), FadeIn(clab), run_time=0.5)
        # "Ollama stays on localhost"
        hear(self, "stays on", lead=0.5)
        self.play(FadeIn(olla), run_time=0.4)
        at(self, 7.75)
        self.play(FadeIn(local), run_time=0.35)
        # "a small web server, Caddy, listens instead": the gate goes up in front of Ollama
        hear(self, "a small web server", lead=0.1)
        self.play(FadeIn(gate), run_time=0.5)
        hear(self, "caddy", lead=0.2)
        self.play(FadeIn(caddy), run_time=0.4)
        # "listens instead": the packet with the token comes up, the lock opens, the gate opens, the packet goes through
        hear(self, "listens instead", lead=0.0)
        self.play(FadeIn(pkA), run_time=0.15)
        self.play(pkA.animate.shift(RIGHT * 2.9), run_time=0.75, rate_func=linear)
        self.play(unlock_anim(lock, 0.35), run_time=0.35)
        self.play(gate.panel.animate.set_opacity(0.1), run_time=0.25)
        # "rejects every request": a second packet, no token, follows; the first goes through to Ollama
        self.add(pkB)
        self.play(pkA.animate.shift(RIGHT * 3.1), pkB.animate.shift(RIGHT * 2.9), run_time=0.8, rate_func=linear)
        # the gate closes again and the lock turns back
        self.play(gate.panel.animate.set_opacity(1.0), lock.shackle.animate.shift(DOWN * 0.3 * lock.s), lock.light.animate.set_color(GHOST), run_time=0.35)
        # "does not carry": the 401 tag lands and the packet is thrown out
        self.add(tag401)
        tag401.shift(UP * 0.6)
        self.play(tag401.animate.shift(DOWN * 0.6), FadeOut(pkB, shift=DOWN * 0.5), run_time=0.4, rate_func=smooth)
        # "your bearer token": a ring pulses round the packet that carried it
        hear(self, "your bearer token", lead=0.2)
        ring = pD_ring(1.45, lane + 0.2, 1.6, 1.6)
        self.add(ring)
        self.play(ring.animate.scale(1.2).set_opacity(0), run_time=0.6)
        done(self)


class B64_TwoRisks(Scene):
    """Other users on the node reach the random port beside the gate; your token sits in plain text on the laptop; scancel stamps and the node dims."""
    def construct(self):
        gy = 0.2
        gate = pD_gate(0.0, gy)
        lock = pD_gate_lock(0.0, gy)
        caddy = logo_chip("caddy", 0.0, 1.95, h=1.1)
        olla = logo_chip("ollama", 2.9, -0.1, h=1.3)
        gst, glt = pD_rack(5.2, -0.05, s=0.85)
        grack = VGroup(gst, glt)
        glab = T("GPU node", 38).move_to([4.1, -1.6, 0])
        node = Group(gate, lock, caddy, olla, grack)
        # the rest of the cluster: grey dots stopped by the gate
        rest = VGroup(*[Dot([x, y, 0], radius=0.16, color=BAR1) for x, y in ((-3.9, 1.1), (-3.5, 0.55), (-3.9, 0.0))])
        rlab = T("rest of cluster", 34).move_to([-3.5, 1.95, 0])
        # the random port: a small socket on the Ollama block
        port = Rectangle(width=0.4, height=0.4, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([2.4, 0.78, 0])
        plab = T("random port", 34).move_to([2.7, 1.7, 0])
        # other users: terracotta dots sitting on the rack's top face, then reaching the port
        users = VGroup(*[Dot([5.2 + dx, 0.38 + dy, 0], radius=0.14, color=TERRA) for dx, dy in ((-0.4, 0.0), (0.0, 0.12), (0.4, 0.0))])
        ulab = T("other users", 34).move_to([5.25, 1.35, 0])
        caut = pD_caution(1.35, 2.75)
        clab = T("obscurity, not security", 34).move_to([4.15, 2.75, 0])
        # the token on your laptop
        laptop = pD_laptop(-5.2, -1.0)
        llab = T("laptop", 34).move_to([-5.2, -2.0, 0])
        page = paper(-3.5, -0.95, w=1.0, h=1.3)
        pl = scribbles_on(page, n=3, inset=0.2, gap=0.32)
        tlab = M("token", 34).move_to([-3.5, 0.05, 0])
        open_lock = padlock(-2.05, -0.95, s=0.7)
        open_lock.shackle.shift(UP * 0.3 * open_lock.s)
        open_lock.light.set_color(TERRA)
        plain = T("plain text", 34).move_to([-2.8, -2.0, 0])
        cmd = plaque("scancel --name=ollama-serve", 0.4, -2.8, w=9.8, h=0.9, size=32)

        self.play(FadeIn(node), FadeIn(glab), run_time=0.5)
        # "The proxy blocks the rest of the cluster": grey dots come up and the gate stops them
        hear(self, "proxy blocks", lead=0.2)
        self.play(FadeIn(rest), FadeIn(rlab), run_time=0.3)
        self.play(rest.animate.shift(RIGHT * 2.1), run_time=0.9, rate_func=smooth)
        # "Ollama's own random port": a socket beside the gate
        hear(self, "random port", lead=0.3)
        self.play(FadeIn(port), FadeIn(plab), run_time=0.4)
        # "other users on the same node": dots on the rack reach the port, past the gate
        hear(self, "other users", lead=0.3)
        self.play(FadeIn(users), FadeIn(ulab), run_time=0.3)
        self.play(users.animate.move_to([2.75, 1.0, 0]), run_time=1.2, rate_func=smooth)
        # after the midpoint: "A random port is obscurity, not security"
        at(self, 7.75)
        self.play(FadeIn(caut), FadeIn(clab), run_time=0.4)
        # "your token sits in plain text on your laptop"
        hear(self, "your token", lead=0.3)
        self.play(FadeIn(laptop), FadeIn(llab), FadeIn(page), FadeIn(pl), FadeIn(tlab), run_time=0.5)
        hear(self, "plain text", lead=0.15)
        self.play(FadeIn(open_lock), FadeIn(plain), run_time=0.4)
        # "cancel the job": the command stamps, the node dims
        hear(self, "cancel the job", lead=0.4)
        self.play(FadeIn(cmd, scale=1.25), run_time=0.35)
        self.play(node.animate.fade(0.7), run_time=0.8)
        done(self)


class B72_LaunchDefaults(Scene):
    """ollama launch wires the tools up at the default port; here the port is random and locked so it breaks; OpenAI-compatible routes take over."""
    def construct(self):
        ys = (1.7, 0.2, -1.3)
        tx = -2.2
        codex = logo_chip("codex", tx, ys[0], h=1.2)
        opencode = logo_chip("opencode", tx, ys[1], h=1.2)
        dshadow = pill(tx + 0.08, ys[2] - 0.08, 1.62, h=1.2, fill=BOX_L)
        dbody = pill(tx, ys[2], 1.62, h=1.2)
        dlab = M("droid", 34).move_to([tx, ys[2], 0])
        droid = VGroup(dshadow, dbody, dlab)
        # the ollama launch command box (two mono lines)
        lshadow = Rectangle(width=2.4, height=1.6, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([-4.9, 0.1, 0])
        lcard = Rectangle(width=2.4, height=1.6, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([-5.0, 0.2, 0])
        la = M("ollama", 34).move_to([-5.0, 0.55, 0])
        lb = M("launch", 34).move_to([-5.0, -0.15, 0])
        launch = VGroup(lshadow, lcard, la, lb)
        fan = VGroup(*[pD_cable([-3.8, 0.2, 0], [tx - 0.85, y, 0]) for y in ys])
        # the model block with its plain slot
        cx, cy, w, d, h, s = 3.0, 0.25, 1.5, 1.5, 1.5, 1.0
        ox = cx - (w - d) / 2 * C30 * s
        oy = cy - ((w + d) / 4 + h / 2) * s
        iso = Iso(ox, oy, s)
        mod = iso.box(0, 0, 0, w, d, h)
        slot1 = iso.quad([(0, 0.3, 0.95), (0, 1.2, 0.95), (0, 1.2, 1.3), (0, 0.3, 1.3)], GHOST, stroke=INK, sw=3)
        s1 = iso.p(0, 0.75, 1.12)
        mlab = T("model", 40).move_to([5.4, 0.25, 0])
        route1 = VGroup(*[pD_cable([tx + 0.85, y, 0], [s1[0] - 0.95, s1[1], 0]) for y in ys])
        loc = M("localhost:11434", 34).move_to([2.9, 2.5, 0])
        ok = check(0.15, 2.5, s=0.24, w=10)
        rnd = T("random port", 38).move_to([2.9, 2.5, 0])
        lock = padlock(s1[0] - 0.55, s1[1] + 0.1, s=0.6)
        lock.set_z_index(6)
        cross1 = x_mark(0.2, 0.55, r=0.4, w=10)
        # the second route: OpenAI-compatible socket, three keyed cables
        slot2 = iso.quad([(0, 0.3, 0.2), (0, 1.2, 0.2), (0, 1.2, 0.55), (0, 0.3, 0.55)], GHOST, stroke=INK, sw=3)
        s2 = iso.p(0, 0.75, 0.37)
        oai = logo_chip("openai", 2.0, -2.3, h=0.95)
        comp = T("compatible", 38).move_to([3.75, -2.3, 0])
        route2 = VGroup(*[pD_cable([tx + 0.85, y, 0], [s2[0] - 0.1, s2[1], 0], w=6) for y in ys])
        keys = []
        for y in ys:
            a = np.array([tx + 0.85, y, 0.0]); b = np.array([s2[0] - 0.1, s2[1], 0.0])
            m = a + (b - a) * 0.5
            keys.append(key_obj(m[0] - 0.85 * 0.36, m[1], s=0.36))
        # the tools' own instructions
        pages = [paper(-4.4, y, w=1.1, h=1.0) for y in ys]
        pls = [scribbles_on(p, n=2, inset=0.2, gap=0.3) for p in pages]

        # "Codex, OpenCode and Droid": the three tools arrive on their names
        self.play(FadeIn(codex), run_time=0.35)
        hear(self, "OpenCode", lead=0.05)
        self.play(FadeIn(opencode), run_time=0.35)
        hear(self, "Droid", lead=0.1)
        self.play(FadeIn(droid), run_time=0.3)
        # "the ollama launch command": the command box, then its lines to the three tools
        hear(self, "Olama launch", lead=0.15)
        self.play(FadeIn(launch), run_time=0.4)
        hear(self, "command", lead=0.1)
        self.play(*[Create(l) for l in fan], run_time=0.5)
        # "only when Ollama is on the same machine at its default port": the model block with the plain slot
        hear(self, "same machine", lead=0.2)
        self.play(FadeIn(mod), FadeIn(mlab), run_time=0.5)
        hear(self, "default port", lead=0.2)
        self.play(FadeIn(slot1), *[Create(l) for l in route1], run_time=0.5)
        self.play(FadeIn(loc), Create(ok), run_time=0.35)
        # "Here the port is random": the slot's address changes to a random port
        hear(self, "Here", lead=0.05)
        self.play(FadeOut(loc), FadeOut(ok), FadeIn(rnd), run_time=0.45)
        # after the midpoint: "behind a token": a padlock sits on the slot
        at(self, 8.56)
        self.play(GrowFromCenter(lock), run_time=0.4)
        # "in Pattern B": the cables to the slot break
        hear(self, "Pattern B", lead=0.1)
        self.play(Create(cross1), route1.animate.set_opacity(0.3), run_time=0.4)
        # "set them up as OpenAI-compatible providers": the broken cables go, a second socket, three keyed cables
        hear(self, "set them up", lead=0.0)
        self.play(FadeOut(cross1), FadeOut(route1), FadeIn(slot2), FadeIn(oai), FadeIn(comp), run_time=0.4)
        hear(self, "OpenAI", lead=0.1)
        self.play(LaggedStart(*[AnimationGroup(Create(r), FadeIn(k)) for r, k in zip(route2, keys)], lag_ratio=0.3), run_time=1.1)
        # "follow each tool's current instructions": each tool's own page
        hear(self, "follow each", lead=0.1)
        self.play(FadeOut(launch), FadeOut(fan), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(VGroup(p, l)) for p, l in zip(pages, pls)], lag_ratio=0.3), run_time=1.0)
        done(self)
