# Predicción y Análisis de la Calidad del Vino Verde Portugués mediante Estadística Descriptiva, Inferencial y Tratamiento de Datos con Python y SPSS

**Inteligencia de Datos — Proyecto final**

| | |
|---|---|
| Institución | TecNM / Instituto Tecnológico de Celaya |
| Materia | Inteligencia de Datos |
| Docente | _(completar)_ |
| Líder de proyecto | Angel Alejandro Adrian Cruz Cruz |
| Integrantes | Roberto Emmanuel Duran Castillo · Josué Yañez Rojas · Andrea Guadalupe Rodriguez Patiño · Enrique Gallegos Linares |
| Fecha | _(completar)_ |

> **Borrador generado a partir de las salidas de `python src/main.py`** (tablas en `outputs/tablas/`, figuras en `outputs/figuras/`).
> Las secciones 5.4–5.5 ya incluyen los resultados de SPSS (`spss/resultados_spss.json`); solo falta pegar capturas del visor.
> Si vuelven a correr el pipeline y cambian los números, actualicen las cifras de este documento.

---

## Resumen

Se analizó el conjunto de datos *Wine Quality* (Cortez et al., 2009) del UCI Machine Learning Repository, que reúne 6,497 muestras de vino verde portugués (1,599 tintos y 4,898 blancos) descritas por 11 propiedades fisicoquímicas y una calificación sensorial de 0 a 10 otorgada por catadores expertos. Tras el tratamiento de datos (eliminación de 1,177 registros duplicados, detección de valores atípicos por IQR y z-score, y winsorización en los percentiles 1–99) quedaron 5,320 observaciones. La estadística descriptiva muestra una calidad concentrada en 5 y 6 puntos (76.6 % de los vinos) y ninguna variable con distribución normal (D'Agostino K², p < 0.001). Las pruebas inferenciales confirmaron que todas las propiedades se correlacionan significativamente con la calidad, destacando el **alcohol** (r = 0.47) y, en sentido inverso, la **densidad** (r = −0.34) y la **acidez volátil** (r = −0.26); que los vinos blancos obtienen calificaciones ligeramente mayores que los tintos (t de Welch, p < 0.001, d = −0.27); y que el contenido de alcohol difiere entre calidades baja, media y alta (ANOVA F = 901.1, η² = 0.25). Un modelo de regresión lineal múltiple explica el 31.7 % de la variabilidad de la calidad. Para clasificar vinos “buenos” (calidad ≥ 7), un Random Forest alcanzó 84.7 % de exactitud y ROC-AUC de 0.878, superando a la regresión logística. Los resultados se replicaron en SPSS.

**Palabras clave:** calidad del vino, estadística inferencial, regresión múltiple, Random Forest, Python, SPSS.

---

## 1. Introducción

### 1.1 Contexto

El *vinho verde* es una denominación de origen de la región del Minho, al noroeste de Portugal. Su certificación incluye pruebas fisicoquímicas de laboratorio (acidez, pH, alcohol, azúcares, sulfitos, etc.) y una evaluación sensorial realizada por catadores. La evaluación sensorial es costosa, lenta y subjetiva; por ello resulta valioso saber en qué medida las mediciones de laboratorio, más baratas y objetivas, permiten explicar y anticipar la calificación de los expertos.

### 1.2 Planteamiento del problema

No se sabe a priori cuáles propiedades fisicoquímicas influyen de forma significativa en la calidad percibida, ni si esa relación es la misma para vinos tintos y blancos. Tampoco es evidente qué tan bien puede predecirse la calidad a partir solo de datos químicos.

### 1.3 Objetivos

**Objetivo general.** Determinar qué propiedades fisicoquímicas influyen significativamente en la calidad sensorial del vino verde portugués y construir un modelo que permita predecirla, aplicando estadística descriptiva e inferencial con Python y SPSS.

**Objetivos específicos.**
1. Realizar el tratamiento de datos: revisión de nulos, duplicados, valores atípicos y normalización.
2. Describir cada variable con medidas de tendencia central, dispersión y forma, en general y por tipo de vino.
3. Contrastar seis hipótesis estadísticas (H1–H6) sobre normalidad, correlación, diferencias de medias, asociación y regresión.
4. Entrenar y comparar modelos de regresión y clasificación para predecir la calidad.
5. Replicar el análisis en SPSS y comparar los resultados con Python.

### 1.4 Hipótesis (α = 0.05)

| | H₀ | H₁ |
|---|---|---|
| H1 | La variable sigue una distribución normal | No sigue una distribución normal |
| H2 | ρ = 0 entre la variable y la calidad | ρ ≠ 0 |
| H3 | μ calidad tinto = μ calidad blanco | Son diferentes |
| H4 | La media de alcohol es igual en calidad baja, media y alta | Al menos una media difiere |
| H5 | El tipo de vino y la categoría de calidad son independientes | Están asociados |
| H6 | Todos los β = 0 (el modelo no explica la calidad) | Al menos un β ≠ 0 |

### 1.5 Justificación

Se revisaron los cuatro repositorios sugeridos en clase (Data and Story Library, Gapminder, FRED y UCI). El dataset *Wine Quality* de UCI se eligió porque no tiene valores faltantes, contiene múltiples variables cuantitativas continuas con una variable objetivo clara, tiene autoría y citación académica verificables, y se importa directamente en Python y SPSS para pruebas t, ANOVA, correlación, χ² y regresión (ver `docs/Investigacion_Dataset_Trabajo_Final.pdf`, sección 7).

---

## 2. Marco teórico

### 2.1 Estadística descriptiva
- **Tendencia central:** media, mediana y moda.
- **Dispersión:** desviación estándar, varianza, rango, rango intercuartílico (IQR) y coeficiente de variación (CV = σ/μ · 100).
- **Forma:** asimetría (sesgo) y curtosis (exceso respecto a la normal).

### 2.2 Estadística inferencial
Una prueba de hipótesis compara un estadístico con su distribución bajo H₀; si el p-valor es menor que α = 0.05 se rechaza H₀. Las pruebas **paramétricas** (t, ANOVA, Pearson) suponen normalidad y, en su caso, homogeneidad de varianzas; las **no paramétricas** (Mann-Whitney, Kruskal-Wallis, Spearman) no lo requieren. Con muestras grandes el p-valor casi siempre es pequeño, por lo que se reportan **tamaños de efecto** (d de Cohen, η², V de Cramér) para valorar la relevancia práctica.

### 2.3 Correlación y regresión lineal múltiple
El coeficiente de Pearson mide asociación lineal y Spearman asociación monótona por rangos. La regresión lineal múltiple modela *calidad = β₀ + Σβᵢxᵢ + ε*; su ajuste se mide con R² y su significancia global con la prueba F. La **multicolinealidad** se diagnostica con el factor de inflación de la varianza (VIF): valores > 10 indican colinealidad severa.

### 2.4 Clasificación
- **Regresión logística:** modela la probabilidad de pertenecer a una clase mediante la función logística.
- **Random Forest:** conjunto de árboles de decisión entrenados sobre submuestras; reduce la varianza y estima la importancia de cada variable.
- **Métricas:** exactitud (accuracy), precisión, sensibilidad (recall), F1 y área bajo la curva ROC (ROC-AUC).

### 2.5 Herramientas
Python 3 con pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib y seaborn; IBM SPSS Statistics.

### 2.6 Trabajo previo
Cortez et al. (2009) usaron este mismo dataset para modelar las preferencias con regresión múltiple, redes neuronales y máquinas de soporte vectorial (SVM), y encontraron que el alcohol, los sulfatos (en tintos) y la acidez volátil están entre las variables más relevantes, con SVM como el mejor modelo.

---

## 3. Descripción del dataset

### 3.1 Autor, fuente y licencia
- **Autores:** Paulo Cortez (Universidad de Minho, Guimarães, Portugal), A. Cerdeira, F. Almeida, T. Matos y J. Reis (Comisión de Viticultura de la Región del Vinho Verde, CVRVV, Oporto).
- **Fuente:** UCI Machine Learning Repository — https://archive.ics.uci.edu/dataset/186/wine+quality
- **Licencia:** Creative Commons Attribution 4.0 (CC BY 4.0).
- **Cita:** Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). *Wine Quality* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56S3T

