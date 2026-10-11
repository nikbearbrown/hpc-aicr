#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-logging-into-aicr-with-claude.

LECTURE (Bear, 2026-10-02): the WHOLE source as one act-structured film, primarily visual, best visual per beat from
the full playset, a tool shown as itself. Skill doctrine: brutalist.art/skills/make/lecture/SKILL.md.

Source:   ../source/README.md
Evidence: ../source/SESSION.md (three real runs, 2026-10-11): every terminal line below is
          copied from it verbatim (the one allowed change: a very long command is shown on two lines with a `\\`).
Primary:  the AICR documentation 'SSH' page (local copy not included), a private project setup note (not included) section 2.

Spine: BOPEN -> BIDEA -> BDEFS -> five acts -> BVDT -> BHTF -> BOUT.
Two passes: pass 1 (no _qc/asr.json) estimates cues; after Kokoro + faster-whisper, pass 2 places every terminal line
and code line on the word Liam says (word times in _qc/asr.json).
"""
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Logging into AICR with Claude"
CAP = "lecture-logging-into-aicr-with-claude"      # runtime/remotion/public/<CAP>/ holds the capture
ART = HERE.parents[2] / "brutalist.art"
FPS = 30

ASR = {}
_ap = HERE / "_qc/asr.json"
if _ap.exists():
    ASR = json.loads(_ap.read_text())


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def word_t(bid, phrase, nth=0, default=None):
    """Seconds at which `phrase` starts in beat `bid`'s spoken audio (faster-whisper word times), or `default`.
    `phrase` may hold alternatives separated by '|' (the recogniser writes 'user name' as 'username', '600' for 'six hundred')."""
    words = ASR.get(bid, {}).get("words")
    if not words:
        return default
    seq = [_norm(w["w"]) for w in words]
    for alt in phrase.split("|"):
        toks = [_norm(x) for x in alt.split() if _norm(x)]
        hits = [i for i in range(len(seq) - len(toks) + 1) if seq[i:i + len(toks)] == toks]
        if len(hits) > nth:
            return words[hits[nth]]["t"]
    return default


def fr(seconds):
    return max(1, int(round(seconds * FPS)))


def cues_for(bid, phrases, narration, est_dur):
    """Frame cues, one per phrase: measured word time when known, else the phrase's character share of the estimate.
    Cues never run backwards (a line cannot land before the line above it)."""
    out, last = [], 0
    for ph in phrases:
        if ph is None:
            out.append(0)                      # on screen from frame 0
            continue
        if isinstance(ph, (int, float)):
            c = max(1, fr(ph), last); out.append(c); last = c
            continue
        t = word_t(bid, ph)
        if t is None:
            print(f"  [cue-fallback] {bid}: '{ph}' not in the recognised words; using the character share")
            alt = ph.split("|")[0]
            i = narration.find(alt)
            t = (est_dur * i / max(1, len(narration))) if i >= 0 else 0.5
        c = max(1, fr(t - 0.15), last)
        out.append(c)
        last = c
    return out


def clear_midpoint(bid, cues):
    """GATE T and Gate V sample the beat's MIDPOINT: no line may be landing (a ~14-frame spring) around it. A cue that
    would start inside (mid-21 .. mid+7 frames) is moved to mid+9 frames. Needs the measured duration (pass 2)."""
    dur = None
    p = HERE / "beat_sheet.json"
    if p.exists():
        for ob in json.load(open(p))["beats"]:
            if ob["beat_id"] == bid:
                dur = ob.get("actual_duration_s")
    if not dur:
        return cues
    mid = dur / 2 * FPS
    out, last = [], 0
    for c in cues:
        if c > 0 and mid - 21 < c < mid + 7:
            c = int(mid + 9)
        c = max(c, last) if c > 0 else c
        out.append(c)
        last = max(last, c)
    return out


def est(n):
    return round(len(n.split()) / 2.5, 1)


SPARSE = ("lecture, isometric lane (show-tell drawing laws): one drawn scene on a cream stage with a few labels, "
          "the voice carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame "
          "and contrast still apply.")


def manim(bid, act, narration, cls, image, show, sparse=True):
    b = {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                  "manim": {"class": cls}, "motion_claim": image}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", lane="remotion", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show,
                  "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


A1, A2, A3, A4, A5 = ("I · What AICR Checks", "II · Unlock Once", "III · Do It For Real",
                      "IV · Rules For A Shared Cluster", "V · When It Fails")

KEYLINE = "256 SHA256:<fingerprint> <aicr-username>@aicr.ai (ED25519)"

# ───────────────────────────── the opening pair ─────────────────────────────
OPEN = [
 remotion("BIDEA", "the idea",
    "Hallo. This is Liam, in for Bear. First, a correction. To let Claude log into AICR, the shared GPU cluster, "
    "you do not hand it your password. AICR has no password. You unlock a key once, yourself, and Claude never sees it.",
    "BrutalistHesitantWriter",
    {"text": "To let Claude log in,\nI give it my password", "triggerWords": "give it my password",
     "replacementWords": "unlock the key once", "fontSize": 70, "charMs": 62, "hesitateBetween": 6,
     "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'To let Claude log in, I give it my password'"},
     {"at": 0.35, "event": "backspaces 'give it my password' -> 'unlock the key once'"}],
    lane="bookend", lead_silence_s=0.8,
    motion_claim="The writer types the newcomer's framing (give it my password) and corrects it to the real one (unlock the key once).",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. A private key: a secret file that proves who you are. A certificate: a signed note from AICR saying "
    "that key is yours. A passphrase: the password that locks the key file. The ssh-agent: a helper that holds your "
    "unlocked key in memory. BatchMode: a setting that makes ssh refuse to ask any question. And a login node: the "
    "shared computer you land on when you log in.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "Private key", "meaning": "a secret file that proves who you are"},
               {"term": "Certificate", "meaning": "a signed note from AICR saying the key is yours"},
               {"term": "Passphrase", "meaning": "the password that locks the key file"},
               {"term": "ssh-agent", "meaning": "a helper that holds your unlocked key in memory"},
               {"term": "BatchMode", "meaning": "an ssh setting that refuses to ask any question"},
               {"term": "Login node", "meaning": "the shared computer you land on when you log in"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "'Private key' lands"}, {"at": 0.25, "event": "'Certificate'"}, {"at": 0.4, "event": "'Passphrase'"},
     {"at": 0.55, "event": "'ssh-agent'"}, {"at": 0.72, "event": "'BatchMode'"}, {"at": 0.87, "event": "'Login node'"}],
    gate="CARD", lane="bookend",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

B = []


def add(b):
    B.append(b)
    return b


def shell(bid, act, narration, title, lines, cue_phrases, show, ring_lines=None, ring_phrases=None, fs=None, margin=None,
          motion_claim="The real commands and their real output print line by line, each as it is spoken."):
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


def codebeat(bid, act, narration, title, code, language, spark, cue_phrases, show, motion_claim):
    """A ClaudeCodeBeat beat. cue_phrases: one phrase (or None) per code line; blank lines get the previous cue."""
    cues = cues_for(bid, cue_phrases, narration, est(narration))
    props = {"title": title, "code": code, "language": language, "sparkLine": spark, "largeText": True, "lineCues": cues}
    return add(remotion(bid, act, narration, "ClaudeCodeBeat", props, show, motion_claim=motion_claim))


# ═════════════════════════════ ACT I · What AICR Checks ═════════════════════════════
add(manim("B10", A1,
    "AICR has no password. At the front door it checks two things. A private key, a secret file that only you hold. "
    "And a certificate, a note that AICR's own certificate authority signed, saying that key is yours.",
    "B10_KeyAndCert",
    "The AICR rack stands behind a closed gate with a padlock; a kraft key slides in from the left and a certificate page from the right; both meet at the lock, the lock opens and the rack's lights turn on.",
    [{"at": 0.25, "event": "private key arrives"}, {"at": 0.6, "event": "certificate arrives"}, {"at": 0.85, "event": "both meet at the lock; it opens"}]))
add(manim("B11", A1,
    "To get in at all, you need an account. A faculty member's proposal opens a project, and your institution creates "
    "your user. Your AICR user name is your campus name with the institution on the end, like j smith underscore n e u.",
    "B11_UserName",
    "Mono 'institutionalusername_institutioncode' on a pill; the two halves are bracketed and labelled; it transforms into 'jsmith_neu'.",
    [{"at": 0.3, "event": "the pattern appears"}, {"at": 0.85, "event": "it becomes jsmith_neu"}], sparse=True))
add(remotion("B12", A1,
    "The key files come from one place: the AICR OnDemand portal, at o o d dot aicr dot AI. You sign in there with "
    "your institutional credentials. That step is yours, not Claude's.",
    "BrowserCapture",
    {"url": "ood.aicr.ai", "image": f"{CAP}/ood.png", "caption": "The real sign-in page, captured 2 October 2026",
     "moves": [{"at": 0.0, "x": 0.5, "y": 0.42, "scale": 1.3},
               {"at": 0.6, "x": 0.5, "y": 0.55, "scale": 1.7, "ring": [0.255, 0.405, 0.49, 0.295]}]},
    [{"at": 0.0, "event": "browser window opens on ood.aicr.ai"}, {"at": 0.6, "event": "zoom to 'Select an Identity Provider'; terracotta ring"}],
    motion_claim="The real sign-in page; the camera pushes in to the sign-in choice as 'you sign in' is said."))
add(manim("B13", A1,
    "Download the folder called aicr keys. Inside are four files. Your private key, locked with a passphrase. Its "
    "public half. Your certificate, which is the credential. And a file holding your first passphrase.",
    "B13_FourFiles",
    "A drawn table builds row by row with the real file names in mono: id_ed25519_aicr (the key, with the key drawing), the .pub, the -cert.pub (certificate page), .passphrase; the certificate row is ringed.",
    [{"at": 0.25, "event": "private key row"}, {"at": 0.45, "event": "public key row"}, {"at": 0.65, "event": "certificate row, ringed"}, {"at": 0.88, "event": "passphrase row"}], sparse=True))
add(manim("B14", A1,
    "Signing in is the human step. So are putting the files in place and choosing a new passphrase. Do not give "
    "Claude your institutional password, and do not ask it to sign in for you.",
    "B14_HumanSteps",
    "A Professor Bear portrait on the left; three chips land beside it, 'Sign in', 'Download', 'Passphrase', each with a check; on the right a closed door labelled 'Claude' stays shut to the password.",
    [{"at": 0.2, "event": "Sign in"}, {"at": 0.4, "event": "Download / files in place"}, {"at": 0.55, "event": "Passphrase"}, {"at": 0.85, "event": "the password is turned away from Claude"}], sparse=True))
shell("B15", A1,
    "Put the files in your dot ssh folder, set their permissions, and swap the first passphrase for one only you "
    "know. Windows is the same, in PowerShell. Then delete the downloaded passphrase file.",
    "Terminal · macOS or Linux",
    ["$ mkdir -p ~/.ssh && chmod 700 ~/.ssh",
     "$ mv ~/Downloads/aicr_keys/id_ed25519_aicr* ~/.ssh/",
     "$ chmod 600 ~/.ssh/id_ed25519_aicr",
     "$ chmod 644 ~/.ssh/id_ed25519_aicr.pub ~/.ssh/id_ed25519_aicr-cert.pub",
     "$ ssh-keygen -p -f ~/.ssh/id_ed25519_aicr",
     "# Windows: same files in C:\\Users\\YOU\\.ssh, same ssh-keygen -p in PowerShell."],
    ["Put the files", "set their permissions", "set their permissions", "set their permissions", "swap the first passphrase", "Windows is the same"],
    [{"at": 0.1, "event": "files go to ~/.ssh"}, {"at": 0.3, "event": "permissions"}, {"at": 0.6, "event": "ssh-keygen -p changes the passphrase"}],
    fs=32, motion_claim="The real commands print line by line as they are described; no output is shown because none was run for this beat.")
shell("B16", A1,
    "Check the certificate with ssh-keygen dash L. Valid is a date range, or forever. Principals must be your AICR "
    "user name. When it nears its end, renew it in the OnDemand portal.",
    "Terminal · the public certificate file",
    ["$ ssh-keygen -L -f ~/.ssh/id_ed25519_aicr-cert.pub",
     "Type: ssh-ed25519-cert-v01@openssh.com user certificate",
     'Key ID: "<aicr-username>@aicr.ai"',
     "Valid: forever",
     "Principals: <aicr-username>",
     "# (other fields omitted)"],
    ["Check the certificate", "Check the certificate", "Check the certificate", "Valid is", "Principals must|Principles must", "When it nears"],
    [{"at": 0.05, "event": "the ssh-keygen -L command"}, {"at": 0.4, "event": "Principals, then Valid, in the real output"}],
    ring_lines=[3, 4], ring_phrases=["Valid is", "Principals must|Principles must"], fs=36)

# ═════════════════════════════ ACT II · Unlock Once ═════════════════════════════
add(manim("B20", A2,
    "Now the problem. Claude Code runs commands with no keyboard attached. If ssh stops to ask for the passphrase, "
    "nobody can answer, and the command hangs or fails.",
    "B20_NobodyAnswers",
    "A locked key with a padlock; an 'ssh' command box rides up to it; the lock raises a 'passphrase?' chip; the box waits, dimmed, with an empty answer slot beside it.",
    [{"at": 0.2, "event": "command arrives at the locked key"}, {"at": 0.45, "event": "'passphrase?' chip"}, {"at": 0.75, "event": "no one answers; the box dims and waits"}]))
add(manim("B21", A2,
    "The fix is not to give Claude the passphrase. The fix is to unlock the key before Claude arrives, once, in your "
    "own terminal, into a helper called ssh-agent. The agent holds the unlocked key in memory.",
    "B21_UnlockOnce",
    "The Professor Bear portrait types the passphrase to the padlock; the lock opens (terracotta light); the key slides into the small dark 'agent' slab and stays there.",
    [{"at": 0.3, "event": "you unlock the key"}, {"at": 0.55, "event": "the key slides into the agent"}, {"at": 0.85, "event": "the agent holds it"}]))
add(manim("B22", A2,
    "From then on, when ssh needs the key, it asks the agent, and the agent answers. The key never leaves the agent. "
    "Claude does the work. The secret never passes through it.",
    "B22_AgentAnswers",
    "The 'ssh' command box asks the agent (a question chip goes out, a signed slip returns); the box rides on to the AICR rack with the slip; the key stays inside the agent, a barrier line between it and the Claude side.",
    [{"at": 0.2, "event": "ssh asks the agent"}, {"at": 0.45, "event": "the agent answers; the key stays"}, {"at": 0.75, "event": "the command reaches AICR"}]))
CONFIG = ("Host aicr\n    HostName login.aicr.ai\n    User AICR_USERNAME\n    IdentityFile ~/.ssh/id_ed25519_aicr\n"
          "    CertificateFile ~/.ssh/id_ed25519_aicr-cert.pub\n    IdentitiesOnly yes\n    ServerAliveInterval 60\n"
          "    AddKeysToAgent yes\n    IgnoreUnknown UseKeychain\n    UseKeychain yes")
CFG1 = "\n".join(CONFIG.split("\n")[:5])
CFGL = CONFIG.split("\n")
shell("B23", A2,
    "Add one block to your ssh config. Host aicr gives the cluster a short name. Then its host name, your AICR user "
    "name, your key file, and your certificate file.",
    "The file ~/.ssh/config",
    CFGL[:5] + ["# now the command is just: ssh aicr"],
    ["Host aicr", "Then its host name", "your AICR user name|your AICR username", "your key file", "and your certificate file", "and your certificate file"],
    [{"at": 0.1, "event": "Host aicr"}, {"at": 0.45, "event": "host name, user"}, {"at": 0.75, "event": "key and certificate files"}],
    fs=46, motion_claim="The real config lines appear one by one as each is named.")
shell("B24", A2,
    "Identities only offers just this key. Server alive interval stops idle connections dropping. Add keys to agent "
    "loads the key into the agent on first use. Use keychain is for macOS only, and ignore unknown makes other "
    "systems skip it.",
    "The file ~/.ssh/config",
    CFGL + ["# keep a single Host aicr block"],
    [None] * 5 + ["Identities only", "Server alive interval", "Add keys to agent", "ignore unknown", "Use keychain", "skip it"],
    [{"at": 0.0, "event": "the first five lines are already there"}, {"at": 0.15, "event": "IdentitiesOnly"}, {"at": 0.35, "event": "ServerAliveInterval"},
     {"at": 0.55, "event": "AddKeysToAgent"}, {"at": 0.8, "event": "IgnoreUnknown / UseKeychain"}],
    fs=36, motion_claim="The five new real lines land one by one as each setting is explained.")
shell("B25", A2,
    "On a Mac, unlock it with S S H add and the apple keychain flag, so the passphrase survives restarts. On Linux, "
    "start an agent, add the key, and start Claude Code from that same terminal.",
    "Terminal · macOS and Linux",
    ["# macOS: the Keychain remembers the passphrase",
     "$ ssh-add --apple-use-keychain ~/.ssh/id_ed25519_aicr",
     "# Linux: one agent per login session",
     '$ eval "$(ssh-agent -s)"',
     "$ ssh-add ~/.ssh/id_ed25519_aicr",
     "# start Claude Code from this same terminal, so it inherits the agent"],
    ["On a Mac", "On a Mac", "On Linux", "start an agent", "add the key", "start Claude Code|start clod code"],
    [{"at": 0.1, "event": "macOS command"}, {"at": 0.55, "event": "Linux commands"}],
    fs=34, motion_claim="The real unlock commands print as each system is named.")
shell("B26", A2,
    "On Windows, open PowerShell as administrator, once. Set the agent service to start automatically, start it, and "
    "add the key.",
    "Terminal · Windows PowerShell",
    ["# PowerShell, run as administrator, once",
     "$ Get-Service ssh-agent | Set-Service -StartupType Automatic",
     "$ Start-Service ssh-agent",
     "$ ssh-add $HOME\\.ssh\\id_ed25519_aicr",
     "# under WSL, use the Linux commands inside WSL"],
    ["On Windows", "Set the agent service", "start it", "add the key", "add the key"],
    [{"at": 0.1, "event": "administrator note"}, {"at": 0.4, "event": "service commands"}, {"at": 0.8, "event": "ssh-add"}],
    fs=36, motion_claim="The real PowerShell commands print as each step is said.")
shell("B27", A2,
    "Each of these asks for your passphrase, in your own terminal. Type it there, never in a prompt to Claude. Then ask "
    "the agent what it holds. One line ending in E D two five five one nine means the key is loaded.",
    "Terminal · your own",
    ["$ ssh-add -l", KEYLINE, "# one line, ending in (ED25519): the key is loaded"],
    ["Type it there", 4.9, "One line ending"],
    [{"at": 0.55, "event": "ssh-add -l"}, {"at": 0.75, "event": "one key, ED25519"}],
    ring_lines=[1], ring_phrases=["One line ending"], fs=36)

# ═════════════════════════════ ACT III · Do It For Real ═════════════════════════════
shell("B30", A3,
    "Test it by hand first. Run ssh aicr hostname. You should get login dot aicr dot AI. The very first connection asks "
    "you to confirm the host key. Type yes yourself, because Claude cannot answer that.",
    "Terminal · your own",
    ["$ ssh aicr hostname",
     "# you should get: login.aicr.ai",
     "# first connection only: a host key prompt. Type yes yourself."],
    ["Run ssh aicr", "You should get", "The very first connection"],
    [{"at": 0.2, "event": "the command"}, {"at": 0.4, "event": "the expected answer (a comment, not captured output)"}, {"at": 0.65, "event": "the host key note"}],
    fs=40, motion_claim="The command from the guide prints; what to expect is a comment line, because this exact command was not captured.")
add(manim("B31", A3,
    "Then test it the way Claude connects: with BatchMode on. BatchMode makes ssh fail at once instead of asking "
    "anything. If it prints your user name and the host, Claude can log in.",
    "B31_FailFast",
    "Two lanes to the same padlocked key: on the top lane the box waits forever at the lock; on the lower lane (BatchMode) the box meets the lock and bounces straight back with a cross, then with the key unlocked the box passes through and a check lands.",
    [{"at": 0.2, "event": "without BatchMode the box waits"}, {"at": 0.45, "event": "with BatchMode it fails at once"}, {"at": 0.8, "event": "unlocked: it passes; a check lands"}]))
RUN1_CMD = [
    "$ ssh -o BatchMode=yes aicr \\",
    "    'whoami; hostname; date; sinfo -o \"%14P %11l %6D\"; squeue -u $USER; pwd'",
    "<aicr-username>", "login.aicr.ai", "Sun Oct 11 13:26:40 EDT 2026"]
shell("B32", A3,
    "Now a real run. Claude Code ran one ssh command with BatchMode on. Before this call, the agent held no keys. "
    "The command asks for the user name, the host, and the date.",
    "Terminal · the command Claude Code ran",
    RUN1_CMD,
    ["Claude Code ran", "Claude Code ran", "the user name|the username", "the host", "and the date"],
    [{"at": 0.15, "event": "the real command"}, {"at": 0.55, "event": "user name, host, date print"}],
    fs=32, ring_lines=[2, 3], ring_phrases=["the user name|the username", "the host"])
shell("B33", A3,
    "The cluster answered with its seven partitions, and an empty job queue, because nothing was running. The last "
    "line is the home directory, named after the user.",
    "Terminal · the command Claude Code ran",
    ["# same run, output continued",
     "PARTITION      TIMELIMIT   NODES",
     "cpu*           1-00:00:00  5",
     "rtx-batch      1-00:00:00  17",
     "b200-batch     1-00:00:00  25",
     "b200-fullnode  1-00:00:00  4",
     "rtx-devel      4:00:00     2",
     "b200-devel     4:00:00     2",
     "preemptable    1-00:00:00  46",
     "# squeue: header only, no jobs",
     "/home/<aicr-username>"],
    [None, "seven partitions", "seven partitions", "seven partitions", "seven partitions", "seven partitions", "seven partitions", "seven partitions",
     "an empty job queue", "an empty job queue", "The last line"],
    [{"at": 0.1, "event": "the partition table prints"}, {"at": 0.5, "event": "empty queue"}, {"at": 0.75, "event": "home directory"}],
    fs=32)
add(manim("B34", A3,
    "Now the test that matters. When you reboot, the agent forgets everything. So empty it on purpose, and see whether "
    "Claude can still get in.",
    "B34_EmptyOnPurpose",
    "The agent slab holds the key; a boot cycle dial sweeps; the key is pulled out and the agent's lights go dark; the 'ssh' box waits in front of the empty agent.",
    [{"at": 0.2, "event": "reboot dial sweeps"}, {"at": 0.45, "event": "the agent forgets: the key leaves, lights go dark"}, {"at": 0.8, "event": "can the box still get in?"}]))
shell("B35", A3,
    "Ask the agent what it holds: one key. Empty it with S S H add dash capital D. Ask again: nothing. The agent is "
    "empty, just as it is after a reboot.",
    "Terminal · your own",
    ["$ ssh-add -l", KEYLINE, "$ ssh-add -D", "All identities removed.", "$ ssh-add -l", "The agent has no identities."],
    ["Ask the agent", "one key", "Empty it", "Empty it", "Ask again", "nothing"],
    [{"at": 0.1, "event": "ssh-add -l shows one key"}, {"at": 0.4, "event": "ssh-add -D empties it"}, {"at": 0.6, "event": "ssh-add -l: no identities; ringed"}],
    ring_lines=[5], ring_phrases=["nothing"], fs=36)
shell("B36", A3,
    "Now log in the way Claude does, with BatchMode on and an empty agent. It still works. No prompt, no passphrase "
    "typed. And ask the agent again: the key is back.",
    "Terminal · your own",
    ["$ ssh-add -l", "The agent has no identities.",
     "$ ssh -o BatchMode=yes aicr 'whoami; hostname'", "<aicr-username>", "login.aicr.ai",
     "$ ssh-add -l", KEYLINE],
    [None, None, "Now log in", "It still works", "It still works", "ask the agent again", "the key is back"],
    [{"at": 0.0, "event": "the empty agent is still on screen"}, {"at": 0.2, "event": "BatchMode login with an empty agent"},
     {"at": 0.4, "event": "user name and host print: it works; ringed"}, {"at": 0.75, "event": "ssh-add -l: the key is back; ringed"}],
    ring_lines=[3, 4, 6], ring_phrases=["It still works", "It still works", "the key is back"], fs=36)
add(manim("B37", A3,
    "On a Mac, that is the Keychain at work. Add keys to agent asks it for the passphrase, and the key goes back into "
    "the agent. Nothing was typed, and nothing passed to Claude.",
    "B37_VaultRefills",
    "The empty agent slab, a dark vault with a round door beside it; the 'ssh' box asks; the vault door opens and the key rises into the agent, whose lights come on; the box passes to AICR. A barrier keeps the Claude side clear of the key.",
    [{"at": 0.2, "event": "the box asks the empty agent"}, {"at": 0.5, "event": "the vault returns the key"}, {"at": 0.8, "event": "the box passes; nothing crossed the barrier"}]))
add(manim("B38", A3,
    "On Linux and Windows there is no Keychain to reload the key. So this same test fails until you run S S H add again. "
    "That is expected. It tells you to run S S H add at the start of each session.",
    "B38_NoVault",
    "Same empty agent, no vault beside it; the 'ssh' box meets the lock and bounces with a cross; the portrait runs ssh-add (key rises into the agent) and the box passes; a small 'session start' tag lands on the ssh-add step.",
    [{"at": 0.2, "event": "no vault; the box bounces"}, {"at": 0.5, "event": "you run ssh-add; the key returns"}, {"at": 0.85, "event": "add it to session start"}]))
shell("B39", A3,
    "How did it get in? Ask ssh to show its steps. It found one key in the agent, and offered the certificate. The "
    "server accepted it, and ssh reports it authenticated with public key.",
    "Terminal · how it authenticated",
    ["$ ssh -v -o BatchMode=yes aicr true",
     "# (output filtered to the lines that matter)",
     "debug1: get_agent_identities: agent returned 1 keys",
     "debug1: Offering public key: ~/.ssh/id_ed25519_aicr-cert.pub ED25519-CERT SHA256:<fingerprint> explicit",
     "debug1: Server accepts key: ~/.ssh/id_ed25519_aicr-cert.pub ED25519-CERT SHA256:<fingerprint> explicit",
     'Authenticated to login.aicr.ai ([192.69.103.11]:22) using "publickey".'],
    ["Ask ssh", "Ask ssh", "It found one key", "offered the certificate", "The server accepted", "ssh reports"],
    [{"at": 0.1, "event": "ssh -v"}, {"at": 0.35, "event": "agent returned 1 keys"}, {"at": 0.5, "event": "certificate offered, accepted"}, {"at": 0.85, "event": "Authenticated ... publickey"}],
    ring_lines=[5], ring_phrases=["ssh reports"], fs=26, margin=96)

# ═════════════════════════════ ACT IV · Rules For A Shared Cluster ═════════════════════════════
add(manim("B40", A4,
    "When you ask, Claude runs one ssh command with BatchMode on, followed by your read-only commands. Claude Code "
    "asks you to approve it. On a shared system, approve each ssh command, at least the first few times.",
    "B40_YouApprove",
    "The 'ssh' command box stops at a gate beside the Professor Bear portrait; the portrait's check lands on a tag on the box; the gate lifts and the box goes on to the AICR rack.",
    [{"at": 0.25, "event": "the command waits at the gate"}, {"at": 0.55, "event": "you approve: the check lands"}, {"at": 0.85, "event": "the box goes on to AICR"}]))
add(manim("B41", A4,
    "Rule one. Read only first. Look before you change anything: s info, s queue for your own jobs, s acct, job stats, "
    "ls, and module avail.",
    "B41_ReadOnly",
    "Six command pills in mono land one by one on a row under an eye drawing: sinfo, squeue -u $USER, sacct, jobstats, ls, module avail; each takes a check; the heading 'Read only first' stays above.",
    [{"at": 0.3, "event": "sinfo, squeue"}, {"at": 0.55, "event": "sacct, jobstats"}, {"at": 0.8, "event": "ls, module avail"}], sparse=True))
add(manim("B42", A4,
    "Rule two. Never compute on a login node. Login nodes are shared, capped at four CPU cores and eight gigabytes of "
    "memory per user. Heavy work goes through Slurm, the scheduler: s batch, or s alloc and s run for a live session.",
    "B42_LoginCap",
    "The small login-node rack with a meter capped at '4 cores' and '8 GB'; a heavy job box tries to run there and is stopped at the cap; it is redirected to a 'Slurm' queue gate and on to the big AICR rack.",
    [{"at": 0.25, "event": "4 cores, 8 GB cap"}, {"at": 0.5, "event": "the heavy job is stopped"}, {"at": 0.8, "event": "it goes through Slurm to the compute rack"}]))
add(manim("B43", A4,
    "Rule three. Ask before s batch, s cancel, r m, or anything that writes outside your own project. Jobs use shared "
    "GPUs, and they count against your project.",
    "B43_AskFirst",
    "Three command pills (sbatch, scancel, rm) wait in front of a gate with the Professor Bear portrait beside it; each takes a check from the portrait before it passes; a shared GPU block lights behind the gate.",
    [{"at": 0.2, "event": "sbatch"}, {"at": 0.4, "event": "scancel"}, {"at": 0.55, "event": "rm"}, {"at": 0.85, "event": "shared GPUs count against the project"}]))
add(manim("B44", A4,
    "Rule four. Never print, copy, or upload the private key. Not cat, not s c p, not into the chat. Claude does not "
    "need to read the key to use it. The agent does that.",
    "B44_KeyStays",
    "The key sits inside the agent slab; three pills 'cat', 'scp', 'chat' approach it from the Claude side and each bounces off a glass barrier; the agent's own arrow to the AICR rack stays open.",
    [{"at": 0.3, "event": "cat bounces"}, {"at": 0.5, "event": "scp bounces"}, {"at": 0.65, "event": "chat bounces"}, {"at": 0.88, "event": "the agent uses the key"}]))
add(manim("B45", A4,
    "Rule five. Never put the passphrase in a prompt, a file, or a command. If a command asks for it, stop, and unlock "
    "the key yourself, in your own terminal.",
    "B45_PassphraseStays",
    "A passphrase chip of dots floats toward a prompt box, a file page and a command pill; each shows a cross; the chip returns to the Professor Bear portrait at the terminal, who unlocks the key (lock opens).",
    [{"at": 0.25, "event": "prompt, file, command each refused"}, {"at": 0.65, "event": "stop"}, {"at": 0.85, "event": "you unlock it yourself"}]))
add(manim("B46", A4,
    "Rule six. Use your own account only. The certificate names you, so do not use it to run work for anyone else.",
    "B46_OwnAccount",
    "The certificate page with a name line and a seal; a second portrait-less user slot to the right is refused: the certificate slides back and stays beside the one Professor Bear portrait it names.",
    [{"at": 0.3, "event": "the certificate names you"}, {"at": 0.7, "event": "no one else may use it"}]))
add(manim("B47", A4,
    "And rule seven. Mind where files live. Home is small and recoverable. Scratch is large, and it is purged. Check "
    "AICR's file system page before you move data.",
    "B47_HomeScratch",
    "A small closed home box and a wide open scratch bin side by side; the home box gets a restore arrow; the scratch bin fills and a sweep clears it; a 'check first' tag lands on the move arrow.",
    [{"at": 0.25, "event": "home: small, recoverable"}, {"at": 0.5, "event": "scratch: large, purged"}, {"at": 0.85, "event": "check before moving data"}]))

# ═════════════════════════════ ACT V · When It Fails ═════════════════════════════
add(manim("B50", A5,
    "The error you will see most is permission denied, public key. It usually means one of three things. The key is "
    "not unlocked, by far the most common after a reboot. Or the certificate is expired or missing. Or the key's "
    "permissions are wrong.",
    "B50_ThreeCauses",
    "A white plaque with 'Permission denied (publickey)' in mono; three cause cards fan out beneath it: 'Key not unlocked' (largest, most common), 'Certificate expired or missing', 'Wrong permissions'.",
    [{"at": 0.2, "event": "the error plaque"}, {"at": 0.45, "event": "key not unlocked (largest)"}, {"at": 0.7, "event": "certificate"}, {"at": 0.88, "event": "permissions"}], sparse=False))
add(manim("B51", A5,
    "Here is the trap. An empty agent looks exactly like an expired certificate. The error is the same. So check the "
    "agent with S S H add dash l before you blame the certificate.",
    "B51_TwinErrors",
    "Two identical error plaques side by side; behind the left one an empty agent, behind the right an expired certificate, both hidden by a curtain; the command pill 'ssh-add -l' sweeps across and lifts the left curtain: the agent is empty.",
    [{"at": 0.2, "event": "two identical errors"}, {"at": 0.5, "event": "same message, different causes"}, {"at": 0.8, "event": "ssh-add -l lifts the curtain: the agent is empty"}], sparse=False))
shell("B52", A5,
    "Then, if the agent holds the key, check the certificate: is it still valid? If it is not, renew it in OnDemand. "
    "And set the private key's permissions to six hundred.",
    "Terminal · your own",
    ["# 1. is the key in the agent?", "$ ssh-add -l",
     "# 2. is the certificate still valid?", "$ ssh-keygen -L -f ~/.ssh/id_ed25519_aicr-cert.pub",
     "# 3. are the permissions right?", "$ chmod 600 ~/.ssh/id_ed25519_aicr"],
    ["Then, if the agent", "Then, if the agent", "check the certificate", "is it still valid", "And set", "permissions to six hundred|permissions to 600"],
    [{"at": 0.05, "event": "step 1"}, {"at": 0.35, "event": "step 2"}, {"at": 0.75, "event": "step 3"}],
    fs=40, motion_claim="The three checks print as commands, in order; no output is shown because none was run for this beat.")
add(manim("B53", A5,
    "Other messages have short fixes. A command that hangs or wants a passphrase: unlock the key yourself. Host key "
    "verification failed: remove the old entry with ssh-keygen dash R, then connect once yourself. A new host key "
    "prompt: type yes.",
    "B53_TableA",
    "A drawn two-column table builds row by row: 'Hangs, wants passphrase' -> 'Unlock the key yourself'; 'Host key verification failed' -> 'ssh-keygen -R login.aicr.ai, connect once'; 'Confirm new host key?' -> 'Type yes yourself'.",
    [{"at": 0.15, "event": "hang row"}, {"at": 0.45, "event": "host key changed row"}, {"at": 0.8, "event": "new host key prompt row"}], sparse=True))
add(manim("B54", A5,
    "Bad configuration option: add ignore unknown above the keychain line. Connection timed out: try another network, "
    "because AICR needs no VPN. Drops when idle: server alive interval sixty. Empty after a restart: S S H add again, "
    "on a Mac with the keychain flag.",
    "B54_TableB",
    "The same table continues: 'Bad configuration option' -> 'IgnoreUnknown UseKeychain'; 'Connection timed out' -> 'Other network, no VPN'; 'Drops when idle' -> 'ServerAliveInterval 60'; 'Agent empty after restart' -> 'ssh-add again'.",
    [{"at": 0.15, "event": "bad option row"}, {"at": 0.4, "event": "timed out row"}, {"at": 0.6, "event": "idle drops row"}, {"at": 0.85, "event": "empty after restart row"}], sparse=True))

# ───────────────────────────── the closing three ─────────────────────────────
RECAP = ["AICR checks a key and a certificate, not a password.",
         "Claude cannot type a passphrase, so unlock the key once into ssh-agent.",
         "Test with BatchMode: even an emptied agent logged in on a Mac.",
         "Claude runs read-only commands and asks before it changes anything.",
         "The key and the passphrase never go into a prompt.",
         "Permission denied? Check ssh-add -l before you blame the certificate."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. AICR checks a key and a certificate, not a password. Claude cannot type a passphrase, so "
    "you unlock the key once into the ssh-agent. Test with BatchMode: even an emptied agent logged in on a Mac. "
    "Claude runs read-only commands, and asks before it changes anything. The key and the passphrase never go into a "
    "prompt. And when you see permission denied, check the agent before you blame the certificate.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land in narration order"}],
    lane="bookend", lead_silence_s=0.5,
    qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

# README step 6, verbatim as the displayed prompt; the spoken form reads the same words, with the output format and
# $USER said aloud (they cannot be read as typed).
YT_PROMPT = ('Log into the AICR cluster with `ssh aicr` and run read-only commands only. '
             'Run: whoami, hostname, pwd, sinfo -o "%14P %11l %6D", squeue -u $USER. '
             'Tell me the user name, the host, and which partitions exist. '
             'Do not submit, cancel or change anything, and do not run computation on the login node.')
YT_SPOKEN = ("Log into the AICR cluster with ssh aicr and run read-only commands only. "
             "Run: whoami, hostname, pwd, s info with its output format set to percent fourteen P, percent eleven l, percent six D, "
             "and s queue for my own user. "
             "Tell me the user name, the host, and which partitions exist. "
             "Do not submit, cancel or change anything, and do not run computation on the login node.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_SPOKEN + " Then check two things yourself. Did Claude run only "
    "read-only commands? And did it ever ask for, or print, your passphrase or your key?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Log Into AICR With Claude", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did Claude run only read-only commands, nothing that submits or changes?",
                "Check: did Claude ever ask for, or print, your passphrase or key? It should not."],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": f"{TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Logging into AICR with Claude. How to let Claude Code log "
                           "into the AICR cluster for you and run commands there, while your key and your passphrase never leave your hands.",
         "estimated_duration_s": 14.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · AICR", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German (Hallo)",
    "audience": "A researcher with an AICR account who wants Claude Code to run commands on the cluster; assumes no other film or book",
    "source_doc": "../source/README.md, evidence ../source/SESSION.md "
                  "(three real runs, 2026-10-11), primary the AICR documentation 'SSH' page (local copy not included) and a private project setup note (not included) section 2",
    "playlist": "Northeastern HPC and AICR", "chapter_number": 8,
    "series_title": "Research Computing on Explorer and AICR", "series_video_number": 9, "series_video_count": 13,
    "series_entry_video": "Video 1 · AICR Introduction",
    "lecture_opening_description": "Let Claude Code log in while your key stays yours",
    "lecture_opening_title_lines": ["Logging into AICR", "with Claude"],
    "tags": ["AICR", "AI Compute Resource", "Claude Code", "SSH", "ssh-agent", "SSH certificate", "BatchMode", "Northeastern University",
             "Research Computing", "HPC", "GPU cluster", "Slurm", "Nik Bear Brown"]},
    "beats": BEATS}

# keep measured audio fields across re-runs (audio-first: never lose the clock)
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

# mirror the capture into the Remotion public folder
pub = ART / "runtime/remotion/public" / CAP
pub.mkdir(parents=True, exist_ok=True)
for png in (HERE / "captures").glob("*.png"):
    shutil.copy2(png, pub / png.name)

p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
n_est = sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in BEATS)
print(len(BEATS), "beats; est", round(n_est), "s", "(measured)" if all(b.get("actual_duration_s") for b in BEATS) else "(estimate)")
