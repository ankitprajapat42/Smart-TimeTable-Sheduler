import os
import datetime
import requests   # FIX 1: requests import kiya
from flask import Flask, request, render_template, redirect, url_for, flash, session  # FIX 2: session import kiya
import firebase_admin
from firebase_admin import credentials, auth, db

# ---------- CONFIG ----------
SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"   # path to downloaded JSON
DATABASE_URL = "https://time-table-schedule-d11aa-default-rtdb.firebaseio.com/"  # your DB URL
API_KEY = "AIzaSyAhyUKUnznBy9FwhU6P0FDP45v_cit_Y1o"  # FIX 3: Firebase project ka Web API Key yaha paste kare
# ----------------------------

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "replace_with_random_secret")

# Initialize Firebase Admin (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': DATABASE_URL
    })


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip().lower()
        mobile = request.form.get('mobile', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirmPassword', '')

        if not fullname or not email or not mobile or not password or not confirm:
            flash("Please fill all fields.", "danger")
            return redirect(url_for('register'))

        if password != confirm:
            flash("Password and confirm password do not match.", "danger")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters (Firebase minimum).", "danger")
            return redirect(url_for('register'))

        try:
            kwargs = {
                "email": email,
                "email_verified": False,
                "password": password,
                "display_name": fullname
            }

            if mobile.startswith("+"):
                kwargs["phone_number"] = mobile

            user_record = auth.create_user(**kwargs)
            uid = user_record.uid

            auth.set_custom_user_claims(uid, {'role': 'admin'})

            ref = db.reference('users/admins')
            ref.child(uid).set({
                'fullname': fullname,
                'email': email,
                'mobile': mobile,
                'role': 'admin',
                'created_at': datetime.datetime.utcnow().isoformat() + "Z"
            })

            flash("✅ Admin registered successfully. You can now login.", "success")
            return redirect(url_for('login'))

        except auth.EmailAlreadyExistsError:
            flash("❌ Email already in use. Try login or use different email.", "danger")
            return redirect(url_for('register'))

        except Exception as e:
            print("Registration error:", e)
            flash("❌ An error occurred while registering. Check server logs.", "danger")
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        userType = request.form.get("userType")
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password or not userType:
            flash("Please fill all fields.", "danger")
            return redirect(url_for("login"))

        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
            payload = {"email": email, "password": password, "returnSecureToken": True}
            res = requests.post(url, json=payload)
            data = res.json()

            if "error" in data:
                flash(data["error"]["message"], "danger")
                return redirect(url_for("login"))

            session["user"] = {
                "email": email,
                "role": userType,
                "idToken": data["idToken"]
            }

            flash("Login successful!", "success")

            if userType == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("faculty_dashboard"))

        except Exception as e:
            print("Login error:", e)
            flash("An error occurred during login.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if "user" in session and session["user"]["role"] == "admin":
        return f"Welcome Admin {session['user']['email']}"
    return redirect(url_for("login"))


@app.route("/faculty/dashboard")
def faculty_dashboard():
    if "user" in session and session["user"]["role"] == "faculty":
        return f"Welcome Faculty {session['user']['email']}"
    return redirect(url_for("login"))


@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    """
    GET -> render forgot password form
    POST -> call Firebase REST API to send password reset email (sendOobCode)
    """
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email:
            flash("Please enter your email address.", "danger")
            return redirect(url_for("forgot_password"))

        try:
            # Firebase REST API: send password reset email
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={API_KEY}"
            payload = {
                "requestType": "PASSWORD_RESET",
                "email": email
            }
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()

            if resp.status_code == 200 and "email" in data:
                flash(f"A password reset email has been sent to {email}. Check your inbox.", "success")
                return redirect(url_for("login"))
            else:
                # firebase returns error object structure: { "error": { "message": "EMAIL_NOT_FOUND", ... } }
                err_msg = data.get("error", {}).get("message", "")
                if err_msg == "EMAIL_NOT_FOUND":
                    flash("Email not found. Please check the email or register first.", "danger")
                else:
                    # For other error codes show friendly message (log full for debugging)
                    print("Password reset error:", data)
                    flash("Could not send reset email. Try again later.", "danger")
                return redirect(url_for("forgot_password"))

        except requests.RequestException as e:
            print("Network error sending reset email:", e)
            flash("Network error. Please try again later.", "danger")
            return redirect(url_for("forgot_password"))

    # GET
    return render_template("forgot.html")


# Example simple logout route (if not present)
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
