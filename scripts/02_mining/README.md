# Stage 2: Subgraph Mining

Scripts and tools for mining frequent subgraphs using ListMiner.

## Overview

This stage uses ListMiner to discover frequent subgraphs that appear across multiple time points:
- Runs ListMiner with various parameter combinations
- Discovers periodic patterns in temporal networks
- Generates candidate subgraphs for further analysis

## Tools

### ListMiner

Location: `external_tools/listminer/`

ListMiner is a frequent subgraph mining tool designed for temporal networks.

**Installation**: See [external_tools/listminer/README.md](../../external_tools/listminer/README.md)

## Scripts

- **run_listminer.sh** - Automated ListMiner execution with multiple parameters
- **prepare_input.py** - Format input for ListMiner
- **validate_output.py** - Validate mining results

## Usage

### Single Run

```bash
cd external_tools/listminer

./listminer \
    -i ../../data/processed/timesteps/ \
    -o ../../results/listminer_output/support_3_size_4/ \
    -s 3 \
    -min 3 \
    -max 4
```

### Multiple Parameter Combinations

```bash
cd scripts/02_mining

# Run with default parameters
bash run_listminer.sh

# Run with custom parameters
bash run_listminer.sh --support 5 --min-size 3 --max-size 6
```

### Parameters

- `-i`: Input directory with timestep files
- `-o`: Output directory for results
- `-s`: **Support threshold** - minimum number of timesteps where pattern must appear
- `-min`: Minimum subgraph size (number of nodes)
- `-max`: Maximum subgraph size (number of nodes)

## Parameter Selection Guide

### Support Threshold (`-s`)

- **Low (2-3)**: Many patterns, less stringent
- **Medium (4-6)**: Balanced
- **High (7-10)**: Few patterns, very frequent only

**Recommendation**: Start with s=3 for initial exploration.

### Subgraph Size

- **Small (3-4 nodes)**: Fast, many patterns, basic motifs
- **Medium (5-6 nodes)**: Balanced, biological modules
- **Large (7-10 nodes)**: Slow, fewer patterns, complex modules

**Recommendation**: Start with min=3, max=4, then expand.

## Output

**Location**: `results/listminer_output/`

**Structure**:
```
results/listminer_output/
├── support_3_size_4/
│   ├── frequent_subgraphs.txt
│   ├── subgraph_list.txt
│   └── statistics.txt
├── support_5_size_6/
│   └── ...
```

**Format**: Each file contains discovered subgraphs with:
- Subgraph ID
- Node list
- Edge list
- Support (frequency)

## Validation

After mining:

```bash
# Check output
ls -lh ../../results/listminer_output/

# Count discovered subgraphs
wc -l ../../results/listminer_output/*/frequent_subgraphs.txt

# View sample subgraph
head ../../results/listminer_output/support_3_size_4/frequent_subgraphs.txt
```

## Performance

**Runtime**: Varies based on:
- Network size (nodes/edges)
- Number of timesteps
- Support threshold (lower = slower)
- Subgraph size (larger = slower)

**Typical**: 10 minutes to 2 hours per parameter combination.

**Memory**: May require 4-8GB RAM for large networks.

## Tips

1. **Start small**: Test with high support and small size first
2. **Parallelize**: Run multiple parameter combinations in parallel
3. **Monitor**: Watch memory usage during execution
4. **Checkpoint**: Keep intermediate results

## Common Parameter Combinations

```bash
# Quick exploration
./listminer -i input/ -o output/quick/ -s 5 -min 3 -max 4

# Comprehensive (slow)
./listminer -i input/ -o output/comprehensive/ -s 2 -min 3 -max 8

# Balanced (recommended)
./listminer -i input/ -o output/balanced/ -s 3 -min 3 -max 6
```

## Troubleshooting

### Issue: ListMiner not found

```bash
cd external_tools/listminer
chmod +x listminer
./listminer --help
```

### Issue: Out of memory

- Increase support threshold
- Reduce maximum subgraph size
- Process fewer timesteps
- Add more RAM

### Issue: No patterns found

- Reduce support threshold
- Check input format
- Verify timestep files are not empty

For more help, see [docs/TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md).

## Next Stage

After mining completes:
- Proceed to **Stage 3: Post-processing** in `scripts/03_postprocessing/`
- See [PIPELINE.md](../../PIPELINE.md) for next steps

## Automated Mining Wrapper

### Quick Start

```bash
# From repository root
python scripts/02_mining/run_listminer.py
```

This automatically:
1. Compiles ListMiner C++ code (if needed)
2. Runs mining with default parameters
3. Generates both regular and edge-annotated outputs
4. Creates statistics files

### Wrapper Features

✅ Automatic compilation check
✅ Configurable parameters
✅ Multiple (period, support) combinations
✅ Progress tracking
✅ Output verification
✅ Statistics generation

### Default Parameters

```python
# In run_listminer.py
periods = [2, 3, 4, 5, 6, 7, 8, 9]
supports = list(range(3, 19))  # 3 through 18
```

This generates files like:
- `p2s3.txt` (period=2, support=3)
- `p2s4.txt` (period=2, support=4)
- ...
- `p9s18.txt` (period=9, support=18)

### Output Structure

```
results/list_miner/
├── default_run/
│   ├── results.txt              # Main results
│   └── results_stat.txt         # Statistics
│
└── list_miner_outputs_with_edges/
    ├── p2s3.txt                 # Period=2, Support=3
    ├── p2s4.txt
    ├── p2s5.txt
    ...
    └── p9s18.txt                # All combinations
```

### Current Status

✅ **Completed:**
- ListMiner C++ implementation compiled
- Wrapper script functional
- Multiple parameter support
- Output validation

🚧 **In Progress:**
- Performance optimization for large datasets
- Parallel execution support

## Mining Parameters

### Period (p)

Defines the recurrence interval:
- `p=2`: Pattern repeats every 2 timesteps
- `p=3`: Pattern repeats every 3 timesteps
- etc.

**Typical range:** 2-9

### Support (s)

Minimum number of occurrences:
- `s=3`: Pattern appears at least 3 times
- `s=10`: Pattern appears at least 10 times

**Typical range:** 3-18

### Example Combinations

| File | Period | Support | Meaning |
|------|--------|---------|---------|
| p2s3.txt | 2 | 3 | Patterns repeating every 2 steps, ≥3 times |
| p5s10.txt | 5 | 10 | Patterns repeating every 5 steps, ≥10 times |
| p7s15.txt | 7 | 15 | Patterns repeating every 7 steps, ≥15 times |

## Runtime

Varies by parameters:
- **Low support (s=3-5):** 5-15 minutes per run
- **Medium support (s=10-12):** 2-5 minutes per run
- **High support (s=15-18):** 1-2 minutes per run

**Total for all combinations:** 2-4 hours

## Next Steps

After mining completes:

```bash
# Check outputs
ls -lh results/list_miner/list_miner_outputs_with_edges/

# Count results per file
wc -l results/list_miner/list_miner_outputs_with_edges/p*.txt

# Proceed to postprocessing
python scripts/03_postprocessing/run_postprocessing.py
```
