#!/bin/bash
#
# run_all.sh
#
# Runs all preprocessing scripts for the periodic subgraph mining pipeline.
# This script handles data preparation and format conversion.
#

set -e  # Exit on error

echo "========================================="
echo "Stage 1: Data Preprocessing"
echo "========================================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Define paths relative to script location
DATA_RAW="../../data/raw"
DATA_PROCESSED="../../data/processed/timesteps"
DATA_MAPPINGS="../../data/mappings"

# Check if data exists
if [ ! -d "$DATA_RAW" ]; then
    echo "Error: Data directory not found: $DATA_RAW"
    echo "Please run setup_structure.sh first"
    exit 1
fi

echo ""
echo "Step 1: Checking for raw data..."
if [ -z "$(ls -A $DATA_RAW 2>/dev/null)" ]; then
    echo "Warning: No data found in $DATA_RAW"
    echo "Please place your raw network files there before running this script."
    echo ""
    echo "Expected files:"
    echo "  - Timestep files: timestep_01.txt, timestep_02.txt, ..."
    echo "  - OR MATLAB files: data/raw/keller_networks/*.mat"
    echo ""
    exit 1
fi

echo "Found data in $DATA_RAW"

# Create output directory if needed
mkdir -p "$DATA_PROCESSED"

echo ""
echo "Step 2: Processing Keller networks (if applicable)..."

# Check for MATLAB files
if ls $DATA_RAW/keller_networks/*.mat 1> /dev/null 2>&1; then
    echo "Found MATLAB files. Checking for MATLAB..."
    
    if command -v matlab &> /dev/null; then
        echo "MATLAB found. Processing Keller networks..."
        cd ../../"Keller codes" || cd ../../matlab
        matlab -nodisplay -r "try; keller; catch ME; disp(ME.message); end; exit"
        cd "$SCRIPT_DIR"
        echo "MATLAB processing complete."
    else
        echo "MATLAB not found. Skipping MATLAB processing."
        echo "To process .mat files, either:"
        echo "  1. Install MATLAB and rerun this script"
        echo "  2. Use Python script to convert .mat files"
        echo ""
    fi
else
    echo "No MATLAB files found. Skipping MATLAB processing."
fi

echo ""
echo "Step 3: Converting to standard format..."

# Check if we have preprocessed files or need to convert
if ls $DATA_PROCESSED/*.txt 1> /dev/null 2>&1; then
    echo "Preprocessed files already exist in $DATA_PROCESSED"
    FILE_COUNT=$(ls $DATA_PROCESSED/*.txt | wc -l)
    echo "Found $FILE_COUNT timestep files"
else
    echo "No preprocessed files found."
    
    # Check if raw text files exist
    if ls $DATA_RAW/*.txt 1> /dev/null 2>&1; then
        echo "Found raw text files. Copying to processed directory..."
        cp $DATA_RAW/*.txt "$DATA_PROCESSED/"
        echo "Files copied."
    else
        echo "No raw text files found."
        echo "Please ensure data is in correct format or run MATLAB preprocessing."
        exit 1
    fi
fi

echo ""
echo "Step 4: Validating network format..."

# Validate a sample file
SAMPLE_FILE=$(ls $DATA_PROCESSED/*.txt | head -1)
if [ -f "$SAMPLE_FILE" ]; then
    echo "Checking format of: $(basename $SAMPLE_FILE)"
    
    # Check number of columns
    NUM_COLS=$(head -1 "$SAMPLE_FILE" | awk '{print NF}')
    if [ "$NUM_COLS" -eq 2 ]; then
        echo "✓ Format valid: 2 columns (edge list)"
    else
        echo "✗ Warning: Expected 2 columns, found $NUM_COLS"
        echo "  First line: $(head -1 $SAMPLE_FILE)"
    fi
    
    # Count edges
    EDGE_COUNT=$(wc -l < "$SAMPLE_FILE")
    echo "  Edges: $EDGE_COUNT"
    
    # Show sample
    echo "  Sample edges:"
    head -3 "$SAMPLE_FILE" | sed 's/^/    /'
fi

echo ""
echo "Step 5: Checking mappings..."

if [ -f "$DATA_MAPPINGS/gene_id_mapping.txt" ]; then
    echo "✓ Gene ID mapping found"
    MAPPING_COUNT=$(wc -l < "$DATA_MAPPINGS/gene_id_mapping.txt")
    echo "  Mappings: $MAPPING_COUNT"
else
    echo "⚠ Warning: Gene ID mapping not found"
    echo "  You'll need this for Stage 4 (Analysis)"
    echo "  Place mapping file in: $DATA_MAPPINGS/gene_id_mapping.txt"
fi

if [ -f "$DATA_MAPPINGS/gene_name_mapping.txt" ]; then
    echo "✓ Gene name mapping found"
else
    echo "⚠ Warning: Gene name mapping not found"
    echo "  You'll need this for Stage 4 (Analysis)"
    echo "  Place mapping file in: $DATA_MAPPINGS/gene_name_mapping.txt"
fi

echo ""
echo "========================================="
echo "Preprocessing Summary"
echo "========================================="

TIMESTEP_COUNT=$(ls $DATA_PROCESSED/*.txt 2>/dev/null | wc -l)
echo "Timestep files: $TIMESTEP_COUNT"
echo "Output directory: $DATA_PROCESSED"
echo ""

if [ "$TIMESTEP_COUNT" -gt 0 ]; then
    echo "✓ Preprocessing complete!"
    echo ""
    echo "Next steps:"
    echo "1. Review preprocessed files in: $DATA_PROCESSED"
    echo "2. Proceed to Stage 2: Mining"
    echo "   cd ../02_mining"
    echo "   bash run_listminer.sh"
    echo ""
    echo "Or follow complete pipeline in: ../../PIPELINE.md"
else
    echo "✗ No preprocessed files generated"
    echo "Please check for errors above and ensure data is in correct location"
    exit 1
fi

echo "========================================="
