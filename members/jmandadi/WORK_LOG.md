# Work Log: M.Sai Jayasankara

**Branch:** `jay`
**Part:** (e.g. Data and Causal Foundation)

Add one row each time you finish something. Be specific, and link the file or commit.

## Week 1

| Date | What I did | Files / commit |
|25-10-2026|Created the GitHub repo and set up branches and folder structure|repo|
|25-10-2026 | Generated the synthetic retail dataset with built-in confounding (loyal customers get bigger discounts and also buy more)|src/data_gen.py |
|25-10-2026|Wrote the Hillstrom loader for the real-data comparison|src/load_hillstrom.py|
| 25 Oct 2026 | Drew the causal graph: loyalty_score and past_purchases are confounders, age and days_since_last_purchase affect buying only | src/causal_dag.py, docs/causal_graph.png |
| 25 Oct 2026 | DoWhy identified the backdoor adjustment set (past_purchases, loyalty_score), matching our graph | docs/week1_results.txt |
| 25 Oct 2026 | Estimated the effect of a $20 discount: naive +0.208, DoWhy +0.166, true +0.156 | docs/week1_results.txt |
| 25 Oct 2026 | Ran refutation tests. Placebo treatment passed (effect about 0, p about 0.45). Random common cause: [fill in]. Data subset: [fill in] | docs/week1_results.txt |
| 25 Oct 2026 | Fixed version errors: pinned networkx<3.5 and pandas<3 for DoWhy | requirements.txt |

## Week 2

| Date | What I did | Files / commit |
|---|---|---|
| | | |

## Mid Review notes

(What I will demo, and what I need to be able to explain in the viva.)

## Week 3

| Date | What I did | Files / commit |
|---|---|---|
| | | |

## Week 4

| Date | What I did | Files / commit |
|---|---|---|
| | | |

## What I learned / what I'm stuck on
