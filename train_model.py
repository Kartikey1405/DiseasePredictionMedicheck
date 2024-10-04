import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Load and preprocess the dataset
data = pd.read_csv('more_extended_disease_symptoms.csv')
X = data.drop(columns=['disease'])
y = data['disease']

# Train the KNN model
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'disease_prediction_model.pkl')
