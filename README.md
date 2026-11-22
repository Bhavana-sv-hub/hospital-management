# 🏥 Hospital Management System

## 📌 Project Overview

The Hospital Management System (HMS) is a web-based application developed using Python Flask and MySQL to simplify and manage hospital operations.

The application provides a user-friendly interface for managing patient information and maintaining organized hospital records.

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS
- **Backend:** Python, Flask
- **Database:** MySQL
- **Database Connectivity:** MySQL Connector for Python
- **Code Editor:** Visual Studio Code

## ✨ Features

- User-friendly and responsive web interface
- Hospital homepage with organized navigation
- Patient registration form
- Patient information stored in MySQL database
- Flask backend integration
- Organized project structure

## 📂 Project Structure

```text
hospital-management/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   └── patient.html
│
├── app.py
├── database.py
├── test_db.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/Bhavana-sv-hub/hospital-management.git
```

### 2. Navigate to the project folder

```bash
cd hospital-management
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure MySQL Database

- Install and open MySQL Workbench.
- Create the database named `hospital_db`.
- Create the required tables: `patients`, `doctors`, and `appointments`.
- Configure your MySQL username and password.

Set your database password in PowerShell:

```powershell
$env:DB_PASSWORD = 'YOUR_MYSQL_PASSWORD'
```

### 7. Run the application

```bash
python app.py
```

### 8. Open the application

Open the following URL in your browser:

```text
http://127.0.0.1:5000/
```

## 👩‍💻 Author

**Bhavana S V**

Electronics and Communication Engineering Student

GitHub: [Bhavana-sv-hub](https://github.com/Bhavana-sv-hub)