### 3.2 Diccionario de datos

| Variable (archivo) | Descripción | Unidad | Tipo | Escala |
|---|---|---|---|---|
| `fixed_acidity` | Acidez fija (ácido tartárico) | g/dm³ | Cuantitativa continua | Razón |
| `volatile_acidity` | Acidez volátil (ácido acético) | g/dm³ | Cuantitativa continua | Razón |
| `citric_acid` | Ácido cítrico | g/dm³ | Cuantitativa continua | Razón |
| `residual_sugar` | Azúcar residual | g/dm³ | Cuantitativa continua | Razón |
| `chlorides` | Cloruros (cloruro de sodio) | g/dm³ | Cuantitativa continua | Razón |
| `free_sulfur_dioxide` | Dióxido de azufre libre | mg/dm³ | Cuantitativa continua | Razón |
| `total_sulfur_dioxide` | Dióxido de azufre total | mg/dm³ | Cuantitativa continua | Razón |
| `density` | Densidad | g/cm³ | Cuantitativa continua | Razón |
| `pH` | pH | — | Cuantitativa continua | Intervalo |
| `sulphates` | Sulfatos (sulfato de potasio) | g/dm³ | Cuantitativa continua | Razón |
| `alcohol` | Grado alcohólico | % vol. | Cuantitativa continua | Razón |
| `quality` | Calidad sensorial (mediana de ≥ 3 catadores) | 0–10 | Cuantitativa discreta | Ordinal |
| `tipo` | Tipo de vino (agregada al unir archivos) | tinto / blanco | Cualitativa | Nominal |

