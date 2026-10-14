#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-logging-into-explorer-with-claude.

LECTURE (Bear, 2026-10-02): the WHOLE source as one act-structured film, primarily visual, best visual per beat from
the full playset, a tool shown as itself. Skill doctrine: brutalist.art/skills/make/lecture/SKILL.md.

Source:   hpc-aicr/Logging-into-Explorer-with-Claude/SESSION.md (the real session, 2026-10-11) and hpc-aicr/skills/hpc/HPC.md section 10.
Evidence: every terminal line is READ FROM THE SESSION RECORD at build time by sl() below (a missing line stops the build).

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
TITLE = "Logging into Explorer (HPC) with Claude"
CAP = "lecture-logging-into-explorer-with-claude"      # captures: none (every terminal beat is the real session record)
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




SESSION = HERE.parents[1] / "Logging-into-Explorer-with-Claude/SESSION.md"
_SL = SESSION.read_text().splitlines()


def sl(start, maxlen=110, nth=0, exact=False):
    """The `nth` line of the real Explorer session record that starts with `start` (or equals it, if exact=True), verbatim; cut
    with an ellipsis if longer than maxlen. Stops the build if there is none: a film must never invent terminal output."""
    hits = [ln for ln in _SL if (ln == start if exact else ln.startswith(start))]
    if len(hits) <= nth:
        raise SystemExit(f"sl: no line (occurrence {nth}) {'equal to' if exact else 'starting with'} {start!r} in the session record")
    ln = hits[nth]
    return ln if len(ln) <= maxlen else ln[:maxlen].rsplit(" ", 1)[0] + " …"
A1, A2, A3, A4, A5 = ("I · What Explorer Asks For", "II · Make And Install A Key", "III · Unlock It Once",
                      "IV · Let Claude Do It", "V · How It Differs From AICR")

# Real names on screen are the researcher's own login name and paths as they appeared in the session record.
# ───────────────────────────── the opening pair ─────────────────────────────
OPEN = [
 remotion("BIDEA", "the idea",
    "Hallo. This is Liam, in for Bear. First, a correction. To let Claude log into Explorer, you do not hand it your password. "
    "You make a key, you unlock it once yourself, and Claude never sees either.",
    "BrutalistHesitantWriter",
    {"text": "To let Claude log in,\nI give it my password", "triggerWords": "give it my password",
     "replacementWords": "make a key and unlock it once", "fontSize": 66, "charMs": 62, "hesitateBetween": 6,
     "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'To let Claude log in, I give it my password'"},
     {"at": 0.35, "event": "backspaces 'give it my password' -> 'make a key and unlock it once'"}],
    lane="bookend", lead_silence_s=0.8,
    motion_claim="The writer types the newcomer's framing (give it my password) and corrects it to the real one (make a key and unlock it once).",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. A private key: a secret file that proves who you are. A public key: its matching half, safe to share. An "
    "ssh agent: a helper that holds your unlocked key. BatchMode: a setting that makes ssh refuse to ask any question. A host "
    "alias: a short name for the cluster in your ssh config. And a login node: the shared computer you land on when you connect.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "Private key", "meaning": "a secret file that proves who you are"},
               {"term": "Public key", "meaning": "its matching half, safe to share"},
               {"term": "ssh-agent", "meaning": "a helper that holds your unlocked key"},
               {"term": "BatchMode", "meaning": "an ssh setting that refuses to ask any question"},
               {"term": "Host alias", "meaning": "a short name for the cluster in your ssh config"},
               {"term": "Login node", "meaning": "the shared computer you land on when you connect"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "'Private key' lands"}, {"at": 0.25, "event": "'Public key'"}, {"at": 0.4, "event": "'ssh-agent'"},
     {"at": 0.55, "event": "'BatchMode'"}, {"at": 0.72, "event": "'Host alias'"}, {"at": 0.87, "event": "'Login node'"}],
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


# ═════════════════════════════ ACT I · What Explorer Asks For ═════════════════════════════
add(manim("B10", A1,
    "Explorer lets you in with your Northeastern password. You connect to the login host, answer the first host key question "
    "with yes, type the password, and you land on a login node. On our account there was no Duo prompt for ssh. The web portal "
    "is different: the documentation says it asks.",
    "B10_PasswordToday",
    "The Professor Bear portrait (1x1) at the left types dots into a password chip; an arrow runs to a small login rack labelled 'login node'; on the way a 'host key? yes' chip is answered; a 'Duo' chip sits crossed beside the ssh arrow and a second 'Duo' chip beside a 'web portal' box is ticked as 'asks (documented)'.",
    [{"at": 0.2, "event": "you, the password, the arrow to the login node"}, {"at": 0.5, "event": "the host key question answered yes"}, {"at": 0.8, "event": "no Duo on ssh; the web portal asks"}]))
