"""
Stage 3, Step 6: Generate Development Genes
Reads justDevelopmentwithLineNum.txt and geneNamesWithLineNum.txt,
and produces justDevelopmentWithGeneName.txt — the gene name list
for the 588 development genes used as the threshold in node filtering.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

GENE_MAP_DIR = REPO_ROOT / "data" / "processed" / "gene_mappings"
DEV_FILE     = GENE_MAP_DIR / "justDevelopmentwithLineNum.txt"
NAMES_FILE   = GENE_MAP_DIR / "geneNamesWithLineNum.txt"
OUTPUT_FILE  = GENE_MAP_DIR / "justDevelopmentWithGeneName.txt"

if not DEV_FILE.exists():
    raise FileNotFoundError(f"Missing: {DEV_FILE}  -- Run 01_number_gene_files.py first.")
if not NAMES_FILE.exists():
    raise FileNotFoundError(f"Missing: {NAMES_FILE} -- Run 01_number_gene_files.py first.")

reference  = DEV_FILE.read_text().strip()
filetext   = NAMES_FILE.read_text().strip()

splitReference = reference.split("\n")
splitFile      = filetext.split("\n")

list2 = []
for referenceLine in splitReference:
    referenceCells = referenceLine.split()
    for fileLine in splitFile:
        lineCells = fileLine.split()
        if referenceCells and lineCells and referenceCells[1] == lineCells[0]:
            list2.append(lineCells[1])

with open(OUTPUT_FILE, "w") as f:
    for item in list2:
        f.write(f"{item}\n")

print(f"Done: wrote {len(list2)} development gene names -> {OUTPUT_FILE}")