**Variables derivadas** (creadas en `limpieza.py`): `calidad_cat` (baja ≤ 5, media = 6, alta ≥ 7), `buen_vino` (1 si calidad ≥ 7) y `tipo_num` (1 = tinto, 0 = blanco).

### 3.3 Tamaño
Tinto: 1,599 registros; blanco: 4,898; total 6,497 con 11 predictoras y 1 variable objetivo, sin valores faltantes.

---

## 4. Metodología

### 4.1 Flujo de trabajo

```
Carga (carga.py) → Tratamiento (limpieza.py) → Descriptiva (descriptiva.py)
     → Inferencial H1–H6 (inferencial.py) → Modelado (modelado.py)
     → Réplica en SPSS (analisis_wine.sps) → Sitio web (exportar_web.py, web/)
```

Todo el pipeline se ejecuta con `python src/main.py`.

### 4.2 Tratamiento de datos
1. Unión de los archivos de tinto y blanco con la columna `tipo`.
2. Revisión de tipos y nulos (tabla 01).
3. Eliminación de registros duplicados.
4. Detección de atípicos con el criterio IQR (fuera de Q1 − 1.5·IQR, Q3 + 1.5·IQR) y z-score (|z| > 3) (tabla 02).
5. **Winsorización** al percentil 1–99: en lugar de eliminar los atípicos (muchos son valores químicamente plausibles, sobre todo en tintos), se recortan a esos límites para reducir su influencia sin perder observaciones.
6. Creación de variables derivadas y versión **normalizada (z-score)** para modelado.
7. Exportación de `data/processed/wine_limpio.csv` (para SPSS) y `wine_normalizado.csv`.

### 4.3 Elección de pruebas
Como ninguna variable resultó normal (H1), cada prueba paramétrica se acompañó de su alternativa no paramétrica: Pearson + Spearman (H2), t de Welch + Mann-Whitney (H3), ANOVA + Kruskal-Wallis con Levene y post-hoc de Tukey (H4). Para la asociación entre variables categóricas se usó χ² de independencia con V de Cramér (H5), y para el modelo global, regresión OLS con diagnóstico VIF (H6). Con n = 5,320, por el teorema del límite central las pruebas sobre medias son robustas a la falta de normalidad.

### 4.4 Diseño del modelo predictivo
- Partición entrenamiento/prueba 80/20 con semilla 42 (estratificada en clasificación).
- Predictoras: las 11 variables fisicoquímicas + `tipo_num`; estandarización para los modelos lineales.
- **Regresión** de la calidad (0–10): regresión lineal vs Random Forest Regressor (300 árboles); métricas RMSE, MAE, R² y exactitud al redondear.
- **Clasificación** de “buen vino” (≥ 7): regresión logística vs Random Forest (300 árboles), ambos con `class_weight="balanced"` por el desbalance de clases (≈ 19 % positivos).

---

## 5. Resultados

### 5.1 Tratamiento de datos

| Concepto | Valor |
|---|---|
| Filas originales | 6,497 |
| Valores nulos | 0 |
| Duplicados eliminados | 1,177 (18.1 %) |
| Filas finales | 5,320 (tinto 1,359 · blanco 3,961) |

