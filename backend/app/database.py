from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables only in development
if os.getenv("ENVIRONMENT") != "production":
    load_dotenv()

# Get database URL with fallback for local development
DATABASE_URL = os.getenv("DATABASE_URL")

# Handle Render PostgreSQL connection requirements
if DATABASE_URL.startswith("postgresql://"):
    # Replace 'postgresql://' with 'postgresql+psycopg2://' for SQLAlchemy
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    # Add SSL requirement for production
    if os.getenv("ENVIRONMENT") == "production":
        DATABASE_URL += "?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Check connections before using them
    connect_args={
        "keepalives": 1,  # Maintain connection to Render PostgreSQL
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "sslmode": "require" if os.getenv("ENVIRONMENT") == "production" else "prefer"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()