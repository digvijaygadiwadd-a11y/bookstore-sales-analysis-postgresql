# Bookstore Sales Analysis | PostgreSQL

A SQL project that models a small online bookstore in **PostgreSQL** and answers 20 business questions about books, customers, and orders using joins, aggregations, and filtering.

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

## Project Files

```
bookstore-sales-analysis-postgresql/
|-- SQL_PROJECT.sql   # schema, data load, 20 queries
|-- data/
|   |-- Books.csv
|   |-- Customers.csv
|   `-- Orders.csv
`-- README.md
```

## How to Run

1. Install PostgreSQL and open pgAdmin or `psql`.
2. Create a database, for example `bookstore`.
3. Put the three CSV files from the `data/` folder in a location PostgreSQL can read.
4. In `SQL_PROJECT.sql`, change the three `COPY ... FROM '...'` paths to match where you saved the CSV files.
5. Run the script. It drops and recreates the tables, loads the data, and runs all 20 queries.

## Skills Demonstrated

PostgreSQL, relational schema design (primary and foreign keys), data import with `COPY`, `JOIN` (inner and left), `GROUP BY` / `HAVING`, aggregate functions, `COALESCE`, sorting and filtering.

## Author

**Digvijay Gadiwadd** | Data Analyst | Pune, India
