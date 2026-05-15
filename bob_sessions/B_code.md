# Session B — Code (edit mode)

**Bob mode:** edit
**Captured:** 2026-05-08
**Target file:** `parity/scoring.py`
**Outcome:** ✅ All tests pass — three additions implemented, public API preserved.

---

## Prompt sent to Bob

> Improve `parity/scoring.py` with these additions, keeping the existing public API unchanged:
>
> 1. Extend the Wilson CI calculation to also return a `confidence_band` dict with `{low, high, width}` so the dashboard can visualise tightness directly.
> 2. Add a new function `score_by_tenant(results: list[dict], tenant_id: str) -> list[dict]` that filters results by `tenant_id` field before scoring (used for multi-entity banks per the v2 plan).
> 3. Add a docstring example showing how to use both new outputs.
> 4. Do not break existing callers — the public API of `score_results()` must remain backward-compatible.
>
> Generate the modified file as a complete replacement.

---

## Bob's summary of changes

✅ **Extended Wilson CI calculation** — added `confidence_band` property and dict output with `{low, high, width}` fields:
- The `confidence_band` property returns a dict for easy dashboard visualization
- Width calculation shows confidence tightness (narrower = more confident)
- Test shows width decreases from 43.4% (n=5) to 3.7% (n=100)

✅ **Added `score_by_tenant()` function** — filters results by tenant_id before scoring:
- Enables multi-entity bank analysis per v2 plan
- Signature: `score_by_tenant(results: list[dict], tenant_id: str) -> list[dict]`
- Tested with retail/commercial tenant separation

✅ **Added comprehensive docstrings** — both functions now have examples:
- `score_results()` shows basic usage and confidence_band access
- `score_by_tenant()` demonstrates multi-tenant filtering use case

✅ **Maintained backward compatibility** — public API unchanged:
- All original fields (ci_low, ci_high, etc.) still present
- `confidence_band` added as new field alongside existing ones
- Existing callers continue to work without modification

---

## Test results (run by Bob)

- ✓ Confidence band present in output
- ✓ All original fields preserved
- ✓ Tenant filtering works correctly
- ✓ Confidence width decreases with sample size (statistical validity)

The dashboard can now visualize confidence tightness directly using `scores[i]['confidence_band']['width']`.

---

## Resulting file structure (`parity/scoring.py`)

After Bob's edits — 238 lines, key additions verified:

| Symbol | Line | Purpose |
|---|---|---|
| `confidence_band` property | 77 | New — returns `{low, high, width}` dict |
| `to_dict()` updated | 126 | New — exposes `confidence_band` in serialised output |
| `score_results()` | 157 | Existing — backward-compatible, now richer output |
| `score_by_tenant()` | 200 | New — multi-tenant filtering wrapper |

The full file content is committed to the public repo as `parity/scoring.py`.
