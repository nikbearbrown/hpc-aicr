A1, A2, A3, A4, A5 = ("I · Why An Agent Needs Rules", "II · Walking Through HPC.md", "III · What AICR.md Changes",
                      "IV · Rules Born From Real Mistakes", "V · Using The Files")

# ───────────────────────────── the opening pair ─────────────────────────────
OPEN = [
 remotion("BIDEA", "the idea",
    "Hallo. This is Liam, in for Bear. First, a correction. To let an agent work on a cluster, you do not just say, run my "
    "job. The cluster is shared, and the agent is fast and literal. You give it two short rule files first, and you point it "
    "at them.",
    "BrutalistHesitantWriter",
    {"text": "To use Claude on a cluster,\nI just say: run my job", "triggerWords": "I just say: run my job",
     "replacementWords": "give it rules first", "fontSize": 66, "charMs": 62, "hesitateBetween": 6,
     "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'To use Claude on a cluster, I just say: run my job'"},
     {"at": 0.35, "event": "backspaces 'I just say: run my job' -> 'give it rules first'"}],
    lane="bookend", lead_silence_s=0.8,
    motion_claim="The writer types the newcomer's framing (I just say: run my job) and corrects it to the real one (give it rules first).",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Five terms. A rule file: a plain text file the agent reads before it acts. A hard never: a rule with no exceptions. A "
    "login node: the shared computer you land on when you connect. A Slurm job: your request for a compute node, written as "
    "a script. And fairshare: the priority you lose when you ask for more than you use.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "Rule file", "meaning": "a text file the agent reads before it acts"},
               {"term": "Hard never", "meaning": "a rule with no exceptions"},
               {"term": "Login node", "meaning": "the shared computer you land on when you connect"},
               {"term": "Slurm job", "meaning": "your request for a compute node, as a script"},
               {"term": "Fairshare", "meaning": "the priority you lose by asking for more than you use"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "'Rule file' lands"}, {"at": 0.3, "event": "'Hard never'"}, {"at": 0.5, "event": "'Login node'"},
     {"at": 0.7, "event": "'Slurm job'"}, {"at": 0.87, "event": "'Fairshare'"}],
    gate="CARD", lane="bookend",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: five prerequisites, one line each."}),
]

B = []


def add(b):
    B.append(b)
    return b


def shell(bid, act, narration, title, lines, cue_phrases, show, ring_lines=None, ring_phrases=None, fs=None, margin=None,
          motion_claim="The real file text prints line by line, each as it is spoken."):
    """A CCPlainShell beat. cue_phrases: one phrase (or None = already on screen) per line."""
    cues = cues_for(bid, cue_phrases, narration, est(narration))
    cues = clear_midpoint(bid, cues)
    props = {"title": title, "lines": lines, "startCue": 20, "lineGap": 30, "lineCues": cues}
    if fs:
        props["fontSize"] = fs
    if margin:
        props["windowMargin"] = margin
    if ring_lines is not None:
        props["rings"] = [{"line": ln, "cue": clear_midpoint(bid, [cues_for(bid, [ph], narration, est(narration))[0] + 12])[0]}
                          for ln, ph in zip(ring_lines, ring_phrases)]
    return add(remotion(bid, act, narration, "CCPlainShell", props, show, motion_claim=motion_claim))


# ═════════════════════════════ ACT I · Why An Agent Needs Rules ═════════════════════════════
add(manim("B10", A1,
    "An agent is fast, literal, and never tired. That is the good news. On a shared cluster it is also the risk. It will do "
    "exactly what you asked, as many times as you asked, and it will not feel the cost to anyone else.",
    "B10_FastAndLiteral",
    "On the left a Claude logo chip (logo_chip('claude')) with a stopwatch and a stack of many small 'job' boxes flying out fast; on the right a shared rack grid with several small dark racks that each get a different terracotta dot (other people's work); the boxes pile into one rack and its dots crowd out the others.",
    [{"at": 0.2, "event": "the agent chip, fast, many job boxes"}, {"at": 0.55, "event": "the shared racks appear"}, {"at": 0.85, "event": "one rack fills; the others dim"}]))
add(manim("B11", A1,
    "Most trouble on a cluster is not hard computer science. It is work on the wrong machine. It is a request far bigger than "
    "the job. And it is a check that passes when it should fail. These are quiet failures: nothing crashes, and you find out later.",
    "B11_ThreeQuietFailures",
    "Three plain cards fan out, each with a short mono label and one small drawing: 'login node' (a door rack with a running job), '8 h for 25 min' (a long bar with a short filled part), 'exit 0, no CUDA' (a check mark over a rack whose GPU slot is empty); a 'no error' tag lands on all three.",
    [{"at": 0.2, "event": "wrong machine: login node"}, {"at": 0.45, "event": "wrong size: 8 h for 25 min"}, {"at": 0.7, "event": "passing check: exit 0, no CUDA"}, {"at": 0.9, "event": "'no error' on all three"}]))
