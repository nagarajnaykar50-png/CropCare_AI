from datetime import datetime, timezone

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from core.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now
    )

    crops = db.relationship(
        "Crop",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )

    def to_dict(self):

        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at else None
            )
        }