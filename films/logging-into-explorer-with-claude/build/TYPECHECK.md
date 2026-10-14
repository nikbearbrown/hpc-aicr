# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-logging-into-explorer-with-claude`  |  Checked: 2026-10-13T14:13  |  Overall: PASS  |  Beats checked: 23  |  FAILs: 0

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
| B10 | manim | light | min-size §8.1: min text-run height 96px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B20 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B21 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B22 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B30 | manim | light | min-size §8.1: min text-run height 190px >= floor 41px | PASS | — |
| B31 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B32 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B33 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B41 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B42 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B43 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B50 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B51 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B52 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
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
| no-wordy-card §8.5 | 9 | 0 |
| min-size §8.1 | 23 | 0 |
| overflow §8.2 | 23 | 0 |
| contrast §8.3 | 23 | 0 |
| contrast-local §8.3b | 23 | 0 |
| bbox-overlap §8.6b | 23 | 0 |
| card-clip §8.13 | 23 | 0 |
| kerning §8.4 | 9 | 0 |
| redundancy §8.10 (advisory) | 9 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