add(manim("B11", A1,
    "That works for you at a keyboard. It does not work for Claude. Claude Code runs commands with no keyboard attached, and a "
    "password is the one thing you must never hand it. So we replace the password with something the agent can use without ever "
    "seeing it. A key.",
    "B11_NotForClaude",
    "The Claude logo chip (logo_chip) at the left reaches toward a password chip held by the portrait; a closed door stops the hand; a small kraft key chip then slides into view beside the logo and the door opens to the login rack.",
    [{"at": 0.2, "event": "Claude has no keyboard"}, {"at": 0.5, "event": "the password is held back"}, {"at": 0.85, "event": "a key opens the door instead"}]))
add(manim("B12", A1,
    "One detail on the login name. The one that worked was the name from the access form, the user I D, not the first part of "
    "an email address. If your first guess is refused, try the other, and wait a little after any password change.",
    "B12_WhichLoginName",
    "Two mono chips side by side: 'user ID from the access form' (ringed, with a check) and 'email prefix' (second try); a small clock chip 'wait after a password change' lands under them.",
    [{"at": 0.25, "event": "the user ID chip, ringed"}, {"at": 0.55, "event": "the email prefix: the second try"}, {"at": 0.88, "event": "wait after a password change"}], sparse=True))

# ═════════════════════════════ ACT II · Make And Install A Key ═════════════════════════════
add(manim("B20", A2,
    "A key comes in two halves. The private half stays on your computer and proves who you are. The public half is safe to hand "
    "out, and Explorer will keep a copy. When you connect, your computer proves it holds the private half that matches.",
    "B20_KeyPair",
    "A kraft key drawn in two halves: the private half (dark outline, a padlock) stays beside the portrait; the public half (lighter, no lock) slides across to the login rack and is filed on a shelf; the two halves briefly line up across the gap with a check.",
    [{"at": 0.2, "event": "two halves"}, {"at": 0.5, "event": "the public half travels to Explorer"}, {"at": 0.85, "event": "the halves match"}]))
shell("B21", A2,
    "Make it with ssh keygen. The type is E D twenty-five five-nineteen, a modern default. You choose a passphrase, which locks "
    "the private file and which Claude never sees. The command prints where both halves went, and a fingerprint, a short name for "
    "this key.",
    "Terminal · your computer, step one",
    [sl("$ ssh-keygen -t ed25519"), sl("Your identification has been saved in"), sl("Your public key has been saved in"),
     sl("The key fingerprint is:"), sl("SHA256:ikUx2")],
    [None, "where both halves went", "where both halves went", "a fingerprint", "a short name for"],
    [{"at": 0.05, "event": "the command"}, {"at": 0.45, "event": "where both halves went"}, {"at": 0.85, "event": "the fingerprint"}],
    ring_lines=[0, 4], ring_phrases=["Make it with", "a short name for"], fs=26, margin=100)
shell("B22", A2,
    "To install the public half, one command: ssh copy id. It asks for your Northeastern password this one time, typed by you, "
    "and it reports that one key was added. After this, Explorer knows your key.",
    "Terminal · your computer, step two",
    [sl("$ ssh-copy-id"), sl("/usr/bin/ssh-copy-id: INFO: 1 key(s) remain", 112), sl("Number of key(s) added")],
    [None, "asks for your Northeastern password", "reports that one key was added"],
    [{"at": 0.05, "event": "the command"}, {"at": 0.45, "event": "it asks for the password once"}, {"at": 0.85, "event": "one key added"}],
    ring_lines=[2], ring_phrases=["reports that one key was added"], fs=28, margin=100)

# ═════════════════════════════ ACT III · Unlock It Once ═════════════════════════════
add(manim("B30", A3,
    "Now the old problem. Claude cannot type a passphrase. So you unlock the key yourself, once, into a helper called the ssh "
    "agent. The agent holds the unlocked key, ssh asks the agent, and the key never passes through Claude.",
    "B30_UnlockOnce",
    "The portrait types the passphrase to a padlock on the private key; the lock opens (terracotta light); the key slides into a dark agent slab; the Claude logo chip then sends an 'ssh' command box to the agent, which answers with a signed slip while the key stays inside; a barrier line separates the key from the Claude side.",
    [{"at": 0.2, "event": "you unlock the key"}, {"at": 0.5, "event": "the key goes into the agent"}, {"at": 0.85, "event": "ssh asks the agent; the key never reaches Claude"}]))
