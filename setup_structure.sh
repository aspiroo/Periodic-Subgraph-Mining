#!/bin/bash
#
# setup_structure.sh
# 
# Creates the complete directory structure for the periodic subgraph mining pipeline.
# Run this script after cloning the repository to set up all necessary directories.
#

set -e  # Exit on error

echo "========================================="
echo "Setting up directory structure..."
echo "========================================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create data directories
echo "Creating data directories..."
mkdir -p data/raw/keller_networks
mkdir -p data/processed/timesteps
mkdir -p data/mappings
mkdir -p data/annotations

# Create results directories
echo "Creating results directories..."
mkdir -p results/listminer_output
mkdir -p results/components/individual
mkdir -p results/components/cleaned
mkdir -p results/components/remapped
mkdir -p results/components/gene_names
mkdir -p results/purity
mkdir -p results/clusters/individual
mkdir -p results/enrichment/flyenrichr
mkdir -p results/enrichment/funcassociate

# Create scripts directories (already exist with READMEs)
echo "Verifying scripts directories..."
mkdir -p scripts/01_preprocessing
mkdir -p scripts/02_mining
mkdir -p scripts/03_component_extraction
mkdir -p scripts/04_analysis
mkdir -p scripts/05_clustering
mkdir -p scripts/06_enrichment

# Create external tools directories
echo "Creating external tools directories..."
mkdir -p external_tools/listminer
mkdir -p external_tools/clusterone

# Create other directories
echo "Creating other directories..."
mkdir -p matlab
mkdir -p notebooks
mkdir -p docs
mkdir -p legacy

# Create .gitkeep files for important empty directories
echo "Creating .gitkeep files..."
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/mappings/.gitkeep
touch results/.gitkeep

# Set appropriate permissions
echo "Setting permissions..."
chmod -R u+rwX data/ results/ 2>/dev/null || true

echo ""
echo "========================================="
echo "Directory structure created successfully!"
echo "========================================="
echo ""
echo "Directory tree:"
echo ""
echo "data/"
echo "├── raw/"
echo "│   ├── keller_networks/"
echo "│   └── .gitkeep"
echo "├── processed/"
echo "│   ├── timesteps/"
echo "│   └── .gitkeep"
echo "├── mappings/"
echo "│   └── .gitkeep"
echo "└── annotations/"
echo ""
echo "results/"
echo "├── listminer_output/"
echo "├── components/"
echo "│   ├── individual/"
echo "│   ├── cleaned/"
echo "│   ├── remapped/"
echo "│   └── gene_names/"
echo "├── purity/"
echo "├── clusters/"
echo "│   └── individual/"
echo "└── enrichment/"
echo "    ├── flyenrichr/"
echo "    └── funcassociate/"
echo ""
echo "scripts/ (6 pipeline stages)"
echo "external_tools/ (ListMiner, ClusterONE)"
echo "matlab/ (MATLAB preprocessing)"
echo "notebooks/ (Jupyter notebooks)"
echo "docs/ (Documentation)"
echo "legacy/ (Original code)"
echo ""
echo "Next steps:"
echo "1. Place your data in data/raw/"
echo "2. Install ListMiner in external_tools/listminer/"
echo "3. Install ClusterONE in external_tools/clusterone/"
echo "4. Follow PIPELINE.md for execution instructions"
echo ""
echo "For more information, see README.md"
echo ""
