# Fixed-Sum S=24 Polytope Audit

Status: Phase E full fixed-sum audit
Date: 2026-05-24

## Purpose

This note records the full vertex audit of the bounded order-4 magic polytope
with fixed magic sum `24`:

```text
1 <= x_ij <= 16
all rows, columns, and the two main diagonals sum to 24
```

Machine artifacts:

```text
scripts/audit_fixed_sum24_polytope.py
results/fixed_sum24_polytope_audit.json
results/FIXED_SUM24_POLYTOPE_AUDIT_REPORT.md
tests/test_fixed_sum24_polytope_audit.py
```

## Method

The affine fixed-sum space has dimension `7`.  A vertex is obtained by adding
enough coordinate bounds to make a zero-dimensional solution.

The audit checks:

```text
32 coordinate-bound hyperplanes
choose 7 at a time
3,365,856 combinations
```

The script uses floating point only as a speed filter.  Every retained
candidate is reconstructed and verified over `Q` before it is recorded.

Audit counts:

```text
checked combinations: 3,365,856
singular combinations: 2,636,768
float-feasible combinations: 12,960
exact-feasible combinations: 12,960
unique vertices: 292
```

## Vertex Census

The full fixed-sum `S=24` polytope has:

```text
affine dimension: 7
vertices: 292
integral vertices: 180
semi-integral vertices: 112
```

Denominator distribution:

```text
1: 180
2: 112
```

Active-bound count distribution:

```text
7: 48
8: 124
9: 80
10: 16
12: 24
```

Therefore the polytope is not integral.

## Symmetry

The full vertex set is stabilized by the full square `D4` action:

```text
id
rot90
rot180
rot270
ref_main_diag
ref_anti_diag
ref_vertical
ref_horizontal
```

This contrasts with the local 47-vertex face around `D(10)`, whose square
stabilizer is identity only.

## D(10)

The audit confirms:

```text
D(10) is not a vertex of the full fixed-sum S=24 polytope.
```

The minimal local face around `D(10)` has:

```text
47 vertices
all 47 are vertices of the full fixed-sum S=24 polytope
```

The two-vertex barycentric certificate also embeds in the full vertex
catalogue:

```text
local vertex indices: 34, 41
full vertex indices: 126, 140
weights: 4/5, 1/5
```

Thus:

```text
D(10) = (4/5) V126 + (1/5) V140
```

in the full fixed-sum `S=24` vertex catalogue.

## Reading

The full `S=24` polytope restores the expected square symmetry.  The Sagrada
endpoint `D(10)` lies on its boundary, not as a vertex, but inside a
distinguished 47-vertex local face selected by the two active lower bounds
`r0c0=1` and `r2c1=1`.

So the correct geometry is:

```text
full S=24 polytope: 292 vertices, full D4 square symmetry
D(10) local face: 47 vertices, trivial square stabilizer
D(10): boundary point with two-vertex barycentric certificate
```
