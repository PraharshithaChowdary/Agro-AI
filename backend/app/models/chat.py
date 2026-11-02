from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, text
from app.database import Base, engine

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    session_id = Column(String(36), nullable=True, index=True)
    sender = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=True)
    evidence_sources_json = Column(Text, nullable=True)
    suggested_questions_json = Column(Text, nullable=True)
    calculator_data_json = Column(Text, nullable=True)
    model_provider = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

def migrate_chat_messages_table():
    """
    Non-destructive automatic migration for chat_messages table.
    Safely adds session_id, evidence_sources_json, etc. to existing SQLite databases.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(chat_messages);")).fetchall()
            existing_cols = {row[1] for row in result}

            new_columns = [
                ("session_id", "TEXT"),
                ("evidence_sources_json", "TEXT"),
                ("suggested_questions_json", "TEXT"),
                ("calculator_data_json", "TEXT"),
                ("model_provider", "VARCHAR(50)")
            ]
            for col_name, col_type in new_columns:
                if col_name not in existing_cols:
                    conn.execute(text(f"ALTER TABLE chat_messages ADD COLUMN {col_name} {col_type};"))
                    conn.commit()
    except Exception as e:
        pass

# Run automatic migration on import
migrate_chat_messages_table()
