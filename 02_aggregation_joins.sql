-- 02_aggregation_joins.sql

-- (a) INNER JOIN with aggregation and HAVING
SELECT p.category,
       COUNT(o.order_id) AS order_count,
       SUM(o.amount_inr) AS total_revenue,
       AVG(o.amount_inr) AS avg_amount_inr
FROM orders o
INNER JOIN products p ON p.product_id = o.product_id
WHERE o.status = 'Delivered'
GROUP BY p.category
HAVING SUM(o.amount_inr) > 10000
ORDER BY total_revenue DESC;

-- (b) LEFT JOIN to keep the zero-order product in the result set
SELECT p.product_name,
       COUNT(o.order_id) AS total_orders
FROM products p
LEFT JOIN orders o ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_orders ASC, p.product_name;
