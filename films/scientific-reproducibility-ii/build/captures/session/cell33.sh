cd rnaseq_project

# Switch back to main — original script is exactly as you left it
git switch main

# FC cutoffs in main script 
grep 'fc >=' scripts/filter_and_summarise.sh