# Inside-Out Main Signature Split

Status: Phase H refinement of the 176-pair main terminal signature

## Summary

- main signature pairs: `176`
- exact canonical `V4` pairs: `144`
- extra non-exact-canonical-`V4` pairs: `32`
- main profile: `{'edge_count': 107, 'left_dependencies_Q': 91, 'rank_F2': 14, 'rank_Q': 16, 'right_kernel_Q': 0, 'snf_counts': {'1': 14, '2': 1, '20': 1}}`

## Exact V4 vs Extra

Exact canonical `V4`:

`{'pair_count': 144, 'square_count': 144, 'mask_counts': {'1203': 4, '1320': 12, '2013': 44, '2130': 24, '3021': 36, '3102': 24}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 144}, 'apd_counts': {'(0,0,0,-288768)': 24, '(0,0,0,-290304)': 24, '(0,0,0,102912)': 24, '(0,0,0,55296)': 24, '(0,0,0,79872)': 48}, 'source_diagonal_size_counts': {'4': 96, '8': 48}, 'terminal_diagonal_size_counts': {'4': 144}, 'terminal_subgroup_counts': {'True': 144}, 'terminal_order_profile_counts': {'1:1,2:3': 144}, 'terminal_set_counts': {'0123,1032,2301,3210': 144}, 'source_type_counts': {'S1': 96, 'S2': 16, 'S3': 16, 'S4': 16}, 'family_flag_counts': {'associated': 16, 'complement_fixed': 48, 'local_2x2': 16, 'most_perfect_proxy': 16, 'panmagic': 16, 'wrap_2x2': 16}, 'square_indices': [16, 17, 21, 23, 26, 30, 31, 34, 72, 76, 81, 84, 89, 91, 95, 96, 101, 102, 109, 112, 113, 116, 123, 124, 136, 140, 145, 147, 172, 174, 176, 181, 190, 195, 200, 205, 213, 215, 224, 225, 227, 230, 232, 236, 278, 281, 286, 289, 300, 304, 305, 308, 309, 312, 315, 321, 323, 324, 328, 329, 333, 341, 343, 349, 359, 361, 366, 371, 392, 394, 398, 401, 419, 420, 423, 424, 431, 435, 442, 445, 460, 461, 464, 465, 475, 476, 480, 482, 536, 539, 548, 552, 557, 564, 565, 571, 575, 576, 581, 582, 588, 591, 598, 603, 627, 632, 641, 645, 657, 658, 661, 662, 698, 703, 719, 721, 729, 734, 740, 747, 770, 773, 777, 778, 783, 784, 789, 790, 797, 802, 805, 808, 826, 827, 834, 835, 839, 841, 842, 843, 849, 852, 853, 858]}`

Extra non-exact-canonical `V4`:

`{'pair_count': 32, 'square_count': 32, 'mask_counts': {'1320': 3, '2013': 8, '2130': 5, '3021': 9, '3102': 7}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 32}, 'apd_counts': {'(0,0,-9216,-1253376)': 4, '(0,0,-9216,-1256448)': 4, '(0,0,0,141312)': 4, '(0,0,0,156672)': 4, '(0,0,12288,1671168)': 8, '(0,0,3072,417792)': 8}, 'source_diagonal_size_counts': {'2': 12, '4': 20}, 'terminal_diagonal_size_counts': {'2': 16, '4': 16}, 'terminal_subgroup_counts': {'True': 32}, 'terminal_order_profile_counts': {'1:1,2:1': 16, '1:1,2:1,4:2': 8, '1:1,2:3': 8}, 'terminal_set_counts': {'0123,0213,3120,3210': 8, '0123,1302,2031,3210': 8, '0123,3210': 16}, 'source_type_counts': {'outside_exact_v4_source_types': 32}, 'family_flag_counts': {'associated': 0, 'complement_fixed': 8, 'local_2x2': 0, 'most_perfect_proxy': 0, 'panmagic': 0, 'wrap_2x2': 0}, 'square_indices': [5, 78, 87, 93, 133, 143, 201, 204, 238, 244, 348, 370, 411, 415, 416, 537, 550, 554, 578, 610, 630, 649, 654, 688, 699, 735, 782, 795, 829, 830, 846, 855]}`

## Source Types

### S1

