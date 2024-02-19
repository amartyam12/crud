import psycopg2
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from main_data import Experience, Employee

app = Flask(__name__)

# Set up the PostgreSQL connection details
hostname = 'localhost'
database = 'database'
username = 'postgres'
pwd = 'qwerty'
port_id = '5432'

# Create the connection to the PostgreSQL database
conn = psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=port_id
)
conn.autocommit = True
cur = conn.cursor()

MAX_NAME_LENGTH = 100
MAX_PHONE_LENGTH = 20
MAX_EMAIL_LENGTH = 100
MAX_PASSWORD_LENGTH = 100

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')

        # Validate input lengths
        if len(name) > MAX_NAME_LENGTH or len(phone) > MAX_PHONE_LENGTH or len(email) > MAX_EMAIL_LENGTH or len(password) > MAX_PASSWORD_LENGTH:
            return jsonify({'error': 'Input values too long'}), 400

        # Check if email already exists
        cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({'error': 'Email already exists'}), 400

        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO employee (name, phone, email, password, status, created_on) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, phone, email, password, 'active', datetime.now()))

        return jsonify({'message': 'Employee registered successfully'})
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Database error'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
        employee = cur.fetchone()
        if employee and (employee[4] == password):
            return jsonify({'message': 'Employee logged in successfully'})
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Database error'}), 500

@app.route('/experience', methods=['POST','GET'])
def experience():
    try:
        data = request.json
        employee_id = data.get('employee_id')
        company_name = data.get('company_name')
        role = data.get('role')
        date_of_joining = data.get('date_of_joining')
        last_date = data.get('last_date')

        # if request.methods == "GET":

        cur.execute("INSERT INTO experience (employee_id, company_name, role, date_of_joining, last_date) VALUES (%s, %s, %s, %s, %s)",
                    (employee_id, company_name, role, date_of_joining, last_date))

        return jsonify({'message': 'Experience added successfully'})
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Database error'}), 500

@app.route('/update', methods=['PUT'])
def update():
    try:
        data = request.json
        employee_id = data.get('employee_id')
        company_name = data.get('company_name')
        role = data.get('role')
        date_of_joining = data.get('date_of_joining')
        last_date = data.get('last_date')

        cur.execute("UPDATE experience SET company_name = %s, role = %s, date_of_joining = %s, last_date = %s WHERE employee_id = %s",
                    (company_name, role, date_of_joining, last_date, employee_id))
        
        if cur.rowcount > 0:
            return jsonify({'message': 'Experience updated successfully'})
        else:
            return "Nothing to update"
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Database error'}), 500

@app.route('/login_get', methods=['GET'])
def login_get():
    try:
        data = request.json
        email = data.get('email')  # Retrieve email from query parameters
        password = data.get('password')  # Retrieve password from query parameters

        cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
        employee = cur.fetchone()

        if employee and employee[4] == password:
            return (f"message: okay , Name :{employee[1]}, Phone_no : {employee[2]}")  # Return message indicating successful login
        
        return "Invalid email or password", 401  # Return message indicating login failure
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Database error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
