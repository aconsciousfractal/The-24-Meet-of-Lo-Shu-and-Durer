# Phase P2 Anchored Johnson Refinement

## Class Counts

```text
{"exact_v4": 144, "extra32": 32, "outside_main": 60}
```

## Terminal Set Sizes

```text
{"exact_v4": {"4": 144}, "extra32": {"2": 16, "4": 16}, "outside_main": {"2": 36, "3": 12, "4": 8, "5": 4}}
```

## Profile Separation

```text
fixed_translation_terminal_anchor_profile: counts={'exact_v4': 1, 'extra32': 4, 'outside_main': 14} intersections={'exact_v4__extra32': 0, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} exact_vs_extra=True all=True
fixed_translation_terminal_affine_anchor_profile: counts={'exact_v4': 1, 'extra32': 2, 'outside_main': 11} intersections={'exact_v4__extra32': 0, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} exact_vs_extra=True all=True
record_terminal_anchor_profile: counts={'exact_v4': 1, 'extra32': 4, 'outside_main': 15} intersections={'exact_v4__extra32': 0, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} exact_vs_extra=True all=True
record_terminal_affine_anchor_profile: counts={'exact_v4': 1, 'extra32': 3, 'outside_main': 15} intersections={'exact_v4__extra32': 0, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} exact_vs_extra=True all=True
```

## Interpretation

The mask-only Johnson profiles from P1 do not separate `144` from
`32`.  Anchoring the terminal quaterne family against the fixed
translation `V4 = {0123,1032,2301,3210}` does separate the exact
`V4` class, the selected-affine extras, and the outside-main records.

This is a real refinement, but it uses the O5 translation anchor.  It
should be described as anchored Johnson/association-scheme data, not
as a mask-only Johnson invariant.
