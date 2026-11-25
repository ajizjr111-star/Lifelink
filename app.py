
import os
import sqlite3
from html import escape
from flask import Flask, request, redirect, session

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "temporary-demo-key")

DB_NAME = "lifelink.db"


# Create database tables
def create_database():
    connection = sqlite3.connect(DB_NAME)

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


# Home page
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>LifeLink</title>
    </head>
    <body style="font-family:Arial;text-align:center;background:#f5f5f5;padding:30px">

        <h1 style="color:#d62828">LifeLink ❤️</h1>
        <h2>Blood Donor and Emergency Request System</h2>

        <p>Donate Blood, Save Lives!</p>

        <p><a href="/register">Become a Donor</a></p>
        <p><a href="/search">Find Blood Donors</a></p>
        <p><a href="/emergency">Emergency Blood Request</a></p>
        <p><a href="/login">Admin Login</a></p>

    </body>
    </html>
    """


# Donor registration
@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        name = request.form["name"]
        blood_group = request.form["blood_group"]
        phone = request.form["phone"]
        city = request.form["city"]

        connection = sqlite3.connect(DB_NAME)

        connection.execute("""
        INSERT INTO donors (name, blood_group, phone, city)
        VALUES (?, ?, ?, ?)
        """, (name, blood_group, phone, city))

        connection.commit()
        connection.close()

        message = "Donor registered successfully!"

    return """
    <html><body style="font-family:Arial;text-align:center;padding:30px">
    <h1>Become a Blood Donor</h1>

    <form method="POST">
    <input name="name" placeholder="Your Name" required><br><br>

    <select name="blood_group" required>
    <option value="">Select Blood Group</option>
    <option>A+</option><option>A-</option>
    <option>B+</option><option>B-</option>
    <option>O+</option><option>O-</option>
    <option>AB+</option><option>AB-</option>
    </select><br><br>

    <input name="phone" placeholder="Phone Number" required><br><br>
    <input name="city" placeholder="City" required><br><br>

    <button type="submit">Register</button>
    </form>

    <h3 style="color:green">""" + message + """</h3>
    <a href="/">Home</a>
    </body></html>
    """


# Search donors
@app.route("/search", methods=["GET", "POST"])
def search():

    donors = []

    if request.method == "POST":

        blood_group = request.form["blood_group"]
        city = request.form["city"]

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT name, blood_group, phone, city
        FROM donors
        WHERE blood_group = ?
        AND city LIKE ?
        AND available = 'Yes'
        """, (blood_group, "%" + city + "%"))

        donors = cursor.fetchall()
        connection.close()

    rows = ""

    for donor in donors:
        rows += "<tr>" + "".join(
            "<td>" + escape(str(value)) + "</td>"
            for value in donor
        ) + "</tr>"

    if request.method == "POST" and not donors:
        rows = "<tr><td colspan='4'>No donors found</td></tr>"

    return """
    <html><body style="font-family:Arial;text-align:center;padding:30px">
    <h1>Find Blood Donors</h1>

    <form method="POST">
    <select name="blood_group" required>
    <option value="">Select Blood Group</option>
    <option>A+</option><option>A-</option>
    <option>B+</option><option>B-</option>
    <option>O+</option><option>O-</option>
    <option>AB+</option><option>AB-</option>
    </select><br><br>

    <input name="city" placeholder="Enter City" required><br><br>
    <button type="submit">Search</button>
    </form>

    <h2>Search Results</h2>

    <table border="1" cellpadding="10" style="margin:auto">
    <tr><th>Name</th><th>Blood Group</th><th>Phone</th><th>City</th></tr>
    """ + rows + """
    </table>

    <br><a href="/">Home</a>
    </body></html>
    """


