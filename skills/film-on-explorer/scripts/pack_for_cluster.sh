#!/usr/bin/env bash
# pack_for_cluster.sh <books-dir> <reel-dir|none> <out-dir> [--max-mb 3000]
#   reel-dir "none" packs the toolkit only (used by bootstrap_toolkit.sh)
# Run on YOUR computer. Builds two archives for one film (nothing is sent anywhere):
#   toolkit-code.tar.gz   the brutalist.art toolkit WITHOUT node_modules, models, other films' assets, media, .git
#                         (node_modules is rebuilt on the cluster: your computer may be arm64 and Explorer is x86_64)
#   reel.tar.gz           the film folder WITHOUT rendered output (keeps beat_sheet, scenes, mp3 + timings, opening fields),
#                         PLUS what `art run` cannot rebuild: the hand-built title-card clip media/BOPEN*.mp4 and the film's own
#                         capture pictures (runtime/remotion/public/<name>/ for every <name> the beat sheet mentions), stored
#                         under <slug>/_public/ and copied into place by explorer_render.sbatch.
#                         Also the Professor Bear portraits the film's scenes pick: professor_bear(ratio, ..., seed="X") chooses file
#                         professor-bear-<ratio>-NN.png by random.Random(seed).randint(1, n), so the exact files are worked out here
#                         and carried under <slug>/_portraits/ (the library itself is 4.5 GB and is never shipped)
# The file list is built explicitly (a pruned walk), the projected size is printed BEFORE anything is archived,
# and the script refuses if it exceeds --max-mb. UNTESTED on the cluster; packing was tested locally.
set -euo pipefail
BOOKS=${1:?books dir}; REEL=${2:?reel dir}; OUT=${3:?out dir}; MAXMB=3000
[ "${4:-}" = "--max-mb" ] && MAXMB=${5:?}
mkdir -p "$OUT"; BOOKS=$(cd "$BOOKS" && pwd); [ "$REEL" = none ] || REEL=$(cd "$REEL" && pwd); OUT=$(cd "$OUT" && pwd)
[ -d "$BOOKS/brutalist.art/runtime" ] || { echo "no toolkit at $BOOKS/brutalist.art"; exit 1; }
SLUG=$(basename "$REEL")

python3 -I - "$BOOKS" "$REEL" "$OUT" "$MAXMB" <<'PY'
import os, sys, json, fnmatch, re
books, reel, out, maxmb = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
slug = os.path.basename(reel)
MEDIA = (".mp4", ".mp3", ".wav", ".mov", ".mkv", ".m4a")
TK_SKIP = ["brutalist.art/.git", "brutalist.art/youtube", "brutalist.art/svg", "brutalist.art/renders", "brutalist.art/reports",
           "brutalist.art/professor-bear", "brutalist.art/runtime/models", "brutalist.art/runtime/remotion/node_modules",
           "brutalist.art/runtime/remotion/public/professor-bear"]
TK_GLOB = ["brutalist.art/runtime/remotion/public/seis*", "brutalist.art/runtime/remotion/public/claude-liam-lecture-*",
           "brutalist.art/runtime/remotion/public/figma-*", "brutalist.art/runtime/remotion/public/lecture-*"]
REEL_SKIP = {"media", "manim", "clips", "exports", "mp4", "_qc", "_superseded", "layout_audit_frames"}

def walk(root_dir, rel_root, skip_fn):
    for dp, dns, fns in os.walk(root_dir, followlinks=False):
        rel = os.path.relpath(dp, rel_root)
        dns[:] = [d for d in dns if not skip_fn(os.path.join(rel, d)) and d not in ("__pycache__",) and not d.startswith(".")]   # hidden dirs (.git, .repoloop run workspaces: GBs) never go
        for f in fns:
            r = os.path.join(rel, f)
            if f == ".DS_Store" or skip_fn(r): continue
            yield r

beat_text = ""
bs = os.path.join(reel, "beat_sheet.json")
if reel != "none" and os.path.exists(bs):
    beat_text = open(bs).read()
PUB = "brutalist.art/runtime/remotion/public/"

def tk_skip(r):
    return r in TK_SKIP or any(fnmatch.fnmatch(r, g) for g in TK_GLOB) or r.lower().endswith(MEDIA)
def reel_skip(r):
    if re.match(r"^[^/]+/media/BOPEN[^/]*\.mp4$", r.replace(os.sep, "/")): return False   # the hand-built title card
    if r.replace(os.sep, "/") == slug + "/media": return False          # enter media/ only to find BOPEN; every other file in it is skipped below
    parts = r.split(os.sep)
    return (len(parts) > 1 and parts[1] in REEL_SKIP) or r.endswith("slate.mp4") or (r.lower().endswith(MEDIA) and "/mp3/" not in "/" + r.replace(os.sep, "/") + "/" and not r.replace(os.sep, "/").startswith(slug + "/mp3/"))

tk_files = list(walk(os.path.join(books, "brutalist.art"), books, tk_skip))
portrait = ""
of = os.path.join(reel, "opening", "opening-fields.json")
if reel != "none" and os.path.exists(of):
    p = json.load(open(of)).get("portrait_path", "")
    if p and os.path.exists(p) and p.startswith(books + os.sep): portrait = os.path.relpath(p, books); tk_files.append(portrait)
