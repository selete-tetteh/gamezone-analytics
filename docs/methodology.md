# Project Methodology Overview

This document summarises the analytical approach and key decisions made across all four projects.

---

## Data source

**GameZone Orders Dataset**
- 21,864 order records · 11 columns · 2019–2021
- 150 countries · 9 products · 2 purchase platforms
- Source: Internal e-commerce transactional data

---

## Data quality baseline (Project 01 findings)

| Issue | Count | % of dataset | Resolution |
|-------|-------|-------------|------------|
| Ship date before purchase date | 1,997 | 9.1% | Investigated — flagged as anomaly cohort |
| $0 price orders | 29 | 0.1% | Excluded (cancelled/test orders) |
| Null USD price | 5 | 0.02% | Excluded |
| Null marketing channel | 83 | 0.4% | Imputed via probabilistic model |
| Duplicate product names | 2 | — | Standardised to canonical name |

---

## Analytical decisions

### Price normalisation
All prices are in USD. No currency conversion required as the dataset is pre-normalised.

### Date handling
`PURCHASE_TS` contains mixed-format strings and was coerced to datetime with `errors='coerce'`. Records with unparseable dates were excluded from time-series analysis.

### Product standardisation
`"27inches 4k gaming monitor"` → `"27in 4K gaming monitor"` (confirmed duplicate via fuzzy matching, Levenshtein distance = 3).

---

## Methodologies by project

### Project 01 — Data Audit
- Great Expectations for schema validation
- Levenshtein distance for entity resolution
- Statistical process control (IQR) for price outlier detection

### Project 02 — CLV Segmentation
- BG/NBD model (Fader & Hardie, 2005) for purchase frequency
- Gamma-Gamma model for expected spend
- K-Means clustering (k selected via elbow + silhouette score)
- Bootstrap confidence intervals for regional CLV comparison

### Project 03 — Demand Forecasting
- Prophet as baseline (additive seasonality)
- LightGBM with lag + rolling features as primary model
- PELT change-point detection (ruptures library) for structural breaks
- SHAP values for feature importance
- MAPE as primary evaluation metric

### Project 04 — Churn & Survival Analysis
- Kaplan-Meier estimator for survival curves by cohort
- Log-rank test for statistical significance between groups
- Cox Proportional Hazards model for multivariate hazard estimation
- XGBoost for churn probability scoring
