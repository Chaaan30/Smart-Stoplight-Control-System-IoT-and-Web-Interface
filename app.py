# app.py

from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Function to connect to MySQL
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="final_mp"  # Replace with your database name
    )

# Function to fetch stoplight data
def get_stoplight_data():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, stat, color FROM stoplight_state")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Function to update stoplight state
def update_stoplight_state(stoplight_id, new_stat):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE stoplight_state SET stat = %s WHERE id = %s", (new_stat, stoplight_id))
    conn.commit()
    conn.close()

# Function to get admin passcode
def get_admin_passcode():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT passcode FROM admin LIMIT 1")  # Assuming there's only one passcode in admin table
    passcode = cursor.fetchone()[0]  # Fetching the passcode value
    cursor.close()
    conn.close()
    return passcode

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    stoplight_data = get_stoplight_data()
    return render_template('dashboard.html', stoplight_data=stoplight_data)

@app.route('/controls')
def controls():
    stoplight_data = get_stoplight_data()
    return render_template('controls.html', stoplight_data=stoplight_data)

@app.route('/check_passcode', methods=['POST'])
def check_passcode():
    passcode_entered = request.form.get('passcodeInput')
    passcode_admin = get_admin_passcode()

    if passcode_entered == passcode_admin:
        return redirect(url_for('controls'))
    else:
        return "Invalid passcode. Please try again."

@app.route('/update_stat', methods=['POST'])
def update_stat():
    stoplight_id = request.form['stoplight_id']
    new_stat = request.form['new_stat']

    try:
        update_stoplight_state(stoplight_id, new_stat)
        return redirect(url_for('controls'))  # Redirect to controls page after update
    except Exception as e:
        return "Failed to update stoplight state: " + str(e)

if __name__ == '__main__':
    app.run(debug=True)
