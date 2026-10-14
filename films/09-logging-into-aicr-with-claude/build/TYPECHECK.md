# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-logging-into-aicr-with-claude`  |  Checked: 2026-10-12T13:27  |  Overall: PASS  |  Beats checked: 44  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [B30] narration recites the card (0.92) — discuss it, don't read it
> - §8.10 [BVDT] narration recites the card (0.94) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 61px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 56px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 68px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B12 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 161px >= floor 41px | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B15 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B16 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B20 | manim | light | min-size §8.1: min text-run height 491px >= floor 41px | PASS | — |
| B21 | manim | light | min-size §8.1: min text-run height 125px >= floor 41px | PASS | — |
| B22 | manim | light | min-size §8.1: min text-run height 56px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B23 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B24 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B25 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B26 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B27 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B30 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B31 | manim | light | min-size §8.1: min text-run height 56px >= floor 41px | PASS | — |
| B32 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B33 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B34 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B35 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B36 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B37 | manim | light | min-size §8.1: min text-run height 843px >= floor 41px | PASS | — |
| B38 | manim | light | min-size §8.1: min text-run height 98px >= floor 41px | PASS | — |
| B39 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | manim | light | min-size §8.1: min text-run height 43px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B41 | manim | light | min-size §8.1: min text-run height 285px >= floor 41px | PASS | — |
| B42 | manim | light | min-size §8.1: min text-run height 269px >= floor 41px | PASS | — |
| B43 | manim | light | min-size §8.1: min text-run height 59px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B44 | manim | light | min-size §8.1: min text-run height 93px >= floor 41px | PASS | — |
| B45 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px | PASS | — |
| B46 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B47 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px | PASS | — |
| B50 | manim | light | min-size §8.1: min text-run height 62px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B51 | manim | light | min-size §8.1: min text-run height 685px >= floor 41px | PASS | — |
| B52 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B53 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B54 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | light | min-size §8.1: min text-run height 65px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 16 | 0 |
| min-size §8.1 | 44 | 0 |
| overflow §8.2 | 44 | 0 |
| contrast §8.3 | 44 | 0 |
| contrast-local §8.3b | 44 | 0 |
| bbox-overlap §8.6b | 44 | 0 |
| card-clip §8.13 | 44 | 0 |
| kerning §8.4 | 23 | 0 |
| redundancy §8.10 (advisory) | 15 | 2 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
