# ══════════════════════════════════════════════════════════════════
#  TPI — Análisis Académico Estudiantil  |  Hito 4: Streamlit
# ══════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

# ── Configuración de página ───────────────────────────────────────
st.set_page_config(
    page_title="Análisis Académico Estudiantil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Paleta de colores globales ────────────────────────────────────
PALETTE_RIESGO  = {'Alto': '#e74c3c', 'Medio': '#f39c12', 'Bajo': '#2ecc71'}
PALETTE_GRADE   = {'A': '#1a9641', 'B': '#a6d96a', 'C': '#f39c12', 'D': '#fdae61', 'F': '#d7191c'}
PALETTE_INGRESO = {'Low': '#e74c3c', 'Medium': '#f39c12', 'High': '#2ecc71'}

sns.set_theme(style='whitegrid', font_scale=1.0)

# ══════════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════════
@st.cache_data
def cargar_datos():
    """Carga el dataset limpio desde GitHub. Usa caché para no recargar en cada interacción."""
    try:
        url = "https://raw.githubusercontent.com/Sabrinavmr/TPI-Analisis-Datos/main/parcial2-AdD/students_clean.csv"
        df = pd.read_csv(url)
        return df, None
    except Exception as e:
        return None, str(e)

# ══════════════════════════════════════════════════════════════════
# FUNCIONES DE KPI
# ══════════════════════════════════════════════════════════════════
def calcular_kpis(df):
    """Calcula los 4 KPIs principales del dataset filtrado."""
    try:
        total         = len(df)
        promedio      = round(df['Total_Score'].mean(), 2) if total > 0 else 0
        pct_riesgo    = round(100 * (df['Categoria_Riesgo'] == 'Alto').sum() / total, 1) if total > 0 else 0
        pct_reprobado = round(100 * (df['Grade'] == 'F').sum() / total, 1) if total > 0 else 0
        return total, promedio, pct_riesgo, pct_reprobado
    except Exception as e:
        st.error(f"Error calculando KPIs: {e}")
        return 0, 0, 0, 0

def mostrar_kpis(total, promedio, pct_riesgo, pct_reprobado):
    """Muestra los 4 KPIs en columnas con colores semafóricos."""
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="👥 Total Estudiantes",
        value=f"{total:,}"
    )
    col2.metric(
        label="📈 Promedio General",
        value=f"{promedio} pts"
    )

    # Color semafórico para Riesgo Alto
    color_riesgo = "🔴" if pct_riesgo > 25 else "🟡" if pct_riesgo > 15 else "🟢"
    col3.metric(
        label=f"{color_riesgo} En Riesgo Alto",
        value=f"{pct_riesgo}%"
    )

    # Color semafórico para Reprobación
    color_repro = "🔴" if pct_reprobado > 20 else "🟡" if pct_reprobado > 10 else "🟢"
    col4.metric(
        label=f"{color_repro} Tasa Reprobación",
        value=f"{pct_reprobado}%"
    )

# ══════════════════════════════════════════════════════════════════
# FUNCIONES DE GRÁFICOS
# ══════════════════════════════════════════════════════════════════
def grafico_riesgo_pie(df):
    """Pie chart: distribución de Categoría de Riesgo."""
    try:
        conteo = df['Categoria_Riesgo'].value_counts()
        orden  = [c for c in ['Bajo', 'Medio', 'Alto'] if c in conteo.index]
        conteo = conteo.reindex(orden)
        colores = [PALETTE_RIESGO[c] for c in orden]

        fig, ax = plt.subplots(figsize=(5, 4))
        wedges, texts, autotexts = ax.pie(
            conteo.values,
            labels=conteo.index,
            colors=colores,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        for at in autotexts:
            at.set_fontsize(10)
            at.set_fontweight('bold')
        ax.set_title('Distribución de Riesgo Académico', fontweight='bold', pad=15)
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Error en gráfico de riesgo: {e}")
        return None

def grafico_grades_bar(df):
    """Bar chart: distribución de calificaciones finales."""
    try:
        orden  = ['A', 'B', 'C', 'D', 'F']
        conteo = df['Grade'].value_counts().reindex(orden, fill_value=0)
        colores = [PALETTE_GRADE[g] for g in orden]

        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.bar(conteo.index, conteo.values, color=colores,
                      edgecolor='white', linewidth=1.5)
        for bar, val in zip(bars, conteo.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                    str(val), ha='center', va='bottom', fontweight='bold', fontsize=10)
        ax.set_title('Distribución de Calificaciones', fontweight='bold')
        ax.set_xlabel('Calificación Final')
        ax.set_ylabel('Cantidad de Estudiantes')
        ax.set_ylim(0, conteo.max() * 1.15)
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Error en gráfico de grades: {e}")
        return None

def grafico_departamento(df):
    """Bar horizontal: score promedio por departamento."""
    try:
        resumen = (df.groupby('Department')['Total_Score']
                     .mean()
                     .sort_values(ascending=True)
                     .round(2))

        fig, ax = plt.subplots(figsize=(7, 4))
        colores = sns.color_palette('Blues_d', len(resumen))
        bars = ax.barh(resumen.index, resumen.values, color=colores,
                       edgecolor='white', linewidth=1)
        for bar, val in zip(bars, resumen.values):
            ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                    f'{val:.1f}', va='center', fontweight='bold', fontsize=10)
        ax.set_title('Score Promedio por Departamento', fontweight='bold')
        ax.set_xlabel('Total Score Promedio')
        ax.set_xlim(0, resumen.max() * 1.12)
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Error en gráfico de departamento: {e}")
        return None

