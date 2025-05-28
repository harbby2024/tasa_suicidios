import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Tasa de Suicidios en Antioquia")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_excel("static/datasets/Cantidad_anual_de_suicidios_reportados.xls")

df = load_data()

# Mostrar dataset
if st.checkbox("Mostrar datos completos"):
    st.dataframe(df)

# Filtros en la barra lateral
st.sidebar.header("Filtros")

# Filtro por rango de años
años = sorted(df["Año"].unique())
rango_años = st.sidebar.slider("Selecciona el rango de años", min_value=min(años), max_value=max(años), value=(min(años), max(años)))

# Filtro por región
regiones = sorted(df["NombreRegion"].dropna().unique())
region_seleccionada = st.sidebar.multiselect("Selecciona región", regiones, default=regiones)

# Filtro por municipio (depende de la región seleccionada)
municipios_disponibles = df[df["NombreRegion"].isin(region_seleccionada)]["NombreMunicipio"].unique()
municipios_seleccionados = st.sidebar.multiselect(
    "Selecciona municipios", sorted(municipios_disponibles), default=sorted(municipios_disponibles)
)

# Filtro por número de casos
min_casos = int(df["NumeroCasos"].min())
max_casos = int(df["NumeroCasos"].max())
rango_casos = st.sidebar.slider("Número de casos", min_casos, max_casos, (min_casos, max_casos))

# Filtro opcional: Municipios con mayor número de casos
top_n = st.sidebar.number_input("Escribe un número para mostrar los municipios con mayor  cantidad de casos", min_value=0, max_value=100, value=0)

# Aplicar filtros
df_filtrado = df[
    (df["Año"] >= rango_años[0]) &
    (df["Año"] <= rango_años[1]) &
    (df["NombreRegion"].isin(region_seleccionada)) &
    (df["NombreMunicipio"].isin(municipios_seleccionados)) &
    (df["NumeroCasos"] >= rango_casos[0]) &
    (df["NumeroCasos"] <= rango_casos[1])
]

# Agrupar por municipio si se seleccionan varios años
df_agrupado = df_filtrado.groupby("NombreMunicipio", as_index=False)["NumeroCasos"].sum()

# Aplicar filtro de Top N si es necesario
if top_n > 0:
    df_agrupado = df_agrupado.sort_values("NumeroCasos", ascending=False).head(top_n)

# Mostrar gráfico
if not df_agrupado.empty:
    fig = px.bar(
        df_agrupado,
        x="NombreMunicipio",
        y="NumeroCasos",
        title=f"Casos de Suicidio por Municipio ({rango_años[0]} - {rango_años[1]})",
        labels={"NumeroCasos": "Número de Casos"},
        height=500
    )
    st.plotly_chart(fig)
else:
    st.warning("No hay datos para los filtros seleccionados.")


st.subheader("📈 Variación Interanual de Casos por Municipio")

# Filtrar sin agrupar (para ver año a año)
df_interanual = df[
    (df["NombreRegion"].isin(region_seleccionada)) &
    (df["NombreMunicipio"].isin(municipios_seleccionados)) &
    (df["Año"] >= rango_años[0]) &
    (df["Año"] <= rango_años[1])
].copy()

# Ordenar y calcular variación por municipio
df_interanual.sort_values(["NombreMunicipio", "Año"], inplace=True)
df_interanual["Variacion"] = df_interanual.groupby("NombreMunicipio")["NumeroCasos"].pct_change() * 100

# Redondear variación
df_interanual["Variacion"] = df_interanual["Variacion"].round(2)

# Crear una copia del DataFrame para mostrar valores formateados
df_mostrar = df_interanual[["NombreMunicipio", "Año", "NumeroCasos", "Variacion"]].copy()

# Reemplazar valores infinitos por NaN o por un símbolo personalizado
df_mostrar["Variacion"].replace([float("inf"), float("-inf")], pd.NA, inplace=True)

# Formatear la columna Variacion como porcentaje con símbolo %
df_mostrar["Variacion"] = df_mostrar["Variacion"].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "—")

# Mostrar la tabla formateada
st.dataframe(df_mostrar, use_container_width=True)



st.subheader("📊 Evolución Temporal de Casos")

fig_line = px.line(
    df_interanual,
    x="Año",
    y="NumeroCasos",
    color="NombreMunicipio",
    markers=True,
    title="Evolución de Casos por Municipio",
    labels={"NumeroCasos": "Número de Casos"},
    height=500
)

st.plotly_chart(fig_line)

st.subheader("🧾 Resumen General de Datos Filtrados")

if df_filtrado.empty:
    st.info("No hay datos disponibles para mostrar un resumen con los filtros aplicados.")
else:
    total_casos = df_filtrado["NumeroCasos"].sum()
    total_municipios = df_filtrado["NombreMunicipio"].nunique()
    años_analizados = df_filtrado["Año"].nunique()
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
        st.metric("📅 Años cubiertos", f"{año_inicio} - {año_fin} ({años_analizados} años)")

    with col2:
        st.metric("📈 Municipio con más casos", f"{municipio_max['NombreMunicipio']} ({int(municipio_max['NumeroCasos'])} casos)")
        st.metric("📉 Municipio con menos casos", f"{municipio_min['NombreMunicipio']} ({int(municipio_min['NumeroCasos'])} casos)")
        st.metric("📊 Promedio por municipio", f"{promedio_municipio:.2f} casos")

    # Variación media si hay solo un municipio
    municipios_unicos = df_interanual["NombreMunicipio"].nunique()
    if municipios_unicos == 1:
        variacion_media = df_interanual["Variacion"].dropna().mean()
        st.info(f"📈 La variación media interanual para **{df_interanual['NombreMunicipio'].iloc[0]}** fue de **{variacion_media:.2f}%**.")







