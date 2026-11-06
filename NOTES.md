# Notes

## Oct 20, 2026 - Days 1-4: data, loading, variance logic, dashboard
- Built the synthetic data generator (src/generate_data.py) for a hypothetical photography business: 7 line items x 6 months (Apr-Sep 2026), 42 budget rows and 41 actual rows. Planted situations on purpose: an equipment spike (May), a revenue dip (August), a $0-budget line (Marketing), and a missing actual (September insurance).
- Built src/load.py (validates columns, row count, type values, duplicate month/line_item rows, numeric amounts) and src/variance.py (variance in $ and %, favorable/unfavorable status, materiality flag). Built the Streamlit dashboard (app.py) and a check.py script to print the flagged rows while developing.
- Design decisions:
  - Revenue and expense logic are opposite: revenue above budget is favorable, expense above budget is unfavorable.
  - A $0 budget would divide by zero, so variance % is left blank (NaN) and those rows are judged on dollars. A real spend against a $0 budget counts as big on the % test.
  - A missing actual stays visible as "missing" instead of being treated as $0, so it can't hide a variance.
  - Materiality has two modes: must exceed BOTH the % and $ thresholds, or EITHER one.
- Problem: pytest failed on my first run because of a wrong file path. Fixed the path and re-ran until all tests passed.
- Learned: for revenue, actual above budget is favorable, but for expenses it is unfavorable, so the label depends on the line type and not just the sign of the variance.

## Oct 27, 2026 - Days 5-7: commentary, Excel export, deploy, memo
- Added src/commentary.py (rule-based plain-English bullets from the numbers, no LLM) and src/export.py (one-page Excel report with openpyxl), with tests. 23 tests total across load (5), variance (12), commentary (4), and export (2). All pass.
- Wrote the README, added a screenshot, deployed on Streamlit Community Cloud, and wrote a sample manager memo (docs/memo.md) from the tool's output.
- Problem: I accidentally committed cache files and had to remove them and add a .gitignore. The README screenshot also showed as broken at first because the image path was wrong; fixed in a follow-up commit.
- Learned: add .gitignore before the first commit, and check the README on GitHub after pushing, not just locally.

## Verification
- Hand-checked two results against the tool: the August standard shoot variance (1,875 vs. 2,500 = -625, or -25.0%) and the net variance across all lines (-$1,075 unfavorable, with the missing September insurance actual excluded). Both matched.
- At the default thresholds (10% AND $500) the tool flags exactly 2 rows, and both are planted: Equipment rental in May (+$750, +214.3%) and standard shoot fees in August (-$625, -25.0%).
- Small items such as the steady Travel creep (+5%, +10%, +15% over budget in Jul-Sep) are not flagged at the default settings. The memo calls this out, and lowering the dollar threshold in the dashboard surfaces them.

## Interview line
"I built a variance tool that handles revenue and expense logic correctly, keeps missing data visible instead of hiding it, flags only material variances, and writes plain-English commentary. I planted known problems in the synthetic data so I could check the tool caught exactly those, and hand-verified the totals."