**Tabla 02 — Valores atípicos (antes de winsorizar)**

| Variable | Atípicos IQR | % | Atípicos \|z\|>3 |
|---|---|---|---|
| Acidez fija | 304 | 5.71 | 108 |
| Acidez volátil | 279 | 5.24 | 77 |
| Cloruros | 237 | 4.45 | 94 |
| Sulfatos | 163 | 3.06 | 63 |
| Ácido cítrico | 143 | 2.69 | 26 |
| Azúcar residual | 141 | 2.65 | 42 |
| pH | 49 | 0.92 | 32 |
| SO₂ libre | 44 | 0.83 | 27 |
| SO₂ total | 10 | 0.19 | 8 |
| Densidad | 3 | 0.06 | 3 |
| Alcohol | 1 | 0.02 | 2 |

Las variables con más atípicos son las relacionadas con la acidez y los cloruros, que además son las que más difieren entre tintos y blancos.

### 5.2 Estadística descriptiva

**Tabla 03 — Resumen general (n = 5,320, datos winsorizados)**

| Variable | Media | Mediana | Desv. est. | CV % | Asimetría | Curtosis |
|---|---|---|---|---|---|---|
| Acidez fija | 7.21 | 7.00 | 1.27 | 17.6 | 1.38 | 2.59 |
| Acidez volátil | 0.343 | 0.30 | 0.163 | 47.5 | 1.27 | 1.23 |
| Ácido cítrico | 0.318 | 0.31 | 0.144 | 45.2 | 0.19 | 0.67 |
| Azúcar residual | 5.02 | 2.70 | 4.37 | 87.0 | 1.24 | 0.58 |
| Cloruros | 0.056 | 0.047 | 0.029 | 52.0 | 2.38 | 7.69 |
| SO₂ libre | 29.8 | 28.0 | 16.9 | 56.5 | 0.53 | −0.34 |
| SO₂ total | 113.9 | 116.0 | 56.1 | 49.3 | −0.03 | −0.68 |
| Densidad | 0.9945 | 0.9946 | 0.0029 | 0.3 | −0.01 | −0.87 |
| pH | 3.22 | 3.21 | 0.157 | 4.9 | 0.30 | −0.16 |
| Sulfatos | 0.532 | 0.51 | 0.139 | 26.2 | 0.98 | 1.19 |
| Alcohol | 10.55 | 10.40 | 1.18 | 11.2 | 0.52 | −0.68 |
| **Calidad** | **5.80** | **6** | **0.88** | 15.2 | 0.15 | 0.30 |

**Interpretación.**
- El **azúcar residual** es la variable más heterogénea (CV = 87 %): su media (5.0) está muy por encima de la mediana (2.7) por la presencia de blancos semisecos.
- Los **cloruros** tienen la mayor asimetría y curtosis (cola larga a la derecha).
- La **densidad** y el **pH** casi no varían (CV < 5 %).
- **Tinto vs blanco (tablas 03 por tipo):** los tintos tienen mayor acidez fija (8.27 vs 6.84), acidez volátil (0.52 vs 0.28), cloruros (0.085 vs 0.046) y sulfatos (0.65 vs 0.49); los blancos tienen mucho más azúcar residual (5.88 vs 2.52) y SO₂ total (136.9 vs 46.8). La calidad media es 5.62 en tintos y 5.85 en blancos.

**Tabla 04 — Distribución de la calidad**

| Calidad | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|
| Blanco | 20 | 153 | 1,175 | 1,788 | 689 | 131 | 5 |
| Tinto | 10 | 53 | 577 | 535 | 167 | 17 | 0 |
| % total | 0.56 | 3.87 | 32.93 | 43.67 | 16.09 | 2.78 | 0.09 |

El 76.6 % de los vinos tiene calidad 5 o 6; los extremos (3, 4, 8 y 9) suman apenas 7.3 %. Ningún vino obtuvo 0–2 ni 10. Este **desbalance** limita la capacidad de los modelos para reconocer vinos excepcionales o muy malos.

**Figuras:** `01_distribucion_calidad.png`, `02_histogramas.png`, `03_boxplots_calidad.png`, `04_heatmap_correlacion.png`, `05_alcohol_vs_calidad.png`.

