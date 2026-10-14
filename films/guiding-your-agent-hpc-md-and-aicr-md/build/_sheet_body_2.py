
# ═════════════════════════════ ACT III · What AICR.md Changes ═════════════════════════════
add(manim("B40", A3,
    "Now AICR dot M D. It builds on the first file, and where the two differ, it wins on AICR. Explorer's hosts, partitions, "
    "storage rules and module setup do not carry over. The first rule of the second file: assume AICR is not Explorer.",
    "B40_AssumeNotExplorer",
    "The two stacked pages from before, now with the AICR.md page on top lit; four small Explorer items (a host chip, a partition chip, a storage chip, a module chip) try to slide from the HPC.md page onto the AICR rack and bounce off one by one; a short line 'AICR is not Explorer' lands.",
    [{"at": 0.2, "event": "AICR.md on top: it wins"}, {"at": 0.5, "event": "Explorer's host, partition, storage, module bounce off"}, {"at": 0.88, "event": "assume AICR is not Explorer"}]))
add(manim("B41", A3,
    "AICR differs in ways that bite. Your user name is built differently. There is no password, only a key and a certificate. "
    "The partition decides which GPU you get. Idle GPUs are cancelled automatically. And scratch is purged after thirty days, "
    "with no off-site backup.",
    "B41_AICRDiffers",
    "A drawn two-column table builds row by row: 'user name' -> 'dot becomes underscore, _neu added'; 'login' -> 'key + certificate, no password'; 'GPU' -> 'the partition picks it'; 'idle GPU' -> 'cancelled automatically'; 'scratch' -> 'purged after 30 days, no off-site backup'.",
    [{"at": 0.15, "event": "user name row"}, {"at": 0.35, "event": "no password row"}, {"at": 0.55, "event": "partition picks the GPU row"}, {"at": 0.72, "event": "idle GPU row"}, {"at": 0.9, "event": "scratch row"}], sparse=True))
shell("B42", A3,
    "AICR's own nevers are specific. Never run S S H add dash capital D, because it empties every key. Never source activate in "
    "a batch script, because a real job died on it. And never copy the workshop's GPU check, because it exits zero even when "
    "the GPU is missing.",
    "AICR.md · three of its hard nevers, from the file",
    [fl("AICR", "| Run `ssh-add -D`", 132, focus="It empties"), fl("AICR", "| `source activate` or `conda activate`", 132, focus="One real job died"),
     fl("AICR", "| Copy `01_gpu_verify.py`", 132, focus="exits with status 0")],
    [None, "Never source activate", "never copy the workshop"],
    [{"at": 0.05, "event": "ssh-add -D"}, {"at": 0.45, "event": "source activate"}, {"at": 0.8, "event": "01_gpu_verify.py"}],
    ring_lines=[0, 1, 2], ring_phrases=["empties every key", "a real job died on it", "exits zero"], fs=28, margin=50)
shell("B43", A3,
    "Section five is a template built from flags that real completed jobs used. Every setting is stated. The environment is "
    "added to the path, not activated. And the script fails itself, on purpose, if the GPU is not visible.",
    "AICR.md · the template, three lines of it",
    [fl("AICR", "#SBATCH --partition=rtx-batch", 100), fl("AICR", "export PATH=$HOME/.conda/envs", 100),
     fl("AICR", 'python -c "import torch,sys; sys.exit', 100)],
    [None, "added to the path", "fails itself, on purpose"],
    [{"at": 0.1, "event": "every setting stated"}, {"at": 0.5, "event": "PATH prepend, not activate"}, {"at": 0.85, "event": "the hard-fail CUDA check"}],
    ring_lines=[1, 2], ring_phrases=["added to the path", "fails itself, on purpose"], fs=30, margin=50)
