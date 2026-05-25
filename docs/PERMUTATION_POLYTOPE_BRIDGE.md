# Permutation-Polytope Bridge

Status: Phase G initial exact replay

## Purpose

Phase D established a guardrail:

```text
D4 and V4 are subgroup/coset tilers in S4, not Type-A poset cones.
```

The arXiv literature on permutation polytopes and the Birkhoff graph gives a
better home for this fact.  For a subgroup `H <= S4`, define:

```text
P(H) = conv{P_sigma : sigma in H}
```

where `P_sigma` is the permutation matrix.

The replay artifact is:

```text
scripts/analyze_permutation_polytope_bridge.py
tests/test_permutation_polytope_bridge.py
results/permutation_polytope_bridge.json
results/PERMUTATION_POLYTOPE_BRIDGE_REPORT.md
```

## Verified Facts

For the Durer source diagonal group and the terminal group:

```text
dim P(D4) = 5
dim P(V4) = 3
```

In the Birkhoff graph on `S4`, where two permutations are adjacent iff their
relative permutation is one nontrivial cycle:

```text
induced edges on D4 = 16
induced edges on V4 = 0
```

Every `V4` left coset is also Birkhoff-independent.  Every `D4` left coset
has the same dimension and induced edge count as `D4`.

So the diagonal break has a certified polytope/graph fingerprint:

```text
permutation-polytope dimension: 5 -> 3
Birkhoff induced edges:         16 -> 0
```

## Interpretation

The correct upgraded bridge is:

```text
D4 -> V4 is a subgroup permutation-polytope / Birkhoff-skeleton collapse.
```

This is stronger and cleaner than trying to force `V4` into:

```text
Type-A poset cone
tetrahedral dissection piece
Coxeter-pure shape family
```

## Open Face Tests

The current certificate does not prove any face relation.  These remain open:

```text
Is P(V4) a face of P(D4)?
Is P(D4) a face of B4?
Which V4 cosets are faces, if any, in the Birkhoff polytope?
What is the f-vector of P(D4) and P(V4)?
```

The finite fingerprints above are enough for roadmap control, not enough for
face-theorem claims.

## Guardrails

Do not claim:

- `P(V4)` is a face of `P(D4)`.
- `P(D4)` or `P(V4)` is a Birkhoff face.
- Birkhoff independence of `V4` explains the bounded terminal value `24` by
  itself.

The permutation-polytope layer explains the `S4` diagonal-group collapse.
