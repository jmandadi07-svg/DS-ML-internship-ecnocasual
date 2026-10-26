# Work Log: M.Sai Jayasankara

**Branch:** `jay`
**Part:** (e.g. Data and Causal Foundation)

Add one row each time you finish something. Be specific, and link the file or commit.

## Week 1

| Date | What I did | Files / commit |
|16-10-2026|Created the GitHub repo and set up branches and folder structure|repo|
|16-10-2026 | Generated the synthetic retail dataset with built-in confounding (loyal customers get bigger discounts and also buy more)|src/data_gen.py |
|16-10-2026|Wrote the Hillstrom loader for the real-data comparison|src/load_hillstrom.py|


## Week 2

| Date | What I did | Files / commit |
| 25 Oct 2026 | Drew the causal graph: loyalty_score and past_purchases are confounders, age and days_since_last_purchase affect buying only | src/causal_dag.py, docs/causal_graph.png |
| 25 Oct 2026 | DoWhy identified the backdoor adjustment set (past_purchases, loyalty_score), matching our graph | docs/week1_results.txt |
| 25 Oct 2026 | Estimated the effect of a $20 discount: naive +0.208, DoWhy +0.166, true +0.156 | docs/week1_results.txt |
| 25 Oct 2026 | Ran refutation tests. Placebo treatment passed (effect about 0, p about 0.45). Random common cause: [fill in]. Data subset: [fill in] | docs/week1_results.txt |
| 25 Oct 2026 | Fixed version errors: pinned networkx<3.5 and pandas<3 for DoWhy | requirements.txt |

## Mid Review notes

MID REVIEW NOTES

What I will demo
1. The repo: main branch plus my own branch, folders src, data, docs, members, and this work log.
2. src/data_gen.py: generates 10,000 synthetic customers with discounts of $0, $10 or $20. Loyal customers get bigger discounts and also buy more anyway, so the data is confounded on purpose.
3. docs/causal_graph.png: the causal graph.
4. src/causal_dag.py: run live. It identifies what to control for, estimates the effect of a $20 discount, and runs refutation tests.
5. Week 2 (pending, update before the review): Double ML model, effect per customer, uplift curve.

Key results
- Naive comparison (discount vs no discount): +0.208
- DoWhy, controlling for confounders: +0.166
- True effect built into the data: +0.156
- Placebo test: effect dropped to about 0 (p about 0.45). Passed.
- Random common cause: [fill in]
- Data subset: [fill in]

Things I must be able to explain
- Confounder: a variable that affects both who gets the treatment and the outcome. Here, loyalty_score and past_purchases. Loyal customers get more discounts and buy more anyway.
- Why the naive number is wrong: it mixes the effect of the discount with the fact that discounted customers were already more likely to buy. It overstates the effect by about a third.
- Why age and days_since_last_purchase are not confounders: in our data they affect buying but do not affect who receives a discount.
- What DoWhy's identify step does: reads the graph and works out which variables to control for. It chose past_purchases and loyalty_score, matching our graph.
- What a refutation test is: an attempt to break our own answer. Placebo replaces the discount with a shuffled fake one, and the effect should drop to zero. Random common cause adds a fake confounder, and the answer should barely change. Data subset re-runs on 80% samples, and the answer should stay similar.
- Why the true effect is known: we wrote the data generator, so we saved the real effect for each customer to check our answer.

Limitations (be honest about these)
- The data is synthetic, and the graph is known because we wrote the generator. With real data, the graph would have to be built with domain experts.
- So far I compared only $0 vs $20, not $10.
- Linear regression assumes the same effect for everyone, but the effect varies (it falls with age). Double ML in Week 2 estimates effects per customer.

Problems I solved
- DoWhy crashed with the newest networkx and pandas. Fixed by pinning networkx<3.5 and pandas<3 in requirements.txt.

Week 2 status (update before the review)
- EconML Double ML model: [not started]
- Effect per customer saved to CSV: [not started]
- Uplift / Qini curve: [not started]

## Week 3

| Date | What I did | Files / commit |
|---|---|---|
| | | |

## Week 4

| Date | What I did | Files / commit |
|---|---|---|
| | | |

## What I learned / what I'm stuck on
