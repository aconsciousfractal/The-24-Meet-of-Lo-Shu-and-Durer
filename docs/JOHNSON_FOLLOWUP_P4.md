# Phase P4 - Johnson Follow-Up

Phase P4 is a follow-up to P1/P2/P3.  It asks two narrow questions.

1. Does the terminal affine layer behave like a small constant-weight code
   relative to the fixed translation `V4` spread?
2. Can the O5e/O5f point-map collision split `24/20/16` be explained by a
   simple anchored Johnson or direction invariant?

## Terminal Affine Code

For the exact `144` records, the `36` terminal affine quaternes have one
uniform profile:

```text
inner distribution:       |Q cap R| = 0:246, 1:192, 2:192
point degrees:            every one of the 16 cells has degree 9
anchor shadow:            12*(1,1,1,1) + 20*(2,2,0,0) + 4*(4,0,0,0)
direction inventory:      3 complement + 5 line + 1 same
non-domain-affine count:  0
```

The `32` selected-affine extras split into two terminal-affine signatures;
the `60` outside-main records split into twelve.  None share the exact
signature.

## O5e Collision Split

The O5e/O5f split remains:

```text
distinct point maps per (P,W)-fiber:
  24 -> 96 fibers
  20 -> 16 fibers
  16 -> 32 fibers
```

No single tested coarse field explains every fiber by itself.  However, the
selected-plane directions fall into three regimes:

```text
0,1,2,3:   24 only
0,4,8,12: 24 only
0,1,4,5:  16/24
0,2,8,10: 16/24
0,1,8,9:  16/20/24
0,2,4,6:  16/20/24
```

The joint key

```text
(selected_plane_direction, translation_direction)
```

classifies the collision type with no ambiguity across the `144` `(P,W)`
fibers.

## Interpretation

P4 strengthens the follow-up layer:

```text
exact 144 = uniform terminal-affine constant-weight code relative to fixed V4
O5e collisions = direction-pair classified, but still mask-refined
```

Guardrail: this is affine/atlas structure.  It is not a new proof of
`Meet_strong = {24}`.

Artifacts:

```text
scripts/analyze_johnson_followup_p4.py
tests/test_johnson_followup_p4.py
results/johnson_followup_p4.json
results/JOHNSON_FOLLOWUP_P4_REPORT.md
```
