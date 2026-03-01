#!/bin/bash
#
# run_listminer.sh
#
# Runs ListMiner with multiple parameter combinations for periodic subgraph mining.
# Explores different support thresholds and subgraph size ranges.
#

set -e  # Exit on error

echo "========================================="
echo "Stage 2: Subgraph Mining with ListMiner"
echo "========================================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Define paths
LISTMINER="../../external_tools/listminer/listminer"
INPUT_FILE="../../data/processed/listMinerInputs.txt"
OUTPUT_BASE="../../results/listminer_output"

# Check if ListMiner exists
if [ ! -f "$LISTMINER" ]; then
    echo "Error: ListMiner not found at: $LISTMINER"
    echo ""
    echo "Please install ListMiner:"
    echo "1. Download or compile ListMiner"
    echo "2. Place binary at: $LISTMINER"
    echo "3. Make executable: chmod +x $LISTMINER"
    echo ""
    echo "See: ../../external_tools/listminer/README.md"
    exit 1
fi

# Check if executable
if [ ! -x "$LISTMINER" ]; then
    echo "Making ListMiner executable..."
    chmod +x "$LISTMINER"
fi

# Check if input data exists
if [ ! -d "$INPUT_DIR" ] || [ -z "$(ls -A $INPUT_DIR 2>/dev/null)" ]; then
    echo "Error: No input data found in: $INPUT_DIR"
    echo ""
    echo "Please run Stage 1 preprocessing first:"
    echo "  cd ../01_preprocessing"
    echo "  bash run_all.sh"
    echo ""
    exit 1
fi

# Count input files
TIMESTEP_COUNT=$(ls $INPUT_DIR/*.txt 2>/dev/null | wc -l)
echo "Input directory: $INPUT_DIR"
echo "Timestep files: $TIMESTEP_COUNT"

if [ "$TIMESTEP_COUNT" -lt 2 ]; then
    echo "Error: Need at least 2 timestep files for mining"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_BASE"

echo ""
echo "ListMiner executable: $LISTMINER"
echo "Output directory: $OUTPUT_BASE"
echo ""

# Parse command line arguments for custom parameters
CUSTOM_SUPPORT=""
CUSTOM_MIN_SIZE=""
CUSTOM_MAX_SIZE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --support)
            CUSTOM_SUPPORT="$2"
            shift 2
            ;;
        --min-size)
            CUSTOM_MIN_SIZE="$2"
            shift 2
            ;;
        --max-size)
            CUSTOM_MAX_SIZE="$2"
            shift 2
            ;;
        --test)
            echo "Running in test mode (single quick run)..."
            TEST_MODE=1
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --support N      Support threshold (default: run multiple values)"
            echo "  --min-size N     Minimum subgraph size (default: 3)"
            echo "  --max-size N     Maximum subgraph size (default: 6)"
            echo "  --test           Quick test run (support=5, size=3-4)"
            echo "  --help           Show this help"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Define parameter combinations
if [ -n "$TEST_MODE" ]; then
    echo "========================================="
    echo "TEST MODE: Quick run"
    echo "========================================="
    SUPPORT_VALUES=(5)
    MIN_SIZE=3
    MAX_SIZE=4
elif [ -n "$CUSTOM_SUPPORT" ]; then
    # Single run with custom parameters
    SUPPORT_VALUES=($CUSTOM_SUPPORT)
    MIN_SIZE=${CUSTOM_MIN_SIZE:-3}
    MAX_SIZE=${CUSTOM_MAX_SIZE:-6}
else
    # Multiple parameter combinations
    SUPPORT_VALUES=(3 4 5)
    MIN_SIZE=3
    MAX_SIZE=6
fi

echo "Parameter settings:"
echo "  Support values: ${SUPPORT_VALUES[@]}"
echo "  Subgraph size: $MIN_SIZE to $MAX_SIZE nodes"
echo ""

# Run ListMiner for each parameter combination
RUN_COUNT=0
SUCCESS_COUNT=0

for SUPPORT in "${SUPPORT_VALUES[@]}"; do
    RUN_COUNT=$((RUN_COUNT + 1))
    
    # Create output directory for this run
    OUTPUT_DIR="$OUTPUT_BASE/support_${SUPPORT}_size_${MIN_SIZE}-${MAX_SIZE}"
    mkdir -p "$OUTPUT_DIR"
    
    echo "========================================="
    echo "Run $RUN_COUNT: Support=$SUPPORT, Size=$MIN_SIZE-$MAX_SIZE"
    echo "========================================="
    echo "Output: $OUTPUT_DIR"
    echo ""
    echo "Starting ListMiner..."
    echo "This may take 10 minutes to several hours depending on data size."
    echo ""
    
    # Record start time
    START_TIME=$(date +%s)
    
    # Run ListMiner
    if $LISTMINER \
        -i "$INPUT_FILE" \
        -o "$OUTPUT_DIR" \
        -s "$SUPPORT"; then
        
        # Record end time
        END_TIME=$(date +%s)
        DURATION=$((END_TIME - START_TIME))
        MINUTES=$((DURATION / 60))
        SECONDS=$((DURATION % 60))
        
        echo ""
        echo "✓ Mining complete! (${MINUTES}m ${SECONDS}s)"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        
        # Check output
        if [ -f "$OUTPUT_DIR/frequent_subgraphs.txt" ]; then
            SUBGRAPH_COUNT=$(wc -l < "$OUTPUT_DIR/frequent_subgraphs.txt" || echo 0)
            echo "  Frequent subgraphs found: $SUBGRAPH_COUNT"
        else
            echo "  Warning: Output file not found"
        fi
    else
        echo ""
        echo "✗ Mining failed for support=$SUPPORT"
        echo "  Check error messages above"
    fi
    
    echo ""
done

# Summary
echo "========================================="
echo "Mining Summary"
echo "========================================="
echo "Runs completed: $SUCCESS_COUNT / $RUN_COUNT"
echo "Output directory: $OUTPUT_BASE"
echo ""

if [ "$SUCCESS_COUNT" -gt 0 ]; then
    echo "Results:"
    for SUPPORT in "${SUPPORT_VALUES[@]}"; do
        OUTPUT_DIR="$OUTPUT_BASE/support_${SUPPORT}_size_${MIN_SIZE}-${MAX_SIZE}"
        if [ -f "$OUTPUT_DIR/frequent_subgraphs.txt" ]; then
            COUNT=$(wc -l < "$OUTPUT_DIR/frequent_subgraphs.txt" || echo 0)
            echo "  Support $SUPPORT: $COUNT subgraphs"
        fi
    done
    echo ""
    echo "✓ Mining complete!"
    echo ""
    echo "Next steps:"
    echo "1. Review mining results in: $OUTPUT_BASE"
    echo "2. Proceed to Stage 3: Component Extraction"
    echo "   cd ../03_component_extraction"
    echo ""
    echo "Or follow complete pipeline in: ../../PIPELINE.md"
else
    echo "✗ All mining runs failed"
    echo "Please check:"
    echo "  1. ListMiner binary is correct version"
    echo "  2. Input files are in correct format"
    echo "  3. Sufficient memory available"
    echo ""
    echo "See: ../../docs/TROUBLESHOOTING.md"
    exit 1
fi

echo "========================================="
