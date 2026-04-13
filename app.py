# coding=utf-8

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from smbus2 import SMBus
from mlx90614 import MLX90614
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
import max30100

app = Flask(__name__)
app.secret_key = 'your_secret_key'

User_Data = "database/users.csv"
Records_Data = "database/records.csv"

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

GPIO.setwarnings(False)  # Suppress channel already in use warnings
GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering mode

hx = HX711(5, 6)  # DT, SCK pins

hx.set_reference_unit(100)  # Adjust this value!
hx.reset()
hx.tare()  # Zero the scale

mx30 = max30100.MAX30100()
mx30.enable_spo2()

def read_csv_safely(file_path, columns):
    """Read a CSV file safely, handling empty or missing files."""
    try:
        # Attempt to read the CSV file
        return pd.read_csv(file_path)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        # If the file is empty or missing, return an empty DataFrame with the correct columns
        return pd.DataFrame(columns=columns)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match. Please try again.", 400

        # Load users data
        users_df = read_csv_safely(User_Data, ['username', 'password', 'first_name', 'last_name', 'phone',
                                               'blood_group', 'medical_allergies', 'age', 'gender', 'medical_info',
                                               'alcoholic', 'smoker'])

        # Check if username exists
        if username in users_df['username'].values:
            return "Username already exists. Please try another.", 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Handle medical allergies
        medical_allergy = request.form.get('medicalAllergies')  # Dropdown selection
        other_medical_allergy = request.form.get('otherMedicalAllergy', '')  # Custom input for "Other"
        final_medical_allergy = other_medical_allergy if medical_allergy == 'Other' else medical_allergy

        # Add the new user as a list
        new_user = [
            username,
            hashed_password,
            request.form.get('firstName'),
            request.form.get('lastName'),
            request.form.get('phone'),
            request.form.get('bloodGroup'),
            final_medical_allergy,
            request.form.get('age'),
            request.form.get('gender'),
            ', '.join(request.form.getlist('medicalInfo')),
            request.form.get('alcoholic', 'No'),
            request.form.get('smoker', 'No')
        ]

        # Append the new user as a row to the DataFrame
        users_df.loc[len(users_df)] = new_user

        users_df.to_csv(User_Data, index=False)  # Save updated DataFrame

        return redirect(url_for('login'))

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Load users data
        users_df = read_csv_safely(User_Data, ['username', 'password', 'first_name', 'last_name', 'phone',
                                               'blood_group', 'medical_allergies', 'age', 'gender', 'medical_info',
                                               'alcoholic', 'smoker'])

        # Check if the username exists and the password matches
        user = users_df[users_df['username'] == username]
        if not user.empty and check_password_hash(user.iloc[0]['password'], password):
            session['username'] = username  # Store username in session
            return redirect(url_for('records'))
        elif not user.empty:
            return "Invalid password. Please try again.", 400

        return "Username does not exist. Please register first.", 400

    return render_template('login.html')

@app.route('/records', methods=['GET', 'POST'])
def records():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Load records data
    records_df = read_csv_safely(Records_Data, ['date', 'time', 'username', 'temperature', 'weight', 'oxygen_level', 'pulse_rate' 'headache', 'nausea', 'cough',
                                                'fatigue', 'cold_symptoms', 'stomach_pain', 'other', 'prescription'])

    # Filter records for the logged-in user
    user_records = records_df[records_df['username'] == session['username']].copy()
    user_records.reset_index(inplace=True)  # Keep the original index in a new column
    user_records.rename(columns={'index': 'original_index'}, inplace=True)

    # Handle actions
    action = request.args.get('action')  # Get action type (view or delete)
    record_id = request.args.get('record_id')  # Get the record ID (index)

    if action == 'delete' and record_id is not None:
        original_index = user_records.loc[int(record_id), 'original_index']  # Map to the original index
        records_df = records_df.drop(index=original_index).reset_index(drop=True)  # Remove the record
        records_df.to_csv(Records_Data, index=False)  # Save updated DataFrame
        return redirect(url_for('records'))

    if action == 'view' and record_id is not None:
        record_to_view = user_records.loc[int(record_id)].to_dict()  # Fetch the record as a dictionary
        return render_template('view_record.html', record=record_to_view)

    return render_template('records.html', records=user_records.to_dict(orient='records'))


