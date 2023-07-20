import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos
df1 = pd.read_csv('Data_ingested/Accesos_a_Internet_fijo_por_velocidad_bajada_y_provincia.csv', encoding='UTF-8')
df2 = pd.read_csv('Data_ingested/Accesos_a_Internet_fijo_por_velocidad_de_bajada_y_localidad.csv', encoding='UTF-8')
df3 = pd.read_csv('Data_ingested/Conectividad_al_servicio_de_Internet.csv', encoding='UTF-8')
df4 = pd.read_csv('Data_ingested/historico_velocidad_internet.csv', encoding='UTF-8')
df5 = pd.read_csv('Data_ingested/Internet_Accesos-por-tecnologia.csv', encoding='UTF-8')
df6 = pd.read_csv('Data_ingested/Internet_Accesos-por-velocidad.csv', encoding='UTF-8')
df7 = pd.read_csv('Data_ingested/Internet_BAF.csv', encoding='UTF-8')
df8 = pd.read_csv('Data_ingested/Internet_Ingresos.csv', encoding='UTF-8')
df9 = pd.read_csv('Data_ingested/Internet_Penetracion.csv', encoding='UTF-8')
df10 = pd.read_csv('Data_ingested/Listado_de_localidades_con_conectividad_a_internet.csv', encoding='UTF-8')
df11 = pd.read_excel('Data_ingested/Metadatos_PBI.xlsx')
df12 = pd.read_excel('Data_ingested/PBI.xlsx')
df13 = pd.read_csv('Data_ingested/velocidad_internet_promedio.csv', encoding='UTF-8')

