# SHOTLIST: Running a Local LLM on Explorer

**What this is.** One row per body beat: what the sentence is about, the lane picked, the runner-up and why this one wins (BEST-BEAT LAW). **Why.** Each beat takes the picture whose MOTION is the claim. **Found.** 33 Manim scenes (mechanisms, structures, a real bar chart), 18 terminal beats (the scripts themselves are the evidence), 6 bookends. No pantry stills, no captures: no tool interface is drawn; Claude Code and Ollama appear as their logos (LOGO LAW).

SHOW-THE-THING: no beat shows a tool's interface, so no capture or skin was needed. Terminal beats show the tutorial's real script text on `CCPlainShell`; no output is shown (none was recorded).

| beat | about | lane picked | runner-up | why this one wins |
|---|---|---|---|---|
| B10 | the idea: ask for a GPU, run a model, agent sends requests | Manim, isometric rack + chips | `ShowTellCard` flow | the arrangement of things (rack, model, agent, files) is physical; a price tag crossing out is the claim |
| B11 | three layers | Manim diagram, three bands | `LibraryIconRow` (3 icons) | the bands stack in the order they depend on each other |
| B12 | Pattern A: everything in one job | Manim, one boundary around agent + model + repo | isometric conveyor | a boundary with a crossed network line is the claim "nothing crosses" |
| B13 | Pattern B: laptop, tunnel, login node, lock | Manim, left-to-right flow with a lock | `DesignPipelineClaim` isometric | the packet stopping at the lock is the claim |
| B20 | an open interface at 0.0.0.0 | Manim, rack with a door | terminal with the env line | the door swinging closed is the fix; strangers reaching in is the harm |
| B21 | the right way: `--env` to localhost | `CCPlainShell`, wrong then right lines | Manim diff | the exact lines are the evidence |
| B22 | base address builds the path | Manim, address pieces slide together | terminal curl lines | a doubled `/v1/v1` colliding is the claim |
| B23 | tunnel target is the compute node | Manim, laptop-login-compute pipes | terminal ssh -L | which machine the pipe ends at is the claim |
| B24 | aliases mapped to one local model | Manim, four arrows converge | terminal env lines (B34 shows them) | arrows redrawn to one block show "every name" |
| B25 | default window sizes cut silently | Manim, window bar with pouring blocks | `ShowTellCard` chart | blocks cut off at the edge without any error is the claim |
| B26 | a tiny model cannot hold the tool list | Manim, two blocks and a card pile | bar chart of sizes | the tiny block dropping the pile |
| B27 | no per-token billing, costs move | Manim, price tag crossed, three meters | `ShowTellCard` dashboard | the meters replacing the tag |
| B30 | the environment file | `CCPlainShell`, env.sh lines | `ClaudeCodeBeat` listing | the real file with the scratch default ringed |
| B31 | home fills from a hidden cache | Manim, quota gauge and redirect | terminal lines | the gauge filling then arrows redirecting |
| B32 | the pulls and the version check | `CCPlainShell`, apptainer lines | Manim | real commands, `latest` ringed |
| B33 | the start script | `CCPlainShell`, key lines | `ClaudeCodeBeat` | localhost and the context flag ringed |
| B34 | the Claude Code script | `CCPlainShell`, env lines | Manim alias map | `unset ANTHROPIC_API_KEY` ringed |
| B35 | a token, then the install | `CCPlainShell` | Manim key | the real commands |
| B40 | weights plus cache must fit | Manim, tank and blocks | bar chart | spill onto the processor and a slow stopwatch |
| B41 | download sizes of three models | Manim real bar chart, shared ruler | `ShowTellCard` chart | numbers are real; the hatched extension is the video-memory figure |
| B42 | strongest model, the tools label | Manim, long bar + two model cards | `LibraryIconRow` | a call running vs printing as text |
| B43 | one GPU per job, which type | Manim, rack with typed slots | terminal sinfo | the h200 slot taking every model |
| B44 | context floor, q8_0 halves the cache | Manim, two cache blocks and a knob | bar chart | the block halving on the knob |
| B50 | the interactive GPU session | `CCPlainShell`, tmux and srun | Manim | the real srun line, time ringed |
| B51 | start Ollama, pull, prove | `CCPlainShell`, six lines | Manim | the proof commands and what they should read |
| B52 | point Claude Code, `/status` | `CCPlainShell` | a Claude Code skin | no session was run, so only the typed commands are shown (SHOW-THE-THING rung 2 would invent output) |
| B53 | unsupported route, web search, caching | Manim, Claude chip with ticked and crossed capabilities | `ShowTellCard` | the road sign plus crossed chips |
| B54 | context grows, exit twice | Manim, growing bar and two exits | terminal | the bar growing and the two exit arrows |
| B55 | headless batch run | `CCPlainShell`, sbatch lines | Manim | the real batch header with `claude -p` ringed |
| B60 | a lock in front of the model | Manim, gate with a padlock and a key packet | terminal Caddyfile | the packet passing or being refused |
| B61 | the proxy's rulebook | `CCPlainShell`, Caddyfile lines | Manim | the exact rules; 401 and `admin off` ringed |
| B62 | the laptop tunnel script | `CCPlainShell` | Manim | real ssh lines, tunnel ringed |
| B63 | check the lock | `CCPlainShell`, two curls and what to expect | Manim | the commands and expected 401 |
| B64 | two residual risks, then cancel | Manim, rack with bypass dots and a plain-text token | terminal scancel | the bypass reaching the random port |
| B70 | Aider on the node and from the laptop | `CCPlainShell` | Manim | the two real invocations |
| B71 | Continue's config.yaml | `CCPlainShell`, YAML lines | Manim | the real YAML |
| B72 | `ollama launch` and its defaults | Manim, box with default vs random port | `LibraryIconRow` logos | the line breaking at a random locked port; logos for Codex and OpenCode, mono chip for Droid (no logo exists) |
| B80 | four common failures | Manim, symptom-cause table | `ShowTellCard` | each cause ringed as it lands |
| B81 | home full, proxy lost on purge | Manim, node with proxy gate and module chip | terminal | the purge sweeping the chip away |
| B82 | proxy variables vs a local server | `CCPlainShell`, RC's commands | Manim | the three commands from Research Computing |
| B90 | the idle watcher | Manim, utilisation line with 15 min and 1 hour | `ShowTellCard` chart | the email then the cancel on a bursty line |
| B91 | an endpoint is not a job's shape | Manim, 8 h dial and cache blocks | bar chart | the endpoint dying and returning elsewhere |
| B92 | a service for many people | Manim, batching server and question chips | terminal | pages merging into one batch; three questions |
| B93 | five questions for Research Computing | `CCPlainShell`, the five lines | `ClaudeComposerAsk` | the real questions, verbatim |
| B94 | AICR's scale and access | Manim, two racks | `LibraryIconRow` | the two GPU counts on the larger rack |
| B95 | what was and was not checked | Manim, two stamped columns | `ClaudeVerdictArtifact` | stamps landing on the five checks; the honesty beat |
| B100 | expect a weaker agent | Manim, growing context and glitching loop | `ShowTellCard` | the thread fraying |
| B101 | where it works and does not | Manim, two chip columns | `ShowTellCard` | chips landing with check and cross |
| B102 | the practical split | Manim, conveyor splitting work | bar chart | small boxes to the local rack, one heavy box to Claude |
| B110 | where to get the paste-in recipe | Manim, repository address and folder chain with dashed slots | `ShowTellCard` | the chain opening down to one page is the claim 'it is in this folder'; the same design as the sibling film's where-to-find beat |
| B111 | how to start: clone, claude, paste | `CCPlainShell`, three real commands from the guide | Manim | the exact commands from `GET-STARTED.md`, the paste step ringed; no output shown |

Lane histogram (information, not a quota): Manim 33, terminal 18 (`CCPlainShell`), bookends 6 (BOPEN card, hesitant writer, terms, recap, Your Turn, outro). Open misses logged: none (no component was missing); Aider and Droid have no logo (mono chips).
