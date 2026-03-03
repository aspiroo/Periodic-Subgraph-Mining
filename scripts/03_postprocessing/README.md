# Stage 3: Post-processing

Scripts for remapping ListMiner output to gene identifiers and preparing components for analysis.

## Overview

This stage transforms the raw ListMiner output into biologically meaningful files:
- Numbers gene files from the ListMiner edge output
- Remaps edge numbers back to gene-level graph representations
- Remaps numeric node IDs to gene numbers (FlyBase IDs)
- Remaps gene numbers to gene names (symbols)
- Generates a "development genes" subset file
- Produces a union-genes file combining all identified genes

## Scripts

- **01_number_gene_files.py** - Adds line numbers to gene files from ListMiner output
- **02_remap_edges_to_graph.py** - Converts edge-number output back to node-level graph files
- **03_remap_to_gene_numbers.py** - Maps numeric node IDs to FlyBase gene IDs
- **04_remap_to_gene_names.py** - Converts FlyBase gene IDs to human-readable gene symbols
- **05_generate_development_genes.py** - Extracts the "just development" gene subset
- **06_union_genes.py** - Combines all components into a single union-genes file

## Usage

### Step 1: Number gene files

```bash
cd scripts/03_postprocessing

python 01_number_gene_files.py
```

### Step 2: Remap edges to graph

```bash
python 02_remap_edges_to_graph.py
```

### Step 3: Remap to gene numbers

```bash
python 03_remap_to_gene_numbers.py
```

### Step 4: Remap to gene names

```bash
python 04_remap_to_gene_names.py
```

### Step 5: Generate development genes

```bash
python 05_generate_development_genes.py
```

### Step 6: Generate union genes

```bash
python 06_union_genes.py
```

## Input

**Location**: `results/listminer_output/`

**Format**: ListMiner output files containing frequent subgraph edge lists

## Output

Multiple output files:
- Numbered gene files
- Node-level graph files per component
- Remapped components with FlyBase IDs
- Components with gene symbol names
- Development gene subset
- Union genes file (`results/clusters/union_network.txt`)

## Troubleshooting

### Issue: Missing input files

- Verify ListMiner output exists in `results/listminer_output/`
- Check that Stage 2 (mining) completed successfully

### Issue: Remapping produces empty output

- Check that mapping files exist in `data/mappings/`
- Verify the format of gene ID and gene name mapping files

For more help, see [docs/TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md).

## Next Stage

After post-processing:
- Proceed to **Stage 4: Analysis** in `scripts/04_analysis/`
- See [PIPELINE.md](../../PIPELINE.md) for next steps

## Current Status

🚧 **In Development**

### Completed Analysis

✅ ListMiner outputs generated
✅ Input files identified

### Next Steps

❌ Union genes script (06_union_genes.py) - needs adaptation
❌ Remap edges script (02_remap_edges_to_graph.py) - needs input
❌ Gene number mapping (03_remap_to_gene_numbers.py)
❌ Gene name mapping (04_remap_to_gene_names.py)
❌ Development genes (05_generate_development_genes.py)

## Planned Wrapper

```bash
# Future usage
python scripts/03_postprocessing/run_postprocessing.py
```

This will run:
1. Generate union of genes (06_union_genes.py)
2. Remap edges to graph (02_remap_edges_to_graph.py)
3. Remap to gene numbers (03_remap_to_gene_numbers.py)
4. Remap to gene names (04_remap_to_gene_names.py)
5. Generate development genes (05_generate_development_genes.py)
6. Number gene files (01_number_gene_files.py)

## Required Inputs

From mining stage:
- `results/list_miner/list_miner_outputs_with_edges/p*s*.txt`

From preprocessing:
- `data/processed/outputWithEdgeNum.txt` ✅ Exists
- `data/raw/Just_development.txt` ✅ Exists
- `data/raw/genenames.txt` ✅ Exists

## Expected Outputs

```
results/
├── components/
│   ├── remapped/              # Remapped components
│   ├── gene_numbers/          # With gene numbers
│   └── gene_names/            # With gene names
│
├── listminer_output/
│   └── union_genes/           # Union across supports
│
└── temp/                      # Temporary files
```

## Script Dependencies

The correct execution order:

```
01_number_gene_files.py          # First - creates mappings
        ↓
06_union_genes.py                # Creates union files
        ↓
02_remap_edges_to_graph.py       # Extracts components
        ↓
03_remap_to_gene_numbers.py      # Maps to numbers
        ↓
04_remap_to_gene_names.py        # Maps to names
        ↓
05_generate_development_genes.py # Filters development genes
```

## Timeline

**Target completion:** Next session
**Blockers:** Script adaptation for current output format
