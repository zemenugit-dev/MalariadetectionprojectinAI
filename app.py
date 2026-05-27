from utils.database import init_db, save_prediction, get_connection

from flask import Flask, render_template, request, redirect, flash, session
import tensorflow as tf
import numpy as np
import cv2
import os
import hashlib
from werkzeug.utils import secure_filename

# ==========================================
# FLASK SETUP
# ==========================================
# ==========================================
# FLASK SETUP
# ==========================================

app = Flask(__name__)

# SECRET KEY
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "dev_secret_key"
)

# BASE DIRECTORY
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# SAFE ABSOLUTE UPLOAD PATH
UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

# FLASK CONFIG
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# MAX IMAGE SIZE = 5MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

# CREATE UPLOAD FOLDER AUTOMATICALLY
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

print("Upload Folder:", UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# ==========================================
# INIT DB
# ==========================================
init_db()

# ==========================================
# LOAD MODEL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "malaria_model.h5")

print("Loading model from:", MODEL_PATH)

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("Model loaded successfully")

# ==========================================
# HELPERS
# ==========================================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_logged_in():
    return "role" in session


def is_admin():
    return session.get("role") == "admin"


def is_doctor():
    return session.get("role") == "doctor"


def is_patient():
    return session.get("role") == "patient"

# ==========================================
# PREDICTION FUNCTION
# ==========================================
def predict_image(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return "Invalid Image", 0

    img = cv2.resize(img, (64, 64))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    # ✅ SAFE MODEL LOADING (NEW FIX)
   

    prediction = model.predict(img, verbose=0)[0][0]

    if prediction >= 0.5:
        confidence = round(prediction * 100, 2)
        result = f"Parasitized (Malaria Detected) - {confidence}%"
    else:
        confidence = round((1 - prediction) * 100, 2)
        result = f"Uninfected (Healthy) - {confidence}%"

    return result, confidence
# ==========================================
# HOME
# ==========================================
@app.route("/")
def home():
    return render_template("index.html")

# ==========================================
# LOGIN
# ==========================================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        hashed = hashlib.sha256(password.encode()).hexdigest()

        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, name, email, role
                FROM users
                WHERE email=? AND password=?
            """, (email, hashed))

            user = cursor.fetchone()

        if user:

            session["user_id"] = user[0]
            session["name"] = user[1]
            session["role"] = user[3]

            if user[3] == "admin":
                return redirect("/admin")
            elif user[3] == "doctor":
                return redirect("/doctor")
            else:
                return redirect("/patient")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ==========================================
# REGISTER
# ==========================================
@app.route("/register", methods=["GET", "POST"])
def register():

    # 🔒 ONLY ADMIN CAN ACCESS PAGE
    if not is_logged_in() or not is_admin():
        return redirect("/login")

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        role = request.form["role"]

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect("/register")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO users (name, email, password, role)
                    VALUES (?, ?, ?, ?)
                """, (fullname, email, hashed_password, role))

                conn.commit()

            flash("User registered successfully!", "success")
            return redirect("/admin/users")

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect("/register")

    return render_template("register.html")
# ==========================================
# PREDICT
# ==========================================
@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ==========================================
        # CHECK IMAGE EXISTS
        # ==========================================
        if "image" not in request.files:
            return render_template(
                "predict.html",
                prediction="No image uploaded"
            )

        file = request.files["image"]

        # ==========================================
        # CHECK FILE NAME
        # ==========================================
        if file.filename == "":
            return render_template(
                "predict.html",
                prediction="No file selected"
            )

        # ==========================================
        # VALIDATE IMAGE TYPE
        # ==========================================
        if file and allowed_file(file.filename):

            import time

            # SAFE FILE NAME
            filename = secure_filename(file.filename)

            unique_name = (
                str(int(time.time())) + "_" + filename
            )

            # CREATE UPLOAD FOLDER
            os.makedirs(
                app.config["UPLOAD_FOLDER"],
                exist_ok=True
            )

            # FILE PATH
            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                unique_name
            )

            print("Saving image to:", filepath)

            # ==========================================
            # SAVE IMAGE
            # ==========================================
            try:

                file.save(filepath)

                if not os.path.exists(filepath):

                    return render_template(
                        "predict.html",
                        prediction="Image not saved"
                    )

                print("Image saved successfully!")

            except Exception as e:

                print("Upload Error:", str(e))

                return render_template(
                    "predict.html",
                    prediction=f"Upload Error: {str(e)}"
                )

            # ==========================================
            # PREDICT IMAGE
            # ==========================================
            print("Starting prediction...")

            result, confidence = predict_image(filepath)

            print("Prediction completed!")

            # ==========================================
            # SAVE TO DATABASE
            # ==========================================
            save_prediction(
                image=unique_name,
                result=result,
                confidence=confidence,
                user_id=session.get("user_id")
            )

            print("Prediction saved!")

            # ==========================================
            # RETURN RESULT
            # ==========================================
            return render_template(
                "predict.html",
                prediction=result,
                image=unique_name
            )

        return render_template(
            "predict.html",
            prediction="Invalid file type"
        )

    except Exception as e:

        print("FULL PREDICT ERROR:", str(e))

        return render_template(
            "predict.html",
            prediction=f"Server Error: {str(e)}"
        )
