from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, Boolean, inspect, text
from app.database import Base, engine

class ProductionAnalysis(Base):
    __tablename__ = "production_analyses"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    analysis_type = Column(String(20), nullable=False)  # 'crop' or 'soil'
    image_filename = Column(String(255), nullable=True)
    is_agricultural = Column(Boolean, default=True, nullable=False)
    predicted_class = Column(String(100), nullable=False)
    sub_category = Column(String(100), nullable=True)  # e.g., disease name or soil subcategory
    confidence = Column(Float, nullable=False)
    severity_level = Column(String(50), nullable=True)
    explanation = Column(Text, nullable=True)
    recommendations_json = Column(Text, nullable=True)
    prevention_tips_json = Column(Text, nullable=True)
    input_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_history_dict(self):
        import json
        try:
            saved_inputs = json.loads(self.input_json) if self.input_json else {}
        except (TypeError, ValueError):
            saved_inputs = {}
        return {
            "id": self.id,
            "type": self.analysis_type,
            "predictedClass": f"{self.predicted_class} ({self.sub_category})" if self.sub_category else self.predicted_class,
            "confidence": self.confidence,
            "date": self.created_at.strftime("%b %d, %Y - %H:%M"),
            "status": "valid" if self.is_agricultural else "invalid_image",
            "inputs": saved_inputs,
        }


def auto_migrate_production_columns():
    """Add optional input metadata to existing SQLite installations without dropping data."""
    try:
        inspector = inspect(engine)
        if "production_analyses" not in inspector.get_table_names():
            return
        existing = {col["name"] for col in inspector.get_columns("production_analyses")}
        if "input_json" not in existing:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE production_analyses ADD COLUMN input_json TEXT"))
    except Exception as exc:
        # Keep application import resilient; actual persistence errors are surfaced at request time.
        print(f"[WARN] Production history schema migration skipped: {exc}")


auto_migrate_production_columns()
