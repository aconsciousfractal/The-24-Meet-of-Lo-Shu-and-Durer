# Lo Shu Lattice Polygon

Status: Phase E lattice lemma
Date: 2026-05-24

## Purpose

This note packages the bounded Lo Shu count table as a small lattice-polygon
lemma.

It is the `3 x 3` geometric side of Phase E. The `4 x 4` side is recorded in
`docs/BOUNDED_MAGIC_POLYTOPE.md`.

## Parametrization

Every Lo Shu-type magic square in the project is written as:

```text
[[g+a,   g-a-b, g+b],
 [g-a+b, g,     g+a-b],
 [g-b,   g+a+b, g-a]]
```

The magic sum is:

```text
S = 3g
```

The bounded condition is:

```text
1 <= every entry <= 9.
```

## Polygon Lemma

For fixed `g`, set:

```text
m = min(g-1, 9-g).
```

Then the bounded fiber in `(a,b)` is the lattice diamond:

```text
|a+b| <= m
|a-b| <= m
```

Equivalently, it has vertices:

```text
(m,0), (0,m), (-m,0), (0,-m)
```

with the convention that for `m=0` the polygon degenerates to the single point
`(0,0)`.

## Count Formula

For `m >= 1`, the diamond has:

```text
area = 2m^2
boundary lattice points = 4m
```

By Pick's theorem:

```text
|P_m cap Z^2| = area + boundary/2 + 1
              = 2m^2 + 2m + 1.
```

The same formula also gives `1` when `m=0`.

## Count Table

| `g` | Magic sum `S=3g` | `m` | Lattice count |
|---:|---:|---:|---:|
| 1 | 3 | 0 | 1 |
| 2 | 6 | 1 | 5 |
| 3 | 9 | 2 | 13 |
| 4 | 12 | 3 | 25 |
| 5 | 15 | 4 | 41 |
| 6 | 18 | 3 | 25 |
| 7 | 21 | 2 | 13 |
| 8 | 24 | 1 | 5 |
| 9 | 27 | 0 | 1 |

Thus:

```text
counts_by_sum = 1,5,13,25,41,25,13,5,1.
```

## The S=24 Fiber

For `S=24`, we have:

```text
g = 8
m = 1
```

The fiber is the diamond:

```text
(0,-1), (1,0), (0,1), (-1,0)
```

It has exactly:

```text
5 lattice points.
```

This is the non-degenerate Lo Shu side of the strong meet.

## Reading

The Lo Shu side of the meet is not a mysterious isolated count. It is the
smallest non-degenerate upper-side diamond after the central fiber:

```text
S=18 -> m=3 -> 25 points
S=21 -> m=2 -> 13 points
S=24 -> m=1 -> 5 points
S=27 -> m=0 -> 1 degenerate point
```

So `24` is the last non-degenerate bounded Lo Shu fiber before the degenerate
all-9 endpoint at `27`.