En la matriz de correlación (figura 04, tabla 05) destacan, entre predictoras, densidad–alcohol (r = −0.69), SO₂ libre–SO₂ total (r = 0.73) y azúcar residual–densidad (r = 0.50): el alcohol y el azúcar determinan en buena parte la densidad del vino.

### 5.3 Estadística inferencial

#### H1 — Normalidad (D'Agostino K² y Kolmogorov-Smirnov)

Las 12 variables rechazan H₀ con p < 0.001 en ambas pruebas (tabla 06). Ejemplos: cloruros K² = 2,700.7; alcohol K² = 458.8; calidad K² = 34.5.
**Decisión:** se rechaza H₀ para todas. **Interpretación:** ninguna variable es normal, lo que justifica reportar también pruebas no paramétricas.

#### H2 — Correlación con la calidad

| Variable | Pearson r | Spearman ρ | p (Pearson) |
|---|---|---|---|
| Alcohol | **0.470** | 0.480 | < 0.001 |
| Densidad | **−0.336** | −0.349 | < 0.001 |
| Acidez volátil | **−0.262** | −0.251 | < 0.001 |
| Cloruros | **−0.231** | −0.304 | < 0.001 |
| Ácido cítrico | 0.101 | 0.116 | < 0.001 |
| Acidez fija | −0.083 | −0.104 | < 0.001 |
| SO₂ libre | 0.072 | 0.090 | < 0.001 |
| Azúcar residual | −0.058 | −0.028 | < 0.001 |
| Sulfatos | 0.054 | 0.036 | < 0.001 |
| SO₂ total | −0.046 | −0.058 | 0.0008 |
| pH | 0.040 | 0.053 | 0.0038 |

**Decisión:** se rechaza H₀ para las 11 variables. **Interpretación:** aunque todas son estadísticamente significativas (por el tamaño de muestra), solo el alcohol tiene una correlación moderada; densidad, acidez volátil y cloruros tienen correlaciones débiles negativas; el resto son prácticamente despreciables (|r| < 0.11).

#### H3 — Calidad de tintos vs blancos

| Prueba | Estadístico | p-valor |
|---|---|---|
| t de Welch | t = −8.757 | 3.6 × 10⁻¹⁸ |
| Mann-Whitney U | U = 2,290,875 | 2.0 × 10⁻¹⁸ |
| d de Cohen | −0.27 | — |

Medias: tinto 5.62, blanco 5.85. **Decisión:** se rechaza H₀. **Interpretación:** los blancos reciben en promedio 0.23 puntos más, pero el efecto es **pequeño** (|d| ≈ 0.27).

#### H4 — Alcohol según categoría de calidad

| Prueba | Estadístico | p-valor |
|---|---|---|
| Levene | 114.77 | 1.6 × 10⁻⁴⁹ |
| ANOVA de una vía | F = 901.06 | < 0.001 |
| Kruskal-Wallis | H = 1,302.25 | 1.7 × 10⁻²⁸³ |
| η² | 0.253 | — |

**Post-hoc de Tukey (tabla 10):** todas las parejas difieren (p < 0.001). Diferencia de medias de alcohol: alta − baja = 1.65 %vol; alta − media = 0.92; media − baja = 0.73.
**Decisión:** se rechaza H₀. **Interpretación:** el alcohol aumenta de forma escalonada con la calidad y la categoría explica el 25 % de su variabilidad (efecto **grande**). Como Levene indica varianzas desiguales, el resultado se confirma con Kruskal-Wallis.

#### H5 — Tipo de vino × categoría de calidad

| Tipo | Baja | Media | Alta |
|---|---|---|---|
| Blanco | 1,348 (34.0 %) | 1,788 (45.1 %) | 825 (20.8 %) |
| Tinto | 640 (47.1 %) | 535 (39.4 %) | 184 (13.5 %) |

χ² = 82.26, gl = 2, p = 1.4 × 10⁻¹⁸, V de Cramér = 0.124.
**Decisión:** se rechaza H₀. **Interpretación:** el tipo y la categoría están asociados — los tintos se concentran más en calidad baja y los blancos en media y alta —, aunque la asociación es **débil**.

#### H6 — Regresión lineal múltiple

R² = 0.317, R² ajustado = 0.315, F(12, 5307) = 205.1, p < 0.001.

