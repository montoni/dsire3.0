# 50 States of Energy Affordability: September 2026 Actions

An interactive dashboard of the 269 state energy affordability actions in DSIRE Insight's *50 States of Energy Affordability* September 2026 report: a filterable tile map of actions by state, small-multiple maps by category, category and sub-topic breakdowns, and a searchable, sortable action database.

## View locally

Browsers block `fetch` from `file://`, so serve the folder:

```bash
python -m http.server 8000
# then open http://localhost:8000
```

## Publish with GitHub Pages

1. Create a repository and push these files to the `main` branch.
2. In the repository, go to **Settings → Pages**, set **Source** to "Deploy from a branch", and pick `main` / `(root)`.
3. The site appears at `https://<your-username>.github.io/<repo-name>/` after a minute or two.

## Updating the data

When a new monthly workbook comes out:

```bash
pip install pandas openpyxl
python scripts/build_data.py path/to/new-workbook.xlsx data/actions.json
```

Then update the report month in `index.html` (page title, heading, and footer) and commit.

## Data notes

- Two Indiana actions tagged "Utility Oversight" are counted under "Utility Oversight and Cost Recovery."
- **Action type** is derived from each action's sources: anything with a bill status code is Legislation; executive orders, press releases, ballot measures and similar items are "Executive & other"; dockets, orders, decisions and proceedings are "Regulatory proceeding."
- **Bill status** comes from the codes on bill citations: E = enacted, P1 = passed one chamber, P2 = passed both chambers, D = failed, V = vetoed.
- Source data © DSIRE Insight. Check your subscription terms before making this repository public.
