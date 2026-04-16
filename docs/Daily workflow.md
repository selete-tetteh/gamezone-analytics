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



conda activate gamezone-analytics
cd '/Users/seleteakpotosu-nartey/Downloads/Data Stuff/Gamezone/gamezone-analytics'
git checkout feature/project-01-audit
jupyter lab 

```

### Ending a session

```bash
# 1. Strip notebook outputs before committing
#    Outputs bloat the Git diff and make changes hard to review
jupyter nbconvert --clear-output --inplace notebooks/01_data_audit/*.ipynb

# 2. Stage all changes
git add .

# 3. Commit with a meaningful message
git commit -m "feat: describe what you worked on today"

# 4. Push to GitHub
git push
```
conda deactivate
---

VS Code

## Starting a Session
conda activate gamezone-analytics
cd '/Users/seleteakpotosu-nartey/Downloads/Data Stuff/Gamezone/gamezone-analytics'
git checkout feature/project-02-clv
git pull origin feature/project-02-clv 
code .




git checkout dev
git pull origin dev
git checkout -b feature/project-02-clv
git push -u origin feature/project-02-clv



Then in Section 0 of every notebook, add one line after set_style():

from utils.helpers import load_orders, set_style, save_figure, start_logging
set_style()
start_logging(project_root, '03_channel_roi_attribution')



##Ending a Session
git add .
git commit -m "feat: completed bgNBD_clv model"
git push
conda deactivate



## New notebook
cd '/Users/seleteakpotosu-nartey/Downloads/Data Stuff/Gamezone/gamezone-analytics'
touch notebooks/01_data_audit/04_great_expectations.ipynb



git add .
git commit -m "feat: complete notebook 3 channel ROI attribution, run bubble chart  "
git push
