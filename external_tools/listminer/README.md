# ListMiner

Frequent subgraph mining tool for temporal networks.

## About ListMiner

ListMiner is a specialized tool for discovering frequent subgraphs in temporal/dynamic networks. It identifies patterns that appear repeatedly across multiple time points.

## Installation

### Option 1: Download Pre-compiled Binary

1. Download ListMiner from [source/website]
2. Place binary in this directory: `external_tools/listminer/listminer`
3. Make executable:
   ```bash
   chmod +x listminer
   ```

### Option 2: Compile from Source

If source code is available:

```bash
# Download source
wget [source_url] -O listminer_source.tar.gz
tar -xzf listminer_source.tar.gz
cd listminer_source

# Compile
make

# Copy binary
cp listminer ../listminer

# Test
../listminer --help
```

## Usage

### Basic Usage

```bash
./listminer -i <input_dir> -o <output_dir> -s <support> -min <min_size> -max <max_size>
```

### Parameters

- `-i`: Input directory containing timestep files
- `-o`: Output directory for results
- `-s`: Support threshold (minimum frequency)
- `-min`: Minimum subgraph size (nodes)
- `-max`: Maximum subgraph size (nodes)
- `-t`: Number of threads (optional)

### Example

```bash
./listminer \
    -i ../../data/processed/timesteps/ \
    -o ../../results/listminer_output/run_001/ \
    -s 3 \
    -min 3 \
    -max 6 \
    -t 4
```

## Input Format

Directory with timestep files:
```
timesteps/
├── timestep_01.txt
├── timestep_02.txt
└── ...
```

Each file contains edge list:
```
node1  node2
1      2
1      5
2      3
```

## Output Format

Creates directory with:
- `frequent_subgraphs.txt`: Discovered patterns
- `subgraph_list.txt`: Detailed subgraph information
- `statistics.txt`: Mining statistics

## Performance

**Runtime**: Depends on:
- Network size
- Support threshold (lower = slower)
- Subgraph size range
- Number of timesteps

**Typical**: 10 minutes to 2 hours

**Memory**: 2-8 GB recommended

## Tips

1. Start with high support (s=5) for quick testing
2. Use small size range (3-4) initially
3. Increase parallelism with `-t` flag
4. Monitor memory usage

## Troubleshooting

### Binary not found
```bash
chmod +x listminer
./listminer --help
```

### Permission denied
```bash
chmod +x listminer
```

### No patterns found
- Lower support threshold
- Check input format
- Verify timestep files exist

### Out of memory
- Increase system memory
- Reduce max subgraph size
- Increase support threshold

## Alternative Tools

If ListMiner is unavailable:
- **gSpan**: Frequent subgraph mining
- **FSG**: Fast Subgraph discovery
- **GREW**: Graph rewriting

## Documentation

For detailed documentation, see:
- Main pipeline: [PIPELINE.md](../../PIPELINE.md)
- Stage 2 guide: [scripts/02_mining/README.md](../../scripts/02_mining/README.md)

## Citation

If you use ListMiner, please cite:
```
[ListMiner citation to be added]
```

## Support

For ListMiner-specific issues:
- Check tool documentation
- Contact tool authors
- See [TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md)
