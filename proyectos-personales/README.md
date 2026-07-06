# 🚀 Proyectos personales

Iniciativas propias: para cada caso real documentado en [trabajo/](../trabajo/README.md) construí una herramienta
original (con datos sintéticos, no confidenciales) que automatiza el tipo de control que hice manualmente en esa
empresa. El código y las métricas de cada herramienta viven junto a su caso real; aquí documento las **pruebas QA**
que le hice a esas mismas herramientas — el mismo rigor de "construyo la herramienta contable Y la pruebo como QA".

| Proyecto | Caso real que lo inspira | Evidencia QA |
|---|---|---|
| [`auditor_reteica.py`](../trabajo/electrovichada-2023/auditor_reteica.py) | [Electrovichada](../trabajo/electrovichada-2023/README.md) — corrección de base ReteICA | [qa/electrovichada-auditor-reteica.md](./qa/electrovichada-auditor-reteica.md) |
| [`conciliador.py`](../trabajo/transervi-2022/conciliador.py) | [Transervi](../trabajo/transervi-2022/README.md) — reconstrucción contable 2021 | [qa/transervi-conciliador.md](./qa/transervi-conciliador.md) |
| [`auditor_checklist.py`](../trabajo/fervicom-2024/auditor_checklist.py) | [FERVICOM](../trabajo/fervicom-2024/README.md) — auditorías internas | [qa/fervicom-auditor-checklist.md](./qa/fervicom-auditor-checklist.md) |
| [`organizador.py`](../trabajo/inlogistic-2025/organizador.py) | [INLOGISTIC](../trabajo/inlogistic-2025/README.md) — estandarización ISO 9001 | [qa/inlogistic-organizador.md](./qa/inlogistic-organizador.md) |

Cada evidencia QA incluye casos de prueba y, cuando aplica, bugs reales encontrados al probar la herramienta —
con causa raíz, corrección aplicada y verificación posterior.

> Esta sección crecerá a medida que desarrolle nuevas herramientas (automatizaciones, control financiero,
> ejercicios de QA sobre aplicaciones reales).
