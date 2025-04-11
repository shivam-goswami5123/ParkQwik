import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Load data
df = pd.read_csv("data.csv")

# Convert 'Time' to hour-only format (numeric)
df['Hour'] = pd.to_datetime(df['Time'], format="%H:%M").dt.hour

# Encode categorical variable 'Weather' using Label Encoding
le = LabelEncoder()
df['Weather'] = le.fit_transform(df['Weather'])

# Select Features (X) and Target (y)
X = df[['Hour', 'Temperature (°C)', 'Jam Factor', 'Weather']]  # Features
y = df['Vacant Spots']  # Target variable

# Split Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on Test Data
y_pred = model.predict(X_test)

# Evaluate Model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R² Score: {r2:.2f}")

# Predict Vacant Spots for a specific time (Example: 10 AM, 25°C, Jam Factor = 5, Weather = 'Clear')
sample_input = np.array([[10, 25, 5, le.transform(['Clear'])[0]]])
predicted_spots = model.predict(sample_input)
print(f"Predicted Vacant Spots at 10 AM: {predicted_spots[0]:.2f}")
