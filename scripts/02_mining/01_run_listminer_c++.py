"""
Python script to compile and run C++ ListMiner for Periodic Subgraph Mining

This runner is intentionally robust:
- It does NOT patch/restore C++ source code.
- It runs the miner from external_tools/listminer_c++ (so relative paths work).
- It copies the preprocessed input file into external_tools/listminer_c++/listMinerInputs.txt.
- It deletes previous outputs before running (miner appends by default).
- It treats exit code 0 or 1 as success (Miner_new.cpp main() returns 1 in this repo).
- It prefers outputs in results/list_miner/default_run (when C++ uses absolute output paths),
  otherwise it falls back to searching for results*.txt under external_tools/listminer_c++.

Repository: aspiroo/Periodic-Subgraph-Mining
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path


# ANSI color codes for nice output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    END = "\033[0m"


def print_header(msg: str) -> None:
    print(f"\n{Colors.GREEN}{'=' * 50}{Colors.END}")
    print(f"{Colors.GREEN}{msg}{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 50}{Colors.END}\n")


def print_step(msg: str) -> None:
    print(f"\n{Colors.YELLOW}{msg}{Colors.END}")


def print_error(msg: str) -> None:
    print(f"\n{Colors.RED}ERROR: {msg}{Colors.END}")


def print_success(msg: str) -> None:
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def print_info(msg: str) -> None:
    print(f"{Colors.CYAN}{msg}{Colors.END}")


# Paths
REPO_ROOT = Path(__file__).resolve().parents[2]
CPP_SOURCE_DIR = REPO_ROOT / "external_tools" / "listminer_c++"
BUILD_DIR = REPO_ROOT / "external_tools" / "listminer"
DATA_DIR = REPO_ROOT / "data" / "processed"
INPUT_FILE = DATA_DIR / "listMinerInputs.txt"
OUTPUT_DIR = REPO_ROOT / "results" / "list_miner"


def check_prerequisites() -> bool:
    print_step("Step 1: Checking prerequisites...")

    if not CPP_SOURCE_DIR.exists():
        print_error(f"C++ source directory not found: {CPP_SOURCE_DIR}")
        return False
    print_info(f"  ✓ C++ source found: {CPP_SOURCE_DIR}")

    main_file = CPP_SOURCE_DIR / "Miner_new.cpp"
    if not main_file.exists():
        print_error(f"Main file not found: {main_file}")
        return False
    print_info(f"  ✓ Main file found: {main_file.name}")

    if not INPUT_FILE.exists():
        print_error(f"Input file not found: {INPUT_FILE}")
        print_info("  Please run preprocessing scripts first (scripts/01_preprocessing/)")
        return False
    print_info(f"  ✓ Input file found: {INPUT_FILE}")

    gpp = shutil.which("g++")
    if not gpp:
        print_error("g++ compiler not found!")
        print_info("\nInstallation options:")
        print_info("  Windows: Install MinGW-w64/MSYS2")
        print_info("  Linux:   sudo apt install g++")
        print_info("  macOS:   xcode-select --install")
        return False
    print_info(f"  ✓ Compiler found: {gpp}")

    return True


def prepare_io(output_subdir: Path) -> None:
    """
    Prepare input/output WITHOUT modifying C++ sources.

    - Copy INPUT_FILE -> external_tools/listminer_c++/listMinerInputs.txt
      because Miner_new.cpp opens "listMinerInputs.txt" relative to cwd.
    - Delete old result files (miner appends by default).
    """
    print_step("Step 1.5: Preparing input/output (no C++ path rewriting)...")

    output_subdir.mkdir(parents=True, exist_ok=True)

    cpp_input = CPP_SOURCE_DIR / "listMinerInputs.txt"
    shutil.copy2(INPUT_FILE, cpp_input)
    print_info(f"  ✓ Copied input to: {cpp_input} ({cpp_input.stat().st_size} bytes)")

    # Delete old outputs in output dir (if C++ writes via absolute paths)
    for p in [output_subdir / "results.txt", output_subdir / "results_stat.txt"]:
        if p.exists():
            p.unlink()
            print_info(f"  ✓ Deleted old: {p}")

    # Delete old outputs in C++ dir (if C++ writes relative to cwd)
    for p in [
        CPP_SOURCE_DIR / "results.txt",
        CPP_SOURCE_DIR / "results_large.txt",
        CPP_SOURCE_DIR / "results_stat.txt",
    ]:
        if p.exists():
            p.unlink()
            print_info(f"  ✓ Deleted old: {p.name}")

    # Also delete any results*.txt under CPP_SOURCE_DIR/results/ if present
    results_dir = CPP_SOURCE_DIR / "results"
    if results_dir.exists() and results_dir.is_dir():
        for p in results_dir.glob("results*.txt"):
            try:
                p.unlink()
                print_info(f"  ✓ Deleted old: results/{p.name}")
            except OSError:
                pass


def compile_listminer() -> Path | None:
    print_step("Step 2: Compiling C++ ListMiner...")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    main_file = CPP_SOURCE_DIR / "Miner_new.cpp"

    executable = BUILD_DIR / ("listminer.exe" if sys.platform == "win32" else "listminer")

    compile_cmd = ["g++", "-std=c++11", "-O3", "-o", str(executable), str(main_file)]
    print_info(f"  Command: {' '.join(compile_cmd)}")

    try:
        result = subprocess.run(
            compile_cmd,
            cwd=str(CPP_SOURCE_DIR),
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            print_error("Compilation failed!")
            if result.stderr:
                print(f"\nStderr:\n{result.stderr}")
            if result.stdout:
                print(f"\nStdout:\n{result.stdout}")
            return None

        if result.stderr and "warning" in result.stderr.lower():
            print_info("  ⚠ Compilation warnings (non-fatal):")
            for line in result.stderr.split("\n"):
                if "warning" in line.lower():
                    print_info(f"    {line}")

        if not executable.exists():
            print_error("Executable was not created!")
            return None

        size_kb = executable.stat().st_size / 1024
        print_success(f"Compilation successful! ({size_kb:.1f} KB)")
        return executable

    except subprocess.TimeoutExpired:
        print_error("Compilation timed out!")
        return None
    except Exception as e:
        print_error(f"Compilation failed: {e}")
        return None


def _newest_nonempty(paths: list[Path]) -> Path | None:
    candidates: list[Path] = []
    for p in paths:
        if p.exists() and p.is_file() and p.stat().st_size > 0:
            candidates.append(p)
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def locate_results_file(output_subdir: Path) -> tuple[Path | None, Path | None]:
    """
    Prefer outputs in output_subdir (when C++ uses absolute output paths),
    else fallback to searching under CPP_SOURCE_DIR.
    """
    # 1) Preferred: output_subdir (your current C++ writes here)
    out_results = output_subdir / "results.txt"
    out_stats = output_subdir / "results_stat.txt"

    results_txt = out_results if out_results.exists() and out_results.stat().st_size > 0 else None
    stats_txt = out_stats if out_stats.exists() and out_stats.stat().st_size > 0 else None

    if results_txt:
        return results_txt, stats_txt

    # 2) Fallback: common places/names under CPP_SOURCE_DIR
    direct = [
        CPP_SOURCE_DIR / "results.txt",
        CPP_SOURCE_DIR / "results_large.txt",
        CPP_SOURCE_DIR / "results_stat.txt",
    ]
    recursive = list(CPP_SOURCE_DIR.rglob("results*.txt"))

    results_txt = _newest_nonempty([p for p in (direct + recursive) if p.name != "results_stat.txt"])
    stats_txt = _newest_nonempty([p for p in (direct + recursive) if p.name == "results_stat.txt"])
    return results_txt, stats_txt


def run_listminer(executable: Path, output_subdir: Path) -> bool:
    print_step("Step 3: Running ListMiner...")
    print_info(f"  CWD: {CPP_SOURCE_DIR}")
    print_info(f"  Output directory: {output_subdir}")
    print_info("  Note: exit code 1 is OK for this miner (main() returns 1 in repo)")

    start_time = time.time()
    try:
        proc = subprocess.run([str(executable)], cwd=str(CPP_SOURCE_DIR), timeout=1800)
        duration = time.time() - start_time

        if proc.returncode not in (0, 1):
            print_error(f"Miner exited with code {proc.returncode}")
            return False

        results_txt, stats_txt = locate_results_file(output_subdir)

        if not results_txt:
            print_error("No non-empty results*.txt produced (neither in output dir nor under external_tools/listminer_c++)")
            print_info("  Files in output directory:")
            if output_subdir.exists():
                for p in sorted(output_subdir.glob("*")):
                    if p.is_file():
                        print_info(f"    - {p.name} ({p.stat().st_size} bytes)")
            print_info("  Files in external_tools/listminer_c++:")
            for p in sorted(CPP_SOURCE_DIR.glob("*")):
                if p.is_file():
                    print_info(f"    - {p.name} ({p.stat().st_size} bytes)")
            return False

        # Ensure we end up with output_subdir/results.txt and output_subdir/results_stat.txt
        dst_results = output_subdir / "results.txt"
        if results_txt.resolve() != dst_results.resolve():
            shutil.copy2(results_txt, dst_results)

        if stats_txt:
            dst_stats = output_subdir / "results_stat.txt"
            if stats_txt.resolve() != dst_stats.resolve():
                shutil.copy2(stats_txt, dst_stats)

        with open(dst_results, "r", encoding="utf-8", errors="replace") as f:
            line_count = sum(1 for line in f if line.strip())

        print_success(f"Complete in {duration:.1f}s")
        print_success(f"Wrote {line_count} non-empty lines to {dst_results}")
        if (output_subdir / "results_stat.txt").exists():
            print_info(f"  Also wrote stats: {output_subdir / 'results_stat.txt'}")

        return True

    except subprocess.TimeoutExpired:
        print_error("ListMiner timed out!")
        return False
    except Exception as e:
        print_error(f"Failed to run ListMiner: {e}")
        return False


def main() -> int:
    print_header("C++ ListMiner - Output to results/list_miner")

    print_info(f"Repository root: {REPO_ROOT}")
    print_info(f"C++ source: {CPP_SOURCE_DIR}")
    print_info(f"Output: {OUTPUT_DIR}")

    if not check_prerequisites():
        return 1

    output_subdir = OUTPUT_DIR / "default_run"
    prepare_io(output_subdir)

    executable = compile_listminer()
    if not executable:
        return 1

    success = run_listminer(executable, output_subdir)

    print_header("ListMiner Execution Complete!")
    if success:
        print_success("✓ Execution successful!")
    else:
        print_error("✗ Execution failed!")

    print_info(f"Results saved in: {output_subdir}")

    if output_subdir.exists():
        print_info("\n📂 Output files:")
        for file in sorted(output_subdir.glob("*.txt")):
            size_kb = file.stat().st_size / 1024
            line_count = (
                sum(1 for _ in open(file, encoding="utf-8", errors="replace"))
                if file.stat().st_size > 0
                else 0
            )
            print_info(f"  - {file.name} ({size_kb:.1f} KB, {line_count} lines)")

    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())