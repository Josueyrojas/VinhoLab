"""Fase 1 — Carga de datos.

Orden de búsqueda:
1. CSV locales en data/raw/ (winequality-red.csv y winequality-white.csv, separador ';').
2. Descarga directa del ZIP oficial de UCI.
"""
import io
import urllib.request
import zipfile

import pandas as pd

from config import RED_CSV, WHITE_CSV, UCI_ZIP_URL, DATA_RAW, RENAME


def _descargar_uci():
    print(f"Descargando dataset desde {UCI_ZIP_URL} ...")
    with urllib.request.urlopen(UCI_ZIP_URL, timeout=60) as r:
        z = zipfile.ZipFile(io.BytesIO(r.read()))
    for nombre in ("winequality-red.csv", "winequality-white.csv"):
        with z.open(nombre) as f:
            (DATA_RAW / nombre).write_bytes(f.read())
    print("Archivos guardados en data/raw/")


def cargar_datos() -> pd.DataFrame:
    if not (RED_CSV.exists() and WHITE_CSV.exists()):
        _descargar_uci()

    tinto = pd.read_csv(RED_CSV, sep=";")
    blanco = pd.read_csv(WHITE_CSV, sep=";")
    tinto["tipo"] = "tinto"
    blanco["tipo"] = "blanco"

    df = pd.concat([tinto, blanco], ignore_index=True).rename(columns=RENAME)
    print(f"Tinto: {len(tinto):,} | Blanco: {len(blanco):,} | Total: {len(df):,} filas, {df.shape[1]} columnas")
    return df


if __name__ == "__main__":
    print(cargar_datos().head())