add(manim("B44", A3,
    "After every batch job the agent runs jobstats, a command that exists only on AICR. Its real example: a job that asked for "
    "eight hours and ran fifty-five minutes, with the GPU eighty percent busy. The targets are written down: over seventy "
    "percent GPU use is acceptable, and under fifty is a problem.",
    "B44_JobstatsTargets",
    "Four horizontal bars drawn like jobstats: CPU utilisation 13%, CPU memory 25%, GPU utilisation 80% (the one filled terracotta), GPU memory 17%; a time bar '8 h asked, 55 min ran'; two tick marks on the GPU bar at 50 and 70 labelled 'problem' and 'acceptable'.",
    [{"at": 0.2, "event": "the time bar: 8 h asked, 55 min ran"}, {"at": 0.5, "event": "GPU utilisation 80%"}, {"at": 0.85, "event": "the 70 and 50 marks"}], sparse=False))
add(manim("B45", A3,
    "Section eleven is lessons from real AICR runs, and they are all quiet failures. A checkpoint that loaded without error and "
    "left random weights. An input clip so quiet it produced silence. A cached file served under the same path after it was "
    "replaced. Each became a rule: prove the weights loaded, gate every input with a number, give a replaced file a new name.",
    "B45_QuietLessons",
    "Three cards each with a small drawing and a rule chip: a model box with a 'loaded, no error' tick but random dots inside -> 'prove the weights loaded'; a flat audio line with peak '4 of 32767' -> 'gate every input with a number'; two files with the same path, the old one served from a cache shelf -> 'give it a new name'.",
    [{"at": 0.2, "event": "weights loaded with no error"}, {"at": 0.45, "event": "the silent clip"}, {"at": 0.7, "event": "the cached file"}, {"at": 0.9, "event": "three rules"}]))
shell("B46", A3,
    "And before any GPU job, the agent asks only what only you can answer. Your user name and account. Whether any data is "
    "restricted. Whether it may submit for you. And what success looks like.",
    "AICR.md · Section 12, the questions, from the file",
    [fl("AICR", "**Must ask (only the researcher can answer):**", 100), fl("AICR", "1. What is your **AICR username**", 112),
     fl("AICR", "2. **Is any of the data non-anonymised", 112), fl("AICR", "4. What counts as success", 112)],
    [None, "Your user name and account", "restricted", "what success looks like"],
    [{"at": 0.05, "event": "must ask"}, {"at": 0.35, "event": "username and account"}, {"at": 0.6, "event": "restricted data"}, {"at": 0.85, "event": "what success looks like"}],
    ring_lines=[2], ring_phrases=["restricted"], fs=28, margin=50)

# ═════════════════════════════ ACT IV · Rules Born From Real Mistakes ═════════════════════════════
shell("B50", A4,
    "Rules also come from mistakes. While making the film about rendering on Explorer, the agent listed every folder under "
    "projects. That showed other people's names. Then it ran a disk usage command over a shared folder, and it hung. Neither was "
    "forbidden by the file. Now both are.",
    "Rules Born From Real Mistakes, the real record, then the rule",
    ["(Redacted: a first command also listed every directory under /projects.",
     "That showed other people's names, so it is not kept.)",
     "Command did not complete within its 120s timeout and was moved to the background",
     "NEW RULE in HPC.md, Section 1:",
     fl("HPC", "| List `/projects`", 96)],
    [None, "That showed other people's names", "it hung", "Now both are", "Now both are"],
    [{"at": 0.05, "event": "the listing, redacted"}, {"at": 0.45, "event": "the hung disk count"}, {"at": 0.85, "event": "the new rule, copied from HPC.md"}],
    ring_lines=[2, 4], ring_phrases=["it hung", "Now both are"], fs=28, margin=100)
