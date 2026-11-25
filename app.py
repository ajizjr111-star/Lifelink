
import os
import sqlite3
from flask import Flask, request, redirect, session, render_template_string

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-before-public-use"
)

DB_NAME = os.environ.get("DATABASE_PATH", "lifelink.db")


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

def create_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            phone TEXT NOT NULL,
            city TEXT NOT NULL,
            available TEXT DEFAULT 'Yes'
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS blood_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            hospital TEXT NOT NULL,
            units INTEGER NOT NULL,
            city TEXT NOT NULL,
            contact TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    connection.commit()
    connection.close()


create_database()


# ==========================================
# PREMIUM DARK WEBSITE DESIGN
# ==========================================

BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{{ page_title }} | LifeLink</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            background: #08090d;
            color: #f5f5f5;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
        }

        :root {
            --red: #ef3340;
            --red-dark: #b91c2b;
            --bg: #08090d;
            --card: #12141c;
            --border: #252733;
            --muted: #a0a2ad;
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        .navbar {
            width: 100%;
            min-height: 76px;
            padding: 15px 7%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(8, 9, 13, 0.94);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(15px);
        }

        .logo {
            font-size: 25px;
            font-weight: 800;
            letter-spacing: -1px;
        }

        .logo span {
            color: var(--red);
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 26px;
        }

        .nav-links a {
            color: #c4c5ce;
            font-size: 13px;
            font-weight: 600;
            transition: 0.3s;
        }

        .nav-links a:hover,
        .nav-links a.active {
            color: var(--red);
        }

        .nav-links .nav-cta {
            background: var(--red);
            color: white;
            padding: 11px 18px;
            border-radius: 8px;
        }

        .nav-links .nav-cta:hover {
            background: var(--red-dark);
            color: white;
        }

        .container {
            width: 86%;
            max-width: 1200px;
            margin: auto;
        }

        .hero {
            min-height: 520px;
            display: flex;
            align-items: center;
            padding: 80px 0;
            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: "";
            position: absolute;
            width: 430px;
            height: 430px;
            background: rgba(239, 51, 64, 0.13);
            filter: blur(100px);
            border-radius: 50%;
            right: -100px;
            top: 30px;
            animation: glow 5s infinite alternate;
        }

        .hero-content {
            max-width: 700px;
            position: relative;
            z-index: 1;
            animation: slideUp 0.9s ease;
        }

        .tag {
            display: inline-block;
            color: #ff737c;
            background: rgba(239, 51, 64, 0.12);
            border: 1px solid rgba(239, 51, 64, 0.3);
            padding: 8px 15px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 22px;
        }

        .hero h1 {
            font-size: clamp(38px, 6vw, 68px);
            line-height: 1.12;
            letter-spacing: -2px;
            margin-bottom: 22px;
        }

        .hero h1 span {
            color: var(--red);
        }

        .hero p {
            color: var(--muted);
            font-size: 16px;
            max-width: 600px;
            margin-bottom: 30px;
        }

        .btn {
            display: inline-block;
            background: var(--red);
            color: white;
            padding: 13px 23px;
            border-radius: 9px;
            font-size: 14px;
            font-weight: 700;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }

        .btn:hover {
            background: var(--red-dark);
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(239, 51, 64, 0.25);
        }

        .btn-outline {
            display: inline-block;
            border: 1px solid #454752;
            color: white;
            padding: 12px 22px;
            border-radius: 9px;
            font-size: 14px;
            font-weight: 600;
            margin-left: 10px;
            transition: 0.3s;
        }

        .btn-outline:hover {
            border-color: var(--red);
            color: var(--red);
        }

        .section {
            padding: 65px 0;
        }

        .section-heading {
            text-align: center;
            margin-bottom: 38px;
        }

        .section-heading h2 {
            font-size: 32px;
            margin-bottom: 10px;
        }

        .section-heading h2 span {
            color: var(--red);
        }

        .section-heading p {
            color: var(--muted);
            font-size: 14px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 22px;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 15px;
            padding: 27px;
            transition: 0.35s;
        }

        .card:hover {
            transform: translateY(-7px);
            border-color: var(--red);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
        }

        .card-icon {
            font-size: 30px;
            margin-bottom: 15px;
        }

        .card h3 {
            font-size: 18px;
            margin-bottom: 10px;
        }

        .card p {
            color: var(--muted);
            font-size: 13px;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .stat-box {
            background: #11131b;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 25px;
            text-align: center;
        }

        .stat-box h2 {
            font-size: 34px;
            color: var(--red);
        }

        .stat-box p {
            color: var(--muted);
            font-size: 13px;
        }

        .form-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 17px;
            padding: 35px;
            max-width: 650px;
            margin: 40px auto;
            box-shadow: 0 15px 45px rgba(0, 0, 0, 0.2);
        }

        .form-card h2 {
            font-size: 27px;
            margin-bottom: 8px;
        }

        .form-card > p {
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 25px;
        }

        .form-group {
            margin-bottom: 18px;
        }

        .form-group label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            background: #090a10;
            border: 1px solid #30323d;
            color: white;
            padding: 13px 14px;
            border-radius: 8px;
            outline: none;
            font-family: inherit;
            font-size: 14px;
        }

        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            border-color: var(--red);
            box-shadow: 0 0 0 3px rgba(239, 51, 64, 0.1);
        }

        .form-group select option {
            background: #12141c;
        }

        .form-card .btn {
            width: 100%;
            margin-top: 8px;
        }

        .notice {
            padding: 13px 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 13px;
            background: rgba(239, 51, 64, 0.12);
            border: 1px solid rgba(239, 51, 64, 0.35);
            color: #ff9ba2;
        }

        .notice.success {
            background: rgba(34, 197, 94, 0.1);
            border-color: rgba(34, 197, 94, 0.3);
            color: #86efac;
        }

        .table-wrap {
            overflow-x: auto;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            margin-top: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 650px;
        }

        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid var(--border);
            font-size: 13px;
        }

        th {
            color: #ff737c;
            background: #19121a;
        }

        td {
            color: #d1d1d8;
        }

        .empty {
            text-align: center;
            color: var(--muted);
            padding: 30px;
        }

        .footer {
            margin-top: 70px;
            padding: 35px 7%;
            border-top: 1px solid var(--border);
            text-align: center;
            background: #07080b;
        }

        .footer p {
            color: var(--muted);
            font-size: 12px;
        }

        .footer span {
            color: var(--red);
        }

        .page-top {
            padding: 55px 0 15px;
            text-align: center;
        }

        .page-top h1 {
            font-size: 38px;
            margin-bottom: 10px;
        }

        .page-top h1 span {
            color: var(--red);
        }

        .page-top p {
            color: var(--muted);
            font-size: 14px;
        }

        .reveal {
            animation: slideUp 0.7s ease both;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(25px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes glow {
            from {
                opacity: 0.5;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1.1);
            }
        }

        @media (max-width: 850px) {
            .navbar {
                padding: 15px 5%;
                align-items: flex-start;
                gap: 15px;
                flex-direction: column;
            }

            .nav-links {
                flex-wrap: wrap;
                gap: 14px;
            }

            .container {
                width: 90%;
            }
        }

        @media (max-width: 550px) {
            .hero {
                min-height: 450px;
                padding: 55px 0;
            }

            .hero h1 {
                font-size: 42px;
            }

            .btn-outline {
                margin: 12px 0 0;
            }

            .form-card {
                padding: 23px;
            }

            .page-top h1 {
                font-size: 30px;
            }
        }
    </style>
</head>

<body>

<nav class="navbar">
    <a href="/" class="logo">Life<span>Link.</span></a>

    <div class="nav-links">
        <a href="/" class="{{ 'active' if active == 'home' else '' }}">Home</a>
        <a href="/register" class="{{ 'active' if active == 'register' else '' }}">Become a Donor</a>
        <a href="/search" class="{{ 'active' if active == 'search' else '' }}">Find Donors</a>
        <a href="/emergency" class="{{ 'active' if active == 'emergency' else '' }}">Emergency</a>

        {% if is_admin %}
            <a href="/admin">Dashboard</a>
            <a href="/logout">Logout</a>
        {% else %}
            <a href="/login" class="nav-cta">Admin Login</a>
        {% endif %}
    </div>
</nav>

{{ content|safe }}

<footer class="footer">
    <p>© 2026 <span>LifeLink</span> — Connecting Donors. Saving Lives.</p>
    <p style="margin-top:8px;">A blood donor and emergency request management project.</p>
</footer>

</body>
</html>
"""


# ==========================================
# PAGE RENDERING HELPER
# ==========================================

def page(template, **context):
    page_title = context.pop("page_title", "Blood Donor Network")
    active = context.pop("active", "")

    return render_template_string(
        BASE.replace("{{ content|safe }}", template),
        page_title=page_title,
        active=active,
        is_admin=bool(session.get("admin")),
        **context
    )

# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    connection = get_db()

    total_donors = connection.execute(
        "SELECT COUNT(*) FROM donors"
    ).fetchone()[0]

    total_requests = connection.execute(
        "SELECT COUNT(*) FROM blood_requests"
    ).fetchone()[0]

    connection.close()

    content = """
    <section class="hero">
        <div class="container">
            <div class="hero-content">

                <div class="tag">
                    ❤️ EVERY DONATION MATTERS
                </div>

                <h1>
                    Your Blood Can
                    <span>Save a Life.</span>
                </h1>

                <p>
                    LifeLink connects blood donors with people
                    who need blood during emergencies.
                    Together, we can make a difference.
                </p>

                <a href="/register" class="btn">
                    Become a Donor →
                </a>

                <a href="/search" class="btn-outline">
                    Find Blood Donors
                </a>

            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">

            <div class="section-heading">
                <h2>Our <span>Impact</span></h2>
                <p>Every number represents an opportunity to help.</p>
            </div>

            <div class="stats">

                <div class="stat-box">
                    <h2>{{ total_donors }}</h2>
                    <p>Registered Donors</p>
                </div>

                <div class="stat-box">
                    <h2>{{ total_requests }}</h2>
                    <p>Blood Requests</p>
                </div>

                <div class="stat-box">
                    <h2>24/7</h2>
                    <p>Emergency Access</p>
                </div>

            </div>

        </div>
    </section>

    <section class="section">
        <div class="container">

            <div class="section-heading">
                <h2>How <span>LifeLink</span> Works</h2>
                <p>Three simple steps to help save a life.</p>
            </div>

            <div class="cards">

                <div class="card">
                    <div class="card-icon">🩸</div>
                    <h3>Register as Donor</h3>
                    <p>
                        Register your details and blood group
                        to become a potential blood donor.
                    </p>
                </div>

                <div class="card">
                    <div class="card-icon">🔍</div>
                    <h3>Find Donors</h3>
                    <p>
                        Search registered donors by blood
                        group and city.
                    </p>
                </div>

                <div class="card">
                    <div class="card-icon">🚨</div>
                    <h3>Emergency Request</h3>
                    <p>
                        Submit a blood requirement with
                        hospital and patient details.
                    </p>
                </div>

            </div>

        </div>
    </section>

    <section class="section">
        <div class="container" style="text-align:center;">

            <h2 style="font-size:30px;">
                Be Someone's <span style="color:#ef3340;">Hero.</span>
            </h2>

            <p style="color:#a0a2ad;margin:15px 0 25px;">
                A small act of kindness can make a huge difference.
            </p>

            <a href="/register" class="btn">
                Register Today →
            </a>

        </div>
    </section>
    """

    return page(
        content,
        page_title="Home",
        active="home",
        total_donors=total_donors,
        total_requests=total_requests
    )

# ==========================================
# DONOR REGISTRATION
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""
    success = False

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        blood_group = request.form.get("blood_group", "").strip()
        phone = request.form.get("phone", "").strip()
        city = request.form.get("city", "").strip()

        valid_groups = [
            "A+", "A-", "B+", "B-",
            "O+", "O-", "AB+", "AB-"
        ]

        if not all([name, blood_group, phone, city]):
            message = "Please fill in all the fields."

        elif blood_group not in valid_groups:
            message = "Please select a valid blood group."

        elif not phone.isdigit() or len(phone) != 10:
            message = "Please enter a valid 10-digit phone number."

        else:
            connection = get_db()

            connection.execute("""
                INSERT INTO donors
                (name, blood_group, phone, city)
                VALUES (?, ?, ?, ?)
            """, (name, blood_group, phone, city))

            connection.commit()
            connection.close()

            message = "Registration successful! Thank you for becoming a donor."
            success = True

    content = """
    <div class="container">

        <div class="page-top">
            <h1>Become a <span>Donor</span></h1>
            <p>Your one registration could help save someone's life.</p>
        </div>

        <div class="form-card">

            <h2>Donor Registration</h2>
            <p>Enter your details to join the LifeLink donor network.</p>

            {% if message %}
                <div class="notice {{ 'success' if success else '' }}">
                    {{ message }}
                </div>
            {% endif %}

            <form method="POST">

                <div class="form-group">
                    <label>Full Name</label>
                    <input
                        type="text"
                        name="name"
                        placeholder="Enter your full name"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Blood Group</label>

                    <select name="blood_group" required>
                        <option value="">Select blood group</option>
                        <option>A+</option>
                        <option>A-</option>
                        <option>B+</option>
                        <option>B-</option>
                        <option>O+</option>
                        <option>O-</option>
                        <option>AB+</option>
                        <option>AB-</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Phone Number</label>
                    <input
                        type="tel"
                        name="phone"
                        placeholder="Enter 10-digit phone number"
                        maxlength="10"
                        pattern="[0-9]{10}"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>City</label>
                    <input
                        type="text"
                        name="city"
                        placeholder="Enter your city"
                        required
                    >
                </div>

                <button type="submit" class="btn">
                    Register as Donor →
                </button>

            </form>

        </div>

    </div>
    """

    return page(
        content,
        page_title="Donor Registration",
        active="register",
        message=message,
        success=success
    )

# ==========================================
# SEARCH BLOOD DONORS
# ==========================================

@app.route("/search", methods=["GET", "POST"])
def search():

    donors = []
    searched = False

    if request.method == "POST":

        blood_group = request.form.get("blood_group", "").strip()
        city = request.form.get("city", "").strip()

        connection = get_db()

        query = """
            SELECT name, blood_group, city, available
            FROM donors
            WHERE available = 'Yes'
        """

        parameters = []

        if blood_group:
            query += " AND blood_group = ?"
            parameters.append(blood_group)

        if city:
            query += " AND city LIKE ?"
            parameters.append("%" + city + "%")

        donors = connection.execute(
            query, parameters
        ).fetchall()

        connection.close()

        searched = True

    content = """
    <div class="container">

        <div class="page-top">
            <h1>Find Blood <span>Donors</span></h1>
            <p>Search for registered donors by blood group and city.</p>
        </div>

        <div class="form-card">

            <h2>Search Donors</h2>
            <p>Enter your search details below.</p>

            <form method="POST">

                <div class="form-group">
                    <label>Blood Group</label>

                    <select name="blood_group">
                        <option value="">All Blood Groups</option>
                        <option>A+</option>
                        <option>A-</option>
                        <option>B+</option>
                        <option>B-</option>
                        <option>O+</option>
                        <option>O-</option>
                        <option>AB+</option>
                        <option>AB-</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>City</label>
                    <input
                        type="text"
                        name="city"
                        placeholder="Enter city name"
                    >
                </div>

                <button type="submit" class="btn">
                    Search Donors →
                </button>

            </form>

        </div>

        {% if searched %}

            <div class="section-heading">
                <h2>Search <span>Results</span></h2>
                <p>{{ donors|length }} donor(s) found.</p>
            </div>

            {% if donors %}

                <div class="cards">

                    {% for donor in donors %}

                        <div class="card">

                            <div class="card-icon">🩸</div>

                            <h3>{{ donor['name'] }}</h3>

                            <p>
                                Blood Group:
                                <strong style="color:#ef3340;">
                                    {{ donor['blood_group'] }}
                                </strong>
                            </p>

                            <p style="margin-top:8px;">
                                📍 {{ donor['city'] }}
                            </p>

                            <p style="margin-top:8px;color:#86efac;">
                                ● Available
                            </p>

                        </div>

                    {% endfor %}

                </div>

            {% else %}

                <div class="card empty">
                    No matching donors found.
                    Try another blood group or city.
                </div>

            {% endif %}

        {% endif %}

    </div>
    """

    return page(
        content,
        page_title="Find Donors",
        active="search",
        donors=donors,
        searched=searched
    )

# ==========================================
# EMERGENCY BLOOD REQUEST
# ==========================================

@app.route("/emergency", methods=["GET", "POST"])
def emergency():

    message = ""
    success = False

    if request.method == "POST":

        patient_name = request.form.get("patient_name", "").strip()
        blood_group = request.form.get("blood_group", "").strip()
        hospital = request.form.get("hospital", "").strip()
        units = request.form.get("units", "").strip()
        city = request.form.get("city", "").strip()
        contact = request.form.get("contact", "").strip()

        valid_groups = [
            "A+", "A-", "B+", "B-",
            "O+", "O-", "AB+", "AB-"
        ]

        if not all([
            patient_name, blood_group, hospital,
            units, city, contact
        ]):
            message = "Please fill in all the fields."

        elif blood_group not in valid_groups:
            message = "Please select a valid blood group."

        elif not units.isdigit() or not (1 <= int(units) <= 100):
            message = "Please enter a valid number of units."

        elif not contact.isdigit() or len(contact) != 10:
            message = "Please enter a valid 10-digit contact number."

        else:
            connection = get_db()

            connection.execute("""
                INSERT INTO blood_requests
                (patient_name, blood_group, hospital,
                 units, city, contact)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                patient_name,
                blood_group,
                hospital,
                int(units),
                city,
                contact
            ))

            connection.commit()
            connection.close()

            message = "Emergency request submitted successfully!"
            success = True

    content = """
    <div class="container">

        <div class="page-top">
            <h1>Emergency <span>Blood Request</span></h1>
            <p>Submit a blood requirement to connect with potential donors.</p>
        </div>

        <div class="form-card">

            <h2>🚨 Request Blood</h2>
            <p>Enter the patient's information carefully.</p>

            {% if message %}
                <div class="notice {{ 'success' if success else '' }}">
                    {{ message }}
                </div>
            {% endif %}

            <form method="POST">

                <div class="form-group">
                    <label>Patient Name</label>
                    <input
                        type="text"
                        name="patient_name"
                        placeholder="Enter patient name"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Required Blood Group</label>

                    <select name="blood_group" required>
                        <option value="">Select blood group</option>
                        <option>A+</option>
                        <option>A-</option>
                        <option>B+</option>
                        <option>B-</option>
                        <option>O+</option>
                        <option>O-</option>
                        <option>AB+</option>
                        <option>AB-</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Hospital Name</label>
                    <input
                        type="text"
                        name="hospital"
                        placeholder="Enter hospital name"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Number of Blood Units</label>
                    <input
                        type="number"
                        name="units"
                        min="1"
                        max="100"
                        placeholder="Example: 2"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>City</label>
                    <input
                        type="text"
                        name="city"
                        placeholder="Enter city"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Contact Number</label>
                    <input
                        type="tel"
                        name="contact"
                        maxlength="10"
                        pattern="[0-9]{10}"
                        placeholder="Enter 10-digit number"
                        required
                    >
                </div>

                <button type="submit" class="btn">
                    Submit Emergency Request →
                </button>

            </form>

            <p style="margin-top:18px;color:#ff9ba2;font-size:12px;">
                Note: LifeLink is a project-based donor connection
                platform, not an emergency medical service.
                For urgent medical help, contact a hospital or
                local emergency services directly.
            </p>

        </div>

    </div>
    """

    return page(
        content,
        page_title="Emergency Request",
        active="emergency",
        message=message,
        success=success
    )

# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if session.get("admin"):
        return redirect("/admin")

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        admin_username = os.environ.get(
            "ADMIN_USERNAME", "admin"
        )

        admin_password = os.environ.get(
            "ADMIN_PASSWORD", "admin123"
        )

        if username == admin_username and password == admin_password:
            session["admin"] = True
            return redirect("/admin")

        else:
            message = "Invalid username or password."

    content = """
    <div class="container">

        <div class="page-top">
            <h1>Admin <span>Login</span></h1>
            <p>Secure access to the LifeLink administration panel.</p>
        </div>

        <div class="form-card">

            <h2>🔐 Welcome Back</h2>
            <p>Login with your administrator credentials.</p>

            {% if message %}
                <div class="notice">{{ message }}</div>
            {% endif %}

            <form method="POST">

                <div class="form-group">
                    <label>Username</label>
                    <input
                        type="text"
                        name="username"
                        placeholder="Enter admin username"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Password</label>
                    <input
                        type="password"
                        name="password"
                        placeholder="Enter admin password"
                        required
                    >
                </div>

                <button type="submit" class="btn">
                    Login to Dashboard →
                </button>

            </form>

        </div>

    </div>
    """

    return page(
        content,
        page_title="Admin Login",
        message=message
    )


# ==========================================
# PROTECT ADMIN PAGES
# ==========================================

