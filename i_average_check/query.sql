SELECT month, 
       avg(check_amount) as avg_check,
       quantileExactExclusive(0.5)(check_amount) as median_check
FROM
    (SELECT toStartOfMonth(toDate(buy_date)) as month, 
            check_amount
     FROM default.view_checks) as t1
GROUP BY month