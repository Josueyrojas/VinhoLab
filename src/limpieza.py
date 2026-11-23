"""Fase 2 — Tratamiento de datos.

- Revisión de tipos y valores faltantes
- Eliminación de duplicados
- Detección de outliers (IQR y z-score)
- Winsorización opcional (recorte a percentiles 1–99)
- Variables derivadas: categoría de calidad, buen_vino, tipo_num
- Normalización (z-score) para modelado
- Exportación a CSV para SPSS
"""
import numpy as np
import pandas as pd

from config import (FEATURES, TARGET, BINS_CALIDAD, LABELS_CALIDAD,
                    UMBRAL_BUEN_VINO, DATA_PROCESSED, TAB_DIR)


def reporte_calidad_datos(df: pd.DataFrame) -> pd.DataFrame:
    rep = pd.DataFrame({
        "tipo_dato": df.dtypes.astype(str),
        "nulos": df.isna().sum(),
        "pct_nulos": (df.isna().mean() * 100).round(2),
        "valores_unicos": df.nunique(),
    })
    rep.to_csv(TAB_DIR / "01_calidad_datos.csv")
    return rep


def outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for col in FEATURES:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        li, ls = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_iqr = ((df[col] < li) | (df[col] > ls)).sum()
        z = (df[col] - df[col].mean()) / df[col].std()
        n_z = (z.abs() > 3).sum()
        filas.append({"variable": col, "lim_inf": li, "lim_sup": ls,
                      "outliers_IQR": n_iqr, "pct_IQR": round(n_iqr / len(df) * 100, 2),
                      "outliers_z>3": n_z})
    out = pd.DataFrame(filas)
    out.to_csv(TAB_DIR / "02_outliers.csv", index=False)
    return out


def winsorizar(df: pd.DataFrame, p_inf=0.01, p_sup=0.99) -> pd.DataFrame:
    df = df.copy()
    for col in FEATURES:
        lo, hi = df[col].quantile([p_inf, p_sup])
        df[col] = df[col].clip(lo, hi)
    return df


def limpiar(df: pd.DataFrame, aplicar_winsor: bool = True) -> pd.DataFrame:
    print("\n=== FASE 2: LIMPIEZA ===")
    print(reporte_calidad_datos(df))

    n0 = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Duplicados eliminados: {n0 - len(df):,} (quedan {len(df):,})")

    out = outliers_iqr(df)
    print(out.to_string(index=False))
    df.attrs["resumen_limpieza"] = {
        "filas_originales": int(n0),
        "duplicados": int(n0 - len(df)),
        "filas_finales": int(len(df)),
        "nulos": int(df.isna().sum().sum()),
        "outliers": out.to_dict(orient="records"),
        "winsorizacion": bool(aplicar_winsor),
    }
    if aplicar_winsor:
        resumen = df.attrs["resumen_limpieza"]
        df = winsorizar(df)
        df.attrs["resumen_limpieza"] = resumen
        print("Winsorización aplicada (p1–p99).")

    # Variables derivadas
    df["calidad_cat"] = pd.cut(df[TARGET], bins=BINS_CALIDAD, labels=LABELS_CALIDAD)
    df["buen_vino"] = (df[TARGET] >= UMBRAL_BUEN_VINO).astype(int)
    df["tipo_num"] = (df["tipo"] == "tinto").astype(int)  # 1 = tinto, 0 = blanco

    # Versión normalizada (z-score) para modelado
    df_z = df.copy()
    df_z[FEATURES] = (df[FEATURES] - df[FEATURES].mean()) / df[FEATURES].std()

    df.to_csv(DATA_PROCESSED / "wine_limpio.csv", index=False)          # <- importar en SPSS
    df_z.to_csv(DATA_PROCESSED / "wine_normalizado.csv", index=False)
    print("Exportado: data/processed/wine_limpio.csv y wine_normalizado.csv")
    return df


if __name__ == "__main__":
    from carga import cargar_datos
    limpiar(cargar_datos())
