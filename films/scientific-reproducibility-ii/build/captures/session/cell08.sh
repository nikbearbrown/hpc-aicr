cd "/private/tmp/claude-501/-Users-bear-Documents-CoWork/f1dde776-b09c-4df5-88a6-6d6593996204/scratchpad/sr2/work2"
mkdir -p rnaseq_project/{data,results,scripts,slurm}
cd rnaseq_project

awk 'BEGIN {
    srand(42)
    print "gene_id\tctrl_1\tctrl_2\tctrl_3\ttreat_1\ttreat_2\ttreat_3"
    for (i = 1; i <= 200; i++) {
        base = int(rand() * 2000)
        fold = (rand() > 0.8) ? 3 : 1
        printf "GENE%04d", i
        for (j = 1; j <= 3; j++)
            printf "\t%d", int(base * (0.8 + rand()*0.4))
        for (j = 1; j <= 3; j++)
            printf "\t%d", int(base * fold * (0.8 + rand()*0.4))
        printf "\n"
    }
}' /dev/null > data/counts.tsv

# Check on "Dimensions"
echo "  Rows (genes + header): $(wc -l < data/counts.tsv)"
echo "  Columns:               $(head -1 data/counts.tsv | awk '{print NF}')"

# First 5 rows of the file we have just created
head -5 data/counts.tsv | column -t