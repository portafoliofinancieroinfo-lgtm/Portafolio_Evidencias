# Estructura del repositorio

```
📁 Portafolio_Evidencias/
 ┣ 📄 README.md                    → portada e índice del portafolio
 ┣ 📄 about.md                     → perfil profesional ampliado
 ┣ 📄 Estructura.md                → este archivo
 ┣ 📁 trabajo/                     → casos reales + herramienta propia por caso
 ┃   ┣ 📄 README.md
 ┃   ┣ 📄 requirements.txt         → dependencias compartidas (pandas, matplotlib, numpy)
 ┃   ┣ 📁 electrovichada-2023/     → README + auditor_reteica.py + evidencia/
 ┃   ┣ 📁 transervi-2022/          → README + conciliador.py + evidencia/
 ┃   ┣ 📁 fervicom-2024/           → README + auditor_checklist.py + evidencia/
 ┃   ┗ 📁 inlogistic-2025/         → README + organizador.py + evidencia/
 ┗ 📁 proyectos-personales/        → evidencia QA de las herramientas de trabajo/
     ┣ 📄 README.md
     ┗ 📁 qa/                      → casos de prueba y bugs por herramienta
```

Cada carpeta dentro de `trabajo/` contiene el estudio de caso real (sin datos confidenciales), el script que
automatiza —sobre datos sintéticos— el tipo de control que hice manualmente en esa empresa, y una carpeta
`evidencia/` con el gráfico de resultados. La formación en QA (bootcamp TripleTen) está referenciada brevemente en
[about.md](./about.md).