`{'pair_count': 96, 'square_count': 96, 'mask_counts': {'1203': 2, '1320': 10, '2013': 26, '2130': 16, '3021': 24, '3102': 18}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 96}, 'apd_counts': {'(0,0,0,-288768)': 24, '(0,0,0,102912)': 24, '(0,0,0,79872)': 48}, 'source_diagonal_size_counts': {'4': 96}, 'terminal_diagonal_size_counts': {'4': 96}, 'terminal_subgroup_counts': {'True': 96}, 'terminal_order_profile_counts': {'1:1,2:3': 96}, 'terminal_set_counts': {'0123,1032,2301,3210': 96}, 'source_type_counts': {'S1': 96}, 'family_flag_counts': {'associated': 0, 'complement_fixed': 32, 'local_2x2': 0, 'most_perfect_proxy': 0, 'panmagic': 0, 'wrap_2x2': 0}, 'square_indices': [16, 17, 23, 30, 31, 34, 72, 76, 84, 91, 95, 96, 102, 109, 113, 124, 136, 140, 145, 147, 172, 181, 190, 195, 215, 224, 225, 227, 230, 236, 281, 286, 300, 308, 309, 312, 321, 324, 328, 329, 333, 341, 343, 349, 361, 366, 398, 401, 419, 423, 424, 431, 435, 442, 460, 461, 465, 476, 480, 539, 548, 552, 565, 571, 575, 576, 581, 588, 598, 603, 632, 641, 657, 658, 662, 698, 719, 721, 729, 734, 770, 773, 777, 783, 790, 797, 805, 808, 826, 835, 839, 841, 842, 852, 853, 858]}`

### S2

`{'pair_count': 16, 'square_count': 16, 'mask_counts': {'2013': 4, '2130': 6, '3021': 2, '3102': 4}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 16}, 'apd_counts': {'(0,0,0,-290304)': 8, '(0,0,0,55296)': 8}, 'source_diagonal_size_counts': {'8': 16}, 'terminal_diagonal_size_counts': {'4': 16}, 'terminal_subgroup_counts': {'True': 16}, 'terminal_order_profile_counts': {'1:1,2:3': 16}, 'terminal_set_counts': {'0123,1032,2301,3210': 16}, 'source_type_counts': {'S2': 16}, 'family_flag_counts': {'associated': 0, 'complement_fixed': 0, 'local_2x2': 0, 'most_perfect_proxy': 0, 'panmagic': 0, 'wrap_2x2': 0}, 'square_indices': [21, 26, 81, 89, 213, 232, 315, 323, 420, 445, 464, 582, 591, 661, 778, 843]}`

### S3

`{'pair_count': 16, 'square_count': 16, 'mask_counts': {'1203': 2, '2013': 10, '3021': 2, '3102': 2}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 16}, 'apd_counts': {'(0,0,0,-290304)': 8, '(0,0,0,55296)': 8}, 'source_diagonal_size_counts': {'8': 16}, 'terminal_diagonal_size_counts': {'4': 16}, 'terminal_subgroup_counts': {'True': 16}, 'terminal_order_profile_counts': {'1:1,2:3': 16}, 'terminal_set_counts': {'0123,1032,2301,3210': 16}, 'source_type_counts': {'S3': 16}, 'family_flag_counts': {'associated': 16, 'complement_fixed': 16, 'local_2x2': 0, 'most_perfect_proxy': 0, 'panmagic': 0, 'wrap_2x2': 0}, 'square_indices': [112, 123, 174, 205, 289, 305, 359, 394, 475, 557, 627, 740, 789, 802, 834, 849]}`

### S4

`{'pair_count': 16, 'square_count': 16, 'mask_counts': {'1320': 2, '2013': 4, '2130': 2, '3021': 8}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 16}, 'apd_counts': {'(0,0,0,-290304)': 8, '(0,0,0,55296)': 8}, 'source_diagonal_size_counts': {'8': 16}, 'terminal_diagonal_size_counts': {'4': 16}, 'terminal_subgroup_counts': {'True': 16}, 'terminal_order_profile_counts': {'1:1,2:3': 16}, 'terminal_set_counts': {'0123,1032,2301,3210': 16}, 'source_type_counts': {'S4': 16}, 'family_flag_counts': {'associated': 0, 'complement_fixed': 0, 'local_2x2': 16, 'most_perfect_proxy': 16, 'panmagic': 16, 'wrap_2x2': 16}, 'square_indices': [101, 116, 176, 200, 278, 304, 371, 392, 482, 536, 564, 645, 703, 747, 784, 827]}`

