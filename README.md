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

- **Project 02:** TBC
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
