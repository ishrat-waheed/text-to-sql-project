from app.clarification import (
    detect_clarification,
    get_clarification_sql
)


question = "Show me the orders"

result = detect_clarification(question)


print("=" * 60)
print("Question:", question)
print("=" * 60)


if result:

    print("⚠️ Clarification required:")
    print(result["question"])

    for option in result["options"]:

        print(
            f'{option["id"]}. '
            f'{option["label"]} - '
            f'{option["description"]}'
        )


# Simulate user selecting option 2
selected_option = 2

sql = get_clarification_sql(
    result["type"],
    selected_option
)


print("\n" + "=" * 60)
print("Selected Option:", selected_option)
print("=" * 60)

print("Generated SQL:")
print(sql)