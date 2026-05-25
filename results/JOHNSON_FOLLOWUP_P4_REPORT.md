# Phase P4 Johnson Follow-Up

## Terminal-24 Code Profiles

```text
class_counts={'extra32': 32, 'outside_main': 60, 'exact_v4': 144}
```

### terminal_profile

```text
signature_counts={'exact_v4': 3, 'extra32': 6, 'outside_main': 15}
pairwise_intersections={'exact_v4__extra32': 0, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0}
```

- extra32:
  - count=8
    signature={"anchor_shadow_profile": {"1,1,1,1": 32, "2,1,1,0": 26, "2,2,0,0": 32, "3,1,0,0": 4, "4,0,0,0": 2}, "count": 96, "domain_direction_inventory": {"direction_relation_counts": {"complement": 4, "line": 2, "same": 1}, "non_domain_affine": 70, "quad_relation_counts": {"complement": 16, "line": 8, "same": 2}}, "inner_distribution": {"0": 1336, "1": 2058, "2": 1090, "3": 76}, "pair_degree_profiles": {"all": {"0": 4, "1": 2, "2": 6, "3": 14, "4": 29, "5": 25, "6": 11, "7": 21, "8": 6, "9": 2}, "different_anchor_block": {"0": 3, "1": 1, "2": 5, "3": 13, "4": 27, "5": 14, "6": 7, "7": 18, "8": 6, "9": 2}, "same_anchor_block": {"0": 1, "1": 1, "2": 1, "3": 1, "4": 2, "5": 11, "6": 4, "7": 3}}, "point_degree_profile": {"19": 1, "21": 2, "22": 3, "24": 2, "25": 3, "26": 2, "27": 2, "28": 1}}
  - count=8
    signature={"anchor_shadow_profile": {"1,1,1,1": 28, "2,1,1,0": 38, "2,2,0,0": 20, "3,1,0,0": 8, "4,0,0,0": 2}, "count": 96, "domain_direction_inventory": {"direction_relation_counts": {"complement": 4, "line": 2, "same": 1}, "non_domain_affine": 70, "quad_relation_counts": {"complement": 16, "line": 8, "same": 2}}, "inner_distribution": {"0": 1336, "1": 2058, "2": 1090, "3": 76}, "pair_degree_profiles": {"all": {"0": 4, "1": 2, "2": 6, "3": 14, "4": 29, "5": 25, "6": 11, "7": 21, "8": 6, "9": 2}, "different_anchor_block": {"0": 4, "1": 2, "2": 6, "3": 8, "4": 24, "5": 21, "6": 4, "7": 19, "8": 6, "9": 2}, "same_anchor_block": {"3": 6, "4": 5, "5": 4, "6": 7, "7": 2}}, "point_degree_profile": {"19": 1, "21": 2, "22": 3, "24": 2, "25": 3, "26": 2, "27": 2, "28": 1}}
  - count=4
    signature={"anchor_shadow_profile": {"1,1,1,1": 26, "2,1,1,0": 38, "2,2,0,0": 24, "3,1,0,0": 6, "4,0,0,0": 2}, "count": 96, "domain_direction_inventory": {"direction_relation_counts": {"complement": 4, "line": 4, "same": 1}, "non_domain_affine": 68, "quad_relation_counts": {"complement": 14, "line": 12, "same": 2}}, "inner_distribution": {"0": 1336, "1": 2058, "2": 1090, "3": 76}, "pair_degree_profiles": {"all": {"0": 4, "1": 2, "2": 6, "3": 14, "4": 29, "5": 25, "6": 11, "7": 21, "8": 6, "9": 2}, "different_anchor_block": {"0": 4, "1": 1, "2": 5, "3": 11, "4": 25, "5": 20, "6": 4, "7": 18, "8": 6, "9": 2}, "same_anchor_block": {"1": 1, "2": 1, "3": 3, "4": 4, "5": 5, "6": 7, "7": 3}}, "point_degree_profile": {"19": 1, "21": 2, "22": 3, "24": 2, "25": 3, "26": 2, "27": 2, "28": 1}}

