# Raw Data Directory

This directory contains the raw input data for the periodic subgraph mining pipeline.

## Required Files

### 1. Temporal Network Files

Network files representing gene regulatory interactions at different time points.

**Format**: Tab-separated edge list
```
gene1_id    gene2_id
1           2
1           5
2           3
```

**Naming Convention**: `timestep_XX.txt` or `network_timeXX.txt`

Place files in: `data/raw/timesteps/` or directly in `data/raw/`

### 2. Gene ID Mapping Files

**File**: `gene_id_mapping.txt`

Maps internal node IDs to FlyBase gene IDs.

**Format**:
```
node_id    flybase_id
1          FBgn0000001
2          FBgn0000002
```

Place in: `data/mappings/`

### 3. Gene Name Mapping Files

**File**: `gene_name_mapping.txt`

Maps FlyBase IDs to gene symbols.

**Format**:
```
flybase_id     gene_symbol
FBgn0000001    abl
FBgn0000002    ace
```

Place in: `data/mappings/`

## Keller Network Data

If using Keller lab networks:

1. The Keller `.mat` files are already present in `data/raw/keller_data/`
2. Run preprocessing scripts in `matlab/network_generation/`

## Data Sources

- **Keller Lab**: Drosophila embryogenesis networks
- **FlyBase**: Gene annotations and IDs
- **Your Data**: Custom temporal networks in compatible format

## File Size Considerations

Network files can be large (10s-100s of MB). They are excluded from git via `.gitignore`.

**Storage**: Keep raw data backed up separately from the repository.

## Validation

Before running the pipeline, verify:

```bash
# Check file format
head data/raw/timestep_01.txt

# Count edges per timestep
wc -l data/raw/*.txt

# Verify mappings exist
ls data/mappings/
```

## Example Data

For testing, you can create small synthetic networks:

```bash
# Generate test network
cat > data/raw/test_timestep_01.txt << EOF
1	2
2	3
3	4
1	4
EOF
```

## Next Steps

After placing data here:
1. Run preprocessing (Stage 1): `scripts/01_preprocessing/`
2. Follow [PIPELINE.md](../../PIPELINE.md) for complete instructions

## Need Help?

- Check [DATA_FORMAT.md](../../docs/DATA_FORMAT.md) for detailed format specifications
- See [TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md) for common data issues