@app.before_request
def protect_admin_pages():

    if request.path in ["/admin", "/logout"]:
        if not session.get("admin"):
            return redirect("/login")

# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    connection = get_db()

    total_donors = connection.execute(
        "SELECT COUNT(*) FROM donors"
    ).fetchone()[0]

    total_requests = connection.execute(
        "SELECT COUNT(*) FROM blood_requests"
    ).fetchone()[0]

    donors = connection.execute(
        "SELECT * FROM donors ORDER BY id DESC"
    ).fetchall()

    requests = connection.execute(
        "SELECT * FROM blood_requests ORDER BY id DESC"
    ).fetchall()

    connection.close()

    content = """
    <div class="container">

        <div class="page-top">
            <h1>Admin <span>Dashboard</span></h1>
            <p>Manage donors and monitor emergency blood requests.</p>
        </div>

        <section class="section">

            <div class="stats">

                <div class="stat-box">
                    <h2>{{ total_donors }}</h2>
                    <p>Total Registered Donors</p>
                </div>

                <div class="stat-box">
                    <h2>{{ total_requests }}</h2>
                    <p>Total Blood Requests</p>
                </div>

            </div>

        </section>

        <section class="section">

            <div class="section-heading">
                <h2>Registered <span>Donors</span></h2>
                <p>Donor information stored in the database.</p>
            </div>

            <div class="table-wrap">

                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Blood Group</th>
                            <th>Phone</th>
                            <th>City</th>
                            <th>Availability</th>
                        </tr>
                    </thead>

                    <tbody>

                        {% for donor in donors %}
                        <tr>
                            <td>{{ donor['id'] }}</td>
                            <td>{{ donor['name'] }}</td>
                            <td>{{ donor['blood_group'] }}</td>
                            <td>{{ donor['phone'] }}</td>
                            <td>{{ donor['city'] }}</td>
                            <td>{{ donor['available'] }}</td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="6" class="empty">
                                No donors registered yet.
                            </td>
                        </tr>
                        {% endfor %}

                    </tbody>
                </table>

            </div>

        </section>

        <section class="section">

            <div class="section-heading">
                <h2>Emergency <span>Requests</span></h2>
                <p>All submitted patient blood requirements.</p>
            </div>

            <div class="table-wrap">

                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Patient</th>
                            <th>Blood Group</th>
                            <th>Hospital</th>
                            <th>Units</th>
                            <th>City</th>
                            <th>Contact</th>
                            <th>Status</th>
                        </tr>
                    </thead>

                    <tbody>

                        {% for item in requests %}
                        <tr>
                            <td>{{ item['id'] }}</td>
                            <td>{{ item['patient_name'] }}</td>
                            <td>{{ item['blood_group'] }}</td>
                            <td>{{ item['hospital'] }}</td>
                            <td>{{ item['units'] }}</td>
                            <td>{{ item['city'] }}</td>
                            <td>{{ item['contact'] }}</td>
                            <td>{{ item['status'] }}</td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="8" class="empty">
                                No emergency requests yet.
                            </td>
                        </tr>
                        {% endfor %}

                    </tbody>
                </table>

            </div>

        </section>

    </div>
    """

    return page(
        content,
        page_title="Admin Dashboard",
        active="admin",
        total_donors=total_donors,
        total_requests=total_requests,
        donors=donors,
        requests=requests
    )

# ==========================================
# ADMIN LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ==========================================
# START FLASK APPLICATION
# ==========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
