#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-intro-to-explorer-ood.

LECTURE (brutalist.art/skills/make/lecture/SKILL.md). Source: hpc/Intro-to-Explorer-OOD-2026/Intro_explorer_ood.md
(Northeastern Research Computing training "Introduction to Explorer and the OOD", presenter Serena Caplins;
github.com/northeastern-rc-training/Intro-to-Explorer-OOD-2026). The training's own screenshots of the real
Open OnDemand site are the captures (SHOW-THE-THING rung 1, human-supplied). Third film of the series; same cast.
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Intro to Explorer and OOD"
CAP = "lecture-explorer-ood"
FPS = 30
SPARSE = ("lecture, drawn lane (show-tell drawing laws): one drawn scene on a cream stage with a few labels, the voice "
          "carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply.")


def manim(bid, act, narration, cls, image, show, sparse=True):
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


def shell(bid, act, narration, lines, show, start=20, gap=40, title="ssh — login.explorer.northeastern.edu"):
    return remotion(bid, act, narration, "CCPlainShell", {"title": title, "lines": lines, "startCue": start, "lineGap": gap}, show,
                    motion_claim="The real commands and the training's own output land in order.")


# The training's screenshots include the browser's own tab/address strip. BrowserCapture supplies its own chrome, and GATE T
# read the strip's grey-on-black text as unreadable type, so each image is cropped by this fraction of its height (captures/orig
# keeps the originals). Ring and focus coordinates below are written against the UNCROPPED image and converted here.
CROP = {"screenshot_OOD.png": 0.075, "screenshot_files1.png": 0.113, "screenshot_files2.png": 0.113, "screenshot_files3.png": 0.113,
        "screenshot_rstudio.png": 0.045, "screenshot_rstudio3.png": 0.0, "screenshot_jobs.png": 0.07, "screenshot_jobs2.png": 0.07}


def capture(bid, act, narration, image, aspect, moves, show, caption="The training's own screenshot of the real site"):
    c = CROP.get(image, 0.0)
    mv = []
    for m in moves:
        m = dict(m)
        m["y"] = round(min(1.0, max(0.0, (m.get("y", 0.5) - c) / (1 - c))), 3)
        if "ring" in m:
            x, y, w, h = m["ring"]
            # pad the ring clear of the text it frames: GATE T merges a stroke that touches type into the text blob
            x, y, w, h = x - 0.02, y - 0.03, w + 0.04, h + 0.06
            m["ring"] = [round(x, 3), round((y - c) / (1 - c), 3), round(w, 3), round(h / (1 - c), 3)]
        mv.append(m)
    return remotion(bid, act, narration, "BrowserCapture",
                    {"url": "ood.explorer.northeastern.edu", "image": f"{CAP}/{image}", "imageAspect": round(aspect / (1 - c), 4),
                     "caption": caption, "moves": mv, "ringColor": "#3D3929"},
                    show, motion_claim="The real Open OnDemand page; the camera pushes in to what the sentence names.")


A1, A2, A3, A4, A5, A6, A7, A8, A9 = ("I · What A Cluster Is", "II · Getting An Account", "III · Logging In", "IV · Where Files Live",
                                      "V · Moving Data", "VI · Running Jobs", "VII · Checking On A Job", "VIII · Right-Sizing", "IX · Software")

