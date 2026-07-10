from flask import (
    Blueprint,
    render_template,
    request
)

import joblib

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
def diabetes_prediction():

    result = None

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

    return render_template(
    "prediction/diabetes_prediction.html",
    result=result,
    insight=insight if result else None
)