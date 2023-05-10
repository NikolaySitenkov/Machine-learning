SELECT DATE(DATE_TRUNC('month', date)) AS time,
       mode,
       100 * COUNT(status) FILTER (WHERE status = 'Confirmed')::DECIMAL / COUNT(status) AS percents
FROM new_payments
WHERE mode != 'Не определено'
GROUP BY time, 
         mode
ORDER BY time, 
         mode