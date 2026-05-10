# GameZone Analytics

An end-to-end data science portfolio project covering anomaly detection, customer lifetime value modelling, demand forecasting, and churn survival analysis on a real-world e-commerce dataset (21,864 orders · 150 countries · 2019–2021).

Built as part of a data analytics portfolio. Every decision in the code, SQL, and documentation includes a reason, not just a description.

---

## Project narrative

The goal was to answer four questions a real e-commerce business would care about:

1. Is the data trustworthy, and where are the quality issues that would corrupt downstream analysis?
2. Which customers are worth the most, and what drives that value?
3. Can we forecast demand reliably enough to inform inventory and staffing decisions?
4. Which customers are about to leave, and which ones are worth fighting to keep?

The four projects run in sequence — each one builds on cleaned data and findings from the previous.

---

## Stack

| Layer | Tools |
|---|---|
| Language | Python 3.11 |
| Data wrangling | pandas, NumPy |
| Statistics | scipy, statsmodels |
| Machine learning | scikit-learn, LightGBM, SHAP |
| Forecasting | Prophet, ruptures (PELT) |
| Survival analysis | lifelines, scikit-survival |
| CLV modelling | lifetimes (BG/NBD, Gamma-Gamma) |
| Data quality | Great Expectations |
| Visualisation | Matplotlib, Seaborn, Plotly, Tableau, Looker |
| Excel reporting | openpyxl |
| Environment | conda, VS Code |
| Version control | Git, GitHub |

---

## Repository structure

```
gamezone-analytics/
├── data/
│   ├── raw/              # Original source data — never modified after download
│   └── processed/        # Cleaned and feature-engineered outputs
├── notebooks/
│   ├── 01_data_audit/
│   ├── 02_clv_segmentation/
│   ├── 03_demand_forecasting/
│   └── 04_churn_survival/
├── src/
│   └── utils/            # Shared helper functions for data loading and plotting
├── reports/
│   ├── figures/          # Exported charts and visualisations
│   └── excel_outputs/    # Excel deliverables with pivot tables and dashboards
├── docs/                 # Project documentation and methodology notes
├── environment.yml
└── .gitignore
```

---

## Setup

**Requirements:** conda, Python 3.11

**1. Clone the repository**

```bash
git clone https://github.com/selete-tetteh/gamezone-analytics.git
cd gamezone-analytics
```

**2. Create the environment**

```bash
conda env create -f environment.yml
conda activate gamezone-analytics
```

**3. Add the raw data**

Place `gamezone-orders-data.xlsx` in `data/raw/`. This file is git-ignored to protect the source data.

**4. Open in VS Code**

```bash
code .
```

Run notebooks in order — each builds on outputs from the previous. Clear all outputs before committing (Restart Kernel then Clear All Outputs).

---

## Projects

**Project 01 — Data Quality and Anomaly Audit**

Investigates the trustworthiness of the raw dataset before any modelling begins. Quantifies anomalies, resolves duplicate entities, and produces a validated clean master dataset for all downstream projects. The audit itself is treated as a finding, not a silent preprocessing step.

**Project 02 — Customer Lifetime Value Segmentation**

RFM segmentation, BG/NBD CLV modelling, channel ROI attribution, and geographic CLV analysis. Identifies which customers are worth the most and what drives that value across channel, geography, and behaviour.

**Project 03 — Demand Forecasting**

Feature engineering, Prophet baseline, LightGBM model, and model comparison. Forecasts weekly revenue with SHAP explainability on the LightGBM model. Documents the dataset constraints that limit forecast reliability and explains what a richer dataset would require.

**Project 04 — Churn and Survival Analysis**

Churn labelling, Kaplan-Meier survival curves, Cox Proportional Hazards model, and composite risk scoring. Produces a prioritised retention target list segmented by CLV and churn risk.

---

## Key findings

### Project 01 — Data Quality and Anomaly Audit

9.1% of orders (1,997) have a ship date preceding the purchase date. The timezone error hypothesis was rejected — 92.8% of anomalies exceed 10 days, beyond any possible timezone offset. The pre-order fulfilment hypothesis is strongly supported: Nintendo Switch median anomaly is −79 days, PS5 −62 days, both bounded within 0–150 days consistent with gaming hardware pre-order windows. Social media shows the highest anomaly rate (12.7%), consistent with social-driven pre-order campaigns. Anomalous records were flagged with `IS_ANOMALY=True` and retained for revenue analysis but excluded from fulfilment time calculations.

Median order value is $168, mean $281. The $113 gap confirms a right-skewed distribution driven by high-price outliers. 29 orders (0.13%) are priced at exactly $0 — all on the website platform, 20 sharing a single product ID — likely cancelled or test transactions. The top 20 most expensive orders are all Sony PS5 Bundles from GB at up to $3,147, likely GBP recorded without USD conversion. Prices are stable across the full 2019–2021 period with no seasonal discounting detectable.

Fuzzy string matching identified one confirmed duplicate product name — `27inches 4k gaming monitor` standardised to `27in 4K gaming monitor`, correcting 61 misclassified orders. 46 unique product IDs reduced to 9 canonical IDs.