### outside_exact_v4_source_types

`{'pair_count': 32, 'square_count': 32, 'mask_counts': {'1320': 3, '2013': 8, '2130': 5, '3021': 9, '3102': 7}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 32}, 'apd_counts': {'(0,0,-9216,-1253376)': 4, '(0,0,-9216,-1256448)': 4, '(0,0,0,141312)': 4, '(0,0,0,156672)': 4, '(0,0,12288,1671168)': 8, '(0,0,3072,417792)': 8}, 'source_diagonal_size_counts': {'2': 12, '4': 20}, 'terminal_diagonal_size_counts': {'2': 16, '4': 16}, 'terminal_subgroup_counts': {'True': 32}, 'terminal_order_profile_counts': {'1:1,2:1': 16, '1:1,2:1,4:2': 8, '1:1,2:3': 8}, 'terminal_set_counts': {'0123,0213,3120,3210': 8, '0123,1302,2031,3210': 8, '0123,3210': 16}, 'source_type_counts': {'outside_exact_v4_source_types': 32}, 'family_flag_counts': {'associated': 0, 'complement_fixed': 8, 'local_2x2': 0, 'most_perfect_proxy': 0, 'panmagic': 0, 'wrap_2x2': 0}, 'square_indices': [5, 78, 87, 93, 133, 143, 201, 204, 238, 244, 348, 370, 411, 415, 416, 537, 550, 554, 578, 610, 630, 649, 654, 688, 699, 735, 782, 795, 829, 830, 846, 855]}`

## Family Slices

### associated

`{'pair_count': 16, 'square_count': 16, 'mask_counts': {'1203': 2, '2013': 10, '3021': 2, '3102': 2}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 16}, 'apd_counts': {'(0,0,0,-290304)': 8, '(0,0,0,55296)': 8}, 'source_diagonal_size_counts': {'8': 16}, 'terminal_diagonal_size_counts': {'4': 16}, 'terminal_subgroup_counts': {'True': 16}, 'terminal_order_profile_counts': {'1:1,2:3': 16}, 'terminal_set_counts': {'0123,1032,2301,3210': 16}, 'source_type_counts': {'S3': 16}, 'family_flag_counts': {'associated': 16, 'complement_fixed': 16, 'local_2x2': 0, 'most_perfect_proxy': 0, 'panmagic': 0, 'wrap_2x2': 0}, 'square_indices': [112, 123, 174, 205, 289, 305, 359, 394, 475, 557, 627, 740, 789, 802, 834, 849]}`

### complement_fixed

`{'pair_count': 56, 'square_count': 56, 'mask_counts': {'1203': 2, '1320': 5, '2013': 14, '2130': 10, '3021': 15, '3102': 10}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 56}, 'apd_counts': {'(0,0,0,-288768)': 8, '(0,0,0,-290304)': 8, '(0,0,0,102912)': 8, '(0,0,0,141312)': 4, '(0,0,0,156672)': 4, '(0,0,0,55296)': 8, '(0,0,0,79872)': 16}, 'source_diagonal_size_counts': {'2': 8, '4': 32, '8': 16}, 'terminal_diagonal_size_counts': {'2': 8, '4': 48}, 'terminal_subgroup_counts': {'True': 56}, 'terminal_order_profile_counts': {'1:1,2:1': 8, '1:1,2:3': 48}, 'terminal_set_counts': {'0123,1032,2301,3210': 48, '0123,3210': 8}, 'source_type_counts': {'S1': 32, 'S3': 16, 'outside_exact_v4_source_types': 8}, 'family_flag_counts': {'associated': 16, 'complement_fixed': 56, 'local_2x2': 0, 'most_perfect_proxy': 0, 'panmagic': 0, 'wrap_2x2': 0}, 'square_indices': [5, 16, 17, 72, 76, 78, 109, 112, 123, 124, 133, 136, 143, 174, 181, 205, 224, 225, 286, 289, 305, 308, 309, 312, 341, 359, 366, 394, 431, 435, 475, 476, 539, 557, 598, 603, 610, 627, 630, 632, 698, 740, 770, 773, 789, 790, 802, 805, 829, 834, 835, 839, 841, 849, 855, 858]}`

### local_2x2