shell("B51", A4,
    "Another. A job script began with module purge. That removed the module that sets the cluster's proxy, so every download "
    "timed out. A one line test showed the network was fine. Now the file says: module purge can remove your network, so load "
    "that module again.",
    "The real test, then the rule that came from it",
    ["before purge: [<the cluster proxy>]", "after purge: []", "after load: []",
     "NEW RULE in HPC.md, Section 8:",
     fl("HPC", "- **`module purge` can also remove your network.**", 110)],
    [None, "removed the module", "removed the module", "Now the file says", "Now the file says"],
    [{"at": 0.05, "event": "proxy set before the purge"}, {"at": 0.4, "event": "gone after the purge, and after loading tools"}, {"at": 0.85, "event": "the new rule"}],
    ring_lines=[1, 4], ring_phrases=["removed the module", "module purge can remove your network"], fs=28, margin=50)
shell("B52", A4,
    "And a third. The scripts assumed scratch belonged to the user. On this account it belonged to root, and refused every "
    "write. The agent had checked with a read first, which is exactly what the file asks. Now the file says why: test before "
    "you write.",
    "The real check, then the rule that came from it",
    ["root:root 755 2023-01-27 16:20:13.110253069 -0500",
     "mkdir: cannot create directory ‘/scratch/<username>/.probe’: Permission denied",
     "NEW RULE in HPC.md, Section 7:",
     fl("HPC", "- **Test before you write to scratch.**", 110)],
    [None, "refused every write", "Now the file says why", "test before you write"],
    [{"at": 0.05, "event": "scratch belongs to root"}, {"at": 0.45, "event": "mkdir refused"}, {"at": 0.85, "event": "the new rule"}],
    ring_lines=[0, 3], ring_phrases=["belonged to root", "test before you write"], fs=28, margin=50)

# ═════════════════════════════ ACT V · Using The Files ═════════════════════════════
add(manim("B59", A5,
    "Where to find them. Both files are free on GitHub, in the hpc dash aicr repository, inside the skills folder. "
    "H P C dot M D is in the hpc folder, and AICR dot M D is in the aicr folder. The link is in the description.",
    "B59_WhereToFindThem",
    "The repository address github.com/nikbearbrown/hpc-aicr appears in mono; below it a skills folder splits into two folders, hpc and aicr, each holding one document page labelled HPC.md and AICR.md.",
    [{"at": 0.2, "event": "the repository address"}, {"at": 0.55, "event": "skills opens into hpc and aicr"}, {"at": 0.85, "event": "the two files, one in each"}]))
add(manim("B60", A5,
    "To use them: put both files where your agent can read them. Add the one line to your Claude dot M D or agents dot M D. And "
    "at the start of cluster work, ask the agent to say back which rules apply, before it runs anything.",
    "B60_ThreeSteps",
    "Three steps land left to right on a line: a folder with two document pages ('put the files where the agent can read them'), a small instructions page with one highlighted line ('add the one line'), and a speech bubble from a Claude logo chip ('say back the rules that apply') that appears before any command box moves.",
    [{"at": 0.2, "event": "two files in a folder"}, {"at": 0.5, "event": "one line in the instructions"}, {"at": 0.85, "event": "the agent says the rules back first"}]))
add(manim("B61", A5,
    "The files do not replace judgment. Nothing in any policy page says whether automated agents are allowed on Explorer or "
    "AICR, so the files say to ask Research Computing once. And every claim is labelled by how we know it: from the sources, "
    "from a real run, or our own judgment.",
    "B61_WhatRulesCannotDo",
    "A small gate drawn with a Professor Bear portrait (1x1) standing beside it holding the key; a Claude logo chip waits at the gate; a note 'ask Research Computing once' lands on the gate; below, three label stamps in a row: 'from the sources', 'from a real run', 'our own judgment'.",
    [{"at": 0.2, "event": "you at the gate, the agent waits"}, {"at": 0.5, "event": "ask Research Computing once"}, {"at": 0.85, "event": "three label stamps"}]))

