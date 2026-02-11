# Stage 5: Clustering

Scripts for clustering components into functional modules using ClusterONE.

## Overview

This stage clusters individual components into larger functional modules:
- Combines components into a union network
- Runs ClusterONE clustering algorithm
- Identifies overlapping protein complexes/modules
- Exports clusters for enrichment analysis

## Tools

### ClusterONE

**Description**: Graph clustering algorithm designed for detecting overlapping protein complexes.

**Location**: `external_tools/clusterone/`

**Installation**: See [external_tools/clusterone/README.md](../../external_tools/clusterone/README.md)

### Cytoscape (Optional)

Visual network analysis and clustering validation.

## Scripts

- **run_clusterone.sh** - Automated ClusterONE execution
- **prepare_network.py** - Format network for clustering
- **process_clusters.py** - Parse and split cluster output
- **analyze_clusters.py** - Generate cluster statistics

## Usage

### Step 1: Prepare Union Network

Create a combined network from all components:

```bash
cd scripts/05_clustering

# Combine components (done in Stage 4)
# Union network should be at: ../../results/clusters/union_network.txt
```

### Step 2: Run ClusterONE

```bash
# Basic clustering
java -jar ../../external_tools/clusterone/cluster_one-1.0.jar \
    ../../results/clusters/union_network.txt \
    > ../../results/clusters/clusters.txt

# With parameters
java -jar ../../external_tools/clusterone/cluster_one-1.0.jar \
    ../../results/clusters/union_network.txt \
    -s 3 \
    -d 0.3 \
    > ../../results/clusters/clusters.txt
```

### Step 3: Process Clusters

```bash
# Split clusters into individual files
python process_clusters.py \
    --input ../../results/clusters/clusters.txt \
    --output ../../results/clusters/individual/
```

### Using Cytoscape (Optional)

1. Open Cytoscape
2. Import union network: `File > Import > Network from File`
3. Select network file: `results/clusters/union_network.txt`
4. Install ClusterONE plugin: `Apps > App Manager`
5. Run clustering: `Apps > ClusterONE > Start`
6. Adjust parameters in ClusterONE panel
7. Export results: `File > Export > Table to File`

## Parameters

### ClusterONE Parameters

- `-s, --min-size`: Minimum cluster size (default: 3)
  - Smaller: More clusters, including small ones
  - Larger: Fewer, larger clusters only

- `-d, --min-density`: Minimum density (default: auto)
  - Lower (0.2-0.4): Looser clusters
  - Higher (0.5-0.8): Tighter clusters

- `--overlap-threshold`: Node overlap threshold (default: 0.8)
  - Controls how much clusters can overlap

- `--penalty`: Penalty for adding nodes (default: 2.0)
  - Higher: Smaller, denser clusters
  - Lower: Larger, looser clusters

### Recommended Settings

```bash
# Balanced (recommended for most cases)
java -jar cluster_one-1.0.jar network.txt -s 3 -d 0.3

# Tight clusters (high confidence)
java -jar cluster_one-1.0.jar network.txt -s 4 -d 0.5

# Permissive (discover more clusters)
java -jar cluster_one-1.0.jar network.txt -s 2 -d 0.2
```

## Input Format

**File**: Union network in edge list format

```
gene1  gene2  [weight]
abl    ace
abl    Acon
ace    Acon
```

Weights are optional (default: 1.0 for all edges).

## Output Format

### Clusters File

Each line represents a cluster:
```
cluster_id: gene1 gene2 gene3 ... (p-value quality_score)
```

Example:
```
1: abl ace Acon arr brk (0.001 0.85)
2: btn bun CG1234 CG5678 (0.01 0.72)
```

### Individual Cluster Files

After processing:
```
results/clusters/individual/
├── cluster_001.txt
├── cluster_002.txt
└── ...
```

Each file contains genes in that cluster (one per line).

## Validation

### Check Clustering Results

```bash
# Count clusters
wc -l ../../results/clusters/clusters.txt

# View cluster sizes
python analyze_clusters.py \
    --input ../../results/clusters/individual/ \
    --output cluster_stats.txt

# Visualize cluster sizes
python plot_cluster_sizes.py \
    --input cluster_stats.txt \
    --output cluster_distribution.png
```

### Quality Metrics

- **Number of clusters**: 10-100 typical
- **Cluster sizes**: 3-50 genes typical
- **Overlap**: Some overlap expected (biological reality)
- **Quality scores**: >0.5 considered good

## Advanced Usage

### Multiple Runs with Different Parameters

```bash
# Test different settings
for min_size in 3 4 5; do
    for density in 0.2 0.3 0.4; do
        java -jar cluster_one-1.0.jar network.txt \
            -s $min_size -d $density \
            > clusters_s${min_size}_d${density}.txt
    done
done
```

### Compare Clustering Results

```bash
# Compare different parameter sets
python compare_clusterings.py \
    --input1 clusters_s3_d0.3.txt \
    --input2 clusters_s4_d0.5.txt \
    --output comparison_report.txt
```

### Merge Similar Clusters

```bash
# Merge highly overlapping clusters
python merge_clusters.py \
    --input ../../results/clusters/individual/ \
    --output ../../results/clusters/merged/ \
    --similarity 0.8
```

## Troubleshooting

### Issue: No clusters found

- Check input network is not empty
- Reduce minimum size (`-s 2`)
- Reduce density threshold (`-d 0.1`)

### Issue: Too many clusters

- Increase minimum size
- Increase density threshold
- Increase penalty parameter

### Issue: Java heap space error

```bash
# Increase Java memory
java -Xmx4G -jar cluster_one-1.0.jar network.txt
```

### Issue: Poor quality clusters

- Adjust density threshold
- Filter union network before clustering
- Review component extraction/filtering

For more help, see [docs/TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md).

## Cluster Interpretation

Good clusters should:
- Contain functionally related genes
- Show enrichment for GO terms (Stage 6)
- Have literature support
- Make biological sense

## Next Stage

After clustering:
- Proceed to **Stage 6: Enrichment** in `scripts/06_enrichment/`
- See [PIPELINE.md](../../PIPELINE.md) for next steps
