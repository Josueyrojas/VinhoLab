# Plan de trabajo

> Propuesta de reparto; ajústenla entre el equipo.

## Roles

| Integrante | Rol | Responsabilidades | Archivos |
|---|---|---|---|
| Angel Alejandro Adrian Cruz Cruz | Líder / integración | Coordinación, integración del reporte final, introducción, conclusiones, ensayo de la exposición | `docs/`, reporte final |
| Josué Yañez Rojas | Tratamiento de datos, modelado y sitio web | Carga, limpieza, outliers, normalización, modelos predictivos, sitio de presentación, repositorio | `carga.py`, `limpieza.py`, `modelado.py`, `exportar_web.py`, `web/` |
| Roberto Emmanuel Duran Castillo | Estadística descriptiva (Python) | Tablas descriptivas, gráficas, interpretación de distribuciones | `descriptiva.py`, `outputs/figuras/` |
| Andrea Guadalupe Rodriguez Patiño | Estadística inferencial (Python) | Pruebas de hipótesis H1–H6, interpretación de p-valores y tamaños de efecto | `inferencial.py`, `outputs/tablas/` |
| Enrique Gallegos Linares | SPSS | Ejecución de la sintaxis, capturas de resultados, tabla comparativa Python vs SPSS | `spss/` |

## Fases y entregables

| # | Fase | Entregable | Responsable |
|---|---|---|---|
| 0 | Investigación del dataset | PDF de investigación (✔ entregado) | Todos |
| 1 | Preparación del entorno | Repo, `requirements.txt`, dataset en `data/raw/` | Josué |
| 2 | Tratamiento de datos | `wine_limpio.csv`, tablas 01–02 | Josué |
| 3 | Estadística descriptiva | Tablas 03–05, figuras 01–05 | Roberto |
| 4 | Estadística inferencial | Tablas 06–14 | Andrea |
| 5 | Análisis en SPSS | Salidas del visor + tabla comparativa | Enrique |
| 6 | Modelo predictivo | Tablas 15–18, figuras 06–07 | Josué |
| 7 | Reporte final | Documento (ver `estructura_reporte.md`) | Angel + todos |
| 8 | Sitio web | `web/index.html` publicado (Netlify / GitHub Pages) | Josué |
| 9 | Presentación | Exposición recorriendo el sitio + demo del simulador | Todos |

## Checklist de entrega

- [ ] Autor del dataset citado en APA (Cortez et al., 2009)
- [ ] Tratamiento de datos documentado (antes/después: filas, duplicados, outliers)
- [ ] Descriptiva en Python **y** SPSS
- [ ] Inferencial en Python **y** SPSS, con H0/H1, estadístico, p-valor y decisión
- [ ] Tabla comparativa de resultados Python vs SPSS
- [ ] Modelo predictivo con métricas e interpretación
- [ ] Código fuente + sintaxis `.sps` en anexos
