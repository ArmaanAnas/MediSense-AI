from app.extensions import db


class HealthProfile(db.Model):
    __tablename__ = "health_profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    gender = db.Column(
        db.String(20),
        nullable=False
    )

    height = db.Column(
        db.Float,
        nullable=False
    )

    weight = db.Column(
        db.Float,
        nullable=False
    )

    blood_pressure = db.Column(
        db.String(20),
        nullable=False
    )

    blood_sugar = db.Column(
        db.Float,
        nullable=False
    )

    cholesterol = db.Column(
        db.Float,
        nullable=False
    )

    smoking_status = db.Column(
        db.String(20),
        nullable=False
    )

    exercise_frequency = db.Column(
        db.String(50),
        nullable=False
    )

    family_history = db.Column(
        db.String(100),
        nullable=False
    )