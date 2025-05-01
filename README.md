# Virtue-Cybernetic Disaster Policy Pipeline

**Author:** Joe Fowler III  
**Dissertation Project — Public Policy & Cybernetic Systems**  
**Focus:** Analyzing virtue stability in disaster relief legislation through PAC, SIG, bureaucratic, and political actor networks.

---

## Project Overview

This project implements a multi-layered data pipeline and modeling system to analyze the stability, ethical responsiveness, and political distortion in U.S. disaster relief policies from 2000 to present.

Built on a theoretical framework integrating:
- **Lyapunov stability** in moral potential fields
- **Cybernetic feedback models**
- **Polycentric governance theory (Ostrom)**
- **Agent-Based Modeling (ABM) and network analytics**

It operationalizes constructs like **virtue potential**, **conversion gain**, and **distortion entropy** using real-world data from:
- FEMA, FEC, OpenSecrets, Census, GAO, LDA filings, etc.

---

## Folder Structure
```bash
virtue-cybernetic-pipeline/
│
├── data/                   # Raw and processed datasets
├── notebooks/              # Exploratory Jupyter notebooks for each actor
├── src/                    # Data ingestion and transformation modules
├── models/                 # Network and ABM models
├── visualizations/         # Static/dynamic graphics and dashboards
├── reports/                # Drafts for dissertation and presentations
├── requirements.txt        # Python packages
├── README.md               # This file
└── .gitignore              # Data/cache exclusions

Core Concepts & Variables
Concept	Variable	Description
Virtue Field	V(x, t):	Composite index of equity, responsiveness, distortion
Virtue Mode	φ_i(x, t):	Domain-specific virtue signals (e.g., care, justice)
Conversion Gain	K_i(x, t):	Actor’s openness to virtue influence
Distortion	D(x, t):	Corruption, delay, mismanagement
Moral Feedback	𝔽_{ij}:	Narrative alignment or coordination across actors
```
---

## Modules

1. build_legislation.py
Collects voting records, sponsorship, and policy metadata

Joins with disaster declaration timeline

2. build_pac_network.py
Extracts PAC contributions and alignments with disaster-related votes

Computes influence weightings per legislator

3. build_sig_lobbying.py
Parses SIG lobbying disclosures

Tracks language and targets related to disaster bills

4. build_fema_response.py
Pulls OpenFEMA, GAO, and budgetary execution data

Calculates time-to-disbursement and error/failure metrics

5. build_constituent_profiles.py
Joins demographic data and disaster severity

Links public opinion where available


