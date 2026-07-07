import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

from app.models.ai_explanation import AIExplanation

class Finding(Base):
    __tablename__ = "findings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String, ForeignKey("scans.id", ondelete="CASCADE"), nullable=False)
    service = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(String, nullable=False)
    has_ai_explanation = Column(Boolean, default=False)
    evidence = Column(JSON, nullable=True)

    # Establish relationships
    scan = relationship("Scan", back_populates="findings")
    ai_explanation = relationship("AIExplanation", back_populates="finding", uselist=False, cascade="all, delete-orphan")