def grafico_estres_reprobacion(df):
    """Bar chart: tasa de reprobación por nivel de estrés."""
    try:
        resumen = (df.groupby('Stress_Level (1-10)')
                     .apply(lambda g: 100 * (g['Grade'] == 'F').mean())
                     .reset_index())
        resumen.columns = ['Nivel_Estres', 'Tasa']
        resumen['Nivel_Estres'] = resumen['Nivel_Estres'].astype(str)

        colores = ['#2ecc71' if t < 15 else '#f39c12' if t < 20 else '#e74c3c'
                   for t in resumen['Tasa']]

        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(resumen['Nivel_Estres'], resumen['Tasa'],
                      color=colores, edgecolor='white', linewidth=1.5)
        for bar, val in zip(bars, resumen['Tasa']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    f'{val:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
        ax.set_title('Tasa de Reprobación por Nivel de Estrés', fontweight='bold')
        ax.set_xlabel('Nivel de Estrés (1–10)')
        ax.set_ylabel('% Reprobados')
        ax.set_ylim(0, resumen['Tasa'].max() * 1.2)
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Error en gráfico de estrés: {e}")
        return None

def grafico_brecha_internet(df):
    """Bar agrupado: score por ingresos x acceso a internet."""
    try:
        resumen = (df.groupby(['Family_Income_Level', 'Internet_Access_at_Home'])['Total_Score']
                     .mean().round(2).unstack())
        orden = [c for c in ['Low', 'Medium', 'High'] if c in resumen.index]
        resumen = resumen.reindex(orden)

        x     = np.arange(len(orden))
        width = 0.35
        fig, ax = plt.subplots(figsize=(7, 4))

        if 'Yes' in resumen.columns:
            bars1 = ax.bar(x - width/2, resumen['Yes'], width, label='Con Internet',
                           color='#2980b9', edgecolor='white')
            for bar in bars1:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                        f'{bar.get_height():.1f}', ha='center', fontsize=9, fontweight='bold')
        if 'No' in resumen.columns:
            bars2 = ax.bar(x + width/2, resumen['No'], width, label='Sin Internet',
                           color='#c0392b', edgecolor='white')
            for bar in bars2:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                        f'{bar.get_height():.1f}', ha='center', fontsize=9, fontweight='bold')

        ax.set_title('Score por Ingresos y Acceso a Internet', fontweight='bold')
        ax.set_xlabel('Nivel de Ingresos')
        ax.set_ylabel('Total Score Promedio')
        ax.set_xticks(x)
        ax.set_xticklabels(['Bajos (Low)', 'Medios (Medium)', 'Altos (High)'])
        ax.legend()
        ax.set_ylim(0, df['Total_Score'].max() * 1.15)
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Error en gráfico de brecha: {e}")
        return None

