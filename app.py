import mysql.connector
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from db import get_db  # your existing reservations DB helper (keep it)

def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="cafe_user",
        password="cafe_password_123",
        database="cafe"
    )

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = "your_secret_key_here"

    # ---- Globals for templates ----
    @app.context_processor
    def inject_globals():
        return {
            "current_year": datetime.now().year,
            "site_settings": {
                "enable_reservations": False,   # True for restaurant clients
                "phone": "+977 98XXXXXXXX",
            }
        }

    # ---- Test DB route ----
    @app.get("/test-db")
    def test_db():
        try:
            conn = get_mysql_connection()
            cur = conn.cursor()
            cur.execute("SELECT DATABASE();")
            db = cur.fetchone()
            cur.close()
            conn.close()
            return f"Connected to: {db}"
        except Exception as e:
            return f"Error: {e}"

    # ---- Home (GET shows reviews, POST saves review) ----
    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            message = request.form.get("message", "").strip()
            rating = request.form.get("rating", "5").strip()

            # validate
            if not name or not message:
                flash("Please enter your name and review.", "error")
                return redirect(url_for("home"))

            try:
                rating_int = int(rating)
            except ValueError:
                rating_int = 5
            if rating_int < 1 or rating_int > 5:
                rating_int = 5

            # insert
            conn = get_mysql_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO reviews (name, rating, message) VALUES (%s, %s, %s)",
                (name[:60], rating_int, message[:600])
            )
            conn.commit()
            cur.close()
            conn.close()

            flash("Thanks! Your review has been added.", "success")
            return redirect(url_for("home"))

        # fetch reviews
        conn = get_mysql_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT name, rating, message
            FROM reviews
            WHERE approved = TRUE
            ORDER BY created_at DESC
            LIMIT 8
        """)
        reviews = cur.fetchall()
        cur.close()
        conn.close()

        return render_template("index.html", reviews=reviews)

    @app.get("/menu")
    def menu():
        return render_template("menu.html")

    @app.get("/contact")
    def contact():
        return render_template("contact.html")

    # Optional: keep reservations route but only link to it when enabled in base.html
    @app.route("/reservations", methods=["GET", "POST"])
    def reservations():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            phone = request.form.get("phone", "").strip()
            guests = request.form.get("guests", "1").strip()
            date = request.form.get("date", "").strip()
            time = request.form.get("time", "").strip()

            if not name or not phone or not date or not time:
                flash("Please fill all required fields.", "error")
                return redirect(url_for("reservations"))

            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO reservations (name, phone, guests, res_date, res_time, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
                """,
                (name, phone, guests, date, time),
            )
            conn.commit()
            cur.close()
            conn.close()

            flash("Reservation received! We’ll contact you to confirm.", "success")
            return redirect(url_for("reservations"))

        return render_template("reservations.html")

    return app

if __name__ == "__main__":
    create_app().run(debug=True)