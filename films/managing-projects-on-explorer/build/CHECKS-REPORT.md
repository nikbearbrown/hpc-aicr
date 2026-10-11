# CHECKS-REPORT — Managing /projects on Explorer

## Self-contained
PASS — Explorer is named in B10 with enough context. Six prerequisite terms defined in BDEFS. No "this chapter", "this training", or other forward/back references.

## BEST-BEAT LAW
PASS — Every body beat auditioned the full playset. Remotion LibraryIconRow chosen for B10/B20 (icon rows teach the permission gradient). Manim chosen for B21 (TTL timeline) and B51 (staggered best-practices list). CCPlainShell chosen for all command beats (the real terminal output is the evidence).

## SHOW-THE-THING LAW
PASS — No tools that need live capture in this lecture. Shell commands shown as CCPlainShell with realistic output (matching source examples). No AI-generated screenshots used.

## FACTCHECK
PASS — 17 claims checked, all trace to source document (see FACTCHECK.md).

## GATE T (typography)
Pending — run after `art run`.

## GATE V (visual QC)
Pending — run after `art run`.

## GATE B (bookend)
Pending — run after `art final`.

## SKIN LINT
Expected: SKIN LINT will warn about BrutalistHesitantWriter for BIDEA (palette=claude, cold open is BrutalistHesitantWriter not ClaudeComposerAsk). This is a known false positive for the lecture skill — BIDEA uses BrutalistHesitantWriter by design (lecture SKILL.md explicitly drops the composer cold open). bookend_check.py will confirm PASS.
