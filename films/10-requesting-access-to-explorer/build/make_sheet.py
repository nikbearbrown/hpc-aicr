#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-requesting-access-to-explorer.

LECTURE (Bear, 2026-10-02): the WHOLE source as one act-structured film, primarily visual, best visual per beat,
a tool shown as itself. Skill doctrine: brutalist.art/skills/make/lecture/SKILL.md.

Source: ../source/README.md (written 2026-10-11 from the Research Computing training
slides, rc-docs pages and the first screen of the ServiceNow access form). Facts the README marks NOT CONFIRMED are
never asserted here; see FACTCHECK.md.

Spine: BOPEN title card -> BIDEA hesitant writer -> BDEFS key terms -> five acts -> BVDT recap -> BHTF your turn -> BOUT.

Run: python3 make_sheet.py   (writes beat_sheet.json; keeps measured audio fields across re-runs; recomputes every
audio-dependent cue - terminal line cues, definitions duration - from the measured clock when it exists).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Requesting Access to Explorer"
FPS = 30                                   # Remotion composition clock (BrowserCapture / CCPlainShell / AccessFormCard)
OOD_IMG = "lecture-explorer-ood/screenshot_OOD.png"     # already in runtime/remotion/public (the training's own screenshot)
OOD_ASPECT = 2126 / 1284                                # the public copy has the browser strip cropped off

SPARSE = ("lecture, drawn lane (show-tell drawing laws): a few cast pieces on a cream stage with short labels; the voice "
          "carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and contrast apply.")
SPARSE_SHELL = ("a real terminal window with the few lines the source gives; the commands are the content and no output "
                "was run, so none is shown. Only underfill is waived.")


def est(n):
    return round(len(n.split()) / 2.5, 1)


def fr(narr, phrase, keep_out=True):
    """Where `phrase` starts in the narration, as a fraction of the beat (0-1). Nothing animates inside 45-55%
    (GATE T and Gate V sample the midpoint): a cue inside that window moves to the nearer edge."""
    i = narr.index(phrase)            # raises if the phrase is not in the narration: a typo must not pass silently
    f = round(i / len(narr), 3)
    if keep_out and 0.43 <= f <= 0.57:
        f = 0.42 if f < 0.50 else 0.58
    return f


def manim(bid, act, narration, cls, image, show):
    return {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW", "narration_text": narration,
            "estimated_duration_s": est(narration), "voice": "am_onyx", "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                     "manim": {"class": cls}, "motion_claim": image},
            "qc": {"sparse_by_design": True, "sparse_reason": SPARSE}}


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", lane="remotion", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": gate, "narration_text": narration,
         "estimated_duration_s": est(narration), "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


SHELL_CUES = {}        # beat_id -> [phrase or None per line]; lineCues are computed from the clock in the post-pass


def shell(bid, act, narration, title, lines, phrases, show, ring_line=None, ring_phrase=None, font=None):
    assert len(lines) == len(phrases), bid
    props = {"title": title, "lines": lines, "startCue": 12, "lineGap": 30}
    if font:
        props["fontSize"] = font
    SHELL_CUES[bid] = (phrases, ring_line, ring_phrase)
    return remotion(bid, act, narration, "CCPlainShell", props, show,
                    motion_claim="The real commands from the source land line by line on the words that name them; no output is shown because none was run.",
                    qc={"sparse_by_design": True, "sparse_reason": SPARSE_SHELL})


