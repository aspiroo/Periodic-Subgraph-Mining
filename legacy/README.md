# Legacy Code

This directory preserves the original code structure for reference and backward compatibility.

## Purpose

The `legacy/` directory serves to:
1. **Preserve history**: Keep original code structure
2. **Reference**: Compare with new organized structure
3. **Backup**: Safety net during migration
4. **Documentation**: Show evolution of repository

## Important Notice

⚠️ **DO NOT use this directory for active development.**

For new work, use the organized structure:
- `scripts/` - Processing pipeline scripts
- `external_tools/` - Third-party tools
- `matlab/` - MATLAB code
- `data/` - Input data
- `results/` - Output results

## Original Structure

If populated, this directory may contain:

```
legacy/
└── original_structure/
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

## When to Use

Use legacy code only if:
- Comparing with new implementation
- Debugging migration issues
- Need reference for specific functionality
- Reproducing old results exactly

## Migration Status

This directory is created as part of repository reorganization.

**Status**: Awaiting migration (original directories currently at repository root)

See [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) for migration instructions.

## Archiving Process

When you're ready to archive old code:

```bash
# Move original directories here
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

# Add archive date
echo "Archived: $(date)" >> legacy/ARCHIVE_DATE.txt
```

## Using Legacy Code

If you need to run legacy code:

```bash
# Navigate to legacy directory
cd legacy/original_structure

# Use old structure
cd "Analysis Code"
python filtering.py

# Remember: paths may be different!
```

**Note**: Legacy code may have hardcoded paths that don't work in new structure.

## Differences from New Structure

| Aspect | Legacy | New |
|--------|--------|-----|
| Organization | Flat, by code type | Hierarchical, by pipeline stage |
| Documentation | Minimal | Comprehensive READMEs |
| Structure | Ad-hoc | Standardized |
| Paths | Various | Consistent |

## Deprecation Notice

**Timeline**: This directory may be removed in future versions after sufficient migration time.

**Recommendation**: Migrate to new structure as soon as practical.

## Questions?

- See [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) for migration help
- See [PIPELINE.md](../PIPELINE.md) for new pipeline usage
- Check [README.md](../README.md) for repository overview

## Preservation Policy

This code is preserved for:
- **Reference**: Understanding original implementation
- **Reproducibility**: Matching published results
- **History**: Tracking repository evolution

But should not be modified or extended.

## Alternative Approach

Instead of archiving, you can:
1. Keep original directories at repository root
2. Use new structure alongside old
3. Gradually phase out old code
4. Document which you're using

See [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) Option 3: Hybrid Approach.

---

**Last Updated**: [To be filled during migration]

**Archive Status**: Awaiting migration

**Original Code Location**: Currently at repository root
