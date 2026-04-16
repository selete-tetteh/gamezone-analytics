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
│   └── sql/              # Schema definitions & seed scripts
│
├── notebooks/
│   ├── 01_data_audit/
│   ├── 02_clv_segmentation/
│   ├── 03_demand_forecasting/
│   └── 04_churn_survival/
│
├── src/
│   ├── utils/            # Shared helper functions (data loading, plotting)
│   └── queries/          # Reusable SQL query templates
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
| Language | Python 3.11 · SQL (MySQL) |
| Data wrangling | pandas · NumPy · SQLAlchemy |
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

- **Project 03:** TBC
- **Project 04:** TBC

---

## Methodology

Full write-ups for each project are in [`docs/`](docs/). Each notebook follows the structure:

1. Business question
2. Data loading & validation
3. Exploratory analysis
4. Modelling / analysis
5. Results & interpretation
6. Recommendations

---

## Author

**Selete Akpotosu Nartey**  
[LinkedIn](https://www.linkedin.com/in/selete-akpotosu-nartey/) · [GitHub](https://github.com/selete-tetteh)
