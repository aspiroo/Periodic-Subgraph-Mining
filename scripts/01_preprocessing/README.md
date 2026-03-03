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

## Automated Execution

### Quick Start - Run All Steps

```bash
# From repository root
python scripts/01_preprocessing/run_preprocessing.py
```

This wrapper script runs all 5 preprocessing steps in order:

**Steps executed:**
1. ✅ **Combine all edges** - Merges 66 timestep files into one
2. ✅ **Remove duplicates** - Deduplicates edge list
3. ✅ **Assign edge numbers** - Adds unique IDs to each edge
4. ✅ **Extract timesteps** - Maps edges back to timesteps (⚠️ 30+ min)
5. ✅ **Generate ListMiner input** - Creates formatted input file

**Features:**
- ✅ Colored progress output
- ✅ Timing for each step
- ✅ Automatic output verification
- ✅ Custom timeouts (no timeout for step 4)
- ✅ Error handling with diagnostics

### Wrapper Output

```
======================================================================
Stage 1: Preprocessing Pipeline - Complete Execution
======================================================================

Checking input files...
  ✓ Found 66 Keller network files

Running 5 Preprocessing Steps
======================================================================

⚠ Note: Step 4 (extract timesteps) may take 30+ minutes to complete

Step 1/5: Combine all edges from 66 timestep files
  Running: 01_combine_all_edges.py
  ✓ Completed in 2.3s

Step 2/5: Remove duplicate edges
  Running: 02_remove_duplicates.py
  ✓ Completed in 1.8s

Step 3/5: Assign edge numbers
  Running: 03_assign_edge_numbers.py
  ✓ Completed in 0.5s

Step 4/5: Extract timesteps with edge numbers
  Running: 04_extract_timesteps.py
  Timeout: None (will run until complete)
  file 1 complete
  file 2 complete
  ...
  ✓ Completed in 1847.2s (30.8 minutes)

Step 5/5: Generate ListMiner input file
  Running: 05_generate_listminer_input.py
  ✓ Completed in 3.1s

Verification
======================================================================
✓ Combined edges: 2096.3 KB, 249382 lines
✓ Deduplicated edges: 150.4 KB, 17891 lines
✓ Edge-numbered output: 245.6 KB, 17891 lines
✓ Timestep files with edge numbers: 66 files
✓ ListMiner input file: 3349.4 KB, 66 lines

✓ All 5 steps completed successfully!
Total execution time: 1854.9s (30.9 minutes)
```

## Manual Execution

If you need to run individual steps:

```bash
cd scripts/01_preprocessing

# Step 1: Combine edges
python 01_combine_all_edges.py

# Step 2: Remove duplicates
python 02_remove_duplicates.py

# Step 3: Assign edge numbers
python 03_assign_edge_numbers.py

# Step 4: Extract timesteps (slow!)
python 04_extract_timesteps.py

# Step 5: Generate ListMiner input
python 05_generate_listminer_input.py
```

## Expected Runtime

| Step | Script | Typical Time | Notes |
|------|--------|--------------|-------|
| 1 | `01_combine_all_edges.py` | ~2s | Fast I/O |
| 2 | `02_remove_duplicates.py` | ~2s | In-memory set |
| 3 | `03_assign_edge_numbers.py` | ~1s | Simple enumeration |
| 4 | `04_extract_timesteps.py` | **30-45 min** | ⚠️ Nested loops over 66 files |
| 5 | `05_generate_listminer_input.py` | ~3s | String processing |

**Total:** ~30-45 minutes (dominated by Step 4)

## Input Requirements

**Required:**
- `data/processed/keller_networks/drosophila_subset_t1.txt` through `t66.txt`

These should already exist in your repository (preprocessed network data).

## Output Files

| File | Size | Description |
|------|------|-------------|
| `data/processed/inputs.txt` | ~2 MB | All edges combined |
| `data/processed/output.txt` | ~150 KB | Unique edges only |
| `data/processed/outputWithEdgeNum.txt` | ~246 KB | Edges with unique IDs |
| `data/processed/timesteps_with_edge_number/t*.txt` | 66 files | Per-timestep edge IDs |
| `data/processed/listMinerInputs.txt` | ~3.3 MB | **Final ListMiner input** |

## Next Steps

After preprocessing completes:

```bash
# Verify output
ls -lh data/processed/listMinerInputs.txt

# Check format (should show timestep markers like *1s followed by edge numbers)
head data/processed/listMinerInputs.txt

# Proceed to mining
python scripts/02_mining/run_listminer.py
```

## Troubleshooting

### Step 4 takes too long

This is **expected**. Step 4 performs nested comparisons:
- 66 timestep files
- ~250K total edges
- Each timestep compared against all edges

**Solution:** Let it run. It's not stuck, just computationally intensive.

### UnicodeEncodeError on Windows

The wrapper handles this automatically by replacing special characters. If you see this in manual runs:

```python
# Add at top of script
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

### Files already exist

The scripts overwrite existing files. To start fresh:

```bash
# Clean outputs
rm data/processed/inputs.txt
rm data/processed/output.txt
rm data/processed/outputWithEdgeNum.txt
rm data/processed/timesteps_with_edge_number/*.txt
rm data/processed/listMinerInputs.txt

# Re-run wrapper
python scripts/01_preprocessing/run_preprocessing.py
```
