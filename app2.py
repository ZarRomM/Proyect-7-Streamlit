import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import altair as alt

# Título principal de la aplicación
st.title('Análisis de Vehículos Usados en EE.UU.')

# Lectura de los datos desde un archivo CSV en línea
url_data = "https://raw.githubusercontent.com/ZarRomM/Proyect-7-Streamlit/main/vehicles_us_limpio_V2.csv"
df_cd = pd.read_csv(url_data)

# Muestra el DataFrame completo
st.header('DataFrame US Cars')
st.dataframe(df_cd)

# Filtramos precios extremos que distorsionan el histograma (outliers)
df_filtrado = df_cd[(df_cd['price'] >= 1000) & (df_cd['price'] <= 100000)]

# Histograma para visualizar la cantidad de vehículos por rango de precio
mostrar = st.button('Mostrar Histograma')
if mostrar:
    st.header('Distribución de Precios')
    fig, ax = plt.subplots()
    sns.histplot(df_filtrado['price'], bins=30, kde=False, ax=ax, color='#0077b6')
    ax.set_xlabel('Precio')
    ax.set_ylabel('Cantidad de vehículos')
    st.pyplot(fig)

# Diagrama de dispersión para visualizar cómo varía el precio con el odómetro
mostrar_2 = st.button('Mostrar Gráfico de Dispersión')
if mostrar_2:
    st.header('Precio vs. Odómetro')
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x='odometer', y='price', data=df_cd, ax=ax2, alpha=0.5)
    ax2.set_xlabel('Odómetro (millas)')
    ax2.set_ylabel('Precio')
    st.pyplot(fig2)

# Casilla para mostrar el DataFrame si el usuario lo desea
if st.checkbox('Mostrar información del DataFrame'):
    buffer = df_cd.dtypes.to_frame(name='Tipo de Dato')
    buffer['Valores No Nulos'] = df_cd.notnull().sum()
    buffer['Valores Nulos'] = df_cd.isnull().sum()
    buffer['Únicos'] = df_cd.nunique()
    st.dataframe(buffer)


# Sección: Precio vs Condición Promedio por Año de Modelo
st.subheader('Precio vs Condición')

# Mapeo numérico de la condición para análisis cuantitativo
condition_map = {'new': 5, 'like new': 4, 'excellent': 3, 'good': 2, 'fair': 1, 'salvage': 0}
df_cd['condition_numeric'] = df_cd['condition'].map(condition_map)

# Promedio de condición por año de modelo
precio_vs_condition = df_cd.groupby('model_year')['condition_numeric'].mean().reset_index()

# Gráfico de barras con Altair
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

# Sección: Histograma del año de modelo
st.subheader('Histograma de Año')
ax = df_cd['model_year'].hist()
st.pyplot(ax.figure)

# Define los límites del año mínimo y máximo para los sliders
min_year = int(df_cd['model_year'].min())
max_year = int(df_cd['model_year'].max())

# Slider para seleccionar el año mínimo de modelo
min_year_slide = st.slider(
    'Selecciona el año mínimo de modelo', 
    min_value=min_year, 
    max_value=max_year, 
    value=min_year
)

# Filtro aplicado usando el slider de año mínimo
st.dataframe(df_cd.query('model_year >= @min_year_slide'))

# Sección: Relación completa entre variables usando filtros de rango de años
st.subheader('Relación Año - Precio - Condición - Odómetro')

# Slider para seleccionar un rango de años completo
year_range = st.slider(
    "Selecciona el rango de años", 
    min_year, 
    max_year, 
    (min_year, max_year)
)

# Filtro del DataFrame según el rango de años seleccionado
df_filtrado = df_cd.query('model_year >= @year_range[0] and model_year <= @year_range[1]')

# Agrupación por año de modelo y cálculo de promedios
resumen = df_filtrado.groupby('model_year').agg({
    'price': 'mean',
    'odometer': 'mean',
    'condition_numeric': 'mean'
}).reset_index()

# Gráfico de burbujas usando Altair
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
