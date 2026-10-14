cd rnaseq_project

git merge explore/fc-cutoff-1.5 --no-ff \
  -m 'Merge explore/fc-cutoff-1.5: FC >= 1.5 for revised submission'

# Full history 
git log --oneline --graph --all

# once the project is merged, then we dont need the exploration branch anymore and thus we will delete it
git branch -d explore/fc-cutoff-1.5