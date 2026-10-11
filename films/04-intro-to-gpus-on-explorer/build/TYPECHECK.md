# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-intro-to-gpus`  |  Checked: 2026-10-09T12:23  |  Overall: PASS  |  Beats checked: 26  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.82) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 62px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 59px >= floor 41px | PASS | — |
| B11 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B12 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B13 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B20 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B21 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B30 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B31 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B41 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B42 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B50 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B51 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B52 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B60 | manim | light | min-size §8.1: min text-run height 105px >= floor 41px | PASS | — |
| B70 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B71 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B72 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B73 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B80 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | light | min-size §8.1: min text-run height 44px >= floor 41px (individual-char fallback at 2×) | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 15 | 0 |
| min-size §8.1 | 26 | 0 |
| overflow §8.2 | 26 | 0 |
| contrast §8.3 | 26 | 0 |
| contrast-local §8.3b | 26 | 0 |
| bbox-overlap §8.6b | 26 | 0 |
| card-clip §8.13 | 26 | 0 |
| kerning §8.4 | 6 | 0 |
| redundancy §8.10 (advisory) | 8 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
