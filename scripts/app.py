
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# Paths
COEF_DIR = os.path.join(os.path.dirname(__file__), '..', 'COEFICIENTES')
CSV_CONS_PESO = os.path.join(COEF_DIR, 'resultados_cons_vs_peso.csv')
CSV_DIA_CONS = os.path.join(COEF_DIR, 'resultados_dia_vs_cons.csv')
LOGO_PATH = os.path.join(COEF_DIR, 'logo mejorado_PEQ.png')

# Load data
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

df_cons_peso = load_csv(CSV_CONS_PESO)
df_dia_cons = load_csv(CSV_DIA_CONS)
logo = Image.open(LOGO_PATH)

# UI
st.image(logo, width=120)
st.title('ALBATEQ S. A. - Dirección Técnica')
st.subheader('Cálculos de Consumos vs la Línea Genética y Peso Estimado de Acuerdo al Consumo Real en granjas.')

razas = sorted(df_cons_peso['RAZA'].unique())
sexos = sorted(df_cons_peso['SEXO'].unique())
raza = st.selectbox('Seleccione la Raza (Línea Genética):', razas)
sexo = st.selectbox('Seleccione el Sexo:', sexos)
dia = st.number_input('Día', min_value=14, value=14)
consumo_real = st.number_input('Consumo Acumulado Real', min_value=0.01, value=0.01)
peso_real = st.number_input('Peso Real', min_value=0.01, value=0.01)

def get_poly_coeffs(df, raza, sexo):
    row = df[(df['RAZA'] == raza) & (df['SEXO'] == sexo)].iloc[0]

    return [row[f'coef_{i}'] for i in range(4, -1, -1)]

def predict_poly(coeffs, x):
    return np.polyval(coeffs, x)

if st.button('Generar Informe'):
    # Cálculos
    coeffs_dia_cons = get_poly_coeffs(df_dia_cons, raza, sexo)
    consumo_estimado = predict_poly(coeffs_dia_cons, dia)
    coeffs_cons_peso = get_poly_coeffs(df_cons_peso, raza, sexo)
    peso_estimado = predict_poly(coeffs_cons_peso, consumo_real)

    diff_cons = consumo_real - consumo_estimado
    pct_diff_cons = 100 * diff_cons / consumo_estimado if consumo_estimado else 0
    diff_peso = peso_real - peso_estimado
    pct_diff_peso = 100 * diff_peso / peso_estimado if peso_estimado else 0
    conversion = consumo_real / peso_real if peso_real else 0

    st.markdown('---')
    st.header('Resultados')
    st.markdown(f"""
    **Consumo Acumulado Estimado para Día {dia}:** {consumo_estimado:.2f}  
    **Consumo Acumulado Real Ingresado:** {consumo_real:.2f}  
    **Diferencia Consumo Acumulado (real - estimado):** {diff_cons:.2f} ({pct_diff_cons:.2f}%)
    
    ---
    **Peso Estimado para Consumo Acumulado {consumo_real}:** {peso_estimado:.2f}  
    **Peso Real ingresado:** {peso_real:.2f}  
    **Diferencia Peso (real - estimado):** {diff_peso:.2f} ({pct_diff_peso:.2f}%)
    
    ---
    **Conversión Alimenticia:** {conversion:.2f}
    """)


    # Gráfico 1: Consumo Acumulado Estimado vs Real por Día
    fig1, ax1 = plt.subplots()
    dias = np.linspace(14, dia+15, 100)
    cons_estimados = predict_poly(coeffs_dia_cons, dias)
    ax1.plot(dias, cons_estimados, 'r-', label='Consumo Acumulado Estimado')
    # Punto real
    ax1.plot([dia], [consumo_real], 'bo', label='Consumo Acumulado Real (input)')
    # Punto estimado
    ax1.plot([dia], [consumo_estimado], 'gx', markersize=10, label='Consumo Acumulado Estimado (input)')
    ax1.set_xlabel('Día')
    ax1.set_ylabel('Consumo Acumulado')
    ax1.set_title('Consumo Acumulado Estimado vs Real por Día')
    ax1.set_xlim(14, dia+15)
    ax1.legend()
    # Marca de agua
    ax1.imshow(logo, aspect='auto', extent=(ax1.get_xlim()[0], ax1.get_xlim()[1], ax1.get_ylim()[0], ax1.get_ylim()[1]), alpha=0.15, zorder=-1)
    st.pyplot(fig1)

    # Gráfico 2: Peso Estimado vs Real por Cons Acumulado
    fig2, ax2 = plt.subplots()
    cons_min = 0
    cons_max = consumo_real + 1000
    cons_range = np.linspace(cons_min, cons_max, 100)
    pesos_estimados = predict_poly(coeffs_cons_peso, cons_range)
    ax2.plot(cons_range, pesos_estimados, color='orange', label='Peso Estimado')
    # Punto real
    ax2.plot([consumo_real], [peso_real], 'bo', label='Peso Real (input)')
    # Punto estimado
    ax2.plot([consumo_real], [peso_estimado], 'gx', markersize=10, label='Peso estimado (input)')
    ax2.set_xlabel('Consumo Acumulado')
    ax2.set_ylabel('Peso')
    ax2.set_title('Peso Estimado vs Real por Cons Acumulado')
    ax2.set_xlim(cons_min, cons_max)
    ax2.legend()
    # Marca de agua
    ax2.imshow(logo, aspect='auto', extent=(ax2.get_xlim()[0], ax2.get_xlim()[1], ax2.get_ylim()[0], ax2.get_ylim()[1]), alpha=0.15, zorder=-1)
    st.pyplot(fig2)

    st.markdown('---')
    st.caption('Herramienta para apoyo en granja. Uso bajo su exclusiva responsabilidad. No sustituye la asesoría profesional y Albateq S.A. no se responsabiliza por las decisiones tomadas con base en ellos.')
