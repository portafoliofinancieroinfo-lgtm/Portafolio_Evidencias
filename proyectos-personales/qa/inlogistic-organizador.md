# QA — `organizador.py` (caso INLOGISTIC)

Herramienta bajo prueba: [trabajo/inlogistic-2025/organizador.py](../../trabajo/inlogistic-2025/organizador.py)

## Casos de prueba

| # | Caso | Datos de entrada | Resultado esperado | Resultado obtenido |
|---|---|---|---|---|
| 1 | Flujo normal | 8 documentos sintéticos + organigrama de 8 puestos | Clasifica los documentos válidos por área/puesto y reporta huérfanos y puestos sin documento | ✅ Pasa |
| 2 | Documento con responsable inexistente | Archivo `POE-07_Tesorero.txt` (puesto no está en el organigrama) | Se reporta como huérfano | ✅ Pasa |
| 3 | Documento sin responsable en el nombre | Archivo `POE-08_.txt` | Se reporta como huérfano con etiqueta "(sin responsable)" | ✅ Pasa |
| 4 | Puesto sin documentos | Puesto del organigrama sin ningún POE asociado | Aparece en `puestos_sin_documentos` | ✅ Pasa |
| 5 | Dos documentos del mismo responsable | Dos archivos distintos apuntando al mismo puesto | Ambos se organizan en la misma carpeta destino, sin sobrescribirse (nombres de archivo distintos) | ✅ Pasa |
| 6 | Diferencia de mayúsculas/tildes | Responsable escrito distinto en mayúsculas/minúsculas o sin tilde | Debe igual coincidir con el puesto del organigrama | ✅ Pasa (normalización con `casefold` + remoción de tildes ya incluida desde el diseño inicial) |
| 7 | Nombre de archivo con sufijo de versión | Archivo `POE-10_Contador-General-v2.txt` | Debe organizarse bajo "Contador General", no marcarse como huérfano | ❌ Falla → ver [BUG-01](#bug-01-los-sufijos-de-version-rompen-el-match-exacto) |

## Bugs encontrados

### BUG-01: Los sufijos de versión rompen el match exacto

- **Severidad:** Media
- **Pasos para reproducir:**
  1. Generar el organigrama y los documentos de entrada.
  2. Agregar un archivo con sufijo de versión, ej. `POE-10_Contador-General-v2.txt` (un caso común en control
     documental real: "-v2", "-final", etc.).
  3. Ejecutar `organizar(documentos, organigrama, carpeta_salida)`.
- **Resultado obtenido:** El archivo se reportaba como huérfano, con responsable detectado `"Contador General v2"`,
  porque el matching original comparaba el nombre extraído contra el organigrama por **igualdad exacta**.
- **Resultado esperado:** Debería reconocer que "Contador General v2" pertenece al puesto "Contador General" y
  organizarlo en su carpeta, igual que la versión sin sufijo.
- **Causa raíz:** `organizar()` buscaba el puesto con un `dict.get()` de igualdad exacta sobre el texto normalizado,
  sin tolerar texto adicional al final (versión, sufijos).
- **Estado:** Corregido — se agregó `encontrar_puesto()`, que busca coincidencia exacta o por prefijo (el nombre
  extraído empieza con el nombre del puesto seguido de un espacio), probando primero los puestos más largos para
  evitar coincidencias ambiguas. Verificado de nuevo con el mismo caso: el archivo versionado ya se organiza bajo
  "Contador General" y los demás casos (huérfanos genuinos, puestos sin documentos) no cambiaron.

## Checklist de verificación

- [x] El script corre sin errores con `python organizador.py`.
- [x] El gráfico se genera en `evidencia/metricas.png`.
- [x] Los archivos se organizan en una carpeta temporal (no deja residuos en el repositorio).
- [x] Un documento sin responsable reconocible se reporta como huérfano, nunca se descarta en silencio.
- [x] El matching de puesto tolera mayúsculas, tildes y sufijos de versión en el nombre del archivo.
