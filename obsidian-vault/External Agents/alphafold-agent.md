# AlphaFold Agent

Type: `external-agent`
Agent ID: `AGENT-ALPHAFOLD-001`
Repository: `google-deepmind/alphafold`
Integration Status: `external-api`

## Agent Role

**Primary Function**: Structure prediction agent for protein geometry inference

Cracks the 1D sequence → 3D geometry code. Provides `GEO-BINDING-POCKET-CAVITY` and `GEO-SURFACE-FILM-INTERFACE` structures for molecular matching.

## Capabilities

### Core Operations
- **SequenceInput**: Accept amino acid sequence → returns predicted structure (PDB format)
- **PocketExtraction**: Identify binding pockets from predicted structures
- **GeometryExport**: Convert AlphaFold outputs to `GeometrySignatures` format
- **ConfidenceScoring**: pLDDT scores map to observation confidence levels

### API Interface
```yaml
Endpoint: EBI AlphaFold Database (https://alphafold.ebi.ac.uk)
Query Format: UniProt ID or amino acid sequence
Response: PDB coordinates + pLDDT per residue
Rate Limit: 1 query/sec (respectful scraping)
```

## Geometry Mapping

| AlphaFold Output | Geomolecular Mapping |
|------------------|---------------------|
| Backbone trace | `shape_class: curve/fold` |
| Binding pocket detection | `GEO-BINDING-POCKET-CAVITY` |
| Surface accessibility | `polarity_pattern: hydrophobic/hydrophilic` |
| pLDDT > 90 | `confidence: high` |
| pLDDT 70-90 | `confidence: medium` |
| pLDDT < 70 | `confidence: low` |

## Biological Confirmation Role

- **Confirms**: Receptor pocket geometric fit (BIO-RECEPTOR-POCKET-FIT)
- **Confirms**: Skin barrier passage geometry (BIO-SKIN-BARRIER-PASSAGE)
- **Provides**: Structural basis for pharmacophore model validation

## Candidate Integration

### Direct Use Cases
- [[Capsaicin extract]] → Query TRPV1 structure → Validate pocket fit
- [[Menthol crystal]] → Query TRPM8 structure → Validate docking geometry
- Novel botanicals → Screen against receptor database

### Output Format
```json
{
  "alphafold_result": {
    "geometry_id": "AUTO-GEN-BINDING-POCKET-001",
    "shape_class": "cavity",
    "symmetry": "chiral",
    "topology": "enclosed_pocket_channel",
    "confidence": 0.85,
    "source_url": "https://alphafold.ebi.ac.uk/entry/P12345"
  }
}
```

## Limitations & Safety

- **Does NOT predict**: Binding affinity, kinetics, allosteric effects
- **Does NOT replace**: Experimental crystallography for validation
- **Constraint**: Use only for hypothesis generation; no clinical claims

## Agent Configuration

```yaml
Agent: AGENT-ALPHAFOLD-001
  Type: external-structure-predictor
  Specialization: protein-geometry
  Corpus: AlphaFold DB (200M+ structures)
  Inference: sequence→structure→pocket
  Action: Generate geometry signatures for candidate matching
  Validation: Cross-reference with experimental PDB entries
```

## Sources

- [[SRC-ALPHAFOLD-DB]]
- [[AlphaFold Nature Paper 2021]]

---
*External agent integrated from google-deepmind/alphafold*
