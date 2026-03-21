"""
Stage 3, Step 4: Remap to Gene Numbers
Maps numeric node IDs in remapped edge files to FlyBase gene IDs
using justDevelopmentwithLineNum.txt as the lookup table.
"""

from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).parent.parent.parent

PERIOD_CONFIGS = [
    (1,  "1th",  9),   # max support = 30/1 = 30, but paper caps at 9
    (2,  "2nd",  9),   # max support = 30/2 = 15, but paper caps at 9
    (3,  "3rd",  9),   # max support = 30/3 = 10
    (4,  "4th",  7),   # max support = 30/4 = 7
    (5,  "5th",  6),   # max support = 30/5 = 6
    (6,  "6th",  5),   # max support = 30/6 = 5
    (7,  "7th",  4),   # max support = 30/7 = 4
    (8,  "8th",  3),   # max support = 30/8 = 3
    (9,  "9th",  3),   # max support = 30/9 = 3
    (10, "10th", 3),   # max support = 30/10 = 3
]

REMAPPED_DIR = REPO_ROOT / "results" / "components" / "remapped"
GENE_MAP     = REPO_ROOT / "data" / "processed" / "gene_mappings" / "justDevelopmentwithLineNum.txt"
OUTPUT_DIR   = REPO_ROOT / "results" / "components" / "gene_numbers"

if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not GENE_MAP.exists():
    raise FileNotFoundError(f"Gene map not found: {GENE_MAP}")

filetext  = GENE_MAP.read_text().strip()
splitFile = filetext.split("\n")

for period, suffix, max_support in PERIOD_CONFIGS:
    for s in range(3, max_support + 1):
        input_file  = REMAPPED_DIR / f"output{suffix}{s}.txt"
        output_file = OUTPUT_DIR   / f"geneNumber{suffix}{s}.txt"

        if not input_file.exists():
            print(f"  SKIP (missing): {input_file.name}")
            continue

        reference     = input_file.read_text().strip()
        splitReference = reference.split("\n")

        with open(output_file, "w") as out:
            for referenceLine in splitReference:
                referenceCells = referenceLine.split()
                if len(referenceCells) < 3:
                    continue
                value1 = value2 = None
                for fileLine in splitFile:
                    lineCells = fileLine.split()
                    if not lineCells:
                        continue
                    if referenceCells[2] == lineCells[0]:
                        value1 = lineCells[1]
                    if referenceCells[1] == lineCells[0]:
                        value2 = lineCells[1]
                if value1 and value2:
                    out.write(f"{value2}\t{value1}\n")

        print(f"  OK  p{period}s{s} -> {output_file.name}")

print("\nDone: 04_remap_to_gene_numbers.py")
