# ═════════════════════════════ the film's cast (shared by every act) ═════════════════════════════
# One cast, whole film. The same object is the same picture in every beat. (ACTS.md lists it per act.)
#   KEY        key_obj()        a flat kraft key, ink outline, large (the private key)
#   LOCK       padlock()        dark body, ink shackle, ghost keyhole/light (turns terracotta when unlocked); unlock(lock)
#   CERT       cert_page()      a white certificate page: ghost lines, a kraft seal with one terracotta dot
#   AGENT      agent_slab(iso)  one dark slab with a light (the ssh-agent); returns (stack, lights)
#   COMMAND    job_box(iso)     a small kraft box with one terracotta tape (an `ssh` command); label it M("ssh")
#   AICR       aicr_rack(iso)   the large dark rack, 4 slabs (the cluster); returns (stack, lights)
#   LOGIN NODE explorer_rack()  the small dark rack, 2 slabs
#   VAULT      vault(iso)       a dark block with a pale square door (the macOS Keychain)
#   YOU        professor_bear("2x3" | "1x1", ...)  a portrait, never a person icon
#   chip(), plaque()            white pills / cards that carry short labels or real mono text
def key_obj(x=0.0, y=0.0, s=1.0):
    """A flat kraft key lying along +x with its bow centred on (x, y). `.bow`, `.width` (approx)."""
    bow = Circle(radius=0.55 * s, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
    hole = Circle(radius=0.2 * s, fill_color=STAGE, fill_opacity=1, stroke_color=INK, stroke_width=4)
    shaft = Rectangle(width=1.9 * s, height=0.26 * s, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5)
    shaft.move_to([0.5 * s + 0.95 * s, 0, 0])
    teeth = VGroup(*[Rectangle(width=0.22 * s, height=0.4 * s, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5)
                     .move_to([(1.85 + 0.3 * i) * s, -0.3 * s, 0]) for i in range(2)])
    g = VGroup(shaft, teeth, bow, hole)
    g.bow, g.width_units = bow, 2.95 * s
    return g.shift([x, y, 0])


def padlock(x=0.0, y=0.0, s=1.0):
    """A padlock centred on (x, y). `.shackle` rises when unlocked, `.light` turns terracotta."""
    shackle = Arc(radius=0.34 * s, start_angle=0, angle=PI, color=INK, stroke_width=12).move_to([0, 0.45 * s + 0.17 * s, 0])
    body = RoundedRectangle(corner_radius=0.08 * s, width=1.1 * s, height=0.9 * s, fill_color=DARK_TOP, fill_opacity=1,
                            stroke_color=INK, stroke_width=5).move_to([0, 0, 0])
    light = Dot([0, 0.02 * s, 0], radius=0.13 * s, color=GHOST)
    g = VGroup(shackle, body, light)
    g.shackle, g.body, g.light, g.s = shackle, body, light, s
    return g.shift([x, y, 0])


def unlock_anim(lock, rt=0.5):
    """Raise the shackle and turn the light terracotta (an AnimationGroup; play it in one self.play)."""
    return AnimationGroup(lock.shackle.animate.shift(UP * 0.3 * lock.s), lock.light.animate.set_color(TERRA), run_time=rt)


def cert_page(x=0.0, y=0.0, w=1.9, h=2.4):
    """The certificate: white page, three ghost lines, a kraft seal with one terracotta dot. `.card`, `.seal`."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([0.1, -0.1, 0])
    card = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
    lines = VGroup(*[Line([-w / 2 + 0.28, h / 2 - 0.5 - 0.38 * i, 0], [w / 2 - 0.28 - (0.5 if i == 2 else 0), h / 2 - 0.5 - 0.38 * i, 0],
                          color=BAR2, stroke_width=7) for i in range(3)])
    seal = Circle(radius=0.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([w / 2 - 0.55, -h / 2 + 0.55, 0])
    dot = Dot(seal.get_center(), radius=0.09, color=TERRA)
    g = VGroup(shadow, card, lines, seal, dot)
    g.card, g.seal, g.w, g.h = card, seal, w, h
    return g.shift([x, y, 0])


def explorer_rack(iso, x0=0.0, y0=0.0, z0=0.0):
    return iso.server(x0, y0, z0, w=1.3, d=1.3, slab=0.42, n=2)


def aicr_rack(iso, x0=0.0, y0=0.0, z0=0.0):
    return iso.server(x0, y0, z0, w=2.4, d=1.6, slab=0.46, n=4)


def job_box(iso, x0=0.0, y0=0.0, z0=0.0, s=0.7):
    return VGroup(iso.box(x0, y0, z0, s, s, s * 0.8), iso.tape(x0, y0, z0 + s * 0.8, s, s, drop=0.18, t=0.08))


def home_box(iso, x0=0.0, y0=0.0, z0=0.0):
    return iso.box(x0, y0, z0, 1.2, 1.2, 0.9)


def scratch_bin(iso, x0=0.0, y0=0.0, z0=0.0):
    return iso.open_box(x0, y0, z0, 2.8, 1.8, 0.8)


def agent_slab(iso, x0=0.0, y0=0.0, z0=0.0):
    """The ssh-agent: one dark slab with a light (starts ghost; turn it terracotta when the agent holds the key)."""
    return iso.server(x0, y0, z0, w=1.5, d=1.5, slab=0.6, n=1)


def vault(iso, x0=0.0, y0=0.0, z0=0.0):
    """The macOS Keychain: a dark block with a pale square door and a dark handle on its right face."""
    body = iso.box(x0, y0, z0, 1.5, 1.5, 1.2, DARK_TOP, DARK_L, DARK_R)
    door = iso.quad([(x0 + 0.25, y0 - 0.02, z0 + 0.2), (x0 + 1.25, y0 - 0.02, z0 + 0.2),
                     (x0 + 1.25, y0 - 0.02, z0 + 1.0), (x0 + 0.25, y0 - 0.02, z0 + 1.0)], GHOST, stroke=INK, sw=4)
    handle = Dot(iso.p(x0 + 1.0, y0 - 0.03, z0 + 0.6), radius=0.09, color=DARK_L)
    return VGroup(body, door, handle)


def chip(text, x, y, w=None, mono=False, size=34):
    """A white pill with a short label (no outline, so text and outline never fuse)."""
    lab = M(text, size - 2) if mono else T(text, size)
    w = w or (lab.width + 0.8)
    shadow = pill(x + 0.08, y - 0.08, w, h=0.8, fill=BOX_L)
    p = pill(x, y, w, h=0.8)
    lab.move_to([x, y, 0])
    g = VGroup(shadow, p, lab)
    g.pill, g.label = p, lab
    return g

def _logo_path(company, n=1):
    """brutalist.art/icons/logos/<company>/<company>-NN.png (LOGO LAW, Bear 2026-10-12: a company is shown by its logo)."""
    cands = [_os.environ.get("ART_HOME") and _os.path.join(_os.environ["ART_HOME"], "icons", "logos")]
    here = _os.path.dirname(_os.path.abspath(__file__))
    for _ in range(8):
        cands.append(_os.path.join(here, "brutalist.art", "icons", "logos")); here = _os.path.dirname(here)
    cands.append("<books>/brutalist.art/icons/logos")
    for c in cands:
        p = c and _os.path.join(c, company, f"{company}-{n:02d}.png")
        if p and _os.path.exists(p):
            return p
    return None


def logo_chip(company, x, y, h=1.35, n=1):
    """A white pill carrying the company's LOGO (no word). Falls back to a text chip if the logo file is missing.
    Returns a Group (it holds an image): use FadeIn/FadeOut/self.add on it."""
    p = _logo_path(company, n)
    if p is None:
        return chip(company.title(), x, y)
    w = h * 1.35
    shadow = pill(x + 0.08, y - 0.08, w, h=h, fill=BOX_L)
    body = pill(x, y, w, h=h)
    img = ImageMobject(p)
    img.scale_to_fit_height(h * 0.78)
    img.move_to([x, y, 0])
    g = Group(shadow, body, img)
    g.pill = body
    return g


def plaque(text, x, y, w=6.2, h=1.0, size=34):
    """A white card carrying REAL error or command text in mono (no outline)."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
    card = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    lab = M(text, size).move_to([x, y, 0])
    g = VGroup(shadow, card, lab)
    g.card, g.label = card, lab
    return g


# ═════════════════════════════ this film's cast (GPU performance) ═════════════════════════════
# GPU        gpu_card(x, y)        a dark card, ghost light (`lit=True` or `.light.set_color(TERRA)` when busy)
# CPU        cpu_chip(x, y)        a dark chip with kraft pins
# JOB        job2(x, y)            a small kraft box with one terracotta tape
# TANK       tank(cx, yb, yt, w)   the VRAM tank (white fill, open-topped ink U)
# GAUGE      gauge(cx, cy, r, v)   a half-dial with a needle (v in 0..1); terracotta only at a mark you add
# STAMP      stamp(text, x, y)     a kraft pill with a short word
def act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


def gpu_card(x, y, w=1.7, h=1.0, lit=False):
    """A GPU: dark card, two pale pin lines on the left, a light on the right (ghost, or terracotta when `lit`)."""
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    pins = VGroup(*[Line([x - w / 2 + 0.28, y + dy, 0], [x + w * 0.1, y + dy, 0], color=BAR1, stroke_width=6) for dy in (0.14, -0.14)])
    light = Dot([x + w / 2 - 0.3, y, 0], radius=0.11, color=TERRA if lit else GHOST)
    g = VGroup(body, pins, light)
    g.body, g.light, g.w, g.h = body, light, w, h
    return g


def cpu_chip(x, y, w=1.5, h=0.9):
    """The processor: a dark chip body with kraft pins on both sides, a light on top-right."""
    body = Rectangle(width=w, height=h, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    pins = VGroup(*[Line([x + s * w / 2, y + dy, 0], [x + s * (w / 2 + 0.26), y + dy, 0], color=KRAFT_DEEP, stroke_width=7)
                    for s in (-1, 1) for dy in (-0.25, 0.0, 0.25)])
    light = Dot([x + w / 2 - 0.25, y + h / 2 - 0.24, 0], radius=0.1, color=GHOST)
    g = VGroup(pins, body, light)
    g.body, g.light = body, light
    return g


def job2(x, y, s=0.8):
    """A small kraft box with one terracotta tape stripe (a job)."""
    box = Rectangle(width=s, height=s * 0.75, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    tape = Rectangle(width=s * 0.2, height=s * 0.75, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    g = VGroup(box, tape)
    g.box = box
    return g


def tank(cx, yb, yt, w):
    """The VRAM tank: a white fill and an open-topped U wall in ink."""
    fill = Rectangle(width=w, height=yt - yb, fill_color=PAGE_TOP, fill_opacity=1, stroke_width=0).move_to([cx, (yt + yb) / 2, 0])
    wall = VMobject(stroke_color=INK, stroke_width=9, fill_opacity=0)
    wall.set_points_as_corners([[cx - w / 2, yt, 0], [cx - w / 2, yb, 0], [cx + w / 2, yb, 0], [cx + w / 2, yt, 0]])
    return VGroup(fill, wall)


def blk(cx, y0, w, h, fill=BAR1, sw=4):
    """A block standing on y0 (its bottom edge), centred on cx; grey fill, ink outline."""
    return Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=sw).move_to([cx, y0 + h / 2, 0])


def gauge(cx, cy, r=1.7, v=0.5, sw=9):
    """A half dial (left = 0, right = 1) with a needle at `v`. `.needle`, `.arc`, `.cx`, `.cy`, `.r`, `.at(v)` gives the arc point."""
    arc = Arc(radius=r, start_angle=0, angle=PI, stroke_color=BAR1, stroke_width=sw).move_arc_center_to([cx, cy, 0])
    ticks = VGroup(*[Line([cx + (r - 0.05) * np.cos(PI - f * PI), cy + (r - 0.05) * np.sin(PI - f * PI), 0],
                          [cx + (r + 0.2) * np.cos(PI - f * PI), cy + (r + 0.2) * np.sin(PI - f * PI), 0], color=INK, stroke_width=6)
                     for f in (0.0, 0.5, 1.0)])
    def pt(f, rr):
        return [cx + rr * np.cos(PI - f * PI), cy + rr * np.sin(PI - f * PI), 0]
    needle = Line([cx, cy, 0], pt(v, r - 0.15), color=INK, stroke_width=8)
    hub = Dot([cx, cy, 0], radius=0.14, color=INK)
    g = VGroup(arc, ticks, needle, hub)
    g.arc, g.needle, g.cx, g.cy, g.r, g.pt = arc, needle, cx, cy, r, pt
    return g


def stamp(text, x, y, w=None, size=32):
    """A kraft pill with a short word, a terracotta dot, ink outline."""
    lab = T(text, size)
    w = w or (lab.width + 0.9)
    sh = pill(x + 0.07, y - 0.07, w, h=0.7, fill=BOX_L)
    body = RoundedRectangle(width=w, height=0.7, corner_radius=0.35, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    dot = Dot([x - w / 2 + 0.3, y, 0], radius=0.08, color=TERRA)
    lab.move_to([x + 0.18, y, 0])
    return VGroup(sh, body, dot, lab)


def ring_around(g, pad=0.14, color=TERRA, sw=6):
    return SurroundingRectangle(g, color=color, buff=pad, stroke_width=sw, corner_radius=0.12)


def dashed_slot(x, y, w, h):
    """A faint dashed outline showing where something will land (keeps the layout visible early)."""
    return DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=min(0.25, h / 2), stroke_color=BAR2, stroke_width=4),
                          num_dashes=36).move_to([x, y, 0])


def lab_l(text, x_left, y, size=34, mono=False):
    """A label whose LEFT edge sits at x_left."""
    t = M(text, size) if mono else T(text, size)
    return t.move_to([x_left + t.width / 2, y, 0])


def lab_c(text, x, y, size=34, mono=False):
    t = M(text, size) if mono else T(text, size)
    return t.move_to([x, y, 0])
