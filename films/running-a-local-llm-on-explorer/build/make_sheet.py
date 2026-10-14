#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-running-a-local-llm-on-explorer.

LECTURE (Bear, 2026-10-02): the WHOLE source as one act-structured film, primarily visual, best visual per beat from
the full playset, a tool shown as itself. Skill doctrine: brutalist.art/skills/make/lecture/SKILL.md.

Source:   _research/source-tutorial.md (a copy of hpc-aicr/Running-a-Local-LLM-on-Northeastern's Explorer-Cluster-and-
          Pointing-Coding-Agents-at-It/explorer-local-llm-tutorial.md). Every script line on a terminal beat is READ FROM THE
          SOURCE at build time by sl()/sq() below (a missing line stops the build): a film must never invent script text.
Honesty:  the setup is DOCUMENTED, not run end to end for this film. The terminal beats show the scripts as written; no
          command output is shown that was not in the source or in a recorded real check (HPC.md Appendix A items 26 and 27,
          Sections 7 and 8). The film says so out loud (B95).

Spine: BOPEN -> BIDEA -> BDEFS -> ten acts -> BVDT -> BHTF -> BOUT.
Two passes: pass 1 (no _qc/asr.json) estimates cues; after Kokoro + faster-whisper, pass 2 places every terminal line on
the word Liam says (word times in _qc/asr.json).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Running a Local LLM on Explorer"
ART = HERE.parents[2] / "brutalist.art"
FPS = 30

ASR = {}
_ap = HERE / "_qc/asr.json"
if _ap.exists():
    ASR = json.loads(_ap.read_text())


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def word_t(bid, phrase, nth=0, default=None):
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
    out, last = [], 0
    for ph in phrases:
        if ph is None:
            out.append(0)
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


SRC = (HERE / "_research/source-tutorial.md").read_text()
_SL = SRC.splitlines()


def _cut(ln, maxlen):
    if len(ln) <= maxlen:
        return ln
    return ln[:maxlen].rsplit(" ", 1)[0] + " …"


def sl(start, maxlen=92, exact=False):
    """The FIRST source line whose text (leading spaces ignored) starts with `start` (or equals it when exact=True),
    verbatim (indentation kept), cut at a word boundary with an ellipsis if longer than maxlen. Stops the build if absent."""
    for ln in _SL:
        s = ln.strip()
        if (s == start) if exact else s.startswith(start):
            return _cut(ln.rstrip(), maxlen)
    raise SystemExit(f"sl: no source line starting with {start!r}")


def sq(text, maxlen=92):
    """An exact fragment that must occur in the source (used for table cells and inline code)."""
    if text not in SRC:
        raise SystemExit(f"sq: fragment not in the source: {text!r}")
    return _cut(text, maxlen)


A1, A2, A3, A4, A5, A6, A7, A8, A9, A10 = (
    "I · The Idea And Its Layers", "II · Wrong Turns To Avoid", "III · One-Time Setup", "IV · Choose A GPU And A Model",
    "V · Pattern A, On The GPU Node", "VI · Pattern B, From Your Laptop", "VII · Other Coding Agents", "VIII · When It Breaks",
    "IX · The Cluster's Rules", "X · What To Expect")

A11 = "XI · Get Started"

# The get-started recipe lives in the hpc-aicr repository; terminal lines for it are read from the guide itself.
GUIDE = (HERE.parents[2] / "hpc-aicr-release/skills/local-llm-on-explorer/GET-STARTED.md").read_text()
_GL = GUIDE.splitlines()


def gl(start):
    for ln in _GL:
        if ln.strip().startswith(start):
            return ln.rstrip()
    raise SystemExit(f"gl: no line starting with {start!r} in GET-STARTED.md")


# ───────────────────────────── the opening pair ─────────────────────────────
OPEN = [
 remotion("BIDEA", "the idea",
    "Hallo. This is Liam, in for Bear. First, a correction. A local model on the cluster is not free and always running. It runs "
    "inside a GPU job you ask for. There is no per-token billing, but the cost moves to queue time and fair share.",
    "BrutalistHesitantWriter",
    {"text": "A local model on the cluster\nis free and always running", "triggerWords": "free and always running",
     "replacementWords": "a GPU job you ask for", "fontSize": 66, "charMs": 62, "hesitateBetween": 6,
     "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'A local model on the cluster is free and always running'"},
     {"at": 0.35, "event": "backspaces 'free and always running' -> 'a GPU job you ask for'"}],
    lane="bookend", lead_silence_s=0.8,
    motion_claim="The writer types the newcomer's framing (free and always running) and corrects it to the real one (a GPU job you ask for).",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Five terms. Ollama: the program that serves an open model. Apptainer: a tool that runs containers without root. A Slurm "
    "job: your request for a compute node. A harness: the coding agent that sends the requests. And a context window: how much "
    "text the model can see at once.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "Ollama", "meaning": "the program that serves an open model"},
               {"term": "Apptainer", "meaning": "runs containers without root"},
               {"term": "Slurm job", "meaning": "your request for a compute node"},
               {"term": "Harness", "meaning": "the coding agent that sends requests"},
               {"term": "Context window", "meaning": "how much text the model sees at once"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "'Ollama' lands"}, {"at": 0.3, "event": "'Apptainer'"}, {"at": 0.5, "event": "'Slurm job'"},
     {"at": 0.7, "event": "'Harness'"}, {"at": 0.87, "event": "'Context window'"}],
    gate="CARD", lane="bookend",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: five prerequisites, one line each."}),
]

B = []


def add(b):
    B.append(b)
    return b


def shell(bid, act, narration, title, lines, cue_phrases, show, ring_lines=None, ring_phrases=None, fs=28, margin=100,
          motion_claim="The script text, exactly as written, prints line by line as it is spoken."):
    cues = cues_for(bid, cue_phrases, narration, est(narration))
    cues = clear_midpoint(bid, cues)
    props = {"title": title, "lines": lines, "startCue": 20, "lineGap": 30, "lineCues": cues, "fontSize": fs, "windowMargin": margin}
    if ring_lines is not None:
        props["rings"] = [{"line": ln, "cue": clear_midpoint(bid, [cues_for(bid, [ph], narration, est(narration))[0] + 12])[0]}
                          for ln, ph in zip(ring_lines, ring_phrases)]
    return add(remotion(bid, act, narration, "CCPlainShell", props, show, motion_claim=motion_claim))


