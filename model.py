import joblib
import pandas as pd
import numpy as np

def load_model():
    model = joblib.load('disease_prediction_model.pkl')
    data = pd.read_csv('disease_symptoms.csv')
    symptom_columns = data.columns[:-1]
    return model, symptom_columns

def preprocess_symptoms(symptoms, symptom_columns):
    input_data = np.zeros(len(symptom_columns))
    for symptom in symptoms:
        if symptom in symptom_columns:
            index = symptom_columns.get_loc(symptom)
            input_data[index] = 1
    return input_data
