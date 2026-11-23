"""Fase 3 — Estadística descriptiva.

Tablas: medidas de tendencia central, dispersión y forma (general y por tipo de vino),
frecuencias de calidad.
Figuras: histogramas, boxplots por calidad, distribución de calidad, heatmap de correlación.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import FEATURES, TARGET, ETIQUETAS, FIG_DIR, TAB_DIR

sns.set_theme(style="whitegrid", palette="deep")


def tabla_descriptiva(df: pd.DataFrame) -> pd.DataFrame:
    cols = FEATURES + [TARGET]
    d = df[cols].describe().T
    d["mediana"] = df[cols].median()
    d["moda"] = df[cols].mode().iloc[0]
    d["varianza"] = df[cols].var()
    d["CV_%"] = (d["std"] / d["mean"] * 100).round(2)
    d["asimetria"] = df[cols].skew()
    d["curtosis"] = df[cols].kurt()
    d["rango"] = d["max"] - d["min"]
    d["IQR"] = d["75%"] - d["25%"]
    d = d.rename(columns={"count": "n", "mean": "media", "std": "desv_est"})
    d.index = [ETIQUETAS[c] for c in d.index]
    return d.round(4)


def descriptiva(df: pd.DataFrame):
    print("\n=== FASE 3: ESTADÍSTICA DESCRIPTIVA ===")
    general = tabla_descriptiva(df)
    general.to_csv(TAB_DIR / "03_descriptiva_general.csv")
    print(general[["media", "mediana", "desv_est", "CV_%", "asimetria", "curtosis"]])

    for tipo, sub in df.groupby("tipo"):
        tabla_descriptiva(sub).to_csv(TAB_DIR / f"03_descriptiva_{tipo}.csv")

    frec = (df.groupby(["tipo", TARGET]).size().unstack(0, fill_value=0))
    frec["total"] = frec.sum(axis=1)
    frec["pct_total"] = (frec["total"] / frec["total"].sum() * 100).round(2)
    frec.to_csv(TAB_DIR / "04_frecuencias_calidad.csv")

    # 1. Distribución de la calidad
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x=TARGET, hue="tipo", ax=ax)
    ax.set(title="Distribución de la calidad por tipo de vino", xlabel="Calidad", ylabel="Frecuencia")
    fig.tight_layout(); fig.savefig(FIG_DIR / "01_distribucion_calidad.png", dpi=150); plt.close(fig)

    # 2. Histogramas de todas las variables
    fig, axes = plt.subplots(4, 3, figsize=(15, 14))
    for ax, col in zip(axes.flat, FEATURES):
        sns.histplot(data=df, x=col, hue="tipo", kde=True, ax=ax, element="step", stat="density", common_norm=False)
        ax.set_title(ETIQUETAS[col]); ax.set_xlabel("")
    axes.flat[-1].axis("off")
    fig.suptitle("Histogramas de variables fisicoquímicas", fontsize=15)
    fig.tight_layout(); fig.savefig(FIG_DIR / "02_histogramas.png", dpi=150); plt.close(fig)

    # 3. Boxplots por categoría de calidad
    fig, axes = plt.subplots(4, 3, figsize=(15, 14))
    for ax, col in zip(axes.flat, FEATURES):
        sns.boxplot(data=df, x="calidad_cat", y=col, hue="tipo", ax=ax)
        ax.set_title(ETIQUETAS[col]); ax.set_xlabel(""); ax.set_ylabel("")
        if ax.get_legend(): ax.get_legend().remove()
    axes.flat[-1].axis("off")
    fig.suptitle("Variables por categoría de calidad (baja / media / alta)", fontsize=15)
    fig.tight_layout(); fig.savefig(FIG_DIR / "03_boxplots_calidad.png", dpi=150); plt.close(fig)

    # 4. Heatmap de correlación (Pearson)
    corr = df[FEATURES + [TARGET]].corr()
    corr_lbl = corr.rename(index=ETIQUETAS, columns=ETIQUETAS)
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(corr_lbl, annot=True, fmt=".2f", cmap="RdBu_r", center=0, square=True, ax=ax)
    ax.set_title("Matriz de correlación de Pearson")
    fig.tight_layout(); fig.savefig(FIG_DIR / "04_heatmap_correlacion.png", dpi=150); plt.close(fig)
    corr.round(4).to_csv(TAB_DIR / "05_matriz_correlacion.csv")

    # 5. Alcohol vs calidad
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.violinplot(data=df, x=TARGET, y="alcohol", hue="tipo", split=True, ax=ax)
    ax.set(title="Grado de alcohol según calidad", xlabel="Calidad", ylabel="Alcohol (% vol)")
    fig.tight_layout(); fig.savefig(FIG_DIR / "05_alcohol_vs_calidad.png", dpi=150); plt.close(fig)

    print("Tablas en outputs/tablas/ y figuras en outputs/figuras/")


if __name__ == "__main__":
    from carga import cargar_datos
    from limpieza import limpiar
    descriptiva(limpiar(cargar_datos()))