`{'pair_count': 16, 'square_count': 16, 'mask_counts': {'1320': 2, '2013': 4, '2130': 2, '3021': 8}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 16}, 'apd_counts': {'(0,0,0,-290304)': 8, '(0,0,0,55296)': 8}, 'source_diagonal_size_counts': {'8': 16}, 'terminal_diagonal_size_counts': {'4': 16}, 'terminal_subgroup_counts': {'True': 16}, 'terminal_order_profile_counts': {'1:1,2:3': 16}, 'terminal_set_counts': {'0123,1032,2301,3210': 16}, 'source_type_counts': {'S4': 16}, 'family_flag_counts': {'associated': 0, 'complement_fixed': 0, 'local_2x2': 16, 'most_perfect_proxy': 16, 'panmagic': 16, 'wrap_2x2': 16}, 'square_indices': [101, 116, 176, 200, 278, 304, 371, 392, 482, 536, 564, 645, 703, 747, 784, 827]}`

### most_perfect_proxy

`{'pair_count': 16, 'square_count': 16, 'mask_counts': {'1320': 2, '2013': 4, '2130': 2, '3021': 8}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 16}, 'apd_counts': {'(0,0,0,-290304)': 8, '(0,0,0,55296)': 8}, 'source_diagonal_size_counts': {'8': 16}, 'terminal_diagonal_size_counts': {'4': 16}, 'terminal_subgroup_counts': {'True': 16}, 'terminal_order_profile_counts': {'1:1,2:3': 16}, 'terminal_set_counts': {'0123,1032,2301,3210': 16}, 'source_type_counts': {'S4': 16}, 'family_flag_counts': {'associated': 0, 'complement_fixed': 0, 'local_2x2': 16, 'most_perfect_proxy': 16, 'panmagic': 16, 'wrap_2x2': 16}, 'square_indices': [101, 116, 176, 200, 278, 304, 371, 392, 482, 536, 564, 645, 703, 747, 784, 827]}`

### panmagic

`{'pair_count': 16, 'square_count': 16, 'mask_counts': {'1320': 2, '2013': 4, '2130': 2, '3021': 8}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 16}, 'apd_counts': {'(0,0,0,-290304)': 8, '(0,0,0,55296)': 8}, 'source_diagonal_size_counts': {'8': 16}, 'terminal_diagonal_size_counts': {'4': 16}, 'terminal_subgroup_counts': {'True': 16}, 'terminal_order_profile_counts': {'1:1,2:3': 16}, 'terminal_set_counts': {'0123,1032,2301,3210': 16}, 'source_type_counts': {'S4': 16}, 'family_flag_counts': {'associated': 0, 'complement_fixed': 0, 'local_2x2': 16, 'most_perfect_proxy': 16, 'panmagic': 16, 'wrap_2x2': 16}, 'square_indices': [101, 116, 176, 200, 278, 304, 371, 392, 482, 536, 564, 645, 703, 747, 784, 827]}`

### wrap_2x2

`{'pair_count': 16, 'square_count': 16, 'mask_counts': {'1320': 2, '2013': 4, '2130': 2, '3021': 8}, 'selected_value_signature_counts': {'(11, 12, 15, 16)': 16}, 'apd_counts': {'(0,0,0,-290304)': 8, '(0,0,0,55296)': 8}, 'source_diagonal_size_counts': {'8': 16}, 'terminal_diagonal_size_counts': {'4': 16}, 'terminal_subgroup_counts': {'True': 16}, 'terminal_order_profile_counts': {'1:1,2:3': 16}, 'terminal_set_counts': {'0123,1032,2301,3210': 16}, 'source_type_counts': {'S4': 16}, 'family_flag_counts': {'associated': 0, 'complement_fixed': 0, 'local_2x2': 16, 'most_perfect_proxy': 16, 'panmagic': 16, 'wrap_2x2': 16}, 'square_indices': [101, 116, 176, 200, 278, 304, 371, 392, 482, 536, 564, 645, 703, 747, 784, 827]}`

## Interpretation

The main inside-out signature is exactly the selected-mask-affine
terminal-24 class, but it is broader than exact canonical `V4`.
The split report identifies the 32 extra pairs explicitly so the next
Phase-H branch can test whether a finer source-type, family,
automorphism, Hilbert, or Markov invariant separates them.

## Guardrail

This is a stratification report.  It still does not prove a Hilbert
or Markov characterization of Durer/Sagrada.
