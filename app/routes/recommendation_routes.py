from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)

from app.models.health_profile import HealthProfile
from app.models.prediction_history import PredictionHistory

recommendation = Blueprint(
    "recommendation",
    __name__
)


@recommendation.route("/recommendations")
@login_required
def recommendations():

    profile = HealthProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    recommendations = []

    health_score = 100

    if profile:

        bmi = round(
            profile.weight /
            ((profile.height / 100) ** 2),
            2
        )

        if bmi > 25:

            recommendations.append(
                "Maintain BMI below 25 through regular exercise and healthy eating."
            )

            health_score -= 10

        if profile.blood_sugar > 140:

            recommendations.append(
                "Reduce sugar intake and monitor blood glucose regularly."
            )

            health_score -= 15

        if profile.cholesterol > 200:

            recommendations.append(
                "Avoid oily foods and increase fiber-rich foods."
            )

            health_score -= 10

        if profile.smoking_status.lower() == "yes":

            recommendations.append(
                "Quit smoking to significantly reduce cardiovascular risk."
            )

            health_score -= 20

    latest_diabetes = PredictionHistory.query.filter_by(
        user_id=current_user.id,
        prediction_type="Diabetes"
    ).order_by(
        PredictionHistory.created_at.desc()
    ).first()

    if latest_diabetes:

        if latest_diabetes.result == "Diabetic":

            recommendations.append(
                "Diabetes risk detected. Monitor blood sugar levels regularly."
            )

            recommendations.append(
                "Avoid soft drinks, sweets and processed foods."
            )

            recommendations.append(
                "Perform at least 30 minutes of physical activity daily."
            )

            health_score -= 15

    latest_heart = PredictionHistory.query.filter_by(
        user_id=current_user.id,
        prediction_type="Heart Disease"
    ).order_by(
        PredictionHistory.created_at.desc()
    ).first()

    if latest_heart:

        if latest_heart.result == "High Risk":

            recommendations.append(
                "Heart disease risk detected. Monitor blood pressure weekly."
            )

            recommendations.append(
                "Reduce sodium and saturated fat intake."
            )

            recommendations.append(
                "Consult a healthcare professional for cardiovascular assessment."
            )

            health_score -= 15

    recommendations.append(
        "Drink at least 3 liters of water daily."
    )

    recommendations.append(
        "Sleep 7-8 hours every night."
    )

    recommendations.append(
        "Walk for 30 minutes every day."
    )

    if health_score < 0:
        health_score = 0

    return render_template(
        "recommendation/recommendations.html",
        recommendations=recommendations,
        health_score=health_score
    )