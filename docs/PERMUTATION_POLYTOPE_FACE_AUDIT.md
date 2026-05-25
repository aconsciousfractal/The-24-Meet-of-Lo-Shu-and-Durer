# Permutation-Polytope Face Audit

Status: Phase G face-test branch

Certificate:

```text
scripts/analyze_permutation_polytope_faces.py
results/permutation_polytope_face_audit.json
results/PERMUTATION_POLYTOPE_FACE_AUDIT_REPORT.md
tests/test_permutation_polytope_faces.py
```

## Question

Phase G had already shown:

```text
dim P(D4) = 5
dim P(V4) = 3
Birkhoff induced edges: D4 -> V4 = 16 -> 0
```

The remaining question was whether the terminal subgroup polytope `P(V4)` is
actually a face of the source subgroup polytope `P(D4)`, or of the full
Birkhoff polytope `B4`.

## Result

The face tests are negative:

```text
P(V4) face of P(D4): false
P(D4) face of B4:   false
P(V4) face of B4:   false
```

Thus the correct statement is:

```text
P(V4) is a natural terminal subpolytope inside the S4 permutation-polytope
language, but it is not a face of P(D4) or B4 in the tested sense.
```

## F-Vectors

The terminal polytope is a tetrahedron:

```text
dim P(V4) = 3
f(P(V4)) = (4, 6, 4)
```

The source `D4` polytope has:

```text
dim P(D4) = 5
f(P(D4)) = (8, 24, 34, 24, 8)
```

Here the f-vector excludes the whole polytope and records nonempty proper
faces by dimension.

## Birkhoff Support Completion

For a face of the Birkhoff polytope, the vertex set is determined by allowed
support positions.  The union support of both `D4` and `V4` uses all `16`
matrix positions:

```text
D4 support size: 16
V4 support size: 16
```

Therefore the support completion in `B4` contains all `24` permutation
vertices:

```text
D4 completion size: 24
V4 completion size: 24
```

So neither is a proper Birkhoff face.

## Interpretation

This closes the permutation-polytope overclaim risk.

What may be said:

```text
D4 -> V4 has a subgroup permutation-polytope and Birkhoff-skeleton signature.
The terminal V4 polytope is tetrahedral and Birkhoff-independent.
```

What may not be said:

```text
P(V4) is a face of P(D4).
P(D4) or P(V4) is a face of B4.
```

The bridge remains useful, but as subgroup/coset polytope geometry rather than
as a face-collapse theorem.
