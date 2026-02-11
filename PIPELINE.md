# Pipeline Execution Guide

Complete step-by-step instructions for running the periodic subgraph mining pipeline.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Stage 1: Data Preprocessing](#stage-1-data-preprocessing)
3. [Stage 2: Subgraph Mining](#stage-2-subgraph-mining)
4. [Stage 3: Component Extraction](#stage-3-component-extraction)
5. [Stage 4: Analysis and Filtering](#stage-4-analysis-and-filtering)
6. [Stage 5: Clustering](#stage-5-clustering)
7. [Stage 6: Enrichment Analysis](#stage-6-enrichment-analysis)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Python 3.x** - For most processing scripts
- **Java 8+** - For ClusterONE
- **MATLAB** (optional) - For Keller network preprocessing
- **ListMiner** - Compiled binary (see `external_tools/listminer/`)

### Data Requirements

You need:
1. Temporal gene regulatory network files
2. Gene ID to gene name mapping file
3. (Optional) Keller lab network data

Place raw data in `data/raw/`. See `data/raw/README.md` for format details.

### Initial Setup

```bash
# Create directory structure
bash setup_structure.sh

# Verify structure
ls -R data/ results/ scripts/ external_tools/
```

## Stage 1: Data Preprocessing

**Goal**: Convert raw network data into format suitable for ListMiner.

### 1.1 Process Keller Networks (Optional)

If using Keller lab data:

```bash
cd "Keller codes"
matlab -nodisplay -r "keller; exit"
```

This generates timestamped network files in MATLAB format.

### 1.2 Convert to Text Format

```bash
cd "Preprocessing Code"

# Convert MATLAB networks to text format
python preprocessing_script.py \
    --input ../data/raw/keller_networks/ \
    --output ../data/processed/timesteps/
```

**Output**: Individual text files for each time step in `data/processed/timesteps/`

### 1.3 Verify Preprocessing

```bash
# Check output files
ls -lh data/processed/timesteps/

# View sample file format (should be edge list: nodeA nodeB)
head data/processed/timesteps/timestep_01.txt
```

**Expected Format**: Tab-separated edge list
```
1    2
1    5
2    3
...
```

## Stage 2: Subgraph Mining

**Goal**: Use ListMiner to discover frequent subgraphs across time steps.

### 2.1 Prepare ListMiner Input

ListMiner requires:
- Input directory with timestep files
- Support threshold (frequency)
- Subgraph size parameters

### 2.2 Run ListMiner

```bash
cd external_tools/listminer

# Single run example
./listminer \
    -i ../../data/processed/timesteps/ \
    -o ../../results/listminer_output/support_3_size_4/ \
    -s 3 \
    -min 3 \
    -max 4

# Run multiple parameter combinations
cd ../../scripts/02_mining
bash run_listminer.sh
```

**Parameters**:
- `-i`: Input directory
- `-o`: Output directory
- `-s`: Support threshold (minimum occurrences)
- `-min`: Minimum subgraph size
- `-max`: Maximum subgraph size

### 2.3 Verify Mining Output

```bash
ls -lh results/listminer_output/

# Check mining results
head results/listminer_output/support_3_size_4/frequent_subgraphs.txt
```

**Typical Runtime**: 10 minutes to several hours depending on data size and parameters.

## Stage 3: Component Extraction

**Goal**: Extract individual connected components from mined subgraphs.

### 3.1 Run Component Extraction

```bash
cd "Subgraph Code"

python subgraph_count.py \
    --input ../results/listminer_output/support_3_size_4/ \
    --output ../results/components/individual/
```

**Output**: One file per connected component in `results/components/individual/`

### 3.2 Verify Extraction

```bash
# Count extracted components
ls results/components/individual/ | wc -l

# View sample component
head results/components/individual/component_001.txt
```

## Stage 4: Analysis and Filtering

**Goal**: Filter components and remap gene IDs to gene names.

### 4.1 Filter Components

```bash
cd "Analysis Code"

# Remove duplicates and small components
python filtering.py \
    --input ../results/components/individual/ \
    --output ../results/components/cleaned/ \
    --min-size 3
```

### 4.2 Remap to Gene IDs

```bash
# Remap node numbers to gene IDs
python remappingGenes.py \
    --input ../results/components/cleaned/ \
    --output ../results/components/remapped/ \
    --mapping ../data/mappings/gene_id_mapping.txt
```

### 4.3 Add Gene Names

```bash
cd "../Post Processing Code"

# Convert gene IDs to gene symbols
python remappingGeneNames.py \
    --input ../results/components/remapped/ \
    --output ../results/components/gene_names/ \
    --mapping ../data/mappings/gene_name_mapping.txt
```

### 4.4 Calculate Purity (Optional)

```bash
cd "../Purity Code"

python purity.py \
    --input ../results/components/gene_names/ \
    --output ../results/purity/
```

### 4.5 Verify Analysis

```bash
# Check processed components
ls -lh results/components/gene_names/

# View component with gene names
head results/components/gene_names/component_001_genes.txt
```

## Stage 5: Clustering

**Goal**: Cluster components into functional modules using ClusterONE.

### 5.1 Prepare Clustering Input

Components need to be combined into a single network file:

```bash
cd "Post Processing Code"

python unionGenes.py \
    --input ../results/components/gene_names/ \
    --output ../results/clusters/union_network.txt
```

### 5.2 Run ClusterONE

```bash
cd ClusterOne

java -jar cluster_one-1.0.jar \
    ../results/clusters/union_network.txt \
    -s 3 \
    > ../results/clusters/clusters.txt
```

**Parameters**:
- `-s`: Minimum cluster size (default: 3)
- `-d`: Density threshold (default: auto)

### 5.3 Process Clusters

```bash
# Extract individual clusters
python process_clusters.py \
    --input ../results/clusters/clusters.txt \
    --output ../results/clusters/individual/
```

### 5.4 Verify Clustering

```bash
# Check clusters
ls -lh results/clusters/individual/

# View cluster sizes
wc -l results/clusters/individual/*.txt
```

## Stage 6: Enrichment Analysis

**Goal**: Perform GO term enrichment analysis on gene clusters.

### 6.1 FlyEnrichr Analysis

```bash
cd "FlyEnrichR Code"

# Run enrichment for each cluster
for cluster in ../results/clusters/individual/*.txt; do
    python flyenrichr_analysis.py \
        --input "$cluster" \
        --output ../results/enrichment/flyenrichr/
done
```

### 6.2 FuncAssociate Analysis (Alternative)

```bash
cd Funcassociate

# Prepare input files
python prepare_funcassociate.py \
    --input ../results/clusters/individual/ \
    --output ../results/enrichment/funcassociate/input/

# Run FuncAssociate (follow tool-specific instructions)
```

### 6.3 Verify Enrichment

```bash
# Check enrichment results
ls -lh results/enrichment/flyenrichr/

# View top enriched terms
head -20 results/enrichment/flyenrichr/cluster_001_enrichment.txt
```

## Verification

### Check All Stages Completed

```bash
# Verify output from each stage
bash scripts/verify_pipeline.sh
```

### Expected Directory Contents

```
data/processed/timesteps/           # ~50-100 timestep files
results/listminer_output/           # Frequent subgraphs
results/components/gene_names/      # ~100-1000 components
results/clusters/individual/        # ~10-50 clusters
results/enrichment/flyenrichr/      # Enrichment for each cluster
```

### Quality Checks

1. **Preprocessing**: All timesteps should have similar file sizes
2. **Mining**: Check for reasonable number of frequent patterns
3. **Components**: Verify gene names map correctly
4. **Clusters**: Inspect biological coherence
5. **Enrichment**: Look for significant GO terms (p < 0.05)

## Troubleshooting

### Common Issues

#### ListMiner fails to run
```bash
# Check binary permissions
chmod +x external_tools/listminer/listminer

# Test with small dataset
./listminer -i test_data/ -o test_output/ -s 2 -min 2 -max 3
```

#### Memory errors during mining
- Reduce support threshold (-s parameter)
- Process time steps in batches
- Increase available memory

#### Missing gene mappings
- Check mapping file format (see `docs/DATA_FORMAT.md`)
- Verify gene IDs match between network and mapping files

#### Empty clustering results
- Check union network file is not empty
- Reduce ClusterONE minimum cluster size (-s parameter)
- Adjust density threshold

For detailed troubleshooting, see **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**.

## Parameter Tuning

### ListMiner Support Threshold

- **Higher support (s=5-10)**: Fewer, more frequent patterns
- **Lower support (s=2-3)**: More patterns, less stringent

### Subgraph Size

- **Smaller (3-4 nodes)**: Faster mining, more patterns
- **Larger (5-8 nodes)**: Slower mining, more specific patterns

### ClusterONE Density

- **Higher density (0.5-0.8)**: Tighter, smaller clusters
- **Lower density (0.2-0.4)**: Looser, larger clusters

## Advanced Usage

### Batch Processing

```bash
# Run complete pipeline with one command
cd scripts
bash run_complete_pipeline.sh \
    --input ../data/raw/ \
    --output ../results/full_run_001/
```

### Custom Parameters

Edit configuration files in `scripts/config/` to set default parameters.

### Parallel Processing

Use GNU parallel for faster component processing:

```bash
ls results/components/cleaned/*.txt | \
    parallel python remapping.py --input {} --output results/components/remapped/
```

## Next Steps

After completing the pipeline:

1. **Explore Results**: Use Jupyter notebooks in `notebooks/`
2. **Visualize Networks**: Use Cytoscape for network visualization
3. **Compare Conditions**: Run pipeline on different datasets
4. **Validate Findings**: Use literature and databases to validate discovered modules

## References

- **ListMiner**: [Citation/URL]
- **ClusterONE**: Nepusz et al., 2012
- **FlyEnrichr**: Chen et al., 2013

For questions or issues, open a GitHub issue or consult the documentation in `docs/`.
