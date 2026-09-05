from app.llm import generate_sql


question = "Show me all customers from Karachi"

sql = generate_sql(question)

print("\nGenerated SQL:")
print(sql)