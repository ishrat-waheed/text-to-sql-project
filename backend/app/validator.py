import re


# Dangerous SQL commands that we never allow
FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
]


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Validate an SQL query before executing it.

    Returns:
        (True, "") if the query is safe.
        (False, reason) if the query is unsafe.
    """

    if not sql:
        return False, "SQL query is empty."

    # Remove markdown code fences if the LLM adds them
    sql = sql.strip()

    sql = re.sub(r"^```sql\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```\s*", "", sql)
    sql = re.sub(r"\s*```$", "", sql)

    sql = sql.strip()

    # Only SELECT queries are allowed
    if not sql.upper().startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    # Check dangerous keywords
    for keyword in FORBIDDEN_KEYWORDS:
        pattern = rf"\b{keyword}\b"

        if re.search(pattern, sql, re.IGNORECASE):
            return False, f"Forbidden SQL keyword detected: {keyword}"

    return True, ""