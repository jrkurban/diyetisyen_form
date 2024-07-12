from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# JSON dosya yolu
DATA_FILE = 'hasta_listesi.json'


# JSON dosyasını oku
def read_patients():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []


# JSON dosyasına yaz
def write_patients(patients):
    with open(DATA_FILE, 'w') as file:
        json.dump(patients, file, indent=4)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    age = request.form.get('age')
    height = request.form.get('height')
    weight = request.form.get('weight')
    gender = request.form.get('gender')
    medical_conditions = request.form.get('medical_conditions')
    last_3_day = request.form.get('last_3_day')

    patient = {
        'name': name,
        'age': age,
        'height': height,
        'weight': weight,
        'gender': gender,
        'medical_conditions': medical_conditions,
        'last_3_day': last_3_day,
        'weights': [{'date': str(datetime.now()), 'weight': weight}]
    }

    patients = read_patients()
    patients.append(patient)
    write_patients(patients)

    return redirect(url_for('patient_list'))


@app.route('/patients')
def patient_list():
    patients = read_patients()
    return render_template('patient_list.html', patients=patients)


@app.route('/profile/<int:index>')
def profile(index):
    patients = read_patients()
    if 0 <= index < len(patients):
        patient = patients[index]
        return render_template('profile.html', patient=patient, index=index)
    return redirect(url_for('patient_list'))


@app.route('/graph/<int:index>')
def patient_graph(index):
    patients = read_patients()
    if 0 <= index < len(patients):
        patient = patients[index]
        return render_template('patient_graph.html', patient=patient, index=index)
    return redirect(url_for('patient_list'))


@app.route('/update_weight/<int:index>', methods=['POST'])
def update_weight(index):
    new_weight = request.form.get('weight')
    new_date = request.form.get('date')
    patients = read_patients()
    if 0 <= index < len(patients):
        patient = patients[index]
        patient['weights'].append({'date': new_date, 'weight': new_weight})
        write_patients(patients)
    return redirect(url_for('patient_graph', index=index))


@app.route('/delete/<int:index>', methods=['POST'])
def delete_patient(index):
    patients = read_patients()
    if 0 <= index < len(patients):
        del patients[index]
        write_patients(patients)
    return redirect(url_for('patient_list'))


if __name__ == '__main__':
    app.run(debug=True)
