cd rnaseq_project

# Commit the run outputs (summary + log are allowed through .gitignore)
git add results/summary.tsv results/run.log
git commit -m 'analysis: baseline run, MIN_COUNT=10, 200 genes, threshold=10'

git log --oneline