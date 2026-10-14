# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-running-a-local-llm-on-explorer`  |  Checked: 2026-10-13T20:13  |  Overall: PASS  |  Beats checked: 57  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.94) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 58px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 61px >= floor 41px | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 279px >= floor 41px | PASS | — |
| B20 | manim | light | min-size §8.1: min text-run height 56px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B21 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B22 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B23 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B24 | manim | light | min-size §8.1: min text-run height 929px >= floor 41px | PASS | — |
| B25 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B26 | manim | light | min-size §8.1: min text-run height 252px >= floor 41px | PASS | — |
| B27 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B30 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B31 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B32 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B33 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B34 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B35 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B41 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B42 | manim | light | min-size §8.1: min text-run height 198px >= floor 41px | PASS | — |
| B43 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B44 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B50 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B51 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B52 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B53 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B54 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B55 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B60 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B61 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B62 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B63 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B64 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B70 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B71 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B72 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px | PASS | — |
| B80 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B81 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B82 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B90 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B91 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B92 | manim | light | min-size §8.1: min text-run height 47px >= floor 41px | PASS | — |
| B93 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B94 | manim | light | min-size §8.1: min text-run height 88px >= floor 41px | PASS | — |
| B95 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B100 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B101 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B102 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B110 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B111 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | dark | min-size §8.1: min text-run height 239px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 19 | 0 |
| min-size §8.1 | 57 | 0 |
| overflow §8.2 | 57 | 0 |
| contrast §8.3 | 57 | 0 |
| contrast-local §8.3b | 57 | 0 |
| bbox-overlap §8.6b | 57 | 0 |
| card-clip §8.13 | 57 | 0 |
| kerning §8.4 | 33 | 0 |
| redundancy §8.10 (advisory) | 19 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
