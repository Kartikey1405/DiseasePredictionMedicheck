import joblib
import pandas as pd
import numpy as np

def load_model():
    model = joblib.load('disease_prediction_model.pkl')
    scaler = joblib.load('scaler.pkl')  # Load the scaler
    data = pd.read_csv('more_extended_disease_symptoms.csv')
    symptom_columns = data.columns[:-1]
    return model, scaler, symptom_columns

def preprocess_symptoms(symptoms, symptom_columns):
    input_data = np.zeros(len(symptom_columns))
    for symptom in symptoms:
        if symptom in symptom_columns:
            index = symptom_columns.get_loc(symptom)
            input_data[index] = 1
    return input_data

def predict_disease(symptoms):
    model, scaler, symptom_columns = load_model()
    input_data = preprocess_symptoms(symptoms, symptom_columns)
    
    # Scale the input data
    input_data_scaled = scaler.transform([input_data])
    
    probabilities = model.predict_proba(input_data_scaled)  # Get probabilities
    
    # Get top 2 predictions
    top_2_indices = np.argsort(probabilities[0])[-2:][::-1]  # Sort and get top 3
    top_2_diseases = []
    
    for index in top_2_indices:
        disease_name = model.classes_[index]
        probability = probabilities[0][index] * 100  # Convert to percentage
        top_diseases.append((disease_name, f"{probability:.0f}%"))  # Format as integer percentage
    
    return top_2_diseases
