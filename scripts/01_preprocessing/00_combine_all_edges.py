"""
Step 0: Combine all edges from 66 timestep files into one master file.
This creates the inputs.txt file needed for duplicate removal.

This script collects all edges from individual timestep files and combines
them into a single file for duplicate detection and edge numbering.
"""

from pathlib import Path
import sys

def combine_all_edges():
    """Combine all timestep edges into inputs.txt"""
    
    # Paths (try multiple locations)
    possible_input_dirs = [
        Path('../../data/processed/timesteps'),  # After conversion
        Path('../../data/raw/keller_networks'),  # Direct from MATLAB
    ]
    output_file = Path('../../data/processed/inputs.txt')
    
    print("=" * 70)
    print("STEP 0: Combining All Edges from Timestep Files")
    print("=" * 70)
    
    # Find input directory
    input_dir = None
    for dir_path in possible_input_dirs:
        if dir_path.exists():
            files = list(dir_path.glob('*.txt')) or list(dir_path.glob('*.mat'))
            if files:
                input_dir = dir_path
                break
    
    if input_dir is None:
        print("❌ ERROR: No timestep files found!")
        print("\nSearched in:")
        for d in possible_input_dirs:
            print(f"  - {d.absolute()}")
        print("\nPlease ensure you have:")
        print("  1. Run 01_convert_mat_to_txt.py first (if using .mat files)")
        print("  2. OR place timestep files in data/processed/timesteps/")
        return False
    
    print(f"✓ Found input directory: {input_dir}")
    
    # Find all timestep files
    timestep_patterns = [
        'drosophila_subset_t*.txt',
        'timestep_*.txt',
    ]
    
    timestep_files = []
    for pattern in timestep_patterns:
        files = sorted(input_dir.glob(pattern))
        if files:
            timestep_files = files
            break
    
    if not timestep_files:
        print(f"❌ ERROR: No timestep files found in {input_dir}")
        return False
    
    print(f"✓ Found {len(timestep_files)} timestep files")
    
    # Create output directory
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Combine all edges
    print("\nCombining edges...")
    total_edges = 0
    
    with open(output_file, 'w') as outfile:
        for i, ts_file in enumerate(timestep_files, 1):
            try:
                with open(ts_file, 'r') as infile:
                    edges = infile.readlines()
                    outfile.writelines(edges)
                    total_edges += len(edges)
                
                if i % 10 == 0:
                    print(f"  Processed {i}/{len(timestep_files)} files... ({total_edges} edges so far)")
            except Exception as e:
                print(f"⚠️  Warning: Could not read {ts_file.name}: {e}")
    
    print("\n" + "=" * 70)
    print(f"✅ SUCCESS!")
    print(f"   Combined: {total_edges:,} edges")
    print(f"   From: {len(timestep_files)} timestep files")
    print(f"   Output: {output_file}")
    print("=" * 70)
    print("\nNext step: Run 02_remove_duplicates.py")
    return True

if __name__ == "__main__":
    success = combine_all_edges()
    sys.exit(0 if success else 1)