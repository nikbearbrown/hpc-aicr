import json, subprocess, sys, os, pathlib, re
S = pathlib.Path('/private/tmp/claude-501/-Users-bear-Documents-CoWork/f1dde776-b09c-4df5-88a6-6d6593996204/scratchpad/sr2')
nb = json.load(open('<books>/hpc-aicr/Scientific-Reproducibility-II-2026/scientific-reproducibility-II.ipynb'))
work = S / 'work2'; home = S / 'home2'
work.mkdir(exist_ok=True); home.mkdir(exist_ok=True)
log = S / 'transcripts2'; log.mkdir(exist_ok=True)
env = dict(os.environ, HOME=str(home), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=str(home/'.gitconfig'), LC_ALL='en_US.UTF-8', GIT_PAGER='cat', PAGER='cat')
def patch(i, src):
    if i == 8: src = src.replace('cd /projects/username', 'cd "%s"' % work)
    if i == 12: src += "\ngit branch -M main\n"
    if i == 14:
        src = src.replace("\nresults/\n", "\nresults/*\n")
        src = re.sub(r"(!results/\S+)\s+#.*", r"\1", src)
    if i == 37: src = src[:src.index('# Once things look good')]
    src = src.replace("sed -i '", "sed -i '' '")
    return src
for a in sys.argv[1:]:
    i = int(a)
    src = patch(i, ''.join(nb['cells'][i]['source']))
    (log / f'cell{i:02d}.sh').write_text(src)
    r = subprocess.run(['bash', '-c', src], cwd=work, env=env, capture_output=True, text=True)
    (log / f'cell{i:02d}.out').write_text(r.stdout + (('\n[stderr]\n' + r.stderr) if r.stderr else '') + f'\n[exit {r.returncode}]\n')
    print(f'--- cell {i} exit {r.returncode}'); print(r.stdout[-2500:]); print(r.stderr[-600:])
