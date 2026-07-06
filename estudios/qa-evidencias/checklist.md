# ✅ Checklist de pruebas — muestra

Las listas de comprobación fueron una de las herramientas centrales del
[proyecto final Urban Scooter](https://github.com/portafoliofinancieroinfo-lgtm/Bootcamp-QA/tree/main/05-documentacion-pruebas-manuales/06-urban-scooter-proyecto-final-manual),
que cubrió las tres capas de una misma plataforma (web + móvil + API) con 11
defectos gestionados en Jira.

## Ejemplo: checklist funcional para una aplicación web

| # | Verificación | Estado |
|---|---|---|
| 1 | La página principal carga sin errores en consola | ☑ |
| 2 | Los campos obligatorios validan entrada vacía | ☑ |
| 3 | Los campos rechazan formatos inválidos (email, teléfono) | ☑ |
| 4 | Los mensajes de error son claros y visibles | ☑ |
| 5 | El flujo principal se completa de extremo a extremo | ☑ |
| 6 | Los botones deshabilitados no ejecutan acciones | ☑ |
| 7 | La UI es consistente en Chrome y Firefox | ☑ |
| 8 | La UI se adapta a resoluciones bajas (800×600) | ☑ |
| 9 | Los datos persisten tras recargar la página | ☑ |
| 10 | Los enlaces y logotipos llevan al destino esperado | ☑ |

## Ejemplo: checklist para pruebas de API

| # | Verificación | Estado |
|---|---|---|
| 1 | El endpoint responde el código de estado documentado | ☑ |
| 2 | Casos positivos: cuerpo válido → 2xx con el recurso creado | ☑ |
| 3 | Casos negativos: campos faltantes → 4xx con mensaje claro | ☑ |
| 4 | Valores límite: longitudes mínima y máxima aceptadas | ☑ |
| 5 | Tipos de dato incorrectos rechazados (no 500) | ☑ |
| 6 | Cabeceras y content-type validados | ☑ |
| 7 | La respuesta no expone información sensible | ☑ |

## Por qué me funcionan

El checklist es el punto de encuentro entre mis dos perfiles: en auditoría
contable uso listas de verificación para revisar procesos (soportes,
causación, conciliaciones); en QA las uso para cubrir sistemáticamente la
funcionalidad de una aplicación. La disciplina es la misma: **nada se da por
válido sin verificarse**.
