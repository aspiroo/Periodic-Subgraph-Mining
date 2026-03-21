"""
Stage 3, Step 2: Union EDGES (legacy name: union_genes)

Reads ListMiner output files:
  results/list_miner/list_miner_outputs_with_edges/p{period}s{support}.txt

Each file contains bracket content only (flattened edge list), one line per subgraph:
  e1 e2 e3 ...

This step unions all edge IDs used by any subgraph for each (period, support) combo.

IMPORTANT:
- Do NOT use the old heuristic "id > 588".
- Instead, keep only edge IDs that actually exist in outputWithEdgeNum.txt.
This prevents mixed-ID formats and corrupted huge integers from polluting outputs.
"""

from __future__ import annotations
from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parents[2]

# (period, suffix_in_filenames, max_support)
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
INPUT_DIR  = REPO_ROOT / "results" / "list_miner" / "list_miner_outputs_with_edges"
EDGE_MAP   = REPO_ROOT / "data" / "processed" / "outputWithEdgeNum.txt"
OUTPUT_DIR = REPO_ROOT / "results" / "list_miner" / "union_genes"
TEMP_DIR   = REPO_ROOT / "results" / "temp"

if TEMP_DIR.exists():
    shutil.rmtree(TEMP_DIR)
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_valid_edge_ids(edge_map_file: Path) -> set[int]:
    valid: set[int] = set()
    with edge_map_file.open("r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            parts = raw.split()
            if not parts:
                continue
            try:
                valid.add(int(parts[0]))
            except ValueError:
                continue
    return valid


def main() -> int:
    if not EDGE_MAP.exists():
        print(f"ERROR: missing edge map: {EDGE_MAP}")
        return 1

    valid_edges = load_valid_edge_ids(EDGE_MAP)
    if not valid_edges:
        print(f"ERROR: parsed 0 edge IDs from {EDGE_MAP}")
        return 1

    min_edge, max_edge = min(valid_edges), max(valid_edges)
    print(f"Loaded {len(valid_edges)} valid edge IDs from {EDGE_MAP} (range {min_edge}..{max_edge})")

    for period, suffix, max_support in PERIOD_CONFIGS:
        for s in range(3, max_support + 1):
            input_file  = INPUT_DIR  / f"p{period}s{s}.txt"
            output_file = OUTPUT_DIR / f"p{period}s{s}.txt"

            if not input_file.exists():
                print(f"  SKIP (missing input): {input_file.name}")
                continue

            kept: set[int] = set()
            total_tokens = 0
            dropped = 0

            with input_file.open("r", encoding="utf-8", errors="ignore") as fin:
                for line in fin:
                    for tok in line.split():
                        try:
                            x = int(tok)
                        except ValueError:
                            continue
                        total_tokens += 1
                        if x in valid_edges:
                            kept.add(x)
                        else:
                            dropped += 1

            with output_file.open("w", encoding="utf-8") as f:
                # space-separated, sorted for reproducibility
                f.write(" ".join(map(str, sorted(kept))))

            print(
                f"  OK  p{period}s{s} -> kept {len(kept)} unique edges "
                f"(dropped {dropped}/{total_tokens} tokens) -> {output_file.name}"
            )

    print("\nDone: 02_union_genes.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())