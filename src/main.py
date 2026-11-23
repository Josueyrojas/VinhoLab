"""Ejecuta el pipeline completo:
carga -> limpieza -> descriptiva -> inferencial -> modelado -> exportación al sitio web.

Uso (desde la raíz del proyecto):
    python src/main.py
Después abre web/index.html en el navegador.
"""
from carga import cargar_datos
from limpieza import limpiar
from descriptiva import descriptiva
from inferencial import inferencial
from modelado import modelado
from exportar_web import exportar_web


def main():
    df = cargar_datos()
    df = limpiar(df)
    descriptiva(df)
    salidas, modelo_ols = inferencial(df)
    res_modelo = modelado(df)
    exportar_web(df, salidas, modelo_ols, res_modelo)
    print("\n✔ Pipeline completo. Abre web/index.html para ver los resultados.")


if __name__ == "__main__":
    main()
