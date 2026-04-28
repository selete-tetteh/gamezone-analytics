# GameZone Analytics — Setup Guide
## From absolute zero to ready for Project 01

This guide assumes nothing is set up. Follow every step in order.
If you have already completed a step, you can skip it — but read the
explanation so you understand what it does.

---

## Step 1 — Check if Git is installed

Open your terminal and run:

```bash
git --version
```

**What this does:**
Prints the installed Git version if it exists. Git is the software that
tracks every change you make to your code over time — like a detailed undo
history for your entire project. Every professional data team uses it.

**If you see a version number (e.g. git version 2.39.5):**
Git is already installed. Move to Step 2.

**If you see "command not found":**
Install Git via Homebrew by running:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git
```

Homebrew is a package manager for Mac — it installs command-line tools
cleanly and safely. The first command installs Homebrew itself, the second
uses it to install Git. Once done, restart your terminal and re-run
`git --version` to confirm.

---

## Step 2 — Configure your Git identity

Run these two commands, replacing the values with your own name and email:

```bash
git config --global user.name "Selete Tetteh"
git config --global user.email "narteykwasi@gmail.com"
```

**What this does:**
Every commit (saved snapshot) you make is permanently stamped with your
name and email. This is how GitHub knows the work belongs to you and
displays it correctly on your profile. The --global flag means this
applies to every Git project on your Mac, not just this one.

---

## Step 3 — Check if Conda is installed

Run:

```bash
conda --version
```

**What Conda is and why it matters:**
Your Mac has one system-wide Python installation. If every project used
it, packages would constantly conflict — Project A needs pandas version
1.5, Project B needs version 2.2, and they cannot both be installed at
the same time. Conda solves this by creating completely isolated,
self-contained Python environments per project. When you activate the
gamezone-analytics environment, you step into a bubble where only this
project's exact packages exist.

**If you see a version number (e.g. conda 23.3.1):**
Conda is already installed. Move to Step 4.

**If you see "command not found":**
Install Miniconda (the lightweight version of Conda):

1. Go to: https://docs.conda.io/en/latest/miniconda.html
2. Download the installer for your Mac:
   - Apple Silicon (M1/M2/M3 chip): choose the "Apple M1" pkg file
   - Intel chip: choose the "Intel x86" pkg file
3. Run the downloaded installer and follow the prompts
4. When asked "Do you wish the installer to initialize Miniconda3?" — say yes
5. Close your terminal completely and reopen it
6. Run `conda --version` again to confirm it worked

> Note: If you have Anaconda installed instead of Miniconda, that is fine.
> Anaconda and Miniconda use the exact same conda command. Anaconda is just
> the larger version with more pre-installed packages. No action needed.

---

## Step 4 — Create the project folder structure

Now we build the skeleton of your project on your Mac. We will put
everything inside a folder called gamezone-analytics.

First, decide where you want the project to live. We will use Downloads
as the location, but you can change this to Desktop or Documents if you prefer.

Run each of these commands in your terminal:

```bash
cd Downloads
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/data/raw"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/data/processed"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/data/sql"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/notebooks/01_data_audit"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/notebooks/02_clv_segmentation"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/notebooks/03_demand_forecasting"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/notebooks/04_churn_survival"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/src/utils"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/src/queries"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/reports/figures"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/reports/excel_outputs"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/docs"
mkdir -p "Data Stuff/Gamezone/gamezone-analytics/.github/ISSUE_TEMPLATE"
```

**What mkdir -p does:**
mkdir stands for "make directory" — it creates a folder. The -p flag
means "create all parent folders too if they don't exist yet", so you
don't have to create each level one at a time.

Verify the structure was created correctly:

```bash
find "Data Stuff/Gamezone/gamezone-analytics" -type d | sort
```

You should see all the folders listed.

**Why this structure matters:**
A well-organised folder structure signals professionalism immediately.
Each folder has a single clear responsibility — raw data never mixes
with processed data, reusable code never mixes with notebooks. When a
hiring manager clones your repo, the structure alone tells them you
think in systems, not just scripts.

---

## Step 5 — Navigate into the project folder

From this point forward, all commands assume you are inside the
gamezone-analytics folder. Run this once at the start of every
terminal session:

```bash
cd '/Users/seleteakpotosu-nartey/Downloads/Data Stuff/Gamezone/gamezone-analytics'
```

**What cd does:**
cd stands for "change directory" — it moves your terminal's current
location into a different folder. The terminal always needs to know
where it is before it can do anything with files.

To confirm you are in the right place:

```bash
pwd
```

pwd stands for "print working directory". It prints your current
location. You should see the full path ending in gamezone-analytics.

---

## Step 6 — Create the project files

Now we create every file the project needs, one by one. Each file is
explained before its contents so you understand what it does.

---

### File 1 — .gitignore

**What this file does:**
Tells Git which files and folders to never track or upload to GitHub.
This protects you from two critical mistakes: accidentally uploading
your raw data, and accidentally uploading passwords or database
credentials. Any file listed here is completely invisible to Git.

Create it by running:

```bash
cat > .gitignore << 'EOF'
# =============================================================
# GameZone Analytics — .gitignore
# =============================================================

# ----- Python -----
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
.eggs/
dist/
build/

# ----- Environments -----
.env
.venv/
env/
venv/
*.conda

# ----- Jupyter -----
.ipynb_checkpoints/
*.ipynb~

# ----- Data (never commit raw data to Git) -----
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# ----- Secrets & credentials -----
.env
.env.*
config/secrets.yml

# ----- macOS -----
.DS_Store
.AppleDouble
Icon?
._*

# ----- VS Code -----
.vscode/settings.json
.vscode/launch.json
!.vscode/extensions.json

# ----- Reports (generated from code, not stored in Git) -----
reports/figures/*
reports/excel_outputs/*
!reports/figures/.gitkeep
!reports/excel_outputs/.gitkeep

# ----- Logs -----
*.log
logs/
EOF
```

---

### File 2 — .env.example

**What this file does:**
A template showing what database credentials are needed, with placeholder
values instead of real ones. This file IS uploaded to GitHub so collaborators
know what variables to set — but it never contains real passwords. The actual
.env file (which contains your real password) is git-ignored and never uploaded.

```bash
cat > .env.example << 'EOF'
# =============================================================
# GameZone Analytics — Environment Variables
# =============================================================
# IMPORTANT: Copy this file to .env and fill in your values.
# The .env file is git-ignored — never commit real credentials.
#
# Usage in Python:
#   from dotenv import load_dotenv; load_dotenv()
#   import os; pw = os.getenv("DB_PASSWORD")
# =============================================================

# MySQL Workbench connection
DB_USER=root
DB_PASSWORD=your_password_here
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=gamezone_analytics
EOF
```

---

### File 3 — environment.yml

**What this file does:**
The recipe for your Conda environment. It lists every Python package
this project needs, with exact version numbers, so the environment is
perfectly reproducible. Anyone — including a future employer — can run
one command and get an identical setup to yours.

```bash
cat > environment.yml << 'EOF'
name: gamezone-analytics
channels:
  - conda-forge
  - defaults

dependencies:
  - python=3.11
  - pandas=2.2
  - numpy=1.26
  - openpyxl=3.1
  - xlrd=2.0
  - sqlalchemy=2.0
  - pymysql=1.1
  - scipy=1.13
  - statsmodels=0.14
  - scikit-learn=1.5
  - lightgbm=4.3
  - ruptures=1.1
  - matplotlib=3.9
  - seaborn=0.13
  - plotly=5.22
  - jupyter=1.0
  - jupyterlab=4.2
  - nbformat=5.10
  - black=24.4
  - flake8=7.1
  - isort=5.13
  - pip
  - pip:
    - lifelines==0.29.0
    - scikit-survival==0.23.0
    - lifetimes==0.11.3
    - prophet==1.1.5
    - shap==0.45.1
    - great-expectations==0.18
    - fuzzywuzzy==0.18.0
    - python-levenshtein==0.25
    - nbconvert==7.16
    - python-dotenv==1.0

variables:
  PYTHONPATH: src
EOF
```

---

### File 4 — README.md

**What this file does:**
The front page of your GitHub repository. This is the first thing a
hiring manager sees when they visit your project. It introduces the
project, lists the techniques used, and explains how to run it.

```bash
cat > README.md << 'EOF'
# GameZone Analytics

**End-to-end data science portfolio project** — anomaly detection,
customer lifetime value modelling, demand forecasting, and churn survival
analysis on a real-world e-commerce dataset (21,864 orders · 150 countries
· 2019–2021).

---

## Projects

| # | Project | Type | Key techniques |
|---|---------|------|----------------|
| 01 | [Data Quality & Anomaly Audit](notebooks/01_data_audit/) | Exploratory analysis | Great Expectations · entity resolution · temporal forensics |
| 02 | [Customer Lifetime Value Segmentation](notebooks/02_clv_segmentation/) | Clustering & analytics | BG/NBD · K-Means · channel ROI attribution |
| 03 | [Demand Forecasting](notebooks/03_demand_forecasting/) | Predictive modelling | Prophet · LightGBM · SHAP · hierarchical reconciliation |
| 04 | [Churn & Survival Analysis](notebooks/04_churn_survival/) | Survival analysis | Kaplan-Meier · Cox PH · churn risk scoring |

---

## Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/selete-tetteh/gamezone-analytics.git
cd gamezone-analytics
```

### 2. Create the Conda environment
```bash
conda env create -f environment.yml
conda activate gamezone-analytics
```

### 3. Add the raw data
Place gamezone-orders-data.xlsx in data/raw/

### 4. Launch JupyterLab
```bash
jupyter lab
```

---

## Tools & stack

| Layer | Tools |
|-------|-------|
| Language | Python 3.11 · SQL (MySQL) |
| Data wrangling | pandas · NumPy · SQLAlchemy |
| Machine learning | scikit-learn · LightGBM · SHAP |
| Forecasting | Prophet · ruptures (PELT) |
| Survival analysis | lifelines · scikit-survival |
| CLV modelling | lifetimes (BG/NBD · Gamma-Gamma) |
| Data quality | Great Expectations |
| Visualisation | Matplotlib · Seaborn · Plotly · Tableau · Looker |
| Excel reporting | openpyxl · pivot tables |
| Environment | Conda · VS Code · JupyterLab |
| Version control | Git · GitHub |

---

## Key findings

> Populated as each project is completed.

- **Project 01:** TBC
- **Project 02:** TBC
- **Project 03:** TBC
- **Project 04:** TBC

---

## Author

**Selete Tetteh**
[LinkedIn](https://linkedin.com/in/yourprofile) · [GitHub](https://github.com/selete-tetteh)
EOF
```

---

### File 5 — CONTRIBUTING.md

**What this file does:**
Documents the Git branching strategy and commit message conventions for
the project. This shows hiring managers that you follow professional
team workflows, not just push everything to one branch.

```bash
cat > CONTRIBUTING.md << 'EOF'
# Contributing & Git Workflow

## Branch strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable, presentation-ready code only |
| `dev` | Active development — merge here first |
| `feature/project-01-audit` | Work branch for Project 01 |
| `feature/project-02-clv` | Work branch for Project 02 |
| `feature/project-03-forecast` | Work branch for Project 03 |
| `feature/project-04-churn` | Work branch for Project 04 |

**Workflow:**
feature branch → dev (pull request) → main (pull request when all done)

## Commit message format

```
<type>: <short description>
```

Types: feat · fix · data · docs · style · refactor

## Before committing notebooks

Always strip output before committing:
```bash
jupyter nbconvert --clear-output --inplace notebooks/**/*.ipynb
```
EOF
```