OPEN = [
 remotion("BIDEA", "the idea",
    "Hola. This is Liam, in for Bear. First, a correction. Explorer is not a big computer where you run your code. "
    "It's a cluster of computers, and you ask it for a slice. This lecture is the whole introduction: what a "
    "cluster is, how you get an account, how you log in through the terminal or the Open OnDemand website, where "
    "your files live, how you move data, how you run and check a job, how to right-size it, and how software works.",
    "BrutalistHesitantWriter",
    {"text": "Explorer is a big computer\nwhere I run my code", "triggerWords": "run my code",
     "replacementWords": "ask for a slice", "fontSize": 70, "charMs": 62, "hesitateBetween": 6, "hesitateWithin": 1,
     "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types the assumption"}, {"at": 0.3, "event": "corrects 'run my code' -> 'ask for a slice'"}],
    lane="bookend", lead_silence_s=0.8, motion_claim="The writer types the newcomer's picture and corrects it.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. An HPC cluster: many computers wired together to work on one problem. A login node: the machine you "
    "land on, for light work only. A compute node: a machine that does the heavy work, handed to you on request. "
    "Slurm: the scheduler that takes those requests and decides who runs where. A partition: a named group of nodes "
    "with its own limits. And Open OnDemand, OOD: a website that gives you the cluster in a browser.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "HPC cluster", "meaning": "many computers wired together to work on one problem"},
               {"term": "login node", "meaning": "the machine you land on; light work only"},
               {"term": "compute node", "meaning": "a machine that does the heavy work, handed to you on request"},
               {"term": "Slurm", "meaning": "the scheduler: takes requests, decides who runs where"},
               {"term": "partition", "meaning": "a named group of nodes with its own limits"},
               {"term": "Open OnDemand", "meaning": "OOD: a website that gives you the cluster in a browser"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "HPC cluster"}, {"at": 0.25, "event": "login node"}, {"at": 0.4, "event": "compute node"},
     {"at": 0.58, "event": "Slurm"}, {"at": 0.72, "event": "partition"}, {"at": 0.87, "event": "Open OnDemand"}],
    gate="CARD", lane="bookend", qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

