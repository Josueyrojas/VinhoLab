* ==========================================================================.
* Proyecto: Predicción y Análisis de la Calidad del Vino Verde Portugués.
* Sintaxis SPSS — replica el análisis de Python para comparar resultados.
* Antes de ejecutar: correr "python src/main.py" para generar wine_limpio.csv
* y AJUSTAR la ruta del archivo en GET DATA.
* ==========================================================================.

* -------- 1. Carga de datos --------.
GET DATA
  /TYPE=TXT
  /FILE="C:\Users\agrod\VinhoLab\data\processed\wine_limpio.csv"
  /ENCODING='UTF8'
  /DELIMITERS=","
  /QUALIFIER='"'
  /ARRANGEMENT=DELIMITED
  /FIRSTCASE=2
  /VARIABLES=
    fixed_acidity F8.3
    volatile_acidity F8.3
    citric_acid F8.3
    residual_sugar F8.3
    chlorides F8.4
    free_sulfur_dioxide F8.2
    total_sulfur_dioxide F8.2
    density F10.5
    pH F8.3
    sulphates F8.3
    alcohol F8.2
    quality F2.0
    tipo A10
    calidad_cat A10
    buen_vino F1.0
    tipo_num F1.0.
EXECUTE.
DATASET NAME wine WINDOW=FRONT.

VARIABLE LABELS
  fixed_acidity 'Acidez fija'
  volatile_acidity 'Acidez volátil'
  citric_acid 'Ácido cítrico'
  residual_sugar 'Azúcar residual'
  chlorides 'Cloruros'
  free_sulfur_dioxide 'SO2 libre'
  total_sulfur_dioxide 'SO2 total'
  density 'Densidad'
  pH 'pH'
  sulphates 'Sulfatos'
  alcohol 'Alcohol (% vol)'
  quality 'Calidad (0-10)'
  tipo 'Tipo de vino'
  calidad_cat 'Categoría de calidad'
  buen_vino 'Buen vino (calidad >= 7)'
  tipo_num 'Tipo (1 = tinto, 0 = blanco)'.

* Categoría de calidad numérica para ANOVA/Tukey.
RECODE quality (LO THRU 5=1) (6=2) (7 THRU HI=3) INTO cal_cat_num.
VARIABLE LABELS cal_cat_num 'Categoría de calidad'.
VALUE LABELS cal_cat_num 1 'Baja' 2 'Media' 3 'Alta'
  /buen_vino 0 'No' 1 'Sí'
  /tipo_num 0 'Blanco' 1 'Tinto'.
VARIABLE LEVEL quality cal_cat_num (ORDINAL) /buen_vino tipo_num (NOMINAL).
EXECUTE.

* -------- 2. Estadística descriptiva --------.
DESCRIPTIVES VARIABLES=fixed_acidity TO quality
  /STATISTICS=MEAN STDDEV VARIANCE RANGE MIN MAX SEMEAN KURTOSIS SKEWNESS.

FREQUENCIES VARIABLES=quality cal_cat_num tipo
  /STATISTICS=MEAN MEDIAN MODE
  /BARCHART FREQ
  /ORDER=ANALYSIS.

MEANS TABLES=fixed_acidity TO alcohol BY tipo_num
  /CELLS=MEAN COUNT STDDEV MEDIAN.

* -------- 3. H1: Normalidad (K-S y Shapiro-Wilk) + boxplots --------.
EXAMINE VARIABLES=alcohol volatile_acidity sulphates quality BY cal_cat_num
  /PLOT BOXPLOT HISTOGRAM NPPLOT
  /STATISTICS DESCRIPTIVES
  /NOTOTAL.

* -------- 4. H2: Correlaciones con la calidad --------.
CORRELATIONS
  /VARIABLES=fixed_acidity volatile_acidity citric_acid residual_sugar chlorides
    free_sulfur_dioxide total_sulfur_dioxide density pH sulphates alcohol quality
  /PRINT=TWOTAIL NOSIG.

NONPAR CORR
  /VARIABLES=fixed_acidity TO quality
  /PRINT=SPEARMAN TWOTAIL NOSIG.

* -------- 5. H3: Calidad tinto vs blanco --------.
T-TEST GROUPS=tipo_num(1 0)
  /VARIABLES=quality alcohol
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).

NPAR TESTS /M-W=quality BY tipo_num(0 1).

* -------- 6. H4: ANOVA alcohol por categoría de calidad --------.
ONEWAY alcohol BY cal_cat_num
  /ES=OVERALL
  /STATISTICS DESCRIPTIVES HOMOGENEITY WELCH
  /PLOT MEANS
  /POSTHOC=TUKEY GH ALPHA(0.05).

NPAR TESTS /K-W=alcohol BY cal_cat_num(1 3).

* -------- 7. H5: Chi-cuadrado tipo x categoría de calidad --------.
CROSSTABS
  /TABLES=tipo_num BY cal_cat_num
  /STATISTICS=CHISQ PHI
  /CELLS=COUNT ROW EXPECTED.

* -------- 8. H6: Regresión lineal múltiple --------.
* METHOD=ENTER mete las 12 variables a la vez, igual que Python (R² = 0.317, F = 205.1).
* Si quieren el modelo por pasos, cambien ENTER por STEPWISE (R² y F ya no serán comparables).
REGRESSION
  /DESCRIPTIVES MEAN STDDEV CORR SIG N
  /STATISTICS COEFF OUTS R ANOVA COLLIN TOL CHANGE
  /DEPENDENT quality
  /METHOD=ENTER fixed_acidity volatile_acidity citric_acid residual_sugar chlorides
    free_sulfur_dioxide total_sulfur_dioxide density pH sulphates alcohol tipo_num
  /SCATTERPLOT=(*ZRESID ,*ZPRED)
  /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID) DURBIN.

* -------- 9. Regresión logística: buen vino (>= 7) --------.
LOGISTIC REGRESSION VARIABLES buen_vino
  /METHOD=FSTEP(LR) fixed_acidity volatile_acidity citric_acid residual_sugar chlorides
    free_sulfur_dioxide total_sulfur_dioxide density pH sulphates alcohol tipo_num
  /PRINT=GOODFIT CI(95)
  /CLASSPLOT
  /CRITERIA=PIN(.05) POUT(.10) ITERATE(20) CUT(.5).