---

### File 6 — data/sql/01_schema.sql

**What this file does:**
The MySQL database schema — it creates the empty tables and a cleaned
view in your local MySQL database. Think of it like building shelves
before stocking them. The actual data gets loaded separately in Project 01.

```bash
cat > data/sql/01_schema.sql << 'EOF'
-- =============================================================
-- GameZone Analytics — MySQL Schema
-- Run this in MySQL Workbench to set up the database
-- =============================================================

CREATE DATABASE IF NOT EXISTS gamezone_analytics
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE gamezone_analytics;

-- Raw orders table
CREATE TABLE IF NOT EXISTS orders_raw (
    user_id                 VARCHAR(50),
    order_id                VARCHAR(50) PRIMARY KEY,
    purchase_ts             DATETIME,
    ship_ts                 DATETIME,
    product_name            VARCHAR(100),
    product_id              VARCHAR(20),
    usd_price               DECIMAL(10, 2),
    purchase_platform       VARCHAR(20),
    marketing_channel       VARCHAR(30),
    account_creation_method VARCHAR(20),
    country_code            CHAR(2),
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Region lookup table
CREATE TABLE IF NOT EXISTS region_lookup (
    country_code  CHAR(2) PRIMARY KEY,
    region        VARCHAR(20)
);

-- Cleaned orders view
-- Applies business rules: excludes $0 prices, standardises product
-- names, calculates fulfilment days, joins region
CREATE OR REPLACE VIEW orders_clean AS
SELECT
    user_id,
    order_id,
    purchase_ts,
    ship_ts,
    CASE
        WHEN product_name = '27inches 4k gaming monitor'
        THEN '27in 4K gaming monitor'
        ELSE product_name
    END                                          AS product_name,
    product_id,
    usd_price,
    purchase_platform,
    COALESCE(marketing_channel, 'unknown')       AS marketing_channel,
    COALESCE(account_creation_method, 'unknown') AS account_creation_method,
    o.country_code,
    COALESCE(r.region, 'Other')                  AS region,
    DATEDIFF(ship_ts, purchase_ts)               AS fulfilment_days,
    YEAR(purchase_ts)                            AS purchase_year,
    MONTH(purchase_ts)                           AS purchase_month
FROM orders_raw o
LEFT JOIN region_lookup r USING (country_code)
WHERE usd_price > 0
  AND purchase_ts IS NOT NULL;
EOF
```

