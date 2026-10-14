# FACTCHECK — Logging into Explorer with Claude (lecture)

**What this is.** Every claim checked against the session record and the rule files. 2026-10-12. **Result.** PASS; caveats in Fix.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B10 | Explorer login: host key question, Northeastern password, a login node; no Duo prompt on ssh (one account, one network); the web portal asks per the documentation | PASS | SESSION.md 'password login'; HPC.md section 3 (OnDemand needs Duo) | web-portal part is documented, not tested; labelled so |
| 2 | B11 | Claude Code runs commands with no keyboard attached; a password is never handed to it | PASS | HPC.md section 1 and 10 | none |
| 3 | B12 | The working login name was the access form's user ID, not the email prefix; wait after a password change | PASS | SESSION.md; HPC.md section 3 | one account |
| 4 | B20-B22 | Key halves; ssh-keygen -t ed25519; ssh-copy-id asks the password once and adds one key | PASS | SESSION.md steps 1 and 2 (read at build) | none |
| 5 | B30-B31 | Unlock once into the agent; ssh-add --apple-use-keychain prints Identity added; the Keychain can reload the key when the agent is emptied | PASS | SESSION.md steps 4 and the empty-agent test | reload observed once, on a Mac |
| 6 | B32 | The config block lines | PASS | SESSION.md step 3 (read at build) | none |
| 7 | B33 | Before the config block, ssh could not resolve hostname explorer | PASS | SESSION.md 'A real mistake' | none |
| 8 | B40-B41 | BatchMode test printed <explorer-username> and explorer-01; Claude Code ran whoami, hostname, pwd, squeue read-only; empty job list | PASS | SESSION.md steps 5 and 'Claude Code runs it' | none |
| 9 | B42 | The HPC.md rules: read-only first, ask before submit/cancel/delete, no compute on the login node, stop on a prompt | PASS | HPC.md sections 1 and 10 | none |
| 10 | B43 | ssh-add -D emptied the agent; login still worked; the key was back; the command empties every key and only the researcher should run it | PASS | SESSION.md empty-agent test; HPC.md and AICR.md hard nevers | it was run in a Claude Code session at the researcher's request; our rules now forbid the agent running it |
| 11 | B50 | Differences: Explorer password then your own key; AICR no password, downloaded key and CA-signed certificate; user name forms; access by sponsor versus proposal | PASS | HPC.md section 3; AICR.md sections 2 and 3 | none |
| 12 | B51-B52 | Same: ssh, agent, BatchMode, Claude never holds secrets; untested: off campus, web portal, agent policy | PASS | SESSION.md findings; HPC.md section 10 | none |
