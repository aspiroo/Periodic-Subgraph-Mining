# Stage 3: Component Extraction

Scripts for extracting individual connected components from mined subgraphs.

## Overview

This stage processes ListMiner output to extract discrete connected components:
- Parses frequent subgraph results
- Identifies connected components within each subgraph
- Splits multi-component graphs into individual files
- Generates one file per component for downstream analysis

## Scripts

- **subgraph_count.py** - Main component extraction
- **extract_components.py** - Component identification
- **split_graphs.py** - Split multi-component graphs

## Usage

### Basic Extraction

```bash
cd scripts/03_component_extraction

# Extract components from mining results
python subgraph_count.py \
    --input ../../results/listminer_output/support_3_size_4/ \
    --output ../../results/components/individual/
```

### Advanced Options

```bash
# Extract with minimum component size filter
python subgraph_count.py \
    --input ../../results/listminer_output/support_3_size_4/ \
    --output ../../results/components/individual/ \
    --min-nodes 3 \
    --max-nodes 20
```

## Input

**Location**: `results/listminer_output/*/`

**Format**: ListMiner output files containing frequent subgraphs

## Output

**Location**: `results/components/individual/`

**Format**: One file per connected component

```
component_001.txt
component_002.txt
...
component_N.txt
```

Each file contains an edge list:
```
node1  node2
1      2
2      3
3      4
```

## Parameters

- `--input`: Directory with ListMiner output
- `--output`: Directory for extracted components
- `--min-nodes`: Minimum component size (default: 2)
- `--max-nodes`: Maximum component size (default: unlimited)
- `--format`: Output format (edgelist, adjacency)

## Validation

After extraction:

```bash
# Count extracted components
ls ../../results/components/individual/ | wc -l

# View component sizes
for f in ../../results/components/individual/*.txt; do
    echo "$f: $(wc -l < $f) edges"
done | head -10

# Check sample component
head ../../results/components/individual/component_001.txt
```

## Component Statistics

Generate statistics:

```bash
python analyze_components.py \
    --input ../../results/components/individual/ \
    --output component_stats.txt
```

Typical output:
```
Total components: 523
Mean size: 4.2 nodes
Median size: 4 nodes
Size range: 3-15 nodes
```

## Filtering

Components can be filtered by various criteria:

```bash
# Filter by size
python filter_components.py \
    --input ../../results/components/individual/ \
    --output ../../results/components/filtered/ \
    --min-size 4 \
    --max-size 10

# Remove duplicates
python deduplicate_components.py \
    --input ../../results/components/individual/ \
    --output ../../results/components/unique/
```

## Visualization

Visualize extracted components:

```bash
# Generate summary plot
python plot_components.py \
    --input ../../results/components/individual/ \
    --output component_distribution.png
```

## Troubleshooting

### Issue: No components extracted

- Check ListMiner output is not empty
- Verify input path is correct
- Check minimum size threshold

### Issue: Too many small components

- Increase `--min-nodes` parameter
- Check mining support threshold (may be too low)

### Issue: Memory errors

- Process in batches
- Filter by size during extraction

For more help, see [docs/TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md).

## Next Stage

After component extraction:
- Proceed to **Stage 4: Analysis** in `scripts/04_analysis/`
- See [PIPELINE.md](../../PIPELINE.md) for next steps
