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

from app.models.prediction_history import (
    PredictionHistory
)

prediction = Blueprint(
    "prediction",
    __name__
)

model = joblib.load(
    "trained_models/diabetes_model.pkl"
)


@prediction.route(
    "/diabetes-prediction",
    methods=["GET", "POST"]
)
@login_required
def diabetes_prediction():

    result = None
    insight = None

    if request.method == "POST":

        features = [[
            int(request.form["pregnancies"]),
            float(request.form["glucose"]),
            float(request.form["blood_pressure"]),
            float(request.form["skin_thickness"]),
            float(request.form["insulin"]),
            float(request.form["bmi"]),
            float(request.form["dpf"]),
            int(request.form["age"])
        ]]

        prediction_result = model.predict(
            features
        )[0]

        if prediction_result == 1:

            result = "Diabetic"

            insight = (
                "Your health indicators suggest a higher risk "
                "of diabetes. Consider consulting a healthcare "
                "professional and maintaining a healthy lifestyle."
            )

        else:

            result = "Not Diabetic"

            insight = (
                "Your health indicators appear normal. "
                "Continue maintaining a balanced diet and "
                "regular exercise routine."
            )

        history = PredictionHistory(
            user_id=current_user.id,
            prediction_type="Diabetes",
            result=result
        )

        db.session.add(history)
        db.session.commit()

    return render_template(
        "prediction/diabetes_prediction.html",
        result=result,
        insight=insight
    )


@prediction.route("/prediction-history")
@login_required
def prediction_history():

    history = PredictionHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(
        PredictionHistory.created_at.desc()
    ).all()

    return render_template(
        "prediction/history.html",
        history=history
    )