shell("B31", A3,
    "On a Mac, one command: ssh add, with the Apple Keychain flag. You type the passphrase here, in your own terminal. It answers "
    "that the identity was added. With the Keychain, the key can reload itself when the agent is emptied.",
    "Terminal · your own terminal, once",
    [sl("$ ssh-add --apple-use-keychain"), sl("Enter passphrase for"), sl("Identity added:")],
    [None, "You type the passphrase", "the identity was added"],
    [{"at": 0.05, "event": "the command"}, {"at": 0.4, "event": "the passphrase prompt (typed by you)"}, {"at": 0.8, "event": "identity added"}],
    ring_lines=[2], ring_phrases=["the identity was added"], fs=28, margin=100)
shell("B32", A3,
    "Then give the cluster a short name. One block in your ssh config. Host explorer. The real host name. Your user name. The key "
    "file, and identities only, so ssh offers just this key. Add keys to agent, use keychain, and a keep alive.",
    "The file ~/.ssh/config",
    [sl("Host explorer"), sl("    HostName login.explorer"), sl("    User <explorer-username>"), sl("    IdentityFile ~/.ssh/id_ed25519_explorer"),
     sl("    IdentitiesOnly yes"), sl("    AddKeysToAgent yes"), sl("    UseKeychain yes"), sl("    ServerAliveInterval 60")],
    [None, "The real host name", "Your user name", "The key file", "identities only", "Add keys to agent", "use keychain", "a keep alive"],
    [{"at": 0.05, "event": "Host explorer"}, {"at": 0.35, "event": "host name and user"}, {"at": 0.6, "event": "the key file"}, {"at": 0.85, "event": "the agent and keep-alive lines"}],
    fs=40, margin=100)
shell("B33", A3,
    "Here is a real mistake from this setup, so you do not repeat it. Before that block existed, the test failed: could not "
    "resolve host name explorer. Ssh treated explorer as a computer name, because nothing told it otherwise. The fix is the block "
    "you just saw.",
    "Terminal · a real failure, before the config block",
    [sl("$ ssh -o BatchMode=yes explorer 'whoami; hostname'", nth=0), sl("ssh: Could not resolve hostname explorer", 118)],
    [None, "could not resolve host name explorer"],
    [{"at": 0.1, "event": "the test command"}, {"at": 0.55, "event": "could not resolve hostname explorer"}],
    ring_lines=[1], ring_phrases=["could not resolve host name explorer"], fs=30, margin=100)

# ═════════════════════════════ ACT IV · Let Claude Do It ═════════════════════════════
shell("B40", A4,
    "Test it the way Claude will connect. BatchMode makes ssh fail at once instead of asking a question. It printed the user name, "
    "and the login node, explorer dash zero one. No password, no passphrase, no Duo.",
    "IV · Let Claude Do It  ·  your terminal, the BatchMode test",
    [sl("$ ssh -o BatchMode=yes explorer 'whoami; hostname'", nth=1), sl("<explorer-username>", exact=True), sl("explorer-01", exact=True)],
    [None, "the user name", "the login node"],
    [{"at": 0.05, "event": "the command"}, {"at": 0.5, "event": "the user name"}, {"at": 0.8, "event": "the login node"}],
    ring_lines=[1, 2], ring_phrases=["the user name", "explorer dash zero one"], fs=38, margin=100)
shell("B41", A4,
    "Then Claude Code ran the same login itself, with four read-only commands: who am I, which host, which folder, and my own "
    "jobs. The job list printed only its header, because there were none.",
    "Terminal · Claude Code's own run, read-only",
    [sl("$ ssh -o BatchMode=yes explorer 'whoami; hostname; pwd; squeue -u <explorer-username>'", 120), sl("/home/<explorer-username>", exact=True),
     sl("             JOBID PARTITION", 90)],
    [None, "which folder", "the job list printed only its header"],
    [{"at": 0.05, "event": "Claude Code's command"}, {"at": 0.5, "event": "the home folder"}, {"at": 0.85, "event": "an empty job list"}],
    ring_lines=[2], ring_phrases=["only its header"], fs=26, margin=100)
