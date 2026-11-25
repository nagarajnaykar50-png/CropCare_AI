from datetime import datetime, timezone

from core.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class Crop(db.Model):

    __tablename__ = "crops"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    crop_name = db.Column(
        db.String(100),
        nullable=False
    )

    variety = db.Column(
        db.String(100)
    )

    location = db.Column(
        db.String(200)
    )

    planting_date = db.Column(
        db.String(30)
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now
    )

    detections = db.relationship(
        "DiseaseDetection",
        backref="crop",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "crop_name": self.crop_name,
            "variety": self.variety,
            "location": self.location,
            "planting_date": self.planting_date,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at else None
            )
        }


class DiseaseDetection(db.Model):

    __tablename__ = "disease_detections"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    crop_id = db.Column(
        db.Integer,
        db.ForeignKey("crops.id"),
        nullable=False
    )

    image_filename = db.Column(
        db.String(255),
        nullable=False
    )

    disease_name = db.Column(
        db.String(150),
        nullable=False
    )

    severity = db.Column(
        db.String(50)
    )

    confidence = db.Column(
        db.Float
    )

    prediction_mode = db.Column(
        db.String(30),
        default="mock"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now
    )

    def to_dict(self):

        return {
            "id": self.id,
            "crop_id": self.crop_id,
            "image_filename": self.image_filename,
            "disease_name": self.disease_name,
            "severity": self.severity,
            "confidence": self.confidence,
            "prediction_mode": self.prediction_mode,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at else None
            )
        }