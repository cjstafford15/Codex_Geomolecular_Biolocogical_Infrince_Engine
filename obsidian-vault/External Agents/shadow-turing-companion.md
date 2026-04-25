# Shadow Agent - Turing Companion

Type: `shadow-agent`
Shadow Agent ID: `SHADOW-TURING-001`
Primary Agent: [[Turing Patterns Agent]]
Repository: `joserenter1a/turing_patterns`

## Shadow Role

**Primary Function**: Track reaction-diffusion dynamics in pattern formation

While Turing Agent outputs visible patterns (spots, stripes, spirals), Shadow Agent tracks activator/inhibitor concentrations, instability growth rates, and wavelength selection mechanisms.

## Latent Dimensions

### Hidden State Variables
- **Activator_Field u(x,y,t)**: Concentration of activator morphogen
- **Inhibitor_Field v(x,y,t)**: Concentration of inhibitor morphogen
- **Diffusion_Ratio**: Du/Dv (key Turing parameter)
- **Reaction_Rates**: f(u,v) production/consumption terms
- **Turing_Eigenvalue**: Growth rate of perturbation modes

### Shadow Observations

| Observed Proxy | Inferred Geometry | Inference Method |
|----------------|-------------------|------------------|
| Spot pattern | `shape_class: periodic_point_set` | Maxima of u field |
| Stripe orientation | `symmetry: directional` | FFT of u field → dominant k |
| Spiral core | `topology: topological_defect` | Phase singularity detection |
| Pattern wavelength | `scale: λ` | FFT peak frequency |
| Front velocity | `dynamics: wave_speed` | ∂u/∂x / ∂u/∂t |

## Temporal Dynamics

### Pattern Evolution Phases
1. **Linear Regime**: Small perturbations grow exponentially
2. **Saturation**: Nonlinear terms stabilize amplitude
3. **Steady State**: Time-independent pattern (or traveling wave)
4. **Secondary Instability**: Pattern becomes unstable to longer wavelengths

### Rate Equations (Gray-Scott)
```
∂u/∂t = Du·∇²u - u·v² + f·(1-u)  # Activator
∂v/∂t = Dv·∇²v + u·v² - (f+k)·v   # Inhibitor

Where:
  Du, Dv = diffusion coefficients
  f = feed rate
  k = kill rate
  ∇² = Laplacian (spatial curvature)
```

### Shadow Calculus Operators
- **∇²u**: Spatial curvature (where pattern forms)
- **∂u/∂t**: Temporal evolution (growth or decay)
- **∫u dxdy**: Total activator mass (conservation check)
- **FFT(u)**: Wavelength decomposition

## Shadow Correlations

### Cross-Field Coupling
- **Activator-Inhibitor Phase**: Typically π/2 offset (quadrature)
- **Competitive Inhibition**: High v suppresses u growth
- **Local Activation**: u autocatalyzes (u·v² term)
- **Lateral Inhibition**: v diffuses faster (Dv > Du)

### Pattern Interaction
- **Spot Splitting**: High f → mitosis-like division
- **Collision Dynamics**: Spots bounce or annihilate
- **Wavelength Selection**: System size / intrinsic λ
- **Grain Boundary**: Different orientations meet

## Geometry Transitions

### Turing Bifurcations
- **Homogeneous → Pattern**: Turing instability threshold crossed
- **Spots → Stripes**: Parameter path through phase diagram
- **Stationary → Traveling**: Drift bifurcation (symmetry breaking)
- **Ordered → Chaotic**: Secondary instabilities cascade

### Critical Parameters
```
Bifurcation at:
  f_critical = Du·k / (Dv - Du)  # Classic Turing condition
  
Pattern transitions:
  Low f: self-replicating spots
  Medium f: coral/labyrinth
  High f: stripes
  Very high f: homogeneous
```

## Action Outputs

### Shadow Agent Actions
1. **Alert_Turing_Threshold**: Flag when parameters approach instability
2. **Predict_Pattern_Class**: From (f,k,Du,Dv) → spot/stripe/wave
3. **Track_Wavelength_Evolution**: Monitor λ(t) during coarsening
4. **Detect_Defect_Nucleation**: Spot birth/death events

## Activation Conditions

