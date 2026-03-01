#!/bin/bash
set -e

echo "========================================="
echo "Stage 3: Post-processing"
echo "========================================="

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Step 1: Numbering gene files..."
python 01_number_gene_files.py

echo "Step 2: Extracting union genes..."
python 06_union_genes.py

echo "Step 3: Remapping edges to graph..."
python 02_remap_edges_to_graph.py

echo "Step 4: Remapping to gene numbers..."
python 03_remap_to_gene_numbers.py

echo "Step 5: Remapping to gene names..."
python 04_remap_to_gene_names.py

echo ""
echo "✅ Post-processing complete!"
echo "Results in: ../../results/components/gene_names/"