SELECT * FROM atliq_tshirts.discounts;

SELECT COUNT(*) FROM atliq_tshirts.t_shirts;

SELECT DISTINCT brand, size, color, stock_quantity FROM atliq_tshirts.t_shirts;

-- Question 1: How many t-shirts do we have left for Nike in extra small size and white colour?
-- Status: Tested & Passed
SELECT `stock_quantity` FROM atliq_tshirts.t_shirts WHERE `brand` = 'Nike' AND `size` = 'XS' AND `color` = 'White' LIMIT 1; -- Result from LLM

SELECT * FROM atliq_tshirts.t_shirts WHERE brand = 'Nike' AND size = 'XS' AND color = 'White';

-- Question 2: How much is the inventory cost for all small-sized t-shirts?
-- Status: Tested & Passed
SELECT SUM(price*stock_quantity) FROM atliq_tshirts.t_shirts WHERE size = 'S';

-- Question 3: How much revenue will our store generate (after discounts) if we sell all the Levi's T-shirts today?
-- Status: Tested & Passed
SELECT SUM(`t_shirts`.`price` * `t_shirts`.`stock_quantity` * (1 - COALESCE(`discounts`.`pct_discount`, 0) / 100)) AS `total_revenue` 
FROM atliq_tshirts.t_shirts LEFT JOIN atliq_tshirts.discounts ON `t_shirts`.`t_shirt_id` = `discounts`.`t_shirt_id` WHERE `t_shirts`.`brand` = 'Levi';

-- Question 4: SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'
-- Status: Tested & Passed
SELECT SUM(price * stock_quantity) FROM atliq_tshirts.t_shirts WHERE brand = 'Levi';

-- Question 5: How many white Levi's t-shirts do we have available?
-- Status: Tested & Passed
SELECT SUM(`stock_quantity`) FROM atliq_tshirts.t_shirts WHERE `brand` = 'Levi' AND `color` = 'White'; -- Result from LLM

SELECT * FROM atliq_tshirts.t_shirts WHERE `brand` = 'Levi' AND `color` = 'White'; 

-- Question 6: What is the percentage contribution of Nike to the total stock quantity of the entire inventory?
-- Status: Tested & Passed
SELECT (SUM(CASE WHEN `brand` = 'Nike' THEN `stock_quantity` ELSE 0 END) * 100.0 / SUM(`stock_quantity`)) AS `percentage` FROM atliq_tshirts.t_shirts;

-- Question 7: List all brands that have more than 50 total items in stock, but only considering White and Blue colors
-- Status: Tested & Passed
SELECT `brand`, SUM(`stock_quantity`) AS `total_stock` FROM atliq_tshirts.t_shirts WHERE `color` IN ('White', 'Blue') GROUP BY `brand` HAVING `total_stock` > 50;

-- Question 8: List all brands that have more than 500 total items in stock, but only considering White and Blue colors
-- Status: Tested & Passed
SELECT `brand` FROM atliq_tshirts.t_shirts WHERE `color` IN ('White', 'Blue') GROUP BY `brand` HAVING SUM(`stock_quantity`) > 500; -- Result from LLM

SELECT `brand`, SUM(`stock_quantity`) FROM atliq_tshirts.t_shirts WHERE `color` IN ('White', 'Blue') GROUP BY `brand` HAVING SUM(`stock_quantity`) > 500;

-- Question 9: Find all colours that are not available in the Adidas brand.
-- Status: Tested & Passed
SELECT DISTINCT `color` FROM atliq_tshirts.t_shirts WHERE `color` NOT IN (SELECT `color` FROM atliq_tshirts.t_shirts WHERE `brand` = 'Adidas'); -- Result from LLM

SELECT * FROM atliq_tshirts.t_shirts WHERE color IN ('White', 'Blue') AND brand = 'Nike';

-- Question 10: Which brand has the highest potential revenue (price multiplied by stock) for Small (S) size t-shirts?
-- Status: Tested & wrong answer
SELECT `brand`, (price * stock_quantity) AS `potential_revenue` FROM atliq_tshirts.t_shirts 
WHERE `size` = 'S' ORDER BY `potential_revenue` DESC LIMIT 1; -- Wrong answer from LLM

SELECT brand, SUM(price * stock_quantity) as potential_revenue FROM atliq_tshirts.t_shirts
WHERE size = 'S' GROUP BY brand ORDER BY potential_revenue DESC LIMIT 1; -- Correct answer for question 10

-- Question 11: Compare the average price of Nike t-shirts versus Adidas t-shirts. Which one is more expensive on average?
-- Status: Tested & Passed
SELECT brand, AVG(price) as average_price
FROM atliq_tshirts.t_shirts
WHERE brand IN ('Nike', 'Adidas')
GROUP BY brand; 

-- Question 12: Tìm áo cỡ đại
-- Status: Tested & Passed
SELECT `t_shirt_id`, `brand`, `color`, `size`, `price` FROM atliq_tshirts.t_shirts WHERE `size` = 'XL' LIMIT 5; -- Result from LLM

SELECT * FROM atliq_tshirts.t_shirts WHERE size = 'XL'; -- Full expected answer from LLM 

-- Question 13: Tổng giá trị kho của Nike
-- Status: Tested & Passed
SELECT SUM(price * stock_quantity) FROM atliq_tshirts.t_shirts WHERE brand = 'Nike';

-- Question 14: Áo màu đen
-- Status: Tested & Passed
SELECT `brand`, `size`, `price`, `stock_quantity` FROM atliq_tshirts.t_shirts WHERE color = 'Black' LIMIT 5; -- Result from LLM

SELECT * FROM atliq_tshirts.t_shirts WHERE color = 'Black'; -- Full expected answer from LLM 

-- Question 15: Liệt kê tất cả áo màu đen, không giới hạn số lượng dòng trả về
-- Status: Tested & Passed
SELECT `t_shirt_id`, `brand`, `color`, `size`, `price`, `stock_quantity` FROM atliq_tshirts.t_shirts WHERE `color` = 'Black';


