#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-scientific-reproducibility.

LECTURE (brutalist.art/skills/make/lecture/SKILL.md). Source: hpc/Intro-to-Scientific-Reproducibility-2026/
scientific_repoducibility_main.md ("Scientific Reproducibility: Best Practices and Implementation", Northeastern Research
Computing, presenter Serena Caplins; github.com/northeastern-rc-training/Intro-to-Scientific-Reproducibility-2026).
Seventh film of the series; same cast.
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Scientific Reproducibility"
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


def shell(bid, act, narration, lines, show, start=20, gap=40, title="ssh — login.explorer.northeastern.edu"):
    return remotion(bid, act, narration, "CCPlainShell", {"title": title, "lines": lines, "startCue": start, "lineGap": gap}, show,
                    motion_claim="The training's own commands and files land in order.")


def code(bid, act, narration, title, src, spark, show, lang="python"):
    return remotion(bid, act, narration, "ClaudeCodeBeat", {"title": title, "code": src, "language": lang, "largeText": True, "sparkLine": spark},
                    show, motion_claim="The training's own text prints line by line.")


A = ["I · Three Words", "II · Why It Matters", "III · The Checklist", "IV · Record Your Software", "V · Conda Environments",
     "VI · Data", "VII · Documentation", "VIII · Start Tomorrow"]

