from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any

from ..core.extensions import db


class CaseStatus(enum.StrEnum):
    UPLOADED = "uploaded"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    FAILED = "failed"


class AccidentCase(db.Model):
    __tablename__ = "accident_cases"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    image_path = db.Column(db.String(255))
    image_hash = db.Column(db.String(64), index=True)
    annotated_image = db.Column(db.String(255))
    video_path = db.Column(db.String(255))

    status = db.Column(db.Enum(CaseStatus), default=CaseStatus.UPLOADED, nullable=False)

    user_role = db.Column(db.String(50))
    vehicle_type = db.Column(db.String(50))
    vehicle_color = db.Column(db.String(50))
    damage_location = db.Column(db.String(100))
    damage_details = db.Column(db.Text)
    witness_observation = db.Column(db.Text)
    expert_notes = db.Column(db.Text)
    number_of_vehicles = db.Column(db.String(20))
    saw_collision = db.Column(db.Boolean)

    gemini_raw_json = db.Column(db.JSON)
    analysis_result = db.Column(db.Text)
    cross_analysis_result = db.Column(db.Text)
    detection_summary = db.Column(db.Text)

    embedding = db.Column(db.LargeBinary)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    analyzed_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="cases")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_path": self.image_path,
            "image_hash": self.image_hash,
            "annotated_image": self.annotated_image,
            "video_path": self.video_path,
            "status": self.status.value if self.status else None,
            "user_role": self.user_role,
            "vehicle_type": self.vehicle_type,
            "vehicle_color": self.vehicle_color,
            "damage_location": self.damage_location,
            "damage_details": self.damage_details,
            "witness_observation": self.witness_observation,
            "expert_notes": self.expert_notes,
            "number_of_vehicles": self.number_of_vehicles,
            "saw_collision": self.saw_collision,
            "gemini_raw_json": self.gemini_raw_json,
            "analysis_result": self.analysis_result,
            "cross_analysis_result": self.cross_analysis_result,
            "detection_summary": self.detection_summary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
        }

