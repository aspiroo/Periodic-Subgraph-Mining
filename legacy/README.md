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

This directory contains the original code directories:

```
legacy/
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

**Status**: Migration complete. All original directories have been moved to `legacy/`.

The organized structure is now active:
- `scripts/` - Processing pipeline scripts
- `external_tools/` - Third-party tools
- `matlab/` - MATLAB code
- `data/` - Input data
- `results/` - Output results

See [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) for migration details.

## Archiving Process

The original code has already been archived to this directory:

```bash
# How the migration was performed
mv "Analysis Code" legacy/
mv "Preprocessing Code" legacy/
mv "Post Processing Code" legacy/
mv "Subgraph Code" legacy/
mv "Purity Code" legacy/
mv "ClusterOne" legacy/
mv "FlyEnrichR Code" legacy/
mv "Funcassociate" legacy/
mv "Rest Genes" legacy/
mv "Keller codes" legacy/
```

## Using Legacy Code

If you need to run legacy code:

```bash
# Navigate to legacy directory
cd legacy

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

**Last Updated**: After repository migration

**Archive Status**: Complete - original code directories are in `legacy/`
