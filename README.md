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

- **Project 01:** TBC
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

**Selete Akpotosu-Nartey**  
[LinkedIn](https://linkedin.com/in/selete-akpotosu-nartey/) · [GitHub](https://github.com/selete-tetteh)
