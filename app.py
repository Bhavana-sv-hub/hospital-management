from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import date
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

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

@app.route('/doctor')
def add_doctor_page():
    return render_template('doctor.html')

@app.route('/doctors')
def view_doctors():

    search = request.args.get('search', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if search:
            query = """
                SELECT * FROM doctors
                WHERE CAST(doctor_id AS CHAR) LIKE %s
                OR name LIKE %s
                OR specialization LIKE %s
                ORDER BY doctor_id DESC
            """

            search_value = f"%{search}%"
            cursor.execute(
                query,
                (search_value, search_value, search_value)
            )
        else:
            cursor.execute(
                "SELECT * FROM doctors ORDER BY doctor_id DESC"
            )

        doctors = cursor.fetchall()

        return render_template(
            'doctors.html',
            doctors=doctors,
            search=search
        )

    finally:
        cursor.close()
        conn.close()

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    name = request.form['name']
    specialization = request.form.get('specialization')
    phone = request.form.get('phone')
    email = request.form.get('email')

    if not name.strip():
        return "Doctor name is required"

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO doctors (name, specialization, phone, email)
            VALUES (%s, %s, %s, %s)
        """

        values = (name, specialization, phone, email)
        cursor.execute(query, values)
        conn.commit()

        return redirect(url_for('add_doctor_page'))

    finally:
        cursor.close()
        conn.close()

@app.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == 'POST':

            name = request.form['name'].strip()
            specialization = request.form.get('specialization')
            phone = request.form.get('phone')
            email = request.form.get('email')

            if not name:
                return "Doctor name is required"

            query = """
                UPDATE doctors
                SET name = %s,
                    specialization = %s,
                    phone = %s,
                    email = %s
                WHERE doctor_id = %s
            """

            cursor.execute(
                query,
                (name, specialization, phone, email, doctor_id)
            )
            conn.commit()

            return redirect(url_for('view_doctors'))

        cursor.execute(
            "SELECT * FROM doctors WHERE doctor_id = %s",
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        if doctor is None:
            return "Doctor not found", 404

        return render_template('edit_doctor.html', doctor=doctor)

    finally:
        cursor.close()
        conn.close()

@app.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT COUNT(*) FROM appointments WHERE doctor_id = %s",
            (doctor_id,)
        )

        appointment_count = cursor.fetchone()[0]

        if appointment_count > 0:
            return "Cannot delete doctor because appointments exist.", 409

        cursor.execute(
            "DELETE FROM doctors WHERE doctor_id = %s",
            (doctor_id,)
        )

        conn.commit()

        return redirect(url_for('view_doctors'))

    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )

            user = cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

        if user and check_password_hash(
            user['password_hash'], password
        ):

            session.clear()

            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']

            return redirect(url_for('dashboard'))

        return render_template(
            'login.html',
            error='Invalid username or password'
        ), 401

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    role = session.get('role')

    if role == 'patient':
        return render_template(
            'patient_dashboard.html',
            username=session['username']
        )

    return "Dashboard for this role is not created yet."

@app.route('/logout', methods=['POST'])
def logout():

    session.clear()

    return redirect(url_for('login'))



@app.route('/register_user', methods=['GET', 'POST'])
def register_user():

    if request.method == 'POST':

        name = request.form.get('name', '').strip()
        age = request.form.get('age', type=int)
        gender = request.form.get('gender', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not all([name, age, username, password]):
            return render_template(
                'register.html',
                error='Please fill in all required fields.'
            )

        if age < 1 or age > 120:
            return render_template(
                'register.html',
                error='Please enter a valid age.'
            )

        if password != confirm_password:
            return render_template(
                'register.html',
                error='Passwords do not match.'
            )

        if len(password) < 8:
            return render_template(
                'register.html',
                error='Password must contain at least 8 characters.'
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT user_id FROM users WHERE username = %s",
                (username,)
            )

            if cursor.fetchone():
                return render_template(
                    'register.html',
                    error='Username already exists.'
                ), 409

            password_hash = generate_password_hash(password)

            # Insert patient information
            cursor.execute(
                """
                INSERT INTO patients
                (name, age, gender, phone, address)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (name, age, gender, phone, address)
            )

            patient_id = cursor.lastrowid

            # Create patient login account
            cursor.execute(
                """
                INSERT INTO users
                (username, password_hash, role, patient_id)
                VALUES (%s, %s, 'patient', %s)
                """,
                (username, password_hash, patient_id)
            )

            conn.commit()

            flash("Registration successful! Please log in.")

            return redirect(url_for('login'))

        except Exception:
            conn.rollback()
            app.logger.exception("Patient registration failed")

            return render_template(
                'register.html',
                error='Registration failed. Please check the server error.'
            ), 400

        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')
