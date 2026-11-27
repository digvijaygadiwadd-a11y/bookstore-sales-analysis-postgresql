"""
Bookstore analysis: statistics, charts and BI-ready exports.

Complements the 25 SQL queries with (1) hypothesis tests, (2) bootstrap confidence
intervals, (3) an A/B test sample-size calculation for the retention recommendation,
(4) charts, and (5) a star-schema CSV export for Power BI / Tableau.

Run from the repo root:  python analysis/bookstore_analysis.py
Requires: pandas, numpy, scipy, matplotlib.
NOTE: the dataset is generated sample data, so results demonstrate the method.
"""
import os, math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

ROOT = os.path.join(os.path.dirname(__file__), "..")
books = pd.read_csv(os.path.join(ROOT, "Books.csv"))
customers = pd.read_csv(os.path.join(ROOT, "Customers.csv"))
orders = pd.read_csv(os.path.join(ROOT, "Orders.csv"), parse_dates=["Order_Date"])
rng = np.random.default_rng(42)

# ---------- Star schema export for Power BI / Tableau ----------
fact = (orders.merge(books, on="Book_ID").merge(customers, on="Customer_ID", suffixes=("", "_cust")))
orders_per_cust = orders.groupby("Customer_ID").size().rename("Customer_Order_Count")
fact = fact.merge(orders_per_cust, on="Customer_ID")
fact["Customer_Type"] = np.where(fact["Customer_Order_Count"] >= 2, "Repeat", "One-time")
sold = orders.groupby("Book_ID")["Quantity"].sum().rename("Units_Sold")
dim_books = books.merge(sold, on="Book_ID", how="left").fillna({"Units_Sold": 0})
dim_books["Inventory_Value"] = dim_books["Stock"] * dim_books["Price"]
dim_books["Never_Sold"] = dim_books["Units_Sold"] == 0
dim_books["Over_Ordered"] = dim_books["Units_Sold"] > dim_books["Stock"]
dim_customers = customers.merge(orders_per_cust, on="Customer_ID", how="left").fillna({"Customer_Order_Count": 0})
dim_customers["Segment"] = pd.cut(dim_customers["Customer_Order_Count"], [-1, 0, 1, 100],
                                  labels=["Never ordered", "One-time", "Repeat"])
os.makedirs(os.path.join(ROOT, "bi_exports"), exist_ok=True)
fact.to_csv(os.path.join(ROOT, "bi_exports", "fact_orders.csv"), index=False)
dim_books.to_csv(os.path.join(ROOT, "bi_exports", "dim_books.csv"), index=False)
dim_customers.to_csv(os.path.join(ROOT, "bi_exports", "dim_customers.csv"), index=False)

lines = []
def say(s=""):
    print(s); lines.append(s)

# ---------- 1. Do repeat customers place bigger orders? (Welch t-test) ----------
rep = fact.loc[fact.Customer_Type == "Repeat", "Total_Amount"]
one = fact.loc[fact.Customer_Type == "One-time", "Total_Amount"]
t, p = stats.ttest_ind(rep, one, equal_var=False)
pooled_sd = math.sqrt((rep.var() + one.var()) / 2)
d = (rep.mean() - one.mean()) / pooled_sd
say("1. Order value: repeat vs one-time customers (Welch t-test)")
say(f"   mean repeat = {rep.mean():.2f} (n={len(rep)}), one-time = {one.mean():.2f} (n={len(one)})")
say(f"   t = {t:.2f}, p = {p:.3f}, Cohen's d = {d:.2f}")
say("   -> " + ("significant difference" if p < 0.05 else "no significant difference: repeat buyers' revenue comes from ORDER FREQUENCY, not bigger baskets"))

# ---------- 2. Bootstrap CI for the revenue share of repeat customers ----------
cust_spend = orders.groupby("Customer_ID").agg(n=("Order_ID", "count"), spent=("Total_Amount", "sum"))
def repeat_share(df):
    return df.loc[df.n >= 2, "spent"].sum() / df["spent"].sum() * 100
boot = [repeat_share(cust_spend.sample(len(cust_spend), replace=True, random_state=int(rng.integers(1e9))))
        for _ in range(2000)]
lo, hi = np.percentile(boot, [2.5, 97.5])
say("\n2. Repeat customers' share of revenue, bootstrap 95% CI (2,000 resamples)")
say(f"   point estimate = {repeat_share(cust_spend):.1f}%, 95% CI = [{lo:.1f}%, {hi:.1f}%]")

