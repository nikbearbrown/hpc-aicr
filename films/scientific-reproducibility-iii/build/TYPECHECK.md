# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-scientific-reproducibility-iii-containers`  |  Checked: 2026-10-14T01:59  |  Overall: PASS  |  Beats checked: 44  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [B30] narration recites the card (0.83) — discuss it, don't read it
> - §8.10 [BVDT] narration recites the card (0.91) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B20 | manim | light | min-size §8.1: min text-run height 41px >= floor 41px | PASS | — |
| B21 | manim | light | min-size §8.1: min text-run height 66px >= floor 41px | PASS | — |
| B22 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B23 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B30 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B31 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B32 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B33 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B34 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B35 | manim | light | min-size §8.1: min text-run height 58px >= floor 41px | PASS | — |
| B36 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B37 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B38 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B39 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B41 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B42 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B50 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B51 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B52 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B53 | manim | light | min-size §8.1: min text-run height 41px >= floor 41px | PASS | — |
| B54 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B55 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B56 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B60 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B61 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B62 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B63 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B64 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B70 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B71 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B72 | manim | light | min-size §8.1: min text-run height 59px >= floor 41px | PASS | — |
| B73 | manim | light | min-size §8.1: min text-run height 105px >= floor 41px | PASS | — |
| B74 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B80 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px (individual-char fallback at 2×) | PASS | — |
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
| no-wordy-card §8.5 | 20 | 0 |
| min-size §8.1 | 44 | 0 |
| overflow §8.2 | 44 | 0 |
| contrast §8.3 | 44 | 0 |
| contrast-local §8.3b | 44 | 0 |
| bbox-overlap §8.6b | 44 | 0 |
| card-clip §8.13 | 44 | 0 |
| kerning §8.4 | 19 | 0 |
| redundancy §8.10 (advisory) | 20 | 2 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