@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():

    # Only logged-in patients can book
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Find the patient linked to the logged-in account
        cursor.execute(
            "SELECT patient_id FROM users WHERE user_id = %s",
            (session['user_id'],)
        )

        user = cursor.fetchone()

        if not user or not user['patient_id']:
            return "Patient account is not linked correctly.", 403

        patient_id = user['patient_id']

        if request.method == 'GET':
            cursor.execute(
                "SELECT doctor_id, name, specialization FROM doctors ORDER BY name"
            )
            doctors = cursor.fetchall()

            return render_template(
                'book_appointment.html',
                doctors=doctors,
                today=date.today().isoformat()
            )

        # Read booking details
        doctor_id = request.form.get('doctor_id', type=int)
        appointment_date = request.form.get('appointment_date')
        reason = request.form.get('reason', '').strip()

        if not doctor_id or not appointment_date:
            return "Please select a doctor and appointment date.", 400

        try:
            selected_date = date.fromisoformat(appointment_date)
        except ValueError:
            return "Invalid appointment date.", 400

        if selected_date < date.today():
            return "You cannot book an appointment in the past.", 400

        # Start a transaction
        conn.start_transaction()

        # Lock the doctor row to prevent simultaneous token allocation
        cursor.execute(
            "SELECT doctor_id FROM doctors WHERE doctor_id = %s FOR UPDATE",
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        if not doctor:
            conn.rollback()
            return "Doctor not found.", 404

        # Prevent the same patient from booking twice
        # with the same doctor on the same date
        cursor.execute(
            """
            SELECT appointment_id
            FROM appointments
            WHERE patient_id = %s
              AND doctor_id = %s
              AND appointment_date = %s
              AND status <> 'Cancelled'
            """,
            (patient_id, doctor_id, selected_date)
        )

        if cursor.fetchone():
            conn.rollback()
            return "You already have an appointment with this doctor on this date."

        # Get currently occupied tokens
        cursor.execute(
            """
            SELECT token_number
            FROM appointments
            WHERE doctor_id = %s
              AND appointment_date = %s
              AND status <> 'Cancelled'
              AND token_number IS NOT NULL
            """,
            (doctor_id, selected_date)
        )

        occupied_tokens = {
            row['token_number'] for row in cursor.fetchall()
        }

        # Find the first available token
        available_token = next(
            (n for n in range(1, 31) if n not in occupied_tokens),
            None
        )

        if available_token is None:
            conn.rollback()

            cursor.execute(
                """
                SELECT name, specialization
                FROM doctors
                WHERE doctor_id = %s
                """,
                (doctor_id,)
            )
            doctor_details = cursor.fetchone()

            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM appointments
                WHERE doctor_id = %s
                  AND appointment_date = %s
                  AND status <> 'Cancelled'
                """,
                (doctor_id, selected_date)
            )
            total = cursor.fetchone()['total']

            cursor.execute(
                "SELECT doctor_id, name, specialization FROM doctors ORDER BY name"
            )
            doctors = cursor.fetchall()

            return render_template(
                'book_appointment.html',
                doctors=doctors,
                today=date.today().isoformat(),
                error=f"{doctor_details['name']} is fully booked on this date ({total}/30). Please choose another date."
            )

        # Save appointment
        cursor.execute(
            """
            INSERT INTO appointments
            (patient_id, doctor_id, appointment_date,
             appointment_time, reason, status, token_number)
            VALUES (%s, %s, %s, NULL, %s, 'Scheduled', %s)
            """,
            (
                patient_id,
                doctor_id,
                selected_date,
                reason,
                available_token
            )
        )

        conn.commit()

        cursor.execute(
            """
            SELECT name, specialization
            FROM doctors
            WHERE doctor_id = %s
            """,
            (doctor_id,)
        )
        doctor_details = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM appointments
            WHERE doctor_id = %s
              AND appointment_date = %s
              AND status <> 'Cancelled'
            """,
            (doctor_id, selected_date)
        )
        total = cursor.fetchone()['total']

        cursor.execute(
            "SELECT doctor_id, name, specialization FROM doctors ORDER BY name"
        )
        doctors = cursor.fetchall()

        return render_template(
            'book_appointment.html',
            doctors=doctors,
            today=date.today().isoformat(),
            success=True,
            token_number=available_token,
            doctor_name=doctor_details['name'],
            appointment_date=selected_date,
            total_booked=total
        )

    except Exception:
        conn.rollback()
        app.logger.exception("Appointment booking failed")
        return "Appointment booking failed. Please try again.", 500

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