OPEN = [
 remotion("BIDEA", "the idea",
    "Hallo. This is Liam, in for Bear. First, a correction. Reproducibility is not a favour you do for other scientists. "
    "The first person it helps is you, six months from now, when a reviewer asks for one more plot. This lecture is a "
    "toolkit for making your research redoable: the three words people confuse, why the field has a crisis, a checklist, "
    "how to record your software, conda environments done properly, data organisation, documentation, and what to do "
    "tomorrow morning.",
    "BrutalistHesitantWriter",
    {"text": "Reproducibility is\nfor other scientists", "triggerWords": "for other scientists", "replacementWords": "for you, six months on",
     "fontSize": 72, "charMs": 62, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types the assumption"}, {"at": 0.3, "event": "corrects it"}],
    lane="bookend", lead_silence_s=0.8, motion_claim="The writer types the newcomer's picture and corrects it.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. Version control: software that records every change to your files, so you can go back. A module: a "
    "piece of software the cluster team installed, loaded by name and version. Conda: a tool that builds isolated "
    "environments of packages. An environment: one named set of software, kept apart from all the others. A README: the "
    "plain-text file that explains a folder. And a random seed: the number that makes a random process repeat exactly.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "version control", "meaning": "software that records every change to your files"},
               {"term": "module", "meaning": "cluster-installed software, loaded by name and version"},
               {"term": "conda", "meaning": "a tool that builds isolated environments of packages"},
               {"term": "environment", "meaning": "one named set of software, kept apart from the others"},
               {"term": "README", "meaning": "the plain-text file that explains a folder"},
               {"term": "random seed", "meaning": "the number that makes a random process repeat exactly"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "version control"}, {"at": 0.25, "event": "module"}, {"at": 0.4, "event": "conda"}, {"at": 0.58, "event": "environment"}, {"at": 0.72, "event": "README"}, {"at": 0.87, "event": "random seed"}],
    gate="CARD", lane="bookend", qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

SBATCH_RECORD = """#!/bin/bash
#SBATCH -N 1
#SBATCH -p short
#SBATCH -t 5:00:00
#SBATCH -n 32
module load julia/1.10.4
module load bwa/0.7.18
module load bamtools/2.5.2
cd /projects/seedpod/rawdata
bwa mem ref.fa reads.fq > aln.sam"""
ENV_YML = """name: research_project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - numpy=1.24.3
  - pandas=2.0.2
  - matplotlib=3.7.1
  - jupyter
  - pip:
    - seaborn"""
README_MD = """# Project Title
Brief description of the project (2-3 sentences)
## Installation
conda env create -f environment.yml
## Reproducibility
1. Clone repository: git clone https://github.com/user/project.git
2. Create environment: conda env create -f environment.yml
3. Run analysis: python src/main_analysis.py
4. Results appear in results/

## Citation · License · Contact"""
DOCSTRING = '''def calculate_mean(data):
    """
    Calculate mean of dataset excluding missing values.

    Parameters: data : array-like
    Returns:    float, the mean value
    """
    data = np.array(data)
    return np.nanmean(data)
# Good: explains reasoning
# Adjust for 1-based indexing in original dataset
x = x + 1'''
DATA_README = """# Dataset: Participant Survey Responses
## Source
Collected via Qualtrics, January 2024
## Variables
- subject_id: Unique participant identifier (integer, 1-500)
- age: Participant age in years (integer, 18-65, -99=missing)
## Processing
1. Removed duplicate entries
2. Recoded missing values to -99
## Known Issues
- 15 participants have missing age data"""

B = [
 # I
 manim("B10", A[0],
    "Three words people mix up. Reproducibility: someone else takes your same data and your same methods and gets your "
    "result. Replicability: a different team collects new data, uses similar methods, and finds a comparable result. "
    "Repeatability: you yourself re-run the same methods on the same data six months later and get the identical answer. "
    "Today is mostly about the first and the third.",
    "B10_ThreeWords",
    "Three columns build: each a small pipeline of data box → method gear → result page. Column 1 'reproducibility': same data (kraft), same method, another person token; column 2 'replicability': a new data box (white), similar method, another team (three tokens); column 3 'repeatability': same data, same method, the same token plus a calendar '+6 months'. Terracotta dots on columns 1 and 3 at the end. Act title top-left.",
    [{"at": 0.1, "event": "reproducibility"}, {"at": 0.35, "event": "replicability"}, {"at": 0.6, "event": "repeatability"}, {"at": 0.9, "event": "the first and the third"}]),
 # II
 manim("B20", A[1],
    "Why it matters. In 2016 a Nature survey asked scientists whether they had failed to reproduce an experiment. Most "
    "had: in chemistry, roughly nine in ten had failed to reproduce someone else's result; in biology, nearly eight in "
    "ten; in physics, medicine and earth science, around two in three. Other studies put numbers on it. In psychology, "
    "only thirty-six to forty-seven of a hundred studies replicated. In biomedicine, eleven percent of fifty-three landmark "
    "cancer studies. In economics, only forty-nine percent of papers even had enough data and code to try.",
    "B20_TheCrisis",
    "Left: horizontal grey bars for the Nature 2016 survey (values read from its published figure, labelled 'approx.'): chemistry ~87%, biology ~77%, physics ~69%, medicine ~67%, earth ~64%; caption 'failed to reproduce someone else's result · Nature survey, 2016'. Right: three stat bars land with their citations in small serif: psychology 36–47 of 100 (Open Science Collaboration, 2015), cancer 11% of 53 (Begley & Ellis, 2012), economics 49% had data and code (Chang & Li, 2015). Act title top-left.",
    [{"at": 0.15, "event": "Nature 2016 bars"}, {"at": 0.5, "event": "psychology 36–47%"}, {"at": 0.68, "event": "cancer 11% of 53"}, {"at": 0.85, "event": "economics 49%"}]),
 manim("B21", A[1],
    "It bites in the real world: clinical decisions built on results no one can reproduce, policy built on models no one "
    "can re-run. And it bites you first. In every project something has to be redone, an analysis, a plot. The more "
    "reproducible your workflow, the faster that is, and the faster you publish. The usual culprits are five: methods not "
    "documented, data and code not shared, software versions not recorded, results that depend on one machine, and "
    "absolute file paths baked into code.",
    "B21_FiveBarriers",
    "A researcher token at a desk with a plot page; a calendar flips '+6 months'; the plot page is requested again (a terracotta ring) and the token re-runs a pipeline that lights green quickly ('redo in minutes'). Then five barrier cards land in a row, each a small drawn glyph with a 1–3 word label (no methods · not shared · no versions · one machine · absolute paths), each struck with a grey X as named.",
    [{"at": 0.3, "event": "six months later, redo the plot"}, {"at": 0.55, "event": "the five culprits land"}, {"at": 0.9, "event": "absolute paths"}]),
 # III
 manim("B30", A[2],
    "The checklist, in three phases. At setup: a Git repository, a consistent folder layout, a documented environment, "
    "a README. During the work: commented code, relative paths, random seeds set, every data transformation written down, "
    "regular commits. At the end: have someone else run it, ship the environment file and the instructions, share the "
    "data and the code, and write down the limitations.",
    "B30_ThreePhaseChecklist",
    "Three columns 'setup · during · completion' with checkbox rows that tick as named (4 · 5 · 5 rows, 1–3 word labels); a progress belt runs under the columns from left to right. Act title top-left.",
    [{"at": 0.1, "event": "setup rows"}, {"at": 0.4, "event": "during rows"}, {"at": 0.7, "event": "completion rows"}]),
 remotion("B31", A[2],
    "And one principle to carry: FAIR, set out in Scientific Data in 2016. Findable: persistent identifiers and metadata. "
    "Accessible: stored in open repositories. Interoperable: standard formats. Reusable: clear licensing and documentation.",
    "LibraryIconRow",
    {"title": "FAIR · Scientific Data, 2016",
     "items": [{"label": "Findable", "sub": "identifiers, metadata", "icon": "search", "cue_phrase": "Findable"},
               {"label": "Accessible", "sub": "open repositories", "icon": "lock-open", "cue_phrase": "Accessible"},
               {"label": "Interoperable", "sub": "standard formats", "icon": "puzzle", "cue_phrase": "Interoperable"},
               {"label": "Reusable", "sub": "licence, documentation", "icon": "recycle", "cue_phrase": "Reusable"}]},
    [{"at": 0.3, "event": "F"}, {"at": 0.5, "event": "A"}, {"at": 0.65, "event": "I"}, {"at": 0.85, "event": "R"}],
    motion_claim="Four principles, each landing as one large library icon."),
 manim("B32", A[2],
    "Version control gets its own lecture, but the idea in one breath: every change is recorded, you can revert to any "
    "earlier version, collaborate without overwriting each other, keep the whole history, and experiment on a branch "
    "without breaking the code that works.",
    "B32_VersionControl",
    "A timeline of commit dots grows left to right; a file page changes at each dot; a 'revert' arrow jumps back two dots and the page restores; a branch forks off, carries a terracotta experiment dot, and merges back; two tokens commit to the same line without collision.",
    [{"at": 0.2, "event": "commits"}, {"at": 0.45, "event": "revert"}, {"at": 0.65, "event": "collaborate"}, {"at": 0.85, "event": "a branch"}]),
 # IV
 shell("B40", A[3],
    "Record your software. If you load a cluster module, write down the version and when you ran it, in the job script "
    "or a README. A job script like this one is already a record: Julia one point ten point four, B W A zero point seven "
    "point eighteen, bamtools two point five point two. Change it, and copy the file first, or let Git keep the versions. "
    "The team's own module install scripts are public on GitHub, so you can see exactly how a module was built.",
    ["$ cat run_bwa.sbatch", "#!/bin/bash", "#SBATCH -N 1", "#SBATCH -p short", "#SBATCH -t 5:00:00", "#SBATCH -n 32",
     "module load julia/1.10.4", "module load bwa/0.7.18", "module load bamtools/2.5.2", "cd /projects/seedpod/rawdata",
     "bwa mem ref.fa reads.fq > aln.sam"],
    [{"at": 0.1, "event": "the script"}, {"at": 0.4, "event": "the three module versions"}, {"at": 0.85, "event": "a record"}], start=20, gap=30),
 shell("B41", A[3],
    "And don't load modules in your dot bash R C. That hidden file runs in every shell and every program you open on the "
    "cluster. Aliases and colours belong there. Modules don't: they break the self-contained job script, so later you can't "
    "tell whether a program came from the script or the shell, and they cause dependency conflicts. Keep software in "
    "scripts and READMEs.",
    ["$ cat .bashrc", "# .bashrc", "if [ -f /etc/bashrc ]; then", "    . /etc/bashrc", "fi", "# User specific aliases and functions",
     "alias less='less --RAW-CONTROL-CHARS'", "export LS_OPTS='--color=auto'", "alias ls='ls ${LS_OPTS}'", "alias me='squeue -u username'",
     "# no module load here"],
    [{"at": 0.1, "event": ".bashrc"}, {"at": 0.45, "event": "aliases belong"}, {"at": 0.8, "event": "no module load here"}], start=20, gap=30),
 # V
 shell("B50", A[4],
    "Conda builds isolated environments. It works on every platform, handles Python and non-Python packages, keeps each "
    "project's dependencies apart, and resolves conflicts. On the cluster: get a compute node, load a miniconda module, "
    "create an environment with a Python version, activate it with source activate, install, and deactivate when done.",
    ["$ srun --pty bash", "$ module load miniconda3/25.9.1", "$ conda create -n myproject python=3.10", "$ source activate myproject",
     "$ conda install numpy pandas matplotlib scipy", "$ conda install -c conda-forge scikit-learn", "$ pip install some-package", "$ conda deactivate"],
    [{"at": 0.4, "event": "compute node, module"}, {"at": 0.6, "event": "create, activate"}, {"at": 0.8, "event": "install, deactivate"}], start=60, gap=34),
 shell("B51", A[4],
    "Seven habits. Pin the versions that matter; unpinned, conda takes the latest. Prefer the conda-forge channel, the best "
    "maintained. Channel order matters: conda searches top to bottom. Install conda packages first, then pip ones. Export "
    "the environment, with from history for a cleaner file. Install everything in one session, because conda resolves "
    "conflicts across the whole set at once, and an environment grown over months is the one that won't rebuild. And keep "
    "environments small: one per analysis, not one to rule them all.",
    ["$ conda install numpy=1.24.3 pandas>=2.0,<3.0 matplotlib scipy", "$ conda install -c conda-forge scikit-learn",
     "$ conda config --show channels", "# channels: conda-forge first, then bioconda, then defaults",
     "$ conda env export --from-history > environment.yml", "$ conda list -e > requirements.txt",
     "# one session, all packages; many small environments"],
    [{"at": 0.1, "event": "pin versions"}, {"at": 0.25, "event": "conda-forge"}, {"at": 0.4, "event": "channel order"}, {"at": 0.6, "event": "export"}, {"at": 0.85, "event": "one session, small"}], start=20, gap=46),
 manim("B52", A[4],
    "Picture the two ways to build one. Added to over months, package by package, the environment collects conflicts, and "
    "when you try to recreate it, it won't resolve. Built in one session from one file, it resolves once and rebuilds "
    "anywhere.",
    "B52_OneSessionVsAccretion",
    "Left: an environment box receives packages one at a time over a calendar strip; two of them clash with a grey X and the rebuild arrow ends in a dashed broken box. Right: an environment.yml page feeds all packages into one box at once; a check lands and a copy of the box appears on a second plinth ('rebuilds anywhere').",
    [{"at": 0.15, "event": "added over months"}, {"at": 0.45, "event": "conflicts; won't rebuild"}, {"at": 0.7, "event": "one session from one file"}, {"at": 0.9, "event": "rebuilds anywhere"}]),
 shell("B53", A[4],
    "Managing them. List your environments. Create one at a specific path, in your project space. Remove one. Clone one as "
    "a backup. Update one from its Y M L file, pruning what the file no longer lists. If solving is slow, install mamba and "
    "use it in place of conda. And always use source activate: conda activate needs conda init, which rewrites your dot "
    "bash R C and fights with Open OnDemand.",
    ["$ conda env list", "$ conda create -p /projects/project_name python=3.10", "$ conda env remove -n myproject",
     "$ conda create --clone myproject -n myproject_backup", "$ conda env update -f environment.yml --prune",
     "$ conda install -c conda-forge mamba", "$ mamba create -n myproject python=3.10", "$ source activate conda_env_name   # not conda activate"],
    [{"at": 0.1, "event": "list"}, {"at": 0.25, "event": "create at a path"}, {"at": 0.5, "event": "clone, update"}, {"at": 0.7, "event": "mamba"}, {"at": 0.88, "event": "source activate"}], start=20, gap=42),
 code("B54", A[4],
    "The complete workflow starts from a file. One environment dot Y M L names the environment, the channels in order, the "
    "pinned Python and packages, and the pip extras last.",
    "environment.yml", ENV_YML, "The environment as a file.", [{"at": 0.1, "event": "the yml prints"}], lang="yaml"),
 shell("B55", A[4],
    "Make the project folder, start Git, create the environment from the file, activate it, work, export the final "
    "environment, and commit both files. In a job script the same two lines, module load and source activate, make the "
    "run reproducible.",
    ["$ mkdir research_project && cd research_project", "$ git init", "$ conda env create -f environment.yml", "$ source activate research_project",
     "$ conda env export > environment_final.yml", "$ git add environment.yml environment_final.yml", "$ git commit -m \"Add conda environment specifications\"",
     "# in a job script:", "module load miniconda3/25.9.1", "source activate /path/to/project/conda_env", "python src/analysis.py"],
    [{"at": 0.1, "event": "mkdir, git init"}, {"at": 0.3, "event": "create, activate"}, {"at": 0.55, "event": "export, commit"}, {"at": 0.8, "event": "in a job script"}], start=20, gap=22),
 # VI
 manim("B60", A[5],
    "Data. Three folders: raw, which is original and read-only; processed, cleaned and transformed; and metadata, "
    "dictionaries and sample IDs. Each with its own README. Make raw read-only with c h mod five five five, with your "
    "professor's agreement, since only the owner can change permissions. And name files to sort themselves: ISO dates, "
    "version numbers, lowercase, underscores or hyphens, never spaces.",
    "B60_DataTree",
    "A folder tree draws: data/ → raw/ (a lock lands, mono 'chmod 555'), processed/, metadata/, each with a README page; then three example file names land in mono with the date, the version and the underscores ringed in grey ('2024-01-15_experiment-data_v01.csv', 'participant_demographics_2024-01-20.csv', 'survey_responses_wave1_v03.csv'). Act title top-left.",
    [{"at": 0.15, "event": "raw, processed, metadata"}, {"at": 0.4, "event": "READMEs"}, {"at": 0.55, "event": "chmod 555 on raw"}, {"at": 0.8, "event": "file names"}]),
 code("B61", A[5],
    "Every data folder needs a README: where the data came from, what each variable means and its range, what processing "
    "was done, and what's known to be wrong with it.",
    "data/README.md", DATA_README, "Source, variables, processing, known issues.", [{"at": 0.1, "event": "the data README prints"}], lang="markdown"),
 manim("B62", A[5],
    "A data dictionary makes the variables a table: name, type, description, units, range, and the missing code. And back it "
    "all up by the three-two-one rule: three copies, on two different media, one of them off-site.",
    "B62_DictionaryAnd321",
    "A drawn table builds from the source's four rows (subject_id · age · treatment · response_time with type, units, range, missing); then three copies of a data box land, two on different media (a disk, a tape/cloud block), one on a distant plinth labelled 'off-site'; numerals 3 · 2 · 1.",
    [{"at": 0.15, "event": "the dictionary rows"}, {"at": 0.6, "event": "3 copies"}, {"at": 0.75, "event": "2 media"}, {"at": 0.9, "event": "1 off-site"}]),
 # VII
 code("B70", A[6],
    "The project README: what it is in two sentences, how to install, how to run, where the data is, and the reproduction "
    "steps as a numbered list someone can follow without you. Then citation, licence, contact.",
    "README.md", README_MD, "Someone else can run it without you.", [{"at": 0.1, "event": "the README prints"}], lang="markdown"),
 code("B71", A[6],
    "In code, give functions docstrings: what it does, parameters, what it returns. And comment the why, not the what. "
    "'Adjust for one-based indexing in the original dataset' tells a reader something. 'Add one to x' does not.",
    "analysis.py", DOCSTRING, "Comment the why, not the what.", [{"at": 0.1, "event": "the docstring prints"}]),
 # VIII
 manim("B80", A[7],
    "Five things to keep, and the exercise. Use version control from day one. Document your environment with conda or "
    "pip. Organise files systematically: data, source, results. Write the documentation: README, comments, dictionaries. "
    "And test reproducibility by having someone else run your code. The exercise: write an environment dot yml with Python "
    "three point ten, numpy, pandas and matplotlib; build it; activate it; install a couple more packages; export the "
    "final file. Start the next project this way, document as you go, and share when you can. Perfect reproducibility is "
    "hard; any improvement counts.",
    "B80_FiveAndTheExercise",
    "Five checkbox rows tick (version control · environment · file layout · documentation · someone else runs it) each with a small cast icon; then a kraft exercise card lands with five mono steps (environment.yml · conda env create · source activate · conda install · conda env export) ticking; 'any improvement counts' lands last. Act title top-left.",
    [{"at": 0.1, "event": "five takeaways tick"}, {"at": 0.55, "event": "the exercise steps"}, {"at": 0.92, "event": "any improvement counts"}]),
]

RECAP = ["Reproducible: same data, same methods, someone else gets your result.",
         "Most scientists have failed to reproduce a result; you are the first person you help.",
         "Setup: Git, layout, environment file, README. During: relative paths, seeds, commits.",
         "Job scripts record module versions; never load modules in .bashrc.",
         "Conda: pin versions, conda-forge, one session, small environments, export, source activate.",
         "Data: raw read-only, READMEs, dictionaries, 3-2-1 backups; comment the why."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. Reproducible means same data, same methods, and someone else gets your result. Most "
    "scientists have failed to reproduce a result, and the first person you help is yourself. At setup: Git, a layout, an "
    "environment file, a README; during: relative paths, seeds, commits. Job scripts record module versions, and modules "
    "never go in dot bash R C. Conda: pin versions, prefer conda-forge, install in one session, keep environments small, "
    "export them, and use source activate. Data: raw read-only, READMEs, dictionaries, three-two-one backups. And comment "
    "the why.",
    "ClaudeVerdictArtifact", {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land"}],
    lane="bookend", lead_silence_s=0.5, qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("Here is how my current research project is organised and what software it uses: [describe it in three sentences]. "
             "Audit it against the reproducibility checklist: version control, environment file, folder layout, README, relative "
             "paths, random seeds, data README and dictionary, backups. List what is missing in order of how much it would hurt "
             "me six months from now, and write the environment.yml and the README skeleton for me.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_PROMPT + " Then check two things yourself. Did it pin versions in the Y M L? "
    "And could a stranger follow the README's steps without asking you anything?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Audit Your Project For Six Months From Now", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did it pin versions in the yml?", "Check: could a stranger follow the README without asking you anything?"],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": f"{TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

# Gate V underfill on drawn beats that build progressively (17–55% at the sampled midpoint on the first 4K run).
for b in B:
    if b["beat_id"] in {"B20", "B21", "B32", "B52", "B60", "B62"} and "qc" not in b:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE + " Progressive drawing: the midpoint frame holds only part of the final picture."}
BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Scientific Reproducibility. How to make your computational work redoable, by you in six months or by anyone else, with environments, data layout and records.",
         "estimated_duration_s": 10.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]
sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · REPRODUCIBILITY", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German (Hallo)",
    "audience": "Graduate students and researchers who want their computational work to be redoable; assumes no other film",
    "source_doc": "hpc/Intro-to-Scientific-Reproducibility-2026/scientific_repoducibility_main.md (Northeastern Research Computing training, "
                  "presenter Serena Caplins; github.com/northeastern-rc-training/Intro-to-Scientific-Reproducibility-2026), read 2026-10-06",
    "playlist": "Explorer", "chapter_number": 6,
    "series_title": "Research Computing on Explorer and AICR", "series_video_number": 7, "series_video_count": 13, "series_entry_video": "Video 1 · AICR Introduction",
    "lecture_opening_description": "Make your computational work redoable",
    "tags": ["reproducibility", "conda", "environment.yml", "FAIR data", "README", "data management", "version control", "HPC",
             "Northeastern", "Research Computing", "Nik Bear Brown"]},
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
