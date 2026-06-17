# 📊 TPI — Introducción al Análisis de Datos

**Tecnicatura Universitaria en Programación — UTN**
**Materia:** Introducción al Análisis de Datos
**Año:** 2026

---

## 👥 Integrantes

| Nombre               |
|----------------------|
| Nicolas Llaneza      |
| David Lopez          |
| Sabrina Moreira      | 
| Emmanuel Avellaneda  | 
| Tomas Ferro          |

---

## 📁 Dataset

**Nombre:** Students Performance Dataset
**Fuente:** Kaggle
**Registros:** 5.000 estudiantes universitarios
**Variables originales:** 22 — **Variables finales (con feature engineering):** 28
**Archivo limpio:** [`parcial2-AdD/students_clean.csv`](./parcial2-AdD/students_clean.csv)

---

## 🎯 Preguntas de Negocio

1. ¿Qué combinación de variables conductuales y académicas permite identificar estudiantes con alta probabilidad de reprobar?
2. ¿Existe una relación no lineal entre horas de estudio y rendimiento? ¿En qué punto el incremento de horas deja de producir mejoras significativas?
3. ¿En qué medida el nivel de ingresos y el acceso a internet condicionan el desempeño académico?

---

## 🗂️ Estructura del Repositorio

```
TPI-Analisis-Datos/
├── parcial2-AdD/
│   ├── TPI_Intro_Analisis_de_Datos.ipynb    # Notebook principal (Hitos 1, 2 y 3)
│   ├── students_clean.csv                    # Dataset limpio exportado
│   └── paneles-grafana/                      # Capturas del dashboard de Grafana
├── dashboard.py                              # App Streamlit (Hito 4)
├── requirements.txt                          # Dependencias Python
├── Hito5_Informe_Gestion.docx                # Informe de gestión (Hito 5)
└── README.md
```

---

## 📌 Hito 1 y 2 — Limpieza y Preparación de Datos

**Archivo:** [`parcial2-AdD/TPI_Intro_Analisis_de_Datos.ipynb`](./parcial2-AdD/TPI_Intro_Analisis_de_Datos.ipynb)

El notebook cubre los primeros dos hitos del TPI de forma integrada:

| Paso | Descripción |
|------|-------------|
| **Paso 0** | Importación de librerías (pandas, numpy, matplotlib, seaborn) |
| **Paso 1** | Carga del dataset desde GitHub (5.000 registros, 22 columnas) |
| **Paso 2** | Auditoría inicial: tipos de datos, estadísticas descriptivas, detección de nulos |
| **Paso 3** | Tratamiento de nulos: mediana para `Attendance (%)` y `Assignments_Avg`; categoría `Unknown` para `Parent_Education_Level` |
| **Paso 4** | Normalización de strings en variables categóricas |
| **Paso 5** | Detección de outliers con IQR — tabla diagnóstica con Q1, Q3, IQR, límites y CV% por variable |
| **Paso 6** | Feature engineering: 5 variables nuevas (`Indice_Riesgo`, `Categoria_Riesgo`, `Delta_Parcial_Final`, `Promedio_Continuo`, `Eficiencia_Estudio`) |
| **Paso 7** | Resumen final con control de calidad — 0 nulos restantes |
| **Paso 8** | Exportación del dataset limpio a `students_clean.csv` |

### ▶️ Cómo ejecutar