add(manim("B12", A1,
    "So there are two files. H P C dot M D holds the rules for any shared cluster, written for Northeastern's Explorer. AICR "
    "dot M D builds on it and adds what is different or stricter on the AICR GPU cluster. Read the first, then the second.",
    "B12_TwoFiles",
    "Two document pages stacked: the lower labelled 'HPC.md' with the subtitle 'any shared cluster (Explorer)', the upper labelled 'AICR.md' with 'stricter on AICR'; an arrow 'builds on' from the upper to the lower; a number-free reading order shown as 'first' on HPC.md and 'then' on AICR.md.",
    [{"at": 0.25, "event": "HPC.md page: any shared cluster"}, {"at": 0.6, "event": "AICR.md page lands on it: builds on"}, {"at": 0.88, "event": "first / then labels"}]))
shell("B13", A1,
    "You do not paste either file into your instructions. You put one line in your Claude dot M D or agents dot M D, and the "
    "agent reads the files when the work is cluster work. Here are the two lines, copied from the files themselves.",
    "The one line, from HPC.md and from AICR.md",
    [fl("HPC", "> When a task involves a research computing cluster", 108),
     fl("AICR", "> When a task involves the AICR cluster", 108)],
    ["Here are the two lines", "Here are the two lines"],
    [{"at": 0.4, "event": "the HPC.md line"}, {"at": 0.75, "event": "the AICR.md line"}],
    ring_lines=[0, 1], ring_phrases=["Claude dot M D", "agents dot M D"], fs=30, margin=50)

# ═════════════════════════════ ACT II · Walking Through HPC.md ═════════════════════════════
shell("B20", A2,
    "Open the file H P C dot M D and the first thing you see is not a rule. It is a short summary: what it is, why it exists, what was "
    "found, and what is not verified. Then a line that says everything below is for the agent. Then fourteen numbered sections, zero to thirteen, and an "
    "honest appendix of conflicts.",
    "II · Walking Through HPC.md  ·  the headings, from the file",
    [fl("HPC", "# HPC.md:", 80), fl("HPC", "# Agent rules", 80), fl("HPC", "## 0. Prime directive", 80),
     fl("HPC", "## 1. Hard NEVERs", 80), fl("HPC", "## 2. Before the first command", 80),
     fl("HPC", "## 6. GPUs", 80), fl("HPC", "## 9. Reproducibility", 80),
     fl("HPC", "## 12. Slurm scripting traps", 80), fl("HPC", "# Appendix A", 80)],
    [None, "everything below is for the agent", "fourteen numbered sections", "fourteen numbered sections", "fourteen numbered sections", "fourteen numbered sections", "fourteen numbered sections", "fourteen numbered sections", "an honest appendix"],
    [{"at": 0.05, "event": "the title"}, {"at": 0.4, "event": "the agent line, then sections"}, {"at": 0.9, "event": "the appendix of conflicts"}],
    ring_lines=[1, 8], ring_phrases=["everything below is for the agent", "an honest appendix"], fs=34)
add(manim("B21", A2,
    "Section zero is the prime directive. The agent does the pipeline work: inspect, measure, size, check, keep records. The "
    "researcher keeps the judgment: what to spend, who gets access, and anything that cannot be undone. Look before you act. "
    "Measure before you change. Ask before you spend, delete, or share.",
    "B21_PrimeDirective",
    "A split drawing: left column 'agent' (a Claude logo chip) with four small verbs inspect / measure / size / record on ticks; right column 'you' (Professor Bear portrait, 1x1) with 'spend', 'access', 'cannot undo' as three chips; a bold horizontal rule between them; three phrases 'look first', 'measure first', 'ask first' land along the rule.",
    [{"at": 0.2, "event": "agent column"}, {"at": 0.45, "event": "you column"}, {"at": 0.75, "event": "look, measure, ask along the rule"}]))
add(manim("B22", A2,
    "Section one is the list the agent checks before every command. Never run computation on a login node. Never ask for, read, "
    "or print a password or a key. Never delete without listing what will go and getting a yes. Never submit a job until you "
    "have confirmed what it asks for. Never cancel with S cancel dash u. And never invent a flag, a module, or a limit.",
    "B22_HardNevers",
    "A drawn table builds row by row, six rows each starting with a bold 'never' chip and a short mono item: 'compute on a login node', 'password or key', 'delete without a list', 'submit unconfirmed', 'scancel -u', 'invent a flag'; each row gets a small cross mark as it lands.",
    [{"at": 0.15, "event": "login node row"}, {"at": 0.3, "event": "password row"}, {"at": 0.45, "event": "delete row"}, {"at": 0.6, "event": "submit row"}, {"at": 0.75, "event": "scancel row"}, {"at": 0.9, "event": "invent row"}], sparse=True))
