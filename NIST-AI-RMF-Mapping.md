# GAIF-4 to NIST AI RMF Mapping

**How GAIF-4 metrics operationalize the NIST AI Risk Management Framework for clinical AI systems**

Version: 1.0
Date: April 2026
Author: Aman Sharma
Parent Specification: GAIF-4 v1.5 (Zenodo DOI: 10.5281/zenodo.19378438)
License: Apache 2.0

---

## Overview

The NIST AI Risk Management Framework (AI RMF 1.0, January 2023) provides a voluntary, principle-based framework for managing risks associated with AI systems. It defines four core functions: Govern, Map, Measure, and Manage.

GAIF-4 provides four computable metrics designed for clinical AI governance: EMR (Emergent Misinformation Rate), T1PR (Tier-1 Performance Ratio), CFR (Compliance Failure Rate), and GDR (Governance Decay Rate).

This document maps GAIF-4 metrics and governance controls to the NIST AI RMF functions and categories, showing how GAIF-4 serves as a **measurement and implementation layer** that operationalizes NIST's abstract governance recommendations specifically for multi-agent clinical AI systems in healthcare.

GAIF-4 does not replace NIST AI RMF. It complements it by providing the concrete measurement tools that NIST recommends but does not itself supply.

---

## Core Function Mapping

### GOVERN: Policies, Processes, Procedures, and Practices

NIST AI RMF GOVERN establishes and maintains AI risk management policies and organizational structures.

| NIST Category | NIST Description | GAIF-4 Implementation |
|---------------|------------------|----------------------|
| GOVERN 1: Policies | Legal and regulatory requirements are understood and inform AI risk management | GAIF-4 regulatory compliance mappings connect governance metrics to HIPAA, state AI laws (CA AB 3030, TX TRAIGA), and Joint Commission/CHAI guidelines. Organizations using GAIF-4 can trace their metric thresholds directly to regulatory obligations. |
| GOVERN 2: Accountability | Roles and responsibilities for AI risk management are established | GAIF-4 Control C3.5 (Governance Ownership Registry) provides a structured approach to assigning ownership of each governance control, with escalation procedures for ownership changes. GDR subcategory T3.5 (Organizational Decay) specifically measures the risk of governance degradation due to personnel changes. |
| GOVERN 3: Workforce | AI risk management workforce is trained and capable | GAIF-4's open-source toolkit (59 tests) provides a standardized, executable governance validation suite that workforce members can run without specialized AI expertise. The toolkit reduces the barrier to governance participation. |
| GOVERN 4: Organizational Context | Organizational context is understood and informs risk management | GAIF-4's four metrics are designed for healthcare-specific organizational contexts. EMR addresses clinical safety, CFR addresses regulatory compliance (HIPAA/CMIA), GDR addresses operational governance sustainability, and T1PR addresses multi-agent pipeline reliability. Each metric is calibrated to healthcare-specific risk tolerances. |
| GOVERN 5: Processes | Processes for risk management are established and maintained | GDR (Governance Decay Rate) directly measures whether governance processes are being maintained over time. A rising GDR indicates that established processes are degrading, triggering remediation before failures occur. This is the only known computable metric for continuous governance process health in clinical AI. |
| GOVERN 6: Plans and Documentation | Plans and documentation are maintained | GAIF-4's specification (Zenodo DOI: 10.5281/zenodo.19378438) provides a published, version-controlled governance standard that organizations can adopt as their documentation baseline. Version history and DOI assignment provide audit-grade documentation lineage. |

**Key value add:** NIST GOVERN recommends continuous governance monitoring but does not provide measurement tools. GDR fills this gap by providing a computable, recurring metric for governance health.

---

### MAP: Context, Scope, and Risk Identification

NIST AI RMF MAP identifies and documents AI risks within the organizational context.

| NIST Category | NIST Description | GAIF-4 Implementation |
|---------------|------------------|----------------------|
| MAP 1: Intended Purpose | AI system purposes and expected benefits are documented | GAIF-4's metric selection framework helps organizations identify which metrics apply to their specific AI deployment. Clinical decision support systems require EMR monitoring. Multi-agent pipelines require T1PR monitoring. Any system handling patient data requires CFR monitoring. All production systems require GDR monitoring. |
| MAP 2: Interdependencies | Interdependencies between AI components are identified | T1PR directly measures inter-agent dependencies by comparing individual agent performance to composed pipeline performance. Gap inversions (where the pipeline performs worse than individual agents) reveal destructive interdependencies that are invisible without compositional measurement. |
| MAP 3: Risks and Impacts | AI risks and potential impacts are identified and documented | GAIF-4's threat taxonomy (five classes: EMG, Contamination Percolation, Governance Decay, PHI Exposure, and Governance Non-Compositionality) provides a structured risk identification framework specific to clinical AI. Each threat class includes subcategories, severity ratings, and clinical impact assessments. |
| MAP 4: Likelihood and Severity | Risks are assessed for likelihood and severity | GAIF-4's severity classification guide (SEV-1 through SEV-4) provides a healthcare-calibrated severity framework tied to clinical impact. SEV-1 (Critical) triggers immediate pipeline halt. SEV-2 (High) requires 24-hour response. This calibration reflects healthcare-specific risk tolerances that generic AI frameworks do not address. |
| MAP 5: Benefits and Costs | Benefits and costs of AI risk management are assessed | GDR provides a quantitative basis for cost-benefit analysis of governance investments. Organizations can measure whether governance spending is preventing decay (low GDR) or whether governance controls are degrading despite investment (high GDR), enabling evidence-based governance budgeting. |

