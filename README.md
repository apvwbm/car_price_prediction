# 🚗 API de Predicción de Precios de Coches

API REST construida con **FastAPI** para estimar el precio de un coche según sus características. Utiliza un modelo de *machine learning* basado en **Random Forest**, entrenado con datos reales.

---

## 📁 Estructura del proyecto

```
car_price_prediction/
├── data/                     # Datos originales (CSV, etc.)
│   └── car_price_dataset.csv
│
├── models/                   # Modelos entrenados (.pkl)
│   └── modelo_coche.pkl
│
├── notebooks/                # Notebooks de pruebas o análisis
│   ├── Notebook_pruebas.ipynb
│   └── Practica_Grupal_Despliegue.ipynb
│
├── src/                      # Código fuente del proyecto
│   ├── __init__.py
│   ├── main.py               # API con FastAPI
│   ├── model_utils.py        # Funciones de predicción y carga de modelo
│   └── training.py           # Entrenamiento del modelo
│
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo 🙂
└── .gitignore                # Archivos y carpetas ignorados por Git
```

---

## ⚙️ Requisitos

Se recomienda crear un **entorno virtual** antes de instalar las dependencias:

```bash
python -m venv venv
source venv/bin/activate      # En Mac/Linux
source venv/Scripts/activate  # En Windows
```

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

---

## 🚀 ¿Cómo usar?

### 1. Entrenar el modelo (opcional si ya existe `models/modelo_coche.pkl`):

```bash
python src/training.py
```

Esto entrenará el modelo usando los datos en `data/car_price_dataset.csv` y lo guardará en `models/modelo_coche.pkl`.

---

### 2. Lanzar la API:

```bash
uvicorn src.main:app --reload
```

Luego accede a:

- [http://localhost:8000](http://localhost:8000) → Página de bienvenida
- [http://localhost:8000/docs](http://localhost:8000/docs) → Swagger UI (documentación interactiva)

---

## 🧪 Ejemplo de entrada (JSON)

```json
{
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
```

---

## 📦 Endpoints

- `GET /` → Página de inicio con info general
- `POST /predict` → Devuelve el precio estimado
- `GET /docs` → Swagger para pruebas y documentación

---

## 👥 Autor

**Team Leviathan**