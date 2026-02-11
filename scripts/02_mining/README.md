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
- Proceed to **Stage 3: Component Extraction** in `scripts/03_component_extraction/`
- See [PIPELINE.md](../../PIPELINE.md) for next steps
