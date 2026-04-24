# Excel Workbook Schema

Use one workbook with stable sheet names. The exporter expects the first row to contain these exact column names.

## BiologicalDefinitions

| Column | Purpose |
| --- | --- |
| bio_id | Stable ID, such as `BIO-FLY-ATTRACTANT`. |
| term | Biological term or observed effect. |
| category | Taxonomy, receptor, behavior, pathway, phenotype, habitat, safety, or other category. |
| definition | Plain-language definition. |
| confirmation_role | How this validates a geometry match. |
| safety_notes | Known hazards, limits, or required review. |
| source_ids | Comma-separated IDs from `Sources`. |

## GeometrySignatures

| Column | Purpose |
| --- | --- |
| geometry_id | Stable ID, such as `GEO-VOLATILE-PLUME-NARROW`. |
| geometry_name | Human-readable geometry name. |
| section | Obsidian grouping, such as `Volatile Plumes`, `Surface Films`, `Binding Pockets`, or `Temporal Pulses`. |
| shape_class | Point, line, plane, cavity, lattice, plume, cluster, spiral, gradient, waveform, etc. |
| symmetry | Radial, bilateral, chiral, asymmetric, periodic, fractal, etc. |
| topology | Connectedness, holes, channels, branching, enclosure, interface, etc. |
| scale | Molecular, cellular, organism, room, landscape, time-series, etc. |
| polarity_pattern | Hydrophobic, hydrophilic, amphiphilic, charge distribution, volatile polarity, etc. |
| dynamics | Static, diffusive, evaporative, oscillating, adhesive, turbulent, aggregating, etc. |
| match_features | Key measurable features used by agents. |
| exclusion_features | Geometry features that reject a match. |

## CandidateMaterials

| Column | Purpose |
| --- | --- |
| candidate_id | Stable ID. |
| name | Material, recipe, food, compound, surface, plant, or product concept input. |
| candidate_type | Food, recipe, botanical, molecule, material, surface, device, observation, etc. |
| geometry_ids | Comma-separated IDs from `GeometrySignatures`. |
| bio_ids | Comma-separated IDs from `BiologicalDefinitions`. |
| notes | Research notes. |
| safety_status | Unknown, low concern, needs review, restricted, or rejected. |
| source_ids | Comma-separated IDs from `Sources`. |

## Observations

| Column | Purpose |
| --- | --- |
| observation_id | Stable ID. |
| candidate_id | ID from `CandidateMaterials`. |
| geometry_id | ID from `GeometrySignatures`. |
| bio_id | ID from `BiologicalDefinitions`. |
| context | Where/how the observation occurred. |
| observed_pattern | What pattern was observed. |
| confidence | Low, medium, high, or numeric score. |
| contradiction | Evidence against the match. |
| source_ids | Comma-separated IDs from `Sources`. |

## Sources

| Column | Purpose |
| --- | --- |
| source_id | Stable ID. |
| title | Source title or lab note title. |
| source_type | Paper, book, URL, lab note, recipe, observation, dataset, etc. |
| url_or_path | URL or local path. |
| reliability | Low, medium, high, peer-reviewed, anecdotal, unverified, etc. |
| notes | Source notes. |

## ProductIdeas

| Column | Purpose |
| --- | --- |
| idea_id | Stable ID. |
| title | Product or research concept title. |
| geometry_ids | Geometry IDs driving the idea. |
| candidate_ids | Candidate material IDs. |
| intended_domain | Household, food, agriculture, medical research, material science, etc. |
| concept_note | Non-actionable concept description. |
| required_validation | Tests, measurements, safety review, regulatory review, or evidence gaps. |
| blocked_claims | Claims that must not be made yet. |

