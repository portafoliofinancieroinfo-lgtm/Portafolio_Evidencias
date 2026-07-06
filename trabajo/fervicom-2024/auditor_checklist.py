"""
Auditor de checklist de auditoría interna.

Inspirado en las auditorías internas que diseñé y ejecuté en FERVICOM S.A.S.
(2024-2025) para los procesos de ingresos, egresos, cartera, activos fijos,
impuestos y nómina.

Este script trabaja sobre un checklist sintético (no son datos reales de
ninguna empresa) y automatiza el tipo de revisión que hice manualmente:
valida que cada ítem marcado como "Cumple" tenga evidencia y firma del
responsable, y calcula el nivel de riesgo por proceso.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

RNG = np.random.default_rng(seed=3)
CARPETA = Path(__file__).parent
EVIDENCIA = CARPETA / "evidencia"
PROCESOS = ["Ingresos", "Egresos", "Cartera", "Activos fijos", "Impuestos", "Nómina"]
ITEMS_POR_PROCESO = 8


def generar_checklist() -> pd.DataFrame:
    filas = []
    for proceso in PROCESOS:
        for i in range(1, ITEMS_POR_PROCESO + 1):
            filas.append({
                "proceso": proceso,
                "item": f"{proceso[:3].upper()}-{i:02d}",
                "responsable": f"Analista {RNG.integers(1, 5)}",
                "estado": "Cumple",
                "evidencia_adjunta": True,
                "firma_responsable": True,
            })
    df = pd.DataFrame(filas)

    # Defectos de calidad, a propósito, para que el auditor los detecte.
    idx_sin_evidencia = RNG.choice(df.index, size=6, replace=False)
    df.loc[idx_sin_evidencia, "evidencia_adjunta"] = False

    idx_sin_firma = RNG.choice(df.index, size=5, replace=False)
    df.loc[idx_sin_firma, "firma_responsable"] = False

    df = pd.concat([df, df.iloc[[10]]], ignore_index=True)  # ítem duplicado

    return df


def auditar(df: pd.DataFrame) -> dict:
    hallazgos = {}

    duplicados = df[df.duplicated(subset=["proceso", "item"], keep=False)]
    hallazgos["items_duplicados"] = duplicados

    df_unico = df.drop_duplicates(subset=["proceso", "item"])

    inconsistentes = df_unico[(df_unico["estado"] == "Cumple") & (~df_unico["evidencia_adjunta"])]
    hallazgos["cumple_sin_evidencia"] = inconsistentes

    sin_firma = df_unico[~df_unico["firma_responsable"]]
    hallazgos["sin_firma_responsable"] = sin_firma

    sin_responsable = df_unico[df_unico["responsable"].fillna("").str.strip() == ""]
    hallazgos["sin_responsable_asignado"] = sin_responsable

    hallazgos_por_item = set(inconsistentes.index) | set(sin_firma.index) | set(sin_responsable.index)
    riesgo_por_proceso = (
        df_unico.assign(tiene_hallazgo=df_unico.index.isin(hallazgos_por_item))
        .groupby("proceso")["tiene_hallazgo"].sum()
        .reindex(PROCESOS, fill_value=0)
    )
    hallazgos["riesgo_por_proceso"] = riesgo_por_proceso

    return hallazgos


def clasificar_riesgo(cantidad_hallazgos: int) -> str:
    if cantidad_hallazgos >= 3:
        return "Alto"
    if cantidad_hallazgos >= 1:
        return "Medio"
    return "Bajo"


def generar_grafico(hallazgos: dict) -> Path:
    EVIDENCIA.mkdir(exist_ok=True)
    ruta = EVIDENCIA / "metricas.png"

    riesgo = hallazgos["riesgo_por_proceso"]
    colores = {"Alto": "#c0392b", "Medio": "#f39c12", "Bajo": "#27ae60"}
    colores_barras = [colores[clasificar_riesgo(v)] for v in riesgo.values]

    fig, ax = plt.subplots(figsize=(7, 4))
    barras = ax.bar(riesgo.index, riesgo.values, color=colores_barras)
    ax.set_ylabel("Hallazgos (sin evidencia o sin firma)")
    ax.set_title("Riesgo por proceso — auditoría interna (checklist sintético)")
    ax.tick_params(axis="x", rotation=20)
    for barra, valor in zip(barras, riesgo.values):
        ax.text(barra.get_x() + barra.get_width() / 2, valor, str(valor), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def imprimir_reporte(hallazgos: dict) -> None:
    print("=== Auditor de checklist de auditoría interna ===\n")
    print(f"Ítems duplicados en el checklist: {len(hallazgos['items_duplicados'])}")
    print(f"Marcados 'Cumple' sin evidencia adjunta: {len(hallazgos['cumple_sin_evidencia'])}")
    print(f"Sin firma del responsable: {len(hallazgos['sin_firma_responsable'])}")
    print(f"Sin responsable asignado: {len(hallazgos['sin_responsable_asignado'])}\n")
    print("Riesgo por proceso:")
    for proceso, cantidad in hallazgos["riesgo_por_proceso"].items():
        print(f"  {proceso:<15} {clasificar_riesgo(cantidad):<6} ({cantidad} hallazgos)")


def main() -> None:
    df = generar_checklist()
    hallazgos = auditar(df)
    imprimir_reporte(hallazgos)
    ruta_grafico = generar_grafico(hallazgos)
    print(f"\nGráfico guardado en: {ruta_grafico}")


if __name__ == "__main__":
    main()
