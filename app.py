from flask import Flask, request, jsonify, render_template
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import os
import pandas as pd
import json
from model import preprocess_symptoms, load_model
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow CORS for all origins and headers

# Cloudant credentials
cloudant_api_key = 'ltTkC89cPIvv7sNHJ4J5f7x-WeQQYy9FcrEKJBsIsvAk'
cloudant_url = 'https://2951e918-b4d6-4a70-96f6-b1237506cac7-bluemix.cloudantnosqldb.appdomain.cloud'

# Connect to Cloudant service
client = Cloudant.iam(None, cloudant_api_key, url=cloudant_url)
client.connect()

# Connect to the database
database_name = 'healthcare_db'
db = client.create_database(database_name, throw_on_exists=False)

# Function to upload dataset to Cloudant
def upload_dataset_to_cloudant():
    try:
        data = pd.read_csv('more_extended_disease_symptoms.csv')
        documents = data.to_dict(orient='records')
        result = db.bulk_docs(documents)
        if all(result):
            print(f"Dataset uploaded successfully to Cloudant. Total {len(documents)} documents.")
        else:
            print("Failed to upload dataset to Cloudant.")
    except Exception as e:
        print(f"Error uploading dataset to Cloudant: {e}")

# Load the trained model
model, symptom_columns = load_model()

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/predict-disease', methods=['POST'])
def predict_disease():
    symptoms = request.json.get('symptoms')
    input_data = preprocess_symptoms(symptoms, symptom_columns)
    prediction = model.predict([input_data])

    # Store the consultation in Cloudant
    try:
        data = {
            'symptoms': symptoms,
            'predicted_disease': prediction[0]
        }
        new_document = db.create_document(data)
        if new_document.exists():
            return jsonify({'disease': prediction[0]})
        else:
            return jsonify({'error': 'Failed to store consultation data'})
    except CloudantException as e:
        return jsonify({'error': f'Cloudant error: {e}'})

if __name__ == '__main__':
    upload_dataset_to_cloudant()
    app.run(port=5000)
