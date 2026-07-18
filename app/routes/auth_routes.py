from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.models.health_profile import HealthProfile
from app.models.prediction_history import PredictionHistory
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.extensions import db, bcrypt
from flask_login import login_user, logout_user, login_required
from app.models import User

auth = Blueprint(
    "auth",
    __name__
)

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash("Email already exists")
            return redirect(url_for("auth.register"))

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        new_user = User(
            name=name,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user and bcrypt.check_password_hash(
            user.password_hash,
            password
        ):

            login_user(user)

            return redirect(
                url_for("auth.dashboard")
            )

        flash("Invalid email or password")

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/login.html"
    )

@auth.route("/dashboard")
@login_required
def dashboard():

    profile = HealthProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    if not profile:
        return redirect(
            url_for("auth.health_profile")
        )

    bmi = round(
        profile.weight /
        ((profile.height / 100) ** 2),
        2
    )

    if bmi < 18.5:
        health_status = "Underweight"

    elif bmi < 25:
        health_status = "Healthy"

    elif bmi < 30:
        health_status = "Overweight"

    else:
        health_status = "Obese"

    risk_score = 0

    if bmi > 25:
        risk_score += 2

    if profile.blood_sugar > 140:
        risk_score += 3

    if profile.cholesterol > 200:
        risk_score += 2

    if profile.smoking_status.lower() == "yes":
        risk_score += 2

    if profile.family_history.lower() != "none":
        risk_score += 1

    if risk_score <= 2:
        risk_level = "Low Risk"

    elif risk_score <= 5:
        risk_level = "Medium Risk"

    else:
        risk_level = "High Risk"

    diabetes_count = PredictionHistory.query.filter_by(
        user_id=current_user.id,
        prediction_type="Diabetes"
    ).count()

    heart_count = PredictionHistory.query.filter_by(
        user_id=current_user.id,
        prediction_type="Heart Disease"
    ).count()

    return render_template(
        "dashboard/dashboard.html",
        profile=profile,
        bmi=bmi,
        health_status=health_status,
        risk_score=risk_score,
        risk_level=risk_level,
        user=current_user,
        diabetes_count=diabetes_count,
        heart_count=heart_count
    )
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("main.home")
    )


@auth.route("/health-profile", methods=["GET", "POST"])
@login_required
def health_profile():

    if request.method == "POST":

        profile = HealthProfile(
            user_id=current_user.id,
            age=request.form.get("age"),
            gender=request.form.get("gender"),
            height=request.form.get("height"),
            weight=request.form.get("weight"),
            blood_pressure=request.form.get("blood_pressure"),
            blood_sugar=request.form.get("blood_sugar"),
            cholesterol=request.form.get("cholesterol"),
            smoking_status=request.form.get("smoking_status"),
            exercise_frequency=request.form.get("exercise_frequency"),
            family_history=request.form.get("family_history")
        )

        db.session.add(profile)
        db.session.commit()

        flash("Health Profile Saved Successfully")

        return redirect(
            url_for("auth.dashboard")
        )

    return render_template(
        "health/health_profile.html"
    )