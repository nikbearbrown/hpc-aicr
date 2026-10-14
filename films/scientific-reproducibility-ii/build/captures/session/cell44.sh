cd rnaseq_project

git add slurm/
git commit -m 'ci: Slurm job script with uncommitted-change guard'

git log --oneline --graph --all