"""
Stage 3, Step 5: Remap to Gene Names
Converts FlyBase gene IDs to human-readable gene symbols.
Outputs both .txt (tab-delimited) and .xlsx per (period, support).
"""

import csv
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

GENE_NUMBERS_DIR = REPO_ROOT / "results" / "components" / "gene_numbers"
NAME_MAP         = REPO_ROOT / "data" / "processed" / "gene_mappings" / "geneNamesWithLineNum.txt"
OUTPUT_DIR       = REPO_ROOT / "results" / "components" / "gene_names"

if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not NAME_MAP.exists():
    raise FileNotFoundError(f"Gene name map not found: {NAME_MAP}")

filetext  = NAME_MAP.read_text().strip()
splitFile = filetext.split("\n")

for period, suffix, max_support in PERIOD_CONFIGS:
    for s in range(3, max_support + 1):
        input_file   = GENE_NUMBERS_DIR / f"geneNumber{suffix}{s}.txt"
        output_txt   = OUTPUT_DIR / f"p{period}s{s}.txt"
        output_xlsx  = OUTPUT_DIR / f"p{period}s{s}.xlsx"

        if not input_file.exists():
            print(f"  SKIP (missing): {input_file.name}")
            continue

        reference      = input_file.read_text().strip()
        splitReference = reference.split("\n")

        list1 = ["gene1"]
        list2 = ["gene2"]

        for referenceLine in splitReference:
            referenceCells = referenceLine.split()
            for fileLine in splitFile:
                lineCells = fileLine.split()
                if not lineCells:
                    continue
                if referenceCells and referenceCells[0] == lineCells[0]:
                    list1.append(lineCells[1])
                if len(referenceCells) > 1 and referenceCells[1] == lineCells[0]:
                    list2.append(lineCells[1])

        # Write .txt
        with open(output_txt, "w", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerows(zip(list1, list2))

        # Write .xlsx
        try:
            from xlsxwriter import Workbook
            workbook = Workbook(str(output_xlsx))
            sheet    = workbook.add_worksheet()
            for row_i, (g1, g2) in enumerate(zip(list1, list2)):
                sheet.write(row_i, 0, g1)
                sheet.write(row_i, 1, g2)
            workbook.close()
        except ImportError:
            print(f"  WARNING: xlsxwriter not installed, skipping {output_xlsx.name}")

        print(f"  OK  p{period}s{s} -> {output_txt.name}")

print("\nDone: 05_remap_to_gene_names.py")
