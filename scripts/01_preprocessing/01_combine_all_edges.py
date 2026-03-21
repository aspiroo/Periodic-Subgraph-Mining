"""Combine all edges from 66 timestep files into one master file."""
from pathlib import Path
import os
import re

def combine_all_edges():
    # Get the script's directory
    script_dir = Path(__file__).parent.absolute()
    # Go up to repo root
    repo_root = script_dir.parent.parent
    
    input_dir = repo_root / 'data' / 'processed' / 'keller_networks'
    output_file = repo_root / 'data' / 'processed' / 'inputs.txt'
    
    print(f"Script location: {script_dir}")
    print(f"Repo root: {repo_root}")
    print(f"Looking for files in: {input_dir}")
    print(f"Directory exists: {input_dir.exists()}")
    
    output_file.parent.mkdir(parents=True, exist_ok=True)

    timestep_files = sorted(
        input_dir.glob('drosophila_subset_t*.txt'),
        key=lambda f: int(re.search(r't(\d+)', f.name).group(1))
    )

    print(f"Found {len(timestep_files)} files")
    
    if not timestep_files:
        print(f"ERROR: No files found!")
        return False
    
    total_edges = 0
    with open(output_file, 'w') as outfile:
        for ts_file in timestep_files:
            with open(ts_file, 'r') as infile:
                edges = infile.readlines()
                outfile.writelines(edges)
                total_edges += len(edges)
    
    print(f"Combined {total_edges} edges from {len(timestep_files)} files → {output_file}")
    return True

if __name__ == "__main__":
    combine_all_edges()