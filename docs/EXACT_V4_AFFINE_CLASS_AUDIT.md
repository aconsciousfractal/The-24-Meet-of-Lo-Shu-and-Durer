# Exact-V4 Affine Class Audit

Status: Phase J finite characterization pass

## Purpose

Phase J tests whether the `144` exact canonical `V4` terminal subclass can be
described more cleanly than by the finite filter ladder alone.

The input artifacts are:

```text
results/order4_f2_extension.json
results/f2_orientation_stability.json
```

The new replay artifacts are:

```text
scripts/analyze_exact_v4_affine_class.py
tests/test_exact_v4_affine_class.py
results/exact_v4_affine_class_audit.json
results/EXACT_V4_AFFINE_CLASS_AUDIT_REPORT.md
```

## Result

Inside the `236` terminal-24 square-mask pairs:

```text
selected-mask affine / selected values {11,12,15,16}: 176
affine cell-value labeling: 144
exact canonical V4: 144
```

The strongest current statement is the finite equivalence:

```text
exact canonical V4
  <=> affine cell-value labeling
  <=> selected-mask affine plus affine cell-value labeling
```

Equivalently, the minimal Phase-J ladder is:

```text
terminal24                                      236
selected values {11,12,15,16} / mask affine     176
plus affine cell-value labeling                 144
exact canonical V4                              144
```

The first filter is too broad.  It gives the main `176`-pair class, which
splits as:

```text
cell_affine_exact_v4:       144
cell_non_affine_non_exact:   32
```

The `32` removed records are exactly the structured extras already visible in
Phase H.  Their terminal diagonal sets split as:

```text
0123,3210:                16
0123,0213,3120,3210:      8
0123,1302,2031,3210:      8
```

## Orientation Reading

The affine cell-value criterion is stable under:

```text
the 8 square symmetries used for essential representatives
direct value complement
canonicalized value complement
joint D4 transforms of terminal-24 square-mask pairs
```

However, the literal phrase:

```text
exact canonical V4 = {0123,1032,2301,3210}
```

is still canonical-orientation wording.  The orientation-stable object is the
affine cell-value criterion and transformed-mask `F2^4` profile.

## Paper Consequence

This is strong enough for an appendix-backed finite theorem:

```text
In the terminal-24 dataset, exact canonical V4 is equivalent to affine
cell-value labeling.
```

It should not delay paper v2.  A broader conceptual explanation belongs to a
follow-up Type-A/subgroup-coset tiler project.

## Guardrails

Do not claim:

- that selected-mask affineness alone characterizes exact canonical `V4`;
- that the literal word set `V4={0123,1032,2301,3210}` is orientation-free;
- that Phase J gives a conceptual proof of the `144` class beyond the finite
  terminal-24 atlas;
- that the `32` extras are noise.
