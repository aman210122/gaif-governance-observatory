# Contributing to GAIF Governance Observatory

Thank you for your interest in contributing. This project grows through community participation. Whether you encode a regulation, classify an AI system, or report an edge case, your contribution makes AI governance more practical and accessible.

## Four Ways to Contribute

### 1. Encode a Regulation

Pick an AI regulation from your jurisdiction and encode it as a Regulatory Policy JSON file.

**Steps:**
1. Review the schema: `observatory/regulations/schema.json`
2. Study an existing example: `observatory/regulations/eu/eu_ai_act.json`
3. Create a new JSON file in the appropriate jurisdiction folder
4. Fill in all required fields: name, jurisdiction, jurisdiction_type, scope, requirements, effective_date, ai_risk_tier, mapping
5. Submit a PR with title: `reg: Add [Regulation Name] ([Jurisdiction])`

**Guidelines:**
- Use the formal regulation name and citation
- Link to the official legal text URL
- Map each requirement to a GAIF category (transparency, disclosure, human_oversight, etc.)
- Include the GAIF mapping showing which architectural components are affected
- Add your name as contributor

### 2. Classify a Public AI System

Apply the GAIF tier classification algorithm to a well-known AI platform.

**Steps:**
1. Review the schema: `observatory/tier_registry/schema.json`
2. Study existing examples in `observatory/tier_registry/classifications/`
3. Run `python tools/tier_classifier.py` to verify your classification
4. Create a JSON file with your classification and justification
5. Submit a PR with title: `tier: Classify [System Name] ([Vendor])`

**Guidelines:**
- Assign D, T, A values with written justification for each
- Note edge cases where the classification is debatable
- If you disagree with an existing classification, open an Issue first for discussion

### 3. Propose Industry-Specific AAHI Weights

Submit dimension weights calibrated for your industry.

**Steps:**
1. Review the healthcare default: `observatory/aahi_weights/healthcare.json`
2. Create a new JSON file for your industry
3. Provide a rationale for each weight choice
4. Submit a PR with title: `weights: Add [Industry] AAHI weights`

**Guidelines:**
- All weights must sum to 1.0
- Provide written rationale explaining why each dimension gets its weight
- Note the calibration status (analytically derived vs. empirically measured)

### 4. Report Edge Cases

Applied a tool and got a surprising result? Open an Issue.

**Use the Issue templates:**
- "Tier Classification Edge Case" for ambiguous D/T/A assignments
- "Regulatory Encoding Question" for regulations that do not map cleanly to the schema
- "Tool Bug Report" for errors in the computable tools

## Code Contributions

For changes to the Python tools:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Write tests in the `tests/` directory
4. Run tests: `python -m pytest tests/`
5. Submit a PR with a clear description of the change

## Style Guidelines

- Python code follows PEP 8
- JSON files use 2-space indentation
- Regulation files use the ISO date format (YYYY-MM-DD)
- All contributions must include a `contributor` field with name and optionally ORCID

## Code of Conduct

Be respectful, constructive, and collaborative. Disagreements about classifications or regulatory interpretations are expected and welcome. Frame disagreements as professional discussions about governance, not personal criticism.

## Questions?

Open an Issue with the "Question" label or reach out to the maintainer on LinkedIn.
