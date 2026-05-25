# Order-4 F2 Extension Report

Status: Phase F extension across terminal-24 Phase-C records

## Summary

- all 880 cell-value affine counts: `{'affine_automorphism': 432, 'non_affine': 448}`
- terminal-24 pairs: `236`
- exact canonical `V4` pairs: `144`
- terminal-24 pairs with affine cell-value labeling: `144`
- affine cell-value labeling pairs equal exact canonical `V4`: `True`
- selected mask affine counts: `{'affine_plane': 176, 'non_affine': 60}`
- selected mask direction counts: `{'(0, 1, 4, 5)': 176}`
- terminal affine pure-transport counts: `{'False': 52, 'True': 184}`

## Exact Canonical V4 Subclass

- pair count: `144`
- all cell labelings affine automorphisms: `True`
- all selected masks affine planes: `True`
- selected mask directions: `{'(0, 1, 4, 5)': 144}`
- all terminal affine layers pure transport: `True`
- terminal affine count distribution: `{'36': 144}`
- transported affine count distribution: `{'36': 144}`

## Signature Profiles

- values `11,12,13,15`: count `4`, mask affine `False`, terminal affine `31`, transported affine `30`, pure `False`
- values `11,12,13,16`: count `4`, mask affine `False`, terminal affine `29`, transported affine `28`, pure `False`
- values `11,12,14,15`: count `4`, mask affine `False`, terminal affine `29`, transported affine `28`, pure `False`
- values `11,12,14,16`: count `8`, mask affine `False`, terminal affine `32`, transported affine `30`, pure `False`
- values `11,12,15,16`: count `176`, mask affine `True`, terminal affine `36`, transported affine `36`, pure `True`
- values `11,13,14,15`: count `8`, mask affine `False`, terminal affine `30`, transported affine `30`, pure `True`
- values `11,13,14,16`: count `4`, mask affine `False`, terminal affine `29`, transported affine `28`, pure `False`
- values `11,13,15,16`: count `16`, mask affine `False`, terminal affine `35`, transported affine `34`, pure `False`
- values `11,14,15,16`: count `12`, mask affine `False`, terminal affine `32`, transported affine `30`, pure `False`

## Guardrail

The exact canonical `V4` subclass is strongly aligned with affine
cell-value labelings in this fixed orientation.  This is a finite
Phase-C fingerprint, not a uniqueness theorem for endpoint `24` in all
magic-square categories.