shell("B23", A2,
    "Notice that every never comes with a because. A rule the agent understands is a rule it can apply to a case the file never "
    "listed. And some rules are labelled house rule, because they are our judgment, not the cluster's policy.",
    "HPC.md · three rows from the hard-never table",
    [fl("HPC", "| `sudo`, `apt install`", 118), fl("HPC", "| Poll the scheduler in a tight loop", 118, focus="(house rule)"), fl("HPC", "| Invent a flag, module name", 118)],
    [None, "house rule", "Notice that every never comes with a because"],
    [{"at": 0.05, "event": "sudo row"}, {"at": 0.5, "event": "poll row: house rule"}, {"at": 0.85, "event": "invent a flag row"}],
    ring_lines=[1], ring_phrases=["house rule"], fs=28, margin=50)
shell("B24", A2,
    "Section two is before the first command. If a read-only command can answer a question, the agent runs it instead of "
    "asking you. Who am I, where am I, which groups, what is free. It asks only what only you can answer: your access, what it "
    "may submit, whether the data is restricted, and what you are trying to do.",
    "HPC.md · Section 2, from the file",
    [fl("HPC", "**Read or measure first;", 112), "…", fl("HPC", "**Must ask**", 112),
     fl("HPC", "1. **Access:**", 112), fl("HPC", "3. **Data:**", 112)],
    [None, "If a read-only command", "It asks only what only you can answer", "your access", "restricted"],
    [{"at": 0.05, "event": "read or measure first"}, {"at": 0.5, "event": "must ask"}, {"at": 0.85, "event": "access and data"}],
    ring_lines=[0, 2], ring_phrases=["If a read-only command", "It asks only what only you can answer"], fs=28, margin=50)
add(manim("B25", A2,
    "Section four stops the agent asking for more than it needs. Is parallel even the answer? In Research Computing's own "
    "benchmark, one core took two hundred fifty seconds. Eight cores took twenty-nine. Twelve cores took thirty-three, slower "
    "than eight. Never promise that N cores is N times faster.",
    "B25_TwelveSlowerThanEight",
    "A bar chart with six bars labelled by cores and real seconds: 1 core 250.7 s; 2 cores 116.8; 4 cores 58.1; 8 cores 29.4; 12 cores 33.4 (this bar ringed in terracotta and a small 'slower than 8' tag); 16 cores 25.2; the 20-core bar 20.2 s lands last. Bars grow on the spoken numbers.",
    [{"at": 0.2, "event": "1 core: 250.7 s"}, {"at": 0.5, "event": "8 cores: 29.4 s"}, {"at": 0.7, "event": "12 cores: 33.4 s, ringed, slower than 8"}, {"at": 0.9, "event": "never promise N times faster"}], sparse=False))
shell("B26", A2,
    "Section five: every script states its numbers. Partition, time, memory, cores, a name, and a log file. Time is the "
    "expected runtime plus about twenty percent, never the maximum just to be safe. And memory is computer memory, not GPU memory.",
    "HPC.md · Section 5, from the file",
    [fl("HPC", "- Always set `--partition`", 110), fl("HPC", "- **`--time` = expected runtime", 110), fl("HPC", "- **`--mem` is CPU RAM", 110)],
    [None, "Time is the expected runtime", "memory is computer memory"],
    [{"at": 0.05, "event": "always set"}, {"at": 0.45, "event": "time = runtime + 20%"}, {"at": 0.8, "event": "mem is CPU RAM"}],
    ring_lines=[1, 2], ring_phrases=["plus about twenty percent", "not GPU memory"], fs=28, margin=50)
shell("B27", A2,
    "Section six is GPUs. Never trust the allocation. A job that worked may have run on the processor with no error. So every "
    "GPU script proves the GPU is there before the expensive part: the device name, the memory, and a number that travels to the "
    "GPU and back.",
    "HPC.md · Section 6, from the file",
    [fl("HPC", "**Never trust the allocation;", 116), fl("HPC", "**A GPU is the right tool only", 116)],
    [None, "Never trust the allocation"],
    [{"at": 0.1, "event": "never trust the allocation"}, {"at": 0.6, "event": "when a GPU is the right tool"}],
    ring_lines=[0], ring_phrases=["proves the GPU is there"], fs=30, margin=50)