B = [
 # I
 manim("B10", A1,
    "Start with the shape of the thing. A cluster is many computers working together on problems too big for one "
    "desk. You log in to a login node. Light work happens there: editing a file, looking around. When you need real "
    "computing power, the work moves to a compute node, and a scheduler called Slurm manages everyone's requests for "
    "those nodes.",
    "B10_ClusterShape",
    "Isometric: a small laptop at left; a cable to a single 'login node' block; behind it a wall of compute racks (aicr_rack ×3). A job box is edited on the login node (a page flips), then a 'Slurm' gate opens and the box rides a belt to a lit compute rack. Act title top-left.",
    [{"at": 0.15, "event": "laptop → login node"}, {"at": 0.45, "event": "light work on the login node"}, {"at": 0.7, "event": "Slurm gate"}, {"at": 0.85, "event": "the job lands on a compute rack"}]),
 manim("B11", A1,
    "Explorer is Northeastern's cluster, run by the Research Computing team, and it replaced the older Discovery "
    "cluster. Forty-five thousand CPU cores. More than five hundred twenty-five GPUs. Free of charge to every "
    "Northeastern faculty member and student. It lives at the Massachusetts Green High Performance Computing Center "
    "in Holyoke.",
    "B11_ExplorerNumbers",
    "Two counters climb: '45,000' over a grid of CPU squares, '525+' over a smaller grid of dark GPU squares; a small 'Holyoke, MA' label lands beside a building block; 'free' lands as a tag.",
    [{"at": 0.3, "event": "45,000 CPU cores"}, {"at": 0.5, "event": "525+ GPUs"}, {"at": 0.65, "event": "free"}, {"at": 0.88, "event": "Holyoke"}], sparse=False),
 manim("B12", A1,
    "Around the compute: a ten-gigabit link to the university network for moving data in and out, six petabytes of "
    "fast shared storage, and between the nodes themselves either ten-gigabit ethernet or InfiniBand at one or two "
    "hundred gigabits a second, so every size of workload has a place.",
    "B12_Plumbing",
    "The racks from B10; a thick pipe labelled '10 GbE' runs from the campus block to the racks; a storage block labelled '6 PB' slides in; between racks a faster double pipe labelled 'InfiniBand · 100–200 Gbps' draws.",
    [{"at": 0.2, "event": "10 GbE to campus"}, {"at": 0.45, "event": "6 PB storage"}, {"at": 0.75, "event": "InfiniBand between nodes"}]),
 # II
 manim("B20", A2,
    "Getting on. For research, every user belongs to a storage space owned by a PI or staff member; storage is free up "
    "to thirty-five terabytes. If your lab has one, the PI adds you with the project command, or you file an access "
    "request. If it doesn't, the PI requests a storage space first. For coursework, your instructor applies through "
    "the classroom access form, and students get in through the course.",
    "B20_TwoDoors",
    "Two doors: 'research' and 'classroom'. Behind research, a project_cabinet labelled '35 TB'; a PI token opens the door and a user token walks through (label 'project command'); a second path 'access form'. Behind classroom, an instructor token opens the door and several student tokens file in. Act title top-left.",
    [{"at": 0.15, "event": "research door, the cabinet"}, {"at": 0.4, "event": "PI adds you"}, {"at": 0.6, "event": "or request the space"}, {"at": 0.8, "event": "classroom door"}]),
 # III
 manim("B30", A3,
    "Two ways in. The terminal, and the Open OnDemand website. Both reach the same cluster. The team's advice is to get "
    "comfortable with the terminal, and we'll use both.",
    "B30_TwoWaysIn",
    "Left: a dark terminal window with a '$' prompt; right: a pale browser window with a dark title bar; both connect by cables to the same login node block in the middle. Act title top-left.",
    [{"at": 0.15, "event": "terminal"}, {"at": 0.35, "event": "browser"}, {"at": 0.6, "event": "same cluster"}]),
 shell("B31", A3,
    "From a Mac, open Terminal and s s h to login dot explorer dot northeastern dot e d u with your Northeastern username. "
    "It asks for your password; the cursor doesn't move while you type it, which is normal. The welcome banner means "
    "you're on. On Windows, install an SSH client such as MobaXterm or PuTTY and point it at the same host, port "
    "twenty-two.",
    ["$ ssh username@login.explorer.northeastern.edu", "username@login.explorer.northeastern.edu's password:",
     "+------------------------------------------------------+", "| You're now connected to the Explorer cluster. Visit |",
     "| our website http://rc.northeastern.edu/support for   |", "| links to our service catalog, documentation,        |",
     "| training, and consultations. You can also email us  |", "| at rchelp@northeastern.edu to generate a help ticket.|",
     "|                                                      |", "| The Research Computing Team                          |",
     "+------------------------------------------------------+", "[username@explorer-02 ~]$ "],
    [{"at": 0.1, "event": "ssh"}, {"at": 0.3, "event": "password prompt"}, {"at": 0.55, "event": "the welcome banner"}], start=20, gap=26, title="Terminal"),
 capture("B32", A3,
    "Or open a browser at o o d dot explorer dot northeastern dot e d u. You sign in with your Northeastern username and "
    "password, confirm with Duo, and land on the Open OnDemand dashboard. You're on the cluster.",
    "screenshot_OOD.png", 2126 / 1388,
    [{"at": 0.0, "x": 0.5, "y": 0.5, "scale": 1.0}, {"at": 0.6, "x": 0.55, "y": 0.2, "scale": 1.5, "ring": [0.11, 0.108, 0.87, 0.06]}],
    [{"at": 0.0, "event": "the dashboard"}, {"at": 0.6, "event": "zoom to the menu bar: Files, Jobs, Clusters, Interactive Apps"}]),
 # IV
 manim("B40", A4,
    "Now, where things live. Everyone has a home directory and a scratch directory. Researchers also have a projects "
    "space. Students in a course have a courses space, and may not have projects. Always write the full path, starting "
    "with a slash, so a script means the same place wherever it runs.",
    "B40_FourPlaces",
    "Four containers land with real mono paths: home_box '/home/username', scratch_bin '/scratch/username', project_cabinet '/projects/projectname', and a second cabinet in kraft '/courses/coursename.code'; a leading '/' on each path gets a small ring. Act title top-left.",
    [{"at": 0.2, "event": "home, scratch"}, {"at": 0.4, "event": "projects"}, {"at": 0.55, "event": "courses"}, {"at": 0.85, "event": "the leading slash"}]),
 manim("B41", A4,
    "Each has a size. Home holds seventy-five gigabytes, and it fills fastest; when it does, you'll see quota exceeded. "
    "Scratch holds fifty terabytes, but it's purged on the first Tuesday of every month, so it's no place for anything "
    "you want to keep. Projects is the long-term home for big data and for folders of many small files. A course "
    "space holds one to five terabytes, shared by the whole class.",
    "B41_Quotas",
    "The four containers from B40 with capacity labels: '75 GB', '50 TB', 'long-term', '1–5 TB · shared'; the home box fills and a 'quota exceeded' stamp lands; a calendar page with the first Tuesday marked sweeps the scratch bin empty; blocks move into the project cabinet.",
    [{"at": 0.15, "event": "75 GB, quota exceeded"}, {"at": 0.45, "event": "50 TB, first-Tuesday purge"}, {"at": 0.7, "event": "projects for the long term"}, {"at": 0.9, "event": "1–5 TB shared"}]),
 shell("B42", A4,
    "Paths in practice. L S lists a directory, and cat prints a file. With an absolute path you can read any file "
    "you have permission for, from anywhere on the cluster.",
    ["$ ls /projects/seedpod/rawdata", "bam_lists           feems_grids        population_files",
     "bam_lists.tar.gz    id.txt             spal", "Chr_genome_final_gene.gff3   metadata   spal_barcodes.txt",
     "feems               nursery_samples.txt   ...", "$ cat /home/s.caplins/myveryimportantscript.sh", ".~*~. Have a wonderful day! .~*~."],
    [{"at": 0.1, "event": "ls"}, {"at": 0.6, "event": "cat prints the file"}], start=20, gap=38),
 # V
 shell("B50", A5,
    "Moving data in. From your own machine, S C P copies a file to the cluster through the transfer node. Make a small "
    "test file, copy it into your home directory, then log in and l s to see it arrive. To put it in your project space "
    "instead, change the destination path. Many small files? Zip or tar them first.",
    ["$ echo \"hello from the Explorer cluster\" > testfile.txt",
     "$ scp testfile.txt username@xfer.discovery.neu.edu:/home/username",
     "$ ssh username@login.explorer.northeastern.edu", "$ ls", "testfile.txt",
     "# or straight into your project space", "$ scp testfile.txt \\", "    username@xfer.discovery.neu.edu:/projects/rc/username"],
    [{"at": 0.1, "event": "echo"}, {"at": 0.3, "event": "scp to home"}, {"at": 0.55, "event": "ls shows it"}, {"at": 0.8, "event": "scp to projects"}], start=20, gap=42, title="Terminal — your laptop"),
 capture("B51", A5,
    "Or use the website. On the Open OnDemand dashboard, open Files, then Home Directory. The Files app starts in your "
    "home directory, and the Change directory button takes you to scratch or projects.",
    "screenshot_files1.png", 2994 / 1494,
    [{"at": 0.0, "x": 0.5, "y": 0.5, "scale": 1.0}, {"at": 0.3, "x": 0.3, "y": 0.25, "scale": 1.8, "ring": [0.13, 0.15, 0.14, 0.08]}],
    [{"at": 0.0, "event": "the Files app"}, {"at": 0.3, "event": "zoom to the path and Change directory"}]),
 capture("B52", A5,
    "Upload opens a window where you browse for files or drop them in. The Files app is limited to ten gigabytes a "
    "transfer. Bigger than that, use S C P; for very large datasets, Globus. And the same app downloads files, edits "
    "them, and makes new folders.",
    "screenshot_files3.png", 2994 / 1494,
    [{"at": 0.0, "x": 0.5, "y": 0.5, "scale": 2.0, "ring": [0.36, 0.45, 0.28, 0.14]}, {"at": 0.6, "x": 0.5, "y": 0.55, "scale": 1.9}],
    [{"at": 0.0, "event": "the upload window, ringed"}, {"at": 0.6, "event": "pull back to the whole app"}]),
 # VI
 manim("B60", A6,
    "Running jobs. So far we've only used the login nodes and the transfer node. Real computation has to move to a "
    "compute node: no scientific software, big transfers or heavy work on the login node, because its traffic slows "
    "the whole cluster for everyone.",
    "B60_LeaveTheLoginNode",
    "The login node block with a job box on it; a terracotta X lands over the box on the login node; the box rides the belt through the Slurm gate to a compute rack that lights. Act title top-left.",
    [{"at": 0.3, "event": "not on the login node"}, {"at": 0.65, "event": "the job moves to a compute node"}]),
 shell("B61", A6,
    "From the terminal, s run gets you a compute node. The simplest form takes the defaults: four hours, one node, "
    "one task, two gigabytes of memory, two CPUs, on the short partition. Flags ask for more: here, six hours, fifty "
    "gigabytes, sixteen tasks. Every flag has a short form too.",
    ["$ srun --pty bash", "# defaults: 4 h, 1 node, 1 task, 2 GB, 2 CPUs, partition short",
     "$ srun --time=6:00:00 --mem=50GB --ntasks=16 \\", "    --partition=short --pty bash",
     "# the same, with short flags", "$ srun -t 6:00:00 --mem 50GB -n 16 -p short --pty bash"],
    [{"at": 0.1, "event": "srun --pty bash"}, {"at": 0.4, "event": "the defaults"}, {"at": 0.6, "event": "more of everything"}, {"at": 0.85, "event": "short flags"}], start=20, gap=50),
 manim("B62", A6,
    "A partition is how the team groups nodes: by time limit, by node count, by CPU or GPU. On Explorer: short, the "
    "default, and sharing for CPU work. gpu, gpu-interactive, gpu-short and sharing for GPU work. Two you apply for: "
    "long and multigpu, once you can show your code uses them well. And two only for courses: courses and courses-gpu.",
    "B62_Partitions",
    "A drawn table builds: two columns 'CPU' (short · sharing) and 'GPU' (gpu · sharing · gpu-interactive · gpu-short) in mono; a second block 'apply for access' (long · multigpu) with a small gate icon; a third 'courses only' (courses · courses-gpu) with a kraft tag.",
    [{"at": 0.3, "event": "CPU column"}, {"at": 0.5, "event": "GPU column"}, {"at": 0.7, "event": "apply: long, multigpu"}, {"at": 0.9, "event": "courses"}], sparse=False),
 manim("B63", A6,
    "Which one? If you're in a course and have a courses directory, use courses for CPU jobs and courses-gpu for GPU "
    "jobs. Otherwise, short for most CPU work; gpu-interactive or gpu-short for interactive GPU sessions; and the gpu "
    "partition for GPU batch jobs.",
    "B63_WhichPartition",
    "A decision tree: root 'in a course?'; yes → 'courses' / 'courses-gpu'; no → 'CPU → short', 'interactive GPU → gpu-interactive · gpu-short', 'GPU batch → gpu'; branches light as spoken.",
    [{"at": 0.15, "event": "in a course?"}, {"at": 0.4, "event": "courses, courses-gpu"}, {"at": 0.6, "event": "short"}, {"at": 0.8, "event": "gpu-interactive, gpu-short, gpu"}], sparse=False),
 shell("B64", A6,
    "A GPU is a processor built for thousands of parallel tasks, and it's what AI and much of modern science run on. "
    "To get one interactively, name the partition and the g r e s. Naming the card type gives you exactly that card. "
    "Leaving it general gives you whatever is free first, fine for a quick test, but for repeated runs use the same "
    "type, or at least record which one you got.",
    ["$ srun --partition=gpu-interactive --gres=gpu:v100-sxm2:1 \\", "    --ntasks=1 --mem=4GB --time=01:00:00 \\", "    --nodes=1 --pty /bin/bash",
     "# or any free GPU type", "$ srun --partition=gpu-interactive --gres=gpu:1 \\", "    --ntasks=1 --mem=4GB --time=01:00:00 \\", "    --nodes=1 --pty /bin/bash"],
    [{"at": 0.3, "event": "a named GPU type"}, {"at": 0.65, "event": "any free GPU"}], start=40, gap=46),
 capture("B65", A6,
    "On the website, an interactive job is a form. For RStudio you pick the version, the partition, the hours, the "
    "CPUs and the memory, and press Launch. The defaults are fine to start.",
    "screenshot_rstudio.png", 2598 / 2056,
    [{"at": 0.0, "x": 0.55, "y": 0.42, "scale": 1.4, "ring": [0.29, 0.28, 0.48, 0.31]}, {"at": 0.65, "x": 0.55, "y": 0.82, "scale": 1.4, "ring": [0.29, 0.895, 0.48, 0.055]}],
    [{"at": 0.0, "event": "the form: version, partition, time"}, {"at": 0.65, "event": "down to Launch"}]),
 capture("B66", A6,
    "The session moves from Queued to Starting to Running, and your time starts when it's running. The card shows the "
    "host node, a Cancel button, the time remaining and a session ID. Cancel it when you're done; that frees the node "
    "for someone else.",
    "screenshot_rstudio3.png", 1866 / 652,
    [{"at": 0.0, "x": 0.5, "y": 0.5, "scale": 1.0}, {"at": 0.4, "x": 0.3, "y": 0.5, "scale": 1.4, "ring": [0.02, 0.22, 0.47, 0.65]}],
    [{"at": 0.0, "event": "Running"}, {"at": 0.4, "event": "zoom to Host, Cancel, time remaining"}]),
 shell("B67", A6,
    "The jobs that do most of the real work are batch jobs: set up, submitted, and run without you. Test your commands "
    "in an s run session first; then write a script. The S BATCH lines name the job, the partition, one node and sixteen "
    "tasks, and ask for email on every event. Then load your software, activate your environment, and run.",
    ["$ cat myjob.sh", "#!/bin/bash", "#SBATCH -J MyJob", "#SBATCH -p short", "#SBATCH -N 1", "#SBATCH -n 16",
     "#SBATCH --mail-user=username@northeastern.edu", "#SBATCH --mail-type=ALL", "module load anaconda3/2024.06",
     "source activate /home/username/.conda/envs/test", "echo \"You are doing great!\"", "python --version"],
    [{"at": 0.3, "event": "the SBATCH lines"}, {"at": 0.75, "event": "software, environment, commands"}], start=30, gap=28),
 shell("B68", A6,
    "Submit it with s batch. Slurm answers with a job ID. When the job runs, its output goes to a file named slurm, dash, "
    "the job ID, dot out; cat shows what the job printed. Use less to page through long files, and q to quit. If "
    "you're unsure how much to ask for, ask for a little and scale up when a job runs out of memory, CPU or time.",
    ["$ sbatch myjob.sh", "Submitted batch job 3719393", "$ cat slurm-3719393.out", "You are doing great!", "Python 3.12.4",
     "$ less slurm-3719393.out", "# q quits less"],
    [{"at": 0.1, "event": "sbatch"}, {"at": 0.25, "event": "Submitted batch job"}, {"at": 0.45, "event": "the .out file"}, {"at": 0.7, "event": "less"}], start=20, gap=44),
 # VII
 shell("B70", A7,
    "Is it running? s queue with your username lists your jobs: ID, partition, name, state, R for running, time and "
    "node. s queue for a partition, piped to w c, counts how busy the queue is: five hundred eighteen lines here. And "
    "dash dash start estimates when a waiting job will begin.",
    ["$ squeue -u username", "JOBID PARTITION     NAME     USER ST  TIME NODES NODELIST(REASON)",
     "3718152     short ood-desk username  R  45:06     1 c0690", "3719477     short     bash username  R   0:59     1 c0690",
     "$ squeue -p short | wc -l", "518", "$ squeue -u username --start"],
    [{"at": 0.1, "event": "squeue -u"}, {"at": 0.5, "event": "how busy: 518"}, {"at": 0.8, "event": "--start"}], start=20, gap=40),
 capture("B71", A7,
    "On the website, Jobs, then Active Jobs, shows the same list. And My Interactive Sessions shows each session with "
    "its host node and, in parentheses, the seven-digit Slurm job ID you'd give the Research Computing team if "
    "something goes wrong.",
    "screenshot_jobs2.png", 1727 / 1042,
    [{"at": 0.0, "x": 0.5, "y": 0.5, "scale": 1.0}, {"at": 0.4, "x": 0.45, "y": 0.4, "scale": 1.7, "ring": [0.32, 0.17, 0.22, 0.1]}],
    [{"at": 0.0, "event": "My Interactive Sessions"}, {"at": 0.4, "event": "zoom to RStudio (3468842), Host"}]),
 capture("B72", A7,
    "Click the Session ID link and you'll see the files Open OnDemand made for the job. output dot log is the one to "
    "read when a session doesn't behave, and the one the team will ask for in a ticket.",
    "screenshot_jobs2.png", 1727 / 1042,
    [{"at": 0.0, "x": 0.45, "y": 0.42, "scale": 1.7, "ring": [0.33, 0.345, 0.26, 0.055]}],
    [{"at": 0.0, "event": "the Session ID link, ringed"}]),
 # VIII
 manim("B80", A8,
    "Now the habit that makes you a power user. Ask for close to the minimum you need, because the more you request, "
    "the longer you wait for it. After a job finishes, seff, Slurm efficiency, shows what it actually used. Two real "
    "reports from the training. Job one: twelve cores, eight percent CPU efficiency, ten percent of fifty gigabytes "
    "used. It could have asked for far less. Job two: eight cores at eighty-four percent CPU efficiency. A much better "
    "fit. Try seff on your next finished job.",
    "B80_Seff",
    "Two drawn seff reports side by side on cream, mono headers ('$ seff 371441' · '$ seff 2612438', cores 12 / 8, wall-clock 00:17:19 / 00:25:57); bars grow to the real values: CPU efficiency 8.29% vs 83.83%, memory efficiency 10.44% of 50 GB vs 3.56% of 15.62 GB; the first report's CPU bar gets a terracotta dot and 'could ask for less', the second an ink check. Act title top-left.",
    [{"at": 0.3, "event": "seff 371441: 8.29%"}, {"at": 0.55, "event": "10% of 50 GB"}, {"at": 0.7, "event": "seff 2612438: 83.83%"}, {"at": 0.9, "event": "a better fit"}], sparse=False),
 # IX
 shell("B90", A9,
    "Software comes as modules, so you load only what you need, when you need it, because some conflict. module avail "
    "lists them; module load loads one, with the exact name and case you saw. Don't put module load in your dot bashrc: "
    "it interferes with Open OnDemand and makes your work harder to reproduce.",
    ["$ module avail", "$ module load anaconda3/2024.06", "# load modules when you need them, not in ~/.bashrc"],
    [{"at": 0.15, "event": "module avail"}, {"at": 0.4, "event": "module load"}, {"at": 0.75, "event": "not in .bashrc"}], start=30, gap=80),
 remotion("B91", A9,
    "Beyond modules, three routes. Conda environments, which can hold many kinds of scientific software, not only "
    "Python. Containers, which the cluster supports. And building from source. And when you're stuck: email r c help at "
    "northeastern dot e d u, come to office hours on Zoom, or book a consultation.",
    "LibraryIconRow",
    {"title": "IX · Software",
     "items": [{"label": "conda", "sub": "environments, not only Python", "icon": "package", "mono": True, "cue_phrase": "Conda environments"},
               {"label": "containers", "sub": "supported on the cluster", "icon": "box", "cue_phrase": "Containers"},
               {"label": "from source", "sub": "build it yourself", "icon": "hammer", "cue_phrase": "building from source"}]},
    [{"at": 0.1, "event": "conda"}, {"at": 0.35, "event": "containers"}, {"at": 0.5, "event": "from source"}],
    motion_claim="Three routes, each landing as one large library icon."),
]

