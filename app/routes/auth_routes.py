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

    return """
    <h1>Welcome to MediSense AI Dashboard</h1>
    <a href='/logout'>Logout</a>
    """
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("main.home")
    )
    return redirect(
    url_for("main.home")
)