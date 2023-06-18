SELECT sku,
       dates, 
       price,
       COUNT(price) AS qty
FROM transactions
GROUP BY sku, dates, price