# ==========================================
# ADMIN DASHBOARD
# ==========================================
@app.route("/admin")
def admin():

    if not is_logged_in() or not is_admin():
        return redirect("/login")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM predictions")
        total_predictions = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM predictions
            WHERE result LIKE '%Parasitized%'
        """)
        positive_cases = cursor.fetchone()[0]

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_predictions=total_predictions,
        positive_cases=positive_cases
    )

# ==========================================
# DOCTOR DASHBOARD
# ==========================================
@app.route("/doctor")
def doctor():

    if not is_logged_in() or not is_doctor():
        return redirect("/login")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM predictions")
        total_predictions = cursor.fetchone()[0]

    return render_template(
        "doctor_dashboard.html",
        total_users=total_users,
        total_predictions=total_predictions
    )

# ==========================================
# PATIENT DASHBOARD
# ==========================================
# ==========================================
# PATIENT DASHBOARD
# ==========================================
@app.route("/patient")
def patient():

    # security check
    if not is_logged_in() or not is_patient():
        return redirect("/login")

    user_id = session.get("user_id")

    try:

        with get_connection() as conn:
            cursor = conn.cursor()

            # ONLY THIS PATIENT DATA
            cursor.execute("""
                SELECT
                    id,
                    result,
                    confidence,
                    created_at
                FROM predictions
                WHERE user_id = ?
                ORDER BY id DESC
            """, (user_id,))

            predictions = cursor.fetchall()

        return render_template(
            "patient_dashboard.html",
            user_name=session.get("name"),
            predictions=predictions,
            total_my_predictions=len(predictions),
            last_result=predictions[0][1] if predictions else "No Result"
        )

    except Exception as e:

        return f"Error loading dashboard: {str(e)}"
# ==========================================
@app.route("/admin/users")
def admin_users():

    if not is_logged_in() or not is_admin():
        return redirect("/login")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email, role
            FROM users
        """)

        users = cursor.fetchall()

    return render_template("admin_users.html", users=users)
# UPDATE USER
# ==========================================
@app.route("/admin/users/update/<int:user_id>", methods=["POST"])
def update_user(user_id):

    if not is_logged_in() or not is_admin():
        return redirect("/login")

    name = request.form["name"]
    email = request.form["email"]
    role = request.form["role"]

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET name=?, email=?, role=?
            WHERE id=?
        """, (name, email, role, user_id))

        conn.commit()

    return redirect("/admin/users")
#edit code 
@app.route("/admin/users/edit/<int:user_id>")
def edit_user(user_id):

    if not is_logged_in() or not is_admin():
        return redirect("/login")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email, role
            FROM users
            WHERE id=?
        """, (user_id,))

        user = cursor.fetchone()

    if user is None:
        return "User not found", 404

    return render_template("edit_user.html", user=user)
# ==========================================
# DELETE USER (FIXED SAFE POST VERSION)
# ==========================================
@app.route("/admin/users/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):

    if not is_logged_in() or not is_admin():
        return redirect("/login")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM users WHERE id=?
        """, (user_id,))

        conn.commit()

    return redirect("/admin/users")
#this is patients 
@app.route("/patients")
def patients():

    if not is_logged_in() or not is_doctor():
        return redirect("/login")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.id,
                u.name,
                u.email,
                p.image,
                p.result,
                p.confidence,
                p.created_at
            FROM predictions p
            JOIN users u
            ON p.user_id = u.id
            ORDER BY p.id DESC
        """)

        patients_data = cursor.fetchall()

    return render_template(
        "patients.html",
        patients=patients_data
    )
#this is also predict page 
@app.route("/predict_page")
def predict_page():

    if not is_logged_in():
        return redirect("/login")

    return render_template("predict.html")
#this is my history sidbar route 
# ==========================================
# MY HISTORY
# ==========================================
@app.route("/my_history")
def my_history():

    if not is_logged_in() or not is_patient():
        return redirect("/login")

    user_id = session.get("user_id")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                u.name,
                p.image,
                p.result,
                p.confidence,
                p.created_at
            FROM predictions p
            JOIN users u
            ON p.user_id = u.id
            WHERE p.user_id = ?
            ORDER BY p.id DESC
        """, (user_id,))

        history = cursor.fetchall()

    return render_template(
        "my_history.html",
        history=history
    )
# ==========================================
# LOGOUT
# ==========================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ==========================================
# RUN APP
# ==========================================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )