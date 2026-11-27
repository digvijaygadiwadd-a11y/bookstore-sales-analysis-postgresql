# Build the Power BI / Tableau Dashboard (about 1 hour)

The data model is already prepared in `bi_exports/` as a star schema:
`fact_orders.csv` (one row per order, joined to book and customer attributes), `dim_books.csv`, `dim_customers.csv`.

## Power BI
1. Get Data -> Text/CSV -> load the three files.
2. Model view: relate `fact_orders[Book_ID]` -> `dim_books[Book_ID]` and `fact_orders[Customer_ID]` -> `dim_customers[Customer_ID]` (many-to-one).
3. Measures (DAX):
   - `Revenue = SUM(fact_orders[Total_Amount])`
   - `Repeat Revenue % = DIVIDE(CALCULATE([Revenue], fact_orders[Customer_Type]="Repeat"), [Revenue])`
   - `Dead Stock Value = CALCULATE(SUM(dim_books[Inventory_Value]), dim_books[Never_Sold]=TRUE())`
   - `Dead Stock % = DIVIDE([Dead Stock Value], SUM(dim_books[Inventory_Value]))`
4. Page 1 "Revenue": KPI cards (Revenue, Repeat Revenue %, Dead Stock %), a bar chart of revenue by genre, a customer-segment donut.
5. Page 2 "Inventory": table of `Over_Ordered` titles and `Never_Sold` titles with `Inventory_Value`.
6. Add a text box with the three recommendations. Save a screenshot as `charts/dashboard.png`.

## Tableau
Connect to `fact_orders.csv`, join `dim_books` and `dim_customers`, then build the same KPI cards and bar charts as calculated fields.

## Rule for the resume
Add the dashboard screenshot to this repo before listing "Power BI" or "Tableau" next to this project.
