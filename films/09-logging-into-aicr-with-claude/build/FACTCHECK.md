# FACTCHECK — Logging into AICR with Claude (lecture)

**What this is.** Every factual claim in the narration and on screen, checked. **Sources.** R = the source README (`hpc-aicr/Logging-into-AICR-with-Claude/README.md`); D = the saved AICR documentation SSH page (June 1, 2026); A = `aicr/bearsvoice/AICR-SETUP.md` section 2; S = `SESSION.md` (three real runs, 2026-10-11, copied beside this file); I = the AICR Introduction film's FACTCHECK. **Result.** 42 claims: 39 PASS, 3 CORRECTED. **Status.** Checked 2026-10-11 by the build agent; Bear's sign-off pending.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN, BIDEA | AICR is the shared GPU cluster; it has no password; access is a private key plus a certificate | PASS | R header; D "no separate AICR password. Your certificate is your credential"; I rows 1-8 | |
| 2 | BIDEA, B21, B22 | Claude never sees the key or passphrase: the agent holds the unlocked key and ssh asks it | PASS | R "Why it works", section 4 | |
| 3 | B10 | The certificate is signed by AICR's own certificate authority | PASS | R section 1; D "signed by AICR's Certificate Authority (CA)" | |
| 4 | B11 | A PI's proposal opens a project; the institution's research-computing team creates your user | PASS | R section 0 | |
| 5 | B11 | The user name has the form institutionalusername_institutioncode, e.g. <aicr-username> | PASS | R section 0; D (its example is jsmith_mit) | |
| 6 | B12 | Key files are downloaded from ood.aicr.ai after signing in with institutional credentials | PASS | R section 1; D | |
| 7 | B12 | The ood.aicr.ai sign-in page asks you to choose an identity provider | PASS | `captures/ood.png`, real page; I row 11 | |
| 8 | B13 | The folder is called aicr_keys and holds four files: private key (passphrase-protected), public key, CA-signed certificate, first passphrase | PASS | R section 1; D | |
| 9 | B14 | Signing in, putting files in place and choosing a passphrase are human steps; do not give Claude the institutional password | PASS | R header table, section 1 | |
| 10 | B15 | Commands: mkdir/chmod 700, mv, chmod 600 on the key, chmod 644 on the .pub files, ssh-keygen -p -f; Windows same in PowerShell | PASS | R section 2; D (chmod lines, Windows note) | |
| 11 | B15 | Delete the downloaded .passphrase file after choosing a new one | PASS | R section 2 | |
| 12 | B16 | `ssh-keygen -L -f` shows Type, Key ID, Valid, Principals; Valid is a date range or forever; renew in the OnDemand SSH Certificate app | PASS | R section 2; S certificate block (verbatim); D "Certificate Renewal" | the Extensions line (107 columns) and other fields are not shown; a comment says so |
| 13 | B16 | This account's certificate prints `Valid: forever` | PASS | S certificate block; A section 2 | the film shows the real output and says Valid is a date range or forever; it does not claim certificates never expire (D says they are short-lived) |
| 14 | B20 | Claude Code runs commands with no keyboard attached; ssh cannot answer a passphrase prompt so the command hangs or fails | PASS | R section 4 | |
| 15 | B21 | The key is unlocked once in your own terminal into ssh-agent, which holds it in memory | PASS | R section 4 | "in memory" is the standard meaning of the agent; R says the agent "holds" the key |
| 16 | B23 | The config block: Host aicr, HostName login.aicr.ai, User AICR_USERNAME, IdentityFile, CertificateFile | PASS | R section 3 verbatim; D (first five lines identical) | |
| 17 | B24 | IdentitiesOnly offers only this key; ServerAliveInterval 60 stops idle drops; AddKeysToAgent loads the key on first use; UseKeychain is macOS-only and IgnoreUnknown lets other systems skip it | PASS | R section 3; D "Connection drops frequently: ServerAliveInterval 60" | |
| 18 | B25 | macOS: `ssh-add --apple-use-keychain`; Linux: `eval "$(ssh-agent -s)"` then `ssh-add`; start Claude Code from the same terminal | PASS | R section 4 | |
| 19 | B26 | Windows: PowerShell as administrator once; Get-Service/Set-Service Automatic, Start-Service, ssh-add | PASS | R section 4 | |
| 20 | B27, B35, B36 | `ssh-add -l` prints one line ending in (ED25519): `256 SHA256:bu4j...yRYEU <aicr-username>@aicr.ai (ED25519)` | PASS | S Run 2 and Run 3, verbatim | |
| 21 | B30 | `ssh aicr hostname` should give login.aicr.ai; the first connection asks to confirm the host key, type yes yourself | PASS | R section 5; D "host key verification prompt. Type yes" | shown as commands and comments, not as captured output |
| 22 | B31 | BatchMode=yes makes ssh fail at once instead of asking | PASS | R section 5 | |
| 23 | B32 | Claude Code ran one ssh command with BatchMode on; the agent held no keys before that call | PASS | R "What was found"; S Run 1 | |
| 24 | B32 | The command and its first output lines: <aicr-username>, login.aicr.ai, Sun Oct 11 13:26:40 EDT 2026 | CORRECTED | S Run 1, verbatim | command shown on two lines with a `\` continuation; text identical |
| 25 | B33 | Seven partitions: cpu*, rtx-batch, b200-batch, b200-fullnode, rtx-devel, b200-devel, preemptable, with the real time limits and node counts | PASS | S Run 1, verbatim; 7 rows counted | |
| 26 | B33 | squeue showed no jobs (header only); the last line is the home directory /home/<aicr-username> | CORRECTED | S Run 1 | the recorder's note is shown as a comment line `# squeue: header only, no jobs`, not as output |
| 27 | B34 | A reboot empties the agent | PASS | R section 5 ("what a reboot does"); section 8 last row | |
| 28 | B35 | ssh-add -l shows the key; ssh-add -D prints "All identities removed."; ssh-add -l then prints "The agent has no identities." | PASS | S Run 3, verbatim | |
| 29 | B36 | With the agent empty, `ssh -o BatchMode=yes aicr 'whoami; hostname'` still printed <aicr-username> and login.aicr.ai, and ssh-add -l then showed the key again | PASS | S Run 3, verbatim | |
| 30 | B37 | On a Mac this is AddKeysToAgent plus the Keychain; nothing typed, nothing passed to Claude | PASS | S Run 3 closing paragraph; R section 5 | |
| 31 | B38 | On Linux and Windows there is no Keychain to reload the key; the same test fails until ssh-add is run again; add ssh-add to session start | PASS | R section 5 final paragraph | |
| 32 | B39 | `ssh -v` shows the agent returned 1 key, the certificate offered, accepted, and "Authenticated ... using publickey" | PASS | S Run 2, verbatim (filtered) | output was filtered to four lines; the screen says so |
| 33 | B40 | Claude runs `ssh -o BatchMode=yes aicr '...'`; approve the command, at least the first few times | PASS | R section 6 | |
| 34 | B41 | Read-only first: sinfo, squeue -u $USER, sacct, jobstats, ls, module avail | PASS | R section 7 rule 1 | |
| 35 | B42 | Login nodes are shared, 4 CPU cores and 8 GB per user; heavy work goes through Slurm (sbatch, or salloc/srun interactively) | PASS | R section 7 rule 2; D "4 CPU cores and 8 GB memory per user" | Slurm is explained as "the scheduler" (D "scheduler") |
| 36 | B43 | Ask before sbatch, scancel, rm, or anything writing outside your project; jobs use shared GPUs and count against the project | PASS | R section 7 rule 3 | |
| 37 | B44 | Never print, copy or upload the key (not cat, not scp, not into chat); Claude need not read it, the agent does | PASS | R section 7 rule 4 | |
| 38 | B45, B46 | Never put the passphrase in a prompt, file or command; use your own account only, the certificate names you | PASS | R section 7 rules 5 and 6 | |
| 39 | B47 | Home is small and recoverable; scratch is large and purged; check AICR's file-system page | PASS | R section 7 rule 7; I rows 15-17 | |
| 40 | B50, B51, B52 | Permission denied (publickey): key not unlocked (most common after a reboot), certificate expired or missing, permissions wrong; an empty agent looks exactly like an expired certificate; check ssh-add -l first; renew in OnDemand; chmod 600 the key | PASS | R section 8 row 1; D "Permission denied (publickey)"; A section 2 | |
| 41 | B53, B54 | Hang / passphrase, host key verification failed (ssh-keygen -R login.aicr.ai), new host key prompt, Bad configuration option (IgnoreUnknown), Connection timed out (no VPN), idle drops (ServerAliveInterval 60), empty agent after restart | PASS | R section 8 rows 2-8; D rows for timed out, host key failed, drops | |
| 42 | BVDT, BHTF | Recap lines restate rows above; the Your Turn prompt is the guide's step 6 prompt | CORRECTED | R section 6 | displayed prompt is verbatim; the spoken version says the sinfo output format and "s queue for my own user" aloud because `-o "%14P %11l %6D"` and `$USER` cannot be read as typed |

Claims stripped as datable or unsourced: none beyond the above. No hardware counts, no dates are spoken. The only date on screen is inside the real captured output (Run 1).
