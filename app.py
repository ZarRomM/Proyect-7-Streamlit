import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import altair as alt

# Título principal
st.title('Análisis de Vehículos Usados en EE.UU.')

# Lectura de datos
url_data = "https://raw.githubusercontent.com/ZarRomM/Proyect-7-Streamlit/main/vehicles_us_limpio_V2.csv"
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


st.subheader('Precio vs Condición')
precio_vs_condition = df_cd.groupby('model_year')['condition_numeric'].mean().reset_index()

chart = alt.Chart(precio_vs_condition).mark_bar().encode(
    x=alt.X('model_year:O', title='Año del Modelo'),
    y=alt.Y('condition_numeric:Q', title='Condición Promedio'),
    tooltip=['model_year', 'condition_numeric']
).properties(
    width=600,
    height=400,
    title='Condición Promedio del Auto por Año de Modelo'
)
st.altair_chart(chart, use_container_width=True)


st.subheader('Histograma de Año')
ax = df_cd['model_year'].hist()
st.pyplot(ax.figure)

min_year = int(df_cd['model_year'].min())
max_year = int(df_cd['model_year'].max())
min_year_slide = st.slider('Selecciona el año mínimo de modelo', 
                     min_value=min_year, max_value=max_year, 
                     value=min_year)
st.dataframe(df_cd.query('model_year >= @min_year_slide'))


# Relacion precio-valor
year_range = st.slider("Selecciona el rango de años", min_year, max_year, (min_year, max_year))

df_filtrado = df_cd.query('model_year >= @year_range[0] and model_year <= @year_range[1]')
resumen = df_filtrado.groupby('model_year').agg({
    'price': 'mean',
    'odometer': 'mean',
    'condition_numeric': 'mean'
}).reset_index()

chart = alt.Chart(resumen).mark_circle().encode(
    x=alt.X('model_year:O', title='Año del Modelo'),
    y=alt.Y('price:Q', title='Precio Promedio $USD'),
    size=alt.Size('odometer:Q', title='Promedio de Odómetro', scale=alt.Scale(range=[10, 100])),
    color=alt.Color('condition_numeric:Q', title='Condición Promedio'),
    tooltip=['model_year', 'price', 'odometer', 'condition_numeric']
).properties(
    width=700,
    height=400,
    title='Relación Año - Precio - Condición - Odómetro'
)

st.altair_chart(chart, use_container_width=True)

condition_map = {'new': 5, 'like new': 4, 'excellent': 3, 'good': 2, 'fair': 1, 'salvage': 0}
df_cd['condition_numeric'] = df_cd['condition'].map(condition_map)