add(manim("B42", A4,
    "From here, Claude follows the rules in the H P C dot M D file. Read only first. Ask before it submits, cancels, or deletes. "
    "Never compute on the login node. And if any command ever prompts, it stops and tells you.",
    "B42_AskBeforeChange",
    "The Claude logo chip stands at a login rack; four small rule chips land beside it: 'read-only first' (ticked), 'ask before submit, cancel, delete' (a gate with the portrait holding the key), 'no compute on the login node' (a crossed job box on the login rack), 'prompt: stop and tell you' (a stop mark).",
    [{"at": 0.2, "event": "read-only first"}, {"at": 0.45, "event": "ask before changing anything"}, {"at": 0.7, "event": "no compute on the login node"}, {"at": 0.9, "event": "a prompt means stop"}]))
shell("B43", A4,
    "Then the hardest test, which is a deliberate one. Empty the agent. It reports no identities. Log in anyway, and it still "
    "works, because the Keychain reloaded the key, and the list shows it back. This command empties every key, so our rules say "
    "only you run it, on purpose, as a test.",
    "Terminal · the empty-agent test, run on purpose",
    [sl("$ ssh-add -D"), sl("All identities removed."), sl("$ ssh-add -l", nth=0), sl("The agent has no identities."),
     sl("$ ssh -o BatchMode=yes explorer 'whoami; hostname'", nth=2), sl("<explorer-username>", exact=True, nth=2), sl("explorer-01", exact=True, nth=2),
     sl("$ ssh-add -l", nth=1), sl("256 SHA256:ikUx2", 100)],
    [None, "Empty the agent", "It reports no identities", "It reports no identities", "Log in anyway", "it still works", "it still works", "the list shows it back", "the list shows it back"],
    [{"at": 0.05, "event": "the agent is emptied"}, {"at": 0.35, "event": "no identities"}, {"at": 0.6, "event": "the login still works"}, {"at": 0.85, "event": "the key is back"}],
    ring_lines=[3, 5, 8], ring_phrases=["It reports no identities", "it still works", "the list shows it back"], fs=28, margin=100)

# ═════════════════════════════ ACT V · How It Differs From AICR ═════════════════════════════
add(manim("B50", A5,
    "How is this different from AICR? On Explorer you start with your password, and you make your own key. On AICR there is no "
    "password at all: you download a key and a certificate that the AICR certificate authority signed. Your Explorer user name is your "
    "university login. Your AICR name is built from it, with an underscore and the institution on the end. And access comes from "
    "a project sponsor on Explorer, and from a proposal on AICR.",
    "B50_ExplorerVsAICR",
    "A drawn three-column table builds row by row: columns '' / 'Explorer' / 'AICR'; rows 'starts with' (password / no password), 'key' (you make it / you download it), 'certificate' (none / signed by AICR), 'user name' (your university login / <aicr-username>), 'access' (project sponsor / proposal); the differing cells are marked, nothing else.",
    [{"at": 0.12, "event": "starts with"}, {"at": 0.3, "event": "key"}, {"at": 0.5, "event": "certificate"}, {"at": 0.7, "event": "user name"}, {"at": 0.88, "event": "access"}], sparse=True))
add(manim("B51", A5,
    "What is the same matters more. Both are ssh. Both need you to unlock a key once into the agent. Both are tested with "
    "BatchMode. And on both, Claude never holds your password, your passphrase, or your key.",
    "B51_WhatIsTheSame",
    "Two racks side by side labelled 'Explorer' and 'AICR' with one shared drawing between them: the key going into the agent slab; four check chips land under it: 'ssh', 'unlock once', 'BatchMode', 'Claude never holds it'.",
    [{"at": 0.2, "event": "both are ssh"}, {"at": 0.45, "event": "unlock once into the agent"}, {"at": 0.65, "event": "BatchMode"}, {"at": 0.88, "event": "Claude never holds the secret"}]))
add(manim("B52", A5,
    "And what we did not test. Logging in from off campus or another network. The web portal. And whether Research Computing "
    "permits automated agent access. The policy pages mention none of them, so ask once, by email to R C help, at Northeastern dot E D U.",
    "B52_NotTested",
    "Three grey dashed chips land in a row: 'off campus or another network', 'the web portal', 'agent access policy', each with an open ring instead of a check; a mail chip 'rchelp@northeastern.edu' lands below them.",
    [{"at": 0.2, "event": "off campus or another network"}, {"at": 0.45, "event": "the web portal"}, {"at": 0.7, "event": "agent access policy"}, {"at": 0.9, "event": "ask Research Computing once"}], sparse=True))

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
    "playlist": "Northeastern HPC and AICR", "chapter_number": 10,
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