1. Abrí el archivo en [Google Colab](https://colab.research.google.com/)
2. Ejecutá todas las celdas en orden: `Entorno de ejecución → Ejecutar todo` (`Ctrl + F9`)
3. El dataset se carga automáticamente desde GitHub, no es necesario subir ningún archivo

---

## 📊 Hito 3 — Visualización Dinámica

**Archivo:** [`parcial2-AdD/TPI_Intro_Analisis_de_Datos.ipynb`](./parcial2-AdD/TPI_Intro_Analisis_de_Datos.ipynb) (celdas del Hito 3 — Pasos 9 y 10)

Análisis visual profesional con Matplotlib y Seaborn respondiendo las tres preguntas de negocio. Todos los gráficos incluyen conclusiones interpretativas embebidas.

**Pregunta 1 — Riesgo de abandono:**
- Boxplot del Índice de Riesgo por calificación final
- Scatter de Asistencia vs. Nota de Parcial coloreado por Categoría de Riesgo
- Heatmap de tasa de reprobación por Riesgo × Nivel de Estrés

**Pregunta 2 — Eficiencia del esfuerzo:**
- Scatter con curva de tendencia LOWESS: Horas de estudio vs. Total Score
- Violin plot de Eficiencia de Estudio por Categoría de Riesgo
- Lineplot de Total Score promedio por tramo de horas y nivel de estrés

**Pregunta 3 — Brecha socioeconómica:**
- Barplot de Score promedio por Ingresos × Acceso a Internet (con barras de error)
- Boxplot de Score por Departamento ordenado por mediana
- Heatmap de Score promedio por Departamento × Nivel de Ingresos

**Análisis complementario (Paso 10):**
- Mapa de correlaciones: matriz triangular de 15 variables numéricas

---

## 🖥️ Hito 4 — Dashboard Interactivo (Streamlit)

### 🔗 [Acceder al dashboard → tpi-datos-utn.streamlit.app](https://tpi-datos-utn.streamlit.app)

**Archivos:** [`dashboard.py`](./dashboard.py) · [`requirements.txt`](./requirements.txt)

Dashboard web interactivo deployado en Streamlit Cloud. Los datos se cargan directamente desde el CSV en este repositorio.

**Filtros interactivos (sidebar):**
- 🏫 Departamento (multiselect)
- ⚠️ Categoría de Riesgo (multiselect)
- 💰 Nivel de Ingresos (multiselect)
- 🎓 Calificación Final (multiselect)
- 🌐 Acceso a Internet (radio)
- 📅 Asistencia mínima (slider)
- 🔄 Botón de reseteo de filtros

**Visualizaciones:**
- 4 KPIs con semáforo 🔴🟡🟢 y delta respecto al dataset completo
- Pie chart de distribución de Riesgo Académico
- Bar chart de calificaciones A/B/C/D/F
- Bar chart horizontal de Score por Departamento
- Bar chart de tasa de reprobación por nivel de estrés
- Bar chart agrupado de Score por Ingresos × Internet
- Bar chart de Eficiencia y Horas por Categoría de Riesgo
- Tabla expandible con datos filtrados

**Características técnicas:**
- Gráficos que se actualizan en tiempo real al cambiar filtros
- Conclusiones dinámicas embebidas en cada sección
- `@st.cache_data` para optimización de carga
- `try/except` + `logging` en todas las funciones
- Validación de esquema del CSV al iniciar

### ▶️ Cómo ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## 📊 Tablero de Control en Grafana

**Capturas:** [`parcial2-AdD/paneles-grafana/`](./parcial2-AdD/paneles-grafana/)

Dashboard complementario construido en Grafana v13 conectado a Supabase (PostgreSQL). El JSON del dashboard se encuentra en el repositorio para reproducibilidad.

**Paneles implementados:**

| # | Tipo | Título |
|---|------|--------|
| 1 | Stat | Total de Estudiantes |
| 2 | Stat | Promedio General |
| 3 | Stat | % en Riesgo Alto (con umbrales semafóricos) |
| 4 | Stat | Tasa de Reprobación Global (con umbrales semafóricos) |
| 5 | Pie chart | Distribución de Riesgo Académico |
| 6 | Bar chart | Distribución de Calificaciones Finales |
| 7 | Bar chart horizontal | Puntaje Promedio por Departamento |
| 8 | Bar chart | Tasa de Reprobación por Nivel de Estrés |
| 9 | Bar chart agrupado | Score Promedio por Ingresos y Acceso a Internet |
| 10 | Bar chart doble | Eficiencia y Horas de Estudio por Categoría de Riesgo |

**Stack:** Grafana v13 · PostgreSQL (Supabase) · SQL nativo por panel

---

## 📝 Hito 5 — Informe de Gestión y Propuesta

**Archivo:** [`Hito5_Informe_Gestion.docx`](./Hito5_Informe_Gestion.docx)

Informe académico que sintetiza los hallazgos del análisis y propone dos mejoras concretas fundamentadas en los datos.

**Diagnóstico principal:**
- El 34,7% de los estudiantes reprobó o tuvo rendimiento bajo (Grades D y F)
- Predictores más fuertes: asistencia < 65%, parcial < 50 pts y estrés ≥ 7
- Segmento más vulnerable: Low sin internet (194 estudiantes, 3,9% del total, promedio 75,85 pts)
- Brecha de estudio: Riesgo Bajo estudia 21 h/sem vs. 10,2 h de Riesgo Alto

**Propuesta 1 — Sistema de Seguimiento Académico Temprano:**
Sistema semanal de cálculo del Índice de Riesgo con alertas para el equipo docente, adaptando el dashboard de Streamlit como panel de monitoreo institucional. Impacto estimado: 253 estudiantes adicionales aprobando por cohorte.

**Propuesta 2 — Programa de Reducción de la Brecha Digital:**
Programa de inclusión digital para los 194 estudiantes de bajos ingresos sin acceso a internet, con tres componentes: convenios de conectividad subsidiada, ampliación del horario de laboratorios y préstamo de dispositivos. Sinergia con Propuesta 1: prioriza dispositivos según el Índice de Riesgo.

---

## 🗄️ Base de Datos (Supabase)

El dataset limpio está alojado en **Supabase (PostgreSQL)**, usado como fuente de datos del dashboard de Grafana.

- **Tabla:** `students`
- **Registros:** 5.000
- **Columnas:** 28
- **Region:** South America (São Paulo)

---

*TPI — Introducción al Análisis de Datos · UTN Tecnicatura en Programación · Junio 2026*
