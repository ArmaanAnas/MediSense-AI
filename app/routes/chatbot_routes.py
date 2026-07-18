from flask import (
    Blueprint,
    render_template,
    request
)

from flask_login import login_required

import google.generativeai as genai
from config import Config


chatbot = Blueprint(
    "chatbot",
    __name__
)

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel("gemini-2.0-flash")

@chatbot.route(
    "/health-chatbot",
    methods=["GET", "POST"]
)
@login_required
def health_chatbot():

    response = None

    if request.method == "POST":

        user_question = request.form.get(
            "question"
        )

        try:

            prompt = f"""
You are MediSense AI Health Assistant.

Rules:
- Provide health information only.
- Give concise and easy-to-understand answers.
- Never claim to be a doctor.
- Recommend consulting healthcare professionals when necessary.
- Do not provide dangerous medical advice.

User Question:
{user_question}
"""

            result = model.generate_content(
                prompt
            )

            response = result.text

        except Exception as e:

            response = (
                f"Error: {str(e)}"
            )

    return render_template(
        "chatbot/chatbot.html",
        response=response
    )