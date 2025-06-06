import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

# Título principal
st.title('Análisis de Vehículos Usados en EE.UU.')

# Lectura de datos
url_data = "https://raw.githubusercontent.com/ZarRomM/Proyect-7-Streamlit/main/vehicles_us_limpio.csv"
df_cd = pd.read_csv(url_data)

# Muestra del DF
st.header('DataFrame US Cars')
st.dataframe(df_cd)

# Encabezado
st.header('Distribución de Precios')

# Histograma de precios
fig, ax = plt.subplots()
sns.histplot(df_cd['price'], bins=30, kde=False, ax=ax, color='#0077b6')
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


st.subheader('Año vs Condición')
precio_vs_ano = df_cd.groupby('model_year')['condition']
st.bar_chart(precio_vs_ano)

st.subheader('Histograma de Año')
ax = df_cd['model_year'].hist()
st.pyplot(ax.figure)

min_year = st.slider('Selecciona que año mínimo quieres buscar', min_value=1.0, max_value=10.0, step=0.5)
st.dataframe(df_cd.querry('model_year>=@min_year'))