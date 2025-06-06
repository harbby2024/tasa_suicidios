import streamlit as st
import base64

# Configuración de la página
st.set_page_config(
    page_title="Nuevas Tecnologías de Programación",
    page_icon="💻",
    layout="wide"
)

# Aplicar estilos personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #003366;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0066cc;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .stButton > button {
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton > button:hover {
        background-color: #003366;
    }
    .highlight {
        color: #0066cc;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Función para cargar y mostrar el logo SVG
def get_svg_logo():
    with open("assets/logo-Cesde-2023.svg", "r") as file:
        svg_content = file.read()
    # Ajustar el tamaño del SVG
    svg_content = svg_content.replace('viewBox="0 0 264 53"', 'viewBox="0 0 264 53" width="300"')
    return svg_content

# Mostrar el logo de CESDE
st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'>{get_svg_logo()}</div>", unsafe_allow_html=True)

# Encabezados
st.markdown('<h1 class="main-header">Nuevas Tecnologías de Programación</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">Programa de Desarrollo de Software</h2>', unsafe_allow_html=True)

# Agregar estilos adicionales para la sección del estudiante
st.markdown('''
<style>
    .student-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        margin: 0 auto;
        padding: 20px;
    }
    .student-image {
        flex: 0 0 auto;
        margin-right: 30px;
    }
    .student-info {
        flex: 1 1 auto;
        text-align: left;
        padding-left: 20px;
    }
    .info-label {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .info-value {
        color: #0066cc;
        font-weight: bold;
        margin-bottom: 15px;
    }
    /* Ajustes para la imagen */
    .student-image img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    /* Ajustes para el contenedor de columnas */
    .student-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        width: 100%;
        margin: 20px auto;
    }
    .student-column-left {
        flex: 0 0 auto;
        padding-right: 20px;
    }
    .student-column-right {
        flex: 1 1 auto;
        padding-left: 20px;
        border-left: 1px solid #eee;
    }
</style>
''', unsafe_allow_html=True)

# Sección de información del estudiante con diseño de dos columnas
col1, col2 = st.columns([1, 2])

# Columna izquierda: Foto del estudiante
with col1:
    st.image("asset/img-grupo.png", width=200, caption="Foto del grupo de estudiantes")

# Columna derecha: Información del estudiante
with col2:
    st.markdown('<h3 style="color: #0066cc; margin-top: 5px;">Alejandra Suarez</h3>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #0066cc; margin-top: 5px;">Andres Tobon</h3>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #0066cc; margin-top: 5px;">Melissa Suarez</h3>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #0066cc; margin-top: 5px;">Alejandra Morales</h3>', unsafe_allow_html=True)
    st.markdown('<p style="margin-top: 10px;">Programa: <span style="color: #0066cc; font-weight: bold;">Desarrollo de Software</span></p>', unsafe_allow_html=True)
    st.markdown('<p>Semestre: <span style="color: #0066cc; font-weight: bold;">2025-1</span></p>', unsafe_allow_html=True)
    st.markdown('<p>Repositorio: <a href="https://github.com/mari4l3/tasa_suicidios" target="_blank" style="color: #0066cc; font-weight: bold; text-decoration: none;">GitHub</a></p>', unsafe_allow_html=True)
    st.markdown('<p>Streamlit: <a href="https://tasasuicidios.streamlit.app/" target="_blank" style="color: #0066cc; font-weight: bold; text-decoration: none;">Streamlit</a></p>', unsafe_allow_html=True)
   

with st.expander("ℹ️ Acerca del Proyecto", expanded=True):
    st.markdown("""
    ### 🎯 Objetivo General
    Este panel interactivo tiene como propósito analizar y visualizar la evolución de los casos reportados de suicidio en los municipios del departamento de **Antioquia**, Colombia, desde el año **2005** hasta **2022**.

    ---
    ### 🧭 Acercamiento Metodológico
    - Se trabajó con una base de datos histórica suministrada en formato Excel, organizada por año, municipio y número de casos reportados.
    - Se normalizaron y filtraron los datos para asegurar la coherencia en los nombres de municipios y años.
    - Se crearon visualizaciones interactivas que permiten a los usuarios explorar **tendencias temporales**, **comparaciones por regiones**, y **diferencias frente al promedio histórico**.

    ---
    ### ✅ Propósito del Panel
    Este panel busca:
    - Facilitar la **exploración visual** de los datos para instituciones, investigadores o ciudadanos interesados.
    - Ofrecer una herramienta que permita identificar posibles patrones o alertas en el comportamiento del fenómeno del suicidio.
    - Promover una base de análisis para estrategias de **intervención, prevención y concientización** en salud mental pública.

    ---
    **Nota:** Los datos utilizados provienen de fuentes oficiales y fueron tratados con fines exclusivamente analíticos y de visualización. Este proyecto no busca emitir juicios, sino contribuir al entendimiento del fenómeno.
    """)


# Pie de página
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    © 2025 CESDE      
</div>
""", unsafe_allow_html=True)