# ═════════════════════════════ ACT I · The Idea And Its Layers ═════════════════════════════
add(manim("B10", A1,
    "Here is the idea. You ask Slurm for a GPU. On that GPU you run an open model. And a coding agent, like Claude Code, sends it "
    "requests and runs tools on your files. There is no per-token bill, because the model is yours for as long as the job runs.",
    "B10_TheIdea",
    "A rack labelled 'GPU node' (explorer_rack) appears; an open-model block (a plain labelled block 'model') slides into it; a Claude logo chip (logo_chip('claude')) on the left sends small request arrows to the model and gets replies; a folder 'your files' sits beside the chip and a tool arrow touches it; a crossed-out price tag 'per token' fades at the top while a small clock 'job' ticks on the rack.",
    [{"at": 0.2, "event": "you ask for a GPU: the node appears"}, {"at": 0.45, "event": "the open model slides into it"}, {"at": 0.7, "event": "the agent sends requests and uses your files"}, {"at": 0.9, "event": "no per-token bill; the job clock ticks"}]))
add(manim("B11", A1,
    "There are three layers. The model host is Ollama, inside an Apptainer container, on a GPU node that Slurm gave you. The "
    "harness is the coding agent: Claude Code, Aider, or Continue. And the transport is whatever joins them: nothing, if they share a machine, or an S S H tunnel.",
    "B11_ThreeLayers",
    "Three horizontal bands stack from the bottom: 'model host' (a rack with a container box labelled 'Apptainer' holding a block 'ollama'), 'harness' (a Claude logo chip and two small mono chips 'aider' and 'continue'), 'transport' (a dashed line that reads 'nothing' when both are on one node and 'ssh tunnel' when they are apart). Bands build bottom to top on the spoken words.",
    [{"at": 0.2, "event": "model host band: Apptainer holding ollama"}, {"at": 0.5, "event": "harness band: Claude, aider, continue"}, {"at": 0.8, "event": "transport band: nothing, or an ssh tunnel"}]))
add(manim("B12", A1,
    "Pattern A keeps everything on the GPU node. The agent and the model run in the same job, so nothing crosses a network, and "
    "your code stays on Northeastern storage. Use it unless you have a specific reason not to.",
    "B12_PatternA",
    "One drawn job boundary (a rounded outline) labelled 'one GPU job' holding a Claude logo chip, an arrow to a block 'ollama' marked 'localhost', and a folder 'your repo'; outside the boundary a dotted network cloud with a small cross on the line leading to it ('nothing crosses'); a terracotta check lands on the boundary.",
    [{"at": 0.2, "event": "the job boundary with agent and model inside"}, {"at": 0.55, "event": "your repo inside too; nothing crosses the network"}, {"at": 0.88, "event": "the check: use this one"}]))
add(manim("B13", A1,
    "Pattern B keeps your editor on your laptop. Only the model's traffic goes to the cluster, through an S S H tunnel to the "
    "login node and on to the GPU node. So the model must be reachable from the login node, and that needs a lock in front of it.",
    "B13_PatternB",
    "Left to right: a laptop (Professor Bear portrait 1x1 beside a plain laptop slab) with a Claude logo chip, a drawn tunnel pipe labelled 'ssh tunnel', a small rack 'login node', a larger rack 'GPU node' whose door is a padlock (padlock()) in front of a block 'ollama'. A request packet travels laptop to login node to the lock and stops there until a key is shown.",
    [{"at": 0.2, "event": "the laptop: editor and agent stay home"}, {"at": 0.5, "event": "the tunnel to the login node, on to the GPU node"}, {"at": 0.85, "event": "the lock in front of the model"}]))

# ═════════════════════════════ ACT II · Wrong Turns To Avoid ═════════════════════════════
add(manim("B20", A2,
    "Advice that circulates about this setup has traps. First, the network. Ollama has no authentication, and its container image "
    "listens on every address by default. On a shared cluster that opens the whole interface, including pulling and deleting models, "
    "to anyone who can reach the node.",
    "B20_OpenDoor",
    "A GPU-node rack with a door standing open, a mono label '0.0.0.0' on the door; four small plain dots from 'other users' walk up and reach in to a block 'ollama' (one picks up a model block labelled 'pull', one carries one away labelled 'delete'); then the door swings closed to the label '127.0.0.1' and the dots stop outside. Real mono text only for the two addresses.",
    [{"at": 0.2, "event": "no authentication; the door stands open at 0.0.0.0"}, {"at": 0.6, "event": "others can pull and delete models"}, {"at": 0.9, "event": "the door closes to 127.0.0.1"}]))
shell("B21", A2,
    "Inside Apptainer, the image's own setting beats a plain export from your shell. So pass the address with the env flag: bound "
    "to localhost, on a random port. That is what the start script does.",
    "Wrong, then right  ·  from the script",
    ["# wrong: it listens on every address, and the image overrides it anyway",
     sq("export OLLAMA_HOST=0.0.0.0:11434"),
     "# right: localhost only, on a random port",
     sl('--env OLLAMA_HOST='),
     sl("# --env is required: the image sets", 96)],
    [None, "plain export", "So pass the address", "bound to local host", "That is what"],
    [{"at": 0.05, "event": "the wrong line"}, {"at": 0.4, "event": "the right line, ringed"}, {"at": 0.85, "event": "the script's own comment"}],
    ring_lines=[3], ring_phrases=["bound to local host"])
add(manim("B22", A2,
    "Second, the address. Claude Code adds slash v one slash messages itself, and the documented examples give a bare host and port. "
    "A base address that already ends in slash v one doubles the path, and the request fails. Give it the bare host and port.",
    "B22_BareBaseUrl",
    "A Claude logo chip on the left builds a request address from two pieces that slide together: the base 'http://127.0.0.1:PORT' (mono) and a suffix '/v1/messages' that the chip adds itself; with a base that already ends '/v1' the pieces collide into '/v1/v1/messages' and a '404' tag lands; with the bare base the address is right and a check lands.",
    [{"at": 0.15, "event": "the chip adds /v1/messages itself"}, {"at": 0.5, "event": "a base ending /v1 doubles it: 404"}, {"at": 0.85, "event": "the bare host and port: right"}]))
add(manim("B23", A2,
    "And the tunnel. Local host on the far side of a tunnel means the login node, not the machine running your model. The target "
    "has to be the compute node, because Research Computing does not support S S H straight into a GPU node.",
    "B23_TunnelTarget",
    "A laptop on the left, a pipe 'ssh -L' to a small rack 'login node' in the middle and a larger rack 'compute node' on the right with a block 'ollama'; a first pipe ending at the login node's 'localhost' is wrong (a cross: nothing there); a second pipe passes through the login node to the compute node: right (a check). A direct dashed line laptop to compute node is crossed out ('no direct ssh').",
    [{"at": 0.2, "event": "localhost on the far side is the login node"}, {"at": 0.55, "event": "the target is the compute node"}, {"at": 0.85, "event": "no direct ssh into a GPU node"}]))
