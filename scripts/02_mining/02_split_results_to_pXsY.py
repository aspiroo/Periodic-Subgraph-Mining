"""
Split ListMiner output into pXsY.txt files matching legacy list_miner_outputs_with_edges format.

Input:  results/list_miner/default_run/results.txt
        Each subgraph produces TWO lines:
            <start> <end> <support> <period>
            [edge1 edge2 edge3 edge4 ...]

Output: results/list_miner/list_miner_outputs_with_edges/p{period}s{support}.txt
        Each output line contains only the bracket content (flattened edge list), e.g.:
            4 5 8 9

Repository: aspiroo/Periodic-Subgraph-Mining
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from collections import defaultdict
import shutil

out_dir = Path('results/list_miner/list_miner_outputs_with_edges')
if out_dir.exists():
    shutil.rmtree(out_dir)
out_dir.mkdir(parents=True)
print("Cleared list_miner_outputs_with_edges")


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "results" / "list_miner" / "default_run"
OUTPUT_DIR = REPO_ROOT / "results" / "list_miner" / "list_miner_outputs_with_edges"


HEADER_RE = re.compile(r"^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$")
EDGES_RE = re.compile(r"^\s*\[\s*(.*?)\s*\]\s*$")


def main() -> int:
    results_file = RESULTS_DIR / "results.txt"
    if not results_file.exists():
        print(f"ERROR: results.txt not found at {results_file}")
        print("  Run scripts/02_mining/01_run_listminer_c++.py first.")
        return 1

    print(f"Reading: {results_file}")

    # bucket[period][support] -> list[str edges]
    buckets: dict[int, dict[int, list[str]]] = defaultdict(lambda: defaultdict(list))

    pending_support: int | None = None
    pending_period: int | None = None
    seen_headers = 0
    seen_edges = 0

    with results_file.open("r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.rstrip("\n")

            m = HEADER_RE.match(line)
            if m:
                # start/end not needed for output files
                support = int(m.group(3))
                period = int(m.group(4))
                pending_support = support
                pending_period = period
                seen_headers += 1
                continue

            m = EDGES_RE.match(line)
            if m:
                edges_str = m.group(1).strip()  # inside brackets
                if pending_support is None or pending_period is None:
                    print("WARNING: edge list encountered without a preceding header; skipping.")
                    continue

                # store and clear pending
                buckets[pending_period][pending_support].append(edges_str)
                pending_support = None
                pending_period = None
                seen_edges += 1
                continue

            # ignore anything else (blank lines etc.)

    if not buckets:
        print("ERROR: No subgraphs parsed from results.txt.")
        print(f"  Seen headers: {seen_headers}, seen edge lines: {seen_edges}")
        print("  Expected alternating lines: '<start> <end> <support> <period>' then '[ ... ]'")
        return 1

    if seen_headers != seen_edges:
        print(f"WARNING: header/edge count mismatch: headers={seen_headers}, edges={seen_edges}")
        print("  (This usually means the file was truncated or contains stray lines.)")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_files = 0
    total_entries = 0

    for period in sorted(buckets.keys()):
        for support in sorted(buckets[period].keys()):
            entries = buckets[period][support]
            out_file = OUTPUT_DIR / f"p{period}s{support}.txt"
            with out_file.open("w", encoding="utf-8") as out:
                for edges_str in entries:
                    out.write(edges_str + "\n")

            total_files += 1
            total_entries += len(entries)
            print(f"  Wrote {len(entries):>5} entries -> {out_file.name}")

    print(f"\nDone: {total_files} files, {total_entries} total subgraphs")
    print(f"Output dir: {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())