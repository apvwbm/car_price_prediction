from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from typing import Optional

from src.model_utils import load_model, predict_price

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="API de Predicción de Precios de Coches")

# Cargar el modelo
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "..", "models", "modelo_coche.pkl")
model = load_model(model_path)

# Configurar Jinja2 para plantillas HTML
templates = Jinja2Templates(directory="templates")

# Clase para los datos del coche
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

# Endpoint raíz: muestra la plantilla con los valores por defecto
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    default_values = {
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
    return templates.TemplateResponse("index.html", {
        "request": request,
        "defaults": default_values
    })
    
@app.get("/info")
async def info():
    return {
        "mensaje": "API de Predicción de Precios de Coches",
        "endpoints": {
            "/": "Landing page con formulario HTML",
            "/predict (POST)": "Recibe un formulario o JSON con los datos del coche y devuelve el precio estimado",
            "/predict (GET)": "Recibe parámetros por URL y devuelve la predicción (ideal para usar con requests.get)",
            "/info": "Información sobre los endpoints disponibles"
        },
        "ejemplo_get": "/predict?Brand=Toyota&Model=Corolla&Year=2015&Engine_Size=1.8&Fuel_Type=Petrol&Transmission=Manual&Mileage=50000&Doors=5&Owner_Count=2"
    }
    
# @app.get("/secret")
# async def secret():
#     return {"mensaje": "Este endpoint ha sido activado tras el redespliegue"}
    
@app.get("/predict")
async def predict_get(
    Brand: str,
    Model: str,
    Year: int,
    Engine_Size: float,
    Fuel_Type: str,
    Transmission: str,
    Mileage: int,
    Doors: int,
    Owner_Count: int
):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado correctamente")

    try:
        car_data = {
            "Brand": Brand,
            "Model": Model,
            "Year": Year,
            "Engine_Size": Engine_Size,
            "Fuel_Type": Fuel_Type,
            "Transmission": Transmission,
            "Mileage": Mileage,
            "Doors": Doors,
            "Owner_Count": Owner_Count
        }
        price = round(predict_price(model, car_data), 2)
        return {
            "input": car_data,
            "precio_predicho": price,
            "mensaje": f"El precio estimado del coche es: {price} euros"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {e}")


# Endpoint para predecir el precio
@app.post("/predict")
async def predict(
    Brand: str = Form(...),
    Model: str = Form(...),
    Year: int = Form(...),
    Engine_Size: float = Form(...),
    Fuel_Type: str = Form(...),
    Transmission: str = Form(...),
    Mileage: int = Form(...),
    Doors: int = Form(...),
    Owner_Count: int = Form(...)
):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado correctamente")

    try:
        car_data = {
            "Brand": Brand,
            "Model": Model,
            "Year": Year,
            "Engine_Size": Engine_Size,
            "Fuel_Type": Fuel_Type,
            "Transmission": Transmission,
            "Mileage": Mileage,
            "Doors": Doors,
            "Owner_Count": Owner_Count
        }

        price = round(predict_price(model, car_data), 2)
        return {
            "input": car_data,
            "precio_predicho": price,
            "mensaje": f"El precio estimado del coche es: {price} euros"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {e}")

# Iniciar el servidor si se ejecuta directamente
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
