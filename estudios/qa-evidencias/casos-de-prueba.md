# 📄 Casos de prueba — muestra

Ejemplos representativos de los **24 casos de prueba** diseñados y ejecutados
sobre la aplicación web *Urban Routes* (mapa interactivo) durante el bootcamp.
La suite completa, con su hoja de cálculo original, está en
[Bootcamp-QA / pruebas manuales](https://github.com/portafoliofinancieroinfo-lgtm/Bootcamp-QA/tree/main/05-documentacion-pruebas-manuales/01-urban-routes-pruebas-funcionales).

## Formato

Cada caso incluye: identificador, título, precondiciones, pasos, resultado
esperado y estado de ejecución (Aprobado / No aprobado / Omitido). Los casos
no aprobados quedan vinculados a su informe de error.

## Ejemplos

### CASO-6 — Búsqueda de estaciones de metro en el campo "Hasta"

| Campo | Detalle |
|---|---|
| **Precondición** | Aplicación Urban Routes abierta |
| **Pasos** | 1. Hacer clic en el campo "Hasta" 2. Escribir "Subway" (Metro) |
| **Resultado esperado** | Se despliega la lista de estaciones de metro disponibles |
| **Estado** | ❌ No aprobado → bug **BR1** (Grave) |

### CASO-7 — Zoom sobre la dirección ingresada en "Desde"

| Campo | Detalle |
|---|---|
| **Precondición** | Aplicación Urban Routes abierta |
| **Pasos** | 1. Hacer clic en el campo "Desde" 2. Ingresar una dirección (ej.: *East 2nd Street, 601*) |
| **Resultado esperado** | El mapa hace zoom sobre el pin de la dirección seleccionada |
| **Estado** | ❌ No aprobado → bug **BR2** (Crítico) |

### CASO-11 — Renderización 3D de objetos del mapa

| Campo | Detalle |
|---|---|
| **Precondición** | Aplicación Urban Routes abierta |
| **Pasos** | 1. Ampliar el mapa varias veces sobre un objeto 3D (ej.: *aeropuerto LAX*) |
| **Resultado esperado** | El objeto se renderiza en 3D |
| **Estado** | ❌ No aprobado → bug **BR4** (Menor) |

## Resultados de la suite completa

| Métrica | Valor |
|---|---|
| Casos diseñados | 24 |
| Aprobados | 17 |
| No aprobados (con bug asociado) | 5 |
| Omitidos (justificados) | 2 |

## Técnicas de diseño aplicadas en otros proyectos

- **Clases de equivalencia y valores límite** — diseño de pruebas de Urban Routes y de la API de Urban Grocers.
- **Tablas de decisión, mapas mentales y diagramas de flujo** — [diseño de pruebas](https://github.com/portafoliofinancieroinfo-lgtm/Bootcamp-QA/tree/main/05-documentacion-pruebas-manuales/02-urban-routes-diseno-de-pruebas).
- **Casos de prueba de API** — positivos y negativos por partición de equivalencia, validando códigos de estado y mensajes de error.
