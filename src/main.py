from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from src.model_utils import load_model, predict_price

app = FastAPI(title="API de Predicción de Precios de Coches")

model = load_model("models/modelo_coche.pkl")

class CarFeatures(BaseModel):
    Brand: str
    Model: str
    Year: int
    Engine_Size: float
    Fuel_Type: str
    Transmission: str
    Mileage: int
    Doors: int
    Owner_Count: int

@app.get("/")
async def root():
    return {
        "mensaje": "¡Bienvenido a la API de predicción de precios de coches!",
        "endpoints": {
            "/": "Página de inicio",
            "/predict": "POST para predecir precio",
            "/docs": "Documentación Swagger"
        },
        "ejemplo": {
            "Brand": "Toyota",
            "Model": "Corolla",
            "Year": 2015,
            "Engine_Size": 1.8,
            "Fuel_Type": "Petrol",
            "Transmission": "Manual",
            "Mileage": 50000,
            "Doors": 5,
            "Owner_Count": 2
        }
    }

@app.post("/predict")
async def predict(car: CarFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado correctamente")

    try:
        price = round(predict_price(model, car.model_dump()), 2)
        return {
            "input": car.model_dump(),
            "precio_predicho": price,
            "mensaje": f"El precio estimado del coche es: {price} euros"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