# Configurar la página
st.set_page_config(
    page_title="Data Analitys Enacom",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Establecer el estilo del dashboard
st.markdown(
    """
    <style>
    .reportview-container {
        background: radial-gradient(#1a1a1a, #000000);
        color: white;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(#1a1a1a, #000000);
        color: white;
    }
    .Widget>label {
        color: white;
        font-family: "Arial", sans-serif;
    }
    .stButton>button {
        background-color: #292929;
        color: white;
        border: 2px solid white;
        border-radius: 12px;
        box-shadow: 2px 2px 4px rgba(255, 255, 255, 0.2);
    }
    .stButton>button:hover {
        background-color: #393939;
    }
    footer {
        font-family: "Arial", sans-serif;
        color: white;
        background-color: #1a1a1a;
        padding: 8px;
        border-top: 1px solid white;
    }
    .stTextInput>div>div>input {
        background-color: #333333 !important;
        color: white !important;
        border: 1px solid white !important;
        border-radius: 8px;
    }
    .stTextInput>div>div>input:focus {
        outline: none;
        border: 2px solid #6c6c6c !important;
    }
    .stDataFrame {
        border: 1px solid white;
        border-radius: 12px;
    }
    .stDataFrame>div>div {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    .stVegaLiteChart {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
    }
    .stMap {
        border-radius: 12px;
        box-shadow: 4px 4px 8px rgba(255, 255, 255, 0.2);
    }
    .stDeckGlChart {
        border-radius: 12px;
    }
    .stGraphvizChart {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título del dashboard
st.title("Data Analitys Enacom")

# Filtros interactivos
with st.sidebar:
    st.header("Filtro:")
    provincia_filter = st.selectbox('Provincia', df3['Provincia'].unique())
    year_filter = st.slider('Año', 2010, 2023, 2021)

# Sección de KPIs (Cajitas)
st.header("KPIs")
st.markdown("Los Kpis seleccionados mas importantes fueron:")

# Aquí puedes agregar tus cajitas de KPIs, por ejemplo:
st.info("KPI Crecimiento anual provincia: 3%")
st.warning("KPI Aumento Fibra optica: 3%")
st.error("KPI Crecimiento por cada 100 Hogares: 5%")




# ... (código para otras visualizaciones y datos en tiempo real)

# Sección de Datos de Accesos a Internet por Tecnología
st.header('Datos de Accesos a Internet por Tecnología')
st.dataframe(df5)

# Eliminar caracteres no numéricos y convertir a tipo numérico
# (código para limpiar y convertir datos)

# Obtener el recuento de registros únicos por provincia
df_counts = df3['Provincia'].value_counts().reset_index()
df_counts.columns = ['Provincia', 'Cantidad']

# Crear el gráfico de barras con Plotly Express
fig = px.bar(df_counts, x='Provincia', y='Cantidad', title='Cantidad de Registros por Provincia')

# Mostrar el gráfico utilizando Streamlit
st.plotly_chart(fig)

# Crear el gráfico de barras apiladas
df_connection_counts_localidad = df3.groupby(['Provincia', 'Localidad']).agg({
    'ADSL': 'sum',
    'CABLEMODEM': 'sum',
    'DIALUP': 'sum',
    'FIBRAOPTICA': 'sum',
    'SATELITAL': 'sum',
    'WIRELESS': 'sum',
    'TELEFONIAFIJA': 'sum',
    '3G': 'sum',
    '4G': 'sum'
}).reset_index()

df_connection_counts_localidad_melt = df_connection_counts_localidad.melt(id_vars=['Provincia', 'Localidad'], var_name='Tipo de Conexión', value_name='Cantidad')

fig_bar_stacked = px.bar(df_connection_counts_localidad_melt, x='Provincia', y='Cantidad', color='Tipo de Conexión',
                         title='Distribución de Tipos de Conexión por Localidad y Provincia', barmode='stack')

# Mostrar el gráfico utilizando Streamlit
st.plotly_chart(fig_bar_stacked)

# Crear el gráfico de dispersión con Plotly Express
fig_scatter = px.scatter(df3, x='Longitud', y='Latitud', size='Poblacion', color='Provincia',
                         title='Dispersión de la Población según Latitud y Longitud')

# Mostrar el gráfico utilizando Streamlit
st.plotly_chart(fig_scatter)

# Obtener el recuento de registros por provincia
df_counts = df3['Provincia'].value_counts().reset_index()
df_counts.columns = ['Provincia', 'Recuento']

# Función para crear el gráfico de pastel
def create_pie_chart(provincia_seleccionada, tecnologia_seleccionada):
    # Filtrar el DataFrame por la provincia seleccionada
    df_provincia = df3[df3['Provincia'] == provincia_seleccionada]

    # Contar la cantidad de registros para la tecnología seleccionada
    counts = df_provincia[tecnologia_seleccionada].value_counts()
    labels = counts.index
    values = counts.values

    # Calcular el porcentaje
    total = values.sum()
    porcentajes = [f'{(value / total) * 100:.2f}%' for value in values]

    # Crear el gráfico de pastel con Plotly Express
    fig_pie = px.pie(values=values, names=labels, labels=porcentajes, title=f'Porcentaje de {tecnologia_seleccionada} en {provincia_seleccionada}')

    return fig_pie

# Seleccionar una provincia para mostrar el gráfico
provincia_seleccionada = st.selectbox('Selecciona una provincia:', df3['Provincia'].unique())

# Seleccionar la tecnología que deseas ver en el gráfico de pastel
tecnologia_seleccionada = st.radio('Selecciona una tecnología:', ['ADSL', 'CABLEMODEM', 'DIALUP', 'FIBRAOPTICA', 'SATELITAL', 'WIRELESS', 'TELEFONIAFIJA', '3G', '4G'])

# Crear y mostrar el gráfico de pastel
fig_pie = create_pie_chart(provincia_seleccionada, tecnologia_seleccionada)
st.plotly_chart(fig_pie)


# Crear el mapa utilizando Plotly Express
fig = px.choropleth(df_counts, 
                    locations='Provincia', 
                    locationmode='country names',
                    color='Recuento',
                    color_continuous_scale='Blues',
                    hover_name='Provincia',
                    title='Recuento de Registros por Provincia',
                    labels={'Recuento': 'Cantidad de Registros'})

# Mostrar el mapa utilizando Streamlit
st.plotly_chart(fig)