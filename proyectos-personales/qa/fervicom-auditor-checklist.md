# QA — `auditor_checklist.py` (caso FERVICOM)

Herramienta bajo prueba: [trabajo/fervicom-2024/auditor_checklist.py](../../trabajo/fervicom-2024/auditor_checklist.py)

## Casos de prueba

| # | Caso | Datos de entrada | Resultado esperado | Resultado obtenido |
|---|---|---|---|---|
| 1 | Flujo normal | Checklist sintético de 6 procesos x 8 ítems, con defectos inyectados | Reporta duplicados, inconsistencias y riesgo por proceso | ✅ Pasa |
| 2 | Ítem duplicado | Mismo `proceso`+`item` repetido dos veces | Se marca en `items_duplicados` y no se cuenta dos veces en el riesgo | ✅ Pasa |
| 3 | "Cumple" sin evidencia | Ítem con `estado="Cumple"` y `evidencia_adjunta=False` | Se marca en `cumple_sin_evidencia` | ✅ Pasa |
| 4 | Sin firma del responsable | Ítem con `firma_responsable=False` | Se marca en `sin_firma_responsable` | ✅ Pasa |
| 5 | Responsable no asignado | Ítem con `responsable=""` | Se marca como hallazgo | ❌ Falla → ver [BUG-01](#bug-01-no-detecta-items-sin-responsable-asignado) |
| 6 | Clasificación de riesgo | Proceso con 3+ hallazgos / 1-2 / 0 | Se clasifica como Alto / Medio / Bajo respectivamente | ✅ Pasa |

## Bugs encontrados

### BUG-01: No detecta ítems sin responsable asignado

- **Severidad:** Alta
- **Pasos para reproducir:**
  1. Generar el checklist con `generar_checklist()`.
  2. Dejar vacío el campo `responsable` de cualquier ítem (`df.loc[i, "responsable"] = ""`).
  3. Ejecutar `auditar(df)`.
- **Resultado obtenido:** El ítem no aparece en ningún hallazgo — el script solo validaba evidencia y firma, nunca si
  existía un responsable asignado.
- **Resultado esperado:** Un ítem de auditoría sin responsable asignado es en sí mismo un hallazgo crítico (nadie
  responde por ese proceso), debería marcarse igual que la falta de evidencia o firma.
- **Causa raíz:** faltaba la validación de `responsable` vacío/nulo en `auditar()`.
- **Estado:** Corregido — se agregó `sin_responsable_asignado` (columna `responsable` vacía o solo espacios) y se
  incluyó en el cálculo de riesgo por proceso. Verificado de nuevo con el mismo caso: el ítem ya se reporta en
  `sin_responsable_asignado`.

## Checklist de verificación

- [x] El script corre sin errores con `python auditor_checklist.py`.
- [x] El gráfico se genera en `evidencia/metricas.png`.
- [x] Los duplicados no inflan el conteo de riesgo (se calculan sobre `df_unico`).
- [x] Un ítem con más de un hallazgo (ej. sin evidencia y sin firma a la vez) no se cuenta dos veces en el riesgo del
      proceso (unión de conjuntos, no suma).
- [x] Todo ítem sin evidencia, sin firma o sin responsable queda cubierto por al menos un hallazgo.
