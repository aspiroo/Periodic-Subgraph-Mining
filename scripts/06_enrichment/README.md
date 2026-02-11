# Stage 6: GO Enrichment Analysis

Scripts for Gene Ontology enrichment analysis of discovered clusters.

## Overview

This stage performs functional enrichment analysis:
- Tests clusters for enriched GO terms
- Uses FlyEnrichr for Drosophila-specific analysis
- Alternative: FuncAssociate for GO enrichment
- Identifies biological processes and pathways
- Validates biological significance of clusters

## Tools

### FlyEnrichr

**Description**: Web-based enrichment analysis for Drosophila genes.

**Website**: https://maayanlab.cloud/FlyEnrichr/

**API**: Available for programmatic access

### FuncAssociate

**Description**: GO term enrichment analysis tool.

**Alternative**: Can be used instead of or alongside FlyEnrichr.

## Scripts

### FlyEnrichr
- **flyenrichr_analysis.py** - Main FlyEnrichr script
- **batch_enrichr.py** - Batch process multiple clusters
- **parse_enrichr_results.py** - Parse and summarize results

### FuncAssociate
- **funcassociate_prepare.py** - Prepare FuncAssociate input
- **funcassociate_parse.py** - Parse FuncAssociate output

### Utilities
- **filter_enrichment.py** - Filter by p-value/FDR
- **compare_enrichments.py** - Compare across clusters
- **plot_enrichment.py** - Visualize enrichment

## Usage

### Method 1: FlyEnrichr (Recommended)

#### Step 1: Prepare Gene Lists

```bash
cd scripts/06_enrichment

# Clusters already in correct format from Stage 5
# One gene per line in each cluster file
```

#### Step 2: Run FlyEnrichr Analysis

```bash
# Single cluster
python flyenrichr_analysis.py \
    --input ../../results/clusters/individual/cluster_001.txt \
    --output ../../results/enrichment/flyenrichr/cluster_001_enrichment.txt

# All clusters (batch)
python batch_enrichr.py \
    --input ../../results/clusters/individual/ \
    --output ../../results/enrichment/flyenrichr/
```

#### Step 3: Filter Significant Terms

```bash
# Filter by adjusted p-value
python filter_enrichment.py \
    --input ../../results/enrichment/flyenrichr/ \
    --output ../../results/enrichment/flyenrichr/significant/ \
    --pvalue 0.05 \
    --fdr 0.1
```

### Method 2: FuncAssociate (Alternative)

#### Step 1: Prepare Input

```bash
# Convert to FuncAssociate format
python funcassociate_prepare.py \
    --input ../../results/clusters/individual/ \
    --output ../../results/enrichment/funcassociate/input/
```

#### Step 2: Run FuncAssociate

Follow FuncAssociate web interface or API instructions.

#### Step 3: Parse Results

```bash
python funcassociate_parse.py \
    --input ../../results/enrichment/funcassociate/raw/ \
    --output ../../results/enrichment/funcassociate/parsed/
```

## FlyEnrichr Libraries

Common libraries to query:

- **GO Biological Process 2018**
- **GO Molecular Function 2018**
- **GO Cellular Component 2018**
- **KEGG 2019**
- **WikiPathways 2019**
- **Reactome 2016**

Specify in scripts:

```python
libraries = [
    'GO_Biological_Process_2018',
    'GO_Molecular_Function_2018',
    'KEGG_2019_Fly'
]
```

## Output Format

### FlyEnrichr Output

Tab-separated file for each cluster:

```
Rank    Term                           P-value    Adjusted_P-value    Genes
1       cell cycle (GO:0007049)       1.23e-08   4.56e-06           abl;ace;brk
2       DNA replication (GO:0006260)  5.67e-07   1.23e-04           btn;bun;arr
```

### Summary Statistics

```bash
# Generate summary across all clusters
python summarize_enrichment.py \
    --input ../../results/enrichment/flyenrichr/ \
    --output enrichment_summary.txt
```

Output:
```
Cluster    Total_Terms    Significant_Terms    Top_Term                  Top_P-value
cluster_001    45            12                 cell cycle                 1.23e-08
cluster_002    38            8                  development               3.45e-06
```

## Validation

### Check Enrichment Results

```bash
# Count enriched clusters
ls ../../results/enrichment/flyenrichr/*.txt | wc -l

# View top terms for each cluster
for f in ../../results/enrichment/flyenrichr/*.txt; do
    echo "=== $f ==="
    head -5 $f
done
```

