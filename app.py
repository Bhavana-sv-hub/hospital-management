
from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret"

# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Patient registration page
@app.route("/patient")
def patient_register():
    return render_template("patient.html")


# Save patient details into MySQL
@app.route("/register", methods=["POST"])
def register_patient():

    name = request.form["name"]
    age = request.form["age"]
    gender = request.form["gender"]
    phone = request.form["phone"]
    address = request.form["address"]

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO patients
        (name, age, gender, phone, address)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (name, age, gender, phone, address)

        cursor.execute(query, values)
        connection.commit()

        flash("Patient registered successfully!")

    except Exception as e:
        if connection:
            connection.rollback()
        print("Error:", e)
        flash("Patient registration failed. Please try again.")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return redirect(url_for("patient_register"))


if __name__ == "__main__":
    app.run(debug=True)
