cd rnaseq_project

bash scripts/filter_and_summarise.sh

# Results with FC cutoff 1.5 from above change
awk 'NR>1 {print $5}' results/summary.tsv | sort | uniq -c

git add scripts/filter_and_summarise.sh results/summary.tsv results/run.log
git commit -m 'explore: relax FC cutoff to 1.5/0.67 (reviewer suggestion)'