# Stage 6: Validation

Scripts for validating and comparing results.

## Overview

This stage validates pipeline results through:
- Randomization tests
- Rare minimal itemset analysis
- Union gene comparisons
- Statistical validation

## Scripts

### Randomization
- **randomize/Code/** - Randomization scripts
- **randomize/Data/** - Randomization results

### Rare Minimal Itemsets
- **rare_minimal_itemset/Code/** - Itemset analysis scripts
- **rare_minimal_itemset/Data/** - Itemset results

### Union Gene Analysis
- **union_genes/Data/** - Combined gene set analysis
  - GO enrichment results for 588 union genes
  - REVIGO summaries
  - Biological process, cellular component, and molecular function annotations

## Usage

Run validation scripts after completing main pipeline to verify results and perform comparative analyses.

## Input

Results from previous pipeline stages

## Output

Validation reports and comparison statistics in `results/validation/`
