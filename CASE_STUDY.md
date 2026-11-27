# Bookstore Sales Analysis: Case Study

**One line:** from raw orders to a business decision: who drives revenue, what stock is dead, what is about to run out, and what to do about it.

> **Data note:** the dataset is generated sample data (500 books, 500 customers, 500 orders). The value here is the method, the statistics and the recommendations, not real-world figures.

## 1. The business question
A bookstore owner wants to know where revenue really comes from, which stock is wasting money, and which titles may run out, so they can decide where to spend on retention, clearance and restocking.

## 2. Approach
1. **Validate first:** 0 nulls; `total_amount` equals `quantity x price` on all 500 orders.
2. **SQL (PostgreSQL, 25 queries):** the first 20 answer descriptive questions; Q21-Q25 answer business questions with CTEs, `NTILE`, `FILTER` and `NOT EXISTS`.
3. **Statistics (Python):** Welch t-test, bootstrap confidence interval, Spearman correlation, ANOVA, and an A/B test sample-size calculation.
4. **Visualisation and BI:** four charts, plus a star-schema export (`bi_exports/`) ready for Power BI or Tableau (see `BI_DASHBOARD_GUIDE.md`).

## 3. Findings and the decision each one supports
| Finding | Evidence | Decision |
|---|---|---|
| Repeat customers drive most revenue | 45.3% of buyers bring **67.2%** of revenue (95% CI **60.9% to 73.3%**) | Invest in retention |
| Repeat buyers do not place bigger orders | order value 152.98 vs 147.86, **p = 0.65** | Grow *frequency* (reorder reminders, loyalty), not basket size (upselling) |
| Revenue is concentrated | top 20% of buyers (62 of 307) bring **47.1%** | Protect and reward top buyers |
| Many customers never bought | **193 (38.6%)** never ordered | Run a reactivation campaign |
| Dead stock | **183 titles (36.6%)** never sold, tying up **36.9%** of inventory value | Stop reordering, discount or clear |
| Stock risk | **30 titles** have orders above stock (233 units) | Restock first, or check the data |
| Genres | order value does not differ by genre (ANOVA p = 0.72); Fiction 9.6% and Biography 10.4% of revenue vs 15-17% for the others | Do not drop genres on order value; review range depth in the two smaller ones |

## 4. Testing the recommendation (A/B design, not run)
To test a loyalty offer for one-time buyers and detect a +5 point lift in repeat-purchase rate (baseline 45.3%, alpha 0.05, power 80%), **1,566 customers per arm** are needed. With only 307 buyers, this store is too small to test quickly. That is a useful finding in itself: **do not run an underpowered test and over-read the result.**

## 5. Limitations
Synthetic data; "stock" is treated as opening stock (same as Q20); the A/B test is a design, not a result.

## 6. Interview Q&A
**What was the most useful insight?** That repeat customers' extra revenue comes from ordering more often, not from bigger baskets (p = 0.65), which changes the recommendation from upselling to loyalty.
**Why did you not run the A/B test?** The required sample (about 3,100 customers) is 10 times what this store has. I designed it and said so.
**How would you present this to the owner?** Start with the money: 37% of inventory value is dead stock and 67% of revenue comes from repeat buyers, then give the three actions.
