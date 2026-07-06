"""
Auditor de calidad de datos contables - caso ReteICA (Ley 56 de 1981).

Inspirado en el saneamiento contable que realicé en Electrovichada ESP S.A.
(2023): la empresa liquidaba el impuesto de ReteICA tomando la producción
TOTAL ANUAL de energía como base del período, cuando la Ley 56 de 1981 exige
liquidarlo sobre el PROMEDIO MENSUAL de producción. Ese error inflaba la base
gravable en más de un 1000%.

Este script trabaja sobre un dataset sintético (no son datos reales de
ninguna empresa) y automatiza el tipo de auditoría que hice manualmente:
detecta la base de ReteICA mal calculada, además de duplicados, montos
atípicos y fechas inconsistentes en el registro contable.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

RNG = np.random.default_rng(seed=42)
CARPETA = Path(__file__).parent
EVIDENCIA = CARPETA / "evidencia"
TASA_RETEICA_POR_KWH = 8.5


def generar_dataset() -> pd.DataFrame:
    meses = pd.date_range("2022-01-01", periods=12, freq="MS")
    produccion_kwh = RNG.normal(loc=4_500_000, scale=250_000, size=12).round(0)

    df = pd.DataFrame({"mes": meses, "produccion_kwh": produccion_kwh})

    # Defectos de calidad de datos, a propósito, para que el auditor los detecte.
    df.loc[3, "produccion_kwh"] = np.nan                   # mes con dato faltante
    df = pd.concat([df, df.iloc[[5]]], ignore_index=True)  # registro duplicado
    df.loc[8, "produccion_kwh"] *= 4                        # monto atípico (outlier)

    return df


def auditar(df: pd.DataFrame) -> dict:
    hallazgos = {}

    duplicados = df[df.duplicated(subset=["mes"], keep=False)]
    hallazgos["duplicados"] = duplicados

    faltantes = df[df["produccion_kwh"].isna()]
    hallazgos["fechas_con_datos_faltantes"] = faltantes

    q1, q3 = df["produccion_kwh"].quantile([0.25, 0.75])
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    atipicos = df[(df["produccion_kwh"] > limite_superior) | (df["produccion_kwh"] < limite_inferior)]
    hallazgos["montos_atipicos"] = atipicos

    df_valido = df.dropna(subset=["produccion_kwh"]).drop_duplicates(subset=["mes"])
    produccion_anual = df_valido["produccion_kwh"].sum()

    # Error real detectado: la empresa liquidaba el ReteICA tomando la
    # producción TOTAL ANUAL como base, en vez del PROMEDIO MENSUAL que
    # exige la Ley 56 de 1981 para el período de facturación.
    base_declarada = produccion_anual
    base_correcta = produccion_anual / 12

    impuesto_declarado = base_declarada * TASA_RETEICA_POR_KWH
    impuesto_correcto = base_correcta * TASA_RETEICA_POR_KWH
    ahorro = impuesto_declarado - impuesto_correcto

    hallazgos["impuesto_declarado"] = impuesto_declarado
    hallazgos["impuesto_correcto"] = impuesto_correcto
    hallazgos["ahorro_potencial"] = ahorro
    hallazgos["inflacion_pct"] = (impuesto_declarado / impuesto_correcto - 1) * 100

    return hallazgos


def generar_grafico(hallazgos: dict) -> Path:
    EVIDENCIA.mkdir(exist_ok=True)
    ruta = EVIDENCIA / "metricas.png"

    fig, ax = plt.subplots(figsize=(6, 4))
    valores = [hallazgos["impuesto_declarado"], hallazgos["impuesto_correcto"]]
    barras = ax.bar(["Base declarada\n(producción total anual)", "Base correcta\n(promedio mensual)"],
                     valores, color=["#c0392b", "#27ae60"])
    ax.set_ylabel("Impuesto ReteICA ($)")
    ax.set_title("Impacto de corregir la base gravable (dataset sintético)")
    for barra, valor in zip(barras, valores):
        ax.text(barra.get_x() + barra.get_width() / 2, valor, f"${valor:,.0f}",
                 ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def imprimir_reporte(hallazgos: dict) -> None:
    print("=== Auditor de calidad de datos contables — ReteICA ===\n")
    print(f"Registros duplicados encontrados: {len(hallazgos['duplicados'])}")
    print(f"Meses con datos faltantes: {len(hallazgos['fechas_con_datos_faltantes'])}")
    print(f"Montos atípicos (outliers): {len(hallazgos['montos_atipicos'])}\n")
    print(f"Impuesto declarado (base incorrecta):  ${hallazgos['impuesto_declarado']:,.0f}")
    print(f"Impuesto correcto (base según Ley 56):  ${hallazgos['impuesto_correcto']:,.0f}")
    print(f"Inflación de la base gravable:          {hallazgos['inflacion_pct']:.0f}%")
    print(f"Ahorro potencial detectado:              ${hallazgos['ahorro_potencial']:,.0f}")


def main() -> None:
    df = generar_dataset()
    hallazgos = auditar(df)
    imprimir_reporte(hallazgos)
    ruta_grafico = generar_grafico(hallazgos)
    print(f"\nGráfico guardado en: {ruta_grafico}")


if __name__ == "__main__":
    main()
