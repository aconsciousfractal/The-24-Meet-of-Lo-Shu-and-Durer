# O5e/O5f Torsor Parametrization Audit

Status: Phase O5e/O5f follow-up audit, outside the paper

## Question

Do the `3456` affine square-mask pairs admit the clean parametrization

```text
selected plane P x invertible direction W x affine bijection phi
```

with the last factor equal to the full `AGL(2,2)` set of `24` affine
bijections?

## Verdict

Not in this naive form.

The coarse fiber count is correct:

- affine square-mask pairs: `3456`
- `(P,W)` fibers: `144`
- fiber sizes: `{'24': 144}`

But `phi` alone is not always injective in a `(P,W)` fiber:

- distinct point-map counts: `{'16': 32, '20': 16, '24': 96}`
- naive `(P,W,phi)` parametrization holds: `False`
- AGL torsor fibers: `{'False': 48, 'True': 96}`
- AGL torsor holds for all fibers: `False`

Only `96` of the `144` fibers realize all `24` affine bijections.

## Corrected Finite Statement

The mask-refined key is injective:

```text
(P, W, phi, mask)
```

- point-map/mask pair counts: `{'24': 144}`
- mask-refined parametrization holds: `True`
- global refined key count: `3456`

Thus the final `24` factor is real, but it is not uniformly the
`24` affine point maps.  It is a mask-refined incidence fiber.

## Guardrail

Do not claim a global `P x W x AGL(2,2)` parametrization of the
`3456` affine square-mask pairs.  The `AGL(2,2)` reading is valid for
a large subfamily (`96` fibers) but not all fibers.
