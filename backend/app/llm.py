import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env")

client = Groq(api_key=GROQ_API_KEY)


def generate_sql(question: str) -> str:

    prompt = f"""
You are an expert PostgreSQL SQL generator.

Convert the user's natural language question into a PostgreSQL SQL query.

Database tables:

customers:
- id
- name
- email
- city
- created_at

products:
- id
- name
- category
- price
- stock

orders:
- id
- customer_id
- order_date
- status
- total_amount

order_items:
- id
- order_id
- product_id
- quantity
- unit_price

payments:
- id
- order_id
- payment_date
- amount
- payment_method
- status

Rules:
1. Generate only SQL.
2. Do not use markdown.
3. Do not explain the SQL.
4. Use PostgreSQL syntax.
5. Only generate SELECT queries.
6. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE.
7. Use correct table relationships.

User question:
{question}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    return sql