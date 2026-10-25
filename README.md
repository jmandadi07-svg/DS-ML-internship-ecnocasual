# EconoCausal

Dynamic pricing with Double Machine Learning. Infotact Solutions internship project (Advanced Data Science & ML Engineering, Vol. II, Project 2).

**Idea in one line:** instead of predicting who will buy, estimate who will buy *because of* a discount, then spend a fixed budget only on those customers.

## Team

| Name | Branch | Part |
|---|---|---|
| (team lead) | `name1` | Data and Causal Foundation |
| | `name2` | Double ML Modelling |
| | `name3` | Optimization and Backend API |
| | `name4` | Frontend Dashboard |

*Replace the names above with your real names. Each person's progress is in `members/<branch>/WORK_LOG.md`.*

## How we use git (simple rules)

1. `main` holds only merged, working code. The team lead merges into it. **Nobody commits directly to main.**
2. Everyone works on **their own branch** named after them.
3. Commit small and often, with a clear message like `Add DoWhy causal graph for synthetic data`. Empty, one-character, or duplicated commits do not count.
4. After each work session, add a line to your own `members/<branch>/WORK_LOG.md`.

Daily workflow:

```bash
git checkout your-branch
git pull
# ... do your work ...
git add .
git commit -m "What you did, in one clear sentence"
git push
```

Review requirements from the handbook: commits on at least 10 different days before the Mid Review, and on every one of the 20 days before the Final Review.

## What's done so far

- [x] Synthetic retail dataset generator with built-in confounding (`src/data_gen.py`)
- [x] Hillstrom real-data loader (`src/load_hillstrom.py`)
- [ ] Causal DAG in DoWhy (Week 1)
- [ ] Double ML with EconML (Week 2)
- [ ] Refutation tests (Mid Review)
- [ ] SciPy budget optimizer (Week 3)
- [ ] REST API and drift detector (Week 4)
- [ ] React + Plotly dashboard (Weeks 1-4)

## Datasets

### Synthetic retail data (main)

```bash
pip install -r requirements.txt
python src/data_gen.py     # creates data/synthetic_retail.csv
```

| Column | Meaning |
|---|---|
| `customer_id` | Unique ID |
| `age`, `past_purchases`, `loyalty_score`, `days_since_last_purchase` | Customer features (X) |
| `discount` | Treatment: 0, 10 or 20 dollars off |
| `bought` | Outcome: 1 if the customer bought |
| `spend` | Outcome: dollars spent |
| `true_ite_10`, `true_ite_20` | Ground-truth effect, only for validating the model. **Never use as features.** |

Confounding is built in: loyal customers get bigger discounts and also buy more anyway.

### Hillstrom Email Marketing (real data, randomized experiment)

1. Download the CSV from Kevin Hillstrom's MineThatData blog and save it as `data/hillstrom_raw.csv`.
2. Run `python src/load_hillstrom.py` to create `data/hillstrom_clean.csv`.

Treatment is an email (0/1), not a discount amount, so it is used only to show the pipeline works on real data.

## Folder structure

```
data/      datasets (generated files are git-ignored if large)
src/       project code
docs/      work distribution document and notes
members/   one folder per person with their WORK_LOG.md
```
