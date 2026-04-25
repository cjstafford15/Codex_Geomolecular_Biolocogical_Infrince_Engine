# Evidence Report

Type: `agent-report`
Agent: `evidence-agent`

## Summary

- Geometries: 7
- Candidates: 10
- Observations: 7
- Sources: 9
- Product ideas: 4
- Validation issues: 0
- Average observation evidence score: 0.286

## Data Integrity

No referential integrity issues found.

## Geometry Evidence Scores

### Surface texture ridge (`GEO-SURFACE-TEXTURE-RIDGE`)

- Observation count: 0
- Evidence score: 0.0
- Lowest observation score: 0.0
- Contradictions/confounders: 0

### Volatile plume gradient (`GEO-VOLATILE-PLUME-GRADIENT`)

- Observation count: 1
- Evidence score: 0.223
- Lowest observation score: 0.223
- Contradictions/confounders: 1

### Volatile plume temporal pulse (`GEO-VOLATILE-PLUME-PULSE`)

- Observation count: 2
- Evidence score: 0.234
- Lowest observation score: 0.223
- Contradictions/confounders: 2

### Surface film interface (`GEO-SURFACE-FILM-INTERFACE`)

- Observation count: 1
- Evidence score: 0.245
- Lowest observation score: 0.245
- Contradictions/confounders: 1

### Temporal pulse train (`GEO-TEMPORAL-PULSE-TRAIN`)

- Observation count: 1
- Evidence score: 0.245
- Lowest observation score: 0.245
- Contradictions/confounders: 1

### Binding pocket cavity (`GEO-BINDING-POCKET-CAVITY`)

- Observation count: 1
- Evidence score: 0.41
- Lowest observation score: 0.41
- Contradictions/confounders: 1

### Skin lamellar lipid layer (`GEO-SKIN-LAMELLAR-LAYER`)

- Observation count: 1
- Evidence score: 0.41
- Lowest observation score: 0.41
- Contradictions/confounders: 1

## Weakest Observations

- `OBS-001` Apple cider vinegar -> Volatile plume gradient: score 0.223 (low confidence, weak source reliability, contradiction or confounder recorded)
- `OBS-002` Yeast bloom mash -> Volatile plume temporal pulse: score 0.223 (low confidence, weak source reliability, contradiction or confounder recorded)
- `OBS-003` Essential oil diffuser -> Volatile plume temporal pulse: score 0.245 (low confidence, weak source reliability, contradiction or confounder recorded)
- `OBS-004` Soap film residue -> Surface film interface: score 0.245 (low confidence, weak source reliability, contradiction or confounder recorded)
- `OBS-007` Citronella candle -> Temporal pulse train: score 0.245 (low confidence, weak source reliability, contradiction or confounder recorded)
- `OBS-005` Menthol crystal -> Binding pocket cavity: score 0.41 (weak source reliability, contradiction or confounder recorded)
- `OBS-006` Menthol crystal -> Skin lamellar lipid layer: score 0.41 (weak source reliability, contradiction or confounder recorded)

## Measurement And Review Gaps

- `observation_validation` OBS-001: Measure volatile concentration over distance and time with a matched control.
- `observation_validation` OBS-002: Measure volatile concentration over distance and time with a matched control.
- `observation_validation` OBS-003: Measure volatile concentration over distance and time with a matched control.
- `observation_validation` OBS-004: Measure contact angle, surface roughness, and treated versus untreated adhesion.
- `observation_validation` OBS-005: Record structural model source, pocket fit metric, and experimental binding status.
- `observation_validation` OBS-006: Use a permeation assay or literature measurement with irritation and safety review.
- `observation_validation` OBS-007: Record frequency, duty cycle, and matched steady-output controls.
- `geometry_without_observation` Surface texture ridge: Measure contact angle, surface roughness, and treated versus untreated adhesion.
- `safety_review` Apple cider vinegar: Record safe handling limits and blocked claims before product interpretation.
- `safety_review` Sugar fermentation aroma: Record safe handling limits and blocked claims before product interpretation.
- `safety_review` Yeast bloom mash: Record safe handling limits and blocked claims before product interpretation.
- `safety_review` Essential oil diffuser: Record safe handling limits and blocked claims before product interpretation.
- `safety_review` Soap film residue: Record safe handling limits and blocked claims before product interpretation.
- `safety_review` Citronella candle: Record safe handling limits and blocked claims before product interpretation.
- `safety_review` Capsaicin extract: Record safe handling limits and blocked claims before product interpretation.
- `safety_review` Menthol crystal: Record safe handling limits and blocked claims before product interpretation.
- `safety_review` Aloe vera gel: Record safe handling limits and blocked claims before product interpretation.
- `product_validation` Geometry-led insect behavior screen: Measure volatile concentration over distance and time with a matched control.
- `product_validation` Geometry-led insect behavior screen: Measure contact angle, surface roughness, and treated versus untreated adhesion.
- `blocked_claim_review` Geometry-led insect behavior screen: Do not claim attraction, repellency, elimination, medical value, or pesticide efficacy yet.
- `blocked_claim_review` Geometry-led insect behavior screen: Do not claim attraction, repellency, elimination, medical value, or pesticide efficacy yet.
- `product_validation` Pulse modulated aroma delivery: Measure volatile concentration over distance and time with a matched control.
- `product_validation` Pulse modulated aroma delivery: Record frequency, duty cycle, and matched steady-output controls.
- `blocked_claim_review` Pulse modulated aroma delivery: Do not claim repellency, medical effect, or guaranteed behavioral change.
- `blocked_claim_review` Pulse modulated aroma delivery: Do not claim repellency, medical effect, or guaranteed behavioral change.
- `blocked_claim_review` Pulse modulated aroma delivery: Do not claim repellency, medical effect, or guaranteed behavioral change.
- `product_validation` Geometry-led surface coating screen: Measure contact angle, surface roughness, and treated versus untreated adhesion.
- `product_validation` Geometry-led surface coating screen: Measure contact angle, surface roughness, and treated versus untreated adhesion.
- `blocked_claim_review` Geometry-led surface coating screen: Do not claim pesticidal, medical, or antimicrobial surface action without validation.
- `product_validation` Dermal permeation geometry screen: Use a permeation assay or literature measurement with irritation and safety review.
- ... 4 additional gaps in JSON report

## Method

Evidence score combines observation confidence, source reliability, and a penalty for contradictions or confounders. It is a readiness score, not a truth claim.
