-- =====================================================
-- Bookstore Sales Analysis | PostgreSQL
-- Tables: books, customers, orders
-- NOTE: Update the CSV file paths in the COPY commands to match
--       your own machine (the files must be readable by PostgreSQL).
-- =====================================================

-- ---------- 1. RESET (drop child table first) ----------
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS books;

-- ---------- 2. CREATE TABLES & LOAD DATA ----------
CREATE TABLE books (
    book_id         SERIAL PRIMARY KEY,
    title           VARCHAR(100) NOT NULL,
    author          VARCHAR(100) NOT NULL,
    genre           VARCHAR(100) NOT NULL,
    published_year  INT NOT NULL,
    price           NUMERIC(10,2) NOT NULL,
    stock           INT NOT NULL
);

COPY books (book_id, title, author, genre, published_year, price, stock)
FROM 'C:/Temp/Books.csv' WITH (FORMAT csv, HEADER);

CREATE TABLE customers (
    customer_id  SERIAL PRIMARY KEY,
    name         VARCHAR(100),
    email        VARCHAR(100),
    phone        VARCHAR(100),
    city         VARCHAR(100),
    country      VARCHAR(100)
);

COPY customers (customer_id, name, email, phone, city, country)
FROM 'C:/Temp/Customers.csv' WITH (FORMAT csv, HEADER);

CREATE TABLE orders (
    order_id      SERIAL PRIMARY KEY,
    customer_id   INT REFERENCES customers (customer_id),
    book_id       INT REFERENCES books (book_id),
    order_date    DATE,
    quantity      INT,
    total_amount  NUMERIC(10,2)
);

COPY orders (order_id, customer_id, book_id, order_date, quantity, total_amount)
FROM 'C:/Temp/Orders.csv' WITH (FORMAT csv, HEADER);

-- Quick check
SELECT * FROM books;
SELECT * FROM customers;
SELECT * FROM orders;

-- =====================================================
-- BASIC QUERIES
-- =====================================================

-- Q1: All Fantasy books, oldest first
SELECT * FROM books
WHERE genre = 'Fantasy'
ORDER BY published_year ASC;

-- Q2: Books published after 1950
SELECT * FROM books
WHERE published_year > 1950
ORDER BY published_year ASC;

-- Q3: Customers from Canada
SELECT * FROM customers
WHERE country = 'Canada';

-- Q4: Orders placed in November 2023, highest amount first
SELECT * FROM orders
WHERE order_date BETWEEN '2023-11-01' AND '2023-11-30'
ORDER BY total_amount DESC;

-- Q5: Total stock of all books
SELECT SUM(stock) AS total_stock FROM books;

-- Q6: Most expensive book
SELECT * FROM books
ORDER BY price DESC
LIMIT 1;

-- Q7: Orders with quantity greater than 1
SELECT * FROM orders
WHERE quantity > 1;

-- Q8: Orders with total amount above 20
SELECT * FROM orders
WHERE total_amount > 20;

-- Q9: All distinct genres
SELECT DISTINCT genre FROM books;

-- Q10: Book with the lowest stock (shows the title, not just the number)
SELECT title, stock FROM books
ORDER BY stock ASC
LIMIT 1;

-- Q11: Total sales revenue
SELECT SUM(total_amount) AS total_sales FROM orders;

-- =====================================================
-- JOINS & AGGREGATIONS
-- =====================================================

-- Q12: Total books sold per genre
SELECT b.genre,
       SUM(o.quantity) AS total_books_sold
FROM books b
INNER JOIN orders o ON b.book_id = o.book_id
GROUP BY b.genre;

-- Q13: Average price of Fantasy books
SELECT AVG(price) AS avg_fantasy_price
FROM books
WHERE genre = 'Fantasy';

-- Q14: Customers who placed 2 or more orders
-- (WHERE filters rows before grouping; HAVING filters after aggregation)
SELECT c.customer_id,
       c.name,
       COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) >= 2;

-- Q15: Most frequently ordered book
SELECT b.title,
       o.book_id,
       COUNT(o.order_id) AS times_ordered
FROM orders o
JOIN books b ON o.book_id = b.book_id
GROUP BY o.book_id, b.title
ORDER BY times_ordered DESC
LIMIT 1;

-- Q16: Top 3 most expensive Fantasy books
SELECT title, price, genre
FROM books
WHERE genre = 'Fantasy'
ORDER BY price DESC
LIMIT 3;

-- Q17: Total books sold by each author
SELECT b.author,
       SUM(o.quantity) AS total_books_sold_by_author
FROM books b
JOIN orders o ON b.book_id = o.book_id
GROUP BY b.author;

-- Q18: Cities where a customer placed an order above 30
SELECT DISTINCT c.city
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > 30
ORDER BY c.city;

-- Q19: Customer who spent the most (grouped by ID so same-name customers are not merged)
SELECT c.customer_id,
       c.name,
       SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC
LIMIT 1;

-- Q20: Remaining stock after all orders
SELECT b.book_id,
       b.title,
       b.stock,
       COALESCE(SUM(o.quantity), 0) AS ordered_quantity,
       b.stock - COALESCE(SUM(o.quantity), 0) AS remaining_quantity
FROM books b
LEFT JOIN orders o ON b.book_id = o.book_id
GROUP BY b.book_id, b.title, b.stock;
