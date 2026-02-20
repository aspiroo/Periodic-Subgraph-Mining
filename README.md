# Periodic Subgraph Mining in Dynamic Networks

A computational pipeline for mining periodic subgraphs in temporal gene regulatory networks during Drosophila embryogenesis.

## Overview

This project implements methods for discovering recurring patterns (periodic subgraphs) in dynamic biological networks. The pipeline processes time-series gene expression data from Drosophila embryogenesis, mines frequent subgraphs using ListMiner, and identifies functional gene modules through clustering and enrichment analysis.

## Quick Start

### Prerequisites

- Python 3.x
- MATLAB (optional, for preprocessing Keller networks)
- Java (for ClusterONE clustering)
- ListMiner compiled binary (see `external_tools/listminer/`)

### Running the Pipeline

```bash
# 1. Set up directory structure
bash setup_structure.sh

# 2. Prepare your data (see PIPELINE.md for details)
# Place network files in data/raw/

# 3. Run the complete pipeline (see PIPELINE.md)
# Follow steps in PIPELINE.md for detailed execution

# 4. View results
# Results will be generated in results/ directory
```

For detailed step-by-step instructions, see **[PIPELINE.md](PIPELINE.md)**.

## Repository Structure

```
.
├── data/                          # Input data (not in git)
│   ├── raw/                       # Original network files
│   │   └── keller_networks/       # Keller lab network data
│   ├── processed/                 # Preprocessed networks
│   │   └── timesteps/             # Individual time step files
│   └── mappings/                  # Gene ID mappings
│
├── results/                       # Pipeline outputs (not in git)
│   ├── listminer_output/          # Raw ListMiner results
│   ├── components/                # Extracted graph components
│   │   ├── individual/            # Individual component files
│   │   ├── cleaned/               # After filtering
│   │   ├── remapped/              # With updated IDs
│   │   └── gene_names/            # With gene symbols
│   ├── purity/                    # Purity analysis results
│   ├── clusters/                  # Clustered modules
│   └── enrichment/                # GO enrichment results
│       ├── flyenrichr/            # FlyEnrichr analysis
│       └── funcassociate/         # FuncAssociate analysis
│
├── scripts/                       # Organized pipeline scripts
│   ├── 01_preprocessing/          # Data preparation
│   ├── 02_mining/                 # Subgraph mining with ListMiner
│   ├── 03_postprocessing/         # Post-processing (remapping, numbering)
│   ├── 04_analysis/               # Filtering and analysis
│   ├── 05_utilities/              # Utility scripts (purity, subgraph count, GO extraction)
│   └── 06_validation/             # Validation scripts (randomization, comparisons, union genes)
│
├── external_tools/                # Third-party tools
│   ├── listminer/                 # ListMiner binary
│   └── clusterone/                # ClusterONE JAR
│
├── matlab/                        # MATLAB preprocessing scripts
├── notebooks/                     # Jupyter notebooks for analysis
├── docs/                          # Documentation
│
├── legacy/                        # Original code structure (preserved)
│   # (Use MIGRATION_GUIDE.md to populate this)
│
├── Analysis Code/                 # Original analysis scripts
├── Preprocessing Code/            # Original preprocessing scripts
├── Post Processing Code/          # Original post-processing scripts
├── Subgraph Code/                 # Original subgraph mining scripts
├── Purity Code/                   # Original purity calculation
├── ClusterOne/                    # ClusterONE files
├── FlyEnrichR Code/               # FlyEnrichr scripts
├── Funcassociate/                 # FuncAssociate scripts
├── Rest Genes/                    # Additional gene data
└── Keller codes/                  # Keller network MATLAB codes
```

## Pipeline Stages

| Stage | Directory | Purpose | Key Tools |
|-------|-----------|---------|-----------|
| 1 | `01_preprocessing` | Convert and prepare network data | Python, MATLAB |
| 2 | `02_mining` | Mine frequent subgraphs | ListMiner |
| 3 | `03_postprocessing` | Remap gene numbers and generate files | Python |
| 4 | `04_analysis` | Filter and remap components | Python |
| 5 | `05_utilities` | Calculate purity, extract GO terms, count subgraphs | Python |
| 6 | `06_validation` | Validate results through randomization and comparison | Python |

## Documentation

- **[PIPELINE.md](PIPELINE.md)** - Complete execution guide with all commands
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - How to migrate from old structure
- **[docs/DATA_FORMAT.md](docs/DATA_FORMAT.md)** - Input/output file format specifications
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[docs/PAPER_REPLICATION.md](docs/PAPER_REPLICATION.md)** - Replicating published results

## Key Features

- **Temporal Network Analysis**: Process time-series gene regulatory networks
- **Frequent Subgraph Mining**: Discover recurring patterns using ListMiner
- **Modular Pipeline**: Six well-defined stages with clear inputs/outputs
- **Flexible Configuration**: Parameter tuning for mining and clustering
- **Biological Validation**: GO enrichment analysis of discovered modules

## Data Requirements

The pipeline requires temporal gene regulatory networks with:
- Time-stamped interaction files
- Gene ID to symbol mappings
- Edge lists in tab-delimited format

See `data/raw/README.md` for detailed format specifications.

## Citation

If you use this pipeline, please cite the associated publication:

```
[Citation information to be added]
```

## Contributing

This repository is actively maintained. For issues or suggestions, please open a GitHub issue.

## License

[License information to be added]

## Acknowledgments

- Keller Lab for Drosophila embryogenesis network data
- ListMiner developers
- ClusterONE authors
- FlyEnrichr and FuncAssociate teams