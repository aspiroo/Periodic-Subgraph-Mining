"""
Python script to compile and run C++ ListMiner for Periodic Subgraph Mining
This modifies C++ source to output directly to results/list_miner
Repository: aspiroo/Periodic-Subgraph-Mining
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time
import re

# ANSI color codes for nice output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(msg):
    print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
    print(f"{Colors.GREEN}{msg}{Colors.END}")
    print(f"{Colors.GREEN}{'='*50}{Colors.END}\n")

def print_step(msg):
    print(f"\n{Colors.YELLOW}{msg}{Colors.END}")

def print_error(msg):
    print(f"\n{Colors.RED}ERROR: {msg}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.CYAN}{msg}{Colors.END}")

# Get paths
REPO_ROOT = Path(__file__).parent.parent.parent
CPP_SOURCE_DIR = REPO_ROOT / "external_tools" / "listminer_c++"
BUILD_DIR = REPO_ROOT / "external_tools" / "listminer"
DATA_DIR = REPO_ROOT / "data" / "processed"
INPUT_FILE = DATA_DIR / "listMinerInputs.txt"
OUTPUT_DIR = REPO_ROOT / "results" / "list_miner"

def check_prerequisites():
    """Check if all required files and tools exist"""
    print_step("Step 1: Checking prerequisites...")
    
    # Check C++ source directory
    if not CPP_SOURCE_DIR.exists():
        print_error(f"C++ source directory not found: {CPP_SOURCE_DIR}")
        return False
    print_info(f"  ✓ C++ source found: {CPP_SOURCE_DIR}")
    
    # Check for main file
    main_file = CPP_SOURCE_DIR / "Miner_new.cpp"
    if not main_file.exists():
        print_error(f"Main file not found: {main_file}")
        return False
    print_info(f"  ✓ Main file found: {main_file.name}")
    
    # Check input file
    if not INPUT_FILE.exists():
        print_error(f"Input file not found: {INPUT_FILE}")
        print_info("  Please run preprocessing scripts first (scripts/01_preprocessing/)")
        return False
    print_info(f"  ✓ Input file found: {INPUT_FILE}")
    
    # Check for g++ compiler
    gpp = shutil.which("g++")
    if not gpp:
        print_error("g++ compiler not found!")
        print_info("\nInstallation options:")
        print_info("  Windows: Install MinGW-w64 or use Visual Studio")
        print_info("  Linux:   sudo apt install g++")
        print_info("  macOS:   xcode-select --install")
        return False
    print_info(f"  ✓ Compiler found: {gpp}")
    
    return True

def modify_cpp_output_paths(output_subdir):
    """
    Modify C++ source to write directly to output directory
    Returns path to modified file
    """
    print_step("Step 1.5: Modifying C++ source for custom output paths...")
    
    # Create output directory first
    output_subdir.mkdir(parents=True, exist_ok=True)
    
    # Convert Windows path to forward slashes for C++
    results_path = str(output_subdir / "results.txt").replace("\\", "/")
    stats_path = str(output_subdir / "results_stat.txt").replace("\\", "/")
    input_path = str(INPUT_FILE).replace("\\", "/")
    
    print_info(f"  Output paths:")
    print_info(f"    results.txt -> {results_path}")
    print_info(f"    results_stat.txt -> {stats_path}")
    print_info(f"    input: {input_path}")
    
    # Files to modify
    miner_cpp = CPP_SOURCE_DIR / "Miner_new.cpp"
    getstat_cpp = CPP_SOURCE_DIR / "GetStat.cpp"
    
    # Create backup directory
    backup_dir = CPP_SOURCE_DIR / ".backup"
    backup_dir.mkdir(exist_ok=True)
    
    # Backup original files
    miner_backup = backup_dir / "Miner_new.cpp.bak"
    getstat_backup = backup_dir / "GetStat.cpp.bak"
    
    if not miner_backup.exists():
        shutil.copy2(miner_cpp, miner_backup)
        print_info(f"  ✓ Backed up Miner_new.cpp")
    
    if not getstat_backup.exists():
        shutil.copy2(getstat_cpp, getstat_backup)
        print_info(f"  ✓ Backed up GetStat.cpp")
    
    # Modify Miner_new.cpp
    with open(miner_cpp, 'r') as f:
        miner_content = f.read()
    
    # Replace output file paths in printGx function
    miner_content = re.sub(
        r'myfile\.open\("results.*?\.txt"',
        f'myfile.open("{results_path}"',
        miner_content
    )
    
    # Replace input file path in Miner function
    miner_content = re.sub(
        r'myfile\.open\("listMinerInputs\.txt"',
        f'myfile.open("{input_path}"',
        miner_content
    )
    
    with open(miner_cpp, 'w') as f:
        f.write(miner_content)
    
    print_info(f"  ✓ Modified Miner_new.cpp")
    
    # Modify GetStat.cpp
    with open(getstat_cpp, 'r') as f:
        getstat_content = f.read()
    
    # Replace file paths
    getstat_content = re.sub(
        r'f1\.open\("results\.txt"',
        f'f1.open("{results_path}"',
        getstat_content
    )
    
    getstat_content = re.sub(
        r'f2\.open\("results_stat\.txt"',
        f'f2.open("{stats_path}"',
        getstat_content
    )
    
    with open(getstat_cpp, 'w') as f:
        f.write(getstat_content)
    
    print_info(f"  ✓ Modified GetStat.cpp")
    
    return miner_cpp

def restore_cpp_files():
    """Restore original C++ files from backup"""
    backup_dir = CPP_SOURCE_DIR / ".backup"
    
    if not backup_dir.exists():
        return
    
    miner_cpp = CPP_SOURCE_DIR / "Miner_new.cpp"
    getstat_cpp = CPP_SOURCE_DIR / "GetStat.cpp"
    miner_backup = backup_dir / "Miner_new.cpp.bak"
    getstat_backup = backup_dir / "GetStat.cpp.bak"
    
    if miner_backup.exists():
        shutil.copy2(miner_backup, miner_cpp)
    
    if getstat_backup.exists():
        shutil.copy2(getstat_backup, getstat_cpp)

def compile_listminer():
    """Compile the C++ ListMiner"""
    print_step("Step 2: Compiling C++ ListMiner...")
    
    # Create build directory
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    
    # ONLY compile Miner_new.cpp - it includes all other files
    main_file = CPP_SOURCE_DIR / "Miner_new.cpp"
    
    # Output executable
    if sys.platform == "win32":
        executable = BUILD_DIR / "listminer.exe"
    else:
        executable = BUILD_DIR / "listminer"
    
    print_info(f"  Compiling: {main_file.name}")
    print_info(f"  Output: {executable}")
    
    # Build compile command
    compile_cmd = [
        "g++",
        "-std=c++11",
        "-O3",
        "-o", str(executable),
        str(main_file)
    ]
    
    print_info(f"  Command: {' '.join(compile_cmd)}")
    
    try:
        result = subprocess.run(
            compile_cmd,
            cwd=str(CPP_SOURCE_DIR),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print_error("Compilation failed!")
            if result.stderr:
                print(f"\nStderr:\n{result.stderr}")
            if result.stdout:
                print(f"\nStdout:\n{result.stdout}")
            restore_cpp_files()
            return None
        
        # Show warnings if any
        if result.stderr and "warning" in result.stderr.lower():
            print_info("  ⚠ Compilation warnings (non-fatal):")
            warning_count = 0
            for line in result.stderr.split('\n'):
                if 'warning' in line.lower():
                    if warning_count < 3:  # Show first 3 warnings
                        print_info(f"    {line}")
                    warning_count += 1
            if warning_count > 3:
                print_info(f"    ... and {warning_count - 3} more warnings")
        
        if not executable.exists():
            print_error("Executable was not created!")
            restore_cpp_files()
            return None
        
        # Get file size
        size_kb = executable.stat().st_size / 1024
        print_success(f"Compilation successful! ({size_kb:.1f} KB)")
        
        return executable
        
    except subprocess.TimeoutExpired:
        print_error("Compilation timed out!")
        restore_cpp_files()
        return None
    except Exception as e:
        print_error(f"Compilation failed: {e}")
        restore_cpp_files()
        return None

def run_listminer(executable, output_subdir):
    """Run ListMiner - now writes directly to output directory"""
    print_step(f"Running ListMiner")
    
    print_info(f"  Output directory: {output_subdir}")
    print_info(f"  Parameters: support=3, period_max=10 (hardcoded in C++)")
    
    start_time = time.time()
    
    try:
        # Run directly - no need to copy, files go directly to output
        result = subprocess.run(
            [str(executable)],
            cwd=str(CPP_SOURCE_DIR),  # Run from source dir
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        duration = time.time() - start_time
        
        # Check if results files were created
        results_file = output_subdir / "results.txt"
        stats_file = output_subdir / "results_stat.txt"
        
        if not results_file.exists():
            print_error("results.txt was not created!")
            print(f"\nExit code: {result.returncode}")
            if result.stdout:
                print(f"\nStdout (last 30 lines):")
                for line in result.stdout.split('\n')[-30:]:
                    print(f"  {line}")
            if result.stderr:
                print(f"\nStderr:\n{result.stderr}")
            return False
        
        # Success!
        print_success(f"Complete in {duration:.1f}s")
        
        # Count lines in results
        with open(results_file, 'r') as f:
            line_count = sum(1 for line in f if line.strip())
        
        print_success(f"Found {line_count} periodic subgraphs")
        
        # Show sample output
        print_info("  Sample results (first 5 lines):")
        with open(results_file, 'r') as f:
            for i, line in enumerate(f):
                if i >= 5:
                    break
                print_info(f"    {line.strip()}")
        
        # Show stats if exists
        if stats_file.exists():
            print_info("\n  Statistics (first 10 lines):")
            with open(stats_file, 'r') as f:
                for i, line in enumerate(f):
                    if i >= 10:
                        remaining = line_count - 10
                        if remaining > 0:
                            print_info(f"    ... and {remaining} more")
                        break
                    print_info(f"    {line.strip()}")
        
        return True
        
    except subprocess.TimeoutExpired:
        print_error("ListMiner timed out!")
        return False
    except Exception as e:
        print_error(f"Failed to run ListMiner: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print_header("C++ ListMiner - Direct Output to results/list_miner")
    
    print_info(f"Repository root: {REPO_ROOT}")
    print_info(f"C++ source: {CPP_SOURCE_DIR}")
    print_info(f"Output: {OUTPUT_DIR}")
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Create output directory
    output_subdir = OUTPUT_DIR / "default_run"
    output_subdir.mkdir(parents=True, exist_ok=True)
    
    # Modify C++ source to output directly to results directory
    try:
        modify_cpp_output_paths(output_subdir)
    except Exception as e:
        print_error(f"Failed to modify C++ source: {e}")
        sys.exit(1)
    
    # Compile ListMiner
    executable = compile_listminer()
    if not executable:
        restore_cpp_files()
        sys.exit(1)
    
    print_step("Step 3: Running ListMiner...")
    
    total_start = time.time()
    
    # Run ListMiner
    success = run_listminer(executable, output_subdir)
    
    total_duration = time.time() - total_start
    
    # Restore original C++ files
    print_step("Step 4: Restoring original C++ files...")
    restore_cpp_files()
    print_info("  ✓ Original files restored")
    
    # Summary
    print_header("ListMiner Execution Complete!")
    
    if success:
        print_success("✓ Execution successful!")
    else:
        print_error("✗ Execution failed!")
    
    print_info(f"Total time: {total_duration:.1f}s")
    print_info(f"\nResults saved in: {output_subdir}")
    
    # List output files
    if output_subdir.exists():
        print_info("\n📂 Output files:")
        for file in sorted(output_subdir.glob("*.txt")):
            size_kb = file.stat().st_size / 1024
            line_count = sum(1 for _ in open(file)) if file.stat().st_size > 0 else 0
            print_info(f"  - {file.name} ({size_kb:.1f} KB, {line_count} lines)")
    
    print_info("\n💡 Next steps:")
    print_info(f"  1. View results: type {output_subdir / 'results.txt'}")
    print_info(f"  2. View statistics: type {output_subdir / 'results_stat.txt'}")
    print_info("  3. Continue to next pipeline stage")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())