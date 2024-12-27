from flask import Flask, render_template, redirect, session, url_for, flash
import json
import time
from flask_dance.contrib.google import make_google_blueprint, google
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_APP_SECRET_KEY")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to="google_login", 
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
)

app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect("/login/google")

    response = google.get("https://www.googleapis.com/oauth2/v1/userinfo")
    if not response.ok:
        print("Error response:", response.text)
        return "Error: Unable to fetch user information from Google."

    user_info = response.json()

    session["user"] = user_info.get("name")
    session["client_id"] = user_info.get("id")

    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("index"))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("not_authorized"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/not_authorized")
def not_authorized():
    return render_template("not_authorized.html"), 403

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(port = 5000, debug = True)
