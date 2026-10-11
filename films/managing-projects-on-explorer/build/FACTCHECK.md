# FACTCHECK — Managing /projects on Explorer

Source: `hpc/Managing-Projects-on-Explorer/train_main.md` (Northeastern Research Computing, Summer 2026 Training Series).

| # | Claim | Source ref | Status |
|---|-------|-----------|--------|
| 1 | /home quota: 75 GB | Source table row 1 | PASS — matches RC docs |
| 2 | /scratch quota: 50 TB | Source table row 2 | PASS |
| 3 | /scratch purged first Tuesday each month | Source table row 2 note | PASS |
| 4 | /projects: up to 35 TB free | Source table row 3 | PASS |
| 5 | project command must run from short partition (not login node) | Source §Setup | PASS |
| 6 | Setup command: `srun -p short --constraint=ib --pty bash` | Source §Setup code block | PASS |
| 7 | Guest: read and execute only (cannot write) | Source §Guest | PASS |
| 8 | Member: read, write, execute | Source §Member | PASS |
| 9 | Delegate: Member permissions + add/remove Members and Guests | Source §Delegate | PASS |
| 10 | Delegate cannot manage other Delegates | Source §Delegate | PASS |
| 11 | PI: all Delegate permissions + add/remove Delegates + view/update TTL and group email | Source §PI | PASS |
| 12 | TTL is administrative — does not restrict access or delete data | Source §TTL | PASS |
| 13 | Comma-separated user list, no spaces, for multi-user add/remove | Source §Adding Users note | PASS |
| 14 | Removing a delegate keeps them as a member | Source §Remove delegates | PASS |
| 15 | `groups <username>` shows group membership | Source §Additional Commands | PASS |
| 16 | `getfacl /projects/<name>` shows ACL | Source §Additional Commands | PASS |
| 17 | Data Custodian: email address (not necessarily a cluster user) for quota/TTL notifications | Source §Data Custodian | PASS |

**Sign-off:** All claims trace directly to the source document. No external verification required for cluster-specific operational facts (quoted verbatim from RC training material).
