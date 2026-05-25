# Hilbert-Style Semigroup Audit

Status: Phase H finite atom/decomposition audit.

This is not a complete Hilbert-basis theorem.  It is a controlled finite
semigroup audit for the nonnegative `4 x 4` diagonal-magic cone.

## Scope

We enumerate nonnegative integer `4 x 4` diagonal-magic squares with fixed
magic sum:

```text
S = 1,2,3,4,5,6,7,8
```

and extract indecomposable elements with respect to addition inside the same
nonnegative diagonal-magic semigroup.

Then we test decompositions of:

```text
D
D(10)
all 236 terminal-24 endpoint squares Q-tM
```

using the atoms found in this finite audit.

## Atom Census

Square counts by magic sum:

```text
1: 8
2: 48
3: 200
4: 675
5: 1904
6: 4736
7: 10608
8: 21925
```

Indecomposable atoms found:

```text
sum 1: 8
sum 2: 12
sum 3: 0
sum 4: 0
sum 5: 0
sum 6: 0
sum 7: 0
sum 8: 0
```

Total checked atoms:

```text
20 = 8 + 12
```

Support counts:

```text
sum 1 atoms: support 4 -> 8
sum 2 atoms: support 7 -> 8, support 8 -> 4
```

## Durer Decompositions

The Durer source `D` has magic sum `34`.  In the checked atom set, its minimum
atom-count decomposition has:

```text
min atom count: 18
support size: 7
atom coefficient profile: sum1:2, sum2:16
```

The terminal `D(10)` has magic sum `24`.  Its minimum atom-count decomposition
has:

```text
min atom count: 18
support size: 8
atom coefficient profile: sum1:12, sum2:6
```

Thus the source and terminal have the same minimum atom count in this checked
atom model, but very different degree profiles.

## Terminal-24 Endpoint Decompositions

All `236` terminal-24 endpoints decompose in the checked atom set.

```text
failed decompositions: 0
```

Minimum atom-count distribution:

```text
12: 4
13: 4
14: 24
15: 8
16: 44
17: 16
18: 100
19: 8
20: 20
22: 8
```

By Phase-H class:

```text
exact_v4:
  14: 16
  16: 24
  18: 80
  20: 16
  22: 8

main_extra:
  12: 4
  14: 8
  16: 4
  18: 12
  20: 4

outside_main:
  13: 4
  15: 8
  16: 16
  17: 16
  18: 8
  19: 8
```

## Interpretation

This gives a new semigroup fingerprint:

```text
minimum atom count in the checked 20-atom model
```

It does not isolate Durer/Sagrada.  The canonical `D(10)` lies in the largest
minimum-count class:

```text
min atom count 18: 100 terminal-24 pairs
```

However, the class distributions differ:

```text
exact_v4 uses even minimum counts 14,16,18,20,22;
main_extra uses even minimum counts 12,14,16,18,20;
outside_main uses 13,15,16,17,18,19.
```

So the audit adds a useful semigroup layer, especially for comparing
`exact_v4`, `main_extra`, and `outside_main`.

## Guardrail

Do not claim:

```text
the full Hilbert basis of the nonnegative diagonal-magic cone is proved;
no higher-degree Hilbert atoms exist;
D(10) is Hilbert-sparse or Hilbert-unique;
the semigroup fingerprint isolates Durer/Sagrada.
```

The established statement is:

```text
up to magic sum 8, the only indecomposable checked atoms occur at sums 1 and
2, and all Magic 24 target endpoints decompose in the 20-atom set found there.
```

## Artifacts

```text
scripts/analyze_hilbert_semigroup_audit.py
tests/test_hilbert_semigroup_audit.py
results/hilbert_semigroup_audit.json
results/HILBERT_SEMIGROUP_AUDIT_REPORT.md
```
