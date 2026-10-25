# Work Distribution Document

*Due before the Mid Review of Month 1. Update it if anyone becomes unresponsive.*

| Member | Branch | Part | Week 1 | Week 2 | Week 3 | Week 4 |
|---|---|---|---|---|---|---|
| (Team Lead) | name1 | Data and Causal Foundation | DoWhy DAG | Propensity matching | Merge and integrate | Drift detector |
| | name2 | Double ML Modelling | Learn EconML, test on mock data | Train DML, compute ITE | Tune, compare with standard model | Package and document |
| | name3 | Optimization and Backend API | API design and JSON formats | Basic API with mock data | SciPy optimizer | Full REST API |
| | name4 | Frontend Dashboard | React scaffold, upload page | Qini/uplift charts | Allocation table | Polish and connect to API |

## Shared handoff files

| File | Produced by | Used by |
|---|---|---|
| `data/synthetic_retail.csv` | Data person | Everyone |
| ITE predictions CSV (`customer_id`, `ite_10`, `ite_20`) | Modelling person | Optimizer, Dashboard |
| Allocation JSON (`customer_id`, `discount`) | Optimizer person | Dashboard |