### Quality Criteria

Good enrichment results:
- **P-value < 0.05**: Statistically significant
- **Adjusted P-value < 0.1**: Passes multiple testing correction
- **Multiple related terms**: Biological coherence
- **Matches cluster genes**: Makes sense for gene set

## Visualization

### Bar Plots

```bash
# Plot top terms for each cluster
python plot_enrichment.py \
    --input ../../results/enrichment/flyenrichr/cluster_001_enrichment.txt \
    --output cluster_001_barplot.png \
    --top 10
```

### Heatmap

```bash
# Compare enrichment across clusters
python plot_enrichment_heatmap.py \
    --input ../../results/enrichment/flyenrichr/ \
    --output enrichment_heatmap.png \
    --metric combined_score
```

### Network View

```bash
# Visualize term relationships
python plot_term_network.py \
    --input ../../results/enrichment/flyenrichr/ \
    --output term_network.png
```

## Parameter Options

### P-value Threshold

- **Stringent (p < 0.01)**: High confidence only
- **Standard (p < 0.05)**: Commonly used
- **Permissive (p < 0.1)**: Exploratory

### FDR Correction

Always use FDR/Bonferroni correction for multiple testing:

```bash
--fdr 0.05    # Standard
--fdr 0.1     # Permissive
```

## Advanced Analysis

### Compare Enrichment Patterns

```bash
# Find common enriched terms
python find_common_terms.py \
    --input ../../results/enrichment/flyenrichr/ \
    --output common_terms.txt \
    --min-clusters 3
```

### Cluster by Enrichment Profile

```bash
# Cluster by GO term enrichment similarity
python cluster_by_enrichment.py \
    --input ../../results/enrichment/flyenrichr/ \
    --output enrichment_clusters.txt
```

### Export for Cytoscape

```bash
# Create Cytoscape-compatible network
python export_for_cytoscape.py \
    --clusters ../../results/clusters/individual/ \
    --enrichment ../../results/enrichment/flyenrichr/ \
    --output cytoscape_network.txt
```

## Troubleshooting

### Issue: No enrichment found

- Check gene names are correct (gene symbols, not IDs)
- Verify cluster size (need ≥3 genes typically)
- Check species (must be Drosophila for FlyEnrichr)
- Try different background gene set

### Issue: API rate limiting

FlyEnrichr API may rate limit:
- Add delays between requests
- Process in smaller batches
- Use local tools if available

### Issue: Low significance

- Clusters may not be functionally coherent
- Try merging similar clusters
- Review clustering parameters (Stage 5)
- Check mining parameters (Stage 2)

### Issue: Generic terms only

- Terms like "metabolic process" too broad
- Filter for more specific terms
- Check term hierarchy level
- Look at combined score, not just p-value

For more help, see [docs/TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md).

## Interpretation Guidelines

### Strong Evidence
- Multiple related specific terms
- Very low p-values (< 1e-5)
- High gene coverage
- Literature support

### Moderate Evidence
- Few related terms
- Moderate p-values (< 0.01)
- Partial gene coverage

### Weak Evidence
- Generic terms only
- Borderline p-values (0.05-0.1)
- Single term

## Biological Validation

After enrichment analysis:

1. **Literature Review**: Check published studies
2. **Database Search**: FlyBase, GO, KEGG
3. **Expression Patterns**: Compare with developmental stages
4. **Protein Interactions**: Validate with BioGRID
5. **Phenotypes**: Check for shared mutant phenotypes

## Reporting Results

Include in reports:
- Number of enriched clusters
- Top terms per cluster
- P-values and FDR
- Biological interpretation
- Validation against literature

## Next Steps

After enrichment analysis:
1. Interpret biological significance
2. Validate key findings experimentally
3. Write up results
4. See [docs/PAPER_REPLICATION.md](../../docs/PAPER_REPLICATION.md) for publication

## References

- **FlyEnrichr**: Chen et al., 2013
- **GO Consortium**: Ashburner et al., 2000; Gene Ontology Consortium, 2019
- **FuncAssociate**: Berriz et al., 2009

## Pipeline Complete!

Congratulations! You've completed all six stages of the periodic subgraph mining pipeline.

**Final outputs**:
- Frequent subgraphs (`results/listminer_output/`)
- Cleaned components (`results/components/`)
- Functional clusters (`results/clusters/`)
- GO enrichment (`results/enrichment/`)

For further analysis, see notebooks in `notebooks/` directory.
