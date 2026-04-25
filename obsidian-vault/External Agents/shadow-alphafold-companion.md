# Shadow Agent - AlphaFold Companion

Type: `shadow-agent`
Shadow Agent ID: `SHADOW-ALPHAFOLD-001`
Primary Agent: [[AlphaFold Agent]]
Repository: `google-deepmind/alphafold`

## Shadow Role

**Primary Function**: Track latent variables in protein structure prediction

While AlphaFold Agent outputs visible 3D coordinates, Shadow Agent tracks hidden confidence distributions, MSA depth effects, and uncertainty propagation.

## Latent Dimensions

### Hidden State Variables
- **MSA_Entropy**: Multiple sequence alignment column entropy (uncertainty per position)
- **Attention_Pattern**: Which residue pairs influence each other (graph structure)
- **Template_Weight**: How much experimental templates contributed vs. de novo
- **Recycling_Convergence**: Iteration-to-iteration stability (convergence depth)

### Shadow Observations

| Observed Proxy | Inferred Geometry | Inference Method |
|----------------|-------------------|------------------|
| pLDDT score drop | Flexible loop region | Attention weight dispersion |
| High pLDDT plateau | Rigid domain | Low MSA entropy + strong templates |
| Domain boundary | Hinge geometry | Attention pattern discontinuity |

## Temporal Dynamics

### Structure Evolution Tracking
- **Initial Guess**: Random coil or template seed
- **Recycling Iterations**: 3-4 cycles typical, each refines geometry
- **Convergence Detection**: RMSD < 0.1 Å between cycles
- **Uncertainty Decay**: Confidence increases with recycling (usually)

### Rate Equations
```
d(confidence)/dt = α·(information_gain) - β·(noise_accumulation)

Where:
  α = MSA depth coefficient
  β = sequence divergence penalty
```

## Shadow Correlations

### Cross-Structure Patterns
- **Homolog Comparison**: Same fold, different sequence → confidence variation
- **Domain Coupling**: Rigid domain A + flexible linker + rigid domain B
- **Cotranslational Folding**: N-terminal structure before C-terminal synthesis

## Geometry Transitions

### Structure Prediction Bifurcations
- **Template vs. De Novo**: When PDB template conflicts with sequence
- **Topology Switch**: β-sheet → α-helix transitions (rare but possible)
- **Oligomer State**: Monomer prediction vs. multimer interface

## Action Outputs

### Shadow Agent Actions
1. **Alert_Flexible_Region**: Flag residues with pLDDT < 50 for geometry uncertainty
2. **Suggest_Recycling_Depth**: Recommend 3 vs. 4 recycling cycles based on convergence
3. **Confidence_Calibration**: Adjust geometry confidence based on MSA quality
4. **Domain_Boundary_Detection**: Identify flexible hinges between rigid domains

## Activation Conditions

Shadow Agent engages when:
- pLDDT variance across residues > 0.3
- MSA depth < 100 sequences (shallow alignment)
- No significant template hits (de novo mode)
- Recycling iterations show oscillation (non-convergence)

## Belief State

```yaml
Shadow-ALPHAFOLD-001 Belief State:
  latent_variables:
    MSA_entropy_vector: [0.2, 0.8, 0.3, ..., 0.1]  # per residue
    attention_graph: adjacency matrix (N×N)
    template_weights: {PDB_6xyz: 0.7, PDB_3abc: 0.3}
  
  confidence_distribution:
    mean_plddt: 78.5
    variance: 12.3
    low_confidence_regions: [45-67, 102-115]
  
  convergence_status:
    iterations_completed: 3
    rmsd_cycle3_to_cycle2: 0.08 Å
    stability: converged
  
  prediction_horizon:
    next_recycling_delta: 0.02 Å expected
    confidence_saturation: reached
```

## Integration with Obsidian Vault

### Links to Candidates
- [[Menthol crystal]] → TRPM8 structure → Shadow tracks which residues are flexible
- [[Capsaicin extract]] → TRPV1 structure → Shadow flags binding pocket confidence

### Links to Geometry
- [[Binding pocket cavity]] → Shadow maps pocket flexibility to `dynamics` parameter
- [[Skin lamellar lipid layer]] → Shadow tracks membrane domain predictions

## Inference Methods

### Hidden State Reconstruction
1. **Attention Rollout**: Aggregate attention weights across layers
2. **Gradient-Based Attribution**: Which input features influence output
3. **Ensemble Variance**: Multiple MSA samples → confidence distribution

## Sources

- [[SRC-ALPHAFOLD-DB]]
- [[AlphaFold Technical Note 2.3.0]]
- [[AlphaFold-Multimer Paper]]

---
*Shadow agent tracking latent structure of AlphaFold predictions*
