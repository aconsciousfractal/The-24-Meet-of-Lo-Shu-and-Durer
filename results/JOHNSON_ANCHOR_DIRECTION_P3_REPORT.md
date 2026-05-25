# Phase P3 Johnson Anchor Direction Audit

## Class Counts

```text
{"exact_v4": 144, "extra32": 32, "outside_main": 60}
```

## Direction Signature Summary

```text
signature_counts={'exact_v4': 1, 'extra32': 2, 'outside_main': 10}
pairwise_intersections={'exact_v4__extra32': 0, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0}
```

## Top Signatures

### exact_v4

```text
count=144 signature={"direction_relation_counts": {"complement": 3, "line": 5, "same": 1}, "non_domain_affine": 0, "quad_relation_counts": {"complement": 12, "line": 20, "same": 4}}
```

### extra32

```text
count=16 signature={"direction_relation_counts": {"complement": 4, "line": 2}, "non_domain_affine": 12, "quad_relation_counts": {"complement": 16, "line": 8}}
count=16 signature={"direction_relation_counts": {"complement": 3, "line": 2}, "non_domain_affine": 16, "quad_relation_counts": {"complement": 12, "line": 8}}
```

### outside_main

```text
count=16 signature={"direction_relation_counts": {"complement": 3, "line": 2}, "non_domain_affine": 15, "quad_relation_counts": {"complement": 12, "line": 8}}
count=8 signature={"direction_relation_counts": {"complement": 3, "line": 2, "same": 1}, "non_domain_affine": 10, "quad_relation_counts": {"complement": 12, "line": 8, "same": 2}}
count=8 signature={"direction_relation_counts": {"complement": 2, "line": 3}, "non_domain_affine": 13, "quad_relation_counts": {"complement": 8, "line": 8}}
count=4 signature={"direction_relation_counts": {"complement": 3, "line": 2}, "non_domain_affine": 12, "quad_relation_counts": {"complement": 12, "line": 8}}
count=4 signature={"direction_relation_counts": {"complement": 3, "line": 3}, "non_domain_affine": 10, "quad_relation_counts": {"complement": 12, "line": 10}}
count=4 signature={"direction_relation_counts": {"complement": 2, "line": 2}, "non_domain_affine": 18, "quad_relation_counts": {"complement": 8, "line": 6}}
count=4 signature={"direction_relation_counts": {"complement": 2, "line": 2}, "non_domain_affine": 16, "quad_relation_counts": {"complement": 8, "line": 6}}
count=4 signature={"direction_relation_counts": {"complement": 3, "line": 2, "same": 1}, "non_domain_affine": 9, "quad_relation_counts": {"complement": 12, "line": 8, "same": 2}}
```

## Interpretation

Relative to the fixed translation `V4` partition, an affine quaterne
with the same direction as the anchor has profile `4,0,0,0`; a
direction meeting the anchor in a line has profile `2,2,0,0`; and
a complementary direction has profile `1,1,1,1`.

The exact `144` records have a uniform terminal-affine direction
inventory:

```text
same direction:       1 direction,  4 quaternes
line intersection:    5 directions, 20 quaternes
complement direction: 3 directions, 12 quaternes
non-domain-affine terminal affine quaternes: 0
```

Thus the exact P2 terminal-affine anchored profile
`4*(4,0,0,0) + 20*(2,2,0,0) + 12*(1,1,1,1)` is not a
mysterious fingerprint; it is the quotient shadow of a uniform
`1+5+3` direction inventory relative to the fixed translation
direction.

The selected-affine extras and outside-main records do not share
this direction inventory.  This explains why the O5-anchored
Johnson profile separates the `144` from the `32`, while the
mask-only Johnson profile does not.
