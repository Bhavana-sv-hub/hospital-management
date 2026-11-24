# Hospital Management System

A web-based Hospital Management System developed using Python, Flask, HTML, CSS and MySQL to manage patient information and hospital records.

## Project Overview

The Hospital Management System (HMS) is designed to simplify basic hospital operations through a centralized web application.

The application allows users to register patients, store their information in a MySQL database and view existing patient records through a web interface.

The project demonstrates frontend development, backend integration, database connectivity and CRUD operations.

## Technologies Used

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3 |
| Backend | Python 3, Flask |
| Database | MySQL |
| Database Connectivity | mysql-connector-python |
| Development Environment | Visual Studio Code |
| Version Control | Git and GitHub |

## Implemented Features

### Patient Management
- Patient registration with name, age, gender, phone number and address.
- Store patient information in MySQL.
- Retrieve and display registered patient records.
- Search patient records by patient ID, name or phone number.
- Edit existing patient information.
- Delete patient records.


### Application Features
- User-friendly web interface.
- Separate pages for patient registration and patient records.
- Flask-based routing and backend processing.
- MySQL database integration.
- Organized project structure.

## Project Architecture

The application follows a simple three-layer architecture:

1. **Presentation Layer:** HTML and CSS provide the user interface.
2. **Application Layer:** Flask handles requests, application logic and routing.
3. **Database Layer:** MySQL stores and manages patient information.

## Project Structure

```text
hospital-management/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── patient.html
│   ├── patients.html
│   └── edit_patient.html
│
├── app.py
├── database.py
├── test_db.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Database Design

Database Name: `hospital_db`

The database contains the following tables:

| Table | Purpose |
|---|---|
| patients | Stores patient information |
| doctors | Stores doctor information |
| appointments | Stores appointment information and patient-doctor relationships |

The patient table includes fields such as patient ID, name, age, gender, phone number, address and registration date.

The doctors and appointments tables have been created as part of the database structure. Their application-level management features are planned for future development.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Bhavana-sv-hub/hospital-management.git
```

### 2. Navigate to the Project Directory

```bash
cd hospital-management
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure MySQL

- Install MySQL Server and MySQL Workbench.
- Create a database named `hospital_db`.
- Create the required database tables.
- Configure your MySQL username and password.

Set the database password in PowerShell:

```powershell
$env:DB_PASSWORD = 'YOUR_MYSQL_PASSWORD'
```
Use your own database password.

### 7. Run the Application

```bash
python app.py
```

### 8. Open the Application

Visit:

http://127.0.0.1:5000/

## Future Enhancements

- Doctor registration and management.
- Doctor information and specialization management.
- Appointment booking and scheduling.
- Appointment status management.
- Improved input validation and error handling.
- User authentication and role-based access.

## Learning Outcomes

Through this project, I am gaining practical experience in:

- Developing web applications using Flask.
- Connecting Python applications to MySQL.
- Performing database CRUD operations.
- Designing frontend interfaces using HTML and CSS.
- Managing application code using Git and GitHub.

## Author

**Bhavana S V**

Electronics and Communication Engineering Student

GitHub Profile: https://github.com/Bhavana-sv-hub

Project Repository: https://github.com/Bhavana-sv-hub/hospital-management