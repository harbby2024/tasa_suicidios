# 📊 Análisis de la Tasa de Suicidios en Antioquia

Este proyecto es una aplicación interactiva construida con **Streamlit** para visualizar, analizar y explorar datos relacionados con los casos de suicidio reportados en el departamento de **Antioquia, Colombia**, a lo largo de varios años.

La app permite a los usuarios aplicar filtros por municipio, región, años y número de casos, y ofrece visualizaciones claras, como gráficos de barras, líneas y tablas con variaciones interanuales.

---

## 🚀 Funcionalidades principales

- 📅 Filtro por rango de **años**
- 🏙️ Filtro por **municipios** y **regiones**
- 🔢 Filtro por rango de **número de casos**
- 📈 Gráfico de barras por municipio
- 📉 Gráfico de variación interanual (%)
- 📊 Gráfico de evolución de casos por municipio
- 🧮 Tabla interactiva con número de casos y variación año a año

---

## 🛠️ Tecnologías y dependencias

Este proyecto fue desarrollado usando:

- [Python 3.8+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) - para crear la interfaz web interactiva
- [Pandas](https://pandas.pydata.org/) - para el análisis y manipulación de datos
- [Plotly Express](https://plotly.com/python/plotly-express/) - para gráficos interactivos
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) - para leer archivos Excel `.xls` o `.xlsx`

Consulta el archivo `requirements.txt` para ver la lista completa de dependencias.


## Instalación

1. Clona o descarga este repositorio en tu computadora

2. Crea un entorno virtual (opcional pero recomendado):
   ```
   python -m venv .venv
   ```

3. Activa el entorno virtual:
   - En Windows:
     ```
     .venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```
     source .venv/bin/activate
     ```

4. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la aplicación:

```
streamlit run Inicio.py
```

La aplicación estará disponible en tu navegador en `http://localhost:8501`.

## Estructura del proyecto

```
├── .streamlit/            # Configuración de Streamlit
│   └── config.toml        # Archivo de configuración (tema, servidor, etc.)
├── assets/                # Recursos estáticos
│   ├── foto.jpg           # Foto del estudiante
│   └── logo-Cesde-2023.svg # Logo de CESDE
├── data/                  # Carpeta para almacenar datos
├── pages/                 # Páginas de la aplicación
│   ├── Analisis.py        # Página de análisis de datos
├── .gitignore             # Archivos ignorados por Git
├── Inicio.py              # Punto de entrada de la aplicación
├── README.md              # Este archivo
└── requirements.txt       # Dependencias del proyecto
```

## Navegación por la aplicación

1. **Página de inicio (Inicio.py)**: Muestra información general del grupo de estudiantes y del curso.

2. **Pagina de análisis de datos (Analisis.py)**: Muestra gráficos y tablas para analizar los datos de casos de suicidio en Antioquia entre el año 2005 y 2022.

### Breve explicacion del funcionamiento de la aplicación

Para completar cada actividad o evaluación:

1. Selecciona la casilla de "Mostrar datos completos" para obtener los datos completos de los casos de suicidio. 
2. A continuacion, en el lateral izquierdo selecciona el año u años de referencia utlizando el slider.
3. Selecciona el municipio o zona de tu interés utilizando el multiselect, que te permitira seleccionar varias zonas.
4. Utiliza el slider para seleccionar el numero de casos de suicidio, esto filtrara los datos por el número de casos correspondiente a las zonas seleccionadas.
5. Puedes escribir un numero en el campo de "Escribe un número para mostrar los municipios con mayor  cantidad de casos" para mostrar los municipios ordenados por cantidad de casos de mayor a menor. Esto modificara todos los graficos y tablas, permitiendo visualizar los datos de manera más clara.

