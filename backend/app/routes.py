from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from .database import SessionLocal
from .llm import generate_sql
from .validator import validate_sql
from .clarification import (
    detect_clarification,
    get_clarification_sql
)


router = APIRouter()


# ============================================================
# NORMAL TEXT-TO-SQL
# ============================================================

@router.post("/query")
def text_to_sql(question: str):

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Generate SQL using Groq
    try:
        sql = generate_sql(question)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error: {str(e)}"
        )

    # Validate SQL
    is_valid, message = validate_sql(sql)

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=message
        )

    # Execute SQL
    db = SessionLocal()

    try:

        result = db.execute(text(sql))

        columns = list(result.keys())

        rows = [
            dict(row._mapping)
            for row in result.fetchall()
        ]

        return {
            "question": question,
            "sql": sql,
            "columns": columns,
            "results": rows,
            "row_count": len(rows)
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=f"Database error: {str(e)}"
        )

    finally:
        db.close()


# ============================================================
# CLARIFICATION DETECTION
# ============================================================

@router.post("/clarify")
def clarify_question(question: str):

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    clarification = detect_clarification(question)

    # Question is clear
    if clarification is None:

        return {
            "needs_clarification": False,
            "message": "Question is clear. Use /query to generate SQL."
        }

    # Question is ambiguous
    return clarification


# ============================================================
# EXECUTE CLARIFICATION OPTION
# ============================================================

@router.post("/clarify/execute")
def execute_clarification(
    clarification_type: str,
    option_id: int
):

    # Get SQL for selected option
    sql = get_clarification_sql(
        clarification_type,
        option_id
    )

    if sql is None:

        raise HTTPException(
            status_code=400,
            detail="Invalid clarification type or option."
        )

    # Validate SQL
    is_valid, message = validate_sql(sql)

    if not is_valid:

        raise HTTPException(
            status_code=400,
            detail=message
        )

    # Execute SQL
    db = SessionLocal()

    try:

        result = db.execute(text(sql))

        columns = list(result.keys())

        rows = [
            dict(row._mapping)
            for row in result.fetchall()
        ]

        return {
            "clarification_type": clarification_type,
            "option_id": option_id,
            "sql": sql,
            "columns": columns,
            "results": rows,
            "row_count": len(rows)
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=f"Database error: {str(e)}"
        )

    finally:

        db.close()