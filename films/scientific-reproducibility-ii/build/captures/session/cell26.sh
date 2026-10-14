cd rnaseq_project

bash scripts/filter_and_summarise.sh

# Status breakdown with MIN_COUNT=20 
awk 'NR>1 {print $5}' results/summary.tsv | sort | uniq -c

git add scripts/filter_and_summarise.sh results/summary.tsv results/run.log
git commit -m 'analysis: raise MIN_COUNT 10->20, stricter low-count filter'

git log --oneline