"""
Generate "Table 1" (paper-style summary) from ListMiner outputs.

Assumption (based on this repo's pipeline and your outputs):
- You have files:
    results/list_miner/list_miner_outputs_with_edges/p{period}s{support}.txt
  where each line is one mined subgraph (flattened edge list).

This script creates a table of counts (#subgraphs) for each period/support pair.

Outputs:
- results/tables/table1_counts_by_period_support.csv
- results/tables/table1_counts_by_period_support.md
"""

from __future__ import annotations

import re
import csv
from pathlib import Path
from collections import defaultdict


REPO_ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = REPO_ROOT / "results" / "list_miner" / "list_miner_outputs_with_edges"
OUT_DIR = REPO_ROOT / "results" / "tables"

FNAME_RE = re.compile(r"^p(?P<p>\d+)s(?P<s>\d+)\.txt$")


def count_nonempty_lines(path: Path) -> int:
    n = 0
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def main() -> int:
    if not INPUT_DIR.exists():
        print(f"ERROR: input directory not found: {INPUT_DIR}")
        print("Expected files like: p10s3.txt, p1s3.txt, ...")
        return 1

    files = sorted([p for p in INPUT_DIR.iterdir() if p.is_file() and FNAME_RE.match(p.name)])
    if not files:
        print(f"ERROR: no p*s*.txt files found in {INPUT_DIR}")
        return 1

    # counts[(p, s)] = number of subgraphs (lines)
    counts: dict[tuple[int, int], int] = {}
    periods = set()
    supports = set()

    for fp in files:
        m = FNAME_RE.match(fp.name)
        assert m
        p = int(m.group("p"))
        s = int(m.group("s"))
        periods.add(p)
        supports.add(s)
        counts[(p, s)] = count_nonempty_lines(fp)

    periods = sorted(periods)
    supports = sorted(supports)

    # Build a dense matrix with 0 default
    matrix = defaultdict(lambda: defaultdict(int))  # matrix[p][s] = count
    for (p, s), c in counts.items():
        matrix[p][s] = c

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---------- CSV ----------
    csv_path = OUT_DIR / "table1_counts_by_period_support.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["period \\ support", *supports, "row_total"])
        for p in periods:
            row = [p] + [matrix[p][s] for s in supports]
            w.writerow([*row, sum(row[1:])])

        col_totals = [sum(matrix[p][s] for p in periods) for s in supports]
        w.writerow(["col_total", *col_totals, sum(col_totals)])

    # ---------- Markdown ----------
    md_path = OUT_DIR / "table1_counts_by_period_support.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Table 1: Number of periodic subgraphs by period (p) and support (s)\n\n")
        f.write(f"Input directory: `{INPUT_DIR.as_posix()}`\n\n")

        header = ["p \\ s", *[str(s) for s in supports], "Total"]
        f.write("| " + " | ".join(header) + " |\n")
        f.write("| " + " | ".join(["---"] * len(header)) + " |\n")

        grand_total = 0
        for p in periods:
            row_counts = [matrix[p][s] for s in supports]
            row_total = sum(row_counts)
            grand_total += row_total
            f.write("| " + " | ".join([str(p), *map(str, row_counts), str(row_total)]) + " |\n")

        col_totals = [sum(matrix[p][s] for p in periods) for s in supports]
        f.write("| " + " | ".join(["Total", *map(str, col_totals), str(sum(col_totals))]) + " |\n")

        f.write(f"\nGrand total subgraphs: **{grand_total}**\n")

    print(f"Wrote: {csv_path}")
    print(f"Wrote: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())