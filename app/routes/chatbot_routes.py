from flask import (
    Blueprint,
    render_template,
    request
)

from flask_login import login_required

chatbot = Blueprint(
    "chatbot",
    __name__
)


@chatbot.route(
    "/health-chatbot",
    methods=["GET", "POST"]
)
@login_required
def health_chatbot():

    response = None

    if request.method == "POST":

        user_message = request.form.get(
            "message"
        ).lower()

        if "diabetes" in user_message:

            response = (
                "Type 2 diabetes can often be managed "
                "through exercise, healthy diet and "
                "medical guidance."
            )

        elif "blood pressure" in user_message:

            response = (
                "A normal blood pressure is around "
                "120/80 mmHg."
            )

        elif "cholesterol" in user_message:

            response = (
                "Maintaining healthy cholesterol "
                "levels reduces heart disease risk."
            )

        elif "exercise" in user_message:

            response = (
                "At least 30 minutes of exercise "
                "daily is recommended."
            )

        else:

            response = (
                "Please consult a healthcare "
                "professional for personalized advice."
            )

    return render_template(
        "chatbot/chatbot.html",
        response=response
    )