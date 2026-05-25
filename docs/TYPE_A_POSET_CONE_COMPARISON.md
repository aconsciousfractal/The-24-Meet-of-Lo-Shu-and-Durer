# Type-A Poset-Cone Comparison

Status: Phase D poset-cone tiler comparison
Date: 2026-05-24

## Purpose

This note compares the subgroup/coset tilers `D4` and `V4` against the
standard Type-A poset cones `L(P)` on 4 labeled elements.

Machine artifact:

```text
results/s4_poset_cone_comparison.json
```

Generator:

```powershell
python "scripts/analyze_s4_poset_cones.py" --write
```

## Enumeration

The exact enumeration gives:

```text
labeled posets on 4 elements: 219
unique linear-extension sets L(P): 219
```

Size distribution:

| Size of `L(P)` | Count |
|---:|---:|
| 1 | 24 |
| 2 | 36 |
| 3 | 48 |
| 4 | 30 |
| 5 | 24 |
| 6 | 20 |
| 8 | 24 |
| 12 | 12 |
| 24 | 1 |

## Left-Tiler Test

For each `L(P)`, the script tests whether left translates of `L(P)` partition
`S_4`.

Result:

```text
left-tiler poset cones: 195
non-tiler poset cones: 24
```

The non-tilers are exactly the size-5 cones, since `5` does not divide `24`.

Left-tiler size distribution:

| Size of `L(P)` | Tiler count |
|---:|---:|
| 1 | 24 |
| 2 | 36 |
| 3 | 48 |
| 4 | 30 |
| 6 | 20 |
| 8 | 24 |
| 12 | 12 |
| 24 | 1 |

## Chamber Connectivity

Every poset cone `L(P)` in this enumeration is connected as an induced
chamber-union in the adjacent-swap `A_3` chamber graph.

Component-size distribution:

| Component sizes | Poset-cone count |
|---|---:|
| `(1,)` | 24 |
| `(2,)` | 36 |
| `(3,)` | 48 |
| `(4,)` | 30 |
| `(5,)` | 24 |
| `(6,)` | 20 |
| `(8,)` | 24 |
| `(12,)` | 12 |
| `(24,)` | 1 |

## Comparison With D4 And V4

`D4` and `V4` are not among the 219 poset cones:

```text
D4 as L(P): false
V4 as L(P): false
```

The distinction is structural:

| Object | Tiler? | Poset cone? | Chamber components |
|---|---|---|---|
| poset-cone tiler `L(P)` | yes, except size 5 | yes | connected |
| `D4` subgroup tiler | yes | no | `2,2,2,2` |
| `V4` subgroup tiler | yes | no | `1,1,1,1` |

## Reading

This cleanly separates two tiler species in `S_4`:

```text
Type-A poset-cone tilers:
  convex/common-halfspace chamber unions L(P), connected.

Subgroup/coset tilers:
  group-theoretic partitions by left cosets, not necessarily convex,
  and in the D4/V4 cases disconnected.
```

Therefore the correct Phase-D bridge is not:

```text
D4 or V4 is a poset cone.
```

It is:

```text
D4 and V4 are subgroup/coset tilers that sit beside the poset-cone tilers in
the A3 chamber model.
```

The terminal break `D4 -> V4` moves within the subgroup/coset tiler species,
not from a poset cone to another poset cone.
