# ACTS — Managing /projects on Explorer (lecture)

**What this is.** Coverage map for the lecture film of `hpc/Managing-Projects-on-Explorer/train_main.md`.
**Why.** A lecture covers the WHOLE source; every section must land in an act or be listed as left out.
**Result.** All ten sections covered in three acts, 10 body beats. Runtime ~5 min.

| Source section | Act | Beats |
|---|---|---|
| What is /projects? (three storage areas, quota table, request form) | I · Storage | B10 |
| Terminology and User Roles (five roles: Data Custodian, Guest, Member, Delegate, PI) | II · Roles | B20 |
| TTL (Time To Live) — administrative marker, not a countdown | II · Roles | B21 |
| Setup — must run from short partition with --constraint=ib | III · Commands | B30 |
| General command form | III · Commands | B31 |
| Viewing Your Group (view members / delegates / guests / groupemail / ttl) | III · Commands | B40 |
| Adding Users (add members / delegates / guests; worked examples) | III · Commands | B41 B42 |
| Removing Users (remove members / delegates; note delegate demotion) | III · Commands | B43 |
| Additional Commands (groups, getfacl) | III · Commands | B50 |
| Best Practices (review, least privilege, delegate, keep email current) + Help | III · Commands | B51 |

## LEFT OUT

Nothing. One detail compressed:
- Data Custodian role is mentioned in BDEFS but not given its own beat (it's an optional email address with no terminal commands attached — not worth a visual slot).
- Quick Reference table is not shown; its content is covered beat-by-beat in Acts II and III.

## Order

Source order preserved.

## Self-contained check

The source assumes Explorer. B10 names Explorer explicitly ("shared storage on Explorer") with enough context. All six prerequisite terms are defined in BDEFS. The film never says "this training" or "this document".
