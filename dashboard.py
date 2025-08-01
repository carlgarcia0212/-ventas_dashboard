import pandas as pd
import streamlit as st
import plotly.express as px

# =====================
# CONFIGURACIÓN INICIAL
# =====================
st.set_page_config(page_title="Dashboard Ventas 2024", layout="wide")
st.markdown(
    """
    <style>
        .reportview-container {background-color: #0e1117; color: white;}
        .stMetric {background-color: #262730; padding: 20px; border-radius: 10px; text-align: center;}
    </style>
    """, unsafe_allow_html=True
)
st.title("Dashboard Interactivo de Ventas 2024")
st.markdown("Explora las ventas por región, categoría y mes. **Descarga el resultado filtrado con un clic.**")

# =====================
# CARGAR DATOS
# =====================
@st.cache_data
def cargar_datos():
    return pd.read_csv("ventas_2024.csv")

data = cargar_datos()
data['Fecha'] = pd.to_datetime(data['Fecha'])

# =====================
# FILTROS
# =====================
col1, col2, col3 = st.columns(3)
with col1:
    regiones = st.multiselect("Selecciona Región:", data['Región'].unique(), default=data['Región'].unique())
with col2:
    categorias = st.multiselect("Selecciona Categoría:", data['Categoría'].unique(), default=data['Categoría'].unique())
with col3:
    meses = st.multiselect("Selecciona Mes:", data['Mes'].unique(), default=data['Mes'].unique())

filtro = data[
    (data['Región'].isin(regiones)) &
    (data['Categoría'].isin(categorias)) &
    (data['Mes'].isin(meses))
]

# =====================
# KPIs
# =====================
# ==== KPIs mejorados ====
st.markdown(
    """
    <style>
    .big-font {
        font-size:40px !important;
        font-weight: bold;
        color: #FFFFFF;
    }
    .kpi-box {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
    }
    </style>
    """,
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown(f"<div class='kpi-box'>Ventas Totales<br><span class='big-font'>${filtro['Ventas'].sum():,}</span></div>", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"<div class='kpi-box'>Promedio Venta<br><span class='big-font'>${filtro['Ventas'].mean():,.0f}</span></div>", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"<div class='kpi-box'>Cantidad Total<br><span class='big-font'>{filtro['Cantidad'].sum():,}</span></div>", unsafe_allow_html=True)


# =====================
# GRÁFICOS
# =====================
st.subheader("Gráficos")

ventas_mes = filtro.groupby('Mes')['Ventas'].sum().reset_index()
fig_barras = px.bar(ventas_mes, x='Mes', y='Ventas', title="Ventas por Mes", text_auto=True, color_discrete_sequence=['#1f77b4'])

ventas_cat = filtro.groupby('Categoría')['Ventas'].sum().reset_index()
fig_pie = px.pie(ventas_cat, names='Categoría', values='Ventas', title="Distribución por Categoría")

ventas_tendencia = filtro.groupby('Fecha')['Ventas'].sum().reset_index()
fig_linea = px.line(ventas_tendencia, x='Fecha', y='Ventas', title="Tendencia de Ventas Diarias", color_discrete_sequence=['#ff7f0e'])

st.plotly_chart(fig_barras, use_container_width=True)
st.plotly_chart(fig_pie, use_container_width=True)
st.plotly_chart(fig_linea, use_container_width=True)

# =====================
# DESCARGA DE DATOS
# =====================
st.subheader("Descargar datos filtrados")
csv = filtro.to_csv(index=False).encode('utf-8')
st.download_button(label="Descargar CSV", data=csv, file_name="ventas_filtradas.csv", mime="text/csv")

# =====================
# TABLA
# =====================
st.subheader("Datos filtrados")
st.dataframe(filtro)