**Key value add:** NIST MAP recommends risk identification but operates at an abstract level. GAIF-4 provides a concrete, healthcare-specific threat taxonomy with five empirically validated threat classes derived from experiments on real clinical data (MIMIC-IV).

---

### MEASURE: Assessment, Analysis, and Monitoring

NIST AI RMF MEASURE assesses, analyzes, and monitors AI risks using appropriate metrics and methods.

| NIST Category | NIST Description | GAIF-4 Implementation |
|---------------|------------------|----------------------|
| MEASURE 1: Appropriate Metrics | Appropriate metrics are identified and applied | GAIF-4 provides four computable metrics specifically designed for clinical AI governance. Each metric has a defined formula, measurement methodology, threshold guidance, and empirical validation data. See metric detail table below. |
| MEASURE 2: AI Systems are Evaluated | AI systems are evaluated for trustworthiness | EMR evaluates clinical trustworthiness by measuring the rate at which multi-agent systems generate false clinical assertions. CFR evaluates compliance trustworthiness by measuring PHI exposure rates. T1PR evaluates compositional trustworthiness by measuring whether agent composition degrades performance. |
| MEASURE 3: Risks are Tracked | Identified risks are tracked over time | GDR is explicitly designed for longitudinal risk tracking. It measures governance control health on a recurring schedule, enabling trend analysis and early warning of governance degradation before clinical incidents occur. |
| MEASURE 4: Feedback | Feedback about AI system performance is collected and used | GAIF-4's toolkit provides automated test execution with pass/fail results that feed directly into governance dashboards. The 59-test suite covers metric computation, threshold validation, and control verification, providing structured performance feedback. |

#### GAIF-4 Metric Detail for NIST MEASURE

| Metric | Full Name | What It Measures | Empirical Validation | Threshold Guidance |
|--------|-----------|------------------|---------------------|-------------------|
| EMR | Emergent Misinformation Rate | Rate of false clinical assertions emerging from multi-agent composition (not attributable to any single agent) | 97,000 API calls; 10 experiments; MIMIC-IV real patient data; 74 CRITICAL drug interactions discovered | Any EMR > 0 in clinical decision support contexts triggers SEV-1 review |
| T1PR | Tier-1 Performance Ratio | Performance gap between individual agents and composed pipeline | 210,000 API calls; DBRX, Claude, Llama, Gemini model families; range +55 to -62 observed | Negative T1PR (gap inversion) triggers SEV-2 investigation |
| CFR | Compliance Failure Rate | Rate of regulatory compliance violations in LLM interactions, with focus on PHI exposure | 30,000 MIMIC-IV clinical queries; zero PHI violations achieved; distribution-free bound 0.00534 | CFR must remain below organization's risk tolerance; PHI-GUARD provides conformal prediction bounds |
| GDR | Governance Decay Rate | Rate at which governance controls degrade over time in production | Changelog analysis of 3 major AI platform vendors; all exceeded targets; pipeline GDR 4.6x critical threshold | GDR > 1.0x critical threshold triggers SEV-2; GDR > 2.0x triggers SEV-1 |

**Key value add:** NIST MEASURE recommends appropriate metrics but does not prescribe specific measurements. GAIF-4 provides four validated, computable metrics with empirical baselines from real clinical data. This is the primary gap that GAIF-4 fills in the NIST framework.

---

### MANAGE: Prioritize, Respond, and Recover

NIST AI RMF MANAGE prioritizes and acts on identified AI risks.

