"""
Organizador de documentos por organigrama.

Inspirado en la estandarización de procesos contables bajo enfoque ISO 9001
que hice en INLOGISTIC S.A.S. (2025): documentar más de 8 procedimientos
operativos estándar (POE) y definir con claridad responsables por proceso.

Este script trabaja sobre un organigrama y documentos sintéticos (no son
datos reales de ninguna empresa) y automatiza una tarea básica de control
documental: clasificar cada POE en la carpeta de su área/puesto según el
organigrama, y detectar documentos huérfanos (responsable que no existe en
el organigrama) o puestos sin ningún documento asociado.
"""
import shutil
import sys
import tempfile
import unicodedata
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

CARPETA = Path(__file__).parent
EVIDENCIA = CARPETA / "evidencia"


def generar_organigrama() -> pd.DataFrame:
    datos = [
        ("Gerente General", "Direccion", None),
        ("Contador General", "Contabilidad", "Gerente General"),
        ("Analista de Costos", "Contabilidad", "Contador General"),
        ("Auxiliar Contable", "Contabilidad", "Contador General"),
        ("Jefe de Nomina", "Talento Humano", "Gerente General"),
        ("Analista de Nomina", "Talento Humano", "Jefe de Nomina"),
        ("Coordinador de Calidad", "Calidad", "Gerente General"),
        ("Auditor Interno", "Calidad", "Coordinador de Calidad"),
    ]
    return pd.DataFrame(datos, columns=["puesto", "area", "jefe"])


def generar_documentos_entrada(carpeta: Path) -> list[Path]:
    carpeta.mkdir(parents=True, exist_ok=True)
    documentos = {
        "POE-01_Contador-General.txt": "Procedimiento de cierre contable mensual",
        "POE-02_Auxiliar-Contable.txt": "Procedimiento de causacion de facturas",
        "POE-03_Jefe-de-Nomina.txt": "Procedimiento de liquidacion de nomina",
        "POE-04_Analista-de-Nomina.txt": "Procedimiento de novedades de nomina",
        "POE-05_Auditor-Interno.txt": "Procedimiento de auditoria interna",
        "POE-06_Analista-de-Costos.txt": "Procedimiento de costeo",
        "POE-07_Tesorero.txt": "Procedimiento de pagos",  # puesto que no existe en el organigrama
        "POE-08_.txt": "Procedimiento sin responsable asignado en el nombre del archivo",
    }
    rutas = []
    for nombre, contenido in documentos.items():
        ruta = carpeta / nombre
        ruta.write_text(contenido, encoding="utf-8")
        rutas.append(ruta)
    return rutas


def extraer_responsable(nombre_archivo: str) -> str:
    partes = Path(nombre_archivo).stem.split("_", 1)
    if len(partes) < 2 or not partes[1].strip():
        return ""
    return partes[1].replace("-", " ").strip()


def normalizar(texto: str) -> str:
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return sin_tildes.casefold().strip()


def encontrar_puesto(responsable_normalizado: str, puestos_normalizados: list[str]) -> str | None:
    if not responsable_normalizado:
        return None
    # Ordenados de más largo a más corto para preferir la coincidencia más específica.
    for candidato in sorted(puestos_normalizados, key=len, reverse=True):
        if responsable_normalizado == candidato or responsable_normalizado.startswith(candidato + " "):
            return candidato
    return None


def organizar(documentos: list[Path], organigrama: pd.DataFrame, carpeta_salida: Path) -> dict:
    mapa_area = {normalizar(puesto): area for puesto, area in zip(organigrama["puesto"], organigrama["area"])}
    mapa_puesto_real = {normalizar(puesto): puesto for puesto in organigrama["puesto"]}
    puestos_normalizados = list(mapa_puesto_real.keys())

    organizados, huerfanos = [], []
    for ruta in documentos:
        responsable = extraer_responsable(ruta.name)
        candidato = encontrar_puesto(normalizar(responsable), puestos_normalizados)
        area = mapa_area.get(candidato)
        if area is None:
            huerfanos.append({"archivo": ruta.name, "responsable_detectado": responsable or "(sin responsable)"})
            continue
        puesto_real = mapa_puesto_real[candidato]
        destino = carpeta_salida / area / puesto_real
        destino.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ruta, destino / ruta.name)
        organizados.append({"archivo": ruta.name, "area": area, "puesto": puesto_real})

    puestos_con_documento = {o["puesto"] for o in organizados}
    puestos_sin_documentos = organigrama[~organigrama["puesto"].isin(puestos_con_documento)]

    return {
        "organizados": pd.DataFrame(organizados),
        "huerfanos": pd.DataFrame(huerfanos),
        "puestos_sin_documentos": puestos_sin_documentos,
    }


def generar_grafico(hallazgos: dict, organigrama: pd.DataFrame) -> Path:
    EVIDENCIA.mkdir(exist_ok=True)
    ruta = EVIDENCIA / "metricas.png"

    conteo_por_area = (
        hallazgos["organizados"].groupby("area").size().reindex(organigrama["area"].unique(), fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    barras = ax.bar(conteo_por_area.index, conteo_por_area.values, color="#2980b9")
    ax.set_ylabel("Documentos organizados")
    ax.set_title(f"Documentos por área — {len(hallazgos['huerfanos'])} huérfanos detectados (datos sintéticos)")
    for barra, valor in zip(barras, conteo_por_area.values):
        ax.text(barra.get_x() + barra.get_width() / 2, valor, str(valor), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def imprimir_reporte(hallazgos: dict) -> None:
    print("=== Organizador de documentos por organigrama ===\n")
    print(f"Documentos organizados: {len(hallazgos['organizados'])}")
    print(f"Documentos huérfanos (responsable no existe en el organigrama): {len(hallazgos['huerfanos'])}")
    if not hallazgos["huerfanos"].empty:
        for _, fila in hallazgos["huerfanos"].iterrows():
            print(f"  - {fila['archivo']} -> responsable detectado: '{fila['responsable_detectado']}'")
    print(f"Puestos del organigrama sin ningún documento: {len(hallazgos['puestos_sin_documentos'])}")
    if not hallazgos["puestos_sin_documentos"].empty:
        for puesto in hallazgos["puestos_sin_documentos"]["puesto"]:
            print(f"  - {puesto}")


def main() -> None:
    organigrama = generar_organigrama()
    with tempfile.TemporaryDirectory() as tmp:
        carpeta_entrada = Path(tmp) / "documentos_entrada"
        carpeta_salida = Path(tmp) / "documentos_organizados"
        documentos = generar_documentos_entrada(carpeta_entrada)
        hallazgos = organizar(documentos, organigrama, carpeta_salida)
        imprimir_reporte(hallazgos)
        ruta_grafico = generar_grafico(hallazgos, organigrama)
        print(f"\nGráfico guardado en: {ruta_grafico}")


if __name__ == "__main__":
    main()
