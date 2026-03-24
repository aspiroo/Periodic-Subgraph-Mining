"""
Generate p{period}s{support}.txt union genes files from filtering_network files.

Input:  results/list_miner/filtering_network/p{period}s{support}.txt
    Format: start X psup Y p Z m W [edge1 num1 edge2 num2 ...]

Output: results/list_miner/list_miner_outputs_with_edges/p{period}s{support}.txt
    Format: space-separated edge numbers > 588, deduplicated

Matches legacy unionGenes.py logic:
    1. Strip tokens: start, psup, p, m, [, ]
    2. Split on space
    3. Filter for integers > 588 (these are edge numbers)
    4. Remove duplicates preserving order
"""

from pathlib import Path
import shutil

REPO_ROOT  = Path(__file__).resolve().parents[2]
INPUT_DIR  = REPO_ROOT / "results" / "list_miner" / "filtering_networks"
OUTPUT_DIR = REPO_ROOT / "results" / "list_miner" / "list_miner_outputs_with_edges"

DELETE_TOKENS = ["start", "psup", "p", "m", "[", "]", "\n"]

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


def remove_duplicates(values):
    seen = set()
    output = []
    for v in values:
        if v not in seen:
            output.append(v)
            seen.add(v)
    return output


def main():
    if not INPUT_DIR.exists():
        print(f"ERROR: filtering_network dir not found: {INPUT_DIR}")
        print("  Run 02_filter_listminer_output.py first.")
        return 1

    # Clear and recreate output dir
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    print(f"Output dir: {OUTPUT_DIR}\n")

    for period, supports in PERIOD_SUPPORT_COMBOS:
        for support in supports:
            in_file  = INPUT_DIR  / f"p{period}s{support}.txt"
            out_file = OUTPUT_DIR / f"p{period}s{support}.txt"

            if not in_file.exists():
                print(f"  SKIP (missing): p{period}s{support}.txt")
                continue

            # Read and strip tokens (matching legacy unionGenes.py exactly)
            text = in_file.read_text(encoding="utf-8", errors="ignore")
            for token in DELETE_TOKENS:
                text = text.replace(token, " ")

            # Split, filter for integers > 588, deduplicate
            str_list = list(filter(None, text.split()))
            try:
                convert2int = list(map(int, str_list))
            except ValueError:
                # Skip non-integer tokens
                convert2int = []
                for t in str_list:
                    try:
                        convert2int.append(int(t))
                    except ValueError:
                        pass

            filtered = list(filter(lambda x: x > 588, convert2int))
            convert2str = list(map(str, filtered))
            result = remove_duplicates(convert2str)

            with out_file.open("w", encoding="utf-8") as f:
                f.write(" ".join(result))

            print(f"  p{period}s{support}: {len(result)} unique edge numbers -> {out_file.name}")

    print("\nDone!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())