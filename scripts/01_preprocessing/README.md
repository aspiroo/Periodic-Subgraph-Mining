# Stage 1: Data Preprocessing

Scripts for converting and preparing network data for subgraph mining.

## Overview

This stage converts raw network data into the format required by ListMiner:
- Converts MATLAB networks to text format (if applicable)
- Splits temporal networks into individual timestep files
- Validates edge list format
- Prepares gene ID mappings

## Scripts

### Main Scripts

- **02_remove_duplicates.py** - Remove duplicate edges from the input network
- **03_assign_edge_numbers.py** - Assign sequential numbers to edges
- **04_extract_timesteps.py** - Extract individual timestep files from the Keller dataset
- **05_generate_listminer_input.py** - Format data into ListMiner input format
- **run_all.sh** - Run all preprocessing steps in order

### MATLAB Scripts

Located in `matlab/network_generation/` directory:
- **keller.m** - Process Keller lab networks
- **drosophila_subset_collector.m** - Extract network subsets

## Usage

### Basic Preprocessing

```bash
cd scripts/01_preprocessing

# Run all preprocessing steps
bash run_all.sh

# Or run individual steps:
python 02_remove_duplicates.py
python 03_assign_edge_numbers.py
python 04_extract_timesteps.py
python 05_generate_listminer_input.py
```

### Process Keller Networks

If using Keller lab MATLAB data:

```bash
# Use MATLAB scripts in matlab/network_generation/
cd matlab/network_generation
matlab -nodisplay -r "keller; exit"
```

### Run All Preprocessing

```bash
bash run_all.sh
```

## Input Requirements

- Raw network files in `data/raw/`
- Gene mappings in `data/mappings/`

See [data/raw/README.md](../../data/raw/README.md) for format details.

## Output

**Location**: `data/processed/timesteps/`

**Format**: Individual text files for each time point
```
timestep_01.txt
timestep_02.txt
...
timestep_N.txt
```

Each file contains edge list:
```
node1  node2
1      2
1      5
```

## Validation

After preprocessing, verify:

```bash
# Check output files
ls -lh ../../data/processed/timesteps/

# Verify format
head ../../data/processed/timesteps/timestep_01.txt

# Count edges per timestep
wc -l ../../data/processed/timesteps/*.txt
```

## Parameters

Common parameters for preprocessing scripts:

- `--input`: Input directory with raw data
- `--output`: Output directory for processed files
- `--format`: Input format (matlab, text, csv)
- `--delimiter`: Field delimiter (default: tab)
- `--validate`: Validate output format

## Troubleshooting

### Issue: MATLAB not found

Use Python conversion scripts as alternative or install MATLAB.

### Issue: Invalid edge format

Check delimiter and ensure two columns per line.

### Issue: Missing gene IDs

Verify mapping files exist in `data/mappings/`.

For more issues, see [docs/TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md).

## Next Stage

After preprocessing completes:
- Proceed to **Stage 2: Subgraph Mining** in `scripts/02_mining/`
- See [PIPELINE.md](../../PIPELINE.md) for next steps
