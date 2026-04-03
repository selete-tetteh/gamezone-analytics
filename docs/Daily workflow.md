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

---