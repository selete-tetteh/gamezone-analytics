# GitHub & Local Setup Guide
## Step-by-step for GameZone Analytics

---

## Part 1 — Install Git (if not installed)

Check if Git is installed:
```bash
git --version
```

If not found, install via Homebrew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git
```

Configure your identity (this appears on all your commits):
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## Part 2 — Install Conda (Miniconda)

1. Download Miniconda for Mac (Apple Silicon or Intel):
   https://docs.conda.io/en/latest/miniconda.html

2. Run the installer and follow prompts.

3. Restart your terminal, then verify:
```bash
conda --version
```

---

## Part 3 — Create the Conda environment

Navigate to your project folder, then:
```bash
conda env create -f environment.yml
conda activate gamezone-analytics
```

Verify everything installed:
```bash
python -c "import pandas, lifelines, prophet, lightgbm, shap; print('All good!')"
```

---

## Part 4 — Create your GitHub repository

1. Go to https://github.com and sign in (create a free account if needed).

2. Click the **+** icon → **New repository**

3. Fill in:
   - **Repository name:** `gamezone-analytics`
   - **Description:** `End-to-end e-commerce data science project — CLV modelling, demand forecasting, and churn survival analysis`
   - **Visibility:** Public (so employers can see it)
   - **Do NOT** initialise with README (you already have one)

4. Click **Create repository**

---

## Part 5 — Connect your local project to GitHub

In your terminal, navigate to the project folder, then run:

```bash
# Initialise Git
git init

# Add all files
git add .

# First commit
git commit -m "feat: initial project structure, environment, and shared utilities"

# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/gamezone-analytics.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Part 6 — Set up your working branches

```bash
# Create a dev branch
git checkout -b dev
git push -u origin dev

# Create feature branches for each project
git checkout -b feature/project-01-audit
git push -u origin feature/project-01-audit
```

When you finish a project, merge it into dev via a Pull Request on GitHub.

---

## Part 7 — Configure your .env file

```bash
# Copy the template
cp .env.example .env

# Open in VS Code and fill in your MySQL credentials
code .env
```

---

## Part 8 — Add your raw data

Place `gamezone-orders-data.xlsx` in:
```
data/raw/gamezone-orders-data.xlsx
```

This file is git-ignored so it will NOT be uploaded to GitHub.

---

## Part 9 — Launch JupyterLab

```bash
conda activate gamezone-analytics
jupyter lab
```

Open the notebooks in order starting with `notebooks/01_data_audit/`.

---

## Daily workflow

```bash
# Start of each session
conda activate gamezone-analytics
git checkout feature/project-01-audit   # your current branch
git pull origin dev                      # get latest changes

# End of each session
jupyter nbconvert --clear-output --inplace notebooks/01_data_audit/*.ipynb
git add .
git commit -m "feat: describe what you did today"
git push
```
