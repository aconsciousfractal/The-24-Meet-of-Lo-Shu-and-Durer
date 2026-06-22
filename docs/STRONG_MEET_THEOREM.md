# Strong Meet Theorem

Status: Phase B paper-ready draft
Date: 2026-05-24

## Purpose

This note isolates the first theorem of the Magic 24 project in a form that can
be moved almost directly into the paper draft.

The statement is intentionally narrow:

```text
24 is the unique strong meet of the Lo Shu bounded upward spectrum and the
Durer/Sagrada bounded downward ray.
```

It does not claim that 24 is universal for magic squares.

## Definitions

Let `B(n,m,S)` be the set of integer `n x n` magic squares whose row sums,
column sums, and two main diagonal sums are all `S`, with every entry in
`[1,m]`. Repeated entries are allowed.

Let

```text
Spec^+_{3,9}(15) = {S > 15 : B(3,9,S) is nonempty}.
```

For the Durer-complement square

```text
1  14 15 4
12 7  6  9
8  11 10 5
13 2  3  16
```

and the Sagrada mask

```text
M = {(0,2), (1,0), (2,1), (3,3)},
```

define the ray

```text
D(t) = D - tM.
```

The bounded downward ray spectrum is

```text
Ray^-_{D,M} = {34-t : 1 <= t <= t_max},
```

where `t_max` is the largest integer for which all entries of `D(t)` remain in
`[1,16]`.

Define the weak meet by ordinary intersection:

```text
Meet_weak = Spec^+_{3,9}(15) cap Ray^-_{D,M}.
```

Define the strong meet as the subset of `Meet_weak` consisting of sums that
are:

1. non-degenerate on the `3 x 3` bounded side, meaning the fiber is not the
   single constant all-boundary square;
2. terminal on the `4 x 4` Durer/Sagrada side, meaning the sum occurs at
   `t=t_max`.

## Theorem

```text
Meet_weak = {24,27}
Meet_strong = {24}
```

## Proof

The integer parametrization of `3 x 3` magic squares gives possible bounded
sums:

```text
3, 6, 9, 12, 15, 18, 21, 24, 27.
```

Therefore

```text
Spec^+_{3,9}(15) = {18,21,24,27}.
```

The Phase-A certificate gives the fiber sizes:

```text
|B(3,9,24)| = 5
|B(3,9,27)| = 1
```

and the unique `S=27` square is the constant all-9 square. Thus `24` is
non-degenerate on the bounded `3 x 3` side, while `27` is degenerate.

For the Durer/Sagrada ray, the selected mask entries are:

```text
15, 12, 11, 16.
```

Hence the largest descent preserving the lower bound `1` is

```text
t_max = min(15-1, 12-1, 11-1, 16-1) = 10.
```

Since the magic sum along the ray is `34-t`, the bounded downward spectrum is:

```text
{24,25,26,27,28,29,30,31,32,33}.
```

More generally, this weak-meet range is forced by terminal feasibility before
using the specific Sagrada mask.  In any normal order-four square, a
one-incidence mask selects four distinct values from `{1,...,16}`.  If `m` is
the smallest selected value, then

```text
t_max = m - 1
terminal sum = 34 - t_max = 35 - m.
```

To match a Lo Shu upper sum `S in {18,21,24,27}`, the selected minimum would
have to be `m = 35-S`:

| Lo Shu sum `S` | Required selected minimum `m` | Terminal feasible? |
|---:|---:|---|
| 18 | 17 | no, outside `{1,...,16}` |
| 21 | 14 | no, only three values `>=14` exist |
| 24 | 11 | yes |
| 27 | 8 | yes, but Lo Shu-degenerate |

Thus the only terminally feasible weak meet values are already `{24,27}`;
after the Lo Shu non-degeneration filter, only `24` remains.

Thus

```text
Meet_weak
= {18,21,24,27} cap {24,25,26,27,28,29,30,31,32,33}
= {24,27}.
```

Among these two weak meet points, `24` is terminal on the Durer/Sagrada ray
because it occurs at `t=10=t_max`. The point `27` occurs at `t=7`, so it is
not terminal.

Combining the two strong criteria:

| Sum | `3 x 3` side | `4 x 4` side | Strong? |
|---:|---|---|---|
| 24 | non-degenerate, 5 fibers | terminal, `t=10` | yes |
| 27 | degenerate all-9 fiber | non-terminal, `t=7` | no |

Therefore:

```text
Meet_strong = {24}.
```

## Certificate Pointers

The finite claims used in the proof are replayed by:

```text
scripts/magic24_certificates.py
results/magic24_certificate_pack.json
```

Relevant JSON sections:

```text
lo_shu_bounded_spectrum
durer_one_incidence_masks
```

Relevant claim IDs:

```text
M24-C01
M24-C02
M24-C03
M24-C04
M24-C05
M24-C06
```

## Scope Boundary

This theorem does not say:

- that `24` is universal for magic squares;
- that `27` is uninteresting;
- that Durer is unique among all order-4 normal magic squares;
- that every one-incidence ray has an analogous endpoint.

Those are separate questions for later phases.
