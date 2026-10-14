# Apply the prompt function for this session only (no ~/.bashrc edit needed)
git_branch() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null | awk '{printf " (" $0 ")"}'
}

cd rnaseq_project

# Let's make sure we are on main branch
echo "rnaseq_project$(git_branch)"

# creating and switching to demo/promt-test branch
git switch -c demo/prompt-test 2>/dev/null

# switching back to main and deleting the test branch
git switch main
git branch -d demo/prompt-test