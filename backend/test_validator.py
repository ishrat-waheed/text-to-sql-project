from app.validator import validate_sql


# Safe query
safe_sql = "SELECT * FROM customers WHERE city = 'Karachi';"

is_valid, message = validate_sql(safe_sql)

print("Safe Query Test:")
print("Valid:", is_valid)
print("Message:", message)


# Dangerous query
dangerous_sql = "DROP TABLE customers;"

is_valid, message = validate_sql(dangerous_sql)

print("\nDangerous Query Test:")
print("Valid:", is_valid)
print("Message:", message)