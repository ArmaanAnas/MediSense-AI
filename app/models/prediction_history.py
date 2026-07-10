from app.extensions import db
from datetime import datetime


class PredictionHistory(db.Model):
    __tablename__ = "prediction_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    prediction_type = db.Column(
        db.String(50),
        nullable=False
    )

    result = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )