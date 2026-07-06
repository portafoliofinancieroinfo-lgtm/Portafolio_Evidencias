"""
Conciliador de movimientos bancarios vs. libro contable.

Inspirado en la reconstrucción contable que hice en Transervi S.A.S. (2022):
la vigencia 2021 completa estaba sin registrar (+3.000 documentos entre
facturas y movimientos bancarios), contra el reloj de los vencimientos de
exógena y renta.

Este script trabaja sobre un dataset sintético (no son datos reales de
ninguna empresa) y automatiza el tipo de conciliación que hice manualmente:
cruza el libro contable contra el extracto bancario y reporta movimientos sin
conciliar, diferencias de monto y registros duplicados.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

RNG = np.random.default_rng(seed=7)
CARPETA = Path(__file__).parent
EVIDENCIA = CARPETA / "evidencia"
N_MOVIMIENTOS = 3000
TOLERANCIA_MONTO = 1.0


def generar_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    ids = np.arange(1, N_MOVIMIENTOS + 1)
    fechas = pd.date_range("2021-01-01", "2021-12-31", periods=N_MOVIMIENTOS)
    montos = RNG.normal(loc=1_500_000, scale=400_000, size=N_MOVIMIENTOS).round(0)

    libro = pd.DataFrame({"id": ids, "fecha": fechas, "monto": montos})

    banco = libro.copy()

    # Movimientos que están en el banco pero nunca se registraron en el libro.
    sin_registrar = RNG.choice(ids, size=40, replace=False)
    libro = libro[~libro["id"].isin(sin_registrar)].reset_index(drop=True)

    # Movimientos registrados en el libro que no aparecen en el extracto bancario.
    sin_extracto = RNG.choice(libro["id"], size=25, replace=False)
    banco = banco[~banco["id"].isin(sin_extracto)].reset_index(drop=True)

    # Diferencias de monto por errores de digitación.
    idx_diferencias = RNG.choice(banco.index, size=15, replace=False)
    banco.loc[idx_diferencias, "monto"] += RNG.uniform(5_000, 50_000, size=15)

    # Registros duplicados en el libro (doble digitación).
    libro = pd.concat([libro, libro.sample(n=10, random_state=1)], ignore_index=True)

    return libro, banco


def conciliar(libro: pd.DataFrame, banco: pd.DataFrame) -> dict:
    hallazgos = {}

    duplicados_libro = libro[libro.duplicated(subset=["id"], keep=False)]
    hallazgos["duplicados_en_libro"] = duplicados_libro

    duplicados_banco = banco[banco.duplicated(subset=["id"], keep=False)]
    hallazgos["duplicados_en_banco"] = duplicados_banco

    libro_unico = libro.drop_duplicates(subset=["id"])
    banco_unico = banco.drop_duplicates(subset=["id"])
    cruce = libro_unico.merge(banco_unico, on="id", how="outer", suffixes=("_libro", "_banco"), indicator=True)

    sin_extracto = cruce[cruce["_merge"] == "left_only"]
    sin_registrar = cruce[cruce["_merge"] == "right_only"]
    hallazgos["sin_extracto_bancario"] = sin_extracto
    hallazgos["sin_registrar_en_libro"] = sin_registrar

    ambos = cruce[cruce["_merge"] == "both"].copy()
    ambos["diferencia"] = (ambos["monto_libro"] - ambos["monto_banco"]).abs()
    diferencias = ambos[ambos["diferencia"] > TOLERANCIA_MONTO]
    hallazgos["diferencias_de_monto"] = diferencias

    conciliados = ambos[ambos["diferencia"] <= TOLERANCIA_MONTO]
    hallazgos["conciliados"] = conciliados
    hallazgos["pct_conciliado"] = len(conciliados) / len(libro_unico) * 100

    return hallazgos


def generar_grafico(hallazgos: dict) -> Path:
    EVIDENCIA.mkdir(exist_ok=True)
    ruta = EVIDENCIA / "metricas.png"

    categorias = {
        "Diferencia\nde monto": len(hallazgos["diferencias_de_monto"]),
        "Sin extracto\nbancario": len(hallazgos["sin_extracto_bancario"]),
        "Sin registrar\nen libro": len(hallazgos["sin_registrar_en_libro"]),
        "Duplicados\nen libro": len(hallazgos["duplicados_en_libro"]),
        "Duplicados\nen banco": len(hallazgos["duplicados_en_banco"]),
    }

    fig, ax = plt.subplots(figsize=(7, 4))
    colores = ["#f39c12", "#e67e22", "#c0392b", "#8e44ad", "#2980b9"]
    barras = ax.bar(categorias.keys(), categorias.values(), color=colores)
    ax.set_ylabel("Cantidad de movimientos")
    ax.set_title(f"Hallazgos de conciliación — {hallazgos['pct_conciliado']:.1f}% conciliado (dataset sintético)")
    for barra, valor in zip(barras, categorias.values()):
        ax.text(barra.get_x() + barra.get_width() / 2, valor, str(valor), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def imprimir_reporte(hallazgos: dict) -> None:
    print("=== Conciliador de movimientos bancarios vs. libro contable ===\n")
    print(f"Movimientos conciliados:            {len(hallazgos['conciliados'])} ({hallazgos['pct_conciliado']:.1f}%)")
    print(f"Diferencias de monto:                {len(hallazgos['diferencias_de_monto'])}")
    print(f"Sin extracto bancario:                {len(hallazgos['sin_extracto_bancario'])}")
    print(f"Sin registrar en el libro:            {len(hallazgos['sin_registrar_en_libro'])}")
    print(f"Registros duplicados en el libro:    {len(hallazgos['duplicados_en_libro'])}")
    print(f"Registros duplicados en el banco:    {len(hallazgos['duplicados_en_banco'])}")


def main() -> None:
    libro, banco = generar_datasets()
    hallazgos = conciliar(libro, banco)
    imprimir_reporte(hallazgos)
    ruta_grafico = generar_grafico(hallazgos)
    print(f"\nGráfico guardado en: {ruta_grafico}")


if __name__ == "__main__":
    main()