# ---------- 3. Does price affect units per order? (Spearman) ----------
rho, p_rho = stats.spearmanr(fact["Price"], fact["Quantity"])
say("\n3. Price vs quantity per order (Spearman rank correlation)")
say(f"   rho = {rho:.3f}, p = {p_rho:.3f} -> " + ("price affects quantity" if p_rho < 0.05 else "no detectable price effect on quantity"))

# ---------- 4. Genre revenue differences (one-way ANOVA on order value) ----------
groups = [g["Total_Amount"].values for _, g in fact.groupby("Genre")]
f_stat, p_anova = stats.f_oneway(*groups)
say("\n4. Order value across genres (one-way ANOVA)")
say(f"   F = {f_stat:.2f}, p = {p_anova:.3f} -> " + ("genres differ in order value" if p_anova < 0.05 else "no significant difference in order value between genres"))

# ---------- 5. A/B test design for the retention recommendation ----------
base = (cust_spend.n >= 2).mean()
mde = 0.05
alpha, power = 0.05, 0.80
z_a, z_b = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
p1, p2 = base, base + mde
n_per_arm = math.ceil(((z_a * math.sqrt(2 * ((p1 + p2) / 2) * (1 - (p1 + p2) / 2)) +
                        z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / (mde ** 2))
say("\n5. Proposed A/B test: loyalty offer to one-time buyers (design only, not run)")
say(f"   baseline repeat-purchase rate = {base:.1%}; to detect +{mde:.0%} absolute lift at alpha={alpha}, power={power:.0%}")
say(f"   required sample = {n_per_arm} customers per arm ({2 * n_per_arm} total)")
say(f"   current buyers = {len(cust_spend)}, so this store is too small to test quickly; a pooled or longer test would be needed")

with open(os.path.join(ROOT, "analysis", "results.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")

# ---------- Charts ----------
os.makedirs(os.path.join(ROOT, "charts"), exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

seg = dim_customers["Segment"].value_counts().reindex(["Repeat", "One-time", "Never ordered"])
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].bar(seg.index, seg.values, color=["#1b9e77", "#7570b3", "#bdbdbd"])
ax[0].set_title("Customers by segment (500 total)")
for i, v in enumerate(seg.values): ax[0].text(i, v + 3, str(v), ha="center")
rev_seg = fact.groupby("Customer_Type")["Total_Amount"].sum()
share = (rev_seg / rev_seg.sum() * 100).reindex(["Repeat", "One-time"])
ax[1].bar(share.index, share.values, color=["#1b9e77", "#7570b3"])
ax[1].set_title("Share of revenue by customer type (%)")
for i, v in enumerate(share.values): ax[1].text(i, v + 1, f"{v:.1f}%", ha="center")
fig.tight_layout(); fig.savefig(os.path.join(ROOT, "charts", "01_customer_segments_revenue.png"), dpi=130); plt.close(fig)

g = fact.groupby("Genre")["Total_Amount"].sum().sort_values()
fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(g.index, g.values / g.sum() * 100, color="#4c78a8")
ax.set_title("Revenue share by genre (%)")
for i, v in enumerate(g.values / g.sum() * 100): ax.text(v + 0.2, i, f"{v:.1f}%", va="center")
fig.tight_layout(); fig.savefig(os.path.join(ROOT, "charts", "02_genre_revenue_share.png"), dpi=130); plt.close(fig)

inv_total = dim_books["Inventory_Value"].sum()
dead = dim_books.loc[dim_books.Never_Sold, "Inventory_Value"].sum()
fig, ax = plt.subplots(figsize=(6, 4))
ax.pie([dead, inv_total - dead], labels=[f"Never-sold titles\n{dead/inv_total:.1%}", f"Titles with sales\n{1-dead/inv_total:.1%}"],
       colors=["#e45756", "#9ecae9"], startangle=90, wedgeprops={"width": 0.45})
ax.set_title("Inventory value tied up in dead stock")
fig.tight_layout(); fig.savefig(os.path.join(ROOT, "charts", "03_dead_stock.png"), dpi=130); plt.close(fig)

cs = cust_spend.sort_values("spent", ascending=False)["spent"].values
cum = np.cumsum(cs) / cs.sum() * 100
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(np.arange(1, len(cs) + 1) / len(cs) * 100, cum, color="#1b9e77", lw=2)
ax.plot([0, 100], [0, 100], "--", color="#999")
ax.set_xlabel("% of buying customers (highest spenders first)"); ax.set_ylabel("Cumulative % of revenue")
ax.set_title("Revenue concentration (Pareto curve)")
fig.tight_layout(); fig.savefig(os.path.join(ROOT, "charts", "04_pareto_curve.png"), dpi=130); plt.close(fig)
print("\nSaved: bi_exports/*.csv, charts/*.png, analysis/results.txt")
