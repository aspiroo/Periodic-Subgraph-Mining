# Troubleshooting Guide

Common issues and solutions for the periodic subgraph mining pipeline.

## Table of Contents

1. [General Issues](#general-issues)
2. [Stage 1: Preprocessing](#stage-1-preprocessing)
3. [Stage 2: Mining](#stage-2-mining)
4. [Stage 3: Component Extraction](#stage-3-component-extraction)
5. [Stage 4: Analysis](#stage-4-analysis)
6. [Stage 5: Clustering](#stage-5-clustering)
7. [Stage 6: Enrichment](#stage-6-enrichment)
8. [Data Issues](#data-issues)
9. [Performance Issues](#performance-issues)

## General Issues

### Python ImportError

**Problem**: `ModuleNotFoundError: No module named 'X'`

**Solutions**:
```bash
# Install missing package
pip install <package_name>

# Install all dependencies
pip install -r requirements.txt

# Check Python version (need 3.x)
python --version

# Use pip3 if needed
pip3 install <package_name>
```

### Permission Denied

**Problem**: `Permission denied` when running scripts

**Solutions**:
```bash
# Make script executable
chmod +x script.py

# Or run with python
python script.py

# For bash scripts
chmod +x script.sh
./script.sh
```

### File Not Found

**Problem**: `No such file or directory`

**Solutions**:
```bash
# Check current directory
pwd

# Verify file exists
ls -l path/to/file

# Use absolute paths
python script.py --input /full/path/to/data

# Check relative path from script location
cd scripts/stage/
python script.py --input ../../data/
```

### Path Issues

**Problem**: Scripts can't find data files

**Solutions**:
```bash
# Always run from correct directory
cd /path/to/Periodic-Subgraph-Mining

# Or use absolute paths in scripts
INPUT=/home/user/Periodic-Subgraph-Mining/data/raw
python script.py --input $INPUT

# Check script expects correct structure
# Scripts in scripts/XX_stage/ expect ../../data/ and ../../results/
```

## Stage 1: Preprocessing

### MATLAB Not Found

**Problem**: `MATLAB: command not found`

**Solutions**:
1. Install MATLAB
2. Add MATLAB to PATH:
   ```bash
   export PATH="/path/to/matlab/bin:$PATH"
   ```
3. Use Python alternatives:
   ```python
   from scipy.io import loadmat
   data = loadmat('file.mat')
   ```

### MATLAB `.mat` File Load Error

**Problem**: Cannot load `.mat` file

**Solutions**:
```python
# Try with scipy
from scipy.io import loadmat
try:
    data = loadmat('file.mat')
except:
    # Try v7.3 format
    import h5py
    data = h5py.File('file.mat', 'r')
```

### Invalid Network Format

**Problem**: Preprocessing fails on network files

**Solutions**:
```bash
# Check file format
head data/raw/network.txt

# Should be tab-separated integers
# Correct: "1\t2"
# Wrong: "1 2" or "gene1\tgene2"

# Convert if needed
awk '{print $1"\t"$2}' input.txt > output.txt
```

### Empty Output Files

**Problem**: Preprocessed files are empty

**Solutions**:
1. Check input files exist and have content
2. Verify file paths in preprocessing script
3. Check for errors in MATLAB/Python output
4. Validate input format matches expected format

```bash
# Check input
ls -lh data/raw/
head data/raw/network.txt

# Check output
ls -lh data/processed/timesteps/
wc -l data/processed/timesteps/*.txt
```

## Stage 2: Mining

### ListMiner Not Found

**Problem**: `./listminer: No such file or directory`

**Solutions**:
```bash
# Check file exists
ls -l external_tools/listminer/listminer

# Make executable
chmod +x external_tools/listminer/listminer

# Verify it's a binary
file external_tools/listminer/listminer

# Download if missing (from source)
```

### ListMiner Permission Denied

**Problem**: `Permission denied: ./listminer`

**Solution**:
```bash
chmod +x external_tools/listminer/listminer
```

### No Patterns Found

**Problem**: ListMiner finds 0 frequent subgraphs

**Solutions**:
1. **Reduce support threshold**: Try `-s 2` instead of `-s 5`
2. **Check input files**:
   ```bash
   ls data/processed/timesteps/
   head data/processed/timesteps/timestep_01.txt
   ```
3. **Verify timestep count**: Need enough timesteps for given support
4. **Check network size**: Very small networks may have few patterns

### ListMiner Out of Memory

**Problem**: `Out of memory` or killed during mining

**Solutions**:
1. **Increase support threshold**: `-s 5` instead of `-s 2`
2. **Reduce max subgraph size**: `-max 4` instead of `-max 8`
3. **Process fewer timesteps**: Split into batches
4. **Add more RAM**: Mining can be memory-intensive
5. **Free memory**:
   ```bash
   # Close other applications
   # Clear cache
   sync; echo 3 > /proc/sys/vm/drop_caches  # Linux, as root
   ```

### ListMiner Very Slow

**Problem**: Mining takes extremely long (>6 hours)

**Solutions**:
1. **Increase support**: Higher support = faster
2. **Reduce size range**: Smaller max size = faster
3. **Test with subset**: Try with fewer timesteps first
4. **Use parallelization**: If tool supports threading
5. **Optimize input**: Remove duplicate edges, sort files

## Stage 3: Component Extraction

### No Components Extracted

**Problem**: Component extraction produces no output

**Solutions**:
```bash
# Check ListMiner output exists
ls results/listminer_output/*/

# Check format of mining output
head results/listminer_output/*/frequent_subgraphs.txt

# Run with verbose output
python subgraph_count.py --input ... --output ... --verbose
```

### Too Many Small Components

**Problem**: Thousands of tiny (2-3 node) components

**Solutions**:
```bash
# Filter by minimum size
python subgraph_count.py \
    --input ... \
    --output ... \
    --min-nodes 4

# Or filter after extraction
python filter_components.py \
    --input results/components/individual/ \
    --output results/components/filtered/ \
    --min-size 4
```

### Memory Error During Extraction

**Problem**: Out of memory while extracting components

**Solutions**:
1. Process in batches
2. Increase available memory
3. Filter during extraction (set min-size)
4. Clear intermediate results

## Stage 4: Analysis

### Remapping Fails

**Problem**: Cannot remap node IDs to gene IDs

**Solutions**:
```bash
# Check mapping file exists
ls data/mappings/gene_id_mapping.txt

# Verify format (tab-separated, header)
head data/mappings/gene_id_mapping.txt

# Should be:
# NodeID    GeneID
# 1         FBgn0000001
# 2         FBgn0000008

# Check all node IDs have mappings
python check_mappings.py \
    --components results/components/cleaned/ \
    --mapping data/mappings/gene_id_mapping.txt
```

### Missing Gene Names

**Problem**: Some genes don't get gene symbols

**Solutions**:
1. **Check mapping file**: Ensure all FlyBase IDs have symbols
2. **Update mappings**: Download latest from FlyBase
3. **Use IDs as fallback**: Keep FlyBase IDs if symbols missing
4. **Partial mapping is OK**: Some genes may lack standard symbols

```bash
# Count unmapped genes
grep -c "FBgn" results/components/gene_names/*.txt

# Use partial mapping
python remappingGeneNames.py \
    --input ... \
    --output ... \
    --keep-unmapped  # Keep FBgn IDs if no symbol
```

### Duplicate Components

**Problem**: Many identical or nearly identical components

**Solutions**:
```bash
# Run deduplication
python deduplicate_components.py \
    --input results/components/cleaned/ \
    --output results/components/unique/

# Or use filtering script
python filtering.py \
    --input ... \
    --output ... \
    --remove-duplicates
```

### Low Purity Scores

**Problem**: All components have purity < 0.5

**Solutions**:
1. **Expected for some datasets**: Not all components are biologically coherent
2. **Filter high purity**:
   ```bash
   python filter_by_purity.py --threshold 0.6
   ```
3. **Review mining parameters**: Too low support may yield noise
4. **Check GO annotations**: Ensure annotation file is current

## Stage 5: Clustering

### Java Not Found

**Problem**: `java: command not found`

**Solutions**:
```bash
# Install Java (Ubuntu/Debian)
sudo apt-get install openjdk-11-jre

# Install Java (macOS)
brew install openjdk@11

# Check Java version
java -version

# Should be 8 or higher
```

### ClusterONE JAR Not Found

**Problem**: Cannot find cluster_one-1.0.jar

**Solutions**:
```bash
# Check file exists
ls external_tools/clusterone/cluster_one-1.0.jar

# Download if missing
wget http://www.paccanarolab.org/static_content/clusterone/cluster_one-1.0.jar

# Move to correct location
mv cluster_one-1.0.jar external_tools/clusterone/
```

### No Clusters Found

**Problem**: ClusterONE produces empty output

**Solutions**:
1. **Check input network**:
   ```bash
   wc -l results/clusters/union_network.txt
   # Should have edges
   ```
2. **Reduce minimum size**: `-s 2`
3. **Reduce density**: `-d 0.2`
4. **Check network connectivity**:
   ```bash
   # Count nodes
   awk '{print $1"\n"$2}' union_network.txt | sort -u | wc -l
   ```

### Java Heap Space Error

**Problem**: `java.lang.OutOfMemoryError: Java heap space`

**Solutions**:
```bash
# Increase heap size
java -Xmx4G -jar cluster_one-1.0.jar ...

# For very large networks
java -Xmx8G -jar cluster_one-1.0.jar ...

# Check available RAM
free -h  # Linux
vm_stat  # macOS
```

### Too Many Overlapping Clusters

**Problem**: Excessive cluster overlap

**Solutions**:
```bash
# Increase overlap threshold
java -jar cluster_one-1.0.jar input.txt --overlap-threshold 0.9

# Increase density
java -jar cluster_one-1.0.jar input.txt -d 0.5

# Increase penalty
java -jar cluster_one-1.0.jar input.txt --penalty 3.0
```

## Stage 6: Enrichment

### API Rate Limiting

**Problem**: FlyEnrichr API limits requests

**Solutions**:
```bash
# Add delays between requests
python batch_enrichr.py \
    --input ... \
    --output ... \
    --delay 2  # 2 seconds between requests

# Process in smaller batches
python batch_enrichr.py --batch-size 5

# Use local enrichment tools if available
```

### No Enrichment Found

**Problem**: No significant GO terms

**Solutions**:
1. **Check gene names**: Must be valid Drosophila gene symbols
2. **Verify species**: FlyEnrichr is Drosophila-specific
3. **Check cluster size**: Need ≥3 genes typically
4. **Try different libraries**:
   ```python
   libraries = [
       'GO_Biological_Process_2018',
       'KEGG_2019_Fly',
       'WikiPathways_2019'
   ]
   ```
5. **Lower p-value threshold**: Try p < 0.1

### Invalid Gene Names

**Problem**: Gene names not recognized

**Solutions**:
```bash
# Check gene name format
head results/clusters/individual/cluster_001.txt

# Should be symbols like: abl, ace, Acon
# Not IDs like: FBgn0000001

# Verify remapping completed
ls results/components/gene_names/

# Validate gene names against FlyBase
python validate_gene_names.py --input cluster_001.txt
```

### Connection Errors

**Problem**: Cannot connect to enrichment service

**Solutions**:
1. **Check internet**: `ping google.com`
2. **Try alternative service**: Use FuncAssociate
3. **Use local tools**: Download GO annotations
4. **Retry with backoff**:
   ```python
   import time
   for attempt in range(3):
       try:
           result = enrichr_query(genes)
           break
       except:
           time.sleep(5 * (attempt + 1))
   ```

## Data Issues

### Inconsistent Gene IDs

**Problem**: Gene IDs don't match between files

**Solutions**:
1. **Check ID format**: All should be FBgn######
2. **Update mappings**: Use same FlyBase release throughout
3. **Standardize IDs**: Convert all to same version
4. **Check for typos**: Validate ID format

### Missing Timesteps

**Problem**: Some timesteps missing or empty

**Solutions**:
```bash
# Check all timesteps
ls -lh data/processed/timesteps/

# Find empty files
find data/processed/timesteps/ -size 0

# List files with edge counts
wc -l data/processed/timesteps/*.txt | sort -n
```

### Encoding Issues

**Problem**: Strange characters or encoding errors

**Solutions**:
```bash
# Check encoding
file -i data/file.txt

# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt

# Remove BOM if present
sed '1s/^\xEF\xBB\xBF//' input.txt > output.txt
```

## Performance Issues

### Pipeline Too Slow

**Solutions**:
1. **Parallelize**: Run independent stages in parallel
2. **Optimize parameters**: Higher support, smaller size ranges
3. **Use subsets**: Test with smaller dataset first
4. **Upgrade hardware**: More RAM, faster CPU
5. **Profile code**: Find bottlenecks

```bash
# Run stages in parallel (if independent)
python stage1.py --input data1 &
python stage1.py --input data2 &
wait

# Use GNU parallel
ls data/*.txt | parallel python process.py --input {}
```

### Disk Space Issues

**Problem**: Running out of disk space

**Solutions**:
```bash
# Check disk usage
df -h
du -sh results/*

# Clean intermediate files
rm -rf results/listminer_output/temp/
rm -rf results/components/individual/*.bak

# Compress large files
gzip results/large_file.txt

# Move results to external storage
mv results/ /external/drive/
ln -s /external/drive/results results
```

### Memory Leaks

**Problem**: Memory usage grows over time

**Solutions**:
1. **Process in batches**: Clear memory between batches
2. **Use generators**: Instead of loading all data
3. **Explicitly free memory**:
   ```python
   import gc
   del large_object
   gc.collect()
   ```
4. **Monitor memory**:
   ```bash
   top
   htop
   # Watch for growing processes
   ```

## Getting More Help

If these solutions don't help:

1. **Check documentation**:
   - [PIPELINE.md](../PIPELINE.md)
   - [DATA_FORMAT.md](DATA_FORMAT.md)
   - Stage-specific READMEs

2. **Search issues**: Check GitHub issues for similar problems

3. **Enable verbose output**: Run with `--verbose` or `--debug` flags

4. **Create minimal example**: Isolate the problem with small test case

5. **Open GitHub issue**: Include:
   - Error message (full traceback)
   - Command you ran
   - Input file format (first few lines)
   - System info (OS, Python version, etc.)

## Debugging Tips

### Enable Verbose Output

```bash
# Python scripts
python script.py --verbose
python script.py --debug

# Bash scripts
bash -x script.sh
```

### Check Exit Codes

```bash
# Run command
python script.py
echo $?  # 0 = success, non-zero = error
```

### Log Output

```bash
# Save output to file
python script.py 2>&1 | tee logfile.txt

# Separate stdout and stderr
python script.py >stdout.log 2>stderr.log
```

### Validate at Each Stage

```bash
# After each stage, verify output
ls -lh results/stage_output/
head results/stage_output/file.txt
wc -l results/stage_output/*.txt
```

### Use Small Test Dataset

```bash
# Create small test set
head -100 data/raw/network.txt > data/raw/test_network.txt

# Run pipeline on test
python script.py --input data/raw/test_network.txt
```

## Prevention

**Best Practices**:
1. **Validate input**: Check formats before processing
2. **Test small**: Run on small dataset first
3. **Document**: Keep notes on what works
4. **Backup**: Backup data before processing
5. **Version control**: Track pipeline parameters
6. **Monitor**: Watch resource usage during runs

---

**Still having issues?** Open a GitHub issue with detailed information.
