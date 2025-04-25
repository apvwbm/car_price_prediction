from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import pandas as pd
import os
import sys

from src.model_utils import load_model, predict_price

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="API de Predicción de Precios de Coches")

# Cargar el modelo
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "..", "models", "modelo_coche.pkl")
model = load_model(model_path)

# Configurar Jinja2
templates = Jinja2Templates(directory="templates")

# Modelo de entrada
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

# Para comparación (si lo activas más adelante)
class CompareRequest(BaseModel):
    car1: CarFeatures
    car2: CarFeatures

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.api_route("/predict", methods=["GET", "POST"], response_class=HTMLResponse)
async def predict_view(
    request: Request,
    Brand: str = Form(None),
    Model: str = Form(None),
    Year: int = Form(None),
    Engine_Size: float = Form(None),
    Fuel_Type: str = Form(None),
    Transmission: str = Form(None),
    Mileage: int = Form(None),
    Doors: int = Form(None),
    Owner_Count: int = Form(None),
):
    defaults = {
        "Brand": Brand or "Toyota",
        "Model": Model or "Corolla",
        "Year": Year or 2015,
        "Engine_Size": Engine_Size or 1.8,
        "Fuel_Type": Fuel_Type or "Petrol",
        "Transmission": Transmission or "Manual",
        "Mileage": Mileage or 50000,
        "Doors": Doors or 5,
        "Owner_Count": Owner_Count or 2
    }

    prediction_text = None
    if request.method == "POST":
        try:
            data = {
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
            price = round(predict_price(model, data), 2)
            prediction_text = f"El precio estimado del coche es de {price} €"
        except Exception as e:
            prediction_text = f"⚠️ Error: {e}"

    return templates.TemplateResponse("predict.html", {
        "request": request,
        "defaults": defaults,
        "prediction_text": prediction_text
    })

@app.post("/predict_json")
async def predict_json(car: CarFeatures):
    try:
        data = car.dict()
        price = round(predict_price(model, data), 2)
        return {"predicted_price": price, "currency": "EUR"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.api_route("/compare", methods=["GET", "POST"], response_class=HTMLResponse)
async def compare_view(
    request: Request,
    Brand1: str = Form(None),
    Model1: str = Form(None),
    Year1: int = Form(None),
    Engine_Size1: float = Form(None),
    Fuel_Type1: str = Form(None),
    Transmission1: str = Form(None),
    Mileage1: int = Form(None),
    Doors1: int = Form(None),
    Owner_Count1: int = Form(None),

    Brand2: str = Form(None),
    Model2: str = Form(None),
    Year2: int = Form(None),
    Engine_Size2: float = Form(None),
    Fuel_Type2: str = Form(None),
    Transmission2: str = Form(None),
    Mileage2: int = Form(None),
    Doors2: int = Form(None),
    Owner_Count2: int = Form(None)
):
    defaults1 = {
        "Brand": Brand1 or "Toyota",
        "Model": Model1 or "Corolla",
        "Year": Year1 or 2018,
        "Engine_Size": Engine_Size1 or 1.8,
        "Fuel_Type": Fuel_Type1 or "Hybrid",
        "Transmission": Transmission1 or "Automatic",
        "Mileage": Mileage1 or 40000,
        "Doors": Doors1 or 5,
        "Owner_Count": Owner_Count1 or 1
    }

    defaults2 = {
        "Brand": Brand2 or "Ford",
        "Model": Model2 or "Focus",
        "Year": Year2 or 2016,
        "Engine_Size": Engine_Size2 or 1.5,
        "Fuel_Type": Fuel_Type2 or "Diesel",
        "Transmission": Transmission2 or "Manual",
        "Mileage": Mileage2 or 60000,
        "Doors": Doors2 or 5,
        "Owner_Count": Owner_Count2 or 2
    }

    prediction_result = None
    if request.method == "POST":
        try:
            price1 = round(predict_price(model, defaults1), 2)
            price2 = round(predict_price(model, defaults2), 2)
            prediction_result = {
                "car1": defaults1,
                "price1": price1,
                "car2": defaults2,
                "price2": price2,
                "mas_caro": "Coche 1" if price1 > price2 else "Coche 2",
                "diferencia": round(abs(price1 - price2), 2)
            }
        except Exception as e:
            prediction_result = {"error": f"⚠️ Error: {e}"}

    return templates.TemplateResponse("compare.html", {
        "request": request,
        "defaults1": defaults1,
        "defaults2": defaults2,
        "resultado": prediction_result
    })

@app.post("/compare_json")
async def compare_json(request: CompareRequest):
    try:
        data1 = request.car1.dict()
        data2 = request.car2.dict()

        price1 = round(predict_price(model, data1), 2)
        price2 = round(predict_price(model, data2), 2)

        return {
            "car1": {"features": data1, "price": price1},
            "car2": {"features": data2, "price": price2},
            "mas_caro": "car1" if price1 > price2 else "car2",
            "diferencia": round(abs(price1 - price2), 2),
            "currency": "EUR"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Ejecutar servidor si es run directo
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
