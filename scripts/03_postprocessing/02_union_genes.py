"""
Stage 3, Step 2: Union Genes
Strips ListMiner output formatting and extracts unique node IDs (>588) for each (period, support) combo.
Covers all periods 1-10 with their respective support ranges derived from legacy data.
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

# (period, suffix_in_filenames, max_support)
# Support always starts at 3. Suffix matches legacy naming convention.
PERIOD_CONFIGS = [
    (1,  "1th",  9),
    (2,  "2nd", 12),
    (3,  "3rd",  9),
    (4,  "4th",  7),
    (5,  "5th",  6),
    (6,  "6th",  5),
    (7,  "7th",  5),
    (8,  "8th",  4),
    (9,  "9th",  4),
    (10, "10th", 4),
    
]

INPUT_DIR  = REPO_ROOT / "results" / "list_miner" / "list_miner_outputs_with_edges"
TEMP_DIR   = REPO_ROOT / "results" / "temp"
OUTPUT_DIR = REPO_ROOT / "results" / "list_miner" / "union_genes"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def remove_duplicates(values):
    seen = set()
    output = []
    for v in values:
        if v not in seen:
            output.append(v)
            seen.add(v)
    return output


delete_list = ["start", "psup", "p", "m", "[", "]", "\n"]

for period, suffix, max_support in PERIOD_CONFIGS:
    for s in range(3, max_support + 1):
        input_file  = INPUT_DIR  / f"p{period}s{s}.txt"
        temp_file   = TEMP_DIR   / f"newfile{suffix}{s}.txt"
        output_file = OUTPUT_DIR / f"p{period}s{s}.txt"

        if not input_file.exists():
            print(f"  SKIP (missing input): {input_file.name}")
            continue

        # Strip ListMiner tokens from each line
        with open(input_file, "r") as fin, open(temp_file, "w+") as fout:
            for line in fin:
                for word in delete_list:
                    line = line.replace(word, "")
                fout.write(line)

        # Read stripped file and collect unique node IDs > 588
        reference = open(temp_file).read().strip()
        str_list   = list(filter(None, reference.split()))
        convert2int = list(map(int, str_list))
        filt        = list(filter(lambda x: x > 588, convert2int))
        convert2str = list(map(str, filt))
        result      = remove_duplicates(convert2str)

        with open(output_file, "w") as f:
            f.write(" ".join(result))

        print(f"  OK  p{period}s{s} -> {len(result)} unique nodes -> {output_file.name}")

print("\nDone: 02_union_genes.py")