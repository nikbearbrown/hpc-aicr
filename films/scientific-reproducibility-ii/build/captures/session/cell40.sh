cd rnaseq_project

# Get the hash of the first analysis commit
HASH=$(git log --oneline --grep='MIN_COUNT=10' | awk '{print $1}')
echo "Restoring script from commit: $HASH"

# Restore just that one file — working tree only, not a full checkout
git checkout $HASH -- scripts/filter_and_summarise.sh

grep 'MIN_COUNT\|fc >=' scripts/filter_and_summarise.sh

bash scripts/filter_and_summarise.sh

# Status breakdown at MIN_COUNT=10 
awk 'NR>1 {print $5}' results/summary.tsv | sort | uniq -c

# Restore current version
git checkout HEAD -- scripts/filter_and_summarise.sh