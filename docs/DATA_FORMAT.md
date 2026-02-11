# Data Format Specifications

Complete specifications for all file formats used in the periodic subgraph mining pipeline.

## Table of Contents

1. [Input Data Formats](#input-data-formats)
2. [Intermediate Formats](#intermediate-formats)
3. [Output Formats](#output-formats)
4. [Mapping Files](#mapping-files)

## Input Data Formats

### Temporal Network Files

**Purpose**: Raw time-series network data

**Location**: `data/raw/` or `data/raw/timesteps/`

**Format**: Tab-separated or space-separated edge list

**Structure**:
```
node1  node2  [weight]  [timestamp]
```

**Example**:
```
1	2
1	5
2	3
3	4
1	4
```

**Specifications**:
- One edge per line
- Node IDs: integers or strings
- Weight: optional, float (default: 1.0)
- Timestamp: optional, for single-file temporal networks
- Delimiter: tab or space
- No header row

**File Naming**:
- Single file: `network.txt`
- Per-timestep: `timestep_01.txt`, `timestep_02.txt`, ...
- Alternative: `network_t01.txt`, `network_t02.txt`, ...

**Validation**:
```bash
# Check format
head -5 data/raw/timestep_01.txt

# Verify two columns
awk '{print NF}' data/raw/timestep_01.txt | sort -u

# Count edges
wc -l data/raw/*.txt
```

### MATLAB Network Files

**Purpose**: Keller lab network data

**Location**: `data/raw/keller_networks/`

**Format**: MATLAB `.mat` file

**Required Variables**:
- `adjacency` or `adj_matrix`: Adjacency matrix (N×N sparse or full)
- `timestamps` or `time`: Time point labels
- `gene_ids` (optional): Gene identifiers

**Example**:
```matlab
% Load file
data = load('keller_network.mat');

% Expected structure
data.adjacency     % N×N matrix
data.timestamps    % 1×T vector
data.gene_ids      % N×1 cell array
```

## Intermediate Formats

### Preprocessed Networks

**Purpose**: Cleaned networks ready for mining

**Location**: `data/processed/timesteps/`

**Format**: Tab-separated edge list (integer node IDs)

**Structure**:
```
1	2
1	5
2	3
```

**Specifications**:
- Integer node IDs only (1, 2, 3, ...)
- Tab-separated
- No weights or attributes
- One file per timestep
- Sorted by first column, then second

### ListMiner Output

**Purpose**: Discovered frequent subgraphs

**Location**: `results/listminer_output/*/`

**Format**: Tool-specific format

**Main Files**:
1. `frequent_subgraphs.txt`: List of discovered patterns
2. `subgraph_list.txt`: Detailed subgraph information
3. `statistics.txt`: Mining statistics

**Example** (`frequent_subgraphs.txt`):
```
SubgraphID: 1
Support: 5
Nodes: 1 2 3 4
Edges: 1-2 2-3 3-4 1-4
Timesteps: 1,3,5,7,9

SubgraphID: 2
Support: 4
Nodes: 5 6 7
Edges: 5-6 6-7
Timesteps: 2,4,6,8
```

### Extracted Components

**Purpose**: Individual connected components

**Location**: `results/components/individual/`

**Format**: Edge list (one component per file)

**Example** (`component_001.txt`):
```
1	2
2	3
3	4
1	4
```

**Naming**: `component_XXX.txt` (zero-padded numbers)

**Specifications**:
- Each file is one connected component
- Nodes are contiguous integers
- Sorted edges

### Cleaned Components

**Purpose**: Filtered, deduplicated components

**Location**: `results/components/cleaned/`

**Format**: Same as extracted components

**Differences from raw components**:
- Duplicates removed
- Size filtered (min/max nodes)
- Quality filtered (if purity calculated)

### Remapped Components (Gene IDs)

**Purpose**: Components with gene IDs instead of node numbers

**Location**: `results/components/remapped/`

**Format**: Edge list with gene IDs

**Example** (`component_001.txt`):
```
FBgn0000001	FBgn0000008
FBgn0000008	FBgn0000014
FBgn0000014	FBgn0000017
```

**Specifications**:
- Gene IDs from FlyBase
- Format: `FBgn` followed by numbers
- Tab-separated
- One edge per line

### Remapped Components (Gene Names)

**Purpose**: Components with gene symbols

**Location**: `results/components/gene_names/`

**Format**: Edge list with gene symbols

**Example** (`component_001.txt`):
```
abl	ace
ace	Acon
Acon	arr
```

**Specifications**:
- Gene symbols (human-readable)
- Case-sensitive
- Tab-separated

## Output Formats

### Purity Scores

**Purpose**: Biological coherence metrics

**Location**: `results/purity/`

**Format**: Tab-separated values

**Example** (`purity_scores.txt`):
```
ComponentID	PurityScore	NumGenes	GOTerm	Pvalue
component_001	0.85	4	cell cycle	0.001
component_002	0.72	5	development	0.005
component_003	0.43	3	metabolic	0.12
```

**Columns**:
1. `ComponentID`: Component file name
2. `PurityScore`: 0-1 score (higher = more coherent)
3. `NumGenes`: Number of genes in component
4. `GOTerm`: Most enriched GO term
5. `Pvalue`: Significance of enrichment

### Union Network

**Purpose**: Combined network for clustering

**Location**: `results/clusters/union_network.txt`

**Format**: Edge list with optional weights

**Example**:
```
abl	ace	2
ace	Acon	3
abl	Acon	1
bun	btn	2
```

**Specifications**:
- Gene symbols (from remapped components)
- Tab-separated
- Optional third column: edge weight (frequency)
- Weights = number of components containing edge

### Cluster Assignments

**Purpose**: ClusterONE clustering results

**Location**: `results/clusters/clusters.txt`

**Format**: One cluster per line

**Example**:
```
1: abl ace Acon arr brk (0.001 0.85)
2: btn bun CG1234 CG5678 dac (0.01 0.72)
3: emc eve exu ftz gcm (0.005 0.68)
```

**Structure**: `ClusterID: gene1 gene2 ... (pvalue quality_score)`

**Columns**:
1. Cluster ID
2. Space-separated gene list
3. P-value (in parentheses)
4. Quality score (in parentheses)

### Individual Cluster Files

**Purpose**: One file per cluster

**Location**: `results/clusters/individual/`

**Format**: One gene per line

**Example** (`cluster_001.txt`):
```
abl
ace
Acon
arr
brk
```

**Specifications**:
- One gene symbol per line
- No header
- Sorted alphabetically (optional)

### Enrichment Results

**Purpose**: GO term enrichment analysis

**Location**: `results/enrichment/flyenrichr/`

**Format**: Tab-separated values

**Example** (`cluster_001_enrichment.txt`):
```
Rank	Term	P-value	Adjusted_P-value	Old_P-value	Old_Adjusted_P-value	Odds_Ratio	Combined_Score	Genes
1	cell cycle (GO:0007049)	1.23e-08	4.56e-06	1.23e-08	4.56e-06	12.5	156.8	abl;ace;brk
2	DNA replication (GO:0006260)	5.67e-07	1.23e-04	5.67e-07	1.23e-04	8.3	89.4	abl;arr
3	mitotic cell cycle (GO:0000278)	2.34e-06	3.45e-04	2.34e-06	3.45e-04	6.7	65.2	ace;brk
```

**Columns**:
1. `Rank`: Order of significance
2. `Term`: GO term name and ID
3. `P-value`: Raw p-value
4. `Adjusted_P-value`: FDR-corrected p-value
5. `Old_P-value`: Previous calculation (if applicable)
6. `Old_Adjusted_P-value`: Previous correction
7. `Odds_Ratio`: Enrichment strength
8. `Combined_Score`: Composite score (p-value × odds ratio)
9. `Genes`: Semicolon-separated gene list

## Mapping Files

### Gene ID Mapping

**Purpose**: Map node numbers to gene IDs

**Location**: `data/mappings/gene_id_mapping.txt`

**Format**: Tab-separated

**Example**:
```
NodeID	GeneID
1	FBgn0000001
2	FBgn0000008
3	FBgn0000014
4	FBgn0000017
```

**Specifications**:
- Header row required
- Column 1: Node ID (integer)
- Column 2: FlyBase gene ID
- Tab-separated
- One mapping per line

### Gene Name Mapping

**Purpose**: Map gene IDs to gene symbols

**Location**: `data/mappings/gene_name_mapping.txt`

**Format**: Tab-separated

**Example**:
```
GeneID	GeneName
FBgn0000001	abl
FBgn0000008	ace
FBgn0000014	Acon
FBgn0000017	Acph-1
```

**Specifications**:
- Header row required
- Column 1: FlyBase gene ID
- Column 2: Gene symbol
- Tab-separated
- One mapping per line

### Combined Mapping

**Alternative**: Single file with both mappings

**Example**:
```
NodeID	GeneID	GeneName
1	FBgn0000001	abl
2	FBgn0000008	ace
3	FBgn0000014	Acon
```

## Format Validation

### Validation Scripts

```bash
# Validate edge list format
python validate_format.py \
    --input data/raw/timestep_01.txt \
    --format edgelist

# Validate mapping format
python validate_format.py \
    --input data/mappings/gene_id_mapping.txt \
    --format mapping

# Validate entire directory
python validate_all.py \
    --input data/processed/timesteps/
```

### Common Validation Checks

1. **Edge List**:
   - Exactly 2-3 columns
   - No empty lines
   - Consistent delimiter
   - Valid node IDs

2. **Mapping Files**:
   - Header present
   - Unique keys (node IDs or gene IDs)
   - No missing values
   - Valid gene ID format (FBgn + numbers)

3. **Component Files**:
   - Connected graph
   - Valid edges
   - Consistent node IDs

## Format Conversion

### Common Conversions

#### Space to Tab-Separated

```bash
# Convert space to tab
sed 's/ /\t/g' input.txt > output.txt
```

#### CSV to Tab-Separated

```bash
# Convert CSV to TSV
sed 's/,/\t/g' input.csv > output.txt
```

#### Add Header

```bash
# Add header to mapping file
echo -e "NodeID\tGeneID" | cat - mapping.txt > mapping_with_header.txt
```

#### Extract Columns

```bash
# Extract first two columns
awk '{print $1"\t"$2}' input.txt > output.txt
```

## File Size Guidelines

Typical file sizes:

| File Type | Size Range | Count |
|-----------|------------|-------|
| Timestep networks | 10-500 KB | 50-100 |
| Components | 1-10 KB | 100-1000 |
| Clusters | 1-5 KB | 10-50 |
| Enrichment | 10-100 KB | 10-50 |
| Mappings | 100 KB - 5 MB | 1-2 |

## Encoding and Line Endings

- **Encoding**: UTF-8 (preferred) or ASCII
- **Line endings**: Unix (LF) preferred, Windows (CRLF) acceptable
- **No BOM**: Files should not have byte-order mark

```bash
# Convert to Unix line endings
dos2unix file.txt

# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt
```

## Best Practices

1. **Consistency**: Use same delimiter throughout
2. **Sorting**: Sort large files for faster processing
3. **Compression**: Compress large intermediate files
4. **Validation**: Always validate after format conversion
5. **Backup**: Keep original files before conversion

## Troubleshooting

### Issue: "Invalid format" error

Check:
- Correct number of columns
- Consistent delimiter (tab vs space)
- No empty lines
- No header in edge list files

### Issue: Mapping fails

Check:
- Mapping file has header row
- All node IDs have mappings
- Gene ID format is correct (FBgn...)

### Issue: Unexpected characters

```bash
# Check for hidden characters
cat -A file.txt | head

# Remove carriage returns
tr -d '\r' < input.txt > output.txt
```

## Reference Tools

- **File validation**: Python, awk, custom scripts
- **Format conversion**: sed, awk, Python pandas
- **Inspection**: head, tail, wc, cat
- **Comparison**: diff, comm, cmp

For more help, see:
- [PIPELINE.md](../PIPELINE.md) - Usage in pipeline
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- Stage-specific READMEs - Format requirements per stage
