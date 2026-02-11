# ClusterONE

Clustering with Overlapping Neighborhood Expansion.

## About ClusterONE

ClusterONE is a graph clustering algorithm designed for detecting potentially overlapping protein complexes from protein-protein interaction networks.

**Key Features**:
- Detects overlapping clusters
- Optimized for biological networks
- Fast and scalable
- Quality scoring for clusters

## Installation

### Option 1: Download Pre-built JAR

```bash
# Download from official source
wget http://www.paccanarolab.org/static_content/clusterone/cluster_one-1.0.jar

# Or if available elsewhere
cp /path/to/cluster_one-1.0.jar .
```

### Option 2: From Maven Central

```bash
# Download using Maven
mvn dependency:get \
    -DgroupId=uk.ac.rhul.cs \
    -DartifactId=clusterone \
    -Dversion=1.0
```

## Usage

### Basic Usage

```bash
java -jar cluster_one-1.0.jar <input_file> [options]
```

### Common Options

- `-s, --min-size <int>`: Minimum cluster size (default: 3)
- `-d, --min-density <float>`: Minimum density (default: auto)
- `-o, --output <file>`: Output file
- `--overlap-threshold <float>`: Overlap threshold (default: 0.8)
- `--penalty <float>`: Penalty value (default: 2.0)
- `-h, --help`: Show help

### Example

```bash
java -jar cluster_one-1.0.jar \
    ../../results/clusters/union_network.txt \
    -s 3 \
    -d 0.3 \
    > ../../results/clusters/clusters.txt
```

### With More Memory

```bash
java -Xmx4G -jar cluster_one-1.0.jar input.txt -s 3
```

## Input Format

Edge list (tab or space separated):
```
gene1  gene2  [weight]
abl    ace
ace    Acon
bun    btn
```

Weights are optional (default: 1.0).

## Output Format

Each line is a cluster:
```
cluster_id: gene1 gene2 gene3 ... (p-value quality_score)
```

Example:
```
1: abl ace Acon arr (0.001 0.85)
2: btn bun CG1234 (0.01 0.72)
```

## Parameter Tuning

### Minimum Size (`-s`)
- **Small (2-3)**: Discover small modules
- **Medium (4-5)**: Balanced
- **Large (6+)**: Only large complexes

### Minimum Density (`-d`)
- **Low (0.1-0.3)**: Looser clusters
- **Medium (0.3-0.5)**: Balanced (recommended)
- **High (0.5-0.8)**: Very tight clusters

### Overlap Threshold
- Controls how much clusters can share nodes
- **Low (0.5-0.7)**: More overlap allowed
- **High (0.8-0.9)**: Less overlap

## Quality Scores

ClusterONE reports quality for each cluster:
- **>0.7**: High quality
- **0.5-0.7**: Good quality
- **0.3-0.5**: Moderate quality
- **<0.3**: Low quality (consider filtering)

## Cytoscape Plugin

ClusterONE is also available as a Cytoscape plugin:

1. Install Cytoscape: https://cytoscape.org/
2. Go to: Apps → App Manager
3. Search for "ClusterONE"
4. Install and restart Cytoscape
5. Import your network
6. Run: Apps → ClusterONE → Start

### Advantages of Cytoscape Plugin
- Visual interface
- Interactive parameter tuning
- Real-time cluster visualization
- Export options

## Performance

**Runtime**: Usually fast (seconds to minutes)
- Depends on network size
- Scalable to large networks (10,000+ nodes)

**Memory**: Adjust Java heap if needed:
```bash
java -Xmx2G -jar cluster_one-1.0.jar ...
```

## Troubleshooting

### Java not found
```bash
# Install Java 8+
sudo apt-get install openjdk-11-jre  # Ubuntu/Debian
brew install openjdk@11              # macOS
```

### Heap space error
```bash
java -Xmx8G -jar cluster_one-1.0.jar ...
```

### No clusters found
- Lower minimum density: `-d 0.2`
- Lower minimum size: `-s 2`
- Check input file format

### Too many overlapping clusters
- Increase overlap threshold: `--overlap-threshold 0.9`
- Increase penalty: `--penalty 3.0`

## Comparison with Other Tools

| Tool | Overlapping | Speed | Quality |
|------|-------------|-------|---------|
| ClusterONE | Yes | Fast | High |
| MCL | No | Fast | Good |
| MCODE | No | Fast | Moderate |
| CFinder | Yes | Slow | High |

## Documentation

- **Official**: http://www.paccanarolab.org/cluster-one/
- **Paper**: Nepusz et al., Nature Methods, 2012
- **Pipeline**: [scripts/05_clustering/README.md](../../scripts/05_clustering/README.md)

## Citation

If you use ClusterONE, please cite:

```
Nepusz, T., Yu, H., & Paccanaro, A. (2012).
Detecting overlapping protein complexes in protein-protein interaction networks.
Nature Methods, 9(5), 471-472.
```

## Alternative Clustering Tools

- **MCL** (Markov Clustering): Fast, no overlap
- **MCODE**: Cytoscape plugin
- **CFinder**: k-clique percolation
- **DPClus**: Density-periphery based

## Support

- Official docs: http://www.paccanarolab.org/cluster-one/
- GitHub issues (if available)
- See [TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md)
