# Phase P - Johnson Quaterne Layer

Status: first audit complete.

## Question

The Phase P question was whether the quaterne layer should be read inside the
Johnson scheme `J(16,4)`.

For a selected mask `M`, define:

```text
J_i(M) = {Q subset cells : |Q| = 4 and |Q cap M| = i}.
```

The transport identity is:

```text
sum_Q(A - tM) = sum_Q(A) - t |Q cap M|.
```

So every transported quaterne count is automatically stratified by the
Johnson intersection number with the mask.

## Durer/Sagrada Replay

For the Durer/Sagrada mask:

```text
H_34(D) Johnson strata:
  |Q cap M| = 0,1,2,3,4 -> 19,50,17,0,0

affine H_34(D) strata:
  |Q cap M| = 0,1,2,3,4 -> 8,36,8,0,0

terminal H_24(D(10)) decomposition:
  source 24 / incidence 0 -> 25
  source 34 / incidence 1 -> 50
  source 44 / incidence 2 -> 21

terminal affine decomposition:
  source 34 / incidence 1 -> 36
```

This makes the quaterne transport formula transparent: the terminal target is
controlled by the Johnson stratum `|Q cap M|`.

## Atlas Result

The terminal-24 atlas splits as:

```text
exact_v4:     144
extra32:       32
outside_main:  60
```

The tested Johnson profiles include:

```text
source H34 strata
source H34 affine strata
terminal strata
terminal decomposition by source sum and incidence
terminal affine strata
terminal affine decomposition
terminal inner Johnson intersection profile
terminal affine inner Johnson intersection profile
```

Result:

```text
All tested Johnson profiles separate:
  176 = 144 exact_v4 + 32 extra32
from:
  60 outside_main records.

No tested Johnson profile separates:
  144 exact_v4
from:
  32 selected-affine extras.
```

In particular, the `144` exact records and the `32` extras share the same
basic terminal Johnson signatures:

```text
terminal decomposition:
  source_24_incidence_0 -> 25
  source_34_incidence_1 -> 50
  source_44_incidence_2 -> 21

terminal affine decomposition:
  source_34_incidence_1 -> 36

terminal inner profile:
  intersection 0,1,2,3,4 -> 1336,2058,1090,76,0

terminal affine inner profile:
  intersection 0,1,2,3,4 -> 246,192,192,0,0
```

## Interpretation

The Johnson scheme is useful, but its first-pass role is bounded:

```text
positive:
  It gives the right language for quaterne transport and separates the main
  176-pair selected-affine signature from the outside-main records.

negative:
  It does not explain the exact-V4 / extra32 boundary.
```

So Phase P is not a new characterization of the `144` exact class. It is a
clean set-system language for the `176` main signature and for the transport
formula.

## Artifacts

```text
scripts/analyze_johnson_quaterne_layer_p.py
tests/test_johnson_quaterne_layer_p.py
results/johnson_quaterne_layer_p.json
results/JOHNSON_QUATERNE_LAYER_P_REPORT.md
```
