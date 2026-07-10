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
        else:
            result = "Not Diabetic"

    return render_template(
        "prediction/diabetes_prediction.html",
        result=result
    )