- outside_main:
  - count=4
    signature={"anchor_shadow_profile": {"1,1,1,1": 19, "2,1,1,0": 61, "2,2,0,0": 18, "3,1,0,0": 11, "4,0,0,0": 2}, "count": 111, "domain_direction_inventory": {"direction_relation_counts": {"complement": 5, "line": 3, "same": 1}, "non_domain_affine": 84, "quad_relation_counts": {"complement": 15, "line": 10, "same": 2}}, "inner_distribution": {"0": 1745, "1": 2832, "2": 1433, "3": 95}, "pair_degree_profiles": {"all": {"0": 2, "1": 2, "2": 9, "4": 12, "5": 25, "6": 33, "7": 24, "8": 10, "9": 3}, "different_anchor_block": {"0": 2, "1": 2, "2": 8, "4": 9, "5": 20, "6": 28, "7": 16, "8": 9, "9": 2}, "same_anchor_block": {"2": 1, "4": 3, "5": 5, "6": 5, "7": 8, "8": 1, "9": 1}}, "point_degree_profile": {"22": 1, "25": 2, "26": 2, "27": 1, "28": 2, "29": 5, "30": 1, "31": 2}}
  - count=4
    signature={"anchor_shadow_profile": {"1,1,1,1": 21, "2,1,1,0": 62, "2,2,0,0": 10, "3,1,0,0": 12, "4,0,0,0": 2}, "count": 107, "domain_direction_inventory": {"direction_relation_counts": {"complement": 3, "line": 2, "same": 1}, "non_domain_affine": 85, "quad_relation_counts": {"complement": 12, "line": 8, "same": 2}}, "inner_distribution": {"0": 1637, "1": 2595, "2": 1346, "3": 93}, "pair_degree_profiles": {"all": {"0": 3, "1": 2, "2": 5, "3": 8, "4": 23, "5": 15, "6": 25, "7": 25, "8": 12, "9": 2}, "different_anchor_block": {"0": 3, "1": 2, "2": 5, "3": 4, "4": 19, "5": 11, "6": 20, "7": 20, "8": 11, "9": 1}, "same_anchor_block": {"3": 4, "4": 4, "5": 4, "6": 5, "7": 5, "8": 1, "9": 1}}, "point_degree_profile": {"20": 1, "23": 1, "24": 2, "26": 1, "27": 2, "28": 6, "29": 1, "30": 2}}
  - count=4
    signature={"anchor_shadow_profile": {"1,1,1,1": 20, "2,1,1,0": 50, "2,2,0,0": 16, "3,1,0,0": 7, "4,0,0,0": 2}, "count": 95, "domain_direction_inventory": {"direction_relation_counts": {"complement": 3, "line": 2, "same": 1}, "non_domain_affine": 73, "quad_relation_counts": {"complement": 12, "line": 8, "same": 2}}, "inner_distribution": {"0": 1287, "1": 2072, "2": 1027, "3": 79}, "pair_degree_profiles": {"all": {"0": 5, "1": 2, "2": 6, "3": 12, "4": 20, "5": 33, "6": 23, "7": 15, "8": 4}, "different_anchor_block": {"0": 4, "1": 1, "2": 5, "3": 10, "4": 19, "5": 22, "6": 19, "7": 14, "8": 2}, "same_anchor_block": {"0": 1, "1": 1, "2": 1, "3": 2, "4": 1, "5": 11, "6": 4, "7": 1, "8": 2}}, "point_degree_profile": {"18": 1, "22": 4, "23": 2, "24": 3, "25": 2, "26": 2, "27": 2}}

