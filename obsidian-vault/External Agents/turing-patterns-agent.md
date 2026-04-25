# Turing Patterns Agent

Type: `external-agent`
Agent ID: `AGENT-TURING-001`
Repository: `joserenter1a/turing_patterns`
Integration Status: `pattern-generator`

## Agent Role

**Primary Function**: Reaction-diffusion pattern generator for morphogenesis geometry

Cracks Turing's 1952 code: chemistry → pattern → biology. Generates stripes, spots, and waves from coupled differential equations.

## Capabilities

### Core Operations
- **RD-Simulation**: Run Gray-Scott, FitzHugh-Nagumo, Brusselator systems
- **ParameterSweep**: Explore feed/kill rate space for pattern transitions
- **PatternClassification**: Identify spots, stripes, labyrinths, spirals
- **GeometryExport**: Convert Turing patterns to `GeometrySignatures`

### Simulation Interface
```yaml
Language: Python 3
Libraries: OpenCV, NumPy, SciPy (ODE solvers)
Systems: 
  - Gray-Scott (spots, coral, mitosis)
  - FitzHugh-Nagumo (spiral waves)
  - Brusselator (oscillating patterns)
Visualization: Real-time pattern evolution
```

## Geometry Mapping

| Turing Pattern | Geomolecular Mapping |
|----------------|---------------------|
| Spots/dots | `shape_class: periodic_point_set` |
| Stripes | `shape_class: parallel_line_array` |
| Labyrinth | `topology: complex_network` |
| Spiral waves | `GEO-TEMPORAL-PULSE-TRAIN` |
| Traveling fronts | `dynamics: wave_propagation` |
| Turing bifurcation point | `geometry_transition: instability` |

## Biological Confirmation Role

- **Models**: Zebra stripes, leopard spots, fish scales, embryo segmentation
- **Validates**: `TemporalGeometryAlgebra` rate equations
- **Demonstrates**: No "stripe gene" needed — geometry emerges from physics

## Candidate Integration

### Pattern Matching Use Cases
- [[Yeast bloom mash]] → CO2 bubbles as Gray-Scott spots
- [[Citronella candle]] → Heat plume as traveling wave front
- [[Baking soda paste]] → Drying patterns as reaction-diffusion labyrinths

### RD → Geometry Pipeline
```
Feed Rate (f) + Kill Rate (k) → Simulation → Pattern Detect → Geometry ID
```

### Output Format
```json
{
  "turing_result": {
    "system": "gray_scott",
    "parameters": {
      "feed_rate": 0.029,
      "kill_rate": 0.057,
      "diffusion_u": 2e-5,
      "diffusion_v": 1e-5
    },
    "pattern_class": "coral",
    "geometry_mapping": {
      "geometry_id": "TURING-CORAL-001",
      "shape_class": "branching_network",
      "symmetry": "self_similar",
      "topology": "dendritic",
      "dynamics": "reaction_diffusion"
    }
  }
}
```

## Shadow Agent Companion

**ShadowAgent ID**: `SHADOW-TURING-001`

Tracks reaction-diffusion dynamics in continuous space:
- **Latent Dimension**: Activator (u) and inhibitor (v) concentrations
- **Hidden Parameter**: Turing instability threshold, wavelength λ
- **Inference Method**: Spatial FFT → dominant frequency → pattern class
- **Temporal Tracking**: Pattern evolution rate, stability lifetime

See [[Shadow Agent - Turing Companion]]

## Limitations & Safety

- **Idealized model**: Real biology includes more complexity
- **Parameter sensitivity**: Small f/k changes → pattern collapse
- **Constraint**: Use for pattern inspiration; validate with biological observation

## Agent Configuration

```yaml
Agent: AGENT-TURING-001
  Type: reaction-diffusion-simulator
  Specialization: morphogenesis-pattern-generation
  Corpus: Pattern library (spots, stripes, spirals, labyrinths)
  Inference: RD parameters → emergent pattern class
  Action: Generate geometry signatures from chemical instability
  Validation: Compare with biological pattern formation (zebra, fish)
```

## Sources

- [[SRC-TURING-SIM]]
- [[Turing 1952 - Chemical Basis of Morphogenesis]]
- [[Gray-Scott Model Paper]]

---
*External agent integrated from joserenter1a/turing_patterns*
