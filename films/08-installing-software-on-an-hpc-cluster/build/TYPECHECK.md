# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-software-installation`  |  Checked: 2026-10-09T12:59  |  Overall: PASS  |  Beats checked: 29  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.80) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 62px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B20 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B21 | manim | light | min-size §8.1: min text-run height 45px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B30 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B31 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B32 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B33 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B41 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B50 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B51 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B52 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B60 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B61 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B62 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B63 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B70 | manim | light | min-size §8.1: min text-run height 119px >= floor 41px | PASS | — |
| B71 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B72 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B73 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B80 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B81 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | light | min-size §8.1: min text-run height 78px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 12 | 0 |
| min-size §8.1 | 29 | 0 |
| overflow §8.2 | 29 | 0 |
| contrast §8.3 | 29 | 0 |
| contrast-local §8.3b | 29 | 0 |
| bbox-overlap §8.6b | 29 | 0 |
| card-clip §8.13 | 29 | 0 |
| kerning §8.4 | 12 | 0 |
| redundancy §8.10 (advisory) | 12 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
