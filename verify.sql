-- Verification results:
-- products = 31
-- customers = 50
-- orders = 500
-- category_targets = 6
-- status counts:
-- Cancelled = 42
-- Delivered = 434
-- Pending = 24

SELECT COUNT(*) AS product_count
FROM products;

SELECT COUNT(*) AS customer_count
FROM customers;

SELECT COUNT(*) AS order_count
FROM orders;

SELECT COUNT(*) AS category_target_count
FROM category_targets;

SELECT status, COUNT(*) AS total_orders
FROM orders
GROUP BY status
ORDER BY status;
