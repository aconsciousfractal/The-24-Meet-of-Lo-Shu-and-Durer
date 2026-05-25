# Type-A Subgroup Tilers

Status: Phase D initial chamber fingerprint
Date: 2026-05-24

## Purpose

This note locates the Durer source diagonal set `D4` and terminal diagonal set
`V4` inside the Type-A `A_3` chamber language.

The guiding distinction is:

```text
poset cones L(P) are one kind of chamber union;
subgroup/coset tilers H <= S_4 are another kind.
```

The project must not force `D4` or `V4` into the poset-cone category.

## Chamber Model

The `A_3` Coxeter chambers are indexed by the `24` words in `S_4`.

Chamber adjacency is modeled by swapping adjacent positions in a word.  The
full chamber graph therefore has:

```text
24 vertices
36 edges
```

Machine artifact:

```text
results/s4_chamber_fingerprints.json
```

Generator:

```powershell
python "scripts/analyze_s4_chambers.py" --write
```

## The Two Subgroups

Durer source diagonal group:

```text
D4 = {0123,0213,1032,1302,2031,2301,3120,3210}
```

Terminal group:

```text
V4 = {0123,1032,2301,3210}
```

Basic fingerprints:

| Group | Size | Order profile | Left cosets | Poset cone? |
|---|---:|---|---:|---|
| `D4` | 8 | `1:1, 2:5, 4:2` | 3 | no |
| `V4` | 4 | `1:1, 2:3` | 6 | no |

The drop is:

```text
D4 -> V4
8 -> 4
```

and `V4` is a subgroup of `D4`.

## Common-Halfspace Closure

In the standard Type-A poset-cone convention, a poset cone `L(P)` is determined
by precedence relations common to all its words.

For both `D4` and `V4`:

```text
common precedence relations: none
common-halfspace closure size: 24
```

Therefore:

```text
D4 != L(P)
V4 != L(P)
```

under this convention.

This is not a failure of the bridge. It identifies the correct side of the
bridge: subgroup/coset tilers, not poset cones.

## Coset Partitions

`D4` partitions `S_4` into 3 left cosets:

```text
{0123,0213,1032,1302,2031,2301,3120,3210}
{0132,0312,1023,1203,2130,2310,3021,3201}
{0231,0321,1230,1320,2013,2103,3012,3102}
```

`V4` partitions `S_4` into 6 left cosets:

```text
{0123,1032,2301,3210}
{0132,1023,2310,3201}
{0213,1302,2031,3120}
{0231,1320,2013,3102}
{0312,1203,2130,3021}
{0321,1230,2103,3012}
```

This is the precise tiler statement:

```text
left cosets of H tile S_4
```

for `H = D4` and `H = V4`.

## Chamber-Graph Connectivity

The induced chamber-unions are not connected in the standard adjacent-swap
chamber graph.

| Group | Components | Component sizes | Internal edges | Boundary edges |
|---|---:|---|---:|---:|
| `D4` | 4 | `2,2,2,2` | 4 | 16 |
| `V4` | 4 | `1,1,1,1` | 0 | 12 |

Explicit `D4` components:

```text
{0123,0213}
{1032,1302}
{2031,2301}
{3120,3210}
```

Explicit `V4` components:

```text
{0123}
{1032}
{2301}
{3210}
```

Thus `D4` and `V4` are subgroup/coset tilers but non-convex, disconnected
chamber unions in this chamber graph.

## Phase-D Reading

The correct Type-A statement is:

```text
The Durer diagonal break D4 -> V4 is a passage between subgroup/coset tilers
inside S_4. These tilers are not standard Type-A poset cones and are
disconnected as induced chamber-unions in the A_3 chamber graph.
```

This gives a clean bridge to the Tetra/Coxeter language:

- `S_4` indexes the `24` chambers of `A_3`;
- `D4` and `V4` are chamber subsets;
- their left cosets tile the chamber set;
- they should be compared to, not identified with, poset-cone tilers.

## Next Questions

1. Compare subgroup/coset tilers to the known poset-cone tiler families.
2. Compute chamber-neighborhood data for the 6 `V4` cosets and 3 `D4` cosets.
3. Decide whether a useful non-convex tiler vocabulary exists for these
   subgroup chamber unions.
4. Connect this with the Tetra `A_3` chamber model without importing
   unsupported convexity claims.
