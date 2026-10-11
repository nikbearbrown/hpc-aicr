# Requesting Access to Explorer from Your Group

**What this is.** How a member of a research group gets onto Northeastern's Explorer cluster: who has to act, which form to fill in, what the form asks, how to confirm you are in, and what your login name is. It is the source document for a short film, and it only states what a source or a real screen confirms. Anything that is not confirmed is marked **NOT CONFIRMED**.

**Why it matters.** Explorer will not let you in just because you have a Northeastern login. Every user must belong to a storage space owned by a sponsor (a PI or staff member). So "request access" really means "get added to your sponsor's group".

**What was found.** There are two routes. The sponsor (or a delegate they chose) can add you directly with one command, or you can submit the ServiceNow access form and name your sponsor. The form's first screen is pre-filled from your university record and asks one thing of you: whether you are requesting a new account or already have access and need to update your sponsor. Your login name is your Northeastern username, and the name that worked in a real test was the UserID the form shows.

---

## 1. The rule that decides everything

Every Explorer user must belong to a **sponsor-owned storage space** (a directory under `/projects`). Storage is free for research groups up to 35 TB. If a sponsor has no storage space yet, they request one first. Classroom use goes through a separate instructor form. *(Sources: Research Computing "Intro to Explorer and OOD" slides, section "How to get an account on Explorer"; the access form's own text.)*

## 2. The people involved

| Role | What they can do | Source |
|---|---|---|
| **PI (sponsor, owner)** | Owns the project. Can add and remove members, guests and delegates | rc-docs "Terminology" |
| **Delegate** | A member the PI elevates. Can add and remove members | rc-docs "Terminology" |
| **Member** | Reads, writes and runs in the project. Cannot add other people | rc-docs "Terminology" |
| **Guest** | Reads and runs in the project, cannot write | rc-docs "Terminology" |

Research Computing recommends every PI name at least one delegate, so adding people does not wait on the PI.

## 3. Route A: your sponsor adds you

**Without a terminal (new, announced 2026-08-25).** Research Computing added an Open OnDemand app called **Managing /projects**. On the Explorer OnDemand dashboard it is under **Files → Managing /projects**. The person adding someone picks the group from a drop-down, types the usernames to add (comma-separated, no spaces), and clicks **Launch**. That submits a short job on the `short` partition that finishes in under ten minutes, and its output log shows who was in the group and what changed. The announcement says no support ticket is needed. The app only lists groups the person already belongs to and may modify, and it lets them add and remove in one go. **Delay:** changes can take up to **2 hours** to take effect across the cluster, and a newly added user may need to start a fresh login session, because group membership is read at login. If a project is missing from the drop-down, contact rchelp@northeastern.edu. *(Source: https://rc.northeastern.edu/2026/08/25/managing-projects-through-open-ondemand-ood/ , read 2026-10-11.)* The announcement says anyone with an Explorer account can open the app; it does not say what a person with no account yet should do (see below).

**With a command.** The PI or a delegate runs, on a cluster node in the `short` partition (reached with `srun -p short --constraint=ib --pty bash`):

```bash
project <project_name> add members <username>
```

Several people go in as a comma-separated list with no spaces: `project mylab add members rot1,rot2,rot3`. To check afterwards: `project <project_name> view members`. *(Source: rc-docs "Group Management Commands"; the Managing /projects training.)*

You give your sponsor your **Northeastern username**. **NOT CONFIRMED:** whether `project ... add members` works for a person who has never had an Explorer account, or whether the account is created some other way. Ask Research Computing (rchelp@northeastern.edu) before promising this route to a brand-new user.

## 4. Route B: you submit the access form

The form is the Northeastern Tech Service Portal (ServiceNow) item reached at https://bit.ly/NURC-AccessRequest. It needs your university sign-in. Its first screen, as it appeared on 2026-10-11:

**Requester Information**, pre-filled from your university record:

| Field | What it holds |
|---|---|
| Requester | your name, as "Last, First" |
| Phone | blank, to fill in |
| Email | your Northeastern email |
| Location | your campus (a drop-down) |
| UserID | your university user ID |
| Department | your department (a drop-down) |

**Please choose one** (required):
- "I do not have access to the High Performance Computer (HPC) cluster. I am requesting a new account."
- "I already have access to the High Performance Computer (HPC) cluster. I need to update my sponsor information."

Then two paragraphs of instruction, in the form's own words in substance: to have access to the HPC environment, all users must belong to a sponsor-owned storage space; if the sponsor has no storage space they can request one (a link); alternatively, if a storage space exists, its owner can add members to the cluster themselves, following the documentation (a second link).

**NOT CONFIRMED:** everything below that point on the form, including how it asks for the sponsor, any approval step, and how long approval takes. The first screen was captured; the rest was not.

### What the sign-in does (observed, with a hedge on the rest)

The form sits behind the Northeastern sign-in page, captured by Bear on 2026-10-11 (`captures/northeastern-sign-in.png`; no personal data on it). Its fields and wording: **"Sign in"**, a box labelled "Email or Username@northeastern.edu", a "Can't access your account?" link, a **Next** button, the line "Please sign in using your Northeastern username@northeastern.edu or email address and password.", a "Tech Service Portal" link for 24/7 service and support, and a "Sign-in options" row.

**Observed:** after signing in, the form's Requester, Email, UserID and Department fields were already filled with the signed-in person's details. Signing in is what identifies you; you do not type who you are.

**How the film words the rest (Bear's call, 2026-10-11):** where the sources do not say how the form is processed, for example whether the named sponsor gets an approve-or-deny request, the film may say "we think this is how it works", out loud and on screen, and must say the viewer should confirm with Research Computing. It never states an unconfirmed step as fact.

## 5. After you are in: log in and check

- Your username is your Northeastern username. The training slides' example is `s.caplins`, which looks like the first part of an email address. **Confirmed on a real login, 2026-10-11:** for one faculty user whose email prefix is `<email-prefix>`, the login that worked was the **UserID** shown on the access form (`<explorer-username>`), not the email prefix. So look at the form's UserID field: that is the name to try first. One user's result; the first successful login settles it for anyone else.
- **Confirmed on the same login:** `ssh <username>@login.explorer.northeastern.edu` asks for the first-time host-key question (type `yes`), then for the **Northeastern password** (the same one used for university email and sign-in; nothing is shown as you type), and then lands on a login node (`explorer-01`) with a welcome banner. **No Duo prompt appeared on the SSH login.** Open OnDemand is documented as password plus Duo.
- Terminal: `ssh <username>@login.explorer.northeastern.edu`, then your Northeastern password. Open OnDemand: https://ood.explorer.northeastern.edu, with your Northeastern username and password and Duo.
- Confirm with `whoami` (your login name) and `groups` (it should list your sponsor's project group).
- Home is `/home/<username>`; scratch is `/scratch/<username>`.

## 6. If something is wrong

| You see | Likely cause | What to do |
|---|---|---|
| OnDemand or SSH rejects your login | No Explorer account yet, the wrong username, or a password changed minutes ago | Try the UserID from the form, then your email prefix; wait a while after a password change; if you are sure, submit the form |
| You can log in but `groups` does not list the project | Your sponsor has not added you to the project | Ask the PI or a delegate to run the add command |
| You are the sponsor and have no storage space | Nothing to add people to | Submit the storage space request first |
| Anything else | | rchelp@northeastern.edu |

## 7. Sources

- Research Computing training slides: `../Intro-to-Explorer-OOD-2026/Intro_explorer_ood.md` (account section, how to access Explorer).
- Research Computing training, Managing /projects: `../Managing-Projects-on-Explorer/train_main.md`.
- rc-docs.northeastern.edu: "Group Management Commands" (https://rc-docs.northeastern.edu/en/latest/managingprojects/commands.html), "Terminology" (https://rc-docs.northeastern.edu/en/latest/managingprojects/terminology.html), "Connecting to Explorer, Mac" (https://rc-docs.northeastern.edu/en/latest/connectingtocluster/mac.html). Read 2026-10-11.
- The access form: first screen captured by Bear, 2026-10-11 (screenshot). The form is behind university sign-in and was not captured by the build.
