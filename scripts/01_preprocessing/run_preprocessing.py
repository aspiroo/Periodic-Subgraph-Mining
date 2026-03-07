"""
Stage 1: Preprocessing - Complete Pipeline
Runs all preprocessing scripts (01-05) in order
Can execute via subprocess OR direct import
Repository: aspiroo/Periodic-Subgraph-Mining
"""

import os
import sys
import subprocess
from pathlib import Path
import time
import importlib.util

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

# Execution mode: 'import' or 'subprocess'
EXECUTION_MODE = 'import'  # Change to 'subprocess' if you prefer


def import_and_run(script_path, function_name=None):
    """Import a script and run its main function or the script itself"""
    try:
        # Load the module
        spec = importlib.util.spec_from_file_location("module", script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["module"] = module
        spec.loader.exec_module(module)
        
        # Try to run specific function or main
        if function_name and hasattr(module, function_name):
            return getattr(module, function_name)()
        elif hasattr(module, 'main'):
            return module.main()
        else:
            # Script already executed on import
            return True
            
    except Exception as e:
        print_error(f"Failed to import/run: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_via_subprocess(script_path, timeout=None):
    """Run script via subprocess (original method)"""
    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        
        # Show output
        if result.stdout:
            for line in result.stdout.split('\n'):
                if line.strip():
                    safe_line = line.replace('→', '->').replace('✓', 'OK')
                    print_info(f"    {safe_line}")
        
        if result.returncode != 0:
            print_error(f"Script exited with code {result.returncode}")
            if result.stderr:
                for line in result.stderr.split('\n'):
                    if line.strip():
                        print_error(f"    {line}")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print_error("Script timed out!")
        return False
    except Exception as e:
        print_error(f"Failed to run: {e}")
        return False


def run_script(script_name, description, step_num, total_steps, timeout=None, function_name=None):
    """Run a preprocessing script using configured method"""
    print_step(f"Step {step_num}/{total_steps}: {description}")
    
    script_path = SCRIPT_DIR / script_name
    
    if not script_path.exists():
        print_error(f"Script not found: {script_name}")
        return False
    
    print_info(f"  Running: {script_name}")
    print_info(f"  Mode: {EXECUTION_MODE}")
    
    if timeout and EXECUTION_MODE == 'subprocess':
        print_info(f"  Timeout: {timeout}s ({timeout/60:.1f} minutes)")
    elif not timeout and EXECUTION_MODE == 'subprocess':
        print_info(f"  Timeout: None (will run until complete)")
    
    start_time = time.time()
    
    # Choose execution method
    if EXECUTION_MODE == 'import':
        success = import_and_run(script_path, function_name)
    else:
        success = run_via_subprocess(script_path, timeout)
    
    duration = time.time() - start_time
    
    if success:
        print_success(f"Completed in {duration:.1f}s ({duration/60:.1f} minutes)")
        return True
    else:
        return False


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
    print_info(f"Execution mode:  {EXECUTION_MODE}")
    
    # Check input files
    if not check_input_files():
        print_error("\nInput files not found!")
        sys.exit(1)
    
    # Define steps: (script, description, timeout, function_name)
    steps = [
        ("01_combine_all_edges.py", "Combine all edges from 66 timestep files", 300, "combine_all_edges"),
        ("02_remove_duplicates.py", "Remove duplicate edges", 300, None),
        ("03_assign_edge_numbers.py", "Assign edge numbers", 300, None),
        ("04_extract_timesteps.py", "Extract timesteps with edge numbers", None, None),
        ("05_generate_listminer_input.py", "Generate ListMiner input file", 600, None),
    ]
    
    print_header(f"Running {len(steps)} Preprocessing Steps")
    print_warning("⚠ Note: Step 4 may take 30+ minutes\n")
    
    total_start = time.time()
    success_count = 0
    failed_step = None
    
    # Run all steps
    for i, (script, desc, timeout, func) in enumerate(steps, 1):
        if run_script(script, desc, i, len(steps), timeout, func):
            success_count += 1
        else:
            failed_step = (i, script, desc)
            print_error(f"\n❌ Step {i} failed: {desc}")
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
        print_error(f"✗ Failed at step {failed_step[0]}/{len(steps)}")
    
    print_info(f"\nTotal time: {total_duration:.1f}s ({total_duration/60:.1f} min)")
    
    if success_count > 0:
        print_info(f"Average per step: {total_duration/success_count:.1f}s")
    
    if verification_passed:
        print_success("\n✓ All outputs verified!")
    
    show_summary()
    
    print_info("\n💡 Next: python scripts/02_mining/run_listminer.py")
    
    return 0 if success_count == len(steps) and verification_passed else 1


if __name__ == "__main__":
    sys.exit(main())