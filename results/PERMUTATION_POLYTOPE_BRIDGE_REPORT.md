# Permutation-Polytope Bridge Report

Status: Phase G initial exact replay

## Core Facts

- `dim P(D4)`: `5`
- `dim P(V4)`: `3`
- Birkhoff induced edges on `D4`: `16`
- Birkhoff induced edges on `V4`: `0`
- `V4` is Birkhoff-independent: `True`
- all `V4` cosets are Birkhoff-independent: `True`

## Reading

This is the natural continuation of the Phase-D guardrail.  `D4` and
`V4` are not Type-A poset cones; they are subgroup/coset objects inside
`S4`, and their convex hulls are small permutation polytopes inside the
Birkhoff setting.

The terminal break has a finite polytope/graph signature:

```text
dimension: 5 -> 3
Birkhoff induced edges: 16 -> 0
```

## Guardrail

These are exact finite fingerprints.  They do not yet prove that
`P(V4)` is a face of `P(D4)` or of the Birkhoff polytope; that is a
separate face-test branch.
