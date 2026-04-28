# GameZone Analytics

**End-to-end data science portfolio project** — anomaly detection, customer lifetime value modelling, demand forecasting, and churn survival analysis on a real-world e-commerce dataset (21,864 orders · 150 countries · 2019–2021).

---

## Projects

| # | Project | Type | Key techniques |
|---|---------|------|----------------|
| 01 | [Data Quality & Anomaly Audit](notebooks/01_data_audit/) | Exploratory analysis | Great Expectations · entity resolution · temporal forensics |
| 02 | [Customer Lifetime Value Segmentation](notebooks/02_clv_segmentation/) | Clustering & analytics | BG/NBD · K-Means · channel ROI attribution |
| 03 | [Demand Forecasting](notebooks/03_demand_forecasting/) | Predictive modelling | Prophet · LightGBM · SHAP · hierarchical reconciliation |
| 04 | [Churn & Survival Analysis](notebooks/04_churn_survival/) | Survival analysis | Kaplan-Meier · Cox PH · churn risk scoring |

---

## Repository structure

```
gamezone-analytics/
│
├── data/
│   ├── raw/              # Original source data (git-ignored)
│   ├── processed/        # Cleaned, feature-engineered data (git-ignored)
│
├── notebooks/
│   ├── 01_data_audit/
│   ├── 02_clv_segmentation/
│   ├── 03_demand_forecasting/
│   └── 04_churn_survival/
│
├── src/
│   ├── utils/            # Shared helper functions (data loading, plotting)
│
├── reports/
│   ├── figures/          # Exported charts & visualisations
│   └── excel_outputs/    # Excel deliverables with pivot tables & dashboards
│
├── docs/                 # Project documentation & methodology notes
├── environment.yml       # Conda environment — reproduce with one command
└── .gitignore
```

---

## Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/gamezone-analytics.git
cd gamezone-analytics
```

### 2. Create the Conda environment
```bash
conda env create -f environment.yml
conda activate gamezone-analytics
```

### 3. Add the raw data
Place `gamezone-orders-data.xlsx` in `data/raw/`. This file is git-ignored to protect the source data.

### 4. Launch JupyterLab
```bash
jupyter lab
```

Open the notebooks in order — each one builds on outputs from the previous.

---

## Tools & stack

| Layer | Tools |
|-------|-------|
| Language | Python 3.11 |
| Data wrangling | pandas · NumPy |
| Statistics | scipy · statsmodels |
| Machine learning | scikit-learn · LightGBM · SHAP |
| Forecasting | Prophet · ruptures (PELT) |
| Survival analysis | lifelines · scikit-survival |
| CLV modelling | lifetimes (BG/NBD · Gamma-Gamma) |
| Data quality | Great Expectations |
| Visualisation | Matplotlib · Seaborn · Plotly · Tableau · Looker |
| Excel reporting | openpyxl · pivot tables · conditional formatting |
| Environment | Conda · VS Code · JupyterLab |
| Version control | Git · GitHub |

---

## Key findings

> _Populated as each project is completed._

### Project 01 — Data Quality & Anomaly Audit

**Temporal anomalies (Notebook 1)**
- 1,997 orders (9.1%) have a ship date preceding the purchase date
- Timezone error hypothesis rejected — 92.8% of anomalies exceed 10 days, beyond any possible timezone offset
- Pre-order fulfilment hypothesis strongly supported — Nintendo Switch median anomaly: -79 days, PS5: -62 days, both bounded within 0–150 days consistent with gaming hardware pre-order windows
- Social media channel shows the highest anomaly rate (12.7%) — consistent with social-driven pre-order campaigns
- India (11.9%), Switzerland (12.2%), and South Korea (11.1%) show above-average anomaly rates
- Decision: anomalous records flagged with `IS_ANOMALY=True` and retained for revenue analysis; excluded from fulfilment time calculations

**Price forensics (Notebook 2)**
- Median order value: $168. Mean: $281. The $113 gap confirms right-skewed distribution driven by high-price outliers
- 29 orders (0.13%) priced at exactly $0 — all on website platform, 20 sharing a single product ID — likely cancelled or test transactions
- 1,681 orders exceed the per-product IQR upper fence — flagged as `IS_PRICE_OUTLIER=True`
- Top 20 most expensive orders are all Sony PS5 Bundles from GB, prices up to $3,147 — likely GBP recorded without USD conversion
- Channel has no influence on price — all channels median $168; pricing is entirely product-driven
- Prices stable across entire 2019–2021 period — no seasonal discounting detectable

**Entity resolution (Notebook 3)**
- Fuzzy string matching identified one confirmed duplicate product name: `27inches 4k gaming monitor` → standardised to `27in 4K gaming monitor` (61 misclassified orders corrected)
- 46 unique product IDs reduced to 9 canonical IDs — Nintendo Switch had the most variants (12 IDs)
- Clean master dataset exported: `orders_clean_master.csv` — used by all subsequent projects

**Validation pipeline (Notebook 4)**
- Formal Great Expectations suite: 41 expectations across 6 categories (schema, completeness, value ranges, valid categories, business rules, statistical properties) — 39/41 passed (95%)
- **Critical finding:** US (10,294 orders) was entirely absent from the region lookup table — any regional analysis would have silently excluded the largest market in the dataset. All 15 missing country codes manually mapped, 0 NaN regions remaining
- **Critical finding:** 145 duplicate ORDER_IDs identified, all in January 2020, across Nintendo Switch (98 pairs), 27in 4K gaming monitor (37 pairs), and PS5 Bundle (10 pairs) — consistent with a batch reprocessing event. Deduplicated by keeping first occurrence
- Final clean dataset: 21,719 orders (reduced from 21,864 after duplicate removal)
- Validation pipeline designed to be re-run on any future data refresh to immediately catch quality regressions

### Project 02 — Customer Lifetime Value Segmentation

**RFM Segmentation (Notebook 1)**
- K-Means clustering (k=4) on StandardScaler-normalised RFM dimensions across 19,723 customers
- Loyal Customers (6.9% of base) generate 36% of total revenue — classic Pareto distribution
- Champions are frequency-driven (avg $435, 2.07 orders) — not spend-driven
- Loyal Customers are spend-driven (avg $1,613, 1.13 orders) — one high-ticket purchase
- 91% of customers ordered exactly once — frequency scoring required fixed thresholds, not quintiles
- Silhouette score at k=4: 0.596 — k=2 was mathematically optimal but business-impractical

**BG/NBD CLV Modelling (Notebook 2)**
- 98.9% of customers (8,733 of 8,826) have zero repeat purchases — BG/NBD signal severely limited
- Model fitted and validated correctly — near-zero CLV predictions accurately reflect the data
- Product category constraint: gaming hardware has 2-4 year repurchase cycles; 2-year dataset is insufficient
- Loyal Customers show 98.4% probability still active — retention focus confirmed
- RFM segments remain the primary CLV decision tool for this dataset

**Channel ROI Attribution (Notebook 3)**
- Kruskal-Wallis H=375.60, p<0.0001 — channel spend differences are statistically significant
- Affiliate leads on per-customer value: $343 avg spend, 16.8% high-value customer rate
- Affiliate vs Direct: NOT significantly different (p=0.122) — same customer quality, lower volume
- Email underperforms: 15.1% of customers but only 10.0% of revenue (0.66x ROI ratio)
- Email Loyal Customer rate (2.8%) is 3× lower than affiliate (7.8%) and direct (7.7%)
- Channel is 8.5× stronger CLV predictor than geography (68% gap vs 8% gap)

**Geographic CLV Analysis (Notebook 4)**
- Bootstrap 95% CIs confirm LATAM estimate uncertainty (CI width: $49 vs $16 for Americas)
- Japan: highest avg spend ($472), best ROI ratio (1.52x), 455 customers — priority growth market
- Denmark (1.33x) and South Korea (1.22x) also punch above their weight
- Australia (0.73x), Russia (0.71x), Mexico (0.69x) underperform on ROI ratio
- Segment mix is uniform across all regions (~9% Champions, ~7% Loyal) — no geographic segmentation signal
- APAC vs LATAM not significantly different (p=0.72) — regional hierarchy less clear than it appears

### Project 03 — Demand Forecasting

**Feature Engineering (Notebook 1)**
- Aggregated 14,954 orders into 790 daily and 112 weekly time series rows
- Calendar features include cyclical sine/cosine encoding for month and day of week — prevents December and January being treated as numerically far apart
- Lag features at 1, 2, 4, and 8 weeks with explicit data leakage prevention via `.shift()`
- Rolling mean and standard deviation features at 4, 8, and 13-week windows
- PELT change-point detection identified one structural shift at 2020-02-24 — consistent with COVID-19 lockdown driving a permanent revenue step-change from ~$20K to ~$60K per week
- Lag 1 week correlation with revenue: 0.814 — strongest single predictor
- No weekend effect detected — revenue flat across all days of the week (max difference $302)
- Product mix feature: high-ticket order percentage averages 7.3% per week, max 15.8%

**Prophet Baseline (Notebook 2)**
- Trained on 104 weeks (2019-01-07 to 2020-12-28), tested on 8 weeks (2021-01-04 to 2021-02-22)
- COVID change-point (2020-02-24) provided explicitly; seasonality mode set to multiplicative
- Training MAPE: 25.1%, MAE: $5,728/week — reasonable fit given dataset constraints
- Test MAPE: 1,062% — caused by dataset truncation: pre-order orders with future ship dates excluded from January-February 2021 counts, producing an artificial revenue collapse
- Components decomposition confirms yearly seasonality with December peak and weekly seasonality with no meaningful day-of-week pattern

**LightGBM Model (Notebook 3)**
- Trained on post-change-point data only (2020-03-02 to 2020-11-30) — 40 weeks, 22 features
- 3-fold time series cross-validation: mean MAPE 11.6%, mean MAE $7,874/week — most reliable performance estimate
- Training MAPE: 0.83% — signals overfitting on 40 training weeks with 22 features
- Top features by SHAP: revenue_roll_std_8 ($2,730), high_ticket_pct ($2,633), month ($1,890)
- Product mix is the second most important predictor — confirms Project 02 CLV finding that what is selling matters as much as how much is selling
- is_weekend, is_month_end, is_q4, and regime all have zero SHAP value — no predictive contribution
- Test MAPE: 339% — same dataset truncation issue as Prophet

**Model Comparison (Notebook 4)**
- Both models predicted December 2020 within 5-10% error — models are sound, dataset is the constraint
- LightGBM outperformed Prophet on shared test window: MAPE 340% vs 710% — lag features self-correct as actuals fall, Prophet continues projecting trained trend
- Prophet recommended for this dataset: lower overfitting risk, built-in confidence intervals, no manual feature engineering required
- LightGBM recommended for richer datasets (3+ years): captures non-linear feature interactions, SHAP explainability provides deeper business insight
- Production recommendation: ensemble both models — weighted average typically outperforms either model alone
- Dataset limitation confirmed: 2-year dataset with mid-period structural break and truncated endpoint is insufficient for production-quality forecasting

### Project 04 — Churn and Survival Analysis

**Churn Labelling (Notebook 1)**
- Churn threshold: 180 days since last purchase — set at 90th percentile of inter-purchase gaps among repeat buyers with a 180-day floor to account for gaming hardware repurchase cycles
- Overall churn rate: 72.5% (9,993 of 13,778 customers) — reflects low-repeat product category, not business failure
- Lapsed RFM segment shows 100% churn rate — independently validates both the RFM segmentation from Project 02 and the survival analysis churn definition
- Email channel has the lowest churn rate (66.5%) despite having the lowest CLV — email attracts lower-spend but longer-tenure customers
- Social media has the highest churn rate (79.0%) — impulsive buyers who do not return

**Kaplan-Meier Survival Analysis (Notebook 2)**
- Overall median survival: 1 day — driven by 91% one-time buyer population; meaningful metric is survival probability at time horizons (27.8% still active at 90 days, 18.3% at 365 days)
- Champions is the only segment with meaningful survival signal — median 28 days vs 1 day for all other segments
- All three stratifications (segment, channel, region) are statistically significant (all p < 0.05)
- LATAM shows unexpectedly flat survival curve after day 200 — customers who survive the initial drop are extremely long-tenured
- Email channel produces the flattest survival curve — most stable ongoing retention of any channel

**Cox Proportional Hazards Model (Notebook 3)**
- Concordance: 0.89 — model correctly ranks which customer churns sooner in 89% of pairwise comparisons
- RFM_score: HR 0.524 (p<0.0001) — strongest protective factor; each standard deviation increase in RFM score cuts churn risk nearly in half
- is_high_ticket_buyer: HR 0.744 (p<0.0001) — PS5 and laptop buyers churn 26% slower, confirming they are more engaged customers
- avg_order_value: HR 1.297 (p<0.0001) — higher average prices associated with 30% faster churn, likely reflecting currency-suspect GB orders from Project 01
- Email (HR 0.881), APAC (HR 0.909), EMEA (HR 0.927) all significantly protective
- Direct and affiliate channels not significantly different from each other — confirms Project 02 equivalence finding
- Proportional hazards assumption holds for 9 of 10 features; total_orders violates assumption

**Churn Risk Scoring (Notebook 4)**
- Composite risk score (0-100): 40% Cox hazard + 40% recency + 20% inverse RFM
- Mean risk score: 39.8, range 5.2 to 92.0 — well-distributed scoring system
- Champions avg risk score 26.1 vs Lapsed 66.9 — 40-point gap validates RFM as churn proxy
- Priority 1 (High CLV / High Risk): 3,210 customers, $1.35M revenue at stake — primary retention target
- Priority 2 (High CLV / Low Risk): 4,814 customers, $2.43M revenue — largest stable revenue pool
- Critical tier customers (753, avg spend $94) do not justify heavy retention investment
- Low tier customers (3,623) show only 15% churn rate and $456 avg spend — protect these customers

---

## Methodology

Full write-ups for each project are in [`docs/`](docs/). Each notebook follows the structure:

1. Data loading & validation
2. Exploratory analysis
3. Modelling / analysis
4. Results & interpretation
5. Recommendations

---

## Author

**Selete Akpotosu Nartey**  
[LinkedIn](https://www.linkedin.com/in/selete-akpotosu-nartey/) · [GitHub](https://github.com/selete-tetteh)
