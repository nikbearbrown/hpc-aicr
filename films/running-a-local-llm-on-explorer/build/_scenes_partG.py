# ═════════════════════════════ PART G — B110 ═════════════════════════════
def pG_act_title(text):
    t = T(text, 40)
    return t.move_to([-6.1 + t.width / 2, 3.0, 0])


class B110_WhereToGetStarted(Scene):
    """The repository address lands, then skills/ and local-llm-on-explorer/ open one under the other, and the get-started page lands."""
    def construct(self):
        title = pG_act_title("XI · Get Started")
        url = M("github.com/nikbearbrown/hpc-aicr", 32).move_to([0, 1.8, 0])
        under = Line([url.get_left()[0], 1.35, 0], [url.get_right()[0], 1.35, 0], color=TERRA, stroke_width=6)
        sk = M("skills/", 36).move_to([0, 0.65, 0])
        lc = M("local-llm-on-explorer/", 34).move_to([0, -0.4, 0])
        c1 = Line([0, 1.15, 0], [0, 0.95, 0], color=INK, stroke_width=5)
        c2 = Line([0, 0.3, 0], [0, 0.05, 0], color=INK, stroke_width=5)
        pg = paper(0, -1.9, w=1.3, h=1.55)
        _w = 1.3 - 2 * 0.22
        ln = VGroup(*[scribble(-_w / 2, -1.9 + 1.55 / 2 - 0.22 - 0.1 - i * 0.3, _w, amp=0.09) for i in range(2)])
        c3 = Line([0, -0.75, 0], [0, -1.1, 0], color=INK, stroke_width=5)
        name = M("GET-STARTED.md", 32).move_to([0, -3.0, 0])
        # faint dashed slots show the whole chain from the start; each real item replaces its slot
        def slot(w, h, y):
            return DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=min(0.3, h / 2), stroke_color=BAR2, stroke_width=4),
                                  num_dashes=36).move_to([0, y, 0])
        g_sk, g_lc, g_pg, g_nm = slot(2.4, 0.75, 0.65), slot(6.2, 0.75, -0.4), slot(1.3, 1.55, -1.9), slot(3.8, 0.7, -3.0)

        self.play(FadeIn(title), run_time=0.4)
        hear(self, "go to the", lead=0.2)
        self.play(FadeIn(url), Create(under), *[FadeIn(g) for g in (g_sk, g_lc, g_pg, g_nm)], run_time=0.6)
        hear(self, "Skills folder", lead=0.3)
        self.play(Create(c1), FadeIn(sk), FadeOut(g_sk), run_time=0.4)
        hear(self, "Local LLM", lead=0.3)
        self.play(Create(c2), FadeIn(lc), FadeOut(g_lc), run_time=0.4)
        hear(self, "Get Started", lead=0.25)
        self.play(Create(c3), FadeIn(pg), FadeIn(ln), FadeIn(name), FadeOut(g_pg), FadeOut(g_nm), run_time=0.5)
        done(self)