def form(bid, act, narration, moves, highlights, link_phrase=None, cont_phrase=None):
    """The access-form card (new component AccessFormCard). `moves` and `highlights` carry PHRASES; they become
    fractions of the beat here, so the card needs no audio to be cued."""
    mv = []
    for i, m in enumerate(moves):
        m = dict(m)
        ph = m.pop("phrase", None)
        m["at"] = 0 if i == 0 else fr(narration, ph)
        mv.append(m)
    hl = [{"target": t, "at": fr(narration, ph), "kind": k} for (t, ph, k) in highlights]
    props = {"link": "https://bit.ly/NURC-AccessRequest", "moves": mv, "highlights": hl, "topBarLabel": "Technology"}
    if link_phrase:
        props["linkAt"] = fr(narration, link_phrase)
    if cont_phrase:
        props["continuesAt"] = fr(narration, cont_phrase)
    return remotion(bid, act, narration, "AccessFormCard", props,
                    [{"at": 0.0, "event": "the form's first screen opens (white page, grey inputs, dark 'Technology' bar)"}] +
                    [{"at": h["at"], "event": f"{h['target']}: {h['kind']}"} for h in hl],
                    motion_claim="The form's real first screen; the highlight lands on each field, option or sentence as it is named.",
                    qc={"sparse_by_design": True, "sparse_reason": "the form's real first screen at reading size; a page, not a poster"})


A1, A2, A3, A4, A5 = ("I · The Rule", "II · Two Routes In", "III · The Form", "IV · After Approval", "V · If It Fails")

# ───────────────────────────── the opening pair ─────────────────────────────
BIDEA_N = ("Bonjour. This is Liam, in for Bear. First, a correction. Getting on Explorer isn't just a form and your login. "
           "Either way, you need a sponsor, someone whose storage space you belong to. This lecture covers the rule, "
           "the two ways in, what the form's first screen looks like, and how to check that it worked.")
BDEFS_N = ("Six terms. A PI: the principal investigator, the faculty member who leads a project. A sponsor: the PI or staff "
           "member who owns a storage space. A storage space: a folder under slash projects that a group shares. A delegate: "
           "a member the sponsor lets add other people. A member: someone who can read, write and run in the project. "
           "And Duo: the second sign-in check.")
