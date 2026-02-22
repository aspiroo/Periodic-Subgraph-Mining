# MATLAB Code

MATLAB scripts for network preprocessing and analysis.

## Overview

This directory contains MATLAB code for:
- Processing Keller lab network data
- Converting MATLAB formats to text
- Network preprocessing
- (Optional) Alternative to Python preprocessing

## Scripts

### Keller Network Processing

Located in `matlab/network_generation/`:
- **keller.m** - Main Keller network processor
- **drosophila_subset.m** - Extract network subsets
- **drosophila_subset_collector.m** - Collect subset data
- **drosophila_master_subset.m** - Master subset processing
- **keller_example.m** - Example usage

### Optimization Utilities

Located in `matlab/min_func/`:
- **minFunc.m** - Main optimization function
- Supporting functions for L-BFGS optimization

## Usage

### Process Keller Networks

```matlab
% In MATLAB
cd matlab/network_generation/

% Run main processor
keller

% Or run from command line
matlab -nodisplay -r "cd matlab/network_generation; keller; exit"
```

### Custom Processing

```matlab
% Load network data
load('../../data/raw/keller_data/drosophila.mat')

% Process timesteps
for t = 1:num_timesteps
    network = extract_timestep(data, t);
    save_edgelist(network, sprintf('timestep_%02d.txt', t));
end
```

## Requirements

- **MATLAB** R2016b or later (recommended)
- Bioinformatics Toolbox (if using advanced features)
- Statistics Toolbox (optional)

## Input

MATLAB `.mat` files containing:
- Network adjacency matrices
- Timestep information
- Gene ID mappings
- Metadata

Place in: `data/raw/keller_data/`

## Output

Text files suitable for ListMiner:
- Edge lists (tab-separated)
- One file per timestep
- Node ID format

Output to: `data/processed/timesteps/`

## Functions

### Network Processing

```matlab
% Extract network at timestep
network = extract_network(data, timestep);

% Convert to edge list
edgelist = adjacency_to_edgelist(adj_matrix);

% Save to file
save_edgelist(edgelist, filename);
```

### Data Conversion

```matlab
% MATLAB matrix to text edge list
function save_edgelist(adj_matrix, filename)
    [i, j] = find(adj_matrix);
    edges = [i, j];
    dlmwrite(filename, edges, 'delimiter', '\t');
end
```

## Alternative: Python

If MATLAB is not available, use Python alternatives:
- `scipy.io.loadmat()` to read .mat files
- Convert using Python scripts in `scripts/01_preprocessing/`

Example Python conversion:
```python
from scipy.io import loadmat
import numpy as np

# Load MATLAB file
data = loadmat('network_data.mat')
adj_matrix = data['adjacency']

# Convert to edge list
edges = np.argwhere(adj_matrix > 0)
np.savetxt('edgelist.txt', edges, fmt='%d', delimiter='\t')
```

## Migration from Original

The original MATLAB scripts were in `legacy/Keller codes/` directory and have been copied to `matlab/network_generation/`.

To use them:
```bash
# Option 1: Use new organized location (recommended)
cd matlab/network_generation/
matlab -nodisplay -r "keller; exit"

# Option 2: Use legacy location
cd "legacy/Keller codes"
matlab -nodisplay -r "keller; exit"
```

## Tips

1. **Large Files**: Process in batches if memory constrained
2. **Parallel Processing**: Use parfor for multiple timesteps
3. **Validation**: Always check output format before mining
4. **Documentation**: Add comments to custom scripts

## Troubleshooting

### MATLAB not installed

Use Python alternatives or install MATLAB.

### Out of memory

```matlab
% Process in chunks
for chunk = 1:num_chunks
    process_chunk(data, chunk);
    clear chunk_data;  % Free memory
end
```

### File format issues

Ensure output is tab-separated integers:
```matlab
% Correct format
dlmwrite(filename, edges, 'delimiter', '\t', 'precision', '%d');
```

### Path issues

```matlab
% Add required paths
addpath('../data/raw/');
addpath('../data/processed/');
```

## Documentation

- **MATLAB Docs**: https://www.mathworks.com/help/matlab/
- **Pipeline Guide**: [PIPELINE.md](../PIPELINE.md)
- **Preprocessing Stage**: [scripts/01_preprocessing/README.md](../scripts/01_preprocessing/README.md)

## Advanced Usage

### Batch Processing

```matlab
% Process all .mat files in directory
files = dir('../../data/raw/keller_data/*.mat');
for i = 1:length(files)
    process_network(files(i).name);
end
```

### Parallel Processing

```matlab
% Use parallel pool
parpool(4);  % 4 workers
parfor t = 1:num_timesteps
    process_timestep(t);
end
delete(gcp);  % Close pool
```

## Optional Usage

MATLAB is **optional** for this pipeline:
- Required only if using Keller .mat files
- Python alternatives available for most tasks
- Use if you're comfortable with MATLAB

## Next Steps

After MATLAB preprocessing:
1. Verify output in `data/processed/timesteps/`
2. Proceed to Stage 2: Mining
3. Follow [PIPELINE.md](../PIPELINE.md)
