cd rnaseq_project

git add scripts/charts/
git commit -m 'feat: add bar chart and fold-change histogram (ASCII, awk-only)'

# Branch graph 
git lg

# Switching to main branch
git switch main

# Merging the exploratory brnach into main and removing the left over
git merge explore/cli-charts --no-ff -m 'Merge explore/cli-charts: bar + histogram charts'
git branch -d explore/cli-charts

# Final graph
git lg