add(manim("B24", A2,
    "Third, the model names. Claude Code uses its small model for background tasks, and a separate setting for subagents. Unless you "
    "point those at your local model, Ollama can be asked for Claude models it does not have. So the script sets the small, medium and large names, and the subagent model, to one local model.",
    "B24_AliasMap",
    "A Claude logo chip fans out four labelled arrows: 'haiku' (tagged 'background tasks'), 'sonnet', 'opus', 'subagent' (its own separate arrow). First they end at a block 'ollama' that answers 'model not found' on the ones that reach it (small cross tags); then all four arrows are redrawn to end at one block 'local model' (a single check), with the mono word 'every name'.",
    [{"at": 0.2, "event": "background tasks use the small model; subagents have their own setting"}, {"at": 0.5, "event": "unmapped: ollama has no such model"}, {"at": 0.85, "event": "all four mapped to one local model"}]))
add(manim("B25", A2,
    "Fourth, context. Ollama sizes its default window by video memory: four thousand tokens under twenty-four gigabytes, thirty-two "
    "thousand up to forty-eight. Claude Code's instructions and tool list alone overflow a small window, and the overflow is cut without any error. "
    "Ask for sixty-five thousand five hundred thirty-six or more.",
    "B25_SilentTruncation",
    "A horizontal window bar labelled 'context window' with tick labels 4k and 32k; stacked prompt blocks 'instructions', 'tools', 'your code' pour into it; the 4k bar fills at the first block and the rest are cut off at its edge, fading away silently (no error tag, a quiet gap); then the bar is redrawn at '65,536' and every block fits. Real mono for the number 65,536.",
    [{"at": 0.15, "event": "default windows: 4k and 32k"}, {"at": 0.5, "event": "instructions and tools overflow; the rest is cut, silently"}, {"at": 0.88, "event": "65,536: everything fits"}]))
add(manim("B26", A2,
    "Fifth, the model. A one-and-a-half-billion parameter reasoning model cannot reliably drive an agent loop with dozens of tool "
    "definitions. Use a tool-capable coding model, in the range of twenty to a hundred twenty billion parameters.",
    "B26_TooSmallModel",
    "Two model blocks side by side: a tiny block '1.5B' and a large block '20B to 120B'; a stack of small tool cards (dozens) is offered to each; the tiny block drops the stack (cards spill, a cross), the large block holds it and returns a check; a size ruler runs under both.",
    [{"at": 0.2, "event": "the tiny model loads"}, {"at": 0.55, "event": "it drops the pile of tool definitions"}, {"at": 0.85, "event": "the 20B to 120B model holds them"}]))
add(manim("B27", A2,
    "And drop the words zero marginal cost. GPU hours count against fair share, you wait in a queue, and an idle watcher cancels "
    "jobs. The accurate claim is no per-token billing. The cost moves to queue time, fair share, and capability.",
    "B27_NotFree",
    "A price tag 'per token' is crossed out and slides off; three new meters appear where it was: a queue line with a waiting clock 'queue', a gauge 'fair share' draining, and a small magnifier 'idle watcher'; a plaque 'no per-token billing' lands beneath them in place of 'free'.",
    [{"at": 0.2, "event": "'zero marginal cost' crossed out"}, {"at": 0.5, "event": "the queue, fair share and idle watcher appear"}, {"at": 0.85, "event": "the accurate claim: no per-token billing"}]))

# ═════════════════════════════ ACT III · One-Time Setup ═════════════════════════════
shell("B30", A3,
    "Setup starts with one small environment file. It says where the images, the models and the container cache live. The "
    "default is scratch, which is purged on the first Tuesday of every month. Model weights belong in project space, and on one real account scratch was not even writable.",
    "III · One-Time Setup  ·  env.sh, as written",
    [sl("# Storage."), sl('export LLM_ROOT='), sl('export OLLAMA_MODELS='), sl('export APPTAINER_CACHEDIR='),
     sl('export LLM_MODEL='), sl('export LLM_CONTEXT=')],
    [None, "The default is scratch", "the models", "container cache", "Model weights belong", "Model weights belong"],
    [{"at": 0.05, "event": "the storage comment"}, {"at": 0.4, "event": "LLM_ROOT, the scratch default, ringed"}, {"at": 0.8, "event": "model and context lines"}],
    ring_lines=[1, 0], ring_phrases=["scratch", "project space"])
add(manim("B31", A3,
    "Apptainer otherwise caches into a hidden folder in home, and home fills first. So point its cache and temporary folders at your "
    "own storage, and pull the images there, on a compute node rather than the login node.",
    "B31_HomeFills",
    "A drawn 'home' box with a small quota gauge filling from a hidden cache folder (a dotted '.apptainer' folder icon) until it is full (a cross); then two arrows redirect the cache and temp folders to a separate storage box labelled 'your storage'; below, a compute-node rack carries the pull (a container-image block travels to the storage box), the login node rack is crossed out for pulls.",
    [{"at": 0.2, "event": "the hidden cache fills home"}, {"at": 0.55, "event": "cache and temp redirected to your own storage"}, {"at": 0.85, "event": "the pull happens on a compute node"}]))
shell("B32", A3,
    "Then two pulls: Ollama, and a small web server called Caddy that the laptop pattern will need. Check the version it prints. "
    "You need zero point fourteen or later. And once something works, pin the version instead of latest, so a whole class does not drift.",
    "III · Pull the images  ·  on a compute node",
    [sl("source ~/.ollama-hpc/env.sh"), sl("mkdir -p"), sl('apptainer pull "$OLLAMA_SIF"'), sl('apptainer pull "$CADDY_SIF"'),
     sl('apptainer exec "$OLLAMA_SIF" ollama --version')],
    [None, "Then two pulls", "pulls", "caddy", "Check the version"],
    [{"at": 0.05, "event": "source the environment"}, {"at": 0.4, "event": "the two pulls; latest ringed"}, {"at": 0.8, "event": "the version check"}],
    ring_lines=[2, 4], ring_phrases=["latest", "Check the version"])
shell("B33", A3,
    "The start script runs inside every GPU job. It picks a random free port, binds Ollama to localhost only, sets the context length, "
    "and defines an ollama function that talks to your server, not the container's default port.",
    "III · The start script  ·  inside every GPU job",
    [sl("export OLLAMA_PORT=", 100), sl("apptainer exec --nv -B"), sl('--env OLLAMA_HOST='), sl('--env OLLAMA_CONTEXT_LENGTH'),
     sl("--env OLLAMA_NUM_PARALLEL"), sl("ollama() {")],
    [None, "random free port", "to localhost only", "sets the context length", "sets the context length", "defines an"],
    [{"at": 0.05, "event": "the random port"}, {"at": 0.4, "event": "localhost and the context length"}, {"at": 0.85, "event": "the ollama function"}],
    ring_lines=[2, 3], ring_phrases=["localhost only", "context length"])
