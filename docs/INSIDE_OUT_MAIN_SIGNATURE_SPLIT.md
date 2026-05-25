# Inside-Out Main Signature Split

Status: Phase H refinement of the `176`-pair main terminal signature.

The Phase-H terminal-24 inside-out extension found a large main terminal
signature:

```text
edges = 107
rank_Q = 16
rank_F2 = 14
SNF = 1^14,2,20
terminal quaterne count = 96
```

This note splits that class.

## Main Split

```text
main inside-out terminal signature: 176 pairs
exact canonical V4 pairs: 144
extra non-exact-canonical-V4 pairs: 32
```

The exact canonical `V4` part has:

```text
terminal set: 0123,1032,2301,3210 in all 144 cases
terminal order profile: 1:1,2:3 in all 144 cases
source types: S1:96, S2:16, S3:16, S4:16
associated: 16
panmagic / most-perfect-proxy: 16
complement-fixed: 48
```

The `32` extra pairs have:

```text
selected values: {11,12,15,16} in all 32 cases
terminal subgroup: true in all 32 cases
source type: outside exact-V4 source types in all 32 cases
associated: 0
panmagic / most-perfect-proxy: 0
complement-fixed: 8
```

Their terminal sets split as:

```text
0123,3210:                16
0123,0213,3120,3210:      8
0123,1302,2031,3210:      8
```

Their terminal order profiles split as:

```text
1:1,2:1:       16
1:1,2:1,4:2:    8
1:1,2:3:        8
```

Their source diagonal sizes split as:

```text
2: 12
4: 20
```

## Interpretation

The main inside-out signature is exactly the selected-mask-affine terminal-24
class, but it is broader than exact canonical `V4`.

The next useful refinement is now very concrete:

```text
selected-mask affine terminal-24 pairs: 176
  exact canonical V4: 144
  subgroup terminal but outside exact-V4 source types: 32
```

This says that selected-mask affineness plus inside-out SNF/parity is still
not enough to isolate the exact canonical `V4` subclass.  However, the
remaining gap is small and structured: the 32 extra pairs are all terminal
subgroups, all have selected values `{11,12,15,16}`, and none lies in the
associated or panmagic/most-perfect proxy branches.

## Guardrail

Do not claim:

```text
the main inside-out signature is exact canonical V4;
the 32 extra pairs are noise;
the split gives a Hilbert or Markov characterization;
the Durer/Sagrada 8-cell is isolated by this invariant.
```

The established claim is a stratification:

```text
236 terminal-24
  -> 176 selected-mask-affine / main inside-out signature
      -> 144 exact canonical V4 + 32 structured subgroup extras
```

## Artifacts

```text
scripts/analyze_inside_out_main_signature_split.py
tests/test_inside_out_main_signature_split.py
results/inside_out_main_signature_split.json
results/INSIDE_OUT_MAIN_SIGNATURE_SPLIT_REPORT.md
```
