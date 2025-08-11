from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
from email_validator import validate_email, EmailNotValidError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            flash("Logged in!", "success")
            return redirect(url_for("main.dashboard"))
        flash("Invalid email or password", "error")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        try:
            validate_email(email)
        except EmailNotValidError as e:
            flash(str(e), "error")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "error")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters", "error")
            return render_template("register.html")

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("auth.login"))
