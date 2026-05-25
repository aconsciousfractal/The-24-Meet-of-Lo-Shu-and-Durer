# Order-4 APD/PTE Profile Report

Status: Phase G APD/PTE extension across Phase-C rays

## Global Counts

- pairs: `7040`
- max APD degree checked: `8`
- endpoint counts: `{'22': 176, '23': 44, '24': 236, '25': 268, '26': 676, '27': 108, '28': 328, '29': 376, '30': 772, '31': 420, '32': 884, '33': 992, '34': 1760}`
- terminal first-nonzero degree counts: `{'none': 32, '3': 5748, '4': 1260}`
- polynomial first-nonzero degree counts: `{'3': 7040}`

## Endpoint 24

- pair count: `236`
- terminal first-nonzero degree counts: `{'3': 236}`
- polynomial first-nonzero degree counts: `{'3': 236}`
- terminal APD3 zero counts: `{'False': 236}`

## Canonical Durer/Sagrada Record

```json
{
  "apd3_polynomial_coefficients": [
    0,
    -1536,
    480,
    -24
  ],
  "endpoint": 24,
  "mask": "1203",
  "polynomial_first_nonzero_degree": 3,
  "source_first_nonzero_degree": 4,
  "square_index": 174,
  "t_max": 10,
  "terminal_apd3_zero": false,
  "terminal_apd_values": {
    "1": 0,
    "2": 0,
    "3": 8640,
    "4": 980736,
    "5": 72875520,
    "6": 4507184640,
    "7": 252369331200,
    "8": 13306787536896
  },
  "terminal_first_nonzero_degree": 3
}
```

## Endpoint Summary

```text
22: pairs=176, terminal_m1={'3': 176}, APD3_zero={'False': 176}
23: pairs=44, terminal_m1={'3': 44}, APD3_zero={'False': 44}
24: pairs=236, terminal_m1={'3': 236}, APD3_zero={'False': 236}
25: pairs=268, terminal_m1={'3': 268}, APD3_zero={'False': 268}
26: pairs=676, terminal_m1={'3': 676}, APD3_zero={'False': 676}
27: pairs=108, terminal_m1={'3': 108}, APD3_zero={'False': 108}
28: pairs=328, terminal_m1={'3': 324, '4': 4}, APD3_zero={'False': 324, 'True': 4}
29: pairs=376, terminal_m1={'3': 372, '4': 4}, APD3_zero={'False': 372, 'True': 4}
30: pairs=772, terminal_m1={'3': 772}, APD3_zero={'False': 772}
31: pairs=420, terminal_m1={'3': 416, '4': 4}, APD3_zero={'False': 416, 'True': 4}
32: pairs=884, terminal_m1={'3': 884}, APD3_zero={'False': 884}
33: pairs=992, terminal_m1={'3': 992}, APD3_zero={'False': 992}
34: pairs=1760, terminal_m1={'3': 480, '4': 1248, 'none': 32}, APD3_zero={'False': 480, 'True': 1280}
```

## Guardrail

This is an APD/PTE stratification, not an endpoint theorem by itself.
Endpoint `24` should only be claimed APD-special if the endpoint
summary separates it from the other terminal sums.
