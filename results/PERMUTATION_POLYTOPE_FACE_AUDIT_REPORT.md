# Permutation-Polytope Face Audit

Status: Phase G face-test branch

## Face Tests

- `P(V4)` face of `P(D4)`: `False`
- `P(D4)` Birkhoff face by support: `False`
- `P(V4)` Birkhoff face by support: `False`

## F-Vectors

- `P(D4)` dimension: `5`
- `P(D4)` f-vector: `{'0': 8, '1': 24, '2': 34, '3': 24, '4': 8}`
- `P(V4)` dimension: `3`
- `P(V4)` f-vector: `{'0': 4, '1': 6, '2': 4}`

## Birkhoff Support Completion

- `D4` support size: `16`
- `D4` completion size: `24`
- `V4` support size: `16`
- `V4` completion size: `24`

## Interpretation

`P(V4)` is a natural subpolytope of `P(D4)`, but it is not a face of
`P(D4)` under this vertex set.  Neither `P(D4)` nor `P(V4)` is a face
of the full Birkhoff polytope `B4`: their union supports allow all 24
permutation vertices.  The correct statement is therefore a subgroup
subpolytope / Birkhoff-skeleton statement, not a face statement.
