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
- **filter_patterns.py** - Remove duplicates and filter components by criteria

### Remapping
- **remap_gene_ids.py** - Map node IDs to FlyBase gene IDs
- **remap_egdes_to_genes.py** - Remap edge-level output to gene-level representation
- **remap_to_gene_names.py** - Map gene IDs to gene symbols

### Output
- **split_patterns_to_files.py** - Split pattern output into individual component files

## Usage

### Step 1: Filter Components

```bash
cd scripts/04_analysis

# Remove duplicates and small components
python filter_patterns.py
```

### Step 2: Remap to Gene IDs

```bash
# Map node numbers to gene IDs
python remap_gene_ids.py
```

### Step 3: Remap Edges to Gene-Level

```bash
python remap_egdes_to_genes.py
```

### Step 4: Add Gene Names

```bash
# Convert gene IDs to gene symbols
python remap_to_gene_names.py
```

### Step 5: Split to Individual Files

```bash
python split_patterns_to_files.py
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
- Proceed to **Stage 5: Utilities** in `scripts/05_utilities/`
- See [PIPELINE.md](../../PIPELINE.md) for next steps
