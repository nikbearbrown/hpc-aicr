# ACTS — Logging into AICR with Claude (lecture)

**What this is.** The coverage map for the lecture film of `hpc-aicr/Logging-into-AICR-with-Claude/README.md`, written before any beat.
**Why.** A lecture covers the WHOLE source: every section lands in an act or is listed under LEFT OUT with a reason.
**Found.** All ten sections (intro table, 0 to 8) are covered in five acts, 37 body beats. Nothing is left out. Two sections are told out of source order (logged under Order). Estimated runtime 9 to 11 minutes (an output, not a target).

Source: `<books>/hpc-aicr/Logging-into-AICR-with-Claude/README.md`
Evidence: `<books>/hpc-aicr/Logging-into-AICR-with-Claude/SESSION.md` (three real runs, 2026-10-11)

| Source section | Act | Beats |
|---|---|---|
| Header: what this is, why it works (no password, key + CA certificate, ssh-agent) | I · What AICR Checks | B10 (and BIDEA) |
| "What you do yourself, and what Claude does" table | I (B14 the human steps), IV (B40 approval) | B14 B40 |
| 0. Before you start (account, AICR user name, Claude Code, ssh on each OS) | I · What AICR Checks | B11 |
| 1. Get your key files (sign in at ood.aicr.ai, download aicr_keys, the four files, human-only) | I | B12 B13 B14 |
| 2. Install the files and set a passphrase (commands, Windows, WSL, `ssh-keygen -L`, Principals, Valid, renewal) | I | B15 B16 |
| 4. Unlock the key once: the problem (Claude has no keyboard) | II · Unlock Once | B20 |
| 4. Unlock the key once: the fix (ssh-agent) and why the secret never passes through Claude | II | B21 B22 |
| 3. Add AICR to your SSH config (block, IdentitiesOnly, ServerAliveInterval, AddKeysToAgent, UseKeychain/IgnoreUnknown) | II | B23 B24 |
| 4. macOS / Linux / Windows agent commands, `ssh-add -l` | II | B25 B26 B27 |
| 5. Test the way Claude will use it (`ssh aicr hostname`, host key prompt, BatchMode) | III · Do It For Real | B30 B31 |
| 5. The real run (SESSION Run 1) | III | B32 B33 |
| 5. Prove it survives an empty agent (SESSION Run 3), macOS Keychain, Linux/Windows caveat | III | B34 B35 B36 B37 B38 |
| How it authenticated (SESSION Run 2) | III | B39 |
| 6. Ask Claude to log in: the command Claude runs, approving it | IV · Rules For A Shared Cluster | B40 (the prompt itself is BHTF) |
| 7. Rules for Claude on a shared cluster, rules 1 to 7 | IV | B41 B42 B43 B44 B45 B46 B47 |
| 8. Troubleshooting: Permission denied (publickey) and the empty-agent trap | V · When It Fails | B50 B51 B52 |
| 8. Troubleshooting: the other seven rows | V | B53 B54 |
| 9. Where this comes from | not narrated | SOURCES.md, description draft "Sources" |
| 6. The pasteable prompt | Your Turn | BHTF |

## LEFT OUT

Nothing is dropped. Compressed, not dropped:
- The "short real example" partition table in README section 6 is the same data as SESSION Run 1, which B33 shows in full from the real run.
- README section 3's closing optional `alias aicr='ssh aicr'` is not spoken (a convenience, adds nothing to the idea). Listed here so it is a decision, not an omission.
- The `ssh -G aicr` filtered output and the certificate "Extensions" line in SESSION.md are not shown: the first only repeats the config block (B23, B24), the second is a 107-column line that cannot be shown verbatim at the type floor; B16 marks it as omitted with a comment line.
- README "Last checked" footer: a maintenance note, not teaching.

## Order

The source's order is kept except two moves, both because a prerequisite forces them:
1. **Section 4's problem (B20) and fix (B21, B22) come BEFORE section 3's config block (B23, B24).** The config block's `AddKeysToAgent` and `UseKeychain` lines only make sense once the viewer knows what an agent is. The block is shown with the reason already earned.
2. **Section 6 (the prompt) is held for the Your Turn beat**; the body keeps only the approval habit (B40). The viewer then reads the same prompt aloud in full where it belongs.

## BIDEA correction and BDEFS terms

- BIDEA: the newcomer's framing "To let Claude log in, I give it my password" is corrected to "I unlock the key once". Trigger `give it my password`; replacement `unlock the key once`.
- BDEFS (six, all under 17 characters): Private key, Certificate, Passphrase, ssh-agent, BatchMode, Login node.

## Cast per act (the same object is the same picture within an act)

| Act | Object | Picture | Beats |
|---|---|---|---|
| I | AICR | the large dark rack (4 slabs) from the AICR Introduction cast | B10 |
| I | key | a flat kraft key, ink outline, large | B10 B13 |
| I | certificate | a white page with three ghost lines, a terracotta dot and a seal | B10 B13 B16 |
| I, II, IV, V | you | a random Professor Bear portrait (PROFESSOR BEAR LAW), seeded by beat id | B14 B21 B40 B43 B45 |
| II, III | command | a small kraft box with one terracotta tape, labelled `ssh` | B20 B22 B31 B34 B37 B38 |
| II, III | lock | a padlock, ink outline, large | B20 B21 B31 |
| II, III | agent | a small dark slab with two ghost lights, labelled `agent` | B21 B22 B34 B37 B38 |
| III | Keychain | a dark vault block with a round door (macOS only) | B37 |
| IV | login node | the small dark rack (Explorer rack from the earlier cast) with a capped meter | B42 |
| IV | home, scratch | the small closed kraft box and the wide open bin | B47 |
| V | error plaque | a white card with the real error text in mono | B50 B51 |

Terminal beats (B15, B16, B30, B32, B33, B35, B36, B39, B52) show the real tool: `CCPlainShell` for commands and output, `ClaudeCodeBeat` for files and command lists. Their evidence is in FACTCHECK.md.

## Self-contained check

The film leans on three outside things and teaches each where it is needed: AICR (BIDEA: "the shared GPU cluster"), Slurm (B42: "the scheduler"), and the account itself (B11). Terms are in BDEFS. The narration never says "the guide", "the README", "last video" or names a section number. No course credit is used; the series is named on the opening card and in BOPEN.