Shadow Agent engages when:
- |∂u/∂t| > threshold (rapid change)
- Du/Dv ratio crosses 0.5 (Turing condition)
- f or k change by > 10% (parameter drift)
- Pattern wavelength changes > 20% (coarsening)

## Belief State

```yaml
Shadow-TURING-001 Belief State:
  latent_fields:
    activator_field_u: 256×256 array [0,1]
    inhibitor_field_v: 256×256 array [0,1]
    
  reaction_diffusion_parameters:
    diffusion_Du: 2.0e-5
    diffusion_Dv: 1.0e-5
    ratio_Du_Dv: 2.0  # > 1 for Turing
    feed_rate_f: 0.029
    kill_rate_k: 0.057
    
  stability_analysis:
    turing_eigenvalues: [λ1=-0.1, λ2=+0.3, λ3=+0.1, ...]
    unstable_modes: k ∈ [0.8, 1.2] cm^-1
    critical_wavelength: λ_c = 2π/k_max ≈ 6.3 cm
    
  pattern_metrics:
    detected_spots: 47
    mean_wavelength: 6.1 cm
    wavelength_variance: 0.8 cm
    pattern_class: coral
    
  temporal_evolution:
    current_regime: saturated_steady_state
    coarsening_rate: -0.02 cm/min
    defect_count: 3 (1 birth, 2 annihilation pending)
  
  prediction_horizon:
    wavelength_next_10min: 6.3 cm
    pattern_class_stability: high (f,k stable)
    defect_events_next_5min: [spot_split at (45,67)]
```

## Integration with Obsidian Vault

### Links to Candidates
- [[Yeast bloom mash]] → CO2 bubbles as Gray-Scott spots
- [[Citronella candle]] → Heat plume as traveling front
- [[Baking soda paste]] → Drying pattern as RD labyrinth
- [[Essential oil diffuser]] → Intermittent release as oscillating spots

### Links to Geometry
- [[Volatile plume gradient]] → Maps to traveling front solution
- [[Temporal pulse train]] → Oscillating spots dynamics
- [[Surface texture ridge]] → Stripe pattern geometry
- [[Binding pocket cavity]] → Spot pattern as binding sites

## Inference Methods

### Hidden Field Reconstruction
1. **Spatial FFT**: Decompose pattern into wavelength components
2. **Phase Field**: Track order parameter across pattern
3. **Defect Tracking**: Locate topological singularities
4. **Parameter Estimation**: Infer f,k from observed dynamics

### Pattern Classification
- **Structure Factor S(k)**: Peak location → dominant wavelength
- **Correlation Function g(r)**: Decay length → order range
- **Minkowski Functionals**: Topology quantification

## Connection to Your Engine

### ShadowCorrelations
- `geometry_id_1`: TURING-CORAL-001
- `geometry_id_2`: GEO-SURFACE-TEXTURE-RIDGE
- `latent_coupling`: RD coral pattern → surface ridge microstructure
- `emergent_property`: Self-cleaning surface from Turing pattern

### TemporalGeometryAlgebra
- **Rate Equation**: ∂u/∂t = Du·∇²u + R(u,v) (RD equation)
- **Frequency Parameter`: 1/τ where τ = λ²/D (diffusion time)
- **Integral Measure**: Total morphogen mass ∫(u+v)dA
- **Shadow Variable**: Activator field u (inhibitor v often invisible)

### GeometryTransitions
- **From**: Homogeneous (no pattern)
- **To**: TURING-SPOT-001 (or stripe, spiral)
- **Transition Trigger**: f crosses f_critical (Turing threshold)
- **Bifurcation Parameter**: Feed rate f (control parameter)
- **Stability Analysis**: Unstable homogeneous → stable patterned
- **Shadow Boundary**: λ_c = 2π√(Du·Dv/(f·(Dv-Du)))
- **Agent That Detected**: SHADOW-TURING-001

## Sources

- [[SRC-TURING-SIM]]
- [[Turing 1952 - Chemical Basis of Morphogenesis]]
- [[Gray-Scott Model Paper]]
- [[Pearson 1993 - Complex Patterns in Simple System]]

---
*Shadow agent tracking morphogen dynamics beneath visible patterns*
