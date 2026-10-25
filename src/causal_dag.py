"""
causal_dag.py  -  Causal graph (DAG) + DoWhy analysis for EconoCausal
=====================================================================

DoWhy works in 4 steps. This script follows them in order:

    1. MODEL     - draw the causal graph (what affects what)
    2. IDENTIFY  - ask: "which variables must we control for to get the
                   true effect of the discount?"
    3. ESTIMATE  - calculate the effect of the discount on buying
    4. REFUTE    - try to break our own answer (the "causal audit")

Run (from the project root, after running src/data_gen.py):
    pip install dowhy matplotlib
    python src/causal_dag.py

Simplification for Week 1:
    The discount has 3 levels ($0, $10, $20). To keep things clear we compare
    only $0 vs $20, so the treatment is a simple yes/no.
    (Extending to $10 is a good Week 2 task.)
"""

import os
import sys

import pandas as pd

DATA_PATH = "data/synthetic_retail.csv"
PLOT_PATH = "docs/causal_graph.png"

# ---------------------------------------------------------------------------
# THE CAUSAL GRAPH
# ---------------------------------------------------------------------------
TREATMENT = "got_20_discount"   # what we change (yes/no)
OUTCOME = "bought"              # what we care about (yes/no)

# CONFOUNDERS: affect BOTH who gets a discount AND who buys.
# In our data: loyal, frequent customers are given bigger discounts,
# and they also buy more even without any discount.
CONFOUNDERS = ["loyalty_score", "past_purchases"]

# These affect buying only. They don't affect who gets a discount.
OUTCOME_ONLY = ["age", "days_since_last_purchase"]

# Each pair (A, B) means "A causes B"  (an arrow A -> B)
EDGES = (
    [(c, TREATMENT) for c in CONFOUNDERS]                # confounder -> discount
    + [(c, OUTCOME) for c in CONFOUNDERS + OUTCOME_ONLY]  # features   -> buying
    + [(TREATMENT, OUTCOME)]                              # discount   -> buying
)
# NOTE: we know this graph because WE wrote the data generator. With real data
# you would not know it, and would have to build it with domain experts.


def load_data():
    """Load the synthetic data and keep only customers with $0 or $20."""
    if not os.path.exists(DATA_PATH):
        sys.exit(f"Can't find {DATA_PATH}. Run first:  python src/data_gen.py")

    df = pd.read_csv(DATA_PATH)
    df = df[df["discount"].isin([0, 20])].copy()
    df[TREATMENT] = df["discount"] == 20          # True / False

    # The generator saved the TRUE effect for each customer.
    # We keep the average only to CHECK our answer at the end.
    # We must NOT give it to the model (that would be cheating).
    true_ate = df["true_ite_20"].mean()

    df = df[CONFOUNDERS + OUTCOME_ONLY + [TREATMENT, OUTCOME]]
    return df, true_ate


def build_gml(edges):
    """Turn our list of arrows into the text format DoWhy understands (GML)."""
    nodes = sorted({n for edge in edges for n in edge})
    lines = ["graph [", "  directed 1"]
    for n in nodes:
        lines.append(f'  node [ id "{n}" label "{n}" ]')
    for source, target in edges:
        lines.append(f'  edge [ source "{source}" target "{target}" ]')
    lines.append("]")
    return "\n".join(lines)


def draw_graph(path=PLOT_PATH):
    """Save a picture of the graph (useful for the review and the viva)."""
    try:
        import matplotlib
        matplotlib.use("Agg")   # draw to a file, no window needed
        import matplotlib.pyplot as plt
        import networkx as nx
    except ImportError:
        print("(Skipping the picture: run  pip install matplotlib networkx)")
        return

    g = nx.DiGraph(EDGES)
    pos = {
        "loyalty_score": (-0.7, 2), "past_purchases": (0.7, 2),
        TREATMENT: (-2, 0), OUTCOME: (2, 0),
        "age": (-0.7, -2), "days_since_last_purchase": (0.7, -2),
    }
    colors = []
    for n in g.nodes:
        if n == TREATMENT:
            colors.append("#f4a261")      # orange = treatment
        elif n == OUTCOME:
            colors.append("#2a9d8f")      # green  = outcome
        elif n in CONFOUNDERS:
            colors.append("#e76f51")      # red    = confounders
        else:
            colors.append("#a8dadc")      # blue   = outcome-only features
    labels = {n: n.replace("_", "\n") for n in g.nodes}

    plt.figure(figsize=(10, 6))
    nx.draw(g, pos, labels=labels, node_color=colors, node_size=5000,
            font_size=8, arrowsize=18, edge_color="#555555",
            connectionstyle="arc3,rad=0.05")
    plt.title("EconoCausal causal graph\n"
              "orange = discount, green = bought, red = confounders, blue = other features")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved graph picture -> {path}")


def main():
    try:
        from dowhy import CausalModel
    except ImportError:
        sys.exit("DoWhy is not installed. Run:  pip install dowhy")

    df, true_ate = load_data()
    print(f"Customers used (discount $0 or $20): {len(df)}")

    # --- Naive answer: just compare the two groups (misleading!) ----------
    rates = df.groupby(TREATMENT)[OUTCOME].mean()
    naive = rates[True] - rates[False]

    draw_graph()

    # --- Step 1: MODEL ----------------------------------------------------
    model = CausalModel(
        data=df,
        treatment=TREATMENT,
        outcome=OUTCOME,
        graph=build_gml(EDGES),
    )

    # --- Step 2: IDENTIFY -------------------------------------------------
    # DoWhy reads the graph and works out what we must control for.
    # Look for "backdoor" in the output: it lists the confounders it found.
    identified = model.identify_effect(proceed_when_unidentifiable=True)
    print("\n=== STEP 2: IDENTIFIED ESTIMAND ===")
    print(identified)

    # --- Step 3: ESTIMATE -------------------------------------------------
    # Linear regression that controls for the confounders found above.
    estimate = model.estimate_effect(
        identified,
        method_name="backdoor.linear_regression",
        target_units="ate",   # ATE = Average Treatment Effect over everyone
    )
    print("\n=== STEP 3: ESTIMATE ===")
    print(estimate)

    print("\n=== RESULT: effect of a $20 discount on probability of buying ===")
    print(f"  Naive (just compare groups): {naive:+.3f}")
    print(f"  DoWhy (controls confounders): {estimate.value:+.3f}")
    print(f"  TRUE effect (from generator): {true_ate:+.3f}")
    print("  The DoWhy number should be closer to the TRUE one than the naive one.")

    # --- Step 4: REFUTE ---------------------------------------------------
    # Each test tries to break our answer. A trustworthy answer survives.
    print("\n=== STEP 4: REFUTATION TESTS ===")
    tests = [
        # Add a random fake confounder. Answer should barely change.
        ("random_common_cause", {}),
        # Re-run on random 80% subsets. Answer should stay similar.
        ("data_subset_refuter", {"subset_fraction": 0.8}),
        # Replace the real discount with a shuffled fake one.
        # The effect should drop to about 0 (a fake treatment does nothing).
        ("placebo_treatment_refuter", {"placebo_type": "permute"}),
    ]
    for name, extra in tests:
        print(f"\n--- {name} ---")
        try:
            result = model.refute_estimate(
                identified, estimate, method_name=name,
                num_simulations=20, **extra,
            )
            print(result)
        except Exception as err:   # keep going if one test fails
            print(f"{name} failed: {err}")


if __name__ == "__main__":
    main()