| NIST Category | NIST Description | GAIF-4 Implementation |
|---------------|------------------|----------------------|
| MANAGE 1: Risks are Prioritized | AI risks are prioritized based on impact and likelihood | GAIF-4's severity classification (SEV-1 through SEV-4) provides a healthcare-calibrated prioritization framework. Clinical impact determines priority: life-threatening potential (SEV-1) takes precedence over operational disruption (SEV-3). |
| MANAGE 2: Strategies to Respond | Strategies to manage AI risks are planned and implemented | GAIF-4 defines 25 governance controls (C1.1-C1.5, C2.1-C2.5, C3.1-C3.5, C4.1-C4.5, C5.1-C5.5) mapped to specific threat classes. Each control includes implementation guidance. Organizations select controls based on their threat exposure profile. |
| MANAGE 3: Risks are Monitored | Managed AI risks are monitored on an ongoing basis | GDR provides continuous monitoring of whether risk management controls remain effective over time. Unlike point-in-time assessments, GDR tracks governance health longitudinally, detecting degradation trends before they result in incidents. |
| MANAGE 4: Risk Treatments | Risk treatments are documented and communicated | GAIF-4's control-to-threat mapping provides a documented treatment plan for each identified risk. The threat interaction matrix identifies cascading risks that require coordinated treatment across multiple threat classes. |

**Key value add:** NIST MANAGE recommends risk response strategies but does not provide healthcare-specific controls. GAIF-4's 25 controls are designed for clinical AI contexts and address threats (emergent misinformation, PHI exposure, governance decay) that generic AI frameworks do not specifically target.

---

## Summary: Where GAIF-4 Adds Value to NIST AI RMF

| NIST Function | What NIST Provides | What NIST Lacks | What GAIF-4 Adds |
|---------------|-------------------|-----------------|-----------------|
| GOVERN | Principles for AI governance policies and structures | No computable metric for governance health over time | GDR: continuous, automated measurement of governance control decay |
| MAP | Abstract risk identification guidance | No healthcare-specific threat taxonomy for multi-agent clinical AI | Five empirically validated threat classes with 25 subcategories |
| MEASURE | Recommendation to use appropriate metrics | No specific metrics; no measurement methodologies; no empirical baselines | Four computable metrics (EMR, T1PR, CFR, GDR) with formulas, thresholds, and validation data from 337,000+ API calls on MIMIC-IV clinical data |
| MANAGE | Guidance to prioritize and respond to risks | No healthcare-calibrated severity framework; no clinical AI-specific controls | SEV-1 through SEV-4 severity classification; 25 governance controls mapped to threats and regulatory requirements |

---

## Regulatory Cross-Reference

Organizations using GAIF-4 to operationalize NIST AI RMF can simultaneously address the following regulatory requirements:

| Regulation | GAIF-4 Metrics Applicable | GAIF-4 Controls Applicable |
|------------|--------------------------|---------------------------|
| HIPAA Security Rule (45 CFR 164) | CFR | C4.1, C4.2, C4.3, C4.4, C4.5 |
| HIPAA Privacy Rule (45 CFR 160, 164) | CFR | C4.1, C4.2, C4.4 |
| California AB 3030 (eff. Jan 2025) | EMR, CFR | C1.5, C4.3 |
| California SB 1120 (eff. Jan 2025) | GDR | C3.3, C3.5 |
| Texas TRAIGA (eff. Jan 2026) | EMR, GDR, CFR | C1.5, C3.1, C4.1 |
| Joint Commission / CHAI Guidelines (2025) | All | All |
| FDA SaMD Guidance / PCCP | GDR | C3.1, C3.2, C3.4 |
| NIST Cyber AI Profile (NISTIR 8596, draft) | T1PR, GDR, CFR | C2.4, C3.1-C3.4, C4.1-C4.5 |

---

## How to Use This Mapping

**If you are already using NIST AI RMF:** Add GAIF-4 metrics as the measurement layer for your existing GOVERN, MAP, MEASURE, and MANAGE processes. Start with GDR for continuous governance monitoring and CFR for compliance measurement.

**If you are starting fresh:** Use NIST AI RMF as your organizational governance framework and GAIF-4 as your measurement and implementation toolkit. The GAIF-4 open-source toolkit (github.com/aman210122/gaif-governance-observatory) provides executable tests to validate your governance controls.

**If you are in a regulated healthcare environment:** Use the regulatory cross-reference table to identify which GAIF-4 metrics and controls address your specific compliance obligations. Map your existing compliance processes to GAIF-4 controls to identify gaps.

---

## References

1. NIST. (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). NIST AI 100-1. https://www.nist.gov/artificial-intelligence/ai-risk-management-framework
2. NIST. (2025). Cybersecurity Framework Profile for Artificial Intelligence (NISTIR 8596). Preliminary Draft.
3. Sharma, A. (2026). GAIF-4 v1.5: Governed AI Architecture Framework. Zenodo. DOI: 10.5281/zenodo.19378438.
4. Sharma, A. (2026). GAIF v1.0: Governed AI Architecture Framework. Zenodo. DOI: 10.5281/zenodo.19341015.

---

*This mapping document is part of the GAIF Governance Observatory project. For the full specification, metrics, and toolkit, visit github.com/aman210122/gaif-governance-observatory.*