shell("B34", A3,
    "The Claude Code script sets the base address to your port, a placeholder token, and every model alias to your local model. Look "
    "at the first line. It clears any real API key, which would otherwise be sent to whatever is listening at that address.",
    "III · Claude Code script  ·  claude-local.sh",
    [sl("unset ANTHROPIC_API_KEY"), sl("export ANTHROPIC_BASE_URL="), sl("export ANTHROPIC_AUTH_TOKEN="), sl("export ANTHROPIC_MODEL="),
     sl("export ANTHROPIC_DEFAULT_HAIKU_MODEL="), sl("export CLAUDE_CODE_SUBAGENT_MODEL=")],
    [None, "base address", "placeholder token", "local model", "every model alias", "every model alias"],
    [{"at": 0.05, "event": "unset the real key"}, {"at": 0.35, "event": "base address and token"}, {"at": 0.8, "event": "aliases and the subagent model"}],
    ring_lines=[0], ring_phrases=["clears any real API key"])
shell("B35", A3,
    "Pattern B needs one persistent token: a random number kept in a file only you can read. Regenerate it any time to revoke "
    "access. Then leave the setup node, and install Claude Code on the login node. It is a small download.",
    "III · A token, then Claude Code",
    [sl("openssl rand -hex 32"), sl("exit", exact=True), sl("curl -fsSL https://claude.ai/install.sh"),
     sl("echo 'export PATH=")],
    [None, "Then leave the setup node", "install clod code|install claude code", "small download"],
    [{"at": 0.05, "event": "the token, readable only by you"}, {"at": 0.5, "event": "leave the setup node"}, {"at": 0.8, "event": "install Claude Code"}],
    ring_lines=[0], ring_phrases=["only you can read"])

# ═════════════════════════════ ACT IV · Choose A GPU And A Model ═════════════════════════════
add(manim("B40", A4,
    "Two numbers decide whether this works. The model's weights must fit in video memory, and there must be room left for the "
    "context window's cache. If either spills over, Ollama pushes layers onto the processor, and generation slows to a crawl.",
    "B40_FitInVram",
    "A tall tank labelled 'video memory'; a block 'weights' sinks in, then a second block 'context cache' stacks on it; both fit with room to spare (a check). Then a bigger cache block overflows the tank top and the spilled part drops onto a small chip labelled 'processor'; a stopwatch beside it slows (hand barely moves) with the word 'crawl'.",
    [{"at": 0.2, "event": "weights fit in video memory"}, {"at": 0.5, "event": "plus the context cache: still fits"}, {"at": 0.8, "event": "too big: layers spill to the processor, a crawl"}]))
add(manim("B41", A4,
    "Models that fit, by download size. The twenty-billion G P T O S S is about fourteen gigabytes. The thirty-billion Qwen three Coder "
    "is about nineteen. G L M four point seven flash is also about nineteen to download, but Ollama puts it near twenty-three of video "
    "memory at sixty-four thousand context.",
    "B41_ModelsThatFit",
    "A horizontal bar chart with three bars on a gigabyte ruler: 'gpt-oss 20b' about 14, 'qwen3-coder 30b' about 19, 'glm-4.7-flash' about 19 to download with a second, hatched extension to about 23 tagged 'video memory at 64k context'. Bars grow on the spoken numbers.",
    [{"at": 0.2, "event": "gpt-oss 20b: about 14 GB"}, {"at": 0.45, "event": "qwen3-coder 30b: about 19 GB"}, {"at": 0.75, "event": "glm-4.7-flash: 19 GB download, about 23 GB of video memory at 64k"}], sparse=False))
add(manim("B42", A4,
    "And the hundred-twenty-billion G P T O S S, about sixty-five gigabytes, is the strongest of these that fits on one card. Before "
    "you pull any model, check its page for the tools label. A model without tool support prints tool calls as plain text instead of running them.",
    "B42_StrongestAndTools",
    "A single long bar 'gpt-oss 120b' about 65 on a gigabyte ruler, ringed as 'strongest on one card'; then two small model cards side by side: one stamped 'tools' that runs a tool call (a gear turns, a check), one without the stamp that prints the call as plain text spilling across the card (a cross).",
    [{"at": 0.2, "event": "gpt-oss 120b: about 65 GB, the strongest on one card"}, {"at": 0.6, "event": "a model with the tools label runs the call"}, {"at": 0.88, "event": "without it, the call prints as plain text"}]))
add(manim("B43", A4,
    "The gpu partition gives one GPU per job, so stay inside one card. An H two hundred has about a hundred forty gigabytes, and every "
    "model on that list fits with room for a large context. Older cards like V one hundred and T four may fall back to the processor, so check the log, and ask for a newer type.",
    "B43_OneGpuPerJob",
    "A rack labelled 'gpu partition' with five GPU slots labelled by type 'v100', 'a100', 'h200', 't4' (types as listed on Explorer: v100-sxm2, v100-pcie, a100, h200, t4); a request chip '--gres=gpu:h200:1' (mono) picks the h200 slot (tagged 'about 140 GB') and the model blocks from the previous beats all slot into it with room left; the v100 and t4 slots get a small caution mark 'may fall back to CPU'.",
    [{"at": 0.2, "event": "one GPU per job"}, {"at": 0.5, "event": "the h200 slot, about 140 GB, takes every model"}, {"at": 0.85, "event": "v100 and t4: may fall back to the processor"}]))
add(manim("B44", A4,
    "On context, sixty-five thousand is the floor for coding agents, and on an H two hundred you can raise it for long sessions. If "
    "memory is tight, storing the cache at eight bits roughly halves its size, at a small cost in quality.",
    "B44_ContextKnobs",
    "Two cache blocks on a memory ruler: a tall one labelled '65,536' and a taller one '131,072'; a mono knob 'OLLAMA_KV_CACHE_TYPE=q8_0' turns and the tall block visibly halves in height, with a small 'small quality cost' tag.",
    [{"at": 0.2, "event": "65,536 is the floor; 131,072 on an h200"}, {"at": 0.6, "event": "the q8_0 knob halves the cache"}, {"at": 0.88, "event": "a small quality cost"}]))

# ═════════════════════════════ ACT V · Pattern A, On The GPU Node ═════════════════════════════
shell("B50", A5,
    "Start with an interactive GPU session. The gpu-interactive partition defaults to one hour, allows two, and gives one GPU. "
    "Asking for a specific type can lengthen the wait. And consider tmux first, so a dropped connection does not kill your session.",
    "V · Pattern A  ·  an interactive GPU session",
    [sl("tmux new -s llm"), sl("srun --partition=gpu-interactive", 104),
     "# gpu-interactive: one hour by default, two at most, one GPU",
     "# a specific GPU type can lengthen the wait"],
    [None, "interactive partition", "defaults to one hour", "Asking for a specific type"],
    [{"at": 0.05, "event": "tmux first"}, {"at": 0.35, "event": "the srun line"}, {"at": 0.75, "event": "limits and the wait"}],
    ring_lines=[1], ring_phrases=["defaults to one hour"], fs=26)
