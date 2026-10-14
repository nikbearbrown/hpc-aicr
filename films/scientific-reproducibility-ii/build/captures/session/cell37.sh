cd rnaseq_project

git tag -a v1.0-submission \
  -m 'Code submitted to journal, 2025-09-01. MIN_COUNT=20, FC=1.5'

# Existing tags
git tag -l -n1

git log --oneline --graph

