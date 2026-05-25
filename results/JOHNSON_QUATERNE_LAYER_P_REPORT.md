# Phase P Johnson Quaterne Layer

## Durer/Sagrada Replay

```text
H34 Johnson strata: {'0': 19, '1': 50, '2': 17, '3': 0, '4': 0}
H34 affine strata: {'0': 8, '1': 36, '2': 8, '3': 0, '4': 0}
Terminal decomposition: {'source_24_incidence_0': 25, 'source_34_incidence_1': 50, 'source_44_incidence_2': 21}
Terminal affine decomposition: {'source_34_incidence_1': 36}
```

## Atlas Class Counts

```text
{"exact_v4": 144, "extra32": 32, "outside_main": 60}
```

## Separation Tests

```text
source_h34_johnson_strata: counts={'exact_v4': 1, 'extra32': 1, 'outside_main': 7} intersections={'exact_v4__extra32': 1, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} main_vs_outside=True exact_vs_extra=False separates_all=False
source_h34_affine_johnson_strata: counts={'exact_v4': 1, 'extra32': 1, 'outside_main': 3} intersections={'exact_v4__extra32': 1, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} main_vs_outside=True exact_vs_extra=False separates_all=False
terminal_johnson_strata: counts={'exact_v4': 1, 'extra32': 1, 'outside_main': 7} intersections={'exact_v4__extra32': 1, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} main_vs_outside=True exact_vs_extra=False separates_all=False
terminal_decomposition: counts={'exact_v4': 1, 'extra32': 1, 'outside_main': 7} intersections={'exact_v4__extra32': 1, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} main_vs_outside=True exact_vs_extra=False separates_all=False
terminal_affine_johnson_strata: counts={'exact_v4': 1, 'extra32': 1, 'outside_main': 6} intersections={'exact_v4__extra32': 1, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} main_vs_outside=True exact_vs_extra=False separates_all=False
terminal_affine_decomposition: counts={'exact_v4': 1, 'extra32': 1, 'outside_main': 6} intersections={'exact_v4__extra32': 1, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} main_vs_outside=True exact_vs_extra=False separates_all=False
terminal_inner_profile: counts={'exact_v4': 1, 'extra32': 1, 'outside_main': 8} intersections={'exact_v4__extra32': 1, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} main_vs_outside=True exact_vs_extra=False separates_all=False
terminal_affine_inner_profile: counts={'exact_v4': 1, 'extra32': 1, 'outside_main': 5} intersections={'exact_v4__extra32': 1, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0} main_vs_outside=True exact_vs_extra=False separates_all=False
```

## Interpretation

The Johnson stratum identity cleanly explains quaterne transport by
`|Q cap M|`.  The first atlas pass records whether these profiles
separate the `144` exact class, the `32` selected-affine extras, and
the remaining `60` outside-main records.  If a profile has nonzero
pairwise intersections, it is useful language but not a classifier.

Current result: the tested Johnson profiles separate the main
`176 = 144 + 32` selected-affine signature from the `60` outside-main
records, but they do not separate the `144` exact-`V4` records from
the `32` selected-affine extras.