shell("B51", A5,
    "Source the start script, pull the model, then prove it. Send one message to the Anthropic-compatible address, and run "
    "ollama p s. The processor should read a hundred percent GPU, and the context should match what you asked for.",
    "V · Start Ollama, pull the model, prove it",
    [sl("source ~/.ollama-hpc/start-ollama.sh", exact=True), sl('ollama pull "$LLM_MODEL"'), sl('curl -s "http://127.0.0.1:$OLLAMA_PORT/v1/messages"', 100),
     sl("ollama ps", exact=True), "# PROCESSOR should read 100% GPU", "# CONTEXT should match LLM_CONTEXT"],
    [None, "pull the model", "Send one message", "run olama ps|run ollama ps", "processor should read", "context should match"],
    [{"at": 0.05, "event": "start Ollama"}, {"at": 0.3, "event": "pull the model"}, {"at": 0.55, "event": "the test message"}, {"at": 0.8, "event": "ollama ps: what it should read"}],
    ring_lines=[4, 5], ring_phrases=["processor should read", "context should match"])
shell("B52", A5,
    "Configure Claude Code for this session, go to your project, and start it. Inside, run slash status to confirm it is using "
    "your local address and not Anthropic's.",
    "V · Claude Code, pointed at your model",
    [sl("source ~/.ollama-hpc/claude-local.sh", exact=True), sl("cd ~/path/to/your/repo", exact=True), sl("claude", exact=True),
     "/status", "# confirm the base URL is your local address, not Anthropic's"],
    [None, "go to your project", "start it", "slash status", "your local address"],
    [{"at": 0.05, "event": "configure the session"}, {"at": 0.4, "event": "go to the project and start it"}, {"at": 0.8, "event": "slash status"}],
    ring_lines=[3], ring_phrases=["slash status"])
add(manim("B53", A5,
    "Know the limits. Anthropic's documentation says it does not support pointing Claude Code at non-Claude models, so this works "
    "through documented settings but is an unsupported route. Claude Code's built-in web search runs on Anthropic's own backend, and Ollama's "
    "layer does not fully support hosted web search. Prompt caching is not supported either.",
    "B53_UnsupportedRoute",
    "A Claude logo chip on the left with four capability chips beneath: 'edit files' and 'run tools' ticked; 'web search' (tagged 'runs on anthropic's backend') and 'prompt caching' crossed. A road drawn from the chip to a block 'local model' carries a small sign 'documented settings, unsupported route'.",
    [{"at": 0.15, "event": "an unsupported route, through documented settings"}, {"at": 0.5, "event": "web search runs on Anthropic's backend"}, {"at": 0.85, "event": "prompt caching is not supported"}]))
add(manim("B54", A5,
    "So long sessions slow down as the context grows, because nothing is cached. Keep tool servers few, since every definition uses "
    "context. And when you finish, exit twice: Claude Code, then the job, which returns the GPU.",
    "B54_ContextGrowsThenExit",
    "A context bar beside a Claude logo chip grows turn by turn as small 'tool definition' blocks stack up and a stopwatch slows; two tool-server chips are crossed down to one; then two exit arrows leave in order 'Claude Code' then 'the job', and the GPU rack beside them dims.",
    [{"at": 0.2, "event": "the context grows turn by turn; the session slows"}, {"at": 0.5, "event": "fewer tool servers, less context used"}, {"at": 0.85, "event": "exit twice: Claude Code, then the job"}]))
shell("B55", A5,
    "For unattended work, run Claude Code headless inside a batch job. The GPU stays busy for the whole job, so the idle watcher "
    "leaves it alone. Put the repository on a fresh branch, and review the diff before you merge anything. Accept edits lets it change files, and simple file commands like move and remove, inside the project; other commands still need permission.",
    "V · Headless, inside a batch job",
    ["#SBATCH --partition=gpu", sl("#SBATCH --gres=gpu:h200:1"), sl("#SBATCH --time=02:00:00"),
     sl("source ~/.ollama-hpc/start-ollama.sh || exit 1"), sl("claude -p")],
    [None, "inside a batch job", "inside a batch job", "headless", "except edits|accept edits"],
    [{"at": 0.05, "event": "the batch header"}, {"at": 0.45, "event": "start the model in the job"}, {"at": 0.85, "event": "claude -p with accept edits"}],
    ring_lines=[4], ring_phrases=["except edits|accept edits"])

# ═════════════════════════════ ACT VI · Pattern B, From Your Laptop ═════════════════════════════
add(manim("B60", A6,
    "Pattern B needs a lock. The laptop reaches the node through the login node, so something has to listen on the node's cluster "
    "network. Ollama stays on localhost. A small web server, Caddy, listens instead, and rejects every request that does not carry your bearer token.",
    "B60_LockInFront",
    "A GPU-node rack with a gate drawn in front of a block 'ollama' (which stays on 'localhost'); the gate is a block labelled 'caddy' with a padlock. A request packet with a key-shaped token (key_obj) passes through to 'ollama'; a second packet with no token stops at the gate and a '401' tag lands.",
    [{"at": 0.2, "event": "ollama stays on localhost"}, {"at": 0.5, "event": "caddy listens in front, with a lock"}, {"at": 0.85, "event": "the packet with the token passes; the other is refused"}]))
shell("B61", A6,
    "Here is the proxy's whole rulebook. Requests with the right header go through to Ollama. Everything else gets a four-oh-one. And "
    "the admin interface is switched off, because it would open yet another port with no lock.",
    "VI · The proxy's rulebook  ·  the Caddyfile",
    [sl("admin off"), sl(":${PROXY_PORT} {"), sl("@authorized header Authorization", 96), sl("reverse_proxy 127.0.0.1:"),
     sl('respond "unauthorized" 401')],
    [None, "right header", "right header", "go through to", "Everything else"],
    [{"at": 0.05, "event": "admin off"}, {"at": 0.4, "event": "the header rule and the pass-through"}, {"at": 0.8, "event": "everything else: 401"}],
    ring_lines=[0, 4], ring_phrases=["admin interface", "401"])
shell("B62", A6,
    "On your laptop, a small script reads which node your job landed on, checks that the job is still running, writes a private "
    "environment file, and opens the tunnel. The local port is eleven four three five, so it does not collide with an Ollama on your laptop.",
    "VI · On the laptop  ·  the tunnel",
    [sl("Host explorer", exact=True), sl("ControlMaster auto"), sl('STATE="$(ssh'), sl('exec ssh -N -L'), sl("~/bin/explorer-llm", exact=True)],
    [None, "reads which node", "checks that the job", "opens the tunnel", "local port"],
    [{"at": 0.05, "event": "the ssh host entry"}, {"at": 0.4, "event": "the job-state check"}, {"at": 0.8, "event": "the tunnel and the script"}],
    ring_lines=[3], ring_phrases=["opens the tunnel"])
