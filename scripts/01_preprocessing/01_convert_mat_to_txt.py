import scipy.io as sio
import numpy as np
import os
from pathlib import Path

def convert_mat_to_edgelist(mat_file, output_file):
    """Convert MATLAB .mat file to edge list text file"""
    try:
        # Load MATLAB file
        mat_data = sio.loadmat(mat_file)
        
        # Try different possible variable names for the adjacency matrix
        adj_matrix = None
        for key in ['adj', 'adjacency', 'network', 'A', 'adjMatrix']:
            if key in mat_data:
                adj_matrix = mat_data[key]
                break
        
        # If not found, try the first non-metadata key
        if adj_matrix is None:
            keys = [k for k in mat_data.keys() if not k.startswith('__')]
            if keys:
                adj_matrix = mat_data[keys[0]]
                print(f"Using key: {keys[0]}")
        
        if adj_matrix is None:
            print(f"Error: Could not find adjacency matrix in {mat_file}")
            print(f"Available keys: {list(mat_data.keys())}")
            return False
        
        # Convert to edge list (get indices of non-zero elements)
        edges = np.argwhere(adj_matrix > 0)
        
        # Add 1 to indices (MATLAB is 1-indexed, Python is 0-indexed)
        edges = edges + 1
        
        # Save as tab-separated file
        np.savetxt(output_file, edges, fmt='%d', delimiter='\t')
        
        print(f"✅ Converted {mat_file} -> {output_file} ({len(edges)} edges)")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {mat_file}: {e}")
        return False

def main():
    # Setup paths
    input_dir = Path('../../data/raw/keller_networks')
    output_dir = Path('../../data/processed/timesteps')
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all .mat files
    mat_files = sorted(input_dir.glob('drosophila_subset_t*.mat'))
    
    print(f"Found {len(mat_files)} MATLAB files to convert")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    # Convert each file
    for mat_file in mat_files:
        # Extract timestep number (e.g., t1, t2, etc.)
        timestep_num = mat_file.stem.split('_t')[1]
        output_file = output_dir / f"timestep_{timestep_num.zfill(2)}.txt"
        
        if convert_mat_to_edgelist(mat_file, output_file):
            successful += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Conversion complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"Output directory: {output_dir.absolute()}")

if __name__ == "__main__":
    main()