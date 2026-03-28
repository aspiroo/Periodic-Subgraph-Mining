"""
Pipeline File Comparison Script
Compares each stage of the pipeline between legacy and current outputs.

Checks:
1. inputs.txt
2. output.txt (deduplicated edges)
3. outputWithEdgeNum.txt
4. timestep files (t1.txt ... t30.txt)
5. listMinerInputs.txt
6. ListMiner raw output (output.txt in java_run)
7. filtering_network p*s*.txt files
8. list_miner_outputs_with_edges p*s*.txt files
"""

from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parents[2]

# ── Legacy paths ──────────────────────────────────────────────────────────────
LEGACY = REPO_ROOT / "legacy"
LEGACY_PREPROCESSING  = LEGACY / "Preprocessing" 
LEGACY_FILTERING      = LEGACY / "Paper" / "filteringNetwork"
LEGACY_UNION          = LEGACY / "listMinerOutputs (with Edges)" / "new"

# ── Current paths ─────────────────────────────────────────────────────────────
CURRENT_PROCESSED     = REPO_ROOT / "data" / "processed"
CURRENT_TIMESTEPS     = CURRENT_PROCESSED / "timesteps_with_edge_number"
CURRENT_JAVA_RUN      = REPO_ROOT / "results" / "list_miner" / "java_run"
CURRENT_FILTERING     = REPO_ROOT / "results" / "list_miner" / "filtering_networks"
CURRENT_UNION         = REPO_ROOT / "results" / "list_miner" / "list_miner_outputs_with_edges"

