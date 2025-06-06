import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport

# Título principal
st.title('Análisis de Vehículos Usados en EE.UU.')

# Lectura de datos
url_data = "https://raw.githubusercontent.com/ZarRomM/Proyect-7-Streamlit/main/vehicles_us_raw.csv"
df_cd = pd.read_csv(url_data)

# Muestra del DF
st.header('DataFrame US Cars')
st.dataframe(df_cd)

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

# Reporte de YData Profiling
pr = ProfileReport(df_cd, title="Reporte YData Profiling")
html = pr.to_html()
st.components.v1.html(html, height=1000, scrolling=True)