shell("B63", A6,
    "Check the lock. The first command should print four-oh-one, because it carries no token. The second sends your token and should "
    "return a short message. Then start Claude Code from your project in that same terminal.",
    "VI · Check the lock  ·  then start Claude Code",
    [sl('source ~/.explorer-llm.env && curl -s -o /dev/null', 104), "# expect: 401", sl('source ~/.explorer-llm.env && curl -s "$ANTHROPIC_BASE_URL/v1/messages"', 104),
     "# expect: a short message", sl("source ~/.explorer-llm.env && claude", exact=True)],
    [None, "401", "sends your token", "short message", "Then start"],
    [{"at": 0.05, "event": "no token: expect 401"}, {"at": 0.45, "event": "with the token: a short message"}, {"at": 0.85, "event": "start Claude Code"}],
    ring_lines=[1, 3], ring_phrases=["401", "short message"])
add(manim("B64", A6,
    "Two risks remain. The proxy blocks the rest of the cluster, but Ollama's own random port is still reachable by other users on "
    "the same node. A random port is obscurity, not security. And your token sits in plain text on your laptop. When you finish, cancel the job.",
    "B64_TwoRisks",
    "The GPU-node rack with the caddy gate and ollama behind it; small dots of 'other users' on the same rack reach the random port beside the gate, bypassing it (a caution mark: 'obscurity, not security'); a laptop with a file 'token' marked 'plain text' (padlock open) in the corner; finally a mono line 'scancel --name=ollama-serve' stamps and the rack dims.",
    [{"at": 0.2, "event": "others on the same node can reach the random port"}, {"at": 0.5, "event": "the token sits in plain text on the laptop"}, {"at": 0.85, "event": "cancel the job; the node dims"}]))

# ═════════════════════════════ ACT VII · Other Coding Agents ═════════════════════════════
shell("B70", A7,
    "Aider on the node: use the ollama underscore chat prefix. From the laptop, through the proxy, use its OpenAI-compatible mode, "
    "because its Ollama provider does not send a bearer token. A warning about an unknown context window is harmless. The server enforces it.",
    "VII · Other Coding Agents  ·  Aider",
    ["# on the node", sl('export OLLAMA_API_BASE=', 100), "# from the laptop, through the proxy",
     sl("source ~/.explorer-llm.env && aider --model", 100)],
    [None, "on the node", "From the laptop", "compatible mode"],
    [{"at": 0.05, "event": "on the node: the ollama_chat prefix"}, {"at": 0.5, "event": "from the laptop: OpenAI-compatible mode"}],
    ring_lines=[1, 3], ring_phrases=["underscore chat", "compatible mode"])
shell("B71", A7,
    "Continue, in VS Code or JetBrains, takes the same endpoint in a YAML file. Paste your token where it says so. The roles are "
    "chat, edit and apply.",
    "VII · Continue  ·  config.yaml",
    ["~/.continue/config.yaml", sl("name: Explorer LLM", exact=True), sl("provider: openai"), sl("model: qwen3-coder:30b"),
     sl("apiBase:"), sl("apiKey:"), sl("roles:")],
    [None, "takes the same endpoint", "takes the same endpoint", "YAML file", "same endpoint", "Paste your token", "chat, edit and apply"],
    [{"at": 0.05, "event": "the file"}, {"at": 0.4, "event": "the endpoint and the token"}, {"at": 0.8, "event": "the roles"}],
    ring_lines=[5], ring_phrases=["Paste your token"])
add(manim("B72", A7,
    "Codex, OpenCode and Droid can be set up by the ollama launch command, but only when Ollama is on the same machine at its default "
    "port. Here the port is random, and behind a token in Pattern B. So set them up as OpenAI-compatible providers, and follow each tool's current instructions.",
    "B72_LaunchDefaults",
    "A box labelled 'ollama launch' (mono) with a line to three mono tool chips 'codex', 'opencode', 'droid'; it works only when the model sits at a plain 'localhost:11434' slot (a check); on Explorer the model block sits at a randomised port and behind a lock, the line breaks (cross); a second route is drawn: the three chips each connect with a key to an 'openai-compatible' socket on the model block.",
    [{"at": 0.2, "event": "ollama launch sets tools up at the default port"}, {"at": 0.55, "event": "here the port is random and locked: it breaks"}, {"at": 0.85, "event": "OpenAI-compatible providers instead"}]))

# ═════════════════════════════ ACT VIII · When It Breaks ═════════════════════════════
add(manim("B80", A8,
    "Four failures cover most trouble. A four-oh-four on every request: the base address ends in slash v one. A Claude model name "
    "not found: the aliases are not mapped. Tool calls printed as raw text: the model has no tools label. And a split between processor and GPU: the model or the window is too big.",
    "B80_FourFailures",
    "A drawn two-column table builds row by row: symptom chips on the left ('404 on every request', 'claude model not found', 'tool calls as raw text', 'CPU/GPU split') each paired on the right with its cause chip ('base URL ends /v1', 'aliases not mapped', 'no tools label', 'too big'); each cause is ringed in terracotta as it lands.",
    [{"at": 0.15, "event": "404: the base address ends in /v1"}, {"at": 0.4, "event": "model not found: aliases not mapped"}, {"at": 0.65, "event": "raw text tool calls: no tools label"}, {"at": 0.88, "event": "CPU/GPU split: too big"}], sparse=False))
add(manim("B81", A8,
    "Three more. A full home folder: the image cache or the models defaulted to home. A pull that fails on a compute node: no outbound "
    "network. On Explorer, a default module sets the proxy that nodes use. If a script begins with module purge, it loses that proxy, so load the module again right after.",
    "B81_ProxyAndModulePurge",
    "A home box with a full gauge appears first; then a compute-node rack with a pipe to 'internet' passing through a small gate labelled 'proxy' set by a module chip 'explorer'; 'module purge' (mono) sweeps the chip off and the pipe breaks (a pull fails: cross); 'module load explorer' puts the chip back and the pipe reconnects (check); a small stamp 'from Research Computing's pages' sits on the corner.",
    [{"at": 0.15, "event": "home is full: cache and models defaulted to home"}, {"at": 0.45, "event": "a pull fails: no outbound network"}, {"at": 0.65, "event": "module purge removes the proxy module"}, {"at": 0.9, "event": "load it again right after"}]))
