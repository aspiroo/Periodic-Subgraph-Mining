# Migration Guide

Guide for reorganizing the repository from the current structure to the new organized structure.

## Overview

This guide helps you transition from the original flat directory structure to the new organized structure with minimal disruption. The migration is **optional** and can be done gradually.

**Important**: The new structure coexists with the old structure. You can continue using the original directories while migrating at your own pace.

## Current vs. New Structure

### Current Structure
```
Periodic-Subgraph-Mining/
├── Analysis Code/
├── Preprocessing Code/
├── Post Processing Code/
├── Subgraph Code/
├── Purity Code/
├── ClusterOne/
├── FlyEnrichR Code/
├── Funcassociate/
├── Rest Genes/
└── Keller codes/
```

### New Structure
```
Periodic-Subgraph-Mining/
├── scripts/
│   ├── 01_preprocessing/
│   ├── 02_mining/
│   ├── 03_component_extraction/
│   ├── 04_analysis/
│   ├── 05_clustering/
│   └── 06_enrichment/
├── external_tools/
│   ├── listminer/
│   └── clusterone/
├── matlab/
├── data/
├── results/
└── legacy/  (for archived original code)
```

## Migration Strategy

You have three options:

### Option 1: Gradual Migration (Recommended)
- Keep both structures during transition
- Copy scripts to new locations
- Update paths in copied scripts
- Test new structure while old remains functional

### Option 2: Complete Migration
- Move all code to new structure at once
- Archive old directories in `legacy/`
- Update all paths
- Comprehensive testing required

### Option 3: Hybrid Approach
- Keep original directories as-is
- Only use new structure for new work
- Document which structure you're using

## Step-by-Step Migration

### Phase 1: Backup Current State

```bash
# Create a backup of your current work
cd /path/to/Periodic-Subgraph-Mining
git branch backup-before-migration
git add .
git commit -m "Backup before migration"

# Or create a tarball backup
tar -czf backup_$(date +%Y%m%d).tar.gz \
    "Analysis Code" \
    "Preprocessing Code" \
    "Post Processing Code" \
    "Subgraph Code" \
    "Purity Code" \
    "ClusterOne" \
    "FlyEnrichR Code" \
    "Funcassociate" \
    "Rest Genes" \
    "Keller codes"
```

### Phase 2: Copy Scripts to New Locations

#### Preprocessing Scripts

```bash
# Copy preprocessing code
cp "Preprocessing Code"/*.py scripts/01_preprocessing/
cp "Preprocessing Code"/*.sh scripts/01_preprocessing/

# Copy Keller MATLAB codes
cp "Keller codes"/*.m matlab/
```

#### Mining Scripts

```bash
# Copy subgraph mining code
cp "Subgraph Code"/*.py scripts/02_mining/

# Note: ListMiner binary goes in external_tools/listminer/
# (You'll need to download/compile ListMiner separately)
```

#### Component Extraction

```bash
# Copy component extraction scripts
cp "Subgraph Code"/subgraph_count.py scripts/03_component_extraction/
```

#### Analysis Scripts

```bash
# Copy analysis code
cp "Analysis Code"/*.py scripts/04_analysis/

# Copy post-processing code
cp "Post Processing Code"/*.py scripts/04_analysis/

# Copy purity calculation
cp "Purity Code"/*.py scripts/04_analysis/
```

#### Clustering Scripts

```bash
# Copy ClusterONE files
cp ClusterOne/*.jar external_tools/clusterone/
cp ClusterOne/*.txt external_tools/clusterone/
cp ClusterOne/*.py scripts/05_clustering/
```

#### Enrichment Scripts

```bash
# Copy FlyEnrichr code
cp "FlyEnrichR Code"/*.py scripts/06_enrichment/

# Copy FuncAssociate code
cp Funcassociate/*.py scripts/06_enrichment/
cp Funcassociate/*.txt scripts/06_enrichment/
```

### Phase 3: Update File Paths

After copying, you need to update paths in the scripts. Here's what to change:

#### Pattern 1: Relative imports
```python
# Old (in Preprocessing Code/)
import ../data/input.txt

# New (in scripts/01_preprocessing/)
import ../../data/raw/input.txt
```

#### Pattern 2: Output directories
```python
# Old
output_dir = "../output/"

# New
output_dir = "../../results/listminer_output/"
```

#### Pattern 3: Data file locations
```python
# Old
data_file = "../data.txt"

# New
data_file = "../../data/processed/timesteps/data.txt"
```

### Automated Path Updates

Use this script to help update paths:

```bash
# Create update script
cat > update_paths.sh << 'EOF'
#!/bin/bash
# Update common path patterns in Python files

find scripts/ -name "*.py" -type f -exec sed -i.bak \
    -e 's|../output/|../../results/|g' \
    -e 's|../data/|../../data/|g' \
    -e 's|../input/|../../data/raw/|g' \
    {} \;

echo "Paths updated. Check .bak files for originals."
EOF

chmod +x update_paths.sh
./update_paths.sh
```