reel_files = [] if reel == "none" else list(walk(reel, os.path.dirname(reel), reel_skip))
sz = lambda base, fs: sum(os.path.getsize(os.path.join(base, f)) for f in fs if os.path.isfile(os.path.join(base, f)))
# This film's own capture pictures: every runtime/remotion/public/<name>/ whose <name> the beat sheet mentions.
pub_rel = []
pubroot = os.path.join(books, PUB)
if reel != "none" and os.path.isdir(pubroot):
    for name in sorted(os.listdir(pubroot)):
        if name and name in beat_text and os.path.isdir(os.path.join(pubroot, name)):
            for dp, dns, fns in os.walk(os.path.join(pubroot, name)):
                pub_rel += [os.path.relpath(os.path.join(dp, f), pubroot) for f in fns if f != ".DS_Store"]
# The portraits the scenes pick (literal seeds only; any other call is reported loudly).
PB_N = {"1x1": 89, "2x3": 24, "16x9": 9}
pb_files, pb_unresolved = set(), []
if reel != "none":
    import random
    for fn in os.listdir(reel):
        if fn.endswith(".py") and ("scenes" in fn):
            src = open(os.path.join(reel, fn)).read()
            for m in re.finditer(r"professor_bear\(\s*\"(1x1|2x3|16x9)\"([^)]*)\)", src):
                sm = re.search(r"seed\s*=\s*\"([^\"]+)\"", m.group(2))
                if not sm: pb_unresolved.append(fn + ": " + m.group(0)[:60]); continue
                k = random.Random(sm.group(1)).randint(1, PB_N[m.group(1)])
                pb_files.add(f"professor-bear-{m.group(1)}-{k:02d}.png")
pb_dir = os.path.join(books, "brutalist.art", "professor-bear")
pb_have = sorted(f for f in pb_files if os.path.isfile(os.path.join(pb_dir, f)))
pb_missing = sorted(set(pb_files) - set(pb_have))
if pb_unresolved: print("WARNING: portrait picks with no literal seed (not carried):", pb_unresolved)
if pb_missing: print("WARNING: portrait files not found in the library:", pb_missing)
print(f"portraits the scenes use: {len(pb_have)} file(s), {sum(os.path.getsize(os.path.join(pb_dir, f)) for f in pb_have)/1e6:.0f} MB")
stage = os.path.join(out, "_stage", slug, "_public")
import shutil
shutil.rmtree(os.path.join(out, "_stage"), ignore_errors=True)
os.makedirs(stage, exist_ok=True)
for rel in pub_rel:
    dst = os.path.join(stage, rel); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(os.path.join(pubroot, rel), dst)
pstage = os.path.join(out, "_stage", slug, "_portraits"); os.makedirs(pstage, exist_ok=True)
for f in pb_have: shutil.copy2(os.path.join(pb_dir, f), os.path.join(pstage, f))
print(f"film capture folders carried in the reel archive: {len(pub_rel)} files")
tk_mb, reel_mb = sz(books, tk_files) / 1e6, sz(os.path.dirname(reel), reel_files) / 1e6 + sum(os.path.getsize(os.path.join(pubroot, r)) for r in pub_rel) / 1e6 + sum(os.path.getsize(os.path.join(pb_dir, f)) for f in pb_have) / 1e6
print(f"projected: toolkit {len(tk_files)} files {tk_mb:.0f} MB uncompressed; reel {len(reel_files)} files {reel_mb:.0f} MB; portrait: {portrait or 'none'}")
if tk_mb + reel_mb > maxmb:
    sys.exit(f"REFUSED: {tk_mb + reel_mb:.0f} MB is over --max-mb {maxmb}. Check the exclude lists.")
open(os.path.join(out, "toolkit.list"), "w").write("\0".join(tk_files) + "\0")
open(os.path.join(out, "reel.list"), "w").write("\0".join(reel_files) + "\0")
PY

COPYFILE_DISABLE=1 tar --no-xattrs -czf "$OUT/toolkit-code.tar.gz" -C "$BOOKS" --null -T "$OUT/toolkit.list"
PARTS="toolkit-code.tar.gz"
if [ "$REEL" != none ]; then COPYFILE_DISABLE=1 tar --no-xattrs -cf "$OUT/reel.tar" -C "$(dirname "$REEL")" --null -T "$OUT/reel.list" && COPYFILE_DISABLE=1 tar --no-xattrs -rf "$OUT/reel.tar" -C "$OUT/_stage" "$SLUG/_public" "$SLUG/_portraits" && gzip -f "$OUT/reel.tar" && mv "$OUT/reel.tar.gz" "$OUT/reel.tar.gz.tmp" && mv "$OUT/reel.tar.gz.tmp" "$OUT/reel.tar.gz"; PARTS="$PARTS reel.tar.gz"; fi
rm -rf "$OUT/toolkit.list" "$OUT/reel.list" "$OUT/_stage"
( cd "$OUT" && ls -lh $PARTS | awk '{print $5, $NF}' && shasum -a 256 $PARTS | tee SHA256SUMS )
echo "reel slug: $SLUG"
