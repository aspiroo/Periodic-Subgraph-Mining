"""
Generate p{period}s{support}.txt union genes files from filtering_network files.

Input:  results/list_miner/filtering_networks/p{period}s{support}.txt
    Format: start X psup Y p Z m W [node1 node2 node3 ...]

Output: results/list_miner/list_miner_outputs_with_edges/p{period}s{support}.txt
    Format: space-separated edge numbers > 588, deduplicated
"""

from pathlib import Path
import shutil

REPO_ROOT  = Path(__file__).resolve().parents[2]
INPUT_DIR  = REPO_ROOT / "results" / "list_miner" / "filtering_networks"
OUTPUT_DIR = REPO_ROOT / "results" / "list_miner" / "list_miner_outputs_with_edges"

DELETE_TOKENS = ["start", "psup", "p", "m", "[", "]", "\n"]

if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True)

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

for period in range(1, 10):
    for support in range(3, 10):
        in_file  = INPUT_DIR  / f"p{period}s{support}.txt"
        out_file = OUTPUT_DIR / f"p{period}s{support}.txt"

        if not in_file.exists():
            continue

        # Read and strip tokens
        text = in_file.read_text(encoding="utf-8", errors="ignore")
        for token in DELETE_TOKENS:
            text = text.replace(token, " ")

        # Split, filter for integers > 588, deduplicate
        str_list = list(filter(None, text.split()))
        convert2int = list(map(int, [t for t in str_list if t.isdigit()]))
        filt = list(filter(lambda x: x > 588, convert2int))
        convert2str = list(map(str, filt))
        result = remove_duplicates(convert2str)

        with out_file.open("w", encoding="utf-8") as f:
            for item in result:
                f.write("%s " % item)

        print(f"  p{period}s{support}: {len(result)} unique edge numbers -> {out_file.name}")

print("\nDone!")