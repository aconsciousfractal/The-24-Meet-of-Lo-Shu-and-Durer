# Bounded Magic Polytope Report

Status: Phase E initial linear certificate

## Sagrada Ray

```text
mask: 2013
t interval: [0, 10]
source sum: 34
terminal sum: 24
terminal hit cells: ['r2c1']
```

At `D(10)`:

```text
free-sum face dimension: 6
fixed-sum S=24 face dimension: 5
vertex in free-sum polytope: False
vertex in fixed-sum S=24 polytope: False
```

Minimal fixed-sum `S=24` face containing `D(10)`:

```text
forced bounds: ['r0c0=1', 'r2c1=1']
face dimension: 5
vertex count: 47
integral vertices: 37
D(10) is vertex of this face: False
max denominator distribution: {'1': 37, '2': 10}
D4 stabilizer: ['id']
D(10) relative interior: True
barycentric certificate: vertices [34, 41] with weights ['4/5', '1/5']
```

## Lo Shu S=24 Fiber

```text
g: 8
dimension: 2
lattice points: 5
vertices (a,b): [['0', '-1'], ['1', '0'], ['0', '1'], ['-1', '0']]
common active bounds: []
```

Closed count formula:

```text
m = min(g-1, 9-g)
|P_g cap Z^2| = 2m^2 + 2m + 1
counts by sum: {'3': 1, '6': 5, '9': 13, '12': 25, '15': 41, '18': 25, '21': 13, '24': 5, '27': 1}
all counts match formula: True
```

## Reading

- `D(10)` is a boundary point, not a vertex, of both the free-sum and
  fixed-sum bounded order-4 magic polytopes.
- The Sagrada ray lies on the persistent lower facet `r0c0 = 1`, leaves
  the initial upper facet `r3c3 = 16`, and terminates when `r2c1 = 1`.
- The Lo Shu `S=24` fiber has 5 lattice points in a 2D parameter polygon;
  it is a bounded-slice phenomenon rather than a common boundary face.