# Emergency blood request
@app.route("/emergency", methods=["GET", "POST"])
def emergency():

    message = ""

    if request.method == "POST":

        patient = request.form["patient_name"]
        blood = request.form["blood_group"]
        hospital = request.form["hospital"]
        units = request.form["units"]
        city = request.form["city"]
        contact = request.form["contact"]

        connection = sqlite3.connect(DB_NAME)

        connection.execute("""
        INSERT INTO blood_requests
        (patient_name, blood_group, hospital, units, city, contact)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (patient, blood, hospital, units, city, contact))

        connection.commit()
        connection.close()

        message = "Emergency request submitted successfully!"

    return """
    <html><body style="font-family:Arial;text-align:center;padding:30px">
    <h1>Emergency Blood Request</h1>

    <form method="POST">
    <input name="patient_name" placeholder="Patient Name" required><br><br>

    <select name="blood_group" required>
    <option value="">Select Blood Group</option>
    <option>A+</option><option>A-</option>
    <option>B+</option><option>B-</option>
    <option>O+</option><option>O-</option>
    <option>AB+</option><option>AB-</option>
    </select><br><br>

    <input name="hospital" placeholder="Hospital Name" required><br><br>
    <input type="number" name="units" min="1" placeholder="Units" required><br><br>
    <input name="city" placeholder="City" required><br><br>
    <input name="contact" placeholder="Contact Number" required><br><br>

    <button type="submit">Submit Request</button>
    </form>

    <h3 style="color:green">""" + message + """</h3>
    <a href="/">Home</a>
    </body></html>
    """


# Admin login
@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        correct_user = os.environ.get("ADMIN_USERNAME", "admin")
        correct_password = os.environ.get("ADMIN_PASSWORD", "admin123")

        if username == correct_user and password == correct_password:
            session["admin"] = True
            return redirect("/admin")

        message = "Invalid username or password!"

    return """
    <html><body style="font-family:Arial;text-align:center;padding:30px">
    <h1>Admin Login</h1>

    <form method="POST">
    <input name="username" placeholder="Username" required><br><br>
    <input type="password" name="password" placeholder="Password" required><br><br>
    <button type="submit">Login</button>
    </form>

    <p style="color:red">""" + message + """</p>
    <a href="/">Home</a>
    </body></html>
    """


# Protect admin dashboard
@app.before_request
def check_admin():

    if request.path in ["/admin", "/logout"]:
        if not session.get("admin"):
            return redirect("/login")


# Admin dashboard
@app.route("/admin")
def admin():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM blood_requests")
    total_requests = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()

    cursor.execute("SELECT * FROM blood_requests")
    requests_data = cursor.fetchall()

    connection.close()

    donor_rows = ""

    for donor in donors:
        donor_rows += "<tr>" + "".join(
            "<td>" + escape(str(value)) + "</td>"
            for value in donor
        ) + "</tr>"

    request_rows = ""

    for item in requests_data:
        request_rows += "<tr>" + "".join(
            "<td>" + escape(str(value)) + "</td>"
            for value in item
        ) + "</tr>"

    return """
    <html><body style="font-family:Arial;padding:30px">
    <h1 style="color:#d62828">LifeLink Admin Dashboard</h1>

    <h2>Total Donors: """ + str(total_donors) + """</h2>
    <h2>Total Emergency Requests: """ + str(total_requests) + """</h2>

    <h2>Donor Details</h2>
    <table border="1" cellpadding="8">
    <tr><th>ID</th><th>Name</th><th>Blood Group</th><th>Phone</th><th>City</th><th>Available</th></tr>
    """ + donor_rows + """
    </table>

    <h2>Emergency Requests</h2>
    <table border="1" cellpadding="8">
    <tr><th>ID</th><th>Patient</th><th>Blood Group</th><th>Hospital</th><th>Units</th><th>City</th><th>Contact</th><th>Status</th></tr>
    """ + request_rows + """
    </table>

    <br><a href="/logout">Logout</a>
    </body></html>
    """


# Admin logout
@app.route("/logout")
def logout():

    session.pop("admin", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


# LifeLink professional design upgrade

@app.after_request
def add_lifelink_design(response):
    if response.content_type and "text/html" in response.content_type:
        html = response.get_data(as_text=True)
        if "</head>" in html:
            html = html.replace("</head>", '\n<style>\n* {\n    box-sizing: border-box;\n}\n\nbody {\n    margin: 0;\n    padding: 30px 18px;\n    font-family: \'Segoe UI\', Arial, sans-serif;\n    background: #fff5f5 !important;\n    color: #252525;\n    line-height: 1.6;\n}\n\nh1, h2, h3 {\n    color: #b5122b !important;\n    font-weight: 750;\n}\n\nh1 {\n    font-size: 38px;\n}\n\na, button, input[type="submit"] {\n    transition: 0.25s ease;\n}\n\na {\n    color: #c1122f;\n    font-weight: 600;\n}\n\na:hover {\n    color: #850019;\n}\n\nbutton, input[type="submit"] {\n    background: #c1122f !important;\n    color: white !important;\n    border: none !important;\n    border-radius: 9px !important;\n    padding: 12px 22px !important;\n    cursor: pointer;\n    font-weight: 700;\n}\n\nbutton:hover, input[type="submit"]:hover {\n    background: #850019 !important;\n    transform: translateY(-2px);\n}\n\ninput, select, textarea {\n    width: 100%;\n    max-width: 450px;\n    padding: 12px !important;\n    margin: 8px 0 16px;\n    border: 1px solid #e4bfc5 !important;\n    border-radius: 8px !important;\n    background: white;\n}\n\ntable {\n    width: 100%;\n    border-collapse: collapse;\n    background: white;\n    border-radius: 12px;\n    overflow: hidden;\n}\n\nth {\n    background: #c1122f;\n    color: white;\n    padding: 14px;\n}\n\ntd {\n    padding: 12px;\n    border-bottom: 1px solid #eee;\n}\n\ntr:hover {\n    background: #fff0f2;\n}\n\nform {\n    background: white;\n    padding: 24px;\n    border-radius: 14px;\n    box-shadow: 0 5px 22px rgba(120, 0, 25, 0.08);\n}\n\n</style>\n' + "</head>", 1)
            response.set_data(html)
    return response
