SELECT time,
       SUM(amount)::DECIMAL / COUNT(DISTINCT email_id) AS arppu,
       SUM(amount)::DECIMAL / COUNT(id) AS aov
FROM (
      SELECT id,
             date_trunc('month', date)::date AS time,
             amount,
             email_id
      FROM new_payments
      WHERE status = 'Confirmed') AS t1
GROUP BY time