- exact_v4:
  - count=48
    signature={"anchor_shadow_profile": {"1,1,1,1": 16, "2,1,1,0": 48, "2,2,0,0": 20, "3,1,0,0": 8, "4,0,0,0": 4}, "count": 96, "domain_direction_inventory": {"direction_relation_counts": {"complement": 3, "line": 5, "same": 1}, "non_domain_affine": 60, "quad_relation_counts": {"complement": 12, "line": 20, "same": 4}}, "inner_distribution": {"0": 1336, "1": 2058, "2": 1090, "3": 76}, "pair_degree_profiles": {"all": {"0": 4, "1": 2, "2": 6, "3": 14, "4": 29, "5": 25, "6": 11, "7": 21, "8": 6, "9": 2}, "different_anchor_block": {"0": 4, "1": 2, "2": 6, "3": 12, "4": 24, "5": 21, "6": 8, "7": 13, "8": 4, "9": 2}, "same_anchor_block": {"3": 2, "4": 5, "5": 4, "6": 3, "7": 8, "8": 2}}, "point_degree_profile": {"19": 1, "21": 2, "22": 3, "24": 2, "25": 3, "26": 2, "27": 2, "28": 1}}
  - count=48
    signature={"anchor_shadow_profile": {"1,1,1,1": 16, "2,1,1,0": 48, "2,2,0,0": 20, "3,1,0,0": 8, "4,0,0,0": 4}, "count": 96, "domain_direction_inventory": {"direction_relation_counts": {"complement": 3, "line": 5, "same": 1}, "non_domain_affine": 60, "quad_relation_counts": {"complement": 12, "line": 20, "same": 4}}, "inner_distribution": {"0": 1336, "1": 2058, "2": 1090, "3": 76}, "pair_degree_profiles": {"all": {"0": 4, "1": 2, "2": 6, "3": 14, "4": 29, "5": 25, "6": 11, "7": 21, "8": 6, "9": 2}, "different_anchor_block": {"0": 4, "1": 2, "2": 4, "3": 14, "4": 25, "5": 20, "6": 9, "7": 12, "8": 4, "9": 2}, "same_anchor_block": {"2": 2, "4": 4, "5": 5, "6": 2, "7": 9, "8": 2}}, "point_degree_profile": {"19": 1, "21": 2, "22": 3, "24": 2, "25": 3, "26": 2, "27": 2, "28": 1}}
  - count=48
    signature={"anchor_shadow_profile": {"1,1,1,1": 16, "2,1,1,0": 48, "2,2,0,0": 20, "3,1,0,0": 8, "4,0,0,0": 4}, "count": 96, "domain_direction_inventory": {"direction_relation_counts": {"complement": 3, "line": 5, "same": 1}, "non_domain_affine": 60, "quad_relation_counts": {"complement": 12, "line": 20, "same": 4}}, "inner_distribution": {"0": 1336, "1": 2058, "2": 1090, "3": 76}, "pair_degree_profiles": {"all": {"0": 4, "1": 2, "2": 6, "3": 14, "4": 29, "5": 25, "6": 11, "7": 21, "8": 6, "9": 2}, "different_anchor_block": {"0": 4, "1": 2, "2": 6, "3": 14, "4": 23, "5": 16, "6": 9, "7": 18, "8": 4}, "same_anchor_block": {"4": 6, "5": 9, "6": 2, "7": 3, "8": 2, "9": 2}}, "point_degree_profile": {"19": 1, "21": 2, "22": 3, "24": 2, "25": 3, "26": 2, "27": 2, "28": 1}}

### terminal_affine_profile

```text
signature_counts={'exact_v4': 1, 'extra32': 2, 'outside_main': 12}
pairwise_intersections={'exact_v4__extra32': 0, 'exact_v4__outside_main': 0, 'extra32__outside_main': 0}
```

- extra32:
  - count=16
    signature={"anchor_shadow_profile": {"1,1,1,1": 16, "2,1,1,0": 12, "2,2,0,0": 8}, "count": 36, "domain_direction_inventory": {"direction_relation_counts": {"complement": 4, "line": 2}, "non_domain_affine": 12, "quad_relation_counts": {"complement": 16, "line": 8}}, "inner_distribution": {"0": 246, "1": 192, "2": 192}, "pair_degree_profiles": {"all": {"0": 24, "1": 24, "2": 48, "4": 24}, "different_anchor_block": {"0": 20, "1": 12, "2": 40, "4": 24}, "same_anchor_block": {"0": 4, "1": 12, "2": 8}}, "point_degree_profile": {"9": 16}}
  - count=16
    signature={"anchor_shadow_profile": {"1,1,1,1": 12, "2,1,1,0": 16, "2,2,0,0": 8}, "count": 36, "domain_direction_inventory": {"direction_relation_counts": {"complement": 3, "line": 2}, "non_domain_affine": 16, "quad_relation_counts": {"complement": 12, "line": 8}}, "inner_distribution": {"0": 246, "1": 192, "2": 192}, "pair_degree_profiles": {"all": {"0": 24, "1": 24, "2": 48, "4": 24}, "different_anchor_block": {"0": 20, "1": 16, "2": 36, "4": 24}, "same_anchor_block": {"0": 4, "1": 8, "2": 12}}, "point_degree_profile": {"9": 16}}

