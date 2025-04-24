import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def train_and_save_model(data_path: str, output_model_path: str):
    df = pd.read_csv(data_path)

    X = df.drop('Price', axis=1)
    y = df['Price']

    categorica = ['Brand', 'Model', 'Fuel_Type', 'Transmission']
    numerica = ['Year', 'Engine_Size', 'Mileage', 'Doors', 'Owner_Count']

    preprocessor = ColumnTransformer([
        ('num', 'passthrough', numerica),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorica)
    ])

    model_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model_pipeline.fit(X_train, y_train)

    print(f"✅ R² Score en test: {model_pipeline.score(X_test, y_test)}")

    with open(output_model_path, 'wb') as file:
        pickle.dump(model_pipeline, file)

    print(f"✅ Modelo guardado en {output_model_path}")

if __name__ == "__main__":
    train_and_save_model("./data/car_price_dataset.csv", "./models/modelo_coche.pkl")
