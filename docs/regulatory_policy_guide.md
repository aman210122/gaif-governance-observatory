# Regulatory Policy Encoding Guide

## Overview

This guide explains how to encode an AI regulation as a machine-readable GAIF Regulatory Policy JSON file.

## The Regulatory Policy Tuple

Each regulation is encoded as:

```
RP = (Jurisdiction, Scope, Requirements, Effective_Date, AI_Risk_Tier, Mapping)
```

## Step-by-Step

### 1. Identify the Regulation

Find the official legal text. Note the formal citation, URL, and effective date.

### 2. Define the Scope

Which AI systems does this regulation affect?

```json
"scope": {
  "deployment_modes": ["all"],
  "data_types": ["personal data", "PHI"],
  "use_case_categories": ["healthcare AI", "employment decisions"],
  "risk_tiers": ["high", "critical"],
  "description": "Plain English description of who this applies to"
}
```

### 3. Encode Requirements

Each requirement gets an ID, obligation text, category, and penalty.

Categories: `transparency`, `disclosure`, `human_oversight`, `bias_testing`, `audit_retention`, `risk_assessment`, `registration`, `data_governance`, `security`, `incident_reporting`, `documentation`

### 4. Map to GAIF Components

Which GAIF architectural components must be configured to satisfy this regulation?

- **compliance_routing_rules**: How should queries be routed?
- **behavioral_contract_thresholds**: What thresholds change?
- **disclosure_requirements**: What must be disclosed to users?
- **monitoring_requirements**: What must be monitored?
- **audit_retention_days**: How long must records be kept?

### 5. Submit

Place your file in the appropriate jurisdiction folder and submit a PR.

## Example

See `observatory/regulations/eu/eu_ai_act.json` for a complete example.

## Schema

See `observatory/regulations/schema.json` for the full JSON schema.

## Reference

GAIF v1.0, Section 6.6. https://doi.org/10.5281/zenodo.19341015
