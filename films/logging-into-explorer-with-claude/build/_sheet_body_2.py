
# ───────────────────────────── the closing three ─────────────────────────────
RECAP = ["Explorer starts with your password, which Claude must never hold.",
         "Make a key, install its public half, and keep the private half yours.",
         "Unlock the key once into ssh-agent, and give the cluster a host alias.",
         "Test with BatchMode, then let Claude run read-only commands.",
         "AICR differs: no password, and a key and certificate you download.",
         "On both, Claude never holds your password, passphrase or key."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. Explorer starts with your password, which Claude must never hold. Make a key, install its public "
    "half, and keep the private half yours. Unlock the key once into the ssh agent, and give the cluster a host alias. Test with "
    "BatchMode, then let Claude run read-only commands. AICR differs: no password, and a key and certificate you download. And on "
    "both, Claude never holds your password, passphrase or key.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land in narration order"}],
    lane="bookend", lead_silence_s=0.5,
    qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ('Log into the Explorer cluster with `ssh explorer` and run read-only commands only. '
             'Run: whoami, hostname, pwd, squeue -u $USER. '
             'Tell me the user name, the host, and which folder I land in. '
             'Do not submit, cancel or change anything, and do not run computation on the login node.')
YT_SPOKEN = ("Log into the Explorer cluster with ssh explorer and run read-only commands only. "
             "Run: whoami, hostname, pwd, and s queue for my own user. "
             "Tell me the user name, the host, and which folder I land in. "
             "Do not submit, cancel or change anything, and do not run computation on the login node.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_SPOKEN + " Then check two things yourself. Did Claude run only read-only commands? "
    "And did it ever ask for, or print, your passphrase or your key?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Log Into Explorer With Claude", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did Claude run only read-only commands, nothing that submits or changes?",
                "Check: did Claude ever ask for, or print, your passphrase or key? It should not."],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": "Logging into Explorer, H P C, with Claude. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Logging into Explorer, H P C, with Claude. How to make a key, unlock it once, "
                           "and let Claude Code log into the Explorer cluster for you, without ever handing it a password.",
         "estimated_duration_s": 14.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · EXPLORER", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German (Hallo)",
    "audience": "A researcher with an Explorer account who wants Claude Code to run commands on the cluster; assumes no other film or book",
    "source_doc": "hpc-aicr/Logging-into-Explorer-with-Claude/SESSION.md (the real key setup and the real Claude Code login, 2026-10-11), hpc-aicr/skills/hpc/HPC.md section 10",
    "playlist": "Northeastern HPC and AICR",
    "series_title": "Research Computing on Explorer and AICR",
    "lecture_opening_description": "Make a key, unlock it once, and let Claude log in",
    "lecture_opening_title_lines": ["Logging into Explorer (HPC)", "with Claude"],
    "tags": ["Explorer", "Northeastern University", "Research Computing", "HPC", "Claude Code", "SSH", "ssh-agent", "BatchMode",
             "SSH key", "Slurm", "Nik Bear Brown"]},
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
