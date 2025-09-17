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

# Load logo
logo = Image.open(LOGO_PATH)

# UI
st.image(logo, width=120)
st.title('ALBATEQ S. A. - Dirección Técnica')
st.subheader('Cálculos de Consumos vs la Línea Genética y Peso Estimado de Acuerdo al Consumo Real en granjas.')

# Selectors

razas = sorted(df_cons_peso['RAZA'].unique())
sexos = sorted(df_cons_peso['SEXO'].unique())
raza = st.selectbox('Seleccione la Raza (Línea Genética):', razas)
sexo = st.selectbox('Seleccione el Sexo:', sexos)

dia = st.number_input('Día', min_value=0, value=0)
consumo_real = st.number_input('Consumo Acumulado Real', min_value=0.0, value=0.0)
peso_real = st.number_input('Peso Real', min_value=0.0, value=0.0)

# Filtrar coeficientes

def get_poly_coeffs(df, raza, sexo):
    row = df[(df['RAZA'] == raza) & (df['SEXO'] == sexo)].iloc[0]
    return [row[f'coef_{i}'] for i in range(4, -1, -1)]  # coef_4 ... coef_0

def predict_poly(coeffs, x):
    return np.polyval(coeffs, x)

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

# Resultados
st.markdown('---')
st.header('Resultados')
st.write(f"Consumo Acumulado Estimado: {consumo_estimado:.2f}")
st.write(f"Peso Estimado: {peso_estimado:.2f}")
st.write(f"Diferencia Consumo (abs): {diff_cons:.2f} | (%) {pct_diff_cons:.2f}%")
st.write(f"Diferencia Peso (abs): {diff_peso:.2f} | (%) {pct_diff_peso:.2f}%")
st.write(f"Conversión Alimenticia: {conversion:.2f}")

# Gráficos
fig1, ax1 = plt.subplots()
ax1.plot([dia], [consumo_real], 'ro', label='Consumo Real')
ax1.plot([dia], [consumo_estimado], 'bo', label='Consumo Estimado')
ax1.set_xlabel('Día')
ax1.set_ylabel('Consumo Acumulado')
ax1.legend()
ax1.set_title('Consumo Acumulado vs. Día')
ax1.imshow(logo, aspect='auto', extent=(ax1.get_xlim()[0], ax1.get_xlim()[1], ax1.get_ylim()[0], ax1.get_ylim()[1]), alpha=0.15, zorder=-1)
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.plot([consumo_real], [peso_real], 'ro', label='Peso Real')
ax2.plot([consumo_real], [peso_estimado], 'bo', label='Peso Estimado')
ax2.set_xlabel('Consumo Acumulado Real')
ax2.set_ylabel('Peso')
ax2.legend()
ax2.set_title('Peso vs. Consumo Acumulado')
ax2.imshow(logo, aspect='auto', extent=(ax2.get_xlim()[0], ax2.get_xlim()[1], ax2.get_ylim()[0], ax2.get_ylim()[1]), alpha=0.15, zorder=-1)
st.pyplot(fig2)

st.markdown('---')
st.caption('Se ofrece como ayuda para cálculos a nivel de granja, úsela bajo su criterio.')
