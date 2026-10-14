cd rnaseq_project

cat > .gitignore << 'EOF'
# ── Results and outputs ──
results/*

# ── Raw data (large — store in institutional repository)
data/*.fastq
data/*.fastq.gz
data/*.bam
data/*.bai

# ── Log files ──
*.log
slurm-*.out

# ── Editor / OS noise ──
.DS_Store
*.swp
*~

# ── Allow small reference files through ──
!results/summary.tsv
!results/run.log
EOF

cat .gitignore