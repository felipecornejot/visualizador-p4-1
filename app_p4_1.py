import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests

# --- Paleta de Colores ---
# Definición de colores en formato RGB (0-1) para Matplotlib
color_primario_1_rgb = (14/255, 69/255, 74/255) # 0E454A (Oscuro)
color_primario_2_rgb = (31/255, 255/255, 95/255) # 1FFF5F (Verde vibrante)
color_primario_3_rgb = (255/255, 255/255, 255/255) # FFFFFF (Blanco)

# Colores del logo de Sustrend para complementar
color_sustrend_1_rgb = (0/255, 155/255, 211/255) # 009BD3 (Azul claro)
color_sustrend_2_rgb = (0/255, 140/255, 207/255) # 008CCF (Azul medio)
color_sustrend_3_rgb = (0/255, 54/255, 110/255) # 00366E (Azul oscuro)

# Selección de colores para los gráficos
colors_for_charts = [color_primario_1_rgb, color_primario_2_rgb, color_sustrend_1_rgb, color_sustrend_3_rgb]

# --- Configuración de la página de Streamlit ---
st.set_page_config(layout="wide")

st.title('✨ Visualizador de Impactos - Proyecto P4')
st.subheader('Desarrollo de salchichas plant based con bajo impacto ambiental')
st.markdown("""
    Ajusta los parámetros para explorar cómo las proyecciones de impacto ambiental, social y económico del proyecto
    varían con diferentes escenarios de volumen producido, factores de emisión, ahorro de agua y precio de mercado.
""")

# --- Widgets Interactivos para Parámetros (Streamlit) ---
st.sidebar.header('Parámetros de Simulación')

volumen_total = st.sidebar.slider(
    'Volumen Total Producido (ton/año):',
    min_value=10,
    max_value=100,
    value=20,
    step=5,
    help="Volumen total de producto producido anualmente."
)

factor_gei_kg = st.sidebar.slider(
    'Factor de GEI Evitados (tCO₂e/ton):',
    min_value=3.5,
    max_value=4.5,
    value=4.1,
    step=0.1,
    help="Emisiones de GEI evitadas por tonelada de producto."
)

factor_agua_litros = st.sidebar.slider(
    'Agua Ahorrada (L/kg de carne reemplazada):',
    min_value=1000,
    max_value=2000,
    value=1500,
    step=100,
    help="Ahorro de agua por kg de carne reemplazada."
)

# Changed 'format='.1%' to simply a label without the explicit '%' sign in the label itself
# and removed format parameter to see if that's the culprit.
# We can format it in the calculation display later if needed.
factor_sustitucion = st.sidebar.slider(
    'Factor de Sustitución de Insumos Sintéticos (decimal):', # Changed label
    min_value=0.1,
    max_value=0.5,
    value=0.3,
    step=0.01,
    # format='.1%', # Removed this to see if it's the issue. We'll format it manually if needed.
    help="Porcentaje de insumos sintéticos reemplazados por naturales (ej. 0.3 para 30%)." # Simplified help
)

precio_mercado = st.sidebar.slider(
    'Precio de Mercado Plant-based (USD/ton):',
    min_value=5000,
    max_value=15000,
    value=10000,
    step=500,
    help="Precio de venta estimado por tonelada."
)

# --- Cálculos de Indicadores ---
gei_ev_ev = volumen_total * factor_gei_kg
agua_ahorrada_litros = volumen_total * factor_agua_litros * 1000
ingredientes_reemplazados = volumen_total * factor_sustitucion
ingresos_estimados = volumen_total * precio_mercado
empleos_generados = 3
simbiosis_industrial = 5


st.header('Resultados Proyectados Anuales:')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🌎 **GEI Evitados**", value=f"{gei_ev_ev:.2f} tCO₂e/año")
    st.caption("Reducción de emisiones de gases de efecto invernadero.")
with col2:
    st.metric(label="💧 **Agua Ahorrada**", value=f"{agua_ahorrada_litros/1000:.2f} m³/año")
    st.caption("Ahorro de agua en el proceso productivo.")
