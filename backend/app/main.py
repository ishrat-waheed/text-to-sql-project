
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from . import models
from .routes import router


print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully!")


app = FastAPI(
    title="Text-to-SQL API",
    description="Natural Language to SQL Query System",
    version="1.0.0"
)


# CORS configuration
# Allows the React frontend to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Text-to-SQL API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(router)



    