| Predictor | β | t | p |
|---|---|---|---|
| Acidez volátil | −1.313 | −14.29 | < 0.001 |
| Sulfatos | 0.879 | 9.80 | < 0.001 |
| Alcohol | 0.202 | 9.40 | < 0.001 |
| Azúcar residual | 0.062 | 8.98 | < 0.001 |
| SO₂ libre | 0.008 | 8.89 | < 0.001 |
| Densidad | −128.69 | −7.43 | < 0.001 |
| pH | 0.713 | 6.93 | < 0.001 |
| Tipo (tinto) | 0.376 | 5.88 | < 0.001 |
| Acidez fija | 0.102 | 5.53 | < 0.001 |
| SO₂ total | −0.0017 | −4.60 | < 0.001 |
| Cloruros | −0.785 | −1.66 | 0.098 |
| Ácido cítrico | 0.139 | 1.54 | 0.125 |

**Decisión:** se rechaza H₀ (al menos un β ≠ 0). **Interpretación:** el modelo explica el 31.7 % de la variación de la calidad; 10 de 12 predictores son significativos. Manteniendo lo demás constante, cada g/dm³ adicional de acidez volátil reduce la calidad en 1.3 puntos y cada grado de alcohol la aumenta en 0.2. Cloruros y ácido cítrico no aportan información adicional una vez considerados los demás.

**Multicolinealidad (tabla 14):** la densidad tiene VIF = 24.7 (> 10) y el azúcar residual 9.1, consistente con que la densidad depende del alcohol y del azúcar. Por eso el coeficiente de la densidad (−128.7) no debe interpretarse aisladamente; un modelo sin densidad sería más interpretable con una pérdida mínima de R². Los residuos no son perfectamente normales (Jarque-Bera p < 0.001), lo cual es esperable porque la calidad es discreta.

### 5.4 Resultados en SPSS

La sintaxis `spss/analisis_wine.sps` se ejecutó en IBM SPSS Statistics sobre `data/processed/wine_limpio.csv` (n = 5,320). Visor completo: `resultados analisis de vino.spv` (anexo E). _Insertar aquí las capturas de las tablas principales._

| Procedimiento SPSS | Resultado principal |
|---|---|
| **Explorar** (H1) | Kolmogorov-Smirnov y Shapiro-Wilk con p < .001 en las tres categorías de calidad para alcohol, acidez volátil y sulfatos → no normalidad. Ejemplo: alcohol en calidad baja, S-W = 0.917. |
| **Correlaciones** (H2) | Pearson calidad–alcohol r = .470\*\*, densidad −.336\*\*, acidez volátil −.262\*\*. Mismos 11 coeficientes que Python. |
| **Prueba T** (H3) | Levene F = 0.784, p = .376. t de Student = −8.428 (gl 5318); t de Welch = −8.757 (gl 2527.0), p < .001. Diferencia de medias −0.232, IC 95 % [−0.283, −0.180]. d de Cohen = −0.265. |
| **U de Mann-Whitney** (H3) | U = 2,290,875, Z = −8.757, p < .001 |
| **ANOVA de un factor** (H4) | Levene (media) = 112.48, p < .001. F(2, 5317) = 901.06, p < .001. Welch robusto = 947.41, p < .001. η² = .253. Tukey y Games-Howell: las tres parejas difieren. |
| **Kruskal-Wallis** (H4) | H = 1,302.25, gl = 2, p < .001 |
| **Tablas cruzadas** (H5) | χ² de Pearson = 82.261, gl = 2, p < .001. Razón de verosimilitud = 82.294. V de Cramér = .124. Ninguna casilla con frecuencia esperada < 5 (mínima 257.75). |
| **Regresión lineal** (H6, método Introducir) | R = .728, R² = .317, R² ajustado = .315. F(12, 5307) = 205.15, p < .001. Durbin-Watson = 1.770. Coeficientes y VIF idénticos a los de Python (densidad VIF = 24.69). |
| **Regresión logística** (buen vino, por pasos hacia adelante RV) | 11 pasos. Modelo final: χ² ómnibus = 1,246.85 (gl 11, p < .001), R² de Nagelkerke = .336, R² de Cox y Snell = .209, Hosmer-Lemeshow χ² = 18.08 (gl 8, p = .021). Clasificación global 82.7 %: 94.9 % de "no buenos" y 30.8 % de "buenos" (punto de corte .5). |