@app.route('/symptoms', methods=['GET', 'POST']) 
def symptoms():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Load records data
    records_df = read_csv_safely(Records_Data, ['date', 'time', 'username', 'temperature', 'weight', 'oxygen_level', 'pulse_rate' 'headache', 'nausea', 'cough',
                                                'fatigue', 'cold_symptoms', 'stomach_pain', 'other', 'prescription'])

    from datetime import datetime

    if request.method == 'POST':
        # Collect form data
        symptoms_data = {
            'temperature': request.form.get('temperature'),
            'weight': request.form.get('weight'),
            'oxygen_level': request.form.get('oxygenLevel'),
            'pulse_rate': request.form.get('pulseRate'),
            'headache': request.form.get('headache'),
            'nausea': request.form.get('nausea'),
            'cough': request.form.get('cough'),
            'fatigue': request.form.get('fatigue'),
            'cold_symptoms': ', '.join(request.form.getlist('coldSymptoms')),  # Combine cold symptoms into a string
            'stomach_pain': request.form.get('stomachPain'),
            'other': request.form.get('other')
        }

        # Convert symptoms to a well-formed English sentence
        symptoms_sentence_parts = []

        for key, value in symptoms_data.items():
            if value:
                if key == 'cold_symptoms':
                    symptoms_sentence_parts.append("cold symptoms including ", value)
                elif key == 'other':
                    symptoms_sentence_parts.append("other issues like ", value)
                else:
                    symptoms_sentence_parts.append(" else ")

        symptoms_sentence = "The Patient has " + ", ".join(symptoms_sentence_parts) + "."

        # Predict using the model
        prescription = predict_prescription(symptoms_sentence)  # Replace with actual model call

        # Create a new record
        new_record = [
            datetime.now().strftime('%Y-%m-%d'),  # Date
            datetime.now().strftime('%H:%M:%S'),  # Time
            session['username'],
            symptoms_data['temperature'],
            symptoms_data['weight'],
            symptoms_data['oxygen_level'],
            symptoms_data['pulse_rate'],
            symptoms_data['headache'],
            symptoms_data['nausea'],
            symptoms_data['cough'],
            symptoms_data['fatigue'],
            symptoms_data['cold_symptoms'],
            symptoms_data['stomach_pain'],
            symptoms_data['other'],
            prescription  # Model-generated prescription
        ]

        # Append the new record to the DataFrame
        records_df.loc[len(records_df)] = new_record

        # Save the updated DataFrame to the CSV file
        records_df.to_csv(Records_Data, index=False)

        return redirect(url_for('records'))

    return render_template('symptoms.html')

@app.route('/get_measurement/<measurement_type>', methods=['GET'])
def get_measurement(measurement_type):
    # Mock data for demonstration
    temperature = (sensor.get_obj_temp() * 9 / 5) + 32
    weight = hx.get_weight()
    oxygenLevel = getoxygen()
    pulseRate = getpulse()

    measurements = {
        "temperature": temperature,
        "weight": weight,
        "oxygenLevel": oxygenLevel,
        "pulseRate": pulseRate
    }
    # Return the requested measurement
    value = measurements.get(measurement_type, "Unknown")
    return jsonify({"measurement": value})

def predict_condition(symptoms_sentence):
    condition = "Condition will be here!"
    return prescription

def getpulse():
    mx30.read_sensor()
    mx30.ir
    hb = int(mx30.ir / 100)

    return hb

def getoxygen():
    mx30.read_sensor()
    mx30.red
    hx = int(mx30.red / 100)
    return hx

if __name__ == '__main__':
    app.run(debug=True)
