from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

is_sqlite = "sqlite" in settings.DATABASE_URL.lower()

connect_args = {}
engine_kwargs = {
    "echo": False,
}

if is_sqlite:
    connect_args["check_same_thread"] = False
else:
    # Supabase PostgreSQL connection pooler resilience:
    # pool_pre_ping prevents disconnects when connection is idle
    # pool_recycle refreshes connections every 5 minutes
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_recycle"] = 300
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