def grafico_eficiencia(df):
    """Bar chart: eficiencia y horas de estudio por categoría de riesgo."""
    try:
        resumen = (df.groupby('Categoria_Riesgo')
                     .agg(Eficiencia=('Eficiencia_Estudio', 'mean'),
                          Horas=('Study_Hours_per_Week', 'mean'))
                     .round(2)
                     .reindex(['Bajo', 'Medio', 'Alto']))

        x     = np.arange(len(resumen))
        width = 0.35
        fig, ax = plt.subplots(figsize=(7, 4))

        bars1 = ax.bar(x - width/2, resumen['Eficiencia'], width,
                       label='Eficiencia Promedio', color='#2ecc71', edgecolor='white')
        bars2 = ax.bar(x + width/2, resumen['Horas'], width,
                       label='Horas Promedio', color='#2980b9', edgecolor='white')

        for bar in list(bars1) + list(bars2):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{bar.get_height():.1f}', ha='center', fontsize=9, fontweight='bold')

        ax.set_title('Eficiencia y Horas de Estudio por Riesgo', fontweight='bold')
        ax.set_xlabel('Categoría de Riesgo')
        ax.set_xticks(x)
        ax.set_xticklabels(['Bajo', 'Medio', 'Alto'])
        ax.legend()
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Error en gráfico de eficiencia: {e}")
        return None

# ══════════════════════════════════════════════════════════════════
# SIDEBAR — FILTROS
# ══════════════════════════════════════════════════════════════════
def construir_sidebar(df):
    """Construye el panel de filtros y retorna el dataframe filtrado."""
    st.sidebar.image(
        "https://img.icons8.com/color/96/graduation-cap.png",
        width=80
    )
    st.sidebar.title("🔍 Filtros")
    st.sidebar.markdown("Filtrá los datos para explorar subgrupos específicos.")
    st.sidebar.markdown("---")

    try:
        # Filtro Departamento
        depts = sorted(df['Department'].unique().tolist())
        sel_dept = st.sidebar.multiselect(
            "🏫 Departamento",
            options=depts,
            default=depts,
            help="Seleccioná uno o más departamentos"
        )

        # Filtro Categoría de Riesgo
        riesgos = ['Bajo', 'Medio', 'Alto']
        sel_riesgo = st.sidebar.multiselect(
            "⚠️ Categoría de Riesgo",
            options=riesgos,
            default=riesgos,
            help="Filtrá por nivel de riesgo académico"
        )

        # Filtro Nivel de Ingresos
        ingresos = sorted(df['Family_Income_Level'].unique().tolist())
        sel_ingreso = st.sidebar.multiselect(
            "💰 Nivel de Ingresos",
            options=ingresos,
            default=ingresos,
            help="Filtrá por nivel de ingresos familiar"
        )

        # Filtro Grade
        grades = ['A', 'B', 'C', 'D', 'F']
        sel_grade = st.sidebar.multiselect(
            "🎓 Calificación Final",
            options=grades,
            default=grades,
            help="Filtrá por calificación obtenida"
        )

        # Filtro Acceso a Internet
        st.sidebar.markdown("---")
        internet = st.sidebar.radio(
            "🌐 Acceso a Internet",
            options=["Todos", "Con Internet", "Sin Internet"],
            index=0
        )

        st.sidebar.markdown("---")
        st.sidebar.markdown("📌 **Nota:** Los gráficos se actualizan automáticamente al cambiar los filtros.")

        # ── Aplicar filtros ───────────────────────────────────────
        df_filtrado = df.copy()

        if sel_dept:
            df_filtrado = df_filtrado[df_filtrado['Department'].isin(sel_dept)]
        if sel_riesgo:
            df_filtrado = df_filtrado[df_filtrado['Categoria_Riesgo'].isin(sel_riesgo)]
        if sel_ingreso:
            df_filtrado = df_filtrado[df_filtrado['Family_Income_Level'].isin(sel_ingreso)]
        if sel_grade:
            df_filtrado = df_filtrado[df_filtrado['Grade'].isin(sel_grade)]
        if internet == "Con Internet":
            df_filtrado = df_filtrado[df_filtrado['Internet_Access_at_Home'] == 'Yes']
        elif internet == "Sin Internet":
            df_filtrado = df_filtrado[df_filtrado['Internet_Access_at_Home'] == 'No']

        return df_filtrado

    except Exception as e:
        st.sidebar.error(f"Error en filtros: {e}")
        return df

