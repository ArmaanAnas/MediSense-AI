from flask import (
    Blueprint,
    send_file
)

from flask_login import (
    login_required,
    current_user
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from app.models.health_profile import HealthProfile
from app.models.prediction_history import PredictionHistory

import os


report = Blueprint(
    "report",
    __name__
)


@report.route("/download-report")
@login_required
def download_report():

    profile = HealthProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    if not profile:
        return "Health profile not found."

    diabetes_count = PredictionHistory.query.filter_by(
        user_id=current_user.id,
        prediction_type="Diabetes"
    ).count()

    heart_count = PredictionHistory.query.filter_by(
        user_id=current_user.id,
        prediction_type="Heart Disease"
    ).count()

    bmi = round(
        profile.weight /
        ((profile.height / 100) ** 2),
        2
    )

    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(
        os.getcwd(),
        "reports"
    )

    os.makedirs(
        reports_dir,
        exist_ok=True
    )

    filename = os.path.join(
        reports_dir,
        f"health_report_{current_user.id}.pdf"
    )

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "MediSense AI Health Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"Name: {current_user.name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Age: {profile.age}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Gender: {profile.gender}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Height: {profile.height} cm",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Weight: {profile.weight} kg",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"BMI: {bmi}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Blood Pressure: {profile.blood_pressure}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Blood Sugar: {profile.blood_sugar}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Cholesterol: {profile.cholesterol}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Smoking Status: {profile.smoking_status}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Exercise Frequency: {profile.exercise_frequency}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Family History: {profile.family_history}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"Diabetes Predictions: {diabetes_count}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Heart Disease Predictions: {heart_count}",
            styles["Normal"]
        )
    )

    pdf.build(content)

    return send_file(
        filename,
        as_attachment=True,
        download_name="MediSense_Health_Report.pdf"
    )