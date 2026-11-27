# Bookstore Sales Analysis | PostgreSQL

> **Interview-ready summary:** see [CASE_STUDY.md](CASE_STUDY.md). Statistics: `analysis/bookstore_analysis.py`. BI-ready data: `bi_exports/`.


A SQL project that models a small online bookstore in **PostgreSQL** and answers 25 business questions about books, customers, and orders using joins, aggregations, and filtering.

## Database Schema

| Table | Key columns |
|---|---|
| `books` | book_id (PK), title, author, genre, published_year, price, stock |
| `customers` | customer_id (PK), name, email, phone, city, country |
| `orders` | order_id (PK), customer_id (FK), book_id (FK), order_date, quantity, total_amount |

Relationships: one customer can place many orders, and each order refers to one book.

## What the queries cover

- **Filtering and sorting:** books by genre or year, customers by country, orders by date range and amount
- **Aggregations:** total stock, total sales, average price, books sold per genre and per author
- **Joins:** customers with their orders, orders with book details, `LEFT JOIN` for remaining stock
- **Grouping with HAVING:** customers with 2 or more orders
- **Ranking-style questions:** most ordered book, top-spending customer, most expensive books
- **Business insights (Q21-Q25):** repeat-customer revenue share, dead stock, restock priority, revenue concentration, reactivation list (uses CTEs, window function `NTILE`, `FILTER`, `NOT EXISTS`)

## Key Findings (sample dataset)

The data is generated sample data (500 books, 500 customers, 500 orders, no nulls; `total_amount` equals `quantity x price` on every row), so the value here is the method and the recommendations, not real-world figures.

| Question | Finding | Query |
|---|---|---|
| Who drives revenue? | Repeat customers are 45.3% of buyers but bring **67.2% of revenue** | Q21 |
| How concentrated is revenue? | Top 20% of buyers (62 of 307) bring **47.1%** of revenue | Q24 |
| Who never bought? | **193 customers (38.6%)** never placed an order | Q25 |
| What stock is dead? | **183 titles (36.6%)** never sold, tying up **36.9%** of inventory value | Q22 |
| What may run out? | **30 titles** have ordered quantity above stock, 233 units in total | Q23 |

**Recommendations:** invest in retention for repeat buyers, run a reactivation campaign for customers who never ordered, stop reordering or discount the never-sold titles, and prioritise restocking (or a data check) for the 30 over-ordered titles. Genre revenue is fairly even; Fiction (9.6%) and Biography (10.4%) trail the other five genres (15-17% each).

## Project Files

```
bookstore-sales-analysis-postgresql/
|-- SQL PROJECT.sql   # schema, data load, 25 queries
|-- Books.csv
|-- Customers.csv
`-- Orders.csv
`-- README.md
```

## How to Run

1. Install PostgreSQL and open pgAdmin or `psql`.
2. Create a database, for example `bookstore`.
3. Put the three CSV files in a location PostgreSQL can read.
4. In `SQL PROJECT.sql`, change the three `COPY ... FROM '...'` paths to match where you saved the CSV files.
5. Run the script. It drops and recreates the tables, loads the data, and runs all 25 queries.

## Skills Demonstrated

PostgreSQL, relational schema design (primary and foreign keys), data import with `COPY`, `JOIN` (inner and left), `GROUP BY` / `HAVING`, aggregate functions, `COALESCE`, sorting and filtering.

## Author

**Digvijay Gadiwadd** | Data Analyst | Pune, India
