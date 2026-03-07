"""
Split the dual-format results.txt (produced by the updated Miner_new.cpp)
into separate pXsY.txt files matching the legacy list_miner_outputs_with_edges format.

Input:  results/list_miner/default_run/results.txt
        Each subgraph produces TWO lines:
            36 50 3 7                              <- compact: start end support period
            start 36 psup 3 p 7 m 1 [4 5 8 9]    <- verbose: edge-list

Output: results/list_miner/list_miner_outputs_with_edges/p{period}s{support}.txt
        Each file contains only the edge-list bracket content, one line per subgraph:
            4 5 8 9

Repository: aspiroo/Periodic-Subgraph-Mining
"""

import sys
from pathlib import Path
from collections import defaultdict

REPO_ROOT   = Path(__file__).parent.parent.parent
RESULTS_DIR = REPO_ROOT / "results" / "list_miner" / "default_run"
OUTPUT_DIR  = REPO_ROOT / "results" / "list_miner" / "list_miner_outputs_with_edges"

def main():
    results_file = RESULTS_DIR / "results.txt"

    if not results_file.exists():
        print(f"ERROR: results.txt not found at {results_file}")
        print("  Run compile_listminer.py first.")
        sys.exit(1)

    print(f"Reading: {results_file}")

    # bucket[period][support] -> list of edge strings
    buckets: dict = defaultdict(lambda: defaultdict(list))

    with open(results_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Only process verbose lines: "start X psup Y p Z m W [...]"
            if not line.startswith("start "):
                continue

            try:
                # Parse tokens: start X psup Y p Z m W [e1 e2 ...]
                bracket_start = line.index("[")
                bracket_end   = line.index("]")
                edges_str     = line[bracket_start+1 : bracket_end].strip()

                meta = line[:bracket_start].split()
                # meta = ['start','X','psup','Y','p','Z','m','W']
                support = int(meta[3])   # psup value
                period  = int(meta[5])   # p value

                buckets[period][support].append(edges_str)

            except (ValueError, IndexError) as e:
                print(f"  WARNING: could not parse line: {line[:80]}  ({e})")
                continue

    if not buckets:
        print("ERROR: No verbose 'start ...' lines found in results.txt.")
        print("  Make sure you are using the updated Miner_new.cpp that writes edge lists.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_files   = 0
    total_entries = 0

    for period in sorted(buckets.keys()):
        for support in sorted(buckets[period].keys()):
            entries    = buckets[period][support]
            out_file   = OUTPUT_DIR / f"p{period}s{support}.txt"

            with open(out_file, "w") as f:
                for edges in entries:
                    f.write(edges + "\n")

            total_files   += 1
            total_entries += len(entries)
            print(f"  Wrote {len(entries):>5} entries -> {out_file.name}")

    print(f"\nDone: {total_files} files, {total_entries} total subgraphs")
    print(f"Output dir: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()