from flask import Flask, render_template, request
import os
import mysql.connector
from vehicle_detect import process_video

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- UPLOAD VIDEO ----------------
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["video"]

    if file:

        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)

        result = process_video(path)

        return f"""
        <html>
        <body style="text-align:center; font-family:Arial; margin-top:50px;">
            <h2>🚦 Processing Completed</h2>
            <p>{result}</p>
            <br><br>
            <a href="/">Go Back</a>
        </body>
        </html>
        """

    return "No file uploaded"


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Magi@123",
        database="noparking"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT vehicle_number, entry_time, exit_time, fine_amount, status 
        FROM violations
    """)
    data = cursor.fetchall()

    conn.close()

    html = """
    <html>
    <body style="font-family:Arial; text-align:center;">
        <h2>🚦 Violations Dashboard</h2>

        <table border="1" cellpadding="10" style="margin:auto;">
            <tr>
                <th>Vehicle</th>
                <th>Entry Time</th>
                <th>Exit Time</th>
                <th>Fine</th>
                <th>Status</th>
            </tr>
    """

    for row in data:
        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
        </tr>
        """

    html += """
        </table>
        <br><br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """

    return html


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    print("Flask starting...")
    app.run(debug=True)