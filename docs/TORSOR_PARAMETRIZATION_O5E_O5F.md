# O5e/O5f Torsor Parametrization Audit

Status: Phase O5e/O5f follow-up audit, outside the paper

## Purpose

O5d shows a uniform split:

```text
3456 = 24 selected value planes x 6 invertible directions x 24 records.
```

The natural next conjecture was that the last factor `24` is always the full
`AGL(2,2)` set of affine bijections from the fixed translation plane to the
selected value plane.

This note tests that conjecture.

Replay artifacts:

```text
scripts/analyze_torsor_parametrization_o5e_o5f.py
tests/test_torsor_parametrization_o5e_o5f.py
results/torsor_parametrization_o5e_o5f.json
results/TORSOR_PARAMETRIZATION_O5E_O5F_REPORT.md
```

## Coarse Fiber Count

The coarse count is correct:

```text
affine square-mask pairs: 3456
(P,W) fibers: 144
records per (P,W): 24
```

Here `P` is a selected value plane and `W` is one of the six invertible graph
complements used by that plane.

## Naive AGL Claim

The naive claim fails:

```text
record = (P, W, phi)
```

where `phi` is only the affine point-map from translation labels to the four
points of `P`.

The distinct point-map counts per `(P,W)` fiber are:

```text
24 maps: 96 fibers
20 maps: 16 fibers
16 maps: 32 fibers
```

Thus only `96` of the `144` fibers realize all `24` affine bijections and
carry the naive `AGL(2,2)` torsor on `phi`.

## Corrected Statement

The mask-refined key is injective:

```text
(P, W, phi, mask)
```

For every `(P,W)` fiber:

```text
distinct (phi,mask) pairs: 24
```

and globally:

```text
global refined keys: 3456
```

So the final `24` factor is real, but it is a **mask-refined incidence
fiber**, not uniformly the pure `AGL(2,2)` point-map torsor.

## Guardrail

Do not claim:

```text
3456 = 24 x 6 x |AGL(2,2)|
```

as a global parametrization by `(P,W,phi)` alone.  The safe statement is:

```text
3456 = 24 selected planes x 6 invertible directions x 24 mask-refined records.
```
