# Predicción y Análisis de la Calidad del Vino Verde Portugués

**Inteligencia de Datos — Proyecto final**
Estadística descriptiva, inferencial y tratamiento de datos con **Python** y **SPSS**.

Equipo: Angel Alejandro Adrian Cruz Cruz (líder), Roberto Emmanuel Duran Castillo, Josué Yañez Rojas, Andrea Guadalupe Rodriguez Patiño, Enrique Gallegos Linares.

Dataset: Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). *Wine Quality* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56S3T

---

## Estructura del proyecto

```
wine-quality-proyecto/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                  # winequality-red.csv y winequality-white.csv (originales UCI, sep=';')
│   └── processed/            # wine_limpio.csv (→ SPSS) y wine_normalizado.csv (→ modelos)
├── src/
│   ├── config.py             # rutas, nombres de columnas, α, semillas
│   ├── carga.py              # Fase 1: carga (descarga UCI si no hay CSV locales)
│   ├── limpieza.py           # Fase 2: duplicados, outliers, winsorización, derivadas, z-score
│   ├── descriptiva.py        # Fase 3: tendencia central, dispersión, forma, gráficas
│   ├── inferencial.py        # Fase 4: pruebas de hipótesis H1–H6
│   ├── modelado.py           # Fase 5: regresión y clasificación (lineal/logística vs Random Forest)
│   ├── exportar_web.py       # Fase 7: exporta resultados a web/data/resultados.js
│   └── main.py               # ejecuta todo el pipeline
├── spss/
│   ├── analisis_wine.sps     # sintaxis SPSS que replica el análisis
│   └── resultados_spss.json  # aquí se capturan los valores del visor de SPSS
├── web/                      # sitio de presentación (HTML/CSS/JS + Plotly)
│   ├── index.html
│   ├── css/estilos.css
│   ├── js/app.js
│   ├── vendor/plotly.min.js  # incluido para funcionar sin internet
│   └── data/resultados.js    # lo genera main.py
├── outputs/
│   ├── figuras/              # PNG para el reporte y la presentación
│   ├── tablas/               # CSV/TXT numerados en orden del reporte
│   └── modelos/              # modelos entrenados (.joblib)
└── docs/
    ├── Investigacion_Dataset_Trabajo_Final.pdf  # fase 0: investigación del dataset
    ├── plan_de_trabajo.md    # fases, roles y entregables
    ├── reporte_final.md      # borrador del reporte con los resultados reales
    └── estructura_reporte.md # índice del documento final
```

## Cómo ejecutarlo

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python src/main.py
```

Si no hay CSV en `data/raw/`, el script descarga el ZIP oficial de UCI. Si no hay internet, descarguen el dataset de https://archive.ics.uci.edu/dataset/186/wine+quality y coloquen los dos CSV en `data/raw/`.

Cada fase también se puede ejecutar sola, por ejemplo `python src/inferencial.py`.

## Sitio web de resultados

Al terminar, `main.py` genera `web/data/resultados.js`. Abran **`web/index.html`** con doble clic: funciona sin servidor y sin internet.

Secciones: dataset · tratamiento · descriptiva (explorador por variable) · correlación · hipótesis H1–H6 (con detalle al hacer clic) · modelo · **simulador de calidad** · Python vs SPSS · conclusiones.

Para publicarlo con un link: suban la carpeta `web/` a Netlify (arrastrar y soltar en app.netlify.com/drop) o a GitHub Pages.

**Comparativa con SPSS:** capturen los valores del visor de SPSS en `spss/resultados_spss.json` (t, p, F, χ², R², r) y vuelvan a correr `python src/main.py`. El sitio marca automáticamente si coinciden.

## Flujo del análisis

| Fase | Script | Qué produce |
|---|---|---|
| 1. Carga | `carga.py` | Une tinto (1,599) + blanco (4,898) con columna `tipo` |
| 2. Tratamiento | `limpieza.py` | Reporte de nulos, duplicados eliminados, outliers (IQR / z>3), winsorización p1–p99, `calidad_cat` (baja ≤5 / media 6 / alta ≥7), `buen_vino` (≥7), `tipo_num`, versión z-score |
| 3. Descriptiva | `descriptiva.py` | Media, mediana, moda, desv. est., varianza, CV, asimetría, curtosis, IQR (general y por tipo); 5 figuras |
| 4. Inferencial | `inferencial.py` | H1 normalidad · H2 correlación Pearson/Spearman · H3 t de Welch + Mann-Whitney (tinto vs blanco) · H4 ANOVA + Levene + Kruskal-Wallis + Tukey (alcohol por calidad) · H5 χ² + V de Cramér · H6 regresión lineal múltiple + VIF |
| 5. Modelado | `modelado.py` | Regresión (RMSE, MAE, R²) y clasificación "buen vino" (accuracy, precision, recall, F1, ROC-AUC), importancia de variables, matriz de confusión |
| 6. SPSS | `analisis_wine.sps` | Las mismas pruebas en SPSS sobre `wine_limpio.csv` para comparar resultados |
| 7. Web | `exportar_web.py` + `web/` | Sitio interactivo con todos los resultados y un simulador de calidad |

## Uso en SPSS

1. Ejecutar primero `python src/main.py` (genera `data/processed/wine_limpio.csv`).
2. Abrir `spss/analisis_wine.sps`, cambiar la ruta en `GET DATA /FILE=...`.
3. *Ejecutar → Todo*. Exportar el visor de resultados a Word/PDF para anexos.

## Hipótesis (α = 0.05)

| | H0 | H1 |
|---|---|---|
| H1 | La variable sigue una distribución normal | No sigue distribución normal |
| H2 | ρ = 0 entre la variable y la calidad | ρ ≠ 0 |
| H3 | μ calidad tinto = μ calidad blanco | Son diferentes |
| H4 | μ alcohol igual en calidad baja, media y alta | Al menos una media difiere |
| H5 | Tipo de vino y categoría de calidad son independientes | Están asociados |
| H6 | Todos los β = 0 (el modelo no explica la calidad) | Al menos un β ≠ 0 |
