import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import seaborn as sns
from scipy import stats

# car_data = df_cd
df_cd = pd.read_csv('vehicles_us_limpio.csv') # leer los datos

df_cd = pd.read_csv('vehicles_us_limpio.csv')

# Título principal
st.title('Análisis de Vehículos Usados en EE.UU.')

# Encabezado
st.header('Distribución de Precios')

# Histograma de precios
fig, ax = plt.subplots()
sns.histplot(df_cd['price'], bins=30, kde=False, ax=ax, color='skyblue')
ax.set_xlabel('Precio')
ax.set_ylabel('Cantidad de vehículos')
st.pyplot(fig)

# Gráfico de dispersión: Precio vs Odómetro
st.header('Precio vs. Odómetro')
fig2, ax2 = plt.subplots()
sns.scatterplot(x='odometer', y='price', data=df_cd, ax=ax2, alpha=0.5)
ax2.set_xlabel('Odómetro (millas)')
ax2.set_ylabel('Precio')
st.pyplot(fig2)

# Casilla de verificación para mostrar los datos
if st.checkbox('Mostrar datos del DataFrame'):
    st.write(df_cd)