shell("B82", A8,
    "And one more trap. Those same proxy settings can get in the way when you talk to your own local server. Research Computing's own "
    "post on running Ollama tells you to unset the proxy variables before you do.",
    "VIII · The proxy  ·  from Research Computing pages",
    ["# module purge also removes the proxy module", "module purge", "module load explorer",
     "# talking to a local server: unset the proxy variables first", "unset http_proxy https_proxy"],
    [None, None, None, "same proxy settings", "unset the proxy variables"],
    [{"at": 0.05, "event": "the purge and the reload"}, {"at": 0.5, "event": "the proxy settings can intercept a local call"}, {"at": 0.85, "event": "unset the proxy variables"}],
    ring_lines=[4], ring_phrases=["unset the proxy variables"])
# ═════════════════════════════ ACT IX · The Cluster's Rules ═════════════════════════════
add(manim("B90", A9,
    "Explorer runs a watcher for idle GPUs. Under-use for fifteen minutes earns an email. Under-use for an hour gets the job cancelled. "
    "Coding is bursty, with long gaps while you read, so a session you walk away from will be flagged. Never add filler work to keep it alive. Start when you sit down, cancel when you stop, and put long unattended work in batch jobs.",
    "B90_IdleWatcher",
    "A GPU-utilisation line with bursts and long flat gaps along a time axis; a watcher marker 'idle watcher' sweeps the flat part; at '15 min' an envelope 'email' lands; at '1 hour' the job box is cancelled (x_mark); a filler-load block 'filler work' is shown and crossed out; two small marks at the end: 'sit down: start', 'stop: cancel'.",
    [{"at": 0.15, "event": "bursty use with long gaps"}, {"at": 0.35, "event": "15 minutes: an email"}, {"at": 0.52, "event": "1 hour: the job is cancelled"}, {"at": 0.72, "event": "no filler work"}, {"at": 0.9, "event": "start when you sit down, cancel when you stop"}]))
add(manim("B91", A9,
    "Now the shared endpoint for a whole class. A Slurm job has a time limit, eight hours on the gpu partition, so an endpoint built on "
    "one dies on a schedule and returns on a different node. Between requests the GPU idles. And Ollama serves one person well: five students at sixty-four thousand context cost roughly five times the cache memory.",
    "B91_NotAJobsShape",
    "A rack with a clock dial running to '8 h'; at the end the rack fades and a new rack appears at a different position with a new address label; below, a single user's cache block grows into five stacked cache blocks labelled by five small student dots, and the memory tank beside them fills to the top ('about 5x').",
    [{"at": 0.2, "event": "the 8-hour limit ends the endpoint"}, {"at": 0.45, "event": "it returns on a different node"}, {"at": 0.75, "event": "five students: about five times the cache"}]))
add(manim("B92", A9,
    "A service for many people would usually use vLLM, which batches concurrent requests and supports API keys, though its own documentation says not to rely on a key alone. And other people's code "
    "and prompts would then pass through a service you run. That raises questions about logging, retention, and who is responsible when it breaks. Those are questions for Research Computing, not settings.",
    "B92_SharedService",
    "A server block labelled 'vllm' with a batching conveyor (several small prompt pages merge into one batch) and a key per user; the prompt pages carry small padlocks; three question chips float above the server: 'logging?', 'retention?', 'who owns it?'; a plaque 'a question for Research Computing' lands under them.",
    [{"at": 0.2, "event": "vllm batches many requests"}, {"at": 0.55, "event": "others' prompts pass through your service"}, {"at": 0.85, "event": "logging, retention, ownership: ask Research Computing"}]))
shell("B93", A9,
    "So ask. Five questions. Is one person's interactive session in a GPU job acceptable? Is S S H port forwarding from a login node "
    "permitted? May a process listen on the node's network behind a token proxy? What is the preferred route for a cohort? And where should model weights live?",
    "IX · Ask Research Computing  ·  five questions",
    [sl("1. Running Ollama inside", 100), sl("2. SSH local port forwarding", 100), sl("3. A process in my job may listen", 100),
     sl("4. For a shared endpoint", 100), sl("5. The preferred storage location", 100)],
    [None, "port forwarding", "May a process listen", "preferred route", "where should"],
    [{"at": 0.05, "event": "question one"}, {"at": 0.35, "event": "forwarding and listening"}, {"at": 0.8, "event": "the cohort route and the storage"}],
    ring_lines=[1, 3], ring_phrases=["port forwarding", "preferred route"])
add(manim("B94", A9,
    "On AICR, the newer AI Compute Resource cluster, there are two hundred forty-eight B two hundred and one hundred fifty-two RTX Pro "
    "GPUs, and access is by proposal. Research Computing says to develop and test on Explorer first. Whether AICR's idle rules treat a standing service differently is a question only Research Computing can answer.",
    "B94_AicrScale",
    "Two rack groups side by side: the Explorer rack (explorer_rack) labelled 'Explorer' and a larger grid (aicr_rack) labelled 'AICR' with two labelled blocks of GPU slots 'B200 x 248' and 'RTX Pro x 152'; a key-and-paper chip 'proposal' beside AICR; a question mark over a service block 'standing service' linking the two racks, ringed as 'ask Research Computing'.",
    [{"at": 0.2, "event": "AICR: 248 B200 and 152 RTX Pro"}, {"at": 0.5, "event": "access by proposal"}, {"at": 0.85, "event": "a standing service: ask Research Computing"}]))
add(manim("B95", A9,
    "Here is what we have and have not checked. We have not run this whole setup from start to finish. We did check, with read-only "
    "commands on Explorer, the partitions, that an H two hundred type exists, that Apptainer is on the login node, that the proxy comes from a default module, and that one account's scratch folder was not writable. Research Computing has a post on running Ollama in a container, but no page we read covers coding agents or says whether automated agents are allowed.",
    "B95_CheckedVsDocumented",
    "Two columns of plain stamped items. Left 'documented' (not run here): the scripts, the tunnel, the proxy, the harness settings. Right 'checked on Explorer' (read-only): 'partitions', 'h200 type exists', 'apptainer on the login node', 'proxy from a default module', 'scratch not writable on one account'. Underneath, one ringed chip: 'agent access: not stated by any policy page'. Stamps land on the spoken words.",
    [{"at": 0.15, "event": "not run start to finish"}, {"at": 0.4, "event": "the five read-only checks stamp in"}, {"at": 0.85, "event": "no policy page says agents are allowed"}], sparse=False))

# ═════════════════════════════ ACT X · What To Expect ═════════════════════════════
add(manim("B100", A10,
    "Expect a weaker agent. Models in this range are capable, but Claude Code's loop is demanding: a long system prompt, dozens of "
    "tool definitions, and a growing history on every turn. Expect more malformed tool calls, more loops, and an earlier loss of the thread on big changes across many files.",
    "B100_WeakerAgent",
    "A context bar fills turn by turn with three block types stacking ('system prompt', 'tool definitions', 'history'); a small agent loop (a Claude logo chip with a circular arrow) turns; glitch marks appear on its tool-call arrows (a malformed call, a repeat) and a thread line from the start frays toward the end of the bar.",
    [{"at": 0.2, "event": "a long prompt, tool definitions, growing history"}, {"at": 0.55, "event": "malformed calls and loops"}, {"at": 0.88, "event": "the thread frays on big multi-file changes"}]))