add(manim("B28", A2,
    "Section seven is where files live. Code and environments in home. Temporary job data in scratch, which is wiped on the "
    "first Tuesday of every month. Anything you keep in projects. And the agent never keeps the only copy of anything in scratch.",
    "B28_WhereFilesLive",
    "Three folder boxes: 'home' (code, environments), 'scratch' (a calendar page 'first Tuesday' with a sweep that empties it), 'projects' (long-term, a check); a kraft box labelled 'only copy' is carried out of scratch and set down in projects just before the sweep.",
    [{"at": 0.2, "event": "home: code, environments"}, {"at": 0.45, "event": "scratch: wiped the first Tuesday"}, {"at": 0.7, "event": "projects: kept"}, {"at": 0.9, "event": "the only copy moves out before the sweep"}]))
add(manim("B29", A2,
    "Section eight is software, in order. First a module. Then conda. Then a container built on your own machine. Then a source "
    "build. And a tool like Spack only last, because each step down costs more to keep. Before installing anything, the agent "
    "checks whether a module already exists.",
    "B29_InstallLadder",
    "A five-rung ladder drawn top to bottom: 'module', 'conda', 'container (built at home)', 'source build', 'Spack / EasyBuild (last)'; a cost bar grows wider with each rung; a magnifier 'module avail' sweeps the top rung first.",
    [{"at": 0.2, "event": "module"}, {"at": 0.4, "event": "conda"}, {"at": 0.55, "event": "container"}, {"at": 0.7, "event": "source build"}, {"at": 0.85, "event": "Spack last; the cost bar widens"}]))
shell("B30", A2,
    "Section nine is the record every job leaves behind. The job and node. When it started. The git commit it ran from. The "
    "exact command, the parameters, the seeds, the inputs. The software, and the hardware it really used. Twelve items, so a "
    "stranger can rerun it.",
    "HPC.md · Section 9, the minimum record",
    [fl("HPC", "  1. job ID", 96), fl("HPC", "  3. git commit hash", 96), fl("HPC", "  6. every random seed", 96),
     fl("HPC", "  10. hardware actually used", 96), fl("HPC", "  12. exit status", 96)],
    [None, "The git commit it ran from", "the seeds", "the hardware it really used", "Twelve items"],
    [{"at": 0.05, "event": "item 1"}, {"at": 0.4, "event": "item 3, the commit"}, {"at": 0.6, "event": "seeds"}, {"at": 0.85, "event": "item 12, so a stranger can rerun"}],
    ring_lines=[1, 4], ring_phrases=["The git commit it ran from", "Twelve items"], fs=32, margin=50)
shell("B31", A2,
    "Section ten is about being an agent on the cluster. The researcher creates and unlocks the key, never the agent. If a "
    "command prompts, hangs, or says permission denied, the agent stops and reports the exact error. It does not retry in a loop, "
    "and it never asks for a password.",
    "HPC.md · Section 10, from the file",
    [fl("HPC", "**If a command prompts, hangs", 118), fl("HPC", "**Getting in (human-only steps first).**", 118)],
    [None, "The researcher creates and unlocks the key"],
    [{"at": 0.1, "event": "stop and report the exact error"}, {"at": 0.55, "event": "human-only steps"}],
    ring_lines=[0], ring_phrases=["stops and reports the exact error"], fs=28, margin=50)
add(manim("B32", A2,
    "Section twelve is a list of things the training slides get wrong. A comment after a line continuation, which breaks the "
    "command. A partition called compute, which does not exist. A sample script with no time and no memory. The agent is told "
    "not to copy them.",
    "B32_DoNotCopy",
    "Three slide cards, each stamped with a terracotta 'do not copy' tag: 'python train.py \\  # CHANGE' (the line cut at the backslash), '--partition=compute' (a partition rack that is not there, dotted), 'sbatch with no --time or --mem' (empty slots); a Claude logo chip nods past them without taking any.",
    [{"at": 0.2, "event": "backslash comment card"}, {"at": 0.45, "event": "partition=compute card (nothing there)"}, {"at": 0.7, "event": "no time or memory card"}, {"at": 0.9, "event": "none copied"}]))
add(manim("B33", A2,
    "And the appendix is the honest part. Where the sources disagree, the file says so and picks the safe reading. The scratch "
    "quota: fifty terabytes in the slides, twenty on the policy page. So the agent is told never to quote a number. Rules marked "
    "house rule or inferred are our judgment, not policy.",
    "B33_HonestAppendix",
    "Two source pages side by side, one with '50 TB' and one with '20 TB' on the same line 'scratch quota'; a not-equal sign; a third card 'the file: never quote a number'; then two small stamps 'house rule' and 'inferred' land beside a rule line.",
    [{"at": 0.2, "event": "50 TB on one page"}, {"at": 0.4, "event": "20 TB on the other"}, {"at": 0.65, "event": "the file picks the safe reading"}, {"at": 0.88, "event": "house rule and inferred stamps"}]))
