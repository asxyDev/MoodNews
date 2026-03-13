# 🌍 MoodNews: Analizador de Sentimiento Global
WebPage de prueba: https://moodnews-alan.streamlit.app/
MoodNews es un proyecto personal construido para explorar la integración de APIs web, el análisis de datos y el Procesamiento de Lenguaje Natural (NLP). 

La aplicación funciona como un buscador interactivo que recopila las noticias más recientes sobre cualquier tema (o categoría) y evalúa el "humor" o sentimiento general de los titulares para determinar si la opinión mediática es positiva, negativa o neutral.

## 🎯 Objetivo del Proyecto
Desarrollé esta herramienta como una práctica para entender cómo conectar diferentes tecnologías en un solo flujo de trabajo: desde la extracción de datos en tiempo real hasta su visualización en un dashboard web. No pretende ser un motor de análisis a nivel empresarial, sino una prueba de concepto funcional sobre cómo interactúan los datos en la web.

## 🛠️ Tecnologías y Librerías Utilizadas
* **Python**: Lenguaje principal.
* **Streamlit**: Para construir la interfaz web y manejar el estado de la sesión (`session_state`).
* **NewsAPI**: Para extraer los artículos y titulares más recientes.
* **TextBlob**: Para el análisis de sentimiento (NLP) de los textos.
* **Plotly & Pandas**: Para la limpieza de datos y la creación de gráficos interactivos (Radar y Pie charts).
* **Deep-Translator**: Para permitir búsquedas en español traduciéndolas al inglés (donde hay mayor volumen de datos) de forma invisible.

## ✨ Funcionalidades Principales
1. **Búsqueda Dinámica**: Los usuarios pueden ingresar cualquier tema o seleccionar categorías predefinidas (Tecnología, Ciencia, etc.).
2. **Dashboard de Sentimiento**: Calcula un puntaje de 0 a 100 y muestra cómo se distribuye la opinión entre los diferentes medios de comunicación.
3. **Persistencia de Datos**: Uso de la memoria de sesión de Streamlit para guardar un historial de noticias "Favoritas" sin necesidad de una base de datos externa.

## 🚀 Cómo ejecutarlo localmente

1. Clona este repositorio a tu computadora.
2. Instala las dependencias necesarias ejecutando: `pip install -r requirements.txt`
3. Reemplaza la variable `API_KEY` en el archivo principal con tu propia llave gratuita de NewsAPI.

4. Ejecuta la aplicación desde tu terminal con el comando: `streamlit run moodnews.py`

