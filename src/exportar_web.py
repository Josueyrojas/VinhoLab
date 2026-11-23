"""Fase 7 — Exportar resultados al sitio web.

Genera web/data/resultados.js (window.WINE = {...}) con todo lo que muestra el sitio:
datos para gráficas, tablas, hipótesis, métricas y los coeficientes del simulador.
Se usa .js (no .json) para que index.html funcione abriéndolo directo, sin servidor.

Los valores de SPSS se capturan a mano en spss/resultados_spss.json y se mezclan aquí.
"""
import json
import math

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler

from config import (ROOT, FEATURES, TARGET, ETIQUETAS, ALPHA, LABELS_CALIDAD, UMBRAL_BUEN_VINO)

WEB_DATA = ROOT / "web" / "data"
SPSS_JSON = ROOT / "spss" / "resultados_spss.json"
X_COLS = FEATURES + ["tipo_num"]

UNIDADES = {
    "fixed_acidity": "g/dm³ (ác. tartárico)", "volatile_acidity": "g/dm³ (ác. acético)",
    "citric_acid": "g/dm³", "residual_sugar": "g/dm³", "chlorides": "g/dm³ (NaCl)",
    "free_sulfur_dioxide": "mg/dm³", "total_sulfur_dioxide": "mg/dm³", "density": "g/cm³",
    "pH": "escala 0–14", "sulphates": "g/dm³ (sulfato de potasio)", "alcohol": "% vol",
    "quality": "0–10 (catadores)",
}
DESCRIPCIONES = {
    "fixed_acidity": "Ácidos no volátiles; aportan frescura.",
    "volatile_acidity": "Ácido acético; en exceso da sabor a vinagre.",
    "citric_acid": "Aporta frescura y sabor.",
    "residual_sugar": "Azúcar que queda tras la fermentación.",
    "chlorides": "Cantidad de sal en el vino.",
    "free_sulfur_dioxide": "SO₂ libre; previene microbios y oxidación.",
    "total_sulfur_dioxide": "SO₂ libre + combinado.",
    "density": "Depende del alcohol y el azúcar.",
    "pH": "Qué tan ácido o básico es el vino.",
    "sulphates": "Aditivo que contribuye al SO₂; antimicrobiano.",
    "alcohol": "Grado alcohólico.",
    "quality": "Mediana de al menos 3 catadores expertos.",
}


