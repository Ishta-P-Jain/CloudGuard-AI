import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class AIExplanation(Base):
    __tablename__ = "ai_explanations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    finding_id = Column(String, ForeignKey("findings.id", ondelete="CASCADE"), nullable=False, unique=True)
    explanation = Column(Text, nullable=False)
    danger = Column(Text, nullable=False)
    real_world_impact = Column(Text, nullable=False)
    remediation_steps = Column(JSON, nullable=False)  # Saved as list/array of strings in JSON format
    estimated_effort = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Establish relationship to finding
    finding = relationship("Finding", back_populates="ai_explanation")
