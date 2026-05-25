# F2 Family Controls

Status: Phase F control-branch audit

## Purpose

This note tests whether the `F2^4` fingerprints separate the
Durer/Sagrada-associated branch from the panmagic/most-perfect-proxy control
branch.

The replay artifacts are:

```text
scripts/analyze_f2_family_controls.py
tests/test_f2_family_controls.py
results/f2_family_controls.json
results/F2_FAMILY_CONTROL_REPORT.md
```

## Main Result

At the current `F2^4` resolution, the associated branch and the
panmagic/most-perfect-proxy branch have the same terminal-24 profile:

```text
associated:
  squares: 48
  affine cell-labeling squares: 48/48
  terminal-24 pairs: 16
  affine cell-labeling terminal-24 pairs: 16
  selected-mask affine terminal-24 pairs: 16
  exact canonical V4 terminal-24 pairs: 16
  pure transport terminal-24 pairs: 16
  terminal affine count: 36 in all 16

most-perfect-proxy:
  squares: 48
  affine cell-labeling squares: 48/48
  terminal-24 pairs: 16
  affine cell-labeling terminal-24 pairs: 16
  selected-mask affine terminal-24 pairs: 16
  exact canonical V4 terminal-24 pairs: 16
  pure transport terminal-24 pairs: 16
  terminal affine count: 36 in all 16
```

Thus the `F2^4` layer confirms the exact-canonical-`V4` structure, but does
not separate the Durer/Sagrada associated branch from the panmagic /
most-perfect-proxy branch.

## Complement-Fixed Control

The larger complement-fixed family is mixed:

```text
complement-fixed squares: 352
affine cell-labeling squares: 144
terminal-24 pairs: 84
affine cell-labeling terminal-24 pairs: 48
selected-mask affine terminal-24 pairs: 56
exact canonical V4 terminal-24 pairs: 48
pure transport terminal-24 pairs: 60
```

Its terminal affine count distribution is:

```text
30: 4
31: 4
32: 16
35: 4
36: 56
```

So complement-fixed is too broad for the clean `F2^4` fingerprint.

## Interpretation

This is a guardrail with useful content:

```text
F2^4 affine structure tracks exact canonical V4.
F2^4 affine structure does not distinguish associated from panmagic controls.
```

For the final paper, this means the Durer/Sagrada 8-cell still needs its
associated/complement-fixed placement, APD/source-type quotient, and
non-panmagic guardrail.  The `F2^4` layer should be presented as a structural
layer for exact `V4`, not as a full classifier of the Durer/Sagrada branch.

## Guardrails

Do not claim:

- `F2^4` distinguishes associated from panmagic/most-perfect endpoint-24
  controls;
- affine cell-value labeling is a Durer/Sagrada-only fingerprint;
- exact canonical `V4` is the same as the associated branch.

The correct statement is:

```text
The terminal-24 exact canonical V4 pairs have a uniform F2^4 affine profile,
and both the associated and panmagic/most-perfect control branches contribute
16 such pairs.
```