**Nota sobre la regresión logística.** Con punto de corte 0.5 y sin balancear clases, SPSS clasifica bien casi todos los vinos “no buenos”, pero solo el 30.8 % de los buenos. En Python se usó `class_weight="balanced"`, lo que sube la sensibilidad a 78.7 % a costa de la precisión. Ambas son válidas; la diferencia muestra el efecto del desbalance de clases. La prueba de Hosmer-Lemeshow (p = .021) sugiere un ajuste de calibración imperfecto, algo habitual con n grande.

### 5.5 Comparativa Python vs SPSS

| Prueba | Python | SPSS | ¿Coincide? |
|---|---|---|---|
| H2 — r Pearson (alcohol) | 0.4700 | 0.470 | ✓ |
| H3 — t de Welch (tinto vs blanco) | −8.7568 | −8.757 | ✓ |
| H3 — p | 3.6 × 10⁻¹⁸ | .000 | ✓ |
| H4 — F ANOVA | 901.063 | 901.063 | ✓ |
| H4 — p | < 0.001 | .000 | ✓ |
| H5 — χ² | 82.261 | 82.261 | ✓ |
| H5 — p | 1.4 × 10⁻¹⁸ | .000 | ✓ |
| H6 — R² | 0.3169 | 0.317 | ✓ |
| H6 — F | 205.147 | 205.147 | ✓ |
| *Extra:* Kruskal-Wallis H | 1,302.25 | 1,302.25 | ✓ |
| *Extra:* η² ANOVA | 0.2531 | 0.253 | ✓ |
| *Extra:* V de Cramér | 0.1243 | 0.124 | ✓ |
| *Extra:* VIF densidad | 24.689 | 24.689 | ✓ |

**Interpretación.** Los valores de Python y SPSS coinciden en todos los decimales reportados, lo que valida que el análisis es reproducible en ambas herramientas. SPSS muestra los p-valores muy pequeños como “.000”, lo que equivale a p < 0.001. Las únicas diferencias son de método, no numéricas:
- La normalidad se probó con D'Agostino/KS en Python y con KS/Shapiro-Wilk en SPSS; ambas rechazan normalidad.
- La regresión logística se ajustó por pasos en SPSS y con todas las variables y clases balanceadas en Python.

### 5.6 Modelo predictivo

**Tabla 15 — Regresión de la calidad (conjunto de prueba, n = 1,064)**

| Modelo | RMSE | MAE | R² | Exactitud al redondear |
|---|---|---|---|---|
| Regresión lineal | 0.718 | 0.560 | 0.314 | 53.4 % |
| Random Forest | **0.661** | **0.507** | **0.418** | **58.9 %** |

**Tabla 16 — Clasificación “buen vino” (calidad ≥ 7)**

| Modelo | Accuracy | Precisión | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Regresión logística | 0.734 | 0.398 | **0.787** | 0.529 | 0.818 |
| Random Forest | **0.847** | **0.592** | 0.619 | **0.605** | **0.878** |

**Matriz de confusión del Random Forest (figura 07):** de 862 vinos “no buenos” clasificó bien 776 (90 %); de 202 vinos “buenos” detectó 125 (62 %).

**Importancia de variables (tabla 18, figura 06):** alcohol (0.199) y densidad (0.121) son las más importantes, seguidas de cloruros (0.089), acidez volátil (0.087) y SO₂ total (0.083). El tipo de vino casi no aporta (0.003).

**Interpretación.** El Random Forest supera a los modelos lineales en ambas tareas porque capta relaciones no lineales e interacciones. En regresión, el error medio es de medio punto en la escala de calidad. En clasificación, la regresión logística detecta más vinos buenos (recall 0.79) pero con muchos falsos positivos; el Random Forest ofrece un mejor equilibrio (F1 0.61) y mayor capacidad de discriminación (AUC 0.88). El sitio web (`web/index.html`) incluye un **simulador** que permite ingresar valores químicos y ver la predicción.

---

## 6. Discusión

