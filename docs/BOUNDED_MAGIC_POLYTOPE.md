# Bounded Magic Polytope

Status: Phase E initial linear certificate
Date: 2026-05-24

## Purpose

Phase E tests whether the meet value `24` is visible as a boundary phenomenon
in bounded magic-square polytopes.

This first layer is deliberately linear and exact:

- rank of the free-sum and fixed-sum magic affine spaces;
- active coordinate bounds along the Sagrada ray;
- local face dimensions at `D(0)` and `D(10)`;
- Lo Shu `S=24` as a lattice polygon in the `(a,b)` parameters.

Machine artifacts:

```text
scripts/analyze_bounded_magic_polytope.py
results/bounded_magic_polytope.json
results/BOUNDED_MAGIC_POLYTOPE_REPORT.md
tests/test_bounded_magic_polytope.py
```

The full fixed-sum `S=24` polytope audit is separated into:

```text
docs/FIXED_SUM24_POLYTOPE_AUDIT.md
results/fixed_sum24_polytope_audit.json
```

## Affine Dimensions

The script computes ranks over `Q`.

| Order | Variables | Free-sum dimension | Fixed-sum dimension |
|---:|---:|---:|---:|
| 3 | 9 | 3 | 2 |
| 4 | 16 | 8 | 7 |

Here "free-sum" means all rows, columns, and the two main diagonals are equal
to one common but unspecified sum. "Fixed-sum" additionally fixes that common
sum.

## Sagrada Ray

The Sagrada mask is:

```text
2013
```

It selects source values:

```text
r0c2 = 15
r1c0 = 12
r2c1 = 11
r3c3 = 16
```

The downward bounded interval is:

```text
0 <= t <= 10
```

At `t=10`, the magic sum is `24` and the terminal hit is:

```text
r2c1 = 1
```

## Active Facets Along The Ray

Coordinate-bound facets encountered by the ray:

| Parameter | Active coordinate bounds |
|---|---|
| `t=0` | `r0c0 = 1`, `r3c3 = 16` |
| `0 < t < 10` | `r0c0 = 1` |
| `t=10` | `r0c0 = 1`, `r2c1 = 1` |

Thus the ray lies on the persistent lower facet `r0c0 = 1`; it leaves the
initial upper facet `r3c3 = 16`; it terminates when `r2c1` hits the lower
bound.

## D(10) Face Dimension

At `D(10)`:

| Ambient bounded magic polytope | Face dimension | Vertex? |
|---|---:|---|
| free-sum order-4 polytope | 6 | no |
| fixed-sum `S=24` order-4 polytope | 5 | no |

Therefore:

```text
D(10) is a boundary point, not a vertex.
```

This is an important correction to any too-strong "endpoint equals vertex"
intuition.

## Local S=24 Face Around D(10)

The minimal fixed-sum `S=24` face containing `D(10)` is obtained by imposing
the two coordinate bounds active at the endpoint:

```text
r0c0 = 1
r2c1 = 1
```

Inside the fixed-sum `S=24` order-4 bounded magic polytope, this face has:

```text
dimension: 5
vertices: 47
integral vertices: 37
semi-integral vertices: 10
D(10) is a vertex of this face: no
```

The vertex denominator distribution is:

```text
1: 37
2: 10
```

The active-bound count distribution among the 47 vertices is:

```text
7: 6
8: 19
9: 6
10: 8
12: 8
```

Thus `D(10)` is not merely a non-vertex by rank count; it lies in a concrete
5-dimensional bounded face with a small exact vertex catalogue.

The first symmetry/fingerprint pass gives:

```text
common active bounds across all 47 vertices: r0c0=1, r2c1=1
D4 square-symmetry stabilizer of the vertex set: identity only
D(10) active bounds equal the common active bounds: yes
D(10) relative-interior point of this minimal face: yes
minimum non-forced lower slack at D(10): 1
minimum non-forced upper slack at D(10): 2
```

So the Sagrada endpoint does not inherit a visible residual square symmetry in
this local face.  It is best read as an oriented local face selected by the
ray, with `D(10)` in its relative interior.

A compact barycentric certificate is:

```text
D(10) = (4/5) V34 + (1/5) V41
```

where `V34` and `V41` are vertices `34` and `41` of the recorded local
47-vertex catalogue in `results/bounded_magic_polytope.json`.

Explicitly:

```text
V34 =
[[1,16,6,1],
 [1,6,6,11],
 [6,1,11,6],
 [16,1,1,6]]

V41 =
[[1,6,1,16],
 [6,11,6,1],
 [16,1,6,1],
 [1,6,11,6]]
```

The weights are strictly positive and sum to `1`.

The full fixed-sum `S=24` audit confirms that `V34` and `V41` are also
vertices of the full `S=24` polytope, with full-catalogue indices `126` and
`140`.

## Lo Shu S=24 Fiber

The Lo Shu parametrization is:

```text
[[g+a,   g-a-b, g+b],
 [g-a+b, g,     g+a-b],
 [g-b,   g+a+b, g-a]]
```

For `S=24`, we have `g=8`. The bounded fiber in `(a,b)` is the diamond:

```text
(0,-1), (1,0), (0,1), (-1,0)
```

It has:

```text
dimension: 2
integer lattice points: 5
common active coordinate-bound facets: none
```

The 5 lattice points recover the five bounded `S=24` Lo Shu squares.

## Reading

The current Phase-E reading is:

```text
On the 4x4 side, 24 is a terminal boundary value of the Sagrada ray, but the
terminal point D(10) is not a vertex.

On the 3x3 side, 24 appears as a small lattice count in the g=8 Lo Shu fiber,
not as a common coordinate-boundary face of the free bounded Lo Shu polytope.
```

This keeps the project honest:

- `24` is an endpoint/boundary value on the Sagrada ray;
- `24` is a non-degenerate small fiber on the Lo Shu side;
- the two mechanisms are related by the meet definition, not by a shared
  vertex statement.

## Next Checks

1. Compute vertices of the fixed-sum `S=24` order-4 bounded magic polytope near
   `D(10)` if a stronger local geometry statement is needed. Done for the
   minimal face defined by the two active endpoint bounds.
2. Decide whether the Lo Shu count table should be packaged as a short
   lattice-polygon/Ehrhart lemma.
3. Test whether the Sagrada ray endpoint lies on any distinguished
   higher-codimension face beyond the two active lower bounds. The first
   check says no extra coordinate-bound face: `D(10)` is relative-interior in
   the two-bound minimal face.
