"""
data_gen.py  -  Synthetic retail dataset for EconoCausal
=========================================================

We create fake customers where WE decide how much a discount really helps each
one. That gives us the "true answer", so later we can check whether our
Double ML model finds it.

Treatment : discount in {0, 10, 20}  (dollars off)
Outcome   : bought (0/1) and spend (dollars)

Built-in CONFOUNDING (this is on purpose!):
    Loyal customers get discounts more often AND buy more anyway.
    A naive model will wrongly think discounts work really well.

Run:  python src/data_gen.py
"""

import numpy as np
import pandas as pd


def sigmoid(x):
    """Squashes any number into a probability between 0 and 1."""
    return 1 / (1 + np.exp(-x))


def generate_data(n=10_000, seed=42):
    rng = np.random.default_rng(seed)  # fixed seed -> same data every time

    # ---- 1. Customer features (X) -----------------------------------------
    age = rng.integers(18, 66, size=n)
    past_purchases = rng.poisson(4, size=n)              # orders in last year
    loyalty_score = rng.beta(2, 2, size=n)               # 0 = new, 1 = very loyal
    days_since_last = rng.integers(1, 366, size=n)

    # ---- 2. Treatment assignment (CONFOUNDED) -----------------------------
    # The company gives bigger discounts to loyal / frequent customers.
    # Because the same variables also affect buying, this creates confounding.
    score = 2.0 * (loyalty_score - 0.5) + 0.15 * (past_purchases - 4)
    logits = np.column_stack([
        np.zeros(n),          # $0  (reference)
        0.3 + score,          # $10
        -0.2 + 1.5 * score,   # $20
    ])
    probs = np.exp(logits)
    probs /= probs.sum(axis=1, keepdims=True)
    discount = np.array([rng.choice([0, 10, 20], p=p) for p in probs])

    # ---- 3. TRUE effect of a discount on buying probability ---------------
    # "price_sensitivity": how much this person responds to discounts.
    #   low loyalty + young  -> high sensitivity  (Persuadables)
    #   very loyal           -> ~0 or slightly negative (Sure Things / Sleeping Dogs)
    price_sensitivity = (0.40 * (1 - loyalty_score)
                         + 0.20 * (age < 30)
                         - 0.10)
    # Diminishing returns: $20 helps more than $10, but not twice as much.
    true_ite_10 = price_sensitivity * np.sqrt(10 / 20)
    true_ite_20 = price_sensitivity * np.sqrt(20 / 20)
    true_effect = np.where(discount == 10, true_ite_10,
                  np.where(discount == 20, true_ite_20, 0.0))

    # ---- 4. Outcome: did they buy? ----------------------------------------
    base_prob = sigmoid(-1.5 + 2.0 * loyalty_score
                        + 0.10 * past_purchases
                        - 0.004 * days_since_last)       # buys even with no discount
    buy_prob = np.clip(base_prob + true_effect, 0.01, 0.99)
    bought = rng.binomial(1, buy_prob)

    # ---- 5. Outcome: how much did they spend? -----------------------------
    order_value = 30 + 20 * loyalty_score + rng.normal(0, 5, size=n)
    spend = np.round(bought * np.clip(order_value - discount, 0, None), 2)

    return pd.DataFrame({
        "customer_id": np.arange(1, n + 1),
        "age": age,
        "past_purchases": past_purchases,
        "loyalty_score": loyalty_score.round(3),
        "days_since_last_purchase": days_since_last,
        "discount": discount,
        "bought": bought,
        "spend": spend,
        # Ground truth - ONLY for checking our model. NEVER use as features!
        "true_ite_10": true_ite_10.round(4),
        "true_ite_20": true_ite_20.round(4),
    })


if __name__ == "__main__":
    df = generate_data()
    df.to_csv("data/synthetic_retail.csv", index=False)
    print(f"Saved {len(df)} rows -> data/synthetic_retail.csv\n")
    print(df.head())

    print("\nDiscount counts:\n", df["discount"].value_counts().sort_index())

    # Show the confounding problem: naive comparison looks too good
    naive = df.groupby("discount")["bought"].mean()
    print("\nBuy rate by discount (NAIVE - misleading!):\n", naive.round(3))
    print("\nAverage TRUE effect of a $20 discount:",
          round(df["true_ite_20"].mean(), 3))
    print("Naive estimate ($20 vs $0)           :",
          round(naive[20] - naive[0], 3))
