# APD / PTE Layer

Status: Phase G initial exact replay

## Purpose

The arXiv literature around Takemura's Alternating Power Difference clarifies
what the APD facts in Magic 24 mean.  For a matrix `A`, Takemura defines

```text
f_A(sigma) = tr(A P_sigma) = sum_i A[i,sigma(i)].
```

This is exactly the permutation-diagonal sum used in the Durer/Sagrada side
of this project.  The alternating power difference is:

```text
APD_m(A) = sum_{sigma in S_n} sgn(sigma) f_A(sigma)^m.
```

Therefore:

```text
APD_m(A)=0
```

is equivalent to equality of the `m`-th power sums of the even and odd
permutation-diagonal sum multisets.  This is the local Prouhet-Tarry-Escott
reading.

The replay artifact is:

```text
scripts/analyze_apd_pte.py
tests/test_apd_pte.py
results/apd_pte_analysis.json
results/APD_PTE_REPORT.md
```

## Verified Along The Sagrada Ray

The Phase-A certificate already had:

```text
APD_3(D(t)) = -24 t(t-4)(t-16)
APD_3(D(t)) = 6 det Ehat(t)
```

The Phase-G replay extends the APD/PTE table to degrees `1,...,8`:

```text
APD_1(t) = 0
APD_2(t) = 0
APD_3(t) = -24 t(t-4)(t-16)
```

On the bounded Sagrada interval `0 <= t <= 10`, the first nonzero degree up
to degree 8 is:

```text
t= 0, sum=34: 4
t= 1, sum=33: 3
t= 2, sum=32: 3
t= 3, sum=31: 3
t= 4, sum=30: 4
t= 5, sum=29: 3
t= 6, sum=28: 3
t= 7, sum=27: 3
t= 8, sum=26: 3
t= 9, sum=25: 3
t=10, sum=24: 3
```

Thus the terminal endpoint `24` is not selected by APD vanishing.  It is
selected by bounded terminality.  APD/PTE explains the parity-power balance
and its deformation along the ray.

## Interpretation

The right sentence is:

```text
The Sagrada ray is a bounded deformation of the even/odd
permutation-diagonal PTE balance of Durer.
```

The wrong sentence is:

```text
24 is the APD-symmetric point.
```

At the terminal endpoint `t=10`, `APD_3` is nonzero.

## Morse-Hedlund / Prouhet Branch

Sergeyev's arXiv paper on symmetric exponential sums connects
Morse-Hedlund/Prouhet sequences with `4 x 4` magic-square constructions.  This
is a promising external bridge because it offers parametrized magic-square
families rather than ad hoc perturbations.

The current verified status is only:

```text
source exists and is relevant;
fit of Durer/Sagrada into the Morse-Hedlund family is OPEN.
```

Next local test:

1. encode the displayed Morse-Hedlund `4 x 4` family;
2. test Durer, Durer-complement, and Sagrada terminal matrices under square
   symmetries, complement, and row/column permutations;
3. decide whether the Sagrada ray is a specialization, a nearby ray, or
   unrelated to that family.

## Guardrails

Do not claim:

- `24` is selected by APD/PTE.
- the Morse-Hedlund/Prouhet family contains Durer/Sagrada before testing.
- APD/PTE replaces the bounded meet theorem.

The APD/PTE layer is a structural explanation of the permutation-diagonal
power-balance deformation.