OPEN = [
    remotion("BIDEA", "the idea", BIDEA_N, "BrutalistHesitantWriter",
             {"text": "To get on Explorer,\nI just need to fill in a form", "triggerWords": "just need to fill in a form",
              "replacementWords": "need my sponsor", "fontSize": 70, "charMs": 62, "hesitateBetween": 6,
              "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
             [{"at": 0.0, "event": "types 'To get on Explorer, I just need to fill in a form'"},
              {"at": 0.35, "event": "backspaces 'just need to fill in a form' -> 'need my sponsor'"}],
             lane="bookend", lead_silence_s=0.8,
             motion_claim="The writer types the newcomer's framing (just a form) and corrects it to the real one (I need my sponsor).",
             qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
    remotion("BDEFS", "terms", BDEFS_N, "ClaudeDefinitions",
             {"title": "Terms In This Lecture",
              "terms": [{"term": "PI", "meaning": "principal investigator: the faculty member who leads a project"},
                        {"term": "Sponsor", "meaning": "the PI or staff member who owns a storage space"},
                        {"term": "Storage space", "meaning": "a folder under /projects that a group shares"},
                        {"term": "Delegate", "meaning": "a member the sponsor lets add other people"},
                        {"term": "Member", "meaning": "can read, write and run in the project"},
                        {"term": "Duo", "meaning": "the second sign-in check"}],
              "folderLabel": "@NikBearBrown"},
             [{"at": 0.08, "event": "'PI' lands"}, {"at": 0.22, "event": "'Sponsor'"}, {"at": 0.38, "event": "'Storage space'"},
              {"at": 0.6, "event": "'Delegate'"}, {"at": 0.76, "event": "'Member'"}, {"at": 0.9, "event": "'Duo'"}],
             gate="CARD", lane="bookend",
             qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

# ───────────────────────────── the acts ─────────────────────────────
N = {}   # narration per beat (the scenes' until() phrases are checked against these)
N["B10"] = ("Here's the rule that decides everything. A Northeastern login alone won't get you onto Explorer. "
            "Every user has to belong to a storage space that a sponsor owns.")
N["B11"] = ("The sponsor is a PI or a staff member, and the space is a folder under slash projects. Research groups get it free, "
            "up to thirty-five terabytes. If a sponsor has no space yet, they request one first.")
N["B12"] = ("Four roles. The PI owns the project, and can add members, guests and delegates. A delegate can add members. "
            "A member reads, writes and runs. A guest reads and runs, but can't write.")
N["B20"] = ("Two routes in. Route A: your sponsor or their delegate adds you. Route B: you submit the access form. "
            "Research Computing recommends every PI name a delegate, so route A never waits on one person.")
N["B21"] = ("Route A has two ways. The simpler one needs no terminal. In Open OnDemand, under Files, is an app called Managing slash "
            "projects. The sponsor picks the group, types the usernames, comma-separated with no spaces, and clicks Launch. "
            "A log shows what changed.")
N["B22"] = ("The other way is a command. First, s run gets the sponsor or a delegate onto a node in the short partition. Then the project "
            "command names the project and your username. Several people go in as a comma-separated list, and view members checks the result.")
N["B23"] = ("Then wait. Changes can take up to two hours to reach the whole cluster. And once you're added, start a fresh login "
            "session, because your groups are read when you log in.")
N["B24"] = ("One caveat I can't settle. Whether either way works for someone who has never had an Explorer account is not "
            "confirmed. If that's you, ask Research Computing first, at r c help at northeastern dot e d u.")
N["B30"] = ("Route B is a form, reached at bit dot l y, slash N U R C, dash Access Request. It starts at the university sign-in. "
            "You sign in yourself, and that is what identifies you.")
N["B31"] = ("Once you're in, the first screen is headed Requester Information, and it's pre-filled from your sign-in. Your name, last then "
            "first. A blank phone. Your Northeastern email. Two drop-downs, location and department. And a user I D.")
N["B32"] = ("Then one required choice. Please choose one. First option: I do not have access to the High Performance Computer, "
            "H P C, cluster. I am requesting a new account.")
N["B33"] = ("Second option: I already have access to the High Performance Computer, H P C, cluster. I need to update my sponsor "
            "information. So: new here, pick the first. Already in, changing sponsor, pick the second.")
N["B34"] = ("Below that, two paragraphs. One: every user must belong to a sponsor-owned storage space, and a sponsor with none can "
            "request one. Two: if a space exists, its owner can add members to the cluster themselves, following the documentation.")
N["B35"] = ("The form goes on below this. I haven't seen the rest, so I won't describe it. Read every field before you submit.")
N["B36"] = ("What happens after you submit? We think your sponsor is asked to approve it. That's our guess, not a confirmed step, and we "
            "don't know how long it takes. Confirm with Research Computing, at r c help at northeastern dot e d u.")
N["B40"] = ("Once you're approved, which name do you log in with? The training's example is s dot caplins. In the one real login "
            "checked, the user I D from the form worked, not the email prefix. So try that first. Your first login settles it.")
N["B41"] = ("Door one is the terminal. S S H, your username, at login dot explorer dot northeastern dot e d u. The first time, it asks "
            "a host-key question: type yes. Then your Northeastern password. Nothing shows as you type. In the one login checked, "
            "no Duo prompt appeared.")
N["B42"] = ("Door two is the browser: O O D dot explorer dot northeastern dot e d u. Your username and password, plus Duo. "
            "You land on this dashboard.")
N["B43"] = ("To check you're in, type who am I. It prints your login name. Then groups. It should list your sponsor's project group.")
N["B44"] = ("Your home is slash home, slash your username. Your scratch is slash scratch, slash your username.")
N["B50"] = ("Rejected at the door? Either you have no Explorer account yet, or the username is wrong. Try the user I D from the form, "
            "then your email prefix. If you changed your password minutes ago, wait a while. If you're sure, submit the form.")
N["B51"] = ("You can log in, but groups doesn't list the project? Your sponsor hasn't added you yet. Ask the PI or a delegate to "
            "run the add command.")
N["B52"] = ("You're the sponsor and you have no storage space? There's nothing to add people to. Submit the storage space request "
            "first. Anything else, write to r c help at northeastern dot e d u.")

B = [
    # ACT I
    manim("B10", A1, N["B10"], "B10_GateNeedsStorage",
          "You stand at a gate with a Login card; the card is turned back. A sponsor's storage space and its owner appear behind the gate; a Member chip travels to you and the gate opens.",
          [{"at": 0.2, "event": "login card turned back at the gate"}, {"at": 0.55, "event": "storage space and sponsor appear"}, {"at": 0.85, "event": "membership reaches you; gate opens"}]),
    manim("B11", A1, N["B11"], "B11_StorageSpace",
          "The cabinet labelled /projects with its owner; a 35 TB bar fills and is marked free; the cabinet goes to a dashed outline, a request page lands, and it is solid again.",
          [{"at": 0.2, "event": "sponsor beside /projects"}, {"at": 0.45, "event": "35 TB bar fills, free"}, {"at": 0.8, "event": "no space: dashed; request lands; space exists"}]),
    manim("B12", A1, N["B12"], "B12_RoleLadder",
          "Four rungs of a ladder land in turn: PI, Delegate, Member, Guest, each with what it can do; the guest's 'can't write' is struck.",
          [{"at": 0.2, "event": "PI"}, {"at": 0.4, "event": "Delegate"}, {"at": 0.62, "event": "Member"}, {"at": 0.8, "event": "Guest; write struck"}]),
    # ACT II
    manim("B20", A2, N["B20"], "B20_TwoRoutes",
          "You on the left, the storage space on the right; path A (sponsor adds you) and path B (the form) draw in; a delegate joins the sponsor and path A flows without the PI.",
          [{"at": 0.15, "event": "route A draws"}, {"at": 0.4, "event": "route B draws"}, {"at": 0.65, "event": "delegate appears"}, {"at": 0.85, "event": "route A flows without the PI"}]),
    manim("B21", A2, N["B21"], "B21_ManagingApp",
          "A sketch of the announced Open OnDemand app: breadcrumb Files > Managing /projects, a Group drop-down, a Usernames box typed as a comma list, a Launch button pressed, an Output log filling.",
          [{"at": 0.15, "event": "Files > Managing /projects"}, {"at": 0.4, "event": "group chosen"}, {"at": 0.6, "event": "usernames typed"}, {"at": 0.78, "event": "Launch pressed"}, {"at": 0.92, "event": "output log"}]),
    shell("B22", A2, N["B22"], "Terminal",
          ["# step 1: a node in the short partition", "$ srun -p short --constraint=ib --pty bash",
           "# step 2: add the member", "$ project <project_name> add members <username>",
           "# several people: a comma-separated list, no spaces", "$ project mylab add members rot1,rot2,rot3",
           "# check afterwards", "$ project <project_name> view members"],
          ["The other way", "First, s run", "Then the project", "names the project", "Several people", "comma-separated list",
           "view members", "checks the result"],
          [{"at": 0.1, "event": "the srun line"}, {"at": 0.4, "event": "the add command"}, {"at": 0.65, "event": "the list form"}, {"at": 0.9, "event": "view members"}]),
    manim("B23", A2, N["B23"], "B23_TwoHourDelay",
          "A clock hand sweeps a full turn to 'up to 2 hours'; an 'old session' chip stands ghosted and a 'new session' chip lands with a terracotta check.",
          [{"at": 0.2, "event": "clock sweeps: up to 2 hours"}, {"at": 0.7, "event": "old session ghosted; new session checked"}]),
    manim("B24", A2, N["B24"], "B24_NewUserCaveat",
          "A command box travels toward you and stops short; 'No account yet' and a terracotta '?' appear; the Research Computing address lands underneath.",
          [{"at": 0.2, "event": "the command travels toward you and stops short"}, {"at": 0.6, "event": "No account yet; ?"}, {"at": 0.85, "event": "rchelp@northeastern.edu"}]),
    # ACT III  (the centrepiece: the form's real first screen, built as a card; see BUILD-LOG for the swap list)
    remotion("B30", A3, N["B30"], "BrowserCapture",
             {"url": "https://bit.ly/NURC-AccessRequest", "image": "lecture-requesting-access/northeastern-sign-in.png",
              "imageAspect": round(1176 / 1230, 4), "caption": "Northeastern sign-in, captured 2026-10-11",
              "moves": [{"at": 0.0, "x": 0.5, "y": 0.3, "scale": 1.0},
                        {"at": fr(N["B30"], "You sign in yourself"), "x": 0.45, "y": 0.22, "scale": 1.25,
                         "ring": [0.115, 0.185, 0.70, 0.075]}],
              "ringColor": "#3D3929"},
             [{"at": 0.0, "event": "browser window opens on the link; the real Northeastern sign-in page"},
              {"at": 0.7, "event": "push in to the 'Email or Username@northeastern.edu' box; ring (nothing is typed)"}],
             motion_claim="The real sign-in page; the camera pushes in to the sign-in box as 'you sign in yourself' is said. No credentials are ever typed."),
    form("B31", A3, N["B31"],
         [{"x": 0.5, "y": 0.28, "scale": 1.0}],
         [("heading", "Requester Information", "glow"), ("requester", "Your name", "glow"), ("phone", "A blank phone", "glow"),
          ("email", "Your Northeastern email", "glow"), ("location", "location and", "glow"), ("department", "department", "glow"),
          ("userid", "user I D", "ring")]),
    form("B32", A3, N["B32"],
         [{"x": 0.65, "y": 0.57, "scale": 1.25}],
         [("choose", "Please choose one", "glow"), ("radio1", "First option", "select")]),
    form("B33", A3, N["B33"],
         [{"x": 0.65, "y": 0.57, "scale": 1.25}],
         [("radio2", "Second option", "select")]),
    form("B34", A3, N["B34"],
         [{"x": 0.65, "y": 0.74, "scale": 1.3}, {"phrase": "Two: if a space exists", "x": 0.65, "y": 0.86, "scale": 1.3}],
         [("p1", "sponsor-owned storage space", "mark"), ("p2", "its owner can add members", "mark")]),
    form("B35", A3, N["B35"],
         [{"x": 0.62, "y": 0.80, "scale": 1.0}],
         [], cont_phrase="I haven't seen the rest"),
    manim("B36", A3, N["B36"], "B36_AfterSubmit",
          "A form page slides to the sponsor; dashed Approve/Deny chips and a 'We think this is how it works' label appear; a terracotta '?' lands over them; the Research Computing address lands.",
          [{"at": 0.2, "event": "the form goes to the sponsor"}, {"at": 0.4, "event": "dashed Approve / Deny; label: We think this is how it works"}, {"at": 0.6, "event": "?"}, {"at": 0.85, "event": "rchelp@northeastern.edu"}]),
    # ACT IV
    manim("B40", A4, N["B40"], "B40_WhichName",
          "The example s.caplins is written; two chips appear, 'UserID' marked 'try first' and 'email prefix' second, and funnel into a 'First login' slot where a terracotta check lands.",
          [{"at": 0.25, "event": "s.caplins"}, {"at": 0.55, "event": "UserID: try first; email prefix second"}, {"at": 0.85, "event": "first login: check"}]),
    shell("B41", A4, N["B41"], "Terminal",
          ["# try the UserID from the form first", "$ ssh <username>@login.explorer.northeastern.edu",
           "Are you sure you want to continue connecting (yes/no/[fingerprint])? yes", "password:",
           "# nothing shows as you type"],
          ["Door one", "S S H, your", "host-key question", "Then your Northeastern", "Nothing shows"],
          [{"at": 0.15, "event": "the ssh command"}, {"at": 0.4, "event": "the real host-key question; yes"}, {"at": 0.7, "event": "password prompt"}],
          ring_line=1, ring_phrase="at login dot", font=32),
    remotion("B42", A4, N["B42"], "BrowserCapture",
             {"url": "ood.explorer.northeastern.edu", "image": OOD_IMG, "imageAspect": round(OOD_ASPECT, 4),
              "caption": "The training's own screenshot of the real site, after sign-in",
              "moves": [{"at": 0.0, "x": 0.5, "y": 0.45, "scale": 1.0},
                        {"at": fr(N["B42"], "You land on this dashboard"), "x": 0.45, "y": 0.3, "scale": 1.5,
                         "ring": [0.06, 0.245, 0.74, 0.065]}],
              "ringColor": "#3D3929"},
             [{"at": 0.0, "event": "browser window opens on ood.explorer.northeastern.edu"},
              {"at": 0.75, "event": "push in to the dashboard; ring"}],
             motion_claim="The real Open OnDemand dashboard (the training's screenshot); the camera pushes in as it is named."),
    shell("B43", A4, N["B43"], "Terminal",
          ["$ whoami", "# your login name", "$ groups", "# should list your sponsor's project group"],
          ["who am I", "It prints", "Then groups", "It should list"],
          [{"at": 0.2, "event": "whoami"}, {"at": 0.5, "event": "groups"}]),
    manim("B44", A4, N["B44"], "B44_HomeScratch",
          "The home box and the scratch bin from the AICR cast drop in with their real path shapes: /home/<username>, /scratch/<username>.",
          [{"at": 0.2, "event": "home box and path"}, {"at": 0.65, "event": "scratch bin and path"}]),
    # ACT V
    manim("B50", A5, N["B50"], "B50_Rejected",
          "You at the shut gate with a cross; 'No account yet' and 'Wrong username' tags land; a form page ringed at its UserID line, then an 'email prefix' chip, then 'Wait a while'; the page slides in and the gate opens.",
          [{"at": 0.15, "event": "No account yet"}, {"at": 0.3, "event": "Wrong username"}, {"at": 0.6, "event": "UserID ringed, then email prefix; wait a while"}, {"at": 0.85, "event": "form submitted"}]),
    manim("B51", A5, N["B51"], "B51_NotInProject",
          "You are in (a check) but the groups list has an empty slot; the sponsor appears and a command box travels to the list; the slot fills with the project.",
          [{"at": 0.15, "event": "a check: you can log in"}, {"at": 0.45, "event": "empty slot in groups"}, {"at": 0.8, "event": "add command fills it"}]),
    manim("B52", A5, N["B52"], "B52_NoStorage",
          "The sponsor beside a dashed (non-existent) storage space; the add command bounces off; a request page lands and the space becomes solid; the Research Computing address lands.",
          [{"at": 0.2, "event": "add bounces off the empty space"}, {"at": 0.55, "event": "request lands; space solid"}, {"at": 0.85, "event": "rchelp@northeastern.edu"}]),
]

# ───────────────────────────── the closing three ─────────────────────────────
RECAP = ["Explorer needs a sponsor's storage space, not just a login.",
         "Your sponsor adds you, or you submit the access form.",
         "Try the form's UserID first; your first login settles it.",
         "Check with whoami and groups; if it fails, ask your sponsor."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. Explorer needs a place in a sponsor's storage space, not just a login. Your sponsor adds you with "
    "one command, or you submit the access form. Try the user I D from the form first, and your first login settles it. "
    "Check with who am I and groups, and if it fails, ask your sponsor.",
    "ClaudeVerdictArtifact", {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "four recap lines land in narration order"}],
    lane="bookend", lead_silence_s=0.5,
    qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("I'm a new user of Northeastern's Explorer cluster. My Northeastern username is [my username] and my sponsor is "
             "[sponsor's name]. Write the short message I send them. It must give my username and the exact command they or a "
             "delegate should run, project [project name] add members [my username], on a node in the short partition. "
             "Keep it to four sentences.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_PROMPT + " Then check two things yourself. Does the message give your username "
    "and the project name? And once your sponsor replies, does groups list the project?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Ask Your Sponsor To Add You", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: does the message give your username and the project name?",
                "Check: once your sponsor replies, does groups list the project?"],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens: 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": f"{TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Requesting Access to Explorer. Why a login alone isn't enough, "
                           "the two ways to get added to a sponsor's storage space, and how to check you're in.",
         "estimated_duration_s": 10.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · EXPLORER", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "French (Bonjour)",
    "audience": "A member of a research group with a Northeastern login who has never used Explorer; assumes no other film or book",
    "source_doc": "../source/README.md (Northeastern Research Computing training slides, rc-docs pages, "
                  "and the first screen of the access form), read 2026-10-11",
    "playlist": "Northeastern HPC and AICR", "chapter_number": 10,
    "series_title": "Research Computing on Explorer and AICR", "series_video_number": 10, "series_video_count": 13,
    "series_entry_video": "Video 1 · AICR Introduction",
    "lecture_opening_description": "Why a login alone isn't enough, and how to get added",
    "tags": ["Explorer cluster", "Northeastern University", "Research Computing", "HPC", "access request", "sponsor",
             "project command", "Open OnDemand", "ssh", "ServiceNow", "Nik Bear Brown"]},
    "beats": BEATS}


# ───────────── audio-first: keep measured fields; derive every audio-dependent cue from the clock ─────────────
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
    rem = b["shot"].get("remotion") or {}
    props = rem.get("props")
    if props is None:
        continue
    pat = rem["pattern"]
    clock = dur or b["estimated_duration_s"]
    if dur and pat in ("ClaudeDefinitions", "BrowserCapture", "CCPlainShell", "AccessFormCard"):
        props["durationSeconds"] = dur
    elif pat in ("CCPlainShell", "AccessFormCard", "BrowserCapture") and "durationSeconds" not in props:
        props["durationSeconds"] = round(clock + 0.5, 2)       # estimate until the audio is measured
    if pat == "CCPlainShell":
        phrases, ring_line, ring_phrase = SHELL_CUES[b["beat_id"]]
        narr = b["narration_text"]
        cues, last = [], 0
        for i, ph in enumerate(phrases):
            c = round(fr(narr, ph) * clock * FPS)
            c = max(c, last + 6) if i else max(12, c)
            cues.append(c)
            last = c
        props["lineCues"] = cues
        if ring_line is not None:
            props["rings"] = [{"line": ring_line, "cue": max(cues[ring_line], round(fr(narr, ring_phrase) * clock * FPS))}]

# ───────────── guards: nothing ships with a TODO, a stray phrase, or a real person's data ─────────────
blob = json.dumps(sheet)
assert "TODO" not in blob and "⚠" not in blob
for bid, n in N.items():
    assert next(b for b in BEATS if b["beat_id"] == bid)["narration_text"] == n
body = (HERE / "_scenes_body.py").read_text() if (HERE / "_scenes_body.py").exists() else ""
missing = []
for m in re.finditer(r'class (B\d+)_\w+\(Scene\).*?(?=\nclass |\n# attach)', body, re.S):
    bid, chunk = m.group(1), m.group(0)
    for ph in re.findall(r'until\(self, "([^"]+)"', chunk):
        if ph not in N.get(bid, ""):
            missing.append((bid, ph))
assert not missing, f"until() phrases not in narration: {missing}"
for b in BEATS:
    if b["beat_id"].startswith("B") and b["beat_id"][1:].isdigit():
        assert 15 <= len(b["narration_text"].split()) <= 56, (b["beat_id"], len(b["narration_text"].split()))
p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(BEATS), "beats; est", round(sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in BEATS)), "s")
