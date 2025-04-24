import pickle
import pandas as pd

def load_model(path: str):
    try:
        with open(path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("⚠️ Modelo no encontrado")
        return None

def predict_price(model, input_dict):
    df = pd.DataFrame([input_dict])
    return float(model.predict(df)[0])
