import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import joblib

# Load and preprocess the dataset
data = pd.read_csv('more_extended_disease_symptoms.csv')
X = data.drop(columns=['disease'])
y = data['disease']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the KNN model
model = KNeighborsClassifier(n_neighbors=2,weights='distance',metric='manhattan')  # You can experiment with this value
model.fit(X_scaled, y)

# Save the trained model and the scaler
joblib.dump(model, 'disease_prediction_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
