import csv
import os
import hashlib
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from model import AirlineEnvironment, QLearningAgent
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Database setup (SQLite)
DATABASE = 'user_data.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT)')
        db.commit()

# Initialize database
init_db()

# Function to write data to any CSV file
def write_to_csv(filename, data):
    try:
        # Ensure the directory exists
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        
        # Open the file in append mode to avoid overwriting
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
            logging.debug(f"Data written: {data}")
    except Exception as e:
        logging.error(f"Error writing to CSV: {e}")

# Function to read data from CSV
def read_from_csv(filename):
    data = []
    try:
        if os.path.exists(filename):
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    data.append(row)
            logging.debug(f"Data read: {data}")
        else:
            logging.warning(f"File {filename} not found.")
    except Exception as e:
        logging.error(f"Error reading from CSV: {e}")
    return data

@app.route('/')
def index():
    if 'username' in session:
        routes = ['Route 1', 'Route 2', 'Route 3']  # Example route list
        return render_template('index.html', routes=routes)
    return redirect(url_for('sign_in'))  # Redirect to sign-in page if not signed in

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):
            session['username'] = username  # Store username in session
            return redirect(url_for('index'))  # Redirect to dashboard
        else:
            error = "Invalid credentials, please try again."
            return render_template('sign-in.html', error=error)
    return render_template('sign-in.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        db.commit()
        return redirect(url_for('sign_in'))
    
    return render_template('sign-up.html')

@app.route('/train_agent', methods=['POST'])
def train_agent():
    episodes = int(request.form['episodes'])
    agent = QLearningAgent(AirlineEnvironment())
    agent.train(episodes=episodes)
    return jsonify({"message": "Training completed!"})

@app.route('/get_dynamic_price', methods=['GET'])
def get_dynamic_price():
    try:
        feature_idx = int(request.args.get('feature_idx'))
        agent = QLearningAgent(AirlineEnvironment())
        state = agent.env.reset()
        action = agent.choose_action(state)
        next_state, reward, done = agent.env.step(action)
        dynamic_price = agent.env.base_price + agent.env.get_feature_price()

        # Write dynamic price and reward to CSV (in this case, using 'data.csv')
        write_to_csv('data.csv', [feature_idx, dynamic_price, reward])

        return jsonify({"dynamic_price": dynamic_price, "reward": reward})

    except Exception as e:
        logging.error(f"Error in get_dynamic_price: {e}")
        return jsonify({"error": "An error occurred while getting dynamic price."}), 500

@app.route('/analyze_revenue_expense', methods=['POST'])
def analyze_revenue_expense():
    try:
        # Sample revenue and expense analysis results
        analysis = "Revenue and Expense analysis results."

        # Write analysis results to CSV (in this case, using 'data.csv')
        write_to_csv('data.csv', [analysis])

        return jsonify({"analysis": analysis})

    except Exception as e:
        logging.error(f"Error in analyze_revenue_expense: {e}")
        return jsonify({"error": "An error occurred during analysis."}), 500

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Read data from 'data.csv' to display on frontend
        data = read_from_csv('data.csv')
        return jsonify({"data": data})

    except Exception as e:
        logging.error(f"Error in get_data: {e}")
        return jsonify({"error": "An error occurred while reading data."}), 500

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('sign_in'))  # Redirect to sign-in page

if __name__ == "__main__":
    app.run(debug=True)
