"""
Split raw Java ListMiner output into p{period}s{support}.txt files.

Input: results/list_miner/java_run/output.txt
    Format per line:
        start X psup Y p Z m W [edge1 num1 edge2 num2 ...]

Output: results/list_miner/filtering_network/p{period}s{support}.txt
    Each file contains all subgraph lines matching that period and support.

Filtering logic (matching legacy filteringPeriodSupport.py):
    - lineCells[1] = start time
    - lineCells[3] = period
    - lineCells[5] = support (psup)
    - condition: int(lineCells[1]) <= (N - (support-1) * period)
      where N = total timesteps used (66)
"""

from pathlib import Path
import shutil

REPO_ROOT  = Path(__file__).resolve().parents[2]
INPUT_FILE = REPO_ROOT / "results" / "list_miner" / "java_run" / "output.txt"
OUTPUT_DIR = REPO_ROOT / "results" / "list_miner" / "filtering_networks"

N = 30  # total timesteps

PERIOD_SUPPORT_COMBOS = [
    (1, list(range(3, 10))),
    (2, list(range(3, 10))),
    (3, list(range(3, 8))),
    (4, list(range(3, 6))),
    (5, list(range(3, 5))),
    (6, list(range(3, 6))),
    (7, list(range(3, 6))),
    (8, list(range(3, 5))),
    (9, list(range(3, 5))),
]


def main():
    if not INPUT_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        print("  Run 02_run_listminer_java.py first.")
        return 1

    # Clear and recreate output dir
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    print(f"Output dir: {OUTPUT_DIR}\n")

    # Read all lines
    lines = INPUT_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
    print(f"Total lines in output.txt: {len(lines)}")

    for period, supports in PERIOD_SUPPORT_COMBOS:
        for support in supports:
            out_file = OUTPUT_DIR / f"p{period}s{support}.txt"
            matched = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                cells = line.split(" ")
                # Need at least: start X psup Y p Z m W [...]
                if len(cells) < 8:
                    continue
                try:
                    start_time = int(cells[1])
                    line_psup  = int(cells[3])
                    line_p     = int(cells[5])
                except (ValueError, IndexError):
                    continue

                # Match period and support
                if line_p != period or line_psup != support:
                    continue

                # Apply start time filter (matching legacy logic)
                max_start = N - (support - 1) * period
                if start_time <= max_start:
                    matched.append(line)

            if matched:
                with out_file.open("w", encoding="utf-8") as f:
                    for m in matched:
                        f.write(m + "\n")
                print(f"  p{period}s{support}: {len(matched)} subgraphs -> {out_file.name}")
            else:
                print(f"  p{period}s{support}: no subgraphs found")

    print("\nDone!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())