# APD / PTE Report

Status: Phase G initial exact replay

## PTE Reading

`APD_m=0` is equivalent to equality of the `m`-th power sums of
the even and odd permutation-diagonal sum multisets.  Along the
Sagrada ray this gives a bounded Prouhet-Tarry-Escott style
deformation, not a new universal invariant of `24`.

## APD Polynomials

- zero APD polynomials: `['1', '2']`
- `APD_3(t)`: `[0, -1536, 480, -24]` = `-24*t*(t-4)*(t-16)`
- `APD_4(t)`: `[55296, -254976, 88992, -7104, 168]`

## First Nonzero Degree On The Bounded Interval

```text
t= 0, sum=34, m1<=8: 4
t= 1, sum=33, m1<=8: 3
t= 2, sum=32, m1<=8: 3
t= 3, sum=31, m1<=8: 3
t= 4, sum=30, m1<=8: 4
t= 5, sum=29, m1<=8: 3
t= 6, sum=28, m1<=8: 3
t= 7, sum=27, m1<=8: 3
t= 8, sum=26, m1<=8: 3
t= 9, sum=25, m1<=8: 3
t=10, sum=24, m1<=8: 3
```

## Special Values

### t=0

- magic sum: `34`
- inside bounded interval: `True`
- first nonzero degree up to max: `4`
- APD values: `{'1': 0, '2': 0, '3': 0, '4': 55296, '5': 9400320, '6': 1005834240, '7': 87253770240, '8': 6720341999616}`

### t=4

- magic sum: `30`
- inside bounded interval: `True`
- first nonzero degree up to max: `4`
- APD values: `{'1': 0, '2': 0, '3': 0, '4': 47616, '5': 7142400, '6': 660864000, '7': 48787200000, '8': 3160244699136}`

### t=10

- magic sum: `24`
- inside bounded interval: `True`
- first nonzero degree up to max: `3`
- APD values: `{'1': 0, '2': 0, '3': 8640, '4': 980736, '5': 72875520, '6': 4507184640, '7': 252369331200, '8': 13306787536896}`

### t=16

- magic sum: `18`
- inside bounded interval: `False`
- first nonzero degree up to max: `4`
- APD values: `{'1': 0, '2': 0, '3': 0, '4': 669696, '5': 60272640, '6': 4025487360, '7': 233814712320, '8': 12600946262016}`

## Guardrail

The PTE/APD layer explains the parity-power balance of permutation
diagonals.  It does not say that `24` is the APD-symmetric point;
at the bounded terminal endpoint `t=10`, `APD_3` is nonzero.
