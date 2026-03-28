"""
Split raw Java ListMiner output into p{period}s{support}.txt files.

Input: results/list_miner/java_run/output.txt
    Format per line:
        start X psup Y p Z m W [edge1 num1 edge2 num2 ...]

Output: results/list_miner/filtering_networks/p{period}s{support}.txt
    Each file contains all subgraph lines matching that period and support.

Filtering logic (matching legacy filteringPeriodSupport.py):
    - lineCells[1] = start time
    - lineCells[3] = support (psup)
    - lineCells[5] = period (p)
    - condition: int(lineCells[1]) <= (N - (support-1) * period)
      where N = total timesteps used (30)
"""

from pathlib import Path
import shutil

REPO_ROOT  = Path(__file__).resolve().parents[2]
INPUT_FILE = REPO_ROOT / "results" / "list_miner" / "java_run" / "output.txt"
OUTPUT_DIR = REPO_ROOT / "results" / "list_miner" / "filtering_networks"

N = 30  # total timesteps

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
    fo = INPUT_FILE.read_text(encoding="utf-8", errors="ignore").strip()
    lines = fo.split("\n")
    print(f"Total lines in output.txt: {len(lines)}")

    for period in range(1, 10):
        for support in range(3, 10):
            out_file = OUTPUT_DIR / f"p{period}s{support}.txt"
            matched = []

            for splitLine in lines:
                lineCells = splitLine.split(" ")
                if len(lineCells) < 8:
                    continue
                try:
                    start_time = int(lineCells[1])
                    line_psup  = int(lineCells[3])
                    line_p     = int(lineCells[5])
                except (ValueError, IndexError):
                    continue

                # Match period and support, apply start time filter
                if line_p == period and line_psup == support:
                    if start_time <= (N - (support - 1) * period):
                        matched.append(splitLine)

            if matched:
                with out_file.open("w", encoding="utf-8") as f:
                    for m in matched:
                        f.write(m + "\n")
                print(f"  p{period}s{support}: {len(matched)} subgraphs -> {out_file.name}")

    print("\nDone!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())