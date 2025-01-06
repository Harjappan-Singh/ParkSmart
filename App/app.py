from flask import Flask, render_template, redirect, session, url_for, flash, request, jsonify
import json
import time
from flask_dance.contrib.google import make_google_blueprint, google
import os
from functools import wraps
import my_db, pb
from dotenv import load_dotenv
import paypalrestsdk

load_dotenv()

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

db = my_db.db
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MYSQL_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production
    "client_id": os.getenv("PAY_PAL_CLIENT_ID"),
    "client_secret": os.getenv("PAY_PAL_CLIENT_SECRET")
})

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
    session["email"] = user_info.get("email")
    session["client_id"] = user_info.get("id")

    my_db.add_user_and_login(user_info.get("name"), user_info.get("id"), user_info.get("email"))

    user_uuid = session["client_id"]
    user = my_db.get_user(user_uuid)
    access = "none"
    if (user.read_access == 1 and user.write_access == 1):
        access = "grant_read_write"
    elif (user.read_access == 1):
        access = "grant_read"
    else:
        access = "none"
        
    print(access)
    token = pb.generate_token(user_info.get("id"), access)

    if token:
        my_db.update_user_token(user_info.get("id"), token)
        session["token"] = token 
        
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
    user = my_db.get_user(session["client_id"])
    if user.read_access == 1 and user.write_access == 1:
        access_level = {'access':'read_and_write'}
    elif user.read_access == 1:
        access_level = {'access': 'read'}
    else:
        access_level = {'access': 'none'}
    return render_template("dashboard.html", user_access = access_level)

@app.route("/admin_panel")
@login_required
def admin_panel():
    if session["client_id"] == os.getenv("ADMIN_CLIENT_ID"):
        users = my_db.get_all_users()
        users_list = []
        for user in users:
            users_list.append({
                'id': user.id,
                'name': user.name,
                'read_access': user.read_access,
                'write_access': user.write_access,
                'email': user.email
            })
        return render_template("admin_panel.html", users = users_list)
    else:
        return render_template("non_admin.html")

@app.route("/update_access", methods=["POST"])
@login_required
def update_access():
    if session["client_id"] == os.getenv("ADMIN_CLIENT_ID"):
        user_id = request.form.get("user_id")
        action = request.form.get("action")
        
        if action == "grant_read":
            success = my_db.update_user_access(user_id, read_access=1, write_access=0)
        elif action == "grant_read_write":
            success = my_db.update_user_access(user_id, read_access=1, write_access=1)
        elif action == "revoke_access":
            success = my_db.update_user_access(user_id, read_access=0, write_access=0)
        else:
            success = False
        
        if success:
            user_uuid = my_db.get_client_id(user_id)
            new_token = pb.refresh_token(user_uuid, action, ttl=60)
            my_db.update_user_token(user_uuid, new_token)
            session["token"] = new_token
            flash("User access updated successfully!", "success")
        else:
            flash("Failed to update user access.", "error")
        
        return redirect(url_for("admin_panel"))
    else:
        return render_template("non_admin.html")
    
@app.route("/view_past_data")
@login_required
def view_past_data():
    user_id = my_db.get_user_id(session["client_id"])
    parking_lot_data = my_db.get_parking_entries_by_user(user_id=user_id)
    parking_lot_entry_list = []
    for entry in parking_lot_data:
        parking_lot_entry_list.append({
            'parking_spot': entry.parking_spot,
            'status': entry.status,
            'timestamp': entry.timestamp,
        })
    return render_template("parking_lot_past_data.html", entries = parking_lot_entry_list)

@app.route("/save_sensor_data", methods=["POST"])
@login_required
def save_sensor_data():
    print("saving sensor data method")
    if request.method == "POST":
        sensor_data = request.json
        user_id = my_db.get_user_id(session["client_id"])
        # print(sensor_data['parkingSpot'], sensor_data['status'])
        try:        
            my_db.add_parking_status(user_id, sensor_data['parkingSpot'], sensor_data['status'])
            return jsonify({"message": "Successfully stored entry"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/subscriptions")
@login_required
def subscriptions():
    return render_template("subscription.html")

@app.route("/refresh_user_token", methods=["POST"])
def refresh_user_token():
    try:
        user_uuid = session["client_id"]
        user = my_db.get_user(user_uuid)
        access = "none"
        if (user.read_access == 1 and user.write_access == 1):
            access = "grant_read_write"
        elif (user.read_access == 1):
            access = "grant_read"
        else:
            access = "none"

        new_token = pb.refresh_token(user_uuid, access, ttl=60)

        my_db.update_user_token(user_uuid, new_token)

        session["token"] = new_token

        return jsonify({"success": True, "token": new_token}), 200
    except Exception as e:
        print(f"Error in refresh_token_endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/upgrade_subscription', methods=['POST'])
def upgrade_subscription():
    # Create a payment
    action = request.form.get("action")
    if action == "grant_read":
        amount = "15.99"
    elif action == "grant_read_write":
        amount = "24.99"
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": url_for('payment_success', action = action, _external=True),
            "cancel_url": url_for('payment_cancel', _external=True)
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Subscription Upgrade",
                    "sku": "001",
                    "price": amount,
                    "currency": "EUR",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": amount,
                "currency": "EUR"
            },
            "description": "Upgrade subscription."
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        flash("Failed to create PayPal payment. Please try again.", "error")
        return redirect(url_for("dashboard"))

@app.route('/payment_success')
def payment_success():
    user_id = my_db.get_user_id(session["client_id"])
    action = request.args.get("action")

    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        if action == "grant_read":
            success = my_db.update_user_access(user_id, read_access=1, write_access=0)
        elif action == "grant_read_write":
            success = my_db.update_user_access(user_id, read_access=1, write_access=1)
        else:
            success = False

        if success:
            refresh_user_token()
            flash("Payment successful! Your subscription has been upgraded.")
        else:
            flash("Payment successful, but failed to update subscription.", "error")
    else:
        flash("Payment failed. Please try again.", "error")

    return redirect(url_for("dashboard"))

@app.route('/payment_cancel')
def payment_cancel():
    flash("Payment canceled by user.") 
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(port = 5000, debug = True)
