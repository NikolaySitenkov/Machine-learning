SELECT DISTINCT day,
       COUNT(DISTINCT user_id) OVER (ORDER BY day ASC
                                     RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS wau
FROM (
SELECT *,
       toDate(timestamp) AS day
FROM churn_submits) AS t1
