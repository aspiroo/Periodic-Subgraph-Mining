# Stage 4: Analysis and Filtering

Scripts for filtering, remapping, and analyzing extracted components.

## Overview

This stage processes extracted components:
- Filters duplicates and low-quality components
- Remaps node IDs to gene IDs
- Converts gene IDs to gene symbols
- Calculates purity scores
- Prepares components for clustering

## Scripts

### Filtering
- **filtering.py** - Remove duplicates and filter by criteria
- **deduplicate.py** - Remove duplicate components

### Remapping
- **remappingGenes.py** - Map node IDs to gene IDs
- **remappingGeneNames.py** - Map gene IDs to gene symbols
- **remappingGraph.py** - Complete graph remapping

### Analysis
- **purity.py** - Calculate component purity scores
- **analyze_components.py** - Generate statistics

### Utilities
- **writingIndividualFile.py** - Split/write individual components
- **unionGenes.py** - Combine components into union network

## Usage

### Step 1: Filter Components

```bash
cd scripts/04_analysis

# Remove duplicates and small components
python filtering.py \
    --input ../../results/components/individual/ \
    --output ../../results/components/cleaned/ \
    --min-size 3 \
    --max-size 20
```

### Step 2: Remap to Gene IDs

```bash
# Map node numbers to gene IDs
python remappingGenes.py \
    --input ../../results/components/cleaned/ \
    --output ../../results/components/remapped/ \
    --mapping ../../data/mappings/gene_id_mapping.txt
```

### Step 3: Add Gene Names

```bash
# Convert gene IDs to gene symbols
python remappingGeneNames.py \
    --input ../../results/components/remapped/ \
    --output ../../results/components/gene_names/ \
    --mapping ../../data/mappings/gene_name_mapping.txt
```

### Step 4: Calculate Purity (Optional)

```bash
# Calculate biological purity of components
python purity.py \
    --input ../../results/components/gene_names/ \
    --output ../../results/purity/ \
    --annotations ../../data/annotations/go_terms.txt
```

### Step 5: Create Union Network

```bash
# Combine all components for clustering
python unionGenes.py \
    --input ../../results/components/gene_names/ \
    --output ../../results/clusters/union_network.txt
```

## Input

**Location**: `results/components/individual/`

**Format**: Individual component files with edge lists

## Output

Multiple output directories:

1. **cleaned/**: Filtered components
2. **remapped/**: Components with gene IDs
3. **gene_names/**: Components with gene symbols
4. **purity/**: Purity scores and analysis

## Filtering Parameters

- `--min-size`: Minimum number of nodes (default: 3)
- `--max-size`: Maximum number of nodes (default: 50)
- `--remove-duplicates`: Remove duplicate components
- `--min-density`: Minimum edge density

## Remapping Requirements

### Gene ID Mapping File

**Format**: `gene_id_mapping.txt`
```
node_id    gene_id
1          FBgn0000001
2          FBgn0000008
```

### Gene Name Mapping File

**Format**: `gene_name_mapping.txt`
```
gene_id        gene_symbol
FBgn0000001    abl
FBgn0000008    Acon
```

Place mapping files in `data/mappings/`.

## Validation

After each step:

```bash
# Check filtered components
ls ../../results/components/cleaned/ | wc -l

# Verify remapping
head ../../results/components/remapped/component_001.txt
head ../../results/components/gene_names/component_001.txt

# Check purity scores
head ../../results/purity/purity_scores.txt
```

## Purity Analysis

Purity measures biological coherence:
- **High purity (>0.7)**: Biologically related genes
- **Medium purity (0.4-0.7)**: Some coherence
- **Low purity (<0.4)**: Mixed function

```bash
# Generate purity report
python purity.py \
    --input ../../results/components/gene_names/ \
    --output ../../results/purity/ \
    --report

# Filter by purity
python filter_by_purity.py \
    --input ../../results/components/gene_names/ \
    --purity ../../results/purity/purity_scores.txt \
    --output ../../results/components/high_purity/ \
    --threshold 0.6
```

## Common Workflows

### Quick Analysis (Skip Purity)

```bash
# Filter → Remap → Gene Names
python filtering.py --input ... --output cleaned/
python remappingGenes.py --input cleaned/ --output remapped/
python remappingGeneNames.py --input remapped/ --output gene_names/
```

### Complete Analysis (With Purity)

```bash
# Full pipeline including purity
bash run_complete_analysis.sh
```

## Statistics

Generate component statistics:

```bash
python analyze_components.py \
    --input ../../results/components/gene_names/ \
    --output analysis_report.txt
```

Output includes:
- Number of components
- Size distribution
- Gene frequency
- Connectivity metrics

## Troubleshooting

### Issue: Remapping fails

- Check mapping file format (tab-separated)
- Verify all node IDs have mappings
- Check for typos in gene IDs

### Issue: Missing gene names

- Some genes may not have symbols
- Check FlyBase version compatibility
- Use gene IDs as fallback

### Issue: Low purity scores

- May indicate noisy components
- Consider stricter filtering in earlier stages
- Adjust mining parameters

For more help, see [docs/TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md).

## Next Stage

After analysis:
- Proceed to **Stage 5: Clustering** in `scripts/05_clustering/`
- See [PIPELINE.md](../../PIPELINE.md) for next steps
