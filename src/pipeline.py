import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

# Cargar los datos
df = pd.read_csv('./data/car_price_dataset.csv')

# Dividir features y target
X = df.drop('Price', axis=1)
y = df['Price']

# Identificar columnas categóricas y numéricas
categorica = ['Brand', 'Model', 'Fuel_Type', 'Transmission']
numerica = ['Year', 'Engine_Size', 'Mileage', 'Doors', 'Owner_Count']

# Crear preprocesadores
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerica),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorica)
    ])

# Crear pipeline con preprocesador y modelo
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Dividir en train y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model_pipeline.fit(X_train, y_train)

# Evaluar el modelo
score = model_pipeline.score(X_test, y_test)
print(f"R² Score: {score}")

# Guardar el modelo entrenado
with open('../models/modelo_coche.pkl', 'wb') as file:
    pickle.dump(model_pipeline, file)

print("Modelo guardado correctamente como 'modelo_coche.pkl' en la carpeta 'models'")