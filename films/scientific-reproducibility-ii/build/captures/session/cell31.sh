cd rnaseq_project

# Modify the fold-change cutoffs in the script
sed -i '' 's/fc >= 2.0/fc >= 1.5/' scripts/filter_and_summarise.sh
sed -i '' 's/fc <= 0.5/fc <= 0.67/' scripts/filter_and_summarise.sh

# Check the change before committing
git diff scripts/filter_and_summarise.sh