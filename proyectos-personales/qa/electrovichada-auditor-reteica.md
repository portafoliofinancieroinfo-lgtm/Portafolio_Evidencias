# QA — `auditor_reteica.py` (caso Electrovichada)

Herramienta bajo prueba: [trabajo/electrovichada-2023/auditor_reteica.py](../../trabajo/electrovichada-2023/auditor_reteica.py)

Aplico a mi propia herramienta el mismo proceso que usé en el bootcamp de QA: diseño casos de prueba, ejecuto la
herramienta con datos límite y reporto los defectos encontrados.

## Casos de prueba

| # | Caso | Datos de entrada | Resultado esperado | Resultado obtenido |
|---|---|---|---|---|
| 1 | Flujo normal | Dataset sintético con 1 mes faltante, 1 duplicado, 1 atípico alto | Reporta 2 duplicados, 1 faltante, 1 atípico; calcula impuesto declarado vs. correcto | ✅ Pasa |
| 2 | Detección de duplicados | Dos filas con el mismo `mes` pero distinto `produccion_kwh` | Ambas filas se marcan como duplicadas | ✅ Pasa |
| 3 | Mes con dato faltante (`NaN`) | Un mes con `produccion_kwh = NaN` | Se excluye del cálculo del impuesto y se reporta aparte | ✅ Pasa |
| 4 | Atípico alto | Un mes con producción 4x el promedio | Se detecta como atípico | ✅ Pasa |
| 5 | Atípico bajo | Un mes con producción anormalmente baja (100 kWh vs. ~4.5M promedio) | Se detecta como atípico | ❌ Falla → ver [BUG-01](#bug-01-no-detecta-valores-atipicos-bajos) |
| 6 | Consistencia del hallazgo tributario | Base declarada = producción anual; base correcta = producción anual / 12 | Inflación reportada ≈ 1100%, coherente con el caso real ("más de 1000%") | ✅ Pasa |

## Bugs encontrados

### BUG-01: No detecta valores atípicos bajos

- **Severidad:** Media
- **Pasos para reproducir:**
  1. Generar el dataset con `generar_dataset()`.
  2. Forzar un mes con producción anormalmente baja (ej. `df.loc[10, "produccion_kwh"] = 100`).
  3. Ejecutar `auditar(df)` y revisar `hallazgos["montos_atipicos"]`.
- **Resultado obtenido:** El mes con producción de 100 kWh no aparece en los atípicos.
- **Resultado esperado:** Debería aparecer, igual que un atípico alto — un mes con producción casi nula suele indicar un
  error de reporte (sensor caído, dato mal digitado), no una caída real de producción.
- **Causa raíz:** el filtro de atípicos solo comparaba contra el límite superior del rango intercuartílico
  (`> limite_superior`), sin comparar contra el límite inferior.
- **Estado:** Corregido — el filtro ahora evalúa ambos límites (`> limite_superior` o `< limite_inferior`).
  Verificado de nuevo con el mismo caso: el mes de producción anómalamente baja ya se reporta como atípico, sin afectar
  el resto de resultados (duplicados, faltantes e impuesto declarado/correcto se mantienen iguales).

## Checklist de verificación

- [x] El script corre sin errores con `python auditor_reteica.py`.
- [x] El gráfico se genera en `evidencia/metricas.png`.
- [x] Los duplicados se detectan por columna `mes`, no por fila completa.
- [x] Los atípicos se detectan en ambos extremos (alto y bajo).
- [x] La cifra de inflación de la base gravable es coherente con el caso real documentado en
      [trabajo/electrovichada-2023/README.md](../../trabajo/electrovichada-2023/README.md).
