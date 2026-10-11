# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-intro-to-parallel-computing`  |  Checked: 2026-10-09T12:31  |  Overall: PASS  |  Beats checked: 31  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.83) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 41px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B20 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B30 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px | PASS | — |
| B31 | manim | light | min-size §8.1: min text-run height 975px >= floor 41px | PASS | — |
| B40 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px | PASS | — |
| B41 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B50 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B51 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B52 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B53 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B54 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B55 | manim | light | min-size §8.1: min text-run height 45px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B60 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B61 | manim | light | min-size §8.1: min text-run height 56px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B62 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B70 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B71 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B72 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B73 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B80 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B81 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B82 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B83 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B90 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B91 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
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
| no-wordy-card §8.5 | 12 | 0 |
| min-size §8.1 | 31 | 0 |
| overflow §8.2 | 31 | 0 |
| contrast §8.3 | 31 | 0 |
| contrast-local §8.3b | 31 | 0 |
| bbox-overlap §8.6b | 31 | 0 |
| card-clip §8.13 | 31 | 0 |
| kerning §8.4 | 14 | 0 |
| redundancy §8.10 (advisory) | 4 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
