SELECT vendor,
       COUNT(sku_type) as sku
FROM sku_dict_another_one
GROUP BY vendor
ORDER BY sku DESC
LIMIT 10