RECAP = ["A cluster: log in to a login node, ask Slurm for a compute node.",
         "Two doors: ssh to login.explorer.northeastern.edu, or ood.explorer.northeastern.edu.",
         "Home 75 GB; scratch 50 TB, purged monthly; projects for the long term.",
         "srun for a live node; sbatch for a script; squeue to check on it.",
         "Partitions: short by default; gpu partitions for GPUs; courses for classes.",
         "seff after every job; request close to what you need."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. A cluster: you log in to a login node and ask Slurm for a compute node. Two doors: s s h "
    "to the login address, or the Open OnDemand website. Home holds seventy-five gigabytes; scratch holds fifty "
    "terabytes and is purged monthly; projects is for the long term. s run for a live node, s batch for a script, "
    "S queue to check on it. Partitions: short by default, the gpu partitions for GPUs, courses for classes. And "
    "seff after every job, so you request close to what you need.",
    "ClaudeVerdictArtifact", {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land"}],
    lane="bookend", lead_silence_s=0.5, qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("I'm new to a Slurm cluster. Here's what I want to run: [describe your program and data in two sentences]. "
             "Tell me which of my files belong in home, scratch and projects; write me an srun command to test it interactively "
             "with modest resources; then write the sbatch script for the real run, and tell me which commands I use to check "
             "on the job and to read its efficiency afterwards.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_PROMPT + " Then check two things yourself. Does every path it wrote start "
    "with a slash? And did it tell you to test with s run before you submit with s batch?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Plan Your First Explorer Job", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: does every path it wrote start with a slash?", "Check: did it tell you to test with srun before sbatch?"],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": f"{TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

# Gate V underfill on drawn beats that build progressively (44% / 39% at the sampled midpoint on the first 4K run):
# the drawn lane's waiver, underfill and clustered only.
for b in B:
    if b["beat_id"] in {"B62", "B63"} and "qc" not in b:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE + " Progressive drawing: the midpoint frame holds only part of the final picture."}
BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Intro to Explorer and O O D. The web front door to the Explorer cluster: launch apps, move files and start jobs from a browser, with no terminal required.",
         "estimated_duration_s": 10.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]
sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · EXPLORER", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "Spanish (Hola)",
    "audience": "Northeastern students and researchers about to use the Explorer cluster for the first time; assumes no other film",
    "source_doc": "hpc/Intro-to-Explorer-OOD-2026/Intro_explorer_ood.md (Northeastern Research Computing training, presenter Serena Caplins; "
                  "github.com/northeastern-rc-training/Intro-to-Explorer-OOD-2026), read 2026-10-06",
    "playlist": "Explorer", "chapter_number": 2,
    "series_title": "Research Computing on Explorer and AICR", "series_video_number": 3, "series_video_count": 13, "series_entry_video": "Video 1 · AICR Introduction",
    "lecture_opening_description": "The web front door to the Explorer cluster",
    "tags": ["Explorer cluster", "Northeastern", "Research Computing", "Open OnDemand", "HPC", "Slurm", "srun", "sbatch", "squeue", "seff",
             "scp", "modules", "conda", "MGHPCC", "Nik Bear Brown"]},
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
        if pat == "LibraryIconRow":
            n = b["narration_text"]
            for it in props["items"]:
                at = round(n.index(it["cue_phrase"]) / len(n), 3)
                it["at"] = at if not 0.43 <= at <= 0.57 else 0.58
p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(BEATS), "beats; est", round(sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in BEATS)), "s")
