"""
TABLE I (Paper):
Number of Unique Genes present in the periodic subgraphs for each parameter combination.

Format confirmed:
- p{p}s{s}.txt  : space-separated edge numbers (>= 589) on one or more lines per subgraph
- outputWithEdgeNum.txt : edge_id <TAB> gene1_id <TAB> gene2_id  (gene IDs are 1-588)

Pipeline:
  1. Load edge_id -> (gene1, gene2) from outputWithEdgeNum.txt
  2. For each (period, support): read all edge numbers from p{p}s{s}.txt,
     look up both gene endpoints, count unique gene IDs.
"""

from __future__ import annotations

import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR      = REPO_ROOT / "results" / "list_miner" / "list_miner_outputs_with_edges"
EDGE_MAP_FILE  = REPO_ROOT / "data" / "processed" / "outputWithEdgeNum.txt"
OUT_DIR        = REPO_ROOT / "results" / "tables"

# Paper grid (Table I rows = periods 1-9, cols = supports 3-9)
DEV_GENES_FILE = REPO_ROOT / "data" / "raw" / "Just_development.txt"

# Paper grid (Table I rows = periods 1-9, cols = supports 3-9)
PERIODS  = list(range(1, 10))   # 1..9
SUPPORTS = list(range(3, 10))   # 3..9


def load_dev_genes(path: Path) -> set[int]:
    """Load the 588 development gene IDs (one per line)."""
    genes: set[int] = set()
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            tok = raw.strip()
            if tok:
                genes.add(int(tok))
    return genes


def load_edge_map(path: Path) -> dict[int, tuple[int, int]]:
    """Return {edge_id: (gene1_id, gene2_id)} from outputWithEdgeNum.txt."""
    edge_map: dict[int, tuple[int, int]] = {}
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            parts = raw.split()
            if len(parts) < 3:
                continue
            try:
                eid  = int(parts[0])
                g1   = int(parts[1])
                g2   = int(parts[2])
                edge_map[eid] = (g1, g2)
            except ValueError:
                continue
    return edge_map


def count_unique_genes(fp: Path, edge_map: dict[int, tuple[int, int]]) -> int:
    """Read all edge numbers from fp, resolve to gene IDs, count only development genes."""
    unique_genes: set[int] = set()
    with fp.open("r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            for tok in raw.split():
                try:
                    eid = int(tok)
                except ValueError:
                    continue
                if eid in edge_map:
                    g1, g2 = edge_map[eid]
                    unique_genes.add(g1)
                    unique_genes.add(g2)
    return len(unique_genes)


def main() -> int:
    if not INPUT_DIR.exists():
        print(f"ERROR: missing input directory: {INPUT_DIR}")
        return 1
    if not EDGE_MAP_FILE.exists():
        print(f"ERROR: missing edge map: {EDGE_MAP_FILE}")
        return 1

    print(f"Loading edge map from: {EDGE_MAP_FILE}")
    edge_map = load_edge_map(EDGE_MAP_FILE)
    print(f"  Loaded {len(edge_map)} edges.")

    print(f"Loading development genes from: {DEV_GENES_FILE}")
    dev_genes = load_dev_genes(DEV_GENES_FILE)
    print(f"  Loaded {len(dev_genes)} development genes.")

    # table[p][s] = count string (or "" if file missing/empty)
    table: dict[int, dict[int, str]] = {p: {s: "" for s in SUPPORTS} for p in PERIODS}

    for p in PERIODS:
        for s in SUPPORTS:
            fp = INPUT_DIR / f"p{p}s{s}.txt"
            if not fp.exists():
                continue
            count = count_unique_genes(fp, edge_map)
            table[p][s] = str(count) if count > 0 else ""
            print(f"  p{p}s{s}: {count} unique genes")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # CSV
    csv_path = OUT_DIR / "table1.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Period \\ Support", *SUPPORTS])
        for p in PERIODS:
            w.writerow([p, *[table[p][s] for s in SUPPORTS]])
    print(f"\nWrote: {csv_path}")

    # Markdown
    md_path = OUT_DIR / "table1.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# TABLE I\n")
        f.write("Number of Unique Genes present in the periodic subgraphs for each parameter combination.\n\n")
        header = ["Periods \\ Supports", *[str(s) for s in SUPPORTS]]
        f.write("| " + " | ".join(header) + " |\n")
        f.write("| " + " | ".join(["---"] * len(header)) + " |\n")
        for p in PERIODS:
            row = [str(p)] + [table[p][s] for s in SUPPORTS]
            f.write("| " + " | ".join(row) + " |\n")
    print(f"Wrote: {md_path}")

    # Pretty-print to terminal
    print("\n--- TABLE I ---")
    col_w = 6
    header_str = f"{'P\\S':<5}" + "".join(f"{s:>{col_w}}" for s in SUPPORTS)
    print(header_str)
    print("-" * len(header_str))
    for p in PERIODS:
        row_str = f"{p:<5}" + "".join(f"{table[p][s]:>{col_w}}" for s in SUPPORTS)
        print(row_str)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())