- **Variables más influyentes.** Todas las técnicas coinciden en que el **alcohol** es el factor más asociado a una mejor calidad, y que la **acidez volátil** (asociada al sabor a vinagre) y la **densidad** se relacionan con peor calidad. Los sulfatos son significativos en la regresión múltiple aunque su correlación simple sea débil, lo que indica un efecto que aparece al controlar las demás variables.
- **Comparación con Cortez et al. (2009).** Nuestros hallazgos coinciden con el artículo original, que también identificó al alcohol, los sulfatos y la acidez volátil entre las variables más relevantes. Ellos obtuvieron sus mejores resultados con SVM; nosotros, con Random Forest, confirmamos que los modelos no lineales superan a la regresión lineal.
- **Tinto vs blanco.** Las diferencias químicas entre tipos son grandes (acidez, azúcar, SO₂), pero la diferencia en calidad es pequeña (d = 0.27) y la asociación tipo–calidad es débil (V = 0.12).
- **Significancia estadística vs práctica.** Con más de 5,000 observaciones, incluso correlaciones de 0.04 resultan significativas; por eso se reportaron tamaños de efecto.

**Limitaciones.**
1. **Desbalance de clases:** pocos vinos con calidad extrema, lo que dificulta predecirlos.
2. **Calidad subjetiva:** la calificación es la mediana de catadores y tiene un componente de gusto personal.
3. **Variables omitidas:** no se dispone de tipo de uva, marca, añada ni precio (por confidencialidad), que probablemente explican parte de la variabilidad restante.
4. **Duplicados:** se eliminó el 18 % de los registros; algunos podrían ser vinos distintos con mediciones idénticas.
5. **Multicolinealidad** entre densidad, alcohol y azúcar, que dificulta interpretar coeficientes individuales.

---

## 7. Conclusiones y trabajo futuro

1. El tratamiento de datos (sin nulos, 1,177 duplicados eliminados, winsorización de atípicos) dejó una base de 5,320 vinos lista para el análisis en Python y SPSS.
2. Ninguna variable sigue una distribución normal, por lo que se complementaron las pruebas paramétricas con no paramétricas, obteniendo las mismas conclusiones.
3. El **alcohol** es la propiedad con mayor influencia positiva en la calidad (r = 0.47; η² = 0.25 entre categorías), mientras que la **acidez volátil**, la **densidad** y los **cloruros** influyen negativamente.
4. Los vinos blancos obtienen calificaciones ligeramente mayores que los tintos, pero el efecto es pequeño.
5. Las propiedades fisicoquímicas explican alrededor de un tercio de la variabilidad de la calidad con un modelo lineal (R² = 0.32) y hasta 42 % con Random Forest; para identificar vinos de calidad ≥ 7, el Random Forest alcanzó 85 % de exactitud y AUC = 0.88.
6. Los datos de laboratorio pueden apoyar, pero no sustituir por completo, la evaluación sensorial.

**Trabajo futuro:** modelos separados por tipo de vino; técnicas de balanceo (SMOTE) para las calidades extremas; validación cruzada y ajuste de hiperparámetros; probar SVM y gradient boosting; regresión ordinal, que respeta la naturaleza ordinal de la calidad.

---

## Referencias (APA 7)

- Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Modeling wine preferences by data mining from physicochemical properties. *Decision Support Systems, 47*(4), 547–553. https://doi.org/10.1016/j.dss.2009.05.016
- Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). *Wine Quality* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56S3T
- Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature, 585*, 357–362. https://doi.org/10.1038/s41586-020-2649-2
- IBM Corp. (2023). *IBM SPSS Statistics for Windows* (Versión 29.0) [Software]. IBM Corp.
- McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56–61.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830.
- Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. *Proceedings of the 9th Python in Science Conference*, 92–96.
- Virtanen, P., et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods, 17*, 261–272. https://doi.org/10.1038/s41592-019-0686-2

_(Ajusten la versión de SPSS a la que usen.)_

---

## Anexos

- **A. Código fuente:** `src/` (`carga.py`, `limpieza.py`, `descriptiva.py`, `inferencial.py`, `modelado.py`, `exportar_web.py`, `main.py`).
- **B. Sintaxis SPSS:** `spss/analisis_wine.sps`.
- **C. Salidas completas:** `outputs/tablas/13_H6_regresion_OLS.txt`, `outputs/tablas/17_reporte_clasificacion.txt` y el resto de tablas 01–18.
- **D. Investigación del dataset:** `docs/Investigacion_Dataset_Trabajo_Final.pdf`.
- **E. Salida de SPSS:** `spss/resultados_analisis_de_vino.spv` (abrir con IBM SPSS Statistics).
