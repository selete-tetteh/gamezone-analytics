# Contributing & Git Workflow

This document describes the branching strategy and commit conventions used in this project.

---

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
```
feature branch → dev (pull request) → main (pull request when project complete)
```

---

## Commit message format

Use the conventional commits standard:

```
<type>: <short description>

[optional body]
```

**Types:**
- `feat:` — new analysis, notebook, or feature
- `fix:` — bug fix
- `data:` — changes to data loading or SQL
- `docs:` — README, methodology notes
- `style:` — formatting, no logic change
- `refactor:` — restructuring code without changing behaviour
- `test:` — adding validation checks

**Examples:**
```
feat: add temporal anomaly detection to project 01
fix: correct fulfilment_days sign for timezone-shifted records
data: add region JOIN to orders_clean SQL view
docs: update README with project 01 key findings
```

---

## Before committing notebooks

Always strip notebook output before committing (keeps diffs clean):

```bash
jupyter nbconvert --clear-output --inplace notebooks/**/*.ipynb
```

Or use the VS Code Jupyter extension: `Kernel → Restart Kernel and Clear All Outputs`.