def _limpiar(o):
    """Convierte tipos numpy/pandas y NaN a tipos JSON."""
    if isinstance(o, dict):
        return {str(k): _limpiar(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_limpiar(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        f = float(o)
        return None if math.isnan(f) or math.isinf(f) else float(f"{f:.6g}")
    if isinstance(o, np.ndarray):
        return _limpiar(o.tolist())
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def _fila(df_tabla, col_prueba, prueba, col_valor):
    fila = df_tabla[df_tabla[col_prueba] == prueba].iloc[0]
    return fila[col_valor]


def _hipotesis(salidas, modelo_ols):
    h = []

    norm = salidas["06_H1_normalidad"]
    n_norm = int((norm["normal"] == "Sí").sum())
    h.append({
        "id": "H1", "titulo": "Normalidad de las variables",
        "h0": "La variable sigue una distribución normal.",
        "h1": "La variable no sigue una distribución normal.",
        "prueba": "D'Agostino-Pearson (K²) y Kolmogorov-Smirnov",
        "estadistico": None, "p": float(norm["p_K2"].max()),
        "decision": "Se rechaza H0" if n_norm == 0 else f"{n_norm} variable(s) normales",
        "rechaza": n_norm == 0,
        "interpretacion": f"{len(norm) - n_norm} de {len(norm)} variables no son normales; "
                          "por eso se acompañan las pruebas paramétricas con alternativas no paramétricas.",
        "tabla": norm.to_dict(orient="records"),
    })

    corr = salidas["07_H2_correlaciones"]
    top = corr.iloc[0]
    sig = int((corr["p_spearman"] < ALPHA).sum())
    h.append({
        "id": "H2", "titulo": "Correlación con la calidad",
        "h0": "ρ = 0: la variable no se relaciona con la calidad.",
        "h1": "ρ ≠ 0: existe relación con la calidad.",
        "prueba": "Correlación de Pearson y Spearman",
        "estadistico": float(top["spearman_rho"]), "estadistico_nombre": f"ρ ({top['variable']})",
        "p": float(top["p_spearman"]), "decision": f"{sig} de {len(corr)} significativas",
        "rechaza": sig > 0,
        "interpretacion": f"La variable con mayor relación es {top['variable']} (ρ = {top['spearman_rho']:.3f}).",
        "tabla": corr.to_dict(orient="records"),
    })

    t = salidas["08_H3_tinto_vs_blanco"]
    p_t = float(_fila(t, "prueba", "t de Welch", "p_valor"))
    m_t = float(_fila(t, "prueba", "media tinto / blanco", "estadistico"))
    m_b = float(_fila(t, "prueba", "media tinto / blanco", "p_valor"))
    h.append({
        "id": "H3", "titulo": "Calidad: tinto vs blanco",
        "h0": "μ calidad tinto = μ calidad blanco.", "h1": "Las medias son diferentes.",
        "prueba": "t de Welch + Mann-Whitney U",
        "estadistico": float(_fila(t, "prueba", "t de Welch", "estadistico")), "estadistico_nombre": "t",
        "p": p_t, "decision": "Se rechaza H0" if p_t < ALPHA else "No se rechaza H0", "rechaza": p_t < ALPHA,
        "interpretacion": f"Media tinto = {m_t:.3f}, media blanco = {m_b:.3f}; "
                          f"d de Cohen = {float(_fila(t, 'prueba', 'd de Cohen (efecto)', 'estadistico')):.3f}.",
        "extra": {"p_mann_whitney": float(_fila(t, "prueba", "Mann-Whitney U", "p_valor"))},
    })

    a = salidas["09_H4_anova_alcohol"]
    p_f = float(_fila(a, "prueba", "ANOVA de una vía", "p_valor"))
    eta = float(_fila(a, "prueba", "Eta cuadrada (efecto)", "estadistico"))
    h.append({
        "id": "H4", "titulo": "Alcohol según categoría de calidad",
        "h0": "μ alcohol es igual en calidad baja, media y alta.", "h1": "Al menos una media difiere.",
        "prueba": "ANOVA de una vía + Levene + Kruskal-Wallis + Tukey HSD",
        "estadistico": float(_fila(a, "prueba", "ANOVA de una vía", "estadistico")), "estadistico_nombre": "F",
        "p": p_f, "decision": "Se rechaza H0" if p_f < ALPHA else "No se rechaza H0", "rechaza": p_f < ALPHA,
        "interpretacion": f"η² = {eta:.3f}: la categoría de calidad explica el {eta * 100:.1f}% de la variación del alcohol.",
        "tabla": salidas["10_H4_tukey"].astype(str).to_dict(orient="records"),
    })

    c = salidas["12_H5_chi_cuadrado"].iloc[0]
    h.append({
        "id": "H5", "titulo": "Tipo de vino × categoría de calidad",
        "h0": "El tipo de vino y la calidad son independientes.", "h1": "Están asociados.",
        "prueba": "Chi-cuadrado de independencia",
        "estadistico": float(c["chi2"]), "estadistico_nombre": "χ²",
        "p": float(c["p_valor"]), "decision": c["decision"], "rechaza": float(c["p_valor"]) < ALPHA,
        "interpretacion": f"gl = {int(c['gl'])}, V de Cramér = {float(c['V_Cramer']):.3f}.",
        "tabla": salidas["11_H5_tabla_contingencia"].reset_index().to_dict(orient="records"),
    })

    coefs = pd.DataFrame({"variable": modelo_ols.params.index, "coef": modelo_ols.params.values,
                          "p": modelo_ols.pvalues.values}).query("variable != 'const'")
    coefs["variable"] = coefs["variable"].map(lambda v: ETIQUETAS.get(v, "Tipo (tinto)"))
    h.append({
        "id": "H6", "titulo": "Regresión lineal múltiple",
        "h0": "Todos los β = 0: el modelo no explica la calidad.", "h1": "Al menos un β ≠ 0.",
        "prueba": "Mínimos cuadrados ordinarios (OLS) + VIF",
        "estadistico": float(modelo_ols.fvalue), "estadistico_nombre": "F",
        "p": float(modelo_ols.f_pvalue),
        "decision": "Se rechaza H0" if modelo_ols.f_pvalue < ALPHA else "No se rechaza H0",
        "rechaza": modelo_ols.f_pvalue < ALPHA,
        "interpretacion": f"R² = {modelo_ols.rsquared:.3f} (R² ajustado = {modelo_ols.rsquared_adj:.3f}): "
                          f"el modelo explica el {modelo_ols.rsquared * 100:.1f}% de la variación de la calidad.",
        "tabla": coefs.to_dict(orient="records"),
        "extra": {"r2": modelo_ols.rsquared, "r2_adj": modelo_ols.rsquared_adj},
    })
    return h


def _simulador(df):
    X, y = df[X_COLS], df[TARGET]
    sc = StandardScaler().fit(X)
    Xs = sc.transform(X)
    lin = LinearRegression().fit(Xs, y)
    log = LogisticRegression(max_iter=1000).fit(Xs, df["buen_vino"])
    rangos = {}
    for col in FEATURES:
        rangos[col] = {
            "min": float(df[col].min()), "max": float(df[col].max()),
            "tinto": float(df.loc[df.tipo == "tinto", col].median()),
            "blanco": float(df.loc[df.tipo == "blanco", col].median()),
        }
    return {"columnas": X_COLS, "media": sc.mean_, "escala": sc.scale_,
            "lineal": {"coef": lin.coef_, "intercepto": lin.intercept_},
            "logistica": {"coef": log.coef_[0], "intercepto": log.intercept_[0]},
            "rangos": rangos, "umbral": UMBRAL_BUEN_VINO}


def _comparativa_spss(hip, modelo_ols, res_modelo):
    py = {
        "h3_t": hip[2]["estadistico"], "h3_p": hip[2]["p"],
        "h4_f": hip[3]["estadistico"], "h4_p": hip[3]["p"],
        "h5_chi2": hip[4]["estadistico"], "h5_p": hip[4]["p"],
        "h6_r2": modelo_ols.rsquared, "h6_f": modelo_ols.fvalue,
        "r_alcohol": next(r["pearson_r"] for r in hip[1]["tabla"] if r["variable"] == "Alcohol"),
    }
    nombres = {
        "h3_t": "H3 · t de Welch (t)", "h3_p": "H3 · t de Welch (p)",
        "h4_f": "H4 · ANOVA (F)", "h4_p": "H4 · ANOVA (p)",
        "h5_chi2": "H5 · Chi-cuadrado (χ²)", "h5_p": "H5 · Chi-cuadrado (p)",
        "h6_r2": "H6 · Regresión (R²)", "h6_f": "H6 · Regresión (F)",
        "r_alcohol": "H2 · Pearson r (alcohol)",
    }
    spss = {}
    if SPSS_JSON.exists():
        spss = json.loads(SPSS_JSON.read_text(encoding="utf-8"))
    else:
        SPSS_JSON.write_text(json.dumps({k: None for k in py}, indent=2), encoding="utf-8")
        print("Plantilla creada: spss/resultados_spss.json (capturen ahí los valores de SPSS)")
    return [{"id": k, "prueba": nombres[k], "python": v, "spss": spss.get(k)} for k, v in py.items()]


def exportar_web(df, salidas, modelo_ols, res_modelo):
    print("\n=== FASE 7: EXPORTAR AL SITIO WEB ===")
    WEB_DATA.mkdir(parents=True, exist_ok=True)

    cols = FEATURES + [TARGET]
    desc = df[cols].describe().T
    desc["mediana"] = df[cols].median()
    desc["asimetria"] = df[cols].skew()
    desc["curtosis"] = df[cols].kurt()
    desc["cv"] = desc["std"] / desc["mean"] * 100

    hip = _hipotesis(salidas, modelo_ols)
    imp = res_modelo["importancia"].sort_values(ascending=False)

    data = {
        "meta": {
            "titulo": "Predicción y Análisis de la Calidad del Vino Verde Portugués",
            "materia": "Inteligencia de Datos",
            "institucion": "Tecnológico Nacional de México · Instituto Tecnológico de Celaya",
            "lider": "Angel Alejandro Adrian Cruz Cruz",
            "integrantes": ["Roberto Emmanuel Duran Castillo", "Josué Yañez Rojas",
                            "Andrea Guadalupe Rodriguez Patiño", "Enrique Gallegos Linares"],
            "cita": "Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Wine Quality "
                    "[Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56S3T",
            "n_tinto": int((df.tipo == "tinto").sum()), "n_blanco": int((df.tipo == "blanco").sum()),
            "alpha": ALPHA,
        },
        "variables": [{"key": c, "etiqueta": ETIQUETAS[c], "unidad": UNIDADES[c],
                       "descripcion": DESCRIPCIONES[c]} for c in cols],
        "limpieza": df.attrs.get("resumen_limpieza", {}),
        "datos": {**{c: df[c].round(4).tolist() for c in cols},
                  "tipo": df["tipo"].tolist(), "calidad_cat": df["calidad_cat"].astype(str).tolist()},
        "descriptiva": [{"variable": ETIQUETAS[c], "key": c, **desc.loc[c].to_dict()} for c in cols],
        "correlacion": {"labels": [ETIQUETAS[c] for c in cols], "matriz": df[cols].corr().values},
        "hipotesis": hip,
        "modelo": {
            "regresion": res_modelo["met_reg"].to_dict(orient="records"),
            "clasificacion": res_modelo["met_clf"].to_dict(orient="records"),
            "importancia": {"variables": imp.index.tolist(), "valores": imp.values},
            "matriz_confusion": res_modelo["cm"],
        },
        "simulador": _simulador(df),
        "conclusiones": {
            "top_variables": imp.index[:3].tolist(),
            "r2": modelo_ols.rsquared,
            "mejor_clf": res_modelo["met_clf"].sort_values("F1", ascending=False).iloc[0].to_dict(),
        },
    }
    data["spss"] = _comparativa_spss(hip, modelo_ols, res_modelo)

    destino = WEB_DATA / "resultados.js"
    destino.write_text("window.WINE = " + json.dumps(_limpiar(data), ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"Exportado: web/data/resultados.js ({destino.stat().st_size / 1024:.0f} KB). Abre web/index.html")