---

### File 7 — src/__init__.py and src/utils/__init__.py

**What these files do:**
Empty files that tell Python "this folder is a package, not just a folder".
Without them, `from utils.helpers import load_orders` would fail with a
ModuleNotFoundError in your notebooks.

```bash
echo "# Makes src importable as a Python package" > src/__init__.py
echo "# Makes src/utils importable as a Python package" > src/utils/__init__.py
```

---

### File 8 — src/utils/helpers.py

**What this file does:**
A shared Python module containing functions used across all four project
notebooks — loading data, connecting to MySQL, and saving charts. Instead
of copying the same code into every notebook, we write it once here and
import it. This is called DRY (Don't Repeat Yourself) — a core
professional coding principle.

```bash
cat > src/utils/helpers.py << 'EOF'
"""
src/utils/helpers.py
--------------------
Shared utility functions used across all GameZone Analytics notebooks.
Import with: from utils.helpers import load_orders, get_db_engine
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = ROOT / "data" / "raw" / "gamezone-orders-data.xlsx"
PROCESSED_PATH = ROOT / "data" / "processed"
FIGURES_PATH = ROOT / "reports" / "figures"
EXCEL_OUTPUT_PATH = ROOT / "reports" / "excel_outputs"


# ── Data loading ───────────────────────────────────────────────────────
def load_orders(cleaned: bool = True) -> pd.DataFrame:
    """
    Load GameZone orders from the raw Excel file.

    Parameters
    ----------
    cleaned : bool
        If True (default), apply standard cleaning rules.

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_excel(RAW_DATA_PATH, sheet_name="orders")
    region = pd.read_excel(RAW_DATA_PATH, sheet_name="region")
    df = df.merge(region, on="COUNTRY_CODE", how="left")
    if cleaned:
        df = _clean_orders(df)
    return df


def _clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Apply standard cleaning rules to raw orders DataFrame."""
    df = df.copy()

    # Parse timestamps — Excel stores dates as strings, pandas needs
    # them as datetime objects to do date arithmetic
    df["PURCHASE_TS"] = pd.to_datetime(df["PURCHASE_TS"], errors="coerce")
    df["SHIP_TS"] = pd.to_datetime(df["SHIP_TS"], errors="coerce")

    # Calculate how many days between purchase and shipment
    # Negative values = shipped before purchase (an anomaly we investigate)
    df["FULFILMENT_DAYS"] = (df["SHIP_TS"] - df["PURCHASE_TS"]).dt.days

    # Standardise the duplicate product name
    df["PRODUCT_NAME"] = df["PRODUCT_NAME"].replace(
        {"27inches 4k gaming monitor": "27in 4K gaming monitor"}
    )

    # Fill missing values in categorical columns
    for col in ["MARKETING_CHANNEL", "ACCOUNT_CREATION_METHOD"]:
        df[col] = df[col].fillna("unknown")

    # Remove $0 orders — these are cancelled or test orders
    df = df[df["USD_PRICE"] > 0].copy()

    # Add convenience columns for time-based analysis
    df["PURCHASE_YEAR"] = df["PURCHASE_TS"].dt.year
    df["PURCHASE_MONTH"] = df["PURCHASE_TS"].dt.month
    df["PURCHASE_YEARMONTH"] = df["PURCHASE_TS"].dt.to_period("M")

    return df.reset_index(drop=True)


# ── Database ───────────────────────────────────────────────────────────
def get_db_engine():
    """
    Create a SQLAlchemy engine using credentials from .env file.
    """
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "gamezone_analytics")
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"
    return create_engine(url)


def run_query(sql: str, engine=None) -> pd.DataFrame:
    """Execute a SQL query and return results as a DataFrame."""
    if engine is None:
        engine = get_db_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)


# ── Plotting ───────────────────────────────────────────────────────────
def set_style():
    """Apply a clean, consistent style to all plots."""
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
    plt.rcParams.update({
        "figure.figsize": (12, 5),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 14,
        "axes.titleweight": "medium",
        "figure.dpi": 120,
    })


def save_figure(fig: plt.Figure, filename: str):
    """Save a matplotlib figure to reports/figures/."""
    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIGURES_PATH / filename, bbox_inches="tight")
    print(f"Saved → reports/figures/{filename}")
EOF
```

---

### File 9 — docs/methodology.md

**What this file does:**
Documents the analytical decisions made across all four projects —
which models were chosen and why, how data quality issues were handled,
and what assumptions were made. This is what separates a portfolio that
looks like coursework from one that looks like real analytical work.

```bash
cat > docs/methodology.md << 'EOF'
# Project Methodology

## Data source

**GameZone Orders Dataset**
- 21,864 order records · 11 columns · 2019–2021
- 150 countries · 9 products · 2 purchase platforms

## Data quality baseline

| Issue | Count | % of dataset | Resolution |
|-------|-------|-------------|------------|
| Ship date before purchase date | 1,997 | 9.1% | Investigated — flagged as anomaly cohort |
| $0 price orders | 29 | 0.1% | Excluded (cancelled/test orders) |
| Null USD price | 5 | 0.02% | Excluded |
| Null marketing channel | 83 | 0.4% | Imputed via probabilistic model |
| Duplicate product names | 2 | — | Standardised to canonical name |

## Methodologies by project

### Project 01 — Data Audit
- Great Expectations for schema validation
- Levenshtein distance for entity resolution
- IQR for price outlier detection

### Project 02 — CLV Segmentation
- BG/NBD model for purchase frequency
- Gamma-Gamma model for expected spend
- K-Means clustering (k via elbow + silhouette)
- Bootstrap confidence intervals for regional CLV

### Project 03 — Demand Forecasting
- Prophet as baseline
- LightGBM with lag and rolling features
- PELT change-point detection
- SHAP values for feature importance
- MAPE as evaluation metric

### Project 04 — Churn & Survival Analysis
- Kaplan-Meier estimator for survival curves
- Log-rank test for significance between groups
- Cox Proportional Hazards for multivariate analysis
- XGBoost for churn probability scoring
EOF
```

---

### File 10 — .github/ISSUE_TEMPLATE/bug_report.md

**What this file does:**
A template that appears when someone opens a bug report on your GitHub
repo. Having this shows you understand collaborative development
workflows — a small but noticeable professional touch.

```bash
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug report
about: Something broken in a notebook or script
title: "[BUG] "
labels: bug
---

**Notebook / script affected**

**What happened**

**Steps to reproduce**
1.
2.

**Expected behaviour**

**Environment**
- OS:
- Python version:
- Conda env: gamezone-analytics [yes/no]

**Error message**
```
paste traceback here
```
EOF
```

---

### File 11 — .vscode/extensions.json

**What this file does:**
Tells VS Code which extensions are recommended for this project. When
someone opens the repo in VS Code, it will automatically suggest these.
It is git-tracked so collaborators get the same setup.

```bash
mkdir -p .vscode
cat > .vscode/extensions.json << 'EOF'
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-toolsai.jupyter",
    "ms-toolsai.jupyter-renderers",
    "mtxr.sqltools",
    "mtxr.sqltools-driver-mysql",
    "mechatroner.rainbow-csv",
    "eamodio.gitlens",
    "mhutchie.git-graph",
    "yzhang.markdown-all-in-one"
  ]
}
EOF
```

---

### File 12 — .gitkeep files

**What these do:**
Git does not track empty folders — if a folder has no files in it, Git
ignores it entirely and it disappears from GitHub. We add a hidden
.gitkeep file to the folders that are currently empty so they are
preserved in the repository structure.

```bash
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch reports/figures/.gitkeep
touch reports/excel_outputs/.gitkeep
```

---

## Step 7 — Create the Conda environment

Now that all the project files exist, we can create the Python
environment from the environment.yml recipe:

```bash
conda env create -f environment.yml
```

**What this does:**
Reads environment.yml and installs every listed package into a new
isolated environment called gamezone-analytics. This takes several
minutes the first time — it is downloading around 50+ packages.

Once complete, activate the environment:

```bash
conda activate gamezone-analytics
```

You know it worked because your terminal prompt changes from (base) to
(gamezone-analytics). You need to activate it at the start of every
session.

Verify every key package installed correctly:

```bash
python -c "import pandas, lifelines, prophet, lightgbm, shap; print('All good!')"
```

You should see: `All good!`

---

## Step 8 — Place the raw data file

Copy your data file into the raw data folder:

```bash
cp ~/Downloads/gamezone-orders-data.xlsx data/raw/gamezone-orders-data.xlsx
```

**If the file is somewhere else on your Mac**, replace ~/Downloads/ with
the actual location. For example if it is on your Desktop:

```bash
cp ~/Desktop/gamezone-orders-data.xlsx data/raw/gamezone-orders-data.xlsx
```

Confirm it is there:

```bash
ls data/raw/
```

You should see: `gamezone-orders-data.xlsx`

This file is listed in .gitignore so it will never be uploaded to
GitHub, no matter what. Raw data never goes into version control.

---

## Step 9 — Create a GitHub account

**What GitHub is and why it is different from Git:**
Git tracks your changes locally on your Mac. GitHub is the website
where you upload your project so it lives in the cloud and is publicly
visible. Git is the engine, GitHub is the garage where you park the
car so others can see it. Your GitHub profile is your live portfolio.

1. Go to **github.com** in your browser
2. Click **Sign up** and follow the prompts
3. Choose a professional username — this appears on your CV and in
   search results. Use your name or a clean variation. Avoid numbers,
   underscores, or anything unprofessional.
4. Verify your email address when prompted

---

## Step 10 — Create the GitHub repository

A repository (repo) is a project folder on GitHub. It holds all your
code, notebooks, SQL, and documentation — everything except the raw data.

1. Log in to **github.com**
2. Click the **+** icon (top right) → **New repository**
3. Fill in:
   - **Repository name:** `gamezone-analytics`
   - **Description:** `End-to-end e-commerce data science project — CLV modelling, demand forecasting, and churn survival analysis`
   - **Visibility:** Public — this is what hiring managers see
   - ❌ Do NOT tick "Add a README file" — you already have one
4. Click **Create repository**

---

## Step 11 — Generate a Personal Access Token

GitHub does not allow pushing code with your account password. Since
2021 it requires a Personal Access Token (PAT) — a long auto-generated
password specifically for Git terminal operations.

1. On github.com → click your **profile picture** → **Settings**
2. Scroll to the bottom of the left sidebar → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. Fill in:
   - **Note:** `gamezone-analytics`
   - **Expiration:** 90 days
   - **Scopes:** tick **repo** only
6. Click **Generate token**
7. **Copy the token immediately** — GitHub never shows it again

It looks like: `ghp_xxxxxxxxxxxxxxxxxxxx`

> Save it in your Notes app or a password manager. If you lose it you
> will need to generate a new one — your existing commits are unaffected.

---

## Step 12 — Initialise Git and push to GitHub

Make sure you are in the project folder, then run these commands in order:

```bash
# Confirm you are in the right place
pwd
# Should end with: gamezone-analytics

# Initialise Git in this folder — this creates the hidden .git folder
# that starts tracking everything
git init

# Stage all the files you just created — tells Git to include them
# in the next commit
git add .

# Create the first commit — a saved snapshot of your entire project
# at this moment
git commit -m "feat: initial project structure, environment, and shared utilities"

# Connect your local folder to the GitHub repo you just created
# Replace YOUR_TOKEN with the token from Step 11
git remote add origin https://YOUR_TOKEN@github.com/selete-tetteh/gamezone-analytics.git

# Rename your branch to main (GitHub's default branch name)
git branch -M main

# Push everything to GitHub
# -u sets origin main as the default so future pushes only need: git push
git push -u origin main
```

If successful you will see:

```
Branch 'main' set up to track remote branch 'main' from 'origin'.
To https://github.com/selete-tetteh/gamezone-analytics.git
   abc1234..def5678  main -> main
```

Visit `https://github.com/selete-tetteh/gamezone-analytics` in your
browser — your files should all be there.

---

## Step 13 — Create your working branches

We never work directly on main. The branching strategy protects your
public portfolio from ever showing broken or half-finished work.

```
main          ← clean, presentable — what hiring managers see
  └── dev     ← staging area, finished projects collect here
        └── feature/project-01-audit  ← where you do the work
```

Run these commands:

```bash
# Create the dev branch and push it to GitHub
git checkout -b dev
git push -u origin dev

# Create the first feature branch for Project 01
git checkout -b feature/project-01-audit
git push -u origin feature/project-01-audit
```

**What git checkout -b does:**
The -b flag creates a new branch AND switches you onto it in one step.
You are now on feature/project-01-audit. All your Project 01 work
happens here. This branch will not be merged into dev until the entire
project is finished, reviewed, and working correctly.

---

## Step 14 — Configure your .env file for MySQL

The .env file stores your MySQL credentials. It is git-ignored so your
password is never uploaded to GitHub.

```bash
# Create your .env file by copying the template
cp .env.example .env

# Open it in VS Code to fill in your real credentials
code .env
```

Replace the placeholder values with your actual MySQL Workbench details:

```
DB_USER=root
DB_PASSWORD=your_actual_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=gamezone_analytics
```

Save the file. You will never commit this file to GitHub — the
.gitignore takes care of that automatically.

**Why we do not hardcode passwords in Python scripts:**
If you wrote your password directly into a .py file and pushed it to
GitHub, it would be publicly visible to the entire internet — including
automated bots that scan GitHub for exposed credentials. The .env file
keeps secrets completely separate from code. This is non-negotiable
in every professional team.

---

## Step 15 — Set up MySQL Workbench database

Open MySQL Workbench and run the schema file to create the database
and empty tables:

1. Open **MySQL Workbench** and connect to your local server
2. Click **File** → **Open SQL Script**
3. Navigate to `data/sql/01_schema.sql` and open it
4. Click the lightning bolt icon (or press Cmd+Shift+Enter) to run it
5. You should see `gamezone_analytics` appear in the Schemas panel

**What this does:**
Creates the empty database structure — the tables and the orders_clean
view. No data is loaded yet. The data gets loaded via Python in Project 01,
which is the professional way to do it (reproducible and automated).

---

## Step 16 — Launch JupyterLab

```bash
# Make sure your environment is active
conda activate gamezone-analytics

# Make sure you are in the project folder
cd '/Users/seleteakpotosu-nartey/Downloads/Data Stuff/Gamezone/gamezone-analytics'

# Launch JupyterLab
jupyter lab
```

JupyterLab opens automatically in your browser. You should see your
full project folder structure in the left sidebar.

**What JupyterLab is:**
An interactive coding environment that runs in your browser. You write
Python code in cells, run them one at a time, and see outputs — charts,
tables, numbers — directly below each cell. Each .ipynb file is a
notebook: a mix of live code, outputs, and written explanations in one
document. It is the standard tool for data science work.

---



## Your daily workflow ## 

Every time you sit down to work on this project, follow this sequence.

### Starting a session

```bash
# 1. Activate your environment
conda activate gamezone-analytics

# 2. Navigate to your project
cd '/Users/seleteakpotosu-nartey/Downloads/Data Stuff/Gamezone/gamezone-analytics'

# 3. Pull any latest changes
git pull origin dev

# 4. Make sure you are on your working branch
git checkout feature/project-01-audit

# 5. Launch JupyterLab
jupyter lab
```

### Ending a session

```bash

CTrl + C
# 1. Strip notebook outputs before committing
#    Outputs bloat the Git diff and make changes hard to review
jupyter nbconvert --clear-output --inplace notebooks/01_data_audit/*.ipynb

# 2. Stage all changes
git add .

# 3. Commit with a meaningful message
git commit -m "feat: describe what you worked on today"

# 4. Push to GitHub
git push

conda deactivate
```

---

## Commit message conventions

Every commit follows this format:

```
<type>: <short description of what you did>
```

| Type | When to use it |
|------|---------------|
| `feat:` | New analysis, notebook section, or feature |
| `fix:` | Correcting a bug or mistake |
| `data:` | Changes to data loading or SQL |
| `docs:` | Updates to README, notes, or comments |
| `style:` | Formatting only, no logic changed |
| `refactor:` | Restructuring code without changing behaviour |

**Good examples:**
```bash
git commit -m "feat: add temporal anomaly detection to project 01"
git commit -m "fix: correct fulfilment_days for negative values"
git commit -m "data: load orders into MySQL and create orders_clean view"
git commit -m "docs: update README with project 01 key findings"
```

**Bad examples — avoid these:**
```bash
git commit -m "update"
git commit -m "fixed stuff"
git commit -m "done"
```

Your commit history is part of your portfolio. A hiring manager reading
through it should be able to understand exactly how you built this
project, in what order, and how methodically you worked.

---

## When a project is complete — merging via Pull Request

When a project is fully finished, merge it up to dev via a Pull Request
on GitHub rather than directly in the terminal. This mirrors real team
workflow.

1. Go to **github.com** → your repository
2. Click **Pull requests** → **New pull request**
3. Set **base** to `dev` and **compare** to `feature/project-01-audit`
4. Write a summary: what the project does, what you found, what
   techniques you used
5. Click **Create pull request**, review it yourself, then
   **Merge pull request**

After merging, create the next feature branch:

```bash
git checkout dev
git pull origin dev
git checkout -b feature/project-02-clv
git push -u origin feature/project-02-clv
```

Only merge `dev` into `main` when all four projects are complete and
polished. `main` is your CV — it should always be in a state you are
proud to show.

---

## Quick reference — commands used every day

| Command | What it does |
|---------|-------------|
| `conda activate gamezone-analytics` | Step into your project environment |
| `conda deactivate` | Step out of the environment |
| `jupyter lab` | Launch JupyterLab |
| `git status` | See which files have changed |
| `git add .` | Stage all changes ready to commit |
| `git commit -m "message"` | Save a snapshot with a description |
| `git push` | Upload commits to GitHub |
| `git pull` | Download latest changes from GitHub |
| `git checkout branch-name` | Switch to a different branch |
| `git log --oneline` | See commit history in compact view |
| `ls` | List files in the current folder |
| `pwd` | Print your current folder location |
| `cd folder-name` | Navigate into a folder |
| `cd ..` | Go up one folder level |

---

## Up next — Project 01: Data Quality & Anomaly Audit

Once all 16 steps above are complete, we begin building the first notebook.

**What Project 01 is:**
Before any analysis or modelling, a real data team always audits the
data first. We found some genuinely interesting problems in this dataset:

- 1,997 orders where the ship date is before the purchase date (9.1%)
- Prices ranging from $0 to $3,147 on the same product
- Two product names that are duplicates with inconsistent spelling
- 83 orders with missing marketing channel data

Project 01 investigates all of these, builds a formal data validation
pipeline, and produces a cleaned dataset that all three subsequent
projects will build on. It uses Python, SQL, and Excel.

**Files we will create:**

```
notebooks/01_data_audit/
    01_temporal_anomalies.ipynb
    02_price_forensics.ipynb
    03_entity_resolution.ipynb
    04_great_expectations_validation.ipynb

data/sql/
    02_load_data.sql
    03_anomaly_queries.sql

reports/excel_outputs/
    data_quality_report.xlsx
```

When you are ready, say the word and we will begin.
