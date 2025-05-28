import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.title("📊 Análisis Visual y Exportación de Datos")

@st.cache_data
def load_data():
    return pd.read_excel("static/datasets/Cantidad_anual_de_suicidios_reportados.xls")

df = load_data()

# ======= Filtros básicos y claros =======
st.sidebar.header("Filtros")

años = sorted(df["Año"].unique())
año_seleccionado = st.sidebar.selectbox("Selecciona un año para comparar", años, index=len(años)-1)

# Filtro 1: Municipios con casos acumulados mayores a un mínimo
df_acumulado = df.groupby("NombreMunicipio", as_index=False)["NumeroCasos"].sum()
min_casos = st.sidebar.slider("Mostrar municipios con al menos N casos en total", 0, int(df_acumulado["NumeroCasos"].max()), 10)
municipios_validos = df_acumulado[df_acumulado["NumeroCasos"] >= min_casos]["NombreMunicipio"]
df_filtrado = df[df["NombreMunicipio"].isin(municipios_validos)]

# Filtro 2: Comparar con promedio general
promedio_general = df.groupby("NombreMunicipio")["NumeroCasos"].mean().reset_index()
promedio_general.columns = ["NombreMunicipio", "PromedioGeneral"]
df_ultimo = df[df["Año"] == año_seleccionado]
df_comparado = df_ultimo.merge(promedio_general, on="NombreMunicipio")
df_comparado["Diferencia"] = df_comparado["NumeroCasos"] - df_comparado["PromedioGeneral"]

comparacion = st.sidebar.radio("Comparar el año seleccionado con el promedio general", ["Todos", "Mayor al promedio", "Menor al promedio"])
if comparacion != "Todos":
    cond = df_comparado["Diferencia"] > 0 if comparacion == "Mayor al promedio" else df_comparado["Diferencia"] < 0
    municipios_comparados = df_comparado[cond]["NombreMunicipio"]
    df_filtrado = df_filtrado[df_filtrado["NombreMunicipio"].isin(municipios_comparados)]

# ======= Gráficos =======
st.subheader("📈 Evolución anual por municipio")

df_lineas = df_filtrado[df_filtrado["NombreMunicipio"].isin(df_filtrado["NombreMunicipio"].unique())]
fig_line = px.line

# Pivotar los datos para tener Municipios en filas y Años en columnas
df_pivot = df_lineas.pivot_table(
    index="NombreMunicipio",
    columns="Año",
    values="NumeroCasos",
    aggfunc='sum',
    fill_value=0
)

fig_heatmap = px.imshow(
    df_pivot,
    labels=dict(x="Año", y="Municipio", color="Número de Casos"),
    x=df_pivot.columns,
    y=df_pivot.index,
    color_continuous_scale='Viridis',
    aspect="auto",
    title="Heatmap de Casos de Suicidio por Municipio y Año"
)

st.plotly_chart(fig_heatmap)

st.subheader("📊 Comparación del último año vs promedio general")
df_plot = df_comparado[df_comparado["NombreMunicipio"].isin(df_filtrado["NombreMunicipio"].unique())]
fig_bar = px.bar(
    df_plot,
    x="NombreMunicipio",
    y=["NumeroCasos", "PromedioGeneral"],
    barmode="group",
    title=f"Casos en {año_seleccionado} vs Promedio histórico",
    labels={"value": "Casos", "variable": "Tipo"},
    height=500
)
st.plotly_chart(fig_bar)

st.subheader("📍 Datos tabulares")
st.dataframe(df_filtrado, use_container_width=True)

# ======= Exportar a Excel =======
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Datos')
    writer.close()
    return output.getvalue()

excel_data = to_excel(df_filtrado)
st.download_button(
    label="📥 Descargar en Excel",
    data=excel_data,
    file_name="datos_suicidios.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ======= Exportar a PDF =======

def to_pdf(df):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    text = c.beginText(40, height - 40)
    text.setFont("Helvetica-Bold", 12)
    text.textLine("Informe de Casos de Suicidio en Antioquia")
    text.setFont("Helvetica", 10)
    text.textLine("")

    if df.empty:
        text.textLine("No hay datos disponibles para los filtros aplicados.")
    else:
        # Estadísticas clave
        total_casos = df["NumeroCasos"].sum()
        total_municipios = df["NombreMunicipio"].nunique()
        año_inicio = df["Año"].min()
        año_fin = df["Año"].max()

        resumen_agrupado = df.groupby("NombreMunicipio")["NumeroCasos"].sum().reset_index()
        municipio_max = resumen_agrupado.loc[resumen_agrupado["NumeroCasos"].idxmax()]
        municipio_min = resumen_agrupado.loc[resumen_agrupado["NumeroCasos"].idxmin()]
        mediana = resumen_agrupado["NumeroCasos"].median()

        text.textLine(f"🔢 Total de casos reportados: {int(total_casos):,}")
        text.textLine(f"🏘️ Municipios analizados: {total_municipios}")
        text.textLine(f"📅 Rango de años: {año_inicio} - {año_fin}")
        text.textLine(f"📈 Municipio con más casos: {municipio_max['NombreMunicipio']} ({int(municipio_max['NumeroCasos'])})")
        text.textLine(f"📉 Municipio con menos casos: {municipio_min['NombreMunicipio']} ({int(municipio_min['NumeroCasos'])})")
        text.textLine(f"📊 Mediana de casos por municipio: {mediana:.2f}")
        text.textLine("")

        # Tabla básica de datos
        text.setFont("Helvetica-Bold", 11)
        text.textLine("📍 Casos por municipio (máximo 30 filas):")
        text.setFont("Helvetica", 9)

        rows = df[["NombreMunicipio", "Año", "NumeroCasos"]].head(30).values.tolist()
        for row in rows:
            line = f"{row[0]} - Año {row[1]}: {row[2]} casos"
            text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

    # ======= Exportar a PDF =======
pdf_data = to_pdf(df_filtrado)

st.download_button(
    label="📄 Descargar en PDF (resumen)",
    data=pdf_data,
    file_name="reporte_suicidios.pdf",
    mime="application/pdf"
)



st.subheader("🧾 Resumen de Datos Filtrados")

if df_filtrado.empty:
    st.info("No hay datos disponibles para mostrar un resumen con los filtros aplicados.")
else:
    total_casos = df_filtrado["NumeroCasos"].sum()
    total_municipios = df_filtrado["NombreMunicipio"].nunique()
    año_inicio = df_filtrado["Año"].min()
    año_fin = df_filtrado["Año"].max()

    resumen_agrupado = df_filtrado.groupby("NombreMunicipio")["NumeroCasos"].sum().reset_index()
    municipio_max = resumen_agrupado.loc[resumen_agrupado["NumeroCasos"].idxmax()]
    municipio_min = resumen_agrupado.loc[resumen_agrupado["NumeroCasos"].idxmin()]
    promedio_municipio = resumen_agrupado["NumeroCasos"].mean()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🔢 Total de casos reportados", f"{int(total_casos):,}")
        st.metric("🏘️ Municipios analizados", total_municipios)
        st.metric("📅 Rango de años", f"{año_inicio} - {año_fin}")

    with col2:
        st.metric("📈 Municipio con más casos", f"{municipio_max['NombreMunicipio']} ({int(municipio_max['NumeroCasos'])})")
        st.metric("📉 Municipio con menos casos", f"{municipio_min['NombreMunicipio']} ({int(municipio_min['NumeroCasos'])})")
        st.metric("📊 Mediana de casos por municipio", f"{resumen_agrupado['NumeroCasos'].median():.2f} casos")

