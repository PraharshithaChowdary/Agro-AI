from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Index
from app.database import Base


class PlantAnalysisHistory(Base):
    __tablename__ = "plant_analysis_history"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    analysis_type = Column(String(30), nullable=False)  # identification or health
    image_filename = Column(String(255), nullable=True)
    plant_name = Column(String(180), nullable=True)
    organ = Column(String(40), nullable=True)
    result_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        import json
        try:
            result = json.loads(self.result_json)
        except (TypeError, ValueError):
            result = {}
        return {
            "id": self.id,
            "type": self.analysis_type,
            "imageFilename": self.image_filename,
            "plantName": self.plant_name,
            "organ": self.organ,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "result": result,
        }
