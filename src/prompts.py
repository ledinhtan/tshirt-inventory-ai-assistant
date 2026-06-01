# src/prompts.py

FEW_SHOTS = [
    {
        "Question": "How much is the inventory cost for all small-sized t-shirts?",
        "SQLQuery": "SELECT SUM(`price` * `stock_quantity`) FROM `t_shirts` WHERE `size` = 'S'",
        "SQLResult": "[(19919,)]",
        "Answer": "The total inventory cost for all small-sized (S) t-shirts is 19,919."
    },
    {
        "Question": "How many white Levi's t-shirts do we have available?",
        "SQLQuery": "SELECT SUM(`stock_quantity`) FROM `t_shirts` WHERE `brand` = 'Levi' AND `color` = 'White'",
        "SQLResult": "[(281,)]",
        "Answer": "We currently have 281 white Levi's t-shirts available in stock."
    },
    {
        "Question": "List all brands that have more than 500 total items in stock, but only considering White and Blue colours",
        "SQLQuery": "SELECT `brand`, SUM(`stock_quantity`) FROM `t_shirts` WHERE `color` IN ('White', 'Blue') GROUP BY `brand` HAVING SUM(`stock_quantity`) > 500",
        "SQLResult": "[('Nike', 711)]",
        "Answer": "When considering only White and Blue colours, Nike is the only brand with more than 500 items in stock, totaling 711 units."
    },
    {
        "Question": "Find all colours that are not available in the Adidas brand.",
        "SQLQuery": "SELECT DISTINCT `color` FROM `t_shirts` WHERE `color` NOT IN (SELECT `color` FROM `t_shirts` WHERE `brand` = 'Adidas')",
        "SQLResult": "[]",
        "Answer": "All available colours in the inventory are also offered by Adidas, so there are no colours exclusive to other brands."
    },
    {
        "Question": "Which brand has the highest potential revenue (price multiplied by stock) for Small (S) size t-shirts?",
        "SQLQuery": "SELECT `brand`, SUM(`price` * `stock_quantity`) AS `potential_revenue` FROM `t_shirts` WHERE `size` = 'S' GROUP BY `brand` ORDER BY `potential_revenue` DESC LIMIT 1",
        "SQLResult": "[('Adidas', 9057)]",
        "Answer": "Adidas has the highest potential revenue for Small (S) size t-shirts, with a total value of 9,057."
    },
    {
        "Question": "Tìm áo cỡ đại",
        "SQLQuery": "SELECT `brand`, `color`, `size`, `price`, `stock_quantity` FROM `t_shirts` WHERE `size` = 'XL'",
        "SQLResult": "[('Adidas', 'Blue', 'XL', 22, 98), ('Adidas', 'Black', 'XL', 31, 76), ('Levi', 'Red', 'XL', 20, 75), ('Adidas', 'Red', 'XL', 13, 83), ('Levi', 'Black', 'XL', 31, 21), ('Van Huesen', 'White', 'XL', 31, 64), ('Nike', 'Black', 'XL', 19, 59), ('Van Huesen', 'Black', 'XL', 31, 100), ('Nike', 'Blue', 'XL', 21, 76), ('Nike', 'Red', 'XL', 16, 88), ('Nike', 'White', 'XL', 39, 87), ('Van Huesen', 'Red', 'XL', 32, 96), ('Van Huesen', 'Blue', 'XL', 27, 38)]",
        "Answer": "Dạ, hiện tại bên mình có khá nhiều mẫu áo cỡ đại (XL) từ các thương hiệu như Adidas, Levi, Nike và Van Huesen với đa dạng màu sắc (Xanh, Đen, Đỏ, Trắng) và mức giá dao động từ 13 đến 39 ạ."
    }
]

MYSQL_PROMPT = """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to answer the user's question.
Unless the user specifies a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause. 
Use the following table schema:
{table_info}
"""

ANSWER_PROMPT = """Dựa vào câu hỏi của người dùng, câu lệnh SQL và kết quả trả về từ database dưới đây, hãy trả lời câu hỏi của người dùng một cách lịch sự.
        
    LƯU Ý QUAN TRỌNG: Trả lời bằng ĐÚNG NGÔN NGỮ mà người dùng đã hỏi.
    - Nếu khách hỏi tiếng Việt, hãy viết câu trả lời tự nhiên bằng tiếng Việt.
    - If the user asks in English, please respond in English.

    Câu hỏi: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """