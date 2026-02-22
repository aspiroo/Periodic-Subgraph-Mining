# Paper Replication Guide

Instructions for replicating the results from the periodic subgraph mining publication.

## Overview

This guide helps you reproduce the computational analyses and results described in the associated publication. It covers data acquisition, parameter settings, and expected outcomes.

## Publication Information

**Title**: [Paper title to be added]

**Authors**: [Authors to be added]

**Journal**: [Journal to be added]

**DOI**: [DOI to be added]

**Abstract**: [Brief description of the paper's findings]

## Prerequisites

Before starting:
- Read the paper thoroughly
- Understand the methodology
- Have necessary computational resources (see [Resource Requirements](#resource-requirements))
- Install all required software (see main [README.md](../README.md))

## Resource Requirements

### Hardware

**Minimum**:
- CPU: 4 cores
- RAM: 8 GB
- Disk: 50 GB free space

**Recommended**:
- CPU: 8+ cores
- RAM: 16+ GB
- Disk: 100 GB free space
- SSD for faster I/O

### Software

- Python 3.7+
- Java 8+ (for ClusterONE)
- MATLAB R2016b+ (optional, for Keller network processing)
- ListMiner binary
- ClusterONE JAR

### Time Estimates

Complete pipeline runtime (typical hardware):
- Preprocessing: 10-30 minutes
- Mining: 2-6 hours (varies with parameters)
- Component extraction: 10-30 minutes
- Analysis: 20-60 minutes
- Clustering: 5-15 minutes
- Enrichment: 15-45 minutes

**Total**: ~4-10 hours for complete pipeline

## Data Acquisition

### Keller Lab Data

**Source**: [Data source URL or reference]

**Download**:
```bash
# The Keller data is already present in data/raw/keller_data/
# drosophila.mat, drosophila_filtered.mat, drosophila.rawdata

# If you need to re-obtain the data from the original source:
mkdir -p data/raw/keller_data
wget [URL] -O data/raw/keller_data/keller_data.mat
```

**Description**: Temporal gene regulatory networks during Drosophila embryogenesis

**Time points**: X timesteps spanning Y-Z hours of development

**Genes**: Approximately N genes

### Gene Annotations

**FlyBase Version**: [Specific release, e.g., FB2021_05]

**Download**:
```bash
# Gene ID mappings
wget ftp://ftp.flybase.net/releases/FB2021_05/precomputed_files/genes/fbgn_annotation_ID.tsv.gz \
    -O data/mappings/fbgn_annotations.tsv.gz

gunzip data/mappings/fbgn_annotations.tsv.gz

# Gene names
wget ftp://ftp.flybase.net/releases/FB2021_05/precomputed_files/genes/gene_map_table_fb_2021_05.tsv.gz \
    -O data/mappings/gene_names.tsv.gz

gunzip data/mappings/gene_names.tsv.gz
```

**Process mappings**:
```bash
# Extract node ID to gene ID mapping
python scripts/create_mappings.py \
    --input data/raw/keller_data/drosophila.mat \
    --fbgn data/mappings/fbgn_annotations.tsv \
    --output data/mappings/gene_id_mapping.txt

# Create gene name mapping
python scripts/create_name_mapping.py \
    --input data/mappings/fbgn_annotations.tsv \
    --names data/mappings/gene_names.tsv \
    --output data/mappings/gene_name_mapping.txt
```

### GO Annotations

**Source**: Gene Ontology Consortium

**Download**:
```bash
wget http://current.geneontology.org/annotations/fb.gaf.gz \
    -O data/annotations/drosophila_go.gaf.gz

gunzip data/annotations/drosophila_go.gaf.gz
```

## Exact Parameters Used in Paper

### Stage 1: Preprocessing

No parameters (follows Keller lab protocols)

```bash
cd matlab/network_generation
matlab -nodisplay -r "keller; exit"
```

**Output**: X timestep files

### Stage 2: Subgraph Mining

**ListMiner Parameters**:
```bash
# Main analysis
./listminer \
    -i data/processed/timesteps/ \
    -o results/listminer_output/main_analysis/ \
    -s 3 \
    -min 3 \
    -max 6

# Sensitivity analysis (if applicable)
for support in 2 3 4 5; do
    ./listminer \
        -i data/processed/timesteps/ \
        -o results/listminer_output/support_${support}/ \
        -s $support \
        -min 3 \
        -max 6
done
```

**Expected Output**: 
- Support=3: ~X frequent subgraphs
- Support=4: ~Y frequent subgraphs
- Support=5: ~Z frequent subgraphs

### Stage 3: Component Extraction

```bash
cd scripts/05_utilities
python subgraph_count.py
```

**Expected Output**: ~N components

### Stage 4: Analysis and Filtering

**Filtering**:
```bash
cd scripts/04_analysis

# Filter components
python filter_patterns.py
```

**Expected Output**: ~M cleaned components

**Remapping**:
```bash
# Remap to gene IDs
python remap_gene_ids.py

# Add gene names
python remap_to_gene_names.py
```

**Purity Calculation**:
```bash
cd ../05_utilities
python purity.py
```

**Expected**: Mean purity score ~X.XX

### Stage 5: Clustering

**Prepare Union Network**:
```bash
cd scripts/03_postprocessing
python 06_union_genes.py
```

**ClusterONE Parameters**:
```bash
cd external_tools/clusterone

java -jar cluster_one-1.0.jar \
    ../../results/clusters/union_network.txt \
    -s 3 \
    -d 0.3 \
    > ../../results/clusters/clusters.txt
```

**Expected Output**: ~K clusters

**Key Clusters** (as reported in paper):
- Cluster 1: Cell cycle genes (X genes)
- Cluster 2: Development genes (Y genes)
- Cluster 3: [Description] (Z genes)

### Stage 6: Enrichment

**FlyEnrichr Analysis**:
```bash
cd scripts/05_utilities

# Extract GO terms from results
python extact_GO_terms.py
```

**Significance Threshold**: FDR < 0.05

**Expected Enrichments** (examples from paper):
- Cluster 1: "cell cycle" (p < 1e-6)
- Cluster 2: "pattern specification" (p < 1e-5)
- Cluster 3: [GO term] (p-value)

## Expected Results Summary

### Quantitative Results

Compare your results with these expected values:

| Metric | Expected Value | Your Value |
|--------|---------------|------------|
| Timesteps | X | |
| Genes | N | |
| Frequent subgraphs (s=3) | ~X | |
| Components extracted | ~N | |
| Components after filtering | ~M | |
| Mean purity score | ~X.XX | |
| Final clusters | ~K | |
| Enriched clusters (FDR<0.05) | ~J | |

### Key Findings

The pipeline should identify:

1. **Cell Cycle Module**: 
   - Genes: [list key genes]
   - GO enrichment: cell cycle, DNA replication
   - Figure in paper: Figure X

2. **Developmental Module**:
   - Genes: [list key genes]
   - GO enrichment: pattern specification, embryo development
   - Figure in paper: Figure Y

3. **[Additional Module]**:
   - Description
   - Figure reference

## Validation Steps

### 1. Verify Intermediate Results

```bash
# Check timestep count
ls data/processed/timesteps/*.txt | wc -l

# Verify subgraph count
wc -l results/listminer_output/main_analysis/frequent_subgraphs.txt

# Check component count
ls results/components/individual/*.txt | wc -l

# Verify cluster count
wc -l results/clusters/clusters.txt
```

### 2. Compare Gene Lists

Extract key gene lists and compare:

```bash
# Extract genes from Cluster 1
head results/clusters/individual/cluster_001.txt

# Should include (from paper): [list expected genes]
```

### 3. Verify GO Enrichment

```bash
# Check top enriched terms for key cluster
head results/enrichment/flyenrichr/cluster_001_enrichment.txt

# Top term should be: [expected GO term]
# P-value should be: < [threshold]
```

## Common Discrepancies

### Minor Variations Expected

- **Gene counts**: ±5% due to mapping version differences
- **P-values**: Small differences due to background gene set
- **Cluster composition**: Minor differences (1-2 genes) acceptable

### Major Discrepancies to Investigate

- **>20% difference in component count**: Check mining parameters
- **Missing key genes**: Verify gene ID mappings
- **No enrichment found**: Check FlyBase version, GO annotations
- **Different cluster structure**: Verify ClusterONE parameters

## Figures from Paper

*(Note: Jupyter notebooks for figure reproduction are not yet included in this repository.)*

### Figure 1: Network Overview
- **Data**: Keller networks (`data/raw/keller_data/`)
- **Script**: To be created
- **Output**: Network visualization across timepoints

### Figure 2: Mining Results
- **Data**: ListMiner output (support=3)
- **Script**: To be created
- **Output**: Frequent subgraph statistics

### Figure 3: Cluster Analysis
- **Data**: ClusterONE clusters
- **Script**: To be created
- **Output**: Cluster network visualization

### Figure 4: GO Enrichment
- **Data**: FlyEnrichr results
- **Script**: To be created
- **Output**: Enrichment bar plots

## Supplementary Materials

### Supplementary Table 1: All Clusters
**File**: `results/clusters/clusters_annotated.txt`
**Columns**: Cluster ID, Genes, Size, Quality, Top GO term

### Supplementary Table 2: GO Enrichment
**File**: `results/enrichment/all_enrichment_summary.txt`
**Columns**: Cluster, GO term, P-value, Adjusted P-value, Genes

### Supplementary Figure 1: Parameter Sensitivity
**Script**: To be created
**Shows**: Effect of support threshold on results

## Troubleshooting Replication

### Results Don't Match

1. **Verify data source**: Same Keller dataset?
2. **Check software versions**: ListMiner version, Python version
3. **Confirm parameters**: Exact same as listed above?
4. **Check random seeds**: If applicable
5. **Verify FlyBase version**: Using same gene annotations?

### Cannot Obtain Data

- Contact paper authors for data access
- Check journal supplementary materials
- Look for deposited data (GEO, ArrayExpress, etc.)

### Tools Not Available

- ListMiner: Contact authors or use alternative (gSpan, FSG)
- ClusterONE: Available at http://www.paccanarolab.org/cluster-one/
- If substituting tools, results may differ

## Citing This Work

If you replicate these results, please cite:

```
[Citation format to be added]
```

And acknowledge:
- Keller Lab (for network data)
- ListMiner authors
- ClusterONE authors
- FlyEnrichr team

## Contact for Replication Issues

For questions about replication:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Open GitHub issue
3. Contact paper authors: [contact info]

## Reproducibility Checklist

- [ ] Obtained original data
- [ ] Installed all required software
- [ ] Downloaded correct FlyBase version
- [ ] Ran preprocessing
- [ ] Completed mining with exact parameters
- [ ] Extracted components
- [ ] Filtered and remapped
- [ ] Performed clustering
- [ ] Calculated enrichment
- [ ] Compared results with paper
- [ ] Validated key findings
- [ ] Generated figures (if applicable)

## Additional Resources

- **Paper PDF**: [Link or DOI]
- **Supplementary Materials**: [Link]
- **Data Repository**: [GEO/ArrayExpress ID]
- **Code Repository**: This GitHub repository
- **Original Analysis Scripts**: In `legacy/` directory
## Updates and Errata

**Last Updated**: [Date]

**Known Issues**:
- [Any known discrepancies or corrections]

**Updates Since Publication**:
- [Any changes to code or pipeline]

---

**Good luck with replication!**

For questions, open a GitHub issue or contact the authors.
