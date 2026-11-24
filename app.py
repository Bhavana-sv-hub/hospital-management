
from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection
from flask import Flask, render_template, request, redirect, url_for

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

# View and Search Patients
@app.route("/patients")
def view_patients():

    search = request.args.get("search", "").strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if search:

        query = """
        SELECT * FROM patients
        WHERE name LIKE %s
        OR phone LIKE %s
        OR CAST(patient_id AS CHAR) LIKE %s
        ORDER BY patient_id DESC
        """

        keyword = "%" + search + "%"

        cursor.execute(
            query,
            (keyword, keyword, keyword)
        )

    else:

        cursor.execute(
            "SELECT * FROM patients ORDER BY patient_id DESC"
        )

    patients = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "patients.html",
        patients=patients,
        search=search
    )



# Edit Patient
@app.route("/edit_patient/<int:patient_id>", methods=["GET", "POST"])
def edit_patient(patient_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        address = request.form["address"]

        query = """
        UPDATE patients
        SET name=%s, age=%s, gender=%s,
            phone=%s, address=%s
        WHERE patient_id=%s
        """

        cursor.execute(
            query,
            (name, age, gender, phone, address, patient_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("view_patients"))

    cursor.execute(
        "SELECT * FROM patients WHERE patient_id=%s",
        (patient_id,)
    )

    patient = cursor.fetchone()

    cursor.close()
    connection.close()

    if patient is None:
        return "Patient not found", 404

    return render_template(
        "edit_patient.html",
        patient=patient
    )


# Delete Patient
@app.route("/delete_patient/<int:patient_id>", methods=["POST"])
def delete_patient(patient_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM patients
    WHERE patient_id = %s
    """

    cursor.execute(query, (patient_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("view_patients"))


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