The Great Expectations validation suite runs 41 expectations across 6 categories and passed 39 of 41 (95%). Two critical findings: the US (10,294 orders, the largest market) was entirely absent from the region lookup table — any regional analysis would have silently excluded it. 145 duplicate ORDER_IDs were identified in January 2020 across Nintendo Switch, 27in 4K gaming monitor, and PS5 Bundle — consistent with a batch reprocessing event. Final clean dataset: 21,719 orders after deduplication.

### Project 02 — Customer Lifetime Value Segmentation

K-Means clustering (k=4) on StandardScaler-normalised RFM dimensions across 19,723 customers. Loyal Customers (6.9% of the base) generate 36% of total revenue — classic Pareto distribution. Champions are frequency-driven (avg $435, 2.07 orders). Loyal Customers are spend-driven (avg $1,613, 1.13 orders). 91% of customers ordered exactly once, which required fixed frequency thresholds rather than quintiles. Silhouette score at k=4 was 0.596 — k=2 was mathematically optimal but business-impractical.

98.9% of customers have zero repeat purchases, which severely limits BG/NBD signal. Near-zero CLV predictions are accurate given the data — gaming hardware has 2–4 year repurchase cycles and the dataset spans only two years. RFM segments remain the primary CLV decision tool for this dataset.

Affiliate leads on per-customer value ($343 avg spend, 16.8% high-value customer rate). Affiliate vs Direct is not significantly different (p=0.122) — same customer quality, lower volume. Email underperforms: 15.1% of customers but only 10.0% of revenue (0.66x ROI ratio). Channel is 8.5× stronger as a CLV predictor than geography.

Japan has the highest average spend ($472), best ROI ratio (1.52×), and 455 customers — priority growth market. Denmark (1.33×) and South Korea (1.22×) also punch above their weight. Australia (0.73×), Russia (0.71×), and Mexico (0.69×) underperform on ROI ratio. Segment mix is uniform across all regions — no geographic segmentation signal.

### Project 03 — Demand Forecasting

14,954 orders aggregated into 790 daily and 112 weekly time series rows. Calendar features use cyclical sine/cosine encoding to prevent December and January being treated as numerically far apart. PELT change-point detection identified one structural shift at 2020-02-24 — consistent with COVID-19 lockdown driving a permanent revenue step-change from ~$20K to ~$60K per week. Lag 1 week correlation with revenue: 0.814 — the strongest single predictor. No weekend effect detected.

Prophet trained on 104 weeks (2019–2020), tested on 8 weeks (2021). Training MAPE: 25.1%. Test MAPE: 1,062% — caused by dataset truncation: pre-order orders with future ship dates were excluded from January–February 2021 counts, producing an artificial revenue collapse that is a data artefact, not a genuine business trend.

LightGBM trained on post-change-point data only (40 weeks, 22 features). 3-fold time series cross-validation: mean MAPE 11.6%. Training MAPE 0.83% signals overfitting on a small training window. Top SHAP features: revenue rolling standard deviation at 8 weeks ($2,730), high-ticket percentage ($2,633), month ($1,890). Product mix is the second most important predictor, confirming the Project 02 CLV finding.

Both models predicted December 2020 within 5–10% error — the models are sound, the dataset is the constraint. Prophet is recommended for this dataset due to lower overfitting risk and built-in confidence intervals. LightGBM is recommended for richer datasets (3+ years) where non-linear feature interactions have room to emerge.

### Project 04 — Churn and Survival Analysis

Churn threshold set at 180 days since last purchase — at the 90th percentile of inter-purchase gaps among repeat buyers, with a 180-day floor to account for gaming hardware repurchase cycles. Overall churn rate: 72.5%, reflecting the low-repeat product category rather than business failure. The Lapsed RFM segment shows 100% churn rate, independently validating both the RFM segmentation and the survival analysis definition.

Overall median survival: 1 day, driven by the 91% one-time buyer population. Meaningful metrics are survival probabilities at time horizons: 27.8% still active at 90 days, 18.3% at 365 days. Champions is the only segment with a meaningful survival signal — median 28 days vs 1 day for all other segments. Email channel produces the flattest survival curve — most stable ongoing retention of any channel despite lowest CLV.

Cox model concordance: 0.89. RFM score (HR 0.524, p<0.0001) is the strongest protective factor — each standard deviation increase cuts churn risk nearly in half. High-ticket buyers (HR 0.744, p<0.0001) churn 26% slower. Higher average order value (HR 1.297, p<0.0001) is associated with 30% faster churn, likely reflecting the currency-suspect GB orders identified in Project 01.

Composite risk scoring (40% Cox hazard + 40% recency + 20% inverse RFM) produces scores from 5.2 to 92.0. Priority 1 retention targets — high CLV, high risk — number 3,210 customers with $1.35M revenue at stake. Priority 2 — high CLV, low risk — is the largest stable revenue pool at 4,814 customers and $2.43M.

---

## Limitations

The dataset spans two years with a mid-period structural break (COVID-19 lockdown) and a truncated endpoint caused by pre-order ship date reporting. These constraints limit the reliability of the demand forecast and CLV model — both are documented explicitly in the relevant notebooks rather than obscured. The survival analysis and RFM segmentation are less affected by these constraints and are considered the most production-ready outputs.

---

## Author

Selete Akpotosu-Nartey — [github.com/selete-tetteh](https://github.com/selete-tetteh) · [LinkedIn](https://www.linkedin.com/in/selete-akpotosu-nartey/)
