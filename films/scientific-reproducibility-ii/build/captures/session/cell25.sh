cd rnaseq_project

# Make a small change: raise the threshold
sed -i '' 's/MIN_COUNT=10/MIN_COUNT=20/' scripts/filter_and_summarise.sh

# What changed? 
git diff scripts/filter_and_summarise.sh