# 🤖 Text-to-SQL Project

An AI-powered **Text-to-SQL system** that converts natural language questions into SQL queries and retrieves results from a PostgreSQL database.

## ✨ Features

* 🗣️ Natural language to SQL
* 🤖 LLM-powered SQL generation
* 🔍 SQL query validation
* 🗄️ PostgreSQL database
* ⚡ FastAPI backend
* 🌱 Sample database seed data
* 📚 Swagger API documentation

## 🏗️ Project Structure

```text
text-to-sql-project/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── llm.py
│   │   ├── validator.py
│   │   └── routes.py
│   │
│   ├── seed.py
│   └── requirements.txt
│
├── frontend/
├── evaluation/
├── README.md
└── .gitignore
```

## 🔄 How It Works

```text
User Question
      ↓
     LLM
      ↓
Generated SQL
      ↓
SQL Validator
      ↓
PostgreSQL
      ↓
    Result
```

## 💬 Example

**Question:**

```text
Show the top 5 customers by number of orders.
```

**Generated SQL:**

```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC
LIMIT 5;
```

## 🚀 Setup

```bash
git clone https://github.com/ishrat-waheed/text-to-sql-project.git
cd text-to-sql-project/backend
pip install -r requirements.txt
```

Create a `.env` file with your database URL and API key.

Run the backend:

```bash
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🛠️ Tech Stack

**Python • FastAPI • PostgreSQL • SQLAlchemy • Pydantic • LLM • Uvicorn**

## 👨‍💻 Author

**Ishrat Ul Abad**
BS Data Science — QUEST Nawabshah, Pakistan.

---

⭐ If you find this project useful, consider giving it a star.