### Phase 4: Update README References

```bash
# Create script-specific READMEs
cat > scripts/01_preprocessing/README.md << 'EOF'
# Preprocessing Stage

Scripts for converting and preparing network data.

## Usage
See main PIPELINE.md for detailed instructions.

## Scripts
- preprocessing_script.py: Main preprocessing
- convert_format.py: Format conversion

EOF
```

Repeat for each script directory (templates provided in repository).

### Phase 5: Test New Structure

```bash
# Test preprocessing
cd scripts/01_preprocessing
python preprocessing_script.py --help

# Test mining
cd ../02_mining
bash run_listminer.sh --test

# Test each stage systematically
```

### Phase 6: Archive Old Structure (Optional)

Once you've verified the new structure works:

```bash
# Move old directories to legacy/
mkdir -p legacy/original_structure

mv "Analysis Code" legacy/original_structure/
mv "Preprocessing Code" legacy/original_structure/
mv "Post Processing Code" legacy/original_structure/
mv "Subgraph Code" legacy/original_structure/
mv "Purity Code" legacy/original_structure/
mv "ClusterOne" legacy/original_structure/
mv "FlyEnrichR Code" legacy/original_structure/
mv "Funcassociate" legacy/original_structure/
mv "Rest Genes" legacy/original_structure/
mv "Keller codes" legacy/original_structure/

# Create archive README
cat > legacy/README.md << 'EOF'
# Legacy Code Archive

This directory contains the original code structure for reference.

**Do not use these directories for active development.**

Use the organized structure in:
- scripts/ (for processing code)
- external_tools/ (for third-party tools)
- matlab/ (for MATLAB code)

Last archived: $(date)
EOF
```

## Verification Checklist

After migration, verify:

- [ ] All Python scripts run without import errors
- [ ] File paths resolve correctly
- [ ] Output directories are created properly
- [ ] Pipeline runs end-to-end
- [ ] Results match previous runs (if applicable)
- [ ] Documentation is accurate
- [ ] Git history is preserved

## Common Migration Issues

### Issue 1: Import Errors

**Problem**: `ModuleNotFoundError` or `FileNotFoundError`

**Solution**:
```bash
# Check current working directory in scripts
pwd

# Verify relative paths
ls ../../data/raw/

# Update PYTHONPATH if needed
export PYTHONPATH="${PYTHONPATH}:/path/to/Periodic-Subgraph-Mining"
```

### Issue 2: Permission Errors

**Problem**: Cannot execute scripts in new locations

**Solution**:
```bash
# Make scripts executable
find scripts/ -name "*.sh" -exec chmod +x {} \;
find scripts/ -name "*.py" -exec chmod +x {} \;
```

### Issue 3: Missing Dependencies

**Problem**: Scripts fail due to missing libraries

**Solution**:
```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install individually as needed
pip install pandas numpy networkx
```

### Issue 4: Data Not Found

**Problem**: Scripts cannot find data files

**Solution**:
```bash
# Create data directories
bash setup_structure.sh

# Move your data to correct location
mv old_data/*.txt data/raw/

# Update data paths in scripts
```

## Rollback Procedure

If you need to rollback:

```bash
# Restore from git backup
git checkout backup-before-migration

# Or restore from tarball
tar -xzf backup_YYYYMMDD.tar.gz

# Or simply use legacy/ directory
cd legacy/original_structure
# Continue using old structure
```

## Best Practices

1. **Migrate one stage at a time** - Test each stage before moving to the next
2. **Keep backups** - Don't delete old code until new structure is verified
3. **Document changes** - Note any modifications you make
4. **Test thoroughly** - Run complete pipeline with both structures
5. **Update gradually** - No need to migrate everything at once

## Getting Help

If you encounter issues:

1. Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
2. Review [PIPELINE.md](PIPELINE.md) for correct usage
3. Open a GitHub issue with:
   - What you were trying to do
   - Error messages
   - Your migration step

## Timeline Recommendation

- **Week 1**: Set up new directories, copy first stage
- **Week 2**: Copy and test stages 2-3
- **Week 3**: Copy and test stages 4-6
- **Week 4**: Full pipeline testing, archive old structure

Take your time - there's no rush to complete migration!

## Maintaining Both Structures

If you choose to keep both structures:

1. **Primary development**: Use new structure
2. **Legacy scripts**: Keep old structure for reference
3. **Documentation**: Note which structure you're using in commit messages
4. **New users**: Direct them to new structure
5. **Old workflows**: Can continue using original directories

## Summary

- Migration is **optional** and can be gradual
- Both structures can coexist
- Test thoroughly before archiving old code
- Focus on one pipeline stage at a time
- Keep backups throughout process

The new structure provides better organization, but the old structure remains functional. Choose the approach that works best for your workflow.
