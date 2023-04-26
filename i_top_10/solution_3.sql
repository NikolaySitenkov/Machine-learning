SELECT vendor,
       COUNT(DISTINCT brand) as brand
FROM sku_dict_another_one
WHERE brand IS NOT NULL
GROUP BY vendor
ORDER BY brand DESC
LIMIT 10