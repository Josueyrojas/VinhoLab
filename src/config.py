"""Configuración central del proyecto: rutas, columnas y parámetros."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
FIG_DIR = ROOT / "outputs" / "figuras"
TAB_DIR = ROOT / "outputs" / "tablas"
MODEL_DIR = ROOT / "outputs" / "modelos"

for d in (DATA_RAW, DATA_PROCESSED, FIG_DIR, TAB_DIR, MODEL_DIR):
    d.mkdir(parents=True, exist_ok=True)

RED_CSV = DATA_RAW / "winequality-red.csv"
WHITE_CSV = DATA_RAW / "winequality-white.csv"
UCI_ZIP_URL = "https://archive.ics.uci.edu/static/public/186/wine+quality.zip"

# Nombres compatibles con SPSS (sin espacios, <= 64 caracteres)
RENAME = {
    "fixed acidity": "fixed_acidity",
    "volatile acidity": "volatile_acidity",
    "citric acid": "citric_acid",
    "residual sugar": "residual_sugar",
    "chlorides": "chlorides",
    "free sulfur dioxide": "free_sulfur_dioxide",
    "total sulfur dioxide": "total_sulfur_dioxide",
    "density": "density",
    "pH": "pH",
    "sulphates": "sulphates",
    "alcohol": "alcohol",
    "quality": "quality",
}

FEATURES = [v for v in RENAME.values() if v != "quality"]
TARGET = "quality"

# Etiquetas en español para gráficas y tablas
ETIQUETAS = {
    "fixed_acidity": "Acidez fija",
    "volatile_acidity": "Acidez volátil",
    "citric_acid": "Ácido cítrico",
    "residual_sugar": "Azúcar residual",
    "chlorides": "Cloruros",
    "free_sulfur_dioxide": "SO2 libre",
    "total_sulfur_dioxide": "SO2 total",
    "density": "Densidad",
    "pH": "pH",
    "sulphates": "Sulfatos",
    "alcohol": "Alcohol",
    "quality": "Calidad",
}

# Categorías de calidad: baja (<=5), media (6), alta (>=7)
BINS_CALIDAD = [0, 5, 6, 10]
LABELS_CALIDAD = ["baja", "media", "alta"]
UMBRAL_BUEN_VINO = 7  # para clasificación binaria

ALPHA = 0.05
RANDOM_STATE = 42
