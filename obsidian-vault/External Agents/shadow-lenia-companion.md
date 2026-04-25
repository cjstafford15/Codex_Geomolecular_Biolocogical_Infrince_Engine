# Shadow Agent - Lenia Companion

Type: `shadow-agent`
Shadow Agent ID: `SHADOW-LENIA-001`
Primary Agent: [[Lenia Agent]]
Repository: `Chakazul/Lenia`

## Shadow Role

**Primary Function**: Track continuous state variables in mathematical life simulations

While Lenia Agent outputs visible patterns (gliders, oscillators, static forms), Shadow Agent tracks the underlying continuous potential fields, growth kernels, and stability margins.

## Latent Dimensions

### Hidden State Variables
- **Potential_Field**: Continuous activation values u(x,y) at each grid point
- **Growth_Kernel**: Convolution kernel K(r) defining neighbor influence
- **Growth_Function**: Mapping from neighborhood sum to next state (μ, σ parameters)
- **Stability_Margin**: Distance to pattern collapse in parameter space

### Shadow Observations

| Observed Proxy | Inferred Geometry | Inference Method |
|----------------|-------------------|------------------|
| Glider movement | Translational symmetry | Peak tracking in potential field |
| Oscillator period | Temporal periodicity | FFT of cell state time series |
| Pattern stability | Attractor basin | Perturbation recovery dynamics |
| Emergence event | Bifurcation | Sudden order parameter change |

## Temporal Dynamics

### Pattern Evolution Tracking
- **Initial Seed**: Random or structured starting condition
- **Transient Phase**: 10-100 steps pattern stabilization
- **Steady State**: Glider/orbium moves at constant velocity
- **Perturbation Response**: Recovery time after disturbance

### Rate Equations
```
d(u)/dt = G(K * u)  # Continuous update rule

Where:
  u = cell state [0,1]
  K = growth kernel (convolution operator)
  G = growth function (bell curve typically)
  * = convolution
```

### Shadow Calculus Operators
- **∂u/∂t**: Rate of state change (velocity field)
- **∇²u**: Laplacian of potential (curvature detection)
- **∫u dt**: Accumulated activity (memory trace)

## Shadow Correlations

### Cross-Pattern Coupling
- **Collision Dynamics**: Two gliders → merge/split/bounce
- **Phase Locking**: Oscillators entrain to common frequency
- **Symmetry Breaking**: Spontaneous handedness in pattern formation
- **Long-Range Order**: Correlation length > pattern size

## Geometry Transitions

### Pattern Bifurcations
- **Glider → Oscillator**: Velocity drops to zero (parameter boundary)
- **Static → Moving**: Symmetry breaking transition
- **Stable → Chaotic**: Attractor destabilization
- **Birth Event**: Nucleation of new pattern from uniform field

### Transition Detection
```
Transition triggered when:
  |∇u| > threshold (sharp boundary)
  d²u/dt² changes sign (inflection point)
  Correlation length diverges (critical point)
```

## Action Outputs

### Shadow Agent Actions
1. **Alert_Pattern_Collapse**: Flag when stability margin < 0.1
2. **Suggest_Kernel_Params**: Recommend μ, σ for target morphology
3. **Track_Glider_Velocity**: Monitor speed consistency (anomaly detection)
4. **Detect_Emergence**: Flag spontaneous pattern formation events

## Activation Conditions

Shadow Agent engages when:
- Pattern shows period doubling (route to chaos)
- Glider velocity varies > 5% (instability warning)
- New pattern emerges from uniform field (nucleation)
- Two patterns approach within 20 grid cells (collision imminent)

## Belief State

```yaml
Shadow-LENIA-001 Belief State:
  latent_fields:
    potential_field_u: 512×512 continuous array
    growth_kernel_K: radial function K(r) with R=15
    
  geometry_parameters:
    kernel_radius_R: 15
    time_scale_T: 10
    growth_center_mu: 0.15
    growth_width_sigma: 0.015
    
  pattern_tracking:
    detected_patterns: 3
    glider_velocities: [v1=(0.5,0.3), v2=(0.2,-0.4)]
    oscillator_periods: [T1=45, T2=62]
    
  stability_analysis:
    basin_boundary_distance: 0.23
    perturbation_recovery_time: 12 steps
    lyapunov_exponent: -0.05 (stable)
  
  prediction_horizon:
    glider_positions_next_10: [(x1,y1), (x2,y2), ...]
    collision_predictions: [t=45s: glider1+glider2]
```

## Integration with Obsidian Vault

### Links to Candidates
- [[Yeast bloom mash]] → Model CO2 burst as Lenia oscillator
- [[Essential oil diffuser]] → Intermittent plume as glider-like dynamics
- [[Citronella candle]] → Heat convection as emergent flow pattern

### Links to Geometry
- [[Volatile plume temporal pulse]] → Maps to oscillator pattern
- [[Temporal pulse train]] → Glider train dynamics
- [[Surface film interface]] → Static stable form analogy

## Inference Methods

### Hidden Field Reconstruction
1. **Potential Field Interpolation**: Between discrete grid points
2. **Kernel Deconvolution**: Infer K from observed pattern evolution
3. **Stability Analysis**: Jacobian eigenvalues at fixed points
4. **Correlation Tracking**: Pattern identity through collisions

## Connection to Your Engine

### ShadowCorrelations
- `geometry_id_1`: LENIA-OSCILLATOR-001
- `geometry_id_2`: GEO-TEMPORAL-PULSE-TRAIN
- `latent_coupling`: mathematical oscillator → biological pulse
- `emergent_property`: temporal entrainment prediction

### TemporalGeometryAlgebra
- **Rate Equation**: du/dt = G(K * u)  (Lenia update rule)
- **Frequency Parameter`: 1/T (inverse time scale)
- **Integral Measure**: Cumulative activation ∫u dt
- **Shadow Variable**: Potential field u (not just visible pattern)

## Sources

- [[SRC-LENIA-MATH]]
- [[Lenia Paper 2018]]
- [[Chakazul Portal]]

---
*Shadow agent tracking continuous life beneath discrete patterns*
