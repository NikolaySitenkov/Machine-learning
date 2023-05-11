WITH sum_am AS (SELECT email_id,
                       SUM(amount) AS sum_amount
                FROM new_payments
                WHERE mode IN ('MasterCard', 'МИР', 'Visa')
                      AND status = 'Confirmed'
                GROUP BY email_id),
                
     max_am AS (SELECT MAX(sum_amount)
                FROM sum_am)

               
SELECT purchase_range,
       COUNT(email_id) AS num_of_users
FROM (SELECT CASE
                  WHEN sum_amount > 0 AND sum_amount <= 20000 THEN '0-20000'
                  WHEN sum_amount > 20000 AND sum_amount <= 40000 THEN '20000-40000'
                  WHEN sum_amount > 40000 AND sum_amount <= 60000 THEN '40000-60000'
                  WHEN sum_amount > 60000 AND sum_amount <= 80000 THEN '60000-80000'
                  WHEN sum_amount > 80000 AND sum_amount <= 100000 THEN '80000-100000'
                  WHEN sum_amount > 100000 AND sum_amount <= (SELECT * FROM max_am) THEN '100000-' || (SELECT * FROM max_am)::int::varchar(255)
             END AS purchase_range,
             CASE
                  WHEN sum_amount > 0 AND sum_amount <= 20000 THEN 1
                  WHEN sum_amount > 20000 AND sum_amount <= 40000 THEN 2
                  WHEN sum_amount > 40000 AND sum_amount <= 60000 THEN 3
                  WHEN sum_amount > 60000 AND sum_amount <= 80000 THEN 4
                  WHEN sum_amount > 80000 AND sum_amount <= 100000 THEN 5
                  WHEN sum_amount > 100000 AND sum_amount <= (SELECT * FROM max_am) THEN 6
             END AS ranked_segment,
                 email_id
     FROM sum_am) AS table1
GROUP BY purchase_range, ranked_segment
ORDER BY ranked_segment







