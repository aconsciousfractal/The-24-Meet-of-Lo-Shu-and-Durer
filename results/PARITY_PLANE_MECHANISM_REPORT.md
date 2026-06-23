# Parity-Plane Mechanism Report

Status: public finite residual check.  The residual step is still a six-value check, not a table-free symbolic proof.

## Summary

- residual values: `[2, 4, 6, 8, 12, 14]`
- all survivors have `a=v`: `True`
- all survivors have `g` zero on the critical bit: `True`
- NW balance possible in row residual: `False`
- column residual by transpose symmetry: `True`

## Six-Value Residual Table

| v | critical bit | direction classes | offsets | a-values | g-values | NW balance possible |
|---:|---:|---:|---:|---|---|---|
| 2 | 0 | 8 | 64 | `[2]` | `[12, 14]` | `False` |
| 4 | 1 | 8 | 64 | `[4]` | `[9, 13]` | `False` |
| 6 | 0 | 16 | 64 | `[6]` | `[8, 10, 12, 14]` | `False` |
| 8 | 2 | 8 | 64 | `[8]` | `[3, 11]` | `False` |
| 12 | 1 | 16 | 64 | `[12]` | `[1, 5, 9, 13]` | `False` |
| 14 | 0 | 24 | 48 | `[14]` | `[2, 4, 6, 8, 10, 12]` | `False` |

## Guardrails

- The final residual step is a six-value finite check, not a table-free symbolic proof.
- The residual values are scoped input cases from the normalized parity-plane reduction, not newly derived here.
- The mechanism is scoped to the normalized parity-plane model used in this paper.
- This is not a universal endpoint-24 invariant for all magic squares.