# ───────────────────────────── the closing three ─────────────────────────────
RECAP = ["An agent is fast and literal, so a shared cluster needs written rules.",
         "HPC.md holds the general rules: never compute on a login node, ask before you spend, verify the GPU.",
         "AICR.md adds what is stricter: no idle GPUs, no source activate, scratch is purged.",
         "Every rule comes with a because.",
         "Real mistakes become new rules.",
         "One line in your instructions points the agent at both files."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. An agent is fast and literal, so a shared cluster needs written rules. H P C dot M D holds the "
    "general rules: never compute on a login node, ask before you spend, verify the GPU. AICR dot M D adds what is stricter: no "
    "idle GPUs, no source activate, and scratch is purged. Every rule comes with a because. Real mistakes become new rules. And "
    "one line in your instructions points the agent at both files.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land in narration order"}],
    lane="bookend", lead_silence_s=0.5,
    qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("Read the files HPC.md and AICR.md completely. Do not run anything on any cluster. "
             "Then tell me the five hard nevers that matter most for my task, which questions you would ask me before your first "
             "command, and anything in the files that you could not confirm. My task: <describe your job in one sentence>.")
YT_SPOKEN = ("Read the files H P C dot M D and AICR dot M D completely. Do not run anything on any cluster. "
             "Then tell me the five hard nevers that matter most for my task, which questions you would ask me before your first "
             "command, and anything in the files that you could not confirm. My task, then describe your job in one sentence.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_SPOKEN + " Then check two things yourself. Did Claude run nothing on a cluster? "
    "And did it say what it could not confirm?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Read The Rules First", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did Claude run nothing on a cluster? It should only read the two files.",
                "Check: did it say what it could not confirm? A good answer names the unverified parts."],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": "Guiding Your Agent, H P C dot M D and AICR dot M D. At Nik Bear Brown.", "estimated_duration_s": 5.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Guiding Your Agent, H P C dot M D and AICR dot M D. Why an agent on a "
                           "shared cluster needs written rules, and a walk through the two rule files that give them.",
         "estimated_duration_s": 14.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · AGENT RULES", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German (Hallo)",
    "audience": "A researcher who wants Claude Code (or another agent) to work on a shared research cluster and needs to know what rules to give it; assumes no other film or book",
    "source_doc": "hpc-aicr/skills/hpc/HPC.md and hpc-aicr/skills/aicr/AICR.md (the two files), STORY.md, and the real Explorer session record in the film 'Making a Lecture Film on Explorer' SESSION.md",
    "playlist": "Northeastern HPC and AICR",
    "series_title": "Research Computing on Explorer and AICR",
    "lecture_opening_description": "Rule files that keep an agent safe on a shared cluster",
    "lecture_opening_title_lines": ["Guiding Your Agent:", "HPC.md and AICR.md"],
    "tags": ["HPC.md", "AICR.md", "Claude Code", "AI agents", "CLAUDE.md", "AGENTS.md", "Slurm", "Explorer", "AICR", "Northeastern University",
             "Research Computing", "HPC", "Nik Bear Brown"]},
    "beats": BEATS}

old = {}
p = HERE / "beat_sheet.json"
if p.exists():
    for ob in json.load(open(p))["beats"]:
        old[ob["beat_id"]] = ob
for b in BEATS:
    ob = old.get(b["beat_id"])
    if ob and ob.get("narration_text") == b["narration_text"]:
        for k in ("actual_duration_s", "audio_file"):
            if k in ob:
                b[k] = ob[k]
    dur = b.get("actual_duration_s")
    props = (b["shot"].get("remotion") or {}).get("props")
    if dur and props is not None:
        pat = b["shot"]["remotion"]["pattern"]
        if pat in ("ClaudeDefinitions", "BrowserCapture", "LibraryIconRow", "CCPlainShell", "ClaudeCodeBeat"):
            props["durationSeconds"] = dur

p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
n_est = sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in BEATS)
print(len(BEATS), "beats; est", round(n_est), "s", "(measured)" if all(b.get("actual_duration_s") for b in BEATS) else "(estimate)")
