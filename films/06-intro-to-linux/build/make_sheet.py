#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-intro-to-linux.

LECTURE (brutalist.art/skills/make/lecture/SKILL.md). Source: hpc/Intro-to-Linux-2026/intro_to_linux.md ("Introduction to
Linux", Northeastern Research Computing, presenter Ghanghoon "Will" Paik; github.com/northeastern-rc-training/Intro-to-Linux-2026).
A terminal lecture: the tool IS the terminal, so most beats are the training's own sessions replayed verbatim in a plain shell.
Sixth film of the series; same cast for the drawn beats.
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Intro to Linux"
FPS = 30
SPARSE = ("lecture, drawn lane (show-tell drawing laws): one drawn scene on a cream stage with a few labels, the voice "
          "carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply.")


def manim(bid, act, narration, cls, image, show, sparse=False):
    b = {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show, "manim": {"class": cls}, "motion_claim": image}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", lane="remotion", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


def shell(bid, act, narration, lines, show, start=20, gap=40, title="Terminal"):
    return remotion(bid, act, narration, "CCPlainShell", {"title": title, "lines": lines, "startCue": start, "lineGap": gap}, show,
                    motion_claim="The training's own terminal session replays line by line, verbatim.")


A = ["I · What Linux Is", "II · Finding Your Way", "III · Making And Moving Files", "IV · Reading Files", "V · Who May Do What",
     "VI · Editing", "VII · Quick Tips"]

OPEN = [
 remotion("BIDEA", "the idea",
    "Salaam. This is Liam, in for Bear. First, a correction. The terminal isn't an old way to use a computer. It's the "
    "direct way, and on a cluster it's the main one: the keyboard becomes your only input. This lecture is the basics of "
    "the Linux terminal: what Linux is, how to find your way around the file system, how to make, move and remove "
    "files, how to read them, who may do what to them, two editors, and three tips that save you every day.",
    "BrutalistHesitantWriter",
    {"text": "The terminal is the old way\nto use a computer", "triggerWords": "old way", "replacementWords": "direct way",
     "fontSize": 72, "charMs": 62, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types the assumption"}, {"at": 0.3, "event": "corrects 'old way' -> 'direct way'"}],
    lane="bookend", lead_silence_s=0.8, motion_claim="The writer types the newcomer's picture and corrects it.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. The kernel: the core of an operating system, the part that talks to the hardware. A shell: the program that "
    "reads what you type and runs it. A directory: a folder. A path: the address of a file, written from the root slash or "
    "from where you stand. Root: the administrator account that may do anything. And a flag: a dash and a letter that "
    "changes what a command does.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "kernel", "meaning": "the core of an operating system; it talks to the hardware"},
               {"term": "shell", "meaning": "the program that reads what you type and runs it"},
               {"term": "directory", "meaning": "a folder"},
               {"term": "path", "meaning": "a file's address, from the root / or from where you stand"},
               {"term": "root", "meaning": "the administrator account that may do anything"},
               {"term": "flag", "meaning": "a dash and a letter that changes what a command does"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "kernel"}, {"at": 0.25, "event": "shell"}, {"at": 0.4, "event": "directory"}, {"at": 0.58, "event": "path"}, {"at": 0.72, "event": "root"}, {"at": 0.87, "event": "flag"}],
    gate="CARD", lane="bookend", qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

B = [
 # I
 manim("B10", A[0],
    "Linux is a family of operating systems built on the Linux kernel, which Linus Torvalds created in 1991 in the "
    "tradition of Unix, the much older system that also shaped macOS. It runs on Android phones, on laptops, and on nearly "
    "every HPC cluster. It's free and open source, so anyone can contribute and a huge toolbox comes at no cost, and it's "
    "considered secure and robust, which is why servers and clusters run it.",
    "B10_LinuxFamily",
    "A dark kernel block at the centre; a timeline tick '1991' lands; a Unix block above feeds two lines down to Linux and macOS; around the kernel three devices appear (a phone, a laptop, a server rack) each lit by a line from the kernel; tags 'free · open source' and 'secure · robust' land. Act title top-left.",
    [{"at": 0.15, "event": "kernel, 1991"}, {"at": 0.3, "event": "Unix → Linux, macOS"}, {"at": 0.5, "event": "phones, laptops, clusters"}, {"at": 0.75, "event": "free, open source"}, {"at": 0.92, "event": "secure, robust"}]),
 shell("B11", A[0],
    "Linux has graphical desktops, but underneath is the command line, reached through a terminal. The prompt tells you four "
    "things: your user name, the host you're on, where you are, and what kind of user you are. A dollar sign means a normal "
    "user. A hash means root, the administrator. A normal user can't install system packages: ask, and you're told you're "
    "not in the sudoers file.",
    ["[user@host myDir]$", "[root@host myDir]#", "# user · host · current directory · $ normal, # root", "",
     "[user@host ~]$ sudo dnf install python", "user is not in the sudoers file. This incident will be reported."],
    [{"at": 0.3, "event": "the two prompts"}, {"at": 0.55, "event": "$ vs #"}, {"at": 0.8, "event": "not in the sudoers file"}], start=40, gap=56),
 # II
 manim("B20", A[1],
    "The file system is files and directories, as on Windows or a Mac. The terminal colours them: blue for directories, green "
    "for executables, red for compressed archives, plain for ordinary files. A path is a file's address. Absolute: from the "
    "root, starting with a slash. Relative: from where you stand. One dot is here. Two dots is one level up.",
    "B20_PathsAndColours",
    "A small directory tree draws (root / → home → user → dir with files); four swatches land with their meanings (directory · executable · compressed · file) in grey, green-grey, kraft-red, ink; a mono '/home/user/dir' path highlights the chain from the root; then '../dir' highlights a hop up and over; '.' and '..' tags land. Act title top-left.",
    [{"at": 0.2, "event": "the tree"}, {"at": 0.4, "event": "four colours"}, {"at": 0.65, "event": "absolute path from /"}, {"at": 0.85, "event": "relative: . and .."}]),
 shell("B21", A[1],
    "Three commands move you around. p w d prints where you are; the tilde is your home. l s lists what's here. Flags change "
    "it: dash l for the long listing with permissions, owner, size and date; dash a for everything, including hidden files, "
    "whose names start with a dot. Flags combine, dash l a.",
    ["[user@host ~]$ pwd", "/home/user", "[user@host ~]$ ls", "dir1 dir2 dir3 file1 file2 file3", "[user@host ~]$ ls -l",
     "drwxr-xr-x. 1 user group 90 Jan  8 13:47 dir1", "-rw-r--r--. 1 user group 10 Jan  8 13:44 file1", "[user@host ~]$ ls -a",
     ". .. dir1 dir2 dir3 file1 file2 file3", ".hidden1 .hidden2 .hiddenDir"],
    [{"at": 0.1, "event": "pwd"}, {"at": 0.3, "event": "ls"}, {"at": 0.5, "event": "ls -l"}, {"at": 0.8, "event": "ls -a, hidden files"}], start=20, gap=30),
 shell("B22", A[1],
    "c d changes directory. c d into a folder; the prompt shows you're there. c d dot dot goes one level up. c d alone, or c d "
    "tilde, takes you home from anywhere.",
    ["[user@host ~]$ cd dir1", "[user@host dir1]$ pwd", "/home/user/dir1", "[user@host dir1]$ cd ..", "[user@host ~]$ pwd", "/home/user",
     "[user@host someDir]$ cd ~", "[user@host ~]$ pwd", "/home/user"],
    [{"at": 0.1, "event": "cd dir1"}, {"at": 0.45, "event": "cd .."}, {"at": 0.75, "event": "cd ~"}], start=20, gap=30),
 # III
 shell("B30", A[2],
    "Making things. touch creates an empty file. To put text in one, redirect: a single greater-than overwrites the file, a "
    "clean slate; a double one appends to the end. cat shows the result. And make-dir, m k d i r, makes a directory.",
    ["[user@host emptyDir]$ touch new_file", "[user@host emptyDir]$ echo \"Hello\" > new_file", "[user@host emptyDir]$ cat new_file", "Hello",
     "[user@host emptyDir]$ echo \"World\" >> new_file", "[user@host emptyDir]$ cat new_file", "Hello", "World",
     "[user@host emptyDir]$ mkdir new_dir", "[user@host emptyDir]$ ls", "new_dir new_file"],
    [{"at": 0.1, "event": "touch"}, {"at": 0.3, "event": "> overwrites"}, {"at": 0.55, "event": ">> appends"}, {"at": 0.85, "event": "mkdir"}], start=20, gap=28),
 shell("B31", A[2],
    "C P copies a file; a directory needs dash capital R, recursive, to copy what's inside. The original stays. m v moves, and "
    "moving a file to a new name is how you rename.",
    ["[user@host emptyDir]$ cp new_file new_file_copy", "[user@host emptyDir]$ cp -R new_dir new_dir_copy", "[user@host emptyDir]$ ls",
     "new_dir new_dir_copy new_file new_file_copy", "[user@host emptyDir]$ mv new_file_copy ./new_dir_copy", "[user@host emptyDir]$ mv new_file new_name",
     "[user@host emptyDir]$ ls", "new_dir new_dir_copy new_name"],
    [{"at": 0.1, "event": "cp"}, {"at": 0.3, "event": "cp -R"}, {"at": 0.6, "event": "mv into a directory"}, {"at": 0.8, "event": "mv as rename"}], start=20, gap=34),
 manim("B32", A[2],
    "r m removes a file; dash r removes a directory and everything in it. There is no trash can and no undo. On a cluster, a "
    "removed file is gone, so read the command twice before you press return.",
    "B32_RemoveIsForever",
    "A file page and a kraft folder on the stage; mono 'rm new_name' lands and the page dissolves to nothing; 'rm -r new_dir_copy' lands and the folder with its contents dissolves; where a trash can would be, a dashed empty outline with 'no undo' beside it. Act title top-left.",
    [{"at": 0.15, "event": "rm: the file vanishes"}, {"at": 0.4, "event": "rm -r: the folder vanishes"}, {"at": 0.7, "event": "no trash can, no undo"}], sparse=True),
 shell("B33", A[2],
    "A symbolic link is a shortcut, like an alias on a Mac. l n dash s, then the target, then the name you want: point to "
    "target, call it link name. In a long listing it starts with l and shows an arrow to where it points. Now c d my_data "
    "jumps to the deep directory. Move or delete the original and the link breaks.",
    ["[user@host ~]$ ln -s /projects/data/intro_to_linux ./my_data", "[user@host ~]$ ls -l", "total 0",
     "lrwxrwxrwx 1 user group 18 Feb 12 15:21 my_data", "    -> /projects/data/intro_to_linux", "[user@host ~]$ cd my_data"],
    [{"at": 0.15, "event": "ln -s target link"}, {"at": 0.5, "event": "l … -> target"}, {"at": 0.8, "event": "cd my_data"}], start=30, gap=56),
 # IV
 shell("B40", A[3],
    "Reading a file. cat dumps the whole thing into the terminal, fine for a short one. For a long one use less: a scrollable "
    "viewer. Arrows move a line, Page Up and Page Down a page, Home and End jump to the ends, and q quits. Escape does not "
    "close it.",
    ["[user@host ~]$ cat short_doc.txt", "hello world!", "[user@host ~]$ less long_doc.txt", "# ↑ ↓ one line · PgUp PgDn a page · Home End · q quits",
     "# ESC does not close less"],
    [{"at": 0.1, "event": "cat"}, {"at": 0.4, "event": "less"}, {"at": 0.7, "event": "the keys"}, {"at": 0.9, "event": "q quits"}], start=30, gap=60),
 # V
 manim("B50", A[4],
    "Who may do what. Every file has three audiences: the user who owns it, the group that owns it, and others, everyone "
    "else. And three permissions: read, write, and execute, which for a directory means entering it. Each permission has a "
    "number: read four, write two, execute one.",
    "B50_ThreeByThree",
    "A 3×3 grid draws: columns user · group · others (small tokens: one figure, three figures, a crowd), rows read · write · execute with their numerals 4 · 2 · 1 beside; cells fill as spoken; a small directory icon beside 'execute' gets a door. Act title top-left.",
    [{"at": 0.2, "event": "user, group, others"}, {"at": 0.5, "event": "read, write, execute"}, {"at": 0.8, "event": "4, 2, 1"}]),
 manim("B51", A[4],
    "Here's a real long-listing line, decoded. The first character is the type: dash for a file, d for a directory, l for a "
    "link. Then nine characters in three groups of three: the owner's permissions, the group's, everyone else's. r w x: the "
    "owner can read, write and execute. r w dash: the group can read and write but not run. r dash dash: others can only "
    "read. After that: the link count, the owner, the group, the size in bytes, the modification time, and the name.",
    "B51_DecodeTheLine",
    "The mono line '-rwxrw-r-- 1 user group 46 Feb 14 16:37 File.txt' sits large on the stage; brackets rise under each part as spoken, with small labels (type · owner · group · others · links · owner · group · size · time · name); the three permission triads lift apart and each gets its reading in words.",
    [{"at": 0.1, "event": "the line"}, {"at": 0.25, "event": "type"}, {"at": 0.45, "event": "rwx · rw- · r--"}, {"at": 0.8, "event": "links, owner, group, size, time, name"}]),
 shell("B52", A[4],
    "Changing permissions with c h mod. By symbol: who, plus or minus, which. g plus x gives the group execute. u minus x "
    "takes it from the owner. Combinations join with commas. Or by number: three digits, owner, group, others, each the sum "
    "of four, two and one. Seven five one is read-write-execute for the owner, read and execute for the group, execute only "
    "for others.",
    ["$ chmod g+x File.txt", "$ chmod u-x File.txt", "$ chmod ug+w,o-r File.txt", "$ chmod 751 File.txt",
     "# USER   = 7: r(4) + w(2) + x(1)", "# GROUP  = 5: r(4) + x(1)", "# OTHERS = 1: x(1)"],
    [{"at": 0.15, "event": "g+x"}, {"at": 0.3, "event": "u-x"}, {"at": 0.45, "event": "combinations"}, {"at": 0.6, "event": "751"}, {"at": 0.8, "event": "7 5 1 decoded"}], start=30, gap=46),
 shell("B53", A[4],
    "And ownership with c h own: user colon group, then the file. Dash capital R for a whole directory.",
    ["$ chown USER:GROUP FILE_NAME", "$ chown -R USER:GROUP DIRECTORY_NAME"],
    [{"at": 0.2, "event": "chown"}, {"at": 0.7, "event": "-R for a directory"}], start=30, gap=50),
 # VI
 shell("B60", A[5],
    "Two editors live in the terminal. Nano is the simple one: nano and a file name. Its shortcuts are listed along the bottom, "
    "and the caret means Control. Vim is the powerful one, with two modes. In normal mode you can't type into the file. "
    "Press i for insert mode and type. Press Escape to get back to normal mode. Type colon w q to save and quit. Stuck? "
    "Escape, then colon q exclamation mark quits without saving.",
    ["$ nano myFile.txt", "# shortcuts along the bottom; ^ means Ctrl", "$ vim myFile.txt", "# normal mode: cannot edit",
     "# i      → insert mode: type", "# ESC    → back to normal mode", "# :wq    → save and quit", "# :q!    → quit without saving"],
    [{"at": 0.1, "event": "nano"}, {"at": 0.35, "event": "vim"}, {"at": 0.55, "event": "i, ESC"}, {"at": 0.75, "event": ":wq"}, {"at": 0.9, "event": ":q!"}], start=30, gap=50),
 # VII
 shell("B70", A[6],
    "Three tips. Tab completes a long name: type the start, press Tab, the shell fills the rest. Control C stops a running "
    "program, or throws away a line you've mistyped. And clear wipes the screen.",
    ["$ cd ~/myRe<TAB>", "$ cd ~/myResearchProject", "$ python longProgram.py", "(... no progress for 30 min ...)", "<Ctrl + C>",
     "$ cd ~/myRESearchProij", "<Ctrl + C>", "$ clear"],
    [{"at": 0.15, "event": "Tab completes"}, {"at": 0.5, "event": "Ctrl + C stops"}, {"at": 0.75, "event": "Ctrl + C cancels"}, {"at": 0.9, "event": "clear"}], start=20, gap=24),
 manim("B71", A[6],
    "That's the terminal. Prompt, path, list, move, make, copy, remove with care, read, permissions, an editor, and Tab. "
    "Questions go to the Research Computing team at r c help at northeastern dot e d u, or to office hours on Zoom.",
    "B71_TheToolbelt",
    "A row of ten small mono command chips lands one by one along a belt (pwd · ls · cd · touch · mkdir · cp · mv · rm · less · chmod), the rm chip gets a small dashed 'no undo' tag; then 'rchelp@northeastern.edu' lands beneath in mono. Act title top-left.",
    [{"at": 0.1, "event": "the chips land"}, {"at": 0.8, "event": "rchelp"}]),
]

RECAP = ["The prompt: user, host, where you are, $ or #.",
         "pwd, ls -la, cd; absolute paths start with /, . is here, .. is up.",
         "touch, > and >>, mkdir, cp -R, mv; rm has no undo; ln -s target link.",
         "cat for short files, less for long ones; q quits.",
         "rwx for user, group, others; chmod by symbol or by 4-2-1 numbers.",
         "nano is simple; vim: i, ESC, :wq. Tab completes, Ctrl+C stops."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. The prompt shows your user, host, location, and whether you're root. p w d, l s with flags, "
    "and c d move you; absolute paths start from the root; a single dot means here, two dots mean up. touch, redirection, make-dir, "
    "C P dash R, M V; r m has no undo; l n dash s makes a shortcut. cat for short files, less for long ones, q quits. Read, "
    "write, execute for user, group and others, changed with c h mod by symbol or by number. Nano is simple; vim is i, "
    "Escape, colon w q. Tab completes, and Control C stops.",
    "ClaudeVerdictArtifact", {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land"}],
    lane="bookend", lead_silence_s=0.5, qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("I'm new to the Linux terminal on a cluster. Give me a ten-command practice session: make a project folder in my home "
             "directory with two subfolders, create a notes file with one line, append a second line, copy it into a subfolder, "
             "rename the copy, make the file readable by my group but not by others, and show me the long listing after each step "
             "so I can see what changed. Explain each command in one sentence.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_PROMPT + " Then check two things yourself. Did every path it wrote start "
    "with a slash or a tilde? And did it warn you before the first r m?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "A Ten-Command Practice Session", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did every path it wrote start with / or ~?", "Check: did it warn you before the first rm?"],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": f"{TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

# Gate V underfill on drawn beats that build progressively (48% / 53% at the sampled midpoint on the first 4K run).
for b in B:
    if b["beat_id"] in {"B51", "B71"} and "qc" not in b:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE + " Progressive drawing: the midpoint frame holds only part of the final picture."}
BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Intro to Linux. The shell commands every cluster user needs: moving around, files, permissions, and the habits that keep a shared system happy.",
         "estimated_duration_s": 10.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]
sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · LINUX", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "Arabic (Salaam)",
    "audience": "Anyone opening a Linux terminal on a cluster for the first time; assumes no other film",
    "source_doc": "hpc/Intro-to-Linux-2026/intro_to_linux.md (Northeastern Research Computing training, presenter Ghanghoon 'Will' Paik; "
                  "github.com/northeastern-rc-training/Intro-to-Linux-2026), read 2026-10-06",
    "playlist": "Explorer", "chapter_number": 5,
    "series_title": "Research Computing on Explorer and AICR", "series_video_number": 6, "series_video_count": 13, "series_entry_video": "Video 1 · AICR Introduction",
    "lecture_opening_description": "The shell commands every cluster user needs",
    "tags": ["Linux", "terminal", "command line", "bash", "ls", "cd", "chmod", "vim", "nano", "HPC", "Northeastern", "Research Computing", "Nik Bear Brown"]},
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
print(len(BEATS), "beats; est", round(sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in BEATS)), "s")
