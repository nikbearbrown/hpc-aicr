# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-aicr-optimizing-gpu-usage`  |  Checked: 2026-10-09T12:07  |  Overall: PASS  |  Beats checked: 48  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.88) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 61px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 105px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px | PASS | — |
| B12 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B12B | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 47px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B15 | manim | light | min-size §8.1: min text-run height 42px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B16 | manim | light | min-size §8.1: min text-run height 607px >= floor 41px | PASS | — |
| B20 | manim | light | min-size §8.1: min text-run height 105px >= floor 41px | PASS | — |
| B21 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B22 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B23 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B30 | manim | light | min-size §8.1: min text-run height 62px >= floor 41px | PASS | — |
| B31 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B32 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B32B | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B33 | manim | light | min-size §8.1: min text-run height 59px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B34 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | manim | light | min-size §8.1: min text-run height 73px >= floor 41px | PASS | — |
| B41 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B41B | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B42 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px | PASS | — |
| B43 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B44 | manim | light | min-size §8.1: min text-run height 46px >= floor 41px | PASS | — |
| B50 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px | PASS | — |
| B51 | manim | light | min-size §8.1: min text-run height 41px >= floor 41px | PASS | — |
| B52 | manim | light | min-size §8.1: min text-run height 225px >= floor 41px | PASS | — |
| B53 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B54 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B55 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B56 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B60 | manim | light | min-size §8.1: min text-run height 105px >= floor 41px | PASS | — |
| B61 | manim | light | min-size §8.1: min text-run height 128px >= floor 41px | PASS | — |
| B62 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B62B | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B63 | manim | light | min-size §8.1: min text-run height 195px >= floor 41px | PASS | — |
| B70 | manim | light | min-size §8.1: min text-run height 105px >= floor 41px | PASS | — |
| B71 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B72 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B73 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B80 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B81 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | dark | min-size §8.1: min text-run height 65px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 16 | 0 |
| min-size §8.1 | 48 | 0 |
| overflow §8.2 | 48 | 0 |
| contrast §8.3 | 48 | 0 |
| contrast-local §8.3b | 48 | 0 |
| bbox-overlap §8.6b | 48 | 0 |
| card-clip §8.13 | 48 | 0 |
| kerning §8.4 | 27 | 0 |
| redundancy §8.10 (advisory) | 6 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
