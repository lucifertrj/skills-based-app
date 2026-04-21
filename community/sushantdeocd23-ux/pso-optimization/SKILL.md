---
name: pso-optimization
description: Particle Swarm Optimization (PSO) skill. A gradient-free, population-based metaheuristic for continuous function minimization, hyperparameter tuning, and black-box problems. Covers velocity and position updates, inertia weight, cognitive and social coefficients, constriction factor, stability and convergence analysis, worked examples on the sphere function and linear regression, and comparisons with gradient descent, least squares, and Bayesian optimization. Use when you need swarm intelligence, derivative-free optimization, or a simple global search over a continuous space.
---

# Particle Swarm Optimization (PSO)

## What This Is

PSO is a population-based optimizer where a swarm of particles moves through a search space. Each particle tracks its own best position (`pbest`) and knows the swarm's best position (`gbest`). Velocity updates pull particles toward both, balancing exploration and exploitation. No gradients needed, just a function you can evaluate.

Use this when you're working on:

* Minimizing black-box, non-differentiable, or noisy objectives
* Hyperparameter search for ML models
* Warm-starting a local optimizer
* Teaching or demoing swarm intelligence

---

## Installation

```bash
pip install numpy matplotlib
# optional helpers
pip install pyswarms scipy
```

Numpy alone is enough for a from-scratch implementation.

---

## Core Update Rules

For each particle `i` at iteration `t`:

```
v_{t+1} = w * v_t + c1 * r1 * (pbest_i - x_t) + c2 * r2 * (gbest - x_t)
x_{t+1} = x_t + v_{t+1}
```

* `w` inertia weight, controls momentum
* `c1` cognitive coefficient, pull toward personal best
* `c2` social coefficient, pull toward swarm best
* `r1, r2` uniform random in [0, 1], resampled every step

---

## Quick Start (numpy, from scratch)

Minimize the sphere function `f(x) = sum(x^2)`:

```python
import numpy as np

def sphere(x):
    return np.sum(x**2, axis=1)

def pso(f, dim=2, n=30, iters=100, bounds=(-5, 5),
        w=0.729, c1=1.49445, c2=1.49445, seed=0):
    rng = np.random.default_rng(seed)
    lo, hi = bounds
    x = rng.uniform(lo, hi, (n, dim))
    v = np.zeros_like(x)
    pbest = x.copy()
    pbest_val = f(x)
    gbest = pbest[np.argmin(pbest_val)].copy()
    gbest_val = pbest_val.min()

    for _ in range(iters):
        r1 = rng.random((n, dim))
        r2 = rng.random((n, dim))
        v = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x)
        x = np.clip(x + v, lo, hi)
        val = f(x)
        improved = val < pbest_val
        pbest[improved] = x[improved]
        pbest_val[improved] = val[improved]
        if pbest_val.min() < gbest_val:
            gbest_val = pbest_val.min()
            gbest = pbest[np.argmin(pbest_val)].copy()
    return gbest, gbest_val

best_x, best_f = pso(sphere)
print(best_x, best_f)   # ~[0, 0], ~0
```

---

## Parameter Defaults (Clerc & Kennedy)

The "just works" values derived from constriction-factor analysis:

* `w = 0.729`
* `c1 = c2 = 1.49445`
* Swarm size `n = 30`
* Iterations `100 - 500` depending on cost

These keep the swarm stable on average. Start here before tuning.

---

## Convergence and Stability

Each particle follows a linear recurrence. Its characteristic equation is:

```
lambda^2 - (1 + w - phi) * lambda + w = 0,    phi = c1*r1 + c2*r2
```

Stability (no blow-up) requires roughly:

```
0 < phi < 4
w < 1
w > 0.5 * (phi - 1)
```

The default `w = 0.729, c1 = c2 = 1.49445` sits inside this region on average, which is why it's the go-to.

---

## Regression Example (PSO as a generic optimizer)

Fit `y = 2x + 3 + noise` by minimizing MSE through PSO:

```python
import numpy as np

rng = np.random.default_rng(0)
X = np.linspace(-1, 1, 100)
y = 2*X + 3 + rng.normal(0, 0.1, 100)

def mse(params):
    a = params[:, 0]
    b = params[:, 1]
    pred = a[:, None] * X + b[:, None]
    return ((pred - y)**2).mean(axis=1)

best, loss = pso(mse, dim=2, bounds=(-10, 10))
print(best, loss)   # ~[2.0, 3.0], tiny loss
```

Analytical least squares is still faster and exact for linear regression. This example is for intuition, not production.

---

## Common Variants

### Constriction PSO

Replaces `w` with constriction factor `chi ~ 0.729`. The Clerc defaults above already give you this behavior.

### Inertia Decay

Start `w = 0.9`, linearly decay to `0.4` across iterations. Early exploration, late exploitation.

```python
w = 0.9 - (0.9 - 0.4) * (t / iters)
```

### Local-Best (lbest) PSO

Replace `gbest` with the best particle in a ring neighborhood of size `k`. Slower convergence but better on multimodal landscapes.

### Binary PSO

Apply sigmoid to velocity to flip 0/1 bits. Useful for feature selection.

---

## Using pyswarms (when you don't want to reinvent)

```python
import numpy as np
import pyswarms as ps

def sphere(x):
    return np.sum(x**2, axis=1)

options = {'c1': 1.49445, 'c2': 1.49445, 'w': 0.729}
optimizer = ps.single.GlobalBestPSO(n_particles=30, dimensions=2,
                                    options=options,
                                    bounds=(np.array([-5, -5]), np.array([5, 5])))
cost, pos = optimizer.optimize(sphere, iters=100)
```

---

## Gotchas

* Clip positions to bounds every step or particles drift off the search space
* Seed your RNG when reporting results
* PSO is stochastic, so benchmark over 10+ seeds and report mean and std
* Scale features if variables have very different magnitudes
* Premature convergence means the swarm collapsed too fast. Raise `w`, increase swarm size, or switch to lbest topology

---

## When to Use What

* Smooth, differentiable, small scale -> gradient descent, BFGS
* Convex -> cvxpy or a convex solver
* Black-box, continuous, moderate dims (up to ~50) -> **PSO**
* Discrete or combinatorial -> genetic algorithm, simulated annealing
* Very expensive objective (budget under ~1000 evals) -> Bayesian optimization

---

## References

* Kennedy & Eberhart 1995, "Particle Swarm Optimization" (original paper)
* Clerc & Kennedy 2002, "The particle swarm: explosion, stability, and convergence"
* pyswarms docs: https://pyswarms.readthedocs.io/
* scipy.optimize overview: https://docs.scipy.org/doc/scipy/reference/optimize.html
* Wikipedia article on PSO: https://en.wikipedia.org/wiki/Particle_swarm_optimization

---

## Extras (Optional Exploration)

* Multi-objective PSO (MOPSO) with Pareto fronts
* Adaptive PSO with dynamic `w, c1, c2`
* Quantum-behaved PSO (QPSO)
* Hybrid PSO + local search (memetic algorithms)
* GPU-parallel swarm evaluation for expensive objectives
