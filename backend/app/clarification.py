from typing import Optional


AMBIGUOUS_PATTERNS = [
    "show me the orders",
    "show orders",
    "orders",

    "show me customers",
    "show me the customers",
    "show customers",
    "customers",

    "show me products",
    "show me the products",
    "show products",
    "products",
]


CLARIFICATION_OPTIONS = {
    "orders": [
        {
            "id": 1,
            "label": "Total number of orders",
            "description": "Count all orders",
            "sql": """
SELECT COUNT(*) AS total_orders
FROM orders;
"""
        },
        {
            "id": 2,
            "label": "Total order amount",
            "description": "Calculate total sales from orders",
            "sql": """
SELECT SUM(total_amount) AS total_sales
FROM orders;
"""
        },
        {
            "id": 3,
            "label": "Orders by customer",
            "description": "Show orders grouped by customer",
            "sql": """
SELECT
    c.id,
    c.name,
    COUNT(o.id) AS total_orders
FROM customers c
JOIN orders o
    ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total_orders DESC;
"""
        },
        {
            "id": 4,
            "label": "Orders by product",
            "description": "Show orders grouped by product",
            "sql": """
SELECT
    p.id,
    p.name,
    SUM(oi.quantity) AS total_quantity
FROM products p
JOIN order_items oi
    ON p.id = oi.product_id
GROUP BY p.id, p.name
ORDER BY total_quantity DESC;
"""
        },
        {
            "id": 5,
            "label": "Complete order details",
            "description": "Show detailed order information",
            "sql": """
SELECT
    o.id,
    c.name AS customer_name,
    o.order_date,
    o.status,
    o.total_amount
FROM orders o
JOIN customers c
    ON o.customer_id = c.id
ORDER BY o.order_date DESC;
"""
        }
    ],

    "customers": [
        {
            "id": 1,
            "label": "Show all customers",
            "description": "Display customer information",
            "sql": """
SELECT *
FROM customers;
"""
        },
        {
            "id": 2,
            "label": "Customers by city",
            "description": "Group customers by city",
            "sql": """
SELECT
    city,
    COUNT(*) AS total_customers
FROM customers
GROUP BY city
ORDER BY total_customers DESC;
"""
        },
        {
            "id": 3,
            "label": "Customer order count",
            "description": "Show how many orders each customer made",
            "sql": """
SELECT
    c.id,
    c.name,
    COUNT(o.id) AS total_orders
FROM customers c
LEFT JOIN orders o
    ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total_orders DESC;
"""
        },
        {
            "id": 4,
            "label": "Customer total spending",
            "description": "Show total amount spent by each customer",
            "sql": """
SELECT
    c.id,
    c.name,
    COALESCE(SUM(o.total_amount), 0) AS total_spending
FROM customers c
LEFT JOIN orders o
    ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total_spending DESC;
"""
        }
    ],

    "products": [
        {
            "id": 1,
            "label": "Show all products",
            "description": "Display all products",
            "sql": """
SELECT *
FROM products;
"""
        },
        {
            "id": 2,
            "label": "Products by category",
            "description": "Group products by category",
            "sql": """
SELECT
    category,
    COUNT(*) AS total_products
FROM products
GROUP BY category
ORDER BY total_products DESC;
"""
        },
        {
            "id": 3,
            "label": "Most expensive products",
            "description": "Show products with highest prices",
            "sql": """
SELECT
    id,
    name,
    category,
    price
FROM products
ORDER BY price DESC
LIMIT 10;
"""
        },
        {
            "id": 4,
            "label": "Products with low stock",
            "description": "Show products with low inventory",
            "sql": """
SELECT
    id,
    name,
    category,
    stock
FROM products
WHERE stock < 20
ORDER BY stock ASC;
"""
        }
    ]
}


def detect_clarification(question: str) -> Optional[dict]:

    normalized_question = question.strip().lower()

    if normalized_question not in AMBIGUOUS_PATTERNS:
        return None

    if "order" in normalized_question:

        return {
            "needs_clarification": True,
            "type": "orders",
            "question": "What would you like to know about the orders?",
            "options": CLARIFICATION_OPTIONS["orders"]
        }

    if "customer" in normalized_question:

        return {
            "needs_clarification": True,
            "type": "customers",
            "question": "What would you like to know about the customers?",
            "options": CLARIFICATION_OPTIONS["customers"]
        }

    if "product" in normalized_question:

        return {
            "needs_clarification": True,
            "type": "products",
            "question": "What would you like to know about the products?",
            "options": CLARIFICATION_OPTIONS["products"]
        }

    return None


def get_clarification_sql(
    clarification_type: str,
    option_id: int
) -> Optional[str]:

    options = CLARIFICATION_OPTIONS.get(clarification_type)

    if not options:
        return None

    for option in options:

        if option["id"] == option_id:
            return option["sql"].strip()

    return None