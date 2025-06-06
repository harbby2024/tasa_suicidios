import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Sistema Académico", layout="wide")
st.title("🏫 Sistema de Gestión Académica")

# URLs de la API (debes reemplazarlas con tus endpoints reales)
API_ENDPOINTS = {
    "estudiantes": "https://horariosnuevo.onrender.com/api/estudiantes",
    "clases": "https://horariosnuevo.onrender.com/api/clases",
    "profesores": "https://horariosnuevo.onrender.com/api/profesores"
    "horarios": "https://horariosnuevo.onrender.com/api/horarios"

}

@st.cache_data(ttl=300)  # Cache de 5 minutos
def cargar_datos(tipo):
    try:
        response = requests.get(API_ENDPOINTS[tipo], timeout=30)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error al cargar {tipo}: {str(e)}")
        return pd.DataFrame()

# Cargar todos los datos
with st.spinner("Cargando datos académicos..."):
    estudiantes_df = cargar_datos("estudiantes")
    clases_df = cargar_datos("clases")
    profesores_df = cargar_datos("profesores")
    horarios_df = cargar_datos("horarios")

# Sidebar con selección de tabla principal
st.sidebar.header("🔍 Filtros Principales")
tabla_seleccionada = st.sidebar.selectbox(
    "Seleccionar tabla para visualizar",
    options=["Estudiantes", "Clases", "Profesores","horarios" ],
    index=0
)

# Función para mostrar tabla con filtros
def mostrar_tabla(titulo, df, columnas_filtro):
    st.header(f"📋 {titulo}")
    
    if df.empty:
        st.warning(f"No hay datos de {titulo.lower()} disponibles")
        return
    
    # Filtros dinámicos
    with st.expander("⚙️ Filtros Avanzados", expanded=False):
        cols = st.columns(3)
        filtros = {}
        
        for i, col in enumerate(columnas_filtro):
            if col in df.columns:
                with cols[i % 3]:
                    if df[col].dtype == 'object':
                        options = ['Todos'] + sorted(df[col].dropna().unique().tolist())
                        seleccion = st.selectbox(f"Filtrar por {col}", options)
                        if seleccion != 'Todos':
                            filtros[col] = seleccion
                    elif pd.api.types.is_numeric_dtype(df[col]):
                        min_val = float(df[col].min())
                        max_val = float(df[col].max())
                        seleccion = st.slider(f"Rango de {col}", min_val, max_val, (min_val, max_val))
                        filtros[col] = seleccion
    
    # Aplicar filtros
    df_filtrado = df.copy()
    for col, val in filtros.items():
        if isinstance(val, tuple):  # Para rangos numéricos
            df_filtrado = df_filtrado[(df_filtrado[col] >= val[0]) & (df_filtrado[col] <= val[1])]
        else:
            df_filtrado = df_filtrado[df_filtrado[col] == val]
    
    # Mostrar datos
    st.dataframe(df_filtrado, height=500, use_container_width=True)
    
    # Estadísticas
    st.subheader("📊 Estadísticas")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registros", len(df_filtrado))
    with col2:
        st.metric("Registros Filtrados", f"{len(df_filtrado)}/{len(df)}")
    with col3:
        if 'fecha' in df_filtrado.columns:
            st.metric("Última Actualización", df_filtrado['fecha'].max())
    
    # Exportar
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        f"⬇️ Exportar {titulo} como CSV",
        data=csv,
        file_name=f"{titulo.lower()}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Visualización según selección
if tabla_seleccionada == "Estudiantes":
    mostrar_tabla(
        "Estudiantes",
        estudiantes_df,
        ["nombre", "email", "carrera", "semestre"]
    )
    
    # Relación estudiantes-clases si existe la columna
    if 'clases' in estudiantes_df.columns and not clases_df.empty:
        st.header("🧑‍🎓 Clases por Estudiante")
        estudiantes_clases = estudiantes_df.explode('clases')
        estudiantes_clases = pd.merge(
            estudiantes_clases,
            clases_df,
            left_on='clases',
            right_on='id_clase',
            how='left'
        )
        st.dataframe(estudiantes_clases[['nombre', 'nombre_clase', 'horario']])

elif tabla_seleccionada == "Clases":
    mostrar_tabla(
        "Clases",
        clases_df,
        ["nombre_clase", "horario", "aula", "id_profesor"]
    )
    
    # Relación clases-profesores si existe la información
    if 'id_profesor' in clases_df.columns and not profesores_df.empty:
        st.header("👨‍🏫 Profesores por Clase")
        clases_profesores = pd.merge(
            clases_df,
            profesores_df,
            left_on='id_profesor',
            right_on='id_profesor',
            how='left'
        )
        st.dataframe(clases_profesores[['nombre_clase', 'nombre_profesor', 'departamento']])

elif tabla_seleccionada == "Profesores":
    mostrar_tabla(
        "Profesores",
        profesores_df,
        ["nombre", "departamento", "especialidad", "email"]
    )
    
    # Relación profesores-clases si existe
    if not clases_df.empty and 'id_profesor' in clases_df.columns:
        st.header("📚 Clases por Profesor")
        profesor_clases = clases_df.groupby('id_profesor')['nombre_clase'].count()
        st.bar_chart(profesor_clases)

# Actualización manual de datos
if st.sidebar.button("🔄 Actualizar Todos los Datos"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")