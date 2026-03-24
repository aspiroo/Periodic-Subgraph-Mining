"""
Run Java ListMiner for Periodic Subgraph Mining.

Steps:
1. Copy fixed ListMiner.java to src directory
2. Compile all Java sources
3. Run ListMiner with correct parameters
4. Output: p{period}s{support}.txt files in results/list_miner/java_run/
"""

from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

JAVA_SRC_DIR  = REPO_ROOT / "external_tools" / "listminer_java" / "src"
JAVA_BIN_DIR  = REPO_ROOT / "external_tools" / "listminer_java" / "bin"
INPUT_FILE    = REPO_ROOT / "data" / "processed" / "listMinerInputs.txt"
OUTPUT_DIR    = REPO_ROOT / "results" / "list_miner" / "java_run"
STATS_FILE    = OUTPUT_DIR / "results_stat.txt"

# ListMiner parameters matching the paper
MIN_SUPPORT = 3
MIN_PERIOD  = 1
MAX_PERIOD  = 22   # floor(66/3) = 22 for 66 timesteps


def check_prerequisites() -> bool:
    if not INPUT_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        return False
    java = shutil.which("java")
    javac = shutil.which("javac")
    if not java:
        print("ERROR: java not found in PATH")
        return False
    if not javac:
        print("ERROR: javac not found in PATH")
        return False
    print(f"  java:  {java}")
    print(f"  javac: {javac}")
    return True


def copy_fixed_listminer() -> bool:
    """Copy the fixed ListMiner.java to the src directory."""
    fixed = Path(__file__).parent / "ListMiner.java"
    if not fixed.exists():
        # Try repo root
        fixed = REPO_ROOT / "ListMiner.java"
    if not fixed.exists():
        print("ERROR: Fixed ListMiner.java not found next to this script or at repo root.")
        print("  Place the fixed ListMiner.java next to this script.")
        return False

    dest = JAVA_SRC_DIR / "com" / "parthtejani" / "listminer" / "ListMiner.java"
    shutil.copy2(fixed, dest)
    print(f"  Copied fixed ListMiner.java -> {dest}")
    return True


def compile_java() -> bool:
    """Compile all Java source files."""
    print("\nCompiling Java sources...")
    JAVA_BIN_DIR.mkdir(parents=True, exist_ok=True)

    src_files = list((JAVA_SRC_DIR / "com" / "parthtejani" / "listminer").glob("*.java"))
    if not src_files:
        print(f"ERROR: No .java files found in {JAVA_SRC_DIR}")
        return False

    cmd = ["javac", "-d", str(JAVA_BIN_DIR)] + [str(f) for f in src_files]
    print(f"  Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: Compilation failed!")
        print(result.stderr)
        return False

    print("  Compilation successful!")
    return True


def run_listminer() -> bool:
    """Run Java ListMiner."""
    print("\nRunning Java ListMiner...")

    # Clear and recreate output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    print(f"  Output dir: {OUTPUT_DIR}")

    cmd = [
        "java",
        "-cp", str(JAVA_BIN_DIR),
        "com.parthtejani.listminer.ListMiner",
        "-i", str(INPUT_FILE),
        "-o", str(STATS_FILE),
        "-s", str(MIN_SUPPORT),
        "-Pmin", str(MIN_PERIOD),
        "-Pmax", str(MAX_PERIOD),
        "-d"
    ]

    # Capture stdout to single output file
    output_file = OUTPUT_DIR / "output.txt"
    with open(output_file, "w") as f:
        result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
    return True


def main() -> int:
    print("=" * 50)
    print("Java ListMiner Runner")
    print("=" * 50)

    if not check_prerequisites():
        return 1

    if not copy_fixed_listminer():
        return 1

    if not compile_java():
        return 1

    if not run_listminer():
        return 1

    print("\nDone! Results in:", OUTPUT_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())