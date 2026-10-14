# STORY: Logging into Explorer with Claude

**What this is.** The facts behind the film about letting Claude Code log into Northeastern's Explorer cluster: make a key, install its public half, unlock it once into ssh-agent, test with BatchMode, and let Claude run read-only commands; then how this differs from AICR. **Why it matters.** Explorer starts with a password, and a password is the one thing an agent must never hold. **What we found.** On 2026-10-11 key login worked end to end on one account (including a real Claude Code login and a deliberate empty-agent test), with no Duo prompt on ssh. **What is NOT verified.** Login from off campus or another network, the web portal (OnDemand), and whether Research Computing permits automated agent access (no policy page mentions it).

Source: `hpc-aicr/Logging-into-Explorer-with-Claude/SESSION.md` (every terminal line on screen is read from it) and `hpc-aicr/skills/hpc/HPC.md` section 10; the differences from AICR come from `hpc-aicr/skills/aicr/AICR.md` section 3 and the AICR login film's record.

## Shape
1. What Explorer asks for: password login, no Duo on ssh (one account, one network); why a password does not work for Claude; which login name worked (the access form's user ID).
2. Make and install a key: two halves; `ssh-keygen`; `ssh-copy-id` (asks the password once).
3. Unlock it once: the agent; `ssh-add --apple-use-keychain`; the config block; a real mistake (no host alias).
4. Let Claude do it: BatchMode test; Claude Code's own read-only login; HPC.md rules; the empty-agent test, run deliberately.
5. How it differs from AICR; what is the same; what was not tested.
