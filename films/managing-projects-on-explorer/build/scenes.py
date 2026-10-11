"""scenes.py — Manim scenes for claude-liam-lecture-managing-projects.

Beats:
  B21 - TTLTimeline: administrative TTL explained as a timeline
  B51 - BestPracticesList: four best practices appearing staggered
"""
from manim import *

# ── palette (Claude brand) ──────────────────────────────────────────
PAGE    = "#FAF9F7"
INK     = "#1A1A1A"
INK_MED = "#4A4A4A"
SPARK   = "#C96442"   # terracotta accent
CARD    = "#F0EDE8"
BORDER  = "#D4CFC9"
MONO    = "#2D2D2D"

config.background_color = PAGE
config.pixel_height = 2160
config.pixel_width  = 3840
config.frame_height = 8.0
config.frame_width  = 14.22


def ink_text(txt, size=0.55, weight=BOLD, color=INK, font="Georgia"):
    return Text(txt, font=font, font_size=size * 72, weight=weight, color=color)


def mono_text(txt, size=0.45, color=MONO):
    return Text(txt, font="Courier New", font_size=size * 72, color=color)


# ─────────────────────────────────────────────────────────────────────
# B21 — TTLTimeline
# ─────────────────────────────────────────────────────────────────────
class TTLTimeline(Scene):
    """Horizontal timeline: project created → TTL marker → RC emails PI.
    Annotation below: 'data untouched'.
    """

    def construct(self):
        # --- title ---
        title = ink_text("Time To Live (TTL)", size=0.88)
        title.move_to(UP * 3.2)
        underline = Line(
            title.get_left() + LEFT * 0.1,
            title.get_right() + RIGHT * 0.1,
            color=SPARK, stroke_width=7
        )
        underline.next_to(title, DOWN, buff=0.14)

        # --- timeline spine: stay safely within ±4.2 ---
        x_left  = LEFT  * 4.2
        x_right = RIGHT * 4.2

        spine = Line(x_left, x_right, color=INK, stroke_width=8)
        spine.move_to(UP * 0.6)

        # --- dots on the spine ---
        dot_created = Dot(spine.get_left(),   radius=0.22, color=SPARK)
        dot_ttl     = Dot(spine.get_center(), radius=0.22, color=SPARK)
        dot_rc      = Dot(spine.get_right(),  radius=0.22, color=SPARK)

        # --- labels above dots ---
        lbl_created = ink_text("Project\ncreated", size=0.64, weight=NORMAL)
        lbl_created.next_to(dot_created, UP, buff=0.44)

        lbl_ttl = ink_text("TTL\nexpires", size=0.64, weight=NORMAL)
        lbl_ttl.next_to(dot_ttl, UP, buff=0.44)

        lbl_rc = ink_text("RC emails\nthe PI", size=0.64, weight=NORMAL)
        lbl_rc.next_to(dot_rc, UP, buff=0.44)

        # --- annotation below TTL dot (no arrowhead — dashed line instead) ---
        lbl_data = ink_text("data untouched", size=0.75, color=SPARK, weight=BOLD)
        lbl_data.next_to(dot_ttl, DOWN, buff=1.2)

        connect_line = DashedLine(
            dot_ttl.get_center() + DOWN * 0.24,
            lbl_data.get_top() + UP * 0.08,
            color=INK_MED,
            stroke_width=4,
            dash_length=0.15,
        )

        lbl_admin = ink_text("administrative marker, not a countdown", size=0.58,
                             color=INK_MED, weight=NORMAL)
        lbl_admin.next_to(lbl_data, DOWN, buff=0.45)

        # ── animate ──
        self.play(
            FadeIn(title, shift=UP * 0.15),
            Create(underline),
            run_time=0.6
        )
        self.wait(0.2)
        self.play(Create(spine), run_time=0.7)
        self.play(
            FadeIn(dot_created, scale=0.5),
            FadeIn(lbl_created, shift=UP * 0.15),
            run_time=0.5
        )
        self.wait(0.3)
        self.play(
            FadeIn(dot_ttl, scale=0.5),
            FadeIn(lbl_ttl, shift=UP * 0.15),
            run_time=0.5
        )
        self.wait(0.3)
        self.play(
            FadeIn(dot_rc, scale=0.5),
            FadeIn(lbl_rc, shift=UP * 0.15),
            run_time=0.5
        )
        self.wait(0.4)
        self.play(
            Create(connect_line),
            FadeIn(lbl_data, shift=DOWN * 0.1),
            run_time=0.6
        )
        self.wait(0.3)
        self.play(FadeIn(lbl_admin), run_time=0.5)
        self.wait(3.0)


# ─────────────────────────────────────────────────────────────────────
# B51 — BestPracticesList
# ─────────────────────────────────────────────────────────────────────
class BestPracticesList(Scene):
    """Four best practices appearing one by one, staggered with the voice."""

    ITEMS = [
        "Review membership after every graduation",
        "Use Guest for externals — read-only, least privilege",
        "Designate a Delegate — keep the PI out of the queue",
        "Keep the group email current for quota warnings",
    ]

    def construct(self):
        title = ink_text("Best Practices", size=0.80, color=INK)
        title.move_to(UP * 3.0)

        underline = Line(
            title.get_left() + LEFT * 0.1,
            title.get_right() + RIGHT * 0.1,
            color=SPARK, stroke_width=7
        )
        underline.next_to(title, DOWN, buff=0.14)

        rows = VGroup()
        for i, text in enumerate(self.ITEMS):
            # Use a filled circle bullet (no period — avoids thin-dot detection)
            bullet = Text("●", font="Georgia", font_size=0.55 * 72, color=SPARK)
            label  = ink_text(text, size=0.65, weight=NORMAL)
            row    = VGroup(bullet, label).arrange(RIGHT, buff=0.45, aligned_edge=UP)
            rows.add(row)

        rows.arrange(DOWN, buff=0.70)
        rows.move_to(DOWN * 0.15)

        # Constrain width to prevent edge-bleed (safe area ≈ ±5.5 units)
        if rows.width > 11.0:
            rows.scale(11.0 / rows.width)

        self.play(
            FadeIn(title, shift=UP * 0.15),
            Create(underline),
            run_time=0.7
        )
        self.wait(0.3)

        for i, row in enumerate(rows):
            self.play(FadeIn(row, shift=RIGHT * 0.18), run_time=0.55)
            self.wait(2.2 if i < len(rows) - 1 else 3.0)