with col3:
    # Now, format the replaced ingredients as a percentage if factor_sustitucion was meant to be displayed as such
    st.metric(label="♻️ **Insumos Sintéticos Reemplazados**", value=f"{ingredientes_reemplazados:.2f} ton/año")
    st.caption("Cantidad de ingredientes sintéticos sustituidos por naturales.")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(label="💰 **Ingresos Estimados**", value=f"USD {ingresos_estimados:,.2f}")
    st.caption("Ingresos proyectados por la venta del producto.")
with col5:
    st.metric(label="👥 **Empleos Generados**", value=f"{empleos_generados}")
    st.caption("Nuevos puestos de trabajo creados por el proyecto.")
with col6:
    st.metric(label="🤝 **Simbiosis Industrial**", value=f"{simbiosis_industrial} interacciones")
    st.caption("Número de colaboraciones para el intercambio de recursos.")

st.markdown("---")

st.header('📊 Análisis Gráfico de Impactos')

# --- Visualización (Gráficos 2D con Matplotlib) ---
base_gei = 82
base_agua = 270   # en m³
base_ingrepl = 6
base_ingresos = 200000

# Convertir agua_ahorrada_litros a m³ para el gráfico
agua_ahorrada_m3 = agua_ahorrada_litros / 1000

# Creamos una figura con 3 subplots (2D)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7), facecolor=color_primario_3_rgb)
fig.patch.set_facecolor(color_primario_3_rgb)

# Definición de etiquetas y valores para los gráficos de barras 2D
labels = ['Línea Base', 'Proyección']
bar_width = 0.6
x = np.arange(len(labels))

# --- Gráfico 1: GEI Evitados (tCO₂e/año) ---
gei_values = [base_gei, gei_ev_ev]
bars1 = ax1.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax1.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax1.set_title('GEI Evitados', fontsize=14, color=colors_for_charts[3], pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax1.yaxis.set_tick_params(colors=colors_for_charts[0])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='x', length=0)
max_gei_val = max(gei_values)
ax1.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 1))
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 2: Agua Ahorrada (m³/año) ---
agua_values = [base_agua, agua_ahorrada_m3]
bars2 = ax2.bar(x, agua_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax2.set_ylabel('m³/año', fontsize=12, color=colors_for_charts[0])
ax2.set_title('Agua Ahorrada', fontsize=14, color=colors_for_charts[3], pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax2.yaxis.set_tick_params(colors=colors_for_charts[0])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='x', length=0)
max_agua_val = max(agua_values)
ax2.set_ylim(bottom=0, top=max(max_agua_val * 1.15, 1))
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 3: Ingresos Estimados (USD/año) ---
ingresos_values = [base_ingresos, ingresos_estimados]
bars3 = ax3.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax3.set_ylabel('USD/año', fontsize=12, color=colors_for_charts[3])
ax3.set_title('Ingresos Estimados', fontsize=14, color=colors_for_charts[3], pad=20)
ax3.set_xticks(x)
ax3.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax3.yaxis.set_tick_params(colors=colors_for_charts[0])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.tick_params(axis='x', length=0)
max_ingresos_val = max(ingresos_values)
ax3.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000))
for bar in bars3:
    yval = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"${yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
st.pyplot(fig)

# --- Funcionalidad de descarga de cada gráfico ---
st.markdown("---")
st.subheader("Descargar Gráficos Individualmente")

# Función auxiliar para generar el botón de descarga
def download_button(fig, filename_prefix, key):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button(
        label=f"Descargar {filename_prefix}.png",
        data=buf.getvalue(),
        file_name=f"{filename_prefix}.png",
        mime="image/png",
        key=key
    )

# Crear figuras individuales para cada gráfico para poder descargarlas
# Figura 1: GEI Evitados
fig_gei, ax_gei = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_gei.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax_gei.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax_gei.set_title('GEI Evitados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_gei.set_xticks(x)
ax_gei.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_gei.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_gei.spines['top'].set_visible(False)
ax_gei.spines['right'].set_visible(False)
ax_gei.tick_params(axis='x', length=0)
ax_gei.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 1))
for bar in ax_gei.patches:
    yval = bar.get_height()
    ax_gei.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_gei, "GEI_Evitados", "download_gei")
