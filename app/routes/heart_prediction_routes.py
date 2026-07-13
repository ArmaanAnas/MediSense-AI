from flask import (
    Blueprint,
    render_template,
    request
)

import joblib

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db
from app.models.prediction_history import PredictionHistory

heart_prediction = Blueprint(
    "heart_prediction",
    __name__
)

model = joblib.load(
    "trained_models/heart_disease_model.pkl"
)

@heart_prediction.route(
    "/heart-disease-prediction",
    methods=["GET", "POST"]
)
@login_required
def predict_heart_disease():

    result = None
    insight = None

    if request.method == "POST":

        features = [[
            int(request.form["age"]),
            int(request.form["sex"]),
            int(request.form["cp"]),
            int(request.form["trestbps"]),
            int(request.form["chol"]),
            int(request.form["fbs"]),
            int(request.form["restecg"]),
            int(request.form["thalach"]),
            int(request.form["exang"]),
            float(request.form["oldpeak"]),
            int(request.form["slope"]),
            int(request.form["ca"]),
            int(request.form["thal"])
        ]]

        prediction_result = model.predict(
            features
        )[0]

        if prediction_result == 1:

            result = "High Risk"

            insight = (
                "Your cardiovascular indicators suggest "
                "an elevated risk of heart disease. "
                "Consider consulting a healthcare professional."
            )

        else:

            result = "Low Risk"

            insight = (
                "Your heart health indicators appear normal. "
                "Maintain a healthy diet and regular exercise."
            )

        history = PredictionHistory(
            user_id=current_user.id,
            prediction_type="Heart Disease",
            result=result
        )

        db.session.add(history)
        db.session.commit()

    return render_template(
        "prediction/heart_prediction.html",
        result=result,
        insight=insight
    )