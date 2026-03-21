"""
TABLE I (Paper):
Number of Unique Genes present in the periodic subgraphs for Each Parameter combination.

Your current p*s*.txt format (confirmed by sample):
- Each line contains node IDs in PAIRS: u1 v1 u2 v2 ...  (i.e., an edge list as endpoints)
- NOT edge numbers. Therefore DO NOT use outputWithEdgeNum.txt.

This script:
- Reads results/list_miner/list_miner_outputs_with_edges/p{p}s{s}.txt
- Extracts node IDs from pairs
- Intersects with developmental gene set from data/raw/Just_development.txt
- Counts unique developmental genes per (p,s)

Outputs (paper grid only):
- results/tables/table1_unique_development_genes_nodepairs_p1-9_s3-9.csv
- results/tables/table1_unique_development_genes_nodepairs_p1-9_s3-9.md
"""

from __future__ import annotations

import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = REPO_ROOT / "results" / "list_miner" / "list_miner_outputs_with_edges"
DEV_GENES_FILE = REPO_ROOT / "data" / "raw" / "Just_development.txt"
OUT_DIR = REPO_ROOT / "results" / "tables"

# Paper grid
PERIODS = list(range(1, 10))   # 1..9
SUPPORTS = list(range(3, 10))  # 3..9


def load_dev_gene_set(path: Path) -> set[int]:
    dev: set[int] = set()
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            tok = line.split()[0]
            try:
                dev.add(int(tok))
            except ValueError:
                raise ValueError(
                    f"Non-numeric id '{tok}' in {path}. "
                    "If this file contains gene symbols/FlyBase IDs, we need a mapping-based version."
                )
    return dev


def main() -> int:
    if not INPUT_DIR.exists():
        print(f"ERROR: missing input directory: {INPUT_DIR}")
        return 1
    if not DEV_GENES_FILE.exists():
        print(f"ERROR: missing developmental gene list: {DEV_GENES_FILE}")
        return 1

    dev = load_dev_gene_set(DEV_GENES_FILE)
    print(f"Loaded developmental genes: {len(dev)}")

    # table[p][s] = count as string (or "" if none)
    table: dict[int, dict[int, str]] = {p: {s: "" for s in SUPPORTS} for p in PERIODS}

    for p in PERIODS:
        for s in SUPPORTS:
            fp = INPUT_DIR / f"p{p}s{s}.txt"
            if not fp.exists():
                continue

            uniq: set[int] = set()
            bad_lines = 0

            with fp.open("r", encoding="utf-8", errors="ignore") as f:
                for raw in f:
                    parts = raw.split()
                    if not parts:
                        continue
                    if len(parts) % 2 != 0:
                        # not pairs; skip but count so user can diagnose
                        bad_lines += 1
                        continue

                    # add both endpoints if they are developmental
                    for i in range(0, len(parts), 2):
                        try:
                            u = int(parts[i])
                            v = int(parts[i + 1])
                        except ValueError:
                            bad_lines += 1
                            break

                        if u in dev:
                            uniq.add(u)
                        if v in dev:
                            uniq.add(v)

            table[p][s] = str(len(uniq)) if uniq else ""

            if bad_lines:
                print(f"WARNING: {fp.name}: skipped {bad_lines} malformed lines (odd tokens / non-ints).")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = OUT_DIR / "table1_unique_development_genes_nodepairs_p1-9_s3-9.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Periods", *SUPPORTS])
        for p in PERIODS:
            w.writerow([p, *[table[p][s] for s in SUPPORTS]])

    md_path = OUT_DIR / "table1_unique_development_genes_nodepairs_p1-9_s3-9.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# TABLE I\n")
        f.write("Number of Unique developmental genes present in the periodic subgraphs for each parameter combination.\n\n")
        f.write(f"- Input dir: `{INPUT_DIR.as_posix()}`\n")
        f.write(f"- Development genes: `{DEV_GENES_FILE.as_posix()}`\n")
        f.write("- Interpreting each p*s*.txt line as node-pairs: `u1 v1 u2 v2 ...`\n\n")

        header = ["Periods", *[str(s) for s in SUPPORTS]]
        f.write("| " + " | ".join(header) + " |\n")
        f.write("| " + " | ".join(["---"] * len(header)) + " |\n")
        for p in PERIODS:
            row = [str(p)] + [table[p][s] for s in SUPPORTS]
            f.write("| " + " | ".join(row) + " |\n")

    print(f"Wrote: {csv_path}")
    print(f"Wrote: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())