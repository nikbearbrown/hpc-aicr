#!/usr/bin/env bash
# pack_for_cluster.sh <books-dir> <reel-dir> <out-dir> [--max-mb 3000]
# Run on YOUR computer. Builds two archives for one film (nothing is sent anywhere):
#   toolkit-code.tar.gz   the brutalist.art toolkit WITHOUT node_modules, models, other films' assets, media, .git
#                         (node_modules is rebuilt on the cluster: your computer may be arm64 and Explorer is x86_64)
#   reel.tar.gz           the film folder WITHOUT rendered output (keeps beat_sheet, scenes, mp3 + timings, opening fields)
# The file list is built explicitly (a pruned walk), the projected size is printed BEFORE anything is archived,
# and the script refuses if it exceeds --max-mb. UNTESTED on the cluster; packing was tested locally.
set -euo pipefail
BOOKS=${1:?books dir}; REEL=${2:?reel dir}; OUT=${3:?out dir}; MAXMB=3000
[ "${4:-}" = "--max-mb" ] && MAXMB=${5:?}
mkdir -p "$OUT"; BOOKS=$(cd "$BOOKS" && pwd); REEL=$(cd "$REEL" && pwd); OUT=$(cd "$OUT" && pwd)
[ -d "$BOOKS/brutalist.art/runtime" ] || { echo "no toolkit at $BOOKS/brutalist.art"; exit 1; }
SLUG=$(basename "$REEL")

python3 -I - "$BOOKS" "$REEL" "$OUT" "$MAXMB" <<'PY'
import os, sys, json, fnmatch
books, reel, out, maxmb = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
slug = os.path.basename(reel)
MEDIA = (".mp4", ".mp3", ".wav", ".mov", ".mkv", ".m4a")
TK_SKIP = ["brutalist.art/.git", "brutalist.art/youtube", "brutalist.art/svg", "brutalist.art/renders", "brutalist.art/reports",
           "brutalist.art/professor-bear", "brutalist.art/runtime/models", "brutalist.art/runtime/remotion/node_modules",
           "brutalist.art/runtime/remotion/public/professor-bear"]
TK_GLOB = ["brutalist.art/runtime/remotion/public/seis*", "brutalist.art/runtime/remotion/public/claude-liam-lecture-*",
           "brutalist.art/runtime/remotion/public/figma-*", "brutalist.art/runtime/remotion/public/lecture-*"]
REEL_SKIP = {"media", "manim", "clips", "exports", "mp4", "_qc", "_superseded"}

def walk(root_dir, rel_root, skip_fn):
    for dp, dns, fns in os.walk(root_dir, followlinks=False):
        rel = os.path.relpath(dp, rel_root)
        dns[:] = [d for d in dns if not skip_fn(os.path.join(rel, d)) and d not in ("__pycache__",) and not d.startswith(".")]   # hidden dirs (.git, .repoloop run workspaces: GBs) never go
        for f in fns:
            r = os.path.join(rel, f)
            if f == ".DS_Store" or skip_fn(r): continue
            yield r

def tk_skip(r):
    return r in TK_SKIP or any(fnmatch.fnmatch(r, g) for g in TK_GLOB) or r.lower().endswith(MEDIA)
def reel_skip(r):
    parts = r.split(os.sep)
    return (len(parts) > 1 and parts[1] in REEL_SKIP) or r.endswith("slate.mp4") or (r.lower().endswith(MEDIA) and "/mp3/" not in "/" + r.replace(os.sep, "/") + "/" and not r.replace(os.sep, "/").startswith(slug + "/mp3/"))

tk_files = list(walk(os.path.join(books, "brutalist.art"), books, tk_skip))
portrait = ""
of = os.path.join(reel, "opening", "opening-fields.json")
if os.path.exists(of):
    p = json.load(open(of)).get("portrait_path", "")
    if p and os.path.exists(p) and p.startswith(books + os.sep): portrait = os.path.relpath(p, books); tk_files.append(portrait)
reel_files = list(walk(reel, os.path.dirname(reel), reel_skip))
sz = lambda base, fs: sum(os.path.getsize(os.path.join(base, f)) for f in fs if os.path.isfile(os.path.join(base, f)))
tk_mb, reel_mb = sz(books, tk_files) / 1e6, sz(os.path.dirname(reel), reel_files) / 1e6
print(f"projected: toolkit {len(tk_files)} files {tk_mb:.0f} MB uncompressed; reel {len(reel_files)} files {reel_mb:.0f} MB; portrait: {portrait or 'none'}")
if tk_mb + reel_mb > maxmb:
    sys.exit(f"REFUSED: {tk_mb + reel_mb:.0f} MB is over --max-mb {maxmb}. Check the exclude lists.")
open(os.path.join(out, "toolkit.list"), "w").write("\0".join(tk_files) + "\0")
open(os.path.join(out, "reel.list"), "w").write("\0".join(reel_files) + "\0")
PY

tar -czf "$OUT/toolkit-code.tar.gz" -C "$BOOKS" --null -T "$OUT/toolkit.list"
tar -czf "$OUT/reel.tar.gz" -C "$(dirname "$REEL")" --null -T "$OUT/reel.list"
rm -f "$OUT/toolkit.list" "$OUT/reel.list"
( cd "$OUT" && ls -lh toolkit-code.tar.gz reel.tar.gz | awk '{print $5, $NF}' && shasum -a 256 toolkit-code.tar.gz reel.tar.gz | tee SHA256SUMS )
echo "reel slug: $SLUG"
