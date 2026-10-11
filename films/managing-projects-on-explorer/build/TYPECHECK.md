# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-managing-projects`  |  Checked: 2026-10-02T15:05  |  Overall: PASS  |  Beats checked: 16  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [B31] narration recites the card (1.00) — discuss it, don't read it
> - §8.10 [B42] narration recites the card (1.00) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BIDEA | bookend | light | min-size §8.1: min text-run height 61px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B20 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B21 | manim | light | min-size §8.1: hand-drawn pattern (TTLTimeline) — §8.1 hachure/crossbar fragments are fals… | PASS | — |
| B30 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B31 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B41 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B42 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B43 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B50 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B51 | manim | light | min-size §8.1: hand-drawn pattern (BestPracticesList) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | dark | min-size §8.1: min text-run height 106px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 10 | 0 |
| min-size §8.1 | 16 | 0 |
| overflow §8.2 | 16 | 0 |
| contrast §8.3 | 16 | 0 |
| contrast-local §8.3b | 16 | 0 |
| bbox-overlap §8.6b | 16 | 0 |
| card-clip §8.13 | 16 | 0 |
| kerning §8.4 | 2 | 0 |
| redundancy §8.10 (advisory) | 10 | 2 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
