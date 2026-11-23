"""Fase 5 — Modelo predictivo.

A) Regresión: predecir la calidad (0–10) -> Regresión lineal vs Random Forest Regressor (RMSE, MAE, R²).
B) Clasificación: predecir "buen vino" (calidad >= 7) -> Regresión logística vs Random Forest
   (accuracy, precision, recall, F1, ROC-AUC, matriz de confusión).
Incluye importancia de variables.
"""
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix, f1_score,
                             mean_absolute_error, mean_squared_error, precision_score, r2_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from config import FEATURES, TARGET, ETIQUETAS, RANDOM_STATE, FIG_DIR, TAB_DIR, MODEL_DIR

X_COLS = FEATURES + ["tipo_num"]


def regresion(df):
    X_tr, X_te, y_tr, y_te = train_test_split(df[X_COLS], df[TARGET], test_size=0.2, random_state=RANDOM_STATE)
    modelos = {
        "Regresión lineal": make_pipeline(StandardScaler(), LinearRegression()),
        "Random Forest": RandomForestRegressor(n_estimators=300, random_state=RANDOM_STATE, n_jobs=-1),
    }
    filas = []
    for nombre, m in modelos.items():
        m.fit(X_tr, y_tr)
        p = m.predict(X_te)
        filas.append({"modelo": nombre, "RMSE": np.sqrt(mean_squared_error(y_te, p)),
                      "MAE": mean_absolute_error(y_te, p), "R2": r2_score(y_te, p),
                      "exactitud_redondeo": (np.round(p) == y_te).mean()})
    return pd.DataFrame(filas), modelos["Random Forest"]


def clasificacion(df):
    X_tr, X_te, y_tr, y_te = train_test_split(df[X_COLS], df["buen_vino"], test_size=0.2,
                                              random_state=RANDOM_STATE, stratify=df["buen_vino"])
    modelos = {
        "Regresión logística": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced")),
        "Random Forest": RandomForestClassifier(n_estimators=300, random_state=RANDOM_STATE,
                                                class_weight="balanced", n_jobs=-1),
    }
    filas, preds = [], {}
    for nombre, m in modelos.items():
        m.fit(X_tr, y_tr)
        p = m.predict(X_te); prob = m.predict_proba(X_te)[:, 1]
        preds[nombre] = p
        filas.append({"modelo": nombre, "accuracy": accuracy_score(y_te, p),
                      "precision": precision_score(y_te, p), "recall": recall_score(y_te, p),
                      "F1": f1_score(y_te, p), "ROC_AUC": roc_auc_score(y_te, prob)})
    reporte = classification_report(y_te, preds["Random Forest"], target_names=["No bueno", "Bueno (>=7)"])
    cm = confusion_matrix(y_te, preds["Random Forest"])
    return pd.DataFrame(filas), modelos["Random Forest"], reporte, cm


def modelado(df):
    print("\n=== FASE 5: MODELADO PREDICTIVO ===")
    met_reg, rf_reg = regresion(df)
    met_clf, rf_clf, reporte, cm = clasificacion(df)

    met_reg.to_csv(TAB_DIR / "15_metricas_regresion.csv", index=False)
    met_clf.to_csv(TAB_DIR / "16_metricas_clasificacion.csv", index=False)
    (TAB_DIR / "17_reporte_clasificacion.txt").write_text(reporte, encoding="utf-8")
    print(met_reg.round(4).to_string(index=False)); print(met_clf.round(4).to_string(index=False)); print(reporte)

    imp = pd.Series(rf_clf.feature_importances_, index=[ETIQUETAS.get(c, "Tipo (tinto)") for c in X_COLS]).sort_values()
    imp.to_csv(TAB_DIR / "18_importancia_variables.csv", header=["importancia"])

    fig, ax = plt.subplots(figsize=(8, 6))
    imp.plot.barh(ax=ax, color="#7b2d43")
    ax.set(title="Importancia de variables (Random Forest)", xlabel="Importancia")
    fig.tight_layout(); fig.savefig(FIG_DIR / "06_importancia_variables.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Reds", ax=ax,
                xticklabels=["No bueno", "Bueno"], yticklabels=["No bueno", "Bueno"])
    ax.set(title="Matriz de confusión (Random Forest)", xlabel="Predicho", ylabel="Real")
    fig.tight_layout(); fig.savefig(FIG_DIR / "07_matriz_confusion.png", dpi=150); plt.close(fig)

    joblib.dump(rf_clf, MODEL_DIR / "rf_buen_vino.joblib")
    joblib.dump(rf_reg, MODEL_DIR / "rf_calidad.joblib")
    print("Modelos guardados en outputs/modelos/")
    return {"met_reg": met_reg, "met_clf": met_clf, "importancia": imp, "cm": cm}


if __name__ == "__main__":
    from carga import cargar_datos
    from limpieza import limpiar
    modelado(limpiar(cargar_datos()))
