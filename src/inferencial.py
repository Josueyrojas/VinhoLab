"""Fase 4 — Estadística inferencial.

Hipótesis (α = 0.05):
  H1  Normalidad de las variables (D'Agostino-Pearson y Kolmogorov-Smirnov).
  H2  Correlación de cada variable con la calidad (Pearson y Spearman).
  H3  La calidad media difiere entre vino tinto y blanco (t de Welch + Mann-Whitney).
  H4  El grado de alcohol difiere entre categorías de calidad (ANOVA + Levene + Kruskal-Wallis + Tukey).
  H5  El tipo de vino y la categoría de calidad son independientes (Chi-cuadrado).
  H6  Regresión lineal múltiple: las variables fisicoquímicas explican la calidad (OLS + VIF).
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.outliers_influence import variance_inflation_factor

from config import FEATURES, TARGET, ETIQUETAS, ALPHA, TAB_DIR


def decision(p):
    return "Se rechaza H0" if p < ALPHA else "No se rechaza H0"


def h1_normalidad(df):
    filas = []
    for col in FEATURES + [TARGET]:
        x = df[col]
        k2, p_k2 = stats.normaltest(x)
        ks, p_ks = stats.kstest((x - x.mean()) / x.std(), "norm")
        filas.append({"variable": ETIQUETAS[col], "DAgostino_K2": k2, "p_K2": p_k2,
                      "KS": ks, "p_KS": p_ks, "normal": "Sí" if p_k2 >= ALPHA else "No"})
    return pd.DataFrame(filas)


def h2_correlaciones(df):
    filas = []
    for col in FEATURES:
        r, p_r = stats.pearsonr(df[col], df[TARGET])
        rho, p_rho = stats.spearmanr(df[col], df[TARGET])
        filas.append({"variable": ETIQUETAS[col], "pearson_r": r, "p_pearson": p_r,
                      "spearman_rho": rho, "p_spearman": p_rho, "decision": decision(p_rho)})
    return pd.DataFrame(filas).sort_values("spearman_rho", key=abs, ascending=False)


def h3_tinto_vs_blanco(df):
    t = df.loc[df.tipo == "tinto", TARGET]
    b = df.loc[df.tipo == "blanco", TARGET]
    t_stat, p_t = stats.ttest_ind(t, b, equal_var=False)
    u_stat, p_u = stats.mannwhitneyu(t, b)
    d = (t.mean() - b.mean()) / np.sqrt((t.var() + b.var()) / 2)  # d de Cohen
    return pd.DataFrame([
        {"prueba": "t de Welch", "estadistico": t_stat, "p_valor": p_t, "decision": decision(p_t)},
        {"prueba": "Mann-Whitney U", "estadistico": u_stat, "p_valor": p_u, "decision": decision(p_u)},
        {"prueba": "d de Cohen (efecto)", "estadistico": d, "p_valor": np.nan, "decision": ""},
        {"prueba": "media tinto / blanco", "estadistico": t.mean(), "p_valor": b.mean(), "decision": ""},
    ])


def h4_anova_alcohol(df):
    grupos = [g["alcohol"].values for _, g in df.groupby("calidad_cat", observed=True)]
    lev, p_lev = stats.levene(*grupos)
    f, p_f = stats.f_oneway(*grupos)
    h, p_h = stats.kruskal(*grupos)
    # eta cuadrada
    gran_media = df["alcohol"].mean()
    ss_between = sum(len(g) * (g.mean() - gran_media) ** 2 for g in grupos)
    ss_total = ((df["alcohol"] - gran_media) ** 2).sum()
    res = pd.DataFrame([
        {"prueba": "Levene (homocedasticidad)", "estadistico": lev, "p_valor": p_lev, "decision": decision(p_lev)},
        {"prueba": "ANOVA de una vía", "estadistico": f, "p_valor": p_f, "decision": decision(p_f)},
        {"prueba": "Kruskal-Wallis", "estadistico": h, "p_valor": p_h, "decision": decision(p_h)},
        {"prueba": "Eta cuadrada (efecto)", "estadistico": ss_between / ss_total, "p_valor": np.nan, "decision": ""},
    ])
    tukey = pairwise_tukeyhsd(df["alcohol"], df["calidad_cat"].astype(str), alpha=ALPHA)
    tukey_df = pd.DataFrame(tukey.summary().data[1:], columns=tukey.summary().data[0])
    return res, tukey_df


def h5_chi_cuadrado(df):
    tabla = pd.crosstab(df["tipo"], df["calidad_cat"])
    chi2, p, gl, _ = stats.chi2_contingency(tabla)
    n = tabla.values.sum()
    v_cramer = np.sqrt(chi2 / (n * (min(tabla.shape) - 1)))
    res = pd.DataFrame([{"chi2": chi2, "gl": gl, "p_valor": p, "V_Cramer": v_cramer, "decision": decision(p)}])
    return tabla, res


def h6_regresion(df):
    X = df[FEATURES + ["tipo_num"]]
    X_const = sm.add_constant(X)
    modelo = sm.OLS(df[TARGET], X_const).fit()
    vif = pd.DataFrame({"variable": X.columns,
                        "VIF": [variance_inflation_factor(X_const.values, i + 1) for i in range(X.shape[1])]})
    return modelo, vif


def inferencial(df):
    print("\n=== FASE 4: ESTADÍSTICA INFERENCIAL ===")
    salidas = {}

    salidas["06_H1_normalidad"] = h1_normalidad(df)
    salidas["07_H2_correlaciones"] = h2_correlaciones(df)
    salidas["08_H3_tinto_vs_blanco"] = h3_tinto_vs_blanco(df)
    salidas["09_H4_anova_alcohol"], salidas["10_H4_tukey"] = h4_anova_alcohol(df)
    salidas["11_H5_tabla_contingencia"], salidas["12_H5_chi_cuadrado"] = h5_chi_cuadrado(df)
    modelo, salidas["14_H6_VIF"] = h6_regresion(df)

    for nombre, tabla in salidas.items():
        tabla.to_csv(TAB_DIR / f"{nombre}.csv", index="contingencia" in nombre)
        print(f"\n--- {nombre} ---\n{tabla.round(4).to_string()}")

    (TAB_DIR / "13_H6_regresion_OLS.txt").write_text(modelo.summary().as_text(), encoding="utf-8")
    print(f"\n--- Regresión lineal múltiple ---\nR² = {modelo.rsquared:.4f} | R² ajustado = {modelo.rsquared_adj:.4f} "
          f"| F = {modelo.fvalue:.2f} (p = {modelo.f_pvalue:.2e})")
    return salidas, modelo


if __name__ == "__main__":
    from carga import cargar_datos
    from limpieza import limpiar
    inferencial(limpiar(cargar_datos()))
