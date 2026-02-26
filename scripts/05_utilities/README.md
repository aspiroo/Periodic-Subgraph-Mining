# Stage 5: Utilities

Utility scripts for specialized analyses and quality metrics.

## Overview

This stage contains utility tools for:
- Calculating biological purity scores for gene patterns
- Counting subgraph occurrences across parameter combinations
- Extracting GO terms from FlyEnrichr enrichment results
- Identifying remaining (non-periodic) genes in each run

## Scripts

- **purity.py** - Calculate purity scores for gene patterns using GO annotations
- **subgraph_count.py** - Count and analyze subgraph statistics across runs
- **extact_GO_terms.py** - Extract GO terms from FlyEnrichr output files
- **rest_genes.py** - Identify genes not covered by any discovered periodic subgraph

## Usage

### Calculate Purity

```bash
cd scripts/05_utilities
python purity.py
```

### Count Subgraphs

```bash
python subgraph_count.py
```

### Extract GO Terms

```bash
python extact_GO_terms.py
```

### Find Remaining Genes

```bash
python rest_genes.py
```

## Input

Varies by script - see individual script headers for expected input file locations.

## Output

Analysis reports and statistics. Results are written to files in the working directory or `results/utilities/`.

## Next Stage

After utilities:
- Proceed to **Stage 6: Validation** in `scripts/06_validation/`
- See [PIPELINE.md](../../PIPELINE.md) for next steps
