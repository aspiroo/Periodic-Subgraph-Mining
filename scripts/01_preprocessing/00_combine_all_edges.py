"""Combine all edges from 66 timestep files into one master file."""
from pathlib import Path

def combine_all_edges():
    input_dir = Path('../../data/raw/keller_networks')
    output_file = Path('../../data/processed/inputs.txt')
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    timestep_files = sorted(input_dir.glob('drosophila_subset_t*.txt'))
    if not timestep_files:
        input_dir = Path('../../data/processed/timesteps')
        timestep_files = sorted(input_dir.glob('timestep_*.txt'))
    
    if not timestep_files:
        print(f"ERROR: No timestep files found in {input_dir}")
        return False
    
    total_edges = 0
    with open(output_file, 'w') as outfile:
        for ts_file in timestep_files:
            with open(ts_file, 'r') as infile:
                edges = infile.readlines()
                outfile.writelines(edges)
                total_edges += len(edges)
    
    print(f"✅ Combined {total_edges} edges from {len(timestep_files)} files → {output_file}")
    return True

if __name__ == "__main__":
    combine_all_edges()