PERIOD_SUPPORT_COMBOS = [
    (1, list(range(3, 10))),
    (2, list(range(3, 10))),
    (3, list(range(3, 8))),
    (4, list(range(3, 6))),
    (5, list(range(3, 5))),
    (6, list(range(3, 6))),
    (7, list(range(3, 6))),
    (8, list(range(3, 5))),
    (9, list(range(3, 5))),
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def compare_token_sets(label, legacy_path, current_path):
    """Compare two files as sets of tokens (order-independent)."""
    if not legacy_path.exists():
        print(f"  ⚠  LEGACY missing:  {legacy_path}")
        return
    if not current_path.exists():
        print(f"  ⚠  CURRENT missing: {current_path}")
        return

    legacy_tokens  = set(legacy_path.read_text(errors="ignore").split())
    current_tokens = set(current_path.read_text(errors="ignore").split())

    only_legacy  = legacy_tokens  - current_tokens
    only_current = current_tokens - legacy_tokens

    if not only_legacy and not only_current:
        print(f"  ✓  {label}: IDENTICAL token sets ({len(legacy_tokens)} tokens)")
    else:
        print(f"  ✗  {label}: DIFFERENT")
        print(f"       Legacy  tokens: {len(legacy_tokens)}")
        print(f"       Current tokens: {len(current_tokens)}")
        if only_legacy:
            sample = list(only_legacy)[:5]
            print(f"       In legacy only (sample): {sample}")
        if only_current:
            sample = list(only_current)[:5]
            print(f"       In current only (sample): {sample}")


def compare_line_counts(label, legacy_path, current_path):
    """Compare two files by line count and token sets."""
    if not legacy_path.exists():
        print(f"  ⚠  LEGACY missing:  {legacy_path.name}")
        return
    if not current_path.exists():
        print(f"  ⚠  CURRENT missing: {current_path.name}")
        return

    legacy_lines  = [l for l in legacy_path.read_text(errors="ignore").splitlines() if l.strip()]
    current_lines = [l for l in current_path.read_text(errors="ignore").splitlines() if l.strip()]

    legacy_tokens  = set(legacy_path.read_text(errors="ignore").split())
    current_tokens = set(current_path.read_text(errors="ignore").split())
    only_legacy  = legacy_tokens  - current_tokens
    only_current = current_tokens - legacy_tokens

    status = "✓ IDENTICAL" if (not only_legacy and not only_current) else "✗ DIFFERENT"
    print(f"  {status}  {label}: legacy={len(legacy_lines)} lines, current={len(current_lines)} lines")
    if only_legacy or only_current:
        if only_legacy:
            print(f"       In legacy only (sample): {list(only_legacy)[:5]}")
        if only_current:
            print(f"       In current only (sample): {list(only_current)[:5]}")


def compare_ordered(label, legacy_path, current_path):
    """Compare two files checking both content AND order."""
    if not legacy_path.exists():
        print(f"  ⚠  LEGACY missing:  {legacy_path.name}")
        return
    if not current_path.exists():
        print(f"  ⚠  CURRENT missing: {current_path.name}")
        return

    legacy_text  = legacy_path.read_text(errors="ignore").strip()
    current_text = current_path.read_text(errors="ignore").strip()

    if legacy_text == current_text:
        print(f"  ✓  {label}: IDENTICAL (content + order)")
    else:
        # Check if same tokens, different order
        lt = set(legacy_text.split())
        ct = set(current_text.split())
        if lt == ct:
            print(f"  ~  {label}: SAME TOKENS, different order")
        else:
            only_l = lt - ct
            only_c = ct - lt
            print(f"  ✗  {label}: DIFFERENT content")
            if only_l:
                print(f"       In legacy only (sample): {list(only_l)[:5]}")
            if only_c:
                print(f"       In current only (sample): {list(only_c)[:5]}")


# ── Stage 1: inputs.txt ───────────────────────────────────────────────────────
header("STAGE 1: inputs.txt")
legacy_inputs  = LEGACY_PREPROCESSING / "Inputs" /"inputs.txt"
current_inputs = CURRENT_PROCESSED /  "inputs.txt"

if legacy_inputs.exists() and current_inputs.exists():
    ll = legacy_inputs.read_text(errors="ignore").splitlines()
    cl = current_inputs.read_text(errors="ignore").splitlines()
    legacy_set  = set(ll)
    current_set = set(cl)
    print(f"  Legacy  lines: {len(ll)} | unique: {len(legacy_set)}")
    print(f"  Current lines: {len(cl)} | unique: {len(current_set)}")
    diff = legacy_set.symmetric_difference(current_set)
    if not diff:
        print("  ✓  Same unique edges (order may differ)")
    else:
        print(f"  ✗  {len(diff)} lines differ")
        print(f"     Sample diff: {list(diff)[:3]}")
else:
    print(f"  ⚠  Legacy path: {legacy_inputs} exists={legacy_inputs.exists()}")
    print(f"  ⚠  Current path: {current_inputs} exists={current_inputs.exists()}")


# ── Stage 2: output.txt ───────────────────────────────────────────────────────
header("STAGE 2: output.txt (deduplicated edges)")
legacy_output  = LEGACY_PREPROCESSING / "Python" / "output.txt"
current_output = CURRENT_PROCESSED / "output.txt"
compare_token_sets("output.txt", legacy_output, current_output)
if legacy_output.exists() and current_output.exists():
    ll = legacy_output.read_text(errors="ignore").splitlines()
    cl = current_output.read_text(errors="ignore").splitlines()
    print(f"  Legacy  line count: {len(ll)}")
    print(f"  Current line count: {len(cl)}")
    if ll == cl:
        print("  ✓  Order also matches!")
    else:
        print("  ~  Content same but order differs (set ordering issue)")


# ── Stage 3: outputWithEdgeNum.txt ────────────────────────────────────────────
header("STAGE 3: outputWithEdgeNum.txt")
legacy_ewn  = LEGACY_PREPROCESSING / "Python" / "outputWithEdgeNum.txt"
current_ewn = CURRENT_PROCESSED / "outputWithEdgeNum.txt"
compare_token_sets("outputWithEdgeNum.txt", legacy_ewn, current_ewn)
if legacy_ewn.exists() and current_ewn.exists():
    ll = legacy_ewn.read_text(errors="ignore").splitlines()
    cl = current_ewn.read_text(errors="ignore").splitlines()
    print(f"  Legacy  line count: {len(ll)}")
    print(f"  Current line count: {len(cl)}")


# ── Stage 4: timestep files ───────────────────────────────────────────────────
header("STAGE 4: Timestep files (t1.txt ... t30.txt)")
legacy_ts_dir  = LEGACY_PREPROCESSING / "Python" / "Timesteps with Edge Number"
current_ts_dir = CURRENT_TIMESTEPS

if not legacy_ts_dir.exists():
    print(f"  ⚠  Legacy timesteps dir not found: {legacy_ts_dir}")
else:
    identical = 0
    different = 0
    missing   = 0
    for i in range(1, 31):
        lf = legacy_ts_dir  / f"t{i}.txt"
        cf = current_ts_dir / f"t{i}.txt"
        if not lf.exists() or not cf.exists():
            missing += 1
            continue
        lt = set(lf.read_text(errors="ignore").split())
        ct = set(cf.read_text(errors="ignore").split())
        if lt == ct:
            identical += 1
        else:
            different += 1
            print(f"  ✗  t{i}.txt differs: legacy={len(lt)} tokens, current={len(ct)} tokens")
            diff = lt.symmetric_difference(ct)
            print(f"       Sample diff: {list(diff)[:3]}")
    print(f"  Summary: {identical} identical, {different} different, {missing} missing")


# ── Stage 5: listMinerInputs.txt ──────────────────────────────────────────────
header("STAGE 5: listMinerInputs.txt")
legacy_lmi  = LEGACY_PREPROCESSING / "Python" / "listMinerInput.txt"
current_lmi = CURRENT_PROCESSED / "listMinerInputs.txt"

if legacy_lmi.exists() and current_lmi.exists():
    ll = legacy_lmi.read_text(errors="ignore").splitlines()
    cl = current_lmi.read_text(errors="ignore").splitlines()
    print(f"  Legacy  lines: {len(ll)}")
    print(f"  Current lines: {len(cl)}")
    mismatches = 0
    for i, (l, c) in enumerate(zip(ll, cl)):
        lt = set(l.split())
        ct = set(c.split())
        if lt != ct:
            mismatches += 1
            if mismatches <= 3:
                diff = lt.symmetric_difference(ct)
                print(f"  ✗  Line {i+1} differs. Sample diff: {list(diff)[:3]}")
    if mismatches == 0:
        print("  ✓  All timestep lines have identical token sets")
    else:
        print(f"  ✗  {mismatches} timestep lines differ")
else:
    print(f"  ⚠  Legacy: {legacy_lmi.exists()} | Current: {current_lmi.exists()}")


# ── Stage 6: Java ListMiner raw output ────────────────────────────────────────
header("STAGE 6: Java ListMiner raw output")
legacy_lm_output  = LEGACY / "listMinerOutputs" / "output.txt"
current_lm_output = CURRENT_JAVA_RUN / "output.txt"

# Try alternate legacy paths
if not legacy_lm_output.exists():
    legacy_lm_output = LEGACY / "Codes & Data" / "ListMiner Output" / "listMinerOutputs" / "output.txt"

if legacy_lm_output.exists() and current_lm_output.exists():
    ll = [l for l in legacy_lm_output.read_text(errors="ignore").splitlines() if l.strip()]
    cl = [l for l in current_lm_output.read_text(errors="ignore").splitlines() if l.strip()]
    print(f"  Legacy  lines: {len(ll)}")
    print(f"  Current lines: {len(cl)}")
else:
    print(f"  ⚠  Legacy output: {legacy_lm_output} exists={legacy_lm_output.exists()}")
    print(f"  ⚠  Current output: {current_lm_output} exists={current_lm_output.exists()}")
    print("  (Raw ListMiner output may not exist in legacy — this is expected)")


# ── Stage 7: filtering_network p*s*.txt ───────────────────────────────────────
header("STAGE 7: filtering_network p*s*.txt files")
identical = different = missing = 0
for period, supports in PERIOD_SUPPORT_COMBOS:
    for support in supports:
        fname = f"p{period}s{support}.txt"
        lf = LEGACY_FILTERING  / fname
        cf = CURRENT_FILTERING / fname
        if not lf.exists() and not cf.exists():
            continue
        if not lf.exists():
            print(f"  ⚠  {fname}: missing in legacy")
            missing += 1
            continue
        if not cf.exists():
            print(f"  ⚠  {fname}: missing in current")
            missing += 1
            continue
        # Compare subgraph counts
        ll = [l for l in lf.read_text(errors="ignore").splitlines() if l.strip()]
        cl = [l for l in cf.read_text(errors="ignore").splitlines() if l.strip()]
        lt = set(lf.read_text(errors="ignore").split())
        ct = set(cf.read_text(errors="ignore").split())
        if lt == ct:
            identical += 1
        else:
            different += 1
            print(f"  ✗  {fname}: legacy={len(ll)} subgraphs, current={len(cl)} subgraphs")
            diff = lt.symmetric_difference(ct)
            print(f"       Token diff sample: {list(diff)[:5]}")

print(f"  Summary: {identical} identical, {different} different, {missing} missing")


# ── Stage 8: list_miner_outputs_with_edges p*s*.txt ───────────────────────────
header("STAGE 8: list_miner_outputs_with_edges (union genes) p*s*.txt files")
identical = different = missing = 0
for period, supports in PERIOD_SUPPORT_COMBOS:
    for support in supports:
        fname = f"p{period}s{support}.txt"
        lf = LEGACY_UNION  / fname
        cf = CURRENT_UNION / fname
        if not lf.exists() and not cf.exists():
            continue
        if not lf.exists():
            print(f"  ⚠  {fname}: missing in legacy")
            missing += 1
            continue
        if not cf.exists():
            print(f"  ⚠  {fname}: missing in current")
            missing += 1
            continue
        lt = set(lf.read_text(errors="ignore").split())
        ct = set(cf.read_text(errors="ignore").split())
        only_l = lt - ct
        only_c = ct - lt
        if not only_l and not only_c:
            identical += 1
        else:
            different += 1
            print(f"  ✗  {fname}: legacy={len(lt)} tokens, current={len(ct)} tokens")
            if only_l:
                print(f"       In legacy only (sample): {list(only_l)[:5]}")
            if only_c:
                print(f"       In current only (sample): {list(only_c)[:5]}")

print(f"  Summary: {identical} identical, {different} different, {missing} missing")


print(f"\n{'='*60}")
print("  COMPARISON COMPLETE")
print(f"{'='*60}\n")