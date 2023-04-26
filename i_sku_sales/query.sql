SELECT cal_date as days, sum(cnt) as sku 
FROM transactions_another_one
GROUP BY cal_date