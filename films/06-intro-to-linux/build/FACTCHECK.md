# FACTCHECK — Intro to Linux (lecture)

**Source.** S = the training document. **Result.** 14 claims, all PASS. Checked 2026-10-06.

| # | Beat | Claim | Verdict | Source |
|---|---|---|---|---|
| 1 | B10 | Linux kernel, Torvalds, 1991, Unix lineage incl. macOS; phones to clusters; free/open source; secure/robust | PASS | S §1 (historically accurate) |
| 2 | B11 | prompt fields; $ normal / # root; sudoers message | PASS | S §1.2 verbatim |
| 3 | B20 | colour code; absolute vs relative; . and .. | PASS | S §2, 2.1 |
| 4 | B21 B22 | pwd, ls, -l, -a, hidden files; cd, cd .., cd ~ | PASS | S §2.2 verbatim (ls -l shortened to two rows) |
| 5 | B30 | touch; > overwrites; >> appends; mkdir | PASS | S §3.1 verbatim |
| 6 | B31 | cp, cp -R, mv, mv as rename | PASS | S §3.2 verbatim |
| 7 | B32 | rm, rm -r; cannot be undone | PASS | S §3.3 |
| 8 | B33 | ln -s target link; l and ->; broken if the original moves | PASS | S §3.4 verbatim |
| 9 | B40 | cat vs less; keys; ESC does not close | PASS | S §4 |
| 10 | B50 | u/g/o/a; r/w/x = 4/2/1; execute on a directory = enter it | PASS | S §5.1–5.2 |
| 11 | B51 | the eight fields of the example line; rwx rw- r-- readings | PASS | S §5.2 |
| 12 | B52 B53 | chmod symbolic and octal (751 = 7/5/1); chown, -R | PASS | S §5.4–5.5 |
| 13 | B60 | nano; ^ = Ctrl; vim modes; i, ESC, :wq, :q! | PASS | S §6 |
| 14 | B70 | Tab; Ctrl+C; clear | PASS | S §7 |