- outside_main:
  - count=8
    signature={"anchor_shadow_profile": {"1,1,1,1": 12, "2,1,1,0": 10, "2,2,0,0": 8, "4,0,0,0": 2}, "count": 32, "domain_direction_inventory": {"direction_relation_counts": {"complement": 3, "line": 2, "same": 1}, "non_domain_affine": 10, "quad_relation_counts": {"complement": 12, "line": 8, "same": 2}}, "inner_distribution": {"0": 171, "1": 189, "2": 136}, "pair_degree_profiles": {"all": {"0": 21, "1": 39, "2": 37, "3": 13, "4": 10}, "different_anchor_block": {"0": 18, "1": 31, "2": 26, "3": 13, "4": 8}, "same_anchor_block": {"0": 3, "1": 8, "2": 11, "4": 2}}, "point_degree_profile": {"10": 1, "11": 1, "6": 1, "7": 6, "8": 4, "9": 3}}
  - count=8
    signature={"anchor_shadow_profile": {"1,1,1,1": 12, "2,1,1,0": 15, "2,2,0,0": 8}, "count": 35, "domain_direction_inventory": {"direction_relation_counts": {"complement": 3, "line": 2}, "non_domain_affine": 15, "quad_relation_counts": {"complement": 12, "line": 8}}, "inner_distribution": {"0": 217, "1": 206, "2": 172}, "pair_degree_profiles": {"all": {"0": 15, "1": 51, "2": 19, "3": 19, "4": 16}, "different_anchor_block": {"0": 13, "1": 36, "2": 14, "3": 17, "4": 16}, "same_anchor_block": {"0": 2, "1": 15, "2": 5, "3": 2}}, "point_degree_profile": {"10": 1, "11": 1, "7": 2, "8": 3, "9": 9}}
  - count=8
    signature={"anchor_shadow_profile": {"1,1,1,1": 8, "2,1,1,0": 13, "2,2,0,0": 8}, "count": 29, "domain_direction_inventory": {"direction_relation_counts": {"complement": 2, "line": 3}, "non_domain_affine": 13, "quad_relation_counts": {"complement": 8, "line": 8}}, "inner_distribution": {"0": 150, "1": 140, "2": 116}, "pair_degree_profiles": {"all": {"0": 25, "1": 43, "2": 35, "3": 7, "4": 10}, "different_anchor_block": {"0": 21, "1": 32, "2": 26, "3": 7, "4": 10}, "same_anchor_block": {"0": 4, "1": 11, "2": 9}}, "point_degree_profile": {"5": 1, "6": 3, "7": 5, "8": 5, "9": 2}}

- exact_v4:
  - count=144
    signature={"anchor_shadow_profile": {"1,1,1,1": 12, "2,2,0,0": 20, "4,0,0,0": 4}, "count": 36, "domain_direction_inventory": {"direction_relation_counts": {"complement": 3, "line": 5, "same": 1}, "non_domain_affine": 0, "quad_relation_counts": {"complement": 12, "line": 20, "same": 4}}, "inner_distribution": {"0": 246, "1": 192, "2": 192}, "pair_degree_profiles": {"all": {"0": 24, "1": 24, "2": 48, "4": 24}, "different_anchor_block": {"0": 24, "1": 24, "2": 32, "4": 16}, "same_anchor_block": {"2": 16, "4": 8}}, "point_degree_profile": {"9": 16}}

## O5e Collision Stratification

```text
fiber_count=144
distinct_point_map_count_distribution={'16': 32, '20': 16, '24': 96}
```

The tested coarse fields by collision type are recorded in the JSON.
No single tested coarse field explains the complete `24/20/16`
split for every fiber by itself.  The selected-plane directions
fall into three regimes:

```text
0,1,2,3: {'24': 24}
0,1,4,5: {'16': 8, '24': 16}
0,1,8,9: {'16': 8, '20': 8, '24': 8}
0,2,4,6: {'16': 8, '20': 8, '24': 8}
0,2,8,10: {'16': 8, '24': 16}
0,4,8,12: {'24': 24}
```

Moreover, the joint key
`(selected_plane_direction, translation_direction)` classifies the
collision type with no ambiguity:

```text
joint_key_count=36
ambiguous_joint_key_count=0
```

## Interpretation

P4 confirms that the exact `144` terminal-affine layer is a uniform
small constant-weight code relative to the fixed translation spread:
its inner distribution, point degrees, pair degrees, anchor shadow,
and direction inventory all collapse to one signature.  The `32`
extras and the `60` outside-main records do not collapse to that
signature.

The O5e collision split remains mask-refined, but it is no longer
opaque: the selected-plane direction gives three coarse regimes,
and adding the translation direction determines the exact collision
type.
