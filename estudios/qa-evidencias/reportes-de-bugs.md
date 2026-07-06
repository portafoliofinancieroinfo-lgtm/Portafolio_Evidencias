# 🐞 Reportes de bugs — muestra

Ejemplos representativos de los **30+ defectos** encontrados, documentados y
gestionados en **Jira** durante el bootcamp (proyectos `BRIAN`, `BD4CG4OS` y
`KAN`). Como esas instancias de Jira son privadas, los reportes están
reproducidos en Markdown en
[Bootcamp-QA / pruebas manuales](https://github.com/portafoliofinancieroinfo-lgtm/Bootcamp-QA/tree/main/05-documentacion-pruebas-manuales).

## Formato

Cada reporte incluye: identificador, título descriptivo, caso de prueba
asociado, pasos para reproducir, resultado esperado, resultado actual y
severidad (Crítico / Grave / Menor / Trivial).

## Ejemplos

### BR2 — El zoom no se genera sobre la ubicación proporcionada

- **Proyecto:** Urban Routes (web) · **Caso asociado:** CASO-7
- **Severidad:** 🔴 Crítico

**Pasos para reproducir**
1. Abrir la aplicación Urban Routes.
2. Hacer clic en el campo "Desde".
3. Ingresar una dirección (ejemplo: *East 2nd Street, 601*).

**Resultado esperado:** el mapa hace zoom sobre el pin de la dirección seleccionada.

**Resultado actual:** el mapa genera zoom en una zona predeterminada, la misma para todas las ubicaciones proporcionadas.

---

### BR1 — No se despliega la lista de estaciones del metro

- **Proyecto:** Urban Routes (web) · **Caso asociado:** CASO-6
- **Severidad:** 🟠 Grave

**Pasos para reproducir**
1. Abrir la aplicación Urban Routes.
2. Hacer clic en el campo "Hasta".
3. Escribir "Subway" (Metro).

**Resultado esperado:** se muestra la lista de estaciones de metro.

**Resultado actual:** no se despliega la lista ni ningún elemento equivalente.

---

### Error 500 en la API de Urban Grocers (proyecto final de automatización)

- **Proyecto:** Urban Grocers (API) · Suite `requests` + `pytest`
- **Severidad:** 🔴 Crítico

Durante la automatización del endpoint de creación de kits, ciertos cuerpos de
petición válidos devolvían **HTTP 500 (Internal Server Error)** en lugar del
código esperado, evidenciando un fallo del servidor no controlado. Documentado
con impacto y recomendaciones en el
[proyecto final](https://github.com/portafoliofinancieroinfo-lgtm/Bootcamp-QA/tree/main/04-proyecto-final-urban-grocers-qa).

## Volumen por proyecto

| Proyecto | Tipo | Bugs reportados |
|---|---|---|
| Urban Routes — funcionales | Web / UI | 5 (BR1–BR5) |
| Urban Routes — cross-browser | Web multi-navegador | 15 (BRIAN-1 a BRIAN-17) |
| Urban Grocers — API | API REST (Postman) | 14+ (incl. errores 500) |
| Urban Lunch — móvil | Android (emulador) | 1 |
| Urban Scooter — proyecto final | Web + móvil + API | 11 (KAN-4 a KAN-14) |
