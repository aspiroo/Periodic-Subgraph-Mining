from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

PERIOD_CONFIGS = [
    (1,  9),
    (2, 12),
    (3,  9),
    (4,  7),
    (5,  6),
    (6,  5),
    (7,  5),
    (8,  4),
    (9,  4),
    (10, 4),
]

UNION_DIR = REPO_ROOT / "results" / "list_miner" / "union_genes"

# Build table: table[period][support] = gene_count
table = {}
all_supports = sorted(set(s for _, max_s in PERIOD_CONFIGS for s in range(3, max_s + 1)))

for period, max_support in PERIOD_CONFIGS:
    table[period] = {}
    for s in range(3, max_support + 1):
        f = UNION_DIR / f"p{period}s{s}.txt"
        if f.exists():
            content = f.read_text().strip()
            genes = [g for g in content.split() if g]
            count = len(genes)
            table[period][s] = count if count > 0 else ""
        else:
            table[period][s] = ""

# Print as TSV
supports = list(range(3, 13))
header = "Period\t" + "\t".join(str(s) for s in supports)
print(header)
for period, _ in PERIOD_CONFIGS:
    row = str(period)
    for s in supports:
        row += "\t" + str(table[period].get(s, ""))
    print(row)

# Also save to file
out = REPO_ROOT / "results" / "tables" / "table1.tsv"
with open(out, "w") as f:
    f.write(header + "\n")
    for period, _ in PERIOD_CONFIGS:
        row = str(period)
        for s in supports:
            row += "\t" + str(table[period].get(s, ""))
        f.write(row + "\n")

print(f"\nSaved to {out}")