# ══════════════════════════════════════════════════════════════════
# APP PRINCIPAL
# ══════════════════════════════════════════════════════════════════
def main():
    # ── Header ───────────────────────────────────────────────────
    st.title("📊 Análisis Académico Estudiantil")
    st.markdown("**TPI — Introducción al Análisis de Datos** | UTN Tecnicatura en Programación")
    st.markdown("Explorá el rendimiento, riesgo y equidad del dataset de 5.000 estudiantes universitarios.")
    st.markdown("---")

    # ── Carga de datos ───────────────────────────────────────────
    with st.spinner("Cargando datos..."):
        df, error = cargar_datos()

    if error:
        st.error(f"❌ No se pudieron cargar los datos: {error}")
        st.info("Verificá que el archivo `students_clean.csv` esté disponible en el repositorio de GitHub.")
        st.stop()

    # ── Filtros ──────────────────────────────────────────────────
    df_filtrado = construir_sidebar(df)

    # ── Validación de datos filtrados ────────────────────────────
    if len(df_filtrado) == 0:
        st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados. Ajustá los filtros.")
        st.stop()

    # ── Indicador de filtro activo ───────────────────────────────
    if len(df_filtrado) < len(df):
        st.info(f"🔍 Mostrando **{len(df_filtrado):,}** de **{len(df):,}** estudiantes según los filtros aplicados.")

    # ── KPIs ─────────────────────────────────────────────────────
    st.subheader("📌 Indicadores Clave")
    total, promedio, pct_riesgo, pct_reprobado = calcular_kpis(df_filtrado)
    mostrar_kpis(total, promedio, pct_riesgo, pct_reprobado)

    st.markdown("---")

    # ── Fila 1: Pie + Grades ─────────────────────────────────────
    st.subheader("📊 Distribución General")
    col1, col2 = st.columns(2)

    with col1:
        fig = grafico_riesgo_pie(df_filtrado)
        if fig:
            st.pyplot(fig)
            plt.close(fig)
            st.caption("Proporción de estudiantes por categoría de riesgo académico.")

    with col2:
        fig = grafico_grades_bar(df_filtrado)
        if fig:
            st.pyplot(fig)
            plt.close(fig)
            st.caption("Cantidad de estudiantes por calificación final obtenida.")

    st.markdown("---")

    # ── Fila 2: Departamento (ancho completo) ────────────────────
    st.subheader("🏫 Rendimiento por Departamento")
    fig = grafico_departamento(df_filtrado)
    if fig:
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Score promedio por departamento, ordenado de mayor a menor.")

    st.markdown("---")

    # ── Fila 3: Estrés + Brecha ──────────────────────────────────
    st.subheader("⚠️ Factores de Riesgo y Equidad")
    col1, col2 = st.columns(2)

    with col1:
        fig = grafico_estres_reprobacion(df_filtrado)
        if fig:
            st.pyplot(fig)
            plt.close(fig)
            st.caption("A mayor estrés, mayor tasa de reprobación.")

    with col2:
        fig = grafico_brecha_internet(df_filtrado)
        if fig:
            st.pyplot(fig)
            plt.close(fig)
            st.caption("Brecha de rendimiento según ingresos y acceso a internet.")

    st.markdown("---")

    # ── Fila 4: Eficiencia (ancho completo) ──────────────────────
    st.subheader("📚 Eficiencia del Esfuerzo")
    fig = grafico_eficiencia(df_filtrado)
    if fig:
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Estudiantes de Riesgo Alto estudian menos horas pero con menor eficiencia real.")

    st.markdown("---")

    # ── Tabla de datos ───────────────────────────────────────────
    with st.expander("🗂️ Ver tabla de datos filtrados"):
        cols_mostrar = [
            'Student_ID', 'Department', 'Grade', 'Total_Score',
            'Attendance (%)', 'Categoria_Riesgo', 'Family_Income_Level',
            'Internet_Access_at_Home', 'Stress_Level (1-10)', 'Eficiencia_Estudio'
        ]
        st.dataframe(
            df_filtrado[cols_mostrar].reset_index(drop=True),
            use_container_width=True,
            height=300
        )
        st.caption(f"Mostrando {len(df_filtrado):,} registros.")

    # ── Footer ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "**TPI — Introducción al Análisis de Datos** · UTN Tecnicatura en Programación  \n"
        "Integrantes: Nicolas Llaneza · David Lopez · Sabrina Morein"
    )

if __name__ == "__main__":
    main()