add(manim("B101", A10,
    "Where it does well: clear tasks with clear tests, bulk work over many files in batch jobs, code that should not leave "
    "Northeastern, and teaching how a smaller model differs from a frontier one. Where it does poorly: open-ended refactors, long debugging across a large codebase, and anything where one wrong tool call is expensive.",
    "B101_WhereItWorks",
    "Two columns. Left, 'does well' with four chips and a check each: 'clear tasks, clear tests', 'bulk batch work', 'stays on Northeastern', 'teaching'. Right, 'does poorly' with three chips and a small cross each: 'open-ended refactors', 'long debugging', 'costly wrong calls'. Chips land on the spoken items.",
    [{"at": 0.15, "event": "does well: tasks with tests, batch, stays here, teaching"}, {"at": 0.6, "event": "does poorly: open refactors, long debugging, costly calls"}], sparse=False))
add(manim("B102", A10,
    "A practical split: the local model for drafting, boilerplate, tests and batch passes, and frontier credits for the hard problems. "
    "Measured that way, the savings are real. Measured as the same thing for free, they are not.",
    "B102_PracticalSplit",
    "A conveyor of work boxes: many small boxes 'drafts', 'boilerplate', 'tests', 'batch' roll to the local-model rack; one heavy box 'hard problem' goes to a Claude logo chip; two receipts at the end: 'real savings' with a check on the split, and 'same thing, free' crossed out.",
    [{"at": 0.2, "event": "small work goes to the local model"}, {"at": 0.5, "event": "the hard problem goes to the frontier model"}, {"at": 0.85, "event": "real savings; not the same thing for free"}]))

# ═════════════════════════════ ACT XI · Get Started ═════════════════════════════
add(manim("B110", A11,
    "To try it, go to the hpc dash aicr repository on GitHub. In the skills folder, under local L L M on Explorer, there is a "
    "get-started recipe. The link is in the description.",
    "B110_WhereToGetStarted",
    "The repository address github.com/nikbearbrown/hpc-aicr appears in mono; a chain opens beneath it: skills/ then local-llm-on-explorer/ then one document page labelled GET-STARTED.md (a plain page with handwriting lines).",
    [{"at": 0.2, "event": "the repository address"}, {"at": 0.5, "event": "skills/ then local-llm-on-explorer/ open one under the other"}, {"at": 0.85, "event": "the get-started page lands"}]))
shell("B111", A11,
    "Clone it, start Claude Code inside it, and paste the prompt at the top of that file. Claude Code then guides you step by "
    "step, and asks before every file it writes and every job it submits. It has not been run end to end yet, so expect to help it fix something.",
    "Clone it, start Claude Code, paste the prompt",
    [gl("git clone https://github.com/nikbearbrown/hpc-aicr.git"), gl("cd hpc-aicr"), gl("claude"),
     "# then paste the prompt at the top of skills/local-llm-on-explorer/GET-STARTED.md",
     "# it asks before every file it writes and every job it submits"],
    [None, "Clone it", "start clod code|start claude code", "paste the prompt", "asks before every"],
    [{"at": 0.05, "event": "git clone and cd"}, {"at": 0.4, "event": "claude, then paste the prompt"}, {"at": 0.8, "event": "it asks before every file and every job"}],
    ring_lines=[3], ring_phrases=["paste the prompt"])

# ───────────────────────────── the closing three ─────────────────────────────
RECAP = ["A local model runs inside a GPU job you ask for, with no per-token billing.",
         "Pattern A keeps the model and the agent on one node; Pattern B adds a tunnel and a token lock.",
         "Bind to localhost, use the bare base address, map every alias, and set the context window high.",
         "Pick a tool-capable model that fits video memory with room for the context.",
         "Idle GPUs are cancelled, so start when you sit down and cancel when you stop.",
         "A shared endpoint for a class is a question for Research Computing, not a setting."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. A local model runs inside a GPU job you ask for, with no per-token billing. Pattern A keeps the model "
    "and the agent on one node. Pattern B adds a tunnel and a token lock. Bind to localhost, use the bare base address, map every alias, and set the context window high. "
    "Pick a tool-capable model that fits video memory with room for the context. Idle GPUs are cancelled, so start when you sit down and cancel when you stop. And a shared endpoint for a class is a question for Research Computing, not a setting.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land in narration order"}],
    lane="bookend", lead_silence_s=0.5,
    qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("I want to run a local model on Explorer for coding. Walk me through choosing between Pattern A and Pattern B. "
             "List which commands run on my computer and which on the cluster, which ones would submit a job, and the five questions "
             "I should ask Research Computing first. Do not run anything on any cluster.")
YT_SPOKEN = ("I want to run a local model on Explorer for coding. Walk me through choosing between Pattern A and Pattern B. "
             "List which commands run on my computer and which on the cluster, which ones would submit a job, and the five questions "
             "I should ask Research Computing first. Do not run anything on any cluster.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_SPOKEN + " Then check two things yourself. Did Claude run nothing on a cluster? "
    "And did it say what it could not confirm?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Plan Before You Submit", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did Claude run nothing on a cluster? It should only plan and explain.",
                "Check: did it say what it could not confirm, such as whether agent access is allowed?"],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": "Running a Local L L M on Explorer. At Nik Bear Brown.", "estimated_duration_s": 5.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Running a Local L L M on Explorer. How to run an open model on a cluster GPU "
                           "and point a coding agent like Claude Code at it, what that saves, and what it really costs.",
         "estimated_duration_s": 14.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · LOCAL MODELS", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German (Hallo)",
    "audience": "A researcher who wants to run an open model on an Explorer GPU and point a coding agent such as Claude Code at it; assumes no other film or book",
    "source_doc": "hpc-aicr/Running-a-Local-LLM-on-Northeastern's Explorer-Cluster-and-Pointing-Coding-Agents-at-It/explorer-local-llm-tutorial.md (read in full; scripts shown verbatim) plus HPC.md for the real checks",
    "playlist": "Northeastern HPC and AICR", "chapter_number": 11,
    "series_title": "Research Computing on Explorer and AICR",
    "lecture_opening_description": "Point Claude Code at a model on a cluster GPU",
    "lecture_opening_title_lines": ["Running a Local LLM", "on Explorer"],
    "tags": ["Ollama", "Apptainer", "Slurm", "Claude Code", "Aider", "Continue", "local LLM", "open-weight model", "GPU", "Explorer", "AICR",
             "Northeastern University", "Research Computing", "HPC", "Nik Bear Brown"]},
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