plt.close(fig_gei)

# Figura 2: Agua Ahorrada
fig_agua, ax_agua = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_agua.bar(x, agua_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax_agua.set_ylabel('m³/año', fontsize=12, color=colors_for_charts[0])
ax_agua.set_title('Agua Ahorrada', fontsize=14, color=colors_for_charts[3], pad=20)
ax_agua.set_xticks(x)
ax_agua.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_agua.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_agua.spines['top'].set_visible(False)
ax_agua.spines['right'].set_visible(False)
ax_agua.tick_params(axis='x', length=0)
ax_agua.set_ylim(bottom=0, top=max(max_agua_val * 1.15, 1))
for bar in ax_agua.patches:
    yval = bar.get_height()
    ax_agua.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_agua, "Agua_Ahorrada", "download_agua")
plt.close(fig_agua)

# Figura 3: Ingresos Estimados
fig_ingresos, ax_ingresos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_ingresos.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax_ingresos.set_ylabel('USD/año', fontsize=12, color=colors_for_charts[3])
ax_ingresos.set_title('Ingresos Estimados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_ingresos.set_xticks(x)
ax_ingresos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_ingresos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_ingresos.spines['top'].set_visible(False)
ax_ingresos.spines['right'].set_visible(False)
ax_ingresos.tick_params(axis='x', length=0)
ax_ingresos.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000))
for bar in ax_ingresos.patches:
    yval = bar.get_height()
    ax_ingresos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"${yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_ingresos, "Ingresos_Estimados", "download_ingresos")
plt.close(fig_ingresos)


st.markdown("---")
st.markdown("### Información Adicional:")
st.markdown(f"- **Estado de Avance y Recomendaciones:** El proyecto se encuentra actualmente en una fase de validación avanzada a escala piloto, con desarrollo tecnológico liderado por CREAS. Se han logrado avances significativos en la formulación de salchichas a base de plantas, incluyendo pruebas de sabor, textura y conservación. Asimismo, se han realizado análisis comparativos preliminares sobre la huella de carbono del producto respecto de su equivalente animal y frente a alternativas plant based importadas, mostrando resultados promisorios en términos de sostenibilidad ambiental y sustitución de insumos.")

st.markdown("---")
# Texto de atribución centrado
st.markdown("<div style='text-align: center;'>Visualizador Creado por el equipo Sustrend SpA en el marco del Proyecto TT GREEN Foods</div>", unsafe_allow_html=True)

# Aumentar el espaciado antes de los logos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Mostrar Logos ---
col_logos_left, col_logos_center, col_logos_right = st.columns([1, 2, 1])

with col_logos_center:
    sustrend_logo_url = "https://drive.google.com/uc?id=1vx_znPU2VfdkzeDtl91dlpw_p9mmu4dd"
    ttgreenfoods_logo_url = "https://drive.google.com/uc?id=1uIQZQywjuQJz6Eokkj6dNSpBroJ8tQf8"

    try:
        sustrend_response = requests.get(sustrend_logo_url)
        sustrend_response.raise_for_status()
        sustrend_image = Image.open(BytesIO(sustrend_response.content))

        ttgreenfoods_response = requests.get(ttgreenfoods_logo_url)
        ttgreenfoods_response.raise_for_status()
        ttgreenfoods_image = Image.open(BytesIO(ttgreenfoods_response.content))

        st.image([sustrend_image, ttgreenfoods_image], width=100)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar los logos desde las URLs. Por favor, verifica los enlaces: {e}")
    except Exception as e:
        st.error(f"Error inesperado al procesar las imágenes de los logos: {e}")

st.markdown("<div style='text-align: center; font-size: small; color: gray;'>Viña del Mar, Valparaíso, Chile</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align: center; font-size: smaller; color: gray;'>Versión del Visualizador: 1.0</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='text-align: center; font-size: x-small; color: lightgray;'>Desarrollado con Streamlit</div>", unsafe_allow_html=True)
