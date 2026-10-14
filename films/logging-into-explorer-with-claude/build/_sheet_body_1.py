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
