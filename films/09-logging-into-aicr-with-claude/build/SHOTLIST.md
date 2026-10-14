# SHOTLIST — Logging into AICR with Claude (lecture)

**What this is.** One row per body beat: what the sentence is about, the lane picked, the runner-up, and why the pick wins (BEST-BEAT LAW). **Result.** 38 body beats: 15 isometric/flat drawings in the show-tell kit, 8 Manim diagrams, tables and text transforms, 1 real web capture, 9 real terminal beats, 5 real code listings. No text-only cards in the body. The real terminal is used wherever the beat is about what a command prints; drawings only where the claim is a relationship (who holds what, what blocks what).

| Beat | About | Lane picked | Runner-up | Why this one wins |
|---|---|---|---|---|
| B10 | no password; key + certificate at the door | drawing: key and certificate arrive at a padlocked door in front of the AICR rack; the lock opens | icon row (key, certificate) | the claim is "two things must both arrive"; two objects meeting at a lock is that claim, and it sets the film's cast |
| B11 | user name pattern | Manim text transform in mono: pattern -> <aicr-username> | static example card | the fact is the shape of the name; bracketing the two halves and transforming shows it |
| B12 | the portal where key files come from | **the real page**, captured (BrowserCapture) | drawn browser window | SHOW-THE-THING rung 1: the viewer will see exactly this page; the camera pushes to the sign-in choice as "you sign in" is said |
| B13 | the four files | Manim drawn table with the real file names; certificate row ringed | isometric file stack | the source's table is the figure to animate (WHOLE-SOURCE LAW 5); the names are the artifact |
| B14 | which steps are the human's | drawing: portrait plus three check chips; Claude's door stays shut to the password | two-column "You / Claude" card | the person is Professor Bear (PROFESSOR BEAR LAW); the shut door is the rule |
| B15 | put files in ~/.ssh, set permissions, new passphrase | **the real commands** (ClaudeCodeBeat, line by line on the voice) | terminal shell | they are commands to copy; a listing card reads them at size |
| B16 | check the certificate | **the real output** of ssh-keygen -L (CCPlainShell), Valid and Principals ringed | drawn certificate page | the viewer will see this output; the rings land on the two fields named |
| B20 | Claude cannot answer a passphrase prompt | drawing: the command box waits at the locked key, "passphrase?" with no answer | terminal showing a hang | no real hang was recorded and none will be invented; the drawing shows the stall honestly as a concept |
| B21 | unlock once, into the agent | drawing: portrait unlocks the key, it slides into the agent; the passphrase is refused to "Claude" | diagram with arrows | "before Claude arrives" is a sequence of who touches what; objects moving show it |
| B22 | ssh asks the agent; the key never leaves | drawing: command asks, agent answers with a slip, key stays inside a barrier | sequence diagram | the picture of the key staying put while a signed slip travels is the key idea of the film |
| B23 | the config block, first five lines | **the real text** (ClaudeCodeBeat), lines land on their names | drawn form | it is a file to copy; show the file |
| B24 | the five flag lines | **the real text**, first five lines already there, flags land on their words | merge into B23 | ten lines at once is unreadable at the type floor; two beats keep it readable |
| B25 | macOS and Linux unlock commands | **the real commands** (ClaudeCodeBeat) | terminal shell | commands without output; a listing card is honest about that |
| B26 | Windows unlock commands | **the real commands** (ClaudeCodeBeat, PowerShell) | merge into B25 | a third operating system on one card pushes the card under the type floor |
| B27 | confirm the agent holds the key | **real output**: ssh-add -l (CCPlainShell), key line ringed | drawn agent with a light | the line the viewer should see is the artifact |
| B30 | test by hand, host key prompt | **the real command** in a plain terminal; expected result as a comment | drawn prompt | the host-key prompt was not captured, so it is told, not shown |
| B31 | BatchMode fails at once | drawing: two lanes to one lock, one waits, one bounces at once | terminal | falsification: the picture of "waits forever" versus "fails at once" is the whole point of BatchMode |
| B32 | the real run: command and first lines | **real command and output** (CCPlainShell), user name and host ringed | CCToolCall block | the Bash tool-call row cannot hold the 90-column command at readable size; a plain shell shows the same real text without mocking an interface |
| B33 | the real run: partitions, queue, home | **real output** (CCPlainShell) | drawn table | seven real rows beat a redrawn table |
| B34 | why test with an empty agent | drawing: a reboot dial, the key leaves, the agent goes dark | text card | sets up the centrepiece: the empty agent is the thing being tested |
| B35 | empty the agent on purpose | **real output** (CCPlainShell), the empty answer ringed | drawing | centrepiece part 1: the viewer sees one key, then "no identities" |
| B36 | log in with an empty agent | **real output**; first two lines already on screen, login result and the key's return ringed | drawing | centrepiece part 2: the proof; the rings land on "it still works" and "the key is back" |
| B37 | the Keychain refills the agent (macOS) | drawing: vault returns the key to the agent; nothing crosses the barrier | text | the mechanism behind the proof is invisible in the terminal; the drawing is labelled as the explanation |
| B38 | no Keychain on Linux and Windows | drawing: no vault; the box bounces; you run ssh-add; add it to session start | table row | the contrast with B37 (same agent, no vault) is the claim |
| B39 | how it authenticated | **real output** of ssh -v (filtered, four lines) | drawn handshake | the viewer sees the certificate offered, accepted and the word publickey |
| B40 | approve each ssh command | drawing: the command waits at a gate beside the portrait, a check lands | CCToolCall approval | no real approval capture exists; a conceptual drawing of the habit is clearly conceptual |
| B41 | rule 1, read-only first | Manim: six real command pills each take a check | icon row | real commands are the content; pills hold mono text |
| B42 | rule 2, the login-node cap | drawing: capped meter, 4 cores and 8 GB, a heavy job stopped and sent through Slurm | chart | "capped" is a ceiling; a job meeting a ceiling shows it |
| B43 | rule 3, ask before changing | drawing: three commands wait at a gate, each takes a check | list | asking is a gate; a gate with a person beside it is the rule |
| B44 | rule 4, never print or copy the key | drawing: cat, scp and chat bounce off a barrier round the agent | list | "never" reads as things that cannot get through |
| B45 | rule 5, never type the passphrase into a prompt | drawing: refused by prompt, file and command; returns to you | list | same grammar as B44 for the passphrase, which keeps the cast |
| B46 | rule 6, your own account | drawing: the certificate names one portrait; a second slot is refused | text | the certificate names you: a leader line to your portrait shows it |
| B47 | rule 7, where files live | drawing: home box (recoverable) beside scratch bin (purged) | table | reuses the AICR Introduction cast so the pair is recognisable |
| B50 | the common error and its three causes | Manim: real error plaque, three cause cards, the likeliest largest | table | one error, three causes, one dominant: size carries the odds |
| B51 | the trap: same error, two causes | Manim: twin plaques, a curtain lifted by ssh-add -l | side-by-side table | falsification: identical symptoms, different truths; lifting the curtain is the claim |
| B52 | the three checks in order | **the real commands** (CCPlainShell), no output (none was run) | numbered list | commands to type; comments number the steps |
| B53 | quick fixes, part 1 | Manim drawn table, row ringed as it is said | text list | the source's table is the figure to animate |
| B54 | quick fixes, part 2 | Manim drawn table continued | merge with B53 | seven rows in one beat would be two sentences per row; two beats keep the pace |

## Tool beats and their SHOW-THE-THING rung

| Beat | Tool | Rung | Evidence |
|---|---|---|---|
| B12 | OnDemand sign-in (CILogon) | 1, real capture | `captures/ood.png`, public page, headless, 2026-10-02 |
| B16, B27, B35, B36, B39, B32, B33 | terminal | 1, real output | `SESSION.md`, verbatim |
| B15, B23, B24, B25, B26, B30, B52 | terminal commands and config text | real text of the guide, no output shown | README sections 2 to 5 and 8 |
| B20, B21, B22, B31, B34, B37, B38, B40 | Claude Code, ssh-agent, the Keychain | conceptual drawings, labelled by role, never presented as an observed session | none needed: no interface is reproduced |
| not shown | OnDemand file browser, SSH Certificate app, Claude Code approval prompt | behind a sign-in or not captured | nothing is drawn as if it were the real screen |

## Built for this film

- `CCPlainShell` gained optional `lineCues` (a frame per line), `rings` (terracotta ring round chosen lines) and `windowMargin`. `ClaudeCodeBeat` gained optional `lineCues`. All default to the old behaviour.
- Cast helpers in `_kit_cast.py`: key, padlock, certificate page, agent slab, vault, chip, plaque.
