# Estructura del reporte final

**Predicción y Análisis de la Calidad del Vino Verde Portugués mediante Estadística Descriptiva, Inferencial y Tratamiento de Datos con Python y SPSS**

---

**Portada** — TecNM / Instituto Tecnológico de Celaya, materia, docente, equipo, fecha.

**Resumen** (150–250 palabras) — objetivo, datos, métodos, hallazgo principal (variables más influyentes y desempeño del modelo).

**1. Introducción**
1.1 Contexto: el vino verde portugués y la certificación de calidad sensorial
1.2 Planteamiento del problema
1.3 Objetivo general y objetivos específicos
1.4 Preguntas de investigación / hipótesis (H1–H6)
1.5 Justificación (retomar la sección 7 del PDF de investigación)

**2. Marco teórico**
2.1 Estadística descriptiva: tendencia central, dispersión, forma
2.2 Estadística inferencial: pruebas paramétricas y no paramétricas, nivel de significancia, tamaño de efecto
2.3 Correlación y regresión lineal múltiple; supuestos y multicolinealidad (VIF)
2.4 Clasificación: regresión logística y Random Forest; métricas
2.5 Herramientas: Python (pandas, scipy, statsmodels, scikit-learn) y SPSS
2.6 Trabajo previo: Cortez et al. (2009)

**3. Descripción del dataset**
3.1 Autor, fuente y licencia
3.2 Diccionario de datos (variable, descripción, unidad, tipo, escala de medición)
3.3 Tamaño: tinto 1,599 / blanco 4,898; 11 predictoras + 1 objetivo

**4. Metodología**
4.1 Diagrama del flujo (carga → limpieza → descriptiva → inferencial → modelado → SPSS)
4.2 Tratamiento de datos: nulos, duplicados, outliers (IQR / z>3), winsorización, variables derivadas, normalización
4.3 Pruebas estadísticas elegidas y por qué (normalidad → paramétrica vs no paramétrica)
4.4 Diseño del modelo: partición 80/20, semilla, métricas

**5. Resultados**
5.1 Tratamiento de datos — tablas 01, 02
5.2 Estadística descriptiva — tablas 03–05, figuras 01–05
5.3 Estadística inferencial — una subsección por hipótesis: H0/H1, estadístico, p-valor, decisión, interpretación (tablas 06–14)
5.4 Resultados en SPSS — capturas del visor
5.5 Comparativa Python vs SPSS (tabla: prueba | valor Python | valor SPSS | coincide)
5.6 Modelo predictivo — tablas 15–18, figuras 06–07

**6. Discusión**
— Variables más influyentes, comparación con Cortez et al. (2009), diferencias tinto vs blanco, limitaciones (desbalance de clases, calidad subjetiva, sin variables de precio/uva).

**7. Conclusiones y trabajo futuro**

**Referencias (APA 7)**
- Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Modeling wine preferences by data mining from physicochemical properties. *Decision Support Systems, 47*(4), 547–553. https://doi.org/10.1016/j.dss.2009.05.016
- Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). *Wine Quality* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56S3T
- Documentación de pandas, SciPy, statsmodels, scikit-learn e IBM SPSS Statistics.

**Anexos**
A. Código fuente (`src/`)
B. Sintaxis SPSS (`spss/analisis_wine.sps`)
C. Salidas completas (regresión OLS, reporte de clasificación)
