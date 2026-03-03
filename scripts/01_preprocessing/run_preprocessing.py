"""
Stage 1: Preprocessing - Complete Pipeline
Runs all preprocessing scripts in order (01-05)
Repository: aspiroo/Periodic-Subgraph-Mining
"""

import os
import sys
import subprocess
from pathlib import Path
import time

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(msg):
    print(f"\n{Colors.GREEN}{'='*70}{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}{msg}{Colors.END}")
    print(f"{Colors.GREEN}{'='*70}{Colors.END}\n")

def print_step(msg):
    print(f"\n{Colors.YELLOW}{Colors.BOLD}{msg}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.CYAN}{msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}ERROR: {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

# Get paths
REPO_ROOT = Path(__file__).parent.parent.parent
SCRIPT_DIR = Path(__file__).parent
DATA_PROCESSED = REPO_ROOT / "data" / "processed"

def check_input_files():
    """Check if input files exist"""
    print_step("Checking input files...")
    
    keller_dir = DATA_PROCESSED / "keller_networks"
    
    if not keller_dir.exists():
        print_error(f"Keller networks directory not found: {keller_dir}")
        return False
    
    keller_files = list(keller_dir.glob("drosophila_subset_t*.txt"))
    
    if not keller_files:
        print_error("No Keller network files found!")
        return False
    
    print_info(f"  ✓ Found {len(keller_files)} Keller network files")
    print_info(f"    Location: {keller_dir}")
    
    return True

def run_script(script_name, description, step_num, total_steps, timeout=None):
    """Run a preprocessing script with optional timeout"""
    print_step(f"Step {step_num}/{total_steps}: {description}")
    
    script_path = SCRIPT_DIR / script_name
    
    if not script_path.exists():
        print_error(f"Script not found: {script_name}")
        print_info(f"  Expected: {script_path}")
        return False
    
    print_info(f"  Running: {script_name}")
    
    # Show timeout info
    if timeout:
        print_info(f"  Timeout: {timeout}s ({timeout/60:.1f} minutes)")
    else:
        print_info(f"  Timeout: None (will run until complete)")
    
    start_time = time.time()
    
    try:
        # Set UTF-8 encoding for subprocess
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(REPO_ROOT),  # Run from repo root so relative paths work
            capture_output=True,
            text=True,
            timeout=timeout,  # Use custom timeout
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        
        duration = time.time() - start_time
        
        # Show output (even if successful)
        if result.stdout:
            for line in result.stdout.split('\n'):
                if line.strip():
                    # Replace problematic characters
                    safe_line = line.replace('→', '->').replace('✓', 'OK')
                    print_info(f"    {safe_line}")
        
        # Check for errors
        if result.returncode != 0:
            print_error(f"Script exited with code {result.returncode}")
            if result.stderr:
                print_error("  Stderr output:")
                for line in result.stderr.split('\n'):
                    if line.strip():
                        safe_line = line.replace('→', '->').replace('✓', 'OK')
                        print_error(f"    {safe_line}")
            return False
        
        print_success(f"Completed in {duration:.1f}s ({duration/60:.1f} minutes)")
        return True
        
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        print_error(f"Script timed out after {duration:.1f}s!")
        print_warning("This script may need more time to complete.")
        print_info("Consider:")
        print_info("  1. Running it separately: python scripts/01_preprocessing/04_extract_timesteps.py")
        print_info("  2. Checking if output was partially created")
        return False
    except Exception as e:
        print_error(f"Failed to run script: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_output(path, description):
    """Check if an output file or directory was created"""
    if path.is_dir():
        file_count = len(list(path.glob("*.txt")))
        if file_count > 0:
            print_success(f"{description}: {file_count} files")
            return True
        else:
            print_warning(f"{description}: Directory exists but no files found")
            return False
    elif path.is_file():
        size_kb = path.stat().st_size / 1024
        try:
            line_count = sum(1 for _ in open(path, encoding='utf-8', errors='ignore')) if size_kb < 10000 else "many"
        except:
            line_count = "unknown"
        print_success(f"{description}: {size_kb:.1f} KB, {line_count} lines")
        return True
    else:
        print_error(f"{description}: Not found at {path}")
        return False

def verify_all_outputs():
    """Verify all expected outputs were created"""
    print_step("Verifying all outputs...")
    
    outputs = [
        (DATA_PROCESSED / "inputs.txt", "Combined edges"),
        (DATA_PROCESSED / "output.txt", "Deduplicated edges"),
        (DATA_PROCESSED / "outputWithEdgeNum.txt", "Edge-numbered output"),
        (DATA_PROCESSED / "timesteps_with_edge_number", "Timestep files with edge numbers"),
        (DATA_PROCESSED / "listMinerInputs.txt", "ListMiner input file"),
    ]
    
    all_verified = True
    for path, description in outputs:
        if not verify_output(path, description):
            all_verified = False
    
    return all_verified

def show_summary():
    """Show final summary of outputs"""
    print_step("Output Summary")
    
    print_info("\n📂 Generated Files:")
    
    files_to_show = [
        ("inputs.txt", "All edges combined"),
        ("output.txt", "Deduplicated edges"),
        ("outputWithEdgeNum.txt", "Edges with numbers"),
        ("listMinerInputs.txt", "ListMiner input"),
    ]
    
    for filename, desc in files_to_show:
        filepath = DATA_PROCESSED / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            print_info(f"  • {filename:<30} {size_kb:>8.1f} KB  - {desc}")
    
    # Show timestep directory
    timestep_dir = DATA_PROCESSED / "timesteps_with_edge_number"
    if timestep_dir.exists():
        count = len(list(timestep_dir.glob("*.txt")))
        print_info(f"  • timesteps_with_edge_number/  {count:>8} files - Individual timesteps")

def main():
    print_header("Stage 1: Preprocessing Pipeline - Complete Execution")
    
    print_info(f"Repository root: {REPO_ROOT}")
    print_info(f"Script directory: {SCRIPT_DIR}")
    print_info(f"Processed data:  {DATA_PROCESSED}")
    
    # Check input files
    if not check_input_files():
        print_error("\nInput files not found!")
        print_info("\nEnsure you have:")
        print_info("  data/processed/keller_networks/drosophila_subset_t1.txt -> t66.txt")
        sys.exit(1)
    
    # Define all preprocessing steps with custom timeouts
    # Script 04 is very slow (nested loops), so no timeout
    steps = [
        ("01_combine_all_edges.py", "Combine all edges from 66 timestep files", 300),
        ("02_remove_duplicates.py", "Remove duplicate edges", 300),
        ("03_assign_edge_numbers.py", "Assign edge numbers", 300),
        ("04_extract_timesteps.py", "Extract timesteps with edge numbers", None),  # No timeout - can take 30+ min
        ("05_generate_listminer_input.py", "Generate ListMiner input file", 600),
    ]
    
    print_header(f"Running {len(steps)} Preprocessing Steps")
    
    print_warning("⚠ Note: Step 4 (extract timesteps) may take 30+ minutes to complete")
    print_info("This is normal - it processes 66 files with nested comparisons\n")
    
    total_start = time.time()
    success_count = 0
    failed_step = None
    
    # Run all steps
    for i, (script_name, description, timeout) in enumerate(steps, 1):
        if run_script(script_name, description, i, len(steps), timeout):
            success_count += 1
        else:
            failed_step = (i, script_name, description)
            print_error(f"\n❌ Step {i} failed: {description}")
            break
    
    total_duration = time.time() - total_start
    
    # Verification
    print_header("Verification")
    
    verification_passed = verify_all_outputs()
    
    # Summary
    print_header("Preprocessing Complete!")
    
    if success_count == len(steps):
        print_success(f"✓ All {len(steps)} steps completed successfully!")
    else:
        print_error(f"✗ Failed at step {failed_step[0]}/{len(steps)}: {failed_step[2]}")
        print_info("\nCompleted steps:")
        for i, (script, desc, _) in enumerate(steps, 1):
            if i < failed_step[0]:
                print_success(f"  ✓ Step {i}: {desc}")
            elif i == failed_step[0]:
                print_error(f"  ✗ Step {i}: {desc}")
            else:
                print_info(f"  ○ Step {i}: {desc} (not run)")
    
    print_info(f"\nTotal execution time: {total_duration:.1f}s ({total_duration/60:.1f} minutes)")
    
    # Fixed division by zero
    if success_count > 0:
        print_info(f"Average time per step: {total_duration/success_count:.1f}s")
    else:
        print_info("No steps completed successfully")
    
    if verification_passed:
        print_success("\n✓ All outputs verified!")
    else:
        print_warning("\n⚠ Some outputs are missing or incomplete")
    
    # Show summary
    show_summary()
    
    # Next steps
    print_info("\n💡 Next Steps:")
    print_info("  1. Verify outputs in data/processed/")
    print_info("  2. Run Stage 2: Mining")
    print_info("     python scripts/02_mining/run_listminer.py")
    print_info("  3. Then Stage 3: Postprocessing")
    
    return 0 if success_count == len(steps) and verification_passed else 1

if __name__ == "__main__":
    sys.exit(main())