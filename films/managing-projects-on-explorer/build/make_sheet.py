#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-managing-projects.

Source: hpc/Managing-Projects-on-Explorer/train_main.md
Skill: lecture (brutalist.art/skills/make/lecture/SKILL.md)
Spine: BIDEA -> BDEFS -> Acts I–III -> BVDT -> BHTF -> BOUT
Voice: Liam, Kokoro am_onyx (free)
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Managing /projects on Explorer"
FPS = 30

A1 = "I · Storage"
A2 = "II · Roles"
A3 = "III · Commands"


def _dur(text):
    return round(len(text.split()) / 2.5, 1)


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", lane="remotion", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": gate,
         "narration_text": narration,
         "estimated_duration_s": _dur(narration),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show,
                  "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


def manim(bid, act, narration, cls, image, show):
    return {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration,
            "estimated_duration_s": _dur(narration),
            "voice": "am_onyx", "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own",
                     "visual_intent": image, "show": show,
                     "manim": {"class": cls}, "motion_claim": image}}


# ─────────────────────────── opening pair ───────────────────────────
OPEN = [
    remotion("BIDEA", "the idea",
        "Hallo. This is Liam, in for Bear. A new grad student joins the lab. "
        "Who adds them to slash projects? If the answer is submit a ticket and wait, "
        "you haven't met the project command yet. This lecture covers how shared storage "
        "actually works on Explorer, the five access roles, and every command a PI — or "
        "their delegate — needs to run a lab without calling for help.",
        "BrutalistHesitantWriter",
        {"text": "I need to submit a ticket\nto add someone to /projects",
         "triggerWords": "submit a ticket",
         "replacementWords": "use the project command",
         "fontSize": 70, "charMs": 62, "hesitateBetween": 6,
         "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
         "seed": SLUG, "banner": ""},
        [{"at": 0.0, "event": "types 'I need to submit a ticket to add someone to /projects'"},
         {"at": 0.35, "event": "backspaces 'submit a ticket' -> 'use the project command'"}],
        lane="bookend", lead_silence_s=0.8,
        motion_claim="The writer types the misconception (ticket) and corrects it (project command).",
        qc={"sparse_by_design": True,
            "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),

    remotion("BDEFS", "terms",
        "Six terms. Slash projects: persistent shared storage on Explorer, up to 35 terabytes free, "
        "right place for research data and shared pipelines, not slash scratch. The project command: "
        "terminal tool that lets PIs and delegates manage membership directly, no ticket. PI: project "
        "owner, full control over roles, email, and TTL. Delegate: trusted lab member promoted by the "
        "PI, can add and remove members and guests. T T L, time to live: administrative marker, not "
        "a countdown — Research Computing emails the PI when it expires, data untouched. And IB "
        "constraint: InfiniBand network fabric required by the project command, which is why you land "
        "on a compute node before running anything.",
        "ClaudeDefinitions",
        {"title": "Terms In This Lecture",
         "terms": [
             {"term": "/projects", "meaning": "persistent shared storage on Explorer, up to 35 TB free — the right place for research data"},
             {"term": "project command", "meaning": "terminal tool letting PIs and delegates manage /projects membership directly"},
             {"term": "PI", "meaning": "project owner: full control over roles, group email, and TTL"},
             {"term": "Delegate", "meaning": "trusted lab member promoted by the PI; can add/remove members and guests"},
             {"term": "TTL", "meaning": "Time To Live: administrative marker, not a countdown — data is never touched when it expires"},
             {"term": "IB constraint", "meaning": "InfiniBand fabric required by the project command; run srun --constraint=ib first"},
         ],
         "folderLabel": "@NikBearBrown"},
        [{"at": 0.08, "event": "'/projects' lands"},
         {"at": 0.25, "event": "'project command'"},
         {"at": 0.42, "event": "'PI'"},
         {"at": 0.60, "event": "'Delegate'"},
         {"at": 0.75, "event": "'TTL'"},
         {"at": 0.88, "event": "'IB constraint'"}],
        gate="CARD", lane="bookend",
        qc={"sparse_by_design": True,
            "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

# ─────────────────────────── Act I · Storage ───────────────────────────
ACT1 = [
    remotion("B10", A1,
        "Three storage areas on Explorer. Slash home: 75 gigabytes, personal scripts and "
        "configuration files. Slash scratch: 50 terabytes — but purged on the first Tuesday "
        "of every month, so not for long-term storage. Slash projects: up to 35 terabytes, "
        "free, persistent, and shared across your entire lab.",
        "LibraryIconRow",
        {"title": "Storage on Explorer",
         "items": [
             {"label": "/home", "sub": "75 GB · personal", "icon": "home", "at": 0.15, "mono": True},
             {"label": "/scratch", "sub": "50 TB · purged monthly", "icon": "trash", "at": 0.42, "mono": True},
             {"label": "/projects", "sub": "35 TB · persistent", "icon": "database", "at": 0.72, "mono": True},
         ],
         "durationSeconds": _dur("Three storage areas on Explorer. Slash home: 75 gigabytes, personal scripts and "
                                  "configuration files. Slash scratch: 50 terabytes — but purged on the first Tuesday "
                                  "of every month, so not for long-term storage. Slash projects: up to 35 terabytes, "
                                  "free, persistent, and shared across your entire lab."),
         "iconPx": 320},
        [{"at": 0.15, "event": "/home tile lands"},
         {"at": 0.42, "event": "/scratch tile lands"},
         {"at": 0.72, "event": "/projects tile lands"}]),
]

# ─────────────────────────── Act II · Roles ───────────────────────────
ACT2 = [
    remotion("B20", A2,
        "Four active roles, stacked by permission. Guest: read-only access to the project "
        "directory. Member: read and write. Delegate: everything a Member can do, plus the "
        "power to add and remove members and guests on the PI's behalf. PI: full ownership — "
        "manages delegates, views and updates the group email, and sees the TTL.",
        "LibraryIconRow",
        {"title": "Access Roles",
         "items": [
             {"label": "Guest", "sub": "read-only", "icon": "eye", "at": 0.10},
             {"label": "Member", "sub": "read + write", "icon": "pencil", "at": 0.32},
             {"label": "Delegate", "sub": "manages members", "icon": "users", "at": 0.57},
             {"label": "PI", "sub": "full control", "icon": "shield", "at": 0.78},
         ],
         "durationSeconds": _dur("Four active roles, stacked by permission. Guest: read-only access to the project "
                                  "directory. Member: read and write. Delegate: everything a Member can do, plus the "
                                  "power to add and remove members and guests on the PI's behalf. PI: full ownership — "
                                  "manages delegates, views and updates the group email, and sees the TTL."),
         "iconPx": 220},
        [{"at": 0.10, "event": "Guest tile lands"},
         {"at": 0.32, "event": "Member tile lands"},
         {"at": 0.57, "event": "Delegate tile lands"},
         {"at": 0.78, "event": "PI tile lands"}]),

    manim("B21", A2,
        "Every project gets a TTL when it's created. Think of it as an expiration date on "
        "the administrative record, not on your data. When it lapses, Research Computing "
        "emails the PI: still active? any changes needed? The data sits exactly where it was.",
        "TTLTimeline",
        "Horizontal timeline: 'project created' → 'TTL expires' → 'RC emails PI'; annotation 'data untouched' below.",
        [{"at": 0.0, "event": "timeline draws left to right"},
         {"at": 0.55, "event": "TTL marker highlighted"},
         {"at": 0.75, "event": "'RC emails PI' lands; 'data untouched' annotation fades in"}]),
]

# ─────────────────────────── Act III · Commands ───────────────────────────
ACT3 = [
    remotion("B30", A3,
        "One rule before any project command: you have to be on a compute node in the "
        "short partition. From the login node, run s-run dash-p short dash dash constraint "
        "equals ib dash dash pty bash. Your prompt changes to show a compute node hostname. "
        "Now you're ready.",
        "CCPlainShell",
        {"title": "getting onto an IB compute node",
         "lines": [
             "$ srun -p short --constraint=ib --pty bash",
             "[s.caplins@c0123 ~]$",
         ],
         "startCue": 15, "lineGap": 36,
         "durationSeconds": _dur("One rule before any project command: you have to be on a compute node in the "
                                  "short partition. From the login node, run s-run dash-p short dash dash constraint "
                                  "equals ib dash dash pty bash. Your prompt changes to show a compute node hostname. "
                                  "Now you're ready.")},
        [{"at": 0.2, "event": "srun command appears"},
         {"at": 0.65, "event": "new prompt appears"}]),

    remotion("B31", A3,
        "Every command follows the same four-part form: project — the project name — "
        "the action — the subcommand — and optionally, a list of users. Memorize the shape; "
        "the subcommands are readable.",
        "CCPlainShell",
        {"title": "command structure",
         "lines": [
             "$ project <project_name> <action> <subcommand> <users>",
         ],
         "startCue": 15, "lineGap": 36,
         "durationSeconds": _dur("Every command follows the same four-part form: project — the project name — "
                                  "the action — the subcommand — and optionally, a list of users. Memorize the shape; "
                                  "the subcommands are readable.")},
        [{"at": 0.3, "event": "command form appears"}]),

    remotion("B40", A3,
        "Viewing your roster. Any member can run project mylab view members. "
        "Delegates and the PI can also view delegates and guests separately. "
        "The PI alone gets two more: view groupemail and view t-t-l.",
        "CCPlainShell",
        {"title": "viewing the group",
         "lines": [
             "$ project mylab view members",
             "Members of mylab:",
             "  pi_username",
             "  labmanager",
             "  jsmith",
         ],
         "startCue": 15, "lineGap": 28,
         "durationSeconds": _dur("Viewing your roster. Any member can run project mylab view members. "
                                  "Delegates and the PI can also view delegates and guests separately. "
                                  "The PI alone gets two more: view groupemail and view t-t-l.")},
        [{"at": 0.2, "event": "project view command appears"},
         {"at": 0.5, "event": "member list appears"}]),

    remotion("B41", A3,
        "New grad student joins the lab. A delegate or PI runs: project mylab add "
        "members jsmith. Then verify: project mylab view members — there they are. No ticket.",
        "CCPlainShell",
        {"title": "adding a member",
         "lines": [
             "$ project mylab add members jsmith",
             "$ project mylab view members",
             "Members of mylab:",
             "  pi_username",
             "  labmanager",
             "  jsmith",
         ],
         "startCue": 15, "lineGap": 26,
         "durationSeconds": _dur("New grad student joins the lab. A delegate or PI runs: project mylab add "
                                  "members jsmith. Then verify: project mylab view members — there they are. No ticket.")},
        [{"at": 0.2, "event": "add command appears"},
         {"at": 0.45, "event": "view command appears"},
         {"at": 0.65, "event": "jsmith appears in list"}]),

    remotion("B42", A3,
        "Three rotation students arriving at once. Comma-separated list, no spaces: "
        "project mylab add members rot1 comma rot2 comma rot3. One command, three additions.",
        "CCPlainShell",
        {"title": "adding multiple members",
         "lines": [
             "$ project mylab add members rot1,rot2,rot3",
         ],
         "startCue": 15, "lineGap": 36,
         "durationSeconds": _dur("Three rotation students arriving at once. Comma-separated list, no spaces: "
                                  "project mylab add members rot1 comma rot2 comma rot3. One command, three additions.")},
        [{"at": 0.35, "event": "multi-add command appears"}]),

    remotion("B43", A3,
        "Student graduates, needs to come off the list. project mylab remove members "
        "bpatel. If bpatel was a delegate, stripping the delegate role only demotes them to "
        "member — you'd run remove members separately to take them out entirely.",
        "CCPlainShell",
        {"title": "removing a member",
         "lines": [
             "$ project mylab remove members bpatel",
             "# note: remove delegates first if they held that role",
             "$ project mylab remove delegates bpatel",
             "$ project mylab remove members bpatel",
         ],
         "startCue": 15, "lineGap": 28,
         "durationSeconds": _dur("Student graduates, needs to come off the list. project mylab remove members "
                                  "bpatel. If bpatel was a delegate, stripping the delegate role only demotes them to "
                                  "member — you'd run remove members separately to take them out entirely.")},
        [{"at": 0.2, "event": "remove members command appears"},
         {"at": 0.56, "event": "delegate-then-member two-step appears"}]),

    remotion("B50", A3,
        "Two diagnostic commands worth knowing. groups username shows every group the "
        "user belongs to, which lets you confirm access without running a project command. "
        "getfacl slash projects slash mylab reads the access control list straight from the "
        "filesystem — the ground truth on who can read and write.",
        "CCPlainShell",
        {"title": "diagnostic commands",
         "lines": [
             "$ groups jsmith",
             "jsmith : jsmith mylab compute_group",
             "$ getfacl /projects/mylab",
             "# file: projects/mylab",
             "user::rwx",
             "group::rwx",
             "other::---",
         ],
         "startCue": 15, "lineGap": 24,
         "durationSeconds": _dur("Two diagnostic commands worth knowing. groups username shows every group the "
                                  "user belongs to, which lets you confirm access without running a project command. "
                                  "getfacl slash projects slash mylab reads the access control list straight from the "
                                  "filesystem — the ground truth on who can read and write.")},
        [{"at": 0.18, "event": "groups command + output appears"},
         {"at": 0.52, "event": "getfacl command + output appears"}]),

    manim("B51", A3,
        "Four habits that prevent headaches. Review membership after every graduation — "
        "students leave, access shouldn't follow them. Use Guest for external collaborators: "
        "read-only, principle of least privilege, protects your data from accidental "
        "modification. Designate at least one Delegate so the PI isn't a bottleneck for "
        "every membership change. Keep the group email pointed at an address someone "
        "actually reads — that's where quota warnings and TTL notifications land.",
        "BestPracticesList",
        "Four best practices appearing one by one: review after graduations; Guest for externals; designate a Delegate; keep group email current.",
        [{"at": 0.12, "event": "'Review membership' appears"},
         {"at": 0.35, "event": "'Use Guest for externals' appears"},
         {"at": 0.58, "event": "'Designate a Delegate' appears"},
         {"at": 0.78, "event": "'Keep group email current' appears"}]),
]

# ─────────────────────────── closing trio ───────────────────────────
CLOSE = [
    remotion("BVDT", "recap",
        "The map. Slash projects persists where slash scratch doesn't. Roles stack: "
        "Guest reads, Member writes, Delegate manages members, PI manages everything. "
        "One setup command gets you onto an IB node. Then: view, add, remove — one "
        "command per task, no ticket required.",
        "ClaudeVerdictArtifact",
        {"title": "Managing /projects",
         "verdict": "no ticket required",
         "lines": [
             "/projects persists — /scratch does not",
             "Roles stack: Guest → Member → Delegate → PI",
             "srun --constraint=ib first, then project commands",
             "view · add · remove — one command per task",
         ],
         "folderLabel": "@NikBearBrown"},
        [{"at": 0.15, "event": "title fades in"},
         {"at": 0.4, "event": "verdict line lands"},
         {"at": 0.65, "event": "bullet list fades in"}],
        lane="bookend"),

    remotion("BHTF", "your turn",
        "Open a terminal on Explorer. Request a compute node with the srun command. "
        "Then run project on your lab's slash projects space — view the membership, "
        "and try adding or removing a user if you have delegate access.",
        "ClaudeComposerAsk",
        {"prompt": "Open a terminal on Explorer.\nRun: srun -p short --constraint=ib --pty bash\nThen: project <your_project> view members\nIf you're a delegate or PI: try adding or removing a user.",
         "folderLabel": "@NikBearBrown"},
        [{"at": 0.3, "event": "prompt text appears in composer"}],
        lane="bookend"),

    remotion("BOUT", "outro",
        "I'm Liam. For Bear. At Nik Bear Brown. Subscribe and I'll see you in the next one.",
        "ClaudeTitleOutro",
        {"title": "Managing /projects on Explorer",
         "handle": "@NikBearBrown",
         "folderLabel": "@NikBearBrown"},
        [{"at": 0.3, "event": "title fades in"},
         {"at": 0.6, "event": "handle fades in"}],
        lane="bookend"),
]

# ─────────────────────────── assemble ───────────────────────────
beats = OPEN + ACT1 + ACT2 + ACT3 + CLOSE

sheet = {
    "metadata": {
        "slug": SLUG,
        "title": TITLE,
        "skill": "lecture",
        "style_preset": "lecture",
        "channel": "claude-liam",
        "voice": "am_onyx",
        "engine": "kokoro",
        "palette": "claude",
        "source": "hpc/Managing-Projects-on-Explorer/train_main.md",
        "fps": FPS,
        "pixel_height": 2160,
    },
    "beats": beats,
}

out = HERE / "beat_sheet.json"
out.write_text(json.dumps(sheet, indent=2, ensure_ascii=False))
print(f"wrote {out}  ({len(beats)} beats)")
