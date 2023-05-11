SELECT DATE(DATE_TRUNC('week', date)) AS weeks,
       COALESCE(SUM(amount) FILTER (WHERE status = 'Confirmed'), 0) AS sum_receipt
FROM new_payments
WHERE mode != 'Не определено'
GROUP BY weeks
ORDER BY weeks