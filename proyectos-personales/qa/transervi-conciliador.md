# QA — `conciliador.py` (caso Transervi)

Herramienta bajo prueba: [trabajo/transervi-2022/conciliador.py](../../trabajo/transervi-2022/conciliador.py)

## Casos de prueba

| # | Caso | Datos de entrada | Resultado esperado | Resultado obtenido |
|---|---|---|---|---|
| 1 | Flujo normal | 3.000 movimientos sintéticos con huecos, diferencias y duplicados inyectados | Reporta % conciliado y desglose por tipo de hallazgo | ✅ Pasa |
| 2 | Movimiento sin extracto bancario | Movimiento registrado en el libro que no está en el banco | Se marca como `sin_extracto_bancario` | ✅ Pasa |
| 3 | Movimiento sin registrar en el libro | Movimiento del banco que nunca se registró contablemente | Se marca como `sin_registrar_en_libro` | ✅ Pasa |
| 4 | Diferencia de monto | Mismo id, monto distinto entre libro y banco | Se marca como `diferencias_de_monto`, no como conciliado | ✅ Pasa |
| 5 | Duplicado en el libro | Mismo id repetido dos veces en el libro (doble digitación) | Ambas filas se marcan en `duplicados_en_libro` | ✅ Pasa |
| 6 | Duplicado en el banco (cobro doble) | Mismo id repetido dos veces en el extracto bancario | Ambas filas se marcan en `duplicados_en_banco` | ❌ Falla → ver [BUG-01](#bug-01-no-detecta-duplicados-en-el-extracto-bancario) |
| 7 | Id inexistente en ambas fuentes | Id que no existe ni en libro ni en banco | No debería aparecer en ningún reporte | ✅ Pasa |

## Bugs encontrados

### BUG-01: No detecta duplicados en el extracto bancario

- **Severidad:** Alta
- **Pasos para reproducir:**
  1. Generar los datasets con `generar_datasets()`.
  2. Duplicar una fila cualquiera del `banco` (simula un cobro bancario duplicado, un caso real y frecuente).
  3. Ejecutar `conciliar(libro, banco)`.
- **Resultado obtenido:** El script solo revisaba duplicados en el **libro** (`duplicados_en_libro`), nunca en el
  **banco**. Además, al cruzar (`merge`) un id duplicado en el banco contra el libro, esa fila se combinaba dos
  veces silenciosamente, inflando el conteo de `conciliados` en uno sin ninguna advertencia.
- **Resultado esperado:** Un cobro bancario duplicado debería reportarse igual que un duplicado en el libro — es
  exactamente el tipo de error que un auxiliar contable necesita detectar antes de cerrar la conciliación.
- **Causa raíz:** faltaba una verificación de duplicados sobre `banco`, y el `merge` se hacía contra el banco
  completo (con duplicados) en vez de una versión deduplicada.
- **Estado:** Corregido — se agregó `duplicados_en_banco` (mismo criterio que `duplicados_en_libro`) y el cruce
  ahora se hace contra `banco_unico` (sin duplicados). Verificado de nuevo con el mismo caso: el duplicado ya se
  reporta en `duplicados_en_banco` y el conteo de `conciliados` deja de inflarse.

## Checklist de verificación

- [x] El script corre sin errores con `python conciliador.py`.
- [x] El gráfico se genera en `evidencia/metricas.png`.
- [x] El % de conciliación se calcula sobre movimientos únicos del libro (sin duplicados).
- [x] Se detectan duplicados tanto en el libro como en el banco.
- [x] Los conteos de "sin extracto"/"sin registrar" no se solapan con "diferencias de monto" (son mutuamente
      excluyentes en el cruce).
