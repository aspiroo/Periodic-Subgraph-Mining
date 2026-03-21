"""
Stage 3, Step 3: Remap Edges to Graph
For each union-genes file, looks up each edge number in outputWithEdgeNum.txt
and writes the matching edge rows to an output file per (period, support).
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

UNION_GENES_DIR = REPO_ROOT / "results" / "list_miner" / "union_genes"
EDGE_MAP_FILE   = REPO_ROOT / "data" / "processed" / "outputWithEdgeNum.txt"
OUTPUT_DIR      = REPO_ROOT / "results" / "components" / "remapped"

if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not EDGE_MAP_FILE.exists():
    raise FileNotFoundError(f"Edge map file not found: {EDGE_MAP_FILE}")

filetext  = EDGE_MAP_FILE.read_text().strip()
splitFile = filetext.split("\n")

for period, suffix, max_support in PERIOD_CONFIGS:
    for s in range(3, max_support + 1):
        input_file  = UNION_GENES_DIR / f"p{period}s{s}.txt"
        output_file = OUTPUT_DIR      / f"output{suffix}{s}.txt"

        if not input_file.exists():
            print(f"  SKIP (missing): {input_file.name}")
            continue

        reference   = input_file.read_text().strip()
        convert2int = list(map(int, filter(None, reference.split())))
        filt        = list(filter(lambda x: x > 588, convert2int))
        convert2str = list(map(str, filt))

        with open(output_file, "w") as out:
            for ref_id in convert2str:
                for fileLine in splitFile:
                    lineCells = fileLine.split()
                    if lineCells and lineCells[0] == ref_id:
                        out.write(fileLine + "\n")

        print(f"  OK  p{period}s{s} -> {output_file.name}")

print("\nDone: 03_remap_edges_to_graph.py")
